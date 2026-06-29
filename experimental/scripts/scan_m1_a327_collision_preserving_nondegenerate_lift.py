#!/usr/bin/env python3
"""Plan collision-preserving nondegenerate exact-lift pin schedules."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_a327_nondegenerate_exact_lift.json")
ROBUST_DATA = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_collision_preserving_nondegenerate_lift_plan.json")

K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "9c2f278"


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


def block_distribution(columns: list[int]) -> dict[str, int]:
    hist: dict[str, int] = {}
    for col in columns:
        label = f"D_{2 + int(col) // K}"
        hist[label] = hist.get(label, 0) + 1
    return dict(sorted(hist.items()))


def unique_in_order(columns: list[int]) -> list[int]:
    seen = set()
    output = []
    for col in columns:
        col = int(col)
        if col in seen:
            continue
        seen.add(col)
        output.append(col)
    return output


def common_free_by_block(system: dict[str, Any], block: int) -> list[int]:
    return [int(col) for col in system["common_free_columns"] if int(col) // K == block]


def proxy_support_free(system: dict[str, Any]) -> list[int]:
    common_free = set(int(col) for col in system["common_free_columns"])
    return unique_in_order([int(col) for col in system["best_schedule"]["free_columns"] if int(col) in common_free])


def pin_families(system: dict[str, Any]) -> list[dict[str, Any]]:
    proxy_cols = proxy_support_free(system)
    families = []
    for per_block in [1, 2, 4]:
        cols = list(proxy_cols)
        pinned = {}
        for block in range(1, DIFF_COUNT):
            block_cols = common_free_by_block(system, block)[:per_block]
            cols.extend(block_cols)
            pinned[f"D_{block + 2}"] = block_cols
        cols = unique_in_order(cols)
        families.append(
            {
                "family": f"coefficient_proxy_plus_5x{per_block}",
                "free_columns": cols,
                "pin_kind": "coefficient_free_values",
                "pin_profile": pinned,
                "free_column_count": len(cols),
                "free_block_distribution": block_distribution(cols),
            }
        )
    cols = list(proxy_cols)
    pinned = {}
    for block in range(DIFF_COUNT):
        block_cols = common_free_by_block(system, block)[:1]
        cols.extend(block_cols)
        pinned[f"D_{block + 2}"] = block_cols
    families.append(
        {
            "family": "coefficient_proxy_plus_6x1",
            "free_columns": unique_in_order(cols),
            "pin_kind": "coefficient_free_values",
            "pin_profile": pinned,
            "free_column_count": len(unique_in_order(cols)),
            "free_block_distribution": block_distribution(unique_in_order(cols)),
        }
    )
    return families


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
    planned = []
    for system in systems:
        planned.append(
            {
                "system_id": system["system_id"],
                "source_proxy_best_max_min": system["source_proxy_best_max_min"],
                "source_proxy_best_agreement": system["source_proxy_best_agreement"],
                "common_pivot_count": system["common_pivot_count"],
                "common_free_count": system["common_free_count"],
                "proxy_support_free_count": len(proxy_support_free(system)),
                "pin_families": pin_families(system),
                "row_subsets": ["proxy_pivot_rows_64", "proxy_pivot_rows_128"],
                "pivot_schedules": ["prefix_pivots", "mixed_block_pivots"],
            }
        )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "collision_preserving_nondegenerate_lift_plan",
        "source_commit": SOURCE_COMMIT,
        "baseline": {
            "best_high_capacity_degenerate_capacity": source["exact_lift_search"]["best_capacity_upper_bound"],
            "best_degenerate_max_min": source["exact_lift_search"]["best_exact_max_min"],
            "best_nondegenerate_capacity": 94,
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
