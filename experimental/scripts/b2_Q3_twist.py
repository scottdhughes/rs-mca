import numpy as np, math
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
def fibers_w(p,n,w,m):
    S=mu_n(p,n)
    shape=(m+1,)+(p,)*w
    D=np.zeros(shape); D[(0,)+(0,)*w]=1.0
    for a in S:
        shifts=[pow(a,j,p) for j in range(1,w+1)]
        sh=D[:m]
        for ax,s in enumerate(shifts): sh=np.roll(sh,s,axis=ax+1)
        D[1:]+=sh
    return D[m]   # N_w(z), shape (p,)*w
def stab_size(z, n):
    # twist stabilizer: {zeta in mu_n : zeta^j = 1 for all j with z_j != 0}
    active=[j+1 for j,zj in enumerate(z) if zj!=0]     # 1-indexed exponents
    if not active: return n
    g=0
    for j in active: g=math.gcd(g,j)
    g=math.gcd(g,n)
    return math.gcd(g,n)  # #{zeta: zeta^{gcd(active)}=1 within mu_n} = gcd(gcd(active),n)
def analyze(p,n,w,m):
    N=fibers_w(p,n,w,m); mean=comb(n,m)/p**w
    flat=N.ravel(); idx=np.argsort(flat)[::-1]
    # classify each z by stabilizer; primitive = stab size 1 (trivial), imprimitive = stab>1
    prim_max=0; imp_max=0
    prim_vals=[]; imp_vals=[]
    P=p
    def unravel(i):
        z=[]; 
        for _ in range(w): z.append(i%P); i//=P
        return tuple(reversed(z))
    for i in range(len(flat)):
        z=unravel(i); ss=stab_size(z,n); v=flat[i]
        if ss==1: prim_vals.append(v)
        else: imp_vals.append(v)
    prim_vals=np.array(prim_vals); imp_vals=np.array(imp_vals)
    print(f"p={p} n={n} w={w} m={m}: mean fiber = {mean:.3f}, C(n,m)={comb(n,m)}")
    print(f"  #primitive z (trivial stab) = {len(prim_vals)}, #imprimitive z (stab>1) = {len(imp_vals)}")
    print(f"  MAX N_w over PRIMITIVE z   = {prim_vals.max():.0f}  ({prim_vals.max()/mean:.2f} x mean)")
    print(f"  MAX N_w over IMPRIMITIVE z = {imp_vals.max():.0f}  ({imp_vals.max()/mean:.2f} x mean)")
    # top-10 fibers: their stabilizer sizes
    print("  top-8 fibers: (N_w, stab_size, primitive?)")
    for i in idx[:8]:
        z=unravel(i); ss=stab_size(z,n)
        print(f"    N={flat[i]:.0f}  stab={ss}  {'PRIM' if ss==1 else 'imprim'}  z={z}")
    print(f"  => Q3 predicts heavy fibers are imprimitive (stab>1); primitive fibers light.\n")
analyze(17,16,2,6)
analyze(97,16,2,6)
analyze(97,16,3,6)
