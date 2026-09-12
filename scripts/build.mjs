import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = dirname(dirname(fileURLToPath(import.meta.url)));
const sourceDir = join(siteDir, "src");
const checkOnly = process.argv.includes("--check");

const pages = [
  {
    key: "about",
    source: "index.html",
    output: "index.html",
    title: "Wu, Zeqi (吴泽齐)",
    description: "Academic homepage of Zeqi Wu, a visiting Ph.D. student at CUHK-Shenzhen and a Ph.D. candidate at Renmin University of China.",
  },
  {
    key: "research",
    source: "research.html",
    output: "research/index.html",
    math: true,
    title: "Research | Wu, Zeqi (吴泽齐)",
    description: "Publications and working papers by Zeqi Wu in econometrics, causal inference, policy learning, and network data.",
  },
  {
    key: "talks",
    source: "talks.html",
    output: "talks/index.html",
    title: "Talks | Wu, Zeqi (吴泽齐)",
    description: "Conference presentations, seminars, and invited talks by Zeqi Wu.",
  },
  {
    key: "cv",
    source: "cv.html",
    output: "cv/index.html",
    title: "CV | Wu, Zeqi (吴泽齐)",
    description: "Academic CV of Zeqi Wu.",
  },
];

const navItems = [
  ["about", "/", "About"],
  ["research", "/research/", "Research"],
  ["talks", "/talks/", "Talks"],
  ["cv", "/cv/", "CV"],
];

const mathHead = [
  '    <link rel="stylesheet" href="/assets/vendor/katex/katex.min.css">',
  '    <script defer src="/assets/vendor/katex/katex.min.js"></script>',
  '    <script defer src="/assets/vendor/katex/contrib/auto-render.min.js"></script>',
  '    <script defer src="/assets/js/math.js?v=1"></script>',
].join("\n");

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function render(template, values, label) {
  const rendered = template.replace(/{{([a-z]+)}}/g, function (match, key) {
    if (!(key in values)) throw new Error(`Missing value "${key}" while rendering ${label}`);
    return values[key];
  });
  const leftover = rendered.match(/{{[^}]+}}/);
  if (leftover) throw new Error(`Unresolved placeholder ${leftover[0]} in ${label}`);
  return rendered;
}

function renderNavigation(activeKey) {
  return navItems
    .map(function ([key, href, label]) {
      const current = key === activeKey ? ' aria-current="page"' : "";
      return `              <li><a class="nav-link" href="${href}"${current}>${label}</a></li>`;
    })
    .join("\n");
}

const [layout, head, header, footer] = await Promise.all([
  readFile(join(sourceDir, "partials", "layout.html"), "utf8"),
  readFile(join(sourceDir, "partials", "head.html"), "utf8"),
  readFile(join(sourceDir, "partials", "header.html"), "utf8"),
  readFile(join(sourceDir, "partials", "footer.html"), "utf8"),
]);

const stale = [];

for (const page of pages) {
  const main = (await readFile(join(sourceDir, "pages", page.source), "utf8")).trimEnd();
  const renderedHead = render(
    head,
    {
      title: escapeHtml(page.title),
      description: escapeHtml(page.description),
      extrahead: page.math ? mathHead : "",
    },
    `head for ${page.output}`,
  ).trimEnd();
  const renderedHeader = render(
    header,
    { navigation: renderNavigation(page.key) },
    `header for ${page.output}`,
  ).trimEnd();
  const output = render(
    layout,
    { head: renderedHead, header: renderedHeader, main, footer: footer.trimEnd() },
    page.output,
  ).trimEnd() + "\n";
  const outputPath = join(siteDir, page.output);

  if (checkOnly) {
    let existing = "";
    try {
      existing = await readFile(outputPath, "utf8");
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    if (existing !== output) stale.push(page.output);
  } else {
    await mkdir(dirname(outputPath), { recursive: true });
    await writeFile(outputPath, output, "utf8");
  }
}

if (stale.length) {
  console.error(`Generated HTML is stale: ${stale.join(", ")}`);
  process.exitCode = 1;
} else if (checkOnly) {
  console.log("Generated HTML is current.");
} else {
  console.log(`Generated ${pages.length} static pages.`);
}
