#!/usr/bin/env python3
"""Verify the finite algebra in the asymptotic C9 radial-shell route cut.

This script is self-contained and uses only the Python standard library.
Every gate raises explicitly; Python's -O flag cannot remove the checks.
"""

from __future__ import annotations

import itertools
import math
from collections import Counter
from fractions import Fraction


class VerificationError(RuntimeError):
    """Raised when an explicit verification gate fails."""


class Checker:
    def __init__(self) -> None:
        self.count = 0

    def check(self, condition: bool, message: str) -> None:
        self.count += 1
        if not condition:
            raise VerificationError(message)


def binom(n: int, k: int) -> int:
    return 0 if k < 0 or k > n else math.comb(n, k)


def weight(word: tuple[int, ...]) -> int:
    return sum(value != 0 for value in word)


def hamming(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a != b for a, b in zip(left, right))


def prime_factors(value: int) -> tuple[int, ...]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return tuple(factors)


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // q, p) != 1 for q in factors):
            return candidate
    raise VerificationError(f"no primitive root found modulo {p}")


def krawtchouk(n: int, p: int, j: int, t: int) -> int:
    return sum(
        ((-1) ** ell)
        * ((p - 1) ** (j - ell))
        * binom(t, ell)
        * binom(n - t, j - ell)
        for ell in range(j + 1)
    )


def mds_weight_enumerator(n: int, p: int, distance: int) -> tuple[int, ...]:
    values = [0] * (n + 1)
    values[0] = 1
    for w in range(distance, n + 1):
        values[w] = binom(n, w) * sum(
            ((-1) ** ell)
            * binom(w, ell)
            * (p ** (w - distance + 1 - ell) - 1)
            for ell in range(w - distance + 1)
        )
    return tuple(values)


def endpoint_matrix(n: int, p: int, d: int) -> tuple[tuple[int, ...], ...]:
    if (p - 1) % n:
        raise VerificationError(f"N={n} does not divide p-1={p - 1}")
    zeta = pow(primitive_root(p), (p - 1) // n, p)
    return tuple(
        tuple(pow(zeta, row * column, p) for column in range(n))
        for row in range(d)
    )


def determinant_mod_p(matrix: tuple[tuple[int, ...], ...], p: int) -> int:
    rows = [list(row) for row in matrix]
    det = 1
    for column in range(len(rows)):
        pivot = next(
            (row for row in range(column, len(rows)) if rows[row][column] % p),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            det = -det
        pivot_value = rows[column][column] % p
        det = (det * pivot_value) % p
        inverse = pow(pivot_value, p - 2, p)
        for row in range(column + 1, len(rows)):
            factor = rows[row][column] * inverse % p
            for col in range(column, len(rows)):
                rows[row][col] = (rows[row][col] - factor * rows[column][col]) % p
    return det % p


def kernel_words(
    matrix: tuple[tuple[int, ...], ...], p: int
) -> tuple[tuple[int, ...], ...]:
    n = len(matrix[0])
    return tuple(
        word
        for word in itertools.product(range(p), repeat=n)
        if all(sum(a * b for a, b in zip(row, word)) % p == 0 for row in matrix)
    )


def row_span(
    matrix: tuple[tuple[int, ...], ...], p: int
) -> tuple[tuple[int, ...], ...]:
    n = len(matrix[0])
    words = {
        tuple(
            sum(coefficient * matrix[row][column] for row, coefficient in enumerate(coefficients)) % p
            for column in range(n)
        )
        for coefficients in itertools.product(range(p), repeat=len(matrix))
    }
    return tuple(sorted(words))


def enumerator(words: tuple[tuple[int, ...], ...], n: int) -> tuple[int, ...]:
    counts = Counter(weight(word) for word in words)
    return tuple(counts.get(t, 0) for t in range(n + 1))


def inner_distribution(family: tuple[tuple[int, ...], ...]) -> tuple[Fraction, ...]:
    n = len(family[0])
    counts = Counter(hamming(left, right) for left in family for right in family)
    return tuple(Fraction(counts.get(t, 0), len(family)) for t in range(n + 1))


def binary_word(n: int, support: tuple[int, ...]) -> tuple[int, ...]:
    support_set = set(support)
    return tuple(int(index in support_set) for index in range(n))


def greedy_constant_weight(n: int, m: int, d: int) -> tuple[tuple[int, ...], ...]:
    selected: list[tuple[int, ...]] = []
    for support in itertools.combinations(range(n), m):
        word = binary_word(n, support)
        if all(hamming(word, prior) >= 2 * d for prior in selected):
            selected.append(word)
    return tuple(selected)


def check_endpoint_windows(checker: Checker) -> None:
    for r in (2, 3, 4):
        cases = ((0, r), (1 - r, r), (1, r + 1), (-r, r + 1))
        for a, expected_d in cases:
            frequencies = set(range(a, a + r)) | {0}
            checker.check(
                len(frequencies) == expected_d,
                f"endpoint frequency count failed for R={r}, a={a}",
            )
            ordered = sorted(frequencies)
            checker.check(
                ordered == list(range(ordered[0], ordered[0] + expected_d)),
                f"endpoint frequencies are not consecutive for R={r}, a={a}",
            )


def check_character_normalization(checker: Checker) -> None:
    n, p = 4, 5
    vectors = tuple(itertools.product(range(p), repeat=n))
    for t in range(n + 1):
        difference = (1,) * t + (0,) * (n - t)
        for j in range(n + 1):
            residue_counts = [0] * p
            for vector in vectors:
                if weight(vector) == j:
                    residue = sum(a * b for a, b in zip(vector, difference)) % p
                    residue_counts[residue] += 1
            expected = krawtchouk(n, p, j, t)
            checker.check(
                all(residue_counts[0] - expected == residue_counts[r] for r in range(1, p)),
                f"character/Krawtchouk normalization failed at t={t}, j={j}",
            )


def check_coset_floor(
    checker: Checker,
    family: tuple[tuple[int, ...], ...],
    dual_enumerator: tuple[int, ...],
    p: int,
) -> None:
    n = len(family[0])
    distribution = inner_distribution(family)
    for j in range(n + 1):
        lhs = sum(distribution[t] * krawtchouk(n, p, j, t) for t in range(n + 1))
        rhs = len(family) * dual_enumerator[j]
        checker.check(lhs >= rhs, f"coset floor failed at j={j}: {lhs} < {rhs}")


def check_small_endpoint_codes(checker: Checker) -> list[tuple[int, int, int]]:
    fixtures = [(4, 5, 1), (4, 5, 2), (6, 7, 2)]
    for n, p, d in fixtures:
        matrix = endpoint_matrix(n, p, d)
        for columns in itertools.combinations(range(n), d):
            minor = tuple(tuple(row[column] for column in columns) for row in matrix)
            checker.check(
                determinant_mod_p(minor, p) != 0,
                f"zero Vandermonde minor for {(n, p, d)}, columns={columns}",
            )
        code = kernel_words(matrix, p)
        dual = row_span(matrix, p)
        code_enum = enumerator(code, n)
        dual_enum = enumerator(dual, n)
        checker.check(len(code) == p ** (n - d), f"wrong code size for {(n, p, d)}")
        checker.check(len(dual) == p**d, f"wrong dual size for {(n, p, d)}")
        checker.check(
            min(weight(word) for word in code if any(word)) == d + 1,
            f"wrong code distance for {(n, p, d)}",
        )
        checker.check(
            min(weight(word) for word in dual if any(word)) == n - d + 1,
            f"wrong dual distance for {(n, p, d)}",
        )
        checker.check(
            code_enum == mds_weight_enumerator(n, p, d + 1),
            f"code enumerator is not MDS for {(n, p, d)}",
        )
        checker.check(
            dual_enum == mds_weight_enumerator(n, p, n - d + 1),
            f"dual enumerator is not MDS for {(n, p, d)}",
        )
        sample = tuple(code[index] for index in range(min(9, len(code))))
        check_coset_floor(checker, sample, dual_enum, p)
    return fixtures


def check_printed_package(
    checker: Checker, n: int, p: int, d: int, m: int, expected_size: int
) -> dict[str, int]:
    family = greedy_constant_weight(n, m, d)
    checker.check(len(family) == expected_size, f"unexpected greedy size for {(n, m, d)}")
    checker.check(all(weight(word) == m for word in family), "constant-weight gate failed")
    checker.check(
        all(hamming(left, right) >= 2 * d for index, left in enumerate(family) for right in family[index + 1 :]),
        f"distance gate failed for {(n, m, d)}",
    )
    distribution = inner_distribution(family)
    code_enum = mds_weight_enumerator(n, p, d + 1)
    dual_enum = mds_weight_enumerator(n, p, n - d + 1)
    checker.check(distribution[0] == 1, "A_0 normalization failed")
    checker.check(sum(distribution) == len(family), "inner-distribution mass failed")
    for t in range(n + 1):
        checker.check(distribution[t] >= 0, f"negative A_{t}")
        if code_enum[t] == 0:
            checker.check(distribution[t] == 0, f"MDS support failed at t={t}")
        checker.check(distribution[t] <= code_enum[t], f"MDS shell cap failed at t={t}")
        if 0 < t < 2 * d:
            checker.check(distribution[t] == 0, f"distance support failed at t={t}")
    for j in range(n + 1):
        lhs = sum(distribution[t] * krawtchouk(n, p, j, t) for t in range(n + 1))
        checker.check(lhs >= 0, f"ambient Delsarte positivity failed at j={j}")
        checker.check(
            lhs >= len(family) * dual_enum[j],
            f"RM_{j} floor failed for greedy fixture {(n, p, d, m)}",
        )
    return {"N": n, "p": p, "D": d, "m": m, "J": len(family)}


def check_finite_bound_fixture(checker: Checker) -> dict[str, int]:
    n, p, d = 8, 257, 2
    checker.check((p - 1) % n == 0, "finite fixture divisibility failed")
    checker.check(2 ** (n + 1) <= (p - 1) ** (d + 1), "finite RM condition one failed")
    checker.check(
        Fraction(2 ** (n + 1) * (p**d), (p - 1) ** d) <= (p - 1) ** (n - d),
        "finite RM condition two failed",
    )
    checker.check(p ** (d - 1) > 2**n, "finite shell-cap condition failed")
    dual_enum = mds_weight_enumerator(n, p, n - d + 1)
    code_enum = mds_weight_enumerator(n, p, d + 1)
    for r in range(1, d + 1):
        j = n - d + r
        checker.check(
            dual_enum[j] <= binom(n, j) * (p**r),
            f"shortened-dual bound failed at j={j}",
        )
        for t in range(2 * d, n + 1):
            checker.check(
                abs(krawtchouk(n, p, j, t))
                <= binom(n, j) * ((p - 1) ** (j - d - r)),
                f"off-diagonal Krawtchouk bound failed at j={j}, t={t}",
            )
    for t in range(2 * d, n + 1):
        support_lower = binom(n, t) * (p - t) * (p ** (t - d - 1))
        checker.check(code_enum[t] >= support_lower, f"support lower bound failed at t={t}")
        checker.check(code_enum[t] > 2**n, f"finite shell cap is not inactive at t={t}")
    return {"N": n, "p": p, "D": d}


def main() -> None:
    checker = Checker()
    check_endpoint_windows(checker)
    check_character_normalization(checker)
    endpoint_fixtures = check_small_endpoint_codes(checker)
    greedy_fixtures = [
        check_printed_package(checker, 4, 5, 1, 2, 6),
        check_printed_package(checker, 6, 7, 2, 3, 4),
        check_printed_package(checker, 8, 17, 2, 4, 14),
    ]
    finite_fixture = check_finite_bound_fixture(checker)
    print(f"RESULT: PASS ({checker.count} explicit checks)")
    print(f"endpoint code fixtures: {endpoint_fixtures}")
    print(f"greedy package fixtures: {greedy_fixtures}")
    print(f"finite sufficient-bound fixture: {finite_fixture}")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as error:
        raise SystemExit(f"RESULT: FAIL: {error}") from error
