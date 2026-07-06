#!/usr/bin/env python3
"""
b2_modp_giant_extras — toy validation at n=16, t=4, q=17.

Object: a "t-null block" is B subset of mu_n (n-th roots of unity) with
        sum_{x in B} x^r = 0 for r=1..t.
Reframe (Newton): t-null  <=>  monic degree-|B| divisor L_B | X^n-1 whose
        top t coefficients (e_1..e_t) vanish  ==> "coefficient gap" divisor count.

We compare CHAR-0 vs MOD-17:
  - char 0: b1 (PROVED) says every 0/1 t-null vector on mu_n (n=2^s) is a union
    of mu_M-cosets with M>t. For (n,t)=(16,4) -> unions of mu_8-cosets (4 blocks).
  - mod 17: 17 = 1 mod 16 so Frobenius fixes mu_16 pointwise -> b1's forcing dies
    -> "extras" (non-coset-union t-null blocks) can appear. b2 bounds them by n^3.

Char-0 exactness: Phi_16(X)=X^8+1, so zeta^m = (m<8 ? zeta^m : -zeta^{m-8}).
Each power sum is thus an exact integer vector in Z^8; t-null <=> all-zero.
"""
from itertools import combinations, chain

q, n, t = 17, 16, 4
CUSHION = n**3  # = 4096

# ---- mu_16 as F_17^* via primitive root g=3 ; exponent k in Z/16 <-> x = 3^k ----
g = 3
x_of_k = [pow(g, k, q) for k in range(n)]           # x_of_k[k] = 3^k mod 17
assert sorted(x_of_k) == list(range(1, q)), "3 must generate F_17^*"

# ---- mod-p power sums over F_17 ----
def modp_tnull(K):
    # K subset of Z/16 (exponents); block B = {3^k}. sum_{k in K} 3^{k r} mod 17
    for r in range(1, t+1):
        if sum(pow(x_of_k[k], r, q) for k in K) % q != 0:
            return False
    return True

# ---- char-0 power sums, EXACT in Z^8 (basis zeta^0..zeta^7, zeta^8=-1) ----
def char0_tnull(K):
    for r in range(1, t+1):
        vec = [0]*8
        for k in K:
            m = (k*r) % 16
            if m < 8: vec[m]   += 1
            else:     vec[m-8] -= 1
        if any(vec):
            return False
    return True

# ---- Newton cross-check: does L_B = prod (X - x) over F_17 have top-t coeffs 0? ----
def coeff_gap_ok(K):
    # build monic poly over F_17 from roots, check coeffs of X^{b-1}..X^{b-t} are 0
    coeffs = [1]  # leading
    for k in K:
        x = x_of_k[k]
        new = [0]*(len(coeffs)+1)
        for i,c in enumerate(coeffs):
            new[i]   = (new[i]   + c) % q          # * X
            new[i+1] = (new[i+1] - c*x) % q        # * (-x)
        coeffs = new
    b = len(K)
    # coeffs[0]=1 (X^b), coeffs[1]=e_1 up to sign, ..., coeffs[j] = (-1)^j e_j
    if b == 0:
        return True
    for j in range(1, min(t, b)+1):
        if coeffs[j] % q != 0:
            return False
    return True

# ---- structured set: unions of mu_8-cosets (b1 char-0 classification) ----
# mu_8 = {x: x^8=1} = even exponents (k even); its coset = odd exponents.
coset_even = frozenset(k for k in range(n) if k % 2 == 0)
coset_odd  = frozenset(k for k in range(n) if k % 2 == 1)
def powerset(it):
    s=list(it); return chain.from_iterable(combinations(s,r) for r in range(len(s)+1))
structured = set()
for combo in powerset([coset_even, coset_odd]):
    U = frozenset().union(*combo) if combo else frozenset()
    structured.add(U)

# ---- enumerate ALL 2^16 subsets of Z/16 ----
allK = list(range(n))
char0_blocks, modp_blocks = [], []
for size in range(n+1):
    for K in combinations(allK, size):
        K = frozenset(K)
        if char0_tnull(K): char0_blocks.append(K)
        if modp_tnull(K):  modp_blocks.append(K)

char0_set = set(char0_blocks)
modp_set  = set(modp_blocks)
extras    = [K for K in modp_blocks if K not in structured]

# ---- Newton reframing check on every mod-p t-null block ----
newton_ok = all(coeff_gap_ok(K) for K in modp_blocks)

print(f"=== b2 toy  n={n} t={t} q={q}  (17=1 mod 16 -> mod-p / Frobenius-gap regime) ===")
print(f"Newton reframing (power-sum vanishing  <=>  top-{t} coeff gap): "
      f"{'HOLDS on all mod-p blocks' if newton_ok else 'FAILED'}")
print()
print(f"CHAR-0 t-null blocks : {len(char0_set):5d}   (b1 predicts = structured mu_8-coset unions)")
print(f"structured (mu_8-coset unions) : {len(structured):5d}   "
      f"[all t-null? {all(char0_tnull(K) for K in structured)}]")
print(f"char-0 == structured ?  {char0_set == structured}")
print()
print(f"MOD-17 t-null blocks : {len(modp_set):5d}")
print(f"EXTRAS (mod-p t-null, NON-structured) : {len(extras):5d}    cushion n^3 = {CUSHION}")
print(f"  extras within cushion? {len(extras) <= CUSHION}")
from collections import Counter
print(f"  extra block sizes |B|: {dict(sorted(Counter(len(K) for K in extras).items()))}")
# show a few smallest non-trivial extras (as exponent sets and as F_17 elements)
nontrivial = sorted([K for K in extras if 0 < len(K) < n], key=len)
print("  sample extras (exponents k | elements 3^k mod17):")
for K in nontrivial[:6]:
    print(f"    K={sorted(K)}  ->  B={sorted(x_of_k[k] for k in K)}")
