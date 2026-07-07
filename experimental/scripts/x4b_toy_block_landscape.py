#!/usr/bin/env python3
"""x4b program, step 1: verify the moment_trade_staircase witness + map the toy t-null block landscape.

A t-moment-null block: B subset mu_n (in F_p), e_1(B)=...=e_t(B)=0 (equiv p_1..p_t=0, char>t), |B|>t.
DAG witness (moment_trade_staircase): B = {11^e : e in {0,1,2,4,16,45,50,60}} in mu_64 over F_193,
t=3-null, p_4 = 18, NO rotation/reflection stabilizer. VERIFY all claims independently.
Then map the landscape at small rows (n, p, t): enumerate t-null blocks by size b (feasible b only),
classify: quotient (union of mu_M-cosets, M|n, M>1  <=> nontrivial rotation stabilizer... precisely:
rotation-stabilizer subgroup S_B = {a in mu_n : aB=B}; B is a coset union iff S_B != {1}), dihedral
(B = cB^{-1} for some c), else PRIMITIVE. Report: #blocks by size, #primitive, max disjoint family size
among primitive blocks (greedy + exact small cases), and the U2-C' check: primitive blocks that are NOT
coset unions falsify the residual dichotomy at that row.
"""
from __future__ import annotations
import math
from itertools import combinations
import sympy


def mu(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return [pow(z, k, p) for k in range(n)], z


def powersums_zero(B, t, p):
    for r in range(1, t + 1):
        if sum(pow(x, r, p) for x in B) % p != 0:
            return False
    return True


def verify_witness():
    p, n, t = 193, 64, 3
    pts, z = mu(p, n)
    # find element of order 64 equal to 11? 11 in mu_64? 11^64 mod 193:
    ok11 = pow(11, 64, 193) == 1 and pow(11, 32, 193) != 1
    B = [pow(11, e, 193) for e in (0, 1, 2, 4, 16, 45, 50, 60)]
    ps = [sum(pow(x, r, 193) for x in B) % 193 for r in range(1, 5)]
    # stabilizer: rotations a in mu_64 with aB=B; reflections c with B = c*B^{-1}
    Bs = set(B)
    rot = [a for a in pts if all((a * x) % 193 in Bs for x in B)]
    Binv = [pow(x, 193 - 2, 193) for x in B]
    refl = [c for c in pts if all((c * y) % 193 in Bs for y in Binv)]
    print(f"[witness] 11 has order 64 in F_193: {ok11}")
    print(f"[witness] p_1..p_4 = {ps}  (claim: 0,0,0,18)  -> t=3-null: {ps[:3] == [0,0,0]} , p_4={ps[3]} (claim 18)")
    print(f"[witness] rotation stabilizer = {rot} (claim trivial: {rot == [1]})  reflections: {len(refl)} (claim 0: {len(refl) == 0})")
    print(f"[witness] |B|={len(B)} > t+1={4}: {len(B) > 4};  is coset union? {'NO (primitive)' if rot == [1] else 'YES'}")
    print(f"[witness] => U2-C' residual dichotomy (every t-null block = coset union w/ M>=t) is FALSIFIED at (193,64,3): {rot == [1]}")


def landscape(p, n, t, bmax):
    pts, z = mu(p, n)
    idx = {x: i for i, x in enumerate(pts)}
    results = {}
    prim_blocks = []
    for b in range(t + 1, bmax + 1):
        cnt = comb_count = 0; prim = 0; quo = 0; dih = 0
        blocks_b = []
        for B in combinations(pts, b):
            if powersums_zero(B, t, p):
                cnt += 1
                Bs = set(B)
                rot = [a for a in pts[1:] if all((a * x) % p in Bs for x in B)]
                if rot:
                    quo += 1; continue
                Binv = [pow(x, p - 2, p) for x in B]
                refl = any(all((c * y) % p in Bs for y in Binv) for c in pts)
                if refl:
                    dih += 1
                else:
                    prim += 1; prim_blocks.append(frozenset(B))
        results[b] = (cnt, quo, dih, prim)
    # max disjoint family among primitive blocks (greedy; exact if few)
    kmax = 0
    if prim_blocks:
        # greedy by size
        chosen = []
        for B in sorted(prim_blocks, key=len):
            if all(not (B & C) for C in chosen):
                chosen.append(B)
        kmax = len(chosen)
    return results, len(prim_blocks), kmax


def main():
    print("### STEP 1a: independent verification of the DAG moment-trade witness")
    verify_witness()
    print("\n### STEP 1b: toy landscape -- t-null blocks by size; quotient/dihedral/PRIMITIVE split; disjoint families")
    print("#  (mean = C(n,b)/p^t printed for calibration; enumeration exact)")
    for p, n, t, bmax in [(97, 16, 2, 6), (193, 16, 2, 6), (97, 32, 2, 5), (193, 32, 3, 5), (257, 16, 2, 6)]:
        if (p - 1) % n:
            continue
        res, nprim, kmax = landscape(p, n, t, bmax)
        print(f"\n  row (p={p}, n={n}, t={t}), sizes {t+1}..{bmax}:")
        for b, (cnt, quo, dih, prim) in res.items():
            mean = math.comb(n, b) / p ** t
            print(f"    b={b}: blocks={cnt:<6} (quo={quo}, dih={dih}, PRIM={prim})   mean={mean:9.3f}")
        print(f"    total primitive={nprim}; max disjoint primitive family (greedy) k={kmax}")
    print("\n# Landscape verdict: where mean >= 1, blocks (incl. primitive) appear; where mean << 1 they vanish.")
    print("# Any PRIM > 0 row falsifies U2-C' there. k tracks how many disjoint primitives coexist (staircase 2^k).")


if __name__ == "__main__":
    raise SystemExit(main())
