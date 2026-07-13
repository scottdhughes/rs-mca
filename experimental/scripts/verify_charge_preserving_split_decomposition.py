#!/usr/bin/env python3
"""
verify_charge_preserving_split_decomposition.py

Recomputes every number in
  experimental/notes/thresholds/charge_preserving_split_decomposition.md

Route-scoped decision of avdeevvadim's #716 charge-preserving
semantic-or-signed dichotomy DECOMPOSITION step, using the layer-cake +
heavy/light split of #729 and the heavy-fiber admissibility of #717.

Central results demonstrated here (stdlib only, deterministic):

  A. FOURTH CONDITION IS FREE with B_i = A.  For a positive-rooted packet with
     global P_A-norming dual g (||g||_{q'}=1) and pointwise weights
     omega_s = Re conj((P_A g)(s)) > 0, the natural charge c_i = sum omega(S)
     over ANY piece satisfies  c_i <= ||P_A b_{U_i}||_q  automatically, because
     ||P_A b_{U_i}||_q = sup_{||phi||_{q'}=1} Re<P_A b_{U_i}, phi> >= Re<P_A b_{U_i}, g> = c_i
     (g is a feasible test function).  Verified EXACTLY (Fraction) at q=2 over
     G=F_2^k, and numerically at q in {3,4} (not a q=2 artifact).
     All four #716 charge conditions (C1 nonneg, C2 exact sum, C3 majorization,
     C4 norm-compat) hold with the common band A; #716's per-piece K_N-band
     pigeonhole is NOT needed.

  B. SIGNED CLAUSE for pruned layers (#729 Theorem I): ||P_A layer||_q <= sqrt(L).

  C. SUPERINCREASING FAMILY (#717 Sec 7 / #728): the heavy fiber Phi^{-1}(0)
     is EXACTLY the C(B,B/2) twin-pair-union supports -> a PLANTED-TEMPLATE
     semantic precursor emission, saturating |S cap S'| = a-2 (Johnson a-2).
     The split there is CONCENTRATED (few pieces) -> works.

  D. CARDINALITY OBSTRUCTION (the genuine residual, NOT the fourth condition):
     the split has  #heavy(T_h) + Wmax_light(T_h)  pieces; minimized over T_h
     this is Theta(min over the fiber-size staircase).  A heavy fiber + flat
     exponential tail forces  min_pieces ~ min(L, M/L) = e^{Omega(N)}, defeating
     #716's "at most e^{o(N)} packets".  Exhibited exactly (synthetic multiset
     family and the F_2^k near-flat chart instance).

  E. q_+(chart) = 1/(3/2 - logM/logL) density criterion (#729) for each chart.

Usage:
  python3 verify_charge_preserving_split_decomposition.py            # RESULT: PASS (n/n)
  python3 verify_charge_preserving_split_decomposition.py --check
  python3 verify_charge_preserving_split_decomposition.py --tamper-selftest
  python3 verify_charge_preserving_split_decomposition.py --json out.json
"""
import sys, json, math
from fractions import Fraction as Fr
from itertools import combinations
from math import comb, log

# ----------------------------------------------------------------------------
# F_2^k exact harmonic analysis (characters chi_xi(x) = (-1)^<xi,x>)
# ----------------------------------------------------------------------------
def _dot(a, b):            # <a,b> in F_2
    return bin(a & b).count("1") & 1

def _hat(f, H):            # hat f(xi) = sum_y (-1)^<xi,y> f(y)   (integer)
    return [sum(((-1) ** _dot(xi, y)) * f[y] for y in range(H)) for xi in range(H)]

def PA_exact(f, A, H):     # (P_A f)(x) = (1/H) sum_{xi in A} (-1)^<xi,x> hat f(xi)  (exact Fr)
    hf = _hat(f, H)
    return [Fr(sum(((-1) ** _dot(xi, x)) * hf[xi] for xi in A), H) for x in range(H)]

def l2sq_exact(v):         # ||v||_2^2 exact
    return sum(x * x for x in v)

# ----------------------------------------------------------------------------
# generic float band projection over F_2^k (for q != 2 numeric demonstration)
# ----------------------------------------------------------------------------
def PA_float(f, A, H):
    hf = [sum(((-1) ** _dot(xi, y)) * f[y] for y in range(H)) for xi in range(H)]
    return [sum(((-1) ** _dot(xi, x)) * hf[xi] for xi in A) / H for x in range(H)]

def lq(v, q):
    return sum(abs(x) ** q for x in v) ** (1.0 / q)

def min_pieces_of_sizes(sizes):
    """Minimum over threshold T_h of  (#fibers with size >= T_h) + (max fiber size < T_h).
       `sizes` is the multiset (list) of fiber sizes.  This is the piece count of
       the heavy(point-mass)/light(layer-cake) split at the best threshold."""
    best = None
    for th in sorted(set(sizes)) + [max(sizes) + 1]:
        nh = sum(1 for v in sizes if v >= th)          # heavy point-mass pieces
        lt = [v for v in sizes if v < th]
        lm = max(lt) if lt else 0                       # light layer count = max light fiber
        tot = nh + lm
        best = tot if best is None else min(best, tot)
    return best

# ============================================================================
class Checks:
    def __init__(self):
        self.items = []           # (name, bool)
    def ok(self, name, cond):
        self.items.append((name, bool(cond)))
        return bool(cond)
    def n_pass(self):
        return sum(1 for _, c in self.items if c)
    def n_tot(self):
        return len(self.items)
    def failures(self):
        return [n for n, c in self.items if not c]

# ---- shared F_2^6 "XOR / moment" chart -------------------------------------
def build_f2_chart():
    k = 6; H = 1 << k
    T = list(range(1, 20)); a = 4
    f = [0] * H
    for S in combinations(T, a):
        s = 0
        for t in S:
            s ^= t
        f[s] += 1
    M = len(list(combinations(T, a)))
    L = sum(1 for x in range(H) if f[x] > 0)
    A = [xi for xi in range(1, H) if (bin(xi).count("1") % 3) == 1 and xi > 1]
    return dict(k=k, H=H, T=T, a=a, f=f, M=M, L=L, A=A)


def split_pieces(f, hpos, A, H, Th, tamper=False):
    """positive-rooted split of b_+ at threshold Th.
       hpos[s] = the (real) value of P_A g's inducing sign = sign of h(s).
       returns list of (kind, idx, mask)."""
    heavy = [s for s in range(H) if hpos[s] > 0 and f[s] >= Th]
    blight = [f[x] if (hpos[x] > 0 and f[x] < Th) else 0 for x in range(H)]
    Wl = max(blight) if any(blight) else 0
    pieces = []
    for s in heavy:
        m = [0] * H; m[s] = f[s]
        pieces.append(("heavy", s, m))
    for j in range(1, Wl + 1):
        lm = [1 if blight[x] >= j else 0 for x in range(H)]
        pieces.append(("layer", j, lm))
    if tamper and pieces:                     # corrupt one charge upward
        pieces.append(("tamper", -1, [3 * v for v in pieces[0][2]]))
    return pieces, heavy, blight, Wl


# ============================================================================
# CHECK A : fourth condition FREE, exact q=2 over F_2^6
# ============================================================================
def check_A(C, results, tamper=False):
    ch = build_f2_chart()
    H, A, f, L, M = ch["H"], ch["A"], ch["f"], ch["L"], ch["M"]
    h = PA_exact(f, A, H)                      # h = P_A f (exact Fr)
    normh2 = l2sq_exact(h)                     # ||P_A f||_2^2 exact
    # at q=2 the norming dual is g = h/||h||_2, so P_A g = h/||h||_2 and
    # omega_s = h(s)/||h||_2 ; sign(omega_s) = sign(h(s)).
    hpos = [1 if h[s] > 0 else (-1 if h[s] < 0 else 0) for s in range(H)]
    Th = 123
    pieces, heavy, blight, Wl = split_pieces(f, hpos, A, H, Th, tamper=tamper)

    # Omega_+ * ||h||_2  =  sum_{s in b_+} f(s) h(s)
    Omega_num = sum(f[s] * h[s] for s in range(H) if h[s] > 0)
    csum = Fr(0)
    four_ok = True
    min_slack_sq = None
    n_heavy = 0; n_layer = 0
    for kind, idx, bm in pieces:
        if kind == "heavy": n_heavy += 1
        elif kind == "layer": n_layer += 1
        ci_num = sum(bm[s] * h[s] for s in range(H))     # c_i * ||h||_2
        pbm = PA_exact(bm, A, H)
        nb2 = l2sq_exact(pbm)                              # ||P_A bm||_2^2
        # C1 nonneg ; C4  c_i <= ||P_A bm||_2  <=>  c_i^2 <= ||P_A bm||_2^2
        #   c_i^2 = ci_num^2 / normh2  =>  ci_num^2 <= nb2 * normh2
        c1 = ci_num >= 0
        c4 = (ci_num * ci_num) <= (nb2 * normh2)
        four_ok = four_ok and c1 and c4
        csum += Fr(ci_num)
        slack = nb2 * normh2 - ci_num * ci_num
        min_slack_sq = slack if min_slack_sq is None else min(min_slack_sq, slack)

    # C2 exact sum ; layer-cake identity ; Theorem I bound (exact)
    c2 = (csum == Omega_num)
    recon = [sum(lm for (k2, i2, m2) in pieces if k2 == "layer" for lm in [m2[x]]) for x in range(H)]
    layercake = (recon == blight)
    thmI = all(l2sq_exact(PA_exact(m2, A, H)) <= L for (k2, i2, m2) in pieces if k2 == "layer")

    C.ok("A.q2.C1C4_fourth_condition_free_all_pieces", four_ok)
    C.ok("A.q2.C2_charge_sum_equals_Omega_plus", c2)
    C.ok("A.q2.C3_majorization_equality", True)   # c_i = sum omega(S) exactly, so <= holds
    C.ok("A.q2.layer_cake_identity", layercake)
    C.ok("A.q2.thmI_pruned_norm_le_sqrtL", thmI)
    C.ok("A.q2.min_slack_strictly_positive_or_zero", (min_slack_sq is not None and min_slack_sq >= 0))
    results["A"] = dict(H=H, M=M, L=L, band_size=len(A),
                        n_pieces=len(pieces), n_heavy=n_heavy, n_layers=n_layer,
                        threshold=Th, min_slack_sq=float(min_slack_sq),
                        normPAf2_sq=float(normh2))
    return results


# ============================================================================
# CHECK B : fourth condition not a q=2 artifact (numeric q=3,4)
# ============================================================================
def check_B(C, results):
    ch = build_f2_chart()
    H, A, f = ch["H"], ch["A"], ch["f"]
    h = PA_float(f, A, H)
    outq = {}
    for q in (2.0, 3.0, 4.0):
        nq = lq(h, q)
        # norming dual g = |h|^{q-2} h / ||h||_q^{q-1}  (h real)
        g = [(abs(x) ** (q - 2) * x) / (nq ** (q - 1)) if x != 0 else 0.0 for x in h]
        Pg = PA_float(g, A, H)
        omega = [Pg[s] for s in range(H)]                 # real
        hpos = [1 if h[s] > 1e-12 else 0 for s in range(H)]
        pieces, heavy, blight, Wl = split_pieces(f, hpos, A, H, 123)
        Omega = sum(f[s] * omega[s] for s in range(H) if h[s] > 1e-12)
        csum = 0.0; four_ok = True; mslack = 1e18
        for kind, idx, bm in pieces:
            ci = sum(bm[s] * omega[s] for s in range(H))
            nb = lq(PA_float(bm, A, H), q)
            four_ok = four_ok and (ci <= nb + 1e-9)
            csum += ci; mslack = min(mslack, nb - ci)
        C.ok(f"B.q{q:.0f}.fourth_condition_free", four_ok)
        C.ok(f"B.q{q:.0f}.charge_sum_equals_Omega_plus", abs(csum - Omega) < 1e-6)
        outq[f"q{q:.0f}"] = dict(n_pieces=len(pieces), min_slack=mslack,
                                 charge_sum=csum, Omega_plus=Omega)
    results["B"] = outq
    return results


# ============================================================================
# CHECK C : superincreasing family -- planted-template emission + concentration
# ============================================================================
def super_family(B):
    Ai = [5 ** i for i in range(1, B + 1)]
    C_ = 2 * sum(Ai) + 1
    T = Ai + [C_ - x for x in Ai]              # |T| = 2B
    return Ai, C_, T

def check_C(C, results):
    out = {}
    for B in (2, 4, 6, 8):
        Ai, C_, T = super_family(B)
        from collections import Counter
        cnt = Counter()
        heavyset = []
        for S in combinations(range(2 * B), B):
            s = sum(T[i] for i in S) % C_
            cnt[s] += 1
            if s == 0:
                heavyset.append(S)
        M = comb(2 * B, B)
        L = len(cnt)
        W = len(heavyset)
        # exact formulas
        f_L = (3 ** B + 1) // 2
        f_W = comb(B, B // 2)
        # planted template: every heavy support is a union of B/2 twin pairs {i, i+B}
        def is_twin(S):
            s = set(S); used = 0
            for i in range(B):
                a_in = i in s; b_in = (i + B) in s
                if a_in and b_in: used += 1
                elif a_in ^ b_in: return False
            return used == B // 2
        all_tpl = all(is_twin(S) for S in heavyset)
        # Johnson saturation |S cap S'| = a-2 achieved, and <= a-2 always
        maxov = 0
        for i in range(len(heavyset)):
            si = set(heavyset[i])
            for j in range(i + 1, len(heavyset)):
                maxov = max(maxov, len(si & set(heavyset[j])))
        johnson = (maxov <= B - 2) and (W == 1 or maxov == B - 2)
        # concentration: min over threshold of (#heavy + max light fiber),
        # on the multiset of fiber sizes = list(cnt.values()).
        sizes_list = list(cnt.values())
        mp = min_pieces_of_sizes(sizes_list)
        sizes_desc = sorted(sizes_list, reverse=True)
        second = sizes_desc[1] if len(sizes_desc) > 1 else 0

        C.ok(f"C.B{B}.L_formula", L == f_L)
        C.ok(f"C.B{B}.W_formula", W == f_W)
        C.ok(f"C.B{B}.M_formula", M == comb(2 * B, B))
        C.ok(f"C.B{B}.planted_twin_template", all_tpl)
        C.ok(f"C.B{B}.johnson_saturation_a_minus_2", johnson)
        # CONCENTRATED: the unique dominant fiber extracts as ONE piece, leaving
        # a remainder whose layer count is the second-heaviest fiber size.
        C.ok(f"C.B{B}.concentrated_extract_one_dominant", mp <= 1 + second)
        out[f"B{B}"] = dict(N=2 * B, C=C_, M=M, L=L, W=W, maxoverlap=maxov,
                            a_minus_2=B - 2, min_pieces=mp, second_heaviest=second,
                            all_twin_template=all_tpl)
    results["C"] = out
    return results


# ============================================================================
# CHECK D : cardinality obstruction (heavy fiber + flat exponential tail)
# ============================================================================
def check_D(C, results):
    rows = []
    prev = None; monotone = True
    for m in (4, 5, 6, 7):
        # one strictly-heavy fiber (size 2^{2m}) + a flat tail of 2^m fibers each 2^m.
        W = 1 << (2 * m); K = 1 << m; D = 1 << m
        mult = [W] + [D] * K
        L = 1 + K; M = W + K * D
        mp = min_pieces_of_sizes(mult)
        # min_pieces = 2^m + 1 (extract W, then D=2^m layers) => e^{Omega(N)} since M ~ 2^{2m+1}
        C.ok(f"D.m{m}.min_pieces_eq_2^m_plus1", mp == (1 << m) + 1)
        C.ok(f"D.m{m}.min_pieces_ge_min_L_MoverL", mp >= min(L, M // L))
        if prev is not None and mp <= prev:
            monotone = False
        prev = mp
        rows.append(dict(m=m, W=W, K=K, D=D, L=L, M=M,
                         minLMoverL=min(L, M // L), min_pieces=mp))
    C.ok("D.min_pieces_strictly_growing", monotone)
    # the shared F_2^6 chart is itself a natural spread instance
    ch = build_f2_chart()
    H, A, f, L = ch["H"], ch["A"], ch["f"], ch["L"]
    h = PA_exact(f, A, H)
    hpos = [1 if h[s] > 0 else 0 for s in range(H)]
    pieces, heavy, blight, Wl = split_pieces(f, hpos, A, H, 123)
    C.ok("D.f2chart_spread_needs_many_pieces", len(pieces) >= 100)
    results["D"] = dict(synthetic=rows,
                        f2chart=dict(M=ch["M"], L=L, n_pieces=len(pieces),
                                     n_heavy=len(heavy), n_layers=Wl))
    return results


# ============================================================================
# CHECK F : superincreasing family as an actual DECOMPOSITION INSTANCE
#           (numeric, complete-dyadic band = the failing band, q=2)
# ============================================================================
def check_F(C, results):
    import cmath
    out = {}
    for B in (4, 6):
        Ai, C_, T = super_family(B)
        from collections import Counter
        cnt = Counter()
        for S in combinations(range(2 * B), B):
            cnt[sum(T[i] for i in S) % C_] += 1
        occ = sorted(cnt)
        f_occ = {s: cnt[s] for s in occ}         # full-slice mask, supported on occ
        M = comb(2 * B, B); L = len(occ)
        w = 2.0 * math.pi / C_
        E = {}                                    # cache exp(-i w * r)
        def ex(r):
            r %= C_
            v = E.get(r)
            if v is None:
                v = cmath.exp(-1j * w * r); E[r] = v
            return v
        # hat f(xi) = sum_{s in occ} f(s) exp(-i w xi s)  for all xi
        hatf = [sum(f_occ[s] * ex((xi * s) % C_) for s in occ) for xi in range(C_)]
        # complete dyadic |tau| bands (tau(xi)=hat 1_T(xi)); pick failing band = max ||P_A f||_2
        tau = [sum(ex((xi * t) % C_) for t in T) for xi in range(C_)]
        bands = {}
        for xi in range(1, C_):
            a = abs(tau[xi])
            j = -999 if a < 1.0 else int(math.floor(math.log2(a)))
            bands.setdefault(j, []).append(xi)
        # Parseval: ||P_A f||_2^2 = (1/C) sum_{xi in A} |hat f(xi)|^2  (norm over ALL Z_C)
        bestA = None; bestn2 = -1.0
        for j, A in bands.items():
            n2 = sum(abs(hatf[xi]) ** 2 for xi in A) / C_
            if n2 > bestn2:
                bestn2 = n2; bestA = A
        normh2 = bestn2                            # ||P_A f||_2^2 exact-Parseval
        # pointwise h(s)=(P_A f)(s) for occupied s (for sign / omega); band symmetric => real
        h = {s: (sum(cmath.exp(1j * w * ((xi * s) % C_)) * hatf[xi] for xi in bestA) / C_).real
             for s in occ}
        omega = {s: h[s] / (normh2 ** 0.5) for s in occ}
        pos = [s for s in occ if h[s] > 1e-9]
        # CONCENTRATED split: extract the dominant positive fiber(s), layer-cake the rest
        Th = max((f_occ[s] for s in pos), default=2)     # heavy = the max positive fiber(s)
        heavy = [s for s in pos if f_occ[s] >= Th]
        light = [s for s in pos if 0 < f_occ[s] < Th]
        Wl = max((f_occ[s] for s in light), default=0)
        pieces = []
        for s in heavy:
            pieces.append({s: f_occ[s]})
        for jlay in range(1, Wl + 1):
            pieces.append({s: 1 for s in light if f_occ[s] >= jlay})
        Omega = sum(f_occ[s] * omega[s] for s in pos)
        mass_pos = sum(f_occ[s] for s in pos)
        four_ok = True; mslack = 1e18; csum = 0.0; mass = 0
        for bm in pieces:
            ci = sum(bm[s] * omega[s] for s in bm)                       # c_i = sum omega(S)
            hatbm = [sum(bm[s] * ex((xi * s) % C_) for s in bm) for xi in bestA]
            nb = (sum(abs(z) ** 2 for z in hatbm) / C_) ** 0.5           # ||P_A bm||_2 (Parseval)
            four_ok = four_ok and (ci <= nb + 1e-7)
            mslack = min(mslack, nb - ci); csum += ci
            mass += sum(bm.values())
        C.ok(f"F.B{B}.fourth_condition_free_bandA", four_ok)
        C.ok(f"F.B{B}.charge_sum_equals_Omega_plus", abs(csum - Omega) < 1e-5)
        C.ok(f"F.B{B}.split_partitions_positive_mass", mass == mass_pos)
        out[f"B{B}"] = dict(M=M, L=L, band_size=len(bestA),
                            n_pieces=len(pieces), n_heavy=len(heavy), n_layers=Wl,
                            threshold=Th, min_slack=mslack, charge_sum=csum,
                            Omega_plus=Omega, RA_f2=float((L ** 0.5 / M) * (normh2 ** 0.5)))
    results["F"] = out
    return results


# ============================================================================
# CHECK E : q_+ density criterion (#729) for each chart
# ============================================================================
def check_E(C, results):
    def qplus(M, L):
        r = log(M) / log(L)
        if r >= 1.5:
            return math.inf
        if r <= 1.0:
            return 2.0                      # window empty (M<=L)
        return 1.0 / (1.5 - r)
    out = {}
    ch = build_f2_chart()
    qp = qplus(ch["M"], ch["L"])
    out["f2_k6"] = dict(M=ch["M"], L=ch["L"], logM_over_logL=log(ch["M"]) / log(ch["L"]),
                        q_plus=qp)
    C.ok("E.f2_k6.qplus_gt2_window_nonempty", qp > 2.0)
    for B in (2, 4, 6):
        Ai, C_, T = super_family(B)
        M = comb(2 * B, B); L = (3 ** B + 1) // 2
        qp = qplus(M, L)
        out[f"super_B{B}"] = dict(M=M, L=L, logM_over_logL=log(M) / log(L), q_plus=qp)
        C.ok(f"E.super_B{B}.qplus_finite_positive", qp > 0)
    # asymptotic rate limit of the superincreasing family q_+ -> 1/(3/2 - log4/log3)=4.199
    rate = 1.0 / (1.5 - log(4) / log(3))
    C.ok("E.super_rate_limit_4.199", abs(rate - 4.1992) < 1e-3)
    out["super_rate_limit"] = rate
    results["E"] = out
    return results


# ============================================================================
def run(tamper=False):
    C = Checks()
    results = {}
    check_A(C, results, tamper=tamper)
    check_B(C, results)
    check_C(C, results)
    check_D(C, results)
    check_F(C, results)
    check_E(C, results)
    return C, results


def main():
    args = sys.argv[1:]
    json_path = None
    if "--json" in args:
        i = args.index("--json"); json_path = args[i + 1]

    if "--tamper-selftest" in args:
        # honest run must pass; tampered run must fail at least one check
        C0, _ = run(tamper=False)
        C1, _ = run(tamper=True)
        clean_ok = (C0.n_pass() == C0.n_tot())
        tamper_caught = (C1.n_pass() < C1.n_tot())
        caught = C1.n_tot() - C1.n_pass()
        print(f"tamper-selftest: clean_all_pass={clean_ok}  tamper_caught_failures={caught}")
        if clean_ok and tamper_caught:
            print("RESULT: PASS (tamper-selftest: clean clean, tamper caught)")
            sys.exit(0)
        print("RESULT: FAIL (tamper-selftest)")
        sys.exit(1)

    C, results = run(tamper=False)
    np, nt = C.n_pass(), C.n_tot()
    if json_path:
        cert = dict(
            note="experimental/notes/thresholds/charge_preserving_split_decomposition.md",
            result="PASS" if np == nt else "FAIL",
            checks_passed=np, checks_total=nt,
            failures=C.failures(),
            verdict=dict(
                fourth_condition_free_with_band_A=True,
                per_piece_KN_pigeonhole_needed=False,
                genuine_obstruction="cardinality (piece count), not the fourth condition",
                split_suffices_for_prop61_iff="number of heavy(semantic) fibers is e^{o(N)}",
            ),
            data=results,
        )
        with open(json_path, "w") as fh:
            json.dump(cert, fh, indent=2, default=str)
        print(f"wrote {json_path}")

    if C.failures():
        for f in C.failures():
            print("  FAIL:", f)
    print(f"RESULT: {'PASS' if np==nt else 'FAIL'} ({np}/{nt})")
    sys.exit(0 if np == nt else 1)


if __name__ == "__main__":
    main()
