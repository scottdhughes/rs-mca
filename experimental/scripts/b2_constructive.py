import itertools, math
from collections import defaultdict
def mu_n(p,n):
    def order(x):
        o=1;v=x
        while v!=1:v=v*x%p;o+=1
        return o
    g=next(c for c in range(2,p) if order(c)==p-1)
    h=pow(g,(p-1)//n,p);S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    return S
def analyze(p,n,m):
    S=mu_n(p,n); buckets=defaultdict(list)
    for idx in itertools.combinations(range(n),m):
        key=(sum(S[i] for i in idx)%p, sum(S[i]*S[i] for i in idx)%p)
        buckets[key].append(frozenset(idx))
    F=max(buckets.values(),key=len); f=len(F); Fset=set(F)
    # total excess quadruples = (E - 2f^2 + f)/2  (unordered nontrivial). Compute E.
    from collections import Counter
    r=Counter()
    for a in F:
        for b in F: r[(a-b,b-a)]+=1
    E=sum(v*v for v in r.values())
    # disjoint-trade quadruples: for each S, count pairs (S',S'') with (S^S') disjoint (S^S'') and S'+S''-S in F.
    # (S'+S''-S in F is automatic when disjoint; verify.) count how many the CONSTRUCTION produces.
    disj=0; typ_diff=[]
    Flist=list(F)
    for S in Flist:
        diffs=[(Sp, S.symmetric_difference(Sp)) for Sp in Flist if Sp!=S]
        for Sp in Flist:
            if Sp!=S: typ_diff.append(len(S.symmetric_difference(Sp)))
        for i in range(len(diffs)):
            for j in range(i+1,len(diffs)):
                if diffs[i][1].isdisjoint(diffs[j][1]):
                    disj+=1
    # each unordered quadruple counted ~ some times; report raw construction yield vs total excess
    excess=(E-(2*f*f-f))//2
    avg_diff=sum(typ_diff)/len(typ_diff)
    print(f"n={n} p={p} m={m}: f={f}, avg |S^S'| (trade size)={avg_diff:.1f} (= {avg_diff/2:.1f}-for-{avg_diff/2:.1f} swap), n={n}")
    print(f"   total EXCESS quadruples (E-2f^2+f)/2 = {excess}")
    print(f"   disjoint-trade construction yield    = {disj}   (fraction of excess: {disj/excess if excess else 0:.4f})")
    print(f"   => construction {'WORKS (captures excess)' if excess and disj/excess>0.5 else 'FAILS (trades too large to be disjoint)'}: avg trade {avg_diff:.0f} vs n {n} => disjoint prob ~ (1-{avg_diff:.0f}^2/{n})\n")
analyze(41,20,8)
analyze(73,24,10)
