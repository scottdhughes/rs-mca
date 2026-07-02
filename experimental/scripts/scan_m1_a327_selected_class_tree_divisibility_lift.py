#!/usr/bin/env python3
"""Prepare tree-divisibility lift targets for the M1 a=327 selected classes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "016f04d"
SOURCE_DATA = Path("experimental/data/m1_a327_selected_class_quotient_nullspace_lift.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_selected_class_tree_divisibility_lift.json")

N = 512
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]
PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def pair_sets(coordinate_classes: list[dict[str, Any]]) -> dict[str, list[int]]:
    sets = {label: [] for label in PAIR_LABELS}
    for row in coordinate_classes:
        position = int(row["position"])
        members = {int(value) for value in row["members"]}
        for label, (left, right) in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if left in members and right in members:
                sets[label].append(position)
    return sets


def edge_label(edge: tuple[int, int] | list[int]) -> str:
    left, right = sorted((int(edge[0]), int(edge[1])))
    return f"P{left}{right}"


def all_edges(pair_counts: dict[str, int]) -> list[tuple[int, int, int]]:
    edges = []
    for left, right in PAIR_INDICES:
        label = f"P{left}{right}"
        edges.append((left, right, int(pair_counts[label])))
    return edges


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n + 1))

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


def kruskal_tree(pair_counts: dict[str, int], edge_order: list[tuple[int, int, int]]) -> list[list[int]]:
    dsu = DSU(LIST_SIZE)
    tree = []
    for left, right, _weight in edge_order:
        if dsu.union(left, right):
            tree.append([left, right])
        if len(tree) == LIST_SIZE - 1:
            break
    if len(tree) != LIST_SIZE - 1:
        raise RuntimeError("failed to build spanning tree")
    return tree


def candidate_trees(pair_counts: dict[str, int]) -> list[dict[str, Any]]:
    edges = all_edges(pair_counts)
    max_weight_order = sorted(edges, key=lambda row: (-row[2], row[0] != 1, row[0], row[1]))
    pair7_order = sorted(edges, key=lambda row: (row[1] != 7, -row[2], row[0], row[1]))
    balanced_order = sorted(edges, key=lambda row: (-row[2], abs(row[0] - row[1]), row[0], row[1]))
    raw = [
        ("max_weight_tree", kruskal_tree(pair_counts, max_weight_order)),
        ("pair7_heavy_tree", kruskal_tree(pair_counts, pair7_order)),
        ("balanced_tree", kruskal_tree(pair_counts, balanced_order)),
    ]
    seen = set()
    out = []
    for name, tree_edges in raw:
        canonical = sorted([sorted(edge) for edge in tree_edges])
        key = tuple(tuple(edge) for edge in canonical)
        if key in seen:
            continue
        seen.add(key)
        tree_labels = [edge_label(edge) for edge in canonical]
        tree_weight = sum(pair_counts[label] for label in tree_labels)
        tree_variables = sum(K - pair_counts[label] for label in tree_labels)
        non_tree_labels = [label for label in PAIR_LABELS if label not in set(tree_labels)]
        non_tree_equations = sum(pair_counts[label] for label in non_tree_labels)
        out.append(
            {
                "tree_name": name,
                "edges": canonical,
                "edge_labels": tree_labels,
                "total_weight": tree_weight,
                "tree_variable_count": tree_variables,
                "non_tree_edge_labels": non_tree_labels,
                "non_tree_equation_count": non_tree_equations,
            }
        )
    return out


def support_counts(coordinate_classes: list[dict[str, Any]]) -> list[int]:
    supports = [0] * LIST_SIZE
    for row in coordinate_classes:
        for witness in row["members"]:
            supports[int(witness) - 1] += 1
    return supports


def build_record() -> dict[str, Any]:
    source = load_source()
    thin = source["thin_selected_hypergraph"]
    coordinate_classes = thin["coordinate_classes"]
    sets = pair_sets(coordinate_classes)
    counts = {label: len(values) for label, values in sets.items()}
    trees = candidate_trees(counts)
    best = min(trees, key=lambda row: (row["tree_variable_count"], -row["total_weight"], row["tree_name"]))
    pair7_counts = [counts[label] for label in PAIR7_PAIR_LABELS]

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "thin_selected_hypergraph": {
            "supports": support_counts(coordinate_classes),
            "selected_incidences": thin["selected_incidences"],
            "max_pair_count": max(counts.values()),
            "pair_counts": counts,
            "pair_sets": sets,
            "pair_sets_hash": hash_payload(sets),
            "pair7_counts": pair7_counts,
            "coordinate_classes_hash": thin["coordinate_classes_hash"],
        },
        "tree_divisibility": {
            "trees_tested": trees,
            "best_tree_name": best["tree_name"],
            "best_tree_edges": best["edges"],
            "best_tree_edge_labels": best["edge_labels"],
            "tree_variable_count": best["tree_variable_count"],
            "non_tree_equation_count": best["non_tree_equation_count"],
            "matrix_shape": [best["non_tree_equation_count"], best["tree_variable_count"]],
            "rank": None,
            "nullity": None,
            "best_failure_mode": None,
            "field": None,
            "field_denominator": None,
            "H_order": None,
        },
        "pair_projection_test": {
            "pairs_tested": 21,
            "forced_equal_pairs": [],
            "min_projection_rank": None,
            "projection_rank_by_pair": None,
        },
        "exact_candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
            "vector_hash": None,
        },
        "proof_status": "CANDIDATE / TREE_DIVISIBILITY_PENDING / PARTIAL / EXPERIMENTAL",
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        summary = {
            "status": record["proof_status"],
            "supports": record["thin_selected_hypergraph"]["supports"],
            "max_pair_count": record["thin_selected_hypergraph"]["max_pair_count"],
            "pair7_counts": record["thin_selected_hypergraph"]["pair7_counts"],
            "best_tree_name": record["tree_divisibility"]["best_tree_name"],
            "best_tree_edges": record["tree_divisibility"]["best_tree_edges"],
            "matrix_shape": record["tree_divisibility"]["matrix_shape"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_SELECTED_CLASS_TREE_DIVISIBILITY_LIFT_READY")


if __name__ == "__main__":
    main()
