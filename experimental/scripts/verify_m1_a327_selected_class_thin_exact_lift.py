#!/usr/bin/env python3
"""Verify the M1 a=327 selected-class thin exact-lift ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_selected_class_thin_exact_lift as scanner


DATA_PATH = Path("experimental/data/m1_a327_selected_class_thin_exact_lift.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_selected_class_thin_exact_lift.md")
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_THIN_FAILURES = {
    "THIN_SUPPORT_FAIL",
    "THIN_PAIR7_GUARD_FAIL",
    "THIN_PAIR_CAP_FAIL",
    "THIN_SPLIT_ROBUSTNESS_LOSS",
    "THIN_LIFT_TARGET",
}
ALLOWED_LIFT_FAILURES = {
    None,
    "SELECTED_LIFT_INCONSISTENT",
    "SELECTED_LIFT_LOW_NULLITY",
    "SELECTED_LIFT_DEGENERATE",
    "SELECTED_LIFT_SUPPORT_LOSS",
    "SELECTED_LIFT_PAIR_CAP_COLLAPSE",
    "SELECTED_LIFT_LOW_AGREEMENT",
    "SELECTED_LIFT_EXACT_CANDIDATE",
    "SELECTED_LIFT_TIMEOUT",
    "SELECTED_LIFT_RANK_ONLY",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_candidate(row: dict[str, Any]) -> None:
    if row["failure_mode"] != "THIN_LIFT_TARGET":
        return
    require(row["supports"] == [scanner.TARGET_AGREEMENT] * scanner.LIST_SIZE, "thin support not exact")
    require(row["selected_incidence_count"] == scanner.LIST_SIZE * scanner.TARGET_AGREEMENT, "bad incidence count")
    require(row["coordinate_count"] == scanner.N, "bad coordinate count")
    require(row["max_pair_count"] <= scanner.PAIR_CAP, "pair cap violated")
    require(min(row["pair7_counts"].values()) >= scanner.PAIR7_LOWER, "pair7 guard violated")
    expected_pair_b = [scanner.N + row["pair7_counts"][label] for label in scanner.PAIR7_LABELS]
    require(row["pair_B_values"] == expected_pair_b, "bad pair B vector")
    require(row["support_exact"] is True, "bad support flag")
    require(row["pair_cap_pass"] is True, "bad pair cap flag")
    require(row["pair7_guard_pass"] is True, "bad pair7 flag")
    if "coordinate_classes" in row:
        verify_coordinate_classes(row["coordinate_classes"], row["supports"], row["selected_incidence_count"])


def verify_coordinate_classes(rows: list[dict[str, Any]], supports: list[int], selected_incidence_count: int) -> None:
    require(len(rows) == scanner.N, "coordinate class count mismatch")
    require(sorted(row["position"] for row in rows) == list(range(scanner.N)), "positions not complete")
    computed_supports = [0] * scanner.LIST_SIZE
    incidence_count = 0
    for row in rows:
        mask = int(row["mask"])
        require(row["fiber"] == row["position"] % scanner.FIBER_COUNT, "bad fiber id")
        require(row["members"] == scanner.mask_members(mask), "bad members")
        require(row["size"] == len(row["members"]), "bad size")
        incidence_count += row["size"]
        for witness in range(scanner.LIST_SIZE):
            computed_supports[witness] += scanner.contains(mask, witness)
    require(computed_supports == supports, "coordinate supports mismatch")
    require(incidence_count == selected_incidence_count, "coordinate incidence mismatch")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == scanner.TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "2e134d7", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    source = record["source_hypergraph"]
    require(source["supports"] == [351] * scanner.LIST_SIZE, "unexpected source supports")
    require(source["selected_class_size_counts"] == {"4": 103, "5": 409}, "unexpected source sizes")

    thin = record["thin_hypergraph"]
    require(thin["candidates_constructed"] == len(thin["candidates"]), "bad candidate count")
    require(thin["lift_targets"] <= thin["candidates_constructed"], "bad target count")
    require(thin["best_failure_mode"] in ALLOWED_THIN_FAILURES, "bad thin failure")
    require(thin["best_selected_incidence_count"] == scanner.LIST_SIZE * scanner.TARGET_AGREEMENT, "bad best incidence")
    require(thin["best_supports"] == [scanner.TARGET_AGREEMENT] * scanner.LIST_SIZE, "bad best supports")
    require(thin["best_max_pair_count"] <= scanner.PAIR_CAP, "bad best max pair")
    require(min(thin["best_pair7_counts"]) >= scanner.PAIR7_LOWER, "bad best pair7")
    require(len(thin["best_coordinate_classes"]) == scanner.N, "missing best coordinate classes")
    verify_coordinate_classes(thin["best_coordinate_classes"], thin["best_supports"], thin["best_selected_incidence_count"])

    for candidate in thin["candidates"]:
        require(candidate["failure_mode"] in ALLOWED_THIN_FAILURES, "bad candidate failure")
        verify_candidate(candidate)

    exact = record["exact_lift"]
    require(exact["best_failure_mode"] in ALLOWED_LIFT_FAILURES, "bad exact failure")
    if exact["matrix_shape"] is not None:
        require(exact["matrix_shape"][1] == 7 * scanner.K + scanner.N, "wrong variable count")
        require(exact["rank"] is not None and exact["nullity"] is not None, "rank/nullity missing")
        require(exact["rank"] + exact["nullity"] == exact["matrix_shape"][1], "bad rank/nullity")

    for phrase in [
        "explicit received-word variables",
        "supports exactly 327",
        "selected incidences",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "lift_targets": thin["lift_targets"],
        "best_strategy": thin["best_strategy"],
        "best_max_pair_count": thin["best_max_pair_count"],
        "best_pair7_counts": thin["best_pair7_counts"],
        "exact_lift_failure": exact["best_failure_mode"],
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
            "PASS: M1 a=327 selected-class thin exact-lift "
            f"({result['lift_targets']} lift targets, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
