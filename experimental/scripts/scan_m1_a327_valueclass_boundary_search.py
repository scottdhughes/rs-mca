#!/usr/bin/env python3
"""Boundary-stressed value-class designs for the M1 a=327 witness search."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from numbers import Integral
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_a327_valueclass_boundary_search.json")

N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
SIZE_FIVE_COUNT = 241
SIZE_FOUR_COUNT = 271
PAIR_CAP = K - 1
BOUNDARY_PAIR_SIZE = PAIR_CAP
RETAINED_PROXY_COUNT = 20


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


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


def quotient_fibers() -> list[list[int]]:
    return [[residue + 16 * offset for offset in range(32)] for residue in range(16)]


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
        "pairs_at_255": sum(1 for value in pair_values if value == PAIR_CAP),
        "pairs_at_or_above_250": sum(1 for value in pair_values if value >= 250),
        "pairs_at_or_above_245": sum(1 for value in pair_values if value >= 245),
        "pair_boundary_score": sum(max(0, value - 245) for value in pair_values),
    }


def quotient_fiber_profile(masks: list[int]) -> dict[str, Any]:
    profile = []
    for fiber_id, positions in enumerate(quotient_fibers()):
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


def boundary_positions(seed: int, family: str) -> list[int]:
    if family == "pair_boundary_45":
        return shuffled(list(range(N)), seed)[:BOUNDARY_PAIR_SIZE]

    fibers = quotient_fibers()
    fiber_order = shuffled(list(range(16)), seed ^ 0x5151)
    positions: list[int] = []
    if family == "quotient_fiber_45":
        for fiber in fiber_order[:7]:
            positions.extend(fibers[fiber])
        residual_fiber = fiber_order[7]
        positions.extend(shuffled(fibers[residual_fiber], seed ^ 0x6161)[:31])
    elif family == "boundary_residual_45":
        for fiber in fiber_order[:6]:
            positions.extend(fibers[fiber])
        residual_sizes = [16, 16, 16, 15]
        for fiber, size in zip(fiber_order[6:10], residual_sizes, strict=True):
            positions.extend(shuffled(fibers[fiber], seed ^ (0x7171 + fiber))[:size])
    else:
        raise ValueError(f"unknown family: {family}")

    if len(positions) != BOUNDARY_PAIR_SIZE:
        raise RuntimeError("wrong boundary size")
    if len(set(positions)) != BOUNDARY_PAIR_SIZE:
        raise RuntimeError("duplicate boundary positions")
    return positions


def add_combo(
    combo: tuple[int, ...],
    remaining: list[int],
    pair_counts: dict[str, int],
) -> int:
    if any(remaining[item] <= 0 for item in combo):
        raise RuntimeError("support degree underflow")
    if any(pair_counts[pair_key(i, j)] >= PAIR_CAP for i, j in itertools.combinations(combo, 2)):
        raise RuntimeError("pair cap exceeded")
    for item in combo:
        remaining[item] -= 1
    for i, j in itertools.combinations(combo, 2):
        pair_counts[pair_key(i, j)] += 1
    return mask_from_combo(combo)


def build_boundary_masks(
    seed: int,
    family: str,
    clique: tuple[int, int, int],
    boundary_five_count: int,
) -> list[int]:
    boundary = set(boundary_positions(seed, family))
    rest = [pos for pos in range(N) if pos not in boundary]
    if not (0 <= boundary_five_count <= SIZE_FIVE_COUNT):
        raise ValueError("bad boundary_five_count")

    masks: list[int | None] = [None] * N
    sizes: dict[int, int] = {}
    boundary_fives = set(shuffled(list(boundary), seed ^ 0xA45)[:boundary_five_count])
    for pos in boundary:
        sizes[pos] = 5 if pos in boundary_fives else 4

    remaining_five_count = SIZE_FIVE_COUNT - boundary_five_count
    rest_fives = set(shuffled(rest, seed ^ 0xB45)[:remaining_five_count])
    for pos in rest:
        sizes[pos] = 5 if pos in rest_fives else 4

    remaining = [TARGET_AGREEMENT] * LIST_SIZE
    pair_counts = {pair_key(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    non_clique = [idx for idx in range(LIST_SIZE) if idx not in clique]

    single_extra_counts = {idx: 0 for idx in non_clique}
    pair_extra_counts = {pair: 0 for pair in itertools.combinations(non_clique, 2)}

    for pos in shuffled([pos for pos in boundary if sizes[pos] == 4], seed ^ 0xC45):
        extra = min(non_clique, key=lambda idx: (single_extra_counts[idx], idx))
        single_extra_counts[extra] += 1
        combo = tuple(sorted((*clique, extra)))
        masks[pos] = add_combo(combo, remaining, pair_counts)

    for pos in shuffled([pos for pos in boundary if sizes[pos] == 5], seed ^ 0xD45):
        best_pair = None
        best_score = None
        for pair in itertools.combinations(non_clique, 2):
            combo = tuple(sorted((*clique, *pair)))
            if any(remaining[item] <= 0 for item in combo):
                continue
            if any(pair_counts[pair_key(i, j)] >= PAIR_CAP for i, j in itertools.combinations(combo, 2)):
                continue
            score = sum(single_extra_counts[item] for item in pair) + 4 * pair_extra_counts[pair]
            if best_score is None or score < best_score:
                best_score = score
                best_pair = pair
        if best_pair is None:
            raise RuntimeError("failed to choose boundary size-5 extras")
        for item in best_pair:
            single_extra_counts[item] += 1
        pair_extra_counts[best_pair] += 1
        combo = tuple(sorted((*clique, *best_pair)))
        masks[pos] = add_combo(combo, remaining, pair_counts)

    rest_size5 = shuffled([pos for pos in rest if sizes[pos] == 5], seed ^ 0xE45)
    for pos in rest_size5:
        target = max(clique, key=lambda idx: (remaining[idx], -idx))
        combo = tuple(sorted((target, *non_clique)))
        masks[pos] = add_combo(combo, remaining, pair_counts)

    rest_size4 = shuffled([pos for pos in rest if sizes[pos] == 4], seed ^ 0xF45)
    target_four_needed = sum(remaining[idx] for idx in clique)
    omit_needed = {idx: len(rest_size4) - remaining[idx] for idx in non_clique}
    if sum(omit_needed.values()) != target_four_needed:
        raise RuntimeError("inconsistent residual omission count")

    for pos in rest_size4:
        if sum(remaining[idx] for idx in clique) > 0:
            target = max(clique, key=lambda idx: (remaining[idx], -idx))
            best = None
            for omitted in non_clique:
                if omit_needed[omitted] <= 0:
                    continue
                combo = tuple(sorted([target, *[idx for idx in non_clique if idx != omitted]]))
                if any(remaining[item] <= 0 for item in combo):
                    continue
                if any(pair_counts[pair_key(i, j)] >= PAIR_CAP for i, j in itertools.combinations(combo, 2)):
                    continue
                projected = [pair_counts[pair_key(i, j)] + 1 for i, j in itertools.combinations(combo, 2)]
                omission_balance = sum(value * value for value in omit_needed.values())
                score = max(projected) + 0.01 * omission_balance - 0.1 * omit_needed[omitted]
                if best is None or score < best[0]:
                    best = (score, omitted, combo)
            if best is None:
                raise RuntimeError("failed to choose residual target-four combo")
            _, omitted, combo = best
            omit_needed[omitted] -= 1
        else:
            combo = tuple(non_clique)
        masks[pos] = add_combo(combo, remaining, pair_counts)

    if any(remaining):
        raise RuntimeError(f"support degrees not exhausted: {remaining}")
    if any(value for value in omit_needed.values()):
        raise RuntimeError(f"residual omissions not exhausted: {omit_needed}")
    if any(mask is None for mask in masks):
        raise RuntimeError("unassigned coordinate")

    final_masks = [int(mask) for mask in masks]
    summary = summarize_masks(final_masks)
    if summary["support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
        raise RuntimeError("support size target not met")
    if summary["max_pair_intersection"] > PAIR_CAP:
        raise RuntimeError("pair cap exceeded")
    return final_masks


def candidate_designs() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    cliques = list(itertools.combinations(range(LIST_SIZE), 3))

    for family, boundary_fives, clique_limit in [
        ("pair_boundary_45", [64, 120], 35),
        ("quotient_fiber_45", [64, 160], 35),
        ("boundary_residual_45", [96, 200], 30),
    ]:
        for clique_index, clique in enumerate(cliques[:clique_limit]):
            for five_count in boundary_fives:
                seed = 0xA327000 + 100_000 * len(candidates) + 997 * five_count + clique_index
                masks = build_boundary_masks(seed, family, clique, five_count)
                summary = summarize_masks(masks)
                candidates.append(
                    {
                        "candidate_id": f"{family}_c{clique_index:02d}_b5_{five_count:03d}",
                        "family": family,
                        "seed": seed,
                        "target_clique": list(clique),
                        "boundary_size": BOUNDARY_PAIR_SIZE,
                        "boundary_five_count": five_count,
                        "membership_masks": masks,
                        "summary": summary,
                        "quotient_fiber_profile_hash": quotient_fiber_profile(masks)["profile_hash"],
                    }
                )

    if len(candidates) != 200:
        raise RuntimeError(f"expected 200 candidates, got {len(candidates)}")
    return candidates


def rank_result_key(row: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    return (
        row["proxy_nullity"],
        -row["proxy_rank"],
        row["pairs_at_255"],
        row["pairs_at_or_above_250"],
        row["pairs_at_or_above_245"],
        row["pair_boundary_score"],
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

    families = sorted({candidate["family"] for candidate in candidates})
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "valueclass_boundary_search",
        "candidate_count": len(candidates),
        "candidate_families": {
            family: sum(1 for item in candidates if item["family"] == family)
            for family in families
        },
        "candidate_design_hash": hash_payload(candidates),
        "design_constraints": {
            "support_size": TARGET_AGREEMENT,
            "pair_cap": PAIR_CAP,
            "boundary_pair_size": BOUNDARY_PAIR_SIZE,
            "membership_sizes": [4, 5],
        },
        "rank_gate": {
            "status": "SAGE_PROXY_RANKED" if rank_results is not None else "NOT_RUN",
            "proxy_field": "GF(12289)",
            "exact_field": "GF(17^32)",
            "exact_trigger": "proxy_nullity > 0",
            "all_result_count": 0 if rank_results is None else len(rank_results),
            "retained_proxy_count": len(retained),
            "proxy_positive_count": proxy_positive_count,
            "best": best,
            "retained_results": retained,
            "all_result_hash": None if rank_results is None else hash_payload(rank_results),
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
