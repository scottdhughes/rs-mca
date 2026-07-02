#!/usr/bin/env sage
"""Cached exact compensated repaired-skeleton split v2 audit."""

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

SCAN_PATH = Path("experimental/scripts/scan_m1_a327_compensated_repaired_skeleton_split_v2.py")
DATA_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")
NATIVE_CACHE_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_repaired_skeleton_sage_native_cache.sage")
REPAIRED_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_repaired_skeleton_nondegenerate_split.sage")
COMP_V1_AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_compensated_repaired_skeleton_split.sage")
PERSISTENT_DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json")

SPLIT_FAMILIES = ["split_4_from_157", "split_14_vs_57", "split_1_from_457"]
REPLACEMENT_BUNDLE_SIZES = [8, 16, 32]
SELECTORS = ["capacity_first", "B27_B37_first", "B47_first", "balanced_repair", "quotient_fiber_local"]
PRIORITY_CASE_KEYS = [
    ("split_4_from_157", 32, "B47_first"),
    ("split_4_from_157", 32, "balanced_repair"),
    ("split_4_from_157", 32, "quotient_fiber_local"),
    ("split_4_from_157", 16, "B47_first"),
    ("split_4_from_157", 16, "balanced_repair"),
    ("split_14_vs_57", 32, "B47_first"),
    ("split_14_vs_57", 32, "balanced_repair"),
    ("split_1_from_457", 32, "B47_first"),
]
REPLACEMENT_CLASSES = {
    "capacity_first": [[1, 4, 5, 7], [4, 5, 7], [1, 4, 7], [2, 3, 7], [2, 4, 7], [3, 4, 7], [4, 7]],
    "B27_B37_first": [[2, 3, 7], [2, 7], [3, 7], [2, 4, 7], [3, 4, 7], [1, 4, 5, 7]],
    "B47_first": [[4, 7], [1, 4, 7], [4, 5, 7], [2, 4, 7], [3, 4, 7], [1, 4], [1, 4, 5], [1, 4, 5, 7]],
    "balanced_repair": [[2, 3, 7], [4, 7], [2, 4, 7], [3, 4, 7], [1, 4, 7], [4, 5, 7], [1, 4, 5, 7]],
    "quotient_fiber_local": [[2, 3, 7], [4, 7], [2, 4, 7], [3, 4, 7], [1, 4, 7], [4, 5, 7], [1, 4, 5, 7]],
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
    module.load = load
    module.save = save
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


def row_dot(row, values):
    total = row[0] * 0
    for idx in range(len(values)):
        coeff = row[idx]
        if coeff != 0:
            total += coeff * values[idx]
    return total


class DirectionCache:
    def __init__(self, artifact):
        self.artifact = artifact
        self.A = artifact["matrix"]
        self.pivots = [int(col) for col in artifact["pivots"][: self.A.nrows()]]
        self.pivot_inverse = artifact["pivot_inverse"]
        self.cache = {}

    def direction(self, free_col):
        free_col = int(free_col)
        if free_col not in self.cache:
            self.cache[free_col] = self.pivot_inverse * (-self.A.column(free_col))
        return self.cache[free_col]


def candidate_free_columns(rows, artifact):
    scored = []
    for col in artifact["free_columns"]:
        col = int(col)
        score = sum(1 for row in rows if row[col] != 0)
        if score:
            scored.append((score, col))
    scored.sort(reverse=True)
    nonzero = [col for _, col in scored]
    remaining = [int(col) for col in artifact["free_columns"] if int(col) not in set(nonzero)]
    return nonzero + remaining


def count_schedule(row_count, candidate_count):
    wanted = [
        row_count,
        row_count + 8,
        2 * row_count,
        4 * row_count,
        256,
        candidate_count,
    ]
    out = []
    for value in wanted:
        value = max(1, min(int(value), int(candidate_count)))
        if value not in out:
            out.append(value)
    return out


def solve_cached_append(artifact, scalable, residual, powers, specs):
    start = time.time()
    F = artifact["matrix"].base_ring()
    rows, rhs = scalable.pin_rows(residual, F, powers, specs)
    base = list(artifact["base_vector"])
    if not rows:
        return base, {"solve_status": "CACHE_APPEND_EMPTY", "appended_rows": 0}

    deltas = [rhs[idx] - row_dot(rows[idx], base) for idx in range(len(rows))]
    if all(delta == 0 for delta in deltas):
        return base, {
            "solve_status": "CACHE_APPEND_ZERO_DELTA",
            "appended_rows": len(rows),
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }

    directions = DirectionCache(artifact)
    candidates = candidate_free_columns(rows, artifact)
    if not candidates:
        return None, {
            "solve_status": "COMP_REPAIRED_SPLIT_INCONSISTENT",
            "appended_rows": len(rows),
            "error": "no free columns touch appended rows",
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }

    last_error = None
    for keep in count_schedule(len(rows), len(candidates)):
        cols = candidates[:keep]
        free_matrix = directions.A.matrix_from_columns(cols)
        sols_matrix = directions.pivot_inverse * (-free_matrix)
        pivot_rows = Matrix(F, [[row[pivot_col] for pivot_col in directions.pivots] for row in rows])
        C = pivot_rows * sols_matrix
        for row_idx, row in enumerate(rows):
            for col_idx, free_col in enumerate(cols):
                C[row_idx, col_idx] += row[int(free_col)]
        try:
            alpha = C.solve_right(vector(F, deltas))
        except Exception as exc:
            last_error = str(exc)
            continue
        out = list(base)
        for idx, scale in enumerate(alpha):
            if scale == 0:
                continue
            free_col = cols[idx]
            out[free_col] += scale
            sol = sols_matrix.column(idx)
            for pivot_idx, pivot_col in enumerate(directions.pivots):
                out[pivot_col] += scale * sol[pivot_idx]
        bad = 0
        for row_idx, row in enumerate(rows):
            if row_dot(row, out) != rhs[row_idx]:
                bad += 1
        if bad:
            last_error = "residual verification failed for %d appended rows" % bad
            continue
        return out, {
            "solve_status": "CACHE_APPEND_SOLVED",
            "appended_rows": len(rows),
            "free_columns_considered": len(cols),
            "free_columns_used": sum(1 for value in alpha if value != 0),
            "direction_cache_size": len(directions.cache),
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }

    return None, {
        "solve_status": "COMP_REPAIRED_SPLIT_INCONSISTENT",
        "appended_rows": len(rows),
        "free_columns_considered": len(candidates),
        "error": last_error or "no residual solution found",
        "elapsed_seconds": float(round(float(time.time() - start), 3)),
    }


def mask_from_witnesses(witnesses):
    mask = int(0)
    for witness in witnesses:
        mask |= int(1 << (int(witness) - 1))
    return mask


def split_ledger_from_artifact(artifact, repaired, residual, F, powers):
    values = residual.exact_values_from_vector(F, powers, list(artifact["base_vector"]))
    class_rows = residual.class_masks_by_position(values)
    occupied = set(int(spec["position"]) for spec in artifact["fixed_specs"])
    coordinate_rows = [repaired.coordinate_row(pos, classes, occupied) for pos, classes in enumerate(class_rows)]
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
    return {
        "coordinates": len(coordinate_rows),
        "capacity_critical_count": sum(1 for row in coordinate_rows if row["is_capacity_critical"]),
        "B27_critical_count": sum(1 for row in coordinate_rows if row["is_B27_critical"]),
        "B37_critical_count": sum(1 for row in coordinate_rows if row["is_B37_critical"]),
        "B57_critical_count": sum(1 for row in coordinate_rows if row["is_B57_critical"]),
        "split_safe_count": sum(1 for row in candidates if row["split_safe_score"] > 0),
        "coordinate_rows_preview": coordinate_rows[:16],
        "candidate_split_rows": candidates[:128],
    }


def residual_class_reduced(degenerate_classes):
    return [1, 4, 5, 7] not in degenerate_classes


def d2_split(degenerate_classes):
    return not any(1 in row and 2 in row for row in degenerate_classes)


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
    if not d2_split(row["degenerate_classes"]) or not residual_class_reduced(row["degenerate_classes"]):
        return "COMP_REPAIRED_SPLIT_COLLAPSE_RETURNS"
    if row.get("exact_max_min") is not None and row["exact_max_min"] >= TARGET_AGREEMENT:
        return "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE"
    if row.get("distinct_codewords") is True:
        return "COMP_REPAIRED_SPLIT_LOW_RESCHEDULE"
    return "COMP_REPAIRED_SPLIT_PARTIAL_DISTINCT"


def evaluate_vector(residual, F, powers, vector_value, metadata):
    row = residual.evaluate_vector(F, powers, vector_value, metadata)
    row["capacity_preserving"] = row["capacity_upper_bound"] >= TARGET_AGREEMENT
    row["pair_guard_preserving"] = (
        row["pair_B_values"][1] >= PAIR_TARGET
        and row["pair_B_values"][2] >= PAIR_TARGET
        and row["pair_B_values"][3] >= PAIR_TARGET
        and row["pair_B_values"][4] >= PAIR_TARGET
    )
    row["partial_split"] = residual_class_reduced(row["degenerate_classes"])
    row["nondegenerate"] = row["distinct_codewords"]
    row["d2_split"] = d2_split(row["degenerate_classes"])
    row["failure_mode"] = classify(row)
    return row


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


def base_cases():
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


def cases():
    keyed = {
        (case["split_family"], case["replacement_bundle_size"], case["selector"]): case
        for case in base_cases()
    }
    ordered = []
    seen = set()
    for key in PRIORITY_CASE_KEYS:
        if key in keyed:
            ordered.append(dict(keyed[key]))
            seen.add(key)
    for case in base_cases():
        key = (case["split_family"], case["replacement_bundle_size"], case["selector"])
        if key not in seen:
            ordered.append(dict(case))
            seen.add(key)
    for idx, case in enumerate(ordered):
        case["case_index"] = int(idx)
    return ordered


def selected_cases_from_args(case_index=None, case_range=None, limit=None):
    selected = cases()
    if case_index is not None:
        idx = int(case_index)
        if idx < 0 or idx >= len(selected):
            raise ValueError("case index out of range: %s" % idx)
        return [selected[idx]]
    if case_range:
        left, right = case_range.split(":", 1)
        start = int(left) if left else 0
        stop = int(right) if right else len(selected)
        selected = selected[start:stop]
    if limit is not None:
        selected = selected[: int(limit)]
    return selected


def case_record(case, artifact, scalable, residual, repaired, comp_v1, persistent, split_ledger, powers):
    start = time.time()
    split_specs, selected_split_rows = repaired.selected_split_specs(split_ledger, case["split_family"], 1, 8)
    if not selected_split_rows:
        return {
            **case,
            "failure_mode": "COMP_REPAIRED_SPLIT_INCONSISTENT",
            "vector_results": [],
            "elapsed_seconds": float(round(float(time.time() - start), 3)),
        }
    replacement_specs, selected_replacements = comp_v1.choose_replacement_specs(
        persistent["exact_state_replay"]["coordinate_ledger"]["rows"],
        case["selector"],
        case["replacement_bundle_size"],
        selected_split_rows[0],
    )
    specs = split_specs + replacement_specs
    vector_value, solve_meta = solve_cached_append(artifact, scalable, residual, powers, specs)
    metadata = {
        **case,
        "phase": "compensated_repaired_skeleton_split_v2",
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
    row = evaluate_vector(residual, artifact["matrix"].base_ring(), powers, vector_value, metadata)
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


def failure_counts(rows):
    out = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def grid_from_results(results, split_ledger):
    vectors = [row for result in results for row in result.get("vector_results", [])]
    best_pool = vectors or [row.get("best", row) for row in results]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    return {
        "systems_planned": len(cases()),
        "systems_tested": len(results),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "COMP_REPAIRED_SPLIT_TIMEOUT"),
        "exact_vectors_constructed": len(vectors),
        "capacity_preserving_vectors": sum(1 for row in vectors if row.get("capacity_preserving") is True),
        "pair_guard_preserving_vectors": sum(1 for row in vectors if row.get("pair_guard_preserving") is True),
        "partial_split_vectors": sum(1 for row in vectors if row.get("partial_split") is True),
        "nondegenerate_vectors": sum(1 for row in vectors if row.get("distinct_codewords") is True),
        "failure_mode_counts": failure_counts(vectors or results),
        "split_families": SPLIT_FAMILIES,
        "replacement_bundle_sizes": REPLACEMENT_BUNDLE_SIZES,
        "selectors": SELECTORS,
        "cache_mode": "SAGE_NATIVE_RESIDUAL_APPEND",
        "split_ledger": {
            "coordinates": split_ledger["coordinates"],
            "capacity_critical_count": split_ledger["capacity_critical_count"],
            "B27_critical_count": split_ledger["B27_critical_count"],
            "B37_critical_count": split_ledger["B37_critical_count"],
            "B57_critical_count": split_ledger["B57_critical_count"],
            "split_safe_count": split_ledger["split_safe_count"],
        },
        "best_capacity": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_collapse_pattern": None if best is None else best.get("degenerate_classes"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_agreement_vector": None if best is None else best.get("exact_agreement_vector"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }


def write_progress(scan, results, split_ledger, path):
    record = jsonable(scan.build_record(compensated_grid=grid_from_results(results, split_ledger)))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")


def audit_record(limit=None, progress_path=None, case_index=None, case_range=None):
    scan = load_python_module(SCAN_PATH, "compensated_repaired_skeleton_split_v2_scan")
    native = load_source_module(NATIVE_CACHE_AUDIT_PATH, "sage_native_cache_helpers_v2")
    repaired = load_source_module(REPAIRED_AUDIT_PATH, "repaired_skeleton_split_helpers_v2")
    comp_v1 = load_source_module(COMP_V1_AUDIT_PATH, "compensated_split_selector_helpers_v2")
    comp_v1.REPLACEMENT_CLASSES = REPLACEMENT_CLASSES
    persistent = load_json(PERSISTENT_DATA_PATH)

    artifact, _ = native.load_cache_artifact()
    scalable, residual = native.load_eval_helpers()
    F = artifact["matrix"].base_ring()
    H = artifact.get("H", [])
    if len(H) != 512:
        _, _, rebuilt_H = residual.field_context()
        H = [F(value) for value in rebuilt_H]
    powers = residual.precompute_powers(F, H)
    split_ledger = split_ledger_from_artifact(artifact, repaired, residual, F, powers)

    selected_cases = selected_cases_from_args(case_index=case_index, case_range=case_range, limit=limit)
    results = []
    for case in selected_cases:
        results.append(case_record(case, artifact, scalable, residual, repaired, comp_v1, persistent, split_ledger, powers))
        if progress_path is not None:
            write_progress(scan, results, split_ledger, progress_path)
    return jsonable(scan.build_record(compensated_grid=grid_from_results(results, split_ledger)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--case-index", type=int)
    parser.add_argument("--case-range")
    parser.add_argument("--list-cases", action="store_true")
    parser.add_argument("--single-case")
    args = parser.parse_args()
    if args.list_cases:
        print(json.dumps(jsonable({"cases": cases(), "systems_planned": len(cases())}), indent=2, sort_keys=True))
        return
    if args.single_case:
        native = load_source_module(NATIVE_CACHE_AUDIT_PATH, "sage_native_cache_helpers_v2_single")
        repaired = load_source_module(REPAIRED_AUDIT_PATH, "repaired_skeleton_split_helpers_v2_single")
        comp_v1 = load_source_module(COMP_V1_AUDIT_PATH, "compensated_split_selector_helpers_v2_single")
        comp_v1.REPLACEMENT_CLASSES = REPLACEMENT_CLASSES
        persistent = load_json(PERSISTENT_DATA_PATH)
        artifact, _ = native.load_cache_artifact()
        scalable, residual = native.load_eval_helpers()
        F = artifact["matrix"].base_ring()
        H = artifact.get("H", [])
        if len(H) != 512:
            _, _, rebuilt_H = residual.field_context()
            H = [F(value) for value in rebuilt_H]
        powers = residual.precompute_powers(F, H)
        split_ledger = split_ledger_from_artifact(artifact, repaired, residual, F, powers)
        print(json.dumps(jsonable(case_record(json.loads(args.single_case), artifact, scalable, residual, repaired, comp_v1, persistent, split_ledger, powers)), sort_keys=True))
        return
    progress_path = DATA_PATH if args.write_json else None
    record = audit_record(limit=args.limit, progress_path=progress_path, case_index=args.case_index, case_range=args.case_range)
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_COMPENSATED_REPAIRED_SKELETON_SPLIT_V2_OK")
        print("systems_tested: %d" % record["compensated_grid"]["systems_tested"])
        print("exact_vectors_constructed: %d" % record["compensated_grid"]["exact_vectors_constructed"])
        print("capacity_preserving_vectors: %d" % record["compensated_grid"]["capacity_preserving_vectors"])
        print("pair_guard_preserving_vectors: %d" % record["compensated_grid"]["pair_guard_preserving_vectors"])
        print("best_failure_mode: %s" % record["compensated_grid"]["best_failure_mode"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
