#!/usr/bin/env python3
"""Search selected-class hypergraphs with quotient rank defect for M1 a=327."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "7e7439a"
OUTPUT_DATA = Path("experimental/data/m1_a327_selected_class_rank_defect_search.json")

N = 512
FIBER_COUNT = 16
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PROXY_PRIME = 12289  # 12289 - 1 is divisible by 512.
VARIABLES = (LIST_SIZE - 1) * K
QUOTIENT_EQUATIONS = LIST_SIZE * TARGET_AGREEMENT - N
RANK_THRESHOLD_FOR_LIFT = VARIABLES - 1

PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]

PROFILE_SPECS = [
    {
        "profile_id": "fiber_balanced_45",
        "selected_class_sizes": [4, 5],
        "max_pair_weight": 1.0,
        "pair7_weight": 0.5,
        "bias_pairs": [],
        "bias_weight": 0.0,
        "assignment_strategies": ["fiber_round_robin", "residue_block"],
    },
    {
        "profile_id": "fiber_block_selected_classes",
        "selected_class_sizes": [4, 5],
        "max_pair_weight": 1.2,
        "pair7_weight": 0.25,
        "bias_pairs": ["P12", "P23", "P34", "P45", "P56", "P67"],
        "bias_weight": 0.4,
        "assignment_strategies": ["fiber_block", "sorted_block"],
    },
    {
        "profile_id": "nested_pairset_7_guard",
        "selected_class_sizes": [3, 4, 5],
        "max_pair_weight": 0.75,
        "pair7_weight": 2.0,
        "bias_pairs": ["P17", "P27", "P37", "P47", "P57"],
        "bias_weight": 0.8,
        "assignment_strategies": ["fiber_round_robin", "pair7_block"],
    },
    {
        "profile_id": "quotient_fiber_rank_defect",
        "selected_class_sizes": [3, 4, 5],
        "max_pair_weight": 1.0,
        "pair7_weight": 1.0,
        "bias_pairs": ["P12", "P13", "P14", "P15", "P16", "P17"],
        "bias_weight": 0.35,
        "assignment_strategies": ["fiber_block", "fiber_round_robin"],
    },
    {
        "profile_id": "residue_class_rank_defect",
        "selected_class_sizes": [3, 4, 5, 6],
        "max_pair_weight": 1.5,
        "pair7_weight": 1.0,
        "bias_pairs": ["P14", "P17", "P27", "P37", "P47", "P57"],
        "bias_weight": 0.25,
        "assignment_strategies": ["residue_block", "fiber_block"],
    },
    {
        "profile_id": "low_cycle_dependency",
        "selected_class_sizes": [3, 4, 5],
        "max_pair_weight": 2.0,
        "pair7_weight": 0.75,
        "bias_pairs": ["P12", "P23", "P37", "P47", "P45", "P15"],
        "bias_weight": 0.6,
        "assignment_strategies": ["sorted_block", "residue_block"],
    },
    {
        "profile_id": "mixed_fiber_residual",
        "selected_class_sizes": [2, 3, 4, 5, 6],
        "max_pair_weight": 1.2,
        "pair7_weight": 1.2,
        "bias_pairs": ["P17", "P27", "P37", "P47", "P57", "P14", "P45"],
        "bias_weight": 0.2,
        "assignment_strategies": ["fiber_round_robin", "pair7_block"],
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


def solve_profile(spec: dict[str, Any]) -> dict[str, Any]:
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover
        return {
            "profile_id": spec["profile_id"],
            "solver_status": "SCIPY_UNAVAILABLE",
            "solver_error": str(exc),
            "failure_mode": "RANK_DEFECT_SUPPORT_FAIL",
        }

    classes = subset_masks(spec["selected_class_sizes"])
    max_pair_idx = len(classes)
    min_pair7_idx = len(classes) + 1
    var_count = len(classes) + 2
    objective = np.zeros(var_count)
    objective[max_pair_idx] = float(spec["max_pair_weight"])
    objective[min_pair7_idx] = -float(spec["pair7_weight"])
    bias_pairs = set(spec.get("bias_pairs", []))
    for idx, mask in enumerate(classes):
        bias_score = sum(pair_same(mask, pair) for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True) if label in bias_pairs)
        objective[idx] -= float(spec.get("bias_weight", 0.0)) * bias_score
        objective[idx] += 0.0001 * abs(mask.bit_count() - 4.47)

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
        row_cap = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row_cap[idx] = pair_same(mask, pair)
        constraints.append(row_cap)
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
        row_guard = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row_guard[idx] = pair_same(mask, pair)
        constraints.append(row_guard)
        lower.append(PAIR7_LOWER)
        upper.append(float("inf"))

        row_min = np.zeros(var_count)
        for idx, mask in enumerate(classes):
            row_min[idx] = pair_same(mask, pair)
        row_min[min_pair7_idx] = -1
        constraints.append(row_min)
        lower.append(0)
        upper.append(float("inf"))

    result = milp(
        objective,
        integrality=np.r_[np.ones(len(classes)), np.zeros(2)],
        bounds=Bounds(np.r_[np.zeros(len(classes)), 0, 0], np.r_[N * np.ones(len(classes)), PAIR_CAP, N]),
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 30},
    )
    if not result.success:
        return {
            "profile_id": spec["profile_id"],
            "selected_class_sizes": spec["selected_class_sizes"],
            "solver_status": "INFEASIBLE_OR_LIMIT",
            "solver_message": str(result.message),
            "failure_mode": "RANK_DEFECT_SUPPORT_FAIL",
        }

    counts = [
        {
            "mask": mask,
            "members": mask_members(mask),
            "size": mask.bit_count(),
            "count": int(round(float(value))),
        }
        for mask, value in zip(classes, result.x[: len(classes)], strict=True)
        if int(round(float(value)))
    ]
    return {
        "profile_id": spec["profile_id"],
        "selected_class_sizes": spec["selected_class_sizes"],
        "assignment_strategies": spec["assignment_strategies"],
        "solver_status": "OPTIMAL_OR_FEASIBLE",
        "solver_message": str(result.message),
        "objective_value": float(result.fun),
        "selected_counts": counts,
        "selected_count_hash": hash_payload(counts),
        "max_pair_bound_value": int(round(float(result.x[max_pair_idx]))),
        "min_pair7_value": int(round(float(result.x[min_pair7_idx]))),
        "failure_mode": "RANK_DEFECT_COUNT_TARGET",
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
        modulus = 32
        return [pos for residue in range(modulus) for pos in range(residue, N, modulus)]
    if strategy == "pair7_block":
        return [pos for block in range(0, N, 64) for pos in range(block, min(block + 64, N))]
    return list(range(N))


def assign_coordinates(counts: list[dict[str, Any]], strategy: str, seed: int) -> list[dict[str, Any]]:
    masks = expanded_masks(counts)
    rng = random.Random(seed)
    if strategy == "fiber_round_robin":
        rng.shuffle(masks)
    elif strategy == "sorted_block":
        masks.sort(key=lambda mask: (mask.bit_count(), mask))
    elif strategy == "pair7_block":
        masks.sort(key=lambda mask: (not contains(mask, 7), mask.bit_count(), mask))
    else:
        masks.sort(key=lambda mask: (mask, mask.bit_count()))

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


def pair_sets(coordinate_classes: list[dict[str, Any]]) -> dict[str, list[int]]:
    sets = {label: [] for label in PAIR_LABELS}
    for row in coordinate_classes:
        members = set(row["members"])
        for label, (left, right) in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if left in members and right in members:
                sets[label].append(int(row["position"]))
    return sets


def pair_counts(pair_sets_: dict[str, list[int]]) -> dict[str, int]:
    return {label: len(values) for label, values in pair_sets_.items()}


def primitive_root_mod_prime(prime: int) -> int:
    factors = sorted(set(factorize(prime - 1)))
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise RuntimeError("primitive root not found")


def factorize(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def proxy_H(prime: int = PROXY_PRIME) -> list[int]:
    generator = primitive_root_mod_prime(prime)
    root = pow(generator, (prime - 1) // N, prime)
    return [pow(root, idx, prime) for idx in range(N)]


def precompute_powers_mod(prime: int = PROXY_PRIME) -> list[list[int]]:
    h_values = proxy_H(prime)
    powers = [[1 for _ in range(N)]]
    for _degree in range(1, K):
        powers.append([(powers[-1][pos] * h_values[pos]) % prime for pos in range(N)])
    return powers


def block_start(witness_one_based: int) -> int:
    return (int(witness_one_based) - 2) * K


def quotient_rows_sparse(coordinate_classes: list[dict[str, Any]], powers: list[list[int]], prime: int) -> list[dict[int, int]]:
    rows = []
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        members = [int(value) for value in coord["members"]]
        anchor = min(members)
        for witness in members:
            if witness == anchor:
                continue
            row: dict[int, int] = {}
            if witness != 1:
                start = block_start(witness)
                for degree in range(K):
                    row[start + degree] = (row.get(start + degree, 0) + powers[degree][pos]) % prime
            if anchor != 1:
                start = block_start(anchor)
                for degree in range(K):
                    row[start + degree] = (row.get(start + degree, 0) - powers[degree][pos]) % prime
            rows.append({col: value % prime for col, value in row.items() if value % prime})
    return rows


def modular_rank_sparse(rows: list[dict[int, int]], ncols: int, prime: int) -> int:
    basis: dict[int, dict[int, int]] = {}
    rank = 0
    for raw in rows:
        row = dict(raw)
        while row:
            pivot = min(row)
            if pivot not in basis:
                inv = pow(row[pivot], prime - 2, prime)
                basis[pivot] = {col: (value * inv) % prime for col, value in row.items()}
                rank += 1
                break
            factor = row[pivot]
            pivot_row = basis[pivot]
            for col, value in pivot_row.items():
                new_value = (row.get(col, 0) - factor * value) % prime
                if new_value:
                    row[col] = new_value
                elif col in row:
                    del row[col]
        if rank == ncols:
            break
    return rank


def proxy_rank(coordinate_classes: list[dict[str, Any]], powers: list[list[int]], prime: int = PROXY_PRIME) -> dict[str, Any]:
    rows = quotient_rows_sparse(coordinate_classes, powers, prime)
    rank = modular_rank_sparse(rows, VARIABLES, prime)
    return {
        "proxy_prime": prime,
        "matrix_shape": [len(rows), VARIABLES],
        "proxy_rank": rank,
        "proxy_nullity": VARIABLES - rank,
        "proxy_failure_mode": "RANK_DEFECT_PROXY_POSITIVE" if rank < VARIABLES else "RANK_DEFECT_PROXY_FULL_RANK",
    }


def fiber_histogram(coordinate_classes: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for row in coordinate_classes:
        fiber = str(row["fiber"])
        size = str(row["size"])
        out.setdefault(fiber, {})
        out[fiber][size] = out[fiber].get(size, 0) + 1
    return out


def evaluate_candidate(profile: dict[str, Any], strategy: str, seed: int, powers: list[list[int]]) -> dict[str, Any]:
    coordinate_classes = assign_coordinates(profile["selected_counts"], strategy, seed)
    sets = pair_sets(coordinate_classes)
    counts = pair_counts(sets)
    supports = support_counts(coordinate_classes)
    pair7_counts = [counts[label] for label in PAIR7_PAIR_LABELS]
    return {
        "profile_id": profile["profile_id"],
        "assignment_strategy": strategy,
        "assignment_seed": seed,
        "supports": supports,
        "max_pair_count": max(counts.values()),
        "pair7_counts": pair7_counts,
        "pair_counts": counts,
        "pair_sets_hash": hash_payload(sets),
        "coordinate_classes_hash": hash_payload(coordinate_classes),
        "quotient_fiber_histogram": fiber_histogram(coordinate_classes),
        "coordinate_classes": coordinate_classes,
        "proxy_prime": PROXY_PRIME,
        "matrix_shape": [QUOTIENT_EQUATIONS, VARIABLES],
        "proxy_rank": None,
        "proxy_nullity": None,
        "best_failure_mode": "RANK_DEFECT_PROXY_PENDING",
    }


def build_record() -> dict[str, Any]:
    profile_rows = [solve_profile(spec) for spec in PROFILE_SPECS]
    candidates = []
    for spec, profile in zip(PROFILE_SPECS, profile_rows, strict=True):
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for index, strategy in enumerate(spec["assignment_strategies"]):
            candidates.append(evaluate_candidate(profile, strategy, seed=1000 + 17 * index, powers=[]))

    if candidates:
        best = max(
            candidates,
            key=lambda row: (
                min(row["pair7_counts"]),
                -row["max_pair_count"],
                row["profile_id"],
                row["assignment_strategy"],
            ),
        )
    else:
        best = None

    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "rank_defect_target": {
            "variables": VARIABLES,
            "selected_incidences": LIST_SIZE * TARGET_AGREEMENT,
            "quotient_equations": QUOTIENT_EQUATIONS,
            "rank_threshold_for_lift": RANK_THRESHOLD_FOR_LIFT,
            "required_row_dependencies_for_nullity": QUOTIENT_EQUATIONS - RANK_THRESHOLD_FOR_LIFT,
        },
        "search": {
            "systems_tested": len(candidates),
            "profile_systems_tested": len(PROFILE_SPECS),
            "rs_feasible_hypergraphs": len(candidates),
            "proxy_rank_defect_candidates": 0,
            "exact_rank_audits": 0,
            "positive_exact_nullity": 0,
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_exact_rank": None,
            "best_exact_nullity": None,
            "best_failure_mode": "RANK_DEFECT_SUPPORT_FAIL" if best is None else best["best_failure_mode"],
            "profiles": profile_rows,
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
        "proof_status": "CANDIDATE / RANK_DEFECT_PROXY_PENDING / PARTIAL / EXPERIMENTAL",
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
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "rs_feasible_hypergraphs": search["rs_feasible_hypergraphs"],
                    "proxy_rank_defect_candidates": search["proxy_rank_defect_candidates"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_SELECTED_CLASS_RANK_DEFECT_SEARCH_READY")


if __name__ == "__main__":
    main()
