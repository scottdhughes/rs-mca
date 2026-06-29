#!/usr/bin/env python3
"""Verifier for the M1 a=327 balanced MILP target/codeword solver."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_balanced_target_milp_codeword_solver.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_balanced_target_milp_codeword_solver_exact_audit.json")

TARGET_AGREEMENT = 327
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


def best_assignment_floor(row: dict[str, Any]) -> int:
    assignment = row["best"]["assignment"]
    return -1 if assignment is None else int(assignment["exact_max_min"])


def verify_scan(record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["construction_mode"] == "balanced_target_milp_codeword_solver", "wrong construction mode")
    require(record["baseline"]["current_public_agreement"] == 326, "wrong baseline agreement")
    require(record["baseline"]["current_lower_bound"] == 7, "wrong baseline lower bound")
    require(record["model"]["anchor"] == "P_1 = 0", "wrong anchor")
    require(record["model"]["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(record["model"]["target_selection"] == "MILP-selected partial received-word value-class constraints", "wrong target model")
    require(record["model"]["samples_per_system"] == 16, "wrong samples per system")
    require(record["row_budgets"] == [384, 448, 512], "wrong row budgets")
    require(
        record["selection_objectives"]
        == [
            "max_min_credit",
            "min_variance",
            "penalize_six_of_seven",
            "fiber_diversity",
            "hybrid_balance",
        ],
        "wrong objectives",
    )
    require(len(record["source_embedding_ids"]) == 8, "wrong source embedding count")
    require(record["target_system_count"] == 120, "wrong target system count")
    require(record["codeword_tuple_sample_count"] == 1920, "wrong codeword sample count")
    require(record["proxy_candidate_system_count"] == 0, "unexpected proxy candidate")
    require(record["exact_audit_triggers"] == [], "unexpected exact audit trigger")
    require(record["failure_mode_counts"]["HIGH_CAPACITY_IMBALANCED"] == 484, "wrong imbalance count")
    require(record["failure_mode_counts"]["LOW_CAPACITY"] == 1436, "wrong low-capacity count")
    require(record["retained_count"] == len(record["retained_results"]) == 32, "wrong retained count")
    require(record["proof_status"] == "TESTED_TARGET_SYSTEMS_NO_A327", "wrong proof status")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    require(record["best"]["target_system_id"] == "all_pair_boundary_bit_reversal__B512__fiber_diversity", "wrong best system")
    require(record["best"]["best"]["capacity_upper_bound"] == 457, "unexpected best capacity")
    require(best_assignment_floor(record["best"]) == 319, "unexpected best assignment floor")
    require(record["best"]["best"]["failure_mode"] == "HIGH_CAPACITY_IMBALANCED", "wrong best failure mode")
    for row in record["retained_results"]:
        require(row["proxy_candidate_count"] == 0, "retained row has proxy candidate")
        require(row["sample_count"] == 16, "wrong retained sample count")
        require(row["rank"] <= row["target_row_count"], "rank exceeds row count")
        for sample in row["sample_results"]:
            require(sample["failure_mode"] in {"LOW_CAPACITY", "HIGH_CAPACITY_IMBALANCED"}, "wrong failure mode")
            if sample["assignment"] is not None:
                require(sample["assignment"]["exact_max_min"] < TARGET_AGREEMENT, "sample reaches target")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong target")
    require(exact["construction_mode"] == "balanced_target_milp_codeword_solver_exact_audit", "exact wrong mode")
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proof_status"] == scan["proof_status"], "source proof status mismatch")
    require(exact["source"]["source_target_system_count"] == scan["target_system_count"], "source target count mismatch")
    require(
        exact["source"]["source_codeword_tuple_sample_count"] == scan["codeword_tuple_sample_count"],
        "source sample count mismatch",
    )
    require(exact["source"]["source_proxy_candidate_system_count"] == scan["proxy_candidate_system_count"] == 0, "source candidate mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["degree_bound"] == 256, "wrong degree bound")
    require(exact["exact_trigger_count"] == 0, "unexpected exact trigger")
    require(exact["exact_audited_count"] == 0, "unexpected exact audit")
    require(exact["results"] == [], "unexpected exact results")
    require(exact["proof_status"] == "NO_EXACT_AUDIT_TRIGGERED", "wrong exact proof status")
    require(exact["mca_counted"] is False, "exact MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "missing exact non-claims")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    verify_scan(scan)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "target_system_count": scan["target_system_count"],
        "codeword_tuple_sample_count": scan["codeword_tuple_sample_count"],
        "best_capacity_upper_bound": scan["best"]["best"]["capacity_upper_bound"],
        "best_proxy_exact_max_min": best_assignment_floor(scan["best"]),
        "exact_trigger_count": exact["exact_trigger_count"],
        "proof_status": scan["proof_status"],
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
            "PASS: M1 a=327 balanced MILP target/codeword solver "
            f"({result['target_system_count']} systems, best max-min={result['best_proxy_exact_max_min']})"
        )


if __name__ == "__main__":
    main()
