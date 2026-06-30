#!/usr/bin/env sage
"""Exact residual [1,2] split and pinned-nullspace audit."""

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

EXACT_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_residual_12_split_pinned_nullspace.py")
DATA_PATH = Path("experimental/data/m1_a327_residual_12_split_pinned_nullspace.json")

RESIDUAL_COORD_LIMIT = 4
GAMMAS = [1, 2, 3, 4]
FREE_PATTERNS = [
    "affine_pivot_solution",
    "d2_first_free",
    "d2_first4_free",
    "d2_even_sparse",
]


def load_module(path, module_name):
    script_dir = str(path.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(module_name, path)
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


def coefficient_row_for_coordinate(F, powers, coord):
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


def expanded_rows(F, powers, selected):
    rows = []
    metas = []
    for coord in selected:
        coord_rows, coord_metas = coefficient_row_for_coordinate(F, powers, coord)
        rows.extend(coord_rows)
        metas.extend(coord_metas)
    if not rows:
        raise RuntimeError("empty exact target row set")
    return rows, metas


def protected_exchange_indices(metas):
    return [
        idx
        for idx, meta in enumerate(metas)
        if meta["source"] in {"pair7_repair", "protected_exchange_repair"}
    ]


def evaluation_row(F, powers, left, right, pos):
    row = [F(0)] * VARIABLE_COUNT
    if left >= 2:
        start = (left - 2) * K
        for degree in range(K):
            row[start + degree] += powers[degree][pos]
    if right >= 2:
        start = (right - 2) * K
        for degree in range(K):
            row[start + degree] -= powers[degree][pos]
    return row


def quotient_round_order():
    return [fiber + 16 * offset for offset in range(32) for fiber in range(16)]


def safe_positions(selected):
    all_used = {int(row["position"]) for row in selected}
    repair_used = {
        int(row["position"])
        for row in selected
        if row["source"] in {"pair7_repair", "protected_exchange_repair"}
    }
    primary = [pos for pos in quotient_round_order() if pos not in all_used]
    if len(primary) >= RESIDUAL_COORD_LIMIT:
        return primary
    return [pos for pos in quotient_round_order() if pos not in repair_used]


def anchor_split_specs(selected):
    positions = safe_positions(selected)
    pairs = [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
    return [
        {
            "left": left,
            "right": right,
            "position": int(positions[idx]),
            "gamma": int(idx + 1),
            "kind": "anchor_split",
        }
        for idx, (left, right) in enumerate(pairs)
    ]


def residual12_specs(selected):
    positions = safe_positions(selected)
    specs = []
    for pos in positions[:RESIDUAL_COORD_LIMIT]:
        for gamma in GAMMAS:
            specs.append(
                {
                    "left": 2,
                    "right": 1,
                    "position": int(pos),
                    "gamma": int(gamma),
                    "kind": "residual12",
                }
            )
    return specs


def pin_rows(F, powers, specs):
    rows = []
    rhs = []
    for spec in specs:
        rows.append(evaluation_row(F, powers, spec["left"], spec["right"], spec["position"]))
        rhs.append(F(Integer(spec["gamma"])))
    return rows, rhs


def free_assignments(F, pattern, pivots):
    pivot_set = set(int(col) for col in pivots)
    free_cols = [col for col in range(VARIABLE_COUNT) if col not in pivot_set]
    d2_free = [col for col in free_cols if 0 <= col < K]
    out = {}
    if pattern == "affine_pivot_solution":
        return out
    if not d2_free:
        return out
    if pattern == "d2_first_free":
        out[d2_free[0]] = F(1)
    elif pattern == "d2_first4_free":
        for idx, col in enumerate(d2_free[:4]):
            out[col] = F(Integer(idx + 1))
    elif pattern == "d2_even_sparse":
        chosen = [col for col in d2_free if col % 2 == 0][:8]
        for idx, col in enumerate(chosen):
            out[col] = F(Integer((idx % (P - 1)) + 1))
    else:
        raise ValueError("unknown free pattern: %s" % pattern)
    return out


def solve_with_free(F, rows, rhs, free_values):
    A = Matrix(F, rows, ncols=VARIABLE_COUNT)
    b = vector(F, rhs)
    pivots = [int(col) for col in A.pivots()]
    if len(pivots) < len(rows):
        return None, "RESIDUAL12_PIN_INCONSISTENT", "dependent or inconsistent row system", pivots
    adjusted = []
    for row_idx, row in enumerate(rows):
        total = F(0)
        for col, value in free_values.items():
            total += row[col] * value
        adjusted.append(b[row_idx] - total)
    pivot_matrix = A.matrix_from_columns(pivots[: len(rows)])
    try:
        sol = pivot_matrix.solve_right(vector(F, adjusted))
    except Exception as exc:
        return None, "RESIDUAL12_PIN_INCONSISTENT", str(exc), pivots
    x = [F(0)] * VARIABLE_COUNT
    for col, value in free_values.items():
        x[col] = value
    for idx, col in enumerate(pivots[: len(rows)]):
        x[col] = sol[idx]
    if all(value == 0 for value in x):
        return None, "RESIDUAL12_PIN_DOES_NOT_SPLIT", "zero solution", pivots
    return x, "EXACT_VECTOR_CONSTRUCTED", None, pivots


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


def equivalence_classes(values):
    hashes = value_hashes(values)
    by_hash = {}
    for idx, digest in enumerate(hashes):
        by_hash.setdefault(digest, []).append(idx + 1)
    return sorted(by_hash.values(), key=lambda row: (len(row), row), reverse=True)


def classify(distinct, degenerate_classes, capacity, pair_metrics, assignment):
    if not distinct:
        if [1, 2] in degenerate_classes:
            return "RESIDUAL12_PIN_DOES_NOT_SPLIT"
        return "RESIDUAL12_PIN_DOES_NOT_SPLIT"
    if capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "RESIDUAL12_SPLIT_CAPACITY_LOSS"
    if pair_metrics["min_pair_B"] < 2 * TARGET_AGREEMENT:
        return "RESIDUAL12_SPLIT_PAIR7_LOSS"
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "RESIDUAL12_EXACT_CANDIDATE"
    if assignment is not None:
        return "RESIDUAL12_SPLIT_LOW_RESCHEDULE"
    return "ASSIGNMENT_UNSOLVED"


def evaluate_vector(F, powers, vector_value, metadata):
    values = exact_values_from_vector(F, powers, vector_value)
    classes = class_masks_by_position(values)
    capacity = capacity_from_class_masks(classes)
    pair_metrics = pair7_metrics(classes)
    eq = equivalence_classes(values)
    distinct = all(len(row) == 1 for row in eq)
    assignment = None
    if (
        distinct
        and capacity["capacity_upper_bound"] >= TARGET_AGREEMENT
        and pair_metrics["min_pair_B"] >= 2 * TARGET_AGREEMENT
    ):
        assignment = assignment_max_min(classes)
    failure = classify(distinct, eq, capacity, pair_metrics, assignment)
    return {
        **metadata,
        "distinct_codewords": distinct,
        "degenerate_classes": eq,
        **capacity,
        **pair_metrics,
        **old_three_subset_metrics(classes),
        "six_class_dominance": six_class_dominance(classes),
        "exact_max_min": None if assignment is None else assignment["exact_max_min"],
        "exact_agreement_vector": None if assignment is None else assignment["agreement_vector"],
        "chosen_masks_hash": None if assignment is None else assignment["chosen_masks_hash"],
        "failure_mode": failure,
    }


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    return (
        row.get("failure_mode") == "RESIDUAL12_EXACT_CANDIDATE",
        row.get("distinct_codewords") is True,
        exact_max,
        row.get("min_pair_B", -1),
        row.get("capacity_upper_bound", -1),
        -row.get("six_class_dominance", 10**9),
    )


def evaluate_candidate(exact_scan, row, F, powers):
    reconstructed = exact_scan.reconstruct_candidate(row)
    selected = reconstructed["selected"]
    exact_rows, metas = expanded_rows(F, powers, selected)
    target_rows = [exact_rows[idx] for idx in protected_exchange_indices(metas)]
    base_specs = anchor_split_specs(selected)
    base_pin_rows, base_rhs = pin_rows(F, powers, base_specs)
    base_rows = target_rows + base_pin_rows
    base_rhs_full = [F(0)] * len(target_rows) + base_rhs
    results = []

    # Sample the affine nullspace of the strongest split system.
    base_matrix = Matrix(F, base_rows, ncols=VARIABLE_COUNT)
    base_pivots = [int(col) for col in base_matrix.pivots()]
    for pattern in FREE_PATTERNS:
        free_values = free_assignments(F, pattern, base_pivots)
        vector_value, status, error, _pivots = solve_with_free(F, base_rows, base_rhs_full, free_values)
        metadata = {
            "candidate_id": row["target_system_id"],
            "search_layer": "pinned_nullspace_sample",
            "pin_family": "anchor_split_34567",
            "free_pattern": pattern,
            "pin_specs": base_specs,
            "solve_status": status,
        }
        if vector_value is None:
            results.append({**metadata, "failure_mode": status, "error": error})
            continue
        results.append(evaluate_vector(F, powers, vector_value, metadata))

    # Add targeted residual P_2(h)=gamma pins after the strongest split.
    for residual_spec in residual12_specs(selected):
        rows, rhs = pin_rows(F, powers, [residual_spec])
        vector_value, status, error, _pivots = solve_with_free(
            F,
            base_rows + rows,
            base_rhs_full + rhs,
            {},
        )
        metadata = {
            "candidate_id": row["target_system_id"],
            "search_layer": "residual_12_single_pin",
            "pin_family": "anchor_split_34567_plus_residual12",
            "residual_pin": residual_spec,
            "pin_specs": base_specs + [residual_spec],
            "solve_status": status,
        }
        if vector_value is None:
            results.append({**metadata, "failure_mode": status, "error": error})
            continue
        results.append(evaluate_vector(F, powers, vector_value, metadata))

    best = sorted(results, key=vector_sort_key, reverse=True)[0]
    return {
        "candidate_id": row["target_system_id"],
        "proxy_max_min": row["best"]["proxy_max_min"],
        "proxy_pair_B_values": row["best"]["pair7_B_values"],
        "attempt_count": len(results),
        "failure_mode_counts": failure_counts(results),
        "best": best,
        "vector_results": results,
        "retained_results": sorted(results, key=vector_sort_key, reverse=True)[:10],
    }


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    exact_scan = load_module(EXACT_SCAN_PATH, "protected_exchange_exact_scan")
    ledger_scan = load_module(LEDGER_SCAN_PATH, "residual12_ledger")
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    source = exact_scan.source_record()
    candidates = exact_scan.proxy_candidate_rows(source)
    results = [evaluate_candidate(exact_scan, row, F, powers) for row in candidates]
    attempts = [row for result in results for row in result["vector_results"]]
    best = sorted(attempts, key=vector_sort_key, reverse=True)[0] if attempts else None
    residual12 = {
        "exact_field": "GF(17^32)",
        "field_denominator": str(q),
        "pin_sets_tested": sum(
            1
            for result in results
            for row in result["vector_results"]
            if row.get("search_layer") == "residual_12_single_pin"
        ),
        "nullspace_samples_tested": sum(
            1
            for result in results
            for row in result["vector_results"]
            if row.get("search_layer") == "pinned_nullspace_sample"
        ),
        "exact_vectors_constructed": sum(
            1 for result in results for row in result["vector_results"] if row.get("distinct_codewords") is not None
        ),
        "nondegenerate_vectors": sum(
            1 for result in results for row in result["vector_results"] if row.get("distinct_codewords") is True
        ),
        "capacity_preserving_nondegenerate_vectors": sum(
            1
            for result in results
            for row in result["vector_results"]
            if row.get("distinct_codewords") is True and row.get("capacity_upper_bound", 0) >= TARGET_AGREEMENT
        ),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_degenerate_classes": None if best is None else best.get("degenerate_classes"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    record = ledger_scan.build_record(residual12_search=residual12)
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
        print("SAGE_AUDIT_M1_A327_RESIDUAL_12_SPLIT_PINNED_NULLSPACE_OK")
        print("pin_sets_tested: %d" % record["residual12_search"]["pin_sets_tested"])
        print("nullspace_samples_tested: %d" % record["residual12_search"]["nullspace_samples_tested"])
        print("nondegenerate_vectors: %d" % record["residual12_search"]["nondegenerate_vectors"])
        print("best_failure_mode: %s" % record["residual12_search"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
