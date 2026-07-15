#!/usr/bin/env python3
"""Exact mixed subset-product audit for first-interior BC modular fibers.

This verifier supports the root-free reduction in
bc_first_interior_modular_subset_product.md. It has three jobs.

1. Enumerate every 9-subset of mu_20 over F_41 and compare ordinary
   depth-three Q with mixed top-coefficient / quotient-algebra maps at the
   same monic rank three.
2. Realize one heaviest target in each quotient-algebra case as an actual
   first-interior weak-Popov modular fiber with fixed multiplier B=X and
   verify both determinant identities and every reconstructed census element.
3. Recompute the exact real nonempty-slice bounds and their least-integer
   ceilings at the two deployed MCA rows.

All arithmetic is exact and stdlib-only. The faithful-average toy has

    binom(20,9) / 41^3 = 167960 / 68921 > 2,

so its normalized spikes are not artifacts of an average below one.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
import json
import math


P = 41
N = 20
K = 7
M = 9
W = M - K
FIRST_INTERIOR = W + 2
OMEGA = N - M
SECOND_ROW_DEGREE = OMEGA - 1
SMALL_B = [0, 1]  # X


def trim(poly: list[int]) -> list[int]:
    poly = [x % P for x in poly]
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def degree(poly: list[int]) -> int:
    poly = trim(poly)
    return -1 if poly == [0] else len(poly) - 1


def padd(a: list[int], b: list[int]) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] = (out[i] + x) % P
    for i, x in enumerate(b):
        out[i] = (out[i] + x) % P
    return trim(out)


def pneg(a: list[int]) -> list[int]:
    return trim([(-x) % P for x in a])


def psub(a: list[int], b: list[int]) -> list[int]:
    return padd(a, pneg(b))


def pscale(a: list[int], scalar: int) -> list[int]:
    return trim([(scalar * x) % P for x in a])


def pmul(a: list[int], b: list[int]) -> list[int]:
    if trim(a) == [0] or trim(b) == [0]:
        return [0]
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return trim(out)


def pdivmod(a: list[int], b: list[int]) -> tuple[list[int], list[int]]:
    a = trim(a)
    b = trim(b)
    assert b != [0]
    if degree(a) < degree(b):
        return [0], a
    q = [0] * (degree(a) - degree(b) + 1)
    r = a[:]
    inv_lc = pow(b[-1], P - 2, P)
    while r != [0] and degree(r) >= degree(b):
        shift = degree(r) - degree(b)
        coeff = r[-1] * inv_lc % P
        q[shift] = coeff
        for i, x in enumerate(b):
            r[i + shift] = (r[i + shift] - coeff * x) % P
        r = trim(r)
    return trim(q), trim(r)


def pmod(a: list[int], b: list[int]) -> list[int]:
    return pdivmod(a, b)[1]


def pgcd(a: list[int], b: list[int]) -> list[int]:
    a, b = trim(a), trim(b)
    while b != [0]:
        a, b = b, pmod(a, b)
    if a == [0]:
        return [0]
    return pscale(a, pow(a[-1], P - 2, P))


def peval(poly: list[int], x: int) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x + coeff) % P
    return value


def monic_locator(roots: tuple[int, ...] | list[int]) -> list[int]:
    out = [1]
    for x in roots:
        out = pmul(out, [(-x) % P, 1])
    return out


def primitive_root(p: int) -> int:
    order = p - 1
    prime_factors = []
    t = order
    q = 2
    while q * q <= t:
        if t % q == 0:
            prime_factors.append(q)
            while t % q == 0:
                t //= q
        q += 1
    if t > 1:
        prime_factors.append(t)
    for g in range(2, p):
        if all(pow(g, order // q, p) != 1 for q in prime_factors):
            return g
    raise AssertionError("primitive root not found")


def first_irreducible_cubic() -> list[int]:
    for c0 in range(1, P):
        for c1 in range(P):
            for c2 in range(P):
                candidate = [c0, c1, c2, 1]
                if all(peval(candidate, x) != 0 for x in range(P)):
                    return candidate
    raise AssertionError("irreducible cubic not found")


def unit_count(d: int, distinct_factor_degrees: tuple[int, ...]) -> int:
    """Cardinality of the units of F[X]/W1."""
    value = Fraction(P**d, 1)
    for factor_degree in distinct_factor_degrees:
        value *= Fraction(P**factor_degree - 1, P**factor_degree)
    assert value.denominator == 1
    return value.numerator


def padded_remainder(poly: list[int], modulus: list[int]) -> tuple[int, ...]:
    d = degree(modulus)
    if d == 0:
        return ()
    rem = pmod(poly, modulus)
    return tuple(rem[i] if i < len(rem) else 0 for i in range(d))


def solve_linear_mod(matrix: list[list[int]], rhs: list[int]) -> list[int]:
    """Return the free-zero solution of a consistent system over F_P."""
    rows = [([x % P for x in row] + [b % P]) for row, b in zip(matrix, rhs)]
    nrows = len(rows)
    ncols = len(matrix[0])
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(ncols):
        found = next((r for r in range(pivot_row, nrows) if rows[r][col]), None)
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        inv = pow(rows[pivot_row][col], P - 2, P)
        rows[pivot_row] = [(inv * x) % P for x in rows[pivot_row]]
        for r in range(nrows):
            if r == pivot_row or rows[r][col] == 0:
                continue
            factor = rows[r][col]
            rows[r] = [
                (x - factor * y) % P
                for x, y in zip(rows[r], rows[pivot_row])
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == nrows:
            break
    for row in rows:
        if all(x == 0 for x in row[:ncols]):
            assert row[ncols] == 0, "inconsistent linear system"
    solution = [0] * ncols
    for r, col in enumerate(pivot_cols):
        solution[col] = rows[r][ncols]
    for row, b in zip(matrix, rhs):
        assert sum(x * y for x, y in zip(row, solution)) % P == b % P
    return solution


def determinant_completion(
    w1: list[int], n1: list[int], lambda_d: list[int]
) -> tuple[list[int], list[int]]:
    """Solve W1*N2-W2*N1=Lambda with the required second-row caps."""
    max_w2 = SECOND_ROW_DEGREE
    max_n2 = SECOND_ROW_DEGREE + K - 2
    n_w2 = max_w2 + 1
    n_n2 = max_n2 + 1
    matrix = [[0] * (n_w2 + n_n2) for _ in range(N + 1)]
    for j in range(n_w2):
        for i, coeff in enumerate(n1):
            if i + j <= N:
                matrix[i + j][j] = (matrix[i + j][j] - coeff) % P
    for j in range(n_n2):
        for i, coeff in enumerate(w1):
            if i + j <= N:
                col = n_w2 + j
                matrix[i + j][col] = (matrix[i + j][col] + coeff) % P
    rhs = [lambda_d[i] if i < len(lambda_d) else 0 for i in range(N + 1)]
    solution = solve_linear_mod(matrix, rhs)
    w2 = trim(solution[:n_w2])
    n2 = trim(solution[n_w2:])
    assert psub(pmul(w1, n2), pmul(w2, n1)) == trim(lambda_d)
    assert degree(w2) == SECOND_ROW_DEGREE
    assert degree(n2) <= max_n2
    return w2, n2


def realize_heaviest_fiber(
    case_name: str,
    w1: list[int],
    locator_indices: list[int],
    locators: list[list[int]],
    domain: list[int],
    lambda_d: list[int],
) -> dict[str, object]:
    """Build a genuine first-interior basis realizing one signature fiber."""
    v0 = locators[locator_indices[0]]
    n1 = pneg(pmul(SMALL_B, v0))
    assert pgcd(w1, n1) == [1]
    w2, n2 = determinant_completion(w1, n1, lambda_d)

    row1_degree = max(degree(w1), degree(n1) - (K - 1))
    row2_degree = max(degree(w2), degree(n2) - (K - 1))
    assert row1_degree == FIRST_INTERIOR
    assert degree(n1) - (K - 1) == FIRST_INTERIOR
    assert row2_degree == SECOND_ROW_DEGREE
    assert degree(w2) == SECOND_ROW_DEGREE
    assert row1_degree + row2_degree == N - K + 1

    received = {
        x: peval(n1, x) * pow(peval(w1, x), P - 2, P) % P
        for x in domain
    }
    verified = 0
    max_codeword_degree = -1
    for locator_index in locator_indices:
        v = locators[locator_index]
        codeword_num = pmul(SMALL_B, psub(v, v0))
        codeword, rem = pdivmod(codeword_num, w1)
        assert rem == [0]
        assert degree(codeword) < K
        max_codeword_degree = max(max_codeword_degree, degree(codeword))
        assert psub(pmul(w1, codeword), n1) == pmul(SMALL_B, v)

        a_num = psub(n2, pmul(w2, codeword))
        a_poly, rem = pdivmod(a_num, v)
        assert rem == [0]
        assert degree(a_poly) <= OMEGA - W - 2
        locator_w = padd(pmul(a_poly, w1), pmul(SMALL_B, w2))
        complement, rem = pdivmod(lambda_d, v)
        assert rem == [0]
        assert locator_w == complement
        numerator_n = padd(pmul(a_poly, n1), pmul(SMALL_B, n2))
        assert numerator_n == pmul(locator_w, codeword)

        roots = [x for x in domain if peval(v, x) == 0]
        assert len(roots) == M
        assert all(peval(codeword, x) == received[x] for x in roots)
        verified += 1

    return {
        "case": case_name,
        "fiber_size": verified,
        "W1": w1,
        "N1": n1,
        "W2": w2,
        "N2": n2,
        "profile": [row1_degree, row2_degree],
        "max_codeword_degree": max_codeword_degree,
        "determinant_ok": True,
        "gluing_ok": True,
    }


def deployed_nonempty_bounds() -> list[dict[str, object]]:
    rows = [
        ("KoalaBear", 2**31 - 2**24 + 1, 981104, 67471),
        ("Mersenne-31", 2**31 - 1, 981128, 67447),
    ]
    n = 2**21
    output = []
    for name, field_size, omega, w in rows:
        m = n - omega
        census = math.comb(n, m)
        strict_rank = w + 1
        strict_den = field_size**strict_rank
        full_den = strict_den * field_size
        strict_log2_average = math.log2(census) - math.log2(strict_den)
        full_log2_average = math.log2(census) - math.log2(full_den)
        strict_floor = (strict_den + census - 1) // census
        full_floor = (full_den + census - 1) // census
        output.append({
            "row": name,
            "field_size": field_size,
            "n": n,
            "m": m,
            "w": w,
            "strict_rank": strict_rank,
            "strict_log2_average": strict_log2_average,
            "strict_real_nonempty_bound_bits": -strict_log2_average,
            "strict_least_integer_overhead": strict_floor,
            "strict_integer_overhead_bits": math.log2(strict_floor),
            "full_rank": w + 2,
            "full_log2_average": full_log2_average,
            "full_real_nonempty_bound_bits": -full_log2_average,
            "full_least_integer_overhead": full_floor,
            "full_integer_overhead_bits": math.log2(full_floor),
        })
    return output


def verify_subunit_collision() -> dict[str, object]:
    """Verify an exact three-element rank-one fiber at average below one."""
    modulus = 101

    def mul(a: list[int], b: list[int]) -> list[int]:
        out = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % modulus
        while len(out) > 1 and out[-1] == 0:
            out.pop()
        return out

    def locator(roots: tuple[int, ...]) -> list[int]:
        out = [1]
        for x in roots:
            out = mul(out, [(-x) % modulus, 1])
        return out

    def sub(a: list[int], b: list[int]) -> list[int]:
        return padd_mod(a, [(-x) % modulus for x in b], modulus)

    def divmod_poly(a: list[int], b: list[int]) -> tuple[list[int], list[int]]:
        a = [x % modulus for x in a]
        b = [x % modulus for x in b]
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        while len(b) > 1 and b[-1] == 0:
            b.pop()
        assert b != [0]
        if len(a) < len(b):
            return [0], a
        quotient = [0] * (len(a) - len(b) + 1)
        inverse = pow(b[-1], modulus - 2, modulus)
        while a != [0] and len(a) >= len(b):
            shift = len(a) - len(b)
            coefficient = a[-1] * inverse % modulus
            quotient[shift] = coefficient
            for i, x in enumerate(b):
                a[i + shift] = (a[i + shift] - coefficient * x) % modulus
            while len(a) > 1 and a[-1] == 0:
                a.pop()
        while len(quotient) > 1 and quotient[-1] == 0:
            quotient.pop()
        return quotient, a

    n1 = [0, 0, 0, 7, -1]
    n1 = [x % modulus for x in n1]
    b_poly = [0, 1]
    expected_supports = ((0, 2, 5), (0, 3, 4), (1, 2, 4))
    realized_supports = []
    for support in combinations(range(6), 3):
        numerator = padd_mod(n1, mul(b_poly, locator(support)), modulus)
        if degree_mod(numerator, modulus) < 3:
            realized_supports.append(support)
    assert tuple(realized_supports) == expected_supports
    assert all(sum(support) == 7 for support in expected_supports)
    assert len(set(expected_supports[1]) - set(expected_supports[2])) == 2
    fiber_locators = [locator(support) for support in expected_supports]

    lambda_d = locator(tuple(range(6)))
    quotient, remainder = divmod_poly(lambda_d, n1)
    w2 = [(-x) % modulus for x in quotient]
    n2 = remainder
    determinant = sub(n2, mul(w2, n1))
    assert determinant == lambda_d
    assert max(0, degree_mod(n1, modulus) - 2) == 2
    assert max(degree_mod(w2, modulus), degree_mod(n2, modulus) - 2) == 2
    for v in fiber_locators:
        codeword = padd_mod(n1, mul(b_poly, v), modulus)
        a_num = sub(n2, mul(w2, codeword))
        a_poly, rem = divmod_poly(a_num, v)
        assert rem == [0] and degree_mod(a_poly, modulus) <= 1
        locator_w = padd_mod(a_poly, mul(b_poly, w2), modulus)
        complement, rem = divmod_poly(lambda_d, v)
        assert rem == [0] and locator_w == complement
        numerator_n = padd_mod(mul(a_poly, n1), mul(b_poly, n2), modulus)
        assert numerator_n == mul(locator_w, codeword)

    average = Fraction(math.comb(6, 3), modulus)
    assert average < 1
    return {
        "field": modulus,
        "domain": list(range(6)),
        "K": 3,
        "m": 3,
        "rank": 1,
        "supports": expected_supports,
        "fiber_size": len(expected_supports),
        "heuristic_average": [average.numerator, average.denominator],
        "exchange": 2,
        "profile": [2, 2],
        "W2": w2,
        "N2": n2,
        "determinant_ok": True,
    }


def padd_mod(a: list[int], b: list[int], modulus: int) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] = (out[i] + x) % modulus
    for i, x in enumerate(b):
        out[i] = (out[i] + x) % modulus
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def degree_mod(poly: list[int], modulus: int) -> int:
    poly = [x % modulus for x in poly]
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return -1 if poly == [0] else len(poly) - 1


def main() -> None:
    generator = primitive_root(P)
    zeta = pow(generator, (P - 1) // N, P)
    domain = [pow(zeta, i, P) for i in range(N)]
    assert len(set(domain)) == N
    lambda_d = [(-1) % P] + [0] * (N - 1) + [1]
    assert monic_locator(domain) == lambda_d

    outside = [x for x in range(1, P) if x not in set(domain)]
    assert len(outside) == 20
    a, b, c = outside[:3]
    irreducible_quadratic = [(-generator) % P, 0, 1]
    assert all(peval(irreducible_quadratic, x) != 0 for x in range(P))
    irreducible_cubic = first_irreducible_cubic()

    linear_a = [(-a) % P, 1]
    linear_b = [(-b) % P, 1]
    linear_c = [(-c) % P, 1]
    cases = [
        ("d0_Q_depth3", [1], ()),
        ("d1_linear_rootfree", linear_a, (1,)),
        ("d2_irreducible", irreducible_quadratic, (2,)),
        ("d2_split_distinct", pmul(linear_a, linear_b), (1, 1)),
        ("d2_repeated", pmul(linear_a, linear_a), (1,)),
        ("d3_irreducible", irreducible_cubic, (3,)),
        ("d3_linear_times_irreducible",
         pmul(linear_a, irreducible_quadratic), (1, 2)),
        ("d3_split_distinct", pmul(pmul(linear_a, linear_b), linear_c),
         (1, 1, 1)),
        ("d3_double_plus_linear", pmul(pmul(linear_a, linear_a), linear_b),
         (1, 1)),
        ("d3_triple", pmul(pmul(linear_a, linear_a), linear_a), (1,)),
    ]
    for _, w1, _ in cases:
        assert degree(w1) <= W + 1
        assert all(peval(w1, x) != 0 for x in domain)
        assert pgcd(w1, SMALL_B) == [1]

    supports: list[tuple[int, ...]] = []
    masks: list[int] = []
    locators: list[list[int]] = []
    for indices in combinations(range(N), M):
        supports.append(indices)
        masks.append(sum(1 << i for i in indices))
        locators.append(monic_locator([domain[i] for i in indices]))
    census_size = math.comb(N, M)
    assert len(locators) == census_size
    assert math.gcd(M, N) == 1

    print("=== BC first-interior mixed subset-product audit ===")
    print("status: PROVED REDUCTION / EXACT CENSUS / REALIZED TOY")
    print(f"field/domain: F_{P}, mu_{N}, generator={generator}, zeta={zeta}")
    print(
        f"row: (K,m,w,d1,d2)=({K},{M},{W},{FIRST_INTERIOR},"
        f"{SECOND_ROW_DEGREE}); supports={census_size}"
    )
    faithful_average = Fraction(census_size, P**(W + 1))
    print(
        "rank-three faithful average: "
        f"{faithful_average.numerator}/{faithful_average.denominator}="
        f"{float(faithful_average):.9f}; gcd(m,n)=1 => all supports aperiodic"
    )

    case_summaries: list[dict[str, object]] = []
    realizations: list[dict[str, object]] = []
    rank = W + 1
    for case_name, w1, factor_degrees in cases:
        d = degree(w1)
        h = max(0, W + degree(SMALL_B) - d)
        assert h + d == rank
        buckets: dict[tuple[tuple[int, ...], tuple[int, ...]], list[int]]
        buckets = defaultdict(list)
        for locator_index, locator in enumerate(locators):
            top = tuple(locator[M - i] for i in range(1, h + 1))
            residue = padded_remainder(locator, w1)
            buckets[(top, residue)].append(locator_index)

        sizes = Counter(len(bucket) for bucket in buckets.values())
        max_fiber = max(sizes)
        heaviest_targets = sorted(key for key, bucket in buckets.items()
                                   if len(bucket) == max_fiber)
        target = heaviest_targets[0]
        min_exchange = M + 1
        collision_pairs = 0
        for bucket in buckets.values():
            for i in range(len(bucket)):
                for j in range(i + 1, len(bucket)):
                    exchange = (masks[bucket[i]] ^ masks[bucket[j]]).bit_count() // 2
                    min_exchange = min(min_exchange, exchange)
                    collision_pairs += 1
        if collision_pairs == 0:
            min_exchange = 0
        assert min_exchange >= rank + 1

        units = unit_count(d, factor_degrees)
        group_size = P**h * units
        kappa = Fraction(P**d, units)
        second_moment = sum(len(bucket) ** 2 for bucket in buckets.values())
        row_overhead = Fraction(max_fiber * P**rank, census_size)
        group_overhead = Fraction(max_fiber * group_size, census_size)
        summary = {
            "case": case_name,
            "degree": d,
            "head_depth": h,
            "rank": rank,
            "W1": w1,
            "factor_degrees": factor_degrees,
            "unit_count": units,
            "unit_defect": [kappa.numerator, kappa.denominator],
            "group_size": group_size,
            "image_size": len(buckets),
            "max_fiber": max_fiber,
            "max_target_count": len(heaviest_targets),
            "occupancy_histogram": dict(sorted(sizes.items())),
            "second_moment": second_moment,
            "collision_pairs": collision_pairs,
            "minimum_exchange": min_exchange,
            "row_normalized_overhead": [row_overhead.numerator,
                                        row_overhead.denominator],
            "group_normalized_overhead": [group_overhead.numerator,
                                          group_overhead.denominator],
            "heaviest_target": target,
        }
        case_summaries.append(summary)
        realizations.append(realize_heaviest_fiber(
            case_name,
            w1,
            buckets[target],
            locators,
            domain,
            lambda_d,
        ))
        print(
            f"{case_name:29s} d/h/r={d}/{h}/{rank} "
            f"|H|={group_size:6d} image={len(buckets):6d} "
            f"max={max_fiber:2d} min-exchange={min_exchange} "
            f"R_s={float(row_overhead):.6f} "
            f"kappa={float(kappa):.6f}"
        )

    subunit_collision = verify_subunit_collision()
    print(
        "\nsubunit-average sharpness: F_101, D={0,...,5}, m=K=3, "
        "rank=1, average=20/101, realized fiber=3, exchange=2"
    )

    toy_sparse_floor = (97**4 + math.comb(16, 7) - 1) // math.comb(16, 7)
    assert toy_sparse_floor == 7739
    deployed = deployed_nonempty_bounds()
    print("\nnonempty-slice bounds (optimistic coefficient field = printed prime):")
    print(
        "F97/mu16 pinned rank-4 nonempty slice: least-integer R="
        f"ceil(97^4/binom(16,7))={toy_sparse_floor}"
    )
    for row in deployed:
        print(
            f"{row['row']:11s} strict r={row['strict_rank']} "
            f"log2(avg)={row['strict_log2_average']:.6f} "
            f"log2(R_real)>={row['strict_real_nonempty_bound_bits']:.6f} "
            f"R_integer>={row['strict_least_integer_overhead']} "
            f"({row['strict_integer_overhead_bits']:.6f} bits); "
            f"full r={row['full_rank']} "
            f"log2(avg)={row['full_log2_average']:.6f} "
            f"log2(R_real)>={row['full_real_nonempty_bound_bits']:.6f} "
            f"R_integer>={row['full_least_integer_overhead']} "
            f"({row['full_integer_overhead_bits']:.6f} bits)"
        )

    assert all(item["profile"] == [FIRST_INTERIOR, SECOND_ROW_DEGREE]
               for item in realizations)
    assert all(item["determinant_ok"] and item["gluing_ok"]
               for item in realizations)
    payload = {
        "problem_id": "prob:saturated-bc / first-interior modular fibers",
        "status": "PROVED_REDUCTION_EXACT_CENSUS_REALIZED_TOY",
        "parameters": {
            "p": P,
            "n": N,
            "K": K,
            "m": M,
            "w": W,
            "profile": [FIRST_INTERIOR, SECOND_ROW_DEGREE],
            "rank": rank,
            "census_size": census_size,
        },
        "cases": case_summaries,
        "realizations": realizations,
        "subunit_collision": subunit_collision,
        "pinned_rank4_nonempty_overhead_floor": toy_sparse_floor,
        "deployed_nonempty_bounds": deployed,
    }
    print("\nJSON_SUMMARY=" + json.dumps(payload, sort_keys=True))
    print(
        "RESULT: PASS; mixed subset-product fibers enumerated, exchange rigidity "
        "verified, one heaviest target per case realized, real/integer floors "
        "recomputed"
    )


if __name__ == "__main__":
    main()
