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

def analyze(p,n,m,w=3,do_coupling=False):
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
    # nu-hat = e_m (signed Newton)
    e=[np.ones(len(tau),dtype=complex)]+[np.zeros(len(tau),dtype=complex) for _ in range(m)]
    for k in range(1,m+1):
        acc=np.zeros(len(tau),dtype=complex)
        for i in range(1,k+1): acc+=((-1)**(i-1))*e[k-i]*pr[i-1]
        e[k]=acc/k
    nuhat=e[m]
    K=(tau.real**2+tau.imag**2)-n
    mask=flat(C)!=0; mu=comb(n,m)/p**w; n2mu=n*n*mu
    Corr=(nuhat[mask]*K[mask]).sum().real/p**w
    Tri =(np.abs(nuhat[mask])*np.abs(K[mask])).sum()/p**w
    out=dict(theta=log(mu)/log(n), mu=mu, corr=Corr/n2mu, tri=Tri/n2mu, cancel=Tri/abs(Corr))
    if do_coupling:
        # provable coupling bound B_c = e_m with p_r -> |p_r| (positive Newton) >= |nuhat|
        ab=[np.abs(x) for x in pr]
        b=[np.ones(len(tau))]+[np.zeros(len(tau)) for _ in range(m)]
        for k in range(1,m+1):
            acc=np.zeros(len(tau))
            for i in range(1,k+1): acc+=b[k-i]*ab[i-1]/1.0
            b[k]=acc/k
        B=b[m]
        Btri=(B[mask]*np.abs(K[mask])).sum()/p**w
        out['coupling_tri']=Btri/n2mu
        out['coupling_loss']=Btri/max((np.abs(nuhat[mask])*np.abs(K[mask])).sum()/p**w,1e-30)
    return out

print("Coupling+triangle path validation. Tri = Sum|nuhat||K| / (n^2 mu)  (want bounded, esp large theta).")
print(f"{'n':>3} {'p':>4} {'m':>3} {'theta':>6} {'Corr/n2mu':>10} {'Tri/n2mu':>9} {'cancel':>7}")
for (n,p,m) in [(16,97,8),(24,193,12),(24,97,12),(24,73,12),(32,193,16)]:
    r=analyze(p,n,m)
    print(f"{n:>3} {p:>4} {m:>3} {r['theta']:>6.2f} {r['corr']:>10.4f} {r['tri']:>9.4f} {r['cancel']:>7.2f}")
print("\ndeployment proxy n=32,p=97,theta~1.87 WITH provable coupling bound B_c=[t^m]exp(sum|tau(rc)|t^r/r):")
r=analyze(97,32,16,do_coupling=True)
print(f"  theta={r['theta']:.2f}  Tri(|nuhat|)/n2mu={r['tri']:.4f}  coupling-Tri(B_c)/n2mu={r['coupling_tri']:.4f}  coupling loss factor={r['coupling_loss']:.2f}")
print("  => if coupling-Tri stays O(1)*n2mu, the provable coupling bound CLOSES SV* (no signed cancellation needed).")
