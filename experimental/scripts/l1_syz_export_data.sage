# export h_k (and g_k, w_k, c_k) for the saturators to an M2-readable data file
SATS = [
    dict(label="ell11p331", p=331, ell=11, gamma=[97,29,97,239,171,92,143,155,270,1]),
    dict(label="ell13p313", p=313, ell=13, gamma=[254,289,29,276,242,219,201,261,79,232,133,1]),
    dict(label="ell17p103", p=103, ell=17, gamma=[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
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
        res.append((int(b**ell), mu, int(modal), [int(c) for c in hk.coefficients(sparse=False)],
                    [int(c) for c in gk.coefficients(sparse=False)]))
    return res
import io
lines=["SATDATA = {"]
for W in SATS:
    fb=fibers(W["gamma"],W["p"],W["ell"])
    mus="{"+",".join(str(mu) for (w,mu,c,h,g) in fb)+"}"
    hks="{"+",".join("{"+",".join(map(str,h))+"}" for (w,mu,c,h,g) in fb)+"}"
    lines.append('  {"%s",%d,%d,%s,%s},' % (W["label"],W["p"],W["ell"],mus,hks))
lines.append("};")
open("/tmp/l1_syz_data.m2","w").write("\n".join(lines)+"\n")
print("wrote /tmp/l1_syz_data.m2")
print(open("/tmp/l1_syz_data.m2").read()[:300])
