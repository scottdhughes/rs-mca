#!/usr/bin/env python3
"""Tradeoff repair for forced P46/P67 projections in M1 a=327 pair-clear kernels."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "c900d81"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_p45_p46_p56_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_p46_p67_tradeoff_repair.json")

ROOT = Path(__file__).resolve().parents[2]
P456_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_p45_p46_p56_codesign.py"

REPAIR_PAIRS = ["P46", "P67"]
PRESERVE_CLEAR_PAIRS = ["P45", "P56"]
SPILLOVER_AVOID_PAIRS = ["P14", "P16", "P17", "P47"]
TARGET_AGREEMENT = 327
P = 17
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p456 = load_module("pairclear_p45_p46_p56_codesign", P456_SCRIPT)
rowspan = p456.rowspan
chamber = p456.chamber
zstable = p456.zstable


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def direction_weight(vector: list[int] | None) -> int | None:
    if vector is None:
        return None
    return sum(1 for value in vector if int(value) % P)


def forced_info(forced_pairs: list[str], direction: list[int] | None = None) -> dict[str, Any]:
    return {
        "forced_pair_count": len(forced_pairs),
        "forced_pairs": forced_pairs,
        "repair_forced_count": sum(1 for pair in forced_pairs if pair in REPAIR_PAIRS),
        "repair_pairs_cleared": [pair for pair in REPAIR_PAIRS if pair not in forced_pairs],
        "preserve_forced_count": sum(1 for pair in forced_pairs if pair in PRESERVE_CLEAR_PAIRS),
        "preserve_pairs_cleared": [pair for pair in PRESERVE_CLEAR_PAIRS if pair not in forced_pairs],
        "spillover_forced_count": sum(1 for pair in forced_pairs if pair in SPILLOVER_AVOID_PAIRS),
        "spillover_pairs_cleared": [pair for pair in SPILLOVER_AVOID_PAIRS if pair not in forced_pairs],
        "other_forced_pairs": [
            pair
            for pair in forced_pairs
            if pair not in REPAIR_PAIRS
            and pair not in PRESERVE_CLEAR_PAIRS
            and pair not in SPILLOVER_AVOID_PAIRS
        ],
        "direction": direction,
        "direction_weight": direction_weight(direction),
    }


def best_tradeoff_subspace_direction(
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
            info["repair_forced_count"],
            info["preserve_forced_count"],
            info["spillover_forced_count"],
            info["forced_pair_count"],
            info["direction_weight"],
            info["direction"],
        )
        if best is None or key < (
            best["repair_forced_count"],
            best["preserve_forced_count"],
            best["spillover_forced_count"],
            best["forced_pair_count"],
            best["direction_weight"],
            best["direction"],
        ):
            best = info
    return best


def analyze_profile(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)
    base_indices = rowspan.row_indices_for_classes(row_classes, rowspan.BASE_ZERO_CLASSES)
    extended_indices = rowspan.row_indices_for_classes(row_classes, rowspan.EXTENDED_ZERO_CLASSES)
    row = {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "seed_offset": candidate.get("seed_offset"),
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "row_classes": row_classes,
        "target_rows_present": base_indices is not None and extended_indices is not None,
        "base_row_indices": base_indices,
        "extended_row_indices": extended_indices,
        "best_failure_mode": "P46P67_TARGET_ROWS_MISSING",
    }
    if base_indices is None or extended_indices is None:
        return row

    base_rows = [matrix[idx] for idx in base_indices]
    extended_rows = [matrix[idx] for idx in extended_indices]
    base_rank = chamber.rank_rows(base_rows)
    extended_rank = chamber.rank_rows(extended_rows)
    base_best = best_tradeoff_subspace_direction(matrix, base_indices, pair_labels, pair_rows)
    extended_best = best_tradeoff_subspace_direction(matrix, extended_indices, pair_labels, pair_rows)
    row.update(
        {
            "base_rank": base_rank,
            "base_nullity": TEMPLATE_DIM - base_rank,
            "extended_rank": extended_rank,
            "extended_nullity": TEMPLATE_DIM - extended_rank,
            "extended_rank_slack": extended_rank <= 4,
            "base_tradeoff_direction": base_best,
            "extended_tradeoff_direction": extended_best,
        }
    )
    if extended_rank <= 4 and extended_best and extended_best["forced_pair_count"] == 0:
        row["best_failure_mode"] = "P46P67_EXACT_PAIRCLEAR_REPAIRED"
    elif (
        extended_rank <= 4
        and extended_best
        and extended_best["repair_forced_count"] == 0
        and extended_best["preserve_forced_count"] == 0
        and extended_best["spillover_forced_count"] == 0
    ):
        row["best_failure_mode"] = "P46P67_TRADEOFF_REPAIRED_OTHER_FORCED"
    elif extended_rank <= 4 and extended_best and extended_best["repair_forced_count"] == 0:
        row["best_failure_mode"] = "P46P67_REPAIR_CLEAR_BUT_GUARDS_LOST"
    elif (
        extended_rank <= 4
        and extended_best
        and extended_best["repair_forced_count"] <= 1
        and extended_best["preserve_forced_count"] == 0
    ):
        row["best_failure_mode"] = "P46P67_NEAR_REPAIR"
    elif extended_rank <= 4:
        row["best_failure_mode"] = "P46P67_FORCED_PROJECTIONS_REMAIN"
    elif extended_best and extended_best["forced_pair_count"] == 0:
        row["best_failure_mode"] = "P46P67_SUPPORT_ONLY"
    else:
        row["best_failure_mode"] = "P46P67_BASE_NOT_RANKSLACK"
    return row


def tradeoff_score_key(row: dict[str, Any]) -> tuple[Any, ...]:
    info = row.get("extended_tradeoff_direction") or {}
    priority = {
        "P46P67_EXACT_PAIRCLEAR_REPAIRED": 0,
        "P46P67_TRADEOFF_REPAIRED_OTHER_FORCED": 1,
        "P46P67_REPAIR_CLEAR_BUT_GUARDS_LOST": 2,
        "P46P67_NEAR_REPAIR": 3,
        "P46P67_FORCED_PROJECTIONS_REMAIN": 4,
        "P46P67_SUPPORT_ONLY": 5,
        "P46P67_BASE_NOT_RANKSLACK": 6,
        "P46P67_TARGET_ROWS_MISSING": 7,
    }.get(row["best_failure_mode"], 9)
    return (
        priority,
        info.get("repair_forced_count", 99),
        info.get("preserve_forced_count", 99),
        info.get("spillover_forced_count", 99),
        info.get("forced_pair_count", 99),
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
        "basis_support_sizes",
        "coefficient_matrix_shape",
        "target_rows_present",
        "base_rank",
        "base_nullity",
        "extended_rank",
        "extended_nullity",
        "extended_rank_slack",
        "base_tradeoff_direction",
        "extended_tradeoff_direction",
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
    previous_search = previous["p45_p46_p56_codesign"]
    profiles, screened, selected_candidates = p456.structural_candidates(
        max_mutations=max_mutations,
        seed_offsets=seed_offsets,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )
    analyzed = []
    basis_profiles_tested = 0
    for candidate, _screen in selected_candidates:
        for profile in rowspan.target_aware_basis_profiles(
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
        if (row.get("extended_tradeoff_direction") or {}).get("forced_pair_count") == 0
    ]
    tradeoff_repaired = [
        row
        for row in extended_rank_slack
        if (row.get("extended_tradeoff_direction") or {}).get("repair_forced_count") == 0
        and (row.get("extended_tradeoff_direction") or {}).get("preserve_forced_count") == 0
    ]
    clean_tradeoff = [
        row
        for row in tradeoff_repaired
        if (row.get("extended_tradeoff_direction") or {}).get("spillover_forced_count") == 0
    ]
    near = [
        row
        for row in extended_rank_slack
        if (row.get("extended_tradeoff_direction") or {}).get("repair_forced_count", 99) <= 1
        and (row.get("extended_tradeoff_direction") or {}).get("preserve_forced_count") == 0
    ]
    best = min(analyzed, key=tradeoff_score_key) if analyzed else None

    forced_patterns = Counter()
    repair_forced_counts = Counter()
    preserve_forced_counts = Counter()
    spillover_forced_counts = Counter()
    total_forced_counts = Counter()
    for row in extended_rank_slack:
        info = row.get("extended_tradeoff_direction") or {}
        forced_patterns[",".join(info.get("forced_pairs") or [])] += 1
        repair_forced_counts[str(info.get("repair_forced_count", 99))] += 1
        preserve_forced_counts[str(info.get("preserve_forced_count", 99))] += 1
        spillover_forced_counts[str(info.get("spillover_forced_count", 99))] += 1
        total_forced_counts[str(info.get("forced_pair_count", 99))] += 1

    failure = "P46P67_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / P46P67_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if best:
        failure = best["best_failure_mode"]
        if failure == "P46P67_EXACT_PAIRCLEAR_REPAIRED":
            proof_status = "CANDIDATE / P46P67_EXACT_PAIRCLEAR_REPAIRED / PARTIAL / EXPERIMENTAL"
        elif failure in {
            "P46P67_TRADEOFF_REPAIRED_OTHER_FORCED",
            "P46P67_REPAIR_CLEAR_BUT_GUARDS_LOST",
            "P46P67_NEAR_REPAIR",
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
        "previous_p45_p46_p56_codesign": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_tested": previous_search["basis_profiles_tested"],
            "extended_rank_slack_profiles": previous_search["extended_rank_slack_profiles"],
            "best_failure_mode": previous_search["best_failure_mode"],
            "best_forced_pairs": previous["best_profile"]["extended_codesign_direction"]["forced_pairs"],
            "best_target_pairs_cleared": previous["best_profile"]["extended_codesign_direction"]["target_pairs_cleared"],
            "best_preserve_pairs_cleared": previous["best_profile"]["extended_codesign_direction"]["preserve_pairs_cleared"],
        },
        "p46_p67_tradeoff_repair": {
            "repair_pairs": REPAIR_PAIRS,
            "preserve_clear_pairs": PRESERVE_CLEAR_PAIRS,
            "spillover_avoid_pairs": SPILLOVER_AVOID_PAIRS,
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
            "tradeoff_repaired_profiles": len(tradeoff_repaired),
            "clean_tradeoff_repaired_profiles": len(clean_tradeoff),
            "near_repair_profiles": len(near),
            "repair_forced_count_histogram": dict(repair_forced_counts),
            "preserve_forced_count_histogram": dict(preserve_forced_counts),
            "spillover_forced_count_histogram": dict(spillover_forced_counts),
            "total_forced_count_histogram": dict(total_forced_counts),
            "forced_pair_pattern_counts": dict(forced_patterns.most_common(16)),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_id": None if best is None else best["basis_id"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in screened)),
        },
        "best_profile": None if best is None else compact_profile(best),
        "profile_summaries": [compact_profile(row) for row in sorted(analyzed, key=tradeoff_score_key)[:40]],
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
            "global obstruction outside the tested P46/P67 tradeoff front",
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
    parser.add_argument("--random-bases", type=int, default=128)
    parser.add_argument("--max-basis-profiles", type=int, default=10)
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
        search = record["p46_p67_tradeoff_repair"]
        best = record["best_profile"]
        best_info = None if best is None else best.get("extended_tradeoff_direction")
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
                    "tradeoff_repaired_profiles": search["tradeoff_repaired_profiles"],
                    "clean_tradeoff_repaired_profiles": search["clean_tradeoff_repaired_profiles"],
                    "near_repair_profiles": search["near_repair_profiles"],
                    "repair_forced_count_histogram": search["repair_forced_count_histogram"],
                    "best_template_id": search["best_template_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_forced_pairs": None if best_info is None else best_info["forced_pairs"],
                    "best_repair_pairs_cleared": None if best_info is None else best_info["repair_pairs_cleared"],
                    "best_preserve_pairs_cleared": None if best_info is None else best_info["preserve_pairs_cleared"],
                    "best_spillover_pairs_cleared": None if best_info is None else best_info["spillover_pairs_cleared"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_P46_P67_TRADEOFF_REPAIR_READY")


if __name__ == "__main__":
    main()
