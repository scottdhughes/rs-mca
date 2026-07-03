#!/usr/bin/env python3
"""Verify the M1 a=327 right-kernel-engineered rank-feedback ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_right_kernel_engineered_rank_feedback.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_right_kernel_engineered_rank_feedback.md")

TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_LABELS = {
    "RIGHT_KERNEL_SUPPORT_FAIL",
    "RIGHT_KERNEL_PAIR_GUARD_FAIL",
    "RIGHT_KERNEL_FORCED_IDENTITY",
    "RIGHT_KERNEL_LOW_FUNCTIONAL_SPAN",
    "RIGHT_KERNEL_DIAGONAL_ANNIHILATOR",
    "RIGHT_KERNEL_STRUCTURAL_PASS",
    "RIGHT_KERNEL_COEFFICIENT_FULL_RANK",
    "RIGHT_KERNEL_PROXY_PENDING",
    "RIGHT_KERNEL_PROXY_FULL_RANK",
    "RIGHT_KERNEL_PROXY_NULLITY_POSITIVE",
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
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "e237ab6", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    dep = record["dependency_engineered"]
    require(dep["commit"] == "c3bb743", "wrong dependency commit")
    require(dep["systems_tested"] == 108, "wrong dependency system count")
    require(dep["proxy_positive_candidates"] == 0, "unexpected dependency positive")
    require(dep["best_template_id"] == "random_matroid_v3_seed_007_m6", "wrong dependency best")
    require(dep["best_proxy_rank"] == 1385, "wrong dependency rank")
    require(dep["best_proxy_nullity"] == 0, "wrong dependency nullity")

    syz = record["syzygy_proxy"]
    require(syz["commit"] == "e237ab6", "wrong syzygy commit")
    require(syz["coefficient_matrix_shape"] == [41, 6], "wrong syzygy coefficient shape")
    require(syz["coefficient_rank"] == 6, "wrong syzygy coefficient rank")
    require(syz["right_kernel_nullity"] == 0, "wrong syzygy right kernel")
    require(syz["left_syzygy_dimension"] == 35, "wrong syzygy left dimension")
    require(syz["best_failure_mode"] == "SYZYGY_PROXY_COEFFICIENT_FULL_RANK_QUOTIENT_FULL_RANK", "wrong syzygy failure")

    search = record["right_kernel_search"]
    require(search["templates_tested"] == 18, "wrong template count")
    require(search["systems_tested"] == 108, "wrong system count")
    require(search["structural_pass_candidates"] == 96, "wrong structural-pass count")
    require(search["coefficient_profiles_tested"] == 3276, "wrong coefficient profile count")
    require(search["right_kernel_positive_candidates"] == 0, "unexpected right-kernel positive")
    require(search["proxy_candidates_tested"] == 0, "unexpected proxy candidate")
    require(search["proxy_basis_profiles_tested"] == 0, "unexpected proxy profile")
    require(search["proxy_positive_candidates"] == 0, "unexpected proxy-positive candidate")
    require(search["best_template_id"] == "random_matroid_v3_seed_010_m6", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(search["best_functional_span_rank"] == 6, "wrong best span")
    require(search["best_proxy_rank"] is None, "unexpected best proxy rank")
    require(search["best_proxy_nullity"] is None, "unexpected best proxy nullity")
    require(search["best_failure_mode"] == "RIGHT_KERNEL_COEFFICIENT_FULL_RANK", "wrong best failure")
    require(search["failure_counts"] == {
        "RIGHT_KERNEL_COEFFICIENT_FULL_RANK": 96,
        "RIGHT_KERNEL_LOW_FUNCTIONAL_SPAN": 12,
    }, "failure counts mismatch")
    require(search["screen_counts"] == {
        "RIGHT_KERNEL_LOW_FUNCTIONAL_SPAN": 12,
        "RIGHT_KERNEL_STRUCTURAL_PASS": 96,
    }, "screen counts mismatch")
    require(set(search["failure_counts"]).issubset(ALLOWED_LABELS), "bad failure label")
    require(set(search["screen_counts"]).issubset(ALLOWED_LABELS), "bad screen label")

    summaries = search["candidate_summaries"]
    require(len(summaries) == search["systems_tested"], "summary count mismatch")
    require(sum(1 for row in summaries if row["structural_status"] == "RIGHT_KERNEL_STRUCTURAL_PASS") == 96, "summary structural count mismatch")
    require(sum(row["basis_profiles_tested"] for row in summaries) == search["coefficient_profiles_tested"], "summary profile count mismatch")
    require(sum(1 for row in summaries if row["right_kernel_profiles"]) == 0, "summary right-kernel count mismatch")

    best = record["best_candidate"]
    require(best["template_id"] == "random_matroid_v3_seed_010_m6", "best template mismatch")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "best strategy mismatch")
    require(best["support_vector"] == [TARGET_AGREEMENT] * 7, "best support mismatch")
    require(best["pair7_counts"] == [233, 233, 233, 233, 233], "best pair7 mismatch")
    require(best["max_pair_count"] == 233, "best max pair mismatch")
    require(best["functional_classes"] == 45, "best functional class mismatch")
    require(best["functional_span_rank"] == 6, "best span mismatch")
    require(best["annihilator_dimension"] == 0, "best annihilator mismatch")
    require(best["forced_functional_identities"] == 0, "best forced identity mismatch")
    require(best["basis_profiles_tested"] == 35, "best profile count mismatch")
    require(best["right_kernel_profiles"] == [], "best right-kernel profiles unexpected")
    require(best["selected_class_size_counts"] == {"3": 87, "4": 97, "5": 328}, "best size counts mismatch")

    require(record["m2_right_kernel_check"] is None, "unexpected M2 run")
    require(record["exact_audit"]["run"] is False, "unexpected exact audit")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 108",
        "structural-pass candidates = 96",
        "coefficient profiles tested = 3276",
        "right-kernel-positive candidates = 0",
        "random_matroid_v3_seed_010_m6",
        "full-rank nonbasis coefficient",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "structural_pass_candidates": search["structural_pass_candidates"],
        "coefficient_profiles_tested": search["coefficient_profiles_tested"],
        "right_kernel_positive_candidates": search["right_kernel_positive_candidates"],
        "best_template_id": search["best_template_id"],
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
        print(f"PASS: M1 a=327 right-kernel-engineered rank feedback (status={result['proof_status']})")


if __name__ == "__main__":
    main()
