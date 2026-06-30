#!/usr/bin/env python3
"""Hall-style rescheduler obstruction audit for M1 a=327 proxy tuples."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_collapse_quotient_line_search as line
import scan_m1_a327_collision_tangent_quotient_plane_search as tangent
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_rescheduler_aware_quotient_plane_search as plane


LINE_DATA = Path("experimental/data/m1_a327_collapse_quotient_line_search.json")
PLANE_DATA = Path("experimental/data/m1_a327_rescheduler_aware_quotient_plane_search.json")
TANGENT_DATA = Path("experimental/data/m1_a327_collision_tangent_quotient_plane_search.json")
SOFT_DATA = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_rescheduler_dual_hall_obstruction.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PRIMARY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "758af1b"
LIST_MASKS = list(range(1, 1 << joint.LIST_SIZE))
LINE_SAMPLE_LIMIT = 16
GENERIC_PLANE_PER_LINE = 3
TANGENT_PLANE_PER_SPACE = 2


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


def soft_rows_by_id() -> dict[str, dict[str, Any]]:
    source = load_json(SOFT_DATA)
    return {row["target_system_id"]: row for row in source["retained_results"]}


def line_rows_by_hash(line_source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = {}
    for system in line_source["systems"]:
        for sample in system["retained_lines"]:
            rows[sample["line_hash"]] = {"system_id": system["system_id"], **sample}
    return rows


def value_class_masks(values: list[list[int]]) -> list[list[int]]:
    classes_by_pos = []
    for pos in range(joint.N):
        buckets: dict[int, int] = {}
        for witness in range(joint.LIST_SIZE):
            value = int(values[witness][pos])
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        classes_by_pos.append(sorted(set(buckets.values())))
    return classes_by_pos


def hall_audit(values: list[list[int]]) -> dict[str, Any]:
    classes_by_pos = value_class_masks(values)
    subset_rows = []
    for subset in LIST_MASKS:
        bound_total = 0
        for classes in classes_by_pos:
            bound_total += max((mask & subset).bit_count() for mask in classes)
        subset_size = subset.bit_count()
        subset_rows.append(
            {
                "subset_mask": subset,
                "subset": [idx + 1 for idx in range(joint.LIST_SIZE) if subset & (1 << idx)],
                "subset_size": subset_size,
                "B_U": bound_total,
                "hall_bound": bound_total // subset_size,
                "deficit_to_327": subset_size * TARGET_AGREEMENT - bound_total,
            }
        )
    hall_bound = min(row["hall_bound"] for row in subset_rows)
    tight = [row for row in subset_rows if row["hall_bound"] == hall_bound]
    tight.sort(key=lambda row: (row["deficit_to_327"], row["subset_size"], -row["subset_mask"]), reverse=True)
    return {
        "hall_bound": hall_bound,
        "tight_subsets": tight[:8],
        "worst_deficit_to_327": max(row["deficit_to_327"] for row in subset_rows),
        "subset_count": len(subset_rows),
    }


def critical_coordinate_summary(values: list[list[int]], subset_mask: int) -> dict[str, Any]:
    classes_by_pos = value_class_masks(values)
    pattern_histogram: dict[str, int] = {}
    fiber_histogram: dict[str, int] = {}
    critical_count = 0
    subset_size = subset_mask.bit_count()
    for pos, classes in enumerate(classes_by_pos):
        best = max((mask & subset_mask).bit_count() for mask in classes)
        if best >= subset_size:
            continue
        best_masks = [mask for mask in classes if (mask & subset_mask).bit_count() == best]
        pattern = ",".join(str(mask) for mask in sorted(best_masks))
        pattern_histogram[pattern] = pattern_histogram.get(pattern, 0) + 1
        fiber = str(pos % 16)
        fiber_histogram[fiber] = fiber_histogram.get(fiber, 0) + 1
        critical_count += 1
    return {
        "subset_mask": subset_mask,
        "count": critical_count,
        "pattern_histogram": dict(sorted(pattern_histogram.items(), key=lambda item: (-item[1], item[0]))[:16]),
        "quotient_fiber_histogram": dict(sorted(fiber_histogram.items(), key=lambda item: int(item[0]))),
    }


def core_cache_for(soft_rows: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {}


def get_core(cache: dict[str, dict[str, Any]], soft_rows: dict[str, dict[str, Any]], system_id: str) -> dict[str, Any]:
    if system_id not in cache:
        cache[system_id] = line.core_for_system(soft_rows[system_id], PRIMARY_PRIME)
    return cache[system_id]


def reconstruct_line_values(
    core_cache: dict[str, dict[str, Any]],
    soft_rows: dict[str, dict[str, Any]],
    line_row: dict[str, Any],
) -> tuple[dict[str, Any], list[list[int]]]:
    core = get_core(core_cache, soft_rows, line_row["system_id"])
    anchors = {anchor["anchor_id"]: anchor for anchor in line.anchor_candidates(core, PRIMARY_PRIME)}
    anchor = anchors[line_row["anchor_id"]]
    q1 = core["null_basis"][int(line_row["quotient_basis_index"])] % PRIMARY_PRIME
    q1_values = line.vector_values(core["powers"], q1, PRIMARY_PRIME)
    values = line.combine_values(anchor["_values"], q1_values, int(line_row["lambda"]), PRIMARY_PRIME)
    return core, values


def reconstruct_generic_plane_values(
    core_cache: dict[str, dict[str, Any]],
    soft_rows: dict[str, dict[str, Any]],
    line_row: dict[str, Any],
    plane_row: dict[str, Any],
) -> list[list[int]]:
    core, base_values = reconstruct_line_values(core_cache, soft_rows, line_row)
    q2 = core["null_basis"][int(plane_row["second_basis_index"])] % PRIMARY_PRIME
    q2_values = line.vector_values(core["powers"], q2, PRIMARY_PRIME)
    return plane.add_values(base_values, q2_values, int(plane_row["mu"]), PRIMARY_PRIME)


def reconstruct_tangent_plane_values(
    core_cache: dict[str, dict[str, Any]],
    soft_rows: dict[str, dict[str, Any]],
    line_row: dict[str, Any],
    space_row: dict[str, Any],
    plane_row: dict[str, Any],
) -> list[list[int]]:
    core, base_values = reconstruct_line_values(core_cache, soft_rows, line_row)
    protected = tangent.protected_classes(base_values, int(space_row["budget"]))
    tangent_space = tangent.tangent_space_for(core, protected)
    coeff = tangent_space["coefficient_basis"][int(plane_row["tangent_basis_index"])]
    q2 = (coeff @ core["null_basis"]) % PRIMARY_PRIME
    q2_values = line.vector_values(core["powers"], q2, PRIMARY_PRIME)
    return tangent.add_values(base_values, q2_values, int(plane_row["mu"]), PRIMARY_PRIME)


def classify_sample(hall: dict[str, Any], assignment: dict[str, Any] | None, capacity: int) -> str:
    if capacity < TARGET_AGREEMENT:
        return "LOW_CAPACITY_SCREEN"
    if assignment is None:
        return "UNKNOWN"
    max_min = assignment["exact_max_min"]
    if hall["hall_bound"] == max_min:
        return "HALL_TIGHT"
    if hall["hall_bound"] < TARGET_AGREEMENT:
        return "HALL_GAP"
    return "BALANCE_GAP"


def analyze_values(sample: dict[str, Any], values: list[list[int]], force_assignment: bool = False) -> dict[str, Any]:
    capacity = joint.value_class_capacity(values)
    hall = hall_audit(values)
    assignment = None
    if force_assignment or capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = joint.exact_assignment_max_min(values)
    tight_subset = hall["tight_subsets"][0]["subset_mask"]
    critical = critical_coordinate_summary(values, tight_subset)
    failure_mode = classify_sample(hall, assignment, capacity["capacity_upper_bound"])
    return {
        **sample,
        "capacity_upper_bound": capacity["capacity_upper_bound"],
        "capacity_total": capacity["capacity_total"],
        "largest_class_histogram": capacity["largest_class_histogram"],
        "rescheduler_max_min": None if assignment is None else assignment["exact_max_min"],
        "agreement_vector": None if assignment is None else assignment["agreement_vector"],
        "hall_bound": hall["hall_bound"],
        "hall_bound_matches_rescheduler": None if assignment is None else hall["hall_bound"] == assignment["exact_max_min"],
        "tight_subsets": hall["tight_subsets"],
        "deficit_to_327": hall["worst_deficit_to_327"],
        "critical_coordinates": critical,
        "failure_mode": failure_mode,
        "value_class_hash": hash_payload(value_class_masks(values)),
    }


def collect_line_samples(line_source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for system in line_source["systems"]:
        for sample in system["retained_lines"]:
            rows.append({"source": "collapse_quotient_line", "system_id": system["system_id"], **sample})
    rows.sort(
        key=lambda row: (
            -1 if row["proxy_max_min"] is None else row["proxy_max_min"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["line_hash"],
        ),
        reverse=True,
    )
    return rows[:LINE_SAMPLE_LIMIT]


def collect_generic_plane_samples(plane_source: dict[str, Any], line_by_hash: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for line_row in plane_source["lines"]:
        for sample in line_row["retained_planes"][:GENERIC_PLANE_PER_LINE]:
            parent = line_by_hash[sample["line_hash"]]
            rows.append(
                {
                    "source": "rescheduler_aware_quotient_plane",
                    "system_id": line_row["system_id"],
                    "parent_line_hash": sample["line_hash"],
                    "parent_line_proxy_max_min": line_row["line_proxy_max_min"],
                    "line_row": parent,
                    "sample": sample,
                }
            )
    return rows


def collect_tangent_samples(tangent_source: dict[str, Any], line_by_hash: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for line_row in tangent_source["lines"]:
        for space in line_row["tangent_spaces"]:
            for sample in space["retained_planes"][:TANGENT_PLANE_PER_SPACE]:
                parent = line_by_hash[sample["line_hash"]]
                rows.append(
                    {
                        "source": "collision_tangent_quotient_plane",
                        "system_id": line_row["system_id"],
                        "parent_line_hash": sample["line_hash"],
                        "parent_line_proxy_max_min": line_row["line_proxy_max_min"],
                        "protection_budget": space["budget"],
                        "tangent_dimension": space["tangent_dimension"],
                        "line_row": parent,
                        "space": space,
                        "sample": sample,
                    }
                )
    return rows


def compact_source_sample(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row.get(key)
        for key in [
            "source",
            "system_id",
            "line_hash",
            "parent_line_hash",
            "plane_hash",
            "protection_budget",
            "tangent_dimension",
            "lambda",
            "mu",
            "six_class_dominance",
            "parent_line_proxy_max_min",
        ]
        if key in row and row.get(key) is not None
    }


def build_record() -> dict[str, Any]:
    line_source = load_json(LINE_DATA)
    plane_source = load_json(PLANE_DATA)
    tangent_source = load_json(TANGENT_DATA)
    soft_rows = soft_rows_by_id()
    cache = core_cache_for(soft_rows)
    line_by_hash = line_rows_by_hash(line_source)

    raw_analyzed = []
    for line_sample in collect_line_samples(line_source):
        _core, values = reconstruct_line_values(cache, soft_rows, line_sample)
        raw_analyzed.append(analyze_values(compact_source_sample(line_sample), values))

    for row in collect_generic_plane_samples(plane_source, line_by_hash):
        values = reconstruct_generic_plane_values(cache, soft_rows, row["line_row"], row["sample"])
        sample = {
            **compact_source_sample(row),
            "plane_hash": row["sample"]["plane_hash"],
            "mu": row["sample"]["mu"],
            "six_class_dominance": row["sample"]["six_class_dominance"],
        }
        raw_analyzed.append(analyze_values(sample, values))

    for row in collect_tangent_samples(tangent_source, line_by_hash):
        values = reconstruct_tangent_plane_values(cache, soft_rows, row["line_row"], row["space"], row["sample"])
        sample = {
            **compact_source_sample(row),
            "plane_hash": row["sample"]["plane_hash"],
            "mu": row["sample"]["mu"],
            "six_class_dominance": row["sample"]["six_class_dominance"],
        }
        raw_analyzed.append(analyze_values(sample, values))

    deduped: dict[str, dict[str, Any]] = {}
    for row in raw_analyzed:
        digest = row["value_class_hash"]
        old = deduped.get(digest)
        if old is None:
            deduped[digest] = row
            continue
        old_key = (
            -1 if old["rescheduler_max_min"] is None else old["rescheduler_max_min"],
            old["hall_bound"],
            old["capacity_upper_bound"],
        )
        new_key = (
            -1 if row["rescheduler_max_min"] is None else row["rescheduler_max_min"],
            row["hall_bound"],
            row["capacity_upper_bound"],
        )
        if new_key > old_key:
            deduped[digest] = row
    analyzed = list(deduped.values())
    analyzed.sort(
        key=lambda row: (
            -1 if row["rescheduler_max_min"] is None else row["rescheduler_max_min"],
            row["hall_bound"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"] if row.get("six_class_dominance") is not None else 0,
            row["source"],
        ),
        reverse=True,
    )
    best = analyzed[0]
    failure_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    hall_tight_count = 0
    for row in analyzed:
        failure_counts[row["failure_mode"]] = failure_counts.get(row["failure_mode"], 0) + 1
        source_counts[row["source"]] = source_counts.get(row["source"], 0) + 1
        if row["hall_bound_matches_rescheduler"]:
            hall_tight_count += 1
    proof_status = "RESCHEDULER_OBSTRUCTION_CERTIFICATE" if hall_tight_count else "AUDIT"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "rescheduler_dual_hall_obstruction",
        "samples_analyzed": len(analyzed),
        "raw_samples_replayed": len(raw_analyzed),
        "duplicate_value_class_samples": len(raw_analyzed) - len(analyzed),
        "source_counts": dict(sorted(source_counts.items())),
        "best_sample": best,
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "hall_tight_count": hall_tight_count,
        "samples": analyzed,
        "result_hash": hash_payload(analyzed),
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
