#!/usr/bin/env python3
"""Pair-clear search allowing one target zero class inside the coefficient basis."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "fa084a3"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_cyclic_tail_mixed_obstruction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_target_basis_exchange_search.json")

ROOT = Path(__file__).resolve().parents[2]
P46P67_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_p46_p67_tradeoff_repair.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
EXTENDED_ZERO_CLASSES = [6, 7, 8, 14, 17, 18, 19, 20]
BASE_ZERO_CLASSES = [6, 7, 8, 14, 18, 19, 20]
TAIL_FRONT = ["P56", "P57", "P67"]
P456_FRONT = ["P45", "P46", "P56"]
MIXED_FRONT = ["P14", "P16", "P17", "P46", "P47", "P67"]
CYCLE_PAIRS = sorted(set(TAIL_FRONT + P456_FRONT + MIXED_FRONT))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p46p67 = load_module("pairclear_p46_p67_tradeoff_repair", P46P67_SCRIPT)
rowspan = p46p67.rowspan
chamber = p46p67.chamber
zstable = p46p67.zstable
basisaware = rowspan.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def direction_weight(vector: list[int] | None) -> int | None:
    if vector is None:
        return None
    return sum(1 for value in vector if int(value) % P)


def rank_rows(rows: list[list[int]]) -> int:
    return chamber.rank_rows(rows, ncols=TEMPLATE_DIM)


def target_basis_exchange_profiles(
    candidate: dict[str, Any],
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
) -> list[dict[str, Any]]:
    classes = basisaware.functional.functional_classes(candidate)
    supports = [int(row["support_size"]) for row in classes]
    functionals = [[int(value) % P for value in row["functional"]] for row in classes]
    by_class = {int(row["class_index"]): idx for idx, row in enumerate(classes)}
    target_indices = [by_class[class_index] for class_index in EXTENDED_ZERO_CLASSES if class_index in by_class]
    non_target_indices = [
        idx
        for idx, row in enumerate(classes)
        if int(row["class_index"]) not in set(EXTENDED_ZERO_CLASSES)
    ]
    front = sorted(non_target_indices, key=lambda idx: (-supports[idx], functionals[idx]))[
        : min(top_classes, len(non_target_indices))
    ]

    combos: list[tuple[int, ...]] = []
    seen_combos: set[tuple[int, ...]] = set()

    def add_combo(combo: tuple[int, ...]) -> None:
        if len(combos) >= max_basis_profiles:
            return
        key = tuple(sorted(combo))
        if key in seen_combos:
            return
        target_count = sum(1 for idx in key if int(classes[idx]["class_index"]) in set(EXTENDED_ZERO_CLASSES))
        if target_count != 1:
            return
        rows = [functionals[idx] for idx in key]
        if rank_rows(rows) != TEMPLATE_DIM:
            return
        seen_combos.add(key)
        combos.append(key)

    for target_idx in target_indices:
        for rest in itertools.combinations(front, TEMPLATE_DIM - 1):
            add_combo((target_idx, *rest))
            if len(combos) >= max_basis_profiles:
                break
        if len(combos) >= max_basis_profiles:
            break

    for seed in range(random_bases):
        if len(combos) >= max_basis_profiles:
            break
        rng = random.Random(1147000 + seed)
        target_idx = target_indices[seed % len(target_indices)] if target_indices else None
        if target_idx is None:
            break
        order = non_target_indices[:]
        rng.shuffle(order)
        selected = [target_idx]
        selected_rows = [functionals[target_idx]]
        current_rank = rank_rows(selected_rows)
        for idx in order:
            trial_rank = rank_rows(selected_rows + [functionals[idx]])
            if trial_rank > current_rank:
                selected.append(idx)
                selected_rows.append(functionals[idx])
                current_rank = trial_rank
            if len(selected) == TEMPLATE_DIM and current_rank == TEMPLATE_DIM:
                break
        if len(selected) == TEMPLATE_DIM and current_rank == TEMPLATE_DIM:
            add_combo(tuple(selected))

    profiles = []
    seen_profiles: set[tuple[int, ...]] = set()
    for combo in combos:
        class_indices = [int(classes[idx]["class_index"]) for idx in combo]
        target_class = next(class_index for class_index in class_indices if class_index in set(EXTENDED_ZERO_CLASSES))
        profile = basisaware.profile_from_indices(
            classes,
            combo,
            "targetbasis_" + str(target_class) + "_" + "_".join(str(class_index) for class_index in class_indices),
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen_profiles:
            continue
        seen_profiles.add(key)
        profile["target_basis_class"] = target_class
        profiles.append(profile)
    return profiles


def augmented_matrix_and_classes(profile: dict[str, Any]) -> tuple[list[list[int]], list[int], list[int]]:
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    augmented_basis_classes = []
    for slot, class_index in enumerate(profile["basis_class_indices"]):
        class_index = int(class_index)
        if class_index in set(EXTENDED_ZERO_CLASSES):
            unit = [0] * TEMPLATE_DIM
            unit[slot] = 1
            matrix.append(unit)
            row_classes.append(class_index)
            augmented_basis_classes.append(class_index)
    return matrix, row_classes, augmented_basis_classes


def forced_info(forced_pairs: list[str], direction: list[int] | None = None) -> dict[str, Any]:
    forced_set = set(forced_pairs)
    return {
        "forced_pair_count": len(forced_pairs),
        "forced_pairs": forced_pairs,
        "cycle_forced_count": sum(1 for pair in forced_pairs if pair in CYCLE_PAIRS),
        "cycle_pairs_cleared": [pair for pair in CYCLE_PAIRS if pair not in forced_set],
        "tail_forced_count": sum(1 for pair in forced_pairs if pair in TAIL_FRONT),
        "p456_forced_count": sum(1 for pair in forced_pairs if pair in P456_FRONT),
        "mixed_forced_count": sum(1 for pair in forced_pairs if pair in MIXED_FRONT),
        "tail_front_returned": all(pair in forced_set for pair in TAIL_FRONT),
        "p456_front_returned": all(pair in forced_set for pair in P456_FRONT),
        "mixed_front_returned": all(pair in forced_set for pair in MIXED_FRONT),
        "other_forced_pairs": [pair for pair in forced_pairs if pair not in CYCLE_PAIRS],
        "direction": direction,
        "direction_weight": direction_weight(direction),
    }


def best_exchange_subspace_direction(
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
        forced_pairs = [pair_labels[idx] for idx, value in enumerate(pair_values) if value % P == 0]
        info = forced_info(forced_pairs, vector)
        info["pair_values"] = pair_values
        key = (
            info["forced_pair_count"],
            info["cycle_forced_count"],
            info["tail_forced_count"],
            info["p456_forced_count"],
            info["mixed_forced_count"],
            info["direction_weight"],
            info["direction"],
        )
        if best is None or key < (
            best["forced_pair_count"],
            best["cycle_forced_count"],
            best["tail_forced_count"],
            best["p456_forced_count"],
            best["mixed_forced_count"],
            best["direction_weight"],
            best["direction"],
        ):
            best = info
    return best


def analyze_profile(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    matrix, row_classes, augmented_basis_classes = augmented_matrix_and_classes(profile)
    pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)
    base_indices = rowspan.row_indices_for_classes(row_classes, BASE_ZERO_CLASSES)
    extended_indices = rowspan.row_indices_for_classes(row_classes, EXTENDED_ZERO_CLASSES)
    row = {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "seed_offset": candidate.get("seed_offset"),
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "target_basis_class": profile.get("target_basis_class"),
        "basis_support_sizes": profile["basis_support_sizes"],
        "augmented_basis_zero_classes": augmented_basis_classes,
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "row_classes": row_classes,
        "target_rows_present": base_indices is not None and extended_indices is not None,
        "base_row_indices": base_indices,
        "extended_row_indices": extended_indices,
        "best_failure_mode": "TARGETBASIS_TARGET_ROWS_MISSING",
    }
    if base_indices is None or extended_indices is None:
        return row

    base_rows = [matrix[idx] for idx in base_indices]
    extended_rows = [matrix[idx] for idx in extended_indices]
    base_rank = chamber.rank_rows(base_rows)
    extended_rank = chamber.rank_rows(extended_rows)
    base_best = best_exchange_subspace_direction(matrix, base_indices, pair_labels, pair_rows)
    extended_best = best_exchange_subspace_direction(matrix, extended_indices, pair_labels, pair_rows)
    row.update(
        {
            "base_rank": base_rank,
            "base_nullity": TEMPLATE_DIM - base_rank,
            "extended_rank": extended_rank,
            "extended_nullity": TEMPLATE_DIM - extended_rank,
            "extended_rank_slack": extended_rank <= 4,
            "base_exchange_direction": base_best,
            "extended_exchange_direction": extended_best,
        }
    )
    if extended_rank <= 4 and extended_best and extended_best["forced_pair_count"] == 0:
        row["best_failure_mode"] = "TARGETBASIS_EXACT_PAIRCLEAR_REPAIRED"
    elif extended_rank <= 4 and extended_best and extended_best["forced_pair_count"] <= 2:
        row["best_failure_mode"] = "TARGETBASIS_CYCLE_PRESSURE_REDUCED"
    elif extended_rank <= 4:
        row["best_failure_mode"] = "TARGETBASIS_FORCED_PROJECTIONS_REMAIN"
    elif extended_best and extended_best["forced_pair_count"] == 0:
        row["best_failure_mode"] = "TARGETBASIS_SUPPORT_ONLY"
    else:
        row["best_failure_mode"] = "TARGETBASIS_BASE_NOT_RANKSLACK"
    return row


def exchange_score_key(row: dict[str, Any]) -> tuple[Any, ...]:
    info = row.get("extended_exchange_direction") or {}
    priority = {
        "TARGETBASIS_EXACT_PAIRCLEAR_REPAIRED": 0,
        "TARGETBASIS_CYCLE_PRESSURE_REDUCED": 1,
        "TARGETBASIS_FORCED_PROJECTIONS_REMAIN": 2,
        "TARGETBASIS_SUPPORT_ONLY": 3,
        "TARGETBASIS_BASE_NOT_RANKSLACK": 4,
        "TARGETBASIS_TARGET_ROWS_MISSING": 5,
    }.get(row["best_failure_mode"], 9)
    return (
        priority,
        info.get("forced_pair_count", 99),
        info.get("cycle_forced_count", 99),
        info.get("tail_forced_count", 99),
        info.get("p456_forced_count", 99),
        info.get("mixed_forced_count", 99),
        row.get("extended_rank", 99),
        row.get("base_rank", 99),
        info.get("direction_weight", 99),
        row["template_id"],
        row["basis_id"],
    )


def compact_profile(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "mutation_id",
        "assignment_strategy",
        "assignment_seed",
        "seed_offset",
        "basis_id",
        "basis_class_indices",
        "target_basis_class",
        "basis_support_sizes",
        "augmented_basis_zero_classes",
        "coefficient_matrix_shape",
        "target_rows_present",
        "base_rank",
        "base_nullity",
        "extended_rank",
        "extended_nullity",
        "extended_rank_slack",
        "base_exchange_direction",
        "extended_exchange_direction",
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
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, screened, selected_candidates = p46p67.p456.structural_candidates(
        max_mutations=max_mutations,
        seed_offsets=seed_offsets,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )
    analyzed = []
    basis_profiles_tested = 0
    for candidate, _screen in selected_candidates:
        for profile in target_basis_exchange_profiles(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            max_basis_profiles=max_basis_profiles,
        ):
            basis_profiles_tested += 1
            analyzed.append(analyze_profile(candidate, profile))

    target_present = [row for row in analyzed if row["target_rows_present"]]
    extended_rank_slack = [row for row in target_present if row.get("extended_rank_slack")]
    exact = [
        row
        for row in extended_rank_slack
        if (row.get("extended_exchange_direction") or {}).get("forced_pair_count") == 0
    ]
    reduced = [
        row
        for row in extended_rank_slack
        if (row.get("extended_exchange_direction") or {}).get("forced_pair_count", 99) <= 2
    ]
    best = min(analyzed, key=exchange_score_key) if analyzed else None

    forced_patterns = Counter()
    target_basis_counts = Counter()
    cycle_forced_counts = Counter()
    total_forced_counts = Counter()
    front_return_counts = Counter()
    for row in extended_rank_slack:
        target_basis_counts[str(row.get("target_basis_class"))] += 1
        info = row.get("extended_exchange_direction") or {}
        forced_patterns[",".join(info.get("forced_pairs") or [])] += 1
        cycle_forced_counts[str(info.get("cycle_forced_count", 99))] += 1
        total_forced_counts[str(info.get("forced_pair_count", 99))] += 1
        if info.get("tail_front_returned"):
            front_return_counts["tail_front"] += 1
        if info.get("p456_front_returned"):
            front_return_counts["p456_front"] += 1
        if info.get("mixed_front_returned"):
            front_return_counts["mixed_front"] += 1

    failure = "TARGETBASIS_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / TARGETBASIS_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if best:
        failure = best["best_failure_mode"]
        if failure == "TARGETBASIS_EXACT_PAIRCLEAR_REPAIRED":
            proof_status = "CANDIDATE / TARGETBASIS_EXACT_PAIRCLEAR_REPAIRED / PARTIAL / EXPERIMENTAL"
        elif failure == "TARGETBASIS_CYCLE_PRESSURE_REDUCED":
            proof_status = "CANDIDATE / TARGETBASIS_CYCLE_PRESSURE_REDUCED / PARTIAL / EXPERIMENTAL"
        else:
            proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_cyclic_obstruction": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "route_cut": previous["cycle_diagnosis"]["route_cut"],
            "observed_cycle": previous["cycle_diagnosis"]["observed_cycle"],
        },
        "target_basis_exchange_search": {
            "extended_zero_classes": EXTENDED_ZERO_CLASSES,
            "base_zero_classes": BASE_ZERO_CLASSES,
            "cycle_pairs": CYCLE_PAIRS,
            "max_mutations": max_mutations,
            "seed_offsets": seed_offsets,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "mutations_generated": len(profiles),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE") * 3 * seed_offsets,
            "structural_pass_candidates": sum(
                1 for _candidate, row in screened if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
            ),
            "selected_candidates": len(selected_candidates),
            "basis_profiles_tested": basis_profiles_tested,
            "target_rows_present_profiles": len(target_present),
            "extended_rank_slack_profiles": len(extended_rank_slack),
            "exact_pairclear_profiles": len(exact),
            "cycle_pressure_reduced_profiles": len(reduced),
            "target_basis_class_counts": dict(target_basis_counts),
            "cycle_forced_count_histogram": dict(cycle_forced_counts),
            "total_forced_count_histogram": dict(total_forced_counts),
            "front_return_counts": dict(front_return_counts),
            "forced_pair_pattern_counts": dict(forced_patterns.most_common(16)),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_id": None if best is None else best["basis_id"],
            "best_target_basis_class": None if best is None else best.get("target_basis_class"),
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in screened)),
        },
        "best_profile": None if best is None else compact_profile(best),
        "profile_summaries": [compact_profile(row) for row in sorted(analyzed, key=exchange_score_key)[:40]],
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
            "global obstruction outside the tested target-basis exchange front",
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
    parser.add_argument("--top-classes", type=int, default=30)
    parser.add_argument("--random-bases", type=int, default=160)
    parser.add_argument("--max-basis-profiles", type=int, default=16)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        seed_offsets=args.seed_offsets,
        max_candidates=args.max_candidates,
        max_diverse_candidates=args.max_diverse_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["target_basis_exchange_search"]
        best = record["best_profile"]
        best_info = None if best is None else best.get("extended_exchange_direction")
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "selected_candidates": search["selected_candidates"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
                    "exact_pairclear_profiles": search["exact_pairclear_profiles"],
                    "cycle_pressure_reduced_profiles": search["cycle_pressure_reduced_profiles"],
                    "cycle_forced_count_histogram": search["cycle_forced_count_histogram"],
                    "best_template_id": search["best_template_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_target_basis_class": search["best_target_basis_class"],
                    "best_forced_pairs": None if best_info is None else best_info["forced_pairs"],
                    "best_cycle_pairs_cleared": None if best_info is None else best_info["cycle_pairs_cleared"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_TARGET_BASIS_EXCHANGE_SEARCH_READY")


if __name__ == "__main__":
    main()
