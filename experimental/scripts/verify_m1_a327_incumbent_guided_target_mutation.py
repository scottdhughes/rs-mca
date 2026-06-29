#!/usr/bin/env python3
"""Verifier for the M1 a=327 incumbent-guided target mutation packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_incumbent_guided_target_mutation.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_incumbent_guided_target_mutation_exact_audit.json")

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


def assignment_floor(sample: dict[str, Any]) -> int:
    assignment = sample["assignment"]
    return -1 if assignment is None else int(assignment["exact_max_min"])


def verify_scan(record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["construction_mode"] == "incumbent_guided_target_mutation", "wrong mode")
    require(record["baseline_public_row"] == {"agreement": 326, "lower_bound": 7}, "wrong baseline")
    require(record["parent_solver"]["commit"] == "43a8a66", "wrong parent commit")
    require(record["parent_solver"]["best_proxy_max_min"] == 319, "wrong parent best max-min")
    require(record["parent_solver"]["best_agreement_vector"] == [319, 320, 319, 319, 319, 319, 319], "wrong parent vector")
    require(record["parent_solver"]["best_raw_capacity_upper_bound"] == 457, "wrong parent capacity")
    search = record["mutation_search"]
    require(search["base_incumbents"] == 5, "wrong incumbent count")
    require(search["mutation_rounds_per_incumbent"] == 10, "wrong mutation rounds")
    require(search["row_budgets"] == [512, 640], "wrong row budgets")
    require(search["mutated_systems"] == 50, "wrong mutated system count")
    require(search["samples_per_system"] == 32, "wrong samples per system")
    require(search["codeword_tuple_samples"] == 1600, "wrong sample count")
    require(search["best_proxy_max_min"] == 329, "wrong best proxy max-min")
    require(search["best_agreement_vector"] == [329, 330, 329, 329, 329, 329, 329], "wrong best vector")
    require(search["best_failure_mode"] == "CANDIDATE", "wrong best failure mode")
    require(search["failure_mode_counts"]["CANDIDATE"] == 52, "wrong candidate sample count")
    require(record["proxy_candidate_system_count"] == 13, "wrong proxy candidate system count")
    require(len(record["exact_audit_triggers"]) == 13, "wrong exact trigger count")
    require(record["retained_count"] == len(record["retained_results"]) == 40, "wrong retained count")
    require(record["proof_status"] == "CANDIDATE", "wrong proof status")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    best = record["best"]
    require(
        best["mutated_system_id"]
        == "all_pair_boundary_bit_reversal__B512__fiber_diversity__M07__variance_min__B640",
        "wrong best mutated system",
    )
    require(best["best"]["capacity_upper_bound"] == 459, "wrong best capacity")
    require(assignment_floor(best["best"]) == 329, "wrong best assignment floor")
    for row in record["retained_results"]:
        require(row["sample_count"] == 32, "wrong retained sample count")
        require(row["rank"] <= row["target_row_count"], "rank exceeds rows")
        if row["proxy_candidate_count"]:
            require(row["best"]["assignment"] is not None, "candidate row missing assignment")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["row"] == "RS[F_17^32,H,256]", "exact wrong row")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong target")
    require(exact["construction_mode"] == "incumbent_guided_target_mutation_exact_lift_audit", "exact wrong mode")
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proof_status"] == scan["proof_status"], "source status mismatch")
    require(exact["source"]["source_proxy_candidate_system_count"] == scan["proxy_candidate_system_count"], "source candidate mismatch")
    require(exact["source"]["source_exact_trigger_count"] == len(scan["exact_audit_triggers"]), "source trigger mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == 512, "wrong subgroup order")
    require(exact["degree_bound"] == 256, "wrong degree bound")
    require(exact["selection_limit"] == 3, "wrong selection limit")
    require(exact["exact_lift_samples_per_system"] == 4, "wrong lift samples")
    require(exact["exact_lift_audited_system_count"] == len(exact["results"]) == 3, "wrong exact system count")
    require(exact["exact_lift_a327_sample_count"] == 0, "unexpected exact lift hit")
    require(
        exact["exact_nullspace_extraction_status"] == "NOT_RUN_EXACT_GF1732_RREF_TOO_SLOW_FOR_THIS_PACKET",
        "wrong exact extraction status",
    )
    require(exact["proof_status"] == "EXACT_LIFTED_PROXY_CANDIDATES_NO_A327", "wrong exact proof status")
    require(exact["mca_counted"] is False, "exact MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "missing exact non-claims")
    best = exact["best"]
    require(best is not None, "missing exact best")
    sample = best["best_exact_lift_sample"]
    require(sample["capacity_upper_bound"] == 439, "wrong exact lift best capacity")
    require(assignment_floor(sample) == 257, "wrong exact lift best assignment")
    require(sample["distinct_codewords"] is False, "expected degenerate exact lift")
    for row in exact["results"]:
        require(row["proxy_best_max_min"] >= TARGET_AGREEMENT, "audited row not a proxy trigger")
        require(row["exact_lift_a327_sample_count"] == 0, "unexpected row exact hit")
        require(row["exact_lift_sample_count"] == 4, "wrong row sample count")
        for sample in row["sample_results"]:
            require(sample["status"] == "EXACT_LIFT_DEGENERATE_CODEWORDS", "unexpected lift status")
            require(sample["was_proxy_candidate"] is True, "expected proxy-candidate sample")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    verify_scan(scan)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "mutated_systems": scan["mutation_search"]["mutated_systems"],
        "codeword_tuple_samples": scan["mutation_search"]["codeword_tuple_samples"],
        "best_proxy_max_min": scan["mutation_search"]["best_proxy_max_min"],
        "proxy_candidate_system_count": scan["proxy_candidate_system_count"],
        "exact_lift_a327_sample_count": exact["exact_lift_a327_sample_count"],
        "exact_lift_best_max_min": assignment_floor(exact["best"]["best_exact_lift_sample"]),
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
            "PASS: M1 a=327 incumbent-guided target mutation "
            f"(best proxy max-min={result['best_proxy_max_min']}, "
            f"exact lift hits={result['exact_lift_a327_sample_count']})"
        )


if __name__ == "__main__":
    main()
