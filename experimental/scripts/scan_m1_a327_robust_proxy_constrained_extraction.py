#!/usr/bin/env python3
"""Constrained extraction diagnostics for robust M1 a=327 proxy systems."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_proxy_positive_exact_extraction as proxy
import scan_m1_a327_joint_target_codeword_solver as joint


SOURCE_DATA = Path("experimental/data/m1_a327_proxy_positive_exact_extraction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")

N = proxy.N
K = proxy.K
LIST_SIZE = proxy.LIST_SIZE
DIFF_COUNT = proxy.DIFF_COUNT
VARIABLE_COUNT = proxy.VARIABLE_COUNT
TARGET_AGREEMENT = proxy.TARGET_AGREEMENT
PROXY_PRIMES = proxy.PROXY_PRIMES
SCHEDULE_SYSTEM_LIMIT = 13


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


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def source_proxy_row_by_id() -> dict[str, dict[str, Any]]:
    source = proxy.load_source()
    return {row["mutated_system_id"]: row for row in proxy.proxy_positive_rows(source)}


def echelon_with_rows(matrix: np.ndarray, p: int) -> tuple[np.ndarray, list[int], list[int]]:
    mat = np.array(matrix, dtype=np.int64, copy=True) % p
    row_indices = list(range(mat.shape[0]))
    row_count, col_count = mat.shape
    rank = 0
    pivots: list[int] = []
    pivot_rows: list[int] = []
    for col in range(col_count):
        pivot_candidates = np.nonzero(mat[rank:, col] % p)[0]
        if len(pivot_candidates) == 0:
            continue
        pivot = rank + int(pivot_candidates[0])
        if pivot != rank:
            mat[[rank, pivot]] = mat[[pivot, rank]]
            row_indices[rank], row_indices[pivot] = row_indices[pivot], row_indices[rank]
        inv = pow(int(mat[rank, col]), p - 2, p)
        mat[rank] = (mat[rank] * inv) % p
        below = np.nonzero(mat[rank + 1 :, col] % p)[0]
        for offset in below:
            row = rank + 1 + int(offset)
            factor = int(mat[row, col])
            mat[row] = (mat[row] - factor * mat[rank]) % p
        pivots.append(col)
        pivot_rows.append(row_indices[rank])
        rank += 1
        if rank == row_count:
            break
    return mat[:rank], pivots, pivot_rows


def vector_from_assignments(echelon: np.ndarray, pivots: list[int], assignments: dict[int, int], p: int) -> np.ndarray:
    vector = np.zeros(VARIABLE_COUNT, dtype=np.int64)
    for col, value in assignments.items():
        vector[col] = value % p
    for row_idx in range(len(pivots) - 1, -1, -1):
        pivot = pivots[row_idx]
        total = int(np.dot(echelon[row_idx], vector) % p)
        vector[pivot] = (-total) % p
    return vector % p


def row_descriptors(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    row_index = 0
    for coord in selected:
        bits = joint.members(coord["mask"])
        if 0 in bits:
            for witness in bits:
                if witness == 0:
                    continue
                rows.append(
                    {
                        "row_index": row_index,
                        "coordinate": coord["position"],
                        "fiber": coord["fiber"],
                        "mask": coord["mask"],
                        "members": bits,
                        "row_kind": "anchor_zero",
                        "blocks": [witness - 1],
                    }
                )
                row_index += 1
            continue
        if len(bits) < 2:
            continue
        left = bits[0]
        for witness in bits[1:]:
            rows.append(
                {
                    "row_index": row_index,
                    "coordinate": coord["position"],
                    "fiber": coord["fiber"],
                    "mask": coord["mask"],
                    "members": bits,
                    "row_kind": "difference",
                    "blocks": [left - 1, witness - 1],
                }
            )
            row_index += 1
    return rows


def choose_round_robin_by_fiber(descriptors: list[dict[str, Any]], count: int) -> list[int]:
    buckets: dict[int, list[int]] = {}
    for row in descriptors:
        buckets.setdefault(row["fiber"], []).append(row["row_index"])
    output = []
    while len(output) < count:
        changed = False
        for fiber in sorted(buckets):
            if buckets[fiber]:
                output.append(buckets[fiber].pop(0))
                changed = True
                if len(output) >= count:
                    break
        if not changed:
            break
    return output


def row_subset_candidates(descriptors: list[dict[str, Any]], pivot_rows_12289: list[int]) -> dict[str, list[int]]:
    rng = random.Random(0xA327CE)
    all_rows = [row["row_index"] for row in descriptors]
    deficit_rows = [
        row["row_index"]
        for row in descriptors
        if 6 in row["members"] or 5 in row["members"] or 4 in row["members"]
    ]
    sample = list(all_rows)
    rng.shuffle(sample)
    return {
        "proxy_pivot_rows_64": pivot_rows_12289[:64],
        "proxy_pivot_rows_128": pivot_rows_12289[:128],
        "deficit_rows_64": deficit_rows[:64],
        "fiber_diverse_rows_64": choose_round_robin_by_fiber(descriptors, 64),
        "full_target_row_sample_64": sorted(sample[:64]),
    }


def block_label(col: int) -> str:
    return f"D_{2 + col // K}"


def block_distribution(columns: list[int]) -> dict[str, int]:
    hist: dict[str, int] = {}
    for col in columns:
        label = block_label(col)
        hist[label] = hist.get(label, 0) + 1
    return dict(sorted(hist.items()))


def first_common_free_by_block(common_free: list[int], per_block: int) -> list[int]:
    output = []
    for block in range(DIFF_COUNT):
        cols = [col for col in common_free if col // K == block]
        output.extend(cols[:per_block])
    return output


def proxy_candidate_support(row: dict[str, Any], selected: list[dict[str, Any]]) -> tuple[set[int], dict[str, np.ndarray]]:
    powers = proxy.vandermonde_powers_modp(12289)
    rows = proxy.rows_for_selected_modp(powers, selected, 12289)
    echelon, pivots = proxy.echelon_modp(rows, 12289)
    source = proxy.source_proxy_row_by_id()[row["system_id"]] if hasattr(proxy, "source_proxy_row_by_id") else None
    seed = int(hash_payload([row["system_id"], 12289, "multiprime"])[:12], 16)
    vectors = proxy.sample_nullspace_vectors(echelon, pivots, 12289, seed)
    support = set()
    vectors_by_hash = {}
    for vector in vectors:
        digest = hash_payload(vector.tolist())
        vectors_by_hash[digest] = vector
        values = proxy.evaluate_vector_modp(powers, vector, 12289)
        capacity = joint.value_class_capacity(values)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = joint.exact_assignment_max_min(values)
        if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
            support.update(int(idx) for idx in np.nonzero(vector % 12289)[0])
    return support, vectors_by_hash


def schedule_definitions(common_free: list[int], support: set[int], system_id: str) -> list[dict[str, Any]]:
    common = sorted(common_free)
    support_common = [col for col in common if col in support]
    rng = random.Random(int(hash_payload([system_id, "common_free_random"])[:12], 16))
    random_common = list(common)
    rng.shuffle(random_common)
    schedules = [
        {
            "schedule_id": "common_free_one_per_block",
            "free_columns": first_common_free_by_block(common, 1),
            "assignment_rule": "all_ones",
        },
        {
            "schedule_id": "common_free_two_per_block",
            "free_columns": first_common_free_by_block(common, 2),
            "assignment_rule": "all_ones",
        },
        {
            "schedule_id": "proxy_support_common_free_12",
            "free_columns": (support_common + common)[:12],
            "assignment_rule": "all_ones",
        },
        {
            "schedule_id": "proxy_support_common_free_24",
            "free_columns": (support_common + common)[:24],
            "assignment_rule": "all_ones",
        },
        {
            "schedule_id": "common_free_random_12",
            "free_columns": sorted(random_common[:12]),
            "assignment_rule": "all_ones",
        },
    ]
    return [schedule for schedule in schedules if schedule["free_columns"]]


def evaluate_schedule_for_prime(
    p: int,
    powers: np.ndarray,
    echelon: np.ndarray,
    pivots: list[int],
    schedule: dict[str, Any],
) -> dict[str, Any]:
    assignments = {int(col): 1 for col in schedule["free_columns"]}
    vector = vector_from_assignments(echelon, pivots, assignments, p)
    values = proxy.evaluate_vector_modp(powers, vector, p)
    capacity = joint.value_class_capacity(values)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = joint.exact_assignment_max_min(values)
    status = (
        "PROXY_A327_ASSIGNMENT"
        if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT
        else "HIGH_CAPACITY_IMBALANCED"
        if assignment is not None
        else "LOW_CAPACITY"
    )
    return {
        "prime": p,
        "vector_hash": hash_payload(vector.tolist()),
        **capacity,
        "assignment": assignment,
        "status": status,
    }


def evaluate_system(source_system: dict[str, Any], source_row: dict[str, Any]) -> dict[str, Any]:
    _source, _base, selected_info = proxy.reconstruct_selected(source_row)
    selected = selected_info["selected"]
    descriptors = row_descriptors(selected)

    by_prime = {}
    pivot_sets = []
    free_sets = []
    pivot_orders = []
    pivot_row_orders = []
    for p in PROXY_PRIMES:
        powers = proxy.vandermonde_powers_modp(p)
        rows = proxy.rows_for_selected_modp(powers, selected, p)
        echelon, pivots, pivot_rows = echelon_with_rows(rows, p)
        free_cols = [col for col in range(VARIABLE_COUNT) if col not in set(pivots)]
        by_prime[p] = {
            "powers": powers,
            "echelon": echelon,
            "pivots": pivots,
            "pivot_rows": pivot_rows,
            "free_cols": free_cols,
        }
        pivot_sets.append(set(pivots))
        free_sets.append(set(free_cols))
        pivot_orders.append(pivots)
        pivot_row_orders.append(pivot_rows)

    common_pivots = sorted(set.intersection(*pivot_sets))
    common_free = sorted(set.intersection(*free_sets))
    pivot_order_stable = all(pivot_orders[0] == order for order in pivot_orders[1:])
    free_order_stable = all(by_prime[PROXY_PRIMES[0]]["free_cols"] == by_prime[p]["free_cols"] for p in PROXY_PRIMES[1:])
    pivot_row_order_stable = all(pivot_row_orders[0] == order for order in pivot_row_orders[1:])
    pivot_stability_score = (
        len(common_pivots) / max(1, source_system["source_proxy_rank"])
        + len(common_free) / max(1, source_system["source_proxy_nullity"])
        + (1 if pivot_order_stable else 0)
        + (1 if free_order_stable else 0)
    ) / 4

    support, _vectors_by_hash = proxy_candidate_support(source_system, selected)
    schedules = schedule_definitions(common_free, support, source_system["system_id"])
    schedule_results = []
    for schedule in schedules:
        prime_results = []
        for p in PROXY_PRIMES:
            prime_results.append(
                evaluate_schedule_for_prime(
                    p,
                    by_prime[p]["powers"],
                    by_prime[p]["echelon"],
                    by_prime[p]["pivots"],
                    schedule,
                )
            )
        candidate_prime_count = sum(1 for row in prime_results if row["status"] == "PROXY_A327_ASSIGNMENT")
        best = max(
            prime_results,
            key=lambda row: (
                -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
                row["capacity_upper_bound"],
                row["prime"],
            ),
        )
        schedule_results.append(
            {
                **schedule,
                "free_column_count": len(schedule["free_columns"]),
                "free_block_distribution": block_distribution(schedule["free_columns"]),
                "candidate_prime_count": candidate_prime_count,
                "best": best,
                "prime_results": prime_results,
            }
        )

    best_schedule = max(
        schedule_results,
        key=lambda row: (
            row["candidate_prime_count"],
            -1 if row["best"]["assignment"] is None else row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            row["schedule_id"],
        ),
    )
    return {
        "system_id": source_system["system_id"],
        "source_proxy_best_max_min": source_system["source_proxy_best_max_min"],
        "source_proxy_best_agreement": source_system["source_proxy_best_agreement"],
        "source_proxy_candidate_count": source_system["source_proxy_candidate_count"],
        "row_budget": source_system["row_budget"],
        "target_row_count": source_system["target_row_count"],
        "target_coordinate_count": source_system["target_coordinate_count"],
        "proxy_primes": PROXY_PRIMES,
        "rank": source_system["source_proxy_rank"],
        "nullity": source_system["source_proxy_nullity"],
        "common_pivot_count": len(common_pivots),
        "common_free_count": len(common_free),
        "pivot_order_stable": pivot_order_stable,
        "free_order_stable": free_order_stable,
        "pivot_row_order_stable": pivot_row_order_stable,
        "pivot_stability_score": pivot_stability_score,
        "common_pivot_columns": common_pivots,
        "common_free_columns": common_free,
        "common_pivot_hash": hash_payload(common_pivots),
        "common_free_hash": hash_payload(common_free),
        "common_free_block_distribution": block_distribution(common_free),
        "proxy_candidate_support_size_12289": len(support),
        "proxy_candidate_support_common_free_count": len([col for col in support if col in set(common_free)]),
        "row_subset_candidates": row_subset_candidates(descriptors, by_prime[12289]["pivot_rows"]),
        "target_row_descriptor_hash": hash_payload(descriptors),
        "schedule_results": schedule_results,
        "best_schedule": best_schedule,
        "schedule_status": (
            "CONSTRAINED_SCHEDULE_PROXY_A327"
            if best_schedule["candidate_prime_count"]
            else "CONSTRAINED_SCHEDULE_NO_PROXY_A327"
        ),
    }


def build_record() -> dict[str, Any]:
    source = load_source()
    source_rows = source_proxy_row_by_id()
    systems = sorted(
        source["systems"],
        key=lambda row: (
            row["multi_prime_candidate_prime_count"],
            row["source_proxy_best_max_min"],
            row["best_prime_fingerprint"]["best"]["capacity_upper_bound"],
            row["system_id"],
        ),
        reverse=True,
    )
    evaluated = [
        evaluate_system(system, source_rows[system["system_id"]])
        for system in systems[:SCHEDULE_SYSTEM_LIMIT]
    ]
    schedule_positive = [row for row in evaluated if row["schedule_status"] == "CONSTRAINED_SCHEDULE_PROXY_A327"]
    best = max(
        evaluated,
        key=lambda row: (
            row["best_schedule"]["candidate_prime_count"],
            row["pivot_stability_score"],
            row["source_proxy_best_max_min"],
            row["system_id"],
        ),
    )
    proof_status = "CONSTRAINED_SCHEDULE_PROXY_A327" if schedule_positive else "STABLE_PIVOT_DIAGNOSTIC_ONLY"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "robust_proxy_constrained_extraction",
        "source": {
            "source_json": str(SOURCE_DATA),
            "source_commit": "bf374dc",
            "source_result_hash": source["result_hash"],
            "source_proof_status": source["proof_status"],
            "source_proxy_positive_systems": source["proxy_positive_systems"],
            "source_proxy_candidate_samples": source["proxy_candidate_samples"],
            "source_multi_prime_robust_system_count": source["multi_prime_robust_system_count"],
        },
        "proxy_primes": PROXY_PRIMES,
        "system_count": len(evaluated),
        "systems_with_stable_pivot_order": sum(1 for row in evaluated if row["pivot_order_stable"]),
        "systems_with_stable_free_order": sum(1 for row in evaluated if row["free_order_stable"]),
        "systems_with_stable_pivot_rows": sum(1 for row in evaluated if row["pivot_row_order_stable"]),
        "constrained_schedule_proxy_positive_system_count": len(schedule_positive),
        "systems": evaluated,
        "best": best,
        "result_hash": hash_payload(evaluated),
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list proof record",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "improvement over PR #133",
            "full GF(17^32) nullspace extraction",
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
