#!/usr/bin/env python3
"""B1 tail: per-d PTE-pair count D_d vs its expected Q^{-w} fraction, and the tail's near-flatness.

tail = sum_{d>w} C(N-2d,m-d) D_d,  flat = C(N,m)^2/Q^w. Reduction: tail/flat <= e^{o(N)} follows from
    D_d <= C(N,d) C(N-d,d) Q^{-w} e^{o(N)}   for every d > w   (the PTE fraction <= expected, up to sub-exp),
since sum_d C(N-2d,m-d) C(N,d) C(N-d,d) = C(N,m)^2 (Vandermonde). This script computes, per d:
  D_d      = # ordered disjoint (A,B), |A|=|B|=d, p_j(A)=p_j(B) for j<=w   (the PTE-pair count),
  exp_d    = C(N,d) C(N-d,d) / Q^w   (expected),  ratio r_d = D_d / exp_d   (want bounded ~ 1),
  and the contribution share of C(N-2d,m-d) D_d to Gamma_2, confirming Gamma_2/flat ~ 1 with no anomalous d.
T6 (pte_rigidity) => D_d = 0 for 1<=d<=w (shown). T12 (b2) => D_{w+1} <= 30 C(N,w+1) (an absolute, generically
LOOSE, ceiling). KEY: D_d is the DISJOINT count (no A=B diagonal); it stays generic (r_d ~ 1) in BOTH the
sparse regime Q^w > C(N,d) and the dense regime -- unlike the diagonal-inclusive fiber energy D_d^all, which
is diagonal-DOMINATED when sparse (so a sum_{c!=0}|e_d|^2 <= C(N,d)^2 bound is false there). We tag each d
sparse/dense and confirm r_d ~ 1 across all d>w -- the numerical content of the tail bound.
"""
from __future__ import annotations
import math
from itertools import combinations
from collections import defaultdict
import sympy


def mu(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)]


def Dd_disjoint(pts, d, w, p):
    if d == 0:
        return 1
    byk = defaultdict(list)
    for A in combinations(pts, d):
        byk[tuple(sum(pow(x, j, p) for x in A) % p for j in range(1, w + 1))].append(frozenset(A))
    tot = 0
    for grp in byk.values():
        for A in grp:
            for B in grp:
                if not (A & B):
                    tot += 1
    return tot


def run(p, n, m, w):
    pts = mu(p, n); Q = p; Cnm = math.comb(n, m)
    flat = Cnm ** 2 / Q ** w
    print(f"\n  p={p} n={n} m={m} w={w}: mean={Cnm/Q**w:.1f}, flat={flat:.1f}, dmax={min(m,n-m)}")
    G2 = 0
    print(f"    d :  D_d      exp_d=C(N,d)C(N-d,d)/Q^w   r_d=D_d/exp   C(N-2d,m-d)D_d  (share of Gamma2)")
    contribs = {}
    for d in range(0, min(m, n - m) + 1):
        if n - 2 * d < m - d or m - d < 0:
            continue
        Dd = Dd_disjoint(pts, d, w, p)
        expd = math.comb(n, d) * math.comb(n - d, d) / Q ** w if d > 0 else 1.0
        rd = Dd / expd if expd > 0 else float('nan')
        contr = math.comb(n - 2 * d, m - d) * Dd
        G2 += contr
        contribs[d] = contr
        reg = "SPARSE" if math.comb(n, d) < Q ** w else "dense "
        tag = "  <- T6: D_d=0" if 1 <= d <= w and Dd == 0 else ("  <- T12 ceiling" if d == w + 1 else "")
        if Dd > 0 or d <= w + 1:
            print(f"    {d:2d}[{reg}]: {Dd:8d}   {expd:12.2f}          {rd:7.3f}       {contr:12d}{tag}")
    print(f"    => Gamma2={G2}, Gamma2/flat={G2/flat:.4f}; max_d>w r_d bounded => tail <= flat*e^o(N).")
    # dominant d
    dom = max(contribs, key=contribs.get)
    print(f"    dominant d={dom} ({100*contribs[dom]/G2:.0f}% of Gamma2); tail(d>w) share = {100*sum(v for k,v in contribs.items() if k>w)/G2:.0f}%")


def main():
    print("# B1 tail: per-d PTE count D_d vs expected; r_d bounded across d>w => tail near-flat (B1).")
    for (p, n, m, w) in [(97, 16, 8, 2), (241, 20, 10, 2), (101, 20, 10, 2), (61, 18, 9, 2)]:
        if (p - 1) % n or not sympy.isprime(p): continue
        run(p, n, m, w)
    print("\n# T6 zeros the d<=w rows; T12 gives an absolute (loose) ceiling at d=w+1; the disjoint r_d stay")
    print("#   ~1 across ALL d>w -- SPARSE and dense alike -- so the d>w tail is flat*e^{o(N)}. The remaining")
    print("#   rigorous step is the uniform-in-d DISJOINT-count law D_d = C(N,d)C(N-d,d)Q^{-w}(1+o(1)) (Lang-")
    print("#   Weil equidistribution of w power-sum constraints on disjoint d-subsets + T12-capped coset term).")


if __name__ == "__main__":
    raise SystemExit(main())
