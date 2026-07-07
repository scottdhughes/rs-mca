#!/usr/bin/env python3
"""Round (c) follow-up: can the 2nd-moment-over-characters route PROVE the sup bound M <= n^0.9?

Identity (exact): |pi_odd(c)|^2 <= (1/m') sum_{psi perp mu_n} |S(psi,c)|^2 = sig2(c) := sum_{a in mu_n} T_a(c),
  T_a(c) = sum_{y in F_p^*} e_p(f_c(ay) - f_c(y))   (a COMPLETE degree-<=w additive char sum; T_1 = p-1).
Weil: |T_a| <= (w-1) sqrt(p) => sig2 <= (p-1)+(n-1)(w-1)sqrt(p) ~ n w sqrt(p) => M <= n^1.25 (too weak).
BUT if |T_a| ~ sqrt(p) TYPICALLY (Weil is worst-case), sig2 ~ n sqrt(p) => M <= n^0.87 (VIABLE, < n^0.9).
This script computes, for the ADVERSARIAL-max c (coordinate ascent), the true sig2 and:
  sqrt(sig2)  vs  |pi_odd|  vs  n^0.9 (target)  vs  n sqrt(p) (viable)  vs  n w sqrt(p) (Weil)
and the typical/max |T_a| over a in mu_n. If sqrt(sig2) ~ n^0.87 the 2nd-moment route is a live proof path;
if ~ n^1.25 the off-diagonal Weil is fatal and a 4th-moment / family-equidistribution is needed.
"""
from __future__ import annotations
import argparse, math
import numpy as np
import sympy


def mu_n(p, n):
    g = int(sympy.primitive_root(p))
    z = pow(g, (p - 1) // n, p)
    return np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)


def odd_exps(n, w_odd):
    out, j = [], 1
    while len(out) < w_odd:
        if j % 2 == 1 and math.gcd(j, n) == 1:
            out.append(j)
        j += 1
    return out


def fvals(c, exps, X, p):
    """f_c(x) mod p for x in array X (any elements of F_p)."""
    acc = np.zeros(len(X), dtype=np.int64)
    for cj, j in zip(c, exps):
        acc = (acc + cj * np.power(X % p, j, dtype=object)) % p  # object to avoid overflow on big j
    return acc.astype(np.int64)


def pi_abs_and_val(c, A, p, tp):
    ph = (c @ A) % p
    z = np.exp(1j * tp * ph).sum()
    return abs(z), z


def coord_ascent_c(A, p, w_odd, restarts, rng):
    tp = 2 * math.pi / p
    best, bestc = 0.0, np.ones(w_odd, dtype=np.int64)
    for r in range(restarts):
        c = np.ones(w_odd, dtype=np.int64) if r == 0 else rng.integers(0, p, size=w_odd, dtype=np.int64)
        cur = pi_abs_and_val(c, A, p, tp)[0]
        improved = True
        while improved:
            improved = False
            for t in range(w_odd):
                cands = rng.integers(0, p, size=min(p, 200), dtype=np.int64)
                oldv, bv, bval = c[t], c[t], cur
                for v in cands:
                    c[t] = v
                    val = pi_abs_and_val(c, A, p, tp)[0]
                    if val > bval:
                        bval, bv = val, v
                c[t] = bv
                if bval > cur + 1e-9:
                    cur, improved = bval, True
        if cur > best:
            best, bestc = cur, c.copy()
    return bestc, best


def sig2_of(c, exps, mu, p, tp):
    """sig2 = sum_{a in mu_n} T_a(c), T_a = sum_{y in F_p^*} e_p(f_c(ay)-f_c(y)); also per-a |T_a|."""
    Y = np.arange(1, p, dtype=np.int64)            # F_p^*
    fY = fvals(c, exps, Y, p)                        # f_c(y)
    ephimY = np.exp(-1j * tp * fY)                   # e_p(-f_c(y))
    Ta = np.empty(len(mu), dtype=complex)
    for i, a in enumerate(mu):
        aY = (int(a) * Y) % p
        faY = fvals(c, exps, aY, p)
        Ta[i] = (np.exp(1j * tp * faY) * ephimY).sum()
    sig2 = Ta.sum().real                              # sum_a T_a  (real)
    absTa = np.abs(Ta)
    # 4th-moment excluding the trivial a=1 diagonal (Ta[0], since mu[0]=1)
    s2off = float((absTa[1:] ** 2).sum())             # sum_{a!=1} |T_a|^2
    return sig2, absTa, s2off


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="512:8,1024:16", help="n:w_odd (regime-representative)")
    ap.add_argument("--nprimes", type=int, default=2)
    ap.add_argument("--restarts", type=int, default=25)
    a = ap.parse_args(argv)
    rng = np.random.default_rng(5)
    print("# 2nd-moment-over-characters route: is sqrt(sig2) ~ n^0.87 (VIABLE) or n^1.25 (DEAD)?")
    print("# n    w_odd p       m'   |pi_odd|  sqrt(sig2)  n^0.9    n*sqrtp  n*w*sqrtp | Ta:med  max  (max/sqrtp)")
    for cfg in a.configs.split(","):
        n, w_odd = (int(x) for x in cfg.split(":"))
        primes, kk = [], 1
        while len(primes) < a.nprimes:
            q = kk * n + 1
            if sympy.isprime(q):
                primes.append(q)
            kk += 1
        for p in primes:
            mu = mu_n(p, n)
            exps = odd_exps(n, w_odd)
            tp = 2 * math.pi / p
            A = np.empty((w_odd, n), dtype=np.int64)
            for t, j in enumerate(exps):
                A[t] = np.array([pow(int(x), j, p) for x in mu], dtype=np.int64)
            c, M = coord_ascent_c(A, p, w_odd, a.restarts, rng)
            sig2, Ta, s2off = sig2_of(c, exps, mu, p, tp)
            mprime = (p - 1) // n
            sq = math.sqrt(max(sig2, 0.0))
            n09 = n ** 0.9
            # Cauchy-Schwarz-implied sup bound from the 4th moment: sig2 <= p + sqrt((n-1) s2off)
            cs_sig2 = (p - 1) + math.sqrt((n - 1) * s2off)
            cs_M = math.sqrt(cs_sig2)
            print(f"  {n:<4} {w_odd:<5} {p:<7} {mprime:<4} {M:>8.2f}  {sq:>9.2f}  {n09:>7.1f}  "
                  f"| S2off/(np)={s2off/(n*p):.3f}  CS_bound(M)={cs_M:.1f} (n^{math.log(cs_M)/math.log(n):.3f})")
    print("# sqrt(sig2)=direct 2nd-moment sup bound. CS_bound(M)=sup bound PROVABLE from the 4th moment via")
    print("#   sig2 <= p + sqrt((n-1) S2off). S2off/(np)=O(1) => 4th-moment bound holds => M <= ~n^0.87 provable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
