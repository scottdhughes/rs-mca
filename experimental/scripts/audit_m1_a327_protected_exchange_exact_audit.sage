#!/usr/bin/env sage
"""Exact GF(17^32) audit for protected-exchange proxy candidates."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path

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

SCAN_PATH = Path("experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py")
DATA_PATH = Path("experimental/data/m1_a327_protected_exchange_exact_audit.json")

ROW_SCHEDULES = [
    "protected_rows_only",
    "protected_plus_exchange_rows",
    "selected_prefix_128",
    "selected_prefix_256",
]
FREE_PATTERNS = [
    "proxy_mod17_support",
    "proxy_sparse_64",
    "blockwise_constants",
]


def load_scan_module():
    script_dir = str(SCAN_PATH.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location("protected_exchange_exact_scan", SCAN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def jsonable(payload):
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


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def members(mask):
    return [idx for idx in range(LIST_SIZE) if int(mask) & (1 << idx)]


def constraint_rows_for_coordinate(F, powers, coord):
    bits = members(coord["mask"])
    pos = int(coord["position"])
    rows = []
    metas = []
    if 0 in bits:
        for witness in bits:
            if witness == 0:
                continue
            row = [F(0)] * VARIABLE_COUNT
            start = (witness - 1) * K
            for degree in range(K):
                row[start + degree] = powers[degree][pos]
            rows.append(row)
            metas.append(coord)
        return rows, metas
    if len(bits) < 2:
        return rows, metas
    left = bits[0]
    left_start = (left - 1) * K
    for witness in bits[1:]:
        row = [F(0)] * VARIABLE_COUNT
        right_start = (witness - 1) * K
        for degree in range(K):
            row[left_start + degree] = powers[degree][pos]
            row[right_start + degree] = -powers[degree][pos]
        rows.append(row)
        metas.append(coord)
    return rows, metas


def expanded_rows_for_selected(F, powers, selected):
    rows = []
    metas = []
    for coord in selected:
        coord_rows, coord_metas = constraint_rows_for_coordinate(F, powers, coord)
        rows.extend(coord_rows)
        metas.extend(coord_metas)
    if not rows:
        raise RuntimeError("empty exact target row set")
    return rows, metas


def row_indices_for_schedule(name, metas):
    if name == "protected_rows_only":
        return [idx for idx, meta in enumerate(metas) if meta["source"] == "pair7_repair"]
    if name == "protected_plus_exchange_rows":
        return [
            idx
            for idx, meta in enumerate(metas)
            if meta["source"] in {"pair7_repair", "protected_exchange_repair"}
        ]
    if name == "selected_prefix_128":
        return list(range(min(128, len(metas))))
    if name == "selected_prefix_256":
        return list(range(min(256, len(metas))))
    raise ValueError(f"unknown row schedule: {name}")


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


def hall_contribution(classes, subset_mask):
    return max((int(mask) & int(subset_mask)).bit_count() for mask in classes)


def pair7_metrics(class_rows):
    pair_masks = [
        (1 << 0) | (1 << 6),
        (1 << 1) | (1 << 6),
        (1 << 2) | (1 << 6),
        (1 << 3) | (1 << 6),
        (1 << 4) | (1 << 6),
    ]
    pair_b = []
    for subset in pair_masks:
        pair_b.append(sum(hall_contribution(classes, subset) for classes in class_rows))
    return {
        "pair_B_values": pair_b,
        "min_pair_B": min(pair_b),
        "pair_deficit_to_654": [2 * TARGET_AGREEMENT - value for value in pair_b],
        "pair_hall_bound": min(value // 2 for value in pair_b),
    }


def old_three_subset_metrics(class_rows):
    masks = [
        (1 << 0) | (1 << 1) | (1 << 2),
        (1 << 1) | (1 << 2) | (1 << 3),
        (1 << 1) | (1 << 2) | (1 << 4),
    ]
    values = []
    for subset in masks:
        values.append(sum(hall_contribution(classes, subset) for classes in class_rows))
    return {
        "old_three_subset_B_values": values,
        "old_three_subset_min_hall_bound": min(value // 3 for value in values),
    }


def six_class_dominance(class_rows):
    collapse_mask = 0
    for witness in [1, 3, 4, 5, 6, 7]:
        collapse_mask |= 1 << (witness - 1)
    return sum(1 for classes in class_rows if collapse_mask in classes)


def assignment_max_min(class_rows):
    offsets = []
    total_vars = 0
    for classes in class_rows:
        offsets.append(total_vars)
        total_vars += len(classes)

    base_rows = []
    lower = []
    upper = []
    for pos, classes in enumerate(class_rows):
        row = np.zeros(total_vars)
        row[offsets[pos] : offsets[pos] + len(classes)] = 1
        base_rows.append(row)
        lower.append(1)
        upper.append(1)
    for witness in range(LIST_SIZE):
        row = np.zeros(total_vars)
        for pos, classes in enumerate(class_rows):
            for idx, mask in enumerate(classes):
                if int(mask) & (1 << witness):
                    row[offsets[pos] + idx] = 1
        base_rows.append(row)
        lower.append(0)
        upper.append(np.inf)
    matrix = np.vstack(base_rows)
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
            options={"time_limit": 15},
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


def classify_evaluation(distinct, capacity, pair_metrics, six_dom, assignment):
    if not distinct:
        return "DEGENERATE_CODEWORDS"
    if capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "CAPACITY_LOSS"
    if pair_metrics["min_pair_B"] < 2 * TARGET_AGREEMENT:
        return "PAIR7_REPAIR_LOST"
    if six_dom > 20:
        return "COLLAPSE_RETURNS"
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "EXACT_CANDIDATE_A327"
    if assignment is not None:
        return "LOW_RESCHEDULE"
    return "ASSIGNMENT_UNSOLVED"


def evaluate_vector(F, powers, vector_value, construction):
    values = exact_values_from_vector(F, powers, vector_value)
    hashes = value_hashes(values)
    distinct = len(set(hashes)) == LIST_SIZE
    class_rows = class_masks_by_position(values)
    capacity = capacity_from_class_masks(class_rows)
    pair_metrics = pair7_metrics(class_rows)
    old_three = old_three_subset_metrics(class_rows)
    six_dom = six_class_dominance(class_rows)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = assignment_max_min(class_rows)
    failure = classify_evaluation(distinct, capacity, pair_metrics, six_dom, assignment)
    return {
        "construction": construction,
        "distinct_codewords": distinct,
        "codeword_value_hash": hash_payload(hashes),
        **capacity,
        **pair_metrics,
        **old_three,
        "six_class_dominance": six_dom,
        "exact_max_min": None if assignment is None else assignment["exact_max_min"],
        "exact_agreement_vector": None if assignment is None else assignment["agreement_vector"],
        "chosen_masks_hash": None if assignment is None else assignment["chosen_masks_hash"],
        "failure_mode": failure,
    }


def direct_proxy_vector(F, proxy_vector):
    return [F(Integer(int(value) % P)) for value in proxy_vector]


def free_assignments(F, pattern, proxy_vector, pivot_cols):
    pivot_set = set(int(col) for col in pivot_cols)
    free_cols = [col for col in range(VARIABLE_COUNT) if col not in pivot_set]
    proxy_support = [col for col in free_cols if int(proxy_vector[col]) % P != 0]
    assignments = {}
    if pattern == "proxy_mod17_support":
        for col in proxy_support:
            assignments[col] = F(Integer(int(proxy_vector[col]) % P))
    elif pattern == "proxy_sparse_64":
        for idx, col in enumerate(proxy_support[:64]):
            assignments[col] = F(Integer((idx % (P - 1)) + 1))
    elif pattern == "blockwise_constants":
        for col in proxy_support:
            block = col // K
            if col % 8 == 0:
                assignments[col] = F(Integer(block + 1))
    else:
        raise ValueError(f"unknown free pattern: {pattern}")
    if not assignments and free_cols:
        assignments[free_cols[0]] = F(1)
    return assignments


def solve_schedule_vector(F, exact_rows, row_indices, pivot_cols, proxy_vector, pattern):
    row_count = len(row_indices)
    pivot_cols = [int(col) for col in pivot_cols[:row_count]]
    if len(pivot_cols) != row_count:
        return None, "INSUFFICIENT_EXACT_PIVOTS"
    matrix_rows = [[exact_rows[row_idx][col] for col in pivot_cols] for row_idx in row_indices]
    A = Matrix(F, matrix_rows, ncols=len(pivot_cols))
    rank = int(A.rank())
    if rank < row_count:
        return None, "SINGULAR_EXACT_PIVOT_MINOR"
    assignments = free_assignments(F, pattern, proxy_vector, pivot_cols)
    rhs = []
    for row_idx in row_indices:
        total = F(0)
        row = exact_rows[row_idx]
        for col, value in assignments.items():
            total += row[col] * value
        rhs.append(-total)
    sol = A.solve_right(vector(F, rhs))
    out = [F(0)] * VARIABLE_COUNT
    for col, value in assignments.items():
        out[col] = value
    for idx, col in enumerate(pivot_cols):
        out[col] = sol[idx]
    if all(value == 0 for value in out):
        return None, "ZERO_VECTOR"
    return out, "EXACT_VECTOR_CONSTRUCTED"


def rank_schedule(F, exact_rows, row_indices):
    if not row_indices:
        return {
            "rows": 0,
            "rank": 0,
            "full_row_rank": False,
        }
    matrix = Matrix(F, [exact_rows[idx] for idx in row_indices], ncols=VARIABLE_COUNT)
    rank = int(matrix.rank())
    pivots = [int(col) for col in matrix.pivots()]
    return {
        "rows": len(row_indices),
        "rank": rank,
        "full_row_rank": rank == len(row_indices),
        "pivot_columns": pivots[: len(row_indices)],
        "pivot_columns_hash": hash_payload(pivots[: len(row_indices)]),
    }


def evaluate_candidate(scan, row, F, powers):
    reconstructed = scan.reconstruct_candidate(row)
    exact_rows, metas = expanded_rows_for_selected(F, powers, reconstructed["selected"])
    schedule_indices = {name: row_indices_for_schedule(name, metas) for name in ROW_SCHEDULES}
    rank_results = []
    vector_results = []
    for name, indices in schedule_indices.items():
        rank_result = rank_schedule(F, exact_rows, indices)
        rank_result["row_schedule"] = name
        rank_results.append(rank_result)
        if not rank_result["full_row_rank"]:
            continue
        for pattern in FREE_PATTERNS:
            vector_value, status = solve_schedule_vector(
                F,
                exact_rows,
                indices,
                rank_result["pivot_columns"],
                reconstructed["proxy_vector"],
                pattern,
            )
            if vector_value is None:
                vector_results.append(
                    {
                        "row_schedule": name,
                        "free_pattern": pattern,
                        "construction": status,
                        "failure_mode": status,
                    }
                )
                continue
            vector_results.append(
                evaluate_vector(
                    F,
                    powers,
                    vector_value,
                    {
                        "row_schedule": name,
                        "free_pattern": pattern,
                        "solve_status": status,
                    },
                )
            )
    direct = evaluate_vector(
        F,
        powers,
        direct_proxy_vector(F, reconstructed["proxy_vector"]),
        {"row_schedule": "direct_proxy_mod17", "free_pattern": "proxy_vector_mod17", "solve_status": "DIRECT_MAP"},
    )
    vector_results.append(direct)
    best = sorted(vector_results, key=vector_sort_key, reverse=True)[0]
    return {
        "candidate_id": row["target_system_id"],
        "proxy_max_min": row["best"]["proxy_max_min"],
        "proxy_agreement_vector": row["best"]["agreement_vector"],
        "proxy_capacity_upper_bound": row["best"]["capacity_upper_bound"],
        "proxy_pair_B_values": row["best"]["pair7_B_values"],
        "proxy_added_six_class_dominance": row["best"]["six_class_dominance_added_by_repair"],
        "target_row_count": row["target_row_count"],
        "target_rows_hash": row["target_rows_hash"],
        "proxy_codeword_tuple_hash": row["best"]["vector_hash"],
        "row_schedule_ranks": rank_results,
        "vector_attempt_count": len(vector_results),
        "best": best,
        "vector_results": vector_results,
        "retained_vector_results": sorted(vector_results, key=vector_sort_key, reverse=True)[:8],
    }


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    return (
        row.get("failure_mode") == "EXACT_CANDIDATE_A327",
        exact_max,
        row.get("min_pair_B", -1),
        row.get("capacity_upper_bound", -1),
        row.get("distinct_codewords") is True,
        -row.get("six_class_dominance", 10**9),
    )


def audit_record():
    scan = load_scan_module()
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    source = scan.source_record()
    candidates = scan.proxy_candidate_rows(source)
    results = [evaluate_candidate(scan, row, F, powers) for row in candidates]
    vectors = [row for result in results for row in result["retained_vector_results"]]
    best = sorted(vectors, key=vector_sort_key, reverse=True)[0] if vectors else None
    exact_audit = {
        "exact_field": "GF(17^32)",
        "field_denominator": str(q),
        "subgroup_order": N,
        "candidates_tested": len(results),
        "row_schedules_tested": sum(len(result["row_schedule_ranks"]) for result in results),
        "free_schedules_tested": len(candidates) * len(ROW_SCHEDULES) * len(FREE_PATTERNS),
        "exact_vectors_constructed": sum(
            1
            for result in results
            for row in result["vector_results"]
            if row.get("distinct_codewords") is not None
        ),
        "nondegenerate_vectors": sum(
            1
            for result in results
            for row in result["vector_results"]
            if row.get("distinct_codewords") is True
        ),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_exact_agreement_vector": None if best is None else best.get("exact_agreement_vector"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    record = scan.build_record(exact_audit=exact_audit)
    record["result_hash"] = hash_payload(results)
    return jsonable(record)


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
        print("SAGE_AUDIT_M1_A327_PROTECTED_EXCHANGE_EXACT_AUDIT_OK")
        print("candidates_tested: %d" % record["exact_audit"]["candidates_tested"])
        print("best_exact_max_min: %s" % record["exact_audit"]["best_exact_max_min"])
        print("best_failure_mode: %s" % record["exact_audit"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
