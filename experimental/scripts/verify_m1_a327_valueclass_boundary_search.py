#!/usr/bin/env python3
"""Dependency-free verifier for the M1 a=327 value-class boundary search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_valueclass_boundary_search as scanner


DATA_PATH = Path("experimental/data/m1_a327_valueclass_boundary_search.json")

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
    require(record["construction_mode"] == "valueclass_boundary_search", "wrong mode")
    require(record["candidate_count"] == len(candidates) == 200, "candidate count mismatch")
    require(record["candidate_design_hash"] == scanner.hash_payload(candidates), "candidate hash mismatch")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    family_counts = {
        family: sum(1 for item in candidates if item["family"] == family)
        for family in sorted({item["family"] for item in candidates})
    }
    require(record["candidate_families"] == family_counts, "family count mismatch")

    for candidate in candidates:
        summary = candidate["summary"]
        require(summary["support_sizes"] == [scanner.TARGET_AGREEMENT] * scanner.LIST_SIZE, "support size mismatch")
        require(summary["min_support_size"] == scanner.TARGET_AGREEMENT, "min support mismatch")
        require(summary["max_pair_intersection"] == scanner.PAIR_CAP, "boundary pair not at cap")
        require(summary["max_pair_intersection"] <= scanner.PAIR_CAP, "pair cap exceeded")
        require(summary["membership_histogram"] == {"4": 271, "5": 241}, "wrong histogram")
        require(summary["pairs_at_255"] >= 3, "missing capped target clique")

    rank_gate = record["rank_gate"]
    if rank_gate["status"] == "SAGE_PROXY_RANKED":
        retained = rank_gate["retained_results"]
        require(rank_gate["all_result_count"] == len(candidates), "rank result count mismatch")
        require(rank_gate["retained_proxy_count"] == len(retained), "retained count mismatch")
        require(len(retained) <= scanner.RETAINED_PROXY_COUNT, "too many retained results")
        require(rank_gate["best"] == retained[0], "best should be first retained result")
        require(rank_gate["all_result_hash"], "missing full rank-result hash")
        require(rank_gate["proxy_field"] == "GF(12289)", "wrong proxy field")
        require(rank_gate["exact_field"] == "GF(17^32)", "wrong exact field")

        retained_ids = {row["candidate_id"] for row in retained}
        candidate_ids = {item["candidate_id"] for item in candidates}
        require(retained_ids.issubset(candidate_ids), "unknown retained candidate")
        best = rank_gate["best"]
        if rank_gate["proxy_positive_count"] == 0:
            require(best["proxy_nullity"] == 0, "unexpected best proxy nullity")
            require(record["proof_status"] == "TESTED_DESIGNS_NO_PROXY_NULLITY", "wrong no-proxy-nullity status")
            require(record["exact_audited_count"] == 0, "unexpected exact audit")
        else:
            require(record["proof_status"] in {"CANDIDATE", "PROOF_RECORD"}, "wrong positive-nullity status")
    else:
        require(record["proof_status"] == "PARTIAL", "non-ranked record must be partial")

    return {
        "status": "PASS",
        "candidate_count": record["candidate_count"],
        "proof_status": record["proof_status"],
        "proxy_positive_count": rank_gate["proxy_positive_count"],
        "retained_proxy_count": rank_gate["retained_proxy_count"],
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
            "PASS: M1 a=327 value-class boundary search record "
            f"({result['candidate_count']} candidates, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
