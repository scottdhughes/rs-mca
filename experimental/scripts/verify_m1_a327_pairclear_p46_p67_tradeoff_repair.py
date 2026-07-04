#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear P46/P67 tradeoff repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_p46_p67_tradeoff_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_p46_p67_tradeoff_repair.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_p46_p67_tradeoff_repair.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested P46/P67 tradeoff front",
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
    require(record["source_commit"] == "c900d81", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / P46P67_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_p45_p46_p56_codesign"]
    require(previous["commit"] == "c900d81", "wrong previous commit")
    require(
        previous["proof_status"] == "EXACT_EXTRACTION_NO_A327 / P456_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["basis_profiles_tested"] == 6850, "wrong previous basis count")
    require(previous["extended_rank_slack_profiles"] == 320, "wrong previous rank-slack count")
    require(previous["best_failure_mode"] == "P456_FORCED_PROJECTIONS_REMAIN", "wrong previous failure")
    require(previous["best_forced_pairs"] == ["P14", "P16", "P17", "P46", "P47", "P67"], "wrong previous forced pairs")
    require(previous["best_target_pairs_cleared"] == ["P45", "P56"], "wrong previous target clearance")
    require(previous["best_preserve_pairs_cleared"] == ["P57"], "wrong previous preserve clearance")

    search = record["p46_p67_tradeoff_repair"]
    require(search["repair_pairs"] == ["P46", "P67"], "wrong repair pairs")
    require(search["preserve_clear_pairs"] == ["P45", "P56"], "wrong preserve pairs")
    require(search["spillover_avoid_pairs"] == ["P14", "P16", "P17", "P47"], "wrong spillover pairs")
    require(search["max_mutations"] == 646, "wrong max mutations")
    require(search["seed_offsets"] == 3, "wrong seed offsets")
    require(search["max_candidates"] == 520, "wrong max candidates")
    require(search["max_diverse_candidates"] == 180, "wrong max diverse candidates")
    require(search["top_classes"] == 26, "wrong top classes")
    require(search["random_bases"] == 128, "wrong random bases")
    require(search["max_basis_profiles"] == 10, "wrong max basis profiles")
    require(search["mutations_generated"] == 646, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 646, "wrong MILP count")
    require(search["candidate_systems_constructed"] == 5814, "wrong candidate count")
    require(search["structural_pass_candidates"] == 5328, "wrong structural pass count")
    require(search["selected_candidates"] == 685, "wrong selected candidate count")
    require(search["basis_profiles_tested"] == 6850, "wrong basis profile count")
    require(search["target_rows_present_profiles"] == 5010, "wrong target-present count")
    require(search["extended_rank_slack_profiles"] == 320, "wrong extended rank-slack count")
    require(search["exact_pairclear_profiles"] == 0, "unexpected exact pair-clear")
    require(search["tradeoff_repaired_profiles"] == 0, "unexpected tradeoff repair")
    require(search["clean_tradeoff_repaired_profiles"] == 0, "unexpected clean tradeoff repair")
    require(search["near_repair_profiles"] == 0, "unexpected near repair")
    require(search["repair_forced_count_histogram"] == {"1": 290, "2": 30}, "wrong repair histogram")
    require(search["preserve_forced_count_histogram"] == {"0": 10, "1": 270, "2": 40}, "wrong preserve histogram")
    require(search["spillover_forced_count_histogram"] == {"0": 280, "1": 20, "2": 10, "4": 10}, "wrong spillover histogram")
    require(search["total_forced_count_histogram"] == {"3": 190, "4": 90, "6": 40}, "wrong total forced histogram")
    require(
        search["forced_pair_pattern_counts"]
        == {
            "P14,P15,P16,P45,P46,P56": 10,
            "P14,P16,P17,P46,P47,P67": 10,
            "P24,P56,P57,P67": 90,
            "P45,P46,P47,P56,P57,P67": 20,
            "P45,P46,P56": 10,
            "P56,P57,P67": 180,
        },
        "wrong forced-pair pattern counts",
    )
    require(search["best_template_id"] == "ninerow_P14_shear_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "P14_shear_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "targetaware_0_1_2_3_4_13", "wrong best basis")
    require(search["best_failure_mode"] == "P46P67_FORCED_PROJECTIONS_REMAIN", "wrong best failure")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P14_shear_c1_d1", "wrong best profile template")
    require(best["mutation_id"] == "P14_shear_c1_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 162526, "wrong best profile seed")
    require(best["basis_id"] == "targetaware_0_1_2_3_4_13", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 4, 13], "wrong best basis classes")
    require(best["basis_support_sizes"] == [142, 142, 142, 142, 105, 68], "wrong best support sizes")
    require(best["coefficient_matrix_shape"] == [20, 6], "wrong best matrix shape")
    require(best["base_rank"] == 4, "wrong best base rank")
    require(best["base_nullity"] == 2, "wrong best base nullity")
    require(best["extended_rank"] == 4, "wrong best extended rank")
    require(best["extended_nullity"] == 2, "wrong best extended nullity")

    info = best["extended_tradeoff_direction"]
    require(info["direction"] == [0, 1, 1, 2, 0, 0], "wrong best direction")
    require(info["repair_pairs_cleared"] == ["P46"], "wrong repaired pairs")
    require(info["repair_forced_count"] == 1, "wrong repair forced count")
    require(info["preserve_pairs_cleared"] == ["P45"], "wrong preserve cleared pairs")
    require(info["preserve_forced_count"] == 1, "wrong preserve forced count")
    require(info["spillover_pairs_cleared"] == ["P14", "P16", "P17", "P47"], "wrong spillover clearance")
    require(info["spillover_forced_count"] == 0, "wrong spillover forced count")
    require(info["forced_pairs"] == ["P56", "P57", "P67"], "wrong best forced pairs")
    require(info["forced_pair_count"] == 3, "wrong forced-pair count")

    for phrase in [
        "EXACT_EXTRACTION_NO_A327 / P46P67_FORCED_PROJECTIONS_REMAIN",
        "candidate systems constructed = 5814",
        "Repair forced-count histogram",
        "repair pairs cleared = [P46]",
        "repair pair still forced = P67",
        "preserve pair still forced = P56",
        "spillover pairs cleared = [P14,P16,P17,P47]",
        "current best forced pairs = [P56,P57,P67]",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "REPAIR_PAIRS",
        "P46P67_EXACT_PAIRCLEAR_REPAIRED",
        "P46P67_FORCED_PROJECTIONS_REMAIN",
        "global obstruction outside the tested P46/P67 tradeoff front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
        "tradeoff_repaired_profiles": search["tradeoff_repaired_profiles"],
        "best_forced_pairs": info["forced_pairs"],
        "best_repair_pairs_cleared": info["repair_pairs_cleared"],
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
        print(f"PASS: M1 a=327 pair-clear P46/P67 tradeoff repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
