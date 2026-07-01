#!/usr/bin/env python3
"""Ledger scaffold for scalable pair-class creation with [1,4,5,6,7] splits."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_pair27_37_class_creation_scalable.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_scalable_pairclass_with_14567_split.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SOURCE_COMMIT = "e99acf6"


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
    search = source["scalable_class_creation"]
    pair_values = search["best_pair_B_values"]
    return {
        "best_pair_B_values": pair_values,
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "collapse_pattern": [[1, 4, 5, 6, 7], [3], [2]],
        "pair27_deficit_to_654": PAIR_TARGET - pair_values[1],
        "pair37_deficit_to_654": PAIR_TARGET - pair_values[2],
    }


def build_record(pairclass_split_search: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    pairclass_split_search = pairclass_split_search or {
        "exact_field": "GF(17^32)",
        "systems_tested": 0,
        "pair_row_extensions": [32, 64, 96],
        "split_families": [],
        "exact_vectors_constructed": 0,
        "capacity_preserving_vectors": 0,
        "pair_values_improved_vectors": 0,
        "collapse_reduced_vectors": 0,
        "best_pair_B_values": None,
        "best_capacity_upper_bound": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_failure_mode": "PAIRCLASS_SPLIT_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if pairclass_split_search["best_failure_mode"] == "PAIRCLASS_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif pairclass_split_search["systems_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "scalable_pairclass_with_14567_split",
        "baseline": baseline(source),
        "pairclass_split_search": pairclass_split_search,
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
