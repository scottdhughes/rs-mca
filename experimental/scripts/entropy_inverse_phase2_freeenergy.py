#!/usr/bin/env python3
r"""Phase 2: does the free-energy decay (the L869 branch Phase 1 put us on) hold, and what does it reduce to?

Gamma_ell = sum_s R(s)^ell (R = prefix-fiber sizes), main_ell = C^ell / Q^{w(ell-1)} (random model), so
ratio_ell = Gamma_ell/main_ell = E_s[(1+delta(s))^ell] with R(s)=mean(1+delta(s)). Free-energy per level =
(1/ell)log2(ratio_ell). The free-energy branch claims this decays (excess controlled) for spread trades.

Findings:
  (1) DENSITY controls it. mean-fiber >> 1 (dense, = deployed ~2^192): free-energy per level ~ 0 (excess tiny).
      mean-fiber ~ 1 (sparse, NOT deployed): excess blows up in ell.
  (2) In the dense regime ratio_ell ~ ratio_2^{ell-1} (the excess factorizes through the 2nd moment; small-delta
      variance control). HONEST: E[(1+delta)^ell] at the deployed ell=(log N)^A is max(1+delta)-dominated, so at
      those levels the decay is EQUIVALENT to the max-fiber theorem (C9) -- the sqrt(p) wall. The toy
      factorization is the small-ell/small-n regime before the tail dominates.
So: the free-energy branch is the right + numerically-valid branch deployed, but its proof at deployed ell is
the same max-fiber/sqrt(p) crux.
"""
from __future__ import annotations
import math, itertools
from collections import defaultdict
import sympy

def mu(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)]

def fiber_moments(p, n, m, w, Lmax=6):
    pts = mu(p, n); C = math.comb(n, m); Q = p
    R = defaultdict(int)
    for S in itertools.combinations(range(n), m):
        R[tuple(sum(pow(pts[i], j, p) for i in S) % p for j in range(1, w + 1))] += 1
    Rv = list(R.values())
    ratio = {L: sum(r ** L for r in Rv) / (C ** L / Q ** (w * (L - 1))) for L in range(2, Lmax + 1)}
    return ratio, C / Q ** w

def main():
    print("# Phase 2: free-energy per level vs density; and the excess factorization ratio_ell ~ ratio_2^{ell-1}.")
    print(f"  {'n':>3} {'p':>5} {'meanfiber':>10} {'r2':>7} {'r4':>8} {'(1/4)log2 r4':>13}  {'r4/r2^3':>8} {'r6/r2^5':>8}")
    for n in [14, 16, 18, 20]:
        m = n // 2; w = 2; k = 1
        while not sympy.isprime(k * n + 1):
            k += 1
        p = k * n + 1
        r, mf = fiber_moments(p, n, m, w)
        fpl = math.log2(r[4]) / 4
        print(f"  {n:>3} {p:>5} {mf:>10.1f} {r[2]:>7.4f} {r[4]:>8.4f} {fpl:>13.4f}  "
              f"{r[4]/r[2]**3:>8.3f} {r[6]/r[2]**5:>8.3f}")
    print("# dense (mean-fiber large) => free-energy per level ~0 (decay holds) AND ratio_ell~ratio_2^{ell-1}.")
    print("# HONEST: at deployed ell=(log N)^A the moments are max-fiber-dominated => decay = the max-fiber")
    print("#   theorem (C9) = the sqrt(p) barrier. Free-energy is the right/viable branch, not an escape from it.")

if __name__ == "__main__":
    raise SystemExit(main())
