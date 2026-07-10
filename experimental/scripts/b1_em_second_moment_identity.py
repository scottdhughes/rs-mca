#!/usr/bin/env python3
r"""B1 in one line: verify  Gamma_2 / flat = 1 + (1/C(N,m)^2) sum_{c!=0} |e_m(v_c)|^2.

The prefix-image energy Gamma_2 = sum_z R(z)^2 (R(z) = #{|S|=m : Phi(S)=z}, Phi = first w power sums on
mu_n) satisfies, by Parseval on the moment map F_p^w,
    Gamma_2 = (1/Q^w)[ C(N,m)^2 + sum_{c!=0} |R_hat(c)|^2 ],   R_hat(c) = sum_{|S|=m} prod_{a in S} e_p(f_c(a)),
and R_hat(c) = e_m(v_c) is exactly the SIGNED elementary symmetric of v_a = e_p(f_c(a)) (round o). With
flat = C(N,m)^2 / Q^w this is
    Gamma_2 / flat = 1 + (1/C(N,m)^2) sum_{c!=0} |e_m(v_c)|^2,
so  B1  <=>  sum_{c!=0} |e_m(v_c)|^2 <= C(N,m)^2 e^{o(N)}  -- a SECOND moment at level d=m (always dense,
C(N,m) >> Q^w), free of the sparse-diagonal pathology that defeats a per-d |e_d|^2 bound at small d.

This script computes Gamma_2 by direct census AND sum_{c!=0}|e_m(v_c)|^2 by an independent character loop,
and asserts the identity (self-checking; nonzero exit on mismatch). Sizes kept tiny (O(p^w C(N,m)) loop).
"""
from __future__ import annotations
import math
import itertools
import cmath
from itertools import combinations
from collections import defaultdict
import sympy


def mu(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)]


def check(p, n, m, w, tol=1e-6):
    pts = mu(p, n); N = n; Q = p
    Cnm = math.comb(N, m); flat = Cnm ** 2 / Q ** w
    # (1) Gamma_2 by census: bin m-subsets by w-moment prefix, sum of squares of bin sizes
    R = defaultdict(int)
    for S in combinations(range(N), m):
        R[tuple(sum(pow(pts[i], j, p) for i in S) % p for j in range(1, w + 1))] += 1
    G2 = sum(v * v for v in R.values())
    # (2) sum_{c!=0} |e_m(v_c)|^2 by independent character loop
    tp = 2j * math.pi / p
    subs = list(combinations(range(N), m))
    fpow = [[pow(pts[i], j, p) for j in range(1, w + 1)] for i in range(N)]
    off = 0.0
    for c in itertools.product(range(p), repeat=w):
        if not any(c):
            continue
        va = [cmath.exp(tp * (sum(c[j] * fpow[i][j] for j in range(w)) % p)) for i in range(N)]
        em = sum(math.prod(va[i] for i in S) for S in subs)
        off += abs(em) ** 2
    lhs = G2 / flat
    rhs = 1.0 + off / Cnm ** 2
    dense = "DENSE" if Cnm > Q ** w else "sparse"
    ok = abs(lhs - rhs) < tol
    print(f"  p={p} n={n} m={m} w={w}: C(N,m)={Cnm} vs Q^w={Q**w} [{dense}]  "
          f"Gamma2/flat={lhs:.6f}  1+sum|e_m|^2/C^2={rhs:.6f}  match={ok}")
    assert ok, f"identity FAILED at (p={p},n={n},m={m},w={w}): {lhs} != {rhs}"
    return lhs


def main():
    print("# B1 identity: Gamma_2/flat = 1 + (1/C(N,m)^2) sum_{c!=0}|e_m(v_c)|^2  (level d=m, always dense).")
    for (p, n, m, w) in [(17, 8, 4, 1), (41, 8, 4, 1), (41, 10, 5, 1), (31, 6, 3, 1), (37, 6, 3, 2)]:
        if (p - 1) % n or not sympy.isprime(p):
            continue
        check(p, n, m, w)
    print("# All identities hold => B1 <=> sum_{c!=0}|e_m(v_c)|^2 <= C(N,m)^2 e^{o(N)} (signed-e_m 2nd moment).")


if __name__ == "__main__":
    raise SystemExit(main())
