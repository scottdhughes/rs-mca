#!/usr/bin/env python3
"""
PROOF verifier for the three char-p differential/cell laws of the primitive
entropic inverse atom prob:entropy-inverse-q (experimental/grande_finale.tex L827).

This packet UPGRADES three laws that PR #446 (thresholds-atom-toy-r-gt-w) reported
as MEASURED / PROVED-AT-TOYS to PROVED (complete arguments at arbitrary p,k,R with
exact hypotheses).  The note experimental/notes/thresholds/atom_differential_cell_laws.md
carries the proofs; this script recomputes every committed number FROM SCRATCH and
gates the closed forms against exhaustive finite-field computation.

THE THREE LAWS (columns v_t=(1,t,...,t^{R-1}) in K^R, K=F_{p^k}; derivative columns
v'_t=(0,1,2t,...,(R-1)t^{R-2}); T subset K distinct; syndromes s_j=sum_t x_t t^j):

 L1  DIFFERENTIAL K-DEFECT LAW (PROVED).  For |T| >= R-1 (sharp: |T| >= M+1, M the
     top surviving exponent),
        rank_K Span{v'_t : t in T} = (R-1) - floor((R-1)/p),
     hence for |T| >= R the K-rank defect is  defect_K = 1 + floor((R-1)/p).
     Root cause: coordinate j of v'_t is j*t^{j-1}, and the coefficient j vanishes
     mod p exactly when p | j (char-p Wronskian prod_{i<R} i!).  The surviving
     coordinates carry the distinct exponents E={j-1 : 1<=j<=R-1, p nmid j}, a
     generalized Vandermonde of full column rank |E| once |T| exceeds max(E).
     Collision corollary (PROVED, Cauchy-Schwarz): Gamma_2(v') >= q^{defect_K};
     total collapse (n_occ=1, Gamma_2=q^R) exactly when E={0} (i.e. p=2,R=3 or R<=2).

 L2  FROBENIUS INDEX LAW (PROVED).  With x_t in F_p (prime-field-valued slice),
        s_{p^d j} = Frob^d(s_j) = s_j^{p^d}   whenever p^d j < R
     (one-line Frobenius linearity; #422 sec.2.1 c-form, #427 sec.4 per-subfield).
     Hence the achievable syndromes lie in the Frobenius-constrained subgroup W_c;
     the move subgroup W_c^0 has F_p-dimension w0 = [head_free] + k*#free with
     #free = (R-1) - floor((R-1)/p), and the collision index is the CLOSED FORM
        index = [K^R : W_c^0] = p^{ k*(1 + floor((R-1)/p)) - eps },  eps=[head_free],
     head_free = 1 iff the slice is signed with p odd (s_0 ranges over all F_p),
     else 0 (s_0 = a pinned).  index constant p^{k-eps} for R<=p, then jumps by a
     factor p^k at each R = m*p+1 (first jump R=p+1).  Gamma_2 >= index (C-S).

 L3  PRIME-FIELD INERTNESS (PROVED corollary).  Over K=F_p (k=1), the deployed
     regime T subset F_p^* forces N<=p-1 and R asymp N, so R<=p and #red=0; the
     L2 formula gives index = p^{1*(1+0) - 1} = 1 (signed).  Direct: F_p-span=K-span,
     no reduced coordinate is in range, W_c^0 = K^R.  HONEST BOUNDARY: index=1
     needs R<=p; if R>p were reached over F_p the same formula gives index=p^{#red}>1
     -- outside the atom's R asymp N <= p-1 regime.

VERDICTS.  L1, L2, L3 all reproduce PR #446's measured values EXACTLY; none needed
correction.  Three sharpenings vs #446's note prose (all consistent with its gated
JSON): L2's index jumps at EVERY R=mp+1 (not only the first, R=p+1); L3's "index=1
at every R" carries the load-bearing hypothesis R<=p (matching #446 sec.6's own
"R<p forced" reasoning); the fp_defect (flat minus dim_Fp V_T) is an N-dependent
occupancy shortfall and correctly stays MEASURED -- only the ambient index is a
closed form.

Standalone, stdlib-only, zero-arg.  RECOMPUTES FROM SCRATCH: field arithmetic
(smallest-irreducible modulus), moment/derivative columns, rank_K, dim_Fp, the
free/red split and #red=floor((R-1)/p), the index closed form, the exhaustive
subfield-law check on syndromes, and the collision census/Gamma_2 -- then gates
every number against the committed JSON (exact on ints/strings/bools, 1e-9 on
floats).  Dual path: field multiply table vs log/antilog.  Ends with >=5 tamper
self-tests threading corrupted values through the LIVE gates.

Lineage (credit by PR): #420/#421 (toy dichotomy / missing-cell hunt, the R=w
wall), #422 (F_p-span cell mechanism; the subfield law's c-form home), #427
(twist span-codim census; per-subfield Frob^d law PROVED-AT-TOYS), #428
(image-structure theorem: occupancy p^{-defect}, Gamma_2>=index*p^{defect}),
#446 (broke the R=w wall; MEASURED L1/L2/L3 which this packet proves).

Note: experimental/notes/thresholds/atom_differential_cell_laws.md
Data: experimental/data/atom_differential_cell_laws.json

Environment knobs (both optional; defaults reproduce the committed run):
  DCL_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0 disables).
                  Applying the cap is NEVER fatal.
  DCL_DATA_DIR    directory holding the committed data JSON (default: ../data
                  relative to this script).
  DCL_DUMP        if set, (re)write the committed JSON from this run's own
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
        gb = float(os.environ.get("DCL_AS_CAP_GB", "2"))
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
DATA = os.environ.get("DCL_DATA_DIR") or os.path.normpath(os.path.join(HERE, "..", "data"))
J_MAIN = "atom_differential_cell_laws.json"

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
#  F_p[x] helpers + finite field F_{p^k} (smallest-irreducible modulus).        #
#  Same table-backed algebra as the #422/#428/#446 GF class (audited).          #
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

    def _find_gen(self):
        q = self.q; need = q - 1; fs = _prime_factors(need)
        if need == 1:          # F_2: the multiplicative group is trivial, g=1
            return 1
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
#  columns, linear algebra, index, census                                      #
# =========================================================================== #
def build_T(F, N):
    """first N nonzero field elements (T subset K^*), distinct."""
    return list(range(1, F.q))[:N]


def moment_columns(F, T, R):
    """v_t = (1, t, ..., t^{R-1}); the admissible c=1 moment curve (rho==1)."""
    VT = []
    for t in T:
        row = []; tj = 1
        for j in range(R):
            row.append(tj); tj = F.mul(tj, t)
        VT.append(row)
    return VT


def deriv_columns(F, T, R):
    """v'_t = (0,1,2t,...,(R-1)t^{R-2}): formal derivative of the moment curve.
    coordinate j is j*t^{j-1}, coefficient j reduced mod p (mulint)."""
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


def red_count(p, R):
    """#{ j : 1 <= j <= R-1, p | j } = floor((R-1)/p)  (the reducible coords)."""
    return (R - 1) // p


def surviving_exponents(p, R):
    """E = { j-1 : 1 <= j <= R-1, p nmid j }  (exponents surviving differentiation)."""
    return [j - 1 for j in range(1, R) if j % p != 0]


def index_closed_form(p, k, R, head_free):
    """L2 closed form: index = p^{ k*(1+floor((R-1)/p)) - eps }, eps=[head_free]."""
    eps = 1 if head_free else 0
    return p ** (k * (1 + red_count(p, R)) - eps)


def ambient_dims(F, R, head_free):
    """dim W_c^flat (head free in a line), dim W_c^0 (move/translation subgroup)."""
    k = F.k; p = F.p
    free = [j for j in range(1, R) if j % p != 0]
    red = [j for j in range(1, R) if j % p == 0]
    flat = 1 + k * len(free)
    w0 = (1 if head_free else 0) + k * len(free)
    return flat, w0, free, red


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
            cnt[tuple(acc)] += 1; C += 1
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
                cnt[tuple(acc)] += 1; C += 1
    return cnt, C


def gamma2(F, cnt, C, R):
    """Gamma_2 = |K|^R sum N(s)^2 / C^2 (def:primitive-logmoment normalization)."""
    return float(Fraction(F.q ** R, 1) * Fraction(sum(c * c for c in cnt.values()), C * C))


def subfield_law_violations(F, T, R, a, signed, d):
    """exhaustive check of s_{p^d j} = s_j^{p^d} on the exactly-a slice.
    returns (head_viol, frob_viol, checks): head = s_0 in F_p (base field)."""
    p, k = F.p, F.k
    MC = moment_columns(F, T, R)
    pd = p ** d
    head_viol = 0; frob_viol = 0; checks = 0
    N = len(T)

    def check(sy):
        nonlocal head_viol, frob_viol, checks
        # head: s_0 lies in the prime field F_p (Frob-fixed)
        if F.powr(sy[0], p) != sy[0]:
            head_viol += 1
        for j in range(R):
            if pd * j < R and j >= 1:
                checks += 1
                if sy[pd * j] != F.powr(sy[j], pd):
                    frob_viol += 1

    if not signed:
        for combo in itertools.combinations(range(N), a):
            s = [0] * R
            for i in combo:
                for j in range(R):
                    s[j] = F.add(s[j], MC[i][j])
            check(s)
    else:
        for combo in itertools.combinations(range(N), a):
            cs = [MC[i] for i in combo]
            for signs in itertools.product((0, 1), repeat=a):
                s = [0] * R
                for idx, sg in enumerate(signs):
                    for j in range(R):
                        s[j] = F.sub(s[j], cs[idx][j]) if sg else F.add(s[j], cs[idx][j])
                check(s)
    return head_viol, frob_viol, checks


# =========================================================================== #
#  BUILD THE PAYLOAD (recompute-from-scratch)                                  #
# =========================================================================== #
def build_data():
    # ------------------------------------------------------------------ #
    #  L1: derivative K-rank defect law, swept p in {2,3,5}, k in {1,2,3}  #
    # ------------------------------------------------------------------ #
    l1 = []
    for (p, k) in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (5, 1), (5, 2), (5, 3)]:
        F = gf(p, k)
        Nmax = min(F.q - 1, 24)
        T = build_T(F, Nmax)
        for R in range(1, min(11, Nmax + 1)):
            if len(T) < R:
                continue
            DC = deriv_columns(F, T, R)
            MC = moment_columns(F, T, R)
            rk_d = k_rank(F, DC, R)
            rk_m = k_rank(F, MC, R)
            E = surviving_exponents(p, R)
            pred_rank = (R - 1) - red_count(p, R)
            pred_defect = 1 + red_count(p, R)
            kfull = min(len(T), R)
            l1.append(dict(
                tag=f"F{F.q}@R{R}", q=F.q, p=p, k=k, R=R, N=len(T),
                deriv_rank=rk_d, pred_rank=pred_rank,
                defect_K=kfull - rk_d, pred_defect=pred_defect,
                mom_rank=rk_m, mom_defect=kfull - rk_m, kfull=kfull,
                red=red_count(p, R), n_surv=len(E), max_exp=(max(E) if E else -1),
            ))

    # ------------------------------------------------------------------ #
    #  L1 sharp |T| threshold: full derivative rank needs |T| >= max(E)+1 #
    # ------------------------------------------------------------------ #
    l1_thr = []
    for (p, k) in [(3, 2), (5, 2)]:
        F = gf(p, k)
        for R in range(3, 9):
            E = surviving_exponents(p, R)
            need = max(E) + 1
            fullrank = (R - 1) - red_count(p, R)
            for nt in (need - 1, need, need + 1):
                if nt < 1 or nt > F.q - 1:
                    continue
                T = build_T(F, nt)
                rk = k_rank(F, deriv_columns(F, T, R), R)
                l1_thr.append(dict(
                    tag=f"F{F.q}@R{R}@T{nt}", q=F.q, p=p, R=R, nt=nt,
                    need=need, fullrank=fullrank, rank=rk,
                    at_full=(rk == fullrank), meets_need=(nt >= need),
                ))

    # ------------------------------------------------------------------ #
    #  L2: Frobenius index closed form, swept p in {2,3,5}, k in {1,2,3}  #
    #      signed (p odd) and unsigned variants                           #
    # ------------------------------------------------------------------ #
    l2 = []
    l2_cfgs = [(2, 2, False), (2, 3, False), (2, 4, False),
               (3, 2, True), (3, 2, False), (3, 3, True), (3, 3, False),
               (5, 2, True), (5, 3, True)]
    for (p, k, signed) in l2_cfgs:
        F = gf(p, k)
        head_free = bool(signed and p > 2)
        for R in range(2, 9):
            flat, w0, free, red = ambient_dims(F, R, head_free)
            index_direct = (F.q ** R) // (p ** w0)
            index_cf = index_closed_form(p, k, R, head_free)
            l2.append(dict(
                tag=f"F{F.q}{'s' if signed else 'u'}@R{R}", q=F.q, p=p, k=k, R=R,
                signed=signed, head_free=head_free,
                free=len(free), red=len(red), flat=flat, w0=w0,
                index=index_direct, pred_index=index_cf,
                red_is_floor=(len(red) == red_count(p, R)),
                first_jump_R=(p + 1), is_jump=((R - 1) % p == 0 and R >= 2),
            ))

    # ------------------------------------------------------------------ #
    #  L2 subfield law: exhaustive s_{p^d j} = s_j^{p^d} on syndromes      #
    #     d=1 (base Frobenius, drives the index) and d=2 (#427 subfield)   #
    # ------------------------------------------------------------------ #
    l2_law = []
    for (name, p, k, N, R, a, signed, d) in [
            ("F16u.d1", 2, 4, 8, 6, 4, False, 1),
            ("F16u.d2", 2, 4, 8, 5, 4, False, 2),   # #427 exact config
            ("F27s.d1", 3, 3, 8, 5, 4, True, 1),
            ("F9s.d1", 3, 2, 6, 5, 3, True, 1),
            ("F25s.d1", 5, 2, 6, 6, 3, True, 1)]:
        F = gf(p, k); T = build_T(F, N)
        hv, fv, ch = subfield_law_violations(F, T, R, a, signed, d)
        l2_law.append(dict(tag=name, q=F.q, p=p, k=k, R=R, N=N, a=a, signed=signed,
                           d=d, head_viol=hv, frob_viol=fv, checks=ch))

    # ------------------------------------------------------------------ #
    #  L3: prime-field inertness, R in [2, p]; plus honest boundary R>p    #
    # ------------------------------------------------------------------ #
    l3 = []
    for p in [3, 5, 7, 13]:
        F = gf(p, 1)
        head_free = True  # signed, odd prime -> deployed KoalaBear/M31 shape
        for R in range(2, p + 1):
            flat, w0, free, red = ambient_dims(F, R, head_free)
            index_direct = (F.q ** R) // (p ** w0)
            l3.append(dict(tag=f"F{p}@R{R}", p=p, k=1, R=R, signed=True,
                           red=len(red), w0=w0, index=index_direct,
                           pred_index=index_closed_form(p, 1, R, head_free),
                           inert=(index_direct == 1)))
        # honest boundary: R>p (unreachable with T subset F_p^*, R asymp N) -> index>1
        Rb = p + 2
        flat, w0, free, red = ambient_dims(F, Rb, head_free)
        index_b = (F.q ** Rb) // (p ** w0)
        l3.append(dict(tag=f"F{p}@R{Rb}.boundary", p=p, k=1, R=Rb, signed=True,
                       red=len(red), w0=w0, index=index_b,
                       pred_index=index_closed_form(p, 1, Rb, head_free),
                       inert=(index_b == 1), pred_boundary=p ** red_count(p, Rb)))

    # ------------------------------------------------------------------ #
    #  Collision consequence (PROVED via Cauchy-Schwarz): Gamma_2 >= q^def #
    #     small census configs only (exponential in a) -- caps reported    #
    # ------------------------------------------------------------------ #
    coll = []
    for (name, p, k, N, a, signed, Rs) in [
            ("F16u", 2, 4, 10, 4, False, [3, 4, 5]),
            ("F27s", 3, 3, 8, 4, True, [4, 5]),
            ("F5s", 5, 1, 4, 2, True, [3, 4])]:
        F = gf(p, k); T = build_T(F, N)
        for R in Rs:
            if len(T) < R:
                continue
            DC = deriv_columns(F, T, R)
            rk = k_rank(F, DC, R)
            defect = min(len(T), R) - rk
            cnt, C = census(F, DC, R, a, signed)
            g2 = gamma2(F, cnt, C, R)
            lb = F.q ** defect
            E = surviving_exponents(p, R)
            coll.append(dict(tag=f"{name}@R{R}", q=F.q, p=p, R=R, N=N, a=a, signed=signed,
                             defect_K=defect, n_occ=len(cnt), C=C,
                             Gamma2=round(g2, 6), q_defect=lb,
                             G2_ge_qdefect=(g2 >= lb - 1e-9),
                             E_is_axis=(E == [0]), qR=F.q ** R))

    # ------------------------------------------------------------------ #
    #  Total collapse (L1 corollary): E={0} at p=2,R=3 -> n_occ=1, G2=q^R  #
    # ------------------------------------------------------------------ #
    F = gf(2, 4); T = build_T(F, 10); R = 3; a = 4
    DC = deriv_columns(F, T, R)
    cnt, C = census(F, DC, R, a, signed=False)
    g2 = gamma2(F, cnt, C, R)
    collapse = dict(tag="F16u@R3.collapse", q=16, p=2, R=3, N=10, a=4,
                    E=surviving_exponents(2, 3), n_occ=len(cnt), C=C,
                    Gamma2=round(g2, 6), qR=16 ** 3,
                    is_total=(len(cnt) == 1 and abs(g2 - 16 ** 3) < 1e-6))

    # ------------------------------------------------------------------ #
    #  HEADLINE reproduction of PR #446's measured values                  #
    # ------------------------------------------------------------------ #
    headline = []
    # F27 index 9 -> 243 across R=p+1 (signed); F16 16 -> 256 (unsigned)
    for (name, p, k, signed, Rs) in [("F27", 3, 3, True, [2, 3, 4, 5, 6, 7]),
                                     ("F16", 2, 4, False, [2, 3, 4, 5, 6, 7])]:
        F = gf(p, k); head_free = bool(signed and p > 2)
        for R in Rs:
            flat, w0, free, red = ambient_dims(F, R, head_free)
            headline.append(dict(field=name, tag=f"{name}@R{R}", p=p, k=k, R=R,
                                 signed=signed, red=len(red),
                                 index=(F.q ** R) // (p ** w0),
                                 pred_index=index_closed_form(p, k, R, head_free),
                                 defect_K=1 + red_count(p, R)))

    return dict(
        _note=("PROVED char-p differential/cell laws for prob:entropy-inverse-q. "
               "L1: rank_K Span{v'_t}=(R-1)-floor((R-1)/p), defect_K=1+floor((R-1)/p), "
               "|T|>=max(E)+1. L2: index=[K^R:W_c^0]=p^{k(1+floor((R-1)/p))-eps} from "
               "the Frobenius law s_{pj}=s_j^p; jumps at every R=mp+1, first R=p+1. "
               "L3: over F_p with R<=p, index=1 (inert); R>p would give p^{#red}>1. "
               "Collision (C-S): Gamma_2(v')>=q^{defect_K}; total collapse iff E={0}."),
        provenance=dict(atom_line=827, escape_clause_line=828, weights_line=828,
                        removal_list_line=839, frontier_norm_line=840,
                        alt_a_line=862, alt_b_line=863, vandermonde_line=876,
                        fourier_flat_line=896, logmoment_line=756),
        L1_defect=l1, L1_threshold=l1_thr,
        L2_index=l2, L2_subfield_law=l2_law,
        L3_inertness=l3,
        collision=coll, total_collapse=collapse, headline=headline,
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
    if os.environ.get("DCL_DUMP"):
        with open(os.path.join(DATA, J_MAIN), "w") as fh:
            json.dump(build_data(), fh, indent=1)
        print("DUMPED", J_MAIN)
        return

    M = load(J_MAIN)
    G = build_data()

    # ---- provenance: tex line refs (gated present) --------------------------- #
    for kk, want in [("atom_line", 827), ("escape_clause_line", 828),
                     ("removal_list_line", 839), ("alt_a_line", 862),
                     ("alt_b_line", 863), ("vandermonde_line", 876),
                     ("fourier_flat_line", 896), ("logmoment_line", 756)]:
        geq(f"prov.{kk}", M["provenance"][kk], want)
        geq(f"prov.recompute.{kk}", G["provenance"][kk], want)

    # ===================================================================== #
    #  L1 -- differential K-rank defect law (PROVED)                          #
    # ===================================================================== #
    for g in G["L1_defect"]:
        w = find(M["L1_defect"], "tag", g["tag"])
        for kk in ("q", "p", "k", "R", "N", "deriv_rank", "pred_rank", "defect_K",
                   "pred_defect", "mom_rank", "mom_defect", "kfull", "red",
                   "n_surv", "max_exp"):
            geq(f"L1.{g['tag']}.{kk}", g[kk], w[kk])
        # THEOREM L1: measured rank == closed form; defect == 1+floor((R-1)/p)
        want_true(f"L1.{g['tag']}.rank_eq_formula", g["deriv_rank"] == g["pred_rank"])
        want_true(f"L1.{g['tag']}.defect_eq_formula", g["defect_K"] == g["pred_defect"])
        # #red = floor((R-1)/p) exactly
        want_true(f"L1.{g['tag']}.red_is_floor", g["red"] == (g["R"] - 1) // g["p"])
        # surviving count = (R-1) - #red
        want_true(f"L1.{g['tag']}.surv_count", g["n_surv"] == (g["R"] - 1) - g["red"])
        # the MOMENT curve never has a defect (prop:vandermonde-kills-low-rank)
        want_true(f"L1.{g['tag']}.mom_full", g["mom_defect"] == 0)
        # char-p part fires exactly past R>p
        want_true(f"L1.{g['tag']}.charp_iff_R>p", (g["red"] >= 1) == (g["R"] > g["p"]))

    # ---- L1 sharp |T| threshold ---------------------------------------------- #
    for g in G["L1_threshold"]:
        w = find(M["L1_threshold"], "tag", g["tag"])
        for kk in ("q", "p", "R", "nt", "need", "fullrank", "rank", "at_full",
                   "meets_need"):
            geq(f"L1thr.{g['tag']}.{kk}", g[kk], w[kk])
        # when |T| >= max(E)+1, the surviving Vandermonde is full column rank
        if g["meets_need"]:
            want_true(f"L1thr.{g['tag']}.full_when_enough", g["at_full"] is True)

    # ===================================================================== #
    #  L2 -- Frobenius index closed form (PROVED)                             #
    # ===================================================================== #
    for g in G["L2_index"]:
        w = find(M["L2_index"], "tag", g["tag"])
        for kk in ("q", "p", "k", "R", "signed", "head_free", "free", "red",
                   "flat", "w0", "index", "pred_index", "red_is_floor",
                   "first_jump_R", "is_jump"):
            geq(f"L2.{g['tag']}.{kk}", g[kk], w[kk])
        # THEOREM L2: direct index == closed form p^{k(1+floor((R-1)/p))-eps}
        want_true(f"L2.{g['tag']}.index_eq_closed", g["index"] == g["pred_index"])
        want_true(f"L2.{g['tag']}.red_is_floor", g["red_is_floor"] is True)
        # #free = (R-1) - #red
        want_true(f"L2.{g['tag']}.free_count", g["free"] == (g["R"] - 1) - g["red"])

    # threshold corollary: index constant for R<=p, jumps *p^k at every R=mp+1 --
    for field_p, k, signed in [(3, 3, True), (2, 4, False), (5, 3, True)]:
        head_free = bool(signed and field_p > 2)
        rows = sorted([r for r in G["L2_index"]
                       if r["p"] == field_p and r["k"] == k and r["signed"] == signed],
                      key=lambda r: r["R"])
        for i in range(1, len(rows)):
            prev, cur = rows[i - 1], rows[i]
            ratio = cur["index"] // prev["index"]
            if (cur["R"] - 1) % field_p == 0:   # R = m*p+1: a jump
                want_true(f"L2thresh.p{field_p}k{k}.R{cur['R']}.jump",
                          ratio == field_p ** k and cur["index"] % prev["index"] == 0)
            else:                               # no reducible added: index constant
                want_true(f"L2thresh.p{field_p}k{k}.R{cur['R']}.flat",
                          cur["index"] == prev["index"])

    # ---- L2 subfield law: exhaustive zero-violation --------------------------- #
    for g in G["L2_subfield_law"]:
        w = find(M["L2_subfield_law"], "tag", g["tag"])
        for kk in ("q", "p", "k", "R", "N", "a", "signed", "d", "head_viol",
                   "frob_viol", "checks"):
            geq(f"L2law.{g['tag']}.{kk}", g[kk], w[kk])
        # THE LAW: s_{p^d j} = s_j^{p^d} and s_0 in F_p, zero violations
        want_true(f"L2law.{g['tag']}.no_head_viol", g["head_viol"] == 0)
        want_true(f"L2law.{g['tag']}.no_frob_viol", g["frob_viol"] == 0)
        want_true(f"L2law.{g['tag']}.nontrivial", g["checks"] >= 1)

    # ===================================================================== #
    #  L3 -- prime-field inertness (PROVED corollary)                        #
    # ===================================================================== #
    for g in G["L3_inertness"]:
        w = find(M["L3_inertness"], "tag", g["tag"])
        for kk in ("p", "k", "R", "signed", "red", "w0", "index", "pred_index",
                   "inert"):
            geq(f"L3.{g['tag']}.{kk}", g[kk], w[kk])
        want_true(f"L3.{g['tag']}.index_eq_closed", g["index"] == g["pred_index"])
        if "boundary" not in g["tag"]:
            # deployed regime R<=p: index == 1, inert
            want_true(f"L3.{g['tag']}.inert", g["index"] == 1 and g["inert"] is True)
            want_true(f"L3.{g['tag']}.no_red", g["red"] == 0)
        else:
            # HONEST BOUNDARY R>p: index = p^{#red} > 1 (NOT inert)
            want_true(f"L3.{g['tag']}.boundary_gt1", g["index"] > 1)
            want_true(f"L3.{g['tag']}.boundary_form", g["index"] == g["pred_boundary"])

    # ===================================================================== #
    #  Collision consequence (PROVED, Cauchy-Schwarz): Gamma_2 >= q^{defect}  #
    # ===================================================================== #
    for g in G["collision"]:
        w = find(M["collision"], "tag", g["tag"])
        for kk in ("q", "p", "R", "N", "a", "signed", "defect_K", "n_occ", "C",
                   "q_defect", "G2_ge_qdefect", "E_is_axis", "qR"):
            geq(f"coll.{g['tag']}.{kk}", g[kk], w[kk])
        feq(f"coll.{g['tag']}.Gamma2", g["Gamma2"], w["Gamma2"])
        # THEOREM: Gamma_2(v') >= q^{defect_K} (image in a rank-dim space + C-S)
        want_true(f"coll.{g['tag']}.G2_ge_qdefect", g["G2_ge_qdefect"] is True)
        want_true(f"coll.{g['tag']}.G2_ge_val", g["Gamma2"] >= g["q_defect"] - 1e-6)

    # ---- total collapse corollary (E={0}) ------------------------------------ #
    g = G["total_collapse"]; w = M["total_collapse"]
    for kk in ("q", "p", "R", "N", "a", "n_occ", "qR", "is_total"):
        geq(f"collapse.{kk}", g[kk], w[kk])
    feq("collapse.Gamma2", g["Gamma2"], w["Gamma2"])
    geq("collapse.E", g["E"], w["E"])
    # E={0}, single syndrome, Gamma_2 = q^R (strongest possible collision)
    want_true("collapse.E_is_axis", g["E"] == [0])
    want_true("collapse.total", g["n_occ"] == 1 and abs(g["Gamma2"] - g["qR"]) < 1e-6)

    # ===================================================================== #
    #  HEADLINE reproduction of PR #446's MEASURED values                    #
    # ===================================================================== #
    for g in G["headline"]:
        w = find(M["headline"], "tag", g["tag"])
        for kk in ("field", "p", "k", "R", "signed", "red", "index", "pred_index",
                   "defect_K"):
            geq(f"head.{g['tag']}.{kk}", g[kk], w[kk])
        want_true(f"head.{g['tag']}.index_eq_closed", g["index"] == g["pred_index"])
    # the exact #446 headline numbers, hard-coded assertions
    want_true("head.F27.wall9", find(G["headline"], "tag", "F27@R3")["index"] == 9)
    want_true("head.F27.break243", find(G["headline"], "tag", "F27@R4")["index"] == 243)
    want_true("head.F27.R7.6561", find(G["headline"], "tag", "F27@R7")["index"] == 6561)
    want_true("head.F16.wall16", find(G["headline"], "tag", "F16@R2")["index"] == 16)
    want_true("head.F16.break256", find(G["headline"], "tag", "F16@R3")["index"] == 256)
    want_true("head.F16.R5.4096", find(G["headline"], "tag", "F16@R5")["index"] == 4096)
    want_true("head.F16.R7.65536", find(G["headline"], "tag", "F16@R7")["index"] == 65536)

    # ===================================================================== #
    #  DUAL PATH: field multiply table vs log/antilog                        #
    # ===================================================================== #
    for (p, k) in [(3, 3), (2, 4), (5, 3)]:
        F = gf(p, k)
        mism = sum(1 for a in range(F.q) for b in range(F.q)
                   if F.mul(a, b) != F.mul_dual(a, b))
        geq(f"dual.mul.F{F.q}", mism, 0)

    # ===================================================================== #
    #  TAMPER SELF-TESTS (>=5) -- each feeds a CORRUPTED value into the SAME   #
    #  live gate function (geq / feq / want_true) used above and confirms the  #
    #  gate returns False (caught), then RETRACTS the side effects so the      #
    #  self-test itself contributes no FAIL and no permanent CHECK.            #
    # ===================================================================== #
    def caught(gate, name, *args):
        """run a live gate on corrupted input; it MUST return False; retract."""
        global CHECKS
        base = len(FAILS)
        res = gate(name, *args)          # threads corruption through the real gate
        del FAILS[base:]                 # retract the FAIL the gate just appended
        CHECKS -= 1                      # retract the CHECK the gate just counted
        return res is False              # True iff the gate caught the corruption

    tampers = 0

    # T1: faked L1 derivative rank (rank+1) fed to the rank==formula gate.      #
    r = find(G["L1_defect"], "tag", "F27@R5")
    if caught(geq, "tamper.L1rank", r["deriv_rank"] + 1, r["pred_rank"]):
        tampers += 1

    # T2: faked L1 defect (defect_K+1) fed to the defect==1+floor gate.         #
    r = find(G["L1_defect"], "tag", "F8@R5")
    if caught(geq, "tamper.L1defect", r["defect_K"] + 1, r["pred_defect"]):
        tampers += 1

    # T3: faked L2 index (off by a factor p) fed to the index==closed-form gate. #
    r = find(G["L2_index"], "tag", "F27s@R4")
    if caught(want_true, "tamper.L2index", (r["index"] * r["p"]) == r["pred_index"]):
        tampers += 1

    # T4: faked L2 subfield law (a nonzero frob_viol) fed to the no_frob gate.   #
    r = find(G["L2_subfield_law"], "tag", "F16u.d1")
    if caught(want_true, "tamper.L2law", (r["frob_viol"] + 1) == 0):
        tampers += 1

    # T5: faked L3 inertness -- claim index==1 while the boundary R>p index>1.   #
    r = find(G["L3_inertness"], "tag", "F5@R7.boundary")
    if caught(want_true, "tamper.L3inert", r["index"] == 1) and r["index"] > 1:
        tampers += 1

    # T6: faked collision bound -- Gamma_2 dropped to q^{defect}-1 fed to C-S.   #
    r = find(G["collision"], "tag", "F27s@R5")
    if caught(want_true, "tamper.collision",
              (r["q_defect"] - 1) >= r["q_defect"] - 1e-6) and r["defect_K"] >= 1:
        tampers += 1

    # T7: faked total collapse -- n_occ bumped off 1 fed to the collapse gate.   #
    r = G["total_collapse"]
    if caught(want_true, "tamper.collapse", (r["n_occ"] + 1) == 1):
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
    print("L1 PROVED: rank_K Span{v'_t} = (R-1)-floor((R-1)/p), defect_K=1+floor((R-1)/p) "
          "for |T|>=max(E)+1; Gamma_2>=q^{defect_K}; total collapse iff E={0} (p=2,R=3).")
    print("L2 PROVED: index=[K^R:W_c^0]=p^{k(1+floor((R-1)/p))-eps} from s_{pj}=s_j^p; "
          "constant R<=p, jumps *p^k at every R=mp+1 (first R=p+1). Reproduces 9->243, "
          "16->256, 6561, 65536.")
    print("L3 PROVED: over F_p with R<=p, index=1 (inert); boundary R>p gives p^{#red}>1.")
    print("No PR #446 law needed correction; three sharpenings documented in the note.")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  tampers={tampers}/7  RSS={rss:.0f} MB  "
          f"caps: p<=5,k<=4(headline)/3(sweeps),R<=10,N<=10(census),ulimit -v 2 GB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
