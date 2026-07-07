#!/usr/bin/env python3
"""SP near-n spectrum: is it confined to STRUCTURED (minimal-value-set) c, with random c << n?

Deployed regime = TRUNCATED odd block: c supported on odd j <= w, w << n (deployed w/n ~ 0.03).
f_c(a) = sum_{j odd <= w} c_j a^j, degree <= w. |pi_odd(c)| = |sum_{a in mu_n} e_p(f_c(a))|.
SP (if true) needs the near-n large spectrum to be THIN. Structural claim: |pi_odd(c)| ~ n only when
f_c has a SMALL VALUE SET on mu_n (concentrated), which is an algebraic (low-codim) condition on c.
This probe, for several (n, w_odd) in the truncated block:
  (A) samples many RANDOM c and reports max sampled |pi_odd|/n and the 99.9th pct -- should be << 1
      (random f_c equidistributes -> |pi| ~ sqrt(n) or sqrt(p)), confirming the near-n set is thin;
  (B) evaluates STRUCTURED families and reports |pi_odd|/n:
      - spike      c = t*(1,1,...,1)      (all odd-block coeffs equal)
      - geometric  c_j = t*rho^{(j-1)/2}  (odd j -> partial geometric series in a^2)
      - single     c = t*e_1              (one monomial; bounded by subgroup Gauss period ~ sqrt p)
    and how the STRUCTURED near-n values scale with p (family size ~ p-1 = poly(n) each).
If random c stay << n while a FEW structured lines reach ~n, SP is supported and the crux is:
classify/count the minimal-value-set c (bounded # of poly(n)-size algebraic families).
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


def pi_of(C, A, p):
    """|pi_odd| for each row of C (shape (m,w_odd)); A shape (w_odd,n)."""
    tp = 2 * math.pi / p
    ph = (C @ A) % p
    return np.abs(np.exp(1j * tp * ph).sum(axis=1))


def run(n, w_odd, primes, samples, seed=11):
    print(f"\n### n={n}, w_odd={w_odd}  (truncated odd block, deg<=~{2*w_odd})")
    J = odd_exps(n, w_odd)
    rng = np.random.default_rng(seed)
    print(f"  exps J={J[:8]}{'...' if len(J)>8 else ''}")
    print(f"  p       gamma  rand_max/n rand_99.9/n |  spike_max/n  geom_max/n  single_max/n")
    for p in primes:
        pts = mu_n(p, n)
        A = np.empty((w_odd, n), dtype=np.int64)
        for t, j in enumerate(J):
            A[t] = np.array([pow(int(a), j, p) for a in pts], dtype=np.int64)
        # (A) random c
        C = rng.integers(0, p, size=(samples, w_odd), dtype=np.int64)
        C[(C == 0).all(axis=1)] = 1
        pr = pi_of(C, A, p) / n
        # (B) structured, sweep t=1..p-1 (and rho for geometric)
        ts = np.arange(1, p, dtype=np.int64)
        spike = pi_of(np.outer(ts, np.ones(w_odd, dtype=np.int64)), A, p) / n
        # geometric: c_j = t * rho^{(idx)}, idx=0..w_odd-1; sweep rho over a few, take max
        geom_max = 0.0
        for rho in [2, 3, 5, (p - 1) // 2 or 1]:
            powers = np.array([pow(int(rho), i, p) for i in range(w_odd)], dtype=np.int64)
            Cg = (ts[:, None] * powers[None, :]) % p
            geom_max = max(geom_max, float(pi_of(Cg, A, p).max()) / n)
        single = pi_of((ts[:, None] * np.eye(1, w_odd, 0, dtype=np.int64)), A, p) / n
        gamma = math.log(n) / math.log(p)
        print(f"  {p:<7} {gamma:.3f}  {pr.max():.3f}      {np.quantile(pr,0.999):.3f}     |  "
              f"{spike.max():.3f}       {geom_max:.3f}       {single.max():.3f}")
    return J


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="16:4,32:4,32:8,64:8",
                    help="comma list n:w_odd")
    ap.add_argument("--nprimes", type=int, default=6)
    ap.add_argument("--samples", type=int, default=200000)
    a = ap.parse_args(argv)
    print(f"# SP structured-vs-random near-n probe. samples/p={a.samples}")
    for cfg in a.configs.split(","):
        n, w_odd = (int(x) for x in cfg.split(":"))
        primes, k = [], 1
        while len(primes) < a.nprimes:
            q = k * n + 1
            if sympy.isprime(q):
                primes.append(q)
            k += 1
        run(n, w_odd, primes, a.samples)
    print("\n# SP supported IFF rand_max/n stays bounded < 1 (thin near-n set) while structured")
    print("#   families reach ~n but number ~O(1) lines each of size p-1=poly(n).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
