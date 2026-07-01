#!/usr/bin/env sage
"""Exact compensated split-and-replace audit."""

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
SOURCE_B27 = 593
SOURCE_B37 = 592
BASE_COLLAPSE = [[1, 4, 5, 6, 7], [3], [2]]

SCRIPT_PATH = Path("experimental/scripts/audit_m1_a327_compensated_split_replace.sage")
SLACK_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_slack_split_selector.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_compensated_split_replace.py")
DATA_PATH = Path("experimental/data/m1_a327_compensated_split_replace.json")

SPLIT_CANDIDATES = 5
EXCHANGE_TYPES = [
    "one_for_one_same_fiber",
    "one_for_two_same_fiber",
    "one_for_two_neighbor_fiber",
    "one_for_two_balanced",
    "one_for_two_pair57_restore",
    "one_for_two_capacity_backfill",
]
FREE_PATTERN = "d2_first_free"
CASE_TIMEOUT_SECONDS = 110


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


def replacement_witnesses(split_kind):
    if split_kind == "split_6_keep1457":
        return [6]
    if split_kind == "split_4_keep1567":
        return [4]
    if split_kind == "split_46_keep157":
        return [4, 6]
    raise ValueError("unknown split kind: %s" % split_kind)


def replacement_spec(witness, position, kind):
    return {
        "left": int(witness),
        "right": 7,
        "position": int(position),
        "gamma": 0,
        "kind": kind,
    }


def candidate_positions(ledger, split_candidate, mode, count):
    split_coord = int(split_candidate["coordinate"])
    split_fiber = split_coord % 16
    occupied = {
        int(row["coordinate"])
        for row in ledger["coordinate_rows"]
        if row["is_occupied_by_pairclass_or_partial"]
    }
    rows = [
        row
        for row in ledger["coordinate_rows"]
        if int(row["coordinate"]) != split_coord and int(row["coordinate"]) not in occupied
    ]
    if mode == "one_for_one_same_fiber" or mode == "one_for_two_same_fiber":
        ranked = [row for row in rows if int(row["quotient_fiber"]) == split_fiber]
    elif mode == "one_for_two_neighbor_fiber":
        ranked = [
            row
            for row in rows
            if int(row["quotient_fiber"]) in {(split_fiber - 1) % 16, split_fiber, (split_fiber + 1) % 16}
        ]
    elif mode == "one_for_two_balanced":
        ranked = sorted(rows, key=lambda row: (row["quotient_fiber"], -row["capacity_contribution"], row["coordinate"]))
    elif mode == "one_for_two_pair57_restore":
        ranked = sorted(rows, key=lambda row: (row["B57_contribution"], row["capacity_contribution"], -row["coordinate"]), reverse=True)
    elif mode == "one_for_two_capacity_backfill":
        ranked = sorted(rows, key=lambda row: (row["capacity_contribution"], row["B57_contribution"], -row["coordinate"]), reverse=True)
    else:
        raise ValueError("unknown exchange type: %s" % mode)
    if mode in {"one_for_one_same_fiber", "one_for_two_same_fiber", "one_for_two_neighbor_fiber"}:
        ranked = sorted(ranked, key=lambda row: (row["capacity_contribution"], row["B57_contribution"], -row["coordinate"]), reverse=True)
    out = []
    seen_fibers = set()
    for row in ranked:
        if mode == "one_for_two_balanced" and row["quotient_fiber"] in seen_fibers:
            continue
        out.append(int(row["coordinate"]))
        seen_fibers.add(row["quotient_fiber"])
        if len(out) >= count:
            break
    if len(out) < count:
        for row in rows:
            pos = int(row["coordinate"])
            if pos not in out:
                out.append(pos)
                if len(out) >= count:
                    break
    return out[:count]


def compensated_specs(slack, ledger, split_candidate, exchange_type):
    split = slack.split_kind_specs(split_candidate["split_kind"], split_candidate["coordinate"])
    replacement_count = 1 if exchange_type == "one_for_one_same_fiber" else 2
    positions = candidate_positions(ledger, split_candidate, exchange_type, replacement_count)
    replacements = []
    for idx, pos in enumerate(positions):
        witnesses = replacement_witnesses(split_candidate["split_kind"])
        witness = witnesses[idx % len(witnesses)]
        replacements.append(replacement_spec(witness, pos, exchange_type))
    return split, replacements


def classify(row):
    if row.get("pair_B_values") is None:
        return "COMP_SPLIT_INCONSISTENT"
    if row["pair_B_values"][4] < PAIR_TARGET:
        return "COMP_SPLIT_PAIR57_LOSS"
    if not row.get("collapse_reduced"):
        return "COMP_SPLIT_COLLAPSE_RETURNS"
    if row["pair_B_values"][1] < SOURCE_B27 or row["pair_B_values"][2] < SOURCE_B37:
        return "COMP_SPLIT_PAIR27_37_STALLS"
    if row.get("capacity_upper_bound", 0) < TARGET_AGREEMENT:
        return "COMP_SPLIT_CAPACITY_NOT_RESTORED"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "COMP_SPLIT_EXACT_CANDIDATE"
    return "COMP_SPLIT_LOW_RESCHEDULE"


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "COMP_SPLIT_EXACT_CANDIDATE",
        row.get("capacity_restored") is True,
        row.get("pair57_preserving") is True,
        row.get("pair27_37_improved") is True,
        row.get("collapse_reduced") is True,
        exact_max,
        row.get("capacity_upper_bound", -1),
        min(pair_values[1], pair_values[2], pair_values[4]),
        row.get("distinct_codewords") is True,
    )


def setup(slack_module):
    scalable = slack_module.load_source_module(slack_module.SCALABLE_AUDIT_PATH, "pairclass_scalable_helpers_comp")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_comp")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_comp")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    base = slack_module.setup_base(scalable, residual, F, powers)
    base_vector = slack_module.solve_base_vector(scalable, residual, F, base)
    ledger = slack_module.ledger_from_base(residual, F, powers, base, base_vector)
    split_candidates = ledger["candidate_split_rows"][:SPLIT_CANDIDATES]
    return scalable, residual, F, powers, base, ledger, split_candidates


def case_record(case):
    slack = load_source_module(SLACK_AUDIT_PATH, "capacity_slack_helpers_comp_case")
    scalable, residual, F, powers, base, ledger, split_candidates = setup(slack)
    split_candidate = split_candidates[int(case["split_candidate_index"])]
    split, replacements = compensated_specs(slack, ledger, split_candidate, case["exchange_type"])
    specs = split + replacements
    rows_pin, rhs_pin = scalable.pin_rows(residual, F, powers, specs)
    rows = base["rows"] + rows_pin
    rhs = base["rhs"] + rhs_pin
    start = time.time()
    A = Matrix(F, rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    rank_after = len(pivots)
    nullity_after = residual.VARIABLE_COUNT - rank_after
    pivot_matrix = A.matrix_from_columns(pivots[: len(rows)]) if rank_after >= len(rows) else None
    if pivot_matrix is None:
        return {
            **case,
            "split_candidate": split_candidate,
            "split_specs": split,
            "replacement_specs": replacements,
            "row_count": len(rows),
            "rank_after": rank_after,
            "nullity_after": nullity_after,
            "failure_mode": "COMP_SPLIT_INCONSISTENT",
            "vector_results": [],
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    free_values = residual.free_assignments(F, FREE_PATTERN, pivots)
    vector_value, status, error = scalable.solve_with_prepared_matrix(
        F, A, vector(F, rhs), free_values, pivots, pivot_matrix
    )
    metadata = {
        **case,
        "free_pattern": FREE_PATTERN,
        "row_count": len(rows),
        "protected_rows": base["protected_rows"],
        "base_creation_rows": base["base_creation_rows"],
        "extension_rows": base["extension_rows"],
        "split_candidate": split_candidate,
        "split_specs": split,
        "replacement_specs": replacements,
        "replacement_rows": len(replacements),
        "rank_after": rank_after,
        "nullity_after": nullity_after,
        "solve_status": status,
    }
    if vector_value is None:
        return {
            **metadata,
            "failure_mode": "COMP_SPLIT_INCONSISTENT",
            "error": error,
            "vector_results": [],
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    row = scalable.evaluate_with_failure(residual, F, powers, vector_value, metadata)
    row["capacity_restored"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
    row["pair57_preserving"] = row["pair_B_values"][4] >= PAIR_TARGET
    row["pair27_37_improved"] = row["pair_B_values"][1] >= SOURCE_B27 and row["pair_B_values"][2] >= SOURCE_B37
    row["collapse_reduced"] = collapse_reduced(row["degenerate_classes"])
    row["failure_mode"] = classify(row)
    row["elapsed_seconds"] = float(round(float(time.time() - start), 3))
    return {
        **case,
        "split_candidate": split_candidate,
        "split_specs": split,
        "replacement_specs": replacements,
        "row_count": len(rows),
        "rank_after": rank_after,
        "nullity_after": nullity_after,
        "elapsed_seconds": row["elapsed_seconds"],
        "best": row,
        "vector_results": [row],
        "failure_mode": row["failure_mode"],
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
            "failure_mode": "COMP_SPLIT_TIMEOUT",
            "timeout_seconds": CASE_TIMEOUT_SECONDS,
            "vector_results": [],
        }
    if completed.returncode != 0:
        return {
            **case,
            "failure_mode": "COMP_SPLIT_INCONSISTENT",
            "returncode": completed.returncode,
            "stderr_tail": completed.stderr[-2000:],
            "vector_results": [],
        }
    try:
        return json.loads(completed.stdout)
    except Exception as exc:
        return {
            **case,
            "failure_mode": "COMP_SPLIT_INCONSISTENT",
            "error": str(exc),
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
            "vector_results": [],
        }


def cases():
    return [
        {"split_candidate_index": int(index), "exchange_type": exchange_type}
        for index in range(SPLIT_CANDIDATES)
        for exchange_type in EXCHANGE_TYPES
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "compensated_split_ledger")
    results = [run_child(case) for case in cases()]
    vectors = [row for result in results for row in result.get("vector_results", [])]
    best_pool = vectors or [row.get("best", row) for row in results]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    exchange = {
        "exact_field": "GF(17^32)",
        "base_system": "scalable_pairclass_overlap_all_extension96",
        "split_candidates": SPLIT_CANDIDATES,
        "exchange_types": EXCHANGE_TYPES,
        "free_pattern": FREE_PATTERN,
        "case_timeout_seconds": CASE_TIMEOUT_SECONDS,
        "systems_tested": len(results),
        "exact_vectors_constructed": sum(1 for row in vectors if row.get("distinct_codewords") is not None),
        "capacity_restored_vectors": sum(1 for row in vectors if row.get("capacity_restored") is True),
        "pair27_37_improved_vectors": sum(1 for row in vectors if row.get("pair27_37_improved") is True),
        "pair57_preserving_vectors": sum(1 for row in vectors if row.get("pair57_preserving") is True),
        "collapse_reduced_vectors": sum(1 for row in vectors if row.get("collapse_reduced") is True),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "COMP_SPLIT_TIMEOUT"),
        "failure_mode_counts": failure_counts(vectors or results),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_collapse_pattern": None if best is None else best.get("degenerate_classes"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    return jsonable(ledger_scan.build_record(compensated_exchange=exchange))


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
        print("SAGE_AUDIT_M1_A327_COMPENSATED_SPLIT_REPLACE_OK")
        print("systems_tested: %d" % record["compensated_exchange"]["systems_tested"])
        print("exact_vectors_constructed: %d" % record["compensated_exchange"]["exact_vectors_constructed"])
        print("capacity_restored_vectors: %d" % record["compensated_exchange"]["capacity_restored_vectors"])
        print("best_failure_mode: %s" % record["compensated_exchange"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
