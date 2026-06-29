#!/usr/bin/env python3
"""Balanced MILP target/codeword proxy solver for the M1 a=327 target."""

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

import scan_m1_a327_joint_target_codeword_solver as joint


OUTPUT_DATA = Path("experimental/data/m1_a327_balanced_target_milp_codeword_solver.json")

N = joint.N
K = joint.K
LIST_SIZE = joint.LIST_SIZE
DIFF_COUNT = joint.DIFF_COUNT
VARIABLE_COUNT = joint.VARIABLE_COUNT
TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
ROW_BUDGETS = [384, 448, 512]
OBJECTIVES = [
    "max_min_credit",
    "min_variance",
    "penalize_six_of_seven",
    "fiber_diversity",
    "hybrid_balance",
]
SAMPLES_PER_SYSTEM = 16
RETAINED_RESULTS = 32


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
    return joint.members(mask)


def fiber_id(pos: int) -> int:
    return pos % 16


def candidate_coordinates(masks: list[int]) -> list[dict[str, Any]]:
    rows = []
    for pos, mask in enumerate(masks):
        bits = members(mask)
        if len(bits) < 3:
            continue
        row_count = len(bits) - 1
        if row_count <= 0:
            continue
        rows.append(
            {
                "position": pos,
                "mask": mask,
                "members": bits,
                "size": len(bits),
                "row_count": row_count,
                "fiber": fiber_id(pos),
                "has_anchor": 0 in bits,
            }
        )
    return rows


def objective_weight(coord: dict[str, Any], objective: str) -> int:
    size = coord["size"]
    anchor_bonus = 4 if coord["has_anchor"] else 0
    if objective == "max_min_credit":
        return 100 * size + anchor_bonus
    if objective == "min_variance":
        return 80 * size - 20 * abs(size - 4.5) + anchor_bonus
    if objective == "penalize_six_of_seven":
        return 120 * size - (220 if size == 6 else 0) - (260 if size == 7 else 0) + anchor_bonus
    if objective == "fiber_diversity":
        return 80 * size + 12 * coord["fiber"] + anchor_bonus
    if objective == "hybrid_balance":
        return (
            140 * size
            - (180 if size >= 6 else 0)
            + (60 if size in {4, 5} else 0)
            + anchor_bonus
        )
    raise ValueError(f"unknown objective: {objective}")


def select_coordinates_milp(
    coords: list[dict[str, Any]],
    row_budget: int,
    objective: str,
) -> dict[str, Any]:
    n = len(coords)
    total_vars = n + LIST_SIZE + 16
    z_offset = 0
    under_offset = n
    fiber_offset = n + LIST_SIZE

    obj = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        obj[z_offset + idx] = -objective_weight(coord, objective)
    # Secondary balance pressure: minimize under-credit slack.
    obj[under_offset : under_offset + LIST_SIZE] = 1000
    if objective in {"fiber_diversity", "hybrid_balance"}:
        obj[fiber_offset : fiber_offset + 16] = -30

    rows = []
    lower = []
    upper = []

    row = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        row[z_offset + idx] = coord["row_count"]
    rows.append(row)
    lower.append(1)
    upper.append(row_budget)

    target_credit = row_budget * 4.5 / 6
    for witness in range(LIST_SIZE):
        row = np.zeros(total_vars)
        for idx, coord in enumerate(coords):
            if witness in coord["members"]:
                row[z_offset + idx] = 1
        row[under_offset + witness] = 1
        rows.append(row)
        lower.append(target_credit)
        upper.append(np.inf)

    for fiber in range(16):
        row = np.zeros(total_vars)
        for idx, coord in enumerate(coords):
            if coord["fiber"] == fiber:
                row[z_offset + idx] = 1
        row[fiber_offset + fiber] = -1
        rows.append(row)
        lower.append(0)
        upper.append(np.inf)

    bounds = Bounds(np.zeros(total_vars), np.full(total_vars, np.inf))
    integrality = np.zeros(total_vars)
    integrality[:n] = 1
    integrality[fiber_offset:] = 1
    upper_bounds = np.full(total_vars, np.inf)
    upper_bounds[:n] = 1
    upper_bounds[fiber_offset:] = 1
    bounds = Bounds(np.zeros(total_vars), upper_bounds)

    result = milp(
        obj,
        integrality=integrality,
        bounds=bounds,
        constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
        options={"time_limit": 10},
    )
    if not result.success:
        raise RuntimeError(f"MILP failed for objective={objective}, budget={row_budget}: {result.message}")
    chosen = [idx for idx in range(n) if int(round(result.x[z_offset + idx]))]
    if not chosen:
        raise RuntimeError("MILP chose no coordinates")
    selected = [coords[idx] for idx in chosen]
    credit = [0] * LIST_SIZE
    for coord in selected:
        for witness in coord["members"]:
            credit[witness] += 1
    row_count = sum(coord["row_count"] for coord in selected)
    fiber_hist: dict[str, int] = {}
    size_hist: dict[str, int] = {}
    for coord in selected:
        fiber_hist[str(coord["fiber"])] = fiber_hist.get(str(coord["fiber"]), 0) + 1
        size_hist[str(coord["size"])] = size_hist.get(str(coord["size"]), 0) + 1
    return {
        "selected": selected,
        "milp_objective_value": float(result.fun),
        "target_coordinate_count": len(selected),
        "target_row_count": row_count,
        "target_credit_profile": credit,
        "target_credit_min": min(credit),
        "target_credit_max": max(credit),
        "target_credit_variance_proxy": sum((value * LIST_SIZE - sum(credit)) ** 2 for value in credit),
        "target_size_histogram": dict(sorted(size_hist.items(), key=lambda item: int(item[0]))),
        "target_fiber_histogram": dict(sorted(fiber_hist.items(), key=lambda item: int(item[0]))),
    }


def rows_for_selected(powers: np.ndarray, selected: list[dict[str, Any]]) -> np.ndarray:
    rows = []
    for coord in selected:
        rows.extend(joint.constraint_rows_for_coordinate(powers, coord["mask"], coord["position"]))
    if not rows:
        raise RuntimeError("no coefficient rows")
    return np.vstack(rows) % PROXY_PRIME


def sample_nullspace_vectors(rref: np.ndarray, pivots: list[int], seed: int, sample_count: int) -> list[np.ndarray]:
    pivot_set = set(pivots)
    free_cols = [col for col in range(VARIABLE_COUNT) if col not in pivot_set]
    if not free_cols:
        return []
    rng = random.Random(seed)
    free_samples: list[dict[int, int]] = []
    # Include deterministic sparse basis probes and then mixed sparse probes.
    for col in free_cols[: min(4, len(free_cols))]:
        free_samples.append({col: 1})
    if len(free_cols) > 4:
        free_samples.append({free_cols[-1]: 1})
    while len(free_samples) < sample_count:
        sample_idx = len(free_samples)
        width = min(len(free_cols), 8 + 2 * sample_idx)
        cols = rng.sample(free_cols, width)
        free_samples.append({col: rng.randrange(1, PROXY_PRIME) for col in cols})

    vectors = []
    for assignments in free_samples[:sample_count]:
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


def failure_mode(sample: dict[str, Any]) -> str:
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "LOW_CAPACITY"
    assignment = sample["assignment"]
    if assignment is None:
        return "HIGH_CAPACITY_UNSOLVED"
    if assignment["exact_max_min"] < TARGET_AGREEMENT:
        return "HIGH_CAPACITY_IMBALANCED"
    return "CANDIDATE"


def evaluate_target_system(
    powers: np.ndarray,
    source: dict[str, Any],
    row_budget: int,
    objective: str,
) -> dict[str, Any]:
    coords = candidate_coordinates(source["membership_masks"])
    selection = select_coordinates_milp(coords, row_budget, objective)
    rows = rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(rows, PROXY_PRIME)
    nullity = VARIABLE_COUNT - len(pivots)
    seed = int(hash_payload([source["candidate_id"], row_budget, objective])[:12], 16)
    vectors = sample_nullspace_vectors(rref, pivots, seed, SAMPLES_PER_SYSTEM)
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
        row["failure_mode"] = failure_mode(row)
        row["status"] = (
            "PROXY_A327_ASSIGNMENT"
            if row["failure_mode"] == "CANDIDATE"
            else "CAPACITY_BELOW_A327"
        )
        sample_results.append(row)
    best = max(
        sample_results,
        key=lambda row: (
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"],
            row["capacity_total"],
            row["sample_index"],
        ),
    )
    failure_counts: dict[str, int] = {}
    for sample in sample_results:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    return {
        "target_system_id": f"{source['candidate_id']}__B{row_budget}__{objective}",
        "source_candidate_id": source["candidate_id"],
        "source_embedding_id": source["embedding_id"],
        "source_embedding_family": source["embedding_family"],
        "source_seed": source["seed"],
        "source_membership_mask_hash": source["membership_mask_hash"],
        "row_budget": row_budget,
        "selection_objective": objective,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": len(pivots),
        "nullity": nullity,
        "pivot_columns_hash": hash_payload(pivots),
        "sample_count": len(sample_results),
        "best": best,
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": sum(1 for row in sample_results if row["status"] == "PROXY_A327_ASSIGNMENT"),
        "sample_results": sample_results,
        "target_rows_hash": hash_payload([row[:16].tolist() for row in rows[:16]]),
        **{key: value for key, value in selection.items() if key != "selected"},
    }


def build_record() -> dict[str, Any]:
    H = joint.proxy_subgroup()
    powers = joint.vandermonde_powers(H)
    systems = []
    for source in joint.source_embeddings():
        for row_budget in ROW_BUDGETS:
            for objective in OBJECTIVES:
                systems.append(evaluate_target_system(powers, source, row_budget, objective))
    retained = sorted(
        systems,
        key=lambda row: (
            row["proxy_candidate_count"],
            -1 if row["best"]["assignment"] is None else row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            -row["target_credit_variance_proxy"],
            row["target_credit_min"],
            row["target_system_id"],
        ),
        reverse=True,
    )[:RETAINED_RESULTS]
    proxy_candidate_systems = [row for row in systems if row["proxy_candidate_count"]]
    failure_counts: dict[str, int] = {}
    for row in systems:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "baseline": {
            "current_public_agreement": 326,
            "current_lower_bound": 7,
        },
        "construction_mode": "balanced_target_milp_codeword_solver",
        "model": {
            "anchor": "P_1 = 0",
            "variables": "six degree<256 difference polynomials",
            "target_selection": "MILP-selected partial received-word value-class constraints",
            "proxy_field": f"GF({PROXY_PRIME})",
            "samples_per_system": SAMPLES_PER_SYSTEM,
        },
        "row_budgets": ROW_BUDGETS,
        "selection_objectives": OBJECTIVES,
        "source_embedding_ids": joint.SOURCE_EMBEDDING_IDS,
        "target_system_count": len(systems),
        "codeword_tuple_sample_count": sum(row["sample_count"] for row in systems),
        "proxy_candidate_system_count": len(proxy_candidate_systems),
        "exact_audit_triggers": [row["target_system_id"] for row in proxy_candidate_systems],
        "failure_mode_counts": dict(sorted(failure_counts.items())),
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
