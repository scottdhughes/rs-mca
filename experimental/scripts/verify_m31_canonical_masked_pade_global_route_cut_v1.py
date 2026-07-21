#!/usr/bin/env python3
"""Verify the M31 canonical-masked Pade global route-cut certificate.

The deployed part is an exact arithmetic/source-interface route cut.  The
finite-field construction is a toy universal-implication falsifier, not an
M31 received-word counterexample and not a ledger payment.  The verifier is
standard-library only and uses explicit exceptions under both normal and
``python -O`` execution.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Sequence


SCHEMA_ID = "rs-mca-m31-canonical-masked-pade-global-route-cut-v1"
ARCHITECTURE_ID = "M31_CANONICAL_MASKED_PADE_GLOBAL_ROUTE_CUT_V1"
STATUS = "PROVED_DEPLOYED_SYMBOLIC_BRIDGE_TOY_COALESCENCE_ROUTE_CUT_ROW_OPEN"

# Deployed M31 arithmetic inherited from the source adapter.
M31_BUDGET = 16_777_215
M31_FORBIDDEN = 16_777_216
M31_FORCED_KEYS = 259_881
M31_SAFE_ALLOWANCE = 259_880
M31_RANK3_DEGREE = 62_295
M31_MAX_INDEPENDENT_RANK3_UNIONS = 4
M31_FOUR_UNION_MASS = 249_180
M31_REMAINDER = 10_700
M31_COUPLED_SIGMA = 913_681
M31_HYPERPLANE_FORMS = 128_589_177_894_085_853_184
M31_TWO_TO_67 = 147_573_952_589_676_412_928
M31_TWO_TO_68 = 295_147_905_179_352_825_856
M31_QUARTIC_FIELD_SIZE = 21_267_647_892_944_572_736_998_860_269_687_930_881
M31_HYPERPLANE_MARGIN_TO_TWO_TO_67 = 18_984_774_695_590_559_744

# Exact toy fixture.
P = 17
K = 7
N = 14
J = 6
RADIUS = 6
AGREEMENT = 8
D0 = 1
SIGMA = 4
MOMENTS = (4, 0, 1, 3, 4, 10, 8)
DOMAIN = tuple(range(N))
EXPECTED_RECEIVED = (4, 3, 11, 5, 13, 6, 9, 0, 0, 0, 0, 0, 0, 0)
ANCHOR_COUNT = 45
PACKET_WIDTH = 46

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_canonical_masked_pade_global_route_cut_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_canonical_masked_pade_global_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json"

SOURCE_SPECS = (
    ("route_cut_schema", SCHEMA_PATH, None,
     "Strict JSON schema for this route-cut certificate."),
    ("route_cut_verifier", VERIFIER_PATH, None,
     "Primary standard-library exact enumerator, source gate, and mutation suite."),
    ("route_cut_sage", SAGE_PATH, None,
     "Independent Sage finite-field, codeword, coupled-rank, and packing replay."),
    ("route_cut_note", NOTE_PATH, None,
     "Symbolic scope and implication boundary for the canonical-masked global route cut."),
    ("route_cut_readme", README_PATH, None,
     "Certificate replay and nonclaim contract."),
    ("source_adapter_note",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Deployed exact-layer adapter, occupancy identity, and null-atom authority."),
    ("source_adapter_verifier",
     ROOT / "experimental/scripts/verify_m31_list_v4_source_adapter_v1.py",
     None, "Exact deployed adapter arithmetic and five-atom chronology replay."),
    ("source_adapter_manifest",
     ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
     "payload_sha256", "Sealed deployed adapter contract and source registry."),
    ("coupled_source_note",
     ROOT / "experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md",
     None, "Field-generic coupled row, pair-minor collision factor, and joint-index source."),
    ("coupled_source_verifier",
     ROOT / "experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py",
     None, "Exact coupled theorem arithmetic and predecessor finite-field controls."),
    ("coupled_source_manifest",
     ROOT / "experimental/data/certificates/m31-coupled-escape-forney-plucker-route-cut/manifest.json",
     None, "Coupled theorem scope and source registry (byte-hash bound)."),
    ("full_layer_source",
     ROOT / "experimental/notes/thresholds/m31_full_packet_pade_forney_source.md",
     None, "Exact-support, full-layer, escape, and Pade source theorem."),
    ("rank46_source",
     ROOT / "experimental/notes/thresholds/m31_canonical_popov_rank46_compiler.md",
     None, "Sharp deployed occupancy extremizer and four-versus-five arithmetic route cut."),
    ("rank46_verifier",
     ROOT / "experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py",
     None, "Exact deployed occupancy optimizer and rank-46 arithmetic replay."),
    ("active_v4_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active five-atom LIST chronology and payment semantics."),
)


class VerificationError(RuntimeError):
    """Fail-closed certificate or exact-model error."""


CHECKS = 0


def require(value: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not value:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("payload is not canonical-JSON serializable") from exc
    return (text + "\n").encode("ascii")


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON is forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN and infinity are forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_json_bytes(raw: bytes) -> Any:
    require(len(raw) <= 64 * 1024 * 1024, "JSON byte-size bound")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    return json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_int=int,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )


def strict_json_path(path: Path, *, canonical: bool = False) -> Any:
    value = strict_json_bytes(path.read_bytes())
    if canonical:
        require(path.read_bytes() == canonical_json(value), f"canonical JSON bytes: {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


# --- Exact prime-field polynomial arithmetic, coefficients low to high. ---


def inv(a: int) -> int:
    require(a % P != 0, "division by zero")
    return pow(a % P, P - 2, P)


def trim(f: Sequence[int]) -> tuple[int, ...]:
    out = [value % P for value in f]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_add(
    f: tuple[int, ...], g: tuple[int, ...], scale: int = 1,
) -> tuple[int, ...]:
    out = [0] * max(len(f), len(g))
    for index, value in enumerate(f):
        out[index] += value
    for index, value in enumerate(g):
        out[index] += scale * value
    return trim(out)


def poly_mul(f: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(f) + len(g) - 1)
    for left, x in enumerate(f):
        for right, y in enumerate(g):
            out[left + right] = (out[left + right] + x * y) % P
    return trim(out)


def poly_divmod(
    numerator: tuple[int, ...], denominator: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(denominator != (0,), "zero polynomial divisor")
    remainder = list(numerator)
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    lead_inverse = inv(denominator[-1])
    while len(remainder) >= len(denominator) and any(remainder):
        shift = len(remainder) - len(denominator)
        scalar = remainder[-1] * lead_inverse % P
        quotient[shift] = scalar
        for index, value in enumerate(denominator):
            remainder[index + shift] = (remainder[index + shift] - scalar * value) % P
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return trim(quotient), trim(remainder)


def poly_gcd(f: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    while g != (0,):
        _, remainder = poly_divmod(f, g)
        f, g = g, remainder
    scalar = inv(f[-1])
    return trim(tuple(scalar * value for value in f))


def locator(points: Sequence[int]) -> tuple[int, ...]:
    out = (1,)
    for point in points:
        out = poly_mul(out, ((-point) % P, 1))
    return out


def divide_linear(f: tuple[int, ...], point: int) -> tuple[int, ...]:
    quotient = [0] * (len(f) - 1)
    quotient[-1] = f[-1]
    for index in range(len(quotient) - 2, -1, -1):
        quotient[index] = (f[index + 1] + point * quotient[index + 1]) % P
    require((f[0] + point * quotient[0]) % P == 0, "inexact linear division")
    return trim(quotient)


def evaluate(f: tuple[int, ...], point: int) -> int:
    return sum(value * pow(point, index, P) for index, value in enumerate(f)) % P


def derivative_value(f: tuple[int, ...], point: int) -> int:
    return sum(
        index * f[index] * pow(point, index - 1, P)
        for index in range(1, len(f))
    ) % P


def functional(f: tuple[int, ...]) -> int:
    require(len(f) <= K, "functional moment range")
    return sum(value * MOMENTS[index] for index, value in enumerate(f)) % P


def divided_numerator(f: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(f)
    for degree in range(1, len(f)):
        for output_degree in range(degree):
            moment = MOMENTS[degree - 1 - output_degree]
            out[output_degree] = (
                out[output_degree] + f[degree] * moment
            ) % P
    return trim(out)


def exact_support(points: tuple[int, ...]) -> bool:
    polynomial = locator(points)
    containment = all(
        functional(trim((0,) * shift + polynomial)) == 0
        for shift in range(K - len(points))
    )
    return containment and all(
        functional(divide_linear(polynomial, point)) != 0 for point in points
    )


def matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    require(bool(rows), "empty matrix")
    matrix = [[value % P for value in row] for row in rows]
    require(all(len(row) == len(matrix[0]) for row in matrix), "ragged matrix")
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scalar = inv(matrix[rank][column])
        matrix[rank] = [(scalar * value) % P for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                (left - scalar * right) % P
                for left, right in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def solve_square(matrix: list[list[int]], target: list[int]) -> tuple[int, ...]:
    require(len(matrix) == len(target), "square solve height")
    require(all(len(row) == len(matrix) for row in matrix), "square solve width")
    rows = [row[:] + [target[index] % P] for index, row in enumerate(matrix)]
    for column in range(len(rows)):
        pivot = next(
            (row for row in range(column, len(rows)) if rows[row][column]),
            None,
        )
        require(pivot is not None, "singular solve chart")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scalar = inv(rows[column][column])
        rows[column] = [(scalar * value) % P for value in rows[column]]
        for row in range(len(rows)):
            if row == column:
                continue
            scalar = rows[row][column]
            rows[row] = [
                (left - scalar * right) % P
                for left, right in zip(rows[row], rows[column], strict=True)
            ]
    return tuple(row[-1] for row in rows)


def lagrange(points: Sequence[tuple[int, int]]) -> tuple[int, ...]:
    answer = (0,)
    for index, (x_value, y_value) in enumerate(points):
        basis = (1,)
        denominator = 1
        for other, (z_value, _) in enumerate(points):
            if index == other:
                continue
            basis = poly_mul(basis, ((-z_value) % P, 1))
            denominator = denominator * (x_value - z_value) % P
        answer = poly_add(answer, basis, y_value * inv(denominator))
    return answer


def support_order_key(points: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(1 if point in points else 0 for point in DOMAIN)


def shifted(f: tuple[int, ...], amount: int) -> tuple[int, ...]:
    require(amount >= 0, "nonnegative polynomial shift")
    return trim((0,) * amount + f)


def exact_support_at_weight(points: tuple[int, ...], weight: int) -> bool:
    require(len(points) == weight < K, "exact-support weight range")
    polynomial = locator(points)
    return all(
        functional(shifted(polynomial, degree)) == 0
        for degree in range(K - weight)
    ) and all(
        functional(divide_linear(polynomial, point)) != 0 for point in points
    )


def joint_relation_matrix(
    first_row: Sequence[tuple[int, ...]],
    second_row: Sequence[tuple[int, ...]],
    multiplier_width: int,
) -> list[list[int]]:
    require(len(first_row) == len(second_row) >= 2, "joint-kernel row width")
    require(multiplier_width >= 1, "positive multiplier width")
    output_length = max(
        max(len(polynomial) for polynomial in first_row),
        max(len(polynomial) for polynomial in second_row),
    ) + multiplier_width - 1
    equations: list[list[int]] = []
    for polynomial_row in (first_row, second_row):
        for output_degree in range(output_length):
            equation: list[int] = []
            for polynomial in polynomial_row:
                for shift in range(multiplier_width):
                    source_degree = output_degree - shift
                    equation.append(
                        polynomial[source_degree]
                        if 0 <= source_degree < len(polynomial) else 0
                    )
            equations.append(equation)
    return equations


def joint_kernel_nullity(
    first_row: Sequence[tuple[int, ...]],
    second_row: Sequence[tuple[int, ...]],
    multiplier_width: int,
) -> int:
    equations = joint_relation_matrix(first_row, second_row, multiplier_width)
    return len(first_row) * multiplier_width - matrix_rank(equations)


def build_masked_bridge_fixture(received: tuple[int, ...]) -> dict[str, Any]:
    """Check the load-bearing bridge on exact codewords with Q != 1."""
    interior_weight = 5
    exact_interior = tuple(
        support for support in itertools.combinations(DOMAIN, interior_weight)
        if exact_support_at_weight(support, interior_weight)
    )
    require(exact_interior == (
        (0, 3, 5, 8, 12),
        (0, 4, 10, 11, 13),
        (1, 2, 5, 6, 13),
        (1, 4, 7, 11, 12),
    ), "complete nontrivial-padding exact layer")

    domain_locator = locator(DOMAIN)
    received_polynomial = lagrange(tuple(
        (point, received[point]) for point in DOMAIN
    ))
    gamma = P - 1
    require(gamma == 16, "dual-weight collision scalar")

    records: list[dict[str, Any]] = []
    canonical_locators: list[tuple[int, ...]] = []
    canonical_numerators: list[tuple[int, ...]] = []
    interpolation_numerators: list[tuple[int, ...]] = []
    error_locators: list[tuple[int, ...]] = []
    padding_locators: list[tuple[int, ...]] = []
    error_numerators: list[tuple[int, ...]] = []

    for support in exact_interior:
        agreements = tuple(point for point in DOMAIN if point not in support)
        selected_agreements = agreements[:AGREEMENT]
        discarded_agreements = agreements[AGREEMENT:]
        require(len(discarded_agreements) == RADIUS - interior_weight == 1,
                "nontrivial padding degree")

        L = locator(support)
        Q = locator(discarded_agreements)
        W = poly_mul(L, Q)
        B_L = divided_numerator(L)
        B_W = divided_numerator(W)
        require(Q != (1,), "padding fixture is nontrivial")
        require(B_W == poly_mul(Q, B_L), "B(LQ)=Q B(L)")
        require(poly_gcd(W, B_W) == Q, "gcd(W,B(W)) recovers Q")
        recovered_L, remainder = poly_divmod(W, poly_gcd(W, B_W))
        require(remainder == (0,) and recovered_L == L,
                "saturation quotient recovers actual locator")

        outside = tuple(point for point in DOMAIN if point not in support)
        codeword = lagrange(tuple(
            (point, received[point]) for point in outside[:K]
        ))
        require(all(evaluate(codeword, point) == received[point] for point in outside),
                "interior codeword agreement")
        domain_over_W, remainder = poly_divmod(domain_locator, W)
        require(remainder == (0,), "canonical locator divides domain locator")
        correction = poly_mul(domain_over_W, B_W)
        reconstructed_codeword = poly_add(
            received_polynomial, correction, inv(gamma)
        )
        require(reconstructed_codeword == codeword,
                "c=Y+gamma^-1(Lambda_D/W)B(W)")

        interpolation_numerator = poly_mul(codeword, W)
        transformed_numerator = poly_add(
            poly_mul(received_polynomial, W),
            poly_mul(domain_locator, B_W),
            inv(gamma),
        )
        require(interpolation_numerator == transformed_numerator,
                "N=YW+gamma^-1 Lambda_D B(W)")

        error_locators.append(L)
        padding_locators.append(Q)
        canonical_locators.append(W)
        error_numerators.append(B_L)
        canonical_numerators.append(B_W)
        interpolation_numerators.append(interpolation_numerator)
        records.append({
            "support": list(support),
            "selected_agreements": list(selected_agreements),
            "discarded_agreements": list(discarded_agreements),
            "L_coefficients": list(L),
            "Q_coefficients": list(Q),
            "W_coefficients": list(W),
            "B_L_coefficients": list(B_L),
            "B_W_coefficients": list(B_W),
            "codeword_coefficients": list(codeword),
            "interpolation_numerator_coefficients": list(interpolation_numerator),
        })

    canonical_pair_factor_checks = 0
    for left, right in itertools.combinations(range(len(records)), 2):
        omega_canonical = poly_add(
            poly_mul(canonical_locators[left], canonical_numerators[right]),
            poly_mul(canonical_locators[right], canonical_numerators[left]),
            -1,
        )
        omega_error = poly_add(
            poly_mul(error_locators[left], error_numerators[right]),
            poly_mul(error_locators[right], error_numerators[left]),
            -1,
        )
        require(
            omega_canonical == poly_mul(
                poly_mul(padding_locators[left], padding_locators[right]),
                omega_error,
            ),
            "canonical pair minor retains both padding factors",
        )
        canonical_pair_factor_checks += 1
    require(canonical_pair_factor_checks == 6, "canonical pair-factor check count")

    kernel_dimensions: list[dict[str, int]] = []
    saturated_error_locators = [
        poly_mul(error_locators[index], padding_locators[index])
        for index in range(len(error_locators))
    ]
    saturated_error_numerators = [
        poly_mul(error_numerators[index], padding_locators[index])
        for index in range(len(error_numerators))
    ]
    require(saturated_error_locators == canonical_locators
            and saturated_error_numerators == canonical_numerators,
            "diagonal padding gives the canonical masked row")
    for width in range(1, 7):
        masked_matrix = joint_relation_matrix(
            canonical_locators, canonical_numerators, width)
        saturated_matrix = joint_relation_matrix(
            saturated_error_locators, saturated_error_numerators, width)
        require(masked_matrix == saturated_matrix,
                "diagonal-saturation relation conditions")
        interpolation_matrix = joint_relation_matrix(
            canonical_locators, interpolation_numerators, width)
        masked_rank = matrix_rank(masked_matrix)
        interpolation_rank = matrix_rank(interpolation_matrix)
        combined_rank = matrix_rank(masked_matrix + interpolation_matrix)
        masked_nullity = len(canonical_locators) * width - masked_rank
        interpolation_nullity = (
            len(canonical_locators) * width - interpolation_rank
        )
        require(masked_nullity == interpolation_nullity,
                "right-kernel conditions agree at every checked width")
        require(masked_rank == interpolation_rank == combined_rank,
                "masked and interpolation right-kernel subspaces agree")
        kernel_dimensions.append({
            "multiplier_width": width,
            "masked_pair_nullity": masked_nullity,
            "interpolation_pair_nullity": interpolation_nullity,
            "combined_relation_rank": combined_rank,
        })
    require(
        [entry["masked_pair_nullity"] for entry in kernel_dimensions]
        == [0, 2, 4, 6, 8, 10],
        "nontrivial-padding kernel profile",
    )

    return {
        "fixed_depth_product_identity": "B(LQ)=Q*B(L)",
        "saturation_identity": "gcd(W,B(W))=Q and W/gcd(W,B(W))=L",
        "diagonal_saturation_identity":
            "ker(H_W)=Delta_Q^-1*ker(H_L) intersect GF(17)[X]^M",
        "codeword_reconstruction_identity":
            "c=Y+gamma^-1*(Lambda_D/W)*B(W)",
        "interpolation_transform_identity":
            "N=Y*W+gamma^-1*Lambda_D*B(W)",
        "right_kernel_identity": "ker(W,B(W))=ker(W,N)",
        "nontrivial_padding": True,
        "interior_weight": interior_weight,
        "padding_degree": 1,
        "gamma": gamma,
        "received_polynomial_coefficients": list(received_polynomial),
        "domain_locator_coefficients": list(domain_locator),
        "complete_interior_exact_layer_size": len(exact_interior),
        "records": records,
        "canonical_pair_factor_checks": canonical_pair_factor_checks,
        "kernel_dimension_replay": kernel_dimensions,
        "all_identities_verified": True,
    }


def exact_set_packing(masks: Sequence[int]) -> tuple[int, tuple[int, ...]]:
    states: dict[int, tuple[int, tuple[int, ...]]] = {0: (0, ())}
    for index, mask in enumerate(masks):
        require(mask != 0, "empty collision union is excluded from packing")
        for used, (count, chosen) in list(states.items()):
            if used & mask:
                continue
            combined = used | mask
            candidate = (count + 1, chosen + (index,))
            if combined not in states or candidate[0] > states[combined][0]:
                states[combined] = candidate
    return max(states.values())


def exact_root_transversals(
    masks: Sequence[int], universe_size: int
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    require(universe_size >= 0, "nonnegative transversal universe size")
    require(all(0 < mask < (1 << universe_size) for mask in masks),
            "nonempty collision masks lie in transversal universe")
    for size in range(universe_size + 1):
        witnesses: list[tuple[int, ...]] = []
        for points in itertools.combinations(range(universe_size), size):
            candidate = sum(1 << point for point in points)
            if all(candidate & mask for mask in masks):
                witnesses.append(points)
        if witnesses:
            return size, tuple(witnesses)
    raise VerificationError("finite nonempty-mask family has no root transversal")


def build_toy_model() -> dict[str, Any]:
    require((N, K, J, RADIUS, AGREEMENT, D0, SIGMA) == (14, 7, 6, 6, 8, 1, 4),
            "toy parameter contract")
    require(N == 2 * K and AGREEMENT == N - RADIUS, "toy RS geometry")
    require(D0 == K - J == AGREEMENT - K, "toy cutoff identities")
    require(SIGMA == 2 * J - K - 1, "toy coupled excess")

    domain_locator = locator(DOMAIN)
    dual_weights = tuple(
        inv(derivative_value(domain_locator, point)) for point in DOMAIN
    )
    moment_chart = [
        [dual_weights[column] * pow(DOMAIN[column], row, P) % P
         for column in range(K)]
        for row in range(K)
    ]
    first_values = solve_square(moment_chart, list(MOMENTS))
    received = first_values + (0,) * (N - K)
    require(received == EXPECTED_RECEIVED, "received-word witness")
    for degree in range(K):
        realized = sum(
            received[column] * dual_weights[column]
            * pow(DOMAIN[column], degree, P)
            for column in range(N)
        ) % P
        require(realized == MOMENTS[degree], "received word realizes functional")

    all_supports = tuple(itertools.combinations(DOMAIN, J))
    require(len(all_supports) == 3_003, "exhaustive support universe")
    ordered_layer = tuple(sorted(
        (support for support in all_supports if exact_support(support)),
        key=support_order_key,
    ))
    require(len(ordered_layer) == 137, "complete exact layer size")
    core = set(ordered_layer[0])
    for support in ordered_layer[1:]:
        core.intersection_update(support)
    require(not core, "complete exact layer common core")

    locators = {support: locator(support) for support in ordered_layer}
    numerators = {
        support: divided_numerator(locators[support]) for support in ordered_layer
    }
    codewords: dict[tuple[int, ...], tuple[int, ...]] = {}
    for support in ordered_layer:
        outside = tuple(point for point in DOMAIN if point not in support)
        require(len(outside) == K + 1, "agreement set size")
        codeword = lagrange(tuple((point, received[point]) for point in outside[:K]))
        require(len(codeword) <= K, "codeword degree")
        require(all(evaluate(codeword, point) == received[point] for point in outside),
                "all outside points agree")
        require(all(evaluate(codeword, point) != received[point] for point in support),
                "all support errors are nonzero")
        codewords[support] = codeword
    require(len(set(codewords.values())) == len(ordered_layer),
            "distinct exact supports retain distinct codewords")

    anchors = ordered_layer[:ANCHOR_COUNT]
    extras = ordered_layer[ANCHOR_COUNT:]
    require(len(anchors) == 45 and len(extras) == 92, "canonical anchor/key split")

    key_collision_unions: list[dict[str, Any]] = []
    collision_masks: list[int] = []
    constant_nullities: list[int] = []
    polynomial_pair_checks = 0
    collision_point_checks = 0
    factor_checks = 0

    for extra_index, extra in enumerate(extras):
        packet = anchors + (extra,)
        coefficient_rows: list[list[int]] = []
        for degree in range(J + 1):
            coefficient_rows.append([
                locators[support][degree] for support in packet
            ])
        for degree in range(J):
            coefficient_rows.append([
                numerators[support][degree]
                if degree < len(numerators[support]) else 0
                for support in packet
            ])
        nullity = PACKET_WIDTH - matrix_rank(coefficient_rows)
        require(nullity >= 3, "three degree-zero coupled rows on every key")
        constant_nullities.append(nullity)

        for left, right in itertools.combinations(packet, 2):
            omega = poly_add(
                poly_mul(locators[left], numerators[right]),
                poly_mul(locators[right], numerators[left]),
                -1,
            )
            require(omega != (0,), "every pair minor is nonzero")
            polynomial_pair_checks += 1

        mask = 0
        for anchor in anchors:
            P_anchor = locators[anchor]
            P_extra = locators[extra]
            B_anchor = numerators[anchor]
            B_extra = numerators[extra]
            overlap = poly_gcd(P_anchor, P_extra)
            omega = poly_add(
                poly_mul(P_anchor, B_extra),
                poly_mul(P_extra, B_anchor),
                -1,
            )
            quotient, remainder = poly_divmod(omega, overlap)
            require(remainder == (0,) and quotient != (0,),
                    "pair-minor overlap quotient")
            require(len(quotient) - 1 <= SIGMA - (len(overlap) - 1),
                    "pair collision-factor degree cap")
            factor_checks += 1
            for point in set(anchor).intersection(extra):
                rho_anchor = (
                    evaluate(B_anchor, point)
                    * inv(derivative_value(P_anchor, point))
                ) % P
                rho_extra = (
                    evaluate(B_extra, point)
                    * inv(derivative_value(P_extra, point))
                ) % P
                normalized_collision = rho_anchor == rho_extra
                actual_collision = (
                    evaluate(codewords[anchor], point)
                    == evaluate(codewords[extra], point)
                )
                require(normalized_collision == actual_collision,
                        "normalized escape equals actual codeword collision")
                require((evaluate(quotient, point) == 0) == actual_collision,
                        "collision-factor root equals actual codeword collision")
                if actual_collision:
                    mask |= 1 << point
                collision_point_checks += 1
        roots = tuple(point for point in DOMAIN if mask & (1 << point))
        require(bool(roots), "every fixture key has a nonempty natural collision union")
        collision_masks.append(mask)
        key_collision_unions.append({
            "extra_index_one_based": extra_index + 1,
            "global_index_one_based": ANCHOR_COUNT + extra_index + 1,
            "support": list(extra),
            "collision_roots": list(roots),
        })

    require(polynomial_pair_checks == 92 * 1_035 == 95_220,
            "all key pair-minor check count")
    require(factor_checks == 92 * 45 == 4_140, "anchor-extra factor check count")
    require(collision_point_checks == 9_914, "common-point collision check count")
    require(min(constant_nullities) == 40, "minimum constant joint-kernel nullity")

    optimum, witness_indices = exact_set_packing(collision_masks)
    require(optimum == 5, "exact disjoint collision-union optimum")
    witness_masks = tuple(collision_masks[index] for index in witness_indices)
    require(all(
        left & right == 0 for left, right in itertools.combinations(witness_masks, 2)
    ), "five witness unions are pairwise disjoint")
    witness = [key_collision_unions[index] for index in witness_indices]
    require(
        [entry["extra_index_one_based"] for entry in witness] == [48, 62, 67, 77, 80],
        "canonical five-union witness indices",
    )

    transversal_minimum, minimum_transversals = exact_root_transversals(
        collision_masks, N
    )
    require(transversal_minimum == 6, "exact root-transversal minimum")
    require(minimum_transversals == (
        (3, 5, 6, 7, 8, 9),
        (3, 5, 7, 8, 9, 13),
        (3, 6, 7, 8, 9, 12),
        (6, 7, 8, 9, 11, 12),
    ), "complete canonical minimum root-transversal list")

    layer_serial = ";".join(",".join(map(str, support)) for support in ordered_layer)
    collision_serial = ";".join(
        f"{','.join(map(str, support))}:{mask}"
        for support, mask in zip(extras, collision_masks, strict=True)
    )
    nullity_histogram = {
        str(value): constant_nullities.count(value)
        for value in sorted(set(constant_nullities))
    }
    collision_size_histogram = {
        str(size): sum(mask.bit_count() == size for mask in collision_masks)
        for size in sorted({mask.bit_count() for mask in collision_masks})
    }

    return {
        "canonical_masked_bridge": build_masked_bridge_fixture(received),
        "toy_parameters": {
            "field": "GF(17)",
            "prime": P,
            "domain": list(DOMAIN),
            "n": N,
            "K": K,
            "radius": RADIUS,
            "agreement": AGREEMENT,
            "weight": J,
            "D0": D0,
            "sigma": SIGMA,
            "moments": list(MOMENTS),
            "functional_formula": "4*q0+q2+3*q3+4*q4+10*q5+8*q6 mod 17",
            "received_word": list(received),
            "dual_weight_normalization": "u_x=1/L_D'(x)",
        },
        "exact_source": {
            "support_universe_size": len(all_supports),
            "support_order": "ASCENDING_LEX_INCIDENCE_VECTOR_0_BEFORE_1",
            "ordered_exact_supports": [list(support) for support in ordered_layer],
            "ordered_layer_sha256": sha256_bytes(layer_serial.encode("ascii")),
            "full_layer_complete": True,
            "full_layer_size": len(ordered_layer),
            "common_core": [],
            "distinct_codewords": len(set(codewords.values())),
            "same_received_word": True,
            "containment_equations_per_support": K - J,
            "all_one_point_escapes_nonzero": True,
        },
        "coupled_keys": {
            "anchor_count": len(anchors),
            "marked_key_count": len(extras),
            "packet_width": PACKET_WIDTH,
            "key_collision_unions": key_collision_unions,
            "collision_table_sha256": sha256_bytes(collision_serial.encode("ascii")),
            "each_key_polynomial_row_rank": 2,
            "all_pair_minors_nonzero": True,
            "pair_minor_checks": polynomial_pair_checks,
            "anchor_extra_factor_checks": factor_checks,
            "common_point_collision_checks": collision_point_checks,
            "minimum_constant_joint_kernel_nullity": min(constant_nullities),
            "constant_joint_kernel_nullity_histogram": nullity_histogram,
            "every_key_has_at_least_three_degree_zero_rows": True,
            "collision_union_size_histogram": collision_size_histogram,
        },
        "noncoalescence": {
            "collision_union_definition": (
                "J(E*)={x in E*: exists canonical anchor E_i containing x "
                "with c_Ei(x)=c_E*(x)}"
            ),
            "exact_set_packing_universe_size": N,
            "exact_disjoint_nonempty_union_optimum": optimum,
            "five_union_witness": witness,
            "witness_pairwise_disjoint": True,
            "exact_root_transversal_minimum": transversal_minimum,
            "minimum_root_transversals": [
                list(points) for points in minimum_transversals
            ],
            "no_four_point_root_transversal": True,
        },
    }


def expected_source_bindings() -> list[dict[str, Any]]:
    bindings: list[dict[str, Any]] = []
    for role, path, internal_key, scope in SOURCE_SPECS:
        require(path.exists() and path.is_file(), f"source exists: {path}")
        try:
            relative = str(path.relative_to(ROOT))
        except ValueError as exc:
            raise VerificationError(f"source outside repository: {path}") from exc
        pure = PurePosixPath(relative)
        require(not pure.is_absolute() and ".." not in pure.parts, "safe source path")
        internal: str | None = None
        if internal_key is not None:
            source_json = strict_json_path(path, canonical=True)
            require(type(source_json) is dict, "bound source manifest object")
            internal = source_json.get(internal_key)
            require(type(internal) is str and len(internal) == 64,
                    "bound source internal payload hash")
        bindings.append({
            "binding_id": f"M31_CANONICAL_MASKED_PADE::{role}",
            "role": role,
            "path": relative,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
            "scope": scope,
        })
    return bindings


def build_payload() -> dict[str, Any]:
    model = build_toy_model()
    hyperplane_forms = (
        M31_FORBIDDEN * 981_129
        + (M31_FORBIDDEN * (M31_FORBIDDEN - 1) // 2) * M31_COUPLED_SIGMA
    )
    require(hyperplane_forms == M31_HYPERPLANE_FORMS,
            "deployed selected-support hyperplane form count")
    require(M31_HYPERPLANE_FORMS < M31_TWO_TO_68 < M31_QUARTIC_FIELD_SIZE,
            "deployed target-field hyperplane inequalities")
    require(M31_HYPERPLANE_FORMS < M31_TWO_TO_67 < M31_TWO_TO_68,
            "strong deployed target-field hyperplane inequalities")
    require(M31_TWO_TO_67 - M31_HYPERPLANE_FORMS
            == M31_HYPERPLANE_MARGIN_TO_TWO_TO_67,
            "hyperplane margin below 2^67")
    return {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "scope": {
            "workboard_item": "M1",
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "impact": "ROUTE_CUT",
            "deployed_symbolic_bridge_proved": True,
            "toy_falsifier_scale": True,
            "deployed_row_closed": False,
            "ledger_movement": 0,
            "is_m31_counterexample": False,
        },
        "deployed_context": {
            "B_star": M31_BUDGET,
            "forbidden_size": M31_FORBIDDEN,
            "forced_marked_keys": M31_FORCED_KEYS,
            "safe_signed_allowance": M31_SAFE_ALLOWANCE,
            "local_rank3_degree": M31_RANK3_DEGREE,
            "independent_rank3_unions_fitting_allowance": M31_MAX_INDEPENDENT_RANK3_UNIONS,
            "four_union_mass": M31_FOUR_UNION_MASS,
            "remainder_after_four": M31_REMAINDER,
            "all_high_atoms_remain_null": True,
            "coupled_sigma": M31_COUPLED_SIGMA,
            "selected_support_count": M31_FORBIDDEN,
            "escape_and_collision_form_upper": M31_HYPERPLANE_FORMS,
            "two_to_67": M31_TWO_TO_67,
            "two_to_68": M31_TWO_TO_68,
            "margin_below_two_to_67": M31_HYPERPLANE_MARGIN_TO_TWO_TO_67,
            "quartic_field_cardinality": M31_QUARTIC_FIELD_SIZE,
            "form_upper_below_two_to_67_below_field": True,
            "hyperplane_dichotomy_is_conditional": True,
            "proper_form_branch": (
                "one functional in the common containment space preserves every selected "
                "support and escape while avoiding every selected common-error collision"
            ),
            "extra_full_list_supports_may_appear": True,
            "hyperplane_branch_is_row_counterexample_or_payment": False,
        },
        **model,
        "route_cut": {
            "falsified_parameter_uniform_implication": (
                "parameter-uniform implication: complete exact same-weight layer for "
                "one received word plus canonical "
                "45 shared anchors, exact escapes, MDS separation, a rank-two coupled "
                "row with at least three low joint relations, and the pair-minor actual-"
                "collision factor identity forces either the intersection matching "
                "number of the natural anchor-extra actual collision-root unions to be "
                "at most four or those unions to admit a root transversal of size at "
                "most four"
            ),
            "falsifier": (
                "natural collision-root unions have exact disjoint packing optimum five "
                "and exact root-transversal minimum six"
            ),
            "does_not_falsify": (
                "an M31-specific theorem using the deployed p,n,K, cross-weight "
                "chronology, canonical padding, or another global invariant"
            ),
            "required_next_input": (
                "M31-domain or cross-weight incidence/coalescence, a chronology-correct "
                "owner/refund theorem, M31-specific primitive elimination, or a direct "
                "distinguished-codeword projection cap"
            ),
            "payment_status": "NONE",
            "deployed_terminal": "UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND",
        },
        "source_bindings": expected_source_bindings(),
    }


def exact_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"{label}: exact keys")


def verify_payload(payload: dict[str, Any], *, reference_model: dict[str, Any] | None = None) -> None:
    exact_keys(payload, {
        "schema", "architecture_id", "status", "payload_sha256", "scope",
        "deployed_context", "canonical_masked_bridge", "toy_parameters",
        "exact_source", "coupled_keys", "noncoalescence", "route_cut",
        "source_bindings",
    }, "payload")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["architecture_id"] == ARCHITECTURE_ID, "architecture id")
    require(payload["status"] == STATUS, "status")
    require(payload["payload_sha256"] == payload_sha256(payload), "payload seal")

    require(payload["scope"] == {
        "workboard_item": "M1",
        "row": "Mersenne-31 list at 2^-100",
        "object": "LIST",
        "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
        "impact": "ROUTE_CUT",
        "deployed_symbolic_bridge_proved": True,
        "toy_falsifier_scale": True,
        "deployed_row_closed": False,
        "ledger_movement": 0,
        "is_m31_counterexample": False,
    }, "scope contract")
    require(payload["deployed_context"] == {
        "B_star": 16_777_215,
        "forbidden_size": 16_777_216,
        "forced_marked_keys": 259_881,
        "safe_signed_allowance": 259_880,
        "local_rank3_degree": 62_295,
        "independent_rank3_unions_fitting_allowance": 4,
        "four_union_mass": 249_180,
        "remainder_after_four": 10_700,
        "all_high_atoms_remain_null": True,
        "coupled_sigma": 913_681,
        "selected_support_count": 16_777_216,
        "escape_and_collision_form_upper": 128_589_177_894_085_853_184,
        "two_to_67": 147_573_952_589_676_412_928,
        "two_to_68": 295_147_905_179_352_825_856,
        "margin_below_two_to_67": 18_984_774_695_590_559_744,
        "quartic_field_cardinality": 21_267_647_892_944_572_736_998_860_269_687_930_881,
        "form_upper_below_two_to_67_below_field": True,
        "hyperplane_dichotomy_is_conditional": True,
        "proper_form_branch": (
            "one functional in the common containment space preserves every selected "
            "support and escape while avoiding every selected common-error collision"
        ),
        "extra_full_list_supports_may_appear": True,
        "hyperplane_branch_is_row_counterexample_or_payment": False,
    }, "deployed route-cut arithmetic")

    if reference_model is None:
        reference_model = build_toy_model()
    for section in (
        "canonical_masked_bridge", "toy_parameters", "exact_source",
        "coupled_keys", "noncoalescence",
    ):
        require(payload[section] == reference_model[section], f"exact toy section: {section}")

    route = payload["route_cut"]
    exact_keys(route, {
        "falsified_parameter_uniform_implication", "falsifier", "does_not_falsify",
        "required_next_input", "payment_status", "deployed_terminal",
    }, "route cut")
    require(route["falsifier"] == (
                "natural collision-root unions have exact disjoint packing optimum five "
                "and exact root-transversal minimum six"
            ),
            "route-cut falsifier")
    require(route["payment_status"] == "NONE", "no toy payment")
    require(route["deployed_terminal"] ==
            "UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND",
            "deployed residual remains open")
    require("parameter-uniform" in route["falsified_parameter_uniform_implication"],
            "route-cut scope remains parameter-uniform")
    require("M31-specific" in route["does_not_falsify"], "M31 nonclaim")

    require(payload["source_bindings"] == expected_source_bindings(),
            "exact live source bindings")


def mutate_path(payload: dict[str, Any], path: Sequence[Any], replacement: Any) -> None:
    cursor: Any = payload
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def tamper_selftest(expected: dict[str, Any], model: dict[str, Any]) -> None:
    mutations: tuple[tuple[str, Sequence[Any], Any], ...] = (
        ("deployed-symbolic-bridge", ("scope", "deployed_symbolic_bridge_proved"), False),
        ("toy-falsifier-scale", ("scope", "toy_falsifier_scale"), False),
        ("m31-counterexample", ("scope", "is_m31_counterexample"), True),
        ("ledger-payment", ("scope", "ledger_movement"), 1),
        ("four-union-cap", ("deployed_context", "independent_rank3_unions_fitting_allowance"), 5),
        ("hyperplane-count", ("deployed_context", "escape_and_collision_form_upper"),
         128_589_177_894_085_853_183),
        ("hyperplane-conditional", ("deployed_context", "hyperplane_dichotomy_is_conditional"),
         False),
        ("hyperplane-extra-support", ("deployed_context", "extra_full_list_supports_may_appear"),
         False),
        ("hyperplane-payment", ("deployed_context", "hyperplane_branch_is_row_counterexample_or_payment"),
         True),
        ("toy-field", ("toy_parameters", "prime"), 19),
        ("drop-support", ("exact_source", "full_layer_size"), 136),
        ("support-order", ("exact_source", "support_order"), "TUPLE_LEX"),
        ("common-core", ("exact_source", "common_core"), [0]),
        ("mask-product", ("canonical_masked_bridge", "fixed_depth_product_identity"),
         "B(LQ)=B(L)"),
        ("mask-gcd", ("canonical_masked_bridge", "saturation_identity"),
         "gcd(W,B(W))=L"),
        ("diagonal-saturation", ("canonical_masked_bridge", "diagonal_saturation_identity"),
         "ker(H_W)=ker(H_L)"),
        ("mask-transform", ("canonical_masked_bridge", "interpolation_transform_identity"),
         "N=Y*W"),
        ("mask-kernel", ("canonical_masked_bridge", "right_kernel_identity"),
         "UNKNOWN"),
        ("padding-trivial", ("canonical_masked_bridge", "nontrivial_padding"), False),
        ("anchor-count", ("coupled_keys", "anchor_count"), 44),
        ("pair-minor", ("coupled_keys", "all_pair_minors_nonzero"), False),
        ("joint-nullity", ("coupled_keys", "minimum_constant_joint_kernel_nullity"), 39),
        ("packing-optimum", ("noncoalescence", "exact_disjoint_nonempty_union_optimum"), 4),
        ("witness-root", ("noncoalescence", "five_union_witness", 0, "collision_roots"), [9]),
        ("transversal-minimum", ("noncoalescence", "exact_root_transversal_minimum"), 5),
        ("transversal-witness", ("noncoalescence", "minimum_root_transversals", 0, 0), 2),
        ("four-point-transversal", ("noncoalescence", "no_four_point_root_transversal"), False),
        ("false-scope", ("route_cut", "does_not_falsify"), "nothing"),
        ("false-payment", ("route_cut", "payment_status"), "PAID"),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
    )
    rejected = 0
    for name, path, replacement in mutations:
        candidate = copy.deepcopy(expected)
        mutate_path(candidate, path, replacement)
        candidate = seal(candidate)
        try:
            verify_payload(candidate, reference_model=model)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"semantic mutation accepted: {name}")
    require(rejected == len(mutations), "all semantic mutations rejected")
    print(f"tamper_selftest=PASS rejected={rejected}/{len(mutations)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--model-check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not any((args.check, args.print_template, args.tamper_selftest, args.model_check)):
        args.check = True

    model = build_toy_model()
    if args.model_check:
        print("toy_model=PASS layer=137 anchors=45 keys=92 "
              "packing_optimum=5 transversal_minimum=6")
        if not any((args.check, args.print_template, args.tamper_selftest)):
            print(f"checks={CHECKS}")
            return

    expected = seal(build_payload())
    verify_payload(expected, reference_model=model)

    if args.check:
        require(MANIFEST_PATH.exists(), "manifest exists")
        actual = strict_json_path(MANIFEST_PATH, canonical=True)
        require(type(actual) is dict, "manifest object")
        verify_payload(actual, reference_model=model)
        require(actual == expected, "manifest equals regenerated payload")
        print("M31 canonical-masked Pade global route cut: PASS")
        print("toy source: GF(17), complete layer=137, anchors=45, keys=92")
        print("coupled: rank2 every key, pair minors=95220, min constant nullity=40")
        print("noncoalescence: packing optimum=5; root-transversal minimum=6")
        print("scope: deployed symbolic bridge PROVED; GF(17) falsifier TOY; "
              "M31 row OPEN; ledger movement=0")

    if args.tamper_selftest:
        tamper_selftest(expected, model)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))

    if not args.print_template:
        print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
