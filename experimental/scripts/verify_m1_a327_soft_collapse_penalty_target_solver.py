#!/usr/bin/env python3
"""Verifier for the M1 a=327 soft collapse-penalty target solver packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")
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
    "HIGH_CAPACITY_DEGENERATE",
    "SOFT_SPLIT_CAPACITY_LOSS",
    "SOFT_SPLIT_LOW_RESCHEDULE",
    "HIGH_CAPACITY_UNSCHEDULED",
    "PROXY_A327_COLLAPSE_REDUCED",
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
    require(record["source_commit"] == "0fb00ee", "wrong source commit")
    require(record["construction_mode"] == "soft_collapse_penalty_target_solver", "wrong mode")
    require(record["baseline"]["hard_split_best_capacity"] == 162, "wrong hard-split baseline")
    require(record["baseline"]["old_proxy_best_max_min"] == 329, "wrong old proxy baseline")
    require(record["baseline"]["known_collapse_class"] == [[1, 3, 4, 5, 6, 7], [2]], "wrong collapse class")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    search = record["soft_collapse_search"]
    expected_systems = (
        search["base_systems"]
        * len(search["row_budgets"])
        * len(search["lambda_values"])
        * len(search["selection_objectives"])
    )
    require(search["systems_tested"] == expected_systems, "bad systems count")
    require(search["systems_tested"] > 0, "empty search")
    require(search["codeword_tuple_samples"] == search["systems_tested"] * search["samples_per_system"], "bad sample count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure mode")
    require(record["retained_count"] == len(record["retained_results"]) > 0, "bad retained count")

    retained_proxy_systems = 0
    retained_reduced_systems = 0
    for row in record["retained_results"]:
        require(row["rank"] + row["nullity"] == 1536, "bad rank/nullity")
        require(row["sample_count"] == search["samples_per_system"], "bad row sample count")
        for sample in row["retained_sample_results"]:
            require(sample["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {sample['failure_mode']}")
            if sample["status"] == "PROXY_A327_ASSIGNMENT":
                require(sample["assignment"] is not None, "proxy assignment missing")
                require(sample["assignment"]["exact_max_min"] >= TARGET_AGREEMENT, "proxy assignment below target")
        retained_proxy_systems += int(row["proxy_candidate_count"] > 0)
        retained_reduced_systems += int(row["collapse_reduced_proxy_candidate_count"] > 0)

    require(search["proxy_candidates"] >= retained_proxy_systems, "retained proxy count exceeds global")
    require(search["collapse_reduced_proxy_candidates"] >= retained_reduced_systems, "retained reduced count exceeds global")
    require(record["proof_status"] in {"CANDIDATE", "TESTED_TARGET_SYSTEMS_NO_A327"}, "bad proof status")
    if record["proof_status"] == "TESTED_TARGET_SYSTEMS_NO_A327":
        require(search["collapse_reduced_proxy_candidates"] == 0, "negative status with reduced proxy candidate")
    if search["collapse_reduced_proxy_candidates"] > 0:
        require(record["exact_audit"]["triggered"] is True, "candidate should trigger exact audit flag")

    return {
        "status": "PASS",
        "systems_tested": search["systems_tested"],
        "codeword_tuple_samples": search["codeword_tuple_samples"],
        "proxy_candidates": search["proxy_candidates"],
        "collapse_reduced_proxy_candidates": search["collapse_reduced_proxy_candidates"],
        "best_proxy_max_min": search["best_proxy_max_min"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "best_six_class_dominance": search["best_six_class_dominance"],
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
            "PASS: M1 a=327 soft collapse-penalty target solver "
            f"({result['systems_tested']} systems, proxy_candidates={result['proxy_candidates']})"
        )


if __name__ == "__main__":
    main()
