import itertools, cmath, math
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
def gcoef(p,n,w,m,v):
    ninv=pow(n,p-2,p); a=[0]*n; a[0]=m*ninv%p
    for j in range(1,w+1): a[n-j]=v[j-1]*ninv%p
    return a  # alpha_r
def gval(alpha,a,p,n): return sum(alpha[r]*pow(a,r,p) for r in range(n))%p

# --- Part 1: brute-force verify Eq 30 (tau*Sigma_v = p^n N - p^{n-1} R) at (5,4,2,3) ---
def N_direct(p,n,w,m,v):  # # m-subsets with syndrome v
    H=mu_n(p,n); c=0
    for S in itertools.combinations(H,m):
        if all(sum(pow(a,j,p) for a in S)%p==v[j-1] for j in range(1,w+1)): c+=1
    return c
def R_direct(p,n,w,m,v):  # #{(s,t): g^2-g + s a^2 + t(2g-1)a = 0 for all a}
    H=mu_n(p,n); al=gcoef(p,n,w,m,v); cnt=0
    for s in range(p):
        for t in range(p):
            if all((gval(al,a,p,n)**2-gval(al,a,p,n)+s*a*a+t*(2*gval(al,a,p,n)-1)*a)%p==0 for a in H): cnt+=1
    return cnt
def Sigma_bruteforce(p,n,w,m,v):  # sum_{A_lam != 0} G_v(lam), G_v(lam)=sum_u e_p(sum_a lam_a(f_u(a)^2-f_u(a)))
    # d=1 so f_u = g_v + u X ; A_lam = sum_a lam_a a^2
    H=mu_n(p,n); al=gcoef(p,n,w,m,v); tp=2j*math.pi/p
    tot=0j
    # precompute f_u(a) for all u,a
    for lam in itertools.product(range(p),repeat=n):
        A=sum(lam[i]*pow(H[i],2,p) for i in range(n))%p
        if A==0: continue
        G=0j
        for u in range(p):
            s=0
            for i,a in enumerate(H):
                fu=(gval(al,a,p,n)+u*a)%p
                s=(s+lam[i]*(fu*fu-fu))%p
            G+=cmath.exp(tp*s)
        tot+=G
    return tot
p,n,w,m=5,4,2,3
H=mu_n(p,n); print(f"(5,4,2,3): mu_n={H}")
# pick v_S = syndrome of mu_n minus one element (b=H[1]); v_0=0
b=H[1]; vS=tuple((-pow(b,j,p))%p for j in range(1,w+1)); v0=tuple([0]*w)
tau=sum(cmath.exp(2j*math.pi*(z*z)/p) for z in range(p))
for tag,v in [("vS",vS),("v0",v0)]:
    N=N_direct(p,n,w,m,v); R=R_direct(p,n,w,m,v)
    Sig=Sigma_bruteforce(p,n,w,m,v)
    lhs=tau*Sig; rhs=p**n*N - p**(n-1)*R
    print(f"  {tag}={v}: N={N} R={R} | tau*Sigma(brute)={lhs.real:.2f}{lhs.imag:+.2f}i  vs p^n N - p^(n-1) R={rhs}  Eq30_MATCH={abs(lhs-rhs)<1e-4*max(1,abs(rhs))}")

# --- Part 2: independent N,R at (17,8,6,7) ---
p,n,w,m=17,8,6,7
H=mu_n(p,n); print(f"\n(17,8,6,7): mu_n={H}")
b=2; vS=tuple((-pow(b,j,p))%p for j in range(1,w+1)); v0=tuple([0]*w)
print(f"  v_S (remove {b}) = {vS}")
for tag,v in [("vS",vS),("v0",v0)]:
    N=N_direct(p,n,w,m,v); R=R_direct(p,n,w,m,v)
    print(f"  {tag}: N(v)={N} (claim 1/0), R(v)={R} (claim 1/0)")
NS,RS=N_direct(p,n,w,m,vS),R_direct(p,n,w,m,vS)
N0,R0=N_direct(p,n,w,m,v0),R_direct(p,n,w,m,v0)
diff=abs(p**n*(NS-N0) - p**(n-1)*(RS-R0))
eq29=p**(n+2-(w+1)/2)
print(f"  => |T_1(vS)-T_1(v0)| = |p^n(NS-N0)-p^(n-1)(RS-R0)| = {diff} = (p-1)p^(n-1)? {diff==(p-1)*p**(n-1)}")
print(f"     Eq29 bound p^(n+2-c/2) = {eq29:.1f};  ratio diff/(2*Eq29) = {diff/(2*eq29):.2f}  => Eq29 VIOLATED if >1: {diff/(2*eq29)>1}")
