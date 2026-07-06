#!/usr/bin/env sage
# -*- mode: python -*-
r"""
moment_hierarchy_e3.sage -- scope the high-moment (Gamma_r) route to E_3 <= ell-2 (CAP25 v13
route A).  M_r := sum_b sum_c N_b(c)^r = #{(x_1..x_r): x_i^ell all equal, Gamma(x_i) all equal}
(r-fold coincidence count).  mu_b = max_c N_b(c), so (sum_c N_b(c)^r)^{1/r} -> mu_b as r->inf,
and B_r := sum_b ((sum_c N_b(c)^r)^{1/r} - 2)_+ is an upper bound for E_3 converging DOWN to it.

Questions this answers:
 (1) how fast does B_r -> E_3 (= the 'r* needed' to make the moment bound sharp, <= ell-2)?
 (2) M_r growth: extremal (E_3=ell-2) vs random (E_3~0) -- where do they diverge?
 (3) the character-sum barrier: M_r main term (mean^r) vs the max-fiber tail.
"""
import random
def fiberdata(gm,p,ell):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen(); G=sum(F(gm[r-1])*X**r for r in range(1,ell))
    per=[]  # per coset: list of fiber sizes N_b(c)
    for i in range(n):
        b=g**i; t={}
        for h in H: t[G(b*h)]=t.get(G(b*h),0)+1
        per.append(sorted(t.values(),reverse=True))
    return per,n

def Mr(per,r):  # global r-th coincidence moment
    return sum(sum(N**r for N in fibs) for fibs in per)
def E3(per):    return sum(max(f)-2 for f in per if max(f)>=3)
def Br(per,r):  # moment-r upper bound for E_3
    return sum((RR(sum(N**r for N in fibs))**(1/r) - 2) for fibs in per if (RR(sum(N**r for N in fibs))**(1/r))>2)

def main():
    SAT=[("SAT ell=11 p=331",331,11,[97,29,97,239,171,92,143,155,270,1]),
         ("SAT ell=17 p=103",103,17,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0])]
    print(" (1)+(2) moment bound B_r (upper bound for E_3, -> E_3 as r grows) and M_r growth:")
    for (tag,p,ell,gm) in SAT:
        per,n=fiberdata(gm,p,ell); e3=E3(per)
        print("  %-18s E_3=%d (ell-2=%d), n=%d cosets" % (tag,e3,ell-2,n))
        row=[]
        for r in [2,3,4,6,8,12,16,24,32]:
            br=Br(per,r); mr=Mr(per,r)
            sharp = "<=ell-2" if br<=ell-2+1e-9 else ""
            row.append("r=%d:B=%.2f%s" % (r,br,("*" if sharp else "")))
        print("      "+"  ".join(row)+"    (B_r decreases to E_3; * = B_r<=ell-2)")
        # random contrast at same p,ell
        rng=random.Random(int(p+ell)); gmr=[rng.randrange(p) for _ in range(ell-1)]
        perr,_=fiberdata(gmr,p,ell)
        print("      random E_3=%d: B_2=%.2f B_4=%.2f B_8=%.2f (collapses fast)"
              % (E3(perr),Br(perr,2),Br(perr,4),Br(perr,8)))
    print("\n (3) the barrier: M_r main term vs max-fiber tail (ell=11 p=331 saturator):")
    per,n=fiberdata([97,29,97,239,171,92,143,155,270,1],331,11)
    p,ell=331,11
    for r in [2,4,8,16]:
        mr=Mr(per,r)
        # 'uniform' main term: if every coset had all N=1 it'd be n*ell; the mean fiber contributes
        main = n*ell   # trivial lower part (all singletons) is n*ell for r>=1 sum N = n*ell...
        maxfib_tail = sum(max(f)**r for f in per)   # contribution of the max fiber per coset
        print("   r=%2d: M_r=%d ; max-fiber tail sum mu_b^r = %d (%.1f%% of M_r)"
              % (r,mr,maxfib_tail,100.0*maxfib_tail/mr))
    print("\n READ: B_r is the moment upper bound for E_3; the r where B_r<=ell-2 is the 'r*' the")
    print(" moment method needs.  If r* is small (single digits) for our toy ell, the hierarchy is")
    print(" a viable finite route; the open problem is BOUNDING M_r (r-fold coincidence count) by")
    print(" character sums sharply enough at that r -- the sqrt(p)-barrier question.")
    return 0

import sys; sys.exit(main())
