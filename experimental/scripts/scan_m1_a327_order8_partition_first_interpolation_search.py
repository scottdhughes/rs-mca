#!/usr/bin/env python3
"""Partition-first order-8 degree-3 interpolation search for M1 a=327."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "bcb9ac5"
PREVIOUS_DATA = Path("experimental/data/m1_a327_order8_degree3_partition_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_order8_partition_first_interpolation_search.json")

TRACK = "INTERLEAVED_LIST"
ROW = "RS[F_17^32,H,256]"
DENOMINATOR = "17^32"
TARGET_AGREEMENT = 327
FIELD_PRIME = 17
DOMAIN_SIZE = 512
ORDER8_LENGTH = 8
BUCKET_SIZE = 64
PAIR_CAP = 255
PAIR7_LOWER = 142
DEGREE_BOUND_Q = 3
VARIABLE_COUNT = 6 * (DEGREE_BOUND_Q + 1)
WITNESSES = tuple(range(1, 8))
NONBASELINE = tuple(range(1, 7))
BASELINE = 7
GUARDED_TO_7 = tuple(range(1, 6))
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track partition-first quotient construction",
    "global obstruction outside the tested order-8 partition-first interpolation search",
]


def require_ortools() -> tuple[Any, str]:
    try:
        from ortools.sat.python import cp_model  # type: ignore
        import ortools  # type: ignore

        return cp_model, str(ortools.__version__)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "OR-Tools is required. Run with "
            "/Users/scott/.venvs/rs-mca-ortools/bin/python "
            "experimental/scripts/scan_m1_a327_order8_partition_first_interpolation_search.py"
        ) from exc


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def canonical_partition(blocks: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((tuple(sorted(block)) for block in blocks), key=lambda block: (block[0], len(block), block)))


def set_partitions(items: tuple[int, ...]) -> list[tuple[tuple[int, ...], ...]]:
    if not items:
        return [tuple()]
    first, rest = items[0], items[1:]
    out: set[tuple[tuple[int, ...], ...]] = set()
    for partition in set_partitions(rest):
        out.add(canonical_partition([(first,), *partition]))
        for idx, block in enumerate(partition):
            new_blocks = list(partition)
            new_blocks[idx] = tuple(sorted((first, *block)))
            out.add(canonical_partition(new_blocks))
    return sorted(out, key=lambda part: (sum(len(block) - 1 for block in part), len(part), part))


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def partition_pair_same(partition: tuple[tuple[int, ...], ...], pair: tuple[int, int]) -> bool:
    return any(pair[0] in block and pair[1] in block for block in partition)


def equation_cost(partition: tuple[tuple[int, ...], ...]) -> int:
    return sum(len(block) - 1 for block in partition)


def order_mod(value: int, prime: int) -> int:
    current = value % prime
    order = 1
    while current != 1:
        current = (current * value) % prime
        order += 1
    return order


def order8_domain() -> list[int]:
    generator = next(value for value in range(2, FIELD_PRIME) if order_mod(value, FIELD_PRIME) == ORDER8_LENGTH)
    return [pow(generator, idx, FIELD_PRIME) for idx in range(ORDER8_LENGTH)]


def variable_index(witness: int, degree: int) -> int | None:
    if witness == BASELINE:
        return None
    return (witness - 1) * (DEGREE_BOUND_Q + 1) + degree


def equality_row(left: int, right: int, point: int) -> list[int]:
    row = [0] * VARIABLE_COUNT
    powers = [1, point, (point * point) % FIELD_PRIME, (point * point * point) % FIELD_PRIME]
    for degree, power in enumerate(powers):
        left_idx = variable_index(left, degree)
        right_idx = variable_index(right, degree)
        if left_idx is not None:
            row[left_idx] = (row[left_idx] + power) % FIELD_PRIME
        if right_idx is not None:
            row[right_idx] = (row[right_idx] - power) % FIELD_PRIME
    return row


def rref(matrix: list[list[int]], ncols: int = VARIABLE_COUNT) -> tuple[list[list[int]], list[int]]:
    rows = [[value % FIELD_PRIME for value in row] for row in matrix if any(value % FIELD_PRIME for value in row)]
    rank = 0
    pivots: list[int] = []
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(rows)):
            if rows[row_idx][col] % FIELD_PRIME:
                pivot = row_idx
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, FIELD_PRIME)
        rows[rank] = [(value * inv) % FIELD_PRIME for value in rows[rank]]
        for row_idx in range(len(rows)):
            if row_idx == rank or not rows[row_idx][col] % FIELD_PRIME:
                continue
            factor = rows[row_idx][col] % FIELD_PRIME
            rows[row_idx] = [
                (rows[row_idx][idx] - factor * rows[rank][idx]) % FIELD_PRIME for idx in range(ncols)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(rows) or rank == ncols:
            break
    return rows[:rank], pivots


def nullspace_basis(matrix: list[list[int]], ncols: int = VARIABLE_COUNT) -> list[list[int]]:
    reduced, pivots = rref(matrix, ncols=ncols)
    pivot_set = set(pivots)
    free_cols = [idx for idx in range(ncols) if idx not in pivot_set]
    basis = []
    for free in free_cols:
        vec = [0] * ncols
        vec[free] = 1
        for row, pivot in zip(reduced, pivots, strict=True):
            vec[pivot] = (-row[free]) % FIELD_PRIME
        basis.append(vec)
    return basis


def matrix_rank(matrix: list[list[int]], ncols: int = VARIABLE_COUNT) -> int:
    return len(rref(matrix, ncols=ncols)[1])


def build_interpolation_rows(partitions: list[tuple[tuple[int, ...], ...]]) -> list[list[int]]:
    domain = order8_domain()
    rows = []
    for bucket, partition in enumerate(partitions):
        point = domain[bucket]
        for block in partition:
            if len(block) <= 1:
                continue
            anchor = block[0]
            for witness in block[1:]:
                rows.append(equality_row(witness, anchor, point))
    return rows


def pair_projection_rank(basis: list[list[int]], left: int, right: int) -> int:
    if not basis:
        return 0
    rows = []
    for vector in basis:
        coeffs = []
        for degree in range(DEGREE_BOUND_Q + 1):
            left_idx = variable_index(left, degree)
            right_idx = variable_index(right, degree)
            value = 0
            if left_idx is not None:
                value += vector[left_idx]
            if right_idx is not None:
                value -= vector[right_idx]
            coeffs.append(value % FIELD_PRIME)
        rows.append(coeffs)
    return matrix_rank(rows, ncols=DEGREE_BOUND_Q + 1)


def construct_distinct_vector(basis: list[list[int]]) -> list[int] | None:
    if not basis:
        return None
    # Deterministic low-cost search over affine combinations of the first basis vectors.
    limit = min(len(basis), 6)
    for coeffs in _small_coefficients(limit):
        vector = [0] * VARIABLE_COUNT
        for coeff, basis_vector in zip(coeffs, basis[:limit], strict=True):
            for idx, value in enumerate(basis_vector):
                vector[idx] = (vector[idx] + coeff * value) % FIELD_PRIME
        if vector and all(pair_difference_nonzero(vector, left, right) for left, right in pairs()):
            return vector
    return None


def _small_coefficients(length: int):
    values = [1, 2, 3, 5, 8, 13]
    if length == 0:
        return
    yield [1] + [0] * (length - 1)
    for seed in range(1, 3000):
        out = []
        value = seed
        for idx in range(length):
            out.append(values[(value + idx) % len(values)] % FIELD_PRIME)
            value //= len(values)
        yield out


def pair_difference_nonzero(vector: list[int], left: int, right: int) -> bool:
    for degree in range(DEGREE_BOUND_Q + 1):
        left_idx = variable_index(left, degree)
        right_idx = variable_index(right, degree)
        value = 0
        if left_idx is not None:
            value += vector[left_idx]
        if right_idx is not None:
            value -= vector[right_idx]
        if value % FIELD_PRIME:
            return True
    return False


def solve_partition_model(
    time_limit: float,
    force_structural_defect: bool,
    max_partition_cost: int,
    feasibility_only: bool = False,
) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    all_partitions = set_partitions(WITNESSES)
    partitions = [partition for partition in all_partitions if equation_cost(partition) <= max_partition_cost]
    model = cp_model.CpModel()
    choose = []
    selected = []
    for bucket in range(ORDER8_LENGTH):
        choose_row = []
        selected_row = []
        for pidx, partition in enumerate(partitions):
            chosen = model.NewBoolVar(f"choose_q{bucket}_p{pidx}")
            choose_row.append(chosen)
            block_counts = []
            for bidx, _block in enumerate(partition):
                count = model.NewIntVar(0, BUCKET_SIZE, f"sel_q{bucket}_p{pidx}_b{bidx}")
                model.Add(count <= BUCKET_SIZE * chosen)
                block_counts.append(count)
            selected_row.append(block_counts)
        model.Add(sum(choose_row) == 1)
        model.Add(sum(count for block_counts in selected_row for count in block_counts) == BUCKET_SIZE)
        choose.append(choose_row)
        selected.append(selected_row)

    for witness in WITNESSES:
        model.Add(
            sum(
                selected[bucket][pidx][bidx]
                for bucket in range(ORDER8_LENGTH)
                for pidx, partition in enumerate(partitions)
                for bidx, block in enumerate(partition)
                if witness in block
            )
            == TARGET_AGREEMENT
        )

    pair_selected = {}
    pair_ambient = {}
    for pair in pairs():
        selected_var = model.NewIntVar(0, DOMAIN_SIZE, f"selected_pair_{pair[0]}_{pair[1]}")
        ambient_var = model.NewIntVar(0, ORDER8_LENGTH, f"ambient_pair_{pair[0]}_{pair[1]}")
        model.Add(
            selected_var
            == sum(
                selected[bucket][pidx][bidx]
                for bucket in range(ORDER8_LENGTH)
                for pidx, partition in enumerate(partitions)
                for bidx, block in enumerate(partition)
                if pair[0] in block and pair[1] in block
            )
        )
        model.Add(
            ambient_var
            == sum(
                choose[bucket][pidx]
                for bucket in range(ORDER8_LENGTH)
                for pidx, partition in enumerate(partitions)
                if partition_pair_same(partition, pair)
            )
        )
        model.Add(selected_var <= PAIR_CAP)
        model.Add(ambient_var <= 3)
        if pair[1] == BASELINE and pair[0] in GUARDED_TO_7:
            model.Add(selected_var >= PAIR7_LOWER)
            model.Add(ambient_var == 3)
        pair_selected[pair] = selected_var
        pair_ambient[pair] = ambient_var

    equation_count = model.NewIntVar(0, ORDER8_LENGTH * 6, "equation_count")
    model.Add(
        equation_count
        == sum(
            equation_cost(partition) * choose[bucket][pidx]
            for bucket in range(ORDER8_LENGTH)
            for pidx, partition in enumerate(partitions)
        )
    )
    if force_structural_defect:
        model.Add(equation_count <= VARIABLE_COUNT - 1)

    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for witness in GUARDED_TO_7:
        model.Add(min_pair7 <= pair_selected[(witness, BASELINE)])
    max_ambient = model.NewIntVar(0, 3, "max_ambient")
    for variable in pair_ambient.values():
        model.Add(max_ambient >= variable)
    if feasibility_only:
        pass
    elif force_structural_defect:
        model.Maximize(1000 * min_pair7 - 20 * equation_count - max_ambient)
    else:
        model.Minimize(1000 * equation_count + 10 * max_ambient - min_pair7)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 0
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "mode": (
            "support_feasibility"
            if feasibility_only
            else ("structural_defect_target" if force_structural_defect else "min_equation_fallback")
        ),
        "ortools_version": ortools_version,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "partition_count": len(partitions),
        "max_partition_cost": max_partition_cost,
        "equation_count": None,
        "support_vector": None,
        "pair7_counts": None,
        "max_ambient_pair_buckets": None,
        "selected_partitions": None,
        "selected_block_counts": None,
        "best_failure_mode": (
            "PARTITION_FIRST_STRUCTURAL_DEFECT_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and force_structural_defect
            else (
                "PARTITION_FIRST_FEASIBILITY_INFEASIBLE"
                if status_name in {"INFEASIBLE", "MODEL_INVALID"} and feasibility_only
                else "PARTITION_FIRST_FALLBACK_INFEASIBLE"
                if status_name in {"INFEASIBLE", "MODEL_INVALID"} and not feasibility_only
                else "PARTITION_FIRST_CP_UNRESOLVED"
            )
        ),
    }
    if not feasible:
        return row

    selected_partitions = []
    selected_block_counts = []
    for bucket in range(ORDER8_LENGTH):
        pidx = next(idx for idx, variable in enumerate(choose[bucket]) if solver.Value(variable))
        partition = partitions[pidx]
        selected_partitions.append([list(block) for block in partition])
        selected_block_counts.append(
            [
                {"block": list(block), "count": int(solver.Value(selected[bucket][pidx][bidx]))}
                for bidx, block in enumerate(partition)
                if int(solver.Value(selected[bucket][pidx][bidx])) > 0
            ]
        )
    selected_pair_counts = {
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in pair_selected.items()
    }
    ambient_pair_bucket_counts = {
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in pair_ambient.items()
    }
    row.update(
        {
            "equation_count": int(solver.Value(equation_count)),
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
            "max_ambient_pair_buckets": max(ambient_pair_bucket_counts.values()),
            "selected_partitions": selected_partitions,
            "selected_block_counts": selected_block_counts,
            "best_failure_mode": "PARTITION_FIRST_SCHEDULE_FEASIBLE",
        }
    )
    return row


def interpolation_audit(schedule: dict[str, Any]) -> dict[str, Any]:
    if not schedule["feasible"]:
        return {
            "attempted": False,
            "rank": None,
            "nullity": None,
            "forced_equal_pairs": [],
            "candidate_constructed": False,
            "best_failure_mode": "PARTITION_FIRST_NO_SCHEDULE",
        }
    partitions = [
        tuple(tuple(block) for block in partition)
        for partition in schedule["selected_partitions"]
    ]
    rows = build_interpolation_rows(partitions)
    rank = matrix_rank(rows)
    basis = nullspace_basis(rows)
    forced = []
    projection_ranks = {}
    if basis:
        for left, right in pairs():
            proj_rank = pair_projection_rank(basis, left, right)
            projection_ranks[f"{left}{right}"] = proj_rank
            if proj_rank == 0:
                forced.append([left, right])
    vector = construct_distinct_vector(basis)
    return {
        "attempted": True,
        "matrix_shape": [len(rows), VARIABLE_COUNT],
        "rank": rank,
        "nullity": VARIABLE_COUNT - rank,
        "basis_dimension": len(basis),
        "forced_equal_pairs": forced,
        "projection_rank_by_pair": projection_ranks,
        "candidate_constructed": vector is not None,
        "candidate_coefficients": None
        if vector is None
        else [vector[(witness - 1) * 4 : witness * 4] for witness in NONBASELINE],
        "best_failure_mode": "PARTITION_FIRST_EXACT_CANDIDATE"
        if vector is not None
        else ("PARTITION_FIRST_INTERPOLATION_NULLITY_ZERO" if not basis else "PARTITION_FIRST_FORCED_PAIR_EQUALITY"),
    }


def build_record(time_limit: float, max_partition_cost: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    target = solve_partition_model(time_limit, force_structural_defect=True, max_partition_cost=max_partition_cost)
    feasibility = solve_partition_model(
        time_limit, force_structural_defect=False, max_partition_cost=max_partition_cost, feasibility_only=True
    )
    fallback = solve_partition_model(time_limit, force_structural_defect=False, max_partition_cost=max_partition_cost)
    chosen = target if target["feasible"] else (feasibility if feasibility["feasible"] else fallback)
    audit = interpolation_audit(chosen)
    candidate = bool(audit["candidate_constructed"])
    proof_status = (
        "CANDIDATE / PARTITION_FIRST_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        if candidate
        else "EXACT_EXTRACTION_NO_A327 / PARTITION_FIRST_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": TRACK,
        "row": ROW,
        "denominator": DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_order8_degree3_codesign": {
            "proof_status": previous["proof_status"],
            "candidates_tested": previous["order8_degree3_codesign"]["candidates_tested"],
            "feasible_allocations": previous["order8_degree3_codesign"]["feasible_allocations"],
            "failure_mode": previous["order8_degree3_codesign"]["best_failure_mode"],
        },
        "partition_first_search": {
            "time_limit_seconds": time_limit,
            "max_partition_cost": max_partition_cost,
            "variable_count": VARIABLE_COUNT,
            "structural_defect_target_feasible": target["feasible"],
            "support_feasibility_feasible": feasibility["feasible"],
            "fallback_feasible": fallback["feasible"],
            "chosen_mode": chosen["mode"],
            "chosen_equation_count": chosen["equation_count"],
            "interpolation_rank": audit["rank"],
            "interpolation_nullity": audit["nullity"],
            "candidate_constructed": candidate,
            "best_failure_mode": audit["best_failure_mode"],
        },
        "models": [target, feasibility, fallback],
        "interpolation_audit": audit,
        "candidate": {
            "constructed": candidate,
            "seven_distinct": candidate,
            "agreement_vector": chosen["support_vector"] if candidate else None,
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
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--max-partition-cost", type=int, default=3)
    args = parser.parse_args()
    record = build_record(args.time_limit, args.max_partition_cost)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {"proof_status": record["proof_status"], **record["partition_first_search"]}
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_ORDER8_PARTITION_FIRST_INTERPOLATION_SEARCH_READY")


if __name__ == "__main__":
    main()
