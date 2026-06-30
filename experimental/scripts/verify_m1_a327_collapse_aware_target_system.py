#!/usr/bin/env python3
"""Verifier for the M1 a=327 collapse-aware target-system packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_collapse_aware_target_system.json")
TARGET_AGREEMENT = 327
COLLAPSE_CLASS = [1, 3, 4, 5, 6, 7]
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "COLLAPSE_CLASS_PERSISTS",
    "SPLIT_DESTROYS_CAPACITY",
    "SPLIT_LOW_RESCHEDULE",
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
    require(record["source_commit"] == "3d12ee1", "wrong source commit")
    require(record["known_collapse_class"] == COLLAPSE_CLASS, "wrong collapse class")
    require(record["construction_mode"] == "collapse_aware_target_system", "wrong mode")
    require(record["baseline"]["best_degenerate_capacity"] == 374, "wrong baseline capacity")
    require(record["baseline"]["collapse_pattern"] == [[1, 3, 4, 5, 6, 7], [2]], "wrong collapse pattern")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    search = record["collapse_aware_search"]
    require(search["systems_tested"] == len(record["systems"]) > 0, "bad systems count")
    require(search["split_rows_inserted"], "missing split budgets")
    require(search["split_partitions_tested"], "missing partitions")
    proxy_candidates = 0
    best_floor = -1
    for system in record["systems"]:
        require(system["system_status"] in {"SAMPLED", "LOW_NULLITY"}, "bad system status")
        if system["system_status"] == "LOW_NULLITY":
            continue
        require(system["rank"] is not None and system["nullity"] is not None, "missing rank/nullity")
        require(system["rank"] + system["nullity"] == 1536, "bad rank/nullity")
        for sample in system["samples"]:
            require(sample["status"] in ALLOWED_FAILURES, f"bad sample status {sample['status']}")
            if sample["assignment"] is not None:
                best_floor = max(best_floor, int(sample["assignment"]["exact_max_min"]))
            if sample["status"] == "PROXY_A327_COLLAPSE_REDUCED":
                proxy_candidates += 1
                require(sample["assignment"]["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(proxy_candidates == search["proxy_candidates"], "proxy candidate mismatch")
    require(record["proof_status"] in {"CANDIDATE", "EXACT_EXTRACTION_NO_A327"}, "bad proof status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(proxy_candidates == 0, "negative status with proxy candidate")
    return {
        "status": "PASS",
        "systems_tested": search["systems_tested"],
        "proxy_candidates": search["proxy_candidates"],
        "best_proxy_max_min": search["best_proxy_max_min"],
        "best_proxy_capacity_upper_bound": search["best_proxy_capacity_upper_bound"],
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
            "PASS: M1 a=327 collapse-aware target system "
            f"({result['systems_tested']} systems, proxy_candidates={result['proxy_candidates']})"
        )


if __name__ == "__main__":
    main()
