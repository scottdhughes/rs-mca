#!/usr/bin/env python3
"""Run compensated repaired-skeleton split v2 one Sage case at a time."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any


AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_compensated_repaired_skeleton_split_v2.sage")
MERGE_PATH = Path("experimental/scripts/merge_m1_a327_compensated_repaired_skeleton_split_v2_results.py")
DEFAULT_CASE_DIR = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2_cases")
DEFAULT_AGGREGATE = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")
DEFAULT_SAGE = "/usr/local/bin/sage"

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


def load_merge_module():
    spec = importlib.util.spec_from_file_location("m1_a327_comp_split_v2_merge", MERGE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def base_cases() -> list[dict[str, Any]]:
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


def ordered_cases() -> list[dict[str, Any]]:
    keyed = {
        (case["split_family"], case["replacement_bundle_size"], case["selector"]): case
        for case in base_cases()
    }
    ordered: list[dict[str, Any]] = []
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


def parse_case_range(value: str | None, total: int) -> set[int] | None:
    if not value:
        return None
    out: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            left, right = part.split(":", 1)
            start = int(left) if left else 0
            stop = int(right) if right else total
            out.update(range(start, stop))
        else:
            out.add(int(part))
    return {idx for idx in out if 0 <= idx < total}


def case_path(case_dir: Path, case_index: int) -> Path:
    return case_dir / f"case_{case_index:04d}.json"


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def tail_text(value: str, limit: int = 4000) -> str:
    return value[-limit:]


def conservative_prescreen(case: dict[str, Any]) -> dict[str, Any]:
    # This is intentionally non-excluding for the first batched pass. It records
    # the prescreen hook without silently discarding borderline exact systems.
    return {
        "status": "PASS_CONSERVATIVE",
        "reason": "no safe static skip; exact residual solve required",
        "targets": ["capacity", "B27", "B37", "B47", "B57"],
    }


def run_case(case: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    start = time.time()
    command = [
        args.sage,
        str(AUDIT_PATH),
        "--case-index",
        str(case["case_index"]),
        "--json",
    ]
    prescreen = conservative_prescreen(case)
    try:
        proc = subprocess.run(
            command,
            cwd=args.workdir,
            text=True,
            capture_output=True,
            timeout=args.timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "case_index": case["case_index"],
            "case": case,
            "status": "TIMEOUT",
            "failure_mode": "COMP_REPAIRED_SPLIT_TIMEOUT",
            "runtime_seconds": round(time.time() - start, 3),
            "timeout_seconds": args.timeout_seconds,
            "command": command,
            "prescreen": prescreen,
            "stdout_tail": tail_text(exc.stdout or ""),
            "stderr_tail": tail_text(exc.stderr or ""),
        }

    runtime = round(time.time() - start, 3)
    if proc.returncode != 0:
        return {
            "case_index": case["case_index"],
            "case": case,
            "status": "ERROR",
            "failure_mode": "COMP_REPAIRED_SPLIT_PROJECTION_ERROR",
            "runtime_seconds": runtime,
            "returncode": proc.returncode,
            "command": command,
            "prescreen": prescreen,
            "stdout_tail": tail_text(proc.stdout),
            "stderr_tail": tail_text(proc.stderr),
            "error": "Sage case subprocess returned nonzero",
        }

    try:
        record = json.loads(proc.stdout)
        results = record["compensated_grid"]["results"]
        if len(results) != 1:
            raise ValueError(f"expected one case result, found {len(results)}")
        result = results[0]
    except Exception as exc:
        return {
            "case_index": case["case_index"],
            "case": case,
            "status": "ERROR",
            "failure_mode": "COMP_REPAIRED_SPLIT_PROJECTION_ERROR",
            "runtime_seconds": runtime,
            "command": command,
            "prescreen": prescreen,
            "stdout_tail": tail_text(proc.stdout),
            "stderr_tail": tail_text(proc.stderr),
            "error": f"could not parse Sage JSON: {exc}",
        }

    return {
        "case_index": case["case_index"],
        "case": case,
        "status": "DONE",
        "runtime_seconds": runtime,
        "command": command,
        "prescreen": prescreen,
        "result": result,
        "failure_mode": result["failure_mode"],
        "exact_vector_constructed": bool(result.get("vector_results")),
        "capacity": (result.get("best") or {}).get("capacity_upper_bound"),
        "pair_B_values": (result.get("best") or {}).get("pair_B_values"),
        "collapse_pattern": (result.get("best") or {}).get("degenerate_classes"),
        "distinct_codewords": (result.get("best") or {}).get("distinct_codewords"),
        "exact_max_min": (result.get("best") or {}).get("exact_max_min"),
    }


def pending_cases(args: argparse.Namespace) -> list[dict[str, Any]]:
    cases = ordered_cases()
    allowed = parse_case_range(args.cases, len(cases))
    selected = [case for case in cases if allowed is None or case["case_index"] in allowed]
    pending = []
    for case in selected:
        path = case_path(args.case_dir, case["case_index"])
        if path.exists() and not args.force:
            continue
        pending.append(case)
    if args.max_cases is not None:
        pending = pending[: args.max_cases]
    return pending


def merge_if_requested(args: argparse.Namespace) -> None:
    if args.no_merge:
        return
    merge_module = load_merge_module()
    merge_module.merge(args.case_dir, args.aggregate)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--sage", default=DEFAULT_SAGE)
    parser.add_argument("--case-dir", type=Path, default=DEFAULT_CASE_DIR)
    parser.add_argument("--aggregate", type=Path, default=DEFAULT_AGGREGATE)
    parser.add_argument("--cases", help="Comma/range selector such as 0,3,8:12")
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-merge", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cases = pending_cases(args)
    if args.dry_run:
        payload = {
            "pending": len(cases),
            "cases": cases,
            "case_dir": str(args.case_dir),
            "aggregate": str(args.aggregate),
            "timeout_seconds": args.timeout_seconds,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    completed = []
    for case in cases:
        row = run_case(case, args)
        atomic_write_json(case_path(args.case_dir, case["case_index"]), row)
        completed.append(row)
        merge_if_requested(args)
        print(
            "case_%04d %s %s %.3fs"
            % (case["case_index"], row["status"], row.get("failure_mode"), row["runtime_seconds"]),
            flush=True,
        )

    if not cases:
        merge_if_requested(args)

    summary = {
        "status": "PASS",
        "cases_run": len(completed),
        "case_dir": str(args.case_dir),
        "aggregate": str(args.aggregate),
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
