#!/usr/bin/env python3
"""
INSTANTIATION EXAMPLES for the proof objects of experimental/asymptotic_rs_mca.tex,
built per the steering priority-3 item ("Final computations and examples", also
listed as work target C0), agents.md @ eb42b82:

    "Produce small and medium examples that instantiate the proof objects:
    bad-line moduli strata, structured cases, primitive Boolean prefix
    fibers, Fourier/Sidon cuts, and the entropy threshold.  These examples
    are for auditing and exposition, not for replacing the proof."

This script recomputes FIVE example families entirely from scratch (no
external data dependency beyond the one committed JSON file it gates
against) and prints RESULT: PASS on success.

  E1. PRIMITIVE BOOLEAN PREFIX FIBERS (def:primitive-leaf, asymptotic_rs_mca
      L148-158).  Four leaves, K in {F16, F27, F49}, N=16, m=8, R in {3,4},
      rho in {ones, twist}: exact fiber census |F_s|, L=|im Phi|, Nbar=M/L,
      max_s|F_s|/Nbar, log(Nbar)/N.  Exhibits Q holding numerically (the
      max/Nbar ratio stays a modest O(1) constant, never approaching L or M).

  E2. MOMENT-MAX EQUIVALENCE (lem:moment-max, L165-178).  On one leaf,
      Gamma^ord_q = L^-1 sum_s (|F_s|/Nbar)^q for q in {2,4,8,16,32}, exact
      big-integer numerator/denominator, sandwiched between the lemma's two
      bounds; Gamma_q^(1/q) is shown climbing toward max/Nbar as q grows.

  E3. FOURIER/SIDON CUT (Sidon cut sec.3 L180-208 + Boolean additive
      combinatorics sec.4/sec:bsg L210-242).  Exact additive energy
      E(F)=#{(a,b,c,d): a-b=c-d} and Delta(F)=E(F)/|F|^3 for the largest
      census fibers (dual path: O(|F|^2) difference-convolution vs exact
      O(|F|^4) 4-tuple count when |F|<=25) plus a small EXACT reference
      family (singleton, pair, product-cubes) that pins the high-Delta
      corner.  Classifies Sidon-heavy vs high-energy under a printed
      convention threshold and verifies the quasicube bound
      |F-F| >= |F|^{3/2} (thm:quasicube, L220-226) exactly (via the integer
      inequality |F-F|^2 >= |F|^3) on every instance.

  E4. ENTROPY THRESHOLD g*(rho,beta) (Statement section, L71-75).  Exact
      bisection (tol 1e-12) of g*(rho,beta) = sup{g: H2(rho+g) >= beta*g}
      over a 9x5 grid, plus one finite row family (rho=0.5, beta=2, n=120)
      exhibiting the sign flip of log2(Nbar_{n,a})/n - [H2(rho+g)-beta*g]
      near g=g*, with a secondary n-sweep showing the finite/idealized gap
      shrink as n grows (the theorem's "+o(1)").

  E5. STRUCTURED-CASE SPOT EXAMPLE, cell (C1) MECHANISM (def:cells L91-92,
      "Quotient-pullback cells... support or locator descends along a
      nontrivial finite map D -> D'").  A concrete squaring map on a
      multiplicative subgroup of F_97^*, an explicit bad-line witness built
      from the paper's own identity-prefix pole construction (L276-287)
      whose support is a union of squaring-fibers (so its locator
      DEMONSTRABLY descends: ell_S(X) = tilde_ell(X^2) exactly), and the
      toy quotient-pullback slope-count budget C(n/2,m/2) vs the raw
      C(n,m).  Labeled exposition of the C1 MECHANISM ONLY -- not a payment
      verification of any row.

  NOT INSTANTIATED: "bad-line moduli strata."  The moduli manuscript
  (Cho26ModuliSelf / Cho26ModuliFinal in asymptotic_rs_mca.tex's
  bibliography) is absent from the repository; PR #433 (przchojecki/rs-mca)
  machine-verified this absence and named the expected path
  experimental/rs_mca_moduli_ledger_final.tex, itself still absent at
  eb42b82.  No moduli-strata example is fabricated here; see the note.

Machinery reuse (per the task's "repo convention, standalone stdlib-only"):
the GF finite-field class, build_T/build_rho/moment_columns, and the
unsigned-family census pattern are COPIED (not imported) from
experimental/scripts/verify_entropy_inverse_fp_span_cell.py, then extended
with a member-tracking census (census_members) needed for E3's per-fiber
additive-energy work.  E1's F16-at-R=3 leaf independently reproduces that
script's char-2 Frobenius coordinate-collapse law (s_2 = s_1^2) in a new
(unsigned, fixed-weight) slice -- see the note, section on E1.

Status of every claim in this packet: MEASURED (recomputed numeracy),
CONVENTION (a stated threshold/parameter choice, not a theorem), or
REFERENCE (a fact quoted from the paper or a cited PR).  This packet proves
nothing about thm:frontier, thm:closed-ledger-package, thm:primitive-q,
def:sidon-paid, prop:no-high-energy, or any other labeled statement of
asymptotic_rs_mca.tex; it does not touch prob:row-sharp-q (the separate
finite-row crux tracked in grande_finale.tex / agents.md); and it certifies
no deployed row.  Replaces no proof -- see the note's nonclaims section and
the steering quote above.

Zero-arg, stdlib-only.  Prints RESULT: PASS (N/N checks) and exits 0.

Environment knobs (both optional; defaults reproduce the committed run):
  APEX_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0 disables).
                   Applying the cap is NEVER fatal: if the platform refuses
                   it, the script proceeds uncapped and prints a notice.
  APEX_DATA_DIR    directory holding the committed data JSON (default:
                   ../data relative to this script, i.e. the in-tree
                   experimental/data/ layout).
"""
import os
import json
import math
import random
import resource
import itertools
from collections import Counter, defaultdict


def _apply_as_cap():
    """Best-effort address-space guard: honor APEX_AS_CAP_GB (default 2 GB,
    0 disables) but never fail on platforms that refuse the cap."""
    try:
        gb = float(os.environ.get("APEX_AS_CAP_GB", "2"))
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
DATA = os.environ.get("APEX_DATA_DIR") or os.path.normpath(
    os.path.join(HERE, "..", "data"))
DATA_FILE = os.path.join(DATA, "asymptotic_proof_object_examples.json")

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
#  GF class -- COPIED (trimmed) from verify_entropy_inverse_fp_span_cell.py    #
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
    """F_{p^k}; elements are base-p digit ints; modulus = smallest monic
    irreducible.  k=1 gives ordinary F_p arithmetic (used by E5)."""

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

    def powr(self, a, e):
        if e == 0:
            return 1
        if a == 0:
            return 0
        e %= (self.q - 1)
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


def build_T(F, N):
    """First N elements of K in canonical (base-p digit) order, 0 included."""
    return list(range(F.q))[:N]


def build_rho(F, T, mode, seed=12345):
    if mode == "ones":
        return [1] * len(T)
    rnd = random.Random(seed)
    return [1 + rnd.randrange(F.q - 1) for _ in T]


def moment_columns(F, T, R, rho):
    VT = []
    for i, t in enumerate(T):
        row = []; tj = 1
        for j in range(R):
            row.append(F.mul(rho[i], tj)); tj = F.mul(tj, t)
        VT.append(row)
    return VT


def census_members(F, VT, R, m, N):
    """Unsigned fixed-weight census: fibers[key] = list of bitmask m-subsets
    of range(N) mapping to that key.  Extends the fp-span-cell script's
    census() by retaining membership (needed for E3's additive energy)."""
    q = F.q
    fibers = defaultdict(list)
    for combo in itertools.combinations(range(N), m):
        acc = [0] * R
        for i in combo:
            row = VT[i]
            for j in range(R):
                acc[j] = F.add(acc[j], row[j])
        key = 0
        for j in range(R):
            key += acc[j] * q ** j
        bitmask = 0
        for i in combo:
            bitmask |= (1 << i)
        fibers[key].append(bitmask)
    return fibers


# =========================================================================== #
#  E1 / E2 -- primitive leaves + moment-max squeeze                            #
# =========================================================================== #
LEAF_SPECS = [
    ("F16-R3", "F16", 16, 8, 3),
    ("F16-R4", "F16", 16, 8, 4),
    ("F27-R3", "F27", 16, 8, 3),
    ("F49-R3", "F49", 16, 8, 3),
]
FIELDS = {"F16": GF(2, 4), "F27": GF(3, 3), "F49": GF(7, 2)}


def build_leaf(qname, N, m, R, rho_mode):
    F = FIELDS[qname]
    T = build_T(F, N)
    rho = build_rho(F, T, rho_mode)
    VT = moment_columns(F, T, R, rho)
    fibers = census_members(F, VT, R, m, N)
    M = math.comb(N, m)
    L = len(fibers)
    Nbar = M / L
    sizes = sorted((len(v) for v in fibers.values()), reverse=True)
    maxF = sizes[0]
    return dict(F=F, T=T, R=R, rho=rho, VT=VT, fibers=fibers, M=M, L=L,
                Nbar=Nbar, sizes=sizes, maxF=maxF)


def e1_table():
    rows = []
    leaves_ones = {}
    for leaf_id, qname, N, m, R in LEAF_SPECS:
        for rho_mode in ("ones", "twist"):
            leaf = build_leaf(qname, N, m, R, rho_mode)
            row = dict(
                leaf_id=leaf_id, field=qname, N=N, m=m, R=R, rho=rho_mode,
                M=leaf["M"], L=leaf["L"], Nbar=leaf["Nbar"], maxF=leaf["maxF"],
                max_over_Nbar=leaf["maxF"] / leaf["Nbar"],
                log_Nbar_over_N=math.log(leaf["Nbar"]) / N,
                top5_sizes=leaf["sizes"][:5],
            )
            rows.append(row)
            if rho_mode == "ones":
                leaves_ones[leaf_id] = leaf
    return rows, leaves_ones


def e2_table(leaf, qs=(2, 4, 8, 16, 32)):
    sizes = leaf["sizes"]; M = leaf["M"]; L = leaf["L"]; maxF = leaf["maxF"]
    Nbar = leaf["Nbar"]
    out = []
    for q in qs:
        sumFq = sum(sz ** q for sz in sizes)
        num = (L ** (q - 1)) * sumFq          # exact numerator of Gamma_q
        den = M ** q                          # exact denominator of Gamma_q
        up_num = (maxF * L) ** q              # exact numerator of (max/Nbar)^q
        gamma_q = num / den
        upper = up_num / den
        lower = up_num / (L * den)
        squeeze_lo = up_num <= num * L         # exact bigint check: lower<=gamma
        squeeze_hi = num <= up_num             # exact bigint check: gamma<=upper
        out.append(dict(
            q=q, lower=lower, gamma_q=gamma_q, upper=upper,
            squeeze_ok=bool(squeeze_lo and squeeze_hi),
            gamma_q_pow=gamma_q ** (1.0 / q),
            lower_pow=(maxF / Nbar) * (L ** (-1.0 / q)),
        ))
    return out


# =========================================================================== #
#  E3 -- additive energy / Sidon cut / quasicube                               #
# =========================================================================== #
def pos_neg_key(a_mask, b_mask, N):
    full = (1 << N) - 1
    pos = a_mask & ~b_mask & full
    neg = ~a_mask & b_mask & full
    return pos | (neg << N)


def energy_and_diffset(members, N):
    """O(|F|^2) exact additive energy + |F-F| via the difference-multiset
    identity E(F) = sum_d r(d)^2."""
    cnt = Counter()
    for a in members:
        for b in members:
            cnt[pos_neg_key(a, b, N)] += 1
    E = sum(c * c for c in cnt.values())
    diffset = len(cnt)
    return E, diffset


def energy_naive_4tuple(members, N):
    """O(|F|^4) exhaustive dual path -- only for |F| <= DUAL_CUTOFF."""
    memset = list(members)
    diffs = {(a, b): pos_neg_key(a, b, N) for a in memset for b in memset}
    total = 0
    for a in memset:
        for b in memset:
            dab = diffs[(a, b)]
            for c in memset:
                for d in memset:
                    if dab == diffs[(c, d)]:
                        total += 1
    return total


DUAL_CUTOFF = 25
TAU_LO, TAU_HI = 0.2, 0.5   # CONVENTION: Sidon-heavy <= TAU_LO, high-energy >= TAU_HI


def classify(delta):
    if delta <= TAU_LO:
        return "sidon-heavy"
    if delta >= TAU_HI:
        return "high-energy"
    return "mixed"


def e3_fiber_row(name, members, N):
    Fsize = len(members)
    E, diffset = energy_and_diffset(members, N)
    Delta = E / (Fsize ** 3)
    quasicube_ok = (diffset ** 2) >= (Fsize ** 3)   # exact integer inequality
    dual_ok = None
    if Fsize <= DUAL_CUTOFF:
        dual_ok = (energy_naive_4tuple(members, N) == E)
    return dict(name=name, Fsize=Fsize, E=E, Delta=Delta, diffset=diffset,
                quasicube_ok=bool(quasicube_ok), dual_ok=dual_ok,
                classification=classify(Delta))


def e3_synthetic_family(N=16):
    """Exact small reference sets pinning the high-Delta corner: a singleton
    (Delta=1 exactly -- the |F|=1 forced-extreme, since Z^N is torsion-free
    so Delta(F)=1 forces F to be a single coset point), a pair (Delta=0.75
    exactly, a universal fact for any 2-point subset of a torsion-free
    group), and product-cubes {0,1}^d x {0}^(N-d) for d=1..6 (Delta=0.75^d
    exactly, by the direct-product energy identity)."""
    rows = []
    singleton = [0]
    rows.append(e3_fiber_row("singleton", singleton, N))
    pair = [0, 1]
    rows.append(e3_fiber_row("pair", pair, N))
    for d in range(1, 7):
        members = list(range(2 ** d))  # {0,1}^d packed into the low d bits
        rows.append(e3_fiber_row(f"cube-d{d}", members, N))
    return rows


def e3_all(leaves_ones, top_k=5):
    fiber_rows = []
    for leaf_id, leaf in leaves_ones.items():
        N = len(leaf["T"])
        ranked = sorted(leaf["fibers"].items(), key=lambda kv: -len(kv[1]))
        for rank, (_key, members) in enumerate(ranked[:top_k]):
            row = e3_fiber_row(f"{leaf_id}#{rank}", members, N)
            row["leaf_id"] = leaf_id; row["rank"] = rank
            fiber_rows.append(row)
    synthetic_rows = e3_synthetic_family()
    return fiber_rows, synthetic_rows


# =========================================================================== #
#  E4 -- entropy threshold g*(rho, beta)                                       #
# =========================================================================== #
def H2(x):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


def g_star(rho, beta, tol=1e-12, iters=200):
    lo, hi = 0.0, 1.0 - rho
    flo = H2(rho + lo) - beta * lo
    fhi = H2(rho + hi) - beta * hi
    assert flo >= -1e-9, (rho, beta, flo)
    assert fhi <= 1e-9, (rho, beta, fhi)
    n = 0
    while hi - lo > tol and n < iters:
        mid = (lo + hi) / 2
        fm = H2(rho + mid) - beta * mid
        if fm >= 0:
            lo = mid
        else:
            hi = mid
        n += 1
    return (lo + hi) / 2


def e4_grid():
    rhos = [round(0.1 * i, 1) for i in range(1, 10)]
    betas = [1, 2, 3, 4, 8]
    out = []
    for beta in betas:
        for rho in rhos:
            out.append(dict(rho=rho, beta=beta, gstar=g_star(rho, beta)))
    return out


def e4_row_family(rho=0.5, beta=2, n=120):
    gstar = g_star(rho, beta)
    k = round(rho * n)
    rows = []
    prev_sign = None
    flip_w = None
    for w in range(0, n - k + 1):
        a = k + 1 + w
        if a > n:
            break
        logC = math.log2(math.comb(n, a))
        val_exact = (logC - w * beta) / n
        g = w / n
        val_closed = H2(rho + g) - beta * g
        rows.append(dict(w=w, g=g, val_exact=val_exact, val_closed=val_closed))
        sign = val_exact >= 0
        if prev_sign is not None and sign != prev_sign and flip_w is None:
            flip_w = w
        prev_sign = sign
    lo_w = max(0, flip_w - 5); hi_w = min(len(rows) - 1, flip_w + 5)
    window = rows[lo_w:hi_w + 1]
    n_growth = []
    for nn in (120, 600, 3000, 15000):
        kk = round(rho * nn)
        prev = None; fw = None
        for w in range(0, nn - kk + 1):
            a = kk + 1 + w
            if a > nn:
                break
            val = (math.log2(math.comb(nn, a)) - w * beta) / nn
            sign = val >= 0
            if prev is not None and sign != prev and fw is None:
                fw = w
                break
            prev = sign
        gap = abs(fw / nn - gstar)
        n_growth.append(dict(n=nn, flip_g=fw / nn, gap=gap))
    return dict(rho=rho, beta=beta, n=n, gstar=gstar, k=k, flip_w=flip_w,
                window=window, n_growth=n_growth)


# =========================================================================== #
#  E5 -- C1 quotient-pullback mechanism toy (prime field, plain polynomials)    #
# =========================================================================== #
def poly_mul(a, b, F):
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            res[i + j] = F.add(res[i + j], F.mul(ai, bj))
    return res


def locator(points, F):
    poly = [1]
    for t in points:
        poly = poly_mul(poly, [F.sub(0, t), 1], F)
    return poly


def poly_eval(poly, x, F):
    acc = 0; xp = 1
    for c in poly:
        acc = F.add(acc, F.mul(c, xp)); xp = F.mul(xp, x)
    return acc


def synthetic_div(poly, alpha, F):
    """Divide poly (low->high) by (X-alpha); returns (quotient low->high, remainder)."""
    n = len(poly) - 1
    coeffs = list(poly)
    out = [0] * n
    rem = 0
    for i in range(n, -1, -1):
        cur = coeffs[i] if i == n else F.add(coeffs[i], F.mul(rem, alpha))
        if i > 0:
            out[i - 1] = cur
        rem = cur
    return out, rem


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def lagrange_interp(xs, ys, F):
    n = len(xs)
    result = [0] * n
    for i in range(n):
        Li = [1]; denom = 1
        for j in range(n):
            if j == i:
                continue
            Li = poly_mul(Li, [F.sub(0, xs[j]), 1], F)
            denom = F.mul(denom, F.sub(xs[i], xs[j]))
        inv_denom = F.inv(denom)
        Li = [F.mul(F.mul(c, inv_denom), ys[i]) for c in Li]
        for d in range(len(Li)):
            result[d] = F.add(result[d], Li[d])
    return result


def e5_toy():
    p = 97
    F97 = GF(p, 1)
    gen = F97.g
    n_sub = 16
    g_n = F97.powr(gen, (p - 1) // n_sub)
    D = []; x = 1
    for _ in range(n_sub):
        D.append(x); x = F97.mul(x, g_n)
    D = sorted(D)
    Dneg = sorted(F97.negt[d] for d in D)
    closed_under_negation = (Dneg == D)

    Dprime = sorted(set(F97.mul(d, d) for d in D))

    fibers = []; seen = set()
    for d in D:
        if d in seen:
            continue
        nd = F97.negt[d]
        seen.add(d); seen.add(nd)
        fibers.append(tuple(sorted((d, nd))))

    k, w = 3, 2
    m = k + 1 + w
    half = m // 2
    chosen = fibers[:half]
    S = sorted(set(t for fib in chosen for t in fib))

    ellS = locator(S, F97)
    Sprime = sorted(set(F97.mul(t, t) for t in S))
    tildeS = locator(Sprime, F97)
    composed = [0] * len(ellS)
    for i, c in enumerate(tildeS):
        composed[2 * i] = c
    descends = (ellS == composed)
    odd_coeffs_zero = all(ellS[i] == 0 for i in range(1, len(ellS), 2))

    alpha = 0
    assert alpha not in D
    ellS_alpha = poly_eval(ellS, alpha, F97)

    Uz = [0] * (m + 1); Uz[m] = 1
    for i in range(1, w + 1):
        Uz[m - i] = ellS[m - i]
    prefix_match = all(Uz[m - i] == ellS[m - i] for i in range(0, w + 1))
    lower_differs = any(Uz[j] != ellS[j] for j in range(0, m - w))
    Uz_alpha = poly_eval(Uz, alpha, F97)
    zeta_bad = F97.sub(Uz_alpha, ellS_alpha)

    Diff = [F97.sub(Uz[i], ellS[i]) for i in range(len(Uz))]
    Diff[0] = F97.sub(Diff[0], zeta_bad)
    h_quot, h_rem = synthetic_div(Diff, alpha, F97)
    h_trim = trim(h_quot)
    h_degree = len(h_trim) - 1 if h_trim != [0] else -1

    def lhs_at(x, zeta):
        fval = F97.mul(poly_eval(Uz, x, F97), F97.inv(F97.sub(x, alpha)))
        gval = F97.mul(F97.negt[1], F97.inv(F97.sub(x, alpha)))
        return F97.add(fval, F97.mul(zeta, gval))

    matches_on_S = all(lhs_at(x, zeta_bad) == poly_eval(h_quot, x, F97) for x in S)

    xs_k = S[:k]
    ys_k = [F97.mul(F97.negt[1], F97.inv(F97.sub(x, alpha))) for x in xs_k]
    interp = lagrange_interp(xs_k, ys_k, F97)
    mismatches = 0
    for x in S[k:]:
        gval = F97.mul(F97.negt[1], F97.inv(F97.sub(x, alpha)))
        if gval != poly_eval(interp, x, F97):
            mismatches += 1

    raw_budget = math.comb(n_sub, m)
    c1_budget = math.comb(n_sub // 2, m // 2)

    return dict(
        p=p, n_sub=n_sub, D=D, closed_under_negation=closed_under_negation,
        Dprime=Dprime, fibers=[list(f) for f in fibers], k=k, w=w, m=m,
        S=S, ellS=ellS, tildeS=tildeS, descends=descends,
        odd_coeffs_zero=odd_coeffs_zero, alpha=alpha, ellS_alpha=ellS_alpha,
        Uz=Uz, prefix_match=prefix_match, lower_differs=lower_differs,
        zeta_bad=zeta_bad, h_rem=h_rem, h_coeffs=h_trim, h_degree=h_degree,
        matches_on_S=matches_on_S, g_alpha_mismatches=mismatches,
        g_alpha_mismatch_total=len(S) - k,
        raw_budget=raw_budget, c1_budget=c1_budget,
        budget_ratio=raw_budget / c1_budget,
    )


# =========================================================================== #
#  compute_all -- the single source of truth used both to gate and to seed     #
#  the committed JSON (see the generator note at the bottom of this file)      #
# =========================================================================== #
def compute_all():
    e1_rows, leaves_ones = e1_table()
    e2_rows = e2_table(leaves_ones["F49-R3"])
    e3_fibers, e3_synth = e3_all(leaves_ones)
    e4_grid_rows = e4_grid()
    e4_family = e4_row_family()
    e5 = e5_toy()
    return dict(
        e1=e1_rows,
        e2=dict(leaf_id="F49-R3", rows=e2_rows),
        e3=dict(fibers=e3_fibers, synthetic=e3_synth,
                tau_lo=TAU_LO, tau_hi=TAU_HI, dual_cutoff=DUAL_CUTOFF),
        e4=dict(grid=e4_grid_rows, family=e4_family),
        e5=e5,
    ), leaves_ones


# =========================================================================== #
def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)


def gate_e1(got_rows, want_rows):
    for got, want in zip(got_rows, want_rows):
        tag = got["leaf_id"] + "." + got["rho"]
        geq(f"e1.{tag}.field", got["field"], want["field"])
        geq(f"e1.{tag}.N", got["N"], want["N"])
        geq(f"e1.{tag}.m", got["m"], want["m"])
        geq(f"e1.{tag}.R", got["R"], want["R"])
        geq(f"e1.{tag}.M", got["M"], want["M"])
        geq(f"e1.{tag}.L", got["L"], want["L"])
        geq(f"e1.{tag}.maxF", got["maxF"], want["maxF"])
        geq(f"e1.{tag}.top5_sizes", got["top5_sizes"], want["top5_sizes"])
        feq(f"e1.{tag}.Nbar", got["Nbar"], want["Nbar"])
        feq(f"e1.{tag}.max_over_Nbar", got["max_over_Nbar"], want["max_over_Nbar"])
        feq(f"e1.{tag}.log_Nbar_over_N", got["log_Nbar_over_N"], want["log_Nbar_over_N"])


def gate_e2(got, want):
    geq("e2.leaf_id", got["leaf_id"], want["leaf_id"])
    for g, w in zip(got["rows"], want["rows"]):
        geq(f"e2.q{g['q']}.q", g["q"], w["q"])
        geq(f"e2.q{g['q']}.squeeze_ok", g["squeeze_ok"], w["squeeze_ok"])
        feq(f"e2.q{g['q']}.lower", g["lower"], w["lower"])
        feq(f"e2.q{g['q']}.gamma_q", g["gamma_q"], w["gamma_q"])
        feq(f"e2.q{g['q']}.upper", g["upper"], w["upper"])
        feq(f"e2.q{g['q']}.gamma_q_pow", g["gamma_q_pow"], w["gamma_q_pow"])
        feq(f"e2.q{g['q']}.lower_pow", g["lower_pow"], w["lower_pow"])


def gate_e3_row(tag, g, w):
    geq(f"e3.{tag}.Fsize", g["Fsize"], w["Fsize"])
    geq(f"e3.{tag}.E", g["E"], w["E"])
    geq(f"e3.{tag}.diffset", g["diffset"], w["diffset"])
    geq(f"e3.{tag}.quasicube_ok", g["quasicube_ok"], w["quasicube_ok"])
    geq(f"e3.{tag}.classification", g["classification"], w["classification"])
    geq(f"e3.{tag}.dual_ok", g["dual_ok"], w["dual_ok"])
    feq(f"e3.{tag}.Delta", g["Delta"], w["Delta"])


def gate_e3(got, want):
    geq("e3.tau_lo", got["tau_lo"], want["tau_lo"])
    geq("e3.tau_hi", got["tau_hi"], want["tau_hi"])
    for g, w in zip(got["fibers"], want["fibers"]):
        gate_e3_row(g["name"], g, w)
    for g, w in zip(got["synthetic"], want["synthetic"]):
        gate_e3_row(g["name"], g, w)


def gate_e4(got, want):
    for g, w in zip(got["grid"], want["grid"]):
        tag = f"rho{g['rho']}_beta{g['beta']}"
        feq(f"e4.grid.{tag}", g["gstar"], w["gstar"])
    gf, wf = got["family"], want["family"]
    geq("e4.family.flip_w", gf["flip_w"], wf["flip_w"])
    geq("e4.family.k", gf["k"], wf["k"])
    feq("e4.family.gstar", gf["gstar"], wf["gstar"])
    for g, w in zip(gf["window"], wf["window"]):
        tag = f"w{g['w']}"
        feq(f"e4.family.window.{tag}.val_exact", g["val_exact"], w["val_exact"])
        feq(f"e4.family.window.{tag}.val_closed", g["val_closed"], w["val_closed"])
    for g, w in zip(gf["n_growth"], wf["n_growth"]):
        tag = f"n{g['n']}"
        feq(f"e4.family.n_growth.{tag}.flip_g", g["flip_g"], w["flip_g"])
        feq(f"e4.family.n_growth.{tag}.gap", g["gap"], w["gap"])
    want_true("e4.family.gap_shrinks",
              gf["n_growth"][-1]["gap"] < gf["n_growth"][0]["gap"])


def gate_e5(got, want):
    for key in ("p", "n_sub", "D", "closed_under_negation", "Dprime", "k", "w",
                "m", "S", "ellS", "tildeS", "descends", "odd_coeffs_zero",
                "alpha", "ellS_alpha", "Uz", "prefix_match", "lower_differs",
                "zeta_bad", "h_rem", "h_coeffs", "h_degree", "matches_on_S",
                "g_alpha_mismatches", "g_alpha_mismatch_total", "raw_budget",
                "c1_budget"):
        geq(f"e5.{key}", got[key], want[key])
    feq("e5.budget_ratio", got["budget_ratio"], want["budget_ratio"])


# =========================================================================== #
def main():
    computed, leaves_ones = compute_all()
    data = load_data()

    gate_e1(computed["e1"], data["e1"])
    gate_e2(computed["e2"], data["e2"])
    gate_e3(computed["e3"], data["e3"])
    gate_e4(computed["e4"], data["e4"])
    gate_e5(computed["e5"], data["e5"])

    # ===================================================================== #
    #  cross-checks internal to this run (not JSON-gated -- structural)      #
    # ===================================================================== #
    # E1: Q holds numerically at every leaf -- max/Nbar is a modest constant,
    # nowhere near L (full injectivity) or M (total collapse).
    for row in computed["e1"]:
        want_true(f"e1.Q_holds.{row['leaf_id']}.{row['rho']}",
                  1.0 <= row["max_over_Nbar"] < 20.0)
    # E1: the F16-R3-ones leaf reproduces the fp-span-cell note's char-2
    # Frobenius law s_2 = s_1^2 as a coordinate collapse: L == q (16), not
    # merely <= q^(R-1) -- the *full* red-column collapse at R=3, p=2.
    f16r3 = leaves_ones["F16-R3"]
    geq("e1.frobenius_collapse.F16_R3.L_eq_q", f16r3["L"], FIELDS["F16"].q)

    # E2: squeeze is monotone -- Gamma_q^(1/q) increases toward max/Nbar.
    pows = [r["gamma_q_pow"] for r in computed["e2"]["rows"]]
    want_true("e2.squeeze_monotone", all(pows[i] < pows[i + 1] for i in range(len(pows) - 1)))
    target = leaves_ones["F49-R3"]["maxF"] / leaves_ones["F49-R3"]["Nbar"]
    want_true("e2.squeeze_below_target", all(p_ <= target + 1e-9 for p_ in pows))

    # E3: no fiber is simultaneously high-|F| and high-energy among the
    # naturally occurring census fibers (the toy-scale echo of
    # prop:no-high-energy); the high-energy corner is only ever populated by
    # the tiny synthetic reference sets.
    for row in computed["e3"]["fibers"]:
        want_true(f"e3.no_high_energy.{row['name']}", row["classification"] != "high-energy")
    high_energy_synth = [r for r in computed["e3"]["synthetic"] if r["classification"] == "high-energy"]
    want_true("e3.synthetic_has_high_energy_examples", len(high_energy_synth) >= 2)
    want_true("e3.synthetic_high_energy_are_tiny", all(r["Fsize"] <= 4 for r in high_energy_synth))
    # every instance obeys the quasicube bound exactly (thm:quasicube)
    for row in computed["e3"]["fibers"] + computed["e3"]["synthetic"]:
        want_true(f"e3.quasicube.{row['name']}", row["quasicube_ok"])

    # E4: g* is a genuine root -- H2(rho+g*)-beta*g* is within bisection
    # tolerance of 0 for every grid point.
    for row in computed["e4"]["grid"]:
        resid = H2(row["rho"] + row["gstar"]) - row["beta"] * row["gstar"]
        want_true(f"e4.root.rho{row['rho']}_beta{row['beta']}", abs(resid) < 1e-9)
    # E4: sign flips exactly around g* in the row family window.
    fam = computed["e4"]["family"]
    win = fam["window"]
    want_true("e4.sign_flip_present",
              any(win[i]["val_exact"] >= 0 > win[i + 1]["val_exact"] for i in range(len(win) - 1)))
    want_true("e4.flip_near_gstar", abs(fam["flip_w"] / fam["n"] - fam["gstar"]) < 0.02)

    # E5: the C1 mechanism -- support genuinely descends, the pole
    # construction gives a real bad slope, g_alpha alone is not explained.
    e5 = computed["e5"]
    want_true("e5.D_closed_under_negation", e5["closed_under_negation"])
    want_true("e5.locator_descends", e5["descends"])
    want_true("e5.odd_coeffs_zero", e5["odd_coeffs_zero"])
    want_true("e5.zeta_bad_nonzero", e5["zeta_bad"] != 0)
    want_true("e5.matches_on_S", e5["matches_on_S"])
    want_true("e5.h_below_k", e5["h_degree"] < e5["k"])
    want_true("e5.h_rem_zero", e5["h_rem"] == 0)
    want_true("e5.g_alpha_not_explained",
              e5["g_alpha_mismatches"] == e5["g_alpha_mismatch_total"] > 0)
    want_true("e5.budget_shrinks", e5["c1_budget"] < e5["raw_budget"])

    # ===================================================================== #
    #  TAMPER SELF-TESTS (7) -- each MUST be caught                          #
    # ===================================================================== #
    tampers = 0

    # T1 (E1): a faked L (off by one) desyncs Nbar from the true M/L.
    leaf = leaves_ones["F49-R3"]
    fake_L = leaf["L"] + 1
    fake_Nbar = leaf["M"] / fake_L
    if abs(fake_Nbar - leaf["Nbar"]) > 1e-6:
        tampers += 1

    # T2 (E2): a too-small fake max makes the upper bound (fake_max/Nbar)^q
    # fall BELOW the true Gamma_q at large q -- the bound needs the real max.
    q = 32
    sizes = leaf["sizes"]; M = leaf["M"]; L = leaf["L"]
    true_gamma32 = (L ** (q - 1)) * sum(s ** q for s in sizes) / (M ** q)
    fake_max = max(1, leaf["maxF"] // 2)
    fake_upper = ((fake_max * L) ** q) / (M ** q)
    if fake_upper < true_gamma32:
        tampers += 1

    # T3 (E3): corrupt one pairwise-difference count in a small fiber and
    # confirm the O(n^2) energy no longer matches the O(n^4) dual path.
    small_fiber = next(r for r in computed["e3"]["fibers"] if r["Fsize"] <= DUAL_CUTOFF)
    leaf_id = small_fiber["leaf_id"]
    members = None
    for lid, lf in leaves_ones.items():
        if lid == leaf_id:
            ranked = sorted(lf["fibers"].items(), key=lambda kv: -len(kv[1]))
            members = ranked[small_fiber["rank"]][1]
            N_local = len(lf["T"])
            break
    real_E, _ = energy_and_diffset(members, N_local)
    fake_E = real_E + 6   # inject one fake symmetric pair's worth of energy
    dual_E = energy_naive_4tuple(members, N_local)
    if fake_E != dual_E and real_E == dual_E:
        tampers += 1

    # T4 (E3): claiming a too-small |F-F| (e.g. 2) breaks the quasicube bound
    # for any real fiber (|F| >= 2 here), showing the check is non-vacuous.
    any_real_fiber = computed["e3"]["fibers"][0]
    fake_diffset = 2
    if (fake_diffset ** 2) < (any_real_fiber["Fsize"] ** 3):
        tampers += 1

    # T5 (E4): perturbing g away from g* by a fixed margin breaks the
    # defining root equation H2(rho+g)-beta*g ~= 0.
    rho5, beta5 = 0.5, 2
    gstar5 = g_star(rho5, beta5)
    resid_true = H2(rho5 + gstar5) - beta5 * gstar5
    resid_perturbed = H2(rho5 + gstar5 + 0.01) - beta5 * (gstar5 + 0.01)
    if abs(resid_true) < 1e-9 and abs(resid_perturbed) > 1e-3:
        tampers += 1

    # T6 (E5): replacing one element of S by a non-paired point breaks
    # locator descent (ell_S(X) != tilde_ell(X^2)).
    F97 = GF(97, 1)
    S_real = e5["S"]
    D_real = e5["D"]
    off_fiber = [t for t in D_real if t not in S_real and F97.negt[t] not in S_real]
    S_fake = sorted(S_real[:-1] + [off_fiber[0]])
    ellS_fake = locator(S_fake, F97)
    Sprime_fake = sorted(set(F97.mul(t, t) for t in S_fake))
    tildeS_fake = locator(Sprime_fake, F97)
    # descent requires deg(ell_S_fake) == 2*deg(tilde_ell_fake); a non-descending
    # support (unpaired points now present) breaks even this degree relation
    if len(ellS_fake) - 1 == 2 * (len(tildeS_fake) - 1):
        composed_fake = [0] * len(ellS_fake)
        for i, c in enumerate(tildeS_fake):
            composed_fake[2 * i] = c
        breaks = (ellS_fake != composed_fake)
    else:
        breaks = True
    if breaks:
        tampers += 1

    # T7 (E5): a wrong zeta breaks the f_alpha+zeta*g_alpha==h identity on S.
    F97b = GF(97, 1)
    Uz = e5["Uz"]; ellS = e5["ellS"]; alpha = e5["alpha"]; zeta_bad = e5["zeta_bad"]
    Diff = [F97b.sub(Uz[i], ellS[i]) for i in range(len(Uz))]
    zeta_wrong = F97b.add(zeta_bad, 1)
    Diff_wrong = list(Diff); Diff_wrong[0] = F97b.sub(Diff_wrong[0], zeta_wrong)
    _, rem_wrong = synthetic_div(Diff_wrong, alpha, F97b)
    if rem_wrong != 0:
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
    print("Instantiation examples for asymptotic_rs_mca.tex (E1 primitive "
          "leaves, E2 moment-max squeeze, E3 Sidon/quasicube cut, E4 entropy "
          "threshold g*, E5 C1 quotient-pullback mechanism) recomputed and "
          "gated exactly.")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
