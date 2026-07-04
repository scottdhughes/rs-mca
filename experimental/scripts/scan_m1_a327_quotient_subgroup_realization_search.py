#!/usr/bin/env python3
"""Realization screen for the M1 a=327 s=4 quotient-subgroup schedule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "7e21f1d"
PREVIOUS_DATA = Path("experimental/data/m1_a327_quotient_subgroup_primal_kernel_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_realization_search.json")

TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
WITNESSES = tuple(range(1, 8))
BASELINE_WITNESS = 7
PAIR_CAP = 255
PAIR7_LOWER = 142
S_VALUE = 4
QUOTIENT_LENGTH = DOMAIN_SIZE // S_VALUE
QUOTIENT_DEGREE_BOUND = PAIR_CAP // S_VALUE
QUOTIENT_VARIABLES = (len(WITNESSES) - 1) * (QUOTIENT_DEGREE_BOUND + 1)
PROXY_PRIME = 257

REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the labelled quotient schedule tested here",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def block_key(block: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(int(value) for value in block))


def partition_key(partition: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((block_key(block) for block in partition), key=lambda block: (block[0], len(block), block)))


def same_block(partition: tuple[tuple[int, ...], ...], left: int, right: int) -> bool:
    return any(left in block and right in block for block in partition)


def primitive_root_mod_prime(prime: int) -> int:
    factors: set[int] = set()
    value = prime - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for {prime}")


def quotient_values_mod_prime(prime: int, length: int) -> tuple[int, ...]:
    if (prime - 1) % length != 0:
        raise ValueError(f"prime {prime} does not contain order-{length} subgroup")
    primitive = primitive_root_mod_prime(prime)
    generator = pow(primitive, (prime - 1) // length, prime)
    values = tuple(pow(generator, idx, prime) for idx in range(length))
    if len(set(values)) != length or pow(generator, length, prime) != 1:
        raise ValueError("failed to build quotient subgroup")
    return values


def variable_index(witness: int, degree: int) -> int | None:
    if witness == BASELINE_WITNESS:
        return None
    if not 1 <= witness <= 6:
        raise ValueError(f"unexpected witness {witness}")
    return (witness - 1) * (QUOTIENT_DEGREE_BOUND + 1) + degree


def equality_row(left: int, right: int, y_value: int, prime: int) -> list[int]:
    row = [0] * QUOTIENT_VARIABLES
    powers = [1]
    for _ in range(QUOTIENT_DEGREE_BOUND):
        powers.append((powers[-1] * y_value) % prime)
    for degree, power in enumerate(powers):
        left_idx = variable_index(left, degree)
        right_idx = variable_index(right, degree)
        if left_idx is not None:
            row[left_idx] = (row[left_idx] + power) % prime
        if right_idx is not None:
            row[right_idx] = (row[right_idx] - power) % prime
    return row


def quotient_rank(matrix: list[list[int]], prime: int) -> int:
    rows = [row[:] for row in matrix if any(value % prime for value in row)]
    rank = 0
    column_count = QUOTIENT_VARIABLES if not rows else len(rows[0])
    for column in range(column_count):
        pivot = None
        for ridx in range(rank, len(rows)):
            if rows[ridx][column] % prime:
                pivot = ridx
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][column] % prime, -1, prime)
        rows[rank] = [(value * inv) % prime for value in rows[rank]]
        for ridx, row in enumerate(rows):
            if ridx == rank:
                continue
            factor = row[column] % prime
            if factor:
                rows[ridx] = [(value - factor * pivot_value) % prime for value, pivot_value in zip(row, rows[rank], strict=True)]
        rank += 1
        if rank == len(rows):
            break
    return rank


def pair_projection_rows(pair: tuple[int, int]) -> list[list[int]]:
    left, right = pair
    out = []
    for degree in range(QUOTIENT_DEGREE_BOUND + 1):
        row = [0] * QUOTIENT_VARIABLES
        left_idx = variable_index(left, degree)
        right_idx = variable_index(right, degree)
        if left_idx is not None:
            row[left_idx] = 1
        if right_idx is not None:
            row[right_idx] = (row[right_idx] - 1) % PROXY_PRIME
        out.append(row)
    return out


def expand_schedule(best_screen: dict[str, Any]) -> list[dict[str, Any]]:
    coordinates: list[dict[str, Any]] = []
    q_index = 0
    for active_index, active in enumerate(best_screen["active_partitions"]):
        partition = partition_key(active["partition"])
        blocks_by_key = {block: block for block in partition}
        remaining: list[tuple[tuple[int, ...], int]] = []
        for entry in active["selected_block_counts"]:
            key = block_key(entry["block"])
            if key not in blocks_by_key:
                raise ValueError(f"selected block {key} not in partition {partition}")
            remaining.append((key, int(entry["count"])))
        block_cursor = 0
        current_block, current_count = remaining[block_cursor]
        for local_index in range(int(active["quotient_fibers"])):
            selected_blocks = []
            for fiber_slot in range(S_VALUE):
                while current_count == 0:
                    block_cursor += 1
                    current_block, current_count = remaining[block_cursor]
                selected_blocks.append(list(current_block))
                current_count -= 1
            coordinates.append(
                {
                    "q_index": q_index,
                    "active_partition_index": active_index,
                    "local_partition_index": local_index,
                    "partition": [list(block) for block in partition],
                    "selected_blocks": selected_blocks,
                }
            )
            q_index += 1
        if current_count != 0 or block_cursor != len(remaining) - 1:
            raise ValueError(f"unconsumed selected block counts for partition {active_index}")
    if q_index != QUOTIENT_LENGTH:
        raise ValueError(f"expanded {q_index} quotient coordinates, expected {QUOTIENT_LENGTH}")
    return coordinates


def schedule_counts(coordinates: list[dict[str, Any]]) -> dict[str, Any]:
    support = {witness: 0 for witness in WITNESSES}
    selected_pair = {f"{left}{right}": 0 for left, right in pairs()}
    pair_equal_quotient = {f"{left}{right}": 0 for left, right in pairs()}
    for coordinate in coordinates:
        partition = partition_key(coordinate["partition"])
        for left, right in pairs():
            if same_block(partition, left, right):
                pair_equal_quotient[f"{left}{right}"] += 1
        if len(coordinate["selected_blocks"]) != S_VALUE:
            raise ValueError(f"q={coordinate['q_index']} has wrong fiber slot count")
        for block in coordinate["selected_blocks"]:
            block_tuple = block_key(block)
            if block_tuple not in partition:
                raise ValueError(f"q={coordinate['q_index']} selected block not in partition")
            for witness in block_tuple:
                support[witness] += 1
            for left, right in pairs():
                if left in block_tuple and right in block_tuple:
                    selected_pair[f"{left}{right}"] += 1
    pair_equal_h = {key: S_VALUE * value for key, value in pair_equal_quotient.items()}
    return {
        "support_vector": [support[witness] for witness in WITNESSES],
        "selected_pair_counts": selected_pair,
        "pair_equal_quotient_counts": pair_equal_quotient,
        "pair_equal_h_counts": pair_equal_h,
        "pair7_counts": [selected_pair[f"{idx}7"] for idx in range(1, 6)],
        "max_pair_equal_quotient_count": max(pair_equal_quotient.values()),
        "max_pair_equal_h_count": max(pair_equal_h.values()),
    }


def build_proxy_rows(coordinates: list[dict[str, Any]], prime: int) -> tuple[list[list[int]], dict[str, int]]:
    values = quotient_values_mod_prime(prime, QUOTIENT_LENGTH)
    rows: list[list[int]] = []
    row_counts = {"anchor_equalities": 0}
    for coordinate in coordinates:
        y_value = values[int(coordinate["q_index"])]
        for block in partition_key(coordinate["partition"]):
            if len(block) <= 1:
                continue
            anchor = block[0]
            for witness in block[1:]:
                rows.append(equality_row(witness, anchor, y_value, prime))
                row_counts["anchor_equalities"] += 1
    return rows, row_counts


def proxy_realization(coordinates: list[dict[str, Any]]) -> dict[str, Any]:
    rows, row_counts = build_proxy_rows(coordinates, PROXY_PRIME)
    rank = quotient_rank(rows, PROXY_PRIME)
    nullity = QUOTIENT_VARIABLES - rank
    forced_pairs: list[list[int]] = []
    projection_rank_by_pair: dict[str, int] = {}
    if nullity > 0:
        for pair in pairs():
            stacked_rank = quotient_rank(rows + pair_projection_rows(pair), PROXY_PRIME)
            projection_rank = stacked_rank - rank
            projection_rank_by_pair[f"{pair[0]}{pair[1]}"] = projection_rank
            if projection_rank == 0:
                forced_pairs.append([pair[0], pair[1]])
    failure = "QUOTIENT_REALIZATION_PROXY_FULL_RANK"
    if nullity > 0 and forced_pairs:
        failure = "QUOTIENT_REALIZATION_FORCED_PAIR_EQUALITY"
    elif nullity > 0:
        failure = "QUOTIENT_REALIZATION_EXACT_CANDIDATE"
    return {
        "proxy_field": f"GF({PROXY_PRIME})",
        "quotient_subgroup_order": QUOTIENT_LENGTH,
        "variables": QUOTIENT_VARIABLES,
        "equations": len(rows),
        "matrix_shape": [len(rows), QUOTIENT_VARIABLES],
        "row_counts": row_counts,
        "rank": rank,
        "nullity": nullity,
        "forced_equal_pairs": forced_pairs,
        "projection_rank_by_pair": projection_rank_by_pair or None,
        "best_failure_mode": failure,
    }


def build_record() -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    best_screen = previous["best_screen"]
    coordinates = expand_schedule(best_screen)
    counts = schedule_counts(coordinates)
    proxy = proxy_realization(coordinates)
    support_ok = counts["support_vector"] == [TARGET_AGREEMENT] * len(WITNESSES)
    pair_cap_ok = counts["max_pair_equal_h_count"] <= PAIR_CAP
    pair7_ok = min(counts["pair7_counts"]) >= PAIR7_LOWER
    if not support_ok:
        failure = "QUOTIENT_REALIZATION_SUPPORT_FAIL"
    elif not pair_cap_ok:
        failure = "QUOTIENT_REALIZATION_PAIR_CAP_FAIL"
    elif not pair7_ok:
        failure = "QUOTIENT_REALIZATION_PAIR7_FAIL"
    else:
        failure = proxy["best_failure_mode"]
    proof_status = (
        "CANDIDATE / QUOTIENT_REALIZATION_EXACT_CANDIDATE / PARTIAL / EXPERIMENTAL"
        if failure == "QUOTIENT_REALIZATION_EXACT_CANDIDATE"
        else f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"
    )
    if failure in {"QUOTIENT_REALIZATION_SUPPORT_FAIL", "QUOTIENT_REALIZATION_PAIR_CAP_FAIL", "QUOTIENT_REALIZATION_PAIR7_FAIL"}:
        proof_status = f"PARTIAL / {failure} / EXPERIMENTAL"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_quotient_subgroup_primal_kernel_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_s": previous["quotient_subgroup_primal_kernel_search"]["best_s"],
            "best_pair7_counts": previous["quotient_subgroup_primal_kernel_search"]["best_pair7_counts"],
            "best_max_pair_equal_h_count": previous["quotient_subgroup_primal_kernel_search"][
                "best_max_pair_equal_h_count"
            ],
            "best_active_partition_count": previous["quotient_subgroup_primal_kernel_search"][
                "best_active_partition_count"
            ],
            "failure_mode": previous["quotient_subgroup_primal_kernel_search"]["best_failure_mode"],
        },
        "schedule": {
            "s": S_VALUE,
            "fiber_size": S_VALUE,
            "quotient_length": QUOTIENT_LENGTH,
            "quotient_degree_bound": QUOTIENT_DEGREE_BOUND,
            "labelled_quotient_coordinates": len(coordinates),
            "active_partition_count": best_screen["active_partition_count"],
            "support_vector": counts["support_vector"],
            "pair7_counts": counts["pair7_counts"],
            "selected_pair_counts": counts["selected_pair_counts"],
            "pair_equal_quotient_counts": counts["pair_equal_quotient_counts"],
            "pair_equal_h_counts": counts["pair_equal_h_counts"],
            "max_pair_equal_quotient_count": counts["max_pair_equal_quotient_count"],
            "max_pair_equal_h_count": counts["max_pair_equal_h_count"],
            "coordinates": coordinates,
        },
        "proxy_realization": proxy,
        "exact_audit": {
            "run": False,
            "field": "GF(17^32)",
            "H_order": 512,
            "candidate_available": False,
            "best_failure_mode": "QUOTIENT_REALIZATION_EXACT_NOT_RUN",
        },
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
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
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "s": record["schedule"]["s"],
                    "support_vector": record["schedule"]["support_vector"],
                    "pair7_counts": record["schedule"]["pair7_counts"],
                    "max_pair_equal_h_count": record["schedule"]["max_pair_equal_h_count"],
                    "proxy_matrix_shape": record["proxy_realization"]["matrix_shape"],
                    "proxy_rank": record["proxy_realization"]["rank"],
                    "proxy_nullity": record["proxy_realization"]["nullity"],
                    "best_failure_mode": record["proxy_realization"]["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_REALIZATION_SEARCH_READY")


if __name__ == "__main__":
    main()
