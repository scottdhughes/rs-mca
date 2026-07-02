#!/usr/bin/env python3
"""Verify the M1 a=327 selected-class quotient-nullspace lift ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_selected_class_quotient_nullspace_lift.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_selected_class_quotient_nullspace_lift.md")

N = 512
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
QUOTIENT_VARIABLES = (LIST_SIZE - 1) * K
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]
PAIR_INDICES = [(i, j) for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)]
PAIR_LABELS = [f"P{i + 1}{j + 1}" for i, j in PAIR_INDICES]
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    None,
    "QUOTIENT_SYSTEM_TIMEOUT",
    "QUOTIENT_SYSTEM_FULL_RANK",
    "QUOTIENT_NULLITY_ZERO",
    "QUOTIENT_LIFT_FORCED_PAIR_EQUALITY",
    "QUOTIENT_LIFT_DEGENERATE",
    "QUOTIENT_LIFT_DISTINCT_BUT_SUPPORT_LOSS",
    "QUOTIENT_LIFT_EXACT_CANDIDATE",
    "QUOTIENT_RANK_ONLY",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def computed_supports(rows: list[dict[str, Any]]) -> list[int]:
    supports = [0] * LIST_SIZE
    for row in rows:
        for witness in row["members"]:
            supports[int(witness) - 1] += 1
    return supports


def computed_pair_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = {label: 0 for label in PAIR_LABELS}
    for row in rows:
        members = {int(value) - 1 for value in row["members"]}
        for label, (left, right) in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if left in members and right in members:
                counts[label] += 1
    return counts


def verify_coordinate_classes(rows: list[dict[str, Any]]) -> None:
    require(len(rows) == N, "coordinate class count mismatch")
    require(sorted(int(row["position"]) for row in rows) == list(range(N)), "positions not complete")
    for row in rows:
        members = [int(value) for value in row["members"]]
        mask = int(row["mask"])
        require(int(row["fiber"]) == int(row["position"]) % 16, "bad fiber")
        require(int(row["size"]) == len(members), "bad size")
        for witness in members:
            require(mask & (1 << (witness - 1)), "member missing from mask")


def verify_anchored_classes(rows: list[dict[str, Any]], coordinate_rows: list[dict[str, Any]]) -> None:
    require(len(rows) == N, "anchored class count mismatch")
    by_position = {int(row["position"]): row for row in coordinate_rows}
    for row in rows:
        position = int(row["position"])
        source = by_position[position]
        members = [int(value) for value in source["members"]]
        require(row["members"] == members, "anchored members mismatch")
        require(int(row["anchor"]) == min(members), "anchor is not canonical")
        require(int(row["equation_count"]) == len(members) - 1, "bad anchored equation count")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "9fcdb02", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    thin = record["thin_selected_hypergraph"]
    rows = thin["coordinate_classes"]
    anchored = thin["anchored_classes"]
    verify_coordinate_classes(rows)
    verify_anchored_classes(anchored, rows)
    supports = computed_supports(rows)
    pairs = computed_pair_counts(rows)
    require(thin["supports"] == [TARGET_AGREEMENT] * LIST_SIZE, "bad supports")
    require(thin["supports"] == supports, "computed supports mismatch")
    require(thin["selected_incidences"] == LIST_SIZE * TARGET_AGREEMENT, "bad incidence count")
    require(sum(int(row["size"]) for row in rows) == thin["selected_incidences"], "computed incidence mismatch")
    require(thin["pair_counts"] == pairs, "computed pair counts mismatch")
    require(thin["max_pair_count"] == max(pairs.values()), "bad max pair")
    require(thin["max_pair_count"] <= PAIR_CAP, "pair cap violated")
    require(thin["pair7_counts"] == [pairs[label] for label in PAIR7_PAIR_LABELS], "bad pair7 vector")
    require(min(thin["pair7_counts"]) >= PAIR7_LOWER, "pair7 guard violated")
    require(thin["pair_B_values"] == [N + value for value in thin["pair7_counts"]], "bad pair B values")

    quotient = record["quotient_system"]
    require(quotient["variables"] == QUOTIENT_VARIABLES, "bad quotient variable count")
    require(quotient["equations"] == thin["selected_incidences"] - N, "bad quotient equation count")
    require(quotient["matrix_shape"] == [quotient["equations"], QUOTIENT_VARIABLES], "bad quotient shape")
    require(quotient["best_failure_mode"] in ALLOWED_FAILURES, "bad quotient failure")
    if quotient["rank"] is not None:
        require(quotient["nullity"] is not None, "nullity missing")
        require(quotient["rank"] + quotient["nullity"] == quotient["variables"], "bad rank/nullity")

    projection = record["pair_projection_test"]
    require(projection["pairs_tested"] == 21, "wrong pair test count")
    require(len(projection["forced_equal_pairs"]) <= 21, "too many forced pairs")
    if projection["projection_results"]:
        require(len(projection["projection_results"]) == 21, "projection result count mismatch")
        forced = [row["pair"] for row in projection["projection_results"] if row["forced_equal"]]
        require(projection["forced_equal_pairs"] == forced, "forced pair list mismatch")

    candidate = record["exact_candidate"]
    if candidate["constructed"]:
        require(candidate["agreement_vector"] is not None, "candidate missing agreement vector")
        require(len(candidate["agreement_vector"]) == LIST_SIZE, "bad agreement vector")
        require(candidate["seven_distinct"] is True, "constructed candidate is not seven distinct")

    for phrase in [
        "quotient system",
        "D_i = P_i - P_1",
        "pair-projection",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "matrix_shape": quotient["matrix_shape"],
        "rank": quotient["rank"],
        "nullity": quotient["nullity"],
        "forced_equal_pairs": projection["forced_equal_pairs"],
        "candidate_constructed": candidate["constructed"],
        "best_failure_mode": quotient["best_failure_mode"],
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
            "PASS: M1 a=327 selected-class quotient-nullspace lift "
            f"(status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
