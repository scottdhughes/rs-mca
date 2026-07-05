#!/usr/bin/env python3
"""Adaptive ratio-column generation for rank-2 mu_8 carrier scheduling."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from itertools import combinations
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


SAGE_MENU_SCRIPT = Path("experimental/scripts/audit_m1_a327_mu8_rank2_cpsat_exact.sage")
MENU_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_menu.json")
ADAPTIVE_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_adaptive_ratio_columns.json")
SCHEDULE_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_adaptive_schedule_candidates.json")

TARGET = 327
REQUIRED_TOTAL = 7 * TARGET
PAIR_CAP = 255
SOURCE_COMMIT = "14684a5"
LABELS = list(range(7))
PAIRS = [(i, j) for i in range(7) for j in range(i + 1, 7)]
PAIR_INDEX = {pair: idx for idx, pair in enumerate(PAIRS)}
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def build_menu(plane_limit: int, ratio_limit: int) -> dict[str, Any]:
    subprocess.run(
        [
            "sage",
            str(SAGE_MENU_SCRIPT),
            "--build-menu-json",
            "--json",
            "--plane-limit",
            str(plane_limit),
            "--ratio-limit",
            str(ratio_limit),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return load_json(MENU_PATH)


def compact_menu(menu: dict[str, Any], ratio_limit: int) -> dict[str, Any]:
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": SOURCE_COMMIT,
        "menu": {
            "field": "GF(17^32)",
            "planes": len(menu["planes"]),
            "quotient_points": 64,
            "ratio_limit": ratio_limit,
            "stored_as": "compact_summary",
            "exact_menu_rebuild_required_for_interpolation": True,
        },
        "plane_ids": [plane["plane_id"] for plane in menu["planes"]],
        "proof_status": "CANDIDATE / MU8_RANK2_ADAPTIVE_RATIO_COLUMNS_READY / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def ratio_option_ids(qrow: dict[str, Any]) -> list[str]:
    return [option["option_id"] for option in qrow["options"] if option["kind"] == "RATIO"]


def nonratio_option_ids(qrow: dict[str, Any]) -> list[str]:
    return [option["option_id"] for option in qrow["options"] if option["kind"] != "RATIO"]


def active_counts(active_ids: dict[int, set[str]], plane: dict[str, Any]) -> dict[str, int]:
    counts = {}
    for qidx, qrow in enumerate(plane["quotient_points"]):
        counts[str(qidx)] = sum(
            1
            for option in qrow["options"]
            if option["kind"] == "RATIO" and option["option_id"] in active_ids[qidx]
        )
    return counts


def initial_active_ids(plane: dict[str, Any], start_width: int) -> dict[int, set[str]]:
    active: dict[int, set[str]] = {}
    for qidx, qrow in enumerate(plane["quotient_points"]):
        ids = set(nonratio_option_ids(qrow))
        ids.update(ratio_option_ids(qrow)[:start_width])
        active[qidx] = ids
    return active


def option_by_id(qrow: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {option["option_id"]: option for option in qrow["options"]}


def solve_active_plane(
    plane: dict[str, Any],
    active_ids: dict[int, set[str]],
    max_time: float,
    workers: int,
    candidate_id: str,
    store_choices: bool = False,
    hint_choices: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    model = cp_model.CpModel()
    z_vars = {}
    x_vars = {}
    options: dict[tuple[int, str], dict[str, Any]] = {}
    block_lookup = {}
    for qidx, qrow in enumerate(plane["quotient_points"]):
        q_options = [option for option in qrow["options"] if option["option_id"] in active_ids[qidx]]
        if not q_options:
            return {
                "candidate_id": candidate_id,
                "plane_id": plane["plane_id"],
                "solver_status": "NO_ACTIVE_OPTIONS",
                "support_pair_pass": False,
                "guard_pass": False,
            }
        z_for_q = []
        for option in q_options:
            z = model.NewBoolVar(f"z_{qidx}_{option['option_id']}")
            z_vars[(qidx, option["option_id"])] = z
            options[(qidx, option["option_id"])] = option
            z_for_q.append(z)
        model.Add(sum(z_for_q) == 1)
        for phase in range(8):
            x_for_phase = []
            for option in q_options:
                for block_idx, block in enumerate(option["phase_blocks"][phase]):
                    key = (qidx, option["option_id"], phase, block_idx)
                    x = model.NewBoolVar(f"x_{qidx}_{option['option_id']}_{phase}_{block_idx}")
                    x_vars[key] = x
                    block_lookup[key] = block
                    model.Add(x <= z_vars[(qidx, option["option_id"])])
                    x_for_phase.append(x)
            model.Add(sum(x_for_phase) == 1)

    supports = [
        sum(var for key, var in x_vars.items() if label in block_lookup[key])
        for label in LABELS
    ]
    pair_loads = []
    for left, right in PAIRS:
        expr = sum(
            var for key, var in x_vars.items()
            if left in block_lookup[key] and right in block_lookup[key]
        )
        model.Add(expr <= PAIR_CAP)
        pair_loads.append(expr)
    row_cost = sum(
        int(options[key]["row_cost"]) * z for key, z in z_vars.items()
    )
    if hint_choices:
        hint_by_qidx = {int(choice["qidx"]): choice for choice in hint_choices}
        for (qidx, option_id), z in z_vars.items():
            model.AddHint(z, 1 if hint_by_qidx.get(qidx, {}).get("option_id") == option_id else 0)
        for key, x in x_vars.items():
            qidx, option_id, phase, _block_idx = key
            choice = hint_by_qidx.get(qidx)
            value = 0
            if choice and choice.get("option_id") == option_id:
                selected_blocks = choice.get("selected_blocks_by_phase", [])
                if phase < len(selected_blocks) and block_lookup[key] == selected_blocks[phase]:
                    value = 1
            model.AddHint(x, value)
    min_support = model.NewIntVar(0, 512, "min_support")
    for expr in supports:
        model.Add(min_support <= expr)
    pair_max = model.NewIntVar(0, PAIR_CAP, "pair_max")
    for expr in pair_loads:
        model.Add(pair_max >= expr)
    total = sum(supports)
    # A lexicographic-scale objective: min support dominates total incidence,
    # then pair slack, then interpolation row cost.
    model.Maximize(10_000_000 * min_support + 10_000 * total - 100 * pair_max - row_cost)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {
            "candidate_id": candidate_id,
            "plane_id": plane["plane_id"],
            "solver_status": solver.StatusName(status),
            "support_pair_pass": False,
            "guard_pass": False,
        }

    support = [int(solver.Value(expr)) for expr in supports]
    pairs = [int(solver.Value(expr)) for expr in pair_loads]
    ratio_counts: dict[str, int] = {}
    chosen = []
    for qidx, qrow in enumerate(plane["quotient_points"]):
        chosen_option_id = next(
            option_id
            for option_id in active_ids[qidx]
            if (qidx, option_id) in z_vars and solver.Value(z_vars[(qidx, option_id)]) == 1
        )
        option = options[(qidx, chosen_option_id)]
        selected_blocks = []
        for phase in range(8):
            for block_idx, block in enumerate(option["phase_blocks"][phase]):
                key = (qidx, chosen_option_id, phase, block_idx)
                if key in x_vars and solver.Value(x_vars[key]) == 1:
                    selected_blocks.append(block)
                    break
        if option["kind"] == "RATIO":
            ratio_counts[option["ratio_key"]] = ratio_counts.get(option["ratio_key"], 0) + 1
        chosen.append(
            {
                "qidx": qidx,
                "option_id": chosen_option_id,
                "kind": option["kind"],
                "row_cost": option["row_cost"],
                "ratio_key": option.get("ratio_key"),
                "selected_blocks_by_phase": selected_blocks,
            }
        )

    support_pass = min(support) >= TARGET
    pair_pass = max(pairs) <= PAIR_CAP
    total_pass = sum(support) >= REQUIRED_TOTAL
    guard_pass = support_pass and pair_pass and total_pass
    near_front = pair_pass and min(support) >= 313 and sum(support) >= 2193
    row: dict[str, Any] = {
        "candidate_id": candidate_id,
        "plane_id": plane["plane_id"],
        "solver_status": solver.StatusName(status),
        "support_vector": support,
        "min_support": min(support),
        "selected_incidence_total": sum(support),
        "pair_count_max": max(pairs),
        "pair_counts": pairs,
        "row_cost": int(solver.Value(row_cost)),
        "support_pass": support_pass,
        "pair_cap_pass": pair_pass,
        "total_incidence_pass": total_pass,
        "support_pair_pass": guard_pass,
        "guard_pass": guard_pass,
        "near_front": near_front,
        "ratio_line_support_histogram": {
            str(size): sum(1 for value in ratio_counts.values() if value == size)
            for size in sorted(set(ratio_counts.values()))
        },
        "max_ratio_line_support": max(ratio_counts.values(), default=0),
        "active_ratio_counts_by_qidx": active_counts(active_ids, plane),
    }
    if store_choices or guard_pass or near_front:
        row["chosen_options"] = chosen
    else:
        row["chosen_options_stored"] = False
    return row


def repeat_bonus(ratio_key: str | None, selected_counts: dict[str, int]) -> float:
    if ratio_key is None:
        return 0.0
    count = selected_counts.get(ratio_key, 0)
    if 16 <= count < 24:
        return 3.0
    if 24 <= count < 31:
        return 6.0
    if count == 31:
        return 1.0
    if count >= 32:
        return -20.0
    return 0.0


def score_option(
    option: dict[str, Any],
    deficits: list[int],
    slacks: list[int],
    selected_ratio_counts: dict[str, int],
    lam: float,
    mu: float,
    eta: float,
    theta: float,
) -> float:
    total = 0.0
    for phase_blocks in option["phase_blocks"]:
        best = None
        for block in phase_blocks:
            support_gain = sum(deficits[label] for label in block)
            overload_penalty = 0.0
            slack_penalty = 0.0
            for left, right in combinations(block, 2):
                slack = slacks[PAIR_INDEX[(left, right)]]
                overload_penalty += max(0, -slack)
                slack_penalty += 1.0 / (1.0 + max(0, slack))
            value = support_gain - lam * overload_penalty - mu * slack_penalty
            if best is None or value > best:
                best = value
        total += 0.0 if best is None else best
    total -= eta * float(option.get("row_cost", 1))
    total += theta * repeat_bonus(option.get("ratio_key"), selected_ratio_counts)
    return total


def selected_ratio_counts(row: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for choice in row.get("chosen_options", []):
        if choice.get("kind") == "RATIO" and choice.get("ratio_key"):
            key = str(choice["ratio_key"])
            counts[key] = counts.get(key, 0) + 1
    return counts


def add_adaptive_options(
    plane: dict[str, Any],
    active_ids: dict[int, set[str]],
    row: dict[str, Any],
    per_q: int,
    global_limit: int,
    width_cap: int,
    lam: float,
    mu: float,
    eta: float,
    theta: float,
) -> int:
    deficits = [max(0, TARGET - value) for value in row.get("support_vector", [])]
    if not deficits:
        return 0
    slacks = [PAIR_CAP - value for value in row.get("pair_counts", [])]
    ratio_counts = selected_ratio_counts(row)
    scored: list[tuple[float, int, str]] = []
    additions: set[tuple[int, str]] = set()
    for qidx, qrow in enumerate(plane["quotient_points"]):
        active_ratio_count = sum(
            1
            for option in qrow["options"]
            if option["kind"] == "RATIO" and option["option_id"] in active_ids[qidx]
        )
        if active_ratio_count >= width_cap:
            continue
        q_scored = []
        for option in qrow["options"]:
            if option["kind"] != "RATIO" or option["option_id"] in active_ids[qidx]:
                continue
            score = score_option(option, deficits, slacks, ratio_counts, lam, mu, eta, theta)
            q_scored.append((score, qidx, option["option_id"]))
            scored.append((score, qidx, option["option_id"]))
        q_scored.sort(reverse=True)
        remaining = max(0, width_cap - active_ratio_count)
        for item in q_scored[: min(per_q, remaining)]:
            additions.add((item[1], item[2]))
    scored.sort(reverse=True)
    for score, qidx, option_id in scored[:global_limit]:
        qrow = plane["quotient_points"][qidx]
        active_ratio_count = sum(
            1
            for option in qrow["options"]
            if option["kind"] == "RATIO" and option["option_id"] in active_ids[qidx]
        )
        if active_ratio_count < width_cap:
            additions.add((qidx, option_id))
    added = 0
    for qidx, option_id in sorted(additions):
        if option_id not in active_ids[qidx]:
            active_ids[qidx].add(option_id)
            added += 1
    return added


def best_key(row: dict[str, Any]) -> tuple[int, int, int, int]:
    return (
        int(row.get("min_support", 0)),
        int(row.get("selected_incidence_total", 0)),
        -int(row.get("pair_count_max", 999)),
        -int(row.get("row_cost", 9999)),
    )


def width_cap_for_round(round_idx: int, caps: list[int], start_width: int) -> int:
    if not caps:
        return start_width
    return caps[min(round_idx, len(caps) - 1)]


def run_plane(
    plane: dict[str, Any],
    start_width: int,
    width_caps: list[int],
    rounds: int,
    max_time: float,
    workers: int,
    per_q: int,
    global_limit: int,
    lam: float,
    mu: float,
    eta: float,
    theta: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    active = initial_active_ids(plane, start_width)
    round_rows = []
    stored_candidates = []
    best = None
    stagnant_rounds = 0
    previous_best_total = 0
    hint_choices = None
    fallback_seed = None
    for round_idx in range(rounds + 1):
        cap = width_cap_for_round(round_idx, width_caps, start_width)
        if round_idx == 0 and start_width > 4:
            fallback_active = initial_active_ids(plane, 4)
            fallback_seed = solve_active_plane(
                plane=plane,
                active_ids=fallback_active,
                max_time=max(max_time, 2.0),
                workers=workers,
                candidate_id=f"{plane['plane_id']}_adaptive_seed_w04",
                store_choices=True,
            )
            if "chosen_options" in fallback_seed:
                hint_choices = fallback_seed["chosen_options"]
        candidate_id = f"{plane['plane_id']}_adaptive_r{round_idx:02d}_w{cap:02d}"
        row = solve_active_plane(
            plane=plane,
            active_ids=active,
            max_time=max_time,
            workers=workers,
            candidate_id=candidate_id,
            hint_choices=hint_choices,
        )
        if "support_vector" not in row and start_width > 4:
            fallback = fallback_seed
            if fallback is not None and "support_vector" in fallback:
                fallback["fallback_from_solver_status"] = row.get("solver_status")
                fallback["fallback_from_start_width"] = start_width
                row = fallback
        row["round"] = round_idx
        row["width_cap"] = cap
        row["status"] = (
            "MU8_RANK2_ADAPTIVE_SUPPORT_PAIR_PASS"
            if row.get("guard_pass")
            else "MU8_RANK2_ADAPTIVE_NEAR_FRONT_DIAGNOSTIC"
            if row.get("near_front")
            else "MU8_RANK2_ADAPTIVE_WIDTH_IMPROVES_SUPPORT"
            if row.get("min_support", 0) >= 313
            else "MU8_RANK2_FULLMENU_SUPPORT_PAIR_INFEASIBLE"
        )
        round_rows.append({k: v for k, v in row.items() if k != "chosen_options"})
        if row.get("guard_pass") or row.get("near_front"):
            stored_candidates.append(row)
        if best is None or best_key(row) > best_key(best):
            if best is not None:
                total_gain = int(row.get("selected_incidence_total", 0)) - previous_best_total
                stagnant_rounds = 0 if total_gain >= 16 or row.get("min_support", 0) > best.get("min_support", 0) else stagnant_rounds + 1
            best = row
            previous_best_total = int(row.get("selected_incidence_total", 0))
        elif best is not None:
            if row.get("min_support", 0) <= best.get("min_support", 0) and row.get("selected_incidence_total", 0) < best.get("selected_incidence_total", 0) + 16:
                stagnant_rounds += 1
        if row.get("guard_pass"):
            break
        if "chosen_options" in row:
            hint_choices = row["chosen_options"]
        if round_idx >= rounds:
            break
        added = add_adaptive_options(plane, active, row, per_q, global_limit, cap, lam, mu, eta, theta)
        round_rows[-1]["adaptive_options_added"] = added
        if added == 0 or stagnant_rounds >= 2:
            break
    best_row = best or {"plane_id": plane["plane_id"], "min_support": 0, "selected_incidence_total": 0}
    summary = {
        "plane_id": plane["plane_id"],
        "rounds_solved": len(round_rows),
        "best_candidate_id": best_row.get("candidate_id"),
        "best_min_support": best_row.get("min_support", 0),
        "best_total_incidence": best_row.get("selected_incidence_total", 0),
        "best_pair_count_max": best_row.get("pair_count_max"),
        "best_row_cost": best_row.get("row_cost"),
        "support_pair_pass": bool(best_row.get("guard_pass")),
        "near_front_seen": any(row.get("near_front") for row in round_rows),
        "best_status": best_row.get("status", "MU8_RANK2_FULLMENU_SUPPORT_PAIR_INFEASIBLE"),
        "rounds": round_rows,
    }
    return summary, stored_candidates


def run_adaptive(
    plane_limit: int,
    start_width: int,
    max_width: int,
    width_caps: list[int],
    rounds: int,
    max_time: float,
    workers: int,
    per_q: int,
    global_limit: int,
    lam: float,
    mu: float,
    eta: float,
    theta: float,
    store_limit: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    menu = build_menu(plane_limit, max_width)
    plane_summaries = []
    stored = []
    for plane in menu["planes"]:
        summary, candidates = run_plane(
            plane=plane,
            start_width=start_width,
            width_caps=width_caps,
            rounds=rounds,
            max_time=max_time,
            workers=workers,
            per_q=per_q,
            global_limit=global_limit,
            lam=lam,
            mu=mu,
            eta=eta,
            theta=theta,
        )
        plane_summaries.append(summary)
        stored.extend(candidates)
    stored.sort(key=best_key, reverse=True)
    unique_stored = []
    seen_candidates = set()
    for candidate in stored:
        key = candidate.get("candidate_id")
        if key in seen_candidates:
            continue
        seen_candidates.add(key)
        unique_stored.append(candidate)
    stored = unique_stored[:store_limit]
    best_min = max([row.get("best_min_support", 0) for row in plane_summaries], default=0)
    best_total = max([row.get("best_total_incidence", 0) for row in plane_summaries], default=0)
    guard_count = sum(1 for row in stored if row.get("guard_pass"))
    near_count = sum(1 for row in stored if row.get("near_front"))
    best_failure = (
        "MU8_RANK2_ADAPTIVE_SUPPORT_PAIR_PASS"
        if guard_count
        else "MU8_RANK2_ADAPTIVE_WIDTH_IMPROVES_SUPPORT"
        if best_min >= 313 or best_total >= 2193
        else "MU8_RANK2_FULLMENU_SUPPORT_PAIR_INFEASIBLE"
    )
    proof_status = (
        "CANDIDATE / MU8_RANK2_ADAPTIVE_SUPPORT_PAIR_PASS / PARTIAL / EXPERIMENTAL"
        if guard_count
        else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_ADAPTIVE_WIDTH_IMPROVES_SUPPORT / PARTIAL / EXPERIMENTAL"
        if best_failure == "MU8_RANK2_ADAPTIVE_WIDTH_IMPROVES_SUPPORT"
        else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_FULLMENU_SUPPORT_PAIR_INFEASIBLE / PARTIAL / EXPERIMENTAL"
    )
    adaptive_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": SOURCE_COMMIT,
        "adaptive_ratio_columns": {
            "planes_solved": len(plane_summaries),
            "start_width": start_width,
            "max_width": max_width,
            "width_caps": width_caps,
            "rounds_requested": rounds,
            "top_k_per_quotient": per_q,
            "top_global": global_limit,
            "near_front_candidates": near_count,
            "support_pair_candidates": guard_count,
            "best_min_support": best_min,
            "best_total_incidence": best_total,
            "best_failure_mode": best_failure,
            "score_model": "deficit_pairslack_repeatbonus",
            "cp_sat_objective": "lexicographic_scale_min_support_total_pairmax_rowcost",
        },
        "plane_summaries": plane_summaries,
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    schedule_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": SOURCE_COMMIT,
        "adaptive_schedule_candidates": {
            "stored_candidates": len(stored),
            "near_front_candidates": near_count,
            "support_pair_candidates": guard_count,
            "best_min_support": max([row.get("min_support", 0) for row in stored], default=best_min),
            "best_total_incidence": max([row.get("selected_incidence_total", 0) for row in stored], default=best_total),
            "menu_ratio_limit": max_width,
            "plane_limit": plane_limit,
            "best_failure_mode": best_failure,
        },
        "candidates": stored,
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    MENU_PATH.write_text(json.dumps(compact_menu(menu, max_width), indent=2, sort_keys=True) + "\n")
    return adaptive_record, schedule_record


def parse_caps(raw: str) -> list[int]:
    return [int(value) for value in raw.split(",") if value.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--plane-limit", type=int, default=64)
    parser.add_argument("--start-width", type=int, default=8)
    parser.add_argument("--max-width", type=int, default=32)
    parser.add_argument("--width-caps", default="12,16,24,32")
    parser.add_argument("--rounds", type=int, default=6)
    parser.add_argument("--max-time", type=float, default=1.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--top-k-per-q", type=int, default=2)
    parser.add_argument("--top-global", type=int, default=128)
    parser.add_argument("--lambda-penalty", type=float, default=100.0)
    parser.add_argument("--mu-penalty", type=float, default=8.0)
    parser.add_argument("--eta-rowcost", type=float, default=0.5)
    parser.add_argument("--theta-repeat", type=float, default=4.0)
    parser.add_argument("--store-limit", type=int, default=96)
    args = parser.parse_args()
    adaptive_record, schedule_record = run_adaptive(
        plane_limit=args.plane_limit,
        start_width=args.start_width,
        max_width=args.max_width,
        width_caps=parse_caps(args.width_caps),
        rounds=args.rounds,
        max_time=args.max_time,
        workers=args.workers,
        per_q=args.top_k_per_q,
        global_limit=args.top_global,
        lam=args.lambda_penalty,
        mu=args.mu_penalty,
        eta=args.eta_rowcost,
        theta=args.theta_repeat,
        store_limit=args.store_limit,
    )
    if args.write:
        write_json(ADAPTIVE_OUTPUT, adaptive_record)
        write_json(SCHEDULE_OUTPUT, schedule_record)
    summary = {
        "proof_status": adaptive_record["proof_status"],
        "best_min_support": adaptive_record["adaptive_ratio_columns"]["best_min_support"],
        "best_total_incidence": adaptive_record["adaptive_ratio_columns"]["best_total_incidence"],
        "near_front_candidates": adaptive_record["adaptive_ratio_columns"]["near_front_candidates"],
        "support_pair_candidates": adaptive_record["adaptive_ratio_columns"]["support_pair_candidates"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_RANK2_ADAPTIVE_RATIO_COLUMNS_READY")


if __name__ == "__main__":
    main()
