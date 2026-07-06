#!/usr/bin/env python3
"""
b2 toy SWEEP: locate the balance point where non-coset-union t-null "extras"
appear, and check they stay <= cushion n^3.

t-null block B subset mu_n (n=2^s):  sum_{x in B} x^r = 0 (F_q) for r=1..t.
structured (b1): unions of mu_{M0}-cosets, M0 = least power of 2 > t.
extra = mod-p t-null block that is NOT structured (the Frobenius-gap objects b2 counts).
"""
from itertools import combinations, chain
from collections import Counter
from math import comb, log2

def smallest_prime_1_mod(n, start=None):
    def isprime(m):
        if m<2: return False
        i=2
        while i*i<=m:
            if m%i==0: return False
            i+=1
        return True
    m = (start or 1)
    # find smallest prime = 1 mod n that is > n
    c = n+1
    while True:
        if c>1 and c%n==1 and isprime(c) and c>n:
            return c
        c += 1

def primitive_root(q):
    # q prime; find generator of F_q^*
    order=q-1
    # factor order
    f=set(); m=order; d=2
    while d*d<=m:
        while m%d==0: f.add(d); m//=d
        d+=1
    if m>1: f.add(m)
    for g in range(2,q):
        if all(pow(g,order//p,q)!=1 for p in f):
            return g
    raise RuntimeError

def toy(n, t, q, restrict_b=None):
    assert (q-1)%n==0, f"need n|q-1: n={n} q={q}"
    g = primitive_root(q)
    # mu_n = { g^{(q-1)/n * j} : j=0..n-1 }; index by exponent k in Z/n
    zeta = pow(g, (q-1)//n, q)              # primitive n-th root
    x_of_k = [pow(zeta, k, q) for k in range(n)]
    assert len(set(x_of_k))==n

    def modp_tnull(K):
        for r in range(1,t+1):
            if sum(pow(x_of_k[k], r, q) for k in K)%q != 0:
                return False
        return True

    # M0 = least power of 2 > t
    M0=1
    while M0<=t: M0*=2
    M0=min(M0,n)
    # cosets of mu_{M0}: in exponent space, mu_{M0} = {k : k ≡ 0 mod n/M0}
    step = n//M0
    base = frozenset(range(0,n,step))       # mu_{M0} as exponents
    cosets=[]
    seen=set()
    for k0 in range(n):
        if k0 in seen: continue
        c=frozenset((k0+b)%n for b in base)
        cosets.append(c); seen|=c
    def powerset(it):
        s=list(it); return chain.from_iterable(combinations(s,r) for r in range(len(s)+1))
    structured=set()
    for combo in powerset(cosets):
        U=frozenset().union(*combo) if combo else frozenset()
        structured.add(U)

    sizes = range(n+1) if restrict_b is None else range(min(restrict_b,n)+1)
    modp=[]
    for size in sizes:
        for K in combinations(range(n), size):
            K=frozenset(K)
            if modp_tnull(K): modp.append(K)
    modp_set=set(modp)
    extras=[K for K in modp if K not in structured]

    entropy = log2(comb(n, n//2))
    cost = t*log2(q)
    return dict(n=n,t=t,q=q,M0=M0,
                n_structured=len(structured),
                n_modp=len(modp_set),
                n_extra=len(extras),
                cushion=n**3,
                entropy_bits=round(entropy,1),
                cost_bits=round(cost,1),
                extra_sizes=dict(sorted(Counter(len(K) for K in extras).items())),
                sample=[sorted(K) for K in sorted(extras,key=len) if 0<len(K)<n][:4])

print(f"{'n':>3} {'t':>2} {'q':>5} {'M0':>3} | {'struct':>6} {'modp':>6} {'EXTRA':>6} {'cushion':>7} | {'entropy':>7} {'cost':>6} | first extras")
print("-"*110)
rows=[]
# n=8 sweep (q=17 works: 8|16)
for t in [1,2,3]:
    rows.append(toy(8, t, 17))
# n=16 sweep (q=17)
for t in [1,2,3,4]:
    rows.append(toy(16, t, 17))
# n=16 with a larger q ≡ 1 mod 16 -> confirm extras vanish as q grows
rows.append(toy(16, 2, 97))
for r in rows:
    tag = "" if r['n_extra']<=r['cushion'] else "  <-- EXCEEDS CUSHION!"
    print(f"{r['n']:>3} {r['t']:>2} {r['q']:>5} {r['M0']:>3} | {r['n_structured']:>6} {r['n_modp']:>6} "
          f"{r['n_extra']:>6} {r['cushion']:>7} | {r['entropy_bits']:>7} {r['cost_bits']:>6} | "
          f"{r['extra_sizes']}{tag}")
print()
# detail on the first row that has extras
for r in rows:
    if r['n_extra']>0:
        print(f"first-extras detail  n={r['n']} t={r['t']} q={r['q']}: "
              f"{r['n_extra']} extras, sizes {r['extra_sizes']}")
        print(f"   sample exponent-sets: {r['sample']}")
        break
