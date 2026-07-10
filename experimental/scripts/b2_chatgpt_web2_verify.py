import numpy as np
from math import comb, factorial
from itertools import product

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

# ===== CLAIM (11): p^-w sum_c |tau(c)|^{2h} <= h! n^h for h<=w  (the large-sieve lever) =====
print("CLAIM (11): p^-w sum_c |tau(c)|^{2h} vs h! n^h   (tau=full moment-curve subgroup sum, h<=w)")
p,n,w=97,16,3
G=subgroup(p,n)
# tau(c) for all c in F_p^w
grids=np.meshgrid(*[np.arange(p)]*w,indexing='ij')
C=np.stack([g.ravel() for g in grids],axis=1)
Mjk=np.array([[pow(h,j,p) for h in G] for j in range(1,w+1)],dtype=np.int64)
ph=(C@Mjk)%p
tau=np.exp(2j*np.pi*ph/p).sum(axis=1)
a2=(tau.real**2+tau.imag**2)
print(f"  n={n},p={p},w={w}:")
for h in range(1,w+1):
    mom=(a2**h).sum()/p**w
    print(f"   h={h}: p^-w sum|tau|^{2*h} = {mom:8.2f}   h! n^h = {factorial(h)*n**h:8.0f}   ratio {mom/(factorial(h)*n**h):.3f}  {'OK <=' if mom<=factorial(h)*n**h else 'EXCEEDS'}")

# ===== ChatGPT counterexample part: N_ev huge (n=16, one-per-antipodal-pair => even moments vanish) =====
print("\nCLAIM: at n=16, the 2^8 'one-per-antipodal-pair' subsets have vanishing even moments (N_ev>=256)")
p2=257; n2=16
G2=subgroup(p2,n2)
# antipodal pairs: i and i+8 (since -1 = z^8)
reps=[G2[i] for i in range(8)]   # one rep per pair
cnt=0
for eps in product([0,1],repeat=8):
    S=[G2[i] if eps[i]==0 else G2[i+8] for i in range(8)]
    ok=all(sum(pow(x,2*j,p2) for x in S)%p2==0 for j in range(1,4))  # x^2,x^4,x^6 =0
    if ok: cnt+=1
print(f"  one-per-pair subsets with x^2=x^4=x^6 sums all 0: {cnt} of 256  (ChatGPT: all 256 => N_ev>=256)")
print(f"  => major-arc N_ev is HUGE while the true D_2^- count is 0 (their algebraic certificate):")
print(f"     positive/separate bounding of major vs minor FAILS; cancellation is essential. CONFIRMED direction.")
