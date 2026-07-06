#!/usr/bin/env sage
# -*- mode: python -*-
r"""
syzygy_generators_e3.sage -- (a) explicit generators of the degree-bounded syzygy module
  Syz = { (q_1,...,q_K) : sum_k h_k q_k = 0,  deg q_k <= mu_k-2 }
at the E_3=ell-2 saturators, and (b)-input: test whether  dim Syz <= K  is a GENERAL fact
about pairwise-coprime co-fiber locators, or whether it NEEDS the common-Gamma realizability.

Map phi: (+)_k F_p[X]_{<=mu_k-2} -> F_p[X]_{<=ell-2}, (q_k) |-> sum_k h_k q_k.
Syz = left-kernel of M whose rows are the coeff vectors of {h_k X^d}.  dim Syz = (E_3+K)-rank M.

Outputs:
  * per saturator: dim Syz (expect K), and each generator printed as its (q_1,...,q_K) tuple,
    to expose structure / a candidate spanning set;
  * ARBITRARY-config stress: random distinct w_k + random mu_k-subsets (NOT from a common Gamma),
    report whether dim Syz ever EXCEEDS K (=> realizability hypothesis is essential).
Cross-check of dim Syz on a second engine (PARI) is in syzygy_xcheck.gp.
"""
import itertools

SATS = [
    dict(label="ell=11 p=331", p=331, ell=11, gamma=[97,29,97,239,171,92,143,155,270,1]),
    dict(label="ell=13 p=313", p=313, ell=13, gamma=[254,289,29,276,242,219,201,261,79,232,133,1]),
    dict(label="ell=17 p=103", p=103, ell=17, gamma=[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
]

def excess_fibers(gamma, p, ell):
    F = GF(p); g = F.multiplicative_generator(); n=(p-1)//ell
    zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen()
    Gamma = sum(F(gamma[r-1])*X**r for r in range(1,ell))
    res=[]
    for i in range(n):
        b=g**i; coset=[b*h for h in H]; tally={}
        for x in coset: tally.setdefault(Gamma(x),[]).append(x)
        mu=max(len(v) for v in tally.values())
        if mu<3: continue
        modal=min((val for val,v in tally.items() if len(v)==mu), key=lambda z:int(z))
        fs=set(tally[modal]); cof=[x for x in coset if x not in fs]
        res.append((b**ell, mu, cof))
    return res, F, Rx, X

def syz_from_fibers(fibers, F, Rx, X, ell):
    """rows = coeff vectors of h_k X^d; returns (M, block_index list, dimSyz, basis, K, E3)."""
    rows=[]; blocks=[]  # blocks[i] = (k, d)
    K=len(fibers); E3=0
    hks=[]
    for k,(w,mu,cof) in enumerate(fibers):
        E3 += mu-2
        hk = prod((X-x) for x in cof); hks.append(hk)
        for d in range(mu-1):
            poly = hk*X**d
            v=[poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)]
            rows.append(v); blocks.append((k,d))
    M=Matrix(F, rows)
    ker=M.left_kernel()
    return M, blocks, ker.dimension(), ker.basis(), K, E3, hks

def gen_to_tuple(vec, blocks, fibers, Rx, X):
    """reconstruct (q_0,...,q_{K-1}) polynomials from a left-kernel vector over the blocks."""
    K=len(fibers)
    qs=[Rx(0)]*K
    for idx,(k,d) in enumerate(blocks):
        qs[k]+= vec[idx]*X**d
    return qs

def main():
    for W in SATS:
        fibers, F, Rx, X = excess_fibers(W["gamma"], W["p"], W["ell"])
        M, blocks, dimSyz, basis, K, E3, hks = syz_from_fibers(fibers, F, Rx, X, W["ell"])
        print("="*92)
        print(" %s : K=%d  E_3=%d  dim Syz = %d   [KEY LEMMA needs dim Syz <= K = %d : %s]"
              % (W["label"], K, E3, dimSyz, K, "OK" if dimSyz<=K else "VIOLATION"))
        # verify each generator really is a syzygy, and print its (q_k) tuple degrees/support
        for gi, v in enumerate(basis):
            qs = gen_to_tuple(v, blocks, fibers, Rx, X)
            check = sum(hks[k]*qs[k] for k in range(K))
            degs = [ (qs[k].degree() if qs[k]!=0 else -1) for k in range(K) ]
            support = [k for k in range(K) if qs[k]!=0]
            print("   gen %d: valid(sum h_k q_k==0)=%s  supp(k)=%s  deg q_k=%s"
                  % (gi, check==0, support, degs))
        if W["ell"]==11:  # print the full generators for the smallest case
            print("   --- full generators (ell=11) ---")
            for gi,v in enumerate(basis):
                qs=gen_to_tuple(v,blocks,fibers,Rx,X)
                print("     gen %d: %s" % (gi, [Rx(q) for q in qs]))
    # ---- ARBITRARY-config stress: does dim Syz<=K hold WITHOUT a common Gamma? ----
    print("="*92)
    print(" ARBITRARY pairwise-coprime configs (random w_k + random mu_k-subsets, NO common Gamma):")
    import random
    for (ell,p) in [(7,211),(11,199),(13,313)]:
        F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell
        zeta=g**n; H=[zeta**j for j in range(ell)]
        Rx=PolynomialRing(F,'X'); X=Rx.gen()
        rng=random.Random(int(1234+ell))
        maxgap=-99; worst=None; ntest=0
        for _ in range(400):
            K=rng.randint(2,5)
            cos=rng.sample(range(n), K)
            sizes=[rng.randint(3,ell-1) for _ in range(K)]
            fibers=[]
            for c,mu in zip(cos,sizes):
                base=g**c; pts=[base*H[e] for e in range(ell)]
                fib=rng.sample(pts, mu); fs=set(fib); cof=[x for x in pts if x not in fs]
                fibers.append((base**ell, mu, cof))
            M,blocks,dimSyz,basis,Kk,E3,hks = syz_from_fibers(fibers,F,Rx,X,ell)
            ntest+=1
            if dimSyz-Kk>maxgap:
                maxgap=dimSyz-Kk; worst=(K,sizes,E3,dimSyz)
        print("   ell=%2d p=%3d: %d configs, max (dim Syz - K)=%d  (worst K,sizes,E3,dimSyz=%s)  "
              "-> %s" % (ell,p,ntest,maxgap,worst,
                         "arbitrary FAILS bound => realizability ESSENTIAL" if maxgap>0
                         else "no violation seen"))
    return 0

import sys
sys.exit(main())
