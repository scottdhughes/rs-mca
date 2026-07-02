#!/usr/bin/env python3
"""Ledger scaffold for cached compensated repaired-skeleton split v2."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


CACHE_DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_sage_native_cache.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SOURCE_COMMIT = "c181b13"
SYSTEMS_PLANNED = 3 * 3 * 5


def jsonable(payload: object) -> object:
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def baseline(cache: dict[str, Any]) -> dict[str, Any]:
    base = cache["base_repaired_skeleton"]
    return {
        "capacity": base["capacity"],
        "pair_B_values": base["pair_B_values"],
        "collapse_pattern": base["collapse_pattern"],
    }


def failed_split(cache: dict[str, Any]) -> dict[str, Any]:
    failed = cache["failed_split"]
    return {
        "split_family": failed["split_family"],
        "capacity": failed["capacity"],
        "pair_B_values": failed["pair_B_values"],
        "collapse_pattern": failed["collapse_pattern"],
        "damage": failed["damage"],
    }


def cache_summary(cache: dict[str, Any]) -> dict[str, Any]:
    state = cache["prepared_state"]
    append = cache["append_test"]
    return {
        "cache_type": state["cache_type"],
        "cache_artifact": state["sage_cache_path"],
        "cache_hash": state["sage_cache_hash"],
        "append_status": append["status"],
    }


def empty_grid() -> dict[str, Any]:
    return {
        "systems_planned": SYSTEMS_PLANNED,
        "systems_tested": 0,
        "timeouts": 0,
        "exact_vectors_constructed": 0,
        "capacity_preserving_vectors": 0,
        "pair_guard_preserving_vectors": 0,
        "partial_split_vectors": 0,
        "nondegenerate_vectors": 0,
        "best_capacity": None,
        "best_pair_B_values": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_agreement_vector": None,
        "best_failure_mode": None,
        "results": [],
    }


def proof_status(grid: dict[str, Any]) -> str:
    if grid.get("best_failure_mode") == "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE":
        return "PROOF_RECORD"
    if grid.get("systems_tested", 0) < grid.get("systems_planned", SYSTEMS_PLANNED):
        return "PARTIAL"
    if grid.get("systems_tested", 0) and grid.get("exact_vectors_constructed", 0):
        return "EXACT_EXTRACTION_NO_A327"
    return "PARTIAL"


def build_record(compensated_grid: dict[str, Any] | None = None) -> dict[str, Any]:
    cache = load_json(CACHE_DATA_PATH)
    compensated_grid = compensated_grid or empty_grid()
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "compensated_repaired_skeleton_split_v2",
        "cache": cache_summary(cache),
        "baseline": baseline(cache),
        "failed_split": failed_split(cache),
        "compensated_grid": compensated_grid,
        "proof_status": proof_status(compensated_grid),
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
