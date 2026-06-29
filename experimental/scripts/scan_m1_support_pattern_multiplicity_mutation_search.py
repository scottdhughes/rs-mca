#!/usr/bin/env python3
"""Emit the M1 support-pattern multiplicity-mutation search checkpoint."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import random
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_support_pattern_multiplicity_mutation_search.json")
BASE_SCANNER_PATH = Path("experimental/scripts/scan_m1_support_pattern_surrogate_nullity_search.py")

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


# Filled from the Sage audit.  The normal scanner/verifier stay dependency-free.
PRECOMPUTED_RANKS: dict[str, dict[str, Any]] = {
    "multiplicity_spread_cyclic_3456_balanced_seed_202607204": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 30,
            "rank": 30,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 4, "2": 5, "3": 10, "4": 4, "5": 6, "6": 1},
            "remaining_pairwise_equations": 3767,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 242,
                "1,4": 252,
                "1,5": 245,
                "1,6": 247,
                "2,3": 253,
                "2,4": 248,
                "2,5": 255,
                "2,6": 248,
                "3,4": 255,
                "3,5": 254,
                "3,6": 250,
                "4,5": 255,
                "4,6": 253,
                "5,6": 255,
            },
            "matrix_metadata_hash": "a7205371dc8ea73601e790bdda52dd944c81203336402da74a9d0bb8b300e3a4",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 30,
            "rank": 30,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 4, "2": 5, "3": 10, "4": 4, "5": 6, "6": 1},
            "remaining_pairwise_equations": 3767,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 242,
                "1,4": 252,
                "1,5": 245,
                "1,6": 247,
                "2,3": 253,
                "2,4": 248,
                "2,5": 255,
                "2,6": 248,
                "3,4": 255,
                "3,5": 254,
                "3,6": 250,
                "4,5": 255,
                "4,6": 253,
                "5,6": 255,
            },
            "matrix_metadata_hash": "090c3758db9babc79c3c06b23db434c8790897f6ea5402c7b8a963a3462efd9b",
            "status": "RANK_COMPUTED",
        },
    },
    "multiplicity_spread_cyclic_45_balanced_seed_202607014": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 23,
            "rank": 23,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 9, "4": 5, "5": 6, "6": 1},
            "remaining_pairwise_equations": 3753,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 244,
                "1,4": 251,
                "1,5": 255,
                "1,6": 251,
                "2,3": 251,
                "2,4": 244,
                "2,5": 252,
                "2,6": 252,
                "3,4": 255,
                "3,5": 246,
                "3,6": 241,
                "4,5": 255,
                "4,6": 246,
                "5,6": 255,
            },
            "matrix_metadata_hash": "e70bbbd033a65bdde0664c4c787c9ae5756d3df93928f481d5fe87ffd983ee9b",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 23,
            "rank": 23,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 9, "4": 5, "5": 6, "6": 1},
            "remaining_pairwise_equations": 3753,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 244,
                "1,4": 251,
                "1,5": 255,
                "1,6": 251,
                "2,3": 251,
                "2,4": 244,
                "2,5": 252,
                "2,6": 252,
                "3,4": 255,
                "3,5": 246,
                "3,6": 241,
                "4,5": 255,
                "4,6": 246,
                "5,6": 255,
            },
            "matrix_metadata_hash": "8a0464b8935810ac53c6cc28a0b6ce5a4b6d1d5a36429c4cc1a101736aa859fa",
            "status": "RANK_COMPUTED",
        },
    },
    "multiplicity_spread_cyclic_45_interval_high_overlap_seed_202606919": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 69,
            "rank": 69,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 16, "3": 20, "4": 17, "5": 14, "6": 1},
            "remaining_pairwise_equations": 3697,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 242,
                "1,4": 240,
                "1,5": 236,
                "1,6": 243,
                "2,3": 254,
                "2,4": 248,
                "2,5": 236,
                "2,6": 246,
                "3,4": 255,
                "3,5": 248,
                "3,6": 241,
                "4,5": 255,
                "4,6": 243,
                "5,6": 255,
            },
            "matrix_metadata_hash": "9fe3576a08f14ce459e76701d2658660abd080a085ccce096083e67d6e7392f3",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 69,
            "rank": 69,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 16, "3": 20, "4": 17, "5": 14, "6": 1},
            "remaining_pairwise_equations": 3697,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 242,
                "1,4": 240,
                "1,5": 236,
                "1,6": 243,
                "2,3": 254,
                "2,4": 248,
                "2,5": 236,
                "2,6": 246,
                "3,4": 255,
                "3,5": 248,
                "3,6": 241,
                "4,5": 255,
                "4,6": 243,
                "5,6": 255,
            },
            "matrix_metadata_hash": "fef29becc20cda3f06f36f9b3d50e3bbb6310594d72ee563d65403c2e6bd927e",
            "status": "RANK_COMPUTED",
        },
    },
    "multiplicity_spread_cyclic_3456_near_boundary_seed_202607109": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 89,
            "rank": 89,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 25, "2": 1, "3": 26, "4": 19, "5": 1, "6": 17},
            "remaining_pairwise_equations": 3654,
            "remaining_equations_by_pair": {
                "1,2": 229,
                "1,3": 255,
                "1,4": 238,
                "1,5": 243,
                "1,6": 255,
                "2,3": 228,
                "2,4": 255,
                "2,5": 238,
                "2,6": 252,
                "3,4": 236,
                "3,5": 255,
                "3,6": 238,
                "4,5": 240,
                "4,6": 255,
                "5,6": 237,
            },
            "matrix_metadata_hash": "0d915f805d23b9d78bec3de9187613b0644765eccfd2051a81a294fbb71e9e98",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 89,
            "rank": 89,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 25, "2": 1, "3": 26, "4": 19, "5": 1, "6": 17},
            "remaining_pairwise_equations": 3654,
            "remaining_equations_by_pair": {
                "1,2": 229,
                "1,3": 255,
                "1,4": 238,
                "1,5": 243,
                "1,6": 255,
                "2,3": 228,
                "2,4": 255,
                "2,5": 238,
                "2,6": 252,
                "3,4": 236,
                "3,5": 255,
                "3,6": 238,
                "4,5": 240,
                "4,6": 255,
                "5,6": 237,
            },
            "matrix_metadata_hash": "1a2352c19e096144415102b5165c35ee167dcd837d11b6e3907e40aa9414c693",
            "status": "RANK_COMPUTED",
        },
    },
    "mixed_boundary_spread_cyclic_3456_balanced_seed_202607280": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 19,
            "rank": 19,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 6, "4": 9, "5": 1, "6": 1},
            "remaining_pairwise_equations": 3771,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 251,
                "1,4": 251,
                "1,5": 253,
                "1,6": 246,
                "2,3": 255,
                "2,4": 252,
                "2,5": 251,
                "2,6": 255,
                "3,4": 255,
                "3,5": 248,
                "3,6": 245,
                "4,5": 255,
                "4,6": 249,
                "5,6": 250,
            },
            "matrix_metadata_hash": "b3b408e607bb8253847899bfa3b9f81732dacf2d93e41f4a00197086721636ef",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 19,
            "rank": 19,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 6, "4": 9, "5": 1, "6": 1},
            "remaining_pairwise_equations": 3771,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 251,
                "1,4": 251,
                "1,5": 253,
                "1,6": 246,
                "2,3": 255,
                "2,4": 252,
                "2,5": 251,
                "2,6": 255,
                "3,4": 255,
                "3,5": 248,
                "3,6": 245,
                "4,5": 255,
                "4,6": 249,
                "5,6": 250,
            },
            "matrix_metadata_hash": "cda57f07e7ab6dc3881a9f51ac5fbabcc5810c8a062e3b9079f119c2d68a288e",
            "status": "RANK_COMPUTED",
        },
    },
    "mixed_boundary_spread_cyclic_45_balanced_seed_202607090": {
        "surrogate": {
            "field_mode": "surrogate",
            "field_label": "GF(12289)_surrogate",
            "field_size": "12289",
            "compressed_variables": 32,
            "rank": 32,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 5, "3": 12, "4": 8, "5": 5, "6": 1},
            "remaining_pairwise_equations": 3773,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 247,
                "1,4": 246,
                "1,5": 251,
                "1,6": 246,
                "2,3": 255,
                "2,4": 247,
                "2,5": 254,
                "2,6": 255,
                "3,4": 255,
                "3,5": 255,
                "3,6": 253,
                "4,5": 255,
                "4,6": 244,
                "5,6": 255,
            },
            "matrix_metadata_hash": "929377ac08b5fbe2d408096adf1e1d9ea88c1ce6d21b43d5608405f9986c9103",
            "status": "RANK_COMPUTED",
        },
        "exact": {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": "2367911594760467245844106297320951247361",
            "compressed_variables": 32,
            "rank": 32,
            "nullity": 0,
            "non_diagonal_solution_found": False,
            "compressed_dimensions_by_witness": {"1": 1, "2": 5, "3": 12, "4": 8, "5": 5, "6": 1},
            "remaining_pairwise_equations": 3773,
            "remaining_equations_by_pair": {
                "1,2": 255,
                "1,3": 247,
                "1,4": 246,
                "1,5": 251,
                "1,6": 246,
                "2,3": 255,
                "2,4": 247,
                "2,5": 254,
                "2,6": 255,
                "3,4": 255,
                "3,5": 255,
                "3,6": 253,
                "4,5": 255,
                "4,6": 244,
                "5,6": 255,
            },
            "matrix_metadata_hash": "60e0d922304c22a20735f18543442802e27edcb6325e1aaca2a79f7da95d3d8f",
            "status": "RANK_COMPUTED",
        },
    },
}


def load_base():
    spec = importlib.util.spec_from_file_location("m1_surrogate_scanner", BASE_SCANNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


base = load_base()


def multiplicity_spread_score(summary: dict[str, Any]) -> int:
    histogram = {int(size): count for size, count in summary["multiplicity_histogram"].items()}
    high = 80 * histogram.get(7, 0) + 35 * histogram.get(6, 0)
    low = 30 * histogram.get(1, 0) + 20 * histogram.get(2, 0)
    mid_penalty = 4 * histogram.get(4, 0) + 2 * histogram.get(5, 0)
    distinct_bonus = 120 * len(histogram)
    return high + low + distinct_bonus - mid_penalty


def proxy_score(memberships: list[list[int]], objective: str) -> tuple[int, dict[str, Any], dict[str, Any]]:
    summary = base.support_summary(memberships)
    if summary["witness_support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
        return -10**18, summary, {}
    if summary["pair_intersection_max"] > K - 1:
        return -10**18, summary, {}
    profile = base.quotient_fiber_profile(memberships)
    row_proxy = base.row_pattern_proxy(summary, profile, "pair_boundary")
    score = row_proxy["proxy_score"]
    score += 12_000 * multiplicity_spread_score(summary)
    if objective == "multiplicity_spread":
        score += 80_000 * multiplicity_spread_score(summary)
    elif objective == "pair_boundary":
        score += 300_000 * summary["pair_intersections_at_255"]
    elif objective == "anchor_compression":
        score += 700_000 - 2_500 * row_proxy["compressed_variables"]
    elif objective == "fiber_repetition":
        score += 1_500 * row_proxy["repeated_fiber_pattern_score"]
    elif objective == "mixed_boundary_spread":
        score += 150_000 * summary["pair_intersections_at_255"]
        score += 50_000 * multiplicity_spread_score(summary)
    return score, summary, profile


def valid_support(memberships: list[list[int]]) -> bool:
    summary = base.support_summary(memberships)
    return (
        summary["witness_support_sizes"] == [TARGET_AGREEMENT] * LIST_SIZE
        and summary["pair_intersection_max"] <= K - 1
    )


def propose_pair_replacement(
    memberships: list[list[int]],
    rng: random.Random,
    restrict_same_fiber: bool,
    force_size_change: bool,
) -> list[list[int]] | None:
    if restrict_same_fiber:
        residue = rng.randrange(16)
        positions = [pos for pos in range(N) if pos % 16 == residue]
        pos_a, pos_b = rng.sample(positions, 2)
    else:
        pos_a, pos_b = rng.sample(range(N), 2)

    set_a = set(memberships[pos_a])
    set_b = set(memberships[pos_b])
    common = set_a & set_b
    movable = sorted(set_a ^ set_b)
    if len(movable) < 2:
        return None

    old_a_size = len(set_a)
    old_b_size = len(set_b)
    choices = []
    for first_count in range(len(movable) + 1):
        new_a_size = len(common) + first_count
        new_b_size = len(common) + len(movable) - first_count
        if not (1 <= new_a_size <= LIST_SIZE and 1 <= new_b_size <= LIST_SIZE):
            continue
        if force_size_change and sorted((new_a_size, new_b_size)) == sorted((old_a_size, old_b_size)):
            continue
        choices.append(first_count)
    if not choices:
        return None

    first_count = rng.choice(choices)
    rng.shuffle(movable)
    first = set(movable[:first_count])
    second = set(movable[first_count:])
    proposal = copy.deepcopy(memberships)
    proposal[pos_a] = sorted(common | first)
    proposal[pos_b] = sorted(common | second)
    if proposal[pos_a] == memberships[pos_a] and proposal[pos_b] == memberships[pos_b]:
        return None
    return proposal


def mutate(
    memberships: list[list[int]],
    objective: str,
    seed: int,
    steps: int,
    restrict_same_fiber: bool,
) -> tuple[list[list[int]], int, int]:
    rng = random.Random(seed)
    current = copy.deepcopy(memberships)
    current_score, _summary, _profile = proxy_score(current, objective)
    accepted = 0
    attempted_valid = 0
    for _idx in range(steps):
        proposal = propose_pair_replacement(
            current,
            rng,
            restrict_same_fiber=restrict_same_fiber,
            force_size_change=True,
        )
        if proposal is None:
            continue
        proposal_score, _proposal_summary, _proposal_profile = proxy_score(proposal, objective)
        if proposal_score <= -10**17:
            continue
        attempted_valid += 1
        if proposal_score > current_score or (
            proposal_score == current_score and rng.random() < 0.01
        ):
            current = proposal
            current_score = proposal_score
            accepted += 1
    assert valid_support(current)
    return current, accepted, attempted_valid


def generated_candidate_specs() -> list[dict[str, Any]]:
    seeds = [
        "cyclic_45_interval_high_overlap",
        "cyclic_45_balanced",
        "cyclic_3456_near_boundary",
        "cyclic_3456_balanced",
    ]
    objectives = [
        ("multiplicity_spread", False),
        ("pair_boundary", False),
        ("anchor_compression", False),
        ("fiber_repetition", True),
        ("mixed_boundary_spread", False),
    ]
    specs = []
    counter = 202606900
    for seed_name in seeds:
        for objective, restrict_same_fiber in objectives:
            counter += 19
            specs.append(
                {
                    "seed_name": seed_name,
                    "objective": objective,
                    "random_seed": counter,
                    "steps": 1800,
                    "restrict_same_fiber": restrict_same_fiber,
                }
            )
    return specs


def retained_candidates() -> list[dict[str, Any]]:
    generated = []
    for spec in generated_candidate_specs():
        seed_memberships = base.seed_memberships(spec["seed_name"])
        memberships, accepted, attempted_valid = mutate(
            seed_memberships,
            objective=spec["objective"],
            seed=spec["random_seed"],
            steps=spec["steps"],
            restrict_same_fiber=spec["restrict_same_fiber"],
        )
        summary = base.support_summary(memberships)
        profile = base.quotient_fiber_profile(memberships)
        row_proxy = base.row_pattern_proxy(summary, profile, "pair_boundary")
        score, _summary, _profile = proxy_score(memberships, spec["objective"])
        candidate_id = (
            f"{spec['objective']}_{spec['seed_name']}_"
            f"seed_{spec['random_seed']}"
        )
        generated.append(
            {
                "candidate_id": candidate_id,
                "mutation_family": "degree_preserving_pair_replacement_membership_hypergraph",
                "seed_design": spec["seed_name"],
                "search_objective": spec["objective"],
                "random_seed": spec["random_seed"],
                "mutation_steps": spec["steps"],
                "valid_mutation_attempts": attempted_valid,
                "accepted_mutations": accepted,
                "restrict_same_quotient_fiber": spec["restrict_same_fiber"],
                "memberships": memberships,
                "support_design": summary,
                "quotient_fiber_profile": profile,
                "rank_proxy": {
                    "method": "multiplicity_pair_boundary_row_pattern_proxy",
                    "proxy_score": score,
                    "compressed_variables": row_proxy["compressed_variables"],
                    "multiplicity_spread_score": multiplicity_spread_score(summary),
                    "repeated_fiber_pattern_score": row_proxy["repeated_fiber_pattern_score"],
                    "status": "SCORED",
                },
            }
        )
    generated.sort(
        key=lambda row: (
            row["rank_proxy"]["proxy_score"],
            row["support_design"]["pair_intersections_at_255"],
            row["rank_proxy"]["multiplicity_spread_score"],
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
        row = {
            key: value
            for key, value in candidate.items()
            if key != "memberships"
        }
        row.update(
            {
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
        rows.append(row)
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
    status = "ROUTE_CUT_TESTED_CANDIDATES" if exact_rows and best_exact_nullity == 0 else "PARTIAL"
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
            "candidate_family": "multiplicity-changing degree-preserving pair replacements",
            "rank_proxy": "multiplicity-spread/pair-boundary score plus GF(12289) Sage rank gate",
            "surrogate_field": "GF(12289), 512 | 12288",
            "exact_field": "GF(17^32)",
            "best_exact_nullity": best_exact_nullity,
            "status": status,
        },
        "candidates": candidates,
        "interpretation": {
            "support_packing_blocks_a327": False,
            "multiplicity_mutation_found_exact_nullity": False,
            "candidate_found": False,
            "status": status,
        },
        "open_layers": {
            "larger_mutation_search": True,
            "positive_exact_nullity_candidate": best_exact_nullity not in {0, None},
            "non_diagonal_nullspace_extraction": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_support_pattern_multiplicity_mutation_search.sage",
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
            "status": status,
        },
        "status": "M1_SUPPORT_PATTERN_MULTIPLICITY_MUTATION_SEARCH_ROUTE_CUT_PARTIAL",
    }
    result["record_hash"] = base.hash_payload(
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
                "multiplicity_histogram": row["support_design"]["multiplicity_histogram"],
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
        print(f"generated {len(generated_candidate_specs())} multiplicity-changing mutations")
        print(f"retained {len(result['candidates'])} surrogate-scored candidates")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
