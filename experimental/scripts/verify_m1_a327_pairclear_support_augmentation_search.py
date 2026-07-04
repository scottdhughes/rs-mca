#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear support augmentation search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_support_augmentation_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_support_augmentation_search.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_support_augmentation_search.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested support-augmentation front",
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
    require(record["source_commit"] == "7076965", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / SUPPORTAUG_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_two_target_basis_exchange"]
    require(previous["commit"] == "7076965", "wrong previous commit")
    require(previous["proof_status"] == "EXACT_EXTRACTION_NO_A327 / TWOTARGETBASIS_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["basis_profiles_tested"] == 13700, "wrong previous basis count")
    require(previous["extended_rank_slack_profiles"] == 640, "wrong previous rank-slack count")
    require(previous["exact_pairclear_profiles"] == 0, "wrong previous exact count")
    require(previous["best_forced_pairs"] == ["P45", "P46", "P56"], "wrong previous forced pairs")

    search = record["support_augmentation_search"]
    require(search["extended_zero_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong extended classes")
    require(search["cycle_pairs"] == ["P14", "P16", "P17", "P45", "P46", "P47", "P56", "P57", "P67"], "wrong cycle pairs")
    require(search["max_mutations"] == 646, "wrong max mutations")
    require(search["seed_offsets"] == 3, "wrong seed offsets")
    require(search["max_candidates"] == 520, "wrong max candidates")
    require(search["max_diverse_candidates"] == 180, "wrong max diverse candidates")
    require(search["top_augment_classes"] == 4, "wrong top augment classes")
    require(search["top_classes"] == 30, "wrong top classes")
    require(search["random_bases"] == 96, "wrong random bases")
    require(search["max_basis_profiles_per_augment"] == 4, "wrong max basis profiles")
    require(search["mutations_generated"] == 646, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 646, "wrong MILP count")
    require(search["candidate_systems_constructed"] == 5814, "wrong candidate count")
    require(search["structural_pass_candidates"] == 5328, "wrong structural pass count")
    require(search["selected_candidates"] == 685, "wrong selected candidate count")
    require(search["basis_profiles_tested"] == 10852, "wrong basis profile count")
    require(search["target_rows_present_profiles"] == 7948, "wrong target-present count")
    require(search["extended_rank_slack_profiles"] == 152, "wrong rank-slack count")
    require(search["exact_pairclear_profiles"] == 0, "unexpected exact pair-clear")
    require(search["cycle_pressure_reduced_profiles"] == 0, "unexpected reduced cycle pressure")
    require(search["augmentation_class_counts"] == {"0": 128, "1": 16, "2": 8}, "wrong augmentation class counts")
    require(search["cycle_forced_count_histogram"] == {"3": 116, "5": 8, "6": 28}, "wrong cycle histogram")
    require(search["total_forced_count_histogram"] == {"3": 80, "4": 36, "6": 36}, "wrong total histogram")
    require(search["front_return_counts"] == {"mixed_front": 12, "p456_front": 32, "tail_front": 124}, "wrong front returns")
    require(
        search["forced_pair_pattern_counts"]
        == {
            "P14,P15,P16,P45,P46,P56": 8,
            "P14,P16,P17,P46,P47,P67": 12,
            "P24,P56,P57,P67": 36,
            "P45,P46,P47,P56,P57,P67": 16,
            "P45,P46,P56": 8,
            "P56,P57,P67": 72,
        },
        "wrong forced-pair pattern counts",
    )
    require(search["best_template_id"] == "ninerow_P17_shear_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "P17_shear_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "supportaug_0_1_2_3_4_5_13", "wrong best basis")
    require(search["best_support_augmentation_class"] == 0, "wrong augmentation class")
    require(search["best_failure_mode"] == "SUPPORTAUG_FORCED_PROJECTIONS_REMAIN", "wrong best failure")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P17_shear_c1_d1", "wrong best profile template")
    require(best["mutation_id"] == "P17_shear_c1_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 164466, "wrong best profile seed")
    require(best["basis_id"] == "supportaug_0_1_2_3_4_5_13", "wrong best profile basis")
    require(best["basis_class_indices"] == [1, 2, 3, 4, 5, 13], "wrong best basis classes")
    require(best["support_augmentation_class"] == 0, "wrong support augmentation class")
    require(best["augmented_zero_classes"] == [0, 6, 7, 8, 14, 17, 18, 19, 20], "wrong augmented zero classes")
    require(best["basis_support_sizes"] == [142, 142, 142, 142, 105, 68], "wrong support sizes")
    require(best["coefficient_matrix_shape"] == [18, 6], "wrong matrix shape")
    require(best["extended_rank"] == 4, "wrong extended rank")
    require(best["extended_nullity"] == 2, "wrong extended nullity")

    info = best["extended_exchange_direction"]
    require(info["direction"] == [0, 1, 1, 2, 0, 0], "wrong best direction")
    require(info["forced_pairs"] == ["P45", "P46", "P56"], "wrong best forced pairs")
    require(info["forced_pair_count"] == 3, "wrong forced-pair count")
    require(info["cycle_forced_count"] == 3, "wrong cycle forced count")
    require(info["p456_front_returned"] is True, "P456 front did not return")
    require(info["tail_front_returned"] is False, "tail front unexpectedly returned")
    require(info["mixed_front_returned"] is False, "mixed front unexpectedly returned")
    require(info["cycle_pairs_cleared"] == ["P14", "P16", "P17", "P47", "P57", "P67"], "wrong cleared cycle pairs")

    for phrase in [
        "EXACT_EXTRACTION_NO_A327 / SUPPORTAUG_FORCED_PROJECTIONS_REMAIN",
        "basis profiles tested = 10852",
        "support-augmented rank-slack profiles = 152",
        "exact pair-clear profiles = 0",
        "cycle pressure reduced profiles = 0",
        "support augmentation class = 0",
        "forced pairs = [P45,P46,P56]",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "support_augmented_basis_profiles",
        "SUPPORTAUG_EXACT_PAIRCLEAR_REPAIRED",
        "global obstruction outside the tested support-augmentation front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
        "exact_pairclear_profiles": search["exact_pairclear_profiles"],
        "best_forced_pairs": info["forced_pairs"],
        "best_support_augmentation_class": best["support_augmentation_class"],
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
        print(f"PASS: M1 a=327 pair-clear support augmentation search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
