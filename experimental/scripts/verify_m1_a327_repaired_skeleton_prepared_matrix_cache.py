#!/usr/bin/env python3
"""Verifier for the repaired-skeleton prepared matrix cache ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_prepared_matrix_cache.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_CACHE_TYPES = {"PIVOT_FREE", "ROW_SUBSET", "SAGE_NATIVE", "RECONSTRUCTION_ONLY"}
ALLOWED_LABELS = {
    "CACHE_REPLAY_PASS",
    "CACHE_REPLAY_TIMEOUT",
    "CACHE_UNSERIALIZABLE",
    "CACHE_PIVOT_REUSE_FAILS",
    "CACHE_SMALL_APPEND_PASS",
    "CACHE_SMALL_APPEND_TIMEOUT",
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
    require(record["source_commit"] == "1a75dfe", "wrong source commit")
    require(record["construction_mode"] == "repaired_skeleton_prepared_matrix_cache", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    state = record["prepared_state"]
    require(state["field"] == "GF(17^32)", "wrong field")
    require(state["H_order"] == 512, "wrong H order")
    require(state["base_source_commit"] == "2dfd1d9", "wrong base source commit")
    require(state["base_capacity"] == 333, "wrong base capacity")
    require(state["base_pair_B_values"] == [1024, 657, 656, 1024, 1024], "wrong base pairs")
    require(state["base_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong base collapse")
    require(state["failed_split_commit"] == "7a02b97", "wrong failed split commit")
    require(state["failed_split_capacity"] == 315, "wrong failed split capacity")
    require(state["failed_split_pair_B_values"] == [1024, 593, 592, 512, 1024], "wrong failed split pairs")
    require(state["matrix_shape"] == [354, 1536], "wrong matrix shape")
    require(state["rank"] == 354, "wrong rank")
    require(state["nullity"] == 1182, "wrong nullity")
    require(state["fixed_specs_count"] == 129, "wrong fixed spec count")
    require(state["free_pattern"] == "d2_first_free", "wrong free pattern")
    require(state["cache_type"] in ALLOWED_CACHE_TYPES, "bad cache type")

    hashes = state["metadata_hashes"]
    for key in [
        "fixed_specs_hash",
        "base_vector_hash",
        "base_codeword_value_hash",
        "base_value_class_hash",
        "coordinate_ledger_hash",
        "parent_result_hash",
    ]:
        require_hash(hashes[key], key)

    if state["cache_type"] == "RECONSTRUCTION_ONLY":
        require(state["pivot_columns_hash"] is None, "unexpected pivot hash")
        require(state["free_columns_hash"] is None, "unexpected free hash")
        require(state["independent_rows_hash"] is None, "unexpected independent row hash")
        require(state["sage_cache_hash"] is None, "unexpected Sage cache hash")
        require(state["cache_limitations"], "missing cache limitations")

    replay = record["cache_replay"]
    require(replay["replay_status"] == "PASS", "base replay did not pass")
    require(isinstance(replay["small_append_test_run"], bool), "bad append flag")
    require(isinstance(replay["small_append_test_timeout"], bool), "bad timeout flag")
    require(set(replay["cache_labels"]).issubset(ALLOWED_LABELS), "bad cache label")
    require_hash(replay["cache_replay_hash"], "cache_replay_hash")

    if replay["small_append_test_timeout"]:
        require(record["proof_status"] == "PARTIAL", "timeout cache should be partial")
        require("CACHE_SMALL_APPEND_TIMEOUT" in replay["cache_labels"], "missing timeout label")
    elif state["cache_type"] != "RECONSTRUCTION_ONLY":
        require(record["proof_status"] == "EXACT_STATE_CACHE", "usable cache should be exact-state cache")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "cache_type": state["cache_type"],
        "matrix_shape": state["matrix_shape"],
        "rank": state["rank"],
        "nullity": state["nullity"],
        "replay_status": replay["replay_status"],
        "small_append_test_run": replay["small_append_test_run"],
        "small_append_test_timeout": replay["small_append_test_timeout"],
        "cache_labels": replay["cache_labels"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 repaired-skeleton prepared matrix cache")


if __name__ == "__main__":
    main()
