#!/usr/bin/env sage
# -*- mode: python -*-
r"""
pencil_monodromy.sage -- Galois/monodromy of the pencil P_t(X) = X^ell - t*Gamma(X) over F_p(t),
i.e. of the degree-ell map psi: X -> X^ell/Gamma(X) whose fibers psi^{-1}(t_0) are the roots of
X^ell - t_0 Gamma.  Sample Frobenius cycle types by factoring X^ell - t_0 Gamma over F_p for all
t_0 in F_p^*, to determine G = Gal(X^ell - t*Gamma / F_p(t)) <= S_ell.

Test whether EXTREMAL Gamma (E_3 = ell-2) have SPECIAL/small monodromy vs RANDOM Gamma (full S_ell)
-- a computable rigidity / inverse-theorem criterion (structure detection).  ell prime => any
transitive G is primitive; a primitive G with a transposition is S_ell (Jordan).
"""
import random
def E3_of(gm,p,ell):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen(); G=sum(F(gm[r-1])*X**r for r in range(1,ell))
    E3=0
    for i in range(n):
        b=g**i; t={}
        for h in H: t[G(b*h)]=t.get(G(b*h),0)+1
        mu=max(t.values())
        if mu>=3: E3+=mu-2
    return E3

def monodromy(gm,p,ell):
    F=GF(p); Rx=PolynomialRing(F,'X'); X=Rx.gen()
    G=sum(F(gm[r-1])*X**r for r in range(1,ell))
    types={}; nbranch=0; nirred=0; ntransp=0
    for t0 in range(1,p):
        f=X**ell - F(t0)*G
        if f.degree()<ell: continue
        fac=f.factor()
        if any(e>1 for _,e in fac): nbranch+=1; continue        # non-squarefree: branch point
        degs=tuple(sorted((fp.degree() for fp,_ in fac),reverse=True))
        types[degs]=types.get(degs,0)+1
        if degs==(ell,): nirred+=1                               # ell-cycle => transitive
        if sorted(degs)==sorted([2]+[1]*(ell-2)): ntransp+=1     # a transposition
    transitive = nirred>0
    # ell prime: transitive => primitive; + a transposition => S_ell (Jordan)
    if transitive and ntransp>0: grp="S_%d (transposition+primitive)"%ell
    elif transitive:
        # no transposition seen: could be A_ell, or a small primitive (affine/Frobenius/dihedral)
        # discriminator: does every cycle type have all parts equal (=> Frobenius/regular-ish)?
        allreg=all(len(set(dt))==1 for dt in types)
        grp=("small-primitive/affine? (no transposition; %d distinct types%s)"
             %(len(types)," ; regular-like" if allreg else ""))
    else: grp="INTRANSITIVE (psi decomposes)"
    return grp,len(types),nbranch,transitive,ntransp,dict(sorted(types.items(),key=lambda kv:-kv[1])[:6])

def main():
    SAT=[("SAT ell=11 p=331",331,11,[97,29,97,239,171,92,143,155,270,1]),
         ("SAT ell=13 p=313",313,13,[254,289,29,276,242,219,201,261,79,232,133,1]),
         ("SAT ell=17 p=103",103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0])]
    print(" Monodromy G = Gal(X^ell - t*Gamma / F_p(t)) via Frobenius cycle-type sampling:")
    print(" -- EXTREMAL (E_3=ell-2) Gamma --")
    for (tag,p,ell,gm) in SAT:
        E3=E3_of(gm,p,ell); grp,nt,nb,tr,ntr,top=monodromy(gm,p,ell)
        print("   %-18s E_3=%d  G = %s" % (tag,E3,grp))
        print("        #cycle-types=%d  #branch(t0)=%d  transitive=%s  #transpositions=%d" % (nt,nb,tr,ntr))
        print("        top cycle types: %s" % {str(list(k)):v for k,v in top.items()})
    print(" -- RANDOM Gamma (E_3 ~ 0) for contrast --")
    for (p,ell) in [(331,11),(313,13),(103,17)]:
        rng=random.Random(int(5*p+ell))
        for _ in range(2):
            gm=[rng.randrange(p) for _ in range(ell-1)]
            if not any(gm): continue
            E3=E3_of(gm,p,ell); grp,nt,nb,tr,ntr,top=monodromy(gm,p,ell)
            print("   rand ell=%2d p=%3d E_3=%d  G = %s  (#types=%d transpositions=%d)" % (ell,p,E3,grp,nt,ntr))
    print("\n READ: if extremal Gamma have SMALL/special monodromy (no transposition => not S_ell)")
    print(" while random Gamma give S_ell, that is the rigidity signal: large E_3 <=> structured")
    print(" pencil monodromy (the inverse-theorem / block-structure route), computably detected.")
    return 0

import sys; sys.exit(main())
