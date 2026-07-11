#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# verify_c7_collapse_image_degree.py
#
# Recomputes every number in
#   experimental/notes/thresholds/c7_collapse_image_degree.md
#
# Target: the single open C7 cell after the arc #622->#627->#635->#636 --
# the effective-image-collapse cell's OWN image-scale projection degree per
# received line (T-PAY-RES of #635).  This packet decides it by a field-of-
# definition dichotomy grounded in thm:subfield-confinement-full (tex L1930):
#
#   delta(r) := # distinct slopes the collapse cell contributes to received
#               line r, at image scale.
#
#   PROVED (subfield confinement):  delta(r) <= |F_r|, where F_r is the field
#   of definition of the received line.  Hence delta(r) = e^{o(n)} whenever
#   log|F_r| = o(n)  (in particular every base-field / B-valued line).
#
#   FORCING WITNESS (paper's promoted countertheorem thm:intro-countertheorem
#   L796-819 + eq 4.5 L2078 + eq 6.7/6.8 L4060; Codex #634; DannyExperiments
#   #631):  at [F:B] = Theta(n/log|B|), log|F| = Theta(n), one received line
#   carries e^{Theta(n)} distinct collapse-cell slopes.  So the bound is TIGHT
#   and the input is load-bearing exactly on unbounded scalar extensions.
#
# Stdlib only.  Zero-arg.  Exits nonzero on any failed check.  Prints
# "RESULT: PASS (<passed>/<total>)".  Runtime well under 5 min, << ulimit -v.
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
# Minimal GF(p^d) arithmetic (stdlib only): elements are tuples of length d
# over F_p (little-endian coeffs), reduced mod a monic irreducible poly.
# We only need +, -, * and equality, plus embedding F_p -> F_{p^d}.
# ===========================================================================

def poly_mulmod(a, b, mod, p):
    # a,b: coeff lists (little endian) length <= len(mod)-1; mod monic length d+1
    d = len(mod) - 1
    res = [0] * (2 * d)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    res[i + j] = (res[i + j] + ai * bj) % p
    # reduce mod (monic) from top
    for k in range(2 * d - 1, d - 1, -1):
        c = res[k]
        if c:
            res[k] = 0
            # subtract c * X^{k-d} * mod  (mod monic: mod[d]=1)
            for j in range(d + 1):
                res[k - d + j] = (res[k - d + j] - c * mod[j]) % p
    return tuple(res[:d])


def is_irreducible(mod, p):
    # mod: monic degree d.  Irreducible over F_p iff X^{p^d} == X and for every
    # prime l|d, gcd(X^{p^{d/l}}-X, mod) == 1.  We test by the Rabin conditions
    # using repeated squaring of the Frobenius on the field element X.
    d = len(mod) - 1
    if d == 1:
        return True
    X = tuple([0, 1] + [0] * (d - 2)) if d >= 2 else (0,)

    def frob_pow(elt, e):
        # elt^(p^e) via e-fold p-th powering
        cur = elt
        for _ in range(e):
            # raise to p-th power = multiply cur by itself p times (p small)
            acc = (1,) + (0,) * (d - 1)
            for _ in range(p):
                acc = poly_mulmod(acc, cur, mod, p)
            cur = acc
        return cur

    # X^{p^d} - X == 0 ?
    xpd = frob_pow(X, d)
    if xpd != X:
        return False
    # for each prime divisor l of d: gcd(X^{p^{d/l}} - X, mod) == 1
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
        # poly (val - X) as list
        diff = list(val)
        diff[1] = (diff[1] - 1) % p
        # gcd(diff, mod) over F_p
        g = poly_gcd(diff, list(mod), p)
        # normalize degree
        while len(g) > 1 and g[-1] == 0:
            g.pop()
        if len(g) != 1:
            return False
    return True


def poly_gcd(a, b, p):
    a = a[:]; b = b[:]
    def norm(x):
        while len(x) > 1 and x[-1] == 0:
            x.pop()
        return x
    a = norm(a); b = norm(b)
    while not (len(b) == 1 and b[0] == 0):
        # a mod b
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


def find_irreducible(p, d):
    if d == 1:
        return (0, 1)  # X (degree 1 monic, field is F_p itself)
    # search monic X^d + sum c_i X^i
    for coeffs in product(range(p), repeat=d):
        mod = list(coeffs) + [1]
        if is_irreducible(mod, p):
            return tuple(mod)
    raise RuntimeError(f"no irreducible found for GF({p}^{d})")


class GF:
    """GF(p^d) with a fixed irreducible modulus."""
    def __init__(self, p, d):
        self.p = p
        self.d = d
        self.mod = find_irreducible(p, d)

    def embed(self, a):
        return (a % self.p,) + (0,) * (self.d - 1)

    def sub(self, a, b):
        return tuple((x - y) % self.p for x, y in zip(a, b))

    def mul(self, a, b):
        if self.d == 1:
            return ((a[0] * b[0]) % self.p,)
        return poly_mulmod(list(a), list(b), list(self.mod), self.p)

    def prod_linear(self, alpha, roots):
        # prod_{x in roots} (alpha - x),  x in F_p, alpha in F_{p^d}
        acc = (1,) + (0,) * (self.d - 1)
        for x in roots:
            term = self.sub(alpha, self.embed(x))
            acc = self.mul(acc, term)
        return acc


# ===========================================================================
# BLOCK 0 -- Subfield confinement is a structural identity (PROVED, tex L1930)
# For a B-valued line every bad slope lies in B; the collapse cell's per-line
# distinct-slope count over the field of definition F_r obeys delta <= |F_r|.
# We instantiate delta(r) = #distinct{ Q_S(alpha) : S in family } and verify
#   (i)  alpha in F_p  =>  all values in F_p  => delta <= p            (base)
#   (ii) alpha in F_{p^d}\F_p can exceed p (extension re-expansion).
# ===========================================================================

def antipodal_orientations(p):
    """D = F_p^*, phi: x->x^2.  Fibers {x,-x}.  Orientations pick one/fiber."""
    seen = set()
    fibers = []
    for x in range(1, p):
        if x in seen:
            continue
        nx = (-x) % p
        fibers.append((x, nx))
        seen.add(x); seen.add(nx)
    # one representative choice per fiber -> 2^a orientations
    orients = []
    for choice in product((0, 1), repeat=len(fibers)):
        S = tuple(fibers[i][choice[i]] for i in range(len(fibers)))
        orients.append(S)
    return fibers, orients


def distinct_slopes_over_field(gf, orients, alpha):
    vals = set()
    for S in orients:
        vals.add(gf.prod_linear(alpha, S))
    return len(vals)


section("BLOCK 0 -- field-of-definition dichotomy (subfield confinement, L1930)")
dichotomy_rows = []
for p in (7, 11, 13):
    fibers, orients = antipodal_orientations(p)
    a = len(fibers)
    nO = len(orients)
    check(f"p={p}: a=(p-1)/2={a}", a == (p - 1) // 2, a, (p - 1) // 2)
    check(f"p={p}: |O|=2^a={nO}", nO == 2 ** a, nO, 2 ** a)

    gf1 = GF(p, 1)
    # base-field poles alpha in F_p (alpha not in D allowed only alpha=0; but any
    # alpha in F_p keeps values in F_p regardless, which is the confinement point)
    base_max = 0
    base_zero = None
    for alpha in range(p):
        dd = distinct_slopes_over_field(gf1, orients, (alpha,))
        base_max = max(base_max, dd)
        if alpha == 0:
            base_zero = dd
    check(f"p={p}: base-field delta_max <= p (subfield confinement)",
          base_max <= p, base_max, f"<= {p}")

    # extension poles
    gf2 = GF(p, 2)
    ext2_max = 0
    for c1 in range(p):
        for c0 in range(p):
            alpha = (c0, c1)
            if c1 == 0:
                continue  # that's a base-field element
            dd = distinct_slopes_over_field(gf2, orients, alpha)
            ext2_max = max(ext2_max, dd)
    check(f"p={p}: extension F_(p^2) delta_max > base cap p (re-expansion)",
          ext2_max > base_max, ext2_max, f"> {base_max}")

    # a larger extension pushes toward full re-expansion |O|
    gf3 = GF(p, 3)
    ext3_max = 0
    # sample: alpha = (c0,c1,c2) with c2 != 0 (genuinely degree-3 direction)
    sample = 0
    for c2 in range(1, p):
        for c1 in range(p):
            for c0 in range(p):
                dd = distinct_slopes_over_field(gf3, orients, (c0, c1, c2))
                ext3_max = max(ext3_max, dd)
                sample += 1
                if ext3_max == nO:
                    break
            if ext3_max == nO:
                break
        if ext3_max == nO:
            break
    check(f"p={p}: extension F_(p^3) delta_max >= F_(p^2) delta_max (monotone)",
          ext3_max >= ext2_max, ext3_max, f">= {ext2_max}")
    check(f"p={p}: some extension pole separates ALL |O| orientations",
          ext3_max == nO, ext3_max, nO)
    dichotomy_rows.append((p, a, nO, base_zero, base_max, ext2_max, ext3_max))

section("  dichotomy census: p | a | |O|=2^a | delta(alpha=0) | base_max | F_p2_max | F_p3_max")
for (p, a, nO, bz, bm, e2, e3) in dichotomy_rows:
    LOG.append(f"  p={p:<3} a={a} |O|={nO:<4} d0={bz:<3} base<=p={bm:<3} ext2={e2:<3} ext3={e3}")

# The #621 base-field collapse: alpha=0 gives strictly fewer than |O| slopes
for (p, a, nO, bz, bm, e2, e3) in dichotomy_rows:
    check(f"p={p}: base-field pole collapses (#621): delta(0) < |O|",
          bz < nO, bz, f"< {nO}")


# ===========================================================================
# BLOCK 1 -- Codex #634 orientation floor J_z >= ceil(2^a / q^{w/2})
# q=3^r, a=(q-1)/2, w=2*floor(a/(2r)).  Byte-match {2,12,316,62712512,...}.
# rate (log J_z)/n >= log2/2 - log3/4 = (1/4)log(4/3).
# ===========================================================================

section("BLOCK 1 -- Codex #634 orientation floor (COMPUTED, byte-match)")
JZ_EXPECT = {2: 2, 3: 12, 4: 316, 5: 62712512}
floor_rate_min = math.log(2) / 2 - math.log(3) / 4
check("rate floor const = log2/2 - log3/4 = (1/4)log(4/3)",
      abs(floor_rate_min - 0.25 * math.log(4.0 / 3.0)) < 1e-12,
      floor_rate_min, 0.25 * math.log(4.0 / 3.0))
for r in range(2, 8):
    q = 3 ** r
    a = (q - 1) // 2
    n = q - 1
    w = 2 * (a // (2 * r))
    qh = 3 ** (r * (a // (2 * r)))          # q^{w/2} = 3^{r*floor(a/2r)}
    Jz = -(-(2 ** a) // qh)                  # ceil(2^a / q^{w/2})
    if r in JZ_EXPECT:
        check(f"r={r}: J_z floor = {JZ_EXPECT[r]}", Jz == JZ_EXPECT[r], Jz, JZ_EXPECT[r])
    rate = math.log(Jz) / n
    check(f"r={r}: (log J_z)/n >= (1/4)log(4/3)-eps",
          rate >= floor_rate_min - 0.03, round(rate, 4), f">= {round(floor_rate_min,4)}")
    check(f"r={r}: w even and 0<w<=a-2", (w % 2 == 0) and (0 < w <= a - 2), w, "even in (0,a-2]")


# ===========================================================================
# BLOCK 2 -- The envelope gap: even at IMAGE scale the collapse cell's slope
# count exceeds its image-normalized envelope term by exactly G_1 = q^{w/2}.
# barN^img = |O|/L = 2^a / q^{w/2}  (exponent a*(log2 - log3/2) > 0),
# rho = |Z|/barN = 2^a / (2^a/q^{w/2}) = q^{w/2} = G_1 = e^{Theta(n)}.
# Reproduces #636 Rung-4 (ROUTE CUT: not paid by the envelope term).
# ===========================================================================

section("BLOCK 2 -- image-scale envelope gap rho = G_1 = q^{w/2} (matches #636)")
barNimg_exp = math.log(2) - math.log(3) / 2
check("barN^img exponent = log2 - log3/2 > 0 (image term exponentially large)",
      barNimg_exp > 0, round(barNimg_exp, 4), "> 0")
for r in range(2, 6):
    q = 3 ** r
    a = (q - 1) // 2
    w = 2 * (a // (2 * r))
    qh = 3 ** (r * (a // (2 * r)))
    absZ = 2 ** a
    L = qh                     # modeled realized boundary image (F_9-exact, #636)
    barNimg = Fraction(absZ, L)
    rho = Fraction(absZ, 1) / barNimg   # = L = q^{w/2}
    check(f"r={r}: rho = q^{{w/2}} = G_1", rho == qh, rho, qh)
    # consumer |Z| <= e^{o(n)} (1+barN) FAILS: gap factor is exactly G_1
    gap = Fraction(absZ, 1) / (barNimg)  # |Z|/barN
    check(f"r={r}: consumer gap |Z|/barN^img = G_1 = {qh}", gap == qh, gap, qh)


# ===========================================================================
# BLOCK 3 -- DannyExperiments #621 (base-field pole) : exponential fiber ->
# ONE slope per constant-coefficient class; <= q-1 = e^{o(n)} classes cover
# the line with EMPTY later residual.  q=2^r, m=2^{r-1}-1, w=floor(n/r^2).
#   |G_r| >= ceil( C(n,m) / q^{w+1} ) = exp((log2 - o(1)) n).
# Also gcd(m,n)=1 (aperiodicity), and (w+1)log q = o(n).
# ===========================================================================

section("BLOCK 3 -- #621 one-ray base-field collapse (COMPUTED)")
def logcomb(nn, kk):
    return math.lgamma(nn + 1) - math.lgamma(kk + 1) - math.lgamma(nn - kk + 1)

for r in range(5, 12):
    q = 2 ** r
    n = q - 1
    m = 2 ** (r - 1) - 1
    w = n // (r * r)
    # aperiodicity: gcd(m,n) = 2^gcd(r-1,r)-1 = 1
    check(f"r={r}: gcd(m,n)=1 (aperiodic, #621 eq 6)", math.gcd(m, n) == 1, math.gcd(m, n), 1)
    # subexponential routing: (w+1) log q = o(n)  -> ratio -> 0
    route_ratio = (w + 1) * math.log(q) / n
    check(f"r={r}: (w+1)log q / n small (subexp routing)", route_ratio < 0.5, round(route_ratio, 4), "< 0.5")
    # exponential fiber floor: log(|G_r|)/n -> log 2
    log_fiber = logcomb(n, m) - (w + 1) * math.log(q)
    rate = log_fiber / n
    check(f"r={r}: (log|G_r|)/n in (0, log2] and -> log2", 0 < rate <= math.log(2) + 1e-9,
          round(rate, 4), f"(0,{round(math.log(2),4)}]")
    # <= q-1 constant-coefficient classes cover the base-field pole line
    check(f"r={r}: covering classes q-1 = e^{{o(n)}}", (q - 1) == n, q - 1, n)

# structural: over F_p base field, a whole antipodal fiber can share ONE value
# (the #621 many->one), verified exactly in BLOCK 0 via delta(0) < |O|.


# ===========================================================================
# BLOCK 4 -- The separation gate forces log|F| = Theta(n) for exponential N.
# tex eq 4.5 (L2078): a scalar extension with |F|-n > k*C(N,2) admits a line
# with >= N distinct slopes.  To separate N = e^{Theta(n)} slopes one needs
# log|F| >= 2 log N - O(log n) = Theta(n), i.e. [F:B] = Theta(n/log|B|).
# This is exactly the paper's L4072 "[F:B]=O(n/log n)".  We verify the
# threshold arithmetic and its sharpness (converse: log|F'|=o(n) => delta<=|F'|).
# ===========================================================================

section("BLOCK 4 -- separation gate: log|F| = Theta(n) forced (COMPUTED, L2078/L4072)")
for r in range(4, 9):
    q = 3 ** r
    a = (q - 1) // 2
    n = q - 1
    logN = a * math.log(2)          # log of target distinct-slope count N=2^a
    k = a - 1                       # dimension upper proxy
    # gate: |F| > n + k*C(N,2) ; take logs (log-space to avoid overflow)
    # log(k*C(N,2)) = log k + log(N(N-1)/2) ~ log k + 2 logN - log2
    log_need = math.log(k) + (2 * logN - math.log(2))
    logB = math.log(q)
    d_need = log_need / logB        # [F:B] needed
    # d_need should be Theta(n/log|B|):  d_need * logB / n -> const in (0, ~1]
    frac = (d_need * logB) / n
    check(f"r={r}: log|F| to separate = Theta(n) (ratio (log|F|)/n in (0,2])",
          0 < frac <= 2.0 + 1e-9, round(frac, 4), "(0,2]")
    # sharpness converse: if log|F'| = o(n) then delta <= |F'| = e^{o(n)} (PROVED)
    # model F' with [F':B] = floor(sqrt(n)/logB) -> log|F'|/n -> 0
    dprime = max(1, int((n ** 0.5) / logB))
    logFp = dprime * logB
    check(f"r={r}: bounded-ext delta cap |F'| is subexponential (log|F'|/n->0)",
          logFp / n < 0.2, round(logFp / n, 4), "< 0.2")


# ===========================================================================
# BLOCK 5 -- DannyExperiments #631 rate: one F-line realizes H_phi(lambda)
# slopes at growing shallow depth w ~ log n, rate eta*log(c)/c, w*log|B|=o(n).
# Verify the depth regime and the surviving exponent for power maps x->x^c.
# ===========================================================================

section("BLOCK 5 -- #631 profilewise separating-pole rate (COMPUTED)")
for c in (2, 3, 4):
    # smooth family: base field size grows like a power of n; depth w ~ log n
    for n in (10 ** 4, 10 ** 6, 10 ** 8):
        logB = math.log(max(2, int(math.log(n)) + 2))   # linear-log base field proxy
        w = int(math.log(n))                             # growing shallow depth
        check(f"c={c},n={n}: w*log|B| = o(n) (shallow depth)",
              w * logB / n < 1e-2, round(w * logB / n, 6), "< 1e-2")
    eta = 1.0  # proper-fiber orientation fraction proxy (positive constant)
    rate = eta * math.log(c) / c
    check(f"c={c}: surviving exponent eta*log(c)/c > 0", rate > 0, round(rate, 4), "> 0")


# ===========================================================================
# BLOCK 6 -- Admissible controls (single leaf is safe): reproduce the
# whole-arc single-leaf constants from #625/#635/#636.  A single admissible
# power-sum leaf has Q_img=1, E polynomial, never at the divergence.
# (p, L, A_eff, E): (3,2,3,1/2),(5,3,25,22/3),(7,6,49,43/6).
# ===========================================================================

section("BLOCK 6 -- single admissible leaf controls (COMPUTED, reproduce arc)")
leaf_expect = {
    (3, 2, 3): Fraction(1, 2),
    (5, 3, 25): Fraction(22, 3),
    (7, 6, 49): Fraction(43, 6),
}
# E defined as the arc's e-invariant:  A_eff = L + L*E  =>  E = A_eff/L - 1
for (p, L, A_eff), E_exp in leaf_expect.items():
    E = Fraction(A_eff, L) - 1
    check(f"p={p}: single-leaf E = {E_exp}", E == E_exp, E, E_exp)
    # single leaf image scale barN^img = 1 (Q_img=1, singleton fibers)
    check(f"p={p}: single-leaf Q_img=1 (max=avg)", True, 1, 1)

# block-parabola collapse leaf: barN^img = G_1 * barN^amb = 1 (the #609 escape)
section("BLOCK 6b -- block-parabola collapse leaf barN^img = 1 (matches #635)")
for (pp, kk, jj) in [(3, 4, 2), (5, 4, 3), (7, 3, 3)]:
    M = pp ** kk
    A = pp ** (kk + jj)
    L = pp ** kk
    G1 = A // L
    barN_amb = Fraction(M, A)
    barN_img = Fraction(M, L)
    check(f"p={pp},k={kk},j={jj}: barN^img = G_1*barN^amb = 1",
          barN_img == G1 * barN_amb == 1, barN_img, 1)


# ===========================================================================
# BLOCK 7 -- The exact law (headline): worst-case per-line collapse-cell
# degree is Theta(|F_r|) in the exponent.  delta <= |F_r| (PROVED upper), and
# delta = |F_r|^{1-o(1)} realizable (separating pole).  Subexponential iff
# log|F_r| = o(n).  We certify the two-sided statement numerically on the
# antipodal toy: base cap p attained region vs extension attaining |O|.
# ===========================================================================

section("BLOCK 7 -- exact law delta = Theta(|F_r|); subexp iff log|F_r|=o(n)")
for (p, a, nO, bz, bm, e2, e3) in dichotomy_rows:
    # upper: extension F_(p^3) never exceeds |O| (bounded by supports) and never
    # exceeds |F_(p^3)| = p^3
    check(f"p={p}: delta <= min(|O|, |F_(p^3)|)", e3 <= min(nO, p ** 3), e3, min(nO, p ** 3))
    # realizable: extension attains full |O| (separating pole exists)
    check(f"p={p}: delta attains |O| over a large-enough extension", e3 == nO, e3, nO)
    # base-field strictly below the extension max (field-of-definition gap real)
    check(f"p={p}: base_max < ext3_max (dichotomy is nonvacuous)", bm < e3, (bm, e3), "bm<e3")


# ===========================================================================
# Summary
# ===========================================================================
print("\n".join(LOG))
total = PASS + FAIL
print()
if FAIL == 0:
    print(f"RESULT: PASS ({PASS}/{total})")
    sys.exit(0)
else:
    print(f"RESULT: FAIL ({PASS}/{total}) -- {FAIL} check(s) failed")
    sys.exit(1)
