#!/usr/bin/env python3
"""Hall-guided target mutation for the M1 a=327 proxy search."""

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
import scan_m1_a327_rescheduler_dual_hall_obstruction as hall
import scan_m1_a327_soft_collapse_penalty_target_solver as soft


HALL_DATA = Path("experimental/data/m1_a327_rescheduler_dual_hall_obstruction.json")
SOFT_DATA = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_hall_guided_target_mutation.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "ed4cf43"
TARGET_ROW_BUDGET = 640
REPAIR_ROW_BUDGETS = [32, 64, 96, 128]
OBJECTIVES = [
    "hall_min_repair",
    "hall_avg_repair",
    "hall_core23_repair",
    "hall_capacity_hybrid",
]
SAMPLES_PER_SYSTEM = 16
RETAINED_RESULTS = 24
TIGHT_SUBSET_LIMIT = 3


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


def tight_subset_masks(hall_data: dict[str, Any]) -> list[int]:
    masks = [int(row["subset_mask"]) for row in hall_data["best_sample"]["tight_subsets"][:TIGHT_SUBSET_LIMIT]]
    if len(masks) < TIGHT_SUBSET_LIMIT:
        raise RuntimeError("not enough tight Hall subsets")
    return masks


def coord_hall_features(coord: dict[str, Any], tight_masks: list[int]) -> dict[str, Any]:
    mask = int(coord["mask"])
    contributions = [(mask & subset).bit_count() for subset in tight_masks]
    core23 = int(bool(mask & (1 << 1)) and bool(mask & (1 << 2)))
    repair_quality = min(contributions)
    repair_row_mass = int(coord["row_count"] if repair_quality >= 2 else 0)
    return {
        "hall_contributions": contributions,
        "hall_min_contribution": min(contributions),
        "hall_avg_contribution": sum(contributions) / len(contributions),
        "hall_sum_contribution": sum(contributions),
        "hall_core23": core23,
        "hall_repair_row_mass": repair_row_mass,
    }


def hall_weight(coord: dict[str, Any], tight_masks: list[int], objective: str) -> float:
    features = coord_hall_features(coord, tight_masks)
    size = int(coord["size"])
    anchor_bonus = 8.0 if coord["has_anchor"] else 0.0
    fiber_bonus = float(coord["fiber"])
    balanced_bonus = 40.0 if size in {4, 5} else 0.0
    collapse_penalty = 25.0 * max(0, size - 5) + (80.0 if size == 7 else 0.0)
    core_bonus = 90.0 * features["hall_core23"]
    if objective == "hall_min_repair":
        base = 420.0 * features["hall_min_contribution"] + 45.0 * features["hall_sum_contribution"]
    elif objective == "hall_avg_repair":
        base = 260.0 * features["hall_avg_contribution"] + 70.0 * features["hall_sum_contribution"]
    elif objective == "hall_core23_repair":
        base = 320.0 * features["hall_min_contribution"] + 130.0 * features["hall_core23"] + 35.0 * size
    elif objective == "hall_capacity_hybrid":
        base = 220.0 * features["hall_min_contribution"] + 80.0 * features["hall_sum_contribution"] + 80.0 * size
    else:
        raise ValueError(f"unknown objective: {objective}")
    return base + core_bonus + balanced_bonus + anchor_bonus + 3.0 * fiber_bonus - collapse_penalty


def select_coordinates_hall(
    coords: list[dict[str, Any]],
    tight_masks: list[int],
    repair_budget: int,
    objective: str,
) -> dict[str, Any]:
    n = len(coords)
    total_vars = n + joint.LIST_SIZE + 16 + len(tight_masks)
    z_offset = 0
    under_offset = n
    fiber_offset = n + joint.LIST_SIZE
    hall_under_offset = n + joint.LIST_SIZE + 16

    obj = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        obj[z_offset + idx] = -hall_weight(coord, tight_masks, objective)
    obj[under_offset:under_offset + joint.LIST_SIZE] = 800.0
    obj[fiber_offset:fiber_offset + 16] = -20.0
    obj[hall_under_offset:hall_under_offset + len(tight_masks)] = 1200.0

    rows = []
    lower = []
    upper = []

    row = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        row[z_offset + idx] = coord["row_count"]
    rows.append(row)
    lower.append(1)
    upper.append(TARGET_ROW_BUDGET)

    row = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        features = coord_hall_features(coord, tight_masks)
        row[z_offset + idx] = features["hall_repair_row_mass"]
    rows.append(row)
    lower.append(repair_budget)
    upper.append(np.inf)

    target_credit = TARGET_ROW_BUDGET * 4.5 / 6.0
    for witness in range(joint.LIST_SIZE):
        row = np.zeros(total_vars)
        for idx, coord in enumerate(coords):
            if witness in coord["members"]:
                row[z_offset + idx] = 1
        row[under_offset + witness] = 1
        rows.append(row)
        lower.append(target_credit)
        upper.append(np.inf)

    hall_target = repair_budget * 2.0
    for subset_idx, subset_mask in enumerate(tight_masks):
        row = np.zeros(total_vars)
        for coord_idx, coord in enumerate(coords):
            row[z_offset + coord_idx] = (int(coord["mask"]) & subset_mask).bit_count()
        row[hall_under_offset + subset_idx] = 1
        rows.append(row)
        lower.append(hall_target)
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
    integrality[fiber_offset:fiber_offset + 16] = 1
    upper_bounds = np.full(total_vars, np.inf)
    upper_bounds[:n] = 1
    upper_bounds[fiber_offset:fiber_offset + 16] = 1

    result = milp(
        obj,
        integrality=integrality,
        bounds=Bounds(np.zeros(total_vars), upper_bounds),
        constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
        options={"time_limit": 10},
    )
    if not result.success:
        raise RuntimeError(
            f"MILP failed for objective={objective}, repair_budget={repair_budget}: {result.message}"
        )
    chosen = [idx for idx in range(n) if int(round(result.x[z_offset + idx]))]
    if not chosen:
        raise RuntimeError("MILP chose no coordinates")
    selected = [coords[idx] for idx in chosen]
    return {
        "selected": selected,
        "milp_objective_value": float(result.fun),
        "repair_budget": repair_budget,
        "selection_objective": objective,
        **summarize_selected_hall(selected, tight_masks),
    }


def summarize_selected_hall(selected: list[dict[str, Any]], tight_masks: list[int]) -> dict[str, Any]:
    credit = [0] * joint.LIST_SIZE
    fiber_hist: dict[str, int] = {}
    size_hist: dict[str, int] = {}
    predicted_b = [0] * len(tight_masks)
    repair_mass = 0
    core23_count = 0
    for coord in selected:
        features = coord_hall_features(coord, tight_masks)
        repair_mass += features["hall_repair_row_mass"]
        core23_count += features["hall_core23"]
        for idx, value in enumerate(features["hall_contributions"]):
            predicted_b[idx] += value
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
        "target_credit_variance_proxy": sum((value * joint.LIST_SIZE - sum(credit)) ** 2 for value in credit),
        "target_size_histogram": dict(sorted(size_hist.items(), key=lambda item: int(item[0]))),
        "target_fiber_histogram": dict(sorted(fiber_hist.items(), key=lambda item: int(item[0]))),
        "predicted_tight_subset_B": predicted_b,
        "predicted_tight_subset_min_B": min(predicted_b),
        "predicted_hall_repair_row_mass": repair_mass,
        "predicted_core23_coordinate_count": core23_count,
    }


def value_hall_metrics(values: list[list[int]], tight_masks: list[int]) -> dict[str, Any]:
    hall_record = hall.hall_audit(values)
    classes_by_pos = hall.value_class_masks(values)
    tight_b = []
    for subset in tight_masks:
        total = 0
        for classes in classes_by_pos:
            total += max((mask & subset).bit_count() for mask in classes)
        tight_b.append(total)
    return {
        "hall_bound": hall_record["hall_bound"],
        "tight_subset_B": tight_b,
        "tight_subset_deficits_to_981": [len(joint.members(subset)) * TARGET_AGREEMENT - value for subset, value in zip(tight_masks, tight_b)],
        "tight_subsets": hall_record["tight_subsets"][:5],
    }


def classify_sample(sample: dict[str, Any], baseline_hall_bound: int) -> str:
    if sample["hall_bound"] <= baseline_hall_bound:
        return "HALL_NOT_REPAIRED"
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "HALL_REPAIR_DESTROYS_CAPACITY"
    if sample["six_class_dominance"] > 20:
        return "HALL_REPAIR_COLLAPSE_RETURNS"
    assignment = sample.get("assignment")
    if assignment is None:
        return "HALL_REPAIR_UNSCHEDULED"
    if assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "HALL_PROXY_CANDIDATE"
    return "HALL_REPAIR_LOW_RESCHEDULE"


def proxy_collapse_classes(values: list[list[int]]) -> list[list[int]]:
    buckets: dict[tuple[int, ...], list[int]] = {}
    for witness, row in enumerate(values, start=1):
        buckets.setdefault(tuple(int(value) for value in row), []).append(witness)
    return list(buckets.values())


def sample_records(
    powers: np.ndarray,
    rref: np.ndarray,
    pivots: list[int],
    tight_masks: list[int],
    seed: int,
    baseline_hall_bound: int,
) -> list[dict[str, Any]]:
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, SAMPLES_PER_SYSTEM)
    samples = []
    for sample_idx, vector in enumerate(vectors):
        values = joint.evaluate_vector(powers, vector)
        capacity = joint.value_class_capacity(values)
        hall_metrics = value_hall_metrics(values, tight_masks)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = joint.exact_assignment_max_min(values)
        sample = {
            "sample_index": sample_idx,
            "vector_hash": hash_payload(vector.tolist()),
            **capacity,
            **hall_metrics,
            "assignment": assignment,
            "six_class_dominance": soft.six_class_dominance(values),
            "collapse_classes": proxy_collapse_classes(values),
            "value_class_hash": hash_payload(hall.value_class_masks(values)),
        }
        sample["failure_mode"] = classify_sample(sample, baseline_hall_bound)
        sample["status"] = "PROXY_A327_ASSIGNMENT" if sample["failure_mode"] == "HALL_PROXY_CANDIDATE" else "NO_PROXY_A327"
        samples.append(sample)
    return samples


def compact_sample(sample: dict[str, Any]) -> dict[str, Any]:
    return {
        "sample_index": sample["sample_index"],
        "vector_hash": sample["vector_hash"],
        "capacity_upper_bound": sample["capacity_upper_bound"],
        "capacity_total": sample["capacity_total"],
        "hall_bound": sample["hall_bound"],
        "tight_subset_B": sample["tight_subset_B"],
        "tight_subset_deficits_to_981": sample["tight_subset_deficits_to_981"],
        "proxy_max_min": None if sample["assignment"] is None else sample["assignment"]["exact_max_min"],
        "agreement_vector": None if sample["assignment"] is None else sample["assignment"]["agreement_vector"],
        "six_class_dominance": sample["six_class_dominance"],
        "failure_mode": sample["failure_mode"],
        "status": sample["status"],
        "value_class_hash": sample["value_class_hash"],
    }


def evaluate_system(
    powers: np.ndarray,
    source: dict[str, Any],
    tight_masks: list[int],
    repair_budget: int,
    objective: str,
    baseline_hall_bound: int,
) -> dict[str, Any]:
    coords = balanced.candidate_coordinates(source["membership_masks"])
    selection = select_coordinates_hall(coords, tight_masks, repair_budget, objective)
    rows = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(rows, PROXY_PRIME)
    seed = int(hash_payload([source["candidate_id"], repair_budget, objective, SOURCE_COMMIT])[:12], 16)
    samples = sample_records(powers, rref, pivots, tight_masks, seed, baseline_hall_bound)
    retained_samples = sorted(
        samples,
        key=lambda row: (
            row["failure_mode"] == "HALL_PROXY_CANDIDATE",
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["hall_bound"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["sample_index"],
        ),
        reverse=True,
    )[:4]
    best = retained_samples[0]
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    return {
        "target_system_id": f"{source['candidate_id']}__HB{repair_budget}__{objective}",
        "source_candidate_id": source["candidate_id"],
        "source_embedding_id": source["embedding_id"],
        "source_embedding_family": source["embedding_family"],
        "repair_row_budget": repair_budget,
        "selection_objective": objective,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": len(pivots),
        "nullity": joint.VARIABLE_COUNT - len(pivots),
        "pivot_columns_hash": hash_payload(pivots),
        "sample_count": len(samples),
        "best": compact_sample(best),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": sum(1 for sample in samples if sample["status"] == "PROXY_A327_ASSIGNMENT"),
        "retained_sample_results": [compact_sample(sample) for sample in retained_samples],
        "target_rows_hash": hash_payload([coord["position"] for coord in selection["selected"]]),
        **{key: value for key, value in selection.items() if key != "selected"},
    }


def build_record() -> dict[str, Any]:
    hall_data = load_json(HALL_DATA)
    soft_rows = load_json(SOFT_DATA)["retained_results"]
    best_system_id = hall_data["best_sample"]["system_id"]
    soft_row = next(row for row in soft_rows if row["target_system_id"] == best_system_id)
    source = soft.source_for_seed({"system_id": soft_row["seed_system_id"]})
    tight_masks = tight_subset_masks(hall_data)
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    baseline_hall_bound = int(hall_data["best_sample"]["hall_bound"])
    systems = []
    for repair_budget in REPAIR_ROW_BUDGETS:
        for objective in OBJECTIVES:
            systems.append(evaluate_system(powers, source, tight_masks, repair_budget, objective, baseline_hall_bound))
    retained = sorted(
        systems,
        key=lambda row: (
            row["proxy_candidate_count"],
            -1 if row["best"]["proxy_max_min"] is None else row["best"]["proxy_max_min"],
            row["best"]["hall_bound"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance"],
            row["target_system_id"],
        ),
        reverse=True,
    )[:RETAINED_RESULTS]
    failure_counts: dict[str, int] = {}
    for row in systems:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    proxy_candidates = [row for row in systems if row["proxy_candidate_count"]]
    best = retained[0]
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_HALL_MUTATIONS_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "hall_guided_target_mutation",
        "hall_baseline": {
            "best_tangent_max_min": hall_data["best_sample"]["rescheduler_max_min"],
            "best_tangent_capacity": hall_data["best_sample"]["capacity_upper_bound"],
            "best_tangent_six_class_dominance": hall_data["best_sample"]["six_class_dominance"],
            "best_tangent_hall_bound": hall_data["best_sample"]["hall_bound"],
            "tight_subsets": hall_data["best_sample"]["tight_subsets"][:TIGHT_SUBSET_LIMIT],
        },
        "hall_guided_search": {
            "source_candidate_id": source["candidate_id"],
            "systems_tested": len(systems),
            "repair_row_budgets": REPAIR_ROW_BUDGETS,
            "selection_objectives": OBJECTIVES,
            "samples_per_system": SAMPLES_PER_SYSTEM,
            "codeword_tuple_samples": sum(row["sample_count"] for row in systems),
            "proxy_candidates": len(proxy_candidates),
            "best_proxy_max_min": best["best"]["proxy_max_min"],
            "best_hall_bound": best["best"]["hall_bound"],
            "best_tight_subset_B": best["best"]["tight_subset_B"],
            "best_capacity_upper_bound": best["best"]["capacity_upper_bound"],
            "best_six_class_dominance": best["best"]["six_class_dominance"],
            "best_failure_mode": best["best"]["failure_mode"],
            "failure_mode_counts": dict(sorted(failure_counts.items())),
        },
        "exact_audit": {
            "triggered": bool(proxy_candidates),
            "best_exact_max_min": None,
        },
        "retained_count": len(retained),
        "retained_results": retained,
        "best": best,
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
