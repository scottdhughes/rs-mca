import numpy as np
from math import comb, log, sqrt
from itertools import combinations

def isprime(m):
    i=2
    while i*i<=m:
        if m%i==0: return False
        i+=1
    return m>=2
def prim_root(p):
    phi=p-1; mm=phi; f=[]; d=2
    while d*d<=mm:
        if mm%d==0:
            f.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: f.append(mm)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g
def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    pts=[]; cur=1
    for _ in range(n): pts.append(cur); cur=cur*z%p
    return pts

def fiber_dp(p,n,m,w,pts):
    """nu(v) over F_p^w via subset DP; returns w-dim array."""
    powtab=[[pow(h,j,p) for h in pts] for j in range(1,w+1)]
    shape=(p,)*w
    D=[np.zeros(shape,dtype=np.float64) for _ in range(m+1)]
    D[0][(0,)*w]=1.0
    for hi in range(n):
        sh=tuple(powtab[j][hi] for j in range(w))
        for k in range(m,0,-1):
            rolled=D[k-1]
            for ax in range(w):
                rolled=np.roll(rolled, sh[ax], axis=ax)
            D[k]+=rolled
    return D[m]

def secant_ratio(p,n,m,w,r=1):
    pts=subgroup(p,n)
    nu=fiber_dp(p,n,m,w,pts)
    M=comb(n,m); Q=p**w; mu=M/Q
    # D_r = {F(B)-F(A): |A|=|B|=r disjoint}
    idxs=set()
    elts=list(range(n))
    from itertools import combinations as comb_it
    Phi=[[pow(pts[i],j,p) for j in range(1,w+1)] for i in range(n)]
    for A in comb_it(elts,r):
        FA=[sum(Phi[i][t] for i in A)%p for t in range(w)]
        rest=[i for i in elts if i not in A]
        for B in comb_it(rest,r):
            FB=[sum(Phi[i][t] for i in B)%p for t in range(w)]
            v=tuple((FB[t]-FA[t])%p for t in range(w))
            idxs.add(v)
    Dr=len(idxs)
    ss=0.0
    for v in idxs:
        ss+=(nu[v]-mu)**2
    Delta_r=ss
    P_r=comb(m,r)*comb(n-m,r)
    R_r=Dr/P_r
    bound=R_r*(mu+sqrt(Delta_r/Dr))
    N=float(nu[(0,)*w])
    return dict(mu=mu,N=N,Dr=Dr,ratio=Delta_r/(Dr*mu),Rr=R_r,bound_over_mu=bound/mu, Nmu=N/mu)

print("W-DEPENDENCE of the secant target Delta_sec/(|D_1| mu)  [caveat: does it survive w=2 -> w=3?]")
print(f"{'n':>4} {'p':>5} {'m':>3} {'w':>2} | {'mu':>10} {'N/mu':>6} {'Dsec/(|D1|mu)':>13}")
for (n,p,m) in [(32,193,10)]:
    for w in [2,3]:
        r=secant_ratio(p,n,m,w,r=1)
        print(f"{n:>4} {p:>5} {m:>3} {w:>2} | {r['mu']:>10.2f} {r['Nmu']:>6.3f} {r['ratio']:>13.4f}")

print("\nr-SWAP amplification (w=2): does higher r tighten the transfer? bound/mu = R_r(1+sqrt(ratio/... ))")
print(f"{'n':>4} {'p':>5} {'m':>3} {'r':>2} | {'|D_r|':>8} {'R_r':>7} {'Dr-var/(|Dr|mu)':>15} {'bound/mu':>9}")
for (n,p,m) in [(32,193,10),(48,433,15)]:
    if not isprime(p): continue
    for rr in [1,2]:
        try:
            res=secant_ratio(p,n,m,2,r=rr)
            print(f"{n:>4} {p:>5} {m:>3} {rr:>2} | {res['Dr']:>8} {res['Rr']:>7.2f} {res['ratio']:>15.4f} {res['bound_over_mu']:>9.2f}")
        except MemoryError:
            print(f"  n={n} r={rr}: too big")
