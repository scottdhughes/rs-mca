#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear deeper rank-slack front ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_deeper_rankslack_front.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_deeper_rankslack_front.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_deeper_rankslack_front.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested deeper rank-slack front",
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
    require(record["source_commit"] == "ced3433", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_rank_slack_kernel_repair"]
    require(previous["commit"] == "ced3433", "wrong previous commit")
    require(
        previous["proof_status"] == "CANDIDATE / RANKSLACK_KERNEL_EIGHT_ROW_STABLE / PARTIAL / EXPERIMENTAL",
        "wrong previous status",
    )
    require(previous["directions_tested"] == 18, "wrong previous direction count")
    require(previous["pair_clear_directions"] == 10, "wrong previous pair-clear count")
    require(previous["support_reduced_directions"] == 1, "wrong previous support-reduced count")
    require(previous["nine_or_better_directions"] == 0, "unexpected previous nine-or-better")
    require(previous["coefficient_kernel_directions"] == 0, "unexpected previous coefficient kernel")
    require(previous["best_failure_mode"] == "RANKSLACK_KERNEL_EIGHT_ROW_STABLE", "wrong previous failure")

    search = record["deeper_rank_slack_front"]
    require(search["max_mutations"] == 160, "wrong max mutations")
    require(search["max_candidates"] == 36, "wrong max candidates")
    require(search["top_classes"] == 16, "wrong top classes")
    require(search["random_bases"] == 32, "wrong random bases")
    require(search["max_basis_profiles"] == 3, "wrong max basis profiles")
    require(search["sample_directions"] == 75000, "wrong sample direction count")
    require(search["full_profiles"] == 4, "wrong full profile target")
    require(search["extension_chamber_limit"] == 100, "wrong extension chamber limit")
    require(search["deep_target"] == "zero_row_count >= 8 and inactive_rank <= 4", "wrong deep target")
    require(search["mutations_generated"] == 160, "wrong mutation count")
    require(search["candidate_systems_constructed"] == 480, "wrong candidate count")
    require(search["structural_pass_candidates"] == 459, "wrong structural pass count")
    require(search["diverse_candidates_selected"] == 36, "wrong diverse candidate count")
    require(search["sampled_profiles"] == 108, "wrong sampled profile count")
    require(search["sample_deep_rank_slack_profiles"] == 0, "unexpected sampled deep rank slack")
    require(search["sample_pair_clear_directions"] == 1821587, "wrong sampled pair-clear count")
    require(search["full_profiles_scanned"] == 4, "wrong full profile count")
    require(search["full_deep_rank_slack_profiles"] == 0, "unexpected full deep rank slack")
    require(search["full_directions_tested"] == 6034392, "wrong full direction count")
    require(search["full_pair_clear_directions"] == 1441440, "wrong full pair-clear count")
    require(search["full_direct_support_reduced_profiles"] == 4, "wrong full support-reduced count")
    require(search["full_rank_slack_profiles"] == 4, "wrong full rank-slack count")
    require(search["full_support_reduced_extension_profiles"] == 4, "wrong support extension count")
    require(search["best_template_id"] == "ninerow_w3_c3_d1", "wrong best template")
    require(search["best_mutation_id"] == "w3_c3_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_basis_id"] == "basisaware_0_1_2_3_5_10", "wrong best basis")
    require(search["best_failure_mode"] == "DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY", "wrong best failure")
    require(
        search["sample_failure_counts"]
        == {
            "DCHAMBER_SAMPLE_LOWER_SUPPORT": 19,
            "DCHAMBER_SAMPLE_NINE_ROW": 19,
            "DCHAMBER_SAMPLE_RANK_SLACK": 16,
            "DCHAMBER_SAMPLE_SUPPORT_REDUCED": 54,
        },
        "wrong sampled failure counts",
    )
    require(search["full_failure_counts"] == {"TCHAMBER_DIRECT_SUPPORT_REDUCED": 4}, "wrong full failure counts")
    require(
        search["screen_counts"]
        == {
            "TCHAMBER_FORCED_IDENTITY": 3,
            "TCHAMBER_LOW_FUNCTIONAL_SPAN": 18,
            "TCHAMBER_STRUCTURAL_PASS": 459,
        },
        "wrong screen counts",
    )

    best = record["best_full_profile"]
    require(best["template_id"] == "ninerow_w3_c3_d1", "wrong best full template")
    require(best["mutation_id"] == "w3_c3_d1", "wrong best full mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best full assignment")
    require(best["assignment_seed"] == 117186, "wrong best full seed")
    require(best["basis_id"] == "basisaware_0_1_2_3_5_10", "wrong best full basis")
    require(best["basis_class_indices"] == [0, 1, 2, 3, 5, 10], "wrong best basis classes")
    require(best["basis_support_sizes"] == [216, 179, 148, 142, 111, 74], "wrong best support sizes")
    require(best["coefficient_matrix_shape"] == [15, 6], "wrong best matrix shape")
    require(best["directions_tested"] == 1508598, "wrong best direction count")
    require(best["pair_clear_directions"] == 360360, "wrong best pair-clear count")
    require(best["distinct_pair_clear_chambers"] == 178, "wrong best chamber count")
    require(best["nine_row_or_better_chambers"] == 31, "wrong best nine-row chambers")
    require(best["direct_support_reduced_chambers"] == 10, "wrong direct support chambers")
    require(best["rank_slack_chambers"] == 20, "wrong rank slack")
    require(best["support_reduced_extensions"] == 40, "wrong support-reduced extensions")
    require(best["deep_rank_slack_chambers"] == 0, "unexpected deep rank slack")
    require(best["best_failure_mode"] == "TCHAMBER_DIRECT_SUPPORT_REDUCED", "wrong best full failure")

    direct = best["best_direct_support_reduced_chamber"]
    require(direct["zero_row_count"] == 8, "wrong direct zero count")
    require(direct["active_row_count"] == 7, "wrong direct active count")
    require(direct["inactive_rank"] == 5, "wrong direct inactive rank")
    require(direct["inactive_kernel_nullity"] == 1, "wrong direct inactive nullity")
    require(direct["zero_row_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong direct zero classes")
    require(direct["active_row_classes"] == [4, 9, 11, 12, 13, 15, 16], "wrong direct active classes")
    require(direct["exemplar_direction"] == [1, 0, 14, 6, 11, 6], "wrong direct direction")
    require(direct["exemplar_weight"] == 5, "wrong direct direction weight")

    rank = best["best_rank_slack_chamber"]
    require(rank["zero_row_count"] == 7, "wrong rank-slack zero count")
    require(rank["active_row_count"] == 8, "wrong rank-slack active count")
    require(rank["inactive_rank"] == 4, "wrong rank-slack inactive rank")
    require(rank["inactive_kernel_nullity"] == 2, "wrong rank-slack nullity")
    require(rank["zero_row_classes"] == [6, 7, 8, 14, 18, 19, 20], "wrong rank-slack zero classes")
    require(rank["active_row_classes"] == [4, 9, 11, 12, 13, 15, 16, 17], "wrong rank-slack active classes")
    require(rank["exemplar_direction"] == [1, 4, 1, 6, 11, 6], "wrong rank-slack direction")

    for row in search["full_profile_summaries"]:
        require(row["best_failure_mode"] == "TCHAMBER_DIRECT_SUPPORT_REDUCED", "full profile not support-reduced")
        require(row["deep_rank_slack_chambers"] == 0, "full profile has deep rank slack")
        require(row["direct_support_reduced_chambers"] > 0, "full profile lacks support-reduced chamber")

    for phrase in [
        "CANDIDATE / DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY",
        "mutations generated = 160",
        "sample deep rank-slack profiles = 0",
        "full deep rank-slack profiles = 0",
        "template = ninerow_w3_c3_d1",
        "zero row count = 8",
        "inactive rank = 5",
        "inactive rank = 4",
        "eight zero rows",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "deep_rank_slack_chambers",
        "DEEP_RANKSLACK_FOUND",
        "DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY",
        "global obstruction outside the tested deeper rank-slack front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "sampled_profiles": search["sampled_profiles"],
        "full_profiles_scanned": search["full_profiles_scanned"],
        "full_direct_support_reduced_profiles": search["full_direct_support_reduced_profiles"],
        "full_deep_rank_slack_profiles": search["full_deep_rank_slack_profiles"],
        "best_zero_row_count": direct["zero_row_count"],
        "best_active_row_count": direct["active_row_count"],
        "best_rank_slack_zero_row_count": rank["zero_row_count"],
        "best_rank_slack_inactive_rank": rank["inactive_rank"],
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
        print(f"PASS: M1 a=327 pair-clear deeper rank-slack front (status={result['proof_status']})")


if __name__ == "__main__":
    main()
