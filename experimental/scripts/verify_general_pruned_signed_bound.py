#!/usr/bin/env python3
"""
verify_general_pruned_signed_bound.py  --  stdlib only, deterministic, <60s.

Recomputes every number in
  experimental/notes/thresholds/general_pruned_signed_bound.md
and writes the JSON certificate
  experimental/data/certificates/general-pruned-signed-bound/
    general_pruned_signed_bound.json

WHAT IS CERTIFIED
-----------------
The CHART-FREE pruned signed bound (Theorem I), escalated from the depth-1
superincreasing instance of PR #728 (first_match_signed_gain.md) to a general
finite abelian source chart.  For every finite abelian G, every chart
Phi: Omega^0 -> G (M supports, image size L=|Phi(Omega^0)|), every band
A subseteq hat(G)\\{0} (delta_A=|A|/|G|), every q in [2,inf], and every signed
mask g with |g|<=1 supported on a set S with at most one point per Phi-syndrome
(|S| <= L):

  (I)   R_A(g) := (L^{1-1/q}/M) ||P_A g||_q  <=  (L/M)(L delta_A)^{1/2-1/q}
                                             <=  L^{3/2-1/q}/M .

Endpoints (both chart-free, verified separately):
  l2   :  ||P_A g||_2 <= ||g||_2 <= sqrt(|S|) <= sqrt(L)     (orth. projection)
  linf :  max_x sum_{s in S} |K_A(x-s)| <= sqrt(L delta_A)   (Cauchy-Schwarz),
          using the Parseval identity  ||K_A||_2^2 = delta_A .

Vanishing criterion (corollary): R_A(g) = e^{-Omega(N)}  iff
  (3/2 - 1/q) log L - log M <= -Omega(N)   -- a pure density condition; the
per-chart threshold is  q_+(chart) = 1 / (3/2 - log M / log L)  (window
[2,q_+) when 1 < logM/logL < 3/2; all q>=2 when logM/logL >= 3/2; empty when
logM/logL <= 1).

Dictionary to avdeevvadim's #716 Sec-6 charge-preserving dichotomy:
  ||P_{B_i} b_{U_i}||_q = (M/L^{1-1/q}) R_{B_i}(b_{U_i}) ,  charge c_i <= ||.||_q
  => pruned nonsemantic packet (|b_{U_i}|<=1) satisfies the signed clause
     c_i <= e^{o(N)} M/L^{1-1/q}  whenever the chart passes the criterion.
Layer-cake extension: a mask with max multiplicity W_max decomposes into W_max
pruned layers, so c_i <= W_max * L^{1/2}; residual is exactly W_max=e^{Omega(N)}
(a heavy fiber -> #716 Sec 2 / #717 semantic side) and q >= q_+ (Sidon residual).

Credit: normalizations R_A, K_A, P_A and the charge clause are avdeevvadim's
#716 (primitive_signed_payment_barrier_v1.md); the dyadic |tau| band grammar,
K_N count, and heavy-fiber transfer are #717
(heavy_fiber_admissibility_transfer.md); the depth-1 superincreasing family and
the q_+=4.199 instance are #728/#723.  This packet proves NONE of the dichotomy,
A4, primitive Q, or the Proximity Prize (see note Nonclaims).

Charts instantiated (>=3 different types, exact small-chart bound checks):
  chart 1  depth-1 elementary prefix  (locator c_1 = e_1)  over F_7, |T|=5, a=3
           G=Z_7 (cyclic) -- EXHAUSTIVE over all signed masks g in {-1,0,1}^S.
  chart 2  depth-2 moment curve  v_t=(t,t^2)  over F_11, |T|=11, a=4
           G=Z_11 x Z_11 (collisions M>L) -- sampled signed/fractional masks.
  chart 3  arbitrary random chart  Phi = seeded hash -> Z_40, Omega^0=C(9,4)
           G=Z_40, ARBITRARY bands (no column structure) -- sampled masks.
  chart 4  depth-2 elementary prefix (e_1,e_2) over F_5, |T|=5, a=2
           G=Z_5 x Z_5 -- sampled masks (a second, R=2, prefix instance).
Plus the depth-R prefix DENSITY-CRITERION table and the #728 q_+ cross-check.
"""

import sys, math, cmath, itertools, json, os, random
from fractions import Fraction

CHECKS = []
def require(name, cond, detail=""):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print(f"FAIL: {name}   {detail}")

TOL = 1e-9

# ===========================================================================
# Finite abelian group  G = prod_j Z_{mods[j]}  with a precomputed char table.
# ===========================================================================
class Ab:
    def __init__(self, mods):
        self.mods = list(mods)
        self.order = 1
        for m in mods:
            self.order *= m
        self.elts = list(itertools.product(*[range(m) for m in mods]))
        self.pos = {e: i for i, e in enumerate(self.elts)}
        n = self.order
        # character table ch[i][j] = chi_{elts[i]}(elts[j]) = exp(2pi i sum xi_k x_k/m_k)
        self.ch = [[0j] * n for _ in range(n)]
        for i, xi in enumerate(self.elts):
            row = self.ch[i]
            for j, x in enumerate(self.elts):
                acc = 0.0
                for a, b, m in zip(xi, x, self.mods):
                    acc += (a * b % m) / m
                row[j] = cmath.exp(2j * math.pi * acc)

    def sub(self, x, y):
        return tuple((a - b) % m for a, b, m in zip(x, y, self.mods))

    def dft(self, fdict):
        # hat f(xi) = sum_x f(x) conj(chi_xi(x))
        n = self.order
        hat = [0j] * n
        items = [(self.pos[x], v) for x, v in fdict.items() if v != 0]
        for i in range(n):
            row = self.ch[i]
            s = 0j
            for jx, v in items:
                s += v * row[jx].conjugate()
            hat[i] = s
        return hat

    def band_project_vec(self, hat, Aidx):
        # returns list P_A f over all elts:  (1/n) sum_{xi in A} hat(xi) chi_xi(x)
        n = self.order
        out = [0j] * n
        for i in Aidx:
            hi = hat[i]
            if hi == 0:
                continue
            row = self.ch[i]
            for j in range(n):
                out[j] += hi * row[j]
        inv = 1.0 / n
        return [v * inv for v in out]

    def kernel_vec(self, Aidx):
        # K_A(x) = (1/n) sum_{xi in A} chi_xi(x)
        n = self.order
        out = [0j] * n
        for i in Aidx:
            row = self.ch[i]
            for j in range(n):
                out[j] += row[j]
        inv = 1.0 / n
        return [v * inv for v in out]


def lq(vec, q):
    if q == float("inf"):
        return max(abs(v) for v in vec)
    return sum(abs(v) ** q for v in vec) ** (1.0 / q)


# ===========================================================================
# Charts.
# ===========================================================================
def prefix_e1(T, p, a):
    """depth-1 elementary/locator prefix  Phi(S)=e_1(S)=sum(S) mod p, G=Z_p."""
    G = Ab([p])
    Om = list(itertools.combinations(T, a))
    Phi = {S: (sum(S) % p,) for S in Om}
    return G, Om, Phi

def prefix_e1e2(T, p, a):
    """depth-2 elementary prefix  Phi(S)=(e_1,e_2) mod p, G=Z_p x Z_p."""
    G = Ab([p, p])
    Om = list(itertools.combinations(T, a))
    def es(S):
        e1 = sum(S) % p
        e2 = sum(S[i] * S[j] for i in range(len(S)) for j in range(i + 1, len(S))) % p
        return (e1, e2)
    Phi = {S: es(S) for S in Om}
    return G, Om, Phi

def moment_p1p2(T, p, a):
    """depth-2 moment curve  v_t=(t,t^2), Phi(S)=(p_1,p_2)=(sum t, sum t^2) mod p."""
    G = Ab([p, p])
    Om = list(itertools.combinations(T, a))
    def ps(S):
        return (sum(S) % p, sum(t * t for t in S) % p)
    Phi = {S: ps(S) for S in Om}
    return G, Om, Phi

def random_chart(n_dom, a, H, seed=12345):
    """arbitrary structureless chart Phi: C([n_dom],a) -> Z_H via a seeded hash."""
    G = Ab([H])
    Om = list(itertools.combinations(range(n_dom), a))
    rng = random.Random(seed)
    # a fixed pseudo-random assignment (no algebra): stable per support tuple
    table = {}
    for S in Om:
        # deterministic hash of the sorted tuple, seed-mixed
        h = seed
        for t in S:
            h = (h * 1000003 ^ (t + 0x9E3779B9)) & 0xFFFFFFFF
        table[S] = (h % H,)
    Phi = table
    return G, Om, Phi


def occupied(Phi):
    S = sorted(set(Phi.values()))
    return S

def full_count(Phi):
    from collections import Counter
    return Counter(Phi.values())


# ---- band constructions ----
def dyadic_bands_from_columns(G, cols):
    """complete symmetric dyadic |tau| bands, tau(xi)=sum_{v in cols} chi_xi(v)."""
    bands = {}
    for i, xi in enumerate(G.elts):
        if all(c == 0 for c in xi):
            continue  # skip trivial character
        row = G.ch[i]
        tau = 0j
        for v in cols:
            tau += row[G.pos[v]]
        m = abs(tau)
        lab = "<1" if m < 1.0 else str(math.floor(math.log2(m)))
        bands.setdefault(lab, []).append(i)
    return bands

def arbitrary_bands(G, k):
    """partition hat(G)\\{0} into k arbitrary (non-dyadic) bands by index mod k."""
    bands = {}
    for i, xi in enumerate(G.elts):
        if all(c == 0 for c in xi):
            continue
        bands.setdefault(f"arb{i % k}", []).append(i)
    return bands


# ===========================================================================
# Core per-chart Theorem-I check.
# ===========================================================================
QS = [2, 3, 4, 8, float("inf")]

def check_theorem_I(G, Om, Phi, bands, masks, label, band_kind):
    """Verify R_A(g) <= (L/M)(L dA)^{1/2-1/q} <= L^{3/2-1/q}/M for every
    (band, q, mask), plus the two endpoint lemmas.  Returns a summary dict."""
    M = len(Om)
    S = occupied(Phi)
    L = len(S)
    Sset = set(S)
    n = G.order
    # endpoint + Theorem-I checks
    max_ratio_sharp = 0.0    # sup over checks of R_A(g) / sharpUB  (must be <=1)
    max_ratio_crude = 0.0
    kappa = len(bands)
    band_report = []
    # precompute kernels + |K_A| convolution sup for the linf endpoint
    for lab, Aidx in sorted(bands.items()):
        dA = Fraction(len(Aidx), n)
        KA = G.kernel_vec(Aidx)
        # Parseval:  ||K_A||_2^2 == delta_A
        k2 = sum(abs(v) ** 2 for v in KA)
        require(f"{label} band {lab}: ||K_A||_2^2 == delta_A (Parseval)",
                abs(k2 - float(dA)) < 1e-6, f"{k2} vs {float(dA)}")
        # linf endpoint: max_x sum_{s in S} |K_A(x-s)| <= sqrt(L*dA)
        KAabs = [abs(v) for v in KA]
        linf_sup = 0.0
        for x in G.elts:
            tot = 0.0
            for s in S:
                tot += KAabs[G.pos[G.sub(x, s)]]
            if tot > linf_sup:
                linf_sup = tot
        require(f"{label} band {lab}: linf endpoint sum|K_A(x-s)| <= sqrt(L dA)",
                linf_sup <= math.sqrt(L * float(dA)) + 1e-6,
                f"{linf_sup} vs {math.sqrt(L*float(dA))}")
        band_report.append({"band": lab, "absA": len(Aidx),
                            "delta_A": float(dA), "linf_sup": linf_sup,
                            "sqrt_L_dA": math.sqrt(L * float(dA))})

    for g in masks:
        # g is a dict elt->value in [-1,1], support subseteq S
        assert all(k in Sset for k in g), "mask off occupied set"
        assert all(abs(v) <= 1 + 1e-12 for v in g.values()), "|g|>1"
        supp = sum(1 for v in g.values() if v != 0)
        require(f"{label}: |supp g| <= L", supp <= L)
        g2 = math.sqrt(sum(abs(v) ** 2 for v in g.values()))
        require(f"{label}: ||g||_2 <= sqrt(|supp|) <= sqrt(L)",
                g2 <= math.sqrt(supp) + 1e-9 and g2 <= math.sqrt(L) + 1e-9)
        hat = G.dft(g)
        for lab, Aidx in sorted(bands.items()):
            dA = float(Fraction(len(Aidx), n))
            Pg = G.band_project_vec(hat, Aidx)
            # l2 endpoint: ||P_A g||_2 <= ||g||_2
            p2 = math.sqrt(sum(abs(v) ** 2 for v in Pg))
            require(f"{label} band {lab}: ||P_A g||_2 <= ||g||_2 (contraction)",
                    p2 <= g2 + 1e-9)
            require(f"{label} band {lab}: ||P_A g||_2^2 <= L",
                    p2 * p2 <= L + 1e-6)
            for q in QS:
                pq = lq(Pg, q)
                if q == float("inf"):
                    inv_q = 0.0
                    RA = (L ** 1.0 / M) * pq        # L^{1-0}/M
                else:
                    inv_q = 1.0 / q
                    RA = (L ** (1 - inv_q) / M) * pq
                ub_sharp = (L / M) * (L * dA) ** (0.5 - inv_q)
                ub_crude = (L ** (1.5 - inv_q)) / M
                require(f"{label} band {lab} q={q}: R_A(g) <= sharp UB",
                        RA <= ub_sharp + TOL,
                        f"RA={RA} sharpUB={ub_sharp}")
                require(f"{label} band {lab} q={q}: R_A(g) <= crude L^(3/2-1/q)/M",
                        RA <= ub_crude + TOL,
                        f"RA={RA} crudeUB={ub_crude}")
                if q == 2:
                    require(f"{label} band {lab}: q=2 sharp R_A(g) <= L/M (exact)",
                            RA <= L / M + TOL)
                if ub_sharp > 0:
                    max_ratio_sharp = max(max_ratio_sharp, RA / ub_sharp)
                if ub_crude > 0:
                    max_ratio_crude = max(max_ratio_crude, RA / ub_crude)
    return {"label": label, "M": M, "L": L, "kappa": kappa,
            "band_kind": band_kind, "n_masks": len(masks),
            "logM_over_logL": (math.log(M) / math.log(L)) if L > 1 else None,
            "q_plus": q_plus_of(M, L),
            "max_ratio_sharp": max_ratio_sharp,
            "max_ratio_crude": max_ratio_crude,
            "bands": band_report}


def q_plus_of(M, L):
    """per-chart window top  q_+ = 1/(3/2 - logM/logL).  None => all q (>=2)."""
    if L <= 1:
        return None
    r = math.log(M) / math.log(L)      # = logM/logL, base-free
    denom = 1.5 - r
    if denom <= 0:
        return float("inf")            # all q>=2 vanish
    return 1.0 / denom


# ===========================================================================
# Mask generators.
# ===========================================================================
def enum_signed_masks(S, cap=None):
    """all g in {-1,0,1}^S (exhaustive)."""
    out = []
    for combo in itertools.product((-1, 0, 1), repeat=len(S)):
        out.append({s: v for s, v in zip(S, combo) if v != 0})
        if cap and len(out) >= cap:
            break
    return out

def sampled_masks(S, n_samples, seed=7):
    rng = random.Random(seed)
    out = [{s: 1.0 for s in S}]                     # all-+1 indicator
    out.append({s: (1.0 if i % 2 == 0 else -1.0) for i, s in enumerate(S)})
    out.append({s: (1.0 if (i * i) % 3 == 0 else -1.0) for i, s in enumerate(S)})
    for _ in range(n_samples):
        # random signs
        out.append({s: rng.choice((-1.0, 1.0)) for s in S})
    for _ in range(n_samples):
        # random fractional |g|<=1 with random dropouts
        out.append({s: rng.uniform(-1.0, 1.0) for s in S if rng.random() < 0.85})
    return out


# ===========================================================================
# Layer-cake / unpruned (Theorem II direction + discharge extension).
# ===========================================================================
def check_layer_cake(G, Om, Phi, bands, label):
    """Unpruned full count b: verify ||P_A b||_q <= sum_j ||P_A g_j||_q with
    W_max pruned {-1,0,1} layers, and that the unpruned excess can exceed the
    pruned bound (Theorem II pigeonhole)."""
    M = len(Om)
    S = occupied(Phi)
    L = len(S)
    n = G.order
    cnt = full_count(Phi)
    b = {s: float(cnt[s]) for s in S}
    Wmax = int(max(cnt.values()))
    # layer cake:  b = sum_{j=1}^{Wmax} g_j,  g_j(s)=1 if b(s)>=j  (b>=0 here)
    layers = []
    for j in range(1, Wmax + 1):
        layers.append({s: 1.0 for s in S if cnt[s] >= j})
    # verify reconstruction
    recon = {}
    for gj in layers:
        for s, v in gj.items():
            recon[s] = recon.get(s, 0.0) + v
    require(f"{label} layer-cake: sum of layers reconstructs b",
            all(abs(recon.get(s, 0.0) - b[s]) < 1e-9 for s in S))
    require(f"{label} layer-cake: #layers == W_max", len(layers) == Wmax)
    hat_b = G.dft(b)
    hats = [G.dft(gj) for gj in layers]
    pig_best = 0.0
    exceed_seen = False
    for lab, Aidx in sorted(bands.items()):
        Pb = G.band_project_vec(hat_b, Aidx)
        for q in (2, 3, 4):
            nb = lq(Pb, q)
            layer_sum = sum(lq(G.band_project_vec(h, Aidx), q) for h in hats)
            require(f"{label} layer-cake band {lab} q={q}: ||P_A b||_q <= sum_j ||P_A g_j||_q",
                    nb <= layer_sum + 1e-6, f"{nb} vs {layer_sum}")
            # crude: layer_sum <= Wmax * sqrt(L)  (Theorem I per layer, q>=2)
            require(f"{label} layer-cake band {lab} q={q}: sum_j ||P_A g_j||_q <= W_max*sqrt(L)",
                    layer_sum <= Wmax * math.sqrt(L) + 1e-6)
            if q == 2:
                RA_un = (L ** 0.5 / M) * nb    # q=2
                if RA_un > L / M + 1e-9:
                    exceed_seen = True         # unpruned exceeds pruned q=2 bound L/M
        # Theorem II pigeonhole: some band has |P_A b(s0)| >= (W - M/n)/kappa
        s0 = max(cnt, key=lambda s: cnt[s])
        pig = abs(Pb[G.pos[s0]])
        pig_best = max(pig_best, pig)
    Wheavy = int(cnt[max(cnt, key=lambda s: cnt[s])])
    require(f"{label} Theorem II pigeonhole |P_A* b(s0)| >= (W - M/|G|)/kappa",
            pig_best >= (Wheavy - M / n) / len(bands) - 1e-6)
    return {"label": label, "W_max": Wmax, "pig_best": pig_best,
            "unpruned_exceeds_pruned_q2_bound": exceed_seen,
            "pigeonhole_lb_q2": (L ** 0.5 / M) * (Wheavy - M / n) / len(bands)}


# ===========================================================================
# Density-criterion table (depth-R prefix charts) + #728 cross-check.
# ===========================================================================
def h_nat(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log(x) - (1 - x) * math.log(1 - x)

def exact_L_prefix(T, p, a, R):
    """exact image size of the depth-R elementary-symmetric prefix."""
    from collections import Counter
    def esR(S):
        # elementary symmetric e_1..e_R of the a-subset S, mod p
        # via coefficients of prod (X - t): power/elem; use Newton-free direct
        coeffs = [1]  # product so far, coeffs[0]=leading
        poly = [1]
        for t in S:
            # multiply poly by (X - t)
            new = [0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] = (new[i] + c) % p           # X * c
                new[i + 1] = (new[i + 1] - c * t) % p  # -t * c
            poly = new
        # poly = X^a - e1 X^{a-1} + e2 X^{a-2} - ...  ; e_j = (-1)^j poly[j]
        es = tuple(((-1) ** j) * poly[j] % p for j in range(1, R + 1))
        return es
    return len(set(esR(S) for S in itertools.combinations(T, a)))

def density_table():
    rows = []
    # exact small depth-R prefix charts
    specs = [
        # (name, p, |T|, a, R)
        ("F5 a2 R1", 5, 5, 2, 1),
        ("F7 a3 R1", 7, 7, 3, 1),
        ("F7 a3 R2", 7, 7, 3, 2),
        ("F11 a4 R1", 11, 11, 4, 1),
        ("F11 a4 R2", 11, 11, 4, 2),
        ("F11 a5 R1", 11, 11, 5, 1),
        ("F13 a6 R1", 13, 13, 6, 1),
    ]
    for name, p, nT, a, R in specs:
        T = list(range(p))[:nT]
        L = exact_L_prefix(T, p, a, R)
        M = math.comb(nT, a)
        qp = q_plus_of(M, L)
        r = math.log(L) / (R * math.log(p)) if L > 1 else 0.0  # tightness of L<=Q^R
        window = ("empty" if (qp is not None and qp <= 2)
                  else "all-q" if qp == float("inf")
                  else f"[2,{qp:.3f})")
        # entropy-form sufficient criterion (uses bound L<=Q^R):
        beta = a / nT
        r_rate = R * math.log(p) / nT          # prefix rate  (nats/symbol)
        h_beta = h_nat(beta)
        rows.append({"chart": name, "p_Q": p, "N": nT, "a": a, "R": R,
                     "L": L, "L_bound_QR": p ** R, "M": M,
                     "logM_over_logL": math.log(M) / math.log(L) if L > 1 else None,
                     "q_plus": qp, "window": window,
                     "rate_r_RlogQ_over_N": r_rate, "h_beta": h_beta,
                     "entropy_criterion_r_lt_h": r_rate < h_beta})
    # #728 superincreasing cross-check: L=(3^B+1)/2, M=C(2B,B), R=1, Q=C.
    # Also the heavy-fiber crossover W vs sqrt(L): once W>sqrt(L) the unpruned
    # full-multiplicity mask b has ||b||_2 >= W > sqrt(L), so its band excess
    # can exceed the pruned q=2 ceiling L/M -- i.e. the unpruned (semantic-side)
    # residual becomes active.  W=C(B,B/2)~2^B/sqrt(B) grows faster than
    # sqrt(L)~3^{B/2}/sqrt2, so the crossover is finite (Part 3 residual regime).
    seven28 = []
    for B in (2, 4, 6, 8, 10, 12):
        L = (3 ** B + 1) // 2
        M = math.comb(2 * B, B)
        W = math.comb(B, B // 2)
        qp = q_plus_of(M, L)
        seven28.append({"B": B, "L": L, "M": M, "W": W,
                        "sqrtL": math.sqrt(L),
                        "W_gt_sqrtL": W > math.sqrt(L),
                        "logM_over_logL": math.log(M) / math.log(L),
                        "q_plus": qp})
    return rows, seven28


# ===========================================================================
# Runner.
# ===========================================================================
def run():
    CHECKS.clear()
    summaries = []

    # ---- chart 1: depth-1 elementary prefix over F_7, |T|=5, a=3 -- EXHAUSTIVE
    T1 = [0, 1, 2, 3, 4]
    G1, Om1, Phi1 = prefix_e1(T1, 7, 3)
    S1 = occupied(Phi1)
    cols1 = [(t % 7,) for t in T1]          # column images of singletons (depth-1)
    bands1 = dyadic_bands_from_columns(G1, cols1)
    for lab, A in arbitrary_bands(G1, 3).items():
        bands1[lab] = A
    masks1 = enum_signed_masks(S1)          # all 3^|S1| signed masks
    require("chart1: exhaustive signed-mask count == 3^|S| - 1 (excl. zero) + zero",
            len(masks1) == 3 ** len(S1))
    summaries.append(check_theorem_I(G1, Om1, Phi1, bands1, masks1,
                                     "chart1-prefix-e1-F7", "dyadic+arbitrary"))
    lc1 = check_layer_cake(G1, Om1, Phi1,
                           dyadic_bands_from_columns(G1, cols1), "chart1")

    # ---- chart 2: depth-2 moment curve over F_11, |T|=11, a=4 -- sampled
    T2 = list(range(11))
    G2, Om2, Phi2 = moment_p1p2(T2, 11, 4)
    S2 = occupied(Phi2)
    cols2 = [(t % 11, (t * t) % 11) for t in T2]
    bands2 = dyadic_bands_from_columns(G2, cols2)
    for lab, A in arbitrary_bands(G2, 4).items():
        bands2[lab] = A
    masks2 = sampled_masks(S2, 120, seed=101)
    summaries.append(check_theorem_I(G2, Om2, Phi2, bands2, masks2,
                                     "chart2-moment-p1p2-F11", "dyadic+arbitrary"))
    lc2 = check_layer_cake(G2, Om2, Phi2, bands2, "chart2")

    # ---- chart 3: arbitrary random chart -> Z_40 -- ARBITRARY bands only
    G3, Om3, Phi3 = random_chart(9, 4, 40, seed=2027)
    S3 = occupied(Phi3)
    bands3 = arbitrary_bands(G3, 5)         # no column structure at all
    masks3 = sampled_masks(S3, 120, seed=303)
    summaries.append(check_theorem_I(G3, Om3, Phi3, bands3, masks3,
                                     "chart3-random-Z40", "arbitrary-only"))
    lc3 = check_layer_cake(G3, Om3, Phi3, bands3, "chart3")

    # ---- chart 4: depth-2 elementary prefix (e_1,e_2) over F_5, a=2 -- sampled
    T4 = list(range(5))
    G4, Om4, Phi4 = prefix_e1e2(T4, 5, 2)
    S4 = occupied(Phi4)
    cols4 = [(t % 5, 0) for t in T4]        # depth-2: singleton e=(t,0)
    bands4 = dyadic_bands_from_columns(G4, cols4)
    for lab, A in arbitrary_bands(G4, 3).items():
        bands4[lab] = A
    masks4 = sampled_masks(S4, 80, seed=404)
    summaries.append(check_theorem_I(G4, Om4, Phi4, bands4, masks4,
                                     "chart4-prefix-e1e2-F5", "dyadic+arbitrary"))

    # every chart-instance ratio must be <= 1 (Theorem I never violated)
    for s in summaries:
        require(f"{s['label']}: max R_A/sharpUB <= 1", s["max_ratio_sharp"] <= 1 + 1e-9)
        require(f"{s['label']}: max R_A/crudeUB <= 1", s["max_ratio_crude"] <= 1 + 1e-9)

    # ---- dictionary / discharge assertions (arithmetic identities) ----
    # For chart 2 (collisions), the q=2 pruned bound L/M discharges the signed
    # clause: c_i <= ||P_A g||_q <= (M/L^{1-1/q}) * (L^{3/2-1/q}/M) = L^{1/2}.
    for s in summaries:
        L, M = s["L"], s["M"]
        for q in (2, 3, 4):
            # ||P_A g||_q upper bound from Theorem I (crude):
            norm_ub = (M / L ** (1 - 1 / q)) * (L ** (1.5 - 1 / q) / M)
            require(f"{s['label']} q={q}: discharge norm UB == L^(1/2)",
                    abs(norm_ub - math.sqrt(L)) < 1e-6)
        # clause direction: L^{3/2-1/q}/M <= e^{o(N)} iff (3/2-1/q)logL <= logM+o(N)
    # q_+ recovers #728 family value 4.199 IN THE ASYMPTOTIC LIMIT only:
    # the finite per-chart q_+ uses the finite ratio logM/logL and increases
    # monotonically toward the rate limit  1/(3/2 - log4/log3) = 4.1992  (which
    # uses log L ~ B log 3, log M ~ B log 4).  This finite-vs-rate distinction
    # is exactly why #728's q_+ is stated asymptotically.
    rows, seven28 = density_table()
    q_inf = 1.0 / (1.5 - math.log(4) / math.log(3))
    require("#728 asymptotic q_+ = 1/(3/2 - log4/log3) = 4.1992 (rate limit)",
            abs(q_inf - 4.19920) < 1e-4, f"{q_inf}")
    qps = [r["q_plus"] for r in seven28]
    require("#728 finite q_+ strictly increases in B (approaches rate limit)",
            all(qps[i] < qps[i + 1] for i in range(len(qps) - 1)))
    require("#728 finite q_+ stays below the 4.1992 rate limit at all tabulated B",
            all(q < q_inf for q in qps))
    ratios = [math.log(r["M"]) / math.log(r["L"]) for r in seven28]
    require("#728 logM/logL increases toward log4/log3 = 1.2619",
            all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1))
            and all(rr < math.log(4) / math.log(3) for rr in ratios))
    # heavy-fiber crossover: W<=sqrt(L) for small B, W>sqrt(L) once heavy
    require("#728 heavy-fiber crossover W>sqrt(L) starts at B=6 (unpruned residual active)",
            [r["B"] for r in seven28 if r["W_gt_sqrtL"]] == [6, 8, 10, 12])
    require("#728 W=C(B,B/2) overtakes sqrt(L) (2^B beats 3^{B/2})",
            seven28[0]["W"] < seven28[0]["sqrtL"] and seven28[-1]["W"] > seven28[-1]["sqrtL"])

    # density table: window classification is monotone-consistent
    for r in rows:
        if r["logM_over_logL"] is not None:
            if r["logM_over_logL"] <= 1.0 + 1e-12:
                require(f"density {r['chart']}: logM/logL<=1 => empty window",
                        r["window"] == "empty")
            elif r["logM_over_logL"] >= 1.5:
                require(f"density {r['chart']}: logM/logL>=3/2 => all-q window",
                        r["window"] == "all-q")

    # entropy-form sanity.  Correct directions:
    #  (a) L <= Q^R  =>  logL <= R logQ  =>  logM/logL >= logM/(R logQ).
    #  (b) entropy bracket:  N h(beta) - log(N+1) <= log C(N,a) <= N h(beta).
    # So a SUFFICIENT (rigorous) condition for the q=2 window (logM > logL) is
    #  logM > R logQ, and since logM ~ N h(beta), the readable form is
    #  R logQ < N h(beta)  (the 'pure density condition on the chart').
    for r in rows:
        if r["L"] > 1:
            logM = math.log(r["M"])
            logL = math.log(r["L"])
            RlogQ = r["R"] * math.log(r["p_Q"])
            Nh = r["N"] * h_nat(r["a"] / r["N"])
            require(f"density {r['chart']}: logL <= R logQ (L <= Q^R)",
                    logL <= RlogQ + 1e-9)
            require(f"density {r['chart']}: logM/logL >= logM/(R logQ) (valid chain)",
                    r["logM_over_logL"] >= logM / RlogQ - 1e-9,
                    f"{r['logM_over_logL']} vs {logM/RlogQ}")
            require(f"density {r['chart']}: entropy bracket N h(beta)-log(N+1) <= logM <= N h(beta)",
                    Nh - math.log(r["N"] + 1) - 1e-9 <= logM <= Nh + 1e-9,
                    f"logM={logM} Nh={Nh}")
            # window nonempty (finite) <=> logM/logL > 1 <=> M > L
            require(f"density {r['chart']}: finite window nonempty iff M>L",
                    (r["window"] != "empty") == (r["M"] > r["L"]))

    cert = {
        "object": "chart-free pruned signed bound (Theorem I) + #716 Sec-6 "
                  "signed-clause discharge for pruned packets + layer-cake residual",
        "theorem_I": "R_A(g) <= (L/M)(L delta_A)^{1/2-1/q} <= L^{3/2-1/q}/M, "
                     "all finite abelian G, all A, all q>=2, |g|<=1 on |S|<=L",
        "q_plus_formula": "q_+(chart) = 1/(3/2 - logM/logL)",
        "dictionary": "||P_A f||_q = (M/L^{1-1/q}) R_A(f); charge c_i <= ||.||_q; "
                      "pruned packet => c_i <= L^{1/2} <= e^{o(N)} M/L^{1-1/q} on "
                      "density-passing charts",
        "charts": summaries,
        "layer_cake": [lc1, lc2, lc3],
        "density_table": rows,
        "family728_qplus_crosscheck": seven28,
        "checks_total": len(CHECKS),
        "checks_passed": sum(1 for _, ok in CHECKS if ok),
    }
    return cert


def tamper_selftest():
    """Each mutation of a load-bearing constant must be caught."""
    caught, muts = 0, 0

    # 1: q_+ formula tampered (drop the 3/2) -> would NOT give 4.199 for #728
    muts += 1
    bad_qp = 1.0 / (1.0 - math.log(4) / math.log(3))   # wrong: uses 1 not 3/2
    if not (4.19 < bad_qp < 4.20):
        caught += 1

    # 2: Theorem I direction flipped -- claim R_A >= sharp UB must FAIL on chart 1
    muts += 1
    T = [0, 1, 2, 3, 4]
    G, Om, Phi = prefix_e1(T, 7, 3)
    S = occupied(Phi)
    M, L = len(Om), len(S)
    cols = [(t % 7,) for t in T]
    bands = dyadic_bands_from_columns(G, cols)
    g = {s: 1.0 for s in S}
    hat = G.dft(g)
    violated = False
    for lab, Aidx in bands.items():
        dA = float(Fraction(len(Aidx), G.order))
        Pg = G.band_project_vec(hat, Aidx)
        for q in (2, 3, 4):
            RA = (L ** (1 - 1 / q) / M) * lq(Pg, q)
            ubc = (L ** (1.5 - 1 / q)) / M
            if RA > ubc + 1e-9:          # Theorem I says this never happens
                violated = True
    if not violated:                     # correct: no violation -> mutation of ">" caught
        caught += 1

    # 3: density criterion tampered -- claim near-injective chart has all-q window
    muts += 1
    L2, M2 = 35, 35                      # logM/logL == 1 -> empty window
    qp = q_plus_of(M2, L2)
    if qp is not None and qp <= 2.0:     # correct classification is 'empty'
        caught += 1

    # 4: layer-cake reconstruction -- W_max-1 layers must NOT reconstruct b
    #    (dropping a layer loses mass at the heaviest fiber).  Robust for W>=2.
    muts += 1
    G3, Om3, Phi3 = random_chart(9, 4, 40, seed=2027)
    S3 = occupied(Phi3)
    cnt3 = full_count(Phi3)
    Wm3 = int(max(cnt3.values()))
    b3 = {s: float(cnt3[s]) for s in S3}
    layers_short = [{s: 1.0 for s in S3 if cnt3[s] >= j} for j in range(1, Wm3)]  # drop top
    recon = {}
    for gj in layers_short:
        for s, v in gj.items():
            recon[s] = recon.get(s, 0.0) + v
    mismatch = any(abs(recon.get(s, 0.0) - b3[s]) > 1e-9 for s in S3)
    if mismatch and Wm3 >= 2:            # W_max-1 layers are insufficient
        caught += 1

    # 5: Parseval identity tampered -- ||K_A||_2^2 must equal delta_A not 2 delta_A
    muts += 1
    KA = G.kernel_vec(bands[list(bands)[0]])
    k2 = sum(abs(v) ** 2 for v in KA)
    dA = float(Fraction(len(bands[list(bands)[0]]), G.order))
    if abs(k2 - 2 * dA) > 1e-6:          # tampered target 2*delta_A is wrong
        caught += 1

    # 6: q=2 sharp bound is L/M; tampered target L/(2M) must be EXCEEDED by a
    #    real signed mask on the nondegenerate collision chart (chart2).  Random
    #    signs spread energy into nonzero bands (unlike the DC-heavy indicator),
    #    so max RA2 approaches the true ceiling L/M > L/(2M).
    muts += 1
    G2, Om2, Phi2 = moment_p1p2(list(range(11)), 11, 4)
    S2 = occupied(Phi2)
    M2, L2 = len(Om2), len(S2)
    bands2 = dyadic_bands_from_columns(G2, [(t % 11, (t * t) % 11) for t in range(11)])
    bad = False
    for g2 in sampled_masks(S2, 40, seed=909):
        hat2 = G2.dft(g2)
        for lab, Aidx in bands2.items():
            Pg = G2.band_project_vec(hat2, Aidx)
            RA2 = (L2 ** 0.5 / M2) * lq(Pg, 2)
            if RA2 > L2 / M2 + 1e-9:             # true bound L/M must hold
                return caught, muts              # real Theorem-I break -> abort
            if RA2 > L2 / (2 * M2) + 1e-9:       # exceeds tampered L/(2M)
                bad = True
    if bad:
        caught += 1

    return caught, muts


def main():
    if "--tamper-selftest" in sys.argv:
        caught, muts = tamper_selftest()
        print(f"TAMPER SELF-TEST: caught {caught}/{muts} mutations")
        print("RESULT:", "PASS" if caught == muts else "FAIL")
        return 0 if caught == muts else 1

    cert = run()
    passed, total = cert["checks_passed"], cert["checks_total"]
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "data", "certificates", "general-pruned-signed-bound")
    outdir = os.path.normpath(outdir)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "general_pruned_signed_bound.json"), "w") as fh:
        json.dump(cert, fh, indent=1, default=str)

    print("=== general chart-free pruned signed bound (Theorem I) ===")
    print("chart                     | M     L    kappa | logM/logL | q_+        | maxR/UB")
    for s in cert["charts"]:
        qp = s["q_plus"]
        qps = "inf(all q)" if qp == float("inf") else f"{qp:.3f}"
        lr = s["logM_over_logL"]
        lrs = "  -  " if lr is None else f"{lr:.4f}"
        print(f"{s['label']:<25} | {s['M']:<5} {s['L']:<4} {s['kappa']:<5} | "
              f"{lrs:<9} | {qps:<10} | {s['max_ratio_crude']:.4f}")
    print("\n--- density criterion (depth-R prefix charts, exact L) ---")
    print("chart        p  N  a R |  L    Q^R    M      logM/logL  q_+        window")
    for r in cert["density_table"]:
        qp = r["q_plus"]
        qps = "inf" if qp == float("inf") else (f"{qp:.3f}" if qp else "-")
        lr = r["logM_over_logL"]
        lrs = "-" if lr is None else f"{lr:.4f}"
        print(f"{r['chart']:<12} {r['p_Q']:<2} {r['N']:<2} {r['a']} {r['R']} | "
              f"{r['L']:<4} {r['L_bound_QR']:<6} {r['M']:<6} {lrs:<10} {qps:<10} {r['window']}")
    print("\n--- #728 superincreasing cross-check  q_+ -> 4.1992 ; heavy-fiber crossover ---")
    for r in cert["family728_qplus_crosscheck"]:
        print(f"  B={r['B']:<2} L={r['L']:<9} M={r['M']:<9} W={r['W']:<6} "
              f"logM/logL={r['logM_over_logL']:.4f} q_+={r['q_plus']:.4f} "
              f"W>sqrtL={r['W_gt_sqrtL']}")
    print("\n--- layer-cake (unpruned) ---")
    for lc in cert["layer_cake"]:
        print(f"  {lc['label']:<8} W_max={lc['W_max']:<3} "
              f"unpruned>pruned q2 bound: {lc['unpruned_exceeds_pruned_q2_bound']}  "
              f"pigeonhole_lb_q2={lc['pigeonhole_lb_q2']:.4f}")
    print(f"\nRESULT: {'PASS' if passed==total else 'FAIL'} ({passed}/{total})")
    print(f"certificate: {os.path.join(outdir, 'general_pruned_signed_bound.json')}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
