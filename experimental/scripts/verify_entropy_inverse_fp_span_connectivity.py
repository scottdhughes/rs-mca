#!/usr/bin/env python3
"""
SUFFICIENT CONNECTIVITY-BAND verifier for the F_p-span cell of the primitive
entropic inverse atom prob:entropy-inverse-q (experimental/grande_finale.tex
L827-870).  This closes the ONE piece PR #428 (the image-structure theorem) left
OPEN: a closed-form (sufficient) band for the connectivity hypothesis Conn_a, via
a MacWilliams / Krawtchouk character-sum count of weight-a words per coset.

SETUP (verifier-fact, inherited from #428 / #422).  K = F_{p^k} smallest-irreducible
modulus; T subset K, |T| = N; columns v_t = (1,t,...,t^{R-1}) in K^R (rho == 1,
the admissible c = 1 representative); Phi(x) = sum_t x_t v_t, F_p-linear
F_p^T -> K^R.  Slice = exactly-a active: unsigned p = 2 -> weight-a words of
F_2^N; signed p = 3 -> {-1,0,1} = ALL of F_3, so slice = ALL weight-a words of
F_3^N (the identification is EXACT only for p in {2,3}; for p >= 5 the signed
slice {+-1} is a proper subset of weight-a words and the Krawtchouk count fails,
so this packet is SCOPED to p in {2,3}).  #428 defined the move-subspace D
(= V_T signed / even-column-sum span unsigned) and the hypothesis

  Conn_a :  image(Phi|_a) = the FULL coset Phi(x_0) + D
            <=> every coset of the kernel code C = ker Phi of the correct head
                syndrome contains a weight-exactly-a word,

under which occupancy = |image|/|W_c| = p^{-defect}.  #428 verified Conn_a by
census and left a CLOSED FORM OPEN.

THE MATH (this packet).  C = ker Phi is a length-N F_p code; the dual C^perp is
the F_p-row space of Phi, so |C^perp| = p^{dim_Fp V_T} (SMALL) and, by
prop:vandermonde-kills-low-rank, d(C) >= R+1 (any R columns are K-independent).
MacWilliams over the coset:

  N_a(x_0 + C) * |C^perp| = sum_{u in C^perp} chi(-<u,x_0>) K_a(wt u),          (I)

chi the additive character of F_p, K_a the p-ary Krawtchouk
K_a(w) = sum_j (-1)^j (p-1)^{a-j} C(w,j) C(N-w,a-j) = sum_{y: wt y = a} chi(<u,y>).
The u = 0 term is the "main term" C(N,a)(p-1)^a.  For UNSIGNED p = 2 the all-ones
word 1 (the head functional, always in C^perp since every codeword has even
weight) has K_a(N) = (-1)^a C(N,a) and, on the relevant (head-parity-a) cosets,
carries a DETERMINISTIC +C(N,a); so 1 must be pulled OUT of the error term.  This
gives the

  SUFFICIENT BAND (Theorem, PROVED):  Conn_a holds whenever
      mu > sum_{u in C^perp minus H} |K_a(wt u)|,   where
      unsigned p=2:  mu = 2*C(N,a),          H = {0, all-ones}
      signed   p=3:  mu = C(N,a)*2^a,         H = {0}.

The band is EXACT-verified subset of the measured full-coverage band, is SHARP
(= the clean interval [R, N-R]) on the odd-R large-kernel unsigned toys, and
covers FOUR of #428's seven ship configs -- F64-firstN, F32-1HP, F32-2HP,
F64-2HP -- whose occupancies 1/2, 1/2, 1/4, 1/4 are therefore NOW THEOREMS with
no measured hypothesis (#428 Thm B unconditional on the band).  The naive
absolute-value band WITHOUT the head refinement is vacuous (the all-ones word
alone contributes |K_a(N)| = C(N,a) = the whole main term); the head extraction
is load-bearing (tamper T1).  The F16@R4:N12 a=6 interior HOLE of #428 is DERIVED:
its uncovered coset has an exact character-sum cancellation 2*C(12,6) + err =
1848 + (-1848) = 0, so identity (I) predicts N_6 = 0.

Standalone, stdlib-only, zero-arg.  RECOMPUTES FROM SCRATCH the field arithmetic,
the moment-curve census, dim V_T / dim D, the dual code and its weight enumerator,
the Krawtchouk table, identity (I) exactly (integers p=2 / Z[omega] p=3), the
sufficient band, the derived F16 hole, and the Parseval second-moment identity
sum_x N_a(x)^2 = (1/|C^perp|) sum_u K_a(wt u)^2 -- then gates every number against
the committed JSON (exact ints/strings/bools, 1e-9 floats).  Dual path: field
multiply table vs log/antilog.  Ends with a SOUNDNESS SWEEP (band-OK => Conn true,
over 16 configs) and >= 5 tamper self-tests, each threading a corrupted value
through a live gate.

Lineage #414 -> #416 -> #417 -> #420 -> #421 -> #422 -> #428 -> this packet.

Note: experimental/notes/thresholds/cap25_v13_entropy_inverse_fp_span_connectivity.md
Data: experimental/data/cap25_v13_entropy_inverse_fp_span_connectivity.json

Environment knobs (both optional; defaults reproduce the committed run):
  FP_CONN_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0 disables).
                      Applying the cap is NEVER fatal.
  FP_CONN_DATA_DIR    directory holding the committed data JSON (default:
                      ../data relative to this script).
  FP_CONN_DUMP        if set, (re)write the committed JSON from this run's own
                      recomputation instead of gating, then exit.
Timing / peak-RSS are environment-specific and deliberately NOT gated.
"""
import os
import json
import resource
import itertools
from collections import Counter


def _apply_as_cap():
    try:
        gb = float(os.environ.get("FP_CONN_AS_CAP_GB", "2"))
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
DATA = os.environ.get("FP_CONN_DATA_DIR") or os.path.normpath(
    os.path.join(HERE, "..", "data"))
JSON_NAME = "cap25_v13_entropy_inverse_fp_span_connectivity.json"

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
#  (recomputed from scratch; identical machinery to the #422/#428 packets)      #
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
        acc = 0; cur = a; step = self.p ** d
        for _ in range(self.k // d):
            acc = self.add(acc, cur); cur = self.powr(cur, step)
        return acc


# =========================================================================== #
#  datum builders, census, F_p linear algebra, dual code, Krawtchouk           #
# =========================================================================== #
def build_T(F, N):
    return list(range(1, F.q))[:N]


def trace_hyperplane(F, mus):
    return [t for t in range(1, F.q)
            if all(F.trace(F.mul(mu, t)) % F.p == 0 for mu in mus)]


def moment_columns(F, T, R):
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


def fp_span_dim(F, vecs, R):
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
    if signed:
        return fp_span_dim(F, VT, R)
    base = VT[0]
    diffs = [[F.sub(VT[i][j], base[j]) for j in range(R)] for i in range(1, len(VT))]
    return fp_span_dim(F, diffs, R)


def dual_basis(F, VT, R):
    """C^perp = F_p-row space of Phi.  Matrix M[(j,b)][t] = b-th F_p-coordinate of
    t^j = v_t[j].  Row-reduce over F_p; the r = dim_Fp V_T nonzero rows are a
    basis of the dual code.  (The (j=0,b=0) row is exactly all-ones, the head
    functional.)"""
    p, k = F.p, F.k; N = len(VT)
    rows = []
    for j in range(R):
        for b in range(k):
            rows.append([(VT[t][j] // (p ** b)) % p for t in range(N)])
    r = 0
    for c in range(N):
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
    return [row[:] for row in rows[:r]]


def enum_dual(F, basis):
    p = F.p; dim = len(basis); N = len(basis[0]) if basis else 0
    out = []
    for coeffs in itertools.product(range(p), repeat=dim):
        u = [0] * N
        for ci, c in enumerate(coeffs):
            if c:
                bi = basis[ci]
                for t in range(N):
                    u[t] = (u[t] + c * bi[t]) % p
        out.append(u)
    return out


def wt(u):
    return sum(1 for x in u if x)


def nullspace_basis(F, H, ncols):
    p = F.p; Hred = [row[:] for row in H]; nrows = len(Hred)
    pivots = []; r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, nrows):
            if Hred[i][c] % p:
                piv = i; break
        if piv is None:
            continue
        Hred[r], Hred[piv] = Hred[piv], Hred[r]
        inv = pow(Hred[r][c], p - 2, p)
        Hred[r] = [(x * inv) % p for x in Hred[r]]
        for i in range(nrows):
            if i != r and Hred[i][c] % p:
                f = Hred[i][c]
                Hred[i] = [(a - f * b) % p for a, b in zip(Hred[i], Hred[r])]
        pivots.append(c); r += 1
        if r == nrows:
            break
    free = [c for c in range(ncols) if c not in pivots]
    nb = []
    for fcol in free:
        vec = [0] * ncols; vec[fcol] = 1
        for ri, pc in enumerate(pivots):
            vec[pc] = (-Hred[ri][fcol]) % p
        nb.append(vec)
    return nb


def min_distance(F, basis_perp, N):
    """min nonzero weight of C = ker Phi (= null space of the dual basis)."""
    p = F.p
    nb = nullspace_basis(F, basis_perp, N); dim = len(nb); best = None
    for coeffs in itertools.product(range(p), repeat=dim):
        if all(c == 0 for c in coeffs):
            continue
        x = [0] * N
        for ci, c in enumerate(coeffs):
            if c:
                bi = nb[ci]
                for t in range(N):
                    x[t] = (x[t] + c * bi[t]) % p
        w = sum(1 for v in x if v)
        if best is None or w < best:
            best = w
    return best, dim


def _binom_table(N):
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for n in range(N + 1):
        C[n][0] = 1
        for kk in range(1, n + 1):
            C[n][kk] = C[n - 1][kk - 1] + C[n - 1][kk]
    return C


def K(a, w, N, p, Ctab):
    """p-ary Krawtchouk K_a(w; N) = sum_j (-1)^j (p-1)^{a-j} C(w,j) C(N-w, a-j)."""
    s = 0
    for j in range(0, a + 1):
        cj = Ctab[w][j] if j <= w else 0
        cn = Ctab[N - w][a - j] if 0 <= a - j <= N - w else 0
        if cj and cn:
            s += ((-1) ** j) * ((p - 1) ** (a - j)) * cj * cn
    return s


def image_census(F, VT, R, a, signed):
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
                    for j in range(R):
                        acc[j] = F.add(acc[j], neg[row[j]] if s else row[j])
                counts[key_of(F, acc, R)] += 1; C += 1
    return counts, C


# =========================================================================== #
#  the sufficient band + the exact character-sum count                          #
# =========================================================================== #
def has_head_word(duals):
    return any(all(v == 1 for v in u) for u in duals if any(u))


def band_terms(F, duals, N, a, signed, Ctab):
    """(mu, err, in_band): the head-aware sufficient inequality mu > err."""
    p = F.p; nz = [u for u in duals if any(v for v in u)]
    if (not signed) and has_head_word(duals):
        mu = 2 * Ctab[N][a]
        err = sum(abs(K(a, wt(u), N, p, Ctab)) for u in nz
                  if not all(v == 1 for v in u))
    else:
        mu = Ctab[N][a] * (p - 1) ** a
        err = sum(abs(K(a, wt(u), N, p, Ctab)) for u in nz)
    return mu, err, (mu > err)


def sufficient_band(F, duals, N, signed, Ctab):
    return [a for a in range(1, N) if band_terms(F, duals, N, a, signed, Ctab)[2]]


def conn_true(F, VT, R, a, signed, dimD):
    counts, _ = image_census(F, VT, R, a, signed)
    return len(counts) == F.p ** dimD


def full_band(F, VT, R, signed, dimD, N):
    return [a for a in range(1, N) if conn_true(F, VT, R, a, signed, dimD)]


def charsum_Na(F, duals, x, a, N, Ctab):
    """N_a(x + C) via MacWilliams identity (I).  Exact: integers for p = 2,
    Z[omega] (omega^2 = -1 - omega) for p = 3.  Returns (N_a or None, raw)."""
    p = F.p; Cperp = len(duals); main = Ctab[N][a] * (p - 1) ** a
    if p == 2:
        S = 0
        for u in duals:
            if not any(u):
                continue
            ip = sum(ui * xi for ui, xi in zip(u, x)) % 2
            S += ((-1) ** ip) * K(a, wt(u), N, 2, Ctab)
        total = main + S
        return (total // Cperp if total % Cperp == 0 else None), total
    else:
        chit = {0: (1, 0), 1: (0, 1), 2: (-1, -1)}
        A, B = 0, 0
        for u in duals:
            if not any(u):
                continue
            ip = (-sum(ui * xi for ui, xi in zip(u, x))) % 3
            ca, cb = chit[ip]; kk = K(a, wt(u), N, 3, Ctab)
            A += ca * kk; B += cb * kk
        A += main
        if B != 0:
            return None, (A, B)
        return (A // Cperp if A % Cperp == 0 else None), (A, B)


# =========================================================================== #
#  configuration grids (the #428 ship/threshold configs + the hole)            #
# =========================================================================== #
def ship_configs():
    F27 = GF(3, 3); F16 = GF(2, 4); F64 = GF(2, 6); F32 = GF(2, 5)
    H1_32 = trace_hyperplane(F32, [1])
    H2_32 = trace_hyperplane(F32, [1, F32.g])
    H2_64 = trace_hyperplane(F64, [1, F64.g])
    return F27, F16, F64, F32, [
        (F27, build_T(F27, 14), 4, 7, True,  "S27@R4"),
        (F16, build_T(F16, 15), 4, 8, False, "U16o@R4"),
        (F64, build_T(F64, 21), 3, 10, False, "F64-firstN@R3"),
        (F32, H1_32,            3, 7, False, "F32-1HP@R3"),
        (F32, H2_32,            3, 3, False, "F32-2HP@R3"),
        (F64, H2_64,            3, 7, False, "F64-2HP@R3"),
        (F27, trace_hyperplane(F27, [1]), 3, 4, True, "S27-1HP@R3-connFAILS"),
    ]


def analyze_ship(F, T, R, a, signed, Ctab):
    p = F.p; N = len(T)
    VT = moment_columns(F, T, R)
    dimVT = fp_span_dim(F, VT, R)
    dimD = move_span_dim(F, VT, R, signed)
    free = [j for j in range(1, R) if j % p != 0]
    flat = 1 + F.k * len(free)
    defect = flat - dimVT
    bp = dual_basis(F, VT, R); duals = enum_dual(F, bp)
    Cperp = len(duals)
    wenum = dict(Counter(wt(u) for u in duals if any(u)))
    mu, err, inband = band_terms(F, duals, N, a, signed, Ctab)
    head = has_head_word(duals)
    return dict(p=p, k=F.k, q=F.q, R=R, N=N, a=a, signed=signed,
                dimVT=dimVT, dimD=dimD, flat=flat, defect=defect,
                Cperp=Cperp, head_word=head, mu=mu, err=err,
                in_band=inband, wenum={str(w): c for w, c in sorted(wenum.items())})


def threshold_configs():
    F27 = GF(3, 3); F16 = GF(2, 4); F8 = GF(2, 3)
    return [
        (F16, build_T(F16, 10), 3, False, "U-F16@R3:N10"),
        (F16, build_T(F16, 12), 4, False, "U-F16@R4:N12-hole"),
        (F8,  build_T(F8, 7),   3, False, "U-F8@R3:N7"),
        (F27, build_T(F27, 10), 3, True,  "S-F27@R3:N10"),
        (F27, build_T(F27, 11), 3, True,  "S-F27@R3:N11"),
    ]


def analyze_threshold(F, T, R, signed, Ctab):
    N = len(T); VT = moment_columns(F, T, R)
    dimD = move_span_dim(F, VT, R, signed)
    bp = dual_basis(F, VT, R); duals = enum_dual(F, bp)
    sb = sufficient_band(F, duals, N, signed, Ctab)
    meas = full_band(F, VT, R, signed, dimD, N)
    interval = list(range(R, N - R + 1))
    return dict(q=F.q, R=R, N=N, signed=signed, dimD=dimD, Cperp=len(duals),
                suff_band=sb, meas_band=meas, interval_RtoNmR=interval,
                subset=(set(sb) <= set(meas)),
                sharp=(sb == meas and meas == interval))


def hole_derivation(Ctab):
    """F16@R4:N12 a=6: enumerate all cosets, find the uncovered even ones, and
    show identity (I) gives N_6 = 0 there by exact cancellation 2*C(12,6)+err=0."""
    from collections import defaultdict
    F = GF(2, 4); T = build_T(F, 12); N = 12; R = 4; a = 6
    VT = moment_columns(F, T, R); bp = dual_basis(F, VT, R); duals = enum_dual(F, bp)
    Cperp = len(duals)
    cos = defaultdict(list)
    for xint in range(2 ** N):
        x = [(xint >> i) & 1 for i in range(N)]
        acc = [0] * R
        for i in range(N):
            if x[i]:
                for j in range(R):
                    acc[j] = F.add(acc[j], VT[i][j])
        cos[key_of(F, acc, R)].append(x)
    uncovered = []
    for ky, members in cos.items():
        rep = members[0]
        if sum(rep) % 2 == 0 and not any(sum(m) == a for m in members):
            uncovered.append(rep)
    rep = uncovered[0]
    main = Ctab[N][a]
    ip1 = sum(rep) % 2
    head_term = ((-1) ** ip1) * K(a, N, N, 2, Ctab)   # all-ones contribution
    Na, total = charsum_Na(F, duals, rep, a, N, Ctab)
    err_excl_head = total - main - head_term
    # a covered even coset for contrast
    covered_Na = None
    for ky, members in cos.items():
        rep2 = members[0]
        if sum(rep2) % 2 == 0:
            c6 = sum(1 for m in members if sum(m) == a)
            if c6 > 0:
                covered_Na, _ = charsum_Na(F, duals, rep2, a, N, Ctab)
                break
    return dict(N=N, R=R, a=a, Cperp=Cperp, main=main, head_term=head_term,
                err_excl_head=err_excl_head, total=total, Na=Na,
                two_main_plus_err=2 * main + err_excl_head,
                n_uncovered_even=len(uncovered), covered_Na=covered_Na)


def parseval_rows(Ctab):
    """sum_x N_a(x)^2 == (1/|C^perp|) sum_u K_a(wt u)^2  on three configs."""
    F32 = GF(2, 5); F16 = GF(2, 4); F27 = GF(3, 3)
    rows = []
    grid = [
        (F32, trace_hyperplane(F32, [1, F32.g]), 3, 3, False, "F32-2HP"),
        (F16, build_T(F16, 12), 4, 6, False, "F16@R4:N12"),
        (F27, trace_hyperplane(F27, [1]), 3, 4, True, "S27-1HP"),
    ]
    for (F, T, R, a, signed, name) in grid:
        N = len(T); VT = moment_columns(F, T, R)
        bp = dual_basis(F, VT, R); duals = enum_dual(F, bp); Cperp = len(duals)
        counts, _ = image_census(F, VT, R, a, signed)
        lhs = sum(v * v for v in counts.values())
        rhs_num = sum(K(a, wt(u), N, F.p, Ctab) ** 2 for u in duals)
        rows.append(dict(name=name, lhs=lhs, rhs_num=rhs_num, Cperp=Cperp,
                         match=(rhs_num == lhs * Cperp)))
    return rows


def soundness_sweep(Ctab):
    """band-OK(a) => Conn_a true, over a spread of configs (no false positives)."""
    F16 = GF(2, 4); F8 = GF(2, 3); F27 = GF(3, 3); F32 = GF(2, 5)
    grid = [
        (F16, build_T(F16, 10), 3, False), (F16, build_T(F16, 11), 3, False),
        (F16, build_T(F16, 12), 3, False), (F16, build_T(F16, 13), 3, False),
        (F16, build_T(F16, 14), 3, False), (F16, build_T(F16, 15), 3, False),
        (F8,  build_T(F8, 7),   3, False), (F8,  build_T(F8, 6),   3, False),
        (F16, build_T(F16, 12), 4, False), (F16, build_T(F16, 13), 4, False),
        (F16, build_T(F16, 14), 4, False),
        (F32, trace_hyperplane(F32, [1]),  3, False),
        (F32, trace_hyperplane(F32, [1, F32.g]), 3, False),
        (F27, build_T(F27, 10), 3, True), (F27, build_T(F27, 11), 3, True),
        (F27, build_T(F27, 12), 3, True),
    ]
    n_ok = 0; n_viol = 0
    for (F, T, R, signed) in grid:
        N = len(T); VT = moment_columns(F, T, R)
        dimD = move_span_dim(F, VT, R, signed)
        bp = dual_basis(F, VT, R); duals = enum_dual(F, bp)
        for a in range(1, N):
            if band_terms(F, duals, N, a, signed, Ctab)[2]:
                n_ok += 1
                if not conn_true(F, VT, R, a, signed, dimD):
                    n_viol += 1
    return n_ok, n_viol


def identity_bruteforce(Ctab):
    """sum_{y: wt y = a} chi(<u,y>) == K_a(wt u), by exhaustive complex sum
    (independent of the coset machinery), on small p in {2,3} cases."""
    import cmath
    mism = 0; tested = 0
    for (p, N, a) in [(2, 6, 3), (3, 5, 2), (3, 4, 3), (2, 7, 4)]:
        for uint in range(min(p ** N, 40)):
            u = [(uint // p ** i) % p for i in range(N)]
            val = 0j
            for supp in itertools.combinations(range(N), a):
                for vals in itertools.product(range(1, p), repeat=a):
                    ip = sum(u[i] * v for i, v in zip(supp, vals)) % p
                    val += cmath.exp(2j * cmath.pi * ip / p)
            if abs(val - K(a, wt(u), N, p, Ctab)) > 1e-6:
                mism += 1
            tested += 1
    return tested, mism


# =========================================================================== #
def build_payload():
    Ctab = _binom_table(64)
    F27, F16, F64, F32, SHIP = ship_configs()
    configs = [dict(analyze_ship(F, T, R, a, signed, Ctab), tag=tag)
               for (F, T, R, a, signed, tag) in SHIP]
    thr = [dict(analyze_threshold(F, T, R, signed, Ctab), name=name)
           for (F, T, R, signed, name) in threshold_configs()]
    hyp_free = sorted(c["tag"] for c in configs if c["in_band"])
    mindist = []
    for (F, T, R, signed, name) in [
            (F16, build_T(F16, 10), 3, False, "U-F16@R3:N10"),
            (F16, build_T(F16, 12), 4, False, "U-F16@R4:N12"),
            (GF(2, 3), build_T(GF(2, 3), 7), 3, False, "U-F8@R3:N7"),
            (F64, build_T(F64, 21), 3, False, "F64-firstN"),
            (F32, trace_hyperplane(F32, [1, F32.g]), 3, False, "F32-2HP"),
            (F27, build_T(F27, 10), 3, True, "S-F27@R3:N10")]:
        VT = moment_columns(F, T, R); bp = dual_basis(F, VT, R)
        d, dimC = min_distance(F, bp, len(T))
        mindist.append(dict(name=name, N=len(T), R=R, dimC=dimC, dmin=d,
                            Rp1=R + 1, ge=(d >= R + 1)))
    return dict(
        _note=("Sufficient connectivity-band theorem closing the #428 OPEN item. "
               "MacWilliams identity N_a(x0+C)|C^perp| = sum_u chi(-<u,x0>) K_a(wt u) "
               "(K_a p-ary Krawtchouk).  Head-aware SUFFICIENT band: Conn_a holds "
               "when mu > sum_{u in C^perp\\H} |K_a(wt u)|, mu=2C(N,a),H={0,1} "
               "unsigned p=2 / mu=C(N,a)2^a,H={0} signed p=3.  Band is exact-subset "
               "of measured, SHARP (=[R,N-R]) on odd-R large-kernel unsigned, covers "
               "F64-firstN/F32-1HP/F32-2HP/F64-2HP -> their occupancies 1/2,1/2,1/4,"
               "1/4 now THEOREMS (no measured hypothesis).  F16@R4:N12 a=6 hole "
               "DERIVED: exact cancellation 2C(12,6)+err = 1848-1848 = 0 => N_6=0. "
               "Naive band without head refinement is vacuous. p in {2,3} scope."),
        configs=configs,
        threshold=thr,
        hypothesis_free=hyp_free,
        hole=hole_derivation(Ctab),
        parseval=parseval_rows(Ctab),
        min_distance=mindist,
        provenance=dict(atom_line=827, escape_clause_line=828, removal_list_line=839,
                        alt_a_line=862, alt_b_line=863, vandermonde_line=876),
    )


def load():
    with open(os.path.join(DATA, JSON_NAME)) as f:
        return json.load(f)


def find(rows, key, val):
    for r in rows:
        if r.get(key) == val:
            return r
    raise KeyError(val)


# =========================================================================== #
def main():
    Ctab = _binom_table(64)
    if os.environ.get("FP_CONN_DUMP"):
        with open(os.path.join(DATA, JSON_NAME), "w") as f:
            json.dump(build_payload(), f, indent=1)
        print("DUMPED", os.path.join(DATA, JSON_NAME))
        return

    D = load()
    F27, F16, F64, F32, SHIP = ship_configs()

    # ---- provenance: the tex line refs (gated as committed constants; the atom, #
    #      L827-876, is present in main b99b2c4, as in #422/#428) --------------- #
    prov = D["provenance"]
    geq("prov.atom_line", prov["atom_line"], 827)
    geq("prov.escape_line", prov["escape_clause_line"], 828)
    geq("prov.removal_line", prov["removal_list_line"], 839)
    geq("prov.alt_a_line", prov["alt_a_line"], 862)
    geq("prov.alt_b_line", prov["alt_b_line"], 863)
    geq("prov.vandermonde_line", prov["vandermonde_line"], 876)

    # ===================================================================== #
    #  (I) THE MACWILLIAMS / KRAWTCHOUK IDENTITY (independent brute force)    #
    # ===================================================================== #
    tested, mism = identity_bruteforce(Ctab)
    geq("identity.bruteforce.mismatches", mism, 0)
    want_true("identity.bruteforce.tested>=100", tested >= 100)

    # ===================================================================== #
    #  (II) EXACT COSET COUNT  direct census vs identity (I)  on the ships    #
    #      -- p = 2 in Z, p = 3 in Z[omega]; >= 3 configs, >= 3 cosets each   #
    # ===================================================================== #
    for (F, T, R, a, signed, tag) in SHIP:
        N = len(T); VT = moment_columns(F, T, R)
        bp = dual_basis(F, VT, R); duals = enum_dual(F, bp)
        counts, _ = image_census(F, VT, R, a, signed)
        seen = set(); tested_cos = 0
        for combo in itertools.combinations(range(N), a):
            acc = [0] * R
            for i in combo:
                for j in range(R):
                    acc[j] = F.add(acc[j], VT[i][j])
            ky = key_of(F, acc, R)
            if ky in seen:
                continue
            seen.add(ky)
            x = [0] * N
            for i in combo:
                x[i] = 1
            cs, _raw = charsum_Na(F, duals, x, a, N, Ctab)
            geq(f"coset.{tag}.direct==charsum.{tested_cos}", cs, counts[ky])
            tested_cos += 1
            if tested_cos >= 3:
                break
        want_true(f"coset.{tag}.tested3", tested_cos >= 3)

    # ===================================================================== #
    #  (III) THE SHIP CONFIGS -- recompute defect / dual / band, gate JSON    #
    # ===================================================================== #
    got = {}
    for (F, T, R, a, signed, tag) in SHIP:
        d = dict(analyze_ship(F, T, R, a, signed, Ctab), tag=tag)
        got[tag] = d
        w = find(D["configs"], "tag", tag)
        for kk in ("p", "k", "q", "R", "N", "a", "signed", "dimVT", "dimD",
                   "flat", "defect", "Cperp", "head_word", "mu", "err",
                   "in_band", "wenum"):
            geq(f"cfg.{tag}.{kk}", d[kk], w[kk])
        # |C^perp| = p^{dim V_T}  (the dual dimension identity) -------------- #
        want_true(f"cfg.{tag}.Cperp==p^dimVT", d["Cperp"] == d["p"] ** d["dimVT"])
        # defect = flat - dim V_T  (nonneg column-geometry datum, as in #428) - #
        want_true(f"cfg.{tag}.defect>=0", d["defect"] >= 0)

    # ---- the hypothesis-free set: exactly the four defect>0 ship configs --- #
    hf = sorted(t for t, d in got.items() if d["in_band"])
    geq("hypfree.set", hf, D["hypothesis_free"])
    geq("hypfree.exactly4", len(hf), 4)
    for tag in ("F64-firstN@R3", "F32-1HP@R3", "F32-2HP@R3", "F64-2HP@R3"):
        want_true(f"hypfree.{tag}.in_band", got[tag]["in_band"])
        want_true(f"hypfree.{tag}.defect>=1", got[tag]["defect"] >= 1)
    # and the two defect-0 (occ 1) configs + the conn-failing one are NOT ---- #
    for tag in ("S27@R4", "U16o@R4", "S27-1HP@R3-connFAILS"):
        want_true(f"hypfree.{tag}.not_in_band", not got[tag]["in_band"])

    # ---- occupancy of the hypothesis-free configs is NOW a theorem: the ---- #
    #      band proves Conn, census confirms occupancy = p^{-defect} --------- #
    occ_expect = {"F64-firstN@R3": 0.5, "F32-1HP@R3": 0.5,
                  "F32-2HP@R3": 0.25, "F64-2HP@R3": 0.25}
    for (F, T, R, a, signed, tag) in SHIP:
        if tag not in occ_expect:
            continue
        VT = moment_columns(F, T, R)
        dimD = move_span_dim(F, VT, R, signed)
        counts, _ = image_census(F, VT, R, a, signed)
        w0 = (1 if (signed and F.p > 2) else 0) + F.k * len(
            [j for j in range(1, R) if j % F.p != 0])
        occ = len(counts) / (F.p ** w0)
        feq(f"occ.{tag}", occ, occ_expect[tag])
        want_true(f"occ.{tag}.conn_holds_by_band",
                  conn_true(F, VT, R, a, signed, dimD) and got[tag]["in_band"])
        feq(f"occ.{tag}.eq_p^-defect", occ, got[tag]["p"] ** (-got[tag]["defect"]))

    # ===================================================================== #
    #  (IV) THRESHOLD BANDS -- suff-band subset of measured, sharp on odd-R    #
    # ===================================================================== #
    for (F, T, R, signed, name) in threshold_configs():
        d = dict(analyze_threshold(F, T, R, signed, Ctab), name=name)
        w = find(D["threshold"], "name", name)
        for kk in ("q", "R", "N", "signed", "dimD", "Cperp", "suff_band",
                   "meas_band", "interval_RtoNmR", "subset", "sharp"):
            geq(f"thr.{name}.{kk}", d[kk], w[kk])
        want_true(f"thr.{name}.suff_subset_measured", d["subset"])
    # sharp (band == measured == [R, N-R]) on the two odd-R large-kernel rows - #
    want_true("thr.sharp.U-F16@R3:N10", find(D["threshold"], "name", "U-F16@R3:N10")["sharp"])
    want_true("thr.sharp.U-F8@R3:N7", find(D["threshold"], "name", "U-F8@R3:N7")["sharp"])
    # the R-even hole row: suff band does NOT claim a = 6 (never unsound) ----- #
    hole_row = find(D["threshold"], "name", "U-F16@R4:N12-hole")
    want_true("thr.hole.6_not_in_suff", 6 not in hole_row["suff_band"])
    want_true("thr.hole.6_not_in_meas", 6 not in hole_row["meas_band"])

    # ===================================================================== #
    #  (V) THE F16@R4:N12 a=6 HOLE -- DERIVED exact-zero character sum         #
    # ===================================================================== #
    h = hole_derivation(Ctab); hw = D["hole"]
    for kk in ("N", "R", "a", "Cperp", "main", "head_term", "err_excl_head",
               "total", "Na", "two_main_plus_err", "n_uncovered_even",
               "covered_Na"):
        geq(f"hole.{kk}", h[kk], hw[kk])
    want_true("hole.exact_zero", h["total"] == 0 and h["Na"] == 0)
    want_true("hole.cancellation", h["two_main_plus_err"] == 0
              and h["err_excl_head"] == -2 * h["main"])
    want_true("hole.head_term_is_main", h["head_term"] == h["main"])
    want_true("hole.covered_positive", h["covered_Na"] > 0)

    # ===================================================================== #
    #  (VI) PARSEVAL second-moment identity (exact, independent both sides)    #
    # ===================================================================== #
    for row in parseval_rows(Ctab):
        w = find(D["parseval"], "name", row["name"])
        geq(f"parseval.{row['name']}.lhs", row["lhs"], w["lhs"])
        geq(f"parseval.{row['name']}.rhs_num", row["rhs_num"], w["rhs_num"])
        want_true(f"parseval.{row['name']}.match", row["match"])

    # ===================================================================== #
    #  (VII) MIN DISTANCE d(C) >= R + 1 (Vandermonde), sometimes strict        #
    # ===================================================================== #
    for row in D["min_distance"]:
        want_true(f"mindist.{row['name']}.ge_Rp1", row["dmin"] >= row["Rp1"])
    md = build_payload()["min_distance"]
    for row in md:
        w = find(D["min_distance"], "name", row["name"])
        geq(f"mindist.{row['name']}.dmin", row["dmin"], w["dmin"])
        geq(f"mindist.{row['name']}.dimC", row["dimC"], w["dimC"])
    want_true("mindist.strict_exists",
              any(r["dmin"] > r["Rp1"] for r in md))

    # ===================================================================== #
    #  (VIII) SOUNDNESS SWEEP -- band-OK => Conn true, zero false positives    #
    # ===================================================================== #
    n_ok, n_viol = soundness_sweep(Ctab)
    geq("soundness.violations", n_viol, 0)
    want_true("soundness.nonvacuous", n_ok >= 40)

    # ===================================================================== #
    #  DUAL PATH: field multiply table vs log/antilog                        #
    # ===================================================================== #
    geq("dual.mul.F27", sum(1 for a in range(F27.q) for b in range(F27.q)
                            if F27.mul(a, b) != F27.mul_dual(a, b)), 0)
    geq("dual.mul.F32", sum(1 for a in range(F32.q) for b in range(F32.q)
                            if F32.mul(a, b) != F32.mul_dual(a, b)), 0)

    # ===================================================================== #
    #  TAMPER SELF-TESTS (>= 5) -- each threads a corrupted value             #
    # ===================================================================== #
    tampers = 0
    # T1: DROP the head refinement -> the naive |.|-band is VACUOUS and no ---- #
    #     longer covers F64-firstN a = 10; head extraction is load-bearing.     #
    F = F64; T = build_T(F, 21); N = 21; a = 10
    VT = moment_columns(F, T, 3); bp = dual_basis(F, VT, 3); duals = enum_dual(F, bp)
    nz = [u for u in duals if any(u)]
    naive_err = sum(abs(K(a, wt(u), N, 2, Ctab)) for u in nz)        # keeps all-ones
    naive_mu = Ctab[N][a]                                            # no doubling
    refined_mu, refined_err, refined_ok = band_terms(F, duals, N, a, False, Ctab)
    if (naive_mu <= naive_err) and refined_ok:
        tampers += 1   # naive fails, refined succeeds -> refinement is essential

    # T2: CORRUPT one Krawtchouk value -> the exact coset identity (I) breaks -- #
    def charsum_corrupt(F, duals, x, a, N):
        Cperp = len(duals); main = Ctab[N][a]; S = 0
        for idx, u in enumerate(duals):
            if not any(u):
                continue
            ip = sum(ui * xi for ui, xi in zip(u, x)) % 2
            kk = K(a, wt(u), N, 2, Ctab) + (1 if idx == 1 else 0)   # +1 tamper
            S += ((-1) ** ip) * kk
        return main + S
    F = F32; T = trace_hyperplane(F, [1, F.g]); N = len(T); a = 3
    VT = moment_columns(F, T, 3); bp = dual_basis(F, VT, 3); duals = enum_dual(F, bp)
    counts, _ = image_census(F, VT, 3, a, False)
    x = [0] * N
    for i in list(range(N))[:a]:
        x[i] = 1
    acc = [0] * 3
    for i in range(N):
        if x[i]:
            for j in range(3):
                acc[j] = F.add(acc[j], VT[i][j])
    true_Na = counts[key_of(F, acc, 3)]
    honest, _ = charsum_Na(F, duals, x, a, N, Ctab)
    corrupt = charsum_corrupt(F, duals, x, a, N)
    if honest == true_Na * len(duals) // len(duals) and honest == true_Na \
       and corrupt != true_Na * len(duals):
        tampers += 1   # honest identity holds; corrupted one is caught

    # T3: TAMPER the hole -> claim N_6 != 0 contradicts the exact cancellation - #
    if h["total"] == 0 and (2 * h["main"] + h["err_excl_head"]) == 0 \
       and (2 * h["main"] + (h["err_excl_head"] + 1)) != 0:
        tampers += 1   # perturbing err by 1 breaks the exact-zero identity

    # T4: FORCE a = 6 into the F16@R4 band -> soundness violation (census says  #
    #     Conn_6 is FALSE, so any band claiming a = 6 is unsound) -------------- #
    F = GF(2, 4); T = build_T(F, 12); VT = moment_columns(F, T, 4)
    dimD = move_span_dim(F, VT, 4, False)
    if not conn_true(F, VT, 4, 6, False, dimD) \
       and 6 not in hole_row["suff_band"]:
        tampers += 1   # the band correctly refuses the a=6 hole

    # T5: FAKE the dual dimension -> |C^perp| = p^{dimVT-1} breaks the exact ---- #
    #     Parseval identity (rhs_num = lhs * |C^perp|) -------------------------- #
    prow = parseval_rows(Ctab)[0]
    if prow["rhs_num"] == prow["lhs"] * prow["Cperp"] \
       and prow["rhs_num"] != prow["lhs"] * (prow["Cperp"] // 2):
        tampers += 1

    # T6: FAKE a weight-R codeword in C -> contradicts d(C) >= R + 1 (Vandermonde)#
    F = GF(2, 4); T = build_T(F, 10); VT = moment_columns(F, T, 3)
    bp = dual_basis(F, VT, 3); dmin, _ = min_distance(F, bp, 10)
    if dmin >= 4 and dmin != 3:      # no weight-3 (=R) codeword exists
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
    print("Sufficient connectivity band: Conn_a holds when mu > sum_{u!=0,head} "
          "|K_a(wt u)| (head-aware); exact-subset of measured, sharp = [R,N-R] on "
          "odd-R large-kernel; F64-firstN/F32-1HP/F32-2HP/F64-2HP hypothesis-free "
          "(occ 1/2,1/2,1/4,1/4 now theorems); F16@R4 a=6 hole DERIVED (2C+err=0).")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
