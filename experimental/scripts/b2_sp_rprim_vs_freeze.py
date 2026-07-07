#!/usr/bin/env python3
"""#397 cross-check: do the freeze families (which kill the |pi_odd| sup bound) inflate max_z|R_prim|?

R_prim(z) = #{primitive S subset mu_n, |S|=m : Phi_w(S)=z}. Its Fourier transform in z is
    Rhat(c) = sum_{|S|=m} prod_{a in S} e_p(f_c(a)) = e_m({v_a}),  v_a = e_p(f_c(a)),  f_c = sum_j c_j x^j.
So max_z|R_prim| <= p^{-w}(C(n,m) + sum_{c!=0}|e_m(v_c)|), and the #397 target
    max_z|R_prim| <= L * mean = L * C(n,m)/p^w   <==>   sum_{c!=0}|e_m(v_c)| <= (L-1) C(n,m).
CLAIM (mechanism): freeze c inflate pi_odd = p_1(v) but NOT e_m(v) -- the small per-element phase arc,
summed over m elements in the m-fold symmetric function, WRAPS and cancels. So freezes do NOT threaten
the #397 sup-certificate; it lives on the SIGNED e_m, immune to the freezes that break the |.|-sup bound.
This script computes, at toy scale, for freeze vs generic c:
  pi_odd = |sum_a v_a|  (freeze: LARGE)   and   |e_m(v)| / C(n,m)  (freeze: NOT large, ~ generic).
e_m via generating function [z^m] prod_a (1 + z v_a).
"""
from __future__ import annotations
import math
import numpy as np
import sympy
from math import comb


def em_of(v, m):
    """e_m(v) = [z^m] prod_a (1 + z v_a), via iterative convolution. v: complex array."""
    poly = np.zeros(m + 1, dtype=complex)
    poly[0] = 1.0
    for va in v:
        # multiply by (1 + va z), truncated at degree m
        poly[1:] = poly[1:] + va * poly[:-1]
    return poly[m]


def phases(n, p, exps, c):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    pts = [pow(z, k, p) for k in range(n)]
    f = np.zeros(n, dtype=np.int64)
    for cj, j in zip(c, exps):
        if cj:
            f = (f + cj * np.array([pow(a, j, p) for a in pts], dtype=object)) % p
    f = np.array([int(x) for x in f], dtype=np.int64)
    return np.exp(2j * math.pi * f / p)


def run(n, p, w, m, rng):
    Cnm = comb(n, m)
    exps = [j for j in range(1, w + 1) if j % 2 == 1]
    # exact-alias freeze: f = x - x^{1+D}, D=2^k' <= w-1, = 0 on mu_D (D frozen points)
    D = 1
    while 2 * D + 1 <= w and 2 * D <= n // 2:
        D *= 2
    fr_exps = [1, 1 + D]
    print(f"\n### n={n} p={p} w={w} m={m}  (C(n,m)=2^{math.log2(Cnm):.1f})  freeze f=x-x^{1+D} (D={D} frozen)")
    print(f"    {'c':<18} pi_odd=|sum v|   pi_odd/n    |e_m|/C(n,m)   log2|e_m|")
    def report(label, cc, ex):
        v = phases(n, p, ex, cc)
        pio = abs(v.sum())
        em = em_of(v, m)
        print(f"    {label:<18} {pio:9.2f}      {pio/n:.3f}     {abs(em)/Cnm:.3e}    {math.log2(max(abs(em),1e-300)):.2f}")
        return abs(em) / Cnm
    # c=0 reference (all v=1): e_m = C(n,m)
    report("c=0 (all frozen)", [1, 0], fr_exps)   # actually f = x - x^{1+D} but coeff... use pure below
    fr = report("FREEZE x-x^{1+D}", [1, p - 1], fr_exps)
    gens = [report(f"generic #{i}", rng.integers(1, p, size=len(exps)).tolist(), exps) for i in range(3)]
    genmax = max(gens)
    print(f"    --> freeze |e_m|/C = {fr:.2e};  generic max |e_m|/C = {genmax:.2e};  "
          f"freeze {'~ generic (NOT inflated)' if fr <= 3*genmax + 1e-12 else 'INFLATES e_m!'}")
    return fr, genmax


def main():
    rng = np.random.default_rng(0)
    print("# #397 cross-check: does a freeze c inflate Rhat(c)=e_m(v) (=> max_z|R_prim|)? or only pi_odd?")
    for n, p, w, m in [(64, 193, 16, 24), (128, 257, 32, 48), (256, 7681, 64, 96)]:
        if (p - 1) % n:
            continue
        run(n, p, w, m, rng)
    print("\n# If freeze |e_m|/C(n,m) ~ generic (both tiny) while pi_odd/n is LARGE for the freeze:")
    print("#   => freezes break the |pi_odd| sup bound but do NOT inflate the SIGNED e_m = Rhat = max_z|R_prim|.")
    print("#   => #397's max_z|R_prim| <= L*mean is on the right (signed) object; our barrier map explains WHY.")


if __name__ == "__main__":
    raise SystemExit(main())
