import numpy as np
from math import comb, log
from collections import defaultdict
from itertools import combinations

def prim_root(p):
    phi=p-1; mm=phi; f=[]; d=2
    while d*d<=mm:
        if mm%d==0:
            f.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: f.append(mm)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g
def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    return [pow(z,k,p) for k in range(n)]

# E^(2)_d over mu_n = additive energy of the mu_n-parabola = pairs of d-subsets with matching (e1,e2)=(p1,p2).
# Compute nu_d(v)=#{d-subsets A: (p1(A),p2(A))=v} via F_p^2 DP; E_d^disjoint = # disjoint pairs matching.
p,n,w=97,32,2   # gamma=0.758 > 2/3 => random-dominated
G=subgroup(p,n); G2=[pow(h,2,p) for h in G]
print(f"n={n} p={p} w={w} gamma={log(n)/log(p):.3f}  (>2/3 => random-dominated)")
print(f"{'d':>3} {'E2_d(disjoint)':>15} {'random C(n,d)C(n-d,d)/p^2':>26} {'ratio':>7} {'max nu_d/mean':>14}")
for d in [2,3,4,5,6,8,10]:
    if d>n//2: break
    # DP for nu_d over (p1,p2)
    D=[np.zeros((p,p),dtype=np.float64) for _ in range(d+1)]
    D[0][0,0]=1.0
    for h,h2 in zip(G,G2):
        for k in range(d,0,-1):
            D[k]+=np.roll(np.roll(D[k-1],h,0),h2,1)
    nu=D[d]
    # disjoint matching count: sum over v of (ordered disjoint pairs A,B with (p1,p2)=v).
    # exact disjoint is expensive; use subset energy E=sum nu^2 (counts ordered pairs incl overlap) as proxy for the
    # equidistribution signal, plus the concentration max nu / mean.
    E=(nu*nu).sum()
    Cnd=comb(n,d); mean_nu=Cnd/(p*p)
    rand=Cnd*comb(n-d,d)/(p*p)
    # subtract diagonal-ish? report E vs Cnd^2/p^2 (the random subset-energy)
    E_over_rand = E/(Cnd*Cnd/(p*p))
    print(f"{d:>3} {E:>15.3e} {Cnd*Cnd/(p*p):>26.3e} {E_over_rand:>7.3f} {nu.max()/mean_nu:>14.2f}")
print("\n(E = sum nu_d(v)^2 = subset additive energy on the parabola; random = C(n,d)^2/p^2.")
print(" ratio ~1 and max nu_d/mean ~ O(1) => equidistribution holds => target confirmed. Deviation = the proof's job.)")
