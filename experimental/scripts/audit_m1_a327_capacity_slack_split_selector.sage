#!/usr/bin/env sage
"""Exact coordinate-ledger capacity-slack split selector audit."""

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

SCRIPT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_slack_split_selector.sage")
SCALABLE_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_pair27_37_class_creation_scalable.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_capacity_slack_split_selector.py")
DATA_PATH = Path("experimental/data/m1_a327_capacity_slack_split_selector.json")

TARGET_SIZE = 128
PAIR_ROW_EXTENSION = 96
SPLIT_BUDGETS = [8, 16, 32]
SPLIT_SELECTORS = ["greedy", "pair27_weighted", "pair37_weighted", "capacity_safe"]
FREE_PATTERNS = ["d2_first_free", "d2_first4_free", "d2_even_sparse"]
CASE_TIMEOUT_SECONDS = 95


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


def mask_to_witnesses(mask):
    return [idx + 1 for idx in range(7) if int(mask) & (1 << idx)]


def class_pattern(classes):
    return sorted([mask_to_witnesses(mask) for mask in classes], key=lambda row: (len(row), row), reverse=True)


def pair_contribution(classes, left, right):
    subset = int((1 << (left - 1)) | (1 << (right - 1)))
    return max((int(mask) & subset).bit_count() for mask in classes)


def collapse_reduced(degenerate_classes):
    return BASE_COLLAPSE[0] not in degenerate_classes


def split_masks_for_kind(classes, kind):
    split_targets = {
        "split_6_keep1457": [6],
        "split_4_keep1567": [4],
        "split_46_keep157": [4, 6],
    }[kind]
    target_bits = int(0)
    for witness in split_targets:
        target_bits |= int(1 << (witness - 1))
    out = []
    for mask in classes:
        mask = int(mask)
        removed = mask & target_bits
        kept = mask & ~target_bits
        if kept:
            out.append(kept)
        for witness in split_targets:
            bit = int(1 << (witness - 1))
            if removed & bit:
                out.append(bit)
    return sorted(set(out))


def split_kind_specs(kind, position):
    if kind == "split_6_keep1457":
        return [offset_spec(6, 1, position, 1, kind)]
    if kind == "split_4_keep1567":
        return [offset_spec(4, 1, position, 1, kind)]
    if kind == "split_46_keep157":
        return [offset_spec(4, 1, position, 1, kind), offset_spec(6, 1, position, 1, kind)]
    raise ValueError("unknown split kind: %s" % kind)


def offset_spec(left, right, position, gamma, family):
    return {
        "left": int(left),
        "right": int(right),
        "position": int(position),
        "gamma": int(gamma),
        "kind": family,
    }


def coordinate_row(pos, classes, occupied):
    capacity_before = max(int(mask).bit_count() for mask in classes)
    b27 = pair_contribution(classes, 2, 7)
    b37 = pair_contribution(classes, 3, 7)
    b57 = pair_contribution(classes, 5, 7)
    collapse_mask = 0
    for witness in [1, 4, 5, 6, 7]:
        collapse_mask |= 1 << (witness - 1)
    candidate_rows = []
    for kind in ["split_6_keep1457", "split_4_keep1567", "split_46_keep157"]:
        after = split_masks_for_kind(classes, kind)
        capacity_after = max(int(mask).bit_count() for mask in after)
        b27_after = pair_contribution(after, 2, 7)
        b37_after = pair_contribution(after, 3, 7)
        b57_after = pair_contribution(after, 5, 7)
        capacity_damage = capacity_before - capacity_after
        b57_damage = b57 - b57_after
        collapse_benefit = 1 if collapse_mask in classes and collapse_mask not in after else 0
        score = (
            12 * collapse_benefit
            + 3 * max(0, b27_after - b27)
            + 3 * max(0, b37_after - b37)
            - 8 * max(0, capacity_damage)
            - 16 * max(0, b57_damage)
            - (2 if capacity_before >= 5 else 0)
            - (2 if b57 == 2 else 0)
        )
        candidate_rows.append(
            {
                "coordinate": int(pos),
                "quotient_fiber": int(pos) % 16,
                "split_kind": kind,
                "split_safe_score": int(score),
                "collapse_reduction_benefit": int(collapse_benefit),
                "predicted_capacity_damage": int(capacity_damage),
                "predicted_B27_gain": int(b27_after - b27),
                "predicted_B37_gain": int(b37_after - b37),
                "predicted_B57_damage": int(b57_damage),
                "is_split_safe": bool(collapse_benefit and capacity_damage <= 1 and b57_damage <= 0),
            }
        )
    return {
        "coordinate": int(pos),
        "quotient_fiber": int(pos) % 16,
        "value_class_pattern": class_pattern(classes),
        "capacity_contribution": int(capacity_before),
        "B27_contribution": int(b27),
        "B37_contribution": int(b37),
        "B57_contribution": int(b57),
        "is_capacity_critical": bool(capacity_before >= 5),
        "is_pair57_critical": bool(b57 == 2),
        "is_occupied_by_pairclass_or_partial": bool(int(pos) in occupied),
        "candidate_split_rows": candidate_rows,
    }


def selector_key(candidate, selector):
    if selector == "greedy":
        return (candidate["split_safe_score"], -candidate["predicted_capacity_damage"], -candidate["coordinate"])
    if selector == "pair27_weighted":
        return (
            candidate["split_safe_score"] + 4 * candidate["predicted_B27_gain"],
            -candidate["predicted_capacity_damage"],
            -candidate["coordinate"],
        )
    if selector == "pair37_weighted":
        return (
            candidate["split_safe_score"] + 4 * candidate["predicted_B37_gain"],
            -candidate["predicted_capacity_damage"],
            -candidate["coordinate"],
        )
    if selector == "capacity_safe":
        return (-candidate["predicted_capacity_damage"], candidate["split_safe_score"], -candidate["coordinate"])
    raise ValueError("unknown selector: %s" % selector)


def select_split_specs(ledger_candidates, selector, budget):
    safe_sorted = sorted(
        ledger_candidates,
        key=lambda row: (row["split_safe_score"], -row["predicted_capacity_damage"], -row["coordinate"]),
        reverse=True,
    )
    pool = safe_sorted[: int(budget)]
    if not pool:
        return []
    chosen = sorted(pool, key=lambda row: selector_key(row, selector), reverse=True)[0]
    return split_kind_specs(chosen["split_kind"], chosen["coordinate"])


def setup_base(scalable, residual, F, powers):
    exact_scan = scalable.load_python_module(scalable.EXACT_SCAN_PATH, "protected_exchange_exact_scan_slack")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_slack")
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
    extension_tuples = scalable.alternating_extension(base_t27, base_t37, full_t27, full_t37, PAIR_ROW_EXTENSION)
    extension_specs = scalable.specs_from_extension(extension_tuples, "overlap_all", TARGET_SIZE)
    class_rows, class_rhs = scalable.pin_rows(residual, F, powers, base_specs + extension_specs)
    rows = target_rows + partial_rows + class_rows
    rhs = [F(0)] * len(target_rows) + partial_rhs + class_rhs
    occupied = (
        [int(spec["position"]) for spec in partial_specs]
        + list(int(pos) for pos in base_t27)
        + list(int(pos) for pos in base_t37)
        + [int(row[2]) for row in extension_tuples]
    )
    return {
        "candidate": candidate,
        "selected": selected,
        "target_rows": target_rows,
        "partial_rows": partial_rows,
        "partial_rhs": partial_rhs,
        "class_rows": class_rows,
        "class_rhs": class_rhs,
        "rows": rows,
        "rhs": rhs,
        "protected_rows": len(target_rows),
        "base_creation_rows": len(base_specs),
        "extension_rows": len(extension_specs),
        "occupied": occupied,
        "partial_specs": partial_specs,
    }


def solve_base_vector(scalable, residual, F, base):
    A = Matrix(F, base["rows"], ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    pivot_matrix = A.matrix_from_columns(pivots[: len(base["rows"])])
    free_values = residual.free_assignments(F, "d2_first_free", pivots)
    vector_value, status, error = scalable.solve_with_prepared_matrix(
        F, A, vector(F, base["rhs"]), free_values, pivots, pivot_matrix
    )
    if vector_value is None:
        raise RuntimeError("base vector solve failed: %s %s" % (status, error))
    return vector_value


def ledger_from_base(residual, F, powers, base, vector_value):
    values = residual.exact_values_from_vector(F, powers, vector_value)
    class_rows = residual.class_masks_by_position(values)
    occupied = set(int(pos) for pos in base["occupied"])
    rows = [coordinate_row(pos, classes, occupied) for pos, classes in enumerate(class_rows)]
    candidates = []
    for row in rows:
        if row["is_occupied_by_pairclass_or_partial"]:
            continue
        for candidate in row["candidate_split_rows"]:
            if candidate["is_split_safe"]:
                candidates.append(candidate)
    fiber_scores = {}
    for candidate in candidates:
        fiber = str(candidate["quotient_fiber"])
        fiber_scores.setdefault(fiber, {"candidate_count": 0, "score_total": 0})
        fiber_scores[fiber]["candidate_count"] += 1
        fiber_scores[fiber]["score_total"] += candidate["split_safe_score"]
    top_fibers = [
        {"quotient_fiber": int(fiber), **payload}
        for fiber, payload in sorted(
            fiber_scores.items(), key=lambda item: (item[1]["score_total"], item[1]["candidate_count"]), reverse=True
        )[:8]
    ]
    return {
        "coordinates": len(rows),
        "capacity_critical_count": sum(1 for row in rows if row["is_capacity_critical"]),
        "pair57_critical_count": sum(1 for row in rows if row["is_pair57_critical"]),
        "split_safe_count": len(candidates),
        "top_slack_fibers": top_fibers,
        "coordinate_rows": rows,
        "candidate_split_rows": sorted(
            candidates,
            key=lambda row: (row["split_safe_score"], -row["predicted_capacity_damage"], -row["coordinate"]),
            reverse=True,
        )[:96],
    }


def classify(row):
    if row.get("pair_B_values") is None:
        return "SPLIT_SELECTOR_INCONSISTENT"
    if row["pair_B_values"][4] < PAIR_TARGET:
        return "SPLIT_SELECTOR_PAIR57_LOSS"
    if row.get("capacity_upper_bound", 0) < TARGET_AGREEMENT:
        return "SPLIT_SELECTOR_CAPACITY_LOSS"
    if not row.get("collapse_reduced"):
        return "SPLIT_SELECTOR_COLLAPSE_NOT_REDUCED"
    if row["pair_B_values"][1] < SOURCE_B27 or row["pair_B_values"][2] < SOURCE_B37:
        return "SPLIT_SELECTOR_PAIR27_37_STALLS"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "SPLIT_SELECTOR_EXACT_CANDIDATE"
    return "SPLIT_SELECTOR_LOW_RESCHEDULE"


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "SPLIT_SELECTOR_EXACT_CANDIDATE",
        row.get("capacity_preserving") is True,
        row.get("pair57_preserving") is True,
        row.get("collapse_reduced") is True,
        exact_max,
        min(pair_values[1], pair_values[2], pair_values[4]),
        row.get("capacity_upper_bound", -1),
        row.get("distinct_codewords") is True,
    )


def case_record(case):
    scalable = load_source_module(SCALABLE_AUDIT_PATH, "pairclass_scalable_helpers_slack_case")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_slack_case")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_slack_case")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    base = setup_base(scalable, residual, F, powers)
    base_vector = solve_base_vector(scalable, residual, F, base)
    ledger = ledger_from_base(residual, F, powers, base, base_vector)
    split = select_split_specs(ledger["candidate_split_rows"], case["selector"], case["split_location_budget"])
    if not split:
        return {**case, "failure_mode": "NO_SPLIT_SAFE_COORDINATES", "vector_results": []}

    split_rows, split_rhs = scalable.pin_rows(residual, F, powers, split)
    rows = base["rows"] + split_rows
    rhs = base["rhs"] + split_rhs
    start = time.time()
    A = Matrix(F, rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    rank_after = len(pivots)
    nullity_after = residual.VARIABLE_COUNT - rank_after
    pivot_matrix = A.matrix_from_columns(pivots[: len(rows)]) if rank_after >= len(rows) else None
    if pivot_matrix is None:
        return {
            **case,
            "split_specs": split,
            "row_count": len(rows),
            "rank_after": rank_after,
            "nullity_after": nullity_after,
            "failure_mode": "SPLIT_SELECTOR_INCONSISTENT",
            "vector_results": [],
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
            "pair_row_extension": PAIR_ROW_EXTENSION,
            "free_pattern": pattern,
            "row_count": len(rows),
            "protected_rows": base["protected_rows"],
            "base_creation_rows": base["base_creation_rows"],
            "extension_rows": base["extension_rows"],
            "split_rows": len(split),
            "split_specs": split,
            "rank_after": rank_after,
            "nullity_after": nullity_after,
            "solve_status": status,
        }
        if vector_value is None:
            vectors.append({**metadata, "failure_mode": "SPLIT_SELECTOR_INCONSISTENT", "error": error})
            continue
        row = scalable.evaluate_with_failure(residual, F, powers, vector_value, metadata)
        row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
        row["pair57_preserving"] = row["pair_B_values"][4] >= PAIR_TARGET
        row["collapse_reduced"] = collapse_reduced(row["degenerate_classes"])
        row["pair27_37_improved"] = row["pair_B_values"][1] >= SOURCE_B27 and row["pair_B_values"][2] >= SOURCE_B37
        row["failure_mode"] = classify(row)
        vectors.append(row)

    best = sorted(vectors, key=vector_sort_key, reverse=True)[0]
    return {
        **case,
        "target_size": TARGET_SIZE,
        "pair_row_extension": PAIR_ROW_EXTENSION,
        "split_specs": split,
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
            "failure_mode": "SPLIT_SELECTOR_TIMEOUT",
            "timeout_seconds": CASE_TIMEOUT_SECONDS,
            "vector_results": [],
        }
    if completed.returncode != 0:
        return {
            **case,
            "failure_mode": "SPLIT_SELECTOR_INCONSISTENT",
            "returncode": completed.returncode,
            "stderr_tail": completed.stderr[-2000:],
            "vector_results": [],
        }
    try:
        return json.loads(completed.stdout)
    except Exception as exc:
        return {
            **case,
            "failure_mode": "SPLIT_SELECTOR_INCONSISTENT",
            "error": str(exc),
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
            "vector_results": [],
        }


def cases():
    return [
        {"split_location_budget": int(budget), "selector": selector}
        for budget in SPLIT_BUDGETS
        for selector in SPLIT_SELECTORS
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    scalable = load_source_module(SCALABLE_AUDIT_PATH, "pairclass_scalable_helpers_slack")
    capacity = scalable.load_source_module(scalable.CAPACITY_AUDIT_PATH, "capacity_preserving_residual12_slack")
    residual = capacity.load_source_module(capacity.RESIDUAL_AUDIT_PATH, "residual12_exact_audit_slack")
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "capacity_slack_split_ledger")
    q, F, H = residual.field_context()
    powers = residual.precompute_powers(F, H)
    base = setup_base(scalable, residual, F, powers)
    base_vector = solve_base_vector(scalable, residual, F, base)
    ledger = ledger_from_base(residual, F, powers, base, base_vector)
    results = [run_child(case) for case in cases()]
    vectors = [row for result in results for row in result.get("vector_results", [])]
    best_pool = vectors or [row.get("best", row) for row in results]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    selector = {
        "exact_field": "GF(17^32)",
        "base_system": "scalable_pairclass_overlap_all_extension96",
        "split_location_budgets": SPLIT_BUDGETS,
        "selectors": SPLIT_SELECTORS,
        "free_patterns": FREE_PATTERNS,
        "systems_tested": len(results),
        "split_rows_tested": sum(len(row.get("split_specs", [])) for row in results),
        "exact_vectors_constructed": sum(1 for row in vectors if row.get("distinct_codewords") is not None),
        "capacity_preserving_vectors": sum(1 for row in vectors if row.get("capacity_preserving") is True),
        "pair57_preserving_vectors": sum(1 for row in vectors if row.get("pair57_preserving") is True),
        "pair27_37_improved_vectors": sum(1 for row in vectors if row.get("pair27_37_improved") is True),
        "collapse_reduced_vectors": sum(1 for row in vectors if row.get("collapse_reduced") is True),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "SPLIT_SELECTOR_TIMEOUT"),
        "failure_mode_counts": failure_counts(vectors or results),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_capacity_upper_bound": None if best is None else best.get("capacity_upper_bound"),
        "best_collapse_pattern": None if best is None else best.get("degenerate_classes"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    record = ledger_scan.build_record(capacity_slack_ledger=ledger, split_selector=selector)
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
        print("SAGE_AUDIT_M1_A327_CAPACITY_SLACK_SPLIT_SELECTOR_OK")
        print("split_safe_count: %d" % record["capacity_slack_ledger"]["split_safe_count"])
        print("systems_tested: %d" % record["split_selector"]["systems_tested"])
        print("exact_vectors_constructed: %d" % record["split_selector"]["exact_vectors_constructed"])
        print("capacity_preserving_vectors: %d" % record["split_selector"]["capacity_preserving_vectors"])
        print("best_failure_mode: %s" % record["split_selector"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
