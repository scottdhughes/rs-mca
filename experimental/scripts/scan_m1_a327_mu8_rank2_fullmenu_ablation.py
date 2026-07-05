#!/usr/bin/env python3
"""Width ablation for rank-2 mu_8 carrier partition scheduling."""

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


SAGE_SCRIPT = Path("experimental/scripts/audit_m1_a327_mu8_rank2_cpsat_exact.sage")
MENU_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_menu.json")
WIDTH_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_width_ablation.json")
SCHEDULE_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_fullmenu_schedule_candidates.json")

TARGET = 327
REQUIRED_TOTAL = 7 * TARGET
PAIR_CAP = 255
LABELS = list(range(7))
PAIRS = [(i, j) for i in range(7) for j in range(i + 1, 7)]
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


def build_menu(plane_limit: int, width: int) -> dict[str, Any]:
    subprocess.run(
        [
            "sage",
            str(SAGE_SCRIPT),
            "--build-menu-json",
            "--json",
            "--plane-limit",
            str(plane_limit),
            "--ratio-limit",
            str(width),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return load_json(MENU_PATH)


def compact_menu(menu: dict[str, Any], width: int) -> dict[str, Any]:
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": "46a0755",
        "menu": {
            "field": "GF(17^32)",
            "planes": len(menu["planes"]),
            "quotient_points": 64,
            "ratio_limit": width,
            "stored_as": "compact_summary",
            "exact_menu_rebuild_required_for_interpolation": True,
        },
        "plane_ids": [plane["plane_id"] for plane in menu["planes"]],
        "proof_status": "CANDIDATE / MU8_RANK2_FULLMENU_MENU_READY / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def solve_plane(plane: dict[str, Any], max_time: float, workers: int) -> dict[str, Any]:
    model = cp_model.CpModel()
    z_vars = {}
    x_vars = {}
    option_lookup = {}
    block_lookup = {}
    for qidx, qrow in enumerate(plane["quotient_points"]):
        z_for_q = []
        for opt_idx, option in enumerate(qrow["options"]):
            z = model.NewBoolVar(f"z_{qidx}_{opt_idx}")
            z_vars[(qidx, opt_idx)] = z
            option_lookup[(qidx, opt_idx)] = option
            z_for_q.append(z)
        model.Add(sum(z_for_q) == 1)
        for phase in range(8):
            x_for_phase = []
            for opt_idx, option in enumerate(qrow["options"]):
                for block_idx, block in enumerate(option["phase_blocks"][phase]):
                    x = model.NewBoolVar(f"x_{qidx}_{opt_idx}_{phase}_{block_idx}")
                    key = (qidx, opt_idx, phase, block_idx)
                    x_vars[key] = x
                    block_lookup[key] = block
                    model.Add(x <= z_vars[(qidx, opt_idx)])
                    x_for_phase.append(x)
            model.Add(sum(x_for_phase) == 1)

    supports = []
    for label in LABELS:
        supports.append(sum(var for key, var in x_vars.items() if label in block_lookup[key]))
    pair_loads = []
    for left, right in PAIRS:
        expr = sum(
            var for key, var in x_vars.items()
            if left in block_lookup[key] and right in block_lookup[key]
        )
        model.Add(expr <= PAIR_CAP)
        pair_loads.append(expr)
    row_cost = sum(int(option_lookup[key]["row_cost"]) * z for key, z in z_vars.items())
    min_support = model.NewIntVar(0, 512, "min_support")
    for expr in supports:
        model.Add(min_support <= expr)
    pair_max = model.NewIntVar(0, PAIR_CAP, "pair_max")
    for expr in pair_loads:
        model.Add(pair_max >= expr)
    total = sum(supports)
    # Row cost is soft here. Exact Sage rank is the only algebraic gate.
    model.Maximize(1_000_000 * min_support + 1_000 * total - 100 * pair_max - row_cost)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {"plane_id": plane["plane_id"], "solver_status": solver.StatusName(status), "guard_pass": False}
    support = [int(solver.Value(expr)) for expr in supports]
    pairs = [int(solver.Value(expr)) for expr in pair_loads]
    ratio_counts: dict[str, int] = {}
    chosen = []
    for qidx, qrow in enumerate(plane["quotient_points"]):
        opt_idx = next(idx for idx, _ in enumerate(qrow["options"]) if solver.Value(z_vars[(qidx, idx)]) == 1)
        option = option_lookup[(qidx, opt_idx)]
        phase_blocks = []
        for phase in range(8):
            for block_idx, block in enumerate(option["phase_blocks"][phase]):
                if solver.Value(x_vars[(qidx, opt_idx, phase, block_idx)]) == 1:
                    phase_blocks.append(block)
                    break
        if option["kind"] == "RATIO":
            ratio_counts[option["ratio_key"]] = ratio_counts.get(option["ratio_key"], 0) + 1
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
    support_pass = min(support) >= TARGET
    pair_pass = max(pairs) <= PAIR_CAP
    total_pass = sum(support) >= REQUIRED_TOTAL
    guard_pass = support_pass and pair_pass and total_pass
    row_cost_value = int(solver.Value(row_cost))
    stored = {
        "candidate_id": f"{plane['plane_id']}_w{len(plane['quotient_points'][0]['options']) - 2}",
        "plane_id": plane["plane_id"],
        "solver_status": solver.StatusName(status),
        "support_vector": support,
        "min_support": min(support),
        "selected_incidence_total": sum(support),
        "pair_count_max": max(pairs),
        "pair_counts": pairs,
        "row_cost": row_cost_value,
        "support_pass": support_pass,
        "pair_cap_pass": pair_pass,
        "total_incidence_pass": total_pass,
        "support_pair_pass": guard_pass,
        "guard_pass": guard_pass,
        "ratio_line_support_histogram": {
            str(size): sum(1 for value in ratio_counts.values() if value == size)
            for size in sorted(set(ratio_counts.values()))
        },
        "max_ratio_line_support": max(ratio_counts.values(), default=0),
    }
    if guard_pass:
        stored["chosen_options"] = chosen
    else:
        stored["chosen_options_stored"] = False
    return stored


def run_width(width: int, plane_limit: int, max_time: float, workers: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    menu = build_menu(plane_limit, width)
    rows = [solve_plane(plane, max_time, workers) for plane in menu["planes"]]
    compact = compact_menu(menu, width)
    MENU_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n")
    best_min = max([row.get("min_support", 0) for row in rows], default=0)
    best_total = max([row.get("selected_incidence_total", 0) for row in rows], default=0)
    return (
        {
            "width": width,
            "planes_solved": len(rows),
            "guard_passing": sum(1 for row in rows if row.get("guard_pass")),
            "support_pair_passing": sum(1 for row in rows if row.get("support_pair_pass")),
            "best_min_support": best_min,
            "best_total_incidence": best_total,
            "best_failure_mode": (
                "MU8_RANK2_FULLMENU_SUPPORT_PAIR_PASS"
                if any(row.get("guard_pass") for row in rows)
                else "MU8_RANK2_CARRIER_FULL_MENU_SUPPORT_PAIR_INFEASIBLE"
            ),
        },
        rows,
    )


def parse_widths(raw: str) -> list[int]:
    return [int(value) for value in raw.split(",") if value.strip()]


def build_records(widths: list[int], plane_limit: int, max_time: float, workers: int) -> tuple[dict[str, Any], dict[str, Any]]:
    width_rows = []
    candidate_rows = []
    for width in widths:
        summary, rows = run_width(width, plane_limit, max_time, workers)
        width_rows.append(summary)
        for row in rows:
            row["width"] = width
            candidate_rows.append(row)
    guard_rows = [row for row in candidate_rows if row.get("guard_pass")]
    width4 = next((row for row in width_rows if row["width"] == 4), None)
    best_min = max([row["best_min_support"] for row in width_rows], default=0)
    best_total = max([row["best_total_incidence"] for row in width_rows], default=0)
    status = (
        "CANDIDATE / MU8_RANK2_FULLMENU_SUPPORT_PAIR_PASS / PARTIAL / EXPERIMENTAL"
        if guard_rows
        else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_FULL_MENU_SUPPORT_PAIR_INFEASIBLE / PARTIAL / EXPERIMENTAL"
    )
    width_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": "46a0755",
        "width_ablation": {
            "widths_tested": widths,
            "planes_per_width": plane_limit,
            "hard_row_slack_gate": False,
            "width4_best_min_support": None if width4 is None else width4["best_min_support"],
            "width4_best_total_incidence": None if width4 is None else width4["best_total_incidence"],
            "best_min_support": best_min,
            "best_total_incidence": best_total,
            "guard_passing_candidates": len(guard_rows),
            "best_failure_mode": (
                "MU8_RANK2_FULLMENU_SUPPORT_PAIR_PASS"
                if guard_rows
                else "MU8_RANK2_CARRIER_FULL_MENU_SUPPORT_PAIR_INFEASIBLE"
            ),
        },
        "width_results": width_rows,
        "proof_status": status,
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    schedule_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": "46a0755",
        "schedule_candidates": {
            "candidates_tested": len(candidate_rows),
            "guard_passing_candidates": len(guard_rows),
            "best_min_support": best_min,
            "best_total_incidence": best_total,
            "best_failure_mode": width_record["width_ablation"]["best_failure_mode"],
        },
        "candidates": candidate_rows,
        "proof_status": status,
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    return width_record, schedule_record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--plane-limit", type=int, default=64)
    parser.add_argument("--widths", default="4")
    parser.add_argument("--max-time", type=float, default=2.0)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    width_record, schedule_record = build_records(parse_widths(args.widths), args.plane_limit, args.max_time, args.workers)
    if args.write:
        WIDTH_OUTPUT.write_text(json.dumps(width_record, indent=2, sort_keys=True) + "\n")
        SCHEDULE_OUTPUT.write_text(json.dumps(schedule_record, indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": width_record["proof_status"],
        "widths_tested": width_record["width_ablation"]["widths_tested"],
        "best_min_support": width_record["width_ablation"]["best_min_support"],
        "best_total_incidence": width_record["width_ablation"]["best_total_incidence"],
        "guard_passing_candidates": width_record["width_ablation"]["guard_passing_candidates"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_RANK2_FULLMENU_ABLATION_READY")


if __name__ == "__main__":
    main()
