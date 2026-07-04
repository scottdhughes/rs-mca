#!/usr/bin/env python3
"""Focused seven-to-eight repair for the M1 a=327 pair-clear rank-slack front."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "36eac30"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_deeper_rankslack_front.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_rankslack_seven_to_eight_repair.json")

ROOT = Path(__file__).resolve().parents[2]
DIVERSE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_diverse_chamber_front.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327

TARGET_MUTATION_ID = "w3_c3_d1"
TARGET_TEMPLATE_ID = "ninerow_w3_c3_d1"
TARGET_ASSIGNMENT_STRATEGY = "fiber_round_robin"
TARGET_ASSIGNMENT_SEED = 117186
TARGET_BASIS_CLASS_INDICES = [0, 1, 2, 3, 5, 10]
TARGET_BASIS_ID = "basisaware_0_1_2_3_5_10"
TARGET_RANKSLACK_ZERO_CLASSES = [6, 7, 8, 14, 18, 19, 20]
TARGET_REPAIR_ROW_CLASS = 17


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


def normalize_projective(vector: list[int]) -> list[int]:
    return chamber.normalize_projective(vector)


def direction_weight(vector: list[int]) -> int:
    return sum(1 for value in vector if int(value) % P)


def compact_chamber(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    keys = [
        "zero_row_count",
        "active_row_count",
        "inactive_rank",
        "inactive_kernel_nullity",
        "zero_row_indices",
        "zero_row_classes",
        "active_row_indices",
        "active_row_classes",
        "exemplar_direction",
        "exemplar_direction_projective",
        "exemplar_weight",
    ]
    return {key: row.get(key) for key in keys}


def reconstruct_target() -> tuple[dict[str, Any], dict[str, Any]]:
    specs = ninerow.mutation_specs(max_mutations=240)
    target_spec = None
    for spec in specs:
        if spec.get("mutation_id") == TARGET_MUTATION_ID:
            target_spec = spec
            break
    if target_spec is None:
        raise RuntimeError(f"could not find mutation spec {TARGET_MUTATION_ID}")

    profile = lowrank.solve_template_counts(target_spec)
    profile["mutation_id"] = target_spec.get("mutation_id")
    profile["base_template_id"] = target_spec.get("base_template_id")
    candidate = diverse.candidate_from_profile(profile, TARGET_ASSIGNMENT_STRATEGY, seed=TARGET_ASSIGNMENT_SEED)
    if candidate["template_id"] != TARGET_TEMPLATE_ID:
        raise RuntimeError(f"wrong reconstructed template {candidate['template_id']}")

    classes = basisaware.functional.functional_classes(candidate)
    by_class = {int(row["class_index"]): idx for idx, row in enumerate(classes)}
    selected = tuple(by_class[class_index] for class_index in TARGET_BASIS_CLASS_INDICES)
    basis_profile = basisaware.profile_from_indices(classes, selected, TARGET_BASIS_ID)
    if basis_profile is None:
        raise RuntimeError(f"could not reconstruct basis profile {TARGET_BASIS_ID}")
    return candidate, basis_profile


def enumerate_chambers(
    matrix: list[list[int]],
    row_classes: list[int],
    pair_rows: list[list[int]],
    direction_limit: int | None,
) -> dict[str, Any]:
    chamber_exemplars: dict[tuple[int, ...], list[int]] = {}
    directions_tested = 0
    pair_clear_directions = 0
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
        old = chamber_exemplars.get(zero_indices)
        if old is None or (direction_weight(vector), vector) < (direction_weight(old), old):
            chamber_exemplars[zero_indices] = vector

    chambers = [
        chamber.chamber_record(zero_indices, matrix, row_classes, exemplar)
        for zero_indices, exemplar in chamber_exemplars.items()
    ]
    return {
        "directions_tested": directions_tested,
        "pair_clear_directions": pair_clear_directions,
        "chambers": chambers,
    }


def extension_attempt_record(
    base_chamber: dict[str, Any],
    active_idx: int,
    matrix: list[list[int]],
    row_classes: list[int],
    pair_rows: list[list[int]],
) -> dict[str, Any]:
    extended_zero_indices = tuple(sorted(base_chamber["zero_row_indices"] + [active_idx]))
    rows = [matrix[idx] for idx in extended_zero_indices]
    rank = chamber.rank_rows(rows)
    nullity = TEMPLATE_DIM - rank
    direction = None
    if nullity > 0:
        basis = chamber.nullspace_basis(rows)
        direction = chamber.pair_clear_vector_in_subspace(pair_rows, basis)
    return {
        "base_zero_row_count": base_chamber["zero_row_count"],
        "base_inactive_rank": base_chamber["inactive_rank"],
        "base_inactive_kernel_nullity": base_chamber["inactive_kernel_nullity"],
        "base_zero_row_indices": base_chamber["zero_row_indices"],
        "base_zero_row_classes": base_chamber["zero_row_classes"],
        "base_exemplar_direction": base_chamber["exemplar_direction"],
        "added_active_row_index": active_idx,
        "added_active_row_class": row_classes[active_idx],
        "zero_row_count": len(extended_zero_indices),
        "active_row_count": len(matrix) - len(extended_zero_indices),
        "inactive_rank": rank,
        "inactive_kernel_nullity": nullity,
        "zero_row_indices": list(extended_zero_indices),
        "zero_row_classes": [row_classes[idx] for idx in extended_zero_indices],
        "active_row_indices": [idx for idx in range(len(matrix)) if idx not in set(extended_zero_indices)],
        "active_row_classes": [row_classes[idx] for idx in range(len(matrix)) if idx not in set(extended_zero_indices)],
        "pair_clear": direction is not None,
        "pair_clear_direction": direction,
        "pair_clear_direction_weight": None if direction is None else direction_weight(direction),
        "rank_preserved": rank <= int(base_chamber["inactive_rank"]),
        "deep_rank_slack": len(extended_zero_indices) >= 8 and rank <= 4 and direction is not None,
        "support_reduced_pair_clear": len(extended_zero_indices) >= 8 and direction is not None,
    }


def extension_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        0 if row["deep_rank_slack"] else 1,
        0 if row["support_reduced_pair_clear"] else 1,
        -row["zero_row_count"],
        row["inactive_rank"],
        row["active_row_count"],
        row["pair_clear_direction_weight"] if row["pair_clear_direction_weight"] is not None else 99,
        row["added_active_row_class"],
        row["base_zero_row_classes"],
    )


def compact_extension(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    keys = [
        "base_zero_row_count",
        "base_inactive_rank",
        "base_inactive_kernel_nullity",
        "base_zero_row_classes",
        "base_exemplar_direction",
        "added_active_row_class",
        "zero_row_count",
        "active_row_count",
        "inactive_rank",
        "inactive_kernel_nullity",
        "zero_row_classes",
        "active_row_classes",
        "pair_clear",
        "pair_clear_direction",
        "pair_clear_direction_weight",
        "rank_preserved",
        "deep_rank_slack",
        "support_reduced_pair_clear",
    ]
    return {key: row.get(key) for key in keys}


def build_record(direction_limit: int | None) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    previous_front = previous["deeper_rank_slack_front"]
    previous_best = previous["best_full_profile"]
    candidate, profile = reconstruct_target()
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)

    enumerated = enumerate_chambers(matrix, row_classes, pair_rows, direction_limit=direction_limit)
    chambers = enumerated["chambers"]
    rank_slack = [row for row in chambers if row["zero_row_count"] >= 5 and row["inactive_rank"] <= 4]
    rank_slack_zero7 = [row for row in rank_slack if row["zero_row_count"] == 7]
    rank_slack_zero8 = [row for row in rank_slack if row["zero_row_count"] >= 8]
    direct_support = [row for row in chambers if row["zero_row_count"] >= 8]

    target_base = next(
        (
            row
            for row in rank_slack
            if row["zero_row_classes"] == TARGET_RANKSLACK_ZERO_CLASSES
        ),
        None,
    )

    extension_attempts: list[dict[str, Any]] = []
    for base in rank_slack:
        zero_set = set(base["zero_row_indices"])
        for active_idx in range(len(matrix)):
            if active_idx in zero_set:
                continue
            extension_attempts.append(extension_attempt_record(base, active_idx, matrix, row_classes, pair_rows))

    target_row_attempts = [
        row
        for row in extension_attempts
        if row["base_zero_row_classes"] == TARGET_RANKSLACK_ZERO_CLASSES
        and row["added_active_row_class"] == TARGET_REPAIR_ROW_CLASS
    ]
    pair_clear_extensions = [row for row in extension_attempts if row["pair_clear"]]
    support_extensions = [row for row in extension_attempts if row["support_reduced_pair_clear"]]
    deep_extensions = [row for row in extension_attempts if row["deep_rank_slack"]]
    rank_preserving_attempts = [
        row
        for row in extension_attempts
        if row["zero_row_count"] >= 8 and row["inactive_rank"] <= 4
    ]
    rank_preserving_pairclear_attempts = [
        row for row in rank_preserving_attempts if row["pair_clear"]
    ]

    best_extension = min(pair_clear_extensions, key=extension_sort_key) if pair_clear_extensions else None
    best_deep_extension = min(deep_extensions, key=extension_sort_key) if deep_extensions else None
    best_support_extension = min(support_extensions, key=extension_sort_key) if support_extensions else None
    target_row17_attempt = min(target_row_attempts, key=extension_sort_key) if target_row_attempts else None

    failure = "SEVEN_TO_EIGHT_NO_EXTENSION_ATTEMPTS"
    proof_status = "EXACT_EXTRACTION_NO_A327 / SEVEN_TO_EIGHT_NO_EXTENSION_ATTEMPTS / PARTIAL / EXPERIMENTAL"
    if deep_extensions:
        failure = "SEVEN_TO_EIGHT_RANKSLACK_REPAIRED"
        proof_status = "CANDIDATE / SEVEN_TO_EIGHT_RANKSLACK_REPAIRED / PARTIAL / EXPERIMENTAL"
    elif rank_preserving_attempts:
        failure = "SEVEN_TO_EIGHT_RANK_PRESERVED_PAIRCLEAR_FAIL"
        proof_status = "EXACT_EXTRACTION_NO_A327 / SEVEN_TO_EIGHT_RANK_PRESERVED_PAIRCLEAR_FAIL / PARTIAL / EXPERIMENTAL"
    elif support_extensions:
        failure = "SEVEN_TO_EIGHT_SUPPORT_ONLY"
        proof_status = "CANDIDATE / SEVEN_TO_EIGHT_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL"
    elif extension_attempts:
        failure = "SEVEN_TO_EIGHT_EXTENSION_NOT_REPAIRED"
        proof_status = "EXACT_EXTRACTION_NO_A327 / SEVEN_TO_EIGHT_EXTENSION_NOT_REPAIRED / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_deeper_rank_slack_front": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "full_deep_rank_slack_profiles": previous_front["full_deep_rank_slack_profiles"],
            "full_direct_support_reduced_profiles": previous_front["full_direct_support_reduced_profiles"],
            "best_template_id": previous_front["best_template_id"],
            "best_mutation_id": previous_front["best_mutation_id"],
            "best_basis_id": previous_front["best_basis_id"],
            "best_failure_mode": previous_front["best_failure_mode"],
        },
        "target_profile": {
            "template_id": candidate["template_id"],
            "mutation_id": candidate.get("mutation_id"),
            "assignment_strategy": candidate["assignment_strategy"],
            "assignment_seed": candidate["assignment_seed"],
            "basis_id": profile["basis_id"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
            "row_classes": row_classes,
            "pair_projection_labels": pair_labels,
            "previous_best_direct_support_reduced_chamber": previous_best["best_direct_support_reduced_chamber"],
            "previous_best_rank_slack_chamber": previous_best["best_rank_slack_chamber"],
        },
        "seven_to_eight_repair": {
            "direction_limit": direction_limit,
            "directions_tested": enumerated["directions_tested"],
            "pair_clear_directions": enumerated["pair_clear_directions"],
            "distinct_pair_clear_chambers": len(chambers),
            "direct_support_reduced_chambers": len(direct_support),
            "rank_slack_chambers": len(rank_slack),
            "rank_slack_zero7_chambers": len(rank_slack_zero7),
            "rank_slack_zero8_chambers": len(rank_slack_zero8),
            "extension_attempts": len(extension_attempts),
            "rank_preserving_extension_attempts": len(rank_preserving_attempts),
            "rank_preserving_pairclear_extensions": len(rank_preserving_pairclear_attempts),
            "pair_clear_extensions": len(pair_clear_extensions),
            "support_reduced_pairclear_extensions": len(support_extensions),
            "deep_rank_slack_extensions": len(deep_extensions),
            "target_row_class": TARGET_REPAIR_ROW_CLASS,
            "target_row_attempts": len(target_row_attempts),
            "best_failure_mode": failure,
            "extension_failure_counts": dict(
                Counter(
                    "deep_rank_slack"
                    if row["deep_rank_slack"]
                    else "support_pairclear"
                    if row["support_reduced_pair_clear"]
                    else "pairclear_lower_support"
                    if row["pair_clear"]
                    else "rank_preserved_pairclear_fail"
                    if row["zero_row_count"] >= 8 and row["inactive_rank"] <= 4
                    else "no_pairclear"
                    for row in extension_attempts
                )
            ),
        },
        "target_rank_slack_chamber": compact_chamber(target_base),
        "target_row17_attempt": compact_extension(target_row17_attempt),
        "best_extension": compact_extension(best_extension),
        "best_support_reduced_extension": compact_extension(best_support_extension),
        "best_deep_rank_slack_extension": compact_extension(best_deep_extension),
        "rank_slack_chamber_summaries": [compact_chamber(row) for row in sorted(rank_slack, key=chamber.rank_slack_sort_key)[:20]],
        "extension_summaries": [compact_extension(row) for row in sorted(extension_attempts, key=extension_sort_key)[:30]],
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
            "global obstruction outside the tested seven-to-eight repair front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--direction-limit", type=int, default=None)
    args = parser.parse_args()
    record = build_record(direction_limit=args.direction_limit)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["seven_to_eight_repair"]
        target = record["target_row17_attempt"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "directions_tested": search["directions_tested"],
                    "pair_clear_directions": search["pair_clear_directions"],
                    "distinct_pair_clear_chambers": search["distinct_pair_clear_chambers"],
                    "rank_slack_chambers": search["rank_slack_chambers"],
                    "rank_slack_zero7_chambers": search["rank_slack_zero7_chambers"],
                    "rank_slack_zero8_chambers": search["rank_slack_zero8_chambers"],
                    "extension_attempts": search["extension_attempts"],
                    "rank_preserving_pairclear_extensions": search["rank_preserving_pairclear_extensions"],
                    "support_reduced_pairclear_extensions": search["support_reduced_pairclear_extensions"],
                    "deep_rank_slack_extensions": search["deep_rank_slack_extensions"],
                    "target_row17_inactive_rank": None if target is None else target["inactive_rank"],
                    "target_row17_pair_clear": None if target is None else target["pair_clear"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_RANKSLACK_SEVEN_TO_EIGHT_REPAIR_READY")


if __name__ == "__main__":
    main()
