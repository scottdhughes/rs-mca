#!/usr/bin/env python3
"""Long CP-SAT front for unresolved M1 a=327 quotient-subgroup schedules."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "59b268b"
PREVIOUS_DATA = Path("experimental/data/m1_a327_quotient_subgroup_rank_aware_schedule_generator.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_long_cpsat_front.json")
PRIMAL_SCAN = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_primal_kernel_search.py")

S_VALUES = [8, 16, 32]
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the bounded long CP-SAT front",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def load_primal_scan() -> Any:
    spec = importlib.util.spec_from_file_location("quotient_primal_scan", PRIMAL_SCAN)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {PRIMAL_SCAN}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_record(time_limit: float, max_active_partitions: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    primal = load_primal_scan()
    screens = [primal.solve_count_model(s, time_limit, max_active_partitions) for s in S_VALUES]
    feasible = [screen for screen in screens if screen["feasible"]]
    best = None
    for screen in screens:
        pair7 = min(screen["pair7_counts"]) if screen.get("pair7_counts") else -1
        pair_equal = screen["max_pair_equal_h_count"] if screen.get("max_pair_equal_h_count") is not None else 10**9
        key = (not screen["feasible"], -pair7, pair_equal, screen["s"])
        if best is None or key < best[0]:
            best = (key, screen)
    best_screen = None if best is None else best[1]
    proof_status = (
        "CANDIDATE / LONG_CPSAT_QUOTIENT_CP_FEASIBLE / PARTIAL / EXPERIMENTAL"
        if feasible
        else "PARTIAL / LONG_CPSAT_UNRESOLVED / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_quotient_subgroup_rank_aware_schedule_generator": {
            "proof_status": previous["proof_status"],
            "schedules_tested": previous["rank_aware_schedule_generator"]["schedules_tested"],
            "cp_feasible_schedules": previous["rank_aware_schedule_generator"]["cp_feasible_schedules"],
            "proxy_positive_schedules": previous["rank_aware_schedule_generator"]["proxy_positive_schedules"],
            "best_proxy_rank": previous["rank_aware_schedule_generator"]["best_proxy_rank"],
            "best_proxy_nullity": previous["rank_aware_schedule_generator"]["best_proxy_nullity"],
            "failure_mode": previous["rank_aware_schedule_generator"]["best_failure_mode"],
        },
        "long_cpsat_front": {
            "s_values": S_VALUES,
            "time_limit_seconds": time_limit,
            "max_active_partitions": max_active_partitions,
            "screens_tested": len(screens),
            "cp_feasible_screens": len(feasible),
            "best_s": None if best_screen is None else best_screen["s"],
            "best_pair7_counts": None if best_screen is None else best_screen["pair7_counts"],
            "best_max_pair_equal_h_count": None if best_screen is None else best_screen["max_pair_equal_h_count"],
            "best_active_partition_count": None if best_screen is None else best_screen["active_partition_count"],
            "best_failure_mode": "LONG_CPSAT_QUOTIENT_CP_FEASIBLE" if feasible else "LONG_CPSAT_UNRESOLVED",
            "failure_counts": dict(Counter(screen["best_failure_mode"] for screen in screens)),
        },
        "screens": screens,
        "best_screen": best_screen,
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": REQUIRED_NONCLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--time-limit", type=float, default=120.0)
    parser.add_argument("--max-active-partitions", type=int, default=120)
    args = parser.parse_args()
    record = build_record(args.time_limit, args.max_active_partitions)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps({"proof_status": record["proof_status"], **record["long_cpsat_front"]}, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_LONG_CPSAT_FRONT_READY")


if __name__ == "__main__":
    main()
