#!/usr/bin/env sage
"""Scalable exact pair {2,7}/{3,7} class-creation audit."""

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
LOW_COLLAPSE_THRESHOLD = 20

SCRIPT_PATH = Path("experimental/scripts/audit_m1_a327_pair27_37_class_creation_scalable.sage")
EXACT_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py")
CAPACITY_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_preserving_residual12_split.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pair27_37_class_creation_scalable.py")
DATA_PATH = Path("experimental/data/m1_a327_pair27_37_class_creation_scalable.json")

BASE_PARTIAL_FAMILY = "one_pair_13"
BASE_DESIGN = "overlap_all"
BASE_SIZE = 32
FREE_PATTERN = "d2_first_free"
T_SIZES = [64, 96]
EXTENSION_ROW_BLOCKS = [32, 64]
SCALABLE_DESIGNS = ["overlap_all", "same_fiber_shifted", "disjoint_low_high"]
CASE_TIMEOUT_SECONDS = 35
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


def alternating_extension(base_t27, base_t37, full_t27, full_t37, row_block):
    base27 = set(int(pos) for pos in base_t27)
    base37 = set(int(pos) for pos in base_t37)
    extra27 = [int(pos) for pos in full_t27 if int(pos) not in base27]
    extra37 = [int(pos) for pos in full_t37 if int(pos) not in base37]
    specs = []
    idx = 0
    while len(specs) < row_block and (idx < len(extra27) or idx < len(extra37)):
        if idx < len(extra27) and len(specs) < row_block:
            specs.append((2, 7, extra27[idx], "27"))
        if idx < len(extra37) and len(specs) < row_block:
            specs.append((3, 7, extra37[idx], "37"))
        idx += 1
    return specs


def specs_from_positions(t27, t37, design, size, source):
    out = []
    for pos in t27:
        out.append(
            {
                "left": 2,
                "right": 7,
                "position": int(pos),
                "gamma": 0,
                "kind": source,
                "pair": "27",
                "design": design,
                "size": int(size),
            }
        )
    for pos in t37:
        out.append(
            {
                "left": 3,
                "right": 7,
                "position": int(pos),
                "gamma": 0,
                "kind": source,
                "pair": "37",
                "design": design,
                "size": int(size),
            }
        )
    return out


def specs_from_extension(extension_specs, design, size):
    return [
        {
            "left": left,
            "right": right,
            "position": int(pos),
            "gamma": 0,
            "kind": "pair_class_creation_extension",
            "pair": pair,
            "design": design,
            "size": int(size),
        }
        for left, right, pos, pair in extension_specs
    ]


def pin_rows(residual, F, powers, specs):
    rows = []
    rhs = []
    for spec in specs:
        rows.append(residual.evaluation_row(F, powers, spec["left"], spec["right"], spec["position"]))
        rhs.append(F(Integer(spec["gamma"])))
    return rows, rhs


def solve_with_prepared_matrix(F, A, rhs, free_values, pivots, pivot_matrix):
    if len(pivots) < A.nrows():
        return None, "SCALABLE_SYSTEM_FULL_RANK", "dependent or inconsistent row system"
    adjusted = []
    for row_idx in range(A.nrows()):
        total = F(0)
        for col, value in free_values.items():
            total += A[row_idx, col] * value
        adjusted.append(rhs[row_idx] - total)
    try:
        sol = pivot_matrix.solve_right(vector(F, adjusted))
    except Exception as exc:
        return None, "SCALABLE_SYSTEM_FULL_RANK", str(exc)
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


def case_record(case):
    exact_scan = load_python_module(EXACT_SCAN_PATH, "protected_exchange_exact_scan_scalable")
    capacity = load_source_module(CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_scalable")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_scalable")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    source = exact_scan.source_record()
    candidate = exact_scan.proxy_candidate_rows(source)[0]
    reconstructed = exact_scan.reconstruct_candidate(candidate)
    selected = reconstructed["selected"]
    exact_rows, metas = residual.expanded_rows(F, powers, selected)
    protected_indices = capacity.protected_row_indices(metas)
    target_rows = [exact_rows[idx] for idx in protected_indices]
    partial_specs = capacity.partial_split_specs(selected, BASE_PARTIAL_FAMILY)
    partial_rows, partial_rhs = residual.pin_rows(F, powers, partial_specs)

    base_t27, base_t37 = class_creation_sets(capacity, selected, partial_specs, BASE_DESIGN, BASE_SIZE)
    full_t27, full_t37 = class_creation_sets(capacity, selected, partial_specs, case["design"], case["size"])
    if len(full_t27) < case["size"] or len(full_t37) < case["size"]:
        return {
            **case,
            "candidate_id": candidate["target_system_id"],
            "failure_mode": "SCALABLE_SYSTEM_FULL_RANK",
            "error": "insufficient structured coordinates",
        }
    base_specs = specs_from_positions(base_t27, base_t37, BASE_DESIGN, BASE_SIZE, "pair_class_creation_base")
    extension_tuples = alternating_extension(base_t27, base_t37, full_t27, full_t37, case["extension_row_block"])
    extension_specs = specs_from_extension(extension_tuples, case["design"], case["size"])
    creation_specs = base_specs + extension_specs
    creation_rows, creation_rhs = pin_rows(residual, F, powers, creation_specs)
    rows = target_rows + partial_rows + creation_rows
    rhs = [F(0)] * len(target_rows) + partial_rhs + creation_rhs
    start = time.time()
    A = Matrix(F, rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    rank_after = len(pivots)
    nullity_after = residual.VARIABLE_COUNT - rank_after
    pivot_matrix = A.matrix_from_columns(pivots[: len(rows)]) if rank_after >= len(rows) else None
    free_values = residual.free_assignments(F, FREE_PATTERN, pivots)
    if pivot_matrix is None:
        return {
            **case,
            "candidate_id": candidate["target_system_id"],
            "row_count": len(rows),
            "protected_rows": len(target_rows),
            "base_creation_rows": len(base_specs),
            "extension_rows": len(extension_specs),
            "rank_after": rank_after,
            "nullity_after": nullity_after,
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
            "failure_mode": "SCALABLE_SYSTEM_FULL_RANK",
            "error": "rank below row count",
        }
    vector_value, status, error = solve_with_prepared_matrix(F, A, vector(F, rhs), free_values, pivots, pivot_matrix)
    metadata = {
        **case,
        "candidate_id": candidate["target_system_id"],
        "search_layer": "pair27_37_class_creation_scalable",
        "partial_split_family": BASE_PARTIAL_FAMILY,
        "free_pattern": FREE_PATTERN,
        "row_count": len(rows),
        "protected_rows": len(target_rows),
        "base_creation_rows": len(base_specs),
        "extension_rows": len(extension_specs),
        "rank_after": rank_after,
        "nullity_after": nullity_after,
        "solve_status": status,
    }
    if vector_value is None:
        return {
            **metadata,
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
            "failure_mode": status,
            "error": error,
        }
    row = evaluate_with_failure(residual, F, powers, vector_value, metadata)
    row["elapsed_seconds"] = float(round(float(time.time() - start), 3))
    return row


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
            "failure_mode": "SCALABLE_SYSTEM_TIMEOUT",
            "timeout_seconds": CASE_TIMEOUT_SECONDS,
        }
    if completed.returncode != 0:
        return {
            **case,
            "failure_mode": "SCALABLE_SYSTEM_FULL_RANK",
            "returncode": completed.returncode,
            "stderr_tail": completed.stderr[-2000:],
        }
    try:
        return json.loads(completed.stdout)
    except Exception as exc:
        return {
            **case,
            "failure_mode": "SCALABLE_SYSTEM_FULL_RANK",
            "error": str(exc),
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        }


def cases():
    out = []
    for size in T_SIZES:
        for design in SCALABLE_DESIGNS:
            for block in EXTENSION_ROW_BLOCKS:
                out.append(
                    {
                        "size": int(size),
                        "design": design,
                        "extension_row_block": int(block),
                    }
                )
    return out


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "pair27_37_class_creation_scalable_ledger")
    results = [run_child(case) for case in cases()]
    best_pool = [row for row in results if row.get("pair_B_values") is not None]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    search = {
        "exact_field": "GF(17^32)",
        "T27_sizes": T_SIZES,
        "T37_sizes": T_SIZES,
        "designs_tested": SCALABLE_DESIGNS,
        "extension_row_blocks": EXTENSION_ROW_BLOCKS,
        "case_timeout_seconds": CASE_TIMEOUT_SECONDS,
        "systems_tested": len(results),
        "incremental_blocks_tested": len(results),
        "exact_vectors_constructed": sum(1 for row in results if row.get("distinct_codewords") is not None),
        "D2_split_vectors": sum(1 for row in results if row.get("d2_split") is True),
        "low_collapse_vectors": sum(1 for row in results if row.get("low_collapse") is True),
        "pair27_repaired_vectors": sum(1 for row in results if row.get("pair27_repaired") is True),
        "pair37_repaired_vectors": sum(1 for row in results if row.get("pair37_repaired") is True),
        "full_pair_repaired_vectors": sum(1 for row in results if row.get("full_pair_repaired") is True),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "SCALABLE_SYSTEM_TIMEOUT"),
        "failure_mode_counts": failure_counts(results),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_B27": None if best is None else best.get("pair27_B"),
        "best_B37": None if best is None else best.get("pair37_B"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    record = ledger_scan.build_record(scalable_class_creation=search)
    return jsonable(record)


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
        print("SAGE_AUDIT_M1_A327_PAIR27_37_CLASS_CREATION_SCALABLE_OK")
        print("systems_tested: %d" % record["scalable_class_creation"]["systems_tested"])
        print("timeouts: %d" % record["scalable_class_creation"]["timeouts"])
        print("exact_vectors_constructed: %d" % record["scalable_class_creation"]["exact_vectors_constructed"])
        print("best_failure_mode: %s" % record["scalable_class_creation"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
