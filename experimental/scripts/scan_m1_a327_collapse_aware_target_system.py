#!/usr/bin/env python3
"""Collapse-aware target-system search for the M1 a=327 proxy obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_robust_proxy_constrained_extraction as robust
import scan_m1_a327_joint_target_codeword_solver as joint


ROBUST_DATA = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
SOURCE_DATA = Path("experimental/data/m1_a327_residual_degeneracy_separation.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_collapse_aware_target_system.json")

N = joint.N
K = joint.K
LIST_SIZE = joint.LIST_SIZE
DIFF_COUNT = LIST_SIZE - 1
VARIABLE_COUNT = joint.VARIABLE_COUNT
TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
SOURCE_COMMIT = "3d12ee1"
COLLAPSE_CLASS = [1, 3, 4, 5, 6, 7]
SAMPLES_PER_SYSTEM = 8

PARTITIONS = [
    ("split_334_567", [[1, 3, 4], [5, 6, 7]]),
    ("split_13_4567", [[1, 3], [4, 5, 6, 7]]),
    ("split_13_45_67", [[1, 3], [4, 5], [6, 7]]),
]
SPLIT_BUDGETS = [8, 16, 32]
SYSTEM_LIMIT = 3


def jsonable(payload: Any) -> Any:
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def one_based_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(LIST_SIZE) if int(mask) & (1 << idx)]


def coord_split_score(coord: dict[str, Any]) -> tuple[int, int, int]:
    members = set(one_based_members(coord["mask"]))
    overlap = len(members.intersection(COLLAPSE_CLASS))
    return (overlap, coord["size"], -coord["position"])


def split_coordinates(selected: list[dict[str, Any]], budget: int) -> list[int]:
    candidates = [
        coord for coord in selected
        if len(set(one_based_members(coord["mask"])).intersection(COLLAPSE_CLASS)) >= 4
    ]
    candidates.sort(key=coord_split_score, reverse=True)
    output = []
    used_fibers = set()
    for coord in candidates:
        if coord["fiber"] in used_fibers:
            continue
        output.append(coord["position"])
        used_fibers.add(coord["fiber"])
        if len(output) >= budget:
            return output
    for coord in candidates:
        if coord["position"] in output:
            continue
        output.append(coord["position"])
        if len(output) >= budget:
            break
    return output


def add_equality_row(rows: list[list[int]], rhs: list[int], powers: np.ndarray, pos: int, left: int, right: int, value: int, p: int) -> None:
    row = np.zeros(VARIABLE_COUNT, dtype=np.int64)
    if left != 1:
        start = (left - 2) * K
        row[start:start + K] = (row[start:start + K] + powers[pos]) % p
    if right != 1:
        start = (right - 2) * K
        row[start:start + K] = (row[start:start + K] - powers[pos]) % p
    rows.append(row.tolist())
    rhs.append(int(value) % p)


def add_mask_rows(rows: list[list[int]], rhs: list[int], powers: np.ndarray, pos: int, mask: int, p: int) -> None:
    members = one_based_members(mask)
    if 1 in members:
        for witness in members:
            if witness == 1:
                continue
            add_equality_row(rows, rhs, powers, pos, witness, 1, 0, p)
        return
    if len(members) < 2:
        return
    left = members[0]
    for witness in members[1:]:
        add_equality_row(rows, rhs, powers, pos, left, witness, 0, p)


def add_partition_rows(
    rows: list[list[int]],
    rhs: list[int],
    powers: np.ndarray,
    pos: int,
    partition: list[list[int]],
    p: int,
    gamma: int,
) -> None:
    for group in partition:
        if len(group) < 2:
            continue
        left = group[0]
        for witness in group[1:]:
            add_equality_row(rows, rhs, powers, pos, left, witness, 0, p)
    if len(partition) >= 2:
        add_equality_row(rows, rhs, powers, pos, partition[0][0], partition[1][0], gamma, p)
    if len(partition) >= 3:
        add_equality_row(rows, rhs, powers, pos, partition[1][0], partition[2][0], gamma + 1, p)


def target_rows_for_modified(selected: list[dict[str, Any]], split_positions: set[int], partition: list[list[int]], p: int):
    powers = robust.proxy.vandermonde_powers_modp(p)
    rows: list[list[int]] = []
    rhs: list[int] = []
    split_count = 0
    for coord in selected:
        if coord["position"] in split_positions:
            split_count += 1
            gamma = 1 + (coord["position"] % (p - 2))
            add_partition_rows(rows, rhs, powers, coord["position"], partition, p, gamma)
        else:
            add_mask_rows(rows, rhs, powers, coord["position"], coord["mask"], p)
    return np.array(rows, dtype=np.int64) % p, np.array(rhs, dtype=np.int64) % p, split_count


def affine_echelon(matrix: np.ndarray, rhs: np.ndarray, p: int):
    mat = np.array(matrix, dtype=np.int64, copy=True) % p
    b = np.array(rhs, dtype=np.int64, copy=True) % p
    row_count, col_count = mat.shape
    rank = 0
    pivots: list[int] = []
    for col in range(col_count):
        pivot_candidates = np.nonzero(mat[rank:, col] % p)[0]
        if len(pivot_candidates) == 0:
            continue
        pivot = rank + int(pivot_candidates[0])
        if pivot != rank:
            mat[[rank, pivot]] = mat[[pivot, rank]]
            b[[rank, pivot]] = b[[pivot, rank]]
        inv = pow(int(mat[rank, col]), p - 2, p)
        mat[rank] = (mat[rank] * inv) % p
        b[rank] = (b[rank] * inv) % p
        below = np.nonzero(mat[rank + 1:, col] % p)[0]
        for offset in below:
            row = rank + 1 + int(offset)
            factor = int(mat[row, col])
            mat[row] = (mat[row] - factor * mat[rank]) % p
            b[row] = (b[row] - factor * b[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == row_count:
            break
    for row in range(rank, row_count):
        if not np.any(mat[row] % p) and int(b[row] % p) != 0:
            return None, None, None, "INCONSISTENT"
    return mat[:rank], b[:rank], pivots, "OK"


def vector_from_free(echelon: np.ndarray, rhs: np.ndarray, pivots: list[int], assignments: dict[int, int], p: int) -> np.ndarray:
    vector = np.zeros(VARIABLE_COUNT, dtype=np.int64)
    for col, value in assignments.items():
        vector[int(col)] = int(value) % p
    for row_idx in range(len(pivots) - 1, -1, -1):
        pivot = pivots[row_idx]
        total = int(np.dot(echelon[row_idx], vector) % p)
        vector[pivot] = (int(rhs[row_idx]) - total) % p
    return vector % p


def sample_vectors(echelon: np.ndarray, rhs: np.ndarray, pivots: list[int], seed: int, p: int) -> list[np.ndarray]:
    pivot_set = set(pivots)
    free_cols = [col for col in range(VARIABLE_COUNT) if col not in pivot_set]
    rng = random.Random(seed)
    schedules: list[dict[int, int]] = []
    schedules.append({})
    for per_block in [1, 2]:
        assignment = {}
        for block in range(DIFF_COUNT):
            block_cols = [col for col in free_cols if col // K == block]
            for idx, col in enumerate(block_cols[:per_block]):
                assignment[col] = 1 + block + idx
        schedules.append(assignment)
    for _ in range(max(0, SAMPLES_PER_SYSTEM - len(schedules))):
        assignment = {}
        for col in rng.sample(free_cols, min(48, len(free_cols))):
            assignment[col] = 1 + rng.randrange(p - 1)
        schedules.append(assignment)
    return [vector_from_free(echelon, rhs, pivots, assignment, p) for assignment in schedules[:SAMPLES_PER_SYSTEM]]


def proxy_collapse_classes(values: list[list[int]]) -> list[list[int]]:
    buckets: dict[tuple[int, ...], list[int]] = {}
    for witness, row in enumerate(values, start=1):
        buckets.setdefault(tuple(int(value) for value in row), []).append(witness)
    return list(buckets.values())


def six_class_dominance(values: list[list[int]]) -> int:
    target = set(COLLAPSE_CLASS)
    count = 0
    for pos in range(N):
        buckets: dict[int, set[int]] = {}
        for witness in range(LIST_SIZE):
            buckets.setdefault(int(values[witness][pos]), set()).add(witness + 1)
        if any(group == target for group in buckets.values()):
            count += 1
    return count


def evaluate_vector(vector: np.ndarray, powers: np.ndarray) -> dict[str, Any]:
    values = robust.proxy.evaluate_vector_modp(powers, vector, PROXY_PRIME)
    capacity = joint.value_class_capacity(values)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = joint.exact_assignment_max_min(values)
    classes = proxy_collapse_classes(values)
    collapse_persists = any(set(cls) == set(COLLAPSE_CLASS) for cls in classes)
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT and not collapse_persists:
        status = "PROXY_A327_COLLAPSE_REDUCED"
    elif collapse_persists:
        status = "COLLAPSE_CLASS_PERSISTS"
    elif capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        status = "SPLIT_DESTROYS_CAPACITY"
    else:
        status = "SPLIT_LOW_RESCHEDULE"
    return {
        **capacity,
        "assignment": assignment,
        "collapse_classes": classes,
        "six_class_dominance": six_class_dominance(values),
        "status": status,
        "vector_hash": hash_payload(vector.tolist()),
    }


def build_systems() -> list[dict[str, Any]]:
    robust_data = load_json(ROBUST_DATA)
    source_rows = robust.source_proxy_row_by_id()
    systems = sorted(
        robust_data["systems"],
        key=lambda row: (
            row["best_schedule"]["candidate_prime_count"],
            row["pivot_stability_score"],
            row["source_proxy_best_max_min"],
            row["system_id"],
        ),
        reverse=True,
    )[:SYSTEM_LIMIT]
    output = []
    powers = robust.proxy.vandermonde_powers_modp(PROXY_PRIME)
    for system in systems:
        source_row = source_rows[system["system_id"]]
        _source, _base, selected_info = robust.proxy.reconstruct_selected(source_row)
        selected = selected_info["selected"]
        for budget in SPLIT_BUDGETS:
            split_pos = set(split_coordinates(selected, budget))
            for partition_id, partition in PARTITIONS:
                rows, rhs, split_count = target_rows_for_modified(selected, split_pos, partition, PROXY_PRIME)
                echelon, echelon_rhs, pivots, status = affine_echelon(rows, rhs, PROXY_PRIME)
                samples = []
                if status == "OK":
                    seed = int(hash_payload([system["system_id"], budget, partition_id])[:12], 16)
                    for vector in sample_vectors(echelon, echelon_rhs, pivots, seed, PROXY_PRIME):
                        samples.append(evaluate_vector(vector, powers))
                best = max(
                    samples,
                    key=lambda sample: (
                        -1 if sample["assignment"] is None else sample["assignment"]["exact_max_min"],
                        sample["capacity_upper_bound"],
                        -sample["six_class_dominance"],
                    ),
                    default=None,
                )
                output.append(
                    {
                        "system_id": system["system_id"],
                        "split_budget_requested": budget,
                        "split_rows_inserted": split_count,
                        "partition_id": partition_id,
                        "partition": partition,
                        "row_count": int(rows.shape[0]),
                        "rank": None if pivots is None else len(pivots),
                        "nullity": None if pivots is None else VARIABLE_COUNT - len(pivots),
                        "system_status": "LOW_NULLITY" if status != "OK" else "SAMPLED",
                        "sample_count": len(samples),
                        "best": best,
                        "samples": samples,
                    }
                )
    return output


def build_record() -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    systems = build_systems()
    proxy_candidates = [
        row for row in systems
        if row["best"] is not None and row["best"]["status"] == "PROXY_A327_COLLAPSE_REDUCED"
    ]
    best = max(
        systems,
        key=lambda row: (
            -1 if row["best"] is None or row["best"]["assignment"] is None else row["best"]["assignment"]["exact_max_min"],
            -1 if row["best"] is None else row["best"]["capacity_upper_bound"],
            0 if row["best"] is None else -row["best"]["six_class_dominance"],
        ),
    )
    best_sample = best["best"]
    proof_status = "CANDIDATE" if proxy_candidates else "EXACT_EXTRACTION_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "known_collapse_class": COLLAPSE_CLASS,
        "baseline": {
            "best_degenerate_capacity": source["separation_search"]["best_capacity_upper_bound"],
            "best_exact_max_min": source["separation_search"]["best_exact_max_min"],
            "collapse_pattern": [[1, 3, 4, 5, 6, 7], [2]],
        },
        "construction_mode": "collapse_aware_target_system",
        "collapse_aware_search": {
            "systems_tested": len(systems),
            "split_rows_inserted": sorted(set(row["split_rows_inserted"] for row in systems)),
            "split_partitions_tested": [partition_id for partition_id, _partition in PARTITIONS],
            "proxy_candidates": len(proxy_candidates),
            "exact_vectors_constructed": 0,
            "nondegenerate_vectors": 0,
            "capacity_preserving_nondegenerate_vectors": 0,
            "best_proxy_max_min": None if best_sample is None or best_sample["assignment"] is None else best_sample["assignment"]["exact_max_min"],
            "best_proxy_capacity_upper_bound": None if best_sample is None else best_sample["capacity_upper_bound"],
            "best_six_class_dominance": None if best_sample is None else best_sample["six_class_dominance"],
            "best_exact_max_min": None,
            "best_failure_mode": "PROXY_CANDIDATE_EXACT_PENDING" if proxy_candidates else (None if best_sample is None else best_sample["status"]),
        },
        "systems": systems,
        "candidate": {
            "reaches_327_exact": False,
            "sage_audited": False,
        },
        "result_hash": hash_payload(systems),
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "GF(17^32) proof record",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
