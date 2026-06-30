#!/usr/bin/env python3
"""Verifier for the M1 a=327 protected-exchange exact audit packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_protected_exchange_exact_audit.json")
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
    "DEGENERATE_CODEWORDS",
    "PAIR7_REPAIR_LOST",
    "COLLAPSE_RETURNS",
    "CAPACITY_LOSS",
    "LOW_RESCHEDULE",
    "ASSIGNMENT_UNSOLVED",
    "EXACT_CANDIDATE_A327",
    "SINGULAR_EXACT_PIVOT_MINOR",
    "INSUFFICIENT_EXACT_PIVOTS",
    "ZERO_VECTOR",
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
    require(record["source_commit"] == "c9f2e4c", "wrong source commit")
    require(record["construction_mode"] == "protected_exchange_exact_audit", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    proxy = record["proxy_candidates"]
    require(proxy["count"] == 2, "wrong proxy candidate count")
    require(proxy["best_candidate_id"] == "7d2bb937c72e__PX48__one_for_two", "wrong best candidate id")
    require(proxy["best_proxy_max_min"] == 335, "wrong best proxy max-min")
    require(proxy["best_proxy_agreement_vector"] == [335, 335, 335, 335, 335, 335, 336], "wrong proxy vector")
    require(proxy["best_pair_B_values"] == [671, 671, 671, 671, 671], "wrong proxy pair values")
    require(proxy["added_six_class_dominance"] == 0, "wrong proxy added dominance")

    exact = record["exact_audit"]
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["candidates_tested"] == 2, "wrong exact candidate count")
    require(exact["row_schedules_tested"] == 8, "wrong row schedule count")
    require(exact["free_schedules_tested"] == 24, "wrong free schedule count")
    require(exact["exact_vectors_constructed"] >= 2, "no exact vectors constructed")
    require(exact["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure mode")

    exact_candidate_count = 0
    for result in exact["results"]:
        require(result["target_row_count"] == 640, "unexpected target row count")
        require(len(result["row_schedule_ranks"]) == 4, "bad rank schedule count")
        for rank_row in result["row_schedule_ranks"]:
            require(rank_row["rank"] <= rank_row["rows"], "rank exceeds rows")
            require(rank_row["full_row_rank"] is True, "tested exact row schedule lost full row rank")
        for attempt in result["vector_results"]:
            require(attempt["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {attempt['failure_mode']}")
            if attempt["failure_mode"] == "EXACT_CANDIDATE_A327":
                exact_candidate_count += 1
                require(attempt["distinct_codewords"] is True, "exact candidate degenerate")
                require(attempt["exact_max_min"] >= TARGET_AGREEMENT, "exact candidate below target")
                require(min(attempt["pair_B_values"]) >= 2 * TARGET_AGREEMENT, "exact candidate pair Hall not repaired")

    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_AUDIT_NO_A327"}, "bad proof status")
    if record["proof_status"] == "EXACT_AUDIT_NO_A327":
        require(exact_candidate_count == 0, "negative exact audit with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "proxy_candidates": proxy["count"],
        "candidates_tested": exact["candidates_tested"],
        "exact_vectors_constructed": exact["exact_vectors_constructed"],
        "nondegenerate_vectors": exact["nondegenerate_vectors"],
        "best_exact_max_min": exact["best_exact_max_min"],
        "best_capacity_upper_bound": exact["best_capacity_upper_bound"],
        "best_pair_B_values": exact["best_pair_B_values"],
        "best_failure_mode": exact["best_failure_mode"],
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
            "PASS: M1 a=327 protected-exchange exact audit "
            f"({result['candidates_tested']} candidates)"
        )


if __name__ == "__main__":
    main()
