#!/usr/bin/env python3
"""Bounded joint target/codeword proxy solver for the M1 a=327 target."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import scan_m1_a327_singular_all_pair_boundary_embedding_search as allpair


OUTPUT_DATA = Path("experimental/data/m1_a327_joint_target_codeword_solver.json")

N = 512
K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
VARIABLE_COUNT = DIFF_COUNT * K
TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
ROW_BUDGET = 384
SAMPLES_PER_SYSTEM = 8
RETAINED_RESULTS = 32

SOURCE_EMBEDDING_IDS = [
    "block",
    "bit_reversal",
    "fiber_round_robin",
    "random_shuffle_0000",
    "random_shuffle_0017",
    "random_shuffle_0064",
    "random_shuffle_0255",
    "random_shuffle_0511",
]

TARGET_STRATEGIES = [
    "high_multiplicity_first",
    "anchor_heavy_first",
    "nonanchor_heavy_first",
    "quotient_fiber_round",
    "seeded_shuffle",
]


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


def members(mask: int) -> list[int]:
    return [idx for idx in range(LIST_SIZE) if mask & (1 << idx)]


def bit_reverse(value: int, width: int = 9) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def quotient_fiber_round_order() -> list[int]:
    return [residue + 16 * offset for offset in range(32) for residue in range(16)]


def source_embeddings() -> list[dict[str, Any]]:
    selected = []
    for candidate in allpair.candidate_embeddings():
        if candidate["embedding_id"] not in SOURCE_EMBEDDING_IDS:
            continue
        masks = candidate["membership_masks"]
        summary = allpair.summarize_masks(masks)
        if summary["support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
            raise RuntimeError("support size mismatch")
        selected.append(
            {
                "candidate_id": f"all_pair_boundary_{candidate['embedding_id']}",
                "embedding_id": candidate["embedding_id"],
                "embedding_family": candidate["embedding_family"],
                "seed": candidate["seed"],
                "membership_masks": masks,
                "membership_mask_hash": allpair.hash_payload(masks),
                "summary": allpair.compact_summary(summary),
            }
        )
    by_id = {candidate["embedding_id"]: candidate for candidate in selected}
    return [by_id[embedding_id] for embedding_id in SOURCE_EMBEDDING_IDS]


def primitive_root_mod_prime(p: int) -> int:
    n = p - 1
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    for candidate in range(2, p):
        if all(pow(candidate, n // factor, p) != 1 for factor in factors):
            return candidate
    raise RuntimeError(f"no primitive root for {p}")


def proxy_subgroup() -> np.ndarray:
    generator = primitive_root_mod_prime(PROXY_PRIME)
    subgroup_generator = pow(generator, (PROXY_PRIME - 1) // N, PROXY_PRIME)
    return np.array([pow(subgroup_generator, idx, PROXY_PRIME) for idx in range(N)], dtype=np.int64)


def vandermonde_powers(H: np.ndarray) -> np.ndarray:
    powers = np.ones((N, K), dtype=np.int64)
    for degree in range(1, K):
        powers[:, degree] = (powers[:, degree - 1] * H) % PROXY_PRIME
    return powers


def coordinate_order(masks: list[int], strategy: str, seed: int) -> list[int]:
    if strategy == "high_multiplicity_first":
        return sorted(range(N), key=lambda pos: (-len(members(masks[pos])), pos))
    if strategy == "anchor_heavy_first":
        return sorted(
            range(N),
            key=lambda pos: (not bool(masks[pos] & 1), -len(members(masks[pos])), pos),
        )
    if strategy == "nonanchor_heavy_first":
        return sorted(
            range(N),
            key=lambda pos: (bool(masks[pos] & 1), -len(members(masks[pos])), pos),
        )
    if strategy == "quotient_fiber_round":
        return quotient_fiber_round_order()
    if strategy == "seeded_shuffle":
        order = list(range(N))
        random.Random(seed).shuffle(order)
        return order
    raise ValueError(f"unknown target strategy: {strategy}")


def constraint_rows_for_coordinate(powers: np.ndarray, mask: int, pos: int) -> list[np.ndarray]:
    bits = members(mask)
    rows = []
    if 0 in bits:
        for witness in bits:
            if witness == 0:
                continue
            row = np.zeros(VARIABLE_COUNT, dtype=np.int64)
            start = (witness - 1) * K
            row[start : start + K] = powers[pos]
            rows.append(row)
        return rows
    if len(bits) < 2:
        return rows
    left = bits[0]
    left_start = (left - 1) * K
    for witness in bits[1:]:
        row = np.zeros(VARIABLE_COUNT, dtype=np.int64)
        row[left_start : left_start + K] = powers[pos]
        right_start = (witness - 1) * K
        row[right_start : right_start + K] = (-powers[pos]) % PROXY_PRIME
        rows.append(row)
    return rows


def target_rows(powers: np.ndarray, masks: list[int], strategy: str, seed: int) -> tuple[np.ndarray, dict[str, Any]]:
    rows = []
    coordinate_count = 0
    row_type_counts: dict[str, int] = {}
    for pos in coordinate_order(masks, strategy, seed):
        coordinate_rows = constraint_rows_for_coordinate(powers, masks[pos], pos)
        if not coordinate_rows:
            continue
        for row in coordinate_rows:
            if len(rows) >= ROW_BUDGET:
                break
            rows.append(row)
        coordinate_count += 1
        row_type_counts[str(len(members(masks[pos])))] = row_type_counts.get(str(len(members(masks[pos]))), 0) + 1
        if len(rows) >= ROW_BUDGET:
            break
    if not rows:
        raise RuntimeError("empty target system")
    return np.vstack(rows) % PROXY_PRIME, {
        "target_coordinate_count": coordinate_count,
        "target_row_count": len(rows),
        "target_row_type_counts": dict(sorted(row_type_counts.items(), key=lambda item: int(item[0]))),
        "target_rows_hash": hash_payload([row[:16].tolist() for row in rows[:16]]),
    }


def rref_modp(matrix: np.ndarray, p: int) -> tuple[np.ndarray, list[int]]:
    mat = np.array(matrix, dtype=np.int64, copy=True) % p
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
        inv = pow(int(mat[rank, col]), p - 2, p)
        mat[rank] = (mat[rank] * inv) % p
        eliminate = np.nonzero(mat[:, col] % p)[0]
        for row in eliminate:
            if row == rank:
                continue
            factor = int(mat[row, col])
            mat[row] = (mat[row] - factor * mat[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == row_count:
            break
    return mat[:rank], pivots


def sample_nullspace_vectors(rref: np.ndarray, pivots: list[int], seed: int) -> list[np.ndarray]:
    pivot_set = set(pivots)
    free_cols = [col for col in range(VARIABLE_COUNT) if col not in pivot_set]
    if not free_cols:
        return []
    rng = random.Random(seed)
    free_samples: list[dict[int, int]] = []
    free_samples.append({free_cols[0]: 1})
    free_samples.append({free_cols[-1]: 1})
    for sample_idx in range(max(0, SAMPLES_PER_SYSTEM - 2)):
        width = min(len(free_cols), 12 + 4 * sample_idx)
        cols = rng.sample(free_cols, width)
        free_samples.append({col: rng.randrange(1, PROXY_PRIME) for col in cols})

    vectors = []
    for assignments in free_samples[:SAMPLES_PER_SYSTEM]:
        vector = np.zeros(VARIABLE_COUNT, dtype=np.int64)
        for col, value in assignments.items():
            vector[col] = value % PROXY_PRIME
        for row_idx in range(len(pivots) - 1, -1, -1):
            pivot = pivots[row_idx]
            total = int(np.dot(rref[row_idx], vector) % PROXY_PRIME)
            vector[pivot] = (-total) % PROXY_PRIME
        if np.any(vector % PROXY_PRIME):
            vectors.append(vector % PROXY_PRIME)
    return vectors


def evaluate_vector(powers: np.ndarray, vector: np.ndarray) -> list[list[int]]:
    values = [[0] * N]
    for witness in range(DIFF_COUNT):
        start = witness * K
        coeffs = vector[start : start + K]
        witness_values = (powers @ coeffs) % PROXY_PRIME
        values.append([int(value) for value in witness_values])
    return values


def value_class_capacity(values: list[list[int]]) -> dict[str, Any]:
    largest_histogram: dict[str, int] = {}
    total_capacity = 0
    for pos in range(N):
        buckets: dict[int, int] = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        largest = max(mask.bit_count() for mask in buckets.values())
        total_capacity += largest
        largest_histogram[str(largest)] = largest_histogram.get(str(largest), 0) + 1
    return {
        "capacity_total": total_capacity,
        "capacity_upper_bound": total_capacity // LIST_SIZE,
        "largest_class_histogram": dict(sorted(largest_histogram.items(), key=lambda item: int(item[0]))),
    }


def exact_assignment_max_min(values: list[list[int]]) -> dict[str, Any]:
    classes_by_pos = []
    for pos in range(N):
        buckets: dict[int, int] = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        classes_by_pos.append(sorted(set(buckets.values())))

    offsets = []
    total_vars = 0
    for classes in classes_by_pos:
        offsets.append(total_vars)
        total_vars += len(classes)

    def feasible(floor: int) -> tuple[bool, list[int] | None]:
        objective = np.zeros(total_vars)
        bounds = Bounds(np.zeros(total_vars), np.ones(total_vars))
        integrality = np.ones(total_vars)
        rows = []
        lower = []
        upper = []
        for pos, classes in enumerate(classes_by_pos):
            row = np.zeros(total_vars)
            row[offsets[pos] : offsets[pos] + len(classes)] = 1
            rows.append(row)
            lower.append(1)
            upper.append(1)
        for witness in range(LIST_SIZE):
            row = np.zeros(total_vars)
            for pos, classes in enumerate(classes_by_pos):
                for idx, mask in enumerate(classes):
                    if mask & (1 << witness):
                        row[offsets[pos] + idx] = 1
            rows.append(row)
            lower.append(floor)
            upper.append(np.inf)
        result = milp(
            objective,
            integrality=integrality,
            bounds=bounds,
            constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
            options={"time_limit": 15},
        )
        if not result.success:
            return False, None
        rounded = np.rint(result.x).astype(int)
        chosen = []
        for pos, classes in enumerate(classes_by_pos):
            start = offsets[pos]
            choice = next((idx for idx, value in enumerate(rounded[start : start + len(classes)]) if value), 0)
            chosen.append(classes[choice])
        return True, chosen

    lo, hi = 0, max(value_class_capacity(values)["capacity_upper_bound"], TARGET_AGREEMENT)
    best_masks = None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok, masks = feasible(mid)
        if ok:
            lo = mid
            best_masks = masks
        else:
            hi = mid - 1
    agreement = [0] * LIST_SIZE
    if best_masks:
        for mask in best_masks:
            for witness in range(LIST_SIZE):
                if mask & (1 << witness):
                    agreement[witness] += 1
    return {
        "exact_max_min": lo,
        "agreement_vector": agreement,
        "chosen_masks_hash": None if best_masks is None else hash_payload(best_masks),
    }


def evaluate_target_system(powers: np.ndarray, source: dict[str, Any], strategy: str) -> dict[str, Any]:
    seed = int(hash_payload([source["candidate_id"], strategy])[:12], 16)
    rows, metadata = target_rows(powers, source["membership_masks"], strategy, seed)
    rref, pivots = rref_modp(rows, PROXY_PRIME)
    nullity = VARIABLE_COUNT - len(pivots)
    vectors = sample_nullspace_vectors(rref, pivots, seed ^ 0xA327)
    sample_results = []
    for sample_idx, vector in enumerate(vectors):
        values = evaluate_vector(powers, vector)
        capacity = value_class_capacity(values)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = exact_assignment_max_min(values)
        sample_results.append(
            {
                "sample_index": sample_idx,
                "vector_hash": hash_payload(vector.tolist()),
                **capacity,
                "assignment": assignment,
                "status": (
                    "PROXY_A327_ASSIGNMENT"
                    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT
                    else "CAPACITY_BELOW_A327"
                ),
            }
        )
    best = max(
        sample_results,
        key=lambda row: (
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"],
            row["capacity_total"],
            row["sample_index"],
        ),
    )
    return {
        "target_system_id": f"{source['candidate_id']}__{strategy}",
        "source_candidate_id": source["candidate_id"],
        "source_embedding_id": source["embedding_id"],
        "source_embedding_family": source["embedding_family"],
        "source_seed": source["seed"],
        "source_membership_mask_hash": source["membership_mask_hash"],
        "target_strategy": strategy,
        "row_budget": ROW_BUDGET,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": len(pivots),
        "nullity": nullity,
        "pivot_columns_hash": hash_payload(pivots),
        "sample_count": len(sample_results),
        "best": best,
        "proxy_candidate_count": sum(1 for row in sample_results if row["status"] == "PROXY_A327_ASSIGNMENT"),
        "sample_results": sample_results,
        **metadata,
    }


def build_record() -> dict[str, Any]:
    H = proxy_subgroup()
    powers = vandermonde_powers(H)
    systems = []
    for source in source_embeddings():
        for strategy in TARGET_STRATEGIES:
            systems.append(evaluate_target_system(powers, source, strategy))
    retained = sorted(
        systems,
        key=lambda row: (
            row["proxy_candidate_count"],
            -1 if row["best"]["assignment"] is None else row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            row["best"]["capacity_total"],
            row["target_system_id"],
        ),
        reverse=True,
    )[:RETAINED_RESULTS]
    proxy_candidate_systems = [row for row in systems if row["proxy_candidate_count"]]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "joint_target_codeword_solver",
        "model": {
            "anchor": "P_1 = 0",
            "variables": "six degree<256 difference polynomials",
            "target_constraints": "bounded received-word value-class equality rows",
            "proxy_field": f"GF({PROXY_PRIME})",
            "row_budget": ROW_BUDGET,
            "samples_per_system": SAMPLES_PER_SYSTEM,
        },
        "source_embedding_ids": SOURCE_EMBEDDING_IDS,
        "target_strategies": TARGET_STRATEGIES,
        "target_system_count": len(systems),
        "codeword_tuple_sample_count": sum(row["sample_count"] for row in systems),
        "proxy_candidate_system_count": len(proxy_candidate_systems),
        "exact_audit_triggers": [row["target_system_id"] for row in proxy_candidate_systems],
        "retained_count": len(retained),
        "retained_results": retained,
        "best": retained[0],
        "result_hash": hash_payload(systems),
        "proof_status": "CANDIDATE" if proxy_candidate_systems else "TESTED_TARGET_SYSTEMS_NO_A327",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list certificate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "improvement over PR #133",
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
