#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear template chamber mutation ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_template_chamber_mutation_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_template_chamber_mutation_search.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_template_chamber_mutation_search.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested template-chamber mutation front",
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
    require(record["source_commit"] == "12a54d9", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / TCHAMBER_NINE_ROW_STABLE_FRONT / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_chamber_search"]
    require(previous["commit"] == "12a54d9", "wrong previous commit")
    require(previous["proof_status"] == "CANDIDATE / CHAMBER_NINE_ROW_STABLE / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["directions_tested"] == 1508598, "wrong previous direction count")
    require(previous["pair_clear_directions"] == 360360, "wrong previous pair-clear count")
    require(previous["distinct_pair_clear_chambers"] == 51, "wrong previous chamber count")
    require(previous["rank_slack_chambers"] == 0, "unexpected previous rank slack")
    require(previous["support_reduced_extensions"] == 0, "unexpected previous support extension")
    require(previous["best_failure_mode"] == "CHAMBER_NINE_ROW_STABLE", "wrong previous failure")

    search = record["template_chamber_search"]
    require(search["max_mutations"] == 24, "wrong max mutations")
    require(search["max_candidates"] == 8, "wrong max candidates")
    require(search["top_classes"] == 14, "wrong top classes")
    require(search["random_bases"] == 16, "wrong random bases")
    require(search["max_basis_profiles"] == 1, "wrong max basis profiles")
    require(search["max_scored_profiles"] == 4, "wrong max scored profiles")
    require(search["direction_limit"] is None, "direction scan unexpectedly limited")
    require(search["extension_chamber_limit"] == 80, "wrong extension chamber limit")
    require(search["mutations_generated"] == 24, "wrong mutation count")
    require(search["candidate_systems_constructed"] == 72, "wrong candidate count")
    require(search["structural_pass_candidates"] == 72, "wrong structural pass count")
    require(search["structural_pass_candidates_analyzed"] == 8, "wrong analyzed count")
    require(search["basis_profiles_scored"] == 4, "wrong scored profile count")
    require(search["directions_tested"] == 6034392, "wrong direction total")
    require(search["pair_clear_directions"] == 1441440, "wrong pair-clear total")
    require(search["distinct_pair_clear_chambers"] == 218, "wrong chamber total")
    require(search["nine_row_or_better_profiles"] == 1, "wrong nine-row profile count")
    require(search["direct_support_reduced_profiles"] == 0, "unexpected direct support reduction")
    require(search["rank_slack_profiles"] == 0, "unexpected rank slack")
    require(search["support_reduced_extension_profiles"] == 0, "unexpected support-reduced extension")
    require(search["best_template_id"] == "ninerow_base_w1_c3_d1", "wrong best template")
    require(search["best_mutation_id"] == "base_w1_c3_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "basisaware_1_4_7_8_9_10", "wrong best basis")
    require(search["best_failure_mode"] == "TCHAMBER_NINE_ROW_STABLE", "wrong best failure")
    require(search["failure_counts"] == {"TCHAMBER_LOWER_SUPPORT_ONLY": 3, "TCHAMBER_NINE_ROW_STABLE": 1}, "wrong failure counts")
    require(search["screen_counts"] == {"TCHAMBER_STRUCTURAL_PASS": 72}, "wrong screen counts")
    require(len(search["scored_profile_summaries"]) == 4, "wrong scored summary count")

    expected_profiles = [
        ("ninerow_base_w1_c3_d1", "base_w1_c3_d1", "TCHAMBER_NINE_ROW_STABLE", 51, 1),
        ("ninerow_w1_c0_d1", "w1_c0_d1", "TCHAMBER_LOWER_SUPPORT_ONLY", 36, 0),
        ("ninerow_w1_c0_d13", "w1_c0_d13", "TCHAMBER_LOWER_SUPPORT_ONLY", 66, 0),
        ("ninerow_w1_c0_d14", "w1_c0_d14", "TCHAMBER_LOWER_SUPPORT_ONLY", 65, 0),
    ]
    for row, expected in zip(search["scored_profile_summaries"], expected_profiles, strict=True):
        template_id, mutation_id, failure, chamber_count, nine_count = expected
        require(row["template_id"] == template_id, f"wrong template for {template_id}")
        require(row["mutation_id"] == mutation_id, f"wrong mutation for {template_id}")
        require(row["assignment_strategy"] == "fiber_round_robin", f"wrong assignment for {template_id}")
        require(row["basis_id"] == "basisaware_1_4_7_8_9_10", f"wrong basis for {template_id}")
        require(row["directions_tested"] == 1508598, f"wrong directions for {template_id}")
        require(row["pair_clear_directions"] == 360360, f"wrong pair-clear count for {template_id}")
        require(row["distinct_pair_clear_chambers"] == chamber_count, f"wrong chamber count for {template_id}")
        require(row["nine_row_or_better_chambers"] == nine_count, f"wrong nine-row count for {template_id}")
        require(row["direct_support_reduced_chambers"] == 0, f"unexpected support reduction for {template_id}")
        require(row["rank_slack_chambers"] == 0, f"unexpected rank slack for {template_id}")
        require(row["support_reduced_extensions"] == 0, f"unexpected support extension for {template_id}")
        require(row["best_failure_mode"] == failure, f"wrong failure for {template_id}")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_base_w1_c3_d1", "wrong best profile template")
    require(best["best_nine_row_chamber"]["zero_row_classes"] == [13, 16, 17, 18, 19], "wrong best zero classes")
    require(best["best_nine_row_chamber"]["inactive_rank"] == 5, "wrong best inactive rank")
    require(best["best_nine_row_chamber"]["inactive_kernel_nullity"] == 1, "wrong best inactive nullity")

    for phrase in [
        "CANDIDATE / TCHAMBER_NINE_ROW_STABLE_FRONT",
        "basis profiles scored = 4",
        "directions tested = 6034392",
        "pair-clear directions = 1441440",
        "direct support-reduced profiles = 0",
        "rank-slack profiles = 0",
        "support-reduced extension profiles = 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "select_diverse_candidates",
        "PREFERRED_BASIS_CLASS_SETS",
        "TCHAMBER_RANK_SLACK_FOUND",
        "global obstruction outside the tested template-chamber mutation front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_scored": search["basis_profiles_scored"],
        "directions_tested": search["directions_tested"],
        "pair_clear_directions": search["pair_clear_directions"],
        "rank_slack_profiles": search["rank_slack_profiles"],
        "support_reduced_extension_profiles": search["support_reduced_extension_profiles"],
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
        print(f"PASS: M1 a=327 pair-clear template chamber mutation search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
