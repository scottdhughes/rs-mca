#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear P45/P46/P56 codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_p45_p46_p56_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_p45_p46_p56_codesign.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_p45_p46_p56_codesign.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested P45/P46/P56 codesign front",
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
    require(record["source_commit"] == "e48c576", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / P456_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_tailpair_projection_repair"]
    require(previous["commit"] == "e48c576", "wrong previous commit")
    require(
        previous["proof_status"] == "EXACT_EXTRACTION_NO_A327 / TAILPAIR_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["tail_candidates"] == 112, "wrong previous tail candidate count")
    require(previous["best_failure_mode"] == "TAILPAIR_FORCED_PROJECTIONS_REMAIN", "wrong previous failure")
    require(previous["best_forced_pairs"] == ["P45", "P46", "P56"], "wrong previous forced pairs")

    search = record["p45_p46_p56_codesign"]
    require(search["target_repair_pairs"] == ["P45", "P46", "P56"], "wrong target repair pairs")
    require(search["preserve_clear_pairs"] == ["P57", "P67"], "wrong preserve pairs")
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
    require(search["target_repaired_profiles"] == 0, "unexpected target repair")
    require(search["near_repair_profiles"] == 0, "unexpected near repair")
    require(search["target_forced_count_histogram"] == {"1": 280, "3": 40}, "wrong target-forced histogram")
    require(search["preserve_forced_count_histogram"] == {"0": 20, "1": 10, "2": 290}, "wrong preserve histogram")
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
    require(search["best_template_id"] == "ninerow_W57_c13_pm1", "wrong best template")
    require(search["best_mutation_id"] == "W57_c13_pm1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "targetaware_0_1_2_3_4_10", "wrong best basis")
    require(search["best_failure_mode"] == "P456_FORCED_PROJECTIONS_REMAIN", "wrong best failure")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_W57_c13_pm1", "wrong best profile template")
    require(best["mutation_id"] == "W57_c13_pm1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 193081, "wrong best profile seed")
    require(best["basis_id"] == "targetaware_0_1_2_3_4_10", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 4, 10], "wrong best basis classes")
    require(best["basis_support_sizes"] == [216, 111, 105, 105, 74, 74], "wrong best support sizes")
    require(best["coefficient_matrix_shape"] == [20, 6], "wrong best matrix shape")
    require(best["base_rank"] == 4, "wrong best base rank")
    require(best["base_nullity"] == 2, "wrong best base nullity")
    require(best["extended_rank"] == 4, "wrong best extended rank")
    require(best["extended_nullity"] == 2, "wrong best extended nullity")

    info = best["extended_codesign_direction"]
    require(info["direction"] == [0, 0, 0, 1, 0, 2], "wrong best direction")
    require(info["target_pairs_cleared"] == ["P45", "P56"], "wrong cleared target pairs")
    require(info["target_forced_count"] == 1, "wrong target forced count")
    require(info["preserve_pairs_cleared"] == ["P57"], "wrong preserve cleared pairs")
    require(info["preserve_forced_count"] == 1, "wrong preserve forced count")
    require(info["forced_pairs"] == ["P14", "P16", "P17", "P46", "P47", "P67"], "wrong best forced pairs")
    require(info["forced_pair_count"] == 6, "wrong forced-pair count")

    for phrase in [
        "EXACT_EXTRACTION_NO_A327 / P456_FORCED_PROJECTIONS_REMAIN",
        "candidate systems constructed = 5814",
        "target forced-count histogram",
        "target pairs cleared = [P45,P56]",
        "target pair still forced = P46",
        "preserve pair still forced = P67",
        "current best forced pairs includes only one target pair: P46",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "TARGET_REPAIR_PAIRS",
        "P456_EXACT_PAIRCLEAR_REPAIRED",
        "P456_FORCED_PROJECTIONS_REMAIN",
        "global obstruction outside the tested P45/P46/P56 codesign front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
        "target_repaired_profiles": search["target_repaired_profiles"],
        "best_forced_pairs": info["forced_pairs"],
        "best_target_pairs_cleared": info["target_pairs_cleared"],
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
        print(f"PASS: M1 a=327 pair-clear P45/P46/P56 codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
