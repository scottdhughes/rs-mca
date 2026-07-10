import numpy as np
from math import comb, log

def isprime(m):
    i=2
    while i*i<=m:
        if m%i==0: return False
        i+=1
    return m>=2
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
def pick_p(n,g=0.68):
    lo=int(n**(1/g)); best=None
    for p in range(max(lo,n+2), lo*3):
        if p%n==1 and isprime(p):
            if best is None or abs(log(n)/log(p)-g)<abs(log(n)/log(best)-g): best=p
            if log(n)/log(p)<=g: break
    return best

def secvar(n,p,m):
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
    onesided=((sv-mu).clip(min=0)**2).sum()
    alpha=m*(n-m)/(n*(n-1))
    return dict(mu=mu,onesided=onesided,budget=(alpha/2)**2*n**8,maxr=sv.max()/mu,gamma=log(n)/log(p))

print("SV* SCALING: one-sided full-secant variance vs n (fixed gamma~0.68, rho=0.5, w=3).")
print(f"{'n':>3} {'p':>5} {'gamma':>6} {'mu':>9} {'onesided_var':>13} {'(a/2)^2 n^8':>12} {'var/budget':>11} {'max nu/mu':>10}")
res=[]
for n in [12,16,24,32]:
    p=pick_p(n); m=n//2
    r=secvar(n,p,m)
    res.append((n,r['onesided']))
    print(f"{n:>3} {p:>5} {r['gamma']:>6.3f} {r['mu']:>9.3f} {r['onesided']:>13.3e} {r['budget']:>12.2e} {r['onesided']/r['budget']:>11.2e} {r['maxr']:>10.2f}")
# fit exponent: log(var) ~ e * log(n)
ns=np.array([x[0] for x in res],float); vs=np.array([x[1] for x in res],float)
e=np.polyfit(np.log(ns),np.log(vs),1)[0]
print(f"\nfitted scaling: one-sided var ~ n^{e:.2f}   (SV* needs <= n^8; var/budget should stay bounded/shrink)")
print("=> if exponent < 8 and var/budget shrinks, SV* is the right target and scales to deployment.")
