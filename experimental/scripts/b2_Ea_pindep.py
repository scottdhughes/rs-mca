from itertools import combinations
from collections import defaultdict
from math import comb

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
            for j2 in range(L):
                if i!=j2 and (mi & masks[j2])==0: total+=1
    return total

# primes = 1 mod 16
def primes_1mod(nmod, count, start=17):
    res=[]; x=start
    def isp(m):
        if m<2: return False
        i=2
        while i*i<=m:
            if m%i==0: return False
            i+=1
        return True
    while len(res)<count:
        if x%nmod==1 and isp(x): res.append(x)
        x+=1
    return res

n=16
for w in [2,3]:
    d=w+1
    print(f"\n=== n={n}, w={w}, first tail d={d}:  E_{d}(p) across p=1 mod {n} ===")
    print(f"{'p':>6} {'gamma':>6} {'E_(w+1)':>9}")
    ps=primes_1mod(n, 12, start=17)
    vals=[]
    from math import log
    for p in ps:
        pts=subgroup(p,n)
        e=Ed(p,n,w,d,pts)
        vals.append(e)
        print(f"{p:>6} {log(n)/log(p):>6.3f} {e:>9}")
    # stabilized value = mode of the large-p tail
    tail=vals[-6:]
    stab=min(tail)
    print(f"  --> large-p stabilized (char-0 PTE baseline): E_{d} = {stab}")
    print(f"      small-p excess visible where E_{d}(p) > {stab} (mod-p collisions)")
