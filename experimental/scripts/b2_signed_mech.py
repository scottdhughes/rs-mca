import cmath, math, itertools
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
def esym(vals,d):
    e=[0j]*(d+1);e[0]=1+0j
    for x in vals:
        for k in range(d,0,-1): e[k]+=x*e[k-1]
    return e[d]
def brute_N0(S,p,w,m):
    # exact: count m-subsets of S with all power sums p_1..p_w == 0 mod p
    n=len(S); cnt=0
    for comb_idx in itertools.combinations(range(n),m):
        ok=True
        for j in range(1,w+1):
            s=0
            for i in comb_idx: s=(s+pow(S[i],j,p))%p
            if s!=0: ok=False;break
        if ok: cnt+=1
    return cnt
def analyze(p,n,w,m):
    S=mu_n(p,n); tp=2j*math.pi/p
    def Nhat(c):
        vals=[]
        for a in S:
            s=0;ap=a
            for j in range(w): s=(s+c[j]*ap)%p; ap=ap*a%p
            vals.append(cmath.exp(tp*s))
        return esym(vals,m)
    signed_all=0j; prim_s=0j; imp_s=0j; prim_abs=0.0; imp_abs=0.0
    freqs=[]
    for c in itertools.product(range(p),repeat=w):
        if all(x==0 for x in c): 
            main=Nhat(c); continue
        v=Nhat(c); signed_all+=v
        imprimitive=all(c[i]==0 for i in range(w) if (i+1)%2==1)
        if imprimitive: imp_s+=v; imp_abs+=abs(v)
        else: prim_s+=v; prim_abs+=abs(v)
        freqs.append((abs(v),v,imprimitive,c))
    mu=comb(n,m)/p**w
    N0_fourier=(main.real+signed_all.real)/p**w
    N0_true=brute_N0(S,p,w,m)
    print(f"  p={p} n={n} w={w} m={m}:  mu=C(n,m)/p^w={mu:.4f}")
    print(f"    N0 (brute)   = {N0_true}")
    print(f"    N0 (fourier) = {N0_fourier:.4f}   [main=C(n,m)={comb(n,m)}]  MATCH={abs(N0_fourier-N0_true)<1e-4}")
    print(f"    signed  Sum_{{xi!=0}} Nhat = {signed_all.real:+.3f} (=p^w*(N0-mu)={p**w*(N0_true-mu):+.3f})")
    tot_abs=prim_abs+imp_abs
    print(f"    UNSIGNED Sum|Nhat|  = {tot_abs:.1f}   (prim {prim_abs:.1f} / imprim {imp_abs:.1f})")
    print(f"    cancellation factor |signed|/unsigned = {abs(signed_all)/tot_abs:.3e}")
    print(f"    SIGNED by class: primitive={prim_s.real:+.3f}  imprimitive={imp_s.real:+.3f}")
    print(f"    *** PRIMITIVE SIGNED SUM == 0 ?  {abs(prim_s)<1e-6}   (|prim_s|={abs(prim_s):.2e}) ***")
    print(f"      prim   cancel |sum|/abs = {abs(prim_s)/prim_abs if prim_abs>0 else 0:.3e}")
    print(f"      imprim cancel |sum|/abs = {abs(imp_s)/imp_abs if imp_abs>0 else 0:.3e}")
    # top-magnitude frequencies: do the biggest |Nhat| cancel among themselves?
    freqs.sort(key=lambda t: t[0], reverse=True)
    for K in [10, 50, len(freqs)]:
        topsum=sum(f[1] for f in freqs[:K]); topabs=sum(f[0] for f in freqs[:K])
        print(f"      top-{K:>4} |Nhat|: signed={topsum.real:+.2f}  unsigned={topabs:.1f}  cancel={abs(topsum)/topabs:.2e}")
    print()

print("SIGNED MECHANISM PROBE: is cancellation structured (resonant) or generic?")
analyze(17,8,2,3)
analyze(17,16,2,6)
analyze(97,16,2,6)
analyze(97,16,3,6)
