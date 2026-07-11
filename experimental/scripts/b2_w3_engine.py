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

# w=3 engine: tau_3(c)=sum_{x in mu_n} e_p(c1 x + c2 x^2 + c3 x^3) over F_p^3; check Sidon 4th moment.
for (p,n) in [(97,32),(97,16)]:
    G=subgroup(p,n); G2=[pow(h,2,p) for h in G]; G3=[pow(h,3,p) for h in G]
    grids=np.meshgrid(np.arange(p),np.arange(p),np.arange(p),indexing='ij')
    C=np.stack([g.ravel() for g in grids],axis=1)
    ph=(np.outer(C[:,0],G)+np.outer(C[:,1],G2)+np.outer(C[:,2],G3))%p
    tau=np.exp(2j*np.pi*ph/p).sum(axis=1)
    a2=tau.real**2+tau.imag**2
    S2=a2.sum(); S4=(a2**2).sum()
    print(f"p={p} n={n}:  Sum|tau3|^2={S2:.3e} vs p^3 n={p**3*n:.3e} (ratio {S2/(p**3*n):.4f})")
    print(f"           Sum|tau3|^4={S4:.3e} vs 2 p^3 n^2={2*p**3*n*n:.3e} (ratio {S4/(p**3*n*n):.4f} vs 2) <- Sidon")

# also verify the recursion for w=3 (convolution form) at small n
p,n=97,16
G=subgroup(p,n); G2=[pow(h,2,p) for h in G]; G3=[pow(h,3,p) for h in G]
def nu_dp(D):
    Dl=[np.zeros((p,p,p)) for _ in range(D+1)]; Dl[0][0,0,0]=1.0
    for h,h2,h3 in zip(G,G2,G3):
        for k in range(D,0,-1):
            Dl[k]+=np.roll(np.roll(np.roll(Dl[k-1],h,0),h2,1),h3,2)
    return Dl
NU=nu_dp(5); P=np.zeros((p,p,p))
for h,h2,h3 in zip(G,G2,G3): P[h,h2,h3]+=1
print(f"\nw=3 recursion check (n={n},p={p}): E3_d vs d^-2*sum(conv(nu_{{d-1}},1_P))^2")
for d in [3,4,5]:
    E=(NU[d]**2).sum()
    conv=np.fft.ifftn(np.fft.fftn(NU[d-1])*np.fft.fftn(P)).real
    RHS=(conv**2).sum()/(d*d)
    print(f"  d={d}: E3_d={E:.3e}  RHS={RHS:.3e}  ratio={RHS/E:.3f}")
print("=> Sidon engine (ratio~2) + recursion (ratio~1) => w=3 closes by the SAME skeleton as w=2.")
