#!/usr/bin/env python3
"""Merge per-case upstream B47 robust exact-scanner results."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


SCAN_PATH = Path("experimental/scripts/scan_m1_a327_upstream_b47_robust_exact_scanner.py")
DEFAULT_CASE_DIR = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner_cases")
DEFAULT_OUTPUT = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json")
SYSTEMS_PLANNED = 24


def load_scan_module():
    spec = importlib.util.spec_from_file_location("m1_a327_upstream_b47_scan", SCAN_PATH)
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


def normalize_case_file(path: Path) -> dict[str, Any]:
    row = load_json(path)
    status = row.get("status")
    if status == "DONE":
        result = row["result"]
        result["case_index"] = row.get("case_index", result.get("case_index"))
        result["runtime_seconds"] = row.get("runtime_seconds")
        return result
    case = row.get("case", {})
    return {
        **case,
        "case_index": row.get("case_index"),
        "failure_mode": row.get("failure_mode", "UPSTREAM_INCONSISTENT"),
        "runtime_seconds": row.get("runtime_seconds"),
        "timeout_seconds": row.get("timeout_seconds"),
        "error": row.get("error"),
        "probe_results": [],
    }


def failure_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        failure = row["failure_mode"]
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def vector_sort_key(result: dict[str, Any]) -> tuple[Any, ...]:
    probe = result.get("best_probe")
    score = result.get("best_robustness_score")
    pre = result.get("pre_split")
    return (
        result.get("failure_mode") == "UPSTREAM_EXACT_CANDIDATE",
        result.get("split_resilient") is True,
        -10**9 if score is None else score,
        -1 if pre is None else pre.get("capacity_upper_bound", -1),
    )


def build_grid(results: list[dict[str, Any]]) -> dict[str, Any]:
    if not results:
        return {
            "systems_planned": SYSTEMS_PLANNED,
            "systems_tested": 0,
            "timeouts": 0,
            "exact_vectors_constructed": 0,
            "split_probe_vectors": 0,
            "split_resilient_skeletons": 0,
            "candidate_families": [
                "alt_14_57",
                "alt_15_47",
                "alt_17_45",
                "alt_145_7",
                "b47_guard",
                "triple_237_b47_guard",
            ],
            "budgets": [1, 2, 4, 8],
            "split_probe_families": ["split_4_from_157", "split_14_vs_57", "split_1_from_457"],
            "best_pre_split_capacity": None,
            "best_pre_split_pair_B_values": None,
            "best_probe_split_capacity": None,
            "best_probe_split_pair_B_values": None,
            "best_robustness_score": None,
            "best_collapse_pattern": None,
            "best_exact_max_min": None,
            "best_failure_mode": "UPSTREAM_EXACT_SCANNER_PENDING",
            "failure_mode_counts": {},
            "results": [],
        }
    best = sorted(results, key=vector_sort_key, reverse=True)[0] if results else None
    probe_vectors = [probe for result in results for probe in result.get("probe_results", []) if probe.get("pair_B_values") is not None]
    return {
        "systems_planned": SYSTEMS_PLANNED,
        "systems_tested": len(results),
        "timeouts": sum(1 for row in results if row.get("failure_mode") == "UPSTREAM_TIMEOUT"),
        "exact_vectors_constructed": sum(1 for row in results if row.get("pre_split") is not None),
        "split_probe_vectors": len(probe_vectors),
        "split_resilient_skeletons": sum(1 for row in results if row.get("split_resilient") is True),
        "candidate_families": [
            "alt_14_57",
            "alt_15_47",
            "alt_17_45",
            "alt_145_7",
            "b47_guard",
            "triple_237_b47_guard",
        ],
        "budgets": [1, 2, 4, 8],
        "split_probe_families": ["split_4_from_157", "split_14_vs_57", "split_1_from_457"],
        "best_pre_split_capacity": None if best is None or best.get("pre_split") is None else best["pre_split"].get("capacity_upper_bound"),
        "best_pre_split_pair_B_values": None if best is None or best.get("pre_split") is None else best["pre_split"].get("pair_B_values"),
        "best_probe_split_capacity": None if best is None or best.get("best_probe") is None else best["best_probe"].get("capacity_upper_bound"),
        "best_probe_split_pair_B_values": None if best is None or best.get("best_probe") is None else best["best_probe"].get("pair_B_values"),
        "best_robustness_score": None if best is None else best.get("best_robustness_score"),
        "best_collapse_pattern": None if best is None or best.get("best_probe") is None else best["best_probe"].get("degenerate_classes"),
        "best_exact_max_min": None if best is None or best.get("best_probe") is None else best["best_probe"].get("exact_max_min"),
        "best_failure_mode": None if best is None else best.get("failure_mode"),
        "failure_mode_counts": failure_counts(results),
        "results": results,
    }


def merge(case_dir: Path, output: Path) -> dict[str, Any]:
    scan = load_scan_module()
    files = sorted(case_dir.glob("case_*.json"))
    results = [normalize_case_file(path) for path in files]
    results = sorted(results, key=lambda row: int(row.get("case_index", 10**9)))
    record = scan.build_record(exact_scanner=build_grid(results))
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
        "systems_tested": record["exact_scanner"]["systems_tested"],
        "exact_vectors_constructed": record["exact_scanner"]["exact_vectors_constructed"],
        "split_probe_vectors": record["exact_scanner"]["split_probe_vectors"],
        "best_failure_mode": record["exact_scanner"]["best_failure_mode"],
        "proof_status": record["proof_status"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("PASS: merged %d upstream B47 exact-scanner cases" % record["exact_scanner"]["systems_tested"])


if __name__ == "__main__":
    main()
