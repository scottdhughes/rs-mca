#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear row17 dependence codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_row17_dependence_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_row17_dependence_codesign.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_row17_dependence_codesign.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested row17 dependence codesign front",
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
    require(record["source_commit"] == "811019a", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / ROW17_DEPENDENCE_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_seven_to_eight_repair"]
    require(previous["commit"] == "811019a", "wrong previous commit")
    require(
        previous["proof_status"] == "CANDIDATE / SEVEN_TO_EIGHT_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["rank_slack_chambers"] == 20, "wrong previous rank-slack count")
    require(previous["support_reduced_pairclear_extensions"] == 1, "wrong previous support extension count")
    require(previous["deep_rank_slack_extensions"] == 0, "unexpected previous deep extension")
    require(previous["best_failure_mode"] == "SEVEN_TO_EIGHT_SUPPORT_ONLY", "wrong previous failure")

    search = record["row17_dependence_codesign"]
    require(search["base_zero_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong base zero classes")
    require(search["repair_row_class"] == 17, "wrong repair row class")
    require(search["extended_zero_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong extended classes")
    require(search["max_mutations"] == 240, "wrong max mutations")
    require(search["max_candidates"] == 180, "wrong max candidates")
    require(search["max_diverse_candidates"] == 80, "wrong max diverse candidates")
    require(search["top_classes"] == 18, "wrong top classes")
    require(search["random_bases"] == 64, "wrong random bases")
    require(search["max_basis_profiles"] == 6, "wrong max basis profiles")
    require(search["mutations_generated"] == 240, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 240, "wrong MILP count")
    require(search["candidate_systems_constructed"] == 720, "wrong candidate count")
    require(search["structural_pass_candidates"] == 681, "wrong structural pass count")
    require(search["selected_candidates"] == 233, "wrong selected candidate count")
    require(search["basis_profiles_tested"] == 1398, "wrong basis profile count")
    require(search["target_rows_present_profiles"] == 253, "wrong target-present count")
    require(search["base_rank_slack_profiles"] == 12, "wrong base rank-slack count")
    require(search["base_pair_clear_profiles"] == 12, "wrong base pair-clear count")
    require(search["row17_dependent_profiles"] == 175, "wrong row17 dependence count")
    require(search["extended_rank_slack_profiles"] == 0, "unexpected extended rank slack")
    require(search["extended_pair_clear_profiles"] == 14, "wrong extended pair-clear count")
    require(search["extended_rank_slack_pair_clear_profiles"] == 0, "unexpected extended rank-slack pair-clear")
    require(search["deep_rank_slack_repair_profiles"] == 0, "unexpected deep repair")
    require(search["best_template_id"] == "ninerow_w3_c3_d1", "wrong best template")
    require(search["best_mutation_id"] == "w3_c3_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "basisaware_0_1_2_3_4_10", "wrong best basis")
    require(search["best_failure_mode"] == "ROW17_DEPENDENCE_SUPPORT_ONLY", "wrong best failure")
    require(
        search["profile_failure_counts"]
        == {
            "ROW17_DEPENDENCE_BASE_NOT_RANKSLACK": 241,
            "ROW17_DEPENDENCE_SUPPORT_ONLY": 12,
            "ROW17_DEPENDENCE_TARGET_ROWS_MISSING": 1145,
        },
        "wrong profile failure counts",
    )
    require(
        search["screen_counts"]
        == {
            "TCHAMBER_FORCED_IDENTITY": 9,
            "TCHAMBER_LOW_FUNCTIONAL_SPAN": 30,
            "TCHAMBER_STRUCTURAL_PASS": 681,
        },
        "wrong screen counts",
    )

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_w3_c3_d1", "wrong best profile template")
    require(best["mutation_id"] == "w3_c3_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 119186, "wrong best profile seed")
    require(best["basis_id"] == "basisaware_0_1_2_3_4_10", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 4, 10], "wrong best basis classes")
    require(best["basis_support_sizes"] == [216, 179, 148, 142, 111, 74], "wrong best support sizes")
    require(best["coefficient_matrix_shape"] == [15, 6], "wrong best matrix shape")
    require(best["base_rank"] == 4, "wrong best base rank")
    require(best["base_nullity"] == 2, "wrong best base nullity")
    require(best["base_pair_clear"] is True, "best base not pair-clear")
    require(best["base_pair_clear_direction"] == [1, 9, 6, 6, 1, 6], "wrong base direction")
    require(best["extended_rank"] == 5, "wrong best extended rank")
    require(best["extended_nullity"] == 1, "wrong best extended nullity")
    require(best["extended_pair_clear"] is True, "best extended not pair-clear")
    require(best["extended_pair_clear_direction"] == [1, 0, 14, 6, 1, 6], "wrong extended direction")
    require(best["row17_dependent"] is False, "row17 unexpectedly dependent in best profile")
    require(best["deep_rank_slack_repair"] is False, "unexpected deep repair")
    require(best["best_failure_mode"] == "ROW17_DEPENDENCE_SUPPORT_ONLY", "wrong best profile failure")

    base_chamber = best["base_direction_chamber"]
    require(base_chamber["zero_row_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong base chamber zeros")
    require(base_chamber["inactive_rank"] == 4, "wrong base chamber rank")
    require(base_chamber["inactive_kernel_nullity"] == 2, "wrong base chamber nullity")

    extended_chamber = best["extended_direction_chamber"]
    require(extended_chamber["zero_row_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong extended chamber zeros")
    require(extended_chamber["inactive_rank"] == 5, "wrong extended chamber rank")
    require(extended_chamber["inactive_kernel_nullity"] == 1, "wrong extended chamber nullity")

    for phrase in [
        "CANDIDATE / ROW17_DEPENDENCE_SUPPORT_ONLY",
        "basis profiles tested = 1398",
        "base rank-slack profiles = 12",
        "extended pair-clear profiles = 14",
        "deep rank-slack repair profiles = 0",
        "basis = basisaware_0_1_2_3_4_10",
        "inactive rank = 5",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "BASE_ZERO_CLASSES",
        "ROW17_DEPENDENCE_DEEP_REPAIR",
        "ROW17_DEPENDENCE_SUPPORT_ONLY",
        "global obstruction outside the tested row17 dependence codesign front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "base_rank_slack_profiles": search["base_rank_slack_profiles"],
        "extended_pair_clear_profiles": search["extended_pair_clear_profiles"],
        "deep_rank_slack_repair_profiles": search["deep_rank_slack_repair_profiles"],
        "best_base_rank": best["base_rank"],
        "best_extended_rank": best["extended_rank"],
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
        print(f"PASS: M1 a=327 pair-clear row17 dependence codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
