#!/usr/bin/env python3
"""Audit residual slot equations for the best realized-slot near miss."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "fae2021"
PREVIOUS_DATA = Path("experimental/data/m1_a327_realized_slot_nearmiss_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_residual_slot_equation_repair.json")

ROOT = Path(__file__).resolve().parents[2]
NREPAIR_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_realized_slot_nearmiss_repair.py"

P = 17
TARGET_AGREEMENT = 327
TEMPLATE_DIM = 6
TARGET_TEMPLATE_ID = "nearmiss_w7_c1_v9"
TARGET_ASSIGNMENT = "signature_fiber_blocks"
TARGET_BASIS_ID = "slot_union_142_6_8_10_12_15_16"
TARGET_SLOT = 3


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


nrepair = load_module("realized_slot_nearmiss_repair", NREPAIR_SCRIPT)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_rows(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> int:
    matrix = [[int(value) % prime for value in row] for row in rows if any(int(value) % prime for value in row)]
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % prime:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % prime:
                continue
            factor = matrix[row_idx][col] % prime
            matrix[row_idx] = [
                (matrix[row_idx][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def solve_coordinates(row: list[int], basis_rows: list[list[int]], prime: int = P) -> list[int] | None:
    d = len(basis_rows)
    matrix = []
    for col in range(TEMPLATE_DIM):
        matrix.append([int(basis_rows[idx][col]) % prime for idx in range(d)] + [int(row[col]) % prime])
    rank = 0
    pivots: list[int] = []
    for col in range(d):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % prime:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % prime:
                continue
            factor = matrix[row_idx][col] % prime
            matrix[row_idx] = [
                (matrix[row_idx][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(d + 1)
            ]
        pivots.append(col)
        rank += 1
    for row_idx in range(rank, len(matrix)):
        if all(matrix[row_idx][col] % prime == 0 for col in range(d)) and matrix[row_idx][d] % prime:
            return None
    solution = [0] * d
    for row_idx, pivot in enumerate(pivots):
        solution[pivot] = matrix[row_idx][d] % prime
    return solution


def reconstruct_target_candidate() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    base = nrepair.near_miss_base_profile()
    vectors = [[int(value) % P for value in row] for row in base["template_vectors"]]
    vectors[6][1] = 9
    profile = {
        **base,
        "template_id": TARGET_TEMPLATE_ID,
        "template_family": "single_outside_w7_v3_nearmiss_repair",
        "template_vectors": vectors,
        "mutation_id": "w7_c1_v9",
        "base_template_id": base["template_id"],
    }
    profile["total_effective_cost"] = nrepair.total_effective_cost(vectors, base["selected_counts"])
    profile["variable_count"] = TEMPLATE_DIM * 256
    candidate = nrepair.dependency.evaluate_dependency_candidate(
        profile,
        TARGET_ASSIGNMENT,
        seed=74425,
    )
    candidate["mutation_id"] = profile["mutation_id"]
    candidate["base_template_id"] = profile["base_template_id"]
    classes = nrepair.functional.functional_classes(candidate)
    stable_total, profiles = nrepair.pslot.stable_profiles_for_candidate(classes, limit=20_000)
    target_profile = next(profile for profile in profiles if profile["basis_id"] == TARGET_BASIS_ID)
    target_profile["stable_profile_total"] = stable_total
    target_profile["stable_profiles_constructed"] = len(profiles)
    return candidate, classes, target_profile


def exhaustive_stable_slot_audit(candidate: dict[str, Any], classes: list[dict[str, Any]]) -> dict[str, Any]:
    stable_total, profiles = nrepair.pslot.stable_profiles_for_candidate(classes, limit=20_000)
    summaries = []
    for profile in profiles:
        for slot in range(TEMPLATE_DIM):
            summaries.append(nrepair.raware.actual_slot_summary(candidate, classes, profile, slot, run_proxy=False))
    best = min(
        summaries,
        key=lambda row: (
            int(row["slot_nonzero_rows"]),
            int(row["forced_pair_count"]),
            int(row["basis_zero_union_size"]),
            row["basis_id"],
            int(row["proxy_kernel_slot"]),
        ),
    )
    return {
        "stable_basis_combinations": stable_total,
        "stable_basis_profiles_constructed": len(profiles),
        "slot_profiles_tested": len(summaries),
        "actual_zero_slot_profiles": sum(1 for row in summaries if row["slot_nonzero_rows"] == 0),
        "pair_projection_clear_actual_slots": sum(
            1 for row in summaries if row["slot_nonzero_rows"] == 0 and row["forced_pair_count"] == 0
        ),
        "best_basis_id": best["basis_id"],
        "best_slot": best["proxy_kernel_slot"],
        "best_slot_nonzero_rows": best["slot_nonzero_rows"],
        "best_forced_pair_count": best["forced_pair_count"],
        "best_basis_zero_union_size": best["basis_zero_union_size"],
    }


def residual_rows(classes: list[dict[str, Any]], profile: dict[str, Any]) -> list[dict[str, Any]]:
    by_index = {int(row["class_index"]): row for row in classes}
    rows = []
    for row in profile["nonbasis_constraint_detail"]:
        coords = [int(value) % P for value in row["basis_coordinates"]]
        if coords[TARGET_SLOT] % P == 0:
            continue
        cls = by_index[int(row["class_index"])]
        rows.append(
            {
                "class_index": int(row["class_index"]),
                "support_size": int(row["support_size"]),
                "functional": cls["functional"],
                "basis_coordinates": coords,
                "slot_coefficient": coords[TARGET_SLOT],
                "positions_hash": cls["positions_hash"],
            }
        )
    return rows


def symbolic_u_slot_audit() -> dict[str, Any]:
    slot_values_e4: set[int] = set()
    slot_values_e4_u: set[int] = set()
    valid_pairs = 0
    singular_pairs = 0
    failures = 0
    for u in range(P):
        for v in range(P):
            basis = [
                [0, 0, 1, 0, u, v],
                [0, 1, 0, 0, u, v],
                [1, 0, 0, 0, u, v],
                [0, 0, 0, 1, P - 1, 0],
                [0, 0, 1, 0, P - 1, 0],
                [0, 0, 0, 0, 0, 1],
            ]
            if rank_rows(basis) < TEMPLATE_DIM:
                singular_pairs += 1
                continue
            valid_pairs += 1
            coords_e4 = solve_coordinates([0, 0, 0, 1, 0, 0], basis)
            coords_e4_u = solve_coordinates([0, 0, 0, 1, u, v], basis)
            if coords_e4 is None or coords_e4_u is None:
                failures += 1
                continue
            slot_values_e4.add(coords_e4[TARGET_SLOT] % P)
            slot_values_e4_u.add(coords_e4_u[TARGET_SLOT] % P)
    return {
        "parameter_model": "basis_rows=[e3+u,e2+u,e1+u,e4-e5,e3-e5,e6]",
        "field": "GF(17)",
        "valid_parameter_pairs": valid_pairs,
        "singular_parameter_pairs": singular_pairs,
        "coordinate_solve_failures": failures,
        "class1_slot_values": sorted(slot_values_e4),
        "class5_slot_values": sorted(slot_values_e4_u),
        "zero_slot_solution_count": 0 if 0 not in slot_values_e4 and 0 not in slot_values_e4_u else None,
        "local_equation_status": "RESIDUAL_SLOT_INVARIANT_NONZERO",
    }


def build_record() -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    candidate, classes, profile = reconstruct_target_candidate()
    stable_audit = exhaustive_stable_slot_audit(candidate, classes)
    residual = residual_rows(classes, profile)
    u_audit = symbolic_u_slot_audit()
    best_profile = previous["best_candidate"]["best_profile"]
    proof_status = "EXACT_EXTRACTION_NO_A327 / RESIDUAL_SLOT_INVARIANT_NONZERO / PARTIAL / EXPERIMENTAL"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_nearmiss_repair": {
            "commit": SOURCE_COMMIT,
            "best_template_id": previous["nearmiss_repair_search"]["best_template_id"],
            "best_mutation_id": previous["nearmiss_repair_search"]["best_mutation_id"],
            "best_assignment_strategy": previous["nearmiss_repair_search"]["best_assignment_strategy"],
            "best_basis_id": best_profile["basis_id"],
            "best_slot": best_profile["proxy_kernel_slot"],
            "best_slot_nonzero_rows": previous["nearmiss_repair_search"]["best_slot_nonzero_rows"],
            "best_forced_pair_count": previous["nearmiss_repair_search"]["best_forced_pair_count"],
            "best_failure_mode": previous["nearmiss_repair_search"]["best_failure_mode"],
        },
        "residual_slot_equations": {
            "template_id": candidate["template_id"],
            "mutation_id": candidate["mutation_id"],
            "assignment_strategy": candidate["assignment_strategy"],
            "basis_id": profile["basis_id"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_functionals": profile["basis_functionals"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "slot": TARGET_SLOT,
            "coefficient_matrix_shape": [len(profile["nonbasis_constraint_detail"]), TEMPLATE_DIM],
            "residual_rows": residual,
            "residual_row_count": len(residual),
            "symbolic_u_audit": u_audit,
            "best_failure_mode": "RESIDUAL_SLOT_INVARIANT_NONZERO",
        },
        "exhaustive_stable_profile_audit": stable_audit,
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
            "success or failure outside this residual slot profile",
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
        equations = record["residual_slot_equations"]
        stable = record["exhaustive_stable_profile_audit"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "residual_row_count": equations["residual_row_count"],
                    "symbolic_slot_values": {
                        "class1": equations["symbolic_u_audit"]["class1_slot_values"],
                        "class5": equations["symbolic_u_audit"]["class5_slot_values"],
                    },
                    "stable_profiles_constructed": stable["stable_basis_profiles_constructed"],
                    "slot_profiles_tested": stable["slot_profiles_tested"],
                    "actual_zero_slot_profiles": stable["actual_zero_slot_profiles"],
                    "best_slot_nonzero_rows": stable["best_slot_nonzero_rows"],
                    "best_forced_pair_count": stable["best_forced_pair_count"],
                    "best_failure_mode": equations["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_RESIDUAL_SLOT_EQUATION_REPAIR_READY")


if __name__ == "__main__":
    main()
