#!/usr/bin/env python3
"""Verify the M1 a=327 prescribed nonbasis kernel generator ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_prescribed_nonbasis_kernel_generator.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_prescribed_nonbasis_kernel_generator.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "synthetic rowspace edits",
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

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "46b73ec", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "ACTUAL_TEMPLATE_ROWSPACES_ONLY", "wrong realization status")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / PNK_NEAR_KERNEL_FORCED_PAIR / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_nonbasis_row_dependency"]
    require(previous["commit"] == "46b73ec", "wrong previous commit")
    require(previous["systems_tested"] == 384, "wrong previous systems count")
    require(previous["near_kernel_profiles"] == 252, "wrong previous near-kernel count")
    require(previous["pair_projection_clear_actual_kernels"] == 0, "unexpected previous pair-clear kernel")
    require(previous["best_failure_mode"] == "NBDEP_NEAR_KERNEL_ONLY", "wrong previous failure")

    search = record["prescribed_nonbasis_kernel"]
    require(search["templates_generated"] == 64, "wrong template count")
    require(search["systems_tested"] == 384, "wrong systems tested")
    require(search["profile_source"] == "previous_summaries", "wrong profile source")
    require(search["previous_front_profiles"] == 70, "wrong previous-front profile count")
    require(search["structural_pass_candidates"] == 384, "wrong structural-pass count")
    require(search["target_present_candidates"] == 84, "wrong target-present count")
    require(search["forced_basis_combinations"] == 7498470, "wrong forced-basis combo count")
    require(search["forced_basis_profiles_tested"] == 84, "wrong forced-basis profile count")
    require(search["row_removal_limit"] == 3, "wrong row-removal limit")
    require(search["actual_kernel_profiles"] == 0, "unexpected actual kernel")
    require(search["near_kernel_profiles"] == 12, "wrong near-kernel count")
    require(search["actual_pair_clear_kernel_profiles"] == 0, "unexpected actual pair-clear kernel")
    require(search["near_pair_clear_kernel_profiles"] == 0, "unexpected near pair-clear kernel")
    require(search["actual_kernel_forced_pair_profiles"] == 0, "unexpected actual forced-pair kernel")
    require(search["near_kernel_forced_pair_profiles"] == 12, "wrong near forced-pair count")
    require(search["remove_limit_full_rank_profiles"] == 72, "wrong remove-limit full-rank count")
    require(search["pair_projection_clear_actual_kernels"] == 0, "unexpected pair-clear actual kernel")
    require(search["best_template_id"] == "rankdefect_hyperplane_r0_out7", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best assignment")
    require(search["best_target_mode"] == "primary_e4", "wrong best target mode")
    require(search["best_min_rows_to_remove"] == 2, "wrong best row-removal count")
    require(search["best_forced_pair_count"] == 10, "wrong best forced-pair count")
    require(search["best_kernel_vector"] == [0, 0, 1, 1, 1, 0], "wrong best kernel vector")
    require(search["best_failure_mode"] == "PNK_NEAR_KERNEL_FORCED_PAIR", "wrong best failure")
    require(
        search["failure_counts"]
        == {
            "PNK_NEAR_KERNEL_FORCED_PAIR": 12,
            "PNK_REMOVE_LIMIT_FULL_RANK": 72,
            "PNK_TARGET_FUNCTIONAL_MISSING": 300,
        },
        "wrong failure counts",
    )
    require(search["screen_counts"] == {"JOINT_TEMPLATE_STRUCTURAL_PASS": 384}, "wrong screen counts")

    best = record["best_candidate"]
    require(best["template_id"] == "rankdefect_hyperplane_r0_out7", "wrong best candidate template")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "wrong best candidate assignment")
    require(best["target_functional_present_modes"] == ["primary_e4"], "wrong target-present modes")
    require(best["target_functional_missing_modes"] == ["both_residuals"], "wrong target-missing modes")
    require(best["actual_pair_clear_kernel_profiles"] == 0, "unexpected best actual pair-clear kernel")
    require(best["near_pair_clear_kernel_profiles"] == 0, "unexpected best near pair-clear kernel")
    require(best["near_kernel_forced_pair_profiles"] == 1, "wrong best near forced-pair profile count")

    profile = best["best_profile"]
    require(profile["basis_id"] == "nbdep_primary_e4_union_253_1_7_14_15_16_18", "wrong best basis")
    require(profile["coefficient_matrix_shape"] == [13, 6], "wrong coefficient matrix shape")
    require(profile["coefficient_rank"] == 6, "wrong coefficient rank")
    require(profile["min_rows_to_remove_for_kernel"] == 2, "wrong profile row-removal count")
    require(profile["removed_row_indices"] == [1, 5], "wrong removed rows")
    require(profile["residual_row_classes"] == [2, 6], "wrong residual classes")
    require(profile["kernel_vector"] == [0, 0, 1, 1, 1, 0], "wrong profile kernel vector")
    require(profile["forced_pair_count"] == 10, "wrong profile forced-pair count")
    require(
        profile["forced_pairs"] == ["P12", "P13", "P15", "P16", "P23", "P25", "P26", "P35", "P36", "P56"],
        "wrong forced pairs",
    )
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "profile source = previous_summaries",
        "previous front profiles = 70",
        "actual pair-clear kernel profiles = 0",
        "near pair-clear kernel profiles = 0",
        "forced pair count = 10",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "near_pair_clear_kernel_profiles": search["near_pair_clear_kernel_profiles"],
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
        print(f"PASS: M1 a=327 prescribed nonbasis kernel generator (status={result['proof_status']})")


if __name__ == "__main__":
    main()
