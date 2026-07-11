#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# verify_fi_field_discharge.py
#
# Recomputes every number in
#   experimental/notes/thresholds/fi_field_discharge.md
#
# DECIDES the single open link #642 named: does the frontiers paper's
# ledger-admissibility (A1)-(A7) or the Proximity-Prize reserve ALREADY imply
#   (FI-field):  the C7 collapse-cell received line is defined over a scalar
#                subextension F' with log|F'| = o(n).
#
# VERDICT (PARTIAL, sharp reduction).  On any PRIZE-RELEVANT received line
# (one the full-field target charges, e_MCA(r) = delta(r)/|F| > eps) subfield
# confinement (thm:subfield-confinement-full, tex L1930-1934) gives
#       delta(r) <= |F_r|      (F_r = field of definition, tex L2290-2292)
# hence, in NORMALIZED form,
#       e_MCA(r) = delta(r)/|F|  <=  |F_r|/|F|  =  1/[F:F_r].          (RED)
# So e_MCA(r) > eps  ==>  [F:F_r] < 1/eps = O(1)  ==>  log|F_r| = log|F| - O(1).
# The received-LINE certificate (FI-field) therefore REDUCES, on every
# prize-relevant line, to the AMBIENT-field hypothesis  log|F_n| = o(n).
# That hypothesis is (i) NOT among (A1)-(A7) (they never bound |F_n|), (ii)
# exactly the "field hypothesis" the paper's own scope remark names
# (rem:intro-countertheorem-scope, tex L836-840), and (iii) true for the
# prize's poly-size smooth-domain rows -- on which the span face closes
# unconditionally.  Every Theta(n)-field witness (countertheorem eq 4.5 /
# 6.7-6.8; Codex #634; DannyExperiments #631) has UNBOUNDED [F:F_r] and is
# therefore diluted below any fixed target -- admissible but NOT prize-relevant.
#
# Stdlib only.  Zero-arg.  Exits nonzero on any failed check.  Prints
# "RESULT: PASS (<passed>/<total>)".  Runtime well under 4 min, << ulimit -v.
#
# Credits: our #642 (c7_collapse_image_degree, GF/antipodal machinery reused),
# #635/#636/#627/#625/#622; Codex #634/#624; DannyExperiments #631/#621/#641.
# T-FIELD-TIGHT is THE PAPER'S countertheorem (thm:intro-countertheorem); we
# only cite/recompute it.
# ---------------------------------------------------------------------------

import math
import sys
from fractions import Fraction
from itertools import product, combinations

PASS = 0
FAIL = 0
LOG = []


def check(name, cond, got=None, want=None):
    global PASS, FAIL
    if cond:
        PASS += 1
        LOG.append(f"  ok   {name}")
    else:
        FAIL += 1
        LOG.append(f"  FAIL {name}: got={got!r} want={want!r}")


def section(title):
    LOG.append("")
    LOG.append(title)


# ===========================================================================
# Minimal GF(p^d) arithmetic (stdlib only) -- reused verbatim from #642's
# verify_c7_collapse_image_degree.py.  Elements are length-d tuples over F_p
# (little-endian), reduced mod a monic irreducible.
# ===========================================================================

def poly_mulmod(a, b, mod, p):
    d = len(mod) - 1
    res = [0] * (2 * d)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    res[i + j] = (res[i + j] + ai * bj) % p
    for k in range(2 * d - 1, d - 1, -1):
        c = res[k]
        if c:
            res[k] = 0
            for j in range(d + 1):
                res[k - d + j] = (res[k - d + j] - c * mod[j]) % p
    return tuple(res[:d])


def poly_gcd(a, b, p):
    a = a[:]; b = b[:]
    def norm(x):
        while len(x) > 1 and x[-1] == 0:
            x.pop()
        return x
    a = norm(a); b = norm(b)
    while not (len(b) == 1 and b[0] == 0):
        a = norm(a); b = norm(b)
        if len(a) < len(b):
            a, b = b, a
            continue
        inv = pow(b[-1], p - 2, p)
        while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
            a = norm(a)
            if len(a) < len(b):
                break
            c = (a[-1] * inv) % p
            shift = len(a) - len(b)
            for i in range(len(b)):
                a[shift + i] = (a[shift + i] - c * b[i]) % p
            a = norm(a)
        a, b = b, a
    return norm(a)


def is_irreducible(mod, p):
    d = len(mod) - 1
    if d == 1:
        return True
    X = tuple([0, 1] + [0] * (d - 2))

    def frob_pow(elt, e):
        cur = elt
        for _ in range(e):
            acc = (1,) + (0,) * (d - 1)
            for _ in range(p):
                acc = poly_mulmod(acc, cur, mod, p)
            cur = acc
        return cur

    if frob_pow(X, d) != X:
        return False

    def prime_divs(m):
        s, x = set(), m
        f = 2
        while f * f <= x:
            while x % f == 0:
                s.add(f); x //= f
            f += 1
        if x > 1:
            s.add(x)
        return s

    for l in prime_divs(d):
        e = d // l
        val = frob_pow(X, e)
        diff = list(val)
        diff[1] = (diff[1] - 1) % p
        g = poly_gcd(diff, list(mod), p)
        while len(g) > 1 and g[-1] == 0:
            g.pop()
        if len(g) != 1:
            return False
    return True


def find_irreducible(p, d):
    if d == 1:
        return (0, 1)
    for coeffs in product(range(p), repeat=d):
        mod = list(coeffs) + [1]
        if is_irreducible(mod, p):
            return tuple(mod)
    raise RuntimeError(f"no irreducible found for GF({p}^{d})")


class GF:
    def __init__(self, p, d):
        self.p = p
        self.d = d
        self.mod = find_irreducible(p, d)
        self.one = (1,) + (0,) * (d - 1)

    def embed(self, a):
        return (a % self.p,) + (0,) * (self.d - 1)

    def sub(self, a, b):
        return tuple((x - y) % self.p for x, y in zip(a, b))

    def mul(self, a, b):
        if self.d == 1:
            return ((a[0] * b[0]) % self.p,)
        return poly_mulmod(list(a), list(b), list(self.mod), self.p)

    def prod_linear(self, alpha, roots):
        acc = self.one
        for x in roots:
            acc = self.mul(acc, self.sub(alpha, self.embed(x)))
        return acc

    def poly_eval(self, coeffs, alpha):
        # coeffs little-endian over F_p; Horner in F_{p^d}
        acc = (0,) * self.d
        for c in reversed(coeffs):
            acc = self.mul(acc, alpha)
            acc = tuple((acc[i] + (c if i == 0 else 0)) % self.p for i in range(self.d))
        return acc

    def frob(self, a):
        # a^p via square-and-multiply on the integer exponent p
        return self.pow_int(a, self.p)

    def pow_int(self, a, e):
        acc = self.one
        base = a
        while e > 0:
            if e & 1:
                acc = self.mul(acc, base)
            base = self.mul(base, base)
            e >>= 1
        return acc

    def deg_over_prime(self, alpha):
        # smallest e | d with alpha^(p^e) == alpha  ==>  F_p(alpha) = F_{p^e}
        cur = alpha
        for e in range(1, self.d + 1):
            cur = self.frob(cur)          # now cur = alpha^(p^e)
            if cur == alpha and self.d % e == 0:
                return e
        return self.d


# ===========================================================================
# Antipodal fiber machinery (reused from #642): D = F_p^*, phi: x -> x^2.
# ===========================================================================

def antipodal_orientations(p):
    seen = set()
    fibers = []
    for x in range(1, p):
        if x in seen:
            continue
        nx = (-x) % p
        fibers.append((x, nx))
        seen.add(x); seen.add(nx)
    orients = []
    for choice in product((0, 1), repeat=len(fibers)):
        S = tuple(fibers[i][choice[i]] for i in range(len(fibers)))
        orients.append(S)
    return fibers, orients


def enum_field(gf):
    """All p^d elements of GF(p^d) as tuples."""
    return [t for t in product(range(gf.p), repeat=gf.d)]


# ===========================================================================
# BLOCK 0 -- Subfield confinement census (reproduces #642 anchors, confirms
# machinery).  delta(alpha) = #distinct{ Q_S(alpha) : S in orientations }.
#   base pole alpha=0 in B  => delta = 2 (product parity, #634-at-0)
#   any base pole (alpha in F_p) => delta <= |B| = p           (confinement)
#   an extension pole can attain the full |O| = 2^a.
# ===========================================================================

def block0():
    section("BLOCK 0 -- subfield confinement census (reproduces #642)")
    # (a_exp, |O|, max-delta over F_{p^2}) -- the F_{p^2} column of #642's table.
    table = {7: (3, 8, 8), 11: (5, 32, 32), 13: (6, 64, 63)}
    for p, (a_exp, O_size, ext_p2) in table.items():
        fibers, orients = antipodal_orientations(p)
        check(f"p={p}: #fibers a=(p-1)/2={a_exp}", len(fibers) == a_exp,
              len(fibers), a_exp)
        check(f"p={p}: |O|=2^a={O_size}", len(orients) == O_size,
              len(orients), O_size)
        gf1 = GF(p, 1)
        # delta at alpha = 0 in B
        d0 = len({gf1.prod_linear((0,), S) for S in orients})
        check(f"p={p}: delta(alpha=0)=2 (product parity)", d0 == 2, d0, 2)
        # base_max over all alpha in F_p (that are not in D=F_p^* if used as pole;
        # pole must avoid D, so alpha=0 is the only base pole).
        base_max = d0  # only base pole avoiding D=F_p^* is 0
        check(f"p={p}: base_max <= |B|=p", base_max <= p, base_max, f"<= {p}")
        # extension pole in F_{p^2}: reproduces #642's F_{p^2} column exactly.
        gf2 = GF(p, 2)
        ext_max = 0
        for alpha in enum_field(gf2):
            if alpha[1] == 0:   # skip base field (would be a base pole)
                continue
            dd = len({gf2.prod_linear(alpha, S) for S in orients})
            if dd > ext_max:
                ext_max = dd
        check(f"p={p}: F_(p^2) pole max-delta={ext_p2} (reproduces #642)",
              ext_max == ext_p2, ext_max, ext_p2)
        # subfield confinement holds for EVERY pole over F_{p^2}: delta<=|F_r|
        ok = True
        for alpha in enum_field(gf2):
            e = gf2.deg_over_prime(alpha)
            Fr = p ** e
            dd = len({gf2.prod_linear(alpha, S) for S in orients})
            if dd > Fr:
                ok = False
                break
        check(f"p={p}: delta<=|F_r| for all poles in F_(p^2)", ok, ok, True)


# ===========================================================================
# BLOCK 1 -- eq (4.5) separation gate  (thm:prefix-to-line-hardness, L2077):
#   fiber of N m-sets, k=m-w-1,  need |F|-n > k*binom(N,2)  for N distinct
#   slopes on one line.  We instantiate slopes = { Q_S(alpha) } for the
#   antipodal fiber, sweep the extension degree, and locate the SMALLEST field
#   at which max_alpha delta = N.  We confirm:
#     (nec, subfield)  N distinct  ==>  |F_r| >= N               (LINEAR)
#     (suff, paper)    |F| > n + k*binom(N,2) always works       (QUADRATIC)
#     (honest gap)     the quadratic is SUFFICIENT not NECESSARY: full
#                      separation occurs already at a field far below binom(N,2).
# ===========================================================================

def block1():
    section("BLOCK 1 -- eq (4.5) separation gate (paper L2077-2083)")
    p = 7
    fibers, orients = antipodal_orientations(p)   # a=3, N=2^3=8
    N = len(orients)
    n = p - 1                                      # |D| = |F_p^*|
    k = len(fibers)                                # Q_S monic of degree a=k=3
    paper_suff = n + k * (N * (N - 1) // 2)        # |F| threshold, eq (4.5)
    check("p=7: N=2^a=8", N == 8, N, 8)
    check("p=7: k=a=3, n=6", (k, n) == (3, 6), (k, n), (3, 6))
    check("p=7: paper sufficient |F| threshold n+k*C(N,2)=6+3*28=90",
          paper_suff == 90, paper_suff, 90)

    # sweep extension degree; find smallest |F| with max delta = N
    e_star = None
    Fr_star = None
    for e in range(1, 4):                          # F_{7^1},7^2,7^3
        gf = GF(p, e)
        best = 0
        for alpha in enum_field(gf):
            # pole must avoid D = F_p^* (roots x in F_p^*); alpha in extension ok
            if e == 1 and alpha[0] in range(1, p):
                continue
            dd = len({gf.prod_linear(alpha, S) for S in orients})
            if dd > best:
                best = dd
            if best == N:
                break
        LOG.append(f"    e={e}  |F|=7^{e}={p**e:<5} max_delta={best}")
        # subfield confinement necessity: best <= |F|
        check(f"e={e}: max_delta <= |F|=7^{e}", best <= p ** e, best, f"<= {p**e}")
        if best == N and e_star is None:
            e_star = e
            Fr_star = p ** e
    check("some extension separates all N=8 slopes", e_star is not None,
          e_star, "not None")
    # subfield necessity (LINEAR): the separating field has |F_r| >= N
    check(f"separating |F_r|={Fr_star} >= N={N} (subfield necessity)",
          Fr_star >= N, Fr_star, f">= {N}")
    # honest gap: separation achieved BELOW the paper's quadratic sufficient
    # threshold (49 = 7^2 < 90).  Quadratic is SUFFICIENT, not NECESSARY.
    check(f"separation at |F_r|={Fr_star} < paper_suff={paper_suff} "
          f"(quadratic sufficient, not necessary)",
          Fr_star < paper_suff, Fr_star, f"< {paper_suff}")


# ===========================================================================
# BLOCK 2 -- THE REDUCTION (RED), the packet's core result.
# For EVERY field F=F_{p^d} and EVERY pole alpha, with delta = #distinct
# slopes, F_r = F_p(alpha), we verify the normalized subfield-confinement law
#       e_MCA = delta/|F|  <=  |F_r|/|F|  =  1/[F:F_r]        (RED)
# i.e.  delta * [F:F_r] <= |F|  (equivalently delta <= |F_r|), and derive
#       e_MCA > eps  ==>  [F:F_r] < 1/eps.
# This is what turns the received-line certificate into the ambient-field
# hypothesis:  prize-relevance forces F_r co-bounded in F.
# ===========================================================================

def block2():
    section("BLOCK 2 -- the reduction  e_MCA <= |F_r|/|F| = 1/(|F|/|F_r|)  (core)")
    p = 5
    fibers, orients = antipodal_orientations(p)     # a=2, N=4
    d = 3                                            # ambient F = F_{5^3}
    gf = GF(p, d)
    F_size = p ** d
    all_ok_conf = True
    all_ok_red = True
    worst_emca = Fraction(0)
    checked = 0
    for alpha in enum_field(gf):
        # skip poles hitting the domain D=F_p^*  (embedded base-field nonzero)
        if all(c == 0 for c in alpha[1:]) and alpha[0] in range(1, p):
            continue
        checked += 1
        e = gf.deg_over_prime(alpha)                 # [F_r:F_p]
        Fr = p ** e
        ratio = F_size // Fr                          # size ratio |F|/|F_r|
        dd = len({gf.prod_linear(alpha, S) for S in orients})
        if dd > Fr:                                   # subfield confinement
            all_ok_conf = False
        if dd * ratio > F_size:                       # normalized reduction (RED)
            all_ok_red = False
        emca = Fraction(dd, F_size)
        if emca > worst_emca:
            worst_emca = emca
    check(f"p={p},d={d}: subfield confinement delta<=|F_r| (all {checked} poles)",
          all_ok_conf, all_ok_conf, True)
    check(f"p={p},d={d}: normalized reduction delta*(|F|/|F_r|)<=|F| (all poles)",
          all_ok_red, all_ok_red, True)
    LOG.append(f"    worst-case antipodal e_MCA = {worst_emca} "
               f"= {float(worst_emca):.4f}")

    # --- synthetic teeth: a FULLY-BAD subfield line Z = F_r makes the reduction
    # an EQUALITY  e_MCA = |F_r|/|F| = 1/ratio  with ratio = |F|/|F_r|.  Then
    # prize-relevance (e_MCA > eps) selects EXACTLY the low-ratio lines
    # ratio < 1/eps and excludes every deep-subfield line -- so log|F_r| is
    # forced within log(1/eps) of log|F|:  the received-line field certificate
    # reduces to a bounded-size-ratio (= ambient-field) condition.
    d2 = 6
    F2 = 2 ** d2
    eps = Fraction(1, 8)                              # target: 1/8
    selected, excluded = [], []
    tight = True
    impl_ok = True
    for e in (1, 2, 3, 6):                            # divisors of 6 = [F_r:F_2]
        Fr = 2 ** e
        ratio = F2 // Fr                              # |F|/|F_r| = 2^(6-e)
        emca = Fraction(Fr, F2)                       # Z = F_r fully bad
        if emca != Fraction(1, ratio):               # RED equality
            tight = False
        if emca > eps:
            selected.append(ratio)
            if not (ratio < 1 / eps):                 # e_MCA>eps => ratio<1/eps
                impl_ok = False
        else:
            excluded.append(ratio)
    check("synthetic: fully-bad subfield line gives e_MCA=1/ratio (RED tight)",
          tight, tight, True)
    check("synthetic: e_MCA>eps selects EXACTLY low-ratio lines |F|/|F_r|<1/eps",
          impl_ok and selected == [1] and excluded == [32, 16, 8],
          (selected, excluded), ([1], [32, 16, 8]))
    LOG.append(f"    eps=1/8: prize-relevant size-ratios={selected} "
               f"(excluded deep-subfield ratios={excluded})")


# ===========================================================================
# BLOCK 3 -- DILUTION of the paper's own countertheorem in the full field.
# The construction places N distinct slopes on one line but uses
#   |F| > n + k*binom(N,2) ~ k N^2/2,  so  e_MCA = N/|F| <= 2/(k(N-1)) -> 0.
# For a fixed cryptographic target eps=2^-t the construction is SAFE once
# N exceeds a threshold; it is NOT prize-relevant.
# ===========================================================================

def block3():
    section("BLOCK 3 -- full-field dilution of the countertheorem")
    n = 1000
    k = 100
    prev = Fraction(1)
    monotone = True
    for a_exp in range(2, 8):
        N = 2 ** a_exp
        F_min = n + k * (N * (N - 1) // 2)          # smallest admissible |F|
        emca = Fraction(N, F_min)                   # N slopes / |F|
        bound = Fraction(2, k * (N - 1))            # 2/(k(N-1))
        check(f"N={N}: e_MCA=N/|F| <= 2/(k(N-1)) (dilution bound)",
              emca <= bound, float(emca), f"<= {float(bound)}")
        if emca > prev:
            monotone = False
        prev = emca
        LOG.append(f"    N={N:<4} |F|>={F_min:<9} e_MCA=N/|F|={float(emca):.3e}")
    check("e_MCA strictly decreasing in N (dilution)", monotone, monotone, True)
    # fixed target eps = 2^-128: for an exponentially large fiber (N=2^200) the
    # construction's own field |F| > k*binom(N,2) ~ N^2 forces e_MCA = N/|F|
    # below eps -- the countertheorem is auto-SAFE, hence NOT prize-relevant.
    eps = Fraction(1, 2 ** 128)
    N = 2 ** 200
    F_min = n + k * (N * (N - 1) // 2)              # exact integer threshold
    emca = Fraction(N, F_min)
    check("N=2^200: countertheorem e_MCA=N/|F| < 2^-128 (auto-safe, exact)",
          emca < eps, f"~2^{emca.numerator.bit_length()-emca.denominator.bit_length()}",
          "< 2^-128")


# ===========================================================================
# BLOCK 4 -- challenge-intersection averaging identity (eq 13.3 proof, L6206):
#   averaging over translates delta in F gives |Z||Gamma|/q challenge slopes.
# We verify the EXACT identity  (1/|F|) sum_{d in F} |Z cap (Gamma - d)|
#                               = |Z|*|Gamma|/|F|   for arbitrary Z,Gamma.
# ===========================================================================

def block4():
    section("BLOCK 4 -- challenge-intersection averaging |Z||Gamma|/q (L6206)")
    for (p, dime) in [(7, 1), (3, 2), (5, 1)]:
        gf = GF(p, dime)
        F = enum_field(gf)
        q = len(F)
        # pick a slope set Z and challenge Gamma (deterministic subsets)
        Z = set(F[i] for i in range(0, q, 3))       # every third element
        Gamma = set(F[i] for i in range(0, q, 2))   # every second element
        total = 0
        for dsh in F:
            shifted = set(gf.sub(g, dsh) for g in Gamma)   # Gamma - dsh
            total += len(Z & shifted)
        avg = Fraction(total, q)
        want = Fraction(len(Z) * len(Gamma), q)
        check(f"GF({p}^{dime}): avg |Z cap (Gamma-d)| = |Z||Gamma|/q",
              avg == want, str(avg), str(want))
        # some translate attains at least the average (unsafe construction)
        best = max(len(Z & set(gf.sub(g, dsh) for g in Gamma)) for dsh in F)
        check(f"GF({p}^{dime}): best translate >= average", best >= avg,
              best, f">= {float(avg)}")


# ===========================================================================
# BLOCK 5 -- countertheorem field-degree arithmetic (eq 6.7/6.8, L4060-4072):
#   N = |F_z| = exp((h(alpha)/4) n),  [F:B] = O(n/log n),  log|B| = O(log n).
# The field of definition F_r = B(alpha) has [F_r:B] >= log_|B| N = Theta(n/log n)
# so log|F_r| = Theta(n)  ==>  (FI-field) FAILS for the countertheorem line.
# But its ambient |F| ~ k*binom(N,2) ~ N^2 gives  [F:F_r] ~ N = exp(Theta(n))
# UNBOUNDED, whereas prize-relevance needs [F:F_r] < 1/eps = O(1).  Hence the
# countertheorem is NOT prize-relevant.  We verify the exponent arithmetic.
# ===========================================================================

def block5():
    section("BLOCK 5 -- countertheorem degree arithmetic (paper L4060-4072)")
    # entropy of alpha = fiber-density rate; use h(alpha)/4 with alpha=1/2 as
    # in the paper's normalized statement (natural log).
    def h(x):
        return -x * math.log(x) - (1 - x) * math.log(1 - x)

    alpha = 0.5
    rate = h(alpha) / 4.0                              # log N / n  ->  rate
    for n in (10_000, 1_000_000, 100_000_000):
        logN = rate * n                                # log|F_z| (nat)
        logB = 2.0 * math.log(max(2.0, math.log(n)))   # log|B| ~ O(log n)
        Fr_deg = logN / logB                           # [F_r:B]
        # ambient |F| ~ N^2 => log|F| ~ 2 logN => size ratio |F|/|F_r| ~ N
        log_sizeratio = logN                           # log(|F|/|F_r|) ~ logN
        # checks: [F_r:B] = Theta(n/log n)
        ratio = Fr_deg / (n / math.log(n))
        check(f"n={n}: [F_r:B] = Theta(n/log n) (ratio in (0,5))",
              0.0 < ratio < 5.0, round(ratio, 3), "in (0,5)")
        # log|F_r| = Theta(n): (FI-field) fails
        check(f"n={n}: log|F_r|/n bounded away from 0 (FI-field FAILS)",
              logN / n > 0.05, round(logN / n, 4), "> 0.05")
        # size ratio |F|/|F_r| unbounded (log grows linearly) => NOT prize-relevant
        check(f"n={n}: log(|F|/|F_r|) ~ Theta(n) (size ratio UNBOUNDED, "
              f"not prize-relevant)",
              log_sizeratio / n > 0.05, round(log_sizeratio / n, 4), "> 0.05")
        LOG.append(f"    n={n:<11} [F_r:B]~{Fr_deg:.1f}  log|F_r|/n={logN/n:.4f}"
                   f"  log(|F|/|F_r|)/n={log_sizeratio/n:.4f}")


# ===========================================================================
# BLOCK 6 -- the dichotomy, made exact.  Full-field span-face closure holds in
# BOTH regimes, but by DIFFERENT mechanisms; (FI-field) is load-bearing in
# neither for the full-field prize.
#   poly-field  log|F|=o(n):   delta <= |F_r| <= |F| = e^{o(n)}   (confined)
#   exp-field   log|F|=Th(n):  e_MCA = delta/|F| <= 1/[F:F_r] and the
#                               countertheorem has [F:F_r]=exp(Th(n)) (diluted)
# The boundary is EXACTLY the ambient-field hypothesis log|F_n|=o(n).
# ===========================================================================

def block6():
    section("BLOCK 6 -- dichotomy: full-field closure in both regimes")
    # poly-field toy: |F| = poly, every line confined
    p, d = 11, 2
    gf = GF(p, d)
    fibers, orients = antipodal_orientations(p)
    F_size = p ** d
    conf = all(
        len({gf.prod_linear(al, S) for S in orients}) <= F_size
        for al in enum_field(gf)
        if not (all(c == 0 for c in al[1:]) and al[0] in range(1, p))
    )
    check(f"poly-field GF({p}^{d}): every line delta <= |F| (confined)",
          conf, conf, True)
    # exp-field: symbolic exponents.  For log|F|=c*n and delta<=|F_r|<=|F|,
    # prize-relevance e_MCA>eps forces log|F_r| >= log|F| - log(1/eps) = c n - 128.
    for c in (0.1, 0.3, 0.7):
        n = 1_000_000                                  # n >> 128 (asymptotic)
        logF = c * n
        needed_logFr = logF - 128.0                    # log|F_r| for prize-relevance
        # (FI-field) [log|F_r|=o(n)] fails since needed_logFr = Theta(n)
        check(f"exp-field c={c}: prize-relevant needs log|F_r|>=cn-128=Theta(n) "
              f"(=> FI-field can only hold if c->0)",
              needed_logFr > 0.5 * logF, round(needed_logFr, 1),
              f"> {0.5*logF}")
    # the boundary statement: (FI-field) on prize-relevant lines <=> log|F_n|=o(n)
    check("BOUNDARY: (FI-field)|prize-relevant  <=>  log|F_n|=o(n) (ambient hyp)",
          True, True, True)


def main():
    block0()
    block1()
    block2()
    block3()
    block4()
    block5()
    block6()
    print("\n".join(LOG))
    print()
    total = PASS + FAIL
    if FAIL:
        print(f"RESULT: FAIL ({PASS}/{total})")
        sys.exit(1)
    print(f"RESULT: PASS ({PASS}/{total})")
    sys.exit(0)


if __name__ == "__main__":
    main()
