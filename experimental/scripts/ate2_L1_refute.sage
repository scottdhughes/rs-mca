# Try to CONSTRUCT an L>1 config: 3 bad slopes with NON-collinear codewords.
# Recipe: triple overlap T (|T|>=10); pick c0,c2 random codewords, and
# c1=(c0+c2+h)/2 with h a deg<k poly vanishing on T (h!=0 => c1 non-collinear).
# Then diff-polys agree on T, so g is consistently defined on the supports.
def run(q,n,k,s):
    set_random_seed(s)
    F=GF(q); pts=[F(i) for i in range(n)]
    C=codes.GeneralizedReedSolomonCode(pts,k); Dec=codes.decoders.GRSBerlekampWelchDecoder(C)
    m=n-k; R3=m//3; A=n-R3-2
    Rr=PolynomialRing(F,'x'); x=Rr.gen()
    # partition D\T into three complements T0,T1,T2 (each size n-A), T = rest
    comp=n-A                      # complement size = R3+2
    idx=list(range(n)); Tset=idx[3*comp:]          # triple overlap = last (n-3comp) points
    T0=idx[0:comp]; T1=idx[comp:2*comp]; T2=idx[2*comp:3*comp]
    Tpts=[pts[i] for i in Tset]
    if len(Tpts) < 1: return None
    # h: vanishes on T, deg<k, nonzero
    hbase=prod([x-t for t in Tpts])
    if hbase.degree()>=k: hbase=Rr(1)  # fallback
    h=hbase*Rr([F.random_element() for _ in range(max(1,k-hbase.degree()))])
    if h==0: h=hbase
    # codewords via random deg<k polys evaluated on D
    p0=Rr([F.random_element() for _ in range(k)]); p2=Rr([F.random_element() for _ in range(k)])
    p1=(p0+p2+h)/2
    c0=[p0(t) for t in pts]; c1=[p1(t) for t in pts]; c2=[p2(t) for t in pts]
    def diffpoly(ca,cb,za,zb):    # = g on S_a ∩ S_b = (ca-cb)/(za-zb) values
        inv=F(za-zb)^(-1); return [ (ca[i]-cb[i])*inv for i in range(n)]
    p01=diffpoly(c0,c1,0,1); p02=diffpoly(c0,c2,0,2); p12=diffpoly(c1,c2,1,2)
    # define g on D: T-> p01 ; T2 (in S0∩S1) -> p01 ; T0 (in S1∩S2)-> p12 ; T1 (in S0∩S2)-> p02
    g=[F(0)]*n
    for i in Tset+T2: g[i]=p01[i]
    for i in T0: g[i]=p12[i]
    for i in T1: g[i]=p02[i]
    # f = c0 on S0 (= all but T0); on T0 use S1: c1 - g
    f=[F(0)]*n
    for i in range(n):
        if i in T0: f[i]=c1[i]-g[i]
        else: f[i]=c0[i]
    # now decode slopes 0,1,2 and check badness + collinearity
    Rr2=PolynomialRing(F,'x')
    def extends(vals,xs): return Rr2.lagrange_polynomial(list(zip(xs,vals))).degree()<k
    bad=[]; cws=[]
    for zz in [0,1,2]:
        z=F(zz); w=vector(F,[f[i]+z*g[i] for i in range(n)])
        try: cw=Dec.decode_to_code(w)
        except Exception: 
            print("  z=%d decode FAILED"%zz); continue
        S=[i for i in range(n) if w[i]==cw[i]]
        ext=extends([g[i] for i in S],[pts[i] for i in S]) if len(S)>=A else True
        if len(S)>=A and not ext: bad.append(zz); cws.append(cw)
        print("  z=%d: agreement=%d (A=%d) g-extends?=%s bad=%s"%(zz,len(S),A,ext,(len(S)>=A and not ext)))
    if len(cws)>=2:
        M=Matrix(F,[list(c-cws[0]) for c in cws[1:]]); rk=M.rank()
        print("  bad slopes=%s  codeword rank=%d  => L>1 (L1 FALSE)? %s"%(bad,rk,rk>=2))
    else:
        print("  <2 bad slopes; inconclusive")
for (q,n,k),s in [((31,31,15),1),((31,31,15),2),((37,31,10),3),((41,40,20),4)]:
    print("q=%d n=%d k=%d seed=%d:"%(q,n,k,s)); run(q,n,k,s)
