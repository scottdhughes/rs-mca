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
def max_fiber_energy(p,n,m):
    S=mu_n(p,n)
    buckets=defaultdict(list)
    for idx in itertools.combinations(range(n),m):
        key=(sum(S[i] for i in idx)%p, sum(S[i]*S[i] for i in idx)%p)
        buckets[key].append(idx)
    F=max(buckets.values(),key=len)
    Fs=[frozenset(x) for x in F]; f=len(Fs)
    r=Counter()
    for a in Fs:
        for b in Fs: r[(a-b,b-a)]+=1
    E=sum(v*v for v in r.values())
    return f,E
pts=[]
for (p,n,m) in [(17,16,6),(41,20,8),(73,24,10),(53,26,11)]:
    f,E=max_fiber_energy(p,n,m); C=E/f**2
    pts.append((n,f,E,C)); print(f"n={n} f={f} E={E} C=E/f^2={C:.4f} logE/logf={math.log(E)/math.log(f):.4f}")
# power-law fit C ~ a*f^eps  (log C = log a + eps log f)
import statistics
xs=[math.log(p[1]) for p in pts]; ys=[math.log(p[3]) for p in pts]
mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
eps=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
a=math.exp(my-eps*mx)
ss_res=sum((y-(math.log(a)+eps*x))**2 for x,y in zip(xs,ys)); ss_tot=sum((y-my)**2 for y in ys)
r2=1-ss_res/ss_tot if ss_tot>0 else 1
print(f"\nPOWER-LAW FIT: C = {a:.3f} * f^{eps:.4f}   (R^2={r2:.4f})")
print(f"  => Delta = C/f = {a:.3f} * f^-{1-eps:.4f}  => razor form (a) holds with c = {1-eps:.4f} (<1 iff eps>0)")
print(f"  eps={eps:.4f} {'>0: RAZOR SUPPORTED (fixed c<1)' if eps>0.01 else '~0: razor form (a) marginal/fails'}")
