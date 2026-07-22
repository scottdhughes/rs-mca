#!/usr/bin/env python3
"""Exact verifier for the M31 c=2048 65-column fixed-anchor route cut.

This packet compiles the whole exact-boundary c=2048 occupancy atlas at the
actual LIST budget.  It proves that a boundary excess forces one 65-codeword
same-profile packet, extracts the strongest cumulative Forney-index ladder
available on those 65 columns, and records the exact collision-avoidance
barrier at that same width.  It also recomputes the predecessor's deployed
source floors and proves that 65-column packets are genuinely populated.

The result is a boundary-owner interface and a route cut.  It is not a
chronology-valid payment and does not close the M31 LIST row.
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


SCHEMA_ID = "rs-mca-c2048-65column-fixed-anchor-route-cut-v1"
ARCHITECTURE_ID = "M31_C2048_65COLUMN_FIXED_ANCHOR_BOUNDARY_ROUTE_CUT_V1"
STATUS = "PROVED_65COLUMN_FIXED_ANCHOR_AND_COLLISION_ROUTE_CUT_ROW_OPEN"
PARENT_TERMINAL = "M31_C2048_FIXED_SYNDROME_MULTIPREFIX_FACE_CARRIER_OWNER"
NEW_TERMINAL = "M31_C2048_65COLUMN_FIXED_ANCHOR_OWNER"

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
B_STAR = P**4 // 2**100
TARGET_FIELD_SIZE = P**4
U_PAID = 3_730
COMBINED_FACE_CARRIER_ALLOWANCE = 9_216_781

C = 2_048
FIBERS = N // C
ERROR_QUOTIENT = RADIUS // C
ERROR_REMAINDER = RADIUS % C
AGREEMENT_QUOTIENT = AGREEMENT // C
AGREEMENT_REMAINDER = AGREEMENT % C
QUOTIENT_PREFIX_DEPTH = W // C
PROFILE_COUNT = 261_192

INDEX_SUM_UPPER = 2 * RADIUS - K - 1
CARRIER_WIDTH = 65
KERNEL_RANK = CARRIER_WIDTH - 2
MAX_PROFILE_CAP = CARRIER_WIDTH - 1

PARENT_PAYLOAD = "dacb9136f5818a5f86d9ca8987fbe4d361a57a70ebb490eac50dfc3822e062e4"
UPSTREAM_MAIN = "32a41660e3088eeeb15a16645330856794302ff0"
PARENT_HEAD = "752872ce98754a05f37540cd7780a89b86818222"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_c2048_65column_fixed_anchor_route_cut_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_c2048_65column_fixed_anchor_route_cut_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_c2048_65column_fixed_anchor_boundary_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-c2048-65column-fixed-anchor-route-cut-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-c2048-65column-fixed-anchor-route-cut-v1/manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the 65-column fixed-anchor certificate."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Primary exact atlas, index-envelope, source-floor, and mutation replay."),
    ("packet_sage", SAGE_PATH, None,
     "Independent exact arithmetic and polynomial fixed-anchor replay."),
    ("packet_note", NOTE_PATH, None,
     "Symbolic boundary trigger, fixed-anchor theorem, and route cut."),
    ("packet_readme", README_PATH, None,
     "Replay, dependency, and nonclaim contract."),
    ("parent_1041_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json",
     "payload_sha256", "Sealed immediate predecessor #1041 packet."),
    ("occupancy_30carrier_source",
     ROOT / "experimental/notes/thresholds/m31_c2048_partial_occupancy_30carrier_reduction.md",
     None, "Complete c=2048 profile atlas and arbitrary-subpacket theorem."),
    ("coupled_forney_source",
     ROOT / "experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md",
     None, "Joint-kernel indices, Plucker minors, and proper-hyperplane avoidance theorem."),
    ("target_field_source_adapter",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Target-field exact-layer source and active five-atom chronology."),
    ("active_v4_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active nonnegative LIST chronology and exact target budget."),
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


def ceil_div(a: int, b: int) -> int:
    require(type(a) is int and type(b) is int and a >= 0 and b > 0,
            "ceil-div domain")
    return (a + b - 1) // b


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
        if role == "parent_1041_manifest":
            require(internal == PARENT_PAYLOAD, "exact #1041 payload")
        result.append({
            "binding_id": f"M31_C2048_65ANCHOR::{role}",
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
            r_err = ERROR_REMAINDER + C * u
            r_agr = AGREEMENT_REMAINDER + C * v
            require(r_err + r_agr == C * h, "profile color sum")
            require(h <= r_err <= h * (C - 1), "profile error feasibility")
            require(h <= r_agr <= h * (C - 1), "profile agreement feasibility")
            profiles.append((u, v))
    require(len(profiles) == PROFILE_COUNT, "profile count")
    require(len(set(profiles)) == PROFILE_COUNT, "profile uniqueness")
    return profiles


def profile_source_floor(u: int, v: int) -> tuple[int, ...]:
    h = u + v + 1
    f = AGREEMENT_QUOTIENT - v
    r = AGREEMENT_REMAINDER + C * v
    available = FIBERS - h
    t = min(QUOTIENT_PREFIX_DEPTH, f)
    require(r + C * f == AGREEMENT, "source agreement size")
    require(0 <= f <= available, "source quotient availability")
    require(h <= r <= h * (C - 1), "source partial template")
    candidates = math.comb(available, f)
    floor = ceil_div(candidates, P**t)
    if t < f:
        degree_bound = r + C * (f - t - 1)
        require(degree_bound == AGREEMENT - C * (t + 1),
                "source degree cancellation")
        require(degree_bound < K, "source codeword degree")
    else:
        degree_bound = -1
        require(floor == 1, "full coefficient bucket singleton")
    return (u, v, h, f, r, available, t, degree_bound, candidates, floor)


def source_floor_census() -> dict[str, Any]:
    digest = hashlib.sha256()
    activated_36: list[tuple[int, ...]] = []
    activated: list[tuple[int, ...]] = []
    for u, v in feasible_profiles():
        row = profile_source_floor(u, v)
        digest.update((",".join(str(x) for x in row) + "\n").encode("ascii"))
        if row[-1] >= 36:
            activated_36.append(row)
        if row[-1] >= CARRIER_WIDTH:
            activated.append(row)
    faces_36 = [row for row in activated_36
                if row[0] == 0 or row[1] == 0]
    bideep_36 = [row for row in activated_36
                 if row[0] >= 1 and row[1] >= 1]
    faces = [row for row in activated if row[0] == 0 or row[1] == 0]
    bideep = [row for row in activated if row[0] >= 1 and row[1] >= 1]
    require(len(activated) == 156, "source floor-65 total")
    require(len(faces) == 34, "source floor-65 faces")
    require(len(bideep) == 122, "source floor-65 bi-deep")
    require((len(activated_36), len(faces_36), len(bideep_36)) ==
            (172, 35, 137), "source floor-36 census")
    global_max = max(activated, key=lambda row: row[-1])
    bideep_max = max(bideep, key=lambda row: row[-1])
    require((global_max[0], global_max[1], global_max[-1]) ==
            (0, 0, 6_796_405), "global source maximum")
    require((bideep_max[0], bideep_max[1], bideep_max[-1]) ==
            (1, 1, 1_693_898), "bi-deep source maximum")

    frontier = []
    for u in sorted({row[0] for row in bideep}):
        rows = [row for row in bideep if row[0] == u]
        last = max(rows, key=lambda row: row[1])
        frontier.append({"u": u, "max_v": last[1],
                         "floor_at_max_v": last[-1]})
    expected = [
        (1, 16, 120), (2, 15, 108), (3, 14, 97), (4, 13, 87),
        (5, 12, 78), (6, 11, 69), (7, 9, 115), (8, 8, 102),
        (9, 7, 89), (10, 6, 78), (11, 5, 68), (12, 3, 109),
        (13, 2, 94), (14, 1, 81),
    ]
    require([(x["u"], x["max_v"], x["floor_at_max_v"])
             for x in frontier] == expected, "source floor-65 frontier")
    return {
        "formula": "ceil(binomial(1023-u-v,544-v)/p^min(32,544-v))",
        "profile_rows_sha256": digest.hexdigest(),
        "profiles_with_floor_at_least_65": len(activated),
        "face_profiles_with_floor_at_least_65": len(faces),
        "bideep_profiles_with_floor_at_least_65": len(bideep),
        "profiles_with_floor_at_least_36": len(activated_36),
        "face_profiles_with_floor_at_least_36": len(faces_36),
        "bideep_profiles_with_floor_at_least_36": len(bideep_36),
        "global_maximum": {"u": 0, "v": 0, "source_floor": 6_796_405},
        "bideep_maximum": {"u": 1, "v": 1, "source_floor": 1_693_898},
        "bideep_frontier": frontier,
        "one_received_word_per_profile": True,
        "different_profiles_simultaneously_attained": False,
        "complete_target_field_ball_boundary_only": True,
        "complete_target_field_ball_base_field_valued": True,
        "universal_profile_cap_64_false": True,
        "carrier_nonexistence_route_false": True,
    }


def cumulative_index_envelope() -> dict[str, Any]:
    quotient, remainder = divmod(INDEX_SUM_UPPER, KERNEL_RANK)
    require((quotient, remainder) == (14_502, 55),
            "index-sum Euclidean division")

    def maximum_prefix_sum(m: int) -> int:
        """Sharp maximum of the first m nondecreasing indices.

        If the m-th index is t, the prefix is at most both m*t and
        S-(r-m)*t.  Their integer maximum occurs at floor(S/r) or one
        larger.  This is attained by the balanced index sequence.
        """
        require(1 <= m <= KERNEL_RANK, "prefix-sum width")
        balanced = m * quotient + max(0, m - (KERNEL_RANK - remainder))
        candidates = []
        for t in (quotient, quotient + 1):
            candidates.append(min(m * t,
                                  INDEX_SUM_UPPER - (KERNEL_RANK - m) * t))
        require(balanced == max(candidates), "sharp prefix-sum optimizer")
        return balanced

    envelope = []
    for m in range(1, 5):
        degree = maximum_prefix_sum(m)
        residual_roots = W + 1 - degree
        nonanchor_columns = CARRIER_WIDTH - m
        require(degree < W + 1, f"fixed {m}-anchor degree")
        require(residual_roots > 0, f"fixed {m}-anchor roots")
        envelope.append({
            "anchor_rank": m,
            "cumulative_index_upper": degree,
            "global_exceptional_domain_points_upper": degree,
            "nonanchor_columns": nonanchor_columns,
            "variable_roots_per_nonanchor_column_lower": residual_roots,
            "rooted_nonanchor_incidence_lower":
                nonanchor_columns * residual_roots,
        })
    require([row["cumulative_index_upper"] for row in envelope] ==
            [14_502, 29_004, 43_506, 58_008], "index ladder envelope")
    require([row["rooted_nonanchor_incidence_lower"] for row in envelope] ==
            [3_388_544, 2_421_972, 1_484_404, 575_840],
            "fixed-anchor incidence ladder")

    low_row_index = 50
    low_row_upper = INDEX_SUM_UPPER // (KERNEL_RANK - low_row_index + 1)
    require(low_row_upper == 65_262 < W, "fifty low rows")
    witness = [0] * 50 + [W + 1] * 13
    require(len(witness) == KERNEL_RANK, "sharp sequence length")
    require(sum(witness) == 876_824 <= INDEX_SUM_UPPER,
            "sharp sequence sum")
    require(sum(1 for x in witness if x <= W) == 50,
            "no fifty-first row from aggregate data")
    syzygy_space_dimension = KERNEL_RANK * (W + 1) - INDEX_SUM_UPPER
    require(syzygy_space_dimension == 3_335_543,
            "low-degree syzygy-space dimension")
    return {
        "joint_index_sum_upper": INDEX_SUM_UPPER,
        "kernel_rank": KERNEL_RANK,
        "cutoff": W,
        "guaranteed_rows_at_or_below_cutoff": 50,
        "fiftieth_row_degree_upper": low_row_upper,
        "coupled_syzygy_F_space_dimension_lower_at_cutoff":
            syzygy_space_dimension,
        "sharp_prefix_sum_quotient": quotient,
        "sharp_prefix_sum_remainder": remainder,
        "fifty_first_row_not_forced_by_sum_alone": True,
        "sharp_abstract_index_sequence": witness,
        "fixed_anchor_ladder": envelope,
        "anchor_selection": "basis_relative_existence_from_first_m_degree_ordered_rows_after_arbitrary_column_labeling",
        "anchor_selection_is_canonical_owner_predicate": False,
        "anchor_ladder_is_nested": False,
        "gcd_of_all_maximal_anchor_minors_is_one": True,
        "anchor_minor_nonzero": True,
        "minimum_reduced_locator_degree": W + 1,
        "minimum_reduced_locator_degree_reason": "pairwise_MDS_union_and_true_common_core",
    }


def collision_avoidance() -> dict[str, Any]:
    def forbidden_count(width: int) -> int:
        return width * RADIUS + math.comb(width, 2) * INDEX_SUM_UPPER

    forbidden = forbidden_count(CARRIER_WIDTH)
    margin = TARGET_FIELD_SIZE - forbidden
    require(forbidden == 1_964_229_865, "65-column forbidden hyperplanes")
    require(margin ==
            21_267_647_892_944_572_736_998_860_267_723_701_016 > 0,
            "65-column target-field avoidance margin")
    budget_width = B_STAR + 1
    budget_forbidden = forbidden_count(budget_width)
    budget_margin = TARGET_FIELD_SIZE - budget_forbidden
    require(budget_forbidden == 128_589_177_894_085_853_184,
            "budget-width forbidden hyperplanes")
    require(budget_margin ==
            21_267_647_892_944_572_608_409_682_375_602_077_697 > 0,
            "budget-width target-field margin")

    lo, hi = 0, 10**17
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if forbidden_count(mid) < TARGET_FIELD_SIZE:
            lo = mid
        else:
            hi = mid
    require((lo, hi) == (6_823_032_369_902_110, 6_823_032_369_902_111),
            "target-field union-bound endpoint")
    require(forbidden_count(lo) < TARGET_FIELD_SIZE <= forbidden_count(hi),
            "target-field endpoint inequalities")
    return {
        "carrier_width": CARRIER_WIDTH,
        "escape_and_collision_hyperplanes_upper": forbidden,
        "coefficient_field": "GF((2^31-1)^4)",
        "field_size": TARGET_FIELD_SIZE,
        "avoidance_margin": margin,
        "avoidance_theorem_applies_if_each_form_is_proper": True,
        "actual_packet_escape_forms_are_proper_by_exactness": True,
        "exhaustive_dichotomy": {
            "case_I": "some_pair_collision_form_vanishes_identically_on_the_complete_containment_space",
            "case_II": "every_pair_collision_form_is_proper_and_an_exact_collision_free_prescribed_packet_functional_exists",
            "forced_component_owner_in_case_I_paid": False,
            "case_II_preserves_prescribed_supports_and_exactness": True,
            "case_II_preserves_complete_exact_layer": False,
        },
        "prescribed_packet_exact_and_collision_free_functional_exists_under_properness": True,
        "additional_complete_layer_supports_excluded": False,
        "forced_identically_zero_form_excluded": False,
        "full_layer_collision_owner_proved": False,
        "budget_violation_packet_width": budget_width,
        "budget_violation_packet_hyperplanes_upper": budget_forbidden,
        "budget_violation_packet_avoidance_margin": budget_margin,
        "maximum_width_certified_by_target_field_union_bound": lo,
        "first_width_not_certified_by_target_field_union_bound": hi,
        "prime_field_67_68_endpoint_transferred": False,
        "route_cut": "every_budget_sized_target_field_packet_with_only_proper_forms_admits_an_exact_collision_free_deformation",
    }


def combined_gate_trigger() -> dict[str, Any]:
    capped = 35 * PROFILE_COUNT
    slack = COMBINED_FACE_CARRIER_ALLOWANCE - capped
    forced_width = ceil_div(COMBINED_FACE_CARRIER_ALLOWANCE + 1,
                            PROFILE_COUNT)
    require(capped == 9_141_720, "35-per-profile combined cap")
    require(slack == 75_061 > 0, "combined gate slack")
    require(forced_width == 36, "combined gate width")

    rank = forced_width - 2
    quotient, remainder = divmod(INDEX_SUM_UPPER, rank)
    require((quotient, remainder) == (26_872, 33),
            "width-36 index division")
    prefix = [
        m * quotient + max(0, m - (rank - remainder))
        for m in (1, 2)
    ]
    require(prefix == [26_872, 53_745], "width-36 prefix envelope")
    guaranteed_low_rows = rank - INDEX_SUM_UPPER // (W + 1)
    require(guaranteed_low_rows == 21, "width-36 low rows")
    dimension = rank * (W + 1) - INDEX_SUM_UPPER
    require(dimension == 1_379_551, "width-36 syzygy dimension")
    anchor_incidences = [
        (forced_width - m) * (W + 1 - degree)
        for m, degree in enumerate(prefix, start=1)
    ]
    require(anchor_incidences == [1_420_160, 465_902],
            "width-36 anchor incidences")
    forbidden = forced_width * RADIUS + math.comb(forced_width, 2) * INDEX_SUM_UPPER
    require(forbidden == 610_939_674, "width-36 forbidden hyperplanes")
    require(TARGET_FIELD_SIZE - forbidden ==
            21_267_647_892_944_572_736_998_860_269_076_991_207 > 0,
            "width-36 avoidance margin")
    return {
        "allowance": COMBINED_FACE_CARRIER_ALLOWANCE,
        "per_profile_cap_if_no_trigger": 35,
        "capped_charge": capped,
        "slack": slack,
        "forced_same_profile_width_if_charge_exceeds_allowance": forced_width,
        "kernel_rank": rank,
        "first_index_upper": prefix[0],
        "first_two_indices_sum_upper": prefix[1],
        "guaranteed_rows_at_or_below_cutoff": guaranteed_low_rows,
        "cutoff_syzygy_F_space_dimension_lower": dimension,
        "fixed_anchor_rooted_incidence_lower_rank_1_and_2": anchor_incidences,
        "collision_avoidance_hyperplanes_upper": forbidden,
        "collision_avoidance_margin": TARGET_FIELD_SIZE - forbidden,
        "inside_target_field_budget_sized_nonforcing_range": True,
    }


def core_payload() -> dict[str, Any]:
    boundary_cap = MAX_PROFILE_CAP * PROFILE_COUNT
    total_cap = U_PAID + boundary_cap
    slack = B_STAR - total_cap
    boundary_violation_floor = B_STAR - U_PAID + 1
    require(B_STAR == 16_777_215, "deployed B star")
    require(boundary_cap == 16_716_288, "64-per-profile boundary cap")
    require(total_cap == 16_720_018, "low plus boundary cap")
    require(slack == 57_197 > 0, "boundary closure slack")
    require(boundary_violation_floor == 16_773_486, "boundary violation floor")
    require(ceil_div(boundary_violation_floor, PROFILE_COUNT) == CARRIER_WIDTH,
            "65-column trigger")
    require(INDEX_SUM_UPPER == 913_681, "joint index upper")

    return {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "scope": {
            "workboard_item": "M1",
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "field": "GF((2^31-1)^4) with sources over GF(2^31-1)",
            "unit": "DISTINCT_EXACT_BOUNDARY_CODEWORDS_PER_RECEIVED_WORD",
            "impact": "WHOLE_EXACT_BOUNDARY_65_TRIGGER_AND_FIXED_ANCHOR_ROUTE_CUT",
            "ledger_movement": 0,
            "deployed_row_closed": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "deployed_parameters": {
            "p": P, "n": N, "K": K, "agreement": AGREEMENT,
            "radius": RADIUS, "boundary_cutoff": W, "B_star": B_STAR,
            "fold_degree": C, "fiber_count": FIBERS,
            "profile_count": PROFILE_COUNT, "U_paid": U_PAID,
        },
        "whole_boundary_trigger": {
            "profile_count": PROFILE_COUNT,
            "per_profile_cap_if_no_carrier": MAX_PROFILE_CAP,
            "boundary_cap_if_no_carrier": boundary_cap,
            "low_plus_boundary_cap_if_no_carrier": total_cap,
            "slack_below_B_star": slack,
            "boundary_mass_floor_under_row_violation": boundary_violation_floor,
            "forced_same_profile_packet_width": CARRIER_WIDTH,
            "includes_C1_shaped_faces": True,
            "includes_bideep_profiles": True,
            "high_interior_included": False,
            "conditional_statement": "if_U_paid_plus_exact_boundary_exceeds_B_star_then_one_profile_has_at_least_65_codewords",
        },
        "combined_face_carrier_gate": combined_gate_trigger(),
        "fixed_anchor_theorem": cumulative_index_envelope(),
        "source_nonemptiness": source_floor_census(),
        "collision_route_cut": collision_avoidance(),
        "chronology": {
            "parent_terminal": PARENT_TERMINAL,
            "successor_terminal": NEW_TERMINAL,
            "parent_atom": "U_new",
            "parent_cell": "HIGH_BOUNDARY_EXACT_CODEWORD",
            "owner_paid": False,
            "active_partition_replaced": False,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "high_U_new": None,
            "high_interior_paid": False,
        },
        "external_dependencies": {
            "mechanical_parent": f"PR #1041 exact head {PARENT_HEAD}",
            "parent_payload_sha256": PARENT_PAYLOAD,
            "upstream_main_at_preparation": UPSTREAM_MAIN,
            "open_PR_newer_than_parent_found": False,
            "rebase_needed_at_preparation": False,
        },
        "nonclaims": {
            "M31_list_row_closed": False,
            "exact_boundary_paid": False,
            "fixed_anchor_is_existing_v4_owner": False,
            "65_column_carrier_impossible": False,
            "universal_profile_cap_64": False,
            "collision_forced": False,
            "forced_component_classified": False,
            "full_layer_exhaustion_from_prescribed_packet": False,
            "attained_prefix_sum_bounded": False,
            "high_interior_bound_proved": False,
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
        "title": "M31 c=2048 65-column fixed-anchor route-cut certificate",
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
        ("profile count", set_path(("whole_boundary_trigger", "profile_count"), PROFILE_COUNT - 1)),
        ("profile cap", set_path(("whole_boundary_trigger", "per_profile_cap_if_no_carrier"), 65)),
        ("boundary cap", set_path(("whole_boundary_trigger", "boundary_cap_if_no_carrier"), 16_716_287)),
        ("trigger slack", set_path(("whole_boundary_trigger", "slack_below_B_star"), 57_196)),
        ("carrier width", set_path(("whole_boundary_trigger", "forced_same_profile_packet_width"), 64)),
        ("face omission", set_path(("whole_boundary_trigger", "includes_C1_shaped_faces"), False)),
        ("interior overclaim", set_path(("whole_boundary_trigger", "high_interior_included"), True)),
        ("combined allowance", set_path(("combined_face_carrier_gate", "allowance"), 9_216_780)),
        ("combined trigger", set_path(("combined_face_carrier_gate", "forced_same_profile_width_if_charge_exceeds_allowance"), 35)),
        ("combined anchor", set_path(("combined_face_carrier_gate", "first_two_indices_sum_upper"), 53_746)),
        ("combined nonforcing", set_path(("combined_face_carrier_gate", "inside_target_field_budget_sized_nonforcing_range"), False)),
        ("index sum", set_path(("fixed_anchor_theorem", "joint_index_sum_upper"), INDEX_SUM_UPPER - 1)),
        ("kernel rank", set_path(("fixed_anchor_theorem", "kernel_rank"), 62)),
        ("low rows", set_path(("fixed_anchor_theorem", "guaranteed_rows_at_or_below_cutoff"), 51)),
        ("row 50", set_path(("fixed_anchor_theorem", "fiftieth_row_degree_upper"), W)),
        ("row 51 overclaim", set_path(("fixed_anchor_theorem", "fifty_first_row_not_forced_by_sum_alone"), False)),
        ("sharp sequence", set_path(("fixed_anchor_theorem", "sharp_abstract_index_sequence"), [0] * 63)),
        ("anchor overclaim", set_path(("fixed_anchor_theorem", "anchor_selection_is_canonical_owner_predicate"), True)),
        ("nested overclaim", set_path(("fixed_anchor_theorem", "anchor_ladder_is_nested"), True)),
        ("anchor gcd", set_path(("fixed_anchor_theorem", "gcd_of_all_maximal_anchor_minors_is_one"), False)),
        ("minimum locator degree", set_path(("fixed_anchor_theorem", "minimum_reduced_locator_degree"), W)),
        ("one-anchor degree", set_path(("fixed_anchor_theorem", "fixed_anchor_ladder", 0, "cumulative_index_upper"), 14_503)),
        ("syzygy dimension", set_path(("fixed_anchor_theorem", "coupled_syzygy_F_space_dimension_lower_at_cutoff"), 3_335_542)),
        ("two-anchor degree", set_path(("fixed_anchor_theorem", "fixed_anchor_ladder", 1, "cumulative_index_upper"), 29_005)),
        ("two-anchor incidence", set_path(("fixed_anchor_theorem", "fixed_anchor_ladder", 1, "rooted_nonanchor_incidence_lower"), 2_421_971)),
        ("four-anchor degree", set_path(("fixed_anchor_theorem", "fixed_anchor_ladder", 3, "cumulative_index_upper"), 58_009)),
        ("source total", set_path(("source_nonemptiness", "profiles_with_floor_at_least_65"), 155)),
        ("source width36", set_path(("source_nonemptiness", "profiles_with_floor_at_least_36"), 171)),
        ("source faces", set_path(("source_nonemptiness", "face_profiles_with_floor_at_least_65"), 33)),
        ("source bi-deep", set_path(("source_nonemptiness", "bideep_profiles_with_floor_at_least_65"), 121)),
        ("source digest", set_path(("source_nonemptiness", "profile_rows_sha256"), "0" * 64)),
        ("cap64 false", set_path(("source_nonemptiness", "universal_profile_cap_64_false"), False)),
        ("simultaneous source", set_path(("source_nonemptiness", "different_profiles_simultaneously_attained"), True)),
        ("hyperplanes", set_path(("collision_route_cut", "escape_and_collision_hyperplanes_upper"), 1_964_229_864)),
        ("avoidance margin", set_path(("collision_route_cut", "avoidance_margin"), 183_253_781)),
        ("properness", set_path(("collision_route_cut", "avoidance_theorem_applies_if_each_form_is_proper"), False)),
        ("escape properness", set_path(("collision_route_cut", "actual_packet_escape_forms_are_proper_by_exactness"), False)),
        ("dichotomy", set_path(("collision_route_cut", "exhaustive_dichotomy", "case_II_preserves_complete_exact_layer"), True)),
        ("collision overclaim", set_path(("collision_route_cut", "full_layer_collision_owner_proved"), True)),
        ("extra supports overclaim", set_path(("collision_route_cut", "additional_complete_layer_supports_excluded"), True)),
        ("forced form overclaim", set_path(("collision_route_cut", "forced_identically_zero_form_excluded"), True)),
        ("target field", set_path(("collision_route_cut", "field_size"), P)),
        ("budget range", set_path(("collision_route_cut", "maximum_width_certified_by_target_field_union_bound"), 67)),
        ("prime endpoint", set_path(("collision_route_cut", "prime_field_67_68_endpoint_transferred"), True)),
        ("terminal", set_path(("chronology", "successor_terminal"), PARENT_TERMINAL)),
        ("owner paid", set_path(("chronology", "owner_paid"), True)),
        ("partition", set_path(("chronology", "active_partition_replaced"), True)),
        ("ledger", set_path(("scope", "ledger_movement"), 1)),
        ("row close", set_path(("scope", "deployed_row_closed"), True)),
        ("boundary paid", set_path(("nonclaims", "exact_boundary_paid"), True)),
        ("parent payload", set_path(("external_dependencies", "parent_payload_sha256"), "0" * 64)),
        ("source path", set_path(("source_bindings", 0, "path"), "experimental/WRONG.json")),
        ("source hash", set_path(("source_bindings", 1, "sha256"), "0" * 64)),
        ("source duplicate", set_path(("source_bindings", 1, "binding_id"), "M31_C2048_65ANCHOR::packet_schema")),
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
    print("PASS: boundary-trigger=65 profiles=261192 floor65=156 "
          "anchor2=29004 low_rows=50 checks=%d" % CHECKS)
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
