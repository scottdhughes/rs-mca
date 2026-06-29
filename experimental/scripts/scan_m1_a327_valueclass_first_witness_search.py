#!/usr/bin/env python3
"""Value-class-first incidence designs for the M1 a=327 witness search."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_a327_valueclass_first_witness_search.json")

N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
SIZE_FIVE_COUNT = 241
SIZE_FOUR_COUNT = 271
PAIR_CAP = K - 1


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def lcg(seed: int) -> int:
    return (6364136223846793005 * seed + 1442695040888963407) & ((1 << 64) - 1)


def shuffled(values: list[int], seed: int) -> list[int]:
    out = list(values)
    state = seed & ((1 << 64) - 1)
    for idx in range(len(out) - 1, 0, -1):
        state = lcg(state)
        swap = state % (idx + 1)
        out[idx], out[swap] = out[swap], out[idx]
    return out


def pair_key(i: int, j: int) -> str:
    if i > j:
        i, j = j, i
    return f"{i},{j}"


def mask_from_combo(combo: tuple[int, ...]) -> int:
    mask = 0
    for item in combo:
        mask |= 1 << item
    return mask


def members(mask: int) -> list[int]:
    return [idx for idx in range(LIST_SIZE) if mask & (1 << idx)]


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
    return {
        "support_sizes": supports,
        "min_support_size": min(supports),
        "max_pair_intersection": max(pair_counts.values()),
        "pair_intersections": dict(sorted(pair_counts.items())),
        "membership_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "pairs_at_cap": sum(1 for value in pair_counts.values() if value == PAIR_CAP),
    }


def feasible_after_choice(new_remaining: list[int], future_coordinates: int) -> bool:
    return all(0 <= value <= future_coordinates for value in new_remaining)


def score_combo(
    combo: tuple[int, ...],
    remaining: list[int],
    pair_counts: dict[str, int],
    future_coordinates: int,
    mode: str,
    target_pair: str | None,
    jitter_seed: int,
) -> tuple[float, int]:
    new_remaining = [remaining[idx] - (1 if idx in combo else 0) for idx in range(LIST_SIZE)]
    if not feasible_after_choice(new_remaining, future_coordinates):
        return (float("inf"), 0)
    for i, j in itertools.combinations(combo, 2):
        if pair_counts[pair_key(i, j)] >= PAIR_CAP:
            return (float("inf"), 0)

    average = sum(new_remaining) / LIST_SIZE
    balance = sum((value - average) ** 2 for value in new_remaining)
    pair_pressure = sum(pair_counts[pair_key(i, j)] for i, j in itertools.combinations(combo, 2))
    boundary_bonus = 0
    if mode == "pair_boundary_push" and target_pair is not None:
        a, b = [int(part) for part in target_pair.split(",")]
        if a in combo and b in combo:
            boundary_bonus = 20
    elif mode == "anti_anchor_balanced":
        if 0 not in combo:
            boundary_bonus = 16

    jitter = (jitter_seed % 997) / 997000.0
    return (balance + 0.015 * pair_pressure - boundary_bonus + jitter, jitter_seed)


def incidence_masks(seed: int, mode: str, target_pair: str | None = None) -> list[int]:
    base_sizes = [5] * SIZE_FIVE_COUNT + [4] * SIZE_FOUR_COUNT
    if mode == "quotient_fiber_balanced":
        sizes = []
        extra_five_used = False
        for fiber in range(16):
            fiber_sizes = [5] * 15 + [4] * 17
            if not extra_five_used:
                fiber_sizes[-1] = 5
                extra_five_used = True
            sizes.extend(shuffled(fiber_sizes, seed + fiber))
    else:
        sizes = shuffled(base_sizes, seed)

    remaining = [TARGET_AGREEMENT] * LIST_SIZE
    pair_counts = {pair_key(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    masks: list[int] = []
    state = seed ^ 0xA327E
    for pos, size in enumerate(sizes):
        future_coordinates = len(sizes) - pos - 1
        candidates = []
        for combo in itertools.combinations(range(LIST_SIZE), size):
            state = lcg(state)
            candidates.append(
                (
                    score_combo(
                        combo,
                        remaining,
                        pair_counts,
                        future_coordinates,
                        mode,
                        target_pair,
                        state,
                    ),
                    combo,
                )
            )
        candidates.sort(key=lambda item: item[0])
        best_score, best_combo = candidates[0]
        if best_score[0] == float("inf"):
            raise RuntimeError(f"no feasible incidence move at coordinate {pos}")
        for item in best_combo:
            remaining[item] -= 1
        for i, j in itertools.combinations(best_combo, 2):
            pair_counts[pair_key(i, j)] += 1
        masks.append(mask_from_combo(best_combo))

    if any(remaining):
        raise RuntimeError(f"failed to use all incidence stubs: {remaining}")
    summary = summarize_masks(masks)
    if summary["min_support_size"] != TARGET_AGREEMENT:
        raise RuntimeError("support size target not met")
    if summary["max_pair_intersection"] > PAIR_CAP:
        raise RuntimeError("pair cap exceeded")
    return masks


def incidence_masks_with_retries(seed: int, mode: str, target_pair: str | None = None) -> list[int]:
    for attempt in range(64):
        try:
            return incidence_masks(seed + 7919 * attempt, mode, target_pair)
        except RuntimeError:
            continue
    raise RuntimeError(f"failed to build incidence design for mode={mode} target_pair={target_pair}")


def candidate_designs() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for variant in range(6):
        seed = 0x450000 + variant
        masks = incidence_masks_with_retries(seed, "balanced_45_regular")
        candidates.append(
            {
                "candidate_id": f"balanced_45_regular_{variant:02d}",
                "family": "balanced_45_regular",
                "seed": seed,
                "membership_masks": masks,
                "summary": summarize_masks(masks),
            }
        )

    for variant in range(4):
        seed = 0x470000 + variant
        masks = incidence_masks_with_retries(seed, "quotient_fiber_balanced")
        candidates.append(
            {
                "candidate_id": f"quotient_fiber_balanced_{variant:02d}",
                "family": "quotient_fiber_balanced",
                "seed": seed,
                "membership_masks": masks,
                "summary": summarize_masks(masks),
            }
        )

    for variant in range(4):
        seed = 0x480000 + variant
        masks = incidence_masks_with_retries(seed, "anti_anchor_balanced")
        candidates.append(
            {
                "candidate_id": f"anti_anchor_balanced_{variant:02d}",
                "family": "anti_anchor_balanced",
                "seed": seed,
                "membership_masks": masks,
                "summary": summarize_masks(masks),
            }
        )
    return candidates


def build_record(rank_results: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    candidates = candidate_designs()
    best = None
    status = "PARTIAL"
    if rank_results is not None:
        if len(rank_results) != len(candidates):
            raise ValueError("rank result count mismatch")
        best = max(
            rank_results,
            key=lambda row: (
                row["proxy_nullity"],
                -row["proxy_rank"],
                row["max_pair_intersection"],
            ),
        )
        status = "CANDIDATE" if best["proxy_nullity"] > 0 else "TESTED_DESIGNS_NO_PROXY_NULLITY"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "valueclass_first",
        "candidate_count": len(candidates),
        "candidate_families": {
            family: sum(1 for item in candidates if item["family"] == family)
            for family in sorted({item["family"] for item in candidates})
        },
        "candidate_design_hash": hash_payload(candidates),
        "design_constraints": {
            "support_size": TARGET_AGREEMENT,
            "pair_cap": PAIR_CAP,
            "membership_histogram": {"4": SIZE_FOUR_COUNT, "5": SIZE_FIVE_COUNT},
        },
        "rank_gate": {
            "status": "SAGE_PROXY_RANKED" if rank_results is not None else "NOT_RUN",
            "proxy_field": "GF(12289)",
            "exact_field": "GF(17^32)",
            "exact_trigger": "proxy_nullity > 0",
            "result_count": 0 if rank_results is None else len(rank_results),
            "best": best,
            "results": [] if rank_results is None else rank_results,
        },
        "proof_status": status,
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
