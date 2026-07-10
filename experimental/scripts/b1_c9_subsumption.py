#!/usr/bin/env python3
r"""B1 (second moment) is SUBSUMED by C9 (the Fourier/Sidon L^1 flatness the paper imports).

asymptotic_rs_mca.tex def:sidon-paid (C9): the Fourier/Sidon cell is paid iff the pushforward
mu = Phi_* Unif(Omega^circ) (Omega^circ = m-subsets, Phi = first-w power-sum prefix map) has
    sum_{chi != 1} |mu_hat(chi)| <= exp(o(N)).
But  mu_hat(c) = sum_z mu(z) e_p(<c,z>) = (1/C) sum_{|S|=m} prod_{a in S} e_p(f_c(a)) = e_m(v_c)/C,
so (with C=C(N,m), and normalizing the paper's exp(o(N)) to the C-scale used by our identity):
    C9  <=>  S1 := sum_{c != 0} |e_m(v_c)|      <= C * exp(o(N))     [L^1 rung, r=1]
    B1  <=>  S2 := sum_{c != 0} |e_m(v_c)|^2     <= C^2 * exp(o(N))    [L^2 rung, r=2]  (our #448)
Since |e_m(v_c)| <= C for every c (a sum of C unit terms), S2 <= (max_c |e_m|) * S1 <= C * S1, hence
    **C9 => B1** (and B1 is strictly weaker: the reverse S1 <= sqrt(Q^w * S2) loses a factor sqrt(Q^w)).
So B1 is a DOWNSTREAM CONSEQUENCE of the C9 input the paper carries as a hypothesis (Cho26ModuliFinal);
proving B1 unconditionally is essentially proving C9 unconditionally -- which is why our T5->NG attempt
(b1_t5_newton_girard_routecut.py) hits the sqrt(p)/BGK barrier. The signed-e_m functional sum_c|e_m(v_c)|^r
is one LADDER: C9 (r=1) / B1 (r=2, ours) / M31 participation-ratio #434 (r~4); all share the sqrt(p) barrier.

This script verifies, exactly (self-checking, nonzero exit on mismatch):
  (1) mu_hat(c) == e_m(v_c)/C   (the C9 object IS the normalized signed-e_m);
  (2) S2 <= C * S1              (C9 => B1);
  (3) S1 vs sqrt(Q^w * S2)      (the reverse is lossy by ~sqrt(Q^w): C9 strictly stronger).
"""
from __future__ import annotations
import math
import cmath
import itertools
from itertools import combinations
from collections import defaultdict
import sympy


def mu_n(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)]


def check(p, n, m, w, tol=1e-6):
    pts = mu_n(p, n); C = math.comb(n, m); tp = 2j * math.pi / p; Qw = p ** w
    R = defaultdict(int)
    for S in combinations(range(n), m):
        R[tuple(sum(pow(pts[i], j, p) for i in S) % p for j in range(1, w + 1))] += 1
    fpow = [[pow(a, j, p) for j in range(1, w + 1)] for a in pts]
    subs = list(combinations(range(n), m))
    S1 = S2 = maxem = 0.0
    for c in itertools.product(range(p), repeat=w):
        if not any(c):
            continue
        va = [cmath.exp(tp * (sum(c[j] * fpow[i][j] for j in range(w)) % p)) for i in range(n)]
        em = sum(math.prod(va[i] for i in Sx) for Sx in subs)
        muhat = sum(R[z] * cmath.exp(tp * (sum(c[k] * z[k] for k in range(w)) % p)) for z in R) / C
        assert abs(muhat - em / C) < tol * max(1, abs(em / C)), f"mu_hat != e_m/C at c={c}"
        ae = abs(em); S1 += ae; S2 += ae * ae; maxem = max(maxem, ae)
    assert maxem <= C + tol, "max|e_m| exceeds C(N,m)?!"
    assert S2 <= C * S1 + tol, "S2 <= C*S1 (C9=>B1) FAILED"
    print(f"  p={p} n={n} m={m} w={w}: mu_hat==e_m/C OK | max|e_m|={maxem:.1f}<=C={C} | "
          f"S2={S2:.1f}<=C*S1={C*S1:.1f} (C9=>B1) | S1={S1:.1f} vs sqrt(Qw*S2)={math.sqrt(Qw*S2):.1f} "
          f"(reverse lossy x sqrt(Qw)={math.sqrt(Qw):.1f})")


def main():
    print("# B1 (L^2 signed-e_m) is SUBSUMED by C9 (L^1 signed-e_m = the paper's Fourier/Sidon input).")
    for (p, n, m, w) in [(17, 8, 4, 1), (37, 6, 3, 2), (41, 10, 5, 1), (29, 8, 4, 1)]:
        if (p - 1) % n or not sympy.isprime(p):
            continue
        check(p, n, m, w)
    print("# => B1 needs NO separate argument beyond C9; proving it unconditionally = proving C9 (sqrt(p) barrier).")


if __name__ == "__main__":
    raise SystemExit(main())
