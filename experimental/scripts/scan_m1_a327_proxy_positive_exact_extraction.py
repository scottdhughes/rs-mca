#!/usr/bin/env python3
"""Proxy-positive exact-extraction diagnostics for the M1 a=327 target."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_allpair_multiprime_sieve as multiprime
import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_incumbent_guided_target_mutation as incumbent
import scan_m1_a327_joint_target_codeword_solver as joint


SOURCE_DATA = Path("experimental/data/m1_a327_incumbent_guided_target_mutation.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_proxy_positive_exact_extraction.json")

N = joint.N
K = joint.K
LIST_SIZE = joint.LIST_SIZE
DIFF_COUNT = joint.DIFF_COUNT
VARIABLE_COUNT = joint.VARIABLE_COUNT
TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIMES = [7681, 10753, 11777, 12289, 13313]
SAMPLES_PER_PRIME = 8
SYSTEM_LIMIT = None


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


def proxy_positive_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in source["retained_results"]
        if row["proxy_candidate_count"] > 0
        and row["best"]["assignment"] is not None
        and row["best"]["assignment"]["exact_max_min"] >= TARGET_AGREEMENT
    ]
    rows.sort(
        key=lambda row: (
            row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            row["proxy_candidate_count"],
            row["mutated_system_id"],
        ),
        reverse=True,
    )
    return rows if SYSTEM_LIMIT is None else rows[:SYSTEM_LIMIT]


def reconstruct_selected(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    parent = incumbent.load_parent()
    incumbents = {
        parent_row["target_system_id"]: parent_row
        for parent_row in parent["retained_results"]
        if parent_row["best"]["assignment"] is not None
    }
    base = incumbents[row["base_target_system_id"]]
    source = incumbent.source_by_candidate_id()[incumbent.parse_source_id(base["target_system_id"])]
    base_selection = incumbent.reconstruct_selected(source, base["row_budget"], base["selection_objective"])
    coords = balanced.candidate_coordinates(source["membership_masks"])
    deficit = [TARGET_AGREEMENT - value for value in base["best"]["assignment"]["agreement_vector"]]
    selected = incumbent.mutate_selected(
        coords,
        base_selection["selected"],
        row["row_budget"],
        row["mutation_profile"],
        deficit,
        row["mutation_round"],
    )
    if selected["mutation_hash"] != row["mutation_hash"]:
        raise RuntimeError(f"mutation hash mismatch for {row['mutated_system_id']}")
    return source, base, selected


def vandermonde_powers_modp(p: int) -> np.ndarray:
    H = multiprime.proxy_subgroup(p)
    powers = np.ones((N, K), dtype=np.int64)
    for degree in range(1, K):
        powers[:, degree] = (powers[:, degree - 1] * H) % p
    return powers


def constraint_rows_for_coordinate_modp(powers: np.ndarray, mask: int, pos: int, p: int) -> list[np.ndarray]:
    bits = joint.members(mask)
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
        right_start = (witness - 1) * K
        row[left_start : left_start + K] = powers[pos]
        row[right_start : right_start + K] = (-powers[pos]) % p
        rows.append(row)
    return rows


def rows_for_selected_modp(powers: np.ndarray, selected: list[dict[str, Any]], p: int) -> np.ndarray:
    rows = []
    for coord in selected:
        rows.extend(constraint_rows_for_coordinate_modp(powers, coord["mask"], coord["position"], p))
    if not rows:
        raise RuntimeError("empty target rows")
    return np.vstack(rows) % p


def echelon_modp(matrix: np.ndarray, p: int) -> tuple[np.ndarray, list[int]]:
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
        below = np.nonzero(mat[rank + 1 :, col] % p)[0]
        for offset in below:
            row = rank + 1 + int(offset)
            factor = int(mat[row, col])
            mat[row] = (mat[row] - factor * mat[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == row_count:
            break
    return mat[:rank], pivots


def sample_nullspace_vectors(echelon: np.ndarray, pivots: list[int], p: int, seed: int) -> list[np.ndarray]:
    pivot_set = set(pivots)
    free_cols = [col for col in range(VARIABLE_COUNT) if col not in pivot_set]
    if not free_cols:
        return []
    rng = random.Random(seed)
    free_samples: list[dict[int, int]] = []
    for col in free_cols[: min(4, len(free_cols))]:
        free_samples.append({col: 1})
    if len(free_cols) > 4:
        free_samples.append({free_cols[-1]: 1})
    while len(free_samples) < SAMPLES_PER_PRIME:
        sample_idx = len(free_samples)
        width = min(len(free_cols), 8 + 2 * sample_idx)
        cols = rng.sample(free_cols, width)
        free_samples.append({col: rng.randrange(1, p) for col in cols})

    vectors = []
    for assignments in free_samples[:SAMPLES_PER_PRIME]:
        vector = np.zeros(VARIABLE_COUNT, dtype=np.int64)
        for col, value in assignments.items():
            vector[col] = value % p
        for row_idx in range(len(pivots) - 1, -1, -1):
            pivot = pivots[row_idx]
            total = int(np.dot(echelon[row_idx], vector) % p)
            vector[pivot] = (-total) % p
        if np.any(vector % p):
            vectors.append(vector % p)
    return vectors


def evaluate_vector_modp(powers: np.ndarray, vector: np.ndarray, p: int) -> list[list[int]]:
    values = [[0] * N]
    for witness in range(DIFF_COUNT):
        start = witness * K
        coeffs = vector[start : start + K]
        witness_values = (powers @ coeffs) % p
        values.append([int(value) for value in witness_values])
    return values


def sample_results_for_prime(
    p: int,
    powers: np.ndarray,
    echelon: np.ndarray,
    pivots: list[int],
    seed: int,
) -> list[dict[str, Any]]:
    vectors = sample_nullspace_vectors(echelon, pivots, p, seed)
    results = []
    for sample_idx, vector in enumerate(vectors):
        values = evaluate_vector_modp(powers, vector, p)
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
        results.append(
            {
                "sample_index": sample_idx,
                "vector_hash": hash_payload(vector.tolist()),
                **capacity,
                "assignment": assignment,
                "status": status,
            }
        )
    return results


def row_type_histogram(selected: list[dict[str, Any]]) -> dict[str, int]:
    hist: dict[str, int] = {}
    for coord in selected:
        key = str(coord["size"])
        hist[key] = hist.get(key, 0) + 1
    return dict(sorted(hist.items(), key=lambda item: int(item[0])))


def block_incidence(selected: list[dict[str, Any]]) -> dict[str, Any]:
    edge_hist: dict[str, int] = {}
    block_degree = [0] * DIFF_COUNT
    anchored_rows = 0
    nonanchored_rows = 0
    for coord in selected:
        bits = joint.members(coord["mask"])
        if 0 in bits:
            anchored_rows += len(bits) - 1
            for witness in bits:
                if witness:
                    block_degree[witness - 1] += 1
            key = "anchor:" + ",".join(str(witness) for witness in bits if witness)
            edge_hist[key] = edge_hist.get(key, 0) + 1
        elif len(bits) >= 2:
            nonanchored_rows += len(bits) - 1
            left = bits[0]
            for witness in bits[1:]:
                block_degree[left - 1] += 1
                block_degree[witness - 1] += 1
            key = "pair:" + ",".join(str(witness) for witness in bits)
            edge_hist[key] = edge_hist.get(key, 0) + 1
    return {
        "variable_blocks": DIFF_COUNT,
        "anchored_row_count": anchored_rows,
        "nonanchored_row_count": nonanchored_rows,
        "block_degree": block_degree,
        "edge_type_histogram": dict(sorted(edge_hist.items())),
        "connected_components": [list(range(1, LIST_SIZE))],
        "block_triangular_order_found": False,
    }


def evaluate_system(row: dict[str, Any]) -> dict[str, Any]:
    _source, _base, selected_info = reconstruct_selected(row)
    selected = selected_info["selected"]
    prime_results = []
    robust_candidate_prime_count = 0
    rank_drop_primes = []
    for p in PROXY_PRIMES:
        powers = vandermonde_powers_modp(p)
        rows = rows_for_selected_modp(powers, selected, p)
        echelon, pivots = echelon_modp(rows, p)
        seed = int(hash_payload([row["mutated_system_id"], p, "multiprime"])[:12], 16)
        samples = sample_results_for_prime(p, powers, echelon, pivots, seed)
        best = max(
            samples,
            key=lambda sample: (
                -1 if sample["assignment"] is None else sample["assignment"]["exact_max_min"],
                sample["capacity_upper_bound"],
                sample["capacity_total"],
                sample["sample_index"],
            ),
        )
        candidate_count = sum(1 for sample in samples if sample["status"] == "PROXY_A327_ASSIGNMENT")
        if candidate_count:
            robust_candidate_prime_count += 1
        if len(pivots) < row["rank"]:
            rank_drop_primes.append(p)
        prime_results.append(
            {
                "prime": p,
                "rank": len(pivots),
                "nullity": VARIABLE_COUNT - len(pivots),
                "pivot_columns_hash": hash_payload(pivots),
                "sample_count": len(samples),
                "candidate_sample_count": candidate_count,
                "best": best,
                "retained_samples": sorted(
                    samples,
                    key=lambda sample: (
                        -1 if sample["assignment"] is None else sample["assignment"]["exact_max_min"],
                        sample["capacity_upper_bound"],
                        sample["sample_index"],
                    ),
                    reverse=True,
                )[:3],
            }
        )

    best_prime = max(
        prime_results,
        key=lambda item: (
            -1 if item["best"]["assignment"] is None else item["best"]["assignment"]["exact_max_min"],
            item["best"]["capacity_upper_bound"],
            item["prime"],
        ),
    )
    artifact_status = (
        "MULTIPRIME_ROBUST_PROXY_CANDIDATE"
        if robust_candidate_prime_count >= 2
        else "SINGLE_PRIME_PROXY_ARTIFACT_SUSPECT"
    )
    return {
        "system_id": row["mutated_system_id"],
        "source_candidate_id": row["source_candidate_id"],
        "row_budget": row["row_budget"],
        "mutation_profile": row["mutation_profile"],
        "mutation_round": row["mutation_round"],
        "target_row_count": row["target_row_count"],
        "target_coordinate_count": row["target_coordinate_count"],
        "target_credit_profile": row["target_credit_profile"],
        "target_credit_min": row["target_credit_min"],
        "target_credit_max": row["target_credit_max"],
        "row_type_histogram": row_type_histogram(selected),
        "quotient_fiber_histogram": row["target_fiber_histogram"],
        "block_structure": block_incidence(selected),
        "source_proxy_rank": row["rank"],
        "source_proxy_nullity": row["nullity"],
        "source_proxy_best_agreement": row["best"]["assignment"]["agreement_vector"],
        "source_proxy_best_max_min": row["best"]["assignment"]["exact_max_min"],
        "source_proxy_candidate_count": row["proxy_candidate_count"],
        "multi_prime_candidate_prime_count": robust_candidate_prime_count,
        "rank_drop_primes_vs_12289": rank_drop_primes,
        "artifact_status": artifact_status,
        "prime_fingerprints": prime_results,
        "best_prime_fingerprint": best_prime,
    }


def build_record() -> dict[str, Any]:
    source = load_source()
    rows = proxy_positive_rows(source)
    systems = [evaluate_system(row) for row in rows]
    robust_systems = [
        row
        for row in systems
        if row["artifact_status"] == "MULTIPRIME_ROBUST_PROXY_CANDIDATE"
    ]
    rank_drop_systems = [row for row in systems if row["rank_drop_primes_vs_12289"]]
    best = max(
        systems,
        key=lambda row: (
            row["multi_prime_candidate_prime_count"],
            -1
            if row["best_prime_fingerprint"]["best"]["assignment"] is None
            else row["best_prime_fingerprint"]["best"]["assignment"]["exact_max_min"],
            row["best_prime_fingerprint"]["best"]["capacity_upper_bound"],
            row["system_id"],
        ),
    )
    proof_status = (
        "MULTIPRIME_ROBUST_PROXY_CANDIDATE"
        if robust_systems
        else "PROXY_ARTIFACT_SUSPECT"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "proxy_positive_exact_extraction_diagnostic",
        "source": {
            "source_json": str(SOURCE_DATA),
            "source_commit": "10ad190",
            "source_result_hash": source["result_hash"],
            "source_best_proxy_max_min": source["mutation_search"]["best_proxy_max_min"],
            "source_best_agreement_vector": source["mutation_search"]["best_agreement_vector"],
            "source_proxy_candidate_system_count": source["proxy_candidate_system_count"],
            "source_proxy_candidate_sample_count": source["mutation_search"]["failure_mode_counts"]["CANDIDATE"],
        },
        "multi_prime_proxy_primes": PROXY_PRIMES,
        "samples_per_prime": SAMPLES_PER_PRIME,
        "proxy_positive_systems": len(systems),
        "proxy_candidate_samples": sum(row["source_proxy_candidate_count"] for row in systems),
        "multi_prime_robust_system_count": len(robust_systems),
        "rank_drop_system_count": len(rank_drop_systems),
        "systems": systems,
        "best": best,
        "result_hash": hash_payload(systems),
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
