import numpy as np, math
from math import comb
def elt(p,n):
    for x in range(2,p):
        h=pow(x,(p-1)//n,p)
        if pow(h,n//2,p)!=1: return h
def mu_n(p,n):
    h=elt(p,n); S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    return S
def fixedweight_DP(p,n,w,m):  # N0^(k) for all k, at syndrome 0 (w=2)
    D=np.zeros((m+1,p,p)); D[0,0,0]=1
    for a in mu_n(p,n):
        a2=a*a%p; sh=np.roll(np.roll(D[:m],a,1),a2,2); D[1:]+=sh
    return D[:,0,0]   # N0^(k) for k=0..m
def bernoulli_shadow(p,n,w,m,rho):  # S_rho = Pr_rho(F(X)=0) exactly
    D=np.zeros((p,p)); D[0,0]=1.0
    for a in mu_n(p,n):
        a2=a*a%p
        D=(1-rho)*D + rho*np.roll(np.roll(D,a,0),a2,1)
    return D[0,0]

print("VERIFY Codex's Bernoulli reformulation: N0 <= S_rho / [rho^m (1-rho)^(n-m)], cost <= sqrt(2n)?")
print(f"{'p':>4} {'n':>3} {'w':>2} {'m':>3} {'N0':>6} {'S_rho/wt':>12} {'cost=ratio':>11} {'sqrt(2n)':>9} {'ok':>4}")
for (p,n,w,m) in [(17,16,2,6),(17,16,2,8),(97,16,2,6),(193,16,2,8),(97,32,2,13)]:
    if (p-1)%n: continue
    rho=m/n
    N0k=fixedweight_DP(p,n,w,m); N0=N0k[m]
    Srho=bernoulli_shadow(p,n,w,m,rho)
    wt=rho**m*(1-rho)**(n-m)
    bound=Srho/wt
    cost=bound/N0 if N0>0 else float('inf')
    s2n=math.sqrt(2*n)
    ok = (N0<=bound+1e-9) and (cost<=s2n+1e-6 or N0==0)
    print(f"{p:>4} {n:>3} {w:>2} {m:>3} {int(N0):>6} {bound:>12.3f} {cost:>11.3f} {s2n:>9.3f} {str(ok):>4}")

# Spot-check Codex's falsifier: D_r^- = {v in F_p^w : even coords 0, odd part nonzero}, r related to w
# Codex row (17,16,3,1): |D_1^-|=16, hits=176, R = p^w/|D| * Pr(F(X in D)) with rho=1/2? 'hits' at rho? 
# It says "exhaustive enumeration at rho=1/2". #hits = # subsets X (all sizes) with F(X) in D_r^-, weighted? 
# Codex's 'hits' looks like an unweighted count over all 2^n subsets. Let me reproduce (17,16,3,1).
def count_hits_D1minus(p,n,w):
    # D_1^-: w=3 here; syndrome (p1,p2,p3); even coord = p2 must be 0; odd part (p1,p3) nonzero
    S=mu_n(p,n); import itertools; hits=0
    for r in range(n+1):
        for X in itertools.combinations(range(n),r):
            p1=sum(S[i] for i in X)%p; p2=sum(S[i]**2 for i in X)%p; p3=sum(S[i]**3 for i in X)%p
            if p2==0 and (p1!=0 or p3!=0): hits+=1
    return hits
h=count_hits_D1minus(17,16,3); print(f"\nCodex table spot-check (17,16,3,1): my #hits(p2=0,odd!=0 over ALL subsets)={h}  (Codex said 176)")
