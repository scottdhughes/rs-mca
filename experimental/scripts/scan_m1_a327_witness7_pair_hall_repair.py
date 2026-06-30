#!/usr/bin/env python3
"""Witness-7 pair Hall repair inside the repaired tangent skeleton."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_hall_guided_target_mutation as guided
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_rescheduler_dual_hall_obstruction as hall
import scan_m1_a327_soft_collapse_penalty_target_solver as soft
import scan_m1_a327_tangent_skeleton_hall_repair as tangent_hall


PARENT_DATA = Path("experimental/data/m1_a327_tangent_skeleton_hall_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_witness7_pair_hall_repair.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "d1fd9d0"
BASE_SYSTEM_COUNT = 5
TARGET_ROW_BUDGET = 640
REPAIR_BUDGETS = [8, 16, 24, 32, 48]
REPAIR_FAMILIES = [
    "pair_i7",
    "triple_i_j_7",
    "mixed_pair_triple_7",
    "quotient_fiber_balanced_i7",
    "residual_pair_i7",
]
SAMPLES_PER_SYSTEM = 16
RETAINED_RESULTS = 40
LOW_ADDED_COLLAPSE_THRESHOLD = 20

PAIR7_MASKS = [
    (1 << 0) | (1 << 6),
    (1 << 1) | (1 << 6),
    (1 << 2) | (1 << 6),
    (1 << 3) | (1 << 6),
    (1 << 4) | (1 << 6),
]
PAIR67_MASK = (1 << 5) | (1 << 6)
TRIPLE_IJ7_MASKS = [
    (1 << 0) | (1 << 1) | (1 << 6),
    (1 << 1) | (1 << 2) | (1 << 6),
    (1 << 2) | (1 << 3) | (1 << 6),
    (1 << 3) | (1 << 4) | (1 << 6),
    (1 << 4) | (1 << 5) | (1 << 6),
]
WITNESS6_GUARD_MASKS = [
    PAIR67_MASK,
    (1 << 0) | (1 << 5) | (1 << 6),
    (1 << 1) | (1 << 5) | (1 << 6),
]
OLD_THREE_SUBSET_MASKS = [
    (1 << 0) | (1 << 1) | (1 << 2),
    (1 << 1) | (1 << 2) | (1 << 3),
    (1 << 1) | (1 << 2) | (1 << 4),
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


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def repair_masks_for(family: str) -> list[int]:
    if family == "pair_i7":
        return PAIR7_MASKS
    if family == "triple_i_j_7":
        return TRIPLE_IJ7_MASKS
    if family == "mixed_pair_triple_7":
        return PAIR7_MASKS + TRIPLE_IJ7_MASKS + WITNESS6_GUARD_MASKS
    if family == "quotient_fiber_balanced_i7":
        return PAIR7_MASKS
    if family == "residual_pair_i7":
        return PAIR7_MASKS
    raise ValueError(f"unknown repair family: {family}")


def parent_base_by_plane() -> dict[str, dict[str, Any]]:
    bases = tangent_hall.base_tangent_samples()
    return {base["plane_hash"]: base for base in bases}


def retained_parent_systems() -> list[dict[str, Any]]:
    data = load_json(PARENT_DATA)
    rows = []
    seen = set()
    for row in data["retained_results"]:
        best = row["best"]
        if best["failure_mode"] != "TANGENT_HALL_REPAIR_LOW_RESCHEDULE":
            continue
        if best["six_class_dominance_added_by_repair"] > LOW_ADDED_COLLAPSE_THRESHOLD:
            continue
        key = best["value_class_hash"]
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)
        if len(rows) >= BASE_SYSTEM_COUNT:
            break
    if not rows:
        raise RuntimeError("no repaired tangent systems found")
    return rows


def reconstruct_parent_values(parent_row: dict[str, Any]) -> tuple[dict[str, Any], list[list[int]]]:
    base = parent_base_by_plane()[parent_row["base_plane_hash"]]
    base_values = tangent_hall.reconstruct_base_values(base)
    old_tight_masks = [int(row["subset_mask"]) for row in base["tight_subsets"][:3]]
    selection = tangent_hall.select_target_rows(
        base_values,
        old_tight_masks,
        int(parent_row["repair_budget"]),
        parent_row["repair_family"],
    )
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    matrix = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(matrix, PROXY_PRIME)
    seed = int(
        guided.hash_payload(
            [base["plane_hash"], parent_row["repair_budget"], parent_row["repair_family"], tangent_hall.SOURCE_COMMIT]
        )[:12],
        16,
    )
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, tangent_hall.SAMPLES_PER_SYSTEM)
    sample_index = int(parent_row["best"]["sample_index"])
    vector = vectors[sample_index]
    values = joint.evaluate_vector(powers, vector)
    if guided.hash_payload(vector.tolist()) != parent_row["best"]["vector_hash"]:
        raise RuntimeError("parent vector reconstruction hash mismatch")
    return {
        "base_plane_hash": parent_row["base_plane_hash"],
        "parent_target_system_id": parent_row["target_system_id"],
        "parent_repair_budget": parent_row["repair_budget"],
        "parent_repair_family": parent_row["repair_family"],
        "parent_sample_index": sample_index,
        "parent_vector_hash": parent_row["best"]["vector_hash"],
        "parent_value_class_hash": parent_row["best"]["value_class_hash"],
        "parent_proxy_max_min": parent_row["best"]["proxy_max_min"],
        "parent_hall_bound": parent_row["best"]["hall_bound"],
        "parent_capacity": parent_row["best"]["capacity_upper_bound"],
        "parent_six_class_dominance_total": parent_row["best"]["six_class_dominance_total"],
        "parent_added_six_class_dominance": parent_row["best"]["six_class_dominance_added_by_repair"],
        "parent_agreement_vector": parent_row["best"]["agreement_vector"],
        "old_tight_subset_B": parent_row["best"]["tight_subset_B"],
        "current_tight_subsets": parent_row["best"]["current_tight_subsets"],
    }, values


def pair7_masks_from_parent(parent: dict[str, Any]) -> list[int]:
    masks = [
        int(row["subset_mask"])
        for row in parent["current_tight_subsets"]
        if len(row["subset"]) == 2 and 7 in row["subset"]
    ]
    if len(masks) < 5:
        return PAIR7_MASKS
    return masks[:5]


def hall_contribution(classes: list[int], subset_mask: int) -> int:
    return max((int(mask) & int(subset_mask)).bit_count() for mask in classes)


def pair7_values(values: list[list[int]], pair_masks: list[int]) -> list[int]:
    classes_by_pos = hall.value_class_masks(values)
    out = []
    for subset in pair_masks:
        out.append(sum(hall_contribution(classes, subset) for classes in classes_by_pos))
    return out


def pair7_metrics(values: list[list[int]], pair_masks: list[int]) -> dict[str, Any]:
    pair_b = pair7_values(values, pair_masks)
    return {
        "pair7_B_values": pair_b,
        "min_pair7_B": min(pair_b),
        "pair7_deficits_to_654": [2 * TARGET_AGREEMENT - value for value in pair_b],
        "pair7_hall_bound": min(value // 2 for value in pair_b),
    }


def repair_gain_for(classes: list[int], repair_mask: int, pair_masks: list[int]) -> int:
    gain = 0
    for subset in pair_masks:
        current = hall_contribution(classes, subset)
        repaired = (int(repair_mask) & int(subset)).bit_count()
        gain += max(0, repaired - current)
    return gain


def repair_candidates(values: list[list[int]], pair_masks: list[int], family: str) -> list[dict[str, Any]]:
    classes_by_pos = hall.value_class_masks(values)
    candidates = []
    for pos, classes in enumerate(classes_by_pos):
        largest = tangent_hall.dominant_mask(classes)
        largest_size = largest.bit_count()
        for mask in repair_masks_for(family):
            gain = repair_gain_for(classes, mask, pair_masks)
            if gain <= 0:
                continue
            if largest_size < 5:
                continue
            if family == "residual_pair_i7" and largest_size >= 7:
                continue
            candidates.append(
                {
                    **tangent_hall.coord_from_mask(pos, mask, "pair7_repair", gain),
                    "base_largest_size": largest_size,
                    "base_largest_mask": largest,
                }
            )
    if family == "quotient_fiber_balanced_i7":
        by_fiber: dict[int, list[dict[str, Any]]] = {}
        for row in candidates:
            by_fiber.setdefault(row["fiber"], []).append(row)
        for rows in by_fiber.values():
            rows.sort(
                key=lambda row: (row["repair_gain"], row["base_largest_size"], -row["position"]),
                reverse=True,
            )
        balanced_rows = []
        while True:
            progressed = False
            for fiber in sorted(by_fiber):
                if by_fiber[fiber]:
                    balanced_rows.append(by_fiber[fiber].pop(0))
                    progressed = True
            if not progressed:
                break
        return balanced_rows
    candidates.sort(
        key=lambda row: (
            row["repair_gain"],
            row["base_largest_size"],
            -row["fiber"],
            -row["position"],
        ),
        reverse=True,
    )
    return candidates


def skeleton_candidates(values: list[list[int]], repair_positions: set[int]) -> list[dict[str, Any]]:
    classes_by_pos = hall.value_class_masks(values)
    collapse_class = sum(1 << (witness - 1) for witness in soft.COLLAPSE_CLASS_ONE_BASED)
    rows = []
    for pos, classes in enumerate(classes_by_pos):
        mask = tangent_hall.dominant_mask(classes)
        if pos in repair_positions or mask.bit_count() < 2:
            continue
        rows.append(tangent_hall.coord_from_mask(pos, mask, "repaired_tangent_skeleton"))
        rows[-1]["is_collapse_class"] = int(mask == collapse_class)
    rows.sort(
        key=lambda row: (
            -row["is_collapse_class"],
            row["size"],
            row["fiber"],
            -row["position"],
        ),
        reverse=True,
    )
    return rows


def select_target_rows(
    values: list[list[int]],
    pair_masks: list[int],
    repair_budget: int,
    family: str,
) -> dict[str, Any]:
    selected = []
    repair_rows_used = 0
    repair_positions: set[int] = set()
    for coord in repair_candidates(values, pair_masks, family):
        if repair_rows_used + coord["row_count"] > repair_budget:
            continue
        key = (coord["position"], coord["mask"])
        if any((row["position"], row["mask"]) == key for row in selected):
            continue
        selected.append(coord)
        repair_rows_used += coord["row_count"]
        repair_positions.add(coord["position"])
        if repair_rows_used >= repair_budget:
            break
    remaining_budget = TARGET_ROW_BUDGET - sum(row["row_count"] for row in selected)
    for coord in skeleton_candidates(values, repair_positions):
        if coord["row_count"] > remaining_budget:
            continue
        selected.append(coord)
        remaining_budget -= coord["row_count"]
        if remaining_budget <= 0:
            break
    if not selected:
        raise RuntimeError("selected no target rows")
    return summarize_selected(selected, pair_masks, repair_budget, family)


def summarize_selected(
    selected: list[dict[str, Any]],
    pair_masks: list[int],
    repair_budget: int,
    family: str,
) -> dict[str, Any]:
    size_hist: dict[str, int] = {}
    source_hist: dict[str, int] = {}
    fiber_hist: dict[str, int] = {}
    repair_pair_b = [0] * len(pair_masks)
    repair_gain = 0
    for coord in selected:
        size_hist[str(coord["size"])] = size_hist.get(str(coord["size"]), 0) + 1
        source_hist[coord["source"]] = source_hist.get(coord["source"], 0) + 1
        fiber_hist[str(coord["fiber"])] = fiber_hist.get(str(coord["fiber"]), 0) + 1
        repair_gain += int(coord.get("repair_gain", 0))
        if coord["source"] == "pair7_repair":
            for idx, subset in enumerate(pair_masks):
                repair_pair_b[idx] += (coord["mask"] & subset).bit_count()
    return {
        "selected": selected,
        "repair_budget": repair_budget,
        "repair_family": family,
        "target_coordinate_count": len(selected),
        "target_row_count": sum(row["row_count"] for row in selected),
        "repair_row_count": sum(row["row_count"] for row in selected if row["source"] == "pair7_repair"),
        "repaired_tangent_skeleton_row_count": sum(row["row_count"] for row in selected if row["source"] == "repaired_tangent_skeleton"),
        "repair_coordinate_count": sum(1 for row in selected if row["source"] == "pair7_repair"),
        "repair_gain_score": repair_gain,
        "repair_pair7_B_proxy": repair_pair_b,
        "target_size_histogram": dict(sorted(size_hist.items(), key=lambda item: int(item[0]))),
        "target_source_histogram": dict(sorted(source_hist.items())),
        "target_fiber_histogram": dict(sorted(fiber_hist.items(), key=lambda item: int(item[0]))),
    }


def classify_sample(sample: dict[str, Any]) -> str:
    if sample["min_pair7_B"] < 2 * TARGET_AGREEMENT:
        return "PAIR7_NOT_REPAIRED"
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "PAIR7_REPAIR_CAPACITY_LOSS"
    if sample["six_class_dominance_added_by_repair"] > LOW_ADDED_COLLAPSE_THRESHOLD:
        return "PAIR7_REPAIR_COLLAPSE_RETURNS"
    assignment = sample.get("assignment")
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "PAIR7_PROXY_CANDIDATE"
    if assignment is not None:
        return "PAIR7_REPAIR_LOW_RESCHEDULE"
    return "PAIR7_REPAIR_UNSCHEDULED"


def sample_records(
    powers: np.ndarray,
    rref: np.ndarray,
    pivots: list[int],
    pair_masks: list[int],
    seed: int,
    parent: dict[str, Any],
) -> list[dict[str, Any]]:
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, SAMPLES_PER_SYSTEM)
    rows = []
    for sample_idx, vector in enumerate(vectors):
        values = joint.evaluate_vector(powers, vector)
        capacity = joint.value_class_capacity(values)
        hall_record = guided.value_hall_metrics(values, OLD_THREE_SUBSET_MASKS)
        pair_record = pair7_metrics(values, pair_masks)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = joint.exact_assignment_max_min(values)
        six_dom = soft.six_class_dominance(values)
        sample = {
            "sample_index": sample_idx,
            "vector_hash": guided.hash_payload(vector.tolist()),
            **capacity,
            **pair_record,
            "old_three_subset_B_values": hall_record["tight_subset_B"],
            "old_three_subset_min_hall_bound": min(value // 3 for value in hall_record["tight_subset_B"]),
            "global_hall_bound": hall_record["hall_bound"],
            "current_tight_subsets": hall_record["tight_subsets"][:5],
            "assignment": assignment,
            "six_class_dominance_total": six_dom,
            "six_class_dominance_inside_repaired_skeleton": parent["parent_six_class_dominance_total"],
            "six_class_dominance_added_by_repair": max(0, six_dom - parent["parent_six_class_dominance_total"]),
            "value_class_hash": guided.hash_payload(hall.value_class_masks(values)),
        }
        sample["failure_mode"] = classify_sample(sample)
        sample["status"] = (
            "PROXY_A327_PAIR7_ASSIGNMENT"
            if sample["failure_mode"] == "PAIR7_PROXY_CANDIDATE"
            else "NO_PAIR7_PROXY_A327"
        )
        rows.append(sample)
    return rows


def compact_sample(sample: dict[str, Any]) -> dict[str, Any]:
    assignment = sample.get("assignment")
    return {
        "sample_index": sample["sample_index"],
        "vector_hash": sample["vector_hash"],
        "capacity_upper_bound": sample["capacity_upper_bound"],
        "capacity_total": sample["capacity_total"],
        "pair7_B_values": sample["pair7_B_values"],
        "min_pair7_B": sample["min_pair7_B"],
        "pair7_deficits_to_654": sample["pair7_deficits_to_654"],
        "pair7_hall_bound": sample["pair7_hall_bound"],
        "old_three_subset_B_values": sample["old_three_subset_B_values"],
        "old_three_subset_min_hall_bound": sample["old_three_subset_min_hall_bound"],
        "global_hall_bound": sample["global_hall_bound"],
        "current_tight_subsets": sample["current_tight_subsets"],
        "proxy_max_min": None if assignment is None else assignment["exact_max_min"],
        "agreement_vector": None if assignment is None else assignment["agreement_vector"],
        "six_class_dominance_total": sample["six_class_dominance_total"],
        "six_class_dominance_inside_repaired_skeleton": sample["six_class_dominance_inside_repaired_skeleton"],
        "six_class_dominance_added_by_repair": sample["six_class_dominance_added_by_repair"],
        "failure_mode": sample["failure_mode"],
        "status": sample["status"],
        "value_class_hash": sample["value_class_hash"],
    }


def sample_sort_key(sample: dict[str, Any]) -> tuple[Any, ...]:
    proxy_max = -1 if sample.get("assignment") is None else sample["assignment"]["exact_max_min"]
    return (
        sample["failure_mode"] == "PAIR7_PROXY_CANDIDATE",
        sample["failure_mode"] == "PAIR7_REPAIR_LOW_RESCHEDULE",
        proxy_max,
        sample["min_pair7_B"],
        sample["capacity_upper_bound"],
        -sample["six_class_dominance_added_by_repair"],
        -sample["six_class_dominance_total"],
    )


def evaluate_system(
    powers: np.ndarray,
    parent: dict[str, Any],
    values: list[list[int]],
    pair_masks: list[int],
    repair_budget: int,
    family: str,
) -> dict[str, Any]:
    selection = select_target_rows(values, pair_masks, repair_budget, family)
    matrix = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(matrix, PROXY_PRIME)
    seed = int(
        guided.hash_payload([parent["parent_value_class_hash"], repair_budget, family, SOURCE_COMMIT])[:12],
        16,
    )
    samples = sample_records(powers, rref, pivots, pair_masks, seed, parent)
    retained_samples = sorted(samples, key=sample_sort_key, reverse=True)[:4]
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    best = retained_samples[0]
    return {
        "target_system_id": f"{parent['parent_value_class_hash'][:12]}__RB{repair_budget}__{family}",
        "parent_target_system_id": parent["parent_target_system_id"],
        "parent_value_class_hash": parent["parent_value_class_hash"],
        "repair_budget": repair_budget,
        "repair_family": family,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": len(pivots),
        "nullity": joint.VARIABLE_COUNT - len(pivots),
        "pivot_columns_hash": guided.hash_payload(pivots),
        "sample_count": len(samples),
        "best": compact_sample(best),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": sum(1 for sample in samples if sample["failure_mode"] == "PAIR7_PROXY_CANDIDATE"),
        "retained_sample_results": [compact_sample(sample) for sample in retained_samples],
        "target_rows_hash": guided.hash_payload([(row["position"], row["mask"]) for row in selection["selected"]]),
        **{key: value for key, value in selection.items() if key != "selected"},
    }


def build_record() -> dict[str, Any]:
    parent_data = load_json(PARENT_DATA)
    parent_rows = retained_parent_systems()
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    systems = []
    parent_summaries = []
    for row in parent_rows:
        parent, values = reconstruct_parent_values(row)
        pair_masks = pair7_masks_from_parent(parent)
        parent_pair = pair7_metrics(values, pair_masks)
        parent_summaries.append({**parent, **parent_pair})
        for repair_budget in REPAIR_BUDGETS:
            for family in REPAIR_FAMILIES:
                systems.append(evaluate_system(powers, parent, values, pair_masks, repair_budget, family))
    retained = sorted(
        systems,
        key=lambda row: (
            row["proxy_candidate_count"],
            row["best"]["failure_mode"] == "PAIR7_REPAIR_LOW_RESCHEDULE",
            -1 if row["best"]["proxy_max_min"] is None else row["best"]["proxy_max_min"],
            row["best"]["min_pair7_B"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance_added_by_repair"],
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
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_PAIR7_REPAIR_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "witness7_pair_hall_repair",
        "tangent_hall_baseline": {
            "proxy_max_min": parent_data["tangent_hall_repair"]["best_proxy_max_min"],
            "capacity": parent_data["tangent_hall_repair"]["best_capacity"],
            "six_class_dominance_total": parent_data["tangent_hall_repair"]["best_six_class_dominance_total"],
            "added_six_class_dominance": parent_data["tangent_hall_repair"]["best_six_class_dominance_added_by_repair"],
            "agreement_vector": parent_data["tangent_hall_repair"]["best_agreement_vector"],
            "old_tight_subsets_B": parent_data["best"]["best"]["tight_subset_B"],
            "new_tight_pairs": parent_data["best"]["best"]["current_tight_subsets"][:5],
        },
        "witness7_pair_repair": {
            "base_systems": len(parent_rows),
            "base_summaries": parent_summaries,
            "systems_tested": len(systems),
            "repair_budgets": REPAIR_BUDGETS,
            "repair_families": REPAIR_FAMILIES,
            "samples_tested": sum(row["sample_count"] for row in systems),
            "proxy_candidates": len(proxy_candidates),
            "best_proxy_max_min": best["best"]["proxy_max_min"],
            "best_capacity": best["best"]["capacity_upper_bound"],
            "best_min_pair_B": best["best"]["min_pair7_B"],
            "best_pair_B_values": best["best"]["pair7_B_values"],
            "best_added_six_class_dominance": best["best"]["six_class_dominance_added_by_repair"],
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
