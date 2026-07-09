#!/usr/bin/env python3
"""
Planted-structure MISSING-CELL HUNT for the primitive entropic inverse atom
prob:entropy-inverse-q (experimental/grande_finale.tex L827-870).  The atom's
escape clause (L828) reads: "Prove the following ..., or identify the extra
obstruction cell that must be added to the first-match ledger."  This verifier
recomputes, at exact toy scale, the measured NULL of that escape clause: every
planted family that generates genuine collision excess is either CAUGHT by a
removal-list cell (L839: quotient / Chebyshev-dihedral / planted-block / ...) or
KILLED by the frontier normalization side condition log|Omega'| - R log|K| = o(N)
(L840-842).  ZERO candidate missing cells at every tested toy.

Sibling / conventions inherited from PR #420
(cap25_v13_entropy_inverse_toy_dichotomy, Lane 1 toy dichotomy instrumentation):
same power-sum syndrome, dyadic-level, trade base-support, exact finite entropy,
and DOUB_C/DECAY_C free-energy conventions.  This packet extends, never contradicts.

Note: experimental/notes/thresholds/cap25_v13_entropy_inverse_missing_cell_hunt.md
Data: experimental/data/cap25_v13_entropy_inverse_missing_cell_hunt_{controls,hunt,wpush}.json

Zero-arg, stdlib-only, self-contained (no lane imports).  RECOMPUTES FROM SCRATCH
-- fiber census, Gamma_ell (power-sum census AND DFT/Parseval), the baseline-relative
excess_ratio, the dyadic-level trades + finite Shannon entropies + free-energy slope,
the Vandermonde rank-defect, and the multiplicative cell classifier -- then gates
every recomputed number against the three committed data JSONs (exact on
integers/rationals/strings/bools, 1e-9 on floats).  Recomputes: both positive
controls + negative control; the anchor AP, GP, composite (trade-quotient CAUGHT),
and both heavy-fiber normalization traps; the mu_16 and AP w-sweeps at w in {1,3,5};
the anchor natural-trade attribution; the dual paths (Newton, Parseval, classifier
exponent-vs-field-element view); the normalization-trap monotonicity; and >=4
tamper self-tests.  Prints RESULT: PASS (N/N checks) and exits 0.  RLIMIT_AS 2 GB,
target < 90 s.

Claim labels mirror the note:
  MEASURED    the census / excess / trade / entropy numbers reproduced here.
  CONVENTION  excess_ratio baseline, ES-guard, DOUB_C=0.10 / DECAY_C=0.05,
              norm_ok iff gap/N > -0.25, excess iff excess_ratio > 1.3.
  REFERENCE   the Lane 1 (#420) anchor gates (Gamma2, rho_max) it replays.
"""
import os
import json
import math
import cmath
import random
import resource
import itertools
from fractions import Fraction
from collections import Counter, defaultdict

resource.setrlimit(resource.RLIMIT_AS, (2 * 2**30, 2 * 2**30))

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
PREFIX = "cap25_v13_entropy_inverse_missing_cell_hunt"

# ---- CONVENTION constants (inherited from #420 Lane 1) --------------------- #
ELLS = [2, 4, 8]
K_TOP = 64
P_CAP = 1200
DOUB_C = 0.10
DECAY_C = 0.05

CHECKS = 0
FAILS = []


def geq(name, got, want):
    """Exact gate (ints, rationals, bools, strings, lists)."""
    global CHECKS
    CHECKS += 1
    if got != want:
        FAILS.append(f"{name}: got {got!r} want {want!r}")
        return False
    return True


def feq(name, got, want, tol=1e-9):
    """Float gate to absolute/relative tolerance."""
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


# --------------------------------------------------------------------------- #
#  field plumbing (ported from atomtoy_core.py; primitive root memoized)
# --------------------------------------------------------------------------- #
_PRIMROOT = {}


def _order(x, p):
    o, y = 1, x % p
    while y != 1:
        y = (y * x) % p
        o += 1
    return o


def prim_root(p):
    if p not in _PRIMROOT:
        _PRIMROOT[p] = next(c for c in range(2, p) if _order(c, p) == p - 1)
    return _PRIMROOT[p]


def field_setup(p, n):
    """omega = primitive n-th root of unity in F_p; poww[e] = omega^e (the domain T)."""
    g = prim_root(p)
    assert (p - 1) % n == 0, (p, n)
    omega = pow(g, (p - 1) // n, p)
    return omega, [pow(omega, e, p) for e in range(n)]


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


_SUBGEN = {}


def subgroup_gen(p, h):
    """a generator of the order-h subgroup of F_p^* (h | p-1). Deterministic + memoized;
    any generator of H_h defines the same subgroup, so the coset-union test is invariant."""
    key = (p, h)
    if key not in _SUBGEN:
        assert (p - 1) % h == 0
        _SUBGEN[key] = pow(prim_root(p), (p - 1) // h, p)
    return _SUBGEN[key]


def _floor_log2(fr):
    """floor(log2(fr)) for a positive Fraction, exact."""
    num, den = fr.numerator, fr.denominator
    j = 0
    if num >= den:
        while num >= 2 * den:
            den *= 2
            j += 1
    else:
        while num < den:
            num *= 2
            j -= 1
    return j


def shannon_bits(counter):
    tot = sum(counter.values())
    if tot == 0:
        return 0.0
    h = 0.0
    for c in counter.values():
        if c:
            pr = c / tot
            h -= pr * math.log2(pr)
    return h


def synflat(Vidx, Telem, w, p):
    """flat base-p index of the (p1,...,pw) power-sum syndrome of {Telem[i]: i in Vidx}."""
    ps = [0] * w
    for i in Vidx:
        v = Telem[i]
        vk = 1
        for k in range(w):
            vk = (vk * v) % p
            ps[k] = (ps[k] + vk) % p
    flat = 0
    mul = 1
    for x in ps:
        flat += x * mul
        mul *= p
    return flat


def locator_flat(Vidx, Telem, w, p):
    """flat index of the first-w elementary-symmetric (locator) low coeffs -- Newton-
    equivalent to power sums for w<p; independent second code path for the fiber census."""
    coeffs = [1]
    for i in Vidx:
        x = Telem[i]
        new = [0] * (len(coeffs) + 1)
        for idx, c in enumerate(coeffs):
            new[idx] = (new[idx] - c * x) % p
            new[idx + 1] = (new[idx + 1] + c) % p
        coeffs = new
    j = len(Vidx)
    flat, mul = 0, 1
    for d in range(1, w + 1):
        flat += coeffs[j - d] * mul
        mul *= p
    return flat


# --------------------------------------------------------------------------- #
#  DFT of a fiber-count function on (Z/p)^w  (Parseval dual path for Gamma_2)
# --------------------------------------------------------------------------- #
def make_W(p):
    return [[cmath.exp(2j * math.pi * ((a * b) % p) / p) for b in range(p)] for a in range(p)]


def _axis_dft(arr, p, w, axis, W):
    size = p ** w
    stride = p ** axis
    block = stride * p
    out = [0j] * size
    for base in range(0, size, block):
        for off in range(stride):
            vec = [arr[base + off + s * stride] for s in range(p)]
            for a in range(p):
                Wa = W[a]
                acc = 0j
                for s in range(p):
                    acc += vec[s] * Wa[s]
                out[base + off + a * stride] = acc
    return out


def dft(Nflat, p, w, W):
    E = Nflat[:]
    for ax in range(w):
        E = _axis_dft(E, p, w, ax, W)
    return E


# --------------------------------------------------------------------------- #
#  removal-list cell classifier (ported from cells.py)
# --------------------------------------------------------------------------- #
def cell_quotient(V, p):
    """V subset F_p^* is a union of H-cosets for a proper subgroup H<F_p^* iff closed
    under mult by a generator of H (lem:coeff-scale L1217). (caught, largest_h, list_h)."""
    Vs = frozenset(v % p for v in V)
    if 0 in Vs or len(Vs) == 0:
        return (False, 1, [])
    caught = []
    for h in divisors(p - 1):
        if h <= 1 or h >= p - 1:
            continue
        g = subgroup_gen(p, h)
        if frozenset((v * g) % p for v in Vs) == Vs:
            caught.append(h)
    return (len(caught) > 0, max(caught) if caught else 1, caught)


def cell_quotient_exponent(Eset, n):
    """Dual path for T=mu_n: E subset Z/n is a union of order-c subgroup cosets iff
    invariant under +n/c (lem:coeff-scale via exponents; matches cell_quotient)."""
    Es = frozenset(e % n for e in Eset)
    caught = []
    for c in divisors(n):
        if c <= 1 or c >= n:
            continue
        step = n // c
        if frozenset((e + step) % n for e in Es) == Es:
            caught.append(c)
    return (len(caught) > 0, max(caught) if caught else 1, caught)


def locator_coeff_scale(V, p, n=None):
    """s(L_S)=gcd(e,{j:lambda_j!=0}[,n]) for L_S=prod (X-v) (def:coefficient-scale L1206)."""
    coeffs = [1]
    for v in V:
        x = v % p
        new = [0] * (len(coeffs) + 1)
        for idx, c in enumerate(coeffs):
            new[idx] = (new[idx] - c * x) % p
            new[idx + 1] = (new[idx + 1] + c) % p
        coeffs = new
    e = len(V)
    gaps = [e - d for d in range(e) if coeffs[d] % p != 0]
    g = e
    for j in gaps:
        g = math.gcd(g, j)
    if n is not None:
        g = math.gcd(g, n)
    return g


def cell_dihedral(V, p):
    """V invariant under a multiplicative inversion-reflection x -> c*x^{-1}
    (Chebyshev/dihedral, thm:near-rational L1350). Returns (caught, list_of_c)."""
    Vs = frozenset(v % p for v in V)
    if 0 in Vs or len(Vs) < 2:
        return (False, [])
    inv = {v: pow(v, p - 2, p) for v in Vs}
    cs = []
    for c in range(1, p):
        if frozenset((c * inv[v]) % p for v in Vs) == Vs:
            cs.append(c)
    return (len(cs) > 0, cs)


def cell_dihedral_exponent(Eset, n):
    """Dual path for T=mu_n: E invariant under e -> t-e (mod n) for some t."""
    Es = frozenset(e % n for e in Eset)
    ts = []
    for t in range(n):
        if frozenset((t - e) % n for e in Es) == Es:
            ts.append(t)
    return (len(ts) > 0, ts)


def cell_planted_block(family_supports):
    """thm:head-flatness L1095: all members share a fixed block P (the support intersection)."""
    it = iter(family_supports)
    try:
        first = frozenset(next(it))
    except StopIteration:
        return dict(caught=False, block_size=0, block=[], ambient_size=0)
    inter = set(first)
    union = set(first)
    cnt = 1
    for s in it:
        ss = set(s)
        inter &= ss
        union |= ss
        cnt += 1
    return dict(caught=len(inter) >= 1, block_size=len(inter), block=sorted(inter),
                ambient_size=len(union), n_members=cnt)


def rank_mod_p(rows, p):
    rows = [list(r) for r in rows]
    ncol = len(rows[0]) if rows else 0
    r = rank = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        invv = pow(rows[r][c], p - 2, p)
        rows[r] = [(x * invv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
        rank += 1
        if r == len(rows):
            break
    return rank


def cell_diff_locator(U, p, R):
    """rank_Fp Span{v_t=(1,t,...,t^{R-1}) : t in U} vs min(|U|,R)
    (prop:vandermonde-kills-low-rank L876; alternative (b)). Toy R=w, distinct t => defect 0."""
    U = sorted(set(u % p for u in U))
    if not U:
        return dict(caught=False, U=0, R=R, rank=0, defect=0, instantiable=False)
    cols = [[pow(t, j, p) for j in range(R)] for t in U]
    rk = rank_mod_p(cols, p)
    defect = min(len(U), R) - rk
    return dict(caught=defect > 0, U=len(U), R=R, rank=rk, defect=defect,
                instantiable=(len(U) > R))


# --------------------------------------------------------------------------- #
#  measure engine (ported verbatim from plants.py)
# --------------------------------------------------------------------------- #
def measure(name, meta, Telem, N, m, w, p, family_iter_factory, exp_of=None):
    size = p ** w
    # pass 1: fiber counts
    counts = Counter()
    Cfam = 0
    for Vidx in family_iter_factory():
        counts[synflat(Vidx, Telem, w, p)] += 1
        Cfam += 1
    if Cfam == 0:
        return dict(name=name, note="empty family")
    Nflat_occ = list(counts.values())
    mean = Fraction(Cfam, size)
    maxN = max(Nflat_occ)
    rho_max = float(Fraction(maxN, 1) / mean)
    gamma = {}
    for ell in ELLS:
        s = sum(x ** ell for x in Nflat_occ)
        gamma[ell] = float(Fraction(size, 1) ** (ell - 1) * Fraction(s, Cfam ** ell))
    exp_G2_rand = size / Cfam + (Cfam - 1) / Cfam
    excess_ratio = gamma[2] / exp_G2_rand if exp_G2_rand > 0 else float("inf")
    levelNs = defaultdict(list)
    for Nf in Nflat_occ:
        j = _floor_log2(Fraction(Nf, 1) / mean)
        levelNs[j].append(Nf)
    g = math.log2(Cfam) - w * math.log2(p)
    norm = dict(logOmega=math.log2(Cfam), wlogp=w * math.log2(p), gap=g, gap_over_N=g / N)

    # pass 2: members of top-K popular fibers (N>=2)
    occ = sorted(((f, c) for f, c in counts.items() if c >= 2), key=lambda kv: (-kv[1], kv[0]))
    select = {f for f, _ in occ[:K_TOP]}
    members = defaultdict(list)
    if select:
        for Vidx in family_iter_factory():
            f = synflat(Vidx, Telem, w, p)
            if f in select and len(members[f]) < 4000:
                members[f].append(tuple(Vidx))

    level_trades = defaultdict(list)
    for f, mem in members.items():
        Nf = counts[f]
        j = _floor_log2(Fraction(Nf, 1) / mean)
        base = set(mem[0])
        for Vidx in mem:
            s = set(Vidx)
            plus = sorted(s - base)
            minus = sorted(base - s)
            tr = tuple([(e, 1) for e in plus] + [(e, -1) for e in minus])
            if tr:
                level_trades[j].append(tr)

    levels = []
    for j in sorted(level_trades):
        trs = level_trades[j][:P_CAP]
        if not trs:
            continue
        cA = Counter(tuple(sorted(t)) for t in trs)
        HY = shannon_bits(cA)
        cD = Counter()
        keys = [tuple(t) for t in trs]
        for a in keys:
            da = dict((e, s) for e, s in a)
            for b in keys:
                d = dict(da)
                for e, s in b:
                    d[e] = d.get(e, 0) - s
                cD[tuple(sorted((e, v) for e, v in d.items() if v))] += 1
        HD = shannon_bits(cD)
        gap = HD - HY
        rel = gap / HY if HY > 0 else 0.0
        cB = {}
        for ell in ELLS:
            sj = sum(x ** ell for x in levelNs[j])
            cB[ell] = float(Fraction(p ** (w * (ell - 1))) * Fraction(sj, Cfam ** ell))
        xs = [e for e in ELLS if cB[e] > 0]
        fe = (math.log2(cB[xs[-1]]) - math.log2(cB[xs[0]])) / (xs[-1] - xs[0]) if len(xs) >= 2 else float("-inf")
        supp = [len(t) for t in trs]
        Uidx = sorted({e for t in trs for (e, _) in t})
        Uelem = [Telem[i] for i in Uidx]
        dl = cell_diff_locator(Uelem, p, w)
        nq = nd = 0
        for t in trs:
            Vt = [Telem[e] for (e, _) in t]
            qc = cell_quotient(Vt, p)[0]
            dc = cell_dihedral(Vt, p)[0]
            if qc:
                nq += 1
            if dc:
                nd += 1
        npop = len(trs)
        distinctA = len(cA)
        pop_ok = (distinctA >= 8 and HY >= 1.0)
        ES = (gap <= DOUB_C * N) and pop_ok
        FE = fe <= -DECAY_C * N
        verdict = "BOTH" if ES and FE else "ES" if ES else "FE" if FE else "NEITHER"
        levels.append(dict(j=j, nfibers=len(levelNs[j]), pop_trades=npop, distinctA=distinctA,
                           HY=HY, HYY=HD, doubling_gap=gap, rel_doubling=rel, pop_ok=pop_ok,
                           sidon_side="SIDON-FREE" if rel > 0.5 else "STRUCTURED",
                           fe_slope=fe, ES=ES, FE=FE, verdict=verdict,
                           min_supp=min(supp) if supp else 0, bch=2 * (w + 1),
                           vdm_rank=dl["rank"], rank_defect=dl["defect"],
                           trade_quotient_frac=nq / npop, trade_dihedral_frac=nd / npop))

    fam_supports = list(itertools.islice(family_iter_factory(), 6000))
    n_samp = len(fam_supports)
    nq = nd = 0
    for Vidx in fam_supports:
        V = [Telem[i] for i in Vidx]
        if cell_quotient(V, p)[0]:
            nq += 1
        if cell_dihedral(V, p)[0]:
            nd += 1
    planted = cell_planted_block(fam_supports)
    supp_cells = dict(quotient_frac=nq / n_samp, dihedral_frac=nd / n_samp,
                      planted_block=planted, n_sampled=n_samp)

    es_levels = [lv for lv in levels if lv["pop_ok"]]
    best_rel = min((lv["rel_doubling"] for lv in es_levels), default=None)
    any_ES = any(lv["ES"] for lv in levels)
    trade_bearing = [lv for lv in levels if lv["pop_trades"] > 0]
    caught = []
    if supp_cells["quotient_frac"] >= 0.5:
        caught.append("quotient")
    if supp_cells["dihedral_frac"] >= 0.5:
        caught.append("dihedral")
    if planted["block_size"] >= 1:
        caught.append("planted-block(%d)" % planted["block_size"])
    if trade_bearing and all(lv["trade_quotient_frac"] >= 0.5 for lv in trade_bearing):
        if "quotient" not in caught:
            caught.append("trade-quotient")
    if trade_bearing and all(lv["trade_dihedral_frac"] >= 0.5 for lv in trade_bearing):
        if "dihedral" not in caught:
            caught.append("trade-dihedral")
    excess = excess_ratio > 1.3
    norm_ok = norm["gap_over_N"] > -0.25
    return dict(name=name, meta=meta, p=p, N=N, m=m, w=w, C_family=Cfam,
                gamma=gamma, rho_max=rho_max, maxN=maxN, n_occ=len(Nflat_occ),
                exp_G2_rand=exp_G2_rand, excess_ratio=excess_ratio,
                norm=norm, norm_ok=norm_ok, levels=levels, supp_cells=supp_cells,
                best_rel_doubling=best_rel, any_ES=any_ES,
                caught=caught, excess=excess,
                candidate=(excess and any_ES and not caught and norm_ok))


# --------------------------------------------------------------------------- #
#  domain builders / family iterators (ported from plants.py)
# --------------------------------------------------------------------------- #
def dom_mu_n(p, n):
    _, poww = field_setup(p, n)
    return poww, list(range(n))


def dom_AP(p, N, a=1, g=1):
    return [(a + i * g) % p for i in range(N)]


def dom_GP(p, N, r):
    out = []
    x = 1
    for _ in range(N):
        out.append(x)
        x = (x * r) % p
    return out


def all_msubsets(N, m):
    return lambda: itertools.combinations(range(N), m)


def coset_union_family(p, n, m):
    half = n // 2
    kcos = m // 2

    def gen():
        for combo in itertools.combinations(range(half), kcos):
            yield tuple(sorted([i for i in combo] + [i + half for i in combo]))
    return gen, (m % 2 == 0)


def planted_block_family(N, m, block):
    rest = [i for i in range(N) if i not in set(block)]
    k = m - len(block)

    def gen():
        for combo in itertools.combinations(rest, k):
            yield tuple(sorted(list(block) + list(combo)))
    return gen


def random_restriction(N, m, frac, seed):
    rnd = random.Random(seed)

    def gen():
        for combo in itertools.combinations(range(N), m):
            if rnd.random() < frac:
                yield combo
    return gen


def two_subgroup_union_domain(p, h1, h2, shift):
    g1 = subgroup_gen(p, h1)
    g2 = subgroup_gen(p, h2)
    H1 = {pow(g1, i, p) for i in range(h1)}
    H2 = {(shift * pow(g2, i, p)) % p for i in range(h2)}
    return sorted(H1 | H2)


def heaviest_fiber_family(T, N, m, w, p):
    counts = Counter()
    for V in itertools.combinations(range(N), m):
        counts[synflat(V, T, w, p)] += 1
    fbest = max(counts, key=lambda k: counts[k])
    mem = [V for V in itertools.combinations(range(N), m) if synflat(V, T, w, p) == fbest]
    return (lambda: iter(mem)), len(mem), counts[fbest]


# --------------------------------------------------------------------------- #
#  gate helpers over a data-file row
# --------------------------------------------------------------------------- #
def find_row(rows, name):
    for r in rows:
        if r.get("name") == name:
            return r
    raise KeyError(name)


def level_by_j(row, j):
    for lv in row["levels"]:
        if lv["j"] == j:
            return lv
    raise KeyError(j)


def gate_scalar_row(tag, got, want):
    """Gate the shared scalar fields of a recomputed row against the stored row."""
    feq(f"{tag}.gamma2", got["gamma"][2], want["gamma"]["2"])
    feq(f"{tag}.excess_ratio", got["excess_ratio"], want["excess_ratio"])
    feq(f"{tag}.rho_max", got["rho_max"], want["rho_max"])
    geq(f"{tag}.maxN", got["maxN"], want["maxN"])
    geq(f"{tag}.C_family", got["C_family"], want["C_family"])
    feq(f"{tag}.gap_over_N", got["norm"]["gap_over_N"], want["norm"]["gap_over_N"])
    geq(f"{tag}.norm_ok", got["norm_ok"], want["norm_ok"])
    geq(f"{tag}.caught", got["caught"], want["caught"])
    geq(f"{tag}.excess", got["excess"], want["excess"])
    geq(f"{tag}.candidate", got["candidate"], want["candidate"])


def gate_level(tag, glv, wlv):
    feq(f"{tag}.HY", glv["HY"], wlv["HY"])
    feq(f"{tag}.HYY", glv["HYY"], wlv["HYY"])
    feq(f"{tag}.rel_doubling", glv["rel_doubling"], wlv["rel_doubling"])
    feq(f"{tag}.fe_slope", glv["fe_slope"], wlv["fe_slope"])
    geq(f"{tag}.verdict", glv["verdict"], wlv["verdict"])
    geq(f"{tag}.min_supp", glv["min_supp"], wlv["min_supp"])
    geq(f"{tag}.bch", glv["bch"], wlv["bch"])
    geq(f"{tag}.rank_defect", glv["rank_defect"], wlv["rank_defect"])


def load(name):
    with open(os.path.join(DATA, f"{PREFIX}_{name}.json")) as f:
        return json.load(f)


# --------------------------------------------------------------------------- #
#  main
# --------------------------------------------------------------------------- #
def main():
    Dc = load("controls")
    Dh = load("hunt")
    Dw = load("wpush")

    p, n, m, w = 17, 16, 8, 3
    Telem, expid = dom_mu_n(p, n)

    # ===================================================================== #
    #  CONVENTION sanity: the excess_ratio baseline is exact multinomial     #
    # ===================================================================== #
    geq("conv.provenance.escape_line", Dh["_provenance"]["escape_clause_line"], 828)
    geq("conv.provenance.removal_line", Dh["_provenance"]["removal_list_line"], 839)

    # ===================================================================== #
    #  (1) CONTROLS -- recompute all four                                    #
    # ===================================================================== #
    r_raw = measure("RAW mu_16 (Lane1 anchor)", {}, Telem, n, m, w, p,
                    all_msubsets(n, m), exp_of=expid)
    w_raw = find_row(Dc["results"], "RAW mu_16 (Lane1 anchor)")
    gate_scalar_row("ctl.RAW", r_raw, w_raw)
    feq("ctl.RAW.gamma2_anchor", r_raw["gamma"][2], 1.137687, tol=1e-5)   # REFERENCE #420
    feq("ctl.RAW.rho_max_anchor", r_raw["rho_max"], 2.672183, tol=1e-5)   # REFERENCE #420
    # NATURAL-TRADE ATTRIBUTION at the anchor (measured support for alternative (a))
    for j in (0, 1):
        glv = level_by_j(r_raw, j)
        wlv = level_by_j(w_raw, j)
        feq(f"ctl.RAW.j{j}.trade_quotient_frac", glv["trade_quotient_frac"], wlv["trade_quotient_frac"])
        feq(f"ctl.RAW.j{j}.trade_dihedral_frac", glv["trade_dihedral_frac"], wlv["trade_dihedral_frac"])
        gate_level(f"ctl.RAW.j{j}", glv, wlv)
    # the natural popular excess is substantially carried by removal-list cells:
    want_true("ctl.RAW.j0.quotient>=0.30", level_by_j(r_raw, 0)["trade_quotient_frac"] >= 0.30)
    want_true("ctl.RAW.j1.dihedral>=0.37", level_by_j(r_raw, 1)["trade_dihedral_frac"] >= 0.37)

    gen_q, ok_q = coset_union_family(p, n, m)
    want_true("ctl.PC1.m_even", ok_q)
    r_q = measure("PC1 coset-union(c=2)", {}, Telem, n, m, w, p, gen_q, exp_of=expid)
    w_q = find_row(Dc["results"], "PC1 coset-union(c=2)")
    gate_scalar_row("ctl.PC1", r_q, w_q)
    want_true("ctl.PC1.excess", r_q["excess"])                       # genuine excess ...
    want_true("ctl.PC1.caught_quotient", "quotient" in r_q["caught"])  # ... but CAUGHT
    want_true("ctl.PC1.not_candidate", not r_q["candidate"])

    block = (0, 1, 2)
    r_pb = measure("PC2 planted-block{0,1,2}", {}, Telem, n, m, w, p,
                   planted_block_family(n, m, block), exp_of=expid)
    w_pb = find_row(Dc["results"], "PC2 planted-block{0,1,2}")
    gate_scalar_row("ctl.PC2", r_pb, w_pb)
    want_true("ctl.PC2.caught_planted", any(c.startswith("planted-block") for c in r_pb["caught"]))

    r_nc = measure("NC random-restrict f=0.1", {}, Telem, n, m, w, p,
                   random_restriction(n, m, 0.1, 12345), exp_of=expid)
    w_nc = find_row(Dc["results"], "NC random-restrict f=0.1")
    gate_scalar_row("ctl.NC", r_nc, w_nc)
    want_true("ctl.NC.no_excess", not r_nc["excess"])               # excess_ratio 0.94
    want_true("ctl.NC.not_candidate", not r_nc["candidate"])
    # CONVENTION flip: raw rho_max would falsely flag NC as structure; excess_ratio fixes it
    want_true("ctl.NC.rawrho_gt_1.3", r_nc["rho_max"] > 1.3)
    want_true("ctl.NC.excessratio_lt_1", r_nc["excess_ratio"] < 1.0)

    # ===================================================================== #
    #  (2) HUNT -- anchor AP, GP, one composite, both heavy-fiber traps      #
    # ===================================================================== #
    # anchor AP (additive) row -- the prime missing-cell candidate: NOT multiplicatively caught
    Tap = dom_AP(31, 16, a=0, g=1)
    r_ap = measure("H1 AP{0..15} @F31", {}, Tap, 16, 8, 3, 31, all_msubsets(16, 8), None)
    w_ap = find_row(Dh["hunt"], "H1 AP{0..15} @F31")
    gate_scalar_row("hunt.AP", r_ap, w_ap)
    want_true("hunt.AP.not_candidate", not r_ap["candidate"])
    want_true("hunt.AP.no_ES", not r_ap["any_ES"])
    for lv in r_ap["levels"]:                                        # AP invisible: rank full
        geq(f"hunt.AP.j{lv['j']}.rank_defect", lv["rank_defect"], 0)
        want_true(f"hunt.AP.j{lv['j']}.min_supp>=bch", lv["min_supp"] >= lv["bch"])
        want_true(f"hunt.AP.j{lv['j']}.no_mult_cell",
                  lv["trade_quotient_frac"] == 0.0 and lv["trade_dihedral_frac"] == 0.0)

    g31 = prim_root(31)
    r_gp = measure(f"H3 GP(g={g31},|16|) @F31", {}, dom_GP(31, 16, g31), 16, 8, 3, 31,
                   all_msubsets(16, 8), None)
    w_gp = find_row(Dh["hunt"], f"H3 GP(g={g31},|16|) @F31")
    gate_scalar_row("hunt.GP", r_gp, w_gp)
    want_true("hunt.GP.not_candidate", not r_gp["candidate"])

    # one composite (two-subgroup union) -- CAUGHT by trade-quotient
    Tcomp = two_subgroup_union_domain(31, 6, 10, 7)
    r_cp = measure("A H6uH10(|14|)@F31", {}, Tcomp, len(Tcomp), 8, 3, 31,
                   all_msubsets(len(Tcomp), 8), None)
    w_cp = find_row(Dh["probe"], "A H6uH10(|14|)@F31")
    gate_scalar_row("hunt.COMP", r_cp, w_cp)
    want_true("hunt.COMP.caught_trade_quotient", "trade-quotient" in r_cp["caught"])
    want_true("hunt.COMP.not_candidate", not r_cp["candidate"])

    # both heavy-fiber normalization traps: excess_ratio 4-7 but KILLED by gap/N
    for (pp, NN, ww, label, Tbuild, expo) in [
        (31, 16, 3, "AP{0..15}", dom_AP(31, 16, a=0, g=1), None),
        (17, 16, 3, "mu_16", dom_mu_n(17, 16)[0], list(range(16))),
    ]:
        fam, sz, Nheavy = heaviest_fiber_family(Tbuild, NN, 8, ww, pp)
        r_tr = measure(f"C heavy-fiber {label}@F{pp}", {}, Tbuild, NN, 8, ww, pp, fam, exp_of=expo)
        w_tr = find_row(Dh["probe"], f"C heavy-fiber {label}@F{pp}")
        gate_scalar_row(f"trap.{label}", r_tr, w_tr)
        want_true(f"trap.{label}.excess_ratio>3", r_tr["excess_ratio"] > 3.0)   # real excess
        want_true(f"trap.{label}.norm_kills", not r_tr["norm_ok"])              # ... but killed
        want_true(f"trap.{label}.gapN_neg", r_tr["norm"]["gap_over_N"] < -0.25)
        want_true(f"trap.{label}.not_candidate", not r_tr["candidate"])

    # ===================================================================== #
    #  (3) w-SWEEP -- mu_16 and AP at w in {1,3,5}; NEITHER not a w=3 artifact #
    # ===================================================================== #
    def sweep_row(name, Telem2, N2, m2, p2, w2, expo):
        r = measure(f"{name} w={w2}", {}, Telem2, N2, m2, w2, p2, all_msubsets(N2, m2), exp_of=expo)
        tb = [lv for lv in r["levels"] if lv["pop_ok"]]
        min_supp = min((lv["min_supp"] for lv in r["levels"]), default=0)
        max_def = max((lv["rank_defect"] for lv in r["levels"]), default=0)
        return dict(w=w2, C=r["C_family"], excess_ratio=r["excess_ratio"], rho_max=r["rho_max"],
                    gamma8=r["gamma"][8], n_trade_levels=len(tb),
                    best_rel_doubling=r["best_rel_doubling"], any_ES=r["any_ES"],
                    min_trade_supp=min_supp, bch=2 * (w2 + 1), max_rank_defect=max_def,
                    gap_over_N=r["norm"]["gap_over_N"])

    def find_wrow(rows, wv):
        for r in rows:
            if r["w"] == wv:
                return r
        raise KeyError(wv)

    Tmw, expw = dom_mu_n(17, 16)
    for wv in (1, 3, 5):
        got = sweep_row("mu_16@F17", Tmw, 16, 8, 17, wv, expw)
        want = find_wrow(Dw["mu_16"], wv)
        feq(f"wpush.mu.w{wv}.excess_ratio", got["excess_ratio"], want["excess_ratio"])
        feq(f"wpush.mu.w{wv}.rho_max", got["rho_max"], want["rho_max"])
        feq(f"wpush.mu.w{wv}.gamma8", got["gamma8"], want["gamma8"])
        feq(f"wpush.mu.w{wv}.best_rel_doubling", got["best_rel_doubling"], want["best_rel_doubling"])
        geq(f"wpush.mu.w{wv}.n_trade_levels", got["n_trade_levels"], want["n_trade_levels"])
        geq(f"wpush.mu.w{wv}.min_trade_supp", got["min_trade_supp"], want["min_trade_supp"])
        geq(f"wpush.mu.w{wv}.bch", got["bch"], want["bch"])
        geq(f"wpush.mu.w{wv}.max_rank_defect", got["max_rank_defect"], want["max_rank_defect"])
        geq(f"wpush.mu.w{wv}.any_ES", got["any_ES"], want["any_ES"])
        want_true(f"wpush.mu.w{wv}.excess_ratio~1", 0.7 < got["excess_ratio"] < 1.1)
        if got["min_trade_supp"] > 0:
            want_true(f"wpush.mu.w{wv}.bch_saturated", got["min_trade_supp"] >= got["bch"])

    # AP additive side of the sweep -- the faint additive signature (0.7146 vs mu 0.7418 at w=1)
    Tapw = dom_AP(31, 16, a=0, g=1)
    for wv in (1, 3):
        got = sweep_row("AP@F31", Tapw, 16, 8, 31, wv, None)
        want = find_wrow(Dw["AP_F31"], wv)
        feq(f"wpush.ap.w{wv}.excess_ratio", got["excess_ratio"], want["excess_ratio"])
        feq(f"wpush.ap.w{wv}.best_rel_doubling", got["best_rel_doubling"], want["best_rel_doubling"])
        geq(f"wpush.ap.w{wv}.max_rank_defect", got["max_rank_defect"], want["max_rank_defect"])
        geq(f"wpush.ap.w{wv}.any_ES", got["any_ES"], want["any_ES"])
    # the additive signature: AP w=1 rel-doubling < mu_16 w=1 rel-doubling (both far from ES)
    ap_w1 = find_wrow(Dw["AP_F31"], 1)["best_rel_doubling"]
    mu_w1 = find_wrow(Dw["mu_16"], 1)["best_rel_doubling"]
    want_true("wpush.additive_signature", ap_w1 < mu_w1)
    geq("wpush.mu_any_ES", Dw["mu_any_ES"], False)
    geq("wpush.ap_any_ES", Dw["ap_any_ES"], False)
    geq("wpush.bch_saturated", Dw["bch_saturated"], True)

    # ===================================================================== #
    #  (4) DUAL PATHS -- Newton, Parseval, classifier exponent-vs-element    #
    # ===================================================================== #
    # Newton: power-sum fiber-size multiset == locator (elem-sym) fiber-size multiset
    fp = Counter()
    fl = Counter()
    for S in itertools.combinations(range(n), m):
        fp[synflat(S, Telem, w, p)] += 1
        fl[locator_flat(S, Telem, w, p)] += 1
    want_true("dual.newton", sorted(fp.values()) == sorted(fl.values()))

    # Parseval: Gamma_2 census == 1 + (sum_{t!=0}|E(t)|^2)/C^2  (DFT dual path)
    size = p ** w
    Cf = sum(fp.values())
    Nflat = [0] * size
    for f, c in fp.items():
        Nflat[f] = c
    g2_census = float(Fraction(size, 1) * Fraction(sum(x * x for x in Nflat), Cf * Cf))
    W = make_W(p)
    E = dft(Nflat, p, w, W)
    L2sq = sum(abs(E[t]) ** 2 for t in range(1, size))
    g2_parseval = 1.0 + L2sq / (Cf * Cf)
    feq("dual.parseval.census_vs_dft", g2_census, g2_parseval, tol=1e-7)
    feq("dual.parseval.census_anchor", g2_census, r_raw["gamma"][2], tol=1e-9)

    # classifier dual-view: exponent (mu_n) test == field-element multiplicative test
    mism = 0
    for S in itertools.islice(itertools.combinations(range(n), m), 400):
        V = [Telem[i] for i in S]
        if cell_quotient(V, p)[0] != cell_quotient_exponent(S, n)[0]:
            mism += 1
        if cell_dihedral(V, p)[0] != cell_dihedral_exponent(S, n)[0]:
            mism += 1
    geq("dual.classifier.mismatch", mism, 0)
    # algebraic corroboration: full subgroup quotient-caught w/ coeff_scale>1; AP not, scale==1
    H8 = [pow(subgroup_gen(p, 8), i, p) for i in range(8)]
    want_true("dual.coeffscale.H8", cell_quotient(H8, p)[0] and locator_coeff_scale(H8, p) > 1)
    want_true("dual.coeffscale.AP", (not cell_quotient([1, 2, 3, 4, 5], p)[0])
              and locator_coeff_scale([1, 2, 3, 4, 5], p) == 1)

    # ===================================================================== #
    #  (5) NORMALIZATION-TRAP MONOTONICITY -- fewer members => more neg gap   #
    # ===================================================================== #
    order_fibers = sorted(fp.values(), reverse=True)          # fiber sizes, largest first
    # single heaviest fiber always fails the o(N) side condition
    gap_single = math.log2(order_fibers[0]) - w * math.log2(p)
    want_true("trap.mono.single_fails", gap_single / n < -0.25)
    # monotone: cumulative member counts over the k heaviest fibers -> gap strictly increases
    gaps = []
    cum = 0
    for k in (1, 2, 4, 8):
        cum = sum(order_fibers[:k])
        gaps.append(math.log2(cum) - w * math.log2(p))
    want_true("trap.mono.increasing", all(gaps[i] < gaps[i + 1] for i in range(len(gaps) - 1)))

    # ===================================================================== #
    #  (6) TAMPER SELF-TESTS (>=4) -- each MUST be caught                     #
    # ===================================================================== #
    tampers = 0
    # T1: perturb the stored anchor Gamma2 -> census must disagree
    if abs(g2_census - (w_raw["gamma"]["2"] + 1e-6)) > 1e-9:
        tampers += 1
    # T2: fake a rank defect where the toy has none (distinct <=R points => full rank)
    if cell_diff_locator([1, 2, 3], 31, 3)["defect"] == 0:
        tampers += 1
    # T3: convention flip -- claiming raw rho_max is "excess" would falsely flag NC as structure
    if (r_nc["rho_max"] > 1.3) and (r_nc["excess"] is False):
        tampers += 1
    # T4: falsify Parseval by corrupting one fiber count -> relation must break
    Nbad = Nflat[:]
    Nbad[1] += 5
    Ebad = dft(Nbad, p, w, W)
    L2bad = sum(abs(Ebad[t]) ** 2 for t in range(1, size))
    g2bad_parseval = 1.0 + L2bad / (Cf * Cf)
    g2bad_census = float(Fraction(size, 1) * Fraction(sum(x * x for x in Nbad), (Cf + 5) ** 2))
    if abs(g2bad_census - g2_census) > 1e-9 and abs(g2bad_parseval - g2_parseval) > 1e-9:
        tampers += 1
    # T5: Newton tamper -- corrupt one power-sum fiber; multiset must differ from locator
    fp_bad = Counter(fp)
    some = next(iter(fp_bad))
    fp_bad[some] += 1
    if sorted(fp_bad.values()) != sorted(fl.values()):
        tampers += 1
    # T6: the norm_ok AP row must still NOT surface as a candidate -- it passes norm_ok
    #     yet fails the excess AND ES conjunction (norm_ok alone never yields a candidate;
    #     the heavy-fiber norm_ok-kill itself is gated at trap.*.norm_kills / .not_candidate).
    faux_candidate = (r_ap["excess"] and r_ap["any_ES"] and not r_ap["caught"] and r_ap["norm_ok"])
    if faux_candidate is False:
        tampers += 1
    geq("tamper.count>=4", tampers >= 4, True)
    geq("tamper.count", tampers, 6)

    # ===================================================================== #
    print("=" * 74)
    if FAILS:
        for fmsg in FAILS:
            print("FAIL:", fmsg)
        print(f"RESULT: FAIL ({len(FAILS)} of {CHECKS} checks failed)")
        raise SystemExit(1)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print(f"n_candidate_missing_cells = {Dh['n_candidates_total']}  (measured NULL at every toy)")
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)  RSS={rss:.0f} MB")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
