#!/usr/bin/env python3
"""Prepare the M1 a=327 low-rank functional-basis extraction ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "edf8a8c"
SOURCE_DATA = Path("experimental/data/m1_a327_lowrank_template_functional_divisibility_lift.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_lowrank_functional_basis_extraction.json")

P = 17
K = 256
TARGET_AGREEMENT = 327
TEMPLATE_DIM = 6


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def normalize_projective(row: list[int], prime: int = P) -> tuple[int, ...]:
    reduced = [value % prime for value in row]
    for value in reduced:
        if value:
            inv = pow(value, -1, prime)
            return tuple((entry * inv) % prime for entry in reduced)
    raise ValueError("zero row has no projective normalization")


def rref(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> tuple[list[list[int]], list[int]]:
    matrix = [[value % prime for value in row] for row in rows if any(value % prime for value in row)]
    pivots: list[int] = []
    rank = 0
    for col in range(ncols):
        pivot = None
        for row in range(rank, len(matrix)):
            if matrix[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][col] % prime:
                continue
            factor = matrix[row][col] % prime
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(matrix):
            break
    return matrix[:rank], pivots


def reduce_mod_span(row: list[int], basis: list[list[int]], pivots: list[int], prime: int = P) -> tuple[int, ...]:
    reduced = [value % prime for value in row]
    for basis_row, pivot in zip(basis, pivots, strict=True):
        factor = reduced[pivot] % prime
        if not factor:
            continue
        reduced = [(reduced[idx] - factor * basis_row[idx]) % prime for idx in range(len(reduced))]
    return tuple(reduced)


def rank_mod_p(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> int:
    return len(rref(rows, ncols=ncols, prime=prime)[0])


def nullspace_basis(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> list[list[int]]:
    basis, pivots = rref(rows, ncols=ncols, prime=prime)
    pivot_set = set(pivots)
    free_cols = [col for col in range(ncols) if col not in pivot_set]
    result = []
    for free_col in free_cols:
        vector = [0] * ncols
        vector[free_col] = 1
        for basis_row, pivot in reversed(list(zip(basis, pivots, strict=True))):
            acc = 0
            for col in free_cols:
                acc = (acc + basis_row[col] * vector[col]) % prime
            vector[pivot] = (-acc) % prime
        result.append(vector)
    return result


def independent_subset(rows: list[list[int]], target_rank: int, prefer_large_support: list[int]) -> list[int]:
    order = sorted(range(len(rows)), key=lambda idx: (-prefer_large_support[idx], rows[idx]))
    selected: list[int] = []
    selected_rows: list[list[int]] = []
    current_rank = 0
    for idx in order:
        trial_rank = rank_mod_p(selected_rows + [rows[idx]])
        if trial_rank > current_rank:
            selected.append(idx)
            selected_rows.append(rows[idx])
            current_rank = trial_rank
        if current_rank == target_rank:
            break
    return selected


def solve_coordinates(row: list[int], basis_rows: list[list[int]], prime: int = P) -> list[int] | None:
    d = len(basis_rows)
    if d == 0:
        return [] if not any(value % prime for value in row) else None
    # Solve B^T c = row^T by row reduction on an augmented system.
    matrix = []
    for col in range(TEMPLATE_DIM):
        matrix.append([basis_rows[idx][col] % prime for idx in range(d)] + [row[col] % prime])
    rank = 0
    pivots: list[int] = []
    for col in range(d):
        pivot = None
        for r in range(rank, len(matrix)):
            if matrix[r][col] % prime:
                pivot = r
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for r in range(len(matrix)):
            if r == rank or not matrix[r][col] % prime:
                continue
            factor = matrix[r][col] % prime
            matrix[r] = [
                (matrix[r][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(d + 1)
            ]
        pivots.append(col)
        rank += 1
    for r in range(rank, len(matrix)):
        if all(matrix[r][col] % prime == 0 for col in range(d)) and matrix[r][d] % prime:
            return None
    solution = [0] * d
    for r, pivot in enumerate(pivots):
        solution[pivot] = matrix[r][d] % prime
    return solution


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def saturate_forced_identities(source: dict[str, Any]) -> dict[str, Any]:
    original_classes = source["functional_classes_detail"]
    forced_rows = [row["functional"] for row in original_classes if row["forced_identity"]]
    changed = True
    iterations = []
    while changed:
        changed = False
        basis, pivots = rref(forced_rows)
        projected: dict[tuple[int, ...], set[int]] = defaultdict(set)
        zero_projected = 0
        for row in original_classes:
            remainder = reduce_mod_span(row["functional"], basis, pivots)
            if not any(remainder):
                zero_projected += 1
                continue
            key = normalize_projective(list(remainder))
            projected[key].update(int(pos) for pos in row["positions"])
        new_forced = []
        for key, positions in projected.items():
            if len(positions) > K - 1:
                new_forced.append(list(key))
        current_rank = len(basis)
        for row in new_forced:
            trial_rank = rank_mod_p(forced_rows + [row])
            if trial_rank > current_rank:
                forced_rows.append(row)
                current_rank = trial_rank
                changed = True
        iterations.append(
            {
                "forced_rank": len(rref(forced_rows)[0]),
                "projected_classes": len(projected),
                "zero_projected_functionals": zero_projected,
                "new_forced_candidates": len(new_forced),
            }
        )
    basis, pivots = rref(forced_rows)
    projected_classes = []
    projected: dict[tuple[int, ...], set[int]] = defaultdict(set)
    source_indices: dict[tuple[int, ...], list[int]] = defaultdict(list)
    zero_projected = 0
    for row in original_classes:
        remainder = reduce_mod_span(row["functional"], basis, pivots)
        if not any(remainder):
            zero_projected += 1
            continue
        key = normalize_projective(list(remainder))
        projected[key].update(int(pos) for pos in row["positions"])
        source_indices[key].append(int(row["class_index"]))
    for idx, (functional, positions_set) in enumerate(
        sorted(projected.items(), key=lambda item: (-len(item[1]), item[0]))
    ):
        positions = sorted(positions_set)
        projected_classes.append(
            {
                "class_index": idx,
                "functional": list(functional),
                "support_size": len(positions),
                "quotient_variables": max(0, K - len(positions)),
                "positions": positions,
                "positions_hash": hash_payload(positions),
                "source_functional_indices": sorted(source_indices[functional]),
            }
        )
    return {
        "forced_rows": [list(row) for row in basis],
        "forced_pivots": pivots,
        "forced_rank": len(basis),
        "reduced_template_dimension": TEMPLATE_DIM - len(basis),
        "projected_classes": projected_classes,
        "zero_projected_functionals": zero_projected,
        "iterations": iterations,
    }


def basis_profiles(reduction: dict[str, Any]) -> list[dict[str, Any]]:
    classes = reduction["projected_classes"]
    d = reduction["reduced_template_dimension"]
    rows = [row["functional"] for row in classes]
    supports = [row["support_size"] for row in classes]
    profiles = []
    if d <= 0:
        return profiles
    strategies = {
        "max_support_basis": independent_subset(rows, d, supports),
        "min_q_basis": independent_subset(rows, d, supports),
    }
    # Deterministic alternatives over small combinations when feasible.
    if len(classes) <= 16:
        best = None
        best_score = None
        for combo in combinations(range(len(classes)), d):
            combo_rows = [rows[idx] for idx in combo]
            if rank_mod_p(combo_rows) != d:
                continue
            score = sum(K - supports[idx] for idx in combo)
            if best_score is None or score < best_score:
                best_score = score
                best = list(combo)
        if best is not None:
            strategies["best_exhaustive_min_q_basis"] = best
    seen = set()
    for basis_id, indices in strategies.items():
        key = tuple(indices)
        if not indices or key in seen:
            continue
        seen.add(key)
        basis_rows = [rows[idx] for idx in indices]
        if rank_mod_p(basis_rows) != d:
            continue
        basis_supports = [supports[idx] for idx in indices]
        q_variable_count = sum(K - support for support in basis_supports)
        nonbasis_rows = 0
        nonbasis_constraints = []
        for idx, row in enumerate(rows):
            if idx in indices:
                continue
            coords = solve_coordinates(row, basis_rows)
            if coords is None:
                continue
            constraints = supports[idx]
            nonbasis_rows += constraints
            nonbasis_constraints.append(
                {
                    "class_index": int(classes[idx]["class_index"]),
                    "support_size": int(supports[idx]),
                    "basis_coordinates": coords,
                }
            )
        profiles.append(
            {
                "basis_id": basis_id,
                "basis_class_indices": [int(classes[idx]["class_index"]) for idx in indices],
                "basis_functionals": [classes[idx]["functional"] for idx in indices],
                "basis_support_sizes": basis_supports,
                "q_variable_count": q_variable_count,
                "nonbasis_constraints": len(nonbasis_constraints),
                "matrix_shape": [nonbasis_rows, q_variable_count],
                "formal_nullity_lower_bound": max(0, q_variable_count - nonbasis_rows),
                "nonbasis_constraint_detail": nonbasis_constraints,
            }
        )
    return profiles


def forced_pair_projection(template_vectors: list[list[int]], forced_rows: list[list[int]]) -> dict[str, Any]:
    w_basis = nullspace_basis(forced_rows)
    ranks = {}
    forced_pairs = []
    for left in range(1, 8):
        for right in range(left + 1, 8):
            diff = [
                (int(template_vectors[left - 1][idx]) - int(template_vectors[right - 1][idx])) % P
                for idx in range(TEMPLATE_DIM)
            ]
            values = [
                sum(diff[idx] * basis_vec[idx] for idx in range(TEMPLATE_DIM)) % P
                for basis_vec in w_basis
            ]
            rank = 1 if any(values) else 0
            label = f"P{left}{right}"
            ranks[label] = rank
            if rank == 0:
                forced_pairs.append([left, right])
    return {
        "kernel_basis": w_basis,
        "projection_rank_by_pair": ranks,
        "forced_equal_pairs": forced_pairs,
        "min_projection_rank": min(ranks.values()) if ranks else None,
    }


def build_record(mark_timeout: bool = False) -> dict[str, Any]:
    source = load_source()
    proxy = source["proxy_candidate"]
    reduction = saturate_forced_identities(source)
    profiles = basis_profiles(reduction)
    forced_projection = forced_pair_projection(proxy["template_vectors"], reduction["forced_rows"])
    best = None
    if profiles:
        best = max(
            profiles,
            key=lambda row: (
                row["formal_nullity_lower_bound"],
                -row["q_variable_count"],
                -row["matrix_shape"][0],
            ),
        )
    proof_status = "CANDIDATE / FUNC_BASIS_METADATA / PARTIAL / EXPERIMENTAL"
    failure = None
    if reduction["reduced_template_dimension"] <= 0:
        proof_status = "EXACT_EXTRACTION_NO_A327 / FUNC_BASIS_FORCED_SPAN_COLLAPSES / PARTIAL / EXPERIMENTAL"
        failure = "FUNC_BASIS_FORCED_SPAN_COLLAPSES"
    elif forced_projection["forced_equal_pairs"]:
        proof_status = "EXACT_EXTRACTION_NO_A327 / FUNC_BASIS_PAIR_FORCED_BY_FORCED_IDENTITIES / PARTIAL / EXPERIMENTAL"
        failure = "FUNC_BASIS_PAIR_FORCED_BY_FORCED_IDENTITIES"
    elif not profiles:
        proof_status = "EXACT_EXTRACTION_NO_A327 / FUNC_BASIS_NO_INDEPENDENT_BASIS / PARTIAL / EXPERIMENTAL"
        failure = "FUNC_BASIS_NO_INDEPENDENT_BASIS"
    if mark_timeout:
        proof_status = "CANDIDATE / FUNC_BASIS_MATRIX_TIMEOUT / PARTIAL / EXPERIMENTAL"
        failure = "FUNC_BASIS_MATRIX_TIMEOUT"
    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "functional_divisibility_baseline": {
            "template_id": proxy["template_id"],
            "template_dimension": proxy["template_dimension"],
            "template_vectors": source["proxy_candidate"]["template_vectors"],
            "functional_classes": source["functional_divisibility"]["functional_classes"],
            "forced_functional_identities": source["functional_divisibility"]["forced_functional_identities"],
            "quotient_variables": source["functional_divisibility"]["quotient_variable_count"],
            "matrix_shape": source["functional_divisibility"]["matrix_shape"],
            "formal_nullity_lower_bound": source["functional_divisibility"]["formal_nullity_lower_bound"],
        },
        "coordinate_classes": source["coordinate_classes"],
        "row_specs": source["row_specs"],
        "forced_identity_reduction": {
            "forced_rank": reduction["forced_rank"],
            "forced_functionals": reduction["forced_rows"],
            "forced_pivots": reduction["forced_pivots"],
            "forced_kernel_basis": forced_projection["kernel_basis"],
            "reduced_template_dimension": reduction["reduced_template_dimension"],
            "remaining_functional_classes": len(reduction["projected_classes"]),
            "zero_projected_functionals": reduction["zero_projected_functionals"],
            "pure_q_kernel_impossible": True,
            "saturation_iterations": reduction["iterations"],
        },
        "projected_functional_classes": reduction["projected_classes"],
        "basis_profiles": profiles,
        "basis_quotient_system": {
            "bases_tested": len(profiles),
            "best_basis_id": None if best is None else best["basis_id"],
            "best_basis_support_sizes": None if best is None else best["basis_support_sizes"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_matrix_shape": None if best is None else best["matrix_shape"],
            "best_rank": None,
            "best_nullity": None,
            "best_failure_mode": failure,
        },
        "pair_projection_test": {
            "pairs_tested": 21,
            "forced_equal_pairs": forced_projection["forced_equal_pairs"],
            "min_projection_rank": forced_projection["min_projection_rank"],
            "projection_rank_by_pair": forced_projection["projection_rank_by_pair"],
        },
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "sage_exact_check": {
            "run": False,
            "field": "GF(17^32)",
            "forced_rank": None,
            "forced_kernel_dimension": None,
            "forced_equal_pairs": None,
            "status": "NOT_RUN",
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
        ],
        "ledger_hashes": {
            "projected_functional_classes_hash": hash_payload(reduction["projected_classes"]),
            "basis_profiles_hash": hash_payload(profiles),
            "coordinate_classes_hash": hash_payload(source["coordinate_classes"]),
            "row_specs_hash": hash_payload(source["row_specs"]),
        },
    }
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--mark-timeout", action="store_true")
    args = parser.parse_args()
    record = build_record(mark_timeout=args.mark_timeout)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        red = record["forced_identity_reduction"]
        basis = record["basis_quotient_system"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "forced_rank": red["forced_rank"],
                    "reduced_template_dimension": red["reduced_template_dimension"],
                    "remaining_functional_classes": red["remaining_functional_classes"],
                    "zero_projected_functionals": red["zero_projected_functionals"],
                    "pure_q_kernel_impossible": red["pure_q_kernel_impossible"],
                    "bases_tested": basis["bases_tested"],
                    "best_basis_id": basis["best_basis_id"],
                    "best_q_variable_count": basis["best_q_variable_count"],
                    "best_matrix_shape": basis["best_matrix_shape"],
                    "best_failure_mode": basis["best_failure_mode"],
                    "forced_equal_pairs": record["pair_projection_test"]["forced_equal_pairs"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LOWRANK_FUNCTIONAL_BASIS_EXTRACTION_READY")


if __name__ == "__main__":
    main()
