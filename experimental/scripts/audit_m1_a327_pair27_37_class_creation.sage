#!/usr/bin/env sage
"""Exact pair {2,7}/{3,7} class-creation audit."""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path


TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
LOW_COLLAPSE_THRESHOLD = 20

EXACT_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py")
CAPACITY_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_preserving_residual12_split.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pair27_37_class_creation.py")
DATA_PATH = Path("experimental/data/m1_a327_pair27_37_class_creation.json")

BASE_PARTIAL_FAMILY = "one_pair_13"
FREE_PATTERNS = ["d2_first_free"]
PAIR_CLASS_SIZES = [32]
PLANNED_LARGER_SIZES = [64, 96, 128, 160]
PAIR_CLASS_DESIGNS = [
    "disjoint_low_high",
    "overlap_all",
    "even_odd",
]
EXCLUDED_POSITIONS = {0, 18}


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


def round_robin_positions(positions, fibers, size, shift=0):
    by_fiber = {
        int(fiber): [int(pos) for pos in positions if int(pos) % 16 == int(fiber)]
        for fiber in fibers
    }
    out = []
    depth = 0
    while len(out) < size:
        progressed = False
        for fiber in fibers:
            rows = by_fiber[int(fiber)]
            idx = depth + shift
            if idx < len(rows):
                out.append(rows[idx])
                progressed = True
                if len(out) >= size:
                    break
        if not progressed:
            break
        depth += 1
    return out


def class_creation_sets(capacity, selected, partial_specs, design, size):
    used = {int(spec["position"]) for spec in partial_specs}
    base_positions = [
        int(pos)
        for pos in capacity.safe_positions(selected)
        if int(pos) not in used and int(pos) not in EXCLUDED_POSITIONS
    ]
    all_fibers = list(range(16))
    low = list(range(8))
    high = list(range(8, 16))
    even = [fiber for fiber in all_fibers if fiber % 2 == 0]
    odd = [fiber for fiber in all_fibers if fiber % 2 == 1]
    if design == "disjoint_low_high":
        return (
            round_robin_positions(base_positions, low, size),
            round_robin_positions(base_positions, high, size),
        )
    if design == "disjoint_high_low":
        return (
            round_robin_positions(base_positions, high, size),
            round_robin_positions(base_positions, low, size),
        )
    if design == "overlap_all":
        shared = round_robin_positions(base_positions, all_fibers, size)
        return shared, shared
    if design == "even_odd":
        return (
            round_robin_positions(base_positions, even, size),
            round_robin_positions(base_positions, odd, size),
        )
    if design == "same_fiber_shifted":
        return (
            round_robin_positions(base_positions, all_fibers, size, shift=0),
            round_robin_positions(base_positions, all_fibers, size, shift=1),
        )
    raise ValueError("unknown pair-class design: %s" % design)


def class_creation_specs(t27, t37, design, size):
    specs = []
    seen = set()
    for pos in t27:
        key = (2, 7, int(pos))
        if key in seen:
            continue
        seen.add(key)
        specs.append(
            {
                "left": 2,
                "right": 7,
                "position": int(pos),
                "gamma": 0,
                "kind": "pair_class_creation",
                "pair": "27",
                "design": design,
                "size": int(size),
            }
        )
    for pos in t37:
        key = (3, 7, int(pos))
        if key in seen:
            continue
        seen.add(key)
        specs.append(
            {
                "left": 3,
                "right": 7,
                "position": int(pos),
                "gamma": 0,
                "kind": "pair_class_creation",
                "pair": "37",
                "design": design,
                "size": int(size),
            }
        )
    return specs


def pin_rows(residual, F, powers, specs):
    rows = []
    rhs = []
    for spec in specs:
        rows.append(residual.evaluation_row(F, powers, spec["left"], spec["right"], spec["position"]))
        rhs.append(F(Integer(spec["gamma"])))
    return rows, rhs


def solve_with_prepared_matrix(F, A, rhs, free_values, pivots, pivot_matrix):
    if len(pivots) < A.nrows():
        return None, "PAIR_CLASS_SYSTEM_INCONSISTENT", "dependent or inconsistent row system"
    adjusted = []
    for row_idx in range(A.nrows()):
        total = F(0)
        for col, value in free_values.items():
            total += A[row_idx, col] * value
        adjusted.append(rhs[row_idx] - total)
    try:
        sol = pivot_matrix.solve_right(vector(F, adjusted))
    except Exception as exc:
        return None, "PAIR_CLASS_SYSTEM_INCONSISTENT", str(exc)
    x = [F(0)] * A.ncols()
    for col, value in free_values.items():
        x[col] = value
    for idx, col in enumerate(pivots[: A.nrows()]):
        x[col] = sol[idx]
    if all(value == 0 for value in x):
        return None, "PAIR_CLASS_UNDOES_D2_SPLIT", "zero solution"
    return x, "EXACT_VECTOR_CONSTRUCTED", None


def d2_split_from_classes(degenerate_classes):
    return not any(1 in row and 2 in row for row in degenerate_classes)


def classify(row):
    if not row["d2_split"]:
        return "PAIR_CLASS_UNDOES_D2_SPLIT"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "PAIR_CLASS_CAPACITY_LOSS"
    if row["six_class_dominance"] > LOW_COLLAPSE_THRESHOLD:
        return "PAIR_CLASS_COLLAPSE_RETURNS"
    if row["pair27_B"] < PAIR_TARGET or row["pair37_B"] < PAIR_TARGET:
        return "PAIR_CLASS_PARTIAL_REPAIR"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "PAIR_CLASS_EXACT_CANDIDATE"
    return "PAIR_CLASS_LOW_RESCHEDULE"


def evaluate_with_failure(residual, F, powers, vector_value, metadata):
    row = residual.evaluate_vector(F, powers, vector_value, metadata)
    row["d2_split"] = d2_split_from_classes(row["degenerate_classes"])
    row["capacity_preserving"] = bool(row["capacity_upper_bound"] >= TARGET_AGREEMENT)
    row["low_collapse"] = bool(row["six_class_dominance"] <= LOW_COLLAPSE_THRESHOLD)
    row["pair27_B"] = row["pair_B_values"][1]
    row["pair37_B"] = row["pair_B_values"][2]
    row["pair27_repaired"] = bool(row["pair27_B"] >= PAIR_TARGET)
    row["pair37_repaired"] = bool(row["pair37_B"] >= PAIR_TARGET)
    row["full_pair_repaired"] = bool(row["pair27_repaired"] and row["pair37_repaired"])
    row["failure_mode"] = classify(row)
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
        row.get("failure_mode") == "PAIR_CLASS_EXACT_CANDIDATE",
        row.get("full_pair_repaired") is True,
        row.get("pair27_repaired") is True and row.get("pair37_repaired") is True,
        row.get("d2_split") is True,
        row.get("capacity_preserving") is True,
        row.get("low_collapse") is True,
        exact_max,
        min(row.get("pair27_B", -1), row.get("pair37_B", -1)),
        row.get("capacity_upper_bound", -1),
        row.get("distinct_codewords") is True,
        -row.get("six_class_dominance", 10**9),
    )


def evaluate_candidate(exact_scan, capacity, residual, row, F, powers):
    reconstructed = exact_scan.reconstruct_candidate(row)
    selected = reconstructed["selected"]
    exact_rows, metas = residual.expanded_rows(F, powers, selected)
    protected_indices = capacity.protected_row_indices(metas)
    target_rows = [exact_rows[idx] for idx in protected_indices]
    partial_specs = capacity.partial_split_specs(selected, BASE_PARTIAL_FAMILY)
    partial_rows, partial_rhs = residual.pin_rows(F, powers, partial_specs)
    results = []
    systems = []

    for design in PAIR_CLASS_DESIGNS:
        for size in PAIR_CLASS_SIZES:
            t27, t37 = class_creation_sets(capacity, selected, partial_specs, design, size)
            if len(t27) < size or len(t37) < size:
                systems.append(
                    {
                        "candidate_id": row["target_system_id"],
                        "design": design,
                        "size": int(size),
                        "T27_count": len(t27),
                        "T37_count": len(t37),
                        "failure_mode": "PAIR_CLASS_SYSTEM_INCONSISTENT",
                        "error": "insufficient structured coordinates",
                        "vector_results": [],
                    }
                )
                continue
            creation_specs = class_creation_specs(t27, t37, design, size)
            creation_rows, creation_rhs = pin_rows(residual, F, powers, creation_specs)
            base_rows = target_rows + partial_rows + creation_rows
            base_rhs = [F(0)] * len(target_rows) + partial_rhs + creation_rhs
            base_matrix = Matrix(F, base_rows, ncols=residual.VARIABLE_COUNT)
            base_pivots = [int(col) for col in base_matrix.pivots()]
            if len(base_pivots) >= len(base_rows):
                pivot_matrix = base_matrix.matrix_from_columns(base_pivots[: len(base_rows)])
            else:
                pivot_matrix = None
            system_rows = []
            for pattern in FREE_PATTERNS:
                free_values = residual.free_assignments(F, pattern, base_pivots)
                if pivot_matrix is None:
                    vector_value, status, error = None, "PAIR_CLASS_SYSTEM_INCONSISTENT", "rank below row count"
                else:
                    vector_value, status, error = solve_with_prepared_matrix(
                        F,
                        base_matrix,
                        vector(F, base_rhs),
                        free_values,
                        base_pivots,
                        pivot_matrix,
                    )
                metadata = {
                    "candidate_id": row["target_system_id"],
                    "search_layer": "pair27_37_class_creation",
                    "partial_split_family": BASE_PARTIAL_FAMILY,
                    "design": design,
                    "T27_size": int(size),
                    "T37_size": int(size),
                    "T27_positions": t27,
                    "T37_positions": t37,
                    "free_pattern": pattern,
                    "pin_specs": partial_specs + creation_specs,
                    "protected_rows": len(target_rows),
                    "creation_rows": len(creation_rows),
                    "solve_status": status,
                }
                if vector_value is None:
                    system_rows.append(
                        {
                            **metadata,
                            "failure_mode": "PAIR_CLASS_SYSTEM_INCONSISTENT",
                            "error": error,
                        }
                    )
                    continue
                system_rows.append(evaluate_with_failure(residual, F, powers, vector_value, metadata))
            results.extend(system_rows)
            best_system = sorted(system_rows, key=vector_sort_key, reverse=True)[0]
            systems.append(
                {
                    "candidate_id": row["target_system_id"],
                    "design": design,
                    "size": int(size),
                    "T27_count": len(t27),
                    "T37_count": len(t37),
                    "creation_rows": len(creation_rows),
                    "failure_mode_counts": failure_counts(system_rows),
                    "best": best_system,
                    "vector_results": system_rows,
                }
            )

    best = sorted(results, key=vector_sort_key, reverse=True)[0]
    return {
        "candidate_id": row["target_system_id"],
        "proxy_max_min": row["best"]["proxy_max_min"],
        "proxy_pair_B_values": row["best"]["pair7_B_values"],
        "protected_rows": len(target_rows),
        "partial_split_family": BASE_PARTIAL_FAMILY,
        "system_count": len(systems),
        "vector_count": len(results),
        "failure_mode_counts": failure_counts(results),
        "best": best,
        "systems": systems,
        "retained_results": sorted(results, key=vector_sort_key, reverse=True)[:12],
    }


def audit_record():
    exact_scan = load_python_module(EXACT_SCAN_PATH, "protected_exchange_exact_scan")
    capacity = load_source_module(CAPACITY_AUDIT_PATH, "capacity_preserving_residual12")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_for_pair_creation")
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "pair27_37_class_creation_ledger")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    source = exact_scan.source_record()
    candidates = exact_scan.proxy_candidate_rows(source)
    results = [evaluate_candidate(exact_scan, capacity, residual, row, F, powers) for row in candidates]
    rows = [
        row
        for result in results
        for system in result["systems"]
        for row in system.get("vector_results", [])
    ]
    best_pool = [system["best"] for result in results for system in result["systems"]] or rows
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    search = {
        "exact_field": "GF(17^32)",
        "field_denominator": str(q),
        "systems_tested": sum(result["system_count"] for result in results),
        "T27_sizes": PAIR_CLASS_SIZES,
        "T37_sizes": PAIR_CLASS_SIZES,
        "planned_larger_sizes": PLANNED_LARGER_SIZES,
        "designs_tested": PAIR_CLASS_DESIGNS,
        "free_patterns": FREE_PATTERNS,
        "exact_vectors_constructed": sum(1 for row in rows if row.get("distinct_codewords") is not None),
        "D2_split_vectors": sum(1 for row in rows if row.get("d2_split") is True),
        "low_collapse_vectors": sum(1 for row in rows if row.get("low_collapse") is True),
        "pair27_repaired_vectors": sum(1 for row in rows if row.get("pair27_repaired") is True),
        "pair37_repaired_vectors": sum(1 for row in rows if row.get("pair37_repaired") is True),
        "full_pair_repaired_vectors": sum(1 for row in rows if row.get("full_pair_repaired") is True),
        "best_pair_values": None if best is None else best.get("pair_B_values"),
        "best_B27": None if best is None else best.get("pair27_B"),
        "best_B37": None if best is None else best.get("pair37_B"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    record = ledger_scan.build_record(pair_class_creation=search)
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
        print("SAGE_AUDIT_M1_A327_PAIR27_37_CLASS_CREATION_OK")
        print("systems_tested: %d" % record["pair_class_creation"]["systems_tested"])
        print("exact_vectors_constructed: %d" % record["pair_class_creation"]["exact_vectors_constructed"])
        print("D2_split_vectors: %d" % record["pair_class_creation"]["D2_split_vectors"])
        print("pair27_repaired_vectors: %d" % record["pair_class_creation"]["pair27_repaired_vectors"])
        print("pair37_repaired_vectors: %d" % record["pair_class_creation"]["pair37_repaired_vectors"])
        print("best_failure_mode: %s" % record["pair_class_creation"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
