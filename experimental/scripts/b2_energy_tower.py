import numpy as np
from math import comb, log
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

# Energy excess Delta = E - C(n,m)^2/p^w, and its odd/even (primitive/descent) Fourier split.
# Delta = p^-w sum_{c!=0} |nuhat(c)|^2.  Even-freq c (odd part 0) = MAJOR arc (descent to mu_{n/2}),
# odd-freq c = MINOR arc (primitive). Does the descent recurse cleanly?
p,n,w,m=97,16,3,8
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
e=[np.ones(len(tau),dtype=complex)]+[np.zeros(len(tau),dtype=complex) for _ in range(m)]
for k in range(1,m+1):
    acc=np.zeros(len(tau),dtype=complex)
    for i in range(1,k+1): acc+=((-1)**(i-1))*e[k-i]*pr[i-1]
    e[k]=acc/k
nuhat=e[m]; nh2=(nuhat.real**2+nuhat.imag**2)
fl=flat(C)
mu=comb(n,m)/p**w
Delta=nh2[fl!=0].sum()/p**w
# even-freq c: c_j=0 for odd j (here odd j in {1,3}, even j=2) -> major arc
even=(C[:,0]==0)&(C[:,2]==0)&(fl!=0)
odd_ =(~((C[:,0]==0)&(C[:,2]==0)))&(fl!=0)
Dmaj=nh2[even].sum()/p**w; Dmin=nh2[odd_].sum()/p**w
# descent prediction: major arc should = energy of mu_{n/2} problem (n/2=8, w/2=1)
print(f"n={n} p={p} w={w} m={m} theta={log(mu)/log(n):.2f}")
print(f"  Delta (energy excess, c!=0)        = {Delta:.3e}   (= E - C(n,m)^2/p^w)")
print(f"  random-model E-C^2/p^w ~ C(n,m)^2/p^w*(collisions)... ; mean mu={mu:.4f}")
print(f"  MAJOR arc (even-freq, descent)      = {Dmaj:.3e}   ({Dmaj/Delta*100:.1f}% of Delta)")
print(f"  MINOR arc (odd-freq, primitive)     = {Dmin:.3e}   ({Dmin/Delta*100:.1f}% of Delta)")
print(f"  => if major arc dominates AND descends to a smaller SAME-type energy, the tower recursion")
print(f"     could close; if minor (primitive) dominates, that's the irreducible frontier piece.")
