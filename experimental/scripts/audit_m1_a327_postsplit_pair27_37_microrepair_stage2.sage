#!/usr/bin/env sage
"""Exact post-split pair {2,7}/{3,7} microrepair stage-2 audit."""

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
BASE_STAGE1_CAPACITY = 330
BASE_STAGE1_PAIR_B = [1024, 645, 644, 1024, 1024]
BASE_COLLAPSE = [[1, 4, 5, 6, 7], [3], [2]]

STAGE1_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_postsplit_pair27_37_microrepair.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_postsplit_pair27_37_microrepair_stage2.py")
DATA_PATH = Path("experimental/data/m1_a327_postsplit_pair27_37_microrepair_stage2.json")

STAGE1_REPAIR_FAMILY = "triple_237"
STAGE1_REPAIR_BUDGET = 8
TOTAL_BUDGETS = [12, 16, 24, 32]
STAGE2_FAMILIES = ["triple_237"]


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


def classify(row):
    if row.get("pair_B_values") is None:
        return "MICROREPAIR_STAGE2_INCONSISTENT"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "MICROREPAIR_STAGE2_CAPACITY_LOSS"
    if row["pair_B_values"][4] < PAIR_TARGET:
        return "MICROREPAIR_STAGE2_PAIR57_LOSS"
    if row["six_class_dominance"] > 0 or not collapse_reduced(row["degenerate_classes"]):
        return "MICROREPAIR_STAGE2_COLLAPSE_RETURNS"
    if row["pair_B_values"][1] < PAIR_TARGET or row["pair_B_values"][2] < PAIR_TARGET:
        return "MICROREPAIR_STAGE2_PAIRCLASS_NOT_REPAIRED"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "MICROREPAIR_STAGE2_EXACT_CANDIDATE"
    return "MICROREPAIR_STAGE2_LOW_RESCHEDULE"


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "MICROREPAIR_STAGE2_EXACT_CANDIDATE",
        pair_values[1] >= PAIR_TARGET and pair_values[2] >= PAIR_TARGET,
        row.get("capacity_upper_bound", -1) >= TARGET_AGREEMENT,
        pair_values[4] >= PAIR_TARGET,
        collapse_reduced(row.get("degenerate_classes", [])),
        exact_max,
        min(pair_values[1], pair_values[2]),
        row.get("capacity_upper_bound", -1),
        row.get("distinct_codewords") is True,
        -row.get("six_class_dominance", 10**9),
    )


def prepare_stage1_context():
    stage1 = load_source_module(STAGE1_AUDIT_PATH, "postsplit_microrepair_stage1_helpers")
    context = stage1.prepare_context()
    stage1_specs, stage1_deltas = stage1.microrepair_specs(
        context["micro_ledger"], STAGE1_REPAIR_FAMILY, STAGE1_REPAIR_BUDGET
    )
    fixed_specs = context["fixed_specs"] + stage1_specs
    vector_value, solve_meta = context["codesign"].solve_with_specs(
        context["scalable"], context["residual"], context["F"], context["base"], fixed_specs
    )
    if vector_value is None:
        raise RuntimeError("stage1 microrepair solve failed: %s" % solve_meta)
    stage1_row = stage1.evaluate_micro(
        context["codesign"],
        context["scalable"],
        context["residual"],
        context["F"],
        context["base"],
        vector_value,
        {
            "phase": "stage1_fixed_microrepair",
            "repair_family": STAGE1_REPAIR_FAMILY,
            "repair_budget": STAGE1_REPAIR_BUDGET,
            "repair_delta_summary": stage1.delta_summary(stage1_deltas),
            **solve_meta,
        },
    )
    stage2_ledger_base = stage1.occupied_augmented_base(context["base"], fixed_specs)
    stage2_ledger = context["slack"].ledger_from_base(
        context["residual"], context["F"], context["base"]["powers"], stage2_ledger_base, vector_value
    )
    context.update(
        {
            "stage1_module": stage1,
            "stage1_specs": stage1_specs,
            "stage1_deltas": stage1_deltas,
            "stage1_fixed_specs": fixed_specs,
            "stage1_row": stage1_row,
            "stage2_ledger": stage2_ledger,
        }
    )
    return context


def evaluate_stage2(context, vector_value, metadata):
    row = context["codesign"].evaluate(
        context["scalable"], context["residual"], context["F"], context["base"], vector_value, metadata
    )
    row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
    row["pair27_repaired"] = row["pair_B_values"][1] >= PAIR_TARGET
    row["pair37_repaired"] = row["pair_B_values"][2] >= PAIR_TARGET
    row["pair27_37_repaired"] = row["pair27_repaired"] and row["pair37_repaired"]
    row["pair57_preserving"] = row["pair_B_values"][4] >= PAIR_TARGET
    row["collapse_preserving"] = row["six_class_dominance"] == 0 and collapse_reduced(row["degenerate_classes"])
    row["pair_deficit_to_654"] = [PAIR_TARGET - value for value in row["pair_B_values"]]
    row["failure_mode"] = classify(row)
    return row


def extra_budget(case):
    total = int(case["total_triple_237_budget"])
    return max(0, total - STAGE1_REPAIR_BUDGET)


def case_record_from_context(context, case):
    start = time.time()
    extra = extra_budget(case)
    repair_specs, repair_deltas = context["stage1_module"].microrepair_specs(
        context["stage2_ledger"], case["repair_family"], extra
    )
    vector_value, solve_meta = context["codesign"].solve_with_specs(
        context["scalable"],
        context["residual"],
        context["F"],
        context["base"],
        context["stage1_fixed_specs"] + repair_specs,
    )
    if vector_value is None:
        return {
            **case,
            "base_system": "postsplit_microrepair_triple_237_budget8",
            "baseline_stage1": {
                "capacity_upper_bound": context["stage1_row"]["capacity_upper_bound"],
                "pair_B_values": context["stage1_row"]["pair_B_values"],
                "degenerate_classes": context["stage1_row"]["degenerate_classes"],
            },
            "extra_repair_budget": extra,
            "repair_specs_preview": repair_specs[:12],
            "repair_delta_summary": context["stage1_module"].delta_summary(repair_deltas),
            "failure_mode": "MICROREPAIR_STAGE2_INCONSISTENT",
            "solve_meta": solve_meta,
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    row = evaluate_stage2(
        context,
        vector_value,
        {
            **case,
            "phase": "postsplit_microrepair_stage2",
            "base_system": "postsplit_microrepair_triple_237_budget8",
            "stage1_repair_family": STAGE1_REPAIR_FAMILY,
            "stage1_repair_budget": STAGE1_REPAIR_BUDGET,
            "extra_repair_budget": extra,
            "stage2_repair_specs_preview": repair_specs[:12],
            "stage2_repair_delta_summary": context["stage1_module"].delta_summary(repair_deltas),
            **solve_meta,
        },
    )
    row["baseline_stage1"] = {
        "capacity_upper_bound": context["stage1_row"]["capacity_upper_bound"],
        "pair_B_values": context["stage1_row"]["pair_B_values"],
        "pair_deficit_to_654": context["stage1_row"]["pair_deficit_to_654"],
        "degenerate_classes": context["stage1_row"]["degenerate_classes"],
    }
    row["extra_repair_budget"] = extra
    row["elapsed_seconds"] = float(round(float(time.time() - start), 3))
    return row


def case_record(case):
    return case_record_from_context(prepare_stage1_context(), case)


def cases():
    return [
        {"total_triple_237_budget": int(budget), "repair_family": family}
        for budget in TOTAL_BUDGETS
        for family in STAGE2_FAMILIES
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "postsplit_pair27_37_microrepair_stage2_ledger")
    context = prepare_stage1_context()
    results = [case_record_from_context(context, case) for case in cases()]
    best_pool = [row for row in results if row.get("pair_B_values") is not None]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    search = {
        "exact_field": "GF(17^32)",
        "base_system": "postsplit_microrepair_triple_237_budget8",
        "stage1_repair_family": STAGE1_REPAIR_FAMILY,
        "stage1_repair_budget": STAGE1_REPAIR_BUDGET,
        "total_triple_237_budgets": TOTAL_BUDGETS,
        "repair_families": STAGE2_FAMILIES,
        "execution_mode": "single_context_in_process",
        "systems_tested": len(results),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "MICROREPAIR_STAGE2_TIMEOUT"),
        "exact_vectors_constructed": sum(1 for row in results if row.get("pair_B_values") is not None),
        "capacity_preserving_vectors": sum(1 for row in results if row.get("capacity_preserving") is True),
        "pair27_repaired_vectors": sum(1 for row in results if row.get("pair27_repaired") is True),
        "pair37_repaired_vectors": sum(1 for row in results if row.get("pair37_repaired") is True),
        "pair27_37_repaired_vectors": sum(1 for row in results if row.get("pair27_37_repaired") is True),
        "pair57_preserving_vectors": sum(1 for row in results if row.get("pair57_preserving") is True),
        "collapse_preserving_vectors": sum(1 for row in results if row.get("collapse_preserving") is True),
        "failure_mode_counts": failure_counts(results),
        "best_capacity": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_agreement_vector": None if best is None else best.get("exact_agreement_vector"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    return jsonable(ledger_scan.build_record(stage2_microrepair=search))


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
        print("SAGE_AUDIT_M1_A327_POSTSPLIT_PAIR27_37_MICROREPAIR_STAGE2_OK")
        print("systems_tested: %d" % record["stage2_microrepair"]["systems_tested"])
        print("timeouts: %d" % record["stage2_microrepair"]["timeouts"])
        print("exact_vectors_constructed: %d" % record["stage2_microrepair"]["exact_vectors_constructed"])
        print("capacity_preserving_vectors: %d" % record["stage2_microrepair"]["capacity_preserving_vectors"])
        print("pair27_37_repaired_vectors: %d" % record["stage2_microrepair"]["pair27_37_repaired_vectors"])
        print("best_failure_mode: %s" % record["stage2_microrepair"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
