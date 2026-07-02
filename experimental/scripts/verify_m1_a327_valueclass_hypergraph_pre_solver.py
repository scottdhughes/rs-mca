#!/usr/bin/env python3
"""Verify the M1 a=327 value-class hypergraph pre-solver ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_valueclass_hypergraph_pre_solver as scanner


DATA_PATH = Path("experimental/data/m1_a327_valueclass_hypergraph_pre_solver.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_valueclass_hypergraph_pre_solver.md")
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "exact GF(17^32) lift",
}
ALLOWED_FAILURES = {
    "HYPERGRAPH_INFEASIBLE",
    "HYPERGRAPH_GUARDS_FAIL",
    "HYPERGRAPH_B47_NOT_ROBUST",
    "HYPERGRAPH_CAPACITY_NOT_ROBUST",
    "HYPERGRAPH_SPLIT_RESILIENT",
    "HYPERGRAPH_LIFT_TARGET",
    "HYPERGRAPH_SOLVER_UNAVAILABLE",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_guard(row: dict[str, Any]) -> None:
    capacity_total = row["capacity_total"]
    pair_values = row["pair_B_values"]
    require(row["capacity_upper_bound"] == capacity_total // scanner.LIST_SIZE, "bad capacity floor")
    require(len(pair_values) == 5, "bad pair vector length")
    require(row["guard_vector"]["capacity"] == row["capacity_upper_bound"], "bad capacity guard")
    for label, value in zip(scanner.PAIR_LABELS, pair_values, strict=True):
        require(row["guard_vector"][label] == value, f"bad guard {label}")
        require(row["guard_margins"][label] == value - scanner.PAIR_TARGET, f"bad margin {label}")
    require(row["guard_margins"]["capacity"] == row["capacity_upper_bound"] - scanner.TARGET_AGREEMENT, "bad capacity margin")
    expected_score = min([row["guard_margins"]["capacity"]] + [row["guard_margins"][label] for label in scanner.PAIR_LABELS])
    require(row["robustness_score"] == expected_score, "bad robustness score")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == scanner.TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "56fd7a9", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    upstream = record["upstream_exact_scanner"]
    require(upstream["systems_tested"] == 24, "wrong upstream exact system count")
    require(upstream["split_resilient_skeletons"] == 0, "upstream should have no resilient skeleton")

    search = record["hypergraph_search"]
    require(search["coordinate_count"] == scanner.N, "wrong coordinate count")
    require(search["fiber_count"] == scanner.FIBER_COUNT, "wrong fiber count")
    require(search["profile_count"] == len(scanner.PROFILE_SPECS), "wrong profile count")
    require(search["systems_tested"] == len(search["profiles"]), "profile result mismatch")
    require(search["systems_tested"] <= len(scanner.PROFILE_SPECS), "too many systems")
    require(search["split_resilient_hypergraphs"] <= search["feasible_hypergraphs"], "bad resilient count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")

    for profile in search["profiles"]:
        require(profile["failure_mode"] in ALLOWED_FAILURES, "bad profile failure")
        if "pre_split" not in profile:
            continue
        verify_guard(profile["pre_split"])
        for probe in profile["split_probes"].values():
            verify_guard(probe)
        best_score = min(
            [profile["pre_split"]["robustness_score"]]
            + [probe["robustness_score"] for probe in profile["split_probes"].values()]
        )
        require(profile["best_robustness_score"] == best_score, "bad profile best score")
        require(profile["split_resilient"] == (profile["best_robustness_score"] >= 0), "bad split-resilient flag")

    if search["systems_tested"] == len(scanner.PROFILE_SPECS):
        if search["split_resilient_hypergraphs"]:
            require("CANDIDATE" in record["proof_status"], "candidate status expected")
        else:
            require("TESTED_NO_SPLIT_RESILIENT" in record["proof_status"], "tested negative status expected")

    for phrase in [
        "value-class hypergraph",
        "not an exact GF(17^32) lift",
        "not an MCA row",
        "split-resilient before exact lifting",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "feasible_hypergraphs": search["feasible_hypergraphs"],
        "split_resilient_hypergraphs": search["split_resilient_hypergraphs"],
        "best_robustness_score": search["best_robustness_score"],
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
        print(
            "PASS: M1 a=327 value-class hypergraph pre-solver "
            f"({result['systems_tested']} systems, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
