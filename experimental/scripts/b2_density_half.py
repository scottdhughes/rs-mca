import itertools, math
from math import comb
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
def R_half(p,n):
    m=n//2; S=mu_n(p,n); buck=defaultdict(int)
    for idx in itertools.combinations(range(n),m):
        buck[(sum(S[i] for i in idx)%p, sum(S[i]*S[i] for i in idx)%p)]+=1
    fmax=max(buck.values()); mean=comb(n,m)/p**2
    return fmax, mean, comb(n,m)
print("Density-1/2 max-fiber inflation R(N,1/2) = f_max * p^2 / C(N,N/2)  (self-similar fixed point):")
print(f"{'N':>3} {'p':>4} {'m=N/2':>6} {'f_max':>7} {'mean':>10} {'R=f_max/mean':>13} {'C(N,N/2)/p^2':>13} {'logR/logN':>10}")
pts=[]
for (p,n) in [(17,8),(13,12),(17,16),(41,20),(73,24)]:
    if (p-1)%n: continue
    fmax,mean,Cnm=R_half(p,n)
    R=fmax/mean
    pts.append((n,R))
    print(f"{n:>3} {p:>4} {n//2:>6} {fmax:>7} {mean:>10.3f} {R:>13.3f} {Cnm/p**2:>13.1f} {math.log(R)/math.log(n):>10.4f}")
# is R bounded, polynomial in N, or exponential?
xs=[math.log(p[0]) for p in pts]; ys=[math.log(p[1]) for p in pts]
mx=sum(xs)/len(xs);my=sum(ys)/len(ys)
slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
print(f"\nfit R ~ N^{slope:.3f}  (poly in N if slope const & finite; the razor needs R=e^{{o(N)}} i.e. logR/N->0)")
print(f"  logR/N per point: " + ", ".join(f"{math.log(r)/n:.4f}" for n,r in pts) + "  (-> 0 supports razor)")
