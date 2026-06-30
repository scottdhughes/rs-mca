#!/usr/bin/env python3
"""Soft collapse-penalty target solver for the M1 a=327 proxy search."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_robust_proxy_constrained_extraction as robust


ROBUST_DATA = Path("experimental/data/m1_a327_robust_proxy_constrained_extraction.json")
HARD_SPLIT_DATA = Path("experimental/data/m1_a327_collapse_aware_target_system.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")

N = joint.N
K = joint.K
LIST_SIZE = joint.LIST_SIZE
VARIABLE_COUNT = joint.VARIABLE_COUNT
TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "0fb00ee"

SYSTEM_LIMIT = 3
ROW_BUDGETS = [512, 576, 640]
LAMBDA_VALUES = [0.01, 0.03, 0.1, 0.3, 1.0]
OBJECTIVES = [
    "soft_collapse",
    "soft_collapse_plus_variance",
    "soft_collapse_plus_fiber",
    "soft_collapse_plus_witness2_repair",
]
SAMPLES_PER_SYSTEM = 16
RETAINED_RESULTS = 36
RETAINED_SAMPLES_PER_SYSTEM = 4

COLLAPSE_CLASS_ONE_BASED = [1, 3, 4, 5, 6, 7]
COLLAPSE_CLASS = {witness - 1 for witness in COLLAPSE_CLASS_ONE_BASED}
WITNESS_2 = 1


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


def robust_seed_systems() -> list[dict[str, Any]]:
    data = load_json(ROBUST_DATA)
    systems = sorted(
        data["systems"],
        key=lambda row: (
            row["best_schedule"]["candidate_prime_count"],
            row["pivot_stability_score"],
            row["source_proxy_best_max_min"],
            row["best_schedule"]["best"]["capacity_upper_bound"],
            row["system_id"],
        ),
        reverse=True,
    )
    return systems[:SYSTEM_LIMIT]


def coordinate_features(coord: dict[str, Any]) -> dict[str, Any]:
    members = set(coord["members"])
    collapse_overlap = len(members.intersection(COLLAPSE_CLASS))
    excludes_witness_2 = WITNESS_2 not in members
    literal_six_class = members == COLLAPSE_CLASS
    six_like = excludes_witness_2 and collapse_overlap >= 5
    return {
        "collapse_overlap": collapse_overlap,
        "excludes_witness_2": excludes_witness_2,
        "literal_six_class": literal_six_class,
        "six_like": six_like,
        "balanced_size": coord["size"] in {4, 5},
    }


def soft_weight(coord: dict[str, Any], objective: str, lambda_value: float) -> float:
    features = coordinate_features(coord)
    size = coord["size"]
    anchor_bonus = 4.0 if coord["has_anchor"] else 0.0
    balanced_bonus = 55.0 if features["balanced_size"] else 0.0
    fiber_bonus = float(coord["fiber"])
    witness2_bonus = 45.0 if WITNESS_2 in coord["members"] else 0.0

    # This is intentionally soft. The previous branch was effectively
    # lambda=infinity and destroyed capacity; here the penalty only nudges the
    # selector away from six-witness collapse rows.
    collapse_penalty = 100.0 * features["collapse_overlap"]
    if features["excludes_witness_2"]:
        collapse_penalty += 180.0
    if features["six_like"]:
        collapse_penalty += 260.0
    if features["literal_six_class"]:
        collapse_penalty += 420.0

    if objective == "soft_collapse":
        base = 135.0 * size + balanced_bonus + anchor_bonus
    elif objective == "soft_collapse_plus_variance":
        base = 120.0 * size + 2.0 * balanced_bonus + anchor_bonus - 45.0 * abs(size - 4.5)
    elif objective == "soft_collapse_plus_fiber":
        base = 125.0 * size + balanced_bonus + anchor_bonus + 12.0 * fiber_bonus
    elif objective == "soft_collapse_plus_witness2_repair":
        base = 125.0 * size + balanced_bonus + anchor_bonus + witness2_bonus
    else:
        raise ValueError(f"unknown objective: {objective}")
    return base - lambda_value * collapse_penalty


def select_coordinates_soft(
    coords: list[dict[str, Any]],
    row_budget: int,
    objective: str,
    lambda_value: float,
) -> dict[str, Any]:
    n = len(coords)
    total_vars = n + LIST_SIZE + 16
    z_offset = 0
    under_offset = n
    fiber_offset = n + LIST_SIZE

    obj = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        obj[z_offset + idx] = -soft_weight(coord, objective, lambda_value)
    obj[under_offset:under_offset + LIST_SIZE] = 1000.0
    if objective == "soft_collapse_plus_fiber":
        obj[fiber_offset:fiber_offset + 16] = -30.0

    rows = []
    lower = []
    upper = []

    row = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        row[z_offset + idx] = coord["row_count"]
    rows.append(row)
    lower.append(1)
    upper.append(row_budget)

    target_credit = row_budget * 4.5 / 6.0
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

    integrality = np.zeros(total_vars)
    integrality[:n] = 1
    integrality[fiber_offset:] = 1
    upper_bounds = np.full(total_vars, np.inf)
    upper_bounds[:n] = 1
    upper_bounds[fiber_offset:] = 1

    result = milp(
        obj,
        integrality=integrality,
        bounds=Bounds(np.zeros(total_vars), upper_bounds),
        constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
        options={"time_limit": 8},
    )
    if not result.success:
        raise RuntimeError(
            f"MILP failed for objective={objective}, budget={row_budget}, lambda={lambda_value}: {result.message}"
        )

    chosen = [idx for idx in range(n) if int(round(result.x[z_offset + idx]))]
    if not chosen:
        raise RuntimeError("MILP chose no target coordinates")
    selected = [coords[idx] for idx in chosen]
    return {
        "selected": selected,
        "milp_objective_value": float(result.fun),
        **summarize_selected(selected),
    }


def summarize_selected(selected: list[dict[str, Any]]) -> dict[str, Any]:
    credit = [0] * LIST_SIZE
    fiber_hist: dict[str, int] = {}
    size_hist: dict[str, int] = {}
    literal_six_count = 0
    six_like_count = 0
    witness2_exclusion_count = 0
    collapse_penalty_score = 0
    for coord in selected:
        features = coordinate_features(coord)
        literal_six_count += int(features["literal_six_class"])
        six_like_count += int(features["six_like"])
        witness2_exclusion_count += int(features["excludes_witness_2"])
        collapse_penalty_score += int(features["collapse_overlap"]) * int(features["excludes_witness_2"])
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
        "literal_six_class_target_rows": literal_six_count,
        "six_like_target_rows": six_like_count,
        "witness_2_exclusion_count": witness2_exclusion_count,
        "target_six_class_penalty_score": collapse_penalty_score,
    }


def proxy_collapse_classes(values: list[list[int]]) -> list[list[int]]:
    buckets: dict[tuple[int, ...], list[int]] = {}
    for witness, row in enumerate(values, start=1):
        buckets.setdefault(tuple(int(value) for value in row), []).append(witness)
    return list(buckets.values())


def six_class_dominance(values: list[list[int]]) -> int:
    target = set(COLLAPSE_CLASS_ONE_BASED)
    count = 0
    for pos in range(N):
        buckets: dict[int, set[int]] = {}
        for witness in range(LIST_SIZE):
            buckets.setdefault(int(values[witness][pos]), set()).add(witness + 1)
        if any(group == target for group in buckets.values()):
            count += 1
    return count


def witness_2_exclusion_rate(values: list[list[int]]) -> float:
    excluded = 0
    for pos in range(N):
        buckets: dict[int, set[int]] = {}
        for witness in range(LIST_SIZE):
            buckets.setdefault(int(values[witness][pos]), set()).add(witness)
        largest = max(buckets.values(), key=lambda group: (len(group), -min(group)))
        if WITNESS_2 not in largest:
            excluded += 1
    return excluded / N


def classify_sample(sample: dict[str, Any]) -> str:
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "SOFT_SPLIT_CAPACITY_LOSS"
    assignment = sample["assignment"]
    if assignment is None:
        return "HIGH_CAPACITY_UNSCHEDULED"
    if assignment["exact_max_min"] < TARGET_AGREEMENT:
        return "SOFT_SPLIT_LOW_RESCHEDULE"
    if sample["six_class_dominance"] > 0:
        return "HIGH_CAPACITY_DEGENERATE"
    return "PROXY_A327_COLLAPSE_REDUCED"


def soft_system_core(
    powers: np.ndarray,
    source: dict[str, Any],
    row_budget: int,
    lambda_value: float,
    objective: str,
) -> dict[str, Any]:
    coords = balanced.candidate_coordinates(source["membership_masks"])
    selection = select_coordinates_soft(coords, row_budget, objective, lambda_value)
    rows = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(rows, PROXY_PRIME)
    return {
        "selection": selection,
        "rref": rref,
        "pivots": pivots,
        "rank": len(pivots),
        "nullity": VARIABLE_COUNT - len(pivots),
        "pivot_columns_hash": hash_payload(pivots),
    }


def sample_records_for_echelon(
    powers: np.ndarray,
    rref: np.ndarray,
    pivots: list[int],
    seed: int,
) -> list[dict[str, Any]]:
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, SAMPLES_PER_SYSTEM)
    samples = []
    for idx, vector in enumerate(vectors):
        values = joint.evaluate_vector(powers, vector)
        capacity = joint.value_class_capacity(values)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = joint.exact_assignment_max_min(values)
        sample = {
            "sample_index": idx,
            "vector_hash": hash_payload(vector.tolist()),
            **capacity,
            "assignment": assignment,
            "six_class_dominance": six_class_dominance(values),
            "witness_2_exclusion_rate": witness_2_exclusion_rate(values),
            "collapse_classes": proxy_collapse_classes(values),
        }
        sample["failure_mode"] = classify_sample(sample)
        sample["status"] = (
            "PROXY_A327_ASSIGNMENT"
            if sample["failure_mode"] in {"HIGH_CAPACITY_DEGENERATE", "PROXY_A327_COLLAPSE_REDUCED"}
            else "NO_PROXY_A327"
        )
        samples.append(sample)
    return samples


def compact_samples(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        samples,
        key=lambda row: (
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["capacity_total"],
            row["sample_index"],
        ),
        reverse=True,
    )[:RETAINED_SAMPLES_PER_SYSTEM]


def evaluate_soft_system(
    powers: np.ndarray,
    seed_system: dict[str, Any],
    source: dict[str, Any],
    row_budget: int,
    lambda_value: float,
    objective: str,
    core_cache: dict[tuple[str, int, str, str], dict[str, Any]],
) -> dict[str, Any]:
    core_key = (source["candidate_id"], row_budget, str(lambda_value), objective)
    if core_key not in core_cache:
        core_cache[core_key] = soft_system_core(powers, source, row_budget, lambda_value, objective)
    core = core_cache[core_key]
    selection = core["selection"]
    seed = int(hash_payload([seed_system["system_id"], row_budget, lambda_value, objective])[:12], 16)
    samples = sample_records_for_echelon(powers, core["rref"], core["pivots"], seed)
    retained = compact_samples(samples)
    best = retained[0]
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    proxy_candidate_count = sum(1 for sample in samples if sample["status"] == "PROXY_A327_ASSIGNMENT")
    reduced_proxy_candidate_count = sum(
        1 for sample in samples if sample["failure_mode"] == "PROXY_A327_COLLAPSE_REDUCED"
    )
    return {
        "target_system_id": (
            f"{seed_system['system_id']}__SB{row_budget}"
            f"__L{str(lambda_value).replace('.', 'p')}__{objective}"
        ),
        "seed_system_id": seed_system["system_id"],
        "source_candidate_id": source["candidate_id"],
        "source_embedding_id": source["embedding_id"],
        "source_embedding_family": source["embedding_family"],
        "row_budget": row_budget,
        "lambda_collapse_penalty": lambda_value,
        "selection_objective": objective,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": core["rank"],
        "nullity": core["nullity"],
        "pivot_columns_hash": core["pivot_columns_hash"],
        "sample_count": len(samples),
        "best": best,
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": proxy_candidate_count,
        "collapse_reduced_proxy_candidate_count": reduced_proxy_candidate_count,
        "retained_sample_results": retained,
        "target_rows_hash": hash_payload([coord["position"] for coord in selection["selected"]]),
        **{key: value for key, value in selection.items() if key != "selected"},
    }


def source_for_seed(seed_system: dict[str, Any]) -> dict[str, Any]:
    source_rows = robust.source_proxy_row_by_id()
    source, _base, _selected = robust.proxy.reconstruct_selected(source_rows[seed_system["system_id"]])
    return source


def build_record() -> dict[str, Any]:
    hard_split = load_json(HARD_SPLIT_DATA)
    robust_data = load_json(ROBUST_DATA)
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    results = []
    seeds = robust_seed_systems()
    core_cache: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for seed in seeds:
        source = source_for_seed(seed)
        for row_budget in ROW_BUDGETS:
            for lambda_value in LAMBDA_VALUES:
                for objective in OBJECTIVES:
                    results.append(
                        evaluate_soft_system(
                            powers,
                            seed,
                            source,
                            row_budget,
                            lambda_value,
                            objective,
                            core_cache,
                        )
                    )

    retained = sorted(
        results,
        key=lambda row: (
            row["collapse_reduced_proxy_candidate_count"],
            row["proxy_candidate_count"],
            -1 if row["best"]["assignment"] is None else row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance"],
            row["target_system_id"],
        ),
        reverse=True,
    )[:RETAINED_RESULTS]
    failure_counts: dict[str, int] = {}
    for row in results:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    proxy_candidates = [row for row in results if row["proxy_candidate_count"]]
    reduced_candidates = [row for row in results if row["collapse_reduced_proxy_candidate_count"]]
    best = retained[0]
    proof_status = "CANDIDATE" if reduced_candidates else "TESTED_TARGET_SYSTEMS_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "soft_collapse_penalty_target_solver",
        "baseline": {
            "hard_split_best_capacity": hard_split["collapse_aware_search"]["best_proxy_capacity_upper_bound"],
            "old_proxy_best_max_min": robust_data["best"]["best_schedule"]["best"]["assignment"]["exact_max_min"],
            "known_collapse_class": [[1, 3, 4, 5, 6, 7], [2]],
        },
        "soft_collapse_search": {
            "base_systems": len(seeds),
            "systems_tested": len(results),
            "unique_rref_cores": len(core_cache),
            "row_budgets": ROW_BUDGETS,
            "lambda_values": LAMBDA_VALUES,
            "selection_objectives": OBJECTIVES,
            "samples_per_system": SAMPLES_PER_SYSTEM,
            "codeword_tuple_samples": sum(row["sample_count"] for row in results),
            "proxy_candidates": len(proxy_candidates),
            "collapse_reduced_proxy_candidates": len(reduced_candidates),
            "best_proxy_max_min": None if best["best"]["assignment"] is None else best["best"]["assignment"]["exact_max_min"],
            "best_capacity_upper_bound": best["best"]["capacity_upper_bound"],
            "best_six_class_dominance": best["best"]["six_class_dominance"],
            "best_agreement_vector": None if best["best"]["assignment"] is None else best["best"]["assignment"]["agreement_vector"],
            "best_failure_mode": best["best"]["failure_mode"],
            "failure_mode_counts": dict(sorted(failure_counts.items())),
        },
        "exact_audit": {
            "triggered": bool(reduced_candidates),
            "exact_vectors_constructed": 0,
            "nondegenerate_vectors": 0,
            "best_exact_max_min": None,
        },
        "retained_count": len(retained),
        "retained_results": retained,
        "best": best,
        "exact_audit_triggers": [row["target_system_id"] for row in reduced_candidates],
        "result_hash": hash_payload(results),
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
