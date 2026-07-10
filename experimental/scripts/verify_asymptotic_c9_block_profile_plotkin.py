#!/usr/bin/env python3
"""Exact stdlib checks for the field-free block-profile Plotkin packet.

This is a finite arithmetic and small-instance sanity checker.  It does not
verify source-to-profile extraction, profile-atlas exhaustion, or any MCA
compiler step beyond the endpoint locator-distance fixtures tested below.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from collections.abc import Iterable
from fractions import Fraction
from itertools import combinations, product
from math import comb


class VerificationError(RuntimeError):
    """Raised when an exact check fails, including under ``python -O``."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def profile_threshold(lengths: tuple[int, ...], weights: tuple[int, ...]) -> Fraction:
    return sum(
        (Fraction(weight * (length - weight), length)
         for length, weight in zip(lengths, weights)),
        Fraction(0),
    )


def compositions(total: int, parts: int) -> list[tuple[int, ...]]:
    if parts == 1:
        return [(total,)]
    result: list[tuple[int, ...]] = []
    for first in range(1, total - parts + 2):
        for tail in compositions(total - first, parts - 1):
            result.append((first,) + tail)
    return result


def verify_shortening(max_n: int) -> int:
    checks = 0
    for n in range(2, max_n + 1):
        for q in range(1, n // 2 + 1):
            initial = Fraction(q * (n - q), n)
            for u in range(n - q + 1):
                shortened = Fraction(q * (n - u - q), n - u)
                drop = Fraction(q * q * u, n * (n - u))
                require(initial - shortened == drop, "one-block threshold drop")

                retention = Fraction(comb(n - u, q), comb(n, q))
                product_retention = Fraction(1)
                for step in range(u):
                    product_retention *= Fraction(n - step - q, n - step)
                require(retention == product_retention, "one-block retention factor")

                checks += 2
    return checks


def supports_for_profile(
    lengths: tuple[int, ...], weights: tuple[int, ...]
) -> list[int]:
    offsets: list[int] = []
    offset = 0
    block_choices: list[list[tuple[int, ...]]] = []
    for length, weight in zip(lengths, weights):
        offsets.append(offset)
        block_choices.append(list(combinations(range(length), weight)))
        offset += length
    supports: list[int] = []
    for choices in product(*block_choices):
        mask = 0
        for block_offset, local in zip(offsets, choices):
            for coordinate in local:
                mask |= 1 << (block_offset + coordinate)
        supports.append(mask)
    return supports


def johnson_distance(left: int, right: int) -> int:
    return (left & ~right).bit_count()


def maximum_clique(adjacency: list[int]) -> list[int]:
    best: list[int] = []

    def search(chosen: list[int], candidates: int) -> None:
        nonlocal best
        if len(chosen) + candidates.bit_count() <= len(best):
            return
        while candidates:
            if len(chosen) + candidates.bit_count() <= len(best):
                return
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            search(chosen + [vertex], candidates & adjacency[vertex])
        if len(chosen) > len(best):
            best = chosen

    search([], (1 << len(adjacency)) - 1)
    return best


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def centered_coordinates(
    mask: int, lengths: tuple[int, ...], weights: tuple[int, ...]
) -> list[Fraction]:
    coordinates: list[Fraction] = []
    offset = 0
    for length, weight in zip(lengths, weights):
        mean = Fraction(weight, length)
        coordinates.extend(
            Fraction((mask >> (offset + local)) & 1) - mean
            for local in range(length)
        )
        offset += length
    return coordinates


def verify_equality_gram() -> tuple[int, int]:
    fixtures = (
        ((4,), (2,)),
        ((2, 2), (1, 1)),
        ((2, 2, 2, 2), (1, 1, 1, 1)),
        ((3, 3, 3), (1, 1, 1)),
        ((4, 4), (2, 2)),
    )
    checks = 0
    words_checked = 0
    for lengths, weights in fixtures:
        threshold = profile_threshold(lengths, weights)
        require(threshold.denominator == 1 and threshold > 0, "equality fixture")
        distance = int(threshold)
        supports = supports_for_profile(lengths, weights)
        adjacency: list[int] = []
        for left, support in enumerate(supports):
            neighbors = 0
            for right, other in enumerate(supports):
                if left != right and johnson_distance(support, other) >= distance:
                    neighbors |= 1 << right
            adjacency.append(neighbors)
        clique = maximum_clique(adjacency)
        family = [supports[index] for index in clique]
        rank_bound = sum(length - 1 for length, weight in zip(lengths, weights) if weight)
        require(len(family) <= 2 * rank_bound, "equality-line code bound")

        coordinates = [centered_coordinates(mask, lengths, weights) for mask in family]
        gram: list[list[Fraction]] = []
        for left, left_vector in enumerate(coordinates):
            row: list[Fraction] = []
            for right, right_vector in enumerate(coordinates):
                inner = sum(
                    (a * b for a, b in zip(left_vector, right_vector)),
                    Fraction(0),
                )
                expected = threshold if left == right else threshold - johnson_distance(
                    family[left], family[right]
                )
                require(inner == expected, "centered Gram identity")
                normalized = inner / threshold
                require(left == right or Fraction(-1) <= normalized <= 0, "Gram sign")
                row.append(normalized)
            gram.append(row)

        rank = matrix_rank(gram)
        trace_square = sum(
            (gram[left][right] * gram[right][left]
             for left in range(len(gram)) for right in range(len(gram))),
            Fraction(0),
        )
        ones_form = sum((entry for row in gram for entry in row), Fraction(0))
        require(rank <= rank_bound, "Gram rank bound")
        require(ones_form >= 0, "Gram all-ones positivity")
        require(trace_square <= 2 * len(family), "Gram trace-square bound")
        require(len(family) ** 2 <= rank * trace_square, "Gram rank-trace bound")
        checks += 6 + len(family) ** 2
        words_checked += len(supports)
    return checks, words_checked


def balanced_step(n: int, q: int) -> tuple[int, int, Fraction, Fraction, bool]:
    require(0 < q <= n // 2, "balanced-step precondition")
    before = Fraction(q * (n - q), n)
    retention = Fraction(n - q, n)
    next_n = n - 1
    next_q = q
    complemented = next_q > next_n - next_q
    if complemented:
        next_q = next_n - next_q
    after = Fraction(next_q * (next_n - next_q), next_n) if next_n else Fraction(0)
    drop = before - after
    require(drop == Fraction(q * q, n * (n - 1)), "dynamic threshold drop")
    require(retention >= Fraction(1, 2), "dynamic retention")
    return next_n, next_q, drop, retention, complemented


def trajectory(n: int, q: int) -> list[tuple[Fraction, Fraction, bool]]:
    steps: list[tuple[Fraction, Fraction, bool]] = []
    while q:
        n, q, drop, retention, complemented = balanced_step(n, q)
        steps.append((drop, retention, complemented))
    return steps


def verify_adaptive(max_n: int) -> tuple[int, int, int, int]:
    kappas = (Fraction(1, 8), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2))
    state_checks = 0
    complement_checks = 0
    for n in range(2, max_n + 1):
        for q in range(1, n // 2 + 1):
            steps = trajectory(n, q)
            require(len(steps) == n - 1, "dynamic trajectory length")
            complement_checks += sum(complemented for _, _, complemented in steps)
            for kappa in kappas:
                if Fraction(q, n) < kappa / 2:
                    continue
                delta = min(kappa * kappa / 4, Fraction(1, 6))
                require(all(drop >= delta for drop, _, _ in steps), "adaptive drop floor")
                state_checks += len(steps) + 1

    profile_checks = 0
    adaptive_payment_cases = 0
    profile_limit = min(max_n, 16)
    for total in range(4, profile_limit + 1):
        for part_count in range(1, min(3, total) + 1):
            for lengths in compositions(total, part_count):
                weight_ranges = [range(length // 2 + 1) for length in lengths]
                for weights in product(*weight_ranges):
                    threshold = profile_threshold(lengths, weights)
                    for kappa in kappas:
                        if threshold <= kappa * total - 1:
                            continue
                        high = [
                            index
                            for index, (length, weight) in enumerate(zip(lengths, weights))
                            if weight and Fraction(weight, length) >= kappa / 2
                        ]
                        supplied = sum(lengths[index] - 1 for index in high)
                        required_supply = (kappa * total / 2).numerator // (
                            kappa * total / 2
                        ).denominator
                        require(supplied >= required_supply, "high-density operation supply")

                        steps = [
                            step
                            for index in high
                            for step in trajectory(lengths[index], weights[index])
                        ]
                        delta = min(kappa * kappa / 4, Fraction(1, 6))
                        require(all(drop >= delta for drop, _, _ in steps), "profile drop floor")
                        for distance in range(ceil_fraction(kappa * total), total + 1):
                            if Fraction(distance) - threshold >= 1:
                                continue
                            deficit = max(Fraction(0), threshold - distance)
                            nu = ceil_fraction((deficit + 1) / delta)
                            if nu > required_supply:
                                continue
                            require(nu <= len(steps), "adaptive trajectory availability")
                            total_drop = sum((step[0] for step in steps[:nu]), Fraction(0))
                            total_retention = product_fraction(step[1] for step in steps[:nu])
                            require(total_drop >= deficit + 1, "adaptive accumulated drop")
                            require(total_retention >= Fraction(1, 2**nu), "adaptive retention")
                            require(threshold - total_drop <= distance - 1, "adaptive Plotkin gap")
                            profile_checks += 4
                            adaptive_payment_cases += 1
                        profile_checks += 2
    return state_checks, profile_checks, complement_checks, adaptive_payment_cases


def product_fraction(values: Iterable[Fraction]) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def verify_targeted_adaptive_payment() -> int:
    """Exercise Theorem 3 on a nonvacuous admissible code fixture."""
    total = 512
    weight = 256
    distance = 128
    kappa = Fraction(distance, total)
    threshold = Fraction(weight * (total - weight), total)
    delta = min(kappa * kappa / 4, Fraction(1, 6))
    deficit = max(Fraction(0), threshold - distance)
    nu = ceil_fraction((deficit + 1) / delta)
    supply = (kappa * total / 2).numerator // (kappa * total / 2).denominator

    left = (1 << weight) - 1
    right = ((1 << 128) - 1) | (((1 << 128) - 1) << 256)
    family = (left, right)
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        require(condition, message)
        checks += 1

    check(all(word.bit_count() == weight for word in family), "targeted profile")
    check(johnson_distance(left, right) == distance, "targeted Johnson distance")
    check(threshold == distance, "targeted equality threshold")
    check(distance >= kappa * total, "targeted linear-distance gate")
    check(nu == 64, "targeted shortening count")
    check(supply == 64 and nu <= supply, "targeted operation supply")

    steps = trajectory(total, weight)
    selected = steps[:nu]
    total_drop = sum((step[0] for step in selected), Fraction(0))
    total_retention = product_fraction(step[1] for step in selected)
    check(len(selected) == nu, "targeted trajectory availability")
    check(all(drop >= delta for drop, _, _ in selected), "targeted drop floor")
    check(total_drop >= deficit + 1, "targeted accumulated drop")
    check(total_retention >= Fraction(1, 2**nu), "targeted retention")
    check(threshold - total_drop <= distance - 1, "targeted Plotkin gap")
    check(len(family) <= total * 2**nu, "targeted adaptive code bound")
    return checks


def verify_variance_and_fixed_blocks(max_n: int) -> tuple[int, int]:
    variance_checks = 0
    limit = min(max_n, 14)
    for total in range(2, limit + 1):
        for part_count in range(1, min(4, total) + 1):
            for lengths in compositions(total, part_count):
                for weights in product(*(range(length + 1) for length in lengths)):
                    weight = sum(weights)
                    global_threshold = Fraction(weight * (total - weight), total)
                    local_threshold = profile_threshold(lengths, weights)
                    theta = Fraction(weight, total)
                    variance = sum(
                        (length * (Fraction(local_weight, length) - theta) ** 2
                         for length, local_weight in zip(lengths, weights)),
                        Fraction(0),
                    )
                    require(global_threshold - local_threshold == variance, "variance identity")
                    variance_checks += 1

    fixed_checks = 0
    for total in range(2, min(max_n, 40) + 1):
        for weight in range(total + 1):
            global_threshold = Fraction(weight * (total - weight), total)
            for forced_one in range(weight + 1):
                for forced_zero in range(total - weight + 1):
                    remaining = total - forced_one - forced_zero
                    if remaining == 0:
                        continue
                    residual = Fraction(
                        (weight - forced_one) * (total - weight - forced_zero),
                        remaining,
                    )
                    difference = Fraction(
                        forced_zero * weight * (weight - forced_one)
                        + forced_one * (total - weight) * (total - weight - forced_zero),
                        total * remaining,
                    )
                    require(global_threshold - residual == difference, "fixed-block identity")
                    fixed_checks += 1
    return variance_checks, fixed_checks


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise VerificationError("primitive root not found")


def endpoint_columns(n: int, prime: int, depth: int, shift: int) -> list[tuple[int, ...]]:
    zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
    points = [pow(zeta, index, prime) for index in range(n)]
    exponents = [(shift + offset) % n for offset in range(depth)]
    return [tuple(pow(point, exponent, prime) for exponent in exponents) for point in points]


def local_profile(mask: int, blocks: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(sum((mask >> coordinate) & 1 for coordinate in block) for block in blocks)


def verify_endpoint_fixtures() -> tuple[int, int, dict[str, int]]:
    families_checked = 0
    pair_checks = 0
    bound_checks = {
        "unshortened": 0,
        "equality": 0,
        "one_block": 0,
        "adaptive": 0,
    }
    for n, prime in ((4, 5), (8, 17), (8, 41)):
        partitions = (
            (tuple(range(n)),),
            (tuple(range(n // 2)), tuple(range(n // 2, n))),
            (tuple(range(0, n, 2)), tuple(range(1, n, 2))),
            ((0,), tuple(range(1, n))),
        )
        for weight in range(1, n):
            supports = [sum(1 << coordinate for coordinate in support) for support in combinations(range(n), weight)]
            for depth in range(1, n // 2 + 1):
                endpoints = (
                    (0, depth),
                    (1, depth + 1),
                    ((1 - depth) % n, depth),
                    ((-depth) % n, depth + 1),
                )
                for shift, distance in endpoints:
                    columns = endpoint_columns(n, prime, depth, shift)
                    for blocks in partitions:
                        fibers: dict[tuple[tuple[int, ...], tuple[int, ...]], list[int]] = defaultdict(list)
                        for mask in supports:
                            syndrome = tuple(
                                sum(columns[coordinate][row] for coordinate in range(n) if (mask >> coordinate) & 1) % prime
                                for row in range(depth)
                            )
                            fibers[(syndrome, local_profile(mask, blocks))].append(mask)
                        lengths = tuple(map(len, blocks))
                        for (_, weights), family in fibers.items():
                            for left, right in combinations(family, 2):
                                require(johnson_distance(left, right) >= distance, "endpoint locator distance")
                                pair_checks += 1

                            balanced = tuple(min(local_weight, length - local_weight) for length, local_weight in zip(lengths, weights))
                            threshold = profile_threshold(lengths, balanced)
                            if Fraction(distance) - threshold >= 1:
                                require(len(family) <= distance <= n, "endpoint unshortened Plotkin bound")
                                bound_checks["unshortened"] += 1
                            elif distance == threshold:
                                rank_bound = sum(length - 1 for length, q in zip(lengths, balanced) if q)
                                require(len(family) <= 2 * rank_bound, "endpoint equality bound")
                                bound_checks["equality"] += 1

                            for index, (length, q) in enumerate(zip(lengths, balanced)):
                                if not q:
                                    continue
                                for u in range(length - q + 1):
                                    shortened = threshold - Fraction(q * q * u, length * (length - u))
                                    if distance <= shortened:
                                        continue
                                    retention = Fraction(comb(length - u, q), comb(length, q))
                                    bound = Fraction(distance, 1) / (distance - shortened) / retention
                                    require(len(family) <= bound, "endpoint one-block bound")
                                    bound_checks["one_block"] += 1

                            kappa = Fraction(distance, n)
                            delta = min(kappa * kappa / 4, Fraction(1, 6))
                            deficit = max(Fraction(0), threshold - distance)
                            nu = ceil_fraction((deficit + 1) / delta)
                            if Fraction(distance) - threshold < 1 and nu <= distance // 2:
                                require(len(family) <= n * 2**nu, "endpoint adaptive bound")
                                bound_checks["adaptive"] += 1
                            families_checked += 1
    return families_checked, pair_checks, bound_checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact checks")
    parser.add_argument(
        "--max-n",
        type=int,
        default=48,
        help="check one-block and dynamic arithmetic through this length (default: 48)",
    )
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")
    if not 16 <= args.max_n <= 128:
        parser.error("--max-n must lie between 16 and 128")

    shortening = verify_shortening(args.max_n)
    equality, equality_words = verify_equality_gram()
    adaptive_states, adaptive_profiles, complements, adaptive_cases = verify_adaptive(
        args.max_n
    )
    targeted_adaptive = verify_targeted_adaptive_payment()
    variance, fixed_blocks = verify_variance_and_fixed_blocks(args.max_n)
    endpoint_families, endpoint_pairs, endpoint_bounds = verify_endpoint_fixtures()
    total = sum(
        (
            shortening,
            equality,
            adaptive_states,
            adaptive_profiles,
            targeted_adaptive,
            variance,
            fixed_blocks,
            endpoint_families,
            endpoint_pairs,
            sum(endpoint_bounds.values()),
        )
    )
    print(f"shortening_checks={shortening}")
    print(f"equality_gram_checks={equality}")
    print(f"equality_fixture_words={equality_words}")
    print(f"adaptive_state_checks={adaptive_states}")
    print(f"adaptive_profile_checks={adaptive_profiles}")
    print(f"sampled_adaptive_payment_cases={adaptive_cases}")
    print(f"targeted_adaptive_payment_cases=1")
    print(f"targeted_adaptive_payment_checks={targeted_adaptive}")
    print(f"dynamic_complements_seen={complements}")
    print(f"variance_identity_checks={variance}")
    print(f"fixed_block_identity_checks={fixed_blocks}")
    print(f"endpoint_profile_families={endpoint_families}")
    print(f"endpoint_pair_checks={endpoint_pairs}")
    for name in ("unshortened", "equality", "one_block", "adaptive"):
        print(f"endpoint_{name}_bound_checks={endpoint_bounds[name]}")
    print(f"RESULT: PASS (work_items={total})")


if __name__ == "__main__":
    main()
