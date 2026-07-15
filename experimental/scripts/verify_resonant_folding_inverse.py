#!/usr/bin/env python3
"""Verifier: resonant-folding inverse + exact parity decomposition on the Sidon-paired class (hard input 2).

Checks, per the note experimental/notes/thresholds/resonant_folding_inverse.md:

V1  Parity-class profile (Theorem 3a): N_v = 2^s C(B-s,(B-s)/2) for
    s = |supp v| == B (mod 2), else 0 -- brute force over all C(2B,B) supports
    (B in {4,6}, both bases); sum_v N_v = M for B <= 64 (exact); the flatness
    window 2^B/sqrt(2B) <= N_v <= 2^B for every admissible class
    (cross-multiplied integers).
V2  Fold-character correlations (Theorem 3b): <psi_H> = sum_S psi_H(S)
    = [z^B] (1-z)^{2h} (1+z)^{2(B-h)} = Krawtchouk alternating sum
    sum_k (-1)^k C(2h,k) C(2B-2h,B-k), h = |H| -- brute force (B in {4,6},
    both bases, ALL 2^B subsets H); closed form == Krawtchouk for all h,
    B <= 64; endpoints h in {0,B} attain +-M; interior |<psi_H>| < M;
    sign symmetry <psi>(B-h) = (-1)^B <psi>(h).
V3  Parity-Parseval (Theorem 3c): sum_H <psi_H>^2 = 2^B sum_v N_v^2 (exact,
    B <= 64); the generating-function identity
    sum_v N_v^2 = [z^B w^B] (4zw + (1+z^2)(1+w^2))^B (exact, B <= 32); the
    participation ratio PR = sum_H <psi_H>^2 / M^2 obeys 2 <= PR <= 3 for all
    even 6 <= B <= 64 (exact rationals; >= 2 because h = 0 and h = B alone
    contribute 2 M^2): the fold spectrum is l^2-dominated by the two +-M
    characters.
V4  M2 reconstruction (Theorem 3d): the closed form
    M2 = sum_s C(B,s) 2^s C(B-s,(B-s)/2)^2 is cross-checked against the
    INDEPENDENT generating function [z^B w^B] (2zw + (1+z^2)(1+w^2))^B
    (2D convolution -- a different computational path), B <= 32; the
    reconstruction identity 2^B * M2 = sum_v N_v^2 2^{B-s(v)} is checked as
    definitional consistency for B <= 64 (its mathematical content -- that
    M2 is the true collision mass and the fibers are the sign-splitting --
    is carried by the brute checks); brute fiber structure (B in {4,6},
    both bases): inside class v the map Phi takes exactly 2^s distinct values
    mod c, each on exactly C(B-s,(B-s)/2) supports, and no two classes share
    a Phi-value (2-superincreasing + c > 2 sum P); brute M2 == closed;
    the per-class term T(s) = C(B,s) 2^s C(B-s,(B-s)/2)^2 has its maximizer
    within |s* - B/3| <= 2 for every even B <= 96 and is unimodal over the
    admissible s.
V5  Parity domination (Theorem 2): with H(j) = {i : cos(2 pi j A_i / c) < 0}
    (exact integer test 4r in (c, 3c), r = j A_i mod c) and
    D(j) = [z^B] prod_i (1 + z^2 + 2 z |cos theta_i|):
    brute force at B = 6, BOTH bases, ALL j: the twisted sum
    A(j) = sum_S e_c(-j Phi(S)) psi_{H(j)}(S) is real, equals D(j), and
    dominates: |hat f(j)| <= D(j); product-formula scan at B = 8 (base 3),
    all j, same domination; equality |hat f(j)| = D(j) whenever
    H(j) in {emptyset, [B]} (z -> -z parity); the brute hat f equals the
    product formula (re-verifies the integrated per-pair factorization);
    every scan is guarded by exact Parseval sum_j hat f(j)^2 == c * M2 to
    1e-6 relative; half-frequency j* = (c-1)/2 has H(j*) = [B] exactly and
    |hat f(j*)| >= 0.70 M (base 3, B in {6,8}) / >= 0.61 M (base 5, B = 6);
    census #{j != 0: |hat f(j)| >= M/10} == 42 (B=6) / 58 (B=8), base 3,
    matching the integrated transverse-charge pins.
V6  Shell structure (Theorem 1): m(j, delta) = #{i : ||j A_i / c|| in
    [delta, 1/2 - delta]} (exact integer classification); the proof's core
    chain |hat f(j)| <= 4^B cos(pi delta)^{2 m(j,delta)} holds for ALL j != 0
    on full scans ((B,base) in {(6,3),(8,3),(6,5)}, delta in
    {1/20, 1/10, 3/20}); the stated bound
    m(j,delta) <= ln(2 sqrt(B)/rho) / (2 ln sec(pi delta)) holds on every
    rho-shell, rho in {1/2, 1/4, 1/10, 1/20}; the binomial input
    M >= 4^B / (2 sqrt B) as 4 B M^2 >= 16^B (exact, B <= 64); worst
    observed m pinned.
V7  Cross-consistency with the integrated transverse-charge packet: same
    class data, same M2, same census pins, same j*; audit-before-consume for
    the one imported identity (the product formula, re-proved by brute here).

Deterministic, stdlib only.  --tamper-selftest mutates five load-bearing
pieces and verifies each is caught.  --emit-certificate PATH writes the JSON
certificate.
"""
import sys
from fractions import Fraction
from math import comb, cos, sin, pi, sqrt, log, isqrt
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


def closed_M(B):
    return comb(2 * B, B)


def closed_M2(B):
    """Integrated closed form: sum_{s == B (2)} C(B,s) 2^s C(B-s,(B-s)/2)^2."""
    return sum(comb(B, s) * 2 ** s * comb(B - s, (B - s) // 2) ** 2
               for s in range(B % 2, B + 1, 2))


def closed_Nv(B, s):
    """Theorem 3a: class size N_v for |supp v| = s (0 unless s == B mod 2)."""
    if s % 2 != B % 2:
        return 0
    return 2 ** s * comb(B - s, (B - s) // 2)


def closed_psi(B, h):
    """Theorem 3b closed form: [z^B] (1-z)^{2h} (1+z)^{2(B-h)}."""
    poly = [0] * (B + 1)
    poly[0] = 1
    for _ in range(h):          # multiply by (1-z)^2 = 1 - 2z + z^2
        new = [0] * (B + 1)
        for i, a in enumerate(poly):
            if a:
                new[i] += a
                if i + 1 <= B:
                    new[i + 1] -= 2 * a
                if i + 2 <= B:
                    new[i + 2] += a
        poly = new
    for _ in range(B - h):      # multiply by (1+z)^2 = 1 + 2z + z^2
        new = [0] * (B + 1)
        for i, a in enumerate(poly):
            if a:
                new[i] += a
                if i + 1 <= B:
                    new[i + 1] += 2 * a
                if i + 2 <= B:
                    new[i + 2] += a
        poly = new
    return poly[B]


def kraw_psi(B, h):
    """Theorem 3b, Krawtchouk form: sum_k (-1)^k C(2h,k) C(2B-2h,B-k)."""
    return sum((-1) ** k * comb(2 * h, k) * comb(2 * B - 2 * h, B - k)
               for k in range(0, B + 1))


def recon_weight(B, s):
    """Theorem 3d reconstruction weight on N_v^2: 2^{B-s} (times 2^{-B})."""
    return 2 ** (B - s)


# ------------------------------------------------- angles, exact and float

def antipodal(j, A, c):
    """cos(2 pi j A / c) < 0, exactly: r = jA mod c has 4r in (c, 3c)."""
    r = (j * A) % c
    return c < 4 * r < 3 * c


def generic(j, A, c, delta_num, delta_den):
    """||jA/c|| in [delta, 1/2 - delta], exactly, delta = delta_num/delta_den:
    min(r, c-r)/c >= delta  AND  |2r - c|/(2c) >= delta."""
    r = (j * A) % c
    return (delta_den * min(r, c - r) >= delta_num * c
            and delta_den * abs(2 * r - c) >= 2 * delta_num * c)


def hatf_and_dom(B, base, j, c, costab):
    """(hat f(j), D(j)) via the per-pair product formula, floats."""
    poly_f = [1.0]
    poly_d = [1.0]
    for A in sidon_P(B, base):
        cth = costab[(j * A) % c]
        for poly, t in ((poly_f, 2.0 * cth), (poly_d, 2.0 * abs(cth))):
            new = [0.0] * (len(poly) + 2)
            for i, a in enumerate(poly):
                if a:
                    new[i] += a
                    new[i + 1] += a * t
                    new[i + 2] += a
            if poly is poly_f:
                poly_f = new
            else:
                poly_d = new
    return poly_f[B], poly_d[B]


def brute_support_groups(B, base):
    """Brute tally over all C(2B,B) supports: {(Phi mod c, v): count}.
    No class structure assumed -- raw enumeration."""
    P = sidon_P(B, base)
    c = sidon_c(B, base)
    T = P + [c - p for p in P]
    pairs = [(P[i], c - P[i]) for i in range(B)]
    groups = defaultdict(int)
    for S in combinations(T, B):
        Sset = set(S)
        v = tuple(((pairs[i][0] in Sset) + (pairs[i][1] in Sset)) % 2
                  for i in range(B))
        groups[(sum(S) % c, v)] += 1
    return groups


# ------------------------------------------------------------ V1 -- profile

def v1_profile():
    for base in (3, 5):
        for B in (4, 6):
            groups = brute_support_groups(B, base)
            tally = defaultdict(int)
            for (_sig, v), n in groups.items():
                tally[v] += n
            ok_all = True
            for smask in range(2 ** B):
                v = tuple((smask >> i) & 1 for i in range(B))
                s = sum(v)
                if tally.get(v, 0) != closed_Nv(B, s):
                    ok_all = False
            check(f"V1 N_v brute == closed, ALL 2^{B} classes (B={B}, base {base})", ok_all)
            check(f"V1 admissible-class count == 2^{B-1} (B={B}, base {base})",
                  sum(1 for v, n in tally.items() if n) == 2 ** (B - 1))
    for B in range(2, 65):
        good = sum(comb(B, s) * closed_Nv(B, s)
                   for s in range(B + 1)) == closed_M(B)
        if not good:
            check(f"V1 sum_v N_v == M at B={B}", False)
            break
    else:
        check("V1 sum_v N_v == M for all 2 <= B <= 64", True)
    flat = True
    for B in range(2, 65):
        for s in range(B % 2, B + 1, 2):
            nv = closed_Nv(B, s)
            if not (2 * B * nv * nv >= 4 ** B and nv <= 2 ** B):
                flat = False
    check("V1 flatness window 2^B/sqrt(2B) <= N_v <= 2^B, all admissible v, B <= 64", flat)


# ------------------------------------------------- V2 -- fold correlations

def v2_fold_characters():
    for base in (3, 5):
        for B in (4, 6):
            groups = brute_support_groups(B, base)
            ok_all = True
            for hmask in range(2 ** B):
                H = [i for i in range(B) if (hmask >> i) & 1]
                acc = 0
                for (_sig, v), n in groups.items():
                    sign = -1 if sum(v[i] for i in H) % 2 else 1
                    acc += sign * n
                if acc != closed_psi(B, len(H)):
                    ok_all = False
            check(f"V2 <psi_H> brute == closed, ALL 2^{B} subsets H (B={B}, base {base})", ok_all)
    ok = all(closed_psi(B, h) == kraw_psi(B, h)
             for B in range(1, 65) for h in range(B + 1))
    check("V2 closed form == Krawtchouk sum, all h <= B <= 64", ok)
    ok_end, ok_int, ok_sym = True, True, True
    for B in range(2, 65):
        M = closed_M(B)
        if closed_psi(B, 0) != M or closed_psi(B, B) != (-1) ** B * M:
            ok_end = False
        if any(abs(closed_psi(B, h)) >= M for h in range(1, B)):
            ok_int = False
        if any(closed_psi(B, B - h) != (-1) ** B * closed_psi(B, h)
               for h in range(B + 1)):
            ok_sym = False
    check("V2 endpoints: <psi> = M at h=0, (-1)^B M at h=B, B <= 64", ok_end)
    check("V2 interior: |<psi_H>| < M for 0 < h < B, B <= 64", ok_int)
    check("V2 sign symmetry <psi>(B-h) == (-1)^B <psi>(h), B <= 64", ok_sym)


# ------------------------------------------------------- V3 -- Parseval, GF

def gf_sum_Nv2(B):
    """[z^B w^B] (4zw + (1+z^2)(1+w^2))^B, exact."""
    g = {(1, 1): 4, (0, 0): 1, (2, 0): 1, (0, 2): 1, (2, 2): 1}
    acc = {(0, 0): 1}
    for _ in range(B):
        nxt = defaultdict(int)
        for (i, j), a in acc.items():
            for (k, l), b in g.items():
                if i + k <= B and j + l <= B:
                    nxt[(i + k, j + l)] += a * b
        acc = dict(nxt)
    return acc.get((B, B), 0)


def v3_parseval(cert=None):
    ok_pars = True
    for B in range(2, 65):
        lhs = sum(comb(B, h) * closed_psi(B, h) ** 2 for h in range(B + 1))
        rhs = 2 ** B * sum(comb(B, s) * closed_Nv(B, s) ** 2
                           for s in range(B % 2, B + 1, 2))
        if lhs != rhs:
            ok_pars = False
    check("V3 parity-Parseval sum_H <psi_H>^2 == 2^B sum_v N_v^2, B <= 64", ok_pars)
    ok_gf = all(gf_sum_Nv2(B) == sum(comb(B, s) * closed_Nv(B, s) ** 2
                                     for s in range(B % 2, B + 1, 2))
                for B in range(2, 33))
    check("V3 GF identity sum_v N_v^2 == [z^B w^B](4zw+(1+z^2)(1+w^2))^B, B <= 32", ok_gf)
    ok_pr = True
    for B in range(6, 65, 2):
        M = closed_M(B)
        pr = Fraction(sum(comb(B, h) * closed_psi(B, h) ** 2
                          for h in range(B + 1)), M * M)
        if not (2 <= pr <= 3):
            ok_pr = False
        if cert is not None and B in (6, 8, 16, 32, 64):
            cert["participation_ratio"][str(B)] = f"{float(pr):.6f}"
    check("V3 participation ratio in [2, 3], even 6 <= B <= 64", ok_pr)


# -------------------------------------------- V4 -- M2 reconstruction, s*

def gf_M2(B):
    """[z^B w^B] (2zw + (1+z^2)(1+w^2))^B, exact -- an independent
    computational path to M2 (2D convolution vs binomial sum)."""
    g = {(1, 1): 2, (0, 0): 1, (2, 0): 1, (0, 2): 1, (2, 2): 1}
    acc = {(0, 0): 1}
    for _ in range(B):
        nxt = defaultdict(int)
        for (i, j), a in acc.items():
            for (k, l), b in g.items():
                if i + k <= B and j + l <= B:
                    nxt[(i + k, j + l)] += a * b
        acc = dict(nxt)
    return acc.get((B, B), 0)


def v4_reconstruction(cert=None):
    ok_gf = all(closed_M2(B) == gf_M2(B) for B in range(2, 33))
    check("V4 closed M2 == independent GF [z^B w^B](2zw+(1+z^2)(1+w^2))^B, B <= 32", ok_gf)
    ok = True
    for B in range(2, 65):
        lhs = 2 ** B * closed_M2(B)
        rhs = sum(comb(B, s) * closed_Nv(B, s) ** 2 * recon_weight(B, s)
                  for s in range(B % 2, B + 1, 2))
        if lhs != rhs:
            ok = False
    check("V4 reconstruction identity 2^B M2 == sum_v N_v^2 2^{B-s} (definitional consistency), B <= 64", ok)
    for base in (3, 5):
        for B in (4, 6):
            groups = brute_support_groups(B, base)
            per_class = defaultdict(list)
            for (sig, v), n in groups.items():
                per_class[v].append((sig, n))
            ok_fib, ok_cnt = True, True
            for v, lst in per_class.items():
                s = sum(v)
                w = comb(B - s, (B - s) // 2)
                if len(lst) != 2 ** s:
                    ok_cnt = False
                if any(n != w for _sig, n in lst):
                    ok_fib = False
            n_sig = len(set(sig for (sig, _v) in groups))
            check(f"V4 within-class: 2^s values x C(B-s,(B-s)/2) each (B={B}, base {base})",
                  ok_fib and ok_cnt)
            check(f"V4 cross-class Phi-values all distinct (B={B}, base {base})",
                  n_sig == sum(2 ** sum(v) for v in per_class))
            fib = defaultdict(int)
            for (sig, _v), n in groups.items():
                fib[sig] += n
            check(f"V4 brute M2 == closed M2 (B={B}, base {base})",
                  sum(n * n for n in fib.values()) == closed_M2(B))
    ok_loc, ok_uni = True, True
    for B in range(6, 97, 2):
        terms = [(s, comb(B, s) * 2 ** s * comb(B - s, (B - s) // 2) ** 2)
                 for s in range(B % 2, B + 1, 2)]
        vals = [t for _s, t in terms]
        smax = max(terms, key=lambda st: st[1])[0]
        if abs(smax - B / 3) > 2:
            ok_loc = False
        k = vals.index(max(vals))
        if not (all(vals[i] < vals[i + 1] for i in range(k)) and
                all(vals[i] > vals[i + 1] for i in range(k, len(vals) - 1))):
            ok_uni = False
        if cert is not None and B in (6, 12, 24, 48, 96):
            cert["m2_maximizer"][str(B)] = smax
    check("V4 M2-term maximizer |s* - B/3| <= 2, even B <= 96", ok_loc)
    check("V4 M2-term profile strictly unimodal over admissible s, even B <= 96", ok_uni)


# ------------------------------------------------- V5 -- parity domination

def scan_products(B, base):
    """(c, costab, hatf[], dom[]) full product-formula scan, floats."""
    c = sidon_c(B, base)
    costab = [cos(2 * pi * r / c) for r in range(c)]
    hatf = [0.0] * c
    dom = [0.0] * c
    for j in range(c):
        hatf[j], dom[j] = hatf_and_dom(B, base, j, c, costab)
    return c, costab, hatf, dom


def v5_domination(cert=None):
    for base, brute in ((3, True), (5, True)):
        B = 6
        c, costab, hatf, dom = scan_products(B, base)
        M = closed_M(B)
        sintab = [sin(2 * pi * r / c) for r in range(c)]
        P = sidon_P(B, base)
        pars = sum(x * x for x in hatf)
        check(f"V5 Parseval guard sum hat f^2 == c*M2 to 1e-6 rel (B=6, base {base})",
              abs(pars - c * closed_M2(B)) <= 1e-6 * c * closed_M2(B))
        groups = brute_support_groups(B, base)
        glist = [(sig, v, n) for (sig, v), n in groups.items()]
        ok_real, ok_eqD, ok_dom, ok_eqcls, ok_prod = True, True, True, True, True
        tol = 1e-8 * M
        for j in range(c):
            H = [i for i in range(B) if antipodal(j, P[i], c)]
            re_a, im_a, re_f, im_f = 0.0, 0.0, 0.0, 0.0
            for sig, v, n in glist:
                r = (j * sig) % c
                cr, sr = costab[r], sintab[r]
                sign = -1 if sum(v[i] for i in H) % 2 else 1
                re_a += sign * n * cr
                im_a -= sign * n * sr
                re_f += n * cr
                im_f -= n * sr
            if abs(im_a) > tol or abs(im_f) > tol:
                ok_real = False
            if abs(re_a - dom[j]) > tol:
                ok_eqD = False
            if abs(re_f - hatf[j]) > tol:
                ok_prod = False
            if abs(hatf[j]) > dom[j] + tol:
                ok_dom = False
            if (len(H) in (0, B)) and abs(abs(hatf[j]) - dom[j]) > tol:
                ok_eqcls = False
        check(f"V5 brute twisted sum is real, ALL j (B=6, base {base})", ok_real)
        check(f"V5 brute <chi_j Phi, psi_H(j)> == D(j) product form, ALL j (B=6, base {base})", ok_eqD)
        check(f"V5 brute hat f == product formula, ALL j (B=6, base {base})", ok_prod)
        check(f"V5 domination |hat f(j)| <= D(j), ALL j (B=6, base {base})", ok_dom)
        check(f"V5 equality on H(j) in {{0,[B]}} classes (B=6, base {base})", ok_eqcls)
        jstar = (c - 1) // 2
        check(f"V5 H(j*) == [B] (B=6, base {base})",
              all(antipodal(jstar, A, c) for A in P))
        thr = 0.70 if base == 3 else 0.61
        check(f"V5 |hat f(j*)| >= {thr} M (B=6, base {base})",
              abs(hatf[jstar]) >= thr * M)
        if base == 3:
            census = sum(1 for j in range(1, c) if abs(hatf[j]) * 10 >= M)
            check("V5 census rho=1/10 == 42 (B=6, base 3, integrated pin)", census == 42)
            if cert is not None:
                cert["resonance"]["base3_B6"] = {
                    "jstar": jstar, "abs_hatf_jstar_over_M": round(abs(hatf[jstar]) / M, 6),
                    "census_rho_tenth": census}
        elif cert is not None:
            cert["resonance"]["base5_B6"] = {
                "jstar": jstar, "abs_hatf_jstar_over_M": round(abs(hatf[jstar]) / M, 6)}
    B, base = 8, 3
    c, costab, hatf, dom = scan_products(B, base)
    M = closed_M(B)
    P = sidon_P(B, base)
    tol = 1e-8 * M
    check("V5 Parseval guard sum hat f^2 == c*M2 to 1e-6 rel (B=8, base 3)",
          abs(sum(x * x for x in hatf) - c * closed_M2(B)) <= 1e-6 * c * closed_M2(B))
    ok_dom = all(abs(hatf[j]) <= dom[j] + tol for j in range(c))
    ok_pos = all(dom[j] >= -tol for j in range(c))
    ok_eqcls = True
    for j in range(c):
        nH = sum(1 for A in P if antipodal(j, A, c))
        if nH in (0, B) and abs(abs(hatf[j]) - dom[j]) > tol:
            ok_eqcls = False
    check("V5 domination |hat f(j)| <= D(j), ALL j (B=8, base 3)", ok_dom)
    check("V5 D(j) >= 0, ALL j (B=8, base 3)", ok_pos)
    check("V5 equality on H(j) in {0,[B]} classes (B=8, base 3)", ok_eqcls)
    jstar = (c - 1) // 2
    check("V5 H(j*) == [B] (B=8, base 3)", all(antipodal(jstar, A, c) for A in P))
    check("V5 |hat f(j*)| >= 0.70 M (B=8, base 3)", abs(hatf[jstar]) >= 0.70 * M)
    census = sum(1 for j in range(1, c) if abs(hatf[j]) * 10 >= M)
    check("V5 census rho=1/10 == 58 (B=8, base 3, integrated pin)", census == 58)
    if cert is not None:
        cert["resonance"]["base3_B8"] = {
            "jstar": jstar, "abs_hatf_jstar_over_M": round(abs(hatf[jstar]) / M, 6),
            "census_rho_tenth": census}


# ------------------------------------------------------ V6 -- shell bound

def v6_shell(cert=None):
    ok_binom = all(4 * B * closed_M(B) ** 2 >= 16 ** B for B in range(1, 65))
    check("V6 binomial input 4 B M^2 >= 16^B (M >= 4^B/(2 sqrt B)), B <= 64", ok_binom)
    for B, base in ((6, 3), (8, 3), (6, 5)):
        c, _costab, hatf, _dom = scan_products(B, base)
        M = closed_M(B)
        P = sidon_P(B, base)
        for dnum, dden in ((1, 20), (1, 10), (3, 20)):
            delta = dnum / dden
            cosd = cos(pi * delta)
            ok_core = True
            worst = {}
            for j in range(1, c):
                m = sum(1 for A in P if generic(j, A, c, dnum, dden))
                if abs(hatf[j]) > (4.0 ** B) * cosd ** (2 * m) * (1 + 1e-9):
                    ok_core = False
                for rho_num, rho_den in ((1, 2), (1, 4), (1, 10), (1, 20)):
                    if abs(hatf[j]) * rho_den >= M * rho_num:
                        key = (rho_num, rho_den)
                        worst[key] = max(worst.get(key, 0), m)
            check(f"V6 core |hat f| <= 4^B cos(pi d)^2m, ALL j (B={B}, base {base}, d={dnum}/{dden})",
                  ok_core)
            ok_shell = True
            for (rn, rd), m_obs in worst.items():
                bound = log(2 * sqrt(B) * rd / rn) / (2 * log(1 / cosd))
                if m_obs > bound:
                    ok_shell = False
            check(f"V6 shell bound m <= ln(2 sqrt B / rho)/(2 ln sec pi d), all shells (B={B}, base {base}, d={dnum}/{dden})",
                  ok_shell)
            if cert is not None and (dnum, dden) == (1, 10):
                cert["shell"][f"base{base}_B{B}_delta0.1"] = {
                    f"rho_{rn}_{rd}": m for (rn, rd), m in sorted(worst.items())}


# ------------------------------------------------- V7 -- cross-consistency

def v7_cross():
    check("V7 M2 closed form matches integrated transverse-charge values (B=6: 3584, B=8: 97444)",
          closed_M2(6) == 3584 and closed_M2(8) == 97444)
    check("V7 ambient c: base 3 is 3^B (B in {6,8})",
          sidon_c(6, 3) == 3 ** 6 and sidon_c(8, 3) == 3 ** 8)
    check("V7 2-superincreasing + center bound, both bases, B <= 64",
          all(all(sidon_P(B, base)[i] > 2 * sum(sidon_P(B, base)[:i])
                  for i in range(B)) and sidon_c(B, base) > 2 * sum(sidon_P(B, base))
              for base in (3, 5) for B in (6, 8, 16, 32, 64)))
    check("V7 f_max^2 L < M^2 payment-gap sanity at B in {6,8} (integrated pin)",
          all(comb(B, B // 2) ** 2 * ((3 ** B + 1) // 2) < closed_M(B) ** 2
              for B in (6, 8)))


# ----------------------------------------------------------------- driver

def run_all(quiet=False, cert=None):
    global QUIET, CHECKS
    QUIET = quiet
    CHECKS = []
    if cert is not None:
        cert.update({"participation_ratio": {}, "m2_maximizer": {},
                     "resonance": {}, "shell": {}})
    v1_profile()
    v2_fold_characters()
    v3_parseval(cert)
    v4_reconstruction(cert)
    v5_domination(cert)
    v6_shell(cert)
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
    orig = me.closed_Nv
    me.closed_Nv = lambda B, s: orig(B, s) + (1 if s == B % 2 else 0)
    if not run_all(quiet=True):
        caught += 1
    me.closed_Nv = orig
    orig_k = me.kraw_psi
    me.kraw_psi = lambda B, h: sum(comb(2 * h, k) * comb(2 * B - 2 * h, B - k)
                                   for k in range(0, B + 1))
    if not run_all(quiet=True):
        caught += 1
    me.kraw_psi = orig_k
    orig_m2 = me.closed_M2
    me.closed_M2 = lambda B: orig_m2(B) + 1
    if not run_all(quiet=True):
        caught += 1
    me.closed_M2 = orig_m2
    orig_w = me.recon_weight
    me.recon_weight = lambda B, s: 2 ** (B - s + 1)
    if not run_all(quiet=True):
        caught += 1
    me.recon_weight = orig_w
    orig_a = me.antipodal
    me.antipodal = lambda j, A, c: not orig_a(j, A, c)
    if not run_all(quiet=True):
        caught += 1
    me.antipodal = orig_a
    print(f"tamper-selftest: caught {caught}/5")
    ok = run_all()
    return caught == 5 and ok


def emit_certificate(path):
    import json
    cert = {}
    ok = run_all(quiet=True, cert=cert)
    cert["all_checks_pass"] = ok
    cert["n_checks"] = len(CHECKS)
    cert["float_note"] = ("hat f / D via per-pair product formula (floats), "
                          "guarded by exact Parseval sum_j hat f^2 == c*M2; "
                          "angle sets H(j), m(j,delta) are exact integer tests")
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
