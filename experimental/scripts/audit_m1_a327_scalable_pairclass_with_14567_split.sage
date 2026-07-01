#!/usr/bin/env sage
"""Exact scalable pair-class creation with controlled [1,4,5,6,7] split."""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import time
from numbers import Integral
from pathlib import Path


TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
BASE_PAIR_VALUES = [1024, 577, 576, 1024, 1024]
BASE_COLLAPSE = [[1, 4, 5, 6, 7], [3], [2]]

SCRIPT_PATH = Path("experimental/scripts/audit_m1_a327_scalable_pairclass_with_14567_split.sage")
SCALABLE_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_pair27_37_class_creation_scalable.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_scalable_pairclass_with_14567_split.py")
DATA_PATH = Path("experimental/data/m1_a327_scalable_pairclass_with_14567_split.json")

TARGET_SIZE = 128
PAIR_ROW_EXTENSIONS = [32, 64, 96]
SPLIT_FAMILIES = [
    "split_7_from_1456",
    "split_14_567",
    "split_145_67",
    "chain_split_14567",
]
FREE_PATTERNS = ["d2_first_free", "d2_first4_free", "d2_even_sparse"]
CASE_TIMEOUT_SECONDS = 55


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
    try:
        if hasattr(payload, "__float__"):
            return float(payload)
    except Exception:
        pass
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def collapse_reduced(degenerate_classes):
    return BASE_COLLAPSE[0] not in degenerate_classes


def split_positions(capacity, selected, partial_specs, occupied, count):
    used = {int(spec["position"]) for spec in partial_specs} | set(int(pos) for pos in occupied)
    positions = [int(pos) for pos in capacity.safe_positions(selected) if int(pos) not in used]
    return positions[:count]


def split_specs(capacity, selected, partial_specs, occupied, family):
    if family == "split_7_from_1456":
        positions = split_positions(capacity, selected, partial_specs, occupied, 1)
        return [{"left": 7, "right": 1, "position": positions[0], "gamma": 1, "kind": family}]
    if family == "split_14_567":
        positions = split_positions(capacity, selected, partial_specs, occupied, 3)
        return [
            {"left": 5, "right": 1, "position": positions[0], "gamma": 1, "kind": family},
            {"left": 6, "right": 5, "position": positions[1], "gamma": 0, "kind": family},
            {"left": 7, "right": 5, "position": positions[2], "gamma": 0, "kind": family},
        ]
    if family == "split_145_67":
        positions = split_positions(capacity, selected, partial_specs, occupied, 2)
        return [
            {"left": 6, "right": 1, "position": positions[0], "gamma": 1, "kind": family},
            {"left": 7, "right": 6, "position": positions[1], "gamma": 0, "kind": family},
        ]
    if family == "chain_split_14567":
        positions = split_positions(capacity, selected, partial_specs, occupied, 4)
        return [
            {"left": 4, "right": 1, "position": positions[0], "gamma": 1, "kind": family},
            {"left": 5, "right": 4, "position": positions[1], "gamma": 1, "kind": family},
            {"left": 6, "right": 5, "position": positions[2], "gamma": 1, "kind": family},
            {"left": 7, "right": 6, "position": positions[3], "gamma": 1, "kind": family},
        ]
    raise ValueError("unknown split family: %s" % family)


def classify(row):
    if row.get("capacity_upper_bound", 0) < TARGET_AGREEMENT:
        return "PAIRCLASS_SPLIT_CAPACITY_LOSS"
    if row.get("pair_B_values") is None:
        return "PAIRCLASS_SPLIT_INCONSISTENT"
    if row["pair_B_values"][1] < BASE_PAIR_VALUES[1] or row["pair_B_values"][2] < BASE_PAIR_VALUES[2]:
        return "PAIRCLASS_SPLIT_PAIR_LOSS"
    if row["pair_B_values"][1] <= BASE_PAIR_VALUES[1] and row["pair_B_values"][2] <= BASE_PAIR_VALUES[2]:
        return "PAIRCLASS_GROWTH_STALLS"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "PAIRCLASS_EXACT_CANDIDATE"
    return "PAIRCLASS_SPLIT_LOW_RESCHEDULE"


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "PAIRCLASS_EXACT_CANDIDATE",
        row.get("collapse_reduced") is True,
        row.get("capacity_preserving") is True,
        exact_max,
        min(pair_values[1], pair_values[2]),
        row.get("capacity_upper_bound", -1),
        row.get("distinct_codewords") is True,
    )


def case_record(case):
    scalable = load_source_module(SCALABLE_AUDIT_PATH, "pairclass_scalable_helpers")
    exact_scan = scalable.load_python_module(scalable.EXACT_SCAN_PATH, "protected_exchange_exact_scan_split")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_split")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_split")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    source = exact_scan.source_record()
    candidate = exact_scan.proxy_candidate_rows(source)[0]
    reconstructed = exact_scan.reconstruct_candidate(candidate)
    selected = reconstructed["selected"]
    exact_rows, metas = residual.expanded_rows(F, powers, selected)
    protected_indices = capacity.protected_row_indices(metas)
    target_rows = [exact_rows[idx] for idx in protected_indices]
    partial_specs = capacity.partial_split_specs(selected, scalable.BASE_PARTIAL_FAMILY)
    partial_rows, partial_rhs = residual.pin_rows(F, powers, partial_specs)
    base_t27, base_t37 = scalable.class_creation_sets(
        capacity, selected, partial_specs, scalable.BASE_DESIGN, scalable.BASE_SIZE
    )
    full_t27, full_t37 = scalable.class_creation_sets(capacity, selected, partial_specs, "overlap_all", TARGET_SIZE)
    base_specs = scalable.specs_from_positions(
        base_t27, base_t37, scalable.BASE_DESIGN, scalable.BASE_SIZE, "pair_class_creation_base"
    )
    extension_tuples = scalable.alternating_extension(
        base_t27, base_t37, full_t27, full_t37, case["pair_row_extension"]
    )
    extension_specs = scalable.specs_from_extension(extension_tuples, "overlap_all", TARGET_SIZE)
    occupied = list(base_t27) + list(base_t37) + [row[2] for row in extension_tuples]
    split = split_specs(capacity, selected, partial_specs, occupied, case["split_family"])
    class_rows, class_rhs = scalable.pin_rows(residual, F, powers, base_specs + extension_specs)
    split_rows, split_rhs = scalable.pin_rows(residual, F, powers, split)
    rows = target_rows + partial_rows + class_rows + split_rows
    rhs = [F(0)] * len(target_rows) + partial_rhs + class_rhs + split_rhs

    start = time.time()
    A = Matrix(F, rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    rank_after = len(pivots)
    nullity_after = residual.VARIABLE_COUNT - rank_after
    pivot_matrix = A.matrix_from_columns(pivots[: len(rows)]) if rank_after >= len(rows) else None
    if pivot_matrix is None:
        return {
            **case,
            "row_count": len(rows),
            "rank_after": rank_after,
            "nullity_after": nullity_after,
            "failure_mode": "PAIRCLASS_SPLIT_INCONSISTENT",
            "error": "rank below row count",
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }

    vectors = []
    for pattern in FREE_PATTERNS:
        free_values = residual.free_assignments(F, pattern, pivots)
        vector_value, status, error = scalable.solve_with_prepared_matrix(
            F, A, vector(F, rhs), free_values, pivots, pivot_matrix
        )
        metadata = {
            **case,
            "target_size": TARGET_SIZE,
            "free_pattern": pattern,
            "row_count": len(rows),
            "protected_rows": len(target_rows),
            "base_creation_rows": len(base_specs),
            "extension_rows": len(extension_specs),
            "split_rows": len(split),
            "split_specs": split,
            "rank_after": rank_after,
            "nullity_after": nullity_after,
            "solve_status": status,
        }
        if vector_value is None:
            vectors.append({**metadata, "failure_mode": "PAIRCLASS_SPLIT_INCONSISTENT", "error": error})
            continue
        row = scalable.evaluate_with_failure(residual, F, powers, vector_value, metadata)
        row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
        row["collapse_reduced"] = collapse_reduced(row["degenerate_classes"])
        row["failure_mode"] = classify(row)
        vectors.append(row)

    best = sorted(vectors, key=vector_sort_key, reverse=True)[0]
    return {
        **case,
        "target_size": TARGET_SIZE,
        "row_count": len(rows),
        "rank_after": rank_after,
        "nullity_after": nullity_after,
        "elapsed_seconds": float(round(float(time.time() - start), 3)),
        "best": best,
        "vector_results": vectors,
        "failure_mode": best["failure_mode"],
    }


def run_child(case):
    cmd = ["/usr/local/bin/sage", str(SCRIPT_PATH), "--single-case", json.dumps(case, sort_keys=True)]
    try:
        completed = subprocess.run(
            cmd,
            check=False,
            text=True,
            capture_output=True,
            timeout=CASE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {
            **case,
            "failure_mode": "PAIRCLASS_SPLIT_TIMEOUT",
            "timeout_seconds": CASE_TIMEOUT_SECONDS,
            "vector_results": [],
        }
    if completed.returncode != 0:
        return {
            **case,
            "failure_mode": "PAIRCLASS_SPLIT_INCONSISTENT",
            "returncode": completed.returncode,
            "stderr_tail": completed.stderr[-2000:],
            "vector_results": [],
        }
    try:
        return json.loads(completed.stdout)
    except Exception as exc:
        return {
            **case,
            "failure_mode": "PAIRCLASS_SPLIT_INCONSISTENT",
            "error": str(exc),
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
            "vector_results": [],
        }


def cases():
    return [
        {"pair_row_extension": int(extension), "split_family": family}
        for extension in PAIR_ROW_EXTENSIONS
        for family in SPLIT_FAMILIES
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "pairclass_split_ledger")
    results = [run_child(case) for case in cases()]
    vectors = [row for result in results for row in result.get("vector_results", [])]
    best_pool = vectors or [row.get("best", row) for row in results]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    search = {
        "exact_field": "GF(17^32)",
        "target_sizes": [TARGET_SIZE],
        "systems_tested": len(results),
        "pair_row_extensions": PAIR_ROW_EXTENSIONS,
        "split_families": SPLIT_FAMILIES,
        "free_patterns": FREE_PATTERNS,
        "case_timeout_seconds": CASE_TIMEOUT_SECONDS,
        "exact_vectors_constructed": sum(1 for row in vectors if row.get("distinct_codewords") is not None),
        "capacity_preserving_vectors": sum(1 for row in vectors if row.get("capacity_preserving") is True),
        "pair_values_improved_vectors": sum(
            1
            for row in vectors
            if row.get("pair_B_values") is not None
            and row["pair_B_values"][1] > BASE_PAIR_VALUES[1]
            and row["pair_B_values"][2] > BASE_PAIR_VALUES[2]
        ),
        "collapse_reduced_vectors": sum(1 for row in vectors if row.get("collapse_reduced") is True),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "PAIRCLASS_SPLIT_TIMEOUT"),
        "failure_mode_counts": failure_counts(vectors or results),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_collapse_pattern": None if best is None else best.get("degenerate_classes"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    return jsonable(ledger_scan.build_record(pairclass_split_search=search))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--single-case")
    args = parser.parse_args()
    if args.single_case:
        print(json.dumps(jsonable(case_record(json.loads(args.single_case))), sort_keys=True))
        return
    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_SCALABLE_PAIRCLASS_WITH_14567_SPLIT_OK")
        print("systems_tested: %d" % record["pairclass_split_search"]["systems_tested"])
        print("exact_vectors_constructed: %d" % record["pairclass_split_search"]["exact_vectors_constructed"])
        print("collapse_reduced_vectors: %d" % record["pairclass_split_search"]["collapse_reduced_vectors"])
        print("best_failure_mode: %s" % record["pairclass_split_search"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
