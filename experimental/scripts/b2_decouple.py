import numpy as np, math
from math import comb
from sympy import nextprime
rng=np.random.default_rng(7)
def elt_order_n(p,n):
    for x in range(2,p):
        h=pow(x,(p-1)//n,p)
        if pow(h,n//2,p)!=1: return h
def mu_n(p,n):
    h=elt_order_n(p,n); S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    assert len(S)==n
    return np.array(S,dtype=np.int64)
def est(p,n,w,d,K):
    S=mu_n(p,n); a=S%p; a2=(S*S)%p
    C=rng.integers(0,p,size=(K,2)); C=C[~((C[:,0]==0)&(C[:,1]==0))]; K=len(C)
    tp=2j*math.pi/p
    expo=(C[:,0:1]*a[None,:]+C[:,1:2]*a2[None,:])%p
    ph=np.exp(tp*expo)
    e=np.zeros((K,d+1),dtype=complex); e[:,0]=1.0
    for j in range(n):
        x=ph[:,j]
        for k in range(d,0,-1): e[:,k]=e[:,k]+x*e[:,k-1]
    return np.mean(np.abs(e[:,d])**2)*(p*p-1)/comb(n,d)**2

w=2; TARGET_ratio=100.0   # hold C(n,d)/p^w ~ 100 (fixed, safely above collision), drive r->0 via n
print(f"DECOUPLED test: FIX C(n,d)/p^w ~ {TARGET_ratio:.0f} (above collision), vary n -> r drops.")
print("If excess/main flat as r->0  => controlled by C/p^w, NOT r  => deployment (huge C/p^w) => target SAFE")
print(f"{'n':>4} {'d':>3} {'p':>10} {'r=n/(w√p)':>10} {'C/p^w':>8} {'excess/main':>13}")
for n in [32,40,48,56,64]:
    d=round(0.33*n)
    Cnd=comb(n,d)
    p0=int((Cnd/TARGET_ratio)**0.5)     # p^2 = C/TARGET
    p=nextprime(p0)
    while (p-1)%n!=0: p=nextprime(p)
    r=n/(w*math.sqrt(p)); ratio=Cnd/p**w
    K=90000
    em=est(p,n,w,d,K)
    print(f"{n:>4} {d:>3} {p:>10} {r:>10.4f} {ratio:>8.1f} {em:>13.4e}")
