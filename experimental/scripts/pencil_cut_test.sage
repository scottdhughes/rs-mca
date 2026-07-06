#!/usr/bin/env sage
# -*- mode: python -*-
r"""
pencil_cut_test.sage -- does the pencil lead actually CUT Syz, or is Sum s_k q_k = 0 a dependent
consequence of Sum h_k q_k = 0 (hence useless as an extra constraint)?

Pencil: F_t := X^ell - t*Gamma,  b_k(t) := w_k - t*c_k,  and  F_t - b_k(t) = g_k*(h_k - t*s_k).
So the K fibers are common level sets of the whole pencil {F_t}.

Test on saturators + the non-saturator: compute
  dim Syz(h)                         = original syzygies,
  dim( Syz(h) & {Sum s_k q_k = 0} )  = adding the s-condition,
  dim( Syz(h) & s & u )              u_k = w_k s_k - c_k h_k (companion),
  dim( Syz(h) & s & u & Gamma^2 )    one more derived multiplier.
If all equal dim Syz(h), the pencil conditions are DEPENDENT (no cut) -- honest negative.
Also verify the pencil identity F_t - b_k(t) == g_k (h_k - t s_k).
"""
CASES=[(331,11,[97,29,97,239,171,92,143,155,270,1]),
       (313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
       (103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
       (409,17,[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1])]  # non-saturator

def dim_with_constraints(fibers, F, Rx, X, ell, extra_polys_list):
    """dim of {(q_k): deg q_k<=mu_k-2, and for each family P in extra_polys_list, Sum P_k q_k = 0}."""
    K=len(fibers)
    # unknown coeff layout: block k has mu_k-1 coeffs (X^0..X^{mu_k-2})
    blocks=[mu-1 for (_,_,mu,_,_,_) in fibers]; ncols=sum(blocks); offs=[sum(blocks[:k]) for k in range(K)]
    rows=[]
    for polys in extra_polys_list:            # each family gives a linear map to F_p[X]_{<=2ell}
        # Sum_k polys[k]*q_k = 0  -> collect coeff of each X^power as a linear form in the unknowns
        maxdeg=max((polys[k].degree() if polys[k]!=0 else -1)+(fibers[k][2]-2) for k in range(K))
        M={}  # power -> row (length ncols)
        for k in range(K):
            Pk=polys[k]
            if Pk==0: continue
            for d in range(fibers[k][2]-1):    # q_k = X^d contributes Pk*X^d
                col=offs[k]+d
                for j,co in enumerate(list(Pk*X**d)):
                    M.setdefault(j,[F(0)]*ncols)
                    M[j][col]=co
        for row in M.values(): rows.append(row)
    if not rows: return ncols
    return ncols - Matrix(F,rows).rank()

def main():
    print(" %-22s %-8s %-10s %-12s %-14s" % ("case","dimSyz(h)","+s","+s+u","+s+u+Gamma^2"))
    for (p,ell,gm) in CASES:
        Fp=GF(p); g=Fp.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; Hs=[zeta**j for j in range(ell)]
        Rx=PolynomialRing(Fp,'X'); X=Rx.gen(); Gamma=sum(Fp(gm[r-1])*X**r for r in range(1,ell))
        fibers=[]
        for i in range(n):
            b=g**i; coset=[b*h for h in Hs]; tally={}
            for x in coset: tally.setdefault(Gamma(x),[]).append(x)
            mu=max(len(t) for t in tally.values())
            if mu<3: continue
            c=min((v for v,t in tally.items() if len(t)==mu),key=lambda z:int(z))
            gk=prod((X-x) for x in tally[c]); w=b**ell; hk=(X**ell-w)//gk; sk=(Gamma-c)//gk
            fibers.append((w,c,mu,gk,hk,sk))
        K=len(fibers)
        # pencil identity check
        pid_ok=all((X**ell - fibers[k][0]) - (fibers[k][1])*Gamma  # this is wrong ordering; check properly below
                   is not None for k in range(K))
        # correct identity: F_t - b_k(t) = g_k(h_k - t s_k); check at t=1 symbolically:
        t=Fp(1)
        pid_ok=all((X**ell - t*Gamma) - (fibers[k][0]-t*fibers[k][1]) == fibers[k][3]*(fibers[k][4]-t*fibers[k][5]) for k in range(K))
        Hf=[f[4] for f in fibers]; Sf=[f[5] for f in fibers]
        Uf=[fibers[k][0]*fibers[k][5]-fibers[k][1]*fibers[k][4] for k in range(K)]      # u_k=w s - c h
        G2=[(Gamma*fibers[k][5])%1 if False else (Gamma*fibers[k][5]) for k in range(K)] # Gamma*s_k (deg may exceed)
        d_h   = dim_with_constraints(fibers,Fp,Rx,X,ell,[Hf])
        d_hs  = dim_with_constraints(fibers,Fp,Rx,X,ell,[Hf,Sf])
        d_hsu = dim_with_constraints(fibers,Fp,Rx,X,ell,[Hf,Sf,Uf])
        d_all = dim_with_constraints(fibers,Fp,Rx,X,ell,[Hf,Sf,Uf,G2])
        tag="SAT" if (fibers and sum(m-2 for (_,_,m,_,_,_) in fibers)==ell-2) else "non-sat"
        print(" ell=%-2d p=%-4d %-6s %-8d %-10d %-12d %-14d  (K=%d, pencil-id=%s)"
              % (ell,p,tag,d_h,d_hs,d_hsu,d_all,K,pid_ok))
    print("\n If +s, +s+u, ... all EQUAL dimSyz(h): the pencil conditions are DEPENDENT (no cut) --")
    print(" the s_k lead reframes the crux (pencil F_t=X^ell-tGamma, common fibers) but does not,")
    print(" by itself, reduce dim Syz. dim Syz<=K stays open; deeper route = pencil-geometry count.")
    return 0

import sys
sys.exit(main())
