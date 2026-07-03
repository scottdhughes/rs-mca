#!/usr/bin/env python3
"""Verify the M1 a=327 connected-subtree selected-class construction ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_connected_subtree_selected_class_construction.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_connected_subtree_selected_class_construction.md")

N = 512
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "CONNECTED_SUBTREE_COUNT_INFEASIBLE",
    "CONNECTED_SUBTREE_PAIR_CAP_FAIL",
    "CONNECTED_SUBTREE_SUPPORT_FAIL",
    "CONNECTED_SUBTREE_EDGE_DEGREE_FAIL",
    "CONNECTED_SUBTREE_DISTINCTNESS_FAIL",
    "CONNECTED_SUBTREE_EXACT_CANDIDATE",
    "CONNECTED_SUBTREE_GLOBAL_COUNT_OBSTRUCTION",
    "CONNECTED_SUBTREE_EXACT_NOT_RUN",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify_design(row: dict[str, Any]) -> None:
    if row["solver_status"] != "OPTIMAL_OR_FEASIBLE":
        require(row["failure_mode"] in ALLOWED_FAILURES, "bad infeasible design label")
        return
    require(row["support_guard"] is True, "support guard failed")
    require(row["pair_cap_guard"] is True, "pair cap guard failed")
    require(row["pair7_guard"] is True, "pair7 guard failed")
    require(row["edge_degree_guard"] is True, "edge degree guard failed")
    require(min(row["support_vector"]) >= TARGET_AGREEMENT, "support too low")
    require(max(row["pair_count_matrix"].values()) <= PAIR_CAP, "pair cap violated")
    require(row["pair7_counts"] == [row["pair_count_matrix"][label] for label in PAIR7_PAIR_LABELS], "bad pair7")
    require(min(row["pair7_counts"]) >= PAIR7_LOWER, "pair7 too low")
    require(sum(count["count"] for count in row["connected_class_counts"]) == N, "bad coordinate count")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "a3be7b6", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    design = record["connected_subtree_design"]
    require(design["trees_tested"] == len(design["all_designs"]), "bad tree count")
    require(design["best_failure_mode"] in ALLOWED_FAILURES, "bad design failure")
    obstruction = design["counting_obstruction"]
    require(obstruction["support_selected_incidence_lower"] == LIST_SIZE * TARGET_AGREEMENT, "bad incidence lower")
    require(obstruction["tree_edge_incidence_lower"] == LIST_SIZE * TARGET_AGREEMENT - N, "bad edge lower")
    require(obstruction["tree_edge_incidence_upper_from_pair_cap"] == (LIST_SIZE - 1) * PAIR_CAP, "bad edge upper")
    require(obstruction["edge_incidence_deficit"] == (LIST_SIZE * TARGET_AGREEMENT - N) - ((LIST_SIZE - 1) * PAIR_CAP), "bad deficit")
    require(obstruction["obstruction_applies_to_any_7_node_tree"] is True, "missing global count obstruction")
    for row in design["all_designs"]:
        verify_design(row)

    exact = record["exact_construction"]
    require(exact["best_failure_mode"] in ALLOWED_FAILURES or exact["best_failure_mode"] is None, "bad exact label")
    if exact["seven_distinct"]:
        require(exact["agreement_vector"] is not None, "missing agreement vector")
        require(min(exact["agreement_vector"]) >= TARGET_AGREEMENT, "candidate agreement too low")

    for phrase in [
        "connected-subtree",
        "tree-edge incidence",
        "1777",
        "1530",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "trees_tested": design["trees_tested"],
        "feasible_designs": design["feasible_designs"],
        "edge_incidence_lower": obstruction["tree_edge_incidence_lower"],
        "edge_incidence_upper": obstruction["tree_edge_incidence_upper_from_pair_cap"],
        "best_failure_mode": design["best_failure_mode"],
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
            "PASS: M1 a=327 connected-subtree selected-class construction "
            f"(status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
