#!/usr/bin/env python3
"""Reconstruct the best cycle-guarded exact pair-clear rank-slack chamber."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "0fc5a00"
SOURCE_DATA = Path("experimental/data/m1_a327_cycle_guarded_template_front_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_exact_pairclear_chamber_realization.json")

ROOT = Path(__file__).resolve().parents[2]
CYCLEG_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycle_guarded_template_front_search.py"

P = 17
K = 256
TARGET_AGREEMENT = 327
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cycleg = load_module("cycle_guarded_template_front_search", CYCLEG_SCRIPT)
p456 = cycleg.p456
chamber = cycleg.chamber
zstable = cycleg.zstable


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def reconstruct_target(source: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    best = source["best_profile"]
    target_mutation = best["mutation_id"]
    target_assignment = best["assignment_strategy"]
    target_seed = int(best["assignment_seed"])
    target_basis = best["basis_id"]

    specs = p456.ninerow.mutation_specs(max_mutations=source["cycle_guarded_template_front"]["max_mutations"])
    profile_index = None
    spec = None
    for idx, candidate_spec in enumerate(specs):
        if candidate_spec.get("mutation_id") == target_mutation:
            profile_index = idx
            spec = candidate_spec
            break
    if spec is None or profile_index is None:
        raise RuntimeError(f"could not find mutation spec {target_mutation}")

    template_profile = p456.lowrank.solve_template_counts(spec)
    strategy_index = template_profile["assignment_strategies"].index(target_assignment)
    seed_offset = None
    for offset in range(source["cycle_guarded_template_front"]["seed_offsets"]):
        seed = 131000 + 97 * profile_index + strategy_index + 1009 * offset
        if seed == target_seed:
            seed_offset = offset
            break
    if seed_offset is None:
        raise RuntimeError(f"could not recover seed offset for seed {target_seed}")

    candidate = p456.diverse.candidate_from_profile(template_profile, target_assignment, seed=target_seed)
    candidate["mutation_id"] = spec.get("mutation_id")
    candidate["base_template_id"] = spec.get("base_template_id")
    candidate["seed_offset"] = seed_offset

    basis_profile = None
    for profile in cycleg.tchamber.basis_profiles(
        candidate,
        top_classes=source["cycle_guarded_template_front"]["top_classes"],
        random_bases=source["cycle_guarded_template_front"]["random_bases"],
        limit=source["cycle_guarded_template_front"]["max_basis_profiles"],
    ):
        if profile["basis_id"] == target_basis:
            basis_profile = profile
            break
    if basis_profile is None:
        raise RuntimeError(f"could not reconstruct basis profile {target_basis}")
    return candidate, basis_profile, template_profile


def class_position_sets(classes: list[dict[str, Any]]) -> dict[int, set[int]]:
    return {
        int(row["class_index"]): {int(pos) for pos in row["positions"]}
        for row in classes
    }


def class_ledger(class_indices: list[int], classes: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "class_index": int(idx),
            "support_size": int(classes[int(idx)]["support_size"]),
            "forced_identity": bool(classes[int(idx)]["forced_identity"]),
            "positions_hash": classes[int(idx)]["positions_hash"],
        }
        for idx in class_indices
    ]


def quotient_fiber_histogram(positions: set[int]) -> dict[str, int]:
    counts = Counter(str(int(pos) // 32) for pos in positions)
    return {str(idx): counts.get(str(idx), 0) for idx in range(16)}


def build_vector(coeffs: list[int], basis: list[list[int]]) -> list[int]:
    vector = [0] * TEMPLATE_DIM
    for scalar, basis_vector in zip(coeffs, basis, strict=True):
        for idx in range(TEMPLATE_DIM):
            vector[idx] = (vector[idx] + int(scalar) * int(basis_vector[idx])) % P
    return chamber.normalize_projective(vector)


def slack_subspace_summary(pair_labels: list[str], pair_rows: list[list[int]], basis: list[list[int]]) -> dict[str, Any]:
    forced_pattern_counts: Counter[str] = Counter()
    pairclear_vectors = []
    directions_tested = 0
    for coeffs in chamber.projective_directions(len(basis)):
        vector = build_vector(coeffs, basis)
        pair_values = chamber.linear_image_rows(pair_rows, vector)
        forced = [pair_labels[idx] for idx, value in enumerate(pair_values) if value % P == 0]
        forced_pattern_counts[",".join(forced)] += 1
        directions_tested += 1
        if not forced:
            pairclear_vectors.append(vector)
    return {
        "basis": basis,
        "projective_directions_tested": directions_tested,
        "pairclear_directions": len(pairclear_vectors),
        "pairclear_direction_examples": pairclear_vectors[:8],
        "forced_pair_pattern_counts": dict(forced_pattern_counts),
    }


def chamber_realization_status(row: dict[str, Any]) -> tuple[str, str]:
    if not row["reconstruction_matches_source"]:
        return (
            "EXACT_EXTRACTION_NO_A327 / CYCLEG_REALIZATION_RECONSTRUCTION_MISMATCH / PARTIAL / EXPERIMENTAL",
            "CYCLEG_REALIZATION_RECONSTRUCTION_MISMATCH",
        )
    if row["best_chamber"]["forced_pairs"]:
        return (
            "EXACT_EXTRACTION_NO_A327 / CYCLEG_REALIZATION_PAIR_FORCED / PARTIAL / EXPERIMENTAL",
            "CYCLEG_REALIZATION_PAIR_FORCED",
        )
    if row["best_chamber"]["inactive_rank"] > 4:
        return (
            "EXACT_EXTRACTION_NO_A327 / CYCLEG_REALIZATION_NO_RANKSLACK / PARTIAL / EXPERIMENTAL",
            "CYCLEG_REALIZATION_NO_RANKSLACK",
        )
    if row["scalar_required_vanishing_union_size"] < K:
        return (
            "CANDIDATE / CYCLEG_REALIZATION_SCALAR_STABLE_WINDOW / PARTIAL / EXPERIMENTAL",
            "CYCLEG_REALIZATION_SCALAR_STABLE_WINDOW",
        )
    if row["zero_class_union_size"] < K:
        return (
            "CANDIDATE / CYCLEG_REALIZATION_BASIS_QUOTIENT_TARGET / PARTIAL / EXPERIMENTAL",
            "CYCLEG_REALIZATION_BASIS_QUOTIENT_TARGET",
        )
    return (
        "EXACT_EXTRACTION_NO_A327 / CYCLEG_REALIZATION_NO_WINDOW / PARTIAL / EXPERIMENTAL",
        "CYCLEG_REALIZATION_NO_WINDOW",
    )


def build_record() -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    candidate, profile, template_profile = reconstruct_target(source)
    source_best = source["best_profile"]
    source_chamber = source_best["best_exact_pairclear_rank_slack_chamber"]

    classes = zstable.functional.functional_classes(candidate)
    classes_by_index = {int(row["class_index"]): row for row in classes}
    positions = class_position_sets(classes)
    structural_row = zstable.candidate_structural_row(candidate)

    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    pair_labels, pair_rows = chamber.pair_projection_matrix(candidate, profile)

    direction = [int(value) % P for value in source_chamber["direction"]]
    row_values = chamber.linear_image_rows(matrix, direction)
    zero_indices = tuple(idx for idx, value in enumerate(row_values) if value % P == 0)
    pair_values = chamber.linear_image_rows(pair_rows, direction)
    forced_pairs = [pair_labels[idx] for idx, value in enumerate(pair_values) if value % P == 0]
    chamber_info = cycleg.forced_pair_info(pair_labels, pair_values)
    best_chamber = cycleg.chamber_record_for(zero_indices, matrix, row_classes, direction, chamber_info)

    zero_classes = [row_classes[idx] for idx in zero_indices]
    active_classes = [row_classes[idx] for idx in range(len(row_classes)) if idx not in set(zero_indices)]
    nonzero_basis_classes = [
        int(class_index)
        for class_index, scalar in zip(profile["basis_class_indices"], direction, strict=True)
        if int(scalar) % P
    ]
    scalar_required_classes = sorted(set(active_classes + nonzero_basis_classes))
    zero_positions: set[int] = set()
    active_positions: set[int] = set()
    scalar_required_positions: set[int] = set()
    for class_index in zero_classes:
        zero_positions |= positions[int(class_index)]
    for class_index in active_classes:
        active_positions |= positions[int(class_index)]
    for class_index in scalar_required_classes:
        scalar_required_positions |= positions[int(class_index)]

    inactive_rows = [matrix[idx] for idx in zero_indices]
    inactive_rank = chamber.rank_rows(inactive_rows)
    inactive_kernel = chamber.nullspace_basis(inactive_rows)
    slack = slack_subspace_summary(pair_labels, pair_rows, inactive_kernel)

    reconstruction_matches_source = (
        candidate["template_id"] == source_best["template_id"]
        and candidate["assignment_strategy"] == source_best["assignment_strategy"]
        and int(candidate["assignment_seed"]) == int(source_best["assignment_seed"])
        and profile["basis_id"] == source_best["basis_id"]
        and best_chamber["zero_row_classes"] == source_chamber["zero_row_classes"]
        and best_chamber["forced_pairs"] == source_chamber["forced_pairs"]
        and best_chamber["inactive_rank"] == source_chamber["inactive_rank"]
        and best_chamber["inactive_kernel_nullity"] == source_chamber["inactive_kernel_nullity"]
    )

    realization_core = {
        "reconstruction_matches_source": reconstruction_matches_source,
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "base_template_id": candidate.get("base_template_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "seed_offset": candidate.get("seed_offset"),
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "basis_functionals": profile["basis_functionals"],
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "row_classes": row_classes,
        "pair_projection_labels": pair_labels,
        "best_chamber": best_chamber,
        "pair_projection_values": {label: int(value) % P for label, value in zip(pair_labels, pair_values, strict=True)},
        "forced_pairs": forced_pairs,
        "zero_class_ledger": class_ledger(zero_classes, classes_by_index),
        "active_class_ledger": class_ledger(active_classes, classes_by_index),
        "nonzero_basis_class_ledger": class_ledger(nonzero_basis_classes, classes_by_index),
        "scalar_required_class_ledger": class_ledger(scalar_required_classes, classes_by_index),
        "zero_class_union_size": len(zero_positions),
        "zero_class_union_hash": hash_payload(sorted(zero_positions)),
        "zero_class_fiber_histogram": quotient_fiber_histogram(zero_positions),
        "zero_row_window_dimension": max(0, K - len(zero_positions)),
        "active_class_union_size": len(active_positions),
        "scalar_required_vanishing_union_size": len(scalar_required_positions),
        "scalar_required_vanishing_union_hash": hash_payload(sorted(scalar_required_positions)),
        "scalar_required_fiber_histogram": quotient_fiber_histogram(scalar_required_positions),
        "scalar_stable_window_dimension": max(0, K - len(scalar_required_positions)),
        "inactive_rank": inactive_rank,
        "inactive_kernel_nullity": TEMPLATE_DIM - inactive_rank,
        "rank_slack_subspace": slack,
        "template_vectors_hash": hash_payload(candidate["template_vectors"]),
        "coordinate_classes_hash": candidate["coordinate_classes_hash"],
    }
    proof_status, failure = chamber_realization_status(realization_core)

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "cycle_guarded_front": {
            "commit": SOURCE_COMMIT,
            "proof_status": source["proof_status"],
            "basis_profiles_tested": source["cycle_guarded_template_front"]["basis_profiles_tested"],
            "exact_pairclear_profiles": source["cycle_guarded_template_front"]["exact_pairclear_profiles"],
            "exact_pairclear_rank_slack_profiles": source["cycle_guarded_template_front"]["exact_pairclear_rank_slack_profiles"],
            "best_template_id": source["cycle_guarded_template_front"]["best_template_id"],
            "best_basis_id": source["cycle_guarded_template_front"]["best_basis_id"],
            "best_failure_mode": source["cycle_guarded_template_front"]["best_failure_mode"],
        },
        "candidate_structural_row": structural_row,
        "template_profile": {
            "mutation_id": template_profile.get("mutation_id"),
            "base_template_id": template_profile.get("base_template_id"),
            "solver_status": template_profile.get("solver_status"),
            "assignment_strategies": template_profile.get("assignment_strategies"),
        },
        "chamber_realization": {
            **realization_core,
            "best_failure_mode": failure,
        },
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
            "global obstruction outside the tested cycle-guarded chamber",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        realization = record["chamber_realization"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "reconstruction_matches_source": realization["reconstruction_matches_source"],
                    "best_template_id": realization["template_id"],
                    "best_basis_id": realization["basis_id"],
                    "best_direction": realization["best_chamber"]["direction"],
                    "forced_pairs": realization["forced_pairs"],
                    "zero_row_count": realization["best_chamber"]["zero_row_count"],
                    "inactive_rank": realization["inactive_rank"],
                    "inactive_kernel_nullity": realization["inactive_kernel_nullity"],
                    "zero_class_union_size": realization["zero_class_union_size"],
                    "zero_row_window_dimension": realization["zero_row_window_dimension"],
                    "scalar_required_vanishing_union_size": realization["scalar_required_vanishing_union_size"],
                    "scalar_stable_window_dimension": realization["scalar_stable_window_dimension"],
                    "slack_pairclear_directions": realization["rank_slack_subspace"]["pairclear_directions"],
                    "best_failure_mode": realization["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_CYCLEGUARD_EXACT_PAIRCLEAR_CHAMBER_REALIZATION_READY")


if __name__ == "__main__":
    main()
