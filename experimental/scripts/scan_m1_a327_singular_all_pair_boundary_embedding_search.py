#!/usr/bin/env python3
"""Search embeddings of the all-pair-boundary a=327 value-class multiset."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_valueclass_milp_incidence_seeds.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_singular_all_pair_boundary_embedding_search.json")

N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = K - 1
PROXY_PRIME = 12289
RANDOM_EMBEDDINGS = 512


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


def members(mask: int) -> list[int]:
    return [idx for idx in range(LIST_SIZE) if mask & (1 << idx)]


def pair_key(i: int, j: int) -> str:
    if i > j:
        i, j = j, i
    return f"{i},{j}"


def primitive_root_mod_prime(p: int) -> int:
    n = p - 1
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    for candidate in range(2, p):
        if all(pow(candidate, n // factor, p) != 1 for factor in factors):
            return candidate
    raise RuntimeError(f"no primitive root for {p}")


def proxy_subgroup() -> np.ndarray:
    generator = primitive_root_mod_prime(PROXY_PRIME)
    subgroup_generator = pow(generator, (PROXY_PRIME - 1) // N, PROXY_PRIME)
    return np.array([pow(subgroup_generator, idx, PROXY_PRIME) for idx in range(N)], dtype=np.int64)


def bit_reverse(value: int, width: int = 9) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def quotient_fibers() -> list[list[int]]:
    return [[residue + 16 * offset for offset in range(32)] for residue in range(16)]


def fiber_round_robin_order() -> list[int]:
    fibers = quotient_fibers()
    return [fibers[residue][offset] for offset in range(32) for residue in range(16)]


def load_all_pair_sequence() -> tuple[dict[str, Any], list[int]]:
    with SOURCE_DATA_PATH.open() as handle:
        source = json.load(handle)
    profile = next(profile for profile in source["profiles"] if profile["profile_id"] == "all_sizes_max_pairs_at255")
    sequence = []
    for mask, count in sorted(profile["mask_counts"].items(), key=lambda item: (len(members(int(item[0]))), int(item[0]))):
        sequence.extend([int(mask)] * int(count))
    if len(sequence) != N:
        raise RuntimeError("wrong all-pair-boundary sequence length")
    return profile, sequence


def assign_by_order(sequence: list[int], order: list[int]) -> list[int]:
    masks = [0] * N
    for idx, position in enumerate(order):
        masks[position] = sequence[idx]
    return masks


def deterministic_embeddings(sequence: list[int]) -> list[dict[str, Any]]:
    embeddings = [
        {
            "embedding_id": "block",
            "embedding_family": "deterministic",
            "seed": None,
            "membership_masks": assign_by_order(sequence, list(range(N))),
        },
        {
            "embedding_id": "bit_reversal",
            "embedding_family": "deterministic",
            "seed": None,
            "membership_masks": assign_by_order(sequence, [bit_reverse(idx) for idx in range(N)]),
        },
        {
            "embedding_id": "fiber_round_robin",
            "embedding_family": "deterministic",
            "seed": None,
            "membership_masks": assign_by_order(sequence, fiber_round_robin_order()),
        },
    ]
    return embeddings


def random_embeddings(sequence: list[int], count: int = RANDOM_EMBEDDINGS) -> list[dict[str, Any]]:
    embeddings = []
    for idx in range(count):
        seed = 0xA32751A9 + 7919 * idx
        rng = random.Random(seed)
        masks = list(sequence)
        rng.shuffle(masks)
        embeddings.append(
            {
                "embedding_id": f"random_shuffle_{idx:04d}",
                "embedding_family": "random_shuffle",
                "seed": seed,
                "membership_masks": masks,
            }
        )
    return embeddings


def summarize_masks(masks: list[int]) -> dict[str, Any]:
    supports = [0] * LIST_SIZE
    pair_counts = {pair_key(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    histogram: dict[str, int] = {}
    for mask in masks:
        bits = members(mask)
        histogram[str(len(bits))] = histogram.get(str(len(bits)), 0) + 1
        for item in bits:
            supports[item] += 1
        for idx, left in enumerate(bits):
            for right in bits[idx + 1 :]:
                pair_counts[pair_key(left, right)] += 1
    pair_values = list(pair_counts.values())
    return {
        "support_sizes": supports,
        "membership_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "max_pair_intersection": max(pair_values),
        "min_pair_intersection": min(pair_values),
        "pairs_at_255": sum(1 for value in pair_values if value == PAIR_CAP),
        "pairs_at_or_above_250": sum(1 for value in pair_values if value >= 250),
        "pair_intersections": dict(sorted(pair_counts.items())),
    }


def compact_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "support_sizes": summary["support_sizes"],
        "membership_histogram": summary["membership_histogram"],
        "max_pair_intersection": summary["max_pair_intersection"],
        "min_pair_intersection": summary["min_pair_intersection"],
        "pairs_at_255": summary["pairs_at_255"],
        "pairs_at_or_above_250": summary["pairs_at_or_above_250"],
    }


def locator_values_modp(H: np.ndarray, zero_positions: list[int]) -> np.ndarray:
    values = np.ones(N, dtype=np.int64)
    for position in zero_positions:
        values = (values * ((H - int(H[position])) % PROXY_PRIME)) % PROXY_PRIME
    values[zero_positions] = 0
    return values


def modular_rank(rows: list[list[int]], columns: int, p: int) -> tuple[int, list[int]]:
    basis: dict[int, list[int]] = {}
    pivot_rows = []
    for row_idx, row in enumerate(rows):
        vec = [int(value) % p for value in row]
        while True:
            pivot = next((idx for idx, value in enumerate(vec) if value % p), None)
            if pivot is None:
                break
            if pivot not in basis:
                inv = pow(vec[pivot], p - 2, p)
                basis[pivot] = [(value * inv) % p for value in vec]
                pivot_rows.append(row_idx)
                break
            factor = vec[pivot]
            base = basis[pivot]
            vec = [(left - factor * right) % p for left, right in zip(vec, base)]
        if len(basis) == columns:
            break
    return len(basis), pivot_rows


def proxy_rank_for_masks(masks: list[int], H: np.ndarray) -> dict[str, Any]:
    locator_by_witness = {}
    anchor_zero_counts = {}
    for witness in range(1, LIST_SIZE):
        zero_positions = [
            position
            for position, mask in enumerate(masks)
            if (mask & 1) and (mask & (1 << witness))
        ]
        anchor_zero_counts[str(witness)] = len(zero_positions)
        locator_by_witness[witness] = locator_values_modp(H, zero_positions)

    rows = []
    row_type_counts: dict[str, int] = {}
    for left in range(1, LIST_SIZE):
        for right in range(left + 1, LIST_SIZE):
            pair_label = f"{left},{right}"
            for position, mask in enumerate(masks):
                if not ((mask & (1 << left)) and (mask & (1 << right))):
                    continue
                left_value = int(locator_by_witness[left][position])
                right_value = int(locator_by_witness[right][position])
                if left_value == 0 and right_value == 0:
                    continue
                row = [0] * (LIST_SIZE - 1)
                row[left - 1] = left_value
                row[right - 1] = (-right_value) % PROXY_PRIME
                rows.append(row)
                row_type_counts[pair_label] = row_type_counts.get(pair_label, 0) + 1

    rank, pivot_rows = modular_rank(rows, LIST_SIZE - 1, PROXY_PRIME)
    return {
        "compressed_variables": LIST_SIZE - 1,
        "remaining_equations": len(rows),
        "anchor_zero_counts": anchor_zero_counts,
        "row_type_counts": dict(sorted(row_type_counts.items())),
        "proxy_rank": rank,
        "proxy_nullity": LIST_SIZE - 1 - rank,
        "proxy_pivot_rows_count": len(pivot_rows),
        "proxy_pivot_rows_hash": hash_payload(pivot_rows),
        "row_sample_hash": hash_payload(rows[:32]),
    }


def candidate_embeddings() -> list[dict[str, Any]]:
    _profile, sequence = load_all_pair_sequence()
    return deterministic_embeddings(sequence) + random_embeddings(sequence)


def build_record() -> dict[str, Any]:
    source_profile, sequence = load_all_pair_sequence()
    H = proxy_subgroup()
    results = []
    for embedding in candidate_embeddings():
        masks = embedding["membership_masks"]
        summary = summarize_masks(masks)
        if summary["support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
            raise RuntimeError("support size mismatch")
        if summary["pairs_at_255"] != 21:
            raise RuntimeError("all-pair boundary profile lost")
        rank = proxy_rank_for_masks(masks, H)
        results.append(
            {
                "candidate_id": f"all_pair_boundary_{embedding['embedding_id']}",
                "profile_id": "all_sizes_max_pairs_at255",
                "embedding_id": embedding["embedding_id"],
                "embedding_family": embedding["embedding_family"],
                "seed": embedding["seed"],
                "membership_mask_hash": hash_payload(masks),
                "summary": compact_summary(summary),
                **rank,
                "status": "PROXY_SINGULAR" if rank["proxy_nullity"] > 0 else "PROXY_FULL_RANK",
            }
        )

    proxy_singular = [row for row in results if row["proxy_nullity"] > 0]
    best = sorted(results, key=lambda row: (row["proxy_nullity"], -row["proxy_rank"], row["candidate_id"]), reverse=True)[0]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "singular_all_pair_boundary_embedding_search",
        "source": {
            "source_json": str(SOURCE_DATA_PATH),
            "source_profile_id": source_profile["profile_id"],
            "source_profile_mask_count_hash": hash_payload(source_profile["mask_counts"]),
        },
        "candidate_count": len(results),
        "candidate_records_include_membership_masks": False,
        "deterministic_embedding_count": 3,
        "random_embedding_count": RANDOM_EMBEDDINGS,
        "proxy_field": "GF(12289)",
        "exact_field": "GF(17^32)",
        "profile_summary": summarize_masks(sequence),
        "results": results,
        "result_hash": hash_payload(results),
        "proxy_singular_count": len(proxy_singular),
        "proxy_full_rank_count": len(results) - len(proxy_singular),
        "best": best,
        "proof_status": "CANDIDATE" if proxy_singular else "TESTED_EMBEDDINGS_NO_PROXY_SINGULAR",
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
