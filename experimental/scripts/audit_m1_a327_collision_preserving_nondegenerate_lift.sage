#!/usr/bin/env sage
"""Exact GF(17^32) collision-preserving nondegenerate lift audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
VARIABLE_COUNT = DIFF_COUNT * K
TARGET_AGREEMENT = 327
SOURCE_COMMIT = "9c2f278"

SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_robust_proxy_constrained_extraction.py")
SOURCE_DATA_PATH = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
BASELINE_PATH = Path("experimental/data/m1_a327_nondegenerate_exact_lift.json")
DATA_PATH = Path("experimental/data/m1_a327_collision_preserving_nondegenerate_lift.json")

SYSTEM_LIMIT = 3
MAX_VECTOR_EVALUATIONS = 36
ROW_SUBSETS = ["proxy_pivot_rows_64", "proxy_pivot_rows_128"]
PIN_FAMILIES = [
    "coefficient_proxy_plus_5x1",
    "coefficient_proxy_plus_5x2",
    "coefficient_proxy_plus_5x4",
    "coefficient_proxy_plus_6x1",
]
PIVOT_SCHEDULES = ["prefix_pivots", "mixed_block_pivots"]


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


def load_module(path: Path, module_name: str):
    script_dir = str(path.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H, generator


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def members(mask):
    return [idx for idx in range(LIST_SIZE) if int(mask) & (1 << idx)]


def constraint_rows_for_coordinate(F, powers, mask, pos):
    bits = members(mask)
    rows = []
    if 0 in bits:
        for witness in bits:
            if witness == 0:
                continue
            row = [F(0)] * VARIABLE_COUNT
            start = (witness - 1) * K
            for degree in range(K):
                row[start + degree] = powers[degree][pos]
            rows.append(row)
        return rows
    if len(bits) < 2:
        return rows
    left = bits[0]
    left_start = (left - 1) * K
    for witness in bits[1:]:
        row = [F(0)] * VARIABLE_COUNT
        right_start = (witness - 1) * K
        for degree in range(K):
            row[left_start + degree] = powers[degree][pos]
            row[right_start + degree] = -powers[degree][pos]
        rows.append(row)
    return rows


def rows_for_selected(F, powers, selected):
    rows = []
    for coord in selected:
        rows.extend(constraint_rows_for_coordinate(F, powers, coord["mask"], coord["position"]))
    if not rows:
        raise RuntimeError("empty exact row set")
    return rows


def exact_values_from_vector(F, powers, vector_value):
    values = [[F(0) for _ in range(N)]]
    for witness in range(DIFF_COUNT):
        start = witness * K
        witness_values = [F(0) for _ in range(N)]
        for degree in range(K):
            coeff = vector_value[start + degree]
            if coeff == 0:
                continue
            power_row = powers[degree]
            for pos in range(N):
                witness_values[pos] += coeff * power_row[pos]
        values.append(witness_values)
    return values


def class_masks_by_position(values):
    rows = []
    for pos in range(N):
        buckets = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = int(buckets.get(value, 0)) | (1 << witness)
        rows.append(sorted(set(int(mask) for mask in buckets.values())))
    return rows


def capacity_from_class_masks(class_rows):
    total = 0
    histogram = {}
    for masks in class_rows:
        largest = max(int(mask).bit_count() for mask in masks)
        total += largest
        histogram[str(largest)] = histogram.get(str(largest), 0) + 1
    return {
        "capacity_total": total,
        "capacity_upper_bound": total // LIST_SIZE,
        "largest_class_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
    }


def assignment_max_min(class_rows):
    offsets = []
    total_vars = 0
    for classes in class_rows:
        offsets.append(total_vars)
        total_vars += len(classes)
    rows = []
    lower = []
    upper = []
    for pos, classes in enumerate(class_rows):
        row = np.zeros(total_vars)
        row[offsets[pos] : offsets[pos] + len(classes)] = 1
        rows.append(row)
        lower.append(1)
        upper.append(1)
    for witness in range(LIST_SIZE):
        row = np.zeros(total_vars)
        for pos, classes in enumerate(class_rows):
            for idx, mask in enumerate(classes):
                if int(mask) & (1 << witness):
                    row[offsets[pos] + idx] = 1
        rows.append(row)
        lower.append(0)
        upper.append(np.inf)
    matrix = np.vstack(rows)
    lower = np.array(lower)
    upper = np.array(upper)

    def feasible(floor):
        local_lower = lower.copy()
        local_lower[-LIST_SIZE:] = floor
        result = milp(
            np.zeros(total_vars),
            integrality=np.ones(total_vars),
            bounds=Bounds(np.zeros(total_vars), np.ones(total_vars)),
            constraints=LinearConstraint(matrix, local_lower, upper),
            options={"time_limit": 20},
        )
        if not result.success:
            return False, None
        rounded = np.rint(result.x).astype(int)
        chosen = []
        for pos, classes in enumerate(class_rows):
            start = offsets[pos]
            choice = next(
                (idx for idx, value in enumerate(rounded[start : start + len(classes)]) if value),
                0,
            )
            chosen.append(int(classes[choice]))
        return True, chosen

    cap = capacity_from_class_masks(class_rows)["capacity_upper_bound"]
    lo, hi = 0, max(cap, TARGET_AGREEMENT)
    best_masks = None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok, masks = feasible(mid)
        if ok:
            lo = mid
            best_masks = masks
        else:
            hi = mid - 1
    agreement = [0] * LIST_SIZE
    if best_masks is not None:
        for mask in best_masks:
            for witness in range(LIST_SIZE):
                if int(mask) & (1 << witness):
                    agreement[witness] += 1
    return {
        "exact_max_min": int(lo),
        "agreement_vector": agreement,
        "chosen_masks_hash": None if best_masks is None else hash_payload(best_masks),
    }


def value_hashes(values):
    return [hash_payload([str(value) for value in row]) for row in values]


def evaluate_vector(F, powers, vector_value):
    values = exact_values_from_vector(F, powers, vector_value)
    hashes = value_hashes(values)
    distinct = len(set(hashes)) == LIST_SIZE
    coeff_support = {}
    nonzero_blocks = []
    for block in range(DIFF_COUNT):
        start = block * K
        count = sum(1 for coeff in vector_value[start : start + K] if coeff != 0)
        label = f"D_{block + 2}"
        coeff_support[label] = count
        if count:
            nonzero_blocks.append(label)
    class_rows = class_masks_by_position(values)
    capacity = capacity_from_class_masks(class_rows)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = assignment_max_min(class_rows)
    if not distinct:
        status = "DEGENERATE_CODEWORDS"
    elif capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        status = "PIN_DESTROYS_COLLISION"
    elif assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        status = "EXACT_A327_ASSIGNMENT"
    else:
        status = "LOW_RESCHEDULE"
    return {
        "distinct_codewords": distinct,
        "nonzero_witness_blocks": nonzero_blocks,
        "coefficient_support_by_block": coeff_support,
        "codeword_value_hash": hash_payload(hashes),
        **capacity,
        "assignment": assignment,
        "status": status,
    }


def unique_in_order(columns):
    seen = set()
    output = []
    for col in columns:
        col = int(col)
        if col in seen:
            continue
        seen.add(col)
        output.append(col)
    return output


def columns_by_block(columns, block):
    return [int(col) for col in columns if int(col) // K == block]


def proxy_support_free_columns(system):
    common_free = set(int(col) for col in system["common_free_columns"])
    return unique_in_order([int(col) for col in system["best_schedule"]["free_columns"] if int(col) in common_free])


def pin_family_columns(system, family):
    common_free = [int(col) for col in system["common_free_columns"]]
    proxy_cols = proxy_support_free_columns(system)
    columns = list(proxy_cols)
    if family == "coefficient_proxy_plus_5x1":
        per_block = 1
        blocks = range(1, DIFF_COUNT)
    elif family == "coefficient_proxy_plus_5x2":
        per_block = 2
        blocks = range(1, DIFF_COUNT)
    elif family == "coefficient_proxy_plus_5x4":
        per_block = 4
        blocks = range(1, DIFF_COUNT)
    elif family == "coefficient_proxy_plus_6x1":
        per_block = 1
        blocks = range(DIFF_COUNT)
    else:
        raise ValueError(f"unknown pin family {family}")
    for block in blocks:
        columns.extend(columns_by_block(common_free, block)[:per_block])
    return unique_in_order(columns)


def block_distribution(columns):
    hist = {}
    for col in columns:
        label = f"D_{2 + int(col) // K}"
        hist[label] = hist.get(label, 0) + 1
    return dict(sorted(hist.items()))


def free_assignments(F, generator, columns):
    assignments = {}
    for idx, col in enumerate(columns):
        block = int(col) // K
        if block == 0:
            value = F(1)
        else:
            value = generator ** (block * 41 + idx + 1)
        assignments[int(col)] = value
    return assignments


def mixed_block_pivots(common_pivots, row_count):
    output = []
    seen = set()
    # Keep enough early D_2 pivots to preserve the high-collision solve shape.
    d2 = columns_by_block(common_pivots, 0)
    for col in d2[: max(8, row_count // 3)]:
        if col not in seen:
            seen.add(col)
            output.append(col)
    while len(output) < row_count:
        changed = False
        for block in range(DIFF_COUNT):
            for col in columns_by_block(common_pivots, block):
                if col in seen:
                    continue
                seen.add(col)
                output.append(col)
                changed = True
                break
            if len(output) >= row_count:
                break
        if not changed:
            break
    return output[:row_count]


def pivot_columns(system, row_count, schedule_id):
    common_pivots = [int(col) for col in system["common_pivot_columns"]]
    if schedule_id == "prefix_pivots":
        return common_pivots[:row_count]
    if schedule_id == "mixed_block_pivots":
        return mixed_block_pivots(common_pivots, row_count)
    raise ValueError(f"unknown pivot schedule {schedule_id}")


def solve_pinned_vector(F, exact_rows, row_indices, pivot_cols, assignments):
    if len(pivot_cols) != len(row_indices):
        return None, {
            "status": "PIN_INCONSISTENT",
            "reason": "pivot_count_row_count_mismatch",
            "pivot_minor_size": len(pivot_cols),
            "rows": len(row_indices),
        }
    matrix_rows = []
    rhs = []
    for row_idx in row_indices:
        row = exact_rows[int(row_idx)]
        matrix_rows.append([row[col] for col in pivot_cols])
        rhs.append(-sum(row[col] * value for col, value in assignments.items()))
    A = Matrix(F, matrix_rows, ncols=len(pivot_cols))
    rank = int(A.rank())
    if rank < len(pivot_cols):
        return None, {
            "status": "PIN_INCONSISTENT",
            "reason": "singular_scheduled_pivot_minor",
            "pivot_minor_rank": rank,
            "pivot_minor_size": len(pivot_cols),
        }
    solution = list(A.solve_right(vector(F, rhs)))
    vec = [F(0)] * VARIABLE_COUNT
    for col, value in assignments.items():
        vec[int(col)] = value
    for col, value in zip(pivot_cols, solution):
        vec[int(col)] = value
    return vec, {
        "status": "PINNED_SOLVE_OK",
        "pivot_minor_rank": rank,
        "pivot_minor_size": len(pivot_cols),
    }


def row_subset_map(scanner, selected):
    powers = scanner.proxy.vandermonde_powers_modp(12289)
    rows = scanner.proxy.rows_for_selected_modp(powers, selected["selected"], 12289)
    _echelon, _pivots, pivot_rows = scanner.echelon_with_rows(rows, 12289)
    descriptors = scanner.row_descriptors(selected["selected"])
    return {
        "proxy_pivot_rows_64": pivot_rows[:64],
        "proxy_pivot_rows_128": pivot_rows[:128],
        "proxy_pivot_rows_256": pivot_rows[:256],
        "fiber_diverse_rows_128": scanner.choose_round_robin_by_fiber(descriptors, 128),
    }


def audit_one_system(scanner, system, F, powers, generator, evaluation_budget):
    source_row = scanner.source_proxy_row_by_id()[system["system_id"]]
    _source, _base, selected = scanner.proxy.reconstruct_selected(source_row)
    exact_rows = rows_for_selected(F, powers, selected["selected"])
    subsets = row_subset_map(scanner, selected)
    evaluations = []
    for subset_name in ROW_SUBSETS:
        row_indices = [int(idx) for idx in subsets[subset_name]]
        for family in PIN_FAMILIES:
            pin_columns = pin_family_columns(system, family)
            assignments = free_assignments(F, generator, pin_columns)
            for pivot_schedule in PIVOT_SCHEDULES:
                if len(evaluations) >= evaluation_budget:
                    break
                pivots = pivot_columns(system, len(row_indices), pivot_schedule)
                vec, solve = solve_pinned_vector(F, exact_rows, row_indices, pivots, assignments)
                evaluation = None if vec is None else evaluate_vector(F, powers, vec)
                evaluations.append(
                    {
                        "subset": subset_name,
                        "rows": len(row_indices),
                        "pin_family": family,
                        "pivot_schedule": pivot_schedule,
                        "free_column_count": len(pin_columns),
                        "free_block_distribution": block_distribution(pin_columns),
                        "solve": solve,
                        "evaluation": evaluation,
                    }
                )
            if len(evaluations) >= evaluation_budget:
                break
        if len(evaluations) >= evaluation_budget:
            break
    exact_hits = [
        row
        for row in evaluations
        if row["evaluation"] is not None and row["evaluation"]["status"] == "EXACT_A327_ASSIGNMENT"
    ]
    nondegenerate_high_capacity = [
        row
        for row in evaluations
        if row["evaluation"] is not None
        and row["evaluation"]["distinct_codewords"]
        and row["evaluation"]["capacity_upper_bound"] >= TARGET_AGREEMENT
    ]
    best = max(
        evaluations,
        key=lambda row: (
            -1
            if row["evaluation"] is None or row["evaluation"]["assignment"] is None
            else row["evaluation"]["assignment"]["exact_max_min"],
            -1 if row["evaluation"] is None else row["evaluation"]["capacity_upper_bound"],
            1 if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"] else 0,
        ),
    )
    hist = {}
    for row in evaluations:
        status = row["evaluation"]["status"] if row["evaluation"] is not None else row["solve"]["status"]
        hist[status] = hist.get(status, 0) + 1
    return {
        "system_id": system["system_id"],
        "source_proxy_best_max_min": system["source_proxy_best_max_min"],
        "common_pivot_count": system["common_pivot_count"],
        "common_free_count": system["common_free_count"],
        "evaluations": evaluations,
        "exact_vectors_constructed": len(evaluations),
        "nondegenerate_vectors": sum(
            1 for row in evaluations if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"]
        ),
        "nondegenerate_high_capacity_vectors": len(nondegenerate_high_capacity),
        "exact_a327_vectors": len(exact_hits),
        "failure_histogram": dict(sorted(hist.items())),
        "best": best,
        "status": "EXACT_A327_FOUND" if exact_hits else "EXACT_EXTRACTION_NO_A327",
    }


def audit_record():
    scanner = load_module(SCANNER_PATH, "robust_proxy_constrained_scanner")
    with SOURCE_DATA_PATH.open() as handle:
        source = json.load(handle)
    with BASELINE_PATH.open() as handle:
        baseline = json.load(handle)
    q, F, H, generator = field_context()
    powers = precompute_powers(F, H)
    systems = sorted(
        source["systems"],
        key=lambda row: (
            row["best_schedule"]["candidate_prime_count"],
            row["pivot_stability_score"],
            row["source_proxy_best_max_min"],
            row["system_id"],
        ),
        reverse=True,
    )[:SYSTEM_LIMIT]
    per_system_budget = max(1, MAX_VECTOR_EVALUATIONS // len(systems))
    results = [audit_one_system(scanner, system, F, powers, generator, per_system_budget) for system in systems]
    all_evaluations = [item for row in results for item in row["evaluations"]]
    exact_hits = sum(row["exact_a327_vectors"] for row in results)
    high_capacity_nondegenerate = sum(row["nondegenerate_high_capacity_vectors"] for row in results)

    def eval_floor(item):
        if item["evaluation"] is None or item["evaluation"]["assignment"] is None:
            return -1
        return item["evaluation"]["assignment"]["exact_max_min"]

    best = max(
        all_evaluations,
        key=lambda row: (
            eval_floor(row),
            -1 if row["evaluation"] is None else row["evaluation"]["capacity_upper_bound"],
            1 if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"] else 0,
        ),
    )
    best_assignment = None if best["evaluation"] is None else best["evaluation"]["assignment"]
    proof_status = "CANDIDATE" if exact_hits else "EXACT_EXTRACTION_NO_A327"
    best_failure = best["evaluation"]["status"] if best["evaluation"] is not None else best["solve"]["status"]
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "collision_preserving_nondegenerate_lift",
            "source_commit": SOURCE_COMMIT,
            "baseline": {
                "best_high_capacity_degenerate_capacity": baseline["exact_lift_search"]["best_capacity_upper_bound"],
                "best_degenerate_max_min": baseline["exact_lift_search"]["best_exact_max_min"],
                "best_nondegenerate_capacity": 94,
                "baseline_result_hash": baseline["result_hash"],
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "pin_search": {
                "pin_families_tested": PIN_FAMILIES,
                "pivot_schedules_tested": PIVOT_SCHEDULES,
                "systems_tested": len(results),
                "exact_vectors_constructed": len(all_evaluations),
                "nondegenerate_vectors": sum(row["nondegenerate_vectors"] for row in results),
                "nondegenerate_high_capacity_vectors": high_capacity_nondegenerate,
                "best_capacity_upper_bound": None if best["evaluation"] is None else best["evaluation"]["capacity_upper_bound"],
                "best_exact_max_min": None if best_assignment is None else best_assignment["exact_max_min"],
                "best_agreement_vector": None if best_assignment is None else best_assignment["agreement_vector"],
                "best_failure_mode": best_failure,
            },
            "exact_a327_vector_count": exact_hits,
            "results": results,
            "candidate": {
                "reaches_327_exact": exact_hits > 0,
                "sage_audited": exact_hits > 0,
            },
            "result_hash": hash_payload(results),
            "proof_status": proof_status,
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond stated interleaved-list predicate",
                "global Lambda_mu(C,327) <= 6",
                "exact Lambda_mu",
                "exact delta*_C",
                "improvement over PR #133",
                "full GF(17^32) nullspace extraction",
            ],
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()
    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_COLLISION_PRESERVING_NONDEGENERATE_LIFT_OK")
        print("exact_vectors_constructed: %d" % record["pin_search"]["exact_vectors_constructed"])
        print("nondegenerate_high_capacity_vectors: %d" % record["pin_search"]["nondegenerate_high_capacity_vectors"])
        print("best_exact_max_min: %s" % record["pin_search"]["best_exact_max_min"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
