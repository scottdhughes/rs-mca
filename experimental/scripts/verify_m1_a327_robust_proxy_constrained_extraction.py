#!/usr/bin/env python3
"""Verifier for the M1 a=327 robust-proxy constrained extraction packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction_exact_audit.json")

TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list proof record",
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
    require(record["construction_mode"] == "robust_proxy_constrained_extraction", "wrong mode")
    require(record["source"]["source_commit"] == "bf374dc", "wrong source commit")
    require(record["source"]["source_proxy_positive_systems"] == 13, "wrong source systems")
    require(record["source"]["source_proxy_candidate_samples"] == 52, "wrong source samples")
    require(record["source"]["source_multi_prime_robust_system_count"] == 13, "wrong source robust count")
    require(record["proxy_primes"] == [7681, 10753, 11777, 12289, 13313], "wrong proxy primes")
    require(record["system_count"] == len(record["systems"]) == 13, "wrong system count")
    require(record["systems_with_stable_pivot_order"] == 13, "wrong stable pivot-order count")
    require(record["systems_with_stable_free_order"] == 13, "wrong stable free-order count")
    require(record["systems_with_stable_pivot_rows"] == 13, "wrong stable pivot-row count")
    require(record["constrained_schedule_proxy_positive_system_count"] == 13, "wrong schedule-positive count")
    require(record["proof_status"] == "CONSTRAINED_SCHEDULE_PROXY_A327", "wrong proof status")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    best = record["best"]
    require(best["pivot_stability_score"] == 1.0, "wrong best stability")
    require(best["common_pivot_count"] == 640, "wrong common pivot count")
    require(best["common_free_count"] == 896, "wrong common free count")
    require(best["best_schedule"]["schedule_id"] == "proxy_support_common_free_24", "wrong best schedule")
    require(best["best_schedule"]["candidate_prime_count"] == 5, "wrong best schedule prime count")
    require(assignment_floor(best["best_schedule"]["best"]) == 329, "wrong best schedule floor")
    for system in record["systems"]:
        require(system["common_pivot_count"] == 640, "system common pivot mismatch")
        require(system["common_free_count"] == 896, "system common free mismatch")
        require(system["pivot_order_stable"] is True, "pivot order unstable")
        require(system["free_order_stable"] is True, "free order unstable")
        require(system["pivot_row_order_stable"] is True, "pivot row order unstable")
        require(system["pivot_stability_score"] == 1.0, "stability not maximal")
        require(system["best_schedule"]["candidate_prime_count"] == 5, "schedule not robust")
        require(assignment_floor(system["best_schedule"]["best"]) >= TARGET_AGREEMENT, "schedule misses target")
        require(set(system["row_subset_candidates"]) >= {
            "proxy_pivot_rows_64",
            "proxy_pivot_rows_128",
            "deficit_rows_64",
            "fiber_diverse_rows_64",
            "full_target_row_sample_64",
        }, "missing row subsets")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["row"] == "RS[F_17^32,H,256]", "exact wrong row")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong target")
    require(exact["construction_mode"] == "robust_proxy_constrained_extraction_exact_audit", "exact wrong mode")
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proof_status"] == scan["proof_status"], "source status mismatch")
    require(exact["source"]["source_system_count"] == 13, "source system count mismatch")
    require(exact["source"]["source_constrained_schedule_proxy_positive_system_count"] == 13, "source schedule mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["degree_bound"] == 256, "wrong degree bound")
    require(exact["row_subsets"] == ["proxy_pivot_rows_64", "fiber_diverse_rows_64"], "wrong row subsets")
    require(exact["partial_solve_row_subset"] == "proxy_pivot_rows_64", "wrong partial subset")
    require(exact["exact_audited_system_count"] == len(exact["results"]) == 1, "wrong exact count")
    require(exact["exact_partial_solve_a327_count"] == 0, "unexpected exact hit")
    require(exact["row_subset_rank_drop_count"] == 0, "unexpected exact rank drop")
    require(exact["proof_status"] == "EXACT_CONSTRAINED_EXTRACTION_NO_A327", "wrong exact proof status")
    require(exact["mca_counted"] is False, "exact MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "missing exact non-claims")
    result = exact["results"][0]
    require(result["common_pivot_count"] == 640, "exact common pivot mismatch")
    require(result["common_free_count"] == 896, "exact common free mismatch")
    require(result["best_schedule_id"] == "proxy_support_common_free_24", "exact wrong schedule")
    require(result["best_schedule_candidate_prime_count"] == 5, "exact schedule not robust")
    require(result["row_subset_rank_drop_found"] is False, "unexpected row-subset drop")
    require(result["row_subset_rank_results"] == [
        {"full_row_rank": True, "rank": 64, "rows": 64, "subset": "proxy_pivot_rows_64"},
        {"full_row_rank": True, "rank": 64, "rows": 64, "subset": "fiber_diverse_rows_64"},
    ], "wrong row-subset ranks")
    partial = result["partial_solve"]
    require(partial["status"] == "PARTIAL_SOLVE_OK", "partial solve failed")
    require(partial["rows"] == 64, "wrong partial row count")
    require(partial["free_column_count"] == 24, "wrong free-column count")
    direct = partial["direct_evaluation"]
    require(direct["status"] == "EXACT_DEGENERATE_CODEWORDS", "unexpected direct status")
    require(direct["distinct_codewords"] is False, "expected degenerate direct vector")
    require(direct["capacity_upper_bound"] == 438, "wrong direct capacity")
    require(assignment_floor(direct) == 256, "wrong direct max-min")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    verify_scan(scan)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "system_count": scan["system_count"],
        "stable_pivot_order": scan["systems_with_stable_pivot_order"],
        "stable_free_order": scan["systems_with_stable_free_order"],
        "constrained_schedule_proxy_positive_system_count": scan[
            "constrained_schedule_proxy_positive_system_count"
        ],
        "exact_partial_solve_a327_count": exact["exact_partial_solve_a327_count"],
        "row_subset_rank_drop_count": exact["row_subset_rank_drop_count"],
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
            "PASS: M1 a=327 robust-proxy constrained extraction "
            f"({result['system_count']} systems, exact hits={result['exact_partial_solve_a327_count']})"
        )


if __name__ == "__main__":
    main()
