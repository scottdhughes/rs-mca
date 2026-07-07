#!/usr/bin/env python3
"""Which mechanism makes |pi_odd(c)| ~ sqrt(p) despite the w*sqrt(p) Weil wall?

pi_odd(c) = (1/m') sum_{psi in H^perp} S(psi,c),  H^perp = characters trivial on mu_n (order | m'=(p-1)/n),
  S(psi,c) = sum_{x in F_p^*} psi(x) e_p(f_c(x))   [COMPLETE sum; Weil: |S| <= (w-1) sqrt p].
Two competing explanations for the observed max|pi_odd| ~ sqrt(p):
  (M1) each |S(psi,c)| is already SMALL (~sqrt p, not w sqrt p): odd-support degenerates the sheaf.
       => target lemma = a SHARPENED Weil bound for odd f_c against mu_n-trivial characters.
  (M2) each |S(psi,c)| ~ w sqrt p but they CANCEL across the m' characters (sum collapses to ~sqrt p).
       => target lemma = character-cancellation over H^perp.
This script measures, per config and per c (dense-adversarial + resonant monomial x^{j0}):
  max_psi |S(psi,c)| / sqrt(p),   median|S|/sqrt(p),   compared to w (=Weil factor);
  and |pi_odd| = (1/m')|sum_psi S| / sqrt(p),  plus the 'cancellation ratio'
      CR = |sum_psi S| / sum_psi|S|   (near 1/m' => full cancellation M2; near 1 => M1/no cancellation).
"""
from __future__ import annotations
import math
import numpy as np
import sympy


def index_table(p, g):
    """ind[x] = discrete log base g, for x in 1..p-1."""
    ind = np.zeros(p, dtype=np.int64)
    cur = 1
    for e in range(p - 1):
        ind[cur] = e
        cur = (cur * g) % p
    return ind


def probe(n, p, w_odd, c, ind, label):
    g_ord = p - 1
    X = np.arange(1, p, dtype=np.int64)
    # f_c(x) for odd exps
    exps = [j for j in range(1, 3 * w_odd) if j % 2 == 1 and math.gcd(j, n) == 1][:w_odd]
    fc = np.zeros(p - 1, dtype=np.int64)
    for cj, j in zip(c, exps):
        if cj:
            fc = (fc + cj * np.power(X % p, j, dtype=object)) % p
    fc = np.array([int(v) for v in fc], dtype=np.int64)
    tp = 2 * math.pi / p
    ef = np.exp(1j * tp * fc)                       # e_p(f_c(x))
    indX = ind[X]                                    # ind(x)
    mprime = (p - 1) // n
    # characters trivial on mu_n: chi_{n*j}, j=0..m'-1;  chi_{nj}(x) = exp(2pi i * (n j) ind(x) / (p-1))
    Svals = np.empty(mprime, dtype=complex)
    tpm = 2 * math.pi / g_ord
    for jj in range(mprime):
        psi = np.exp(1j * tpm * ((n * jj) * indX % g_ord))
        Svals[jj] = (psi * ef).sum()
    absS = np.abs(Svals)
    pi_odd = Svals.sum() / mprime
    sp = math.sqrt(p)
    CR = abs(Svals.sum()) / max(absS.sum(), 1e-12)
    print(f"  [{label}] m'={mprime}  w={2*w_odd}  |  max|S|/sqrtp={absS.max()/sp:6.2f}  med|S|/sqrtp={np.median(absS)/sp:6.2f}"
          f"  (Weil factor w={2*w_odd})  |  |pi_odd|/sqrtp={abs(pi_odd)/sp:5.2f}  CR={CR:.4f} (1/m'={1/mprime:.4f})")


def main():
    print("# Mechanism: is max|pi_odd|~sqrt(p) from SMALL completed sums (M1) or character CANCELLATION (M2)?")
    print("# M1 <=> max|S|/sqrtp = O(1) (<< w).   M2 <=> max|S|/sqrtp ~ w  AND  CR ~ 1/m'.")
    rng = np.random.default_rng(9)
    for n, p, w_odd in [(512, 7681, 8), (512, 10753, 8), (1024, 12289, 16), (256, 7937, 8)]:
        if (p - 1) % n or not sympy.isprime(p):
            continue
        g = int(sympy.primitive_root(p))
        ind = index_table(p, g)
        print(f"\n### n={n} p={p} (gamma={math.log(n)/math.log(p):.3f})")
        # dense adversarial c (random) -- take max over a few
        for r in range(2):
            c = rng.integers(1, p, size=w_odd, dtype=np.int64)
            probe(n, p, w_odd, c, ind, f"dense#{r}")
        # resonant monomial x^{j0}: j0 = odd exp in support with max gcd(j0,p-1)
        exps = [j for j in range(1, 3 * w_odd) if j % 2 == 1 and math.gcd(j, n) == 1][:w_odd]
        j0 = max(exps, key=lambda j: math.gcd(j, p - 1))
        cm = np.zeros(w_odd, dtype=np.int64); cm[exps.index(j0)] = 1
        probe(n, p, w_odd, cm, ind, f"monomial x^{j0} (d=gcd={math.gcd(j0,p-1)})")
    print("\n# Verdict printed above: compare max|S|/sqrtp to w, and CR to 1/m'.")


if __name__ == "__main__":
    main()
