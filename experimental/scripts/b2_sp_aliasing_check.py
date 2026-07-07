#!/usr/bin/env python3
"""VERIFY the dyadic-aliasing counterexample + test whether the GOAL survives it, at FULL DEPLOYED SCALE.

Counterexample (model round): f = x - x^{65537}, 65537 = 1 + 2^16, both odd <= w=67471. On G_j, j<=16:
x^{2^16}=1 so f == 0 -- phase constant, butterfly ratio exactly 2, per-level lemma FALSE (theta >= 1).
Checks here (deployed p = 2^31-2^24+1, FULL k=21 -- feasible because c is 2-sparse):
  (A) f == 0 on G_16 (numerically, all 2^16 points).
  (B) top-level spectrum: max_t |phihat_{G_21}(t)| and phihat_0 = pi(c) for f = x - x^{65537}.
      Structure: for x in G_21, x^{2^16} =: omega in mu_32, f(x) = x(1 - omega). The omega=1 coset
      (= mu_{2^16}, 65536 points) is FROZEN: contributes exactly 2^16 to phihat_0 with zero cancellation.
      PREDICTION: sup ~ 2^16 = n^{0.7619} -- ABOVE the generic n^{0.60} but BELOW the goal n^{0.81}=2^{17.01}.
  (C) THE CAP (our addition, PROVED): f constant on S subset G => |S| <= deg f <= w, so the exact-freeze
      mass is <= w = 67471 = n^{0.7626} for EVERY c and every level. Exact aliasing cannot break the goal.
  (D) depth-15 multi-pair variant f = sum_a (x^a - x^{a+2^15}), a odd <= 1935: frozen mass 2^15 on mu_{2^15};
      measure top-level sup (tests whether many pairs inflate beyond the single frozen coset).
  (E) worst measured exponent vs goal 0.81 and vs cap 0.7626.
"""
from __future__ import annotations
import math
import numpy as np
import sympy

P = 2**31 - 2**24 + 1
K = 21
N = 1 << K
W = 67471


def build_powtab():
    g0 = int(sympy.primitive_root(P))
    zeta = pow(g0, (P - 1) // N, P)
    powtab = np.empty(N, dtype=np.int64)
    cur = 1
    for m in range(N):
        powtab[m] = cur
        cur = (cur * zeta) % P
    return powtab


def spectrum(powtab, terms):
    """terms: list of (coeff, exponent). Returns (max|phihat|, |phihat_0|) over G_21."""
    m = np.arange(N, dtype=np.int64)
    fval = np.zeros(N, dtype=np.int64)
    for coef, e in terms:
        fval = (fval + coef * powtab[(e * m) % N]) % P
    phi = np.exp(2j * math.pi * fval / P)
    hat = np.fft.fft(phi)
    return float(np.abs(hat).max()), float(abs(hat[0]))


def main():
    print(f"# Deployed-scale aliasing check: p=2^31-2^24+1, n=2^21, w={W}. goal n^0.81=2^{0.81*K:.2f}={2**(0.81*K):.0f}")
    print(f"# cap (PROVED, deg bound): exact-freeze mass <= w = {W} = n^{math.log(W)/math.log(N):.4f}")
    powtab = build_powtab()

    # (A) f = x - x^65537 identically 0 on G_16
    m16 = np.arange(0, N, 32, dtype=np.int64)          # G_16 = <zeta^32>
    fA = (powtab[m16 % N] - powtab[(65537 * m16) % N]) % P
    print(f"\n(A) f=x-x^65537 on G_16: all zero? {bool((fA == 0).all())}  (2^16 points checked)")

    # (B) top-level spectrum for the counterexample
    mx, pi0 = spectrum(powtab, [(1, 1), (P - 1, 65537)])
    print(f"(B) f=x-x^65537 on G_21: max|phihat|={mx:.0f}=n^{math.log(mx)/math.log(N):.4f}  "
          f"pi(c)=|phihat_0|={pi0:.0f}=n^{math.log(max(pi0,2))/math.log(N):.4f}")
    print(f"    frozen coset mass 2^16={2**16}; goal n^0.81={2**(0.81*K):.0f}; under goal? {mx < 2**(0.81*K)}")

    # (D) depth-15 multi-pair: a odd <= 1935 (so a+2^15 <= 34703 <= w), 200 random coeffs
    rng = np.random.default_rng(1)
    terms = []
    for a in range(1, 400, 2):                         # 200 aliased pairs frozen on mu_{2^15}
        lam = int(rng.integers(1, P))
        terms.append((lam, a)); terms.append((P - lam, a + 2**15))
    mx2, pi2 = spectrum(powtab, terms)
    print(f"(D) 200 pairs frozen on mu_2^15: max|phihat|={mx2:.0f}=n^{math.log(mx2)/math.log(N):.4f}  "
          f"|phihat_0|={pi2:.0f}  (frozen mass 2^15={2**15})")

    # (E) deepest single pair: x - x^{1+2^16} is depth 16 (max possible: 1+2^17 > w). also x^3 - x^{3+2^16}? 3+65536=65539<=w yes
    mx3, pi3 = spectrum(powtab, [(1, 3), (P - 1, 65539)])
    print(f"(E) f=x^3-x^65539 (also depth-16): max|phihat|={mx3:.0f}=n^{math.log(mx3)/math.log(N):.4f}")
    worst = max(mx, mx2, mx3)
    print(f"\n# WORST measured sup = n^{math.log(worst)/math.log(N):.4f}; cap n^0.7626; goal n^0.81 -> "
          f"{'GOAL SURVIVES exact aliasing (margin ~%.2fx)' % (2**(0.81*K)/worst) if worst < 2**(0.81*K) else 'GOAL BROKEN'}")


if __name__ == "__main__":
    raise SystemExit(main())
