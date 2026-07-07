#!/usr/bin/env python3
"""VERIFY the frontier-model's coefficient-space L^2 theorem: fibers of Q -> (Delta_1,Delta_3,Delta_5) are <= 16.

Q = (x1,x2,x3,x4) in G^4 with x1 x2 = x3 x4 and {x1,x2} != {x3,x4}  (off-diagonal mult-energy quadruples).
Delta_j(Q) = x1^j + x2^j - x3^j - x4^j  (in F_p).  Claim (model, sec 2): each fiber of
Q -> (Delta_1, Delta_3, Delta_5) has size <= 16  => (1/p^r) sum_c |OffDiag(c)|^2 = #{Q,Q':Delta(Q)=Delta(Q')}
<= 16 |Q| <= 16 n^3, and (sec 3) sum_c OffDiag(c) = #{Q: Delta(Q)=0} = 0 (off-diagonal forbids Delta_1=0).
This script enumerates Q for a small G=mu_n and checks: (i) max fiber of (D1,D3,D5) <= 16;
(ii) #{Q,Q':(D1,D3,D5) equal}/n^3 <= 16; (iii) #{Q in Q: D1=D3=D5=0} == 0 (mean-zero, first 3 diffs).
"""
from __future__ import annotations
import math
from collections import Counter
import numpy as np
import sympy


def Gset(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)]


def check(n, p):
    G = Gset(p, n)
    Ginv = {x: pow(x, p - 2, p) for x in G}
    Gset_ = set(G)
    # powers x^1, x^3, x^5 mod p
    pw = {x: (x % p, pow(x, 3, p), pow(x, 5, p)) for x in G}
    fibers = Counter()
    nQ = 0
    zero_offdiag = 0
    for x1 in G:
        for x2 in G:
            P = (x1 * x2) % p
            s_pair = frozenset((x1, x2))
            for x3 in G:
                x4 = (P * Ginv[x3]) % p
                if x4 not in Gset_:
                    continue
                if frozenset((x3, x4)) == s_pair:      # diagonal -> skip
                    continue
                nQ += 1
                d1 = (pw[x1][0] + pw[x2][0] - pw[x3][0] - pw[x4][0]) % p
                d3 = (pw[x1][1] + pw[x2][1] - pw[x3][1] - pw[x4][1]) % p
                d5 = (pw[x1][2] + pw[x2][2] - pw[x3][2] - pw[x4][2]) % p
                fibers[(d1, d3, d5)] += 1
                if d1 == 0 and d3 == 0 and d5 == 0:
                    zero_offdiag += 1
    maxfib = max(fibers.values()) if fibers else 0
    coll = sum(m * m for m in fibers.values())          # #{Q,Q': (D1,D3,D5) equal}
    print(f"  n={n:<4} p={p:<7} |Q_offdiag|={nQ:<9} n^3={n**3:<10} | max fiber(D1,D3,D5)={maxfib:<3} (<=16? {maxfib<=16})"
          f"  coll/n^3={coll/n**3:.3f} (<=16? {coll/n**3<=16})  #{{Delta=0}}={zero_offdiag} (==0? {zero_offdiag==0})")
    return maxfib


def main():
    print("# Verify model L^2 theorem: fibers of Q->(Delta_1,Delta_3,Delta_5) on off-diagonal mult-energy quadruples")
    print("# claim: max fiber <= 16, coll <= 16 n^3, and no off-diagonal Q has Delta_1=Delta_3=Delta_5=0.")
    worst = 0
    for n in [16, 32, 64, 128]:
        # smallest prime p = 1 mod n, p > 5, with p not tiny
        k = 1
        while True:
            p = k * n + 1
            if p > 50 and sympy.isprime(p):
                break
            k += 1
        worst = max(worst, check(n, p))
        # a second prime for n=64 to be safe
    print(f"# overall max fiber observed = {worst}  (model claims <= 16).")


if __name__ == "__main__":
    main()
