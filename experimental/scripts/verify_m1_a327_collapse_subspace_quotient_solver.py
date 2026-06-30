#!/usr/bin/env python3
"""Verifier for the M1 a=327 collapse-subspace quotient solver packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_collapse_subspace_quotient_solver.json")
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
    "COLLAPSE_ONLY_HIGH_CAPACITY",
    "QUOTIENT_DIRECTION_CAPACITY_LOSS",
    "QUOTIENT_DIRECTION_LOW_RESCHEDULE",
    "QUOTIENT_DIRECTION_HIGH_CAPACITY_DEGENERATE",
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
    require(record["source_commit"] == "f266cf1", "wrong source commit")
    require(record["collapse_class"] == [1, 3, 4, 5, 6, 7], "wrong collapse class")
    require(record["construction_mode"] == "collapse_subspace_quotient_solver", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    systems = record["systems"]
    require(record["proxy_systems"]["systems_tested"] == len(systems) > 0, "bad system count")
    sample_total = 0
    candidate_count = 0
    for row in systems:
        require(row["proxy_rank"] + row["proxy_nullity"] == 1536, "bad proxy rank/nullity")
        require(row["quotient_dimension"] == row["proxy_nullity"] - row["collapse_subspace_dimension"], "bad quotient dimension")
        require(row["collapse_subspace_dimension"] >= 0, "negative collapse dimension")
        require(row["quotient_dimension"] >= 0, "negative quotient dimension")
        require(row["samples_tested"] > 0, "no quotient samples")
        sample_total += row["samples_tested"]
        for block in ["D_2", "D_3", "D_4", "D_5", "D_6", "D_7"]:
            require(block in row["projection_rank_by_block"], f"missing projection block {block}")
        for sample in row["sample_results"]:
            require(sample["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {sample['failure_mode']}")
            if sample["failure_mode"] == "PROXY_A327_COLLAPSE_REDUCED":
                candidate_count += 1
                require(sample["assignment"]["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(record["collapse_quotient"]["samples_tested"] == sample_total, "bad sample total")
    require(record["proof_status"] in {"CANDIDATE", "TESTED_QUOTIENT_DIRECTIONS_NO_A327"}, "bad proof status")
    if record["proof_status"] == "TESTED_QUOTIENT_DIRECTIONS_NO_A327":
        require(candidate_count == 0, "negative status with retained candidate")
    return {
        "status": "PASS",
        "systems_tested": len(systems),
        "samples_tested": sample_total,
        "collapse_subspace_dimensions": record["collapse_quotient"]["collapse_subspace_dimensions"],
        "quotient_dimensions": record["collapse_quotient"]["quotient_dimensions"],
        "best_capacity_upper_bound": record["collapse_quotient"]["best_capacity_upper_bound"],
        "best_proxy_max_min": record["collapse_quotient"]["best_proxy_max_min"],
        "best_six_class_dominance": record["collapse_quotient"]["best_six_class_dominance"],
        "best_failure_mode": record["collapse_quotient"]["best_failure_mode"],
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
            "PASS: M1 a=327 collapse-subspace quotient solver "
            f"({result['systems_tested']} systems, samples={result['samples_tested']})"
        )


if __name__ == "__main__":
    main()
