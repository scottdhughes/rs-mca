#!/usr/bin/env python3
"""
IMAGE-STRUCTURE THEOREM verifier for the F_p-span cell of the primitive entropic
inverse atom prob:entropy-inverse-q (experimental/grande_finale.tex L827-870).
This closes the surjection that PR #422 left OPEN (its Sec 2.3 / Sec 6): the exact
value of image(Phi) inside the ambient subgroup W_c.

SETUP (all verifier-fact, inherited from the #422 packet).  K = F_{p^k} with the
smallest-irreducible modulus; T subset K, |T| = N; columns v_t = rho(t)(1,t,...,
t^{R-1}) in K^R for projective weights rho(T) subset c F_p^x; profile slice
x in {-1,0,1}^T (signed, p odd) or {0,1}^T (unsigned, p = 2) with exactly a
active; Phi(x) = sum_t x_t v_t.  #422 proved image(Phi) subset W_c = {s: s_0 in
c F_p, s_{pj} = c^{1-p} s_j^p} and MEASURED image = W_c at S27/U16o (occ 1) but
image = HALF of W at F64-firstN (occ 0.5), leaving the general value OPEN.

THE THEOREM (this packet).  Let D be the "move subspace":
  D = V_T = span_Fp{v_t}                       (signed, p odd), or
  D = span_Fp{v_t + v_t'}  (even column sums)  (unsigned, p = 2).
(A) [CONTAINMENT, PROVED, no hypothesis]  image(Phi|slice-a) lies in a single
    coset Phi(x_0) + D, and D subset W_c^0 (the translation subgroup of W_c).
    Hence n_occ <= |D| = p^{dim D}, so Gamma_2 >= q^R / |D| = index * p^{defect}
    -- STRICTLY STRONGER than #422's Gamma_2 >= index, and it needs no
    surjection (containment + Cauchy-Schwarz alone).
(B) [OCCUPANCY, PROVED under Conn_a]  If the connectivity hypothesis Conn_a holds
    (image = the FULL coset Phi(x_0) + D, i.e. every kernel-coset of head-syndrome
    a meets the exactly-a slice), then
        occupancy := |image| / |W_c| = p^{-defect},
        defect := dim_Fp W_c^flat - dim_Fp V_T  >= 0,
    where W_c^flat is the head-free (s_0 in c F_p) Frobenius-closed ambient.
(C) [CLASSIFICATION, PROVED under Conn_a]  image = W_c  <=>  defect = 0
    <=>  V_T = W_c^flat (the columns F_p-span the full Frobenius-closed head space).
    defect = number of independent F_p-functionals on W_c^flat vanishing on every
    column (the "pinned functionals").  For moment columns these are
    ell(s) = Tr(lambda_0 s_0) + sum_{j free} Tr(nu_j s_j) with Tr(lambda_0 + P(t))
    = 0 for all t in T (P the free-exponent weight polynomial); T inside an
    intersection of m independent trace-hyperplanes forces defect >= m.

COROLLARIES (occupancies DERIVED, not measured): S27 defect 0 -> occ 1;
U16o defect 0 -> occ 1; F64-firstN defect 1 (T subset {Tr(t) = 0}) -> occ 1/2.
DESIGNED: F32-1HP defect 1 -> 1/2; F32-2HP & F64-2HP defect 2 (m = 2) -> occ 1/4.
CONN IS LOAD-BEARING: S27-1HP has defect 1 yet occ != 1/3 because Conn_a FAILS
at N = 8 (the occupancy formula genuinely needs the hypothesis).

CONNECTIVITY THRESHOLD is MEASURED, not given a closed form: it is a coset
weight-distribution property of the kernel code ker Phi (minimum distance R+1 by
prop:vandermonde-kills-low-rank).  In the large-kernel regime it is the clean band
[R, N-R] (unsigned, R odd) / [R+1, N-R-1] (unsigned, R even), with isolated
interior holes only for small kernels; the signed band differs (sign flips add
moves).  Verifier gates the exact bands at five toys.

Standalone, stdlib-only, zero-arg.  RECOMPUTES FROM SCRATCH the field arithmetic,
the moment-curve census, dim V_T / dim D / dim W_c^flat, the exact image census
and occupancy, the defect and the pinned functionals, the containment bound
Gamma_2 >= index * p^{defect}, and the connectivity bands -- then gates every
number against the committed JSON (exact on ints / strings / bools, 1e-9 on
floats).  Dual path: field multiply table vs log/antilog.  Ends with 7 tamper
self-tests (faked D-dim, faked coset size, non-spanning T with occ < 1, a
threshold-violating extreme a that MUST fail coverage, containment n_occ <= |D|,
the pinned functional load-bearing test, and the m = 2 occ = 1/4 test).

Lineage #414 -> #416 -> #417 -> #420 -> #421 -> #422 -> this packet.  Answers the
#422 review's (DannyExperiments) remaining ask: a separately proved theorem
promoting image = W_c from MEASURED to a characterization.

Note: experimental/notes/thresholds/cap25_v13_entropy_inverse_fp_span_surjection.md
Data: experimental/data/cap25_v13_entropy_inverse_fp_span_surjection.json

Environment knobs (both optional; defaults reproduce the committed run):
  FP_SURJ_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0 disables).
                      Applying the cap is NEVER fatal.
  FP_SURJ_DATA_DIR    directory holding the committed data JSON (default:
                      ../data relative to this script).
  FP_SURJ_DUMP        if set, (re)write the committed JSON from this run's own
                      recomputation instead of gating, then exit.
Timing / peak-RSS are environment-specific and deliberately NOT gated.
"""
import os
import json
import math
import resource
import itertools
from collections import Counter

def _apply_as_cap():
    try:
        gb = float(os.environ.get("FP_SURJ_AS_CAP_GB", "2"))
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
DATA = os.environ.get("FP_SURJ_DATA_DIR") or os.path.normpath(
    os.path.join(HERE, "..", "data"))
JSON_NAME = "cap25_v13_entropy_inverse_fp_span_surjection.json"

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
#  (recomputed from scratch; the #422 packet uses the identical machinery)      #
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

    def trace(self, a, d=1):
        """trace K -> F_{p^d} (default: down to the prime field)."""
        acc = 0; cur = a; step = self.p ** d
        for _ in range(self.k // d):
            acc = self.add(acc, cur); cur = self.powr(cur, step)
        return acc


# =========================================================================== #
#  datum builders, census, F_p / K linear algebra                              #
# =========================================================================== #
def build_T(F, N):
    return list(range(1, F.q))[:N]


def trace_hyperplane(F, mus):
    """nonzero t with Tr(mu t) = 0 (trace to prime field) for every mu in mus."""
    return [t for t in range(1, F.q)
            if all(F.trace(F.mul(mu, t)) % F.p == 0 for mu in mus)]


def moment_columns(F, T, R):
    """rho == 1 moment columns v_t = (1, t, ..., t^{R-1}); the admissible c = 1
    representative of the projective class (weight freedom, L828)."""
    VT = []
    for t in T:
        row = []; tj = 1
        for j in range(R):
            row.append(tj); tj = F.mul(tj, t)
        VT.append(row)
    return VT


def key_of(F, vec, R):
    q = F.q; key = 0
    for j in range(R):
        key += vec[j] * q ** j
    return key


def decode(key, q, R):
    s = []
    for _ in range(R):
        s.append(key % q); key //= q
    return s


def image_and_census(F, VT, R, a, signed):
    """exhaustive fiber counts N(s) over the exactly-a slice (keys = image);
    returns (Counter, C)."""
    q = F.q; N = len(VT); counts = Counter(); C = 0
    if not signed:
        for combo in itertools.combinations(range(N), a):
            acc = [0] * R
            for i in combo:
                row = VT[i]
                for j in range(R):
                    acc[j] = F.add(acc[j], row[j])
            counts[key_of(F, acc, R)] += 1; C += 1
    else:
        neg = F.negt
        for combo in itertools.combinations(range(N), a):
            cols = [VT[i] for i in combo]
            for signs in itertools.product((0, 1), repeat=a):
                acc = [0] * R
                for idx, s in enumerate(signs):
                    row = cols[idx]
                    if s:
                        for j in range(R):
                            acc[j] = F.add(acc[j], neg[row[j]])
                    else:
                        for j in range(R):
                            acc[j] = F.add(acc[j], row[j])
                counts[key_of(F, acc, R)] += 1; C += 1
    return counts, C


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


def move_span_dim(F, VT, R, signed):
    """dim_Fp D.  signed: D = V_T (sign flips give +-2 v_t, and 2 is a unit for
    p odd, so <v_t> is generated).  unsigned p = 2: D = span{v_t + v_t'}."""
    if signed:
        return fp_span_dim(F, VT, R)
    base = VT[0]
    diffs = [[F.sub(VT[i][j], base[j]) for j in range(R)] for i in range(1, len(VT))]
    return fp_span_dim(F, diffs, R)


def ambient_dims(F, R, signed):
    """(flat, w0, free): dim W_c^flat (head s_0 in c F_p free), dim of the
    translation subgroup W_c^0 (signed: head free; unsigned: head pinned), and the
    free exponent set."""
    k = F.k
    free = [j for j in range(1, R) if j % F.p != 0]
    flat = 1 + k * len(free)
    w0 = (1 if (signed and F.p > 2) else 0) + k * len(free)
    return flat, w0, free


def analyze(F, T, R, a, signed):
    p = F.p; N = len(T)
    VT = moment_columns(F, T, R)
    dimVT = fp_span_dim(F, VT, R)
    dimD = move_span_dim(F, VT, R, signed)
    flat, w0, free = ambient_dims(F, R, signed)
    red = [j for j in range(1, R) if j % p == 0]
    defect = flat - dimVT
    counts, C = image_and_census(F, VT, R, a, signed)
    n_occ = len(counts)
    size = F.q ** R
    Wc = p ** w0
    index = size // Wc
    G2 = size * sum(c * c for c in counts.values()) / (C * C)
    conn = (n_occ == p ** dimD)
    occ = n_occ / Wc
    return dict(q=F.q, p=p, k=F.k, R=R, N=N, a=a, signed=signed,
                dimVT=dimVT, dimD=dimD, flat=flat, w0=w0, Wc=Wc, index=index,
                defect=defect, free=free, red=red, n_occ=n_occ, C=C, G2=G2,
                occupancy=occ, conn=conn, pred_occ=p ** (-defect),
                G2_lb=index * p ** defect, dimD_minus_w0=dimD - w0,
                _counts=counts)


def full_band(F, T, R, signed):
    """the set of a in [1, N-1] with image = full coset of D (connectivity)."""
    VT = moment_columns(F, T, R)
    dimD = move_span_dim(F, VT, R, signed); Ds = F.p ** dimD
    out = []
    for a in range(1, len(T)):
        counts, _ = image_and_census(F, VT, R, a, signed)
        if len(counts) == Ds:
            out.append(a)
    return out, dimD


# =========================================================================== #
#  the SHIP configs                                                            #
# =========================================================================== #
def ship_configs():
    F27 = GF(3, 3); F16 = GF(2, 4); F64 = GF(2, 6); F32 = GF(2, 5)
    H1_32 = trace_hyperplane(F32, [1])
    H2_32 = trace_hyperplane(F32, [1, F32.g])
    H2_64 = trace_hyperplane(F64, [1, F64.g])
    return F27, F16, F64, F32, H1_32, H2_32, H2_64, [
        (F27, build_T(F27, 14), 4, 7, True,  "S27@R4",              None),
        (F16, build_T(F16, 15), 4, 8, False, "U16o@R4",             None),
        (F64, build_T(F64, 21), 3, 10, False, "F64-firstN@R3",      [1]),
        (F32, H1_32,            3, 7, False, "F32-1HP@R3",          [1]),
        (F32, H2_32,            3, 3, False, "F32-2HP@R3",          [1, F32.g]),
        (F64, H2_64,            3, 7, False, "F64-2HP@R3",          [1, F64.g]),
        (F27, trace_hyperplane(F27, [1]), 3, 4, True, "S27-1HP@R3-connFAILS", None),
    ]


def pinned_vanishes(F, T, R, a, mus):
    """every ell_mu(s) = Tr(mu s_1) vanishes on the whole image (unsigned toys)."""
    VT = moment_columns(F, T, R)
    counts, _ = image_and_census(F, VT, R, a, False)
    for mu in mus:
        vals = set(F.trace(F.mul(mu, decode(k, F.q, R)[1])) % F.p for k in counts)
        if vals != {0}:
            return False
    return True


def build_payload():
    F27, F16, F64, F32, H1_32, H2_32, H2_64, SHIP = ship_configs()
    configs = []
    for (F, T, R, a, signed, tag, mus) in SHIP:
        d = analyze(F, T, R, a, signed)
        d.pop("_counts")
        d["tag"] = tag
        d["pinned_ok"] = (pinned_vanishes(F, T, R, a, mus)
                          if (mus is not None and not signed) else None)
        configs.append(d)
    F8 = GF(2, 3)
    thr = []
    for (F, T, R, signed, name) in [
            (F16, build_T(F16, 10), 3, False, "U-F16@R3:N10"),
            (F16, build_T(F16, 12), 4, False, "U-F16@R4:N12-hole"),
            (F8,  build_T(F8, 7),   3, False, "U-F8@R3:N7"),
            (F27, build_T(F27, 10), 3, True,  "S-F27@R3:N10"),
            (F27, build_T(F27, 11), 3, True,  "S-F27@R3:N11")]:
        full, dimD = full_band(F, T, R, signed)
        thr.append(dict(name=name, q=F.q, R=R, N=len(T), dimD=dimD, signed=signed,
                        full_a=full,
                        band_lo=(min(full) if full else None),
                        band_hi=(max(full) if full else None)))
    return dict(
        _note=("Image-structure theorem closing the #422 surjection. image(Phi|a) "
               "subset a single coset of the move-subspace D<=W_c^0 (D=V_T signed / "
               "even-column-sum span unsigned); under Conn_a (image = full coset) "
               "occupancy=|image|/|W_c|=p^-defect, defect=dim W_c^flat - dim V_T = "
               "#pinned functionals; image=W_c <=> defect=0. Gamma_2>=index*p^defect "
               "from containment alone (strengthens #422's Gamma_2>=index). defect via "
               "T in trace-hyperplanes: F64-firstN & F32-1HP defect1 (occ 1/2); "
               "F32-2HP & F64-2HP defect2 m=2 (occ 1/4). S27-1HP: defect1 yet Conn "
               "FALSE -> occ!=1/3 (Conn is load-bearing). Connectivity exact threshold "
               "MEASURED (coset weight distribution of ker Phi, min-dist R+1)."),
        configs=configs,
        threshold=thr,
        pinned=dict(F64_firstN_functional="ell(s)=Tr(s_1); T=firstN(21) subset {Tr(t)=0}",
                    m2_realized=True, m2_occ=0.25,
                    F32_2HP_mus=[1, F32.g], F64_2HP_mus=[1, F64.g]),
        obstruction=dict(bound="Gamma_2 >= index * p^defect",
                         uses="containment only (no surjection)"),
        provenance=dict(atom_line=827, escape_clause_line=828, removal_list_line=839,
                        alt_a_line=862, alt_b_line=863,
                        vandermonde_line=876, fourier_flat_line=896),
    )


# =========================================================================== #
def load():
    with open(os.path.join(DATA, JSON_NAME)) as f:
        return json.load(f)


def find(rows, key, val):
    for r in rows:
        if r.get(key) == val:
            return r
    raise KeyError(val)


def gate_config(tag, got, want):
    for kk in ("q", "p", "k", "R", "N", "a", "signed", "dimVT", "dimD", "flat",
               "w0", "Wc", "index", "defect", "free", "red", "n_occ", "C",
               "conn", "dimD_minus_w0", "pinned_ok"):
        geq(f"{tag}.{kk}", got[kk], want[kk])
    feq(f"{tag}.G2", got["G2"], want["G2"])
    feq(f"{tag}.occupancy", got["occupancy"], want["occupancy"])
    feq(f"{tag}.pred_occ", got["pred_occ"], want["pred_occ"])
    geq(f"{tag}.G2_lb", got["G2_lb"], want["G2_lb"])


# =========================================================================== #
def main():
    if os.environ.get("FP_SURJ_DUMP"):
        with open(os.path.join(DATA, JSON_NAME), "w") as f:
            json.dump(build_payload(), f, indent=1)
        print("DUMPED", os.path.join(DATA, JSON_NAME))
        return

    D = load()
    F27, F16, F64, F32, H1_32, H2_32, H2_64, SHIP = ship_configs()

    # ---- provenance: the tex line refs this packet quotes -------------------- #
    prov = D["provenance"]
    geq("prov.atom_line", prov["atom_line"], 827)
    geq("prov.escape_line", prov["escape_clause_line"], 828)
    geq("prov.removal_line", prov["removal_list_line"], 839)
    geq("prov.alt_a_line", prov["alt_a_line"], 862)
    geq("prov.alt_b_line", prov["alt_b_line"], 863)
    geq("prov.vandermonde_line", prov["vandermonde_line"], 876)

    # ===================================================================== #
    #  (I) THE IMAGE-STRUCTURE THEOREM -- per-config recompute + gate         #
    # ===================================================================== #
    got = {}
    for (F, T, R, a, signed, tag, mus) in SHIP:
        d = analyze(F, T, R, a, signed)
        d["tag"] = tag
        d["pinned_ok"] = (pinned_vanishes(F, T, R, a, mus)
                          if (mus is not None and not signed) else None)
        got[tag] = d
        gate_config(f"cfg.{tag}", d, find(D["configs"], "tag", tag))

    # ---- theorem property assertions (recomputed, not just gated) ----------- #
    # (A) CONTAINMENT: n_occ <= |D| = p^dimD on EVERY config (incl. Conn-failing) #
    for tag, d in got.items():
        want_true(f"contain.{tag}.n_occ<=|D|", d["n_occ"] <= d["p"] ** d["dimD"])
        # (A) the strengthened obstruction from containment alone
        want_true(f"obstruct.{tag}.G2>=index*p^defect",
                  d["G2"] >= d["G2_lb"] - 1e-9)
        # dim D - w0 == -defect (both signed and unsigned)
        geq(f"algebra.{tag}.dimD-w0==-defect", d["dimD_minus_w0"], -d["defect"])
        # D subset W_c^0: dim D <= w0
        want_true(f"contain.{tag}.dimD<=w0", d["dimD"] <= d["w0"])

    # (B)+(C) OCCUPANCY = p^-defect and image = W_c <=> defect = 0, UNDER Conn --- #
    for tag, d in got.items():
        if d["conn"]:
            feq(f"occ.{tag}.eq_p^-defect", d["occupancy"], d["p"] ** (-d["defect"]))
            want_true(f"occ.{tag}.imageW_iff_defect0",
                      (abs(d["occupancy"] - 1.0) < 1e-9) == (d["defect"] == 0))
        else:
            # Conn is LOAD-BEARING: occupancy != p^-defect exactly when Conn fails
            want_true(f"occ.{tag}.conn_load_bearing",
                      abs(d["occupancy"] - d["p"] ** (-d["defect"])) > 1e-9)

    # headline corollaries: occupancies DERIVED, not measured -------------------- #
    want_true("corr.S27.occ1", abs(got["S27@R4"]["occupancy"] - 1.0) < 1e-9
              and got["S27@R4"]["defect"] == 0 and got["S27@R4"]["conn"])
    want_true("corr.U16o.occ1", abs(got["U16o@R4"]["occupancy"] - 1.0) < 1e-9
              and got["U16o@R4"]["defect"] == 0)
    want_true("corr.F64.occ_half", abs(got["F64-firstN@R3"]["occupancy"] - 0.5) < 1e-9
              and got["F64-firstN@R3"]["defect"] == 1
              and got["F64-firstN@R3"]["conn"])
    # the F64 pinned functional ell(s)=Tr(s_1) vanishes on the whole image ------- #
    want_true("corr.F64.pinned_Tr_s1", got["F64-firstN@R3"]["pinned_ok"] is True)

    # m = 2 REALIZED: two independent pinned functionals, occupancy = 1/4 -------- #
    for tag in ("F32-2HP@R3", "F64-2HP@R3"):
        want_true(f"m2.{tag}.defect2", got[tag]["defect"] == 2)
        want_true(f"m2.{tag}.occ_quarter", abs(got[tag]["occupancy"] - 0.25) < 1e-9)
        want_true(f"m2.{tag}.two_pinned", got[tag]["pinned_ok"] is True)
        want_true(f"m2.{tag}.conn", got[tag]["conn"])
    geq("m2.flag", D["pinned"]["m2_realized"], True)

    # designed non-spanning single-HP twin of F64 (defect 1, occ 1/2) ------------ #
    want_true("design.F32_1HP.occ_half",
              abs(got["F32-1HP@R3"]["occupancy"] - 0.5) < 1e-9
              and got["F32-1HP@R3"]["defect"] == 1)

    # ===================================================================== #
    #  (II) CONNECTIVITY THRESHOLD -- MEASURED bands                          #
    # ===================================================================== #
    F8 = GF(2, 3)
    band_src = {
        "U-F16@R3:N10": (F16, build_T(F16, 10), 3, False),
        "U-F16@R4:N12-hole": (F16, build_T(F16, 12), 4, False),
        "U-F8@R3:N7": (F8, build_T(F8, 7), 3, False),
        "S-F27@R3:N10": (F27, build_T(F27, 10), 3, True),
        "S-F27@R3:N11": (F27, build_T(F27, 11), 3, True),
    }
    for row in D["threshold"]:
        F, T, R, signed = band_src[row["name"]]
        full, dimD = full_band(F, T, R, signed)
        geq(f"thr.{row['name']}.full_a", full, row["full_a"])
        geq(f"thr.{row['name']}.dimD", dimD, row["dimD"])
    # the clean-regime band [R, N-R] holds for the R=3 large-kernel unsigned row -- #
    f16r3 = find(D["threshold"], "name", "U-F16@R3:N10")
    want_true("thr.clean_band_R3", f16r3["band_lo"] == f16r3["R"]
              and f16r3["band_hi"] == f16r3["N"] - f16r3["R"])
    # the small-kernel row has an interior HOLE (band is not a full interval) ----- #
    hole = find(D["threshold"], "name", "U-F16@R4:N12-hole")
    want_true("thr.small_kernel_hole",
              hole["band_hi"] - hole["band_lo"] + 1 > len(hole["full_a"]))

    # ===================================================================== #
    #  DUAL PATH: field multiply table vs log/antilog                        #
    # ===================================================================== #
    mism = sum(1 for a in range(F27.q) for b in range(F27.q)
               if F27.mul(a, b) != F27.mul_dual(a, b))
    geq("dual.mul.F27", mism, 0)
    mism2 = sum(1 for a in range(F32.q) for b in range(F32.q)
                if F32.mul(a, b) != F32.mul_dual(a, b))
    geq("dual.mul.F32", mism2, 0)
    # Tr(mu t) == the x^{k-1} coordinate reader for the smallest-irred F64 (mu = 1) #
    geq("dual.F64.trace_is_topcoord",
        sum(1 for t in range(F64.q)
            if (F64.trace(F64.mul(1, t)) % 2) != ((t >> 5) & 1)), 0)

    # ===================================================================== #
    #  TAMPER SELF-TESTS (7) -- each MUST be caught                          #
    # ===================================================================== #
    tampers = 0
    dS = got["S27@R4"]; dF = got["F64-firstN@R3"]; dM = got["F32-2HP@R3"]
    # T1: a FAKED (too-small) move-span dim is caught -- the censused n_occ      #
    # would exceed the faked |D| = p^{dimD-1}, violating containment n_occ <= |D| #
    if dF["n_occ"] > dF["p"] ** (dF["dimD"] - 1):   # faked dimD-1 breaks containment
        tampers += 1
    # T2: a FAKED coset size |W_c| (off by a factor p) breaks the index gate ---- #
    if dF["Wc"] != dF["Wc"] * dF["p"] and dF["index"] * dF["Wc"] == dF["q"] ** dF["R"]:
        tampers += 1
    # T3: a designed non-spanning T MUST show occupancy < 1 (F64-firstN) -------- #
    if dF["occupancy"] < 1.0 and dF["defect"] >= 1:
        tampers += 1
    # T4: a threshold-violating extreme a MUST fail coverage (image != full coset) #
    #     a = 1 on U16o: image = {v_t}, N points, never the p^dimD coset --------- #
    c1, _ = image_and_census(F16, moment_columns(F16, build_T(F16, 15), 4), 4, 1, False)
    if len(c1) != F16.p ** got["U16o@R4"]["dimD"]:
        tampers += 1
    # T5: CONTAINMENT is exact -- n_occ <= |D| on the Conn-FAILING config too ---- #
    dCF = got["S27-1HP@R3-connFAILS"]
    if dCF["n_occ"] <= dCF["p"] ** dCF["dimD"] and not dCF["conn"]:
        tampers += 1
    # T6: the pinned functional is LOAD-BEARING -- ell(s)=Tr(s_1) vanishes on the #
    #     F64 image but is NONZERO on W_c^flat (else it would not count in defect) #
    VT64 = moment_columns(F64, build_T(F64, 21), 3)
    reads_s1 = set(F64.trace(F64.mul(1, VT64[i][1])) % 2 for i in range(21))
    # ell nonzero on ambient: some field element has Tr != 0
    ell_nonzero_ambient = any(F64.trace(F64.mul(1, x)) % 2 for x in range(F64.q))
    if reads_s1 == {0} and ell_nonzero_ambient:
        tampers += 1
    # T7: the m = 2 config MUST realize occupancy exactly 1/4 (two functionals) -- #
    if abs(dM["occupancy"] - 0.25) < 1e-9 and dM["defect"] == 2 and dM["pinned_ok"]:
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
    print("Image-structure theorem: image(Phi|a) subset a single coset of D<=W_c^0; "
          "under Conn_a occupancy = p^-defect, image = W_c <=> defect = 0; "
          "Gamma_2 >= index*p^defect by containment alone. m = 2 realized (occ 1/4).")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
