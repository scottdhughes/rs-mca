# Non-degenerate L=1 cross-check: plant a genuine nonzero code-line (a,b) drawn
# from the code, add the a425 residual, confirm bad=R3+3 and codewords rank<=1.
def run(q,n,k,s):
    set_random_seed(s)
    F=GF(q); pts=[F(i) for i in range(n)]
    C=codes.GeneralizedReedSolomonCode(pts,k); Dec=codes.decoders.GRSBerlekampWelchDecoder(C)
    m=n-k; R3=m//3; A=n-R3-2; core=A-1
    Rr=PolynomialRing(F,'x')
    def extends(vals,xs):
        return Rr.lagrange_polynomial(list(zip(xs,vals))).degree()<k
    av=C.random_element(); bv=C.random_element()       # two random codewords = the code-line
    f=[av[i] for i in range(n)]; g=[bv[i] for i in range(n)]
    for idx in range(core,n):                           # a425 residual on outside coords
        lam=F((idx-core)%q); g[idx]=bv[idx]+F(1); f[idx]=av[idx]-lam
    bad=[]; cws=[]
    for zz in range(q):
        z=F(zz); w=vector(F,[f[i]+z*g[i] for i in range(n)])
        try: cw=Dec.decode_to_code(w)
        except Exception: continue
        S=[i for i in range(n) if w[i]==cw[i]]
        if len(S)<A: continue
        if not extends([g[i] for i in S],[pts[i] for i in S]): bad.append(zz); cws.append(cw)
    M=Matrix(F,[list(c-cws[0]) for c in cws[1:]]) if len(cws)>=2 else Matrix(F,0,n)
    rk=M.rank()
    print("q=%d n=%d k=%d: bad=%d (R3+3=%d) match=%s | codeword-rank=%d (L=1? %s) | line nonzero? %s"
          %(q,n,k,len(bad),R3+3,len(bad)==R3+3,rk,rk<=1,bool(bv!=0)))
for (q,n,k),s in [((31,31,15),1),((41,40,20),2),((37,31,10),3)]:
    run(q,n,k,s)
