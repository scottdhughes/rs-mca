#!/usr/bin/env python3
"""Tree-rank feedback search for RS-feasible M1 a=327 selected hypergraphs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "aed0ef0"
SOURCE_DATA = Path("experimental/data/m1_a327_selected_class_tree_divisibility_lift.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_rs_feasible_hypergraph_tree_rank_feedback.json")

N = 512
FIBER_COUNT = 16
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PROXY_PRIME = 12289  # 12289 - 1 is divisible by 512.

PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]

TREE_EDGE_SETS = {
    "max_weight_tree": None,
    "pair7_heavy_tree": None,
    "balanced_tree": None,
}

PROFILE_SPECS = [
    {
        "profile_id": "balanced_45",
        "selected_class_sizes": [4, 5],
        "max_pair_weight": 1.0,
        "min_pair7_weight": 0.25,
        "tree_bias_weight": 0.0,
        "tree_bias_edges": [],
        "seeds": [0, 1],
    },
    {
        "profile_id": "pair7_guarded_45",
        "selected_class_sizes": [4, 5],
        "max_pair_weight": 0.5,
        "min_pair7_weight": 3.0,
        "tree_bias_weight": 0.0,
        "tree_bias_edges": [],
        "seeds": [2, 3],
    },
    {
        "profile_id": "low_cycle_overlap_45",
        "selected_class_sizes": [4, 5],
        "max_pair_weight": 2.5,
        "min_pair7_weight": 0.5,
        "tree_bias_weight": 0.0,
        "tree_bias_edges": [],
        "seeds": [4, 5],
    },
    {
        "profile_id": "tree_nullity_weighted_path",
        "selected_class_sizes": [4, 5],
        "max_pair_weight": 0.5,
        "min_pair7_weight": 0.5,
        "tree_bias_weight": 2.0,
        "tree_bias_edges": ["P12", "P23", "P34", "P45", "P46", "P67"],
        "seeds": [6, 7],
    },
    {
        "profile_id": "mixed_345",
        "selected_class_sizes": [3, 4, 5],
        "max_pair_weight": 1.0,
        "min_pair7_weight": 0.75,
        "tree_bias_weight": 0.25,
        "tree_bias_edges": ["P17", "P27", "P37", "P47", "P57"],
        "seeds": [8, 9],
    },
    {
        "profile_id": "fiber_balanced_tree_slack",
        "selected_class_sizes": [3, 4, 5],
        "max_pair_weight": 1.5,
        "min_pair7_weight": 1.0,
        "tree_bias_weight": 1.0,
        "tree_bias_edges": ["P12", "P23", "P34", "P45", "P56", "P67"],
        "seeds": [10, 11],
    },
]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def mask_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(LIST_SIZE) if mask & (1 << idx)]


def subset_masks(sizes: list[int]) -> list[int]:
    masks = []
    for size in sizes:
        for combo in itertools.combinations(range(LIST_SIZE), size):
            mask = 0
            for idx in combo:
                mask |= 1 << idx
            masks.append(mask)
    return sorted(set(masks), key=lambda value: (value.bit_count(), value))


def contains(mask: int, witness_zero: int) -> int:
    return int(bool(mask & (1 << witness_zero)))


def pair_same(mask: int, pair: tuple[int, int]) -> int:
    left, right = pair
    return int(bool(mask & (1 << (left - 1))) and bool(mask & (1 << (right - 1))))


def solve_profile(spec: dict[str, Any]) -> dict[str, Any]:
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover
        return {
            "profile_id": spec["profile_id"],
            "solver_status": "SCIPY_UNAVAILABLE",
            "solver_error": str(exc),
            "failure_mode": "RANK_FEEDBACK_SOLVER_UNAVAILABLE",
        }

    classes = subset_masks(spec["selected_class_sizes"])
    max_pair_idx = len(classes)
    min_pair7_idx = len(classes) + 1
    var_count = len(classes) + 2
    objective = np.zeros(var_count)
    objective[max_pair_idx] = float(spec["max_pair_weight"])
    objective[min_pair7_idx] = -float(spec["min_pair7_weight"])
    tree_bias = set(spec.get("tree_bias_edges", []))
    for idx, mask in enumerate(classes):
        pair_score = sum(pair_same(mask, pair) for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True) if label in tree_bias)
        objective[idx] -= float(spec["tree_bias_weight"]) * pair_score
        objective[idx] += 0.0001 * mask.bit_count()

    constraints = []
    lower = []
    upper = []

    row = np.zeros(var_count)
    row[: len(classes)] = 1
    constraints.append(row)
    lower.append(N)
    upper.append(N)

    for witness in range(LIST_SIZE):
        row = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row[idx] = contains(mask, witness)
        constraints.append(row)
        lower.append(TARGET_AGREEMENT)
        upper.append(TARGET_AGREEMENT)

    for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
        row = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row[idx] = pair_same(mask, pair)
        row[max_pair_idx] = -1
        constraints.append(row)
        lower.append(float("-inf"))
        upper.append(0)

        row_cap = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row_cap[idx] = pair_same(mask, pair)
        constraints.append(row_cap)
        lower.append(float("-inf"))
        upper.append(PAIR_CAP)

    for label in PAIR7_PAIR_LABELS:
        pair = next(pair for pair_label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True) if pair_label == label)
        row = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row[idx] = pair_same(mask, pair)
        row[min_pair7_idx] = -1
        constraints.append(row)
        lower.append(0)
        upper.append(float("inf"))

        row_lower = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row_lower[idx] = pair_same(mask, pair)
        constraints.append(row_lower)
        lower.append(PAIR7_LOWER)
        upper.append(float("inf"))

    bounds = Bounds(
        np.r_[np.zeros(len(classes)), 0, 0],
        np.r_[N * np.ones(len(classes)), PAIR_CAP, N],
    )
    integrality = np.r_[np.ones(len(classes)), np.zeros(2)]
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 30},
    )
    if not result.success:
        return {
            "profile_id": spec["profile_id"],
            "selected_class_sizes": spec["selected_class_sizes"],
            "solver_status": "INFEASIBLE_OR_LIMIT",
            "solver_message": str(result.message),
            "failure_mode": "RANK_FEEDBACK_RS_CAP_FAIL",
        }
    counts = [
        {"mask": mask, "members": mask_members(mask), "count": int(round(value))}
        for mask, value in zip(classes, result.x[: len(classes)], strict=True)
        if int(round(value))
    ]
    return {
        "profile_id": spec["profile_id"],
        "selected_class_sizes": spec["selected_class_sizes"],
        "solver_status": "OPTIMAL_OR_FEASIBLE",
        "solver_message": str(result.message),
        "objective_value": float(result.fun),
        "selected_counts": counts,
        "selected_count_hash": hash_payload(counts),
        "max_pair_bound_value": int(round(result.x[max_pair_idx])),
        "min_pair7_value": int(round(result.x[min_pair7_idx])),
        "failure_mode": "RANK_FEEDBACK_COUNT_TARGET",
    }


def expand_coordinate_classes(count_rows: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    masks = []
    for row in count_rows:
        masks.extend([int(row["mask"])] * int(row["count"]))
    if len(masks) != N:
        raise RuntimeError("bad coordinate count")
    rng = random.Random(seed)
    rng.shuffle(masks)
    return [
        {
            "position": pos,
            "fiber": pos % FIBER_COUNT,
            "mask": mask,
            "members": mask_members(mask),
            "size": mask.bit_count(),
        }
        for pos, mask in enumerate(masks)
    ]


def pair_sets(coordinate_classes: list[dict[str, Any]]) -> dict[str, list[int]]:
    sets = {label: [] for label in PAIR_LABELS}
    for row in coordinate_classes:
        members = set(row["members"])
        for label, (left, right) in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if left in members and right in members:
                sets[label].append(int(row["position"]))
    return sets


def pair_counts(pair_sets_: dict[str, list[int]]) -> dict[str, int]:
    return {label: len(rows) for label, rows in pair_sets_.items()}


class DSU:
    def __init__(self):
        self.parent = list(range(LIST_SIZE + 1))

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


def edge_label(edge: list[int] | tuple[int, int]) -> str:
    left, right = sorted((int(edge[0]), int(edge[1])))
    return f"P{left}{right}"


def kruskal(edge_order: list[tuple[int, int, int]]) -> list[list[int]]:
    dsu = DSU()
    edges = []
    for left, right, _weight in edge_order:
        if dsu.union(left, right):
            edges.append([left, right])
        if len(edges) == LIST_SIZE - 1:
            return sorted([sorted(edge) for edge in edges])
    raise RuntimeError("failed to build tree")


def candidate_trees(counts: dict[str, int]) -> list[dict[str, Any]]:
    edge_rows = [(left, right, counts[f"P{left}{right}"]) for left, right in PAIR_INDICES]
    raw_orders = [
        ("max_weight_tree", sorted(edge_rows, key=lambda row: (-row[2], row[0] != 1, row[0], row[1]))),
        ("pair7_heavy_tree", sorted(edge_rows, key=lambda row: (row[1] != 7, -row[2], row[0], row[1]))),
        ("balanced_tree", sorted(edge_rows, key=lambda row: (-row[2], abs(row[0] - row[1]), row[0], row[1]))),
        ("min_cycle_pressure_tree", sorted(edge_rows, key=lambda row: (-row[2], -int(row[1] == 7), row[0], row[1]))),
    ]
    seen = set()
    out = []
    for name, order in raw_orders:
        edges = kruskal(order)
        labels = [edge_label(edge) for edge in edges]
        key = tuple(labels)
        if key in seen:
            continue
        seen.add(key)
        tree_weight = sum(counts[label] for label in labels)
        tree_vars = sum(K - counts[label] for label in labels)
        non_tree = [label for label in PAIR_LABELS if label not in set(labels)]
        non_tree_eqs = sum(counts[label] for label in non_tree)
        out.append(
            {
                "tree_name": name,
                "edges": edges,
                "edge_labels": labels,
                "total_weight": tree_weight,
                "tree_variable_count": tree_vars,
                "non_tree_edge_labels": non_tree,
                "non_tree_equation_count": non_tree_eqs,
                "surplus": tree_vars - non_tree_eqs,
            }
        )
    return out


def primitive_root_mod_prime(prime: int) -> int:
    factors = [2, 3]
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise RuntimeError("primitive root not found")


def proxy_H(prime: int = PROXY_PRIME) -> list[int]:
    generator = primitive_root_mod_prime(prime)
    root = pow(generator, (prime - 1) // N, prime)
    return [pow(root, idx, prime) for idx in range(N)]


def modular_rank(rows: list[list[int]], ncols: int, prime: int) -> int:
    basis: dict[int, list[int]] = {}
    rank = 0
    for raw in rows:
        row = [value % prime for value in raw]
        while True:
            pivot = next((idx for idx, value in enumerate(row) if value), None)
            if pivot is None:
                break
            if pivot not in basis:
                inv = pow(row[pivot], prime - 2, prime)
                row = [(value * inv) % prime for value in row]
                basis[pivot] = row
                rank += 1
                break
            factor = row[pivot]
            pivot_row = basis[pivot]
            row = [(value - factor * pivot_row[idx]) % prime for idx, value in enumerate(row)]
        if rank == ncols:
            break
    return rank


def orient_tree(edges: list[list[int]]) -> dict[int, dict[str, int]]:
    adjacency: dict[int, list[int]] = {node: [] for node in range(1, LIST_SIZE + 1)}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    parent = {1: None}
    stack = [1]
    while stack:
        node = stack.pop()
        for nxt in adjacency[node]:
            if nxt not in parent:
                parent[nxt] = node
                stack.append(nxt)
    paths: dict[int, dict[str, int]] = {1: {}}
    for node in range(2, LIST_SIZE + 1):
        current = node
        coeffs: dict[str, int] = {}
        while current != 1:
            previous = parent[current]
            label = edge_label([previous, current])
            coeffs[label] = coeffs.get(label, 0) + 1
            current = previous
        paths[node] = coeffs
    return paths


def path_coeffs(paths: dict[int, dict[str, int]], left: int, right: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for label, coeff in paths[left].items():
        out[label] = out.get(label, 0) + coeff
    for label, coeff in paths[right].items():
        out[label] = out.get(label, 0) - coeff
    return {label: coeff for label, coeff in out.items() if coeff}


def proxy_rank(pair_sets_: dict[str, list[int]], tree: dict[str, Any], prime: int = PROXY_PRIME) -> dict[str, Any]:
    h_values = proxy_H(prime)
    powers = [[1 for _ in range(N)]]
    for _degree in range(1, K):
        powers.append([(powers[-1][pos] * h_values[pos]) % prime for pos in range(N)])

    blocks = {}
    cursor = 0
    z_evals: dict[str, list[int]] = {}
    for label in tree["edge_labels"]:
        qdeg = K - len(pair_sets_[label])
        blocks[label] = (cursor, qdeg)
        cursor += qdeg
        evals = []
        roots = pair_sets_[label]
        for pos in range(N):
            value = 1
            x = h_values[pos]
            for root_pos in roots:
                value = (value * (x - h_values[int(root_pos)])) % prime
            evals.append(value)
        z_evals[label] = evals

    paths = orient_tree(tree["edges"])
    rows = []
    for non_tree_label in tree["non_tree_edge_labels"]:
        left, right = int(non_tree_label[1]), int(non_tree_label[2])
        path = path_coeffs(paths, left, right)
        for pos in pair_sets_[non_tree_label]:
            pos = int(pos)
            row = [0] * cursor
            for label, sign in path.items():
                start, qdeg = blocks[label]
                z_value = z_evals[label][pos]
                if z_value == 0:
                    continue
                for degree in range(qdeg):
                    row[start + degree] = (row[start + degree] + sign * z_value * powers[degree][pos]) % prime
            rows.append(row)
    rank = modular_rank(rows, cursor, prime)
    return {
        "proxy_prime": prime,
        "matrix_shape": [len(rows), cursor],
        "proxy_rank": rank,
        "proxy_nullity": cursor - rank,
        "proxy_failure_mode": "TREE_PROXY_NULLITY_POSITIVE" if cursor - rank > 0 else "TREE_PROXY_FULL_RANK",
    }


def evaluate_candidate(profile: dict[str, Any], seed: int) -> dict[str, Any]:
    coordinate_classes = expand_coordinate_classes(profile["selected_counts"], seed)
    sets = pair_sets(coordinate_classes)
    counts = pair_counts(sets)
    trees = candidate_trees(counts)
    proxy_results = []
    for tree in trees:
        proxy = proxy_rank(sets, tree)
        proxy_results.append({**tree, **proxy})
    best_proxy = max(proxy_results, key=lambda row: (row["proxy_nullity"], row["tree_variable_count"], -row["non_tree_equation_count"]))
    supports = [0] * LIST_SIZE
    for row in coordinate_classes:
        for witness in row["members"]:
            supports[int(witness) - 1] += 1
    pair7_counts = [counts[label] for label in PAIR7_PAIR_LABELS]
    return {
        "profile_id": profile["profile_id"],
        "assignment_seed": seed,
        "supports": supports,
        "max_pair_count": max(counts.values()),
        "pair7_counts": pair7_counts,
        "pair_counts": counts,
        "pair_sets_hash": hash_payload(sets),
        "coordinate_classes_hash": hash_payload(coordinate_classes),
        "coordinate_classes": coordinate_classes,
        "trees": proxy_results,
        "best_tree_name": best_proxy["tree_name"],
        "best_tree_edges": best_proxy["edges"],
        "best_tree_edge_labels": best_proxy["edge_labels"],
        "best_tree_variable_count": best_proxy["tree_variable_count"],
        "best_non_tree_equation_count": best_proxy["non_tree_equation_count"],
        "best_proxy_rank": best_proxy["proxy_rank"],
        "best_proxy_nullity": best_proxy["proxy_nullity"],
        "best_failure_mode": "RANK_FEEDBACK_PROXY_FULL_RANK"
        if best_proxy["proxy_nullity"] == 0
        else "TREE_PROXY_NULLITY_POSITIVE",
    }


def source_obstruction() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        source = json.load(handle)
    tree = source["tree_divisibility"]
    return {
        "target": "9fcdb02_thin_selected_class",
        "best_tree_shape": tree["matrix_shape"],
        "best_tree_rank": tree["rank"],
        "best_tree_nullity": tree["nullity"],
        "failure_mode": tree["best_failure_mode"],
    }


def build_record() -> dict[str, Any]:
    profile_rows = [solve_profile(spec) for spec in PROFILE_SPECS]
    candidates = []
    for spec, profile in zip(PROFILE_SPECS, profile_rows, strict=True):
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for seed in spec["seeds"]:
            candidates.append(evaluate_candidate(profile, seed))
    if candidates:
        best = max(
            candidates,
            key=lambda row: (
                row["best_proxy_nullity"],
                row["best_tree_variable_count"],
                min(row["pair7_counts"]),
                -row["max_pair_count"],
            ),
        )
    else:
        best = None
    proxy_positive = sum(1 for row in candidates if row["best_proxy_nullity"] > 0)
    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_tree_obstruction": source_obstruction(),
        "rank_feedback_search": {
            "systems_tested": len(candidates),
            "profile_systems_tested": len(PROFILE_SPECS),
            "rs_feasible_hypergraphs": len(candidates),
            "proxy_positive_nullity": proxy_positive,
            "exact_tree_audits": 0,
            "positive_exact_nullity": 0,
            "best_tree_variable_count": None if best is None else best["best_tree_variable_count"],
            "best_non_tree_equation_count": None if best is None else best["best_non_tree_equation_count"],
            "best_proxy_nullity": None if best is None else best["best_proxy_nullity"],
            "best_exact_nullity": None,
            "best_failure_mode": None if best is None else best["best_failure_mode"],
            "profiles": profile_rows,
            "candidates": [
                {key: value for key, value in row.items() if key != "coordinate_classes"}
                for row in candidates
            ],
        },
        "best_candidate": best,
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
        },
        "proof_status": "CANDIDATE / TREE_RANK_FEEDBACK_SCAN / PARTIAL / EXPERIMENTAL",
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
        search = record["rank_feedback_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "rs_feasible_hypergraphs": search["rs_feasible_hypergraphs"],
                    "proxy_positive_nullity": search["proxy_positive_nullity"],
                    "best_tree_variable_count": search["best_tree_variable_count"],
                    "best_non_tree_equation_count": search["best_non_tree_equation_count"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_RS_FEASIBLE_HYPERGRAPH_TREE_RANK_FEEDBACK_READY")


if __name__ == "__main__":
    main()
