#!/usr/bin/env python3
"""Initial ledger for upstream B47-robust repaired-skeleton search."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any


LOCAL_BASIN_PATH = Path("experimental/data/m1_a327_local_basin_conservation_note.json")
V2_GRID_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")
CODESIGN_PATH = Path("experimental/data/m1_a327_reserve_pairclass_codesign_before_split.json")
MICROREPAIR_STAGE2_PATH = Path("experimental/data/m1_a327_postsplit_pair27_37_microrepair_stage2.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_upstream_b47_robust_skeleton_search.json")

TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SOURCE_COMMIT = "f2c7823"
FRAGILE_CLASS = [1, 4, 5, 7]


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


def contains_fragile_class(collapse: list[list[int]] | None) -> bool:
    return any(sorted(block) == FRAGILE_CLASS for block in collapse or [])


def margins(capacity: int | None, pair_values: list[int] | None) -> dict[str, int | None]:
    if capacity is None or pair_values is None:
        return {"capacity": None, "B27": None, "B37": None, "B47": None, "B57": None}
    return {
        "capacity": capacity - TARGET_AGREEMENT,
        "B27": pair_values[1] - PAIR_TARGET,
        "B37": pair_values[2] - PAIR_TARGET,
        "B47": pair_values[3] - PAIR_TARGET,
        "B57": pair_values[4] - PAIR_TARGET,
    }


def robustness_score(capacity: int | None, pair_values: list[int] | None) -> int | None:
    values = margins(capacity, pair_values)
    if any(value is None for value in values.values()):
        return None
    return min(int(value) for value in values.values() if value is not None)


def skeleton_record(
    *,
    name: str,
    source: str,
    capacity: int | None,
    pair_values: list[int] | None,
    collapse: list[list[int]] | None,
    failure_mode: str | None,
) -> dict[str, Any]:
    return {
        "name": name,
        "source": source,
        "capacity": capacity,
        "pair_B_values": pair_values,
        "guard_margins": margins(capacity, pair_values),
        "robustness_score_before_split": robustness_score(capacity, pair_values),
        "collapse_pattern": collapse,
        "contains_fragile_1457_class": contains_fragile_class(collapse),
        "failure_mode": failure_mode,
    }


def candidate_skeletons(local: dict[str, Any], codesign: dict[str, Any], micro: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    base = local["baseline_repaired_skeleton"]
    candidates.append(
        skeleton_record(
            name="route_cut_budget32_repaired_skeleton",
            source="m1_a327_local_basin_conservation_note",
            capacity=base["capacity"],
            pair_values=base["pair_B_values"],
            collapse=base["collapse_pattern"],
            failure_mode="ROUTE_CUT_LOCAL_BASIN",
        )
    )

    codesign_search = codesign["codesign_search"]
    if codesign_search.get("best_post_split_capacity") is not None:
        candidates.append(
            skeleton_record(
                name="reserve_pairclass_codesign_best_postsplit",
                source="m1_a327_reserve_pairclass_codesign_before_split",
                capacity=codesign_search["best_post_split_capacity"],
                pair_values=codesign_search["best_post_split_pair_B_values"],
                collapse=codesign_search.get("best_collapse_pattern"),
                failure_mode=codesign_search.get("best_failure_mode"),
            )
        )

    for index, result in enumerate(micro["stage2_microrepair"].get("results", [])):
        if result.get("capacity_upper_bound") is None or result.get("pair_B_values") is None:
            continue
        candidates.append(
            skeleton_record(
                name=f"microrepair_stage2_result_{index:02d}",
                source="m1_a327_postsplit_pair27_37_microrepair_stage2",
                capacity=result["capacity_upper_bound"],
                pair_values=result["pair_B_values"],
                collapse=result.get("degenerate_classes"),
                failure_mode=result.get("failure_mode"),
            )
        )

    return candidates


def split_probe_records(v2: dict[str, Any]) -> list[dict[str, Any]]:
    probes: list[dict[str, Any]] = []
    for result in v2["compensated_grid"].get("results", []):
        best = result.get("best")
        if not best:
            continue
        capacity = best.get("capacity_upper_bound")
        pair_values = best.get("pair_B_values")
        collapse = best.get("degenerate_classes")
        score = robustness_score(capacity, pair_values)
        probes.append(
            {
                "case_index": result["case_index"],
                "split_family": result["split_family"],
                "replacement_bundle_size": result["replacement_bundle_size"],
                "selector": result["selector"],
                "capacity": capacity,
                "pair_B_values": pair_values,
                "guard_margins": margins(capacity, pair_values),
                "robustness_score_after_split": score,
                "collapse_pattern": collapse,
                "contains_fragile_1457_class": contains_fragile_class(collapse),
                "guard_preserving": bool(score is not None and score >= 0),
                "failure_mode": result["failure_mode"],
            }
        )
    return probes


def best_by_score(items: list[dict[str, Any]], score_key: str) -> dict[str, Any] | None:
    scored = [item for item in items if item.get(score_key) is not None]
    if not scored:
        return None
    return max(scored, key=lambda item: (item[score_key], item.get("capacity") or -10**9))


def build_record() -> dict[str, Any]:
    local = load_json(LOCAL_BASIN_PATH)
    v2 = load_json(V2_GRID_PATH)
    codesign = load_json(CODESIGN_PATH)
    micro = load_json(MICROREPAIR_STAGE2_PATH)

    candidates = candidate_skeletons(local, codesign, micro)
    probes = split_probe_records(v2)
    best_pre = best_by_score(candidates, "robustness_score_before_split")
    best_probe = best_by_score(probes, "robustness_score_after_split")

    split_resilient = [probe for probe in probes if probe["guard_preserving"]]
    fragile_candidates = [candidate for candidate in candidates if candidate["contains_fragile_1457_class"]]

    upstream_search = {
        "systems_tested": 0,
        "source_skeletons_analyzed": len(candidates),
        "exact_vectors_constructed": 0,
        "split_probe_vectors": len(probes),
        "split_resilient_skeletons": len(split_resilient),
        "fragile_1457_candidate_skeletons": len(fragile_candidates),
        "candidate_split_families": [
            "split_4_from_157",
            "split_14_vs_57",
            "split_1_from_457",
            "split_15_vs_47",
            "split_17_vs_45",
        ],
        "candidate_row_families": [
            "quotient_fiber_buffer",
            "B47_robust_buffer",
            "split_resilient_pairclass",
            "balanced_residual_collapse",
            "triple_237_with_B47_guard",
            "alternate_collapse_selector",
        ],
        "best_pre_split_capacity": None if best_pre is None else best_pre["capacity"],
        "best_pre_split_pair_B_values": None if best_pre is None else best_pre["pair_B_values"],
        "best_pre_split_collapse_pattern": None if best_pre is None else best_pre["collapse_pattern"],
        "best_pre_split_robustness_score": None if best_pre is None else best_pre["robustness_score_before_split"],
        "best_probe_split_capacity": None if best_probe is None else best_probe["capacity"],
        "best_probe_split_pair_B_values": None if best_probe is None else best_probe["pair_B_values"],
        "best_probe_split_collapse_pattern": None if best_probe is None else best_probe["collapse_pattern"],
        "best_probe_robustness_score": None if best_probe is None else best_probe["robustness_score_after_split"],
        "best_failure_mode": "UPSTREAM_B47_NOT_ROBUST" if not split_resilient else "UPSTREAM_SPLIT_RESILIENT_SKELETON",
        "candidate_skeletons": candidates,
        "split_probe_results": probes,
    }

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "local_basin_conservation": {
            "systems_tested": local["full_v2_grid"]["systems_tested"],
            "exact_vectors_constructed": local["full_v2_grid"]["exact_vectors_constructed"],
            "capacity_preserving_vectors": local["full_v2_grid"]["capacity_preserving_vectors"],
            "pair_guard_preserving_vectors": local["full_v2_grid"]["pair_guard_preserving_vectors"],
            "best_capacity": local["full_v2_grid"]["best_capacity"],
            "best_pair_B_values": local["full_v2_grid"]["best_pair_B_values"],
            "status": "ROUTE_CUT_LOCAL_BASIN",
        },
        "upstream_b47_search": upstream_search,
        "proof_status": "PARTIAL",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "global obstruction outside the tested basin",
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
