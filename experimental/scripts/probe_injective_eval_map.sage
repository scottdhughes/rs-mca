#!/usr/bin/env sage
# -*- mode: python -*-
r"""
probe_injective_eval_map.sage -- robustness test of the candidate proof of dim Syz <= K:
  the evaluation map  ev: Syz -> F_p^K,  (q_k) |-> (q_k(alpha_k))_k  is INJECTIVE.
If so, dim Syz <= K.  Proof target (kernel-trivial): Sum h_k q_k = 0, deg q_k<=mu_k-2,
q_k(alpha_k)=0 for all k  =>  all q_k = 0.

Test across saturators + non-saturator + random Gamma, and for several anchor choices
(fiber point, co-fiber point, several random points), to see whether injectivity is
robust / which anchors work.
"""
import random
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

def syz(F,Rx,X,ell,fibers):
    rows=[]; blocks=[]
    for k,f in enumerate(fibers):
        for d in range(f[2]-1):
            poly=f[6]*X**d
            rows.append([poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)]); blocks.append((k,d))
    basis=Matrix(F,rows).left_kernel().basis()
    def qt(v):
        qs=[Rx(0)]*len(fibers)
        for idx,(k,d) in enumerate(blocks): qs[k]+=v[idx]*X**d
        return qs
    return basis,qt

def test(tag,p,ell,gm):
    F,Rx,X,Gamma,fibers=build(p,ell,gm); K=len(fibers); basis,qt=syz(F,Rx,X,ell,fibers); dS=len(basis)
    rng=random.Random(int(p+ell))
    # anchor families
    fam={"fiber-pt":[f[3][0] for f in fibers],
         "cofiber-pt":[f[4][0] for f in fibers],
         "fiber-pt#2":[f[3][min(1,len(f[3])-1)] for f in fibers],
         "random-Fp*":[F(rng.randrange(1,p)) for _ in fibers]}
    res={}
    for name,alphas in fam.items():
        img=Matrix(F,[[qt(v)[k](alphas[k]) for k in range(K)] for v in basis]) if dS>0 else Matrix(F,0,K)
        res[name]=(img.rank(), img.rank()==dS)
    print("   %-20s dim Syz=%d K=%d  " % (tag,dS,K) +
          " ".join("%s:%d%s"%(n,r,"inj" if ok else "NO") for n,(r,ok) in res.items()))
    return res

def main():
    print(" ev: Syz -> F_p^K, (q_k)->(q_k(alpha_k)) ; rank==dim Syz => injective => dim Syz<=K :")
    for (tag,p,ell,gm) in CASES: test(tag,p,ell,gm)
    print("\n random Gamma (realizable, dim Syz<=K):")
    import random as _r
    for (p,ell) in [(199,11),(331,11),(313,13),(103,17)]:
        rng=_r.Random(int(9*p+ell))
        for t in range(3):
            gm=[rng.randrange(p) for _ in range(ell-1)]
            if not any(gm): continue
            test("rand ell=%d p=%d #%d"%(ell,p,t),p,ell,gm)
    print("\n READ: if the FIBER-PT (or cofiber-pt) anchor is injective across ALL configs, the map")
    print(" ev is the route: dim Syz<=K reduces to 'a degree-bounded syzygy vanishing at the K")
    print(" anchor points is zero' -- a concrete, non-circular proof target (use single-Gamma structure).")
    return 0

import sys; sys.exit(main())
