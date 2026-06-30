#!/usr/bin/env python3
"""Verifier for the M1 a=327 collapse-constrained Hall repair packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_collapse_constrained_hall_repair.json")
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
    "HALL_REPAIR_COLLAPSE_RETURNS",
    "HALL_REPAIR_BLOCKED_BY_CAP",
    "HALL_REPAIR_CAPACITY_LOSS",
    "HALL_REPAIR_LOW_RESCHEDULE",
    "HALL_REPAIR_UNSCHEDULED",
    "HALL_CONSTRAINED_PROXY_CANDIDATE",
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
    require(record["source_commit"] == "4d5ce7f", "wrong source commit")
    require(record["construction_mode"] == "collapse_constrained_hall_repair", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["hall_baseline"]
    require(baseline["best_hall_bound"] == 332, "wrong baseline Hall bound")
    require(baseline["best_proxy_max_min"] == 332, "wrong baseline proxy max-min")
    require(baseline["six_class_dominance"] == 359, "wrong baseline dominance")
    require(baseline["failure_mode"] == "HALL_REPAIR_COLLAPSE_RETURNS", "wrong baseline failure")

    search = record["collapse_constrained_search"]
    retained = record["retained_results"]
    expected = (
        len(search["dominance_caps"])
        * len(search["repair_row_budgets"])
        * len(search["selection_objectives"])
    )
    require(search["systems_attempted"] == expected, "bad attempted system count")
    require(search["systems_tested"] + search["selection_failures"] == expected, "bad tested/failure count")
    require(record["retained_count"] == len(retained) > 0, "bad retained count")
    require(len(search["pareto_frontier"]) == len(search["dominance_caps"]), "bad frontier length")

    failure_total = sum(search["failure_mode_counts"].values())
    require(failure_total == search["samples_tested"], "bad aggregate failure counts")

    candidate_count = 0
    for row in retained:
        require(row["dominance_cap"] in search["dominance_caps"], "unexpected dominance cap")
        require(row["repair_row_budget"] in search["repair_row_budgets"], "unexpected repair budget")
        require(row["selection_objective"] in search["selection_objectives"], "unexpected objective")
        require(row["rank"] + row["nullity"] == 1536, "bad rank/nullity ledger")
        require(row["target_row_count"] <= 640, "row budget exceeded")
        require(
            row["target_six_like_coordinate_count"] <= row["target_six_like_coordinate_cap"],
            "target six-like coordinate cap exceeded",
        )
        for sample in row["retained_sample_results"]:
            require(sample["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {sample['failure_mode']}")
            require(len(sample["tight_subset_B"]) == 3, "bad tight-subset vector")
            require(len(sample["tight_subset_deficits_to_981"]) == 3, "bad deficit vector")
            if sample["dominance_cap_satisfied"]:
                require(sample["six_class_dominance"] <= sample["dominance_cap"], "bad cap flag")
            if sample["proxy_max_min"] is not None:
                require(min(sample["agreement_vector"]) == sample["proxy_max_min"], "bad agreement vector")
            if sample["failure_mode"] == "HALL_CONSTRAINED_PROXY_CANDIDATE":
                candidate_count += 1
                require(sample["proxy_max_min"] >= TARGET_AGREEMENT, "candidate below target")
                require(sample["six_class_dominance"] <= 250, "candidate dominance too high")

    for point in search["pareto_frontier"]:
        require(point["dominance_cap"] in search["dominance_caps"], "bad frontier cap")
        require(point["best_failure_mode"] in ALLOWED_FAILURES, "bad frontier failure")
        if point["best_proxy_max_min"] is not None:
            require(point["best_proxy_max_min"] >= 0, "bad frontier proxy max-min")

    rejected = search["best_rejected_collapse_return"]
    if rejected is not None:
        require(rejected["failure_mode"] == "HALL_REPAIR_COLLAPSE_RETURNS", "bad rejected sample")
        require(not rejected["dominance_cap_satisfied"], "rejected sample unexpectedly satisfies cap")

    require(record["proof_status"] in {"CANDIDATE", "TESTED_CONSTRAINED_HALL_REPAIR_NO_A327"}, "bad status")
    if record["proof_status"] == "TESTED_CONSTRAINED_HALL_REPAIR_NO_A327":
        require(candidate_count == 0, "negative status with candidate")
    if search["proxy_candidates"] > 0:
        require(record["exact_audit"]["triggered"] is True, "candidate should trigger exact audit")

    return {
        "status": "PASS",
        "systems_tested": search["systems_tested"],
        "samples_tested": search["samples_tested"],
        "proxy_candidates": search["proxy_candidates"],
        "best_hall_bound_under_low_dominance": search["best_hall_bound_under_low_dominance"],
        "best_failure_mode": search["best_failure_mode"],
        "best_rejected_proxy_max_min": None
        if rejected is None
        else rejected["proxy_max_min"],
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
            "PASS: M1 a=327 collapse-constrained Hall repair "
            f"({result['systems_tested']} systems)"
        )


if __name__ == "__main__":
    main()
