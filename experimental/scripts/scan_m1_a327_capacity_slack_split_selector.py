#!/usr/bin/env python3
"""Ledger scaffold for capacity-slack split selection."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_capacity_skeleton_protected_split_placement.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_capacity_slack_split_selector.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "395e7e0"


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
    search = source["capacity_skeleton_search"]
    return {
        "best_pair_B_values": search["best_pair_B_values"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "best_collapse_pattern": search["best_collapse_pattern"],
        "failure_counts": search["failure_mode_counts"],
    }


def build_record(
    capacity_slack_ledger: dict[str, Any] | None = None,
    split_selector: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    capacity_slack_ledger = capacity_slack_ledger or {
        "coordinates": 0,
        "capacity_critical_count": None,
        "pair57_critical_count": None,
        "split_safe_count": None,
        "top_slack_fibers": [],
        "coordinate_rows": [],
    }
    split_selector = split_selector or {
        "systems_tested": 0,
        "split_rows_tested": 0,
        "exact_vectors_constructed": 0,
        "capacity_preserving_vectors": 0,
        "pair57_preserving_vectors": 0,
        "pair27_37_improved_vectors": 0,
        "collapse_reduced_vectors": 0,
        "best_pair_B_values": None,
        "best_capacity_upper_bound": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_failure_mode": "CAPACITY_SLACK_SELECTOR_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if split_selector["best_failure_mode"] == "SPLIT_SELECTOR_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif split_selector["systems_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "capacity_slack_split_selector",
        "baseline": baseline(source),
        "capacity_slack_ledger": capacity_slack_ledger,
        "split_selector": split_selector,
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
