#!/usr/bin/env python3
"""Run upstream B47 robust exact scanner one Sage case at a time."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any


AUDIT_PATH = Path("experimental/scripts/audit_m1_a327_upstream_b47_robust_exact_scanner.sage")
MERGE_PATH = Path("experimental/scripts/merge_m1_a327_upstream_b47_robust_exact_scanner_results.py")
DEFAULT_CASE_DIR = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner_cases")
DEFAULT_AGGREGATE = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json")
DEFAULT_SAGE = "/usr/local/bin/sage"

FAMILIES = [
    "alt_14_57",
    "alt_15_47",
    "alt_17_45",
    "alt_145_7",
    "b47_guard",
    "triple_237_b47_guard",
]
BUDGETS = [1, 2, 4, 8]


def load_merge_module():
    spec = importlib.util.spec_from_file_location("m1_a327_upstream_b47_merge", MERGE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def cases() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    idx = 0
    for family in FAMILIES:
        for budget in BUDGETS:
            out.append({"case_index": idx, "candidate_family": family, "budget": int(budget)})
            idx += 1
    return out


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


def run_case(case: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    start = time.time()
    command = [
        args.sage,
        str(AUDIT_PATH),
        "--case-index",
        str(case["case_index"]),
        "--json",
    ]
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
            "failure_mode": "UPSTREAM_TIMEOUT",
            "runtime_seconds": round(time.time() - start, 3),
            "timeout_seconds": args.timeout_seconds,
            "command": command,
            "stdout_tail": tail_text(exc.stdout or ""),
            "stderr_tail": tail_text(exc.stderr or ""),
        }

    runtime = round(time.time() - start, 3)
    if proc.returncode != 0:
        return {
            "case_index": case["case_index"],
            "case": case,
            "status": "ERROR",
            "failure_mode": "UPSTREAM_INCONSISTENT",
            "runtime_seconds": runtime,
            "returncode": proc.returncode,
            "command": command,
            "stdout_tail": tail_text(proc.stdout),
            "stderr_tail": tail_text(proc.stderr),
            "error": "Sage case subprocess returned nonzero",
        }

    try:
        record = json.loads(proc.stdout)
        results = record["exact_scanner"]["results"]
        if len(results) != 1:
            raise ValueError(f"expected one case result, found {len(results)}")
        result = results[0]
    except Exception as exc:
        return {
            "case_index": case["case_index"],
            "case": case,
            "status": "ERROR",
            "failure_mode": "UPSTREAM_INCONSISTENT",
            "runtime_seconds": runtime,
            "command": command,
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
        "result": result,
        "failure_mode": result["failure_mode"],
        "pre_split_capacity": (result.get("pre_split") or {}).get("capacity_upper_bound"),
        "best_probe_capacity": (result.get("best_probe") or {}).get("capacity_upper_bound"),
        "best_probe_pair_B_values": (result.get("best_probe") or {}).get("pair_B_values"),
        "best_robustness_score": result.get("best_robustness_score"),
    }


def pending_cases(args: argparse.Namespace) -> list[dict[str, Any]]:
    all_cases = cases()
    allowed = parse_case_range(args.cases, len(all_cases))
    selected = [case for case in all_cases if allowed is None or case["case_index"] in allowed]
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

    selected = pending_cases(args)
    if args.dry_run:
        print(json.dumps({
            "pending": len(selected),
            "cases": selected,
            "case_dir": str(args.case_dir),
            "aggregate": str(args.aggregate),
            "timeout_seconds": args.timeout_seconds,
        }, indent=2, sort_keys=True))
        return

    completed = []
    for case in selected:
        row = run_case(case, args)
        atomic_write_json(case_path(args.case_dir, case["case_index"]), row)
        completed.append(row)
        print(
            f"case_{case['case_index']:04d} {row['status']} {row['failure_mode']} "
            f"{row['runtime_seconds']:.3f}s",
            flush=True,
        )
        merge_if_requested(args)

    if args.json:
        print(json.dumps({"completed": completed, "count": len(completed)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
