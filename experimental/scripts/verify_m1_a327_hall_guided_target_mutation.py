#!/usr/bin/env python3
"""Verifier for the M1 a=327 Hall-guided target mutation packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_hall_guided_target_mutation.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "HALL_NOT_REPAIRED",
    "HALL_REPAIR_DESTROYS_CAPACITY",
    "HALL_REPAIR_LOW_RESCHEDULE",
    "HALL_REPAIR_COLLAPSE_RETURNS",
    "HALL_REPAIR_UNSCHEDULED",
    "HALL_PROXY_CANDIDATE",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "ed4cf43", "wrong source commit")
    require(record["construction_mode"] == "hall_guided_target_mutation", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    baseline = record["hall_baseline"]
    require(baseline["best_tangent_max_min"] == 260, "wrong baseline max-min")
    require(baseline["best_tangent_capacity"] == 404, "wrong baseline capacity")
    require(baseline["best_tangent_hall_bound"] == 260, "wrong baseline Hall bound")
    require(len(baseline["tight_subsets"]) == 3, "expected three tight subsets")
    search = record["hall_guided_search"]
    retained = record["retained_results"]
    require(search["systems_tested"] == len(search["repair_row_budgets"]) * len(search["selection_objectives"]), "bad system count")
    require(search["codeword_tuple_samples"] == sum(row["sample_count"] for row in retained), "retained sample count mismatch")
    require(record["retained_count"] == len(retained) > 0, "bad retained count")
    failure_total = sum(search["failure_mode_counts"].values())
    require(failure_total == search["codeword_tuple_samples"], "bad failure counts")
    candidate_count = 0
    for row in retained:
        require(row["repair_row_budget"] in search["repair_row_budgets"], "unexpected repair budget")
        require(row["selection_objective"] in search["selection_objectives"], "unexpected objective")
        require(row["rank"] + row["nullity"] == 1536, "bad rank/nullity ledger")
        require(row["target_row_count"] <= 640, "row budget exceeded")
        require(len(row["predicted_tight_subset_B"]) == 3, "bad predicted B vector")
        for sample in row["retained_sample_results"]:
            require(sample["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {sample['failure_mode']}")
            require(len(sample["tight_subset_B"]) == 3, "bad sample tight B vector")
            require(len(sample["tight_subset_deficits_to_981"]) == 3, "bad sample deficit vector")
            if sample["proxy_max_min"] is not None:
                require(min(sample["agreement_vector"]) == sample["proxy_max_min"], "bad agreement vector")
            if sample["failure_mode"] == "HALL_PROXY_CANDIDATE":
                candidate_count += 1
                require(sample["proxy_max_min"] is not None and sample["proxy_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(record["proof_status"] in {"CANDIDATE", "TESTED_HALL_MUTATIONS_NO_A327"}, "bad proof status")
    if record["proof_status"] == "TESTED_HALL_MUTATIONS_NO_A327":
        require(candidate_count == 0, "negative status with candidate")
    if search["proxy_candidates"] > 0:
        require(record["exact_audit"]["triggered"] is True, "candidate should trigger exact audit")
    return {
        "status": "PASS",
        "systems_tested": search["systems_tested"],
        "codeword_tuple_samples": search["codeword_tuple_samples"],
        "proxy_candidates": search["proxy_candidates"],
        "best_proxy_max_min": search["best_proxy_max_min"],
        "best_hall_bound": search["best_hall_bound"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "best_six_class_dominance": search["best_six_class_dominance"],
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
            "PASS: M1 a=327 Hall-guided target mutation "
            f"({result['systems_tested']} systems)"
        )


if __name__ == "__main__":
    main()
