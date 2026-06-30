#!/usr/bin/env python3
"""Plan dominant-collision-preserving separation pins for M1 a=327."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_a327_collision_preserving_nondegenerate_lift.json")
ROBUST_DATA = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_dominant_collision_preserving_separation_plan.json")

TARGET_AGREEMENT = 327
SOURCE_COMMIT = "9bbffb8"


def jsonable(payload: Any) -> Any:
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


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def build_plan(system_limit: int = 3) -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    robust = load_json(ROBUST_DATA)
    systems = sorted(
        robust["systems"],
        key=lambda row: (
            row["best_schedule"]["candidate_prime_count"],
            row["pivot_stability_score"],
            row["source_proxy_best_max_min"],
            row["system_id"],
        ),
        reverse=True,
    )[:system_limit]
    planned = [
        {
            "system_id": system["system_id"],
            "source_proxy_best_max_min": system["source_proxy_best_max_min"],
            "best_schedule_id": system["best_schedule"]["schedule_id"],
            "proxy_support_free_columns": system["best_schedule"]["free_columns"],
            "row_subsets": [
                "dominant_collision_rows_64",
                "proxy_pivot_rows_128",
            ],
            "separation_families": [
                "one_pairwise_safe",
                "two_pairwise_safe",
                "five_eval_safe",
                "six_eval_safe",
            ],
            "pivot_schedules": ["prefix_pivots", "separation_aware_pivots"],
        }
        for system in systems
    ]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "dominant_collision_preserving_separation_plan",
        "source_commit": SOURCE_COMMIT,
        "baseline": {
            "best_degenerate_capacity_upper_bound": source["baseline"]["best_high_capacity_degenerate_capacity"],
            "best_pinned_nondegenerate_capacity_upper_bound": source["pin_search"]["best_capacity_upper_bound"],
        },
        "system_count": len(planned),
        "systems": planned,
        "result_hash": hash_payload(planned),
        "proof_status": "PARTIAL",
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
    parser.add_argument("--system-limit", type=int, default=3)
    args = parser.parse_args()
    record = build_plan(args.system_limit)
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
