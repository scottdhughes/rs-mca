import numpy as np
from math import comb, log, sqrt

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

p,n,w,m=97,32,3,16
G=subgroup(p,n)
grids=np.meshgrid(*[np.arange(p)]*w,indexing='ij')
C=np.stack([g.ravel() for g in grids],axis=1)
Mjk=np.array([[pow(h,j,p) for h in G] for j in range(1,w+1)],dtype=np.int64)
tau=np.exp(2j*np.pi*((C@Mjk)%p)/p).sum(axis=1)
def flat(Cc):
    idx=np.zeros(len(Cc),dtype=np.int64)
    for j in range(w): idx=idx*p+Cc[:,j]
    return idx
pr=[tau]+[tau[flat((C*r)%p)] for r in range(2,m+1)]
# nu-hat (signed) and B_c (positive majorant)
e=[np.ones(len(tau),dtype=complex)]+[np.zeros(len(tau),dtype=complex) for _ in range(m)]
for k in range(1,m+1):
    acc=np.zeros(len(tau),dtype=complex)
    for i in range(1,k+1): acc+=((-1)**(i-1))*e[k-i]*pr[i-1]
    e[k]=acc/k
nuhat=e[m]
ab=[np.abs(x) for x in pr]
b=[np.ones(len(tau))]+[np.zeros(len(tau)) for _ in range(m)]
for k in range(1,m+1):
    acc=np.zeros(len(tau))
    for i in range(1,k+1): acc+=b[k-i]*ab[i-1]
    b[k]=acc/k
B=b[m]
K=np.abs((tau.real**2+tau.imag**2)-n)
mask=flat(C)!=0
taumag=np.abs(tau)
mu=comb(n,m)/p**w; n2mu=n*n*mu; rt=sqrt(n)
bins=[(0,1.5),(1.5,2.5),(2.5,4),(4,6),(6,100)]   # |tau|/sqrt(n) bins
print(f"n={n} p={p} m={m} theta={log(mu)/log(n):.2f}  sqrt(n)={rt:.1f}. Loss structure by |tau(c)|/sqrt(n):")
print(f"{'|tau|/rtn':>12} {'#c':>8} {'sum|nuhat|K/n2mu':>16} {'sum B_c K/n2mu':>15} {'lossB/nu':>9}")
totA=totB=0
for lo,hi in bins:
    sel=mask & (taumag>=lo*rt) & (taumag<hi*rt)
    A=(np.abs(nuhat[sel])*K[sel]).sum()/n2mu
    Bs=(B[sel]*K[sel]).sum()/n2mu
    totA+=A; totB+=Bs
    print(f"  [{lo:>3.1f},{hi:>4.1f}) {sel.sum():>8} {A:>16.4f} {Bs:>15.4f} {Bs/max(A,1e-9):>9.1f}")
print(f"  {'TOTAL':>10} {mask.sum():>8} {totA:>16.4f} {totB:>15.4f} {totB/max(totA,1e-9):>9.1f}")
print("\n=> if sum B_c K is dominated by the large-|tau| (resonant) bins that are FEW,")
print("   a major/minor split (large sieve counts the resonant c) recovers the 43x factor.")
