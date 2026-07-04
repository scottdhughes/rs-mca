#!/usr/bin/env python3
"""Probe whether low-rank proxy kernels are common-kernel degeneracies."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "fc61a75"
LOWRANK_DATA = Path("experimental/data/m1_a327_lowrank_template_selected_class_search.json")
REPAIR_DATA = Path("experimental/data/m1_a327_lowrank_template_forced_identity_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_lowrank_common_kernel_degeneracy_probe.json")

P = 17
K = 256
TARGET_AGREEMENT = 327
LIST_SIZE = 7


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def rref(rows: list[list[int]], ncols: int, prime: int = P) -> tuple[list[list[int]], list[int]]:
    matrix = [[value % prime for value in row] for row in rows if any(value % prime for value in row)]
    pivots: list[int] = []
    rank = 0
    for col in range(ncols):
        pivot = None
        for row in range(rank, len(matrix)):
            if matrix[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][col] % prime:
                continue
            factor = matrix[row][col] % prime
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(matrix):
            break
    return matrix[:rank], pivots


def rank_mod_p(rows: list[list[int]], ncols: int, prime: int = P) -> int:
    return len(rref(rows, ncols=ncols, prime=prime)[0])


def nullspace_basis(rows: list[list[int]], ncols: int, prime: int = P) -> list[list[int]]:
    basis, pivots = rref(rows, ncols=ncols, prime=prime)
    pivot_set = set(pivots)
    free_cols = [col for col in range(ncols) if col not in pivot_set]
    result = []
    for free_col in free_cols:
        vector = [0] * ncols
        vector[free_col] = 1
        for basis_row, pivot in reversed(list(zip(basis, pivots, strict=True))):
            acc = 0
            for col in free_cols:
                acc = (acc + basis_row[col] * vector[col]) % prime
            vector[pivot] = (-acc) % prime
        result.append(vector)
    return result


def row_basis_mod_p(vectors: list[list[int]], members: list[int], prime: int = P) -> list[list[int]]:
    if len(members) <= 1:
        return []
    anchor = [value % prime for value in vectors[int(members[0]) - 1]]
    rows = []
    for witness in members[1:]:
        rows.append([(vectors[int(witness) - 1][idx] - anchor[idx]) % prime for idx in range(len(anchor))])
    basis, _pivots = rref(rows, ncols=len(anchor), prime=prime)
    return basis


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def resolve_candidates() -> list[dict[str, Any]]:
    lowrank = load_json(LOWRANK_DATA)
    repair = load_json(REPAIR_DATA)
    candidates = lowrank["lowrank_template_search"]["candidates"]

    lowrank_best_hash = lowrank["best_candidate"]["coordinate_classes_hash"]
    repair_best_hash = repair["best_candidate"]["coordinate_classes_hash"]
    wanted = [
        {
            "source_label": "mixed_rank6_proxy_positive",
            "coordinate_classes_hash": lowrank_best_hash,
            "template_id": lowrank["best_candidate"]["template_id"],
            "proxy_rank": lowrank["best_candidate"]["proxy_rank"],
            "proxy_nullity": lowrank["best_candidate"]["proxy_nullity"],
        },
        {
            "source_label": "random_matroid_seeded_0_m6_forced_identity_repair",
            "coordinate_classes_hash": repair_best_hash,
            "template_id": repair["best_candidate"]["template_id"],
            "proxy_rank": repair["best_candidate"]["proxy_rank"],
            "proxy_nullity": repair["best_candidate"]["proxy_nullity"],
        },
    ]
    resolved = []
    for spec in wanted:
        matches = [
            row for row in candidates
            if row.get("coordinate_classes_hash") == spec["coordinate_classes_hash"]
            and row.get("template_id") == spec["template_id"]
        ]
        if len(matches) != 1:
            raise RuntimeError(f"could not resolve {spec['source_label']}: {len(matches)} matches")
        row = dict(matches[0])
        row["source_label"] = spec["source_label"]
        row["proxy_rank"] = spec["proxy_rank"]
        row["proxy_nullity"] = spec["proxy_nullity"]
        resolved.append(row)
    return resolved


def connected_components(edges: list[tuple[int, int]]) -> list[list[int]]:
    graph = {idx: set() for idx in range(1, LIST_SIZE + 1)}
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    components = []
    seen = set()
    for start in range(1, LIST_SIZE + 1):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        component = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for nxt in sorted(graph[node]):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        components.append(sorted(component))
    return components


def candidate_probe(candidate: dict[str, Any]) -> dict[str, Any]:
    vectors = candidate["template_vectors"]
    ncols = int(candidate["template_dimension"])
    rows = []
    pair_counts = Counter()
    row_rank_hist = Counter()
    for coord in candidate["coordinate_classes"]:
        members = [int(value) for value in coord["members"]]
        for left_idx, left in enumerate(members):
            for right in members[left_idx + 1:]:
                pair_counts[f"P{left}{right}"] += 1
        basis = row_basis_mod_p(vectors, members)
        row_rank_hist[str(len(basis))] += 1
        rows.extend(basis)
    span_rank = rank_mod_p(rows, ncols=ncols)
    common_kernel = nullspace_basis(rows, ncols=ncols)
    pair_projection_ranks = {}
    forced_pairs = []
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            diff = [
                (int(vectors[left - 1][idx]) - int(vectors[right - 1][idx])) % P
                for idx in range(ncols)
            ]
            values = [
                sum(diff[idx] * kernel_vec[idx] for idx in range(ncols)) % P
                for kernel_vec in common_kernel
            ]
            rank = 1 if any(values) else 0
            label = f"P{left}{right}"
            pair_projection_ranks[label] = rank
            if rank == 0:
                forced_pairs.append([left, right])
    cooccurrence_edges = []
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            if pair_counts[f"P{left}{right}"] > 0:
                cooccurrence_edges.append((left, right))
    components = connected_components(cooccurrence_edges)
    expected_rank = span_rank * K
    expected_nullity = (ncols - span_rank) * K
    artifact_match = (
        int(candidate["proxy_rank"]) == expected_rank
        and int(candidate["proxy_nullity"]) == expected_nullity
    )
    connected = len(components) == 1
    all_pairs_forced_on_common_kernel = len(forced_pairs) == 21
    degeneracy = artifact_match and connected and all_pairs_forced_on_common_kernel
    return {
        "source_label": candidate["source_label"],
        "template_id": candidate["template_id"],
        "template_family": candidate["template_family"],
        "template_dimension": ncols,
        "assignment_strategy": candidate["assignment_strategy"],
        "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        "support_vector": candidate["support_vector"],
        "max_pair_count": candidate["max_pair_count"],
        "pair7_counts": candidate["pair7_counts"],
        "raw_constraint_rows": len(rows),
        "row_rank_histogram": dict(sorted(row_rank_hist.items(), key=lambda item: int(item[0]))),
        "functional_span_rank": span_rank,
        "common_kernel_dimension": len(common_kernel),
        "common_kernel_basis": common_kernel,
        "proxy_rank": candidate["proxy_rank"],
        "proxy_nullity": candidate["proxy_nullity"],
        "expected_common_kernel_artifact_rank": expected_rank,
        "expected_common_kernel_artifact_nullity": expected_nullity,
        "common_kernel_artifact_rank_match": artifact_match,
        "cooccurrence_graph_connected": connected,
        "cooccurrence_components": components,
        "cooccurrence_edges": [[left, right] for left, right in cooccurrence_edges],
        "pair_projection_rank_on_common_kernel": pair_projection_ranks,
        "forced_equal_pairs_on_common_kernel": forced_pairs,
        "all_pairs_forced_on_common_kernel": all_pairs_forced_on_common_kernel,
        "degeneracy_detected": degeneracy,
        "failure_mode": "LOWRANK_TEMPLATE_COMMON_KERNEL_DEGENERACY" if degeneracy else "LOWRANK_TEMPLATE_SPAN_NOT_DEGENERATE",
        "ledger_hashes": {
            "coordinate_classes_hash": hash_payload(candidate["coordinate_classes"]),
            "template_vectors_hash": hash_payload(candidate["template_vectors"]),
            "common_kernel_basis_hash": hash_payload(common_kernel),
            "pair_projection_hash": hash_payload(pair_projection_ranks),
        },
    }


def build_record() -> dict[str, Any]:
    probes = [candidate_probe(candidate) for candidate in resolve_candidates()]
    all_degenerate = all(row["degeneracy_detected"] for row in probes)
    status = (
        "EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_COMMON_KERNEL_DEGENERACY / PARTIAL / EXPERIMENTAL"
        if all_degenerate
        else "CANDIDATE / LOWRANK_TEMPLATE_SPAN_NOT_DEGENERATE / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "source_artifacts": {
            "lowrank_selected_class_search": str(LOWRANK_DATA),
            "forced_identity_repair": str(REPAIR_DATA),
        },
        "probe": {
            "field_basis": "GF(17) template rows embedded in GF(17^32)",
            "degree_bound": K,
            "candidates_tested": len(probes),
            "degenerate_candidates": sum(1 for row in probes if row["degeneracy_detected"]),
            "best_failure_mode": "LOWRANK_TEMPLATE_COMMON_KERNEL_DEGENERACY" if all_degenerate else "LOWRANK_TEMPLATE_SPAN_NOT_DEGENERATE",
        },
        "candidate_probes": probes,
        "proof_status": status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "global obstruction outside the tested low-rank templates",
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
    summary = {
        "proof_status": record["proof_status"],
        "candidates_tested": record["probe"]["candidates_tested"],
        "degenerate_candidates": record["probe"]["degenerate_candidates"],
        "candidates": [
            {
                "source_label": row["source_label"],
                "template_id": row["template_id"],
                "span_rank": row["functional_span_rank"],
                "kernel_dim": row["common_kernel_dimension"],
                "proxy_rank": row["proxy_rank"],
                "proxy_nullity": row["proxy_nullity"],
                "artifact_match": row["common_kernel_artifact_rank_match"],
                "connected": row["cooccurrence_graph_connected"],
                "forced_pairs": len(row["forced_equal_pairs_on_common_kernel"]),
                "failure_mode": row["failure_mode"],
            }
            for row in record["candidate_probes"]
        ],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_LOWRANK_COMMON_KERNEL_DEGENERACY_PROBE_READY")


if __name__ == "__main__":
    main()
