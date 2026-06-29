#!/usr/bin/env python3
"""Pairwise-divisibility null-vector systems for M1 a=327."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from itertools import combinations
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_a327_pairwise_divisibility_nullvector_system.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
TARGET_BITS = 128
CURRENT_PR_133_AGREEMENT = 326
CURRENT_PR_133_LAMBDA_LOWER = 7
FIELD_DENOMINATOR = P**FIELD_DEGREE
SURROGATE_FIELD_SIZE = 12289
GENERATED_CANDIDATES = 48
RANK_SCREEN_CANDIDATES = 12
RETAINED_CANDIDATES = 6
RANDOM_SEED = 2026062804


# Filled from the Sage audit after retained candidate identities are fixed.
# The scanner is dependency-free; Sage is the exact GF(17^32) rank source.
PRECOMPUTED_EXACT_RANKS: dict[str, dict[str, Any]] = {
    "balanced_clique_m2_o1": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 179,
        "rank": 179,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 49, "2": 24, "3": 27, "4": 21, "5": 12, "6": 46},
        "remaining_pairwise_equations": 3251,
        "remaining_equations_by_pair": {
            "1,2": 207,
            "1,3": 218,
            "1,4": 186,
            "1,5": 235,
            "1,6": 245,
            "2,3": 213,
            "2,4": 229,
            "2,5": 212,
            "2,6": 226,
            "3,4": 210,
            "3,5": 225,
            "3,6": 217,
            "4,5": 189,
            "4,6": 249,
            "5,6": 190,
        },
        "matrix_metadata_hash": "b1dadb8a93eb5d76e4ec240a69c83fd4f0f523532ab7c41dbbb8a5bc5b9164e0",
        "status": "RANK_COMPUTED",
    },
    "balanced_clique_m6_o1": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 205,
        "rank": 205,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 5, "2": 35, "3": 43, "4": 50, "5": 31, "6": 41},
        "remaining_pairwise_equations": 3277,
        "remaining_equations_by_pair": {
            "1,2": 232,
            "1,3": 204,
            "1,4": 205,
            "1,5": 188,
            "1,6": 222,
            "2,3": 206,
            "2,4": 215,
            "2,5": 232,
            "2,6": 208,
            "3,4": 249,
            "3,5": 222,
            "3,6": 224,
            "4,5": 223,
            "4,6": 215,
            "5,6": 232,
        },
        "matrix_metadata_hash": "0959dcb1db0842d8e668526fc159147dddee590e81fcce31d7b345fca36b045a",
        "status": "RANK_COMPUTED",
    },
    "balanced_clique_m5_o1": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 205,
        "rank": 205,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 51, "2": 15, "3": 17, "4": 45, "5": 18, "6": 59},
        "remaining_pairwise_equations": 3277,
        "remaining_equations_by_pair": {
            "1,2": 214,
            "1,3": 222,
            "1,4": 224,
            "1,5": 223,
            "1,6": 224,
            "2,3": 194,
            "2,4": 238,
            "2,5": 205,
            "2,6": 234,
            "3,4": 196,
            "3,5": 227,
            "3,6": 236,
            "4,5": 211,
            "4,6": 226,
            "5,6": 203,
        },
        "matrix_metadata_hash": "7d54bb69fa18f95d8534d246a808d97312b0ecd4df96e2acb7264b92fdf5ed63",
        "status": "RANK_COMPUTED",
    },
    "balanced_clique_m2_o0": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 206,
        "rank": 206,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 39, "2": 41, "3": 25, "4": 37, "5": 9, "6": 55},
        "remaining_pairwise_equations": 3278,
        "remaining_equations_by_pair": {
            "1,2": 196,
            "1,3": 238,
            "1,4": 206,
            "1,5": 218,
            "1,6": 246,
            "2,3": 212,
            "2,4": 254,
            "2,5": 214,
            "2,6": 222,
            "3,4": 198,
            "3,5": 214,
            "3,6": 222,
            "4,5": 214,
            "4,6": 222,
            "5,6": 202,
        },
        "matrix_metadata_hash": "c06a4e283897b7b60a61dbdbe673637bb939d8b231da3010153f4b81369eb1e0",
        "status": "RANK_COMPUTED",
    },
    "balanced_clique_m6_o0": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 214,
        "rank": 214,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 2, "2": 60, "3": 42, "4": 44, "5": 48, "6": 18},
        "remaining_pairwise_equations": 3286,
        "remaining_equations_by_pair": {
            "1,2": 230,
            "1,3": 190,
            "1,4": 214,
            "1,5": 206,
            "1,6": 222,
            "2,3": 252,
            "2,4": 224,
            "2,5": 208,
            "2,6": 212,
            "3,4": 234,
            "3,5": 212,
            "3,6": 216,
            "4,5": 242,
            "4,6": 194,
            "5,6": 230,
        },
        "matrix_metadata_hash": "af5704490f49d175caa196e161978a46a66356ecd986c76b31d44311c5c785fa",
        "status": "RANK_COMPUTED",
    },
    "balanced_clique_m1_o0": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 217,
        "rank": 217,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 14, "2": 44, "3": 42, "4": 41, "5": 59, "6": 17},
        "remaining_pairwise_equations": 3289,
        "remaining_equations_by_pair": {
            "1,2": 236,
            "1,3": 216,
            "1,4": 203,
            "1,5": 211,
            "1,6": 199,
            "2,3": 254,
            "2,4": 215,
            "2,5": 191,
            "2,6": 207,
            "3,4": 215,
            "3,5": 231,
            "3,6": 197,
            "4,5": 236,
            "4,6": 226,
            "5,6": 252,
        },
        "matrix_metadata_hash": "1b770f5aaf1cc84f0626a2398a4eeaa1f010c77c5945cfae746569a505f6d307",
        "status": "RANK_COMPUTED",
    },
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def primitive_root_prime(prime: int) -> int:
    factors = []
    value = prime - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise RuntimeError(f"no primitive root found for {prime}")


def subgroup_points_mod_prime() -> list[int]:
    generator = primitive_root_prime(SURROGATE_FIELD_SIZE)
    subgroup_generator = pow(generator, (SURROGATE_FIELD_SIZE - 1) // N, SURROGATE_FIELD_SIZE)
    points = [pow(subgroup_generator, idx, SURROGATE_FIELD_SIZE) for idx in range(N)]
    assert len(set(points)) == N
    return points


H_SURROGATE = subgroup_points_mod_prime()


def normalize_partition(partition: list[list[int]]) -> list[list[int]]:
    return sorted([sorted(block) for block in partition if len(block) >= 2])


def partition_from_permutation(perm: list[int], sizes: list[int]) -> list[list[int]]:
    out = []
    start = 0
    for size in sizes:
        block = perm[start : start + size]
        if len(block) >= 2:
            out.append(sorted(block))
        start += size
    return normalize_partition(out)


def affine_permutation(pos: int, multiplier: int, offset: int, salt: int) -> list[int]:
    base = [(multiplier * idx + offset + salt) % LIST_SIZE for idx in range(LIST_SIZE)]
    shift = (pos + 3 * salt) % LIST_SIZE
    return base[shift:] + base[:shift]


def balanced_clique_partitions(multiplier: int, offset: int, salt: int) -> list[list[list[int]]]:
    rng = random.Random(RANDOM_SEED + 101 * multiplier + 17 * offset + salt)
    partitions = []
    for pos in range(N):
        perm = list(range(LIST_SIZE))
        rng.shuffle(perm)
        if pos % 13 == 0:
            perm = affine_permutation(pos, multiplier, offset + (pos // 23), salt)
        sizes = [4, 3] if ((pos + salt) % 2 == 0) else [3, 4]
        partitions.append(partition_from_permutation(perm, sizes))
    return partitions


def quotient_fiber_pairwise_partitions(multiplier: int, offset: int, defect: int) -> list[list[list[int]]]:
    rng = random.Random(RANDOM_SEED + 1009 * multiplier + 53 * offset + defect)
    fiber_patterns: list[list[list[int]]] = []
    for fiber in range(16):
        perm = list(range(LIST_SIZE))
        rng.shuffle(perm)
        if fiber % 5 == 0:
            perm = affine_permutation(fiber, multiplier, offset + defect * fiber, defect)
        sizes = [4, 3] if (fiber + defect) % 3 else [3, 2, 2]
        fiber_patterns.append(partition_from_permutation(perm, sizes))
    partitions = []
    for pos in range(N):
        pattern = [block[:] for block in fiber_patterns[pos % 16]]
        if (pos // 16 + defect) % 11 == 0:
            perm = affine_permutation(pos, multiplier, offset + pos // 16, defect + 5)
            pattern = partition_from_permutation(perm, [3, 4])
        partitions.append(pattern)
    return partitions


def pair_boundary_partitions(pair_a: tuple[int, int], pair_b: tuple[int, int], salt: int) -> list[list[list[int]]]:
    rng = random.Random(RANDOM_SEED + 97 * salt)
    partitions = []
    for pos in range(N):
        perm = list(range(LIST_SIZE))
        rng.shuffle(perm)
        if pos % 5 in {0, 1}:
            rest = [idx for idx in perm if idx not in pair_a]
            block = sorted([pair_a[0], pair_a[1], rest[0], rest[1]])
            other = sorted([idx for idx in range(LIST_SIZE) if idx not in block])
            pattern = [block, other]
        elif pos % 7 in {0, 3}:
            rest = [idx for idx in perm if idx not in pair_b]
            block = sorted([pair_b[0], pair_b[1], rest[0]])
            other = sorted([idx for idx in range(LIST_SIZE) if idx not in block])
            pattern = [block, other]
        else:
            pattern = partition_from_permutation(perm, [3, 2, 2])
        partitions.append(normalize_partition(pattern))
    return partitions


def mixed_clique_partitions(multiplier: int, offset: int, salt: int) -> list[list[list[int]]]:
    rng = random.Random(RANDOM_SEED + 2003 * multiplier + 71 * offset + salt)
    partitions = []
    for pos in range(N):
        perm = list(range(LIST_SIZE))
        rng.shuffle(perm)
        if pos % 17 == 0:
            perm = affine_permutation(pos + (pos // 16), multiplier, offset, salt)
        mode = (pos + 2 * (pos // 16) + salt) % 6
        if mode in {0, 1}:
            sizes = [4, 3]
        elif mode in {2, 3}:
            sizes = [3, 2, 2]
        elif mode == 4:
            sizes = [2, 3, 2]
        else:
            sizes = [2, 2, 3]
        partitions.append(partition_from_permutation(perm, sizes))
    return partitions


def pair_label(pair: tuple[int, int]) -> str:
    return f"{pair[0]},{pair[1]}"


def pair_positions(partitions: list[list[list[int]]]) -> dict[tuple[int, int], list[int]]:
    positions: dict[tuple[int, int], list[int]] = {
        pair: [] for pair in combinations(range(LIST_SIZE), 2)
    }
    for pos, partition in enumerate(partitions):
        for block in partition:
            for i, j in combinations(block, 2):
                positions[(i, j)].append(pos)
    return positions


def equality_summary(partitions: list[list[list[int]]]) -> dict[str, Any]:
    pairs = pair_positions(partitions)
    pair_counts = {pair_label(pair): len(values) for pair, values in pairs.items()}
    pair_values = sorted(pair_counts.values())
    incidence = [0 for _idx in range(LIST_SIZE)]
    block_size_histogram: dict[str, int] = {}
    partition_histogram: dict[str, int] = {}
    for partition in partitions:
        covered: set[int] = set()
        for block in partition:
            block_size_histogram[str(len(block))] = block_size_histogram.get(str(len(block)), 0) + 1
            covered.update(block)
        for witness in covered:
            incidence[witness] += 1
        key = json.dumps(normalize_partition(partition), sort_keys=True, separators=(",", ":"))
        partition_histogram[key] = partition_histogram.get(key, 0) + 1
    quotient_profiles = []
    for fiber in range(16):
        hist: dict[str, int] = {}
        for pos in range(fiber, N, 16):
            key = json.dumps(normalize_partition(partitions[pos]), sort_keys=True, separators=(",", ":"))
            hist[key] = hist.get(key, 0) + 1
        quotient_profiles.append(
            {
                "fiber": fiber,
                "distinct_patterns": len(hist),
                "largest_pattern_multiplicity": max(hist.values()),
            }
        )
    return {
        "coordinate_count": N,
        "min_witness_equality_incidence": min(incidence),
        "witness_equality_incidences": incidence,
        "pair_equality_counts": dict(sorted(pair_counts.items())),
        "pair_equality_values": pair_values,
        "max_pair_equality_size": max(pair_values),
        "pair_equalities_at_255": sum(1 for value in pair_values if value == 255),
        "pair_equality_sum": sum(pair_values),
        "block_size_histogram": dict(sorted(block_size_histogram.items())),
        "partition_pattern_count": len(partition_histogram),
        "partition_pattern_histogram_hash": hash_payload(partition_histogram),
        "quotient_fiber_profile": quotient_profiles,
        "equality_pattern_hash": hash_payload([normalize_partition(partition) for partition in partitions]),
    }


def is_valid_pairwise_design(summary: dict[str, Any]) -> bool:
    return (
        summary["min_witness_equality_incidence"] >= TARGET_AGREEMENT
        and summary["max_pair_equality_size"] <= K - 1
        and all(summary["pair_equality_counts"][f"0,{idx}"] < K for idx in range(1, LIST_SIZE))
    )


def compressed_variable_count(summary: dict[str, Any]) -> int:
    return sum(K - summary["pair_equality_counts"][f"0,{idx}"] for idx in range(1, LIST_SIZE))


def structural_score(summary: dict[str, Any]) -> dict[str, Any]:
    compressed = compressed_variable_count(summary)
    pair_values = summary["pair_equality_values"]
    boundary_pressure = sum(max(0, value - 248) for value in pair_values)
    balance_penalty = max(pair_values) - min(pair_values)
    score = (
        20 * summary["pair_equalities_at_255"]
        + boundary_pressure
        + summary["min_witness_equality_incidence"] // 8
        - compressed // 16
        - balance_penalty // 8
    )
    return {
        "method": "pairwise_divisibility_structural_screen",
        "compressed_variables_estimate": compressed,
        "boundary_pressure": boundary_pressure,
        "pair_balance_penalty": balance_penalty,
        "score": score,
        "status": "SCORED",
    }


def locator_values_mod(vanish_positions: list[int]) -> list[int]:
    roots = [H_SURROGATE[pos] for pos in vanish_positions]
    values = []
    for point in H_SURROGATE:
        acc = 1
        for root in roots:
            acc = (acc * (point - root)) % SURROGATE_FIELD_SIZE
        values.append(acc)
    return values


def rank_mod_prime(rows: list[list[int]], modulus: int) -> int:
    pivots: dict[int, list[int]] = {}
    rank = 0
    for input_row in rows:
        row = [value % modulus for value in input_row]
        while True:
            pivot_col = next((idx for idx, value in enumerate(row) if value), None)
            if pivot_col is None:
                break
            if pivot_col not in pivots:
                inv = pow(row[pivot_col], -1, modulus)
                row = [(value * inv) % modulus for value in row]
                pivots[pivot_col] = row
                rank += 1
                break
            pivot = pivots[pivot_col]
            scale = row[pivot_col]
            row = [(value - scale * pivot[idx]) % modulus for idx, value in enumerate(row)]
    return rank


def surrogate_rank_gate(partitions: list[list[list[int]]]) -> dict[str, Any]:
    pairs = pair_positions(partitions)
    witness_dims: dict[str, int] = {}
    witness_offsets: dict[int, int] = {}
    locator_eval: dict[int, list[int]] = {}
    ambient_dimension = 0
    for witness in range(1, LIST_SIZE):
        vanish = pairs[(0, witness)]
        dim = K - len(vanish)
        if dim <= 0:
            return {
                "field_mode": "surrogate",
                "field_label": "GF(12289)_surrogate",
                "field_size": str(SURROGATE_FIELD_SIZE),
                "compressed_variables": 0,
                "rank": None,
                "nullity": None,
                "status": "ANCHOR_EQUALITY_TOO_LARGE",
            }
        witness_dims[str(witness)] = dim
        witness_offsets[witness] = ambient_dimension
        ambient_dimension += dim
        locator_eval[witness] = locator_values_mod(vanish)

    rows: list[list[int]] = []
    remaining_by_pair: dict[str, int] = {}
    for i in range(1, LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            positions = pairs[(i, j)]
            remaining_by_pair[pair_label((i, j))] = len(positions)
            dim_i = witness_dims[str(i)]
            dim_j = witness_dims[str(j)]
            off_i = witness_offsets[i]
            off_j = witness_offsets[j]
            for pos in positions:
                point = H_SURROGATE[pos]
                row = [0 for _idx in range(ambient_dimension)]
                power = 1
                scale_i = locator_eval[i][pos]
                for degree in range(dim_i):
                    row[off_i + degree] = (scale_i * power) % SURROGATE_FIELD_SIZE
                    power = (power * point) % SURROGATE_FIELD_SIZE
                power = 1
                scale_j = locator_eval[j][pos]
                for degree in range(dim_j):
                    row[off_j + degree] = (row[off_j + degree] - scale_j * power) % SURROGATE_FIELD_SIZE
                    power = (power * point) % SURROGATE_FIELD_SIZE
                rows.append(row)

    rank = rank_mod_prime(rows, SURROGATE_FIELD_SIZE)
    nullity = ambient_dimension - rank
    return {
        "field_mode": "surrogate",
        "field_label": "GF(12289)_surrogate",
        "field_size": str(SURROGATE_FIELD_SIZE),
        "compressed_variables": ambient_dimension,
        "rank": rank,
        "nullity": nullity,
        "non_diagonal_solution_found": nullity > 0,
        "compressed_dimensions_by_witness": witness_dims,
        "remaining_pairwise_equations": len(rows),
        "remaining_equations_by_pair": remaining_by_pair,
        "matrix_metadata_hash": hash_payload(
            {
                "field_mode": "surrogate",
                "witness_dims": witness_dims,
                "remaining_equations_by_pair": remaining_by_pair,
                "equality_pattern_hash": equality_summary(partitions)["equality_pattern_hash"],
            }
        ),
        "status": "RANK_COMPUTED",
    }


def generated_candidate_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for idx, multiplier in enumerate([1, 2, 3, 4, 5, 6]):
        for offset in range(2):
            specs.append(
                {
                    "candidate_id": f"balanced_clique_m{multiplier}_o{offset}",
                    "family": "balanced_clique_blocks",
                    "partitions": balanced_clique_partitions(multiplier, offset, idx),
                }
            )
    for idx, multiplier in enumerate([1, 2, 3, 4, 5, 6]):
        for defect in range(3):
            specs.append(
                {
                    "candidate_id": f"quotient_fiber_m{multiplier}_d{defect}",
                    "family": "quotient_fiber_pairwise_blocks",
                    "partitions": quotient_fiber_pairwise_partitions(multiplier, idx, defect),
                }
            )
    pair_list = list(combinations(range(LIST_SIZE), 2))
    for idx in range(10):
        specs.append(
            {
                "candidate_id": f"pair_boundary_{idx:02d}",
                "family": "pair_boundary_design",
                "partitions": pair_boundary_partitions(
                    pair_list[(3 * idx) % len(pair_list)],
                    pair_list[(3 * idx + 8) % len(pair_list)],
                    idx,
                ),
            }
        )
    for idx, multiplier in enumerate([1, 2, 3, 4, 5, 6, 1, 2]):
        specs.append(
            {
                "candidate_id": f"mixed_clique_{idx:02d}",
                "family": "mixed_clique_design",
                "partitions": mixed_clique_partitions(multiplier, 2 * idx, idx + 11),
            }
        )
    assert len(specs) == GENERATED_CANDIDATES
    return specs


def generated_candidates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in generated_candidate_specs():
        partitions = spec["partitions"]
        summary = equality_summary(partitions)
        if not is_valid_pairwise_design(summary):
            continue
        rows.append(
            {
                "candidate_id": spec["candidate_id"],
                "construction_family": spec["family"],
                "construction_mode": "pairwise_divisibility_nullvector",
                "equality_partitions": partitions,
                "equality_design": summary,
                "structural_score": structural_score(summary),
            }
        )
    return rows


def structurally_screened_candidates() -> list[dict[str, Any]]:
    rows = generated_candidates()
    rows.sort(
        key=lambda row: (
            row["structural_score"]["score"],
            row["equality_design"]["pair_equalities_at_255"],
            -row["structural_score"]["compressed_variables_estimate"],
            row["equality_design"]["min_witness_equality_incidence"],
            row["candidate_id"],
        ),
        reverse=True,
    )
    return rows[:RANK_SCREEN_CANDIDATES]


def retained_candidates() -> list[dict[str, Any]]:
    rows = []
    for row in structurally_screened_candidates():
        ranked = dict(row)
        ranked["surrogate_rank_gate"] = surrogate_rank_gate(row["equality_partitions"])
        rows.append(ranked)
    rows.sort(
        key=lambda row: (
            row["surrogate_rank_gate"]["nullity"] or 0,
            -row["surrogate_rank_gate"]["rank"],
            row["structural_score"]["score"],
            row["candidate_id"],
        ),
        reverse=True,
    )
    return rows[:RETAINED_CANDIDATES]


def exact_rank_from_precomputed(candidate_id: str) -> dict[str, Any]:
    computed = PRECOMPUTED_EXACT_RANKS.get(candidate_id)
    if computed is None:
        return {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": str(FIELD_DENOMINATOR),
            "rank": None,
            "nullity": None,
            "status": "NOT_RUN",
        }
    return computed


def build_candidates() -> list[dict[str, Any]]:
    rows = []
    for candidate in retained_candidates():
        exact_gate = exact_rank_from_precomputed(candidate["candidate_id"])
        if exact_gate.get("nullity") == 0:
            proof_status = "ROUTE_CUT_TESTED_CANDIDATE"
        elif exact_gate.get("nullity") not in {None, 0}:
            proof_status = "CANDIDATE"
        elif candidate["surrogate_rank_gate"].get("nullity") not in {None, 0}:
            proof_status = "CANDIDATE_PROXY_NULLITY"
        else:
            proof_status = "CANDIDATE"
        row = {key: value for key, value in candidate.items() if key != "equality_partitions"}
        row.update(
            {
                "sage_exact_rank": exact_gate,
                "extraction": {
                    "non_diagonal_solution_found": False,
                    "agreement_verified": False,
                    "status": "NOT_RUN",
                },
                "proof_status": proof_status,
            }
        )
        rows.append(row)
    return rows


def build_result() -> dict[str, Any]:
    generated = generated_candidates()
    candidates = build_candidates()
    exact_rows = [row for row in candidates if row["sage_exact_rank"]["status"] != "NOT_RUN"]
    best_exact_nullity = max((row["sage_exact_rank"]["nullity"] or 0 for row in exact_rows), default=None)
    proxy_positive_count = sum(
        1 for row in candidates if row["surrogate_rank_gate"]["nullity"] not in {None, 0}
    )
    family_counts: dict[str, int] = {}
    retained_family_counts: dict[str, int] = {}
    for row in generated:
        family_counts[row["construction_family"]] = family_counts.get(row["construction_family"], 0) + 1
    for row in candidates:
        retained_family_counts[row["construction_family"]] = (
            retained_family_counts.get(row["construction_family"], 0) + 1
        )
    assert threshold_floor() == 6
    if exact_rows and best_exact_nullity == 0:
        status = "ROUTE_CUT_TESTED_CANDIDATES"
    elif proxy_positive_count:
        status = "CANDIDATE_PROXY_NULLITY"
    else:
        status = "PARTIAL"

    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "denominator": "17^32",
        "field_denominator": str(FIELD_DENOMINATOR),
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "agreement_target": TARGET_AGREEMENT,
        "baseline": {
            "current_pr_133_agreement": CURRENT_PR_133_AGREEMENT,
            "current_pr_133_lambda_lower": CURRENT_PR_133_LAMBDA_LOWER,
            "source": "PR #133 hybrid quotient-residual certificate",
        },
        "construction_mode": "pairwise_divisibility_nullvector",
        "search_summary": {
            "generated_spec_count": GENERATED_CANDIDATES,
            "valid_pairwise_design_count": len(generated),
            "rank_screen_candidate_count": RANK_SCREEN_CANDIDATES,
            "retained_candidate_count": len(candidates),
            "exact_audited_count": len(exact_rows),
            "random_seed": RANDOM_SEED,
            "families": [
                "balanced_clique_blocks",
                "quotient_fiber_pairwise_blocks",
                "pair_boundary_design",
                "mixed_clique_design",
            ],
            "valid_family_counts": dict(sorted(family_counts.items())),
            "retained_family_counts": dict(sorted(retained_family_counts.items())),
            "rank_proxy": "GF(12289) pairwise-divisibility reduced rank",
            "surrogate_field": "GF(12289), 512 | 12288",
            "exact_field": "GF(17^32)",
            "proxy_positive_count": proxy_positive_count,
            "best_exact_nullity": best_exact_nullity,
            "candidate_found": best_exact_nullity not in {0, None},
            "status": status,
        },
        "candidates": candidates,
        "interpretation": {
            "pairwise_equalities_designed_jointly": True,
            "support_packing_only": False,
            "exact_audited_candidate_found_nullity": best_exact_nullity not in {0, None},
            "a327_certificate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "status": status,
        },
        "open_layers": {
            "larger_pairwise_divisibility_systems": True,
            "non_diagonal_nullspace_extraction": True,
            "value_class_max_min_after_positive_nullity": True,
            "two_level_quotient_plus_residual": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_a327_pairwise_divisibility_nullvector_system.sage",
            "constructs_GF_17_32": True,
            "recomputes_retained_candidates": True,
            "checks_surrogate_rank_gate": True,
            "uses_exact_pairwise_divisibility_rank_gate": True,
            "extracts_codewords_only_if_positive_nullity": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list certificate",
                "PROOF_RECORD lower bound without Sage extraction",
                "exact Lambda_mu",
                "exact delta*_C",
                "global Lambda_mu(C,327) <= 6",
                "global pairwise-divisibility obstruction",
                "improvement over PR #133",
            ],
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": status,
        },
        "status": "M1_A327_PAIRWISE_DIVISIBILITY_NULLVECTOR_SYSTEM_PARTIAL",
    }
    result["record_hash"] = hash_payload(
        {
            "search_summary": result["search_summary"],
            "candidates": result["candidates"],
            "interpretation": result["interpretation"],
            "open": result["open_layers"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_result(), indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--list-candidates", action="store_true")
    args = parser.parse_args()

    if args.list_candidates:
        rows = [
            {
                "candidate_id": row["candidate_id"],
                "family": row["construction_family"],
                "equality_hash": row["equality_design"]["equality_pattern_hash"],
                "structural_score": row["structural_score"]["score"],
                "min_witness_incidence": row["equality_design"]["min_witness_equality_incidence"],
                "max_pair_equality_size": row["equality_design"]["max_pair_equality_size"],
                "pairs_at_255": row["equality_design"]["pair_equalities_at_255"],
                "surrogate_rank": row["surrogate_rank_gate"]["rank"],
                "surrogate_nullity": row["surrogate_rank_gate"]["nullity"],
                "compressed_variables": row["surrogate_rank_gate"]["compressed_variables"],
                "remaining_equations": row["surrogate_rank_gate"]["remaining_pairwise_equations"],
            }
            for row in retained_candidates()
        ]
        print(json.dumps(rows, indent=2, sort_keys=True))
        return

    result = build_result()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output)
        print(f"WROTE {args.output}")
        print(f"generated {GENERATED_CANDIDATES} pairwise-divisibility specs")
        print(f"valid pairwise designs: {result['search_summary']['valid_pairwise_design_count']}")
        print(f"retained {len(result['candidates'])} candidates")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
