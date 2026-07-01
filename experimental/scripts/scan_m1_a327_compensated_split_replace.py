#!/usr/bin/env python3
"""Ledger scaffold for compensated split-and-replace search."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_capacity_slack_split_selector.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_compensated_split_replace.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "976d215"


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


def baseline(source: dict[str, Any]) -> dict[str, Any]:
    selector = source["split_selector"]
    return {
        "pre_split_pair_B_values": [1024, 577, 576, 1024, 1024],
        "pre_split_capacity": 384,
        "post_split_pair_B_values": selector["best_pair_B_values"],
        "post_split_capacity": selector["best_capacity_upper_bound"],
        "post_split_collapse_pattern": selector["best_collapse_pattern"],
        "split_gain_B27_B37": [
            selector["best_pair_B_values"][1] - 577,
            selector["best_pair_B_values"][2] - 576,
        ],
        "capacity_loss": 384 - selector["best_capacity_upper_bound"],
    }


def build_record(compensated_exchange: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    compensated_exchange = compensated_exchange or {
        "systems_tested": 0,
        "exchange_types": [],
        "exact_vectors_constructed": 0,
        "capacity_restored_vectors": 0,
        "pair27_37_improved_vectors": 0,
        "pair57_preserving_vectors": 0,
        "collapse_reduced_vectors": 0,
        "best_pair_B_values": None,
        "best_capacity_upper_bound": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_failure_mode": "COMP_SPLIT_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if compensated_exchange["best_failure_mode"] == "COMP_SPLIT_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif compensated_exchange["systems_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "compensated_split_replace",
        "baseline": baseline(source),
        "compensated_exchange": compensated_exchange,
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
