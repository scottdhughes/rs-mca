import itertools
from math import comb
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
def check(p,n,m):
    S=mu_n(p,n)
    # all fibers, exact energies
    buckets=defaultdict(list)
    for idx in itertools.combinations(range(n),m):
        key=(sum(S[i] for i in idx)%p, sum(S[i]*S[i] for i in idx)%p)
        buckets[key].append(frozenset(idx))
    # T = sum_v E(F_v)  (brute, exact)
    T=0
    for v,F in buckets.items():
        r=Counter()
        for a in F:
            for b in F: r[(a-b,b-a)]+=1
        T+=sum(x*x for x in r.values())
    # V(s) = #{ordered (A,B) disjoint, |A|=|B|=s, p1(A)=p1(B),p2(A)=p2(B)}
    def V(s):
        cnt=0; subs=list(itertools.combinations(range(n),s))
        syn=defaultdict(list)
        for A in subs:
            syn[(sum(S[i] for i in A)%p, sum(S[i]**2 for i in A)%p)].append(set(A))
        for key,lst in syn.items():
            for A in lst:
                for B in lst:
                    if A.isdisjoint(B): cnt+=1
        return cnt
    smax=m
    my_formula=sum(V(s)*comb(n-2*s,m-s)**2 for s in range(3,smax+1) if n-2*s>=0)
    # correct: T = sum_tau sum_v r_v(tau)^2 -- recompute directly to confirm brute T
    print(f"p={p} n={n} m={m}:")
    print(f"  T = sum_v E(F_v) [brute exact]      = {T}")
    print(f"  my claimed Sum_s V(s) C(n-2s,m-s)^2 = {my_formula}   MATCH={T==my_formula}")
    for s in range(3,min(smax,6)+1):
        if n-2*s>=0: print(f"    V({s})={V(s)}  C(n-2s,m-s)={comb(n-2*s,m-s)}  term={V(s)*comb(n-2*s,m-s)**2}")
    # also: second moment Sum_v f_v^2 and its trade formula Sum_s V(s) C(n-2s,m-s)
    sec=sum(len(F)**2 for F in buckets.values())
    sec_formula=comb(n,m)+sum(V(s)*comb(n-2*s,m-s) for s in range(3,smax+1) if n-2*s>=0)
    print(f"  2nd moment Sum_v f_v^2 = {sec};  diag C(n,m)+Sum_s V(s)C(n-2s,m-s) = {sec_formula}  MATCH={sec==sec_formula}")
check(17,16,6)
check(13,12,5)
