import itertools, cmath, math
from collections import defaultdict
def prim_root(p):
    x=p-1;f=[];q=2
    while q*q<=x:
        if x%q==0:
            f.append(q)
            while x%q==0:x//=q
        q+=1
    if x>1:f.append(x)
    return next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in f))
def mu_n(p,n):
    g=prim_root(p);h=pow(g,(p-1)//n,p);return [pow(h,k,p) for k in range(n)]
def detmod(M,p):
    A=[row[:] for row in M];N=len(A);det=1
    for c in range(N):
        piv=next((i for i in range(c,N) if A[i][c]%p),None)
        if piv is None: return 0
        if piv!=c: A[c],A[piv]=A[piv],A[c]; det=-det
        det=(det*A[c][c])%p; inv=pow(A[c][c],p-2,p)
        for i in range(c+1,N):
            f=(A[i][c]*inv)%p
            if f: A[i]=[(A[i][k]-f*A[c][k])%p for k in range(N)]
    return det%p
def leg(a,p): 
    a%=p; 
    return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)
def verify(p,n,w,m):
    H=mu_n(p,n); ninv=pow(n,p-2,p); d=n-w-1; c=w+1; tp=2j*math.pi/p
    a0=m*ninv%p
    # pick a FULL-SUPPORT full-rank lambda (all lam_a != 0)
    import random; random.seed(1)
    v=tuple([0]*w)  # syndrome 0
    aJ=[0]*n; aJ[0]=a0
    for j in range(1,w+1): aJ[n-j]=v[j-1]*ninv%p
    # g_v(a): the fixed interpolation poly
    def gval(a): return sum(aJ[r]*pow(a,r,p) for r in range(n))%p
    checks=0; okG=True; okdual=True
    for trial in range(6):
        lam={a: random.randrange(1,p) for a in H}   # full support
        A=[[sum(lam[a]*pow(a,i+j,p) for a in H)%p for j in range(1,d+1)] for i in range(1,d+1)]
        detA=detmod(A,p)
        if detA==0: continue
        checks+=1
        # G_v(lambda) exact by brute sum over u in F_p^d
        Gv=0j
        for u in itertools.product(range(p),repeat=d):
            alpha=aJ[:]
            for i in range(1,d+1): alpha[i]=u[i-1]
            s=0
            for a in H:
                fa=sum(alpha[r]*pow(a,r,p) for r in range(n))%p
                s=(s+lam[a]*(fa*fa-fa))%p
            Gv+=cmath.exp(tp*s)
        # (1) |G_v| = p^{d/2} ?
        modG=abs(Gv); okG &= abs(modG-p**(d/2))<1e-6*p**(d/2)
        # (2) Hankel duality: B_{uv}=(1/n^2) sum_a lam_a^{-1} a^{u+v}, u,v=0..w ; chi(detA)chi(detB)=chi(prod lam)?
        laminv={a:pow(lam[a],p-2,p) for a in H}
        B=[[ (pow(ninv,2,p)*sum(laminv[a]*pow(a,u+vv,p) for a in H))%p for vv in range(c)] for u in range(c)]
        detB=detmod(B,p)
        prodlam=1
        for a in H: prodlam=(prodlam*lam[a])%p
        lhs=leg(detA,p)*leg(detB,p); rhs=leg(prodlam,p)
        okdual &= (lhs==rhs)
        if trial<2:
            print(f"  trial {trial}: |G_v|={modG:.3f} (p^(d/2)={p**(d/2):.3f}); detA={detA} detB={detB} prodlam={prodlam}")
            print(f"           chi(detA)chi(detB)={lhs}  chi(prod lam)={rhs}  DUALITY {'OK' if lhs==rhs else 'FAIL'}")
    print(f"p={p} n={n} w={w} m={m} d={d} c={c}: full-rank Gauss |G|=p^(d/2) OK? {okG};  Hankel duality (Eq27) OK? {okdual}  ({checks} full-rank trials)")
verify(7,6,1,3)
verify(11,5,1,2)
verify(13,6,2,3)
