#!/usr/bin/env python3
"""Prescribe pair-clear nonbasis kernels for M1 a=327 realized templates."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "46b73ec"
PREVIOUS_DATA = Path("experimental/data/m1_a327_nonbasis_row_dependency_ansatz.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_prescribed_nonbasis_kernel_generator.json")

ROOT = Path(__file__).resolve().parents[2]
RANKDEFECT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_rankdefect_template_ansatz.py"

P = 17
K = 256
TARGET_AGREEMENT = 327
TEMPLATE_DIM = 6
DEFAULT_ROW_REMOVAL_LIMIT = 3


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rankdefect = load_module("rankdefect_template_ansatz", RANKDEFECT_SCRIPT)
codesign = rankdefect.codesign
joint = rankdefect.joint
zstable = codesign.zstable
functional = codesign.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_rows(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> int:
    matrix = [[int(value) % P for value in row] for row in rows if any(int(value) % P for value in row)]
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % P:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, P)
        matrix[rank] = [(value * inv) % P for value in matrix[rank]]
        for row_idx in range(rank + 1, len(matrix)):
            if not matrix[row_idx][col] % P:
                continue
            factor = matrix[row_idx][col] % P
            matrix[row_idx] = [(matrix[row_idx][idx] - factor * matrix[rank][idx]) % P for idx in range(ncols)]
        rank += 1
        if rank == ncols:
            break
    return rank


def rref(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> tuple[list[list[int]], list[int]]:
    matrix = [[int(value) % P for value in row] for row in rows if any(int(value) % P for value in row)]
    pivots: list[int] = []
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % P:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, P)
        matrix[rank] = [(value * inv) % P for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % P:
                continue
            factor = matrix[row_idx][col] % P
            matrix[row_idx] = [(matrix[row_idx][idx] - factor * matrix[rank][idx]) % P for idx in range(ncols)]
        pivots.append(col)
        rank += 1
        if rank == len(matrix) or rank == ncols:
            break
    return matrix[:rank], pivots


def nullspace_basis(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> list[list[int]]:
    basis, pivots = rref(rows, ncols=ncols)
    pivot_set = set(pivots)
    free_cols = [col for col in range(ncols) if col not in pivot_set]
    result = []
    for free_col in free_cols:
        vector = [0] * ncols
        vector[free_col] = 1
        for basis_row, pivot in reversed(list(zip(basis, pivots, strict=True))):
            vector[pivot] = (-sum(basis_row[col] * vector[col] for col in free_cols)) % P
        result.append(vector)
    return result


def normalize_vector(vector: list[int]) -> list[int]:
    values = [int(value) % P for value in vector]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return [(entry * inv) % P for entry in values]
    return values


def dot(row: tuple[int, ...] | list[int], vector: tuple[int, ...] | list[int]) -> int:
    return sum(int(row[col]) * int(vector[col]) for col in range(TEMPLATE_DIM)) % P


def pair_projection_for_vector(candidate: dict[str, Any], profile: dict[str, Any], vector: list[int]) -> dict[str, Any]:
    if not vector:
        return {
            "forced_pair_count": None,
            "forced_pairs": None,
            "pair_projection_scalars": None,
        }
    scalars = zstable.zexp.pair_projection_scalars(candidate, profile, vector)
    forced = [label for label, value in scalars.items() if int(value) % P == 0]
    return {
        "forced_pair_count": len(forced),
        "forced_pairs": forced,
        "pair_projection_scalars": scalars,
    }


def span_projective_vectors(basis: list[list[int]]) -> list[list[int]]:
    if not basis:
        return []
    seen: set[tuple[int, ...]] = set()
    out: list[list[int]] = []
    for coeffs in itertools.product(range(P), repeat=len(basis)):
        if not any(coeffs):
            continue
        vector = [0] * TEMPLATE_DIM
        for scalar, basis_vector in zip(coeffs, basis, strict=True):
            if not scalar:
                continue
            for col, value in enumerate(basis_vector):
                vector[col] = (vector[col] + scalar * value) % P
        normalized = tuple(normalize_vector(vector))
        if normalized in seen:
            continue
        seen.add(normalized)
        out.append(list(normalized))
    return sorted(out)


def best_pair_projection_vector(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    basis: list[list[int]],
) -> dict[str, Any] | None:
    best = None
    for vector in span_projective_vectors(basis):
        pair_record = pair_projection_for_vector(candidate, profile, vector)
        key = (
            pair_record["forced_pair_count"] if pair_record["forced_pair_count"] is not None else 99,
            vector,
        )
        record = {
            "kernel_vector": vector,
            **pair_record,
        }
        if best is None or key < best[0]:
            best = (key, record)
        if pair_record["forced_pair_count"] == 0:
            return record
    return None if best is None else best[1]


def prescribed_kernel_record(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    row_removal_limit: int,
) -> dict[str, Any]:
    matrix_tuple = tuple(
        tuple(int(value) % P for value in row["basis_coordinates"]) for row in profile["nonbasis_constraint_detail"]
    )
    matrix = [list(row) for row in matrix_tuple]
    full_rank = rank_rows(matrix)
    indices = list(range(len(matrix)))
    best = None
    max_remove = min(len(matrix), row_removal_limit)
    for remove_count in range(0, max_remove + 1):
        removed_iter = [()] if remove_count == 0 else itertools.combinations(indices, remove_count)
        for removed in removed_iter:
            removed_set = set(removed)
            kept = [row for idx, row in enumerate(matrix) if idx not in removed_set]
            if rank_rows(kept) >= TEMPLATE_DIM:
                continue
            basis = nullspace_basis(kept)
            pair_best = best_pair_projection_vector(candidate, profile, basis)
            if pair_best is None:
                continue
            vector = pair_best["kernel_vector"]
            residual_indices = [idx for idx, row in enumerate(matrix_tuple) if dot(row, vector)]
            residual_classes = [
                int(profile["nonbasis_constraint_detail"][idx]["class_index"]) for idx in residual_indices
            ]
            record = {
                "coefficient_rank": full_rank,
                "min_rows_to_remove_for_kernel": remove_count,
                "removed_row_indices": list(removed),
                "kept_row_count": len(kept),
                "kernel_search_exhausted_to": remove_count,
                "residual_row_indices": residual_indices,
                "residual_row_classes": residual_classes,
                **pair_best,
            }
            key = (
                pair_best["forced_pair_count"] if pair_best["forced_pair_count"] is not None else 99,
                remove_count,
                len(residual_indices),
                list(removed),
                vector,
            )
            if best is None or key < best[0]:
                best = (key, record)
            if pair_best["forced_pair_count"] == 0:
                return record
        if best is not None and best[1]["forced_pair_count"] == 0:
            return best[1]
    if best is not None:
        return best[1]
    return {
        "coefficient_rank": full_rank,
        "min_rows_to_remove_for_kernel": None,
        "removed_row_indices": [],
        "kept_row_count": None,
        "kernel_search_exhausted_to": max_remove,
        "residual_row_indices": [],
        "residual_row_classes": [],
        "kernel_vector": [],
        "forced_pair_count": None,
        "forced_pairs": None,
        "pair_projection_scalars": None,
    }


def summarize_profile(
    candidate: dict[str, Any],
    classes: list[dict[str, Any]],
    profile: dict[str, Any],
    target_mode: str,
    row_removal_limit: int,
) -> dict[str, Any]:
    kernel = prescribed_kernel_record(candidate, profile, row_removal_limit)
    positions = zstable.class_position_sets(classes)
    union_size = zstable.profile_union_size(profile, positions)
    failure = "PNK_ACTUAL_PAIR_CLEAR_KERNEL"
    if kernel["min_rows_to_remove_for_kernel"] is None:
        failure = "PNK_REMOVE_LIMIT_FULL_RANK"
    elif kernel["min_rows_to_remove_for_kernel"] > 0 and kernel["forced_pair_count"] == 0:
        failure = "PNK_NEAR_PAIR_CLEAR_KERNEL"
    elif kernel["min_rows_to_remove_for_kernel"] == 0 and kernel["forced_pair_count"] and kernel["forced_pair_count"] > 0:
        failure = "PNK_ACTUAL_KERNEL_FORCED_PAIR"
    elif kernel["min_rows_to_remove_for_kernel"] > 0:
        failure = "PNK_NEAR_KERNEL_FORCED_PAIR"
    return {
        "basis_id": profile["basis_id"],
        "target_mode": target_mode,
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "q_variable_count": profile["q_variable_count"],
        "basis_zero_union_size": union_size,
        "stable_common_multiplier_dimension": K - union_size,
        "coefficient_matrix_shape": [len(profile["nonbasis_constraint_detail"]), TEMPLATE_DIM],
        **kernel,
        "best_failure_mode": failure,
    }


def previous_profile_front(previous: dict[str, Any]) -> dict[tuple[str, str], set[str]]:
    front: dict[tuple[str, str], set[str]] = {}
    for row in previous["nonbasis_row_dependency"]["candidate_summaries"]:
        profile_ids = set()
        best = row.get("best_profile")
        if best is not None:
            profile_ids.add(best["basis_id"])
        for profile in row.get("profile_summaries", []):
            if profile.get("min_rows_to_remove_for_kernel") is not None:
                profile_ids.add(profile["basis_id"])
        if profile_ids:
            front[(row["template_id"], row["coordinate_classes_hash"])] = profile_ids
    return front


def analyze_candidate(
    candidate: dict[str, Any],
    stable_basis_limit: int,
    row_removal_limit: int,
    allowed_profile_ids: set[str] | None,
) -> dict[str, Any]:
    row = codesign.zstable.candidate_structural_row(candidate)
    row["forced_basis_modes_tested"] = 0
    row["target_functional_present_modes"] = []
    row["target_functional_missing_modes"] = []
    row["forced_basis_combinations"] = 0
    row["forced_basis_profiles_tested"] = 0
    row["actual_kernel_profiles"] = 0
    row["near_kernel_profiles"] = 0
    row["actual_pair_clear_kernel_profiles"] = 0
    row["near_pair_clear_kernel_profiles"] = 0
    row["actual_kernel_forced_pair_profiles"] = 0
    row["near_kernel_forced_pair_profiles"] = 0
    row["pair_projection_clear_actual_kernels"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = codesign.zstable.mapped_structural_failure(row["structural_status"]).replace("ZSTABLE", "PNK")
        return row
    classes = functional.functional_classes(candidate)
    summaries = []
    for target_mode in codesign.basis_force.TARGET_MODES:
        stable_total, front, required = codesign.stable_forced_combos(classes, target_mode=target_mode, limit=stable_basis_limit)
        row["forced_basis_modes_tested"] += 1
        row["forced_basis_combinations"] += stable_total
        if not required:
            row["target_functional_missing_modes"].append(target_mode)
            continue
        row["target_functional_present_modes"].append(target_mode)
        for union_size, combo in front:
            profile = zstable.profile_from_combo(
                classes,
                combo,
                f"nbdep_{target_mode}_union_{union_size}_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
            )
            if profile is None:
                continue
            if allowed_profile_ids is not None and profile["basis_id"] not in allowed_profile_ids:
                continue
            row["forced_basis_profiles_tested"] += 1
            summaries.append(
                summarize_profile(
                    candidate,
                    classes,
                    profile,
                    target_mode=target_mode,
                    row_removal_limit=row_removal_limit,
                )
            )
    row["actual_kernel_profiles"] = sum(1 for item in summaries if item["min_rows_to_remove_for_kernel"] == 0)
    row["near_kernel_profiles"] = sum(
        1 for item in summaries if item["min_rows_to_remove_for_kernel"] is not None and item["min_rows_to_remove_for_kernel"] > 0
    )
    row["actual_pair_clear_kernel_profiles"] = sum(
        1 for item in summaries if item["best_failure_mode"] == "PNK_ACTUAL_PAIR_CLEAR_KERNEL"
    )
    row["near_pair_clear_kernel_profiles"] = sum(
        1 for item in summaries if item["best_failure_mode"] == "PNK_NEAR_PAIR_CLEAR_KERNEL"
    )
    row["actual_kernel_forced_pair_profiles"] = sum(
        1 for item in summaries if item["best_failure_mode"] == "PNK_ACTUAL_KERNEL_FORCED_PAIR"
    )
    row["near_kernel_forced_pair_profiles"] = sum(
        1 for item in summaries if item["best_failure_mode"] == "PNK_NEAR_KERNEL_FORCED_PAIR"
    )
    row["remove_limit_full_rank_profiles"] = sum(
        1 for item in summaries if item["best_failure_mode"] == "PNK_REMOVE_LIMIT_FULL_RANK"
    )
    row["pair_projection_clear_actual_kernels"] = sum(
        1 for item in summaries if item["min_rows_to_remove_for_kernel"] == 0 and item["forced_pair_count"] == 0
    )
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["min_rows_to_remove_for_kernel"] if item["min_rows_to_remove_for_kernel"] is not None else 99,
            item["forced_pair_count"] if item["forced_pair_count"] is not None else 99,
            len(item["residual_row_classes"]),
            item["coefficient_matrix_shape"][0],
            item["basis_zero_union_size"],
        ),
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["actual_pair_clear_kernel_profiles"]:
        row["best_failure_mode"] = "PNK_ACTUAL_PAIR_CLEAR_KERNEL"
    elif row["near_pair_clear_kernel_profiles"]:
        row["best_failure_mode"] = "PNK_NEAR_PAIR_CLEAR_KERNEL"
    elif row["actual_kernel_profiles"]:
        row["best_failure_mode"] = "PNK_ACTUAL_KERNEL_FORCED_PAIR"
    elif row["near_kernel_profiles"]:
        row["best_failure_mode"] = "PNK_NEAR_KERNEL_FORCED_PAIR"
    elif row["forced_basis_profiles_tested"]:
        row["best_failure_mode"] = "PNK_REMOVE_LIMIT_FULL_RANK"
    elif row["target_functional_present_modes"]:
        row["best_failure_mode"] = "PNK_NO_STABLE_TARGET_BASIS"
    elif row["target_functional_missing_modes"]:
        row["best_failure_mode"] = "PNK_TARGET_FUNCTIONAL_MISSING"
    else:
        row["best_failure_mode"] = "PNK_NO_TARGET_MODES"
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "template_family",
        "assignment_strategy",
        "assignment_seed",
        "support_vector",
        "pair7_counts",
        "max_pair_count",
        "selected_class_size_counts",
        "coordinate_classes_hash",
        "functional_classes",
        "functional_span_rank",
        "forced_functional_identities",
        "structural_status",
        "forced_basis_modes_tested",
        "target_functional_present_modes",
        "target_functional_missing_modes",
        "forced_basis_combinations",
        "forced_basis_profiles_tested",
        "actual_kernel_profiles",
        "near_kernel_profiles",
        "actual_pair_clear_kernel_profiles",
        "near_pair_clear_kernel_profiles",
        "actual_kernel_forced_pair_profiles",
        "near_kernel_forced_pair_profiles",
        "remove_limit_full_rank_profiles",
        "pair_projection_clear_actual_kernels",
        "effective_cost",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_record(max_specs: int, stable_basis_limit: int, row_removal_limit: int, profile_source: str) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    allowed_front = previous_profile_front(previous) if profile_source == "previous_summaries" else None
    _profiles, candidates = rankdefect.build_candidates(max_specs=max_specs)
    rows = [
        analyze_candidate(
            candidate,
            stable_basis_limit=stable_basis_limit,
            row_removal_limit=row_removal_limit,
            allowed_profile_ids=None
            if allowed_front is None
            else allowed_front.get((candidate["template_id"], candidate["coordinate_classes_hash"]), set()),
        )
        for candidate in candidates
    ]
    actual_pair_clear = [row for row in rows if row["actual_pair_clear_kernel_profiles"] > 0]
    near_pair_clear = [row for row in rows if row["near_pair_clear_kernel_profiles"] > 0]
    actual = [row for row in rows if row["actual_kernel_profiles"] > 0]
    near = [row for row in rows if row["near_kernel_profiles"] > 0]
    if actual_pair_clear:
        best = max(actual_pair_clear, key=lambda row: row["actual_pair_clear_kernel_profiles"])
        proof_status = "CANDIDATE / PNK_ACTUAL_PAIR_CLEAR_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "PNK_ACTUAL_PAIR_CLEAR_KERNEL"
    elif near_pair_clear:
        best = min(
            near_pair_clear,
            key=lambda row: (
                row["best_profile"]["min_rows_to_remove_for_kernel"] if row["best_profile"] else 99,
                len(row["best_profile"]["residual_row_classes"]) if row["best_profile"] else 99,
                row["template_id"],
            ),
        )
        proof_status = "CANDIDATE / PNK_NEAR_PAIR_CLEAR_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "PNK_NEAR_PAIR_CLEAR_KERNEL"
    elif actual:
        best = max(actual, key=lambda row: row["actual_kernel_profiles"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / PNK_ACTUAL_KERNEL_FORCED_PAIR / PARTIAL / EXPERIMENTAL"
        failure = "PNK_ACTUAL_KERNEL_FORCED_PAIR"
    elif near:
        best = min(
            near,
            key=lambda row: (
                row["best_profile"]["min_rows_to_remove_for_kernel"] if row["best_profile"] else 99,
                row["best_profile"]["forced_pair_count"] if row["best_profile"] else 99,
                row["template_id"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / PNK_NEAR_KERNEL_FORCED_PAIR / PARTIAL / EXPERIMENTAL"
        failure = "PNK_NEAR_KERNEL_FORCED_PAIR"
    elif any(row["forced_basis_profiles_tested"] for row in rows):
        best = max(rows, key=lambda row: (row["forced_basis_profiles_tested"], row["functional_span_rank"], row["template_id"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / PNK_REMOVE_LIMIT_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "PNK_REMOVE_LIMIT_FULL_RANK"
    elif rows:
        best = max(rows, key=lambda row: (row["forced_basis_profiles_tested"], row["functional_span_rank"], row["template_id"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / PNK_TARGET_FUNCTIONAL_MISSING / PARTIAL / EXPERIMENTAL"
        failure = "PNK_TARGET_FUNCTIONAL_MISSING"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / PNK_NO_CANDIDATES / PARTIAL / EXPERIMENTAL"
        failure = "PNK_NO_CANDIDATES"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_nonbasis_row_dependency": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "systems_tested": previous["nonbasis_row_dependency"]["systems_tested"],
            "near_kernel_profiles": previous["nonbasis_row_dependency"]["near_kernel_profiles"],
            "pair_projection_clear_actual_kernels": previous["nonbasis_row_dependency"]["pair_projection_clear_actual_kernels"],
            "best_failure_mode": previous["nonbasis_row_dependency"]["best_failure_mode"],
        },
        "prescribed_nonbasis_kernel": {
            "templates_generated": max_specs,
            "systems_tested": len(rows),
            "profile_source": profile_source,
            "previous_front_templates": None if allowed_front is None else len(allowed_front),
            "previous_front_profiles": None if allowed_front is None else sum(len(value) for value in allowed_front.values()),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "target_present_candidates": sum(1 for row in rows if row["target_functional_present_modes"]),
            "forced_basis_combinations": sum(row["forced_basis_combinations"] for row in rows),
            "forced_basis_profiles_tested": sum(row["forced_basis_profiles_tested"] for row in rows),
            "row_removal_limit": row_removal_limit,
            "actual_kernel_profiles": sum(row["actual_kernel_profiles"] for row in rows),
            "near_kernel_profiles": sum(row["near_kernel_profiles"] for row in rows),
            "actual_pair_clear_kernel_profiles": sum(row["actual_pair_clear_kernel_profiles"] for row in rows),
            "near_pair_clear_kernel_profiles": sum(row["near_pair_clear_kernel_profiles"] for row in rows),
            "actual_kernel_forced_pair_profiles": sum(row["actual_kernel_forced_pair_profiles"] for row in rows),
            "near_kernel_forced_pair_profiles": sum(row["near_kernel_forced_pair_profiles"] for row in rows),
            "remove_limit_full_rank_profiles": sum(row["remove_limit_full_rank_profiles"] for row in rows),
            "pair_projection_clear_actual_kernels": sum(row["pair_projection_clear_actual_kernels"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_target_mode": None if best is None or best["best_profile"] is None else best["best_profile"]["target_mode"],
            "best_min_rows_to_remove": None if best is None or best["best_profile"] is None else best["best_profile"]["min_rows_to_remove_for_kernel"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["forced_pair_count"],
            "best_kernel_vector": None if best is None or best["best_profile"] is None else best["best_profile"]["kernel_vector"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "ACTUAL_TEMPLATE_ROWSPACES_ONLY",
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
            "synthetic rowspace edits",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-specs", type=int, default=64)
    parser.add_argument("--stable-basis-limit", type=int, default=96)
    parser.add_argument("--row-removal-limit", type=int, default=DEFAULT_ROW_REMOVAL_LIMIT)
    parser.add_argument("--profile-source", choices=["previous_summaries", "full"], default="previous_summaries")
    args = parser.parse_args()
    record = build_record(
        max_specs=args.max_specs,
        stable_basis_limit=args.stable_basis_limit,
        row_removal_limit=args.row_removal_limit,
        profile_source=args.profile_source,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["prescribed_nonbasis_kernel"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "profile_source": search["profile_source"],
                    "previous_front_profiles": search["previous_front_profiles"],
                    "target_present_candidates": search["target_present_candidates"],
                    "forced_basis_profiles_tested": search["forced_basis_profiles_tested"],
                    "row_removal_limit": search["row_removal_limit"],
                    "actual_kernel_profiles": search["actual_kernel_profiles"],
                    "near_kernel_profiles": search["near_kernel_profiles"],
                    "actual_pair_clear_kernel_profiles": search["actual_pair_clear_kernel_profiles"],
                    "near_pair_clear_kernel_profiles": search["near_pair_clear_kernel_profiles"],
                    "remove_limit_full_rank_profiles": search["remove_limit_full_rank_profiles"],
                    "pair_projection_clear_actual_kernels": search["pair_projection_clear_actual_kernels"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_target_mode": search["best_target_mode"],
                    "best_min_rows_to_remove": search["best_min_rows_to_remove"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_kernel_vector": search["best_kernel_vector"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PRESCRIBED_NONBASIS_KERNEL_GENERATOR_READY")


if __name__ == "__main__":
    main()
