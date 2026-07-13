#!/usr/bin/env python3
"""Exact F_101 replay of the one-deeper prefix anti-host compiler."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product


P = 101
D = tuple(range(1, 9))
N_DOMAIN = len(D)
K = 3
M = 4
S_DEPTH = M - K


def fail(message: str) -> None:
    raise RuntimeError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def inv(value: int) -> int:
    value %= P
    check(value != 0, "division by zero")
    return pow(value, P - 2, P)


def trim(poly: list[int]) -> list[int]:
    result = [value % P for value in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_eval(poly: list[int], x: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % P
    return value


def poly_add(left: list[int], right: list[int], scale: int = 1) -> list[int]:
    size = max(len(left), len(right))
    result = [0] * size
    for index in range(size):
        a = left[index] if index < len(left) else 0
        b = right[index] if index < len(right) else 0
        result[index] = (a + scale * b) % P
    return trim(result)


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % P
    return trim(result)


def locator(support: tuple[int, ...]) -> list[int]:
    result = [1]
    for root in support:
        result = poly_mul(result, [(-root) % P, 1])
    return result


def divide_by_x_minus_alpha(poly: list[int], alpha: int) -> list[int]:
    remainder = [value % P for value in poly]
    check(len(remainder) >= 2, "linear division needs positive degree")
    quotient = [0] * (len(remainder) - 1)
    for degree in range(len(remainder) - 1, 0, -1):
        quotient[degree - 1] = remainder[degree]
        remainder[degree - 1] = (
            remainder[degree - 1] + alpha * quotient[degree - 1]
        ) % P
        remainder[degree] = 0
    check(remainder[0] == 0, "polynomial is not divisible by X-alpha")
    return trim(quotient)


def linear_system_consistent(matrix: list[list[int]], rhs: list[int]) -> bool:
    augmented = [
        [entry % P for entry in row] + [value % P]
        for row, value in zip(matrix, rhs)
    ]
    rows = len(augmented)
    columns = len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if augmented[row][column] % P),
            None,
        )
        if pivot is None:
            continue
        augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        scale = inv(augmented[pivot_row][column])
        augmented[pivot_row] = [(entry * scale) % P for entry in augmented[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = augmented[row][column] % P
            if factor:
                augmented[row] = [
                    (a - factor * b) % P
                    for a, b in zip(augmented[row], augmented[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return not any(
        all(row[column] % P == 0 for column in range(columns))
        and row[columns] % P != 0
        for row in augmented
    )


def degree_lt_interpolant_exists(
    xs: tuple[int, ...], ys: tuple[int, ...], degree: int
) -> bool:
    matrix = [[pow(x, power, P) for power in range(degree)] for x in xs]
    return linear_system_consistent(matrix, list(ys))


def main() -> None:
    check(S_DEPTH == 1, "unexpected prefix depth")
    check(M * M - N_DOMAIN * (K - 1) == 0, "test instance should have J=0")

    fibers: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for support in combinations(D, M):
        q_support = locator(support)
        prefix = q_support[M - 1]
        fibers[prefix].append(support)
    prefix, family = max(fibers.items(), key=lambda item: (len(item[1]), -item[0]))
    check(prefix == (-18) % P, "unexpected largest prefix")
    check(len(family) == 8, "unexpected largest fiber size")
    n_slopes = len(family)

    u = [0] * (M + 1)
    u[M] = 1
    u[M - 1] = prefix
    p_polys = [poly_add(u, locator(support), scale=-1) for support in family]
    check(all(len(poly) - 1 <= K - 1 for poly in p_polys), "prefix cancellation failed")

    extension_gate = max(
        N_DOMAIN + (K - 1) * (n_slopes * (n_slopes - 1) // 2),
        1 + (N_DOMAIN - M) * n_slopes,
    )
    check(P > extension_gate, "F_101 does not satisfy the extension gate")

    alpha = None
    slopes: list[int] = []
    for candidate in range(P):
        if candidate in D:
            continue
        candidate_slopes = [poly_eval(poly, candidate) for poly in p_polys]
        if len(set(candidate_slopes)) == n_slopes:
            alpha = candidate
            slopes = candidate_slopes
            break
    check(alpha is not None, "no separating pole found")

    theta = None
    for candidate in range(1, P):
        valid = True
        for support, gamma in zip(family, slopes):
            support_set = set(support)
            for x in D:
                if x not in support_set:
                    factor = (inv(x - alpha) + candidate * gamma) % P
                    if factor == 0:
                        valid = False
                        break
            if not valid:
                break
        if valid:
            theta = candidate
            break
    check(theta is not None, "no twist scalar found")

    r0 = {x: poly_eval(u, x) * inv(x - alpha) % P for x in D}
    r1 = {
        x: (theta * poly_eval(u, x) - inv(x - alpha)) % P
        for x in D
    }

    exact_checks = 0
    for support, p_support, gamma in zip(family, p_polys, slopes):
        numerator = p_support[:]
        numerator[0] = (numerator[0] - poly_eval(p_support, alpha)) % P
        quotient = divide_by_x_minus_alpha(numerator, alpha)
        h = poly_add(quotient, p_support, scale=theta * gamma)
        check(len(h) - 1 < K, "explaining polynomial exceeds degree")
        agreement = tuple(
            x
            for x in D
            if (r0[x] + gamma * r1[x] - poly_eval(h, x)) % P == 0
        )
        check(agreement == support, f"agreement set mismatch for {support}")
        explained_r1 = degree_lt_interpolant_exists(
            support,
            tuple(r1[x] for x in support),
            K,
        )
        check(not explained_r1, f"direction is explained on {support}")
        exact_checks += len(D)

    gamma_set = set(slopes)
    challenge = set(range(10))
    intersections = [
        len({(gamma - delta) % P for gamma in gamma_set} & challenge)
        for delta in range(P)
    ]
    check(sum(intersections) == n_slopes * len(challenge), "translation average mismatch")
    lower = (n_slopes * len(challenge) + P - 1) // P
    check(max(intersections) >= lower, "challenge restriction lower bound failed")

    admissible_denominators = 0
    host_solutions = 0
    for degree in (1, 2):
        for lower_coefficients in product(range(P), repeat=degree):
            l_poly = list(lower_coefficients) + [1]
            if any(poly_eval(l_poly, x) == 0 for x in D):
                continue
            admissible_denominators += 1
            matrix = []
            rhs = []
            for x in D:
                l_value = poly_eval(l_poly, x)
                matrix.append(
                    [l_value * pow(x, power, P) % P for power in range(K)]
                    + [(-pow(x, power, P)) % P for power in range(degree)]
                )
                rhs.append(l_value * r1[x] % P)
            if linear_system_consistent(matrix, rhs):
                host_solutions += 1
    check(admissible_denominators == 9_514, "admissible denominator census mismatch")
    check(host_solutions == 0, "rational-host presentation found")

    print("ONE_DEEPER_PREFIX_ANTI_HOST_COMPILER")
    print(
        "parameters="
        f"p={P},n={N_DOMAIN},k={K},m={M},s={S_DEPTH},J=0,N={n_slopes}"
    )
    print(f"prefix={prefix},alpha={alpha},theta={theta}")
    print(f"slopes={','.join(str(value) for value in sorted(slopes))}")
    print(f"exact_agreement_coordinate_checks={exact_checks}")
    print(
        "challenge_translation="
        f"sum={sum(intersections)},max={max(intersections)},ceil_lower={lower}"
    )
    print(
        "anti_host="
        f"admissible_monic_denominators={admissible_denominators},solutions={host_solutions}"
    )
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
