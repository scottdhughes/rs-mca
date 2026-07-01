#!/usr/bin/env sage
"""Exact repaired-skeleton nondegenerate split audit."""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import sys
import time
from numbers import Integral
from pathlib import Path


TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
BASE_COLLAPSE = [[1, 4, 5, 7], [6], [3], [2]]
RESIDUAL_MASK = int((1 << 0) | (1 << 3) | (1 << 4) | (1 << 6))

STAGE2_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_postsplit_pair27_37_microrepair_stage2.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_repaired_skeleton_nondegenerate_split.py")
DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_nondegenerate_split.json")

TOTAL_STAGE2_BUDGET = 32
STAGE2_REPAIR_FAMILY = "triple_237"
FREE_PATTERNS = ["d2_first_free"]
SPLIT_FAMILIES = ["split_14_vs_57", "split_4_from_157", "split_1_from_457", "split_15_vs_47"]
PLANNED_PIN_BUDGETS = [1, 2, 4]
PLANNED_COORDINATE_LIMITS = [8, 16]
CASES = [
    {"split_family": "split_4_from_157", "pin_budget": 1, "coordinate_limit": 8},
]


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


def family_groups(family):
    if family == "split_14_vs_57":
        return [[1, 4], [5, 7]]
    if family == "split_4_from_157":
        return [[4], [1, 5, 7]]
    if family == "split_1_from_457":
        return [[1], [4, 5, 7]]
    if family == "split_15_vs_47":
        return [[1, 5], [4, 7]]
    raise ValueError("unknown split family: %s" % family)


def group_mask(group):
    out = int(0)
    for witness in group:
        out |= int(1 << (int(witness) - 1))
    return out


def split_masks_for_family(classes, family):
    groups = [group_mask(group) for group in family_groups(family)]
    target = int(0)
    for group in groups:
        target |= int(group)
    out = []
    for mask in classes:
        mask = int(mask)
        outside = mask & ~int(target)
        if outside:
            out.append(outside)
        for group in groups:
            part = mask & group
            if part:
                out.append(part)
    return sorted(set(out))


def split_specs_for_family(family, position, gamma):
    gamma = int(gamma)
    if family == "split_14_vs_57":
        return [
            {"left": 5, "right": 1, "position": int(position), "gamma": gamma, "kind": family},
            {"left": 7, "right": 5, "position": int(position), "gamma": 0, "kind": family},
        ]
    if family == "split_4_from_157":
        return [{"left": 4, "right": 1, "position": int(position), "gamma": gamma, "kind": family}]
    if family == "split_1_from_457":
        return [
            {"left": 4, "right": 1, "position": int(position), "gamma": gamma, "kind": family},
            {"left": 5, "right": 4, "position": int(position), "gamma": 0, "kind": family},
            {"left": 7, "right": 4, "position": int(position), "gamma": 0, "kind": family},
        ]
    if family == "split_15_vs_47":
        return [
            {"left": 4, "right": 1, "position": int(position), "gamma": gamma, "kind": family},
            {"left": 7, "right": 4, "position": int(position), "gamma": 0, "kind": family},
            {"left": 5, "right": 1, "position": int(position), "gamma": 0, "kind": family},
        ]
    raise ValueError("unknown split family: %s" % family)


def coordinate_row(pos, classes, occupied):
    capacity_before = max(int(mask).bit_count() for mask in classes)
    b27 = pair_contribution(classes, 2, 7)
    b37 = pair_contribution(classes, 3, 7)
    b57 = pair_contribution(classes, 5, 7)
    candidates = []
    for family in SPLIT_FAMILIES:
        after = split_masks_for_family(classes, family)
        capacity_after = max(int(mask).bit_count() for mask in after)
        b27_after = pair_contribution(after, 2, 7)
        b37_after = pair_contribution(after, 3, 7)
        b57_after = pair_contribution(after, 5, 7)
        capacity_damage = capacity_before - capacity_after
        b27_damage = b27 - b27_after
        b37_damage = b37 - b37_after
        b57_damage = b57 - b57_after
        collapse_benefit = 1 if any((int(mask) & RESIDUAL_MASK) == RESIDUAL_MASK for mask in classes) else 0
        score = (
            24 * collapse_benefit
            + 3 * max(0, b27_after - b27)
            + 3 * max(0, b37_after - b37)
            - 20 * max(0, capacity_damage)
            - 24 * max(0, b27_damage)
            - 24 * max(0, b37_damage)
            - 4 * max(0, b57_damage)
            - (8 if int(pos) in occupied else 0)
        )
        candidates.append(
            {
                "coordinate": int(pos),
                "quotient_fiber": int(pos) % 16,
                "split_family": family,
                "split_safe_score": int(score),
                "collapse_reduction_benefit": int(collapse_benefit),
                "predicted_capacity_damage": int(capacity_damage),
                "predicted_B27_damage": int(max(0, b27_damage)),
                "predicted_B37_damage": int(max(0, b37_damage)),
                "predicted_B57_damage": int(max(0, b57_damage)),
                "predicted_B27_gain": int(max(0, b27_after - b27)),
                "predicted_B37_gain": int(max(0, b37_after - b37)),
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
        "is_capacity_critical": bool(capacity_before >= 4),
        "is_B27_critical": bool(b27 == 2),
        "is_B37_critical": bool(b37 == 2),
        "is_B57_critical": bool(b57 == 2),
        "is_occupied": bool(int(pos) in occupied),
        "candidate_split_rows": candidates,
    }


def repaired_context():
    stage2 = load_source_module(STAGE2_AUDIT_PATH, "postsplit_stage2_helpers_repaired_split")
    context = stage2.prepare_stage1_context()
    extra = TOTAL_STAGE2_BUDGET - int(stage2.STAGE1_REPAIR_BUDGET)
    extra_specs, extra_deltas = context["stage1_module"].microrepair_specs(
        context["stage2_ledger"], STAGE2_REPAIR_FAMILY, extra
    )
    fixed_specs = context["stage1_fixed_specs"] + extra_specs
    vector_value, solve_meta = context["codesign"].solve_with_specs(
        context["scalable"], context["residual"], context["F"], context["base"], fixed_specs
    )
    if vector_value is None:
        raise RuntimeError("budget-32 repaired skeleton solve failed: %s" % solve_meta)
    base_row = stage2.evaluate_stage2(
        context,
        vector_value,
        {
            "phase": "repaired_skeleton_baseline",
            "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
            "total_triple_237_budget": TOTAL_STAGE2_BUDGET,
            "extra_repair_budget": extra,
            "stage2_repair_delta_summary": context["stage1_module"].delta_summary(extra_deltas),
            **solve_meta,
        },
    )
    occupied_base = context["stage1_module"].occupied_augmented_base(context["base"], fixed_specs)
    values = context["residual"].exact_values_from_vector(context["F"], context["base"]["powers"], vector_value)
    class_rows = context["residual"].class_masks_by_position(values)
    occupied = set(int(pos) for pos in occupied_base["occupied"])
    coordinate_rows = [coordinate_row(pos, classes, occupied) for pos, classes in enumerate(class_rows)]
    candidates = []
    for row in coordinate_rows:
        if row["is_occupied"]:
            continue
        candidates.extend(row["candidate_split_rows"])
    candidates = sorted(
        candidates,
        key=lambda row: (
            row["split_safe_score"],
            -row["predicted_capacity_damage"],
            -row["predicted_B27_damage"],
            -row["predicted_B37_damage"],
            -row["coordinate"],
        ),
        reverse=True,
    )
    ledger = {
        "coordinates": len(coordinate_rows),
        "capacity_critical_count": sum(1 for row in coordinate_rows if row["is_capacity_critical"]),
        "B27_critical_count": sum(1 for row in coordinate_rows if row["is_B27_critical"]),
        "B37_critical_count": sum(1 for row in coordinate_rows if row["is_B37_critical"]),
        "B57_critical_count": sum(1 for row in coordinate_rows if row["is_B57_critical"]),
        "split_safe_count": sum(1 for row in candidates if row["split_safe_score"] > 0),
        "coordinate_rows_preview": coordinate_rows[:16],
        "candidate_split_rows": candidates[:128],
    }
    context.update(
        {
            "stage2_module": stage2,
            "stage2_extra_specs": extra_specs,
            "stage2_extra_deltas": extra_deltas,
            "repaired_fixed_specs": fixed_specs,
            "repaired_base_row": base_row,
            "repaired_base_vector": vector_value,
            "repaired_ledger": ledger,
        }
    )
    return context


def selected_split_specs(ledger, family, pin_budget, coordinate_limit):
    pool = [row for row in ledger["candidate_split_rows"] if row["split_family"] == family]
    pool = pool[: int(coordinate_limit)]
    chosen = []
    used = set()
    for row in pool:
        coord = int(row["coordinate"])
        if coord in used:
            continue
        used.add(coord)
        chosen.append(row)
        if len(chosen) >= int(pin_budget):
            break
    specs = []
    for idx, row in enumerate(chosen):
        specs.extend(split_specs_for_family(family, row["coordinate"], idx + 1))
    return specs, chosen


def independent_solve_with_pattern(context, specs, free_pattern):
    codesign = context["codesign"]
    scalable = context["scalable"]
    residual = context["residual"]
    F = context["F"]
    base = context["base"]
    rows_pin, rhs_pin = scalable.pin_rows(residual, F, base["powers"], specs)
    rows = base["rows"] + rows_pin
    rhs = base["rhs"] + rhs_pin
    independent_rows, independent_rhs, system_meta = codesign.independent_system(F, residual, rows, rhs)
    A = Matrix(F, independent_rows, ncols=residual.VARIABLE_COUNT)
    pivots = [int(col) for col in A.pivots()]
    pivot_matrix = A.matrix_from_columns(pivots[: len(independent_rows)]) if len(pivots) >= len(independent_rows) else None
    if pivot_matrix is None:
        return None, {
            **system_meta,
            "solve_status": "REPAIRED_SPLIT_INCONSISTENT",
            "free_pattern": free_pattern,
            "error": "rank below row count",
        }
    free_values = residual.free_assignments(F, free_pattern, pivots)
    vector_value, status, error = scalable.solve_with_prepared_matrix(
        F, A, vector(F, independent_rhs), free_values, pivots, pivot_matrix
    )
    meta = {
        **system_meta,
        "solve_status": status,
        "free_pattern": free_pattern,
    }
    if vector_value is None:
        meta["error"] = error
    return vector_value, meta


def residual_class_reduced(degenerate_classes):
    return [1, 4, 5, 7] not in degenerate_classes


def classify(row):
    if row.get("pair_B_values") is None:
        return "REPAIRED_SPLIT_INCONSISTENT"
    if row["six_class_dominance"] > 0:
        return "REPAIRED_SPLIT_COLLAPSE_RETURNS"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "REPAIRED_SPLIT_CAPACITY_LOSS"
    if row["pair_B_values"][1] < PAIR_TARGET or row["pair_B_values"][2] < PAIR_TARGET:
        return "REPAIRED_SPLIT_PAIR27_37_LOSS"
    if row["pair_B_values"][4] < PAIR_TARGET:
        return "REPAIRED_SPLIT_PAIR57_LOSS"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "REPAIRED_SPLIT_EXACT_CANDIDATE"
    if row.get("distinct_codewords") is True:
        return "REPAIRED_SPLIT_LOW_RESCHEDULE"
    if residual_class_reduced(row["degenerate_classes"]):
        return "REPAIRED_SPLIT_PARTIAL_DISTINCT"
    return "REPAIRED_SPLIT_NOT_DISTINCT"


def evaluate_split(context, vector_value, metadata):
    row = context["codesign"].evaluate(
        context["scalable"], context["residual"], context["F"], context["base"], vector_value, metadata
    )
    row["pair_guard_preserving"] = (
        row["pair_B_values"][1] >= PAIR_TARGET
        and row["pair_B_values"][2] >= PAIR_TARGET
        and row["pair_B_values"][4] >= PAIR_TARGET
    )
    row["partial_split"] = residual_class_reduced(row["degenerate_classes"])
    row["nondegenerate"] = row["distinct_codewords"]
    row["failure_mode"] = classify(row)
    return row


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "REPAIRED_SPLIT_EXACT_CANDIDATE",
        row.get("distinct_codewords") is True,
        row.get("pair_guard_preserving") is True,
        row.get("capacity_upper_bound", -1) >= TARGET_AGREEMENT,
        row.get("partial_split") is True,
        exact_max,
        min(pair_values[1], pair_values[2], pair_values[4]),
        row.get("capacity_upper_bound", -1),
        -row.get("six_class_dominance", 10**9),
    )


def case_record_from_context(context, case):
    start = time.time()
    specs, selected = selected_split_specs(
        context["repaired_ledger"], case["split_family"], case["pin_budget"], case["coordinate_limit"]
    )
    if not specs:
        return {
            **case,
            "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
            "split_specs": [],
            "selected_split_rows": [],
            "failure_mode": "REPAIRED_SPLIT_INCONSISTENT",
            "vector_results": [],
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    vectors = []
    for pattern in FREE_PATTERNS:
        vector_value, solve_meta = independent_solve_with_pattern(context, specs, pattern)
        metadata = {
            **case,
            "phase": "repaired_skeleton_nondegenerate_split",
            "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
            "total_triple_237_budget": TOTAL_STAGE2_BUDGET,
            "split_specs": specs,
            "selected_split_rows": selected,
            **solve_meta,
        }
        if vector_value is None:
            vectors.append({**metadata, "pair_B_values": None, "failure_mode": "REPAIRED_SPLIT_INCONSISTENT"})
            continue
        vectors.append(evaluate_split(context, vector_value, metadata))
    best = sorted(vectors, key=vector_sort_key, reverse=True)[0]
    return {
        **case,
        "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
        "split_specs": specs,
        "selected_split_rows": selected,
        "vector_results": vectors,
        "best_failure_mode": best["failure_mode"],
        "best_capacity": best.get("capacity_upper_bound"),
        "best_pair_B_values": best.get("pair_B_values"),
        "best_collapse_pattern": best.get("degenerate_classes"),
        "elapsed_seconds": float(round(float(time.time() - start), 3)),
    }


def failure_counts(rows):
    out = {}
    for row in rows:
        for vector_row in row["vector_results"]:
            failure = vector_row["failure_mode"]
            out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "repaired_skeleton_split_ledger")
    context = repaired_context()
    results = [case_record_from_context(context, case) for case in CASES]
    vector_rows = [row for case in results for row in case["vector_results"] if row.get("pair_B_values") is not None]
    best = sorted(vector_rows, key=vector_sort_key, reverse=True)[0] if vector_rows else None
    search = {
        "exact_field": "GF(17^32)",
        "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
        "split_families": SPLIT_FAMILIES,
        "planned_pin_budgets": PLANNED_PIN_BUDGETS,
        "planned_coordinate_limits": PLANNED_COORDINATE_LIMITS,
        "free_patterns": FREE_PATTERNS,
        "baseline_repaired_skeleton": context["repaired_base_row"],
        "capacity_slack_ledger": context["repaired_ledger"],
        "systems_tested": len(results),
        "timeouts": sum(1 for row in vector_rows if row.get("failure_mode") == "REPAIRED_SPLIT_TIMEOUT"),
        "exact_vectors_constructed": len(vector_rows),
        "nondegenerate_vectors": sum(1 for row in vector_rows if row.get("distinct_codewords") is True),
        "partial_split_vectors": sum(1 for row in vector_rows if row.get("partial_split") is True),
        "capacity_preserving_vectors": sum(1 for row in vector_rows if row.get("capacity_upper_bound", 0) >= TARGET_AGREEMENT),
        "pair_guard_preserving_vectors": sum(1 for row in vector_rows if row.get("pair_guard_preserving") is True),
        "failure_mode_counts": failure_counts(results),
        "best_capacity": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_collapse_pattern": None if best is None else best.get("degenerate_classes"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_agreement_vector": None if best is None else best.get("exact_agreement_vector"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    return jsonable(ledger_scan.build_record(repaired_skeleton_split=search))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--single-case")
    args = parser.parse_args()
    if args.single_case:
        context = repaired_context()
        print(json.dumps(jsonable(case_record_from_context(context, json.loads(args.single_case))), sort_keys=True))
        return
    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_REPAIRED_SKELETON_NONDEGENERATE_SPLIT_OK")
        print("systems_tested: %d" % record["repaired_skeleton_split"]["systems_tested"])
        print("exact_vectors_constructed: %d" % record["repaired_skeleton_split"]["exact_vectors_constructed"])
        print("nondegenerate_vectors: %d" % record["repaired_skeleton_split"]["nondegenerate_vectors"])
        print("partial_split_vectors: %d" % record["repaired_skeleton_split"]["partial_split_vectors"])
        print("best_failure_mode: %s" % record["repaired_skeleton_split"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
