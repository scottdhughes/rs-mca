#!/usr/bin/env sage
# -*- mode: python -*-
r"""
subspace_form_e3.sage -- test the note's second-pass PROOF TARGET for the KEY LEMMA:

  E_3 <= ell-2   <=>   dim(V_1 + ... + V_K) >= E_3,
  V_k = h_k * F_p[X]_{<= mu_k-2},  h_k = (X^ell - w_k)/g_k  the CO-FIBER locator
  (g_k = fiber locator = prod_{x in F_k}(X-x); h_k = prod_{x in coset\F_k}(X-x), deg = ell-mu_k).

Each V_k lives in F_p[X]_{<= ell-2} (dim ell-1), with dim V_k = mu_k-1.
We compute dim(sum_k V_k) at the E_3=ell-2 saturators and check it against E_3 and
against sum(mu_k-1)=P-K.  If the subspace identity is the right proof target, dim(sum V_k)
should sit at E_3 (tight) for saturators.  (Independent Sage/GF(p) check.)
"""

SATURATORS = [
    dict(label="ell=11 p=331 (E3=9=ell-2)", p=331, ell=11,
         gamma=[97,29,97,239,171,92,143,155,270,1]),
    dict(label="ell=13 p=313 (E3=11=ell-2)", p=313, ell=13,
         gamma=[254,289,29,276,242,219,201,261,79,232,133,1]),
    dict(label="ell=17 p=103 (E3=15=ell-2)", p=103, ell=17,
         gamma=[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
    dict(label="ell=17 p=409 (E3=14=ell-3, contrast)", p=409, ell=17,
         gamma=[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1]),
]

def excess_fibers_with_cofiber(gamma, p, ell):
    """Return list of (w_k, mu_k, fiber_pts, cofiber_pts) for cosets with mu>=3."""
    F = GF(p); g = F.multiplicative_generator(); n = (p-1)//ell
    zeta = g**n; H = [zeta**j for j in range(ell)]
    gam = [F(c) for c in gamma]
    res = []
    for i in range(n):
        b = g**i
        coset = [b*h for h in H]
        tally = {}
        for x in coset:
            val = F(0)
            for r in range(ell-1,0,-1):
                val = (val+gam[r-1])*x
            tally.setdefault(val, []).append(x)
        mu = max(len(v) for v in tally.values())
        if mu < 3:
            continue
        modal = min((val for val,v in tally.items() if len(v)==mu), key=lambda z: int(z))
        fiber = tally[modal]
        fiberset = set(fiber)
        cofiber = [x for x in coset if x not in fiberset]
        res.append((b**ell, mu, fiber, cofiber))
    return res, F

def coeff_vec(poly_coeffs, ncols):
    v = [0]*ncols
    for d,c in enumerate(poly_coeffs):
        v[d] = c
    return v

def main():
    R.<X> = PolynomialRing(GF(2))  # placeholder, rebuilt per prime below
    for W in SATURATORS:
        ell, p = W["ell"], W["p"]
        fibers, F = excess_fibers_with_cofiber(W["gamma"], p, ell)
        Rx = PolynomialRing(F, 'X'); X = Rx.gen()
        ncols = ell-1  # degrees 0..ell-2
        E3 = sum(mu-2 for (_,mu,_,_) in fibers)
        K = len(fibers); P = sum(mu for (_,mu,_,_) in fibers)
        rows = []
        per_dim = []
        for (w, mu, fiber, cofiber) in fibers:
            hk = prod((X - x) for x in cofiber)      # co-fiber locator, deg = ell-mu
            assert hk.degree() == ell-mu
            dimk = 0
            for d in range(0, mu-1):                 # multipliers X^d, d=0..mu-2
                poly = (hk * X**d)
                cs = list(poly)                      # ascending coeffs
                rows.append(coeff_vec([int(c) for c in cs], ncols))
                dimk += 1
            per_dim.append(dimk)                     # = mu-1
        M = Matrix(F, rows)
        dimsum = M.rank()
        sum_dimVk = sum(per_dim)                     # = P-K
        print("="*88)
        print(" %s" % W["label"])
        print(" K=%d  P=%d  E_3=%d  sum dim V_k = P-K = %d" % (K, P, E3, sum_dimVk))
        print(" dim(V_1+...+V_K) = %d   [target: >= E_3=%d ?  %s;  tight (== E_3)? %s]"
              % (dimsum, E3, "YES" if dimsum >= E3 else "NO -- would BREAK the reduction",
                 dimsum == E3))
    print("="*88)
    return 0

import sys
sys.exit(main())
