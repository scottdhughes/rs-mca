#!/usr/bin/env python3
"""Ledger scaffold for pair {2,7}/{3,7} exchange-obstruction audit."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_post_d2split_pair7_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pair27_37_exchange_obstruction.json")
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "0639865"


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
    repair = source["post_d2_pair7_repair"]
    return {
        "d2_split_retained": repair["d2_split_retained"],
        "capacity_preserving_vectors": repair["capacity_preserving_vectors"],
        "low_collapse_capacity_preserving_vectors": repair["low_collapse_capacity_preserving_vectors"],
        "best_pair_B_values": repair["best_pair_B_values"],
        "best_capacity_upper_bound": repair["best_capacity_upper_bound"],
        "best_failure_mode": repair["best_failure_mode"],
    }


def build_record(
    pair27_37_diagnostic: dict[str, Any] | None = None,
    targeted_repair: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = load_json(SOURCE_DATA_PATH)
    pair27_37_diagnostic = pair27_37_diagnostic or {
        "vectors_analyzed": 0,
        "B27": None,
        "B37": None,
        "deficit27": None,
        "deficit37": None,
        "pair27_credit_histogram": {},
        "pair37_credit_histogram": {},
        "critical_coordinates": 0,
        "exchange_graph_feasible": None,
    }
    targeted_repair = targeted_repair or {
        "repair_sets_tested": 0,
        "exact_vectors_constructed": 0,
        "B27_repaired_vectors": 0,
        "B37_repaired_vectors": 0,
        "full_pair_repaired_vectors": 0,
        "best_exact_max_min": None,
        "best_pair_B_values": None,
        "best_failure_mode": "PAIR27_37_REPAIR_PENDING",
        "results": [],
    }
    proof_status = "PARTIAL"
    if targeted_repair["best_failure_mode"] == "PAIR27_37_EXACT_CANDIDATE":
        proof_status = "PROOF_RECORD"
    elif pair27_37_diagnostic["vectors_analyzed"] or targeted_repair["repair_sets_tested"]:
        proof_status = "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "pair27_37_exchange_obstruction",
        "baseline": baseline(source),
        "pair27_37_diagnostic": pair27_37_diagnostic,
        "targeted_repair": targeted_repair,
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
