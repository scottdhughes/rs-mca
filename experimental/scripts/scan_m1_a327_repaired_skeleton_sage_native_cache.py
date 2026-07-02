#!/usr/bin/env python3
"""Ledger scaffold for Sage-native repaired-skeleton cache."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any


PARENT_CACHE_PATH = Path("experimental/data/m1_a327_repaired_skeleton_prepared_matrix_cache.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_repaired_skeleton_sage_native_cache.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "c3a0f82"


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


def hash_payload(payload: object) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def base_state(parent: dict[str, Any]) -> dict[str, Any]:
    prepared = parent["prepared_state"]
    return {
        "capacity": prepared["base_capacity"],
        "pair_B_values": prepared["base_pair_B_values"],
        "collapse_pattern": prepared["base_collapse_pattern"],
    }


def failed_split(parent: dict[str, Any]) -> dict[str, Any]:
    prepared = parent["prepared_state"]
    source = prepared["base_pair_B_values"]
    failed = prepared["failed_split_pair_B_values"]
    return {
        "split_family": "split_4_from_157",
        "capacity": prepared["failed_split_capacity"],
        "pair_B_values": failed,
        "collapse_pattern": [[1, 5, 6, 7], [4], [3], [2]],
        "damage": {
            "capacity": prepared["failed_split_capacity"] - prepared["base_capacity"],
            "B27": failed[1] - source[1],
            "B37": failed[2] - source[2],
            "B47": failed[3] - source[3],
            "B57": failed[4] - source[4],
        },
    }


def build_record(
    prepared_state: dict[str, Any] | None = None,
    append_test: dict[str, Any] | None = None,
) -> dict[str, Any]:
    parent = load_json(PARENT_CACHE_PATH)
    parent_state = parent["prepared_state"]
    prepared_state = prepared_state or {
        "cache_type": "RECONSTRUCTION_ONLY",
        "matrix_shape": parent_state["matrix_shape"],
        "rank": parent_state["rank"],
        "nullity": parent_state["nullity"],
        "fixed_specs_count": parent_state["fixed_specs_count"],
        "pivot_columns_hash": None,
        "free_columns_hash": None,
        "independent_rows_hash": None,
        "sage_cache_hash": None,
        "sage_cache_path": None,
    }
    append_test = append_test or {
        "run": False,
        "timeout": False,
        "status": "NOT_RUN",
    }
    proof_status = "PARTIAL"
    if prepared_state["cache_type"] in {"SAGE_NATIVE", "PIVOT_FREE", "ROW_SUBSET"} and append_test["status"] == "CACHE_SMALL_APPEND_PASS":
        proof_status = "EXACT_STATE_CACHE"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "repaired_skeleton_sage_native_cache",
        "base_repaired_skeleton": base_state(parent),
        "failed_split": failed_split(parent),
        "prepared_state": prepared_state,
        "append_test": append_test,
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
