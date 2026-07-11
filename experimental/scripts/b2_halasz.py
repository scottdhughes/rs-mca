import numpy as np, math, itertools
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
def analyze(p,n,w,m):
    S=mu_n(p,n); tp=2*math.pi/p; rho=m/n
    # S(xi)=sum_a e_p(xi.Phi(a)); n-Re S(xi); split primitive/resonant
    def curveRe(c):
        s=0j
        for a in S:
            e=0;ap=a
            for j in range(w): e=(e+c[j]*ap)%p; ap=ap*a%p
            s+=math.cos(tp*e)
        return s.real
    prim_min_nmReS=1e18; res_min=1e18; halasz_sum=0.0
    # exact signed shadow deviation: (1/p^w) sum_{xi!=0} prod_a(1-rho+rho e_p(xi.Phi(a)))
    signed_dev=0j
    for c in itertools.product(range(p),repeat=w):
        if all(x==0 for x in c): continue
        # product and Re S together
        prod=1+0j; ReS=0.0
        for a in S:
            e=0;ap=a
            for j in range(w): e=(e+c[j]*ap)%p; ap=ap*a%p
            ph=complex(math.cos(tp*e),math.sin(tp*e))
            prod*= (1-rho+rho*ph); ReS+=ph.real
        signed_dev+=prod
        nmReS=n-ReS
        halasz_sum+=math.exp(-rho*(1-rho)*nmReS)     # magnitude/union-bound term
        imprimitive=all(c[i]==0 for i in range(w) if (i+1)%2==1)
        if imprimitive: res_min=min(res_min,nmReS)
        else: prim_min_nmReS=min(prim_min_nmReS,nmReS)
    thresh=(w*math.log(p))/(rho*(1-rho))
    print(f"p={p} n={n} w={w} m={m} rho={rho:.3f}:")
    print(f"  Halasz threshold need n-ReS >= w*log(p)/(rho(1-rho)) = {thresh:.1f};  but max possible 2n={2*n}")
    print(f"    => union-bound feasible? {thresh <= 2*n}  (w*log p={w*math.log(p):.0f} vs rho(1-rho)2n={rho*(1-rho)*2*n:.0f})")
    print(f"  min(n-ReS) over PRIMITIVE xi = {prim_min_nmReS:.2f}   over RESONANT xi = {res_min:.2f}  (resonant small => blocks Halasz)")
    print(f"  MAGNITUDE (Halasz) sum_xi exp(...) = {halasz_sum:.3e}   vs  |SIGNED shadow dev| = {abs(signed_dev):.3e}")
    print(f"    ratio magnitude/signed = {halasz_sum/abs(signed_dev) if abs(signed_dev)>1e-9 else float('inf'):.2e}  (>>1 => sign-blindness is lossy)\n")
analyze(17,16,2,7)
analyze(97,16,2,7)
analyze(97,16,3,7)
