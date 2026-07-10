import numpy as np
from math import comb, log, sqrt
from itertools import combinations

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
    return [pow(z,k,p) for k in range(n)]

def fiber_w2(p,n,m,pts):
    D=[np.zeros((p,p),dtype=np.float64) for _ in range(m+1)]
    D[0][0,0]=1.0
    for h in pts:
        h2=(h*h)%p
        for k in range(m,0,-1):
            D[k]+=np.roll(np.roll(D[k-1],h,axis=0),h2,axis=1)
    return D[m]

def secant(p,n,m,pts,nu):
    mu=comb(n,m)/(p*p)
    Dsec=0.0; seen=set()
    for i in range(n):
        for j in range(n):
            if i==j: continue
            u=(pts[j]-pts[i])%p; v=((pts[j]**2-pts[i]**2))%p
            Dsec+=(nu[u,v]-mu)**2
    return Dsec, mu

print("=== CLAIM: dyadic block obstruction makes Delta_sec >> n^2 mu when B_{q,k}>mu (small theta) ===")
# n=16, q=4>w=2, m=8=k*q (k=2), p large so mu small
for p in [257, 97]:
    n,w,m=16,2,8
    pts=subgroup(p,n)
    # verify mu_4 coset is a zero solution
    mu4_idx=[k for k in range(n) if (4*k)%n==0]  # elements of order|4 => indices k with n | 4k => k in {0,4,8,12}
    mu4=[pts[k] for k in mu4_idx]
    ps1=sum(mu4)%p; ps2=sum(x*x for x in mu4)%p
    # block solution = 2 cosets of mu_4. cosets: multiply mu_4 by coset reps
    cosets=[]
    used=set()
    for k in range(n):
        if k in used: continue
        cos=tuple(sorted((k+j)%n for j in mu4_idx))
        cosets.append(cos)
        used.update(cos)
    L=len(cosets)
    block=set(cosets[0])|set(cosets[1])   # union of 2 cosets, |block|=8=m
    bp1=sum(pts[k] for k in block)%p; bp2=sum(pts[k]**2 for k in block)%p
    # theory
    k_=m//4; B=comb(L-2,k_-1); Nqk=comb(L,k_)
    nu=fiber_w2(p,n,m,pts)
    mu=comb(n,m)/(p*p)
    N=nu[0,0]
    Dsec,_=secant(p,n,m,pts,nu)
    lb=n*(n-4)*max(0.0,(B-mu))**2   # ChatGPT lower bound (1.4)
    print(f"\n p={p}: mu4 power sums (p1,p2)=({ps1},{ps2}) [should be 0,0];  block(2 cosets) sums=({bp1},{bp2}) [0,0]")
    print(f"   L={L} cosets, k={k_}, B_qk=C({L-2},{k_-1})={B}, N_qk=C({L},{k_})={Nqk}, mu={mu:.3f}, N={N:.0f}")
    print(f"   B>mu? {B>mu}   Delta_sec/n^2mu = {Dsec/(n*n*mu):.2f}   (ChatGPT LB (1.4)/n^2mu = {lb/(n*n*mu):.2f})")
    # check a cross-coset secant fiber >= B
    a=cosets[0][0]; b=cosets[1][0]
    du=(pts[b]-pts[a])%p; dv=(pts[b]**2-pts[a]**2)%p
    print(f"   nu(d_ab) for cross-coset a,b = {nu[du,dv]:.0f}  (theory: >= B={B})  {'OK' if nu[du,dv]>=B else 'FAIL'}")

print("\n=== CONTRAST: same structure but B<mu (moderate theta) => no obstruction ===")
# n=32, q=4>w=2, m=16=k*4 (k=4), p moderate so mu large
n,w,m,p=32,2,16,193
pts=subgroup(p,n)
nu=fiber_w2(p,n,m,pts); mu=comb(n,m)/(p*p)
Dsec,_=secant(p,n,m,pts,nu)
L=8; k_=4; B=comb(L-2,k_-1)
print(f" n=32,p=193,m=16: L={L},k={k_},B={B},mu={mu:.1f}  B>mu? {B>mu}  Delta_sec/n^2mu={Dsec/(n*n*mu):.3f}")
print(" => obstruction is REGIME-DEPENDENT: present only when B_qk>mu (small entropy gap).")
