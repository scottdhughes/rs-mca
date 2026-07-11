import cmath, math, itertools
from math import comb

def mu_n(p, n):
    # multiplicative subgroup of order n in F_p^*  (requires n | p-1)
    assert (p-1) % n == 0
    # find a generator g of F_p^*
    def order(x):
        o=1; v=x
        while v!=1: v=v*x%p; o+=1
        return o
    g=None
    for cand in range(2,p):
        if order(cand)==p-1: g=cand; break
    h=pow(g,(p-1)//n,p)               # element of order n
    S=[1]; v=h
    while v!=1: S.append(v); v=v*h%p
    assert len(S)==n
    return S

def elem_sym_d(vals, d):
    # d-th elementary symmetric polynomial of the list vals (complex)
    e=[0j]*(d+1); e[0]=1+0j
    for x in vals:
        for k in range(d,0,-1):
            e[k]=e[k]+x*e[k-1]
    return e[d]

def analyze(p,n,w,d):
    S=mu_n(p,n)                        # the n-th roots of unity in F_p
    tp=2j*math.pi/p
    def chi(c,a):                      # exp(2pi i * (c1 a + c2 a^2 + ... + cw a^w)/p)
        s=0
        ap=a
        for j in range(w):
            s=(s+c[j]*ap)%p
            ap=ap*a%p
        return cmath.exp(tp*s)
    tot=0.0; prim=0.0; imprim=0.0; main=0.0
    # iterate all c in F_p^w
    for c in itertools.product(range(p),repeat=w):
        vals=[chi(c,a) for a in S]
        nu=elem_sym_d(vals,d)
        e2=abs(nu)**2
        tot+=e2
        if all(x==0 for x in c):
            main+=e2; continue
        # primitivity: c is imprimitive (factors through a->a^2) iff c_j=0 for all ODD j (1-indexed exponent j)
        # exponent of coordinate index i (0-based) is (i+1)
        imprimitive = all(c[i]==0 for i in range(w) if (i+1)%2==1)
        if imprimitive: imprim+=e2
        else: prim+=e2
    excess=tot-main
    rand=comb(n,d)**2/p**w             # heuristic "random" energy per... (mean of |nu|^2 summed ~ C(n,d) per freq)
    print(f"  p={p} n={n} w={w} d={d}:  C(n,d)={comb(n,d)}")
    print(f"     main(c=0)={main:.1f} [=C(n,d)^2={comb(n,d)**2}]   excess(c!=0)={excess:.2f}")
    print(f"       -> primitive c: {prim:.3f}    imprimitive c (thru a^2): {imprim:.3f}")
    print(f"       excess/main = {excess/main:.3e};  imprim/excess = {imprim/excess if excess>1e-9 else float('nan'):.4f}")
    # predicted 'random' per-frequency |nu|^2 ~ C(n,d); # primitive freqs ~ p^w
    print(f"       primitive avg |nu|^2 per freq = {prim/max(1,(p**w - (p**(w//1)) )):.4g} (compare C(n,d)={comb(n,d)}, random~C(n,d))")
    return prim,imprim,excess,main

print("=== EQUIDISTRIBUTION SPLIT TEST: does energy excess live on imprimitive (resonant) frequencies? ===")
analyze(17,8,2,3)
analyze(17,8,2,4)
analyze(17,16,2,5)
analyze(97,16,2,5)
analyze(97,16,3,5)
