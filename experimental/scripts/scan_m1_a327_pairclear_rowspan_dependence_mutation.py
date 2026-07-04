#!/usr/bin/env python3
"""Target-aware row-span dependence mutation search for M1 a=327 pair-clear chambers."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "8613e96"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_row17_dependence_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_rowspan_dependence_mutation.json")

ROOT = Path(__file__).resolve().parents[2]
DIVERSE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_diverse_chamber_front.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
BASE_ZERO_CLASSES = [6, 7, 8, 14, 18, 19, 20]
REPAIR_ROW_CLASS = 17
EXTENDED_ZERO_CLASSES = [6, 7, 8, 14, 17, 18, 19, 20]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


diverse = load_module("pairclear_diverse_chamber_front", DIVERSE_SCRIPT)
tchamber = diverse.tchamber
chamber = diverse.chamber
ninerow = diverse.ninerow
lowrank = diverse.lowrank
zstable = diverse.zstable
basisaware = diverse.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def direction_weight(vector: list[int] | None) -> int | None:
    if vector is None:
        return None
    return sum(1 for value in vector if int(value) % P)


def structural_candidates(
    max_mutations: int,
    max_candidates: int,
    max_diverse_candidates: int,
) -> tuple[list[dict[str, Any]], list[tuple[dict[str, Any], dict[str, Any]]], list[tuple[dict[str, Any], dict[str, Any]]]]:
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
            candidates.append(
                diverse.candidate_from_profile(
                    profile,
                    strategy,
                    seed=121000 + 97 * profile_index + strategy_index,
                )
            )

    screened = [(candidate, tchamber.candidate_screen_row(candidate)) for candidate in candidates]
    structural_pass = [
        (candidate, row)
        for candidate, row in screened
        if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
    ]
    structural_pass.sort(key=tchamber.candidate_sort_key)

    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen: set[tuple[str, str, int]] = set()

    def add(item: tuple[dict[str, Any], dict[str, Any]]) -> None:
        candidate, _row = item
        key = (
            str(candidate.get("mutation_id")),
            str(candidate["assignment_strategy"]),
            int(candidate["assignment_seed"]),
        )
        if key in seen:
            return
        seen.add(key)
        selected.append(item)

    for item in structural_pass[:max_candidates]:
        add(item)
    for item in diverse.diverse_candidates(structural_pass, max_diverse_candidates):
        add(item)
    return profiles, screened, selected


def rank_rows(rows: list[list[int]]) -> int:
    return chamber.rank_rows(rows, ncols=TEMPLATE_DIM)


def target_aware_basis_profiles(
    candidate: dict[str, Any],
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
) -> list[dict[str, Any]]:
    classes = basisaware.functional.functional_classes(candidate)
    target_set = set(EXTENDED_ZERO_CLASSES)
    eligible = [
        idx
        for idx, row in enumerate(classes)
        if int(row["class_index"]) not in target_set
    ]
    supports = [int(row["support_size"]) for row in classes]
    functionals = [[int(value) % P for value in row["functional"]] for row in classes]
    front = sorted(eligible, key=lambda idx: (-supports[idx], functionals[idx]))[: min(top_classes, len(eligible))]

    combos: list[tuple[int, ...]] = []
    seen_combos: set[tuple[int, ...]] = set()

    def add_combo(combo: tuple[int, ...]) -> None:
        if len(combos) >= max_basis_profiles:
            return
        key = tuple(combo)
        if key in seen_combos:
            return
        rows = [functionals[idx] for idx in combo]
        if rank_rows(rows) != TEMPLATE_DIM:
            return
        seen_combos.add(key)
        combos.append(key)

    for combo in itertools.combinations(front, TEMPLATE_DIM):
        add_combo(tuple(combo))
        if len(combos) >= max_basis_profiles:
            break

    for seed in range(random_bases):
        if len(combos) >= max_basis_profiles:
            break
        rng = random.Random(917000 + seed)
        order = eligible[:]
        rng.shuffle(order)
        selected: list[int] = []
        selected_rows: list[list[int]] = []
        current_rank = 0
        for idx in order:
            trial_rank = rank_rows(selected_rows + [functionals[idx]])
            if trial_rank > current_rank:
                selected.append(idx)
                selected_rows.append(functionals[idx])
                current_rank = trial_rank
            if current_rank == TEMPLATE_DIM:
                break
        if len(selected) == TEMPLATE_DIM:
            add_combo(tuple(selected))

    profiles = []
    seen_profiles: set[tuple[int, ...]] = set()
    for combo in combos:
        profile = basisaware.profile_from_indices(
            classes,
            combo,
            "targetaware_" + "_".join(str(classes[idx]["class_index"]) for idx in combo),
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen_profiles:
            continue
        seen_profiles.add(key)
        profiles.append(profile)
    return profiles


def row_indices_for_classes(row_classes: list[int], classes: list[int]) -> list[int] | None:
    by_class = {int(class_index): idx for idx, class_index in enumerate(row_classes)}
    try:
        return [by_class[class_index] for class_index in classes]
    except KeyError:
        return None


def pair_clear_direction_for_rows(
    matrix: list[list[int]],
    row_indices: list[int],
    pair_rows: list[list[int]],
) -> tuple[int, int, list[int] | None]:
    rows = [matrix[idx] for idx in row_indices]
    rank = rank_rows(rows)
    nullity = TEMPLATE_DIM - rank
    direction = None
    if nullity > 0:
        basis = chamber.nullspace_basis(rows)
        direction = chamber.pair_clear_vector_in_subspace(pair_rows, basis)
    return rank, nullity, direction


def best_subspace_direction(
    matrix: list[list[int]],
    row_indices: list[int],
    pair_labels: list[str],
    pair_rows: list[list[int]],
) -> dict[str, Any] | None:
    rows = [matrix[idx] for idx in row_indices]
    basis = chamber.nullspace_basis(rows)
    if not basis:
        return None
    best: dict[str, Any] | None = None
    for coeffs in chamber.projective_directions(len(basis)):
        vector = [0] * TEMPLATE_DIM
        for coeff, basis_vector in zip(coeffs, basis, strict=True):
            if not coeff:
                continue
            vector = [(vector[idx] + coeff * basis_vector[idx]) % P for idx in range(TEMPLATE_DIM)]
        vector = chamber.normalize_projective(vector)
        pair_values = chamber.linear_image_rows(pair_rows, vector)
        forced_indices = [idx for idx, value in enumerate(pair_values) if value % P == 0]
        candidate = {
            "direction": vector,
            "direction_weight": direction_weight(vector),
            "forced_pair_count": len(forced_indices),
            "forced_pair_indices": forced_indices,
            "forced_pairs": [pair_labels[idx] for idx in forced_indices],
            "pair_values": pair_values,
        }
        key = (
            candidate["forced_pair_count"],
            candidate["direction_weight"],
            candidate["direction"],
        )
        if best is None or key < (
            best["forced_pair_count"],
            best["direction_weight"],
            best["direction"],
        ):
            best = candidate
    return best


def direction_chamber(
    matrix: list[list[int]],
    row_classes: list[int],
    direction: list[int] | None,
) -> dict[str, Any] | None:
    if direction is None:
        return None
    row_values = chamber.linear_image_rows(matrix, direction)
    zero_indices = tuple(idx for idx, value in enumerate(row_values) if value % P == 0)
    return chamber.chamber_record(zero_indices, matrix, row_classes, direction)


def analyze_profile(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)
    base_indices = row_indices_for_classes(row_classes, BASE_ZERO_CLASSES)
    extended_indices = row_indices_for_classes(row_classes, EXTENDED_ZERO_CLASSES)

    row = {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "row_classes": row_classes,
        "target_rows_present": base_indices is not None and extended_indices is not None,
        "base_zero_classes": BASE_ZERO_CLASSES,
        "extended_zero_classes": EXTENDED_ZERO_CLASSES,
        "base_row_indices": base_indices,
        "extended_row_indices": extended_indices,
        "best_failure_mode": "ROWSPAN_TARGET_ROWS_MISSING",
    }
    if base_indices is None or extended_indices is None:
        return row

    base_rank, base_nullity, base_direction = pair_clear_direction_for_rows(matrix, base_indices, pair_rows)
    extended_rank, extended_nullity, extended_direction = pair_clear_direction_for_rows(matrix, extended_indices, pair_rows)
    base_best_subspace = best_subspace_direction(matrix, base_indices, pair_labels, pair_rows)
    extended_best_subspace = best_subspace_direction(matrix, extended_indices, pair_labels, pair_rows)
    base_chamber = direction_chamber(matrix, row_classes, base_direction)
    extended_chamber = direction_chamber(matrix, row_classes, extended_direction)
    row.update(
        {
            "base_rank": base_rank,
            "base_nullity": base_nullity,
            "base_pair_clear": base_direction is not None,
            "base_pair_clear_direction": base_direction,
            "base_pair_clear_direction_weight": direction_weight(base_direction),
            "base_best_subspace_direction": base_best_subspace,
            "base_direction_chamber": base_chamber,
            "extended_rank": extended_rank,
            "extended_nullity": extended_nullity,
            "extended_rank_slack": extended_rank <= 4,
            "extended_pair_clear": extended_direction is not None,
            "extended_pair_clear_direction": extended_direction,
            "extended_pair_clear_direction_weight": direction_weight(extended_direction),
            "extended_best_subspace_direction": extended_best_subspace,
            "extended_direction_chamber": extended_chamber,
            "deep_rank_slack_repair": extended_rank <= 4 and extended_direction is not None,
        }
    )
    if row["deep_rank_slack_repair"]:
        row["best_failure_mode"] = "ROWSPAN_DEEP_REPAIR"
    elif extended_rank <= 4:
        row["best_failure_mode"] = "ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL"
    elif extended_direction is not None:
        row["best_failure_mode"] = "ROWSPAN_SUPPORT_ONLY"
    elif base_rank <= 4 and base_direction is not None:
        row["best_failure_mode"] = "ROWSPAN_BASE_ONLY"
    elif base_rank <= 4:
        row["best_failure_mode"] = "ROWSPAN_BASE_PAIRCLEAR_FAIL"
    else:
        row["best_failure_mode"] = "ROWSPAN_BASE_NOT_RANKSLACK"
    return row


def score_key(row: dict[str, Any]) -> tuple[Any, ...]:
    priority = {
        "ROWSPAN_DEEP_REPAIR": 0,
        "ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL": 1,
        "ROWSPAN_SUPPORT_ONLY": 2,
        "ROWSPAN_BASE_ONLY": 3,
        "ROWSPAN_BASE_PAIRCLEAR_FAIL": 4,
        "ROWSPAN_BASE_NOT_RANKSLACK": 5,
        "ROWSPAN_TARGET_ROWS_MISSING": 6,
    }.get(row["best_failure_mode"], 9)
    chamber_row = row.get("extended_direction_chamber") or row.get("base_direction_chamber") or {}
    return (
        priority,
        row.get("extended_rank", 99),
        row.get("base_rank", 99),
        -(chamber_row.get("zero_row_count", 0)),
        chamber_row.get("active_row_count", 99),
        row["template_id"],
        row["assignment_strategy"],
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
        "target_rows_present",
        "base_rank",
        "base_nullity",
        "base_pair_clear",
        "base_pair_clear_direction",
        "base_best_subspace_direction",
        "extended_rank",
        "extended_nullity",
        "extended_rank_slack",
        "extended_pair_clear",
        "extended_pair_clear_direction",
        "extended_best_subspace_direction",
        "deep_rank_slack_repair",
        "base_direction_chamber",
        "extended_direction_chamber",
        "best_failure_mode",
    ]
    return {key: row.get(key) for key in keys}


def build_record(
    max_mutations: int,
    max_candidates: int,
    max_diverse_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    previous_search = previous["row17_dependence_codesign"]
    profiles, screened, selected_candidates = structural_candidates(
        max_mutations=max_mutations,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )

    analyzed = []
    basis_profiles_tested = 0
    for candidate, _screen in selected_candidates:
        for profile in target_aware_basis_profiles(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            max_basis_profiles=max_basis_profiles,
        ):
            basis_profiles_tested += 1
            analyzed.append(analyze_profile(candidate, profile))

    best = min(analyzed, key=score_key) if analyzed else None
    failure = "ROWSPAN_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / ROWSPAN_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if best:
        failure = best["best_failure_mode"]
        if failure == "ROWSPAN_DEEP_REPAIR":
            proof_status = "CANDIDATE / ROWSPAN_DEEP_REPAIR / PARTIAL / EXPERIMENTAL"
        elif failure == "ROWSPAN_SUPPORT_ONLY":
            proof_status = "CANDIDATE / ROWSPAN_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL"
        else:
            proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    target_present = [row for row in analyzed if row["target_rows_present"]]
    base_rank_slack = [row for row in target_present if row.get("base_rank", 99) <= 4]
    base_pair_clear = [row for row in base_rank_slack if row.get("base_pair_clear")]
    extended_rank_slack = [row for row in target_present if row.get("extended_rank", 99) <= 4]
    extended_pair_clear = [row for row in target_present if row.get("extended_pair_clear")]
    extended_rank_slack_pair_clear = [row for row in extended_rank_slack if row.get("extended_pair_clear")]
    deep = [row for row in analyzed if row.get("deep_rank_slack_repair")]

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_row17_dependence_codesign": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "base_rank_slack_profiles": previous_search["base_rank_slack_profiles"],
            "extended_pair_clear_profiles": previous_search["extended_pair_clear_profiles"],
            "extended_rank_slack_pair_clear_profiles": previous_search["extended_rank_slack_pair_clear_profiles"],
            "deep_rank_slack_repair_profiles": previous_search["deep_rank_slack_repair_profiles"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "rowspan_dependence_mutation": {
            "base_zero_classes": BASE_ZERO_CLASSES,
            "repair_row_class": REPAIR_ROW_CLASS,
            "extended_zero_classes": EXTENDED_ZERO_CLASSES,
            "max_mutations": max_mutations,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "mutations_generated": len(profiles),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE") * 3,
            "structural_pass_candidates": sum(
                1 for _candidate, row in screened if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
            ),
            "selected_candidates": len(selected_candidates),
            "basis_profiles_tested": basis_profiles_tested,
            "target_rows_present_profiles": len(target_present),
            "base_rank_slack_profiles": len(base_rank_slack),
            "base_pair_clear_profiles": len(base_pair_clear),
            "extended_rank_slack_profiles": len(extended_rank_slack),
            "extended_pair_clear_profiles": len(extended_pair_clear),
            "extended_rank_slack_pair_clear_profiles": len(extended_rank_slack_pair_clear),
            "deep_rank_slack_repair_profiles": len(deep),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_id": None if best is None else best["basis_id"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
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
            "global obstruction outside the tested row-span dependence mutation front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=640)
    parser.add_argument("--max-candidates", type=int, default=260)
    parser.add_argument("--max-diverse-candidates", type=int, default=120)
    parser.add_argument("--top-classes", type=int, default=24)
    parser.add_argument("--random-bases", type=int, default=96)
    parser.add_argument("--max-basis-profiles", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        max_diverse_candidates=args.max_diverse_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["rowspan_dependence_mutation"]
        best = record["best_profile"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "selected_candidates": search["selected_candidates"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "target_rows_present_profiles": search["target_rows_present_profiles"],
                    "base_rank_slack_profiles": search["base_rank_slack_profiles"],
                    "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
                    "extended_pair_clear_profiles": search["extended_pair_clear_profiles"],
                    "extended_rank_slack_pair_clear_profiles": search["extended_rank_slack_pair_clear_profiles"],
                    "deep_rank_slack_repair_profiles": search["deep_rank_slack_repair_profiles"],
                    "best_template_id": search["best_template_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_base_rank": None if best is None else best.get("base_rank"),
                    "best_extended_rank": None if best is None else best.get("extended_rank"),
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_ROWSPAN_DEPENDENCE_MUTATION_READY")


if __name__ == "__main__":
    main()
