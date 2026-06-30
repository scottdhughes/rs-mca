#!/usr/bin/env python3
"""Ledger scaffold for protected-exchange nondegenerate exact lifting."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_protected_exchange_exact_audit.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_protected_exchange_nondegenerate_lift.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "a2d31ee"


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
    exact = source["exact_audit"]
    return {
        "proxy_candidates_tested": exact["candidates_tested"],
        "exact_vectors_constructed": exact["exact_vectors_constructed"],
        "nondegenerate_vectors": exact["nondegenerate_vectors"],
        "best_exact_max_min": exact["best_exact_max_min"],
        "best_capacity_upper_bound": exact["best_capacity_upper_bound"],
        "best_pair_B_values": exact["best_pair_B_values"],
        "best_failure_mode": exact["best_failure_mode"],
    }


def build_record(nondegenerate_lift: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    nondegenerate_lift = nondegenerate_lift or {
        "pin_sets_tested": 0,
        "exact_vectors_constructed": 0,
        "nondegenerate_vectors": 0,
        "capacity_preserving_nondegenerate_vectors": 0,
        "best_exact_max_min": None,
        "best_capacity_upper_bound": None,
        "best_pair_B_values": None,
        "best_failure_mode": "EXACT_NONDEGENERATE_LIFT_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if nondegenerate_lift["best_failure_mode"] == "EXACT_CANDIDATE_A327":
        proof_status = "PROOF_RECORD"
    elif nondegenerate_lift["pin_sets_tested"] > 0:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "protected_exchange_nondegenerate_lift",
        "exact_audit_baseline": baseline(source),
        "nondegenerate_lift": nondegenerate_lift,
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
