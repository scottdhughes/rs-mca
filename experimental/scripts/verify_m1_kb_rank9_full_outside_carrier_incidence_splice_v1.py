#!/usr/bin/env python3
"""Verify the full-outside carrier-sensitive rank-nine incidence splice.

This packet is stacked on the degree-195 effective-multiplier owner.  It
combines the source-slack floor, the rich-line moving-zero inequality, the
canonical rich-pencil atlas, the full-outside carrier shrink, and the exact
rank-nine one-cut compiler.  It closes two exact slack ranges without moving
the ledger and isolates a finite intermediate scalar route cut.  It does not
close rank nine or the KoalaBear row.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1 as predecessor


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-full-outside-carrier-incidence-splice-v1"
ARTIFACT_KIND = "M1_KB_RANK9_FULL_OUTSIDE_CARRIER_INCIDENCE_SPLICE"
STATUS = (
    "PROVED_LOCAL_EXACT_TWO_RANGE_CLOSURE_ZERO_LEDGER_MOVEMENT_"
    "INTERMEDIATE_LOW_X_DETERMINANT_PACKING_ROUTE_CUT_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-full-outside-carrier-incidence-splice-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_full_outside_carrier_incidence_splice_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_full_outside_carrier_incidence_splice_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-outside-carrier-incidence-splice-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.sage"
)
ATLAS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)
FIXED_BASIS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md"
)
MOVING_ROOT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_moving_root_slack_c5_boundary_v1.md"
)
TANGENT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_tangent_owner_splice_v1.md"
)
TANGENT_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py"
)

P = predecessor.P
N = predecessor.N
K = predecessor.K
A = predecessor.A
J = predecessor.J
T = predecessor.T
RICH_X_MAX = predecessor.RICH_X_MAX
CUTOFF_D = predecessor.CUTOFF_D
B_STAR = predecessor.B_STAR
U_PAID = predecessor.U_PAID_AFTER
B_REMAINING = predecessor.B_REMAINING_AFTER
K_REMAINING = predecessor.EXPECTED_K_REMAINING
TANGENT = predecessor.TANGENT

OWNER_CLOSED_R_MAX = predecessor.DEPLOYED_M
SCAN_R_MIN = OWNER_CLOSED_R_MAX + 1
SCAN_R_MAX = J - T - 1
CORE_RANK = TANGENT.CORE_R
SELECTOR_RANK = TANGENT.RANK_S
UNIFORM_BASIS_CAP = TANGENT.UNIFORM_CAP
CORE_BASIS_COUNT = math.comb(T + CORE_RANK, CORE_RANK)
MU_ZERO = TANGENT.m2b_multiplicity(0, 1)
MU_HIGH = TANGENT.m2b_multiplicity(CUTOFF_D + 1, 1)
MU_GAIN = MU_HIGH - MU_ZERO

FIRST_PAID_END = 67_466
GAP_START = FIRST_PAID_END + 1
GAP_END = 236_097
SECOND_PAID_START = GAP_END + 1
LAST_ONE_CUT_R = 330_335
FIRST_COARSE_R = LAST_ONE_CUT_R + 1

PAID_INCIDENCE_TERMINAL = "PAID_FULL_OUTSIDE_RICH_PENCIL_CARRIER_ONE_CUT"
PAID_COARSE_TERMINAL = "PAID_FULL_OUTSIDE_M2B_COARSE_CARRIER"
OPEN_TERMINAL = (
    "UNPAID_FULL_OUTSIDE_LOW_X_DETERMINANT_PACKING_"
    "SLACK_67467_TO_236097"
)

EXPECTED_PREDECESSOR_PAYLOAD = "5d886686d6d1f301396dcfbfb3ef499f31875edf6f0dd4f5f707e64b01e92fdd"

EXPECTED_INTERVALS = [
    [SCAN_R_MIN, FIRST_PAID_END, PAID_INCIDENCE_TERMINAL],
    [GAP_START, GAP_END, OPEN_TERMINAL],
    [SECOND_PAID_START, LAST_ONE_CUT_R, PAID_INCIDENCE_TERMINAL],
    [FIRST_COARSE_R, SCAN_R_MAX, PAID_COARSE_TERMINAL],
]

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessor",
    "counted_object_contract",
    "line_occupancy_lemma",
    "atlas_compiler",
    "carrier_sensitive_scan",
    "scalar_route_cut",
    "first_match_and_restart",
    "ledger",
    "revised_residual",
    "scope_guards",
    "nonclaims",
    "source_bindings",
    "payload_sha256",
}


class ContractError(RuntimeError):
    """Raised for parser, source, semantic, or arithmetic drift."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def ceil_div(a: int, b: int) -> int:
    require(b > 0, "ceil_div denominator must be positive")
    return -(-a // b)


def exact_int(value: object, name: str) -> int:
    require(type(value) is int, f"{name} is not an exact integer")
    return value


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ContractError(f"nonstandard JSON constant: {value}")


def reject_float(value: str) -> None:
    raise ContractError(f"floating-point JSON number: {value}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {path}")
    return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def payload_hash(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing source binding: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    predecessor_cert_rel = predecessor.CERT_PATH.relative_to(ROOT)
    return [
        source_binding("proof-note", NOTE_REL, "symbolic theorem and scope"),
        source_binding("readme", README_REL, "replay and status contract"),
        source_binding("python-verifier", SCRIPT_REL, "exact scan and mutations"),
        source_binding("sage-control", SAGE_REL, "independent arithmetic and toy controls"),
        source_binding(
            "predecessor-certificate",
            predecessor_cert_rel,
            "degree-195 owner payload",
        ),
        source_binding(
            "predecessor-note",
            predecessor.NOTE_REL,
            "degree-195 deletion and slack residual",
        ),
        source_binding("rich-pencil-atlas", ATLAS_NOTE_REL, "atlas identity and moving zeros"),
        source_binding("fixed-basis-compiler", FIXED_BASIS_NOTE_REL, "basis double count"),
        source_binding("moving-root-slack", MOVING_ROOT_NOTE_REL, "slack simplex and x floor"),
        source_binding("one-cut-note", TANGENT_NOTE_REL, "rank-nine restart semantics"),
        source_binding("one-cut-verifier", TANGENT_SCRIPT_REL, "exact M2b formulas"),
    ]


def validate_predecessor() -> dict[str, Any]:
    value = predecessor.load_json(predecessor.CERT_PATH)
    require(set(value) == predecessor.TOP_KEYS, "predecessor top-level key drift")
    require(value["schema"] == predecessor.SCHEMA, "predecessor schema drift")
    require(value["artifact_kind"] == predecessor.ARTIFACT_KIND, "predecessor kind drift")
    require(value["payload_sha256"] == predecessor.payload_hash(value), "predecessor payload hash mismatch")
    require(value["payload_sha256"] == EXPECTED_PREDECESSOR_PAYLOAD, "predecessor frozen payload drift")
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for binding in value["source_bindings"]:
        binding_id = binding["binding_id"]
        path = binding["path"]
        require(binding_id not in seen_ids, "duplicate predecessor binding id")
        require(path not in seen_paths, "duplicate predecessor binding path")
        seen_ids.add(binding_id)
        seen_paths.add(path)
        require(file_hash(Path(path)) == binding["sha256"], f"predecessor source drift: {path}")
    require(value["ledger"]["B_remaining_after"] == str(B_REMAINING), "predecessor budget drift")
    require(value["revised_residual"]["next_slack_r_min"] == SCAN_R_MIN, "predecessor residual drift")
    require(value["scope_guards"]["complete_rank9_payment_proved"] is False, "predecessor scope drift")
    return value


def source_size(r: int) -> int:
    return T + r + 1


def maximal_full_outside_carrier(r: int) -> int:
    return N - source_size(r)


def x_floor(r: int) -> int:
    s = source_size(r)
    return (s + 1) // 2 - r


def line_multiplicity_cap(r: int) -> int:
    floor = x_floor(r)
    if floor >= 1:
        return 1 + J // floor
    return J + 1


def coarse_cap(carrier: int) -> int:
    return math.comb(carrier, SELECTOR_RANK) // MU_ZERO


def one_cut_tail(carrier: int) -> int:
    ambient = math.comb(carrier, SELECTOR_RANK)
    require(ambient // MU_ZERO > B_REMAINING, "one-cut called on coarse-paid carrier")
    excess_needed = ambient + 1 - (B_REMAINING + 1) * MU_ZERO
    required_high = 0 if excess_needed <= 0 else ceil_div(excess_needed, MU_GAIN)
    tail = B_REMAINING + 1 - required_high
    require(tail >= 0, "one-cut has no useful threshold")
    return tail


def max_count_with_one_cut(low_cap: int, carrier: int) -> int:
    ambient = math.comb(carrier, SELECTOR_RANK)
    cheap = min(low_cap, ambient // MU_ZERO)
    return cheap + (ambient - cheap * MU_ZERO) // MU_HIGH


def low_deficit_cap(r: int) -> int:
    carrier = maximal_full_outside_carrier(r)
    return line_multiplicity_cap(r) * math.comb(carrier, CORE_RANK) // CORE_BASIS_COUNT


def terminal_for_r(r: int) -> str:
    carrier = maximal_full_outside_carrier(r)
    if coarse_cap(carrier) <= B_REMAINING:
        return PAID_COARSE_TERMINAL
    return PAID_INCIDENCE_TERMINAL if low_deficit_cap(r) <= one_cut_tail(carrier) else OPEN_TERMINAL


def compress_intervals(rows: list[tuple[int, str]]) -> list[list[Any]]:
    require(rows, "empty scan")
    result: list[list[Any]] = []
    start, status = rows[0]
    previous = start
    for r, current in rows[1:]:
        require(r == previous + 1, "nonconsecutive scan")
        if current != status:
            result.append([start, previous, status])
            start, status = r, current
        previous = r
    result.append([start, previous, status])
    return result


def route_relaxation(r: int) -> dict[str, Any]:
    require(terminal_for_r(r) == OPEN_TERMINAL, "route relaxation outside gap")
    carrier = maximal_full_outside_carrier(r)
    tail = one_cut_tail(carrier)
    low_count = tail + 1
    line_cap = line_multiplicity_cap(r)
    line_count = ceil_div(low_count, line_cap)
    ambient_bases = math.comb(carrier, CORE_RANK)
    bases_used = line_count * CORE_BASIS_COUNT
    chosen_x = x_floor(r) if x_floor(r) >= 1 else 1
    e_floor = (source_size(r) + 1) // 2
    u = e_floor - chosen_x
    h = r - u
    common_zero_size = carrier - (J + chosen_x)
    local_basis_capacity = math.comb(common_zero_size, CORE_RANK)
    require(chosen_x >= x_floor(r), "relaxation x misses source floor")
    require((line_cap - 1) * chosen_x <= J, "moving-zero cap violated")
    require(h >= 0 and u >= CUTOFF_D + 1, "slack relaxation infeasible")
    require(r - (CUTOFF_D + 1) > OWNER_CLOSED_R_MAX, "high-deficit scalar layer hits predecessor owner")
    require(local_basis_capacity >= CORE_BASIS_COUNT, "local common-zero basis capacity fails")
    require(bases_used <= ambient_bases, "abstract disjoint basis packing fails")
    require(
        max_count_with_one_cut(low_count, carrier) == B_REMAINING + 1,
        "one-cut sharpness histogram drift",
    )
    return {
        "r": r,
        "source_size": source_size(r),
        "carrier_size": carrier,
        "x_floor": x_floor(r),
        "chosen_scalar_x": chosen_x,
        "chosen_e": e_floor,
        "chosen_u": u,
        "chosen_h": h,
        "chosen_ell": 0,
        "chosen_effective_multiplier_degree": r,
        "survives_degree_195_owner_scalar_guard": True,
        "common_zero_size_per_line": common_zero_size,
        "local_basis_capacity_per_line": str(local_basis_capacity),
        "line_slope_cap": line_cap,
        "low_deficit_count": str(low_count),
        "abstract_line_count": str(line_count),
        "bases_per_line": str(CORE_BASIS_COUNT),
        "abstract_bases_used": str(bases_used),
        "ambient_basis_capacity": str(ambient_bases),
        "basis_capacity_margin": str(ambient_bases - bases_used),
        "one_cut_count": str(B_REMAINING + 1),
        "one_cut_breaks_budget_by": "1",
        "actual_RS_selector_constructed": False,
    }


def endpoint_record(r: int) -> dict[str, Any]:
    carrier = maximal_full_outside_carrier(r)
    current_coarse = coarse_cap(carrier)
    result: dict[str, Any] = {
        "r": r,
        "source_size": source_size(r),
        "maximal_full_outside_carrier": carrier,
        "x_floor": x_floor(r),
        "line_multiplicity_cap": line_multiplicity_cap(r),
        "coarse_cap": str(current_coarse),
        "terminal": terminal_for_r(r),
    }
    if current_coarse > B_REMAINING:
        tail = one_cut_tail(carrier)
        h_cap = low_deficit_cap(r)
        imported = TANGENT.one_cut_gate(B_REMAINING, CUTOFF_D, carrier, 1)
        require(int(imported["largest_sufficient_low_deficit_cap_T_star"]) == tail, "imported tail drift")
        require(int(imported["cap_at_T_star"]) == B_REMAINING, "Tstar sharpness drift")
        require(int(imported["cap_at_T_star_plus_1"]) == B_REMAINING + 1, "Tstar+1 sharpness drift")
        result.update(
            {
                "tail_target": str(tail),
                "low_deficit_cap": str(h_cap),
                "tail_margin": str(tail - h_cap),
                "cap_at_T_star": imported["cap_at_T_star"],
                "cap_at_T_star_plus_1": imported["cap_at_T_star_plus_1"],
            }
        )
    return result


@functools.lru_cache(maxsize=1)
def scan_profiles_cached() -> dict[str, Any]:
    rows: list[tuple[int, str]] = []
    counts: dict[str, int] = {
        PAID_INCIDENCE_TERMINAL: 0,
        PAID_COARSE_TERMINAL: 0,
        OPEN_TERMINAL: 0,
    }
    digest = hashlib.sha256()
    route_digest = hashlib.sha256()
    route_count = 0
    for r in range(SCAN_R_MIN, SCAN_R_MAX + 1):
        terminal = terminal_for_r(r)
        counts[terminal] += 1
        rows.append((r, terminal))
        carrier = maximal_full_outside_carrier(r)
        current_coarse = coarse_cap(carrier)
        tail = None if current_coarse <= B_REMAINING else one_cut_tail(carrier)
        h_cap = None if current_coarse <= B_REMAINING else low_deficit_cap(r)
        digest.update(
            canonical_bytes(
                [r, source_size(r), carrier, x_floor(r), line_multiplicity_cap(r), current_coarse, tail, h_cap, terminal]
            )
        )
        if terminal == OPEN_TERMINAL:
            relaxation = route_relaxation(r)
            route_count += 1
            route_digest.update(canonical_bytes(relaxation))

    intervals = compress_intervals(rows)
    require(intervals == EXPECTED_INTERVALS, "exact interval partition drift")
    require(route_count == GAP_END - GAP_START + 1, "route-cut count drift")
    return {
        "scan_r_min": SCAN_R_MIN,
        "scan_r_max": SCAN_R_MAX,
        "scan_count": SCAN_R_MAX - SCAN_R_MIN + 1,
        "scan_sha256": digest.hexdigest(),
        "intervals": intervals,
        "terminal_counts": counts,
        "route_relaxation_count": route_count,
        "route_relaxation_sha256": route_digest.hexdigest(),
    }


def scan_profiles() -> dict[str, Any]:
    return copy.deepcopy(scan_profiles_cached())


NONCLAIMS = [
    "does not construct a KoalaBear deployed selector or counterexample",
    "does not sum charges over source sizes, selectors, graph lines, or received pairs",
    "does not alter the degree-195 owner or its first-match charge",
    "does not replace cutoff 18014 by an incomparable cutoff",
    "does not pay the intermediate slack band 67467 through 236097",
    "does not promote an abstract scalar packing to Reed-Solomon realizability",
    "does not pay non-full-outside source load",
    "does not determine U_Q or residual U_A",
    "does not close rank nine, branch 3, KoalaBear, or the complete theorem",
    "does not authorize rank at least ten, Lean, or stable-paper promotion",
]


_EXPECTED_CACHE: dict[str, Any] | None = None


def expected_certificate() -> dict[str, Any]:
    global _EXPECTED_CACHE
    if _EXPECTED_CACHE is not None:
        return copy.deepcopy(_EXPECTED_CACHE)

    predecessor_document = validate_predecessor()
    scan = scan_profiles()
    note = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        PAID_INCIDENCE_TERMINAL,
        PAID_COARSE_TERMINAL,
        OPEN_TERMINAL,
        "67{,}466",
        "236{,}098",
        "330{,}336",
        "determinant packing",
        "zero ledger movement",
    ):
        require(token in note, f"proof-note token missing: {token}")

    endpoints = [
        endpoint_record(r)
        for r in [
            SCAN_R_MIN,
            FIRST_PAID_END,
            GAP_START,
            GAP_END,
            SECOND_PAID_START,
            LAST_ONE_CUT_R,
            FIRST_COARSE_R,
            SCAN_R_MAX,
        ]
    ]
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "n": N,
            "k": K,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
            "rich_x_max": RICH_X_MAX,
            "cutoff_D": CUTOFF_D,
            "core_rank": CORE_RANK,
            "selector_rank": SELECTOR_RANK,
            "source_size_cap": J,
        },
        "predecessor": {
            "schema": predecessor.SCHEMA,
            "payload_sha256": predecessor_document["payload_sha256"],
            "stacked_on_commit": "f1ee7b5229701af56c13c278ece780553c9b3ce8",
            "degree_195_owner_deletion_precedes_this_splice": True,
            "first_incoming_slack": SCAN_R_MIN,
        },
        "counted_object_contract": {
            "object": "distinct finite bad slopes for one fixed received pair and its one SP3 translation",
            "source_support_is_fixed_before_selector": True,
            "source_slack_r_is_one_fixed_integer_per_received_pair": True,
            "union_over_r_forbidden": True,
            "full_outside_required": True,
            "complete_rebuilt_rank9_selector_required": True,
            "low_deficit_family": "Gamma_D={eta:0<=delta_eta<=18014}",
        },
        "line_occupancy_lemma": {
            "source_size_formula": "s=t+r+1",
            "full_outside_carrier_formula": "N_V<=n-s",
            "x_floor_formula": "x_L>=ceil(s/2)-r",
            "moving_zero_formula": "J_L*x_L+sum_eta(delta_eta)<=j+x_L",
            "moving_zero_nonempty_formula": "x_L+delta_eta>=1",
            "line_cap_when_x_floor_positive": "1+floor(j/x_floor)",
            "uniform_line_cap_when_x_floor_nonpositive": J + 1,
            "line_cap_derivation_for_x_nonpositive": "J_L<=j+x_L<=j; x_L>=1 uses J_L<=1+floor(j/x_L)<=j+1",
            "all_parameters_exact_integers": True,
        },
        "atlas_compiler": {
            "core_basis_count": str(CORE_BASIS_COUNT),
            "lower_double_count": "H_D*C(t+8,8)<=sum_B(m_B)",
            "atlas_identity": "E_20=sum_L beta_L*(J_L-20)",
            "rich_bases_partition_by_unique_graph_line": True,
            "sum_beta_bound": "sum_L(beta_L)<=C(N_V,8)",
            "compiled_bound": "H_D<=floor(J_star(r)*C(N_V,8)/C(t+8,8))",
            "uniform_basis_cap": UNIFORM_BASIS_CAP,
        },
        "carrier_sensitive_scan": {
            "remaining_budget": str(B_REMAINING),
            "mu_zero": str(MU_ZERO),
            "mu_D_plus_1": str(MU_HIGH),
            "mu_gain": str(MU_GAIN),
            "source_distance_one_is_imported_worst_case": True,
            "maximal_carrier_is_worst_for_incidence_cap": True,
            "maximal_carrier_is_worst_for_one_cut_tail": True,
            "paid_carrier_exits_before_one_cut": True,
            "scan": scan,
            "endpoints": endpoints,
        },
        "scalar_route_cut": {
            "terminal": OPEN_TERMINAL,
            "gap_r_min": GAP_START,
            "gap_r_max": GAP_END,
            "gap_source_size_min": source_size(GAP_START),
            "gap_source_size_max": source_size(GAP_END),
            "every_gap_profile_has_exact_abstract_relaxation": True,
            "relaxation_uses_T_star_plus_one_low_deficit_slopes": True,
            "relaxation_partitions_abstract_bases_into_disjoint_graph_line_blocks": True,
            "relaxation_respects_moving_zero_slack_and_M2b_scalar_inequalities": True,
            "first_gap_control": route_relaxation(GAP_START),
            "last_gap_control": route_relaxation(GAP_END),
            "missing_lemma": (
                "deployed determinant/source coupling that forbids the abstract "
                "low-x disjoint-basis packing or supplies another paid owner"
            ),
            "actual_selector_or_counterexample_claimed": False,
        },
        "first_match_and_restart": {
            "predecessor_owner_order_unchanged": True,
            "new_root_owner_added": False,
            "new_charge_added": False,
            "same_selector_fields_used_in_each_incidence implication": True,
            "stale_pre_deletion_selector_fields_forbidden": True,
            "later_terminals_receive_exact_residual": True,
        },
        "ledger": {
            "B_star": str(B_STAR),
            "U_paid_before": str(U_PAID),
            "U_paid_after": str(U_PAID),
            "B_remaining_before": str(B_REMAINING),
            "B_remaining_after": str(B_REMAINING),
            "K_remaining": K_REMAINING,
            "ledger_movement": "0",
            "U_Q": None,
            "residual_U_A": None,
            "complete_upper_inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "revised_residual": {
            "upstream_C5_owns_r_zero": True,
            "predecessor_owner_owns_r_1_through_195": True,
            "incidence_paid_r_196_through_67466": True,
            "unpaid_r_67467_through_236097": True,
            "incidence_paid_r_236098_through_330335": True,
            "coarse_carrier_paid_r_330336_through_913631": True,
            "source_slack_upper_endpoint": SCAN_R_MAX,
            "only_remaining_full_outside_slack_interval": [GAP_START, GAP_END],
            "terminal": OPEN_TERMINAL,
        },
        "scope_guards": {
            "symbolic_line_occupancy_proved": True,
            "exact_carrier_scan_proved": True,
            "scalar_gap_route_cut_proved": True,
            "deployed_gap_determinant_packing_bound_proved": False,
            "non_full_outside_paid": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": list(NONCLAIMS),
        "source_bindings": expected_source_bindings(),
        "payload_sha256": "",
    }
    result["payload_sha256"] = payload_hash(result)
    _EXPECTED_CACHE = copy.deepcopy(result)
    return result


def verify_semantics(value: dict[str, Any]) -> None:
    require(set(value) == TOP_KEYS, "top-level key set drift")
    require(value.get("schema") == SCHEMA, "schema drift")
    require(value.get("artifact_kind") == ARTIFACT_KIND, "artifact kind drift")
    require(value.get("status") == STATUS, "status drift")
    require(value.get("payload_sha256") == payload_hash(value), "payload hash mismatch")
    for key in ("p", "n", "k", "agreement_A", "error_count_j", "syndrome_depth_t", "cutoff_D"):
        exact_int(value["row"][key], f"row.{key}")
    expected = expected_certificate()
    require(canonical_bytes(value) == canonical_bytes(expected), "certificate semantic or source-binding drift")


def run_check() -> None:
    value = load_json(CERT_PATH)
    verify_semantics(value)
    print("M1 KoalaBear full-outside carrier-incidence splice: PASS")
    print(f"  incidence-paid slack: {SCAN_R_MIN:,}..{FIRST_PAID_END:,}")
    print(f"  primitive gap: {GAP_START:,}..{GAP_END:,}")
    print(f"  incidence-paid slack: {SECOND_PAID_START:,}..{LAST_ONE_CUT_R:,}")
    print(f"  coarse-carrier-paid slack: {FIRST_COARSE_R:,}..{SCAN_R_MAX:,}")
    print("  ledger movement: 0; rank nine and KoalaBear remain OPEN")


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-mutated")),
        ("kind", lambda d: d.__setitem__("artifact_kind", "ROW_CLOSURE")),
        ("status", lambda d: d.__setitem__("status", "KOALABEAR_CLOSED")),
        ("row-rank", lambda d: d["row"].__setitem__("selector_rank", 10)),
        ("row-D", lambda d: d["row"].__setitem__("cutoff_D", CUTOFF_D + 1)),
        ("source-not-fixed", lambda d: d["counted_object_contract"].__setitem__("source_support_is_fixed_before_selector", False)),
        ("union-r", lambda d: d["counted_object_contract"].__setitem__("union_over_r_forbidden", False)),
        ("not-full-outside", lambda d: d["counted_object_contract"].__setitem__("full_outside_required", False)),
        ("x-floor", lambda d: d["line_occupancy_lemma"].__setitem__("x_floor_formula", "x_L>=0")),
        ("negative-x-cap", lambda d: d["line_occupancy_lemma"].__setitem__("uniform_line_cap_when_x_floor_nonpositive", J)),
        ("atlas-overlap", lambda d: d["atlas_compiler"].__setitem__("rich_bases_partition_by_unique_graph_line", False)),
        ("basis-count", lambda d: d["atlas_compiler"].__setitem__("core_basis_count", str(CORE_BASIS_COUNT + 1))),
        ("budget", lambda d: d["carrier_sensitive_scan"].__setitem__("remaining_budget", str(B_REMAINING + 1))),
        ("mu0", lambda d: d["carrier_sensitive_scan"].__setitem__("mu_zero", str(MU_ZERO + 1))),
        ("carrier-monotone", lambda d: d["carrier_sensitive_scan"].__setitem__("maximal_carrier_is_worst_for_one_cut_tail", False)),
        ("interval-start", lambda d: d["carrier_sensitive_scan"]["scan"]["intervals"][0].__setitem__(0, SCAN_R_MIN + 1)),
        ("interval-first-end", lambda d: d["carrier_sensitive_scan"]["scan"]["intervals"][0].__setitem__(1, FIRST_PAID_END + 1)),
        ("gap-start", lambda d: d["scalar_route_cut"].__setitem__("gap_r_min", GAP_START + 1)),
        ("gap-end", lambda d: d["scalar_route_cut"].__setitem__("gap_r_max", GAP_END - 1)),
        ("fake-selector", lambda d: d["scalar_route_cut"].__setitem__("actual_selector_or_counterexample_claimed", True)),
        ("packing", lambda d: d["scalar_route_cut"].__setitem__("every_gap_profile_has_exact_abstract_relaxation", False)),
        ("local-capacity", lambda d: d["scalar_route_cut"]["first_gap_control"].__setitem__("common_zero_size_per_line", 0)),
        ("owner-scalar-guard", lambda d: d["scalar_route_cut"]["last_gap_control"].__setitem__("survives_degree_195_owner_scalar_guard", False)),
        ("owner-added", lambda d: d["first_match_and_restart"].__setitem__("new_root_owner_added", True)),
        ("charge-added", lambda d: d["first_match_and_restart"].__setitem__("new_charge_added", True)),
        ("stale-selector", lambda d: d["first_match_and_restart"].__setitem__("stale_pre_deletion_selector_fields_forbidden", False)),
        ("ledger-move", lambda d: d["ledger"].__setitem__("ledger_movement", "1")),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID + 1))),
        ("residual-gap", lambda d: d["revised_residual"]["only_remaining_full_outside_slack_interval"].__setitem__(1, GAP_END + 1)),
        ("pay-gap", lambda d: d["revised_residual"].__setitem__("unpaid_r_67467_through_236097", False)),
        ("global-incidence", lambda d: d["scope_guards"].__setitem__("deployed_gap_determinant_packing_bound_proved", True)),
        ("rank9", lambda d: d["scope_guards"].__setitem__("complete_rank9_payment_proved", True)),
        ("closure", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("lean", lambda d: d["scope_guards"].__setitem__("lean_authorized", True)),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("duplicate-binding", lambda d: d["source_bindings"][1].__setitem__("binding_id", d["source_bindings"][0]["binding_id"])),
        ("bool-int", lambda d: d["row"].__setitem__("n", True)),
        ("payload", lambda d: d.__setitem__("payload_sha256", "1" * 64)),
    ]


def run_tamper_selftest() -> None:
    baseline = expected_certificate()
    verify_semantics(baseline)
    passed = 0
    for label, mutate in mutation_cases():
        changed = copy.deepcopy(baseline)
        mutate(changed)
        if label != "payload":
            changed["payload_sha256"] = payload_hash(changed)
        try:
            verify_semantics(changed)
        except (ContractError, KeyError, ValueError, IndexError):
            passed += 1
        else:
            raise ContractError(f"semantic mutation survived: {label}")

    parser_cases = [
        ('{"schema":"x","schema":"y"}', "duplicate-key"),
        ('{"x":1.25}', "float"),
        ('{"x":NaN}', "nan"),
        ('{"x":Infinity}', "infinity"),
        ('[1,2,3]', "top-level-list"),
    ]
    for raw, label in parser_cases:
        try:
            value = json.loads(
                raw,
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=reject_constant,
                parse_float=reject_float,
            )
            require(type(value) is dict, f"{label}: top-level is not object")
        except (ContractError, ValueError):
            passed += 1
        else:
            raise ContractError(f"parser mutation survived: {label}")
    expected = len(mutation_cases()) + len(parser_cases)
    require(passed == expected, "tamper count drift")
    print(f"M1 carrier-incidence mutations: {passed}/{expected} PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check:
        run_check()
    elif args.tamper_selftest:
        run_tamper_selftest()
    elif args.write:
        CERT_PATH.write_text(
            json.dumps(expected_certificate(), sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        print(json.dumps(expected_certificate(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
