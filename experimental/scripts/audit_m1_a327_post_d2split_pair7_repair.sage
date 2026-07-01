#!/usr/bin/env sage
"""Exact post-D2-split pair-7 repair audit."""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path


TARGET_AGREEMENT = 327
PAIR7_TARGET = 2 * TARGET_AGREEMENT
LOW_COLLAPSE_THRESHOLD = 20

EXACT_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py")
CAPACITY_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_preserving_residual12_split.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_post_d2split_pair7_repair.py")
DATA_PATH = Path("experimental/data/m1_a327_post_d2split_pair7_repair.json")

BASE_PARTIAL_FAMILIES = ["one_pair_13"]
BASE_FREE_PATTERNS = ["d2_first_free", "d2_first4_free", "d2_even_sparse"]
REPAIR_POSITION_LIMIT = 4


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


def repair_positions(capacity, selected, partial_specs):
    used = {int(spec["position"]) for spec in partial_specs}
    out = []
    for pos in capacity.safe_positions(selected):
        if int(pos) in used:
            continue
        out.append(int(pos))
        if len(out) >= REPAIR_POSITION_LIMIT:
            break
    return out


def repair_specs_at_position(pos):
    return [
        {
            "repair_family": "pair_27",
            "pin_specs": [
                {"left": 2, "right": 7, "position": int(pos), "gamma": 0, "kind": "pair7_repair"}
            ],
        },
        {
            "repair_family": "pair_37",
            "pin_specs": [
                {"left": 3, "right": 7, "position": int(pos), "gamma": 0, "kind": "pair7_repair"}
            ],
        },
        {
            "repair_family": "triple_237",
            "pin_specs": [
                {"left": 2, "right": 7, "position": int(pos), "gamma": 0, "kind": "pair7_repair"},
                {"left": 3, "right": 7, "position": int(pos), "gamma": 0, "kind": "pair7_repair"},
            ],
        },
    ]


def repair_pin_rows(residual, F, powers, specs):
    rows = []
    rhs = []
    for spec in specs:
        rows.append(residual.evaluation_row(F, powers, spec["left"], spec["right"], spec["position"]))
        rhs.append(F(0))
    return rows, rhs


def d2_split_from_classes(degenerate_classes):
    return not any(1 in row and 2 in row for row in degenerate_classes)


def classify(row):
    if not row["d2_split"]:
        return "POST_D2_PAIR7_REPAIR_UNDOES_D2_SPLIT"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "POST_D2_PAIR7_REPAIR_CAPACITY_LOSS"
    if row["six_class_dominance"] > LOW_COLLAPSE_THRESHOLD:
        return "POST_D2_PAIR7_REPAIR_COLLAPSE_RETURNS"
    if row["min_pair_B"] < PAIR7_TARGET:
        return "POST_D2_PAIR7_NOT_REPAIRED"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "POST_D2_EXACT_CANDIDATE"
    return "POST_D2_PAIR7_REPAIR_LOW_RESCHEDULE"


def evaluate_with_failure(capacity, residual, F, powers, vector_value, metadata):
    row = residual.evaluate_vector(F, powers, vector_value, metadata)
    row["d2_split"] = d2_split_from_classes(row["degenerate_classes"])
    row["capacity_preserving"] = bool(row["capacity_upper_bound"] >= TARGET_AGREEMENT)
    row["low_collapse"] = bool(row["six_class_dominance"] <= LOW_COLLAPSE_THRESHOLD)
    row["pair27_B"] = row["pair_B_values"][1]
    row["pair37_B"] = row["pair_B_values"][2]
    row["pair27_repaired"] = bool(row["pair27_B"] >= PAIR7_TARGET)
    row["pair7_repaired"] = bool(row["min_pair_B"] >= PAIR7_TARGET)
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
        row.get("failure_mode") == "POST_D2_EXACT_CANDIDATE",
        row.get("pair7_repaired") is True,
        row.get("pair27_repaired") is True,
        row.get("d2_split") is True,
        row.get("capacity_preserving") is True,
        row.get("low_collapse") is True,
        exact_max,
        row.get("min_pair_B", -1),
        row.get("pair27_B", -1),
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
    results = []
    base_results = []

    for family in BASE_PARTIAL_FAMILIES:
        partial_specs = capacity.partial_split_specs(selected, family)
        partial_rows, partial_rhs = residual.pin_rows(F, powers, partial_specs)
        base_rows = target_rows + partial_rows
        base_rhs = [F(0)] * len(target_rows) + partial_rhs
        base_matrix = Matrix(F, base_rows, ncols=residual.VARIABLE_COUNT)
        base_pivots = [int(col) for col in base_matrix.pivots()]

        for pattern in BASE_FREE_PATTERNS:
            free_values = residual.free_assignments(F, pattern, base_pivots)
            vector_value, status, error, _pivots = residual.solve_with_free(F, base_rows, base_rhs, free_values)
            base_metadata = {
                "candidate_id": row["target_system_id"],
                "search_layer": "base_d2split_vector",
                "partial_split_family": family,
                "free_pattern": pattern,
                "pin_specs": partial_specs,
                "solve_status": status,
            }
            if vector_value is None:
                base_results.append({**base_metadata, "failure_mode": status, "error": error})
                continue
            base_results.append(evaluate_with_failure(capacity, residual, F, powers, vector_value, base_metadata))

            for pos in repair_positions(capacity, selected, partial_specs):
                for repair in repair_specs_at_position(pos):
                    repair_rows, repair_rhs = repair_pin_rows(residual, F, powers, repair["pin_specs"])
                    vector_value, status, error, _pivots = residual.solve_with_free(
                        F,
                        base_rows + repair_rows,
                        base_rhs + repair_rhs,
                        free_values,
                    )
                    metadata = {
                        "candidate_id": row["target_system_id"],
                        "search_layer": "post_d2_pair7_repair_pin",
                        "partial_split_family": family,
                        "free_pattern": pattern,
                        "repair_family": repair["repair_family"],
                        "repair_position": int(pos),
                        "repair_pin_specs": repair["pin_specs"],
                        "pin_specs": partial_specs + repair["pin_specs"],
                        "solve_status": status,
                    }
                    if vector_value is None:
                        results.append({**metadata, "failure_mode": status, "error": error})
                        continue
                    results.append(evaluate_with_failure(capacity, residual, F, powers, vector_value, metadata))

    all_rows = base_results + results
    best = sorted(all_rows, key=vector_sort_key, reverse=True)[0]
    return {
        "candidate_id": row["target_system_id"],
        "proxy_max_min": row["best"]["proxy_max_min"],
        "proxy_pair_B_values": row["best"]["pair7_B_values"],
        "protected_rows": len(target_rows),
        "base_vector_count": len(base_results),
        "repair_attempt_count": len(results),
        "failure_mode_counts": failure_counts(all_rows),
        "best": best,
        "base_results": base_results,
        "vector_results": results,
        "retained_results": sorted(all_rows, key=vector_sort_key, reverse=True)[:12],
    }


def audit_record():
    exact_scan = load_python_module(EXACT_SCAN_PATH, "protected_exchange_exact_scan")
    capacity = load_source_module(CAPACITY_AUDIT_PATH, "capacity_preserving_residual12")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_for_pair7")
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "post_d2_pair7_ledger")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    source = exact_scan.source_record()
    candidates = exact_scan.proxy_candidate_rows(source)
    results = [evaluate_candidate(exact_scan, capacity, residual, row, F, powers) for row in candidates]
    vectors = [row for result in results for row in result["vector_results"]]
    all_rows = [row for result in results for row in result["base_results"] + result["vector_results"]]
    best = sorted(all_rows, key=vector_sort_key, reverse=True)[0] if all_rows else None
    search = {
        "exact_field": "GF(17^32)",
        "field_denominator": str(q),
        "base_vectors_tested": sum(result["base_vector_count"] for result in results),
        "pin_sets_tested": sum(result["repair_attempt_count"] for result in results),
        "nullspace_samples_tested": sum(result["base_vector_count"] for result in results),
        "exact_vectors_constructed": sum(1 for row in all_rows if row.get("distinct_codewords") is not None),
        "d2_split_retained": sum(1 for row in all_rows if row.get("d2_split") is True),
        "capacity_preserving_vectors": sum(1 for row in all_rows if row.get("capacity_preserving") is True),
        "low_collapse_capacity_preserving_vectors": sum(
            1 for row in all_rows if row.get("capacity_preserving") is True and row.get("low_collapse") is True
        ),
        "pair27_repaired_vectors": sum(1 for row in all_rows if row.get("pair27_repaired") is True),
        "pair7_repaired_vectors": sum(1 for row in all_rows if row.get("pair7_repaired") is True),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_degenerate_classes": None if best is None else best.get("degenerate_classes"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    record = ledger_scan.build_record(post_d2_pair7_repair=search)
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
        print("SAGE_AUDIT_M1_A327_POST_D2SPLIT_PAIR7_REPAIR_OK")
        print("base_vectors_tested: %d" % record["post_d2_pair7_repair"]["base_vectors_tested"])
        print("pin_sets_tested: %d" % record["post_d2_pair7_repair"]["pin_sets_tested"])
        print("d2_split_retained: %d" % record["post_d2_pair7_repair"]["d2_split_retained"])
        print("pair27_repaired_vectors: %d" % record["post_d2_pair7_repair"]["pair27_repaired_vectors"])
        print("pair7_repaired_vectors: %d" % record["post_d2_pair7_repair"]["pair7_repaired_vectors"])
        print("best_failure_mode: %s" % record["post_d2_pair7_repair"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
