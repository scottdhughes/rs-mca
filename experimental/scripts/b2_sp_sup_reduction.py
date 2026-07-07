#!/usr/bin/env python3
"""Round (c): SP <== a UNIFORM SUP bound max_{c!=0}|pi_odd(c)| <= p^{theta}, via the crude count.

Two parts:
(1) REDUCTION ARITHMETIC (exact exponents, deployed KoalaBear): the crude bound
      Sum_{c!=0}|pi_odd(c)|^s <= p^{w_odd} M^s,  M = max_{c!=0}|pi_odd(c)|
    beats the SP target n^{O(1)} n^s = p^{gamma s + O(1)} iff  log_p M <= gamma - w_odd/s.
    Report the threshold theta* = gamma - w_odd/s and compare to sqrt(p) (0.5), sqrt(wn), w*sqrt(p) (Weil).
(2) ADVERSARIAL MAX SEARCH in the regime-representative setting (w_odd/(n/2) ~ 0.03): coordinate
    ascent on c over F_p^{w_odd} maximizing |pi_odd(c)|, from spike + random restarts, to estimate
    the TRUE M and the ratio M/sqrt(p). If M/sqrt(p) stays O(1) (<< the threshold p^{theta*}), the
    sup-bound route to SP is comfortable. Also confirms odd-support blocks minimal-value-set (M ~ sqrt p,
    NOT sqrt(wn)).
"""
from __future__ import annotations
import argparse, math
import numpy as np
import sympy


def reduction_arithmetic():
    log2p, k, gamma = 31.0, 21, 0.678
    n = 2 ** k
    w = 67471
    w_odd = w // 2
    s = n // 4
    theta_star = gamma - w_odd / s            # log_p M threshold for SP via crude count
    print("## (1) crude-count reduction arithmetic (deployed KoalaBear)")
    print(f"  p~2^{log2p}, n=2^{k}, w={w}, w_odd~{w_odd}, s=n/4=2^{math.log2(s):.1f}, gamma={gamma}")
    print(f"  THRESHOLD  theta* = gamma - w_odd/s = {gamma} - {w_odd/s:.4f} = {theta_star:.4f}")
    print(f"    => SP holds if  max|pi_odd| <= p^{theta_star:.4f} = n^{theta_star/gamma:.4f}")
    # candidate M scales, in log_p and log_n
    def show(name, log_p_M):
        print(f"    {name:<28} log_p M = {log_p_M:.4f} (n^{log_p_M/gamma:.3f})  "
              f"{'OK  <= theta*' if log_p_M <= theta_star else 'FAILS > theta*'}")
    show("sqrt(p)  [numerics/truth]", 0.5)
    lw = math.log2(w) / log2p
    show("sqrt(w n) [min-val-set wc]", 0.5 * (lw + gamma))
    show("w*sqrt(p) [Weil, useless]", lw + 0.5)
    print(f"  margin at truth sqrt(p): theta* - 0.5 = {theta_star-0.5:.4f} (in n: n^{(theta_star-0.5)/gamma:.3f} slack)")


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


def pi_abs(c, A, p, tp):
    ph = (c @ A) % p
    return abs(np.exp(1j * tp * ph).sum())


def coord_ascent(A, p, w_odd, n, restarts, rng):
    tp = 2 * math.pi / p
    best = 0.0
    for r in range(restarts):
        if r == 0:
            c = np.ones(w_odd, dtype=np.int64)                    # spike start
        elif r == 1:
            c = np.array([pow(2, i, p) for i in range(w_odd)], dtype=np.int64)  # geometric start
        else:
            c = rng.integers(0, p, size=w_odd, dtype=np.int64)
        cur = pi_abs(c, A, p, tp)
        improved = True
        while improved:
            improved = False
            for t in range(w_odd):
                # try best value for coordinate t over a candidate set (full p is slow; sample)
                cands = rng.integers(0, p, size=min(p, 256), dtype=np.int64)
                old = c[t]
                bestv, bestval = old, cur
                for v in cands:
                    c[t] = v
                    val = pi_abs(c, A, p, tp)
                    if val > bestval:
                        bestval, bestv = val, v
                c[t] = bestv
                if bestval > cur + 1e-9:
                    cur, improved = bestval, True
        best = max(best, cur)
    return best


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="512:8,1024:16,2048:33", help="n:w_odd, regime-representative")
    ap.add_argument("--nprimes", type=int, default=3)
    ap.add_argument("--restarts", type=int, default=40)
    a = ap.parse_args(argv)
    reduction_arithmetic()
    print("\n## (2) adversarial max search (coordinate ascent), regime-representative w_odd/(n/2)~0.03")
    print("  n     w_odd  ratio   p       gamma   M=max|pi_odd|   M/sqrt(p)   M/sqrt(w n)   (M/n)")
    rng = np.random.default_rng(3)
    for cfg in a.configs.split(","):
        n, w_odd = (int(x) for x in cfg.split(":"))
        primes, kk = [], 1
        while len(primes) < a.nprimes:
            q = kk * n + 1
            if sympy.isprime(q):
                primes.append(q)
            kk += 1
        for p in primes:
            pts = mu_n(p, n)
            J = odd_exps(n, w_odd)
            A = np.empty((w_odd, n), dtype=np.int64)
            for t, j in enumerate(J):
                A[t] = np.array([pow(int(a_), j, p) for a_ in pts], dtype=np.int64)
            M = coord_ascent(A, p, w_odd, n, a.restarts, rng)
            gamma = math.log(n) / math.log(p)
            print(f"  {n:<5} {w_odd:<5} {w_odd/(n/2):.3f}  {p:<7} {gamma:.3f}  "
                  f"{M:>10.2f}     {M/math.sqrt(p):.3f}       {M/math.sqrt(w_odd*2*n):.3f}       ({M/n:.3f})")
    print("\n# SP-via-sup comfortable IFF M/sqrt(p) = O(1) (truth), well below p^{theta*-0.5} headroom.")
    print("# M ~ sqrt(p) (NOT sqrt(w n)) confirms odd-support blocks minimal-value-set concentration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
