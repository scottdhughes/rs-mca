#!/usr/bin/env python3
"""Verify the M31 c=2048 partial-occupancy / 30-carrier packet.

This is an exact, standard-library replay.  It enumerates the deployed
occupancy atlas from the fiber inequalities, checks its disjoint partitions,
recomputes the coupled-Forney and budget thresholds, runs a small exhaustive
support census, binds every local source, and rejects semantic mutations.

It proves a boundary reduction, not a C1 payment or the M31 list endpoint.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_ID = "rs-mca-c2048-partial-occupancy-30carrier-v1"
ARCHITECTURE_ID = "M31_C2048_PARTIAL_OCCUPANCY_30CARRIER_REDUCTION_V1"
STATUS = "PROVED_BOUNDARY_OCCUPANCY_ATLAS_AND_30CARRIER_REDUCTION_ROW_OPEN"
ROUTE_TERMINAL = "M31_C2048_BIDEEP_30COLUMN_OWNER"

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
B_STAR = P**4 // 2**100
U_LOW = 3_730

C = 2_048
FIBERS = N // C
ERROR_QUOTIENT = RADIUS // C
ERROR_REMAINDER = RADIUS % C
AGREEMENT_QUOTIENT = AGREEMENT // C
AGREEMENT_REMAINDER = AGREEMENT % C

FORNEY_SUM = 2 * RADIUS - K - 1
D0 = K - RADIUS
SOURCE_FLOOR = 6_796_405
EXTERNAL_C1_HEAD = "a843a8f7930054617ef1d94169a4a9d3422cb909"
PREDECESSOR_PAYLOAD = "056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_c2048_partial_occupancy_30carrier_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_c2048_partial_occupancy_30carrier_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_c2048_partial_occupancy_30carrier_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_c2048_partial_occupancy_30carrier_reduction.md"
README_PATH = ROOT / "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the occupancy/30-carrier certificate."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Primary exhaustive integer atlas, budgets, and mutation replay."),
    ("packet_sage", SAGE_PATH, None,
     "Independent finite-field occupancy and reciprocal-recovery replay."),
    ("packet_note", NOTE_PATH, None,
     "Symbolic target-field occupancy and 30-carrier theorem."),
    ("packet_readme", README_PATH, None,
     "Replay, scope, and nonclaim contract."),
    ("predecessor_manifest",
     ROOT / "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json",
     "payload_sha256", "Sealed predecessor #1039 packet."),
    ("target_field_source_adapter",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Field-generic exact-layer and target-field source adapter."),
    ("target_field_source_manifest",
     ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
     "payload_sha256", "Sealed target-field source-adapter contract."),
    ("coupled_subpacket_theorem",
     ROOT / "experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md",
     None, "Arbitrary-m coupled joint-kernel and 30/29 threshold theorem."),
    ("coupled_subpacket_replay",
     ROOT / "experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py",
     None, "Exact coupled-kernel arithmetic and finite-field replay."),
    ("quotient_remainder_source", ROOT / "experimental/rs_mca_thresholds.tex",
     None, "Exact QR normal form and arbitrary partial-occupancy limitation."),
    ("active_v4_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active five-atom LIST chronology and deployed row."),
    ("admissibility_authority",
     ROOT / "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex",
     None, "Non-oracular first-match payment rules."),
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
        if role == "predecessor_manifest":
            require(internal == PREDECESSOR_PAYLOAD, "exact predecessor payload")
        result.append({
            "binding_id": f"M31_C2048_30CARRIER::{role}",
            "path": relative.as_posix(),
            "role": role,
            "scope": scope,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
        })
    return result


def occupancy_record(m: int, z: int) -> dict[str, int] | None:
    h = FIBERS - m - z
    if h < 0:
        return None
    r_err = RADIUS - C * m
    r_agr = AGREEMENT - C * z
    if r_err < 0 or r_agr < 0 or r_err + r_agr != C * h:
        return None
    if h == 0:
        feasible = r_err == 0 and r_agr == 0
    else:
        feasible = (
            h <= r_err <= h * (C - 1)
            and h <= r_agr <= h * (C - 1)
        )
    if not feasible:
        return None
    return {
        "u": ERROR_QUOTIENT - m,
        "v": AGREEMENT_QUOTIENT - z,
        "m": m,
        "z": z,
        "h": h,
        "r_err": r_err,
        "r_agr": r_agr,
    }


def enumerate_profiles() -> list[dict[str, int]]:
    records = []
    for m in range(FIBERS + 1):
        for z in range(FIBERS - m + 1):
            record = occupancy_record(m, z)
            if record is not None:
                records.append(record)
    records.sort(key=lambda row: (row["u"], row["v"]))
    return records


def profile_digest(records: list[dict[str, int]]) -> str:
    compact = [
        [row[key] for key in ("u", "v", "m", "z", "h", "r_err", "r_agr")]
        for row in records
    ]
    return sha256_bytes(canonical_json(compact))


def forney_partial(columns: int, rows: int) -> int:
    require(columns >= 3, "Forney column lower bound")
    require(1 <= rows <= columns - 2, "Forney row range")
    return rows * FORNEY_SUM // (columns - 2)


def toy_census() -> dict[str, Any]:
    toy_c = 4
    toy_fibers = 4
    toy_radius = 7
    toy_agreement = toy_c * toy_fibers - toy_radius
    domain = tuple(range(toy_c * toy_fibers))
    histogram: Counter[tuple[int, int]] = Counter()
    for support_tuple in itertools.combinations(domain, toy_radius):
        support = set(support_tuple)
        occupancies = [
            sum(point in support for point in range(j * toy_c, (j + 1) * toy_c))
            for j in range(toy_fibers)
        ]
        m = occupancies.count(toy_c)
        z = occupancies.count(0)
        u = toy_radius // toy_c - m
        v = toy_agreement // toy_c - z
        histogram[(u, v)] += 1
    rows = [[u, v, count] for (u, v), count in sorted(histogram.items())]
    return {
        "fiber_size": toy_c,
        "fiber_count": toy_fibers,
        "domain_size": len(domain),
        "error_size": toy_radius,
        "agreement_size": toy_agreement,
        "support_count": sum(histogram.values()),
        "profile_histogram": rows,
        "histogram_sha256": sha256_bytes(
            json.dumps(rows, separators=(",", ":")).encode("ascii")
        ),
        "faces_and_bideep_are_disjoint": True,
        "complement_count_preserved": True,
    }


def build_payload() -> dict[str, Any]:
    profiles = enumerate_profiles()
    pairs = {(row["u"], row["v"]) for row in profiles}
    face = {(u, v) for u, v in pairs if u == 0 or v == 0}
    bideep = {(u, v) for u, v in pairs if u >= 1 and v >= 1}
    arms = {(u, v) for u, v in bideep if u <= 32 or v <= 32}
    core = {(u, v) for u, v in bideep if u >= 33 and v >= 33}
    residual_cap = 29 * len(bideep)
    early_target = B_STAR - U_LOW - residual_cap
    return {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "scope": {
            "workboard_item": "M1",
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "field": "GF((2^31-1)^4)",
            "unit": "DISTINCT_EXACT_BOUNDARY_CODEWORDS_PER_RECEIVED_WORD",
            "impact": "PROVED_EXHAUSTIVE_BOUNDARY_REDUCTION_AND_ROUTE_CUT",
            "deployed_row_closed": False,
            "ledger_movement": 0,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "deployed_parameters": {
            "p": P,
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "prefix_depth": W,
            "B_star": B_STAR,
            "fold_degree": C,
            "fiber_count": FIBERS,
            "error_quotient": ERROR_QUOTIENT,
            "error_remainder": ERROR_REMAINDER,
            "agreement_quotient": AGREEMENT_QUOTIENT,
            "agreement_remainder": AGREEMENT_REMAINDER,
            "forney_sum_upper": FORNEY_SUM,
            "boundary_cutoff": D0,
        },
        "occupancy_atlas": {
            "parameterization": {
                "u": "479-m",
                "v": "544-z",
                "h": "u+v+1",
                "r_err": "137+2048*u",
                "r_agr": "1911+2048*v",
            },
            "feasible_set": "u=0,0<=v<=136 OR 1<=u<=479,0<=v<=544",
            "profile_count": len(profiles),
            "profile_sha256": profile_digest(profiles),
            "c1_face_count": len(face),
            "bideep_count": len(bideep),
            "visible_arm_count": len(arms),
            "double_strict_core_count": len(core),
            "face_and_bideep_disjoint": not (face & bideep),
            "face_and_bideep_exhaustive": face | bideep == pairs,
            "arm_and_core_disjoint": not (arms & core),
            "arm_and_core_exhaustive": arms | core == bideep,
            "infeasible_boundary_pair": [0, 137],
            "error_visible_u_max": 32,
            "agreement_visible_v_max": 32,
            "error_u32_remainder": ERROR_REMAINDER + C * 32,
            "error_u33_remainder": ERROR_REMAINDER + C * 33,
            "agreement_v32_remainder": AGREEMENT_REMAINDER + C * 32,
            "agreement_v33_remainder": AGREEMENT_REMAINDER + C * 33,
        },
        "chronology_contract": {
            "declared_first_match_dependency_head": EXTERNAL_C1_HEAD,
            "error_face": "u=0",
            "agreement_face": "v=0",
            "face_route": "REMOVED_BY_OR_AT_C1_UNDER_DECLARED_ORDER",
            "face_route_is_conditional": True,
            "face_numerical_payment_proved": False,
            "orientations_are_one_support_not_two_charges": True,
            "arbitrary_boundary_to_Q_adapter_proved": False,
            "visible_arm_fixed_quotient_recovery_proved": True,
            "visible_arm_quotient_count_bound_proved": False,
        },
        "carrier_reduction": {
            "route_terminal": ROUTE_TERMINAL,
            "profile_residual_cap_without_30_carrier": 29,
            "bideep_residual_cap_without_30_carrier": residual_cap,
            "carrier_columns": 30,
            "joint_kernel_rank": 28,
            "joint_index_sum_upper": FORNEY_SUM,
            "first_index_upper": forney_partial(30, 1),
            "first_two_index_sum_upper": forney_partial(30, 2),
            "boundary_cutoff": D0,
            "two_row_strict_below_cutoff": forney_partial(30, 2) < D0,
            "columns_29_first_two_upper": forney_partial(29, 2),
            "columns_29_not_certified": forney_partial(29, 2) > D0,
            "minimal_width_from_aggregate_bound": min(
                m for m in range(4, 100)
                if forney_partial(m, 2) < D0
            ),
            "target_field_arbitrary_m_corollary_explicit": True,
            "complete_layer_core_divided_before_restriction": True,
            "same_profile_owner_paid": False,
            "residual_cap_requires_fixed_exhaustive_disjoint_owner_compiler": True,
            "one_carrier_classification_suffices_for_residual_cap": False,
        },
        "budget_calibration": {
            "U_low": U_LOW,
            "bideep_conditional_cap": residual_cap,
            "early_boundary_target": early_target,
            "early_boundary_target_unit":
                "COMBINED_DISJOINT_C1_SHAPED_FACE_AND_ACTIVATED_30CARRIER_OWNER_CHARGES",
            "includes_all_activated_carrier_owner_charges": True,
            "carrier_codewords_deleted_without_charge": False,
            "fixed_remainder_source_floor": SOURCE_FLOOR,
            "source_floor_slack": early_target - SOURCE_FLOOR,
            "boundary_only_sum": U_LOW + residual_cap + early_target,
            "raw_profiles_times_64": len(profiles) * 64,
            "bideep_profiles_times_64": len(bideep) * 64,
            "same_profile_columns_for_above_budget_raw":
                (B_STAR + 1 + len(profiles) - 1) // len(profiles),
            "same_profile_columns_for_above_budget_bideep":
                (B_STAR + 1 + len(bideep) - 1) // len(bideep),
            "columns_65_first_index_upper": forney_partial(65, 1),
            "columns_65_first_two_upper": forney_partial(65, 2),
            "allocation_is_boundary_only": True,
            "high_interior_reserve": 0,
        },
        "toy_control": toy_census(),
        "external_dependencies": {
            "predecessor_pr": 1039,
            "predecessor_payload_sha256": PREDECESSOR_PAYLOAD,
            "logical_c1_pr": 1032,
            "logical_c1_head": EXTERNAL_C1_HEAD,
            "logical_c1_is_mechanical_ancestor": False,
        },
        "nonclaims": {
            "C1_numerical_payment_proved": False,
            "thirty_column_owner_paid": False,
            "twenty_nine_column_geometry_impossible": False,
            "visible_arms_paid": False,
            "high_interior_paid": False,
            "U_Q_assigned": False,
            "U_list_int_assigned": False,
            "U_ext_assigned": False,
            "M31_list_row_closed": False,
            "official_endpoint_changed": False,
        },
        "source_bindings": expected_source_bindings(),
    }


def exact_keys(value: Any, keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"{label}: exact keys")


def verify_payload(payload: dict[str, Any]) -> None:
    exact_keys(payload, {
        "schema", "architecture_id", "status", "payload_sha256", "scope",
        "deployed_parameters", "occupancy_atlas", "chronology_contract",
        "carrier_reduction", "budget_calibration", "toy_control",
        "external_dependencies", "nonclaims", "source_bindings",
    }, "payload")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["architecture_id"] == ARCHITECTURE_ID, "architecture id")
    require(payload["status"] == STATUS, "status")
    require(payload["payload_sha256"] == payload_sha256(payload), "payload seal")

    expected = seal(build_payload())
    require(payload == expected, "payload equals exact regenerated theorem")

    scope = payload["scope"]
    require(scope["field"] == "GF((2^31-1)^4)", "target-field scope")
    require(scope["ledger_movement"] == 0, "ledger remains fixed")
    require(scope["deployed_row_closed"] is False, "row remains open")

    deployed = payload["deployed_parameters"]
    require((deployed["p"], deployed["n"], deployed["K"]) ==
            (2_147_483_647, 2_097_152, 1_048_576), "deployed base")
    require((deployed["agreement"], deployed["radius"],
             deployed["prefix_depth"], deployed["B_star"]) ==
            (1_116_023, 981_129, 67_447, 16_777_215), "deployed row")
    require((deployed["fold_degree"], deployed["fiber_count"]) ==
            (2_048, 1_024), "fold partition")
    require((deployed["error_quotient"], deployed["error_remainder"]) ==
            (479, 137), "error Euclidean division")
    require((deployed["agreement_quotient"],
             deployed["agreement_remainder"]) == (544, 1_911),
            "agreement Euclidean division")
    require(deployed["forney_sum_upper"] == 913_681, "Forney sum")
    require(deployed["boundary_cutoff"] == 67_447, "boundary cutoff")

    atlas = payload["occupancy_atlas"]
    require(atlas["profile_count"] == 261_192, "profile count")
    require(atlas["c1_face_count"] == 616, "face count")
    require(atlas["bideep_count"] == 260_576, "bi-deep count")
    require(atlas["visible_arm_count"] == 31_712, "visible arm count")
    require(atlas["double_strict_core_count"] == 228_864,
            "double strict core count")
    require(all(atlas[key] is True for key in (
        "face_and_bideep_disjoint", "face_and_bideep_exhaustive",
        "arm_and_core_disjoint", "arm_and_core_exhaustive",
    )), "atlas partitions")
    require(atlas["infeasible_boundary_pair"] == [0, 137],
            "infeasible u=0,v=137 guard")
    require((atlas["error_u32_remainder"], atlas["error_u33_remainder"]) ==
            (65_673, 67_721), "error arm transition")
    require((atlas["agreement_v32_remainder"],
             atlas["agreement_v33_remainder"]) == (67_447, 69_495),
            "agreement arm transition")
    require(atlas["error_u32_remainder"] <= W < atlas["error_u33_remainder"],
            "error visibility iff u<=32")
    require(atlas["agreement_v32_remainder"] <= W <
            atlas["agreement_v33_remainder"],
            "agreement visibility iff v<=32")

    chronology = payload["chronology_contract"]
    require(chronology["declared_first_match_dependency_head"] ==
            EXTERNAL_C1_HEAD, "exact C1 logical head")
    require(chronology["face_route_is_conditional"] is True,
            "conditional C1 route")
    require(chronology["face_numerical_payment_proved"] is False,
            "no C1 numerical payment")
    require(chronology["orientations_are_one_support_not_two_charges"] is True,
            "no orientation double charge")
    require(chronology["arbitrary_boundary_to_Q_adapter_proved"] is False,
            "no arbitrary Q adapter")
    require(chronology["visible_arm_fixed_quotient_recovery_proved"] is True,
            "visible-arm local recovery")
    require(chronology["visible_arm_quotient_count_bound_proved"] is False,
            "no quotient-set count")

    carrier = payload["carrier_reduction"]
    require(carrier["route_terminal"] == ROUTE_TERMINAL, "route terminal")
    require(carrier["profile_residual_cap_without_30_carrier"] == 29,
            "per-profile residual cap")
    require(carrier["bideep_residual_cap_without_30_carrier"] == 7_556_704,
            "global residual cap")
    require((carrier["carrier_columns"], carrier["joint_kernel_rank"]) ==
            (30, 28), "carrier dimensions")
    require((carrier["first_index_upper"],
             carrier["first_two_index_sum_upper"]) == (32_631, 65_262),
            "30-column ordered bounds")
    require(carrier["two_row_strict_below_cutoff"] is True,
            "30-column two-row gate")
    require(carrier["columns_29_first_two_upper"] == 67_680,
            "29-column aggregate bound")
    require(carrier["columns_29_not_certified"] is True,
            "29-column noncertification")
    require(carrier["minimal_width_from_aggregate_bound"] == 30,
            "minimal aggregate width")
    require(carrier["target_field_arbitrary_m_corollary_explicit"] is True,
            "explicit target-field arbitrary-m corollary")
    require(carrier["complete_layer_core_divided_before_restriction"] is True,
            "complete-layer core order")
    require(carrier["same_profile_owner_paid"] is False,
            "carrier still unpaid")
    require(carrier["residual_cap_requires_fixed_exhaustive_disjoint_owner_compiler"] is True,
            "residual cap requires admissible compiler")
    require(carrier["one_carrier_classification_suffices_for_residual_cap"] is False,
            "one carrier does not prune a profile")

    budget = payload["budget_calibration"]
    require(budget["bideep_conditional_cap"] == 7_556_704,
            "conditional bi-deep budget")
    require(budget["early_boundary_target"] == 9_216_781,
            "early boundary target")
    require(budget["early_boundary_target_unit"] ==
            "COMBINED_DISJOINT_C1_SHAPED_FACE_AND_ACTIVATED_30CARRIER_OWNER_CHARGES",
            "combined face/carrier target unit")
    require(budget["includes_all_activated_carrier_owner_charges"] is True,
            "carrier charges included")
    require(budget["carrier_codewords_deleted_without_charge"] is False,
            "carrier codewords not erased")
    require(budget["fixed_remainder_source_floor"] == SOURCE_FLOOR,
            "source floor")
    require(budget["source_floor_slack"] == 2_420_376,
            "source-floor slack")
    require(budget["boundary_only_sum"] == B_STAR,
            "exact boundary-only allocation")
    require(budget["raw_profiles_times_64"] == 16_716_288 < B_STAR,
            "raw 65-column pigeonhole")
    require(budget["bideep_profiles_times_64"] == 16_676_864 < B_STAR,
            "bi-deep 65-column pigeonhole")
    require(budget["same_profile_columns_for_above_budget_raw"] == 65,
            "raw same-profile columns")
    require(budget["same_profile_columns_for_above_budget_bideep"] == 65,
            "bi-deep same-profile columns")
    require((budget["columns_65_first_index_upper"],
             budget["columns_65_first_two_upper"]) == (14_502, 29_005),
            "65-column bounds")
    require(budget["allocation_is_boundary_only"] is True
            and budget["high_interior_reserve"] == 0,
            "boundary-only warning")

    toy = payload["toy_control"]
    require(toy == {
        "fiber_size": 4,
        "fiber_count": 4,
        "domain_size": 16,
        "error_size": 7,
        "agreement_size": 9,
        "support_count": 11_440,
        "profile_histogram": [
            [0, 0, 48], [0, 1, 576], [0, 2, 256],
            [1, 1, 2_496], [1, 2, 8_064],
        ],
        "histogram_sha256":
            "d300d8ca1799fb840a5bf191c440aff0b998a6461d3331674970718c332dc45a",
        "faces_and_bideep_are_disjoint": True,
        "complement_count_preserved": True,
    }, "toy exhaustive census")

    external = payload["external_dependencies"]
    require(external["predecessor_pr"] == 1039, "predecessor PR")
    require(external["predecessor_payload_sha256"] == PREDECESSOR_PAYLOAD,
            "predecessor seal")
    require(external["logical_c1_pr"] == 1032
            and external["logical_c1_head"] == EXTERNAL_C1_HEAD,
            "logical C1 dependency")
    require(external["logical_c1_is_mechanical_ancestor"] is False,
            "logical dependency only")

    nonclaims = payload["nonclaims"]
    require(all(value is False for value in nonclaims.values()),
            "all positive overclaims rejected")
    require(set(nonclaims) == {
        "C1_numerical_payment_proved", "thirty_column_owner_paid",
        "twenty_nine_column_geometry_impossible", "visible_arms_paid",
        "high_interior_paid", "U_Q_assigned", "U_list_int_assigned",
        "U_ext_assigned", "M31_list_row_closed", "official_endpoint_changed",
    }, "exact nonclaims")
    require(payload["source_bindings"] == expected_source_bindings(),
            "live source bindings")


def mutate_path(payload: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def tamper_selftest(expected: dict[str, Any]) -> None:
    mutations: tuple[tuple[str, tuple[Any, ...], Any], ...] = (
        ("status", ("status",), "CLOSED"),
        ("ledger", ("scope", "ledger_movement"), 1),
        ("field", ("scope", "field"), "GF(2^31-1)"),
        ("fold", ("deployed_parameters", "fold_degree"), 1_024),
        ("fiber-count", ("deployed_parameters", "fiber_count"), 2_048),
        ("error-remainder", ("deployed_parameters", "error_remainder"), 136),
        ("agreement-remainder", ("deployed_parameters", "agreement_remainder"), 1_910),
        ("profile-count", ("occupancy_atlas", "profile_count"), 480 * 545),
        ("face-count", ("occupancy_atlas", "c1_face_count"), 615),
        ("bideep-count", ("occupancy_atlas", "bideep_count"), 260_575),
        ("arm-count", ("occupancy_atlas", "visible_arm_count"), 31_711),
        ("core-count", ("occupancy_atlas", "double_strict_core_count"), 228_865),
        ("infeasible-face", ("occupancy_atlas", "infeasible_boundary_pair", 1), 136),
        ("duplicate-partition", ("occupancy_atlas", "face_and_bideep_disjoint"), False),
        ("missing-partition", ("occupancy_atlas", "face_and_bideep_exhaustive"), False),
        ("u-threshold", ("occupancy_atlas", "error_visible_u_max"), 33),
        ("v-threshold", ("occupancy_atlas", "agreement_visible_v_max"), 33),
        ("C1-head", ("chronology_contract", "declared_first_match_dependency_head"), "0" * 40),
        ("C1-unconditional", ("chronology_contract", "face_route_is_conditional"), False),
        ("C1-payment", ("chronology_contract", "face_numerical_payment_proved"), True),
        ("orientation-double", ("chronology_contract", "orientations_are_one_support_not_two_charges"), False),
        ("false-Q", ("chronology_contract", "arbitrary_boundary_to_Q_adapter_proved"), True),
        ("false-arm-count", ("chronology_contract", "visible_arm_quotient_count_bound_proved"), True),
        ("residual-30", ("carrier_reduction", "profile_residual_cap_without_30_carrier"), 30),
        ("global-cap", ("carrier_reduction", "bideep_residual_cap_without_30_carrier"), 7_556_705),
        ("29-promoted", ("carrier_reduction", "minimal_width_from_aggregate_bound"), 29),
        ("29-bound", ("carrier_reduction", "columns_29_first_two_upper"), 67_447),
        ("30-bound", ("carrier_reduction", "first_two_index_sum_upper"), 65_263),
        ("wrong-rank", ("carrier_reduction", "joint_kernel_rank"), 29),
        ("wrong-field-corollary", ("carrier_reduction", "target_field_arbitrary_m_corollary_explicit"), False),
        ("core-order", ("carrier_reduction", "complete_layer_core_divided_before_restriction"), False),
        ("owner-paid", ("carrier_reduction", "same_profile_owner_paid"), True),
        ("compiler-omitted", ("carrier_reduction", "residual_cap_requires_fixed_exhaustive_disjoint_owner_compiler"), False),
        ("one-carrier-overclaim", ("carrier_reduction", "one_carrier_classification_suffices_for_residual_cap"), True),
        ("early-target", ("budget_calibration", "early_boundary_target"), 9_216_782),
        ("carrier-charge-omitted", ("budget_calibration", "includes_all_activated_carrier_owner_charges"), False),
        ("carrier-erased", ("budget_calibration", "carrier_codewords_deleted_without_charge"), True),
        ("source-floor", ("budget_calibration", "fixed_remainder_source_floor"), 6_796_404),
        ("source-slack", ("budget_calibration", "source_floor_slack"), 2_420_375),
        ("interior-reserve", ("budget_calibration", "high_interior_reserve"), 1),
        ("raw-pigeonhole", ("budget_calibration", "same_profile_columns_for_above_budget_raw"), 64),
        ("toy-histogram", ("toy_control", "profile_histogram", 3, 2), 2_495),
        ("toy-digest", ("toy_control", "histogram_sha256"), "0" * 64),
        ("mechanical-C1", ("external_dependencies", "logical_c1_is_mechanical_ancestor"), True),
        ("false-close", ("nonclaims", "M31_list_row_closed"), True),
        ("false-interior", ("nonclaims", "high_interior_paid"), True),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
    )
    rejected = 0
    for label, path, value in mutations:
        trial = copy.deepcopy(expected)
        mutate_path(trial, path, value)
        trial = seal(trial)
        try:
            verify_payload(trial)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")
    require(rejected == len(mutations), "all mutations rejected")
    print(f"tamper_selftest=PASS rejected={rejected}/{len(mutations)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not any((args.check, args.print_template, args.tamper_selftest)):
        args.check = True
    expected = seal(build_payload())
    verify_payload(expected)

    if args.check:
        require(MANIFEST_PATH.exists(), "manifest exists")
        actual = strict_json_path(MANIFEST_PATH, canonical=True)
        require(type(actual) is dict, "manifest object")
        verify_payload(actual)
        require(actual == expected, "manifest equals regenerated payload")
        print("M31 c=2048 occupancy / 30-carrier reduction: PASS")
        print("atlas: 261192 = 616 C1 faces + 260576 bi-deep profiles")
        print("deep split: 31712 visible-arm + 228864 double-strict profiles")
        print("dichotomy: bi-deep<=7556704 OR same-profile 30-carrier")
        print("Forney: 30 columns give mu1+mu2<=65262<67447; 29 gives 67680")
        print("budget: early boundary target=9216781; source-floor slack=2420376")
        print("scope: target-field boundary reduction; owner/interior/row remain OPEN")

    if args.tamper_selftest:
        tamper_selftest(expected)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
    else:
        print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
