import itertools
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
def rankmod(M,p):
    A=[row[:] for row in M];R=len(A);C=len(A[0]) if A else 0;r=0
    for c in range(C):
        piv=next((i for i in range(r,R) if A[i][c]%p),None)
        if piv is None:continue
        A[r],A[piv]=A[piv],A[r]
        inv=pow(A[r][c],p-2,p);A[r]=[(x*inv)%p for x in A[r]]
        for i in range(R):
            if i!=r and A[i][c]%p:
                fq=A[i][c];A[i]=[(A[i][k]-fq*A[r][k])%p for k in range(C)]
        r+=1
    return r
for (p,n,w) in [(7,6,1),(13,6,2),(11,5,1)]:
    d=n-w-1;H=mu_n(p,n);ok=True;ch=0
    for t in range(1,d+1):
        for T in itertools.combinations(H,t):
            lam={a:1 for a in T}
            A=[[sum(lam.get(a,0)*pow(a,i+j,p) for a in H)%p for j in range(1,d+1)] for i in range(1,d+1)]
            if rankmod(A,p)!=t: ok=False
            ch+=1
    print(f"  p={p} n={n} w={w} d={d}: rank(A_lambda)=|supp| for all |supp|<=d ? {ok}  ({ch} checked)")
