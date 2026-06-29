#!/usr/bin/env python3
"""Verifier for the M1 a=327 coefficient-nullspace target search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_coefficient_nullspace_target_search.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_coefficient_nullspace_target_search_exact_audit.json")

TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
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


def verify_scan(record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["construction_mode"] == "coefficient_nullspace_target_search", "wrong mode")
    require(record["model"]["anchor"] == "P_1 = 0", "wrong anchor model")
    require(record["root_tuple_count"] == 44, "wrong root tuple count")
    require(record["candidate_constant_count"] == 10736, "wrong constant candidate count")
    require(record["proxy_candidate_count"] == 0, "unexpected proxy candidate")
    require(record["proof_status"] == "TESTED_ROOT_SETS_NO_PROXY_A327", "wrong proxy proof status")
    require(record["best"]["capacity_upper_bound"] == 293, "unexpected proxy best cap")
    require(record["best"]["capacity_upper_bound"] < TARGET_AGREEMENT, "proxy best reaches target")
    require(record["retained_count"] == len(record["retained_results"]) == 32, "wrong retained count")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing proxy non-claims")
    for row in record["retained_results"]:
        require(row["capacity_upper_bound"] < TARGET_AGREEMENT, "retained row reaches target")
        require(row["status"] == "CAPACITY_BELOW_A327", "wrong retained status")
        require(row["assignment"] is None, "unexpected assignment result")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong target")
    require(exact["construction_mode"] == "coefficient_nullspace_target_exact_capacity_audit", "exact wrong mode")
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proxy_candidate_count"] == scan["proxy_candidate_count"] == 0, "source candidate mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["degree_bound"] == 256, "wrong degree bound")
    require(exact["top_labels_per_witness"] == 3, "wrong label count")
    require(exact["exact_root_tuple_count"] == len(exact["results"]) == 6, "wrong exact tuple count")
    require(exact["exact_candidate_count"] == 0, "unexpected exact candidate")
    require(exact["proof_status"] == "ROUTE_CUT_TESTED_ROOT_SETS", "wrong exact proof status")
    require(exact["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "missing exact non-claims")
    for row in exact["results"]:
        require(row["constant_candidates_tested"] == 244, "wrong exact constant count")
        require(row["best"]["capacity_upper_bound"] < TARGET_AGREEMENT, "exact tuple reaches target")
        require(row["status"] == "EXACT_CAPACITY_BELOW_A327", "wrong exact row status")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    verify_scan(scan)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "root_tuple_count": scan["root_tuple_count"],
        "candidate_constant_count": scan["candidate_constant_count"],
        "proxy_best_capacity_upper_bound": scan["best"]["capacity_upper_bound"],
        "exact_root_tuple_count": exact["exact_root_tuple_count"],
        "exact_candidate_count": exact["exact_candidate_count"],
        "proof_status": exact["proof_status"],
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
            "PASS: M1 a=327 coefficient-nullspace target search "
            f"({result['root_tuple_count']} root tuples, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
