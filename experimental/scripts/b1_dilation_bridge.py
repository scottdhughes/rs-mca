#!/usr/bin/env python3
r"""B1 analytic bridge: e_m(v_c) is a Newton-Girard polynomial in the DILATED character sums {pi(rc)}.

With v_a = e_p(f_c(a)) and pi(c) := sum_{a in mu_n} e_p(f_c(a)), the power sums of v_c are dilates of pi:
    p_r(v_c) = sum_a v_a^r = sum_a e_p(r f_c(a)) = sum_a e_p(f_{rc}(a)) = pi(r c).
By Newton-Girard, e_m(v_c) = R_hat(c) is a fixed universal polynomial in pi(c), pi(2c), ..., pi(mc). Thus the
B1 second moment  sum_{c!=0} |e_m(v_c)|^2  is governed by JOINT MOMENTS of pi at the dilates {rc}, and the b2
moment law T5 (E_c|pi(c)|^{2s} <= (2s-1)!! n^s) is the direct analytic input. This script asserts BOTH:
  (1) p_r(v_c) == pi(rc)   for r = 1..m,   and
  (2) e_m(v_c) reconstructed via Newton-Girard from {pi(rc)}_{r<=m} == the direct e_m(v_c),
to machine precision (self-checking; nonzero exit on mismatch).
"""
from __future__ import annotations
import math
import random
import cmath
from itertools import combinations
import sympy


def mu(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)]


def pi_sum(pts, c, p):
    """pi(c) = sum_{a in mu_n} e_p(f_c(a)), f_c(a) = sum_j c[j] a^{j+1} (exps 1..w)."""
    tp = 2j * math.pi / p; w = len(c)
    return sum(cmath.exp(tp * (sum(c[j] * pow(a, j + 1, p) for j in range(w)) % p)) for a in pts)


def newton_e(psums, m):
    """e_m from power sums p_1..p_m via the Newton-Girard recursion e_k = (1/k) sum_i (-1)^{i-1} e_{k-i} p_i."""
    e = [1.0 + 0j]
    for k in range(1, m + 1):
        e.append(sum((-1) ** (i - 1) * e[k - i] * psums[i - 1] for i in range(1, k + 1)) / k)
    return e[m]


def check(p, n, m, w, ntest=6, seed=1, tol=1e-6):
    pts = mu(p, n); tp = 2j * math.pi / p
    rng = random.Random(seed)
    for _ in range(ntest):
        c = [rng.randrange(0, p) for _ in range(w)]
        if not any(c):
            c[0] = 1
        va = [cmath.exp(tp * (sum(c[j] * pow(a, j + 1, p) for j in range(w)) % p)) for a in pts]
        # (1) p_r(v_c) == pi(rc)
        for r in range(1, m + 1):
            pr_direct = sum(v ** r for v in va)
            pr_dilate = pi_sum(pts, [(r * cj) % p for cj in c], p)
            assert abs(pr_direct - pr_dilate) < 1e-8, f"p_r != pi(rc) at r={r}, c={c}"
        # (2) e_m via NG from {pi(rc)} == direct e_m
        psums = [pi_sum(pts, [(r * cj) % p for cj in c], p) for r in range(1, m + 1)]
        em_ng = newton_e(psums, m)
        em_direct = sum(math.prod(va[i] for i in S) for S in combinations(range(n), m))
        assert abs(em_ng - em_direct) < tol * max(1, abs(em_direct)), f"e_m NG != direct, c={c}"
    print(f"  p={p} n={n} m={m} w={w}: p_r(v_c)==pi(rc) [{ntest*m}/{ntest*m}]  e_m NG-from-dilated-pi==direct [{ntest}/{ntest}]  OK")


def main():
    print("# B1 bridge: p_r(v_c)=pi(rc); e_m(v_c) is a Newton-Girard poly in dilated {pi(rc)}.")
    for (p, n, m, w) in [(41, 8, 4, 2), (61, 10, 5, 2), (37, 6, 3, 2), (73, 8, 4, 1)]:
        if (p - 1) % n or not sympy.isprime(p):
            continue
        check(p, n, m, w)
    print("# => sum_{c!=0}|e_m(v_c)|^2 is controlled by joint moments of pi at dilates; T5 is the input.")


if __name__ == "__main__":
    raise SystemExit(main())
