#!/usr/bin/env python3
"""Verify the M1 a=327 cycle-guarded template front search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_cycle_guarded_template_front_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_cycle_guarded_template_front_search.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_cycle_guarded_template_front_search.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested cycle-guarded template front",
}

CYCLE_PAIRS = ["P14", "P16", "P17", "P45", "P46", "P47", "P56", "P57", "P67"]


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
    require(record["source_commit"] == "a63ab87", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_support_augmentation"]
    require(previous["commit"] == "a63ab87", "wrong previous commit")
    require(
        previous["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / SUPPORTAUG_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["basis_profiles_tested"] == 10852, "wrong previous basis count")
    require(previous["extended_rank_slack_profiles"] == 152, "wrong previous rank-slack count")
    require(previous["exact_pairclear_profiles"] == 0, "wrong previous exact count")
    require(previous["best_forced_pairs"] == ["P45", "P46", "P56"], "wrong previous forced pairs")

    search = record["cycle_guarded_template_front"]
    require(search["cycle_pairs"] == CYCLE_PAIRS, "wrong cycle-pair guard")
    require(search["max_mutations"] == 646, "wrong max mutations")
    require(search["seed_offsets"] == 3, "wrong seed offsets")
    require(search["max_candidates"] == 160, "wrong max candidates")
    require(search["max_diverse_candidates"] == 64, "wrong max diverse candidates")
    require(search["top_classes"] == 26, "wrong top classes")
    require(search["random_bases"] == 48, "wrong random bases")
    require(search["max_basis_profiles"] == 4, "wrong max basis profiles")
    require(search["sample_directions"] == 2048, "wrong sampled directions")
    require(search["mutations_generated"] == 646, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 646, "wrong MILP count")
    require(search["candidate_systems_constructed"] == 5814, "wrong candidate count")
    require(search["structural_pass_candidates"] == 5328, "wrong structural pass count")
    require(search["selected_candidates"] == 219, "wrong selected candidate count")
    require(search["basis_profiles_tested"] == 876, "wrong basis profile count")
    require(search["cycle_clear_profiles"] == 453, "wrong cycle-clear count")
    require(search["exact_pairclear_profiles"] == 291, "wrong exact pair-clear count")
    require(search["cycle_clear_rank_slack_profiles"] == 203, "wrong cycle-clear rank-slack count")
    require(search["exact_pairclear_rank_slack_profiles"] == 80, "wrong exact pair-clear rank slack")
    require(
        search["profile_failure_counts"]
        == {
            "CYCLEG_TEMPLATE_CYCLE_CLEAR_ONLY": 89,
            "CYCLEG_TEMPLATE_CYCLE_CLEAR_RANKSLACK": 73,
            "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_ONLY": 211,
            "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK": 80,
            "CYCLEG_TEMPLATE_NO_CYCLE_CLEAR_DIRECTION": 423,
        },
        "wrong profile failure counts",
    )
    require(
        search["screen_counts"]
        == {
            "TCHAMBER_FORCED_IDENTITY": 144,
            "TCHAMBER_LOW_FUNCTIONAL_SPAN": 342,
            "TCHAMBER_STRUCTURAL_PASS": 5328,
        },
        "wrong screen counts",
    )
    require(search["best_template_id"] == "ninerow_P57_shear_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "P57_shear_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "basisaware_0_1_2_3_4_5", "wrong best basis")
    require(search["best_failure_mode"] == "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK", "wrong best failure")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P57_shear_c1_d1", "wrong best profile template")
    require(best["mutation_id"] == "P57_shear_c1_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 179986, "wrong best profile seed")
    require(best["basis_id"] == "basisaware_0_1_2_3_4_5", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 4, 5], "wrong basis classes")
    require(best["basis_support_sizes"] == [216, 142, 142, 105, 105, 74], "wrong basis support sizes")
    require(best["coefficient_matrix_shape"] == [19, 6], "wrong matrix shape")
    require(best["directions_sampled"] == 2048, "wrong best sampled directions")
    require(best["cycle_clear_directions"] == 876, "wrong cycle-clear direction count")
    require(best["exact_pairclear_directions"] == 355, "wrong exact-pairclear direction count")
    require(best["cycle_clear_rank_slack_directions"] == 8, "wrong cycle-clear rank-slack directions")
    require(best["exact_pairclear_rank_slack_directions"] == 3, "wrong exact-pairclear rank-slack directions")
    require(best["best_failure_mode"] == "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK", "wrong best profile failure")

    chamber = best["best_exact_pairclear_rank_slack_chamber"]
    require(chamber["direction"] == [1, 4, 0, 0, 10, 0], "wrong best direction")
    require(chamber["direction_weight"] == 3, "wrong best direction weight")
    require(chamber["forced_pairs"] == [], "best chamber did not clear all pair projections")
    require(chamber["forced_pair_count"] == 0, "wrong forced-pair count")
    require(chamber["cycle_forced_count"] == 0, "wrong cycle forced count")
    require(chamber["cycle_pairs_cleared"] == CYCLE_PAIRS, "wrong cleared cycle pairs")
    require(chamber["zero_row_count"] == 8, "wrong zero-row count")
    require(chamber["zero_row_classes"] == [7, 8, 9, 13, 17, 19, 21, 23], "wrong zero-row classes")
    require(chamber["inactive_rank"] == 4, "wrong inactive rank")
    require(chamber["inactive_kernel_nullity"] == 2, "wrong inactive kernel nullity")

    for phrase in [
        "CANDIDATE / CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK",
        "basis profiles tested = 876",
        "exact pair-clear profiles = 291",
        "exact pair-clear rank-slack profiles = 80",
        "direction = [1,4,0,0,10,0]",
        "forced pairs = []",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "CYCLE_PAIRS",
        "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_ONLY",
        "global obstruction outside the tested cycle-guarded template front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "cycle_clear_profiles": search["cycle_clear_profiles"],
        "exact_pairclear_profiles": search["exact_pairclear_profiles"],
        "exact_pairclear_rank_slack_profiles": search["exact_pairclear_rank_slack_profiles"],
        "best_direction": chamber["direction"],
        "best_forced_pairs": chamber["forced_pairs"],
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
        print(f"PASS: M1 a=327 cycle-guarded template front search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
