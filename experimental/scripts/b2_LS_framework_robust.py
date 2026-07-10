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

def root_framework(p,n,m):
    G=subgroup(p,n); G3=[pow(h,3,p) for h in G]; G2=[pow(h,2,p) for h in G]
    D=[np.zeros((p,p,p),dtype=np.float64) for _ in range(m+1)]
    D[0][0,0,0]=1.0
    for h,h2,h3 in zip(G,G2,G3):
        for k in range(m,0,-1):
            D[k]+=np.roll(np.roll(np.roll(D[k-1],h,0),h2,1),h3,2)
    nu=D[m]; mu=comb(n,m)/p**3; N=nu[0,0,0]; g=nu[:,0,:]
    neg={}
    for i in range(n):
        for j in range(n):
            if (G[i]+G[j])%p==0: neg[i]=j
    I_anti=0.0; gen=[]
    for i in range(n):
        for j in range(n):
            val=g[(2*(G[i]+G[j]))%p, (2*(G3[i]+G3[j]))%p]
            if neg.get(i)==j: I_anti+=val
            else: gen.append(val)
    gen=np.array(gen)
    return dict(mu=mu,N=N,Nmu=N/mu,anti_share=I_anti/(I_anti+gen.sum()),
               gen_mean=gen.mean()/mu, gen_max=gen.max()/mu, gen_res=(gen>5*mu).sum(),
               gamma=log(n)/log(p))

print("Root-framework regime-robustness (w=3). q=4>w=3, m div by 4 => dyadic BLOCK structure present.")
print(f"{'n':>3} {'p':>4} {'m':>3} {'gamma':>6} {'mu':>9} {'N/mu':>6} | {'anti%':>6} {'gen_mean/mu':>11} {'gen_max/mu':>10} {'gen>5mu':>8}")
print("-"*90)
for (n,p,m) in [(24,73,12),(24,97,12),(24,193,12),(32,97,16),(16,193,8)]:
    if (p-1)%n: continue
    r=root_framework(p,n,m)
    print(f"{n:>3} {p:>4} {m:>3} {r['gamma']:>6.3f} {r['mu']:>9.3f} {r['Nmu']:>6.2f} | "
          f"{r['anti_share']*100:>5.1f}% {r['gen_mean']:>11.3f} {r['gen_max']:>10.2f} {r['gen_res']:>8}")
print("\nKEY: if 'gen_max/mu' stays O(1) and 'gen>5mu'=0 across mu (incl small-mu block regime),")
print("the resonance is ALWAYS confined to the antipodal locus => framework is regime-robust.")
