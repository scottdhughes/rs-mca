#!/usr/bin/env python3
"""Dependency-free verifier for the M1 a=327 value-class-first search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_valueclass_first_witness_search as scanner


DATA_PATH = Path("experimental/data/m1_a327_valueclass_first_witness_search.json")

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
    candidates = scanner.candidate_designs()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == scanner.TARGET_AGREEMENT, "wrong target")
    require(record["candidate_count"] == len(candidates), "candidate count mismatch")
    require(record["candidate_design_hash"] == scanner.hash_payload(candidates), "candidate hash mismatch")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    for candidate in candidates:
        summary = candidate["summary"]
        require(summary["min_support_size"] == scanner.TARGET_AGREEMENT, "support size mismatch")
        require(summary["max_pair_intersection"] <= scanner.PAIR_CAP, "pair cap exceeded")
        require(summary["membership_histogram"] == {"4": 271, "5": 241}, "wrong histogram")

    rank_gate = record["rank_gate"]
    if rank_gate["status"] == "SAGE_PROXY_RANKED":
        results = rank_gate["results"]
        require(rank_gate["result_count"] == len(results), "rank result count mismatch")
        require(len(results) == len(candidates), "rank result count mismatch")
        require({row["candidate_id"] for row in results} == {item["candidate_id"] for item in candidates}, "candidate ids mismatch")
        best = max(
            results,
            key=lambda row: (
                row["proxy_nullity"],
                -row["proxy_rank"],
                row["max_pair_intersection"],
            ),
        )
        require(rank_gate["best"]["candidate_id"] == best["candidate_id"], "best candidate mismatch")
        if best["proxy_nullity"] == 0:
            require(record["proof_status"] == "TESTED_DESIGNS_NO_PROXY_NULLITY", "wrong no-proxy-nullity status")
            require(all(row["non_diagonal_solution_found"] is False for row in results), "unexpected solution")
        else:
            require(record["proof_status"] in {"CANDIDATE", "PROOF_RECORD"}, "wrong positive-nullity status")
    else:
        require(record["proof_status"] == "PARTIAL", "non-ranked record must be partial")

    return {
        "status": "PASS",
        "candidate_count": record["candidate_count"],
        "proof_status": record["proof_status"],
        "best_proxy_nullity": None if rank_gate["best"] is None else rank_gate["best"]["proxy_nullity"],
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
            "PASS: M1 a=327 value-class-first search record "
            f"({result['candidate_count']} candidates, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
