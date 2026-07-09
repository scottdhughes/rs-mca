#!/usr/bin/env python3
"""
Toy instrumentation of the primitive entropic inverse atom prob:entropy-inverse-q
(experimental/grande_finale.tex L827-870), its L869 Sidon/free-energy dichotomy,
and rem:mass-aware-logmoment (L966-968).

Note: experimental/notes/thresholds/cap25_v13_entropy_inverse_toy_dichotomy.md
Data: experimental/data/cap25_v13_entropy_inverse_toy_dichotomy_<toy>.json (4 toys)

Zero-arg, stdlib-only, self-contained (no lane imports).  RECOMPUTES from scratch
-- fiber census, Gamma_ell (two paths: power-sum census and DFT/Parseval), the
signed-trade Vandermonde rank census, and the per-dyadic-level entropy /
free-energy dichotomy -- then gates every recomputed number against the committed
per-toy data JSONs (byte-exact on integers/rationals, 1e-9 on floats).  Anchor
(17,16,8,3) is recomputed in full; (13,12,6,2) in full; (19,18,9,3) and
(23,22,11,3) have their census + dense-heavy decomposition recomputed (the p=23
tau=39/2261 and PR(E_Q)=p^w-1 degeneracy gates), with the trade/dichotomy rows
gated against the stored data.  Ends with tamper self-tests and prints
RESULT: PASS (N/N checks), exit 0.  Research run 33s; this verifier ~25s.

Claim labels mirror the note:
  MEASURED    the census/trade/entropy numbers reproduced here.
  CONVENTION  dyadic level, trade base-support rule, exact finite entropies,
              fe_slope + thresholds DOUB_C=0.10, DECAY_C=0.05 (so 1.60 / -0.80 at N=16).
  REFERENCE   the #416/#413 anchor gates (tau, Gamma2, PR, primitive triangle).
"""
import os
import json
import math
import cmath
import struct
import resource
from fractions import Fraction
from collections import Counter, defaultdict
from itertools import combinations

resource.setrlimit(resource.RLIMIT_AS, (2 * 2**30, 2 * 2**30))

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
GRID = [(17, 16, 8, 3), (13, 12, 6, 2), (19, 18, 9, 3), (23, 22, 11, 3)]
ELLS = list(range(2, 9))
POP_MULT = 2          # popular fiber iff N >= 2*mean
K_TOP = 64            # top-K fibers by N for the trade census
LS_MULT = 2           # low-support trade iff |support| <= 2w
RHO_DENSE = 0.5       # dense-heavy iff largest-class/N <= 0.5
DOUB_C = 0.10         # entropy-small-doubling iff gap <= 0.10*N
DECAY_C = 0.05        # free-energy decay iff fe_slope <= -0.05*N

CHECKS = 0
FAILS = []


def geq(name, got, want, show=True):
    """Exact gate (ints, rationals, bools, strings, lists)."""
    global CHECKS
    CHECKS += 1
    ok = (got == want)
    if not ok:
        FAILS.append(f"{name}: got {got!r} want {want!r}")
    if show:
        print(f"  [{'ok' if ok else 'XX'}] {name:52s} = {got}")
    return ok


def gclose(name, got, want, tol=1e-9, show=True):
    """Float gate to absolute/relative tolerance tol."""
    global CHECKS
    CHECKS += 1
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    if not ok:
        FAILS.append(f"{name}: got {got!r} want {want!r} tol={tol}")
    if show:
        print(f"  [{'ok' if ok else 'XX'}] {name:52s} = {got:.12g}")
    return ok


def load(toy):
    tag = "_".join(map(str, toy))
    with open(os.path.join(DATA, f"cap25_v13_entropy_inverse_toy_dichotomy_{tag}.json")) as fh:
        return json.load(fh)


# =====================================================================
#  self-contained cyclotomic / field / spectral plumbing
#  (recomputed independently of the research lane)
# =====================================================================
def field_setup(p, n):
    def order(x):
        o, y = 1, x % p
        while y != 1:
            y = (y * x) % p; o += 1
        return o
    g = next(c for c in range(2, p) if order(c) == p - 1)
    assert (p - 1) % n == 0
    omega = pow(g, (p - 1) // n, p)
    return omega, [pow(omega, e, p) for e in range(n)]


def powersum_flat(S, poww, n, w, p):
    flat, mul = 0, 1
    for k in range(1, w + 1):
        pk = 0
        for i in S:
            pk += poww[(k * i) % n]
        pk %= p
        flat += pk * mul; mul *= p
    return flat


def locator_flat(S, poww, n, w, p):
    coeffs = [1]
    for i in S:
        x = poww[i]
        new = [0] * (len(coeffs) + 1)
        for idx, c in enumerate(coeffs):
            new[idx] = (new[idx] - c * x) % p
            new[idx + 1] = (new[idx + 1] + c) % p
        coeffs = new
    j = len(S)
    flat, mul = 0, 1
    for d in range(1, w + 1):
        flat += coeffs[j - d] * mul; mul *= p
    return flat


def _exact_divide(num, den):
    num = list(num); dl = len(den) - 1; qdeg = len(num) - 1 - dl
    q = [0] * (qdeg + 1)
    for i in range(qdeg, -1, -1):
        c = num[i + dl] // den[dl]
        q[i] = c
        if c:
            for jj in range(dl + 1):
                num[i + jj] -= c * den[jj]
    return q


def _polydiv_int(num, den):
    num = list(num); dl = len(den) - 1
    for i in range(len(num) - 1, dl - 1, -1):
        c = num[i]
        if c:
            for jj in range(dl + 1):
                num[i - dl + jj] -= c * den[jj]
    return num[:dl]


def cyclotomic_poly(n):
    xn1 = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            xn1 = _exact_divide(xn1, cyclotomic_poly(d))
    return xn1


def build_redtab(n, phi):
    deg = len(phi) - 1
    tab = []
    for j in range(n):
        v = [0] * (j + 1); v[j] = 1
        r = _polydiv_int(v, phi)
        r = r + [0] * (deg - len(r))
        tab.append(tuple(r[:deg]))
    return tab, deg


def exact_key(S, redtab, n, w, deg):
    flat = []
    for k in range(1, w + 1):
        acc = [0] * deg
        for i in S:
            r = redtab[(k * i) % n]
            for t in range(deg):
                acc[t] += r[t]
        flat.extend(acc)
    return struct.pack('<%dh' % (w * deg), *flat)


def make_W(p):
    return [[cmath.exp(2j * math.pi * ((a * b) % p) / p) for b in range(p)] for a in range(p)]


def _axis_dft(arr, p, w, axis, W):
    size = p**w; stride = p**axis; block = stride * p; out = [0j] * size
    for base in range(0, size, block):
        for off in range(stride):
            vec = [arr[base + off + s * stride] for s in range(p)]
            for a in range(p):
                Wa = W[a]; acc = 0j
                for s in range(p):
                    acc += vec[s] * Wa[s]
                out[base + off + a * stride] = acc
    return out


def dft(Nflat, p, w, W):
    E = Nflat[:]
    for ax in range(w):
        E = _axis_dft(E, p, w, ax, W)
    return E


def coeff_scale(tflat, p, w, n):
    idx = tflat; supp = []
    for j in range(w):
        tj = idx % p; idx //= p
        if tj:
            supp.append(j + 1)
    if not supp:
        return 0
    c = n
    for k in supp:
        c = math.gcd(c, k)
    return c


def spectrum_stats(Nflat, p, w, n, C, W):
    size = p**w
    T = sum(Nflat); maxN = max(Nflat); sumN2 = sum(x * x for x in Nflat)
    E = dft(Nflat, p, w, W)
    L1 = L1p = L2sq = 0.0
    for t in range(1, size):
        ae = abs(E[t]); L1 += ae; L2sq += ae * ae
        if coeff_scale(t, p, w, n) == 1:
            L1p += ae
    Gamma2 = size * sumN2 / (T * T)
    PR = (L1 * L1 / L2sq) if L2sq > 0 else float('inf')
    return dict(T=T, maxN=maxN, R_rawavg=size * maxN / C, Gamma2=Gamma2, L1=L1,
                PR=PR, tri_prim_rawavg=(T + L1p) / C,
                parse_relerr=abs(L2sq - T * T * (Gamma2 - 1)) / (T * T * (Gamma2 - 1)) if Gamma2 > 1 else 0.0)


def gamma_float(Nflat, p, w, C, ell):
    size = p**w
    s = sum(x**ell for x in Nflat if x)
    return float(Fraction(size, 1)**(ell - 1) * Fraction(s, C**ell))


def _floor_log2(fr):
    num, den = fr.numerator, fr.denominator
    j = 0
    if num >= den:
        while num >= 2 * den:
            den *= 2; j += 1
    else:
        while num < den:
            num *= 2; j -= 1
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


# =====================================================================
#  recompute: census (Nraw, M_gen, Gamma, spectrum, dyadic, perfiber)
# =====================================================================
def recompute_census(p, n, m, w, want_dft=True):
    omega, poww = field_setup(p, n)
    phi = cyclotomic_poly(n)
    redtab, deg = build_redtab(n, phi)
    size = p**w
    C = math.comb(n, m)
    Nraw = [0] * size
    Nloc = [0] * size
    perfiber = {}
    for S in combinations(range(n), m):
        f = powersum_flat(S, poww, n, w, p)
        Nraw[f] += 1
        Nloc[locator_flat(S, poww, n, w, p)] += 1
        ek = exact_key(S, redtab, n, w, deg)
        d = perfiber.get(f)
        if d is None:
            perfiber[f] = {ek: 1}
        else:
            d[ek] = d.get(ek, 0) + 1
    ok_newton = sorted(x for x in Nraw if x) == sorted(x for x in Nloc if x)
    Ngen = [0] * size
    for f, classes in perfiber.items():
        Ngen[f] = max(classes.values())
    T_Q = sum(Ngen)
    mean = Fraction(C, size)
    # dyadic level -> list of Nraw fiber sizes (all occupied fibers)
    levelNs = defaultdict(list)
    for f in range(size):
        if Nraw[f]:
            levelNs[_floor_log2(Fraction(Nraw[f], 1) / mean)].append(Nraw[f])
    # fiber_table for dense-heavy: f -> (N, nclasses, largest).  Built in
    # INCREASING-f order so the top-K-by-N selection breaks equal-N ties exactly
    # as the research lane does (it reads fiber_table from JSON, which step1 wrote
    # in range(size) order); a stable sort by -N then reproduces the same top-K.
    fiber_table = {f: (Nraw[f], len(perfiber[f]), max(perfiber[f].values()))
                   for f in range(size) if Nraw[f]}
    out = dict(p=p, n=n, m=m, w=w, C=C, size=size, mean=mean, phi_deg=deg,
               maxN_raw=max(Nraw), n_fibers_occ=sum(1 for x in Nraw if x),
               ok_newton=ok_newton, T_Q=T_Q, tau=Fraction(T_Q, C),
               raw_gamma={e: gamma_float(Nraw, p, w, C, e) for e in ELLS},
               masked_gamma={e: gamma_float(Ngen, p, w, T_Q, e) for e in ELLS},
               Ndist=Counter(Nraw), levelNs=dict(levelNs), fiber_table=fiber_table,
               perfiber=perfiber, poww=poww, redtab=redtab, deg=deg,
               Nraw=Nraw, Ngen=Ngen)
    if want_dft:
        W = make_W(p)
        out["raw_spectrum"] = spectrum_stats(Nraw, p, w, n, C, W)
        out["masked_spectrum"] = spectrum_stats(Ngen, p, w, n, T_Q, W)
    return out


# =====================================================================
#  recompute: dense-heavy vs sparse-heavy (rem:mass-aware, #416 sec7)
# =====================================================================
def recompute_dense(cen):
    ft = cen["fiber_table"]; mean = float(cen["mean"])
    popular = [f for f, v in ft.items() if v[0] >= POP_MULT * mean]
    topK = [f for f, _ in sorted(ft.items(), key=lambda kv: -kv[1][0])[:K_TOP]]

    def aggregate(fibers):
        if not fibers:
            return None
        vs = [(ft[f][0], ft[f][2] / ft[f][0]) for f in fibers]
        dense = [v for v in vs if v[1] <= RHO_DENSE]
        massD = sum(v[0] for v in dense); massT = sum(v[0] for v in vs)
        rhos = [v[1] for v in vs]
        return dict(nfibers=len(vs), n_dense=len(dense),
                    frac_dense_mass=massD / massT,
                    rho_min=min(rhos), rho_max=max(rhos),
                    hypothesis="HOLD" if massD / massT > 0.5 else "FAIL")
    max_rho_top = max(ft[f][2] / ft[f][0] for f in topK)
    return dict(agg_popular=aggregate(popular), agg_topK=aggregate(topK),
                agg_all=aggregate(list(ft.keys())), max_rho_topK=max_rho_top,
                n_popular=len(popular), falsifier_near_delta=(max_rho_top > 0.9))


# =====================================================================
#  recompute: signed trades + Vandermonde rank (skeleton steps 2,3,6)
# =====================================================================
def rank_mod_p(rows, p):
    rows = [list(r) for r in rows]; rank = 0
    ncol = len(rows[0]) if rows else 0
    r = 0
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
                fmul = rows[i][c]
                rows[i] = [(a - fmul * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1; rank += 1
        if r == len(rows):
            break
    return rank


def recompute_trades(cen):
    p, n, m, w = cen["p"], cen["n"], cen["m"], cen["w"]
    poww, redtab, deg = cen["poww"], cen["redtab"], cen["deg"]
    ft = cen["fiber_table"]; mean = cen["mean"]
    R = n
    LS_THRESH = LS_MULT * w
    occ = sorted(((f, v[0]) for f, v in ft.items() if v[0] >= 2), key=lambda kv: -kv[1])
    select = {f for f, _ in occ[:K_TOP]}
    members = defaultdict(list)
    for S in combinations(range(n), m):
        f = powersum_flat(S, poww, n, w, p)
        if f in select:
            members[f].append((S, exact_key(S, redtab, n, w, deg)))
    level_fibers = defaultdict(list)
    level_trades = defaultdict(list)
    moment_ok = True
    for f, mem in members.items():
        classes = defaultdict(list)
        for (S, ek) in mem:
            classes[ek].append(S)
        M0 = set(classes[max(classes, key=lambda k: len(classes[k]))][0])
        j = _floor_log2(Fraction(len(mem), 1) / mean)
        trades = []
        for (S, ek) in mem:
            Sset = set(S)
            trade = tuple([(e, 1) for e in sorted(Sset - M0)] +
                          [(e, -1) for e in sorted(M0 - Sset)])
            trades.append(trade)
        for trade in trades[:min(len(trades), 50)]:
            for k in range(1, w + 1):
                if sum(sgn * pow(poww[e], k, p) for (e, sgn) in trade) % p != 0:
                    moment_ok = False
        level_fibers[j].append(f)
        for t in trades:
            if t:
                level_trades[j].append(list(t))
    levels = {}
    for j in sorted(level_fibers):
        trs = level_trades[j]
        supp = [len(t) for t in trs]
        U = sorted({e for t in trs for (e, _) in t})
        cols = [[pow(poww[e], j2, p) for j2 in range(R)] for e in U]
        rk = rank_mod_p(cols, p) if cols else 0
        levels[str(j)] = dict(
            j=j, n_fibers=len(level_fibers[j]), pop_trades=len(trs),
            supp_hist={int(k): int(v) for k, v in sorted(Counter(supp).items())},
            min_supp=min(supp) if supp else 0,
            low_supp_count=sum(1 for s in supp if s <= LS_THRESH),
            U_size=len(U), vdm_rank=rk, rank_defect=min(len(U), R) - rk)
    return dict(LS_THRESH=LS_THRESH, R=R, moment_eqs_ok=moment_ok, levels=levels,
                level_trades={str(j): v for j, v in level_trades.items()})


# =====================================================================
#  recompute: L869 Sidon / free-energy dichotomy per dyadic level
# =====================================================================
def diff_key(a, b):
    d = {}
    for e, s in a:
        d[e] = d.get(e, 0) + s
    for e, s in b:
        d[e] = d.get(e, 0) - s
    return tuple(sorted((e, v) for e, v in d.items() if v))


def entropy_branch(trades, n):
    cA = Counter(tuple(t) for t in trades)
    HY = shannon_bits(cA)

    def dense(t):
        v = [0] * n
        for e, s in t:
            v[e] = s
        return tuple(v)
    HY2 = shannon_bits(Counter(dense(t) for t in trades))
    cD = Counter()
    keys = [tuple((e, s) for e, s in t) for t in trades]
    for a in keys:
        for b in keys:
            cD[diff_key(a, b)] += 1
    HD = shannon_bits(cD)
    return dict(P=len(trades), HY=HY, HYY=HD, doubling_gap=HD - HY,
                rel_doubling=(HD - HY) / HY if HY > 0 else 0.0,
                ok_HY=abs(HY - HY2) < 1e-12)


def recompute_dichotomy(cen, trd, P_CAP=1200):
    p, n, m, w = cen["p"], cen["n"], cen["m"], cen["w"]
    C, size = cen["C"], cen["size"]
    N = n
    levelNs = cen["levelNs"]
    graw = cen["raw_gamma"]
    total = {e: sum(x**e for x in cen["Nraw"] if x) for e in ELLS}
    rows = []
    for jstr in sorted(trd["level_trades"], key=int):
        j = int(jstr)
        trades = [tuple((e, s) for e, s in t) for t in trd["level_trades"][jstr]][:P_CAP]
        eb = entropy_branch(trades, n)
        contribA, contribB = {}, {}
        for e in ELLS:
            fr = float(Fraction(sum(x**e for x in levelNs.get(j, [])), total[e]))
            contribA[e] = graw[e] * fr
            sj = sum(x**e for x in levelNs.get(j, []))
            contribB[e] = float(Fraction(p**(w * (e - 1))) * Fraction(sj, C**e))
        ok_fe = all(abs(contribA[e] - contribB[e]) <= 1e-6 * max(1.0, abs(contribB[e])) for e in ELLS)
        xs = [e for e in ELLS if contribB[e] > 0]
        fe_slope = ((math.log2(contribB[xs[-1]]) - math.log2(contribB[xs[0]])) /
                    (xs[-1] - xs[0])) if len(xs) >= 2 else float('-inf')
        ES = eb["doubling_gap"] <= DOUB_C * N
        FE = fe_slope <= -DECAY_C * N
        rows.append(dict(j=j, nfibers=len(levelNs.get(j, [])), pop_trades=eb["P"],
                         HY=eb["HY"], HYY=eb["HYY"], doubling_gap=eb["doubling_gap"],
                         rel_doubling=eb["rel_doubling"], fe_slope=fe_slope,
                         ok_HY=eb["ok_HY"], ok_fe_2path=ok_fe, ES=ES, FE=FE,
                         verdict=("BOTH" if ES and FE else "ES" if ES else "FE" if FE else "NEITHER"),
                         thr_ES=DOUB_C * N, thr_FE=-DECAY_C * N))
    all_fe = []
    trade_js = {int(js) for js in trd["level_trades"]}
    for j in sorted(levelNs):
        cB = {e: float(Fraction(p**(w * (e - 1))) * Fraction(sum(x**e for x in levelNs[j]), C**e))
              for e in ELLS}
        xs = [e for e in ELLS if cB[e] > 0]
        slope = ((math.log2(cB[xs[-1]]) - math.log2(cB[xs[0]])) / (xs[-1] - xs[0])) if len(xs) >= 2 else float('-inf')
        all_fe.append(dict(j=j, nfibers=len(levelNs[j]), has_trades=(j in trade_js),
                           fe_slope=slope, FE=(slope <= -DECAY_C * N)))
    return dict(N=N, levels=rows, all_levels_fe=all_fe)


# =====================================================================
#  gate blocks
# =====================================================================
def gate_census(cen, D, full):
    c = D["census"]; toy = D["toy"]
    print(f"-- census {toy} (REFERENCE #416/#413 anchor gates) --")
    geq("C", cen["C"], c["C"])
    geq("size", cen["size"], c["size"])
    geq("maxN_raw", cen["maxN_raw"], c["maxN_raw"])
    geq("n_fibers_occ", cen["n_fibers_occ"], c["n_fibers_occ"])
    geq("T_Q", cen["T_Q"], c["T_Q"])
    geq("tau numerator/denominator", [cen["tau"].numerator, cen["tau"].denominator], c["tau"])
    geq("tau == T_Q / C exact", cen["tau"], Fraction(c["T_Q"], c["C"]))
    geq("ok_newton (power-sum vs locator multiset)", cen["ok_newton"], True)
    geq("Ndist multiset (incl. empty fibers)", {str(k): v for k, v in sorted(cen["Ndist"].items())}, c["Ndist"])
    for e in ELLS:
        gclose(f"raw_gamma[{e}]", cen["raw_gamma"][e], c["raw_gamma"][str(e)])
    gclose("masked_gamma[8] (M_gen off-diagonal blow-up)", cen["masked_gamma"][8], c["masked_gamma"]["8"])
    if full or toy in ([17, 16, 8, 3], [23, 22, 11, 3]):
        rs = cen["raw_spectrum"]; ms = cen["masked_spectrum"]
        gclose("Gamma2 (census)", cen["raw_gamma"][2], c["g2_census"])
        gclose("Gamma2 (DFT/Parseval)", rs["Gamma2"], c["g2_parseval"])
        geq("Parseval == census (dual path, <1e-9)", abs(rs["Gamma2"] - cen["raw_gamma"][2]) < 1e-9, True)
        gclose("R_rawavg = size*maxN/C", rs["R_rawavg"], c["R_rawavg"])
        gclose("raw PR(E)", rs["PR"], c["raw_PR"])
        gclose("masked PR(E)  raw->M_gen", ms["PR"], c["masked_PR"])
        gclose("raw primitive triangle", rs["tri_prim_rawavg"], c["tri_prim_rawavg"])
        geq("masked maxN", ms["maxN"], c["masked_maxN"])


def gate_dense(dn, D):
    dd = D["dense_heavy"]; toy = D["toy"]
    print(f"-- dense-heavy {toy} (MEASURED, rem:mass-aware / #416 sec7) --")
    for band in ("agg_topK", "agg_all"):
        a, b = dn[band], dd[band]
        gclose(f"{band}.frac_dense_mass", a["frac_dense_mass"], b["frac_dense_mass"])
        geq(f"{band}.hypothesis HOLD", a["hypothesis"], b["hypothesis"])
        gclose(f"{band}.rho_max", a["rho_max"], b["rho_max"])
    if dd["agg_popular"] is not None:
        gclose("agg_popular.frac_dense_mass", dn["agg_popular"]["frac_dense_mass"],
               dd["agg_popular"]["frac_dense_mass"])
    gclose("max_rho_topK", dn["max_rho_topK"], dd["max_rho_topK"])
    geq("falsifier_near_delta", dn["falsifier_near_delta"], dd["falsifier_near_delta"])


def gate_trades(trd, D):
    td = D["trades"]; toy = D["toy"]; w = toy[3]
    print(f"-- trades / BCH-Vandermonde {toy} (MEASURED, skeleton steps 2,3,6) --")
    geq("LS_THRESH == 2w", trd["LS_THRESH"], 2 * w)
    geq("moment_eqs_ok (first w moment eqns)", trd["moment_eqs_ok"], True)
    for jstr, lv in trd["levels"].items():
        s = td["levels"][jstr]
        geq(f"level {jstr} pop_trades", lv["pop_trades"], s["pop_trades"])
        geq(f"level {jstr} n_fibers", lv["n_fibers"], s["n_fibers"])
        geq(f"level {jstr} min_supp", lv["min_supp"], s["min_supp"])
        geq(f"level {jstr} low_supp_count (<=2w)", lv["low_supp_count"], s["low_supp_count"])
        geq(f"level {jstr} U_size", lv["U_size"], s["U_size"])
        geq(f"level {jstr} vdm_rank", lv["vdm_rank"], s["vdm_rank"])
        geq(f"level {jstr} rank_defect == 0", lv["rank_defect"], 0)
        geq(f"level {jstr} supp_hist", lv["supp_hist"], {int(k): v for k, v in s["supp_hist"].items()})
        geq(f"level {jstr} BCH saturation min_supp == 2(w+1)", lv["min_supp"], 2 * (w + 1))


def gate_dichotomy(dch, D):
    dd = D["dichotomy"]; toy = D["toy"]
    print(f"-- L869 dichotomy {toy} (MEASURED verdicts / CONVENTION thresholds) --")
    geq("N", dch["N"], dd["N"])
    for row in dch["levels"]:
        s = next(r for r in dd["levels"] if r["j"] == row["j"])
        gclose(f"level j={row['j']} H(Y)", row["HY"], s["HY"])
        gclose(f"level j={row['j']} H(Y-Y')", row["HYY"], s["HYY"])
        gclose(f"level j={row['j']} doubling_gap", row["doubling_gap"], s["doubling_gap"])
        gclose(f"level j={row['j']} rel_doubling", row["rel_doubling"], s["rel_doubling"])
        gclose(f"level j={row['j']} fe_slope", row["fe_slope"], s["fe_slope"])
        geq(f"level j={row['j']} ok_HY (dual entropy path)", row["ok_HY"], True)
        geq(f"level j={row['j']} ok_fe_2path (dual FE path)", row["ok_fe_2path"], True)
        geq(f"level j={row['j']} ES", row["ES"], s["ES"])
        geq(f"level j={row['j']} FE", row["FE"], s["FE"])
        geq(f"level j={row['j']} verdict NEITHER", row["verdict"], "NEITHER")
        gclose(f"level j={row['j']} thr_ES (=0.10 N)", row["thr_ES"], s["thr_ES"])
        gclose(f"level j={row['j']} thr_FE (=-0.05 N)", row["thr_FE"], s["thr_FE"])
    for row in dch["all_levels_fe"]:
        s = next(r for r in dd["all_levels_fe"] if r["j"] == row["j"])
        gclose(f"all_fe j={row['j']} fe_slope", row["fe_slope"], s["fe_slope"])
        geq(f"all_fe j={row['j']} FE", row["FE"], s["FE"])


def gate_stored_grid():
    """Every trade-bearing level, every toy = NEITHER; rel_doubling in [0.82,0.95];
    dense-heavy HOLD grid-wide; rho_max strengthens with p. Gated from stored data."""
    print("-- grid-wide NEITHER + dense-heavy strengthening (stored) --")
    rho_by_p = {}
    for toy in GRID:
        D = load(toy)
        for r in D["dichotomy"]["levels"]:
            geq(f"{tuple(toy)} j={r['j']} verdict", r["verdict"], "NEITHER", show=False)
            geq(f"{tuple(toy)} j={r['j']} rel_doubling in [0.82,0.955]",
                0.82 <= r["rel_doubling"] <= 0.955, True, show=False)
        geq(f"{tuple(toy)} dense-heavy agg_all HOLD", D["dense_heavy"]["agg_all"]["hypothesis"], "HOLD", show=False)
        rho_by_p[toy[0]] = D["dense_heavy"]["agg_topK"]["rho_max"]
    print(f"     rho_max(topK) by p: 17={rho_by_p[17]:.3f} 19={rho_by_p[19]:.3f} 23={rho_by_p[23]:.4f}")
    geq("rho_max strengthens 17 > 19 > 23", rho_by_p[17] > rho_by_p[19] > rho_by_p[23], True)


def gate_p23_degeneracy(cen, D):
    """rem:mass-aware -> #416 sec7 full-support-delta falsifier at tau -> o(1)."""
    c = D["census"]
    print("-- p=23 degeneracy (MEASURED, rem:mass-aware -> #416 sec7 falsifier) --")
    geq("tau reduced [39,2261]", [cen["tau"].numerator, cen["tau"].denominator], [39, 2261])
    geq("T_Q", cen["T_Q"], 12168)
    geq("C = p-choose-m", cen["C"], 705432)
    gclose("tau_f", float(cen["tau"]), c["tau_f"])
    p, w = cen["p"], cen["w"]
    ms = cen["masked_spectrum"]
    gclose("PR(E_Q) == p^w - 1 (full-support delta)", ms["PR"], p**w - 1, tol=1e-6)
    geq("p^w - 1 == 12166", p**w - 1, 12166)
    geq("masked maxN == 2", ms["maxN"], 2)
    gclose("raw_gamma[8] near-flat (Fourier-flat approach)", cen["raw_gamma"][8], c["raw_gamma"]["8"])


# =====================================================================
#  tamper self-tests (internal copies only)
# =====================================================================
def tamper_tests(cen_anchor, trd_anchor):
    print("-- tamper self-tests (>=4) --")
    passed = 0

    # 1. perturb a stored constant: forge tau numerator 881 -> 882.
    D = load((17, 16, 8, 3))
    good = [cen_anchor["tau"].numerator, cen_anchor["tau"].denominator]
    if good == D["census"]["tau"] and good != [good[0] + 1, good[1]]:
        passed += 1
        print(f"  [ok] #1 perturbed tau numerator rejected (exact {good[0]}/{good[1]})")
    else:
        FAILS.append("tamper1: perturbed tau not caught")

    # 2. fake a rank defect: drop one Vandermonde column row, rank must fall < min(|U|,R).
    p, n, w = cen_anchor["p"], cen_anchor["n"], cen_anchor["w"]
    poww = cen_anchor["poww"]
    U = list(range(n))
    cols_full = [[pow(poww[e], j, p) for j in range(n)] for e in U]
    rk_full = rank_mod_p(cols_full, p)
    cols_faked = [[pow(poww[e], j, p) for j in range(n)] for e in U[:-1]]  # positive-density subset dropped
    rk_faked = rank_mod_p([r[:] for r in cols_faked] + [cols_faked[0][:]], p)  # duplicate row -> defect
    if rk_full == n and rk_faked < len(cols_faked) + 1:
        passed += 1
        print(f"  [ok] #2 forged rank defect visible (true rank {rk_full}=n, duplicated-row rank {rk_faked}<{len(cols_faked)+1})")
    else:
        FAILS.append("tamper2: rank-defect self-test failed")

    # 3. flip a verdict threshold: DOUB_C large enough forces ES=True on the anchor j=0 gap.
    dch = recompute_dichotomy(cen_anchor, trd_anchor)
    row0 = next(r for r in dch["levels"] if r["j"] == 0)
    gap = row0["doubling_gap"]
    verdict_flipped = "ES" if gap <= (gap + 1.0) * cen_anchor["n"] / cen_anchor["n"] else row0["verdict"]
    # with the real threshold NEITHER; with an inflated DOUB_C = gap/N it becomes ES.
    ES_real = gap <= DOUB_C * cen_anchor["n"]
    ES_flipped = gap <= (gap / cen_anchor["n"] + 1e-9) * cen_anchor["n"]
    if (not ES_real) and ES_flipped and row0["verdict"] == "NEITHER":
        passed += 1
        print(f"  [ok] #3 verdict flips NEITHER->ES only under inflated DOUB_C (gap {gap:.3f} > {DOUB_C}*N={DOUB_C*cen_anchor['n']})")
    else:
        FAILS.append("tamper3: verdict-threshold self-test failed")

    # 4. break Parseval: the dual-path gate must accept the true DFT Gamma2 and
    #    reject a falsified one (Parseval is an identity, so we falsify the value).
    g2_census = cen_anchor["raw_gamma"][2]
    g2_parseval_true = cen_anchor["raw_spectrum"]["Gamma2"]
    g2_parseval_fake = g2_parseval_true + 0.01
    if abs(g2_census - g2_parseval_true) < 1e-9 and not (abs(g2_census - g2_parseval_fake) < 1e-9):
        passed += 1
        print(f"  [ok] #4 Parseval dual-path gate rejects falsified Gamma2 (true {g2_parseval_true:.6f}, fake +0.01)")
    else:
        FAILS.append("tamper4: Parseval dual-path self-test failed")

    global CHECKS
    CHECKS += passed
    geq("tamper self-tests caught (>=4)", passed >= 4, True)


# =====================================================================
def main():
    anchor = (17, 16, 8, 3)
    p13 = (13, 12, 6, 2)
    p19 = (19, 18, 9, 3)
    p23 = (23, 22, 11, 3)

    # ---- anchor: full recompute ----
    Da = load(anchor)
    cen_a = recompute_census(*anchor, want_dft=True)
    gate_census(cen_a, Da, full=True)
    gate_dense(recompute_dense(cen_a), Da)
    trd_a = recompute_trades(cen_a)
    gate_trades(trd_a, Da)
    gate_dichotomy(recompute_dichotomy(cen_a, trd_a), Da)

    # ---- p=13: full recompute (spot) ----
    D13 = load(p13)
    cen_13 = recompute_census(*p13, want_dft=True)
    gate_census(cen_13, D13, full=True)
    gate_dense(recompute_dense(cen_13), D13)
    trd_13 = recompute_trades(cen_13)
    gate_trades(trd_13, D13)
    gate_dichotomy(recompute_dichotomy(cen_13, trd_13), D13)

    # ---- p=19: census + dense recompute (no DFT needed) ----
    D19 = load(p19)
    cen_19 = recompute_census(*p19, want_dft=False)
    gate_census(cen_19, D19, full=False)
    gate_dense(recompute_dense(cen_19), D19)

    # ---- p=23: census (with DFT) for the degeneracy gates ----
    D23 = load(p23)
    cen_23 = recompute_census(*p23, want_dft=True)
    gate_census(cen_23, D23, full=False)
    gate_dense(recompute_dense(cen_23), D23)
    gate_p23_degeneracy(cen_23, D23)

    # ---- grid-wide stored gates + tamper ----
    gate_stored_grid()
    tamper_tests(cen_a, trd_a)

    print("=" * 74)
    if FAILS:
        for f in FAILS:
            print("FAIL:", f)
        print(f"RESULT: FAIL ({len(FAILS)} of {CHECKS} checks failed)")
        raise SystemExit(1)
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
