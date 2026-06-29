#!/usr/bin/env python3
"""Incumbent-guided target mutation search for the M1 a=327 target."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_joint_target_codeword_solver as joint


SOURCE_DATA = Path("experimental/data/m1_a327_balanced_target_milp_codeword_solver.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_incumbent_guided_target_mutation.json")

N = joint.N
K = joint.K
LIST_SIZE = joint.LIST_SIZE
VARIABLE_COUNT = joint.VARIABLE_COUNT
TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME

BASE_INCUMBENTS = 5
MUTATION_ROUNDS_PER_INCUMBENT = 10
ROW_BUDGETS = [512, 640]
SAMPLES_PER_SYSTEM = 32
RETAINED_RESULTS = 40
RETAINED_SAMPLES_PER_SYSTEM = 6

MUTATION_PROFILES = [
    "deficit_repair",
    "anti_six_of_seven",
    "variance_min",
    "fiber_rebalance",
    "hybrid_deficit_fiber",
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


def load_parent() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def source_by_candidate_id() -> dict[str, dict[str, Any]]:
    return {source["candidate_id"]: source for source in joint.source_embeddings()}


def parse_source_id(target_system_id: str) -> str:
    return target_system_id.split("__", 1)[0]


def incumbent_records(parent: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in parent["retained_results"]:
        assignment = row["best"]["assignment"]
        if assignment is None:
            continue
        rows.append(row)
    rows.sort(
        key=lambda row: (
            row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            -row["target_credit_variance_proxy"],
            row["target_system_id"],
        ),
        reverse=True,
    )
    return rows[:BASE_INCUMBENTS]


def reconstruct_selected(source: dict[str, Any], row_budget: int, objective: str) -> dict[str, Any]:
    coords = balanced.candidate_coordinates(source["membership_masks"])
    return balanced.select_coordinates_milp(coords, row_budget, objective)


def summarize_selected(selected: list[dict[str, Any]]) -> dict[str, Any]:
    credit = [0] * LIST_SIZE
    fiber_hist: dict[str, int] = {}
    size_hist: dict[str, int] = {}
    for coord in selected:
        for witness in coord["members"]:
            credit[witness] += 1
        fiber_hist[str(coord["fiber"])] = fiber_hist.get(str(coord["fiber"]), 0) + 1
        size_hist[str(coord["size"])] = size_hist.get(str(coord["size"]), 0) + 1
    return {
        "target_coordinate_count": len(selected),
        "target_row_count": sum(coord["row_count"] for coord in selected),
        "target_credit_profile": credit,
        "target_credit_min": min(credit),
        "target_credit_max": max(credit),
        "target_credit_variance_proxy": sum((value * LIST_SIZE - sum(credit)) ** 2 for value in credit),
        "target_size_histogram": dict(sorted(size_hist.items(), key=lambda item: int(item[0]))),
        "target_fiber_histogram": dict(sorted(fiber_hist.items(), key=lambda item: int(item[0]))),
    }


def coord_score(
    coord: dict[str, Any],
    profile: str,
    deficit: list[int],
    credit: list[int],
    fiber_hist: dict[int, int],
) -> float:
    members = coord["members"]
    size = coord["size"]
    deficit_gain = sum(deficit[witness] for witness in members)
    missing_deficit = sum(deficit[witness] for witness in range(LIST_SIZE) if witness not in members)
    low_credit_gain = sum(max(credit) - credit[witness] for witness in members)
    fiber_gap = max(fiber_hist.values() or [0]) - fiber_hist.get(coord["fiber"], 0)
    balanced_size_bonus = 12 if size in {4, 5} else 0
    six_penalty = 35 if size >= 6 else 0
    anchor_bonus = 3 if coord["has_anchor"] else 0

    if profile == "deficit_repair":
        return 40 * deficit_gain + 4 * low_credit_gain + balanced_size_bonus + anchor_bonus
    if profile == "anti_six_of_seven":
        return 38 * deficit_gain + 5 * missing_deficit + balanced_size_bonus - 8 * six_penalty
    if profile == "variance_min":
        return 8 * low_credit_gain + 18 * deficit_gain + balanced_size_bonus - 2 * six_penalty
    if profile == "fiber_rebalance":
        return 22 * deficit_gain + 15 * fiber_gap + balanced_size_bonus - six_penalty
    if profile == "hybrid_deficit_fiber":
        return 30 * deficit_gain + 6 * low_credit_gain + 10 * fiber_gap + balanced_size_bonus - 3 * six_penalty
    raise ValueError(f"unknown profile: {profile}")


def mutate_selected(
    coords: list[dict[str, Any]],
    base_selected: list[dict[str, Any]],
    row_budget: int,
    profile: str,
    deficit: list[int],
    round_index: int,
) -> dict[str, Any]:
    rng = random.Random(int(hash_payload([profile, row_budget, deficit, round_index])[:12], 16))
    selected_by_pos = {coord["position"]: dict(coord) for coord in base_selected}
    if sum(coord["row_count"] for coord in selected_by_pos.values()) > row_budget:
        ordered = sorted(selected_by_pos.values(), key=lambda coord: (-coord["row_count"], coord["position"]))
        selected_by_pos = {}
        total = 0
        for coord in ordered:
            if total + coord["row_count"] <= row_budget:
                selected_by_pos[coord["position"]] = coord
                total += coord["row_count"]

    def current_stats() -> tuple[list[int], dict[int, int], int]:
        credit = [0] * LIST_SIZE
        fibers: dict[int, int] = {}
        rows = 0
        for coord in selected_by_pos.values():
            rows += coord["row_count"]
            fibers[coord["fiber"]] = fibers.get(coord["fiber"], 0) + 1
            for witness in coord["members"]:
                credit[witness] += 1
        return credit, fibers, rows

    credit, fibers, total_rows = current_stats()
    remove_count = 3 + (round_index % 6)
    selected_scores = []
    for coord in selected_by_pos.values():
        jitter = rng.random() * 0.01
        selected_scores.append((coord_score(coord, profile, deficit, credit, fibers) + jitter, coord["position"]))
    selected_scores.sort()
    for _score, pos in selected_scores[: min(remove_count, len(selected_scores))]:
        total_rows -= selected_by_pos[pos]["row_count"]
        del selected_by_pos[pos]

    credit, fibers, total_rows = current_stats()
    available = [coord for coord in coords if coord["position"] not in selected_by_pos]
    available_scores = []
    for coord in available:
        jitter = rng.random() * 0.01
        available_scores.append((coord_score(coord, profile, deficit, credit, fibers) + jitter, coord["position"], coord))
    available_scores.sort(reverse=True)
    target_floor = max(row_budget - 4, int(0.92 * row_budget))
    for _score, _pos, coord in available_scores:
        if total_rows + coord["row_count"] > row_budget:
            continue
        selected_by_pos[coord["position"]] = dict(coord)
        total_rows += coord["row_count"]
        if total_rows >= target_floor:
            # Keep going occasionally to fill exact budget if cheap rows fit.
            if row_budget - total_rows <= 1:
                break

    # Deterministic fill for any remaining row slack.
    if total_rows < target_floor:
        credit, fibers, total_rows = current_stats()
        for _score, _pos, coord in available_scores:
            if coord["position"] in selected_by_pos:
                continue
            if total_rows + coord["row_count"] > row_budget:
                continue
            selected_by_pos[coord["position"]] = dict(coord)
            total_rows += coord["row_count"]
            if total_rows >= target_floor:
                break

    selected = sorted(selected_by_pos.values(), key=lambda coord: coord["position"])
    return {
        "selected": selected,
        "mutation_profile": profile,
        "mutation_round": round_index,
        "row_budget": row_budget,
        "mutation_hash": hash_payload([coord["position"] for coord in selected]),
        **summarize_selected(selected),
    }


def rows_for_selected(powers: np.ndarray, selected: list[dict[str, Any]]) -> np.ndarray:
    return balanced.rows_for_selected(powers, selected)


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


def sample_records_for_system(
    powers: np.ndarray,
    rows: np.ndarray,
    seed: int,
) -> tuple[list[dict[str, Any]], int, int, str]:
    echelon, pivots = echelon_modp(rows, PROXY_PRIME)
    vectors = balanced.sample_nullspace_vectors(echelon, pivots, seed, SAMPLES_PER_SYSTEM)
    sample_results = []
    for sample_idx, vector in enumerate(vectors):
        values = joint.evaluate_vector(powers, vector)
        capacity = joint.value_class_capacity(values)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = joint.exact_assignment_max_min(values)
        row = {
            "sample_index": sample_idx,
            "vector_hash": hash_payload(vector.tolist()),
            **capacity,
            "assignment": assignment,
        }
        row["failure_mode"] = balanced.failure_mode(row)
        row["status"] = (
            "PROXY_A327_ASSIGNMENT"
            if row["failure_mode"] == "CANDIDATE"
            else "CAPACITY_BELOW_A327"
        )
        sample_results.append(row)
    return sample_results, len(pivots), VARIABLE_COUNT - len(pivots), hash_payload(pivots)


def compact_samples(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        samples,
        key=lambda row: (
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"],
            row["capacity_total"],
            row["sample_index"],
        ),
        reverse=True,
    )
    return ordered[:RETAINED_SAMPLES_PER_SYSTEM]


def evaluate_mutation(
    powers: np.ndarray,
    source: dict[str, Any],
    incumbent: dict[str, Any],
    selected_info: dict[str, Any],
) -> dict[str, Any]:
    rows = rows_for_selected(powers, selected_info["selected"])
    seed = int(hash_payload([incumbent["target_system_id"], selected_info["mutation_hash"]])[:12], 16)
    samples, rank, nullity, pivots_hash = sample_records_for_system(powers, rows, seed)
    best = compact_samples(samples)[0]
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    return {
        "mutated_system_id": (
            f"{incumbent['target_system_id']}__M{selected_info['mutation_round']:02d}"
            f"__{selected_info['mutation_profile']}__B{selected_info['row_budget']}"
        ),
        "base_target_system_id": incumbent["target_system_id"],
        "source_candidate_id": source["candidate_id"],
        "source_embedding_id": source["embedding_id"],
        "source_embedding_family": source["embedding_family"],
        "source_membership_mask_hash": source["membership_mask_hash"],
        "parent_best_agreement_vector": incumbent["best"]["assignment"]["agreement_vector"],
        "parent_best_max_min": incumbent["best"]["assignment"]["exact_max_min"],
        "parent_best_capacity_upper_bound": incumbent["best"]["capacity_upper_bound"],
        "deficit_vector": [TARGET_AGREEMENT - value for value in incumbent["best"]["assignment"]["agreement_vector"]],
        "rank": rank,
        "nullity": nullity,
        "pivot_columns_hash": pivots_hash,
        "sample_count": len(samples),
        "best": best,
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": sum(1 for sample in samples if sample["status"] == "PROXY_A327_ASSIGNMENT"),
        "retained_sample_results": compact_samples(samples),
        "target_rows_hash": hash_payload([row[:16].tolist() for row in rows[:16]]),
        **{key: value for key, value in selected_info.items() if key != "selected"},
    }


def build_record() -> dict[str, Any]:
    parent = load_parent()
    sources = source_by_candidate_id()
    incumbents = incumbent_records(parent)
    H = joint.proxy_subgroup()
    powers = joint.vandermonde_powers(H)
    results = []
    for incumbent_idx, incumbent in enumerate(incumbents):
        source = sources[parse_source_id(incumbent["target_system_id"])]
        base_selection = reconstruct_selected(source, incumbent["row_budget"], incumbent["selection_objective"])
        coords = balanced.candidate_coordinates(source["membership_masks"])
        deficit = [TARGET_AGREEMENT - value for value in incumbent["best"]["assignment"]["agreement_vector"]]
        for round_idx in range(MUTATION_ROUNDS_PER_INCUMBENT):
            profile = MUTATION_PROFILES[round_idx % len(MUTATION_PROFILES)]
            row_budget = ROW_BUDGETS[(round_idx + incumbent_idx) % len(ROW_BUDGETS)]
            selected_info = mutate_selected(
                coords,
                base_selection["selected"],
                row_budget,
                profile,
                deficit,
                round_idx + 1000 * incumbent_idx,
            )
            results.append(evaluate_mutation(powers, source, incumbent, selected_info))

    retained = sorted(
        results,
        key=lambda row: (
            row["proxy_candidate_count"],
            -1 if row["best"]["assignment"] is None else row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            row["best"]["capacity_total"],
            row["mutated_system_id"],
        ),
        reverse=True,
    )[:RETAINED_RESULTS]
    proxy_candidate_systems = [row for row in results if row["proxy_candidate_count"]]
    failure_counts: dict[str, int] = {}
    for row in results:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    best = retained[0]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "baseline_public_row": {
            "agreement": 326,
            "lower_bound": 7,
        },
        "construction_mode": "incumbent_guided_target_mutation",
        "parent_solver": {
            "commit": "43a8a66",
            "source_json": str(SOURCE_DATA),
            "best_proxy_max_min": parent["best"]["best"]["assignment"]["exact_max_min"],
            "best_agreement_vector": parent["best"]["best"]["assignment"]["agreement_vector"],
            "best_raw_capacity_upper_bound": parent["best"]["best"]["capacity_upper_bound"],
            "source_result_hash": parent["result_hash"],
        },
        "mutation_search": {
            "base_incumbents": len(incumbents),
            "mutation_rounds_per_incumbent": MUTATION_ROUNDS_PER_INCUMBENT,
            "row_budgets": ROW_BUDGETS,
            "mutation_profiles": MUTATION_PROFILES,
            "mutated_systems": len(results),
            "samples_per_system": SAMPLES_PER_SYSTEM,
            "codeword_tuple_samples": sum(row["sample_count"] for row in results),
            "best_proxy_max_min": None if best["best"]["assignment"] is None else best["best"]["assignment"]["exact_max_min"],
            "best_agreement_vector": None if best["best"]["assignment"] is None else best["best"]["assignment"]["agreement_vector"],
            "best_failure_mode": best["best"]["failure_mode"],
            "failure_mode_counts": dict(sorted(failure_counts.items())),
        },
        "retained_count": len(retained),
        "retained_results": retained,
        "best": best,
        "proxy_candidate_system_count": len(proxy_candidate_systems),
        "exact_audit_triggers": [row["mutated_system_id"] for row in proxy_candidate_systems],
        "result_hash": hash_payload(results),
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
