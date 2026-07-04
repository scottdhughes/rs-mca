#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear two-target basis exchange search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_two_target_basis_exchange_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_two_target_basis_exchange_search.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_two_target_basis_exchange_search.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested two-target basis exchange front",
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
    require(record["source_commit"] == "b84b4ca", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / TWOTARGETBASIS_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_target_basis_exchange"]
    require(previous["commit"] == "b84b4ca", "wrong previous commit")
    require(previous["proof_status"] == "EXACT_EXTRACTION_NO_A327 / TARGETBASIS_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["basis_profiles_tested"] == 10960, "wrong previous basis count")
    require(previous["extended_rank_slack_profiles"] == 512, "wrong previous rank-slack count")
    require(previous["exact_pairclear_profiles"] == 0, "wrong previous exact count")
    require(previous["best_forced_pairs"] == ["P45", "P46", "P56"], "wrong previous forced pairs")

    search = record["two_target_basis_exchange_search"]
    require(search["extended_zero_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong extended classes")
    require(search["base_zero_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong base classes")
    require(search["cycle_pairs"] == ["P14", "P16", "P17", "P45", "P46", "P47", "P56", "P57", "P67"], "wrong cycle pairs")
    require(search["max_mutations"] == 646, "wrong max mutations")
    require(search["seed_offsets"] == 3, "wrong seed offsets")
    require(search["max_candidates"] == 520, "wrong max candidates")
    require(search["max_diverse_candidates"] == 180, "wrong max diverse candidates")
    require(search["top_classes"] == 34, "wrong top classes")
    require(search["random_bases"] == 192, "wrong random bases")
    require(search["max_basis_profiles"] == 20, "wrong max basis profiles")
    require(search["mutations_generated"] == 646, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 646, "wrong MILP count")
    require(search["candidate_systems_constructed"] == 5814, "wrong candidate count")
    require(search["structural_pass_candidates"] == 5328, "wrong structural pass count")
    require(search["selected_candidates"] == 685, "wrong selected candidate count")
    require(search["basis_profiles_tested"] == 13700, "wrong basis profile count")
    require(search["target_rows_present_profiles"] == 10020, "wrong target-present count")
    require(search["extended_rank_slack_profiles"] == 640, "wrong rank-slack count")
    require(search["exact_pairclear_profiles"] == 0, "unexpected exact pair-clear")
    require(search["cycle_pressure_reduced_profiles"] == 0, "unexpected reduced cycle pressure")
    require(search["target_basis_class_counts"] == {"6,7": 640}, "wrong target-basis class counts")
    require(search["cycle_forced_count_histogram"] == {"3": 560, "5": 20, "6": 60}, "wrong cycle histogram")
    require(search["total_forced_count_histogram"] == {"3": 380, "4": 180, "6": 80}, "wrong total histogram")
    require(search["front_return_counts"] == {"mixed_front": 20, "p456_front": 80, "tail_front": 580}, "wrong front returns")
    require(
        search["forced_pair_pattern_counts"]
        == {
            "P14,P15,P16,P45,P46,P56": 20,
            "P14,P16,P17,P46,P47,P67": 20,
            "P24,P56,P57,P67": 180,
            "P45,P46,P47,P56,P57,P67": 40,
            "P45,P46,P56": 20,
            "P56,P57,P67": 360,
        },
        "wrong forced-pair pattern counts",
    )
    require(search["best_template_id"] == "ninerow_P17_shear_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "P17_shear_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "twotargetbasis_6_7_0_1_2_4_6_7", "wrong best basis")
    require(search["best_target_basis_classes"] == [6, 7], "wrong target basis classes")
    require(search["best_failure_mode"] == "TWOTARGETBASIS_FORCED_PROJECTIONS_REMAIN", "wrong best failure")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P17_shear_c1_d1", "wrong best profile template")
    require(best["mutation_id"] == "P17_shear_c1_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 164466, "wrong best profile seed")
    require(best["basis_id"] == "twotargetbasis_6_7_0_1_2_4_6_7", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 4, 6, 7], "wrong best basis classes")
    require(best["target_basis_classes"] == [6, 7], "wrong best target basis classes")
    require(best["augmented_basis_zero_classes"] == [6, 7], "wrong augmented zero classes")
    require(best["basis_support_sizes"] == [142, 142, 142, 142, 74, 74], "wrong support sizes")
    require(best["coefficient_matrix_shape"] == [20, 6], "wrong matrix shape")
    require(best["base_rank"] == 4, "wrong base rank")
    require(best["base_nullity"] == 2, "wrong base nullity")
    require(best["extended_rank"] == 4, "wrong extended rank")
    require(best["extended_nullity"] == 2, "wrong extended nullity")

    info = best["extended_exchange_direction"]
    require(info["direction"] == [0, 0, 1, 2, 0, 0], "wrong best direction")
    require(info["forced_pairs"] == ["P45", "P46", "P56"], "wrong best forced pairs")
    require(info["forced_pair_count"] == 3, "wrong forced-pair count")
    require(info["cycle_forced_count"] == 3, "wrong cycle forced count")
    require(info["p456_front_returned"] is True, "P456 front did not return")
    require(info["tail_front_returned"] is False, "tail front unexpectedly returned")
    require(info["mixed_front_returned"] is False, "mixed front unexpectedly returned")
    require(info["cycle_pairs_cleared"] == ["P14", "P16", "P17", "P47", "P57", "P67"], "wrong cleared cycle pairs")

    for phrase in [
        "EXACT_EXTRACTION_NO_A327 / TWOTARGETBASIS_FORCED_PROJECTIONS_REMAIN",
        "basis profiles tested = 13700",
        "two-target rank-slack profiles = 640",
        "exact pair-clear profiles = 0",
        "cycle pressure reduced profiles = 0",
        "target basis classes = [6,7]",
        "forced pairs = [P45,P46,P56]",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "two_target_basis_exchange_profiles",
        "TWOTARGETBASIS_EXACT_PAIRCLEAR_REPAIRED",
        "global obstruction outside the tested two-target basis exchange front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
        "exact_pairclear_profiles": search["exact_pairclear_profiles"],
        "best_forced_pairs": info["forced_pairs"],
        "best_target_basis_classes": best["target_basis_classes"],
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
        print(f"PASS: M1 a=327 pair-clear two-target basis exchange search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
