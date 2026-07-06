#!/usr/bin/env python3
r"""verify_l1_e3_flint_crosscheck.py -- INDEPENDENT (python-flint / FLINT) cross-check of the
load-bearing L1 results, from scratch (own primitive root, own F_p polynomial + matrix arithmetic;
engine independent of Sage's linbox and PARI). Run: ~/math_code/.venv/bin/python3 <this>.

Re-verifies at the E_3=ell-2 saturators:
  (1) spectra + E_3 (independent recompute of the coset level sets);
  (2) structural: g_k h_k = X^ell - w_k  and  Gamma = c_k + g_k s_k (g_k | Gamma-c_k);
  (3) UPPER-HALF PROOF CORE: [X^{ell-1}]( h_k X^d Gamma ) = 0 for 0<=d<=mu_k-2;
  (4) dim(sum V_k) = rank{h_k X^d} = E_3  and  <= ell-2  (=> dim Syz = (E_3+K)-rank = K).
"""
from flint import nmod_poly, nmod_mat

def primitive_root(p):
    # factor p-1
    m=p-1; fac=set(); d=2
    while d*d<=m:
        while m%d==0: fac.add(d); m//=d
        d+=1
    if m>1: fac.add(m)
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in fac): return g
    raise RuntimeError

def poly(coeffs,p): return nmod_poly([c%p for c in coeffs],p)

def main():
    SATS=[(331,11,[97,29,97,239,171,92,143,155,270,1]),
          (313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
          (103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0])]
    X=lambda p: nmod_poly([0,1],p)
    allok=True
    for (p,ell,gm) in SATS:
        g=primitive_root(p); n=(p-1)//ell; zeta=pow(g,n,p)
        H=[pow(zeta,j,p) for j in range(ell)]
        # Gamma coeffs: gm[r-1] = gamma_r, r=1..ell-1 ; constant term 0
        gcoeffs=[0]+[gm[r-1] for r in range(1,ell)]
        Gam=poly(gcoeffs,p)
        # (1) spectra + E_3, and collect excess fibers
        E3=0; K=0; fibers=[]   # (w,c,mu,fiber_pts,cofiber_pts)
        for i in range(n):
            b=pow(g,i,p); coset=[(b*h)%p for h in H]; tally={}
            for x in coset:
                v=int(Gam(x)); tally.setdefault(v,[]).append(x)
            mu=max(len(t) for t in tally.values())
            if mu<3: continue
            c=min(v for v,t in tally.items() if len(t)==mu)
            fib=tally[c]; fs=set(fib); cof=[x for x in coset if x not in fs]
            fibers.append(((b**ell)%p if False else pow(b,ell,p), c, mu, fib, cof)); E3+=mu-2; K+=1
        # build per-fiber g_k,h_k,s_k and run checks (2),(3)
        struct_ok=True; vanish_ok=True; rows=[]
        Xp=poly([0]*ell+[1],p)   # X^ell
        for (w,c,mu,fib,cof) in fibers:
            gk=poly([1],p)
            for x in fib: gk=gk*poly([(-x)%p,1],p)
            hk=poly([1],p)
            for x in cof: hk=hk*poly([(-x)%p,1],p)
            # (2a) g_k h_k = X^ell - w
            lhs=gk*hk; rhs=Xp - poly([w],p)
            if lhs!=rhs: struct_ok=False
            # (2b) Gamma - c divisible by g_k, s_k = quotient
            q,r=divmod(Gam - poly([c],p), gk)
            if r!=nmod_poly([],p) and r!=poly([0],p): struct_ok=False
            sk=q
            # (3) [X^{ell-1}](h_k X^d Gamma)=0 for d=0..mu-2
            for d in range(mu-1):
                prod=hk*poly([0]*d+[1],p)*Gam
                coeff=int(prod[ell-1]) if prod.degree()>=ell-1 else 0
                if coeff!=0: vanish_ok=False
            # rows for rank: coeffs of h_k X^d, degrees 0..ell-2
            for d in range(mu-1):
                pdp=hk*poly([0]*d+[1],p)
                rows.append([int(pdp[j]) for j in range(ell-1)])
        # (4) rank over F_p via FLINT nmod_mat
        Mrank = nmod_mat(rows,p).rank() if rows else 0
        dimSyz=(E3+K)-Mrank
        ok = struct_ok and vanish_ok and (Mrank==E3) and (Mrank<=ell-2) and (dimSyz==K)
        allok = allok and ok
        print(" ell=%2d p=%3d : E_3=%d K=%d | struct(g_k h_k=X^l-w, g_k|Gamma-c)=%s | "
              "[X^{l-1}](h_k X^d Gamma)=0 =%s | rank(sumV)=%d(=E_3? %s, <=l-2=%d? %s) dimSyz=%d(=K? %s) -> %s"
              % (ell,p,E3,K,struct_ok,vanish_ok,Mrank,Mrank==E3,ell-2,Mrank<=ell-2,dimSyz,dimSyz==K,
                 "PASS" if ok else "FAIL"))
    print("="*100)
    print(" FLINT independent cross-check: %s" %
          ("ALL LOAD-BEARING RESULTS REPRODUCED (upper half + dim Syz=K)" if allok else "MISMATCH"))
    return 0 if allok else 1

import sys; sys.exit(main())
