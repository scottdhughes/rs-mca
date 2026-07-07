#!/usr/bin/env python3
"""Barrier-beating attack, prong 1: does the fiber ENERGY concentrate?

Fiber f(z) = #{ m-subsets M of mu_n : Phi_w(M) = z },  z in F_q^w, Phi_w = (p_1,...,p_w).
The Cauchy-Schwarz first sqrt-layer needs the additive energy E2 = sum_z f(z)^2 to be near
the "flat" value C(n,m)^2 / q^w (all fibers equal). Report:
  mean   = C(n,m)/q^w                         (flat fiber size)
  maxfib = max_z f(z)                          (the conj:Q max-fiber object)
  E2     = sum_z f(z)^2                         (additive energy = #equal-moment pairs)
  E2/flat= E2 / (C(n,m)^2/q^w)                 (collision multiplier; 1 = perfectly flat)
  conc   = maxfib / mean                        (max-fiber concentration)
  f(0)   = the t-null fiber (usually the extremal target)
If maxfib/mean stays poly(n) as n grows, the 2nd moment beats the barrier; if it blows up,
the energy is carried by unstructured collisions and higher moments are needed.

Exact numpy DP returning the FULL final fiber array (int64; asserts no overflow).
"""
from __future__ import annotations
import argparse, math
import numpy as np


def _pf(x):
    fs, d = set(), 2
    while d * d <= x:
        while x % d == 0:
            fs.add(d); x //= d
        d += 1
    if x > 1:
        fs.add(x)
    return fs


def primroot(q):
    facs = _pf(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // p, q) != 1 for p in facs):
            return g
    raise ValueError


def mu_n(q, n):
    assert (q - 1) % n == 0
    z = pow(primroot(q), (q - 1) // n, q)
    return [pow(z, k, q) for k in range(n)]


def fiber_array(q, n, m, w, pts):
    """Full dp[m] over F_q^w (key = sum_h p_h q^(h-1)). Exact int64."""
    size = q ** w
    radix = np.array([q ** h for h in range(w)], dtype=np.int64)
    idx = np.arange(size, dtype=np.int64)
    comps = np.stack([(idx // radix[h]) % q for h in range(w)])
    dp = [np.zeros(size, dtype=np.int64) for _ in range(m + 1)]
    dp[0][0] = 1
    for x in pts:
        c = np.array([pow(int(x), h, q) for h in range(1, w + 1)], dtype=np.int64)
        perm = ((comps + c[:, None]) % q * radix[:, None]).sum(axis=0)
        for cnt in range(m - 1, -1, -1):
            src = dp[cnt]
            if src.any():
                dp[cnt + 1][perm] += src
    assert dp[m].max() < (1 << 62), "int64 overflow"
    return dp[m]


def stats(q, n, rho_num, rho_den, w):
    pts = mu_n(q, n)
    m = rho_num * n // rho_den + w
    if m > n:
        return None
    f = fiber_array(q, n, m, w, pts).astype(object)   # object => exact big-int sums
    tot = int(f.sum())
    flat = tot * tot / (q ** w)
    maxfib = int(f.max())
    E2 = int((f * f).sum())
    mean = tot / (q ** w)
    return {"n": n, "w": w, "m": m, "total": tot, "mean": mean, "maxfib": maxfib,
            "f0": int(f[0]), "E2": E2, "E2_over_flat": E2 / flat if flat else float("inf"),
            "conc_max_over_mean": maxfib / mean if mean else float("inf"),
            "n3": n ** 3}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=97)
    ap.add_argument("--rho", default="1/2")
    ap.add_argument("--ns", default="16,32")
    ap.add_argument("--w", type=int, default=2)
    a = ap.parse_args(argv)
    rn, rd = (int(x) for x in a.rho.split("/"))
    print(f"# q={a.q} rho={a.rho} w={a.w}: fiber energy concentration")
    print(f"# {'n':>4} {'m':>4} {'mean':>12} {'maxfib':>14} {'conc(max/mean)':>15} "
          f"{'E2/flat':>10} {'f(0)':>14} {'n^3':>10}")
    for n in [int(x) for x in a.ns.split(",")]:
        if (a.q - 1) % n or (n & (n - 1)):
            print(f"  n={n}: SKIP (need power-of-2 n | q-1)"); continue
        if a.q <= a.w:
            print("  SKIP q<=w"); continue
        s = stats(a.q, n, rn, rd, a.w)
        if not s:
            continue
        print(f"  {s['n']:>4} {s['m']:>4} {s['mean']:>12.4g} {s['maxfib']:>14} "
              f"{s['conc_max_over_mean']:>15.3g} {s['E2_over_flat']:>10.4g} "
              f"{s['f0']:>14} {s['n3']:>10}")
    print("\n# conc(max/mean) poly(n) => 2nd moment beats the barrier; blows up => need higher moments.")
    print("# E2/flat -> 1 => fibers flat (collision-free); >>1 => heavy collisions (zone-b heavy).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
