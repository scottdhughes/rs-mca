#!/usr/bin/env sage
# -*- mode: python -*-
r"""
moment_charsum_test.sage -- STEP 2: does the character-sum bound on M_r deliver B_r <= ell-2?

M_r = sum_x K(x)^{r-1}, K(x) = #{zeta in mu_ell : Gamma(x zeta)=Gamma(x)}.  Expanding via additive
characters, the r-fold coincidence count is governed by the Weil sums
   S(t, zeta) = sum_{x in F_p^*} e_p( t * Delta_zeta(x) ),  Delta_zeta(X)=Gamma(X)-Gamma(zeta X),
(the r=2 / pair frequencies; higher r use products).  Test:
 (1) character MAXIMA  max_{t!=0, zeta!=1} |S(t,zeta)|  vs the Weil bound (ell-2)sqrt(p) and sqrt(p):
     do they hit the sqrt(p) barrier?  (index structure would push them below.)
 (2) Parseval:  sum_{t,zeta} |S|^2  vs  p * (M_2 - main)  -- is the L^2 bound CIRCULAR?
 (3) the naive per-frequency bound on M_r: error ~ (#freq) * charmax; does it swamp M_r (=> the
     per-frequency / Wan-index route is INSUFFICIENT, and joint cancellation / inverse theorem needed)?
"""
def setup(gm,p,ell):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen(); G=sum(F(gm[r-1])*X**r for r in range(1,ell))
    return F,Rx,X,G,H,n
def K_and_M(G,F,p,ell,H,n,r):
    # K(x)=#{zeta: Gamma(x zeta)=Gamma(x)}; M_r = sum_x K(x)^{r-1}
    Mr=0; perK=[]
    for x in F:
        if x==0: continue
        gx=G(x); k=sum(1 for z in H if G(x*z)==gx); perK.append(k); Mr+=k**(r-1)
    return Mr,perK

def charsums(G,Rx,X,F,p,ell,H):
    zc=CDF(0)  # use exact roots of unity via CDF for |.|
    import cmath
    w=CDF(exp(2*pi*I/p))
    Smax=0.0; L2=0.0; cnt=0
    e=[CDF(exp(2*pi*I*a/p)) for a in range(p)]
    for zi in range(1,ell):
        z=H[zi]; Dz=G - G(z*X)                       # Delta_zeta
        for t in range(1,p):
            S=CDF(0)
            for x in F:
                if x==0: continue
                S+=e[int(F(t)*Dz(x))]
            aS=abs(S); Smax=max(Smax,aS); L2+=aS*aS; cnt+=1
    return Smax,L2,cnt

def main():
    for (tag,p,ell,gm) in [("SAT ell=11 p=331",331,11,[97,29,97,239,171,92,143,155,270,1])]:
        F,Rx,X,G,H,n=setup(gm,p,ell)
        M2,perK=K_and_M(G,F,p,ell,H,n,2)
        # E_3 from perK: per coset max K; but perK is per-x; group not needed for the barrier test
        Smax,L2,cnt=charsums(G,Rx,X,F,p,ell,H)
        sq=RR(p).sqrt()
        print(" %s :" % tag)
        print("   char MAXIMA max|S(t,zeta)| = %.1f    Weil (ell-2)sqrt(p)=%.1f   sqrt(p)=%.1f   (ratio to sqrt p: %.2f)"
              % (Smax,(ell-2)*sq,sq,Smax/sq))
        print("   Parseval: sum|S|^2 = %.0f  ;  p*(M_2-(p-1)) = %.0f   [equal? => L^2 is CIRCULAR]"
              % (L2, p*(M2-(p-1))))
        # naive per-frequency bound on M_r error, using char max:
        print("   #frequencies (t,zeta) = %d ; naive per-freq error on M_2 ~ (#freq)*charmax/p = %.0f  vs true M_2=%d"
              % (cnt, cnt*Smax/p, M2))
        # random contrast
    print()
    gmr=[GF(331)(v) for v in [17,204,3,88,251,140,199,66,31,7]]
    F,Rx,X,G,H,n=setup([17,204,3,88,251,140,199,66,31,7],331,11)
    Smax,L2,cnt=charsums(G,Rx,X,F,331,11,H); sq=RR(331).sqrt()
    print(" random ell=11 p=331: char maxima = %.1f (ratio to sqrt p: %.2f)  vs extremal above" % (Smax,Smax/sq))
    print("\n READ: if char maxima ~ sqrt(p) for BOTH extremal and random, the per-frequency (Weil/Wan-")
    print(" index) bound cannot separate them / cannot beat sqrt(p); with error accumulating over")
    print(" #freq ~ ell*p frequencies, the per-frequency route is INSUFFICIENT -> the route needs")
    print(" JOINT cancellation (additive-combinatorics inverse theorem, BGK), NOT per-sum index bounds.")
    return 0

import sys; sys.exit(main())
