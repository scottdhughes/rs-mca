#!/usr/bin/env python3
"""CP-SAT partition scheduler for rank-2 mu_8 carrier menus."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


VENV_PYTHON = Path("/Users/scott/.venvs/rs-mca-ortools/bin/python")
if os.environ.get("RS_MCA_ORTOOLS_REEXEC") != "1":
    try:
        from ortools.sat.python import cp_model  # type: ignore
    except ModuleNotFoundError:
        if VENV_PYTHON.exists():
            os.environ["RS_MCA_ORTOOLS_REEXEC"] = "1"
            os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), *sys.argv])
        raise
else:
    from ortools.sat.python import cp_model  # type: ignore


MENU_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_menu.json")
OUTPUT_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_schedule_candidates.json")
SAGE_SCRIPT = Path("experimental/scripts/audit_m1_a327_mu8_rank2_cpsat_exact.sage")

TARGET_AGREEMENT = 327
REQUIRED_INCIDENCES = 7 * TARGET_AGREEMENT
PAIR_CAP = 255
INTERPOLATION_ROW_CAP = 63
LABELS = list(range(7))
PAIR_LABELS = [(left, right) for left in range(7) for right in range(left + 1, 7)]

NOT_CLAIMED = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def ensure_menu(plane_limit: int, ratio_limit: int) -> None:
    cmd = [
        "sage",
        str(SAGE_SCRIPT),
        "--build-menu-json",
        "--json",
        "--plane-limit",
        str(plane_limit),
        "--ratio-limit",
        str(ratio_limit),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def solve_plane(plane: dict[str, Any], max_time: float, workers: int) -> dict[str, Any]:
    model = cp_model.CpModel()
    z_vars: dict[tuple[int, int], cp_model.IntVar] = {}
    x_vars: dict[tuple[int, int, int, int], cp_model.IntVar] = {}
    option_lookup: dict[tuple[int, int], dict[str, Any]] = {}
    block_lookup: dict[tuple[int, int, int, int], list[int]] = {}

    for qidx, qrow in enumerate(plane["quotient_points"]):
        z_for_q = []
        for opt_idx, option in enumerate(qrow["options"]):
            z = model.NewBoolVar(f"z_{qidx}_{opt_idx}")
            z_vars[(qidx, opt_idx)] = z
            z_for_q.append(z)
            option_lookup[(qidx, opt_idx)] = option
        model.Add(sum(z_for_q) == 1)
        for phase in range(8):
            x_for_phase = []
            for opt_idx, option in enumerate(qrow["options"]):
                blocks = option["phase_blocks"][phase]
                for block_idx, block in enumerate(blocks):
                    x = model.NewBoolVar(f"x_{qidx}_{opt_idx}_{phase}_{block_idx}")
                    x_vars[(qidx, opt_idx, phase, block_idx)] = x
                    block_lookup[(qidx, opt_idx, phase, block_idx)] = block
                    model.Add(x <= z_vars[(qidx, opt_idx)])
                    x_for_phase.append(x)
            model.Add(sum(x_for_phase) == 1)

    support_exprs = []
    for label in LABELS:
        terms = [
            x for key, x in x_vars.items()
            if label in block_lookup[key]
        ]
        support_exprs.append(sum(terms))

    pair_exprs = []
    for left, right in PAIR_LABELS:
        terms = [
            x for key, x in x_vars.items()
            if left in block_lookup[key] and right in block_lookup[key]
        ]
        expr = sum(terms)
        pair_exprs.append(expr)
        model.Add(expr <= PAIR_CAP)

    row_cost_terms = []
    for key, z in z_vars.items():
        row_cost_terms.append(int(option_lookup[key]["row_cost"]) * z)
    row_cost = sum(row_cost_terms)
    model.Add(row_cost <= INTERPOLATION_ROW_CAP)

    min_support = model.NewIntVar(0, 512, "min_support")
    for expr in support_exprs:
        model.Add(min_support <= expr)
    pair_max = model.NewIntVar(0, PAIR_CAP, "pair_max")
    for expr in pair_exprs:
        model.Add(pair_max >= expr)
    total_incidence = sum(support_exprs)
    model.Maximize(1_000_000 * min_support + 1_000 * total_incidence - 100 * pair_max - row_cost)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {
            "plane_id": plane["plane_id"],
            "solver_status": status_name,
            "guard_pass": False,
            "best_failure_mode": "MU8_RANK2_CARRIER_PLANE_SUPPORT_PAIR_SLACK_INFEASIBLE",
        }

    support = [int(solver.Value(expr)) for expr in support_exprs]
    pair_counts = [int(solver.Value(expr)) for expr in pair_exprs]
    chosen = []
    ratio_line_counts: dict[str, int] = {}
    for qidx, qrow in enumerate(plane["quotient_points"]):
        chosen_option_idx = None
        for opt_idx, _option in enumerate(qrow["options"]):
            if solver.Value(z_vars[(qidx, opt_idx)]) == 1:
                chosen_option_idx = opt_idx
                break
        assert chosen_option_idx is not None
        option = option_lookup[(qidx, chosen_option_idx)]
        phase_blocks = []
        for phase in range(8):
            for block_idx, block in enumerate(option["phase_blocks"][phase]):
                if solver.Value(x_vars[(qidx, chosen_option_idx, phase, block_idx)]) == 1:
                    phase_blocks.append(block)
                    break
        if option["kind"] == "RATIO":
            ratio_line_counts[option["ratio_key"]] = ratio_line_counts.get(option["ratio_key"], 0) + 1
        chosen.append(
            {
                "qidx": qidx,
                "option_id": option["option_id"],
                "kind": option["kind"],
                "row_cost": option["row_cost"],
                "ratio_key": option.get("ratio_key"),
                "selected_blocks_by_phase": phase_blocks,
            }
        )
    row_cost_value = int(solver.Value(row_cost))
    guard_pass = (
        min(support) >= TARGET_AGREEMENT
        and sum(support) >= REQUIRED_INCIDENCES
        and max(pair_counts) <= PAIR_CAP
        and row_cost_value <= INTERPOLATION_ROW_CAP
    )
    max_ratio_support = max(ratio_line_counts.values(), default=0)
    forced_global_ratio_count = sum(1 for value in ratio_line_counts.values() if value >= 32)
    return {
        "candidate_id": f"{plane['plane_id']}_cpsat",
        "plane_id": plane["plane_id"],
        "solver_status": status_name,
        "objective_value": int(solver.ObjectiveValue()),
        "support_vector": support,
        "min_support": min(support),
        "selected_incidence_total": sum(support),
        "pair_counts": pair_counts,
        "pair_count_max": max(pair_counts),
        "interpolation_row_cost": row_cost_value,
        "ratio_line_classes": len(ratio_line_counts),
        "ratio_support_histogram": {
            str(size): sum(1 for value in ratio_line_counts.values() if value == size)
            for size in sorted(set(ratio_line_counts.values()))
        },
        "max_ratio_support": max_ratio_support,
        "forced_global_ratio_count": forced_global_ratio_count,
        "rank_one_collapse_detected": forced_global_ratio_count > 0,
        "guard_pass": guard_pass,
        "best_failure_mode": (
            "MU8_RANK2_CPSAT_GUARD_PASSING_SCHEDULE"
            if guard_pass
            else "MU8_RANK2_CARRIER_PLANE_SUPPORT_PAIR_SLACK_INFEASIBLE"
        ),
        "chosen_options": chosen,
    }


def build_record(plane_limit: int, ratio_limit: int, max_time: float, workers: int) -> dict[str, Any]:
    ensure_menu(plane_limit=plane_limit, ratio_limit=ratio_limit)
    menu = load_json(MENU_PATH)
    candidates = []
    for plane in menu["planes"]:
        candidates.append(solve_plane(plane, max_time=max_time, workers=workers))
    guard_passing = [row for row in candidates if row.get("guard_pass")]
    stored_candidates = []
    for row in candidates:
        if row.get("guard_pass"):
            stored_candidates.append(row)
            continue
        compact = {key: value for key, value in row.items() if key != "chosen_options"}
        compact["chosen_options_stored"] = False
        compact["chosen_options_omitted_reason"] = "candidate_failed_support_pair_slack_guards"
        stored_candidates.append(compact)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "ddc7fe9",
        "cpsat_scheduler": {
            "ortools_version": cp_model.__name__.split(".")[0],
            "planes_solved": len(candidates),
            "ratio_limit": ratio_limit,
            "guard_passing_schedules": len(guard_passing),
            "max_time_seconds_per_plane": max_time,
            "interpolation_row_cap": INTERPOLATION_ROW_CAP,
            "best_min_support": max([row.get("min_support", 0) for row in candidates], default=0),
            "best_selected_incidence_total": max([row.get("selected_incidence_total", 0) for row in candidates], default=0),
            "best_failure_mode": (
                "MU8_RANK2_CPSAT_GUARD_PASSING_SCHEDULE"
                if guard_passing
                else "MU8_RANK2_CARRIER_PLANE_SUPPORT_PAIR_SLACK_INFEASIBLE"
            ),
        },
        "candidates": stored_candidates,
        "proof_status": (
            "CANDIDATE / MU8_RANK2_CPSAT_GUARD_PASSING_SCHEDULE / PARTIAL / EXPERIMENTAL"
            if guard_passing
            else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_PLANE_SUPPORT_PAIR_SLACK_INFEASIBLE / PARTIAL / EXPERIMENTAL"
        ),
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def compact_menu_record(menu: dict[str, Any], plane_limit: int, ratio_limit: int) -> dict[str, Any]:
    option_counts = []
    ratio_counts = []
    for plane in menu["planes"]:
        counts = []
        ratios = []
        for qrow in plane["quotient_points"]:
            counts.append(len(qrow["options"]))
            ratios.append(sum(1 for option in qrow["options"] if option["kind"] == "RATIO"))
        option_counts.extend(counts)
        ratio_counts.extend(ratios)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "ddc7fe9",
        "menu": {
            "field": "GF(17^32)",
            "planes": len(menu["planes"]),
            "quotient_points": 64,
            "ratio_limit": ratio_limit,
            "stored_as": "compact_summary",
            "exact_menu_rebuild_required_for_interpolation": True,
            "min_options_per_quotient": min(option_counts) if option_counts else None,
            "max_options_per_quotient": max(option_counts) if option_counts else None,
            "max_ratio_options_per_quotient": max(ratio_counts) if ratio_counts else None,
        },
        "plane_ids": [plane["plane_id"] for plane in menu["planes"][:plane_limit]],
        "proof_status": "CANDIDATE / MU8_RANK2_CPSAT_MENU_READY / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--plane-limit", type=int, default=64)
    parser.add_argument("--ratio-limit", type=int, default=4)
    parser.add_argument("--max-time", type=float, default=2.0)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        plane_limit=args.plane_limit,
        ratio_limit=args.ratio_limit,
        max_time=args.max_time,
        workers=args.workers,
    )
    if args.write:
        OUTPUT_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        full_menu = load_json(MENU_PATH)
        MENU_PATH.write_text(
            json.dumps(compact_menu_record(full_menu, args.plane_limit, args.ratio_limit), indent=2, sort_keys=True) + "\n"
        )
    summary = {
        "proof_status": record["proof_status"],
        "planes_solved": record["cpsat_scheduler"]["planes_solved"],
        "guard_passing_schedules": record["cpsat_scheduler"]["guard_passing_schedules"],
        "best_min_support": record["cpsat_scheduler"]["best_min_support"],
        "best_selected_incidence_total": record["cpsat_scheduler"]["best_selected_incidence_total"],
        "best_failure_mode": record["cpsat_scheduler"]["best_failure_mode"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_RANK2_CPSAT_PARTITION_SCHEDULER_READY")


if __name__ == "__main__":
    main()
