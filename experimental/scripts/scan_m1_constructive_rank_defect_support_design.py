#!/usr/bin/env python3
"""Emit the M1 constructive rank-defect support-design checkpoint."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import random
from itertools import combinations
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_constructive_rank_defect_support_design.json")
RANK_FEEDBACK_SCANNER_PATH = Path(
    "experimental/scripts/scan_m1_support_pattern_surrogate_rank_feedback_search.py"
)

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
GENERATED_CANDIDATES = 80
RETAINED_CANDIDATES = 8


# Filled from the Sage audit after retained candidate identities are fixed.
# The scanner stays dependency-free; Sage is the exact GF(17^32) source.
PRECOMPUTED_EXACT_RANKS: dict[str, dict[str, Any]] = {
    "anchored_zero_cyclic_45_balanced_r12_seed_202609189": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 134,
        "rank": 134,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 11, "2": 22, "3": 24, "4": 32, "5": 28, "6": 17},
        "remaining_pairwise_equations": 3381,
        "remaining_equations_by_pair": {
            "1,2": 236,
            "1,3": 222,
            "1,4": 223,
            "1,5": 219,
            "1,6": 223,
            "2,3": 232,
            "2,4": 225,
            "2,5": 227,
            "2,6": 221,
            "3,4": 229,
            "3,5": 222,
            "3,6": 215,
            "4,5": 230,
            "4,6": 222,
            "5,6": 235,
        },
        "matrix_metadata_hash": "be8ea29a9c284334ec0d400bea2b0514f80e80dea3599184009fd1051c526591",
        "status": "RANK_COMPUTED",
    },
    "overlap_cycle_cyclic_3456_balanced_r12_seed_202608929": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 136,
        "rank": 136,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 19, "2": 23, "3": 24, "4": 30, "5": 26, "6": 14},
        "remaining_pairwise_equations": 3468,
        "remaining_equations_by_pair": {
            "1,2": 235,
            "1,3": 231,
            "1,4": 224,
            "1,5": 234,
            "1,6": 227,
            "2,3": 242,
            "2,4": 232,
            "2,5": 240,
            "2,6": 225,
            "3,4": 229,
            "3,5": 226,
            "3,6": 231,
            "4,5": 233,
            "4,6": 225,
            "5,6": 234,
        },
        "matrix_metadata_hash": "fde2879dbfa5ae62cbe65c170590606edd0967197889911ef1ebf3b97d72a5ce",
        "status": "RANK_COMPUTED",
    },
    "anchored_zero_cyclic_45_balanced_r0_seed_202609033": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 138,
        "rank": 138,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 14, "2": 28, "3": 31, "4": 26, "5": 32, "6": 7},
        "remaining_pairwise_equations": 3372,
        "remaining_equations_by_pair": {
            "1,2": 232,
            "1,3": 219,
            "1,4": 226,
            "1,5": 228,
            "1,6": 218,
            "2,3": 225,
            "2,4": 215,
            "2,5": 221,
            "2,6": 217,
            "3,4": 232,
            "3,5": 218,
            "3,6": 224,
            "4,5": 228,
            "4,6": 229,
            "5,6": 240,
        },
        "matrix_metadata_hash": "fc8230b95edd0588179434df9cc7884ee1692002249045603811d08bd2519f3a",
        "status": "RANK_COMPUTED",
    },
    "anchored_zero_cyclic_45_balanced_r16_seed_202609241": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 150,
        "rank": 150,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 13, "2": 34, "3": 23, "4": 29, "5": 29, "6": 22},
        "remaining_pairwise_equations": 3335,
        "remaining_equations_by_pair": {
            "1,2": 229,
            "1,3": 223,
            "1,4": 224,
            "1,5": 219,
            "1,6": 223,
            "2,3": 224,
            "2,4": 219,
            "2,5": 214,
            "2,6": 213,
            "3,4": 229,
            "3,5": 217,
            "3,6": 220,
            "4,5": 238,
            "4,6": 215,
            "5,6": 228,
        },
        "matrix_metadata_hash": "54ce4aee1820b9d7400a64d5e67edbd6642628ac347086c7a247df43c4f9e293",
        "status": "RANK_COMPUTED",
    },
    "anchored_zero_cyclic_45_balanced_r14_seed_202609215": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 152,
        "rank": 152,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 25, "2": 34, "3": 27, "4": 26, "5": 27, "6": 13},
        "remaining_pairwise_equations": 3396,
        "remaining_equations_by_pair": {
            "1,2": 236,
            "1,3": 222,
            "1,4": 225,
            "1,5": 224,
            "1,6": 217,
            "2,3": 240,
            "2,4": 224,
            "2,5": 222,
            "2,6": 209,
            "3,4": 238,
            "3,5": 219,
            "3,6": 221,
            "4,5": 243,
            "4,6": 220,
            "5,6": 236,
        },
        "matrix_metadata_hash": "1d2d260229d89b01171145837a44e4597ebad28fcdb9174397cef0a86b116f6e",
        "status": "RANK_COMPUTED",
    },
    "anchored_zero_cyclic_45_balanced_r8_seed_202609137": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 152,
        "rank": 152,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 23, "2": 30, "3": 33, "4": 29, "5": 24, "6": 13},
        "remaining_pairwise_equations": 3329,
        "remaining_equations_by_pair": {
            "1,2": 240,
            "1,3": 213,
            "1,4": 212,
            "1,5": 215,
            "1,6": 211,
            "2,3": 238,
            "2,4": 215,
            "2,5": 217,
            "2,6": 214,
            "3,4": 231,
            "3,5": 215,
            "3,6": 218,
            "4,5": 228,
            "4,6": 226,
            "5,6": 236,
        },
        "matrix_metadata_hash": "f16c572b31a9ed7134f53f8181910753531c29e3c49522cf8df488f6a34b1ece",
        "status": "RANK_COMPUTED",
    },
    "overlap_cycle_cyclic_3456_balanced_r6_seed_202608851": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 158,
        "rank": 158,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 20, "2": 37, "3": 29, "4": 29, "5": 27, "6": 16},
        "remaining_pairwise_equations": 3426,
        "remaining_equations_by_pair": {
            "1,2": 233,
            "1,3": 229,
            "1,4": 226,
            "1,5": 234,
            "1,6": 225,
            "2,3": 235,
            "2,4": 215,
            "2,5": 230,
            "2,6": 222,
            "3,4": 230,
            "3,5": 232,
            "3,6": 224,
            "4,5": 236,
            "4,6": 221,
            "5,6": 234,
        },
        "matrix_metadata_hash": "da645cb5869b6b85f39b02237973ec273f0056008c264d28c4dd909d7f8b1e46",
        "status": "RANK_COMPUTED",
    },
    "overlap_cycle_cyclic_3456_balanced_r2_seed_202608799": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 159,
        "rank": 159,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 16, "2": 25, "3": 32, "4": 34, "5": 32, "6": 20},
        "remaining_pairwise_equations": 3411,
        "remaining_equations_by_pair": {
            "1,2": 242,
            "1,3": 226,
            "1,4": 222,
            "1,5": 221,
            "1,6": 218,
            "2,3": 233,
            "2,4": 224,
            "2,5": 216,
            "2,6": 225,
            "3,4": 246,
            "3,5": 219,
            "3,6": 226,
            "4,5": 234,
            "4,6": 224,
            "5,6": 235,
        },
        "matrix_metadata_hash": "69132663d57d90f8a7c360bb50527cfe7125f7ad7b5947dced5e8585574c0252",
        "status": "RANK_COMPUTED",
    },
}


def load_rank_feedback_scanner():
    spec = importlib.util.spec_from_file_location(
        "m1_rank_feedback_scanner", RANK_FEEDBACK_SCANNER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


feedback = load_rank_feedback_scanner()
base = feedback.base
mult = feedback.mult


def pair_key(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def membership_key(members: list[int]) -> str:
    return ",".join(str(item) for item in sorted(members))


def equation_template_histogram(memberships: list[list[int]]) -> dict[str, int]:
    histogram: dict[str, int] = {}
    for pos, members in enumerate(memberships):
        residue = pos % 16
        members = sorted(members)
        anchored = 0 in members
        non_anchor = [item for item in members if item != 0]
        pairs = ["%d-%d" % pair for pair in combinations(non_anchor, 2)]
        template = (
            f"fiber={residue}:size={len(members)}:"
            f"anchor={int(anchored)}:pairs={'/'.join(pairs)}"
        )
        histogram[template] = histogram.get(template, 0) + 1
    return dict(sorted(histogram.items()))


def equation_template_summary(memberships: list[list[int]]) -> dict[str, Any]:
    histogram = equation_template_histogram(memberships)
    counts = sorted(histogram.values(), reverse=True)
    repeated = [count for count in counts if count > 1]
    return {
        "template_count": len(histogram),
        "largest_template_multiplicity": counts[0],
        "repeated_template_count": len(repeated),
        "repeated_template_square_sum": sum(count * count for count in repeated),
        "histogram_hash": base.hash_payload(histogram),
    }


def quotient_integer_profile(memberships: list[list[int]]) -> dict[str, Any]:
    rows = []
    for residue in range(16):
        positions = [pos for pos in range(N) if pos % 16 == residue]
        incidence = [0 for _idx in range(LIST_SIZE)]
        pair_counts = {pair: 0 for pair in combinations(range(LIST_SIZE), 2)}
        for pos in positions:
            members = sorted(memberships[pos])
            for member in members:
                incidence[member] += 1
            for pair in combinations(members, 2):
                pair_counts[pair_key(*pair)] += 1
        rows.append(
            {
                "residue": residue,
                "incidence": incidence,
                "pair_counts": {f"{a},{b}": value for (a, b), value in sorted(pair_counts.items())},
            }
        )
    incidence_rows = [tuple(row["incidence"]) for row in rows]
    return {
        "fiber_count": 16,
        "fiber_size": 32,
        "distinct_incidence_rows": len(set(incidence_rows)),
        "largest_incidence_row_multiplicity": max(incidence_rows.count(row) for row in set(incidence_rows)),
        "profile_hash": base.hash_payload(rows),
    }


def structural_scores(memberships: list[list[int]], family: str) -> dict[str, Any]:
    summary = base.support_summary(memberships)
    profile = base.quotient_fiber_profile(memberships)
    template = equation_template_summary(memberships)
    quotient_profile = quotient_integer_profile(memberships)
    compressed = base.compressed_variables(summary)

    cycle_score = 0
    anchor_score = 0
    high_multiplicity_score = 0
    for members in memberships:
        members_set = set(members)
        non_anchor_count = len([member for member in members if member != 0])
        if len(members) >= 5:
            high_multiplicity_score += len(members) * len(members)
        if 0 in members_set:
            anchor_score += 12 * non_anchor_count + non_anchor_count * non_anchor_count
        for cycle in ((1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (1, 3, 5), (2, 4, 6)):
            if set(cycle).issubset(members_set):
                cycle_score += 1

    repeated_score = (
        35 * template["repeated_template_square_sum"]
        + 800 * template["largest_template_multiplicity"]
        + 75 * sum(profile["largest_pattern_multiplicities"])
        + 900 * quotient_profile["largest_incidence_row_multiplicity"]
    )
    pair_score = (
        110_000 * summary["pair_intersections_at_255"]
        + 6_000 * summary["pair_intersections_at_254_or_255"]
        + summary["pair_intersection_square_sum"] // 50
    )
    compression_score = 900_000 - 6_000 * compressed
    spread_score = mult.multiplicity_spread_score(summary)

    family_bonus = 0
    if family == "quotient_template":
        family_bonus = repeated_score + 2_000 * quotient_profile["largest_incidence_row_multiplicity"]
    elif family == "overlap_cycle":
        family_bonus = 9_000 * cycle_score + repeated_score // 2
    elif family == "anchored_zero":
        family_bonus = 1_800 * anchor_score + compression_score
    elif family == "quotient_integer":
        family_bonus = 12_000 * (16 - quotient_profile["distinct_incidence_rows"]) + repeated_score

    total = pair_score + compression_score + 40_000 * spread_score + family_bonus
    return {
        "method": "constructive_rank_defect_structural_score",
        "family": family,
        "score": total,
        "compressed_variables": compressed,
        "repeated_template_square_sum": template["repeated_template_square_sum"],
        "largest_template_multiplicity": template["largest_template_multiplicity"],
        "cycle_score": cycle_score,
        "anchor_score": anchor_score,
        "high_multiplicity_score": high_multiplicity_score,
        "multiplicity_spread_score": spread_score,
        "pair_boundary_score": pair_score,
        "quotient_incidence_repetition": quotient_profile["largest_incidence_row_multiplicity"],
        "status": "SCORED",
    }


def valid_support(memberships: list[list[int]]) -> bool:
    summary = base.support_summary(memberships)
    return (
        summary["witness_support_sizes"] == [TARGET_AGREEMENT] * LIST_SIZE
        and summary["pair_intersection_max"] <= K - 1
    )


def propose_family_move(
    memberships: list[list[int]], rng: random.Random, family: str
) -> list[list[int]] | None:
    restrict_same_fiber = family in {"quotient_template", "quotient_integer"}
    force_size_change = family in {"overlap_cycle", "anchored_zero"}
    proposal = mult.propose_pair_replacement(
        memberships,
        rng,
        restrict_same_fiber=restrict_same_fiber,
        force_size_change=force_size_change,
    )
    if proposal is None:
        return None

    if family == "anchored_zero" and rng.random() < 0.35:
        with_anchor = [idx for idx, members in enumerate(proposal) if 0 in members and len(members) < LIST_SIZE]
        without_anchor = [idx for idx, members in enumerate(proposal) if 0 not in members and len(members) > 1]
        if with_anchor and without_anchor:
            a = rng.choice(with_anchor)
            b = rng.choice(without_anchor)
            movable = [member for member in proposal[b] if member != 0]
            if movable:
                member = rng.choice(movable)
                proposal = copy.deepcopy(proposal)
                proposal[a] = sorted(set(proposal[a]) | {member})
                proposal[b] = sorted(set(proposal[b]) - {member})
    return proposal


def mutate_constructive(
    memberships: list[list[int]], family: str, seed: int, steps: int
) -> tuple[list[list[int]], int, int]:
    rng = random.Random(seed)
    current = copy.deepcopy(memberships)
    current_score = structural_scores(current, family)["score"]
    accepted = 0
    attempted_valid = 0
    for _idx in range(steps):
        proposal = propose_family_move(current, rng, family)
        if proposal is None:
            continue
        if not valid_support(proposal):
            continue
        attempted_valid += 1
        proposal_score = structural_scores(proposal, family)["score"]
        if proposal_score > current_score or (
            proposal_score == current_score and rng.random() < 0.02
        ):
            current = proposal
            current_score = proposal_score
            accepted += 1
    assert valid_support(current)
    return current, accepted, attempted_valid


def generated_candidate_specs() -> list[dict[str, Any]]:
    seed_by_family = {
        "quotient_template": ["cyclic_3456_balanced", "cyclic_45_balanced"],
        "overlap_cycle": ["cyclic_3456_balanced", "cyclic_3456_near_boundary"],
        "anchored_zero": ["cyclic_45_balanced", "cyclic_45_interval_high_overlap"],
        "quotient_integer": ["cyclic_3456_balanced", "cyclic_45_interval_high_overlap"],
    }
    specs = []
    counter = 202608500
    for family, seeds in seed_by_family.items():
        for repeat in range(20):
            seed_name = seeds[repeat % len(seeds)]
            counter += 13
            specs.append(
                {
                    "family": family,
                    "seed_name": seed_name,
                    "repeat": repeat,
                    "random_seed": counter,
                    "steps": 520,
                }
            )
    assert len(specs) == GENERATED_CANDIDATES
    return specs


def generated_candidates() -> list[dict[str, Any]]:
    rows = []
    for spec in generated_candidate_specs():
        seed_memberships = base.seed_memberships(spec["seed_name"])
        memberships, accepted, attempted_valid = mutate_constructive(
            seed_memberships,
            family=spec["family"],
            seed=spec["random_seed"],
            steps=spec["steps"],
        )
        summary = base.support_summary(memberships)
        profile = base.quotient_fiber_profile(memberships)
        template = equation_template_summary(memberships)
        quotient_profile = quotient_integer_profile(memberships)
        structural = structural_scores(memberships, spec["family"])
        surrogate = feedback.surrogate_rank_gate(memberships)
        candidate_id = (
            f"{spec['family']}_{spec['seed_name']}_"
            f"r{spec['repeat']}_seed_{spec['random_seed']}"
        )
        rows.append(
            {
                "candidate_id": candidate_id,
                "construction_family": spec["family"],
                "mutation_family": "constructive_rank_defect_membership_hypergraph",
                "seed_design": spec["seed_name"],
                "random_seed": spec["random_seed"],
                "repeat": spec["repeat"],
                "mutation_steps": spec["steps"],
                "valid_mutation_attempts": attempted_valid,
                "accepted_mutations": accepted,
                "memberships": memberships,
                "support_design": summary,
                "quotient_fiber_profile": profile,
                "equation_template_summary": template,
                "quotient_integer_profile": quotient_profile,
                "structural_score": structural,
                "surrogate_rank_gate": surrogate,
            }
        )
    return rows


def retained_candidates() -> list[dict[str, Any]]:
    rows = generated_candidates()
    rows.sort(
        key=lambda row: (
            row["surrogate_rank_gate"]["nullity"] or 0,
            -row["surrogate_rank_gate"]["rank"],
            -row["surrogate_rank_gate"]["compressed_variables"],
            row["equation_template_summary"]["repeated_template_square_sum"],
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
        proof_status = (
            "ROUTE_CUT_TESTED_CANDIDATE"
            if exact_gate.get("nullity") == 0
            else "CANDIDATE_PROXY_NULLITY"
            if candidate["surrogate_rank_gate"].get("nullity") not in {None, 0}
            else "CANDIDATE"
        )
        row = {key: value for key, value in candidate.items() if key != "memberships"}
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


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def build_result() -> dict[str, Any]:
    candidates = build_candidates()
    exact_rows = [row for row in candidates if row["sage_exact_rank"]["status"] != "NOT_RUN"]
    best_exact_nullity = max(
        (row["sage_exact_rank"]["nullity"] or 0 for row in exact_rows),
        default=None,
    )
    proxy_positive_count = sum(
        1 for row in candidates if row["surrogate_rank_gate"]["nullity"] not in {None, 0}
    )
    family_counts: dict[str, int] = {}
    for row in candidates:
        family = row["construction_family"]
        family_counts[family] = family_counts.get(family, 0) + 1
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
            "generated_candidate_count": GENERATED_CANDIDATES,
            "retained_candidate_count": len(candidates),
            "exact_audited_count": len(exact_rows),
            "candidate_family": "constructive repeated-template support designs",
            "construction_families": [
                "quotient_template",
                "overlap_cycle",
                "anchored_zero",
                "quotient_integer",
            ],
            "retained_family_counts": dict(sorted(family_counts.items())),
            "rank_proxy": "GF(12289) reduced rank plus equation-template structural score",
            "surrogate_field": "GF(12289), 512 | 12288",
            "exact_field": "GF(17^32)",
            "proxy_positive_count": proxy_positive_count,
            "best_exact_nullity": best_exact_nullity,
            "status": status,
        },
        "candidates": candidates,
        "interpretation": {
            "support_packing_blocks_a327": False,
            "constructive_search_found_proxy_nullity": proxy_positive_count > 0,
            "exact_audited_candidate_found_nullity": best_exact_nullity not in {0, None},
            "candidate_found": False,
            "status": status,
        },
        "open_layers": {
            "larger_constructive_search": True,
            "direct_symbolic_rank_defect_construction": True,
            "positive_exact_nullity_candidate": best_exact_nullity not in {0, None},
            "non_diagonal_nullspace_extraction": True,
            "global_support_pattern_rank_nullity_classification": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_constructive_rank_defect_support_design.sage",
            "recomputes_retained_candidates": True,
            "constructs_GF_17_32": True,
            "checks_surrogate_rank_gate": True,
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
                "global support-pattern rank-nullity classification",
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
        "status": "M1_CONSTRUCTIVE_RANK_DEFECT_SUPPORT_DESIGN_ROUTE_CUT_PARTIAL",
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
                "family": row["construction_family"],
                "structural_score": row["structural_score"]["score"],
                "support_hash": row["support_design"]["support_hash"],
                "multiplicity_histogram": row["support_design"]["multiplicity_histogram"],
                "pair_max": row["support_design"]["pair_intersection_max"],
                "pairs_at_255": row["support_design"]["pair_intersections_at_255"],
                "surrogate_rank": row["surrogate_rank_gate"]["rank"],
                "surrogate_nullity": row["surrogate_rank_gate"]["nullity"],
                "compressed_variables": row["surrogate_rank_gate"]["compressed_variables"],
                "largest_template_multiplicity": row["equation_template_summary"][
                    "largest_template_multiplicity"
                ],
                "repeated_template_square_sum": row["equation_template_summary"][
                    "repeated_template_square_sum"
                ],
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
        print(f"generated {GENERATED_CANDIDATES} constructive support designs")
        print(f"retained {len(result['candidates'])} candidates after GF(12289) rank feedback")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
