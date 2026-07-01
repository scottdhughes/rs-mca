#!/usr/bin/env sage
"""Exact high-buffer pairclass before split audit."""

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
BUFFER_TARGET = 420
SOURCE_B27 = 577
SOURCE_B37 = 576
POST_SPLIT_B27 = 593
POST_SPLIT_B37 = 592
BASE_COLLAPSE = [[1, 4, 5, 6, 7], [3], [2]]

SCRIPT_PATH = Path("experimental/scripts/audit_m1_a327_high_buffer_pairclass_before_split.sage")
SLACK_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_slack_split_selector.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_high_buffer_pairclass_before_split.py")
DATA_PATH = Path("experimental/data/m1_a327_high_buffer_pairclass_before_split.json")

BUFFER_BUDGETS = [32, 64, 96, 128]
BUFFER_FAMILIES = [
    "pair57_buffer",
    "all_capacity_buffer",
    "pair27_37_plus_capacity",
    "quotient_fiber_buffer",
    "mixed_buffer",
]
FREE_PATTERN = "d2_first_free"
CASE_TIMEOUT_SECONDS = 135


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


def buffer_positions(ledger, count, family):
    rows = [row for row in ledger["coordinate_rows"] if not row["is_occupied_by_pairclass_or_partial"]]
    if family == "quotient_fiber_buffer":
        rows = sorted(rows, key=lambda row: (row["quotient_fiber"], -row["capacity_contribution"], row["coordinate"]))
        out = []
        used_fibers = set()
        for row in rows:
            if row["quotient_fiber"] in used_fibers:
                continue
            out.append(int(row["coordinate"]))
            used_fibers.add(row["quotient_fiber"])
            if len(out) >= count:
                break
        if len(out) >= count:
            return out
    ranked = sorted(rows, key=lambda row: (row["capacity_contribution"], row["B57_contribution"], -row["coordinate"]), reverse=True)
    return [int(row["coordinate"]) for row in ranked[:count]]


def spec(left, right, position, kind):
    return {
        "left": int(left),
        "right": int(right),
        "position": int(position),
        "gamma": 0,
        "kind": kind,
    }


def buffer_specs(ledger, family, budget):
    positions = buffer_positions(ledger, max(1, int(budget)), family)
    specs = []
    if family == "pair57_buffer":
        cycle = [(5, 7)]
    elif family == "all_capacity_buffer":
        cycle = [(4, 7), (5, 7), (6, 7), (1, 7)]
    elif family == "pair27_37_plus_capacity":
        cycle = [(2, 7), (3, 7), (5, 7), (6, 7)]
    elif family == "quotient_fiber_buffer":
        cycle = [(5, 7), (6, 7), (4, 7), (1, 7)]
    elif family == "mixed_buffer":
        cycle = [(2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (1, 7)]
    else:
        raise ValueError("unknown buffer family: %s" % family)
    for idx in range(int(budget)):
        pos = positions[idx % len(positions)]
        left, right = cycle[idx % len(cycle)]
        specs.append(spec(left, right, pos, family))
    return specs


def known_split_specs(slack):
    return slack.split_kind_specs("split_6_keep1457", 1)


def independent_system(F, residual, rows, rhs):
    coefficient = Matrix(F, rows, ncols=residual.VARIABLE_COUNT)
    pivot_rows = [int(row) for row in coefficient.pivot_rows()]
    coefficient_rank = len(pivot_rows)
    selected_rows = [rows[idx] for idx in pivot_rows]
    selected_rhs = [rhs[idx] for idx in pivot_rows]
    return selected_rows, selected_rhs, {
        "row_count": len(rows),
        "effective_row_count": len(selected_rows),
        "rank_after": coefficient_rank,
        "nullity_after": residual.VARIABLE_COUNT - coefficient_rank,
        "row_reduction": "pivot_row_subset",
    }


def solve_with_specs(scalable, residual, F, base, specs):
    rows_pin, rhs_pin = scalable.pin_rows(residual, F, base["powers"], specs)
    rows = base["rows"] + rows_pin
    rhs = base["rhs"] + rhs_pin
    independent_rows, independent_rhs, system_meta = independent_system(F, residual, rows, rhs)
    if independent_rows is None:
        return None, system_meta
    A = Matrix(F, independent_rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    pivot_matrix = A.matrix_from_columns(pivots[: len(independent_rows)]) if len(pivots) >= len(independent_rows) else None
    if pivot_matrix is None:
        return None, {
            **system_meta,
            "solve_status": "HIGH_BUFFER_INCONSISTENT",
            "error": "rank below row count",
        }
    free_values = residual.free_assignments(F, FREE_PATTERN, pivots)
    vector_value, status, error = scalable.solve_with_prepared_matrix(
        F, A, vector(F, independent_rhs), free_values, pivots, pivot_matrix
    )
    meta = {
        **system_meta,
        "solve_status": status,
    }
    if vector_value is None:
        meta["error"] = error
    return vector_value, meta


def evaluate(scalable, residual, F, base, vector_value, metadata):
    row = scalable.evaluate_with_failure(residual, F, base["powers"], vector_value, metadata)
    row["capacity_buffer"] = row["capacity_upper_bound"] >= BUFFER_TARGET
    row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
    row["pair57_preserving"] = row["pair_B_values"][4] >= PAIR_TARGET
    row["pair27_37_at_least_source"] = row["pair_B_values"][1] >= SOURCE_B27 and row["pair_B_values"][2] >= SOURCE_B37
    row["pair27_37_at_least_post_split"] = row["pair_B_values"][1] >= POST_SPLIT_B27 and row["pair_B_values"][2] >= POST_SPLIT_B37
    row["collapse_reduced"] = collapse_reduced(row["degenerate_classes"])
    return row


def classify(pre, post):
    if pre is None or post is None:
        return "BUFFER_INCONSISTENT"
    if pre["capacity_upper_bound"] < BUFFER_TARGET:
        return "BUFFER_NOT_CREATED"
    if pre["six_class_dominance"] > 0:
        return "BUFFER_CREATES_COLLAPSE"
    if pre["pair_B_values"][1] < SOURCE_B27 or pre["pair_B_values"][2] < SOURCE_B37:
        return "BUFFER_KILLS_PAIR27_37"
    if post["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "SPLIT_CONSUMES_BUFFER"
    if post["pair_B_values"][4] < PAIR_TARGET:
        return "SPLIT_PAIR57_LOSS"
    if post.get("exact_max_min") is not None and post["exact_max_min"] >= TARGET_AGREEMENT:
        return "HIGH_BUFFER_EXACT_CANDIDATE"
    return "SPLIT_LOW_RESCHEDULE"


def vector_sort_key(row):
    post = row.get("post_split") or {}
    pre = row.get("pre_split") or {}
    exact_max = -1 if post.get("exact_max_min") is None else post["exact_max_min"]
    return (
        row.get("failure_mode") == "HIGH_BUFFER_EXACT_CANDIDATE",
        post.get("capacity_upper_bound", -1) >= TARGET_AGREEMENT,
        pre.get("capacity_upper_bound", -1) >= BUFFER_TARGET,
        post.get("pair57_preserving") is True,
        post.get("collapse_reduced") is True,
        exact_max,
        post.get("capacity_upper_bound", -1),
        pre.get("capacity_upper_bound", -1),
    )


def setup(slack):
    scalable = slack.load_source_module(slack.SCALABLE_AUDIT_PATH, "pairclass_scalable_helpers_buffer")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_buffer")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_buffer")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    base = slack.setup_base(scalable, residual, F, powers)
    base["powers"] = powers
    base_vector = slack.solve_base_vector(scalable, residual, F, base)
    ledger = slack.ledger_from_base(residual, F, powers, base, base_vector)
    return scalable, residual, F, base, ledger


def case_record(case):
    slack = load_source_module(SLACK_AUDIT_PATH, "capacity_slack_helpers_buffer_case")
    scalable, residual, F, base, ledger = setup(slack)
    buffer = buffer_specs(ledger, case["buffer_family"], case["buffer_rows"])
    split = known_split_specs(slack)
    start = time.time()
    pre_vector, pre_solve = solve_with_specs(scalable, residual, F, base, buffer)
    pre = None
    if pre_vector is not None:
        pre = evaluate(
            scalable,
            residual,
            F,
            base,
            pre_vector,
            {
                **case,
                "phase": "pre_split",
                "free_pattern": FREE_PATTERN,
                "buffer_specs": buffer,
                **pre_solve,
            },
        )
    post_vector, post_solve = solve_with_specs(scalable, residual, F, base, buffer + split)
    post = None
    if post_vector is not None:
        post = evaluate(
            scalable,
            residual,
            F,
            base,
            post_vector,
            {
                **case,
                "phase": "post_split",
                "free_pattern": FREE_PATTERN,
                "buffer_specs": buffer,
                "split_specs": split,
                **post_solve,
            },
        )
    failure = classify(pre, post)
    capacity_loss = None
    if pre is not None and post is not None:
        capacity_loss = pre["capacity_upper_bound"] - post["capacity_upper_bound"]
    return {
        **case,
        "buffer_specs": buffer,
        "split_specs": split,
        "pre_split": pre,
        "pre_split_solve": pre_solve,
        "post_split": post,
        "post_split_solve": post_solve,
        "capacity_loss": capacity_loss,
        "elapsed_seconds": float(round(float(time.time() - start), 3)),
        "failure_mode": failure,
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
            "failure_mode": "HIGH_BUFFER_TIMEOUT",
            "timeout_seconds": CASE_TIMEOUT_SECONDS,
        }
    if completed.returncode != 0:
        return {
            **case,
            "failure_mode": "BUFFER_INCONSISTENT",
            "returncode": completed.returncode,
            "stderr_tail": completed.stderr[-2000:],
        }
    try:
        return json.loads(completed.stdout)
    except Exception as exc:
        return {
            **case,
            "failure_mode": "BUFFER_INCONSISTENT",
            "error": str(exc),
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        }


def cases():
    return [
        {"buffer_rows": int(rows), "buffer_family": family}
        for rows in BUFFER_BUDGETS
        for family in BUFFER_FAMILIES
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "high_buffer_ledger")
    results = [run_child(case) for case in cases()]
    best = sorted(results, key=vector_sort_key, reverse=True)[0] if results else None
    search = {
        "exact_field": "GF(17^32)",
        "base_system": "scalable_pairclass_overlap_all_extension96",
        "buffer_rows": BUFFER_BUDGETS,
        "buffer_families": BUFFER_FAMILIES,
        "split_family": "known_best_split_6_keep1457_at_1",
        "free_pattern": FREE_PATTERN,
        "systems_tested": len(results),
        "pre_split_vectors": sum(1 for row in results if row.get("pre_split") is not None),
        "post_split_vectors": sum(1 for row in results if row.get("post_split") is not None),
        "pre_split_capacity_target": BUFFER_TARGET,
        "capacity_buffer_vectors": sum(
            1 for row in results if (row.get("pre_split") or {}).get("capacity_upper_bound", 0) >= BUFFER_TARGET
        ),
        "post_split_capacity_preserving_vectors": sum(
            1 for row in results if (row.get("post_split") or {}).get("capacity_upper_bound", 0) >= TARGET_AGREEMENT
        ),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "HIGH_BUFFER_TIMEOUT"),
        "failure_mode_counts": failure_counts(results),
        "best_pre_split_capacity": None if best is None or best.get("pre_split") is None else best["pre_split"]["capacity_upper_bound"],
        "best_post_split_capacity": None if best is None or best.get("post_split") is None else best["post_split"]["capacity_upper_bound"],
        "best_pair_B_values": None if best is None or best.get("post_split") is None else best["post_split"]["pair_B_values"],
        "best_collapse_pattern": None if best is None or best.get("post_split") is None else best["post_split"]["degenerate_classes"],
        "best_exact_max_min": None if best is None or best.get("post_split") is None else best["post_split"].get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    return jsonable(ledger_scan.build_record(high_buffer_search=search))


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
        print("SAGE_AUDIT_M1_A327_HIGH_BUFFER_PAIRCLASS_BEFORE_SPLIT_OK")
        print("systems_tested: %d" % record["high_buffer_search"]["systems_tested"])
        print("capacity_buffer_vectors: %d" % record["high_buffer_search"]["capacity_buffer_vectors"])
        print("post_split_capacity_preserving_vectors: %d" % record["high_buffer_search"]["post_split_capacity_preserving_vectors"])
        print("best_failure_mode: %s" % record["high_buffer_search"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
