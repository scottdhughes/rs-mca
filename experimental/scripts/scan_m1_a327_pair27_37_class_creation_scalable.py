#!/usr/bin/env python3
"""Ledger scaffold for scalable exact pair {2,7}/{3,7} class creation."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_pair27_37_class_creation.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pair27_37_class_creation_scalable.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "07e987c"


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
    search = source["pair_class_creation"]
    return {
        "systems_tested": search["systems_tested"],
        "best_pair_B_values": search["best_pair_values"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "D2_split": search["D2_split_vectors"] > 0,
        "low_collapse_vectors": search["low_collapse_vectors"],
        "failure_mode": search["best_failure_mode"],
    }


def build_record(scalable_class_creation: dict[str, Any] | None = None) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    scalable_class_creation = scalable_class_creation or {
        "exact_field": "GF(17^32)",
        "T27_sizes": [64, 96],
        "T37_sizes": [64, 96],
        "systems_tested": 0,
        "incremental_blocks_tested": 0,
        "exact_vectors_constructed": 0,
        "D2_split_vectors": 0,
        "low_collapse_vectors": 0,
        "pair27_repaired_vectors": 0,
        "pair37_repaired_vectors": 0,
        "full_pair_repaired_vectors": 0,
        "best_pair_B_values": None,
        "best_capacity_upper_bound": None,
        "best_exact_max_min": None,
        "best_failure_mode": "SCALABLE_CLASS_CREATION_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if scalable_class_creation["best_failure_mode"] == "PAIR_CLASS_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif scalable_class_creation["systems_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "pair27_37_class_creation_scalable",
        "baseline": baseline(source),
        "scalable_class_creation": scalable_class_creation,
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
