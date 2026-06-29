#!/usr/bin/env python3
"""Emit the M1 support-pattern surrogate-nullity search checkpoint."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
from itertools import combinations
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_support_pattern_surrogate_nullity_search.json")

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
RETAINED_CANDIDATES = 6


# Filled from the Sage audit.  The scanner is dependency-free; Sage is the
# exact finite-field rank source for these retained candidates.
PRECOMPUTED_RANKS: dict[str, dict[str, Any]] = {
    "pair_boundary_cyclic_3456_near_boundary_seed_202606399": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 360,
            "rank": 360,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 108, "2": 6, "3": 61, "4": 74, "5": 1, "6": 110},
            "remaining_pairwise_equations": 2905,
            "remaining_equations_by_pair": {
                "1,2": 148,
                "1,3": 240,
                "1,4": 189,
                "1,5": 183,
                "1,6": 255,
                "2,3": 149,
                "2,4": 250,
                "2,5": 184,
                "2,6": 182,
                "3,4": 145,
                "3,5": 255,
                "3,6": 180,
                "4,5": 145,
                "4,6": 255,
                "5,6": 145,
            },
            "matrix_metadata_hash": "c3afd73c0e0241e15be723b5dd494cf5643863b841e4d751c68687604107825f",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 360,
            "rank": 360,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 108, "2": 6, "3": 61, "4": 74, "5": 1, "6": 110},
            "remaining_pairwise_equations": 2905,
            "remaining_equations_by_pair": {
                "1,2": 148,
                "1,3": 240,
                "1,4": 189,
                "1,5": 183,
                "1,6": 255,
                "2,3": 149,
                "2,4": 250,
                "2,5": 184,
                "2,6": 182,
                "3,4": 145,
                "3,5": 255,
                "3,6": 180,
                "4,5": 145,
                "4,6": 255,
                "5,6": 145,
            },
            "matrix_metadata_hash": "749e4b520081459c11126fe37b12b2b01f4a1f46922d9c4c68c0f226932d5420",
            "status": "RANK_COMPUTED",
        },
    },
    "pair_boundary_cyclic_45_interval_high_overlap_seed_202606297": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 365,
            "rank": 365,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 66, "3": 102, "4": 110, "5": 73, "6": 13},
            "remaining_pairwise_equations": 2868,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 183,
                "1,4": 142,
                "1,5": 142,
                "1,6": 179,
                "2,3": 242,
                "2,4": 176,
                "2,5": 142,
                "2,6": 143,
                "3,4": 242,
                "3,5": 177,
                "3,6": 147,
                "4,5": 255,
                "4,6": 188,
                "5,6": 255,
            },
            "matrix_metadata_hash": "3edd6176f84ae30ebae35e42ac44959daeed8ed68313b25510f8a19d407a5049",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 365,
            "rank": 365,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 66, "3": 102, "4": 110, "5": 73, "6": 13},
            "remaining_pairwise_equations": 2868,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 183,
                "1,4": 142,
                "1,5": 142,
                "1,6": 179,
                "2,3": 242,
                "2,4": 176,
                "2,5": 142,
                "2,6": 143,
                "3,4": 242,
                "3,5": 177,
                "3,6": 147,
                "4,5": 255,
                "4,6": 188,
                "5,6": 255,
            },
            "matrix_metadata_hash": "716181398e6e125e04a14fb56c3f9a89309fa9a9d460c054ec4c3f919d0829de",
            "status": "RANK_COMPUTED",
        },
    },
    "fiber_repetition_cyclic_45_interval_high_overlap_seed_202606331": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 381,
            "rank": 381,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 76, "3": 112, "4": 114, "5": 77, "6": 1},
            "remaining_pairwise_equations": 2884,
            "remaining_equations_by_pair": {
                "1,2": 250,
                "1,3": 180,
                "1,4": 142,
                "1,5": 143,
                "1,6": 186,
                "2,3": 255,
                "2,4": 181,
                "2,5": 145,
                "2,6": 143,
                "3,4": 251,
                "3,5": 182,
                "3,6": 143,
                "4,5": 255,
                "4,6": 181,
                "5,6": 247,
            },
            "matrix_metadata_hash": "7b301a1510620d96d4a62cf82c3fda9ec8b5b5868aa41e90af89354187ab5b1c",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 381,
            "rank": 381,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 76, "3": 112, "4": 114, "5": 77, "6": 1},
            "remaining_pairwise_equations": 2884,
            "remaining_equations_by_pair": {
                "1,2": 250,
                "1,3": 180,
                "1,4": 142,
                "1,5": 143,
                "1,6": 186,
                "2,3": 255,
                "2,4": 181,
                "2,5": 145,
                "2,6": 143,
                "3,4": 251,
                "3,5": 182,
                "3,6": 143,
                "4,5": 255,
                "4,6": 181,
                "5,6": 247,
            },
            "matrix_metadata_hash": "19f4b5c75414c8deb2adc8679d2588e45ccebed63ffa8417ad93b736b0ab5177",
            "status": "RANK_COMPUTED",
        },
    },
    "anchor_compression_cyclic_3456_near_boundary_seed_202606416": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 355,
            "rank": 355,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 103, "2": 9, "3": 65, "4": 72, "5": 1, "6": 105},
            "remaining_pairwise_equations": 2900,
            "remaining_equations_by_pair": {
                "1,2": 149,
                "1,3": 236,
                "1,4": 187,
                "1,5": 183,
                "1,6": 255,
                "2,3": 152,
                "2,4": 250,
                "2,5": 182,
                "2,6": 183,
                "3,4": 146,
                "3,5": 255,
                "3,6": 177,
                "4,5": 145,
                "4,6": 255,
                "5,6": 145,
            },
            "matrix_metadata_hash": "5ebdd1180a48fb4111babcd87f26c326eadb881a3eb96720862085fc8d39b6a1",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 355,
            "rank": 355,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 103, "2": 9, "3": 65, "4": 72, "5": 1, "6": 105},
            "remaining_pairwise_equations": 2900,
            "remaining_equations_by_pair": {
                "1,2": 149,
                "1,3": 236,
                "1,4": 187,
                "1,5": 183,
                "1,6": 255,
                "2,3": 152,
                "2,4": 250,
                "2,5": 182,
                "2,6": 183,
                "3,4": 146,
                "3,5": 255,
                "3,6": 177,
                "4,5": 145,
                "4,6": 255,
                "5,6": 145,
            },
            "matrix_metadata_hash": "d0f91c40f243f5f99715b38e6d1288b9e13f6d921ff3b5bd1f5716c6afd65a0e",
            "status": "RANK_COMPUTED",
        },
    },
    "anchor_compression_cyclic_45_interval_high_overlap_seed_202606314": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 374,
            "rank": 374,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 10, "2": 74, "3": 112, "4": 109, "5": 68, "6": 1},
            "remaining_pairwise_equations": 2877,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 186,
                "1,4": 146,
                "1,5": 142,
                "1,6": 180,
                "2,3": 255,
                "2,4": 178,
                "2,5": 142,
                "2,6": 142,
                "3,4": 246,
                "3,5": 177,
                "3,6": 143,
                "4,5": 250,
                "4,6": 180,
                "5,6": 255,
            },
            "matrix_metadata_hash": "88d6d4a510824697d45f80a0e0d45e11f2a983a80ec503600ed2decdbc21c1a6",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 374,
            "rank": 374,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 10, "2": 74, "3": 112, "4": 109, "5": 68, "6": 1},
            "remaining_pairwise_equations": 2877,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 186,
                "1,4": 146,
                "1,5": 142,
                "1,6": 180,
                "2,3": 255,
                "2,4": 178,
                "2,5": 142,
                "2,6": 142,
                "3,4": 246,
                "3,5": 177,
                "3,6": 143,
                "4,5": 250,
                "4,6": 180,
                "5,6": 255,
            },
            "matrix_metadata_hash": "e7553de7ff693dc973057f2e06ef2d856b3980b0e353dbbb0f22852e72845283",
            "status": "RANK_COMPUTED",
        },
    },
    "fiber_repetition_cyclic_3456_near_boundary_seed_202606433": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 366,
            "rank": 366,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 109, "2": 5, "3": 70, "4": 72, "5": 1, "6": 109},
            "remaining_pairwise_equations": 2911,
            "remaining_equations_by_pair": {
                "1,2": 147,
                "1,3": 255,
                "1,4": 185,
                "1,5": 184,
                "1,6": 250,
                "2,3": 146,
                "2,4": 250,
                "2,5": 185,
                "2,6": 184,
                "3,4": 145,
                "3,5": 250,
                "3,6": 184,
                "4,5": 145,
                "4,6": 255,
                "5,6": 146,
            },
            "matrix_metadata_hash": "8e2b39515f21790d455f3e0ffb58b236c4cffef75a79191c063e06bac8a381bc",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 366,
            "rank": 366,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 109, "2": 5, "3": 70, "4": 72, "5": 1, "6": 109},
            "remaining_pairwise_equations": 2911,
            "remaining_equations_by_pair": {
                "1,2": 147,
                "1,3": 255,
                "1,4": 185,
                "1,5": 184,
                "1,6": 250,
                "2,3": 146,
                "2,4": 250,
                "2,5": 185,
                "2,6": 184,
                "3,4": 145,
                "3,5": 250,
                "3,6": 184,
                "4,5": 145,
                "4,6": 255,
                "5,6": 146,
            },
            "matrix_metadata_hash": "d0f8aaeed536f4259ee14b65c75452f319490c781d9daf143bfaaca6e6fb2f9f",
            "status": "RANK_COMPUTED",
        },
    },
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def pair_key(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def pair_label(pair: tuple[int, int]) -> str:
    return f"{pair[0]},{pair[1]}"


def cyclic_orbit(pattern: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [
        tuple(sorted(((item + shift) % LIST_SIZE for item in pattern)))
        for shift in range(LIST_SIZE)
    ]


def cyclic_sequence(specs: list[tuple[int, tuple[int, ...]]]) -> list[tuple[int, ...]]:
    sequence: list[tuple[int, ...]] = [tuple(range(LIST_SIZE))]
    for count, pattern in specs:
        orbit = cyclic_orbit(pattern)
        for _idx in range(count):
            sequence.extend(orbit)
    assert len(sequence) == N
    return sequence


def bit_reverse(value: int, bits: int = 9) -> int:
    out = 0
    for _idx in range(bits):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def place_sequence(sequence: list[tuple[int, ...]], order_name: str) -> list[list[int]]:
    if order_name == "identity":
        order = list(range(N))
    elif order_name == "quotient_fiber":
        order = sorted(range(N), key=lambda pos: (pos % 16, pos // 16))
    elif order_name == "bit_reverse":
        order = [bit_reverse(pos) for pos in range(N)]
    else:
        raise ValueError(f"unknown order {order_name}")
    memberships: list[list[int] | None] = [None for _idx in range(N)]
    for idx, pos in enumerate(order):
        memberships[pos] = list(sequence[idx])
    assert all(item is not None for item in memberships)
    return [list(item) for item in memberships if item is not None]


def seed_memberships(seed_name: str) -> list[list[int]]:
    if seed_name == "cyclic_45_interval_high_overlap":
        return place_sequence(
            cyclic_sequence([(39, (0, 1, 2, 3)), (34, (0, 1, 2, 3, 4))]),
            "identity",
        )
    if seed_name == "cyclic_45_balanced":
        return place_sequence(
            cyclic_sequence([(39, (0, 1, 2, 4)), (34, (0, 1, 2, 3, 4))]),
            "identity",
        )
    if seed_name == "cyclic_3456_near_boundary":
        return place_sequence(
            cyclic_sequence(
                [
                    (3, (0, 2, 4)),
                    (36, (0, 2, 4, 6)),
                    (31, (0, 1, 3, 5, 6)),
                    (3, (1, 2, 3, 4, 5, 6)),
                ]
            ),
            "identity",
        )
    if seed_name == "cyclic_3456_balanced":
        return place_sequence(
            cyclic_sequence(
                [
                    (3, (0, 2, 4)),
                    (36, (0, 1, 2, 4)),
                    (31, (0, 1, 2, 3, 4)),
                    (3, (0, 1, 2, 4, 5, 6)),
                ]
            ),
            "quotient_fiber",
        )
    raise ValueError(f"unknown seed {seed_name}")


def support_summary(memberships: list[list[int]]) -> dict[str, Any]:
    counts = [0 for _idx in range(LIST_SIZE)]
    pair_counts = {(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    pattern_histogram: dict[str, int] = {}
    multiplicity_histogram: dict[str, int] = {}
    for members in memberships:
        key = ",".join(str(item) for item in sorted(members))
        pattern_histogram[key] = pattern_histogram.get(key, 0) + 1
        size_key = str(len(members))
        multiplicity_histogram[size_key] = multiplicity_histogram.get(size_key, 0) + 1
        for member in members:
            counts[member] += 1
        for a, b in combinations(sorted(members), 2):
            pair_counts[pair_key(a, b)] += 1
    pair_values = list(pair_counts.values())
    return {
        "witness_support_sizes": counts,
        "pair_intersection_min": min(pair_values),
        "pair_intersection_max": max(pair_values),
        "pair_intersection_values": sorted(pair_values),
        "pair_intersections": {pair_label(pair): pair_counts[pair] for pair in sorted(pair_counts)},
        "pair_intersections_at_255": sum(1 for value in pair_values if value == K - 1),
        "pair_intersections_at_254_or_255": sum(1 for value in pair_values if value >= K - 2),
        "pair_intersection_sum": sum(pair_values),
        "pair_intersection_square_sum": sum(value * value for value in pair_values),
        "multiplicity_histogram": dict(sorted(multiplicity_histogram.items())),
        "membership_pattern_count": len(pattern_histogram),
        "membership_pattern_histogram_hash": hash_payload(pattern_histogram),
        "support_hash": hash_payload([sorted(members) for members in memberships]),
    }


def quotient_fiber_profile(memberships: list[list[int]]) -> dict[str, Any]:
    profiles = []
    for residue in range(16):
        positions = [pos for pos in range(N) if pos % 16 == residue]
        histogram: dict[str, int] = {}
        for pos in positions:
            key = ",".join(str(item) for item in sorted(memberships[pos]))
            histogram[key] = histogram.get(key, 0) + 1
        profiles.append(
            {
                "distinct_patterns": len(histogram),
                "largest_pattern_multiplicity": max(histogram.values()),
                "multiplicities": {
                    str(size): sum(1 for pos in positions if len(memberships[pos]) == size)
                    for size in range(1, LIST_SIZE + 1)
                    if any(len(memberships[pos]) == size for pos in positions)
                },
            }
        )
    return {
        "fiber_count": 16,
        "fiber_size": 32,
        "distinct_pattern_counts": [row["distinct_patterns"] for row in profiles],
        "largest_pattern_multiplicities": [row["largest_pattern_multiplicity"] for row in profiles],
        "multiplicity_profiles": [row["multiplicities"] for row in profiles],
    }


def compressed_variables(summary: dict[str, Any]) -> int:
    return sum(K - summary["pair_intersections"][f"0,{witness}"] for witness in range(1, LIST_SIZE))


def row_pattern_proxy(summary: dict[str, Any], profile: dict[str, Any], objective: str) -> dict[str, Any]:
    pair_values = summary["pair_intersection_values"]
    compressed = compressed_variables(summary)
    repeated_fiber_patterns = sum(profile["largest_pattern_multiplicities"])
    high_pair_sum = sum(value for value in pair_values if value >= 250)
    base_score = (
        1_000_000 * summary["pair_intersections_at_255"]
        + 20_000 * summary["pair_intersections_at_254_or_255"]
        + 10 * high_pair_sum
        + summary["pair_intersection_square_sum"] // 100
        + 25 * repeated_fiber_patterns
        - 50 * compressed
    )
    if objective == "anchor_compression":
        base_score += 500_000 - 2_000 * compressed
    elif objective == "fiber_repetition":
        base_score += 1_000 * repeated_fiber_patterns
    elif objective == "pair_boundary":
        base_score += 100_000 * summary["pair_intersections_at_255"]
    return {
        "method": "row_pattern_pair_boundary_proxy",
        "proxy_score": base_score,
        "compressed_variables": compressed,
        "repeated_fiber_pattern_score": repeated_fiber_patterns,
        "status": "SCORED",
    }


def valid_support(memberships: list[list[int]]) -> bool:
    summary = support_summary(memberships)
    return (
        summary["witness_support_sizes"] == [TARGET_AGREEMENT] * LIST_SIZE
        and summary["pair_intersection_max"] <= K - 1
    )


def objective_score(memberships: list[list[int]], objective: str) -> int:
    summary = support_summary(memberships)
    if summary["witness_support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
        return -10**18
    if summary["pair_intersection_max"] > K - 1:
        return -10**18
    profile = quotient_fiber_profile(memberships)
    return row_pattern_proxy(summary, profile, objective)["proxy_score"]


def propose_two_switch(
    memberships: list[list[int]],
    rng: random.Random,
    restrict_same_fiber: bool,
) -> list[list[int]] | None:
    if restrict_same_fiber:
        residue = rng.randrange(16)
        positions = [pos for pos in range(N) if pos % 16 == residue]
        pos_a, pos_b = rng.sample(positions, 2)
    else:
        pos_a, pos_b = rng.sample(range(N), 2)
    set_a = set(memberships[pos_a])
    set_b = set(memberships[pos_b])
    only_a = sorted(set_a - set_b)
    only_b = sorted(set_b - set_a)
    if not only_a or not only_b:
        return None
    i = rng.choice(only_a)
    j = rng.choice(only_b)
    proposal = copy.deepcopy(memberships)
    proposal[pos_a] = sorted((set_a - {i}) | {j})
    proposal[pos_b] = sorted((set_b - {j}) | {i})
    return proposal


def mutate(
    memberships: list[list[int]],
    objective: str,
    seed: int,
    steps: int,
    restrict_same_fiber: bool,
) -> tuple[list[list[int]], int]:
    rng = random.Random(seed)
    current = copy.deepcopy(memberships)
    current_score = objective_score(current, objective)
    accepted = 0
    for _idx in range(steps):
        proposal = propose_two_switch(current, rng, restrict_same_fiber)
        if proposal is None:
            continue
        proposal_score = objective_score(proposal, objective)
        if proposal_score > current_score or (
            proposal_score == current_score and rng.random() < 0.02
        ):
            current = proposal
            current_score = proposal_score
            accepted += 1
    assert valid_support(current)
    return current, accepted


def generated_candidate_specs() -> list[dict[str, Any]]:
    seeds = [
        "cyclic_45_interval_high_overlap",
        "cyclic_45_balanced",
        "cyclic_3456_near_boundary",
        "cyclic_3456_balanced",
    ]
    objectives = [
        ("pair_boundary", False),
        ("anchor_compression", False),
        ("fiber_repetition", True),
    ]
    specs: list[dict[str, Any]] = []
    seed_counter = 202606280
    for seed_name in seeds:
        for objective, restrict_same_fiber in objectives:
            seed_counter += 17
            specs.append(
                {
                    "seed_name": seed_name,
                    "objective": objective,
                    "random_seed": seed_counter,
                    "steps": 1200,
                    "restrict_same_fiber": restrict_same_fiber,
                }
            )
    return specs


def retained_candidates() -> list[dict[str, Any]]:
    generated = []
    for spec in generated_candidate_specs():
        base = seed_memberships(spec["seed_name"])
        memberships, accepted = mutate(
            base,
            objective=spec["objective"],
            seed=spec["random_seed"],
            steps=spec["steps"],
            restrict_same_fiber=spec["restrict_same_fiber"],
        )
        summary = support_summary(memberships)
        profile = quotient_fiber_profile(memberships)
        proxy = row_pattern_proxy(summary, profile, spec["objective"])
        candidate_id = (
            f"{spec['objective']}_{spec['seed_name']}_"
            f"seed_{spec['random_seed']}"
        )
        generated.append(
            {
                "candidate_id": candidate_id,
                "mutation_family": "balanced_two_switch_membership_hypergraph",
                "seed_design": spec["seed_name"],
                "search_objective": spec["objective"],
                "random_seed": spec["random_seed"],
                "mutation_steps": spec["steps"],
                "accepted_mutations": accepted,
                "restrict_same_quotient_fiber": spec["restrict_same_fiber"],
                "memberships": memberships,
                "support_design": summary,
                "quotient_fiber_profile": profile,
                "rank_proxy": proxy,
            }
        )
    generated.sort(
        key=lambda row: (
            row["rank_proxy"]["proxy_score"],
            row["support_design"]["pair_intersections_at_255"],
            -row["rank_proxy"]["compressed_variables"],
            row["candidate_id"],
        ),
        reverse=True,
    )
    return generated[:RETAINED_CANDIDATES]


def rank_gate_from_precomputed(candidate_id: str, field_mode: str) -> dict[str, Any]:
    computed = PRECOMPUTED_RANKS.get(candidate_id, {}).get(field_mode)
    if computed is None:
        return {
            "field_mode": field_mode,
            "field_label": "GF(17^32)" if field_mode == "exact" else "GF(12289)_surrogate",
            "field_size": str(FIELD_DENOMINATOR if field_mode == "exact" else SURROGATE_FIELD_SIZE),
            "rank": None,
            "nullity": None,
            "status": "NOT_RUN",
        }
    return computed


def build_candidates() -> list[dict[str, Any]]:
    rows = []
    for candidate in retained_candidates():
        exact_gate = rank_gate_from_precomputed(candidate["candidate_id"], "exact")
        surrogate_gate = rank_gate_from_precomputed(candidate["candidate_id"], "surrogate")
        proof_status = (
            "ROUTE_CUT_TESTED_CANDIDATE"
            if exact_gate.get("nullity") == 0
            else "CANDIDATE"
        )
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "mutation_family": candidate["mutation_family"],
                "seed_design": candidate["seed_design"],
                "search_objective": candidate["search_objective"],
                "random_seed": candidate["random_seed"],
                "mutation_steps": candidate["mutation_steps"],
                "accepted_mutations": candidate["accepted_mutations"],
                "restrict_same_quotient_fiber": candidate["restrict_same_quotient_fiber"],
                "support_design": candidate["support_design"],
                "quotient_fiber_profile": candidate["quotient_fiber_profile"],
                "rank_proxy": candidate["rank_proxy"],
                "surrogate_rank_gate": surrogate_gate,
                "sage_exact_rank": exact_gate,
                "extraction": {
                    "non_diagonal_solution_found": False,
                    "agreement_verified": False,
                    "status": "NOT_RUN",
                },
                "proof_status": proof_status,
            }
        )
    return rows


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def build_result() -> dict[str, Any]:
    candidates = build_candidates()
    exact_rows = [row for row in candidates if row["sage_exact_rank"]["status"] != "NOT_RUN"]
    best_exact_nullity = max(
        (row["sage_exact_rank"]["nullity"] or 0 for row in exact_rows),
        default=None,
    )
    assert threshold_floor() == 6
    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "field_denominator": str(FIELD_DENOMINATOR),
        "field_denominator_label": "17^32",
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "target_agreement": TARGET_AGREEMENT,
        "baseline": {
            "current_pr_133_agreement": CURRENT_PR_133_AGREEMENT,
            "current_pr_133_lambda_lower": CURRENT_PR_133_LAMBDA_LOWER,
            "source": "PR #133 hybrid quotient-residual certificate",
        },
        "search_summary": {
            "generated_candidate_count": len(generated_candidate_specs()),
            "retained_candidate_count": len(candidates),
            "exact_audited_count": len(exact_rows),
            "candidate_family": "surrogate-scored balanced two-switch membership mutations",
            "rank_proxy": "row-pattern/pair-boundary score plus GF(12289) Sage rank gate",
            "surrogate_field": "GF(12289), 512 | 12288",
            "exact_field": "GF(17^32)",
            "best_exact_nullity": best_exact_nullity,
            "status": (
                "ROUTE_CUT_TESTED_CANDIDATES"
                if exact_rows and best_exact_nullity == 0
                else "PARTIAL"
            ),
        },
        "candidates": candidates,
        "interpretation": {
            "support_packing_blocks_a327": False,
            "proxy_search_found_exact_nullity": False,
            "candidate_found": False,
            "status": (
                "ROUTE_CUT_TESTED_CANDIDATES"
                if exact_rows and best_exact_nullity == 0
                else "PARTIAL"
            ),
        },
        "open_layers": {
            "larger_mutation_search": True,
            "positive_exact_nullity_candidate": best_exact_nullity not in {0, None},
            "non_diagonal_nullspace_extraction": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_support_pattern_surrogate_nullity_search.sage",
            "recomputes_retained_candidates": True,
            "constructs_GF_17_32": True,
            "uses_surrogate_rank_gate": True,
            "uses_exact_rank_gate": True,
        },
        "repo_claim": {
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
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": (
                "ROUTE_CUT_TESTED_CANDIDATES"
                if exact_rows and best_exact_nullity == 0
                else "PARTIAL"
            ),
        },
        "status": "M1_SUPPORT_PATTERN_SURROGATE_NULLITY_SEARCH_ROUTE_CUT_PARTIAL",
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
                "proxy_score": row["rank_proxy"]["proxy_score"],
                "support_hash": row["support_design"]["support_hash"],
                "pair_max": row["support_design"]["pair_intersection_max"],
                "pairs_at_255": row["support_design"]["pair_intersections_at_255"],
                "compressed_variables": row["rank_proxy"]["compressed_variables"],
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
        print(f"generated {len(generated_candidate_specs())} support-pattern mutations")
        print(f"retained {len(result['candidates'])} surrogate-scored candidates")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
