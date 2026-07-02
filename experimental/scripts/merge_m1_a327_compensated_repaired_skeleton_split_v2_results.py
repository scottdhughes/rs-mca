#!/usr/bin/env python3
"""Merge per-case compensated repaired-skeleton split v2 results."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


SCAN_PATH = Path("experimental/scripts/scan_m1_a327_compensated_repaired_skeleton_split_v2.py")
DEFAULT_CASE_DIR = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2_cases")
DEFAULT_OUTPUT = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")
SYSTEMS_PLANNED = 45
TIMEOUT_FAILURE = "COMP_REPAIRED_SPLIT_TIMEOUT"
ERROR_FAILURE = "COMP_REPAIRED_SPLIT_PROJECTION_ERROR"


def load_scan_module():
    spec = importlib.util.spec_from_file_location("m1_a327_comp_split_v2_scan", SCAN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def case_sort_key(result: dict[str, Any]) -> tuple[int, str]:
    return int(result.get("case_index", 10**9)), str(result.get("path", ""))


def timeout_case(row: dict[str, Any]) -> dict[str, Any]:
    case = row.get("case", {})
    return {
        **case,
        "case_index": row.get("case_index"),
        "failure_mode": TIMEOUT_FAILURE,
        "runtime_seconds": row.get("runtime_seconds"),
        "timeout_seconds": row.get("timeout_seconds"),
        "vector_results": [],
    }


def error_case(row: dict[str, Any]) -> dict[str, Any]:
    case = row.get("case", {})
    return {
        **case,
        "case_index": row.get("case_index"),
        "failure_mode": ERROR_FAILURE,
        "runtime_seconds": row.get("runtime_seconds"),
        "error": row.get("error"),
        "stderr_tail": row.get("stderr_tail"),
        "vector_results": [],
    }


def normalize_case_file(path: Path) -> dict[str, Any]:
    row = load_json(path)
    row["path"] = str(path)
    status = row.get("status")
    if status == "DONE":
        result = row["result"]
        result["case_index"] = row.get("case_index", result.get("case_index"))
        return result
    if status == "TIMEOUT":
        return timeout_case(row)
    return error_case(row)


def failure_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def vector_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    exact_max = -1 if row.get("exact_max_min") is None else row["exact_max_min"]
    pair_values = row.get("pair_B_values") or [0, 0, 0, 0, 0]
    return (
        row.get("failure_mode") == "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE",
        row.get("pair_guard_preserving") is True,
        row.get("capacity_upper_bound", -1) >= 327,
        row.get("partial_split") is True,
        exact_max,
        min(pair_values[1], pair_values[2], pair_values[3], pair_values[4]),
        row.get("capacity_upper_bound", -1),
        row.get("distinct_codewords") is True,
        -row.get("six_class_dominance", 10**9),
    )


def build_grid(results: list[dict[str, Any]]) -> dict[str, Any]:
    vectors = [row for result in results for row in result.get("vector_results", [])]
    best_pool = vectors or [row.get("best", row) for row in results]
    best = sorted(best_pool, key=vector_sort_key, reverse=True)[0] if best_pool else None
    return {
        "systems_planned": SYSTEMS_PLANNED,
        "systems_tested": len(results),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == TIMEOUT_FAILURE),
        "exact_vectors_constructed": len(vectors),
        "capacity_preserving_vectors": sum(1 for row in vectors if row.get("capacity_preserving") is True),
        "pair_guard_preserving_vectors": sum(1 for row in vectors if row.get("pair_guard_preserving") is True),
        "partial_split_vectors": sum(1 for row in vectors if row.get("partial_split") is True),
        "nondegenerate_vectors": sum(1 for row in vectors if row.get("distinct_codewords") is True),
        "failure_mode_counts": failure_counts(results),
        "vector_failure_mode_counts": failure_counts(vectors) if vectors else {},
        "cache_mode": "SAGE_NATIVE_RESIDUAL_APPEND_BATCHED",
        "best_capacity": None if best is None else best.get("capacity_upper_bound"),
        "best_pair_B_values": None if best is None else best.get("pair_B_values"),
        "best_collapse_pattern": None if best is None else best.get("degenerate_classes"),
        "best_exact_max_min": None if best is None else best.get("exact_max_min"),
        "best_agreement_vector": None if best is None else best.get("exact_agreement_vector"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "results": results,
    }


def merge(case_dir: Path, output: Path) -> dict[str, Any]:
    scan = load_scan_module()
    files = sorted(case_dir.glob("case_*.json"))
    results = [normalize_case_file(path) for path in files]
    results = sorted(results, key=case_sort_key)
    record = scan.build_record(compensated_grid=build_grid(results))
    atomic_write_json(output, scan.jsonable(record))
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-dir", type=Path, default=DEFAULT_CASE_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = merge(args.case_dir, args.output)
    summary = {
        "status": "PASS",
        "systems_tested": record["compensated_grid"]["systems_tested"],
        "exact_vectors_constructed": record["compensated_grid"]["exact_vectors_constructed"],
        "best_failure_mode": record["compensated_grid"]["best_failure_mode"],
        "proof_status": record["proof_status"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(
            "PASS: merged %d compensated split v2 case results"
            % record["compensated_grid"]["systems_tested"]
        )


if __name__ == "__main__":
    main()
