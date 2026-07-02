#!/usr/bin/env sage
"""Exact compensated repaired-skeleton split audit."""

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

REPAIRED_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_repaired_skeleton_nondegenerate_split.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_compensated_repaired_skeleton_split.py")
PERSISTENT_DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json")
DATA_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split.json")

FREE_PATTERNS = ["d2_first_free"]
SPLIT_FAMILIES = ["split_4_from_157", "split_14_vs_57", "split_1_from_457"]
REPLACEMENT_BUNDLE_SIZES = [8, 16, 32]
SELECTORS = ["capacity_first", "B27_B37_first", "B47_first", "balanced_repair", "quotient_fiber_local"]

REPLACEMENT_CLASSES = {
    "capacity_first": [[1, 4, 5, 7], [4, 5, 7], [1, 4, 7], [2, 3, 7], [2, 4, 7], [3, 4, 7]],
    "B27_B37_first": [[2, 3, 7], [2, 7], [3, 7], [2, 4, 7], [3, 4, 7]],
    "B47_first": [[4, 7], [1, 4, 7], [4, 5, 7], [2, 4, 7], [3, 4, 7], [1, 4], [1, 4, 5]],
    "balanced_repair": [[2, 3, 7], [4, 7], [2, 4, 7], [3, 4, 7], [1, 4, 7], [4, 5, 7]],
    "quotient_fiber_local": [[2, 3, 7], [4, 7], [2, 4, 7], [3, 4, 7], [1, 4, 7], [4, 5, 7]],
}


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


def load_json(path):
    with path.open() as handle:
        return json.load(handle)


def residual_class_reduced(degenerate_classes):
    return [1, 4, 5, 7] not in degenerate_classes


def equality_spec(left, right, position, kind, replacement_class=None, delta=None):
    out = {
        "left": int(left),
        "right": int(right),
        "position": int(position),
        "gamma": 0,
        "kind": kind,
    }
    if replacement_class is not None:
        out["replacement_class"] = [int(value) for value in replacement_class]
    if delta is not None:
        out["delta"] = delta
    return out


def class_specs(replacement_class, position, selector, candidate):
    witnesses = [int(value) for value in replacement_class]
    anchor = 7 if 7 in witnesses else witnesses[0]
    specs = []
    for witness in witnesses:
        if witness == anchor:
            continue
        specs.append(equality_spec(witness, anchor, position, selector, witnesses, candidate))
    return specs


def replacement_delta(row, replacement_class):
    size = len(replacement_class)
    has = lambda a, b: int(a) in replacement_class and int(b) in replacement_class
    return {
        "capacity": max(0, int(size) - int(row["capacity_after"])),
        "B27": max(0, 2 - int(row["B27_after"])) if has(2, 7) else 0,
        "B37": max(0, 2 - int(row["B37_after"])) if has(3, 7) else 0,
        "B47": max(0, 2 - int(row["B47_after"])) if has(4, 7) else 0,
        "B57": max(0, 2 - int(row["B57_after"])) if has(5, 7) else 0,
    }


def score_candidate(row, replacement_class, selector, split_fiber):
    delta = replacement_delta(row, replacement_class)
    cap_damage = max(0, int(row["capacity_before"]) - int(row["capacity_after"]))
    b27_damage = max(0, int(row["B27_before"]) - int(row["B27_after"]))
    b37_damage = max(0, int(row["B37_before"]) - int(row["B37_after"]))
    b47_damage = max(0, int(row["B47_before"]) - int(row["B47_after"]))
    b57_damage = max(0, int(row["B57_before"]) - int(row["B57_after"]))
    local_bonus = 10 if int(row["quotient_fiber"]) == int(split_fiber) else 0
    if selector == "capacity_first":
        score = 18 * cap_damage + 8 * delta["capacity"] + 4 * b47_damage + 3 * (b27_damage + b37_damage)
    elif selector == "B27_B37_first":
        score = 18 * (b27_damage + b37_damage) + 12 * (delta["B27"] + delta["B37"]) + 2 * cap_damage
    elif selector == "B47_first":
        score = 24 * b47_damage + 18 * delta["B47"] + 3 * cap_damage
    elif selector == "quotient_fiber_local":
        score = local_bonus + 8 * cap_damage + 10 * (b27_damage + b37_damage) + 14 * b47_damage
    else:
        score = 5 * min(delta["B27"], delta["B37"]) + 4 * delta["B47"] + 3 * delta["capacity"]
        score += 10 * cap_damage + 12 * (b27_damage + b37_damage) + 16 * b47_damage
    concentration_penalty = int(row["quotient_fiber"])
    return int(score - concentration_penalty)


def replacement_candidates(ledger_rows, selector, split_row):
    split_fiber = int(split_row["quotient_fiber"])
    rows = [row for row in ledger_rows if int(row["coordinate"]) != int(split_row["coordinate"])]
    if selector == "quotient_fiber_local":
        local = [row for row in rows if int(row["quotient_fiber"]) == split_fiber]
        if len(local) >= 8:
            rows = local
    candidates = []
    for row in rows:
        for replacement_class in REPLACEMENT_CLASSES[selector]:
            delta = replacement_delta(row, replacement_class)
            candidate = {
                "coordinate": int(row["coordinate"]),
                "quotient_fiber": int(row["quotient_fiber"]),
                "replacement_class": [int(value) for value in replacement_class],
                "predicted_delta": delta,
                "split_damage_score": int(row["split_damage_score"]),
                "replacement_priority_score": int(row["replacement_priority_score"]),
                "selector_score": score_candidate(row, replacement_class, selector, split_fiber),
                "before_after": {
                    "capacity": [int(row["capacity_before"]), int(row["capacity_after"])],
                    "B27": [int(row["B27_before"]), int(row["B27_after"])],
                    "B37": [int(row["B37_before"]), int(row["B37_after"])],
                    "B47": [int(row["B47_before"]), int(row["B47_after"])],
                    "B57": [int(row["B57_before"]), int(row["B57_after"])],
                },
            }
            candidates.append(candidate)
    return sorted(
        candidates,
        key=lambda row: (
            row["selector_score"],
            row["predicted_delta"]["capacity"],
            row["predicted_delta"]["B27"] + row["predicted_delta"]["B37"],
            row["predicted_delta"]["B47"],
            row["replacement_priority_score"],
            -row["coordinate"],
        ),
        reverse=True,
    )


def choose_replacement_specs(ledger_rows, selector, bundle_size, split_row):
    candidates = replacement_candidates(ledger_rows, selector, split_row)
    specs = []
    selected = []
    seen_specs = set()
    used_pairs_by_coordinate = set()
    for candidate in candidates:
        key = (candidate["coordinate"], tuple(candidate["replacement_class"]))
        if key in used_pairs_by_coordinate:
            continue
        candidate_specs = class_specs(candidate["replacement_class"], candidate["coordinate"], selector, candidate)
        fresh = []
        for spec in candidate_specs:
            spec_key = (spec["left"], spec["right"], spec["position"])
            if spec_key not in seen_specs:
                fresh.append(spec)
        if not fresh:
            continue
        selected.append(candidate)
        used_pairs_by_coordinate.add(key)
        for spec in fresh:
            seen_specs.add((spec["left"], spec["right"], spec["position"]))
            specs.append(spec)
        if len(selected) >= int(bundle_size):
            break
    return specs, selected


def classify(row):
    if row.get("pair_B_values") is None:
        return "COMP_REPAIRED_SPLIT_INCONSISTENT"
    if row["six_class_dominance"] > 0:
        return "COMP_REPAIRED_SPLIT_COLLAPSE_RETURNS"
    if row["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED"
    if row["pair_B_values"][1] < PAIR_TARGET or row["pair_B_values"][2] < PAIR_TARGET:
        return "COMP_REPAIRED_SPLIT_PAIR27_37_LOSS"
    if row["pair_B_values"][3] < PAIR_TARGET:
        return "COMP_REPAIRED_SPLIT_PAIR47_LOSS"
    if row["pair_B_values"][4] < PAIR_TARGET:
        return "COMP_REPAIRED_SPLIT_PAIR57_LOSS"
    if not residual_class_reduced(row["degenerate_classes"]):
        return "COMP_REPAIRED_SPLIT_COLLAPSE_RETURNS"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE"
    if row.get("distinct_codewords") is True:
        return "COMP_REPAIRED_SPLIT_LOW_RESCHEDULE"
    return "COMP_REPAIRED_SPLIT_PARTIAL_DISTINCT"


def vector_sort_key(row):
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE",
        row.get("pair_guard_preserving") is True,
        row.get("capacity_upper_bound", -1) >= TARGET_AGREEMENT,
        row.get("partial_split") is True,
        row.get("distinct_codewords") is True,
        exact_max,
        min(pair_values[1], pair_values[2], pair_values[3], pair_values[4]),
        row.get("capacity_upper_bound", -1),
        -row.get("six_class_dominance", 10**9),
    )


def evaluate_compensated(context, vector_value, metadata):
    row = context["codesign"].evaluate(
        context["scalable"], context["residual"], context["F"], context["base"], vector_value, metadata
    )
    row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
    row["pair_guard_preserving"] = (
        row["pair_B_values"][1] >= PAIR_TARGET
        and row["pair_B_values"][2] >= PAIR_TARGET
        and row["pair_B_values"][3] >= PAIR_TARGET
        and row["pair_B_values"][4] >= PAIR_TARGET
    )
    row["partial_split"] = residual_class_reduced(row["degenerate_classes"])
    row["nondegenerate"] = row["distinct_codewords"]
    row["failure_mode"] = classify(row)
    return row


def case_record_from_context(context, persistent, case):
    start = time.time()
    split_specs, selected_split_rows = context["repaired_module"].selected_split_specs(
        context["repaired_ledger"], case["split_family"], 1, 8
    )
    if not selected_split_rows:
        return {
            **case,
            "failure_mode": "COMP_REPAIRED_SPLIT_INCONSISTENT",
            "vector_results": [],
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    replacement_specs, selected_replacements = choose_replacement_specs(
        persistent["exact_state_replay"]["coordinate_ledger"]["rows"],
        case["selector"],
        case["replacement_bundle_size"],
        selected_split_rows[0],
    )
    specs = split_specs + replacement_specs
    vector_value, solve_meta = context["repaired_module"].independent_solve_with_pattern(
        context, specs, FREE_PATTERNS[0]
    )
    metadata = {
        **case,
        "phase": "compensated_repaired_skeleton_split",
        "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
        "split_specs": split_specs,
        "selected_split_rows": selected_split_rows,
        "replacement_specs_preview": replacement_specs[:24],
        "selected_replacements_preview": selected_replacements[:24],
        "replacement_specs_count": len(replacement_specs),
        "selected_replacements_count": len(selected_replacements),
        **solve_meta,
    }
    if vector_value is None:
        return {
            **case,
            "split_specs": split_specs,
            "selected_split_rows": selected_split_rows,
            "replacement_specs_count": len(replacement_specs),
            "selected_replacements_count": len(selected_replacements),
            "failure_mode": "COMP_REPAIRED_SPLIT_INCONSISTENT",
            "solve_meta": solve_meta,
            "vector_results": [],
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    row = evaluate_compensated(context, vector_value, metadata)
    row["elapsed_seconds"] = float(round(float(time.time() - start), 3))
    return {
        **case,
        "split_specs": split_specs,
        "selected_split_rows": selected_split_rows,
        "replacement_specs_count": len(replacement_specs),
        "selected_replacements_count": len(selected_replacements),
        "selected_replacements_preview": selected_replacements[:24],
        "elapsed_seconds": row["elapsed_seconds"],
        "best": row,
        "vector_results": [row],
        "failure_mode": row["failure_mode"],
    }


def cases():
    return [
        {
            "split_family": split_family,
            "replacement_bundle_size": int(bundle_size),
            "selector": selector,
        }
        for split_family in SPLIT_FAMILIES
        for bundle_size in REPLACEMENT_BUNDLE_SIZES
        for selector in SELECTORS
    ]


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def audit_record():
    scan = load_python_module(LEDGER_SCAN_PATH, "compensated_repaired_skeleton_split_scan")
    repaired = load_source_module(REPAIRED_AUDIT_PATH, "repaired_skeleton_comp_helpers")
    persistent = load_json(PERSISTENT_DATA_PATH)
    context = repaired.repaired_context()
    context["repaired_module"] = repaired
    results = [case_record_from_context(context, persistent, case) for case in cases()]
    vectors = [row for result in results for row in result.get("vector_results", [])]
    best_pool = vectors or [row.get("best", row) for row in results]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    search = {
        "exact_field": "GF(17^32)",
        "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
        "split_families": SPLIT_FAMILIES,
        "replacement_bundle_sizes": REPLACEMENT_BUNDLE_SIZES,
        "selectors": SELECTORS,
        "free_patterns": FREE_PATTERNS,
        "persistent_state_result_hash": persistent["exact_state_replay"]["state_hashes"]["result_hash"],
        "systems_tested": len(results),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "COMP_REPAIRED_SPLIT_TIMEOUT"),
        "exact_vectors_constructed": len(vectors),
        "capacity_preserving_vectors": sum(1 for row in vectors if row.get("capacity_preserving") is True),
        "pair_guard_preserving_vectors": sum(1 for row in vectors if row.get("pair_guard_preserving") is True),
        "partial_split_vectors": sum(1 for row in vectors if row.get("partial_split") is True),
        "nondegenerate_vectors": sum(1 for row in vectors if row.get("distinct_codewords") is True),
        "failure_mode_counts": failure_counts(vectors or results),
        "best_capacity": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_collapse_pattern": None if best is None else best.get("degenerate_classes"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_agreement_vector": None if best is None else best.get("exact_agreement_vector"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }
    return jsonable(scan.build_record(compensated_split=search))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--single-case")
    args = parser.parse_args()
    if args.single_case:
        repaired = load_source_module(REPAIRED_AUDIT_PATH, "repaired_skeleton_comp_single")
        persistent = load_json(PERSISTENT_DATA_PATH)
        context = repaired.repaired_context()
        context["repaired_module"] = repaired
        print(json.dumps(jsonable(case_record_from_context(context, persistent, json.loads(args.single_case))), sort_keys=True))
        return
    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_COMPENSATED_REPAIRED_SKELETON_SPLIT_OK")
        print("systems_tested: %d" % record["compensated_split"]["systems_tested"])
        print("exact_vectors_constructed: %d" % record["compensated_split"]["exact_vectors_constructed"])
        print("capacity_preserving_vectors: %d" % record["compensated_split"]["capacity_preserving_vectors"])
        print("pair_guard_preserving_vectors: %d" % record["compensated_split"]["pair_guard_preserving_vectors"])
        print("best_failure_mode: %s" % record["compensated_split"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
