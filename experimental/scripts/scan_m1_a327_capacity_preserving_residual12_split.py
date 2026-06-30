#!/usr/bin/env python3
"""Ledger scaffold for capacity-preserving residual [1,2] split search."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_residual_12_split_pinned_nullspace.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_capacity_preserving_residual12_split.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "5105961"


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
    search = source["residual12_search"]
    return {
        "hard_split_vectors": search["exact_vectors_constructed"],
        "nondegenerate_vectors": search["nondegenerate_vectors"],
        "capacity_preserving_nondegenerate_vectors": search["capacity_preserving_nondegenerate_vectors"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "best_pair_B_values": search["best_pair_B_values"],
        "best_failure_mode": search["best_failure_mode"],
    }


def build_record(capacity_preserving_search: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    capacity_preserving_search = capacity_preserving_search or {
        "protected_rows": 0,
        "pin_sets_tested": 0,
        "nullspace_samples_tested": 0,
        "exact_vectors_constructed": 0,
        "d2_split_vectors": 0,
        "capacity_preserving_d2_split_vectors": 0,
        "low_collapse_capacity_preserving_d2_split_vectors": 0,
        "best_capacity_upper_bound": None,
        "best_pair_B_values": None,
        "best_exact_max_min": None,
        "best_failure_mode": "CAPACITY_PRESERVING_RESIDUAL12_SEARCH_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if capacity_preserving_search["best_failure_mode"] == "RESIDUAL12_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif capacity_preserving_search["pin_sets_tested"] or capacity_preserving_search["nullspace_samples_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "capacity_preserving_residual12_split",
        "baseline": baseline(source),
        "capacity_preserving_residual12_search": capacity_preserving_search,
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
