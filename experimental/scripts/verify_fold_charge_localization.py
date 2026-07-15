#!/usr/bin/env python3
r"""Verifier: fold-level charge triviality + flat-cube reduction on the Sidon-paired class (hard input 2).

Checks, per the note experimental/notes/thresholds/fold_charge_localization.md:

V1  Theorem A instances (fold pieces are ell^2-charge-trivial): brute class
    structure at B in {4,6}, both bases, maximal band, unnormalized weights
    h_+ = (f - M/c)_+ (exact Fractions): for round-robin K-block coarsenings
    of the parity fold, K * sum_i ||b_i||_2^2 < Omega~_+^2 for every
    K in {2,4,16} BELOW the participation number PN (the exact regime of the
    theorem: fold blocks have sum_i ||b_i||_2^2 == sum_sigma f^2 h_+^2
    independent of the blocking, so unsatisfiability is exactly K < PN); the
    multiplicity bound sum_i ||b_i||_2^2 <= f_max^2 sum_sigma h_+^2 (exact);
    and the rate ingredient f_max^2 L < M^2 (integers, even B <= 64).
V2  Theorem B (exact charge ledger): level shares
    Omega~_+(s) = C(B,s) 2^s w_s (w_s - M/c)_+ pinned at B in {6,8} (exact,
    scaled by c); zero-share levels == {s : w_s <= M/c} for even B <= 64
    (base 3); on base 5 EVERY level is heavy (M/c -> 0: no light threshold)
    while the argmax stays in the sigma = 1/3 window (B in {6,12,24});
    ledger argmax s* with |s*/B - 1/3| <= 1/12 + 2/B for even 6 <= B <= 96;
    away-mass sum_{|s/B-1/3| >= 1/6} share decreasing along B = 8,16,32,64
    and < 2^{-6} at B = 64 (exact rationals); the light-threshold trend
    min{s : w_s <= M/c}/B within 0.05 of 1 - log2(4/3) at B in {32,64,96}
    with the deviation decreasing (the limit is exact; the O(log B / B)
    correction is visible at these sizes).
V3  #776-window erratum witnesses: at B in {6,8} the exact set
    {s : w_s < 2M/L} (= {4,6} / {4,6,8}) is nonempty although the integrated
    transverse-charge note's Sec-5 prose asserts every fiber >= 2M/L; the
    upper end (all fibers < M/sqrt(L), i.e. w_s^2 L < M^2) IS universal
    (all levels, even B <= 64).  Nothing there consumes the lower end
    universally (existence f_max L >= 2M is re-verified, even B <= 64).
V4  Theorem C (maximal-band cube flatness + participation): h is EXACTLY
    constant on each class's syndrome set (brute, B in {4,6}, both bases);
    the squared identity (class ell^1)^2 == 2^s * (class ell^2)^2 is
    computed from PER-SYNDROME sums, so it is a Cauchy-Schwarz-equality
    witness of that constancy, not a restatement; the participation number
    PN(B) = Omega~_+^2 / sum_sigma f^2 h_+^2 (exact rationals via closed
    level sums) is pinned at B in {6,8,16,32} and at least doubles at each
    step (exponential-growth witness); any ell^2-capped scheme with
    K < PN(B) pieces cannot pay (Cauchy-Schwarz), checked as exact
    cross-multiplied unsatisfiability at B in {6,8,16,32} for K = 2^{B/2}.
V5  Theorem D (bridge identity, floats + Parseval guard): at B = 6, BOTH
    bases, for EVERY class at every level s >= 2 and EVERY pattern
    D subseteq U: the brute sign-cube Fourier coefficient of h on the class
    equals (1/c) sum_xi hatf(xi) prod_{i in D}(-i sin theta_i(xi))
    prod_{i in U\D}(cos theta_i(xi)) (minus M/c at D = empty); coefficients
    vanish for D != empty (maximal band); hatf is Parseval-guarded
    (sum hatf^2 == c*M2 to 1e-6 rel).
V6  The reduction's easy direction (exact): the admissible levels as
    level-block pieces are fold-measurable, disjoint, at most B/2 + 1 many,
    each level is uniform (all its classes carry identical
    (2^s, w_s, h-value) data; brute), and their ell^1 charges sum to
    Omega~_+ EXACTLY (Fractions).
V7  Cross-consistency: class/fiber structure recomputed here matches the
    resonant-folding closed forms (N_v, M2); distinct classes have DISJOINT
    syndrome sets (union count == sum of per-class counts, brute); and the
    integrated pins hold (M2 = 3584 / 97444 at B = 6 / 8).

Deterministic, stdlib only.  --tamper-selftest mutates five load-bearing
pieces and verifies each is caught.  --emit-certificate PATH writes JSON.
"""
import sys
from fractions import Fraction
from math import comb, cos, sin, pi, sqrt
from itertools import combinations
from collections import defaultdict

CHECKS = []
QUIET = False


def check(name, ok):
    CHECKS.append((name, bool(ok)))
    if not ok and not QUIET:
        print(f"FAIL: {name}")
    return ok


# ---------------------------------------------------------------- class data

def sidon_P(B, base):
    return [base ** i for i in range(B)]


def sidon_c(B, base):
    return 2 * sum(sidon_P(B, base)) + 1


def fiber_w(B, s):
    """Within-class fiber size w_s = C(B-s,(B-s)/2)."""
    return comb(B - s, (B - s) // 2)


def closed_M(B):
    return comb(2 * B, B)


def closed_M2(B):
    return sum(comb(B, s) * 2 ** s * fiber_w(B, s) ** 2
               for s in range(B % 2, B + 1, 2))


def closed_L(B):
    return (3 ** B + 1) // 2 if B % 2 == 0 else (3 ** B - 1) // 2


def ledger_term(B, s, c):
    """Omega~_+(s) = C(B,s) 2^s w_s (w_s - M/c)_+, exact Fraction."""
    ws = fiber_w(B, s)
    hp = Fraction(ws) - Fraction(closed_M(B), c)
    if hp <= 0:
        return Fraction(0)
    return comb(B, s) * 2 ** s * ws * hp


def sq_term(B, s, c):
    """sum over level-s syndromes of f^2 h_+^2 = C(B,s) 2^s w^2 (w-M/c)_+^2."""
    ws = fiber_w(B, s)
    hp = Fraction(ws) - Fraction(closed_M(B), c)
    if hp <= 0:
        return Fraction(0)
    return comb(B, s) * 2 ** s * ws ** 2 * hp ** 2


def brute_classes(B, base):
    """{v: {sigma: count}} by raw enumeration."""
    P = sidon_P(B, base)
    c = sidon_c(B, base)
    T = P + [c - p for p in P]
    pairs = [(P[i], c - P[i]) for i in range(B)]
    out = defaultdict(lambda: defaultdict(int))
    for S in combinations(T, B):
        Sset = set(S)
        v = tuple(((pairs[i][0] in Sset) + (pairs[i][1] in Sset)) % 2
                  for i in range(B))
        out[v][sum(S) % c] += 1
    return out


# ------------------------------------------------------------ V1 -- Thm A

def v1_fold_triviality(cert=None):
    ok_rate = all(comb(B, B // 2) ** 2 * closed_L(B) < closed_M(B) ** 2
                  for B in range(4, 65, 2))
    check("V1 rate ingredient f_max^2 L < M^2, even 4 <= B <= 64", ok_rate)
    for base in (3, 5):
        for B in (4, 6):
            cls = brute_classes(B, base)
            c = sidon_c(B, base)
            M = closed_M(B)
            Mc = Fraction(M, c)
            hp = {}
            for v, fib in cls.items():
                for sig, n in fib.items():
                    x = Fraction(n) - Mc
                    hp[sig] = x if x > 0 else Fraction(0)
            omega = sum(Fraction(n) * hp[sig]
                        for v, fib in cls.items() for sig, n in fib.items())
            sum_h2 = sum(x * x for x in hp.values())
            fmax = comb(B, B // 2)
            classes = sorted(cls.keys(), key=lambda v: (sum(v), v))
            sq_all = sum((Fraction(n) * hp[sig]) ** 2
                         for v in classes for sig, n in cls[v].items())
            pn = omega * omega / sq_all
            ok_unsat, ok_mult, tested = True, True, 0
            for K in (2, 4, 16):
                blocks = [classes[i::K] for i in range(K)]
                s2 = Fraction(0)
                for blk in blocks:
                    s2 += sum((Fraction(n) * hp[sig]) ** 2
                              for v in blk for sig, n in cls[v].items())
                if s2 != sq_all:
                    ok_mult = False   # blocking must not change the ell^2 mass
                if not s2 <= fmax * fmax * sum_h2:
                    ok_mult = False
                if Fraction(K) < pn:
                    tested += 1
                    if not K * s2 < omega * omega:
                        ok_unsat = False
                elif K * s2 < omega * omega:
                    ok_unsat = False   # K >= PN must NOT be unsatisfiable
                if cert is not None and base == 3 and B == 6:
                    cert["fold_coarsening"][f"K{K}"] = \
                        f"{float(K * s2 / (omega * omega)):.6f}"
            check(f"V1 coarsening unsatisfiable iff K < PN, K in {{2,4,16}}, >=2 tested below PN (B={B}, base {base})",
                  ok_unsat and tested >= 2)
            check(f"V1 blocking-invariant ell^2 mass, <= f_max^2 sum h_+^2 (B={B}, base {base})",
                  ok_mult)


# ------------------------------------------------------------ V2 -- Thm B

def v2_ledger(cert=None):
    for B in (6, 8):
        c = 3 ** B
        tot = sum(ledger_term(B, s, c) for s in range(B % 2, B + 1, 2))
        shares = {s: ledger_term(B, s, c) / tot
                  for s in range(B % 2, B + 1, 2)}
        if B == 6:
            check("V2 ledger pinned B=6: shares (.1542/.7011/.1447/0) at s=(0/2/4/6)",
                  abs(float(shares[0]) - 0.1542) < 5e-4
                  and abs(float(shares[2]) - 0.7011) < 5e-4
                  and abs(float(shares[4]) - 0.1447) < 5e-4
                  and shares[6] == 0)
        if cert is not None:
            cert["ledger_shares"][str(B)] = {
                str(s): f"{float(x):.4f}" for s, x in shares.items()}
    ok_zero = True
    for B in range(4, 65, 2):
        c = 3 ** B
        Mc = Fraction(closed_M(B), c)
        zero = {s for s in range(0, B + 1, 2) if ledger_term(B, s, c) == 0}
        light = {s for s in range(0, B + 1, 2) if Fraction(fiber_w(B, s)) <= Mc}
        if zero != light:
            ok_zero = False
    check("V2 zero-share levels == {s : w_s <= M/c}, even B <= 64", ok_zero)
    ok_loc = True
    for B in range(6, 97, 2):
        c = 3 ** B
        smax = max(range(0, B + 1, 2), key=lambda s: ledger_term(B, s, c))
        if abs(smax / B - 1 / 3) > 1 / 12 + 2 / B:
            ok_loc = False
        if cert is not None and B in (6, 8, 16, 32, 64, 96):
            cert["ledger_argmax"][str(B)] = smax
    check("V2 ledger argmax |s*/B - 1/3| <= 1/12 + 2/B, even 6 <= B <= 96", ok_loc)
    prev = None
    ok_away, ok_last = True, None
    for B in (8, 16, 32, 64):
        c = 3 ** B
        tot = sum(ledger_term(B, s, c) for s in range(0, B + 1, 2))
        away = sum(ledger_term(B, s, c) for s in range(0, B + 1, 2)
                   if abs(Fraction(s, B) - Fraction(1, 3)) >= Fraction(1, 6))
        frac = away / tot
        if prev is not None and not frac < prev:
            ok_away = False
        prev = frac
        ok_last = frac
        if cert is not None:
            cert["away_mass"][str(B)] = f"{float(frac):.6f}"
    check("V2 away-mass (|s/B-1/3| >= 1/6) strictly decreasing along B = 8,16,32,64",
          ok_away)
    check("V2 away-mass < 2^{-6} at B = 64", ok_last < Fraction(1, 64))
    ok_thr, prev_dev = True, None
    for B in (32, 64, 96):
        c = 3 ** B
        Mc = Fraction(closed_M(B), c)
        smin = min(s for s in range(0, B + 1, 2)
                   if Fraction(fiber_w(B, s)) <= Mc)
        dev = abs(smin / B - (1 - 0.4150374992788438))
        if dev > 0.05 or (prev_dev is not None and dev > prev_dev):
            ok_thr = False
        prev_dev = dev
    check("V2 light-threshold min{s: w_s <= M/c}/B within .05 of 1 - log2(4/3), deviation non-increasing, B in {32,64,96}",
          ok_thr)
    ok_b5 = True
    for B in (6, 12, 24):
        c5 = sidon_c(B, 5)
        Mc5 = Fraction(closed_M(B), c5)
        if any(Fraction(fiber_w(B, s)) <= Mc5 for s in range(0, B + 1, 2)):
            ok_b5 = False
        smax = max(range(0, B + 1, 2), key=lambda s: ledger_term(B, s, c5))
        if abs(smax / B - 1 / 3) > 1 / 12 + 2 / B:
            ok_b5 = False
    check("V2 base 5: EVERY level heavy (M/c -> 0, no light threshold) and ledger argmax in the sigma=1/3 window, B in {6,12,24}",
          ok_b5)


# ---------------------------------------------------- V3 -- window erratum

def v3_erratum(cert=None):
    expect = {6: {4, 6}, 8: {4, 6, 8}}
    for B in (6, 8):
        L, M = closed_L(B), closed_M(B)
        below = {s for s in range(0, B + 1, 2)
                 if fiber_w(B, s) * L < 2 * M}
        check(f"V3 erratum witnesses: {{s : w_s < 2M/L}} == {sorted(expect[B])} (B={B})",
              below == expect[B])
        if cert is not None:
            cert["erratum_below_2ML"][str(B)] = sorted(below)
    ok_upper = all(fiber_w(B, s) ** 2 * closed_L(B) < closed_M(B) ** 2
                   for B in range(4, 65, 2) for s in range(0, B + 1, 2))
    check("V3 upper end universal: w_s^2 L < M^2, ALL levels, even B <= 64", ok_upper)
    ok_exist = all(comb(B, B // 2) * closed_L(B) >= 2 * closed_M(B)
                   for B in range(4, 65, 2))
    check("V3 existence f_max L >= 2M re-verified, even B <= 64", ok_exist)


# ------------------------------------------------------------ V4 -- Thm C

def participation(B):
    """PN(B) = Omega~_+^2 / sum f^2 h_+^2, exact Fraction (base 3)."""
    c = 3 ** B
    om = sum(ledger_term(B, s, c) for s in range(B % 2, B + 1, 2))
    sq = sum(sq_term(B, s, c) for s in range(B % 2, B + 1, 2))
    return om * om / sq


def v4_flatness_participation(cert=None):
    for base in (3, 5):
        for B in (4, 6):
            cls = brute_classes(B, base)
            c = sidon_c(B, base)
            M = closed_M(B)
            ok_const, ok_sq = True, True
            for v, fib in cls.items():
                s = sum(v)
                if len(set(fib.values())) != 1:
                    ok_const = False
                l1, l2sq = Fraction(0), Fraction(0)
                for _sig, n in fib.items():   # per-syndrome sums, NOT collapsed:
                    hp = Fraction(n) - Fraction(M, c)   # the squared identity below
                    if hp < 0:                          # is Cauchy-Schwarz EQUALITY,
                        hp = Fraction(0)                # true iff n*hp is constant
                    l1 += Fraction(n) * hp              # across the class's cube
                    l2sq += (Fraction(n) * hp) ** 2
                if l1 * l1 != 2 ** s * l2sq:
                    ok_sq = False
            check(f"V4 h constant on every class (fiber counts equal) (B={B}, base {base})",
                  ok_const)
            check(f"V4 class ell1^2 == 2^s * ell2^2 (flat-cube gap sqrt(2^s)) (B={B}, base {base})",
                  ok_sq)
    pins = {}
    for B in (6, 8, 16, 32):
        pins[B] = participation(B)
        if cert is not None:
            cert["participation"][str(B)] = f"{float(pins[B]):.3f}"
    check("V4 participation number at least doubles along B = 6,8,16,32",
          pins[8] > 2 * pins[6] and pins[16] > 2 * pins[8]
          and pins[32] > 2 * pins[16])
    ok_unsat = True
    for B in (6, 8, 16, 32):
        c = 3 ** B
        K = 2 ** (B // 2)
        om = sum(ledger_term(B, s, c) for s in range(0, B + 1, 2))
        sq = sum(sq_term(B, s, c) for s in range(0, B + 1, 2))
        if not (Fraction(K) < pins[B]) or not (K * sq < om * om):
            ok_unsat = False
    check("V4 ell2-capped schemes with K = 2^{B/2} pieces cannot pay (K*sum f^2h_+^2 < Omega~^2), B in {6,8,16,32}",
          ok_unsat)


# ------------------------------------------------------------ V5 -- Thm D

def hatf_scan(B, base):
    c = sidon_c(B, base)
    P = sidon_P(B, base)
    vals = []
    for j in range(c):
        poly = [1.0]
        for A in P:
            th = 2 * pi * ((j * A) % c) / c
            t = 2 * cos(th)
            new = [0.0] * (len(poly) + 2)
            for i, a in enumerate(poly):
                new[i] += a
                new[i + 1] += a * t
                new[i + 2] += a
            poly = new
        vals.append(poly[B])
    return c, P, vals


def v5_bridge(cert=None):
    B = 6
    for base in (3, 5):
        c, P, hf = hatf_scan(B, base)
        M = closed_M(B)
        check(f"V5 Parseval guard sum hatf^2 == c*M2 to 1e-6 rel (B=6, base {base})",
              abs(sum(x * x for x in hf) - c * closed_M2(B))
              <= 1e-6 * c * closed_M2(B))
        cls = brute_classes(B, base)
        maxdev, maxvanish = 0.0, 0.0
        for v, fib in cls.items():
            s = sum(v)
            if s == 0:
                continue
            U = [i for i in range(B) if v[i]]
            sigs = {}
            for bits in range(2 ** s):
                eps = [1 if (bits >> t) & 1 == 0 else -1 for t in range(s)]
                sigs[bits] = sum(e * P[U[t]] for t, e in enumerate(eps)) % c
            for dbits in range(2 ** s):
                brute = 0.0
                for bits, sig in sigs.items():
                    sgn = -1 if bin(bits & dbits).count("1") % 2 else 1
                    brute += sgn * (fib.get(sig, 0) - M / c)
                brute /= 2 ** s
                acc = complex(0.0)
                for xi in range(c):
                    prod = complex(1.0)
                    for t in range(s):
                        th = 2 * pi * ((xi * P[U[t]]) % c) / c
                        prod *= (-1j * sin(th)) if (dbits >> t) & 1 else cos(th)
                    acc += hf[xi] * prod
                acc /= c
                if dbits == 0:
                    acc -= M / c
                maxdev = max(maxdev, abs(acc - brute))
                if dbits != 0:
                    maxvanish = max(maxvanish, abs(brute))
        check(f"V5 bridge identity brute == theta-product formula, ALL classes/patterns (B=6, base {base})",
              maxdev <= 1e-8 * M)
        check(f"V5 cube spectrum vanishes off D=empty (maximal band) (B=6, base {base})",
              maxvanish <= 1e-9 * M)
        if cert is not None:
            cert["bridge_maxdev"][f"base{base}"] = f"{maxdev:.2e}"


# ------------------------------------------------------- V6 -- reduction

def v6_reduction(cert=None):
    for base in (3, 5):
        for B in (4, 6):
            cls = brute_classes(B, base)
            c = sidon_c(B, base)
            M = closed_M(B)
            Mc = Fraction(M, c)
            by_level = defaultdict(list)
            for v, fib in cls.items():
                by_level[sum(v)].append(fib)
            ok_uniform = True
            total = Fraction(0)
            for s, fibs in by_level.items():
                datas = set()
                for fib in fibs:
                    counts = set(fib.values())
                    datas.add((len(fib), counts.pop() if len(counts) == 1 else -1))
                if len(datas) != 1:
                    ok_uniform = False
                for fib in fibs:
                    for sig, n in fib.items():
                        hp = Fraction(n) - Mc
                        if hp > 0:
                            total += Fraction(n) * hp
            ledger_total = sum(ledger_term(B, s, sidon_c(B, base))
                               for s in range(B % 2, B + 1, 2)) if base == 3 else None
            check(f"V6 levels uniform (identical (#syndromes, fiber) per class) (B={B}, base {base})",
                  ok_uniform)
            check(f"V6 level-block count <= B/2 + 1 (B={B}, base {base})",
                  len(by_level) <= B // 2 + 1)
            if base == 3:
                check(f"V6 level-block ell^1 total == closed ledger == Omega~_+ (B={B}, base 3)",
                      total == ledger_total)


# ------------------------------------------------- V7 -- cross-consistency

def v7_cross():
    ok_prof, ok_disj = True, True
    for base in (3, 5):
        for B in (4, 6):
            cls = brute_classes(B, base)
            n_syn = 0
            union = set()
            for v, fib in cls.items():
                s = sum(v)
                if len(fib) != 2 ** s or set(fib.values()) != {fiber_w(B, s)}:
                    ok_prof = False
                n_syn += len(fib)
                union.update(fib.keys())
            if len(union) != n_syn:
                ok_disj = False
    check("V7 brute class/fiber grid == resonant-folding closed forms (B in {4,6}, both bases)",
          ok_prof)
    check("V7 distinct classes have disjoint syndrome sets (union count == sum of counts) (B in {4,6}, both bases)",
          ok_disj)
    check("V7 M2 pins match integrated values (3584 / 97444)",
          closed_M2(6) == 3584 and closed_M2(8) == 97444)


# ----------------------------------------------------------------- driver

def run_all(quiet=False, cert=None):
    global QUIET, CHECKS
    QUIET = quiet
    CHECKS = []
    if cert is not None:
        cert.update({"fold_coarsening": {}, "ledger_shares": {},
                     "ledger_argmax": {}, "away_mass": {},
                     "erratum_below_2ML": {}, "participation": {},
                     "bridge_maxdev": {}})
    v1_fold_triviality(cert)
    v2_ledger(cert)
    v3_erratum(cert)
    v4_flatness_participation(cert)
    v5_bridge(cert)
    v6_reduction(cert)
    v7_cross()
    bad = [n for n, ok in CHECKS if not ok]
    if not quiet:
        print(f"RESULT: {'PASS' if not bad else 'FAIL'} "
              f"({len(CHECKS) - len(bad)}/{len(CHECKS)})")
    return not bad


def tamper_selftest():
    """Mutate five load-bearing pieces; each must flip PASS -> FAIL."""
    me = sys.modules[__name__]
    caught = 0
    orig_l = me.ledger_term
    me.ledger_term = lambda B, s, c: orig_l(B, s, c) + 1
    if not run_all(quiet=True):
        caught += 1
    me.ledger_term = orig_l
    orig_w = me.fiber_w
    me.fiber_w = lambda B, s: orig_w(B, s) + (1 if s == B else 0)
    if not run_all(quiet=True):
        caught += 1
    me.fiber_w = orig_w
    orig_s = me.sq_term
    me.sq_term = lambda B, s, c: orig_s(B, s, c) * 4
    if not run_all(quiet=True):
        caught += 1
    me.sq_term = orig_s
    orig_m2 = me.closed_M2
    me.closed_M2 = lambda B: orig_m2(B) + 1
    if not run_all(quiet=True):
        caught += 1
    me.closed_M2 = orig_m2
    orig_L = me.closed_L
    me.closed_L = lambda B: orig_L(B) * 4
    if not run_all(quiet=True):
        caught += 1
    me.closed_L = orig_L
    print(f"tamper-selftest: caught {caught}/5")
    ok = run_all()
    return caught == 5 and ok


def emit_certificate(path):
    import json
    cert = {}
    ok = run_all(quiet=True, cert=cert)
    cert["all_checks_pass"] = ok
    cert["n_checks"] = len(CHECKS)
    cert["float_note"] = ("bridge identity (V5) uses floats guarded by exact "
                          "Parseval; every other number is exact int/Fraction")
    with open(path, "w") as fh:
        json.dump(cert, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"certificate written: {path}")


if __name__ == "__main__":
    if "--tamper-selftest" in sys.argv:
        sys.exit(0 if tamper_selftest() else 1)
    if "--emit-certificate" in sys.argv:
        emit_certificate(sys.argv[sys.argv.index("--emit-certificate") + 1])
        sys.exit(0)
    sys.exit(0 if run_all() else 1)
