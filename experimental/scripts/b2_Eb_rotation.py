import numpy as np
from itertools import combinations
from collections import Counter, defaultdict

def prim_root(p):
    phi=p-1; m=phi; f=[]; d=2
    while d*d<=m:
        if m%d==0:
            f.append(d)
            while m%d==0: m//=d
        d+=1
    if m>1: f.append(m)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g

def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    pts=[]; cur=1
    for _ in range(n): pts.append(cur); cur=cur*z%p
    return pts

def analyze(p,n,m,w):
    pts=subgroup(p,n)
    # fiber values nu(v): v=(p_1..p_w) mod p for each m-subset; count
    nu=Counter()
    N0=0
    minus = n//2   # index shift: -a = z^{n/2} * a => index k -> (k+n/2)%n
    sym_fiber0=0
    for S in combinations(range(n),m):
        v=tuple(sum(pts[(j*k)%n] for k in S)%p for j in range(1,w+1))
        nu[v]+=1
    N=nu[tuple([0]*w)]
    mean=sum(v for v in nu.values())/ (p**w)   # C(n,m)/p^w
    E=sum(c*c for c in nu.values())
    # rotation-orbit check: for v!=0, values come in n-orbits with equal nu
    # count how many m-subsets S at v=0 are mu_2-symmetric (S=-S)
    for S in combinations(range(n),m):
        v=tuple(sum(pts[(j*k)%n] for k in S)%p for j in range(1,w+1))
        if any(v): continue
        Sset=set(S); sym=all(((k+minus)%n) in Sset for k in S)
        if sym: sym_fiber0+=1
    Cnm=sum(nu.values())
    return dict(N=N, mean=mean, ratio=N/mean if mean>0 else float('inf'),
               E=E, E_over_mean2=E/(mean*mean) if mean>0 else 0, Cnm=Cnm, sym0=sym_fiber0)

print("E-b empirics: is nu(0)=N atypical vs mean=C(n,m)/p^w?  (N/mean ~ 1 => typical => E-b benign)")
print(f"{'p':>5} {'n':>3} {'m':>3} {'w':>2} | {'N=nu(0)':>9} {'mean':>10} {'N/mean':>8} "
      f"{'E/mean^2':>9} {'sym@0':>7} {'gamma':>6}")
from math import log
for (p,n,m,w) in [(97,16,6,3),(97,16,8,3),(193,16,6,3),(241,16,6,3),(97,16,6,2),(257,16,8,3)]:
    r=analyze(p,n,m,w)
    print(f"{p:>5} {n:>3} {m:>3} {w:>2} | {r['N']:>9} {r['mean']:>10.3f} {r['ratio']:>8.3f} "
          f"{r['E_over_mean2']:>9.3f} {r['sym0']:>7} {log(n)/log(p):>6.3f}")
print("\nsym@0 = # mu_2-symmetric S in the v=0 fiber (peeled by descent). N/mean~1 => nu(0) typical.")
