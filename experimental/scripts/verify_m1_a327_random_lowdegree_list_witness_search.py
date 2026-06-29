#!/usr/bin/env python3
"""Dependency-free verifier for the M1 a=327 random low-degree search record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_random_lowdegree_list_witness_search as scanner


DATA_PATH = Path("experimental/data/m1_a327_random_lowdegree_list_witness_search.json")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    descriptors = scanner.candidate_descriptors()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == scanner.TARGET_AGREEMENT, "wrong target")
    require(record["candidate_count"] == len(descriptors), "candidate count mismatch")
    require(
        record["candidate_descriptor_hash"] == scanner.hash_payload(descriptors),
        "candidate descriptor hash mismatch",
    )
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    exact = record["exact_evaluation"]
    if exact["status"] == "SAGE_EVALUATED":
        results = exact["results"]
        require(exact["result_count"] == len(results), "result count mismatch")
        require(len(results) == len(descriptors), "exact result count mismatch")
        by_id = {row["candidate_id"]: row for row in results}
        require(set(by_id) == {item["candidate_id"] for item in descriptors}, "candidate ids mismatch")
        best = max(results, key=lambda row: row["capacity_upper_bound"])
        require(exact["best"]["candidate_id"] == best["candidate_id"], "best candidate mismatch")
        require(exact["best"]["capacity_upper_bound"] == best["capacity_upper_bound"], "best upper mismatch")
        if best["capacity_upper_bound"] < record["agreement_target"]:
            require(record["proof_status"] == "TESTED_TUPLES_NO_A327", "wrong no-candidate status")
            require(
                all(row["solver_status"] == "SKIPPED_BY_CAPACITY_UPPER_BOUND" for row in results),
                "unexpected assignment solver status",
            )
        else:
            require(record["proof_status"] in {"CANDIDATE", "PARTIAL"}, "wrong candidate status")
    else:
        require(record["proof_status"] == "PARTIAL", "non-evaluated record must be partial")

    return {
        "status": "PASS",
        "candidate_count": record["candidate_count"],
        "proof_status": record["proof_status"],
        "best_capacity_upper_bound": None
        if exact["best"] is None
        else exact["best"]["capacity_upper_bound"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "PASS: M1 a=327 random low-degree search record "
            f"({result['candidate_count']} candidates, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
