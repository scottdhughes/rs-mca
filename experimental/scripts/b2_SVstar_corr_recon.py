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

# deployment-theta instance: n=32,p=97,w=3,m=16 (theta~1.87)
p,n,w,m=97,32,3,16
G=subgroup(p,n)
# tau(c) over F_p^3
grids=np.meshgrid(*[np.arange(p)]*w,indexing='ij')
C=np.stack([g.ravel() for g in grids],axis=1)          # (p^3, 3) columns c1,c2,c3
Mjk=np.array([[pow(h,j,p) for h in G] for j in range(1,w+1)],dtype=np.int64)  # (3,n)
ph=(C@Mjk)%p
tau=np.exp(2j*np.pi*ph/p).sum(axis=1)                   # tau(c), length p^3
def flat(Cc):
    idx=np.zeros(len(Cc),dtype=np.int64)
    for j in range(w): idx=idx*p+Cc[:,j]
    return idx
# power sums p_r[c] = tau(r c),  r=1..m  (dilate lookups)
pr=[tau]  # r=1
for r in range(2,m+1):
    pr.append(tau[flat((C*r)%p)])
# nu-hat(c) = e_m via Newton from p_r, vectorized over c
e=[np.ones(len(tau),dtype=complex)]+[np.zeros(len(tau),dtype=complex) for _ in range(m)]
for k in range(1,m+1):
    acc=np.zeros(len(tau),dtype=complex)
    for i in range(1,k+1):
        acc+=((-1)**(i-1))*e[k-i]*pr[i-1]
    e[k]=acc/k
nuhat=e[m]
K=(tau.real**2+tau.imag**2)-n                            # |tau(c)|^2 - n
mask=flat(C)!=0                                           # c != 0
mu=comb(n,m)/p**w
Corr=(nuhat[mask]*K[mask]).sum().real/p**w
Tri =(np.abs(nuhat[mask])*np.abs(K[mask])).sum()/p**w
n2mu=n*n*mu
print(f"n={n} p={p} w={w} m={m}  theta={log(mu)/log(n):.2f}  mu={mu:.2f}  |D_1|mu~n^2mu={n2mu:.3e}")
print(f"  Corr = p^-w sum_c!=0 nuhat(c)(|tau|^2-n) = {Corr:.4e}   Corr/(n^2 mu) = {Corr/n2mu:.4f}")
print(f"  Triangle sum|nuhat||K|                    = {Tri:.4e}   Tri /(n^2 mu) = {Tri/n2mu:.4f}")
print(f"  CANCELLATION factor Triangle/|Corr|       = {Tri/abs(Corr):.2f}")
print(f"  => if ~O(1): coupling+triangle suffices.  if >>1: need SIGNED cancellation.")
# cross-check: shadow count = n^2mu + Corr should match direct secant fiber sum
