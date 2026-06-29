#!/usr/bin/env python3
"""High-overlap value-class beam search for the M1 a=327 witness target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import scan_m1_a327_valueclass_boundary_search as boundary


OUTPUT_DATA = Path("experimental/data/m1_a327_valueclass_high_overlap_beam.json")

N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = K - 1
RETAINED_PROXY_COUNT = 20
MUTATION_STEPS = 5000
TRAJECTORIES_PER_SEED = 8


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


def mask_from_combo(combo: tuple[int, ...]) -> int:
    mask = 0
    for item in combo:
        mask |= 1 << item
    return mask


ALL_MASKS = [
    mask_from_combo(combo)
    for size in [3, 4, 5, 6]
    for combo in itertools.combinations(range(LIST_SIZE), size)
]


def pair_count_key(mask_a: int, mask_b: int) -> tuple[int, ...]:
    counts = [0] * LIST_SIZE
    for mask in [mask_a, mask_b]:
        for item in members(mask):
            counts[item] += 1
    return tuple(counts)


def replacement_pairs() -> dict[tuple[int, ...], list[tuple[int, int]]]:
    replacements: dict[tuple[int, ...], list[tuple[int, int]]] = {}
    for left in ALL_MASKS:
        for right in ALL_MASKS:
            replacements.setdefault(pair_count_key(left, right), []).append((left, right))
    return replacements


REPLACEMENT_PAIRS = replacement_pairs()


def quotient_fiber_profile(masks: list[int]) -> dict[str, Any]:
    profile = []
    for fiber_id, positions in enumerate(boundary.quotient_fibers()):
        hist: dict[str, int] = {}
        unique_masks = set()
        for pos in positions:
            mask = masks[pos]
            hist[str(len(members(mask)))] = hist.get(str(len(members(mask))), 0) + 1
            unique_masks.add(mask)
        profile.append(
            {
                "fiber": fiber_id,
                "membership_histogram": dict(sorted(hist.items(), key=lambda item: int(item[0]))),
                "unique_mask_count": len(unique_masks),
            }
        )
    return {
        "fiber_count": 16,
        "fiber_size": 32,
        "profile_hash": hash_payload(profile),
        "profiles": profile,
    }


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
    return {
        "support_sizes": supports,
        "min_support_size": min(supports),
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
    }


def pair_counts_from_masks(masks: list[int]) -> dict[str, int]:
    pair_counts = {pair_key(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    for mask in masks:
        for i, j in itertools.combinations(members(mask), 2):
            pair_counts[pair_key(i, j)] += 1
    return pair_counts


def histogram_from_masks(masks: list[int]) -> dict[int, int]:
    histogram: dict[int, int] = {}
    for mask in masks:
        histogram[len(members(mask))] = histogram.get(len(members(mask)), 0) + 1
    return histogram


def beam_score(pair_counts: dict[str, int], histogram: dict[int, int]) -> int:
    values = list(pair_counts.values())
    size_diversity = sum(1 for size in [3, 4, 5, 6] if histogram.get(size, 0))
    return (
        100_000 * sum(1 for value in values if value >= 250)
        + 10_000 * sum(1 for value in values if value == PAIR_CAP)
        + 1_000 * sum(1 for value in values if value >= 245)
        + 10 * sum(max(0, value - 245) for value in values)
        + 50 * size_diversity
        + histogram.get(3, 0)
        + histogram.get(6, 0)
    )


def pair_delta(old_masks: tuple[int, int], new_masks: tuple[int, int]) -> dict[str, int]:
    delta: dict[str, int] = {}
    for mask, sign in [(old_masks[0], -1), (old_masks[1], -1), (new_masks[0], 1), (new_masks[1], 1)]:
        for i, j in itertools.combinations(members(mask), 2):
            key = pair_key(i, j)
            delta[key] = delta.get(key, 0) + sign
    return delta


def run_mutation_trajectory(base_masks: list[int], seed: int, steps: int = MUTATION_STEPS) -> tuple[list[int], int]:
    rng = random.Random(seed)
    masks = list(base_masks)
    pair_counts = pair_counts_from_masks(masks)
    histogram = histogram_from_masks(masks)
    current_score = beam_score(pair_counts, histogram)
    best_masks = list(masks)
    best_score = current_score

    for _ in range(steps):
        left_idx, right_idx = rng.sample(range(N), 2)
        old_pair = (masks[left_idx], masks[right_idx])
        choices = REPLACEMENT_PAIRS[pair_count_key(*old_pair)]
        for _attempt in range(8):
            new_pair = rng.choice(choices)
            if new_pair == old_pair:
                continue
            delta = pair_delta(old_pair, new_pair)
            if any(pair_counts[key] + change < 0 or pair_counts[key] + change > PAIR_CAP for key, change in delta.items()):
                continue

            new_histogram = dict(histogram)
            for mask in old_pair:
                size = len(members(mask))
                new_histogram[size] -= 1
            for mask in new_pair:
                size = len(members(mask))
                new_histogram[size] = new_histogram.get(size, 0) + 1

            new_pair_counts = dict(pair_counts)
            for key, change in delta.items():
                new_pair_counts[key] += change
            new_score = beam_score(new_pair_counts, new_histogram)
            if new_score >= current_score or rng.random() < 0.001:
                masks[left_idx], masks[right_idx] = new_pair
                pair_counts = new_pair_counts
                histogram = new_histogram
                current_score = new_score
                if current_score > best_score:
                    best_score = current_score
                    best_masks = list(masks)
                break

    return best_masks, best_score


def seed_candidates() -> list[dict[str, Any]]:
    boundary_candidates = boundary.candidate_designs()
    seed_ids = [
        "pair_boundary_45_c00_b5_064",
        "pair_boundary_45_c15_b5_064",
        "quotient_fiber_45_c00_b5_064",
        "quotient_fiber_45_c15_b5_064",
        "boundary_residual_45_c00_b5_096",
        "boundary_residual_45_c00_b5_200",
        "boundary_residual_45_c15_b5_096",
        "boundary_residual_45_c15_b5_200",
    ]
    by_id = {candidate["candidate_id"]: candidate for candidate in boundary_candidates}
    return [by_id[candidate_id] for candidate_id in seed_ids]


def candidate_designs() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for seed_index, seed_candidate in enumerate(seed_candidates()):
        for trajectory in range(TRAJECTORIES_PER_SEED):
            seed = 0xA327B000 + 1009 * seed_index + 9176 * trajectory
            masks, score = run_mutation_trajectory(seed_candidate["membership_masks"], seed)
            summary = summarize_masks(masks)
            if summary["support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
                raise RuntimeError("support size target not met")
            if summary["max_pair_intersection"] > PAIR_CAP:
                raise RuntimeError("pair cap exceeded")
            candidates.append(
                {
                    "candidate_id": (
                        f"high_overlap_from_{seed_candidate['candidate_id']}"
                        f"_t{trajectory:02d}"
                    ),
                    "family": "high_overlap_beam",
                    "source_candidate_id": seed_candidate["candidate_id"],
                    "source_family": seed_candidate["family"],
                    "seed": seed,
                    "mutation_steps": MUTATION_STEPS,
                    "beam_score": score,
                    "membership_masks": masks,
                    "summary": summary,
                    "quotient_fiber_profile_hash": quotient_fiber_profile(masks)["profile_hash"],
                }
            )
    return sorted(candidates, key=lambda item: (item["beam_score"], item["candidate_id"]), reverse=True)


def rank_result_key(row: dict[str, Any]) -> tuple[int, int, int, int, int, int, int]:
    return (
        row["proxy_nullity"],
        -row["proxy_rank"],
        row["pairs_at_255"],
        row["pairs_at_or_above_250"],
        row["pairs_at_or_above_245"],
        row["pair_boundary_score"],
        row["beam_score"],
    )


def build_record(rank_results: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    candidates = candidate_designs()
    best = None
    retained: list[dict[str, Any]] = []
    proof_status = "PARTIAL"
    proxy_positive_count = 0
    if rank_results is not None:
        if len(rank_results) != len(candidates):
            raise ValueError("rank result count mismatch")
        sorted_results = sorted(rank_results, key=rank_result_key, reverse=True)
        best = sorted_results[0]
        retained = sorted_results[:RETAINED_PROXY_COUNT]
        proxy_positive_count = sum(1 for row in rank_results if row["proxy_nullity"] > 0)
        proof_status = "CANDIDATE" if proxy_positive_count else "TESTED_DESIGNS_NO_PROXY_NULLITY"

    summary_rows = [candidate["summary"] for candidate in candidates]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "valueclass_high_overlap_beam",
        "candidate_count": len(candidates),
        "seed_candidate_count": len(seed_candidates()),
        "trajectories_per_seed": TRAJECTORIES_PER_SEED,
        "mutation_steps": MUTATION_STEPS,
        "candidate_design_hash": hash_payload(candidates),
        "design_constraints": {
            "support_size": TARGET_AGREEMENT,
            "pair_cap": PAIR_CAP,
            "membership_sizes_allowed": [3, 4, 5, 6],
        },
        "search_summary": {
            "max_pairs_at_255": max(row["pairs_at_255"] for row in summary_rows),
            "max_pairs_at_or_above_250": max(row["pairs_at_or_above_250"] for row in summary_rows),
            "max_pairs_at_or_above_245": max(row["pairs_at_or_above_245"] for row in summary_rows),
            "max_pair_boundary_score": max(row["pair_boundary_score"] for row in summary_rows),
            "membership_histograms": sorted(
                {hash_payload(row["membership_histogram"]): row["membership_histogram"] for row in summary_rows}.values(),
                key=lambda row: json.dumps(row, sort_keys=True),
            )[:8],
        },
        "rank_gate": {
            "status": "SAGE_PROXY_RANKED" if rank_results is not None else "NOT_RUN",
            "proxy_field": "GF(12289)",
            "exact_field": "GF(17^32)",
            "exact_trigger": "proxy_nullity > 0",
            "all_result_count": 0 if rank_results is None else len(rank_results),
            "all_result_hash": None if rank_results is None else hash_payload(rank_results),
            "retained_proxy_count": len(retained),
            "proxy_positive_count": proxy_positive_count,
            "best": best,
            "retained_results": retained,
        },
        "exact_audited_count": 0,
        "proof_status": proof_status,
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
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
