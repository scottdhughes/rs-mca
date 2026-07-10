import numpy as np
from math import log

def prim_root(p):
    phi=p-1; m=phi; f=[]; d=2
    while d*d<=m:
        if m%d==0:
            f.append(d)
            while m%d==0: m//=d
        d+=1
    if m>1: f.append(m)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g

def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    pts=np.empty(n,dtype=np.int64); cur=1
    for k in range(n): pts[k]=cur; cur=cur*z%p
    return pts

def pi2_table(p,n,pts,w):
    grids=np.meshgrid(*[np.arange(p)]*w, indexing='ij')
    C=np.stack([g.ravel() for g in grids],axis=1)
    Mjk=np.array([[pts[(j*k)%n] for k in range(n)] for j in range(1,w+1)],dtype=np.int64)
    ph=(C@Mjk)%p
    z=np.exp(2j*np.pi*ph/p).sum(axis=1)
    return (z.real**2+z.imag**2), C

def Kgrowth(p,n,w,Kmax):
    pts=subgroup(p,n); pi2,C=pi2_table(p,n,pts,w)
    P=p
    def flat(Cc):
        idx=np.zeros(len(Cc),dtype=np.int64)
        for j in range(w): idx=idx*P+Cc[:,j]
        return idx
    nz = flat(C)!=0                    # mask c != 0
    cur=pi2.copy(); nK=float(n)
    out={}
    for K in range(2,Kmax+1):
        cur=cur*pi2[flat((C*K)%P)]
        full=cur.mean()/nK**K
        nzmean=cur[nz].mean()/nK**K
        nzmed=np.median(cur[nz])/nK**K
        out[K]=(full,nzmean,nzmed)
    return out

def fitverdict(Ks,vals):
    Ks=np.array(Ks,float); v=np.array(vals,float)
    good=v>0
    Ks,v=Ks[good],v[good]
    if len(Ks)<4: return "n/a",0,0
    lv=np.log(v)
    a_exp=np.polyfit(Ks,lv,1)[0]; r_exp=abs(np.corrcoef(Ks,lv)[0,1])
    a_poly=np.polyfit(np.log(Ks),lv,1)[0]; r_poly=abs(np.corrcoef(np.log(Ks),lv)[0,1])
    verdict = 'EXP' if r_exp>r_poly+0.02 else 'POLY' if r_poly>r_exp+0.02 else 'AMBIG'
    return verdict,a_exp,a_poly

print("Corrected K-growth: C^{(K)} via full-mean (incl c=0), mean over c!=0, MEDIAN over c!=0.")
print("The route needs the TYPICAL (median, c!=0) coupling to be POLYNOMIAL in K.\n")
n=16
for (p,w) in [(97,2),(193,2),(401,2),(97,3),(193,3)]:
    Kmax=40
    out=Kgrowth(p,n,w,Kmax)
    Ks=sorted(out)
    full=[out[K][0] for K in Ks]; nzm=[out[K][1] for K in Ks]; med=[out[K][2] for K in Ks]
    vf,ae_f,_=fitverdict(Ks,full)
    vn,ae_n,ap_n=fitverdict(Ks,nzm)
    vm,ae_m,ap_m=fitverdict(Ks,med)
    print(f"p={p} w={w}:")
    print(f"   full-mean  C^(5)={out[5][0]:.2f}  C^(20)={out[20][0]:.2e}  C^(40)={out[40][0]:.2e}  -> {vf}")
    print(f"   c!=0 mean  C^(5)={out[5][1]:.2f}  C^(20)={out[20][1]:.2e}  C^(40)={out[40][1]:.2e}  -> {vn}")
    print(f"   c!=0 MED   C^(5)={out[5][2]:.3f}  C^(20)={out[20][2]:.3f}  C^(40)={out[40][2]:.3f}"
          f"  -> {vm} (exp slope {ae_m:+.3f}/K, poly slope {ap_m:+.2f}/logK)")
