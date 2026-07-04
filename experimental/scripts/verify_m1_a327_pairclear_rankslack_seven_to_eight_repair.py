#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear rank-slack seven-to-eight repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_rankslack_seven_to_eight_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_rankslack_seven_to_eight_repair.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_rankslack_seven_to_eight_repair.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested seven-to-eight repair front",
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
    require(record["source_commit"] == "36eac30", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / SEVEN_TO_EIGHT_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_deeper_rank_slack_front"]
    require(previous["commit"] == "36eac30", "wrong previous commit")
    require(
        previous["proof_status"] == "CANDIDATE / DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["full_deep_rank_slack_profiles"] == 0, "unexpected previous deep rank slack")
    require(previous["full_direct_support_reduced_profiles"] == 4, "wrong previous support-reduced count")
    require(previous["best_template_id"] == "ninerow_w3_c3_d1", "wrong previous template")
    require(previous["best_mutation_id"] == "w3_c3_d1", "wrong previous mutation")
    require(previous["best_basis_id"] == "basisaware_0_1_2_3_5_10", "wrong previous basis")
    require(previous["best_failure_mode"] == "DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY", "wrong previous failure")

    target = record["target_profile"]
    require(target["template_id"] == "ninerow_w3_c3_d1", "wrong target template")
    require(target["mutation_id"] == "w3_c3_d1", "wrong target mutation")
    require(target["assignment_strategy"] == "fiber_round_robin", "wrong target assignment")
    require(target["assignment_seed"] == 117186, "wrong target seed")
    require(target["basis_id"] == "basisaware_0_1_2_3_5_10", "wrong target basis")
    require(target["basis_class_indices"] == [0, 1, 2, 3, 5, 10], "wrong target basis classes")
    require(target["basis_support_sizes"] == [216, 179, 148, 142, 111, 74], "wrong target support sizes")
    require(target["coefficient_matrix_shape"] == [15, 6], "wrong target matrix shape")

    search = record["seven_to_eight_repair"]
    require(search["direction_limit"] is None, "unexpected direction limit")
    require(search["directions_tested"] == 1508598, "wrong direction count")
    require(search["pair_clear_directions"] == 360360, "wrong pair-clear count")
    require(search["distinct_pair_clear_chambers"] == 178, "wrong chamber count")
    require(search["direct_support_reduced_chambers"] == 1, "wrong direct support count")
    require(search["rank_slack_chambers"] == 20, "wrong rank-slack chamber count")
    require(search["rank_slack_zero7_chambers"] == 1, "wrong zero-7 rank-slack count")
    require(search["rank_slack_zero8_chambers"] == 0, "unexpected zero-8 rank slack")
    require(search["extension_attempts"] == 194, "wrong extension attempt count")
    require(search["rank_preserving_extension_attempts"] == 0, "unexpected rank-preserving attempt")
    require(search["rank_preserving_pairclear_extensions"] == 0, "unexpected rank-preserving pair-clear extension")
    require(search["pair_clear_extensions"] == 40, "wrong pair-clear extension count")
    require(search["support_reduced_pairclear_extensions"] == 1, "wrong support extension count")
    require(search["deep_rank_slack_extensions"] == 0, "unexpected deep extension")
    require(search["target_row_class"] == 17, "wrong target row class")
    require(search["target_row_attempts"] == 1, "wrong target row attempt count")
    require(search["best_failure_mode"] == "SEVEN_TO_EIGHT_SUPPORT_ONLY", "wrong failure")
    require(
        search["extension_failure_counts"]
        == {
            "no_pairclear": 154,
            "pairclear_lower_support": 39,
            "support_pairclear": 1,
        },
        "wrong extension failure counts",
    )

    base = record["target_rank_slack_chamber"]
    require(base["zero_row_count"] == 7, "wrong target base zero count")
    require(base["inactive_rank"] == 4, "wrong target base inactive rank")
    require(base["inactive_kernel_nullity"] == 2, "wrong target base nullity")
    require(base["zero_row_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong target base zero classes")
    require(base["active_row_classes"] == [4, 9, 11, 12, 13, 15, 16, 17], "wrong target base active classes")
    require(base["exemplar_direction"] == [1, 4, 1, 6, 11, 6], "wrong target base direction")

    attempt = record["target_row17_attempt"]
    require(attempt["base_zero_row_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong row17 base")
    require(attempt["added_active_row_class"] == 17, "wrong added row")
    require(attempt["zero_row_count"] == 8, "wrong row17 zero count")
    require(attempt["zero_row_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong row17 zero classes")
    require(attempt["inactive_rank"] == 5, "wrong row17 inactive rank")
    require(attempt["inactive_kernel_nullity"] == 1, "wrong row17 nullity")
    require(attempt["pair_clear"] is True, "row17 attempt not pair-clear")
    require(attempt["pair_clear_direction"] == [1, 0, 14, 6, 11, 6], "wrong row17 pair-clear direction")
    require(attempt["rank_preserved"] is False, "row17 rank unexpectedly preserved")
    require(attempt["support_reduced_pair_clear"] is True, "row17 not support-reduced pair-clear")
    require(attempt["deep_rank_slack"] is False, "row17 unexpectedly deep rank slack")

    best_support = record["best_support_reduced_extension"]
    require(best_support == attempt, "best support extension is not target row17 attempt")
    require(record["best_deep_rank_slack_extension"] is None, "unexpected best deep extension")

    for phrase in [
        "CANDIDATE / SEVEN_TO_EIGHT_SUPPORT_ONLY",
        "directions tested = 1508598",
        "extension attempts = 194",
        "rank-preserving pair-clear extensions = 0",
        "added row class = 17",
        "new inactive rank = 5",
        "SEVEN_TO_EIGHT_SUPPORT_ONLY",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "extension_attempt_record",
        "SEVEN_TO_EIGHT_RANKSLACK_REPAIRED",
        "SEVEN_TO_EIGHT_SUPPORT_ONLY",
        "global obstruction outside the tested seven-to-eight repair front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "directions_tested": search["directions_tested"],
        "pair_clear_directions": search["pair_clear_directions"],
        "extension_attempts": search["extension_attempts"],
        "support_reduced_pairclear_extensions": search["support_reduced_pairclear_extensions"],
        "deep_rank_slack_extensions": search["deep_rank_slack_extensions"],
        "target_row17_inactive_rank": attempt["inactive_rank"],
        "target_row17_pair_clear": attempt["pair_clear"],
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
        print(f"PASS: M1 a=327 pair-clear rank-slack seven-to-eight repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
