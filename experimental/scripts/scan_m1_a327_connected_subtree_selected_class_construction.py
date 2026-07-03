#!/usr/bin/env python3
"""Search connected-subtree selected-class designs for M1 a=327."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import deque
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "a3be7b6"
OUTPUT_DATA = Path("experimental/data/m1_a327_connected_subtree_selected_class_construction.json")

N = 512
FIBER_COUNT = 16
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142

PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]

TREE_SPECS = [
    {
        "tree_id": "path_1237456",
        "tree_edges": [[1, 2], [2, 3], [3, 7], [7, 4], [4, 5], [5, 6]],
    },
    {
        "tree_id": "path_1234765",
        "tree_edges": [[1, 2], [2, 3], [3, 4], [4, 7], [7, 6], [6, 5]],
    },
    {
        "tree_id": "balanced_T",
        "tree_edges": [[7, 2], [7, 3], [7, 4], [2, 1], [4, 5], [4, 6]],
    },
    {
        "tree_id": "two_pair_spine",
        "tree_edges": [[2, 1], [1, 4], [4, 7], [7, 5], [5, 3], [3, 6]],
    },
]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def mask_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(LIST_SIZE) if mask & (1 << idx)]


def mask_from_members(members: list[int] | tuple[int, ...]) -> int:
    mask = 0
    for member in members:
        mask |= 1 << (int(member) - 1)
    return mask


def adjacency(tree_edges: list[list[int]]) -> dict[int, list[int]]:
    out = {node: [] for node in range(1, LIST_SIZE + 1)}
    for left, right in tree_edges:
        out[int(left)].append(int(right))
        out[int(right)].append(int(left))
    return out


def is_connected_subset(mask: int, adj: dict[int, list[int]]) -> bool:
    members = mask_members(mask)
    if not members:
        return False
    seen = {members[0]}
    queue = deque([members[0]])
    member_set = set(members)
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor in member_set and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen == member_set


def connected_subtree_masks(tree_edges: list[list[int]], sizes: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7)) -> list[int]:
    adj = adjacency(tree_edges)
    masks = []
    for size in sizes:
        for combo in itertools.combinations(range(1, LIST_SIZE + 1), size):
            mask = mask_from_members(combo)
            if is_connected_subset(mask, adj):
                masks.append(mask)
    return sorted(set(masks), key=lambda value: (value.bit_count(), mask_members(value)))


def contains(mask: int, witness: int) -> int:
    return int(bool(mask & (1 << (witness - 1))))


def pair_same(mask: int, pair: tuple[int, int]) -> int:
    return contains(mask, pair[0]) * contains(mask, pair[1])


def solve_tree_counts(tree_spec: dict[str, Any]) -> dict[str, Any]:
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover
        return {
            "tree_id": tree_spec["tree_id"],
            "tree_edges": tree_spec["tree_edges"],
            "solver_status": "SCIPY_UNAVAILABLE",
            "solver_error": str(exc),
            "failure_mode": "CONNECTED_SUBTREE_COUNT_INFEASIBLE",
        }

    masks = connected_subtree_masks(tree_spec["tree_edges"])
    max_pair_idx = len(masks)
    min_pair7_idx = len(masks) + 1
    min_support_idx = len(masks) + 2
    var_count = len(masks) + 3
    objective = np.zeros(var_count)
    objective[max_pair_idx] = 10.0
    objective[min_pair7_idx] = -3.0
    objective[min_support_idx] = -1.0
    for idx, mask in enumerate(masks):
        # Prefer class sizes near the required 4.47 average without forbidding flexibility.
        objective[idx] = 0.001 * abs(mask.bit_count() - 4.5)

    constraints = []
    lower = []
    upper = []

    row = np.zeros(var_count)
    row[: len(masks)] = 1
    constraints.append(row)
    lower.append(N)
    upper.append(N)

    for witness in range(1, LIST_SIZE + 1):
        row = np.zeros(var_count)
        for idx, mask in enumerate(masks):
            row[idx] = contains(mask, witness)
        row[min_support_idx] = -1
        constraints.append(row)
        lower.append(0)
        upper.append(float("inf"))

        row_lower = np.zeros(var_count)
        for idx, mask in enumerate(masks):
            row_lower[idx] = contains(mask, witness)
        constraints.append(row_lower)
        lower.append(TARGET_AGREEMENT)
        upper.append(N - 1)

    for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
        row = np.zeros(var_count)
        for idx, mask in enumerate(masks):
            row[idx] = pair_same(mask, pair)
        row[max_pair_idx] = -1
        constraints.append(row)
        lower.append(float("-inf"))
        upper.append(0)

        row_cap = np.zeros(var_count)
        for idx, mask in enumerate(masks):
            row_cap[idx] = pair_same(mask, pair)
        constraints.append(row_cap)
        lower.append(float("-inf"))
        upper.append(PAIR_CAP)

    for label in PAIR7_PAIR_LABELS:
        pair = next(pair for pair_label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True) if pair_label == label)
        row = np.zeros(var_count)
        for idx, mask in enumerate(masks):
            row[idx] = pair_same(mask, pair)
        row[min_pair7_idx] = -1
        constraints.append(row)
        lower.append(0)
        upper.append(float("inf"))

        row_lower = np.zeros(var_count)
        for idx, mask in enumerate(masks):
            row_lower[idx] = pair_same(mask, pair)
        constraints.append(row_lower)
        lower.append(PAIR7_LOWER)
        upper.append(float("inf"))

    bounds = Bounds(
        np.r_[np.zeros(len(masks)), 0, 0, 0],
        np.r_[N * np.ones(len(masks)), PAIR_CAP, N, N],
    )
    integrality = np.r_[np.ones(len(masks)), np.zeros(3)]
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 30},
    )
    if not result.success:
        return {
            "tree_id": tree_spec["tree_id"],
            "tree_edges": tree_spec["tree_edges"],
            "connected_subtree_count": len(masks),
            "solver_status": "INFEASIBLE_OR_LIMIT",
            "solver_message": str(result.message),
            "failure_mode": "CONNECTED_SUBTREE_COUNT_INFEASIBLE",
        }

    counts = [
        {
            "mask": mask,
            "members": mask_members(mask),
            "size": mask.bit_count(),
            "count": int(round(value)),
        }
        for mask, value in zip(masks, result.x[: len(masks)], strict=True)
        if int(round(value))
    ]
    summary = evaluate_counts(counts, tree_spec["tree_edges"])
    summary.update(
        {
            "tree_id": tree_spec["tree_id"],
            "tree_edges": tree_spec["tree_edges"],
            "connected_subtree_count": len(masks),
            "solver_status": "OPTIMAL_OR_FEASIBLE",
            "solver_message": str(result.message),
            "objective_value": float(result.fun),
            "connected_class_counts": counts,
            "connected_class_count_hash": hash_payload(counts),
            "failure_mode": "CONNECTED_SUBTREE_EXACT_TARGET",
        }
    )
    return summary


def evaluate_counts(counts: list[dict[str, Any]], tree_edges: list[list[int]]) -> dict[str, Any]:
    supports = [0] * LIST_SIZE
    pair_counts = {label: 0 for label in PAIR_LABELS}
    for row in counts:
        mask = int(row["mask"])
        count = int(row["count"])
        for witness in range(1, LIST_SIZE + 1):
            supports[witness - 1] += count * contains(mask, witness)
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            pair_counts[label] += count * pair_same(mask, pair)
    edge_counts = {f"P{min(edge)}{max(edge)}": pair_counts[f"P{min(edge)}{max(edge)}"] for edge in tree_edges}
    pair7_counts = [pair_counts[label] for label in PAIR7_PAIR_LABELS]
    size_counts: dict[str, int] = {}
    for row in counts:
        key = str(row["size"])
        size_counts[key] = size_counts.get(key, 0) + int(row["count"])
    return {
        "support_vector": supports,
        "selected_incidence_count": sum(supports),
        "pair_count_matrix": pair_counts,
        "max_pair_count": max(pair_counts.values()),
        "pair7_counts": pair7_counts,
        "edge_counts": edge_counts,
        "max_edge_count": max(edge_counts.values()),
        "selected_class_size_counts": dict(sorted(size_counts.items(), key=lambda item: int(item[0]))),
        "support_guard": min(supports) >= TARGET_AGREEMENT,
        "pair_cap_guard": max(pair_counts.values()) <= PAIR_CAP,
        "pair7_guard": min(pair7_counts) >= PAIR7_LOWER,
        "edge_degree_guard": max(edge_counts.values()) <= PAIR_CAP,
    }


def assign_coordinates(counts: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    masks = []
    for row in counts:
        masks.extend([int(row["mask"])] * int(row["count"]))
    if len(masks) != N:
        raise RuntimeError("bad coordinate count")
    rng = random.Random(seed)
    rng.shuffle(masks)
    rows = []
    for position, mask in enumerate(masks):
        rows.append(
            {
                "position": position,
                "fiber": position % FIBER_COUNT,
                "mask": mask,
                "members": mask_members(mask),
                "size": mask.bit_count(),
            }
        )
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
    designs = [solve_tree_counts(tree_spec) for tree_spec in TREE_SPECS]
    feasible = [
        row
        for row in designs
        if row.get("solver_status") == "OPTIMAL_OR_FEASIBLE"
        and row["support_guard"]
        and row["pair_cap_guard"]
        and row["pair7_guard"]
        and row["edge_degree_guard"]
    ]
    if feasible:
        best = max(
            feasible,
            key=lambda row: (
                min(row["support_vector"]) - TARGET_AGREEMENT,
                min(row["pair7_counts"]) - PAIR7_LOWER,
                -row["max_pair_count"],
                -row["max_edge_count"],
            ),
        )
        coordinate_classes = assign_coordinates(best["connected_class_counts"], seed=17)
        best["coordinate_classes"] = coordinate_classes
        best["coordinate_classes_hash"] = hash_payload(coordinate_classes)
        best["quotient_fiber_histogram"] = fiber_histogram(coordinate_classes)
    else:
        best = None

    selected_incidence_lower = LIST_SIZE * TARGET_AGREEMENT
    tree_edge_incidence_lower = selected_incidence_lower - N
    tree_edge_incidence_upper = (LIST_SIZE - 1) * PAIR_CAP
    count_obstruction = {
        "reason": "For connected selected classes on a tree, sum_e edge_count_e = sum_h(|C_h|-1).",
        "support_selected_incidence_lower": selected_incidence_lower,
        "tree_edge_incidence_lower": tree_edge_incidence_lower,
        "tree_edge_incidence_upper_from_pair_cap": tree_edge_incidence_upper,
        "edge_incidence_deficit": tree_edge_incidence_lower - tree_edge_incidence_upper,
        "obstruction_applies_to_any_7_node_tree": tree_edge_incidence_lower > tree_edge_incidence_upper,
    }

    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "connected_subtree_design": {
            "trees_tested": len(TREE_SPECS),
            "feasible_designs": len(feasible),
            "counting_obstruction": count_obstruction,
            "tree_id": None if best is None else best["tree_id"],
            "tree_edges": None if best is None else best["tree_edges"],
            "connected_class_counts": None if best is None else best["connected_class_counts"],
            "support_vector": None if best is None else best["support_vector"],
            "pair_count_matrix": None if best is None else best["pair_count_matrix"],
            "max_pair_count": None if best is None else best["max_pair_count"],
            "pair7_counts": None if best is None else best["pair7_counts"],
            "edge_counts": None if best is None else best["edge_counts"],
            "quotient_fiber_histogram": None if best is None else best["quotient_fiber_histogram"],
            "coordinate_classes_hash": None if best is None else best["coordinate_classes_hash"],
            "coordinate_classes": None if best is None else best["coordinate_classes"],
            "all_designs": designs,
            "best_failure_mode": "CONNECTED_SUBTREE_GLOBAL_COUNT_OBSTRUCTION" if best is None else best["failure_mode"],
        },
        "exact_construction": {
            "edge_zero_set_sizes": None,
            "edge_polynomial_degrees": None,
            "scalars": None,
            "degree_bound_ok": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
            "best_failure_mode": None,
        },
        "proof_status": "CANDIDATE / CONNECTED_SUBTREE_COUNT / PARTIAL / EXPERIMENTAL"
        if best is not None
        else "CONSTRUCTION_FAIL / CONNECTED_SUBTREE_GLOBAL_COUNT_OBSTRUCTION / PARTIAL / EXPERIMENTAL",
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
        design = record["connected_subtree_design"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "trees_tested": design["trees_tested"],
                    "feasible_designs": design["feasible_designs"],
                    "tree_id": design["tree_id"],
                    "support_vector": design["support_vector"],
                    "max_pair_count": design["max_pair_count"],
                    "pair7_counts": design["pair7_counts"],
                    "edge_counts": design["edge_counts"],
                    "best_failure_mode": design["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_CONNECTED_SUBTREE_SELECTED_CLASS_CONSTRUCTION_READY")


if __name__ == "__main__":
    main()
