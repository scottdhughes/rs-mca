import numpy as np
from math import comb, log

def prim_root(p):
    phi=p-1; mm=phi; f=[]; d=2
    while d*d<=mm:
        if mm%d==0:
            f.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: f.append(mm)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g
def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    return [pow(z,k,p) for k in range(n)]

def secant_variance(n,p,m):
    G=subgroup(p,n); G2=[pow(h,2,p) for h in G]; G3=[pow(h,3,p) for h in G]
    D=[np.zeros((p,p,p),dtype=np.float64) for _ in range(m+1)]
    D[0][0,0,0]=1.0
    for h,h2,h3 in zip(G,G2,G3):
        for k in range(m,0,-1):
            D[k]+=np.roll(np.roll(np.roll(D[k-1],h,0),h2,1),h3,2)
    nu=D[m]; mu=comb(n,m)/p**3
    sv=[]
    for i in range(n):
        for j in range(n):
            if i!=j: sv.append(nu[(G[j]-G[i])%p,(G2[j]-G2[i])%p,(G3[j]-G3[i])%p])
    sv=np.array(sv)
    var=((sv-mu).clip(min=0)**2).sum()
    return dict(mu=mu, theta=log(mu)/log(n) if mu>0 else float('-inf'),
                var=var, n2mu2=n*n*mu*mu, inv=var/(n*n*mu*mu) if mu>0 else float('inf'),
                maxr=sv.max()/mu, budget=(m*(n-m)/(n*(n-1))/2)**2*n**8)

# controlled set spanning mu (small -> large); w=3, rho=0.5. Sorted by theta.
cases=[(16,97,8),(16,193,8),(16,17,8),(24,193,12),(24,97,12),(24,73,12),(32,193,16),(32,97,16)]
rows=[]
for (n,p,m) in cases:
    if (p-1)%n: continue
    rows.append((n,p,m,secant_variance(n,p,m)))
rows.sort(key=lambda r:r[3]['theta'])
print("SV* theta-INVARIANT test: variance/(n^2 mu^2).  Bounded (esp. large theta) => SV* holds at deployment.")
print("  (SV* holds if var <= budget=(a/2)^2 n^8;  var ~ n^2 mu^2 * [inv].  n^2mu^2=n^{2+2theta} < n^8 iff theta<3.)")
print(f"{'n':>3} {'p':>4} {'theta':>7} {'mu':>10} {'max nu/mu':>9} {'variance':>11} {'var/(n^2mu^2)':>14} {'var/budget':>11}")
print("-"*88)
for (n,p,m,r) in rows:
    print(f"{n:>3} {p:>4} {r['theta']:>7.3f} {r['mu']:>10.3f} {r['maxr']:>9.2f} {r['var']:>11.3e} {r['inv']:>14.3f} {r['var']/r['budget']:>11.2e}")
print("\nREAD: as theta grows toward deployment (1.7), does var/(n^2mu^2) stay bounded / shrink?")
print("deployment proxy = largest-theta row (n=32,p=97,theta~1.87).")
