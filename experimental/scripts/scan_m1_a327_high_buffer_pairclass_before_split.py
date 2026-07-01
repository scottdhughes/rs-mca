#!/usr/bin/env python3
"""Ledger scaffold for high-buffer pairclass before split."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_compensated_split_replace.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_high_buffer_pairclass_before_split.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "0f2655a"


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


def local_basin_baseline(source: dict[str, Any]) -> dict[str, Any]:
    baseline = source["baseline"]
    exchange = source["compensated_exchange"]
    return {
        "pre_split_pair_B_values": baseline["pre_split_pair_B_values"],
        "pre_split_capacity": baseline["pre_split_capacity"],
        "post_split_pair_B_values": exchange["best_pair_B_values"],
        "post_split_capacity": exchange["best_capacity_upper_bound"],
        "capacity_loss": baseline["capacity_loss"],
        "best_failure": exchange["best_failure_mode"],
    }


def build_record(high_buffer_search: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    high_buffer_search = high_buffer_search or {
        "systems_tested": 0,
        "pre_split_vectors": 0,
        "post_split_vectors": 0,
        "pre_split_capacity_target": 420,
        "capacity_buffer_vectors": 0,
        "post_split_capacity_preserving_vectors": 0,
        "best_pre_split_capacity": None,
        "best_post_split_capacity": None,
        "best_pair_B_values": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_failure_mode": "HIGH_BUFFER_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if high_buffer_search["best_failure_mode"] == "HIGH_BUFFER_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif high_buffer_search["systems_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "high_buffer_pairclass_before_split",
        "local_basin_baseline": local_basin_baseline(source),
        "high_buffer_search": high_buffer_search,
        "proof_status": proof_status,
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
