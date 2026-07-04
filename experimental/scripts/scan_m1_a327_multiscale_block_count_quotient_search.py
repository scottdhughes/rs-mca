#!/usr/bin/env python3
"""Multiscale block-count quotient search for M1 a=327."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "f5dcd61"
PREVIOUS_DATA = Path("experimental/data/m1_a327_order8_block_count_partition_grammar_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_multiscale_block_count_quotient_search.json")

TRACK = "INTERLEAVED_LIST"
ROW = "RS[F_17^32,H,256]"
DENOMINATOR = "17^32"
TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
PAIR_CAP = 255
PAIR7_LOWER = 142
WITNESSES = tuple(range(1, 8))
NONBASELINE = tuple(range(1, 7))
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
    "MCA/protocol consequence from this list-track multiscale quotient search",
    "global obstruction outside the tested quotient block-count models",
]


class PrimeField:
    def __init__(self, prime: int) -> None:
        self.prime = prime
        self.zero = 0
        self.one = 1
        self.name = f"GF({prime})"

    def add(self, left: int, right: int) -> int:
        return (left + right) % self.prime

    def sub(self, left: int, right: int) -> int:
        return (left - right) % self.prime

    def mul(self, left: int, right: int) -> int:
        return (left * right) % self.prime

    def inv(self, value: int) -> int:
        if value % self.prime == 0:
            raise ZeroDivisionError("field inverse of zero")
        return pow(value, -1, self.prime)

    def pow(self, value: int, exponent: int) -> int:
        return pow(value, exponent, self.prime)

    def neg(self, value: int) -> int:
        return (-value) % self.prime

    def small_elements(self) -> list[int]:
        return [1, 2, 3, 5, 8, 13]

    def element_label(self, value: int) -> str:
        return str(value % self.prime)

    def elements(self) -> range:
        return range(self.prime)


class QuadraticField:
    """GF(17^2) as GF(17)[u]/(u^2-3), with elements a + 17*b."""

    def __init__(self) -> None:
        self.prime = 17
        self.nonsquare = 3
        self.zero = 0
        self.one = 1
        self.name = "GF(17^2)"

    def _split(self, value: int) -> tuple[int, int]:
        return value % self.prime, (value // self.prime) % self.prime

    def _join(self, real: int, imag: int) -> int:
        return (real % self.prime) + self.prime * (imag % self.prime)

    def add(self, left: int, right: int) -> int:
        a, b = self._split(left)
        c, d = self._split(right)
        return self._join(a + c, b + d)

    def sub(self, left: int, right: int) -> int:
        a, b = self._split(left)
        c, d = self._split(right)
        return self._join(a - c, b - d)

    def neg(self, value: int) -> int:
        a, b = self._split(value)
        return self._join(-a, -b)

    def mul(self, left: int, right: int) -> int:
        a, b = self._split(left)
        c, d = self._split(right)
        return self._join(a * c + self.nonsquare * b * d, a * d + b * c)

    def pow(self, value: int, exponent: int) -> int:
        out = self.one
        base = value
        current = exponent
        while current:
            if current & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            current >>= 1
        return out

    def inv(self, value: int) -> int:
        if value == self.zero:
            raise ZeroDivisionError("field inverse of zero")
        # Multiplicative group has order 17^2-1.
        return self.pow(value, self.prime * self.prime - 2)

    def small_elements(self) -> list[int]:
        return [1, 2, 3, 5, 8, 13, 17, 18, 19, 34]

    def element_label(self, value: int) -> str:
        a, b = self._split(value)
        if b == 0:
            return str(a)
        if a == 0:
            return f"{b}u"
        return f"{a}+{b}u"

    def elements(self) -> range:
        return range(self.prime * self.prime)


def require_ortools() -> tuple[Any, str]:
    try:
        from ortools.sat.python import cp_model  # type: ignore
        import ortools  # type: ignore

        return cp_model, str(ortools.__version__)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "OR-Tools is required. Run with "
            "/Users/scott/.venvs/rs-mca-ortools/bin/python "
            "experimental/scripts/scan_m1_a327_multiscale_block_count_quotient_search.py"
        ) from exc


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def block_family(block_sizes: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [tuple(block) for size in block_sizes for block in combinations(WITNESSES, size)]


def quotient_degree_bound(quotient_order: int) -> int:
    fiber_size = DOMAIN_SIZE // quotient_order
    return PAIR_CAP // fiber_size


def quotient_field(quotient_order: int) -> PrimeField | QuadraticField:
    if quotient_order == 16:
        return PrimeField(17)
    if quotient_order == 32:
        return QuadraticField()
    raise ValueError(f"unsupported quotient order: {quotient_order}")


def multiplicative_order(field: PrimeField | QuadraticField, value: int) -> int:
    if value == field.zero:
        return 0
    current = value
    order = 1
    while current != field.one:
        current = field.mul(current, value)
        order += 1
        if order > 1000:
            raise RuntimeError("order search did not terminate")
    return order


def quotient_domain(quotient_order: int) -> list[int]:
    field = quotient_field(quotient_order)
    generator = next(value for value in field.elements() if multiplicative_order(field, value) == quotient_order)
    return [field.pow(generator, idx) for idx in range(quotient_order)]


def variable_index(witness: int, degree: int, degree_bound: int) -> int | None:
    if witness == BASELINE:
        return None
    return (witness - 1) * (degree_bound + 1) + degree


def equality_row(
    field: PrimeField | QuadraticField,
    degree_bound: int,
    left: int,
    right: int,
    point: int,
) -> list[int]:
    ncols = len(NONBASELINE) * (degree_bound + 1)
    row = [field.zero] * ncols
    powers = [field.one]
    for _degree in range(degree_bound):
        powers.append(field.mul(powers[-1], point))
    for degree, power in enumerate(powers):
        left_idx = variable_index(left, degree, degree_bound)
        right_idx = variable_index(right, degree, degree_bound)
        if left_idx is not None:
            row[left_idx] = field.add(row[left_idx], power)
        if right_idx is not None:
            row[right_idx] = field.sub(row[right_idx], power)
    return row


def rref(
    matrix: list[list[int]],
    field: PrimeField | QuadraticField,
    ncols: int,
) -> tuple[list[list[int]], list[int]]:
    rows = [[value for value in row] for row in matrix if any(value != field.zero for value in row)]
    rank = 0
    pivots: list[int] = []
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(rows)):
            if rows[row_idx][col] != field.zero:
                pivot = row_idx
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = field.inv(rows[rank][col])
        rows[rank] = [field.mul(value, inv) for value in rows[rank]]
        for row_idx in range(len(rows)):
            if row_idx == rank or rows[row_idx][col] == field.zero:
                continue
            factor = rows[row_idx][col]
            rows[row_idx] = [
                field.sub(rows[row_idx][idx], field.mul(factor, rows[rank][idx])) for idx in range(ncols)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(rows) or rank == ncols:
            break
    return rows[:rank], pivots


def matrix_rank(matrix: list[list[int]], field: PrimeField | QuadraticField, ncols: int) -> int:
    return len(rref(matrix, field, ncols)[1])


def nullspace_basis(matrix: list[list[int]], field: PrimeField | QuadraticField, ncols: int) -> list[list[int]]:
    reduced, pivots = rref(matrix, field, ncols)
    pivot_set = set(pivots)
    free_cols = [idx for idx in range(ncols) if idx not in pivot_set]
    basis = []
    for free in free_cols:
        vector = [field.zero] * ncols
        vector[free] = field.one
        for row, pivot in zip(reduced, pivots, strict=True):
            vector[pivot] = field.neg(row[free])
        basis.append(vector)
    return basis


def build_interpolation_rows(
    selected_partitions: list[list[list[int]]],
    quotient_order: int,
) -> tuple[list[list[int]], PrimeField | QuadraticField, int]:
    field = quotient_field(quotient_order)
    degree_bound = quotient_degree_bound(quotient_order)
    domain = quotient_domain(quotient_order)
    rows = []
    for bucket, partition in enumerate(selected_partitions):
        point = domain[bucket]
        for block in partition:
            if len(block) <= 1:
                continue
            anchor = block[0]
            for witness in block[1:]:
                rows.append(equality_row(field, degree_bound, witness, anchor, point))
    return rows, field, degree_bound


def pair_difference_nonzero(
    vector: list[int],
    field: PrimeField | QuadraticField,
    degree_bound: int,
    left: int,
    right: int,
) -> bool:
    for degree in range(degree_bound + 1):
        left_idx = variable_index(left, degree, degree_bound)
        right_idx = variable_index(right, degree, degree_bound)
        value = field.zero
        if left_idx is not None:
            value = field.add(value, vector[left_idx])
        if right_idx is not None:
            value = field.sub(value, vector[right_idx])
        if value != field.zero:
            return True
    return False


def pair_projection_rank(
    basis: list[list[int]],
    field: PrimeField | QuadraticField,
    degree_bound: int,
    left: int,
    right: int,
) -> int:
    if not basis:
        return 0
    rows = []
    for vector in basis:
        coeffs = []
        for degree in range(degree_bound + 1):
            left_idx = variable_index(left, degree, degree_bound)
            right_idx = variable_index(right, degree, degree_bound)
            value = field.zero
            if left_idx is not None:
                value = field.add(value, vector[left_idx])
            if right_idx is not None:
                value = field.sub(value, vector[right_idx])
            coeffs.append(value)
        rows.append(coeffs)
    return matrix_rank(rows, field, degree_bound + 1)


def small_coefficients(field: PrimeField | QuadraticField, length: int):
    values = field.small_elements()
    if length <= 0:
        return
    yield [field.one] + [field.zero] * (length - 1)
    for seed in range(1, 5000):
        out = []
        current = seed
        for idx in range(length):
            out.append(values[(current + idx) % len(values)])
            current //= len(values)
        yield out


def construct_distinct_vector(
    basis: list[list[int]],
    field: PrimeField | QuadraticField,
    degree_bound: int,
) -> list[int] | None:
    if not basis:
        return None
    limit = min(len(basis), 8)
    ncols = len(basis[0])
    for coeffs in small_coefficients(field, limit):
        vector = [field.zero] * ncols
        for coeff, basis_vector in zip(coeffs, basis[:limit], strict=True):
            for idx, value in enumerate(basis_vector):
                vector[idx] = field.add(vector[idx], field.mul(coeff, value))
        if all(pair_difference_nonzero(vector, field, degree_bound, left, right) for left, right in pairs()):
            return vector
    return None


def solve_block_count_model(
    quotient_order: int,
    mode: str,
    block_sizes: tuple[int, ...],
    time_limit: float,
    seed: int,
) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    bucket_size = DOMAIN_SIZE // quotient_order
    degree_bound = quotient_degree_bound(quotient_order)
    blocks = block_family(block_sizes)
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
        if mode in {"pair_cap", "ambient_pair_cap"}:
            model.Add(selected_var <= PAIR_CAP)
        if mode in {"pair7_guard", "pair_cap", "ambient_pair_cap"}:
            if right == BASELINE and left in GUARDED_TO_7:
                model.Add(selected_var >= PAIR7_LOWER)
        if mode == "ambient_pair_cap":
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
    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for witness in GUARDED_TO_7:
        model.Add(min_pair7 <= pair_selected[(witness, BASELINE)])
    max_selected_pair = model.NewIntVar(0, DOMAIN_SIZE, "max_selected_pair")
    max_ambient_pair = model.NewIntVar(0, quotient_order, "max_ambient_pair")
    for pair in pairs():
        model.Add(max_selected_pair >= pair_selected[pair])
        model.Add(max_ambient_pair >= pair_ambient[pair])
    if mode == "support_only":
        model.Minimize(equation_count)
    elif mode == "pair7_guard":
        model.Minimize(1000 * equation_count + max_selected_pair - min_pair7)
    else:
        model.Minimize(1000 * equation_count + 10 * max_ambient_pair + max_selected_pair - min_pair7)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "quotient_order": quotient_order,
        "bucket_size": bucket_size,
        "degree_bound": degree_bound,
        "mode": mode,
        "ortools_version": ortools_version,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "time_limit_seconds": time_limit,
        "block_sizes": list(block_sizes),
        "block_count": len(blocks),
        "equation_count": None,
        "support_vector": None,
        "pair7_counts": None,
        "max_selected_pair_count": None,
        "max_ambient_pair_buckets": None,
        "selected_partitions": None,
        "selected_block_counts": None,
        "best_failure_mode": (
            "MULTISCALE_SUPPORT_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "support_only"
            else "MULTISCALE_PAIR7_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "pair7_guard"
            else "MULTISCALE_PAIR_CAP_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "pair_cap"
            else "MULTISCALE_AMBIENT_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "ambient_pair_cap"
            else "MULTISCALE_CP_UNRESOLVED"
        ),
    }
    if not feasible:
        return row

    selected_block_counts = []
    selected_partitions = []
    for bucket in range(quotient_order):
        bucket_blocks = [block for bidx, block in enumerate(blocks) if int(solver.Value(active[bucket][bidx])) > 0]
        covered = {witness for block in bucket_blocks for witness in block}
        partition = [list(block) for block in bucket_blocks]
        partition.extend([witness] for witness in WITNESSES if witness not in covered)
        selected_partitions.append(sorted(partition, key=lambda block: (block[0], len(block), block)))
        selected_block_counts.append(
            [
                {"block": list(block), "count": int(solver.Value(selected[bucket][bidx]))}
                for bidx, block in enumerate(blocks)
                if int(solver.Value(active[bucket][bidx])) > 0
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
            "max_selected_pair_count": max(selected_pair_counts.values()),
            "max_ambient_pair_buckets": max(ambient_pair_bucket_counts.values()),
            "selected_partitions": selected_partitions,
            "selected_block_counts": selected_block_counts,
            "best_failure_mode": "MULTISCALE_SCHEDULE_FEASIBLE",
        }
    )
    return row


def audit_schedule(schedule: dict[str, Any]) -> dict[str, Any]:
    if not schedule["feasible"]:
        return {
            "attempted": False,
            "rank": None,
            "nullity": None,
            "forced_equal_pairs": [],
            "candidate_constructed": False,
            "best_failure_mode": "MULTISCALE_NO_SCHEDULE",
        }
    rows, field, degree_bound = build_interpolation_rows(schedule["selected_partitions"], schedule["quotient_order"])
    ncols = len(NONBASELINE) * (degree_bound + 1)
    rank = matrix_rank(rows, field, ncols)
    basis = nullspace_basis(rows, field, ncols)
    forced = []
    projection_ranks = {}
    if basis:
        for left, right in pairs():
            proj_rank = pair_projection_rank(basis, field, degree_bound, left, right)
            projection_ranks[f"{left}{right}"] = proj_rank
            if proj_rank == 0:
                forced.append([left, right])
    vector = construct_distinct_vector(basis, field, degree_bound)
    return {
        "attempted": True,
        "quotient_order": schedule["quotient_order"],
        "field": field.name,
        "degree_bound": degree_bound,
        "matrix_shape": [len(rows), ncols],
        "rank": rank,
        "nullity": ncols - rank,
        "basis_dimension": len(basis),
        "forced_equal_pairs": forced,
        "projection_rank_by_pair": projection_ranks,
        "candidate_constructed": vector is not None,
        "candidate_coefficients": None
        if vector is None
        else [
            [field.element_label(value) for value in vector[(witness - 1) * (degree_bound + 1) : witness * (degree_bound + 1)]]
            for witness in NONBASELINE
        ],
        "best_failure_mode": "MULTISCALE_EXACT_CANDIDATE"
        if vector is not None
        else ("MULTISCALE_INTERPOLATION_NULLITY_ZERO" if not basis else "MULTISCALE_FORCED_PAIR_EQUALITY"),
    }


def run_order(quotient_order: int, block_sizes: tuple[int, ...], time_limit: float, seed: int) -> dict[str, Any]:
    modes = ["support_only", "pair7_guard", "pair_cap", "ambient_pair_cap"]
    models = [
        solve_block_count_model(quotient_order, mode, block_sizes, time_limit, seed + quotient_order + idx)
        for idx, mode in enumerate(modes)
    ]
    fully_constrained = models[-1]
    audit = audit_schedule(fully_constrained)
    return {
        "quotient_order": quotient_order,
        "bucket_size": DOMAIN_SIZE // quotient_order,
        "degree_bound": quotient_degree_bound(quotient_order),
        "field": quotient_field(quotient_order).name,
        "models": models,
        "interpolation_audit": audit,
        "summary": {
            "support_only_feasible": models[0]["feasible"],
            "pair7_guard_feasible": models[1]["feasible"],
            "pair_cap_feasible": models[2]["feasible"],
            "ambient_pair_cap_feasible": fully_constrained["feasible"],
            "interpolation_audit_attempted": audit["attempted"],
            "interpolation_rank": audit["rank"],
            "interpolation_nullity": audit["nullity"],
            "candidate_constructed": audit["candidate_constructed"],
            "best_failure_mode": audit["best_failure_mode"]
            if fully_constrained["feasible"]
            else fully_constrained["best_failure_mode"],
        },
    }


def build_record(orders: list[int], time_limit: float, block_sizes: tuple[int, ...], seed: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    results = [run_order(order, block_sizes, time_limit, seed) for order in orders]
    candidate_orders = [result["quotient_order"] for result in results if result["summary"]["candidate_constructed"]]
    if candidate_orders:
        proof_status = "CANDIDATE / MULTISCALE_QUOTIENT_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        best_failure = "MULTISCALE_EXACT_CANDIDATE"
    elif any(result["summary"]["interpolation_audit_attempted"] for result in results):
        proof_status = "EXACT_EXTRACTION_NO_A327 / MULTISCALE_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
        best_failure = "MULTISCALE_INTERPOLATION_NO_CANDIDATE"
    elif all(result["summary"]["ambient_pair_cap_feasible"] is False for result in results):
        proof_status = "EXACT_EXTRACTION_NO_A327 / MULTISCALE_AMBIENT_INFEASIBLE / PARTIAL / EXPERIMENTAL"
        best_failure = "MULTISCALE_AMBIENT_INFEASIBLE"
    else:
        proof_status = "EXACT_EXTRACTION_NO_A327 / MULTISCALE_CP_UNRESOLVED / PARTIAL / EXPERIMENTAL"
        best_failure = "MULTISCALE_CP_UNRESOLVED"
    return {
        "track": TRACK,
        "row": ROW,
        "denominator": DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_order8_block_count": {
            "proof_status": previous["proof_status"],
            "support_only_feasible": previous["block_count_search"]["support_only_feasible"],
            "pair7_guard_feasible": previous["block_count_search"]["pair7_guard_feasible"],
            "pair_cap_feasible": previous["block_count_search"]["pair_cap_feasible"],
            "ambient_pair_cap_feasible": previous["block_count_search"]["ambient_pair_cap_feasible"],
            "best_failure_mode": previous["block_count_search"]["best_failure_mode"],
        },
        "multiscale_search": {
            "orders_tested": orders,
            "block_sizes": list(block_sizes),
            "time_limit_seconds_per_model": time_limit,
            "models_tested": len(results) * 4,
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
    parser.add_argument("--time-limit", type=float, default=30.0)
    parser.add_argument("--block-sizes", type=int, nargs="+", default=[1, 2, 3, 4, 5, 6, 7])
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    record = build_record(args.orders, args.time_limit, tuple(args.block_sizes), args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {"proof_status": record["proof_status"], **record["multiscale_search"]}
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MULTISCALE_BLOCK_COUNT_QUOTIENT_SEARCH_READY")


if __name__ == "__main__":
    main()
