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
def fiber_energy(F):
    # F = list of frozensets (m-subsets). E(F)=#{(S1,S2,S3,S4): 1_S1-1_S2 = 1_S3-1_S4}
    # trade (S1,S2) -> (S1\S2 as frozenset, S2\S1). r(tau)^2 summed.
    r=Counter()
    for S1 in F:
        for S2 in F:
            tau=(S1-S2, S2-S1)
            r[tau]+=1
    return sum(v*v for v in r.values())
def probe(p,n,m,topK=6):
    S=mu_n(p,n)
    buckets=defaultdict(list)
    for idx in itertools.combinations(range(n),m):
        p1=sum(S[i] for i in idx)%p
        p2=sum(S[i]*S[i] for i in idx)%p
        buckets[(p1,p2)].append(frozenset(idx))
    sizes=sorted((len(v) for v in buckets.values()),reverse=True)
    mean=math.comb(n,m)/p**2
    print(f"p={p} n={n} m={m} (dens {m/n:.2f}): #fibers={len(buckets)}, mean fiber={mean:.2f}, max fiber={sizes[0]}")
    # take the largest fibers, compute energy exponent
    big=sorted(buckets.values(),key=len,reverse=True)[:topK]
    print(f"  {'f':>5} {'E':>8} {'Delta=E/f^3':>11} {'sidon 2/f':>10} {'E/f^2':>7} {'logE/logf':>9} {'above_sidon':>11}")
    for F in big:
        f=len(F)
        if f<2: continue
        E=fiber_energy(F)
        Delta=E/f**3; sidon=(2*f-1)/f**2; Ef2=E/f**2
        exp_=math.log(E)/math.log(f) if f>1 else 0
        print(f"  {f:>5} {E:>8} {Delta:>11.4f} {sidon:>10.4f} {Ef2:>7.3f} {exp_:>9.4f} {str(E>2*f*f-f):>11}")
    print()
probe(17,16,6)
probe(41,20,8)
probe(73,24,10)
