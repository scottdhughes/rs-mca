#!/usr/bin/env sage
# -*- mode: python -*-
r"""
universal_dim_sweep_e3.sage -- stress-test whether  dim(sum_k V_k) <= ell-2  is UNIVERSAL
(over all mixed Gamma), and whether the note's reduction  dim(sum_k V_k) >= E_3  ever fails.

V_k built from excess cosets (mu_b>=3, modal max fiber):
  h_k = co-fiber locator = prod_{x in coset\F_k}(X-x),  deg = ell-mu_k;
  V_k = h_k * F_p[X]_{<= mu_k-2} subset F_p[X]_{<= ell-2}  (columns = degrees 0..ell-2).

If dim(sum V_k) <= ell-2 holds everywhere AND dim(sum V_k) >= E_3, then E_3 <= ell-2.
When dim = ell-2 we extract the annihilating functional lambda (right-kernel of the basis
matrix) and probe whether it is STRUCTURED / universal -- the would-be proof handle.

Three Gamma sources per (ell,p): (R) random mixed, (P) solve-based planted high-E_3, plus
the shipped witness ANCHORS.  Deterministic (fixed LCG seed).  Independent Sage/GF(p).
"""
import itertools

class LCG:
    def __init__(s, seed): s.s = seed & ((1<<64)-1)
    def nxt(s):
        s.s = (s.s*6364136223846793005 + 1442695040888963407) & ((1<<64)-1); return s.s>>17
    def ri(s, lo, hi): return lo + s.nxt() % (hi-lo+1)

CONFIGS = [(7,211),(7,337),(11,199),(11,331),(13,313),(17,103),(17,409)]
ANCHORS = [
    (11,331,[97,29,97,239,171,92,143,155,270,1]),
    (13,313,[254,289,29,276,242,219,201,261,79,232,133,1]),
    (17,103,[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]),
    (17,409,[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1]),
]
NRAND, NPLANT = 3000, 400

def setup(p, ell):
    F = GF(p); g = F.multiplicative_generator(); n = (p-1)//ell
    zeta = g**n; H = [zeta**j for j in range(ell)]
    return F, g, n, zeta, H

def excess_fibers(gamma, F, g, n, H, ell):
    gam = [F(c) for c in gamma]
    res = []
    for i in range(n):
        b = g**i; coset = [b*h for h in H]; tally = {}
        for x in coset:
            val = F(0)
            for r in range(ell-1,0,-1): val = (val+gam[r-1])*x
            tally.setdefault(val,[]).append(x)
        mu = max(len(v) for v in tally.values())
        if mu < 3: continue
        modal = min((val for val,v in tally.items() if len(v)==mu), key=lambda z:int(z))
        fs = set(tally[modal]); cof = [x for x in coset if x not in fs]
        res.append((mu, cof))
    return res

def dim_and_ann(fibers, F, ell):
    ncols = ell-1
    Rx = PolynomialRing(F,'X'); X = Rx.gen()
    rows = []
    for (mu, cof) in fibers:
        hk = prod((X-x) for x in cof)
        for d in range(mu-1):
            cs = list(hk*X**d); v = [F(0)]*ncols
            for dd,c in enumerate(cs): v[dd]=c
            rows.append(v)
    if not rows: return 0, 0, None
    M = Matrix(F, rows); dim = M.rank()
    ann = None
    if dim == ncols-1:
        b = M.right_kernel().basis()
        if b: ann = b[0]
    return dim, len(rows), ann

def E3_of(fibers): return sum(mu-2 for (mu,_) in fibers)

def random_gamma(rng, p, ell):
    while True:
        gm = [rng.ri(0,p-1) for _ in range(ell-1)]
        if any(gm): return gm

def planted_gamma(rng, F, g, n, H, ell, p):
    """plant K fibers on distinct cosets, solve nullspace of coincidence rows for a gamma."""
    K = rng.ri(2, min(6, n-1))
    cos = []
    while len(cos) < K:
        c = rng.ri(0, n-1)
        if c not in cos: cos.append(c)
    Rx = PolynomialRing(F,'X'); X = Rx.gen()
    rows = []
    for c in cos:
        nu = rng.ri(3, ell-1)                 # aim high (excess-heavy)
        base = g**c
        pts = [base*H[e] for e in range(nu)]
        v0 = [pts[0]**r for r in range(1,ell)]
        for x in pts[1:]:
            rows.append([x**r - v0[r-1] for r in range(1,ell)])
    if not rows: return None
    M = Matrix(F, rows)
    if M.rank() > ell-2: return None          # not realizable
    ker = M.right_kernel().basis()
    if not ker: return None
    gm = list(ker[rng.ri(0, len(ker)-1)])
    if not any(gm): return None
    return [int(c) for c in gm]

def run():
    worst_dim_gap = -10**9   # max (dim - (ell-2))  ; must stay <= 0 for universality
    worst_red_gap = 10**9    # min (dim - E_3)      ; must stay >= 0 for the reduction
    ann_records = []
    total = 0
    for (ell, p) in CONFIGS:
        F,g,n,zeta,H = setup(p, ell)
        rng = LCG(1000*ell + p)
        maxdim = 0; maxE3 = 0; n_at_cap = 0; viol_dim = 0; viol_red = 0; tested = 0
        srcs = ([("R", random_gamma(rng,p,ell)) for _ in range(NRAND)] +
                [("P", planted_gamma(rng,F,g,n,H,ell,p)) for _ in range(NPLANT)])
        for tag, gm in srcs:
            if gm is None: continue
            fibers = excess_fibers(gm, F, g, n, H, ell)
            if not fibers: continue
            E3 = E3_of(fibers)
            dim, nrows, ann = dim_and_ann(fibers, F, ell)
            tested += 1; total += 1
            maxdim = max(maxdim, dim); maxE3 = max(maxE3, E3)
            worst_dim_gap = max(worst_dim_gap, dim - (ell-2))
            worst_red_gap = min(worst_red_gap, dim - E3)
            if dim > ell-2: viol_dim += 1
            if dim < E3: viol_red += 1
            if dim == ell-2: n_at_cap += 1
        print(" ell=%2d p=%3d : tested=%4d  maxE3=%d(ell-2=%d)  max dim(sumV)=%d  #{dim==ell-2}=%d  "
              "viol[dim>ell-2]=%d  viol[dim<E3]=%d"
              % (ell, p, tested, maxE3, ell-2, maxdim, n_at_cap, viol_dim, viol_red))
    print("-"*96)
    # annihilator structure on the ANCHORS (known gamma) -- is lambda related to Gamma?
    print(" ANNIHILATOR PROBE (dim==ell-2 anchors): is the missing functional structured?")
    for (ell,p,gm) in ANCHORS:
        F,g,n,zeta,H = setup(p,ell)
        fibers = excess_fibers(gm, F, g, n, H, ell)
        dim, nrows, ann = dim_and_ann(fibers, F, ell)
        if ann is None:
            print("   ell=%d p=%d: dim=%d != ell-2, no 1-dim annihilator" % (ell,p,dim)); continue
        annv = [int(a) for a in ann]                     # functional on coeffs deg 0..ell-2
        gamv = [c % p for c in gm]                        # Gamma coeffs for X^1..X^{ell-1}
        # normalize both (first nonzero -> 1) and compare a few candidate alignments
        def norm(v):
            for a in v:
                if a % p:
                    ia = pow(a, p-2, p); return [ (x*ia) % p for x in v]
            return v
        na, ng, ngr = norm(annv), norm(gamv), norm(list(reversed(gamv)))
        eq_gamma = (na == ng); eq_gamma_rev = (na == ngr)
        print("   ell=%d p=%d dim=%d: ann(norm)=%s" % (ell,p,dim, na))
        print("            gamma(norm)=%s  rev=%s   ann==gamma?%s  ann==rev(gamma)?%s"
              % (ng, ngr, eq_gamma, eq_gamma_rev))
    print("="*96)
    print(" VERDICT: total=%d  worst (dim-(ell-2))=%d  [<=0 => dim<=ell-2 UNIVERSAL so far]"
          % (total, worst_dim_gap))
    print("          worst (dim-E_3)=%d  [>=0 => reduction dim>=E_3 holds]" % worst_red_gap)
    if worst_dim_gap <= 0 and worst_red_gap >= 0:
        print("  => Across all tested Gamma: E_3 <= dim(sumV) <= ell-2 CONFIRMED (2-step split viable).")
    elif worst_dim_gap > 0:
        print("  => dim(sumV) EXCEEDS ell-2 somewhere: the ell-2 upper structure is a MIRAGE.")
    return 0

import sys
sys.exit(run())
