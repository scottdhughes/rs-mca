#!/usr/bin/env python3
"""Verify the M1 a=327 prescribed Z_lambda-stable relation generator ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_prescribed_zlambda_stable_relation_generator.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_prescribed_zlambda_stable_relation_generator.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "realized exact template vectors for the prescribed coefficients",
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
    require(record["agreement_target"] == 327, "wrong target")
    require(record["source_commit"] == "9cc5e91", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "SYNTHETIC_FUNCTIONAL_PROXY_TARGET", "wrong realization status")
    require(record["proof_status"] == "CANDIDATE / PZREL_PROXY_PENDING / PARTIAL / EXPERIMENTAL", "wrong proof status")

    previous = record["previous_stable_basis_relation_search"]
    require(previous["systems_tested"] == 216, "wrong previous systems")
    require(previous["stable_basis_profiles_tested"] == 12312, "wrong previous stable profiles")
    require(previous["stable_coefficient_kernel_profiles"] == 0, "unexpected previous kernel")
    require(previous["best_failure_mode"] == "ZREL_STABLE_COEFFICIENT_FULL_RANK", "wrong previous failure")

    search = record["prescribed_stable_relation"]
    require(search["templates_tested"] == 36, "wrong template count")
    require(search["systems_tested"] == 216, "wrong system count")
    require(search["structural_pass_candidates"] == 210, "wrong structural count")
    require(search["engineered_profiles_tested"] == 14310, "wrong engineered profile count")
    require(search["pair_projection_clear_profiles"] == 1770, "wrong pair-clear count")
    require(search["proxy_candidates_tested"] == 0, "unexpected proxy candidate")
    require(search["proxy_positive_candidates"] == 0, "unexpected proxy positive")
    require(search["best_template_id"] == "single_outside_w6_v0", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(search["best_basis_zero_union_size"] == 85, "wrong best union")
    require(search["best_stable_common_multiplier_dimension"] == 171, "wrong stable dimension")
    require(search["best_forced_pair_count"] == 0, "wrong forced-pair count")
    require(search["best_proxy_rank"] is None, "unexpected proxy rank")
    require(search["best_proxy_nullity"] is None, "unexpected proxy nullity")
    require(search["best_failure_mode"] == "PZREL_PROXY_PENDING", "wrong best failure")
    require(
        search["failure_counts"]
        == {
            "PZREL_LOW_FUNCTIONAL_SPAN": 6,
            "PZREL_NO_STABLE_BASIS": 6,
            "PZREL_PROXY_PENDING": 204,
        },
        "failure counts mismatch",
    )
    require(len(search["candidate_summaries"]) == 216, "candidate summary count mismatch")

    best = record["best_candidate"]
    require(best["template_id"] == "single_outside_w6_v0", "best template mismatch")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "best strategy mismatch")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(best["pair7_counts"] == [206, 206, 206, 206, 206], "pair7 mismatch")
    require(best["max_pair_count"] == 206, "max pair mismatch")
    require(best["functional_classes"] == 20, "functional class mismatch")
    require(best["functional_span_rank"] == 6, "span mismatch")
    require(best["pair_projection_clear_profiles"] == 15, "best pair-clear count mismatch")
    profile = best["best_profile"]
    require(profile["source_basis_id"] == "pzrel_union_85_14_15_16_17_18_19", "wrong source basis")
    require(profile["prescribed_kernel_id"] == "random_kernel_0", "wrong kernel id")
    require(profile["prescribed_kernel_vector"] == [1, 9, 4, 9, 13, 14], "wrong kernel vector")
    require(profile["basis_class_indices"] == [14, 15, 16, 17, 18, 19], "wrong basis indices")
    require(profile["basis_support_sizes"] == [29, 28, 21, 6, 1, 1], "wrong basis supports")
    require(profile["q_variable_count"] == 1450, "wrong q variable count")
    require(profile["coefficient_matrix_shape"] == [14, 6], "wrong coefficient shape")
    require(profile["coefficient_rank"] == 5, "wrong coefficient rank")
    require(profile["right_kernel_nullity"] == 1, "wrong right-kernel nullity")
    require(profile["right_kernel_verified"] is True, "right kernel not verified")
    require(profile["coordinate_rows_changed"] == 14, "wrong changed row count")
    require(profile["basis_zero_union_size"] == 85, "wrong profile union")
    require(profile["stable_common_multiplier_dimension"] == 171, "wrong profile stable dimension")
    require(profile["forced_pair_count"] == 0, "unexpected forced pairs")
    require(profile["forced_pairs"] == [], "forced pair list not empty")
    require(profile["proxy_result"] is None, "unexpected proxy result")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 216",
        "engineered profiles tested = 14,310",
        "pair-projection-clear profiles = 1,770",
        "basis-zero union size = 85",
        "stable common multiplier dimension = 171",
        "right-kernel nullity = 1",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "realization_status": record["realization_status"],
        "systems_tested": search["systems_tested"],
        "engineered_profiles_tested": search["engineered_profiles_tested"],
        "pair_projection_clear_profiles": search["pair_projection_clear_profiles"],
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
        print(f"PASS: M1 a=327 prescribed Z_lambda-stable relation generator (status={result['proof_status']})")


if __name__ == "__main__":
    main()
