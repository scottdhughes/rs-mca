# Verify: every degree-bounded h-syzygy (q_k) also satisfies sum_k q_k s_k = 0,
# where s_k = (Gamma - c_k)/g_k (the realizability identity Gamma = c_k + g_k s_k).
SATS = [
    dict(label="ell=11 p=331", p=331, ell=11, gamma=[97,29,97,239,171,92,143,155,270,1]),
    dict(label="ell=13 p=313", p=313, ell=13, gamma=[254,289,29,276,242,219,201,261,79,232,133,1]),
    dict(label="ell=17 p=103", p=103, ell=17, gamma=[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
]
def fibers(gamma,p,ell):
    F=GF(p); g=F.multiplicative_generator(); n=(p-1)//ell; zeta=g**n; H=[zeta**j for j in range(ell)]
    Rx=PolynomialRing(F,'X'); X=Rx.gen(); Gamma=sum(F(gamma[r-1])*X**r for r in range(1,ell))
    res=[]
    for i in range(n):
        b=g**i; coset=[b*h for h in H]; tally={}
        for x in coset: tally.setdefault(Gamma(x),[]).append(x)
        mu=max(len(v) for v in tally.values())
        if mu<3: continue
        modal=min((val for val,v in tally.items() if len(v)==mu), key=lambda z:int(z))
        fs=set(tally[modal]); cof=[x for x in coset if x not in fs]
        gk=prod((X-x) for x in fs); hk=prod((X-x) for x in cof)
        sk=(Gamma-modal)//gk
        assert (Gamma-modal) == sk*gk, "g_k | Gamma-c_k failed"
        res.append(dict(w=b**ell, mu=mu, ck=modal, gk=gk, hk=hk, sk=sk))
    return res, F, Rx, X, Gamma

for W in SATS:
    fb, F, Rx, X, Gamma = fibers(W["gamma"], W["p"], W["ell"]); ell=W["ell"]
    K=len(fb); mus=[f["mu"] for f in fb]; hks=[f["hk"] for f in fb]; sks=[f["sk"] for f in fb]
    # build h-syzygy module (left-kernel of coeff matrix of h_k X^d in deg<=ell-2)
    rows=[]; blocks=[]
    for k in range(K):
        for d in range(mus[k]-1):
            poly=hks[k]*X**d; rows.append([poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)]); blocks.append((k,d))
    M=Matrix(F,rows); basis=M.left_kernel().basis()
    # for each syzygy, reconstruct q_k and test sum q_k s_k == 0
    allzero=True; degSs=[]
    for v in basis:
        qs=[Rx(0)]*K
        for idx,(k,d) in enumerate(blocks): qs[k]+=v[idx]*X**d
        Ssum=sum(qs[k]*sks[k] for k in range(K))
        if Ssum!=0: allzero=False
        # also confirm it IS an h-syzygy (sanity)
        assert sum(hks[k]*qs[k] for k in range(K))==0
    print("%s: K=%d  #syz=%d  |  sum_k q_k s_k == 0 for ALL h-syzygies: %s"
          % (W["label"], K, len(basis), allzero))
    # is the s-syzygy constraint INDEPENDENT (does adding it cut dimension)? build combined kernel
    rows2=[]
    for k in range(K):
        for d in range(mus[k]-1):
            poly2=sks[k]*X**d
            deg2=ell-2  # s_k X^d has degree <= (ell-1-mu_k)+(mu_k-2)=ell-3
            rows2.append([poly2[j] if j<=poly2.degree() else F(0) for j in range(ell-1)])
    M2=Matrix(F,rows2)
    combined=Matrix(F,[list(r1)+list(r2) for r1,r2 in zip(rows,rows2)])  # stack columns: [h-part | s-part]
    dimH=M.left_kernel().dimension(); dimHS=combined.left_kernel().dimension()
    print("    dim(h-syz)=%d ; dim(h-syz AND s-syz)=%d  -> s-constraint %s"
          % (dimH, dimHS, "REDUNDANT (contained)" if dimH==dimHS else "CUTS to %d"%dimHS))
