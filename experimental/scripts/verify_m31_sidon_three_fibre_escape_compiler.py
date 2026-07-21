#!/usr/bin/env python3
"""Verify the M31 Sidon, three-fibre, and escape route-cut packet.

The artifact proves exact local and conditional theorems, but deliberately
fails closed on the whole-ball M31 list bound.  Assertions are implemented
with explicit exceptions so optimized Python performs identical checks.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
SIGMA = AGREEMENT - K
RADIUS = N - AGREEMENT
BUDGET = P**4 // 2**100
FORBIDDEN = BUDGET + 1
BASE_COMMIT = "f8d29402790331aeca5697ab6da9716406d38043"

LOW_WEIGHT_CAP = K // 2
LOW_WEIGHT_SUPPORT_CAP = LOW_WEIGHT_CAP
HIGH_LAYER_COUNT = RADIUS - LOW_WEIGHT_CAP
HIGH_LAYER_MASS = FORBIDDEN - LOW_WEIGHT_SUPPORT_CAP
SAME_WEIGHT_PACKET = (HIGH_LAYER_MASS + HIGH_LAYER_COUNT - 1) // HIGH_LAYER_COUNT
RANK16_FLOOR_AT_BOUNDARY = 16 * (K - RADIUS) - (K - 1)
RANK36_FLOOR_AT_BOUNDARY = 36 * (K - RADIUS) - (K - 1)

FACTOR_DEGREE = 33 * 1024
ROW_DEGREE = 3 * FACTOR_DEGREE
CORE_SIZE = RADIUS - ROW_DEGREE
TAU_MIN = 0
TAU_MAX = 136
CELL_COUNT = TAU_MAX + 1
MAX_CANCELLED_LOCATOR_ROOTS = 6 * TAU_MAX
MAX_ESCAPE_LINES = 4 * RADIUS
ESCAPE_UNION_MARGIN = P - MAX_ESCAPE_LINES
ANNIHILATOR_DIMENSION_MAX = CORE_SIZE + 137
ANNIHILATOR_DIMENSION_MIN = CORE_SIZE + 1

SIMPLEX_LENGTH = 2**12 - 1
SIMPLEX_DIMENSION = 12
SIMPLEX_DISTANCE = 2**11
REPETITION = 33
DIRECT_SUM_BLOCKS = 4
SIDON_CODE_ACTIVE_LENGTH = DIRECT_SUM_BLOCKS * REPETITION * SIMPLEX_LENGTH
SIDON_CODE_PADDING = RADIUS - SIDON_CODE_ACTIVE_LENGTH
SIDON_CODE_DIMENSION = DIRECT_SUM_BLOCKS * SIMPLEX_DIMENSION
SIDON_CODE_DISTANCE = REPETITION * SIMPLEX_DISTANCE
UNUSED_DOMAIN_POINTS = N - 2 * RADIUS
MAX_AGREEMENT_INTERSECTION = AGREEMENT - SIDON_CODE_DISTANCE

GF24_MODULUS_EXPONENTS = (24, 16, 15, 14, 13, 10, 9, 7, 5, 3, 0)
GF24_MODULUS_BITS = sum(1 << exponent for exponent in GF24_MODULUS_EXPONENTS)
SMALL_GF_DEGREE = 6
SMALL_GF_MODULUS_BITS = (1 << 6) | (1 << 1) | 1

CHEB_TOY_FIELD = 31
CHEB_TOY_DEGREE = 8
CHEB_TOY_ROOTS = (2, 5, 10, 11, 20, 21, 26, 29)
CHEB_TOY_TOTAL = 20_160
CHEB_TOY_FULL_RANK = 19_440
CHEB_TOY_RANK_DROP = 720
CHEB_TOY_FIXTURE = (2, 5, 10, 20, 11, 29)
CHEB_TOY_Q = (4, 25, 13, 23, 19, 14)
CHEB_TOY_RECEIVED = (28, 0, 21, 25, 0, 0, 0, 0)
CHEB_TOY_EXPLANATIONS = (
    (0, 0, 0, 0),
    (30, 23, 11, 4),
    (12, 26, 2, 25),
    (29, 17, 4, 13),
)
CHEB_TOY_FIFTH_SUPPORT = (5, 21, 26)
CHEB_TOY_FIFTH_EXPLANATION = (22, 27, 29, 26)
CHEB_TOY_DOMAIN_STABILIZER_ORDER = 6
CHEB_TOY_UNORDERED_PRIMITIVE_FACES = 30

ESCAPE_COLLISIONS: tuple[dict[str, Any], ...] = (
    {"support": "00", "locator": "A0", "quotients": ["qB0", "qC0"]},
    {"support": "00", "locator": "B0", "quotients": ["qA0", "qC0"]},
    {"support": "00", "locator": "C0", "quotients": ["qA0", "qB0"]},
    {"support": "10", "locator": "A1", "quotients": ["qB0", "qC1"]},
    {"support": "10", "locator": "B0", "quotients": ["qA1", "qC1"]},
    {"support": "10", "locator": "C1", "quotients": ["qA1", "qB0"]},
    {"support": "01", "locator": "A0", "quotients": ["qB1", "qC1"]},
    {"support": "01", "locator": "B1", "quotients": ["qA0", "qC1"]},
    {"support": "01", "locator": "C1", "quotients": ["qA0", "qB1"]},
    {"support": "11", "locator": "A1", "quotients": ["qB1", "qC0"]},
    {"support": "11", "locator": "B1", "quotients": ["qA1", "qC0"]},
    {"support": "11", "locator": "C0", "quotients": ["qA1", "qB1"]},
)

ROOT = Path(__file__).resolve().parents[2]
PYTHON_PATH = ROOT / "experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_sidon_three_fibre_escape_compiler.md"
README_PATH = ROOT / "experimental/data/certificates/m31-sidon-three-fibre-escape-compiler/README.md"
CERTIFICATE_PATH = ROOT / "experimental/data/certificates/m31-sidon-three-fibre-escape-compiler/manifest.json"

SOURCE_PATHS = (
    ROOT / "experimental/notes/audits/sidon_direct_payment.md",
    ROOT / "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md",
    ROOT / "experimental/notes/thresholds/m31_chebyshev_global_separator.md",
    ROOT / "experimental/notes/thresholds/m31_whole_ball_source_separator_compiler.md",
    ROOT / "experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py",
    NOTE_PATH,
    PYTHON_PATH,
    SAGE_PATH,
    README_PATH,
)


class VerificationError(RuntimeError):
    """Raised when an exact semantic certificate gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(payload: Any) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal_certificate(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("certificate_sha256", None)
    out["certificate_sha256"] = hashlib.sha256(canonical_json(out)).hexdigest()
    return out


def verify_self_hash(payload: dict[str, Any]) -> None:
    claimed = payload.get("certificate_sha256")
    require(isinstance(claimed, str) and len(claimed) == 64, "certificate hash shape")
    unsealed = copy.deepcopy(payload)
    unsealed.pop("certificate_sha256", None)
    require(hashlib.sha256(canonical_json(unsealed)).hexdigest() == claimed, "certificate self hash")


def trim(poly: Sequence[int]) -> list[int]:
    out = [int(value) for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(left: Sequence[int], right: Sequence[int], p: int) -> list[int]:
    size = max(len(left), len(right))
    return trim([
        ((left[index] if index < len(left) else 0)
         + (right[index] if index < len(right) else 0)) % p
        for index in range(size)
    ])


def poly_scale(poly: Sequence[int], scalar: int, p: int) -> list[int]:
    return trim([(scalar * value) % p for value in poly])


def poly_mul(left: Sequence[int], right: Sequence[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out)


def poly_eval(poly: Sequence[int], value: int, p: int) -> int:
    out = 0
    for coefficient in reversed(poly):
        out = (out * value + coefficient) % p
    return out


def locator(point: int, p: int) -> list[int]:
    return [(-point) % p, 1]


def rank_mod(columns: Sequence[Sequence[int]], p: int) -> int:
    require(bool(columns), "rank has columns")
    rows = len(columns[0])
    require(all(len(column) == rows for column in columns), "rank rectangular")
    matrix = [[columns[column][row] % p for column in range(len(columns))] for row in range(rows)]
    rank = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(rank, rows) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, p)
        matrix[rank] = [(inverse * value) % p for value in matrix[rank]]
        for row in range(rows):
            if row == rank or matrix[row][column] == 0:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                (matrix[row][index] - multiplier * matrix[rank][index]) % p
                for index in range(len(columns))
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def left_kernel_line(columns: Sequence[Sequence[int]], p: int) -> list[int]:
    """Return the normalized left-kernel generator of a corank-one square matrix."""
    size = len(columns)
    require(size > 0 and all(len(column) == size for column in columns), "left kernel square")
    matrix = [[columns[column][row] % p for row in range(size)] for column in range(size)]
    # This is the nullspace of the transpose: rows above are the original columns.
    rank = 0
    pivots: list[int] = []
    for column in range(size):
        pivot = next((row for row in range(rank, size) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, p)
        matrix[rank] = [(inverse * value) % p for value in matrix[rank]]
        for row in range(size):
            if row == rank or matrix[row][column] == 0:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                (matrix[row][index] - multiplier * matrix[rank][index]) % p
                for index in range(size)
            ]
        pivots.append(column)
        rank += 1
    require(rank == size - 1, "left kernel has dimension one")
    free = next(column for column in range(size) if column not in pivots)
    vector = [0] * size
    vector[free] = 1
    for row in range(rank - 1, -1, -1):
        pivot = pivots[row]
        vector[pivot] = -sum(matrix[row][column] * vector[column] for column in range(pivot + 1, size)) % p
    first = next(value for value in vector if value)
    inverse = pow(first, -1, p)
    vector = [(inverse * value) % p for value in vector]
    require(all(sum(columns[column][row] * vector[row] for row in range(size)) % p == 0
                for column in range(size)), "left kernel replay")
    return vector


def divide_by_root(poly: Sequence[int], root: int, p: int) -> list[int]:
    """Exactly divide a coefficient-order polynomial by X-root."""
    require(len(poly) >= 2 and poly_eval(poly, root, p) == 0, "root exact division")
    quotient = [0] * (len(poly) - 1)
    quotient[-1] = poly[-1] % p
    for index in range(len(poly) - 2, 0, -1):
        quotient[index - 1] = (poly[index] + root * quotient[index]) % p
    require(poly_mul(quotient, locator(root, p), p) == trim(poly), "root division replay")
    return trim(quotient)


def chebyshev_standard(degree: int, p: int) -> list[int]:
    require(degree >= 0, "nonnegative Chebyshev degree")
    if degree == 0:
        return [1]
    if degree == 1:
        return [0, 1]
    previous, current = [1], [0, 1]
    for _ in range(2, degree + 1):
        doubled_x_current = poly_mul([0, 2], current, p)
        following = poly_add(doubled_x_current, poly_scale(previous, -1, p), p)
        previous, current = current, following
    return current


def parity_columns(values: Sequence[int], p: int) -> tuple[list[int], ...]:
    require(len(values) == 6 and len(set(values)) == 6, "six distinct factors")
    a0, a1, b0, b1, c0, c1 = (locator(value, p) for value in values)
    return (
        poly_mul(poly_mul(a0, b0, p), c0, p),
        poly_mul(poly_mul(a1, b0, p), c1, p),
        poly_mul(poly_mul(a0, b1, p), c1, p),
        poly_mul(poly_mul(a1, b1, p), c0, p),
    )


def chebyshev_toy_control() -> dict[str, Any]:
    polynomial = chebyshev_standard(CHEB_TOY_DEGREE, CHEB_TOY_FIELD)
    roots = tuple(value for value in range(CHEB_TOY_FIELD) if poly_eval(polynomial, value, CHEB_TOY_FIELD) == 0)
    require(roots == CHEB_TOY_ROOTS, "GF31 T8 roots")
    counts: Counter[int] = Counter()
    first_drop: tuple[int, ...] | None = None
    escape_valid_rank_drops = 0
    faces: set[tuple[tuple[int, ...], ...]] = set()
    for values in itertools.permutations(roots, 6):
        columns = parity_columns(values, CHEB_TOY_FIELD)
        rank = rank_mod(columns, CHEB_TOY_FIELD)
        counts[rank] += 1
        if rank == 3 and first_drop is None:
            first_drop = values
        if rank == 3:
            functional = left_kernel_line(columns, CHEB_TOY_FIELD)
            a0, a1, b0, b1, c0, c1 = values
            support_roots = (
                (a0, b0, c0),
                (a1, b0, c1),
                (a0, b1, c1),
                (a1, b1, c0),
            )
            guards_nonzero = True
            for column, local_roots in zip(columns, support_roots):
                for root in local_roots:
                    direction = divide_by_root(column, root, CHEB_TOY_FIELD) + [0]
                    if sum(functional[index] * direction[index] for index in range(4)) % CHEB_TOY_FIELD == 0:
                        guards_nonzero = False
            if guards_nonzero:
                escape_valid_rank_drops += 1
            faces.add(tuple(sorted(tuple(sorted(support)) for support in support_roots)))
    require(sum(counts.values()) == CHEB_TOY_TOTAL, "GF31 census size")
    require(dict(counts) == {4: CHEB_TOY_FULL_RANK, 3: CHEB_TOY_RANK_DROP}, "GF31 rank census")
    require(first_drop == CHEB_TOY_FIXTURE, "GF31 canonical rank-drop fixture")
    require(escape_valid_rank_drops == CHEB_TOY_RANK_DROP, "all GF31 rank drops escape valid")
    require(len(faces) == CHEB_TOY_UNORDERED_PRIMITIVE_FACES, "GF31 unordered face count")

    pgl_representatives: set[tuple[int, int, int, int]] = set()
    for entries in itertools.product(range(CHEB_TOY_FIELD), repeat=4):
        a, b, c, d = entries
        if (a * d - b * c) % CHEB_TOY_FIELD == 0:
            continue
        first = next(value for value in entries if value)
        inverse = pow(first, -1, CHEB_TOY_FIELD)
        pgl_representatives.add(tuple(value * inverse % CHEB_TOY_FIELD for value in entries))
    require(len(pgl_representatives) == CHEB_TOY_FIELD * (CHEB_TOY_FIELD**2 - 1), "GF31 PGL2 order")

    def action(matrix: tuple[int, int, int, int], point: int) -> int | None:
        a, b, c, d = matrix
        denominator = (c * point + d) % CHEB_TOY_FIELD
        if denominator == 0:
            return None
        return (a * point + b) * pow(denominator, -1, CHEB_TOY_FIELD) % CHEB_TOY_FIELD

    root_set = set(roots)
    domain_stabilizer = []
    for matrix in sorted(pgl_representatives):
        image = [action(matrix, point) for point in roots]
        if None not in image and set(image) == root_set:
            domain_stabilizer.append(matrix)
    require(domain_stabilizer == [
        (1, 0, 0, 1),
        (1, 0, 0, 30),
        (1, 3, 1, 30),
        (1, 3, 30, 1),
        (1, 28, 1, 1),
        (1, 28, 30, 30),
    ], "GF31 T8 domain stabilizer")
    for face in faces:
        stabilizer = []
        target = set(face)
        for matrix in domain_stabilizer:
            image = {
                tuple(sorted(action(matrix, point) for point in support))
                for support in face
            }
            if image == target:
                stabilizer.append(matrix)
        require(stabilizer == [(1, 0, 0, 1)], "GF31 face stabilizer trivial")

    for fold_degree in (2, 4, 8):
        fold = chebyshev_standard(fold_degree, CHEB_TOY_FIELD)
        fibres: dict[int, set[int]] = {}
        for point in roots:
            fibres.setdefault(poly_eval(fold, point, CHEB_TOY_FIELD), set()).add(point)
        require({len(fibre) for fibre in fibres.values()} == {fold_degree}, "GF31 dyadic fibre sizes")
        for face in faces:
            for support in face:
                selected = [fibre for fibre in fibres.values() if fibre <= set(support)]
                selected_union = set().union(*selected) if selected else set()
                require(selected_union != set(support), "GF31 support not quotient invariant")

    a0, a1, b0, b1, c0, c1 = CHEB_TOY_FIXTURE
    supports = (
        {a0, b0, c0},
        {a1, b0, c1},
        {a0, b1, c1},
        {a1, b1, c0},
    )
    require(len(set().union(*supports)) == 6, "toy factor union")
    exact_errors = []
    for support, explanation in zip(supports, CHEB_TOY_EXPLANATIONS):
        error_support = {
            point
            for point, received in zip(CHEB_TOY_ROOTS, CHEB_TOY_RECEIVED)
            if (received - poly_eval(explanation, point, CHEB_TOY_FIELD)) % CHEB_TOY_FIELD != 0
        }
        require(error_support == support, "toy explanation exact support")
        exact_errors.append(sorted(error_support))

    q_a0, q_a1, q_b0, q_b1, q_c0, q_c1 = CHEB_TOY_Q
    factors = [locator(value, CHEB_TOY_FIELD) for value in CHEB_TOY_FIXTURE]
    A0, A1, B0, B1, C0, C1 = factors
    M_A = poly_scale(poly_mul(A0, A1, CHEB_TOY_FIELD), q_a0 * q_a1, CHEB_TOY_FIELD)
    M_B = poly_scale(poly_mul(B0, B1, CHEB_TOY_FIELD), q_b0 * q_b1, CHEB_TOY_FIELD)
    M_C = poly_scale(poly_mul(C0, C1, CHEB_TOY_FIELD), q_c0 * q_c1, CHEB_TOY_FIELD)
    require(poly_add(M_B, M_C, CHEB_TOY_FIELD) == M_A, "toy three-fibre identity")
    require(all(value % CHEB_TOY_FIELD for value in CHEB_TOY_Q), "toy tau0 quotients nonzero")

    radius_three: dict[tuple[int, ...], tuple[int, ...]] = {}
    weight_counts: Counter[int] = Counter()
    for explanation in itertools.product(range(CHEB_TOY_FIELD), repeat=4):
        support = tuple(
            point
            for point, received in zip(CHEB_TOY_ROOTS, CHEB_TOY_RECEIVED)
            if (received - poly_eval(explanation, point, CHEB_TOY_FIELD)) % CHEB_TOY_FIELD != 0
        )
        if len(support) <= 3:
            require(support not in radius_three, "toy exact support duplicate")
            radius_three[support] = explanation
            weight_counts[len(support)] += 1
    require(weight_counts == Counter({3: 5}), "toy closed radius-three list")
    require(tuple(sorted(radius_three)) == tuple(sorted(tuple(sorted(support)) for support in supports)
            + [CHEB_TOY_FIFTH_SUPPORT]), "toy radius-three support set")
    require(radius_three[CHEB_TOY_FIFTH_SUPPORT] == CHEB_TOY_FIFTH_EXPLANATION, "toy fifth explanation")

    return {
        "field": CHEB_TOY_FIELD,
        "chebyshev_degree": CHEB_TOY_DEGREE,
        "roots": list(roots),
        "ordered_distinct_sextuples": CHEB_TOY_TOTAL,
        "theta1_rank4": CHEB_TOY_FULL_RANK,
        "theta1_rank3": CHEB_TOY_RANK_DROP,
        "escape_valid_rank3": escape_valid_rank_drops,
        "unordered_escape_valid_faces": CHEB_TOY_UNORDERED_PRIMITIVE_FACES,
        "rank_drop_fraction": [CHEB_TOY_RANK_DROP, CHEB_TOY_TOTAL],
        "fixture": list(CHEB_TOY_FIXTURE),
        "fixture_tau": 0,
        "fixture_q": list(CHEB_TOY_Q),
        "fixture_received_values_in_root_order": list(CHEB_TOY_RECEIVED),
        "fixture_explanations_coefficient_order": [list(poly) for poly in CHEB_TOY_EXPLANATIONS],
        "fixture_exact_error_supports": exact_errors,
        "all_fixture_escape_collisions_empty": True,
        "closed_radius_three_list_size": len(radius_three),
        "closed_radius_three_weight_counts": {str(key): value for key, value in sorted(weight_counts.items())},
        "fifth_exact_support": list(CHEB_TOY_FIFTH_SUPPORT),
        "fifth_explanation_coefficient_order": list(CHEB_TOY_FIFTH_EXPLANATION),
        "domain_stabilizer_order": CHEB_TOY_DOMAIN_STABILIZER_ORDER,
        "nontrivial_face_support_stabilizers": 0,
        "nontrivial_dyadic_quotient_owned_faces": 0,
        "symmetry_dyadic_primitive_faces": CHEB_TOY_UNORDERED_PRIMITIVE_FACES,
        "deployed_implication": False,
    }


def gf2_mul(left: int, right: int, modulus: int, degree: int) -> int:
    out = 0
    a, b = left, right
    mask = (1 << degree) - 1
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
    return out & mask


def small_sidon_control() -> dict[str, Any]:
    size = 1 << SMALL_GF_DEGREE
    cubes = [gf2_mul(gf2_mul(value, value, SMALL_GF_MODULUS_BITS, SMALL_GF_DEGREE), value,
                     SMALL_GF_MODULUS_BITS, SMALL_GF_DEGREE) for value in range(size)]
    pair_sums: dict[tuple[int, int], tuple[int, int]] = {}
    for left, right in itertools.combinations(range(size), 2):
        key = (left ^ right, cubes[left] ^ cubes[right])
        require(key not in pair_sums, "small Sidon pair-sum uniqueness")
        pair_sums[key] = (left, right)
    require(len(pair_sums) == size * (size - 1) // 2, "small Sidon pair count")
    return {
        "field_size": size,
        "modulus_bits": SMALL_GF_MODULUS_BITS,
        "graph_size": size,
        "unordered_distinct_pairs": len(pair_sums),
        "pair_sum_collisions": 0,
        "deployed_implication": False,
    }


def defect_cells() -> list[dict[str, int]]:
    cells = []
    for tau in range(TAU_MIN, TAU_MAX + 1):
        cells.append({
            "tau": tau,
            "cokernel_defect": 137 - tau,
            "rational_degree_lower": 2 * FACTOR_DEGREE - 2 * tau,
            "rational_degree_upper": 2 * FACTOR_DEGREE + 2 * tau,
            "distinct_domain_points_per_special_fibre_lower": 2 * FACTOR_DEGREE - 2 * tau,
            "simple_domain_points_per_special_fibre_lower": 2 * FACTOR_DEGREE - 4 * tau,
            "cancelled_locator_roots_upper": 6 * tau,
            "forced_escape_incidences_per_support_upper": 3 * tau,
        })
    require(len(cells) == CELL_COUNT, "137 defect cells")
    require(cells[0] == {
        "tau": 0,
        "cokernel_defect": 137,
        "rational_degree_lower": 67_584,
        "rational_degree_upper": 67_584,
        "distinct_domain_points_per_special_fibre_lower": 67_584,
        "simple_domain_points_per_special_fibre_lower": 67_584,
        "cancelled_locator_roots_upper": 0,
        "forced_escape_incidences_per_support_upper": 0,
    }, "tau0 cell")
    require(cells[-1]["rational_degree_lower"] == 67_312, "worst degree lower")
    require(cells[-1]["rational_degree_upper"] == 67_856, "worst degree upper")
    require(cells[-1]["simple_domain_points_per_special_fibre_lower"] == 67_040, "worst simple roots")
    require(cells[-1]["cancelled_locator_roots_upper"] == 816, "worst cancelled roots")
    return cells


def validate_contract(payload: dict[str, Any]) -> None:
    require(payload["artifact_kind"] == "M31_ACTIVATION_ROUTE_CUT_COMPILER", "artifact kind")
    require(payload["terminal"] == "ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_REQUIRED", "artifact terminal")

    extraction = payload["whole_ball_same_weight_extraction"]
    require(extraction["forbidden_family_size"] == FORBIDDEN, "extraction family size")
    require(extraction["low_weight_support_cap"] == LOW_WEIGHT_SUPPORT_CAP, "low support cap")
    require(extraction["high_layer_count"] == HIGH_LAYER_COUNT, "high layer count")
    require(extraction["high_layer_mass_lower"] == HIGH_LAYER_MASS, "high layer mass")
    require(extraction["same_weight_packet_lower"] == SAME_WEIGHT_PACKET == 36, "same-weight 36")
    require(extraction["rank16_kernel_floor_at_boundary"] == RANK16_FLOOR_AT_BOUNDARY, "rank16 floor")
    require(extraction["rank36_kernel_floor_at_boundary"] == RANK36_FLOOR_AT_BOUNDARY, "rank36 floor")
    require(extraction["factorized_face_guaranteed"] is False, "extraction face nonclaim")

    sidon = payload["sidon_source_selection_wall"]
    require(sidon["distinct_from_C9_N20_sidon_direct_payment"] is True, "Sidon scope distinction")
    require(sidon["code_parameters"] == [RADIUS, SIDON_CODE_DIMENSION, SIDON_CODE_DISTANCE], "Sidon code parameters")
    require(sidon["active_length"] == SIDON_CODE_ACTIVE_LENGTH, "Sidon active length")
    require(sidon["zero_padding"] == SIDON_CODE_PADDING, "Sidon padding")
    require(sidon["subset_size"] == FORBIDDEN, "Sidon subset size")
    require(sidon["unused_domain_points"] == UNUSED_DOMAIN_POINTS, "Sidon unused points")
    require(sidon["maximum_agreement_intersection"] == K - 137, "Sidon intersection")
    require(sidon["four_distinct_zero_sum_labels"] == 0, "Sidon no parity face")
    require(sidon["common_hyperplane_realized"] is False, "Sidon hyperplane nonclaim")
    require(sidon["invariants_rejected"] == [
        "CARDINALITY",
        "BOUNDARY_WEIGHT",
        "PAIRWISE_MDS_PACKING",
        "K_PLUS_2_SHADOW",
        "INDEPENDENT_COORDINATE_SHORTENED_LOCAL_LINES",
    ], "Sidon rejected invariants")

    three = payload["conditional_three_fibre_compiler"]
    require(three["conditional_on_selected_rank_drop_face"] is True, "three-fibre conditional scope")
    require(three["cell_count"] == CELL_COUNT, "three-fibre cells")
    require(three["cells"] == defect_cells(), "three-fibre cell ledger")
    require(three["pairwise_coprime_reduced_fibre_polynomials"] is True, "three-fibre coprime")
    require(three["separable"] is True, "three-fibre separability")
    require(three["named_quotient_owner_proved"] is False, "three-fibre owner nonclaim")

    escape = payload["conditional_escape_compiler"]
    require(escape["collision_table"] == list(ESCAPE_COLLISIONS), "escape collision table")
    require(escape["evaluated_frame_gate"] == "UNIMODULAR_FORNEY_TWO_FRAME", "unimodular gate")
    require(escape["primitive_q_gcd_alone_sufficient"] is False, "q primitive insufficiency")
    require(escape["maximum_escape_lines"] == MAX_ESCAPE_LINES, "escape line count")
    require(escape["field_minus_escape_lines"] == ESCAPE_UNION_MARGIN, "escape union margin")
    require(escape["terminals"] == ["ESCAPE_KILLED", "ACTUAL_HYPERPLANE_SURVIVOR"], "escape terminals")
    require(escape["tau0_terminal"] == "ACTUAL_HYPERPLANE_SURVIVOR", "tau0 survives")
    require(escape["whole_list_closed"] is False, "four survivors do not close")

    toy = payload["literal_chebyshev_toy_control"]
    require(toy["ordered_distinct_sextuples"] == CHEB_TOY_TOTAL, "toy sextuple count")
    require(toy["theta1_rank3"] == CHEB_TOY_RANK_DROP, "toy rank-drop count")
    require(toy["escape_valid_rank3"] == CHEB_TOY_RANK_DROP, "toy escape-valid count")
    require(toy["unordered_escape_valid_faces"] == CHEB_TOY_UNORDERED_PRIMITIVE_FACES, "toy unordered faces")
    require(toy["closed_radius_three_list_size"] == 5, "toy closed list size")
    require(toy["closed_radius_three_weight_counts"] == {"3": 5}, "toy weight census")
    require(toy["domain_stabilizer_order"] == CHEB_TOY_DOMAIN_STABILIZER_ORDER, "toy domain stabilizer")
    require(toy["nontrivial_face_support_stabilizers"] == 0, "toy primitive symmetry")
    require(toy["nontrivial_dyadic_quotient_owned_faces"] == 0, "toy primitive quotient")
    require(toy["symmetry_dyadic_primitive_faces"] == CHEB_TOY_UNORDERED_PRIMITIVE_FACES, "toy scoped primitive faces")
    require(toy["deployed_implication"] is False, "toy deployed nonclaim")

    closure = payload["closure_state"]
    require(closure["closure_certified"] is False, "closure remains open")
    require(closure["result"] == "ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_REQUIRED", "open result")
    require(closure["source_valid_face_extraction_proved"] is False, "source extraction open")
    require(closure["global_add_back_proved"] is False, "add-back open")
    require(closure["ledger_movement"] == 0, "zero ledger movement")
    require(all(value is None for value in closure["ledger_atoms"].values()), "null ledger atoms")
    require(closure["unresolved_terminals"] == [
        "ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_OPEN",
        "GENERAL_EQUAL_WEIGHT_RANK_PACKET_CLASSIFICATION_OPEN",
        "THREE_FIBRE_CHEBYSHEV_RIGIDITY_OR_OWNER_OPEN",
        "INTERIOR_WEIGHT_ADDBACK_OPEN",
        "GLOBAL_DISJOINT_ADDBACK_OPEN",
    ], "canonical unresolved terminals")


def build_certificate() -> dict[str, Any]:
    require((P, N, K, AGREEMENT) == (2_147_483_647, 2_097_152, 1_048_576, 1_116_023), "M31 parameters")
    require((SIGMA, RADIUS, BUDGET, FORBIDDEN) == (67_447, 981_129, 16_777_215, 16_777_216), "M31 row arithmetic")
    require((HIGH_LAYER_MASS, HIGH_LAYER_COUNT, SAME_WEIGHT_PACKET) == (16_252_928, 456_841, 36), "same-weight arithmetic")
    require((RANK16_FLOOR_AT_BOUNDARY, RANK36_FLOOR_AT_BOUNDARY) == (30_577, 1_379_517), "kernel floors")
    require((FACTOR_DEGREE, ROW_DEGREE, CORE_SIZE) == (33_792, 101_376, 879_753), "face degrees")
    require((SIDON_CODE_ACTIVE_LENGTH, SIDON_CODE_PADDING) == (540_540, 440_589), "Sidon lengths")
    require((SIDON_CODE_DIMENSION, SIDON_CODE_DISTANCE) == (48, 67_584), "Sidon code")
    require(MAX_AGREEMENT_INTERSECTION == K - 137 == 1_048_439, "agreement intersection")
    require(UNUSED_DOMAIN_POINTS == 134_894, "unused domain points")
    require((MAX_ESCAPE_LINES, ESCAPE_UNION_MARGIN) == (3_924_516, 2_143_559_131), "escape union bound")
    require((ANNIHILATOR_DIMENSION_MIN, ANNIHILATOR_DIMENSION_MAX) == (879_754, 879_890), "annihilator dimensions")
    require(GF24_MODULUS_BITS.bit_length() == 25, "GF24 modulus degree")

    cells = defect_cells()
    toy = chebyshev_toy_control()
    small_sidon = small_sidon_control()
    payload: dict[str, Any] = {
        "schema": "m31-sidon-three-fibre-escape-compiler-v1",
        "artifact_kind": "M31_ACTIVATION_ROUTE_CUT_COMPILER",
        "terminal": "ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_REQUIRED",
        "base_commit": BASE_COMMIT,
        "status": "PROVED_CONDITIONAL_FACE_TERMINALS_GLOBAL_ACTIVATION_OPEN",
        "parameters": {
            "p": P,
            "n": N,
            "k": K,
            "agreement": AGREEMENT,
            "sigma": SIGMA,
            "radius": RADIUS,
            "budget": BUDGET,
            "forbidden_size": FORBIDDEN,
        },
        "whole_ball_same_weight_extraction": {
            "forbidden_family_size": FORBIDDEN,
            "low_weight_interval": [1, LOW_WEIGHT_CAP],
            "low_weight_support_cap": LOW_WEIGHT_SUPPORT_CAP,
            "high_weight_interval": [LOW_WEIGHT_CAP + 1, RADIUS],
            "high_layer_count": HIGH_LAYER_COUNT,
            "high_layer_mass_lower": HIGH_LAYER_MASS,
            "same_weight_packet_lower": SAME_WEIGHT_PACKET,
            "rank_kernel_formula": "m*(K-j)-(K-1)",
            "rank16_kernel_floor_at_boundary": RANK16_FLOOR_AT_BOUNDARY,
            "rank36_kernel_floor_at_boundary": RANK36_FLOOR_AT_BOUNDARY,
            "original_containments_preserved": True,
            "original_one_point_escapes_preserved": True,
            "factorized_face_guaranteed": False,
        },
        "sidon_source_selection_wall": {
            "distinct_from_C9_N20_sidon_direct_payment": True,
            "simplex_parameters": [SIMPLEX_LENGTH, SIMPLEX_DIMENSION, SIMPLEX_DISTANCE],
            "coordinate_repetition": REPETITION,
            "direct_sum_blocks": DIRECT_SUM_BLOCKS,
            "active_length": SIDON_CODE_ACTIVE_LENGTH,
            "zero_padding": SIDON_CODE_PADDING,
            "code_parameters": [RADIUS, SIDON_CODE_DIMENSION, SIDON_CODE_DISTANCE],
            "message_space": "GF(2^24)^2",
            "subset": "{(x,x^3):x in GF(2^24)}",
            "subset_size": FORBIDDEN,
            "gf24_modulus_exponents": list(GF24_MODULUS_EXPONENTS),
            "sidon_symbolic_proof": "equal_sum_and_equal_cube_give_equal_product_and_equal_unordered_pair",
            "small_exact_control": small_sidon,
            "transversal_pair_count": RADIUS,
            "unused_domain_points": UNUSED_DOMAIN_POINTS,
            "maximum_agreement_intersection": MAX_AGREEMENT_INTERSECTION,
            "four_distinct_zero_sum_labels": 0,
            "factorized_parity_face_present": False,
            "K_plus_2_completion_replays": True,
            "first_two_selected_shell_formulas_replay": True,
            "common_hyperplane_realized": False,
            "exact_received_word_family": False,
            "invariants_rejected": [
                "CARDINALITY",
                "BOUNDARY_WEIGHT",
                "PAIRWISE_MDS_PACKING",
                "K_PLUS_2_SHADOW",
                "INDEPENDENT_COORDINATE_SHORTENED_LOCAL_LINES",
            ],
        },
        "conditional_three_fibre_compiler": {
            "conditional_on_selected_rank_drop_face": True,
            "factor_degree": FACTOR_DEGREE,
            "row_degree": ROW_DEGREE,
            "tau_interval": [TAU_MIN, TAU_MAX],
            "cell_count": CELL_COUNT,
            "identity": "MA=MB+MC",
            "MA": "A0*A1*qA0*qA1",
            "MB": "B0*B1*qB0*qB1",
            "MC": "C0*C1*qC0*qC1",
            "common_gcd": "gcd(MA,MC)=gcd(MA,MB)=gcd(MB,MC)",
            "pairwise_coprime_reduced_fibre_polynomials": True,
            "rational_map": "lambda=(MA/g)/(MC/g)",
            "special_fibres": [0, 1, "infinity"],
            "separable": True,
            "separability_reason": "nonconstant degree strictly below characteristic",
            "cells": cells,
            "worst_cell": cells[-1],
            "surviving_locator_roots_all_fibres_lower": 6 * FACTOR_DEGREE - MAX_CANCELLED_LOCATOR_ROOTS,
            "simple_locator_roots_all_fibres_lower": 6 * FACTOR_DEGREE - 12 * TAU_MAX,
            "named_quotient_owner_proved": False,
            "received_data_descent_proved": False,
        },
        "conditional_escape_compiler": {
            "conditional_on_selected_rank_drop_face": True,
            "quotient_dimension": "137-tau",
            "variable_direction": "[P_i/(X-alpha)] in coker(Theta_sigma)",
            "zero_direction_criterion": "e_i in rowspan(S(alpha),T(alpha))",
            "evaluated_frame_gate": "UNIMODULAR_FORNEY_TWO_FRAME",
            "primitive_q_gcd_alone_sufficient": False,
            "collision_table": list(ESCAPE_COLLISIONS),
            "forced_incidences_per_support_upper": "3*tau",
            "core_escape_directions_automatically_nonzero": True,
            "annihilator_dimension_interval": [ANNIHILATOR_DIMENSION_MIN, ANNIHILATOR_DIMENSION_MAX],
            "maximum_escape_lines": MAX_ESCAPE_LINES,
            "field_minus_escape_lines": ESCAPE_UNION_MARGIN,
            "surviving_functional_lower": "p^(c+h-1)*(p-4R)",
            "center_to_functional_surjective": True,
            "terminals": ["ESCAPE_KILLED", "ACTUAL_HYPERPLANE_SURVIVOR"],
            "tau0_collision_sets_empty": True,
            "tau0_terminal": "ACTUAL_HYPERPLANE_SURVIVOR",
            "four_codeword_survivor_is_forbidden_list": False,
            "whole_list_closed": False,
        },
        "literal_chebyshev_toy_control": toy,
        "closure_state": {
            "closure_certified": False,
            "result": "ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_REQUIRED",
            "source_valid_face_extraction_proved": False,
            "interior_covered": False,
            "boundary_unrestricted_covered": False,
            "global_add_back_proved": False,
            "unresolved_terminals": [
                "ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_OPEN",
                "GENERAL_EQUAL_WEIGHT_RANK_PACKET_CLASSIFICATION_OPEN",
                "THREE_FIBRE_CHEBYSHEV_RIGIDITY_OR_OWNER_OPEN",
                "INTERIOR_WEIGHT_ADDBACK_OPEN",
                "GLOBAL_DISJOINT_ADDBACK_OPEN",
            ],
            "ledger_atoms": {
                "U_paid": None,
                "U_Q": None,
                "U_list_int": None,
                "U_new": None,
            },
            "ledger_movement": 0,
            "prime_field_row_closed": False,
            "quartic_field_row_closed": False,
            "prize_claimed": False,
        },
        "provenance": {
            "parent_pr": 1003,
            "parent_head": BASE_COMMIT,
            "support_flat_wall": "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md",
            "factorized_face": "experimental/notes/thresholds/m31_chebyshev_global_separator.md",
            "pluecker_compiler": "experimental/notes/thresholds/m31_whole_ball_source_separator_compiler.md",
        },
        "source_sha256": {str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS},
    }
    validate_contract(payload)
    return seal_certificate(payload)


def validate_certificate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    verify_self_hash(candidate)
    validate_contract(candidate)
    require(candidate == expected, "canonical certificate payload")


def set_path(payload: dict[str, Any], path: Sequence[str], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations: tuple[tuple[tuple[str, ...], Any], ...] = (
        (("base_commit",), "0" * 40),
        (("parameters", "budget"), BUDGET + 1),
        (("whole_ball_same_weight_extraction", "low_weight_support_cap"), LOW_WEIGHT_SUPPORT_CAP + 1),
        (("whole_ball_same_weight_extraction", "high_layer_count"), HIGH_LAYER_COUNT - 1),
        (("whole_ball_same_weight_extraction", "high_layer_mass_lower"), HIGH_LAYER_MASS - 1),
        (("whole_ball_same_weight_extraction", "same_weight_packet_lower"), 35),
        (("whole_ball_same_weight_extraction", "rank16_kernel_floor_at_boundary"), RANK16_FLOOR_AT_BOUNDARY - 1),
        (("whole_ball_same_weight_extraction", "rank36_kernel_floor_at_boundary"), RANK36_FLOOR_AT_BOUNDARY - 1),
        (("whole_ball_same_weight_extraction", "factorized_face_guaranteed"), True),
        (("sidon_source_selection_wall", "code_parameters"), [RADIUS, 48, SIDON_CODE_DISTANCE - 1]),
        (("sidon_source_selection_wall", "distinct_from_C9_N20_sidon_direct_payment"), False),
        (("sidon_source_selection_wall", "active_length"), SIDON_CODE_ACTIVE_LENGTH - 1),
        (("sidon_source_selection_wall", "zero_padding"), SIDON_CODE_PADDING + 1),
        (("sidon_source_selection_wall", "subset_size"), BUDGET),
        (("sidon_source_selection_wall", "unused_domain_points"), UNUSED_DOMAIN_POINTS - 1),
        (("sidon_source_selection_wall", "maximum_agreement_intersection"), K),
        (("sidon_source_selection_wall", "four_distinct_zero_sum_labels"), 1),
        (("sidon_source_selection_wall", "common_hyperplane_realized"), True),
        (("sidon_source_selection_wall", "invariants_rejected"), ["CARDINALITY"]),
        (("conditional_three_fibre_compiler", "cell_count"), 136),
        (("conditional_three_fibre_compiler", "pairwise_coprime_reduced_fibre_polynomials"), False),
        (("conditional_three_fibre_compiler", "separable"), False),
        (("conditional_three_fibre_compiler", "cells"), expected["conditional_three_fibre_compiler"]["cells"][:-1]),
        (("conditional_three_fibre_compiler", "named_quotient_owner_proved"), True),
        (("conditional_escape_compiler", "evaluated_frame_gate"), "PRIMITIVE_Q_GCD"),
        (("conditional_escape_compiler", "primitive_q_gcd_alone_sufficient"), True),
        (("conditional_escape_compiler", "collision_table"), list(reversed(ESCAPE_COLLISIONS))),
        (("conditional_escape_compiler", "maximum_escape_lines"), MAX_ESCAPE_LINES - 1),
        (("conditional_escape_compiler", "field_minus_escape_lines"), ESCAPE_UNION_MARGIN + 1),
        (("conditional_escape_compiler", "terminals"), ["ESCAPE_KILLED"]),
        (("conditional_escape_compiler", "tau0_terminal"), "ESCAPE_KILLED"),
        (("conditional_escape_compiler", "whole_list_closed"), True),
        (("literal_chebyshev_toy_control", "theta1_rank3"), CHEB_TOY_RANK_DROP - 1),
        (("literal_chebyshev_toy_control", "escape_valid_rank3"), CHEB_TOY_RANK_DROP - 1),
        (("literal_chebyshev_toy_control", "closed_radius_three_list_size"), 4),
        (("literal_chebyshev_toy_control", "symmetry_dyadic_primitive_faces"), 29),
        (("literal_chebyshev_toy_control", "fixture_q"), [0, 25, 13, 23, 19, 14]),
        (("closure_state", "closure_certified"), True),
        (("closure_state", "result"), "SAFE"),
        (("closure_state", "source_valid_face_extraction_proved"), True),
        (("closure_state", "global_add_back_proved"), True),
        (("closure_state", "ledger_atoms", "U_Q"), 0),
        (("closure_state", "ledger_movement"), 1),
        (("closure_state", "unresolved_terminals"), []),
        (("source_sha256", "experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py"), "0" * 64),
    )
    rejected = 0
    for path, value in mutations:
        mutated = copy.deepcopy(expected)
        set_path(mutated, path, value)
        mutated = seal_certificate(mutated)
        try:
            validate_certificate(mutated, expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {'.'.join(path)}")

    raw_hash = copy.deepcopy(expected)
    raw_hash["certificate_sha256"] = "0" * 64
    raw_payload = copy.deepcopy(expected)
    raw_payload["parameters"]["radius"] = RADIUS - 1
    for label, mutated in (("raw hash", raw_hash), ("raw payload", raw_payload)):
        try:
            validate_certificate(mutated, expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")
    require(rejected == len(mutations) + 2, "all tampers rejected")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare with the pinned manifest")
    parser.add_argument("--print-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build_certificate()
    if args.print_certificate:
        print(json.dumps(expected, indent=2, sort_keys=True))
        return
    if args.tamper_selftest:
        rejected = tamper_selftest(expected)
        print(f"M31 Sidon/three-fibre/escape tampers: {rejected}/{rejected} rejected PASS")
        return
    require(args.check, "explicit --check required")
    require(CERTIFICATE_PATH.exists(), "pinned manifest exists")
    pinned = json.loads(CERTIFICATE_PATH.read_text())
    validate_certificate(pinned, expected)
    print(f"M31 Sidon/three-fibre/escape compiler PASS ({CHECKS} exact checks)")
    print("RESULT: ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_REQUIRED")
    print("M31 rows remain OPEN; ledger movement 0")


if __name__ == "__main__":
    main()
