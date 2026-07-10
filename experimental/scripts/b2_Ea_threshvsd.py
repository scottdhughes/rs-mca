from itertools import combinations
from collections import defaultdict

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

def Ed(p,n,w,d,pts):
    buckets=defaultdict(list)
    for A in combinations(range(n),d):
        sig=tuple(sum(pts[(j*k)%n] for k in A)%p for j in range(1,w+1))
        mask=0
        for k in A: mask|=(1<<k)
        buckets[sig].append(mask)
    total=0
    for masks in buckets.values():
        L=len(masks)
        if L<2: continue
        for i in range(L):
            mi=masks[i]
            for jj in range(L):
                if i!=jj and (mi & masks[jj])==0: total+=1
    return total

def primes_1mod(nmod, count):
    def isp(m):
        if m<2: return False
        i=2
        while i*i<=m:
            if m%i==0: return False
            i+=1
        return True
    res=[]; x=nmod+1
    while len(res)<count:
        if x%nmod==1 and isp(x): res.append(x)
        x+=1
    return res

for (n,w,dmax) in [(24,3,7),(32,3,5)]:
    print(f"\n### n={n}, w={w}: threshold-vs-d (E_d(p) across p=1 mod {n}) ###")
    ps=primes_1mod(n, 7)
    print(f"   primes: {ps}")
    for d in range(w+1, dmax+1):
        row=[]
        for p in ps:
            pts=subgroup(p,n)
            row.append(Ed(p,n,w,d,pts))
        baseline=row[-1]  # largest p = char-0 baseline
        # threshold = first p (ascending) matching baseline and staying there
        thr=None
        for i in range(len(ps)):
            if all(row[k]==baseline for k in range(i,len(ps))):
                thr=ps[i]; break
        print(f"   d={d}: E_d(p)={row}  -> char0 baseline={baseline}, stabilizes at p>={thr}")
