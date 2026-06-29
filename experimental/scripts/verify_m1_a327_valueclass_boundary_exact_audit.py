#!/usr/bin/env python3
"""Dependency-free verifier for the M1 a=327 value-class boundary exact audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_valueclass_boundary_search as scanner


DATA_PATH = Path("experimental/data/m1_a327_valueclass_boundary_exact_audit.json")
SOURCE_DATA_PATH = Path("experimental/data/m1_a327_valueclass_boundary_search.json")

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

EXPECTED_SELECTION = {
    "boundary_residual_45_c00_b5_200",
    "quotient_fiber_45_c00_b5_064",
    "pair_boundary_45_c15_b5_064",
    "boundary_residual_45_c00_b5_096",
    "pair_boundary_45_c00_b5_064",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    source = load_json(SOURCE_DATA_PATH)
    candidates = scanner.candidate_designs()
    candidate_by_id = {candidate["candidate_id"]: candidate for candidate in candidates}

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == scanner.TARGET_AGREEMENT, "wrong target")
    require(record["construction_mode"] == "valueclass_boundary_exact_audit", "wrong mode")
    require(record["candidate_count"] == len(candidates) == 200, "candidate count mismatch")
    require(record["exact_field"] == "GF(17^32)", "wrong exact field")
    require(record["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(record["subgroup_order"] == scanner.N, "wrong subgroup order")
    require(record["degree_bound"] == scanner.K, "wrong degree bound")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    require(record["source"]["source_candidate_count"] == source["candidate_count"], "source candidate count mismatch")
    require(
        record["source"]["source_candidate_design_hash"] == source["candidate_design_hash"],
        "source hash mismatch",
    )
    require(record["source"]["source_proxy_positive_count"] == 0, "source proxy unexpectedly positive")

    results = record["results"]
    require(record["exact_audited_count"] == len(results) == 5, "wrong exact audit count")
    require({row["candidate_id"] for row in results} == EXPECTED_SELECTION, "wrong candidate selection")
    require(record["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATES", "wrong proof status")
    require(record["exact_minor_full_rank_count"] == len(results), "not all minors full rank")
    require(record["exact_minor_singular_count"] == 0, "singular exact minor present")

    for row in results:
        candidate = candidate_by_id[row["candidate_id"]]
        summary = candidate["summary"]
        require(row["support_sizes"] == [scanner.TARGET_AGREEMENT] * scanner.LIST_SIZE, "support size mismatch")
        require(row["support_sizes"] == summary["support_sizes"], "candidate support mismatch")
        require(row["max_pair_intersection"] == scanner.PAIR_CAP, "max pair mismatch")
        require(row["pairs_at_255"] == summary["pairs_at_255"] >= 3, "cap pair mismatch")
        require(row["membership_histogram"] == {"4": 271, "5": 241}, "wrong histogram")
        require(row["compressed_variables"] == row["exact_minor_rank"], "rank not full")
        require(row["exact_nullity"] == 0, "nullity not zero")
        require(row["proxy_pivot_rows_count"] == row["compressed_variables"], "wrong pivot row count")
        require(row["status"] == "EXACT_MINOR_FULL_RANK", "wrong row status")
        require(row["agreement_verified"] is False, "unexpected agreement certificate")

    return {
        "status": "PASS",
        "exact_audited_count": record["exact_audited_count"],
        "proof_status": record["proof_status"],
        "exact_minor_full_rank_count": record["exact_minor_full_rank_count"],
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
            "PASS: M1 a=327 value-class boundary exact audit "
            f"({result['exact_audited_count']} candidates, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
