#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear row-span dependence mutation ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_rowspan_dependence_mutation.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_rowspan_dependence_mutation.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_rowspan_dependence_mutation.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested row-span dependence mutation front",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    scan_text = SCAN_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "8613e96", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_row17_dependence_codesign"]
    require(previous["commit"] == "8613e96", "wrong previous commit")
    require(
        previous["proof_status"] == "CANDIDATE / ROW17_DEPENDENCE_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["base_rank_slack_profiles"] == 12, "wrong previous base rank-slack count")
    require(previous["extended_pair_clear_profiles"] == 14, "wrong previous extended pair-clear count")
    require(previous["extended_rank_slack_pair_clear_profiles"] == 0, "unexpected previous extended pair-clear rank slack")
    require(previous["deep_rank_slack_repair_profiles"] == 0, "unexpected previous deep repair")
    require(previous["best_failure_mode"] == "ROW17_DEPENDENCE_SUPPORT_ONLY", "wrong previous failure")

    search = record["rowspan_dependence_mutation"]
    require(search["base_zero_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong base zero classes")
    require(search["repair_row_class"] == 17, "wrong repair row class")
    require(search["extended_zero_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong extended classes")
    require(search["max_mutations"] == 640, "wrong max mutations")
    require(search["max_candidates"] == 260, "wrong max candidates")
    require(search["max_diverse_candidates"] == 120, "wrong max diverse candidates")
    require(search["top_classes"] == 24, "wrong top classes")
    require(search["random_bases"] == 96, "wrong random bases")
    require(search["max_basis_profiles"] == 8, "wrong max basis profiles")
    require(search["mutations_generated"] == 640, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 640, "wrong MILP count")
    require(search["candidate_systems_constructed"] == 1920, "wrong candidate count")
    require(search["structural_pass_candidates"] == 1758, "wrong structural pass count")
    require(search["selected_candidates"] == 357, "wrong selected candidate count")
    require(search["basis_profiles_tested"] == 2856, "wrong basis profile count")
    require(search["target_rows_present_profiles"] == 2024, "wrong target-present count")
    require(search["base_rank_slack_profiles"] == 120, "wrong base rank-slack count")
    require(search["base_pair_clear_profiles"] == 8, "wrong base pair-clear count")
    require(search["extended_rank_slack_profiles"] == 112, "wrong extended rank-slack count")
    require(search["extended_pair_clear_profiles"] == 16, "wrong extended pair-clear count")
    require(search["extended_rank_slack_pair_clear_profiles"] == 0, "unexpected extended rank-slack pair-clear")
    require(search["deep_rank_slack_repair_profiles"] == 0, "unexpected deep repair")
    require(search["best_template_id"] == "ninerow_P14_shear_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "P14_shear_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "targetaware_0_1_2_3_4_11", "wrong best basis")
    require(search["best_failure_mode"] == "ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL", "wrong best failure")
    require(
        search["profile_failure_counts"]
        == {
            "ROWSPAN_BASE_NOT_RANKSLACK": 1896,
            "ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL": 112,
            "ROWSPAN_SUPPORT_ONLY": 16,
            "ROWSPAN_TARGET_ROWS_MISSING": 832,
        },
        "wrong profile failure counts",
    )
    require(
        search["screen_counts"]
        == {
            "TCHAMBER_FORCED_IDENTITY": 48,
            "TCHAMBER_LOW_FUNCTIONAL_SPAN": 114,
            "TCHAMBER_STRUCTURAL_PASS": 1758,
        },
        "wrong screen counts",
    )

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P14_shear_c1_d1", "wrong best profile template")
    require(best["mutation_id"] == "P14_shear_c1_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 152526, "wrong best profile seed")
    require(best["basis_id"] == "targetaware_0_1_2_3_4_11", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 4, 11], "wrong best basis classes")
    require(best["basis_support_sizes"] == [142, 142, 142, 142, 105, 74], "wrong best support sizes")
    require(best["coefficient_matrix_shape"] == [20, 6], "wrong best matrix shape")
    require(best["base_rank"] == 4, "wrong best base rank")
    require(best["base_nullity"] == 2, "wrong best base nullity")
    require(best["extended_rank"] == 4, "wrong best extended rank")
    require(best["extended_nullity"] == 2, "wrong best extended nullity")
    require(best["extended_rank_slack"] is True, "best extended not rank slack")
    require(best["extended_pair_clear"] is False, "best extended unexpectedly pair-clear")
    require(best["deep_rank_slack_repair"] is False, "unexpected deep repair")
    require(best["best_failure_mode"] == "ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL", "wrong best profile failure")

    forced = best["extended_best_subspace_direction"]
    require(forced["direction"] == [0, 1, 1, 2, 0, 1], "wrong best subspace direction")
    require(forced["forced_pair_count"] == 3, "wrong forced-pair count")
    require(forced["forced_pairs"] == ["P56", "P57", "P67"], "wrong forced pairs")

    for phrase in [
        "EXACT_EXTRACTION_NO_A327 / ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL",
        "basis profiles tested = 2856",
        "extended rank-slack profiles = 112",
        "extended rank-slack pair-clear profiles = 0",
        "template = ninerow_P14_shear_c1_d1",
        "forced pairs = [P56,P57,P67]",
        "row-span dependence achieved",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "target_aware_basis_profiles",
        "ROWSPAN_DEEP_REPAIR",
        "ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL",
        "global obstruction outside the tested row-span dependence mutation front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
        "extended_rank_slack_pair_clear_profiles": search["extended_rank_slack_pair_clear_profiles"],
        "best_extended_rank": best["extended_rank"],
        "best_forced_pairs": forced["forced_pairs"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 pair-clear row-span dependence mutation (status={result['proof_status']})")


if __name__ == "__main__":
    main()
