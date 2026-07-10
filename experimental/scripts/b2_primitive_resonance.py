import numpy as np

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

def build(p,n,w,pts):
    grids=np.meshgrid(*[np.arange(p)]*w, indexing='ij')
    C=np.stack([g.ravel() for g in grids],axis=1)   # (p^w, w), col j-1 = c_j
    Mjk=np.array([[pts[(j*k)%n] for k in range(n)] for j in range(1,w+1)],dtype=np.int64)
    ph=(C@Mjk)%p
    z=np.exp(2j*np.pi*ph/p).sum(axis=1)
    return (z.real**2+z.imag**2), C

def fitverdict(Ks,v):
    Ks=np.array(Ks,float); v=np.array(v,float); good=v>0
    Ks,v=Ks[good],v[good]
    if len(Ks)<4: return "n/a"
    lv=np.log(v)
    re=abs(np.corrcoef(Ks,lv)[0,1]); ae=np.polyfit(Ks,lv,1)[0]
    rp=abs(np.corrcoef(np.log(Ks),lv)[0,1])
    return f"{'EXP' if re>rp+0.02 else 'POLY' if rp>re+0.02 else 'AMBIG'}(slope {ae:+.3f}/K)"

n=16; w=3; Kmax=40
for p in [97,193]:
    pts=subgroup(p,n); pi2,C=build(p,n,w,pts)
    P=p
    def flat(Cc):
        idx=np.zeros(len(Cc),dtype=np.int64)
        for j in range(w): idx=idx*P+Cc[:,j]
        return idx
    fl=flat(C)
    prim = (C[:,1]==0) & (fl!=0)          # c_2=0, c!=0  (odd-freq support j=1,3)
    struct=(C[:,0]==0)&(C[:,2]==0)&(fl!=0) # c_1=c_3=0, c!=0 (even-freq j=2 only)
    allnz = fl!=0
    print(f"\n### p={p}, w={w}, n={n}:  #prim={prim.sum()} #struct={struct.sum()} #all!=0={allnz.sum()} ###")
    cur=pi2.copy()
    rec={'prim_mean':[],'prim_med':[],'struct_mean':[],'all_mean':[]}
    Ks=list(range(2,Kmax+1))
    for K in Ks:
        cur=cur*pi2[flat((C*K)%P)]
        rec['prim_mean'].append(cur[prim].mean())
        rec['prim_med'].append(np.median(cur[prim]))
        rec['struct_mean'].append(cur[struct].mean())
        rec['all_mean'].append(cur[allnz].mean())
    def at(key,K): return rec[key][K-2]
    print(f"  {'K':>3} | {'PRIM mean':>12} {'PRIM med':>12} | {'STRUCT mean':>13} | {'all!=0 mean':>13}")
    for K in [2,5,10,20,30,40]:
        print(f"  {K:>3} | {at('prim_mean',K):>12.3e} {at('prim_med',K):>12.3e} | "
              f"{at('struct_mean',K):>13.3e} | {at('all_mean',K):>13.3e}")
    print(f"  growth verdicts:  PRIM mean={fitverdict(Ks,rec['prim_mean'])}   "
          f"PRIM med={fitverdict(Ks,rec['prim_med'])}   STRUCT mean={fitverdict(Ks,rec['struct_mean'])}")
    print(f"  KEY: if PRIM stays POLY/bounded while STRUCT is EXP => descent peels the resonances => E-b closes on primitive part.")
