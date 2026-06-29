#!/usr/bin/env python3
"""Verifier for the M1 a=327 nondegenerate exact-lift packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_nondegenerate_exact_lift.json")
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
ALLOWED_FAILURES = {
    "DEGENERATE_CODEWORDS",
    "LOW_CAPACITY",
    "LOW_RESCHEDULE",
    "EXACT_A327_ASSIGNMENT",
    "SINGULAR_PARTIAL_PIVOT_MINOR",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assignment_floor(sample: dict[str, Any] | None) -> int:
    if sample is None:
        return -1
    assignment = sample.get("assignment")
    return -1 if assignment is None else int(assignment["exact_max_min"])


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["construction_mode"] == "nondegenerate_exact_lift", "wrong mode")
    require(record["source"]["source_commit"] == "f9a43ea", "wrong source commit")
    require(record["source"]["source_system_count"] == 13, "wrong source system count")
    require(record["source"]["source_best_proxy_max_min"] >= TARGET_AGREEMENT, "source misses proxy target")
    require(record["exact_field"] == "GF(17^32)", "wrong exact field")
    require(record["subgroup_order"] == 512, "wrong subgroup order")
    require(record["degree_bound"] == 256, "wrong degree bound")
    require(record["proxy_systems"]["count"] == 13, "wrong proxy system count")
    require(record["proxy_systems"]["stable_pivot_columns"] == 640, "wrong pivot count")
    require(record["proxy_systems"]["stable_free_columns"] == 896, "wrong free count")
    require(record["proxy_systems"]["best_proxy_max_min"] >= TARGET_AGREEMENT, "wrong best proxy")
    require(record["exact_audited_system_count"] == len(record["results"]) == 1, "wrong audited system count")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    search = record["exact_lift_search"]
    require(search["exact_vectors_constructed"] > 0, "no exact vectors")
    require(search["exact_vectors_constructed"] <= search["max_vector_evaluations"], "vector cap exceeded")
    require(search["row_subsets_tested"] >= 1, "no row subsets tested")
    require(search["free_schedules_tested"] >= 1, "no free schedules tested")
    require(search["value_patterns_tested"] >= 1, "no value patterns tested")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "unknown best failure mode")
    require(record["proof_status"] in {"CANDIDATE", "EXACT_EXTRACTION_NO_A327"}, "wrong proof status")
    require(record["candidate"]["reaches_327_exact"] == (record["proof_status"] == "CANDIDATE"), "candidate mismatch")

    exact_hits = 0
    nondegenerate = 0
    constructed = 0
    for result in record["results"]:
        require(result["common_pivot_count"] == 640, "result pivot count mismatch")
        require(result["common_free_count"] == 896, "result free count mismatch")
        require(result["pivot_stability_score"] == 1.0, "result stability mismatch")
        require(result["exact_vectors_constructed"] == len(result["evaluations"]), "evaluation count mismatch")
        require(result["failure_histogram"], "missing failure histogram")
        constructed += result["exact_vectors_constructed"]
        exact_hits += result["exact_a327_vectors"]
        nondegenerate += result["nondegenerate_vectors"]
        for subset_result in result["row_subset_rank_results"].values():
            require(subset_result["rank"] <= subset_result["rows"], "rank exceeds row count")
        for sample in result["evaluations"]:
            require(sample["solve"]["status"] in {"PARTIAL_SOLVE_OK", "SINGULAR_PARTIAL_PIVOT_MINOR"}, "bad solve")
            if sample["evaluation"] is None:
                continue
            require(sample["evaluation"]["status"] in ALLOWED_FAILURES, "bad evaluation status")
            require(sample["evaluation"]["capacity_upper_bound"] <= 512, "capacity impossible")
            require(set(sample["evaluation"]["coefficient_support_by_block"]) == {
                "D_2",
                "D_3",
                "D_4",
                "D_5",
                "D_6",
                "D_7",
            }, "bad support blocks")
            if sample["evaluation"]["status"] == "EXACT_A327_ASSIGNMENT":
                require(assignment_floor(sample["evaluation"]) >= TARGET_AGREEMENT, "candidate below target")
    require(constructed == search["exact_vectors_constructed"], "constructed mismatch")
    require(nondegenerate == search["nondegenerate_vectors"], "nondegenerate mismatch")
    require(exact_hits == record["exact_a327_vector_count"], "exact hit mismatch")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_hits == 0, "negative packet has exact hit")
    return {
        "status": "PASS",
        "exact_vectors_constructed": constructed,
        "nondegenerate_vectors": nondegenerate,
        "exact_a327_vector_count": exact_hits,
        "best_exact_max_min": search["best_exact_max_min"],
        "best_failure_mode": search["best_failure_mode"],
        "proof_status": record["proof_status"],
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
            "PASS: M1 a=327 nondegenerate exact lift "
            f"({result['exact_vectors_constructed']} vectors, exact_hits={result['exact_a327_vector_count']})"
        )


if __name__ == "__main__":
    main()
