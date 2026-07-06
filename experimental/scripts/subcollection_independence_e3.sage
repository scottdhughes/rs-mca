#!/usr/bin/env sage
# -*- mode: python -*-
r"""
subcollection_independence_e3.sage -- test the candidate CLEAN proof route for the KEY LEMMA:

  CLAIM: the E_3 polynomials  { h_k * X^d : 1<=k<=K, 0<=d<=mu_k-3 }  (i.e. DROP the top
  monomial X^{mu_k-2} from each co-fiber-locator block) are F_p-linearly INDEPENDENT.

If true: dim(sum_k V_k) >= (that independent set) = E_3, which with the proven upper bound
dim(sum V_k) <= ell-2 gives the KEY LEMMA E_3 <= ell-2.  (Equivalently: the leading-coefficient
map Syz -> F_p^K is injective, so dim Syz <= K.)

Test: for saturators + random/planted Gamma at ell in {7,11,13,17}, compare
  rank{ h_k X^d : d<=mu_k-3 }  vs  E_3 = sum(mu_k-2).
Report any Gamma where rank < E_3 (would REFUTE this particular route).
"""
import itertools

def setup(p, ell):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell
    zeta=g**n; H=[zeta**j for j in range(ell)]
    return F,g,n,zeta,H

def excess(gamma,F,g,n,H,ell):
    Rx=PolynomialRing(F,'X'); X=Rx.gen()
    Gamma=sum(F(gamma[r-1])*X**r for r in range(1,ell))
    res=[]
    for i in range(n):
        b=g**i; coset=[b*h for h in H]; tally={}
        for x in coset: tally.setdefault(Gamma(x),[]).append(x)
        mu=max(len(v) for v in tally.values())
        if mu<3: continue
        modal=min((val for val,v in tally.items() if len(v)==mu),key=lambda z:int(z))
        fs=set(tally[modal]); cof=[x for x in coset if x not in fs]
        res.append((mu,cof))
    return res,F,Rx,X

def subcoll_rank(fibers,F,Rx,X,ell):
    rows=[]; E3=0
    for (mu,cof) in fibers:
        E3+=mu-2
        hk=prod((X-x) for x in cof)
        for d in range(mu-2):          # d = 0 .. mu-3  (DROP top monomial X^{mu-2})
            poly=hk*X**d
            rows.append([poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)])
    if not rows: return 0,0
    return Matrix(F,rows).rank(), E3

SATS=[(331,11,[97,29,97,239,171,92,143,155,270,1]),
      (313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
      (103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
      (409,17,[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1])]

def main():
    print(" SATURATORS / anchors:")
    for (p,ell,gm) in SATS:
        F,g,n,zeta,H=setup(p,ell); fibers,F,Rx,X=excess(gm,F,g,n,H,ell)
        r,E3=subcoll_rank(fibers,F,Rx,X,ell)
        print("   ell=%2d p=%3d: E_3=%d  rank{h_k X^d, d<=mu_k-3}=%d  independent? %s"
              % (ell,p,E3,r,"YES" if r==E3 else "NO (rank<E_3 -> route needs work)"))
    print(" RANDOM/PLANTED sweep (looking for rank < E_3, which would refute this route):")
    import random
    worst=None; nbad=0; ntot=0
    for (ell,p) in [(7,211),(7,337),(11,199),(11,331),(13,313),(17,103),(17,409)]:
        F,g,n,zeta,H=setup(p,ell)
        rng=random.Random(int(99+ell*7+p))
        maxgap=0
        for _ in range(1500):
            gm=[rng.randrange(p) for _ in range(ell-1)]
            if not any(gm): continue
            fibers,_,Rx,X=excess(gm,F,g,n,H,ell)
            if not fibers: continue
            r,E3=subcoll_rank(fibers,F,Rx,X,ell)
            ntot+=1
            if r<E3:
                nbad+=1;
                if E3-r>maxgap: maxgap=E3-r; worst=(ell,p,E3,r)
        print("   ell=%2d p=%3d: swept; running max (E_3 - rank)=%d" % (ell,p,maxgap))
    print("="*80)
    if nbad==0:
        print(" VERDICT: over %d Gamma, {h_k X^d: d<=mu_k-3} ALWAYS independent (rank==E_3)." % ntot)
        print("          => leading-coeff map Syz->F_p^K injective => dim Syz<=K => KEY LEMMA route HOLDS.")
    else:
        print(" VERDICT: %d/%d Gamma had rank<E_3 (worst %s) => this simple route is INCOMPLETE;" % (nbad,ntot,worst))
        print("          the dropped top monomials are sometimes needed. Route needs refinement.")
    return 0

import sys
sys.exit(main())
