#!/usr/bin/env python3
"""Verifier for the M1 a=327 post-D2-split pair-7 repair packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_post_d2split_pair7_repair.json")
TARGET_AGREEMENT = 327
PAIR7_TARGET = 2 * TARGET_AGREEMENT
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "POST_D2_PAIR7_NOT_REPAIRED",
    "POST_D2_PAIR7_REPAIR_UNDOES_D2_SPLIT",
    "POST_D2_PAIR7_REPAIR_COLLAPSE_RETURNS",
    "POST_D2_PAIR7_REPAIR_CAPACITY_LOSS",
    "POST_D2_PAIR7_REPAIR_LOW_RESCHEDULE",
    "POST_D2_EXACT_CANDIDATE",
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
    require(record["source_commit"] == "f272e60", "wrong source commit")
    require(record["construction_mode"] == "post_d2split_pair7_repair", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["exact_vectors_constructed"] == 76, "wrong baseline vector count")
    require(baseline["d2_split_vectors"] == 72, "wrong baseline D2 split count")
    require(baseline["capacity_preserving_d2_split_vectors"] == 48, "wrong baseline capacity split count")
    require(baseline["low_collapse_capacity_preserving_d2_splits"] == 24, "wrong baseline low-collapse count")
    require(baseline["best_capacity_upper_bound"] == 439, "wrong baseline capacity")
    require(baseline["best_pair_B_values"] == [1024, 514, 1024, 1024, 1024], "wrong baseline pair values")
    require(baseline["best_failure_mode"] == "RESIDUAL12_SPLIT_COLLAPSE_RETURNS", "wrong baseline failure")

    search = record["post_d2_pair7_repair"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["base_vectors_tested"] == 6, "wrong base vector count")
    require(search["pin_sets_tested"] == 72, "wrong repair pin count")
    require(search["nullspace_samples_tested"] == 6, "wrong nullspace sample count")
    require(search["exact_vectors_constructed"] == 78, "wrong exact vector count")
    require(search["d2_split_retained"] == 78, "wrong retained D2 split count")
    require(search["capacity_preserving_vectors"] == 78, "wrong capacity-preserving count")
    require(search["low_collapse_capacity_preserving_vectors"] == 78, "wrong low-collapse count")
    require(search["pair27_repaired_vectors"] == 0, "unexpected pair27 repair")
    require(search["pair7_repaired_vectors"] == 0, "unexpected full pair7 repair")
    require(search["best_pair_B_values"] == [1024, 514, 513, 1024, 1024], "wrong best pair values")
    require(search["best_capacity_upper_bound"] == 366, "wrong best capacity")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["best_failure_mode"] == "POST_D2_PAIR7_NOT_REPAIRED", "wrong best failure")
    require(len(search["results"]) == 2, "wrong candidate count")

    exact_candidate_count = 0
    total_rows = 0
    for result in search["results"]:
        require(result["base_vector_count"] == 3, "wrong per-candidate base count")
        require(result["repair_attempt_count"] == 36, "wrong per-candidate repair count")
        rows = result["base_results"] + result["vector_results"]
        require(len(rows) == 39, "wrong per-candidate vector row count")
        require(sum(result["failure_mode_counts"].values()) == 39, "bad failure count total")
        total_rows += len(rows)
        for attempt in rows:
            require(attempt["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {attempt['failure_mode']}")
            require(attempt["d2_split"] is True, "D2 split was not retained")
            require(attempt["capacity_upper_bound"] >= TARGET_AGREEMENT, "capacity lost unexpectedly")
            require(attempt["six_class_dominance"] <= 20, "six-class collapse returned unexpectedly")
            if attempt["failure_mode"] == "POST_D2_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(attempt["exact_max_min"] >= TARGET_AGREEMENT, "exact candidate below target")
                require(min(attempt["pair_B_values"]) >= PAIR7_TARGET, "candidate pair Hall below target")

    require(total_rows == search["exact_vectors_constructed"], "bad total exact vector count")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative extraction status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "base_vectors_tested": search["base_vectors_tested"],
        "pin_sets_tested": search["pin_sets_tested"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "d2_split_retained": search["d2_split_retained"],
        "capacity_preserving_vectors": search["capacity_preserving_vectors"],
        "low_collapse_capacity_preserving_vectors": search["low_collapse_capacity_preserving_vectors"],
        "pair27_repaired_vectors": search["pair27_repaired_vectors"],
        "pair7_repaired_vectors": search["pair7_repaired_vectors"],
        "best_pair_B_values": search["best_pair_B_values"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
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
            "PASS: M1 a=327 post-D2 pair-7 repair "
            f"({result['pin_sets_tested']} repair pins)"
        )


if __name__ == "__main__":
    main()
