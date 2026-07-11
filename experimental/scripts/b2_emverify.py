import numpy as np, math, cmath, itertools
from math import comb
def mu_n(p,n):
    def order(x):
        o=1;v=x
        while v!=1:v=v*x%p;o+=1
        return o
    g=next(c for c in range(2,p) if order(c)==p-1)
    h=pow(g,(p-1)//n,p);S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    return S
def esym(vals,d):
    e=np.zeros(d+1,dtype=complex); e[0]=1
    for x in vals:
        for k in range(d,0,-1): e[k]+=x*e[k-1]
    return e[d]
def analyze(p,n,m):
    S=mu_n(p,n); tp=2*math.pi/p
    maxem=0.0; argmax=None; maxtau=0.0
    for c1 in range(p):
        for c2 in range(p):
            if c1==0 and c2==0: continue
            phases=[cmath.exp(tp*1j*((c1*a+c2*a*a)%p)) for a in S]
            em=abs(esym(phases,m))
            tau=abs(sum(phases))
            if em>maxem: maxem=em; argmax=(c1,c2)
            if tau>maxtau: maxtau=tau
    Cnm=comb(n,m); mean=Cnm/p**2
    print(f"n={n} p={p} m={m}: C(n,m)={Cnm}, mean=C/p^2={mean:.2f}, 2sqrt(p)={2*math.sqrt(p):.2f}")
    print(f"   max_xi!=0 |tau_2(xi)| = {maxtau:.2f}  (<= 2sqrt(p)={2*math.sqrt(p):.2f}? {maxtau<=2*math.sqrt(p)+.01})")
    print(f"   max_xi!=0 |e_m(xi)|   = {maxem:.3g}  at {argmax}")
    print(f"      vs C(n,m)={Cnm:.3g} : ratio |e_m|/C = {maxem/Cnm:.4g}  (<<1 needed)")
    print(f"      vs mean={mean:.3g}  : |e_m|/mean = {maxem/mean:.4g}  (bound max<=mean(1+this); flat iff <<1... small n won't be)")
    print(f"      vs e^{{2sqrt(p)}}={math.exp(2*math.sqrt(p)):.3g} : |e_m|/e^{{2sqrt p}} = {maxem/math.exp(2*math.sqrt(p)):.4g}  (<=~1 confirms Newton bound)")
    print(f"      => the Newton/Weil bound predicts |e_m| <= e^{{O(sqrt p)}}; check it CAPS |e_m| (not ~C(n,m))")
analyze(17,16,8)
analyze(41,20,10)
analyze(73,24,12)
analyze(89,22,11)
