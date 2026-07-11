# Exact char-0 count N0^(0)(n,w,m) = #{m-subsets S of mu_n : p_1(S)=...=p_w(S)=0 in C}
# for n=2^k, via CyclotomicField exact arithmetic; verify the antipodal halving recursion.
from itertools import combinations

def char0_brute(k, w, m):
    n = 2**k
    K = CyclotomicField(n); z = K.gen()
    pts = [z**i for i in range(n)]
    # precompute powers pts[i]^j via z^{i*j mod n}
    cnt = 0
    for S in combinations(range(n), m):
        ok = True
        for j in range(1, w+1):
            s = sum(z**((i*j) % n) for i in S)
            if s != 0:
                ok = False; break
        if ok: cnt += 1
    return cnt

def char0_recur(k, w, m):
    # N0^(0)(2^k,w,m) = [m even]*N0^(0)(2^{k-1},floor(w/2),m/2); base w=0 -> C(2^k,m)
    if w == 0:
        return binomial(2**k, m)
    if m % 2 == 1:
        return 0
    if k == 0:
        return 1 if m == 0 else 0
    return char0_recur(k-1, w//2, m//2)

print("VERIFY char-0 antipodal halving recursion (brute cyclotomic vs recursion)")
print(f"{'k':>2} {'n':>4} {'w':>2} {'m':>2} {'brute':>7} {'recur':>7} {'match':>6}")
cases = [(3,1,4),(3,2,4),(3,3,4),(3,1,2),(3,2,6),(4,1,8),(4,2,8),(4,3,8),(4,2,4),(4,1,6),(4,3,6),(4,4,8)]
allok = True
for (k,w,m) in cases:
    b = char0_brute(k,w,m); r = char0_recur(k,w,m); ok = (b==r); allok &= ok
    print(f"{k:>2} {2**k:>4} {w:>2} {m:>2} {b:>7} {r:>7} {str(ok):>6}")
print(f"\nALL MATCH: {allok}")

# Deployed structure: n=2^21, w=67471, m=981104
k,w,m = 21, 67471, 981104
seq=[]; kk,ww,mm=k,w,m
while ww>0:
    seq.append((kk,ww,mm, mm%2))
    if mm%2==1: break
    kk-=1; ww//=2; mm//=2
print("\nDeployed trace (k,w,m,m%2):")
for t in seq: print("  ",t)
print("N0^(0)(deployed) =", char0_recur(21,67471,981104), " => char-0 (algebraic) part is EMPTY; all of N_0 is generic mod-p.")
