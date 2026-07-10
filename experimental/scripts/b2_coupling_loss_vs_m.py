import numpy as np
from math import comb, log

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

p,n,w=97,32,3; MMAX=24
G=subgroup(p,n)
grids=np.meshgrid(*[np.arange(p)]*w,indexing='ij')
C=np.stack([g.ravel() for g in grids],axis=1)
Mjk=np.array([[pow(h,j,p) for h in G] for j in range(1,w+1)],dtype=np.int64)
tau=np.exp(2j*np.pi*((C@Mjk)%p)/p).sum(axis=1)
def flat(Cc):
    idx=np.zeros(len(Cc),dtype=np.int64)
    for j in range(w): idx=idx*p+Cc[:,j]
    return idx
pr=[tau]+[tau[flat((C*r)%p)] for r in range(2,MMAX+1)]
ab=[np.abs(x) for x in pr]
K=np.abs((tau.real**2+tau.imag**2)-n); mask=flat(C)!=0
# build e[k] (signed) and b[k] (majorant) cumulatively
e=[np.ones(len(tau),dtype=complex)]; bb=[np.ones(len(tau))]
print(f"n={n} p={p} w={w}. Coupling loss factor  ΣB_c|K| / Σ|nuhat||K|  vs m:")
print(f"{'m':>3} {'theta':>6} {'Tri|nuhat|/n2mu':>16} {'ΣB_c|K|/n2mu':>14} {'loss factor':>12} {'loss/m':>8}")
for k in range(1,MMAX+1):
    acc=np.zeros(len(tau),dtype=complex); accb=np.zeros(len(tau))
    for i in range(1,k+1):
        acc+=((-1)**(i-1))*e[k-i]*pr[i-1]; accb+=bb[k-i]*ab[i-1]
    e.append(acc/k); bb.append(accb/k)
    m=k
    if m in (4,8,12,16,20,24):
        mu=comb(n,m)/p**w; n2mu=n*n*mu
        A=(np.abs(e[m][mask])*K[mask]).sum()/n2mu
        Bs=(bb[m][mask]*K[mask]).sum()/n2mu
        print(f"{m:>3} {log(mu)/log(n):>6.2f} {A:>16.4f} {Bs:>14.4f} {Bs/max(A,1e-12):>12.1f} {Bs/max(A,1e-12)/m:>8.2f}")
print("\n=> loss factor ~ linear/poly in m  => coupling bound CLOSES SV* (budget n^{3-theta} outgrows it).")
print("   loss factor ~ exponential in m   => coupling too loose; need a sharper e_m inequality.")
