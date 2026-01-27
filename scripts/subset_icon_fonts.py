#!/usr/bin/env python3
"""
Subset icon fonts to only the glyphs actually used by this site.

Why:
- Smaller font files -> faster first load and faster icon rendering.
- Still keep the same CSS classes (`fa-...`, `ai-...`) and font families.

How to maintain:
- Whenever you add/remove icons in templates/CSS/JS, re-run this script.
  It auto-scans the repo, so you do NOT need to manually maintain a list.

This script rewrites:
- assets/webfonts/fa-solid-900.woff2 (from fa-solid-900.ttf)
- assets/webfonts/fa-brands-400.woff2 (from fa-brands-400.ttf)
- assets/fonts/academicons.woff (from academicons.ttf)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


ROOT = Path(__file__).resolve().parents[1]


SCAN_ROOTS = [
    ROOT / "_includes",
    ROOT / "_layouts",
    ROOT / "_pages",
    ROOT / "_data",
    ROOT / "_sass",
    ROOT / "assets" / "js",
]

SKIP_DIR_NAMES = {
    ".git",
    "_site",
    "node_modules",
    "vendor",
    ".bundle",
    ".jekyll-cache",
}

# Vendor / mapping sources: we parse them separately; don't treat them as usage.
SKIP_PATH_PARTS = {
    ("_sass", "font-awesome"),
    ("_sass", "tabler-icons"),
    # Vendor JS (can contain lots of false positives).
    ("assets", "js", "distillpub"),
}

SKIP_FILES = {
    # Contains definitions for every Academicons glyph; not usage.
    Path("assets/css/academicons.min.css"),
    # Notebook themes reference old FontAwesome; not part of this site's icon usage.
    Path("assets/css/jupyter-grade3.css"),
    Path("assets/css/jupyter-monokai.css"),
}

TEXT_EXTS = {
    ".liquid",
    ".html",
    ".md",
    ".scss",
    ".css",
    ".js",
    ".yml",
    ".yaml",
}


FA_TOKEN_RE = re.compile(r"\bfa-([a-z0-9-]+)\b", re.IGNORECASE)
AI_TOKEN_RE = re.compile(r"\bai-([a-z0-9-]+)\b", re.IGNORECASE)

# CSS escapes like: content: "\f08e";
CSS_UNICODE_RE = re.compile(r'content\s*:\s*["\']\\([0-9a-fA-F]{3,6})["\']')


FA_IGNORE = {
    # Styles
    "solid",
    "regular",
    "brands",
    # Sizes
    "xs",
    "sm",
    "lg",
    "xl",
    "2xl",
    "1x",
    "2x",
    "3x",
    "4x",
    "5x",
    "6x",
    "7x",
    "8x",
    "9x",
    "10x",
    # Utilities / animation / layout
    "fw",
    "ul",
    "li",
    "border",
    "inverse",
    "stack",
    "stack-1x",
    "stack-2x",
    "pull-left",
    "pull-right",
    "rotate-90",
    "rotate-180",
    "rotate-270",
    "flip",
    "flip-horizontal",
    "flip-vertical",
    "spin",
    "spin-reverse",
    "pulse",
    "bounce",
    "beat",
    "fade",
    "shake",
    # Our own "font loaded" gate classes + file-name fragments.
    "solid-loaded",
    "brands-loaded",
    "solid-900",
    "brands-400",
    "font-path",
}

AI_IGNORE = {
    # Sizes
    "xs",
    "sm",
    "lg",
    "1x",
    "2x",
    "3x",
    "4x",
    "5x",
    "6x",
    "7x",
    "8x",
    "9x",
    "10x",
    # Utilities / layout
    "fw",
    "ul",
    "li",
    "border",
    "inverse",
    "stack",
    "stack-1x",
    "stack-2x",
    "pull-left",
    "pull-right",
    # Our own "font loaded" gate class.
    "loaded",
}


@dataclass(frozen=True)
class FontJob:
    name: str
    input_path: Path
    output_path: Path
    flavor: str  # "woff2" or "woff"
    unicodes: Set[int]


def iter_scan_files() -> Iterable[Path]:
    for base in SCAN_ROOTS:
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if path.is_dir():
                # Skip heavy directories early.
                if path.name in SKIP_DIR_NAMES:
                    continue
                continue

            rel = path.relative_to(ROOT)

            if rel in SKIP_FILES:
                continue

            if path.suffix.lower() not in TEXT_EXTS:
                continue

            # Skip vendor scss trees.
            parts = rel.parts
            skip = False
            for prefix in SKIP_PATH_PARTS:
                if parts[: len(prefix)] == prefix:
                    skip = True
                    break
            if skip:
                continue

            # Skip generated / cache dirs if nested under scan roots.
            if any(p in SKIP_DIR_NAMES for p in parts):
                continue

            yield path


def read_text(path: Path) -> str:
    # Use 'utf-8' but tolerate odd files.
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_fa_mappings(variables_scss: Path) -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    Returns:
      (classic_icons, brand_icons) where keys are icon names without 'fa-'.
    """
    text = read_text(variables_scss)

    var_map: Dict[str, int] = {}
    var_re = re.compile(r"^\$fa-var-([a-z0-9-]+):\s*\\([0-9a-fA-F]+);", re.MULTILINE)
    for m in var_re.finditer(text):
        var_map[m.group(1)] = int(m.group(2), 16)

    classic: Dict[str, int] = {}
    brands: Dict[str, int] = {}

    section = None
    for line in text.splitlines():
        if line.startswith("$fa-icons:"):
            section = "classic"
            continue
        if line.startswith("$fa-brand-icons:"):
            section = "brands"
            continue
        if section and line.strip() == ");":
            section = None
            continue

        if not section:
            continue

        m = re.search(r'"([^"]+)":\s*\$fa-var-([a-z0-9-]+)', line)
        if not m:
            continue

        icon_name = m.group(1)
        var_name = m.group(2)
        codepoint = var_map.get(var_name)
        if codepoint is None:
            continue

        if section == "brands":
            brands[icon_name] = codepoint
        else:
            classic[icon_name] = codepoint

    return classic, brands


def parse_academicons_mapping(academicons_css: Path) -> Dict[str, int]:
    """
    Returns mapping from ai icon name (without `ai-`) to codepoint int.
    """
    text = read_text(academicons_css)
    mapping: Dict[str, int] = {}

    # Matches e.g.: .ai-arxiv:before {content: "\e974";}
    re_ai = re.compile(r"\.ai-([a-z0-9-]+):before\s*\{content:\s*\"\\([0-9a-fA-F]+)\"", re.IGNORECASE)
    for m in re_ai.finditer(text):
        mapping[m.group(1)] = int(m.group(2), 16)

    return mapping


def collect_used_icons(files: Iterable[Path]) -> Tuple[Set[str], Set[str], Set[int]]:
    """
    Returns:
      (fa_names, ai_names, raw_unicode_escapes)
    where:
      - fa_names: icon names without 'fa-'
      - ai_names: icon names without 'ai-'
      - raw_unicode_escapes: codepoints referenced directly in CSS `content: "\\xxxx"`
    """
    fa_names: Set[str] = set()
    ai_names: Set[str] = set()
    raw_codes: Set[int] = set()

    for path in files:
        text = read_text(path)

        for m in FA_TOKEN_RE.finditer(text):
            name = m.group(1).lower()
            if name in FA_IGNORE:
                continue
            fa_names.add(name)

        for m in AI_TOKEN_RE.finditer(text):
            name = m.group(1).lower()
            if name in AI_IGNORE:
                continue
            ai_names.add(name)

        for m in CSS_UNICODE_RE.finditer(text):
            raw_codes.add(int(m.group(1), 16))

    return fa_names, ai_names, raw_codes


def format_unicodes_arg(codepoints: Set[int]) -> str:
    return ",".join(f"U+{cp:04X}" for cp in sorted(codepoints))


def subset_font(job: FontJob, *, dry_run: bool) -> None:
    if not job.unicodes:
        print(f"[skip] {job.name}: no glyphs to keep")
        return

    if not job.input_path.exists():
        raise FileNotFoundError(f"Missing input font: {job.input_path}")

    before = job.output_path.stat().st_size if job.output_path.exists() else 0
    unicodes_arg = format_unicodes_arg(job.unicodes)

    # Write to a temp file, then replace atomically.
    tmp = job.output_path.with_suffix(job.output_path.suffix + ".tmp")

    cmd = [
        sys.executable,
        "-m",
        "fontTools.subset",
        str(job.input_path),
        f"--output-file={tmp}",
        f"--flavor={job.flavor}",
        f"--unicodes={unicodes_arg}",
        "--layout-features=*",
        "--no-hinting",
        "--desubroutinize",
    ]

    print(f"[run] {job.name}: {len(job.unicodes)} glyphs -> {job.output_path.relative_to(ROOT)}")
    if dry_run:
        print("      (dry-run) " + " ".join(cmd))
        return

    subprocess.run(cmd, check=True, cwd=str(ROOT))
    tmp.replace(job.output_path)

    after = job.output_path.stat().st_size if job.output_path.exists() else 0
    if before and after:
        delta = after - before
        sign = "+" if delta >= 0 else "-"
        print(f"      size: {before} -> {after} bytes ({sign}{abs(delta)})")


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Subset icon fonts used by this site.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    parser.add_argument("--print-icons", action="store_true", help="Print detected icon names.")
    args = parser.parse_args(argv)

    fa_vars = ROOT / "_sass" / "font-awesome" / "_variables.scss"
    academicons_css = ROOT / "assets" / "css" / "academicons.min.css"

    classic_map, brand_map = parse_fa_mappings(fa_vars)
    ai_map = parse_academicons_mapping(academicons_css)

    scan_files = list(iter_scan_files())
    fa_names, ai_names, raw_codes = collect_used_icons(scan_files)

    # Resolve names to codepoints.
    fa_solid_codes: Set[int] = set()
    fa_brand_codes: Set[int] = set()
    ai_codes: Set[int] = set()

    missing_fa: Set[str] = set()
    for name in sorted(fa_names):
        if name in brand_map:
            fa_brand_codes.add(brand_map[name])
        elif name in classic_map:
            fa_solid_codes.add(classic_map[name])
        else:
            missing_fa.add(name)

    missing_ai: Set[str] = set()
    for name in sorted(ai_names):
        cp = ai_map.get(name)
        if cp is None:
            missing_ai.add(name)
        else:
            ai_codes.add(cp)

    # Also include explicit CSS content escapes, but only if they belong to our maps.
    classic_vals = set(classic_map.values())
    brand_vals = set(brand_map.values())
    ai_vals = set(ai_map.values())
    for cp in raw_codes:
        if cp in classic_vals:
            fa_solid_codes.add(cp)
        elif cp in brand_vals:
            fa_brand_codes.add(cp)
        elif cp in ai_vals:
            ai_codes.add(cp)

    if args.print_icons:
        print("Font Awesome (solid):")
        for n in sorted({n for n in fa_names if n in classic_map and n not in brand_map}):
            print(f"  - fa-{n}")
        print("Font Awesome (brands):")
        for n in sorted({n for n in fa_names if n in brand_map}):
            print(f"  - fa-{n}")
        print("Academicons:")
        for n in sorted(ai_names):
            print(f"  - ai-{n}")

    if missing_fa:
        print("[warn] Unresolved Font Awesome icon names (kept out of subset):")
        for n in sorted(missing_fa):
            print(f"  - fa-{n}")

    if missing_ai:
        print("[warn] Unresolved Academicons icon names (kept out of subset):")
        for n in sorted(missing_ai):
            print(f"  - ai-{n}")

    jobs = [
        FontJob(
            name="Font Awesome Solid",
            input_path=ROOT / "assets" / "webfonts" / "fa-solid-900.ttf",
            output_path=ROOT / "assets" / "webfonts" / "fa-solid-900.woff2",
            flavor="woff2",
            unicodes=fa_solid_codes,
        ),
        FontJob(
            name="Font Awesome Brands",
            input_path=ROOT / "assets" / "webfonts" / "fa-brands-400.ttf",
            output_path=ROOT / "assets" / "webfonts" / "fa-brands-400.woff2",
            flavor="woff2",
            unicodes=fa_brand_codes,
        ),
        FontJob(
            name="Academicons",
            input_path=ROOT / "assets" / "fonts" / "academicons.ttf",
            output_path=ROOT / "assets" / "fonts" / "academicons.woff",
            flavor="woff",
            unicodes=ai_codes,
        ),
    ]

    for job in jobs:
        subset_font(job, dry_run=args.dry_run)

    print("[ok] Done. Rebuild the site to verify icons: `bundle exec jekyll build`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
