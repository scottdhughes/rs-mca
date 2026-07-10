#!/usr/bin/env python3
"""Finite checks for near-norm-gate first-failure remainder packing.

Coverage is exhaustive for every one-sided mask and cyclic interval at n=4.
The n=8 and n=16 rows are deterministic samples.  The proof in the companion
note is symbolic; these scans are regression and arithmetic checks only.
"""

from __future__ import annotations

import argparse
import random
from collections import defaultdict
from itertools import combinations, product


class CheckFailure(RuntimeError):
    """Raised when a verifier obligation fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


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
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise CheckFailure(f"no primitive root modulo {prime}")


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    if size == 1:
        return work[0][0]
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if work[row][pivot_index] != 0
                ),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                require(
                    numerator % previous == 0,
                    "Bareiss division was not exact",
                )
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def cyclotomic_resultant(coefficients: tuple[int, ...]) -> int:
    """Return Res(X^h+1,g) for deg(g)<h via the quotient algebra."""
    h = len(coefficients)
    matrix = [[0] * h for _ in range(h)]
    for column in range(h):
        for exponent, coefficient in enumerate(coefficients):
            target = exponent + column
            if target >= h:
                target -= h
                coefficient = -coefficient
            matrix[target][column] += coefficient
    return bareiss_determinant(matrix)


def evaluate_mod(coefficients: tuple[int, ...], value: int, prime: int) -> int:
    out = 0
    for coefficient in reversed(coefficients):
        out = (out * value + coefficient) % prime
    return out


def cyclic_interval(start: int, length: int, modulus: int) -> tuple[int, ...]:
    return tuple((start + offset) % modulus for offset in range(length))


def split_interval(interval: tuple[int, ...], h: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    odd = tuple(((value - 1) // 2) % h for value in interval if value % 2)
    even = tuple((value // 2) % h for value in interval if value % 2 == 0)
    return odd, even


def is_cyclic_interval(values: tuple[int, ...], modulus: int) -> bool:
    if not values:
        return True
    target = set(values)
    return any(
        target == set(cyclic_interval(start, len(values), modulus))
        for start in range(modulus)
    )


def words_for_mask(mask: tuple[tuple[int, ...], ...]):
    yield from product(*mask)


def half_channels(word: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    h = len(word) // 2
    difference = tuple(word[i] - word[i + h] for i in range(h))
    total = tuple(word[i] + word[i + h] for i in range(h))
    return difference, total


def exact_remainder_bound(prime: int, q: int, h: int, width_square_sum: int) -> int:
    """Return floor(2V/(p^(2q/h)-2V)) using integer comparisons."""
    require(q > 0 and width_square_sum > 0, "packing bound needs q,V>0")
    require(
        2**h * prime ** (2 * q) > width_square_sum**h,
        "packing gate is not open",
    )
    candidate = 0
    while (
        (2 * (candidate + 1)) ** h * prime ** (2 * q)
        <= (width_square_sum * (candidate + 2)) ** h
    ):
        candidate += 1
    return candidate


def even_descent_levels(h: int, prime: int, e: int) -> tuple[int, int]:
    levels = 0
    scale = h
    max_levels = h.bit_length() - 2
    while levels < max_levels:
        inherited = e // (1 << (levels + 1))
        if inherited == 0:
            break
        if prime**inherited <= (2 * scale) ** (scale // 4):
            break
        levels += 1
        scale //= 2
    return levels, scale


def compatible_lifts(
    mask: tuple[tuple[int, ...], ...], difference: tuple[int, ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    h = len(difference)
    return tuple(
        tuple(
            (left, right)
            for left in mask[i]
            for right in mask[i + h]
            if left - right == difference[i]
        )
        for i in range(h)
    )


def validate_remainder_family(
    n: int,
    prime: int,
    zeta: int,
    mask: tuple[tuple[int, ...], ...],
    interval: tuple[int, ...],
    valid_words: list[tuple[int, ...]],
    exhaustive: bool,
) -> tuple[int, int, int, int]:
    h = n // 2
    eta = pow(zeta, 2, prime)
    odd, even = split_interval(interval, h)
    require(is_cyclic_interval(odd, h), "odd decimation is not cyclic")
    require(is_cyclic_interval(even, h), "even decimation is not cyclic")

    grouped: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    identity_checks = 0
    for word in valid_words:
        difference, total = half_channels(word)
        require(any(difference), "first-failure family contains a divisible word")
        for u in range(h):
            odd_root = zeta * pow(eta, u, prime) % prime
            require(
                evaluate_mod(word, odd_root, prime)
                == evaluate_mod(difference, odd_root, prime),
                "odd half-channel identity failed",
            )
            require(
                evaluate_mod(word, pow(eta, u, prime), prime)
                == evaluate_mod(total, pow(eta, u, prime), prime),
                "even half-channel identity failed",
            )
            identity_checks += 2
        grouped[difference].append(word)

    widths = tuple(max(values) - min(values) for values in mask)
    width_square_sum = sum(
        (widths[i] + widths[i + h]) ** 2 for i in range(h)
    )
    require(width_square_sum <= 4 * h, "V_A exceeds h")
    remainders = list(grouped)
    separation_checks = 0
    pair_source = [tuple(0 for _ in range(h)), *remainders]
    pairs = list(combinations(pair_source, 2))
    if not exhaustive and len(pairs) > 256:
        pairs = pairs[:128] + pairs[-128:]
    for left, right in pairs:
        delta = tuple(a - b for a, b in zip(left, right))
        require(any(delta), "distinct remainder pair collapsed")
        for u in odd:
            root = zeta * pow(eta, u, prime) % prime
            require(evaluate_mod(delta, root, prime) == 0, "lost common odd root")
        resultant = cyclotomic_resultant(delta)
        require(resultant != 0, "nonzero degree<h remainder has zero resultant")
        require(
            abs(resultant) % (prime ** len(odd)) == 0,
            "resultant lacks the inherited p-adic valuation",
        )
        energy = sum(value * value for value in delta)
        require(
            energy**h >= prime ** (2 * len(odd)),
            "resultant-energy separation failed",
        )
        separation_checks += 1

    points = [tuple(0 for _ in range(h)), *remainders]
    pair_energy = sum(
        sum((a - b) ** 2 for a, b in zip(left, right))
        for left, right in combinations(points, 2)
    )
    require(
        4 * pair_energy <= len(points) ** 2 * width_square_sum,
        "coordinatewise Popoviciu sum failed",
    )

    lift_checks = 0
    levels, terminal_scale = even_descent_levels(h, prime, len(even))
    for difference, family in grouped.items():
        lifts = compatible_lifts(mask, difference)
        require(all(lifts), "remainder has an empty compatible-lift coordinate")
        nu = sum(len(options) == 2 for options in lifts)
        require(
            all(len(options) <= 2 for options in lifts),
            "one-sided coordinate has more than two compatible lifts",
        )
        require(
            len(family) <= 2 ** max(nu - len(even), 0),
            "unconditional MDS lift ceiling failed",
        )
        require(
            len(family) <= 2**terminal_scale,
            "triggered even-descent ceiling failed",
        )
        base = family[0]
        for word in family:
            increment = tuple(word[i] - base[i] for i in range(h))
            require(
                increment
                == tuple(word[i + h] - base[i + h] for i in range(h)),
                "same-remainder increment does not match across halves",
            )
            for i, value in enumerate(increment):
                require(
                    value
                    in set(mask[i][j] - base[i] for j in range(len(mask[i])))
                    and value
                    in set(
                        mask[i + h][j] - base[i + h]
                        for j in range(len(mask[i + h]))
                    ),
                    "increment escaped its one-sided common mask",
                )
            for v in even:
                require(
                    evaluate_mod(increment, pow(eta, v, prime), prime) == 0,
                    "same-remainder compiler lost an even root",
                )
            lift_checks += 1

    q = len(odd)
    if (
        grouped
        and q
        and width_square_sum
        and 2**h * prime ** (2 * q) > width_square_sum**h
    ):
        bound = exact_remainder_bound(prime, q, h, width_square_sum)
        require(len(grouped) <= bound, "distinct-remainder packing bound failed")
        require(
            len(valid_words) <= bound * 2**terminal_scale,
            "paid first-failure family ceiling failed",
        )

    exercised_levels = levels if grouped else 0
    triggered_family = int(bool(grouped) and levels > 0)
    return (
        identity_checks,
        separation_checks,
        lift_checks,
        exercised_levels,
        triggered_family,
    )


def masks_for_row(n: int) -> tuple[list[tuple[tuple[int, ...], ...]], bool]:
    zero = (0,)
    plus = (0, 1)
    minus = (0, -1)
    alphabet = (zero, plus, minus)
    if n == 4:
        return [tuple(mask) for mask in product(alphabet, repeat=n)], True

    rng = random.Random(20260710 + n)
    masks: set[tuple[tuple[int, ...], ...]] = {
        (plus,) * n,
        (minus,) * n,
        tuple(plus if i % 2 == 0 else minus for i in range(n)),
        tuple(plus if i < n // 2 else minus for i in range(n)),
    }
    target = 48 if n == 8 else 20
    while len(masks) < target:
        if n == 16:
            active = set(rng.sample(range(n), 10))
            mask = tuple(rng.choice((plus, minus)) if i in active else zero for i in range(n))
        else:
            mask = tuple(rng.choice(alphabet) for _ in range(n))
        masks.add(mask)
    return sorted(masks), False


def intervals_for_row(n: int, exhaustive: bool) -> list[tuple[int, ...]]:
    if exhaustive:
        return [
            cyclic_interval(start, length, n)
            for start in range(n)
            for length in range(1, n + 1)
        ]
    lengths = (max(1, n // 4), n // 2, min(n, n // 2 + 1))
    starts = range(n) if n == 8 else (0, 1, 5, 9)
    return [cyclic_interval(start, length, n) for start in starts for length in lengths]


def verify_half_channel_packets() -> dict[str, int]:
    totals = defaultdict(int)
    for n, prime in ((4, 5), (8, 17), (16, 97)):
        zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
        masks, exhaustive = masks_for_row(n)
        intervals = intervals_for_row(n, exhaustive)
        for mask in masks:
            words = list(words_for_mask(mask))
            for interval in intervals:
                valid = [
                    word
                    for word in words
                    if all(
                        evaluate_mod(word, pow(zeta, root, prime), prime) == 0
                        for root in interval
                    )
                    and any(half_channels(word)[0])
                ]
                counts = validate_remainder_family(
                    n, prime, zeta, mask, interval, valid, exhaustive
                )
                totals["families"] += 1
                totals["nonempty_families"] += bool(valid)
                totals["identity_checks"] += counts[0]
                totals["separation_checks"] += counts[1]
                totals["lift_checks"] += counts[2]
                totals["exercised_descent_levels"] += counts[3]
                totals["nonempty_descent_families"] += counts[4]
        totals[f"n{n}_masks"] = len(masks)
        totals[f"n{n}_intervals"] = len(intervals)
    return dict(totals)


def syndrome(
    bits: int, n: int, prime: int, zeta: int, shift: int, depth: int
) -> tuple[int, ...]:
    return tuple(
        sum(pow(zeta, ((shift + j) * i) % n, prime) for i in range(n) if bits >> i & 1)
        % prime
        for j in range(depth)
    )


def first_failure_key(word: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    level = 0
    current = word
    while len(current) > 1:
        half = len(current) // 2
        if current[:half] != current[half:]:
            break
        current = current[:half]
        level += 1
    return level, current


def reconstruct_first_failure(level: int, reduced: tuple[int, ...]) -> tuple[int, ...]:
    word = reduced
    for _ in range(level):
        word = word + word
    return word


def verify_first_failure_decomposition() -> dict[str, int]:
    totals = defaultdict(int)
    cases = (
        (4, 5, 2, (0, 1, 3)),
        (8, 17, 3, (0, 2, 7)),
        (8, 17, 4, (1, 5)),
        (16, 97, 8, (0, 1, 5)),
    )
    for n, prime, depth, shifts in cases:
        zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
        for shift in shifts:
            fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
            for bits in range(1 << n):
                fibers[syndrome(bits, n, prime, zeta, shift, depth)].append(bits)
            maximum = max(map(len, fibers.values()))
            if depth == n // 2:
                require(maximum <= 4 * n + 4, "half-window finite ceiling failed")
            for family in fibers.values():
                base_bits = family[0]
                seen: set[tuple[int, tuple[int, ...]]] = set()
                totals["nontrivial_fibers"] += len(family) > 1
                for family_index, bits in enumerate(family):
                    word = tuple(
                        ((bits >> i) & 1) - ((base_bits >> i) & 1)
                        for i in range(n)
                    )
                    for root in cyclic_interval(shift, depth, n):
                        require(
                            evaluate_mod(word, pow(zeta, root, prime), prime) == 0,
                            "fiber difference lost a root",
                        )
                    key = first_failure_key(word)
                    require(key not in seen, "first-failure key is not injective")
                    seen.add(key)
                    require(
                        reconstruct_first_failure(*key) == word,
                        "first-failure reconstruction failed",
                    )
                    totals["reconstruction_smoke_checks"] += 1
                    totals["nonbase_reconstruction_checks"] += family_index > 0
                totals["fibers"] += 1
            totals["maps"] += 1
            totals["maximum_fiber_sum"] += maximum
    return dict(totals)


def verify_scale_arithmetic() -> int:
    checks = 0
    for h in (2, 4, 8, 16, 32, 64, 128):
        for prime in (17, 97, 193, 257, 769):
            if (prime - 1) % (2 * h):
                continue
            for e in range(h + 1):
                levels, terminal = even_descent_levels(h, prime, e)
                require(terminal == h // (1 << levels), "wrong terminal scale")
                for level in range(levels):
                    scale = h // (1 << level)
                    inherited = e // (1 << (level + 1))
                    require(
                        prime**inherited > (2 * scale) ** (scale // 4),
                        "reported descent level does not satisfy its gate",
                    )
                    checks += 1
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run finite checks")
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")

    packet = verify_half_channel_packets()
    decomposition = verify_first_failure_decomposition()
    scale_checks = verify_scale_arithmetic()

    print("coverage_n4=exhaustive_masks_and_intervals")
    print("coverage_n8_n16=deterministic_samples")
    for key in sorted(packet):
        print(f"{key}={packet[key]}")
    for key in sorted(decomposition):
        print(f"{key}={decomposition[key]}")
    print(f"descent_gate_arithmetic_checks={scale_checks}")
    work_items = (
        packet["identity_checks"]
        + packet["separation_checks"]
        + packet["lift_checks"]
        + decomposition["nonbase_reconstruction_checks"]
        + scale_checks
    )
    print(f"RESULT: PASS (work_items={work_items})")


if __name__ == "__main__":
    main()
