#!/usr/bin/env python3
"""Verifier for the M1 a=327 protected-exchange nondegenerate lift packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_protected_exchange_nondegenerate_lift.json")
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
    "PIN_INCONSISTENT",
    "PIN_DOES_NOT_SPLIT",
    "PIN_SPLITS_CAPACITY_LOSS",
    "PIN_SPLITS_PAIR7_LOSS",
    "PIN_SPLITS_LOW_RESCHEDULE",
    "ASSIGNMENT_UNSOLVED",
    "EXACT_CANDIDATE_A327",
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
    require(record["source_commit"] == "a2d31ee", "wrong source commit")
    require(record["construction_mode"] == "protected_exchange_nondegenerate_lift", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["exact_audit_baseline"]
    require(baseline["proxy_candidates_tested"] == 2, "wrong baseline candidate count")
    require(baseline["exact_vectors_constructed"] == 26, "wrong baseline vector count")
    require(baseline["nondegenerate_vectors"] == 0, "wrong baseline nondegenerate count")
    require(baseline["best_exact_max_min"] == 287, "wrong baseline exact max-min")
    require(baseline["best_failure_mode"] == "DEGENERATE_CODEWORDS", "wrong baseline failure mode")

    lift = record["nondegenerate_lift"]
    require(lift["exact_field"] == "GF(17^32)", "wrong exact field")
    require(lift["pin_sets_tested"] == 12, "wrong pin set count")
    require(lift["exact_vectors_constructed"] == 12, "wrong constructed vector count")
    require(lift["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure mode")
    require(len(lift["results"]) == 2, "wrong candidate result count")

    exact_candidate_count = 0
    for result in lift["results"]:
        require(result["pin_attempt_count"] == 6, "wrong pin attempt count")
        failure_total = sum(result["failure_mode_counts"].values())
        require(failure_total == result["pin_attempt_count"], "bad failure count total")
        for row in result["retained_pin_results"]:
            require(row["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {row['failure_mode']}")
            if row["failure_mode"] == "EXACT_CANDIDATE_A327":
                exact_candidate_count += 1
                require(row["distinct_codewords"] is True, "candidate is degenerate")
                require(row["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")

    require(record["proof_status"] in {"PROOF_RECORD", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad proof status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative extraction status with candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "pin_sets_tested": lift["pin_sets_tested"],
        "exact_vectors_constructed": lift["exact_vectors_constructed"],
        "nondegenerate_vectors": lift["nondegenerate_vectors"],
        "capacity_preserving_nondegenerate_vectors": lift["capacity_preserving_nondegenerate_vectors"],
        "best_exact_max_min": lift["best_exact_max_min"],
        "best_capacity_upper_bound": lift["best_capacity_upper_bound"],
        "best_pair_B_values": lift["best_pair_B_values"],
        "best_failure_mode": lift["best_failure_mode"],
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
            "PASS: M1 a=327 protected-exchange nondegenerate lift "
            f"({result['pin_sets_tested']} pin sets)"
        )


if __name__ == "__main__":
    main()
