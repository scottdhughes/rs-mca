#!/usr/bin/env python3
"""
b2 Step 2, prong 1 (setup): the FIXED-degree-b count -- the correct target.

Correction to the first-move scoping: b2 bounds NON-coset-union t-null blocks of a
FIXED size b in the giant regime (b > t), i.e. monic degree-b divisors of X^n-1 with
a top-t coefficient gap (attack_surface).  The all-sizes N_t is the wrong object: at
prize scale N_t ~ 2^{n - t log2 q} >> n^3, but per-fixed-giant-b counts are tiny.

This script:
  (A) buckets ALL t-null blocks (Codex-green MITM/brute) by (size b, structured?),
      where structured = M_sym >= M0 = least 2-power > t (b1 coarse coset-unions);
  (B) independently computes N_{t,b} = #{t-null blocks of size b} via an EXACT
      size-marked integer DP;  cross-checks (A) per-b totals against (B);
  and reports the extras-by-size, highlighting the giant regime b > t vs n^3.

Structural note tested here: a mu_{M0}-coset-union has size divisible by M0, so at any
size b NOT divisible by M0 EVERY t-null block is automatically an extra
(cf. u2c "weight not divisible by 16 => automatically primitive").

Primitives below are copied verbatim from the Codex-green b2_phase0_dichotomy.py /
b2_charsum_crosscheck.py.
"""
from itertools import combinations
from collections import defaultdict, Counter

def _isprime(m):
    if m<2: return False
    i=2
    while i*i<=m:
        if m%i==0: return False
        i+=1
    return True

def primitive_root(q):
    assert _isprime(q), f"q must be prime: {q}"
    order=q-1; f=set(); m=order; d=2
    while d*d<=m:
        while m%d==0: f.add(d); m//=d
        d+=1
    if m>1: f.add(m)
    for g in range(2,q):
        if all(pow(g,order//p,q)!=1 for p in f): return g
    raise RuntimeError

def mu_n(n,q):
    assert (q-1)%n==0, f"need n|q-1 (so mu_n <= F_q): n={n} q={q}"
    g=primitive_root(q); zeta=pow(g,(q-1)//n,q)
    xs=[pow(zeta,k,q) for k in range(n)]
    assert len(set(xs))==n, "zeta must be a primitive n-th root"
    return xs

def M_sym(K, n):
    Kset=set(K); M=n
    while M>=2:
        d=n//M
        if all(((k+d)%n) in Kset for k in Kset):
            return M
        M//=2
    return 1

def powersum_vec(K, xs, t, q):
    v=[0]*t
    for k in K:
        xr=xs[k]
        for r in range(t):
            v[r]=(v[r]+xr)%q
            xr=(xr*xs[k])%q
    return tuple(v)

def all_tnull_full(n,t,q):
    xs=mu_n(n,q); out=[]
    z=tuple([0]*t)
    for size in range(n+1):
        for K in combinations(range(n),size):
            if powersum_vec(K,xs,t,q)==z:
                out.append(frozenset(K))
    return out

def all_tnull_mitm(n,t,q):
    xs=mu_n(n,q); half=n//2
    left=defaultdict(list)
    for mask in range(1<<half):
        K=[i for i in range(half) if (mask>>i)&1]
        left[powersum_vec(K,xs,t,q)].append(K)
    out=[]
    for mask in range(1<<half):
        K=[half+i for i in range(half) if (mask>>i)&1]
        need=tuple((-x)%q for x in powersum_vec(K,xs,t,q))
        if need in left:
            for LK in left[need]:
                out.append(frozenset(LK+K))
    return out

# ---------- (B) exact size-marked DP: N_{t,b} = #{t-null blocks of size b} ----------
def fixed_b_counts_DP(n,t,q):
    xs=mu_n(n,q)
    zero=(0,)*t
    dp={(0,zero):1}                       # (size, powersum vector) -> count
    for x in xs:
        pv=[]; xr=x
        for r in range(t):
            pv.append(xr); xr=(xr*x)%q
        pv=tuple(pv)
        ndp=defaultdict(int)
        for (s,v),c in dp.items():
            ndp[(s,v)]+=c                                   # exclude x
            nv=tuple((v[i]+pv[i])%q for i in range(t))
            ndp[(s+1,nv)]+=c                                # include x
        dp=ndp
    return {b: dp.get((b,zero),0) for b in range(n+1)}

# ---------- (A) bucket t-null blocks by (size, structured?) ----------
def bucket(n,t,q,blocks):
    M0=1
    while M0<=t: M0*=2
    M0=min(M0,n)
    per=defaultdict(lambda:[0,0])   # size b -> [structured, extra]
    for K in blocks:
        b=len(K)
        if M_sym(K,n)>=M0: per[b][0]+=1
        else:              per[b][1]+=1
    return M0, per

def analyze(name,n,t,q, use_mitm=False, do_DP=True):
    print(f"=== {name}: n={n} t={t} q={q} ===")
    blocks = all_tnull_mitm(n,t,q) if use_mitm else all_tnull_full(n,t,q)
    M0, per = bucket(n,t,q,blocks)
    print(f"  M0 (least 2-power > t) = {M0};  n^3 = {n**3}")
    # cross-check per-b totals against independent DP
    if do_DP:
        DP=fixed_b_counts_DP(n,t,q)
        ok=all((per[b][0]+per[b][1])==DP[b] for b in range(n+1))
        print(f"  cross-check (A bucket totals == B size-DP N_(t,b)) : {'MATCH' if ok else 'MISMATCH!'}")
    tot_extra=sum(v[1] for v in per.values())
    print(f"  total extras (all giant+small sizes) = {tot_extra}   within n^3? {tot_extra<=n**3}")
    print(f"  {'b':>3} {'giant?':>6} {'total':>7} {'struct':>7} {'EXTRA':>7} {'b%M0':>5}")
    for b in sorted(per):
        s,e=per[b]
        if s+e==0: continue
        print(f"  {b:>3} {('b>t' if b>t else '.'):>6} {s+e:>7} {s:>7} {e:>7} {b%M0:>5}")
    print()
    return tot_extra

print("b2 prong 1: fixed-degree-b extras (the correct target)\n")
analyze("small (full+DP)",       16,2,17, use_mitm=False, do_DP=True)
analyze("t=2 (MITM+DP xcheck)",  32,2,97, use_mitm=True,  do_DP=True)
analyze("near-balance giant (MITM)", 32,4,97, use_mitm=True, do_DP=False)  # DP state too big at t=4
