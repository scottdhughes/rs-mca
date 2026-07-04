#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear diverse chamber front ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_diverse_chamber_front.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_diverse_chamber_front.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_diverse_chamber_front.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested diverse chamber front",
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
    require(record["source_commit"] == "dbad852", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / DCHAMBER_DIRECT_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_template_chamber_search"]
    require(previous["commit"] == "dbad852", "wrong previous commit")
    require(previous["proof_status"] == "CANDIDATE / TCHAMBER_NINE_ROW_STABLE_FRONT / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["basis_profiles_scored"] == 4, "wrong previous scored profiles")
    require(previous["directions_tested"] == 6034392, "wrong previous direction count")
    require(previous["pair_clear_directions"] == 1441440, "wrong previous pair-clear count")
    require(previous["rank_slack_profiles"] == 0, "unexpected previous rank slack")
    require(previous["support_reduced_extension_profiles"] == 0, "unexpected previous support extension")
    require(previous["best_failure_mode"] == "TCHAMBER_NINE_ROW_STABLE", "wrong previous failure")

    search = record["diverse_chamber_front"]
    require(search["max_mutations"] == 96, "wrong max mutations")
    require(search["max_candidates"] == 24, "wrong max candidates")
    require(search["top_classes"] == 14, "wrong top classes")
    require(search["random_bases"] == 24, "wrong random bases")
    require(search["max_basis_profiles"] == 2, "wrong max basis profiles")
    require(search["sample_directions"] == 50000, "wrong sample direction count")
    require(search["full_profiles"] == 4, "wrong full profile target")
    require(search["extension_chamber_limit"] == 80, "wrong extension chamber limit")
    require(search["mutations_generated"] == 96, "wrong mutation count")
    require(search["candidate_systems_constructed"] == 288, "wrong candidate count")
    require(search["structural_pass_candidates"] == 279, "wrong structural pass count")
    require(search["diverse_candidates_selected"] == 24, "wrong diverse candidate count")
    require(search["sampled_profiles"] == 48, "wrong sampled profile count")
    require(search["full_profiles_scanned"] == 4, "wrong full profile count")
    require(search["sample_pair_clear_directions"] == 527002, "wrong sampled pair-clear count")
    require(search["sample_direct_support_reduced_profiles"] == 13, "wrong sampled support reduction")
    require(search["sample_rank_slack_profiles"] == 19, "wrong sampled rank slack")
    require(search["sample_nine_row_or_better_profiles"] == 36, "wrong sampled nine-row count")
    require(search["full_directions_tested"] == 6034392, "wrong full direction count")
    require(search["full_pair_clear_directions"] == 1441440, "wrong full pair-clear count")
    require(search["full_direct_support_reduced_profiles"] == 4, "wrong full support-reduced count")
    require(search["full_rank_slack_profiles"] == 4, "wrong full rank-slack count")
    require(search["full_support_reduced_extension_profiles"] == 3, "wrong support-reduced extension count")
    require(search["best_template_id"] == "ninerow_w2_c0_d1", "wrong best template")
    require(search["best_mutation_id"] == "w2_c0_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "basisaware_0_1_2_3_4_6", "wrong best basis")
    require(search["best_failure_mode"] == "DCHAMBER_DIRECT_SUPPORT_REDUCED", "wrong best failure")
    require(search["sample_failure_counts"] == {
        "DCHAMBER_SAMPLE_LOWER_SUPPORT": 12,
        "DCHAMBER_SAMPLE_NINE_ROW": 17,
        "DCHAMBER_SAMPLE_RANK_SLACK": 6,
        "DCHAMBER_SAMPLE_SUPPORT_REDUCED": 13,
    }, "wrong sampled failure counts")
    require(search["full_failure_counts"] == {"TCHAMBER_DIRECT_SUPPORT_REDUCED": 4}, "wrong full failure counts")
    require(search["screen_counts"] == {
        "TCHAMBER_LOW_FUNCTIONAL_SPAN": 9,
        "TCHAMBER_STRUCTURAL_PASS": 279,
    }, "wrong screen counts")

    best = record["best_full_profile"]
    require(best["template_id"] == "ninerow_w2_c0_d1", "wrong best full template")
    require(best["mutation_id"] == "w2_c0_d1", "wrong best full mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best full assignment")
    require(best["basis_id"] == "basisaware_0_1_2_3_4_6", "wrong best full basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 4, 6], "wrong best basis classes")
    require(best["basis_support_sizes"] == [216, 216, 179, 148, 142, 111], "wrong best support sizes")
    require(best["coefficient_matrix_shape"] == [13, 6], "wrong best matrix shape")
    require(best["directions_tested"] == 1508598, "wrong best direction count")
    require(best["pair_clear_directions"] == 360360, "wrong best pair-clear count")
    require(best["distinct_pair_clear_chambers"] == 129, "wrong best chamber count")
    require(best["nine_row_or_better_chambers"] == 18, "wrong best nine-row chambers")
    require(best["direct_support_reduced_chambers"] == 5, "wrong best direct support chambers")
    require(best["rank_slack_chambers"] == 15, "wrong best rank slack")
    require(best["extension_pairclear_successes"] == 295, "wrong extension successes")
    require(best["support_reduced_extensions"] == 28, "wrong support-reduced extensions")
    require(best["best_failure_mode"] == "TCHAMBER_DIRECT_SUPPORT_REDUCED", "wrong best full failure")

    direct = best["best_direct_support_reduced_chamber"]
    require(direct["zero_row_count"] == 8, "wrong direct zero count")
    require(direct["active_row_count"] == 5, "wrong direct active count")
    require(direct["inactive_rank"] == 5, "wrong direct inactive rank")
    require(direct["inactive_kernel_nullity"] == 1, "wrong direct inactive nullity")
    require(direct["zero_row_classes"] == [7, 8, 10, 12, 15, 16, 17, 18], "wrong direct zero classes")
    require(direct["active_row_classes"] == [5, 9, 11, 13, 14], "wrong direct active classes")
    require(direct["exemplar_direction"] == [1, 16, 0, 14, 14, 11], "wrong direct direction")
    require(direct["exemplar_weight"] == 5, "wrong direct direction weight")

    rank = best["best_rank_slack_chamber"]
    require(rank["zero_row_count"] == 7, "wrong rank-slack zero count")
    require(rank["inactive_rank"] == 4, "wrong rank-slack inactive rank")
    require(rank["inactive_kernel_nullity"] == 2, "wrong rank-slack nullity")

    for row in search["full_profile_summaries"]:
        require(row["best_failure_mode"] == "TCHAMBER_DIRECT_SUPPORT_REDUCED", "full profile not support-reduced")
        require(row["direct_support_reduced_chambers"] > 0, "full profile lacks support-reduced chamber")

    for phrase in [
        "CANDIDATE / DCHAMBER_DIRECT_SUPPORT_REDUCED",
        "mutations generated = 96",
        "sample pair-clear directions = 527002",
        "full direct support-reduced profiles = 4",
        "template = ninerow_w2_c0_d1",
        "zero row count = 8",
        "active row count = 5",
        "old active row count = 9",
        "new best active row count = 5",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "sampled_projective_directions",
        "diverse_candidates",
        "DCHAMBER_DIRECT_SUPPORT_REDUCED",
        "global obstruction outside the tested diverse chamber front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "sampled_profiles": search["sampled_profiles"],
        "full_profiles_scanned": search["full_profiles_scanned"],
        "full_direct_support_reduced_profiles": search["full_direct_support_reduced_profiles"],
        "best_active_row_count": direct["active_row_count"],
        "best_zero_row_count": direct["zero_row_count"],
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
        print(f"PASS: M1 a=327 pair-clear diverse chamber front (status={result['proof_status']})")


if __name__ == "__main__":
    main()
