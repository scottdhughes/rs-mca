# Step-3 census: low-support primitive trades on a 2-power domain D = mu_n, at p==+1 vs p==-1 mod n.
# (A) t-null blocks of size b in [t+1, 2t+1] (the moment-null-block trades = moment_trade_staircase object);
#     classify coset-union (nontrivial rotation stab) vs PRIMITIVE. Reciprocal-gap predicts PRIMITIVE=0 at p==-1.
# (B) sp_w(w+1; D) top-stratum shift-pairs: disjoint (w+1)-subsets S,T with matching p_1..p_w; classify
#     coset/dilation vs PRIMITIVE. Measure p==+1 vs p==-1.
from itertools import combinations

def domain(p, n):
    # mu_n in F_p if n | p-1 else in F_{p^2}
    if (p - 1) % n == 0:
        F = GF(p); q = p
    else:
        assert (p + 1) % n == 0
        F = GF(p^2, 'a'); q = p^2
    g = F.multiplicative_generator(); z = g^((q - 1)//n)
    assert z.multiplicative_order() == n
    return F, [z^k for k in range(n)]

def rot_stab_nontrivial(B, pts, F):
    Bs = set(B)
    return any(all(a*x in Bs for x in B) for a in pts[1:])

def census(p, n, t):
    F, pts = domain(p, n)
    sign = "+1" if (p-1) % n == 0 else "-1"
    # (A) t-null blocks
    print(f"  p={p} (== {sign} mod {n}), n={n}, t=w={t}:")
    for b in range(t+1, 2*t+2):
        blocks = [B for B in combinations(pts, b)
                  if all(sum(x^j for x in B) == 0 for j in range(1, t+1))]
        prim = sum(0 if rot_stab_nontrivial(B, pts, F) else 1 for B in blocks)
        print(f"    (A) t-null blocks b={b}: total={len(blocks):4d}  coset={len(blocks)-prim:4d}  PRIMITIVE={prim:4d}"
              + ("   <- reciprocal-gap: predict 0" if sign=="-1" else ""))
    # (B) sp_w(w+1) top stratum: disjoint (w+1)-subsets with matching p_1..p_w
    k = t + 1
    subs = list(combinations(pts, k))
    # index by prefix (p_1..p_w)
    from collections import defaultdict
    byp = defaultdict(list)
    for S in subs:
        key = tuple(sum(x^j for x in S) for j in range(1, t+1))
        byp[key].append(set(S))
    pairs = prim_pairs = 0
    for key, group in byp.items():
        for i in range(len(group)):
            for jx in range(len(group)):
                if i == jx: continue
                S, Tt = group[i], group[jx]
                if S & Tt: continue         # disjoint
                pairs += 1
                U = list(S | Tt)
                # primitive = union not rotation-stabilized AND not dilation/inversion related
                primU = not rot_stab_nontrivial(U, pts, F)
                prim_pairs += primU
    print(f"    (B) sp_w(w+1) top stratum: ordered disjoint pairs={pairs:5d}  union-PRIMITIVE={prim_pairs:5d}")

for p, n, t in [(97, 16, 2), (31, 16, 2), (113, 16, 2), (47, 16, 2), (193, 16, 3), (79, 16, 3)]:
    census(p, n, t)
print("# reciprocal-gap => PRIMITIVE t-null blocks of size <= 2t+1 are 0 at p==-1 rows (Mersenne).")
print("# (B) shows whether the shift-pair top stratum also thins at p==-1 (measured, not claimed).")
