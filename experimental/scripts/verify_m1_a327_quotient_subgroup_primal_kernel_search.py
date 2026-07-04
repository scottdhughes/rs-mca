#!/usr/bin/env python3
"""Verify the M1 a=327 quotient-subgroup primal-kernel search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_primal_kernel_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_primal_kernel_search.md")

TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "cff22a0", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_collision_budget_rightkernel_codesign"]
    require(previous["basis_profiles_constructed"] == 240, "wrong previous profile count")
    require(previous["rightkernel_collision_budget_profiles"] == 192, "wrong previous rightkernel count")
    require(previous["proxy_ranked_profiles"] == 12, "wrong previous proxy-ranked count")
    require(previous["proxy_positive_profiles"] == 0, "unexpected previous proxy positive")
    require(previous["best_proxy_rank"] == 666, "wrong previous proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous proxy nullity")
    require(previous["failure_mode"] == "RKERNEL_PROXY_FULL_RANK", "wrong previous failure")

    tools = record["tools"]
    require(tools["ortools_available"] is True, "OR-Tools unavailable")
    require(tools["ortools_version"] == "9.15.6755", "wrong OR-Tools version")
    require(tools["cp_sat_smoke"] is True, "CP-SAT smoke failed")

    search = record["quotient_subgroup_primal_kernel_search"]
    require(search["s_values"] == [32, 16, 8, 4], "wrong s values")
    require(search["time_limit_seconds"] == 20.0, "wrong time limit")
    require(search["max_active_partitions"] == 80, "wrong active partition cap")
    require(search["screens_tested"] == 4, "wrong screen count")
    require(search["cp_feasible_screens"] == 1, "wrong feasible count")
    require(search["best_s"] == 4, "wrong best s")
    require(search["best_pair7_counts"] == [252, 252, 252, 252, 252], "wrong pair7 counts")
    require(search["best_max_pair_equal_h_count"] == 252, "wrong max pair equality count")
    require(search["best_active_partition_count"] == 22, "wrong active partition count")
    require(search["best_failure_mode"] == "QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING", "wrong failure")
    require(
        search["failure_counts"] == {
            "QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING": 1,
            "QUOTIENT_CP_UNRESOLVED": 3,
        },
        "wrong failure counts",
    )

    screens = {row["s"]: row for row in record["screens"]}
    for s in [32, 16, 8]:
        require(screens[s]["best_failure_mode"] == "QUOTIENT_CP_UNRESOLVED", f"s={s} should be unresolved")
        require(screens[s]["cp_sat_status"] == "UNKNOWN", f"s={s} wrong status")
        require(screens[s]["feasible"] is False, f"s={s} unexpectedly feasible")

    best = record["best_screen"]
    require(best["s"] == 4, "best screen not s=4")
    require(best["quotient_length"] == 128, "wrong quotient length")
    require(best["quotient_degree_bound"] == 63, "wrong quotient degree bound")
    require(best["cp_sat_status"] == "OPTIMAL", "best screen not optimal")
    require(best["feasible"] is True, "best screen not feasible")
    require(best["support_vector"] == [327] * 7, "wrong support vector")
    require(best["pair7_counts"] == [252, 252, 252, 252, 252], "wrong best pair7")
    require(best["max_pair_equal_h_count"] == 252, "wrong best pair cap")
    require(best["max_pair_equal_quotient_count"] == 63, "wrong quotient pair count")
    require(best["active_partition_count"] == 22, "wrong active partition count")
    require(len(best["active_partitions"]) == 22, "active partitions not fully retained")
    require(best["best_failure_mode"] == "QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING", "wrong best failure")
    require(best["active_partitions"][0]["partition"] == [[1, 2, 3, 4, 5, 6, 7]], "unexpected first partition")
    require(best["active_partitions"][0]["quotient_fibers"] == 19, "unexpected first partition count")

    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING",
        "best s = 4",
        "support vector = [327,327,327,327,327,327,327]",
        "pair7 counts = [252,252,252,252,252]",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "screens_tested": search["screens_tested"],
        "cp_feasible_screens": search["cp_feasible_screens"],
        "best_s": search["best_s"],
        "best_pair7_counts": search["best_pair7_counts"],
        "best_max_pair_equal_h_count": search["best_max_pair_equal_h_count"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 quotient-subgroup primal-kernel search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
