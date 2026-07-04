#!/usr/bin/env python3
"""Audit the five-active-row chamber from the diverse pair-clear front."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "e7dada7"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_diverse_chamber_front.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_diverse_five_row_module_audit.json")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_pairclear_diverse_five_row_module_audit.m2")

ROOT = Path(__file__).resolve().parents[2]
DIVERSE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_diverse_chamber_front.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
TARGET_MUTATION_ID = "w2_c0_d1"
TARGET_ASSIGNMENT = "fiber_round_robin"
TARGET_ASSIGNMENT_SEED = 109978
TARGET_BASIS_CLASS_INDICES = [0, 1, 2, 3, 4, 6]
TARGET_DIRECTION = [1, 16, 0, 14, 14, 11]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


diverse = load_module("pairclear_diverse_chamber_front", DIVERSE_SCRIPT)
ninerow = diverse.ninerow
lowrank = diverse.lowrank
zstable = diverse.zstable
basisaware = diverse.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def dot(row: list[int] | tuple[int, ...], vector: list[int] | tuple[int, ...]) -> int:
    return sum(int(row[idx]) * int(vector[idx]) for idx in range(TEMPLATE_DIM)) % P


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
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % P:
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


def normalize_projective(vector: list[int]) -> list[int]:
    values = [int(value) % P for value in vector]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return [(entry * inv) % P for entry in values]
    return values


def matrix_record(name: str, rows: list[list[int]]) -> dict[str, Any]:
    rank = rank_rows(rows)
    return {
        "name": name,
        "shape": [len(rows), TEMPLATE_DIM],
        "rank": rank,
        "right_kernel_nullity": TEMPLATE_DIM - rank,
        "left_syzygy_dimension": len(rows) - rank,
        "right_kernel_basis": nullspace_basis(rows),
    }


def m2_row(row: list[int]) -> str:
    return "{" + ",".join(f"{int(value) % P}_R" for value in row) + "}"


def m2_matrix(rows: list[list[int]]) -> str:
    return "{" + ",".join(m2_row(row) for row in rows) + "}"


def m2_block(name: str, rows: list[list[int]]) -> str:
    return f"""{name} = matrix({m2_matrix(rows)})
print concatenate("M2_{name}_ROWS=", toString numRows {name})
print concatenate("M2_{name}_COLS=", toString numColumns {name})
print concatenate("M2_{name}_RANK=", toString rank {name})
{name}RightK = gens kernel {name}
print concatenate("M2_{name}_RIGHT_KERNEL_GENS=", toString numColumns {name}RightK)
{name}LeftK = gens kernel transpose {name}
print concatenate("M2_{name}_LEFT_SYZYGY_GENS=", toString numColumns {name}LeftK)
print concatenate("M2_{name}_LEFT_SYZYGY_RANK=", toString rank {name}LeftK)
"""


def run_m2() -> dict[str, Any]:
    proc = subprocess.run(
        ["M2", "--script", str(M2_SCRIPT_PATH)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    parsed: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        if line.startswith("M2_") and "=" in line:
            key, value = line.split("=", 1)
            parsed[key] = int(value)
    return {
        "command": ["M2", "--script", str(M2_SCRIPT_PATH)],
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "parsed": parsed,
    }


def reconstruct_target() -> tuple[dict[str, Any], dict[str, Any], int]:
    specs = ninerow.mutation_specs(max_mutations=96)
    for profile_index, spec in enumerate(specs):
        if spec.get("mutation_id") != TARGET_MUTATION_ID:
            continue
        profile = lowrank.solve_template_counts(spec)
        profile["mutation_id"] = spec.get("mutation_id")
        profile["base_template_id"] = spec.get("base_template_id")
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            raise RuntimeError("target profile not feasible")
        strategy_index = profile["assignment_strategies"].index(TARGET_ASSIGNMENT)
        candidate = diverse.candidate_from_profile(
            profile,
            TARGET_ASSIGNMENT,
            seed=106000 + 97 * profile_index + strategy_index,
        )
        if candidate["assignment_seed"] != TARGET_ASSIGNMENT_SEED:
            raise RuntimeError(f"unexpected assignment seed {candidate['assignment_seed']}")
        classes = basisaware.functional.functional_classes(candidate)
        by_class = {int(row["class_index"]): idx for idx, row in enumerate(classes)}
        combo = tuple(by_class[int(class_index)] for class_index in TARGET_BASIS_CLASS_INDICES)
        basis_profile = basisaware.profile_from_indices(
            classes,
            combo,
            "basisaware_" + "_".join(str(item) for item in TARGET_BASIS_CLASS_INDICES),
        )
        if basis_profile is None:
            raise RuntimeError("target basis profile missing")
        return candidate, basis_profile, profile_index
    raise RuntimeError("target mutation not generated")


def build_record(run_macaulay2: bool) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    candidate, profile, profile_index = reconstruct_target()
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_values = [dot(row, TARGET_DIRECTION) for row in matrix]
    inactive_indices = [idx for idx, value in enumerate(row_values) if not value % P]
    active_indices = [idx for idx, value in enumerate(row_values) if value % P]
    inactive_rows = [matrix[idx] for idx in inactive_indices]
    active_rows = [matrix[idx] for idx in active_indices]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    inactive_classes = [row_classes[idx] for idx in inactive_indices]
    active_classes = [row_classes[idx] for idx in active_indices]

    pair_scalars = zstable.zexp.pair_projection_scalars(candidate, profile, TARGET_DIRECTION)
    forced_pairs = [pair for pair, value in pair_scalars.items() if int(value) % P == 0]
    direction_projective = normalize_projective(TARGET_DIRECTION)

    singleton_records = []
    for active_idx, active_class in zip(active_indices, active_classes, strict=True):
        rows = inactive_rows + [matrix[active_idx]]
        rank = rank_rows(rows)
        singleton_records.append(
            {
                "active_row_index": active_idx,
                "active_row_class": active_class,
                "rank_inactive_plus_row": rank,
                "right_kernel_nullity": TEMPLATE_DIM - rank,
                "full_rank": rank == TEMPLATE_DIM,
            }
        )

    pair_records = []
    for first_pos, first_idx in enumerate(active_indices):
        for second_idx in active_indices[first_pos + 1 :]:
            rows = inactive_rows + [matrix[first_idx], matrix[second_idx]]
            rank = rank_rows(rows)
            pair_records.append(
                {
                    "active_row_indices": [first_idx, second_idx],
                    "active_row_classes": [row_classes[first_idx], row_classes[second_idx]],
                    "rank_inactive_plus_rows": rank,
                    "right_kernel_nullity": TEMPLATE_DIM - rank,
                    "full_rank": rank == TEMPLATE_DIM,
                }
            )

    inactive_record = matrix_record("INACTIVE", inactive_rows)
    inactive_projective = [normalize_projective(vector) for vector in inactive_record["right_kernel_basis"]]

    rank_slack = previous["best_full_profile"]["best_rank_slack_chamber"]
    rank_slack_rows = [matrix[idx] for idx in rank_slack["zero_row_indices"]]
    rank_slack_record = matrix_record("RANKSLACK", rank_slack_rows)
    rank_slack_projective = [normalize_projective(vector) for vector in rank_slack_record["right_kernel_basis"]]

    m2_result = None
    if run_macaulay2:
        m2_text = "-- Generated by scan_m1_a327_pairclear_diverse_five_row_module_audit.py\n"
        m2_text += "R = ZZ/17[x]\n"
        m2_text += m2_block("FULL", matrix)
        m2_text += m2_block("ACTIVE", active_rows)
        m2_text += m2_block("INACTIVE", inactive_rows)
        m2_text += m2_block("RANKSLACK", rank_slack_rows)
        for idx, row in enumerate(singleton_records):
            ext_rows = inactive_rows + [matrix[row["active_row_index"]]]
            m2_text += f"EXT{idx} = matrix({m2_matrix(ext_rows)})\n"
            m2_text += f'print concatenate("M2_EXT{idx}_RANK=", toString rank EXT{idx})\n'
        M2_SCRIPT_PATH.write_text(m2_text)
        m2_result = run_m2()

    proof_status = "AUDIT / DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL"
    failure = "DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED"
    if forced_pairs:
        proof_status = "EXACT_EXTRACTION_NO_A327 / DIVERSE_FIVEROW_FORCED_PAIR / PARTIAL / EXPERIMENTAL"
        failure = "DIVERSE_FIVEROW_FORCED_PAIR"
    elif inactive_record["right_kernel_nullity"] != 1:
        proof_status = "CANDIDATE / DIVERSE_FIVEROW_INACTIVE_NULLITY_NOT_ONE / PARTIAL / EXPERIMENTAL"
        failure = "DIVERSE_FIVEROW_INACTIVE_NULLITY_NOT_ONE"
    elif direction_projective not in inactive_projective:
        proof_status = "EXACT_EXTRACTION_NO_A327 / DIVERSE_FIVEROW_DIRECTION_NOT_IN_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "DIVERSE_FIVEROW_DIRECTION_NOT_IN_KERNEL"

    previous_search = previous["diverse_chamber_front"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_diverse_chamber_front": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "sampled_profiles": previous_search["sampled_profiles"],
            "full_profiles_scanned": previous_search["full_profiles_scanned"],
            "full_direct_support_reduced_profiles": previous_search["full_direct_support_reduced_profiles"],
            "best_template_id": previous_search["best_template_id"],
            "best_mutation_id": previous_search["best_mutation_id"],
            "best_basis_id": previous_search["best_basis_id"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "target_system": {
            "template_id": candidate["template_id"],
            "mutation_id": candidate.get("mutation_id"),
            "profile_index": profile_index,
            "assignment_strategy": candidate["assignment_strategy"],
            "assignment_seed": candidate["assignment_seed"],
            "basis_id": profile["basis_id"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "direction": TARGET_DIRECTION,
            "direction_projective": direction_projective,
            "pair_projection_scalars": pair_scalars,
            "forced_pairs": forced_pairs,
            "row_classes": row_classes,
            "row_values": row_values,
            "active_row_indices": active_indices,
            "active_row_classes": active_classes,
            "inactive_row_indices": inactive_indices,
            "inactive_row_classes": inactive_classes,
        },
        "module_audit": {
            "field": "GF(17)",
            "full_matrix": matrix_record("FULL", matrix),
            "active_matrix": matrix_record("ACTIVE", active_rows),
            "inactive_matrix": inactive_record,
            "inactive_kernel_projective_basis": inactive_projective,
            "direction_spans_inactive_kernel": direction_projective in inactive_projective,
            "singleton_extensions": singleton_records,
            "singleton_full_rank_count": sum(1 for row in singleton_records if row["full_rank"]),
            "singleton_extensions_tested": len(singleton_records),
            "pair_extensions": pair_records,
            "pair_full_rank_count": sum(1 for row in pair_records if row["full_rank"]),
            "pair_extensions_tested": len(pair_records),
            "rank_slack_chamber": {
                "zero_row_indices": rank_slack["zero_row_indices"],
                "zero_row_classes": rank_slack["zero_row_classes"],
                "exemplar_direction": rank_slack["exemplar_direction"],
                "exemplar_direction_projective": rank_slack["exemplar_direction_projective"],
                "matrix": rank_slack_record,
                "kernel_projective_basis": rank_slack_projective,
            },
            "best_failure_mode": failure,
        },
        "macaulay2": {
            "script_path": str(M2_SCRIPT_PATH),
            "result": m2_result,
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
            "global obstruction outside the audited five-row module front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--skip-m2", action="store_true")
    args = parser.parse_args()
    record = build_record(run_macaulay2=not args.skip_m2)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        module = record["module_audit"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "full_rank": module["full_matrix"]["rank"],
                    "active_rank": module["active_matrix"]["rank"],
                    "inactive_rank": module["inactive_matrix"]["rank"],
                    "inactive_right_kernel_nullity": module["inactive_matrix"]["right_kernel_nullity"],
                    "direction_spans_inactive_kernel": module["direction_spans_inactive_kernel"],
                    "active_row_count": module["active_matrix"]["shape"][0],
                    "inactive_row_count": module["inactive_matrix"]["shape"][0],
                    "singleton_extensions_tested": module["singleton_extensions_tested"],
                    "singleton_full_rank_count": module["singleton_full_rank_count"],
                    "rank_slack_rank": module["rank_slack_chamber"]["matrix"]["rank"],
                    "rank_slack_nullity": module["rank_slack_chamber"]["matrix"]["right_kernel_nullity"],
                    "best_failure_mode": module["best_failure_mode"],
                    "m2_returncode": None if record["macaulay2"]["result"] is None else record["macaulay2"]["result"]["returncode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_DIVERSE_FIVEROW_MODULE_AUDIT_READY")


if __name__ == "__main__":
    main()
