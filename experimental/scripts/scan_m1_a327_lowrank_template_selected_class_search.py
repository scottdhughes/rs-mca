#!/usr/bin/env python3
"""Search low-rank coefficient-template selected-class designs for M1 a=327."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "b41747d"
OUTPUT_DATA = Path("experimental/data/m1_a327_lowrank_template_selected_class_search.json")

N = 512
FIBER_COUNT = 16
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PROXY_PRIME = 12289

PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]

TEMPLATE_SPECS = [
    {
        "template_id": "pencil_line_arrangement_m2",
        "template_family": "pencil_line_arrangement",
        "vectors": [[1, t] for t in range(7)],
        "selected_class_sizes": [4, 5],
        "cost_weight": 10.0,
        "pair7_weight": 1.0,
        "assignment_strategies": ["fiber_round_robin", "residue_block"],
    },
    {
        "template_id": "planar_rich_rank5",
        "template_family": "planar_rich_rank5",
        "vectors": [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ],
        "selected_class_sizes": [3, 4, 5],
        "cost_weight": 6.0,
        "pair7_weight": 1.0,
        "assignment_strategies": ["fiber_block", "sorted_block"],
    },
    {
        "template_id": "pair7_guarded_rank5",
        "template_family": "pair7_guarded_lowrank",
        "vectors": [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ],
        "selected_class_sizes": [3, 4, 5],
        "cost_weight": 6.0,
        "pair7_weight": 2.5,
        "assignment_strategies": ["pair7_block", "fiber_round_robin"],
    },
    {
        "template_id": "mixed_rank6",
        "template_family": "mixed_rank6",
        "vectors": [
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1],
        ],
        "selected_class_sizes": [3, 4, 5, 6],
        "cost_weight": 4.0,
        "pair7_weight": 1.5,
        "assignment_strategies": ["fiber_block", "residue_block"],
    },
    {
        "template_id": "random_matroid_seeded_0_m6",
        "template_family": "random_matroid_seeded",
        "vectors": [
            [1, 0, 0, 1, 2, 3],
            [0, 1, 0, 2, 3, 5],
            [0, 0, 1, 3, 5, 8],
            [1, 1, 0, 5, 8, 13],
            [1, 0, 1, 8, 13, 21],
            [0, 1, 1, 13, 21, 34],
            [1, 1, 1, 21, 34, 55],
        ],
        "selected_class_sizes": [3, 4, 5],
        "cost_weight": 5.0,
        "pair7_weight": 1.0,
        "assignment_strategies": ["sorted_block", "fiber_round_robin"],
    },
]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def mask_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(LIST_SIZE) if mask & (1 << idx)]


def subset_masks(sizes: list[int]) -> list[int]:
    masks = []
    for size in sizes:
        for combo in itertools.combinations(range(LIST_SIZE), size):
            mask = 0
            for idx in combo:
                mask |= 1 << idx
            masks.append(mask)
    return sorted(set(masks), key=lambda value: (value.bit_count(), value))


def contains(mask: int, witness_one_based: int) -> int:
    return int(bool(mask & (1 << (witness_one_based - 1))))


def pair_same(mask: int, pair: tuple[int, int]) -> int:
    return contains(mask, pair[0]) * contains(mask, pair[1])


def modular_rank(rows: list[list[int]], ncols: int, prime: int = PROXY_PRIME) -> int:
    basis: dict[int, list[int]] = {}
    rank = 0
    for raw in rows:
        row = [value % prime for value in raw]
        while True:
            pivot = next((idx for idx, value in enumerate(row) if value), None)
            if pivot is None:
                break
            if pivot not in basis:
                inv = pow(row[pivot], prime - 2, prime)
                row = [(value * inv) % prime for value in row]
                basis[pivot] = row
                rank += 1
                break
            factor = row[pivot]
            pivot_row = basis[pivot]
            row = [(value - factor * pivot_row[idx]) % prime for idx, value in enumerate(row)]
    return rank


def affine_rank(mask: int, vectors: list[list[int]], prime: int = PROXY_PRIME) -> int:
    members = mask_members(mask)
    if len(members) <= 1:
        return 0
    anchor = vectors[members[0] - 1]
    rows = []
    for witness in members[1:]:
        rows.append([(value - anchor[idx]) % prime for idx, value in enumerate(vectors[witness - 1])])
    return modular_rank(rows, len(anchor), prime)


def solve_template_counts(spec: dict[str, Any]) -> dict[str, Any]:
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover
        return {
            "template_id": spec["template_id"],
            "template_family": spec["template_family"],
            "solver_status": "SCIPY_UNAVAILABLE",
            "solver_error": str(exc),
            "failure_mode": "LOWRANK_TEMPLATE_SUPPORT_FAIL",
        }

    classes = subset_masks(spec["selected_class_sizes"])
    costs = {mask: affine_rank(mask, spec["vectors"]) for mask in classes}
    max_pair_idx = len(classes)
    min_pair7_idx = len(classes) + 1
    total_cost_idx = len(classes) + 2
    var_count = len(classes) + 3
    objective = np.zeros(var_count)
    objective[max_pair_idx] = 1.0
    objective[min_pair7_idx] = -float(spec["pair7_weight"])
    objective[total_cost_idx] = float(spec["cost_weight"])

    constraints = []
    lower = []
    upper = []

    row = np.zeros(var_count)
    row[: len(classes)] = 1
    constraints.append(row)
    lower.append(N)
    upper.append(N)

    for witness in range(1, LIST_SIZE + 1):
        row = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row[idx] = contains(mask, witness)
        constraints.append(row)
        lower.append(TARGET_AGREEMENT)
        upper.append(TARGET_AGREEMENT)

    for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
        cap = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            cap[idx] = pair_same(mask, pair)
        constraints.append(cap)
        lower.append(float("-inf"))
        upper.append(PAIR_CAP)

        row_max = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row_max[idx] = pair_same(mask, pair)
        row_max[max_pair_idx] = -1
        constraints.append(row_max)
        lower.append(float("-inf"))
        upper.append(0)

    for label in PAIR7_PAIR_LABELS:
        pair = next(pair for pair_label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True) if pair_label == label)
        guard = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            guard[idx] = pair_same(mask, pair)
        constraints.append(guard)
        lower.append(PAIR7_LOWER)
        upper.append(float("inf"))

        row_min = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row_min[idx] = pair_same(mask, pair)
        row_min[min_pair7_idx] = -1
        constraints.append(row_min)
        lower.append(0)
        upper.append(float("inf"))

    cost_row = np.zeros(var_count)
    for idx, mask in enumerate(classes):
        cost_row[idx] = costs[mask]
    cost_row[total_cost_idx] = -1
    constraints.append(cost_row)
    lower.append(0)
    upper.append(0)

    result = milp(
        objective,
        integrality=np.r_[np.ones(len(classes)), np.zeros(3)],
        bounds=Bounds(
            np.r_[np.zeros(len(classes)), 0, 0, 0],
            np.r_[N * np.ones(len(classes)), PAIR_CAP, N, N * max(costs.values())],
        ),
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 30},
    )
    if not result.success:
        return {
            "template_id": spec["template_id"],
            "template_family": spec["template_family"],
            "template_dimension": len(spec["vectors"][0]),
            "solver_status": "INFEASIBLE_OR_LIMIT",
            "solver_message": str(result.message),
            "failure_mode": "LOWRANK_TEMPLATE_SUPPORT_FAIL",
        }

    counts = []
    for mask, value in zip(classes, result.x[: len(classes)], strict=True):
        count = int(round(float(value)))
        if count:
            counts.append(
                {
                    "mask": mask,
                    "members": mask_members(mask),
                    "size": mask.bit_count(),
                    "affine_rank_cost": costs[mask],
                    "count": count,
                }
            )
    return {
        "template_id": spec["template_id"],
        "template_family": spec["template_family"],
        "template_dimension": len(spec["vectors"][0]),
        "template_vectors": spec["vectors"],
        "selected_class_sizes": spec["selected_class_sizes"],
        "assignment_strategies": spec["assignment_strategies"],
        "solver_status": "OPTIMAL_OR_FEASIBLE",
        "solver_message": str(result.message),
        "objective_value": float(result.fun),
        "selected_counts": counts,
        "selected_count_hash": hash_payload(counts),
        "total_effective_cost": int(round(float(result.x[total_cost_idx]))),
        "variable_count": K * len(spec["vectors"][0]),
        "max_pair_bound_value": int(round(float(result.x[max_pair_idx]))),
        "min_pair7_value": int(round(float(result.x[min_pair7_idx]))),
        "failure_mode": "LOWRANK_TEMPLATE_COST_TOO_HIGH"
        if int(round(float(result.x[total_cost_idx]))) >= K * len(spec["vectors"][0])
        else "LOWRANK_TEMPLATE_PROXY_PENDING",
    }


def expanded_masks(counts: list[dict[str, Any]]) -> list[int]:
    masks = []
    for row in counts:
        masks.extend([int(row["mask"])] * int(row["count"]))
    if len(masks) != N:
        raise RuntimeError("bad coordinate count")
    return masks


def position_order(strategy: str) -> list[int]:
    if strategy == "fiber_block":
        return [fiber + FIBER_COUNT * idx for fiber in range(FIBER_COUNT) for idx in range(N // FIBER_COUNT)]
    if strategy == "residue_block":
        return [pos for residue in range(32) for pos in range(residue, N, 32)]
    return list(range(N))


def assign_coordinates(counts: list[dict[str, Any]], strategy: str, seed: int) -> list[dict[str, Any]]:
    masks = expanded_masks(counts)
    rng = random.Random(seed)
    if strategy == "fiber_round_robin":
        rng.shuffle(masks)
    elif strategy == "pair7_block":
        masks.sort(key=lambda mask: (not contains(mask, 7), mask.bit_count(), mask))
    else:
        masks.sort(key=lambda mask: (mask.bit_count(), mask))
    order = position_order(strategy)
    if strategy == "fiber_round_robin":
        order = list(range(N))
        rng.shuffle(order)
    coordinates = [None] * N
    for mask, position in zip(masks, order, strict=True):
        coordinates[position] = {
            "position": position,
            "fiber": position % FIBER_COUNT,
            "mask": mask,
            "members": mask_members(mask),
            "size": mask.bit_count(),
        }
    return [row for row in coordinates if row is not None]


def support_counts(coordinate_classes: list[dict[str, Any]]) -> list[int]:
    supports = [0] * LIST_SIZE
    for row in coordinate_classes:
        for witness in row["members"]:
            supports[int(witness) - 1] += 1
    return supports


def pair_counts(coordinate_classes: list[dict[str, Any]]) -> dict[str, int]:
    counts = {label: 0 for label in PAIR_LABELS}
    for row in coordinate_classes:
        members = set(row["members"])
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if pair[0] in members and pair[1] in members:
                counts[label] += 1
    return counts


def size_histogram(coordinate_classes: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in coordinate_classes:
        key = str(row["size"])
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda item: int(item[0])))


def fiber_histogram(coordinate_classes: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for row in coordinate_classes:
        fiber = str(row["fiber"])
        size = str(row["size"])
        out.setdefault(fiber, {})
        out[fiber][size] = out[fiber].get(size, 0) + 1
    return out


def evaluate_candidate(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    coordinates = assign_coordinates(profile["selected_counts"], strategy, seed)
    pairs = pair_counts(coordinates)
    pair7 = [pairs[label] for label in PAIR7_PAIR_LABELS]
    return {
        "template_id": profile["template_id"],
        "template_family": profile["template_family"],
        "template_dimension": profile["template_dimension"],
        "template_vectors": profile["template_vectors"],
        "assignment_strategy": strategy,
        "assignment_seed": seed,
        "support_vector": support_counts(coordinates),
        "pair_count_matrix": pairs,
        "max_pair_count": max(pairs.values()),
        "pair7_counts": pair7,
        "selected_class_size_counts": size_histogram(coordinates),
        "total_effective_cost": profile["total_effective_cost"],
        "variable_count": profile["variable_count"],
        "cost_margin": profile["variable_count"] - profile["total_effective_cost"],
        "coordinate_classes_hash": hash_payload(coordinates),
        "quotient_fiber_histogram": fiber_histogram(coordinates),
        "coordinate_classes": coordinates,
        "proxy_prime": PROXY_PRIME,
        "proxy_rank": None,
        "proxy_nullity": None,
        "best_failure_mode": profile["failure_mode"],
    }


def previous_rank_defect_search() -> dict[str, Any]:
    path = Path("experimental/data/m1_a327_selected_class_rank_defect_search.json")
    with path.open() as handle:
        previous = json.load(handle)
    search = previous["search"]
    return {
        "systems_tested": search["systems_tested"],
        "proxy_rank_defect_candidates": search["proxy_rank_defect_candidates"],
        "best_proxy_rank": search["best_proxy_rank"],
        "best_proxy_nullity": search["best_proxy_nullity"],
        "failure_mode": search["best_failure_mode"],
    }


def build_record() -> dict[str, Any]:
    profiles = [solve_template_counts(spec) for spec in TEMPLATE_SPECS]
    candidates = []
    for profile in profiles:
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for index, strategy in enumerate(profile["assignment_strategies"]):
            candidates.append(evaluate_candidate(profile, strategy, seed=2000 + 31 * index))
    best = None if not candidates else max(
        candidates,
        key=lambda row: (
            row["cost_margin"],
            min(row["pair7_counts"]),
            -row["max_pair_count"],
            -row["template_dimension"],
            row["template_id"],
        ),
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_rank_defect_search": previous_rank_defect_search(),
        "lowrank_template_search": {
            "templates_tested": len(TEMPLATE_SPECS),
            "systems_tested": len(candidates),
            "proxy_positive_candidates": 0,
            "exact_audits": 0,
            "best_template_dimension": None if best is None else best["template_dimension"],
            "best_effective_cost": None if best is None else best["total_effective_cost"],
            "best_variable_count": None if best is None else best["variable_count"],
            "best_proxy_rank": None,
            "best_proxy_nullity": None,
            "best_exact_nullity": None,
            "best_failure_mode": "LOWRANK_TEMPLATE_SUPPORT_FAIL" if best is None else best["best_failure_mode"],
            "profiles": profiles,
            "candidates": candidates,
        },
        "best_candidate": best,
        "exact_audit": {
            "run": False,
            "field": None,
            "H_order": None,
            "matrix_shape": None,
            "rank": None,
            "nullity": None,
            "forced_equal_pairs": [],
            "min_projection_rank": None,
            "best_failure_mode": None,
        },
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": "CANDIDATE / LOWRANK_TEMPLATE_PROXY_PENDING / PARTIAL / EXPERIMENTAL",
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
        search = record["lowrank_template_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "templates_tested": search["templates_tested"],
                    "systems_tested": search["systems_tested"],
                    "best_template_dimension": search["best_template_dimension"],
                    "best_effective_cost": search["best_effective_cost"],
                    "best_variable_count": search["best_variable_count"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LOWRANK_TEMPLATE_SELECTED_CLASS_SEARCH_READY")


if __name__ == "__main__":
    main()
