#!/usr/bin/env python3
"""Rank-feedback multiscale quotient search for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "a1f304c"
PREVIOUS_DATA = Path("experimental/data/m1_a327_multiscale_block_count_quotient_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_multiscale_rank_feedback_quotient_search.json")
MULTISCALE_SCRIPT = Path("experimental/scripts/scan_m1_a327_multiscale_block_count_quotient_search.py")

TRACK = "INTERLEAVED_LIST"
ROW = "RS[F_17^32,H,256]"
DENOMINATOR = "17^32"
TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
PAIR_CAP = 255
PAIR7_LOWER = 142
WITNESSES = tuple(range(1, 8))
GUARDED_TO_7 = tuple(range(1, 6))
BASELINE = 7
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track rank-feedback quotient search",
    "global obstruction outside the tested rank-feedback quotient schedules",
]


def load_multiscale_module() -> Any:
    spec = importlib.util.spec_from_file_location("m1_a327_multiscale", MULTISCALE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {MULTISCALE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MS = load_multiscale_module()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def build_full_model(
    quotient_order: int,
    block_sizes: tuple[int, ...],
    seed: int,
    equation_cap: int | None = None,
) -> dict[str, Any]:
    cp_model, ortools_version = MS.require_ortools()
    bucket_size = DOMAIN_SIZE // quotient_order
    degree_bound = MS.quotient_degree_bound(quotient_order)
    blocks = MS.block_family(block_sizes)
    model = cp_model.CpModel()
    active: list[list[Any]] = []
    selected: list[list[Any]] = []

    for bucket in range(quotient_order):
        active_row = []
        selected_row = []
        for bidx, block in enumerate(blocks):
            on = model.NewBoolVar(f"active_q{bucket}_b{bidx}")
            count = model.NewIntVar(0, bucket_size, f"count_q{bucket}_b{bidx}")
            model.Add(count <= bucket_size * on)
            model.Add(count >= on)
            active_row.append(on)
            selected_row.append(count)
        model.Add(sum(selected_row) == bucket_size)
        for witness in WITNESSES:
            model.Add(sum(active_row[bidx] for bidx, block in enumerate(blocks) if witness in block) <= 1)
        active.append(active_row)
        selected.append(selected_row)

    for witness in WITNESSES:
        model.Add(
            sum(
                selected[bucket][bidx]
                for bucket in range(quotient_order)
                for bidx, block in enumerate(blocks)
                if witness in block
            )
            == TARGET_AGREEMENT
        )

    pair_selected = {}
    pair_ambient = {}
    for left, right in pairs():
        selected_var = model.NewIntVar(0, DOMAIN_SIZE, f"selected_pair_{left}_{right}")
        ambient_var = model.NewIntVar(0, quotient_order, f"ambient_pair_{left}_{right}")
        model.Add(
            selected_var
            == sum(
                selected[bucket][bidx]
                for bucket in range(quotient_order)
                for bidx, block in enumerate(blocks)
                if left in block and right in block
            )
        )
        model.Add(
            ambient_var
            == sum(
                active[bucket][bidx]
                for bucket in range(quotient_order)
                for bidx, block in enumerate(blocks)
                if left in block and right in block
            )
        )
        model.Add(selected_var <= PAIR_CAP)
        if right == BASELINE and left in GUARDED_TO_7:
            model.Add(selected_var >= PAIR7_LOWER)
        model.Add(ambient_var <= degree_bound)
        pair_selected[(left, right)] = selected_var
        pair_ambient[(left, right)] = ambient_var

    equation_count = model.NewIntVar(0, quotient_order * 6, "equation_count")
    model.Add(
        equation_count
        == sum(
            (len(block) - 1) * active[bucket][bidx]
            for bucket in range(quotient_order)
            for bidx, block in enumerate(blocks)
        )
    )
    if equation_cap is not None:
        model.Add(equation_count <= equation_cap)

    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for witness in GUARDED_TO_7:
        model.Add(min_pair7 <= pair_selected[(witness, BASELINE)])
    max_selected_pair = model.NewIntVar(0, DOMAIN_SIZE, "max_selected_pair")
    max_ambient_pair = model.NewIntVar(0, quotient_order, "max_ambient_pair")
    for pair in pairs():
        model.Add(max_selected_pair >= pair_selected[pair])
        model.Add(max_ambient_pair >= pair_ambient[pair])
    model.Minimize(100000 * equation_count + 1000 * max_ambient_pair + max_selected_pair - min_pair7)
    return {
        "cp_model": cp_model,
        "ortools_version": ortools_version,
        "model": model,
        "active": active,
        "selected": selected,
        "blocks": blocks,
        "equation_count": equation_count,
        "pair_selected": pair_selected,
        "pair_ambient": pair_ambient,
        "max_selected_pair": max_selected_pair,
        "max_ambient_pair": max_ambient_pair,
        "min_pair7": min_pair7,
        "bucket_size": bucket_size,
        "degree_bound": degree_bound,
        "seed": seed,
    }


def extract_schedule(
    built: dict[str, Any],
    solver: Any,
    quotient_order: int,
    block_sizes: tuple[int, ...],
    time_limit: float,
) -> dict[str, Any]:
    blocks = built["blocks"]
    active = built["active"]
    selected = built["selected"]
    selected_block_counts = []
    selected_partitions = []
    active_signature: list[list[int]] = []
    for bucket in range(quotient_order):
        bucket_active = [
            bidx for bidx, _block in enumerate(blocks) if int(solver.Value(active[bucket][bidx])) > 0
        ]
        active_signature.append(bucket_active)
        bucket_blocks = [blocks[bidx] for bidx in bucket_active]
        covered = {witness for block in bucket_blocks for witness in block}
        partition = [list(block) for block in bucket_blocks]
        partition.extend([witness] for witness in WITNESSES if witness not in covered)
        selected_partitions.append(sorted(partition, key=lambda block: (block[0], len(block), block)))
        selected_block_counts.append(
            [
                {"block": list(blocks[bidx]), "count": int(solver.Value(selected[bucket][bidx]))}
                for bidx in bucket_active
            ]
        )
    selected_pair_counts = {
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in built["pair_selected"].items()
    }
    ambient_pair_bucket_counts = {
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in built["pair_ambient"].items()
    }
    return {
        "quotient_order": quotient_order,
        "bucket_size": built["bucket_size"],
        "degree_bound": built["degree_bound"],
        "mode": "rank_feedback",
        "ortools_version": built["ortools_version"],
        "cp_sat_status": "FEASIBLE",
        "feasible": True,
        "time_limit_seconds": time_limit,
        "block_sizes": list(block_sizes),
        "block_count": len(blocks),
        "equation_count": int(solver.Value(built["equation_count"])),
        "support_vector": [
            sum(
                entry["count"]
                for bucket_entries in selected_block_counts
                for entry in bucket_entries
                if witness in entry["block"]
            )
            for witness in WITNESSES
        ],
        "pair7_counts": [selected_pair_counts[f"{idx}7"] for idx in GUARDED_TO_7],
        "selected_pair_counts": selected_pair_counts,
        "ambient_pair_bucket_counts": ambient_pair_bucket_counts,
        "max_selected_pair_count": max(selected_pair_counts.values()),
        "max_ambient_pair_buckets": max(ambient_pair_bucket_counts.values()),
        "selected_partitions": selected_partitions,
        "selected_block_counts": selected_block_counts,
        "active_signature": active_signature,
        "best_failure_mode": "RANK_FEEDBACK_SCHEDULE_FEASIBLE",
    }


def add_no_good_cut(built: dict[str, Any], active_signature: list[list[int]]) -> None:
    active = built["active"]
    blocks = built["blocks"]
    model = built["model"]
    literals = []
    for bucket, active_indices in enumerate(active_signature):
        active_set = set(active_indices)
        for bidx in range(len(blocks)):
            variable = active[bucket][bidx]
            literals.append(variable if bidx in active_set else 1 - variable)
    model.Add(sum(literals) <= len(literals) - 1)


def solve_structural_defect(
    quotient_order: int,
    block_sizes: tuple[int, ...],
    time_limit: float,
    seed: int,
) -> dict[str, Any]:
    ncols = 6 * (MS.quotient_degree_bound(quotient_order) + 1)
    built = build_full_model(quotient_order, block_sizes, seed, equation_cap=ncols - 1)
    solver = built["cp_model"].CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed
    status = solver.Solve(built["model"])
    status_name = solver.StatusName(status)
    feasible = status in (built["cp_model"].OPTIMAL, built["cp_model"].FEASIBLE)
    row = {
        "quotient_order": quotient_order,
        "equation_cap": ncols - 1,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "best_failure_mode": "RANK_FEEDBACK_STRUCTURAL_DEFECT_FEASIBLE"
        if feasible
        else "RANK_FEEDBACK_STRUCTURAL_DEFECT_INFEASIBLE"
        if status_name in {"INFEASIBLE", "MODEL_INVALID"}
        else "RANK_FEEDBACK_STRUCTURAL_DEFECT_UNRESOLVED",
    }
    if feasible:
        schedule = extract_schedule(built, solver, quotient_order, block_sizes, time_limit)
        audit = MS.audit_schedule(schedule)
        row.update({"schedule": schedule, "interpolation_audit": audit})
    return row


def rank_feedback_order(
    quotient_order: int,
    block_sizes: tuple[int, ...],
    samples: int,
    time_limit: float,
    seed: int,
) -> dict[str, Any]:
    built = build_full_model(quotient_order, block_sizes, seed)
    solver = built["cp_model"].CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed
    schedules = []
    best: dict[str, Any] | None = None
    positive_nullity = 0
    for sample_index in range(samples):
        status = solver.Solve(built["model"])
        status_name = solver.StatusName(status)
        if status not in (built["cp_model"].OPTIMAL, built["cp_model"].FEASIBLE):
            schedules.append(
                {
                    "sample_index": sample_index,
                    "cp_sat_status": status_name,
                    "feasible": False,
                    "best_failure_mode": "RANK_FEEDBACK_CP_EXHAUSTED"
                    if status_name in {"INFEASIBLE", "MODEL_INVALID"}
                    else "RANK_FEEDBACK_CP_UNRESOLVED",
                }
            )
            break
        schedule = extract_schedule(built, solver, quotient_order, block_sizes, time_limit)
        audit = MS.audit_schedule(schedule)
        row = {"sample_index": sample_index, "schedule": schedule, "interpolation_audit": audit}
        schedules.append(row)
        if audit["nullity"] and audit["nullity"] > 0:
            positive_nullity += 1
        if best is None or (
            (audit["candidate_constructed"], audit["nullity"] or -1, -(audit["rank"] or 9999), -schedule["equation_count"])
            > (
                best["interpolation_audit"]["candidate_constructed"],
                best["interpolation_audit"]["nullity"] or -1,
                -(best["interpolation_audit"]["rank"] or 9999),
                -best["schedule"]["equation_count"],
            )
        ):
            best = row
        add_no_good_cut(built, schedule["active_signature"])
        if audit["candidate_constructed"]:
            break
    if best is None:
        best_failure = schedules[-1]["best_failure_mode"] if schedules else "RANK_FEEDBACK_NO_SCHEDULE"
    elif best["interpolation_audit"]["candidate_constructed"]:
        best_failure = "RANK_FEEDBACK_EXACT_CANDIDATE"
    elif positive_nullity:
        best_failure = "RANK_FEEDBACK_POSITIVE_NULLITY_NO_CANDIDATE"
    else:
        best_failure = "RANK_FEEDBACK_FULL_RANK_FRONT"
    return {
        "quotient_order": quotient_order,
        "bucket_size": DOMAIN_SIZE // quotient_order,
        "degree_bound": MS.quotient_degree_bound(quotient_order),
        "field": MS.quotient_field(quotient_order).name,
        "samples_requested": samples,
        "samples_tested": sum(1 for row in schedules if "interpolation_audit" in row),
        "positive_nullity_schedules": positive_nullity,
        "candidate_constructed": bool(best and best["interpolation_audit"]["candidate_constructed"]),
        "best_rank": None if best is None else best["interpolation_audit"]["rank"],
        "best_nullity": None if best is None else best["interpolation_audit"]["nullity"],
        "best_matrix_shape": None if best is None else best["interpolation_audit"]["matrix_shape"],
        "best_equation_count": None if best is None else best["schedule"]["equation_count"],
        "best_failure_mode": best_failure,
        "structural_defect_screen": solve_structural_defect(quotient_order, block_sizes, time_limit, seed + 1000),
        "samples": schedules,
    }


def build_record(
    orders: list[int],
    samples: int,
    time_limit: float,
    block_sizes: tuple[int, ...],
    seed: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    results = [
        rank_feedback_order(order, block_sizes, samples, time_limit, seed + idx * 100)
        for idx, order in enumerate(orders)
    ]
    candidate_orders = [result["quotient_order"] for result in results if result["candidate_constructed"]]
    positive_orders = [result["quotient_order"] for result in results if result["positive_nullity_schedules"] > 0]
    if candidate_orders:
        proof_status = "CANDIDATE / RANK_FEEDBACK_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        best_failure = "RANK_FEEDBACK_EXACT_CANDIDATE"
    elif positive_orders:
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_POSITIVE_NULLITY_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
        best_failure = "RANK_FEEDBACK_POSITIVE_NULLITY_NO_CANDIDATE"
    elif all(result["best_failure_mode"] == "RANK_FEEDBACK_FULL_RANK_FRONT" for result in results):
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_FULL_RANK_FRONT / PARTIAL / EXPERIMENTAL"
        best_failure = "RANK_FEEDBACK_FULL_RANK_FRONT"
    else:
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_CP_UNRESOLVED / PARTIAL / EXPERIMENTAL"
        best_failure = "RANK_FEEDBACK_CP_UNRESOLVED"
    return {
        "track": TRACK,
        "row": ROW,
        "denominator": DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_multiscale": {
            "proof_status": previous["proof_status"],
            "orders_tested": previous["multiscale_search"]["orders_tested"],
            "candidate_orders": previous["multiscale_search"]["candidate_orders"],
            "best_failure_mode": previous["multiscale_search"]["best_failure_mode"],
        },
        "rank_feedback_search": {
            "orders_tested": orders,
            "block_sizes": list(block_sizes),
            "samples_per_order": samples,
            "time_limit_seconds_per_solve": time_limit,
            "total_samples_tested": sum(result["samples_tested"] for result in results),
            "positive_nullity_orders": positive_orders,
            "candidate_orders": candidate_orders,
            "best_failure_mode": best_failure,
        },
        "results": results,
        "candidate": {
            "constructed": bool(candidate_orders),
            "orders": candidate_orders,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": REQUIRED_NONCLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--orders", type=int, nargs="+", default=[16, 32])
    parser.add_argument("--samples-per-order", type=int, default=8)
    parser.add_argument("--time-limit", type=float, default=15.0)
    parser.add_argument("--block-sizes", type=int, nargs="+", default=[1, 2, 3, 4, 5, 6, 7])
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    record = build_record(args.orders, args.samples_per_order, args.time_limit, tuple(args.block_sizes), args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {"proof_status": record["proof_status"], **record["rank_feedback_search"]}
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MULTISCALE_RANK_FEEDBACK_QUOTIENT_SEARCH_READY")


if __name__ == "__main__":
    main()
