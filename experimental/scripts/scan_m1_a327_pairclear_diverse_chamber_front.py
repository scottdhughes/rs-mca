#!/usr/bin/env python3
"""Diverse pair-clear chamber front for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "dbad852"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_template_chamber_mutation_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_diverse_chamber_front.json")

ROOT = Path(__file__).resolve().parents[2]
TCHAMBER_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_template_chamber_mutation_search.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tchamber = load_module("pairclear_template_chamber_mutation_search", TCHAMBER_SCRIPT)
chamber = tchamber.chamber
ninerow = tchamber.ninerow
lowrank = tchamber.lowrank
zstable = tchamber.zstable
basisaware = tchamber.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize_projective(vector: list[int]) -> list[int]:
    values = [int(value) % P for value in vector]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return [(entry * inv) % P for entry in values]
    return values


def mutation_category(mutation_id: str | None) -> tuple[Any, ...]:
    mutation = mutation_id or ""
    if mutation.startswith("base"):
        return ("base",)
    match = re.match(r"w(\d+)_c(\d+)_d(\d+)$", mutation)
    if match:
        return ("single", int(match.group(1)), int(match.group(2)))
    match = re.match(r"P(\d+)(\d+)_shear_c(\d+)(?:_d(\d+))?$", mutation)
    if match:
        return ("shear", int(match.group(1)), int(match.group(2)), int(match.group(3)))
    match = re.match(r"W(\d+)(\d+)_c(\d)(\d)_pm1$", mutation)
    if match:
        return ("double", int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))
    return ("other", mutation)


def direction_key(vector: list[int]) -> tuple[int, ...]:
    return tuple(normalize_projective(vector))


def sampled_projective_directions(limit: int, seed: int = 327091) -> list[list[int]]:
    """Deterministic broad sample, including low-weight and random directions."""
    directions: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()

    def add(vector: list[int]) -> None:
        key = direction_key(vector)
        if key in seen or all(value == 0 for value in key):
            return
        seen.add(key)
        directions.append(list(key))

    # Known productive direction and low-weight projective directions.
    add([0, 1, 0, 0, 0, 7])
    for idx in range(TEMPLATE_DIM):
        vector = [0] * TEMPLATE_DIM
        vector[idx] = 1
        add(vector)
    for i in range(TEMPLATE_DIM):
        for j in range(i + 1, TEMPLATE_DIM):
            for value in range(1, P):
                vector = [0] * TEMPLATE_DIM
                vector[i] = 1
                vector[j] = value
                add(vector)
    for i in range(TEMPLATE_DIM):
        for j in range(i + 1, TEMPLATE_DIM):
            for k in range(j + 1, TEMPLATE_DIM):
                for a in range(1, P):
                    for b in range(1, P):
                        vector = [0] * TEMPLATE_DIM
                        vector[i] = 1
                        vector[j] = a
                        vector[k] = b
                        add(vector)
                        if len(directions) >= limit:
                            return directions

    rng = random.Random(seed)
    while len(directions) < limit:
        vector = [rng.randrange(P) for _ in range(TEMPLATE_DIM)]
        if any(vector):
            add(vector)
    return directions


def candidate_from_profile(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    candidate = lowrank.evaluate_candidate(profile, strategy, seed=seed)
    candidate["mutation_id"] = profile.get("mutation_id")
    candidate["base_template_id"] = profile.get("base_template_id")
    candidate["total_effective_cost"] = ninerow.syzygy.rowred.total_effective_cost_gf17(
        profile["template_vectors"],
        candidate["coordinate_classes"],
    )
    return candidate


def diverse_candidates(
    structural_pass: list[tuple[dict[str, Any], dict[str, Any]]],
    limit: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    used_categories: set[tuple[Any, ...]] = set()
    used_assignment_categories: set[tuple[tuple[Any, ...], str]] = set()

    # First pass: category coverage across witnesses, coordinates, and shears.
    for item in structural_pass:
        candidate, _row = item
        category = mutation_category(candidate.get("mutation_id"))
        if category in used_categories:
            continue
        selected.append(item)
        used_categories.add(category)
        used_assignment_categories.add((category, candidate["assignment_strategy"]))
        if len(selected) >= limit:
            return selected

    # Second pass: assignment variants inside already-seen categories.
    for item in structural_pass:
        candidate, _row = item
        category = mutation_category(candidate.get("mutation_id"))
        key = (category, candidate["assignment_strategy"])
        if key in used_assignment_categories:
            continue
        selected.append(item)
        used_assignment_categories.add(key)
        if len(selected) >= limit:
            return selected

    return selected[:limit]


def cheap_score_profile(candidate: dict[str, Any], profile: dict[str, Any], directions: list[list[int]]) -> dict[str, Any]:
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    _pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)

    chamber_exemplars: dict[tuple[int, ...], list[int]] = {}
    pair_clear_directions = 0
    support_reduced_directions = 0
    rank_slack_directions = 0
    for vector in directions:
        pair_values = chamber.linear_image_rows(pair_rows, vector)
        if any(value % P == 0 for value in pair_values):
            continue
        pair_clear_directions += 1
        row_values = chamber.linear_image_rows(matrix, vector)
        zero_indices = tuple(idx for idx, value in enumerate(row_values) if value % P == 0)
        if len(zero_indices) >= 6:
            support_reduced_directions += 1
        if len(zero_indices) >= 5 and chamber.rank_rows([matrix[idx] for idx in zero_indices]) <= 4:
            rank_slack_directions += 1
        old = chamber_exemplars.get(zero_indices)
        if old is None or (sum(1 for value in vector if value % P), vector) < (sum(1 for value in old if value % P), old):
            chamber_exemplars[zero_indices] = vector

    chambers = [
        chamber.chamber_record(zero_indices, matrix, row_classes, exemplar)
        for zero_indices, exemplar in chamber_exemplars.items()
    ]
    nine_or_better = [row for row in chambers if row["zero_row_count"] >= 5]
    direct_support_reduced = [row for row in chambers if row["zero_row_count"] >= 6]
    rank_slack = [row for row in chambers if row["zero_row_count"] >= 5 and row["inactive_rank"] <= 4]
    best_chamber = min(chambers, key=chamber.chamber_sort_key) if chambers else None
    best_nine = min(nine_or_better, key=chamber.chamber_sort_key) if nine_or_better else None
    best_direct = min(direct_support_reduced, key=chamber.chamber_sort_key) if direct_support_reduced else None
    best_rank_slack = min(rank_slack, key=chamber.rank_slack_sort_key) if rank_slack else None
    failure = "DCHAMBER_NO_PAIR_CLEAR_CHAMBER"
    if best_direct is not None:
        failure = "DCHAMBER_SAMPLE_SUPPORT_REDUCED"
    elif best_rank_slack is not None:
        failure = "DCHAMBER_SAMPLE_RANK_SLACK"
    elif best_nine is not None:
        failure = "DCHAMBER_SAMPLE_NINE_ROW"
    elif best_chamber is not None:
        failure = "DCHAMBER_SAMPLE_LOWER_SUPPORT"

    return {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "mutation_category": list(mutation_category(candidate.get("mutation_id"))),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "directions_sampled": len(directions),
        "pair_clear_directions": pair_clear_directions,
        "distinct_pair_clear_chambers": len(chambers),
        "sample_nine_row_or_better_chambers": len(nine_or_better),
        "sample_direct_support_reduced_chambers": len(direct_support_reduced),
        "sample_rank_slack_chambers": len(rank_slack),
        "sample_direct_support_reduced_directions": support_reduced_directions,
        "sample_rank_slack_directions": rank_slack_directions,
        "best_sample_chamber": best_chamber,
        "best_sample_nine_row_chamber": best_nine,
        "best_sample_direct_support_reduced_chamber": best_direct,
        "best_sample_rank_slack_chamber": best_rank_slack,
        "best_failure_mode": failure,
    }


def sample_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    priority = {
        "DCHAMBER_SAMPLE_SUPPORT_REDUCED": 0,
        "DCHAMBER_SAMPLE_RANK_SLACK": 1,
        "DCHAMBER_SAMPLE_NINE_ROW": 2,
        "DCHAMBER_SAMPLE_LOWER_SUPPORT": 3,
        "DCHAMBER_NO_PAIR_CLEAR_CHAMBER": 4,
    }.get(row["best_failure_mode"], 9)
    best = (
        row.get("best_sample_direct_support_reduced_chamber")
        or row.get("best_sample_rank_slack_chamber")
        or row.get("best_sample_nine_row_chamber")
        or row.get("best_sample_chamber")
        or {}
    )
    return (
        priority,
        -(best.get("zero_row_count", 0)),
        best.get("inactive_rank", 99),
        -row["pair_clear_directions"],
        row["template_id"],
        row["basis_id"],
    )


def select_full_profiles(sampled: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    used_categories: set[tuple[Any, ...]] = set()
    used_basis: set[str] = set()
    for row in sorted(sampled, key=sample_sort_key):
        category = tuple(row["mutation_category"])
        if category in used_categories and row["basis_id"] in used_basis:
            continue
        selected.append(row)
        used_categories.add(category)
        used_basis.add(row["basis_id"])
        if len(selected) >= limit:
            return selected
    return selected[:limit]


def compact_sample(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "mutation_id",
        "mutation_category",
        "assignment_strategy",
        "basis_id",
        "basis_class_indices",
        "coefficient_matrix_shape",
        "directions_sampled",
        "pair_clear_directions",
        "distinct_pair_clear_chambers",
        "sample_nine_row_or_better_chambers",
        "sample_direct_support_reduced_chambers",
        "sample_rank_slack_chambers",
        "best_failure_mode",
        "best_sample_chamber",
        "best_sample_nine_row_chamber",
        "best_sample_direct_support_reduced_chamber",
        "best_sample_rank_slack_chamber",
    ]
    return {key: row.get(key) for key in keys}


def compact_full(row: dict[str, Any]) -> dict[str, Any]:
    return tchamber.compact_score(row)


def build_record(
    max_mutations: int,
    max_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
    sample_directions: int,
    full_profiles: int,
    extension_chamber_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    specs = ninerow.mutation_specs(max_mutations=max_mutations)
    profiles = []
    for spec in specs:
        profile = lowrank.solve_template_counts(spec)
        profile["mutation_id"] = spec.get("mutation_id")
        profile["base_template_id"] = spec.get("base_template_id")
        profiles.append(profile)

    candidates = []
    for profile_index, profile in enumerate(profiles):
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for strategy_index, strategy in enumerate(profile["assignment_strategies"]):
            candidates.append(tchamber.candidate_from_profile(profile, strategy, seed=106000 + 97 * profile_index + strategy_index))

    screened = [(candidate, tchamber.candidate_screen_row(candidate)) for candidate in candidates]
    structural_pass = [
        (candidate, row)
        for candidate, row in screened
        if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
    ]
    structural_pass.sort(key=tchamber.candidate_sort_key)
    selected_candidates = diverse_candidates(structural_pass, max_candidates)
    directions = sampled_projective_directions(sample_directions)

    sampled = []
    profile_lookup: dict[tuple[str, str, int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    for candidate, _row in selected_candidates:
        profiles_for_candidate = tchamber.basis_profiles(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            limit=max_basis_profiles,
        )
        for profile in profiles_for_candidate:
            score = cheap_score_profile(candidate, profile, directions)
            sampled.append(score)
            profile_lookup[
                (
                    score["template_id"],
                    score["assignment_strategy"],
                    score["assignment_seed"],
                    score["basis_id"],
                )
            ] = (candidate, profile)

    full_inputs = select_full_profiles(sampled, full_profiles)
    full_scores = []
    for row in full_inputs:
        key = (row["template_id"], row["assignment_strategy"], row["assignment_seed"], row["basis_id"])
        candidate, profile = profile_lookup[key]
        full_scores.append(
            tchamber.score_profile(
                candidate,
                profile,
                direction_limit=None,
                extension_chamber_limit=extension_chamber_limit,
            )
        )

    best_full = min(full_scores, key=tchamber.score_sort_key) if full_scores else None
    best_sample = min(sampled, key=sample_sort_key) if sampled else None
    failure = "DCHAMBER_NO_SCORED_PROFILES"
    if best_full is not None:
        failure = best_full["best_failure_mode"].replace("TCHAMBER", "DCHAMBER")
    elif best_sample is not None:
        failure = best_sample["best_failure_mode"]

    if failure == "DCHAMBER_DIRECT_SUPPORT_REDUCED":
        proof_status = "CANDIDATE / DCHAMBER_DIRECT_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL"
    elif failure == "DCHAMBER_EXTENSION_SUPPORT_REDUCED":
        proof_status = "CANDIDATE / DCHAMBER_EXTENSION_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL"
    elif failure == "DCHAMBER_RANK_SLACK_FOUND":
        proof_status = "CANDIDATE / DCHAMBER_RANK_SLACK_FOUND / PARTIAL / EXPERIMENTAL"
    elif failure in {"DCHAMBER_NINE_ROW_STABLE", "DCHAMBER_LOWER_SUPPORT_ONLY"}:
        proof_status = f"CANDIDATE / {failure}_FRONT / PARTIAL / EXPERIMENTAL"
    else:
        proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    previous_search = previous["template_chamber_search"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_template_chamber_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_scored": previous_search["basis_profiles_scored"],
            "directions_tested": previous_search["directions_tested"],
            "pair_clear_directions": previous_search["pair_clear_directions"],
            "rank_slack_profiles": previous_search["rank_slack_profiles"],
            "support_reduced_extension_profiles": previous_search["support_reduced_extension_profiles"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "diverse_chamber_front": {
            "max_mutations": max_mutations,
            "max_candidates": max_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "sample_directions": len(directions),
            "full_profiles": full_profiles,
            "extension_chamber_limit": extension_chamber_limit,
            "mutations_generated": len(specs),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": len(candidates),
            "structural_pass_candidates": len(structural_pass),
            "diverse_candidates_selected": len(selected_candidates),
            "sampled_profiles": len(sampled),
            "full_profiles_scanned": len(full_scores),
            "sample_pair_clear_directions": sum(row["pair_clear_directions"] for row in sampled),
            "sample_direct_support_reduced_profiles": sum(1 for row in sampled if row["sample_direct_support_reduced_chambers"] > 0),
            "sample_rank_slack_profiles": sum(1 for row in sampled if row["sample_rank_slack_chambers"] > 0),
            "sample_nine_row_or_better_profiles": sum(1 for row in sampled if row["sample_nine_row_or_better_chambers"] > 0),
            "full_directions_tested": sum(row["directions_tested"] for row in full_scores),
            "full_pair_clear_directions": sum(row["pair_clear_directions"] for row in full_scores),
            "full_direct_support_reduced_profiles": sum(1 for row in full_scores if row["direct_support_reduced_chambers"] > 0),
            "full_rank_slack_profiles": sum(1 for row in full_scores if row["rank_slack_chambers"] > 0),
            "full_support_reduced_extension_profiles": sum(1 for row in full_scores if row["support_reduced_extensions"] > 0),
            "best_template_id": None if best_full is None else best_full["template_id"],
            "best_mutation_id": None if best_full is None else best_full.get("mutation_id"),
            "best_assignment_strategy": None if best_full is None else best_full["assignment_strategy"],
            "best_basis_id": None if best_full is None else best_full["basis_id"],
            "best_failure_mode": failure,
            "sample_failure_counts": dict(Counter(row["best_failure_mode"] for row in sampled)),
            "full_failure_counts": dict(Counter(row["best_failure_mode"] for row in full_scores)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in screened)),
            "sampled_profile_summaries": [compact_sample(row) for row in sorted(sampled, key=sample_sort_key)[:20]],
            "full_profile_summaries": [compact_full(row) for row in sorted(full_scores, key=tchamber.score_sort_key)],
        },
        "best_sample_profile": None if best_sample is None else compact_sample(best_sample),
        "best_full_profile": None if best_full is None else compact_full(best_full),
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "Sage GF(17^32) exact lift",
            "MCA/protocol consequence from this list-track proxy",
            "global obstruction outside the tested diverse chamber front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=96)
    parser.add_argument("--max-candidates", type=int, default=24)
    parser.add_argument("--top-classes", type=int, default=14)
    parser.add_argument("--random-bases", type=int, default=24)
    parser.add_argument("--max-basis-profiles", type=int, default=2)
    parser.add_argument("--sample-directions", type=int, default=50000)
    parser.add_argument("--full-profiles", type=int, default=4)
    parser.add_argument("--extension-chamber-limit", type=int, default=80)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
        sample_directions=args.sample_directions,
        full_profiles=args.full_profiles,
        extension_chamber_limit=args.extension_chamber_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["diverse_chamber_front"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "mutations_generated": search["mutations_generated"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "diverse_candidates_selected": search["diverse_candidates_selected"],
                    "sampled_profiles": search["sampled_profiles"],
                    "full_profiles_scanned": search["full_profiles_scanned"],
                    "sample_pair_clear_directions": search["sample_pair_clear_directions"],
                    "sample_direct_support_reduced_profiles": search["sample_direct_support_reduced_profiles"],
                    "sample_rank_slack_profiles": search["sample_rank_slack_profiles"],
                    "full_directions_tested": search["full_directions_tested"],
                    "full_direct_support_reduced_profiles": search["full_direct_support_reduced_profiles"],
                    "full_rank_slack_profiles": search["full_rank_slack_profiles"],
                    "full_support_reduced_extension_profiles": search["full_support_reduced_extension_profiles"],
                    "best_template_id": search["best_template_id"],
                    "best_mutation_id": search["best_mutation_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_failure_mode": search["best_failure_mode"],
                    "sample_failure_counts": search["sample_failure_counts"],
                    "full_failure_counts": search["full_failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_DIVERSE_CHAMBER_FRONT_READY")


if __name__ == "__main__":
    main()
