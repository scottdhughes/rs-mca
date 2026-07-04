#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear tail-pair projection repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_tailpair_projection_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_tailpair_projection_repair.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_tailpair_projection_repair.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested tail-pair projection repair front",
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
    require(record["source_commit"] == "8184509", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / TAILPAIR_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_rowspan_dependence_mutation"]
    require(previous["commit"] == "8184509", "wrong previous commit")
    require(
        previous["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["extended_rank_slack_profiles"] == 112, "wrong previous rank-slack count")
    require(previous["extended_rank_slack_pair_clear_profiles"] == 0, "unexpected previous pair-clear rank slack")
    require(previous["best_failure_mode"] == "ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL", "wrong previous failure")

    search = record["tailpair_projection_repair"]
    require(search["target_tail_pairs"] == ["P56", "P57", "P67"], "wrong target tail pairs")
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
    require(search["extended_rank_slack_profiles"] == 112, "wrong extended rank-slack count")
    require(search["extended_pair_clear_profiles"] == 16, "wrong extended pair-clear count")
    require(search["deep_rank_slack_repair_profiles"] == 0, "unexpected deep repair")
    require(search["tail_candidates"] == 112, "wrong tail candidate count")
    require(search["forced_pair_count_histogram"] == {"3": 72, "4": 24, "6": 16}, "wrong forced-pair histogram")
    require(search["tail_forced_count_histogram"] == {"1": 24, "3": 88}, "wrong tail-forced histogram")
    require(
        search["forced_pair_pattern_counts"]
        == {
            "P24,P56,P57,P67": 24,
            "P45,P46,P47,P56,P57,P67": 16,
            "P45,P46,P56": 24,
            "P56,P57,P67": 48,
        },
        "wrong forced-pair patterns",
    )
    require(search["best_template_id"] == "ninerow_P17_shear_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "P17_shear_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "targetaware_0_1_2_3_4_13", "wrong best basis")
    require(search["best_failure_mode"] == "TAILPAIR_FORCED_PROJECTIONS_REMAIN", "wrong best failure")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P17_shear_c1_d1", "wrong best profile template")
    require(best["mutation_id"] == "P17_shear_c1_d1", "wrong best profile mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best profile assignment")
    require(best["assignment_seed"] == 154466, "wrong best profile seed")
    require(best["basis_id"] == "targetaware_0_1_2_3_4_13", "wrong best profile basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 4, 13], "wrong best basis classes")
    require(best["basis_support_sizes"] == [142, 142, 142, 142, 142, 68], "wrong best support sizes")
    require(best["coefficient_matrix_shape"] == [18, 6], "wrong best matrix shape")
    require(best["base_rank"] == 4, "wrong best base rank")
    require(best["base_nullity"] == 2, "wrong best base nullity")
    require(best["extended_rank"] == 4, "wrong best extended rank")
    require(best["extended_nullity"] == 2, "wrong best extended nullity")
    require(best["extended_rank_slack"] is True, "best extended not rank slack")
    require(best["extended_pair_clear"] is False, "best extended unexpectedly pair-clear")

    tail = best["tailpair_projection"]
    require(tail["direction"] == [0, 0, 1, 1, 2, 0], "wrong best direction")
    require(tail["forced_pair_count"] == 3, "wrong forced-pair count")
    require(tail["forced_pairs"] == ["P45", "P46", "P56"], "wrong forced pairs")
    require(tail["tail_forced_count"] == 1, "wrong tail forced count")
    require(tail["tail_pairs_cleared"] == ["P57", "P67"], "wrong cleared tail pairs")

    for phrase in [
        "EXACT_EXTRACTION_NO_A327 / TAILPAIR_FORCED_PROJECTIONS_REMAIN",
        "tail candidates = 112",
        "P45,P46,P56: 24",
        "tail pairs cleared = [P57,P67]",
        "old best forced pairs = [P56,P57,P67]",
        "new best forced pairs = [P45,P46,P56]",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "TARGET_TAIL_PAIRS",
        "TAILPAIR_EXACT_PAIRCLEAR_REPAIRED",
        "TAILPAIR_FORCED_PROJECTIONS_REMAIN",
        "global obstruction outside the tested tail-pair projection repair front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "tail_candidates": search["tail_candidates"],
        "forced_pair_count_histogram": search["forced_pair_count_histogram"],
        "best_forced_pairs": tail["forced_pairs"],
        "best_tail_pairs_cleared": tail["tail_pairs_cleared"],
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
        print(f"PASS: M1 a=327 pair-clear tail-pair projection repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
