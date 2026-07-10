import numpy as np

def prim_root(p):
    phi = p-1
    m = phi; f=[]; d=2
    while d*d<=m:
        if m%d==0:
            f.append(d)
            while m%d==0: m//=d
        d+=1
    if m>1: f.append(m)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g

def setup(p,n):
    assert (p-1)%n==0
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    pts=np.empty(n,dtype=np.int64); cur=1
    for k in range(n):
        pts[k]=cur; cur=cur*z%p
    return z,pts

def stats(p,n,pts,exps,coefs):
    """Return (ratio_to_diagonal, actual_max/sqrt(n), fourthmoment_bound/sqrt(n))."""
    ks=np.arange(n)
    g=np.zeros(n,dtype=np.int64)
    for e,c in zip(exps,coefs):
        g=(g + (c%p)*pts[(e*ks)%n])%p
    W=np.zeros(p,dtype=np.complex128)
    W[pts]=np.exp(2j*np.pi*g/p)
    A=np.fft.fft(W)
    a2=(A.real**2+A.imag**2)
    S4=np.sum(a2**2)              # sum_{c1}|S|^4
    quad=S4/p                     # sum over additive-energy quadruples of g-phase
    ratio=quad/(2.0*n*n)          # vs diagonal 2n^2
    a2[0]=0.0                     # drop c1=0
    mx=np.sqrt(a2.max())
    bnd=(S4)**0.25               # 4th-moment bound on max|S|
    return ratio, mx/np.sqrt(n), bnd/np.sqrt(n), quad

rng=np.random.default_rng(20260706)

for (p,n) in [(12289,2048),(40961,4096)]:
    z,pts=setup(p,n)
    gamma=np.log(n)/np.log(p)
    print(f"\n{'='*70}\np={p}  n={n}  gamma=log n/log p={gamma:.3f}   diagonal 2n^2={2*n*n}")
    print(f"   E_+ (g=0 quad sum) ratio-to-diag = {stats(p,n,pts,[],[])[0]:.1f}")

    # ---- Test A: RESONANT g (factors through d-power map) should BLOW UP ----
    print("  --- TEST A: resonant g = factors through x->x^d (exponents all multiples of d) ---")
    for d in [2,4,8, n//4, n//2]:
        # exponents that are multiples of d (so x^e=(x^d)^{e/d}, image=mu_{n/d})
        mult=[d*t for t in range(1,9) if (d*t)%n!=0][:6]
        if not mult: mult=[d]
        coefs=rng.integers(1,p,size=len(mult))
        r,mx,bnd,q=stats(p,n,pts,mult,coefs)
        tag="  <== BLOW-UP" if r>10 else ("  (mild)" if r>3 else "")
        print(f"    d={d:>5}  |quotient mu_(n/d)|={n//d:>5}  ratio={r:8.1f}  max|S|/sqrt n={mx:6.2f}{tag}")

    # ---- generic g (exponents coprime to n) should COLLAPSE ----
    print("  --- generic g: exponents coprime to n, random coefs (should collapse ~1.5) ---")
    for r_terms in [1,2,4,16,64]:
        # pick r_terms exponents coprime to n
        exps=[]
        e=3
        while len(exps)<r_terms:
            if np.gcd(e,n)==1: exps.append(e)
            e+=2
        coefs=rng.integers(1,p,size=r_terms)
        r,mx,bnd,q=stats(p,n,pts,exps,coefs)
        print(f"    #terms={r_terms:>3}  ratio={r:7.3f}  max|S|/sqrt n={mx:6.2f}  4th-moment bnd/sqrt n={bnd:6.2f}")

    # ---- Test B: coordinate-ascent WORST-CASE over generic exponents ----
    print("  --- TEST B: coordinate-ascent adversary (fixed generic coprime exponents) ---")
    R=8
    exps=[]; e=3
    while len(exps)<R:
        if np.gcd(e,n)==1: exps.append(e)
        e+=2
    best_overall=0.0
    for restart in range(4):
        coefs=rng.integers(1,p,size=R).astype(np.int64)
        cur_r=stats(p,n,pts,exps,coefs)[0]
        for sweep in range(3):
            for j in range(R):
                cand=rng.integers(0,p,size=160)
                bestc=coefs[j]; bestr=cur_r
                for cv in cand:
                    coefs[j]=cv
                    rr=stats(p,n,pts,exps,coefs)[0]
                    if rr>bestr: bestr=rr; bestc=cv
                coefs[j]=bestc; cur_r=bestr
        best_overall=max(best_overall,cur_r)
    r,mx,bnd,q=stats(p,n,pts,exps,coefs)
    print(f"    worst ratio found over 4 restarts x 3 sweeps: {best_overall:7.3f}"
          f"   (max|S|/sqrt n at that g = {mx:.2f}, 4th-moment bnd/sqrt n = {bnd:.2f})")
    print(f"    => adversary on generic exponents stays {'BOUNDED' if best_overall<5 else 'UNBOUNDED'}"
          f" (resonant blow-up above was ratio>>10)")
