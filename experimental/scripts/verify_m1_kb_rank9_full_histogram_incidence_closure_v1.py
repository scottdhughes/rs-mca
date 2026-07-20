#!/usr/bin/env python3
"""Verify the M1 KoalaBear full-histogram incidence closure.

The certificate proves two exact paid slack ranges and constructs an abstract
all-zero-deficit scalar packing at every integer in the residual interval.
The packing is a route cut, not a deployed Reed--Solomon selector.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1 as predecessor


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-full-histogram-incidence-closure-v1"
ARTIFACT_KIND = "M1_KB_RANK9_FULL_HISTOGRAM_INCIDENCE_CLOSURE"
STATUS = (
    "PROVED_LOCAL_FULL_HISTOGRAM_TWO_RANGE_CLOSURE_"
    "EXACT_142082_LAYER_SCALAR_ROUTE_CUT_REVIEW_PENDING_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-full-histogram-incidence-closure-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_full_histogram_incidence_closure_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_full_histogram_incidence_closure_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-histogram-incidence-closure-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.sage"
)
PREDECESSOR_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-outside-carrier-incidence-splice-v1/"
    "m1_kb_rank9_full_outside_carrier_incidence_splice_v1.json"
)
PREDECESSOR_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_full_outside_carrier_incidence_splice_v1.md"
)
PREDECESSOR_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.py"
)
PREDECESSOR_SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.sage"
)
PREDECESSOR_README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-outside-carrier-incidence-splice-v1/README.md"
)
BOUNDED_SLACK_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.md"
)
MOVING_ROOT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_moving_root_slack_c5_boundary_v1.md"
)
RICH_ATLAS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)
FIXED_BASIS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md"
)

P = predecessor.P
N = predecessor.N
K = predecessor.K
A = predecessor.A
J = predecessor.J
T = predecessor.T
B_STAR = predecessor.B_STAR
U_PAID = predecessor.U_PAID
B_REMAINING = predecessor.B_REMAINING
K_REMAINING = predecessor.K_REMAINING
CORE_RANK = predecessor.CORE_RANK
SELECTOR_RANK = predecessor.SELECTOR_RANK
C0 = predecessor.CORE_BASIS_COUNT
MU_ZERO = predecessor.MU_ZERO
OWNER_CLOSED_R_MAX = predecessor.OWNER_CLOSED_R_MAX

SCAN_R_MIN = OWNER_CLOSED_R_MAX + 1
SCAN_R_MAX = J - T - 1
FIRST_PAID_END = 67_470
GAP_START = 67_471
GAP_END = 209_552
SECOND_PAID_START = 209_553
GAP_COUNT = GAP_END - GAP_START + 1

PAID_TERMINAL = "PAID_FULL_OUTSIDE_FULL_HISTOGRAM_CARRIER_INCIDENCE"
OPEN_TERMINAL = (
    "UNPAID_FULL_OUTSIDE_X1_DETERMINANT_SOURCE_PACKING_"
    "SLACK_67471_TO_209552"
)

EXPECTED_PREDECESSOR_SCHEMA = (
    "rs-mca-m1-kb-rank9-full-outside-carrier-incidence-splice-v1"
)
EXPECTED_PREDECESSOR_PAYLOAD = (
    "92bf739436b713d8c759209f2ceb1d105c2bf0f09fa73934464222af386230b8"
)
STACKED_ON_COMMIT = "99fd355d7f25afff471d1a6bdf5977c447c5d037"

# Filled after the exact scan is frozen.  These constants bind the complete
# integer ranges independently of the pretty-printed JSON certificate.
EXPECTED_SCAN_SHA256 = "3d4aa95eedd837899bdeb2206ec03602f43b507ad4619f24b1fcadd548e3a91d"
EXPECTED_ROUTE_SHA256 = "4b3b7eaa50eaf65bc510db346f3d99ce4f575e41fc52287bb6b09831aa40b6a3"

EXPECTED_INTERVALS = [
    [SCAN_R_MIN, FIRST_PAID_END, PAID_TERMINAL],
    [GAP_START, GAP_END, OPEN_TERMINAL],
    [SECOND_PAID_START, SCAN_R_MAX, PAID_TERMINAL],
]
EXPECTED_TERMINAL_COUNTS = {
    PAID_TERMINAL: (FIRST_PAID_END - SCAN_R_MIN + 1) + (SCAN_R_MAX - SECOND_PAID_START + 1),
    OPEN_TERMINAL: GAP_COUNT,
}

SOURCE_FILES = [
    NOTE_REL,
    README_REL,
    SCRIPT_REL,
    SAGE_REL,
    PREDECESSOR_CERT_REL,
    PREDECESSOR_NOTE_REL,
    PREDECESSOR_SCRIPT_REL,
    PREDECESSOR_SAGE_REL,
    PREDECESSOR_README_REL,
    BOUNDED_SLACK_NOTE_REL,
    MOVING_ROOT_NOTE_REL,
    RICH_ATLAS_NOTE_REL,
    FIXED_BASIS_NOTE_REL,
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def ceil_div(a: int, b: int) -> int:
    require(b > 0, "ceil-div denominator must be positive")
    return -(-a // b)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_noninteger_json_number(token: str) -> Any:
    raise RuntimeError(f"noninteger or nonstandard JSON number: {token}")


def parse_json_strict_text(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_float=reject_noninteger_json_number,
        parse_constant=reject_noninteger_json_number,
    )
    require(isinstance(value, dict), "JSON root is not an object")
    return value


def load_json_strict(path: Path) -> dict[str, Any]:
    try:
        return parse_json_strict_text(path.read_text())
    except RuntimeError as exc:
        raise RuntimeError(f"strict JSON failure in {path}: {exc}") from exc


def payload_sha256(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def source_size(r: int) -> int:
    return T + r + 1


def maximal_carrier(r: int) -> int:
    return N - source_size(r)


def x_floor(r: int) -> int:
    return (source_size(r) + 1) // 2 - r


def line_cap(r: int) -> int:
    x0 = x_floor(r)
    return 1 + J // x0 if x0 >= 1 else J + 1


def full_histogram_cap(r: int) -> int:
    return line_cap(r) * math.comb(maximal_carrier(r), CORE_RANK) // C0


def terminal_for_r(r: int) -> str:
    return PAID_TERMINAL if full_histogram_cap(r) <= B_REMAINING else OPEN_TERMINAL


def endpoint_record(r: int) -> dict[str, Any]:
    cap = full_histogram_cap(r)
    return {
        "r": r,
        "source_size": source_size(r),
        "maximal_full_outside_carrier": maximal_carrier(r),
        "x_floor": x_floor(r),
        "line_multiplicity_cap": line_cap(r),
        "full_histogram_cap": str(cap),
        "budget_minus_cap": str(B_REMAINING - cap),
        "terminal": terminal_for_r(r),
    }


def scan_profiles() -> dict[str, Any]:
    digest = hashlib.sha256()
    intervals: list[list[Any]] = []
    counts = {PAID_TERMINAL: 0, OPEN_TERMINAL: 0}
    current_start = SCAN_R_MIN
    current_terminal = terminal_for_r(SCAN_R_MIN)
    previous = SCAN_R_MIN - 1

    for r in range(SCAN_R_MIN, SCAN_R_MAX + 1):
        status = terminal_for_r(r)
        counts[status] += 1
        digest.update(
            canonical_bytes(
                [
                    r,
                    source_size(r),
                    maximal_carrier(r),
                    x_floor(r),
                    line_cap(r),
                    str(full_histogram_cap(r)),
                    status,
                ]
            )
        )
        digest.update(b"\n")
        if status != current_terminal:
            intervals.append([current_start, r - 1, current_terminal])
            current_start = r
            current_terminal = status
        previous = r

    require(previous == SCAN_R_MAX, "scan ended early")
    intervals.append([current_start, SCAN_R_MAX, current_terminal])
    require(intervals == EXPECTED_INTERVALS, "full-histogram interval drift")
    require(counts == EXPECTED_TERMINAL_COUNTS, "terminal count drift")
    return {
        "scan_r_min": SCAN_R_MIN,
        "scan_r_max": SCAN_R_MAX,
        "scan_count": SCAN_R_MAX - SCAN_R_MIN + 1,
        "intervals": intervals,
        "terminal_counts": counts,
        "scan_sha256": digest.hexdigest(),
    }


def route_record(r: int) -> dict[str, Any]:
    require(GAP_START <= r <= GAP_END, "route record outside exact gap")
    require(terminal_for_r(r) == OPEN_TERMINAL, "route record is not residual")
    H = B_REMAINING + 1
    carrier = maximal_carrier(r)
    j_cap = line_cap(r)
    line_count = ceil_div(H, j_cap)
    bases_used = line_count * C0
    ambient_bases = math.comb(carrier, CORE_RANK)
    chosen_x = 1
    e = (source_size(r) + 1) // 2
    u = e - chosen_x
    h = r - u
    ell = 0
    common_zero_size = carrier - (J + chosen_x)
    local_basis_capacity = math.comb(common_zero_size, CORE_RANK)
    ambient_rank9 = math.comb(carrier, SELECTOR_RANK)
    weighted_rank9 = H * MU_ZERO

    require(j_cap == J + 1, "route line cap is not the x<=1 cap")
    require(chosen_x >= x_floor(r), "route chosen x misses source floor")
    require(h >= 0 and u >= 0 and h + u + ell == r, "route slack simplex failed")
    require(0 <= u <= r, "route deficit envelope failed")
    require((j_cap - 1) * chosen_x == J, "moving-zero equality drift")
    require(r > OWNER_CLOSED_R_MAX, "route hits degree-195 owner")
    require(bases_used <= ambient_bases, "global abstract basis capacity failed")
    require(C0 <= local_basis_capacity, "local abstract basis capacity failed")
    require(weighted_rank9 <= ambient_rank9, "rank-nine scalar capacity failed")
    require(H <= P**6, "extension slope universe too small")
    return {
        "r": r,
        "source_size": source_size(r),
        "carrier_size": carrier,
        "x_floor": x_floor(r),
        "chosen_x": chosen_x,
        "chosen_e": e,
        "chosen_h": h,
        "chosen_u": u,
        "chosen_ell": ell,
        "chosen_deficit": 0,
        "line_slope_cap": j_cap,
        "slope_count": str(H),
        "abstract_line_count": str(line_count),
        "bases_per_line": str(C0),
        "global_basis_margin": str(ambient_bases - bases_used),
        "common_zero_size_per_line": common_zero_size,
        "local_basis_margin": str(local_basis_capacity - C0),
        "rank9_capacity_margin": str(ambient_rank9 - weighted_rank9),
        "survives_degree_195_owner_scalar_guard": True,
        "all_deficits_zero": True,
        "actual_RS_selector_constructed": False,
    }


def scan_route_cut() -> dict[str, Any]:
    digest = hashlib.sha256()
    first: dict[str, Any] | None = None
    last: dict[str, Any] | None = None
    count = 0
    for r in range(GAP_START, GAP_END + 1):
        record = route_record(r)
        if first is None:
            first = record
        last = record
        count += 1
        digest.update(canonical_bytes(record))
        digest.update(b"\n")
    require(first is not None and last is not None, "empty route scan")
    require(count == GAP_COUNT == 142_082, "route count drift")
    return {
        "gap_r_min": GAP_START,
        "gap_r_max": GAP_END,
        "route_relaxation_count": count,
        "route_sha256": digest.hexdigest(),
        "first_gap_control": first,
        "last_gap_control": last,
    }


def load_predecessor() -> dict[str, Any]:
    value = load_json_strict(ROOT / PREDECESSOR_CERT_REL)
    require(value.get("schema") == EXPECTED_PREDECESSOR_SCHEMA, "predecessor schema drift")
    require(value.get("payload_sha256") == EXPECTED_PREDECESSOR_PAYLOAD, "predecessor payload drift")
    require(
        predecessor.payload_hash(value) == EXPECTED_PREDECESSOR_PAYLOAD,
        "predecessor self-hash drift",
    )
    require(
        value["ledger"]["B_remaining_after"] == str(B_REMAINING),
        "predecessor budget drift",
    )
    require(value["ledger"]["U_paid_after"] == str(U_PAID), "predecessor charge drift")
    require(
        value["revised_residual"]["only_remaining_full_outside_slack_interval"]
        == [67_467, 236_097],
        "predecessor residual drift",
    )
    return value


def source_bindings() -> dict[str, str]:
    bindings: dict[str, str] = {}
    for relative in SOURCE_FILES:
        path = ROOT / relative
        require(path.is_file(), f"missing bound source: {relative}")
        key = relative.as_posix()
        require(key not in bindings, f"duplicate bound source: {key}")
        bindings[key] = sha256_file(path)
    return dict(sorted(bindings.items()))


def verify_text_contracts() -> None:
    note = (ROOT / NOTE_REL).read_text()
    readme = (ROOT / README_REL).read_text()
    note_fragments = [
        "PAID_FULL_OUTSIDE_FULL_HISTOGRAM_CARRIER_INCIDENCE",
        "UNPAID_FULL_OUTSIDE_X1_DETERMINANT_SOURCE_PACKING_SLACK_67471_TO_209552",
        "67{,}471\\le r\\le209{,}552",
        "209{,}553\\le r\\le913{,}631",
        "226{,}725{,}640{,}592{,}636{,}461",
        "237{,}273{,}154{,}024",
        "971{,}348{,}191{,}761",
        "The global verdict remains **YELLOW**.",
    ]
    readme_fragments = [
        "196..67470",
        "209553..913631",
        "67471..209552",
        "142,082 layers",
        "not a Reed--Solomon selector",
    ]
    for fragment in note_fragments:
        require(fragment in note, f"proof-note contract missing: {fragment}")
    for fragment in readme_fragments:
        require(fragment in readme, f"README contract missing: {fragment}")


def build_certificate() -> dict[str, Any]:
    load_predecessor()
    verify_text_contracts()
    scan = scan_profiles()
    route = scan_route_cut()
    if EXPECTED_SCAN_SHA256 != "TO_BE_FROZEN":
        require(scan["scan_sha256"] == EXPECTED_SCAN_SHA256, "frozen scan digest drift")
    if EXPECTED_ROUTE_SHA256 != "TO_BE_FROZEN":
        require(route["route_sha256"] == EXPECTED_ROUTE_SHA256, "frozen route digest drift")

    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "extension_degree": 6,
            "n": N,
            "k": K,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
            "core_rank": CORE_RANK,
            "selector_rank": SELECTOR_RANK,
        },
        "predecessor": {
            "schema": EXPECTED_PREDECESSOR_SCHEMA,
            "payload_sha256": EXPECTED_PREDECESSOR_PAYLOAD,
            "stacked_on_commit": STACKED_ON_COMMIT,
            "exact_deletion_and_selector_restart_precede_this_packet": True,
        },
        "full_histogram_lemma": {
            "all_selected_deficits_nonnegative": True,
            "all_slope_mds_basis_floor": "C(t+8+delta_eta,8)>=C(t+8,8)",
            "rich_line_slack_simplex": "h_L+u_L+ell_L=r with h_L,u_L,ell_L>=0",
            "rich_line_deficit_bound": "0<=delta_eta,L<=u_L<=r",
            "rich_line_coverage_of_all_slopes_claimed": False,
            "source_size_formula": "s=t+r+1",
            "full_outside_carrier_formula": "N_V<=n-s",
            "x_floor_formula": "x_L>=ceil((t-r+1)/2)",
            "moving_zero_formula": "J_L*x_L+sum_eta(delta_eta,L)<=j+x_L",
            "moving_zero_nonempty_formula": "x_L+delta_eta,L>=1",
            "line_cap_positive_x": "1+floor(j/x_floor)",
            "line_cap_nonpositive_floor": J + 1,
            "core_basis_count": str(C0),
            "compiled_total_bound": "|Gamma|<=floor(J_star(r)*C(N_V,8)/C(t+8,8))",
            "fixed_basis_graph_line_argument_is_subset_uniform": True,
            "full_selector_atlas_replayed_without_numeric_cutoff": True,
            "same_selector_provenance_required": True,
        },
        "exact_scan": {
            **scan,
            "endpoints": [
                endpoint_record(r)
                for r in [196, 67_466, 67_467, 67_470, 67_471, 209_552, 209_553, 236_097, 913_631]
            ],
            "newly_closed_lower_layers": [67_467, 67_470],
            "newly_closed_upper_layers": [209_553, 236_097],
            "newly_closed_layer_count": 26_549,
        },
        "scalar_route_cut": {
            **route,
            "target_slope_count": str(B_REMAINING + 1),
            "all_zero_deficits_defeat_every_nonnegative_cutoff": True,
            "cutoff_optimization_can_close_gap": False,
            "actual_selector_or_counterexample_claimed": False,
            "missing_object": "deployed determinant/source packing or disjoint named owner",
        },
        "ledger": {
            "B_star": str(B_STAR),
            "U_paid_before": str(U_PAID),
            "U_paid_after": str(U_PAID),
            "B_remaining_before": str(B_REMAINING),
            "B_remaining_after": str(B_REMAINING),
            "ledger_movement": "0",
            "K_remaining": K_REMAINING,
            "U_Q": None,
            "residual_U_A": None,
            "complete_upper_inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "revised_residual": {
            "upstream_C5_owns_r_zero": True,
            "degree_195_owner_owns_r_1_through_195": True,
            "full_histogram_paid_intervals": [[196, 67_470], [209_553, 913_631]],
            "only_remaining_full_outside_slack_interval": [GAP_START, GAP_END],
            "terminal": OPEN_TERMINAL,
            "next_exact_boundary": {"r": GAP_START, "x_floor": 1},
        },
        "first_match_and_restart": {
            "new_root_owner_added": False,
            "new_charge_added": False,
            "predecessor_owner_order_unchanged": True,
            "later_terminals_receive_exact_residual": True,
            "one_fixed_r_per_received_pair": True,
            "union_over_r_forbidden": True,
            "stale_pre_deletion_selector_fields_forbidden": True,
        },
        "scope_guards": {
            "full_outside_only": True,
            "coefficient_rank_two_only": True,
            "complete_rebuilt_rank9_selector_required": True,
            "deployed_determinant_source_packing_proved": False,
            "non_full_outside_paid": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "U_Q_determined": False,
            "residual_U_A_determined": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
        },
        "nonclaims": [
            "does not construct a deployed Reed-Solomon selector or counterexample",
            "does not promote the abstract scalar packing to realizability",
            "does not sum over source sizes, selectors, graph lines, or received pairs",
            "does not introduce or charge a new owner",
            "does not pay non-full-outside source load",
            "does not determine U_Q or residual U_A",
            "does not close rank nine, KoalaBear, or the complete theorem",
            "does not authorize rank at least ten, Lean, or stable-paper promotion",
        ],
        "source_bindings": source_bindings(),
    }
    certificate["payload_sha256"] = ""
    certificate["payload_sha256"] = payload_sha256(certificate)
    return certificate


def validate_candidate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    require(candidate.get("schema") == SCHEMA, "certificate schema mismatch")
    require(candidate.get("artifact_kind") == ARTIFACT_KIND, "artifact kind mismatch")
    require(candidate.get("status") == STATUS, "certificate status mismatch")
    require(candidate.get("payload_sha256") == payload_sha256(candidate), "payload self-hash mismatch")
    require(
        canonical_bytes(candidate) == canonical_bytes(expected),
        "certificate differs from canonical exact typed payload",
    )


def check_certificate() -> None:
    expected = build_certificate()
    actual = load_json_strict(CERT_PATH)
    validate_candidate(actual, expected)


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_suite() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-tampered")),
        ("artifact", lambda d: d.__setitem__("artifact_kind", "WRONG")),
        ("status", lambda d: d.__setitem__("status", "GREEN_GLOBAL")),
        ("row-p", lambda d: d["row"].__setitem__("p", P + 1)),
        ("row-p-float", lambda d: d["row"].__setitem__("p", float(P))),
        ("row-n", lambda d: d["row"].__setitem__("n", N - 1)),
        ("row-k", lambda d: d["row"].__setitem__("k", K - 1)),
        ("row-A", lambda d: d["row"].__setitem__("agreement_A", A - 1)),
        ("row-j", lambda d: d["row"].__setitem__("error_count_j", J + 1)),
        ("row-t", lambda d: d["row"].__setitem__("syndrome_depth_t", T + 1)),
        ("pred-schema", lambda d: d["predecessor"].__setitem__("schema", "wrong")),
        ("pred-payload", lambda d: d["predecessor"].__setitem__("payload_sha256", "0" * 64)),
        ("pred-commit", lambda d: d["predecessor"].__setitem__("stacked_on_commit", "0" * 40)),
        ("pred-restart", lambda d: d["predecessor"].__setitem__("exact_deletion_and_selector_restart_precede_this_packet", False)),
        ("deficit-bound", lambda d: d["full_histogram_lemma"].__setitem__("rich_line_deficit_bound", "delta<=u")),
        ("all-slope-mds", lambda d: d["full_histogram_lemma"].__setitem__("all_selected_deficits_nonnegative", False)),
        ("coverage-overclaim", lambda d: d["full_histogram_lemma"].__setitem__("rich_line_coverage_of_all_slopes_claimed", True)),
        ("line-cap", lambda d: d["full_histogram_lemma"].__setitem__("line_cap_nonpositive_floor", J)),
        ("subset-uniform", lambda d: d["full_histogram_lemma"].__setitem__("fixed_basis_graph_line_argument_is_subset_uniform", False)),
        ("same-selector", lambda d: d["full_histogram_lemma"].__setitem__("same_selector_provenance_required", False)),
        ("scan-min", lambda d: d["exact_scan"].__setitem__("scan_r_min", SCAN_R_MIN + 1)),
        ("scan-min-float", lambda d: d["exact_scan"].__setitem__("scan_r_min", float(SCAN_R_MIN))),
        ("scan-max", lambda d: d["exact_scan"].__setitem__("scan_r_max", SCAN_R_MAX - 1)),
        ("scan-count", lambda d: d["exact_scan"].__setitem__("scan_count", d["exact_scan"]["scan_count"] - 1)),
        ("scan-digest", lambda d: d["exact_scan"].__setitem__("scan_sha256", "f" * 64)),
        ("scan-interval", lambda d: d["exact_scan"]["intervals"][1].__setitem__(1, GAP_END + 1)),
        ("terminal-count", lambda d: d["exact_scan"]["terminal_counts"].__setitem__(OPEN_TERMINAL, GAP_COUNT - 1)),
        ("new-layer-count", lambda d: d["exact_scan"].__setitem__("newly_closed_layer_count", 26_548)),
        ("endpoint-cap", lambda d: d["exact_scan"]["endpoints"][4].__setitem__("full_histogram_cap", "0")),
        ("endpoint-margin", lambda d: d["exact_scan"]["endpoints"][6].__setitem__("budget_minus_cap", "0")),
        ("route-min", lambda d: d["scalar_route_cut"].__setitem__("gap_r_min", GAP_START + 1)),
        ("route-max", lambda d: d["scalar_route_cut"].__setitem__("gap_r_max", GAP_END - 1)),
        ("route-count", lambda d: d["scalar_route_cut"].__setitem__("route_relaxation_count", GAP_COUNT - 1)),
        ("route-digest", lambda d: d["scalar_route_cut"].__setitem__("route_sha256", "e" * 64)),
        ("route-target", lambda d: d["scalar_route_cut"].__setitem__("target_slope_count", str(B_REMAINING))),
        ("route-cutoff", lambda d: d["scalar_route_cut"].__setitem__("all_zero_deficits_defeat_every_nonnegative_cutoff", False)),
        ("route-selector", lambda d: d["scalar_route_cut"].__setitem__("actual_selector_or_counterexample_claimed", True)),
        ("first-lines", lambda d: d["scalar_route_cut"]["first_gap_control"].__setitem__("abstract_line_count", "0")),
        ("first-basis", lambda d: d["scalar_route_cut"]["first_gap_control"].__setitem__("global_basis_margin", "-1")),
        ("last-local", lambda d: d["scalar_route_cut"]["last_gap_control"].__setitem__("local_basis_margin", "-1")),
        ("last-rank9", lambda d: d["scalar_route_cut"]["last_gap_control"].__setitem__("rank9_capacity_margin", "-1")),
        ("ledger-U", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID + 1))),
        ("ledger-B", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING - 1))),
        ("ledger-move", lambda d: d["ledger"].__setitem__("ledger_movement", "1")),
        ("residual", lambda d: d["revised_residual"].__setitem__("only_remaining_full_outside_slack_interval", [GAP_START, GAP_END + 1])),
        ("residual-terminal", lambda d: d["revised_residual"].__setitem__("terminal", "PAID")),
        ("new-owner", lambda d: d["first_match_and_restart"].__setitem__("new_root_owner_added", True)),
        ("union-r", lambda d: d["first_match_and_restart"].__setitem__("union_over_r_forbidden", False)),
        ("global-close", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("rank9-close", lambda d: d["scope_guards"].__setitem__("complete_rank9_payment_proved", True)),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
        ("source-remove", lambda d: d["source_bindings"].pop(next(iter(d["source_bindings"])))),
        ("source-hash", lambda d: d["source_bindings"].__setitem__(next(iter(d["source_bindings"])), "0" * 64)),
        ("payload", lambda d: d.__setitem__("payload_sha256", "0" * 64)),
    ]


def run_tamper_selftest() -> None:
    expected = build_certificate()
    mutations = mutation_suite()
    rejected = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        if name != "payload":
            candidate["payload_sha256"] = payload_sha256(candidate)
        try:
            validate_candidate(candidate, expected)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError(f"tamper mutation accepted: {name}")
    parser_mutations = [
        ("float", '{"x":1.0}'),
        ("negative-float", '{"x":-0.5}'),
        ("nan", '{"x":NaN}'),
        ("infinity", '{"x":Infinity}'),
        ("negative-infinity", '{"x":-Infinity}'),
        ("duplicate-key", '{"x":1,"x":2}'),
    ]
    parser_rejected = 0
    for name, text in parser_mutations:
        try:
            parse_json_strict_text(text)
        except RuntimeError:
            parser_rejected += 1
        else:
            raise RuntimeError(f"strict parser mutation accepted: {name}")
    require(rejected == len(mutations), "semantic tamper rejection count drift")
    require(parser_rejected == len(parser_mutations), "parser rejection count drift")
    total = rejected + parser_rejected
    expected_total = len(mutations) + len(parser_mutations)
    print(f"M1 full-histogram incidence mutations: {total}/{expected_total} PASS")


def write_certificate() -> None:
    value = build_certificate()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    print(CERT_PATH.relative_to(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--write-certificate", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    args = parser.parse_args()

    if args.check:
        check_certificate()
        print("M1 KoalaBear full-histogram incidence closure: PASS")
        print("  paid ranges: 196..67,470 and 209,553..913,631")
        print("  scalar route cut: 67,471..209,552 (142,082 layers)")
        print("  ledger movement: 0; rank nine and KoalaBear remain OPEN")
    elif args.tamper_selftest:
        run_tamper_selftest()
    elif args.write_certificate:
        write_certificate()
    else:
        print(json.dumps(build_certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
