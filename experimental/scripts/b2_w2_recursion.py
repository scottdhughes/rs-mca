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

p,n,w=97,16,2
G=subgroup(p,n); G2=[pow(h,2,p) for h in G]
# build nu_d(v) for d=0..D via DP
def nu_dp(D):
    Dl=[np.zeros((p,p),dtype=np.float64) for _ in range(D+1)]
    Dl[0][0,0]=1.0
    for h,h2 in zip(G,G2):
        for k in range(D,0,-1):
            Dl[k]+=np.roll(np.roll(Dl[k-1],h,0),h2,1)
    return Dl
Dmax=5
NU=nu_dp(Dmax)
# parabola indicator 1_P
P=np.zeros((p,p)); 
for h,h2 in zip(G,G2): P[h,h2]+=1
print(f"n={n} p={p} w={w}. Verify recursion  d*nu_d ~ (nu_{{d-1}} * 1_P) - correction, and the energy form.")
print(f"{'d':>3} {'E2_d = sum nu_d^2':>18} {'recursion RHS (energy form)':>28} {'ratio':>7}")
for d in range(3,Dmax+1):
    E_exact=(NU[d]**2).sum()
    # recursion RHS: (1/d^2) sum_{x,x'} corr(nu_{d-1}, shift Phi(x)-Phi(x'))
    #   = (1/d^2) sum_v (conv(nu_{d-1},1_P)(v))^2  -- via convolution (cyclic in F_p^2)
    conv=np.fft.ifft2(np.fft.fft2(NU[d-1])*np.fft.fft2(P)).real
    RHS=(conv**2).sum()/(d*d)
    print(f"{d:>3} {E_exact:>18.4e} {RHS:>28.4e} {RHS/E_exact:>7.3f}")
print("\n(ratio ~1 confirms the convolution recursion drives the energy; the off-diagonal (x!=x') secant-shifted")
print(" energies are the Rudnev target. The 'correction' (x already in A) is lower order -- check ratio.)")
