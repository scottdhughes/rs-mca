#!/usr/bin/env sage
# -*- mode: python -*-
r"""
multiplicative_redei.sage -- build the MULTIPLICATIVE Redei polynomial of a Gamma-coset config
and read off its repeated-root / lacunary structure (the bridge to Redei-Szonyi lacunary theory).

  R(W,T) = Res_X( X^ell - W , T - Gamma(X) )  in F_p[W,T]
         = prod_{x : x^ell = W} (T - Gamma(x))          (degree ell in T)

A coset w_b has max-fiber mu_b >= 2  <=>  R(w_b,T) has a repeated root  <=>  D(w_b)=0, where
  D(W) = disc_T R(W,T)  in F_p[W].
Claims to test numerically:
  (i)   roots of D(W) (in F_p) = exactly the coset labels w_b with mu_b >= 2;
  (ii)  ord_{W=w_b} D(W) = coincidence count of coset b = sum_c C(f_c,2)  (f_c = fiber sizes);
  (iii) deg D(W) and the W-support of R(W,T) (lacunarity) -- the quantities the classical
        f=X^n g+h / slopes classification bounds. Compare witness vs random Gamma.
This is the constructive step: if the classical lacunary gap on R/D yields E_3<=ell-2, we win.
"""
CASES = [
    ("WITNESS ell=11 p=331", 331, 11, [97,29,97,239,171,92,143,155,270,1]),
    ("random  ell=11 p=331", 331, 11, None),   # filled below (E_3~0 contrast)
]

def coset_data(gamma, p, ell):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen(); G=sum(F(gamma[r-1])*X**r for r in range(1,ell))
    info={}  # w -> (mu, coincidence_count)
    for i in range(n):
        b=g**i; tally={}
        for h in H: v=G(b*h); tally[v]=tally.get(v,0)+1
        w=b**ell; mu=max(tally.values()); coinc=sum(f*(f-1)//2 for f in tally.values())
        info[F(w)]=(mu,coinc)
    return info,F,G,X

def build_redei(gamma, p, ell):
    F=GF(p)
    A=PolynomialRing(F,['W','T']); W,T=A.gens()
    AX=PolynomialRing(A,'X'); X=AX.gen()
    Gpoly=sum(A(gamma[r-1])*X**r for r in range(1,ell))
    f=X**ell - W
    g=T - Gpoly
    Rez=f.resultant(g)               # Res_X, in F_p[W,T], degree ell in T
    return Rez,A,W,T

def main():
    import random
    for (label,p,ell,gm) in CASES:
        F=GF(p)
        if gm is None:
            rng=random.Random(int(4242+p+ell)); gm=[rng.randrange(p) for _ in range(ell-1)]
            while not any(gm): gm=[rng.randrange(p) for _ in range(ell-1)]
        info,Ff,G,X = coset_data(gm,p,ell)
        E3=sum(mu-2 for (mu,_) in info.values() if mu>=3)
        Ctot=sum(c for (_,c) in info.values())
        concentrated={w:(mu,c) for w,(mu,c) in info.items() if mu>=2}
        Rez,A,W,T = build_redei(gm,p,ell)
        # structure of R(W,T)
        degT=Rez.degree(T); degW=Rez.degree(W)
        # discriminant in T -> D(W) in F_p[W]
        SW=PolynomialRing(F,'w'); w=SW.gen()
        D_AT = Rez.discriminant(T)               # element of F_p[W,T] with no T
        D = SW({m.degrees()[0]:c for m,c in zip(D_AT.monomials(), D_AT.coefficients())}) if D_AT!=0 else SW(0)
        print("="*90)
        print(" %s :  E_3=%d  coincidences C=%d  #cosets{mu>=2}=%d" % (label,E3,Ctot,len(concentrated)))
        print("   R(W,T): deg_T=%d (=ell)  deg_W=%d   #monomials=%d" % (degT,degW,len(Rez.monomials())))
        if D==0:
            print("   D(W)=disc_T R == 0  (R not separable in T generically)"); continue
        print("   D(W)=disc_T R:  deg=%d   nonzero-in-F_p-roots checked below" % D.degree())
        fac=D.factor()
        # (i) roots of D vs concentrated cosets ; (ii) multiplicity vs coincidence count
        linroots={(-t[0].constant_coefficient()/t[0][1]):t[1] for t in fac if t[0].degree()==1}
        # match: does every concentrated coset appear as a root, with mult == coincidence count?
        match_i=all(w0 in linroots for w0 in concentrated)
        match_ii=all(linroots.get(w0,None)==c for w0,(mu,c) in concentrated.items())
        extra=[r for r in linroots if r not in concentrated]
        print("   (i)  every mu>=2 coset is a root of D(W)?           %s" % match_i)
        print("   (ii) root multiplicity == coset coincidence count?  %s   (extra F_p roots: %d)"
              % (match_ii, len(extra)))
        print("   deg D = %d ; sum coincidence counts = %d ; (2 deg_W(coeffs) route: R deg_W=%d)"
              % (D.degree(), Ctot, degW))
    print("="*90)
    print(" If (i)&(ii) hold: the level-set problem = the repeated-root locus of ONE bivariate")
    print(" Redei polynomial R(W,T); E_3 is read from D(W)'s factorization. Next: bound via the")
    print(" classical f=X^n g+h / (Xg+h)(h'g-g'h) lacunary mechanism applied to R (or D).")
    return 0

import sys
sys.exit(main())
