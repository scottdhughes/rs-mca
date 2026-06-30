#!/usr/bin/env python3
"""Verifier for the M1 a=327 residual [1,2] split packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_residual_12_split_pinned_nullspace.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "RESIDUAL12_PIN_INCONSISTENT",
    "RESIDUAL12_PIN_DOES_NOT_SPLIT",
    "RESIDUAL12_SPLIT_CAPACITY_LOSS",
    "RESIDUAL12_SPLIT_PAIR7_LOSS",
    "RESIDUAL12_SPLIT_LOW_RESCHEDULE",
    "RESIDUAL12_EXACT_CANDIDATE",
    "ASSIGNMENT_UNSOLVED",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "024481e", "wrong source commit")
    require(record["construction_mode"] == "residual_12_split_pinned_nullspace", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["best_capacity_upper_bound"] == 438, "wrong baseline capacity")
    require(baseline["best_pair_B_values"] == [1024, 1024, 512, 1024, 1024], "wrong baseline pair values")
    require(baseline["best_failure_mode"] == "PIN_DOES_NOT_SPLIT", "wrong baseline failure mode")
    collapse = baseline["strongest_split_remaining_collapse"]
    require([1, 2] in collapse, "strongest split should leave [1,2] collapsed")

    search = record["residual12_search"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["pin_sets_tested"] == 32, "wrong residual pin count")
    require(search["nullspace_samples_tested"] == 8, "wrong nullspace sample count")
    require(search["exact_vectors_constructed"] == 40, "wrong exact vector count")
    require(search["nondegenerate_vectors"] == 38, "wrong nondegenerate vector count")
    require(search["capacity_preserving_nondegenerate_vectors"] == 0, "unexpected capacity-preserving vector")
    require(search["best_exact_max_min"] is None, "unexpected exact rescheduler result")
    require(search["best_capacity_upper_bound"] == 83, "wrong best capacity")
    require(search["best_pair_B_values"] == [575, 513, 512, 512, 512], "wrong best pair values")
    require(search["best_failure_mode"] == "RESIDUAL12_SPLIT_CAPACITY_LOSS", "wrong best failure")
    require(len(search["results"]) == 2, "wrong candidate count")

    exact_candidate_count = 0
    total_attempts = 0
    for result in search["results"]:
        require(result["attempt_count"] == 20, "wrong per-candidate attempt count")
        require(len(result["vector_results"]) == result["attempt_count"], "missing raw vector attempts")
        require(len(result["retained_results"]) == 10, "wrong retained result count")
        failure_total = sum(result["failure_mode_counts"].values())
        require(failure_total == result["attempt_count"], "bad failure count total")
        total_attempts += result["attempt_count"]
        for attempt in result["vector_results"]:
            require(attempt["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {attempt['failure_mode']}")
            if attempt["failure_mode"] == "RESIDUAL12_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(attempt["distinct_codewords"] is True, "candidate is degenerate")
                require(attempt["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
                require(min(attempt["pair_B_values"]) >= 2 * TARGET_AGREEMENT, "candidate pair Hall below target")

    require(total_attempts == search["pin_sets_tested"] + search["nullspace_samples_tested"], "bad total attempts")
    require(record["proof_status"] in {"PROOF_RECORD", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad proof status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative extraction status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "pin_sets_tested": search["pin_sets_tested"],
        "nullspace_samples_tested": search["nullspace_samples_tested"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "nondegenerate_vectors": search["nondegenerate_vectors"],
        "capacity_preserving_nondegenerate_vectors": search["capacity_preserving_nondegenerate_vectors"],
        "best_exact_max_min": search["best_exact_max_min"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "best_pair_B_values": search["best_pair_B_values"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "PASS: M1 a=327 residual [1,2] split "
            f"({result['exact_vectors_constructed']} exact vectors)"
        )


if __name__ == "__main__":
    main()
