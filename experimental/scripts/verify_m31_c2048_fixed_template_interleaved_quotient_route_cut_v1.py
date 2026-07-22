#!/usr/bin/env python3
"""Exact verifier for the M31 fixed-template interleaved quotient route cut.

The packet proves the complete fixed-partial-template packing bound, the
locator-jet/normalized-cofactor-jet bijection, a 15-target fixed-template
construction, and a varying-template gluing obstruction.  It deliberately
ends at an unpaid attained-image sum and moves no LIST ledger atom.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable


SCHEMA_ID = "rs-mca-c2048-fixed-template-interleaved-quotient-route-cut-v1"
ARCHITECTURE_ID = "M31_C2048_FIXED_TEMPLATE_INTERLEAVED_QUOTIENT_ROUTE_CUT_V1"
STATUS = "PROVED_FIXED_TEMPLATE_BOUND_AND_TARGET_ROUTE_CUT_GLOBAL_SUM_OPEN"
PARENT_TERMINAL = "M31_C2048_65COLUMN_FIXED_ANCHOR_OWNER"
NEW_TERMINAL = "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER"

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
B_STAR = P**4 // 2**100
TARGET_FIELD_SIZE = P**4
U_PAID = 3_730
COMBINED_BOUNDARY_ALLOWANCE = 9_216_781

C = 2_048
FIBERS = N // C
AGREEMENT_QUOTIENT = AGREEMENT // C
AGREEMENT_REMAINDER = AGREEMENT % C
ERROR_QUOTIENT = RADIUS // C
ERROR_REMAINDER = RADIUS % C
QUOTIENT_PREFIX_DEPTH = W // C
QUOTIENT_PREFIX_REMAINDER = W % C
PROFILE_COUNT = 261_192

PARENT_PAYLOAD = "1474cf06d7a058a010462ca06758df0576de9464441fa9245ddaf1b8e7d23245"
PARENT_HEAD = "464091b7a3b85048b6646dded6b7455e471cd0f7"
PARENT_PR = 1042
UPSTREAM_MAIN = "32a41660e3088eeeb15a16645330856794302ff0"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_c2048_fixed_template_interleaved_quotient_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the fixed-template interleaved quotient packet."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Primary exact profile census, constructions, and mutation replay."),
    ("packet_sage", SAGE_PATH, None,
     "Independent finite-field and polynomial-module replay."),
    ("packet_note", NOTE_PATH, None,
     "Symbolic local theorems, legal global sum, and route cut."),
    ("packet_readme", README_PATH, None,
     "Replay, dependency, and nonclaim contract."),
    ("parent_1042_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-65column-fixed-anchor-route-cut-v1/manifest.json",
     "payload_sha256", "Sealed immediate predecessor PR #1042 packet."),
    ("multiprefix_source_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json",
     "payload_sha256", "Fixed-template sources and arbitrary-word multiprefix correction."),
    ("occupancy_atlas_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json",
     "payload_sha256", "Exhaustive c=2048 occupancy atlas."),
    ("exact_quotient_remainder_source",
     ROOT / "experimental/rs_mca_thresholds.tex", None,
     "QR2/QR5 reciprocal normal form and complete-support factorization."),
    ("chebyshev_domain_source", ROOT / "tex/cs25_cap_v13_2.tex", None,
     "Deployed complete Chebyshev fibers and target-field parameters."),
    ("target_field_source_adapter",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Exact target-field LIST chronology and source adapter."),
    ("active_v4_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active nonnegative LIST chronology and row-sharp Q target."),
    ("admissibility_authority",
     ROOT / "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex",
     None, "Non-oracular first-match and attained-image requirements."),
)


class VerificationError(RuntimeError):
    """Fail-closed certificate error."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
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
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, *, canonical: bool = False) -> Any:
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
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def strict_json_path(path: Path, *, canonical: bool = False) -> Any:
    require(path.is_file(), f"JSON path exists: {path}")
    return strict_json_bytes(path.read_bytes(), canonical=canonical)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"bound source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_sha256(result)
    return result


def internal_payload(path: Path, key: str | None) -> str | None:
    if key is None:
        return None
    value = strict_json_path(path, canonical=True)
    require(type(value) is dict, f"internal manifest object: {path}")
    internal = value.get(key)
    require(type(internal) is str and len(internal) == 64,
            f"internal payload hash: {path}")
    return internal


def expected_source_bindings() -> list[dict[str, Any]]:
    result = []
    for role, path, internal_key, scope in SOURCE_SPECS:
        relative = path.relative_to(ROOT)
        require(PurePosixPath(relative.as_posix()).as_posix() == relative.as_posix(),
                f"canonical source path: {path}")
        internal = internal_payload(path, internal_key)
        if role == "parent_1042_manifest":
            require(internal == PARENT_PAYLOAD, "exact #1042 payload")
        result.append({
            "binding_id": f"M31_C2048_FIXED_TEMPLATE::{role}",
            "path": relative.as_posix(),
            "role": role,
            "scope": scope,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
        })
    return result


def feasible_profiles() -> list[tuple[int, int]]:
    profiles: list[tuple[int, int]] = []
    for u in range(480):
        vmax = 136 if u == 0 else 544
        for v in range(vmax + 1):
            h = u + v + 1
            r_error = ERROR_REMAINDER + C * u
            r_agreement = AGREEMENT_REMAINDER + C * v
            require(r_error + r_agreement == C * h, "profile color sum")
            require(h <= r_error <= h * (C - 1), "error partial feasibility")
            require(h <= r_agreement <= h * (C - 1),
                    "agreement partial feasibility")
            profiles.append((u, v))
    require(len(profiles) == PROFILE_COUNT, "profile count")
    require(len(set(profiles)) == PROFILE_COUNT, "profile uniqueness")
    return profiles


def fixed_template_row(u: int, v: int) -> tuple[Any, ...]:
    h = u + v + 1
    r = AGREEMENT_REMAINDER + C * v
    f = AGREEMENT_QUOTIENT - v
    available = FIBERS - h
    require(r + C * f == AGREEMENT, "agreement decomposition")
    require(available == 1023 - u - v, "available quotient labels")
    require(0 <= f <= available, "quotient support feasibility")
    if v >= 512:
        require(r >= K, "uniqueness root gate")
        branch = "MDS_FIXED_TEMPLATE_UNIQUENESS"
        kappa = 0
        high_component_degree = -1
        low_component_degree = -1
        cap = 1
    else:
        require(r < K, "interleaved quotient gate")
        kappa = 512 - v
        require(K - r == C * (511 - v) + 137,
                "component degree split")
        high_component_degree = 511 - v
        low_component_degree = 510 - v
        require(kappa == high_component_degree + 1, "packing subset size")
        require(1 <= kappa <= f <= available, "packing parameters")
        numerator = math.comb(available, kappa)
        denominator = math.comb(f, kappa)
        require(numerator >= denominator > 0, "packing quotient domain")
        cap = numerator // denominator
        branch = "INTERLEAVED_QUOTIENT_PACKING"
    return (
        u, v, h, r, f, available, branch, kappa,
        high_component_degree, low_component_degree, cap,
    )


def profile_census() -> dict[str, Any]:
    digest = hashlib.sha256()
    rows = []
    thresholds = (1, 15, 36, 65, B_STAR)
    counts = {value: 0 for value in thresholds}
    uniqueness = 0
    additional_budget = 0
    for u, v in feasible_profiles():
        row = fixed_template_row(u, v)
        rows.append(row)
        digest.update((",".join(str(x) for x in row) + "\n").encode("ascii"))
        cap = row[-1]
        for threshold in thresholds:
            counts[threshold] += int(cap <= threshold)
        if v >= 512:
            uniqueness += 1
        elif cap <= B_STAR:
            additional_budget += 1

    budget_rows = [row for row in rows if row[-1] <= B_STAR]
    unpaid_rows = [row for row in rows if row[-1] > B_STAR]
    maximum_budget_cap = max(row[-1] for row in budget_rows)
    minimum_unpaid_cap = min(row[-1] for row in unpaid_rows)
    maximum_budget_profiles = [[row[0], row[1]] for row in budget_rows
                               if row[-1] == maximum_budget_cap]
    minimum_unpaid_profiles = [[row[0], row[1]] for row in unpaid_rows
                               if row[-1] == minimum_unpaid_cap]
    face_00 = next(row for row in rows if row[0] == 0 and row[1] == 0)

    require(uniqueness == 15_807, "uniqueness profile census")
    require(additional_budget == 9_960, "additional budget profile census")
    require(counts[1] == 16_422, "cap-one profile census")
    require(counts[15] == 17_763, "cap-fifteen profile census")
    require(counts[36] == 18_105, "cap-thirty-six profile census")
    require(counts[65] == 18_388, "cap-sixty-five profile census")
    require(counts[B_STAR] == 25_767, "budget-fitting profile census")
    require(len(unpaid_rows) == 235_425, "unpaid profile census")
    require(maximum_budget_cap == 16_769_604, "largest budget-fitting cap")
    require(maximum_budget_profiles == [[128, 505], [472, 161]],
            "largest budget-fitting profiles")
    require(minimum_unpaid_cap == 16_808_455, "smallest above-budget cap")
    require(minimum_unpaid_profiles == [[224, 504], [471, 257]],
            "smallest above-budget profiles")
    require(len(str(face_00[-1])) == 255, "face cap digit count")

    return {
        "profile_count": len(rows),
        "rows_sha256": digest.hexdigest(),
        "v_at_least_512_uniqueness_profiles": uniqueness,
        "additional_budget_fitting_profiles": additional_budget,
        "cap_at_most_1_profiles": counts[1],
        "cap_at_most_15_profiles": counts[15],
        "cap_at_most_36_profiles": counts[36],
        "cap_at_most_65_profiles": counts[65],
        "cap_at_most_B_star_profiles": counts[B_STAR],
        "cap_above_B_star_profiles": len(unpaid_rows),
        "largest_budget_fitting_cap": maximum_budget_cap,
        "largest_budget_fitting_profiles": maximum_budget_profiles,
        "smallest_above_budget_cap": minimum_unpaid_cap,
        "smallest_above_budget_profiles": minimum_unpaid_profiles,
        "profile_0_0_cap": str(face_00[-1]),
        "profile_0_0_cap_digits": len(str(face_00[-1])),
    }


def deterministic_blocks() -> tuple[list[list[int]], list[int], list[int]]:
    remaining = list(range(512, 1024))
    blocks: list[list[int]] = []
    sums: list[int] = []
    for index in range(15):
        require(len(remaining) == 512 - 33 * index, "block remaining size")
        anchor = remaining[:32]
        candidates = remaining[32:]
        require(len(candidates) >= 18, "distinct-sum candidate floor")
        selected = None
        for point in candidates:
            candidate_sum = (sum(anchor) + point) % P
            if candidate_sum not in sums:
                selected = point
                break
        require(selected is not None, "new block sum exists")
        block = [*anchor, selected]
        block_set = set(block)
        require(len(block_set) == 33, "block cardinality")
        blocks.append(block)
        sums.append(sum(block) % P)
        remaining = [point for point in remaining if point not in block_set]
    require(len(remaining) == 17, "unused label count")
    require(len(set(sums)) == 15, "block sums distinct")
    require(len(set().union(*(set(block) for block in blocks))) == 495,
            "blocks pairwise disjoint")
    return blocks, sums, remaining


def fifteen_target_fixture() -> dict[str, Any]:
    blocks, sums, unused = deterministic_blocks()
    j_labels = list(range(1, 512))
    beta_0 = 0
    scalars = list(range(1, 16))
    target_coefficients = [(-sum(j_labels) - value) % P for value in sums]
    require(len(j_labels) == 511, "J cardinality")
    require(len(set(j_labels).intersection(set().union(
        *(set(block) for block in blocks)))) == 0, "J-block disjointness")
    require(beta_0 not in j_labels and beta_0 not in unused,
            "beta separate from quotient partition")
    require(len(set(target_coefficients)) == 15, "quotient targets distinct")
    require(len(set(scalars)) == 15 and all(value != 0 for value in scalars),
            "nonzero distinct scalars")

    codeword_degree = AGREEMENT_REMAINDER + C * 511
    center_degree_upper = AGREEMENT_REMAINDER + C * 1023
    cofactor_quotient_degree_upper = 479
    cofactor_degree_upper = C * cofactor_quotient_degree_upper
    support_size = AGREEMENT_REMAINDER + C * (511 + 33)
    require(codeword_degree == K - 137, "15-target codeword degree")
    require(center_degree_upper == N - 137, "15-target center degree")
    require(cofactor_degree_upper == RADIUS - 137,
            "15-target cofactor degree")
    require(support_size == AGREEMENT, "15-target exact support size")
    require(511 + 15 * 33 + 17 + 1 == FIBERS,
            "quotient label partition")
    for i in range(15):
        zero_labels = set(j_labels).union(blocks[i])
        other_blocks = set().union(
            *(set(blocks[j]) for j in range(15) if j != i))
        nonzero_labels = other_blocks.union(unused).union({beta_0})
        require(len(zero_labels) == 544, "exact quotient zero labels")
        require(len(nonzero_labels) == 480, "exact quotient nonzero labels")
        require(zero_labels.isdisjoint(nonzero_labels),
                "zero/nonzero label disjointness")
        require(len(zero_labels.union(nonzero_labels)) == FIBERS,
                "zero/nonzero label exhaustion")

    block_digest = sha256_bytes(canonical_json({
        "blocks": blocks, "sums": sums, "unused": unused,
    }))
    return {
        "profile": [0, 0],
        "fixed_partial_label_count": 1,
        "fixed_partial_template_size": AGREEMENT_REMAINDER,
        "J_size": len(j_labels),
        "U_size": 512,
        "block_count": len(blocks),
        "block_size": 33,
        "unused_labels": len(unused),
        "block_sums_pairwise_distinct": True,
        "block_fixture_sha256": block_digest,
        "interpolation_label_count": 513,
        "interpolation_degree_upper": 512,
        "distinct_nonzero_scalars": len(scalars),
        "full_agreement_labels_per_codeword": 544,
        "codeword_degree": codeword_degree,
        "codeword_headroom": K - codeword_degree,
        "center_degree_upper": center_degree_upper,
        "center_headroom": N - center_degree_upper,
        "quotient_cofactor_degree_upper": cofactor_quotient_degree_upper,
        "cofactor_degree_upper": cofactor_degree_upper,
        "cofactor_headroom": RADIUS - cofactor_degree_upper,
        "exact_support_size": support_size,
        "attained_quotient_locator_cofactor_targets_lower": 15,
        "QR2_directly_applicable_here": True,
        "complete_ball_target_count_claimed": False,
    }


def core_payload() -> dict[str, Any]:
    census = profile_census()
    fixture = fifteen_target_fixture()
    require(P == 2_147_483_647, "Mersenne prime")
    require(N == 2_097_152 and K == 1_048_576, "deployed dimensions")
    require(AGREEMENT == 1_116_023 and RADIUS == 981_129,
            "agreement and radius")
    require(W == 67_447, "prefix depth")
    require(B_STAR == 16_777_215, "LIST budget")
    require(FIBERS == 1_024, "quotient labels")
    require(AGREEMENT_QUOTIENT == 544 and AGREEMENT_REMAINDER == 1_911,
            "agreement quotient remainder")
    require(ERROR_QUOTIENT == 479 and ERROR_REMAINDER == 137,
            "error quotient remainder")
    require(QUOTIENT_PREFIX_DEPTH == 32 and QUOTIENT_PREFIX_REMAINDER == 1_911,
            "quotient prefix decomposition")
    require(C - AGREEMENT_REMAINDER == 137,
            "137 high-component residue count")
    require(AGREEMENT_REMAINDER == 1_911,
            "1911 low-component residue count")
    require(AGREEMENT - K == W, "cofactor modulus headroom")
    require(66 * C == 135_168 < K, "varying-template intersection gate")

    return {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "deployed_parameters": {
            "p": P,
            "target_field_size": str(TARGET_FIELD_SIZE),
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "prefix_depth_w": W,
            "B_star": B_STAR,
            "U_paid": U_PAID,
            "combined_boundary_allowance": COMBINED_BOUNDARY_ALLOWANCE,
            "fold_degree": C,
            "quotient_labels": FIBERS,
            "agreement_quotient": AGREEMENT_QUOTIENT,
            "agreement_remainder": AGREEMENT_REMAINDER,
            "error_quotient": ERROR_QUOTIENT,
            "error_remainder": ERROR_REMAINDER,
            "quotient_prefix_depth": QUOTIENT_PREFIX_DEPTH,
            "quotient_prefix_remainder": QUOTIENT_PREFIX_REMAINDER,
        },
        "fixed_template_theorem": {
            "profile_coordinates": {
                "partial_label_count": "h=u+v+1",
                "partial_agreement_size": "r=1911+2048*v",
                "full_agreement_labels": "f=544-v",
                "available_full_labels": "M=1023-u-v",
            },
            "v_at_least_512_cap": 1,
            "v_at_most_511_kappa": "512-v",
            "v_at_most_511_cap": "floor(binomial(M,kappa)/binomial(f,kappa))",
            "free_module_basis_size": C,
            "high_component_count": 137,
            "high_component_degree_upper": "511-v",
            "low_component_count": 1_911,
            "low_component_degree_upper": "510-v",
            "v_511_low_components_zero": True,
            "pairwise_quotient_support_intersection_upper": "511-v",
            "exactness_only_restricts_further": True,
            "field_generic": True,
        },
        "profile_census": census,
        "cofactor_jet_bridge": {
            "nonempty_family_forces_degree_Y_at_least_A": True,
            "degree_parameter": "deg(Y)=A+s",
            "leading_normalization": "Hbar=lc(Y)^(-1)*H is monic of degree s",
            "reciprocal_congruence": "L_S^vee*Hbar^vee=lc(Y)^(-1)*Y^vee mod Z^(w+s+1)",
            "codeword_term_valuation_lower": "A+s-(K-1)=w+s+1",
            "locator_and_normalized_cofactor_w_jets_bijective": True,
            "fiber_cardinalities_preserved": True,
            "fixed_template_cancellation_uses_unit_L0_reciprocal": True,
            "quotient_coefficients_visible": "min(32,f)",
            "general_fixed_template_uses_QR5_triangular_argument": True,
            "general_fixed_template_claims_QR2_directly": False,
            "zero_padding_when_s_less_than_w": True,
        },
        "fifteen_target_construction": fixture,
        "varying_template_route_cut": {
            "profile": [0, 0],
            "partial_template_count": 2,
            "partial_template_size_each": AGREEMENT_REMAINDER,
            "distinct_partial_labels": 2,
            "common_full_labels": 66,
            "private_full_labels_each": 478,
            "full_agreement_labels_each": 544,
            "support_size_each": AGREEMENT,
            "intersection_size": 66 * C,
            "intersection_below_K": True,
            "gluing_codewords": ["0", "L_intersection"],
            "same_profile_forces_common_template": False,
            "budget_violation_claimed": False,
        },
        "chronology": {
            "parent_terminal": PARENT_TERMINAL,
            "successor_terminal": NEW_TERMINAL,
            "legal_exact_boundary_sum": "sum_profile sum_partial_template sum_attained_normalized_cofactor_jet N_Y",
            "fixed_template_theorem_bounds_innermost_target_sum": True,
            "global_profile_template_target_sum_paid": False,
            "row_sharp_Q_payment_proved": False,
            "varying_template_owner_proved": False,
            "maximum_prefix_fiber_is_sufficient": False,
            "owner_paid": False,
        },
        "external_dependencies": {
            "parent_pr": PARENT_PR,
            "parent_head": PARENT_HEAD,
            "parent_payload_sha256": PARENT_PAYLOAD,
            "upstream_main_at_preparation": UPSTREAM_MAIN,
        },
        "scope": {
            "object": "LIST",
            "row": "Mersenne-31 list at 2^-100",
            "workboard_item": "M1",
            "unit": "DISTINCT_EXACT_BOUNDARY_CODEWORDS_PER_RECEIVED_WORD",
            "impact": "FIXED_TEMPLATE_INTERLEAVED_BOUND_AND_ATTAINED_TARGET_ROUTE_CUT",
            "ledger_movement": 0,
            "deployed_row_closed": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "nonclaims": {
            "complete_exact_boundary_paid": False,
            "combined_boundary_allowance_paid": False,
            "high_interior_paid": False,
            "U_Q_paid": False,
            "U_list_int_paid": False,
            "U_ext_paid": False,
            "U_new_paid": False,
            "all_same_profile_codewords_share_one_template": False,
            "one_or_four_attained_targets_per_fixed_template": False,
            "fifteen_target_complete_ball_is_boundary_only": False,
            "official_endpoint_or_score_changed": False,
        },
    }


def build_manifest() -> dict[str, Any]:
    payload = core_payload()
    payload["source_bindings"] = expected_source_bindings()
    return seal(payload)


def source_binding_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "binding_id", "internal_payload_sha256", "path", "role",
            "scope", "sha256",
        ],
        "properties": {
            "binding_id": {"type": "string", "minLength": 1},
            "internal_payload_sha256": {
                "type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
            "path": {"type": "string", "minLength": 1},
            "role": {"type": "string", "minLength": 1},
            "scope": {"type": "string", "minLength": 1},
            "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
    }


def build_schema() -> dict[str, Any]:
    core = core_payload()
    keys = sorted([*core, "payload_sha256", "source_bindings"])
    properties: dict[str, Any] = {key: {"const": value}
                                  for key, value in core.items()}
    properties["payload_sha256"] = {
        "type": "string", "pattern": "^[0-9a-f]{64}$"}
    properties["source_bindings"] = {
        "type": "array", "minItems": len(SOURCE_SPECS),
        "maxItems": len(SOURCE_SPECS), "uniqueItems": True,
        "items": {"$ref": "#/$defs/sourceBinding"},
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "M31 fixed-template interleaved quotient route-cut certificate",
        "type": "object",
        "additionalProperties": False,
        "required": keys,
        "properties": properties,
        "$defs": {"sourceBinding": source_binding_schema()},
    }


def validate_schema(schema: Any, payload: dict[str, Any]) -> None:
    require(type(schema) is dict, "schema object")
    require(schema == build_schema(), "schema exact replay")
    require(set(schema["required"]) == set(payload), "schema root keys")
    require(set(schema["properties"]) == set(payload), "schema properties")


def verify_payload(candidate: dict[str, Any], *, expected: dict[str, Any]) -> None:
    require(type(candidate) is dict, "manifest object")
    require(type(candidate.get("payload_sha256")) is str, "payload hash type")
    require(candidate.get("payload_sha256") == payload_sha256(candidate),
            "payload hash")
    bindings = candidate.get("source_bindings")
    require(type(bindings) is list and len(bindings) == len(SOURCE_SPECS),
            "source binding count")
    ids = [item.get("binding_id") for item in bindings if type(item) is dict]
    require(len(ids) == len(bindings) and len(set(ids)) == len(ids),
            "source binding IDs unique")
    require(candidate == expected, "manifest exact replay")


def write_artifacts() -> None:
    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_PATH.write_bytes(canonical_json(build_schema()))
    MANIFEST_PATH.write_bytes(canonical_json(build_manifest()))


def set_path(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def mutate(payload: dict[str, Any]) -> None:
        target: Any = payload
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    return mutate


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("B star", set_path(("deployed_parameters", "B_star"), B_STAR - 1)),
        ("prefix depth", set_path(("deployed_parameters", "prefix_depth_w"), W - 1)),
        ("prefix quotient", set_path(("deployed_parameters", "quotient_prefix_depth"), 31)),
        ("prefix remainder", set_path(("deployed_parameters", "quotient_prefix_remainder"), 1_910)),
        ("profile count", set_path(("profile_census", "profile_count"), PROFILE_COUNT - 1)),
        ("profile digest", set_path(("profile_census", "rows_sha256"), "0" * 64)),
        ("v512 census", set_path(("profile_census", "v_at_least_512_uniqueness_profiles"), 15_806)),
        ("additional budget census", set_path(("profile_census", "additional_budget_fitting_profiles"), 9_959)),
        ("cap one census", set_path(("profile_census", "cap_at_most_1_profiles"), 16_421)),
        ("cap 15 census", set_path(("profile_census", "cap_at_most_15_profiles"), 17_762)),
        ("cap 36 census", set_path(("profile_census", "cap_at_most_36_profiles"), 18_104)),
        ("cap 65 census", set_path(("profile_census", "cap_at_most_65_profiles"), 18_387)),
        ("budget profile census", set_path(("profile_census", "cap_at_most_B_star_profiles"), 25_766)),
        ("unpaid profile census", set_path(("profile_census", "cap_above_B_star_profiles"), 235_424)),
        ("max paid cap", set_path(("profile_census", "largest_budget_fitting_cap"), 16_769_605)),
        ("max paid profile", set_path(("profile_census", "largest_budget_fitting_profiles", 0, 0), 129)),
        ("min unpaid cap", set_path(("profile_census", "smallest_above_budget_cap"), 16_808_454)),
        ("min unpaid profile", set_path(("profile_census", "smallest_above_budget_profiles", 1, 1), 258)),
        ("face cap", set_path(("profile_census", "profile_0_0_cap"), "1")),
        ("face digits", set_path(("profile_census", "profile_0_0_cap_digits"), 254)),
        ("MDS cap", set_path(("fixed_template_theorem", "v_at_least_512_cap"), 2)),
        ("kappa", set_path(("fixed_template_theorem", "v_at_most_511_kappa"), "511-v")),
        ("packing formula", set_path(("fixed_template_theorem", "v_at_most_511_cap"), "ceil ratio")),
        ("basis size", set_path(("fixed_template_theorem", "free_module_basis_size"), 2_047)),
        ("high components", set_path(("fixed_template_theorem", "high_component_count"), 136)),
        ("high degree", set_path(("fixed_template_theorem", "high_component_degree_upper"), "510-v")),
        ("low components", set_path(("fixed_template_theorem", "low_component_count"), 1_912)),
        ("v511 zero", set_path(("fixed_template_theorem", "v_511_low_components_zero"), False)),
        ("intersection", set_path(("fixed_template_theorem", "pairwise_quotient_support_intersection_upper"), "512-v")),
        ("field generic", set_path(("fixed_template_theorem", "field_generic"), False)),
        ("degree Y gate", set_path(("cofactor_jet_bridge", "nonempty_family_forces_degree_Y_at_least_A"), False)),
        ("leading normalization", set_path(("cofactor_jet_bridge", "leading_normalization"), "H is monic")),
        ("reciprocal modulus", set_path(("cofactor_jet_bridge", "reciprocal_congruence"), "mod Z^(w+s)")),
        ("valuation", set_path(("cofactor_jet_bridge", "codeword_term_valuation_lower"), "w+s")),
        ("jet bijection", set_path(("cofactor_jet_bridge", "locator_and_normalized_cofactor_w_jets_bijective"), False)),
        ("fiber preservation", set_path(("cofactor_jet_bridge", "fiber_cardinalities_preserved"), False)),
        ("fixed unit", set_path(("cofactor_jet_bridge", "fixed_template_cancellation_uses_unit_L0_reciprocal"), False)),
        ("visible quotient", set_path(("cofactor_jet_bridge", "quotient_coefficients_visible"), "31")),
        ("general QR2 overclaim", set_path(("cofactor_jet_bridge", "general_fixed_template_claims_QR2_directly"), True)),
        ("zero padding", set_path(("cofactor_jet_bridge", "zero_padding_when_s_less_than_w"), False)),
        ("block count", set_path(("fifteen_target_construction", "block_count"), 14)),
        ("block size", set_path(("fifteen_target_construction", "block_size"), 32)),
        ("unused labels", set_path(("fifteen_target_construction", "unused_labels"), 16)),
        ("block digest", set_path(("fifteen_target_construction", "block_fixture_sha256"), "0" * 64)),
        ("duplicate sums", set_path(("fifteen_target_construction", "block_sums_pairwise_distinct"), False)),
        ("interpolation labels", set_path(("fifteen_target_construction", "interpolation_label_count"), 512)),
        ("codeword degree", set_path(("fifteen_target_construction", "codeword_degree"), K - 136)),
        ("center degree", set_path(("fifteen_target_construction", "center_degree_upper"), N - 136)),
        ("cofactor degree", set_path(("fifteen_target_construction", "cofactor_degree_upper"), RADIUS - 136)),
        ("support size", set_path(("fifteen_target_construction", "exact_support_size"), AGREEMENT - 1)),
        ("target floor", set_path(("fifteen_target_construction", "attained_quotient_locator_cofactor_targets_lower"), 14)),
        ("complete target overclaim", set_path(("fifteen_target_construction", "complete_ball_target_count_claimed"), True)),
        ("varying intersection", set_path(("varying_template_route_cut", "intersection_size"), 135_169)),
        ("varying gate", set_path(("varying_template_route_cut", "intersection_below_K"), False)),
        ("common template overclaim", set_path(("varying_template_route_cut", "same_profile_forces_common_template"), True)),
        ("global payment", set_path(("chronology", "global_profile_template_target_sum_paid"), True)),
        ("maximum fiber", set_path(("chronology", "maximum_prefix_fiber_is_sufficient"), True)),
        ("terminal", set_path(("chronology", "successor_terminal"), PARENT_TERMINAL)),
        ("owner paid", set_path(("chronology", "owner_paid"), True)),
        ("ledger", set_path(("scope", "ledger_movement"), 1)),
        ("row close", set_path(("scope", "deployed_row_closed"), True)),
        ("high interior", set_path(("nonclaims", "high_interior_paid"), True)),
        ("parent payload", set_path(("external_dependencies", "parent_payload_sha256"), "0" * 64)),
        ("source path", set_path(("source_bindings", 0, "path"), "experimental/WRONG.json")),
        ("source hash", set_path(("source_bindings", 1, "sha256"), "0" * 64)),
        ("source duplicate", set_path(("source_bindings", 1, "binding_id"),
                                      "M31_C2048_FIXED_TEMPLATE::packet_schema")),
    ]


def run_tamper_selftest() -> int:
    base = build_manifest()
    rejected = 0
    for label, mutate in mutation_cases():
        candidate = copy.deepcopy(base)
        mutate(candidate)
        candidate = seal(candidate)
        try:
            verify_payload(candidate, expected=base)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"semantic mutation accepted: {label}")

    malformed = [
        b'{"x":1,"x":2}\n',
        b'{"x":1.0}\n',
        b'{"x":NaN}\n',
        b'{"x":"\xff"}\n',
        b'{"x":1}',
    ]
    for raw in malformed:
        try:
            strict_json_bytes(raw, canonical=True)
        except (VerificationError, json.JSONDecodeError):
            rejected += 1
        else:
            raise VerificationError("malformed JSON accepted")
    total = len(mutation_cases()) + len(malformed)
    print(f"PASS: rejected {rejected}/{total} mutations; checks={CHECKS}")
    return 0


def run_check() -> int:
    candidate = strict_json_path(MANIFEST_PATH, canonical=True)
    require(type(candidate) is dict, "manifest root")
    expected = build_manifest()
    verify_payload(candidate, expected=expected)
    schema = strict_json_path(SCHEMA_PATH, canonical=True)
    validate_schema(schema, candidate)
    print("PASS: profiles=261192 budget-fitting=25767 "
          "fixed-targets=15 global-sum=OPEN checks=%d" % CHECKS)
    print(f"payload_sha256={candidate['payload_sha256']}")
    print(f"route_terminal={NEW_TERMINAL}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_artifacts()
            print(f"WROTE {SCHEMA_PATH}")
            print(f"WROTE {MANIFEST_PATH}")
            return 0
        if args.tamper_selftest:
            return run_tamper_selftest()
        return run_check()
    except (VerificationError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
