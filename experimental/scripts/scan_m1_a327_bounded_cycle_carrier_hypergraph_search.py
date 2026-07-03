#!/usr/bin/env python3
"""Search bounded-cycle carrier selected-class designs for M1 a=327.

This is a combinatorial pre-solver.  It looks for selected classes C_h and
carrier edge sets T_h inside small-cycle graphs on seven witnesses.  Exact
GF(17^32) lifting is left to the matching Sage audit.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import deque
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "2b54b7c"
OUTPUT_DATA = Path("experimental/data/m1_a327_bounded_cycle_carrier_hypergraph_search.json")

N = 512
FIBER_COUNT = 16
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
K = 256

PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]

TREE_EDGE_INCIDENCE_LOWER = LIST_SIZE * TARGET_AGREEMENT - N
TREE_EDGE_CAPACITY = (LIST_SIZE - 1) * PAIR_CAP

GRAPH_SPECS = [
    {
        "graph_id": "m7_cycle_12347_tail_56",
        "edges": [[1, 2], [2, 3], [3, 4], [4, 7], [1, 7], [7, 5], [5, 6]],
    },
    {
        "graph_id": "m7_cycle_1475_spine_1236",
        "edges": [[1, 4], [4, 7], [7, 5], [1, 5], [1, 2], [2, 3], [3, 6]],
    },
    {
        "graph_id": "m7_cycle_237_path_1456",
        "edges": [[2, 3], [3, 7], [2, 7], [7, 4], [4, 1], [4, 5], [5, 6]],
    },
    {
        "graph_id": "m8_two_triangles_sharing_7",
        "edges": [[2, 3], [3, 7], [2, 7], [1, 4], [4, 7], [1, 7], [7, 5], [5, 6]],
    },
    {
        "graph_id": "m8_square_1457_triangle_237",
        "edges": [[1, 4], [4, 5], [5, 7], [1, 7], [2, 3], [3, 7], [2, 7], [7, 6]],
    },
    {
        "graph_id": "m8_b47_robust",
        "edges": [[1, 4], [4, 7], [7, 5], [1, 5], [2, 7], [3, 7], [2, 3], [5, 6]],
    },
    {
        "graph_id": "m9_low_cycle_robust",
        "edges": [[1, 2], [2, 3], [3, 7], [7, 4], [4, 5], [5, 6], [1, 7], [2, 7], [3, 4]],
    },
    {
        "graph_id": "m9_dense_7_hub",
        "edges": [[7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [1, 4], [2, 3], [5, 6]],
    },
    {
        "graph_id": "m9_b47_b57_robust",
        "edges": [[4, 7], [5, 7], [2, 7], [3, 7], [1, 7], [1, 4], [4, 5], [2, 3], [5, 6]],
    },
]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def edge_label(edge: tuple[int, int] | list[int]) -> str:
    left, right = sorted((int(edge[0]), int(edge[1])))
    return f"P{left}{right}"


def canonical_edges(edges: list[list[int]]) -> list[list[int]]:
    out = sorted([sorted([int(edge[0]), int(edge[1])]) for edge in edges])
    if len(out) != len({tuple(edge) for edge in out}):
        raise ValueError("duplicate carrier edge")
    return out


def mask_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(LIST_SIZE) if mask & (1 << idx)]


def mask_from_members(members: list[int] | tuple[int, ...]) -> int:
    mask = 0
    for member in members:
        mask |= 1 << (int(member) - 1)
    return mask


def contains(mask: int, witness: int) -> int:
    return int(bool(mask & (1 << (witness - 1))))


def pair_same(mask: int, pair: tuple[int, int]) -> int:
    return contains(mask, pair[0]) * contains(mask, pair[1])


def adjacency(edges: list[list[int]]) -> dict[int, list[int]]:
    out = {node: [] for node in range(1, LIST_SIZE + 1)}
    for left, right in edges:
        out[int(left)].append(int(right))
        out[int(right)].append(int(left))
    return out


def connected_vertices(edges: list[list[int]], vertices: set[int] | None = None) -> bool:
    adj = adjacency(edges)
    target = set(range(1, LIST_SIZE + 1)) if vertices is None else set(vertices)
    if not target:
        return False
    start = min(target)
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor in target and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen == target


def graph_summary(spec: dict[str, Any]) -> dict[str, Any]:
    edges = canonical_edges(spec["edges"])
    if not connected_vertices(edges):
        raise ValueError(f"carrier graph is disconnected: {spec['graph_id']}")
    return {
        "graph_id": spec["graph_id"],
        "edges": edges,
        "edge_labels": [edge_label(edge) for edge in edges],
        "edge_count": len(edges),
        "cycle_rank": len(edges) - (LIST_SIZE - 1),
    }


class DSU:
    def __init__(self, members: list[int]):
        self.parent = {member: member for member in members}

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        self.parent[right_root] = left_root
        return True


def is_tree_on_members(edges: list[list[int]], members: list[int]) -> bool:
    if len(members) <= 1:
        return len(edges) == 0
    if len(edges) != len(members) - 1:
        return False
    dsu = DSU(members)
    for left, right in edges:
        if not dsu.union(int(left), int(right)):
            return False
    roots = {dsu.find(member) for member in members}
    return len(roots) == 1


def spanning_edge_sets_for_mask(mask: int, graph_edges: list[list[int]], max_sets: int = 24) -> list[list[list[int]]]:
    members = mask_members(mask)
    if len(members) == 1:
        return [[]]
    member_set = set(members)
    induced = [edge for edge in graph_edges if int(edge[0]) in member_set and int(edge[1]) in member_set]
    needed = len(members) - 1
    trees = []
    for combo in itertools.combinations(induced, needed):
        tree = canonical_edges([list(edge) for edge in combo])
        if is_tree_on_members(tree, members):
            trees.append(tree)
    trees = sorted(trees, key=lambda row: ([edge_label(edge) for edge in row], row))
    return trees[:max_sets]


def carrier_patterns(graph_edges: list[list[int]]) -> list[dict[str, Any]]:
    patterns = []
    seen = set()
    for size in range(1, LIST_SIZE + 1):
        for combo in itertools.combinations(range(1, LIST_SIZE + 1), size):
            mask = mask_from_members(combo)
            for tree in spanning_edge_sets_for_mask(mask, graph_edges):
                labels = [edge_label(edge) for edge in tree]
                key = (mask, tuple(labels))
                if key in seen:
                    continue
                seen.add(key)
                patterns.append(
                    {
                        "mask": mask,
                        "members": mask_members(mask),
                        "size": size,
                        "edge_labels": labels,
                        "edge_count": len(labels),
                    }
                )
    return patterns


def solve_graph_counts(graph: dict[str, Any]) -> dict[str, Any]:
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover
        out = dict(graph)
        out.update(
            {
                "solver_status": "SCIPY_UNAVAILABLE",
                "solver_error": str(exc),
                "failure_mode": "BOUNDED_CYCLE_COUNT_INFEASIBLE",
            }
        )
        return out

    patterns = carrier_patterns(graph["edges"])
    if not patterns:
        out = dict(graph)
        out.update(
            {
                "pattern_count": 0,
                "solver_status": "NO_PATTERNS",
                "failure_mode": "BOUNDED_CYCLE_COUNT_INFEASIBLE",
            }
        )
        return out

    max_pair_idx = len(patterns)
    max_edge_idx = len(patterns) + 1
    min_pair7_idx = len(patterns) + 2
    min_support_idx = len(patterns) + 3
    var_count = len(patterns) + 4

    objective = np.zeros(var_count)
    objective[max_pair_idx] = 8.0
    objective[max_edge_idx] = 10.0
    objective[min_pair7_idx] = -2.5
    objective[min_support_idx] = -1.0
    for idx, pattern in enumerate(patterns):
        objective[idx] = 0.001 * abs(pattern["size"] - 4.5) + 0.0002 * pattern["edge_count"]

    constraints = []
    lower = []
    upper = []

    row = np.zeros(var_count)
    row[: len(patterns)] = 1
    constraints.append(row)
    lower.append(N)
    upper.append(N)

    for witness in range(1, LIST_SIZE + 1):
        row = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row[idx] = contains(int(pattern["mask"]), witness)
        constraints.append(row)
        lower.append(TARGET_AGREEMENT)
        upper.append(N - 1)

        row_min = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row_min[idx] = contains(int(pattern["mask"]), witness)
        row_min[min_support_idx] = -1
        constraints.append(row_min)
        lower.append(0)
        upper.append(float("inf"))

    for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
        row = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row[idx] = pair_same(int(pattern["mask"]), pair)
        constraints.append(row)
        lower.append(float("-inf"))
        upper.append(PAIR_CAP)

        row_max = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row_max[idx] = pair_same(int(pattern["mask"]), pair)
        row_max[max_pair_idx] = -1
        constraints.append(row_max)
        lower.append(float("-inf"))
        upper.append(0)

    for label in PAIR7_PAIR_LABELS:
        pair = next(pair for pair_label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True) if pair_label == label)
        row = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row[idx] = pair_same(int(pattern["mask"]), pair)
        constraints.append(row)
        lower.append(PAIR7_LOWER)
        upper.append(float("inf"))

        row_min = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row_min[idx] = pair_same(int(pattern["mask"]), pair)
        row_min[min_pair7_idx] = -1
        constraints.append(row_min)
        lower.append(0)
        upper.append(float("inf"))

    for label in graph["edge_labels"]:
        row = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row[idx] = int(label in pattern["edge_labels"])
        constraints.append(row)
        lower.append(float("-inf"))
        upper.append(PAIR_CAP)

        row_max = np.zeros(var_count)
        for idx, pattern in enumerate(patterns):
            row_max[idx] = int(label in pattern["edge_labels"])
        row_max[max_edge_idx] = -1
        constraints.append(row_max)
        lower.append(float("-inf"))
        upper.append(0)

    bounds = Bounds(
        np.r_[np.zeros(len(patterns)), 0, 0, 0, 0],
        np.r_[N * np.ones(len(patterns)), PAIR_CAP, PAIR_CAP, N, N],
    )
    integrality = np.r_[np.ones(len(patterns)), np.zeros(4)]
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 45},
    )

    out = dict(graph)
    out["pattern_count"] = len(patterns)
    if not result.success:
        out.update(
            {
                "solver_status": "INFEASIBLE_OR_LIMIT",
                "solver_message": str(result.message),
                "failure_mode": "BOUNDED_CYCLE_COUNT_INFEASIBLE",
            }
        )
        return out

    counts = []
    for pattern, value in zip(patterns, result.x[: len(patterns)], strict=True):
        count = int(round(float(value)))
        if not count:
            continue
        row = dict(pattern)
        row["count"] = count
        counts.append(row)
    summary = evaluate_counts(counts, graph)
    out.update(summary)
    out.update(
        {
            "solver_status": "OPTIMAL_OR_FEASIBLE",
            "solver_message": str(result.message),
            "objective_value": float(result.fun),
            "connected_class_edge_counts": counts,
            "connected_class_edge_counts_hash": hash_payload(counts),
            "failure_mode": "BOUNDED_CYCLE_EXACT_TARGET",
        }
    )
    return out


def evaluate_counts(counts: list[dict[str, Any]], graph: dict[str, Any]) -> dict[str, Any]:
    supports = [0] * LIST_SIZE
    pair_counts = {label: 0 for label in PAIR_LABELS}
    edge_loads = {label: 0 for label in graph["edge_labels"]}
    size_counts: dict[str, int] = {}
    selected_incidence_count = 0
    edge_incidence_count = 0
    for row in counts:
        mask = int(row["mask"])
        count = int(row["count"])
        selected_incidence_count += count * int(row["size"])
        edge_incidence_count += count * len(row["edge_labels"])
        size_counts[str(row["size"])] = size_counts.get(str(row["size"]), 0) + count
        for witness in range(1, LIST_SIZE + 1):
            supports[witness - 1] += count * contains(mask, witness)
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            pair_counts[label] += count * pair_same(mask, pair)
        for label in row["edge_labels"]:
            edge_loads[label] += count
    pair7_counts = [pair_counts[label] for label in PAIR7_PAIR_LABELS]
    guard_values = [
        min(supports) - TARGET_AGREEMENT,
        min(pair7_counts) - PAIR7_LOWER,
        PAIR_CAP - max(pair_counts.values()),
        PAIR_CAP - max(edge_loads.values()),
    ]
    return {
        "support_vector": supports,
        "selected_incidence_count": selected_incidence_count,
        "edge_incidence_count": edge_incidence_count,
        "pair_count_matrix": pair_counts,
        "max_pair_count": max(pair_counts.values()),
        "pair7_counts": pair7_counts,
        "edge_loads": edge_loads,
        "max_edge_load": max(edge_loads.values()),
        "edge_slack_total": sum(PAIR_CAP - value for value in edge_loads.values()),
        "selected_class_size_counts": dict(sorted(size_counts.items(), key=lambda item: int(item[0]))),
        "support_guard": min(supports) >= TARGET_AGREEMENT,
        "pair_cap_guard": max(pair_counts.values()) <= PAIR_CAP,
        "pair7_guard": min(pair7_counts) >= PAIR7_LOWER,
        "edge_cap_guard": max(edge_loads.values()) <= PAIR_CAP,
        "guard_margin": min(guard_values),
        "quotient_variable_budget": sum(K - value for value in edge_loads.values()),
        "cycle_constraint_count": graph["cycle_rank"] * K,
    }


def assign_coordinates(counts: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    rows = []
    for row in counts:
        for _ in range(int(row["count"])):
            rows.append(
                {
                    "mask": int(row["mask"]),
                    "members": [int(value) for value in row["members"]],
                    "size": int(row["size"]),
                    "edge_labels": [str(value) for value in row["edge_labels"]],
                }
            )
    if len(rows) != N:
        raise RuntimeError("bad coordinate count")
    rng = random.Random(seed)
    rng.shuffle(rows)
    for position, row in enumerate(rows):
        row["position"] = position
        row["fiber"] = position % FIBER_COUNT
    return rows


def fiber_histogram(coordinate_classes: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for row in coordinate_classes:
        fiber = str(row["fiber"])
        size = str(row["size"])
        out.setdefault(fiber, {})
        out[fiber][size] = out[fiber].get(size, 0) + 1
    return out


def build_record() -> dict[str, Any]:
    graphs = [graph_summary(spec) for spec in GRAPH_SPECS]
    designs = [solve_graph_counts(graph) for graph in graphs]
    feasible = [
        row
        for row in designs
        if row.get("solver_status") == "OPTIMAL_OR_FEASIBLE"
        and row["support_guard"]
        and row["pair_cap_guard"]
        and row["pair7_guard"]
        and row["edge_cap_guard"]
    ]
    if feasible:
        best = max(
            feasible,
            key=lambda row: (
                row["guard_margin"],
                row["cycle_rank"],
                row["quotient_variable_budget"],
                -row["max_edge_load"],
                -row["max_pair_count"],
                row["graph_id"],
            ),
        )
        coordinate_classes = assign_coordinates(best["connected_class_edge_counts"], seed=327)
        best["coordinate_classes"] = coordinate_classes
        best["coordinate_classes_hash"] = hash_payload(coordinate_classes)
        best["quotient_fiber_histogram"] = fiber_histogram(coordinate_classes)
    else:
        best = None

    tree_obstruction = {
        "selected_incidence_lower": LIST_SIZE * TARGET_AGREEMENT,
        "tree_edge_incidence_lower": TREE_EDGE_INCIDENCE_LOWER,
        "tree_edge_capacity": TREE_EDGE_CAPACITY,
        "edge_incidence_deficit": TREE_EDGE_INCIDENCE_LOWER - TREE_EDGE_CAPACITY,
        "minimum_carrier_edges_by_count": (TREE_EDGE_INCIDENCE_LOWER + PAIR_CAP - 1) // PAIR_CAP,
    }

    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "tree_obstruction": tree_obstruction,
        "bounded_cycle_search": {
            "carrier_graphs_tested": len(designs),
            "feasible_hypergraphs": len(feasible),
            "exact_lift_attempts": 0,
            "best_carrier_edge_count": None if best is None else best["edge_count"],
            "best_cycle_rank": None if best is None else best["cycle_rank"],
            "best_graph_id": None if best is None else best["graph_id"],
            "best_graph_edges": None if best is None else best["edges"],
            "best_supports": None if best is None else best["support_vector"],
            "best_pair_counts": None if best is None else best["pair_count_matrix"],
            "best_edge_loads": None if best is None else best["edge_loads"],
            "best_guard_margin": None if best is None else best["guard_margin"],
            "best_coordinate_classes_hash": None if best is None else best["coordinate_classes_hash"],
            "best_quotient_fiber_histogram": None if best is None else best["quotient_fiber_histogram"],
            "coordinate_classes": None if best is None else best["coordinate_classes"],
            "all_designs": designs,
            "best_failure_mode": "BOUNDED_CYCLE_COUNT_INFEASIBLE" if best is None else best["failure_mode"],
        },
        "exact_edge_lift": {
            "field": None,
            "H_order": None,
            "edge_variable_count": None if best is None else best["quotient_variable_budget"],
            "cycle_constraint_count": None if best is None else best["cycle_constraint_count"],
            "matrix_shape": None,
            "rank": None,
            "nullity": None,
            "forced_equal_pairs": [],
            "min_projection_rank": None,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
            "best_failure_mode": None,
        },
        "proof_status": "CANDIDATE / BOUNDED_CYCLE_COMBINATORIAL_TARGET / PARTIAL / EXPERIMENTAL"
        if best is not None
        else "CONSTRUCTION_FAIL / BOUNDED_CYCLE_COUNT_INFEASIBLE / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
        ],
    }
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["bounded_cycle_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "carrier_graphs_tested": search["carrier_graphs_tested"],
                    "feasible_hypergraphs": search["feasible_hypergraphs"],
                    "best_graph_id": search["best_graph_id"],
                    "best_carrier_edge_count": search["best_carrier_edge_count"],
                    "best_cycle_rank": search["best_cycle_rank"],
                    "best_guard_margin": search["best_guard_margin"],
                    "best_edge_loads": search["best_edge_loads"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_BOUNDED_CYCLE_CARRIER_HYPERGRAPH_SEARCH_READY")


if __name__ == "__main__":
    main()
