import numpy as np, math, itertools
from collections import defaultdict
from math import comb
def mu_n(p,n):
    def order(x):
        o=1;v=x
        while v!=1:v=v*x%p;o+=1
        return o
    g=next(c for c in range(2,p) if order(c)==p-1)
    h=pow(g,(p-1)//n,p);S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    return S
def analyze(p,n,m):
    S=np.array(mu_n(p,n)); rho=m/n; tp=2*math.pi/p
    S2=(S*S)%p
    # T(xi) for all xi in F_p^2, via tau_2(xi)=sum_a e_p(xi.Phi(a))
    c1=np.arange(p); c2=np.arange(p)
    # tau[c1,c2] = sum_a exp(tp*(c1*a + c2*a^2))
    A=np.exp(tp*1j*np.outer(np.arange(p),S))        # (p, n): exp(tp i c1 a)
    B=np.exp(tp*1j*np.outer(np.arange(p),S2))       # (p, n): exp(tp i c2 a^2)
    # tau[c1,c2] = sum_a A[c1,a]*B[c2,a]  = A @ B^T
    tau=A@B.T                                        # (p,p) complex
    T=n-tau.real                                     # (p,p)
    D=np.exp(-rho*(1-rho)*T).sum()/p**2              # resonance sum / p^2
    # resonant frequencies: T(xi) small (xi!=0)
    Tflat=T.copy(); Tflat[0,0]=1e9
    order=np.argsort(Tflat.ravel())
    # true max fiber via DP
    Dl=[np.zeros((p,p)) for _ in range(m+1)]; Dl[0][0,0]=1.0
    for a,a2 in zip(S.tolist(),S2.tolist()):
        for k in range(m,0,-1): Dl[k]+=np.roll(np.roll(Dl[k-1],a,0),a2,1)
    N=Dl[m]; fmax=N.max(); mean=comb(n,m)/p**2; R=fmax/mean
    print(f"n={n} p={p} m={m} rho={rho:.2f}: mean={mean:.2f} f_max={fmax:.0f} R=f_max/mean={R:.3f}")
    print(f"   RV/Halasz resonance sum D=(1/p^2)sum_xi exp(-rho(1-rho)T) = {D:.3f}  (max fiber <~ mean*D; sign-blind)")
    print(f"   2nd-moment (sign-blind) gives R<=p={p}. RV-LCD target: D=poly, ideally O(1).")
    # how many resonant xi (T < n/4), and their max |tau|
    nres=(Tflat<n/4).sum(); print(f"   #resonant xi (T<n/4, xi!=0) = {nres}  (out of p^2={p*p}); min T (xi!=0) = {Tflat.min():.3f}")
    # top-5 resonant xi
    print("   top resonant xi (c1,c2,T,|tau|):")
    for idx in order[:5]:
        i,j=idx//p, idx%p
        print(f"      ({i},{j}) T={T[i,j]:.2f} |tau|={abs(tau[i,j]):.2f} (n={n})")
    return R,D
for (p,n,m) in [(17,16,8),(41,20,10),(73,24,12)]:
    analyze(p,n,m); print()
