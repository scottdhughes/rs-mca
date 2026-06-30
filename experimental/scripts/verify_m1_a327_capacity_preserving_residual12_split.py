#!/usr/bin/env python3
"""Verifier for the M1 a=327 capacity-preserving residual [1,2] split packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_capacity_preserving_residual12_split.json")
TARGET_AGREEMENT = 327
PAIR7_BASELINE = 631
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "RESIDUAL12_NOT_SPLIT",
    "RESIDUAL12_PIN_DOES_NOT_SPLIT",
    "RESIDUAL12_SPLIT_CAPACITY_LOSS",
    "RESIDUAL12_SPLIT_COLLAPSE_RETURNS",
    "RESIDUAL12_SPLIT_PAIR7_LOSS",
    "RESIDUAL12_SPLIT_LOW_RESCHEDULE",
    "RESIDUAL12_CAPACITY_PRESERVING_SPLIT",
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
    require(record["source_commit"] == "5105961", "wrong source commit")
    require(record["construction_mode"] == "capacity_preserving_residual12_split", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["hard_split_vectors"] == 40, "wrong baseline vector count")
    require(baseline["nondegenerate_vectors"] == 38, "wrong baseline nondegenerate count")
    require(baseline["capacity_preserving_nondegenerate_vectors"] == 0, "wrong baseline capacity-preserving count")
    require(baseline["best_capacity_upper_bound"] == 83, "wrong baseline capacity")
    require(baseline["best_pair_B_values"] == [575, 513, 512, 512, 512], "wrong baseline pair values")
    require(baseline["best_failure_mode"] == "RESIDUAL12_SPLIT_CAPACITY_LOSS", "wrong baseline failure")

    search = record["capacity_preserving_residual12_search"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["protected_rows"] == 64, "wrong protected row count")
    require(search["pin_sets_tested"] == 54, "wrong residual pin count")
    require(search["nullspace_samples_tested"] == 24, "wrong nullspace sample count")
    require(search["pin_sets_tested"] + search["nullspace_samples_tested"] == 78, "wrong attempt count")
    require(search["exact_vectors_constructed"] == 76, "wrong exact vector count")
    require(search["d2_split_vectors"] == 72, "wrong D2 split count")
    require(search["capacity_preserving_d2_split_vectors"] == 48, "wrong capacity-preserving D2 split count")
    require(
        search["low_collapse_capacity_preserving_d2_split_vectors"] == 24,
        "wrong low-collapse capacity-preserving count",
    )
    require(search["best_capacity_upper_bound"] == 439, "wrong best capacity")
    require(search["best_pair_B_values"] == [1024, 514, 1024, 1024, 1024], "wrong best pair values")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["best_failure_mode"] == "RESIDUAL12_SPLIT_COLLAPSE_RETURNS", "wrong best failure")
    require(len(search["results"]) == 2, "wrong candidate count")

    exact_candidate_count = 0
    low_collapse_capacity_count = 0
    for result in search["results"]:
        require(result["attempt_count"] == 39, "wrong per-candidate attempt count")
        require(len(result["vector_results"]) == result["attempt_count"], "missing raw vector attempts")
        require(len(result["retained_results"]) == 12, "wrong retained result count")
        require(sum(result["failure_mode_counts"].values()) == result["attempt_count"], "bad failure count total")
        for attempt in result["vector_results"]:
            require(attempt["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {attempt['failure_mode']}")
            if attempt.get("capacity_preserving_d2_split"):
                require(attempt["d2_split"] is True, "capacity-preserving split without D2 split")
                require(attempt["capacity_upper_bound"] >= TARGET_AGREEMENT, "capacity-preserving split below capacity")
            if attempt.get("low_collapse_capacity_preserving_d2_split"):
                low_collapse_capacity_count += 1
                require(attempt["six_class_dominance"] <= 20, "low-collapse split has high collapse")
            if attempt["failure_mode"] == "RESIDUAL12_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(attempt["distinct_codewords"] is True, "candidate is degenerate")
                require(attempt["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
                require(min(attempt["pair_B_values"]) >= 2 * TARGET_AGREEMENT, "candidate pair Hall below target")
            if attempt["failure_mode"] in {"RESIDUAL12_SPLIT_PAIR7_LOSS", "RESIDUAL12_SPLIT_COLLAPSE_RETURNS"}:
                require(min(attempt.get("pair_B_values", [0])) < PAIR7_BASELINE or attempt.get("six_class_dominance", 0) > 20,
                        "misclassified pair/collapse failure")

    require(low_collapse_capacity_count == search["low_collapse_capacity_preserving_d2_split_vectors"], "bad low-collapse count")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
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
        "d2_split_vectors": search["d2_split_vectors"],
        "capacity_preserving_d2_split_vectors": search["capacity_preserving_d2_split_vectors"],
        "low_collapse_capacity_preserving_d2_split_vectors": search[
            "low_collapse_capacity_preserving_d2_split_vectors"
        ],
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
            "PASS: M1 a=327 capacity-preserving residual [1,2] split "
            f"({result['capacity_preserving_d2_split_vectors']} capacity-preserving D2 splits)"
        )


if __name__ == "__main__":
    main()
