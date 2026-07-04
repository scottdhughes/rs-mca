#!/usr/bin/env python3
"""Pair-clear search allowing two target zero classes inside the coefficient basis."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "b84b4ca"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_target_basis_exchange_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_two_target_basis_exchange_search.json")

ROOT = Path(__file__).resolve().parents[2]
TARGETBASIS_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_target_basis_exchange_search.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
EXTENDED_ZERO_CLASSES = [6, 7, 8, 14, 17, 18, 19, 20]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


targetbasis = load_module("pairclear_target_basis_exchange_search", TARGETBASIS_SCRIPT)
rowspan = targetbasis.rowspan
basisaware = targetbasis.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_rows(rows: list[list[int]]) -> int:
    return targetbasis.rank_rows(rows)


def remap_failure(label: str) -> str:
    return label.replace("TARGETBASIS_", "TWOTARGETBASIS_")


def two_target_basis_exchange_profiles(
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
    target_set = set(target_indices)
    non_target_indices = [idx for idx in range(len(classes)) if idx not in target_set]
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
        target_count = sum(1 for idx in key if idx in target_set)
        if target_count != 2:
            return
        rows = [functionals[idx] for idx in key]
        if rank_rows(rows) != TEMPLATE_DIM:
            return
        seen_combos.add(key)
        combos.append(key)

    for target_pair in itertools.combinations(target_indices, 2):
        for rest in itertools.combinations(front, TEMPLATE_DIM - 2):
            add_combo((*target_pair, *rest))
            if len(combos) >= max_basis_profiles:
                break
        if len(combos) >= max_basis_profiles:
            break

    target_pairs = list(itertools.combinations(target_indices, 2))
    for seed in range(random_bases):
        if len(combos) >= max_basis_profiles or not target_pairs:
            break
        rng = random.Random(1279000 + seed)
        selected_targets = list(target_pairs[seed % len(target_pairs)])
        order = non_target_indices[:]
        rng.shuffle(order)
        selected = selected_targets[:]
        selected_rows = [functionals[idx] for idx in selected]
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
        target_classes = [class_index for class_index in class_indices if class_index in set(EXTENDED_ZERO_CLASSES)]
        profile = basisaware.profile_from_indices(
            classes,
            combo,
            "twotargetbasis_" + "_".join(str(class_index) for class_index in target_classes)
            + "_"
            + "_".join(str(class_index) for class_index in class_indices),
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen_profiles:
            continue
        seen_profiles.add(key)
        profile["target_basis_classes"] = sorted(target_classes)
        profiles.append(profile)
    return profiles


def analyze_profile(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    row = targetbasis.analyze_profile(candidate, profile)
    row["target_basis_classes"] = profile.get("target_basis_classes")
    row["best_failure_mode"] = remap_failure(row["best_failure_mode"])
    return row


def score_key(row: dict[str, Any]) -> tuple[Any, ...]:
    original = dict(row)
    original["best_failure_mode"] = row["best_failure_mode"].replace("TWOTARGETBASIS_", "TARGETBASIS_")
    return targetbasis.exchange_score_key(original)


def compact_profile(row: dict[str, Any]) -> dict[str, Any]:
    compact = targetbasis.compact_profile(row)
    compact["target_basis_classes"] = row.get("target_basis_classes")
    compact["best_failure_mode"] = row.get("best_failure_mode")
    return compact


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
    profiles, screened, selected_candidates = targetbasis.p46p67.p456.structural_candidates(
        max_mutations=max_mutations,
        seed_offsets=seed_offsets,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )
    analyzed = []
    basis_profiles_tested = 0
    for candidate, _screen in selected_candidates:
        for profile in two_target_basis_exchange_profiles(
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
    best = min(analyzed, key=score_key) if analyzed else None

    forced_patterns = Counter()
    target_basis_counts = Counter()
    cycle_forced_counts = Counter()
    total_forced_counts = Counter()
    front_return_counts = Counter()
    for row in extended_rank_slack:
        target_basis_counts[",".join(str(value) for value in row.get("target_basis_classes") or [])] += 1
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

    failure = "TWOTARGETBASIS_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / TWOTARGETBASIS_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if best:
        failure = best["best_failure_mode"]
        if failure == "TWOTARGETBASIS_EXACT_PAIRCLEAR_REPAIRED":
            proof_status = "CANDIDATE / TWOTARGETBASIS_EXACT_PAIRCLEAR_REPAIRED / PARTIAL / EXPERIMENTAL"
        elif failure == "TWOTARGETBASIS_CYCLE_PRESSURE_REDUCED":
            proof_status = "CANDIDATE / TWOTARGETBASIS_CYCLE_PRESSURE_REDUCED / PARTIAL / EXPERIMENTAL"
        else:
            proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_target_basis_exchange": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_tested": previous["target_basis_exchange_search"]["basis_profiles_tested"],
            "extended_rank_slack_profiles": previous["target_basis_exchange_search"]["extended_rank_slack_profiles"],
            "exact_pairclear_profiles": previous["target_basis_exchange_search"]["exact_pairclear_profiles"],
            "best_forced_pairs": previous["best_profile"]["extended_exchange_direction"]["forced_pairs"],
        },
        "two_target_basis_exchange_search": {
            "extended_zero_classes": targetbasis.EXTENDED_ZERO_CLASSES,
            "base_zero_classes": targetbasis.BASE_ZERO_CLASSES,
            "cycle_pairs": targetbasis.CYCLE_PAIRS,
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
            "best_target_basis_classes": None if best is None else best.get("target_basis_classes"),
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
            "global obstruction outside the tested two-target basis exchange front",
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
    parser.add_argument("--top-classes", type=int, default=34)
    parser.add_argument("--random-bases", type=int, default=192)
    parser.add_argument("--max-basis-profiles", type=int, default=20)
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
        search = record["two_target_basis_exchange_search"]
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
                    "best_target_basis_classes": search["best_target_basis_classes"],
                    "best_forced_pairs": None if best_info is None else best_info["forced_pairs"],
                    "best_cycle_pairs_cleared": None if best_info is None else best_info["cycle_pairs_cleared"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_TWO_TARGET_BASIS_EXCHANGE_SEARCH_READY")


if __name__ == "__main__":
    main()
