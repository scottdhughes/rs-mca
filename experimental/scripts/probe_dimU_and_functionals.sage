#!/usr/bin/env sage
# -*- mode: python -*-
r"""
probe_dimU_and_functionals.sage -- probe toward proving dim Syz <= K (= the paper's finite
"max-fiber inequality", Remark 16.10 / Prop 16.17 of CAP25 v13).

(A) U = {A in F_p[X] : deg A <= ell-1, A constant on each excess maximal fiber F_k}.
    Always {1, Gamma} subset U, so dim U >= 2. Test: is dim U == 2 always (invariant, useless),
    or does it VARY (discriminating)? Check the note identity  delta = P - ell - K + dim U.
(B) Candidate injective maps Syz -> F_p^K (if injective => dim Syz <= K). Test kernels of:
    - leading coeff (known to fail);
    - residue mod g_k : (q_k) -> (q_k mod g_k evaluated... ) -- fiber-localized;
    - value q_k(alpha_k) at a co-fiber anchor.
"""
CASES=[("SAT ell=11 p=331",331,11,[97,29,97,239,171,92,143,155,270,1]),
       ("SAT ell=13 p=313",313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
       ("SAT ell=17 p=103",103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
       ("nonsat ell=17 p=409",409,17,[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1])]

def build(p,ell,gm):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen(); Gamma=sum(F(gm[r-1])*X**r for r in range(1,ell))
    fibers=[]
    for i in range(n):
        b=g**i; coset=[b*h for h in H]; tally={}
        for x in coset: tally.setdefault(Gamma(x),[]).append(x)
        mu=max(len(t) for t in tally.values())
        if mu<3: continue
        c=min((v for v,t in tally.items() if len(t)==mu),key=lambda z:int(z))
        gk=prod((X-x) for x in tally[c]); w=b**ell; hk=(X**ell-w)//gk
        fibers.append((w,c,mu,tally[c],[x for x in coset if x not in set(tally[c])],gk,hk))
    return F,Rx,X,Gamma,fibers

def dimU(F,X,ell,fibers):
    # A = sum_{j=0}^{ell-1} a_j X^j constant on each fiber: A(x)-A(x0)=0
    rows=[]
    for (w,c,mu,fib,cof,gk,hk) in fibers:
        x0=fib[0]
        for x in fib[1:]:
            rows.append([x**j - x0**j for j in range(ell)])   # ell columns (deg 0..ell-1)
    if not rows: return ell
    return ell - Matrix(F,rows).rank()

def syz_basis(F,X,ell,fibers):
    rows=[]; blocks=[]
    for k,(w,c,mu,fib,cof,gk,hk) in enumerate(fibers):
        for d in range(mu-1):
            poly=hk*X**d
            rows.append([poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)]); blocks.append((k,d))
    return Matrix(F,rows).left_kernel().basis(), blocks

def main():
    print(" (A) dim U (constant-on-fibers), identity delta=P-ell-K+dimU, and whether dim U varies:")
    for (tag,p,ell,gm) in CASES:
        F,Rx,X,Gamma,fibers=build(p,ell,gm); K=len(fibers); P=sum(f[2] for f in fibers)
        E3=sum(f[2]-2 for f in fibers); dU=dimU(F,X,ell,fibers)
        basis,blocks=syz_basis(F,X,ell,fibers); dS=len(basis)
        delta=P-ell-K+dU
        print("   %-20s E_3=%2d K=%d P=%2d dimU=%d  delta(=P-l-K+dimU)=%d  dimSyz=%d  [dimU==2? %s]"
              % (tag,E3,K,P,dU,delta,dS,dU==2))
    # (B) candidate injective maps Syz->F_p^K on the ell=11 saturator
    print("\n (B) injectivity of candidate maps Syz -> F_p^K (kernel 0 => dim Syz<=K):")
    F,Rx,X,Gamma,fibers=build(331,11,[97,29,97,239,171,92,143,155,270,1]); K=len(fibers)
    basis,blocks=syz_basis(F,X,ell:=11,fibers)
    def qtuple(v):
        qs=[Rx(0)]*K
        for idx,(k,d) in enumerate(blocks): qs[k]+=v[idx]*X**d
        return qs
    # map candidates: for each syzygy, a K-vector
    def m_lead(v):  qs=qtuple(v); return [qs[k][fibers[k][2]-2] for k in range(K)]         # leading coeff
    def m_res0(v):  qs=qtuple(v); return [qs[k](0) for k in range(K)]                        # q_k(0)
    def m_gk(v):    qs=qtuple(v); return [ (qs[k] % fibers[k][5])(fibers[k][3][0]) for k in range(K)]  # q_k at a fiber pt
    def m_anchor(v):qs=qtuple(v); return [qs[k](fibers[k][4][0]) for k in range(K)]          # q_k at a co-fiber pt
    for name,mp in [("leading-coeff",m_lead),("q_k(0)",m_res0),("q_k@fiberpt",m_gk),("q_k@cofiberpt",m_anchor)]:
        img=Matrix(F,[mp(v) for v in basis]); r=img.rank()
        print("   %-16s: rank on Syz basis = %d / dim Syz = %d   injective? %s" % (name,r,len(basis),r==len(basis)))
    return 0

import sys; sys.exit(main())
