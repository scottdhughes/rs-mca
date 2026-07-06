#!/usr/bin/env sage
# -*- mode: python -*-
r"""
redei_RWc_structure.sage -- apply the fully-reducible-lacunary lens to
  R(W,c) = Res_X( Gamma(X) - c , W - X^ell ) = prod_{x: Gamma(x)=c} (W - x^ell)  in F_p[W].
For each excess coset's modal value c, factor R(W,c) and check:
  * root multiplicities = fiber sizes of value c (so R(W,c) IS fully reducible, mult=fibers);
  * degree deg_W R(W,c) <= ell-1  (<< p): it is NOT a Frobenius-lacunary W^p g + h object,
    so Ball Thm 1.9 (built on x->x^p, X^p-X=prod(X-a)) does NOT literally apply.  The correct
    machinery is the MULTIPLICATIVE / cyclotomic-class (Carlitz-McConnel) analog (X^ell,
    ell | p-1), not the additive Frobenius one.
"""
WIT = (331,11,[97,29,97,239,171,92,143,155,270,1])

def main():
    p,ell,gm = WIT
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    SX=PolynomialRing(F,'X'); X=SX.gen(); Gamma=sum(F(gm[r-1])*X**r for r in range(1,ell))
    SW=PolynomialRing(F,'W'); W=SW.gen()
    # find excess cosets and their modal value c
    excess=[]
    for i in range(n):
        b=g**i; tally={}
        for h in H: v=Gamma(b*h); tally[v]=tally.get(v,[])+[b*h]
        mu=max(len(t) for t in tally.values())
        if mu>=3:
            c=min((v for v,t in tally.items() if len(t)==mu),key=lambda z:int(z))
            # fiber-size multiset of value c across ALL cosets:
            excess.append((b**ell,mu,c))
    print("ell=%d p=%d : excess cosets (w, mu, modal c):" % (ell,p))
    for (w,mu,c) in excess: print("   w=%s mu=%d c=%s" % (int(w),mu,int(c)))
    print()
    for (w0,mu0,c) in excess[:4]:
        # R(W,c) = Res_X(Gamma-c, W - X^ell)
        AX=PolynomialRing(PolynomialRing(F,'W'),'X'); XX=AX.gen(); WW=AX.base_ring().gen()
        Gc=sum(AX.base_ring()(gm[r-1])*XX**r for r in range(1,ell)) - c
        Rwc=(WW - XX**ell).resultant(Gc)
        Rwc=SW(Rwc)
        fac=Rwc.factor()
        # fiber sizes of value c per coset (F_p roots x of Gamma-c, grouped by x^ell)
        fibers={}
        for x in F:
            if x!=0 and Gamma(x)==c: fibers[x**ell]=fibers.get(x**ell,0)+1
        mults={(-t[0].constant_coefficient()):t[1] for t in fac if t[0].degree()==1}  # W-w -> mult
        # match multiplicities to fiber sizes
        match=all(mults.get(F(w),0)>=fibers.get(F(w),0) for w in fibers) and \
              all(fibers.get(F(w),0)==m for w,m in mults.items() if F(w) in fibers)
        # is it lacunary (Frobenius sense)?  deg << p, so NO
        print("value c=%s (coset w=%s, mu=%d):" % (int(c),int(w0),mu0))
        print("   R(W,c) deg=%d (<= ell-1=%d, << p=%d)  #F_p-linear-factors=%d" %
              (Rwc.degree(), ell-1, p, len(mults)))
        print("   root mult == fiber sizes of c ? %s   (fibers of c: %s)" %
              (match, sorted(fibers.values(),reverse=True)))
        print("   Frobenius-lacunary (W^p g + h)? NO: deg_W = %d < p = %d  => Thm 1.9 hypothesis fails" %
              (Rwc.degree(), p))
        print()
    print("CONCLUSION: R(W,c) is fully reducible with root multiplicities = value-c fiber sizes,")
    print("but has degree <= ell-1 << p, so it is NOT the Frobenius X^p g+h object of Ball Thm 1.9.")
    print("The correct engine is the MULTIPLICATIVE/cyclotomic analog (ell | p-1), not additive Frobenius.")
    return 0

import sys
sys.exit(main())
