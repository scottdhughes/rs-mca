# Dissect the pivot/free structure of the h_k X^d columns: which (k,d) are the E_3 pivots
# (independent) vs the K "free" (dependent -> syzygy-generating), and the pattern.
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
        res.append((mu, prod((X-x) for x in cof)))
    return res, F, Rx, X

def pivot_structure(fb, F, Rx, X, ell, order):
    # columns c=(k,d), vector = coeffs of h_k X^d in deg<=ell-2; order them; find pivot cols via echelon.
    cols=[]; tag=[]
    for k,(mu,hk) in enumerate(fb):
        for d in range(mu-1): cols.append((k,d))
    cols.sort(key=order)
    vecs=[]
    for (k,d) in cols:
        mu,hk=fb[k]; poly=hk*X**d
        vecs.append([poly[j] if j<=poly.degree() else F(0) for j in range(ell-1)])
    M=Matrix(F, vecs)              # (#cols) x (ell-1); rows are the column-vectors
    # greedy independent set in the given order = pivots
    piv=[]; cur=Matrix(F,0,ell-1)
    for i in range(M.nrows()):
        test=cur.stack(M[i])
        if test.rank()>cur.rank(): piv.append(i); cur=test
    pivset=set(piv); free=[i for i in range(len(cols)) if i not in pivset]
    return cols, pivset, free

for W in SATS:
    fb,F,Rx,X=fibers(W["gamma"],W["p"],W["ell"]); ell=W["ell"]
    mus=[mu for (mu,h) in fb]; K=len(fb); E3=sum(mu-2 for (mu,h) in fb)
    # order: largest fiber first, then by degree d ascending
    order=lambda kd,mus=mus: (-mus[kd[0]], kd[1])
    cols,piv,free=pivot_structure(fb,F,Rx,X,ell,order)
    print("%s: K=%d E3=%d mus(sorted desc)=%s   #pivots=%d (=E3?) #free=%d (=K?)"
          % (W["label"],K,E3,sorted(mus,reverse=True),len(piv),len(free)))
    # per-fiber: how many of fiber k's (mu_k-1) columns are FREE?
    from collections import Counter
    freecnt=Counter(cols[i][0] for i in free)
    print("   FREE columns (the K syzygy directions), as (fiber k has mu_k, #its columns that are free):")
    for k in sorted(range(K), key=lambda k:-mus[k]):
        print("      fiber %d (mu=%d, cols=%d): %d free  %s"
              % (k, mus[k], mus[k]-1, freecnt.get(k,0),
                 "<- ALL free" if freecnt.get(k,0)==mus[k]-1 else ""))
