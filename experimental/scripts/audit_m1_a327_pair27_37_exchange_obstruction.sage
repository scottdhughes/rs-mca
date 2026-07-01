#!/usr/bin/env sage
"""Exact pair {2,7}/{3,7} exchange-obstruction audit."""

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

EXACT_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_protected_exchange_exact_audit.py")
CAPACITY_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_preserving_residual12_split.sage")
POST_REPAIR_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_post_d2split_pair7_repair.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pair27_37_exchange_obstruction.py")
DATA_PATH = Path("experimental/data/m1_a327_pair27_37_exchange_obstruction.json")

BASE_PARTIAL_FAMILY = "one_pair_13"
BASE_FREE_PATTERNS = ["d2_first_free", "d2_first4_free", "d2_even_sparse"]


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


def pair_mask(left, right):
    return (1 << (left - 1)) | (1 << (right - 1))


def pair_contribution(classes, mask):
    return max((int(row) & int(mask)).bit_count() for row in classes)


def histogram(values):
    out = {}
    for value in values:
        key = str(int(value))
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda item: int(item[0])))


def fiber_histogram(positions):
    out = {}
    for pos in positions:
        key = str(int(pos) % 16)
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda item: int(item[0])))


def d2_split_from_classes(degenerate_classes):
    return not any(1 in row and 2 in row for row in degenerate_classes)


def analyze_vector(residual, F, powers, vector_value, metadata):
    values = residual.exact_values_from_vector(F, powers, vector_value)
    classes = residual.class_masks_by_position(values)
    capacity = residual.capacity_from_class_masks(classes)
    pair7 = residual.pair7_metrics(classes)
    old_three = residual.old_three_subset_metrics(classes)
    degenerate = residual.equivalence_classes(values)
    six_dom = residual.six_class_dominance(classes)
    mask27 = pair_mask(2, 7)
    mask37 = pair_mask(3, 7)
    contrib27 = [pair_contribution(row, mask27) for row in classes]
    contrib37 = [pair_contribution(row, mask37) for row in classes]
    credit27 = [idx for idx, value in enumerate(contrib27) if value == 2]
    credit37 = [idx for idx, value in enumerate(contrib37) if value == 2]
    B27 = sum(contrib27)
    B37 = sum(contrib37)
    exchange_feasible = B27 >= PAIR_TARGET and B37 >= PAIR_TARGET
    return {
        **metadata,
        "d2_split": d2_split_from_classes(degenerate),
        "capacity_preserving": capacity["capacity_upper_bound"] >= TARGET_AGREEMENT,
        "low_collapse": six_dom <= 20,
        "degenerate_classes": degenerate,
        **capacity,
        **pair7,
        **old_three,
        "six_class_dominance": six_dom,
        "B27": B27,
        "B37": B37,
        "deficit27": PAIR_TARGET - B27,
        "deficit37": PAIR_TARGET - B37,
        "pair27_credit_histogram": histogram(contrib27),
        "pair37_credit_histogram": histogram(contrib37),
        "pair27_credit_coordinates": credit27,
        "pair37_credit_coordinates": credit37,
        "pair27_credit_fiber_histogram": fiber_histogram(credit27),
        "pair37_credit_fiber_histogram": fiber_histogram(credit37),
        "critical_coordinates": len(set(credit27) | set(credit37)),
        "exchange_graph_feasible": exchange_feasible,
        "failure_mode": "PAIR27_37_EXCHANGE_FEASIBLE" if exchange_feasible else "PAIR27_37_EXCHANGE_INFEASIBLE",
    }


def vector_sort_key(row):
    return (
        row.get("exchange_graph_feasible") is True,
        min(row.get("B27", 0), row.get("B37", 0)),
        row.get("capacity_upper_bound", -1),
        -row.get("six_class_dominance", 10**9),
    )


def reconstruct_post_d2_vectors(exact_scan, capacity, post_repair, residual, F, powers):
    source = exact_scan.source_record()
    out = []
    for candidate in exact_scan.proxy_candidate_rows(source):
        reconstructed = exact_scan.reconstruct_candidate(candidate)
        selected = reconstructed["selected"]
        exact_rows, metas = residual.expanded_rows(F, powers, selected)
        protected_indices = capacity.protected_row_indices(metas)
        target_rows = [exact_rows[idx] for idx in protected_indices]
        partial_specs = capacity.partial_split_specs(selected, BASE_PARTIAL_FAMILY)
        partial_rows, partial_rhs = residual.pin_rows(F, powers, partial_specs)
        base_rows = target_rows + partial_rows
        base_rhs = [F(0)] * len(target_rows) + partial_rhs
        base_matrix = Matrix(F, base_rows, ncols=residual.VARIABLE_COUNT)
        base_pivots = [int(col) for col in base_matrix.pivots()]
        for pattern in BASE_FREE_PATTERNS:
            free_values = residual.free_assignments(F, pattern, base_pivots)
            vector_value, status, error, _pivots = residual.solve_with_free(F, base_rows, base_rhs, free_values)
            metadata = {
                "candidate_id": candidate["target_system_id"],
                "partial_split_family": BASE_PARTIAL_FAMILY,
                "free_pattern": pattern,
                "pin_specs": partial_specs,
                "solve_status": status,
            }
            if vector_value is None:
                out.append({**metadata, "failure_mode": status, "error": error})
                continue
            out.append(analyze_vector(residual, F, powers, vector_value, metadata))
            for pos in post_repair.repair_positions(capacity, selected, partial_specs):
                for repair in post_repair.repair_specs_at_position(pos):
                    repair_rows, repair_rhs = post_repair.repair_pin_rows(residual, F, powers, repair["pin_specs"])
                    vector_value, status, error, _pivots = residual.solve_with_free(
                        F,
                        base_rows + repair_rows,
                        base_rhs + repair_rhs,
                        free_values,
                    )
                    repair_metadata = {
                        "candidate_id": candidate["target_system_id"],
                        "partial_split_family": BASE_PARTIAL_FAMILY,
                        "free_pattern": pattern,
                        "repair_family": repair["repair_family"],
                        "repair_position": int(pos),
                        "repair_pin_specs": repair["pin_specs"],
                        "pin_specs": partial_specs + repair["pin_specs"],
                        "solve_status": status,
                    }
                    if vector_value is None:
                        out.append({**repair_metadata, "failure_mode": status, "error": error})
                        continue
                    out.append(analyze_vector(residual, F, powers, vector_value, repair_metadata))
    return out


def aggregate_diagnostic(rows):
    analyzed = [row for row in rows if row.get("B27") is not None]
    best = sorted(analyzed, key=vector_sort_key, reverse=True)[0] if analyzed else None
    feasible = any(row.get("exchange_graph_feasible") is True for row in analyzed)
    return {
        "vectors_analyzed": len(analyzed),
        "B27": None if best is None else best["B27"],
        "B37": None if best is None else best["B37"],
        "deficit27": None if best is None else best["deficit27"],
        "deficit37": None if best is None else best["deficit37"],
        "pair27_credit_histogram": {} if best is None else best["pair27_credit_histogram"],
        "pair37_credit_histogram": {} if best is None else best["pair37_credit_histogram"],
        "critical_coordinates": 0 if best is None else best["critical_coordinates"],
        "pair27_credit_coordinates": [] if best is None else best["pair27_credit_coordinates"],
        "pair37_credit_coordinates": [] if best is None else best["pair37_credit_coordinates"],
        "pair27_credit_fiber_histogram": {} if best is None else best["pair27_credit_fiber_histogram"],
        "pair37_credit_fiber_histogram": {} if best is None else best["pair37_credit_fiber_histogram"],
        "exchange_graph_feasible": feasible,
        "best_vector": best,
        "retained_vectors": sorted(analyzed, key=vector_sort_key, reverse=True)[:6],
    }


def audit_record():
    exact_scan = load_python_module(EXACT_SCAN_PATH, "protected_exchange_exact_scan")
    capacity = load_source_module(CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_for_exchange")
    post_repair = load_source_module(POST_REPAIR_AUDIT_PATH, "post_d2_pair7_repair_for_exchange")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_for_exchange")
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "pair27_37_exchange_ledger")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    rows = reconstruct_post_d2_vectors(exact_scan, capacity, post_repair, residual, F, powers)
    diagnostic = aggregate_diagnostic(rows)
    repair = {
        "repair_sets_tested": 0,
        "exact_vectors_constructed": 0,
        "B27_repaired_vectors": 0,
        "B37_repaired_vectors": 0,
        "full_pair_repaired_vectors": 0,
        "best_exact_max_min": None,
        "best_pair_B_values": None if diagnostic["best_vector"] is None else diagnostic["best_vector"]["pair_B_values"],
        "best_failure_mode": "PAIR27_37_EXCHANGE_FEASIBLE"
        if diagnostic["exchange_graph_feasible"]
        else "PAIR27_37_EXCHANGE_INFEASIBLE",
        "results": [],
    }
    record = ledger_scan.build_record(
        pair27_37_diagnostic={
            key: value for key, value in diagnostic.items() if key not in {"best_vector", "retained_vectors"}
        },
        targeted_repair=repair,
    )
    record["pair27_37_diagnostic"]["best_vector"] = diagnostic["best_vector"]
    record["pair27_37_diagnostic"]["retained_vectors"] = diagnostic["retained_vectors"]
    record["pair27_37_diagnostic"]["exact_field"] = "GF(17^32)"
    record["pair27_37_diagnostic"]["field_denominator"] = str(q)
    record["result_hash"] = residual.hash_payload(rows)
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
        diag = record["pair27_37_diagnostic"]
        print("SAGE_AUDIT_M1_A327_PAIR27_37_EXCHANGE_OBSTRUCTION_OK")
        print("vectors_analyzed: %d" % diag["vectors_analyzed"])
        print("B27: %s" % diag["B27"])
        print("B37: %s" % diag["B37"])
        print("exchange_graph_feasible: %s" % diag["exchange_graph_feasible"])
        print("best_failure_mode: %s" % record["targeted_repair"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
