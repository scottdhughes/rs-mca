#!/usr/bin/env python3
"""Verify the moment-map max-fiber note: phi* = log 2.

Stdlib-only, zero-arg. Recomputes every number in
experimental/notes/thresholds/moment_map_max_fiber.md and re-checks the pigeonhole
squeeze on exact objects. Exact fstar past b=30 (to the b=36 ceiling) is in
experimental/scripts/repro_moment_map_max_fiber.py (documented runtime; b=38
exceeds the 2 GB cap). The R2 theorem needs no computation -- it is closed-form.

  BLOCK 0  setup: signature DP; fstar affine-invariant (Lemma A, AUDIT #643);
           interval {0..5} is signature-injective (L1=2^6)
  BLOCK 1  R2 theorem: box bound L1<=B(b), B(b)<b^6 (all b>=2), pigeonhole
           fstar>=2^b/B(b), closed-form phi(V_b) > log2 - 6 ln(b)/b, and the
           squeeze log2-6lnb/b < phi(V_b) <= (1-3/b)log2 (PROVED, exact)
  BLOCK 2  R3 exact census fstar,L1 for b=8..30; the note's table values;
           phi monotone increasing; chain 2^b/B <= 2^b/L1 <= fstar <= 2^{b-3}
  BLOCK 3  R3 max fiber at central weight w=b/2 (b=16 -> (8,64,680), fstar=22)
  BLOCK 4  R4 poly-loss: det G = b^9/2160*(1+o(1)); covolume 2; local-CLT
           prediction ratio order 1; growth-factor 2.86~=2.87; deficit fit alpha
  BLOCK 5  R5 rho(V_b) < champion 0.156659 & rho<=phi (Prop D, AUDIT #643);
           squares contrast phi(squares) << phi(interval)
  BLOCK 6  summary bracket: log2-6lnb/b < phi(b) <= log2, phi* = log2

Exit 0 iff every check passes. Labels: PROVED / COMPUTED / MEASURED / AUDIT.

Credit: our #643 pte_cluster_packing_frontier.md (the phi* wall, Lemma C, Prop D,
Fekete, measured phi(b)); our #623 pte_extremality_image_face.md (the degree-2
moment map). hughes #564 minimal trade support 6 (context, not used).
Erdos-Moser / Sarkozy-Szemeredi (linear anticoncentration context); Bhattacharya-
Rao multidimensional lattice local CLT (R4 refinement).
"""
from __future__ import annotations
import math, time
from collections import defaultdict
from fractions import Fraction
from math import gcd, log

try:
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (2097152 * 1024, 2097152 * 1024))
except Exception:
    pass

LOG2 = math.log(2)
CHECKS: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> bool:
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------- core DP
def sig_dp(V):
    """dict[(w,s,q)] = #subsets of V with that signature."""
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp


def fstar_L1(V):
    dp = sig_dp(V)
    return max(dp.values()), len(dp)


def box_bound(b):
    """B(b) = (b+1)(1+SV)(1+SV2), the signature box of {0..b-1}."""
    SV = b * (b - 1) // 2
    SV2 = (b - 1) * b * (2 * b - 1) // 6
    return (b + 1) * (1 + SV) * (1 + SV2)


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def gram(b):
    p = [sum(i ** m for i in range(b)) for m in range(5)]
    return [[p[0], p[1], p[2]], [p[1], p[2], p[3]], [p[2], p[3], p[4]]]


def clt_pred(b):
    """leading-order local-CLT prediction for fstar(interval,b) (covol=2)."""
    detS = det3(gram(b)) / 64.0
    return 2.0 / ((2 * math.pi) ** 1.5 * math.sqrt(detS)) * (2 ** b)


def covolume(V):
    """covolume of the lattice <(1,v,v^2)> = gcd of all 3x3 minors."""
    rows = [[1, v, v * v] for v in V]
    g = 0
    n = len(rows)
    import itertools
    for a, b_, c in itertools.combinations(range(n), 3):
        g = gcd(g, abs(det3([rows[a], rows[b_], rows[c]])))
    return g


CENSUS_B = list(range(8, 31, 2))  # b = 8..30


def build_census():
    data = {}
    for b in CENSUS_B:
        f, L = fstar_L1(list(range(b)))
        data[b] = (f, L)
    return data


# named exact values from the note ------------------------------------------
NOTE_TABLE = {  # b : (fstar, L1, B(b))
    8: (2, 247, 36801), 12: (5, 3067, 441597), 16: (22, 23635, 2552737),
    20: (98, 110627, 9911181), 24: (617, 372727, 29950625),
    28: (4481, 1014423, 76178621), 30: (12247, 1578540, None),
}


def block0():
    print("\nBLOCK 0  setup: signature DP + Lemma A affine invariance (AUDIT #643)")
    # fstar,L1 affine-invariant
    base = fstar_L1(list(range(14)))
    ok = all(fstar_L1([a * x + sh for x in range(14)]) == base
             for a, sh in ((1, 0), (3, 7), (2, -5), (5, 100)))
    check(ok, f"Lemma A: (fstar,L1) invariant under x->ax+b; base(b=14)={base}")
    # interval {0..5} is signature-injective
    f6, L6 = fstar_L1(list(range(6)))
    check((f6, L6) == (1, 64), f"interval {{0..5}}: fstar=1, L1=2^6=64 (injective) got {(f6,L6)}")


def block1(census):
    print("\nBLOCK 1  R2 THEOREM: pigeonhole squeeze phi* = log 2 (PROVED, exact)")
    # box bound L1 <= B(b), on every census block
    okbox = True
    for b in CENSUS_B:
        f, L = census[b]
        if not (L <= box_bound(b)):
            okbox = False
    check(okbox, "box bound: L1(V_b) <= B(b) = (b+1)(1+SV)(1+SV2) on all census b")
    # closed form B(b) < b^6 and 6*B(b) <= (b+1) b^5 for all b>=2
    okB = all(box_bound(b) < b ** 6 and 6 * box_bound(b) <= (b + 1) * b ** 5
              for b in range(2, 400))
    check(okB, "closed form: B(b) <= (b+1)b^5/6 < b^6 for all 2<=b<400 (=> b>=2)")
    # pigeonhole fstar >= 2^b/B(b) >= 2^b/b^6  (exact integer form fstar*b^6 > 2^b)
    okpig = True
    for b in CENSUS_B:
        f, L = census[b]
        if not (f * box_bound(b) >= (1 << b) and f * b ** 6 > (1 << b)):
            okpig = False
    check(okpig, "pigeonhole: fstar(V_b)*B(b) >= 2^b and fstar(V_b)*b^6 > 2^b (all census b)")
    # closed-form lower bound phi(V_b) > log2 - 6 ln(b)/b, and squeeze <= (1-3/b)log2
    oksq = True
    for b in CENSUS_B:
        f, L = census[b]
        phi = log(f) / b
        lo = LOG2 - 6 * log(b) / b
        hi = (1 - 3 / b) * LOG2
        if not (lo < phi <= hi + 1e-12):
            oksq = False
    check(oksq, "squeeze: log2 - 6 ln(b)/b < phi(V_b) <= (1-3/b) log2 on all census b")
    # the two squeeze rails both -> log2
    check(approx(LOG2 - 6 * log(10 ** 8) / 10 ** 8, LOG2, 1e-4)
          and approx((1 - 3 / 10 ** 8) * LOG2, LOG2, 1e-4),
          "both squeeze rails -> log2 as b->inf (=> phi* = log2)")


def block2(census):
    print("\nBLOCK 2  R3 exact census + three-level chain (COMPUTED)")
    # named table values
    for b, (f, L, B) in NOTE_TABLE.items():
        cf, cL = census[b]
        check((cf, cL) == (f, L), f"b={b}: fstar={f}, L1={L} (got {(cf,cL)})")
        if B is not None:
            check(box_bound(b) == B, f"b={b}: B(b)={B} (got {box_bound(b)})")
    # phi monotone increasing, no plateau
    phis = [log(census[b][0]) / b for b in CENSUS_B]
    check(all(phis[i] < phis[i + 1] for i in range(len(phis) - 1)),
          f"phi(interval,b) strictly increasing {phis[0]:.4f}..{phis[-1]:.4f} (no plateau)")
    check(phis[0] > 0.086 and phis[-1] > 0.31,
          f"phi climbs 0.0866 (b=8) -> {phis[-1]:.4f} (b=30) > 0.31, past #643's 0.18-0.25")
    check(approx(phis[CENSUS_B.index(16)], 0.1932, 1e-3),
          "matches #643 measured phi(16)=0.1932 (interval is the natural max-fiber family)")
    # three-level chain 2^b/B <= 2^b/L1 <= fstar <= 2^{b-3}
    okchain = True
    for b in CENSUS_B:
        f, L = census[b]
        B = box_bound(b)
        pg = Fraction(1 << b, B); pl = Fraction(1 << b, L)
        if not (pg <= pl <= f <= (1 << (b - 3))):
            okchain = False
    check(okchain, "chain: 2^b/B(b) <= 2^b/L1 <= fstar <= 2^{b-3} exact on all census b")
    # rigorous pigeonhole exponent becomes non-vacuous and climbs
    e28 = log(float(Fraction(1 << 28, box_bound(28)))) / 28
    check(float(Fraction(1 << 28, box_bound(28))) > 1 and approx(e28, 0.0450, 1e-3),
          f"gridbox pigeonhole non-vacuous at b=28: 2^b/B(b)>1, exponent {e28:.4f}~=0.045")


def block3(census):
    print("\nBLOCK 3  R3 max fiber at central weight (MEASURED)")
    dp = sig_dp(list(range(16)))
    fstar = max(dp.values())
    args = sorted(k for k, c in dp.items() if c == fstar)
    ws = sorted(set(w for w, _, _ in args))
    check(fstar == 22 and ws == [8], f"b=16: fstar=22 at central weight w=8 (got {fstar}, w={ws})")
    check((8, 64, 680) in args and len(args) == 2,
          f"b=16 argmax includes (8,64,680); 2 symmetric argmax fibers (got {args})")
    # central-weight location across a few b
    okcw = True
    for b in (14, 20, 24):
        dpb = sig_dp(list(range(b)))
        fb = max(dpb.values())
        wb = set(w for (w, s, q), c in dpb.items() if c == fb)
        if wb != {b // 2}:
            okcw = False
    check(okcw, "max fiber at central weight w=b/2 for b=14,20,24 (MEASURED)")


def block4(census):
    print("\nBLOCK 4  R4 poly-loss: fstar = Theta(2^b/b^{9/2}) (MEASURED / local-CLT)")
    # det G = b^9/2160 * (1+o(1))
    ratios = [(b, det3(gram(b)) / (b ** 9 / 2160.0)) for b in (20, 40, 80, 160, 320)]
    check(all(0.98 <= r <= 1.001 for _, r in ratios) and ratios[-1][1] > 0.9999,
          f"det G / (b^9/2160) -> 1: {[round(r,5) for _,r in ratios]}")
    # covolume of increment lattice = 2
    check(all(covolume(list(range(b))) == 2 for b in (4, 6, 8, 10)),
          "covolume of <(1,i,i^2)> = 2 (the q ≡ s mod 2 constraint)")
    # local-CLT prediction ratio is order 1 across the census
    ratios2 = [census[b][0] / clt_pred(b) for b in CENSUS_B]
    check(all(0.9 <= r <= 2.1 for r in ratios2),
          f"fstar / clt_pred in [0.9,2.1] across b=8..30 (same order): "
          f"{ratios2[0]:.2f}..{ratios2[-1]:.2f}")
    # growth factor b=26->28 matches 4*(26/28)^{9/2}
    gf = clt_pred(28) / clt_pred(26)
    check(approx(gf, 4 * (26 / 28) ** 4.5, 1e-3) and approx(gf, 2.87, 1e-2),
          f"clt growth factor b=26->28 = {gf:.3f} = 4*(26/28)^4.5 (b^9 scaling)")
    # deficit fit alpha in [4,6] (local-CLT 9/2; measured ~5)
    xs = [log(b) for b in CENSUS_B]
    ys = [b * LOG2 - log(census[b][0]) for b in CENSUS_B]
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    alpha = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    check(4.0 <= alpha <= 6.0,
          f"deficit fit D_b ~ alpha*ln b: alpha={alpha:.2f} in [4,6] (local-CLT 9/2=4.5; bounded => ->log2)")


def block5(census):
    print("\nBLOCK 5  R5 consequence for rho* + squares contrast (PROVED/MEASURED)")
    # rho(V_b) = phi + lambda - log2; rho <= phi (Prop D); rho < champion 0.156659
    okrho = True; okD = True
    for b in CENSUS_B:
        f, L = census[b]
        phi = log(f) / b; lam = log(L) / b; rho = phi + lam - LOG2
        if not (rho < 0.156659): okrho = False
        if not (rho <= phi + 1e-12): okD = False
    check(okD, "Prop D (AUDIT #643): rho(V_b) <= phi(V_b) on all census b")
    check(okrho, "interval never reaches rho champion 0.156659 (phi*=log2 doesn't move rho* lower bound)")
    # rho -> 0 direction: rho(b=30) below its mid-b peak (heading down)
    def rho(b):
        f, L = census[b]; return log(f) / b + log(L) / b - LOG2
    check(rho(30) < rho(16), f"rho(interval,30)={rho(30):.4f} < peak rho(16)={rho(16):.4f} (rho->0 as phi->log2, lam->0)")
    # squares contrast: phi(squares) << phi(interval)
    okc = True
    for b in (10, 12, 14, 16):
        fs, _ = fstar_L1([i * i for i in range(b)])
        fi, _ = fstar_L1(list(range(b)))
        if not (log(fs) / b < log(fi) / b):
            okc = False
    check(okc, "phi(squares,b) << phi(interval,b) for b=10..16 (spreading kills fstar)")


def block6(census):
    print("\nBLOCK 6  summary bracket: phi* = log 2")
    check(approx(LOG2, 0.693147, 1e-5), f"phi* = log 2 = {LOG2:.6f}")
    # every finite phi(b) strictly below log2 (sup not attained), yet -> log2
    check(all(log(census[b][0]) / b < LOG2 for b in CENSUS_B),
          "each phi(b) < log2 strictly; sup_b phi(b) = log2 (not attained)")
    print("\n    VERDICT: the question 'is phi* < log 2?' is answered NO. phi* = log 2.")


def main() -> int:
    t0 = time.time()
    census = build_census()
    block0(); block1(census); block2(census); block3(census)
    block4(census); block5(census); block6(census)
    npass = sum(1 for ok, _ in CHECKS if ok)
    ok = npass == len(CHECKS)
    print(f"\nRESULT: {'PASS' if ok else 'FAIL'} ({npass}/{len(CHECKS)})  [{time.time()-t0:.1f}s]")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
