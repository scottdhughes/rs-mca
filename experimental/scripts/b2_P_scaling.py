import numpy as np, math
from math import comb
def elt_order_n(p,n):
    for x in range(2,p):
        h=pow(x,(p-1)//n,p)
        if pow(h,n//2,p)!=1: return h
def mu_n(p,n):
    h=elt_order_n(p,n); S=[1];v=h
    while v!=1:S.append(v);v=v*h%p
    assert len(S)==n
    return S
def counts_w2(p,n,m):
    # exact DP: D[k, s1, s2] = #{k-subsets with (p_1,p_2)=(s1,s2) mod p}
    S=mu_n(p,n)
    D=np.zeros((m+1,p,p),dtype=np.float64)
    D[0,0,0]=1.0
    for a in S:
        a2=(a*a)%p
        # D[1:] += roll(D[:-1], (a,a2)) along axes (1,2)
        shifted=np.roll(D[:m], a, axis=1)
        shifted=np.roll(shifted, a2, axis=2)
        D[1:]+=shifted
    N0=D[m,0,0]                      # p_1=p_2=0
    N0_even=D[m,:,0].sum()           # p_2=0, p_1 free (the single even power sum)
    return N0, N0_even
def check_brute(p,n,m):
    import itertools
    S=mu_n(p,n); c=0
    for idx in itertools.combinations(range(n),m):
        s1=sum(S[i] for i in idx)%p; s2=sum(S[i]*S[i] for i in idx)%p
        if s1==0 and s2==0: c+=1
    return c

n=32; w=2; m=6; Cnm=comb(n,m)
# sanity check DP vs brute on small p
p0=97
N0d,_=counts_w2(p0,n,m); print(f"DP check p={p0}: N0={int(N0d)} vs brute={check_brute(p0,n,m)}  (Cnm={Cnm})\n")
print(f"P-SCALING TEST  n={n} w={w} m={m}  C(n,m)={Cnm}  [sqrt-cancel: |P|~sqrt(p^w Cnm)=p*{math.sqrt(Cnm):.0f}]")
print(f"{'p':>5} {'r=n/(w√p)':>10} {'Cnm/p^w':>9} {'N0':>7} {'mu':>9} {'|P|':>12} {'|P|/p':>9} {'|P|/p^2':>9}")
for p in [97,257,353,449,577,641,673,769,929,1153,1409,1601]:
    if (p-1)%n!=0: continue
    N0,N0e=counts_w2(p,n,m)
    P=p**2*N0 - p*N0e
    mu=Cnm/p**2; r=n/(w*math.sqrt(p))
    print(f"{p:>5} {r:>10.3f} {Cnm/p**2:>9.1f} {int(N0):>7} {mu:>9.3f} {abs(P):>12.1f} {abs(P)/p:>9.1f} {abs(P)/p**2:>9.3f}")
