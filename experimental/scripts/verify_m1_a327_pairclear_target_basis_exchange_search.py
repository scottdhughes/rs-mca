#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear target-basis exchange search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_target_basis_exchange_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_target_basis_exchange_search.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_target_basis_exchange_search.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested target-basis exchange front",
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
    require(record["source_commit"] == "fa084a3", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / TARGETBASIS_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_cyclic_obstruction"]
    require(previous["commit"] == "fa084a3", "wrong previous commit")
    require(previous["proof_status"] == "AUDIT / ROUTE_CUT_LOCAL_PAIRCLEAR_FRONT / EXPERIMENTAL", "wrong previous status")
    require(
        previous["observed_cycle"]
        == [
            ["P56", "P57", "P67"],
            ["P45", "P46", "P56"],
            ["P14", "P16", "P17", "P46", "P47", "P67"],
            ["P56", "P57", "P67"],
        ],
        "wrong previous cycle",
    )

    search = record["target_basis_exchange_search"]
    require(search["extended_zero_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong extended classes")
    require(search["base_zero_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong base classes")
    require(search["cycle_pairs"] == ["P14", "P16", "P17", "P45", "P46", "P47", "P56", "P57", "P67"], "wrong cycle pairs")
    require(search["max_mutations"] == 646, "wrong max mutations")
    require(search["seed_offsets"] == 3, "wrong seed offsets")
    require(search["max_candidates"] == 520, "wrong max candidates")
    require(search["max_diverse_candidates"] == 180, "wrong max diverse candidates")
    require(search["top_classes"] == 30, "wrong top classes")
    require(search["random_bases"] == 160, "wrong random bases")
    require(search["max_basis_profiles"] == 16, "wrong max basis profiles")
    require(search["mutations_generated"] == 646, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 646, "wrong MILP count")
    require(search["candidate_systems_constructed"] == 5814, "wrong candidate count")
    require(search["structural_pass_candidates"] == 5328, "wrong structural pass count")
    require(search["selected_candidates"] == 685, "wrong selected candidate count")
    require(search["basis_profiles_tested"] == 10960, "wrong basis profile count")
    require(search["target_rows_present_profiles"] == 8016, "wrong target-present count")
    require(search["extended_rank_slack_profiles"] == 512, "wrong rank-slack count")
    require(search["exact_pairclear_profiles"] == 0, "unexpected exact pair-clear")
    require(search["cycle_pressure_reduced_profiles"] == 0, "unexpected reduced cycle pressure")
    require(search["target_basis_class_counts"] == {"6": 512}, "wrong target-basis class counts")
    require(search["cycle_forced_count_histogram"] == {"3": 448, "5": 16, "6": 48}, "wrong cycle histogram")
    require(search["total_forced_count_histogram"] == {"3": 304, "4": 144, "6": 64}, "wrong total histogram")
    require(search["front_return_counts"] == {"mixed_front": 16, "p456_front": 64, "tail_front": 464}, "wrong front returns")
    require(
        search["forced_pair_pattern_counts"]
        == {
            "P14,P15,P16,P45,P46,P56": 16,
            "P14,P16,P17,P46,P47,P67": 16,
            "P24,P56,P57,P67": 144,
            "P45,P46,P47,P56,P57,P67": 32,
            "P45,P46,P56": 16,
            "P56,P57,P67": 288,
        },
        "wrong forced-pair pattern counts",
    )
    require(search["best_template_id"] == "ninerow_P17_shear_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "P17_shear_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "targetbasis_6_0_1_2_4_5_6", "wrong best basis")
    require(search["best_target_basis_class"] == 6, "wrong target basis class")
    require(search["best_failure_mode"] == "TARGETBASIS_FORCED_PROJECTIONS_REMAIN", "wrong best failure")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P17_shear_c1_d1", "wrong best profile template")
    require(best["mutation_id"] == "P17_shear_c1_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 164466, "wrong best profile seed")
    require(best["basis_id"] == "targetbasis_6_0_1_2_4_5_6", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 4, 5, 6], "wrong best basis classes")
    require(best["target_basis_class"] == 6, "wrong best target basis class")
    require(best["augmented_basis_zero_classes"] == [6], "wrong augmented zero classes")
    require(best["basis_support_sizes"] == [142, 142, 142, 142, 105, 74], "wrong support sizes")
    require(best["coefficient_matrix_shape"] == [19, 6], "wrong matrix shape")
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
        "EXACT_EXTRACTION_NO_A327 / TARGETBASIS_FORCED_PROJECTIONS_REMAIN",
        "basis profiles tested = 10960",
        "target-basis rank-slack profiles = 512",
        "exact pair-clear profiles = 0",
        "cycle pressure reduced profiles = 0",
        "target basis class = 6",
        "forced pairs = [P45,P46,P56]",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "target_basis_exchange_profiles",
        "augmented_matrix_and_classes",
        "TARGETBASIS_EXACT_PAIRCLEAR_REPAIRED",
        "global obstruction outside the tested target-basis exchange front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
        "exact_pairclear_profiles": search["exact_pairclear_profiles"],
        "best_forced_pairs": info["forced_pairs"],
        "best_target_basis_class": best["target_basis_class"],
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
        print(f"PASS: M1 a=327 pair-clear target-basis exchange search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
