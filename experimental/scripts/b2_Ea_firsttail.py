import numpy as np
from itertools import combinations
from math import comb, log

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
    return pts  # pts[k]=z^k

def Ed(p,n,w,d,pts):
    """#{ordered disjoint (A,B), |A|=|B|=d in mu_n, p_j(A)=p_j(B) all j<=w}."""
    # power tables: powtab[j][k] = pts[k]^j mod p = pts[(j*k)%n]
    idx=range(n)
    # signature of a subset = tuple(sum_{k in A} pts[(j*k)%n] mod p for j=1..w)
    from collections import defaultdict
    buckets=defaultdict(list)  # sig -> list of bitmask
    for A in combinations(idx,d):
        sig=tuple(sum(pts[(j*k)%n] for k in A)%p for j in range(1,w+1))
        mask=0
        for k in A: mask|=(1<<k)
        buckets[sig].append(mask)
    total=0
    for sig,masks in buckets.items():
        if len(masks)<2: continue
        L=len(masks)
        for i in range(L):
            mi=masks[i]
            for j2 in range(L):
                if i==j2: continue
                if mi & masks[j2]==0:  # disjoint
                    total+=1
    return total

print(f"{'p':>5} {'n':>4} {'gamma':>6} {'w':>3} {'d':>3} | {'E_d(exact)':>12} {'random pred':>12} {'ratio':>7} {'note'}")
print("-"*80)
for (p,n,w) in [(97,16,3),(97,16,4),(257,16,3),(193,16,4),(97,16,2)]:
    pts=subgroup(p,n)
    gamma=log(n)/log(p)
    for d in range(w, min(w+3,n//2)+1):
        pred=comb(n,d)*comb(n-d,d)/p**w   # random model (ordered disjoint / p^w)
        e=Ed(p,n,w,d,pts)
        ratio = e/pred if pred>0 else float('inf')
        tag = "RIGID (=0, proved d<=w)" if d<=w and e==0 else ("first tail" if d==w+1 else "")
        print(f"{p:>5} {n:>4} {gamma:>6.3f} {w:>3} {d:>3} | {e:>12} {pred:>12.2f} {ratio:>7.3f} {tag}")
    print()
