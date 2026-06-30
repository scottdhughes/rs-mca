#!/usr/bin/env sage
"""Exact GF(17^32) dominant-collision-preserving separation audit."""

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
SOURCE_COMMIT = "9bbffb8"

SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_robust_proxy_constrained_extraction.py")
ROBUST_DATA_PATH = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
BASELINE_PATH = Path("experimental/data/m1_a327_collision_preserving_nondegenerate_lift.json")
DATA_PATH = Path("experimental/data/m1_a327_dominant_collision_preserving_separation.json")

SYSTEM_LIMIT = 3
ROW_SUBSETS = ["dominant_collision_rows_64", "proxy_pivot_rows_128"]
SEPARATION_FAMILIES = ["one_pairwise_safe", "two_pairwise_safe", "five_eval_safe", "six_eval_safe"]
PIVOT_SCHEDULES = ["prefix_pivots", "separation_aware_pivots"]
MAX_EVALUATIONS = 24


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


def evaluate_vector(F, powers, vector_value):
    values = exact_values_from_vector(F, powers, vector_value)
    value_hashes = [hash_payload([str(value) for value in row]) for row in values]
    distinct = len(set(value_hashes)) == LIST_SIZE
    support_by_block = {}
    nonzero_blocks = []
    for block in range(DIFF_COUNT):
        start = block * K
        count = sum(1 for coeff in vector_value[start : start + K] if coeff != 0)
        label = f"D_{block + 2}"
        support_by_block[label] = count
        if count:
            nonzero_blocks.append(label)
    class_rows = class_masks_by_position(values)
    capacity = capacity_from_class_masks(class_rows)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = assignment_max_min(class_rows)
    if not distinct and capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        status = "DEGENERATE_HIGH_CAPACITY"
    elif not distinct:
        status = "DEGENERATE_CODEWORDS"
    elif capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        status = "PIN_DESTROYS_COLLISION"
    elif assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        status = "CANDIDATE_A327"
    else:
        status = "NONDEGENERATE_LOW_RESCHEDULE"
    return {
        "distinct_codewords": distinct,
        "nonzero_witness_blocks": nonzero_blocks,
        "coefficient_support_by_block": support_by_block,
        "codeword_value_hash": hash_payload(value_hashes),
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


def proxy_support_columns(system):
    common_free = set(int(col) for col in system["common_free_columns"])
    return unique_in_order([int(col) for col in system["best_schedule"]["free_columns"] if int(col) in common_free])


def eval_row(F, powers, block, pos, scale=1):
    row = [F(0)] * VARIABLE_COUNT
    start = int(block) * K
    for degree in range(K):
        row[start + degree] = F(scale) * powers[degree][pos]
    return row


def pairwise_row(F, powers, left_block, right_block, pos):
    row = eval_row(F, powers, left_block, pos, 1)
    right = eval_row(F, powers, right_block, pos, -1)
    return [a + b for a, b in zip(row, right)]


def columns_by_block(columns, block):
    return [int(col) for col in columns if int(col) // K == int(block)]


def separation_blocks(specs):
    blocks = []
    for spec in specs:
        for key in ["left_block", "right_block"]:
            label = spec[key]
            if label is None:
                continue
            blocks.append(int(label.split("_")[1]) - 2)
    return unique_in_order(blocks)


def pivot_columns(system, target_count, sep_count, specs, schedule_id):
    count = target_count + sep_count
    common_pivots = [int(col) for col in system["common_pivot_columns"]]
    if schedule_id == "prefix_pivots":
        return common_pivots[:count]
    if schedule_id != "separation_aware_pivots":
        raise ValueError(f"unknown pivot schedule {schedule_id}")
    output = []
    seen = set()
    # Preserve the target-row pivot skeleton first.
    for col in common_pivots[:target_count]:
        if col not in seen:
            seen.add(col)
            output.append(col)
    # Add pivots in the blocks touched by separation pins.
    for block in separation_blocks(specs):
        for col in columns_by_block(common_pivots, block):
            if col in seen:
                continue
            seen.add(col)
            output.append(col)
            break
        if len(output) >= count:
            break
    # Fill deterministically if the touched blocks were already covered.
    for col in common_pivots:
        if len(output) >= count:
            break
        if col in seen:
            continue
        seen.add(col)
        output.append(col)
    return output[:count]


def row_subset_map(scanner, selected):
    powers = scanner.proxy.vandermonde_powers_modp(12289)
    rows = scanner.proxy.rows_for_selected_modp(powers, selected["selected"], 12289)
    _echelon, _pivots, pivot_rows = scanner.echelon_with_rows(rows, 12289)
    return {
        "dominant_collision_rows_64": pivot_rows[:64],
        "proxy_pivot_rows_128": pivot_rows[:128],
    }


def solve_base_degenerate(F, exact_rows, system, row_indices):
    free_cols = proxy_support_columns(system)
    rows = []
    rhs = []
    for row_idx in row_indices:
        row = exact_rows[int(row_idx)]
        rows.append([row[col] for col in system["common_pivot_columns"][: len(row_indices)]])
        rhs.append(-sum(row[col] for col in free_cols))
    A = Matrix(F, rows, ncols=len(row_indices))
    sol = list(A.solve_right(vector(F, rhs)))
    vec = [F(0)] * VARIABLE_COUNT
    for col in free_cols:
        vec[col] = F(1)
    for col, value in zip(system["common_pivot_columns"][: len(row_indices)], sol):
        vec[int(col)] = value
    return vec


def diverse_safe_positions(class_rows, count):
    safe = [pos for pos, masks in enumerate(class_rows) if max(int(mask).bit_count() for mask in masks) == 6]
    buckets = {}
    for pos in safe:
        buckets.setdefault(pos % 16, []).append(pos)
    output = []
    while len(output) < count:
        changed = False
        for fiber in sorted(buckets):
            if buckets[fiber]:
                output.append(buckets[fiber].pop(0))
                changed = True
                if len(output) >= count:
                    break
        if not changed:
            break
    return output


def separation_pins(F, powers, family, safe_positions, generator):
    rows = []
    rhs = []
    specs = []
    if family == "one_pairwise_safe":
        pin_specs = [("pair", 1, 2, safe_positions[0], F(1))]
    elif family == "two_pairwise_safe":
        pin_specs = [
            ("pair", 1, 2, safe_positions[0], F(1)),
            ("pair", 3, 4, safe_positions[1], F(2)),
        ]
    elif family == "five_eval_safe":
        pin_specs = [("eval", block, None, safe_positions[block - 1], F(block + 1)) for block in range(1, 6)]
    elif family == "six_eval_safe":
        pin_specs = [("eval", block, None, safe_positions[block], generator ** (block + 1)) for block in range(6)]
    else:
        raise ValueError(f"unknown separation family {family}")
    for kind, left, right, pos, gamma in pin_specs:
        if kind == "pair":
            rows.append(pairwise_row(F, powers, left, right, pos))
        else:
            rows.append(eval_row(F, powers, left, pos))
        rhs.append(gamma)
        specs.append(
            {
                "kind": kind,
                "left_block": None if left is None else f"D_{left + 2}",
                "right_block": None if right is None else f"D_{right + 2}",
                "position": int(pos),
                "fiber": int(pos) % 16,
                "rhs_hash": hash_payload(str(gamma)),
            }
        )
    return rows, rhs, specs


def solve_scheduled_system(F, rows, rhs, pivot_cols, free_assignments):
    if len(rows) != len(pivot_cols):
        return None, {
            "status": "PIN_INCONSISTENT",
            "reason": "pivot_count_row_count_mismatch",
            "rows": len(rows),
            "pivot_count": len(pivot_cols),
        }
    matrix_rows = []
    adjusted_rhs = []
    for row, value in zip(rows, rhs):
        matrix_rows.append([row[col] for col in pivot_cols])
        adjusted_rhs.append(value - sum(row[col] * fixed for col, fixed in free_assignments.items()))
    A = Matrix(F, matrix_rows, ncols=len(pivot_cols))
    rank = int(A.rank())
    if rank < len(pivot_cols):
        return None, {
            "status": "PIN_INCONSISTENT",
            "reason": "singular_scheduled_pivot_minor",
            "pivot_minor_rank": rank,
            "pivot_minor_size": len(pivot_cols),
        }
    solution = list(A.solve_right(vector(F, adjusted_rhs)))
    vec = [F(0)] * VARIABLE_COUNT
    for col, fixed in free_assignments.items():
        vec[int(col)] = fixed
    for col, value in zip(pivot_cols, solution):
        vec[int(col)] = value
    return vec, {
        "status": "PINNED_SOLVE_OK",
        "pivot_minor_rank": rank,
        "pivot_minor_size": len(pivot_cols),
    }


def audit_system(scanner, system, F, powers, generator, budget):
    source_row = scanner.source_proxy_row_by_id()[system["system_id"]]
    _source, _base, selected = scanner.proxy.reconstruct_selected(source_row)
    exact_rows = rows_for_selected(F, powers, selected["selected"])
    subsets = row_subset_map(scanner, selected)
    base_vec = solve_base_degenerate(F, exact_rows, system, subsets["dominant_collision_rows_64"])
    base_values = exact_values_from_vector(F, powers, base_vec)
    base_class_rows = class_masks_by_position(base_values)
    safe_positions = diverse_safe_positions(base_class_rows, 16)
    protected_count = sum(1 for masks in base_class_rows if max(int(mask).bit_count() for mask in masks) == 7)
    evaluations = []
    for subset_name in ROW_SUBSETS:
        target_indices = subsets[subset_name]
        target_rows = [exact_rows[int(idx)] for idx in target_indices]
        target_rhs = [F(0)] * len(target_rows)
        free_assignments = {int(col): F(1) for col in proxy_support_columns(system)}
        for family in SEPARATION_FAMILIES:
            if len(evaluations) >= budget:
                break
            sep_rows, sep_rhs, specs = separation_pins(F, powers, family, safe_positions, generator)
            for pivot_schedule in PIVOT_SCHEDULES:
                if len(evaluations) >= budget:
                    break
                pivots = pivot_columns(system, len(target_rows), len(sep_rows), specs, pivot_schedule)
                sol, solve = solve_scheduled_system(
                    F,
                    target_rows + sep_rows,
                    target_rhs + sep_rhs,
                    pivots,
                    free_assignments,
                )
                evaluation = None if sol is None else evaluate_vector(F, powers, sol)
                evaluations.append(
                    {
                        "subset": subset_name,
                        "target_rows": len(target_rows),
                        "fixed_proxy_support_coefficients": len(free_assignments),
                        "separation_family": family,
                        "pivot_schedule": pivot_schedule,
                        "separation_pins": specs,
                        "solve": solve,
                        "evaluation": evaluation,
                    }
                )
        if len(evaluations) >= budget:
            break
    hist = {}
    for row in evaluations:
        status = row["evaluation"]["status"] if row["evaluation"] is not None else row["solve"]["status"]
        hist[status] = hist.get(status, 0) + 1
    exact_hits = [row for row in evaluations if row["evaluation"] is not None and row["evaluation"]["status"] == "CANDIDATE_A327"]
    cap_preserving = [
        row
        for row in evaluations
        if row["evaluation"] is not None
        and row["evaluation"]["distinct_codewords"]
        and row["evaluation"]["capacity_upper_bound"] >= TARGET_AGREEMENT
    ]
    best = max(
        evaluations,
        key=lambda row: (
            -1 if row["evaluation"] is None or row["evaluation"]["assignment"] is None else row["evaluation"]["assignment"]["exact_max_min"],
            -1 if row["evaluation"] is None else row["evaluation"]["capacity_upper_bound"],
            1 if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"] else 0,
        ),
    )
    return {
        "system_id": system["system_id"],
        "source_proxy_best_max_min": system["source_proxy_best_max_min"],
        "dominant_skeleton": {
            "base_capacity_upper_bound": capacity_from_class_masks(base_class_rows)["capacity_upper_bound"],
            "protected_all_seven_coordinates": protected_count,
            "safe_separation_coordinates": len(safe_positions),
            "safe_positions_hash": hash_payload(safe_positions),
        },
        "evaluations": evaluations,
        "pin_sets_tested": len(evaluations),
        "exact_vectors_constructed": sum(1 for row in evaluations if row["evaluation"] is not None),
        "nondegenerate_vectors": sum(1 for row in evaluations if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"]),
        "capacity_preserving_nondegenerate_vectors": len(cap_preserving),
        "exact_a327_vectors": len(exact_hits),
        "failure_histogram": dict(sorted(hist.items())),
        "best": best,
        "status": "CANDIDATE_A327" if exact_hits else "EXACT_EXTRACTION_NO_A327",
    }


def audit_record():
    scanner = load_module(SCANNER_PATH, "robust_proxy_scanner")
    with ROBUST_DATA_PATH.open() as handle:
        robust = json.load(handle)
    with BASELINE_PATH.open() as handle:
        baseline = json.load(handle)
    q, F, H, generator = field_context()
    powers = precompute_powers(F, H)
    systems = sorted(
        robust["systems"],
        key=lambda row: (
            row["best_schedule"]["candidate_prime_count"],
            row["pivot_stability_score"],
            row["source_proxy_best_max_min"],
            row["system_id"],
        ),
        reverse=True,
    )[:SYSTEM_LIMIT]
    per_system_budget = max(1, MAX_EVALUATIONS // len(systems))
    results = [audit_system(scanner, system, F, powers, generator, per_system_budget) for system in systems]
    all_evals = [row for result in results for row in result["evaluations"]]
    exact_hits = sum(result["exact_a327_vectors"] for result in results)
    cap_preserving = sum(result["capacity_preserving_nondegenerate_vectors"] for result in results)

    def floor(row):
        if row["evaluation"] is None or row["evaluation"]["assignment"] is None:
            return -1
        return row["evaluation"]["assignment"]["exact_max_min"]

    best = max(
        all_evals,
        key=lambda row: (
            floor(row),
            -1 if row["evaluation"] is None else row["evaluation"]["capacity_upper_bound"],
            1 if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"] else 0,
        ),
    )
    best_assignment = None if best["evaluation"] is None else best["evaluation"]["assignment"]
    best_failure = best["evaluation"]["status"] if best["evaluation"] is not None else best["solve"]["status"]
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "source_commit": SOURCE_COMMIT,
            "construction_mode": "dominant_collision_preserving_separation",
            "baseline": {
                "best_degenerate_capacity_upper_bound": baseline["baseline"]["best_high_capacity_degenerate_capacity"],
                "best_pinned_nondegenerate_capacity_upper_bound": baseline["pin_search"]["best_capacity_upper_bound"],
                "baseline_result_hash": baseline["result_hash"],
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "dominant_collision_skeletons": {
                "systems_tested": len(results),
                "skeletons_tested": len(results),
                "protected_rows": sum(result["dominant_skeleton"]["protected_all_seven_coordinates"] for result in results),
                "safe_separation_coordinates": sum(result["dominant_skeleton"]["safe_separation_coordinates"] for result in results),
            },
            "separation_search": {
                "pin_sets_tested": len(all_evals),
                "exact_vectors_constructed": sum(result["exact_vectors_constructed"] for result in results),
                "nondegenerate_vectors": sum(result["nondegenerate_vectors"] for result in results),
                "capacity_preserving_nondegenerate_vectors": cap_preserving,
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
            "proof_status": "CANDIDATE" if exact_hits else "EXACT_EXTRACTION_NO_A327",
            "result_hash": hash_payload(results),
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
        print("SAGE_AUDIT_M1_A327_DOMINANT_COLLISION_PRESERVING_SEPARATION_OK")
        print("pin_sets_tested: %d" % record["separation_search"]["pin_sets_tested"])
        print("capacity_preserving_nondegenerate_vectors: %d" % record["separation_search"]["capacity_preserving_nondegenerate_vectors"])
        print("best_exact_max_min: %s" % record["separation_search"]["best_exact_max_min"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
