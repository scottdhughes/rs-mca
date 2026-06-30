#!/usr/bin/env python3
"""Hall repair inside low-collapse tangent skeletons for M1 a=327."""

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


HALL_DATA = Path("experimental/data/m1_a327_rescheduler_dual_hall_obstruction.json")
TANGENT_DATA = Path("experimental/data/m1_a327_collision_tangent_quotient_plane_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_tangent_skeleton_hall_repair.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "f0d758d"
BASE_TANGENT_COUNT = 5
TARGET_ROW_BUDGET = 640
REPAIR_BUDGETS = [16, 32, 64, 96]
REPAIR_FAMILIES = [
    "pair_23",
    "triples_123_234_235",
    "mixed_pair_triple",
    "fiber_balanced_pair23",
]
SAMPLES_PER_SYSTEM = 16
RETAINED_RESULTS = 32
LOW_COLLAPSE_THRESHOLD = 20
TIGHT_SUBSET_LIMIT = 3

MASK_PAIR_23 = (1 << 1) | (1 << 2)
MASK_123 = (1 << 0) | (1 << 1) | (1 << 2)
MASK_234 = (1 << 1) | (1 << 2) | (1 << 3)
MASK_235 = (1 << 1) | (1 << 2) | (1 << 4)
MASK_1234 = MASK_123 | (1 << 3)
MASK_1235 = MASK_123 | (1 << 4)
MASK_2345 = MASK_234 | (1 << 4)


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


def coord_from_mask(pos: int, mask: int, source: str, repair_gain: int = 0) -> dict[str, Any]:
    bits = joint.members(int(mask))
    return {
        "position": int(pos),
        "mask": int(mask),
        "members": bits,
        "size": len(bits),
        "row_count": max(0, len(bits) - 1),
        "fiber": int(pos) % 16,
        "has_anchor": 0 in bits,
        "source": source,
        "repair_gain": int(repair_gain),
    }


def repair_masks_for(family: str) -> list[int]:
    if family == "pair_23":
        return [MASK_PAIR_23]
    if family == "triples_123_234_235":
        return [MASK_123, MASK_234, MASK_235]
    if family == "mixed_pair_triple":
        return [MASK_PAIR_23, MASK_123, MASK_234, MASK_235, MASK_1234, MASK_1235, MASK_2345]
    if family == "fiber_balanced_pair23":
        return [MASK_PAIR_23]
    raise ValueError(f"unknown repair family: {family}")


def classes_by_position(values: list[list[int]]) -> list[list[int]]:
    return hall.value_class_masks(values)


def dominant_mask(classes: list[int]) -> int:
    return int(max(classes, key=lambda mask: (int(mask).bit_count(), int(mask))))


def base_tangent_samples() -> list[dict[str, Any]]:
    data = load_json(HALL_DATA)
    candidates = [
        row
        for row in data["samples"]
        if row["source"] == "collision_tangent_quotient_plane"
        and row["capacity_upper_bound"] >= TARGET_AGREEMENT
        and row["six_class_dominance"] <= LOW_COLLAPSE_THRESHOLD
    ]
    candidates.sort(
        key=lambda row: (
            row["rescheduler_max_min"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["hall_bound"],
            row["value_class_hash"],
        ),
        reverse=True,
    )
    selected = []
    seen = set()
    for row in candidates:
        key = row["value_class_hash"]
        if key in seen:
            continue
        seen.add(key)
        selected.append(row)
        if len(selected) >= BASE_TANGENT_COUNT:
            break
    if not selected:
        raise RuntimeError("no low-collapse tangent samples found")
    return selected


def tangent_plane_index(tangent_data: dict[str, Any]) -> dict[str, tuple[dict[str, Any], dict[str, Any], dict[str, Any]]]:
    out = {}
    for line_row in tangent_data["lines"]:
        for space in line_row["tangent_spaces"]:
            for plane in space["retained_planes"]:
                out[plane["plane_hash"]] = (line_row, space, plane)
    return out


def reconstruct_base_values(sample: dict[str, Any]) -> list[list[int]]:
    tangent_data = load_json(TANGENT_DATA)
    plane_by_hash = tangent_plane_index(tangent_data)
    line_source = hall.load_json(hall.LINE_DATA)
    line_by_hash = hall.line_rows_by_hash(line_source)
    soft_rows = hall.soft_rows_by_id()
    cache: dict[str, dict[str, Any]] = {}
    line_row = line_by_hash[sample["parent_line_hash"]]
    _line_analysis, space_row, plane_row = plane_by_hash[sample["plane_hash"]]
    return hall.reconstruct_tangent_plane_values(cache, soft_rows, line_row, space_row, plane_row)


def tight_masks_from_sample(sample: dict[str, Any]) -> list[int]:
    return [int(row["subset_mask"]) for row in sample["tight_subsets"][:TIGHT_SUBSET_LIMIT]]


def hall_contribution(classes: list[int], subset_mask: int) -> int:
    return max((int(mask) & int(subset_mask)).bit_count() for mask in classes)


def repair_gain_for(classes: list[int], repair_mask: int, tight_masks: list[int]) -> int:
    gain = 0
    for subset in tight_masks:
        current = hall_contribution(classes, subset)
        repaired = (int(repair_mask) & int(subset)).bit_count()
        gain += max(0, repaired - current)
    return gain


def repair_candidates(
    values: list[list[int]],
    tight_masks: list[int],
    family: str,
) -> list[dict[str, Any]]:
    classes = classes_by_position(values)
    candidates = []
    for pos, pos_classes in enumerate(classes):
        largest = dominant_mask(pos_classes)
        largest_size = largest.bit_count()
        for mask in repair_masks_for(family):
            gain = repair_gain_for(pos_classes, mask, tight_masks)
            if gain <= 0:
                continue
            # Stay local to coordinates that already carry nontrivial tangent
            # collision structure; otherwise this degenerates into generic
            # Hall repair.
            if largest_size < 5:
                continue
            candidates.append(
                {
                    **coord_from_mask(pos, mask, "repair", gain),
                    "base_largest_size": largest_size,
                    "base_largest_mask": largest,
                }
            )
    if family == "fiber_balanced_pair23":
        by_fiber: dict[int, list[dict[str, Any]]] = {}
        for row in candidates:
            by_fiber.setdefault(row["fiber"], []).append(row)
        for rows in by_fiber.values():
            rows.sort(
                key=lambda row: (
                    row["repair_gain"],
                    row["base_largest_size"],
                    -row["position"],
                ),
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
    classes = classes_by_position(values)
    collapse_class = sum(1 << (witness - 1) for witness in soft.COLLAPSE_CLASS_ONE_BASED)
    rows = []
    for pos, pos_classes in enumerate(classes):
        mask = dominant_mask(pos_classes)
        if mask.bit_count() < 2:
            continue
        if pos in repair_positions:
            # Let repair rows carry the local modification first.
            continue
        rows.append(coord_from_mask(pos, mask, "tangent_skeleton"))
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
    tight_masks: list[int],
    repair_budget: int,
    family: str,
) -> dict[str, Any]:
    selected = []
    repair_rows_used = 0
    repair_positions: set[int] = set()
    for coord in repair_candidates(values, tight_masks, family):
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
    return summarize_selected(selected, tight_masks, repair_budget, family)


def summarize_selected(
    selected: list[dict[str, Any]],
    tight_masks: list[int],
    repair_budget: int,
    family: str,
) -> dict[str, Any]:
    size_hist: dict[str, int] = {}
    source_hist: dict[str, int] = {}
    fiber_hist: dict[str, int] = {}
    target_b = [0] * len(tight_masks)
    repair_gain = 0
    six_class_repair_rows = 0
    for coord in selected:
        size_hist[str(coord["size"])] = size_hist.get(str(coord["size"]), 0) + 1
        source_hist[coord["source"]] = source_hist.get(coord["source"], 0) + 1
        fiber_hist[str(coord["fiber"])] = fiber_hist.get(str(coord["fiber"]), 0) + 1
        repair_gain += int(coord.get("repair_gain", 0))
        if coord["source"] == "repair":
            for idx, subset in enumerate(tight_masks):
                target_b[idx] += (coord["mask"] & subset).bit_count()
            if coord["mask"] == sum(1 << (witness - 1) for witness in soft.COLLAPSE_CLASS_ONE_BASED):
                six_class_repair_rows += coord["row_count"]
    return {
        "selected": selected,
        "repair_budget": repair_budget,
        "repair_family": family,
        "target_coordinate_count": len(selected),
        "target_row_count": sum(row["row_count"] for row in selected),
        "repair_row_count": sum(row["row_count"] for row in selected if row["source"] == "repair"),
        "tangent_skeleton_row_count": sum(row["row_count"] for row in selected if row["source"] == "tangent_skeleton"),
        "repair_coordinate_count": sum(1 for row in selected if row["source"] == "repair"),
        "repair_gain_score": repair_gain,
        "repair_target_B_proxy": target_b,
        "repair_six_class_rows": six_class_repair_rows,
        "target_size_histogram": dict(sorted(size_hist.items(), key=lambda item: int(item[0]))),
        "target_source_histogram": dict(sorted(source_hist.items())),
        "target_fiber_histogram": dict(sorted(fiber_hist.items(), key=lambda item: int(item[0]))),
    }


def classify_sample(sample: dict[str, Any], baseline: dict[str, Any]) -> str:
    if sample["hall_bound"] <= baseline["hall_bound"]:
        return "TANGENT_HALL_NOT_REPAIRED"
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "TANGENT_HALL_REPAIR_CAPACITY_LOSS"
    if sample["six_class_dominance_added_by_repair"] > LOW_COLLAPSE_THRESHOLD:
        return "TANGENT_HALL_REPAIR_COLLAPSE_RETURNS"
    assignment = sample.get("assignment")
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "TANGENT_HALL_PROXY_CANDIDATE"
    if assignment is not None:
        return "TANGENT_HALL_REPAIR_LOW_RESCHEDULE"
    return "TANGENT_HALL_REPAIR_UNSCHEDULED"


def sample_records(
    powers: np.ndarray,
    rref: np.ndarray,
    pivots: list[int],
    tight_masks: list[int],
    seed: int,
    baseline: dict[str, Any],
) -> list[dict[str, Any]]:
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, SAMPLES_PER_SYSTEM)
    rows = []
    for sample_idx, vector in enumerate(vectors):
        values = joint.evaluate_vector(powers, vector)
        capacity = joint.value_class_capacity(values)
        hall_metrics = guided.value_hall_metrics(values, tight_masks)
        assignment = None
        if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
            assignment = joint.exact_assignment_max_min(values)
        six_dom = soft.six_class_dominance(values)
        sample = {
            "sample_index": sample_idx,
            "vector_hash": guided.hash_payload(vector.tolist()),
            **capacity,
            **hall_metrics,
            "assignment": assignment,
            "six_class_dominance_total": six_dom,
            "six_class_dominance_inside_tangent_skeleton": baseline["six_class_dominance"],
            "six_class_dominance_added_by_repair": max(0, six_dom - baseline["six_class_dominance"]),
            "value_class_hash": guided.hash_payload(hall.value_class_masks(values)),
        }
        sample["failure_mode"] = classify_sample(sample, baseline)
        sample["status"] = (
            "PROXY_A327_TANGENT_HALL_ASSIGNMENT"
            if sample["failure_mode"] == "TANGENT_HALL_PROXY_CANDIDATE"
            else "NO_TANGENT_HALL_PROXY_A327"
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
        "hall_bound": sample["hall_bound"],
        "tight_subset_B": sample["tight_subset_B"],
        "tight_subset_deficits_to_981": sample["tight_subset_deficits_to_981"],
        "current_tight_subsets": sample["tight_subsets"][:5],
        "proxy_max_min": None if assignment is None else assignment["exact_max_min"],
        "agreement_vector": None if assignment is None else assignment["agreement_vector"],
        "six_class_dominance_total": sample["six_class_dominance_total"],
        "six_class_dominance_inside_tangent_skeleton": sample["six_class_dominance_inside_tangent_skeleton"],
        "six_class_dominance_added_by_repair": sample["six_class_dominance_added_by_repair"],
        "failure_mode": sample["failure_mode"],
        "status": sample["status"],
        "value_class_hash": sample["value_class_hash"],
    }


def sample_sort_key(sample: dict[str, Any]) -> tuple[Any, ...]:
    proxy_max = -1 if sample.get("assignment") is None else sample["assignment"]["exact_max_min"]
    return (
        sample["failure_mode"] == "TANGENT_HALL_PROXY_CANDIDATE",
        sample["failure_mode"] == "TANGENT_HALL_REPAIR_LOW_RESCHEDULE",
        proxy_max,
        sample["hall_bound"],
        sample["capacity_upper_bound"],
        -sample["six_class_dominance_added_by_repair"],
        -sample["six_class_dominance_total"],
    )


def evaluate_system(
    powers: np.ndarray,
    base: dict[str, Any],
    values: list[list[int]],
    repair_budget: int,
    family: str,
) -> dict[str, Any]:
    tight_masks = [int(row["subset_mask"]) for row in base["tight_subsets"][:TIGHT_SUBSET_LIMIT]]
    selection = select_target_rows(values, tight_masks, repair_budget, family)
    matrix = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(matrix, PROXY_PRIME)
    seed = int(
        guided.hash_payload([base["plane_hash"], repair_budget, family, SOURCE_COMMIT])[:12],
        16,
    )
    samples = sample_records(powers, rref, pivots, tight_masks, seed, base)
    retained_samples = sorted(samples, key=sample_sort_key, reverse=True)[:4]
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    best = retained_samples[0]
    return {
        "target_system_id": f"{base['plane_hash'][:12]}__RB{repair_budget}__{family}",
        "base_plane_hash": base["plane_hash"],
        "base_system_id": base["system_id"],
        "repair_budget": repair_budget,
        "repair_family": family,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": len(pivots),
        "nullity": joint.VARIABLE_COUNT - len(pivots),
        "pivot_columns_hash": guided.hash_payload(pivots),
        "sample_count": len(samples),
        "best": compact_sample(best),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": sum(
            1 for sample in samples if sample["failure_mode"] == "TANGENT_HALL_PROXY_CANDIDATE"
        ),
        "retained_sample_results": [compact_sample(sample) for sample in retained_samples],
        "target_rows_hash": guided.hash_payload([(row["position"], row["mask"]) for row in selection["selected"]]),
        **{key: value for key, value in selection.items() if key != "selected"},
    }


def build_record() -> dict[str, Any]:
    hall_data = load_json(HALL_DATA)
    bases = base_tangent_samples()
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    systems = []
    base_summaries = []
    for base in bases:
        values = reconstruct_base_values(base)
        base_summaries.append(
            {
                "plane_hash": base["plane_hash"],
                "system_id": base["system_id"],
                "capacity_upper_bound": base["capacity_upper_bound"],
                "proxy_max_min": base["rescheduler_max_min"],
                "hall_bound": base["hall_bound"],
                "six_class_dominance": base["six_class_dominance"],
                "tight_subset_B": [row["B_U"] for row in base["tight_subsets"][:TIGHT_SUBSET_LIMIT]],
                "agreement_vector": base["agreement_vector"],
            }
        )
        for repair_budget in REPAIR_BUDGETS:
            for family in REPAIR_FAMILIES:
                systems.append(evaluate_system(powers, base, values, repair_budget, family))
    retained = sorted(
        systems,
        key=lambda row: (
            row["proxy_candidate_count"],
            row["best"]["failure_mode"] == "TANGENT_HALL_REPAIR_LOW_RESCHEDULE",
            -1 if row["best"]["proxy_max_min"] is None else row["best"]["proxy_max_min"],
            row["best"]["hall_bound"],
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
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_TANGENT_HALL_REPAIR_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "tangent_skeleton_hall_repair",
        "tangent_baseline": {
            "proxy_max_min": hall_data["best_sample"]["rescheduler_max_min"],
            "capacity": hall_data["best_sample"]["capacity_upper_bound"],
            "six_class_dominance": hall_data["best_sample"]["six_class_dominance"],
            "hall_bound": hall_data["best_sample"]["hall_bound"],
            "tight_subsets": hall_data["best_sample"]["tight_subsets"][:TIGHT_SUBSET_LIMIT],
        },
        "tangent_hall_repair": {
            "base_tangent_systems": len(bases),
            "base_tangent_summaries": base_summaries,
            "systems_tested": len(systems),
            "repair_budgets": REPAIR_BUDGETS,
            "repair_families": REPAIR_FAMILIES,
            "samples_tested": sum(row["sample_count"] for row in systems),
            "proxy_candidates": len(proxy_candidates),
            "best_proxy_max_min": best["best"]["proxy_max_min"],
            "best_hall_bound": best["best"]["hall_bound"],
            "best_capacity": best["best"]["capacity_upper_bound"],
            "best_six_class_dominance_total": best["best"]["six_class_dominance_total"],
            "best_six_class_dominance_added_by_repair": best["best"]["six_class_dominance_added_by_repair"],
            "best_agreement_vector": best["best"]["agreement_vector"],
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
