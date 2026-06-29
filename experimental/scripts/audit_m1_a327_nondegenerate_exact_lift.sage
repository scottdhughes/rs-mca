#!/usr/bin/env sage
"""Bounded nondegenerate GF(17^32) lift audit for robust proxy systems."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
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
SOURCE_COMMIT = "f9a43ea"

SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_robust_proxy_constrained_extraction.py")
PLAN_PATH = Path("experimental/scripts/scan_m1_a327_nondegenerate_exact_lift.py")
SOURCE_DATA_PATH = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
DATA_PATH = Path("experimental/data/m1_a327_nondegenerate_exact_lift.json")

ROW_SUBSETS = [
    "proxy_pivot_rows_64",
    "fiber_diverse_rows_64",
    "deficit_rows_64",
    "full_target_row_sample_64",
    "proxy_pivot_rows_128",
]
VALUE_PATTERNS = ["all_ones", "blockwise_constants", "geometric_generator", "seeded_basefield"]
MAX_VECTOR_EVALUATIONS = 32


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
    nonzero_blocks = []
    coefficient_support_by_block = {}
    for block in range(DIFF_COUNT):
        start = block * K
        count = sum(1 for coeff in vector_value[start : start + K] if coeff != 0)
        coefficient_support_by_block[f"D_{block + 2}"] = count
        if count:
            nonzero_blocks.append(f"D_{block + 2}")
    class_rows = class_masks_by_position(values)
    capacity = capacity_from_class_masks(class_rows)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = assignment_max_min(class_rows)
    if not distinct:
        status = "DEGENERATE_CODEWORDS"
    elif capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        status = "LOW_CAPACITY"
    elif assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        status = "EXACT_A327_ASSIGNMENT"
    else:
        status = "LOW_RESCHEDULE"
    return {
        "distinct_codewords": distinct,
        "nonzero_witness_blocks": nonzero_blocks,
        "coefficient_support_by_block": coefficient_support_by_block,
        "codeword_value_hash": hash_payload(hashes),
        **capacity,
        "assignment": assignment,
        "status": status,
    }


def first_common_free_by_block(common_free, per_block):
    output = []
    for block in range(DIFF_COUNT):
        block_cols = [int(col) for col in common_free if int(col) // K == block]
        output.extend(block_cols[:per_block])
    return output


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


def proxy_support_free_columns(system):
    free = unique_in_order([int(col) for col in system["best_schedule"]["free_columns"]])
    common_free = set(int(col) for col in system["common_free_columns"])
    return [col for col in free if col in common_free]


def free_schedule_definitions(system):
    common_free = [int(col) for col in system["common_free_columns"]]
    proxy_support = proxy_support_free_columns(system)
    rng = random.Random(int(hash_payload([system["system_id"], "nondegenerate_free"])[:12], 16))
    random_common = list(common_free)
    rng.shuffle(random_common)
    definitions = [
        ("free_24_proxy_support", (proxy_support + common_free)[:24]),
        ("free_48_balanced_blocks", first_common_free_by_block(common_free, 8)),
        ("free_96_balanced_blocks", first_common_free_by_block(common_free, 16)),
        ("free_48_seeded_common", sorted(random_common[:48])),
    ]
    output = []
    seen = set()
    for schedule_id, columns in definitions:
        columns = unique_in_order(columns)
        digest = hash_payload(columns)
        if not columns or digest in seen:
            continue
        seen.add(digest)
        output.append({"schedule_id": schedule_id, "free_columns": columns})
    return output


def assignment_values(F, generator, schedule_id, pattern_id, columns):
    rng = random.Random(int(hash_payload([schedule_id, pattern_id, len(columns)])[:12], 16))
    assignments = {}
    for idx, col in enumerate(columns):
        block = int(col) // K
        if pattern_id == "all_ones":
            value = F(1)
        elif pattern_id == "blockwise_constants":
            value = F(block + 2)
        elif pattern_id == "geometric_generator":
            value = generator ** (1 + block * 37 + idx)
        elif pattern_id == "seeded_basefield":
            value = F(1 + rng.randrange(P - 1))
        else:
            raise ValueError(f"unknown value pattern {pattern_id}")
        assignments[int(col)] = value
    return assignments


def solve_partial_vector(F, exact_rows, row_indices, pivot_cols, free_assignments):
    matrix_rows = []
    rhs = []
    for row_idx in row_indices:
        row = exact_rows[int(row_idx)]
        matrix_rows.append([row[col] for col in pivot_cols])
        rhs.append(-sum(row[col] * value for col, value in free_assignments.items()))
    A = Matrix(F, matrix_rows, ncols=len(pivot_cols))
    rank = int(A.rank())
    if rank < len(pivot_cols):
        return None, {
            "status": "SINGULAR_PARTIAL_PIVOT_MINOR",
            "pivot_minor_rank": rank,
            "pivot_minor_size": len(pivot_cols),
        }
    solution = list(A.solve_right(vector(F, rhs)))
    vec = [F(0)] * VARIABLE_COUNT
    for col, value in free_assignments.items():
        vec[int(col)] = value
    for col, value in zip(pivot_cols, solution):
        vec[int(col)] = value
    return vec, {
        "status": "PARTIAL_SOLVE_OK",
        "pivot_minor_rank": rank,
        "pivot_minor_size": len(pivot_cols),
    }


def rank_subset(F, exact_rows, row_indices):
    matrix = Matrix(F, [exact_rows[int(idx)] for idx in row_indices], ncols=VARIABLE_COUNT)
    rank = int(matrix.rank())
    return {"rows": len(row_indices), "rank": rank, "full_row_rank": rank == len(row_indices)}


def failure_summary(evaluations):
    hist = {}
    for row in evaluations:
        status = row["evaluation"]["status"] if row.get("evaluation") else row["solve"]["status"]
        hist[status] = hist.get(status, 0) + 1
    return dict(sorted(hist.items()))


def audit_system(scanner, system, F, powers, generator):
    source_row = scanner.source_proxy_row_by_id()[system["system_id"]]
    _source, _base, selected = scanner.proxy.reconstruct_selected(source_row)
    exact_rows = rows_for_selected(F, powers, selected["selected"])
    row_subset_ranks = {}
    for subset_name in ["proxy_pivot_rows_64", "fiber_diverse_rows_64", "proxy_pivot_rows_128"]:
        if subset_name in system["row_subset_candidates"]:
            row_subset_ranks[subset_name] = rank_subset(F, exact_rows, system["row_subset_candidates"][subset_name])

    evaluations = []
    for subset_name in ROW_SUBSETS:
        if subset_name not in system["row_subset_candidates"]:
            continue
        row_indices = [int(idx) for idx in system["row_subset_candidates"][subset_name]]
        pivot_cols = [int(col) for col in system["common_pivot_columns"][: len(row_indices)]]
        for schedule in free_schedule_definitions(system):
            for pattern_id in VALUE_PATTERNS:
                if len(evaluations) >= MAX_VECTOR_EVALUATIONS:
                    break
                free_assignments = assignment_values(F, generator, schedule["schedule_id"], pattern_id, schedule["free_columns"])
                vec, solve = solve_partial_vector(F, exact_rows, row_indices, pivot_cols, free_assignments)
                evaluation = None if vec is None else evaluate_vector(F, powers, vec)
                evaluations.append(
                    {
                        "subset": subset_name,
                        "rows": len(row_indices),
                        "schedule_id": schedule["schedule_id"],
                        "free_column_count": len(schedule["free_columns"]),
                        "value_pattern": pattern_id,
                        "solve": solve,
                        "evaluation": evaluation,
                    }
                )
            if len(evaluations) >= MAX_VECTOR_EVALUATIONS:
                break
        if len(evaluations) >= MAX_VECTOR_EVALUATIONS:
            break

    best = max(
        evaluations,
        key=lambda row: (
            -1 if row["evaluation"] is None else row["evaluation"]["assignment"]["exact_max_min"]
            if row["evaluation"]["assignment"] is not None
            else -1,
            -1 if row["evaluation"] is None else row["evaluation"]["capacity_upper_bound"],
            1 if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"] else 0,
            row["subset"],
            row["schedule_id"],
            row["value_pattern"],
        ),
    )
    nondegenerate = [
        row
        for row in evaluations
        if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"]
    ]
    exact_hits = [
        row
        for row in evaluations
        if row["evaluation"] is not None and row["evaluation"]["status"] == "EXACT_A327_ASSIGNMENT"
    ]
    return {
        "system_id": system["system_id"],
        "source_proxy_best_max_min": system["source_proxy_best_max_min"],
        "source_proxy_best_agreement": system["source_proxy_best_agreement"],
        "pivot_stability_score": system["pivot_stability_score"],
        "common_pivot_count": system["common_pivot_count"],
        "common_free_count": system["common_free_count"],
        "best_schedule_id": system["best_schedule"]["schedule_id"],
        "row_subset_rank_results": row_subset_ranks,
        "exact_vectors_constructed": len(evaluations),
        "nondegenerate_vectors": len(nondegenerate),
        "exact_a327_vectors": len(exact_hits),
        "failure_histogram": failure_summary(evaluations),
        "best": best,
        "evaluations": evaluations,
        "status": "EXACT_A327_FOUND" if exact_hits else "EXACT_EXTRACTION_NO_A327",
    }


def audit_record():
    scanner = load_module(SCANNER_PATH, "robust_proxy_constrained_scanner")
    with SOURCE_DATA_PATH.open() as handle:
        source = json.load(handle)
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
    )[:1]
    results = [audit_system(scanner, system, F, powers, generator) for system in systems]
    exact_hits = sum(row["exact_a327_vectors"] for row in results)
    all_evaluations = [item for row in results for item in row["evaluations"]]
    nondegenerate_count = sum(
        1 for item in all_evaluations if item["evaluation"] is not None and item["evaluation"]["distinct_codewords"]
    )

    def eval_max_min(item):
        if item["evaluation"] is None or item["evaluation"]["assignment"] is None:
            return None
        return item["evaluation"]["assignment"]["exact_max_min"]

    best_eval = max(
        all_evaluations,
        key=lambda row: (
            -1 if eval_max_min(row) is None else eval_max_min(row),
            -1 if row["evaluation"] is None else row["evaluation"]["capacity_upper_bound"],
            1 if row["evaluation"] is not None and row["evaluation"]["distinct_codewords"] else 0,
        ),
    )
    best_assignment = None if best_eval["evaluation"] is None else best_eval["evaluation"]["assignment"]
    best_max_min = None if best_assignment is None else best_assignment["exact_max_min"]
    proof_status = "CANDIDATE" if exact_hits else "EXACT_EXTRACTION_NO_A327"
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "nondegenerate_exact_lift",
            "source": {
                "source_json": str(SOURCE_DATA_PATH),
                "source_commit": SOURCE_COMMIT,
                "source_result_hash": source["result_hash"],
                "source_proof_status": source["proof_status"],
                "source_system_count": source["system_count"],
                "source_best_proxy_max_min": source["best"]["best_schedule"]["best"]["assignment"]["exact_max_min"],
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "degree_bound": K,
            "proxy_systems": {
                "count": source["system_count"],
                "stable_pivot_columns": source["best"]["common_pivot_count"],
                "stable_free_columns": source["best"]["common_free_count"],
                "best_proxy_max_min": source["best"]["best_schedule"]["best"]["assignment"]["exact_max_min"],
            },
            "exact_lift_search": {
                "row_subsets_requested": ROW_SUBSETS,
                "value_patterns": VALUE_PATTERNS,
                "max_vector_evaluations": MAX_VECTOR_EVALUATIONS,
                "row_subsets_tested": len({item["subset"] for item in all_evaluations}),
                "free_schedules_tested": len({item["schedule_id"] for item in all_evaluations}),
                "value_patterns_tested": len({item["value_pattern"] for item in all_evaluations}),
                "exact_vectors_constructed": len(all_evaluations),
                "nondegenerate_vectors": nondegenerate_count,
                "best_capacity_upper_bound": None if best_eval["evaluation"] is None else best_eval["evaluation"]["capacity_upper_bound"],
                "best_exact_max_min": best_max_min,
                "best_agreement_vector": None if best_assignment is None else best_assignment["agreement_vector"],
                "best_failure_mode": best_eval["evaluation"]["status"] if best_eval["evaluation"] is not None else best_eval["solve"]["status"],
            },
            "exact_audited_system_count": len(results),
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
        print("SAGE_AUDIT_M1_A327_NONDEGENERATE_EXACT_LIFT_OK")
        print("exact_vectors_constructed: %d" % record["exact_lift_search"]["exact_vectors_constructed"])
        print("nondegenerate_vectors: %d" % record["exact_lift_search"]["nondegenerate_vectors"])
        print("best_exact_max_min: %s" % record["exact_lift_search"]["best_exact_max_min"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
