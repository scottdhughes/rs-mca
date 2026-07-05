#!/usr/bin/env python3
"""Synthesize deterministic rank-2 mu_8 carrier-plane seeds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scan_m1_a327_mu8_rank2_carrier_generator import (
    NOT_CLAIMED,
    build_planes,
    forced_equal_pairs,
    normalize_vector,
    rref_key,
)


OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_synthesized_carrier_planes.json")
TARGET = 327


def synthesized_vectors() -> list[dict]:
    vectors = []

    def add(name: str, values: list[int], family: str) -> None:
        vectors.append({"name": name, "family": family, "vector": list(normalize_vector(values))})

    templates = [
        ("block_0123", [1, 1, 1, 1, 0, 0, 0]),
        ("block_3456", [0, 0, 0, 1, 1, 1, 1]),
        ("block_0246", [1, 0, 1, 0, 1, 0, 1]),
        ("block_135", [0, 1, 0, 1, 0, 1, 0]),
        ("balanced_alt", [1, -1, 1, -1, 1, -1, 1]),
        ("balanced_ramp", [1, 2, 3, 4, 5, 6, 7]),
        ("balanced_reverse", [7, 6, 5, 4, 3, 2, 1]),
    ]
    for name, values in templates:
        add(name, values, "block_synthesis")
    return vectors


def build_synthesized(limit: int) -> list[dict]:
    base = build_planes(min(64, limit))
    synth = synthesized_vectors()
    seen = {tuple(tuple(row) for row in plane["gf17_rref_key"]) for plane in base}
    rows = list(base)
    for left in synth:
        for right in synth:
            if left["name"] >= right["name"]:
                continue
            key = rref_key([left["vector"], right["vector"]])
            if len(key) < 2 or key in seen:
                continue
            forced = forced_equal_pairs(left["vector"], right["vector"])
            if forced:
                continue
            seen.add(key)
            rows.append(
                {
                    "plane_id": f"synth_plane_{len(rows):04d}",
                    "left_vector_id": left["name"],
                    "right_vector_id": right["name"],
                    "families": sorted({left["family"], right["family"]}),
                    "u": left["vector"],
                    "v": right["vector"],
                    "gf17_rref_key": [list(row) for row in key],
                    "forced_equal_pairs": [],
                    "synthesis_method": "gf17_balanced_block_seed",
                    "status": "MU8_RANK2_SYNTHESIZED_CARRIER_PLANE",
                }
            )
            if len(rows) >= limit:
                return rows
    return rows[:limit]


def build_record(limit: int) -> dict:
    rows = build_synthesized(limit)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": "46a0755",
        "synthesis": {
            "requested_limit": limit,
            "planes_emitted": len(rows),
            "forced_pair_filtered": True,
            "best_failure_mode": "MU8_RANK2_SYNTHESIZED_CARRIER_PLANE",
        },
        "carrier_planes": rows,
        "proof_status": "CANDIDATE / MU8_RANK2_SYNTHESIZED_CARRIER_PLANE / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=256)
    args = parser.parse_args()
    record = build_record(args.limit)
    if args.write:
        OUTPUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        "planes_emitted": record["synthesis"]["planes_emitted"],
        "best_failure_mode": record["synthesis"]["best_failure_mode"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_RANK2_SYNTHESIZED_PLANES_READY")


if __name__ == "__main__":
    main()
