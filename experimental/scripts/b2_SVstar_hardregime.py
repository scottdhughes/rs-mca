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

# Full secant D_1 (w=3, all moments): d_{a,b}=(b-a, b^2-a^2, b^3-a^3). Test SV* in the small-mu regime
# that broke the antipodal route: does the FULL secant one-sided variance stay controlled?
for (n,p,m) in [(24,193,12),(24,97,12),(24,73,12)]:
    G=subgroup(p,n); G2=[pow(h,2,p) for h in G]; G3=[pow(h,3,p) for h in G]
    D=[np.zeros((p,p,p),dtype=np.float64) for _ in range(m+1)]
    D[0][0,0,0]=1.0
    for h,h2,h3 in zip(G,G2,G3):
        for k in range(m,0,-1):
            D[k]+=np.roll(np.roll(np.roll(D[k-1],h,0),h2,1),h3,2)
    nu=D[m]; mu=comb(n,m)/p**3; N=nu[0,0,0]
    secvals=[]
    for i in range(n):
        for j in range(n):
            if i==j: continue
            d=((G[j]-G[i])%p,(G2[j]-G2[i])%p,(G3[j]-G3[i])%p)
            secvals.append(nu[d])
    sv=np.array(secvals)
    # one-sided variance and the secant transfer bound on N
    onesided=((sv-mu).clip(min=0)**2).sum()
    firstmom=sv.sum()
    alpha=m*(n-m)/(n*(n-1))
    # secant bound: N <= (1/(m(n-m))) sum nu(d)  (raw, untrimmed)
    Nbound=firstmom/(m*(n-m))
    print(f"n={n} p={p} m={m} mu={mu:.3f} N={N:.0f} N/mu={N/mu:.1f} gamma={log(n)/log(p):.3f}")
    print(f"   full-secant: max nu(d)/mu={sv.max()/mu:.2f}  mean/mu={sv.mean()/mu:.3f}  #(>5mu)={(sv>5*mu).sum()} of {len(sv)}")
    print(f"   one-sided var sum(nu-mu)_+^2 = {onesided:.3e}   (SV*-scale ref (alpha/2)^2 n^8 = {(alpha/2)**2*n**8:.2e})")
    print(f"   raw secant bound N <= {Nbound:.1f}  [actual N={N:.0f}]  {'OK' if N<=Nbound+1 else 'FAIL'}  vs n^3={n**3}")
    print()
