#!/usr/bin/env python3
"""Find support/pair-passing rank-3 mu_8 schedules with low row cost."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from ortools.sat.python import cp_model


TARGET = 327
REQUIRED_TOTAL = 7 * TARGET
PAIR_CAP = 255
SOURCE_COMMIT = "daca3df"
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

DEFAULT_INPUT = Path("experimental/data/m1_a327_mu8_rank3_projective_menu.json")
DEFAULT_OUTPUT = Path("experimental/data/m1_a327_mu8_rank3_projective_lowrow_schedule_candidates.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def load_core_avoidance(paths: list[Path] | None, mode: str) -> dict[str, set[tuple[int, str]]]:
    if not paths:
        return {}
    by_key: dict[str, set[tuple[int, str]]] = {}
    for path in paths:
        payload = load_json(path)
        for system in payload.get("systems", []):
            selected_core = None
            for core in system.get("pivot_cores", []):
                if core.get("mode") == mode:
                    selected_core = core
                    break
            if not selected_core:
                continue
            groups: set[tuple[int, str]] = set()
            for group_id in selected_core.get("core_group_ids", []):
                try:
                    qidx_raw, option_id = str(group_id).split(":", 1)
                except ValueError:
                    continue
                groups.add((int(qidx_raw), option_id))
            for key in (system.get("plane_id"), system.get("subspace_id"), system.get("candidate_id")):
                if key:
                    by_key.setdefault(str(key), set()).update(groups)
    return by_key


def load_core_nogoods(paths: list[Path] | None, mode: str) -> dict[str, list[set[tuple[int, str]]]]:
    if not paths:
        return {}
    by_key: dict[str, list[set[tuple[int, str]]]] = {}
    seen: dict[str, set[tuple[tuple[int, str], ...]]] = {}
    for path in paths:
        payload = load_json(path)
        for system in payload.get("systems", []):
            for core in system.get("pivot_cores", []):
                if core.get("mode") != mode:
                    continue
                groups: set[tuple[int, str]] = set()
                for group_id in core.get("core_group_ids", []):
                    try:
                        qidx_raw, option_id = str(group_id).split(":", 1)
                    except ValueError:
                        continue
                    groups.add((int(qidx_raw), option_id))
                if not groups:
                    continue
                signature = tuple(sorted(groups))
                for key in (system.get("plane_id"), system.get("subspace_id"), system.get("candidate_id")):
                    if not key:
                        continue
                    key_text = str(key)
                    if signature in seen.setdefault(key_text, set()):
                        continue
                    seen[key_text].add(signature)
                    by_key.setdefault(key_text, []).append(groups)
    return by_key


def solve_plane(
    plane: dict[str, Any],
    subspace: dict[str, Any],
    hint_row: dict[str, Any] | None,
    avoid_core_groups: set[tuple[int, str]],
    core_nogood_sets: list[set[tuple[int, str]]],
    max_time: float,
    workers: int,
    row_cost_cap: int | None,
    repeat_weight: int,
    row_cost_weight: int,
    generic_row_cost_weight: int,
    dependency_row_cost_weight: int,
    min_repeat_key_support: int,
    max_projective_key_count: int | None,
    min_projective_key_count: int | None,
    min_fixed_point_count: int | None,
    max_generic_row_cost: int | None,
    max_generic_point_row_cost: int | None,
    max_zero_row_cost: int | None,
    min_dependency_row_cost: int | None,
    fixed_point_weight: int,
    max_core_overlap: int | None,
    core_overlap_weight: int,
    store_choices: bool,
) -> dict[str, Any]:
    model = cp_model.CpModel()
    z_vars: dict[tuple[int, str], Any] = {}
    x_vars: dict[tuple[int, str, int, int], Any] = {}
    options: dict[tuple[int, str], dict[str, Any]] = {}
    blocks: dict[tuple[int, str, int, int], list[int]] = {}

    for qrow in plane.get("quotient_points", []):
        qidx = int(qrow["qidx"])
        z_for_q = []
        for option in qrow.get("options", []):
            option_id = str(option["option_id"])
            z = model.NewBoolVar(f"z_{qidx}_{option_id}")
            z_vars[(qidx, option_id)] = z
            options[(qidx, option_id)] = option
            z_for_q.append(z)
        if not z_for_q:
            return {"candidate_id": subspace["subspace_id"] + "_lowrow", "solver_status": "NO_OPTIONS"}
        model.Add(sum(z_for_q) == 1)
        for phase in range(8):
            x_for_phase = []
            for option in qrow.get("options", []):
                option_id = str(option["option_id"])
                for block_idx, raw_block in enumerate(option["phase_blocks"][phase]):
                    key = (qidx, option_id, phase, block_idx)
                    x = model.NewBoolVar(f"x_{qidx}_{option_id}_{phase}_{block_idx}")
                    x_vars[key] = x
                    blocks[key] = [int(label) for label in raw_block]
                    model.Add(x <= z_vars[(qidx, option_id)])
                    x_for_phase.append(x)
            if not x_for_phase:
                return {"candidate_id": subspace["subspace_id"] + "_lowrow", "solver_status": "NO_BLOCKS"}
            model.Add(sum(x_for_phase) == 1)

    if hint_row and hint_row.get("chosen_options"):
        hinted_options = {
            int(row["qidx"]): row
            for row in hint_row.get("chosen_options", [])
            if "qidx" in row and "option_id" in row
        }
        for (qidx, option_id), var in z_vars.items():
            hint = hinted_options.get(qidx)
            model.AddHint(var, 1 if hint and str(hint.get("option_id")) == option_id else 0)
        for qidx, hint in hinted_options.items():
            option_id = str(hint.get("option_id"))
            selected_blocks = hint.get("selected_blocks_by_phase", [])
            for phase, raw_block in enumerate(selected_blocks[:8]):
                wanted = [int(label) for label in raw_block]
                for key, var in x_vars.items():
                    if key[0] != qidx or key[1] != option_id or key[2] != phase:
                        continue
                    if blocks[key] == wanted:
                        model.AddHint(var, 1)
                        break

    supports = [
        sum(var for key, var in x_vars.items() if label in blocks[key])
        for label in LABELS
    ]
    pair_loads = []
    for left, right in PAIRS:
        expr = sum(var for key, var in x_vars.items() if left in blocks[key] and right in blocks[key])
        model.Add(expr <= PAIR_CAP)
        pair_loads.append(expr)
    total = sum(supports)
    row_cost = sum(int(options[key].get("row_cost", 0)) * z for key, z in z_vars.items())
    for support in supports:
        model.Add(support >= TARGET)
    model.Add(total >= REQUIRED_TOTAL)
    if row_cost_cap is not None:
        model.Add(row_cost <= int(row_cost_cap))
    projective_key_vars: dict[str, list[Any]] = {}
    for key, z in z_vars.items():
        option = options[key]
        if option.get("kind") == "POINT" and option.get("projective_key"):
            projective_key_vars.setdefault(str(option["projective_key"]), []).append(z)
    if max_projective_key_count is not None:
        for vars_for_key in projective_key_vars.values():
            model.Add(sum(vars_for_key) <= int(max_projective_key_count))
    max_key_count = model.NewIntVar(0, 64, "max_projective_key_count")
    if projective_key_vars:
        model.AddMaxEquality(max_key_count, [sum(vars_for_key) for vars_for_key in projective_key_vars.values()])
    else:
        model.Add(max_key_count == 0)
    if min_projective_key_count is not None:
        model.Add(max_key_count >= int(min_projective_key_count))
    repeat_eligible_keys = {
        key for key, vars_for_key in projective_key_vars.items()
        if len(vars_for_key) >= min_repeat_key_support
    }
    fixed_point_terms = [
        z
        for key, z in z_vars.items()
        if options[key].get("kind") == "POINT" and options[key].get("fixed_projective_point")
    ]
    fixed_point_score = sum(fixed_point_terms) if fixed_point_terms else 0
    if min_fixed_point_count is not None:
        model.Add(fixed_point_score >= int(min_fixed_point_count))
    dependency_row_cost = sum(
        int(option.get("row_cost", 0)) * z_vars[key]
        for key, option in options.items()
        if option.get("kind") == "POINT"
        and (
            option.get("fixed_projective_point")
            or str(option.get("projective_key")) in repeat_eligible_keys
        )
    )
    generic_point_row_cost = sum(
        int(option.get("row_cost", 0)) * z_vars[key]
        for key, option in options.items()
        if option.get("kind") == "POINT"
        and not (
            option.get("fixed_projective_point")
            or str(option.get("projective_key")) in repeat_eligible_keys
        )
    )
    zero_row_cost = sum(
        int(option.get("row_cost", 0)) * z_vars[key]
        for key, option in options.items()
        if option.get("kind") == "ZERO"
    )
    generic_row_cost = row_cost - dependency_row_cost
    if max_generic_row_cost is not None:
        model.Add(generic_row_cost <= int(max_generic_row_cost))
    if max_generic_point_row_cost is not None:
        model.Add(generic_point_row_cost <= int(max_generic_point_row_cost))
    if max_zero_row_cost is not None:
        model.Add(zero_row_cost <= int(max_zero_row_cost))
    if min_dependency_row_cost is not None:
        model.Add(dependency_row_cost >= int(min_dependency_row_cost))
    core_overlap_terms = [
        z
        for key, z in z_vars.items()
        if key in avoid_core_groups
    ]
    core_overlap = sum(core_overlap_terms) if core_overlap_terms else 0
    if max_core_overlap is not None:
        model.Add(core_overlap <= int(max_core_overlap))
    core_nogood_constraints = 0
    core_nogood_partial = 0
    for nogood_idx, nogood in enumerate(core_nogood_sets):
        vars_for_nogood = [
            z_vars[key]
            for key in sorted(nogood)
            if key in z_vars
        ]
        if len(vars_for_nogood) == len(nogood):
            model.Add(sum(vars_for_nogood) <= len(vars_for_nogood) - 1)
            core_nogood_constraints += 1
        elif vars_for_nogood:
            core_nogood_partial += 1
    repeat_terms = [
        z
        for vars_for_key in projective_key_vars.values()
        if len(vars_for_key) >= min_repeat_key_support
        for z in vars_for_key
    ]
    repeat_score = sum(repeat_terms) if repeat_terms else 0
    pair_max = model.NewIntVar(0, PAIR_CAP, "pair_max")
    for pair_load in pair_loads:
        model.Add(pair_max >= pair_load)
    surplus = total - REQUIRED_TOTAL
    model.Minimize(
        row_cost_weight * row_cost
        + generic_row_cost_weight * generic_row_cost
        + 1_000 * pair_max
        + core_overlap_weight * core_overlap
        - surplus
        - repeat_weight * repeat_score
        - fixed_point_weight * fixed_point_score
        - dependency_row_cost_weight * dependency_row_cost
    )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {
            "candidate_id": subspace["subspace_id"] + "_lowrow",
            "plane_id": plane["plane_id"],
            "subspace_id": subspace["subspace_id"],
            "solver_status": solver.StatusName(status),
            "support_pair_pass": False,
            "guard_pass": False,
            "row_cost_cap": row_cost_cap,
            "max_generic_row_cost": max_generic_row_cost,
            "max_generic_point_row_cost": max_generic_point_row_cost,
            "max_zero_row_cost": max_zero_row_cost,
            "min_dependency_row_cost": min_dependency_row_cost,
            "max_core_overlap": max_core_overlap,
            "core_overlap_weight": core_overlap_weight,
            "generic_row_cost_weight": generic_row_cost_weight,
            "dependency_row_cost_weight": dependency_row_cost_weight,
            "core_nogood_sets": len(core_nogood_sets),
            "core_nogood_constraints": core_nogood_constraints,
            "core_nogood_partial_matches": core_nogood_partial,
        }

    support_vector = [int(solver.Value(expr)) for expr in supports]
    pair_counts = [int(solver.Value(expr)) for expr in pair_loads]
    chosen = []
    option_kind_counts: Counter[str] = Counter()
    selected_projective_counts: Counter[str] = Counter()
    selected_fixed_point_counts: Counter[str] = Counter()
    for qrow in plane.get("quotient_points", []):
        qidx = int(qrow["qidx"])
        selected = None
        selected_id = None
        for option in qrow.get("options", []):
            option_id = str(option["option_id"])
            if solver.Value(z_vars[(qidx, option_id)]) == 1:
                selected = option
                selected_id = option_id
                break
        if selected is None or selected_id is None:
            continue
        option_kind_counts[str(selected.get("kind"))] += 1
        if selected.get("kind") == "POINT" and selected.get("projective_key"):
            selected_projective_counts[str(selected["projective_key"])] += 1
        if selected.get("kind") == "POINT" and selected.get("fixed_projective_point"):
            selected_fixed_point_counts[str(selected.get("fixed_point_id", "FIXED_UNKNOWN"))] += 1
        selected_blocks = []
        for phase in range(8):
            for key, var in x_vars.items():
                if key[0] == qidx and key[1] == selected_id and key[2] == phase and solver.Value(var) == 1:
                    selected_blocks.append(blocks[key])
                    break
        chosen.append(
            {
                "qidx": qidx,
                "option_id": selected_id,
                "kind": selected.get("kind"),
                "row_cost": int(selected.get("row_cost", 0)),
                "projective_key": selected.get("projective_key"),
                "ratio_key": selected.get("ratio_key"),
                "selected_blocks_by_phase": selected_blocks,
            }
        )

    row: dict[str, Any] = {
        "candidate_id": subspace["subspace_id"] + "_lowrow",
        "plane_id": plane["plane_id"],
        "subspace_id": subspace["subspace_id"],
        "solver_status": solver.StatusName(status),
        "support_vector": support_vector,
        "min_support": min(support_vector),
        "selected_incidence_total": sum(support_vector),
        "selected_incidence_gap": REQUIRED_TOTAL - sum(support_vector),
        "pair_counts": pair_counts,
        "pair_count_max": max(pair_counts),
        "row_cost": int(solver.Value(row_cost)),
        "dependency_row_cost": int(solver.Value(dependency_row_cost)),
        "generic_row_cost": int(solver.Value(generic_row_cost)),
        "generic_point_row_cost": int(solver.Value(generic_point_row_cost)),
        "zero_row_cost": int(solver.Value(zero_row_cost)),
        "core_overlap": int(solver.Value(core_overlap)) if core_overlap_terms else 0,
        "core_nogood_sets": len(core_nogood_sets),
        "core_nogood_constraints": core_nogood_constraints,
        "core_nogood_partial_matches": core_nogood_partial,
        "row_cost_cap": row_cost_cap,
        "max_generic_row_cost": max_generic_row_cost,
        "max_generic_point_row_cost": max_generic_point_row_cost,
        "max_zero_row_cost": max_zero_row_cost,
        "min_dependency_row_cost": min_dependency_row_cost,
        "max_core_overlap": max_core_overlap,
        "core_overlap_weight": core_overlap_weight,
        "generic_row_cost_weight": generic_row_cost_weight,
        "dependency_row_cost_weight": dependency_row_cost_weight,
        "support_pass": min(support_vector) >= TARGET,
        "pair_cap_pass": max(pair_counts) <= PAIR_CAP,
        "total_incidence_pass": sum(support_vector) >= REQUIRED_TOTAL,
        "support_pair_pass": True,
        "guard_pass": True,
        "near_front": True,
        "option_kind_counts": dict(option_kind_counts),
        "repeat_score": int(solver.Value(repeat_score)) if repeat_terms else 0,
        "fixed_point_score": int(solver.Value(fixed_point_score)) if fixed_point_terms else 0,
        "selected_projective_key_histogram": {
            str(size): sum(1 for value in selected_projective_counts.values() if value == size)
            for size in sorted(set(selected_projective_counts.values()))
        },
        "selected_fixed_point_histogram": {
            str(size): sum(1 for value in selected_fixed_point_counts.values() if value == size)
            for size in sorted(set(selected_fixed_point_counts.values()))
        },
        "selected_fixed_point_ids": sorted(selected_fixed_point_counts),
        "max_selected_projective_key_support": max(selected_projective_counts.values(), default=0),
        "max_selected_fixed_point_support": max(selected_fixed_point_counts.values(), default=0),
    }
    if store_choices:
        row["chosen_options"] = chosen
    return row


def load_hints(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    payload = load_json(path)
    hints = {}
    rows = list(payload.get("candidates", []))
    for cap_result in payload.get("cap_results", []):
        best = cap_result.get("best")
        if best:
            rows.append(best)
        rows.extend(cap_result.get("candidates", []))
    for row in rows:
        if not row.get("chosen_options"):
            continue
        subspace_id = row.get("subspace_id")
        plane_id = row.get("plane_id")
        candidate_id = row.get("candidate_id")
        for key in (subspace_id, plane_id, candidate_id):
            if key:
                hints[str(key)] = row
    return hints


def build_record(args: argparse.Namespace) -> dict[str, Any]:
    menu = load_json(args.input)
    hints = load_hints(args.hint_schedule)
    core_avoidance = load_core_avoidance(args.avoid_core_file, args.avoid_core_mode)
    core_nogoods = load_core_nogoods(args.avoid_core_file, args.avoid_core_mode) if args.forbid_core_subsets else {}
    wanted_subspaces = set(args.subspace_id or [])
    rows = []
    subspaces = []
    for subspace in menu.get("subspaces", []):
        if wanted_subspaces:
            keys = {
                str(subspace.get("subspace_id")),
                str(subspace.get("plane", {}).get("plane_id")),
            }
            if not (keys & wanted_subspaces):
                continue
        subspaces.append(subspace)
    for subspace in subspaces[: args.subspace_limit]:
        hint_row = hints.get(str(subspace.get("subspace_id"))) or hints.get(str(subspace.get("plane", {}).get("plane_id")))
        avoid_core_groups = (
            core_avoidance.get(str(subspace.get("subspace_id")))
            or core_avoidance.get(str(subspace.get("plane", {}).get("plane_id")))
            or set()
        )
        core_nogood_sets = (
            core_nogoods.get(str(subspace.get("subspace_id")))
            or core_nogoods.get(str(subspace.get("plane", {}).get("plane_id")))
            or []
        )
        row = solve_plane(
            subspace["plane"],
            subspace,
            hint_row,
            avoid_core_groups,
            core_nogood_sets,
            max_time=args.max_time,
            workers=args.workers,
            row_cost_cap=args.row_cost_cap,
            repeat_weight=args.repeat_weight,
            row_cost_weight=args.row_cost_weight,
            generic_row_cost_weight=args.generic_row_cost_weight,
            dependency_row_cost_weight=args.dependency_row_cost_weight,
            min_repeat_key_support=args.min_repeat_key_support,
            max_projective_key_count=args.max_projective_key_count,
            min_projective_key_count=args.min_projective_key_count,
            min_fixed_point_count=args.min_fixed_point_count,
            max_generic_row_cost=args.max_generic_row_cost,
            max_generic_point_row_cost=args.max_generic_point_row_cost,
            max_zero_row_cost=args.max_zero_row_cost,
            min_dependency_row_cost=args.min_dependency_row_cost,
            fixed_point_weight=args.fixed_point_weight,
            max_core_overlap=args.max_core_overlap,
            core_overlap_weight=args.core_overlap_weight,
            store_choices=args.store_choices,
        )
        rows.append(row)
    rows.sort(
        key=lambda row: (
            row.get("support_pair_pass", False),
            -int(row.get("generic_row_cost", 99999)),
            -int(row.get("row_cost", 99999)),
            int(row.get("min_support", 0)),
            int(row.get("selected_incidence_total", 0)),
        ),
        reverse=True,
    )
    support_pair = [row for row in rows if row.get("support_pair_pass")]
    best = support_pair[0] if support_pair else (rows[0] if rows else {})
    status = (
        "CANDIDATE / MU8_RANK3_LOWROW_SUPPORT_PAIR_PASS / PARTIAL / EXPERIMENTAL"
        if support_pair
        else "EXACT_EXTRACTION_NO_A327 / MU8_RANK3_LOWROW_NO_SUPPORT_PAIR_PASS / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": SOURCE_COMMIT,
        "rank3_lowrow_schedule": {
            "strategy": "support_pair_pass_minimize_projective_interpolation_row_cost",
            "input": str(args.input),
            "hint_schedule": str(args.hint_schedule) if args.hint_schedule else None,
            "subspaces_solved": len(rows),
            "support_pair_candidates": len(support_pair),
            "best_row_cost": best.get("row_cost"),
            "best_dependency_row_cost": best.get("dependency_row_cost"),
            "best_generic_row_cost": best.get("generic_row_cost"),
            "best_generic_point_row_cost": best.get("generic_point_row_cost"),
            "best_zero_row_cost": best.get("zero_row_cost"),
            "best_core_overlap": best.get("core_overlap"),
            "max_generic_row_cost": args.max_generic_row_cost,
            "max_generic_point_row_cost": args.max_generic_point_row_cost,
            "max_zero_row_cost": args.max_zero_row_cost,
            "min_dependency_row_cost": args.min_dependency_row_cost,
            "max_core_overlap": args.max_core_overlap,
            "avoid_core_files": [str(path) for path in args.avoid_core_file] if args.avoid_core_file else [],
            "avoid_core_mode": args.avoid_core_mode,
            "generic_row_cost_weight": args.generic_row_cost_weight,
            "core_overlap_weight": args.core_overlap_weight,
            "dependency_row_cost_weight": args.dependency_row_cost_weight,
            "forbid_core_subsets": args.forbid_core_subsets,
            "best_core_nogood_sets": best.get("core_nogood_sets"),
            "best_core_nogood_constraints": best.get("core_nogood_constraints"),
            "best_core_nogood_partial_matches": best.get("core_nogood_partial_matches"),
            "best_min_support": best.get("min_support"),
            "best_total_incidence": best.get("selected_incidence_total"),
            "best_pair_count_max": best.get("pair_count_max"),
            "best_repeat_score": best.get("repeat_score"),
            "best_fixed_point_score": best.get("fixed_point_score"),
            "best_max_selected_projective_key_support": best.get("max_selected_projective_key_support"),
            "best_max_selected_fixed_point_support": best.get("max_selected_fixed_point_support"),
            "best_failure_mode": (
                "MU8_RANK3_LOWROW_SUPPORT_PAIR_PASS"
                if support_pair
                else "MU8_RANK3_LOWROW_NO_SUPPORT_PAIR_PASS"
            ),
        },
        "candidates": rows[: args.store_limit],
        "proof_status": status,
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--hint-schedule", type=Path)
    parser.add_argument("--subspace-id", action="append")
    parser.add_argument("--subspace-limit", type=int, default=6)
    parser.add_argument("--max-time", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--row-cost-cap", type=int)
    parser.add_argument("--repeat-weight", type=int, default=0)
    parser.add_argument("--row-cost-weight", type=int, default=1_000_000)
    parser.add_argument("--generic-row-cost-weight", type=int, default=0)
    parser.add_argument("--dependency-row-cost-weight", type=int, default=0)
    parser.add_argument("--min-repeat-key-support", type=int, default=2)
    parser.add_argument("--max-projective-key-count", type=int)
    parser.add_argument("--min-projective-key-count", type=int)
    parser.add_argument("--min-fixed-point-count", type=int)
    parser.add_argument("--max-generic-row-cost", type=int)
    parser.add_argument("--max-generic-point-row-cost", type=int)
    parser.add_argument("--max-zero-row-cost", type=int)
    parser.add_argument("--min-dependency-row-cost", type=int)
    parser.add_argument("--fixed-point-weight", type=int, default=0)
    parser.add_argument("--avoid-core-file", type=Path, action="append")
    parser.add_argument("--avoid-core-mode", default="dependency_last")
    parser.add_argument("--max-core-overlap", type=int)
    parser.add_argument("--forbid-core-subsets", action="store_true")
    parser.add_argument("--core-overlap-weight", type=int, default=0)
    parser.add_argument("--store-choices", action="store_true")
    parser.add_argument("--store-limit", type=int, default=12)
    args = parser.parse_args()
    record = build_record(args)
    if args.write:
        write_json(args.output, record)
    summary = {
        "proof_status": record["proof_status"],
        "subspaces_solved": record["rank3_lowrow_schedule"]["subspaces_solved"],
        "support_pair_candidates": record["rank3_lowrow_schedule"]["support_pair_candidates"],
        "best_row_cost": record["rank3_lowrow_schedule"]["best_row_cost"],
        "best_dependency_row_cost": record["rank3_lowrow_schedule"].get("best_dependency_row_cost"),
        "best_generic_row_cost": record["rank3_lowrow_schedule"].get("best_generic_row_cost"),
        "best_generic_point_row_cost": record["rank3_lowrow_schedule"].get("best_generic_point_row_cost"),
        "best_zero_row_cost": record["rank3_lowrow_schedule"].get("best_zero_row_cost"),
        "best_core_overlap": record["rank3_lowrow_schedule"].get("best_core_overlap"),
        "max_generic_row_cost": record["rank3_lowrow_schedule"].get("max_generic_row_cost"),
        "max_generic_point_row_cost": record["rank3_lowrow_schedule"].get("max_generic_point_row_cost"),
        "max_zero_row_cost": record["rank3_lowrow_schedule"].get("max_zero_row_cost"),
        "min_dependency_row_cost": record["rank3_lowrow_schedule"].get("min_dependency_row_cost"),
        "max_core_overlap": record["rank3_lowrow_schedule"].get("max_core_overlap"),
        "generic_row_cost_weight": record["rank3_lowrow_schedule"].get("generic_row_cost_weight"),
        "core_overlap_weight": record["rank3_lowrow_schedule"].get("core_overlap_weight"),
        "dependency_row_cost_weight": record["rank3_lowrow_schedule"].get("dependency_row_cost_weight"),
        "forbid_core_subsets": record["rank3_lowrow_schedule"].get("forbid_core_subsets"),
        "best_core_nogood_sets": record["rank3_lowrow_schedule"].get("best_core_nogood_sets"),
        "best_core_nogood_constraints": record["rank3_lowrow_schedule"].get("best_core_nogood_constraints"),
        "best_core_nogood_partial_matches": record["rank3_lowrow_schedule"].get("best_core_nogood_partial_matches"),
        "best_min_support": record["rank3_lowrow_schedule"]["best_min_support"],
        "best_total_incidence": record["rank3_lowrow_schedule"]["best_total_incidence"],
        "best_pair_count_max": record["rank3_lowrow_schedule"]["best_pair_count_max"],
        "best_repeat_score": record["rank3_lowrow_schedule"].get("best_repeat_score"),
        "best_fixed_point_score": record["rank3_lowrow_schedule"].get("best_fixed_point_score"),
        "best_max_selected_projective_key_support": record["rank3_lowrow_schedule"].get("best_max_selected_projective_key_support"),
        "best_max_selected_fixed_point_support": record["rank3_lowrow_schedule"].get("best_max_selected_fixed_point_support"),
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_RANK3_PROJECTIVE_LOWROW_READY")


if __name__ == "__main__":
    main()
