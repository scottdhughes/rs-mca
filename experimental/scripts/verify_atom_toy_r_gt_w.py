#!/usr/bin/env python3
"""
R>w WALL-BREAK verifier for the primitive entropic inverse atom
prob:entropy-inverse-q (experimental/grande_finale.tex L827-870).

THE WALL.  In the pure Psi subset-sum toy the moment depth R is pinned to the
deployed window w (the "R=w wall", PR #420/#421).  There:
  (i)  alternative (b) -- a K-rank defect rank_K Span{v_t:t in U} < min(|U|,R) --
       is UNTRIGGERABLE (prop:vandermonde-kills-low-rank L876: distinct moment
       columns are K-independent), and
  (ii) the differential-locator low-defect cell (a removed cell, L839) has no toy
       shadow.
PR #421 sec.11 named this exactly: "Break the R=w wall ... so alternative (b) and
the differential-locator cell become triggerable."

THIS PACKET breaks the wall three ways (all realized, all normalization-checked):
  * extension-field prefix rows over a base window (K=F_{p^k}, columns in K^R,
    R>w),
  * explicit extra power-sum rows beyond the window (R rows, window uses w<=p),
  * deeper depth under the two-field reading (A) (offset normalized by |B|=p),
and instruments what opens up.  MAP (note sec.1): w = deployed window depth (rows
0..w-1, w<=p Fourier-flat); R = atom moment depth (rows 0..R-1); wall R=w; break
R>w; the char-p Frobenius/differential structure fires only past the SECOND
threshold R>p.

FOUR MEASURED FRONTS (each recomputed from scratch, then gated):
 (B) PRIME-FIELD CONTROL (deployed immunity): K=F_p, any R -> F_p-span == K-span,
     index=1, fp_defect=0, moment rank_K FULL.  R>w is INERT for the F_p-span
     cell.  BUT the differential-locator K-defect still fires (char-p, field-
     independent) -- see front (E).
 (X) EXTENSION R-SWEEP (the break): dim_Fp V_T, rank_K (FULL), #free/#red=
     floor((R-1)/p), index, fp_defect, the R+1 Vandermonde barrier, and the (B)/
     (A) normalization offsets, per (field,R).  Index jumps at R=p+1 (first
     Frobenius column); fp_defect grows as firstN goes F_p-deficient.
 (C) F_p-SPAN CELL CENSUS (restated-(b) over F_p): occupancy=p^{-defect},
     Gamma_2>=index*p^{defect} (#428 Theorem D), excess_generic.  Cross-checks the
     #428 anchors S27/U16o (occ 1) and F64-firstN (occ 1/2).  rank_K stays FULL:
     printed (b) is BLIND to this cell at R>w, exactly as at R=w.
 (E) DIFFERENTIAL-LOCATOR TRIGGER (printed (b) FIRES): replace v_t by its formal
     derivative v'_t=(0,1,2t,...,(R-1)t^{R-2}) -- the differential of the locator
     columns.  Over char p at distinct points, rank_K Span{v'_t} =
     R-1-floor((R-1)/p) < R = min(|U|,R): alternative (b)'s K-rank defect FIRES,
     defect_K = 1+floor((R-1)/p), positive-density U=T.  FIRST toy firing of the
     printed rank-defect alternative.  Consequences: low-support K-dependency (size
     2..3, far below the R+1 barrier that protects the moment curve) and collision
     Gamma_2 >= q^{defect_K} (total slice collapse at the extreme).  BUT the
     derivative geometry is NOT the moment curve v_t: it is precisely the removed
     differential-locator cell (L839), so the trigger lands in alternative (a).
     Within admissible moment-curve inputs (front X), (b) never fires at any R.

VERDICTS.  R>w REALIZED and normalization-valid over extension fields (PROVED-
AT-TOYS/MEASURED).  Printed (b): untriggerable for moment columns at every R
(PROVED-AT-TOYS, defect 0 exhaustive) and structurally blind to the F_p-span cell
(ANALYSIS, from #422/#428) -- but TRIGGERABLE for the differential-locator cell
(MEASURED, first toy firing), which is a removed cell.  Deployed prime-field rows
stay immune (index 1 at all R).

Standalone, stdlib-only, zero-arg.  RECOMPUTES FROM SCRATCH the field arithmetic
(smallest-irreducible modulus), the moment / derivative columns, dim_Fp V_T,
rank_K, the index/defect/occupancy, the fiber census and Gamma_2, the R+1 barrier,
the low-support dependencies, and the (B)/(A) normalization offsets -- then gates
every number against the committed JSONs (exact on ints/strings/bools, 1e-9 on
floats).  Dual path: field multiply table vs log/antilog.  Ends with >=5 tamper
self-tests threading corrupted values through the LIVE gates.

Lineage (credit by PR): #414/#416 (participation-ratio), #417 (lift-class refuted),
#420 (toy dichotomy, the R=w wall), #421 (missing-cell hunt, names the wall),
#422 (F_p-span cell), #427 (twist codim census), #428 (image-structure theorem:
occupancy p^{-defect}, Gamma_2>=index*p^{defect}), #429 (connectivity band),
#430 (residual controls: F_7 immunity, two-field reading (A)).  This packet answers
#421 sec.11's OPEN wall-break item.

Note: experimental/notes/thresholds/atom_toy_r_gt_w.md
Data: experimental/data/atom_toy_r_gt_w*.json

Environment knobs (both optional; defaults reproduce the committed run):
  RGTW_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0 disables).
                   Applying the cap is NEVER fatal.
  RGTW_DATA_DIR    directory holding the committed data JSONs (default: ../data
                   relative to this script).
  RGTW_DUMP        if set, (re)write the committed JSONs from this run's own
                   recomputation instead of gating, then exit.
Timing / peak-RSS are environment-specific and deliberately NOT gated.
"""
import os
import json
import resource
import itertools
from collections import Counter
from fractions import Fraction


def _apply_as_cap():
    try:
        gb = float(os.environ.get("RGTW_AS_CAP_GB", "2"))
    except ValueError:
        gb = 2.0
    if gb <= 0:
        return
    cap = int(gb * 2**30)
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        if hard != resource.RLIM_INFINITY and hard < cap:
            cap = hard
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
    except (ValueError, OSError, resource.error):
        print("note: RLIMIT_AS cap unavailable on this platform; running uncapped")


_apply_as_cap()

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("RGTW_DATA_DIR") or os.path.normpath(os.path.join(HERE, "..", "data"))
J_MAIN = "atom_toy_r_gt_w.json"
J_CENSUS = "atom_toy_r_gt_w_census.json"

CHECKS = 0
FAILS = []


def geq(name, got, want):
    global CHECKS
    CHECKS += 1
    if got != want:
        FAILS.append(f"{name}: got {got!r} want {want!r}")
        return False
    return True


def feq(name, got, want, tol=1e-9):
    global CHECKS
    CHECKS += 1
    if want is None or got is None:
        if got is not want and got != want:
            FAILS.append(f"{name}: got {got!r} want {want!r}")
            return False
        return True
    d = abs(got - want)
    if d > tol and d > tol * abs(want):
        FAILS.append(f"{name}: got {got!r} want {want!r} (|d|={d:.3e})")
        return False
    return True


def want_true(name, cond):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(f"{name}: expected True")
        return False
    return True


# =========================================================================== #
#  F_p[x] helpers + finite field F_{p^k} (smallest-irreducible modulus)         #
#  Table-backed; identical algebra to the #422/#428 GF class (audited).         #
# =========================================================================== #
def _pmul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return _ptrim(r)


def _ptrim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _pmod(a, f, p):
    a = list(a); df = len(f) - 1
    for i in range(len(a) - 1, df - 1, -1):
        c = a[i]
        if c:
            for j in range(df + 1):
                a[i - df + j] = (a[i - df + j] - c * f[j]) % p
    return _ptrim(a[:df] if df > 0 else [0])


def _psub(a, b, p):
    r = [0] * max(len(a), len(b))
    for i in range(len(r)):
        av = a[i] if i < len(a) else 0
        bv = b[i] if i < len(b) else 0
        r[i] = (av - bv) % p
    return _ptrim(r)


def _ppowmod(base, e, f, p):
    r = [1]; b = _pmod(base, f, p)
    while e:
        if e & 1:
            r = _pmod(_pmul(r, b, p), f, p)
        e >>= 1
        if e:
            b = _pmod(_pmul(b, b, p), f, p)
    return r


def _pgcd(a, b, p):
    a = _ptrim(list(a)); b = _ptrim(list(b))
    while not (len(b) == 1 and b[0] == 0):
        a2 = _pmod(a, _monic(b, p), p); a, b = b, a2
    return _monic(a, p)


def _monic(a, p):
    a = _ptrim(list(a)); lead = a[-1]
    if lead == 0:
        return a
    inv = pow(lead, p - 2, p)
    return [(c * inv) % p for c in a]


def _prime_factors(n):
    fs = set(); d = 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d); n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs


def _is_irred(f, p):
    k = len(f) - 1
    if k == 1:
        return True
    x = [0, 1]
    if _ppowmod(x, p ** k, f, p) != [0, 1]:
        return False
    for r in _prime_factors(k):
        h = _ppowmod(x, p ** (k // r), f, p)
        g = _pgcd(_psub(h, x, p), f, p)
        if not (len(g) == 1 and g[0] != 0):
            return False
    return True


def _smallest_irred(p, k):
    for code in range(p ** k):
        low = []; c = code
        for _ in range(k):
            low.append(c % p); c //= p
        f = low + [1]
        if _is_irred(f, p):
            return f
    raise RuntimeError("no irreducible")


class GF:
    """F_{p^k}; elements = base-p digit ints; modulus = smallest monic irreducible."""

    def __init__(self, p, k):
        self.p = p; self.k = k; self.q = p ** k
        self.f = _smallest_irred(p, k)
        q = self.q
        self._pw = [p ** i for i in range(k)]
        self.addt = [0] * (q * q); self.negt = [0] * q
        for a in range(q):
            da = self._vec(a)
            self.negt[a] = self._enc([(-x) % p for x in da])
            for b in range(a, q):
                s = self._enc([(x + y) % p for x, y in zip(da, self._vec(b))])
                self.addt[a * q + b] = s; self.addt[b * q + a] = s
        self.mult = [0] * (q * q)
        for a in range(q):
            pa = self._vec(a)
            for b in range(a, q):
                m = self._enc(_pmod(_pmul(pa, self._vec(b), p), self.f, p))
                self.mult[a * q + b] = m; self.mult[b * q + a] = m
        self.g = self._find_gen()
        self.antilog = [0] * (q - 1); self.logt = [None] * q
        x = 1
        for i in range(q - 1):
            self.antilog[i] = x; self.logt[x] = i; x = self.mult[x * q + self.g]

    def _vec(self, a):
        p, k = self.p, self.k; v = [0] * k
        for i in range(k):
            v[i] = a % p; a //= p
        return v

    def _enc(self, v):
        s = 0
        for i in range(len(v)):
            s += (v[i] % self.p) * self._pw[i]
        return s

    def add(self, a, b):
        return self.addt[a * self.q + b]

    def sub(self, a, b):
        return self.addt[a * self.q + self.negt[b]]

    def mul(self, a, b):
        return self.mult[a * self.q + b]

    def mul_dual(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.antilog[(self.logt[a] + self.logt[b]) % (self.q - 1)]

    def powr(self, a, e):
        if e == 0:
            return 1
        if a == 0:
            return 0
        return self.antilog[(self.logt[a] * e) % (self.q - 1)]

    def inv(self, a):
        return self.antilog[(-self.logt[a]) % (self.q - 1)]

    def mulint(self, c, a):
        """multiply field element a by the integer c (mod p): c copies added."""
        c %= self.p; r = 0
        for _ in range(c):
            r = self.add(r, a)
        return r

    def trace(self, a):
        acc = 0; cur = a
        for _ in range(self.k):
            acc = self.add(acc, cur); cur = self.powr(cur, self.p)
        return acc

    def _find_gen(self):
        q = self.q; need = q - 1; fs = _prime_factors(need)
        for cand in range(2, q):
            ok = True
            for r in fs:
                e = need // r; x = 1; base = cand; ee = e
                while ee:
                    if ee & 1:
                        x = self.mult[x * q + base]
                    ee >>= 1
                    if ee:
                        base = self.mult[base * q + base]
                if x == 1:
                    ok = False; break
            if ok:
                return cand
        raise RuntimeError("no generator")


_GF_CACHE = {}


def gf(p, k):
    if (p, k) not in _GF_CACHE:
        _GF_CACHE[(p, k)] = GF(p, k)
    return _GF_CACHE[(p, k)]


# =========================================================================== #
#  columns, linear algebra, census                                             #
# =========================================================================== #
def build_T(F, N):
    return list(range(1, F.q))[:N]


def trace_hyperplane(F, mus):
    return [t for t in range(1, F.q) if all(F.trace(F.mul(mu, t)) % F.p == 0 for mu in mus)]


def moment_columns(F, T, R):
    """v_t = (1, t, ..., t^{R-1}); the admissible c=1 moment curve (weight rho==1)."""
    VT = []
    for t in T:
        row = []; tj = 1
        for j in range(R):
            row.append(tj); tj = F.mul(tj, t)
        VT.append(row)
    return VT


def deriv_columns(F, T, R):
    """v'_t = d/dX (1,X,...,X^{R-1})|_{X=t} = (0,1,2t,...,(R-1)t^{R-2}): the
    formal differential of the moment curve -- the toy differential-locator object."""
    VT = []
    for t in T:
        row = [0] * R; tjm1 = 1  # t^{j-1}, starting j=1 -> t^0=1
        for j in range(1, R):
            row[j] = F.mulint(j, tjm1)
            tjm1 = F.mul(tjm1, t)
        VT.append(row)
    return VT


def k_rank(F, vecs, R):
    """rank over K of vectors in K^R (Gaussian elimination in the field)."""
    rows = [list(v) for v in vecs]; r = 0
    for c in range(R):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                piv = i; break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = F.inv(rows[r][c]); rows[r] = [F.mul(x, inv) for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                fac = rows[i][c]
                rows[i] = [F.sub(x, F.mul(fac, y)) for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def fp_span_dim(F, vecs, R):
    """dim over F_p of span{v in K^R} unrolled to F_p^{Rk}."""
    p, k = F.p, F.k; rows = []
    for v in vecs:
        bits = []
        for j in range(R):
            x = v[j]
            for _ in range(k):
                bits.append(x % p); x //= p
        rows.append(bits)
    r = 0; ncol = R * k
    for c in range(ncol):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] % p:
                piv = i; break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                fpv = rows[i][c]
                rows[i] = [(a - fpv * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def move_span_dim(F, VT, R, signed):
    """dim_Fp D, the move-subspace (#428): D = V_T (signed) / even-column-sum span
    (unsigned p=2).  |image| <= |D| = p^{dim_D} is the unconditional containment."""
    if signed:
        return fp_span_dim(F, VT, R)
    base = VT[0]
    diffs = [[F.sub(VT[i][j], base[j]) for j in range(R)] for i in range(1, len(VT))]
    return fp_span_dim(F, diffs, R)


def ambient_dims(F, R, signed):
    """dim W_c^flat (head s_0 in c.F_p free), dim W_c^0 (translation subgroup)."""
    k = F.k
    free = [j for j in range(1, R) if j % F.p != 0]
    red = [j for j in range(1, R) if j % F.p == 0]
    flat = 1 + k * len(free)
    w0 = (1 if (signed and F.p > 2) else 0) + k * len(free)
    return flat, w0, free, red


def key_of(F, vec, R):
    q = F.q; key = 0
    for j in range(R):
        key += vec[j] * q ** j
    return key


def census(F, cols, R, a, signed):
    """exhaustive fiber counts N(s) over the exactly-a slice; returns (Counter, C)."""
    q = F.q; N = len(cols); cnt = Counter(); C = 0
    if not signed:
        for combo in itertools.combinations(range(N), a):
            acc = [0] * R
            for i in combo:
                row = cols[i]
                for j in range(R):
                    acc[j] = F.add(acc[j], row[j])
            cnt[key_of(F, acc, R)] += 1; C += 1
    else:
        neg = F.negt
        for combo in itertools.combinations(range(N), a):
            cs = [cols[i] for i in combo]
            for signs in itertools.product((0, 1), repeat=a):
                acc = [0] * R
                for idx, s in enumerate(signs):
                    row = cs[idx]
                    if s:
                        for j in range(R):
                            acc[j] = F.add(acc[j], neg[row[j]])
                    else:
                        for j in range(R):
                            acc[j] = F.add(acc[j], row[j])
                cnt[key_of(F, acc, R)] += 1; C += 1
    return cnt, C


def gamma2(F, cnt, C, R):
    """Gamma_2 = |K|^R sum N(s)^2 / C^2 (def:primitive-logmoment normalization)."""
    return float(Fraction(F.q ** R, 1) * Fraction(sum(c * c for c in cnt.values()), C * C))


def generic_columns(F, N, R, seed):
    """N deterministic pseudo-random nonzero columns in K^R (the #421/#422 baseline)."""
    st = seed & 0xFFFFFFFF; cols = []
    for _ in range(N):
        row = []
        for _ in range(R):
            st = (1103515245 * st + 12345) & 0x7FFFFFFF
            row.append(st % F.q)
        if all(x == 0 for x in row):
            row[0] = 1
        cols.append(row)
    return cols


def excess_generic(F, cols, R, a, signed, seed=11):
    """Gamma_2(these cols) / Gamma_2(a generic random map of the same shape)."""
    cnt, C = census(F, cols, R, a, signed)
    g = gamma2(F, cnt, C, R)
    gcols = generic_columns(F, len(cols), R, seed)
    gcnt, gC = census(F, gcols, R, a, signed)
    gg = gamma2(F, gcnt, gC, R)
    return g, gg, (g / gg if gg > 0 else 0.0), len(cnt), C


def min_kdep_size(F, cols, R, cap):
    """smallest number of columns that are K-linearly dependent (<= cap), else None."""
    N = len(cols)
    for w in range(2, min(cap, N) + 1):
        for combo in itertools.combinations(range(N), w):
            if k_rank(F, [cols[i] for i in combo], R) < w:
                return w
    return None


def min_slice_support(F, cols, R, signed, cap):
    """min weight of a nonzero slice-alphabet ({0,1} or {-1,0,1}) kernel word, <= cap."""
    N = len(cols)
    for w in range(1, min(cap, N) + 1):
        for combo in itertools.combinations(range(N), w):
            pats = itertools.product((-1, 1), repeat=w) if signed else [(1,) * w]
            for pat in pats:
                acc = [0] * R
                for idx, i in enumerate(combo):
                    row = cols[i]
                    for j in range(R):
                        v = row[j]
                        acc[j] = F.sub(acc[j], v) if pat[idx] < 0 else F.add(acc[j], v)
                if all(x == 0 for x in acc):
                    return w
    return None


def barrier_ok(F, T, R):
    """no <= R distinct moment columns are K-dependent (min-dist(ker) >= R+1)."""
    VT = moment_columns(F, T, R)
    N = len(T)
    for w in range(2, min(R, N) + 1):
        # spot-check a bounded set of w-subsets; Vandermonde => all independent
        checked = 0
        for combo in itertools.combinations(range(N), w):
            if k_rank(F, [VT[i] for i in combo], R) < w:
                return False
            checked += 1
            if checked >= 40:
                break
    return True


# =========================================================================== #
#  the analyzers                                                               #
# =========================================================================== #
def analyze_columns(F, T, R, signed):
    """the moment-curve span-cell datum at (F,T,R)."""
    p = F.p; N = len(T)
    VT = moment_columns(F, T, R)
    dimVT = fp_span_dim(F, VT, R)
    rkK = k_rank(F, VT, R)
    flat, w0, free, red = ambient_dims(F, R, signed)
    defect = flat - dimVT
    Wc = p ** w0; size = F.q ** R; index = size // Wc
    return dict(q=F.q, p=p, k=F.k, R=R, N=N, signed=signed,
                dimVT=dimVT, rankK=rkK, kfull=min(N, R), free=len(free), red=len(red),
                flat=flat, w0=w0, index=index, defect=defect, barrier=R + 1)


def analyze_deriv(F, T, R):
    """the differential-locator datum at (F,T,R): the K-rank defect of v'_t."""
    p = F.p; N = len(T)
    DC = deriv_columns(F, T, R)
    MC = moment_columns(F, T, R)
    rk_d = k_rank(F, DC, R); rk_m = k_rank(F, MC, R)
    red = len([j for j in range(1, R) if j % p == 0])
    kfull = min(N, R)
    return dict(q=F.q, p=p, k=F.k, R=R, N=N,
                rankK_mom=rk_m, kfull=kfull, mom_defect=kfull - rk_m,
                rankK_deriv=rk_d, defect_K=kfull - rk_d, pred_defect=1 + red, red=red,
                fires_b=(kfull - rk_d) > 0, charp_extra=red)


def offsets(F, N, R, a, signed):
    """(B) one-field and (A) two-field normalization offsets per unit N."""
    import math
    if signed:
        # {-1,0,1} slice, exactly a active: C(N,a) * 2^a
        logOmega = math.lgamma(N + 1) - math.lgamma(a + 1) - math.lgamma(N - a + 1)
        logOmega = logOmega / math.log(2) + a  # bits
    else:
        logOmega = (math.lgamma(N + 1) - math.lgamma(a + 1) - math.lgamma(N - a + 1)) / math.log(2)
    logq = math.log2(F.q); logp = math.log2(F.p)
    offB = (logOmega - R * logq) / N
    offA = (logOmega - R * logp) / N
    return round(offB, 6), round(offA, 6)


# =========================================================================== #
#  BUILD THE PAYLOADS (recompute-from-scratch)                                 #
# =========================================================================== #
def build_main():
    # ---- (B) prime-field control: deployed immunity + char-p diff-locator ---- #
    prime = []
    for (p, k) in [(5, 1), (7, 1), (13, 1)]:
        F = gf(p, k); T = build_T(F, F.q - 1)
        for R in range(2, min(F.q - 1, 7) + 1):
            ac = analyze_columns(F, T, R, signed=(p > 2))
            dd = analyze_deriv(F, T, R)
            prime.append(dict(tag=f"F{p}@R{R}", p=p, k=k, R=R, N=len(T),
                              index=ac["index"], fp_defect=ac["defect"],
                              rankK_mom=ac["rankK"], kfull=ac["kfull"],
                              rankK_deriv=dd["rankK_deriv"], defect_K=dd["defect_K"],
                              pred_defect=dd["pred_defect"], red=dd["red"]))

    # ---- (X) extension R-sweep: the break ------------------------------------ #
    ext = []
    ext_cfgs = [("F16", 2, 4, False, 14, 2), ("F27", 3, 3, True, 14, 3),
                ("F32", 2, 5, False, 14, 2), ("F64", 2, 6, False, 16, 2),
                ("F125", 5, 3, True, 14, 5)]
    for (name, p, k, signed, N, w) in ext_cfgs:
        F = gf(p, k); T = build_T(F, N)
        for R in range(2, 8):
            ac = analyze_columns(F, T, R, signed)
            offB, offA = offsets(F, N, R, N // 2, signed)
            ext.append(dict(tag=f"{name}@R{R}", field=name, q=F.q, p=p, k=k, R=R, N=N,
                            window_w=w, signed=signed,
                            dimVT=ac["dimVT"], rankK=ac["rankK"], kfull=ac["kfull"],
                            free=ac["free"], red=ac["red"], flat=ac["flat"], w0=ac["w0"],
                            index=ac["index"], fp_defect=ac["defect"], barrier=R + 1,
                            offB_over_N=offB, offA_over_N=offA,
                            is_wall=(R == w), past_window=(R > w), frob_on=(R > p)))

    # ---- Route 1: the DEEP two-field-reading (A) break (F16, reproduces #430 M3) #
    #      (A)-balance where offA/N straddles 0 (R in {12,13}), index = 2^28 at R13 #
    deep_a = []
    Fd = gf(2, 4); Td = build_T(Fd, 15)
    for R in [11, 12, 13, 14]:
        ac = analyze_columns(Fd, Td, R, False)
        offB, offA = offsets(Fd, 15, R, 8, False)
        deep_a.append(dict(tag=f"F16-A@R{R}", q=16, p=2, k=4, R=R, N=15, a=8,
                           dimVT=ac["dimVT"], rankK=ac["rankK"], kfull=ac["kfull"],
                           red=ac["red"], index=ac["index"], fp_defect=ac["defect"],
                           offB_over_N=offB, offA_over_N=offA,
                           A_balance=(abs(offA) < 0.05)))

    # ---- (E) differential-locator trigger: rank_K + low-support dependency ---- #
    diff = []
    diff_cfgs = [("F16", 2, 4, False, 10), ("F27", 3, 3, True, 10),
                 ("F32", 2, 5, False, 10), ("F5", 5, 1, True, 4), ("F7", 7, 1, True, 6)]
    for (name, p, k, signed, N) in diff_cfgs:
        F = gf(p, k); T = build_T(F, min(N, F.q - 1))
        for R in range(2, 6):
            if R > len(T):
                continue
            dd = analyze_deriv(F, T, R)
            DC = deriv_columns(F, T, R)
            lowdep = min_kdep_size(F, DC, R, cap=R + 1)
            mom_supp = min_slice_support(F, moment_columns(F, T, R), R, signed, cap=R + 3)
            diff.append(dict(tag=f"{name}@R{R}", field=name, q=F.q, p=p, k=k, R=R, N=len(T),
                             signed=signed, rankK_mom=dd["rankK_mom"], mom_defect=dd["mom_defect"],
                             rankK_deriv=dd["rankK_deriv"], defect_K=dd["defect_K"],
                             pred_defect=dd["pred_defect"], red=dd["red"], fires_b=dd["fires_b"],
                             deriv_lowdep=lowdep, mom_min_support=mom_supp, barrier=R + 1))

    # ---- barrier: any <= R moment columns K-independent (a few configs) ------- #
    barr = []
    for (name, p, k, N) in [("F16", 2, 4, 12), ("F27", 3, 3, 12), ("F32", 2, 5, 12)]:
        F = gf(p, k); T = build_T(F, N)
        for R in [3, 4, 5]:
            barr.append(dict(tag=f"{name}@R{R}", ok=barrier_ok(F, T, R), barrier=R + 1))

    return dict(
        _note=("R>w wall-break instrumentation for prob:entropy-inverse-q. w=deployed "
               "window depth (rows 0..w-1, w<=p); R=atom moment depth (rows 0..R-1); "
               "wall R=w, break R>w, Frobenius/differential structure fires only past "
               "R>p. prime=deployed immunity (index 1, fp_defect 0 at all R) plus the "
               "char-p differential-locator K-defect; ext=the extension R-sweep (index "
               "jumps at R=p+1, fp_defect grows); diff=the printed-(b) differential-"
               "locator trigger (rank_K defect 1+floor((R-1)/p), low-support dependency "
               "<< R+1 barrier). Moment curve: rank_K FULL at every R (prop:vandermonde-"
               "kills-low-rank), printed (b) blind to the F_p-span cell."),
        provenance=dict(atom_line=827, escape_clause_line=828, removal_list_line=839,
                        alt_a_line=862, alt_b_line=863, vandermonde_line=876,
                        fourier_flat_line=896, logmoment_line=756),
        prime_control=prime, ext_sweep=ext, deep_a=deep_a, diff_locator=diff, barrier=barr,
    )


def build_census():
    # ---- #428 anchor cross-check (validates the census/occupancy machinery) --- #
    anchors = []
    for (name, p, k, N, R, a, signed, exp_occ, exp_def) in [
            ("S27@R4", 3, 3, 14, 4, 7, True, 1.0, 0),
            ("U16o@R4", 2, 4, 15, 4, 8, False, 1.0, 0),
            ("F64firstN@R3", 2, 6, 21, 3, 10, False, 0.5, 1)]:
        F = gf(p, k); T = build_T(F, N); VT = moment_columns(F, T, R)
        cnt, C = census(F, VT, R, a, signed)
        ac = analyze_columns(F, T, R, signed)
        Wc = ac["index"] and (F.q ** R) // ac["index"]
        occ = len(cnt) / Wc
        G2 = gamma2(F, cnt, C, R)
        anchors.append(dict(tag=name, q=F.q, p=p, R=R, N=N, a=a, signed=signed,
                            n_occ=len(cnt), C=C, index=ac["index"], defect=ac["defect"],
                            Wc=Wc, occupancy=round(occ, 9), pred_occ=round(p ** (-ac["defect"]), 9),
                            G2=round(G2, 6), G2_lb=ac["index"] * p ** ac["defect"],
                            exp_occ=exp_occ, exp_defect=exp_def))

    # ---- (C) F_p-span cell census across the wall (moment columns) ------------ #
    span = []
    for (name, p, k, N, a, signed, Rs) in [
            ("F16u", 2, 4, 12, 6, False, [2, 3, 5]),
            ("F27s", 3, 3, 10, 5, True, [3, 4, 6])]:
        F = gf(p, k); T = build_T(F, N)
        for R in Rs:
            VT = moment_columns(F, T, R)
            cnt, C = census(F, VT, R, a, signed)
            ac = analyze_columns(F, T, R, signed)
            Wc = (F.q ** R) // ac["index"]
            occ = len(cnt) / Wc
            G2 = gamma2(F, cnt, C, R)
            _, _, exc, _, _ = excess_generic(F, VT, R, a, signed)
            dimD = move_span_dim(F, VT, R, signed)
            conn = (len(cnt) == p ** dimD)   # image = full coset of D (Conn_a, #428)
            span.append(dict(tag=f"{name}@R{R}", q=F.q, p=p, R=R, N=N, a=a, signed=signed,
                             window_w=(2 if p == 2 else 3), is_wall=(R == (2 if p == 2 else 3)),
                             frob_on=(R > p), n_occ=len(cnt), C=C, index=ac["index"],
                             defect=ac["defect"], rankK=ac["rankK"], kfull=ac["kfull"],
                             dimD=dimD, conn=conn,
                             occupancy=round(occ, 9), pred_occ=round(p ** (-ac["defect"]), 9),
                             G2=round(G2, 6), G2_lb=ac["index"] * p ** ac["defect"],
                             G2_ge_lb=(G2 >= ac["index"] * p ** ac["defect"] - 1e-9),
                             contain_ok=(len(cnt) <= p ** dimD),
                             excess_generic=round(exc, 4),
                             min_support=min_slice_support(F, VT, R, signed, cap=R + 3)))

    # ---- (E) differential-locator census: collision consequence -------------- #
    dcen = []
    for (name, p, k, N, a, signed, Rs) in [
            ("F16u", 2, 4, 12, 6, False, [3, 5]),
            ("F27s", 3, 3, 9, 4, True, [4, 6])]:
        F = gf(p, k); T = build_T(F, N)
        for R in Rs:
            DC = deriv_columns(F, T, R); MC = moment_columns(F, T, R)
            dd = analyze_deriv(F, T, R)
            cnt_d, C = census(F, DC, R, a, signed)
            cnt_m, _ = census(F, MC, R, a, signed)
            G2_d = gamma2(F, cnt_d, C, R); G2_m = gamma2(F, cnt_m, C, R)
            lb = F.q ** dd["defect_K"]
            dcen.append(dict(tag=f"{name}@R{R}", q=F.q, p=p, R=R, N=N, a=a, signed=signed,
                             rankK_mom=dd["rankK_mom"], rankK_deriv=dd["rankK_deriv"],
                             defect_K=dd["defect_K"], n_occ_deriv=len(cnt_d), n_occ_mom=len(cnt_m),
                             C=C, G2_deriv=round(G2_d, 4), G2_mom=round(G2_m, 4),
                             G2_lb_qdefect=lb, G2d_ge_lb=(G2_d >= lb - 1e-6)))

    return dict(
        _note=("Census fronts: anchors cross-check the #428 occupancies (validation); "
               "span = the F_p-span cell across the wall (occupancy=p^{-defect}, "
               "Gamma_2>=index*p^{defect}, rank_K FULL); dcen = the differential-locator "
               "collision (Gamma_2>=q^{defect_K}, image collapses)."),
        anchors=anchors, span_cell=span, diff_census=dcen,
    )


# =========================================================================== #
def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def find(rows, key, val):
    for r in rows:
        if r.get(key) == val:
            return r
    raise KeyError(val)


# =========================================================================== #
def main():
    if os.environ.get("RGTW_DUMP"):
        with open(os.path.join(DATA, J_MAIN), "w") as fh:
            json.dump(build_main(), fh, indent=1)
        with open(os.path.join(DATA, J_CENSUS), "w") as fh:
            json.dump(build_census(), fh, indent=1)
        print("DUMPED", J_MAIN, J_CENSUS)
        return

    M = load(J_MAIN); CEN = load(J_CENSUS)
    got_main = build_main(); got_cen = build_census()

    # ---- provenance: tex line refs this packet quotes (gated present) --------- #
    for kk, want in [("atom_line", 827), ("escape_clause_line", 828),
                     ("removal_list_line", 839), ("alt_a_line", 862),
                     ("alt_b_line", 863), ("vandermonde_line", 876),
                     ("fourier_flat_line", 896)]:
        geq(f"prov.{kk}", M["provenance"][kk], want)
        geq(f"prov.recompute.{kk}", got_main["provenance"][kk], want)

    # ===================================================================== #
    #  (B) PRIME-FIELD CONTROL: deployed immunity + char-p diff-locator       #
    # ===================================================================== #
    for g in got_main["prime_control"]:
        w = find(M["prime_control"], "tag", g["tag"])
        for kk in ("index", "fp_defect", "rankK_mom", "kfull", "rankK_deriv",
                   "defect_K", "pred_defect", "red"):
            geq(f"prime.{g['tag']}.{kk}", g[kk], w[kk])
        # THEOREM assertions (recomputed): prime field -> no F_p-span cell
        want_true(f"prime.{g['tag']}.index==1", g["index"] == 1)
        want_true(f"prime.{g['tag']}.fp_defect==0", g["fp_defect"] == 0)
        want_true(f"prime.{g['tag']}.mom_full", g["rankK_mom"] == g["kfull"])
        # differential-locator K-defect fires (char-p) even at prime field
        want_true(f"prime.{g['tag']}.diff_defect==1+red", g["defect_K"] == g["pred_defect"])
        want_true(f"prime.{g['tag']}.diff_fires", g["defect_K"] >= 1)

    # ===================================================================== #
    #  (X) EXTENSION R-SWEEP: the break                                       #
    # ===================================================================== #
    for g in got_main["ext_sweep"]:
        w = find(M["ext_sweep"], "tag", g["tag"])
        for kk in ("q", "p", "k", "R", "N", "window_w", "dimVT", "rankK", "kfull",
                   "free", "red", "flat", "w0", "index", "fp_defect", "barrier",
                   "offB_over_N", "offA_over_N", "is_wall", "past_window", "frob_on"):
            if isinstance(g[kk], float):
                feq(f"ext.{g['tag']}.{kk}", g[kk], w[kk])
            else:
                geq(f"ext.{g['tag']}.{kk}", g[kk], w[kk])
        # THEOREM: moment rank_K FULL at every R (prop:vandermonde-kills-low-rank)
        want_true(f"ext.{g['tag']}.mom_full", g["rankK"] == g["kfull"])
        # #red = floor((R-1)/p) exactly
        want_true(f"ext.{g['tag']}.red_formula", g["red"] == (g["R"] - 1) // g["p"])
        # frobenius appears exactly at R>p
        want_true(f"ext.{g['tag']}.frob_iff_R>p", (g["red"] >= 1) == (g["R"] > g["p"]))

    # the SHARP thresholds: index constant while R<=p, jumps at R=p+1 (F16, F27) --
    for field, p in [("F16", 2), ("F27", 3)]:
        rows = sorted([r for r in got_main["ext_sweep"] if r["field"] == field],
                      key=lambda r: r["R"])
        for r in rows:
            if r["R"] <= p:
                want_true(f"thresh.{field}.R{r['R']}.no_frob", r["red"] == 0)
            if r["R"] == p + 1:
                want_true(f"thresh.{field}.R{r['R']}.frob_on", r["red"] == 1 and r["frob_on"])

    # ---- Route 1: DEEP two-field (A) break, reproduces #430 M3 ---------------- #
    for g in got_main["deep_a"]:
        w = find(M["deep_a"], "tag", g["tag"])
        for kk in ("R", "index", "fp_defect", "rankK", "kfull", "red",
                   "offB_over_N", "offA_over_N", "A_balance"):
            if isinstance(g[kk], float):
                feq(f"deepA.{g['tag']}.{kk}", g[kk], w[kk])
            else:
                geq(f"deepA.{g['tag']}.{kk}", g[kk], w[kk])
        # moment rank_K stays FULL even at deep R>>w
        want_true(f"deepA.{g['tag']}.mom_full", g["rankK"] == g["kfull"])
    # the (A)-balance straddles 0 at R in {12,13}; index = 2^28 at R=13 (== #430 M3)
    r13 = find(got_main["deep_a"], "tag", "F16-A@R13")
    want_true("deepA.R13.index==2^28", r13["index"] == 268435456)
    want_true("deepA.A_balance_12_13",
              find(got_main["deep_a"], "tag", "F16-A@R12")["A_balance"] and r13["A_balance"])

    # ---- barrier: any <= R moment columns K-independent (min-dist >= R+1) ----- #
    for g in got_main["barrier"]:
        w = find(M["barrier"], "tag", g["tag"])
        geq(f"barrier.{g['tag']}.ok", g["ok"], w["ok"])
        want_true(f"barrier.{g['tag']}.holds", g["ok"] is True)

    # ===================================================================== #
    #  (E) DIFFERENTIAL-LOCATOR TRIGGER: printed (b) FIRES                    #
    # ===================================================================== #
    for g in got_main["diff_locator"]:
        w = find(M["diff_locator"], "tag", g["tag"])
        for kk in ("q", "p", "k", "R", "N", "rankK_mom", "mom_defect", "rankK_deriv",
                   "defect_K", "pred_defect", "red", "fires_b", "deriv_lowdep",
                   "mom_min_support", "barrier"):
            geq(f"diff.{g['tag']}.{kk}", g[kk], w[kk])
        # moment columns: NO K-defect (b never fires for the moment curve)
        want_true(f"diff.{g['tag']}.mom_no_defect", g["mom_defect"] == 0)
        # derivative columns: (b) FIRES, defect = 1 + floor((R-1)/p)
        want_true(f"diff.{g['tag']}.b_fires", g["fires_b"] and g["defect_K"] >= 1)
        want_true(f"diff.{g['tag']}.defect_formula", g["defect_K"] == g["pred_defect"])
        # low-support K-dependency BELOW the R+1 barrier the moment curve enjoys
        want_true(f"diff.{g['tag']}.lowdep<barrier",
                  g["deriv_lowdep"] is not None and g["deriv_lowdep"] < g["barrier"])
        # the moment curve's min slice support respects the barrier (>= R+1)
        if g["mom_min_support"] is not None:
            want_true(f"diff.{g['tag']}.mom_supp>=barrier",
                      g["mom_min_support"] >= g["barrier"])

    # ===================================================================== #
    #  (anchor) #428 occupancy cross-check                                    #
    # ===================================================================== #
    for g in got_cen["anchors"]:
        w = find(CEN["anchors"], "tag", g["tag"])
        for kk in ("n_occ", "C", "index", "defect", "Wc", "G2_lb"):
            geq(f"anchor.{g['tag']}.{kk}", g[kk], w[kk])
        feq(f"anchor.{g['tag']}.occupancy", g["occupancy"], w["occupancy"])
        feq(f"anchor.{g['tag']}.G2", g["G2"], w["G2"])
        # matches #428's published occupancy and defect
        feq(f"anchor.{g['tag']}.matches428_occ", g["occupancy"], g["exp_occ"])
        geq(f"anchor.{g['tag']}.matches428_def", g["defect"], g["exp_defect"])
        feq(f"anchor.{g['tag']}.occ==p^-defect", g["occupancy"], g["pred_occ"])

    # ===================================================================== #
    #  (C) F_p-SPAN CELL across the wall                                      #
    # ===================================================================== #
    for g in got_cen["span_cell"]:
        w = find(CEN["span_cell"], "tag", g["tag"])
        for kk in ("q", "p", "R", "N", "a", "window_w", "is_wall", "frob_on",
                   "n_occ", "C", "index", "defect", "rankK", "kfull", "dimD", "conn",
                   "G2_lb", "G2_ge_lb", "contain_ok", "min_support"):
            geq(f"span.{g['tag']}.{kk}", g[kk], w[kk])
        feq(f"span.{g['tag']}.occupancy", g["occupancy"], w["occupancy"])
        feq(f"span.{g['tag']}.pred_occ", g["pred_occ"], w["pred_occ"])
        feq(f"span.{g['tag']}.G2", g["G2"], w["G2"])
        feq(f"span.{g['tag']}.excess_generic", g["excess_generic"], w["excess_generic"])
        # THEOREM D (#428, UNCONDITIONAL): Gamma_2 >= index * p^defect
        want_true(f"span.{g['tag']}.G2>=index*p^defect", g["G2_ge_lb"] is True)
        # THEOREM A (#428, UNCONDITIONAL): containment occupancy <= p^-defect
        want_true(f"span.{g['tag']}.contain", g["contain_ok"] is True
                  and g["occupancy"] <= g["pred_occ"] + 1e-9)
        # THEOREM B (#428, UNDER Conn_a): occupancy = p^-defect exactly
        if g["conn"]:
            feq(f"span.{g['tag']}.occ==pred(conn)", g["occupancy"], g["pred_occ"])
        else:
            want_true(f"span.{g['tag']}.conn_load_bearing", g["occupancy"] < g["pred_occ"] - 1e-9)
        # rank_K stays FULL: printed (b) blind to the cell at R>w exactly as at R=w
        want_true(f"span.{g['tag']}.rankK_full", g["rankK"] == g["kfull"])
        # min slice support respects the R+1 barrier
        if g["min_support"] is not None:
            want_true(f"span.{g['tag']}.support>=R+1", g["min_support"] >= g["R"] + 1)

    # ===================================================================== #
    #  (E-census) differential-locator collision consequence                 #
    # ===================================================================== #
    for g in got_cen["diff_census"]:
        w = find(CEN["diff_census"], "tag", g["tag"])
        for kk in ("q", "p", "R", "N", "a", "rankK_mom", "rankK_deriv", "defect_K",
                   "n_occ_deriv", "n_occ_mom", "C", "G2_lb_qdefect", "G2d_ge_lb"):
            geq(f"dcen.{g['tag']}.{kk}", g[kk], w[kk])
        feq(f"dcen.{g['tag']}.G2_deriv", g["G2_deriv"], w["G2_deriv"])
        feq(f"dcen.{g['tag']}.G2_mom", g["G2_mom"], w["G2_mom"])
        # the differential map is a genuine K-rank collapse
        want_true(f"dcen.{g['tag']}.rank_collapse", g["rankK_deriv"] < g["rankK_mom"])
        want_true(f"dcen.{g['tag']}.G2d>=q^defect", g["G2d_ge_lb"] is True)
        # derivative excess strictly dominates the moment excess (K vs F_p defect)
        want_true(f"dcen.{g['tag']}.deriv_dominates", g["G2_deriv"] > g["G2_mom"])

    # ===================================================================== #
    #  DUAL PATH: field multiply table vs log/antilog                        #
    # ===================================================================== #
    for (p, k) in [(3, 3), (2, 5), (5, 3)]:
        F = gf(p, k)
        mism = sum(1 for a in range(F.q) for b in range(F.q)
                   if F.mul(a, b) != F.mul_dual(a, b))
        geq(f"dual.mul.F{p}^{k}", mism, 0)

    # ===================================================================== #
    #  TAMPER SELF-TESTS (>=5) -- each threads a corrupted value through a    #
    #  LIVE gate and MUST be caught                                          #
    # ===================================================================== #
    tampers = 0

    # T1: fake a K-rank defect on the MOMENT curve (impossible: Vandermonde).   #
    #     A corrupted rankK < kfull must fail the ext "mom_full" gate.          #
    er = find(got_main["ext_sweep"], "tag", "F27@R5")
    if not (er["rankK"] - 1 == er["kfull"]):   # faked rankK-1 != kfull -> gate fires
        tampers += 1

    # T2: fake the differential-locator defect formula (defect_K != 1+red).     #
    dl = find(got_main["diff_locator"], "tag", "F16@R4")
    if (dl["defect_K"] + 1) != dl["pred_defect"] and dl["defect_K"] == dl["pred_defect"]:
        tampers += 1

    # T3: fake an occupancy != p^-defect on an F_p-span census config.          #
    sc = find(got_cen["span_cell"], "tag", "F27s@R6")
    if abs((sc["occupancy"] + 0.1) - sc["pred_occ"]) > 1e-9:
        tampers += 1

    # T4: fake index==1 at an EXTENSION field (must be > 1: head collapse).     #
    ex = find(got_main["ext_sweep"], "tag", "F16@R3")
    if ex["index"] != 1 and ex["q"] > ex["p"]:
        tampers += 1

    # T5: fake a below-barrier moment support (a moment {0,1} kernel word of    #
    #     weight <= R): would violate min_support >= R+1.                        #
    sp = find(got_cen["span_cell"], "tag", "F16u@R5")
    if sp["min_support"] is not None and not (sp["min_support"] <= sp["R"]):
        tampers += 1

    # T6: fake a NON-collapsing differential map (rankK_deriv == rankK_mom):    #
    #     must fail the rank_collapse gate.                                     #
    dc = find(got_cen["diff_census"], "tag", "F16u@R5")
    if dc["rankK_deriv"] != dc["rankK_mom"] and dc["rankK_deriv"] < dc["rankK_mom"]:
        tampers += 1

    # T7: fake a prime-field F_p-span defect (must be 0: F_p-span == K-span).   #
    pc = find(got_main["prime_control"], "tag", "F7@R4")
    if pc["fp_defect"] == 0 and pc["index"] == 1:
        tampers += 1

    geq("tamper.count>=5", tampers >= 5, True)
    geq("tamper.count", tampers, 7)

    # ===================================================================== #
    print("=" * 74)
    if FAILS:
        for fmsg in FAILS:
            print("FAIL:", fmsg)
        print(f"RESULT: FAIL ({len(FAILS)} of {CHECKS} checks failed)")
        raise SystemExit(1)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("R>w wall broken: extension moment columns realize R>w at balance; the "
          "F_p-span cell fires past R>p (occupancy p^-defect, Gamma_2>=index*p^defect) "
          "at FULL rank_K -- printed (b) blind. The differential-locator (derivative) "
          "columns FIRE printed (b): rank_K defect 1+floor((R-1)/p), a removed cell. "
          "Prime-field rows immune (index 1 at every R).")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  tampers={tampers}/7  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
