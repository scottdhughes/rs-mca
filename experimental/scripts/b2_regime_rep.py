import numpy as np, math
from math import comb
def mu_n(p,n):
    def order(x):
        o=1;v=x
        while v!=1:v=v*x%p;o+=1
        return o
    g=next(c for c in range(2,p) if order(c)==p-1)
    h=pow(g,(p-1)//n,p);S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    return np.array(S,dtype=np.int64)
def excess_over_main(p,n,w,d):
    # w=2 only, numpy-vectorized over all c=(c1,c2)
    S=mu_n(p,n); a=S%p; a2=(S*S)%p
    c1=np.arange(p); c2=np.arange(p)
    # exponent[c1,c2,a] = (c1*a + c2*a2) mod p ; build phases and e_d via recurrence over a
    # loop over c1 (p iters), vectorize c2 and a
    main=comb(n,d)**2
    tot=0.0
    tp=2j*math.pi/p
    for cc1 in range(p):
        # phase[c2, a] = exp(tp*((cc1*a + c2*a2) mod p))
        expo=(cc1*a[None,:] + np.outer(c2,a2))%p      # (p, n)
        ph=np.exp(tp*expo)                             # (p, n) complex
        # e_d over axis=1 (the n values) via Newton/elementary recurrence
        e=np.zeros((p,d+1),dtype=complex); e[:,0]=1.0
        for j in range(n):
            x=ph[:,j]
            for k in range(d,0,-1):
                e[:,k]=e[:,k]+x*e[:,k-1]
        tot+=np.sum(np.abs(e[:,d])**2)
    return tot/main - 1.0, comb(n,d)/p**w

n=32; w=2
print("REGIME-REP TEST: above collision threshold (C(n,d)>>p^w) AND below equidist (r<1)")
print(f"n={n}, w={w}, d=round(0.33n)=11.   deployment analog: C(n,d)>>p^w, r<1")
print(f"{'p':>5} {'r=n/(w√p)':>10} {'C(n,d)/p^w':>12} {'excess/main':>13}")
d=11
for p in [257,353,449,577,641,769]:
    if (p-1)%n!=0: 
        print(f"{p} skip (n not | p-1)"); continue
    r=n/(w*math.sqrt(p))
    em,ratio=excess_over_main(p,n,w,d)
    print(f"{p:>5} {r:>10.3f} {comb(n,d)/p**w:>12.1f} {em:>13.4e}")
