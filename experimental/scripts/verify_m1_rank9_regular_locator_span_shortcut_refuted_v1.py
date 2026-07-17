#!/usr/bin/env python3
"""Verify the rank-nine regular-locator generic route cut.

The exact control is an RS[24,13,12] instance over
GF(2^23)=GF(2)[u]/(u^23+u^5+1) with an explicitly declared retained
55-slope family.  Its unique noncontained selector on that family has affine
witness rank nine, raw witness rank ten, carrier excess eleven, and
locator-vector rank eleven.  A symbolic extension of the same five pencils
gives locator rank j+1 for every j>=10 while keeping the three ranks
(s,t,nu)=(9,10,11) fixed.

This is a fail-closed route cut for a *generic local* rank-to-locator-span
shortcut.  It does not instantiate the KoalaBear domain, execute the actual
periodic/quotient/Johnson/B11 masks, move the ledger, or close branch 3.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-rank9-regular-locator-span-shortcut-refuted-v1"
ARTIFACT_KIND = "M1_RANK9_GENERIC_LOCAL_LOCATOR_SPAN_ROUTE_CUT"
STATUS = "PROVED_GENERIC_LOCAL_RANK_TO_LOCATOR_SPAN_SHORTCUT_FALSE"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-rank9-regular-locator-span-shortcut-refuted-v1"
)
CERT_PATH = CERT_DIR / "m1_rank9_regular_locator_span_shortcut_refuted_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-rank9-regular-locator-span-shortcut-refuted-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.sage"
)
SPARSE_BOUNDARY_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"
)
SPARSE_BOUNDARY_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-sparse-chart-boundary-v1/"
    "m1_kb_branch3_rank9_sparse_chart_boundary_v1.json"
)
SPARSE_BOUNDARY_PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py"
)
SPARSE_BOUNDARY_SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.sage"
)
ACTUAL_CORE_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_actual_core_mds_rank_ladder_v1.md"
)
ACTUAL_CORE_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-actual-core-mds-v1/"
    "m1_kb_branch3_actual_core_mds_v1.json"
)
ACTUAL_CORE_PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py"
)
LOW_EXCESS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_low_excess_carrier_cut_v1.md"
)
LOW_EXCESS_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-low-excess-carrier-cut-v1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.json"
)
LOW_EXCESS_PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py"
)
FIXED_EXCESS_REL = Path(
    "experimental/notes/thresholds/"
    "cap25_v12_fixed_residual_excess_audit.md"
)
SPARSE_HANKEL_REL = Path(
    "experimental/notes/thresholds/"
    "cap25_v12_sparse_sigma_first_layer_audit.md"
)

Q = 1 << 23
DEGREE = 23
MODULUS = (1 << 23) | (1 << 5) | 1
MASK = Q - 1
GENERATOR = 2
GENERATOR_ORDER = Q - 1
GENERATOR_ORDER_FACTORS = (47, 178_481)

J = 10
N = 24
K = 13
R = N - K
A = N - J
SPARSE_SUPPORT_SIZE = 2

CORES = (
    (3, 5, 6, 7, 9, 11, 13, 16, 17, 20, 21),
    (0, 2, 3, 6, 7, 8, 9, 10, 12, 13, 19),
    (1, 2, 4, 6, 7, 8, 10, 15, 17, 20, 21),
    (2, 3, 5, 9, 11, 12, 13, 14, 19, 20, 21),
    (0, 1, 2, 5, 6, 12, 14, 15, 18, 20, 21),
)

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "exact_control",
    "parametric_route_cut",
    "scope_guards",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not assert that declared Gamma exhausts the full bad-slope set.",
    "This packet does not instantiate the deployed KoalaBear evaluation domain or row.",
    "This packet does not execute periodic, quotient, Johnson, or B11 first-match masks.",
    "This packet does not prove that the declared slopes survive the deployed first-match order.",
    "This packet does not move U_paid or B_remaining.",
    "This packet does not close rank nine, branch 3, or the KoalaBear row.",
    "This packet does not attack intrinsic rank at least ten.",
    "This packet does not authorize Lean or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """An arithmetic, source, schema, or semantic gate failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def gf_add(left: int, right: int) -> int:
    return left ^ right


def gf_mul(left: int, right: int) -> int:
    require(0 <= left < Q and 0 <= right < Q, "field operand out of range")
    result = 0
    a = left
    b = right
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & Q:
            a ^= MODULUS
    return result & MASK


def gf_pow(base: int, exponent: int) -> int:
    require(exponent >= 0, "negative field exponent")
    result = 1
    value = base
    power = exponent
    while power:
        if power & 1:
            result = gf_mul(result, value)
        value = gf_mul(value, value)
        power >>= 1
    return result


def gf_inv(value: int) -> int:
    require(value != 0, "division by zero")
    inverse = gf_pow(value, Q - 2)
    require(gf_mul(value, inverse) == 1, "field inverse check failed")
    return inverse


def gf_div(numerator: int, denominator: int) -> int:
    return gf_mul(numerator, gf_inv(denominator))


def poly_trim(polynomial: Sequence[int]) -> tuple[int, ...]:
    values = list(polynomial)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] ^= gf_mul(a, b)
    return poly_trim(result)


def poly_scale(polynomial: Sequence[int], scalar: int) -> tuple[int, ...]:
    return poly_trim([gf_mul(value, scalar) for value in polynomial])


def poly_eval(polynomial: Sequence[int], point: int) -> int:
    result = 0
    for coefficient in reversed(polynomial):
        result = gf_mul(result, point) ^ coefficient
    return result


def root_polynomial(points: Iterable[int]) -> tuple[int, ...]:
    polynomial: tuple[int, ...] = (1,)
    for point in points:
        # Characteristic two: X-point = X+point.
        polynomial = poly_mul(polynomial, (point, 1))
    return polynomial


def pad_row(row: Sequence[int], width: int) -> list[int]:
    require(len(row) <= width, "row exceeds declared width")
    return list(row) + [0] * (width - len(row))


def rref_rank_pivots(rows: Sequence[Sequence[int]]) -> tuple[int, list[int]]:
    if not rows:
        return 0, []
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    matrix = [list(row) for row in rows]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(width):
        chosen = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if chosen is None:
            continue
        matrix[pivot_row], matrix[chosen] = matrix[chosen], matrix[pivot_row]
        inverse = gf_inv(matrix[pivot_row][column])
        matrix[pivot_row] = [gf_mul(value, inverse) for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value ^ gf_mul(factor, pivot)
                for value, pivot in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row, pivots


def matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    return rref_rank_pivots(rows)[0]


def determinant(rows: Sequence[Sequence[int]]) -> int:
    size = len(rows)
    require(size > 0 and all(len(row) == size for row in rows), "determinant needs square matrix")
    matrix = [list(row) for row in rows]
    result = 1
    for column in range(size):
        chosen = next(
            (row for row in range(column, size) if matrix[row][column]),
            None,
        )
        require(chosen is not None, "singular determinant witness")
        matrix[column], matrix[chosen] = matrix[chosen], matrix[column]
        pivot = matrix[column][column]
        result = gf_mul(result, pivot)
        inverse = gf_inv(pivot)
        for row in range(column + 1, size):
            if matrix[row][column] == 0:
                continue
            factor = gf_mul(matrix[row][column], inverse)
            for entry in range(column, size):
                matrix[row][entry] ^= gf_mul(factor, matrix[column][entry])
    return result


def matrix_vector(rows: Sequence[Sequence[int]], vector: Sequence[int]) -> list[int]:
    require(all(len(row) == len(vector) for row in rows), "matrix-vector dimension mismatch")
    return [
        functools.reduce(
            gf_add,
            (gf_mul(left, right) for left, right in zip(row, vector, strict=True)),
            0,
        )
        for row in rows
    ]


def matrix_columns(rows: Sequence[Sequence[int]], columns: Sequence[int]) -> list[list[int]]:
    return [[row[column] for column in columns] for row in rows]


def nonzero_minor(rows: Sequence[Sequence[int]]) -> dict[str, Any]:
    rank, pivots = rref_rank_pivots(rows)
    require(rank == len(rows), "declared rows are not independent")
    square = [[row[column] for column in pivots] for row in rows]
    value = determinant(square)
    require(value != 0, "selected rank minor vanished")
    return {"columns": pivots, "determinant": value}


def sha256_int_rows(rows: Sequence[Sequence[int]]) -> str:
    return canonical_hash([list(row) for row in rows])


def field_polynomial(value: int) -> str:
    if value == 0:
        return "0"
    terms: list[str] = []
    for exponent in range(DEGREE - 1, -1, -1):
        if not (value >> exponent) & 1:
            continue
        if exponent == 0:
            terms.append("1")
        elif exponent == 1:
            terms.append("u")
        else:
            terms.append(f"u^{exponent}")
    return " + ".join(terms)


@functools.lru_cache(maxsize=1)
def _exact_control_json() -> str:
    require((N, K, R, J, A) == (24, 13, 11, 10, 14), "RS row drift")
    require(MODULUS == (1 << 23) | (1 << 5) | 1, "field modulus drift")
    require(
        functools.reduce(lambda x, y: x * y, GENERATOR_ORDER_FACTORS, 1)
        == GENERATOR_ORDER,
        "generator-order factorization drift",
    )
    require(
        all(gf_pow(GENERATOR, GENERATOR_ORDER // prime) != 1 for prime in GENERATOR_ORDER_FACTORS),
        "u is not primitive",
    )

    exponents = tuple(1 << index for index in range(22))
    ratios = tuple(gf_pow(GENERATOR, exponent) for exponent in exponents)
    B = tuple(gf_inv(1 ^ ratio) for ratio in ratios)
    domain = (0, 1) + B
    require(len(set(domain)) == N, "evaluation domain collision")
    require(all(point not in (0, 1) for point in B), "moving point hit sparse support")
    require(
        all(gf_div(1 ^ B[index], B[index]) == ratios[index] for index in range(22)),
        "point-to-ratio formula drift",
    )
    max_sum = sum(exponents)
    require(max_sum == (1 << 22) - 1 < GENERATOR_ORDER, "subset exponent envelope drift")
    twelve_sums = {
        sum(exponents[index] for index in subset)
        for subset in itertools.combinations(range(22), 12)
    }
    require(len(twelve_sums) == 646_646, "12-subset products lost injectivity")

    lambdas: list[int] = []
    for point in domain:
        denominator = 1
        for other in domain:
            if other != point:
                denominator = gf_mul(denominator, point ^ other)
        lambdas.append(gf_inv(denominator))
    parity = [
        [gf_mul(lambdas[column], gf_pow(domain[column], row)) for column in range(N)]
        for row in range(R)
    ]
    require(matrix_rank(parity) == R, "parity check lost rank")

    require(all(len(core) == len(set(core)) == 11 for core in CORES), "core size drift")
    require(not set.intersection(*(set(core) for core in CORES)), "core intersection is nonempty")
    require(
        min(len(set(left) ^ set(right)) for left, right in itertools.combinations(CORES, 2)) >= 8,
        "core symmetric-difference guard drift",
    )

    root_sets: list[tuple[int, ...]] = []
    offsets: list[int] = []
    for core in CORES:
        offsets.append(len(root_sets))
        for moving in range(22):
            if moving not in core:
                root_sets.append(tuple(sorted(core + (moving,))))
    require(len(root_sets) == len(set(root_sets)) == 55, "five pencils are not 55 distinct root sets")

    code_polynomials: list[tuple[int, ...]] = []
    slopes: list[int] = []
    errors: list[list[int]] = []
    supports: list[tuple[int, ...]] = []
    locators: list[tuple[int, ...]] = []
    all_transverse = True
    all_residual = True

    y0 = [row[0] for row in parity]
    y1 = [row[1] for row in parity]
    require(matrix_rank([y0, y1]) == 2, "syndrome line is degenerate")

    for root_set in root_sets:
        root_poly = root_polynomial(B[index] for index in root_set)
        require(len(root_poly) == 13, "root polynomial degree drift")
        code_poly = poly_scale(root_poly, gf_inv(poly_eval(root_poly, 0)))
        gamma = poly_eval(code_poly, 1)
        expected_gamma = 1
        for index in root_set:
            expected_gamma = gf_mul(expected_gamma, ratios[index])
        require(gamma == expected_gamma != 0, "slope formula or nontangency failed")
        codeword = [poly_eval(code_poly, point) for point in domain]
        require(matrix_vector(parity, codeword) == [0] * R, "degree-12 word left RS code")
        sparse_word = [1, gamma] + [0] * 22
        error = [left ^ right for left, right in zip(sparse_word, codeword, strict=True)]
        support = tuple(index for index in range(22) if index not in set(root_set))
        actual_B_support = tuple(index for index, value in enumerate(error[2:]) if value)
        require(error[0] == error[1] == 0, "error did not vanish on sparse support")
        require(actual_B_support == support and len(support) == J, "full-weight support drift")
        require(sum(value != 0 for value in error) == J, "error weight drift")
        locator = root_polynomial(B[index] for index in support)
        require(len(locator) == J + 1 and locator[-1] == 1, "locator degree/monicity drift")
        require(all(poly_eval(locator, B[index]) == 0 for index in support), "locator split failed")
        syndrome_error = matrix_vector(parity, error)
        require(
            syndrome_error == [left ^ gf_mul(gamma, right) for left, right in zip(y0, y1, strict=True)],
            "error left syndrome line",
        )
        M_ell = gf_mul(lambdas[0], poly_eval(locator, 0)) ^ gf_mul(
            gf_mul(lambdas[1], gamma), poly_eval(locator, 1)
        )
        H2_ell = gf_mul(lambdas[1], poly_eval(locator, 1))
        chosen_minor = gf_mul(lambdas[1], gamma)
        require(M_ell == 0, "M(gamma) ell failed")
        require(H2_ell != 0, "H2 ell noncontainment failed")
        require(chosen_minor != 0, "fixed column-1 chart is singular")
        support_columns = [2 + index for index in support]
        support_image = matrix_columns(parity, support_columns)
        augmented = matrix_columns(parity, support_columns + [1])
        require(matrix_rank(support_image) == J, "support image lost MDS rank")
        require(matrix_rank(augmented) == J + 1, "y1 entered support image")

        code_polynomials.append(code_poly)
        slopes.append(gamma)
        errors.append(error)
        supports.append(support)
        locators.append(locator)

    require(len(set(slopes)) == 55, "selected slopes are not distinct")
    require(len(set(supports)) == 55, "selected supports are not distinct")

    raw_rank = matrix_rank(errors)
    affine_rows = [
        [left ^ right for left, right in zip(error, errors[0], strict=True)]
        for error in errors[1:]
    ]
    affine_rank = matrix_rank(affine_rows)
    locator_rows = [pad_row(locator, J + 1) for locator in locators]
    locator_rank = matrix_rank(locator_rows)
    require((affine_rank, raw_rank, locator_rank) == (9, 10, 11), "rank triple drift")

    basis_indices = [index for offset in offsets for index in (offset, offset + 1)]
    basis_errors = [errors[index] for index in basis_indices]
    basis_polynomials = [pad_row(code_polynomials[index], K) for index in basis_indices]
    require(matrix_rank(basis_errors) == matrix_rank(basis_polynomials) == 10, "ten-witness basis drift")
    polynomial_minor = nonzero_minor(basis_polynomials)
    require(
        field_polynomial(polynomial_minor["determinant"])
        == "u^22 + u^16 + u^15 + u^14 + u^12 + u^11 + u^10 + u^7 + u^6 + u^5 + u^2 + 1",
        "frozen polynomial-space determinant drift",
    )
    basis_affine = [
        [left ^ right for left, right in zip(row, basis_polynomials[0], strict=True)]
        for row in basis_polynomials[1:]
    ]
    require(matrix_rank(basis_affine) == 9, "basis affine rank drift")
    affine_minor = nonzero_minor(basis_affine)
    one_pencil_locators = locator_rows[: J + 1]
    require(matrix_rank(one_pencil_locators) == J + 1, "one-pencil Lagrange basis drift")
    locator_minor = nonzero_minor(one_pencil_locators)

    carrier = set().union(*(set(support) for support in supports))
    basis_carrier = set().union(*(set(supports[index]) for index in basis_indices))
    require(carrier == basis_carrier == set(range(22)), "carrier recovery drift")
    N_V = len(carrier)
    nu = N_V - R
    require((N_V, nu) == (22, 11), "carrier excess drift")
    carrier_parity = matrix_columns(parity, [2 + index for index in sorted(carrier)])
    require(matrix_rank(carrier_parity) == R, "carrier parity rank drift")
    require(len(carrier_parity[0]) - matrix_rank(carrier_parity) == 11, "carrier kernel drift")

    agreement_pairs = [
        [roots_B, agreements_E]
        for roots_B in range(13)
        for agreements_E in range(3)
        if roots_B + agreements_E >= A
    ]
    require(agreement_pairs == [[12, 2]], "unique-witness agreement arithmetic drift")

    control = {
        "field": {
            "characteristic": 2,
            "extension_degree": DEGREE,
            "cardinality": Q,
            "modulus": "u^23 + u^5 + 1",
            "generator_integer_encoding": GENERATOR,
            "generator_order": GENERATOR_ORDER,
            "generator_order_prime_factors": list(GENERATOR_ORDER_FACTORS),
        },
        "row": {
            "n": N,
            "k": K,
            "redundancy_R": R,
            "radius_j": J,
            "agreement_A": A,
            "R_minus_j": R - J,
            "sparse_support_size": SPARSE_SUPPORT_SIZE,
        },
        "domain": {
            "a": 0,
            "b": 1,
            "B_integer_encoding": list(B),
            "B_sha256": canonical_hash(list(B)),
            "formula": "z_i=(1-u^(2^i))^(-1), 0<=i<22",
            "all_distinct": True,
        },
        "five_pencils": {
            "cores": [list(core) for core in CORES],
            "minimum_pairwise_symmetric_difference": min(
                len(set(left) ^ set(right)) for left, right in itertools.combinations(CORES, 2)
            ),
            "common_core_intersection_empty": True,
            "root_set_count": len(root_sets),
            "root_sets_sha256": canonical_hash([list(root_set) for root_set in root_sets]),
            "slope_count": len(slopes),
            "distinct_slopes": len(set(slopes)),
            "slopes_integer_encoding_sha256": canonical_hash(slopes),
        },
        "selector": {
            "complete_on_declared_Gamma": True,
            "declared_Gamma_exhausts_full_bad_set": False,
            "declared_Gamma_is_proper_subfamily": True,
            "ambient_noncontained_bad_slope_count": len(twelve_sums),
            "unique_noncontained_witness_per_slope": True,
            "rank_minimizing_because_unique": True,
            "all_full_weight": True,
            "all_transverse": all_transverse,
            "all_non_tangent": True,
            "all_regular_on_fixed_column_1_chart": True,
            "chosen_minor_formula": "Delta(gamma)=lambda_b*gamma",
            "all_M_ell_zero": all_residual,
            "all_H2_ell_nonzero": True,
            "all_squarefree_D_split_locators": True,
            "affine_difference_rank_s_star": affine_rank,
            "raw_witness_rank_t": raw_rank,
            "locator_vector_rank": locator_rank,
            "errors_sha256": sha256_int_rows(errors),
            "locators_sha256": sha256_int_rows(locator_rows),
        },
        "rank_witnesses": {
            "ten_basis_indices": basis_indices,
            "ten_basis_supports_recover_carrier": True,
            "code_polynomial_minor": polynomial_minor,
            "code_polynomial_minor_as_field_polynomial": field_polynomial(
                polynomial_minor["determinant"]
            ),
            "affine_difference_minor": affine_minor,
            "one_pencil_locator_minor": locator_minor,
        },
        "carrier": {
            "N_V": N_V,
            "R": R,
            "nu": nu,
            "kappa_star": nu,
            "kappa_star_exact_because_selector_unique": True,
            "carrier_is_B": True,
            "restricted_kernel_dimension": N_V - R,
            "restricted_MDS_distance": R + 1,
        },
        "injectivity_and_uniqueness": {
            "all_12_subset_count": len(twelve_sums),
            "all_12_subset_products_distinct": True,
            "maximum_binary_subset_exponent": max_sum,
            "maximum_below_generator_order": True,
            "nonzero_witness_agreement_pairs": agreement_pairs,
            "zero_codeword_error_weight": 2,
            "zero_codeword_witness_contained_and_H2_rejected": True,
        },
    }
    return json.dumps(control, sort_keys=True, allow_nan=False)


def exact_control() -> dict[str, Any]:
    return json.loads(_exact_control_json())


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing bound source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        binding("packet-note", NOTE_REL, "parametric route-cut statement and proof"),
        binding("packet-readme", README_REL, "replay and scope contract"),
        binding("packet-python", PYTHON_REL, "independent exact GF(2^23) verifier"),
        binding("packet-sage", SAGE_REL, "independent Sage finite-field replay"),
        binding("sparse-boundary-note", SPARSE_BOUNDARY_NOTE_REL, "regular residual (6.1) producer"),
        binding("sparse-boundary-certificate", SPARSE_BOUNDARY_CERT_REL, "frozen regular-route predecessor"),
        binding("sparse-boundary-verifier", SPARSE_BOUNDARY_PYTHON_REL, "predecessor fail-closed replay"),
        binding("sparse-boundary-sage", SPARSE_BOUNDARY_SAGE_REL, "predecessor Sage control"),
        binding("actual-core-note", ACTUAL_CORE_NOTE_REL, "s_star and kappa_star selector contract"),
        binding("actual-core-certificate", ACTUAL_CORE_CERT_REL, "frozen rank-nine carrier state"),
        binding("actual-core-verifier", ACTUAL_CORE_PYTHON_REL, "actual-core exact replay"),
        binding("low-excess-note", LOW_EXCESS_NOTE_REL, "kappa_star<=10 owner boundary"),
        binding("low-excess-certificate", LOW_EXCESS_CERT_REL, "frozen low-excess owner"),
        binding("low-excess-verifier", LOW_EXCESS_PYTHON_REL, "low-excess exact replay"),
        binding("fixed-excess-proof", FIXED_EXCESS_REL, "generic Padé-Hankel chart argument"),
        binding("closed-ball-proof", SPARSE_HANKEL_REL, "exact split-locator equivalence"),
    ]


def contains_all(text: str, anchors: Sequence[str], label: str) -> None:
    for anchor in anchors:
        require(anchor in text, f"{label} semantic anchor missing: {anchor}")


def validate_source_contracts() -> None:
    note = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    contains_all(
        note,
        [
            "For every integer \\(j\\ge10\\)",
            "s_*=9",
            "\\kappa_*=11",
            "\\operatorname{rank}\\{\\ell_O\\}=j+1",
            "GENERIC_LOCAL_RANK_TO_LOCATOR_SPAN_SHORTCUT_REFUTED",
            "explicitly declared retained slope family",
            "full bad-slope set",
            "no ledger movement",
            "RED",
            "YELLOW",
        ],
        "packet note",
    )
    predecessor = (ROOT / SPARSE_BOUNDARY_NOTE_REL).read_text(encoding="utf-8")
    contains_all(
        predecessor,
        [
            "REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE",
            "Delta(\\gamma)\\ne0",
            "H_2\\ell_T\\ne0",
            "affine witness rank nine / witness-column rank ten",
        ],
        "sparse-boundary predecessor",
    )
    actual_core = (ROOT / ACTUAL_CORE_NOTE_REL).read_text(encoding="utf-8")
    contains_all(
        actual_core,
        ["s_*(\\Gamma)", "\\kappa_*(\\Gamma)\\ge11", "TEN_ACTUAL_SUPPORTS_RECOVER"],
        "actual-core predecessor",
    )
    low_excess = (ROOT / LOW_EXCESS_NOTE_REL).read_text(encoding="utf-8")
    contains_all(
        low_excess,
        ["kappa_*(Z) <= 10", "kappa_*(Z) >= 11", "CERTIFIED_LOW_EXCESS_COMMON_CARRIER"],
        "low-excess predecessor",
    )


def expected_parametric_route_cut() -> dict[str, Any]:
    return {
        "quantifier": "FOR_EVERY_INTEGER_j_AT_LEAST_10_THERE_EXISTS_A_FINITE_EXTENSION_RS_INSTANCE_AND_DECLARED_RETAINED_Gamma",
        "Gamma_scope": {
            "explicitly_declared_retained_family": True,
            "full_bad_slope_set_exhaustion_assumed": False,
            "deployed_first_match_survival_assumed": False,
        },
        "row_family": {
            "n": "j+14",
            "k": 13,
            "R": "j+1",
            "radius": "j",
            "agreement": 14,
            "sparse_support_size": 2,
            "declared_Gamma_size": "5*(j+1)",
        },
        "fixed_invariants": {
            "affine_rank_s_star": 9,
            "raw_rank_t": 10,
            "carrier_excess_nu": 11,
            "kappa_star": 11,
            "ten_basis_supports_recover_carrier": True,
            "selector_unique_and_rank_minimizing": True,
        },
        "growing_invariant": {
            "locator_vector_rank": "j+1",
            "one_pencil_is_a_Lagrange_basis_of": "F[X]_{<=j}",
            "unbounded_with_j": True,
        },
        "finite_field_existence": {
            "base_field": "GF(2^23)",
            "old_22_ratios_have_all_subset_products_distinct": True,
            "new_ratios": "chosen over algebraic closure outside finitely many nonzero Laurent hypersurfaces",
            "finite_extension_exists": True,
            "reason": "a finite product of nonzero Laurent polynomials is nonzero; a finite chosen tuple is contained in one finite extension",
        },
        "witness_proof": {
            "five_pencil_polynomial_span_dimension": 10,
            "normalization_q_at_a": 1,
            "affine_difference_kernel_dimension": 9,
            "nonzero_radius_witness_agreement_pair": [12, 2],
            "subset_product_slope_map_injective": True,
            "zero_codeword_witness_rejected_by_H2": True,
            "all_regular_residual_6_1_gates": True,
        },
        "cover_obstruction": {
            "single_vector_span_bound_depending_only_on_s_t_nu": False,
            "B_vector_subspaces_dimension_C_requires": "B*C>=j+1",
            "B_projective_subspaces_dimension_c_requires": "B*(c+1)>=j+1",
            "fixed_B_C_cover_possible_for_all_j": False,
        },
        "terminal": "GENERIC_LOCAL_RANK_TO_LOCATOR_SPAN_SHORTCUT_REFUTED",
    }


def expected_scope_guards() -> dict[str, Any]:
    return {
        "generic_local_implication_refuted": True,
        "declared_Gamma_exhausts_full_bad_set": False,
        "full_bad_family_or_deployed_first_match_strengthened_statement_refuted": False,
        "koalabear_domain_instantiated": False,
        "project_owner_masks_checked": False,
        "actual_first_match_survival_proved": False,
        "koalabear_rank9_residual_refuted": False,
        "branch3_closed": False,
        "ledger_movement": 0,
        "next_required_structure": "DEPLOYED_DOMAIN_OR_EXECUTABLE_OWNER_MASK_HYPOTHESIS",
    }


def expected_audit_sections() -> dict[str, str]:
    return {
        "statement": "generic local rank/carrier/regularity hypotheses without Gamma exhaustion imply bounded locator span or bounded cover",
        "dependencies": "PROVED exact base control plus symbolic scalar-extension and finite-hypersurface-avoidance argument",
        "parameter_dependence": "s=9, t=10, nu=11 fixed; locator rank=j+1 unbounded",
        "layer_cake_dyadic_summability": "NOT_APPLICABLE",
        "moment_markov_chebyshev": "NOT_APPLICABLE",
        "numerical_evidence": "EXACT_FINITE_FIELD_CONTROL_NOT_DEPLOYED_DOMAIN_CENSUS",
        "generic_local_verdict": "RED_FALSE_AS_STATED",
        "koalabear_owner_strengthened_verdict": "YELLOW_OPEN",
    }


def expected_certificate() -> dict[str, Any]:
    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "exact_control": exact_control(),
        "parametric_route_cut": expected_parametric_route_cut(),
        "scope_guards": expected_scope_guards(),
        "audit_sections": expected_audit_sections(),
        "nonclaims": NONCLAIMS,
    }
    certificate["payload_sha256"] = payload_hash(certificate)
    return certificate


def validate_certificate(certificate: dict[str, Any]) -> None:
    validate_source_contracts()
    require(set(certificate) == TOP_KEYS, "certificate top-level key drift")
    require(certificate.get("payload_sha256") == payload_hash(certificate), "payload hash mismatch")
    expected = expected_certificate()
    require(certificate == expected, "certificate differs from exact recomputation")

    control = certificate["exact_control"]
    selector = control["selector"]
    carrier = control["carrier"]
    require(
        (
            selector["affine_difference_rank_s_star"],
            selector["raw_witness_rank_t"],
            carrier["nu"],
            selector["locator_vector_rank"],
        )
        == (9, 10, 11, 11),
        "base rank/carrier tuple drift",
    )
    require(selector["rank_minimizing_because_unique"] is True, "rank minimizer unproved")
    require(
        selector["declared_Gamma_exhausts_full_bad_set"] is False
        and selector["declared_Gamma_is_proper_subfamily"] is True
        and selector["ambient_noncontained_bad_slope_count"] == 646_646,
        "declared-Gamma scope drift",
    )
    require(carrier["kappa_star_exact_because_selector_unique"] is True, "kappa_star unproved")
    route = certificate["parametric_route_cut"]
    require(route["growing_invariant"]["unbounded_with_j"] is True, "unbounded route cut disabled")
    scope = certificate["scope_guards"]
    require(scope["generic_local_implication_refuted"] is True, "route cut disabled")
    require(scope["declared_Gamma_exhausts_full_bad_set"] is False, "Gamma exhaustion overclaim")
    require(
        scope["full_bad_family_or_deployed_first_match_strengthened_statement_refuted"] is False,
        "full-family strengthened statement overclaim",
    )
    require(scope["koalabear_rank9_residual_refuted"] is False, "KoalaBear residual overclaim")
    require(scope["ledger_movement"] == 0, "ledger moved")


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def mutation_cases() -> list[tuple[str, tuple[Any, ...], Any]]:
    return [
        ("schema", ("schema",), SCHEMA + "-tampered"),
        ("status", ("status",), "GREEN_ROW_CLOSED"),
        ("field-degree", ("exact_control", "field", "extension_degree"), 22),
        ("field-modulus", ("exact_control", "field", "modulus"), "u^23+u+1"),
        ("n", ("exact_control", "row", "n"), 25),
        ("k", ("exact_control", "row", "k"), 12),
        ("j", ("exact_control", "row", "radius_j"), 9),
        ("A", ("exact_control", "row", "agreement_A"), 13),
        ("domain-hash", ("exact_control", "domain", "B_sha256"), "0" * 64),
        ("core-count", ("exact_control", "five_pencils", "root_set_count"), 54),
        ("slope-count", ("exact_control", "five_pencils", "slope_count"), 54),
        ("distinct-slopes", ("exact_control", "five_pencils", "distinct_slopes"), 54),
        ("complete", ("exact_control", "selector", "complete_on_declared_Gamma"), False),
        ("Gamma-exhaustion", ("exact_control", "selector", "declared_Gamma_exhausts_full_bad_set"), True),
        ("Gamma-proper", ("exact_control", "selector", "declared_Gamma_is_proper_subfamily"), False),
        ("ambient-bad-count", ("exact_control", "selector", "ambient_noncontained_bad_slope_count"), 55),
        ("unique", ("exact_control", "selector", "unique_noncontained_witness_per_slope"), False),
        ("minimizer", ("exact_control", "selector", "rank_minimizing_because_unique"), False),
        ("full-weight", ("exact_control", "selector", "all_full_weight"), False),
        ("transverse", ("exact_control", "selector", "all_transverse"), False),
        ("regular", ("exact_control", "selector", "all_regular_on_fixed_column_1_chart"), False),
        ("Mell", ("exact_control", "selector", "all_M_ell_zero"), False),
        ("H2ell", ("exact_control", "selector", "all_H2_ell_nonzero"), False),
        ("affine-rank", ("exact_control", "selector", "affine_difference_rank_s_star"), 8),
        ("raw-rank", ("exact_control", "selector", "raw_witness_rank_t"), 9),
        ("locator-rank", ("exact_control", "selector", "locator_vector_rank"), 10),
        ("polynomial-det", ("exact_control", "rank_witnesses", "code_polynomial_minor", "determinant"), 0),
        ("basis-carrier", ("exact_control", "rank_witnesses", "ten_basis_supports_recover_carrier"), False),
        ("NV", ("exact_control", "carrier", "N_V"), 21),
        ("nu", ("exact_control", "carrier", "nu"), 10),
        ("kappa", ("exact_control", "carrier", "kappa_star"), 10),
        ("kappa-proof", ("exact_control", "carrier", "kappa_star_exact_because_selector_unique"), False),
        ("subset-injective", ("exact_control", "injectivity_and_uniqueness", "all_12_subset_products_distinct"), False),
        ("agreement-pair", ("exact_control", "injectivity_and_uniqueness", "nonzero_witness_agreement_pairs"), [[11, 2]]),
        ("quantifier", ("parametric_route_cut", "quantifier"), "EXISTS_ONE_j"),
        ("Gamma-scope", ("parametric_route_cut", "Gamma_scope", "full_bad_slope_set_exhaustion_assumed"), True),
        ("fixed-s", ("parametric_route_cut", "fixed_invariants", "affine_rank_s_star"), 10),
        ("fixed-nu", ("parametric_route_cut", "fixed_invariants", "carrier_excess_nu"), 10),
        ("unbounded", ("parametric_route_cut", "growing_invariant", "unbounded_with_j"), False),
        ("field-existence", ("parametric_route_cut", "finite_field_existence", "finite_extension_exists"), False),
        ("cover", ("parametric_route_cut", "cover_obstruction", "fixed_B_C_cover_possible_for_all_j"), True),
        ("terminal", ("parametric_route_cut", "terminal"), "PAID_LOW_EXCESS_CARRIER"),
        ("generic-refute", ("scope_guards", "generic_local_implication_refuted"), False),
        ("scope-exhaustion", ("scope_guards", "declared_Gamma_exhausts_full_bad_set"), True),
        ("scope-strengthened", ("scope_guards", "full_bad_family_or_deployed_first_match_strengthened_statement_refuted"), True),
        ("domain-overclaim", ("scope_guards", "koalabear_domain_instantiated"), True),
        ("owner-overclaim", ("scope_guards", "project_owner_masks_checked"), True),
        ("residual-overclaim", ("scope_guards", "koalabear_rank9_residual_refuted"), True),
        ("branch-close", ("scope_guards", "branch3_closed"), True),
        ("ledger", ("scope_guards", "ledger_movement"), 1),
        ("generic-verdict", ("audit_sections", "generic_local_verdict"), "GREEN"),
        ("KB-verdict", ("audit_sections", "koalabear_owner_strengthened_verdict"), "GREEN_CLOSED"),
        ("nonclaim", ("nonclaims", 0), "This instantiates KoalaBear."),
    ]


def tamper_selftest() -> int:
    baseline = load_json(CERT_PATH)
    validate_certificate(baseline)
    rejected = 0
    for name, path, replacement in mutation_cases():
        mutated = copy.deepcopy(baseline)
        set_path(mutated, path, replacement)
        mutated["payload_sha256"] = payload_hash(mutated)
        try:
            validate_certificate(mutated)
        except (VerificationError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {name}")

    binding_tamper = copy.deepcopy(baseline)
    binding_tamper["source_bindings"][0]["sha256"] = "0" * 64
    binding_tamper["payload_sha256"] = payload_hash(binding_tamper)
    try:
        validate_certificate(binding_tamper)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("source-binding mutation accepted")

    duplicate_binding = copy.deepcopy(baseline)
    duplicate_binding["source_bindings"].append(copy.deepcopy(duplicate_binding["source_bindings"][0]))
    duplicate_binding["payload_sha256"] = payload_hash(duplicate_binding)
    try:
        validate_certificate(duplicate_binding)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("duplicate binding accepted")

    extra_key = copy.deepcopy(baseline)
    extra_key["unexpected"] = True
    extra_key["payload_sha256"] = payload_hash(extra_key)
    try:
        validate_certificate(extra_key)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("unknown top-level key accepted")

    for raw, label in [
        ('{"schema":"a","schema":"b"}', "duplicate JSON key"),
        ('{"x":NaN}', "nonstandard JSON constant"),
    ]:
        try:
            parse_json(raw, label)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"raw JSON tamper accepted: {label}")
    return rejected


def write_certificate() -> None:
    validate_source_contracts()
    certificate = expected_certificate()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(certificate, indent=2, sort_keys=False, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def print_summary(certificate: dict[str, Any]) -> None:
    selector = certificate["exact_control"]["selector"]
    carrier = certificate["exact_control"]["carrier"]
    pencils = certificate["exact_control"]["five_pencils"]
    print(f"schema={certificate['schema']}")
    print(f"status={certificate['status']}")
    print(f"slopes={pencils['slope_count']} distinct={pencils['distinct_slopes']}")
    print(
        "rank_tuple="
        f"({selector['affine_difference_rank_s_star']},"
        f"{selector['raw_witness_rank_t']},"
        f"{selector['locator_vector_rank']})"
    )
    print(f"carrier_N_V={carrier['N_V']} R={carrier['R']} nu=kappa_star={carrier['nu']}")
    print(f"parametric_locator_rank={certificate['parametric_route_cut']['growing_invariant']['locator_vector_rank']}")
    print(f"terminal={certificate['parametric_route_cut']['terminal']}")
    print("koalabear_residual_status=YELLOW_OPEN")
    print("ledger_movement=0")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write the exact JSON certificate")
    mode.add_argument("--check", action="store_true", help="recompute and validate the certificate")
    mode.add_argument("--tamper-selftest", action="store_true", help="reject semantic and serialization mutations")
    args = parser.parse_args()

    if args.write:
        write_certificate()
        certificate = load_json(CERT_PATH)
        validate_certificate(certificate)
        print_summary(certificate)
        print(f"wrote={CERT_PATH.relative_to(ROOT)}")
        return 0
    if args.check:
        certificate = load_json(CERT_PATH)
        validate_certificate(certificate)
        print_summary(certificate)
        print("certificate_check=PASS")
        return 0
    rejected = tamper_selftest()
    print(f"tamper_selftest=PASS rejected={rejected}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as error:
        print(f"verification_error={error}", file=__import__("sys").stderr)
        raise SystemExit(1)
