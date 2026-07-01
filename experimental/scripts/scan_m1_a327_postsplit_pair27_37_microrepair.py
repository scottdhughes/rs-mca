#!/usr/bin/env python3
"""Ledger scaffold for post-split pair {2,7}/{3,7} microrepair."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_reserve_pairclass_codesign_before_split.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_postsplit_pair27_37_microrepair.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SOURCE_COMMIT = "6c54e44"


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
    search = source["codesign_search"]
    pair_values = search["best_post_split_pair_B_values"]
    return {
        "post_split_capacity": search["best_post_split_capacity"],
        "post_split_pair_B_values": pair_values,
        "B27_deficit": PAIR_TARGET - pair_values[1],
        "B37_deficit": PAIR_TARGET - pair_values[2],
        "collapse_pattern": search["best_collapse_pattern"],
        "failure_mode": search["best_failure_mode"],
    }


def build_record(microrepair: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    microrepair = microrepair or {
        "systems_tested": 0,
        "timeouts": 0,
        "exact_vectors_constructed": 0,
        "capacity_preserving_vectors": 0,
        "pair27_repaired_vectors": 0,
        "pair37_repaired_vectors": 0,
        "pair27_37_repaired_vectors": 0,
        "pair57_preserving_vectors": 0,
        "collapse_preserving_vectors": 0,
        "best_capacity": None,
        "best_pair_B_values": None,
        "best_exact_max_min": None,
        "best_agreement_vector": None,
        "best_failure_mode": "MICROREPAIR_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if microrepair["best_failure_mode"] == "MICROREPAIR_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif microrepair["systems_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "postsplit_pair27_37_microrepair",
        "baseline": baseline(source),
        "microrepair": microrepair,
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
