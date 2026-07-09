#!/usr/bin/env python3
"""
TWIST SPAN-CODIMENSION CENSUS for the F_p-span cell of the primitive entropic
inverse atom prob:entropy-inverse-q (experimental/grande_finale.tex L827-870).

This is a follow-on measurement to
experimental/notes/thresholds/cap25_v13_entropy_inverse_fp_span_cell.md (PR
#422, not yet merged at HEAD of this branch), which identified the F_p-span
cell: for a weight rho on a projective class rho(T) subset c F_p^x, the span
V_T = span_{F_p}{rho(t) v_t : t in T} (v_t = the moment column
(1,t,...,t^{R-1})) is F_p-deficient inside the ambient K^R, while for a
generic twist it fills the ambient exactly. #422 §2.4 posed three options to
resolve the resulting ledger gap; option 1 is a "rho-genericity hypothesis"
excluding the deficient weights. #422 §6 (OPEN) asked exactly the question
this script answers: how fast does the deficiency (codim_{F_p} V_T) die as
rho departs from a single projective class, i.e. how much genericity would
option 1 actually need to demand?

Four deterministic-rho families, swept over a field/config grid
{F27(3,3), F16(2,4), F64(2,6), F49(7,2), F125(5,3)} x {R in 3,4,5,6} x
{N in 12..16} (T = firstN throughout; NO combinatorial slice is enumerated
for the grid measurements -- dim_Fp(V_T) is the F_p-rank of N raw weighted
columns, cheap linear algebra, independent of any slice/weight-count `a`):

  F1  m-class mixtures: rho(t) in a round-robin, balanced union of m distinct
      projective classes c_1 F_p^x,...,c_m F_p^x (m = 1..6; ascending coset
      representatives of F_p^x in K^x). Tests the naive law
      dim(m) = min(ambient, m*dim_1).
  F2  epsilon-contamination: rho = the c=1 class except the first j positions
      of T (nested in j, deterministic) hold a generic K^x value. Tests
      whether a SINGLE contaminated column (j=1) already fills the ambient.
  F3  subfield-valued rho: rho(t) generic (seeded-uniform) in a proper
      subfield's unit group F_{p^d}^x < K^x (F16 k=4: d in {1,2}; F64 k=6:
      d in {1,2,3}). Also verifies EXHAUSTIVELY (one enumerable config, F16
      d=2) the natural per-subfield generalization of #422's c=1 law:
      s_0 in F_{p^d} and s_{p^d j} = Frob^d(s_j) = s_j^{p^d} for p^d*j < R.
  F4  Hamming perturbation: rho = the c=1 class except the first h positions
      (nested in h) are multiplied by a fixed non-F_p unit (the field
      generator g). The multiplicative-side analog of F2's question.

At three configs (2-3 as scoped), the combinatorial slice IS exhaustively
enumerated to tie dim_Fp/codim to the actual collision excess
(excess_generic = Gamma_2(moment curve) / Gamma_2(generic map of the same
shape), #422's baseline): F27 R=4 N=12 a=7 signed (F2, j=0,1,2), F16 R=3
N=12 a=6 unsigned (F2, j=0,1), F49 R=2 N=10 a=4 signed (F1, m=1,2). A fourth
exhaustive config (F16 R=5 N=8 a=4 unsigned, d=2) is dedicated solely to the
F3 Frobenius^d law verification, not the excess tie.

This script COPIES (per repo convention: standalone stdlib-only scripts, no
cross-imports) the finite-field GF class, fp_span_dim, moment_columns,
gamma2, generic_cols, and decode helpers verbatim from
experimental/scripts/verify_entropy_inverse_fp_span_cell.py
(PR #422; that script's own header credits these as recomputing from scratch
the smallest-irreducible-modulus field arithmetic and the F_p-span Gaussian
elimination), and ADAPTS its census/gamma2_generic (same algorithm,
refactored signatures).  New to this packet: the four rho families, the
class enumerator, and the Frobenius^d law check.

This is a MEASUREMENT-ONLY packet. It claims no theorem: every law tested
against the grid is reported with its exact match/violation count, not
asserted. In particular the naive m-class law dim(m)=min(ambient,m*dim_1) is
MEASURED FALSE (concrete counterexamples gated below); the epsilon/Hamming
"does j=1 (or h=1) fill?" question is MEASURED NO in the overwhelming
majority of swept configs (fill_j / fill_h distributions gated below); the
subfield Frobenius^d law is MEASURED TRUE with zero violations on the one
config checked exhaustively (PROVED-AT-TOYS in #422's sense, not a general
theorem).

Zero-arg, stdlib-only. Prints RESULT: PASS (N/N checks) and exits 0.

Environment knobs (both optional; defaults reproduce the committed run):
  FP_CODIM_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0
                        disables). Applying the cap is NEVER fatal: if the
                        platform refuses it, the script proceeds uncapped
                        and prints a notice.
  FP_CODIM_DATA_DIR    directory holding the committed data JSON (default:
                        ../data relative to this script, i.e. the in-tree
                        experimental/data/ layout).

Note: experimental/notes/thresholds/cap25_v13_entropy_inverse_fp_span_codim_census.md
Data: experimental/data/cap25_v13_entropy_inverse_fp_span_codim_census.json

Claim labels mirror the note:
  MEASURED    every dim_Fp / codim / excess_generic number recomputed and
              gated here.
  PROVED-AT-TOYS  the F3 Frobenius^d law only -- an exhaustive
              zero-violation recompute on the dedicated F16 d=2 config, the
              same epistemic status PR #422 uses for its own c-form laws,
              not a general theorem.  (The F2 j=0 exact-equality is internal
              tamper machinery, not a note-level claim.)
  CONVENTION  the grid, the round-robin class assignment, the deterministic
              contamination/perturbation positions, the excess_generic
              baseline (inherited from #421/#422).
"""
import os
import json
import math
import random
import resource
import itertools
from collections import Counter


def _apply_as_cap():
    """Best-effort address-space guard: honor FP_CODIM_AS_CAP_GB (default
    2 GB, 0 disables) but never fail on platforms that refuse the cap."""
    try:
        gb = float(os.environ.get("FP_CODIM_AS_CAP_GB", "2"))
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
DATA = os.environ.get("FP_CODIM_DATA_DIR") or os.path.normpath(
    os.path.join(HERE, "..", "data"))
PREFIX = "cap25_v13_entropy_inverse_fp_span_codim_census"

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
#  -- copied verbatim from verify_entropy_inverse_fp_span_cell.py (PR #422)     #
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


# =========================================================================== #
#  datum builders + F_p-span dimension -- copied verbatim from #422             #
# =========================================================================== #
def build_T(F, N):
    return list(range(1, F.q))[:N]


def moment_columns(F, T, R, rho):
    VT = []
    for i, t in enumerate(T):
        row = []; tj = 1
        for j in range(R):
            row.append(F.mul(rho[i], tj)); tj = F.mul(tj, t)
        VT.append(row)
    return VT


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


# =========================================================================== #
#  NEW to this packet: the four rho families                                   #
# =========================================================================== #
def classes_of(F, m):
    """The first m distinct projective classes c_i F_p^x < K^x, as ascending
    coset representatives (deterministic, no seed): for p=2, F_p^x={1} so
    every nonzero element is its own class."""
    p, q = F.p, F.q
    seen = [False] * q
    reps = []
    for x in range(1, q):
        if seen[x]:
            continue
        coset = sorted(F.mul(x, u) for u in range(1, p))
        for y in coset:
            seen[y] = True
        reps.append(coset[0])
        if len(reps) == m:
            break
    return reps


def rho_m_class(F, T, classes):
    """(F1) Round-robin balanced assignment over m distinct classes. a_t == 1
    throughout: multiplying a single column by a nonzero F_p scalar never
    changes the F_p-span of the whole set, so this is WLOG for dim_Fp(V_T)
    (the class-invariance #422 §2.1 already established for a single class
    extends trivially here)."""
    m = len(classes)
    return [classes[i % m] for i in range(len(T))]


def rho_epsilon_contam(F, T, j, base_c=1, seed=777):
    """(F2) The c=1 projective class except the first j positions of T
    (nested in j: the same RNG draw is reused for position i regardless of
    how large j grows) hold a generic K^x value."""
    rnd = random.Random(seed)
    rho = [base_c] * len(T)
    for i in range(len(T)):
        val = 1 + rnd.randrange(F.q - 1)
        if i < j:
            rho[i] = val
    return rho


def rho_subfield(F, T, d, seed):
    """(F3) rho(t) generic (seeded-uniform) in the proper subfield unit group
    F_{p^d}^x < K^x (d must divide k)."""
    q = F.q
    order = F.p ** d - 1
    h = F.powr(F.g, (q - 1) // order)
    units = []
    x = 1
    for _ in range(order):
        units.append(x)
        x = F.mul(x, h)
    rnd = random.Random(seed)
    return [units[rnd.randrange(order)] for _ in T]


def rho_hamming(F, T, h, base_c=1):
    """(F4) The c=1 projective class except the first h positions of T
    (nested in h) are multiplied by the non-F_p unit g (g is never in F_p
    for k >= 2, #422's own convention)."""
    unit = F.g
    rho = [base_c] * len(T)
    for i in range(min(h, len(T))):
        rho[i] = F.mul(base_c, unit)
    return rho


def measure(F, T, rho, R):
    """dim_Fp(V_T), ambient = R*k, codim = ambient - dim."""
    VT = moment_columns(F, T, R, rho)
    dim = fp_span_dim(F, VT, R)
    ambient = R * F.k
    return dim, ambient, ambient - dim


# =========================================================================== #
#  Exhaustive-slice helpers (spot-checks only): census, Gamma_2, excess_generic #
# =========================================================================== #
def decode(key, q, R):
    s = []
    for _ in range(R):
        s.append(key % q); key //= q
    return s


def census(F, VT, R, a, N, signed):
    """Fiber counts N(s) over the {-1,0,1}^T (signed) or {0,1}^T (unsigned)
    profile slice, exactly `a` active; s encoded little-endian base-q."""
    q = F.q; counts = Counter(); C = 0
    if signed:
        for combo in itertools.combinations(range(N), a):
            cols = [VT[i] for i in combo]
            for signs in itertools.product((0, 1), repeat=len(combo)):
                acc = [0] * R
                for idx, sbit in enumerate(signs):
                    row = cols[idx]
                    if sbit:
                        for j in range(R):
                            acc[j] = F.sub(acc[j], row[j])
                    else:
                        for j in range(R):
                            acc[j] = F.add(acc[j], row[j])
                key = 0
                for j in range(R):
                    key += acc[j] * q ** j
                counts[key] += 1; C += 1
    else:
        for combo in itertools.combinations(range(N), a):
            acc = [0] * R
            for i in combo:
                row = VT[i]
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
    """excess_generic's denominator: Gamma_2 of a generic random K^R linear
    map of the same shape (N columns, same slice), averaged over two seeds
    -- #422's baseline, extended to arbitrary (N,a,R,signed) here."""
    g2s = []
    for sd in seeds:
        counts, Cf = census(F, generic_cols(F, N, R, sd), R, a, N, signed)
        g2s.append(gamma2(counts, F.q ** R, Cf))
    return sum(g2s) / len(g2s)


def offset_over_N(N, a, R, q, signed):
    Omega = math.comb(N, a) * (2 ** a if signed else 1)
    return (math.log2(Omega) - R * math.log2(q)) / N


# =========================================================================== #
#  Grid definition                                                             #
# =========================================================================== #
FIELDS = [("F27", 3, 3), ("F16", 2, 4), ("F64", 2, 6), ("F49", 7, 2), ("F125", 5, 3)]
PRIMARY_R, PRIMARY_N = 4, 16
SWEEP_FIELD = "F27"
R_GRID = [3, 4, 5, 6]
N_GRID = [12, 13, 14, 15, 16]
JMAX = 5
SUBFIELD_FIELDS = {"F16": [1, 2], "F64": [1, 2, 3]}


def points_for(name):
    pts = [(PRIMARY_R, PRIMARY_N)]
    if name == SWEEP_FIELD:
        pts += [(R, PRIMARY_N) for R in R_GRID if R != PRIMARY_R]
        pts += [(PRIMARY_R, N) for N in N_GRID if N != PRIMARY_N]
    return pts


def load(name):
    with open(os.path.join(DATA, f"{PREFIX}.json")) as f:
        d = json.load(f)
    return d[name]


def find(rows, val):
    for r in rows:
        if r.get("tag") == val:
            return r
    raise KeyError(val)


def gate_dim_row(tag, got, want):
    geq(f"{tag}.dim", got["dim"], want["dim"])
    geq(f"{tag}.ambient", got["ambient"], want["ambient"])
    geq(f"{tag}.codim", got["codim"], want["codim"])


# =========================================================================== #
def main():
    Wf1 = load("F1_m_class_mixture")
    Wf2 = load("F2_epsilon_contamination")
    Wf3 = load("F3_subfield_valued")
    Wf4 = load("F4_hamming_perturbation")
    Wspot = load("spot_checks_excess_tie")
    Wlaw = load("F3_frobenius_law_check")

    FS = {name: GF(p, k) for name, p, k in FIELDS}

    # ---- field self-tests: q=p^k, antilog bijective, g never in F_p (k>=2) - #
    for name, p, k in FIELDS:
        F = FS[name]
        geq(f"field.{name}.q", F.q, p ** k)
        want_true(f"field.{name}.antilog_bijective", len(set(F.antilog)) == F.q - 1)
        want_true(f"field.{name}.g_not_in_Fp", F.g >= p)
        # dual-path field multiply: table backend vs log/antilog backend, full sweep
        mism = sum(1 for a in range(F.q) for b in range(F.q) if F.mul(a, b) != F.mul_dual(a, b))
        geq(f"field.{name}.mul_dual_path", mism, 0)

    # ===================================================================== #
    #  (I) F1 -- m-class mixtures                                           #
    # ===================================================================== #
    f1_rows = []
    f1_fill = []
    f1_match = 0
    f1_total = 0
    for name, p, k in FIELDS:
        F = FS[name]
        for (R, N) in points_for(name):
            T = build_T(F, N)
            classes = classes_of(F, 6)
            geq(f"F1.{name}.R{R}.N{N}.nclasses", len(classes), 6)
            dims = {}
            for m in range(1, 7):
                rho = rho_m_class(F, T, classes[:m])
                dim, amb, codim = measure(F, T, rho, R)
                dims[m] = dim
                tag = f"F1|{name}|R{R}|N{N}|m{m}"
                got = dict(dim=dim, ambient=amb, codim=codim)
                gate_dim_row(tag, got, find(Wf1["rows"], tag))
                f1_rows.append(got)
            dim1 = dims[1]
            amb = R * k
            fillm = None
            for m in range(1, 7):
                if dims[m] == amb:
                    fillm = m; break
            ftag = f"F1fill|{name}|R{R}|N{N}"
            fwant = find(Wf1["fill_summary"], ftag)
            geq(f"{ftag}.dim1", dim1, fwant["dim1"])
            geq(f"{ftag}.fill_m", fillm, fwant["fill_m"])
            for m in range(1, 7):
                predicted = min(amb, m * dim1)
                f1_total += 1
                if dims[m] == predicted:
                    f1_match += 1
    geq("F1.naive_law.total", f1_total, Wf1["naive_law_test"]["total"])
    geq("F1.naive_law.matches", f1_match, Wf1["naive_law_test"]["matches"])
    geq("F1.naive_law.violations", f1_total - f1_match, Wf1["naive_law_test"]["violations"])
    # the naive law "dim(m)=min(ambient,m*dim_1)" is measured FALSE far more often
    # than true -- this is a finding, not a bug: gate the majority-violation fact
    want_true("F1.naive_law.majority_violation", (f1_total - f1_match) > f1_total // 2)

    # ===================================================================== #
    #  (II) F2 -- epsilon-contamination                                     #
    # ===================================================================== #
    f2_fill_js = []
    for name, p, k in FIELDS:
        F = FS[name]
        for (R, N) in points_for(name):
            T = build_T(F, N)
            dims = {}
            for j in range(0, JMAX + 1):
                rho = rho_epsilon_contam(F, T, j)
                dim, amb, codim = measure(F, T, rho, R)
                dims[j] = dim
                tag = f"F2|{name}|R{R}|N{N}|j{j}"
                got = dict(dim=dim, ambient=amb, codim=codim)
                gate_dim_row(tag, got, find(Wf2["rows"], tag))
                # T2 (internal tamper check, exact): j=0 must equal the pure single-class weight
                if j == 0:
                    want_true(f"{tag}.j0_is_pure_class",
                              rho_epsilon_contam(F, T, 0) == [1] * len(T))
            amb = R * k
            fillj = None
            for j in range(0, JMAX + 1):
                if dims[j] == amb:
                    fillj = j; break
            f2_fill_js.append(fillj)
            ftag = f"F2fill|{name}|R{R}|N{N}"
            fwant = find(Wf2["fill_summary"], ftag)
            geq(f"{ftag}.codim0", amb - dims[0], fwant["codim0"])
            geq(f"{ftag}.fill_j", fillj, fwant["fill_j"])
    # headline finding: j=1 essentially never fills the ambient by itself
    n_fill_at_1 = sum(1 for x in f2_fill_js if x == 1)
    geq("F2.fill_at_j1.count", n_fill_at_1,
        sum(1 for r in Wf2["fill_summary"] if r["fill_j"] == 1))
    want_true("F2.fill_at_j1.rare", n_fill_at_1 <= len(f2_fill_js) // 4)

    # ===================================================================== #
    #  (III) F4 -- Hamming perturbation                                     #
    # ===================================================================== #
    f4_fill_hs = []
    for name, p, k in FIELDS:
        F = FS[name]
        for (R, N) in points_for(name):
            T = build_T(F, N)
            dims = {}
            for h in range(0, 4):
                rho = rho_hamming(F, T, h)
                dim, amb, codim = measure(F, T, rho, R)
                dims[h] = dim
                tag = f"F4|{name}|R{R}|N{N}|h{h}"
                got = dict(dim=dim, ambient=amb, codim=codim)
                gate_dim_row(tag, got, find(Wf4["rows"], tag))
                if h == 0:
                    want_true(f"{tag}.h0_is_pure_class",
                              rho_hamming(F, T, 0) == [1] * len(T))
            amb = R * k
            fillh = None
            for h in range(0, 4):
                if dims[h] == amb:
                    fillh = h; break
            f4_fill_hs.append(fillh)
            ftag = f"F4fill|{name}|R{R}|N{N}"
            fwant = find(Wf4["fill_summary"], ftag)
            geq(f"{ftag}.codim0", amb - dims[0], fwant["codim0"])
            geq(f"{ftag}.fill_h", fillh, fwant["fill_h"])
    n_fill_at_1_h = sum(1 for x in f4_fill_hs if x == 1)
    want_true("F4.fill_at_h1.rare", n_fill_at_1_h <= len(f4_fill_hs) // 4)

    # ===================================================================== #
    #  (IV) F3 -- subfield-valued rho (dim ladder)                          #
    # ===================================================================== #
    for name, ds in SUBFIELD_FIELDS.items():
        p, k = dict((n, (pp, kk)) for n, pp, kk in FIELDS)[name]
        F = FS[name]
        for R in R_GRID:
            T = build_T(F, PRIMARY_N)
            dims = {}
            for d in ds:
                rho = rho_subfield(F, T, d, seed=555 + d)
                dim, amb, codim = measure(F, T, rho, R)
                dims[d] = dim
                tag = f"F3|{name}|R{R}|N{PRIMARY_N}|d{d}"
                got = dict(dim=dim, ambient=amb, codim=codim)
                gate_dim_row(tag, got, find(Wf3["rows"], tag))
            amb = R * k
            filld = None
            for d in ds:
                if dims[d] == amb:
                    filld = d; break
            ftag = f"F3fill|{name}|R{R}"
            fwant = find(Wf3["fill_summary"], ftag)
            geq(f"{ftag}.fill_d", filld, fwant["fill_d"])
            # the ladder is non-decreasing in d (bigger subfield => more generic)
            want_true(f"{ftag}.ladder_nondecreasing",
                      all(dims[ds[i]] <= dims[ds[i + 1]] for i in range(len(ds) - 1)))

    # ===================================================================== #
    #  (V) Spot-checks -- exhaustive census, codim tied to excess_generic   #
    # ===================================================================== #
    spot_by_tag = {}

    FA = FS["F27"]; TA = build_T(FA, 12)
    g2g_A = gamma2_generic(FA, 12, 7, 4, True)
    oA = offset_over_N(12, 7, 4, 27, True)
    want_true("spotA.balance_guard", oA > -0.25)
    for j in (0, 1, 2):
        rho = rho_epsilon_contam(FA, TA, j)
        dim, amb, codim = measure(FA, TA, rho, 4)
        VT = moment_columns(FA, TA, 4, rho)
        counts, C = census(FA, VT, 4, 7, 12, True)
        G2 = gamma2(counts, FA.q ** 4, C)
        eg = G2 / g2g_A
        tag = f"spotA|F27|j{j}"
        want = find(Wspot["rows"], tag)
        gate_dim_row(tag, dict(dim=dim, ambient=amb, codim=codim), want)
        geq(f"{tag}.n_occ", len(counts), want["n_occ"])
        geq(f"{tag}.C", C, want["C"])
        feq(f"{tag}.G2", G2, want["G2"])
        feq(f"{tag}.excess_generic", eg, want["excess_generic"])
        feq(f"{tag}.offset_over_N", oA, want["offset_over_N"])
        spot_by_tag[tag] = dict(codim=codim, eg=eg)

    FB = FS["F16"]; TB = build_T(FB, 12)
    g2g_B = gamma2_generic(FB, 12, 6, 3, False)
    oB = offset_over_N(12, 6, 3, 16, False)
    for j in (0, 1):
        rho = rho_epsilon_contam(FB, TB, j)
        dim, amb, codim = measure(FB, TB, rho, 3)
        VT = moment_columns(FB, TB, 3, rho)
        counts, C = census(FB, VT, 3, 6, 12, False)
        G2 = gamma2(counts, FB.q ** 3, C)
        eg = G2 / g2g_B
        tag = f"spotB|F16|j{j}"
        want = find(Wspot["rows"], tag)
        gate_dim_row(tag, dict(dim=dim, ambient=amb, codim=codim), want)
        geq(f"{tag}.n_occ", len(counts), want["n_occ"])
        geq(f"{tag}.C", C, want["C"])
        feq(f"{tag}.G2", G2, want["G2"])
        feq(f"{tag}.excess_generic", eg, want["excess_generic"])
        feq(f"{tag}.offset_over_N", oB, want["offset_over_N"])

    FC = FS["F49"]; TC = build_T(FC, 10)
    g2g_C = gamma2_generic(FC, 10, 4, 2, True)
    oC = offset_over_N(10, 4, 2, 49, True)
    want_true("spotC.balance_guard", oC > -0.25)
    classesC = classes_of(FC, 2)
    for m in (1, 2):
        rho = rho_m_class(FC, TC, classesC[:m])
        dim, amb, codim = measure(FC, TC, rho, 2)
        VT = moment_columns(FC, TC, 2, rho)
        counts, C = census(FC, VT, 2, 4, 10, True)
        G2 = gamma2(counts, FC.q ** 2, C)
        eg = G2 / g2g_C
        tag = f"spotC|F49|m{m}"
        want = find(Wspot["rows"], tag)
        gate_dim_row(tag, dict(dim=dim, ambient=amb, codim=codim), want)
        geq(f"{tag}.n_occ", len(counts), want["n_occ"])
        geq(f"{tag}.C", C, want["C"])
        feq(f"{tag}.G2", G2, want["G2"])
        feq(f"{tag}.excess_generic", eg, want["excess_generic"])
        feq(f"{tag}.offset_over_N", oC, want["offset_over_N"])

    # codim and excess_generic move together at spot A (both strictly decreasing) #
    want_true("spotA.codim_monotone_decreasing",
              spot_by_tag["spotA|F27|j0"]["codim"] > spot_by_tag["spotA|F27|j1"]["codim"] >
              spot_by_tag["spotA|F27|j2"]["codim"])
    want_true("spotA.excess_monotone_decreasing",
              spot_by_tag["spotA|F27|j0"]["eg"] > spot_by_tag["spotA|F27|j1"]["eg"] >
              spot_by_tag["spotA|F27|j2"]["eg"])

    # ===================================================================== #
    #  (VI) F3 exhaustive Frobenius^d law -- one enumerable config          #
    # ===================================================================== #
    FD = FS["F16"]; TD = build_T(FD, 8)
    rhoD = rho_subfield(FD, TD, 2, seed=557)
    VTD = moment_columns(FD, TD, 5, rhoD)
    countsD, CD = census(FD, VTD, 5, 4, 8, False)
    head_viol = 0; frob_viol = 0; checked = 0
    step = FD.p ** 2
    for key in countsD:
        s = decode(key, FD.q, 5)
        if not FD.in_subfield(s[0], 2):
            head_viol += 1
        for jx in range(1, 5):
            if step * jx < 5:
                checked += 1
                if s[step * jx] != FD.powr(s[jx], step):
                    frob_viol += 1
    wrong_head_viol = sum(1 for key in countsD
                           if not FD.in_subfield(decode(key, FD.q, 5)[0], 1))
    dimD, ambD, codimD = measure(FD, TD, rhoD, 5)

    geq("F3law.n_occ", len(countsD), Wlaw["n_occ"])
    geq("F3law.C", CD, Wlaw["C"])
    geq("F3law.checked_pairs", checked, Wlaw["checked_pairs"])
    geq("F3law.head_violations", head_viol, Wlaw["head_violations"])
    geq("F3law.frob_violations", frob_viol, Wlaw["frob_violations"])
    geq("F3law.wrong_degree_head_violations", wrong_head_viol,
        Wlaw["wrong_degree_head_violations"])
    gate_dim_row("F3law", dict(dim=dimD, ambient=ambD, codim=codimD), Wlaw)
    want_true("F3law.zero_violations_exhaustive", head_viol == 0 and frob_viol == 0)
    want_true("F3law.checked_nonempty", checked > 0)
    # load-bearing: the SAME census must break the wrong-degree containment
    want_true("F3law.wrong_degree_breaks", wrong_head_viol > 0)

    # ===================================================================== #
    #  TAMPER SELF-TESTS (>=5) -- each MUST be caught                       #
    # ===================================================================== #
    tampers = 0

    # T1: a faked F_p-span dimension must be CAUGHT by the live gate -- feed #
    # a freshly recomputed dim through the same geq() the real rows use with #
    # a corrupted expectation, confirm FAILS grows, then retract the scratch #
    # entry (exercises the actual gating pipeline, not an arithmetic         #
    # tautology)                                                             #
    ref_row_t1 = find(Wf1["rows"], "F1|F27|R4|N16|m1")
    F27t1 = FS["F27"]; T27t1 = build_T(F27t1, 16)
    dim_t1, _amb_t1, _cod_t1 = measure(
        F27t1, T27t1, rho_m_class(F27t1, T27t1, classes_of(F27t1, 6)[:1]), 4)
    pre_fails_t1 = len(FAILS)
    geq("tamper.T1.scratch_corrupted_dim", dim_t1, ref_row_t1["dim"] - 1)
    if len(FAILS) == pre_fails_t1 + 1 and dim_t1 == ref_row_t1["dim"]:
        FAILS.pop()
        tampers += 1

    # T2: the j=0 control is EXACTLY the pure single-class weight, not just  #
    # dimension-equal -- an off-by-one contamination-start bug would corrupt #
    # position 0 and this exact list-equality check would catch it          #
    F27x = FS["F27"]; T27x = build_T(F27x, 16)
    if (rho_epsilon_contam(F27x, T27x, 0) == [1] * len(T27x)
            and rho_epsilon_contam(F27x, T27x, 1) != [1] * len(T27x)):
        tampers += 1

    # T3: a full-twist (fully generic) control must be codim 0 exactly --   #
    # validates this script's OWN copy of fp_span_dim/moment_columns        #
    # against #422's established fact that a generic twist fills the ambient. #
    # Uses N=21, R=2 (ambient = 2k <= 12 for every field here) so N_real     #
    # clears ambient with comfortable slack (build_T caps at the q-1 nonzero #
    # elements -- e.g. F16 yields N_real = 15): dim_Fp(V_T) <=               #
    # min(N_real, ambient) always, and at the grid's N=16,R=4 points that    #
    # structural bound alone already forces codim >= 8 for F64 (ambient=24)  #
    # and codim >= 1 for F16 (ambient=16 > N_real=15, structurally forced)   #
    # -- this control must isolate genuine genericity from that trap.        #
    full_twist_ok = True
    for name, p, k in FIELDS:
        F = FS[name]; T = build_T(F, 21)
        rnd = random.Random(9191)
        twist = [1 + rnd.randrange(F.q - 1) for _ in T]
        dim, amb, codim = measure(F, T, twist, 2)
        if codim != 0:
            full_twist_ok = False
    if full_twist_ok:
        tampers += 1

    # T4: a faked codim law -- the UNCAPPED "m*dim_1" (no min(ambient,...))  #
    # must fail to match measured dim at m>=2 wherever m*dim_1 > ambient;   #
    # catches a hypothetical bug that dropped the min() cap                 #
    uncapped_breaks = 0; uncapped_total = 0
    for name, p, k in FIELDS:
        F = FS[name]
        for (R, N) in points_for(name):
            T = build_T(F, N); classes = classes_of(F, 6)
            dim1, amb, _ = measure(F, T, rho_m_class(F, T, classes[:1]), R)
            for m in range(2, 7):
                if m * dim1 > amb:
                    uncapped_total += 1
                    dim_m, _, _ = measure(F, T, rho_m_class(F, T, classes[:m]), R)
                    if dim_m != m * dim1:
                        uncapped_breaks += 1
    if uncapped_total > 0 and uncapped_breaks == uncapped_total:
        tampers += 1

    # T5: the F3 law is load-bearing -- checking against the WRONG subfield  #
    # degree (d=1 instead of d=2) must break the head-containment law       #
    if wrong_head_viol > 0 and head_viol == 0:
        tampers += 1

    # T6: codim and excess_generic are CONSISTENT signals at spot A (both   #
    # strictly decreasing j=0->1->2) -- catches a hypothetical inconsistency #
    # between the dim-based and census-based measurement pipelines          #
    eg0 = spot_by_tag["spotA|F27|j0"]["eg"]; eg2 = spot_by_tag["spotA|F27|j2"]["eg"]
    cd0 = spot_by_tag["spotA|F27|j0"]["codim"]; cd2 = spot_by_tag["spotA|F27|j2"]["codim"]
    if (cd0 > cd2) and (eg0 > eg2) and (eg0 / max(eg2, 1e-9) > 2.0):
        tampers += 1

    geq("tamper.count>=5", tampers >= 5, True)
    geq("tamper.count", tampers, 6)

    # ===================================================================== #
    print("=" * 74)
    if FAILS:
        for fmsg in FAILS:
            print("FAIL:", fmsg)
        print(f"RESULT: FAIL ({len(FAILS)} of {CHECKS} checks failed)")
        raise SystemExit(1)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("Twist span-codimension census: dim_Fp(V_T) measured across four "
          "departure-from-projective-class families (m-class mixture, "
          "epsilon-contamination, subfield ladder, Hamming perturbation). "
          "Headline: fill is GRADUAL under contamination/Hamming perturbation "
          "(j=1 / h=1 essentially never fills the ambient); the naive m-class "
          "additivity law is measured FALSE in the majority of swept configs; "
          "the per-subfield Frobenius^d law holds exactly on the one config "
          "checked exhaustively.")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
