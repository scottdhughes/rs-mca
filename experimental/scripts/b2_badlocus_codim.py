#!/usr/bin/env python3
"""First sub-lemma of the Sawin-adaptation route (b2/conj:Q proof attack).

Dual Fourier family (from the extraction of arXiv:1809.05137 onto our object):
    N = q^-w * sum_{t in F_q^w} T(t),   T(t) = e_m({ psi(P_t(a)) : a in mu_n }),
    P_t(X) = sum_{j=1}^w t_j X^j,   psi(y) = e_q(y).
The single-frequency Weil sum that controls cancellation is
    pi(t) = sum_{a in mu_n} psi(P_t(a))  in C.
"Good" t give square-root-type cancellation (|pi| small); "bad" t (the singular-locus
analogue) fail (|pi| ~ n).

SUB-LEMMA under test:  dim B <= w-1  (codim >= 1), B = { t : |pi(t)| not cancelling }.
The CODIMENSION is read off the SCALING of #bad with q (fixed w): #bad ~ q^{w-1} => codim 1
(sub-lemma holds); ~ q^w => codim 0 (fails). Exact-degenerate t (|pi|=n exactly) are the
hard core of B; near-degenerate (|pi| large but < n) are the incomplete-sum tail.
"""
from __future__ import annotations
import argparse, cmath, math, itertools


def _prime_factors(x):
    fs, d = set(), 2
    while d * d <= x:
        while x % d == 0:
            fs.add(d); x //= d
        d += 1
    if x > 1:
        fs.add(x)
    return fs


def primroot(q):
    facs = _prime_factors(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // p, q) != 1 for p in facs):
            return g
    raise ValueError(f"no primitive root mod {q}")


def mu_n(q, n):
    assert (q - 1) % n == 0
    z = pow(primroot(q), (q - 1) // n, q)
    return [pow(z, k, q) for k in range(n)]


def badlocus(q, n, w, thresh_frac=0.5):
    """Enumerate t in F_q^w, compute pi(t), classify bad = |pi| >= thresh_frac * n.
    Returns (#bad, #exact_degenerate(|pi|==n), q^w, q^{w-1}, max_good, sample_bad)."""
    pts = mu_n(q, n)
    eq = [cmath.exp(2j * math.pi * u / q) for u in range(q)]
    PV = [[pow(a, j, q) for j in range(1, w + 1)] for a in pts]   # a^j mod q
    thr = thresh_frac * n
    nbad = nexact = 0
    max_good = 0.0
    sample = []
    for t in itertools.product(range(q), repeat=w):
        s = 0j
        for k in range(n):
            ph = 0
            for j in range(w):
                ph += t[j] * PV[k][j]
            s += eq[ph % q]
        a = abs(s)
        if a >= thr:
            nbad += 1
            if a > n - 1e-9:
                nexact += 1
            if len(sample) < 6:
                sample.append((t, round(a, 2)))
        else:
            max_good = max(max_good, a)
    return nbad, nexact, q ** w, q ** (w - 1), max_good, sample


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--w", type=int, default=2)
    ap.add_argument("--qs", default="13,17,29,37,41,53", help="primes q; n = largest 2-power | q-1")
    ap.add_argument("--thresh", type=float, default=0.5, help="bad iff |pi| >= thresh * n")
    args = ap.parse_args(argv)
    qs = [int(x) for x in args.qs.split(",")]
    print(f"# Sub-lemma test: does #bad scale like q^(w-1) (codim 1)?  w={args.w}, bad=|pi|>={args.thresh}*n")
    print(f"# {'q':>4} {'n':>4} {'#bad':>7} {'#exact':>7} {'q^w':>8} {'q^(w-1)':>8} "
          f"{'#bad/q^(w-1)':>13} {'maxgood':>8} {'~sqrt(n*w)':>10}")
    for q in qs:
        if q < args.w + 1:
            continue
        # n = largest power of two dividing q-1
        n = 1
        while (q - 1) % (n * 2) == 0:
            n *= 2
        if n < 4:
            continue
        nbad, nexact, qw, qw1, maxgood, sample = badlocus(q, n, args.w, args.thresh)
        ratio = nbad / qw1 if qw1 else float("nan")
        print(f"  {q:>4} {n:>4} {nbad:>7} {nexact:>7} {qw:>8} {qw1:>8} "
              f"{ratio:>13.3f} {maxgood:>8.2f} {math.sqrt(n*args.w):>10.2f}")
    print("\n# codim read: #bad/q^(w-1) ~ constant => codim 1 (sub-lemma holds);")
    print("#             growing ~q => codim 0 (fails); shrinking ~1/q => codim>=2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
