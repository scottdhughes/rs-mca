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
    F=max(buckets.values(),key=len); f=len(F)
    # N_sub(x1,x3) = #{S in F : x1∩x3 ⊆ S ⊆ x1∪x3}; group by d=|x1△x3|
    by_d=defaultdict(lambda:[0,0,0])   # d -> [num pairs, sum N_sub, sum (N_sub-2)]
    Fl=list(F)
    for x1 in Fl:
        for x3 in Fl:
            inter=x1&x3; union=x1|x3; d=len(x1^x3)
            Nsub=sum(1 for Ssub in Fl if inter<=Ssub<=union)
            by_d[d][0]+=1; by_d[d][1]+=Nsub; by_d[d][2]+=(Nsub-2 if d>0 else 0)
    E=sum(v[1] for v in by_d.values())
    print(f"n={n} p={p} m={m}: f={f}, E={E}, E/f^2={E/f**2:.3f}, excess/f^2={(E-(2*f*f-f))/f**2:.4f}")
    print(f"  {'d':>4} {'#pairs':>8} {'avg N_sub':>10} {'random C(d,d/2)/p^2':>20} {'inflation I(d)':>14} {'avg(Nsub-2)':>11}")
    for d in sorted(by_d):
        np_,sN,sX=by_d[d]
        avgN=sN/np_; rand=math.comb(d,d//2)/p**2 if d>0 else 1
        infl=avgN/rand if rand>0 else float('inf')
        print(f"  {d:>4} {np_:>8} {avgN:>10.3f} {rand:>20.4g} {infl:>14.3f} {sX/np_:>11.4f}")
    print()
analyze(41,20,8)
analyze(73,24,10)
