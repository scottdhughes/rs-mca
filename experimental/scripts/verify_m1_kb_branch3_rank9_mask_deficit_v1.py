#!/usr/bin/env python3
"""Verify the KoalaBear rank-nine mask-deficit route cut and compiler.

This packet specializes the imported nonuniform actual-core inequality to the
rank-nine residual left by the branch-3 rank ladder.  It proves two things:

1. M2b plus the currently exported scalar/support-size constraints still has
   the all-zero deficit histogram as its sharp optimizer, so those inputs alone
   cannot improve the predecessor's coarse cap.
2. A proved cumulative deficit-tail bound has an exact fail-closed compiler,
   with sharp integer thresholds and a generic multi-cut extension.

The all-zero histogram is an interface-level extremizer, not a constructed
deployed Reed--Solomon witness.  No charge or closure is banked.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-rank9-mask-deficit-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_RANK9_MASK_DEFICIT_ROUTE_CUT"
STATUS = (
    "PROVED_CURRENT_SCALAR_INTERFACE_ROUTE_CUT_AND_SHARP_DEFICIT_TAIL_COMPILER_"
    "NO_LEDGER_MOVEMENT"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-rank9-mask-deficit-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_rank9_mask_deficit_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-mask-deficit-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.sage"
)

RANK_LADDER_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_actual_core_mds_rank_ladder_v1.md"
)
RANK_LADDER_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-actual-core-mds-v1/"
    "m1_kb_branch3_actual_core_mds_v1.json"
)
RANK_LADDER_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py"
)
TDD_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_tdd_excess_v1.md"
)
TDD_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-tdd-excess-v1/"
    "m1_kb_branch3_tdd_excess_v1.json"
)
TDD_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py"
)
ACTUAL_CORE_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "a6_actual_witness_core_rank_preflight.md"
)
ACTUAL_CORE_VERIFIER_REL = Path(
    "experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py"
)

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
DELTA_ZERO = R - J
MINIMUM_DISTANCE = R + 1
HEAVY_FLOOR_L = 349_526
MAX_DEFICIT = J - HEAVY_FLOOR_L
MIN_GLOBAL_UNPAID_EXCESS = 11

RANK_S = 9
CORE_R = 8
BASIS_SUPPORTS = 10

DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID
COUNTEREXAMPLE_SIZE = B_REMAINING + 1

COARSE_BOUNDARIES = {
    1: 1_699_344,
    2: 1_835_392,
    3: 1_919_971,
    4: 1_982_333,
    5: 2_032_097,
    6: 2_073_683,
}

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "row",
    "predecessor_contract",
    "rank9_m2b_specialization",
    "exported_histogram_constraints",
    "unconstrained_optimizer",
    "coarse_failure_controls",
    "one_cut_tail_frontier",
    "multi_cut_compiler",
    "classifier_contract",
    "exact_controls",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not construct an actual deployed RS rank-nine family.",
    "This packet does not prove that the all-zero deficit profile is realizable.",
    "This packet does not rule out a new syndrome-line incidence theorem.",
    "This packet does not supply the missing cumulative deficit-tail lemma.",
    "This packet does not pay the complete rank-nine residual.",
    "This packet does not bank an unconditional charge.",
    "This packet does not prove branch 3 closed.",
    "This packet does not prove the KoalaBear row safe.",
    "This packet does not attack intrinsic rank at least ten.",
    "This packet does not authorize Lean or Paper-D promotion.",
]


class VerificationError(RuntimeError):
    """A source, arithmetic, schema, or semantic check failed."""


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
        binding("packet-note", NOTE_REL, "load-bearing route-cut note"),
        binding("packet-readme", README_REL, "replay instructions"),
        binding("packet-verifier", PYTHON_REL, "exact optimizer verifier"),
        binding("sage-control", SAGE_REL, "independent exact toy control"),
        binding(
            "rank-ladder-note",
            RANK_LADDER_NOTE_REL,
            "rank-nine coarse failure predecessor",
        ),
        binding(
            "rank-ladder-certificate",
            RANK_LADDER_CERT_REL,
            "frozen rank-nine carrier boundaries",
        ),
        binding(
            "rank-ladder-verifier",
            RANK_LADDER_VERIFIER_REL,
            "rank-ladder predecessor replay",
        ),
        binding(
            "tdd-note",
            TDD_NOTE_REL,
            "complete selector and heavy-weight floor",
        ),
        binding(
            "tdd-certificate",
            TDD_CERT_REL,
            "frozen complete-selector state",
        ),
        binding(
            "tdd-verifier",
            TDD_VERIFIER_REL,
            "complete-selector predecessor replay",
        ),
        binding(
            "actual-core-theorem",
            ACTUAL_CORE_NOTE_REL,
            "imported set-pair and M2b inequalities",
        ),
        binding(
            "actual-core-verifier",
            ACTUAL_CORE_VERIFIER_REL,
            "imported theorem replay",
        ),
    ]


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator > 0, "invalid ceiling division")
    return (numerator + denominator - 1) // denominator


def extension_factor(source_distance: int, deficit: int) -> int:
    require(1 <= source_distance <= R, "source distance outside 1..R")
    require(0 <= deficit <= MAX_DEFICIT, "deficit outside deployed range")
    return max(1, source_distance - J + deficit)


def multiplicity(source_distance: int, deficit: int) -> int:
    ell = extension_factor(source_distance, deficit)
    basis_count = math.comb(DELTA_ZERO + CORE_R + deficit, CORE_R)
    return ceil_div(ell * basis_count, RANK_S)


def set_pair_denominator(deficit: int) -> int:
    require(0 <= deficit <= MAX_DEFICIT, "set-pair deficit out of range")
    return math.comb(J + RANK_S - deficit, RANK_S)


def validate_source_contracts(
    *,
    rank_ladder_override: dict[str, Any] | None = None,
    tdd_override: dict[str, Any] | None = None,
    theorem_text_override: str | None = None,
) -> None:
    """Validate semantic predecessor anchors before blessing source hashes."""

    rank_ladder = (
        rank_ladder_override
        if rank_ladder_override is not None
        else load_json(ROOT / RANK_LADDER_CERT_REL)
    )
    require(
        rank_ladder.get("schema") == "rs-mca-m1-kb-branch3-actual-core-mds-v1",
        "rank-ladder predecessor schema drift",
    )
    require(
        rank_ladder.get("payload_sha256") == payload_hash(rank_ladder),
        "rank-ladder predecessor payload drift",
    )
    rank_row = rank_ladder.get("row", {})
    require(
        (
            rank_row.get("n"),
            rank_row.get("k"),
            rank_row.get("agreement_A"),
            rank_row.get("redundancy_R"),
            rank_row.get("error_cap_j"),
            rank_row.get("zero_mask_surplus_Delta0"),
            rank_row.get("B_remaining"),
        )
        == (N, K, A, R, J, DELTA_ZERO, str(B_REMAINING)),
        "rank-ladder deployed row drift",
    )
    rank_contract = rank_ladder.get("predecessor_contract", {})
    require(
        rank_contract.get("rank_minimizing_complete_selector_fixed_before_anchors")
        is True,
        "rank-minimizing complete selector contract drift",
    )
    require(
        rank_contract.get("transverse_actual_witness_contract") is True,
        "rank-ladder transversality contract drift",
    )
    require(
        rank_contract.get("basis_carrier_equals_complete_selected_union") is True,
        "rank-ladder complete-union contract drift",
    )
    restricted = rank_ladder.get("restricted_mds_splice", {})
    require(
        restricted.get("actual_core_rank") == "r=s_star-1"
        and restricted.get("rank_carrier_lift_values_from_same_selector_and_restriction")
        is True
        and restricted.get("source_minimum_lift")
        == "d_V=MIN{wt(z):H_V z=y1}",
        "rank-ladder restricted-MDS contract drift",
    )
    ladder = rank_ladder.get("rank_ladder", {})
    require(
        (
            ladder.get("first_rank_not_uniformly_paid"),
            ladder.get("rank9_residual_core_rank"),
            ladder.get("rank9_basis_carrier_supports"),
        )
        == (RANK_S, CORE_R, BASIS_SUPPORTS),
        "rank-nine predecessor boundary drift",
    )
    joint = ladder.get("rank9_joint_boundary", [])
    require(len(joint) == 7, "rank-nine joint-boundary row count drift")
    require(
        [row.get("extension_factor_ell_q") for row in joint] == list(range(1, 8)),
        "rank-nine extension-factor rows drift",
    )
    require(
        [row.get("largest_paid_carrier_size") for row in joint]
        == [COARSE_BOUNDARIES[i] for i in range(1, 7)] + [N],
        "rank-nine carrier boundaries drift",
    )
    require(
        ladder.get("larger_actual_masks_or_nonuniform_sum_may_pay_inside_failure_region")
        is True,
        "rank-ladder nonuniform handoff drift",
    )
    rank_ledger = rank_ladder.get("ledger", {})
    require(
        rank_ledger.get("packet_banked_charge") == "0"
        and rank_ledger.get("U_paid_before") == rank_ledger.get("U_paid_after")
        and rank_ledger.get("B_remaining_before")
        == rank_ledger.get("B_remaining_after")
        and rank_ledger.get("branch3_closed") is False,
        "rank-ladder ledger contract drift",
    )

    tdd = (
        tdd_override
        if tdd_override is not None
        else load_json(ROOT / TDD_CERT_REL)
    )
    require(
        tdd.get("schema") == "rs-mca-m1-kb-branch3-tdd-excess-v1",
        "TDD predecessor schema drift",
    )
    require(
        tdd.get("payload_sha256") == payload_hash(tdd),
        "TDD predecessor payload drift",
    )
    tdd_row = tdd.get("row", {})
    require(
        (
            tdd_row.get("n"),
            tdd_row.get("redundancy_R"),
            tdd_row.get("error_cap_j"),
            tdd_row.get("surviving_error_weight_floor_L"),
            tdd_row.get("B_remaining"),
        )
        == (N, R, J, HEAVY_FLOOR_L, str(B_REMAINING)),
        "TDD deployed row or heavy floor drift",
    )
    bridge = tdd.get("defect_span_bridge", {})
    require(
        bridge.get("chosen_selector_attains_intrinsic_minimum") is True
        and bridge.get("rank_identity")
        == "s_star=1+dim(R_sel)_FOR_MINIMIZING_SELECTOR"
        and bridge.get("basis_carrier_support_count") == "s_star+1"
        and bridge.get("basis_carrier_equals_complete_selected_union") is True,
        "TDD selector/rank/carrier bridge drift",
    )
    tdd_ledger = tdd.get("ledger", {})
    require(
        tdd_ledger.get("packet_banked_charge") == "0"
        and tdd_ledger.get("U_paid_before") == tdd_ledger.get("U_paid_after")
        and tdd_ledger.get("B_remaining_before")
        == tdd_ledger.get("B_remaining_after")
        and tdd_ledger.get("branch3_closed") is False,
        "TDD ledger contract drift",
    )

    theorem_text = (
        theorem_text_override
        if theorem_text_override is not None
        else (ROOT / ACTUAL_CORE_NOTE_REL).read_text(encoding="utf-8")
    )
    compact = " ".join(theorem_text.split())
    theorem_anchors = [
        "sum_(gamma in Z) 1/binom(s+wt(c_gamma),s) <=1, (P2)",
        "a_gamma=|T_gamma|, ell_gamma=max(1,d+a_gamma-N),",
        "mu_gamma=ceil[ (ell_gamma/s) binom(a_gamma-kappa+r,r) ]. (M2a)",
        "sum_gamma mu_gamma<=binom(N,s). (M2b)",
    ]
    for anchor in theorem_anchors:
        require(anchor in compact, f"actual-core theorem anchor drift: {anchor}")


def coarse_cap(carrier_size: int, source_distance: int) -> int:
    require(
        R + MIN_GLOBAL_UNPAID_EXCESS <= carrier_size <= N,
        "carrier size outside residual range",
    )
    return math.comb(carrier_size, RANK_S) // multiplicity(source_distance, 0)


def max_count_with_one_cut(
    carrier_size: int,
    source_distance: int,
    cutoff: int,
    low_count_cap: int,
) -> int:
    require(0 <= cutoff < MAX_DEFICIT, "cutoff outside 0..Delta_max-1")
    require(low_count_cap >= 0, "negative low-deficit cap")
    budget = math.comb(carrier_size, RANK_S)
    mu0 = multiplicity(source_distance, 0)
    mu_high = multiplicity(source_distance, cutoff + 1)
    cheap = min(low_count_cap, budget // mu0)
    return cheap + (budget - cheap * mu0) // mu_high


def one_cut_gate(
    carrier_size: int,
    source_distance: int,
    cutoff: int,
) -> dict[str, Any]:
    require(0 <= cutoff < MAX_DEFICIT, "cutoff outside 0..Delta_max-1")
    budget = math.comb(carrier_size, RANK_S)
    target_size = COUNTEREXAMPLE_SIZE
    mu0 = multiplicity(source_distance, 0)
    mu_high = multiplicity(source_distance, cutoff + 1)
    gain = mu_high - mu0
    require(gain > 0, "deficit multiplicity is not strictly increasing")
    excess_needed = budget + 1 - target_size * mu0
    if excess_needed <= 0:
        required_high = 0
        maximum_low = target_size
        useful = True
    else:
        required_high = ceil_div(excess_needed, gain)
        maximum_low = target_size - required_high
        useful = maximum_low >= 0
    result: dict[str, Any] = {
        "carrier_size_N_V": carrier_size,
        "source_minimum_lift_d_V": source_distance,
        "coarse_extension_factor": max(1, source_distance - J),
        "cutoff_D": cutoff,
        "first_high_deficit": cutoff + 1,
        "ambient_budget_C_N_choose_9": str(budget),
        "target_counterexample_size_m": str(target_size),
        "mu_0": str(mu0),
        "mu_D_plus_1": str(mu_high),
        "per_high_item_gain": str(gain),
        "excess_weight_needed": str(excess_needed),
        "required_high_deficit_count": str(required_high),
        "formal_T_star": str(maximum_low),
        "largest_sufficient_low_deficit_cap_T_star": (
            str(maximum_low) if useful else None
        ),
        "one_cut_can_close": useful,
    }
    if useful:
        good_cost = maximum_low * mu0 + required_high * mu_high
        bad_low = maximum_low + 1
        bad_high = target_size - bad_low
        bad_cost = bad_low * mu0 + bad_high * mu_high
        result.update(
            {
                "minimum_weight_at_T_star": str(good_cost),
                "good_cost_excess_over_C": str(good_cost - budget),
                "sharp_bad_low_count": str(bad_low),
                "sharp_bad_high_count": str(bad_high),
                "sharp_bad_weight": str(bad_cost),
                "sharp_bad_slack_below_C": str(budget - bad_cost),
                "cap_at_T_star": str(
                    max_count_with_one_cut(
                        carrier_size,
                        source_distance,
                        cutoff,
                        maximum_low,
                    )
                ),
                "cap_at_T_star_plus_1": str(
                    max_count_with_one_cut(
                        carrier_size,
                        source_distance,
                        cutoff,
                        maximum_low + 1,
                    )
                ),
            }
        )
    return result


def first_useful_cutoff(carrier_size: int, source_distance: int) -> int:
    target_size = COUNTEREXAMPLE_SIZE
    budget = math.comb(carrier_size, RANK_S)

    def useful(cutoff: int) -> bool:
        return (
            target_size * multiplicity(source_distance, cutoff + 1)
            > budget
        )

    require(useful(MAX_DEFICIT - 1), "no useful cutoff in deficit range")
    lower = 0
    upper = MAX_DEFICIT - 1
    while lower < upper:
        middle = (lower + upper) // 2
        if useful(middle):
            upper = middle
        else:
            lower = middle + 1
    return lower


def prefix_minimum_weight(
    source_distance: int,
    total_size: int,
    cuts: list[tuple[int, int]],
) -> int:
    require(total_size >= 0, "negative histogram size")
    previous_cutoff = -1
    previous_cap = 0
    weight = 0
    for cutoff, cap in cuts:
        require(
            0 <= cutoff < MAX_DEFICIT,
            "multi-cut cutoff outside 0..Delta_max-1",
        )
        require(cutoff > previous_cutoff, "multi-cut cutoffs not strictly increasing")
        require(previous_cap <= cap <= total_size, "multi-cut caps not monotone")
        bin_count = cap - previous_cap
        cheapest_deficit = 0 if previous_cutoff < 0 else previous_cutoff + 1
        weight += bin_count * multiplicity(source_distance, cheapest_deficit)
        previous_cutoff = cutoff
        previous_cap = cap
    tail_deficit = 0 if previous_cutoff < 0 else previous_cutoff + 1
    weight += (total_size - previous_cap) * multiplicity(
        source_distance, tail_deficit
    )
    return weight


def classify_tail_certificate(
    *,
    predecessor_rank9_contract_present: bool = False,
    complete_rank_minimizing_selector: bool = False,
    intrinsic_affine_rank: int | None = None,
    same_restricted_map_and_selector: bool = False,
    carrier_size_certified: bool = False,
    source_distance_mode: str | None = None,
    exact_source_distance_certified: bool = False,
    cumulative_tail_lemma_proved: bool = False,
    carrier_size: int | None = None,
    source_distance_used: int | None = None,
    cutoff: int | None = None,
    low_count_cap: int | None = None,
) -> str:
    if (
        not predecessor_rank9_contract_present
        or not complete_rank_minimizing_selector
        or intrinsic_affine_rank != RANK_S
        or not same_restricted_map_and_selector
        or not carrier_size_certified
        or carrier_size is None
        or source_distance_used is None
    ):
        return "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED"
    if source_distance_mode not in {
        "UNIVERSAL_D_GE_1",
        "EXACT_MATCHED_D_V",
    }:
        return "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED"
    if source_distance_mode == "UNIVERSAL_D_GE_1":
        if source_distance_used != 1:
            return "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED"
    elif not exact_source_distance_certified:
        return "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED"
    if coarse_cap(carrier_size, source_distance_used) <= B_REMAINING:
        return "PAID_BY_PREDECESSOR_COARSE_RANK9_BOUND"
    if not cumulative_tail_lemma_proved:
        return "UNPAID_CURRENT_SCALAR_INTERFACE_ALL_ZERO_DEFICIT_EXTREMIZER"
    if cutoff is None or low_count_cap is None or low_count_cap < 0:
        return "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED"
    gate = one_cut_gate(carrier_size, source_distance_used, cutoff)
    if not gate["one_cut_can_close"]:
        return "UNPAID_RANK9_ONE_CUT_TAIL_INSUFFICIENT"
    maximum = int(gate["largest_sufficient_low_deficit_cap_T_star"])
    if low_count_cap <= maximum:
        return "PAID_BY_PROVED_RANK9_M2B_CUMULATIVE_DEFICIT_TAIL"
    return "UNPAID_RANK9_ONE_CUT_TAIL_INSUFFICIENT"


def expected_row() -> dict[str, Any]:
    return {
        "row_id": "koalabear-mca-A1116048",
        "p": P,
        "ambient_extension_degree": EXTENSION_DEGREE,
        "q_line": str(Q_LINE),
        "n": N,
        "k": K,
        "agreement_A": A,
        "redundancy_R": R,
        "error_cap_j": J,
        "post_deep_weight_floor_L": HEAVY_FLOOR_L,
        "maximum_deficit_Delta_max": MAX_DEFICIT,
        "zero_mask_surplus_Delta0": DELTA_ZERO,
        "minimum_distance": MINIMUM_DISTANCE,
        "B_star": str(B_STAR),
        "U_paid": str(U_PAID),
        "B_remaining": str(B_REMAINING),
        "first_forbidden_family_size": str(COUNTEREXAMPLE_SIZE),
    }


def expected_predecessor_contract() -> dict[str, Any]:
    return {
        "rank_ladder_schema": "rs-mca-m1-kb-branch3-actual-core-mds-v1",
        "tdd_schema": "rs-mca-m1-kb-branch3-tdd-excess-v1",
        "one_rank_minimizing_complete_selector": True,
        "intrinsic_affine_rank_s": RANK_S,
        "actual_core_rank_r": CORE_R,
        "basis_support_count": BASIS_SUPPORTS,
        "basis_carrier_equals_complete_union": True,
        "carrier_notation": "N_V=R+nu",
        "carrier_range": [R + MIN_GLOBAL_UNPAID_EXCESS, N],
        "same_selector_and_restricted_H_V_required": True,
        "source_semantic_contracts_validated": True,
        "source_minimum_lift_range": [1, R],
        "selected_weight_range": [HEAVY_FLOOR_L, J],
        "coarse_failure_boundaries_ell_1_to_6": [
            COARSE_BOUNDARIES[ell] for ell in range(1, 7)
        ],
        "rank_at_least_ten_out_of_scope": True,
    }


def expected_rank9_specialization() -> dict[str, Any]:
    return {
        "deficit_definition": "delta_eta=j-|E_eta|",
        "actual_mask_definition": "a_eta=N_V-|E_eta|",
        "deficit_range": [0, MAX_DEFICIT],
        "actual_mask_identity": "a_eta=nu+Delta0+delta_eta",
        "binomial_identity": "a_eta-nu+r=67480+delta_eta",
        "extension_identity": "ell_eta=max(1,d_V-j+delta_eta)",
        "multiplicity_formula": (
            "mu_d(delta)=CEIL(max(1,d_V-j+delta)*"
            "BINOM(67480+delta,8)/9)"
        ),
        "m2b_histogram_formula": (
            "SUM_delta h_delta*mu_d(delta)<=BINOM(N_V,9)"
        ),
        "multiplicity_strictly_increasing": True,
        "strictness_witness": (
            "BINOM(67481+delta,8)-BINOM(67480+delta,8)="
            "BINOM(67480+delta,7)>9"
        ),
        "ceilings_are_load_bearing": True,
        "d_V_common_to_one_selector": True,
        "ell_0_does_not_determine_positive_deficit_multiplicities": True,
    }


def expected_exported_constraints() -> dict[str, Any]:
    minimum_first_unpaid = min(value + 1 for value in COARSE_BOUNDARIES.values())
    return {
        "histogram_integrality": "h_delta IN Z_GE_0",
        "histogram_total": "SUM_delta h_delta=|Gamma|",
        "deficit_support": [0, MAX_DEFICIT],
        "m2b": "SUM h_delta*mu_d(delta)<=BINOM(N_V,9)",
        "set_pair_P2": (
            "SUM h_delta/BINOM(j+9-delta,9)<=1"
        ),
        "pairwise_difference_gate": (
            "delta_eta+delta_theta<=2j-d_V FOR eta!=theta"
        ),
        "transversality_support_gate": "selected supports form an antichain",
        "complete_union_gate": "UNION_eta E_eta=V",
        "zero_mask_intersection_gate": "INTERSECTION_eta T_eta=EMPTY",
        "minimum_coarse_failure_carrier": minimum_first_unpaid,
        "all_coarse_failure_carriers_exceed_j": minimum_first_unpaid > J,
        "all_coarse_failure_carriers_below_3j": N < 3 * J,
        "ten_j_sets_have_enough_total_size": BASIS_SUPPORTS * J > N,
        "no_exported_positive_deficit_tail_bound": True,
        "no_exported_average_deficit_bound": True,
    }


def all_zero_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ell in range(1, 7):
        carrier_size = COARSE_BOUNDARIES[ell] + 1
        source_distance = 1 if ell == 1 else J + ell
        mu0 = multiplicity(source_distance, 0)
        budget = math.comb(carrier_size, RANK_S)
        cost = COUNTEREXAMPLE_SIZE * mu0
        rows.append(
            {
                "coarse_extension_factor": ell,
                "first_unpaid_carrier_size": carrier_size,
                "source_distance_control": source_distance,
                "all_zero_mu_0": str(mu0),
                "m2b_budget": str(budget),
                "all_zero_candidate_cost": str(cost),
                "all_zero_candidate_m2b_feasible": cost <= budget,
                "coarse_cap": str(budget // mu0),
            }
        )
    return rows


def expected_unconstrained_optimizer() -> dict[str, Any]:
    minimum_first_unpaid = min(value + 1 for value in COARSE_BOUNDARIES.values())
    set_pair_denom = set_pair_denominator(0)
    min_binomial_support_count = math.comb(minimum_first_unpaid, RANK_S)
    return {
        "integer_program": (
            "MAX SUM h_delta SUBJECT TO SUM mu_d(delta)h_delta<=C, "
            "h_delta IN Z_GE_0"
        ),
        "optimizer_from_strict_weight_monotonicity": (
            "h_0=FLOOR(BINOM(N_V,9)/mu_d(0)); h_delta=0 FOR delta>0"
        ),
        "all_zero_test_size": str(COUNTEREXAMPLE_SIZE),
        "all_zero_passes_each_first_unpaid_m2b_cell": all(
            row["all_zero_candidate_m2b_feasible"] for row in all_zero_rows()
        ),
        "all_zero_set_pair_denominator": str(set_pair_denom),
        "all_zero_passes_set_pair_P2": COUNTEREXAMPLE_SIZE <= set_pair_denom,
        "all_zero_pairwise_rhs_at_largest_d": 2 * J - R,
        "all_zero_passes_pairwise_gate": 0 <= 2 * J - R,
        "equal_size_distinct_supports_are_an_antichain": True,
        "distinct_j_supports_available_lower_bound": str(
            min_binomial_support_count
        ),
        "distinct_j_supports_available_for_test_size": (
            min_binomial_support_count >= COUNTEREXAMPLE_SIZE
        ),
        "two_or_three_distinct_j_sets_can_cover_every_failure_carrier": True,
        "cover_construction": (
            "IF N_V<=2j USE [0,j) AND [N_V-j,N_V); "
            "ELSE USE [0,j),[j,2j),[2j,N_V) UNION [0,3j-N_V)"
        ),
        "support_fixture_scope": (
            "CARDINALITY_ANTICHAIN_AND_UNION_ONLY_NOT_VECTOR_REALIZABILITY"
        ),
        "route_cut": (
            "CURRENT_EXPORTED_SCALAR_CONSTRAINTS_DO_NOT_EXCLUDE_ALL_ZERO_DEFICIT"
        ),
        "actual_RS_extremizer_constructed": False,
    }


def exact_distance_frontier_rows() -> list[dict[str, Any]]:
    cases = [
        ("UNIVERSAL_D_V_GE_1", 1),
        ("EXACT_d_minus_j_EQ_1", J + 1),
        ("EXACT_d_minus_j_EQ_2", J + 2),
        ("EXACT_d_minus_j_EQ_3", J + 3),
        ("EXACT_d_minus_j_EQ_4", J + 4),
        ("EXACT_d_minus_j_EQ_5", J + 5),
        ("EXACT_d_minus_j_EQ_6", J + 6),
    ]
    rows: list[dict[str, Any]] = []
    for label, source_distance in cases:
        cutoff = first_useful_cutoff(N, source_distance)
        gate = one_cut_gate(N, source_distance, cutoff)
        previous = one_cut_gate(N, source_distance, cutoff - 1) if cutoff else None
        rows.append(
            {
                "distance_case": label,
                "source_minimum_lift_d_V": source_distance,
                "d_V_minus_j": source_distance - J,
                "coarse_extension_factor": max(1, source_distance - J),
                "first_useful_cutoff_D": cutoff,
                "previous_cut_can_close": (
                    previous["one_cut_can_close"] if previous is not None else None
                ),
                "previous_T_star": (
                    previous["largest_sufficient_low_deficit_cap_T_star"]
                    if previous is not None
                    else None
                ),
                "first_gate": gate,
            }
        )
    return rows


def largest_carrier_where_h0_cut_can_help(source_distance: int) -> int:
    mu_high = multiplicity(source_distance, 1)

    def useful(carrier_size: int) -> bool:
        return COUNTEREXAMPLE_SIZE * mu_high > math.comb(carrier_size, RANK_S)

    lower = R + MIN_GLOBAL_UNPAID_EXCESS
    if not useful(lower):
        return lower - 1
    if useful(N):
        return N
    upper = N
    while lower < upper:
        middle = (lower + upper + 1) // 2
        if useful(middle):
            lower = middle
        else:
            upper = middle - 1
    return lower


def universal_anchor_rows() -> list[dict[str, Any]]:
    return [
        one_cut_gate(N, 1, cutoff)
        for cutoff in [18_014, 20_000, 50_000, 100_000, MAX_DEFICIT - 1]
    ]


def expected_one_cut_frontier() -> dict[str, Any]:
    universal_cutoff = first_useful_cutoff(N, 1)
    universal_gate = one_cut_gate(N, 1, universal_cutoff)
    previous_gate = one_cut_gate(N, 1, universal_cutoff - 1)
    h0_cases = []
    for b in [1 - J, 1, 2, 3, 4, 5, 6]:
        source_distance = 1 if b == 1 - J else J + b
        h0_cases.append(
            {
                "d_V_minus_j": b,
                "source_minimum_lift_d_V": source_distance,
                "largest_carrier_where_an_h0_cap_can_help": (
                    largest_carrier_where_h0_cut_can_help(source_distance)
                ),
            }
        )
    return {
        "one_cut_definition": "H_D=SUM_(delta<=D) h_delta",
        "sharp_formula": (
            "T_star=FLOOR(((B_remaining+1)*mu(D+1)-C-1)/"
            "(mu(D+1)-mu(0)))"
        ),
        "equivalent_high_count_formula": (
            "L_D=CEIL((C+1-(B_remaining+1)*mu(0))/"
            "(mu(D+1)-mu(0))); T_star=B_remaining+1-L_D"
        ),
        "sufficient_implication": (
            "PROVED H_D<=T_star IMPLIES |Gamma|<=B_remaining"
        ),
        "sharpness_scope": "SHARP_FOR_THE_ONE_CUT_M2B_HISTOGRAM_RELAXATION",
        "different_cutoffs_are_incomparable": True,
        "worst_corner_for_each_fixed_cutoff": "N_V=n AND d_V=1",
        "worst_corner_monotonicity": (
            "BINOM(N_V,9) INCREASES IN N_V; mu_d(delta) INCREASES IN d_V"
        ),
        "universal_first_useful_cutoff_D": universal_cutoff,
        "universal_previous_gate": previous_gate,
        "universal_first_gate": universal_gate,
        "universal_anchor_curve": universal_anchor_rows(),
        "exact_distance_frontiers_at_full_carrier": exact_distance_frontier_rows(),
        "h0_only_usefulness_by_distance": h0_cases,
        "single_h0_cap_uniformly_sufficient": False,
        "ell_0_equal_one_loses_exact_distance_information": True,
    }


def expected_multi_cut_compiler() -> dict[str, Any]:
    toy_cuts = [(0, 3), (2, 7)]
    toy_total = 10
    toy_d = 1
    return {
        "input_contract": (
            "0<=D_1<...<D_k<Delta_max AND 0<=T_1<=...<=T_k<=m"
        ),
        "exact_greedy_formula": (
            "T_1*mu(0)+SUM_(i>=2)(T_i-T_(i-1))*mu(D_(i-1)+1)+"
            "(m-T_k)*mu(D_k+1)"
        ),
        "why_greedy_is_exact": "mu_d(delta) is strictly increasing",
        "empty_cut_behavior": "all m items use deficit zero",
        "toy_input": {
            "source_distance": toy_d,
            "total_size": toy_total,
            "cuts": [[d, t] for d, t in toy_cuts],
        },
        "toy_exact_minimum_weight": str(
            prefix_minimum_weight(toy_d, toy_total, toy_cuts)
        ),
        "incidence_proof_required_before_payment": True,
    }


def expected_classifier_contract() -> dict[str, Any]:
    universal = one_cut_gate(N, 1, 18_014)
    universal_t = int(universal["largest_sufficient_low_deficit_cap_T_star"])
    exact_b1 = one_cut_gate(N, J + 1, 5)
    exact_b1_t = int(exact_b1["largest_sufficient_low_deficit_cap_T_star"])
    base = {
        "predecessor_rank9_contract_present": True,
        "complete_rank_minimizing_selector": True,
        "intrinsic_affine_rank": 9,
        "same_restricted_map_and_selector": True,
        "carrier_size_certified": True,
        "source_distance_mode": "UNIVERSAL_D_GE_1",
        "exact_source_distance_certified": False,
        "carrier_size": N,
        "source_distance_used": 1,
    }
    return {
        "fail_closed_defaults": classify_tail_certificate(),
        "missing_predecessor_rank9_contract": classify_tail_certificate(
            **{
                **base,
                "predecessor_rank9_contract_present": False,
            }
        ),
        "current_interface_only": classify_tail_certificate(**base),
        "universal_tail_paid": classify_tail_certificate(
            **base,
            cumulative_tail_lemma_proved=True,
            cutoff=18_014,
            low_count_cap=universal_t,
        ),
        "universal_tail_boundary_plus_one": classify_tail_certificate(
            **base,
            cumulative_tail_lemma_proved=True,
            cutoff=18_014,
            low_count_cap=universal_t + 1,
        ),
        "universal_previous_cut": classify_tail_certificate(
            **base,
            cumulative_tail_lemma_proved=True,
            cutoff=18_013,
            low_count_cap=0,
        ),
        "negative_tail_cap_rejected": classify_tail_certificate(
            **base,
            cumulative_tail_lemma_proved=True,
            cutoff=18_014,
            low_count_cap=-1,
        ),
        "unproved_numerical_tail_not_owner": classify_tail_certificate(
            **base,
            cumulative_tail_lemma_proved=False,
            cutoff=18_014,
            low_count_cap=universal_t,
        ),
        "unmatched_exact_distance": classify_tail_certificate(
            **{
                **base,
                "source_distance_mode": "EXACT_MATCHED_D_V",
                "source_distance_used": J + 1,
            },
            cumulative_tail_lemma_proved=True,
            cutoff=5,
            low_count_cap=exact_b1_t,
        ),
        "matched_exact_distance_paid": classify_tail_certificate(
            **{
                **base,
                "source_distance_mode": "EXACT_MATCHED_D_V",
                "source_distance_used": J + 1,
                "exact_source_distance_certified": True,
            },
            cumulative_tail_lemma_proved=True,
            cutoff=5,
            low_count_cap=exact_b1_t,
        ),
        "predecessor_boundary_paid": classify_tail_certificate(
            **{
                **base,
                "carrier_size": COARSE_BOUNDARIES[1],
            }
        ),
        "required_flags": [
            "complete_rank_minimizing_selector",
            "predecessor_rank9_actual_core_contract",
            "intrinsic_affine_rank_exactly_9",
            "same_restricted_map_and_selector",
            "carrier_size_certified",
            "universal_d_ge_1_or_exact_matched_d_V",
            "proved_cumulative_tail_lemma",
        ],
    }


def expected_exact_controls() -> dict[str, Any]:
    universal = one_cut_gate(N, 1, 18_014)
    bad_low = int(universal["sharp_bad_low_count"])
    bad_high = int(universal["sharp_bad_high_count"])
    bad_deficit = 18_015
    set_pair_value = (
        Fraction(bad_low, set_pair_denominator(0))
        + Fraction(bad_high, set_pair_denominator(bad_deficit))
    )
    return {
        "constant_identities": {
            "R_equals_n_minus_k": R == N - K,
            "j_equals_n_minus_A": J == N - A,
            "Delta0_equals_R_minus_j_equals_A_minus_k": (
                DELTA_ZERO == R - J == A - K
            ),
            "Delta_max_equals_j_minus_L": MAX_DEFICIT == J - HEAVY_FLOOR_L,
            "rank9_r_equals_8": CORE_R == RANK_S - 1,
            "B_star_equals_U_paid_plus_B_remaining": (
                B_STAR == U_PAID + B_REMAINING
            ),
        },
        "all_zero_first_unpaid_cells": all_zero_rows(),
        "full_carrier_universal_all_zero_cap": str(coarse_cap(N, 1)),
        "full_carrier_universal_all_zero_over_budget_by": str(
            coarse_cap(N, 1) - B_REMAINING
        ),
        "universal_first_cut_expected": {
            "D": 18_014,
            "T_star": "17907572507584",
            "required_high": "274962817936384505",
            "mu_0": "1184288048715968585930152451399175",
            "mu_D_plus_1": "7863582775712820188422356536857430",
        },
        "universal_previous_T_star": one_cut_gate(N, 1, 18_013)[
            "formal_T_star"
        ],
        "sharp_bad_profile_passes_set_pair_P2": set_pair_value <= 1,
        "sharp_bad_profile_set_pair_fraction": (
            f"{set_pair_value.numerator}/{set_pair_value.denominator}"
        ),
        "sharp_bad_profile_passes_pairwise_gate": (
            2 * bad_deficit <= 2 * J - 1
        ),
        "toy_sage_expected": {
            "field": 17,
            "N": 8,
            "R": 6,
            "kappa": 2,
            "s": 2,
            "r": 1,
            "j": 5,
            "d": 1,
            "deficit_multiplicities": [1, 2],
            "injective_mask_minimum_D_basis_counts": [1, 2],
            "ambient_budget": 28,
            "test_size": 15,
            "cutoff": 0,
            "T_star": 1,
            "good_weight": 29,
            "sharp_bad_weight": 28,
        },
        "numerical_scale": "EXACT_FINITE_INTEGERS_PLUS_TOY_GF17_CONTROL",
        "deployed_field_census_performed": False,
    }


def expected_certificate() -> dict[str, Any]:
    validate_source_contracts()
    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "row": expected_row(),
        "predecessor_contract": expected_predecessor_contract(),
        "rank9_m2b_specialization": expected_rank9_specialization(),
        "exported_histogram_constraints": expected_exported_constraints(),
        "unconstrained_optimizer": expected_unconstrained_optimizer(),
        "coarse_failure_controls": {
            "first_unpaid_cells": all_zero_rows(),
            "all_zero_size_B_remaining_plus_one_passes_every_cell": True,
            "coarse_cap_recovered_exactly_at_delta_zero": True,
            "actual_vector_family_realization_claimed": False,
        },
        "one_cut_tail_frontier": expected_one_cut_frontier(),
        "multi_cut_compiler": expected_multi_cut_compiler(),
        "classifier_contract": expected_classifier_contract(),
        "exact_controls": expected_exact_controls(),
        "charges": {
            "packet_banked_charge": "0",
            "conditional_tail_owner_banked": False,
            "reason": "NO_DEPLOYED_CUMULATIVE_DEFICIT_TAIL_LEMMA",
        },
        "ledger": {
            "U_paid_before": str(U_PAID),
            "U_paid_after": str(U_PAID),
            "B_remaining_before": str(B_REMAINING),
            "B_remaining_after": str(B_REMAINING),
            "branch3_status": "YELLOW_OPEN",
            "koalabear_row_status": "YELLOW_OPEN",
            "next_route": (
                "PROVE_A_CUMULATIVE_LOW_DEFICIT_INCIDENCE_BOUND_OR_FREEZE_"
                "THE_SURVIVING_SYNDROME_LINE_TEMPLATE"
            ),
        },
        "audit_sections": {
            "statement": "rank-nine deficit-histogram interface and tail compiler",
            "dependency_status": (
                "IMPORTED_M2B_PLUS_PROVED_PREDECESSORS_NEW_TAIL_LEMMA_UNPROVEN"
            ),
            "parameter_dependence": "EXACT_KOALABEAR_FINITE_ROW_ONLY",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "edge_cases": (
                "CEILING_PLUS_ONE_D_PLUS_ONE_EXACT_d_V_AND_SAME_SELECTOR_"
                "PROVENANCE_ARE_LOAD_BEARING"
            ),
            "numerical_evidence": (
                "EXACT_INTEGER_CERTIFICATE_AND_TOY_GF17_CONTROL_NOT_"
                "DEPLOYED_REALIZABILITY"
            ),
            "packet_verdict": "GREEN_ROUTE_CUT_AND_COMPILER",
            "global_verdict": "YELLOW_RANK9_AND_BRANCH3_OPEN",
        },
        "nonclaims": NONCLAIMS,
    }
    certificate["payload_sha256"] = payload_hash(certificate)
    return certificate


def validate_certificate(certificate: dict[str, Any]) -> None:
    require(set(certificate) == TOP_KEYS, "top-level key drift")
    require(certificate["schema"] == SCHEMA, "schema drift")
    require(certificate["artifact_kind"] == ARTIFACT_KIND, "artifact kind drift")
    require(certificate["status"] == STATUS, "status drift")
    require(
        certificate["payload_sha256"] == payload_hash(certificate),
        "payload hash mismatch",
    )

    expected = expected_certificate()
    for key in TOP_KEYS - {"payload_sha256"}:
        require(certificate[key] == expected[key], f"section drift: {key}")
    require(
        certificate["payload_sha256"] == expected["payload_sha256"],
        "expected payload drift",
    )

    bindings = certificate["source_bindings"]
    ids = [row["binding_id"] for row in bindings]
    paths = [row["path"] for row in bindings]
    require(len(ids) == len(set(ids)), "duplicate source binding id")
    require(len(paths) == len(set(paths)), "duplicate source binding path")

    specialization = certificate["rank9_m2b_specialization"]
    require(
        specialization["multiplicity_strictly_increasing"],
        "multiplicity monotonicity missing",
    )
    require(
        all(multiplicity(1, d) < multiplicity(1, d + 1) for d in [0, 1, 18_014, MAX_DEFICIT - 1]),
        "multiplicity checkpoint not strict",
    )

    optimizer = certificate["unconstrained_optimizer"]
    require(
        optimizer["all_zero_passes_each_first_unpaid_m2b_cell"],
        "all-zero route-cut positive control failed",
    )
    require(
        optimizer["actual_RS_extremizer_constructed"] is False,
        "scalar extremizer promoted to actual RS witness",
    )

    frontier = certificate["one_cut_tail_frontier"]
    first_gate = frontier["universal_first_gate"]
    require(first_gate["one_cut_can_close"], "universal first gate no longer closes")
    require(
        int(first_gate["cap_at_T_star"]) == B_REMAINING,
        "universal T-star cap drift",
    )
    require(
        int(first_gate["cap_at_T_star_plus_1"]) == COUNTEREXAMPLE_SIZE,
        "universal sharp boundary drift",
    )
    require(
        not frontier["universal_previous_gate"]["one_cut_can_close"],
        "previous universal cutoff unexpectedly closes",
    )
    require(
        frontier["ell_0_equal_one_loses_exact_distance_information"],
        "exact distance information loss not recorded",
    )

    classifier = certificate["classifier_contract"]
    require(
        classifier["universal_tail_paid"]
        == "PAID_BY_PROVED_RANK9_M2B_CUMULATIVE_DEFICIT_TAIL",
        "proved universal tail did not classify as paid",
    )
    require(
        classifier["unproved_numerical_tail_not_owner"]
        == "UNPAID_CURRENT_SCALAR_INTERFACE_ALL_ZERO_DEFICIT_EXTREMIZER",
        "unproved numerical tail became an owner",
    )
    require(
        classifier["missing_predecessor_rank9_contract"]
        == "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED",
        "missing predecessor rank-nine contract was accepted",
    )
    require(
        classifier["unmatched_exact_distance"]
        == "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED",
        "unmatched exact distance was accepted",
    )
    require(
        classifier["negative_tail_cap_rejected"]
        == "UNPAID_RANK9_MASK_DATA_NOT_CERTIFIED",
        "negative cumulative tail cap was accepted",
    )

    multi_cut = certificate["multi_cut_compiler"]
    multi_input = multi_cut["toy_input"]
    require(
        prefix_minimum_weight(
            multi_input["source_distance"],
            multi_input["total_size"],
            [tuple(row) for row in multi_input["cuts"]],
        )
        == int(multi_cut["toy_exact_minimum_weight"]),
        "multi-cut greedy control drift",
    )

    require(certificate["charges"]["packet_banked_charge"] == "0", "charge moved")
    require(
        certificate["ledger"]["U_paid_before"]
        == certificate["ledger"]["U_paid_after"],
        "U_paid ledger moved",
    )
    require(
        certificate["ledger"]["B_remaining_before"]
        == certificate["ledger"]["B_remaining_after"],
        "remaining budget moved",
    )


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def mutation_cases(baseline: dict[str, Any]) -> list[tuple[str, tuple[Any, ...], Any]]:
    first_t = int(
        baseline["one_cut_tail_frontier"]["universal_first_gate"][
            "largest_sufficient_low_deficit_cap_T_star"
        ]
    )
    return [
        ("schema", ("schema",), "rs-mca-mutated"),
        ("artifact", ("artifact_kind",), "MUTATED"),
        ("status", ("status",), "GREEN_GLOBAL_CLOSURE"),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
        ("source-path", ("source_bindings", 0, "path"), "wrong.md"),
        ("source-role", ("source_bindings", 0, "role"), "decorative"),
        ("row-n", ("row", "n"), N - 1),
        ("row-j", ("row", "error_cap_j"), J - 1),
        ("row-L", ("row", "post_deep_weight_floor_L"), HEAVY_FLOOR_L - 1),
        ("row-dmax", ("row", "maximum_deficit_Delta_max"), MAX_DEFICIT - 1),
        ("row-Delta0", ("row", "zero_mask_surplus_Delta0"), DELTA_ZERO - 1),
        ("row-budget", ("row", "B_remaining"), str(B_REMAINING - 1)),
        ("row-m", ("row", "first_forbidden_family_size"), str(B_REMAINING)),
        ("rank-s", ("predecessor_contract", "intrinsic_affine_rank_s"), 8),
        ("rank-r", ("predecessor_contract", "actual_core_rank_r"), 7),
        ("basis-supports", ("predecessor_contract", "basis_support_count"), 9),
        ("same-selector", ("predecessor_contract", "same_selector_and_restricted_H_V_required"), False),
        ("deficit-range", ("rank9_m2b_specialization", "deficit_range", 1), MAX_DEFICIT - 1),
        ("binomial-offset", ("rank9_m2b_specialization", "binomial_identity"), "67479+delta"),
        ("extension", ("rank9_m2b_specialization", "extension_identity"), "max(1,ell0+delta)"),
        ("formula", ("rank9_m2b_specialization", "multiplicity_formula"), "FLOOR(...)"),
        ("m2b", ("rank9_m2b_specialization", "m2b_histogram_formula"), "SUM<=BINOM(n,9)"),
        ("strict", ("rank9_m2b_specialization", "multiplicity_strictly_increasing"), False),
        ("set-pair", ("exported_histogram_constraints", "set_pair_P2"), "REMOVED"),
        ("pairwise", ("exported_histogram_constraints", "pairwise_difference_gate"), "REMOVED"),
        ("antichain", ("exported_histogram_constraints", "transversality_support_gate"), "REMOVED"),
        ("tail-exists", ("exported_histogram_constraints", "no_exported_positive_deficit_tail_bound"), False),
        ("optimizer", ("unconstrained_optimizer", "optimizer_from_strict_weight_monotonicity"), "h_1"),
        ("optimizer-size", ("unconstrained_optimizer", "all_zero_test_size"), str(B_REMAINING)),
        ("optimizer-m2b", ("unconstrained_optimizer", "all_zero_passes_each_first_unpaid_m2b_cell"), False),
        ("actual-realization", ("unconstrained_optimizer", "actual_RS_extremizer_constructed"), True),
        ("coarse-control", ("coarse_failure_controls", "all_zero_size_B_remaining_plus_one_passes_every_cell"), False),
        ("formula-plus-one", ("one_cut_tail_frontier", "sharp_formula"), "REMOVE_MINUS_ONE"),
        ("different-cuts", ("one_cut_tail_frontier", "different_cutoffs_are_incomparable"), False),
        ("worst-corner", ("one_cut_tail_frontier", "worst_corner_for_each_fixed_cutoff"), "N_MIN"),
        ("Dcrit", ("one_cut_tail_frontier", "universal_first_useful_cutoff_D"), 18_013),
        ("Tcrit", ("one_cut_tail_frontier", "universal_first_gate", "largest_sufficient_low_deficit_cap_T_star"), str(first_t + 1)),
        ("required-high", ("one_cut_tail_frontier", "universal_first_gate", "required_high_deficit_count"), "0"),
        ("cap-good", ("one_cut_tail_frontier", "universal_first_gate", "cap_at_T_star"), str(B_REMAINING + 1)),
        ("cap-bad", ("one_cut_tail_frontier", "universal_first_gate", "cap_at_T_star_plus_1"), str(B_REMAINING)),
        ("previous", ("one_cut_tail_frontier", "universal_previous_gate", "one_cut_can_close"), True),
        ("ell-loss", ("one_cut_tail_frontier", "ell_0_equal_one_loses_exact_distance_information"), False),
        ("multicut-order", ("multi_cut_compiler", "input_contract"), "UNSORTED_ALLOWED"),
        ("multicut-formula", ("multi_cut_compiler", "exact_greedy_formula"), "USES_D_i_NOT_D_(i-1)+1"),
        ("incidence-owner", ("multi_cut_compiler", "incidence_proof_required_before_payment"), False),
        ("classifier-default", ("classifier_contract", "fail_closed_defaults"), "PAID"),
        ("classifier-contract", ("classifier_contract", "missing_predecessor_rank9_contract"), "PAID"),
        ("classifier-unproved", ("classifier_contract", "unproved_numerical_tail_not_owner"), "PAID"),
        ("classifier-distance", ("classifier_contract", "unmatched_exact_distance"), "PAID"),
        ("classifier-negative", ("classifier_contract", "negative_tail_cap_rejected"), "PAID"),
        ("control-mu", ("exact_controls", "universal_first_cut_expected", "mu_0"), "1"),
        ("control-T", ("exact_controls", "universal_first_cut_expected", "T_star"), str(first_t + 1)),
        ("toy-mu", ("exact_controls", "toy_sage_expected", "deficit_multiplicities", 1), 1),
        ("toy-boundary", ("exact_controls", "toy_sage_expected", "T_star"), 2),
        ("charge", ("charges", "packet_banked_charge"), "1"),
        ("ledger-paid", ("ledger", "U_paid_after"), str(U_PAID + 1)),
        ("ledger-budget", ("ledger", "B_remaining_after"), str(B_REMAINING - 1)),
        ("branch-close", ("ledger", "branch3_status"), "GREEN_CLOSED"),
        ("verdict", ("audit_sections", "global_verdict"), "GREEN_ROW_CLOSED"),
        ("nonclaim", ("nonclaims", 0), "This constructs an actual deployed family."),
    ]


def tamper_selftest() -> None:
    baseline = load_json(CERT_PATH)
    validate_certificate(baseline)
    rejected = 0
    cases = mutation_cases(baseline)
    for name, path, replacement in cases:
        mutated = copy.deepcopy(baseline)
        set_path(mutated, path, replacement)
        mutated["payload_sha256"] = payload_hash(mutated)
        try:
            validate_certificate(mutated)
        except (VerificationError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {name}")

    duplicate_binding = copy.deepcopy(baseline)
    duplicate_binding["source_bindings"].append(
        copy.deepcopy(duplicate_binding["source_bindings"][0])
    )
    duplicate_binding["payload_sha256"] = payload_hash(duplicate_binding)
    try:
        validate_certificate(duplicate_binding)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("duplicate source binding accepted")

    extra_key = copy.deepcopy(baseline)
    extra_key["unexpected"] = True
    extra_key["payload_sha256"] = payload_hash(extra_key)
    try:
        validate_certificate(extra_key)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("unknown top-level key accepted")

    raw_bad = [
        ('{"schema":"a","schema":"b"}', "duplicate JSON key"),
        ('{"x":NaN}', "nonstandard JSON constant"),
    ]
    for raw, label in raw_bad:
        try:
            parse_json(raw, label)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"raw JSON tamper accepted: {label}")

    rank_source_bad = load_json(ROOT / RANK_LADDER_CERT_REL)
    rank_source_bad["rank_ladder"]["first_rank_not_uniformly_paid"] = 8
    rank_source_bad["payload_sha256"] = payload_hash(rank_source_bad)
    try:
        validate_source_contracts(rank_ladder_override=rank_source_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("rank-ladder semantic source tamper accepted")

    tdd_source_bad = load_json(ROOT / TDD_CERT_REL)
    tdd_source_bad["row"]["surviving_error_weight_floor_L"] -= 1
    tdd_source_bad["payload_sha256"] = payload_hash(tdd_source_bad)
    try:
        validate_source_contracts(tdd_override=tdd_source_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("TDD semantic source tamper accepted")

    theorem_source = (ROOT / ACTUAL_CORE_NOTE_REL).read_text(encoding="utf-8")
    theorem_source_bad = theorem_source.replace("(M2b)", "(M2b-REMOVED)")
    try:
        validate_source_contracts(theorem_text_override=theorem_source_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("actual-core theorem semantic tamper accepted")

    total = len(cases) + 7
    require(rejected == total, "tamper rejection count drift")
    print(f"PASS tamper-selftest: {rejected}/{total} mutations rejected")


def write_certificate() -> None:
    certificate = expected_certificate()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(certificate, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {CERT_PATH.relative_to(ROOT)}")


def check_certificate() -> None:
    certificate = load_json(CERT_PATH)
    validate_certificate(certificate)
    gate = certificate["one_cut_tail_frontier"]["universal_first_gate"]
    print(f"PASS {SCHEMA}")
    print(
        "route cut: current scalar interface permits all-zero deficit; "
        f"coarse cap={coarse_cap(N, 1)}"
    )
    print(
        "universal first tail gate: "
        f"D={gate['cutoff_D']}; H_D<={gate['largest_sufficient_low_deficit_cap_T_star']}"
    )
    print(
        "ledger: no charge; "
        f"U_paid={U_PAID}; B_remaining={B_REMAINING}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_certificate()
        elif args.check:
            check_certificate()
        else:
            tamper_selftest()
    except (VerificationError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
