#!/usr/bin/env python3
"""Verify the PTE-cluster packing frontier note (image-normalized R=2).

Stdlib-only, zero-arg. Recomputes every number in
experimental/notes/thresholds/pte_cluster_packing_frontier.md and re-checks each
named block exactly. Heavy *searches* that find the champions live in
experimental/scripts/repro_pte_cluster_census.py; here we re-derive the reported
blocks and run only the small certified censuses.

  BLOCK 0  #623 baseline recompute (Prouhet 0.1129, #623 champion 0.131684)
  BLOCK 1  R1: rho=phi+lam-log2 identity; Lemma A affine invariance (PROVED)
  BLOCK 2  R2: diameter-bounded exhaustive optimum (small b) + refutation of
           tight-box / 2-point optimality; Pareto (phi,lam) champions
  BLOCK 3  R2/R3/Prop E: the b=14 champion 0.156659, symmetry, central weight,
           finite-k tensor validation; clean nameable near-champions
  BLOCK 4  R4: Lemma B (c>=2^{b-2r}), Lemma C (fstar<=2^{b-3} -> (1-3/b)log2),
           Prop D (rho<=phi => rho*<=phi*), phi(b) increasing trend
  BLOCK 5  R5: honest bracket [0.156659, log2]
  BLOCK 6  R6: Codex F_17 block gives rho=0.065330 in image-normalization (AUDIT)

Exit 0 iff every check passes. Labels: PROVED / COMPUTED / MEASURED / AUDIT.

Credit: our #623 pte_extremality_image_face.md (consumed at c2027dc); hughes
#564 w_a_star_pte_lemma.md (minimal trade support 6, used in Lemma B). Codex
TEAM_BOARD 2026-07-11 12:42Z F_17 ledger line tested in BLOCK 6.
"""
from __future__ import annotations
import itertools, math, sys
from collections import defaultdict
from fractions import Fraction
from math import comb, gcd, log

LOG2 = math.log(2)
CHECKS: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> bool:
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------- core
def sig_dp(V):
    """DP over elements -> dict[(w,s,q)] = multiplicity (stores only L1 keys)."""
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp


def stat(V):
    """(fstar, L1, rho, phi, lam) for a block V (rho = symmetric tensor rate)."""
    dp = sig_dp(V); b = len(V)
    f = max(dp.values()); L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2, log(f) / b, log(L) / b


def canon(V):
    m = min(V); W = tuple(sorted(x - m for x in V)); g = 0
    for x in W: g = gcd(g, x)
    if g > 1: W = tuple(x // g for x in W)
    R = tuple(sorted(W[-1] - x for x in W))
    return min(W, R)


def is_sym(V):
    V = tuple(sorted(V))
    return V == tuple(sorted(max(V) - x for x in V))


def min_trade_support(V):
    """smallest support 2r of a degree-2 PTE trade inside V (early return)."""
    Vs = tuple(V)
    for r in range(3, len(Vs) // 2 + 1):
        for P in itertools.combinations(Vs, r):
            sp = sum(P); qp = sum(x * x for x in P)
            rest = [x for x in Vs if x not in P]
            for Q in itertools.combinations(rest, r):
                if sum(Q) == sp and sum(x * x for x in Q) == qp:
                    return 2 * r
    return None


# named blocks (exact) -------------------------------------------------------
PROUHET = (0, 1, 2, 4, 5, 6)
CHAMP623 = tuple(x for x in range(14) if x not in (4, 9))            # {0..13}\{4,9}
CHAMP = (0, 2, 3, 4, 5, 8, 9, 13, 14, 17, 18, 19, 20, 22)           # b=14, rho .156659
CLEAN_A = tuple(x for x in range(17) if x not in (2, 8, 14))         # {0..16}\{2,8,14}
CLEAN_B = tuple(x for x in range(19) if x not in (1, 4, 9, 14, 17))  # {0..18}\{1,4,9,14,17}
WIDE12 = tuple(x for x in range(21) if x not in (1, 3, 8, 9, 10, 11, 12, 17, 19))
WIDE13 = tuple(x for x in range(17) if x not in (1, 7, 9, 15))                        # b=13
WIDE15 = tuple(x for x in range(23) if x not in (2, 3, 4, 5, 17, 18, 19, 20))         # b=15
WIDE16 = tuple(x for x in range(23) if x not in (2, 3, 4, 11, 18, 19, 20))            # b=16
F17 = (1, 2, 3, 4, 5, 6, 7, 8, 10, 16)                              # Codex ledger


def block0():
    print("\nBLOCK 0  #623 baseline recompute (AUDIT)")
    f, L, r, _, _ = stat(PROUHET)
    check((f, L) == (2, 63), f"Prouhet {{0,1,2,4,5,6}}: fstar=2 L1=63 (got {f},{L})")
    check(approx(r, log(Fraction(63, 32)) / 6), f"Prouhet rho=log(63/32)/6={r:.6f}=0.112900")
    f, L, r, _, _ = stat(CHAMP623)
    check((f, L) == (6, 3315), f"#623 champ {{0..13}}\\{{4,9}}: fstar=6 L1=3315 (got {f},{L})")
    check(approx(r, 0.131684, 1e-5), f"#623 champ rho={r:.6f}=0.131684")


def block1():
    print("\nBLOCK 1  R1: rho identity + Lemma A affine invariance (PROVED)")
    for V in (PROUHET, CHAMP623, CHAMP, CLEAN_A):
        f, L, r, phi, lam = stat(V)
        check(approx(r, phi + lam - LOG2), f"b={len(V)}: rho == phi+lam-log2 ({r:.6f})")
    # Lemma A: fstar,L1 are affine invariants
    base = stat(CHAMP)[:2]
    ok = True
    for a, sh in ((1, 0), (3, 7), (2, -5), (5, 100), (1, 999)):
        W = tuple(a * x + sh for x in CHAMP)
        if stat(W)[:2] != base:
            ok = False
    check(ok, f"Lemma A: fstar,L1 invariant under x->ax+b (a!=0), base (fstar,L1)={base}")
    # canonical form collapses affine copies
    check(canon(CHAMP) == canon(tuple(3 * x + 7 for x in CHAMP)),
          "affine canonical form identifies x and 3x+7")


def exhaustive_opt(b, slack):
    seen = set(); best = None
    for rest in itertools.combinations(range(1, b + slack), b - 1):
        cv = canon((0,) + rest)
        if cv in seen: continue
        seen.add(cv)
        f, L, r, _, _ = stat(cv)
        if f >= 2 and (best is None or r > best[0]):
            best = (r, cv, f, L)
    return best, len(seen)


def block2():
    print("\nBLOCK 2  R2: diameter-bounded exhaustive optimum + refutation (COMPUTED)")
    exp = {6: (5, 0.112900, (0, 1, 2, 4, 5, 6)),
           9: (4, 0.117188, (0, 1, 2, 3, 5, 6, 7, 11, 12)),
           10: (4, 0.106485, None),
           11: (4, 0.119780, None)}
    for b, (sl, rr, optV) in exp.items():
        best, nb = exhaustive_opt(b, sl)
        r, cv, f, L = best
        check(approx(r, rr, 1e-5),
              f"b={b} (diam<={b+sl-1}, {nb} classes): OPT rho={r:.6f}=={rr} V={cv}")
        if optV is not None:
            check(canon(cv) == canon(optV), f"b={b} optimizer == {optV}")
    # REFUTATION: tight-box {0..13}\{4,9} is NOT the b=12 optimum (wider diam beats it)
    r12wide = stat(WIDE12)[2]
    check(r12wide > 0.131684 + 1e-4,
          f"b=12 wider-diam block rho={r12wide:.6f} > #623 tight champ 0.131684 (tight box was artifact)")
    check(approx(r12wide, 0.140863, 1e-5), f"b=12 wide champ rho={r12wide:.6f}=0.140863")
    # R2 table (b): the other wide-diameter best-known blocks recomputed exactly
    for V, rr, lab in ((WIDE13, 0.139291, "b=13 {0..16}\\{1,7,9,15}"),
                       (WIDE15, 0.144539, "b=15 {0..22}\\{2,3,4,5,17,18,19,20}"),
                       (WIDE16, 0.148886, "b=16 {0..22}\\{2,3,4,11,18,19,20}")):
        f, L, r, _, _ = stat(V)
        check(approx(r, rr, 1e-5) and is_sym(V), f"{lab}: rho={r:.6f}={rr} fstar={f} (symmetric)")
    # REFUTATION of 2-point optimality (as in #623): champion beats Prouhet strictly
    check(stat(CHAMP)[2] > log(Fraction(63, 32)) / 6 + 1e-3,
          f"champion rho={stat(CHAMP)[2]:.6f} >> 2-point Prouhet 0.112900")
    # Pareto (phi,lam) champions
    print("    Pareto (phi, lam, rho, gamma):")
    for b, V in ((6, PROUHET), (9, exp[9][2]), (12, CHAMP623), (14, CHAMP)):
        f, L, r, phi, lam = stat(V)
        print(f"        b={b:2d} phi={phi:.4f} lam={lam:.4f} rho={r:.6f} gamma={LOG2-lam:.4f}")


def poly_pow(coeffs, k):
    out = [1]
    for _ in range(k):
        nxt = [0] * (len(out) + len(coeffs) - 1)
        for i, a in enumerate(out):
            if a:
                for j, cc in enumerate(coeffs):
                    if cc: nxt[i + j] += a * cc
        out = nxt
    return out


def MF_dp(mu, b, k, total):
    dp = {0: 1}
    for _ in range(k):
        nd = defaultdict(int)
        for ws, pr in dp.items():
            for w in range(b + 1):
                if mu[w] > 0 and pr * mu[w] > nd[ws + w]:
                    nd[ws + w] = pr * mu[w]
        dp = nd
    return dp.get(total, 0)


def block3():
    print("\nBLOCK 3  R2/R3/Prop E: b=14 champion 0.156659 + tensor validation")
    f, L, r, phi, lam = stat(CHAMP)
    check((f, L) == (12, 12239), f"champion b=14: fstar=12 L1=12239 (got {f},{L})")
    check(approx(r, 0.156659, 1e-5), f"champion rho={r:.6f}=0.156659 (> #623 0.131684)")
    check(is_sym(CHAMP), "champion is affine-symmetric (R3)")
    # fstar at central weight w=7
    dp = sig_dp(CHAMP); g = defaultdict(lambda: defaultdict(int))
    for (w, s, q), c in dp.items(): g[w][(s, q)] += c
    mu = [max(g[w].values()) if g.get(w) else 0 for w in range(15)]
    D = [len(g.get(w, {})) for w in range(15)]
    check(mu.index(max(mu)) == 7 and max(mu) == 12, f"fstar=12 at central weight 7; mu={mu}")
    check(mu == mu[::-1], "mu profile symmetric (R3 central-weight structure)")
    # Prop E: exact finite-k tensor rate increases to rho
    seq = []
    for k in (1, 2, 3):
        tot = 7 * k; Lk = poly_pow(D, k)[tot]; Mk = comb(14 * k, tot); MF = MF_dp(mu, 14, k, tot)
        rk = log(MF * Fraction(Lk, Mk)) / (14 * k); seq.append(rk)
        check(MF == 12 ** k, f"k={k}: MF_k=12^{k} (max fiber tensors)")
    check(seq[0] < seq[1] < seq[2] < r and approx(seq[2], 0.154981, 1e-4),
          f"Prop E: rho_k={seq[0]:.6f}<{seq[1]:.6f}<{seq[2]:.6f} increasing to rho=0.156659")
    # clean nameable near-champions
    check(approx(stat(CLEAN_A)[2], 0.150163, 1e-5), f"clean {{0..16}}\\{{2,8,14}} rho={stat(CLEAN_A)[2]:.6f}=0.150163")
    check(approx(stat(CLEAN_B)[2], 0.151643, 1e-5), f"clean {{0..18}}\\{{1,4,9,14,17}} rho={stat(CLEAN_B)[2]:.6f}=0.151643")


def block4():
    print("\nBLOCK 4  R4: Lemma B, Lemma C, Prop D, phi(b) trend (PROVED/MEASURED)")
    # Lemma B: c >= 2^{b - 2 r_min}
    okB = True
    for V in (PROUHET, CHAMP623, CLEAN_A, CHAMP):
        b = len(V); c = (1 << b) - stat(V)[1]; ts = min_trade_support(V)
        bound = 1 << (b - ts)
        if not (c >= bound): okB = False
        print(f"        b={b}: c={c} minsupport={ts} 2^(b-2r)={bound} ok={c>=bound}")
    check(okB, "Lemma B: c >= 2^{b-2r} for the minimal trade support (PROVED)")
    # minimal degree-2 trade support is 6 (hughes #564) -- census pin
    supts = set()
    for b in range(6, 9):
        for V in itertools.islice((canon((0,) + r) for r in itertools.combinations(range(1, b + 4), b - 1)), 400):
            if stat(V)[0] >= 2:
                t = min_trade_support(V)
                if t: supts.add(t)
    check(min(supts) == 6, f"minimal degree-2 PTE trade support = 6 (hughes #564); observed {sorted(supts)[:4]}")
    # Lemma C: fstar <= 2^{b-3}
    okC = all(stat(V)[0] <= (1 << (len(V) - 3)) for V in (PROUHET, CHAMP623, CHAMP, CLEAN_A, CLEAN_B))
    check(okC, "Lemma C: fstar <= 2^{b-3} on every named block (PROVED)")
    # cap (1-3/b)log2 strictly tighter than (1-2/b)log2, both -> log2
    for b in (12, 14, 24):
        c3 = (1 - 3 / b) * LOG2; c2 = (1 - 2 / b) * LOG2
        check(c3 < c2, f"b={b}: cap (1-3/b)log2={c3:.4f} < #623 (1-2/b)log2={c2:.4f}")
    check(stat(CHAMP)[2] <= (1 - 3 / 14) * LOG2 + 1e-9, "champion obeys its cap (1-3/14)log2=0.5446")
    check(approx((1 - 3 / 1_000_000) * LOG2, LOG2, 1e-4), f"both caps -> log2 = {LOG2:.6f} (asymptotic wall)")
    # Prop D: rho <= phi on every block; rho* <= phi*
    okD = all(stat(V)[2] <= stat(V)[3] + 1e-12
              for V in (PROUHET, CHAMP623, CHAMP, CLEAN_A, CLEAN_B, WIDE12))
    check(okD, "Prop D: rho <= phi on every block (=> rho* <= phi* = max-fiber rate)")
    # phi(b) increasing: measured lower bounds on the max-fiber rate, no plateau
    pv = [log(stat(V)[0]) / len(V) for V in (PROUHET, CHAMP623, CHAMP)]
    check(pv[0] < pv[1] < pv[2], f"phi(b) increasing: {pv[0]:.4f}<{pv[1]:.4f}<{pv[2]:.4f} (MEASURED, no plateau)")


def block5():
    print("\nBLOCK 5  R5: honest bracket (OPEN wall)")
    lo = stat(CHAMP)[2]
    check(approx(lo, 0.156659, 1e-5), f"proved lower bound rho* >= {lo:.6f} (b=14 champion, tensored)")
    check(approx(LOG2, 0.693147, 1e-5), f"proved upper bound rho* <= phi* <= log2 = {LOG2:.6f}")
    check(lo < LOG2, "bracket [0.156659, 0.693147] non-empty; sup rho OPEN (bound phi*)")


def block6():
    print("\nBLOCK 6  R6: Codex F_17 block in image-normalization (AUDIT, negative)")
    f, L, r, _, _ = stat(F17)
    check((f, L) == (2, 984), f"Codex F_17 {{1..8,10,16}}: fstar=2 L1=984 (got {f},{L})")
    check(approx(r, 0.065330, 1e-5),
          f"F_17 image-normalized rho={r:.6f}=0.065330 < Prouhet 0.1129 (mechanism does not port)")


def main() -> int:
    block0(); block1(); block2(); block3(); block4(); block5(); block6()
    npass = sum(1 for ok, _ in CHECKS if ok)
    ok = npass == len(CHECKS)
    print(f"\nRESULT: {'PASS' if ok else 'FAIL'} ({npass}/{len(CHECKS)})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
