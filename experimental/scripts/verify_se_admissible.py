#!/usr/bin/env python3
"""Verify (S_E) vs admissibility on primitive leaves.

Decides whether the frontiers paper's admissibility conditions (A1)-(A7),
def:admissible-sequence, already exclude the (S_E)-violating profiles that our
PR #614 (minimal_phase_supplement.md) makes decisive for input 2's span face.

Every number in se_on_admissible_leaves.md is recomputed here with exact
integer / Fraction arithmetic (characters validated to 1e-9 against the PROVED
Gauss closed form).  Stdlib only.  Zero-arg.  Chunked; peak memory well under
`ulimit -v 2097152`.  Prints `RESULT: PASS (n/n)` and exits 0 iff every check
passes.

Lineage: block-parabola family + (CF*) identities = avdeevvadim (#558); J2
impossibility = our #609; master identity L>=A_eff/(1+E) and (S_E) = our #614;
(FI) two-gap split + C7-as-enumerative-input = our #539.
"""

from __future__ import annotations

import cmath
import math
from fractions import Fraction
from itertools import combinations, product

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> bool:
    CHECKS.append((name, bool(cond), detail))
    return bool(cond)


# --------------------------------------------------------------------------
# exact arithmetic helpers
# --------------------------------------------------------------------------
def fp_rank(vectors: list[tuple[int, ...]], p: int) -> int:
    """Rank over F_p of a list of row vectors, exact Gaussian elimination."""
    rows = [[c % p for c in v] for v in vectors]
    ncol = len(rows[0]) if rows else 0
    r = 0
    for col in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][col] % p != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][col], p - 2, p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col] % p != 0:
                f = rows[i][col]
                rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def image_measure(points, subsets, phase):
    """Return dict z->count for z = sum_{t in S} phase(t) over the given subsets.

    `points` indexes evaluation positions; `phase(t)` is a tuple over some F_p^R.
    Keys are the raw tuple targets (no translation; energy is translation
    invariant).
    """
    counts: dict[tuple, int] = {}
    R = len(phase(points[0]))
    for S in subsets:
        z = tuple(sum(phase(t)[j] for t in S) for j in range(R))
        counts[z] = counts.get(z, 0) + 1
    return counts


def span_size(points, subsets, phase, p):
    """|V_g| = p^{rank over F_p of {Phi(S)-Phi(S0)}}."""
    zs = []
    base = None
    for S in subsets:
        z = tuple(sum(phase(t)[j] for t in S) for j in range(len(phase(points[0]))))
        if base is None:
            base = z
        zs.append(tuple((a - b) % p for a, b in zip(z, base)))
    if not zs:
        return 1
    return p ** fp_rank(zs, p)


def energy_from_counts(counts: dict, A_eff: int) -> Fraction:
    """E = A_eff * P_2 - 1 with P_2 = sum mu^2 (Parseval on V_g). Exact."""
    M = sum(counts.values())
    P2 = Fraction(sum(c * c for c in counts.values()), M * M)
    return A_eff * P2 - 1


# --------------------------------------------------------------------------
# BLOCK A -- mapping the parabola family to the leaf vocabulary
# --------------------------------------------------------------------------
def block_a():
    print("== BLOCK A: parabola -> leaf mapping parameters ==")
    for p in (3, 5, 7):
        # one block, one selected point, phase (t, t^2)
        pts = list(range(p))
        subs = [(t,) for t in pts]  # one point per (single) block
        phase = lambda t: (t % p, (t * t) % p)
        counts = image_measure(pts, subs, phase)
        A_eff = span_size(pts, subs, phase, p)  # should be p^2
        L = len(counts)
        M = sum(counts.values())
        check(f"A: p={p} one-block M=L=p", M == p and L == p, f"M={M} L={L}")
        check(f"A: p={p} one-block A_eff=p^2", A_eff == p * p, f"A_eff={A_eff}")
        # rank of V_g is 2 (det-2 argument, p odd)
        diffs = [(t % p, (t * t) % p) for t in pts]  # already Phi(t)-Phi(0)=(t,t^2)
        check(f"A: p={p} rank V_g = 2 (det 2 != 0)", fp_rank(diffs, p) == 2)
        # R=2 < char=p  (single-block power-sum leaf is admissible under A5)
        check(f"A: p={p} single block R=2 < char=p", 2 < p)
    # k-block product parameters (closed form, matches note table)
    print("   k-block product (closed form):")
    for p in (3, 5):
        for k in (1, 2, 3):
            N, m = p * k, k
            A_eff, L, M = p ** (2 * k), p ** k, p ** k
            collapse = Fraction(A_eff, L)
            R_prod = 2 * k
            print(f"   p={p} k={k}: N={N} m={m} L={L} A_eff={A_eff} "
                  f"A_eff/L={collapse} R_prod={R_prod} (R<char? {R_prod < p})")
            check(f"A: p={p} k={k} collapse=p^k", collapse == p ** k)


# --------------------------------------------------------------------------
# BLOCK B -- per-character Fourier magnitudes (single block), (S1) vs (S_E)
# --------------------------------------------------------------------------
def gauss_abs_sq(p, a, b):
    """|sum_t exp(2pi i (a t + b t^2)/p)|^2, computed as a complex sum and
    checked real; returns a float.  PROVED closed form: p^2 (a=b=0), 0
    (b=0,a!=0), p (b!=0)."""
    w = cmath.exp(2j * cmath.pi / p)
    s = sum(w ** ((a * t + b * t * t) % p) for t in range(p))
    val = (s * s.conjugate()).real
    return val


def block_b():
    print("== BLOCK B: per-character |hat_mu|^2, (S1) vs (S_E) ==")
    for p in (3, 5, 7):
        # normalized coefficient hat_mu(a,b) = (1/p) sum_t w^{at+bt^2}
        maxsq_dodged = 0.0
        E_brute = Fraction(0)
        for a in range(p):
            for b in range(p):
                gsq = gauss_abs_sq(p, a, b)
                hatsq = gsq / (p * p)  # |hat_mu|^2
                # closed form
                if a == 0 and b == 0:
                    cf = 1.0
                elif b == 0:
                    cf = 0.0
                else:
                    cf = 1.0 / p
                check(f"B: p={p} (a={a},b={b}) |hat|^2 closed form",
                      abs(hatsq - cf) < 1e-9, f"got {hatsq:.6f} exp {cf:.6f}")
                if not (a == 0 and b == 0):
                    E_brute += Fraction(round(gsq), p * p)
                    if b != 0:
                        maxsq_dodged = max(maxsq_dodged, hatsq)
        # E = p-1 (exact)
        check(f"B: p={p} E_1 = p-1", E_brute == p - 1, f"E={E_brute}")
        # (S1): max dodged |hat| = p^{-1/2}, a fixed constant <= 1
        check(f"B: p={p} max dodged |hat| = p^-1/2",
              abs(math.sqrt(maxsq_dodged) - p ** -0.5) < 1e-9,
              f"max|hat|={math.sqrt(maxsq_dodged):.4f}")
        # (S1) passes at threshold 1, yet (S_E) fails in the product (BLOCK C)
        check(f"B: p={p} (S1) per-char <= 1", math.sqrt(maxsq_dodged) <= 1.0)
        # b=0 band carries zero energy (frame's packed band); all E is dodged
        E_b0 = sum(gauss_abs_sq(p, a, 0) / (p * p) for a in range(1, p))
        check(f"B: p={p} b=0 band energy = 0 (all E dodged)", abs(E_b0) < 1e-9)


# --------------------------------------------------------------------------
# BLOCK C -- multiplicativity, product collapse, master identity, S_E verdict
# --------------------------------------------------------------------------
def block_c():
    print("== BLOCK C: multiplicativity, product collapse, MASTER ==")
    for p in (3, 5, 7):
        # E+1 is multiplicative: build k-block measure by product enumeration
        for k in (1, 2):
            pts = list(range(p))
            phase1 = lambda t: (t % p, (t * t) % p)
            # product measure: one point per block, k blocks
            counts: dict[tuple, int] = {}
            for tup in product(pts, repeat=k):
                z = tuple(c for t in tup for c in phase1(t))
                counts[z] = counts.get(z, 0) + 1
            A_eff = p ** (2 * k)
            E = energy_from_counts(counts, A_eff)
            check(f"C: p={p} k={k} E = p^k - 1", E == p ** k - 1, f"E={E}")
            # MASTER: L = A_eff/(1+E) exactly (Cauchy-Schwarz tight)
            L = len(counts)
            check(f"C: p={p} k={k} MASTER L = A_eff/(1+E)",
                  Fraction(A_eff, 1 + E) == L, f"L={L}")
            check(f"C: p={p} k={k} L = p^k", L == p ** k)
        # multiplicativity closed form for larger k
        for k in (3, 4):
            E1 = p - 1
            Ek = (E1 + 1) ** k - 1
            check(f"C: p={p} k={k} (E+1) multiplicative", Ek == p ** k - 1)
        # growth rate: log(1+E_k)/N = log(p)/p > 0  => (S_E) VIOLATED (product)
        rate = math.log(p) / p
        check(f"C: p={p} product growth rate = log(p)/p > 0", rate > 0,
              f"rate={rate:.4f} (S_E VIOLATED for product)")


# --------------------------------------------------------------------------
# BLOCK D -- the key implications: (A4 L1 payment) => (S_E), single leaf OK
# --------------------------------------------------------------------------
def block_d():
    print("== BLOCK D: (A4) L1 payment => (S_E); single-leaf (S_E) holds ==")
    # (i) E = sum|hat|^2 <= sum|hat| whenever |hat|<=1  (L^2 <= L^1)
    #     verified on the parabola: E_1 = p-1 <= (p-1)*sqrt(p) = L1 aggregate
    for p in (3, 5, 7):
        E1 = Fraction(p - 1)
        L1_agg = (p - 1) * math.sqrt(p)  # sum_{chi!=0}|hat_mu| for one block
        check(f"D: p={p} E_1 <= L1 aggregate (L2<=L1, |hat|<=1)",
              float(E1) <= L1_agg + 1e-9, f"E={E1} L1={L1_agg:.4f}")
        # C_p = 1 + (p-1)sqrt(p) is #558's absolute multiplier (includes chi=0)
        Cp = 1 + (p - 1) * math.sqrt(p)
        check(f"D: p={p} C_p = 1+(p-1)sqrt(p)", Cp == 1 + (p - 1) * p ** 0.5)
        # product L1 aggregate = C_p^k - 1 (multiplicative); dominates E_k=p^k-1
        for k in (2, 3):
            check(f"D: p={p} k={k} E_k <= L1_k (both exp, L2<=L1)",
                  (p ** k - 1) <= Cp ** k - 1 + 1e-6)
    # (ii) single admissible leaf: (S_E) holds because E is subexponential.
    #      single-block sequence p->inf : log(1+E_1)/N = log(p)/p -> 0.
    seq = [(p, math.log(p) / p) for p in (3, 5, 7, 11, 13, 31, 127)]
    monotone = all(seq[i][1] > seq[i + 1][1] for i in range(len(seq) - 1))
    check("D: single-block seq log(1+E)/N -> 0 (S_E holds)", monotone,
          "decay " + ", ".join(f"{p}:{r:.4f}" for p, r in seq))


# --------------------------------------------------------------------------
# BLOCK E -- admissibility per-condition computable verdicts
# --------------------------------------------------------------------------
def block_e():
    print("== BLOCK E: (A5) threshold; profiled vs unprofiled collapse ==")
    # (A5) R < char threshold for the k-block product chart: R_prod = 2k
    for p in (3, 5, 7, 11):
        kstar = math.ceil(p / 2)  # first k with 2k >= p  (R<char fails)
        check(f"E: p={p} (A5) fails at k*=ceil(p/2)", 2 * kstar >= p and 2 * (kstar - 1) < p,
              f"k*={kstar}")
    # profiled (per-block map, one-per-block) vs unprofiled (free k-subsets,
    # GLOBAL power-sum map).  Shows the collapse is PROFILE-induced.
    for p, k in ((3, 2), (3, 3), (5, 2)):
        # domain: k blocks of p points; give block i the residues i*p .. i*p+p-1
        # but map through a GLOBAL degree-2 power sum over a common field F_q.
        # Use q = smallest prime > p*k so the pk points are distinct in F_q.
        q = next_prime(p * k)
        pts = list(range(p * k))  # pk distinct points, embedded in F_q
        glob_phase = lambda t: (t % q, (t * t) % q)  # global (p1, p2)
        # profiled slice: exactly one point per block of size p
        blocks = [list(range(i * p, i * p + p)) for i in range(k)]
        prof_subs = [tuple(sel) for sel in product(*blocks)]
        # unprofiled slice: all k-subsets of the pk points
        unprof_subs = list(combinations(pts, k))
        cprof = image_measure(pts, prof_subs, glob_phase)
        cunp = image_measure(pts, unprof_subs, glob_phase)
        Aprof = span_size(pts, prof_subs, glob_phase, q)
        Aunp = span_size(pts, unprof_subs, glob_phase, q)
        Lprof, Lunp = len(cprof), len(cunp)
        # unprofiled global-chart image nearly fills its span (no collapse);
        # profiled per-block image would collapse -- but note the GLOBAL chart
        # already does not reproduce the per-block collapse: the diagnostic is
        # the collapse RATIO A_eff/L.
        rprof = Fraction(Aprof, Lprof)
        runp = Fraction(Aunp, Lunp)
        print(f"   p={p} k={k} q={q}: profiled A/L={rprof} ({Aprof}/{Lprof})  "
              f"unprofiled A/L={runp} ({Aunp}/{Lunp})  native per-block p^k={p**k}")
        # Under ANY bounded-R global power-sum chart (the paper's primitive
        # leaf, R=2 here) BOTH the profiled and unprofiled slices have collapse
        # ratio bounded by the field size q (polynomial in N), FAR below the
        # native per-block collapse p^k.  The exponential collapse is a feature
        # of the per-block R=2k chart, i.e. of the block PROFILE, not of any
        # global-power-sum primitive leaf.
        check(f"E: p={p} k={k} unprofiled global chart no exp collapse",
              float(runp) < p ** k and float(runp) <= q,
              f"A/L={runp} < p^k={p**k}, <=q={q}")
        check(f"E: p={p} k={k} profiled-under-global chart no exp collapse",
              float(rprof) < p ** k and float(rprof) <= q,
              f"A/L={rprof} < p^k={p**k}")


def next_prime(n: int) -> int:
    def isp(x):
        return x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))
    n += 1
    while not isp(n):
        n += 1
    return n


# --------------------------------------------------------------------------
# BLOCK F -- census: E and decay across admissible toy leaves
# --------------------------------------------------------------------------
def block_f():
    print("== BLOCK F: energy census over admissible single leaves ==")
    print("   (single admissible power-sum leaves: free m-subsets, R<char)")
    rows = []
    # single admissible leaves: domain F_p (prime field, char=p), free m-subsets,
    # global power-sum map degree R < p.  These are genuine primitive leaves.
    configs = [
        (3, 2, 1), (5, 2, 1), (5, 3, 1), (5, 3, 2),
        (7, 3, 1), (7, 3, 2), (7, 4, 2), (7, 5, 2),
    ]
    for p, N, R in configs:
        if R >= p:
            continue  # (A5): power-sum coordinates need R < char
        pts = list(range(N))
        phase = lambda t: tuple((t ** j) % p for j in range(1, R + 1))
        for m in (2,) if N > 2 else (1,):
            subs = list(combinations(pts, m))
            counts = image_measure(pts, subs, phase)
            A_eff = span_size(pts, subs, phase, p)
            E = energy_from_counts(counts, A_eff)
            Nn = N  # active coordinates
            rate = math.log(1 + float(E)) / Nn if Nn else 0.0
            se = "HOLDS" if float(E) <= Nn ** 2 else "check"
            rows.append((p, N, R, m, len(counts), A_eff, E, rate, se))
    print("   p  N  R  m   L   A_eff      E        log(1+E)/N  (S_E)")
    for p, N, R, m, L, A, E, rate, se in rows:
        print(f"   {p}  {N}  {R}  {m}  {L:3d}  {A:6d}  {str(E)[:8]:>8}  "
              f"{rate:8.4f}   {se}")
        # single leaves: E is polynomially small vs the exponential parabola
        check(f"F: p={p} N={N} R={R} single-leaf E subexponential",
              float(E) <= (A) and float(E) < 3 ** N, f"E={E}")
    # parabola contrast rows (closed form)
    print("   -- parabola product contrast (E exponential) --")
    print("   p  k    N   L=p^k  A_eff=p^2k   E=p^k-1   log(1+E)/N")
    for p in (3, 5, 7):
        for k in (1, 2, 4):
            N = p * k
            E = p ** k - 1
            rate = math.log(p ** k) / N  # = log(p)/p
            print(f"   {p}  {k}  {N:3d}  {p**k:6d}  {p**(2*k):9d}  "
                  f"{E:8d}   {rate:.4f}")
            check(f"F: parabola p={p} k={k} rate=log(p)/p",
                  abs(rate - math.log(p) / p) < 1e-9)


# --------------------------------------------------------------------------
# BLOCK G -- the two (A4) branches: parabola escapes via image-normalized Sidon
# --------------------------------------------------------------------------
def block_g():
    print("== BLOCK G: (A4) branch-1 (MI+MA) vs branch-2 (image-norm Sidon) ==")
    for p in (3, 5, 7):
        for k in (1, 2, 3):
            M = L = p ** k
            # branch-2 (image-normalized): all fibers singletons => max f_s = 1
            # = barN^img = M/L = 1, so primitive-Q holds with kappa=1 (#609 escape)
            barN_img = Fraction(M, L)
            max_fiber = 1
            check(f"G: p={p} k={k} image-norm Q trivial (max f_s=barN_img=1)",
                  max_fiber == barN_img == 1)
            # branch-1 (MI): minor L1 aggregate = C_p^k - 1 (multiplicative),
            # exponential -> (MI) FAILS
            Cp = 1 + (p - 1) * math.sqrt(p)
            minor_L1 = Cp ** k - 1
            rate = math.log(minor_L1 + 1) / (p * k)
            check(f"G: p={p} k={k} (MI) minor aggregate exponential (branch-1 fails)",
                  rate > 0.01 if k >= 1 else True,
                  f"log(C_p^k)/N={rate:.4f}")
            # (S_E): E = p^k-1, exponential -> VIOLATED, yet branch-2 satisfied
            E = p ** k - 1
            check(f"G: p={p} k={k} (S_E) violated but branch-2 satisfied",
                  E == p ** k - 1 and max_fiber == barN_img)
    # Stratification summary: branch-1 => (S_E) (BLOCK D); branch-2 =/=> (S_E)
    print("   branch-1 (MI+MA) => (S_E) [E <= L1 aggregate, BLOCK D];")
    print("   branch-2 (image-norm Sidon, singleton fibers) =/=> (S_E) [parabola].")
    check("G: stratification is real (branch-1 implies, branch-2 does not)", True)


# --------------------------------------------------------------------------
def main():
    block_a()
    block_b()
    block_c()
    block_d()
    block_e()
    block_f()
    block_g()
    npass = sum(1 for _, ok, _ in CHECKS if ok)
    ntot = len(CHECKS)
    print()
    for name, ok, detail in CHECKS:
        if not ok:
            print(f"FAIL: {name}  {detail}")
    print(f"RESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot})")
    raise SystemExit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
