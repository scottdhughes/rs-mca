#!/usr/bin/env sage
# -*- mode: python -*-
r"""
extremal_structure_e3.sage -- dissect the E_3 = ell-2 SATURATING witnesses to expose the
exact extremal locus the KEY LEMMA proof (open K>=3 chart) must handle.

For each saturating Gamma we:
  * recover per-coset modal max-fibers (label w_b = b^ell, shared value c_b, points),
  * list the excess-carrying cosets (mu_b >= 3), confirm sum(mu_b - 2) = ell-2,
  * form the K excess fibers and compute, over GF(p):
      R    = rank of the coincidence rows { v(x)-v(anchor) },  v(x)=(x,..,x^{ell-1});
             realizable <=> R <= ell-2;  dim U = ell - R  (U = deg<=ell-1 polys const on
             each fiber; the note predicts extremal dim U = 2, i.e. R = ell-2);
      P    = sum mu_k,  delta = (P-K) - R  (note: extremal delta = K);
  * check EVERY pair (K=2 sub-config) has delta=0 (the PROVED K=2 case) -- i.e. the
    ceiling-saturating coupling is irreducibly >=3-way (lives exactly in the open chart).
"""

SATURATORS = [
    dict(label="ell=11 p=331 (E3=9=ell-2)", p=331, ell=11,
         gamma=[97,29,97,239,171,92,143,155,270,1]),
    dict(label="ell=13 p=313 (E3=11=ell-2)", p=313, ell=13,
         gamma=[254,289,29,276,242,219,201,261,79,232,133,1]),
    dict(label="ell=17 p=103 (E3=15=ell-2)", p=103, ell=17,
         gamma=[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
    dict(label="ell=17 p=409 (E3=14=ell-3, NON-saturator, for contrast)", p=409, ell=17,
         gamma=[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1]),
]

def coset_detail(gamma, p, ell):
    F = GF(p); g = F.multiplicative_generator(); n = (p-1)//ell
    zeta = g**n; H = [zeta**j for j in range(ell)]
    gam = [F(c) for c in gamma]
    out = []
    for i in range(n):
        b = g**i
        tally = {}
        for h in H:
            x = b*h
            val = F(0)
            for r in range(ell-1,0,-1):
                val = (val+gam[r-1])*x
            tally.setdefault(val, []).append(x)
        # modal max fiber (smallest value among those attaining the max, for determinism)
        mu = max(len(v) for v in tally.values())
        modal = min((val for val,v in tally.items() if len(v)==mu), key=lambda z: int(z))
        out.append(dict(rep=b, label=b**ell, mu=mu, cval=modal, pts=tally[modal]))
    return out, F

def coincidence_rank(fibers, F, ell):
    """rank of stacked { v(x)-v(anchor) }, v(x)=(x,...,x^{ell-1}); columns = ell-1."""
    rows = []
    for pts in fibers:
        if len(pts) < 2: continue
        x0 = pts[0]
        v0 = [x0**r for r in range(1, ell)]
        for x in pts[1:]:
            rows.append([x**r - v0[r-1] for r in range(1, ell)])
    if not rows:
        return 0
    return Matrix(F, rows).rank()

def main():
    for W in SATURATORS:
        ell, p = W["ell"], W["p"]
        det, F = coset_detail(W["gamma"], p, ell)
        excess_cosets = [d for d in det if d["mu"] >= 3]
        E3 = sum(d["mu"]-2 for d in excess_cosets)
        fibers = [d["pts"] for d in excess_cosets]
        K = len(fibers); P = sum(len(f) for f in fibers)
        R = coincidence_rank(fibers, F, ell)
        dimU = ell - R
        delta = (P - K) - R
        realizable = (R <= ell - 2)
        print("="*94)
        print(" %s" % W["label"])
        print("="*94)
        print(" excess-carrying cosets (mu>=3): K=%d,  sum(mu-2)=E_3=%d  (ell-2=%d)" % (K, E3, ell-2))
        print(" %-14s %-14s %-4s" % ("label w_b=b^ell", "value c_b", "mu_b"))
        for d in excess_cosets:
            print(" %-14s %-14s %-4d" % (int(d["label"]), int(d["cval"]), d["mu"]))
        print(" JOINT:  P=%d  K=%d  R(coincidence)=%d  realizable(R<=ell-2)=%s  dim U=%d  delta=(P-K)-R=%d"
              % (P, K, R, realizable, dimU, delta))
        print("         [note predicts saturator: dim U = 2 (R=ell-2), delta = K = %d]" % K)
        # pairwise: every K=2 sub-config should have delta=0 (PROVED case) => coupling is >=3-way
        pair_deltas = []
        allpairs_delta0 = True
        for i in range(K):
            for j in range(i+1, K):
                fij = [fibers[i], fibers[j]]
                Pij = len(fibers[i]) + len(fibers[j]); Rij = coincidence_rank(fij, F, ell)
                dij = (Pij - 2) - Rij
                pair_deltas.append(dij)
                if dij != 0: allpairs_delta0 = False
        print(" PAIRWISE: all %d pairs delta=0? %s   (max pair delta=%d)  ->  coupling is irreducibly >=3-way"
              % (len(pair_deltas), allpairs_delta0, max(pair_deltas) if pair_deltas else 0))
    return 0

import sys
sys.exit(main())
