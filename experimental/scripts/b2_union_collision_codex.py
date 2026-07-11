#!/usr/bin/env python3
"""Exact small-instance check of the disjoint-union collision inequality."""

from collections import Counter, defaultdict
from itertools import combinations
from math import comb, log

from sympy import isprime, primitive_root


def least_prime_one_mod_n(n: int) -> int:
    p = n + 1
    while not isprime(p):
        p += n
    return p


def balanced_gain(P: int, H: int) -> int:
    """Minimum sum q(q-2), for positive even q, sum q=P, <=H bins."""
    assert P % 2 == 0
    if P == 0:
        return 0
    assert H > 0
    t = P // 2
    if t <= H:
        return 0
    a, b = divmod(t, H)
    return 4 * (H * a * (a - 1) + 2 * a * b)


def check(n: int, alpha_num: int = 42, alpha_den: int = 100) -> None:
    p = least_prime_one_mod_n(n)
    m = (alpha_num * n) // alpha_den
    g = primitive_root(p)
    zeta = pow(g, (p - 1) // n, p)
    coords = [pow(zeta, j, p) for j in range(n)]

    fibers = defaultdict(list)
    for S in combinations(range(n), m):
        v = (sum(coords[i] for i in S) % p,
             sum(coords[i] * coords[i] for i in S) % p)
        mask = sum(1 << i for i in S)
        fibers[v].append(mask)
    v, F = max(fibers.items(), key=lambda item: (len(item[1]), item[0]))
    f = len(F)

    q = Counter()
    for x in F:
        for z in F:
            if x & z == 0:
                q[x | z] += 1
    P = sum(q.values())
    exact_gain = sum(qU * (qU - 2) for qU in q.values())

    energy = 0
    for x in F:
        for z in F:
            intersection = x & z
            union = x | z
            energy += sum((y & intersection) == intersection and
                          (y & ~union) == 0 for y in F)
    baseline = 2 * f * f - f

    target = ((2 * v[0]) % p, (2 * v[1]) % p)
    H = 0
    for U in combinations(range(n), 2 * m):
        w = (sum(coords[i] for i in U) % p,
             sum(coords[i] * coords[i] for i in U) % p)
        H += (w == target)

    local_data = []
    for Umask, qU in q.items():
        indices = [i for i in range(n) if (Umask >> i) & 1]
        local_fibers = Counter()
        for A in combinations(indices, m):
            w = (sum(coords[i] for i in A) % p,
                 sum(coords[i] * coords[i] for i in A) % p)
            local_fibers[w] += 1
        local_second_moment = sum(gw * gw for gw in local_fibers.values())
        local_data.append((qU, local_second_moment - comb(2 * m, m)))

    bound = balanced_gain(P, H)
    assert all(qU % 2 == 0 and qU >= 2 for qU in q.values())
    assert len(q) <= H
    assert exact_gain >= bound
    print({
        "n": n, "p": p, "m": m, "C(n,m)": comb(n, m),
        "v": v, "f": f, "P": P, "active_unions": len(q), "H": H,
        "exact_gain": exact_gain, "mass_capacity_bound": bound,
        "gain_over_f2": exact_gain / (f * f),
        "E": energy, "E-baseline": energy - baseline,
        "disjoint_share_of_excess": (exact_gain / (energy - baseline)
                                      if energy > baseline else 0.0),
        "effective_epsilon": (log(energy / (f * f), f) if f > 1 else 0.0),
        "local_(central_q,total_2nd_moment_excess)": sorted(local_data),
    })


def find_central_two_example(n: int, m: int) -> None:
    """Find U of size 2m whose central local fiber is 2 but moment excess > 0."""
    p = least_prime_one_mod_n(n)
    g = primitive_root(p)
    zeta = pow(g, (p - 1) // n, p)
    coords = [pow(zeta, j, p) for j in range(n)]
    inv2 = pow(2, -1, p)
    for U in combinations(range(n), 2 * m):
        phi_U = (sum(coords[i] for i in U) % p,
                 sum(coords[i] * coords[i] for i in U) % p)
        center = (phi_U[0] * inv2 % p, phi_U[1] * inv2 % p)
        local_fibers = Counter()
        for A in combinations(U, m):
            w = (sum(coords[i] for i in A) % p,
                 sum(coords[i] * coords[i] for i in A) % p)
            local_fibers[w] += 1
        excess = sum(gw * gw for gw in local_fibers.values()) - comb(2 * m, m)
        if local_fibers[center] == 2 and excess > 0:
            print({"central-two example": {"n": n, "p": p, "m": m,
                  "U": U, "central_q": 2, "local_2nd_moment_excess": excess}})
            return
    print({"central-two example": None, "n": n, "p": p, "m": m})


if __name__ == "__main__":
    for n in (8, 16):
        check(n)
    find_central_two_example(16, 6)
