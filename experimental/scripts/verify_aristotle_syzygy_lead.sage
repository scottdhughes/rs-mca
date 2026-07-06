#!/usr/bin/env sage
# -*- mode: python -*-
r"""
verify_aristotle_syzygy_lead.sage -- VERIFY Aristotle's lead (reviewer != generator):
every degree-bounded syzygy (q_k) of the co-fiber locators h_k is ALSO a syzygy of
  s_k := (Gamma - c_k)/g_k     (g_k = fiber locator, c_k = modal value; g_k | Gamma - c_k).
i.e.  Sum_k h_k q_k = 0  (deg q_k <= mu_k-2)  ==>  Sum_k s_k q_k = 0.
Also check the companion identity  Sum_k w_k q_k s_k == Sum_k c_k q_k h_k.
Tested on the E_3=ell-2 saturators.
"""
SATS=[(331,11,[97,29,97,239,171,92,143,155,270,1]),
      (313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
      (103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0])]

def main():
    for (p,ell,gm) in SATS:
        F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
        Rx=PolynomialRing(F,'X'); X=Rx.gen(); Gamma=sum(F(gm[r-1])*X**r for r in range(1,ell))
        fibers=[]  # (w, c, mu, g_k, h_k, s_k)
        for i in range(n):
            b=g**i; coset=[b*h for h in H]; tally={}
            for x in coset: tally.setdefault(Gamma(x),[]).append(x)
            mu=max(len(t) for t in tally.values())
            if mu<3: continue
            c=min((v for v,t in tally.items() if len(t)==mu),key=lambda z:int(z))
            fib=tally[c]; gk=prod((X-x) for x in fib); w=b**ell
            hk=(X**ell-w)//gk
            sk_num=Gamma-c; sk,rem=sk_num.quo_rem(gk)
            assert rem==0, "g_k must divide Gamma-c_k"
            fibers.append((w,c,mu,gk,hk,sk))
        K=len(fibers)
        # build Syz basis (left-kernel of rows = coeffs of h_k X^d, d<=mu_k-2)
        rows=[]; blocks=[]
        for k,(w,c,mu,gk,hk,sk) in enumerate(fibers):
            for d in range(mu-1):
                poly=hk*X**d
                rows.append([poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)]); blocks.append((k,d))
        M=Matrix(F,rows); basis=M.left_kernel().basis()
        # for each syzygy vector, reconstruct q_k and check Sum s_k q_k == 0 and companion identity
        all_szero=True; all_comp=True
        for v in basis:
            qs=[Rx(0)]*K
            for idx,(k,d) in enumerate(blocks): qs[k]+=v[idx]*X**d
            # sanity: it IS a syzygy of h_k
            assert sum(fibers[k][4]*qs[k] for k in range(K))==0
            s_syz=sum(fibers[k][5]*qs[k] for k in range(K))          # Sum s_k q_k
            comp=sum(fibers[k][0]*qs[k]*fibers[k][5] for k in range(K)) - \
                 sum(fibers[k][1]*qs[k]*fibers[k][4] for k in range(K))  # Sum w q s - Sum c q h
            if s_syz!=0: all_szero=False
            if comp!=0: all_comp=False
        print(" ell=%2d p=%3d : K=%d dim Syz=%d  ->  every syzygy of h_k is a syzygy of s_k? %s   companion id holds? %s"
              % (ell,p,K,len(basis), all_szero, all_comp))
    print("\n VERDICT: if both TRUE across saturators, Aristotle's lead is CONFIRMED (Syz(h) subset Syz(s),")
    print(" using the single-Gamma structure) -- a real narrowing of the syzygy space toward dim Syz <= K.")
    return 0

import sys
sys.exit(main())
