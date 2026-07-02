#!/usr/bin/env sage
"""Exact GF(17^32) tree-rank audit for rank-feedback hypergraph candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
DATA_PATH = Path("experimental/data/m1_a327_rs_feasible_hypergraph_tree_rank_feedback.json")


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    try:
        if hasattr(payload, "__float__"):
            return float(payload)
    except Exception:
        pass
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def pair_label(left, right):
    left, right = sorted((int(left), int(right)))
    return "P%s%s" % (left, right)


def parse_pair_label(label):
    return int(label[1]), int(label[2])


def pair_sets(coordinate_classes):
    labels = ["P%s%s" % (i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
    sets = {label: [] for label in labels}
    for row in coordinate_classes:
        position = int(row["position"])
        members = set(int(value) for value in row["members"])
        for i in range(1, LIST_SIZE + 1):
            for j in range(i + 1, LIST_SIZE + 1):
                if i in members and j in members:
                    sets["P%s%s" % (i, j)].append(position)
    return sets


def orient_tree(edges):
    adjacency = {node: [] for node in range(1, LIST_SIZE + 1)}
    for left, right in edges:
        left = int(left)
        right = int(right)
        adjacency[left].append(right)
        adjacency[right].append(left)
    parent = {1: None}
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor in parent:
                continue
            parent[neighbor] = node
            queue.append(neighbor)
    if len(parent) != LIST_SIZE:
        raise RuntimeError("tree is not connected")
    paths = {1: {}}
    for node in range(2, LIST_SIZE + 1):
        coeffs = {}
        current = node
        while current != 1:
            previous = parent[current]
            label = pair_label(previous, current)
            coeffs[label] = coeffs.get(label, 0) + 1
            current = previous
        paths[node] = coeffs
    return paths


def path_coeffs(paths, left, right):
    coeffs = {}
    for label, value in paths[int(left)].items():
        coeffs[label] = coeffs.get(label, 0) + value
    for label, value in paths[int(right)].items():
        coeffs[label] = coeffs.get(label, 0) - value
    return {label: value for label, value in coeffs.items() if value}


def z_evals(F, H, pair_sets_, tree_labels):
    out = {}
    R = PolynomialRing(F, "x")
    x = R.gen()
    for label in tree_labels:
        poly = R(1)
        for pos in pair_sets_[label]:
            poly *= x - H[int(pos)]
        out[label] = {
            "degree": int(poly.degree()),
            "evals": [poly(value) for value in H],
            "poly_hash": hash_payload([str(value) for value in poly.list()]),
        }
    return out


def build_matrix(F, H, powers, pair_sets_, tree_edges, pair_counts):
    tree_labels = [pair_label(edge[0], edge[1]) for edge in tree_edges]
    blocks = {}
    cursor = 0
    for label in tree_labels:
        qdeg = K - int(pair_counts[label])
        blocks[label] = {"start": cursor, "q_degree_bound": qdeg, "pair_count": int(pair_counts[label])}
        cursor += qdeg
    paths = orient_tree(tree_edges)
    z = z_evals(F, H, pair_sets_, tree_labels)
    entries = {}
    row_index = 0
    non_tree_labels = [label for label in pair_sets_ if label not in set(tree_labels)]
    for non_tree_label in non_tree_labels:
        left, right = parse_pair_label(non_tree_label)
        path = path_coeffs(paths, left, right)
        for pos in pair_sets_[non_tree_label]:
            pos = int(pos)
            for label, sign_int in path.items():
                z_value = z[label]["evals"][pos]
                if z_value == 0:
                    continue
                block = blocks[label]
                start = block["start"]
                sign = F(sign_int)
                for degree in range(block["q_degree_bound"]):
                    entries[(row_index, start + degree)] = (
                        entries.get((row_index, start + degree), F(0))
                        + sign * z_value * powers[degree][pos]
                    )
            row_index += 1
    return Matrix(F, row_index, cursor, entries, sparse=True), blocks, z


def audit():
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    candidate = record["best_candidate"]
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    sets = pair_sets(candidate["coordinate_classes"])
    counts = {label: len(values) for label, values in sets.items()}
    matrix, blocks, z = build_matrix(F, H, powers, sets, candidate["best_tree_edges"], counts)
    rank = int(matrix.rank())
    nrows, ncols = int(matrix.nrows()), int(matrix.ncols())
    nullity = ncols - rank
    failure_mode = (
        "RANK_FEEDBACK_EXACT_NULLITY_ZERO"
        if nullity == 0
        else "TREE_PROXY_NULLITY_POSITIVE"
    )
    exact = {
        "run": True,
        "field": "GF(17^32)",
        "field_denominator": str(q),
        "H_order": len(H),
        "profile_id": candidate["profile_id"],
        "assignment_seed": candidate["assignment_seed"],
        "tree_name": candidate["best_tree_name"],
        "tree_edges": candidate["best_tree_edges"],
        "matrix_shape": [nrows, ncols],
        "rank": rank,
        "nullity": nullity,
        "tree_variable_blocks": blocks,
        "tree_z_hashes": {label: z[label]["poly_hash"] for label in z},
        "best_failure_mode": failure_mode,
    }
    record["exact_tree_audit"] = jsonable(exact)
    record["rank_feedback_search"]["exact_tree_audits"] = 1
    record["rank_feedback_search"]["positive_exact_nullity"] = 1 if nullity > 0 else 0
    record["rank_feedback_search"]["best_exact_nullity"] = nullity
    record["rank_feedback_search"]["best_failure_mode"] = failure_mode
    record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / %s / PARTIAL / EXPERIMENTAL" % failure_mode
    return jsonable(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = audit()
    if args.write_json:
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        exact = record["exact_tree_audit"]
        print("SAGE_AUDIT_M1_A327_RS_FEASIBLE_HYPERGRAPH_TREE_RANK_FEEDBACK_OK")
        print("matrix_shape: %s" % exact["matrix_shape"])
        print("rank: %s" % exact["rank"])
        print("nullity: %s" % exact["nullity"])
        print("best_failure_mode: %s" % exact["best_failure_mode"])


if __name__ == "__main__":
    main()
