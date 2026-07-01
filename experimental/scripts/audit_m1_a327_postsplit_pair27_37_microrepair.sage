#!/usr/bin/env sage
"""Exact post-split pair {2,7}/{3,7} microrepair audit."""

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
BASE_POST_CAPACITY = 329
BASE_POST_B27 = 641
BASE_POST_B37 = 640
BASE_POST_B57 = 1024
BASE_COLLAPSE = [[1, 4, 5, 6, 7], [3], [2]]

SCRIPT_PATH = Path("experimental/scripts/audit_m1_a327_postsplit_pair27_37_microrepair.sage")
CODESIGN_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_reserve_pairclass_codesign_before_split.sage")
SLACK_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_capacity_slack_split_selector.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_postsplit_pair27_37_microrepair.py")
DATA_PATH = Path("experimental/data/m1_a327_postsplit_pair27_37_microrepair.json")

BEST_ROW_FAMILY = "quotient_fiber_buffer"
BEST_ROW_EXTENSION_SIZE = 96
PLANNED_REPAIR_BUDGETS = [8, 16, 24, 32]
PLANNED_REPAIR_FAMILIES = [
    "pair27_micro",
    "pair37_micro",
    "balanced_pair27_37_micro",
    "triple_237",
    "postsplit_survivor_pair_micro",
    "quotient_fiber_pair27_37_micro",
]
REPAIR_BUDGETS = [8]
REPAIR_FAMILIES = ["triple_237"]
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


def pair_field(left, right):
    key = set([int(left), int(right)])
    if key == set([2, 7]):
        return "B27_contribution"
    if key == set([3, 7]):
        return "B37_contribution"
    if key == set([5, 7]):
        return "B57_contribution"
    return None


def equality_spec(left, right, position, family, delta=None):
    out = {
        "left": int(left),
        "right": int(right),
        "position": int(position),
        "gamma": 0,
        "kind": family,
    }
    if delta is not None:
        out["delta"] = delta
    return out


def candidate_delta(row, left, right, family):
    field = pair_field(left, right)
    pair_gain = 0 if field is None else max(0, 2 - int(row[field]))
    b27_gain = pair_gain if set([int(left), int(right)]) == set([2, 7]) else 0
    b37_gain = pair_gain if set([int(left), int(right)]) == set([3, 7]) else 0
    b57_gain = pair_gain if set([int(left), int(right)]) == set([5, 7]) else 0
    capacity = int(row["capacity_contribution"])
    b57 = int(row["B57_contribution"])
    score = (
        18 * b27_gain
        + 18 * b37_gain
        + 8 * b57_gain
        + 3 * capacity
        + 4 * b57
        - (5 if int(row["coordinate"]) == 1 else 0)
    )
    if family == "postsplit_survivor_pair_micro":
        score += 4 * capacity + 6 * b57
    if family == "quotient_fiber_pair27_37_micro":
        score += 2 * (b27_gain + b37_gain)
    return {
        "coordinate": int(row["coordinate"]),
        "quotient_fiber": int(row["quotient_fiber"]),
        "left": int(left),
        "right": int(right),
        "post_B27_delta": int(b27_gain),
        "post_B37_delta": int(b37_gain),
        "post_B57_delta": int(b57_gain),
        "capacity_contribution": capacity,
        "B57_contribution": b57,
        "score": int(score),
        "family": family,
    }


def pair_cycle(family):
    if family == "pair27_micro":
        return [(2, 7)]
    if family == "pair37_micro":
        return [(3, 7)]
    if family == "balanced_pair27_37_micro":
        return [(2, 7), (3, 7)]
    if family == "postsplit_survivor_pair_micro":
        return [(2, 7), (3, 7), (2, 7), (3, 7), (5, 7)]
    if family == "quotient_fiber_pair27_37_micro":
        return [(2, 7), (3, 7), (2, 7), (3, 7)]
    raise ValueError("pair cycle not available for %s" % family)


def occupied_augmented_base(base, specs):
    out = dict(base)
    out["occupied"] = list(base["occupied"]) + [int(spec["position"]) for spec in specs]
    return out


def repair_rows_from_ledger(ledger, family):
    rows = [
        row
        for row in ledger["coordinate_rows"]
        if not row["is_occupied_by_pairclass_or_partial"] and int(row["coordinate"]) != 1
    ]
    candidates = []
    if family == "triple_237":
        for row in rows:
            c27 = candidate_delta(row, 2, 7, family)
            c37 = candidate_delta(row, 3, 7, family)
            merged = {
                "coordinate": int(row["coordinate"]),
                "quotient_fiber": int(row["quotient_fiber"]),
                "post_B27_delta": c27["post_B27_delta"],
                "post_B37_delta": c37["post_B37_delta"],
                "post_B57_delta": 0,
                "capacity_contribution": int(row["capacity_contribution"]),
                "B57_contribution": int(row["B57_contribution"]),
                "score": int(c27["score"] + c37["score"] + 10),
                "family": family,
                "triple": True,
            }
            candidates.append(merged)
    else:
        for row in rows:
            for left, right in pair_cycle(family):
                candidates.append(candidate_delta(row, left, right, family))
    if family == "quotient_fiber_pair27_37_micro":
        candidates = sorted(
            candidates,
            key=lambda row: (row["quotient_fiber"], -row["score"], row["coordinate"], row.get("left", 0)),
        )
        out = []
        used = {}
        for candidate in candidates:
            fiber = candidate["quotient_fiber"]
            used[fiber] = used.get(fiber, 0)
            if used[fiber] >= 4:
                continue
            out.append(candidate)
            used[fiber] += 1
        return out
    return sorted(
        candidates,
        key=lambda row: (
            row["score"],
            row["post_B27_delta"] + row["post_B37_delta"],
            row["B57_contribution"],
            row["capacity_contribution"],
            -row["coordinate"],
        ),
        reverse=True,
    )


def microrepair_specs(ledger, family, budget):
    candidates = repair_rows_from_ledger(ledger, family)
    specs = []
    deltas = []
    idx = 0
    seen = set()
    while len(specs) < int(budget) and candidates:
        candidate = candidates[idx % len(candidates)]
        idx += 1
        if candidate.get("triple"):
            key = ("triple", candidate["coordinate"], len(specs) // max(1, len(candidates)))
            if key in seen and len(candidates) >= int(budget):
                continue
            seen.add(key)
            if len(specs) + 2 > int(budget):
                break
            specs.append(equality_spec(2, 7, candidate["coordinate"], family, candidate))
            specs.append(equality_spec(3, 7, candidate["coordinate"], family, candidate))
            deltas.append(candidate)
        else:
            key = (
                candidate["left"],
                candidate["right"],
                candidate["coordinate"],
                len(specs) // max(1, len(candidates)),
            )
            if key in seen and len(candidates) >= int(budget):
                continue
            seen.add(key)
            specs.append(
                equality_spec(candidate["left"], candidate["right"], candidate["coordinate"], family, candidate)
            )
            deltas.append(candidate)
        if idx > int(budget) * 12 and len(candidates) < int(budget):
            break
    return specs, deltas


def delta_summary(rows):
    return {
        "rows": len(rows),
        "post_B27_delta": sum(row["post_B27_delta"] for row in rows),
        "post_B37_delta": sum(row["post_B37_delta"] for row in rows),
        "post_B57_delta": sum(row["post_B57_delta"] for row in rows),
        "score": sum(row["score"] for row in rows),
    }


def classify(row):
    if row.get("pair_B_values") is None:
        return "MICROREPAIR_INCONSISTENT"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "MICROREPAIR_CAPACITY_LOSS"
    if row["pair_B_values"][4] < PAIR_TARGET:
        return "MICROREPAIR_PAIR57_LOSS"
    if row["six_class_dominance"] > 0 or not collapse_reduced(row["degenerate_classes"]):
        return "MICROREPAIR_COLLAPSE_RETURNS"
    if row["pair_B_values"][1] < PAIR_TARGET or row["pair_B_values"][2] < PAIR_TARGET:
        return "MICROREPAIR_PAIRCLASS_NOT_REPAIRED"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "MICROREPAIR_EXACT_CANDIDATE"
    return "MICROREPAIR_LOW_RESCHEDULE"


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "MICROREPAIR_EXACT_CANDIDATE",
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


def setup(codesign, slack):
    scalable, residual, F, base, ledger = codesign.setup(slack)
    return scalable, residual, F, base, ledger


def evaluate_micro(codesign, scalable, residual, F, base, vector_value, metadata):
    row = codesign.evaluate(scalable, residual, F, base, vector_value, metadata)
    row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
    row["pair27_repaired"] = row["pair_B_values"][1] >= PAIR_TARGET
    row["pair37_repaired"] = row["pair_B_values"][2] >= PAIR_TARGET
    row["pair27_37_repaired"] = row["pair27_repaired"] and row["pair37_repaired"]
    row["pair57_preserving"] = row["pair_B_values"][4] >= PAIR_TARGET
    row["collapse_preserving"] = row["six_class_dominance"] == 0 and collapse_reduced(row["degenerate_classes"])
    row["pair_deficit_to_654"] = [PAIR_TARGET - value for value in row["pair_B_values"]]
    row["failure_mode"] = classify(row)
    return row


def prepare_context():
    codesign = load_source_module(CODESIGN_AUDIT_PATH, "reserve_pairclass_codesign_helpers_micro_case")
    slack = load_source_module(SLACK_AUDIT_PATH, "capacity_slack_helpers_micro_case")
    scalable, residual, F, base, ledger = setup(codesign, slack)
    codesign_rows, codesign_deltas = codesign.codesign_specs(ledger, BEST_ROW_FAMILY, BEST_ROW_EXTENSION_SIZE)
    split = codesign.known_split_specs(slack)
    fixed_specs = codesign_rows + split
    baseline_vector, baseline_solve = codesign.solve_with_specs(scalable, residual, F, base, fixed_specs)
    if baseline_vector is None:
        raise RuntimeError("baseline post-split solve failed: %s" % baseline_solve)
    baseline_post = evaluate_micro(
        codesign,
        scalable,
        residual,
        F,
        base,
        baseline_vector,
        {
            "phase": "baseline_post_split",
            "row_family": BEST_ROW_FAMILY,
            "row_extension_size": BEST_ROW_EXTENSION_SIZE,
            "split_specs": split,
            "codesign_row_count": len(codesign_rows),
            "delta_summary": codesign.delta_summary(codesign_deltas),
            **baseline_solve,
        },
    )
    micro_ledger_base = occupied_augmented_base(base, fixed_specs)
    micro_ledger = slack.ledger_from_base(residual, F, base["powers"], micro_ledger_base, baseline_vector)
    return {
        "codesign": codesign,
        "slack": slack,
        "scalable": scalable,
        "residual": residual,
        "F": F,
        "base": base,
        "codesign_rows": codesign_rows,
        "codesign_deltas": codesign_deltas,
        "split": split,
        "fixed_specs": fixed_specs,
        "baseline_post": baseline_post,
        "micro_ledger": micro_ledger,
        "baseline_solve": baseline_solve,
    }


def case_record_from_context(context, case):
    codesign = context["codesign"]
    scalable = context["scalable"]
    residual = context["residual"]
    F = context["F"]
    base = context["base"]
    codesign_rows = context["codesign_rows"]
    codesign_deltas = context["codesign_deltas"]
    split = context["split"]
    fixed_specs = context["fixed_specs"]
    baseline_post = context["baseline_post"]
    micro_ledger = context["micro_ledger"]
    start = time.time()
    repair_specs, repair_deltas = microrepair_specs(micro_ledger, case["repair_family"], case["repair_budget"])
    vector_value, solve_meta = codesign.solve_with_specs(scalable, residual, F, base, fixed_specs + repair_specs)
    if vector_value is None:
        return {
            **case,
            "base_system": "reserve_pairclass_codesign_quotient_fiber_buffer_extension96",
            "baseline_post_split": {
                "capacity_upper_bound": baseline_post["capacity_upper_bound"],
                "pair_B_values": baseline_post["pair_B_values"],
                "degenerate_classes": baseline_post["degenerate_classes"],
            },
            "repair_specs_preview": repair_specs[:12],
            "repair_delta_summary": delta_summary(repair_deltas),
            "failure_mode": "MICROREPAIR_INCONSISTENT",
            "solve_meta": solve_meta,
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    row = evaluate_micro(
        codesign,
        scalable,
        residual,
        F,
        base,
        vector_value,
        {
            **case,
            "phase": "postsplit_microrepair",
            "base_system": "reserve_pairclass_codesign_quotient_fiber_buffer_extension96",
            "row_family": BEST_ROW_FAMILY,
            "row_extension_size": BEST_ROW_EXTENSION_SIZE,
            "codesign_row_count": len(codesign_rows),
            "microrepair_row_count": len(repair_specs),
            "split_specs": split,
            "repair_specs_preview": repair_specs[:12],
            "repair_delta_summary": delta_summary(repair_deltas),
            **solve_meta,
        },
    )
    row["baseline_post_split"] = {
        "capacity_upper_bound": baseline_post["capacity_upper_bound"],
        "pair_B_values": baseline_post["pair_B_values"],
        "pair_deficit_to_654": baseline_post["pair_deficit_to_654"],
        "degenerate_classes": baseline_post["degenerate_classes"],
    }
    row["elapsed_seconds"] = float(round(float(time.time() - start), 3))
    return row


def case_record(case):
    return case_record_from_context(prepare_context(), case)


def cases():
    return [
        {"repair_budget": int(budget), "repair_family": family}
        for budget in REPAIR_BUDGETS
        for family in REPAIR_FAMILIES
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    ledger_scan = load_python_module(LEDGER_SCAN_PATH, "postsplit_pair27_37_microrepair_ledger")
    context = prepare_context()
    results = [case_record_from_context(context, case) for case in cases()]
    best_pool = [row for row in results if row.get("pair_B_values") is not None]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    search = {
        "exact_field": "GF(17^32)",
        "base_system": "reserve_pairclass_codesign_quotient_fiber_buffer_extension96",
        "base_row_family": BEST_ROW_FAMILY,
        "base_row_extension_size": BEST_ROW_EXTENSION_SIZE,
        "repair_budgets": REPAIR_BUDGETS,
        "repair_families": REPAIR_FAMILIES,
        "planned_repair_budgets": PLANNED_REPAIR_BUDGETS,
        "planned_repair_families": PLANNED_REPAIR_FAMILIES,
        "case_timeout_seconds": None,
        "execution_mode": "single_context_in_process",
        "systems_tested": len(results),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "MICROREPAIR_TIMEOUT"),
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
    return jsonable(ledger_scan.build_record(microrepair=search))


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
        print("SAGE_AUDIT_M1_A327_POSTSPLIT_PAIR27_37_MICROREPAIR_OK")
        print("systems_tested: %d" % record["microrepair"]["systems_tested"])
        print("timeouts: %d" % record["microrepair"]["timeouts"])
        print("exact_vectors_constructed: %d" % record["microrepair"]["exact_vectors_constructed"])
        print("capacity_preserving_vectors: %d" % record["microrepair"]["capacity_preserving_vectors"])
        print("pair27_37_repaired_vectors: %d" % record["microrepair"]["pair27_37_repaired_vectors"])
        print("best_failure_mode: %s" % record["microrepair"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
