#!/usr/bin/env python3
"""
RESIDUAL CONTROLS for the F_p-span cell of the primitive entropic inverse atom
prob:entropy-inverse-q (experimental/grande_finale.tex L827-870).

This is a follow-on measurement to
experimental/notes/thresholds/cap25_v13_entropy_inverse_fp_span_cell.md (PR
#422, fetched read-only from branch thresholds-entropy-inverse-fp-span-cell,
not yet merged at HEAD of this branch), which identified the F_p-span cell
and left three CHEAP measurement items on its Section 6 OPEN list. This
script answers those three:

  M1  q=121/q=125 thin-alphabet-residual replication.  #422 Section 4 reports
      a bounded "thin-alphabet residual" conditional excess with an N-sweep
      1.05->1.16->1.40->1.44->1.37 (N=8..16), peaking near balance.  ITS
      GENERATING CODE IS NOT IN THE REPO on any branch (confirmed by
      full-history grep; only the OUTPUT survives in
      cap25_v13_entropy_inverse_fp_span_cell_nulls.json's "thin_alphabet"
      block).  This script therefore does not attempt bit-for-bit replication.
      Instead it reconstructs the concept precisely from #422's own EXACT,
      already-gated `exc_cond` statistic (law_check, copied verbatim below):
      swept over N at each field's own near-balance R (#422's own per-field
      convention -- S27 used R=4 near its R*=3.94, U16 used R=3 near its
      R*=3.16), the sweep separates into two regimes by whether that
      near-balance R leaves any Frobenius-reducible ("red") column at all
      (#red = floor((R-1)/p)): when R-1>=p there is a red column and the
      established mechanism (image=W_c exactly) pins exc_cond ~ 1; when
      R-1<p there is NO red column, the coord-0 head law alone survives (a
      genuinely "thin" p-element sub-alphabet of the q-element field), and a
      bounded but non-trivial residual excess appears.  This IS the natural
      reading of "thin-alphabet residual", reconstructed and gated here, not
      invented: it is realized at p=7 (F49), and this script measures whether
      it is ALSO realized at the two new, larger primes p=11 (F121, q=121)
      and p=5 (F125, q=125) -- i.e. whether the R-1<p residual corner is
      intrinsic across characteristics or a p in {2,3,7} coincidence.

  M2  Full-alphabet p=7 control: T = ALL of F_7^x (N=6, the full prime field
      unit group), K=F_7 itself (k=1).  Per #422 Section 7's own nonclaim,
      the F_p-span cell is DEFINITIONALLY ABSENT at a prime field (F_p-span
      IS the K-span).  This is a negative control validating that immunity
      argument at an actual toy: dim_Fp(V_T) must equal rank_K(V_T) exactly,
      the predicted coset W_c must equal the FULL ambient (index=1 exactly,
      not merely close to 1), and excess_generic must sit near 1 (no
      structural inflation).  Also relevant: cor:large-characteristic-fourier-
      examples (experimental/grande_finale.tex L949-960), the atom's own
      T=E=F_p Fourier-flat corollary for this exact prime-field regime.

  M3  Two-field-reading confirmation (repair (A) of #422 Section 3):
      instantiate the point-field E (where the moment columns live, |E|>=N)
      vs. the base field B (the O(1)-size field used ONLY in the
      normalization bookkeeping, |B|=p) as two literally different symbols.
      Sweeping R on one field (F16, q=16=2^4) shows the (B)-reading balance
      (offset_over_N, using log|K|=log q) and the (A)-reading balance
      (offset_A_over_N, using log|B|=log p) cross zero at DIFFERENT R (R~3-4
      vs R~12-13, a factor near k=4, exactly as repair (A) implies), and the
      exact span-cell index/exc_cond machinery is recomputed AT the
      (A)-balance R to confirm the index inflation survives there too.

This script COPIES (per repo convention: standalone stdlib-only scripts, no
cross-imports) the finite-field GF class, build_T, build_rho, moment_columns,
census, gamma2, exp_g2_rand, fp_span_dim, rank_fq, decode, frob_free_red,
generic_cols, and gamma2_generic verbatim from
experimental/scripts/verify_entropy_inverse_fp_span_cell.py (PR #422), and
EXTENDS its law_check with two new fields (offset_A_bits, offset_A_over_N --
the repair-(A) bookkeeping of M3) that do not change any previously-gated
quantity.

This is a MEASUREMENT-ONLY packet, asymptotic lane, no finite claims (see the
note's Section 6 nonclaims). Zero-arg, stdlib-only. Prints
RESULT: PASS (N/N checks) and exits 0.

Environment knobs (both optional; defaults reproduce the committed run):
  FP_RESID_AS_CAP_GB   best-effort RLIMIT_AS guard in GB (default 2; 0
                        disables). Applying the cap is NEVER fatal: if the
                        platform refuses it, the script proceeds uncapped and
                        prints a notice.
  FP_RESID_DATA_DIR    directory holding the committed data JSON (default:
                        ../data relative to this script, i.e. the in-tree
                        experimental/data/ layout).

Note: experimental/notes/thresholds/cap25_v13_entropy_inverse_span_residual_controls.md
Data: experimental/data/cap25_v13_entropy_inverse_span_residual_controls.json

Claim labels mirror the note:
  MEASURED     every exc_cond / offset / index / dim number recomputed here.
  CONVENTION   the near-balance-R-per-field choice, the R-1<p thin-alphabet
               split, the (A)-reading offset formula, excess_generic.
  AUDIT        the confirmed absence of #422's own thin-alphabet-residual
               source code, and the honest scoping of what M1 is and is not.
"""
import os
import json
import math
import random
import resource
import itertools
from collections import Counter


def _apply_as_cap():
    """Best-effort address-space guard: honor FP_RESID_AS_CAP_GB (default
    2 GB, 0 disables) but never fail on platforms that refuse the cap."""
    try:
        gb = float(os.environ.get("FP_RESID_AS_CAP_GB", "2"))
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
DATA = os.environ.get("FP_RESID_DATA_DIR") or os.path.normpath(
    os.path.join(HERE, "..", "data"))
PREFIX = "cap25_v13_entropy_inverse_span_residual_controls"

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


# =========================================================================== #
#  datum builders + moment-curve census -- copied verbatim from #422           #
# =========================================================================== #
def build_T(F, N):
    return list(range(1, F.q))[:N]


def build_rho(F, T, mode, seed=12345):
    if mode == "ones":
        return [1] * len(T)
    rnd = random.Random(seed)
    if mode == "proj":
        return [F.mul(F.g, 1 + rnd.randrange(F.p - 1)) for _ in T]
    return [1 + rnd.randrange(F.q - 1) for _ in T]


def moment_columns(F, T, R, rho):
    VT = []
    for i, t in enumerate(T):
        row = []; tj = 1
        for j in range(R):
            row.append(F.mul(rho[i], tj)); tj = F.mul(tj, t)
        VT.append(row)
    return VT


def census(F, VT, R, family, signed):
    q = F.q; counts = Counter(); C = 0
    if not signed:
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
#  law_check -- copied from #422, EXTENDED here with the (A)-reading offset    #
#  (offset_A_bits, offset_A_over_N: repair (A) of #422 Section 3, |B|=p        #
#  instead of |K|=q; M3's own bookkeeping, does not alter any prior field)     #
# =========================================================================== #
def law_check(F, T, a, signed, R, rho_mode):
    p, q, k = F.p, F.q, F.k
    N = len(T)
    rho = build_rho(F, T, rho_mode)
    VT = moment_columns(F, T, R, rho)
    fam = lambda: itertools.combinations(range(N), a)
    counts, C = census(F, VT, R, fam, signed)
    size = q ** R
    free, red = frob_free_red(p, R)
    c = 1
    c_inv = F.inv(c)
    c_1mp = F.mul(c, F.inv(F.powr(c, p)))            # c^(1-p), c=1 here => 1
    law0 = lawp = 0
    a_const = (a % p) if ((not signed or p == 2)) else None
    for key in counts:
        s = decode(key, q, R)
        y0 = F.mul(c_inv, s[0])
        if y0 >= p or (a_const is not None and y0 != a_const):
            law0 += 1
        for j in range(1, R):
            if p * j < R and s[p * j] != F.mul(c_1mp, F.powr(s[j], p)):
                lawp += 1
    c0 = 1 if a_const is not None else p
    pred_W = c0 * (q ** len(free))
    sumN2 = sum(cc * cc for cc in counts.values())
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
                offset_A_bits=math.log2(C) - R * math.log2(p),
                offset_A_over_N=(math.log2(C) - R * math.log2(p)) / N,
                dim_span_Fp=dim, ambient_Fp=R * k,
                K_rank=rank_fq(F, VT), K_rank_full=min(N, R))


# =========================================================================== #
def load(name):
    with open(os.path.join(DATA, f"{PREFIX}.json")) as f:
        d = json.load(f)
    return d[name]


def find(rows, key, val):
    for r in rows:
        if r.get(key) == val:
            return r
    raise KeyError(val)


def gate_sweep_row(tag, got, want):
    feq(f"{tag}.exc_cond", got["exc_cond"], want["exc_cond"])
    feq(f"{tag}.offset_over_N", got["offset_over_N"], want["offset_over_N"])
    geq(f"{tag}.index", got["index"], want["index"])
    geq(f"{tag}.red", got["red"], want["red"])
    geq(f"{tag}.n_occ", got["n_occ"], want["n_occ"])
    geq(f"{tag}.C", got["C"], want["C"])


# =========================================================================== #
def main():
    # ===================================================================== #
    #  M1 -- thin-alphabet residual replication at q=121, q=125             #
    # ===================================================================== #
    Wm1 = load("M1_thin_alphabet_sweep")
    fields = {
        "F16": (GF(2, 4), 3), "F27": (GF(3, 3), 4), "F49": (GF(7, 2), 3),
        "F121": (GF(11, 2), 3), "F125": (GF(5, 3), 3),
    }
    full_N = {"F16": [8, 10, 12, 14], "F27": [14], "F49": [8, 10, 12, 14],
              "F121": [8, 10, 12, 14, 16], "F125": [8, 10, 12, 14, 16]}

    m1_results = {}
    for name, (F, R) in fields.items():
        rows = []
        for N in full_N[name]:
            a = N // 2
            T = build_T(F, N)
            res = law_check(F, T, a, True, R, "ones")
            tag = f"M1|{name}|R{R}|N{N}"
            gate_sweep_row(tag, res, find(Wm1["rows"], "tag", tag))
            rows.append(res)
        m1_results[name] = rows

    # thin-alphabet split: F49/F121/F125's near-balance R leaves NO red
    # column (R-1 < p); F16/F27's near-balance R DOES (the established,
    # already-gated-by-#422 mechanism).  This is the exact criterion #422
    # Section 2.3 states: floor((R-1)/p).
    for name in ("F49", "F121", "F125"):
        F, R = fields[name]
        want_true(f"M1.{name}.thin_regime_no_red", (R - 1) // F.p == 0)
        for res in m1_results[name]:
            geq(f"M1.{name}.red_empty", res["red"], [])
    for name in ("F16", "F27"):
        F, R = fields[name]
        want_true(f"M1.{name}.has_red_column", (R - 1) // F.p >= 1)
        for res in m1_results[name]:
            want_true(f"M1.{name}.red_nonempty", len(res["red"]) >= 1)

    # the has-red baseline pins exc_cond near 1 (the established mechanism,
    # #422 Section 2.2: "conditioning on W removes ALL the excess") -- gate
    # this holds throughout the guard-passing region for both baseline fields
    for name in ("F16", "F27"):
        for res in m1_results[name]:
            want_true(f"M1.{name}.N{res['N']}.baseline_near_one",
                      0.85 < res["exc_cond"] < 1.15)

    # cross-check against #422's OWN literal published, already-gated number:
    # F27 N=14 R=4 signed a=7 rho=ones must equal S27's exc_cond EXACTLY --
    # this validates this script's law_check is a faithful continuation of
    # #422's methodology, independent of the thin-alphabet reconstruction.
    s27_crosscheck = find(m1_results["F27"], "N", 14)
    feq("M1.F27.crosscheck_vs_422_S27_exc_cond", s27_crosscheck["exc_cond"],
        Wm1["crosscheck_422_S27_exc_cond"])
    geq("M1.F27.crosscheck_vs_422_S27_index", s27_crosscheck["index"],
        Wm1["crosscheck_422_S27_index"])

    # the thin-regime residual is BOUNDED within the tested range (nowhere
    # near the >100x main-mechanism scale) at all three thin primes,
    # including the two new ones -- the headline M1 measurement.
    for name in ("F49", "F121", "F125"):
        for res in m1_results[name]:
            want_true(f"M1.{name}.N{res['N']}.bounded_not_exponential",
                      res["exc_cond"] < 20.0)
    # and it is NOT simply ~1 (i.e. a genuine residual, not noise) at the
    # guard-passing (at-balance) points -- the phenomenon is real, not absent
    for name in ("F49", "F121", "F125"):
        at_balance = [r for r in m1_results[name] if r["offset_over_N"] > -0.25]
        want_true(f"M1.{name}.has_guard_passing_point", len(at_balance) >= 1)
        want_true(f"M1.{name}.residual_exceeds_baseline_band",
                  max(r["exc_cond"] for r in at_balance) > 1.15)

    # ===================================================================== #
    #  M2 -- full-alphabet p=7 control: T = F_7^x, K=F_7 prime field         #
    # ===================================================================== #
    Wm2 = load("M2_prime_field_control")
    F7 = GF(7, 1)
    geq("M2.field.q", F7.q, 7)
    geq("M2.field.k", F7.k, 1)
    T7 = build_T(F7, 6)
    geq("M2.T_is_full_Fp_star", sorted(T7), list(range(1, 7)))
    m2 = law_check(F7, T7, 3, True, 3, "ones")

    geq("M2.law0_violations", m2["law0_violations"], Wm2["law0_violations"])
    geq("M2.lawp_violations", m2["lawp_violations"], Wm2["lawp_violations"])
    want_true("M2.coord0_collapse_trivial", m2["law0_violations"] == 0)

    # the definitional-absence claim: F_p-span dim EXACTLY equals K-rank
    # (k=1 means "unrolling to F_p" is the identity on K^R) -- and BOTH are
    # FULL (ambient_Fp = K_rank_full), i.e. no deficiency of either kind
    geq("M2.dim_span_Fp", m2["dim_span_Fp"], Wm2["dim_span_Fp"])
    geq("M2.K_rank", m2["K_rank"], Wm2["K_rank"])
    want_true("M2.span_equals_Krank_exactly", m2["dim_span_Fp"] == m2["K_rank"])
    want_true("M2.both_full",
              m2["dim_span_Fp"] == m2["ambient_Fp"] == m2["K_rank_full"])

    # the cell is definitionally absent: index == 1 EXACTLY (not merely
    # small) -- the predicted coset W_c is the FULL ambient K^R
    geq("M2.index", m2["index"], Wm2["index"])
    want_true("M2.no_index_inflation", m2["index"] == 1)
    geq("M2.pred_W_is_full_size", m2["pred_W"], F7.q ** 3)

    feq("M2.exc_cond", m2["exc_cond"], Wm2["exc_cond"])
    g2g7 = gamma2_generic(F7, 6, 3, 3, True)
    eg7 = m2["G2"] / g2g7
    feq("M2.excess_generic", eg7, Wm2["excess_generic"])
    want_true("M2.excess_generic_near_one", 0.5 < eg7 < 2.0)
    feq("M2.offset_over_N", m2["offset_over_N"], Wm2["offset_over_N"])
    want_true("M2.at_balance_guard", m2["offset_over_N"] > -0.25)

    # ===================================================================== #
    #  M3 -- two-field reading (repair A): E vs B offset sweep over R        #
    # ===================================================================== #
    Wm3 = load("M3_two_field_reading")
    F16m = GF(2, 4)
    T16m = build_T(F16m, 15)
    geq("M3.N_real", len(T16m), 15)
    m3_rows = {}
    for R in range(3, 15):
        res = law_check(F16m, T16m, 8, False, R, "ones")
        tag = f"M3|R{R}"
        want = find(Wm3["rows"], "tag", tag)
        feq(f"{tag}.offset_over_N", res["offset_over_N"], want["offset_over_N"])
        feq(f"{tag}.offset_A_over_N", res["offset_A_over_N"], want["offset_A_over_N"])
        geq(f"{tag}.index", res["index"], want["index"])
        feq(f"{tag}.exc_cond", res["exc_cond"], want["exc_cond"])
        m3_rows[R] = res

    # (B)-reading balance sits at R in {3,4} (matches #422's own U16 balance_R=3
    # exactly); (A)-reading balance sits at R in {12,13} -- a genuinely
    # different R, straddling in EACH reading at ITS OWN R, not the other's
    want_true("M3.B_balance_straddles_at_R3_R4",
              m3_rows[3]["offset_over_N"] > 0 > m3_rows[4]["offset_over_N"])
    want_true("M3.A_balance_straddles_at_R12_R13",
              m3_rows[12]["offset_A_over_N"] > 0 > m3_rows[13]["offset_A_over_N"])
    # the two readings' balance points are NOT the same R (the conflation
    # repair (A) fixes is a real, measured effect, not a rounding wobble):
    # compute, from the swept data itself, which R minimizes |offset| under
    # each reading, and require them to differ by a wide margin
    b_nearest = min(range(3, 15), key=lambda R: abs(m3_rows[R]["offset_over_N"]))
    a_nearest = min(range(3, 15), key=lambda R: abs(m3_rows[R]["offset_A_over_N"]))
    geq("M3.b_nearest_balance_R", b_nearest, Wm3["b_nearest_balance_R"])
    geq("M3.a_nearest_balance_R", a_nearest, Wm3["a_nearest_balance_R"])
    want_true("M3.readings_disagree_on_balance_R", abs(a_nearest - b_nearest) >= 5)

    # the index inflation SURVIVES at the (A)-balance R=13: exact, large
    # index, and exc_cond ~ 1 (conditioning on W_c removes the excess there
    # too, same mechanism as #422's headline S27/U16o rows)
    r13 = m3_rows[13]
    geq("M3.R13.index_survives", r13["index"], Wm3["R13_index"])
    want_true("M3.R13.index_is_large", r13["index"] > 10**7)
    feq("M3.R13.exc_cond", r13["exc_cond"], Wm3["R13_exc_cond"])
    want_true("M3.R13.exc_cond_near_one", 0.9 < r13["exc_cond"] < 1.1)
    want_true("M3.R13.red_nonempty", len(r13["red"]) >= 1)
    # explicit nonclaim gate: this does NOT certify the printed asymptotic
    # o(N) clause -- only that finite offsets straddle 0 under this reading,
    # the same finite-balance-not-printed-clause discipline #422 uses
    geq("M3.printed_oN_clause_not_claimed", Wm3["printed_oN_clause_claimed"], False)

    # ===================================================================== #
    #  TAMPER SELF-TESTS (>=5) -- each MUST be caught, threaded through a    #
    #  live gate, none tautological                                         #
    # ===================================================================== #
    tampers = 0

    # T1: a faked M1 exc_cond value fed through the SAME feq() the real rows
    # use, with a corrupted expectation -- confirm FAILS grows, then retract
    # (exercises the actual gating pipeline, not an arithmetic tautology)
    ref = m1_results["F121"][0]
    pre_fails = len(FAILS)
    feq("tamper.T1.scratch_corrupted_exc_cond", ref["exc_cond"], ref["exc_cond"] * 1.5)
    if len(FAILS) == pre_fails + 1:
        FAILS.pop()
        tampers += 1

    # T2: M2's span=K-rank identity, corrupted by 1, must be CAUGHT by the
    # SAME geq() gate the real check uses (threads a corrupted value through
    # the live gate; not just an inline Python equality on the true values)
    pre_fails_t2 = len(FAILS)
    geq("tamper.T2.scratch_corrupted_span_eq_rank", m2["dim_span_Fp"], m2["K_rank"] + 1)
    if len(FAILS) == pre_fails_t2 + 1:
        FAILS.pop()
        tampers += 1

    # T3: the thin/has-red classification is a real, checkable fact, not a
    # hardcoded label -- claiming F16/F27 (the has-red baseline fields)
    # belong to the "thin" (#red=0) class must be FALSE for BOTH (catches a
    # hypothetical mislabeling of the M1 split, or a frob_free_red bug that
    # made #red vanish where it should not)
    mislabel_rejected = sum(1 for nm in ("F16", "F27")
                             if (fields[nm][1] - 1) // fields[nm][0].p != 0)
    if mislabel_rejected == 2:
        tampers += 1

    # T4: the (A) vs (B) reading offsets are genuinely different formulas --
    # the (B)-reading offset_over_N is NOWHERE NEAR straddling zero at
    # R=12/13 (both strongly negative), so a bug that conflated the two
    # readings (used offset_over_N where offset_A_over_N was intended) would
    # make the M3.A_balance_straddles_at_R12_R13 check above FAIL; verify
    # that precondition holds (the B-offset really is far from 0 there)
    if m3_rows[12]["offset_over_N"] < -2.0 and m3_rows[13]["offset_over_N"] < -2.0:
        tampers += 1

    # T5: a corrupted M2 index (off by a factor of p, mimicking a
    # hypothetical free/red-split bug at k=1) must be CAUGHT by the SAME
    # geq() gate the real check uses
    pre_fails_t5 = len(FAILS)
    geq("tamper.T5.scratch_corrupted_index", m2["index"], F7.p)
    if len(FAILS) == pre_fails_t5 + 1:
        FAILS.pop()
        tampers += 1

    # T6: dual-path field multiply -- table backend vs log/antilog backend
    # agree on the FULL q x q sweep for the two new M1 primes (validates
    # this script's own GF copy at the two new (p,k) pairs, not just the
    # three already exercised by #422)
    F121c, _ = fields["F121"]; F125c, _ = fields["F125"]
    mism121 = sum(1 for a in range(F121c.q) for b in range(F121c.q)
                  if F121c.mul(a, b) != F121c.mul_dual(a, b))
    mism125 = sum(1 for a in range(F125c.q) for b in range(F125c.q)
                  if F125c.mul(a, b) != F125c.mul_dual(a, b))
    geq("dual.mul.F121", mism121, 0)
    geq("dual.mul.F125", mism125, 0)
    if mism121 == 0 and mism125 == 0:
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
    print("Residual controls: M1 thin-alphabet residual (R-1<p corner) measured "
          "BOUNDED at q=121,125 too (not a p in {2,3,7} coincidence, though not a "
          "universal constant either); M2 prime-field control confirms the F_p-span "
          "cell is definitionally absent at K=F_7 (index=1 exactly); M3 confirms the "
          "span-cell index survives at the (A)-reading balance R (~12-13, distinct "
          "from the (B)-reading balance R~3-4).")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
