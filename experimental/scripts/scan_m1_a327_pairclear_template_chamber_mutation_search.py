#!/usr/bin/env python3
"""Search mutated pair-clear templates for better direction chambers."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "12a54d9"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_direction_support_chamber_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_template_chamber_mutation_search.json")

ROOT = Path(__file__).resolve().parents[2]
CHAMBER_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_direction_support_chamber_search.py"
NINEROW_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_direction_nine_row_repair.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PREFERRED_BASIS_CLASS_SETS = [
    [1, 4, 7, 8, 9, 10],
    [1, 4, 7, 8, 9, 12],
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


chamber = load_module("pairclear_direction_support_chamber_search", CHAMBER_SCRIPT)
ninerow = load_module("pairclear_direction_nine_row_repair", NINEROW_SCRIPT)
lowrank = ninerow.lowrank
zstable = ninerow.zstable
basisaware = ninerow.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def structural_status(candidate: dict[str, Any]) -> str:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "TCHAMBER_SUPPORT_FAIL"
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return "TCHAMBER_PAIR_GUARD_FAIL"
    row = zstable.candidate_structural_row(candidate)
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        return row["structural_status"].replace("JOINT_TEMPLATE", "TCHAMBER")
    return "TCHAMBER_STRUCTURAL_PASS"


def candidate_from_profile(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    candidate = lowrank.evaluate_candidate(profile, strategy, seed=seed)
    candidate["mutation_id"] = profile.get("mutation_id")
    candidate["base_template_id"] = profile.get("base_template_id")
    candidate["total_effective_cost"] = ninerow.syzygy.rowred.total_effective_cost_gf17(
        profile["template_vectors"],
        candidate["coordinate_classes"],
    )
    return candidate


def candidate_screen_row(candidate: dict[str, Any]) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    row["mutation_id"] = candidate.get("mutation_id")
    row["base_template_id"] = candidate.get("base_template_id")
    row["backward_structural_status"] = structural_status(candidate)
    return row


def candidate_sort_key(item: tuple[dict[str, Any], dict[str, Any]]) -> tuple[Any, ...]:
    candidate, row = item
    return (
        row["forced_functional_identities"],
        -row["functional_span_rank"],
        candidate["total_effective_cost"],
        -min(candidate["pair7_counts"]),
        candidate["max_pair_count"],
        candidate.get("mutation_id", ""),
        candidate["assignment_strategy"],
    )


def basis_profiles(candidate: dict[str, Any], top_classes: int, random_bases: int, limit: int) -> list[dict[str, Any]]:
    classes = basisaware.functional.functional_classes(candidate)
    _combo_count, combos = basisaware.candidate_basis_combos(
        classes,
        top_classes=top_classes,
        random_bases=random_bases,
    )
    profiles = []
    seen: set[tuple[int, ...]] = set()

    by_class = {int(row["class_index"]): idx for idx, row in enumerate(classes)}
    preferred_combos = []
    for class_set in PREFERRED_BASIS_CLASS_SETS:
        try:
            preferred_combos.append(tuple(by_class[int(class_index)] for class_index in class_set))
        except KeyError:
            continue

    ordered_combos = preferred_combos + [combo for combo in combos if combo not in set(preferred_combos)]
    for combo in ordered_combos:
        profile = basisaware.profile_from_indices(
            classes,
            combo,
            f"basisaware_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        profiles.append(profile)
    preferred_keys = {tuple(class_set) for class_set in PREFERRED_BASIS_CLASS_SETS}
    profiles.sort(
        key=lambda profile: (
            0 if tuple(profile["basis_class_indices"]) in preferred_keys else 1,
            len(profile["nonbasis_constraint_detail"]),
            profile["q_variable_count"],
            -min(profile["basis_support_sizes"]),
            profile["basis_class_indices"],
        )
    )
    return profiles[:limit]


def score_profile(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    direction_limit: int | None,
    extension_chamber_limit: int,
) -> dict[str, Any]:
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)

    chamber_exemplars: dict[tuple[int, ...], list[int]] = {}
    directions_tested = 0
    pair_clear_directions = 0
    support_reduced_directions = 0
    rank_slack_directions = 0
    for vector in chamber.projective_directions(TEMPLATE_DIM):
        if direction_limit is not None and directions_tested >= direction_limit:
            break
        directions_tested += 1
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

    extension_inputs = sorted(
        [row for row in chambers if row["inactive_rank"] <= 4],
        key=lambda row: (-row["zero_row_count"], row["inactive_rank"], row["active_row_count"]),
    )[:extension_chamber_limit]
    extension_tests = 0
    extensions = []
    for base_chamber in extension_inputs:
        zero_set = set(base_chamber["zero_row_indices"])
        for active_idx in range(len(matrix)):
            if active_idx in zero_set:
                continue
            extension_tests += 1
            extension = chamber.extension_record(base_chamber, active_idx, matrix, row_classes, pair_rows)
            if extension is not None:
                extensions.append(extension)
    support_reduced_extensions = [row for row in extensions if row["zero_row_count"] >= 6]

    best_chamber = min(chambers, key=chamber.chamber_sort_key) if chambers else None
    best_nine = min(nine_or_better, key=chamber.chamber_sort_key) if nine_or_better else None
    best_direct = min(direct_support_reduced, key=chamber.chamber_sort_key) if direct_support_reduced else None
    best_rank_slack = min(rank_slack, key=chamber.rank_slack_sort_key) if rank_slack else None
    best_extension = min(extensions, key=chamber.extension_sort_key) if extensions else None
    best_support_extension = min(support_reduced_extensions, key=chamber.extension_sort_key) if support_reduced_extensions else None

    failure = "TCHAMBER_NO_PAIR_CLEAR_CHAMBER"
    if best_direct is not None:
        failure = "TCHAMBER_DIRECT_SUPPORT_REDUCED"
    elif best_support_extension is not None:
        failure = "TCHAMBER_EXTENSION_SUPPORT_REDUCED"
    elif best_rank_slack is not None:
        failure = "TCHAMBER_RANK_SLACK_FOUND"
    elif best_nine is not None:
        failure = "TCHAMBER_NINE_ROW_STABLE"
    elif best_chamber is not None:
        failure = "TCHAMBER_LOWER_SUPPORT_ONLY"

    return {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "q_variable_count": profile["q_variable_count"],
        "row_classes": row_classes,
        "pair_projection_labels": pair_labels,
        "direction_limit": direction_limit,
        "directions_tested": directions_tested,
        "pair_clear_directions": pair_clear_directions,
        "distinct_pair_clear_chambers": len(chambers),
        "nine_row_or_better_chambers": len(nine_or_better),
        "direct_support_reduced_directions": support_reduced_directions,
        "direct_support_reduced_chambers": len(direct_support_reduced),
        "rank_slack_directions": rank_slack_directions,
        "rank_slack_chambers": len(rank_slack),
        "extension_tests": extension_tests,
        "extension_pairclear_successes": len(extensions),
        "support_reduced_extensions": len(support_reduced_extensions),
        "best_chamber": best_chamber,
        "best_nine_row_chamber": best_nine,
        "best_direct_support_reduced_chamber": best_direct,
        "best_rank_slack_chamber": best_rank_slack,
        "best_extension": best_extension,
        "best_support_reduced_extension": best_support_extension,
        "best_failure_mode": failure,
    }


def score_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    priority = {
        "TCHAMBER_DIRECT_SUPPORT_REDUCED": 0,
        "TCHAMBER_EXTENSION_SUPPORT_REDUCED": 1,
        "TCHAMBER_RANK_SLACK_FOUND": 2,
        "TCHAMBER_NINE_ROW_STABLE": 3,
        "TCHAMBER_LOWER_SUPPORT_ONLY": 4,
        "TCHAMBER_NO_PAIR_CLEAR_CHAMBER": 5,
    }.get(row["best_failure_mode"], 9)
    best = (
        row.get("best_direct_support_reduced_chamber")
        or row.get("best_support_reduced_extension")
        or row.get("best_rank_slack_chamber")
        or row.get("best_nine_row_chamber")
        or row.get("best_chamber")
        or {}
    )
    return (
        priority,
        -(best.get("zero_row_count", 0)),
        best.get("inactive_rank", 99),
        best.get("active_row_count", 99),
        row["template_id"],
        row["basis_id"],
    )


def compact_score(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "mutation_id",
        "assignment_strategy",
        "assignment_seed",
        "basis_id",
        "basis_class_indices",
        "basis_support_sizes",
        "coefficient_matrix_shape",
        "directions_tested",
        "pair_clear_directions",
        "distinct_pair_clear_chambers",
        "nine_row_or_better_chambers",
        "direct_support_reduced_chambers",
        "rank_slack_chambers",
        "extension_pairclear_successes",
        "support_reduced_extensions",
        "best_nine_row_chamber",
        "best_direct_support_reduced_chamber",
        "best_rank_slack_chamber",
        "best_support_reduced_extension",
        "best_failure_mode",
    ]
    return {key: row.get(key) for key in keys}


def select_diverse_candidates(
    structural_pass: list[tuple[dict[str, Any], dict[str, Any]]],
    limit: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    selected_keys: set[tuple[str, str]] = set()
    seen_mutations: set[str] = set()

    for item in structural_pass:
        candidate, _row = item
        mutation = str(candidate.get("mutation_id"))
        key = (mutation, str(candidate["assignment_strategy"]))
        if mutation in seen_mutations or key in selected_keys:
            continue
        seen_mutations.add(mutation)
        selected_keys.add(key)
        selected.append(item)
        if len(selected) >= limit:
            return selected

    for item in structural_pass:
        candidate, _row = item
        key = (str(candidate.get("mutation_id")), str(candidate["assignment_strategy"]))
        if key in selected_keys:
            continue
        selected_keys.add(key)
        selected.append(item)
        if len(selected) >= limit:
            return selected
    return selected


def build_record(
    max_mutations: int,
    max_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
    max_scored_profiles: int,
    direction_limit: int | None,
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
            candidates.append(candidate_from_profile(profile, strategy, seed=105000 + 97 * profile_index + strategy_index))

    screened = [(candidate, candidate_screen_row(candidate)) for candidate in candidates]
    structural_pass = [
        (candidate, row)
        for candidate, row in screened
        if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
    ]
    structural_pass.sort(key=candidate_sort_key)
    selected_candidates = select_diverse_candidates(structural_pass, max_candidates)

    scored = []
    basis_profiles_tested = 0
    for candidate, _row in selected_candidates:
        for profile in basis_profiles(candidate, top_classes=top_classes, random_bases=random_bases, limit=max_basis_profiles):
            if len(scored) >= max_scored_profiles:
                break
            basis_profiles_tested += 1
            scored.append(
                score_profile(
                    candidate,
                    profile,
                    direction_limit=direction_limit,
                    extension_chamber_limit=extension_chamber_limit,
                )
            )
        if len(scored) >= max_scored_profiles:
            break

    if scored:
        best = min(scored, key=score_sort_key)
        failure = best["best_failure_mode"]
    else:
        best = None
        failure = "TCHAMBER_NO_SCORED_PROFILES"

    if failure == "TCHAMBER_DIRECT_SUPPORT_REDUCED":
        proof_status = "CANDIDATE / TCHAMBER_DIRECT_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL"
    elif failure == "TCHAMBER_EXTENSION_SUPPORT_REDUCED":
        proof_status = "CANDIDATE / TCHAMBER_EXTENSION_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL"
    elif failure == "TCHAMBER_RANK_SLACK_FOUND":
        proof_status = "CANDIDATE / TCHAMBER_RANK_SLACK_FOUND / PARTIAL / EXPERIMENTAL"
    elif failure == "TCHAMBER_NINE_ROW_STABLE":
        proof_status = "CANDIDATE / TCHAMBER_NINE_ROW_STABLE_FRONT / PARTIAL / EXPERIMENTAL"
    else:
        proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    previous_search = previous["chamber_search"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_chamber_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "directions_tested": previous_search["directions_tested"],
            "pair_clear_directions": previous_search["pair_clear_directions"],
            "distinct_pair_clear_chambers": previous_search["distinct_pair_clear_chambers"],
            "rank_slack_chambers": previous_search["rank_slack_chambers"],
            "support_reduced_extensions": previous_search["support_reduced_extensions"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "template_chamber_search": {
            "max_mutations": max_mutations,
            "max_candidates": max_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "max_scored_profiles": max_scored_profiles,
            "direction_limit": direction_limit,
            "extension_chamber_limit": extension_chamber_limit,
            "mutations_generated": len(specs),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": len(candidates),
            "structural_pass_candidates": len(structural_pass),
            "structural_pass_candidates_analyzed": len(selected_candidates),
            "basis_profiles_scored": basis_profiles_tested,
            "directions_tested": sum(row["directions_tested"] for row in scored),
            "pair_clear_directions": sum(row["pair_clear_directions"] for row in scored),
            "distinct_pair_clear_chambers": sum(row["distinct_pair_clear_chambers"] for row in scored),
            "nine_row_or_better_profiles": sum(1 for row in scored if row["nine_row_or_better_chambers"] > 0),
            "direct_support_reduced_profiles": sum(1 for row in scored if row["direct_support_reduced_chambers"] > 0),
            "rank_slack_profiles": sum(1 for row in scored if row["rank_slack_chambers"] > 0),
            "support_reduced_extension_profiles": sum(1 for row in scored if row["support_reduced_extensions"] > 0),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_id": None if best is None else best["basis_id"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in scored)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in screened)),
            "scored_profile_summaries": [compact_score(row) for row in sorted(scored, key=score_sort_key)[:12]],
        },
        "best_profile": None if best is None else compact_score(best),
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
            "global obstruction outside the tested template-chamber mutation front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=24)
    parser.add_argument("--max-candidates", type=int, default=8)
    parser.add_argument("--top-classes", type=int, default=14)
    parser.add_argument("--random-bases", type=int, default=16)
    parser.add_argument("--max-basis-profiles", type=int, default=2)
    parser.add_argument("--max-scored-profiles", type=int, default=8)
    parser.add_argument("--direction-limit", type=int, default=None)
    parser.add_argument("--extension-chamber-limit", type=int, default=80)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
        max_scored_profiles=args.max_scored_profiles,
        direction_limit=args.direction_limit,
        extension_chamber_limit=args.extension_chamber_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["template_chamber_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "mutations_generated": search["mutations_generated"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "basis_profiles_scored": search["basis_profiles_scored"],
                    "directions_tested": search["directions_tested"],
                    "pair_clear_directions": search["pair_clear_directions"],
                    "nine_row_or_better_profiles": search["nine_row_or_better_profiles"],
                    "direct_support_reduced_profiles": search["direct_support_reduced_profiles"],
                    "rank_slack_profiles": search["rank_slack_profiles"],
                    "support_reduced_extension_profiles": search["support_reduced_extension_profiles"],
                    "best_template_id": search["best_template_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_TEMPLATE_CHAMBER_MUTATION_SEARCH_READY")


if __name__ == "__main__":
    main()
