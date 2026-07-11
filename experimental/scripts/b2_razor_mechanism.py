import itertools, math
from collections import defaultdict, Counter
def mu_n(p,n):
    def order(x):
        o=1;v=x
        while v!=1:v=v*x%p;o+=1
        return o
    g=next(c for c in range(2,p) if order(c)==p-1)
    h=pow(g,(p-1)//n,p);S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    return S
def analyze_max_fiber(p,n,m):
    S=mu_n(p,n)
    buckets=defaultdict(list)
    for idx in itertools.combinations(range(n),m):
        key=(sum(S[i] for i in idx)%p, sum(S[i]*S[i] for i in idx)%p)
        buckets[key].append(frozenset(idx))
    F=max(buckets.values(),key=len); f=len(F)
    # energy decomposed by trade support size 2s (s = |S1\S2|)
    r=Counter()
    for a in F:
        for b in F:
            s=len(a-b)   # symmetric-difference half-size
            r[(a-b,b-a)]+=1
    by_support=defaultdict(lambda:[0,0])   # support -> [num distinct trades, energy contribution]
    for tau,cnt in r.items():
        supp=2*len(tau[0])
        by_support[supp][0]+=1
        by_support[supp][1]+=cnt*cnt
    E=sum(v[1] for v in by_support.values())
    print(f"n={n} p={p} m={m}: max fiber f={f}, E={E}, E/f^2={E/f**2:.3f}")
    print(f"  {'supp':>5} {'#trades':>8} {'energy':>10} {'frac of E':>10} {'frac of excess':>14}")
    excess=E-by_support[0][1]   # subtract diagonal (support 0, r(0)=f, energy f^2)
    for supp in sorted(by_support):
        nt,en=by_support[supp]
        fx=(en/excess) if (supp>0 and excess>0) else float('nan')
        print(f"  {supp:>5} {nt:>8} {en:>10} {en/E:>10.4f} {fx:>14.4f}")
    print(f"  => support-0 (diagonal) energy = f^2 = {by_support[0][1]}; EXCESS (support>0) = {excess}")
    print(f"     is excess dominated by support-6 (3-for-3 = T_3 trades)? support-6 frac of excess = {by_support[6][1]/excess:.4f}\n")
analyze_max_fiber(41,20,8)
analyze_max_fiber(73,24,10)
