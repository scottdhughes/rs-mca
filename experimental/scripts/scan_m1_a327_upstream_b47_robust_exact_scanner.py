#!/usr/bin/env python3
"""Ledger scaffold for exact upstream B47-robust skeleton scanner."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


LEDGER_PATH = Path("experimental/data/m1_a327_upstream_b47_robust_skeleton_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SOURCE_COMMIT = "0500d07"
SYSTEMS_PLANNED = 24


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


def empty_exact_scanner() -> dict[str, Any]:
    return {
        "systems_planned": SYSTEMS_PLANNED,
        "systems_tested": 0,
        "timeouts": 0,
        "exact_vectors_constructed": 0,
        "split_probe_vectors": 0,
        "split_resilient_skeletons": 0,
        "candidate_families": [
            "alt_14_57",
            "alt_15_47",
            "alt_17_45",
            "alt_145_7",
            "b47_guard",
            "triple_237_b47_guard",
        ],
        "budgets": [1, 2, 4, 8],
        "split_probe_families": [
            "split_4_from_157",
            "split_14_vs_57",
            "split_1_from_457",
        ],
        "best_pre_split_capacity": None,
        "best_pre_split_pair_B_values": None,
        "best_probe_split_capacity": None,
        "best_probe_split_pair_B_values": None,
        "best_robustness_score": None,
        "best_collapse_pattern": None,
        "best_exact_max_min": None,
        "best_failure_mode": "UPSTREAM_EXACT_SCANNER_PENDING",
        "failure_mode_counts": {},
        "results": [],
    }


def proof_status(exact_scanner: dict[str, Any]) -> str:
    if exact_scanner.get("best_failure_mode") == "UPSTREAM_EXACT_CANDIDATE":
        return "PROOF_RECORD"
    if exact_scanner.get("systems_tested", 0) < exact_scanner.get("systems_planned", SYSTEMS_PLANNED):
        return "PARTIAL"
    if exact_scanner.get("systems_tested", 0):
        return "EXACT_EXTRACTION_NO_A327"
    return "PARTIAL"


def build_record(exact_scanner: dict[str, Any] | None = None) -> dict[str, Any]:
    ledger = load_json(LEDGER_PATH)
    exact_scanner = exact_scanner or empty_exact_scanner()
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "upstream_b47_ledger": {
            "source_skeletons_analyzed": ledger["upstream_b47_search"]["source_skeletons_analyzed"],
            "split_probe_vectors": ledger["upstream_b47_search"]["split_probe_vectors"],
            "split_resilient_skeletons": ledger["upstream_b47_search"]["split_resilient_skeletons"],
            "best_failure_mode": ledger["upstream_b47_search"]["best_failure_mode"],
        },
        "exact_scanner": exact_scanner,
        "proof_status": proof_status(exact_scanner),
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "global obstruction outside the tested basin",
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
