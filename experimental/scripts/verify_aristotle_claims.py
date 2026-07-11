import numpy as np, itertools
from math import comb
from collections import Counter
def mu_all(p,n):  # n-th roots of unity in F_p
    # find element of order n
    for g in range(2,p):
        if pow(g,p-1,p)==1:
            # order of g
            o=1;v=g
            while v!=1:v=v*g%p;o+=1
            if o==p-1:
                z=pow(g,(p-1)//n,p); break
    return [pow(z,k,p) for k in range(n)]
def fibers(p,n,w,d):
    S=mu_all(p,n)
    syn=Counter()
    for A in itertools.combinations(range(n),d):
        v=tuple(sum(pow(S[i],j,p) for i in A)%p for j in range(1,w+1))
        syn[v]+=1
    return syn

# CLAIM 1: Aristotle's counterexample p=13,n=12,w=2,d=3 has a fiber of size 4 (=> pointwise/max-fiber bound false)
p,n,w,d=13,12,2,3
syn=fibers(p,n,w,d)
maxf=max(syn.values()); avg=comb(n,d)/p**w
print(f"COUNTEREXAMPLE CHECK p={p},n={n},w={w},d={d}: max fiber = {maxf}, avg = C(n,d)/p^w = {avg:.3f}")
print(f"  max fiber {maxf} > 2*avg {2*avg:.3f}? {maxf>2*avg}  => pointwise 'fiber<=2*avg' FALSE (Aristotle claimed max=4)")
print(f"  Aristotle arithmetic: max_fiber*p^w = {maxf*p**w} vs 2*C(n,d) = {2*comb(n,d)}  ({maxf*p**w} > {2*comb(n,d)} = {maxf*p**w>2*comb(n,d)})")

# CLAIM 2: the sorry'd inequality E_d <= 2 C(n,d)^2 / p^w  IS TRUE above threshold (ratio in [1,2))
print("\nSORRY'd CLAIM check: E_d <= 2 C(n,d)^2/p^w above threshold (C(n,d)>=p^w)?")
print(f"{'p':>4} {'n':>3} {'w':>2} {'d':>2} {'E_d':>8} {'2Cnd^2/p^w':>12} {'ratio E_d/(Cnd^2/p^w)':>22} {'<2?':>5}")
for (p,n,w,d) in [(13,12,2,3),(13,12,2,4),(13,12,2,5),(17,16,2,5),(17,16,2,6),(41,20,2,7)]:
    if (p-1)%n: continue
    if comb(n,d)<p**w: 
        print(f"{p:>4} {n:>3} {w:>2} {d:>2}  (below threshold C(n,d)<p^w, skip)"); continue
    syn=fibers(p,n,w,d)
    Ed=sum(v*v for v in syn.values())
    rand=comb(n,d)**2/p**w
    print(f"{p:>4} {n:>3} {w:>2} {d:>2} {Ed:>8} {2*rand:>12.1f} {Ed/rand:>22.4f} {str(Ed<=2*rand):>5}")
