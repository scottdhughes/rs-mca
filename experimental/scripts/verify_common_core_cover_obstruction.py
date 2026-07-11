#!/usr/bin/env python3
"""Finite replay for the common-core shortening and capacity formulas."""

from itertools import combinations
from math import comb


def trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(a, b, p):
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0)
                  + (b[i] if i < len(b) else 0)) % p
    return trim(out)


def sub(a, b, p):
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0)
                  - (b[i] if i < len(b) else 0)) % p
    return trim(out)


def scale(a, c, p):
    return trim([(c * x) % p for x in a])


def mul(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out)


def div_exact(num, den, p):
    num = trim(num[:])
    den = trim(den[:])
    if len(num) < len(den):
        assert num == [0]
        return [0]
    out = [0] * (len(num) - len(den) + 1)
    inv = pow(den[-1], -1, p)
    while num != [0] and len(num) >= len(den):
        shift = len(num) - len(den)
        coeff = num[-1] * inv % p
        out[shift] = coeff
        for i, x in enumerate(den):
            num[i + shift] = (num[i + shift] - coeff * x) % p
        trim(num)
    assert num == [0]
    return trim(out)


def evaluate(poly, x, p):
    out = 0
    for coeff in reversed(poly):
        out = (out * x + coeff) % p
    return out


def locator(points, p):
    out = [1]
    for x in points:
        out = mul(out, [(-x) % p, 1], p)
    return out


def interpolate(points, values, p):
    if not points:
        return [0]
    out = [0]
    for i, x_i in enumerate(points):
        basis = [1]
        denom = 1
        for j, x_j in enumerate(points):
            if i == j:
                continue
            basis = mul(basis, [(-x_j) % p, 1], p)
            denom = denom * (x_i - x_j) % p
        out = add(out, scale(basis, values[i] * pow(denom, -1, p), p), p)
    return trim(out)


def matrix_rank(matrix, p):
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, p)
        a[rank] = [(inv * x) % p for x in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col] % p:
                factor = a[r][col]
                a[r] = [(x - factor * y) % p
                        for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def explainable(values, domain, support, degree, p):
    if degree == 0:
        return all(values[x] == 0 for x in support)
    seed = support[:degree]
    poly = interpolate(seed, [values[x] for x in seed], p)
    return all(evaluate(poly, x, p) == values[x] for x in support)


def check_configuration(n, k, w, s, p):
    assert n < p
    r = n - k
    a = k + w + 1
    t = n - a
    assert 0 <= w <= r - 1 and 0 <= s <= k
    domain = tuple(range(1, n + 1))
    k_set = domain[:k - s]
    q_k = locator(k_set, p)
    eligible = [support for support in combinations(domain, a)
                if set(k_set).issubset(support)]
    assert len(eligible) == comb(r + s, w + s + 1)

    checks = 1
    prefix_groups = {}
    for support in eligible:
        residual = tuple(x for x in support if x not in k_set)
        q_s = locator(support, p)
        q_residual = locator(residual, p)
        assert q_s == mul(q_k, q_residual, p)
        assert div_exact(q_s, q_k, p) == q_residual
        prefix = tuple(q_s[-2-i] for i in range(w))
        short_prefix = tuple(q_residual[-2-i] for i in range(w))
        prefix_groups.setdefault(prefix, []).append((support, short_prefix))
        checks += 2

    for group in prefix_groups.values():
        short_prefixes = {item[1] for item in group}
        assert len(short_prefixes) == 1
        supports = [item[0] for item in group]
        core = set(supports[0])
        for support in supports[1:]:
            core.intersection_update(support)
        error_union = sorted(set(domain) - core)
        h = [[pow(x, row, p) for x in error_union] for row in range(r)]
        kappa_rank = len(error_union) - matrix_rank(h, p)
        assert kappa_rank == max(0, k - len(core))
        checks += 2

    # Construct one exact witness and replay the received-line shortening.
    support = eligible[len(eligible) // 2]
    gamma = 3
    h_poly = [(7 + 2 * i) % p for i in range(k)]
    r1 = {x: (x * x + 3 * x + 5) % p for x in domain}
    r0 = {x: (evaluate(h_poly, x, p) - gamma * r1[x]) % p
          for x in domain}
    for x in set(domain) - set(support):
        r0[x] = (r0[x] + 1) % p

    g0 = interpolate(k_set, [r0[x] for x in k_set], p)
    g1 = interpolate(k_set, [r1[x] for x in k_set], p)
    numerator = sub(sub(h_poly, g0, p), scale(g1, gamma, p), p)
    h_tilde = div_exact(numerator, q_k, p)
    assert len(h_tilde) - 1 < s or h_tilde == [0]

    short_domain = tuple(x for x in domain if x not in k_set)
    short_support = tuple(x for x in support if x not in k_set)
    r0_tilde = {}
    r1_tilde = {}
    for x in short_domain:
        inv = pow(evaluate(q_k, x, p), -1, p)
        r0_tilde[x] = (r0[x] - evaluate(g0, x, p)) * inv % p
        r1_tilde[x] = (r1[x] - evaluate(g1, x, p)) * inv % p
        original = (r0[x] + gamma * r1[x] - evaluate(h_poly, x, p)) % p
        shortened = (r0_tilde[x] + gamma * r1_tilde[x]
                     - evaluate(h_tilde, x, p)) % p
        assert (original == 0) == (shortened == 0)
        checks += 1

    assert sum((r0[x] + gamma * r1[x]) % p == evaluate(h_poly, x, p)
               for x in domain) == a
    assert sum((r0_tilde[x] + gamma * r1_tilde[x]) % p
               == evaluate(h_tilde, x, p) for x in short_domain) == w + s + 1
    original_common = (explainable(r0, domain, support, k, p)
                       and explainable(r1, domain, support, k, p))
    shortened_common = (explainable(r0_tilde, short_domain, short_support, s, p)
                        and explainable(r1_tilde, short_domain, short_support, s, p))
    assert original_common == shortened_common
    checks += 3

    support_cap = comb(r + s, w + s + 1)
    secant_cap = comb(r + s, s + 1)
    assert min(support_cap, secant_cap) <= support_cap
    assert t + 1 <= r <= secant_cap
    checks += 2
    return checks, len(eligible), len(prefix_groups)


def main():
    configs = [
        (7, 3, 1, 1, 11),
        (8, 3, 1, 1, 11),
        (9, 4, 1, 2, 13),
        (10, 4, 2, 1, 13),
    ]
    total = 0
    for config in configs:
        checks, supports, groups = check_configuration(*config)
        total += checks
        print(f"config={config} supports={supports} prefix_groups={groups}: PASS")
    print(f"RESULT: PASS ({total} checks)")


if __name__ == "__main__":
    main()
