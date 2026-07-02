#!/usr/bin/env python3
"""Verify the M1 a=327 selected-class tree-divisibility lift ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_selected_class_tree_divisibility_lift.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_selected_class_tree_divisibility_lift.md")

N = 512
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]
PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
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
    "TREE_DIVISIBILITY_TIMEOUT",
    "TREE_DIVISIBILITY_NULLITY_ZERO",
    "TREE_DIVISIBILITY_FULL_RANK",
    "TREE_DIVISIBILITY_FORCED_PAIR_EQUALITY",
    "TREE_DIVISIBILITY_DEGENERATE_SAMPLE",
    "TREE_DIVISIBILITY_EXACT_CANDIDATE",
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


def verify_tree(tree: dict[str, Any], pair_counts: dict[str, int]) -> None:
    edges = tree["edges"]
    require(len(edges) == LIST_SIZE - 1, "tree has wrong edge count")
    labels = [edge_label(edge) for edge in edges]
    require(tree["edge_labels"] == labels, "bad tree labels")
    require(len(set(labels)) == LIST_SIZE - 1, "duplicate tree edge")
    vertices = {1}
    changed = True
    while changed:
        changed = False
        for left, right in edges:
            left = int(left)
            right = int(right)
            if left in vertices and right not in vertices:
                vertices.add(right)
                changed = True
            if right in vertices and left not in vertices:
                vertices.add(left)
                changed = True
    require(vertices == set(range(1, LIST_SIZE + 1)), "tree not connected")
    require(tree["total_weight"] == sum(pair_counts[label] for label in labels), "bad tree weight")
    require(tree["tree_variable_count"] == sum(K - pair_counts[label] for label in labels), "bad variable count")
    non_tree = [label for label in PAIR_LABELS if label not in set(labels)]
    require(tree["non_tree_edge_labels"] == non_tree, "bad non-tree labels")
    require(tree["non_tree_equation_count"] == sum(pair_counts[label] for label in non_tree), "bad non-tree equations")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "016f04d", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    thin = record["thin_selected_hypergraph"]
    require(thin["supports"] == [TARGET_AGREEMENT] * LIST_SIZE, "bad supports")
    require(thin["selected_incidences"] == LIST_SIZE * TARGET_AGREEMENT, "bad selected incidence count")
    require(thin["max_pair_count"] <= PAIR_CAP, "pair cap violated")
    require(thin["pair7_counts"] == [thin["pair_counts"][label] for label in PAIR7_PAIR_LABELS], "bad pair7 counts")
    require(set(thin["pair_counts"]) == set(PAIR_LABELS), "bad pair count labels")
    require(set(thin["pair_sets"]) == set(PAIR_LABELS), "bad pair set labels")
    for label in PAIR_LABELS:
        positions = thin["pair_sets"][label]
        require(len(positions) == thin["pair_counts"][label], f"bad pair set size for {label}")
        require(all(0 <= int(pos) < N for pos in positions), f"bad pair position for {label}")

    tree_data = record["tree_divisibility"]
    require(tree_data["trees_tested"], "no trees tested")
    for tree in tree_data["trees_tested"]:
        verify_tree(tree, thin["pair_counts"])
    best_tree = next(tree for tree in tree_data["trees_tested"] if tree["tree_name"] == tree_data["best_tree_name"])
    require(tree_data["best_tree_edges"] == best_tree["edges"], "bad best edges")
    require(tree_data["tree_variable_count"] == best_tree["tree_variable_count"], "bad best variable count")
    require(tree_data["non_tree_equation_count"] == best_tree["non_tree_equation_count"], "bad best equation count")
    require(
        tree_data["matrix_shape"] == [tree_data["non_tree_equation_count"], tree_data["tree_variable_count"]],
        "bad tree matrix shape",
    )
    require(tree_data["best_failure_mode"] in ALLOWED_FAILURES, "bad tree failure mode")
    if tree_data["rank"] is not None:
        require(tree_data["nullity"] is not None, "nullity missing")
        require(tree_data["rank"] + tree_data["nullity"] == tree_data["tree_variable_count"], "bad rank/nullity")

    projection = record["pair_projection_test"]
    require(projection["pairs_tested"] == 21, "bad projection pair count")
    if projection["projection_rank_by_pair"] is not None:
        require(set(projection["projection_rank_by_pair"]) == set(PAIR_LABELS), "bad projection labels")

    candidate = record["exact_candidate"]
    if candidate["constructed"]:
        require(candidate["agreement_vector"] is not None, "candidate missing agreement vector")
        require(len(candidate["agreement_vector"]) == LIST_SIZE, "bad agreement vector")
        require(candidate["seven_distinct"] is True, "constructed candidate is not seven distinct")

    for phrase in [
        "tree-divisibility",
        "Z_ij",
        "maximum-weight spanning tree",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "best_tree_name": tree_data["best_tree_name"],
        "matrix_shape": tree_data["matrix_shape"],
        "rank": tree_data["rank"],
        "nullity": tree_data["nullity"],
        "best_failure_mode": tree_data["best_failure_mode"],
        "candidate_constructed": candidate["constructed"],
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
            "PASS: M1 a=327 selected-class tree-divisibility lift "
            f"(status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
