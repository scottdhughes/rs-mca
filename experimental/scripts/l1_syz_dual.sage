# Dual formulation: annihilator A = {m in F_p[X]_{<=ell-2} : <h_k X^d, m>=0 for d=0..mu_k-2 all k}.
# Verify dim A = ell-1-E_3 (=1 at saturators) and A = <rev(Gamma)>; and that rev(Gamma) satisfies
# the top-window gap [ell+1-mu_k, ell-1] of h_k*Gamma via the realizability identity.
SATS = [
    dict(label="ell=11 p=331", p=331, ell=11, gamma=[97,29,97,239,171,92,143,155,270,1]),
    dict(label="ell=13 p=313", p=313, ell=13, gamma=[254,289,29,276,242,219,201,261,79,232,133,1]),
    dict(label="ell=17 p=103", p=103, ell=17, gamma=[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
]
def setup(gamma,p,ell):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen(); Gamma=sum(F(gamma[r-1])*X**r for r in range(1,ell))
    fb=[]
    for i in range(n):
        b=g**i; coset=[b*h for h in H]; tally={}
        for x in coset: tally.setdefault(Gamma(x),[]).append(x)
        mu=max(len(v) for v in tally.values())
        if mu<3: continue
        modal=min((val for val,v in tally.items() if len(v)==mu), key=lambda z:int(z))
        cof=[x for x in coset if x not in set(tally[modal])]
        fb.append((mu, prod((X-x) for x in cof)))
    return F,Rx,X,Gamma,fb
for W in SATS:
    F,Rx,X,Gamma,fb=setup(W["gamma"],W["p"],W["ell"]); ell=W["ell"]
    E3=sum(mu-2 for (mu,h) in fb); K=len(fb)
    # annihilator: m=(m_0..m_{ell-2}); condition <h_k X^d,m>=[X^{ell-1-d}](h_k*m*) ... build directly:
    # <h_k X^d, m> = sum_j (h_k X^d)_j m_j.  rows = h_k X^d vectors; A = right-kernel of that matrix.
    rows=[]
    for (mu,hk) in fb:
        for d in range(mu-1):
            poly=hk*X**d; rows.append([poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)])
    M=Matrix(F,rows); ann=M.right_kernel()
    # rev(Gamma) truncated: m_i = Gamma_{ell-1-i}, i=0..ell-2
    gv=[Gamma[j] for j in range(ell)]  # Gamma coeffs deg 0..ell-1
    revG=vector(F,[gv[ell-1-i] for i in range(ell-1)])
    in_ann = revG in ann
    isspan = (ann.dimension()==1 and ann.basis()[0].is_zero()==False and revG!=0 and (ann==(F**(ell-1)).subspace([revG])))
    print("%s: E3=%d K=%d | dim annihilator=%d (expect ell-1-E3=%d) | rev(Gamma) in ann: %s | ann==<revG>: %s"
          % (W["label"],E3,K,ann.dimension(),ell-1-E3,in_ann,isspan))
