#!/usr/bin/env python3
"""Verify the M1 a=327 bounded-cycle carrier hypergraph ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_bounded_cycle_carrier_hypergraph_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_bounded_cycle_carrier_hypergraph_search.md")

N = 512
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
K = 256
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
    None,
    "BOUNDED_CYCLE_COUNT_INFEASIBLE",
    "BOUNDED_CYCLE_PAIR_CAP_FAIL",
    "BOUNDED_CYCLE_EDGE_CAP_FAIL",
    "BOUNDED_CYCLE_GUARD_FAIL",
    "BOUNDED_CYCLE_EXACT_NULLITY_ZERO",
    "BOUNDED_CYCLE_FORCED_PAIR_EQUALITY",
    "BOUNDED_CYCLE_EXACT_CANDIDATE",
    "BOUNDED_CYCLE_EXACT_TARGET",
    "BOUNDED_CYCLE_EXACT_NOT_RUN",
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


def connected(edges: list[list[int]]) -> bool:
    adjacency = {node: [] for node in range(1, LIST_SIZE + 1)}
    for left, right in edges:
        adjacency[int(left)].append(int(right))
        adjacency[int(right)].append(int(left))
    seen = {1}
    stack = [1]
    while stack:
        node = stack.pop()
        for neighbor in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen == set(range(1, LIST_SIZE + 1))


def contains(mask: int, witness: int) -> bool:
    return bool(mask & (1 << (witness - 1)))


def verify_counts_from_coordinates(search: dict[str, Any]) -> None:
    coordinates = search["coordinate_classes"]
    if coordinates is None:
        return
    require(len(coordinates) == N, "coordinate class count is not 512")
    supports = [0] * LIST_SIZE
    pair_counts = {label: 0 for label in PAIR_LABELS}
    edge_loads = {label: 0 for label in [edge_label(edge) for edge in search["best_graph_edges"]]}
    for row in coordinates:
        position = int(row["position"])
        require(0 <= position < N, "bad coordinate position")
        mask = int(row["mask"])
        require(set(row["members"]) == {idx for idx in range(1, LIST_SIZE + 1) if contains(mask, idx)}, "bad mask members")
        for witness in range(1, LIST_SIZE + 1):
            if contains(mask, witness):
                supports[witness - 1] += 1
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if contains(mask, pair[0]) and contains(mask, pair[1]):
                pair_counts[label] += 1
        for label in row["edge_labels"]:
            require(label in edge_loads, "coordinate uses non-carrier edge")
            edge_loads[label] += 1
    require(supports == search["best_supports"], "support vector mismatch")
    require(pair_counts == search["best_pair_counts"], "pair count mismatch")
    require(edge_loads == search["best_edge_loads"], "edge load mismatch")


def verify_design(row: dict[str, Any]) -> None:
    require(row["failure_mode"] in ALLOWED_FAILURES, "bad design failure label")
    require(row["edge_count"] in {7, 8, 9}, "bad carrier edge count")
    require(row["cycle_rank"] == row["edge_count"] - (LIST_SIZE - 1), "bad cycle rank")
    require([edge_label(edge) for edge in row["edges"]] == row["edge_labels"], "bad edge labels")
    require(connected(row["edges"]), "carrier graph disconnected")
    if row.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
        return
    require(row["support_guard"] is True, "support guard failed")
    require(row["pair_cap_guard"] is True, "pair cap guard failed")
    require(row["pair7_guard"] is True, "pair7 guard failed")
    require(row["edge_cap_guard"] is True, "edge cap guard failed")
    require(min(row["support_vector"]) >= TARGET_AGREEMENT, "support too low")
    require(max(row["pair_count_matrix"].values()) <= PAIR_CAP, "pair cap violated")
    require(max(row["edge_loads"].values()) <= PAIR_CAP, "edge cap violated")
    require(min(row["pair7_counts"]) >= PAIR7_LOWER, "pair7 too low")
    require(sum(count["count"] for count in row["connected_class_edge_counts"]) == N, "bad pattern count")
    require(row["quotient_variable_budget"] == sum(K - value for value in row["edge_loads"].values()), "bad quotient budget")
    require(row["cycle_constraint_count"] == row["cycle_rank"] * K, "bad cycle row count")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "2b54b7c", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    obstruction = record["tree_obstruction"]
    require(obstruction["selected_incidence_lower"] == LIST_SIZE * TARGET_AGREEMENT, "bad selected lower")
    require(obstruction["tree_edge_incidence_lower"] == LIST_SIZE * TARGET_AGREEMENT - N, "bad tree edge lower")
    require(obstruction["tree_edge_capacity"] == (LIST_SIZE - 1) * PAIR_CAP, "bad tree edge capacity")
    require(obstruction["minimum_carrier_edges_by_count"] == 7, "bad minimum carrier count")

    search = record["bounded_cycle_search"]
    require(search["carrier_graphs_tested"] == len(search["all_designs"]), "bad design count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad search failure label")
    for row in search["all_designs"]:
        verify_design(row)
    verify_counts_from_coordinates(search)

    exact = record["exact_edge_lift"]
    require(exact["best_failure_mode"] in ALLOWED_FAILURES, "bad exact failure label")
    if exact["rank"] is not None:
        require(exact["nullity"] is not None, "missing nullity")
        require(exact["edge_variable_count"] is not None, "missing variable count")
        require(exact["rank"] + exact["nullity"] == exact["edge_variable_count"], "bad rank/nullity")
    if exact["seven_distinct"]:
        require(exact["agreement_vector"] is not None, "missing agreement vector")
        require(min(exact["agreement_vector"]) >= TARGET_AGREEMENT, "candidate agreement too low")

    for phrase in [
        "bounded-cycle",
        "edge-load",
        "cycle constraints",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "carrier_graphs_tested": search["carrier_graphs_tested"],
        "feasible_hypergraphs": search["feasible_hypergraphs"],
        "best_graph_id": search["best_graph_id"],
        "best_guard_margin": search["best_guard_margin"],
        "exact_rank": exact["rank"],
        "exact_nullity": exact["nullity"],
        "best_failure_mode": exact["best_failure_mode"] or search["best_failure_mode"],
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
            "PASS: M1 a=327 bounded-cycle carrier hypergraph search "
            f"(status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
