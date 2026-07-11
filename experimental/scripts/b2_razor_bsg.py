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
def fiber_stats(p,n,m):
    S=mu_n(p,n)
    buckets=defaultdict(list)
    for idx in itertools.combinations(range(n),m):
        key=(sum(S[i] for i in idx)%p, sum(S[i]*S[i] for i in idx)%p)
        buckets[key].append(frozenset(idx))
    F=max(buckets.values(),key=len); f=len(F)
    # difference set |F-F| = # distinct trades (ordered), and energy E
    diffs=set(); r=Counter()
    for a in F:
        for b in F:
            tau=(a-b,b-a); diffs.add(tau); r[tau]+=1
    FmF=len(diffs); E=sum(v*v for v in r.values())
    # sumset |F+F|: distinct multiset sums 1_a+1_b (as sorted tuple of (elt,count))
    sums=set()
    for i,a in enumerate(F):
        for b in list(F)[i:]:
            c=Counter(a)+Counter(b); sums.add(frozenset(c.items()))
    FpF=len(sums)
    return f,E,FmF,FpF
print("Difference-set / doubling exponents for the max mu_n fiber (razor <=> theta<2):")
print(f"{'n':>3} {'f':>6} {'|F-F|':>8} {'theta=log|F-F|/logf':>20} {'|F+F|':>8} {'sigma=log|F+F|/logf':>20} {'E':>10} {'CS: f/|F-F|':>12} {'actual Delta':>12}")
pts=[]
for (p,n,m) in [(17,16,6),(41,20,8),(73,24,10),(53,26,11)]:
    f,E,FmF,FpF=fiber_stats(p,n,m)
    th=math.log(FmF)/math.log(f); sg=math.log(FpF)/math.log(f)
    cs=f/FmF; Delta=E/f**3
    pts.append((n,f,FmF,th))
    print(f"{n:>3} {f:>6} {FmF:>8} {th:>20.4f} {FpF:>8} {sg:>20.4f} {E:>10} {cs:>12.5f} {Delta:>12.5f}")
# fit theta trend
xs=[math.log(p[1]) for p in pts]; ys=[math.log(p[2]) for p in pts]
mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
print(f"\nfit |F-F| ~ f^{slope:.4f}  => difference-set exponent theta ~ {slope:.4f}")
print(f"  razor form (a) via CS needs theta <= 1+c < 2; measured theta={slope:.3f} => {'SUBQUADRATIC (CS route viable, c='+format(slope-1,'.3f')+')' if slope<2 else 'quadratic/Sidon (CS route fails)'}")
