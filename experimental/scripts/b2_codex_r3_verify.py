from itertools import combinations, product
from math import comb

def prim_root(p):
    phi=p-1; mm=phi; f=[]; d=2
    while d*d<=mm:
        if mm%d==0:
            f.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: f.append(mm)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in f): return g
def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    return [pow(z,k,p) for k in range(n)]

# CLAIM (Codex Sec 2): Z_1 = #{S subset mu_n,|S|=m, sum_x x^{2j}=0, j=1..e} equals the WEIGHTED
# ternary slice over y=x^2 in mu_{n/2}: sum over k_y in {0,1,2} with sum k_y=m, sum k_y y^j=0 (j<=e),
# weighted by 2^{#{k_y=1}}. And this is NOT the plain Boolean mu_{n/2} fiber count.
p,n,m,e=97,16,8,2
G=subgroup(p,n)
# Z_1 direct: even power sums x^{2j}=0 for j=1..e  (exponents 2,4)
Z1_direct=0
for S in combinations(range(n),m):
    ok=all(sum(pow(G[i],2*j,p) for i in S)%p==0 for j in range(1,e+1))
    if ok: Z1_direct+=1
# weighted ternary over y in mu_{n/2}: pair i and i+n/2 (antipodes, same square)
half=n//2
Y=[pow(G[i],2,p) for i in range(half)]   # y = x^2, mu_{n/2}
# enumerate k_y in {0,1,2} for each of the `half` pairs, sum k=m, sum k_y y^j=0
Z1_weighted=0
plain_boolean=0   # k_y in {0,1} only (would-be plain mu_{n/2} fiber count at size m -- ill-defined but for contrast)
for ks in product(range(3),repeat=half):
    if sum(ks)!=m: continue
    if all(sum(ks[i]*pow(Y[i],j,p) for i in range(half))%p==0 for j in range(1,e+1)):
        singles=sum(1 for k in ks if k==1)
        Z1_weighted+= 2**singles
# plain Boolean mu_{n/2} fiber at size m/2 (Codex says descended object is NOT this)
plain=0
for T in combinations(range(half),m//2):
    if all(sum(pow(Y[i],j,p) for i in T)%p==0 for j in range(1,e+1)): plain+=1

print(f"Z_1 (direct, even-moment fiber over mu_16)     = {Z1_direct}")
print(f"Z_1 (weighted ternary k_y in 0/1/2, 2^singles) = {Z1_weighted}   MATCH={Z1_direct==Z1_weighted}")
print(f"plain Boolean mu_8 fiber (|T|=m/2, Codex: NOT this) = {plain}")
print(f"=> alphabet-growth claim {'CONFIRMED' if Z1_direct==Z1_weighted and Z1_weighted!=plain else 'NOT confirmed'}: "
      f"peeling leaves the Boolean category (weighted ternary != plain fiber).")

# sanity: 17 levels at deployment
w=67471
L=0; wl=w
while wl>0: wl//=2; L+=1
print(f"\nDeployment levels: w=67471 -> w halves to 0 after L={L} steps (Codex claim: 17).")
