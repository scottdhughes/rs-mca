import numpy as np
from math import comb, log, sqrt

def isprime(m):
    if m<2: return False
    i=2
    while i*i<=m:
        if m%i==0: return False
        i+=1
    return True
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
    pts=[]; cur=1
    for _ in range(n): pts.append(cur); cur=cur*z%p
    return pts
def pick_p(n, target_gamma=0.68):
    lo=int(n**(1/target_gamma))
    best=None
    for p in range(max(lo-1,n+1), lo*3):
        if p%n==1 and isprime(p):
            g=log(n)/log(p)
            if best is None or abs(g-target_gamma)<abs(log(n)/log(best)-target_gamma):
                best=p
            if g<=target_gamma: break
    return best

def analyze(n,p,m):
    H=subgroup(p,n); H2=[(h*h)%p for h in H]
    D=[np.zeros((p,p),dtype=np.float64) for _ in range(m+1)]
    D[0][0,0]=1.0
    for h,h2 in zip(H,H2):
        for k in range(m,0,-1):
            D[k]+=np.roll(np.roll(D[k-1],h,axis=0),h2,axis=1)
    nu=D[m]
    M=comb(n,m); Q=p*p; mu=M/Q
    N=nu[0,0]
    Delta2=float(((nu-mu)**2).sum())
    # secant set D_1
    idx=[]
    for i in range(n):
        for j in range(n):
            if i!=j: idx.append(((H[j]-H[i])%p,(H2[j]-H2[i])%p))
    us=np.array([a for a,_ in idx]); vs=np.array([b for _,b in idx])
    nuD=nu[us,vs]
    Dsec=float(((nuD-mu)**2).sum())
    R=n*(n-1)/(m*(n-m))
    secant=R*(mu+sqrt(Dsec/(n*(n-1))))
    naive=mu+sqrt((Q-1)/Q*Delta2)
    theta=log(mu)/log(n) if mu>1 else float('nan')
    return dict(N=N,mu=mu,theta=theta, Dsec_ratio=Dsec/(n*n*mu),
                D2_ratio=Delta2/(n*n*mu), Nmu=N/mu, secant=secant, naive=naive, R=R)

print("Secant-local-variance across the finite window (w=2, gamma~0.68).")
print("KEY metric: Delta_sec/(n^2 mu) -- O(1) => Poisson-scale => secant route proves N=O(mu).\n")
print(f"{'n':>4} {'p':>5} {'gamma':>6} {'m':>4} {'rho':>4} {'theta':>6} | "
      f"{'N/mu':>6} {'Dsec/n^2mu':>10} {'D2/n^2mu':>9} | {'secantB/mu':>10} {'naiveB/mu':>9}")
print("-"*95)
for n in [32,64,128]:
    p=pick_p(n)
    for rho in [0.3,0.5]:
        m=max(3,round(rho*n))
        r=analyze(n,p,m)
        print(f"{n:>4} {p:>5} {log(n)/log(p):>6.3f} {m:>4} {rho:>4.1f} {r['theta']:>6.2f} | "
              f"{r['Nmu']:>6.3f} {r['Dsec_ratio']:>10.3f} {r['D2_ratio']:>9.2e} | "
              f"{r['secant']/r['mu']:>10.2f} {r['naive']/r['mu']:>9.2f}")
print("\nDsec/n^2mu bounded across n => secant target Delta_sec=O(n^2 mu) is regime-robust (w=2).")
print("secantB/mu vs naiveB/mu: which transfer is tighter as n grows.")
