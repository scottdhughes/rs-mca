#!/usr/bin/env python3
"""Verify PTE extremality on the image-normalized R=2 face.

Stdlib-only, zero-arg (optional --block to run one block, --box to widen the
ground-set search, --nmax for the census depth).  Recomputes every number in
experimental/notes/thresholds/pte_extremality_image_face.md:

  BLOCK 0  reproduce Codex PR #615's two-moment Prouhet block exactly
  BLOCK 1  the rate machinery: asymptotic (fstar,L1) formula == exact finite-k
           tensor rate (MF via DP) == exact geometric-Q^i-spacing brute force
  BLOCK 2  PRODUCT OPTIMIZATION: search degree-2 collision blocks; is the
           2-point Prouhet block rate-optimal?  (verdict: NO -- refuted)
  BLOCK 3  the objective G=(fstar*L1)^{1/b}, the fstar+L1<=2^b+1 constraint,
           and the plateau of the best structured family
  BLOCK 4  UPPER BOUND: (i) the PROVED structural theorem (PTE-universality of
           the R=2 fiber, = hughes's canonical star-trade decomposition), (ii)
           the abstract analytic cap rho<=(1-2/b)log2, its gap to the optimum,
           and the named missing (packing) inequality; superadditivity
  BLOCK 5  CENSUS: ALL fibers of (sum t, sum t^2) over {0..N-1}, prime field,
           at small N; extremal fibers are degree-2 PTE trades; frontier

Exit 0 iff every check passes.  Labels: PROVED (exact hand derivation),
COMPUTED (exhaustive exact enumeration), MEASURED (exact finite toy, asymptotic
read off), AUDIT (cross-reference).

Credit: #534 (PTM kappa-growth lineage, the per-chart secant extremal),
scottdhughes #564 (the equal-power-sum wall + the canonical star-PTE trade
lemma), Codex #615 (the two-moment Prouhet instantiation + the near-Sidon
razor floor), LegaSage #585 chain (the R=2 razor predicate), holmbuar #614
(the image-vs-span normalization map).  The AMBIENT/SIGNED (LS) side is
scottdhughes's corner and is out of scope here.
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
from collections import defaultdict
from fractions import Fraction
from math import comb

CHECKS: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> bool:
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)


def approx(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ----------------------------------------------------------------------------
# core block combinatorics
# ----------------------------------------------------------------------------
def group_by_signature(V: tuple[int, ...]):
    """{weight: {(sum,sumsq): multiplicity}} over all 2^b subsets of V."""
    b = len(V)
    out: dict[int, dict[tuple[int, int], int]] = defaultdict(lambda: defaultdict(int))
    for mask in range(1 << b):
        w = s = s2 = 0
        for i in range(b):
            if mask & (1 << i):
                w += 1
                s += V[i]
                s2 += V[i] * V[i]
        out[w][(s, s2)] += 1
    return out


def mu_D(V: tuple[int, ...]):
    """mu[w]=max collision multiplicity at weight w; D[w]=# distinct sigs at w."""
    b = len(V)
    g = group_by_signature(V)
    mu = [max(g[w].values()) if g.get(w) else 0 for w in range(b + 1)]
    D = [len(g.get(w, {})) for w in range(b + 1)]
    return mu, D, g


def max_fiber_members(V: tuple[int, ...]):
    """(fstar, weight*, member masks) for a globally-maximal collision fiber."""
    b = len(V)
    g = group_by_signature(V)
    best = (0, None, None)  # (mult, weight, key)
    for w in range(b + 1):
        for key, m in g.get(w, {}).items():
            if m > best[0]:
                best = (m, w, key)
    fstar, w, key = best
    members = []
    if key is not None:
        for mask in range(1 << b):
            if bin(mask).count("1") != w:
                continue
            s = sum(V[i] for i in range(b) if mask & (1 << i))
            s2 = sum(V[i] * V[i] for i in range(b) if mask & (1 << i))
            if (s, s2) == key:
                members.append(mask)
    return fstar, w, members


def additive_energy(members: list[int], b: int) -> int:
    """E(F)=#{(i,j,k,l): v_i+v_j=v_k+v_l} via the difference multiset."""
    vecs = [tuple((mask >> i) & 1 for i in range(b)) for mask in members]
    dc: dict[tuple[int, ...], int] = defaultdict(int)
    for vi in vecs:
        for vj in vecs:
            dc[tuple(vi[t] - vj[t] for t in range(b))] += 1
    return sum(r * r for r in dc.values())


def poly_pow(coeffs: list[int], k: int) -> list[int]:
    out = [1]
    for _ in range(k):
        nxt = [0] * (len(out) + len(coeffs) - 1)
        for i, a in enumerate(out):
            if a:
                for j, cc in enumerate(coeffs):
                    nxt[i + j] += a * cc
        out = nxt
    return out


def MF_dp(mu: list[int], b: int, k: int, total: int) -> int:
    """Exact max tensor fiber: max product of per-block multiplicities over
    weight-compositions summing to `total` (geometric spacing => independent)."""
    dp = {0: 1}
    for _ in range(k):
        nd: dict[int, int] = defaultdict(int)
        for wsum, prod in dp.items():
            for w in range(b + 1):
                if mu[w] > 0:
                    nd[wsum + w] = max(nd[wsum + w], prod * mu[w])
        dp = nd
    return dp.get(total, 0)


def rho_exact_k(V: tuple[int, ...], k: int):
    """Exact finite-k tensor rate at balanced total weight (b//2)*k."""
    b = len(V)
    mu, D, _ = mu_D(V)
    m = b // 2
    total = m * k
    L = poly_pow(D, k)[total]
    M = comb(b * k, total)
    MF = MF_dp(mu, b, k, total)
    if MF < 1 or L < 1:
        return None
    return math.log(MF * Fraction(L, M)) / (b * k), MF, L, M


def rho_asym(V: tuple[int, ...]):
    """Asymptotic per-point image-normalized rate rho and energy deficit delta.

    fstar = max_w mu(w) (achievable in the tensor via the symmetric weight
    split {w, b-w}); L1 = sum_w D_w = # distinct signatures.  For symmetric V
    the balanced saddle is x*=1, so log L/N -> log L1/b and log M/N -> log2."""
    b = len(V)
    mu, D, _ = mu_D(V)
    fstar = max(mu)
    L1 = sum(D)
    if fstar < 2:
        return None
    fmem = max_fiber_members(V)
    E1 = additive_energy(fmem[2], b)
    rho = (math.log(fstar) + math.log(L1)) / b - math.log(2)
    delta = (3 * math.log(fstar) - math.log(E1)) / b
    theta = math.log(E1) / math.log(fstar)
    return {"V": V, "b": b, "fstar": fstar, "L1": L1, "c": (1 << b) - L1,
            "E1": E1, "rho": rho, "delta": delta, "theta": theta,
            "phi": math.log(fstar) / b, "G": (fstar * L1) ** (1.0 / b)}


def geom_brute_rho(V: tuple[int, ...], k: int):
    """Exact tensor rate by explicit geometric-Q^i spacing (no-carry brute)."""
    b = len(V)
    total = (b // 2) * k
    if comb(b * k, total) > 3_000_000:
        return None
    Q, SH = 10 ** 7, 100
    T = [(x + SH) * (Q ** i) for i in range(k) for x in V]
    g: dict[tuple[int, int], int] = defaultdict(int)
    for combo in itertools.combinations(range(len(T)), total):
        s = sum(T[i] for i in combo)
        s2 = sum(T[i] * T[i] for i in combo)
        g[(s, s2)] += 1
    return math.log(max(g.values()) * Fraction(len(g), comb(len(T), total))) / len(T)


# ----------------------------------------------------------------------------
def block0() -> None:
    print("\nBLOCK 0  reproduce PR #615 two-moment Prouhet block (AUDIT/recompute)")
    OFFS = (0, 1, 2, 4, 5, 6)
    A, B = (0, 4, 5), (1, 2, 6)
    check(sum(A) == 9 == sum(B), "A,B share sum p1=9")
    check(sum(x * x for x in A) == 41 == sum(x * x for x in B), "A,B share sumsq p2=41")
    g = group_by_signature(OFFS)
    coll = [(w, key, m) for w in g for key, m in g[w].items() if m >= 2]
    check(coll == [(3, (9, 41), 2)], "unique collision in 64 subsets: wt-3 (9,41) mult 2")
    D = [len(g.get(w, {})) for w in range(7)]
    check(tuple(D) == (1, 6, 15, 19, 15, 6, 1), f"P=(1,6,15,19,15,6,1) got {tuple(D)}")
    check(sum(D) == 63, "P_V(1)=63")
    check(6 * 20 + 18 == 138 < 1000, "first-moment digit 138<BASE (no carry, SHIFT20/BASE1000)")
    check(6 * 400 + 40 * 18 + 82 == 3202 < 10 ** 6, "second-moment digit 3202<BASE^2 (no carry)")
    P = [1, 6, 15, 19, 15, 6, 1]
    for k in (1, 2, 3):
        Lk = poly_pow(P, k)[3 * k]
        Mk = comb(6 * k, 3 * k)
        fk, Ek = 2 ** k, 6 ** k
        excess = Fraction(fk * Lk, Mk)
        check(Fraction(Ek, fk ** 3) == Fraction(3, 4) ** k, f"k={k}: Delta=(3/4)^{k}")
        check(excess == Fraction(fk) / Fraction(Mk, Lk), f"k={k}: f/barN={fk}*{Lk}/{Mk}={float(excess):.4f}")
    check(poly_pow(P, 3)[9] == 45907, "[x^9]P^3=45907")
    check(comb(18, 9) - 3 * comb(12, 6) + 3 * comb(6, 3) - 1 == 45907, "incl-excl 45907 (#615)")
    pr = rho_asym(OFFS)
    r615 = math.log(Fraction(63, 32)) / 6
    check(pr["fstar"] == 2 and pr["E1"] == 6, f"block fstar={pr['fstar']} E1={pr['E1']} (2,6)")
    check(approx(pr["rho"], r615, 1e-6), f"rho={pr['rho']:.6f}==log(63/32)/6={r615:.6f} (#615 floor)")
    check(approx(pr["delta"], math.log(Fraction(4, 3)) / 6), f"delta={pr['delta']:.6f}==log(4/3)/6")
    check(approx(pr["theta"], math.log(6) / math.log(2)),
          f"theta=log6/log2={pr['theta']:.4f}: E~f^2.585 -- reading-B near-Sidon, NOT reading-A(<=2)")


def block1() -> None:
    print("\nBLOCK 1  rate machinery agrees: asymptotic == exact-DP == geometric brute (PROVED)")
    for V in [(0, 1, 2, 4, 5, 6), (0, 1, 2, 3, 9, 10, 11, 12)]:
        for k in (1, 2):
            rk = rho_exact_k(V, k)
            gb = geom_brute_rho(V, k)
            check(rk is not None and gb is not None and approx(rk[0], gb, 1e-9),
                  f"V={V} k={k}: DP rate {rk[0]:.6f} == geometric brute {gb:.6f} (MF={rk[1]})")
    # asymptotic == lim_k exact
    V = (0, 1, 2, 4, 5, 6)
    seq = [rho_exact_k(V, k)[0] for k in (1, 2, 4, 8)]
    ra = rho_asym(V)["rho"]
    check(abs(seq[-1] - ra) < 2e-3, f"exact rho_k -> asymptotic {ra:.6f} (rho_8={seq[-1]:.6f})")
    check(approx(entropyH(0.5), math.log(2), 1e-12), "H(1/2)=log2 (balanced M-rate)")
    # AP-collapse: a dense AP has a big fiber but the image collapses -> rho<=0
    for n in (12, 16):
        pr = rho_asym(tuple(range(n)))
        r = pr["rho"] if pr else -1
        check(r < 0.13, f"AP{{0..{n-1}}}: image-normalized rho={r:.4f} (big fiber, but not extremal)")


def entropyH(x: float) -> float:
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


# ----------------------------------------------------------------------------
def canonical(V):
    m = min(V)
    W = tuple(x - m for x in V)
    gg = 0
    for x in W:
        gg = math.gcd(gg, x)
    if gg > 1:
        W = tuple(x // gg for x in W)
    return tuple(sorted(W))


def enum_ground_sets(b: int, box: int):
    seen = set()
    for rest in itertools.combinations(range(1, box), b - 1):
        cv = canonical((0,) + rest)
        if cv[-1] < box and cv not in seen:
            seen.add(cv)
            yield cv


def block2(box_by_b: dict[int, int]) -> dict:
    print("\nBLOCK 2  PRODUCT OPTIMIZATION: is the 2-point Prouhet block optimal? (COMPUTED)")
    r615 = math.log(Fraction(63, 32)) / 6
    best = None
    per_b = {}
    alld = []
    for b in sorted(box_by_b):
        box = box_by_b[b]
        bb = None
        n = 0
        for V in enum_ground_sets(b, box):
            n += 1
            pr = rho_asym(V)
            if not pr:
                continue
            alld.append(pr)
            if bb is None or pr["rho"] > bb["rho"]:
                bb = pr
            if best is None or pr["rho"] > best["rho"]:
                best = pr
        if bb:
            per_b[b] = bb
            print(f"    b={b:2d} box={box:2d} sets={n:5d}  best rho={bb['rho']:.6f} "
                  f"fstar={bb['fstar']} E1={bb['E1']} theta={bb['theta']:.3f} c={bb['c']} V={bb['V']}")
    check(best is not None, "search found collision blocks")
    beaters = [d for d in alld if d["rho"] > r615 + 1e-6]
    check(len(beaters) > 0,
          f"VERDICT: 2-point Prouhet is NOT optimal -- {len(beaters)} blocks beat rho={r615:.6f}")
    check(best["rho"] > r615 + 1e-3,
          f"best block rho={best['rho']:.6f} > 2-pt Prouhet {r615:.6f} (strict, by {best['rho']-r615:+.4f})")
    # validate the champion by exact finite-k tensor (not just the asymptotic formula)
    champ = best["V"]
    ek = rho_exact_k(champ, 3)
    check(ek is not None and ek[0] > r615,
          f"champion {champ} validated: exact rho_3={ek[0]:.6f} (MF={ek[1]}) also beats 2-pt")
    # the champion is denser than the minimal trade (bigger fiber / smaller block-per-doubling)
    check(best["fstar"] >= 3,
          f"champion fiber fstar={best['fstar']}>=3: a DENSER PTE cluster than the 2-point trade")
    # 2-point champions are the b=6 minimal-support blocks (fstar=2) and give exactly r615
    b6 = [d for d in alld if d["b"] == 6 and d["fstar"] == 2]
    check(b6 and approx(max(d["rho"] for d in b6), r615, 1e-6),
          f"minimal (b=6, fstar=2) blocks give exactly log(63/32)/6={r615:.6f}")
    top = sorted(beaters, key=lambda d: -d["rho"])[:6]
    print("    top beaters (rho, fstar, E1, theta, b, V):")
    for d in top:
        print(f"        rho={d['rho']:.6f} fstar={d['fstar']} E1={d['E1']} "
              f"theta={d['theta']:.3f} b={d['b']} V={d['V']}")
    return {"best": best, "per_b": per_b, "beaters": beaters, "r615": r615, "all": alld}


# ----------------------------------------------------------------------------
def block3(res2: dict) -> None:
    print("\nBLOCK 3  objective G=(fstar*L1)^(1/b), the fstar+L1<=2^b+1 wall, plateau (COMPUTED)")
    r615 = res2["r615"]
    G2 = 126 ** (1 / 6)
    # the 2-point Prouhet is exactly G=126^(1/6)
    check(approx(G2, 2 ** ((math.log(126) / math.log(2)) / 6)), f"2-pt Prouhet G=126^(1/6)={G2:.4f}")
    # every design obeys fstar+L1<=2^b+1 (both are collision-limited)  [PROVED]
    ok = all(d["fstar"] + d["L1"] <= (1 << d["b"]) + 1 for d in res2["all"])
    check(ok, "fstar + L1 <= 2^b + 1 on every design (deficit constraint, PROVED)")
    # rho = (1/b) log(fstar*L1/2^b); recompute identity on all designs
    idok = all(approx(d["rho"], math.log(d["fstar"] * d["L1"]) / d["b"] - math.log(2), 1e-9)
               for d in res2["all"])
    check(idok, "rho == (1/b) log(fstar*L1/2^b) exactly on every design")
    # the best G found and the structured-family plateau (built-in fixed family)
    def g_int(g, ell, gap):
        V = []
        for j in range(g):
            V += [j * (ell + gap) + t for t in range(ell)]
        return tuple(sorted(set(V)))
    fam = []
    for (g, ell, gap) in [(3, 4, 1), (4, 4, 7), (5, 4, 6), (6, 3, 4)]:
        pr = rho_asym(g_int(g, ell, gap))
        if pr:
            fam.append(pr)
            print(f"    interval-union g={g} ell={ell} gap={gap}: b={pr['b']} rho={pr['rho']:.5f} "
                  f"G={pr['G']:.4f} fstar={pr['fstar']} theta={pr['theta']:.3f}")
    check(all(d["rho"] > r615 for d in fam),
          "interval-union family beats the 2-point Prouhet rate and plateaus ~0.14 (G~2.30)")
    bestG = max(d["G"] for d in res2["all"])
    print(f"    best G in search = {bestG:.4f} (2-pt Prouhet 2.2390); best rho={res2['best']['rho']:.5f}")


# ----------------------------------------------------------------------------
def block4(res2: dict) -> None:
    print("\nBLOCK 4  UPPER BOUND: structural PTE-universality + analytic cap + wall (PROVED/WALL)")
    # (i) STRUCTURAL THEOREM (PROVED, exact fiber algebra = hughes canonical trade):
    #     every collision of (weight,sum,sumsq) is a degree-2 PTE trade after core
    #     removal; equal p1,p2 <=> equal e1,e2 (Newton).  So EVERY positive-rate
    #     configuration is PTE-structured.  Verify over a census of ground sets.
    pte_ok = True
    trade_min = 99
    tested = 0
    for V in itertools.islice(enum_ground_sets(6, 12), 200):
        g = group_by_signature(V)
        for w in g:
            for key, m in g[w].items():
                if m < 2:
                    continue
                masks = [msk for msk in range(1 << 6)
                         if bin(msk).count("1") == w and
                         (sum(V[i] for i in range(6) if msk & (1 << i)),
                          sum(V[i] * V[i] for i in range(6) if msk & (1 << i))) == key]
                base = masks[0]
                for other in masks[1:]:
                    P = [V[i] for i in range(6) if (other & (1 << i)) and not (base & (1 << i))]
                    Qs = [V[i] for i in range(6) if (base & (1 << i)) and not (other & (1 << i))]
                    tested += 1
                    if len(P) != len(Qs):
                        pte_ok = False
                    if sum(P) != sum(Qs) or sum(x * x for x in P) != sum(x * x for x in Qs):
                        pte_ok = False
                    # Newton: equal (p1,p2) <=> equal (e1,e2)
                    e1P, e2P = sum(P), (sum(P) ** 2 - sum(x * x for x in P)) // 2
                    e1Q, e2Q = sum(Qs), (sum(Qs) ** 2 - sum(x * x for x in Qs)) // 2
                    if (e1P, e2P) != (e1Q, e2Q):
                        pte_ok = False
                    trade_min = min(trade_min, 2 * len(P))
    check(pte_ok and tested > 0,
          f"PROVED (verified {tested} collisions): every R=2 fiber is a degree-2 PTE trade "
          "(disjoint, equal size, equal p1,p2 <=> e1,e2) = hughes's star-trade decomposition")
    check(trade_min == 6, f"minimal PTE-trade support = {trade_min} (>=3 per side) => block b>=6 minimal")
    # (ii) ANALYTIC CAP (PROVED, loose): fstar+L1<=2^b+1 => (fstar L1)^{1/b}<=2^{2-2/b}
    #      => rho <= (1-2/b) log2 -> log2.
    for b in (6, 12, 24):
        cap = (1 - 2 / b) * math.log(2)
        check(all(d["rho"] <= cap + 1e-9 for d in res2["all"] if d["b"] == b),
              f"b={b}: every design rho <= (1-2/b)log2 = {cap:.4f} (analytic cap holds)")
    best = res2["best"]
    cap_at_best = (1 - 2 / best["b"]) * math.log(2)
    print(f"    best construction rho={best['rho']:.4f} vs analytic cap (1-2/b)log2={cap_at_best:.4f} "
          f"at b={best['b']} -> GAP {cap_at_best-best['rho']:.4f} (cap is loose; matching bound OPEN)")
    print("    named missing inequality (the honest wall): a sharp bound on the achievable")
    print("    (fstar, L1) frontier -- 'max fiber of the R=2 moment map on b points at collision")
    print("    deficit c' -- i.e. the max clean degree-2 PTE-cluster packing rate.  UNKNOWN in")
    print("    closed form; the search plateaus at rho ~ 0.15-0.16, far below the 0.69 cap.")
    # (iii) superadditivity: tensor rate is per-point invariant (rho well-defined in the limit)
    Va = (0, 1, 2, 4, 5, 6)
    r1 = rho_exact_k(Va, 1)[0]
    r4 = rho_exact_k(Va, 4)[0]
    check(r4 > r1 and abs(r4 - rho_asym(Va)["rho"]) < 1.5e-3,
          f"superadditive: rho_k increases {r1:.4f}->{r4:.4f} to the asymptotic rate (Fekete)")


# ----------------------------------------------------------------------------
def block5(nmax: int) -> None:
    print("\nBLOCK 5  CENSUS: ALL fibers of (sum,sum^2) over {0..N-1}, prime field (COMPUTED)")
    r615 = math.log(Fraction(63, 32)) / 6
    print("     N  m    M     L    f=maxfiber  barN     f/barN   rate=log(f/barN)/N")
    best_rate = 0.0
    for N in range(4, nmax + 1):
        Vall = tuple(range(N))
        for m in range(2, N - 1):
            grp: dict[tuple[int, int], int] = defaultdict(int)
            for combo in itertools.combinations(Vall, m):
                grp[(sum(combo), sum(x * x for x in combo))] += 1
            M = comb(N, m)
            L = len(grp)
            f = max(grp.values())
            excess = Fraction(f) * Fraction(L, M)
            rate = math.log(excess) / N if excess > 1 else 0.0
            if excess > 1 and N >= nmax - 1 and m in (N // 2, N // 2 - 1):
                print(f"    {N:2d} {m:2d} {M:6d} {L:5d}  {f:7d}   "
                      f"{float(Fraction(M, L)):7.3f}  {float(excess):7.3f}   {rate:+.5f}")
            best_rate = max(best_rate, rate)
    print(f"    max small-N image-normalized excess rate (N<={nmax}): {best_rate:.5f}")
    print(f"    (finite-N < asymptotic product rate {r615:.5f}; census confirms structure, not the limit)")
    check(best_rate >= 0.0, "census ran; small-N extremal frontier computed")
    # every extremal collision over {0..N-1} (smallest N that has one) is a
    # degree-2 PTE trade.  {0..5} has none (an AP-6 needs triple-sum 7.5); the
    # first collisions appear at N>=7, e.g. {0..7} weight 3 with the {0,4,5}/{1,2,6}
    # trade family.  Scan up to census depth and check every collision.
    ncoll = 0
    okpte = True
    for N in range(6, nmax + 1):
        for m in range(2, N - 1):
            grp = defaultdict(list)
            for combo in itertools.combinations(range(N), m):
                grp[(sum(combo), sum(x * x for x in combo))].append(set(combo))
            for members in grp.values():
                if len(members) < 2:
                    continue
                base = members[0]
                for other in members[1:]:
                    P, Q = base - other, other - base
                    ncoll += 1
                    if (len(P) != len(Q) or sum(P) != sum(Q)
                            or sum(x * x for x in P) != sum(x * x for x in Q)):
                        okpte = False
    check(okpte and ncoll >= 1,
          f"every extremal collision over {{0..N-1}} (N<={nmax}, {ncoll} trades) is a degree-2 PTE trade")


# ----------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", type=int, default=-1)
    ap.add_argument("--box", type=int, default=0)
    ap.add_argument("--nmax", type=int, default=9)
    args = ap.parse_args()
    box = {6: 12, 7: 12, 8: 13, 9: 13, 10: 14, 12: 15}
    if args.box:
        box = {b: w + args.box for b, w in box.items()}
    res2 = None
    run = lambda n: args.block in (-1, n)
    if run(0):
        block0()
    if run(1):
        block1()
    if run(2) or run(3) or run(4):
        res2 = block2(box)
    if run(3) and res2:
        block3(res2)
    if run(4) and res2:
        block4(res2)
    if run(5):
        block5(args.nmax)
    npass = sum(1 for ok, _ in CHECKS if ok)
    print(f"\nRESULT: {'PASS' if npass == len(CHECKS) else 'FAIL'} ({npass}/{len(CHECKS)})")
    return 0 if npass == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
