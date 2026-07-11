import itertools, cmath, math
from collections import defaultdict, Counter
def prim_root(p):
    x=p-1; f=[]; q=2
    while q*q<=x:
        if x%q==0:
            f.append(q)
            while x%q==0: x//=q
        q+=1
    if x>1: f.append(x)
    return next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in f))
def mu_n(p,n):
    g=prim_root(p); h=pow(g,(p-1)//n,p)
    return [pow(h,k,p) for k in range(n)]
def verify(p,n,w,m):
    H=mu_n(p,n); ninv=pow(n,p-2,p); d=n-w-1
    idx={a:i for i,a in enumerate(H)}
    # --- direct fibers N(v) ---
    direct=defaultdict(int)
    for S in itertools.combinations(H,m):
        v=tuple(sum(pow(a,j,p) for a in S)%p for j in range(1,w+1))
        direct[v]+=1
    # --- Eq 1: interpolation reformulation ---
    # alpha_0 = m/n ; alpha_{n-j} = v_j/n (j=1..w) ; alpha_1..alpha_d free (u)
    # f(a) = sum_r alpha_r a^r.  Count u in F_p^d giving f(a) in {0,1} for all a in H.
    Hpow=[[pow(a,r,p) for r in range(n)] for a in H]   # Hpow[i][r]=a_i^r
    reform=defaultdict(int)
    a0=m*ninv%p
    for v in direct:  # only over achieved syndromes (others give same or 0; check all v too below)
        aJ=[0]*n; aJ[0]=a0
        for j in range(1,w+1): aJ[n-j]=v[j-1]*ninv%p
        cnt=0
        for u in itertools.product(range(p),repeat=d):
            alpha=aJ[:]
            for i in range(1,d+1): alpha[i]=u[i-1]
            ok=all((sum(alpha[r]*Hpow[i][r] for r in range(n))%p) in (0,1) for i in range(n))
            if ok: cnt+=1
        reform[v]=cnt
    eq1=all(direct[v]==reform[v] for v in direct)
    print(f"p={p} n={n} w={w} m={m} d={d}: Eq1 (interpolation reformulation) MATCHES direct N(v)? {eq1}")
    if not eq1:
        for v in list(direct)[:3]: print(f"    v={v}: direct={direct[v]} reform={reform[v]}")
    # --- Eq 2 + Eq 8: G_v(lambda) and sparse annihilation ---
    tp=2j*math.pi/p
    # G_v(lambda) = sum_{u in F_p^d} e_p(u^T A u + l^T u + gamma); lambda: H->F_p
    def Gv(v, lam):  # lam = dict a->lambda_a (nonzero support)
        aJ=[0]*n; aJ[0]=a0
        for j in range(1,w+1): aJ[n-j]=v[j-1]*ninv%p
        tot=0j
        for u in itertools.product(range(p),repeat=d):
            alpha=aJ[:]
            for i in range(1,d+1): alpha[i]=u[i-1]
            s=0
            for a,la in lam.items():
                fa=sum(alpha[r]*pow(a,r,p) for r in range(n))%p
                s=(s+la*(fa*fa-fa))%p
            tot+=cmath.exp(tp*s)
        return tot
    # Eq 8: pick a T with |T|<=d, sum G_v over supp lambda = T, check = p^d
    vpick=next(iter(direct))
    Tsets=[H[:t] for t in [1,2,min(d,3)]]
    print("  Eq 8 (sparse annihilation: sum_{supp lam=T} G_v(lam) = p^d):")
    for T in Tsets:
        t=len(T); acc=0j
        for lamvals in itertools.product(range(1,p),repeat=t):
            acc+=Gv(vpick, dict(zip(T,lamvals)))
        print(f"    |T|={t}: sum={acc.real:.4f}{acc.imag:+.4f}i  vs p^d={p**d}  match={abs(acc-p**d)<1e-6*p**d}")
verify(7,6,1,3)
verify(11,5,1,2)
