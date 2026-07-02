#!/usr/bin/env python3
"""Verify the M1 a=327 RS-feasible hypergraph tree-rank feedback ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_rs_feasible_hypergraph_tree_rank_feedback.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_rs_feasible_hypergraph_tree_rank_feedback.md")

N = 512
LIST_SIZE = 7
K = 256
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
    "RANK_FEEDBACK_RS_CAP_FAIL",
    "RANK_FEEDBACK_PAIR7_FAIL",
    "RANK_FEEDBACK_TREE_SURPLUS_NEGATIVE",
    "RANK_FEEDBACK_PROXY_FULL_RANK",
    "RANK_FEEDBACK_EXACT_NULLITY_ZERO",
    "RANK_FEEDBACK_FORCED_PAIR_EQUALITY",
    "RANK_FEEDBACK_EXACT_CANDIDATE",
    "RANK_FEEDBACK_TIMEOUT",
    "TREE_PROXY_NULLITY_POSITIVE",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def edge_label(edge: list[int]) -> str:
    left, right = sorted((int(edge[0]), int(edge[1])))
    return f"P{left}{right}"


def verify_coordinate_classes(rows: list[dict[str, Any]]) -> list[int]:
    require(len(rows) == N, "coordinate class count mismatch")
    require(sorted(int(row["position"]) for row in rows) == list(range(N)), "positions incomplete")
    supports = [0] * LIST_SIZE
    for row in rows:
        members = [int(value) for value in row["members"]]
        mask = int(row["mask"])
        require(int(row["fiber"]) == int(row["position"]) % 16, "bad fiber")
        require(int(row["size"]) == len(members), "bad size")
        for witness in members:
            require(mask & (1 << (witness - 1)), "mask/member mismatch")
            supports[witness - 1] += 1
    return supports


def verify_candidate(row: dict[str, Any]) -> None:
    supports = verify_coordinate_classes(row["coordinate_classes"])
    require(row["supports"] == [TARGET_AGREEMENT] * LIST_SIZE, "candidate supports not exact")
    require(row["supports"] == supports, "computed supports mismatch")
    require(set(row["pair_counts"]) == set(PAIR_LABELS), "bad pair labels")
    require(row["max_pair_count"] == max(row["pair_counts"].values()), "bad max pair")
    require(row["max_pair_count"] <= PAIR_CAP, "pair cap violated")
    require(row["pair7_counts"] == [row["pair_counts"][label] for label in PAIR7_PAIR_LABELS], "bad pair7 vector")
    require(min(row["pair7_counts"]) >= PAIR7_LOWER, "pair7 guard violated")
    require(row["best_failure_mode"] in ALLOWED_FAILURES, "bad candidate failure")
    for tree in row["trees"]:
        labels = [edge_label(edge) for edge in tree["edges"]]
        require(tree["edge_labels"] == labels, "bad edge labels")
        require(len(labels) == LIST_SIZE - 1, "bad tree edge count")
        require(tree["tree_variable_count"] == sum(K - row["pair_counts"][label] for label in labels), "bad tree vars")
        non_tree = [label for label in PAIR_LABELS if label not in set(labels)]
        require(tree["non_tree_edge_labels"] == non_tree, "bad non-tree labels")
        require(tree["non_tree_equation_count"] == sum(row["pair_counts"][label] for label in non_tree), "bad non-tree eqs")
        require(tree["matrix_shape"] == [tree["non_tree_equation_count"], tree["tree_variable_count"]], "bad proxy shape")
        require(tree["proxy_rank"] + tree["proxy_nullity"] == tree["tree_variable_count"], "bad proxy rank/nullity")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "aed0ef0", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_tree_obstruction"]
    require(previous["best_tree_nullity"] == 0, "previous obstruction not nullity zero")
    require(previous["failure_mode"] == "TREE_DIVISIBILITY_NULLITY_ZERO", "wrong previous failure")

    search = record["rank_feedback_search"]
    require(search["systems_tested"] == len(search["candidates"]), "bad systems count")
    require(search["rs_feasible_hypergraphs"] == len(search["candidates"]), "bad feasible count")
    require(search["proxy_positive_nullity"] == sum(1 for row in search["candidates"] if row["best_proxy_nullity"] > 0), "bad proxy count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad search failure")
    best = record["best_candidate"]
    if best is not None:
        verify_candidate(best)
        require(search["best_tree_variable_count"] == best["best_tree_variable_count"], "best variable mismatch")
        require(search["best_non_tree_equation_count"] == best["best_non_tree_equation_count"], "best equation mismatch")
        require(search["best_proxy_nullity"] == best["best_proxy_nullity"], "best proxy mismatch")
    for row in search["candidates"]:
        require(row["best_failure_mode"] in ALLOWED_FAILURES, "bad compact candidate failure")

    exact = record.get("exact_tree_audit", {})
    if exact:
        require(exact["best_failure_mode"] in ALLOWED_FAILURES, "bad exact failure")
        if exact.get("rank") is not None:
            require(exact["rank"] + exact["nullity"] == exact["matrix_shape"][1], "bad exact rank/nullity")

    for phrase in [
        "tree-rank feedback",
        "positive tree-divisibility nullity",
        "proxy rank",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "proxy_positive_nullity": search["proxy_positive_nullity"],
        "best_proxy_nullity": search["best_proxy_nullity"],
        "best_exact_nullity": search["best_exact_nullity"],
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
            "PASS: M1 a=327 RS-feasible hypergraph tree-rank feedback "
            f"(systems={result['systems_tested']}, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
