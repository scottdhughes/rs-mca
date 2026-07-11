import numpy as np, itertools
def prim_root(p):
    phi=p-1; mm=phi; f=[]; d=2
    while d*d<=mm:
        if mm%d==0:
            f.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: f.append(mm)
    return next(g for g in range(2,p) if all(pow(g,phi//q,p)!=1 for q in f))
def subgroup(p,n):
    g=prim_root(p); z=pow(g,(p-1)//n,p)
    return [pow(z,k,p) for k in range(n)]
# EXACT claim: Sum_c |tau_w(c)|^4 = p^w * (2n^2 - n) for w>=2, and Sum_c|tau_w|^2 = p^w * n.
# Verify by DIRECT solution count: #{(a,b,c,d) in mu_n^4 : a^j+b^j=c^j+d^j for all j=1..w}.
print("EXACT engine identity check (direct mu_n^4 solution count, no floats):")
print(f"{'p':>4} {'n':>3} {'w':>2} {'#4-sols':>9} {'2n^2-n':>8} {'match4':>7} {'#2-sols':>8} {'n':>4} {'match2':>7}")
for (p,n,w) in [(97,16,2),(97,16,3),(193,16,4),(97,32,2),(257,16,5)]:
    if (p-1)%n: continue
    G=subgroup(p,n)
    pw=[[pow(a,j,p) for a in G] for j in range(1,w+1)]  # pw[j-1][i]=G[i]^j
    # 2-fold: #{(a,b): Phi(a)=Phi(b)} = #{a=b} = n (Phi injective since j=1 coord)
    two=sum(1 for i in range(n) for k in range(n) if all(pw[j][i]==pw[j][k] for j in range(w)))
    # 4-fold: #{(a,b,c,d): a^j+b^j=c^j+d^j all j}. Index by (i1,i2) syndrome, match.
    from collections import Counter
    syn=Counter()
    for i in range(n):
        for k in range(n):
            syn[tuple((pw[j][i]+pw[j][k])%p for j in range(w))]+=1
    four=sum(v*v for v in syn.values())
    print(f"{p:>4} {n:>3} {w:>2} {four:>9} {2*n*n-n:>8} {str(four==2*n*n-n):>7} {two:>8} {n:>4} {str(two==n):>7}")
print("\n=> Sum_c|tau|^4 = p^w(2n^2-n) and Sum_c|tau|^2 = p^w n hold EXACTLY (integer solution counts).")
