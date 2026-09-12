"""Exact rank calculations for the four five-node, seven-edge graphs.

For H_uv = z_v, use (z_0,...,z_4) = (0,1,3,7,12).  For the two-sided
directions, let (z_0,...,z_4) range over all 120 permutations of
(0,1,2,3,4).  For each assignment:

1. At rho = 1, select independent columns, then independent rows within
   those columns, to obtain a nonsingular submatrix of the required size.
2. Keep its indices fixed and calculate its determinant polynomial p(rho).
3. Factor p exactly over Q and list all its nonzero real roots.
4. At each root, select another nonsingular submatrix of the same full
   matrix family and verify its determinant by exact algebraic arithmetic.

The first minor covers rho such that p(rho) != 0; step 4 covers every remaining nonzero
real root of p(rho).  The four graphs, 120 assignments of z, and kappa in {1,2}
give 960 cases.  Each case keeps z fixed and uses exact arithmetic.

Column A contains the coefficients of R_A = product_{e in A} R_e,
where R_uv = (1 + W_uv alpha_u)(1 + W_vu alpha_v), exactly as in
the manuscript's C_G(W).  The base matrix and its directional derivatives
therefore directly determine the T_G blocks used in the certificates.

This script requires Python 3.9 or later and SymPy.
Install the SymPy version used for these calculations
in your Python environment:
    python3 -m pip install sympy==1.14.0

Run from the folder containing this script:
    python3 verify_pentad_minimality.py --output certificates.json

This runs all 960 cases and saves the exact calculation details to
certificates.json in that folder. Omit --output to print only a summary.
Add --workers N to use N worker processes (default: 1).
"""

from __future__ import annotations

import argparse
import itertools
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


FIVE_NODES = tuple(range(5))
ALL_FIVE_NODE_EDGES = tuple(itertools.combinations(FIVE_NODES, 2))
RHO = sp.symbols("rho")
RECEIVER_VALUES = (0, 1, 3, 7, 12)
DISTANCE_VALUES = (0, 1, 2, 3, 4)


@dataclass(frozen=True)
class GraphCase:
    degree_sequence: tuple[int, ...]
    edges: tuple[tuple[int, int], ...]
    target_rank: int
    base_rank: int
    quotient_rank: int


GRAPH_CASES = (
    GraphCase(
        (4, 3, 3, 3, 1),
        tuple(
            edge
            for edge in ALL_FIVE_NODE_EDGES
            if edge not in {(0, 1), (0, 2), (0, 3)}
        ),
        128,
        108,
        20,
    ),
    GraphCase(
        (4, 4, 2, 2, 2),
        ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (0, 4), (1, 4)),
        127,
        108,
        19,
    ),
    GraphCase(
        (4, 3, 3, 2, 2),
        tuple(
            edge
            for edge in ALL_FIVE_NODE_EDGES
            if edge not in {(0, 1), (1, 2), (2, 3)}
        ),
        128,
        112,
        16,
    ),
    GraphCase(
        (3, 3, 3, 3, 2),
        tuple(
            edge
            for edge in ALL_FIVE_NODE_EDGES
            if edge not in {(0, 1), (0, 2), (3, 4)}
        ),
        128,
        108,
        20,
    ),
)


def add_exponents(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def factor_terms(
    edge: tuple[int, int],
    z_values: tuple[int, ...],
    order: int,
    nodes: tuple[int, ...],
    *,
    receiver: bool = False,
) -> tuple[tuple[tuple[int, ...], tuple[int, int, int]], ...]:
    """Return (base, plus, minus) coefficients for R_edge and its derivative."""

    u, v = edge
    if receiver:
        # Store H_uv = z_v in the first derivative; the second is unused.
        derivative_uv = (z_values[v], 0)
        derivative_vu = (z_values[u], 0)
    else:
        distance = abs(z_values[v] - z_values[u]) ** order
        if z_values[u] < z_values[v]:
            derivative_uv = (distance, 0)
            derivative_vu = (0, distance)
        else:
            derivative_uv = (0, distance)
            derivative_vu = (distance, 0)

    exponent_u = tuple(int(node == u) for node in nodes)
    exponent_v = tuple(int(node == v) for node in nodes)
    exponent_uv = add_exponents(exponent_u, exponent_v)
    return (
        ((0,) * len(nodes), (1, 0, 0)),
        (exponent_u, (1, *derivative_uv)),
        (exponent_v, (1, *derivative_vu)),
        (
            exponent_uv,
            (
                1,
                derivative_uv[0] + derivative_vu[0],
                derivative_uv[1] + derivative_vu[1],
            ),
        ),
    )


def coefficient_matrices(
    edges: tuple[tuple[int, int], ...],
    z_values: tuple[int, ...],
    order: int,
    nodes: tuple[int, ...],
    *,
    receiver: bool = False,
) -> tuple[sp.SparseMatrix, sp.SparseMatrix, sp.SparseMatrix]:
    """Construct C_G(1) and its directional derivatives from the R_A columns.

    Column A is encoded by its binary mask in the supplied edge order.
    Occurring exponent vectors are sorted in decreasing lexicographic order.
    All omitted monomial rows are identically zero, including in derivatives.
    With receiver=True, the first derivative instead uses H_uv = z_v.
    """

    factors = tuple(
        factor_terms(edge, z_values, order, nodes, receiver=receiver)
        for edge in edges
    )
    zero = (0,) * len(nodes)
    columns: list[dict[tuple[int, ...], tuple[int, int, int]]] = []

    for absent_mask in range(1 << len(edges)):
        polynomial = {zero: (1, 0, 0)}
        for edge_index, terms in enumerate(factors):
            if not (absent_mask >> edge_index) & 1:
                continue
            product: dict[tuple[int, ...], tuple[int, int, int]] = {}
            for exponent_0, (base_0, plus_0, minus_0) in polynomial.items():
                for exponent_1, (base_1, plus_1, minus_1) in terms:
                    exponent = add_exponents(exponent_0, exponent_1)
                    old_base, old_plus, old_minus = product.get(exponent, (0, 0, 0))
                    product[exponent] = (
                        old_base + base_0 * base_1,
                        old_plus + plus_0 * base_1 + base_0 * plus_1,
                        old_minus + minus_0 * base_1 + base_0 * minus_1,
                    )
            polynomial = product
        columns.append(polynomial)

    monomials = sorted(
        set().union(*(column.keys() for column in columns)), reverse=True
    )
    row_index = {monomial: index for index, monomial in enumerate(monomials)}
    matrices = []
    for part in range(3):
        entries = {}
        for column_index, column in enumerate(columns):
            for monomial, coefficient in column.items():
                if coefficient[part]:
                    entries[(row_index[monomial], column_index)] = coefficient[part]
        matrices.append(sp.SparseMatrix(len(monomials), len(columns), entries))
    return tuple(matrices)


@dataclass
class QuotientData:
    base: sp.SparseMatrix
    pivot_columns: tuple[int, ...]
    nonpivot_columns: tuple[int, ...]
    pivot_rows: tuple[int, ...]
    nonpivot_rows: tuple[int, ...]
    right_null_basis: sp.Matrix
    projection_block: sp.Matrix


def quotient_data(base: sp.SparseMatrix) -> QuotientData:
    """Fix the transformations defining T_G using only C_G(1).

    After putting selected rows/columns first, write base = [A B; C D].
    The row transformation [A^-1 0; -C A^-1 I] and column transformation
    [I -A^-1 B; 0 I] give [I 0; 0 0].  The stored right_null_basis is the
    last block of the column transformation, in the original column order.
    """

    _, pivot_columns_raw = base.rref()
    _, pivot_rows_raw = base.T.rref()
    pivot_columns = tuple(pivot_columns_raw)
    pivot_rows = tuple(pivot_rows_raw)
    pivot_column_set = set(pivot_columns)
    pivot_row_set = set(pivot_rows)
    nonpivot_columns = tuple(
        index for index in range(base.cols) if index not in pivot_column_set
    )
    nonpivot_rows = tuple(
        index for index in range(base.rows) if index not in pivot_row_set
    )

    pivot_block_inverse = base.extract(pivot_rows, pivot_columns).inv()
    right_null_basis = sp.zeros(base.cols, len(nonpivot_columns))
    for basis_column, free_column in enumerate(nonpivot_columns):
        right_null_basis[free_column, basis_column] = 1
        pivot_values = -pivot_block_inverse * base.extract(pivot_rows, [free_column])
        for pivot_index, column_index in enumerate(pivot_columns):
            right_null_basis[column_index, basis_column] = pivot_values[pivot_index]

    projection_block = (
        base.extract(nonpivot_rows, pivot_columns) * pivot_block_inverse
    )
    assert base * right_null_basis == sp.zeros(base.rows, len(nonpivot_columns))
    return QuotientData(
        base,
        pivot_columns,
        nonpivot_columns,
        pivot_rows,
        nonpivot_rows,
        right_null_basis,
        projection_block,
    )


def induced_quotient_map(
    derivative: sp.SparseMatrix,
    data: QuotientData,
) -> sp.Matrix:
    """Represent ker(base) -> coker(base) in the chosen complements."""

    projected = derivative.extract(data.nonpivot_rows, range(derivative.cols)) - (
        data.projection_block
        * derivative.extract(data.pivot_rows, range(derivative.cols))
    )
    return projected * data.right_null_basis


def select_nonsingular_submatrix(
    matrix: DomainMatrix, size: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Select columns left to right, then rows top to bottom within them.

    The ordered independent indices from exact row reduction implement the
    greedy rule: keep a column/row only when it increases the current rank.
    Selecting rows AFTER restricting the columns guarantees nonsingularity.
    """

    assert size >= 1
    _, independent_columns = matrix.rref()
    if len(independent_columns) < size:
        raise AssertionError(f"Rank {len(independent_columns)} is below {size}")
    columns = tuple(independent_columns[:size])
    restricted = matrix.extract(range(matrix.shape[0]), columns)
    _, independent_rows = restricted.transpose().rref()
    rows = tuple(independent_rows)
    assert len(rows) == size
    return rows, columns


def matrix_at_root(
    plus_map: sp.Matrix, minus_map: sp.Matrix, root: sp.Expr
) -> DomainMatrix:
    """Evaluate exactly over Q or the real algebraic field Q(root)."""

    field = sp.QQ if root.is_Rational else sp.QQ.algebraic_field(root)
    value = field.from_sympy(root)
    entries = {}
    indices = sorted(set(plus_map.todok()) | set(minus_map.todok()))
    for i, j in indices:
        entry = field.from_sympy(plus_map[i, j]) + value * field.from_sympy(
            minus_map[i, j]
        )
        if entry:
            entries.setdefault(i, {})[j] = entry
    return DomainMatrix(entries, plus_map.shape, field)


def factor_and_find_roots(polynomial: sp.Poly) -> tuple[dict, list[sp.Expr]]:
    """Factor exactly, verify the product, and enumerate nonzero real roots.

    Compute the roots of the linear and quadratic factors using exact
    rational and quadratic algebraic arithmetic.
    """

    constant, factors = sp.factor_list(polynomial)
    reconstructed = sp.Poly(constant, RHO, domain=sp.QQ)
    roots = []
    factor_records = []
    for factor, multiplicity in factors:
        reconstructed *= factor**multiplicity
        factor_records.append(
            {"coefficients": [str(c) for c in factor.all_coeffs()],
             "multiplicity": multiplicity}
        )
        if factor.degree() == 1:
            a, b = factor.all_coeffs()
            candidates = [-b / a]
        elif factor.degree() == 2:
            a, b, c = factor.all_coeffs()
            discriminant = b**2 - 4 * a * c
            candidates = [] if discriminant < 0 else [
                sp.simplify((-b - sp.sqrt(discriminant)) / (2 * a)),
                sp.simplify((-b + sp.sqrt(discriminant)) / (2 * a)),
            ]
        else:
            raise AssertionError(f"Factor degree exceeds two: {factor.as_expr()}")
        for root in candidates:
            if root != 0 and root not in roots:
                assert root.is_real is True
                assert sp.simplify(polynomial.eval(root)) == 0
                roots.append(root)
    assert reconstructed == polynomial
    return {"constant": str(constant), "factors": factor_records}, roots


def certify_receiver(
    case: GraphCase, data: QuotientData, nodes: tuple[int, ...]
) -> int:
    """Check H_uv = z_v at the fixed values in the manuscript's labeling."""

    base, derivative, _ = coefficient_matrices(
        case.edges, RECEIVER_VALUES, 1, nodes, receiver=True
    )
    assert base == data.base
    return induced_quotient_map(derivative, data).rank()


def certify_distance_case(
    case: GraphCase,
    data: QuotientData,
    z_values: tuple[int, ...],
    leading_order: int,
    nodes: tuple[int, ...],
) -> dict:
    """One initial minor plus exact checks at all its nonzero real roots."""

    base, plus_derivative, minus_derivative = coefficient_matrices(
        case.edges, z_values, leading_order, nodes
    )
    assert base == data.base
    plus_map = induced_quotient_map(plus_derivative, data)
    minus_map = induced_quotient_map(minus_derivative, data)

    # The first minor is selected once, at rho = 1, with z held fixed.
    evaluation = matrix_at_root(plus_map, minus_map, sp.S.One)
    rows, columns = select_nonsingular_submatrix(evaluation, case.quotient_rank)
    at_one = evaluation.extract(rows, columns).det()
    assert at_one != evaluation.domain.zero
    pencil = plus_map.extract(rows, columns) + RHO * minus_map.extract(rows, columns)
    polynomial = sp.Poly(pencil.det(method="domain-ge"), RHO, domain=sp.QQ)
    assert polynomial.eval(1) == evaluation.domain.to_sympy(at_one)
    assert polynomial.degree() <= case.quotient_rank
    factorization, roots = factor_and_find_roots(polynomial)

    # With z fixed, select a nonzero minor at each root of p.
    exceptions = []
    for root in roots:
        evaluation = matrix_at_root(plus_map, minus_map, root)
        root_rows, root_columns = select_nonsingular_submatrix(
            evaluation, case.quotient_rank
        )
        determinant = evaluation.extract(root_rows, root_columns).det()
        assert determinant != evaluation.domain.zero
        exceptions.append(
            {"rho": str(root), "rows": root_rows, "columns": root_columns,
             "determinant": str(evaluation.domain.to_sympy(determinant))}
        )

    return {
        "degree_sequence": case.degree_sequence,
        "kappa": leading_order,
        "z": z_values,
        "required_rank": case.quotient_rank,
        "initial_minor": {
            "rows": rows,
            "columns": columns,
            "polynomial_coefficients": [str(c) for c in polynomial.all_coeffs()],
            "determinant_at_one": str(polynomial.eval(1)),
            "factorization": factorization,
        },
        "exceptions": exceptions,
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError("Run without -O: assertions are part of the verification")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        help="write exact polynomials, factors, roots, and selected row/column indices",
    )
    parser.add_argument(
        "--workers", type=int, default=1,
        help="parallel workers for independent z assignments (default: 1)",
    )
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    records = []
    graph_records = []

    for case in GRAPH_CASES:
        nodes = FIVE_NODES
        base, _, _ = coefficient_matrices(case.edges, DISTANCE_VALUES, 1, nodes)
        data = quotient_data(base)
        assert case.base_rank + case.quotient_rank == case.target_rank

        receiver_rank = certify_receiver(case, data, nodes)
        assert receiver_rank == case.quotient_rank
        z_assignments = tuple(itertools.permutations(DISTANCE_VALUES))
        assert len(z_assignments) == len(set(z_assignments)) == 120
        graph_records.append(
            {**asdict(case), "z_assignment_count": len(z_assignments),
             "coefficient_matrix_shape": base.shape,
             "base_independent_rows": data.pivot_rows,
             "base_independent_columns": data.pivot_columns,
             "base_remaining_rows": data.nonpivot_rows,
             "base_remaining_columns": data.nonpivot_columns,
             "rank_for_H_uv_equals_z_v": receiver_rank}
        )
        print(
            f"degree={case.degree_sequence}: "
            f"rank(T_G) for H_uv=z_v is {receiver_rank}, "
            f"z assignments={len(z_assignments)}", flush=True,
        )
        for leading_order in (1, 2):
            if args.workers == 1:
                group = [
                    certify_distance_case(case, data, z_values, leading_order, nodes)
                    for z_values in z_assignments
                ]
            else:
                with ProcessPoolExecutor(max_workers=min(args.workers, len(z_assignments))) as executor:
                    group = list(executor.map(
                        certify_distance_case,
                        itertools.repeat(case), itertools.repeat(data), z_assignments,
                        itertools.repeat(leading_order), itertools.repeat(nodes),
                    ))
            records.extend(group)
            assert len(group) == 120
            assert {tuple(record["z"]) for record in group} == set(z_assignments)
            root_count = sum(len(record["exceptions"]) for record in group)
            print(
                f"  kappa={leading_order}: {len(group)} cases passed; "
                f"{root_count} nonzero real roots checked exactly", flush=True,
            )

    root_count = sum(len(record["exceptions"]) for record in records)
    max_roots = max(len(record["exceptions"]) for record in records)
    assert len(records) == 960
    assert len({(tuple(record["degree_sequence"]), tuple(record["z"]),
                 record["kappa"]) for record in records}) == 960
    summary = {
        "five_node_cases": len(records),
        "nonzero_real_roots_checked": root_count,
        "maximum_nonzero_real_roots_per_case": max_roots,
        "all_exception_determinants_nonzero": True,
    }
    if args.output is not None:
        output = {
            "schema_version": 4,
            "sympy_version": sp.__version__,
            "indexing": {
                "coefficient_basis": "R_A = product_{(u,v) in A} R_uv",
                "z_assignment_coverage": "all 120 permutations of (0,1,2,3,4) for each graph and kappa",
                "z": "values assigned to nodes i,j,k,l,m, in that order",
                "nodes": "0,1,2,3,4 correspond to i,j,k,l,m",
                "indices": "all row and column indices are zero-based",
                "coefficient_rows": "occurring exponent tuples in decreasing lexicographic order",
                "coefficient_columns": "binary subset masks in each graph's listed edge order",
                "T_rows": "base_remaining_rows in the recorded order",
                "T_columns": "base_remaining_columns in the recorded order",
                "polynomial_coefficients": "highest degree first; all numbers are exact strings",
            },
            "distance_values": DISTANCE_VALUES,
            "values_for_H_uv_equals_z_v": RECEIVER_VALUES,
            "summary": summary,
            "graphs": graph_records,
            "cases": records,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, indent=2) + "\n")
        print(f"Exact calculation details written to {args.output}")
    print(
        f"All {len(records)} cases passed; {root_count} exceptional-root determinants "
        f"are nonzero; at most {max_roots} roots per case."
    )


if __name__ == "__main__":
    main()
