#!/usr/bin/env python3
"""r-uniformity probe at SCALE: does the subgroup sum cancel uniformly in #monomials?

The barrier-beating lemma needs |pi(c)| = |sum_{a in mu_n} e_p(sum_{j in J} c_j a^j)| <= n * p^{-delta}
with delta INDEPENDENT of |J| (the open crux; all proven Bourgain-Chang bounds have delta -> 0 as
|J| -> inf). The single sum pi(c) is over n terms, so it is computable for n ~ 10^4-10^6 -- a
thousandfold past the fiber-count DP (which is q^w-bound). This tests whether generic/worst-sampled
cancellation |pi| ~ sqrt(n) survives as the monomial count r=|J| grows toward a fraction of n.

Reports, per r (J = {1,...,r}, the deployed initial-segment shape), over `samples` random nonzero c:
  max|pi|, mean|pi|, max|pi|/n (1 = NO cancellation), max|pi|/sqrt(n) (1 = perfect sqrt-cancellation).
If max|pi|/n stays small (bounded, ~ n^{-delta}) as r grows -> the per-t ingredient is r-uniform
(evidence FOR the lemma's base ingredient); if it climbs toward 1 -> degradation (obstruction real).
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


def primroot(p):
    facs = _pf(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in facs):
            return g
    raise ValueError


def mu_n(p, n):
    assert (p - 1) % n == 0, f"n={n} must divide p-1={p-1}"
    z = pow(primroot(p), (p - 1) // n, p)
    return np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)


def probe(p, n, rmax, samples, rng_seed=12345):
    pts = mu_n(p, n)                                  # (n,)
    # POW[j, a] = pts[a]^(j+1) mod p, j = 0..rmax-1
    POW = np.empty((rmax, n), dtype=np.int64)
    cur = pts.copy()
    for j in range(rmax):
        POW[j] = cur
        cur = (cur * pts) % p
    twopi_over_p = 2.0 * math.pi / p
    rng = np.random.default_rng(rng_seed)
    rows = []
    rs = [r for r in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096] if r <= rmax]
    for r in rs:
        C = rng.integers(0, p, size=(samples, r), dtype=np.int64)       # random coeff vectors
        C[(C == 0).all(axis=1)] = 1                                     # avoid all-zero c
        # phases[s, a] = sum_j C[s,j] * POW[j,a]  mod p   -> (samples, n)
        phases = (C @ POW[:r]) % p
        z = np.exp(1j * twopi_over_p * phases)                          # (samples, n)
        pin = np.abs(z.sum(axis=1))                                     # |pi(c)| per sample
        mx = float(pin.max()); mn = float(pin.mean())
        rows.append((r, mx, mn, mx / n, mx / math.sqrt(n)))
    return rows, math.sqrt(n)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=12289)     # p-1 = 2^12 * 3
    ap.add_argument("--n", type=int, default=4096)      # mu_n, power of 2 | p-1
    ap.add_argument("--rmax", type=int, default=2048)
    ap.add_argument("--samples", type=int, default=300)
    a = ap.parse_args(argv)
    gamma = math.log(a.n) / math.log(a.p)
    print(f"# r-uniformity probe: p={a.p}, n=|mu_n|={a.n}=p^{gamma:.3f} "
          f"({'LARGE, > sqrt p' if gamma > 0.5 else 'below sqrt p'}), samples={a.samples}")
    print(f"# {'r=|J|':>6} {'max|pi|':>10} {'mean|pi|':>10} {'max|pi|/n':>11} {'max|pi|/sqrt(n)':>15}")
    rows, sq = probe(a.p, a.n, a.rmax, a.samples)
    for r, mx, mn, mxn, mxs in rows:
        print(f"  {r:>6} {mx:>10.2f} {mn:>10.2f} {mxn:>11.4f} {mxs:>15.3f}")
    print(f"\n# sqrt(n) = {sq:.1f}. max|pi|/n staying small as r grows => per-t ingredient is r-UNIFORM")
    print("# (evidence FOR the lemma base); climbing toward 1 => degradation (obstruction real).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
