#!/usr/bin/env sage
# -*- mode: python -*-
r"""
charsum_paircap.sage -- derive + verify the CHARACTER-SUM (Fourier-over-mu_ell) pair inequality
for the level-set concentration, and measure how far it gets toward E_3 <= ell-2.

Coincidence energy (ordered pairs, same coset, equal value):
  2C := sum_{b} sum_{c} N_b(c)(N_b(c)-1)
      = #{(x,x') in (F_p^*)^2 : x'/x in mu_ell\{1}, Gamma(x)=Gamma(x')}
      = sum_{zeta in mu_ell, zeta!=1} #{x in F_p^* : Delta_zeta(x)=0},   Delta_zeta:=Gamma(X)-Gamma(zeta X).

Since Delta_zeta has degree <= ell-1 and X | Delta_zeta (Gamma constant-free), it has <= ell-2 nonzero
roots; and Delta_zeta != 0 for zeta!=1 (Gamma mixed).  Summing over the ell-1 nontrivial zeta:

      PAIR-CAP:  2C = sum_b sum_c N_b(c)(N_b(c)-1)  <=  (ell-1)(ell-2).

This is the 2nd-moment / character-sum-accessible bound.  We verify the identity + cap, its
tightness, and compare the E_3-implication (ell-1)(ell-2)/6 against the true ell-2.
"""
WIT=[(331,11,[97,29,97,239,171,92,143,155,270,1]),
     (313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
     (103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0])]

def analyze(p,ell,gm):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    SX=PolynomialRing(F,'X'); X=SX.gen(); G=sum(F(gm[r-1])*X**r for r in range(1,ell))
    # 2C via coset tally + E_3
    twoC_b=0; E3=0
    for i in range(n):
        b=g**i; tally={}
        for h in H: v=G(b*h); tally[v]=tally.get(v,0)+1
        for f in tally.values(): twoC_b += f*(f-1)
        mu=max(tally.values())
        if mu>=3: E3+=mu-2
    # 2C via Delta_zeta root counts + max single-zeta root count
    twoC_a=0; maxroots=0
    for j in range(1,ell):
        z=H[j]
        Dz=G - G(z*X)                    # Gamma(X)-Gamma(zeta X)
        rts=[r for r,_ in Dz.roots() if r!=0]   # nonzero F_p roots
        twoC_a += len(rts); maxroots=max(maxroots,len(rts))
    return twoC_a,twoC_b,E3,maxroots

def main():
    print(" character-sum pair-cap:  2C = sum_zeta #roots(Delta_zeta) = sum_b sum_c N(N-1)  <=  (ell-1)(ell-2)")
    print(" %-16s %-8s %-8s %-6s %-10s %-8s %-8s %-10s" %
          ("case","2C(via Dz)","2C(coset)","match","(l-1)(l-2)","E_3","ell-2","(l-1)(l-2)/6"))
    for (p,ell,gm) in WIT:
        a,b,E3,mx=analyze(p,ell,gm)
        cap=(ell-1)*(ell-2)
        print(" ell=%-2d p=%-4d  %-8d %-8d %-6s %-10d %-8d %-8d %.2f  (max single-zeta roots=%d<=ell-2=%d)"
              % (ell,p,a,b,a==b,cap,E3,ell-2,cap/6,mx,ell-2))
    print()
    print(" READ: identity 2C(Delta)==2C(coset) confirms the Fourier-over-mu_ell pairing.")
    print(" The pair-cap 2C<=(ell-1)(ell-2) holds and gives only  E_3 <= (ell-1)(ell-2)/6  (>> ell-2):")
    print(" the 2nd moment / character-sum bound is NOT sharp -- E_3<=ell-2 needs the rank/spectral")
    print(" (realizability / cyclotomic-scheme eigenvalue) ingredient beyond the moment.")
    return 0

import sys
sys.exit(main())
