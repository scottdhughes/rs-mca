#!/usr/bin/env sage
"""Exact capacity-preserving residual [1,2] split audit."""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path


P = 17
TARGET_AGREEMENT = 327
PAIR7_BASELINE = 631
PAIR7_TARGET = 2 * TARGET_AGREEMENT
LOW_COLLAPSE_THRESHOLD = 20

EXACT_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py")
RESIDUAL_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_residual_12_split_pinned_nullspace.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_capacity_preserving_residual12_split.py")
DATA_PATH = Path("experimental/data/m1_a327_capacity_preserving_residual12_split.json")

PARTIAL_SPLIT_FAMILIES = [
    "none",
    "one_pair_13",
    "two_pair_balanced_split",
]
FREE_PATTERNS = [
    "affine_pivot_solution",
    "d2_first_free",
    "d2_first4_free",
    "d2_even_sparse",
]
RESIDUAL_COORD_LIMIT = 3
GAMMAS = [1, 2, 3]


def load_python_module(path, module_name):
    script_dir = str(path.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_source_module(path, module_name):
    loader = importlib.machinery.SourceFileLoader(module_name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    module.Integer = Integer
    module.GF = GF
    module.Matrix = Matrix
    module.vector = vector
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


def quotient_round_order():
    return [fiber + 16 * offset for offset in range(32) for fiber in range(16)]


def protected_row_indices(metas):
    return [
        idx
        for idx, meta in enumerate(metas)
        if meta["source"] in {"pair7_repair", "protected_exchange_repair"}
    ]


def safe_positions(selected):
    all_used = {int(row["position"]) for row in selected}
    repair_used = {
        int(row["position"])
        for row in selected
        if row["source"] in {"pair7_repair", "protected_exchange_repair"}
    }
    primary = [pos for pos in quotient_round_order() if pos not in all_used]
    if len(primary) >= RESIDUAL_COORD_LIMIT + 4:
        return primary
    return [pos for pos in quotient_round_order() if pos not in repair_used]


def partial_split_specs(selected, family):
    positions = safe_positions(selected)
    if family == "none":
        return []
    if family == "one_pair_13":
        pairs = [(1, 3)]
    elif family == "two_pair_balanced_split":
        pairs = [(1, 3), (4, 7)]
    else:
        raise ValueError("unknown partial split family: %s" % family)
    return [
        {
            "left": left,
            "right": right,
            "position": int(positions[idx]),
            "gamma": int(idx + 1),
            "kind": "partial_split",
            "family": family,
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


def d2_split_from_classes(degenerate_classes):
    return not any(1 in row and 2 in row for row in degenerate_classes)


def classify_capacity_preserving(row):
    if not d2_split_from_classes(row["degenerate_classes"]):
        return "RESIDUAL12_NOT_SPLIT"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "RESIDUAL12_SPLIT_CAPACITY_LOSS"
    if row["six_class_dominance"] > LOW_COLLAPSE_THRESHOLD:
        return "RESIDUAL12_SPLIT_COLLAPSE_RETURNS"
    if row["min_pair_B"] < PAIR7_BASELINE:
        return "RESIDUAL12_SPLIT_PAIR7_LOSS"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "RESIDUAL12_EXACT_CANDIDATE"
    if row.get("exact_max_min") is not None:
        return "RESIDUAL12_SPLIT_LOW_RESCHEDULE"
    return "RESIDUAL12_CAPACITY_PRESERVING_SPLIT"


def evaluate_with_failure(residual, F, powers, vector_value, metadata):
    row = residual.evaluate_vector(F, powers, vector_value, metadata)
    row["d2_split"] = d2_split_from_classes(row["degenerate_classes"])
    row["capacity_preserving_d2_split"] = bool(
        row["d2_split"] and row["capacity_upper_bound"] >= TARGET_AGREEMENT
    )
    row["low_collapse_capacity_preserving_d2_split"] = bool(
        row["capacity_preserving_d2_split"] and row["six_class_dominance"] <= LOW_COLLAPSE_THRESHOLD
    )
    row["pair7_baseline_preserved"] = bool(row["min_pair_B"] >= PAIR7_BASELINE)
    row["pair7_target_preserved"] = bool(row["min_pair_B"] >= PAIR7_TARGET)
    row["failure_mode"] = classify_capacity_preserving(row)
    return row


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    return (
        row.get("failure_mode") == "RESIDUAL12_EXACT_CANDIDATE",
        row.get("capacity_preserving_d2_split") is True,
        row.get("pair7_target_preserved") is True,
        row.get("pair7_baseline_preserved") is True,
        row.get("d2_split") is True,
        exact_max,
        row.get("min_pair_B", -1),
        row.get("capacity_upper_bound", -1),
        row.get("distinct_codewords") is True,
        -row.get("six_class_dominance", 10**9),
    )


def evaluate_candidate(exact_scan, residual, row, F, powers):
    reconstructed = exact_scan.reconstruct_candidate(row)
    selected = reconstructed["selected"]
    exact_rows, metas = residual.expanded_rows(F, powers, selected)
    protected_indices = protected_row_indices(metas)
    target_rows = [exact_rows[idx] for idx in protected_indices]
    results = []

    for family in PARTIAL_SPLIT_FAMILIES:
        partial_specs = partial_split_specs(selected, family)
        partial_rows, partial_rhs = residual.pin_rows(F, powers, partial_specs)
        base_rows = target_rows + partial_rows
        base_rhs = [F(0)] * len(target_rows) + partial_rhs
        base_matrix = Matrix(F, base_rows, ncols=residual.VARIABLE_COUNT)
        base_pivots = [int(col) for col in base_matrix.pivots()]

        for pattern in FREE_PATTERNS:
            free_values = residual.free_assignments(F, pattern, base_pivots)
            vector_value, status, error, _pivots = residual.solve_with_free(F, base_rows, base_rhs, free_values)
            metadata = {
                "candidate_id": row["target_system_id"],
                "search_layer": "d2_nullspace_sample",
                "row_schedule": "protected_plus_exchange_rows",
                "partial_split_family": family,
                "free_pattern": pattern,
                "pin_specs": partial_specs,
                "solve_status": status,
            }
            if vector_value is None:
                results.append({**metadata, "failure_mode": status, "error": error})
                continue
            results.append(evaluate_with_failure(residual, F, powers, vector_value, metadata))

        for residual_spec in residual12_specs(selected):
            residual_rows, residual_rhs = residual.pin_rows(F, powers, [residual_spec])
            vector_value, status, error, _pivots = residual.solve_with_free(
                F,
                base_rows + residual_rows,
                base_rhs + residual_rhs,
                {},
            )
            metadata = {
                "candidate_id": row["target_system_id"],
                "search_layer": "soft_residual12_pin",
                "row_schedule": "protected_plus_exchange_rows",
                "partial_split_family": family,
                "residual_pin": residual_spec,
                "pin_specs": partial_specs + [residual_spec],
                "solve_status": status,
            }
            if vector_value is None:
                results.append({**metadata, "failure_mode": status, "error": error})
                continue
            results.append(evaluate_with_failure(residual, F, powers, vector_value, metadata))

    best = sorted(results, key=vector_sort_key, reverse=True)[0]
    return {
        "candidate_id": row["target_system_id"],
        "proxy_max_min": row["best"]["proxy_max_min"],
        "proxy_pair_B_values": row["best"]["pair7_B_values"],
        "protected_rows": len(target_rows),
        "attempt_count": len(results),
        "failure_mode_counts": failure_counts(results),
        "best": best,
        "vector_results": results,
        "retained_results": sorted(results, key=vector_sort_key, reverse=True)[:12],
    }


def audit_record():
    exact_scan = load_python_module(EXACT_SCAN_PATH, "protected_exchange_exact_scan")
    residual = load_source_module(RESIDUAL_AUDIT_PATH, "residual12_exact_audit")
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "capacity_preserving_residual12_ledger")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    source = exact_scan.source_record()
    candidates = exact_scan.proxy_candidate_rows(source)
    results = [evaluate_candidate(exact_scan, residual, row, F, powers) for row in candidates]
    attempts = [row for result in results for row in result["vector_results"]]
    best = sorted(attempts, key=vector_sort_key, reverse=True)[0] if attempts else None
    search = {
        "exact_field": "GF(17^32)",
        "field_denominator": str(q),
        "protected_rows": max((result["protected_rows"] for result in results), default=0),
        "pin_sets_tested": sum(
            1 for result in results for row in result["vector_results"] if row.get("search_layer") == "soft_residual12_pin"
        ),
        "nullspace_samples_tested": sum(
            1 for result in results for row in result["vector_results"] if row.get("search_layer") == "d2_nullspace_sample"
        ),
        "exact_vectors_constructed": sum(
            1 for result in results for row in result["vector_results"] if row.get("distinct_codewords") is not None
        ),
        "d2_split_vectors": sum(
            1 for result in results for row in result["vector_results"] if row.get("d2_split") is True
        ),
        "capacity_preserving_d2_split_vectors": sum(
            1
            for result in results
            for row in result["vector_results"]
            if row.get("capacity_preserving_d2_split") is True
        ),
        "low_collapse_capacity_preserving_d2_split_vectors": sum(
            1
            for result in results
            for row in result["vector_results"]
            if row.get("low_collapse_capacity_preserving_d2_split") is True
        ),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_degenerate_classes": None if best is None else best.get("degenerate_classes"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    record = ledger_scan.build_record(capacity_preserving_search=search)
    record["result_hash"] = residual.hash_payload(results)
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
        print("SAGE_AUDIT_M1_A327_CAPACITY_PRESERVING_RESIDUAL12_SPLIT_OK")
        print("pin_sets_tested: %d" % record["capacity_preserving_residual12_search"]["pin_sets_tested"])
        print("nullspace_samples_tested: %d" % record["capacity_preserving_residual12_search"]["nullspace_samples_tested"])
        print("d2_split_vectors: %d" % record["capacity_preserving_residual12_search"]["d2_split_vectors"])
        print(
            "capacity_preserving_d2_split_vectors: %d"
            % record["capacity_preserving_residual12_search"]["capacity_preserving_d2_split_vectors"]
        )
        print("best_failure_mode: %s" % record["capacity_preserving_residual12_search"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
