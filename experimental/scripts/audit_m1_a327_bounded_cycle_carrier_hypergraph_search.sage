#!/usr/bin/env sage
"""Exact GF(17^32) edge-divisibility audit for bounded-cycle carriers."""

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
TARGET_AGREEMENT = 327
DATA_PATH = Path("experimental/data/m1_a327_bounded_cycle_carrier_hypergraph_search.json")


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


def edge_label(edge):
    left, right = sorted((int(edge[0]), int(edge[1])))
    return "P%s%s" % (left, right)


def parse_edge_label(label):
    return int(label[1]), int(label[2])


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def pair_indices():
    return [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]


def carrier_spanning_tree(edges):
    adjacency = {node: [] for node in range(1, LIST_SIZE + 1)}
    for edge in edges:
        left, right = int(edge[0]), int(edge[1])
        adjacency[left].append(right)
        adjacency[right].append(left)
    parent = {1: None}
    tree_edges = []
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in sorted(adjacency[node]):
            if neighbor in parent:
                continue
            parent[neighbor] = node
            tree_edges.append([node, neighbor])
            queue.append(neighbor)
    if len(parent) != LIST_SIZE:
        raise RuntimeError("carrier graph disconnected")
    tree_labels = {edge_label(edge) for edge in tree_edges}
    non_tree = [edge for edge in edges if edge_label(edge) not in tree_labels]
    return tree_edges, non_tree


def path_edges(tree_edges, start, finish):
    adjacency = {node: [] for node in range(1, LIST_SIZE + 1)}
    for edge in tree_edges:
        left, right = int(edge[0]), int(edge[1])
        adjacency[left].append(right)
        adjacency[right].append(left)
    parent = {int(start): None}
    queue = deque([int(start)])
    while queue:
        node = queue.popleft()
        if node == int(finish):
            break
        for neighbor in adjacency[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    if int(finish) not in parent:
        raise RuntimeError("no path in tree")
    path = []
    node = int(finish)
    while node != int(start):
        previous = parent[node]
        label = edge_label([previous, node])
        left, right = parse_edge_label(label)
        sign = 1 if previous == left and node == right else -1
        path.append((label, sign))
        node = previous
    return path[::-1]


def root_path_coeffs(tree_edges):
    out = {1: {}}
    for node in range(2, LIST_SIZE + 1):
        coeffs = {}
        for label, sign in path_edges(tree_edges, 1, node):
            coeffs[label] = coeffs.get(label, 0) + sign
        out[node] = {label: value for label, value in coeffs.items() if value}
    return out


def pair_path_coeffs(path_coeffs, left, right):
    coeffs = {}
    for label, value in path_coeffs[int(right)].items():
        coeffs[label] = coeffs.get(label, 0) + value
    for label, value in path_coeffs[int(left)].items():
        coeffs[label] = coeffs.get(label, 0) - value
    return {label: value for label, value in coeffs.items() if value}


def edge_zero_sets(coordinate_classes, edge_labels):
    out = {label: [] for label in edge_labels}
    for row in coordinate_classes:
        pos = int(row["position"])
        for label in row["edge_labels"]:
            if label in out:
                out[label].append(pos)
    return out


def z_polynomials(F, H, edge_sets):
    R = PolynomialRing(F, "x")
    x = R.gen()
    out = {}
    for label, positions in edge_sets.items():
        poly = R(1)
        for pos in positions:
            poly *= x - H[int(pos)]
        coeffs = [F(value) for value in poly.list()]
        out[label] = {
            "degree": int(poly.degree()),
            "coeffs": coeffs,
            "poly_hash": hash_payload([str(value) for value in coeffs]),
        }
    return out


def variable_blocks(edge_loads, edge_labels):
    blocks = {}
    cursor = 0
    for label in edge_labels:
        qdeg = K - int(edge_loads[label])
        if qdeg <= 0:
            raise RuntimeError("nonpositive quotient degree for %s" % label)
        blocks[label] = {
            "start": cursor,
            "q_degree_bound": qdeg,
            "edge_load": int(edge_loads[label]),
        }
        cursor += qdeg
    return blocks, cursor


def add_polynomial_to_row(F, entries, row_index, sign_int, label, blocks, z):
    sign = F(sign_int)
    block = blocks[label]
    start = block["start"]
    z_coeffs = z[label]["coeffs"]
    for q_degree in range(block["q_degree_bound"]):
        target_degree = row_index["degree_offset"] + q_degree
        for z_degree, z_coeff in enumerate(z_coeffs):
            degree = q_degree + z_degree
            if degree != row_index["degree"]:
                continue
            column = start + q_degree
            key = (row_index["row"], column)
            entries[key] = entries.get(key, F(0)) + sign * z_coeff


def build_cycle_matrix(F, carrier_edges, tree_edges, non_tree_edges, edge_loads, z):
    edge_labels = [edge_label(edge) for edge in carrier_edges]
    blocks, ncols = variable_blocks(edge_loads, edge_labels)
    entries = {}
    row = 0
    for edge in non_tree_edges:
        left, right = parse_edge_label(edge_label(edge))
        cycle_terms = [(edge_label(edge), 1)]
        for label, sign in path_edges(tree_edges, left, right):
            cycle_terms.append((label, -sign))
        for degree in range(K):
            for label, sign_int in cycle_terms:
                block = blocks[label]
                z_coeffs = z[label]["coeffs"]
                start = block["start"]
                for q_degree in range(block["q_degree_bound"]):
                    z_degree = degree - q_degree
                    if 0 <= z_degree < len(z_coeffs):
                        key = (row, start + q_degree)
                        entries[key] = entries.get(key, F(0)) + F(sign_int) * z_coeffs[z_degree]
            row += 1
    return Matrix(F, row, ncols, entries, sparse=True), blocks


def edge_polynomial_coeffs(F, vector_row, label, block, z):
    coeffs = [F(0) for _ in range(K)]
    start = block["start"]
    z_coeffs = z[label]["coeffs"]
    for q_degree in range(block["q_degree_bound"]):
        q_coeff = vector_row[start + q_degree]
        if q_coeff == 0:
            continue
        for z_degree, z_coeff in enumerate(z_coeffs):
            coeffs[q_degree + z_degree] += q_coeff * z_coeff
    return coeffs


def pair_polynomial_coeffs(F, vector_row, pair, blocks, path_coeffs, z):
    coeffs = [F(0) for _ in range(K)]
    for label, sign_int in pair_path_coeffs(path_coeffs, pair[0], pair[1]).items():
        edge_coeffs = edge_polynomial_coeffs(F, vector_row, label, blocks[label], z)
        for degree in range(K):
            coeffs[degree] += F(sign_int) * edge_coeffs[degree]
    return coeffs


def pair_projection_test(F, basis, blocks, path_coeffs, z, exact_rank_limit=256):
    projection_rank_by_pair = {}
    forced_equal_pairs = []
    exact_ranks = len(basis) <= exact_rank_limit
    for left, right in pair_indices():
        label = edge_label([left, right])
        rows = []
        has_nonzero = False
        for vector_row in basis:
            coeffs = pair_polynomial_coeffs(F, vector_row, [left, right], blocks, path_coeffs, z)
            if any(value != 0 for value in coeffs):
                has_nonzero = True
            if exact_ranks:
                rows.append(coeffs)
        rank = int(Matrix(F, rows).rank()) if exact_ranks and rows else (1 if has_nonzero else 0)
        projection_rank_by_pair[label] = rank
        if rank == 0:
            forced_equal_pairs.append([left, right])
    return {
        "forced_equal_pairs": forced_equal_pairs,
        "min_projection_rank": min(projection_rank_by_pair.values()) if projection_rank_by_pair else None,
        "projection_rank_by_pair": projection_rank_by_pair,
    }


def codeword_coefficients(F, vector_row, blocks, path_coeffs, z):
    edge_cache = {
        label: edge_polynomial_coeffs(F, vector_row, label, block, z)
        for label, block in blocks.items()
    }
    codewords = [[F(0) for _ in range(K)] for _ in range(LIST_SIZE)]
    for witness in range(2, LIST_SIZE + 1):
        for label, sign_int in path_coeffs[witness].items():
            for degree in range(K):
                codewords[witness - 1][degree] += F(sign_int) * edge_cache[label][degree]
    return codewords


def evaluate_candidate(F, H, vector_row, blocks, path_coeffs, z, coordinate_classes):
    coeffs = codeword_coefficients(F, vector_row, blocks, path_coeffs, z)
    values = []
    for witness in range(LIST_SIZE):
        witness_values = []
        for x_value in H:
            acc = F(0)
            power = F(1)
            for degree in range(K):
                acc += coeffs[witness][degree] * power
                power *= x_value
            witness_values.append(acc)
        values.append(witness_values)
    r_values = []
    for row in coordinate_classes:
        pos = int(row["position"])
        anchor = min(int(value) for value in row["members"])
        r_values.append(values[anchor - 1][pos])
    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [hash_payload([str(value) for value in row]) for row in coeffs]
    return {
        "agreement_vector": agreements,
        "seven_distinct": len(set(codeword_hashes)) == LIST_SIZE,
        "codeword_hashes": codeword_hashes,
        "received_word_hash": hash_payload([str(value) for value in r_values]),
    }


def deterministic_candidates(F, basis, sample_limit):
    if not basis or sample_limit <= 0:
        return []
    parent = basis[0].parent()
    generator = F.multiplicative_generator()
    candidates = []
    candidates.extend(basis[: min(len(basis), sample_limit)])
    if len(candidates) < sample_limit:
        acc = parent.zero()
        for row in basis:
            acc += row
        candidates.append(acc)
    idx = 1
    while len(candidates) < sample_limit:
        acc = parent.zero()
        for basis_idx, row in enumerate(basis):
            acc += (generator ** ((idx + 1) * (basis_idx + 1))) * row
        candidates.append(acc)
        idx += 1
    return candidates[:sample_limit]


def audit(sample_limit=24):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    search = record["bounded_cycle_search"]
    if not search["coordinate_classes"]:
        record["exact_edge_lift"]["best_failure_mode"] = "BOUNDED_CYCLE_COUNT_INFEASIBLE"
        record["proof_status"] = "CONSTRUCTION_FAIL / BOUNDED_CYCLE_COUNT_INFEASIBLE / PARTIAL / EXPERIMENTAL"
        return record

    q, F, H = field_context()
    carrier_edges = search["best_graph_edges"]
    edge_labels = [edge_label(edge) for edge in carrier_edges]
    edge_loads = search["best_edge_loads"]
    coordinate_classes = search["coordinate_classes"]
    edge_sets = edge_zero_sets(coordinate_classes, edge_labels)
    z = z_polynomials(F, H, edge_sets)
    tree_edges, non_tree_edges = carrier_spanning_tree(carrier_edges)
    matrix, blocks = build_cycle_matrix(F, carrier_edges, tree_edges, non_tree_edges, edge_loads, z)
    rank = int(matrix.rank())
    nullity = int(matrix.ncols() - rank)

    record["bounded_cycle_search"]["exact_lift_attempts"] = 1
    record["exact_edge_lift"].update(
        {
            "field": "GF(17^32)",
            "field_denominator": "17^32",
            "H_order": len(H),
            "carrier_spanning_tree_edges": tree_edges,
            "non_tree_edges": non_tree_edges,
            "edge_zero_set_sizes": {label: len(values) for label, values in edge_sets.items()},
            "edge_polynomial_degrees": {label: int(z[label]["degree"]) for label in edge_labels},
            "edge_polynomial_hashes": {label: z[label]["poly_hash"] for label in edge_labels},
            "edge_variable_count": int(matrix.ncols()),
            "cycle_constraint_count": int(matrix.nrows()),
            "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
            "rank": rank,
            "nullity": nullity,
        }
    )

    if nullity == 0:
        record["exact_edge_lift"]["best_failure_mode"] = "BOUNDED_CYCLE_EXACT_NULLITY_ZERO"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / BOUNDED_CYCLE_EXACT_NULLITY_ZERO / PARTIAL / EXPERIMENTAL"
        return record

    basis = matrix.right_kernel().basis()
    path_coeffs = root_path_coeffs(tree_edges)
    projection = pair_projection_test(F, basis, blocks, path_coeffs, z)
    record["exact_edge_lift"].update(projection)
    if projection["forced_equal_pairs"]:
        record["exact_edge_lift"]["best_failure_mode"] = "BOUNDED_CYCLE_FORCED_PAIR_EQUALITY"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / BOUNDED_CYCLE_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        return record

    for candidate in deterministic_candidates(F, basis, sample_limit):
        evaluated = evaluate_candidate(F, H, candidate, blocks, path_coeffs, z, coordinate_classes)
        if evaluated["seven_distinct"] and min(evaluated["agreement_vector"]) >= TARGET_AGREEMENT:
            record["exact_edge_lift"].update(
                {
                    "seven_distinct": True,
                    "agreement_vector": evaluated["agreement_vector"],
                    "received_word_hash": evaluated["received_word_hash"],
                    "codeword_hashes": evaluated["codeword_hashes"],
                    "best_failure_mode": "BOUNDED_CYCLE_EXACT_CANDIDATE",
                }
            )
            record["proof_status"] = "PROOF_RECORD / BOUNDED_CYCLE_EXACT_CANDIDATE / EXPERIMENTAL"
            return record

    record["exact_edge_lift"]["best_failure_mode"] = "BOUNDED_CYCLE_FORCED_PAIR_EQUALITY"
    record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / BOUNDED_CYCLE_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=24)
    args = parser.parse_args()
    record = audit(sample_limit=args.sample_limit)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        exact = record["exact_edge_lift"]
        print("SAGE_AUDIT_M1_A327_BOUNDED_CYCLE_CARRIER_HYPERGRAPH_SEARCH_OK")
        print("matrix_shape: %s" % exact["matrix_shape"])
        print("rank: %s" % exact["rank"])
        print("nullity: %s" % exact["nullity"])
        print("best_failure_mode: %s" % exact["best_failure_mode"])


if __name__ == "__main__":
    main()
