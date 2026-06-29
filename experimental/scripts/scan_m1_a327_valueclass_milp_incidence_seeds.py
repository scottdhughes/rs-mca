#!/usr/bin/env python3
"""MILP-generated value-class incidence seeds for the M1 a=327 target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


OUTPUT_DATA = Path("experimental/data/m1_a327_valueclass_milp_incidence_seeds.json")

N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = K - 1

PROFILE_SPECS = [
    {
        "profile_id": "all_sizes_max_pairs_at255",
        "allowed_sizes": [1, 2, 3, 4, 5, 6, 7],
        "objective": "max_threshold_pairs",
        "threshold": 255,
    },
    {
        "profile_id": "all_sizes_max_pairs_at250",
        "allowed_sizes": [1, 2, 3, 4, 5, 6, 7],
        "objective": "max_threshold_pairs",
        "threshold": 250,
    },
    {
        "profile_id": "all_sizes_min_anchor_variables",
        "allowed_sizes": [1, 2, 3, 4, 5, 6, 7],
        "objective": "min_anchor_variables",
        "threshold": 255,
    },
    {
        "profile_id": "sizes_3_6_max_pairs_at255",
        "allowed_sizes": [3, 4, 5, 6],
        "objective": "max_threshold_pairs",
        "threshold": 255,
    },
    {
        "profile_id": "sizes_3_7_max_pairs_at255",
        "allowed_sizes": [3, 4, 5, 6, 7],
        "objective": "max_threshold_pairs",
        "threshold": 255,
    },
    {
        "profile_id": "sizes_4_5_max_pairs_at255",
        "allowed_sizes": [4, 5],
        "objective": "max_threshold_pairs",
        "threshold": 255,
    },
]

EMBEDDINGS = ["block", "bit_reversal", "fiber_round_robin"]


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


def pair_key(i: int, j: int) -> str:
    if i > j:
        i, j = j, i
    return f"{i},{j}"


def members(mask: int) -> list[int]:
    return [idx for idx in range(LIST_SIZE) if mask & (1 << idx)]


def mask_size(mask: int) -> int:
    return len(members(mask))


def pair_labels() -> list[tuple[int, int]]:
    return list(itertools.combinations(range(LIST_SIZE), 2))


def quotient_fibers() -> list[list[int]]:
    return [[residue + 16 * offset for offset in range(32)] for residue in range(16)]


def bit_reverse(value: int, width: int = 9) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def embedding_order(embedding: str) -> list[int]:
    if embedding == "block":
        return list(range(N))
    if embedding == "bit_reversal":
        return [bit_reverse(idx) for idx in range(N)]
    if embedding == "fiber_round_robin":
        fibers = quotient_fibers()
        return [fibers[residue][offset] for offset in range(32) for residue in range(16)]
    raise ValueError(f"unknown embedding: {embedding}")


def summarize_masks(masks: list[int]) -> dict[str, Any]:
    supports = [0] * LIST_SIZE
    pair_counts = {pair_key(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    histogram: dict[str, int] = {}
    for mask in masks:
        bits = members(mask)
        histogram[str(len(bits))] = histogram.get(str(len(bits)), 0) + 1
        for item in bits:
            supports[item] += 1
        for i, j in itertools.combinations(bits, 2):
            pair_counts[pair_key(i, j)] += 1
    pair_values = list(pair_counts.values())
    anchor_pair_sum = sum(pair_counts[pair_key(0, witness)] for witness in range(1, LIST_SIZE))
    return {
        "support_sizes": supports,
        "min_support_size": min(supports),
        "max_support_size": max(supports),
        "max_pair_intersection": max(pair_values),
        "min_pair_intersection": min(pair_values),
        "pair_intersections": dict(sorted(pair_counts.items())),
        "membership_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "membership_size_support": sorted(int(size) for size, count in histogram.items() if count),
        "pairs_at_255": sum(1 for value in pair_values if value == PAIR_CAP),
        "pairs_at_or_above_250": sum(1 for value in pair_values if value >= 250),
        "pairs_at_or_above_245": sum(1 for value in pair_values if value >= 245),
        "pair_boundary_score": sum(max(0, value - 245) for value in pair_values),
        "pair_square_score": sum(value * value for value in pair_values),
        "pair_intersection_sum": sum(pair_values),
        "anchor_pair_sum": anchor_pair_sum,
        "anchor_compressed_variables": (LIST_SIZE - 1) * K - anchor_pair_sum,
    }


def solve_profile(spec: dict[str, Any]) -> dict[str, Any]:
    allowed_masks = [mask for mask in range(1, 1 << LIST_SIZE) if mask_size(mask) in spec["allowed_sizes"]]
    pairs = pair_labels()
    mask_count = len(allowed_masks)
    pair_count = len(pairs)
    total_vars = mask_count + pair_count
    objective = np.zeros(total_vars)

    pair_incidence = []
    for left, right in pairs:
        row = np.zeros(total_vars)
        for idx, mask in enumerate(allowed_masks):
            if (mask & (1 << left)) and (mask & (1 << right)):
                row[idx] = 1
        pair_incidence.append(row)

    if spec["objective"] == "max_threshold_pairs":
        # Primary objective: maximize threshold indicators. Secondary objective:
        # maximize total pair pressure among tied optima.
        objective[mask_count:] = -1_000_000
        for idx, mask in enumerate(allowed_masks):
            objective[idx] = -sum(1 for left, right in pairs if (mask & (1 << left)) and (mask & (1 << right)))
    elif spec["objective"] == "min_anchor_variables":
        # Equivalent to maximizing the six anchor pair intersections.
        for idx, mask in enumerate(allowed_masks):
            objective[idx] = -sum(1 for witness in range(1, LIST_SIZE) if (mask & 1) and (mask & (1 << witness)))
        for idx, (left, right) in enumerate(pairs):
            if left == 0:
                objective[mask_count + idx] = -1
    else:
        raise ValueError(f"unknown objective: {spec['objective']}")

    rows = []
    lower = []
    upper = []

    row = np.zeros(total_vars)
    row[:mask_count] = 1
    rows.append(row)
    lower.append(N)
    upper.append(N)

    for witness in range(LIST_SIZE):
        row = np.zeros(total_vars)
        for idx, mask in enumerate(allowed_masks):
            if mask & (1 << witness):
                row[idx] = 1
        rows.append(row)
        lower.append(TARGET_AGREEMENT)
        upper.append(TARGET_AGREEMENT)

    for pair_idx, row in enumerate(pair_incidence):
        rows.append(row.copy())
        lower.append(0)
        upper.append(PAIR_CAP)
        if spec["objective"] == "max_threshold_pairs":
            threshold_row = row.copy()
            threshold_row[mask_count + pair_idx] = -spec["threshold"]
            rows.append(threshold_row)
            lower.append(0)
            upper.append(np.inf)

    constraints = LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper))
    bounds = Bounds(np.zeros(total_vars), np.r_[np.full(mask_count, N), np.ones(pair_count)])
    integrality = np.ones(total_vars)
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=constraints,
        options={"time_limit": 60},
    )
    if not result.success:
        raise RuntimeError(f"MILP failed for {spec['profile_id']}: {result.message}")

    counts = np.rint(result.x[:mask_count]).astype(int)
    indicators = np.rint(result.x[mask_count:]).astype(int)
    mask_counts = {
        str(mask): int(count)
        for mask, count in zip(allowed_masks, counts)
        if int(count) != 0
    }
    sequence = []
    for mask in sorted(mask_counts, key=lambda item: (mask_size(int(item)), int(item))):
        sequence.extend([int(mask)] * mask_counts[str(mask)])
    if len(sequence) != N:
        raise RuntimeError(f"profile {spec['profile_id']} expanded to {len(sequence)} coordinates")

    block_summary = summarize_masks(sequence)
    threshold = spec["threshold"]
    return {
        "profile_id": spec["profile_id"],
        "allowed_sizes": spec["allowed_sizes"],
        "objective": spec["objective"],
        "threshold": threshold,
        "milp_success": bool(result.success),
        "milp_message": str(result.message),
        "objective_value": float(result.fun),
        "threshold_indicator_count": int(sum(indicators)),
        "mask_counts": mask_counts,
        "mask_count_hash": hash_payload(mask_counts),
        "profile_summary": block_summary,
    }


def masks_from_profile(profile: dict[str, Any], embedding: str) -> list[int]:
    sequence = []
    mask_counts = {int(mask): int(count) for mask, count in profile["mask_counts"].items()}
    for mask in sorted(mask_counts, key=lambda item: (mask_size(item), item)):
        sequence.extend([mask] * mask_counts[mask])
    order = embedding_order(embedding)
    masks = [0] * N
    for source_idx, position in enumerate(order):
        masks[position] = sequence[source_idx]
    return masks


def candidate_designs(profiles: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    profiles = profiles if profiles is not None else [solve_profile(spec) for spec in PROFILE_SPECS]
    candidates = []
    for profile in profiles:
        for embedding in EMBEDDINGS:
            masks = masks_from_profile(profile, embedding)
            summary = summarize_masks(masks)
            if summary["support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
                raise RuntimeError("support size target not met")
            if summary["max_pair_intersection"] > PAIR_CAP:
                raise RuntimeError("pair cap exceeded")
            candidates.append(
                {
                    "candidate_id": f"{profile['profile_id']}_{embedding}",
                    "family": "milp_incidence_seed",
                    "profile_id": profile["profile_id"],
                    "embedding": embedding,
                    "membership_masks": masks,
                    "membership_mask_hash": hash_payload(masks),
                    "summary": summary,
                }
            )
    return candidates


def build_record() -> dict[str, Any]:
    profiles = [solve_profile(spec) for spec in PROFILE_SPECS]
    candidates = candidate_designs(profiles)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "valueclass_milp_incidence_seeds",
        "solver": {
            "name": "scipy.optimize.milp",
            "profile_count": len(PROFILE_SPECS),
            "embedding_count": len(EMBEDDINGS),
        },
        "design_constraints": {
            "support_size": TARGET_AGREEMENT,
            "pair_cap": PAIR_CAP,
            "coordinate_count": N,
            "list_size": LIST_SIZE,
        },
        "profiles": profiles,
        "candidate_count": len(candidates),
        "candidate_design_hash": hash_payload(candidates),
        "candidates": candidates,
        "rank_gate": {
            "status": "NOT_RUN",
            "proxy_field": "GF(12289)",
            "exact_field": "GF(17^32)",
        },
        "proof_status": "CANDIDATE_SEEDS",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list certificate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "improvement over PR #133",
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
