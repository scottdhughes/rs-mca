#!/usr/bin/env sage
"""Exact reserve/pairclass co-design before split audit."""

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
PRE_CAPACITY_TARGET = 430
PRE_B27_TARGET = 640
PRE_B37_TARGET = 640
BASE_SOURCE_B27 = 608
BASE_SOURCE_B37 = 608
BASE_COLLAPSE = [[1, 4, 5, 6, 7], [3], [2]]

SCRIPT_PATH = Path("experimental/scripts/audit_m1_a327_reserve_pairclass_codesign_before_split.sage")
SLACK_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_slack_split_selector.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_reserve_pairclass_codesign_before_split.py")
DATA_PATH = Path("experimental/data/m1_a327_reserve_pairclass_codesign_before_split.json")

ROW_EXTENSION_SIZES = [64, 96, 128, 160]
ROW_FAMILIES = [
    "pair27_37_plus_capacity",
    "pair27_37_plus_57_guard",
    "quotient_fiber_buffer",
    "mixed_buffer_pairclass",
    "postsplit_survivor_rows",
]
FREE_PATTERN = "d2_first_free"
CASE_TIMEOUT_SECONDS = 210


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


def spec(left, right, position, kind, delta=None):
    row = {
        "left": int(left),
        "right": int(right),
        "position": int(position),
        "gamma": 0,
        "kind": kind,
    }
    if delta is not None:
        row["delta"] = delta
    return row


def pair_gain(row, pair_key, left, right):
    if {int(left), int(right)} == set(pair_key):
        return max(0, 2 - int(row[pair_key_to_field(pair_key)]))
    return 0


def pair_key_to_field(pair_key):
    if pair_key == (2, 7):
        return "B27_contribution"
    if pair_key == (3, 7):
        return "B37_contribution"
    if pair_key == (5, 7):
        return "B57_contribution"
    return "capacity_contribution"


def candidate_delta(row, left, right, family):
    b27_gain = pair_gain(row, (2, 7), left, right)
    b37_gain = pair_gain(row, (3, 7), left, right)
    b57_gain = pair_gain(row, (5, 7), left, right)
    capacity_delta = max(0, 5 - int(row["capacity_contribution"]))
    if int(row["capacity_contribution"]) >= 5:
        capacity_delta += 1
    post_capacity_delta = capacity_delta
    if int(row["coordinate"]) == 1:
        post_capacity_delta -= 4
    if int(row["quotient_fiber"]) == 1:
        post_capacity_delta -= 1
    post_B27_delta = b27_gain
    post_B37_delta = b37_gain
    post_B57_delta = b57_gain
    score = (
        10 * post_capacity_delta
        + 12 * post_B27_delta
        + 12 * post_B37_delta
        + 8 * post_B57_delta
        + int(row["capacity_contribution"])
        + int(row["B57_contribution"])
        - (6 if int(row["quotient_fiber"]) == 1 else 0)
    )
    if family == "postsplit_survivor_rows":
        score += 6 * post_capacity_delta
    if family == "pair27_37_plus_capacity":
        score += 4 * (post_B27_delta + post_B37_delta)
    if family == "pair27_37_plus_57_guard":
        score += 3 * (post_B27_delta + post_B37_delta + post_B57_delta)
    return {
        "coordinate": int(row["coordinate"]),
        "quotient_fiber": int(row["quotient_fiber"]),
        "left": int(left),
        "right": int(right),
        "pre_capacity_delta": int(capacity_delta),
        "post_capacity_delta": int(post_capacity_delta),
        "pre_B27_delta": int(b27_gain),
        "post_B27_delta": int(post_B27_delta),
        "pre_B37_delta": int(b37_gain),
        "post_B37_delta": int(post_B37_delta),
        "pre_B57_delta": int(b57_gain),
        "post_B57_delta": int(post_B57_delta),
        "collapse_delta": 0,
        "score": int(score),
        "family": family,
    }


def pair_cycle(family):
    if family == "pair27_37_plus_capacity":
        return [(2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
    if family == "pair27_37_plus_57_guard":
        return [(2, 7), (3, 7), (5, 7), (2, 7), (3, 7), (1, 7), (4, 7)]
    if family == "quotient_fiber_buffer":
        return [(2, 7), (3, 7), (5, 7), (6, 7), (4, 7)]
    if family == "mixed_buffer_pairclass":
        return [(2, 7), (3, 7), (5, 7), (4, 7), (6, 7), (1, 7)]
    if family == "postsplit_survivor_rows":
        return [(2, 7), (3, 7), (5, 7), (4, 7), (1, 7), (6, 7)]
    raise ValueError("unknown row family: %s" % family)


def candidate_pool(ledger, family):
    rows = [
        row
        for row in ledger["coordinate_rows"]
        if not row["is_occupied_by_pairclass_or_partial"] and int(row["coordinate"]) != 1
    ]
    candidates = []
    for row in rows:
        for left, right in pair_cycle(family):
            candidates.append(candidate_delta(row, left, right, family))
    if family == "quotient_fiber_buffer":
        candidates = sorted(
            candidates,
            key=lambda row: (row["quotient_fiber"], -row["score"], row["coordinate"], row["left"], row["right"]),
        )
        out = []
        used = {}
        for candidate in candidates:
            fiber = candidate["quotient_fiber"]
            used[fiber] = used.get(fiber, 0)
            if used[fiber] >= 8:
                continue
            out.append(candidate)
            used[fiber] += 1
        return out
    return sorted(
        candidates,
        key=lambda row: (
            row["score"],
            row["post_capacity_delta"],
            row["post_B27_delta"] + row["post_B37_delta"],
            row["post_B57_delta"],
            -row["coordinate"],
        ),
        reverse=True,
    )


def codesign_specs(ledger, family, size):
    pool = candidate_pool(ledger, family)
    if not pool:
        return [], []
    specs = []
    delta_rows = []
    seen = set()
    idx = 0
    while len(specs) < int(size):
        candidate = pool[idx % len(pool)]
        idx += 1
        key = (candidate["left"], candidate["right"], candidate["coordinate"], len(specs) // max(1, len(pool)))
        if key in seen and len(pool) >= int(size):
            continue
        seen.add(key)
        specs.append(spec(candidate["left"], candidate["right"], candidate["coordinate"], family, candidate))
        delta_rows.append(candidate)
        if idx > int(size) * 8 and len(pool) < int(size):
            break
    return specs, delta_rows


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
    A = Matrix(F, independent_rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    pivot_matrix = A.matrix_from_columns(pivots[: len(independent_rows)]) if len(pivots) >= len(independent_rows) else None
    if pivot_matrix is None:
        return None, {
            **system_meta,
            "solve_status": "CODESIGN_INCONSISTENT",
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
    row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
    row["capacity_reserve"] = row["capacity_upper_bound"] >= PRE_CAPACITY_TARGET
    row["pair57_preserving"] = row["pair_B_values"][4] >= PAIR_TARGET
    row["pair27_37_repaired"] = row["pair_B_values"][1] >= PAIR_TARGET and row["pair_B_values"][2] >= PAIR_TARGET
    row["pre_pair27_37_near_target"] = row["pair_B_values"][1] >= PRE_B27_TARGET and row["pair_B_values"][2] >= PRE_B37_TARGET
    row["collapse_reduced"] = collapse_reduced(row["degenerate_classes"])
    return row


def classify(pre, post):
    if pre is None or post is None:
        return "CODESIGN_INCONSISTENT"
    if pre["capacity_upper_bound"] < PRE_CAPACITY_TARGET:
        return "RESERVE_NOT_CREATED"
    if post["six_class_dominance"] > 0 or not post["collapse_reduced"]:
        return "COLLAPSE_RETURNS"
    if post["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "RESERVE_NOT_POSTSPLIT_SURVIVING"
    if post["pair_B_values"][4] < PAIR_TARGET:
        return "PAIR57_GUARD_LOSS"
    if post["pair_B_values"][1] < PAIR_TARGET or post["pair_B_values"][2] < PAIR_TARGET:
        return "PAIRCLASS_NOT_CREATED"
    if post.get("exact_max_min") is not None and post["exact_max_min"] >= TARGET_AGREEMENT:
        return "EXACT_CANDIDATE"
    return "LOW_RESCHEDULE"


def vector_sort_key(row):
    post = row.get("post_split") or {}
    pre = row.get("pre_split") or {}
    exact_max = -1 if post.get("exact_max_min") is None else post["exact_max_min"]
    pair_values = post.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "EXACT_CANDIDATE",
        post.get("capacity_upper_bound", -1) >= TARGET_AGREEMENT,
        pair_values[1] >= PAIR_TARGET and pair_values[2] >= PAIR_TARGET,
        pair_values[4] >= PAIR_TARGET,
        post.get("collapse_reduced") is True,
        exact_max,
        min(pair_values[1], pair_values[2], pair_values[4]),
        post.get("capacity_upper_bound", -1),
        pre.get("capacity_upper_bound", -1),
    )


def setup(slack):
    scalable = slack.load_source_module(slack.SCALABLE_AUDIT_PATH, "pairclass_scalable_helpers_codesign")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_codesign")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_codesign")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    base = slack.setup_base(scalable, residual, F, powers)
    base["powers"] = powers
    base_vector = slack.solve_base_vector(scalable, residual, F, base)
    ledger = slack.ledger_from_base(residual, F, powers, base, base_vector)
    return scalable, residual, F, base, ledger


def delta_summary(rows):
    return {
        "rows": len(rows),
        "pre_capacity_delta": sum(row["pre_capacity_delta"] for row in rows),
        "post_capacity_delta": sum(row["post_capacity_delta"] for row in rows),
        "pre_B27_delta": sum(row["pre_B27_delta"] for row in rows),
        "post_B27_delta": sum(row["post_B27_delta"] for row in rows),
        "pre_B37_delta": sum(row["pre_B37_delta"] for row in rows),
        "post_B37_delta": sum(row["post_B37_delta"] for row in rows),
        "pre_B57_delta": sum(row["pre_B57_delta"] for row in rows),
        "post_B57_delta": sum(row["post_B57_delta"] for row in rows),
        "score": sum(row["score"] for row in rows),
    }


def specs_preview(rows):
    return rows[:12]


def case_record(case):
    slack = load_source_module(SLACK_AUDIT_PATH, "capacity_slack_helpers_codesign_case")
    scalable, residual, F, base, ledger = setup(slack)
    rowspecs, deltas = codesign_specs(ledger, case["row_family"], case["row_extension_size"])
    split = known_split_specs(slack)
    start = time.time()
    pre_vector, pre_solve = solve_with_specs(scalable, residual, F, base, rowspecs)
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
                "codesign_row_count": len(rowspecs),
                "codesign_specs_preview": specs_preview(rowspecs),
                "delta_summary": delta_summary(deltas),
                **pre_solve,
            },
        )
    post_vector, post_solve = solve_with_specs(scalable, residual, F, base, rowspecs + split)
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
                "codesign_row_count": len(rowspecs),
                "codesign_specs_preview": specs_preview(rowspecs),
                "split_specs": split,
                "delta_summary": delta_summary(deltas),
                **post_solve,
            },
        )
    failure = classify(pre, post)
    capacity_loss = None
    if pre is not None and post is not None:
        capacity_loss = pre["capacity_upper_bound"] - post["capacity_upper_bound"]
    pair_gain = None
    if pre is not None and post is not None:
        pair_gain = [
            post["pair_B_values"][idx] - pre["pair_B_values"][idx]
            for idx in range(len(post["pair_B_values"]))
        ]
    return {
        **case,
        "codesign_row_count": len(rowspecs),
        "codesign_specs_preview": specs_preview(rowspecs),
        "split_specs": split,
        "delta_summary": delta_summary(deltas),
        "pre_split": pre,
        "pre_split_solve": pre_solve,
        "post_split": post,
        "post_split_solve": post_solve,
        "capacity_loss": capacity_loss,
        "pair_gain": pair_gain,
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
            "failure_mode": "CODESIGN_TIMEOUT",
            "timeout_seconds": CASE_TIMEOUT_SECONDS,
        }
    if completed.returncode != 0:
        return {
            **case,
            "failure_mode": "CODESIGN_INCONSISTENT",
            "returncode": completed.returncode,
            "stderr_tail": completed.stderr[-2000:],
        }
    try:
        return json.loads(completed.stdout)
    except Exception as exc:
        return {
            **case,
            "failure_mode": "CODESIGN_INCONSISTENT",
            "error": str(exc),
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        }


def cases():
    return [
        {"row_extension_size": int(size), "row_family": family}
        for size in ROW_EXTENSION_SIZES
        for family in ROW_FAMILIES
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "reserve_pairclass_codesign_ledger")
    results = [run_child(case) for case in cases()]
    best = sorted(results, key=vector_sort_key, reverse=True)[0] if results else None
    search = {
        "exact_field": "GF(17^32)",
        "base_systems": ["scalable_pairclass_overlap_all_extension96"],
        "row_extension_sizes": ROW_EXTENSION_SIZES,
        "row_families": ROW_FAMILIES,
        "split_family": "known_best_split_6_keep1457_at_1",
        "free_pattern": FREE_PATTERN,
        "systems_tested": len(results),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "CODESIGN_TIMEOUT"),
        "exact_vectors_constructed": sum(
            int((row.get("pre_split") is not None)) + int((row.get("post_split") is not None))
            for row in results
        ),
        "pre_split_vectors": sum(1 for row in results if row.get("pre_split") is not None),
        "post_split_vectors": sum(1 for row in results if row.get("post_split") is not None),
        "postsplit_capacity_preserving_vectors": sum(
            1 for row in results if (row.get("post_split") or {}).get("capacity_upper_bound", 0) >= TARGET_AGREEMENT
        ),
        "postsplit_pairclass_repaired_vectors": sum(
            1
            for row in results
            if (row.get("post_split") or {}).get("pair_B_values", [0, 0, 0, 0, 0])[1] >= PAIR_TARGET
            and (row.get("post_split") or {}).get("pair_B_values", [0, 0, 0, 0, 0])[2] >= PAIR_TARGET
        ),
        "postsplit_pair57_preserving_vectors": sum(
            1
            for row in results
            if (row.get("post_split") or {}).get("pair_B_values", [0, 0, 0, 0, 0])[4] >= PAIR_TARGET
        ),
        "collapse_reduced_vectors": sum(
            1 for row in results if (row.get("post_split") or {}).get("collapse_reduced") is True
        ),
        "failure_mode_counts": failure_counts(results),
        "best_pre_split_capacity": None if best is None or best.get("pre_split") is None else best["pre_split"]["capacity_upper_bound"],
        "best_post_split_capacity": None if best is None or best.get("post_split") is None else best["post_split"]["capacity_upper_bound"],
        "best_post_split_pair_B_values": None if best is None or best.get("post_split") is None else best["post_split"]["pair_B_values"],
        "best_collapse_pattern": None if best is None or best.get("post_split") is None else best["post_split"]["degenerate_classes"],
        "best_exact_max_min": None if best is None or best.get("post_split") is None else best["post_split"].get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    return jsonable(ledger_scan.build_record(codesign_search=search))


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
        print("SAGE_AUDIT_M1_A327_RESERVE_PAIRCLASS_CODESIGN_BEFORE_SPLIT_OK")
        print("systems_tested: %d" % record["codesign_search"]["systems_tested"])
        print("timeouts: %d" % record["codesign_search"]["timeouts"])
        print("postsplit_capacity_preserving_vectors: %d" % record["codesign_search"]["postsplit_capacity_preserving_vectors"])
        print("postsplit_pairclass_repaired_vectors: %d" % record["codesign_search"]["postsplit_pairclass_repaired_vectors"])
        print("best_failure_mode: %s" % record["codesign_search"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
