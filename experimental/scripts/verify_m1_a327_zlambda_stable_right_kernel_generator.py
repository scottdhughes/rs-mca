#!/usr/bin/env python3
"""Verify the M1 a=327 Z_lambda-stable right-kernel generator ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_zlambda_stable_right_kernel_generator.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_zlambda_stable_right_kernel_generator.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
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
    require(record["source_commit"] == "f47d995", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / ZSTABLE_BASIS_UNION_TOO_LARGE / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_zlambda_audit"]
    require(previous["profiles_audited"] == 30, "wrong previous profile count")
    require(previous["stable_lift_targets"] == 0, "unexpected previous stable target")
    require(previous["coefficient_kernel_profiles"] == 30, "wrong previous coefficient kernel count")
    require(previous["best_basis_zero_union_size"] == 327, "wrong previous best union")
    require(previous["best_forced_pair_count"] == 15, "wrong previous forced-pair count")
    require(previous["best_failure_mode"] == "ZEXP_BASIS_UNION_TOO_LARGE", "wrong previous failure")

    search = record["zlambda_stable_generator"]
    require(search["templates_tested"] == 36, "wrong template count")
    require(search["systems_tested"] == 216, "wrong system count")
    require(search["structural_pass_candidates"] == 210, "wrong structural count")
    require(search["basis_profiles_tested"] == 13440, "wrong basis profile count")
    require(search["coefficient_kernel_profiles"] == 30, "wrong coefficient kernel count")
    require(search["stable_basis_union_profiles"] == 0, "unexpected stable basis-union profile")
    require(search["pair_projection_clear_profiles"] == 0, "unexpected pair-clear profile")
    require(search["proxy_candidates_tested"] == 0, "unexpected proxy candidate")
    require(search["proxy_positive_candidates"] == 0, "unexpected proxy positive")
    require(search["best_template_id"] == "single_outside_w7_v1", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(search["best_basis_zero_union_size"] == 327, "wrong best union")
    require(search["best_stable_common_multiplier_dimension"] == 0, "wrong stable dimension")
    require(search["best_forced_pair_count"] == 15, "wrong forced-pair count")
    require(search["best_proxy_rank"] is None, "unexpected proxy rank")
    require(search["best_proxy_nullity"] is None, "unexpected proxy nullity")
    require(search["best_failure_mode"] == "ZSTABLE_BASIS_UNION_TOO_LARGE", "wrong best failure")
    require(
        search["failure_counts"]
        == {
            "ZSTABLE_BASIS_UNION_TOO_LARGE": 6,
            "ZSTABLE_COEFFICIENT_FULL_RANK": 204,
            "ZSTABLE_LOW_FUNCTIONAL_SPAN": 6,
        },
        "failure counts mismatch",
    )
    require(search["screen_counts"] == {"JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN": 6, "JOINT_TEMPLATE_STRUCTURAL_PASS": 210}, "screen counts mismatch")
    require(len(search["candidate_summaries"]) == 216, "candidate summary count mismatch")

    best = record["best_candidate"]
    require(best["template_id"] == "single_outside_w7_v1", "best template mismatch")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "best strategy mismatch")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "best support mismatch")
    require(best["pair7_counts"] == [253, 253, 253, 253, 253], "best pair7 mismatch")
    require(best["max_pair_count"] == 253, "best max pair mismatch")
    require(best["functional_classes"] == 14, "best functional class mismatch")
    require(best["functional_span_rank"] == 6, "best span rank mismatch")
    require(best["coefficient_kernel_profiles"] == 5, "best coefficient-kernel count mismatch")
    require(best["stable_basis_union_profiles"] == 0, "best stable union mismatch")
    profile = best["best_profile"]
    require(profile["basis_id"] == "zstable_union_327_0_1_2_3_4_5", "wrong profile basis")
    require(profile["basis_class_indices"] == [0, 1, 2, 3, 4, 5], "wrong basis classes")
    require(profile["basis_support_sizes"] == [253, 216, 216, 216, 179, 179], "wrong basis supports")
    require(profile["coefficient_matrix_shape"] == [8, 6], "wrong coefficient shape")
    require(profile["coefficient_rank_gf17"] == 5, "wrong GF17 rank")
    require(profile["coefficient_nullity_gf17"] == 1, "wrong GF17 nullity")
    require(profile["coefficient_rank_gf12289"] == 5, "wrong GF12289 rank")
    require(profile["coefficient_nullity_gf12289"] == 1, "wrong GF12289 nullity")
    require(profile["basis_zero_union_size"] == 327, "wrong profile union")
    require(profile["stable_common_multiplier_dimension"] == 0, "wrong profile stable dimension")
    require(profile["kernel_basis"] == [[1, 1, 1, 1, 1, 1]], "wrong kernel basis")
    require(profile["best_forced_pair_count"] == 15, "wrong profile forced-pair count")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 216",
        "basis profiles tested = 13,440",
        "coefficient-kernel profiles = 30",
        "stable basis-union profiles = 0",
        "pair-projection-clear profiles = 0",
        "best basis-zero union size = 327",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "basis_profiles_tested": search["basis_profiles_tested"],
        "coefficient_kernel_profiles": search["coefficient_kernel_profiles"],
        "stable_basis_union_profiles": search["stable_basis_union_profiles"],
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
        print(f"PASS: M1 a=327 Z_lambda-stable right-kernel generator (status={result['proof_status']})")


if __name__ == "__main__":
    main()
