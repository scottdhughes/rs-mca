#!/usr/bin/env python3
"""Verify the full-span forced-collision route-cut packet.

The abstract statement is finite-dimensional linear algebra.  The exact
GF(17) replay shows that the ``identically forced collision'' branch need not
imply the natural packing/transversal conclusion: the complete locator family
spans the whole syndrome hyperplane, so every actual collision form is
identically zero on the common containment-functional line.  This is a
universal-implication route cut, not a deployed M31 counterexample or payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Sequence


SCHEMA_ID = "rs-mca-m31-full-span-forced-collision-route-cut-v1"
ARCHITECTURE_ID = "M31_FULL_SPAN_FORCED_COLLISION_ROUTE_CUT_V1"
STATUS = "PROVED_ANNIHILATOR_CRITERION_EXACT_FULL_SPAN_ROUTE_CUT_ROW_OPEN"

P = 17
K = 7
N = 14
J = 6
RADIUS = 6
AGREEMENT = 8
MOMENTS = (4, 0, 1, 3, 4, 10, 8)
DOMAIN = tuple(range(N))
EXPECTED_RECEIVED = (4, 3, 11, 5, 13, 6, 9, 0, 0, 0, 0, 0, 0, 0)
ANCHOR_COUNT = 45

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_full_span_forced_collision_route_cut_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_full_span_forced_collision_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json"
ACTIVATION_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_actual_hyperplane_packet_activation_route_cut.md"
ACTIVATION_VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py"
ACTIVATION_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-actual-hyperplane-packet-activation-route-cut/manifest.json"

SOURCE_SPECS = (
    ("route_cut_schema", SCHEMA_PATH, None,
     "Strict schema for the full-span forced-collision route-cut certificate."),
    ("route_cut_verifier", VERIFIER_PATH, None,
     "Primary exact full-layer enumerator and hostile mutation gate."),
    ("route_cut_sage", SAGE_PATH, None,
     "Independent Sage finite-field and linear-algebra replay."),
    ("route_cut_note", NOTE_PATH, None,
     "Abstract annihilator theorem, factorization, and implication boundary."),
    ("route_cut_readme", README_PATH, None,
     "Replay, provenance, and nonclaim contract."),
    ("canonical_predecessor_note",
     ROOT / "experimental/notes/thresholds/m31_canonical_masked_pade_global_route_cut.md",
     None, "Target-field deformation dichotomy and complete-layer regression source."),
    ("canonical_predecessor_verifier",
     ROOT / "experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py",
     None, "Predecessor exact layer, canonical masking, and collision replay."),
    ("canonical_predecessor_manifest",
     ROOT / "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json",
     "payload_sha256", "Sealed predecessor contract and source registry."),
    ("source_adapter_note",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Deployed five-atom LIST chronology adapter and null-atom authority."),
    ("source_adapter_manifest",
     ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
     "payload_sha256", "Sealed v4 source adapter and banked low-weight atom."),
    ("actual_boundary_source_note", ACTIVATION_NOTE_PATH, None,
     "Proved identity-prefix exact boundary layer with at least 1,993,678 supports."),
    ("actual_boundary_source_verifier", ACTIVATION_VERIFIER_PATH, None,
     "Exact verifier for the deployed identity-prefix boundary source."),
    ("actual_boundary_source_manifest", ACTIVATION_MANIFEST_PATH, None,
     "File-hash binding to the sealed actual-hyperplane activation route cut."),
    ("active_v4_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active LIST owner chronology and exact completion semantics."),
)


class VerificationError(RuntimeError):
    """Fail-closed exact-certificate error."""


CHECKS = 0


def require(value: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not value:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (encoded + "\n").encode("ascii")


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


def strict_json_path(path: Path, *, canonical: bool = False) -> Any:
    raw = path.read_bytes()
    require(len(raw) <= 32 * 1024 * 1024, "JSON size bound")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    value = json.loads(
        text, object_pairs_hook=unique_object, parse_int=int,
        parse_float=reject_float, parse_constant=reject_constant,
    )
    if canonical:
        require(raw == canonical_json(value), f"canonical JSON bytes: {path}")
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


# Coefficients are low to high throughout.


def inv(value: int) -> int:
    require(value % P != 0, "division by zero")
    return pow(value % P, P - 2, P)


def trim(polynomial: Sequence[int]) -> tuple[int, ...]:
    out = [value % P for value in polynomial]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def pad(polynomial: tuple[int, ...], width: int = K) -> list[int]:
    require(len(polynomial) <= width, "polynomial padding width")
    return list(polynomial) + [0] * (width - len(polynomial))


def poly_add(
    left: tuple[int, ...], right: tuple[int, ...], scale: int = 1,
) -> tuple[int, ...]:
    out = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += scale * value
    return trim(out)


def poly_scale(polynomial: tuple[int, ...], scale: int) -> tuple[int, ...]:
    return trim(tuple(scale * value for value in polynomial))


def poly_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x_value in enumerate(left):
        for j, y_value in enumerate(right):
            out[i + j] = (out[i + j] + x_value * y_value) % P
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
            remainder[index + shift] = (
                remainder[index + shift] - scalar * value
            ) % P
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return trim(quotient), trim(remainder)


def poly_gcd(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    while right != (0,):
        _, remainder = poly_divmod(left, right)
        left, right = right, remainder
    return poly_scale(left, inv(left[-1]))


def locator(points: Sequence[int]) -> tuple[int, ...]:
    out = (1,)
    for point in points:
        out = poly_mul(out, ((-point) % P, 1))
    return out


def divide_linear(polynomial: tuple[int, ...], point: int) -> tuple[int, ...]:
    quotient = [0] * (len(polynomial) - 1)
    quotient[-1] = polynomial[-1]
    for index in range(len(quotient) - 2, -1, -1):
        quotient[index] = (
            polynomial[index + 1] + point * quotient[index + 1]
        ) % P
    require((polynomial[0] + point * quotient[0]) % P == 0,
            "inexact linear division")
    return trim(quotient)


def evaluate(polynomial: tuple[int, ...], point: int) -> int:
    return sum(
        coefficient * pow(point, degree, P)
        for degree, coefficient in enumerate(polynomial)
    ) % P


def derivative_value(polynomial: tuple[int, ...], point: int) -> int:
    return sum(
        degree * polynomial[degree] * pow(point, degree - 1, P)
        for degree in range(1, len(polynomial))
    ) % P


def functional(polynomial: tuple[int, ...]) -> int:
    require(len(polynomial) <= K, "functional degree range")
    return sum(
        coefficient * MOMENTS[degree]
        for degree, coefficient in enumerate(polynomial)
    ) % P


def exact_support(points: tuple[int, ...]) -> bool:
    polynomial = locator(points)
    return (
        all(
            functional(trim((0,) * shift + polynomial)) == 0
            for shift in range(K - len(points))
        )
        and all(
            functional(divide_linear(polynomial, point)) != 0
            for point in points
        )
    )


def support_order_key(points: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(1 if point in points else 0 for point in DOMAIN)


def matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    require(bool(rows), "nonempty rank input")
    width = len(rows[0])
    require(width > 0 and all(len(row) == width for row in rows),
            "rectangular rank input")
    matrix = [[value % P for value in row] for row in rows]
    rank = 0
    for column in range(width):
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
        if rank == min(len(matrix), width):
            break
    return rank


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


def collision_polynomial(
    left: tuple[int, ...], right: tuple[int, ...], point: int,
) -> tuple[int, ...]:
    return poly_add(
        poly_scale(divide_linear(left, point), derivative_value(right, point)),
        poly_scale(divide_linear(right, point), derivative_value(left, point)),
        -1,
    )


def exact_set_packing(masks: Sequence[int]) -> tuple[int, tuple[int, ...]]:
    states: dict[int, tuple[int, tuple[int, ...]]] = {0: (0, ())}
    for index, mask in enumerate(masks):
        require(mask != 0, "nonempty collision mask")
        for used, (count, chosen) in list(states.items()):
            if used & mask:
                continue
            combined = used | mask
            candidate = (count + 1, chosen + (index,))
            if combined not in states or candidate[0] > states[combined][0]:
                states[combined] = candidate
    return max(states.values())


def exact_root_transversals(
    masks: Sequence[int], universe_size: int,
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    for size in range(universe_size + 1):
        witnesses: list[tuple[int, ...]] = []
        for points in itertools.combinations(range(universe_size), size):
            candidate = sum(1 << point for point in points)
            if all(candidate & mask for mask in masks):
                witnesses.append(points)
        if witnesses:
            return size, tuple(witnesses)
    raise VerificationError("nonempty finite family has no transversal")


def build_model() -> dict[str, Any]:
    require((N, K, J, RADIUS, AGREEMENT) == (14, 7, 6, 6, 8),
            "toy parameter contract")
    require(K - J == 1, "one containment row per toy support")

    supports = tuple(itertools.combinations(DOMAIN, J))
    layer = tuple(sorted(
        (support for support in supports if exact_support(support)),
        key=support_order_key,
    ))
    require(len(supports) == 3_003 and len(layer) == 137,
            "complete exact support census")

    locators = {support: locator(support) for support in layer}
    locator_rows = [pad(locators[support]) for support in layer]
    locator_rank = matrix_rank(locator_rows)
    require(locator_rank == K - 1 == 6, "full syndrome-hyperplane span")
    require(all(functional(locators[support]) == 0 for support in layer),
            "every locator lies in the syndrome hyperplane")

    codewords: dict[tuple[int, ...], tuple[int, ...]] = {}
    for support in layer:
        agreements = tuple(point for point in DOMAIN if point not in support)
        codeword = lagrange(tuple(
            (point, EXPECTED_RECEIVED[point]) for point in agreements[:K]
        ))
        require(all(
            evaluate(codeword, point) == EXPECTED_RECEIVED[point]
            for point in agreements
        ), "all agreement evaluations")
        require(all(
            evaluate(codeword, point) != EXPECTED_RECEIVED[point]
            for point in support
        ), "all error evaluations")
        codewords[support] = codeword
    require(len(set(codewords.values())) == len(layer), "distinct codewords")

    common_point_incidences = 0
    collision_incidences: list[tuple[int, int, int, tuple[int, ...]]] = []
    noncollision_incidences = 0
    factorization_checks = 0
    incidence_serial: list[str] = []
    for left_index, left_support in enumerate(layer):
        left_locator = locators[left_support]
        for right_index in range(left_index + 1, len(layer)):
            right_support = layer[right_index]
            right_locator = locators[right_support]
            for point in sorted(set(left_support).intersection(right_support)):
                common_point_incidences += 1
                polynomial = collision_polynomial(
                    left_locator, right_locator, point,
                )
                require(polynomial != (0,), "distinct-support collision form nonzero")

                common_locator = poly_gcd(left_locator, right_locator)
                common_without_point = divide_linear(common_locator, point)
                left_reduced, left_remainder = poly_divmod(
                    left_locator, common_locator,
                )
                right_reduced, right_remainder = poly_divmod(
                    right_locator, common_locator,
                )
                require(left_remainder == right_remainder == (0,),
                        "pair common-locator division")
                bracket = poly_add(
                    poly_scale(left_reduced, evaluate(right_reduced, point)),
                    poly_scale(right_reduced, evaluate(left_reduced, point)),
                    -1,
                )
                factorized = poly_scale(
                    poly_mul(common_without_point, bracket),
                    evaluate(common_without_point, point),
                )
                require(polynomial == factorized,
                        "reduced collision-form factorization")
                _, common_remainder = poly_divmod(polynomial, common_locator)
                require(common_remainder == (0,),
                        "collision polynomial contains full pairwise common locator")
                factorization_checks += 1

                actual_collision = (
                    evaluate(codewords[left_support], point)
                    == evaluate(codewords[right_support], point)
                )
                functional_collision = functional(polynomial) == 0
                require(actual_collision == functional_collision,
                        "collision form equals reconstructed codeword collision")
                incidence_serial.append(
                    f"{left_index},{right_index},{point},{int(actual_collision)}:"
                    + ",".join(map(str, pad(polynomial)))
                )
                if actual_collision:
                    collision_incidences.append(
                        (left_index, right_index, point, polynomial)
                    )
                else:
                    noncollision_incidences += 1

    require(common_point_incidences == 23_813, "common-point incidence count")
    require(len(collision_incidences) == 1_326, "actual collision incidence count")
    require(noncollision_incidences == 22_487, "proper collision-form count")
    require(factorization_checks == common_point_incidences,
            "all collision-form factorizations")

    collision_polynomials = [record[3] for record in collision_incidences]
    distinct_collision_polynomials = tuple(sorted(set(collision_polynomials)))
    require(len(distinct_collision_polynomials) == 1_219,
            "distinct forced collision polynomial count")
    require(matrix_rank([pad(value) for value in collision_polynomials]) == 4,
            "forced collision polynomial span rank")
    require(matrix_rank(locator_rows + [pad(value) for value in collision_polynomials])
            == locator_rank, "every actual collision polynomial lies in locator span")

    anchors = layer[:ANCHOR_COUNT]
    extras = layer[ANCHOR_COUNT:]
    anchor_locator_rank = matrix_rank([pad(locators[support]) for support in anchors])
    require(anchor_locator_rank == K - 1 == 6,
            "anchor locators span the syndrome hyperplane")
    collision_lookup = {
        (left, right, point)
        for left, right, point, _ in collision_incidences
    }
    masks: list[int] = []
    anchor_extra_collision_incidences = 0
    key_records: list[dict[str, Any]] = []
    marked_key_locator_ranks: list[int] = []
    for extra_offset, extra in enumerate(extras):
        extra_index = ANCHOR_COUNT + extra_offset
        key_rank = matrix_rank(
            [pad(locators[support]) for support in anchors]
            + [pad(locators[extra])]
        )
        require(key_rank == K - 1 == 6,
                "every 46-column marked family spans the syndrome hyperplane")
        marked_key_locator_ranks.append(key_rank)
        mask = 0
        for anchor_index, anchor in enumerate(anchors):
            for point in set(anchor).intersection(extra):
                if (anchor_index, extra_index, point) in collision_lookup:
                    anchor_extra_collision_incidences += 1
                    mask |= 1 << point
        require(mask != 0, "every marked key has an identically forced collision")
        masks.append(mask)
        key_records.append({
            "extra_index_one_based": extra_offset + 1,
            "global_index_one_based": extra_index + 1,
            "support": list(extra),
            "forced_collision_roots": [
                point for point in DOMAIN if mask & (1 << point)
            ],
        })
    require(anchor_extra_collision_incidences == 597,
            "anchor-extra forced collision incidences")
    require(sum(mask.bit_count() for mask in masks) == 357,
            "deduplicated key forced-root mass")

    packing, packing_indices = exact_set_packing(masks)
    require(packing == 5, "forced-root packing optimum")
    packing_witness = [key_records[index] for index in packing_indices]
    require(all(
        masks[left] & masks[right] == 0
        for left, right in itertools.combinations(packing_indices, 2)
    ), "forced-root packing witness")
    transversal, transversals = exact_root_transversals(masks, N)
    require(transversal == 6 and len(transversals) == 4,
            "forced-root transversal census")

    layer_serial = ";".join(",".join(map(str, support)) for support in layer)
    forced_serial = ";".join(
        f"{left},{right},{point}:" + ",".join(map(str, pad(polynomial)))
        for left, right, point, polynomial in collision_incidences
    )
    key_serial = ";".join(
        f"{record['global_index_one_based']}:"
        + ",".join(map(str, record["forced_collision_roots"]))
        for record in key_records
    )

    return {
        "toy_parameters": {
            "field": "GF(17)",
            "prime": P,
            "domain": list(DOMAIN),
            "n": N,
            "K": K,
            "weight": J,
            "radius": RADIUS,
            "agreement": AGREEMENT,
            "moments": list(MOMENTS),
            "received_word": list(EXPECTED_RECEIVED),
        },
        "full_span_fixture": {
            "support_universe_size": len(supports),
            "complete_exact_layer_size": len(layer),
            "ordered_layer_sha256": sha256_bytes(layer_serial.encode("ascii")),
            "containment_generator_count": len(layer),
            "containment_generator_rank": locator_rank,
            "syndrome_hyperplane_dimension": K - 1,
            "common_containment_functional_dimension": K - locator_rank,
            "span_equals_original_syndrome_kernel": True,
            "distinct_codeword_count": len(set(codewords.values())),
            "common_point_incidences": common_point_incidences,
            "actual_collision_incidences": len(collision_incidences),
            "proper_noncollision_incidences": noncollision_incidences,
            "distinct_forced_collision_polynomials": len(distinct_collision_polynomials),
            "forced_collision_polynomial_span_rank": 4,
            "all_actual_collisions_identically_forced": True,
            "all_noncollisions_proper_on_common_functional_space": True,
            "all_pair_common_locator_factorizations_verified": True,
            "incidence_table_sha256": sha256_bytes(
                ";".join(incidence_serial).encode("ascii")
            ),
            "forced_collision_table_sha256": sha256_bytes(
                forced_serial.encode("ascii")
            ),
        },
        "forced_key_noncoalescence": {
            "anchor_count": len(anchors),
            "anchor_containment_generator_rank": anchor_locator_rank,
            "marked_key_count": len(extras),
            "minimum_marked_key_containment_rank": min(marked_key_locator_ranks),
            "maximum_marked_key_containment_rank": max(marked_key_locator_ranks),
            "every_marked_key_spans_syndrome_hyperplane": True,
            "every_key_has_identically_forced_collision": True,
            "anchor_extra_forced_collision_incidences":
                anchor_extra_collision_incidences,
            "deduplicated_forced_root_mass": sum(mask.bit_count() for mask in masks),
            "forced_key_table_sha256": sha256_bytes(key_serial.encode("ascii")),
            "exact_disjoint_nonempty_union_optimum": packing,
            "five_union_witness": packing_witness,
            "exact_root_transversal_minimum": transversal,
            "minimum_root_transversals": [list(points) for points in transversals],
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
        require(not pure.is_absolute() and ".." not in pure.parts,
                "safe source path")
        internal: str | None = None
        if internal_key is not None:
            source = strict_json_path(path, canonical=True)
            require(type(source) is dict, "source manifest object")
            internal = source.get(internal_key)
            require(type(internal) is str and len(internal) == 64,
                    "source internal payload hash")
        bindings.append({
            "binding_id": f"M31_FULL_SPAN_FORCED_COLLISION::{role}",
            "role": role,
            "path": relative,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
            "scope": scope,
        })
    return bindings


def build_payload() -> dict[str, Any]:
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
            "deployed_row_closed": False,
            "ledger_movement": 0,
            "is_m31_counterexample": False,
            "toy_falsifier_scale": True,
        },
        "abstract_theorem": {
            "ambient_space": "V=F[X]_{<K}",
            "containment_span":
                "A(S)=span_F{X^t L_E: E in S, 0<=t<K-|E|}",
            "common_functional_space": "L(S)=A(S)^perp in V*",
            "collision_polynomial":
                "g_ikx=L_Ek'(x)L_Ei/(X-x)-L_Ei'(x)L_Ek/(X-x)",
            "forced_criterion":
                "chi_ikx vanishes identically on L(S) iff g_ikx is in A(S)",
            "quotient_column_criterion":
                "[v_i,x]=[v_k,x] in V/A(S), with v_i,x=L_i/((X-x)L_i'(x))",
            "pair_factorization":
                "g_ikx=C_x(x) C_x (P_k(x)P_i-P_i(x)P_k), C=(X-x)C_x",
            "full_common_locator_divides_collision_polynomial": True,
            "same_layer_theta_criterion":
                "after L_i=G P_i, the reduced collision column lies in im Theta_D0",
            "bounded_syzygy_criterion":
                "a degree-at-most-D0 locator syzygy evaluates to -alpha_i e_i+alpha_k e_k at x",
            "popov_evaluation_criterion":
                "-alpha_i e_i+alpha_k e_k lies in the evaluation rowspace of Popov rows of degree at most D0",
            "graph_to_common_zero_adapter":
                "one forced quotient-column class on a common-error coordinate makes that coordinate a common zero of all codeword differences in the class and a fixed mismatch for the original word",
            "maximum_rank_consequence":
                "if A(S)=ker(ell_0), then L(S)=F ell_0 and identically forced iff actual collision for ell_0",
            "maximum_rank_for_nonzero_exact_functional": "dim A(S)=K-1",
            "classification_is_semantic_owner": False,
        },
        "deployed_context": {
            "B_star": 16_777_215,
            "forbidden_size": 16_777_216,
            "banked_U_paid": 3_730,
            "low_weight_cutoff": 614_160,
            "high_weight_layer_count": 366_969,
            "high_baseline_45H": 16_513_605,
            "exact_mass_base_with_low_cap": 16_517_335,
            "safe_signed_occupancy_max": 259_880,
            "identity_prefix_boundary_layer_floor": 1_993_678,
            "identity_prefix_T46_floor": 1_993_633,
            "identity_prefix_T46_margin_over_signed_allowance": 1_733_753,
            "raw_T46_cap_refuted": True,
            "identity_prefix_boundary_only": True,
            "identity_prefix_delta46": 16_517_290,
            "identity_prefix_signed_target_is_Q_cap": True,
            "identity_prefix_complete_list_budget_status": "UNKNOWN",
            "signed_Xi46_cap_required": 259_880,
            "signed_refund_is_proved": False,
            "v4_negative_refund_interface_exists": False,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "high_U_new": None,
            "predecessor_terminal":
                "UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND",
            "successor_terminal":
                "UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER",
            "deployed_full_span_is_proved": False,
            "annihilator_membership_is_payment": False,
            "required_next_input":
                "a source-bound first-match theorem routing the identity-prefix boundary cell and proving the signed Xi46<=259880 bound with chronology-valid deficits and refunds",
        },
        **build_model(),
        "route_cut": {
            "falsified_parameter_uniform_implication":
                "complete exact layer plus prior canonical coupled hypotheses plus an identically forced collision on every marked key forces packing number at most four or a four-point transversal for the natural anchor-extra forced-collision-root unions",
            "falsifier":
                "the anchor locators and every 46-column marked family span the entire syndrome hyperplane, every marked key has an identically forced collision, but the natural forced-root unions have packing five and transversal six",
            "does_not_falsify":
                "an M31-specific split-locator hyperplane bound, cross-weight chronology theorem, non-root owner, or direct complete-list bound",
            "raw_T46_cap_refuted": True,
            "raw_T46_counterexample":
                "the proved identity-prefix boundary source has M_R>=1993678 and therefore T46>=1993633>259880",
            "signed_target_specializes_to_Q_cap": True,
            "payment_status": "NONE",
            "row_status": "OPEN",
        },
        "source_bindings": expected_source_bindings(),
    }


def exact_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"{label}: exact keys")


def verify_payload(
    payload: dict[str, Any], *, reference_model: dict[str, Any] | None = None,
) -> None:
    exact_keys(payload, {
        "schema", "architecture_id", "status", "payload_sha256", "scope",
        "abstract_theorem", "deployed_context", "toy_parameters",
        "full_span_fixture", "forced_key_noncoalescence", "route_cut",
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
        "deployed_row_closed": False,
        "ledger_movement": 0,
        "is_m31_counterexample": False,
        "toy_falsifier_scale": True,
    }, "scope contract")

    theorem = payload["abstract_theorem"]
    require(theorem["forced_criterion"] ==
            "chi_ikx vanishes identically on L(S) iff g_ikx is in A(S)",
            "annihilator criterion")
    require(theorem["full_common_locator_divides_collision_polynomial"] is True,
            "common-locator factor")
    require("Popov" in theorem["popov_evaluation_criterion"],
            "Popov evaluation-code criterion")
    require("common zero" in theorem["graph_to_common_zero_adapter"],
            "graph-to-common-zero adapter")
    require(theorem["classification_is_semantic_owner"] is False,
            "no automatic semantic owner")

    context = payload["deployed_context"]
    require(context == {
        "B_star": 16_777_215,
        "forbidden_size": 16_777_216,
        "banked_U_paid": 3_730,
        "low_weight_cutoff": 614_160,
        "high_weight_layer_count": 366_969,
        "high_baseline_45H": 16_513_605,
        "exact_mass_base_with_low_cap": 16_517_335,
        "safe_signed_occupancy_max": 259_880,
        "identity_prefix_boundary_layer_floor": 1_993_678,
        "identity_prefix_T46_floor": 1_993_633,
        "identity_prefix_T46_margin_over_signed_allowance": 1_733_753,
        "raw_T46_cap_refuted": True,
        "identity_prefix_boundary_only": True,
        "identity_prefix_delta46": 16_517_290,
        "identity_prefix_signed_target_is_Q_cap": True,
        "identity_prefix_complete_list_budget_status": "UNKNOWN",
        "signed_Xi46_cap_required": 259_880,
        "signed_refund_is_proved": False,
        "v4_negative_refund_interface_exists": False,
        "U_Q": None,
        "U_list_int": None,
        "U_ext": None,
        "high_U_new": None,
        "predecessor_terminal":
            "UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND",
        "successor_terminal":
            "UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER",
        "deployed_full_span_is_proved": False,
        "annihilator_membership_is_payment": False,
        "required_next_input":
            "a source-bound first-match theorem routing the identity-prefix boundary cell and proving the signed Xi46<=259880 bound with chronology-valid deficits and refunds",
    }, "deployed context")
    require(context["high_baseline_45H"] ==
            45 * context["high_weight_layer_count"], "45H baseline")
    require(context["exact_mass_base_with_low_cap"] ==
            context["banked_U_paid"] + context["high_baseline_45H"],
            "exact low-plus-high baseline")
    require(context["identity_prefix_T46_floor"] ==
            context["identity_prefix_boundary_layer_floor"] - 45,
            "identity-prefix T46 floor")
    require(context["identity_prefix_T46_margin_over_signed_allowance"] ==
            context["identity_prefix_T46_floor"]
            - context["safe_signed_occupancy_max"],
            "raw T46 counterexample margin")
    require(context["raw_T46_cap_refuted"] is True,
            "raw T46 cap refuted")
    require(context["signed_refund_is_proved"] is False,
            "signed refund remains open")
    require(context["identity_prefix_boundary_only"] is True,
            "identity-prefix center is boundary-only")
    require(context["identity_prefix_delta46"] ==
            3_730 + 45 * (context["high_weight_layer_count"] - 1),
            "identity-prefix exact deficit")
    require(context["identity_prefix_signed_target_is_Q_cap"] is True,
            "signed target specializes to Q cap")
    require(context["v4_negative_refund_interface_exists"] is False,
            "no v4 negative-refund interface")
    require(context["exact_mass_base_with_low_cap"]
            + context["signed_Xi46_cap_required"] == context["B_star"],
            "signed target equals exact Q budget")

    if reference_model is None:
        reference_model = build_model()
    for section in (
        "toy_parameters", "full_span_fixture", "forced_key_noncoalescence",
    ):
        require(payload[section] == reference_model[section],
                f"exact regenerated section: {section}")

    fixture = payload["full_span_fixture"]
    require(fixture["containment_generator_rank"] ==
            fixture["syndrome_hyperplane_dimension"] == 6,
            "full-span equality")
    require(fixture["common_containment_functional_dimension"] == 1,
            "common functional line")
    require(fixture["all_actual_collisions_identically_forced"] is True,
            "all actual collisions forced")
    require(fixture["all_noncollisions_proper_on_common_functional_space"] is True,
            "all noncollisions proper")

    keys = payload["forced_key_noncoalescence"]
    require(keys["every_key_has_identically_forced_collision"] is True,
            "forced collision on every key")
    require(keys["anchor_containment_generator_rank"] == 6,
            "anchor full-span rank")
    require(keys["minimum_marked_key_containment_rank"] ==
            keys["maximum_marked_key_containment_rank"] == 6,
            "marked-key full-span ranks")
    require(keys["every_marked_key_spans_syndrome_hyperplane"] is True,
            "every marked key full span")
    require(keys["exact_disjoint_nonempty_union_optimum"] == 5,
            "packing optimum")
    require(keys["exact_root_transversal_minimum"] == 6,
            "transversal minimum")
    require(keys["no_four_point_root_transversal"] is True,
            "no four-point transversal")

    route = payload["route_cut"]
    require(route["payment_status"] == "NONE" and route["row_status"] == "OPEN",
            "route-cut nonpayment")
    require(route["raw_T46_cap_refuted"] is True,
            "raw T46 route cut")
    require(route["signed_target_specializes_to_Q_cap"] is True,
            "signed target Q specialization")
    require("M31-specific" in route["does_not_falsify"], "M31 nonclaim")
    require(payload["source_bindings"] == expected_source_bindings(),
            "live source bindings")


def mutate_path(payload: dict[str, Any], path: Sequence[Any], replacement: Any) -> None:
    cursor: Any = payload
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def tamper_selftest(expected: dict[str, Any], model: dict[str, Any]) -> None:
    mutations: tuple[tuple[str, Sequence[Any], Any], ...] = (
        ("row-closed", ("scope", "deployed_row_closed"), True),
        ("ledger-movement", ("scope", "ledger_movement"), 1),
        ("m31-counterexample", ("scope", "is_m31_counterexample"), True),
        ("forced-criterion", ("abstract_theorem", "forced_criterion"), "UNKNOWN"),
        ("common-factor", ("abstract_theorem", "full_common_locator_divides_collision_polynomial"), False),
        ("semantic-owner", ("abstract_theorem", "classification_is_semantic_owner"), True),
        ("popov-criterion", ("abstract_theorem", "popov_evaluation_criterion"), "UNKNOWN"),
        ("common-zero-adapter", ("abstract_theorem", "graph_to_common_zero_adapter"), "UNKNOWN"),
        ("invent-UQ", ("deployed_context", "U_Q"), 0),
        ("invent-Uext", ("deployed_context", "U_ext"), 0),
        ("deployed-full-span", ("deployed_context", "deployed_full_span_is_proved"), True),
        ("payment", ("deployed_context", "annihilator_membership_is_payment"), True),
        ("terminal", ("deployed_context", "successor_terminal"), "PAID"),
        ("high-baseline", ("deployed_context", "high_baseline_45H"), 16_513_604),
        ("raw-T46-cap", ("deployed_context", "raw_T46_cap_refuted"), False),
        ("identity-prefix-floor", ("deployed_context", "identity_prefix_boundary_layer_floor"), 1_993_677),
        ("signed-refund", ("deployed_context", "signed_refund_is_proved"), True),
        ("boundary-only", ("deployed_context", "identity_prefix_boundary_only"), False),
        ("identity-deficit", ("deployed_context", "identity_prefix_delta46"), 16_517_289),
        ("negative-refund-interface", ("deployed_context", "v4_negative_refund_interface_exists"), True),
        ("toy-field", ("toy_parameters", "prime"), 19),
        ("layer-size", ("full_span_fixture", "complete_exact_layer_size"), 136),
        ("locator-rank", ("full_span_fixture", "containment_generator_rank"), 5),
        ("functional-dimension", ("full_span_fixture", "common_containment_functional_dimension"), 2),
        ("collision-count", ("full_span_fixture", "actual_collision_incidences"), 1_325),
        ("proper-count", ("full_span_fixture", "proper_noncollision_incidences"), 22_486),
        ("forced-count", ("full_span_fixture", "distinct_forced_collision_polynomials"), 1_218),
        ("factorization", ("full_span_fixture", "all_pair_common_locator_factorizations_verified"), False),
        ("all-forced", ("full_span_fixture", "all_actual_collisions_identically_forced"), False),
        ("anchor-rank", ("forced_key_noncoalescence", "anchor_containment_generator_rank"), 5),
        ("key-rank", ("forced_key_noncoalescence", "minimum_marked_key_containment_rank"), 5),
        ("every-key-span", ("forced_key_noncoalescence", "every_marked_key_spans_syndrome_hyperplane"), False),
        ("key-forced", ("forced_key_noncoalescence", "every_key_has_identically_forced_collision"), False),
        ("packing", ("forced_key_noncoalescence", "exact_disjoint_nonempty_union_optimum"), 4),
        ("transversal", ("forced_key_noncoalescence", "exact_root_transversal_minimum"), 5),
        ("witness-root", ("forced_key_noncoalescence", "five_union_witness", 0, "forced_collision_roots"), [9]),
        ("false-payment", ("route_cut", "payment_status"), "PAID"),
        ("false-row", ("route_cut", "row_status"), "CLOSED"),
        ("false-scope", ("route_cut", "does_not_falsify"), "nothing"),
        ("false-T46-route", ("route_cut", "raw_T46_cap_refuted"), False),
        ("false-Q-specialization", ("route_cut", "signed_target_specializes_to_Q_cap"), False),
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

    model = build_model()
    if args.model_check:
        print("model=PASS layer=137 locator_rank=6 containment_dim=1 "
              "forced_collisions=1326 packing=5 transversal=6")
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
        print("M31 full-span forced-collision route cut: PASS")
        print("abstract: forced iff collision polynomial lies in containment span")
        print("GF(17): layer=137, locator span=6=K-1, common functional dim=1")
        print("incidences: common=23813, forced collisions=1326, proper=22487")
        print("noncoalescence: every key full-span/forced; packing=5; transversal=6")
        print("deployed route cut: identity-prefix T46>=1993633; raw T46 cap refuted")
        print("scope: universal route cut; M31 row OPEN; ledger movement=0")

    if args.tamper_selftest:
        tamper_selftest(expected, model)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
    else:
        print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
