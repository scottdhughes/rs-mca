#!/usr/bin/env python3
"""Verify the M1 a=327 RS-feasible selected-class hypergraph ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_rs_feasible_valueclass_hypergraph_pre_solver as scanner


DATA_PATH = Path("experimental/data/m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.md")
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
    "RS_HYPERGRAPH_PAIR_CAP_FAIL",
    "RS_HYPERGRAPH_SUPPORT_FAIL",
    "RS_HYPERGRAPH_PAIR7_GUARD_FAIL",
    "RS_HYPERGRAPH_SPLIT_NOT_ROBUST",
    "RS_HYPERGRAPH_FEASIBLE",
    "RS_HYPERGRAPH_LIFT_TARGET",
    "RS_HYPERGRAPH_SOLVER_UNAVAILABLE",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_state(row: dict[str, Any]) -> None:
    supports = row["support_counts"]
    pair_counts = row["pair_counts"]
    pair7_counts = row["pair7_counts"]
    pair_b_values = row["pair_B_values"]
    require(len(supports) == scanner.LIST_SIZE, "bad support vector length")
    require(len(pair_counts) == len(scanner.PAIR_LABELS), "bad pair count length")
    require(len(pair_b_values) == len(scanner.PAIR7_LABELS), "bad pair B length")
    require(max(pair_counts.values()) == row["max_pair_count"], "bad max pair count")
    require(pair_counts[row["max_pair_label"]] == row["max_pair_count"], "bad max pair label")
    for idx, margin in enumerate(row["support_margins"]):
        require(margin == supports[idx] - scanner.TARGET_AGREEMENT, "bad support margin")
    for label, value in pair_counts.items():
        require(row["pair_cap_margins"][label] == row["pair_cap"] - value, f"bad pair cap margin {label}")
    for label, value in pair7_counts.items():
        require(row["pair7_margins"][label] == value - scanner.PAIR7_LOWER, f"bad pair7 margin {label}")
    expected_pair_b = [scanner.N + pair7_counts[label] for label in scanner.PAIR7_LABELS]
    require(pair_b_values == expected_pair_b, "bad pair B values")
    expected_score = min(
        row["support_margins"]
        + list(row["pair_cap_margins"].values())
        + list(row["pair7_margins"].values())
    )
    require(row["robustness_score"] == expected_score, "bad robustness score")
    require(row["rs_pair_cap_pass"] == (row["max_pair_count"] <= row["pair_cap"]), "bad pair cap flag")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == scanner.TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "e4e966a", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    legacy = record["legacy_e4e966a_pair_cap_audit"]
    require(legacy["failure_mode"] == "RS_HYPERGRAPH_PAIR_CAP_FAIL", "legacy should fail pair cap")
    require(legacy["rs_pair_cap_pass"] is False, "legacy pair cap unexpectedly passed")
    require(legacy["max_pair_count"] > scanner.PAIR_CAP, "legacy max pair should exceed cap")
    require(legacy["violating_pairs"], "legacy should list violating pairs")

    feasibility = record["rs_feasibility"]
    require(feasibility["coordinate_count"] == scanner.N, "wrong coordinate count")
    require(feasibility["support_target"] == scanner.TARGET_AGREEMENT, "wrong support target")
    require(feasibility["pair_cap"] == scanner.PAIR_CAP, "wrong pair cap")
    require(feasibility["pair7_lower"] == scanner.PAIR7_LOWER, "wrong pair7 lower")

    search = record["search_result"]
    require(search["systems_tested"] == len(search["profiles"]), "profile count mismatch")
    require(search["systems_tested"] <= len(scanner.PROFILE_SPECS), "too many systems")
    require(search["rs_feasible_hypergraphs"] == search["split_resilient_hypergraphs"], "unexpected split count mismatch")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure mode")

    for profile in search["profiles"]:
        require(profile["failure_mode"] in ALLOWED_FAILURES, "bad profile failure mode")
        if "pre_split" not in profile:
            continue
        verify_state(profile["pre_split"])
        for probe in profile["split_probes"].values():
            verify_state(probe)
        best_score = min(
            [profile["pre_split"]["robustness_score"]]
            + [probe["robustness_score"] for probe in profile["split_probes"].values()]
        )
        require(profile["best_robustness_score"] == best_score, "bad profile best score")
        require(profile["split_resilient"] == (best_score >= 0), "bad split flag")
        require(profile["rs_feasible"] == profile["pre_split"]["rs_pair_cap_pass"], "bad RS feasible flag")

    if search["rs_feasible_hypergraphs"]:
        require("CANDIDATE" in record["proof_status"], "candidate status expected")

    for phrase in [
        "Pairwise co-occurrence cap lemma",
        "selected received class",
        "not an exact GF(17^32) lift",
        "not an MCA row",
        "RS_HYPERGRAPH_PAIR_CAP_FAIL",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "rs_feasible_hypergraphs": search["rs_feasible_hypergraphs"],
        "best_robustness_score": search["best_robustness_score"],
        "best_max_pair_count": search["best_max_pair_count"],
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
            "PASS: M1 a=327 RS-feasible selected-class hypergraph pre-solver "
            f"({result['systems_tested']} systems, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
