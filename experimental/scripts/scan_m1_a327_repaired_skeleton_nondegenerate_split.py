#!/usr/bin/env python3
"""Ledger scaffold for repaired-skeleton nondegenerate split."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_postsplit_pair27_37_microrepair_stage2.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_repaired_skeleton_nondegenerate_split.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SOURCE_COMMIT = "2dfd1d9"


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


def best_stage2(source: dict[str, Any]) -> dict[str, Any]:
    rows = source["stage2_microrepair"]["results"]
    return max(
        rows,
        key=lambda row: (
            row.get("pair27_37_repaired") is True,
            row.get("capacity_upper_bound", -1),
            row.get("min_pair_B", -1),
            row.get("total_triple_237_budget", -1),
        ),
    )


def baseline(source: dict[str, Any]) -> dict[str, Any]:
    best = best_stage2(source)
    pair_values = best["pair_B_values"]
    return {
        "capacity": best["capacity_upper_bound"],
        "pair_B_values": pair_values,
        "pair_hall_bound": best["pair_hall_bound"],
        "B27_deficit": PAIR_TARGET - pair_values[1],
        "B37_deficit": PAIR_TARGET - pair_values[2],
        "B57": pair_values[4],
        "collapse_pattern": best["degenerate_classes"],
        "distinct_codewords": best["distinct_codewords"],
        "failure_mode": best["failure_mode"],
    }


def build_record(repaired_skeleton_split: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    repaired_skeleton_split = repaired_skeleton_split or {
        "systems_tested": 0,
        "timeouts": 0,
        "exact_vectors_constructed": 0,
        "nondegenerate_vectors": 0,
        "partial_split_vectors": 0,
        "capacity_preserving_vectors": 0,
        "pair_guard_preserving_vectors": 0,
        "best_capacity": None,
        "best_pair_B_values": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_agreement_vector": None,
        "best_failure_mode": "REPAIRED_SPLIT_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if repaired_skeleton_split["best_failure_mode"] == "REPAIRED_SPLIT_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif repaired_skeleton_split["systems_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "repaired_skeleton_nondegenerate_split",
        "baseline": baseline(source),
        "repaired_skeleton_split": repaired_skeleton_split,
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
