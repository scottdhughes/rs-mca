#!/usr/bin/env sage
"""Exact GF(17^32) bounded audit for robust proxy constrained extraction."""

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

SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_robust_proxy_constrained_extraction.py")
SOURCE_DATA_PATH = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
DATA_PATH = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction_exact_audit.json")

ROW_SUBSETS = ["proxy_pivot_rows_64", "fiber_diverse_rows_64"]
PARTIAL_SOLVE_ROW_SUBSET = "proxy_pivot_rows_64"
PARTIAL_SOLVE_PIVOT_COUNT = 64


def load_scanner():
    script_dir = str(SCANNER_PATH.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location("robust_proxy_constrained_scanner", SCANNER_PATH)
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


def exact_values_from_vector(F, powers, vector):
    values = [[F(0) for _ in range(N)]]
    for witness in range(DIFF_COUNT):
        start = witness * K
        witness_values = [F(0) for _ in range(N)]
        for degree in range(K):
            coeff = vector[start + degree]
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

    def feasible(floor):
        objective = np.zeros(total_vars)
        bounds = Bounds(np.zeros(total_vars), np.ones(total_vars))
        integrality = np.ones(total_vars)
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
            lower.append(floor)
            upper.append(np.inf)
        result = milp(
            objective,
            integrality=integrality,
            bounds=bounds,
            constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
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


def evaluate_vector(F, powers, vector):
    values = exact_values_from_vector(F, powers, vector)
    hashes = value_hashes(values)
    distinct = len(set(hashes)) == LIST_SIZE
    class_rows = class_masks_by_position(values)
    capacity = capacity_from_class_masks(class_rows)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = assignment_max_min(class_rows)
    return {
        "distinct_codewords": distinct,
        "codeword_value_hash": hash_payload(hashes),
        **capacity,
        "assignment": assignment,
        "status": "EXACT_A327_ASSIGNMENT"
        if distinct and assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT
        else "EXACT_HIGH_CAPACITY_IMBALANCED"
        if distinct and assignment is not None
        else "EXACT_DEGENERATE_CODEWORDS"
        if not distinct
        else "EXACT_LOW_CAPACITY",
    }


def partial_solve_vector(F, exact_rows, system):
    row_indices = system["row_subset_candidates"][PARTIAL_SOLVE_ROW_SUBSET][:PARTIAL_SOLVE_PIVOT_COUNT]
    pivot_cols = system["common_pivot_columns"][:PARTIAL_SOLVE_PIVOT_COUNT]
    schedule = system["best_schedule"]
    free_cols = [int(col) for col in schedule["free_columns"]]
    matrix_rows = []
    rhs = []
    for row_idx in row_indices:
        row = exact_rows[row_idx]
        matrix_rows.append([row[col] for col in pivot_cols])
        rhs.append(-sum(row[col] for col in free_cols))
    A = Matrix(F, matrix_rows, ncols=len(pivot_cols))
    if A.rank() < len(pivot_cols):
        return None, "SINGULAR_PARTIAL_PIVOT_MINOR"
    solution = list(A.solve_right(vector(F, rhs)))
    vec = [F(0)] * VARIABLE_COUNT
    for col in free_cols:
        vec[col] = F(1)
    for col, value in zip(pivot_cols, solution):
        vec[col] = value
    return vec, "PARTIAL_SOLVE_OK"


def audit_system(scanner, source_record, system, F, powers):
    source_row = scanner.source_proxy_row_by_id()[system["system_id"]]
    _source, _base, selected = scanner.proxy.reconstruct_selected(source_row)
    exact_rows = rows_for_selected(F, powers, selected["selected"])
    subset_results = []
    for subset_name in ROW_SUBSETS:
        row_indices = system["row_subset_candidates"][subset_name]
        matrix = Matrix(F, [exact_rows[idx] for idx in row_indices], ncols=VARIABLE_COUNT)
        rank = int(matrix.rank())
        subset_results.append(
            {
                "subset": subset_name,
                "rows": len(row_indices),
                "rank": rank,
                "full_row_rank": rank == len(row_indices),
            }
        )
    vector_value, solve_status = partial_solve_vector(F, exact_rows, system)
    if vector_value is None:
        direct_eval = None
    else:
        direct_eval = evaluate_vector(F, powers, vector_value)
    return {
        "system_id": system["system_id"],
        "source_proxy_best_max_min": system["source_proxy_best_max_min"],
        "source_proxy_best_agreement": system["source_proxy_best_agreement"],
        "pivot_stability_score": system["pivot_stability_score"],
        "common_pivot_count": system["common_pivot_count"],
        "common_free_count": system["common_free_count"],
        "best_schedule_id": system["best_schedule"]["schedule_id"],
        "best_schedule_candidate_prime_count": system["best_schedule"]["candidate_prime_count"],
        "row_subset_rank_results": subset_results,
        "row_subset_rank_drop_found": any(not row["full_row_rank"] for row in subset_results),
        "partial_solve": {
            "row_subset": PARTIAL_SOLVE_ROW_SUBSET,
            "rows": PARTIAL_SOLVE_PIVOT_COUNT,
            "free_column_count": len(system["best_schedule"]["free_columns"]),
            "status": solve_status,
            "direct_evaluation": direct_eval,
        },
        "status": "EXACT_PARTIAL_SOLVE_A327"
        if direct_eval is not None and direct_eval["status"] == "EXACT_A327_ASSIGNMENT"
        else "EXACT_PARTIAL_SOLVE_NO_A327",
    }


def audit_record():
    scanner = load_scanner()
    with SOURCE_DATA_PATH.open() as handle:
        source = json.load(handle)
    q, F, H = field_context()
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
    )[:1]
    results = [audit_system(scanner, source, system, F, powers) for system in systems]
    exact_hits = sum(1 for row in results if row["status"] == "EXACT_PARTIAL_SOLVE_A327")
    rank_drops = sum(1 for row in results if row["row_subset_rank_drop_found"])
    proof_status = "CANDIDATE" if exact_hits else "EXACT_CONSTRAINED_EXTRACTION_NO_A327"
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "robust_proxy_constrained_extraction_exact_audit",
            "source": {
                "source_json": str(SOURCE_DATA_PATH),
                "source_result_hash": source["result_hash"],
                "source_proof_status": source["proof_status"],
                "source_system_count": source["system_count"],
                "source_constrained_schedule_proxy_positive_system_count": source[
                    "constrained_schedule_proxy_positive_system_count"
                ],
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "degree_bound": K,
            "row_subsets": ROW_SUBSETS,
            "partial_solve_row_subset": PARTIAL_SOLVE_ROW_SUBSET,
            "exact_audited_system_count": len(results),
            "exact_partial_solve_a327_count": exact_hits,
            "row_subset_rank_drop_count": rank_drops,
            "results": results,
            "result_hash": hash_payload(results),
            "proof_status": proof_status,
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list proof record",
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
        print("SAGE_AUDIT_M1_A327_ROBUST_PROXY_CONSTRAINED_EXTRACTION_OK")
        print("exact_audited_system_count: %d" % record["exact_audited_system_count"])
        print("exact_partial_solve_a327_count: %d" % record["exact_partial_solve_a327_count"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
