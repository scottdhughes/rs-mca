#!/usr/bin/env python3
"""Verifier for the M1 a=327 proxy-positive exact-extraction diagnostic."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_proxy_positive_exact_extraction.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_proxy_positive_exact_extraction_exact_audit.json")

TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
    "full GF(17^32) nullspace extraction",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assignment_floor(sample: dict[str, Any]) -> int:
    assignment = sample["assignment"]
    return -1 if assignment is None else int(assignment["exact_max_min"])


def verify_scan(record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["construction_mode"] == "proxy_positive_exact_extraction_diagnostic", "wrong mode")
    require(record["source"]["source_commit"] == "10ad190", "wrong source commit")
    require(record["source"]["source_best_proxy_max_min"] == 329, "wrong source best")
    require(record["source"]["source_best_agreement_vector"] == [329, 330, 329, 329, 329, 329, 329], "wrong source vector")
    require(record["source"]["source_proxy_candidate_system_count"] == 13, "wrong source system count")
    require(record["source"]["source_proxy_candidate_sample_count"] == 52, "wrong source sample count")
    require(record["multi_prime_proxy_primes"] == [7681, 10753, 11777, 12289, 13313], "wrong primes")
    require(record["samples_per_prime"] == 8, "wrong samples per prime")
    require(record["proxy_positive_systems"] == len(record["systems"]) == 13, "wrong system count")
    require(record["proxy_candidate_samples"] == 52, "wrong proxy sample count")
    require(record["multi_prime_robust_system_count"] == 13, "wrong robust count")
    require(record["rank_drop_system_count"] == 0, "unexpected rank drop")
    require(record["proof_status"] == "MULTIPRIME_ROBUST_PROXY_CANDIDATE", "wrong proof status")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    for system in record["systems"]:
        require(system["artifact_status"] == "MULTIPRIME_ROBUST_PROXY_CANDIDATE", "non-robust system")
        require(system["multi_prime_candidate_prime_count"] == 5, "wrong robust prime count")
        require(system["rank_drop_primes_vs_12289"] == [], "unexpected rank drop prime")
        require(len(system["prime_fingerprints"]) == 5, "wrong fingerprint count")
        for fingerprint in system["prime_fingerprints"]:
            require(fingerprint["rank"] == 640, "wrong fingerprint rank")
            require(fingerprint["nullity"] == 896, "wrong fingerprint nullity")
            require(fingerprint["candidate_sample_count"] >= 4, "missing candidate samples")
            require(assignment_floor(fingerprint["best"]) >= TARGET_AGREEMENT, "fingerprint misses target")
            require(fingerprint["best"]["capacity_upper_bound"] == 459, "wrong capacity upper bound")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["row"] == "RS[F_17^32,H,256]", "exact wrong row")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong target")
    require(exact["construction_mode"] == "proxy_positive_exact_extraction_prefix_rank_audit", "exact wrong mode")
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proof_status"] == scan["proof_status"], "source proof status mismatch")
    require(exact["source"]["source_proxy_positive_systems"] == 13, "source system mismatch")
    require(exact["source"]["source_proxy_candidate_samples"] == 52, "source sample mismatch")
    require(exact["source"]["source_multi_prime_robust_system_count"] == 13, "source robust mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["degree_bound"] == 256, "wrong degree bound")
    require(exact["audit_system_limit"] == 1, "wrong exact audit limit")
    require(exact["prefix_row_counts"] == [16, 32], "wrong prefix rows")
    require(exact["exact_audited_system_count"] == len(exact["results"]) == 1, "wrong exact result count")
    require(exact["prefix_rank_drop_count"] == 0, "unexpected exact prefix rank drop")
    require(exact["proof_status"] == "EXACT_PREFIX_ROWS_FULL_RANK", "wrong exact proof status")
    require(exact["mca_counted"] is False, "exact MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "missing exact non-claims")
    result = exact["results"][0]
    require(result["full_exact_nullspace_extraction"] == "NOT_RUN", "unexpected full extraction")
    require(result["status"] == "EXACT_PREFIX_ROWS_FULL_RANK", "wrong exact result status")
    require(result["prefix_rank_drop_found"] is False, "unexpected prefix rank drop")
    require(result["exact_prefix_rank_growth"] == [
        {"full_row_rank_prefix": True, "nullity_in_prefix_projection": 1520, "rank": 16, "rows": 16},
        {"full_row_rank_prefix": True, "nullity_in_prefix_projection": 1504, "rank": 32, "rows": 32},
    ], "wrong exact rank growth")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    verify_scan(scan)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "proxy_positive_systems": scan["proxy_positive_systems"],
        "proxy_candidate_samples": scan["proxy_candidate_samples"],
        "multi_prime_robust_system_count": scan["multi_prime_robust_system_count"],
        "rank_drop_system_count": scan["rank_drop_system_count"],
        "exact_prefix_rank_drop_count": exact["prefix_rank_drop_count"],
        "proof_status": scan["proof_status"],
        "exact_proof_status": exact["proof_status"],
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
            "PASS: M1 a=327 proxy-positive exact extraction "
            f"({result['multi_prime_robust_system_count']} robust systems, "
            f"exact prefix drops={result['exact_prefix_rank_drop_count']})"
        )


if __name__ == "__main__":
    main()
