#!/usr/bin/env python3
"""Ledger scaffold for residual [1,2] split and pinned-nullspace audit."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_protected_exchange_nondegenerate_lift.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_residual_12_split_pinned_nullspace.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "024481e"


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
    lift = source["nondegenerate_lift"]
    strongest = None
    for result in lift["results"]:
        for row in result["retained_pin_results"]:
            if row.get("pin_family") == "anchor_split_34567":
                strongest = row
                break
        if strongest:
            break
    return {
        "best_capacity_upper_bound": lift["best_capacity_upper_bound"],
        "best_pair_B_values": lift["best_pair_B_values"],
        "best_failure_mode": lift["best_failure_mode"],
        "strongest_split_remaining_collapse": None
        if strongest is None
        else strongest.get("degenerate_classes"),
        "strongest_split_capacity_upper_bound": None
        if strongest is None
        else strongest.get("capacity_upper_bound"),
        "strongest_split_pair_B_values": None
        if strongest is None
        else strongest.get("pair_B_values"),
    }


def build_record(residual12_search: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    residual12_search = residual12_search or {
        "pin_sets_tested": 0,
        "nullspace_samples_tested": 0,
        "exact_vectors_constructed": 0,
        "nondegenerate_vectors": 0,
        "capacity_preserving_nondegenerate_vectors": 0,
        "best_exact_max_min": None,
        "best_capacity_upper_bound": None,
        "best_pair_B_values": None,
        "best_degenerate_classes": None,
        "best_failure_mode": "RESIDUAL12_SEARCH_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if residual12_search["best_failure_mode"] == "RESIDUAL12_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif residual12_search["pin_sets_tested"] or residual12_search["nullspace_samples_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "residual_12_split_pinned_nullspace",
        "baseline": baseline(source),
        "residual12_search": residual12_search,
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
