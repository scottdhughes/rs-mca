#!/usr/bin/env python3
"""Verifier for the M1 a=327 witness-7 pair Hall repair stage-2 packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_witness7_pair_hall_repair_stage2.json")
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
    "PAIR7_STAGE2_NOT_REPAIRED",
    "PAIR7_STAGE2_COLLAPSE_RETURNS",
    "PAIR7_STAGE2_CAPACITY_LOSS",
    "PAIR7_STAGE2_LOW_RESCHEDULE",
    "PAIR7_STAGE2_UNSCHEDULED",
    "PAIR7_STAGE2_PROXY_CANDIDATE",
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
    require(record["source_commit"] == "8669680", "wrong source commit")
    require(record["construction_mode"] == "witness7_pair_hall_repair_stage2", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["proxy_max_min"] == 315, "wrong baseline proxy max-min")
    require(baseline["capacity"] == 455, "wrong baseline capacity")
    require(baseline["pair_B_values"] == [631, 631, 631, 631, 631], "wrong baseline pair values")
    require(baseline["pair_deficit_to_654"] == [23, 23, 23, 23, 23], "wrong baseline deficits")
    require(baseline["added_six_class_dominance"] == 0, "wrong baseline added dominance")

    search = record["stage2_search"]
    retained = record["retained_results"]
    expected_systems = (
        search["base_systems"]
        * len(search["repair_budgets"])
        * len(search["repair_families"])
    )
    require(search["systems_tested"] == expected_systems, "bad system count")
    require(search["samples_tested"] == search["systems_tested"] * 16, "bad sample count")
    require(record["retained_count"] == len(retained) > 0, "bad retained count")
    require(len(search["base_summaries"]) == search["base_systems"], "bad base summary count")

    failure_total = sum(search["failure_mode_counts"].values())
    require(failure_total == search["samples_tested"], "bad failure counts")

    candidate_count = 0
    for row in retained:
        require(row["repair_budget"] in search["repair_budgets"], "unexpected repair budget")
        require(row["repair_family"] in search["repair_families"], "unexpected repair family")
        require(row["rank"] + row["nullity"] == 1536, "bad rank/nullity ledger")
        require(row["target_row_count"] <= 640, "target row budget exceeded")
        require(row["repair_row_count"] <= row["repair_budget"], "repair row budget exceeded")
        for sample in row["retained_sample_results"]:
            require(sample["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {sample['failure_mode']}")
            require(len(sample["pair7_B_values"]) >= 5, "bad pair7 B vector")
            require(len(sample["pair7_deficits_to_654"]) >= 5, "bad pair7 deficit vector")
            require(sample["min_pair7_B"] == min(sample["pair7_B_values"]), "bad min pair B")
            require(sample["pair7_hall_bound"] == sample["min_pair7_B"] // 2, "bad pair Hall bound")
            require(len(sample["old_three_subset_B_values"]) == 3, "bad old three-subset vector")
            if sample["proxy_max_min"] is not None:
                require(min(sample["agreement_vector"]) == sample["proxy_max_min"], "bad agreement vector")
            if sample["failure_mode"] == "PAIR7_STAGE2_PROXY_CANDIDATE":
                candidate_count += 1
                require(sample["proxy_max_min"] >= TARGET_AGREEMENT, "candidate below target")
                require(sample["min_pair7_B"] >= 2 * TARGET_AGREEMENT, "candidate pair Hall not repaired")
                require(sample["six_class_dominance_added_by_repair"] <= 20, "candidate added collapse too high")

    require(record["proof_status"] in {"CANDIDATE", "TESTED_PAIR7_STAGE2_NO_A327"}, "bad status")
    if record["proof_status"] == "TESTED_PAIR7_STAGE2_NO_A327":
        require(candidate_count == 0, "negative status with candidate")
    if search["proxy_candidates"] > 0:
        require(record["exact_audit"]["triggered"] is True, "candidate should trigger exact audit")

    return {
        "status": "PASS",
        "systems_tested": search["systems_tested"],
        "samples_tested": search["samples_tested"],
        "proxy_candidates": search["proxy_candidates"],
        "best_proxy_max_min": search["best_proxy_max_min"],
        "best_capacity": search["best_capacity"],
        "best_pair_B_values": search["best_pair_B_values"],
        "best_added_dominance": search["best_added_six_class_dominance"],
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
            "PASS: M1 a=327 witness-7 pair Hall repair stage 2 "
            f"({result['systems_tested']} systems)"
        )


if __name__ == "__main__":
    main()
