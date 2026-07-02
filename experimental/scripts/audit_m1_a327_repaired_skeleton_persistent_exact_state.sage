#!/usr/bin/env sage
"""Exact-state replay/cache audit for the repaired M1 a=327 skeleton."""

from __future__ import annotations

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path


TARGET_AGREEMENT = 327
REPAIRED_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_repaired_skeleton_nondegenerate_split.sage")
LEDGER_SCAN_PATH = Path("experimental/scripts/scan_m1_a327_repaired_skeleton_persistent_exact_state.py")
DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json")
FAILED_SPLIT_CASE = {"split_family": "split_4_from_157", "pin_budget": 1, "coordinate_limit": 8}


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


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def vector_hash(vector_value):
    return hash_payload([str(value) for value in vector_value])


def value_state(residual, F, powers, vector_value):
    values = residual.exact_values_from_vector(F, powers, vector_value)
    class_rows = residual.class_masks_by_position(values)
    codeword_hashes = [hash_payload([str(value) for value in row]) for row in values]
    return {
        "values": values,
        "class_rows": class_rows,
        "codeword_value_hash": hash_payload(codeword_hashes),
        "value_class_hash": hash_payload(class_rows),
    }


def capacity(classes):
    return max(int(mask).bit_count() for mask in classes)


def pair(classes, left, right):
    return max((int(mask) & int((1 << (left - 1)) | (1 << (right - 1)))).bit_count() for mask in classes)


def compact_pattern(repaired, classes):
    return repaired.class_pattern(classes)


def coordinate_ledger(repaired, before_classes, after_classes):
    rows = []
    for pos, (before, after) in enumerate(zip(before_classes, after_classes)):
        capacity_before = capacity(before)
        capacity_after = capacity(after)
        b27_before = pair(before, 2, 7)
        b27_after = pair(after, 2, 7)
        b37_before = pair(before, 3, 7)
        b37_after = pair(after, 3, 7)
        b47_before = pair(before, 4, 7)
        b47_after = pair(after, 4, 7)
        b57_before = pair(before, 5, 7)
        b57_after = pair(after, 5, 7)
        cap_damage = max(0, capacity_before - capacity_after)
        b27_damage = max(0, b27_before - b27_after)
        b37_damage = max(0, b37_before - b37_after)
        b47_damage = max(0, b47_before - b47_after)
        b57_damage = max(0, b57_before - b57_after)
        split_damage = 8 * cap_damage + 12 * (b27_damage + b37_damage + b47_damage) + 4 * b57_damage
        replacement_priority = 10 * cap_damage + 16 * (b27_damage + b37_damage + b47_damage) + 3 * b57_damage
        changed = sorted(int(mask) for mask in before) != sorted(int(mask) for mask in after)
        rows.append(
            {
                "coordinate": int(pos),
                "quotient_fiber": int(pos) % 16,
                "value_class_pattern_before": compact_pattern(repaired, before),
                "value_class_pattern_after": compact_pattern(repaired, after),
                "changed_by_failed_split": bool(changed),
                "capacity_before": int(capacity_before),
                "capacity_after": int(capacity_after),
                "B27_before": int(b27_before),
                "B27_after": int(b27_after),
                "B37_before": int(b37_before),
                "B37_after": int(b37_after),
                "B47_before": int(b47_before),
                "B47_after": int(b47_after),
                "B57_before": int(b57_before),
                "B57_after": int(b57_after),
                "split_damage_score": int(split_damage),
                "replacement_priority_score": int(replacement_priority),
            }
        )
    return rows


def replay_state():
    repaired = load_source_module(REPAIRED_AUDIT_PATH, "repaired_skeleton_split_replay_helpers")
    context = repaired.repaired_context()
    split_specs, selected_split_rows = repaired.selected_split_specs(
        context["repaired_ledger"],
        FAILED_SPLIT_CASE["split_family"],
        FAILED_SPLIT_CASE["pin_budget"],
        FAILED_SPLIT_CASE["coordinate_limit"],
    )
    failed_vector, failed_solve = repaired.independent_solve_with_pattern(context, split_specs, "d2_first_free")
    if failed_vector is None:
        raise RuntimeError("failed split replay did not construct vector: %s" % failed_solve)
    failed_row = repaired.evaluate_split(
        context,
        failed_vector,
        {
            **FAILED_SPLIT_CASE,
            "phase": "persistent_exact_state_failed_split_replay",
            "base_system": "postsplit_microrepair_stage2_triple_237_budget32",
            "total_triple_237_budget": repaired.TOTAL_STAGE2_BUDGET,
            "split_specs": split_specs,
            "selected_split_rows": selected_split_rows,
            **failed_solve,
        },
    )
    base_state = value_state(context["residual"], context["F"], context["base"]["powers"], context["repaired_base_vector"])
    failed_state = value_state(context["residual"], context["F"], context["base"]["powers"], failed_vector)
    ledger_rows = coordinate_ledger(repaired, base_state["class_rows"], failed_state["class_rows"])
    ledger_hash = hash_payload(ledger_rows)
    state_hashes = {
        "base_vector_hash": vector_hash(context["repaired_base_vector"]),
        "base_codeword_value_hash": base_state["codeword_value_hash"],
        "base_value_class_hash": base_state["value_class_hash"],
        "failed_split_vector_hash": vector_hash(failed_vector),
        "failed_split_codeword_value_hash": failed_state["codeword_value_hash"],
        "failed_split_value_class_hash": failed_state["value_class_hash"],
        "fixed_specs_hash": hash_payload(context["repaired_fixed_specs"]),
        "failed_split_specs_hash": hash_payload(split_specs),
        "coordinate_ledger_hash": ledger_hash,
    }
    row_state = {
        "fixed_specs_count": len(context["repaired_fixed_specs"]),
        "failed_split_specs_count": len(split_specs),
        "selected_split_rows": selected_split_rows,
        "source_row_count": context["repaired_base_row"]["row_count"],
        "source_effective_row_count": context["repaired_base_row"]["effective_row_count"],
        "source_rank_after": context["repaired_base_row"]["rank_after"],
        "source_nullity_after": context["repaired_base_row"]["nullity_after"],
        "failed_split_row_count": failed_row["row_count"],
        "failed_split_effective_row_count": failed_row["effective_row_count"],
        "failed_split_rank_after": failed_row["rank_after"],
        "failed_split_nullity_after": failed_row["nullity_after"],
        "free_pattern": "d2_first_free",
        "pivot_columns_persisted": False,
        "free_columns_persisted": False,
        "nonpersistent_reason": "Current helper APIs expose stable rank/nullity and specs but not reusable prepared matrices.",
    }
    replay = {
        "exact_field": "GF(17^32)",
        "H_order": 512,
        "replay_status": "PASS",
        "source_skeleton": {
            "commit": "2dfd1d9",
            "capacity": context["repaired_base_row"]["capacity_upper_bound"],
            "pair_B_values": context["repaired_base_row"]["pair_B_values"],
            "collapse_pattern": context["repaired_base_row"]["degenerate_classes"],
            "six_class_dominance": context["repaired_base_row"]["six_class_dominance"],
            "distinct_codewords": context["repaired_base_row"]["distinct_codewords"],
        },
        "failed_split": {
            "commit": "7a02b97",
            "split_family": FAILED_SPLIT_CASE["split_family"],
            "capacity": failed_row["capacity_upper_bound"],
            "pair_B_values": failed_row["pair_B_values"],
            "collapse_pattern": failed_row["degenerate_classes"],
            "six_class_dominance": failed_row["six_class_dominance"],
            "failure_mode": failed_row["failure_mode"],
        },
        "state_hashes": state_hashes,
        "row_state": row_state,
        "coordinate_ledger": {
            "coordinates": len(ledger_rows),
            "ledger_hash": ledger_hash,
            "changed_coordinates": sum(1 for row in ledger_rows if row["changed_by_failed_split"]),
            "rows": ledger_rows,
        },
    }
    replay["state_hashes"]["result_hash"] = hash_payload(
        {
            "source_skeleton": replay["source_skeleton"],
            "failed_split": replay["failed_split"],
            "row_state": row_state,
            "coordinate_ledger_hash": ledger_hash,
        }
    )
    return replay


def audit_record():
    scan = load_python_module(LEDGER_SCAN_PATH, "persistent_exact_state_scan")
    return scan.build_record(exact_state_replay=jsonable(replay_state()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()
    record = jsonable(audit_record())
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_REPAIRED_SKELETON_PERSISTENT_EXACT_STATE_OK")
        print("replay_status: %s" % record["exact_state_replay"]["replay_status"])
        print("source_capacity: %d" % record["exact_state_replay"]["source_skeleton"]["capacity"])
        print("failed_split_capacity: %d" % record["exact_state_replay"]["failed_split"]["capacity"])
        print("coordinate_rows: %d" % record["exact_state_replay"]["coordinate_ledger"]["coordinates"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
