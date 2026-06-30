#!/usr/bin/env python3
"""Collapse-constrained Hall repair for the M1 a=327 proxy search."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_hall_guided_target_mutation as guided
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_soft_collapse_penalty_target_solver as soft


HALL_GUIDED_DATA = Path("experimental/data/m1_a327_hall_guided_target_mutation.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_collapse_constrained_hall_repair.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "4d5ce7f"
TARGET_ROW_BUDGET = 640
DOMINANCE_CAPS = [350, 300, 250, 200, 150, 100, 50, 25]
REPAIR_ROW_BUDGETS = [32, 64, 96, 128]
OBJECTIVES = [
    "hall_min_repair",
    "hall_avg_repair",
    "hall_core23_repair",
    "hall_capacity_hybrid",
]
SAMPLES_PER_SYSTEM = 16
RETAINED_RESULTS = 40
LOW_DOMINANCE_THRESHOLD = 250


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def target_six_like_cap(dominance_cap: int) -> int:
    """Map sampled six-class dominance caps to target-coordinate pressure caps."""
    return max(0, min(40, dominance_cap // 9))


def coord_collapse_features(coord: dict[str, Any]) -> dict[str, Any]:
    members = set(coord["members"])
    collapse_class = set(soft.COLLAPSE_CLASS)
    collapse_overlap = len(members.intersection(collapse_class))
    excludes_witness_2 = soft.WITNESS_2 not in members
    literal_six_class = members == collapse_class
    six_like = excludes_witness_2 and collapse_overlap >= 5
    pressure_units = 1 if six_like else 0
    pressure_score = 0
    if excludes_witness_2:
        pressure_score += 1
    pressure_score += collapse_overlap
    if six_like:
        pressure_score += 8
    if literal_six_class:
        pressure_score += 10
    return {
        "collapse_overlap": collapse_overlap,
        "excludes_witness_2": excludes_witness_2,
        "literal_six_class": literal_six_class,
        "six_like": six_like,
        "pressure_units": pressure_units,
        "pressure_score": pressure_score,
    }


def constrained_hall_weight(
    coord: dict[str, Any],
    tight_masks: list[int],
    objective: str,
    dominance_cap: int,
) -> float:
    base = guided.hall_weight(coord, tight_masks, objective)
    features = coord_collapse_features(coord)
    cap_pressure = (360.0 - float(dominance_cap)) / 360.0
    return base - cap_pressure * 120.0 * features["pressure_score"]


def summarize_selected_constrained(
    selected: list[dict[str, Any]],
    tight_masks: list[int],
) -> dict[str, Any]:
    summary = guided.summarize_selected_hall(selected, tight_masks)
    literal_six = 0
    six_like = 0
    pressure_score = 0
    for coord in selected:
        features = coord_collapse_features(coord)
        literal_six += int(features["literal_six_class"])
        six_like += int(features["six_like"])
        pressure_score += int(features["pressure_score"])
    summary.update(
        {
            "target_literal_six_class_count": literal_six,
            "target_six_like_coordinate_count": six_like,
            "target_collapse_pressure_score": pressure_score,
        }
    )
    return summary


def select_coordinates_constrained(
    coords: list[dict[str, Any]],
    tight_masks: list[int],
    repair_budget: int,
    objective: str,
    dominance_cap: int,
) -> dict[str, Any]:
    n = len(coords)
    total_vars = n + joint.LIST_SIZE + 16 + len(tight_masks)
    z_offset = 0
    under_offset = n
    fiber_offset = n + joint.LIST_SIZE
    hall_under_offset = n + joint.LIST_SIZE + 16

    obj = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        obj[z_offset + idx] = -constrained_hall_weight(coord, tight_masks, objective, dominance_cap)
    obj[under_offset : under_offset + joint.LIST_SIZE] = 850.0
    obj[fiber_offset : fiber_offset + 16] = -20.0
    obj[hall_under_offset : hall_under_offset + len(tight_masks)] = 1300.0

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
        features = guided.coord_hall_features(coord, tight_masks)
        row[z_offset + idx] = features["hall_repair_row_mass"]
    rows.append(row)
    lower.append(repair_budget)
    upper.append(np.inf)

    row = np.zeros(total_vars)
    for idx, coord in enumerate(coords):
        row[z_offset + idx] = coord_collapse_features(coord)["pressure_units"]
    rows.append(row)
    lower.append(0)
    upper.append(target_six_like_cap(dominance_cap))

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
    integrality[fiber_offset : fiber_offset + 16] = 1
    upper_bounds = np.full(total_vars, np.inf)
    upper_bounds[:n] = 1
    upper_bounds[fiber_offset : fiber_offset + 16] = 1

    result = milp(
        obj,
        integrality=integrality,
        bounds=Bounds(np.zeros(total_vars), upper_bounds),
        constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
        options={"time_limit": 10},
    )
    if not result.success:
        raise RuntimeError(
            "MILP failed for "
            f"dominance_cap={dominance_cap}, objective={objective}, "
            f"repair_budget={repair_budget}: {result.message}"
        )
    chosen = [idx for idx in range(n) if int(round(result.x[z_offset + idx]))]
    if not chosen:
        raise RuntimeError("MILP chose no coordinates")
    selected = [coords[idx] for idx in chosen]
    return {
        "selected": selected,
        "milp_objective_value": float(result.fun),
        "dominance_cap": dominance_cap,
        "target_six_like_coordinate_cap": target_six_like_cap(dominance_cap),
        "repair_budget": repair_budget,
        "selection_objective": objective,
        **summarize_selected_constrained(selected, tight_masks),
    }


def classify_sample(sample: dict[str, Any], dominance_cap: int) -> str:
    assignment = sample.get("assignment")
    proxy_max = None if assignment is None else assignment["exact_max_min"]
    if sample["six_class_dominance"] > dominance_cap:
        return "HALL_REPAIR_COLLAPSE_RETURNS"
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "HALL_REPAIR_CAPACITY_LOSS"
    if sample["hall_bound"] < TARGET_AGREEMENT:
        return "HALL_REPAIR_BLOCKED_BY_CAP"
    if assignment is None:
        return "HALL_REPAIR_UNSCHEDULED"
    if proxy_max >= TARGET_AGREEMENT:
        if sample["six_class_dominance"] <= LOW_DOMINANCE_THRESHOLD:
            return "HALL_CONSTRAINED_PROXY_CANDIDATE"
        return "HALL_REPAIR_COLLAPSE_RETURNS"
    return "HALL_REPAIR_LOW_RESCHEDULE"


def sample_records(
    powers: np.ndarray,
    rref: np.ndarray,
    pivots: list[int],
    tight_masks: list[int],
    seed: int,
    dominance_cap: int,
) -> list[dict[str, Any]]:
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, SAMPLES_PER_SYSTEM)
    samples = []
    for sample_idx, vector in enumerate(vectors):
        values = joint.evaluate_vector(powers, vector)
        capacity = joint.value_class_capacity(values)
        hall_metrics = guided.value_hall_metrics(values, tight_masks)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = joint.exact_assignment_max_min(values)
        sample = {
            "sample_index": sample_idx,
            "vector_hash": guided.hash_payload(vector.tolist()),
            **capacity,
            **hall_metrics,
            "assignment": assignment,
            "six_class_dominance": soft.six_class_dominance(values),
            "collapse_classes": guided.proxy_collapse_classes(values),
            "value_class_hash": guided.hash_payload(guided.hall.value_class_masks(values)),
        }
        sample["failure_mode"] = classify_sample(sample, dominance_cap)
        sample["status"] = (
            "PROXY_A327_CONSTRAINED_ASSIGNMENT"
            if sample["failure_mode"] == "HALL_CONSTRAINED_PROXY_CANDIDATE"
            else "NO_CONSTRAINED_PROXY_A327"
        )
        samples.append(sample)
    return samples


def compact_sample(sample: dict[str, Any]) -> dict[str, Any]:
    assignment = sample.get("assignment")
    return {
        "sample_index": sample["sample_index"],
        "vector_hash": sample["vector_hash"],
        "capacity_upper_bound": sample["capacity_upper_bound"],
        "capacity_total": sample["capacity_total"],
        "hall_bound": sample["hall_bound"],
        "tight_subset_B": sample["tight_subset_B"],
        "tight_subset_deficits_to_981": sample["tight_subset_deficits_to_981"],
        "proxy_max_min": None if assignment is None else assignment["exact_max_min"],
        "agreement_vector": None if assignment is None else assignment["agreement_vector"],
        "six_class_dominance": sample["six_class_dominance"],
        "dominance_cap_satisfied": sample["six_class_dominance"] <= sample["dominance_cap"],
        "dominance_cap": sample["dominance_cap"],
        "failure_mode": sample["failure_mode"],
        "status": sample["status"],
        "value_class_hash": sample["value_class_hash"],
    }


def sample_sort_key(sample: dict[str, Any], dominance_cap: int) -> tuple[Any, ...]:
    proxy_max = -1 if sample.get("assignment") is None else sample["assignment"]["exact_max_min"]
    return (
        sample["failure_mode"] == "HALL_CONSTRAINED_PROXY_CANDIDATE",
        sample["six_class_dominance"] <= dominance_cap,
        proxy_max,
        sample["hall_bound"],
        sample["capacity_upper_bound"],
        -sample["six_class_dominance"],
        sample["sample_index"],
    )


def evaluate_system(
    powers: np.ndarray,
    source: dict[str, Any],
    tight_masks: list[int],
    repair_budget: int,
    objective: str,
    dominance_cap: int,
) -> dict[str, Any]:
    coords = balanced.candidate_coordinates(source["membership_masks"])
    selection = select_coordinates_constrained(coords, tight_masks, repair_budget, objective, dominance_cap)
    rows = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(rows, PROXY_PRIME)
    seed = int(
        guided.hash_payload(
            [source["candidate_id"], repair_budget, objective, dominance_cap, SOURCE_COMMIT]
        )[:12],
        16,
    )
    samples = sample_records(powers, rref, pivots, tight_masks, seed, dominance_cap)
    for sample in samples:
        sample["dominance_cap"] = dominance_cap
    sorted_samples = sorted(samples, key=lambda row: sample_sort_key(row, dominance_cap), reverse=True)
    retained_samples = sorted_samples[:4]
    best = retained_samples[0]
    best_overall = max(
        samples,
        key=lambda sample: (
            -1 if sample.get("assignment") is None else sample["assignment"]["exact_max_min"],
            sample["hall_bound"],
            sample["capacity_upper_bound"],
            -sample["six_class_dominance"],
        ),
    )
    collapse_returns = [
        sample for sample in samples if sample["failure_mode"] == "HALL_REPAIR_COLLAPSE_RETURNS"
    ]
    best_collapse_return = None
    if collapse_returns:
        best_collapse_return = max(
            collapse_returns,
            key=lambda sample: (
                -1 if sample.get("assignment") is None else sample["assignment"]["exact_max_min"],
                sample["hall_bound"],
                sample["capacity_upper_bound"],
                sample["six_class_dominance"],
            ),
        )
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    return {
        "target_system_id": f"{source['candidate_id']}__D{dominance_cap}__HB{repair_budget}__{objective}",
        "source_candidate_id": source["candidate_id"],
        "source_embedding_id": source["embedding_id"],
        "source_embedding_family": source["embedding_family"],
        "dominance_cap": dominance_cap,
        "repair_row_budget": repair_budget,
        "selection_objective": objective,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": len(pivots),
        "nullity": joint.VARIABLE_COUNT - len(pivots),
        "pivot_columns_hash": guided.hash_payload(pivots),
        "sample_count": len(samples),
        "best": compact_sample(best),
        "best_overall": compact_sample(best_overall),
        "best_collapse_return": None if best_collapse_return is None else compact_sample(best_collapse_return),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": sum(
            1 for sample in samples if sample["failure_mode"] == "HALL_CONSTRAINED_PROXY_CANDIDATE"
        ),
        "retained_sample_results": [compact_sample(sample) for sample in retained_samples],
        "target_rows_hash": guided.hash_payload([coord["position"] for coord in selection["selected"]]),
        **{key: value for key, value in selection.items() if key != "selected"},
    }


def source_from_parent() -> dict[str, Any]:
    guided_data = load_json(HALL_GUIDED_DATA)
    source_id = guided_data["hall_guided_search"]["source_candidate_id"]
    for source in joint.source_embeddings():
        if source["candidate_id"] == source_id:
            return source
    raise RuntimeError(f"source not found: {source_id}")


def cap_frontier(systems: list[dict[str, Any]]) -> list[dict[str, Any]]:
    frontier = []
    for dominance_cap in DOMINANCE_CAPS:
        rows = [row for row in systems if row["dominance_cap"] == dominance_cap]
        samples = [sample for row in rows for sample in row["retained_sample_results"]]
        under_cap = [sample for sample in samples if sample["six_class_dominance"] <= dominance_cap]
        pool = under_cap or samples
        if not pool:
            continue
        best = max(
            pool,
            key=lambda sample: (
                sample["failure_mode"] == "HALL_CONSTRAINED_PROXY_CANDIDATE",
                -1 if sample["proxy_max_min"] is None else sample["proxy_max_min"],
                sample["hall_bound"],
                sample["capacity_upper_bound"],
                -sample["six_class_dominance"],
            ),
        )
        frontier.append(
            {
                "dominance_cap": dominance_cap,
                "samples_under_cap": len(under_cap),
                "best_hall_bound": best["hall_bound"],
                "best_tight_subset_B": best["tight_subset_B"],
                "best_capacity_upper_bound": best["capacity_upper_bound"],
                "best_proxy_max_min": best["proxy_max_min"],
                "best_six_class_dominance": best["six_class_dominance"],
                "best_failure_mode": best["failure_mode"],
            }
        )
    return frontier


def build_record() -> dict[str, Any]:
    parent = load_json(HALL_GUIDED_DATA)
    source = source_from_parent()
    tight_masks = guided.tight_subset_masks(load_json(guided.HALL_DATA))
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    systems = []
    selection_failures = []
    for dominance_cap in DOMINANCE_CAPS:
        for repair_budget in REPAIR_ROW_BUDGETS:
            for objective in OBJECTIVES:
                try:
                    systems.append(
                        evaluate_system(powers, source, tight_masks, repair_budget, objective, dominance_cap)
                    )
                except RuntimeError as exc:
                    selection_failures.append(
                        {
                            "dominance_cap": dominance_cap,
                            "repair_row_budget": repair_budget,
                            "selection_objective": objective,
                            "error": str(exc),
                        }
                    )
    retained = sorted(
        systems,
        key=lambda row: (
            row["proxy_candidate_count"],
            row["best"]["dominance_cap_satisfied"],
            -1 if row["best"]["proxy_max_min"] is None else row["best"]["proxy_max_min"],
            row["best"]["hall_bound"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance"],
            -row["dominance_cap"],
            row["target_system_id"],
        ),
        reverse=True,
    )[:RETAINED_RESULTS]
    failure_counts: dict[str, int] = {}
    for row in systems:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    proxy_candidates = [row for row in systems if row["proxy_candidate_count"]]
    frontier = cap_frontier(systems)
    low_dominance_samples = [
        sample
        for row in systems
        for sample in row["retained_sample_results"]
        if sample["six_class_dominance"] <= LOW_DOMINANCE_THRESHOLD
    ]
    best_low_dominance_hall = (
        max(sample["hall_bound"] for sample in low_dominance_samples) if low_dominance_samples else None
    )
    collapse_return_samples = [
        row["best_collapse_return"] for row in systems if row["best_collapse_return"] is not None
    ]
    best_collapse_return = None
    if collapse_return_samples:
        best_collapse_return = max(
            collapse_return_samples,
            key=lambda sample: (
                -1 if sample["proxy_max_min"] is None else sample["proxy_max_min"],
                sample["hall_bound"],
                sample["capacity_upper_bound"],
                sample["six_class_dominance"],
            ),
        )
    best = retained[0] if retained else None
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_CONSTRAINED_HALL_REPAIR_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "collapse_constrained_hall_repair",
        "hall_baseline": {
            "best_hall_bound": parent["hall_guided_search"]["best_hall_bound"],
            "best_proxy_max_min": parent["hall_guided_search"]["best_proxy_max_min"],
            "best_agreement_vector": parent["best"]["best"]["agreement_vector"],
            "best_tight_subset_B": parent["hall_guided_search"]["best_tight_subset_B"],
            "six_class_dominance": parent["hall_guided_search"]["best_six_class_dominance"],
            "failure_mode": parent["hall_guided_search"]["best_failure_mode"],
        },
        "collapse_constrained_search": {
            "source_candidate_id": source["candidate_id"],
            "dominance_caps": DOMINANCE_CAPS,
            "target_six_like_coordinate_caps": {
                str(cap): target_six_like_cap(cap) for cap in DOMINANCE_CAPS
            },
            "repair_row_budgets": REPAIR_ROW_BUDGETS,
            "selection_objectives": OBJECTIVES,
            "systems_attempted": len(DOMINANCE_CAPS) * len(REPAIR_ROW_BUDGETS) * len(OBJECTIVES),
            "systems_tested": len(systems),
            "selection_failures": len(selection_failures),
            "samples_tested": sum(row["sample_count"] for row in systems),
            "proxy_candidates": len(proxy_candidates),
            "pareto_frontier": frontier,
            "best_proxy_max_min": None if best is None else best["best"]["proxy_max_min"],
            "best_hall_bound_under_low_dominance": best_low_dominance_hall,
            "best_capacity_upper_bound": None if best is None else best["best"]["capacity_upper_bound"],
            "best_six_class_dominance": None if best is None else best["best"]["six_class_dominance"],
            "best_failure_mode": None if best is None else best["best"]["failure_mode"],
            "best_rejected_collapse_return": best_collapse_return,
            "failure_mode_counts": dict(sorted(failure_counts.items())),
        },
        "exact_audit": {
            "triggered": bool(proxy_candidates),
            "best_exact_max_min": None,
        },
        "retained_count": len(retained),
        "retained_results": retained,
        "selection_failures": selection_failures[:16],
        "best": best,
        "result_hash": guided.hash_payload(systems),
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
