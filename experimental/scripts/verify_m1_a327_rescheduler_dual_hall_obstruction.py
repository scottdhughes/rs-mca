#!/usr/bin/env python3
"""Verifier for the M1 a=327 rescheduler dual/Hall obstruction audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_rescheduler_dual_hall_obstruction.json")
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
    "LOW_CAPACITY_SCREEN",
    "HALL_TIGHT",
    "HALL_GAP",
    "BALANCE_GAP",
    "UNKNOWN",
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
    require(record["source_commit"] == "758af1b", "wrong source commit")
    require(record["construction_mode"] == "rescheduler_dual_hall_obstruction", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    samples = record["samples"]
    require(record["samples_analyzed"] == len(samples) > 0, "bad sample count")
    require(record["raw_samples_replayed"] >= record["samples_analyzed"], "raw count below unique count")
    require(
        record["duplicate_value_class_samples"] == record["raw_samples_replayed"] - record["samples_analyzed"],
        "bad duplicate count",
    )
    require(len({sample["value_class_hash"] for sample in samples}) == len(samples), "duplicate value-class hashes retained")
    require(record["best_sample"] == samples[0], "best sample should be first sorted sample")
    source_total = sum(record["source_counts"].values())
    require(source_total == len(samples), "bad source counts")
    failure_total = sum(record["failure_mode_counts"].values())
    require(failure_total == len(samples), "bad failure counts")
    hall_tight_count = 0
    for sample in samples:
        require(sample["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {sample['failure_mode']}")
        require(sample["hall_bound"] <= sample["capacity_upper_bound"], "Hall bound exceeds capacity upper bound")
        require(sample["deficit_to_327"] >= 0, "unexpected nonpositive max deficit convention")
        require(len(sample["tight_subsets"]) > 0, "missing tight subset")
        for subset in sample["tight_subsets"]:
            require(subset["hall_bound"] == sample["hall_bound"], "non-tight subset listed")
            require(subset["subset_size"] == len(subset["subset"]), "bad subset size")
            require(subset["deficit_to_327"] == subset["subset_size"] * TARGET_AGREEMENT - subset["B_U"], "bad deficit")
        if sample["rescheduler_max_min"] is not None:
            require(sample["rescheduler_max_min"] <= sample["hall_bound"], "rescheduler exceeds Hall bound")
            require(sample["agreement_vector"] is not None and min(sample["agreement_vector"]) == sample["rescheduler_max_min"], "bad agreement vector")
        if sample["hall_bound_matches_rescheduler"]:
            hall_tight_count += 1
            require(sample["failure_mode"] == "HALL_TIGHT", "tight sample should be classified HALL_TIGHT")
    require(record["hall_tight_count"] == hall_tight_count, "bad tight count")
    require(record["proof_status"] in {"AUDIT", "RESCHEDULER_OBSTRUCTION_CERTIFICATE"}, "bad proof status")
    if hall_tight_count:
        require(record["proof_status"] == "RESCHEDULER_OBSTRUCTION_CERTIFICATE", "tight certificate should set proof status")
    return {
        "status": "PASS",
        "samples_analyzed": len(samples),
        "raw_samples_replayed": record["raw_samples_replayed"],
        "duplicate_value_class_samples": record["duplicate_value_class_samples"],
        "source_counts": record["source_counts"],
        "failure_mode_counts": record["failure_mode_counts"],
        "hall_tight_count": hall_tight_count,
        "best_source": record["best_sample"]["source"],
        "best_capacity_upper_bound": record["best_sample"]["capacity_upper_bound"],
        "best_rescheduler_max_min": record["best_sample"]["rescheduler_max_min"],
        "best_hall_bound": record["best_sample"]["hall_bound"],
        "best_failure_mode": record["best_sample"]["failure_mode"],
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
            "PASS: M1 a=327 rescheduler dual/Hall obstruction audit "
            f"({result['samples_analyzed']} samples)"
        )


if __name__ == "__main__":
    main()
