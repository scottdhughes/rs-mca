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

# w=3: exponents 1,2,3; odd={1,3}, even={2}. fiber map S -> (p1,p2,p3).
p,n,m=73,24,12
G=subgroup(p,n); G2=[(h*h)%p for h in G]; G3=[(h*h*h)%p for h in G]
# nu(v) over F_p^3 via DP, v=(p1,p2,p3)
D=[np.zeros((p,p,p),dtype=np.float64) for _ in range(m+1)]
D[0][0,0,0]=1.0
for h,h2,h3 in zip(G,G2,G3):
    for k in range(m,0,-1):
        D[k]+=np.roll(np.roll(np.roll(D[k-1],h,0),h2,1),h3,2)
nu=D[m]
mu=comb(n,m)/p**3
N=nu[0,0,0]
# g(p1,p3) = nu(p1, 0, p3): fiber with even moment p2=0
g=nu[:,0,:]   # shape (p,p), indexed (p1,p3)
# incidence over (a,a') in mu_n^2: target t=(2(a+a')%p, 2(a^3+a'^3)%p)
I=0.0; I_anti=0.0; I_gen=0.0; n_anti=0; n_gen=0; gen_vals=[]
minus={ (p - x)%p : True for x in G }  # -a set membership by value
Gval=G
neg_idx={}
for i,a in enumerate(G):
    for j in range(n):
        if (Gval[i]+Gval[j])%p==0: neg_idx[i]=j  # a' = -a
for i in range(n):
    for j in range(n):
        t1=(2*(G[i]+G[j]))%p; t3=(2*(G3[i]+G3[j]))%p
        val=g[t1,t3]
        I+=val
        if neg_idx.get(i)==j:   # antipodal a'=-a
            I_anti+=val; n_anti+=1
        else:
            I_gen+=val; n_gen+=1; gen_vals.append(val)
gen=np.array(gen_vals)
print(f"n={n},p={p},m={m},w=3  gamma={log(n)/log(p):.3f}")
print(f"  mu (mean fiber) = {mu:.4f}   N=g(0,0)=nu(0,0,0) = {N:.0f}   N/mu={N/mu:.2f}")
print(f"  incidence I = sum_(a,a') g(t) = {I:.1f}")
print(f"   antipodal (a'=-a): {n_anti} pairs -> all target t=(0,0), contrib {I_anti:.1f}  (= n_anti * N = {n_anti*N:.0f})")
print(f"   generic ({n_gen} pairs): contrib {I_gen:.1f}, mean g/mu = {gen.mean()/mu:.3f}, max g/mu = {gen.max()/mu:.2f}")
print(f"  => antipodal share of I = {I_anti/I*100:.1f}%   generic mean-fiber ~ mu? ratio {gen.mean()/mu:.3f}")
# how many generic targets are RESONANT (g >> mu)?  (the residual PTE directions beyond antipodal)
res = (gen > 5*mu).sum()
print(f"  generic targets with g>5*mu (residual resonances): {res} of {n_gen}  (their total: {gen[gen>5*mu].sum():.1f})")
