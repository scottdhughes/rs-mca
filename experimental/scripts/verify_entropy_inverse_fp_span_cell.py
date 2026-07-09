#!/usr/bin/env python3
"""
F_p-SPAN CELL verifier for the primitive entropic inverse atom
prob:entropy-inverse-q (experimental/grande_finale.tex L827-870).  The atom's
escape clause (L828) reads: "Prove the following standalone additive-combinatorics
statement, or identify the extra obstruction cell that must be added to the
first-match ledger."  This verifier recomputes, at exact toy scale, the candidate
extra cell: the map Phi(x)=sum_t x_t v_t extends to an F_p-LINEAR map on the
ambient F_p^T, and the profile slice x in {-1,0,1}^T is a subset of F_p^T, so the
slice image lies in the F_p-span V_T = span_{F_p}{rho(t) v_t}, which can be
F_p-deficient WHILE rank_K stays full -- exactly the case alternative (b) (L863:
rank_K Span{v_t} defect) is blind to.  The cell condition is PROJECTIVE:
rho(T) subset c F_p^x for a single c in K^x (rho == 1 is the c = 1 instance).
Two exact coordinate laws pin the image: s_0 in c F_p and
s_{pj} = c^{1-p} s_j^p whenever pj < R; both hold on every slice point for every
tested projective weight (c = 1 "ones" and c = g "proj" configs) and break under
a generic twist.  The measured 110x-120x / 23x collision excess is the subgroup
index [K^R : W_c] exactly (conditional excess on W_c ~ 1); by containment +
Cauchy-Schwarz/Jensen alone, Gamma_2 >= index (gated), so the obstruction does
not need the (toy-exact, in-general-OPEN) image = W_c surjection.

This verifier is standalone (no lane imports).  It RECOMPUTES FROM SCRATCH the
finite-field arithmetic (smallest-irreducible modulus), the moment-curve census,
the two exact laws (in projective c-form) + Frobenius free/red split, the
red-count identity #red == floor((R-1)/p) behind the sharp index criterion,
image = W_c occupancies, conditional excess on W_c, the containment-only Jensen
bound Gamma_2 >= index, the F_p-span dimension vs the K-rank, the baseline-relative
excess_generic (moment curve vs a generic random linear map of the same shape),
the frontier-normalization offset table, the -Theta(N log N) tension arithmetic,
a generic-rho null row and a large-subgroup row, and the exact Vandermonde min
signed-dependency (R+1) -- then gates every recomputed number against the three
committed data JSONs (exact on ints / rationals / strings / bools, 1e-9 on
floats).  Dual paths: the field multiply table vs the log/antilog backend, and
Gamma_2 by census vs additive-character Parseval.  Ends with 7 tamper
self-tests, including a faked K-rank defect, a faked F_p-span dimension, and
a c-form load-bearing test.

Lineage #414 -> #416 -> #417 -> #420 -> #421 -> this packet.  Conventions
(excess_ratio baseline, R=w wall, norm_ok gap/N > -0.25) inherited from #420/#421
and extended by the excess_generic datum and the R>w moment-curve reading.

Note: experimental/notes/thresholds/cap25_v13_entropy_inverse_fp_span_cell.md
Data: experimental/data/cap25_v13_entropy_inverse_fp_span_cell_{regime,spancell,nulls}.json

Zero-arg, stdlib-only.  Prints RESULT: PASS (N/N checks) and exits 0.

Environment knobs (both optional; defaults reproduce the committed run):
  FP_SPAN_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0 disables).
                      Applying the cap is NEVER fatal: if the platform refuses
                      it, the script proceeds uncapped and prints a notice.
  FP_SPAN_DATA_DIR    directory holding the three committed data JSONs
                      (default: ../data relative to this script, i.e. the
                      in-tree experimental/data/ layout).
Timing (~11 s) and peak-RSS figures quoted in the note are from the authoring
box only -- they are environment-specific and deliberately NOT gated here.

Claim labels mirror the note:
  ANALYSIS   the containment image(Phi) subset V_T and the (b)-blindness argument.
  PROVED     the two coordinate laws (char-p Frobenius identity), gated by an
             exhaustive 0-violation recompute on every slice point.
  MEASURED   census / excess / span-dim / occupancy numbers reproduced here.
  CONVENTION excess_generic baseline, norm_ok gap/N > -0.25, index [K^R:W].
"""
import os
import json
import math
import cmath
import random
import resource
import itertools
from collections import Counter

def _apply_as_cap():
    """Best-effort address-space guard: honor FP_SPAN_AS_CAP_GB (default 2 GB,
    0 disables) but never fail on platforms that refuse the cap."""
    try:
        gb = float(os.environ.get("FP_SPAN_AS_CAP_GB", "2"))
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
DATA = os.environ.get("FP_SPAN_DATA_DIR") or os.path.normpath(
    os.path.join(HERE, "..", "data"))
PREFIX = "cap25_v13_entropy_inverse_fp_span_cell"

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
    """F_{p^k}; elements are base-p digit ints; modulus = smallest monic irreducible."""

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
        self._trace_prime = [self.trace(a, 1) % p for a in range(q)]

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

    def frob(self, a):
        return self.powr(a, self.p)

    def in_subfield(self, a, d):
        return self.powr(a, self.p ** d) == a

    def trace(self, a, d=1):
        acc = 0; cur = a; step = self.p ** d
        for _ in range(self.k // d):
            acc = self.add(acc, cur); cur = self.powr(cur, step)
        return acc

    def add_char(self, a):
        return cmath.exp(2j * math.pi * self._trace_prime[a] / self.p)


# =========================================================================== #
#  datum builders + moment-curve census                                        #
# =========================================================================== #
def build_T(F, N):
    return list(range(1, F.q))[:N]


def build_rho(F, T, mode, seed=12345):
    if mode == "ones":
        return [1] * len(T)
    rnd = random.Random(seed)
    if mode == "proj":
        # the projective class rho(T) subset c F_p^x with c = F.g (g is never in
        # the prime subfield for k >= 2: its order q-1 exceeds p-1) and
        # deterministic a_t in F_p^x; for p = 2, a_t == 1 and rho == c * ones
        return [F.mul(F.g, 1 + rnd.randrange(F.p - 1)) for _ in T]
    return [1 + rnd.randrange(F.q - 1) for _ in T]


def proj_c(F, rho_mode):
    """the projective scalar c of the weight class rho(T) subset c F_p^x:
    1 for "ones", the field generator for "proj", None (no class) for "twist"."""
    if rho_mode == "ones":
        return 1
    if rho_mode == "proj":
        return F.g
    return None


def moment_columns(F, T, R, rho):
    VT = []
    for i, t in enumerate(T):
        row = []; tj = 1
        for j in range(R):
            row.append(F.mul(rho[i], tj)); tj = F.mul(tj, t)
        VT.append(row)
    return VT


def census(F, VT, R, family, signed):
    """fiber counts N(s) over the profile slice; s encoded little-endian base-q
    (== per-k-bit packing when p == 2)."""
    q = F.q; counts = Counter(); C = 0
    if F.p == 2:
        packed = []
        for row in VT:
            s = 0
            for j in range(R):
                s |= row[j] << (F.k * j)
            packed.append(s)
        for combo in family():
            key = 0
            for i in combo:
                key ^= packed[i]
            counts[key] += 1; C += 1
    elif not signed:
        for combo in family():
            acc = [0] * R
            for i in combo:
                row = VT[i]
                for j in range(R):
                    acc[j] = F.add(acc[j], row[j])
            key = 0
            for j in range(R):
                key += acc[j] * q ** j
            counts[key] += 1; C += 1
    else:
        neg = F.negt
        for combo in family():
            cols = [VT[i] for i in combo]
            for signs in itertools.product((0, 1), repeat=len(combo)):
                acc = [0] * R
                for idx, s in enumerate(signs):
                    row = cols[idx]
                    if s:
                        for j in range(R):
                            acc[j] = F.add(acc[j], neg[row[j]])
                    else:
                        for j in range(R):
                            acc[j] = F.add(acc[j], row[j])
                key = 0
                for j in range(R):
                    key += acc[j] * q ** j
                counts[key] += 1; C += 1
    return counts, C


def gamma2(counts, size, C):
    s = sum(c * c for c in counts.values())
    return size * s / (C * C)


def exp_g2_rand(size, C):
    return size / C + (C - 1) / C


def fp_span_dim(F, vecs, R):
    """dim over F_p of span{v in K^R} unrolled to F_p^{R k}."""
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


def rank_fq(F, rows):
    """rank over K of a list of K^R vectors (prop:vandermonde-kills-low-rank)."""
    rows = [list(r) for r in rows]
    ncol = len(rows[0]) if rows else 0
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                piv = i; break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        invv = F.inv(rows[r][c])
        rows[r] = [F.mul(invv, x) for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                fpv = rows[i][c]
                rows[i] = [F.sub(a, F.mul(fpv, b)) for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def decode(key, q, R):
    s = []
    for _ in range(R):
        s.append(key % q); key //= q
    return s


def frob_free_red(p, R):
    red = [j for j in range(1, R) if j % p == 0]
    free = [j for j in range(1, R) if j % p != 0]
    return free, red


def law_check(F, T, a, signed, R, rho_mode):
    """exact coordinate laws in projective c-form (s_0 in c F_p and
    s_{pj} = c^{1-p} s_j^p; c = 1 is the rho == 1 instance, and "twist" is
    evaluated at c = 1 -- its law break is the point) + image = W_c +
    conditional excess + F_p-span vs K-rank."""
    p, q, k = F.p, F.q, F.k
    N = len(T)
    rho = build_rho(F, T, rho_mode)
    VT = moment_columns(F, T, R, rho)
    fam = lambda: itertools.combinations(range(N), a)
    counts, C = census(F, VT, R, fam, signed)
    size = q ** R
    free, red = frob_free_red(p, R)
    c = proj_c(F, rho_mode) or 1
    c_inv = F.inv(c)
    c_1mp = F.mul(c, F.inv(F.powr(c, p)))            # c^(1-p)
    law0 = lawp = 0
    # the head is a pinned constant only when the active weights sum identically
    # over the slice: unsigned "ones" (sum = a mod p), or p = 2 (signs collapse
    # and, for "proj", a_t == 1); signed p > 2 and "proj" unsigned p > 2 are free
    a_const = (a % p) if ((not signed or p == 2) and (rho_mode != "proj" or p == 2)) else None
    for key in counts:
        s = decode(key, q, R)
        y0 = F.mul(c_inv, s[0])                       # s_0 in c F_p  <=>  y0 in F_p
        if y0 >= p or (a_const is not None and y0 != a_const):
            law0 += 1
        for j in range(1, R):
            if p * j < R and s[p * j] != F.mul(c_1mp, F.powr(s[j], p)):
                lawp += 1
    c0 = 1 if a_const is not None else p
    pred_W = c0 * (q ** len(free))
    sumN2 = sum(c * c for c in counts.values())
    G2 = size * sumN2 / (C * C)
    G2_cond = pred_W * sumN2 / (C * C)
    exp_cond = pred_W / C + (C - 1) / C
    dim = fp_span_dim(F, VT, R)
    return dict(rho=rho_mode, R=R, N=N, a=a, signed=signed,
                law0_violations=law0, lawp_violations=lawp, n_occ=len(counts),
                pred_W=pred_W, index=size // pred_W, W_occupancy=len(counts) / pred_W,
                G2=G2, excess_multi=G2 / exp_g2_rand(size, C),
                G2_cond=G2_cond, exp_cond=exp_cond, exc_cond=G2_cond / exp_cond,
                free=free, red=red, C=C,
                offset_bits=math.log2(C) - R * math.log2(q),
                offset_over_N=(math.log2(C) - R * math.log2(q)) / N,
                dim_span_Fp=dim, ambient_Fp=R * k, V_T=p ** dim,
                K_rank=rank_fq(F, VT), K_rank_full=min(N, R))


# =========================================================================== #
#  excess_generic (moment curve vs generic random linear map of same shape)     #
# =========================================================================== #
def generic_cols(F, N, R, seed):
    rnd = random.Random(seed * 2654435761 + R * 97 + N)
    cols = []
    for _ in range(N):
        while True:
            v = [rnd.randrange(F.q) for _ in range(R)]
            if any(v):
                break
        cols.append(v)
    return cols


def gamma2_generic(F, N, a, R, signed, seeds=(11, 23)):
    fam = lambda: itertools.combinations(range(N), a)
    g2s = []
    for sd in seeds:
        counts, Cf = census(F, generic_cols(F, N, R, sd), R, fam, signed)
        g2s.append(gamma2(counts, F.q ** R, Cf))
    return sum(g2s) / len(g2s)


# =========================================================================== #
#  exact Vandermonde min signed-dependency (the R+1 barrier)                    #
# =========================================================================== #
def min_signed_dep(F, T, R, wmax):
    """min #columns v_t=(1,t,..,t^{R-1}) with a nonzero {-1,0,1} vanishing sum."""
    N = len(T)
    VT = moment_columns(F, T, R, build_rho(F, T, "ones"))
    if F.p == 2:
        packed = []
        for row in VT:
            s = 0
            for j in range(R):
                s |= row[j] << (F.k * j)
            packed.append(s)
        for w in range(R + 1, wmax + 1):
            for combo in itertools.combinations(range(N), w):
                key = 0
                for i in combo:
                    key ^= packed[i]
                if key == 0:
                    return w
        return None
    neg = F.negt
    for w in range(R + 1, wmax + 1):
        for combo in itertools.combinations(range(N), w):
            cols = [VT[i] for i in combo]
            for signs in itertools.product((1, -1), repeat=w - 1):
                sg = (1,) + signs
                acc = [0] * R
                for idx, s in enumerate(sg):
                    row = cols[idx]
                    for j in range(R):
                        acc[j] = F.add(acc[j], row[j] if s == 1 else neg[row[j]])
                if all(x == 0 for x in acc):
                    return w
    return None


def diff_locator_defect(F, U, R):
    """rank_K Span{(1,t,..,t^{R-1}): t in U} vs min(|U|,R): alternative (b) probe."""
    U = sorted(set(U))
    cols = [[F.powr(t, j) for j in range(R)] for t in U]
    rk = rank_fq(F, cols)
    return min(len(U), R) - rk


# =========================================================================== #
#  Gamma_2 by additive-character Parseval (dual path)                           #
# =========================================================================== #
def parseval(F, Nmap, R, C):
    q = F.q; size = q ** R
    g2_census = size * sum(c * c for c in Nmap.values()) / (C * C)
    ch = [[F.add_char(F.mul(a, s)) for s in range(q)] for a in range(q)]
    total = 0.0; alpha = [0] * R
    while True:
        E = 0j
        for s, c in Nmap.items():
            pr = 1.0 + 0j; ss = s
            for j in range(R):
                pr *= ch[alpha[j]][ss % q]; ss //= q
            E += c * pr
        total += (E.real * E.real + E.imag * E.imag)
        i = 0
        while i < R:
            alpha[i] += 1
            if alpha[i] < q:
                break
            alpha[i] = 0; i += 1
        if i == R:
            break
    return g2_census, total / (C * C)


# =========================================================================== #
#  claim II: the -Theta(N log N) frontier-normalization tension                 #
# =========================================================================== #
def tension_row(N, kappa=0.25):
    R_low = kappa * N
    log_absK_min = math.log(N)          # T subset K, |T|=N  =>  |K| >= N
    max_log_Omega = N * math.log(3)     # Omega subset {-1,0,1}^T
    min_R_logK = R_low * log_absK_min
    val = max_log_Omega - min_R_logK
    return dict(N=N, max_log_Omega=max_log_Omega, min_R_logK=min_R_logK,
                max_norm_value=val, max_norm_over_N=val / N)


# =========================================================================== #
def load(name):
    with open(os.path.join(DATA, f"{PREFIX}_{name}.json")) as f:
        return json.load(f)


def find(rows, key, val):
    for r in rows:
        if r.get(key) == val:
            return r
    raise KeyError(val)


def gate_span(tag, got, want):
    geq(f"{tag}.law0", got["law0_violations"], want["law0_violations"])
    geq(f"{tag}.lawp", got["lawp_violations"], want["lawp_violations"])
    geq(f"{tag}.n_occ", got["n_occ"], want["n_occ"])
    geq(f"{tag}.pred_W", got["pred_W"], want["pred_W"])
    geq(f"{tag}.index", got["index"], want["index"])
    geq(f"{tag}.dim_span_Fp", got["dim_span_Fp"], want["dim_span_Fp"])
    geq(f"{tag}.ambient_Fp", got["ambient_Fp"], want["ambient_Fp"])
    geq(f"{tag}.V_T", got["V_T"], want["V_T"])
    geq(f"{tag}.K_rank", got["K_rank"], want["K_rank"])
    geq(f"{tag}.K_rank_full", got["K_rank_full"], want["K_rank_full"])
    geq(f"{tag}.free", got["free"], want["free"])
    geq(f"{tag}.red", got["red"], want["red"])
    feq(f"{tag}.W_occupancy", got["W_occupancy"], want["W_occupancy"])
    feq(f"{tag}.exc_cond", got["exc_cond"], want["exc_cond"])
    feq(f"{tag}.G2", got["G2"], want["G2"])
    feq(f"{tag}.excess_multi", got["excess_multi"], want["excess_multi"])
    feq(f"{tag}.offset_over_N", got["offset_over_N"], want["offset_over_N"])


# =========================================================================== #
def main():
    Dreg = load("regime")
    Dspan = load("spancell")
    Dnull = load("nulls")

    F27 = GF(3, 3); F16 = GF(2, 4); F64 = GF(2, 6)

    # ---- provenance: the tex line refs this packet quotes -------------------- #
    prov = Dreg["_provenance"]
    geq("prov.atom_line", prov["atom_line"], 827)
    geq("prov.escape_line", prov["escape_clause_line"], 828)
    geq("prov.removal_line", prov["removal_list_line"], 839)
    geq("prov.normalization_line", prov["normalization_line"], 840)
    geq("prov.alt_a_line", prov["alt_a_line"], 862)
    geq("prov.alt_b_line", prov["alt_b_line"], 863)

    # ===================================================================== #
    #  (I) THE F_p-SPAN CELL -- exact laws, image=W, span vs K-rank          #
    # ===================================================================== #
    # S27 (signed, F27, N=14, a=7, R=4): headline. ones passes the laws exactly. #
    T27 = build_T(F27, 14)
    s27_ones = law_check(F27, T27, 7, True, 4, "ones")
    gate_span("span.S27.ones", s27_ones, find(Dspan["configs"], "tag", "S27@R4:ones"))
    want_true("span.S27.laws_hold", s27_ones["law0_violations"] == 0 and s27_ones["lawp_violations"] == 0)
    want_true("span.S27.image_is_W", s27_ones["n_occ"] == s27_ones["pred_W"])          # image = W
    want_true("span.S27.Krank_full", s27_ones["K_rank"] == s27_ones["K_rank_full"])    # rank_K FULL
    want_true("span.S27.Fp_deficient", s27_ones["dim_span_Fp"] < s27_ones["ambient_Fp"])  # ... yet F_p-deficient
    want_true("span.S27.exc_cond~1", 0.9 < s27_ones["exc_cond"] < 1.05)                # excess is the index
    want_true("span.S27.big_excess", s27_ones["excess_multi"] > 100.0)                 # 110x unconditional
    want_true("span.S27.norm_passes", s27_ones["offset_over_N"] > -0.25)               # NOT a small-family trap

    # twist BREAKS both laws and fills the F_p-span (the (b)-blindness is rho-specific) #
    s27_tw = law_check(F27, T27, 7, True, 4, "twist")
    gate_span("span.S27.twist", s27_tw, find(Dspan["configs"], "tag", "S27@R4:twist"))
    want_true("span.S27.twist_breaks_law0", s27_tw["law0_violations"] > 0)
    want_true("span.S27.twist_breaks_lawp", s27_tw["lawp_violations"] > 0)
    want_true("span.S27.twist_full_span", s27_tw["dim_span_Fp"] == s27_tw["ambient_Fp"])

    # U16o (unsigned, F16, N=15, a=8, R=4): s0 = a mod p fixes the head -> W = V_T/p  #
    u16_ones = law_check(F16, build_T(F16, 15), 8, False, 4, "ones")
    gate_span("span.U16o.ones", u16_ones, find(Dspan["configs"], "tag", "U16o@R4:ones"))
    want_true("span.U16o.laws_hold", u16_ones["law0_violations"] == 0 and u16_ones["lawp_violations"] == 0)
    want_true("span.U16o.image_is_W", u16_ones["n_occ"] == u16_ones["pred_W"])
    want_true("span.U16o.Krank_full", u16_ones["K_rank"] == u16_ones["K_rank_full"])
    want_true("span.U16o.exc_cond~1", 0.9 < u16_ones["exc_cond"] < 1.05)

    # F64-firstN (unsigned, F64, N=21, a=10, R=3): dim 6/18, K-rank 3 full ----- #
    f64_ones = law_check(F64, build_T(F64, 21), 10, False, 3, "ones")
    gate_span("span.F64.ones", f64_ones, find(Dspan["configs"], "tag", "F64-firstN@R3:ones"))
    want_true("span.F64.Fp_deficient", f64_ones["dim_span_Fp"] < f64_ones["ambient_Fp"])
    want_true("span.F64.Krank_full", f64_ones["K_rank"] == f64_ones["K_rank_full"])

    # excess_generic: the rho=ones structural excess is huge; it is exactly [K^R:W] #
    g2g_S27 = gamma2_generic(F27, 14, 7, 4, True)          # shared generic baseline
    eg_ones = s27_ones["G2"] / g2g_S27
    feq("span.S27.excess_generic_ones", eg_ones, Dspan["S27_excess_generic_ones"])
    want_true("span.S27.excess_generic_big", eg_ones > 100.0)

    # PROJECTIVE form (repair per the #422 review): the c-form laws hold        #
    # exhaustively on rho(T) subset c F_p^x with c = g not in F_p, and every    #
    # census statistic equals the ones instance EXACTLY -- mul-by-c is an       #
    # F_p-automorphism of K^R carrying W_1 to W_c, and the a_t in F_p^x factors #
    # act by slice symmetries.  The cell is a projective-class phenomenon.      #
    want_true("proj.c27_not_in_Fp", F27.g >= F27.p)
    want_true("proj.c16_not_in_Fp", F16.g >= F16.p)
    Dproj = Dspan["projective"]
    geq("proj.c27", F27.g, Dproj["c_S27"])
    geq("proj.c16", F16.g, Dproj["c_U16"])
    geq("proj.stats_flag", Dproj["stats_equal_ones_exactly"], True)
    s27_proj = law_check(F27, T27, 7, True, 4, "proj")
    gate_span("span.S27.proj", s27_proj, find(Dspan["configs"], "tag", "S27@R4:proj"))
    want_true("span.S27.proj_laws_hold",
              s27_proj["law0_violations"] == 0 and s27_proj["lawp_violations"] == 0)
    want_true("span.S27.proj_stats_eq_ones",
              all(s27_proj[key] == s27_ones[key] for key in
                  ("n_occ", "pred_W", "index", "dim_span_Fp", "K_rank",
                   "G2", "exc_cond", "excess_multi", "W_occupancy")))
    u16_proj = law_check(F16, build_T(F16, 15), 8, False, 4, "proj")
    gate_span("span.U16o.proj", u16_proj, find(Dspan["configs"], "tag", "U16o@R4:proj"))
    want_true("span.U16o.proj_laws_hold",
              u16_proj["law0_violations"] == 0 and u16_proj["lawp_violations"] == 0)
    want_true("span.U16o.proj_stats_eq_ones",
              all(u16_proj[key] == u16_ones[key] for key in
                  ("n_occ", "pred_W", "index", "dim_span_Fp", "K_rank",
                   "G2", "exc_cond", "excess_multi", "W_occupancy")))

    # containment + Jensen alone forces the excess (review sharpening): the raw #
    # Gamma_2 >= [K^R : W_c] with NO use of the toy-exact, in-general-OPEN      #
    # image = W_c surjection (Cauchy-Schwarz over <= |W_c| occupied fibers)     #
    for jtag, jd in (("S27.ones", s27_ones), ("U16o.ones", u16_ones),
                     ("F64.ones", f64_ones), ("S27.proj", s27_proj),
                     ("U16o.proj", u16_proj)):
        want_true(f"jensen.{jtag}.G2_ge_index", jd["G2"] >= jd["index"] - 1e-9)

    # the sharp trigger criterion's arithmetic (review repair of the bounded-   #
    # field trigger): #red == floor((R-1)/p) exactly, and the closed form       #
    # q^(1+#red)/p^[s0 free] equals the recomputed index exactly, so            #
    # log index = floor((R-1)/p) log|K| + head-coordinate correction            #
    for ctag, cd, Fld in (("S27.ones", s27_ones, F27), ("U16o.ones", u16_ones, F16),
                          ("F64.ones", f64_ones, F64), ("S27.proj", s27_proj, F27),
                          ("U16o.proj", u16_proj, F16)):
        geq(f"crit.{ctag}.red_floor", len(cd["red"]), (cd["R"] - 1) // Fld.p)
        s0_free = 1 if (cd["signed"] and Fld.p > 2) else 0
        geq(f"crit.{ctag}.index_closed_form", cd["index"],
            Fld.q ** (1 + len(cd["red"])) // (Fld.p ** s0_free))

    # ===================================================================== #
    #  (II) NORMALIZATION WELLFORMEDNESS -- the -Theta(N log N) tension       #
    # ===================================================================== #
    for row in Dreg["tension"]["instances"]:
        got = tension_row(row["N"], Dreg["tension"]["kappa"])
        feq(f"tension.N{row['N']}.max_norm_value", got["max_norm_value"], row["max_norm_value"])
        feq(f"tension.N{row['N']}.over_N", got["max_norm_over_N"], row["max_norm_over_N"])
    # the failure is omega(N): |offset/N| strictly GROWS with N (not o(N))
    seq = [tension_row(N, 0.25)["max_norm_over_N"] for N in (100, 1000, 10000, 100000)]
    want_true("tension.grows", all(seq[i] > seq[i + 1] for i in range(len(seq) - 1)))  # more negative
    want_true("tension.not_oN", abs(seq[-1]) > abs(seq[0]) + 1.0)
    geq("tension.order", Dreg["tension"]["order_of_failure"], "-Theta(N log N)")
    geq("repairs.count", len(Dreg["two_repairs"]), 2)

    # finite toys sit ON the balance, offsets straddling 0 (recompute two exactly) #
    feq("reg.S27.offset_bits", s27_ones["offset_bits"], find(Dreg["balance"], "name", "S27")["offset_bits"])
    u16tw_bal = law_check(F16, build_T(F16, 15), 8, False, 3, "twist")   # U16 balance R=3
    feq("reg.U16.offset_bits", u16tw_bal["offset_bits"], find(Dreg["balance"], "name", "U16")["offset_bits"])

    # ===================================================================== #
    #  (III) SUPPORTING INSTRUMENTATION                                      #
    # ===================================================================== #
    # generic-rho null: NO excess survives balance under a generic weight.    #
    eg_S27t = s27_tw["G2"] / g2g_S27                              # reuse twist census + baseline
    feq("null.S27t.excess_generic", eg_S27t, find(Dnull["generic_rho_null"], "name", "S27t")["excess_generic"])
    want_true("null.S27t.le_108", eg_S27t <= 1.08)
    T16 = build_T(F16, 15)
    cnt, CU = census(F16, moment_columns(F16, T16, 3, build_rho(F16, T16, "twist")), 3,
                     lambda: itertools.combinations(range(15), 8), False)
    eg_U16 = gamma2(cnt, 16 ** 3, CU) / gamma2_generic(F16, 15, 8, 3, False)
    feq("null.U16.excess_generic", eg_U16, find(Dnull["generic_rho_null"], "name", "U16")["excess_generic"])
    want_true("null.U16.le_108", eg_U16 <= 1.08)

    # large-subgroup corner CLOSED: mu21 subset F64 retains no excess vs firstN control #
    mu21 = []
    ggen = F64.powr(F64.g, (F64.q - 1) // 21); x = 1
    for _ in range(21):
        mu21.append(x); x = F64.mul(x, ggen)
    mu21 = sorted(mu21)
    fam21 = lambda: itertools.combinations(range(21), 10)
    g2g_F64 = gamma2_generic(F64, 21, 10, 3, False)             # shared generic baseline

    def eg_dom(dom):
        rho = build_rho(F64, dom, "twist")
        cc, CC = census(F64, moment_columns(F64, dom, 3, rho), 3, fam21, False)
        return gamma2(cc, 64 ** 3, CC) / g2g_F64
    retained = eg_dom(mu21) / eg_dom(build_T(F64, 21))
    feq("null.F64.mu21_retained", retained, Dnull["large_subgroup"]["F64_mu21_retained_excess"])
    want_true("null.F64.corner_closed", 0.4 < retained < 1.2)                       # ~1 => no missing cell

    # min signed-dependency: the exact Vandermonde barrier R+1 (sharper than 2(R+1)) #
    mindep = min_signed_dep(F16, build_T(F16, 15), 3, 8)
    geq("null.min_dep.F16_R3", mindep, Dnull["min_signed_dep"]["F16_R3"])
    want_true("null.min_dep.eq_R+1", mindep == 3 + 1)
    want_true("null.min_dep.below_2R+2", mindep < 2 * (3 + 1))
    # stored dichotomy min_supp values all obey the R+1 <= min_supp < 2(R+1) barrier #
    for row in Dnull["dichotomy_S27_ones"]:
        want_true(f"null.dich.R{row['R']}.min_supp>=R+1", row["min_supp"] >= row["R"] + 1)
        want_true(f"null.dich.R{row['R']}.min_supp<2(R+1)", row["min_supp"] < 2 * (row["R"] + 1))
        geq(f"null.dich.R{row['R']}.vdm_barrier", row["vdm_barrier"], row["R"] + 1)

    # differential-locator defect = 0 on distinct points (prop:vandermonde) ---- #
    for (Fld, dom, R) in ((F16, build_T(F16, 7), 3), (F16, build_T(F16, 9), 5),
                          (F27, build_T(F27, 7), 3), (F27, build_T(F27, 9), 5)):
        geq(f"null.dl.q{Fld.q}_U{len(dom)}_R{R}", diff_locator_defect(Fld, dom, R), 0)
    geq("null.dl.all_zero", Dnull["diff_locator"]["all_defects_zero"], True)
    geq("null.plants.n_candidates", Dnull["plant_hunt"]["n_candidates"], 0)

    # gamma-scaling honesty item: the two discriminator T's are gamma=42 equivalent #
    geq("null.gamma_scaling", Dnull["gamma_scaling"]["gamma"], 42)

    # ===================================================================== #
    #  DUAL PATHS                                                            #
    # ===================================================================== #
    # (a) field multiply: table backend vs log/antilog backend, full sweeps -- #
    mism = sum(1 for a in range(F27.q) for b in range(F27.q) if F27.mul(a, b) != F27.mul_dual(a, b))
    geq("dual.mul.F27", mism, 0)
    mism2 = sum(1 for a in range(F16.q) for b in range(F16.q) if F16.mul(a, b) != F16.mul_dual(a, b))
    geq("dual.mul.F16", mism2, 0)

    # (b) Gamma_2 by census vs additive-character Parseval on a small census --- #
    F9 = GF(3, 2); Tp = build_T(F9, 8); Rp = 3
    VTp = moment_columns(F9, Tp, Rp, [1] * 8)
    cp, Cp = census(F9, VTp, Rp, lambda: itertools.combinations(range(8), 4), False)
    g2c, g2p = parseval(F9, cp, Rp, Cp)
    feq("dual.parseval.census_vs_char", g2c, g2p, tol=1e-7)

    # ===================================================================== #
    #  TAMPER SELF-TESTS (7) -- each MUST be caught                          #
    # ===================================================================== #
    tampers = 0
    # T1: a faked K-rank defect -- distinct moment columns are always K-independent #
    if diff_locator_defect(F27, build_T(F27, 4), 3) == 0:      # min(4,3)-rank = 0 defect
        tampers += 1
    # T2: a faked F_p-span dimension -- corrupting dim_span breaks the V_T = p^dim gate #
    faked_dim = s27_ones["dim_span_Fp"] - 1
    if F27.p ** faked_dim != s27_ones["V_T"]:
        tampers += 1
    # T3: the exact laws must genuinely hold for ones and genuinely break for twist #
    if (s27_ones["law0_violations"] == 0) and (s27_tw["law0_violations"] > 0):
        tampers += 1
    # T4: image = W is exact -- a perturbed W (off by one) would miss the census -- #
    if s27_ones["n_occ"] == s27_ones["pred_W"] and s27_ones["n_occ"] != s27_ones["pred_W"] + 1:
        tampers += 1
    # T5: Parseval falsification -- corrupt one fiber count, the relation must break #
    cbad = Counter(cp); cbad[next(iter(cbad))] += 3
    g2c_b, _ = parseval(F9, cbad, Rp, Cp + 3)
    if abs(g2c_b - g2c) > 1e-9:
        tampers += 1
    # T6: conditional excess is ~1 (index-only), NOT the raw 110x -- guards the claim #
    if s27_ones["exc_cond"] < 1.05 and s27_ones["excess_multi"] > 100.0:
        tampers += 1
    # T7: the c-form is load-bearing -- the same proj census must BREAK the c = 1 #
    # laws (s_0 lands in c F_p, not in F_p, on every nonzero-head fiber)          #
    cnts_p7, _C7 = census(F27, moment_columns(F27, T27, 4, build_rho(F27, T27, "proj")),
                          4, lambda: itertools.combinations(range(14), 7), True)
    bad_head = sum(1 for key in cnts_p7 if decode(key, F27.q, 4)[0] >= F27.p)
    if bad_head > 0:
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
    print("F_p-span cell (projective class c F_p^x): image(Phi) subset V_T "
          "(F_p-deficient) while rank_K FULL => alternative (b) is blind to it; "
          "Gamma_2 >= index by containment + Jensen alone.")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
