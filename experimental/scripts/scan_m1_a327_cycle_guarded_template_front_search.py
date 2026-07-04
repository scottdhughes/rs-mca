#!/usr/bin/env python3
"""Cycle-guarded high-level template front search for M1 a=327 pair-clear."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "a63ab87"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_support_augmentation_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycle_guarded_template_front_search.json")

ROOT = Path(__file__).resolve().parents[2]
P456_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_p45_p46_p56_codesign.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
CYCLE_PAIRS = ["P14", "P16", "P17", "P45", "P46", "P47", "P56", "P57", "P67"]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p456 = load_module("pairclear_p45_p46_p56_codesign", P456_SCRIPT)
tchamber = p456.tchamber
chamber = p456.chamber
zstable = p456.zstable
diverse = p456.diverse


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def direction_weight(vector: list[int] | None) -> int | None:
    if vector is None:
        return None
    return sum(1 for value in vector if int(value) % P)


def forced_pair_info(pair_labels: list[str], pair_values: list[int]) -> dict[str, Any]:
    forced_pairs = [pair_labels[idx] for idx, value in enumerate(pair_values) if value % P == 0]
    forced_set = set(forced_pairs)
    return {
        "forced_pair_count": len(forced_pairs),
        "forced_pairs": forced_pairs,
        "cycle_forced_count": sum(1 for pair in forced_pairs if pair in CYCLE_PAIRS),
        "cycle_pairs_cleared": [pair for pair in CYCLE_PAIRS if pair not in forced_set],
        "noncycle_forced_pairs": [pair for pair in forced_pairs if pair not in CYCLE_PAIRS],
    }


def chamber_record_for(
    zero_indices: tuple[int, ...],
    matrix: list[list[int]],
    row_classes: list[int],
    vector: list[int],
    info: dict[str, Any],
) -> dict[str, Any]:
    row = chamber.chamber_record(zero_indices, matrix, row_classes, vector)
    row["direction"] = vector
    row["direction_weight"] = direction_weight(vector)
    row.update(info)
    return row


def guarded_score_profile(candidate: dict[str, Any], profile: dict[str, Any], directions: list[list[int]]) -> dict[str, Any]:
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)

    cycle_clear_exemplars: dict[tuple[int, ...], tuple[list[int], dict[str, Any]]] = {}
    exact_pairclear_exemplars: dict[tuple[int, ...], tuple[list[int], dict[str, Any]]] = {}
    cycle_clear_directions = 0
    exact_pairclear_directions = 0
    cycle_clear_support_reduced_directions = 0
    cycle_clear_rank_slack_directions = 0
    exact_pairclear_rank_slack_directions = 0
    cycle_forced_counts = Counter()
    total_forced_counts = Counter()
    forced_patterns = Counter()

    for vector in directions:
        pair_values = chamber.linear_image_rows(pair_rows, vector)
        info = forced_pair_info(pair_labels, pair_values)
        cycle_forced_counts[str(info["cycle_forced_count"])] += 1
        total_forced_counts[str(info["forced_pair_count"])] += 1
        forced_patterns[",".join(info["forced_pairs"])] += 1
        if info["cycle_forced_count"] != 0:
            continue
        cycle_clear_directions += 1
        row_values = chamber.linear_image_rows(matrix, vector)
        zero_indices = tuple(idx for idx, value in enumerate(row_values) if value % P == 0)
        if len(zero_indices) >= 6:
            cycle_clear_support_reduced_directions += 1
        rank = chamber.rank_rows([matrix[idx] for idx in zero_indices]) if zero_indices else 0
        if len(zero_indices) >= 5 and rank <= 4:
            cycle_clear_rank_slack_directions += 1
        old = cycle_clear_exemplars.get(zero_indices)
        if old is None or (
            info["forced_pair_count"],
            direction_weight(vector),
            vector,
        ) < (
            old[1]["forced_pair_count"],
            direction_weight(old[0]),
            old[0],
        ):
            cycle_clear_exemplars[zero_indices] = (vector, info)
        if info["forced_pair_count"] == 0:
            exact_pairclear_directions += 1
            if len(zero_indices) >= 5 and rank <= 4:
                exact_pairclear_rank_slack_directions += 1
            old_exact = exact_pairclear_exemplars.get(zero_indices)
            if old_exact is None or (direction_weight(vector), vector) < (direction_weight(old_exact[0]), old_exact[0]):
                exact_pairclear_exemplars[zero_indices] = (vector, info)

    cycle_chambers = [
        chamber_record_for(zero_indices, matrix, row_classes, vector, info)
        for zero_indices, (vector, info) in cycle_clear_exemplars.items()
    ]
    exact_chambers = [
        chamber_record_for(zero_indices, matrix, row_classes, vector, info)
        for zero_indices, (vector, info) in exact_pairclear_exemplars.items()
    ]
    cycle_rank_slack = [
        row for row in cycle_chambers if row["zero_row_count"] >= 5 and row["inactive_rank"] <= 4
    ]
    cycle_support_reduced = [row for row in cycle_chambers if row["zero_row_count"] >= 6]
    exact_rank_slack = [
        row for row in exact_chambers if row["zero_row_count"] >= 5 and row["inactive_rank"] <= 4
    ]

    best_cycle = min(
        cycle_chambers,
        key=lambda row: (
            row["forced_pair_count"],
            -row["zero_row_count"],
            row["inactive_rank"],
            row["direction_weight"],
            row["direction"],
        ),
    ) if cycle_chambers else None
    best_cycle_rank = min(
        cycle_rank_slack,
        key=lambda row: (
            row["forced_pair_count"],
            -row["zero_row_count"],
            row["inactive_rank"],
            row["direction_weight"],
            row["direction"],
        ),
    ) if cycle_rank_slack else None
    best_exact = min(exact_chambers, key=chamber.chamber_sort_key) if exact_chambers else None
    best_exact_rank = min(exact_rank_slack, key=chamber.rank_slack_sort_key) if exact_rank_slack else None

    failure = "CYCLEG_TEMPLATE_NO_CYCLE_CLEAR_DIRECTION"
    if best_exact_rank is not None:
        failure = "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK"
    elif best_exact is not None:
        failure = "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_ONLY"
    elif best_cycle_rank is not None:
        failure = "CYCLEG_TEMPLATE_CYCLE_CLEAR_RANKSLACK"
    elif cycle_support_reduced:
        failure = "CYCLEG_TEMPLATE_CYCLE_CLEAR_SUPPORT_REDUCED"
    elif best_cycle is not None:
        failure = "CYCLEG_TEMPLATE_CYCLE_CLEAR_ONLY"

    return {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "directions_sampled": len(directions),
        "cycle_clear_directions": cycle_clear_directions,
        "exact_pairclear_directions": exact_pairclear_directions,
        "cycle_clear_support_reduced_directions": cycle_clear_support_reduced_directions,
        "cycle_clear_rank_slack_directions": cycle_clear_rank_slack_directions,
        "exact_pairclear_rank_slack_directions": exact_pairclear_rank_slack_directions,
        "cycle_clear_chambers": len(cycle_chambers),
        "exact_pairclear_chambers": len(exact_chambers),
        "cycle_forced_count_histogram": dict(cycle_forced_counts),
        "total_forced_count_histogram": dict(total_forced_counts),
        "forced_pair_pattern_counts": dict(forced_patterns.most_common(12)),
        "best_cycle_clear_chamber": best_cycle,
        "best_cycle_clear_rank_slack_chamber": best_cycle_rank,
        "best_exact_pairclear_chamber": best_exact,
        "best_exact_pairclear_rank_slack_chamber": best_exact_rank,
        "best_failure_mode": failure,
    }


def score_key(row: dict[str, Any]) -> tuple[Any, ...]:
    priority = {
        "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK": 0,
        "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_ONLY": 1,
        "CYCLEG_TEMPLATE_CYCLE_CLEAR_RANKSLACK": 2,
        "CYCLEG_TEMPLATE_CYCLE_CLEAR_SUPPORT_REDUCED": 3,
        "CYCLEG_TEMPLATE_CYCLE_CLEAR_ONLY": 4,
        "CYCLEG_TEMPLATE_NO_CYCLE_CLEAR_DIRECTION": 5,
    }.get(row["best_failure_mode"], 9)
    best = (
        row.get("best_exact_pairclear_rank_slack_chamber")
        or row.get("best_exact_pairclear_chamber")
        or row.get("best_cycle_clear_rank_slack_chamber")
        or row.get("best_cycle_clear_chamber")
        or {}
    )
    return (
        priority,
        best.get("forced_pair_count", 99),
        -(best.get("zero_row_count", 0)),
        best.get("inactive_rank", 99),
        -row["cycle_clear_directions"],
        -row["exact_pairclear_directions"],
        row["template_id"],
        row["basis_id"],
    )


def compact_profile(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "mutation_id",
        "assignment_strategy",
        "assignment_seed",
        "basis_id",
        "basis_class_indices",
        "basis_support_sizes",
        "coefficient_matrix_shape",
        "directions_sampled",
        "cycle_clear_directions",
        "exact_pairclear_directions",
        "cycle_clear_support_reduced_directions",
        "cycle_clear_rank_slack_directions",
        "exact_pairclear_rank_slack_directions",
        "cycle_clear_chambers",
        "exact_pairclear_chambers",
        "best_cycle_clear_chamber",
        "best_cycle_clear_rank_slack_chamber",
        "best_exact_pairclear_chamber",
        "best_exact_pairclear_rank_slack_chamber",
        "best_failure_mode",
    ]
    return {key: row.get(key) for key in keys}


def build_record(
    max_mutations: int,
    seed_offsets: int,
    max_candidates: int,
    max_diverse_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
    sample_directions: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, screened, selected_candidates = p456.structural_candidates(
        max_mutations=max_mutations,
        seed_offsets=seed_offsets,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )
    directions = diverse.sampled_projective_directions(sample_directions)
    analyzed = []
    basis_profiles_tested = 0
    for candidate, _screen in selected_candidates:
        for profile in tchamber.basis_profiles(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            limit=max_basis_profiles,
        ):
            basis_profiles_tested += 1
            analyzed.append(guarded_score_profile(candidate, profile, directions))

    best = min(analyzed, key=score_key) if analyzed else None
    cycle_clear_profiles = [row for row in analyzed if row["cycle_clear_directions"] > 0]
    exact_profiles = [row for row in analyzed if row["exact_pairclear_directions"] > 0]
    cycle_rank_profiles = [row for row in analyzed if row["cycle_clear_rank_slack_directions"] > 0]
    exact_rank_profiles = [row for row in analyzed if row["exact_pairclear_rank_slack_directions"] > 0]

    failure = "CYCLEG_TEMPLATE_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / CYCLEG_TEMPLATE_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if best:
        failure = best["best_failure_mode"]
        if failure in {
            "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK",
            "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_ONLY",
            "CYCLEG_TEMPLATE_CYCLE_CLEAR_RANKSLACK",
            "CYCLEG_TEMPLATE_CYCLE_CLEAR_SUPPORT_REDUCED",
            "CYCLEG_TEMPLATE_CYCLE_CLEAR_ONLY",
        }:
            proof_status = f"CANDIDATE / {failure} / PARTIAL / EXPERIMENTAL"
        else:
            proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_support_augmentation": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_tested": previous["support_augmentation_search"]["basis_profiles_tested"],
            "extended_rank_slack_profiles": previous["support_augmentation_search"]["extended_rank_slack_profiles"],
            "exact_pairclear_profiles": previous["support_augmentation_search"]["exact_pairclear_profiles"],
            "best_forced_pairs": previous["best_profile"]["extended_exchange_direction"]["forced_pairs"],
        },
        "cycle_guarded_template_front": {
            "cycle_pairs": CYCLE_PAIRS,
            "max_mutations": max_mutations,
            "seed_offsets": seed_offsets,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "sample_directions": sample_directions,
            "mutations_generated": len(profiles),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE") * 3 * seed_offsets,
            "structural_pass_candidates": sum(
                1 for _candidate, row in screened if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
            ),
            "selected_candidates": len(selected_candidates),
            "basis_profiles_tested": basis_profiles_tested,
            "cycle_clear_profiles": len(cycle_clear_profiles),
            "exact_pairclear_profiles": len(exact_profiles),
            "cycle_clear_rank_slack_profiles": len(cycle_rank_profiles),
            "exact_pairclear_rank_slack_profiles": len(exact_rank_profiles),
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_id": None if best is None else best["basis_id"],
            "best_failure_mode": failure,
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in screened)),
        },
        "best_profile": None if best is None else compact_profile(best),
        "profile_summaries": [compact_profile(row) for row in sorted(analyzed, key=score_key)[:40]],
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
            "global obstruction outside the tested cycle-guarded template front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=646)
    parser.add_argument("--seed-offsets", type=int, default=3)
    parser.add_argument("--max-candidates", type=int, default=520)
    parser.add_argument("--max-diverse-candidates", type=int, default=180)
    parser.add_argument("--top-classes", type=int, default=26)
    parser.add_argument("--random-bases", type=int, default=96)
    parser.add_argument("--max-basis-profiles", type=int, default=8)
    parser.add_argument("--sample-directions", type=int, default=4096)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        seed_offsets=args.seed_offsets,
        max_candidates=args.max_candidates,
        max_diverse_candidates=args.max_diverse_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
        sample_directions=args.sample_directions,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["cycle_guarded_template_front"]
        best = record["best_profile"]
        best_chamber = None if best is None else (
            best.get("best_exact_pairclear_rank_slack_chamber")
            or best.get("best_exact_pairclear_chamber")
            or best.get("best_cycle_clear_rank_slack_chamber")
            or best.get("best_cycle_clear_chamber")
        )
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "selected_candidates": search["selected_candidates"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "cycle_clear_profiles": search["cycle_clear_profiles"],
                    "exact_pairclear_profiles": search["exact_pairclear_profiles"],
                    "cycle_clear_rank_slack_profiles": search["cycle_clear_rank_slack_profiles"],
                    "exact_pairclear_rank_slack_profiles": search["exact_pairclear_rank_slack_profiles"],
                    "best_template_id": search["best_template_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_failure_mode": search["best_failure_mode"],
                    "best_forced_pairs": None if best_chamber is None else best_chamber["forced_pairs"],
                    "best_zero_row_count": None if best_chamber is None else best_chamber["zero_row_count"],
                    "best_inactive_rank": None if best_chamber is None else best_chamber["inactive_rank"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_CYCLE_GUARDED_TEMPLATE_FRONT_SEARCH_READY")


if __name__ == "__main__":
    main()
