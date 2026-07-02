#!/usr/bin/env python3
"""Prepared-state cache ledger for the repaired M1 a=327 skeleton."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any


PERSISTENT_STATE_PATH = Path("experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json")
COMPENSATED_TIMEOUT_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_repaired_skeleton_prepared_matrix_cache.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "1a75dfe"


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


def build_prepared_state(persistent: dict[str, Any]) -> dict[str, Any]:
    replay = persistent["exact_state_replay"]
    row_state = replay["row_state"]
    state_hashes = replay["state_hashes"]
    variable_count = int(row_state["source_rank_after"]) + int(row_state["source_nullity_after"])
    return {
        "field": "GF(17^32)",
        "H_order": 512,
        "field_construction_hash": state_hashes["result_hash"],
        "subgroup_generator_hash": None,
        "subgroup_generator_hash_status": "not_persisted_in_parent_replay",
        "base_source_commit": "2dfd1d9",
        "base_capacity": replay["source_skeleton"]["capacity"],
        "base_pair_B_values": replay["source_skeleton"]["pair_B_values"],
        "base_collapse_pattern": replay["source_skeleton"]["collapse_pattern"],
        "failed_split_commit": "7a02b97",
        "failed_split_capacity": replay["failed_split"]["capacity"],
        "failed_split_pair_B_values": replay["failed_split"]["pair_B_values"],
        "matrix_shape": [row_state["source_effective_row_count"], variable_count],
        "rank": row_state["source_rank_after"],
        "nullity": row_state["source_nullity_after"],
        "fixed_specs_count": row_state["fixed_specs_count"],
        "free_pattern": row_state["free_pattern"],
        "pivot_columns_hash": None,
        "free_columns_hash": None,
        "independent_rows_hash": None,
        "row_reduced_state_hash": None,
        "sage_cache_hash": None,
        "sage_cache_artifact": None,
        "cache_type": "RECONSTRUCTION_ONLY",
        "cache_limitations": [
            "parent replay persists deterministic specs and vector/value hashes but not pivot columns",
            "parent replay persists rank/nullity but not independent row indices",
            "parent replay does not expose a Sage-native prepared matrix or transformation object",
        ],
        "metadata_hashes": {
            "fixed_specs_hash": state_hashes["fixed_specs_hash"],
            "base_vector_hash": state_hashes["base_vector_hash"],
            "base_codeword_value_hash": state_hashes["base_codeword_value_hash"],
            "base_value_class_hash": state_hashes["base_value_class_hash"],
            "coordinate_ledger_hash": state_hashes["coordinate_ledger_hash"],
            "parent_result_hash": state_hashes["result_hash"],
        },
    }


def build_cache_replay(persistent: dict[str, Any], compensated: dict[str, Any]) -> dict[str, Any]:
    comp = compensated["compensated_split"]
    replay = persistent["exact_state_replay"]
    labels = ["CACHE_REPLAY_PASS"]
    if comp.get("best_failure_mode") == "COMP_REPAIRED_SPLIT_TIMEOUT":
        labels.append("CACHE_SMALL_APPEND_TIMEOUT")
    labels.append("CACHE_PIVOT_REUSE_FAILS")
    return {
        "replay_status": "PASS" if replay["replay_status"] == "PASS" else "FAIL",
        "small_append_test_run": comp.get("systems_tested", 0) > 0,
        "small_append_test_timeout": comp.get("best_failure_mode") == "COMP_REPAIRED_SPLIT_TIMEOUT",
        "small_append_test_source_commit": "1a75dfe",
        "small_append_test_failure_mode": comp.get("best_failure_mode"),
        "small_append_test_timeout_stage": comp.get("timeout_stage"),
        "small_append_exact_vectors_constructed": comp.get("exact_vectors_constructed"),
        "cache_labels": labels,
        "cache_replay_hash": hash_payload(
            {
                "persistent_result": replay["state_hashes"]["result_hash"],
                "compensated_timeout": comp.get("best_failure_mode"),
                "systems_tested": comp.get("systems_tested"),
                "exact_vectors_constructed": comp.get("exact_vectors_constructed"),
            }
        ),
    }


def build_record() -> dict[str, Any]:
    persistent = load_json(PERSISTENT_STATE_PATH)
    compensated = load_json(COMPENSATED_TIMEOUT_PATH)
    prepared_state = build_prepared_state(persistent)
    cache_replay = build_cache_replay(persistent, compensated)
    proof_status = "EXACT_STATE_CACHE"
    if prepared_state["cache_type"] == "RECONSTRUCTION_ONLY" or cache_replay["small_append_test_timeout"]:
        proof_status = "PARTIAL"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "repaired_skeleton_prepared_matrix_cache",
        "prepared_state": prepared_state,
        "cache_replay": cache_replay,
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
