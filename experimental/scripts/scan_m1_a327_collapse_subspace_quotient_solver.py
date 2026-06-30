#!/usr/bin/env python3
"""Collapse-subspace quotient diagnostics for M1 a=327 proxy systems."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_soft_collapse_penalty_target_solver as soft


SOURCE_DATA = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_collapse_subspace_quotient_solver.json")

N = joint.N
K = joint.K
LIST_SIZE = joint.LIST_SIZE
VARIABLE_COUNT = joint.VARIABLE_COUNT
TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "f266cf1"
COLLAPSE_CLASS_ONE_BASED = [1, 3, 4, 5, 6, 7]

SYSTEM_LIMIT = 6
QUOTIENT_DIRECTIONS_PER_BLOCK = 3
RANDOM_QUOTIENT_DIRECTIONS = 12
SCALARS = [1, 2, 5, 17]


def jsonable(payload: Any) -> Any:
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def echelon_modp(matrix: np.ndarray, p: int) -> tuple[np.ndarray, list[int]]:
    mat = np.array(matrix, dtype=np.int64, copy=True) % p
    row_count, col_count = mat.shape
    rank = 0
    pivots: list[int] = []
    for col in range(col_count):
        pivot_candidates = np.nonzero(mat[rank:, col] % p)[0]
        if len(pivot_candidates) == 0:
            continue
        pivot = rank + int(pivot_candidates[0])
        if pivot != rank:
            mat[[rank, pivot]] = mat[[pivot, rank]]
        inv = pow(int(mat[rank, col]), p - 2, p)
        mat[rank] = (mat[rank] * inv) % p
        below = np.nonzero(mat[rank + 1:, col] % p)[0]
        for offset in below:
            row = rank + 1 + int(offset)
            factor = int(mat[row, col])
            mat[row] = (mat[row] - factor * mat[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == row_count:
            break
    return mat[:rank], pivots


def rank_modp(matrix: np.ndarray, p: int) -> int:
    if matrix.size == 0:
        return 0
    _echelon, pivots = echelon_modp(matrix, p)
    return len(pivots)


def nullspace_basis_matrix(echelon: np.ndarray, pivots: list[int], col_count: int, p: int) -> tuple[np.ndarray, list[int]]:
    pivot_set = set(pivots)
    free_cols = [col for col in range(col_count) if col not in pivot_set]
    if not free_cols:
        return np.zeros((0, col_count), dtype=np.int64), free_cols
    basis_cols = np.zeros((col_count, len(free_cols)), dtype=np.int64)
    basis_cols[np.array(free_cols), np.arange(len(free_cols))] = 1
    for row_idx in range(len(pivots) - 1, -1, -1):
        pivot = pivots[row_idx]
        total = np.dot(echelon[row_idx], basis_cols) % p
        basis_cols[pivot, :] = (-total) % p
    return basis_cols.T % p, free_cols


def selected_soft_rows(source: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    return soft.select_coordinates_soft(
        balanced.candidate_coordinates(source["membership_masks"]),
        int(row["row_budget"]),
        row["selection_objective"],
        float(row["lambda_collapse_penalty"]),
    )


def retained_unique_systems(source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        row for row in source["retained_results"]
        if row["proxy_candidate_count"] > 0
        and row["best"]["assignment"] is not None
        and row["best"]["assignment"]["exact_max_min"] >= TARGET_AGREEMENT
    ]
    rows.sort(
        key=lambda row: (
            row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance"],
            row["target_system_id"],
        ),
        reverse=True,
    )
    unique = []
    seen = set()
    for row in rows:
        if row["target_rows_hash"] in seen:
            continue
        seen.add(row["target_rows_hash"])
        unique.append(row)
        if len(unique) >= SYSTEM_LIMIT:
            break
    return unique


def source_for_row(row: dict[str, Any]) -> dict[str, Any]:
    seed = {"system_id": row["seed_system_id"]}
    return soft.source_for_seed(seed)


def collapse_basis_for_rows(rows: np.ndarray) -> tuple[np.ndarray, int]:
    restricted = rows[:, :K] % PROXY_PRIME
    echelon, pivots = echelon_modp(restricted, PROXY_PRIME)
    small_basis, _free_cols = nullspace_basis_matrix(echelon, pivots, K, PROXY_PRIME)
    full_basis = np.zeros((small_basis.shape[0], VARIABLE_COUNT), dtype=np.int64)
    full_basis[:, :K] = small_basis
    return full_basis, small_basis.shape[0]


def projection_rank_by_block(null_basis: np.ndarray) -> dict[str, int]:
    ranks = {}
    for block in range(LIST_SIZE - 1):
        start = block * K
        ranks[f"D_{block + 2}"] = rank_modp(null_basis[:, start:start + K], PROXY_PRIME)
    return ranks


def quotient_direction_indices(free_cols: list[int], null_basis: np.ndarray) -> list[int]:
    by_block: dict[int, list[int]] = {block: [] for block in range(1, LIST_SIZE - 1)}
    for idx, col in enumerate(free_cols):
        block = col // K
        if block >= 1:
            by_block.setdefault(block, []).append(idx)
    selected = []
    for block in range(1, LIST_SIZE - 1):
        selected.extend(by_block.get(block, [])[:QUOTIENT_DIRECTIONS_PER_BLOCK])
    rng = random.Random(20260629)
    quotient_indices = [
        idx for idx, vector in enumerate(null_basis)
        if np.any(vector[K:] % PROXY_PRIME)
    ]
    remaining = [idx for idx in quotient_indices if idx not in selected]
    if remaining:
        selected.extend(rng.sample(remaining, min(RANDOM_QUOTIENT_DIRECTIONS, len(remaining))))
    return selected


def evaluate_vector(vector: np.ndarray, powers: np.ndarray, family: str, detail: str) -> dict[str, Any]:
    values = joint.evaluate_vector(powers, vector % PROXY_PRIME)
    capacity = joint.value_class_capacity(values)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = joint.exact_assignment_max_min(values)
    six_dom = soft.six_class_dominance(values)
    in_collapse = not np.any(vector[K:] % PROXY_PRIME)
    if in_collapse and capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        failure_mode = "COLLAPSE_ONLY_HIGH_CAPACITY"
    elif capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        failure_mode = "QUOTIENT_DIRECTION_CAPACITY_LOSS"
    elif assignment is None or assignment["exact_max_min"] < TARGET_AGREEMENT:
        failure_mode = "QUOTIENT_DIRECTION_LOW_RESCHEDULE"
    elif six_dom > 0:
        failure_mode = "QUOTIENT_DIRECTION_HIGH_CAPACITY_DEGENERATE"
    else:
        failure_mode = "PROXY_A327_COLLAPSE_REDUCED"
    return {
        "sample_family": family,
        "sample_detail": detail,
        "vector_hash": hash_payload(vector.tolist()),
        "in_collapse_subspace": in_collapse,
        **capacity,
        "assignment": assignment,
        "six_class_dominance": six_dom,
        "failure_mode": failure_mode,
    }


def sample_tradeoff(null_basis: np.ndarray, free_cols: list[int], collapse_basis: np.ndarray, powers: np.ndarray) -> list[dict[str, Any]]:
    samples: list[tuple[str, str, np.ndarray]] = []
    if collapse_basis.shape[0]:
        collapse_seed = np.zeros(VARIABLE_COUNT, dtype=np.int64)
        for idx, vector in enumerate(collapse_basis[: min(16, collapse_basis.shape[0])]):
            collapse_seed = (collapse_seed + (idx + 1) * vector) % PROXY_PRIME
        samples.append(("collapse_only", "weighted_first_16", collapse_seed))
        for idx, vector in enumerate(collapse_basis[:4]):
            samples.append(("collapse_only", f"basis_{idx}", vector))
    else:
        collapse_seed = np.zeros(VARIABLE_COUNT, dtype=np.int64)

    q_indices = quotient_direction_indices(free_cols, null_basis)
    for idx in q_indices[:20]:
        q = null_basis[idx]
        samples.append(("quotient_only", f"basis_{idx}", q))
        for scalar in SCALARS:
            samples.append(("collapse_plus_one_quotient", f"basis_{idx}_scalar_{scalar}", collapse_seed + scalar * q))

    for offset in range(0, min(len(q_indices), 20), 2):
        if offset + 1 >= len(q_indices):
            break
        q1 = null_basis[q_indices[offset]]
        q2 = null_basis[q_indices[offset + 1]]
        samples.append(("collapse_plus_two_quotients", f"basis_{q_indices[offset]}_{q_indices[offset + 1]}", collapse_seed + q1 + 2 * q2))

    by_block: dict[int, np.ndarray] = {}
    for idx in q_indices:
        block = free_cols[idx] // K if idx < len(free_cols) else -1
        if block >= 1 and block not in by_block:
            by_block[block] = null_basis[idx]
    if len(by_block) >= 5:
        balanced_vector = collapse_seed.copy()
        for coeff, block in enumerate(sorted(by_block), start=1):
            balanced_vector = (balanced_vector + coeff * by_block[block]) % PROXY_PRIME
        samples.append(("balanced_quotient_blocks", "one_direction_per_noncollapse_block", balanced_vector))

    seen = set()
    output = []
    for family, detail, vector in samples:
        vector = vector % PROXY_PRIME
        digest = hash_payload(vector.tolist())
        if digest in seen or not np.any(vector):
            continue
        seen.add(digest)
        output.append(evaluate_vector(vector, powers, family, detail))
    return output


def analyze_system(row: dict[str, Any], powers: np.ndarray) -> dict[str, Any]:
    source = source_for_row(row)
    selection = selected_soft_rows(source, row)
    rows = balanced.rows_for_selected(powers, selection["selected"])
    echelon, pivots = echelon_modp(rows, PROXY_PRIME)
    null_basis, free_cols = nullspace_basis_matrix(echelon, pivots, VARIABLE_COUNT, PROXY_PRIME)
    collapse_basis, collapse_dim = collapse_basis_for_rows(rows)
    samples = sample_tradeoff(null_basis, free_cols, collapse_basis, powers)
    best = max(
        samples,
        key=lambda sample: (
            -1 if sample["assignment"] is None else sample["assignment"]["exact_max_min"],
            sample["capacity_upper_bound"],
            -sample["six_class_dominance"],
            sample["capacity_total"],
        ),
    )
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    quotient_dim = (VARIABLE_COUNT - len(pivots)) - collapse_dim
    return {
        "system_id": row["target_system_id"],
        "parent_best_proxy_max_min": row["best"]["assignment"]["exact_max_min"],
        "parent_best_capacity_upper_bound": row["best"]["capacity_upper_bound"],
        "parent_six_class_dominance": row["best"]["six_class_dominance"],
        "target_rows_hash": row["target_rows_hash"],
        "row_budget": row["row_budget"],
        "lambda_collapse_penalty": row["lambda_collapse_penalty"],
        "selection_objective": row["selection_objective"],
        "proxy_rank": len(pivots),
        "proxy_nullity": VARIABLE_COUNT - len(pivots),
        "collapse_subspace_dimension": collapse_dim,
        "quotient_dimension": quotient_dim,
        "projection_rank_by_block": projection_rank_by_block(null_basis),
        "free_column_count": len(free_cols),
        "quotient_direction_count": sum(1 for vector in null_basis if np.any(vector[K:] % PROXY_PRIME)),
        "samples_tested": len(samples),
        "best": best,
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "sample_results": sorted(
            samples,
            key=lambda sample: (
                -1 if sample["assignment"] is None else sample["assignment"]["exact_max_min"],
                sample["capacity_upper_bound"],
                -sample["six_class_dominance"],
            ),
            reverse=True,
        )[:24],
    }


def build_record() -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    systems = retained_unique_systems(source)
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    analyses = [analyze_system(row, powers) for row in systems]
    best = max(
        analyses,
        key=lambda row: (
            -1 if row["best"]["assignment"] is None else row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance"],
        ),
    )
    failure_counts: dict[str, int] = {}
    for row in analyses:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    proxy_candidates = [
        row for row in analyses
        if row["best"]["failure_mode"] == "PROXY_A327_COLLAPSE_REDUCED"
    ]
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_QUOTIENT_DIRECTIONS_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "collapse_class": COLLAPSE_CLASS_ONE_BASED,
        "construction_mode": "collapse_subspace_quotient_solver",
        "proxy_systems": {
            "systems_tested": len(analyses),
            "best_parent_proxy_max_min": source["soft_collapse_search"]["best_proxy_max_min"],
            "best_parent_capacity": source["soft_collapse_search"]["best_capacity_upper_bound"],
        },
        "collapse_quotient": {
            "collapse_subspace_dimensions": [row["collapse_subspace_dimension"] for row in analyses],
            "quotient_dimensions": [row["quotient_dimension"] for row in analyses],
            "projection_rank_by_block": best["projection_rank_by_block"],
            "samples_tested": sum(row["samples_tested"] for row in analyses),
            "best_capacity_upper_bound": best["best"]["capacity_upper_bound"],
            "best_proxy_max_min": None if best["best"]["assignment"] is None else best["best"]["assignment"]["exact_max_min"],
            "best_six_class_dominance": best["best"]["six_class_dominance"],
            "best_failure_mode": best["best"]["failure_mode"],
            "failure_mode_counts": dict(sorted(failure_counts.items())),
        },
        "systems": analyses,
        "best": best,
        "exact_lift": {
            "triggered": bool(proxy_candidates),
            "exact_vectors_constructed": 0,
            "best_exact_max_min": None,
        },
        "result_hash": hash_payload(analyses),
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "GF(17^32) proof record",
            "improvement over PR #133",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
