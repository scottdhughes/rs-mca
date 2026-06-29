#!/usr/bin/env python3
"""Plan nondegenerate exact-lift schedules for robust M1 a=327 proxy systems."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_nondegenerate_exact_lift_plan.json")

K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "f9a43ea"


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


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def block_label(col: int) -> str:
    return f"D_{2 + col // K}"


def block_distribution(columns: list[int]) -> dict[str, int]:
    hist: dict[str, int] = {}
    for col in columns:
        label = block_label(int(col))
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


def first_common_free_by_block(common_free: list[int], per_block: int) -> list[int]:
    output = []
    for block in range(DIFF_COUNT):
        block_cols = [col for col in common_free if col // K == block]
        output.extend(block_cols[:per_block])
    return output


def proxy_support_columns(system: dict[str, Any]) -> list[int]:
    schedule = system["best_schedule"]
    columns = unique_in_order([int(col) for col in schedule["free_columns"]])
    common_free = set(int(col) for col in system["common_free_columns"])
    return [col for col in columns if col in common_free]


def free_schedules(system: dict[str, Any]) -> list[dict[str, Any]]:
    common_free = [int(col) for col in system["common_free_columns"]]
    proxy_support = proxy_support_columns(system)
    rng = random.Random(int(hash_payload([system["system_id"], "nondegenerate_free"])[:12], 16))
    random_common = list(common_free)
    rng.shuffle(random_common)
    schedules = [
        ("free_24_proxy_support", (proxy_support + common_free)[:24]),
        ("free_48_balanced_blocks", first_common_free_by_block(common_free, 8)),
        ("free_96_balanced_blocks", first_common_free_by_block(common_free, 16)),
        ("free_6x8_per_witness_block", first_common_free_by_block(common_free, 8)),
        ("free_6x16_per_witness_block", first_common_free_by_block(common_free, 16)),
        ("free_48_seeded_common", sorted(random_common[:48])),
    ]
    output = []
    seen_ids = set()
    for schedule_id, columns in schedules:
        columns = unique_in_order([int(col) for col in columns])
        if not columns:
            continue
        digest = hash_payload(columns)
        if digest in seen_ids:
            continue
        seen_ids.add(digest)
        output.append(
            {
                "schedule_id": schedule_id,
                "free_column_count": len(columns),
                "free_columns": columns,
                "free_block_distribution": block_distribution(columns),
            }
        )
    return output


def row_subset_plan(system: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = system["row_subset_candidates"]
    subset_ids = [
        "proxy_pivot_rows_64",
        "fiber_diverse_rows_64",
        "deficit_rows_64",
        "full_target_row_sample_64",
        "proxy_pivot_rows_128",
    ]
    output = []
    for subset_id in subset_ids:
        if subset_id not in candidates:
            continue
        rows = [int(row) for row in candidates[subset_id]]
        output.append(
            {
                "subset_id": subset_id,
                "row_count": len(rows),
                "row_hash": hash_payload(rows),
                "rows": rows,
            }
        )
    return output


def top_systems(source: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    return sorted(
        source["systems"],
        key=lambda row: (
            row["best_schedule"]["candidate_prime_count"],
            row["pivot_stability_score"],
            row["source_proxy_best_max_min"],
            row["system_id"],
        ),
        reverse=True,
    )[:limit]


def build_plan(system_limit: int = 1) -> dict[str, Any]:
    source = load_source()
    systems = []
    for system in top_systems(source, system_limit):
        systems.append(
            {
                "system_id": system["system_id"],
                "source_proxy_best_max_min": system["source_proxy_best_max_min"],
                "source_proxy_best_agreement": system["source_proxy_best_agreement"],
                "best_schedule_id": system["best_schedule"]["schedule_id"],
                "best_schedule_candidate_prime_count": system["best_schedule"]["candidate_prime_count"],
                "pivot_stability_score": system["pivot_stability_score"],
                "common_pivot_count": system["common_pivot_count"],
                "common_free_count": system["common_free_count"],
                "common_pivot_hash": system["common_pivot_hash"],
                "common_free_hash": system["common_free_hash"],
                "row_subsets": row_subset_plan(system),
                "free_schedules": free_schedules(system),
            }
        )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "nondegenerate_exact_lift_plan",
        "source": {
            "source_json": str(SOURCE_DATA),
            "source_commit": SOURCE_COMMIT,
            "source_result_hash": source["result_hash"],
            "source_proof_status": source["proof_status"],
            "source_system_count": source["system_count"],
        },
        "exact_strategy": {
            "row_subsets": [
                "proxy_pivot_rows_64",
                "fiber_diverse_rows_64",
                "deficit_rows_64",
                "full_target_row_sample_64",
                "proxy_pivot_rows_128",
            ],
            "value_patterns": [
                "all_ones",
                "blockwise_constants",
                "geometric_generator",
                "seeded_basefield",
            ],
            "full_nullspace_extraction": False,
        },
        "system_count": len(systems),
        "systems": systems,
        "result_hash": hash_payload(systems),
        "proof_status": "PARTIAL",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list proof record",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "improvement over PR #133",
            "full GF(17^32) nullspace extraction",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--system-limit", type=int, default=1)
    args = parser.parse_args()
    record = build_plan(args.system_limit)
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
