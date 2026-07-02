#!/usr/bin/env python3
"""Ledger scaffold for compensated repaired-skeleton split."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SOURCE_COMMIT = "30d0cdb"


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
    base = source["baseline"]
    return {
        "capacity": base["source_skeleton_capacity"],
        "pair_B_values": base["source_skeleton_pair_B_values"],
        "collapse_pattern": base["source_skeleton_collapse_pattern"],
    }


def failed_split(source: dict[str, Any]) -> dict[str, Any]:
    base = source["baseline"]
    source_pairs = base["source_skeleton_pair_B_values"]
    failed_pairs = base["failed_split_pair_B_values"]
    return {
        "split_family": base["failed_split_family"],
        "capacity": base["failed_split_capacity"],
        "pair_B_values": failed_pairs,
        "collapse_pattern": base["failed_split_collapse_pattern"],
        "damage": {
            "capacity": base["failed_split_capacity"] - base["source_skeleton_capacity"],
            "B27": failed_pairs[1] - source_pairs[1],
            "B37": failed_pairs[2] - source_pairs[2],
            "B47": failed_pairs[3] - source_pairs[3],
            "B57": failed_pairs[4] - source_pairs[4],
        },
    }


def build_record(compensated_split: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    compensated_split = compensated_split or {
        "systems_tested": 0,
        "timeouts": 0,
        "exact_vectors_constructed": 0,
        "capacity_preserving_vectors": 0,
        "pair_guard_preserving_vectors": 0,
        "partial_split_vectors": 0,
        "nondegenerate_vectors": 0,
        "best_capacity": None,
        "best_pair_B_values": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_failure_mode": "COMP_REPAIRED_SPLIT_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if compensated_split["best_failure_mode"] == "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif compensated_split["systems_tested"] and compensated_split["best_failure_mode"] != "COMP_REPAIRED_SPLIT_TIMEOUT":
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "compensated_repaired_skeleton_split",
        "baseline": baseline(source),
        "failed_split": failed_split(source),
        "compensated_split": compensated_split,
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


def timeout_record() -> dict[str, Any]:
    planned_systems = 3 * 3 * 5
    return {
        "exact_field": "GF(17^32)",
        "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
        "split_families": ["split_4_from_157", "split_14_vs_57", "split_1_from_457"],
        "replacement_bundle_sizes": [8, 16, 32],
        "selectors": ["capacity_first", "B27_B37_first", "B47_first", "balanced_repair", "quotient_fiber_local"],
        "planned_systems": planned_systems,
        "systems_tested": 1,
        "timeouts": 1,
        "exact_vectors_constructed": 0,
        "capacity_preserving_vectors": 0,
        "pair_guard_preserving_vectors": 0,
        "partial_split_vectors": 0,
        "nondegenerate_vectors": 0,
        "setup_attempts": 3,
        "timeout_stage": "repaired_context GF(17^32) skeleton reconstruction",
        "timeout_observation": "Manual exact attempts were interrupted after multi-minute finite-field echelonization before any compensated vector was constructed.",
        "best_capacity": None,
        "best_pair_B_values": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_agreement_vector": None,
        "best_failure_mode": "COMP_REPAIRED_SPLIT_TIMEOUT",
        "failure_mode_counts": {"COMP_REPAIRED_SPLIT_TIMEOUT": 1},
        "results": [
            {
                "split_family": "split_4_from_157",
                "replacement_bundle_size": 8,
                "selector": "B47_first",
                "failure_mode": "COMP_REPAIRED_SPLIT_TIMEOUT",
                "timeout_stage": "repaired_context GF(17^32) skeleton reconstruction",
                "vector_results": [],
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--write-timeout-record", action="store_true")
    args = parser.parse_args()
    record = build_record(timeout_record() if args.write_timeout_record else None)
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.write_timeout_record:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
