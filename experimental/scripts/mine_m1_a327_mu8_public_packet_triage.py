#!/usr/bin/env python3
"""Mine the current M1 a=327 mu8 work into a compact public-packet triage.

This is deliberately not a search script.  It reads already-produced ledgers and
classifies whether the local state is board-ready, PR-ready as a route cut, or
still research-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(".")
OUT_PATH = Path("experimental/data/m1_a327_mu8_public_packet_triage.json")

RANK_ONE_PATH = Path("experimental/data/m1_a327_mu8_rank_one_carrier_obstruction.json")

RANK2_ADAPTIVE_PATH = Path("experimental/data/m1_a327_mu8_rank2_adaptive_ratio_columns.json")
RANK2_FEEDBACK_PATH = Path("experimental/data/m1_a327_mu8_rank2_feedback_adaptive_ratio_columns.json")
RANK2_FEEDBACK2_PATH = Path("experimental/data/m1_a327_mu8_rank2_feedback2_adaptive_ratio_columns.json")
RANK2_FRONTIER_PATH = Path("experimental/data/m1_a327_mu8_rank2_frontier_mining.json")
RANK2_CEILING_PATH = Path("experimental/data/m1_a327_mu8_rank2_current_menu_ceiling.json")
RANK2_FEEDBACK_EXACT_PATH = Path("experimental/data/m1_a327_mu8_rank2_feedback_exact_interpolation.json")
RANK2_WIDTH16_EXACT_PATH = Path("experimental/data/m1_a327_mu8_rank2_width16_near_front_exact.json")

RANK3_SINGLETON_FILES = {
    22: Path("experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_singleton22.json"),
    21: Path("experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_singleton21.json"),
    20: Path("experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_singleton20.json"),
    18: Path("experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_singleton18.json"),
    12: Path("experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_singleton12.json"),
    5: Path("experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_repfixed6_singleton5.json"),
}
RANK3_SINGLETON22_EXACT_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_singleton22_exact_interpolation.json"
)
RANK3_SINGLETON22_PRESSURE_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multiphase_corecap34_targetrepair_nondep84_singleton22_row_dependency_pressure.json"
)
RANK3_NON_SINGLETON_SYNTH_SUMMARY_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_non_singleton_synthesized_dependency_summary.json"
)
RANK3_SINGLETON_BLOCKED_SUPPORT_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_singleton_blocked_support_first_schedule.json"
)
RANK3_SINGLETON_BLOCKED_EXACT_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_singleton_blocked_support_first_exact_interpolation.json"
)
RANK3_SINGLETON_BLOCKED_PRESSURE_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_singleton_blocked_support_first_row_dependency_pressure.json"
)
RANK3_SINGLETON_BLOCKED_REPEAT_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_singleton_blocked_repeat_pressure_schedule.json"
)
RANK3_CORE_DEPENDENCY_SUMMARY_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_core_dependency_synthesis_summary.json"
)
RANK3_GENERIC_CORE_NOGOODS_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_generic_core_nogoods.json"
)
RANK3_CORE_NOGOOD_LOWROW_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_core_nogood_lowrow_schedule.json"
)
RANK3_CORE_NOGOOD_EXACT_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_core_nogood_exact_interpolation.json"
)
RANK3_CORE_NOGOOD_WITNESS_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_core_nogood_witness_audit.json"
)
RANK3_CORE_NOGOOD_PRESSURE_PATH = Path(
    "experimental/data/m1_a327_mu8_rank3_core_nogood_row_dependency_pressure.json"
)

REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
]


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open() as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_tracked_files() -> set[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return set()
    return set(result.stdout.splitlines())


def base_record(source_commit: str = "local-uncommitted") -> dict[str, Any]:
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": 327,
        "source_commit": source_commit,
        "mca_counted": False,
        "not_claimed": REQUIRED_NONCLAIMS,
    }


def header_ok(record: dict[str, Any] | None) -> bool:
    if not record:
        return False
    return (
        record.get("track") == "INTERLEAVED_LIST"
        and record.get("row") == "RS[F_17^32,H,256]"
        and record.get("denominator") == "17^32"
        and record.get("agreement_target") == 327
        and record.get("mca_counted") is False
        and set(REQUIRED_NONCLAIMS).issubset(set(record.get("not_claimed", [])))
    )


def compact_rank2_adaptive(path: Path) -> dict[str, Any]:
    record = load_json(path)
    if not record:
        return {"path": str(path), "present": False}
    meta = record.get("adaptive_ratio_columns", {})
    return {
        "path": str(path),
        "present": True,
        "header_ok": header_ok(record),
        "best_failure_mode": meta.get("best_failure_mode"),
        "best_min_support": meta.get("best_min_support"),
        "best_total_incidence": meta.get("best_total_incidence"),
        "selected_incidence_gap": None
        if meta.get("best_total_incidence") is None
        else 7 * 327 - meta.get("best_total_incidence"),
        "support_gap": None
        if meta.get("best_min_support") is None
        else 327 - meta.get("best_min_support"),
        "support_pair_candidates": meta.get("support_pair_candidates"),
        "near_front_candidates": meta.get("near_front_candidates"),
        "planes_solved": meta.get("planes_solved"),
        "max_width": meta.get("max_width"),
        "rounds_requested": meta.get("rounds_requested"),
    }


def compact_exact(path: Path, key: str = "exact_interpolation") -> dict[str, Any]:
    record = load_json(path)
    if not record:
        return {"path": str(path), "present": False}
    meta = record.get(key, {})
    return {
        "path": str(path),
        "present": True,
        "header_ok": header_ok(record),
        "best_failure_mode": meta.get("best_failure_mode"),
        "systems_tested": meta.get("systems_tested"),
        "best_nullity": meta.get("best_nullity"),
        "positive_nullity_systems": meta.get("positive_nullity_systems"),
        "pair_visible_systems": meta.get("pair_visible_systems"),
    }


def iter_json_files(pattern: str) -> list[Path]:
    return sorted(Path("experimental/data").glob(pattern))


def recursive_status_contains(obj: Any, needle: str) -> bool:
    if isinstance(obj, dict):
        return any(recursive_status_contains(value, needle) for value in obj.values())
    if isinstance(obj, list):
        return any(recursive_status_contains(value, needle) for value in obj)
    return obj == needle


def compact_rank2_sweep() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for path in iter_json_files("m1_a327_mu8_rank2_*adaptive_ratio_columns.json"):
        compact = compact_rank2_adaptive(path)
        if compact.get("present"):
            rows.append(compact)

    def support_key(row: dict[str, Any]) -> tuple[int, int]:
        return (
            int(row.get("best_min_support") or -1),
            int(row.get("best_total_incidence") or -1),
        )

    best = max(rows, key=support_key) if rows else None
    support_pair_passes = [
        row for row in rows if int(row.get("support_pair_candidates") or 0) > 0
    ]
    near_front = [
        row for row in rows if int(row.get("near_front_candidates") or 0) > 0
    ]
    top_fronts = sorted(rows, key=support_key, reverse=True)[:8]
    return {
        "adaptive_ledgers_scanned": len(rows),
        "support_pair_passing_ledgers": len(support_pair_passes),
        "near_front_ledgers": len(near_front),
        "best": best,
        "top_fronts": top_fronts,
    }


def compact_exact_sweep(prefix: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    paths = iter_json_files(f"{prefix}*exact_interpolation.json") + iter_json_files(
        f"{prefix}*near_front_exact.json"
    )
    for path in sorted(set(paths)):
        record = load_json(path)
        if not record:
            continue
        key = "exact_interpolation"
        if key not in record:
            key = "near_front_exact"
        if key not in record:
            # Rank-3 scripts still store the same summary under exact_interpolation
            # in all current ledgers, but keep this fallback for older variants.
            key = "projective_exact_interpolation"
        meta = record.get(key, {})
        rows.append(
            {
                "path": str(path),
                "header_ok": header_ok(record),
                "best_failure_mode": meta.get("best_failure_mode"),
                "systems_tested": meta.get("systems_tested", 0),
                "best_nullity": meta.get("best_nullity", 0),
                "positive_nullity_systems": meta.get("positive_nullity_systems", 0),
                "pair_visible_systems": meta.get("pair_visible_systems", 0),
            }
        )
    total_systems = sum(int(row.get("systems_tested") or 0) for row in rows)
    positive = sum(int(row.get("positive_nullity_systems") or 0) for row in rows)
    pair_visible = sum(int(row.get("pair_visible_systems") or 0) for row in rows)
    max_nullity = max([int(row.get("best_nullity") or 0) for row in rows], default=0)
    return {
        "exact_ledgers_scanned": len(rows),
        "systems_tested_total": total_systems,
        "positive_nullity_systems_total": positive,
        "pair_visible_systems_total": pair_visible,
        "max_best_nullity": max_nullity,
        "all_tested_systems_full_rank": total_systems > 0 and positive == 0 and max_nullity == 0,
        "top_by_systems_tested": sorted(
            rows, key=lambda row: int(row.get("systems_tested") or 0), reverse=True
        )[:12],
    }


def compact_rank3_pressure_sweep() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for path in iter_json_files("m1_a327_mu8_rank3_*row_dependency_pressure.json"):
        record = load_json(path)
        if not record:
            continue
        meta = record.get("row_dependency_pressure", {})
        rows.append(
            {
                "path": str(path),
                "header_ok": header_ok(record),
                "best_failure_mode": meta.get("best_failure_mode"),
                "systems_tested": meta.get("systems_tested", 0),
                "best_nullity": meta.get("best_nullity", 0),
                "positive_nullity_systems": meta.get("positive_nullity_systems", 0),
            }
        )
    total_systems = sum(int(row.get("systems_tested") or 0) for row in rows)
    positive = sum(int(row.get("positive_nullity_systems") or 0) for row in rows)
    return {
        "pressure_ledgers_scanned": len(rows),
        "systems_tested_total": total_systems,
        "positive_nullity_systems_total": positive,
        "all_tested_cores_full_rank": total_systems > 0 and positive == 0,
        "top_by_systems_tested": sorted(
            rows, key=lambda row: int(row.get("systems_tested") or 0), reverse=True
        )[:12],
    }


def compact_witness_sweep() -> dict[str, Any]:
    files = sorted(Path("experimental/data").glob("m1_a327_mu8_*witness_audit.json"))
    passes = []
    for path in files:
        record = load_json(path)
        if record and recursive_status_contains(record, "EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS"):
            passes.append(str(path))
    return {
        "witness_ledgers_scanned": len(files),
        "exact_a327_witness_passes": len(passes),
        "pass_paths": passes,
    }


def compact_rank2_frontier() -> dict[str, Any]:
    frontier = load_json(RANK2_FRONTIER_PATH)
    ceiling = load_json(RANK2_CEILING_PATH)
    out: dict[str, Any] = {
        "frontier_path": str(RANK2_FRONTIER_PATH),
        "ceiling_path": str(RANK2_CEILING_PATH),
        "frontier_present": frontier is not None,
        "ceiling_present": ceiling is not None,
    }
    if frontier:
        frontier_meta = (
            frontier.get("frontier_mining")
            or frontier.get("ratio_repeat_frontier_mining")
            or frontier.get("current_menu_ceiling")
            or frontier
        )
        out["frontier"] = {
            "candidate_id": frontier_meta.get("candidate_id"),
            "plane_id": frontier_meta.get("plane_id"),
            "support_vector": frontier_meta.get("support_vector"),
            "label_deficits": frontier_meta.get("label_deficits"),
            "selected_incidence_total": frontier_meta.get("selected_incidence_total"),
            "selected_incidence_gap": frontier_meta.get("selected_incidence_gap"),
            "pair_count_max": frontier_meta.get("pair_count_max"),
            "row_cost": frontier_meta.get("row_cost"),
            "selected_block_size_histogram": frontier_meta.get("selected_block_size_histogram"),
            "ratio_line_support_histogram": frontier_meta.get("ratio_line_support_histogram"),
            "max_ratio_line_support": frontier_meta.get("max_ratio_line_support"),
            "best_single_repair_min_support": frontier_meta.get("best_single_repair_min_support"),
            "best_single_repair_total_incidence": frontier_meta.get("best_single_repair_total_incidence"),
            "best_single_repair_pair_cap_pass": frontier_meta.get("best_single_repair_pair_cap_pass"),
        }
    if ceiling:
        meta = ceiling.get("current_menu_ceiling", ceiling)
        out["current_menu_ceiling"] = {
            "best_failure_mode": meta.get("best_failure_mode"),
            "best_min_support": meta.get("best_min_support"),
            "best_total_incidence": meta.get("best_total_incidence"),
            "selected_incidence_gap": None
            if meta.get("best_total_incidence") is None
            else 7 * 327 - meta.get("best_total_incidence"),
            "support_gap": None
            if meta.get("best_min_support") is None
            else 327 - meta.get("best_min_support"),
            "support_pair_candidates": meta.get("support_pair_candidates"),
            "max_selected_ratio_line_support": meta.get("max_selected_ratio_line_support"),
            "menu_ratio_limit": meta.get("menu_ratio_limit"),
            "planes_tested": meta.get("planes_tested"),
        }
    return out


def compact_rank3_singleton(cap: int, path: Path) -> dict[str, Any]:
    record = load_json(path)
    if not record:
        return {"cap": cap, "path": str(path), "present": False}
    meta = record.get("balanced_key_bundle_search", {})
    candidates = record.get("candidates", [])
    best = candidates[0] if candidates else {}
    return {
        "cap": cap,
        "path": str(path),
        "present": True,
        "header_ok": header_ok(record),
        "best_failure_mode": meta.get("best_failure_mode"),
        "support_pair_candidates": meta.get("support_pair_candidates"),
        "best_min_support": meta.get("best_min_support"),
        "best_total_incidence": meta.get("best_total_incidence"),
        "support_gap": None
        if meta.get("best_min_support") is None
        else 327 - meta.get("best_min_support"),
        "selected_incidence_gap": meta.get("best_selected_incidence_gap"),
        "best_pair_count_max": meta.get("best_pair_count_max"),
        "best_repeated_fixed_group_count": meta.get("best_repeated_fixed_group_count"),
        "best_singleton_fixed_group_count": meta.get("best_singleton_fixed_group_count"),
        "candidate_min_support": best.get("min_support"),
        "candidate_total_incidence": best.get("selected_incidence_total"),
        "candidate_pair_count_max": best.get("pair_count_max"),
        "candidate_support_vector": best.get("support_vector"),
        "candidate_selected_fixed_point_histogram": best.get("selected_fixed_point_histogram"),
    }


def compact_rank3_pressure() -> dict[str, Any]:
    exact = load_json(RANK3_SINGLETON22_EXACT_PATH)
    pressure = load_json(RANK3_SINGLETON22_PRESSURE_PATH)
    out = {
        "exact": compact_exact(RANK3_SINGLETON22_EXACT_PATH),
        "pressure_path": str(RANK3_SINGLETON22_PRESSURE_PATH),
        "pressure_present": pressure is not None,
    }
    if not pressure:
        return out
    systems = pressure.get("systems", [])
    first = systems[0] if systems else {}
    dependency_last = None
    for core in first.get("pivot_cores", []):
        if core.get("mode") == "dependency_last":
            dependency_last = core
            break
    out["row_dependency_pressure"] = {
        "header_ok": header_ok(pressure),
        "best_failure_mode": pressure.get("row_dependency_pressure", {}).get("best_failure_mode"),
        "best_nullity": pressure.get("row_dependency_pressure", {}).get("best_nullity"),
        "systems_tested": pressure.get("row_dependency_pressure", {}).get("systems_tested"),
        "first_system_status": first.get("status"),
        "first_system_rank": first.get("rank"),
        "first_system_nullity": first.get("nullity"),
        "selected_group_histograms": first.get("selected_group_histograms"),
        "dependency_last_core": None
        if dependency_last is None
        else {
            "core_rank": dependency_last.get("core_rank"),
            "core_row_count": dependency_last.get("core_row_count"),
            "dependency_rows_in_core": dependency_last.get("dependency_rows_in_core"),
            "dependency_groups_in_core": dependency_last.get("dependency_groups_in_core"),
            "core_group_histograms": dependency_last.get("core_group_histograms"),
        },
    }
    if exact:
        systems = exact.get("systems", [])
        out["exact"]["first_system"] = systems[0] if systems else None
    return out


def compact_rank3_non_singleton_synthesized() -> dict[str, Any]:
    record = load_json(RANK3_NON_SINGLETON_SYNTH_SUMMARY_PATH)
    if not record:
        return {"path": str(RANK3_NON_SINGLETON_SYNTH_SUMMARY_PATH), "present": False}
    return {
        "path": str(RANK3_NON_SINGLETON_SYNTH_SUMMARY_PATH),
        "present": True,
        "header_ok": header_ok(record),
        "proof_status": record.get("proof_status"),
        "anchors": record.get("anchor_plan", {}).get("anchor_targets"),
        "carriers_emitted": record.get("synthesized_menu", {}).get("carriers_emitted"),
        "support_pair_candidates": record.get("schedule", {}).get("support_pair_candidates"),
        "best_min_support": record.get("schedule", {}).get("best_min_support"),
        "best_total_incidence": record.get("schedule", {}).get("best_total_incidence"),
        "best_pair_count_max": record.get("schedule", {}).get("best_pair_count_max"),
        "exact_best_nullity": record.get("exact_audit", {}).get("best_nullity"),
        "exact_systems_tested": record.get("exact_audit", {}).get("systems_tested"),
        "depmin2_support_pair_candidates": record.get("depmin2_schedule", {}).get("support_pair_candidates"),
        "depmin2_best_min_support": record.get("depmin2_schedule", {}).get("best_min_support"),
        "depmin2_best_total_incidence": record.get("depmin2_schedule", {}).get("best_total_incidence"),
        "depmin2_pair_count_max": record.get("depmin2_schedule", {}).get("best_pair_count_max"),
        "depmin2_exact_best_nullity": record.get("depmin2_exact_audit", {}).get("best_nullity"),
        "depmin3_support_pair_candidates": record.get("depmin3_schedule", {}).get("support_pair_candidates"),
        "depmin3_best_min_support": record.get("depmin3_schedule", {}).get("best_min_support"),
        "depmin3_best_total_incidence": record.get("depmin3_schedule", {}).get("best_total_incidence"),
        "depmin3_pair_count_max": record.get("depmin3_schedule", {}).get("best_pair_count_max"),
        "depmin3_selected_incidence_gap": record.get("depmin3_schedule", {}).get("best_selected_incidence_gap"),
        "depmin4_support_pair_candidates": record.get("depmin4_schedule", {}).get("support_pair_candidates"),
        "depmin4_best_min_support": record.get("depmin4_schedule", {}).get("best_min_support"),
        "depmin4_best_total_incidence": record.get("depmin4_schedule", {}).get("best_total_incidence"),
        "depmin4_pair_count_max": record.get("depmin4_schedule", {}).get("best_pair_count_max"),
        "depmin4_selected_incidence_gap": record.get("depmin4_schedule", {}).get("best_selected_incidence_gap"),
    }


def compact_support_first_schedule(path: Path) -> dict[str, Any]:
    record = load_json(path)
    if not record:
        return {"path": str(path), "present": False}
    meta = record.get("rank3_singleton_blocked_support_first", {})
    paircap_rows = [
        row
        for row in record.get("candidates", [])
        if row.get("stage") == "paircap_front" and row.get("support_vector")
    ]
    best_paircap = max(
        paircap_rows,
        key=lambda row: (
            int(row.get("min_support", -1)),
            int(row.get("selected_incidence_total", -1)),
            -int(row.get("pair_count_max", 999)),
        ),
        default={},
    )
    return {
        "path": str(path),
        "present": True,
        "header_ok": header_ok(record),
        "proof_status": record.get("proof_status"),
        "best_failure_mode": meta.get("best_failure_mode"),
        "subspaces_solved": meta.get("subspaces_solved"),
        "solved_stage_rows": meta.get("solved_stage_rows"),
        "support_pair_candidates": meta.get("support_pair_candidates"),
        "near_front_candidates": meta.get("near_front_candidates"),
        "best_min_support": meta.get("best_min_support"),
        "best_total_incidence": meta.get("best_total_incidence"),
        "best_pair_count_max": meta.get("best_pair_count_max"),
        "best_support_pair_min_support": meta.get("best_support_pair_min_support"),
        "best_support_pair_total_incidence": meta.get("best_support_pair_total_incidence"),
        "best_support_pair_pair_count_max": meta.get("best_support_pair_pair_count_max"),
        "best_support_pair_max_projective_key_support": meta.get("best_support_pair_max_projective_key_support"),
        "min_projective_key_count": meta.get("min_projective_key_count"),
        "repeat_weight": meta.get("repeat_weight"),
        "best_paircap_min_support": best_paircap.get("min_support"),
        "best_paircap_total_incidence": best_paircap.get("selected_incidence_total"),
        "best_paircap_pair_count_max": best_paircap.get("pair_count_max"),
        "best_paircap_projective_key_support": best_paircap.get("max_selected_projective_key_support"),
    }


def compact_singleton_blocked_pressure(path: Path) -> dict[str, Any]:
    record = load_json(path)
    if not record:
        return {"path": str(path), "present": False}
    meta = record.get("row_dependency_pressure", {})
    systems = record.get("systems", [])
    first = systems[0] if systems else {}
    zero_last = None
    for core in first.get("pivot_cores", []):
        if core.get("mode") == "zero_last":
            zero_last = core
            break
    greedy = first.get("greedy_core", {})
    return {
        "path": str(path),
        "present": True,
        "header_ok": header_ok(record),
        "best_failure_mode": meta.get("best_failure_mode"),
        "systems_tested": meta.get("systems_tested"),
        "best_nullity": meta.get("best_nullity"),
        "positive_nullity_systems": meta.get("positive_nullity_systems"),
        "first_system_status": first.get("status"),
        "first_system_matrix_shape": first.get("matrix_shape"),
        "first_system_rank": first.get("rank"),
        "first_system_nullity": first.get("nullity"),
        "rank_drop_histogram": first.get("rank_drop_histogram"),
        "greedy_core_row_count": greedy.get("greedy_core_row_count"),
        "greedy_core_rank": greedy.get("greedy_core_rank"),
        "greedy_removed_group_count": greedy.get("greedy_removed_group_count"),
        "greedy_core_group_histograms": greedy.get("greedy_core_group_histograms"),
        "zero_last_core": None
        if zero_last is None
        else {
            "core_row_count": zero_last.get("core_row_count"),
            "core_rank": zero_last.get("core_rank"),
            "core_group_histograms": zero_last.get("core_group_histograms"),
        },
    }


def compact_rank3_singleton_blocked_current() -> dict[str, Any]:
    return {
        "support_first": compact_support_first_schedule(RANK3_SINGLETON_BLOCKED_SUPPORT_PATH),
        "exact": compact_exact(RANK3_SINGLETON_BLOCKED_EXACT_PATH),
        "row_pressure": compact_singleton_blocked_pressure(RANK3_SINGLETON_BLOCKED_PRESSURE_PATH),
        "repeat_pressure": compact_support_first_schedule(RANK3_SINGLETON_BLOCKED_REPEAT_PATH),
    }


def compact_rank3_core_dependency_smoke() -> dict[str, Any]:
    record = load_json(RANK3_CORE_DEPENDENCY_SUMMARY_PATH)
    if not record:
        return {"path": str(RANK3_CORE_DEPENDENCY_SUMMARY_PATH), "present": False}
    return {
        "path": str(RANK3_CORE_DEPENDENCY_SUMMARY_PATH),
        "present": True,
        "header_ok": header_ok(record),
        "proof_status": record.get("proof_status"),
        "anchor_targets": record.get("core_dependency_anchor_file", {}).get("anchor_targets"),
        "replacement_rows": record.get("core_dependency_anchor_file", {}).get("replacement_rows"),
        "support_pair_replacements": record.get("core_dependency_anchor_file", {}).get("support_pair_replacements"),
        "carriers_emitted": record.get("synthesis_smoke", {}).get("carriers_emitted"),
        "support_pair_candidates": record.get("support_schedule_smoke", {}).get("support_pair_candidates"),
        "best_support_pair_min_support": record.get("support_schedule_smoke", {}).get("best_support_pair_min_support"),
        "best_support_pair_total_incidence": record.get("support_schedule_smoke", {}).get("best_support_pair_total_incidence"),
        "best_support_pair_pair_count_max": record.get("support_schedule_smoke", {}).get("best_support_pair_pair_count_max"),
        "exact_best_nullity": record.get("exact_smoke", {}).get("best_nullity"),
        "exact_positive_nullity_systems": record.get("exact_smoke", {}).get("positive_nullity_systems"),
        "row_pressure_best_nullity": record.get("row_pressure_smoke", {}).get("best_nullity"),
        "witness_constructed": record.get("witness_smoke", {}).get("constructed"),
    }


def compact_rank3_generic_core_nogoods() -> dict[str, Any]:
    nogoods = load_json(RANK3_GENERIC_CORE_NOGOODS_PATH)
    schedule = load_json(RANK3_CORE_NOGOOD_LOWROW_PATH)
    pressure = load_json(RANK3_CORE_NOGOOD_PRESSURE_PATH)
    out: dict[str, Any] = {
        "nogoods_path": str(RANK3_GENERIC_CORE_NOGOODS_PATH),
        "schedule_path": str(RANK3_CORE_NOGOOD_LOWROW_PATH),
        "exact_path": str(RANK3_CORE_NOGOOD_EXACT_PATH),
        "witness_path": str(RANK3_CORE_NOGOOD_WITNESS_PATH),
        "pressure_path": str(RANK3_CORE_NOGOOD_PRESSURE_PATH),
        "nogoods_present": nogoods is not None,
        "schedule_present": schedule is not None,
        "pressure_present": pressure is not None,
        "exact": compact_exact(RANK3_CORE_NOGOOD_EXACT_PATH),
        "witness": compact_exact(RANK3_CORE_NOGOOD_WITNESS_PATH, key="witness_audit"),
    }
    if nogoods:
        meta = nogoods.get("generic_core_nogoods", {})
        out["nogoods"] = {
            "header_ok": header_ok(nogoods),
            "proof_status": nogoods.get("proof_status"),
            "pressure_files_scanned": meta.get("pressure_files_scanned"),
            "pressure_systems_scanned": meta.get("pressure_systems_scanned"),
            "eligible_dependency_free_full_rank_systems": meta.get(
                "eligible_dependency_free_full_rank_systems"
            ),
            "unique_core_nogoods": meta.get("unique_core_nogoods"),
            "singleton_projective_core_nogoods": meta.get("singleton_projective_core_nogoods"),
        }
    if schedule:
        meta = schedule.get("rank3_lowrow_schedule", {})
        out["guarded_schedule"] = {
            "header_ok": header_ok(schedule),
            "proof_status": schedule.get("proof_status"),
            "forbid_core_subsets": meta.get("forbid_core_subsets"),
            "support_pair_candidates": meta.get("support_pair_candidates"),
            "best_min_support": meta.get("best_min_support"),
            "best_total_incidence": meta.get("best_total_incidence"),
            "best_pair_count_max": meta.get("best_pair_count_max"),
            "best_core_nogood_constraints": meta.get("best_core_nogood_constraints"),
            "best_max_selected_projective_key_support": meta.get(
                "best_max_selected_projective_key_support"
            ),
        }
    if pressure:
        meta = pressure.get("row_dependency_pressure", {})
        systems = pressure.get("systems", [])
        dependency_free_cores = 0
        singleton_projective_systems = 0
        for system in systems:
            hist = system.get("selected_group_histograms", {})
            if int(hist.get("max_projective_key_support", 0) or 0) <= 1:
                singleton_projective_systems += 1
            for core in system.get("pivot_cores", []):
                if int(core.get("dependency_groups_in_core", 0) or 0) == 0:
                    dependency_free_cores += 1
        out["followup_pressure"] = {
            "header_ok": header_ok(pressure),
            "proof_status": pressure.get("proof_status"),
            "systems_tested": meta.get("systems_tested"),
            "best_nullity": meta.get("best_nullity"),
            "positive_nullity_systems": meta.get("positive_nullity_systems"),
            "dependency_free_pivot_cores": dependency_free_cores,
            "singleton_projective_systems": singleton_projective_systems,
        }
    return out


def build_triage() -> dict[str, Any]:
    rank_one = load_json(RANK_ONE_PATH)
    rank_one_obstruction = None
    if rank_one:
        rank_one_obstruction = rank_one.get("rank_one_mu8_carrier_obstruction")

    witness_sweep = compact_witness_sweep()
    rank2_sweep = compact_rank2_sweep()
    rank2_exact_sweep = compact_exact_sweep("m1_a327_mu8_rank2_")
    rank3_exact_sweep = compact_exact_sweep("m1_a327_mu8_rank3_")
    rank3_pressure_sweep = compact_rank3_pressure_sweep()

    rank2 = {
        "adaptive": compact_rank2_adaptive(RANK2_ADAPTIVE_PATH),
        "feedback": compact_rank2_adaptive(RANK2_FEEDBACK_PATH),
        "feedback2": compact_rank2_adaptive(RANK2_FEEDBACK2_PATH),
        "frontier": compact_rank2_frontier(),
        "feedback_exact": compact_exact(RANK2_FEEDBACK_EXACT_PATH),
        "width16_near_exact": compact_exact(RANK2_WIDTH16_EXACT_PATH, key="near_front_exact"),
        "adaptive_sweep": rank2_sweep,
        "exact_sweep": rank2_exact_sweep,
    }

    rank3_singleton = {
        str(cap): compact_rank3_singleton(cap, path)
        for cap, path in sorted(RANK3_SINGLETON_FILES.items(), reverse=True)
    }
    rank3 = {
        "singleton_boundary": rank3_singleton,
        "singleton22_exact_and_pressure": compact_rank3_pressure(),
        "non_singleton_synthesized_dependency": compact_rank3_non_singleton_synthesized(),
        "singleton_blocked_current": compact_rank3_singleton_blocked_current(),
        "core_dependency_smoke": compact_rank3_core_dependency_smoke(),
        "generic_core_nogoods": compact_rank3_generic_core_nogoods(),
        "exact_sweep": rank3_exact_sweep,
        "row_pressure_sweep": rank3_pressure_sweep,
    }

    evidence_files = [
        RANK_ONE_PATH,
        RANK2_ADAPTIVE_PATH,
        RANK2_FEEDBACK_PATH,
        RANK2_FEEDBACK2_PATH,
        RANK2_FRONTIER_PATH,
        RANK2_CEILING_PATH,
        RANK2_FEEDBACK_EXACT_PATH,
        RANK2_WIDTH16_EXACT_PATH,
        *RANK3_SINGLETON_FILES.values(),
        RANK3_SINGLETON22_EXACT_PATH,
        RANK3_SINGLETON22_PRESSURE_PATH,
        RANK3_NON_SINGLETON_SYNTH_SUMMARY_PATH,
        RANK3_SINGLETON_BLOCKED_SUPPORT_PATH,
        RANK3_SINGLETON_BLOCKED_EXACT_PATH,
        RANK3_SINGLETON_BLOCKED_PRESSURE_PATH,
        RANK3_SINGLETON_BLOCKED_REPEAT_PATH,
        RANK3_CORE_DEPENDENCY_SUMMARY_PATH,
        RANK3_GENERIC_CORE_NOGOODS_PATH,
        RANK3_CORE_NOGOOD_LOWROW_PATH,
        RANK3_CORE_NOGOOD_EXACT_PATH,
        RANK3_CORE_NOGOOD_WITNESS_PATH,
        RANK3_CORE_NOGOOD_PRESSURE_PATH,
    ]
    file_hashes = {str(path): sha256_file(path) for path in evidence_files if path.exists()}
    tracked_files = git_tracked_files()
    existing_evidence = [str(path) for path in evidence_files if path.exists()]
    missing_evidence = [str(path) for path in evidence_files if not path.exists()]
    tracked_evidence = sorted(path for path in existing_evidence if path in tracked_files)
    untracked_evidence = sorted(path for path in existing_evidence if path not in tracked_files)
    evidence_tracking = {
        "evidence_files_expected": len(evidence_files),
        "evidence_files_hashed": len(file_hashes),
        "tracked_count": len(tracked_evidence),
        "untracked_count": len(untracked_evidence),
        "missing_count": len(missing_evidence),
        "tracked_files": tracked_evidence,
        "untracked_files": untracked_evidence,
        "missing_files": missing_evidence,
        "self_contained_for_public_pr": not untracked_evidence and not missing_evidence,
    }
    self_contained = evidence_tracking["self_contained_for_public_pr"]

    board_ready = False
    exact_witness = witness_sweep["exact_a327_witness_passes"] > 0
    route_cut_candidate = bool(rank_one_obstruction and rank3["singleton22_exact_and_pressure"]["exact"].get("best_nullity") == 0)

    record = base_record()
    record.update(
        {
            "proof_status": "PARTIAL / EXPERIMENTAL",
            "public_packet_triage": {
                "board_ready": board_ready,
                "exact_a327_witness": exact_witness,
                "route_cut_candidate": route_cut_candidate,
                "recommended_public_action": (
                    "open_narrow_route_cut_pr_if_desired"
                    if self_contained and route_cut_candidate and not exact_witness
                    else "do_not_open_board_pr_yet"
                ),
                "reason": (
                    "No exact a=327 witness exists.  The current useful output is a compact "
                    "route-cut/triage packet: rank-one mu8 carriers are structurally cut, "
                    "rank-2 menus remain support-infeasible across the scanned adaptive ledgers, "
                    "and the current rank-3 exact/row-pressure sweep is consistently full rank; "
                    "the newer non-singleton synthesized rank-3 menu is also full-rank at the "
                    "support/pair gate and loses support when dependency-row pressure is raised. "
                    "The latest singleton-blocked rank-3 sample likewise passes support/pair only "
                    "in a generic exact-full-rank schedule, while hard reuse of the available "
                    "repeated projective keys loses the support front.  A new core-dependency "
                    "anchor smoke can synthesize carriers and pass support/pair, but its exact "
                    "audit is also full-rank.  A generic-core no-good layer blocks previously "
                    "mined dependency-free full-rank pivot cores while preserving support/pair, "
                    "but exact Sage and follow-up pressure audits still find fresh full-rank "
                    "singleton-projective cores.  The evidence-tracking audit "
                    + (
                        "shows this packet is self-contained as a narrow route-cut PR candidate; "
                        "it is still not board-ready because no exact witness or global theorem is claimed."
                        if self_contained
                        else (
                            "also shows this packet is not self-contained for a public PR as-is: "
                            f"{len(untracked_evidence)} hashed evidence files are local untracked ledgers."
                        )
                    )
                ),
            },
            "witness_sweep": witness_sweep,
            "rank_one_mu8": {
                "path": str(RANK_ONE_PATH),
                "header_ok": header_ok(rank_one),
                "obstruction": rank_one_obstruction,
            },
            "rank2_mu8": rank2,
            "rank3_mu8": rank3,
            "next_best_attack": {
                "primary": "new_dependency_family",
                "avoid": [
                    "more mutation of the same fixed rank-3 menu",
                    "board update without exact witness or theorem-style route cut",
                ],
                "options": [
                    "rank-2 feedback carrier synthesis with better balanced carrier planes",
                    "rank-3 menus whose dependency rows cannot be bypassed by singleton fixed groups",
                    "structural constraints against singleton projective-key full-rank cores",
                    "module/syzygy abstraction of the repeated full-rank singleton pivot pattern",
                ],
            },
            "tooling": {
                "support_pair_scheduler": "OR-Tools CP-SAT",
                "exact_authority": "Sage GF(17^32)",
                "reproducibility": "Python JSON verifiers",
                "module_syzygy_if_packaging_obstruction": ["Macaulay2", "Singular"],
                "not_primary_now": ["PARI/GP", "Wolfram", "msolve"],
            },
            "evidence_hashes_sha256": file_hashes,
            "evidence_tracking": evidence_tracking,
        }
    )
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true", help="print JSON to stdout")
    parser.add_argument("--output", type=Path, default=OUT_PATH)
    args = parser.parse_args()

    record = build_triage()
    text = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    if args.json or not args.write:
        print(text, end="")


if __name__ == "__main__":
    main()
