import itertools
from collections import defaultdict

def prim_root(p):
    phi=p-1; m=phi; f=[]; d=2
    while d*d<=m:
        if m%d==0:
            f.append(d)
            while m%d==0: m//=d
        d+=1
    if m>1: f.append(m)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g

def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    pts=[]; cur=1
    for _ in range(n): pts.append(cur); cur=cur*z%p
    return pts

def coupling(p,n,w,dilates,pts):
    """E_c[ prod_{r in dilates} |pi(rc)|^2 ] / n^K  = collision-count(signature)/n^K.
       signature(a_1..a_K) = ( sum_i dilates[i]*a_i^j mod p )_{j=1..w}, a_i in mu_n."""
    K=len(dilates)
    buck=defaultdict(int)
    for tup in itertools.product(range(n),repeat=K):
        sig=tuple(sum(dilates[i]*pts[(j*tup[i])%n] for i in range(K))%p for j in range(1,w+1))
        buck[sig]+=1
    coll=sum(v*v for v in buck.values())
    return coll/(n**K)

def primes_1mod(nmod,count):
    def isp(m):
        i=2
        while i*i<=m:
            if m%i==0: return False
            i+=1
        return m>=2
    r=[]; x=nmod+1
    while len(r)<count:
        if x%nmod==1 and isp(x): r.append(x)
        x+=1
    return r

n=16
ps=primes_1mod(n,9)   # 17,97,113,193,241,257,337,353,401 ...
from math import log
print(f"n={n}. Coupling C(D)=E_c[prod|pi(rc)|^2]/n^K.  C=1 <=> dilates INDEPENDENT; C>1 <=> coupled.\n")
for w in [2,3]:
    print(f"===== w={w}  (p^w vs n^K saturation: p^w={ps[0]}^{w}.. ; n^2={n**2}, n^3={n**3}, n^4={n**4}) =====")
    hdr=f"{'p':>6} {'gamma':>6} | {'C[1,2]':>8} {'C[1,3]':>8} {'C[1,4]':>8} | {'C[1,2,3]':>9} {'C[1,2,3,4]':>11}"
    print(hdr); print("-"*len(hdr))
    for p in ps:
        pts=subgroup(p,n)
        c12=coupling(p,n,w,[1,2],pts)
        c13=coupling(p,n,w,[1,3],pts)
        c14=coupling(p,n,w,[1,4],pts)
        c123=coupling(p,n,w,[1,2,3],pts)
        c1234=coupling(p,n,w,[1,2,3,4],pts)
        print(f"{p:>6} {log(n)/log(p):>6.3f} | {c12:>8.3f} {c13:>8.3f} {c14:>8.3f} | {c123:>9.3f} {c1234:>11.3f}")
    print()
print("Read: does C stay ~1 (dilates independent => product-structure proof route open),")
print("or grow with #dilates / at saturation (small p) => coupled => obstruction mechanism.")
