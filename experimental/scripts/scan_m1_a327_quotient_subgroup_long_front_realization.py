#!/usr/bin/env python3
"""Proxy realization screen for feasible long-front quotient-subgroup schedules."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


SOURCE_COMMIT = "59b268b"
INPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_long_cpsat_front.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_long_front_realization.json")

TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
WITNESSES = tuple(range(1, 8))
BASELINE_WITNESS = 7
PAIR_CAP = 255
PAIR7_LOWER = 142
PROXY_PRIME = 193
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the tested long-front realization schedules",
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
    if len(set(values)) != length:
        raise ValueError("failed to build quotient values")
    return values


def variable_index(witness: int, degree: int, degree_bound: int) -> int | None:
    if witness == BASELINE_WITNESS:
        return None
    if not 1 <= witness <= 6:
        raise ValueError(f"unexpected witness {witness}")
    return (witness - 1) * (degree_bound + 1) + degree


def equality_row(left: int, right: int, y_value: int, degree_bound: int, prime: int) -> list[int]:
    variables = 6 * (degree_bound + 1)
    row = [0] * variables
    powers = [1]
    for _ in range(degree_bound):
        powers.append((powers[-1] * y_value) % prime)
    for degree, power in enumerate(powers):
        left_idx = variable_index(left, degree, degree_bound)
        right_idx = variable_index(right, degree, degree_bound)
        if left_idx is not None:
            row[left_idx] = (row[left_idx] + power) % prime
        if right_idx is not None:
            row[right_idx] = (row[right_idx] - power) % prime
    return row


def numpy_rank_mod(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    rows = np.array(matrix, dtype=np.int64) % prime
    rank = 0
    row_count, column_count = rows.shape
    for column in range(column_count):
        pivots = np.nonzero(rows[rank:, column] % prime)[0]
        if pivots.size == 0:
            continue
        pivot = rank + int(pivots[0])
        if pivot != rank:
            rows[[rank, pivot]] = rows[[pivot, rank]]
        inverse = pow(int(rows[rank, column]), -1, prime)
        rows[rank, :] = (rows[rank, :] * inverse) % prime
        factors = rows[:, column].copy() % prime
        mask = factors != 0
        mask[rank] = False
        if mask.any():
            rows[mask, :] = (rows[mask, :] - factors[mask, None] * rows[rank, :]) % prime
        rank += 1
        if rank == row_count:
            break
    return rank


def expand_schedule(screen: dict[str, Any]) -> list[dict[str, Any]]:
    s = int(screen["s"])
    quotient_length = int(screen["quotient_length"])
    coordinates = []
    q_index = 0
    for active_index, active in enumerate(screen["active_partitions"]):
        partition = partition_key(active["partition"])
        remaining = [(block_key(entry["block"]), int(entry["count"])) for entry in active["selected_block_counts"]]
        cursor = 0
        current_block, current_count = remaining[cursor]
        for local_index in range(int(active["quotient_fibers"])):
            selected_blocks = []
            for _slot in range(s):
                while current_count == 0:
                    cursor += 1
                    current_block, current_count = remaining[cursor]
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
        if current_count != 0 or cursor != len(remaining) - 1:
            raise ValueError(f"unconsumed selected counts for active partition {active_index}")
    if q_index != quotient_length:
        raise ValueError(f"expanded {q_index} quotient coordinates, expected {quotient_length}")
    return coordinates


def partition_payloads(coordinates: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for coordinate in coordinates:
        grouped[int(coordinate["active_partition_index"])].append(coordinate)
    for values in grouped.values():
        values.sort(key=lambda item: int(item["local_partition_index"]))
    return dict(grouped)


def rebuild_coordinates(signature: list[int], payloads: dict[int, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    cursors = {key: 0 for key in payloads}
    out = []
    for q_index, active_index in enumerate(signature):
        source = payloads[active_index][cursors[active_index]]
        cursors[active_index] += 1
        out.append(
            {
                "q_index": q_index,
                "active_partition_index": active_index,
                "local_partition_index": cursors[active_index] - 1,
                "partition": source["partition"],
                "selected_blocks": source["selected_blocks"],
            }
        )
    return out


def round_robin_signature(counts: Counter[int]) -> list[int]:
    remaining = Counter(counts)
    out = []
    previous = None
    while remaining:
        candidates = sorted(remaining, key=lambda key: (-remaining[key], key))
        chosen = candidates[0]
        if chosen == previous and len(candidates) > 1:
            chosen = candidates[1]
        out.append(chosen)
        previous = chosen
        remaining[chosen] -= 1
        if remaining[chosen] == 0:
            del remaining[chosen]
    return out


def residue_spread_signature(counts: Counter[int], stride: int) -> list[int]:
    values = []
    for key, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        values.extend([key] * count)
    out: list[int | None] = [None] * len(values)
    position = 0
    for value in values:
        while out[position] is not None:
            position = (position + 1) % len(out)
        out[position] = value
        position = (position + stride) % len(out)
    return [int(value) for value in out]


def candidate_signatures(base_signature: tuple[int, ...], random_trials: int, seed: int) -> list[tuple[str, list[int]]]:
    counts = Counter(base_signature)
    out = [("grouped_baseline", list(base_signature)), ("round_robin", round_robin_signature(counts))]
    for stride in [3, 5, 7, 11, 17, 31]:
        out.append((f"residue_spread_stride_{stride}", residue_spread_signature(counts, stride)))
    rng = random.Random(seed)
    seen = {tuple(signature) for _, signature in out}
    base = list(base_signature)
    for trial in range(random_trials):
        shuffled = base[:]
        rng.shuffle(shuffled)
        key = tuple(shuffled)
        if key in seen:
            continue
        seen.add(key)
        out.append((f"random_seed_{seed}_{trial}", shuffled))
    return out


def build_proxy_rows(coordinates: list[dict[str, Any]], s: int, prime: int) -> list[list[int]]:
    quotient_length = DOMAIN_SIZE // s
    degree_bound = PAIR_CAP // s
    values = quotient_values_mod_prime(prime, quotient_length)
    rows = []
    for coordinate in coordinates:
        y_value = values[int(coordinate["q_index"])]
        for block in partition_key(coordinate["partition"]):
            if len(block) <= 1:
                continue
            anchor = block[0]
            for witness in block[1:]:
                rows.append(equality_row(witness, anchor, y_value, degree_bound, prime))
    return rows


def proxy_for_coordinates(coordinates: list[dict[str, Any]], s: int) -> dict[str, Any]:
    degree_bound = PAIR_CAP // s
    variables = 6 * (degree_bound + 1)
    rows = build_proxy_rows(coordinates, s, PROXY_PRIME)
    rank = numpy_rank_mod(rows, PROXY_PRIME)
    nullity = variables - rank
    return {
        "proxy_field": f"GF({PROXY_PRIME})",
        "matrix_shape": [len(rows), variables],
        "rank": rank,
        "nullity": nullity,
        "best_failure_mode": "LONG_FRONT_REALIZATION_PROXY_POSITIVE" if nullity > 0 else "LONG_FRONT_REALIZATION_PROXY_FULL_RANK",
    }


def evaluate_screen(screen: dict[str, Any], random_trials: int, seed: int) -> dict[str, Any]:
    coordinates = expand_schedule(screen)
    payloads = partition_payloads(coordinates)
    base_signature = tuple(int(coordinate["active_partition_index"]) for coordinate in coordinates)
    best = None
    tested = 0
    positive = 0
    for label, signature in candidate_signatures(base_signature, random_trials, seed):
        labelled = rebuild_coordinates(signature, payloads)
        proxy = proxy_for_coordinates(labelled, int(screen["s"]))
        tested += 1
        if proxy["nullity"] > 0:
            positive += 1
        row = {
            "label": label,
            "matrix_shape": proxy["matrix_shape"],
            "proxy_rank": proxy["rank"],
            "proxy_nullity": proxy["nullity"],
            "best_failure_mode": proxy["best_failure_mode"],
        }
        if best is None or (row["proxy_rank"], -row["proxy_nullity"], row["label"]) < (
            best["proxy_rank"],
            -best["proxy_nullity"],
            best["label"],
        ):
            best = row
    assert best is not None
    return {
        "s": screen["s"],
        "quotient_length": screen["quotient_length"],
        "quotient_degree_bound": screen["quotient_degree_bound"],
        "support_vector": screen["support_vector"],
        "pair7_counts": screen["pair7_counts"],
        "max_pair_equal_h_count": screen["max_pair_equal_h_count"],
        "active_partition_count": screen["active_partition_count"],
        "labellings_tested": tested,
        "proxy_positive_labellings": positive,
        "best_label": best["label"],
        "best_matrix_shape": best["matrix_shape"],
        "best_proxy_rank": best["proxy_rank"],
        "best_proxy_nullity": best["proxy_nullity"],
        "best_failure_mode": best["best_failure_mode"],
    }


def build_record(random_trials: int, seed: int) -> dict[str, Any]:
    previous = load_json(INPUT_DATA)
    feasible = [screen for screen in previous["screens"] if screen["feasible"]]
    results = [evaluate_screen(screen, random_trials, seed + int(screen["s"])) for screen in feasible]
    positives = [row for row in results if row["proxy_positive_labellings"] > 0]
    best = None
    for row in results:
        key = (row["best_proxy_rank"], -row["best_proxy_nullity"], row["s"])
        if best is None or key < best[0]:
            best = (key, row)
    best_row = None if best is None else best[1]
    proof_status = (
        "CANDIDATE / LONG_FRONT_REALIZATION_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if positives
        else "EXACT_EXTRACTION_NO_A327 / LONG_FRONT_REALIZATION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_long_cpsat_front": {
            "proof_status": previous["proof_status"],
            "screens_tested": previous["long_cpsat_front"]["screens_tested"],
            "cp_feasible_screens": previous["long_cpsat_front"]["cp_feasible_screens"],
            "best_s": previous["long_cpsat_front"]["best_s"],
            "failure_mode": previous["long_cpsat_front"]["best_failure_mode"],
        },
        "long_front_realization": {
            "proxy_field": f"GF({PROXY_PRIME})",
            "random_trials_per_screen": random_trials,
            "seed": seed,
            "screens_realized": len(results),
            "proxy_positive_screens": len(positives),
            "best_s": None if best_row is None else best_row["s"],
            "best_matrix_shape": None if best_row is None else best_row["best_matrix_shape"],
            "best_proxy_rank": None if best_row is None else best_row["best_proxy_rank"],
            "best_proxy_nullity": None if best_row is None else best_row["best_proxy_nullity"],
            "best_failure_mode": "LONG_FRONT_REALIZATION_PROXY_POSITIVE" if positives else "LONG_FRONT_REALIZATION_PROXY_FULL_RANK",
        },
        "realization_results": results,
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
    parser.add_argument("--random-trials", type=int, default=24)
    parser.add_argument("--seed", type=int, default=2)
    args = parser.parse_args()
    record = build_record(args.random_trials, args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps({"proof_status": record["proof_status"], **record["long_front_realization"]}, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_LONG_FRONT_REALIZATION_READY")


if __name__ == "__main__":
    main()
