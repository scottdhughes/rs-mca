#!/usr/bin/env python3
"""Verifier for Sage-native repaired-skeleton cache."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_sage_native_cache.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_CACHE_TYPES = {"SAGE_NATIVE", "PIVOT_FREE", "ROW_SUBSET", "RECONSTRUCTION_ONLY"}
ALLOWED_APPEND_STATUSES = {
    "NOT_RUN",
    "CACHE_SMALL_APPEND_PASS",
    "CACHE_SMALL_APPEND_TIMEOUT",
    "CACHE_REPLAY_TIMEOUT",
    "CACHE_UNSERIALIZABLE",
    "CACHE_PIVOT_REUSE_FAILS",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_hash(value: Any, name: str) -> None:
    require(isinstance(value, str) and len(value) == 64, f"bad hash for {name}")


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "c3a0f82", "wrong source commit")
    require(record["construction_mode"] == "repaired_skeleton_sage_native_cache", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    base = record["base_repaired_skeleton"]
    require(base["capacity"] == 333, "wrong base capacity")
    require(base["pair_B_values"] == [1024, 657, 656, 1024, 1024], "wrong base pairs")
    require(base["collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong base collapse")

    failed = record["failed_split"]
    require(failed["capacity"] == 315, "wrong failed split capacity")
    require(failed["pair_B_values"] == [1024, 593, 592, 512, 1024], "wrong failed pairs")
    require(failed["damage"] == {"capacity": -18, "B27": -64, "B37": -64, "B47": -512, "B57": 0}, "wrong damage")

    state = record["prepared_state"]
    require(state["cache_type"] in ALLOWED_CACHE_TYPES, "bad cache type")
    require(state["matrix_shape"] == [354, 1536], "wrong matrix shape")
    require(state["rank"] == 354, "wrong rank")
    require(state["nullity"] == 1182, "wrong nullity")
    require(state["fixed_specs_count"] == 129, "wrong fixed specs")
    if state["cache_type"] == "SAGE_NATIVE":
        require(state["sage_cache_path"], "missing Sage cache path")
        require_hash(state["sage_cache_hash"], "sage_cache_hash")
        require_hash(state["pivot_columns_hash"], "pivot_columns_hash")
        require_hash(state["free_columns_hash"], "free_columns_hash")
        require_hash(state["independent_rows_hash"], "independent_rows_hash")

    append = record["append_test"]
    require(append["status"] in ALLOWED_APPEND_STATUSES, "bad append status")
    require(isinstance(append["run"], bool), "bad append run flag")
    require(isinstance(append["timeout"], bool), "bad append timeout flag")
    if append["status"] == "CACHE_SMALL_APPEND_PASS":
        require(append["run"] is True, "append pass but not run")
        require(append["timeout"] is False, "append pass but timeout")
        require(append["vector_constructed"] is True, "append pass without vector")
        require(append["capacity"] is not None, "missing append capacity")
        require(append["pair_B_values"] is not None, "missing append pairs")
    if record["proof_status"] == "EXACT_STATE_CACHE":
        require(state["cache_type"] != "RECONSTRUCTION_ONLY", "exact cache cannot be reconstruction-only")
        require(append["status"] == "CACHE_SMALL_APPEND_PASS", "exact cache needs append pass")
    if record["proof_status"] == "PARTIAL":
        require(append["status"] != "CACHE_SMALL_APPEND_PASS" or state["cache_type"] == "RECONSTRUCTION_ONLY", "unexpected partial")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "cache_type": state["cache_type"],
        "matrix_shape": state["matrix_shape"],
        "rank": state["rank"],
        "nullity": state["nullity"],
        "append_status": append["status"],
        "append_timeout": append["timeout"],
        "vector_constructed": append.get("vector_constructed", False),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 repaired-skeleton Sage-native cache")


if __name__ == "__main__":
    main()
