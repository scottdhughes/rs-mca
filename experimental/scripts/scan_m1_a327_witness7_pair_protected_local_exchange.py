#!/usr/bin/env python3
"""Protected local exchange around the stage-1 witness-7 pair Hall incumbent."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_hall_guided_target_mutation as guided
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_rescheduler_dual_hall_obstruction as hall
import scan_m1_a327_soft_collapse_penalty_target_solver as soft
import scan_m1_a327_witness7_pair_hall_repair as stage1


STAGE1_DATA = Path("experimental/data/m1_a327_witness7_pair_hall_repair.json")
STAGE2_DATA = Path("experimental/data/m1_a327_witness7_pair_hall_repair_stage2.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_witness7_pair_protected_local_exchange.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "ad2ed83"
BASE_SYSTEM_COUNT = 1
TARGET_ROW_BUDGET = 640
EXCHANGE_BUDGETS = [8, 16, 24, 32, 48]
EXCHANGE_MOVES = [
    "one_for_one",
    "two_for_one",
    "one_for_two",
    "fiber_local",
    "balanced_five_pair",
    "residual_patch",
]
SAMPLES_PER_SYSTEM = 16
RETAINED_RESULTS = 40
LOW_ADDED_COLLAPSE_THRESHOLD = 20

PAIR7_MASKS = stage1.PAIR7_MASKS
TRIPLE_I7_MASKS = [
    (1 << 0) | (1 << 1) | (1 << 6),
    (1 << 1) | (1 << 2) | (1 << 6),
    (1 << 2) | (1 << 3) | (1 << 6),
    (1 << 3) | (1 << 4) | (1 << 6),
    (1 << 0) | (1 << 4) | (1 << 6),
]
QUAD_I7_MASKS = [
    (1 << 0) | (1 << 1) | (1 << 2) | (1 << 6),
    (1 << 1) | (1 << 2) | (1 << 3) | (1 << 6),
    (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6),
    (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6),
    (1 << 0) | (1 << 1) | (1 << 4) | (1 << 6),
]
OLD_THREE_SUBSET_MASKS = stage1.OLD_THREE_SUBSET_MASKS


def jsonable(payload: object) -> object:
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


def row_key(row: dict[str, Any]) -> tuple[int, int]:
    return int(row["position"]), int(row["mask"])


def retained_stage1_bases() -> list[dict[str, Any]]:
    data = load_json(STAGE1_DATA)
    rows = []
    seen = set()
    for row in data["retained_results"]:
        best = row["best"]
        if best["failure_mode"] != "PAIR7_NOT_REPAIRED":
            continue
        if best["proxy_max_min"] is None or best["proxy_max_min"] < 315:
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
        raise RuntimeError("no stage-1 incumbent found")
    return rows


def reconstruct_stage1_state(stage1_row: dict[str, Any]) -> tuple[dict[str, Any], list[list[int]], list[dict[str, Any]]]:
    parent = None
    parent_values = None
    for candidate in stage1.retained_parent_systems():
        candidate_parent, candidate_values = stage1.reconstruct_parent_values(candidate)
        if candidate_parent["parent_value_class_hash"] == stage1_row["parent_value_class_hash"]:
            parent = candidate_parent
            parent_values = candidate_values
            break
    if parent is None or parent_values is None:
        raise RuntimeError("stage-1 parent not found")

    pair_masks = stage1.pair7_masks_from_parent(parent)
    selection = stage1.select_target_rows(
        parent_values,
        pair_masks,
        int(stage1_row["repair_budget"]),
        stage1_row["repair_family"],
    )
    target_hash = guided.hash_payload([(row["position"], row["mask"]) for row in selection["selected"]])
    if target_hash != stage1_row["target_rows_hash"]:
        raise RuntimeError("stage-1 target row reconstruction hash mismatch")

    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    matrix = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(matrix, PROXY_PRIME)
    seed = int(
        guided.hash_payload(
            [parent["parent_value_class_hash"], stage1_row["repair_budget"], stage1_row["repair_family"], stage1.SOURCE_COMMIT]
        )[:12],
        16,
    )
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, stage1.SAMPLES_PER_SYSTEM)
    sample_index = int(stage1_row["best"]["sample_index"])
    vector = vectors[sample_index]
    if guided.hash_payload(vector.tolist()) != stage1_row["best"]["vector_hash"]:
        raise RuntimeError("stage-1 vector reconstruction hash mismatch")
    values = joint.evaluate_vector(powers, vector)

    protected = [row for row in selection["selected"] if row["source"] == "pair7_repair"]
    exchangeable = [row for row in selection["selected"] if row["source"] != "pair7_repair"]
    if not protected or not exchangeable:
        raise RuntimeError("stage-1 selection lacks protected or exchangeable rows")

    base = {
        "stage1_target_system_id": stage1_row["target_system_id"],
        "stage1_value_class_hash": stage1_row["best"]["value_class_hash"],
        "stage1_vector_hash": stage1_row["best"]["vector_hash"],
        "stage1_proxy_max_min": stage1_row["best"]["proxy_max_min"],
        "stage1_capacity": stage1_row["best"]["capacity_upper_bound"],
        "stage1_pair_B_values": stage1_row["best"]["pair7_B_values"],
        "stage1_min_pair_B": stage1_row["best"]["min_pair7_B"],
        "stage1_pair_deficits_to_654": stage1_row["best"]["pair7_deficits_to_654"],
        "stage1_added_six_class_dominance": stage1_row["best"]["six_class_dominance_added_by_repair"],
        "stage1_six_class_dominance_total": stage1_row["best"]["six_class_dominance_total"],
        "stage1_agreement_vector": stage1_row["best"]["agreement_vector"],
        "old_three_subset_B": stage1_row["best"]["old_three_subset_B_values"],
        "pair_masks": pair_masks,
        "protected_rows": len(protected),
        "protected_row_count": sum(row["row_count"] for row in protected),
        "exchangeable_rows": len(exchangeable),
        "exchangeable_row_count": sum(row["row_count"] for row in exchangeable),
        "stage1_target_row_count": selection["target_row_count"],
        "stage1_target_coordinate_count": selection["target_coordinate_count"],
        "stage1_target_rows_hash": target_hash,
    }
    return base, values, selection["selected"]


def repair_masks_for(move: str) -> list[int]:
    if move == "one_for_one":
        return PAIR7_MASKS + TRIPLE_I7_MASKS
    if move == "two_for_one":
        return TRIPLE_I7_MASKS + QUAD_I7_MASKS
    if move == "one_for_two":
        return PAIR7_MASKS
    if move == "fiber_local":
        return PAIR7_MASKS + TRIPLE_I7_MASKS
    if move == "balanced_five_pair":
        return TRIPLE_I7_MASKS + QUAD_I7_MASKS
    if move == "residual_patch":
        return PAIR7_MASKS + TRIPLE_I7_MASKS
    raise ValueError(f"unknown exchange move: {move}")


def repair_gain_for(classes: list[int], repair_mask: int, pair_masks: list[int]) -> int:
    gain = 0
    for subset in pair_masks:
        current = stage1.hall_contribution(classes, subset)
        repaired = (int(repair_mask) & int(subset)).bit_count()
        gain += max(0, repaired - current)
    return gain


def repair_candidates(
    values: list[list[int]],
    pair_masks: list[int],
    move: str,
    protected_keys: set[tuple[int, int]],
    selected_keys: set[tuple[int, int]],
) -> list[dict[str, Any]]:
    classes_by_pos = hall.value_class_masks(values)
    rows = []
    for pos, classes in enumerate(classes_by_pos):
        largest = stage1.tangent_hall.dominant_mask(classes)
        largest_size = largest.bit_count()
        if largest_size < 5:
            continue
        if move == "residual_patch" and largest_size >= 7:
            continue
        for mask in repair_masks_for(move):
            key = (pos, mask)
            if key in protected_keys or key in selected_keys:
                continue
            gain = repair_gain_for(classes, mask, pair_masks)
            if gain <= 0:
                continue
            rows.append(
                {
                    **stage1.tangent_hall.coord_from_mask(pos, mask, "protected_exchange_repair", gain),
                    "base_largest_size": largest_size,
                    "base_largest_mask": largest,
                }
            )
    rows.sort(
        key=lambda row: (
            row["repair_gain"],
            row["base_largest_size"],
            -abs(7 - row["fiber"]),
            -row["position"],
        ),
        reverse=True,
    )
    if move == "fiber_local":
        by_fiber: dict[int, list[dict[str, Any]]] = {}
        for row in rows:
            by_fiber.setdefault(row["fiber"], []).append(row)
        best_fibers = sorted(
            by_fiber,
            key=lambda fiber: (sum(row["repair_gain"] for row in by_fiber[fiber]), len(by_fiber[fiber])),
            reverse=True,
        )[:2]
        return [row for fiber in best_fibers for row in by_fiber[fiber]]
    if move == "balanced_five_pair":
        balanced_rows = []
        wanted = list(pair_masks)
        for subset in wanted * 16:
            candidates = [row for row in rows if (row["mask"] & subset).bit_count() >= 2 and row not in balanced_rows]
            if candidates:
                balanced_rows.append(candidates[0])
        return balanced_rows or rows
    return rows


def exchangeable_order(selected: list[dict[str, Any]], move: str) -> list[dict[str, Any]]:
    rows = [row for row in selected if row["source"] != "pair7_repair"]
    if move == "fiber_local":
        rows.sort(key=lambda row: (row["fiber"] not in {6, 7, 8, 9}, row["fiber"], -row["position"]))
    elif move == "residual_patch":
        rows.sort(key=lambda row: (-row["position"], -row["fiber"]))
    else:
        rows.sort(key=lambda row: (row["fiber"], -row["position"]))
    return rows


def skeleton_refill_candidates(
    values: list[list[int]],
    blocked_keys: set[tuple[int, int]],
    blocked_positions: set[int],
) -> list[dict[str, Any]]:
    classes_by_pos = hall.value_class_masks(values)
    collapse_class = sum(1 << (witness - 1) for witness in soft.COLLAPSE_CLASS_ONE_BASED)
    rows = []
    for pos, classes in enumerate(classes_by_pos):
        mask = stage1.tangent_hall.dominant_mask(classes)
        key = (pos, mask)
        if mask.bit_count() < 2 or key in blocked_keys or pos in blocked_positions:
            continue
        coord = stage1.tangent_hall.coord_from_mask(pos, mask, "protected_exchange_refill")
        coord["is_collapse_class"] = int(mask == collapse_class)
        rows.append(coord)
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


def select_exchange_rows(
    values: list[list[int]],
    base: dict[str, Any],
    original_selected: list[dict[str, Any]],
    exchange_budget: int,
    move: str,
) -> dict[str, Any]:
    protected = [row for row in original_selected if row["source"] == "pair7_repair"]
    protected_keys = {row_key(row) for row in protected}
    selected_keys = {row_key(row) for row in original_selected}
    removed = []
    freed = 0
    remove_target = exchange_budget * (2 if move == "two_for_one" else 1)
    for row in exchangeable_order(original_selected, move):
        removed.append(row)
        freed += row["row_count"]
        if freed >= remove_target:
            break
    removed_keys = {row_key(row) for row in removed}
    removed_positions = {int(row["position"]) for row in removed}

    kept = [row for row in original_selected if row_key(row) not in removed_keys]
    selected = list(kept)
    row_budget = TARGET_ROW_BUDGET - sum(row["row_count"] for row in selected)
    repair_rows = []
    repair_positions: set[int] = set()
    for candidate in repair_candidates(values, base["pair_masks"], move, protected_keys, selected_keys):
        if candidate["position"] in repair_positions:
            continue
        if candidate["row_count"] > row_budget:
            continue
        selected.append(candidate)
        repair_rows.append(candidate)
        repair_positions.add(int(candidate["position"]))
        row_budget -= candidate["row_count"]
        if row_budget <= 0:
            break

    blocked_keys = {row_key(row) for row in selected} | removed_keys
    blocked_positions = repair_positions
    refill_rows = []
    for candidate in skeleton_refill_candidates(values, blocked_keys, blocked_positions):
        if candidate["row_count"] > row_budget:
            continue
        selected.append(candidate)
        refill_rows.append(candidate)
        row_budget -= candidate["row_count"]
        if row_budget <= 0:
            break
    return summarize_selected(selected, protected, removed, repair_rows, refill_rows, exchange_budget, move)


def summarize_selected(
    selected: list[dict[str, Any]],
    protected: list[dict[str, Any]],
    removed: list[dict[str, Any]],
    repair_rows: list[dict[str, Any]],
    refill_rows: list[dict[str, Any]],
    exchange_budget: int,
    move: str,
) -> dict[str, Any]:
    size_hist: dict[str, int] = {}
    source_hist: dict[str, int] = {}
    fiber_hist: dict[str, int] = {}
    repair_pair_b = [0] * len(PAIR7_MASKS)
    repair_gain = 0
    for coord in selected:
        size_hist[str(coord["size"])] = size_hist.get(str(coord["size"]), 0) + 1
        source_hist[coord["source"]] = source_hist.get(coord["source"], 0) + 1
        fiber_hist[str(coord["fiber"])] = fiber_hist.get(str(coord["fiber"]), 0) + 1
        repair_gain += int(coord.get("repair_gain", 0))
        if coord["source"] == "protected_exchange_repair":
            for idx, subset in enumerate(PAIR7_MASKS):
                repair_pair_b[idx] += (coord["mask"] & subset).bit_count()
    protected_keys = {row_key(row) for row in protected}
    selected_keys = {row_key(row) for row in selected}
    return {
        "selected": selected,
        "exchange_budget": exchange_budget,
        "exchange_move": move,
        "target_coordinate_count": len(selected),
        "target_row_count": sum(row["row_count"] for row in selected),
        "protected_coordinate_count": len(protected),
        "protected_row_count": sum(row["row_count"] for row in protected),
        "protected_rows_preserved": len(protected_keys - selected_keys) == 0,
        "exchange_removed_coordinate_count": len(removed),
        "exchange_removed_row_count": sum(row["row_count"] for row in removed),
        "new_repair_coordinate_count": len(repair_rows),
        "new_repair_row_count": sum(row["row_count"] for row in repair_rows),
        "refill_coordinate_count": len(refill_rows),
        "refill_row_count": sum(row["row_count"] for row in refill_rows),
        "repair_gain_score": repair_gain,
        "repair_pair7_B_proxy": repair_pair_b,
        "target_size_histogram": dict(sorted(size_hist.items(), key=lambda item: int(item[0]))),
        "target_source_histogram": dict(sorted(source_hist.items())),
        "target_fiber_histogram": dict(sorted(fiber_hist.items(), key=lambda item: int(item[0]))),
    }


def classify_sample(sample: dict[str, Any], base: dict[str, Any]) -> str:
    if not sample["protected_rows_preserved"]:
        return "PROTECTED_EXCHANGE_REGRESSES_PAIR7"
    if sample["min_pair7_B"] < base["stage1_min_pair_B"]:
        return "PROTECTED_EXCHANGE_REGRESSES_PAIR7"
    if sample["min_pair7_B"] < 2 * TARGET_AGREEMENT:
        return "PROTECTED_EXCHANGE_NOT_REPAIRED"
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "PROTECTED_EXCHANGE_CAPACITY_LOSS"
    if sample["six_class_dominance_added_by_repair"] > LOW_ADDED_COLLAPSE_THRESHOLD:
        return "PROTECTED_EXCHANGE_COLLAPSE_RETURNS"
    assignment = sample.get("assignment")
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "PROTECTED_EXCHANGE_PROXY_CANDIDATE"
    if assignment is not None:
        return "PROTECTED_EXCHANGE_LOW_RESCHEDULE"
    return "PROTECTED_EXCHANGE_UNSCHEDULED"


def sample_records(
    powers,
    rref,
    pivots,
    base: dict[str, Any],
    selection: dict[str, Any],
    seed: int,
) -> list[dict[str, Any]]:
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, SAMPLES_PER_SYSTEM)
    rows = []
    for sample_idx, vector in enumerate(vectors):
        values = joint.evaluate_vector(powers, vector)
        capacity = joint.value_class_capacity(values)
        pair_record = stage1.pair7_metrics(values, base["pair_masks"])
        hall_record = guided.value_hall_metrics(values, OLD_THREE_SUBSET_MASKS)
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
            "six_class_dominance_inside_stage1": base["stage1_six_class_dominance_total"],
            "six_class_dominance_added_by_repair": max(0, six_dom - base["stage1_six_class_dominance_total"]),
            "protected_rows_preserved": selection["protected_rows_preserved"],
            "value_class_hash": guided.hash_payload(hall.value_class_masks(values)),
        }
        sample["failure_mode"] = classify_sample(sample, base)
        sample["status"] = (
            "PROXY_A327_PROTECTED_EXCHANGE_ASSIGNMENT"
            if sample["failure_mode"] == "PROTECTED_EXCHANGE_PROXY_CANDIDATE"
            else "NO_PROTECTED_EXCHANGE_PROXY_A327"
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
        "six_class_dominance_inside_stage1": sample["six_class_dominance_inside_stage1"],
        "six_class_dominance_added_by_repair": sample["six_class_dominance_added_by_repair"],
        "protected_rows_preserved": sample["protected_rows_preserved"],
        "failure_mode": sample["failure_mode"],
        "status": sample["status"],
        "value_class_hash": sample["value_class_hash"],
    }


def sample_sort_key(sample: dict[str, Any]) -> tuple[Any, ...]:
    proxy_max = -1 if sample.get("assignment") is None else sample["assignment"]["exact_max_min"]
    return (
        sample["failure_mode"] == "PROTECTED_EXCHANGE_PROXY_CANDIDATE",
        sample["failure_mode"] == "PROTECTED_EXCHANGE_LOW_RESCHEDULE",
        sample["failure_mode"] == "PROTECTED_EXCHANGE_NOT_REPAIRED",
        proxy_max,
        sample["min_pair7_B"],
        sample["capacity_upper_bound"],
        -sample["six_class_dominance_added_by_repair"],
        -sample["six_class_dominance_total"],
    )


def evaluate_system(
    powers,
    base: dict[str, Any],
    values: list[list[int]],
    original_selected: list[dict[str, Any]],
    exchange_budget: int,
    move: str,
) -> dict[str, Any]:
    selection = select_exchange_rows(values, base, original_selected, exchange_budget, move)
    matrix = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(matrix, PROXY_PRIME)
    seed = int(
        guided.hash_payload([base["stage1_value_class_hash"], exchange_budget, move, SOURCE_COMMIT])[:12],
        16,
    )
    samples = sample_records(powers, rref, pivots, base, selection, seed)
    retained_samples = sorted(samples, key=sample_sort_key, reverse=True)[:4]
    failure_counts: dict[str, int] = {}
    for sample in samples:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    best = retained_samples[0]
    return {
        "target_system_id": f"{base['stage1_value_class_hash'][:12]}__PX{exchange_budget}__{move}",
        "stage1_target_system_id": base["stage1_target_system_id"],
        "stage1_value_class_hash": base["stage1_value_class_hash"],
        "exchange_budget": exchange_budget,
        "exchange_move": move,
        "proxy_field": f"GF({PROXY_PRIME})",
        "rank": len(pivots),
        "nullity": joint.VARIABLE_COUNT - len(pivots),
        "pivot_columns_hash": guided.hash_payload(pivots),
        "sample_count": len(samples),
        "best": compact_sample(best),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "proxy_candidate_count": sum(
            1 for sample in samples if sample["failure_mode"] == "PROTECTED_EXCHANGE_PROXY_CANDIDATE"
        ),
        "retained_sample_results": [compact_sample(sample) for sample in retained_samples],
        "target_rows_hash": guided.hash_payload([(row["position"], row["mask"]) for row in selection["selected"]]),
        **{key: value for key, value in selection.items() if key != "selected"},
    }


def build_record() -> dict[str, Any]:
    stage1_data = load_json(STAGE1_DATA)
    stage2_data = load_json(STAGE2_DATA)
    bases = retained_stage1_bases()
    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    systems = []
    base_summaries = []
    for row in bases:
        base, values, selected = reconstruct_stage1_state(row)
        base_summaries.append(base)
        for exchange_budget in EXCHANGE_BUDGETS:
            for move in EXCHANGE_MOVES:
                systems.append(evaluate_system(powers, base, values, selected, exchange_budget, move))
    retained = sorted(
        systems,
        key=lambda row: (
            row["proxy_candidate_count"],
            row["best"]["failure_mode"] == "PROTECTED_EXCHANGE_LOW_RESCHEDULE",
            row["best"]["failure_mode"] == "PROTECTED_EXCHANGE_NOT_REPAIRED",
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
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_PROTECTED_EXCHANGE_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "witness7_pair_protected_local_exchange",
        "stage1_baseline": {
            "proxy_max_min": stage1_data["witness7_pair_repair"]["best_proxy_max_min"],
            "capacity": stage1_data["witness7_pair_repair"]["best_capacity"],
            "pair_B_values": stage1_data["witness7_pair_repair"]["best_pair_B_values"],
            "pair_deficit_to_654": [
                2 * TARGET_AGREEMENT - value for value in stage1_data["witness7_pair_repair"]["best_pair_B_values"]
            ],
            "added_six_class_dominance": stage1_data["witness7_pair_repair"]["best_added_six_class_dominance"],
        },
        "stage2_rebuild_regression": {
            "proxy_max_min": stage2_data["stage2_search"]["best_proxy_max_min"],
            "pair_B_values": stage2_data["stage2_search"]["best_pair_B_values"],
            "pair_deficit_to_654": stage2_data["stage2_search"]["best_pair_deficit"],
        },
        "protected_exchange": {
            "base_systems": len(bases),
            "base_summaries": base_summaries,
            "protected_rows": base_summaries[0]["protected_row_count"] if base_summaries else 0,
            "exchangeable_rows": base_summaries[0]["exchangeable_row_count"] if base_summaries else 0,
            "systems_tested": len(systems),
            "exchange_budgets": EXCHANGE_BUDGETS,
            "exchange_moves": EXCHANGE_MOVES,
            "samples_tested": sum(row["sample_count"] for row in systems),
            "proxy_candidates": len(proxy_candidates),
            "best_proxy_max_min": best["best"]["proxy_max_min"],
            "best_capacity": best["best"]["capacity_upper_bound"],
            "best_pair_B_values": best["best"]["pair7_B_values"],
            "best_pair_deficit": best["best"]["pair7_deficits_to_654"],
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
