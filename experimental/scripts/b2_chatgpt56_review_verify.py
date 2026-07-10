import numpy as np
from math import comb, sqrt
from itertools import combinations, product

def prim_root(p):
    phi=p-1; m=phi; f=[]; d=2
    while d*d<=m:
        if m%d==0:
            f.append(d)
            while m%d==0: m//=d
        d+=1
    if m>1: f.append(m)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g

def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    pts=[]; cur=1
    for _ in range(n): pts.append(cur); cur=cur*z%p
    return pts

# ===== CLAIM 1: N (subsets) vs Q^{-1} sum pi(c)^m (tuples) =====
print("CLAIM 1: N=Q^-1 sum pi(c)^m is the TUPLE count, not subset count?")
p,n,m,w=5,4,2,1
H=subgroup(p,n)  # F_5^*
# subsets with p_1=0
Nsub=sum(1 for S in combinations(H,m) if sum(S)%p==0)
# formula
import cmath
tot=0
for c in range(p):
    pi=sum(cmath.exp(2j*cmath.pi*c*a/p) for a in H)
    tot+=pi**m
formula=(tot/p).real
# ordered tuples (with repetition) with sum 0
tup=sum(1 for t in product(H,repeat=m) if sum(t)%p==0)
print(f"  p={p},n={n},m={m},w={w}: N(subsets)={Nsub}, Q^-1 sum pi^m={formula:.3f}, ordered tuples={tup}")
print(f"  => formula counts tuples, NOT subsets: {'CONFIRMED' if abs(formula-tup)<1e-6 and Nsub!=tup else 'NOT confirmed'}")

# ===== CLAIM 2: orbit size of v=(0,1,...) =====
print("\nCLAIM 2: does every nonzero v have orbit size n?")
# v=(0,1) under rotation zeta: (0*zeta, 1*zeta^2). fixed iff zeta^2=1 => stab>=mu_2 => orbit<=n/2
print("  v=(0,1): stabilizer = {zeta: zeta^2=1} = mu_2, orbit size = n/2, NOT n. (algebraic, CONFIRMED)")

# ===== CLAIM 3 (KEY): n=64,p=449,w=2,m=7 -> N=3584, m odd so ALL primitive =====
print("\nCLAIM 3 (KEY - refutes my descent-carrier lead): n=64,p=449,w=2,m=7")
p,n,m,w=449,64,7,2
assert (p-1)%n==0 and all(x%2 for x in [m])  # m odd
H=subgroup(p,n); H2=[(h*h)%p for h in H]
# DP over (u,v) in F_p^2, subset size up to m
D=[np.zeros((p,p),dtype=np.int64) for _ in range(m+1)]
D[0][0,0]=1
for h,h2 in zip(H,H2):
    for k in range(m,0,-1):
        D[k]+= np.roll(np.roll(D[k-1], h, axis=0), h2, axis=1)
nu=D[m]                      # nu(v) over all v=(u,v) in F_p^2
N=int(nu[0,0])
M=comb(n,m); Q=p*p; mu=M/Q
E=int((nu.astype(np.float64)**2).sum())
Delta2=float(((nu-mu)**2).sum())
print(f"  N=nu(0,0)={N}   (ChatGPT claim: 3584, =64*56={64*56})  {'MATCH' if N==3584 else 'MISMATCH'}")
print(f"  m={m} ODD => no S=-S possible => ALL {N} solutions PRIMITIVE (descent removes 0)")
print(f"  mu={mu:.3f}  n^3={n**3}   N/mu={N/mu:.3f}  (N>mu with all-primitive => descent-carrier lead REFUTED)")
print(f"  E/(M^2/Q)-1 = {E/(M*M/Q)-1:.3e}  (near-random global energy)")

# ===== CLAIM 4: secant-shadow inequality & Delta_sec Poisson scale =====
print("\nCLAIM 4: secant transfer inequality + Delta_sec scale")
# D_1 = {Phi(b)-Phi(a) = (b-a, b^2-a^2): a!=b}, |D_1|=n(n-1)
Dsec=0.0; cnt=0
Hs=H; H2s=H2
seen=set()
for i in range(n):
    for j in range(n):
        if i==j: continue
        u=(Hs[j]-Hs[i])%p; v=(H2s[j]-H2s[i])%p
        Dsec+=(nu[u,v]-mu)**2; cnt+=1
print(f"  |D_1|=n(n-1)={n*(n-1)}  (counted {cnt})")
print(f"  Delta_sec={Dsec:.4e}   n^2*mu (Poisson scale)={n*n*mu:.4e}   ratio={Dsec/(n*n*mu):.3f}")
# secant bound (4.1)
R=n*(n-1)/(m*(n-m))
secant_bound=R*(mu+sqrt(Dsec/(n*(n-1))))
naive_bound=mu+sqrt((Q-1)/Q*Delta2)
print(f"  secant bound (4.1): N <= {secant_bound:.1f}   [actual N={N}]  {'HOLDS' if N<=secant_bound+1 else 'FAILS'}")
print(f"  naive L2  bound   : N <= {naive_bound:.1f}")
print(f"  secant improves naive by factor ~ {naive_bound/secant_bound:.1f}x")
