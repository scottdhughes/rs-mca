#!/usr/bin/env python3
"""Ledger scaffold for repaired-skeleton persistent exact state."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_nondegenerate_split.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "7a02b97"


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
    search = source["repaired_skeleton_split"]
    return {
        "source_skeleton_commit": "2dfd1d9",
        "source_skeleton_capacity": source["baseline"]["capacity"],
        "source_skeleton_pair_B_values": source["baseline"]["pair_B_values"],
        "source_skeleton_collapse_pattern": source["baseline"]["collapse_pattern"],
        "failed_split_commit": SOURCE_COMMIT,
        "failed_split_family": "split_4_from_157",
        "failed_split_capacity": search["best_capacity"],
        "failed_split_pair_B_values": search["best_pair_B_values"],
        "failed_split_collapse_pattern": search["best_collapse_pattern"],
        "failed_split_failure_mode": search["best_failure_mode"],
    }


def build_record(exact_state_replay: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    exact_state_replay = exact_state_replay or {
        "exact_field": "GF(17^32)",
        "H_order": 512,
        "replay_status": "PENDING",
        "state_hashes": {},
        "row_state": {},
        "coordinate_ledger": {
            "coordinates": 0,
            "ledger_hash": None,
            "rows": [],
        },
    }
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "repaired_skeleton_persistent_exact_state",
        "baseline": baseline(source),
        "exact_state_replay": exact_state_replay,
        "proof_status": "EXACT_STATE_REPLAY" if exact_state_replay["replay_status"] == "PASS" else "PARTIAL",
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
