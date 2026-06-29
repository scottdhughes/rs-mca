#!/usr/bin/env python3
"""Verifier for the M1 a=327 degree-1 residual nullspace search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_degree1_residual_nullspace_search.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_degree1_residual_nullspace_search_exact_audit.json")

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
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["construction_mode"] == "degree1_residual_nullspace_search", "wrong construction mode")
    require(record["model"]["anchor"] == "P_1 = 0", "wrong anchor model")
    require(record["model"]["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(record["model"]["top_labels_per_witness"] == 2, "wrong top-label count")
    require(record["source_root_tuple_count"] == 28, "wrong source root tuple count")
    require(record["root_tuple_count"] == 112, "wrong root tuple count")
    require(
        record["root_tuple_family_counts"]
        == {
            "all_pair_boundary_embedding_roots": 32,
            "cyclic_interval": 24,
            "quotient_fiber_plus_residual": 24,
            "seeded_random_255": 32,
        },
        "wrong root tuple family counts",
    )
    require(record["drop_modes"] == ["first", "middle", "last", "witness_index"], "wrong drop modes")
    require(record["residual_pattern_count_per_root_tuple"] == 13, "wrong residual count")
    require(record["candidate_constant_count"] == 48048, "wrong candidate count")
    require(record["proxy_candidate_count"] == 0, "unexpected proxy candidate")
    require(record["proof_status"] == "TESTED_DEGREE1_RESIDUALS_NO_PROXY_A327", "wrong proof status")
    require(record["best"]["capacity_upper_bound"] == 293, "unexpected best proxy cap")
    require(record["best"]["capacity_upper_bound"] < TARGET_AGREEMENT, "proxy best reaches target")
    require(record["best"]["root_tuple_id"] == "all_pair_boundary_random_shuffle_0255_drop_first", "wrong best root tuple")
    require(record["best"]["residual_id"] == "common_root_000", "wrong best residual")
    require(record["retained_count"] == len(record["retained_results"]) == 40, "wrong retained count")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing scan non-claims")
    require("a=327 interleaved-list certificate over GF(17^32)" in record["not_claimed"], "missing proxy certificate non-claim")
    for row in record["retained_results"]:
        require(row["capacity_upper_bound"] < TARGET_AGREEMENT, "retained row reaches target")
        require(row["status"] == "CAPACITY_BELOW_A327", "wrong retained row status")
        require(row["assignment"] is None, "unexpected assignment result")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong agreement target")
    require(
        exact["construction_mode"] == "degree1_residual_nullspace_exact_capacity_audit",
        "exact wrong construction mode",
    )
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proof_status"] == scan["proof_status"], "source proof status mismatch")
    require(exact["source"]["source_proxy_candidate_count"] == scan["proxy_candidate_count"] == 0, "source candidate mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["degree_bound"] == 256, "wrong degree bound")
    require(exact["top_labels_per_witness"] == 2, "wrong exact label count")
    require(exact["exact_selection_count"] == len(exact["results"]) == 7, "wrong exact selection count")
    require(exact["exact_candidate_count"] == 0, "unexpected exact candidate")
    require(exact["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATES", "wrong exact proof status")
    require(exact["mca_counted"] is False, "exact MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "missing exact non-claims")
    require("a=327 interleaved-list certificate" in exact["not_claimed"], "missing exact certificate non-claim")
    for row in exact["results"]:
        require(row["constant_candidates_tested"] == 33, "wrong exact constant candidate count")
        require(row["best"]["capacity_upper_bound"] < TARGET_AGREEMENT, "exact row reaches target")
        require(row["status"] == "EXACT_CAPACITY_BELOW_A327", "wrong exact row status")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    verify_scan(scan)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "source_root_tuple_count": scan["source_root_tuple_count"],
        "root_tuple_count": scan["root_tuple_count"],
        "candidate_constant_count": scan["candidate_constant_count"],
        "proxy_best_capacity_upper_bound": scan["best"]["capacity_upper_bound"],
        "exact_selection_count": exact["exact_selection_count"],
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
            "PASS: M1 a=327 degree-1 residual nullspace search "
            f"({result['root_tuple_count']} root tuples, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
