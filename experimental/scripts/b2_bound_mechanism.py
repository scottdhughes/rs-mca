#!/usr/bin/env python3
"""
b2 bound mechanism scoping: which quantity actually bounds extras_b <= n^3, and how does it scale?
Near-balance giant regime (32,4,97). Per giant b (b not divisible by M0=8, so all t-null of size b
are extras): compare
   first_moment = C(n,b)/q^t   (the c=0 main term)
   actual       = N_{t,b}      (exact, via MITM)
   mean|S_b(c)|, max|S_b(c)|    (sampled; extras_b <= mean|S_b(c)| is the L1 bound)
   n^3
to see the true mechanism.  S_b(c) = [z^b] prod_{x in mu_n}(1 + z e_q(f_c(x))), f_c=sum_r c_r x^r.
"""
import cmath, math, random
from math import comb
from collections import defaultdict

q, n, t = 97, 32, 4
random.seed(12345)

def primroot(q):
    for g in range(2, q):
        seen=set(); x=1
        for _ in range(q-1):
            x=x*g%q; seen.add(x)
        if len(seen)==q-1: return g
g=primroot(q); zeta=pow(g,(q-1)//n,q)
mu=[pow(zeta,k,q) for k in range(n)]
eq=[cmath.exp(2j*math.pi*u/q) for u in range(q)]

def powvec(k):                      # (x, x^2, ..., x^t) mod q for x=mu[k]
    x=mu[k]; v=[]; xr=x
    for _ in range(t): v.append(xr); xr=xr*x%q
    return v
PV=[powvec(k) for k in range(n)]

def Sb_all(c):                      # returns dict b -> |S_b(c)| via z-polynomial coeffs
    coeff=[0j]*(n+1); coeff[0]=1+0j
    for k in range(n):
        s=sum(c[r]*PV[k][r] for r in range(t))%q
        y=eq[s]
        for i in range(n,0,-1): coeff[i]+=coeff[i-1]*y
    return coeff

# actual N_{t,b} via MITM (exact)
def mitm_counts():
    half=n//2
    from collections import defaultdict
    left=defaultdict(list)
    for mask in range(1<<half):
        vv=[0]*t
        for i in range(half):
            if (mask>>i)&1:
                for r in range(t): vv[r]=(vv[r]+PV[i][r])%q
        left[tuple(vv)].append(bin(mask).count('1'))
    cnt=defaultdict(int)
    for mask in range(1<<half):
        vv=[0]*t
        for i in range(half):
            if (mask>>i)&1:
                for r in range(t): vv[r]=(vv[r]+PV[half+i][r])%q
        need=tuple((-x)%q for x in vv)
        rb=bin(mask).count('1')
        if need in left:
            for lb in left[need]: cnt[lb+rb]+=1
    return cnt

actual=mitm_counts()
M0=8
# sample |S_b(c)| over random c != 0
NS=20000
giant_bs=[b for b in range(t+1,n) if b%M0!=0 and actual.get(b,0)>0]
sums={b:0.0 for b in giant_bs}; maxs={b:0.0 for b in giant_bs}
for _ in range(NS):
    c=[random.randrange(q) for _ in range(t)]
    if not any(c): continue
    coeff=Sb_all(c)
    for b in giant_bs:
        a=abs(coeff[b]); sums[b]+=a; maxs[b]=max(maxs[b],a)

print(f"b2 bound mechanism  n={n} t={t} q={q}  n^3={n**3}")
print(f"{'b':>3} {'first_moment':>12} {'actual':>7} {'mean|S_b|':>10} {'max|S_b|':>10} {'actual<=mean?':>13} {'mean<=n^3?':>10}")
for b in giant_bs:
    fm=comb(n,b)/q**t
    mean=sums[b]/NS; mx=maxs[b]
    print(f"{b:>3} {fm:>12.2f} {actual[b]:>7} {mean:>10.1f} {mx:>10.1f} {str(actual[b]<=mean):>13} {str(mean<=n**3):>10}")
print("\nREAD: if actual<=mean|S_b(c)|<=n^3 across giant b, the L1-average is the bound; then the lemma")
print("needs a bound on the AVERAGE polynomial-subgroup char-sum mass (Bourgain-Chang regime), crude OK.")
