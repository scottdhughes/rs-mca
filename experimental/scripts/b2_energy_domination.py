import numpy as np
from math import lgamma, log2, log

def logC(N,K):
    if K<0 or K>N or N<0: return -np.inf
    return (lgamma(N+1)-lgamma(K+1)-lgamma(N-K+1))/log(2)  # log2 C(N,K)

# Deployment-ish params (KoalaBear L1 row)
n   = 2**21          # 2097152
w   = 67471
logp = 31.0          # p ~ 2^31 (KoalaBear)
print(f"n={n}  w={w}  p~2^{logp}   (tail terms d>w)")
print(f"{'rho':>5} {'m':>9} | {'argmax d*':>10} {'d*/w':>7} {'d*/n':>7} | "
      f"{'edge log2 term':>15} {'peak log2 term':>15} {'edge-peak gap(bits)':>20}")
print("-"*100)
for rho in [0.10, 0.30, 0.48]:
    m=int(rho*n)
    # tail term T_d = C(n-2d,m-d) * E_d,  E_d ~ C(n,d)*C(n-d,d)/p^w  (random model, valid at deployed large p)
    dmax=min(m, n-m)          # weight nonzero only for d<=m and n-2d>=m-d
    ds=np.arange(w+1, dmax, max(1,(dmax-w)//4000))
    def logterm(d):
        lE = logC(n,d)+logC(n-d,d) - w*logp        # log2 E_d (random)
        lW = logC(n-2*d, m-d)                        # log2 weight
        return lW+lE
    vals=np.array([logterm(int(d)) for d in ds])
    i=np.argmax(vals); dstar=int(ds[i])
    edge=logterm(w+1)
    print(f"{rho:>5} {m:>9} | {dstar:>10} {dstar/w:>7.2f} {dstar/n:>7.3f} | "
          f"{edge:>15.1f} {vals[i]:>15.1f} {vals[i]-edge:>20.1f}")
print()
print("Reading: if d*/w >> 1 (argmax far above the edge), the energy tail is BULK-dominated =>")
print("the small-d edge (char-0 PTE / vanishing-sums-controlled) is exponentially subdominant in E.")
print("edge-peak gap in bits = how many bits smaller the edge term is than the dominant term.")
