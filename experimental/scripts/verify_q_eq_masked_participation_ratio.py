"""
verify_q_eq_masked_participation_ratio.py  --  zero-arg, stdlib-only verifier for
the MASKED-residual participation-ratio packet
(cap25_v13_q_eq_masked_participation_ratio.md).  Follow-on to the OPEN PR #414
(cap25_v13_q_em_inverse_participation_ratio, branch
thresholds-em-inverse-participation-ratio @54f8129): it answers the masked-residual
open variant that #414 names, using the object introduced by the integrated
signed-e_m masked-residual audit (cap25_v13_signed_em_masked_residual_audit.md,
integrated e83962ae, was PR #413).

Merges the three finished lane_eq_masked research scripts (verify_eq_masked.py,
verify_eq_masked_detail.py, verify_not_projection.py) into one gated verifier.
Every number printed in the note is recomputed here (witness-vs-lemma closure).

Object.  D = mu_n subset F_p^*.  Prefix map Phi_w(S)=(p_1,...,p_w) mod p.
Raw family = all C(n,m) m-subsets.  N(z)=|Phi_w^{-1}(z)|, E(t)=DFT(N)=e_m(v_t).
Support-side first-match masks (faithful TOY reconstructions of the ledger
branches, kb_mca_1116048_first_match_ledger_v1.md "First-match branches"):
  M_quot : branch-4 quotient-periodic cell -- remove 2-periodic supports (S=-S).
  M_gen  : branch-7 generated-field collision removal -- per finite fiber keep
           only the LARGEST exact Z[zeta_n] lift class (the honest lift), charge
           the rest to generated-field (the ledger's largest-honest-class
           worst-case model: F_17 z=1 replay had largest exact class 20 of 757).
  M_both : periodic removed, then largest exact class per surviving fiber.
For each mask: T_Q=|P_Q|, tau=T_Q/C, N_Q, E_Q=DFT(N_Q),
  ||E_Q||_1, ||E_Q||_2^2 = T_Q^2(Gamma2_Q-1) [Parseval], PR=||.||_1^2/||.||_2^2.

Replays / gates, exactly:
  - the M31-list reference budget 16777215/1993678 = 8.4152079724
    (prop:q-exact-target) and the deployment KB-MCA ledger constants (exact big-int;
    matches #412/#414/the integrated ledger);
  - REDUCED: (STAR)_masked  Sum|E_Q| <= (K_Q-1)T_Q  <=>  PR(E_Q) <= nu*_masked
    = (K_Q-1)^2/(Gamma2_Q-1) for K_Q >= 1 (gated; K_Q in [8.4152, 20.6057] here),
    substitutions C->T_Q=tau*C, K_rem->K_Q=K_rem/tau,
    Gamma2->Gamma2_Q; Parseval exact per mask (relerr <= 3.8e-15);
  - the DECISIVE row (17,16,8,3) table for all four masks;
  - the #413 counterexample replay: RAW primitive triangle 1+L1p/C=10.472846
    (reproduces #413's printed constant), M_gen 5.967/6.071 < 8.4152 (viable where
    raw is overstrong -- CONDITIONAL: this support-removal is exactly the ledger's
    still-open lift-class cost model, NOT its proved branch-7 image-cell deduction),
    M_quot WORSENS to 11.89;
  - the equivalence-flip scan (agree at all K);
  - support-vs-projection: 4880 of 4912 directions frequency-MIXED (NOT a character
    projection), 0 mass born; Parseval survives every mask;
  - the 5-toy PR grid RAW vs M_gen (M_gen INERT tau=1 on the proper-subgroup n=8
    rows, large on full-group / large-field rows; primitive Fourier share survives);
  - the masked L2 floor factors, exact form sqrt((p^w-1)(Gamma2_Q-1)) (masking
    changes only sqrt(Gamma2_Q-1): 0.371->0.274; the mask-independent factor
    sqrt(p^w-1) ~= p^{w/2} is INHERITED -- the p^{w/2} closed form is approximate,
    off by exactly sqrt(p^w/(p^w-1)), rel 1.0e-4 at the toy);
  - the FALSIFIER row: over-pruning to the single largest exact class gives a
    full-support delta spectrum PR = p^w-1, triangle = p^w
    (the dense-heavy-fiber precondition of rem:mass-aware-logmoment);
  - >=6 tamper self-tests.

Run:  python3 experimental/scripts/verify_q_eq_masked_participation_ratio.py
      (exit 0 on PASS; ~17 s)
"""
import cmath, math
from itertools import combinations
from collections import defaultdict
from fractions import Fraction

CHECKS = []
def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

def log2int(x):
    if x <= 0: return float('-inf')
    b = x.bit_length(); top = x >> max(0, b-64)
    return (b-min(b, 64)) + math.log2(top)
def log2frac(fr): return log2int(fr.numerator) - log2int(fr.denominator)
def approx(x, y, rel=3e-3, ab=6e-3): return abs(x-y) <= ab + rel*abs(y)

# ===================================================================== toy engine
def subgroup_exps(p, n):
    def order(x):
        o = 1; y = x % p
        while y != 1: y = (y*x) % p; o += 1
        return o
    g = next(c for c in range(2, p) if order(c) == p-1)
    omega = pow(g, (p-1)//n, p)
    return omega, [pow(omega, e, p) for e in range(n)]

def make_W(p):
    return [[cmath.exp(2j*math.pi*((a*b) % p)/p) for b in range(p)] for a in range(p)]

def axis_dft(arr, p, w, axis, W):
    size = p**w; stride = p**axis; block = stride*p; out = [0j]*size
    for base in range(0, size, block):
        for off in range(stride):
            vec = [arr[base+off+s*stride] for s in range(p)]
            for a in range(p):
                Wa = W[a]; acc = 0j
                for s in range(p): acc += vec[s]*Wa[s]
                out[base+off+a*stride] = acc
    return out

def dft(Nflat, p, w, W):
    E = Nflat[:]
    for ax in range(w): E = axis_dft(E, p, w, ax, W)
    return E

def coeff_scale(tflat, p, w, n):
    idx = tflat; supp = []
    for j in range(w):
        tj = idx % p; idx //= p
        if tj: supp.append(j+1)
    if not supp: return 0
    c = n
    for k in supp: c = math.gcd(c, k)
    return c

def analyze(Nflat, p, w, n, C, W, label):
    size = p**w
    T = sum(Nflat); maxN = max(Nflat); sumN2 = sum(x*x for x in Nflat)
    E = dft(Nflat, p, w, W)
    L1 = 0.0; L1p = 0.0; L2sq = 0.0; maxE = 0.0
    for t in range(1, size):
        ae = abs(E[t]); L1 += ae; L2sq += ae*ae; maxE = max(maxE, ae)
        if coeff_scale(t, p, w, n) == 1: L1p += ae
    Gamma2 = size*sumN2/(T*T)
    PR = L1*L1/L2sq if L2sq > 0 else float('inf')
    parse = abs(L2sq-(T*T*(Gamma2-1)))/(T*T*(Gamma2-1)) if Gamma2 > 1 else 0.0
    floorRHS = math.sqrt((size-1)*(Gamma2-1))
    return dict(label=label, T=T, tau=T/C, maxN=maxN,
        R_masked=size*maxN/T, R_rawavg=size*maxN/C,
        Gamma2=Gamma2, L1=L1, L1_over_T=L1/T, L1p=L1p,
        primshare=(L1p/L1 if L1 > 0 else 1.0),
        PR=PR, effsupp=PR/(size-1), maxE_over_T=maxE/T, maxE=maxE,
        tri_masked=1+L1/T, tri_rawavg=(T+L1)/C,
        tri_prim_masked=1+L1p/T, tri_prim_rawavg=(T+L1p)/C,
        floorRHS=floorRHS, parse=parse, ndir=size-1,
        sqrt_G2m1=math.sqrt(Gamma2-1) if Gamma2 > 1 else 0.0)

def build_masks(p, n, m, w):
    omega, poww = subgroup_exps(p, n)
    half = n//2; exps = list(range(n)); size = p**w
    Nraw = [0]*size; Nquot = [0]*size
    perfiber = defaultdict(lambda: defaultdict(int))
    perfiber_np = defaultdict(lambda: defaultdict(int))
    for S in combinations(exps, m):
        Sset = set(S)
        zc = []; flat = 0; mul = 1
        for k in range(1, w+1):
            pk = 0
            for i in S: pk += poww[(k*i) % n]
            pk %= p; zc.append(pk); flat += pk*mul; mul *= p
        Nraw[flat] += 1
        key = []
        for k in range(1, w+1):
            v = [0]*half
            for i in S:
                e = (k*i) % n
                if e < half: v[e] += 1
                else: v[e-half] -= 1
            key.append(tuple(v))
        key = tuple(key)
        periodic = all(((i+half) % n) in Sset for i in S)
        perfiber[flat][key] += 1
        if not periodic:
            Nquot[flat] += 1
            perfiber_np[flat][key] += 1
    Ngen = [0]*size
    for z, classes in perfiber.items(): Ngen[z] = max(classes.values())
    Nboth = [0]*size
    for z, classes in perfiber_np.items(): Nboth[z] = max(classes.values()) if classes else 0
    C = math.comb(n, m)
    return dict(Nraw=Nraw, Nquot=Nquot, Ngen=Ngen, Nboth=Nboth, C=C, perfiber=perfiber)

_MB = {}; _AN = {}
def masks(cfg):
    if cfg not in _MB: _MB[cfg] = build_masks(*cfg)
    return _MB[cfg]
_WC = {}
def Wp(p):
    if p not in _WC: _WC[p] = make_W(p)
    return _WC[p]
def res(cfg, tag):
    key = (cfg, tag)
    if key not in _AN:
        p, n, m, w = cfg; M = masks(cfg)
        _AN[key] = analyze(M[{'RAW':'Nraw', 'M_quot':'Nquot', 'M_gen':'Ngen', 'M_both':'Nboth'}[tag]],
                           p, w, n, M['C'], Wp(p), tag)
    return _AN[key]

# ===================================================================== §1 ledger
print("== §1 deployment KB-MCA a=1116048 ledger + M31-list budget (exact big-int) ==")
p_dep = 2130706433; n = 2**21; k = 2**20; a = 1116048; m_dep = 981104; w_dep = 67471
Krem = 4805007; Kraw = 4807520
check("p=2^31-2^24+1", p_dep == 2**31-2**24+1)
check("n=2^21, m=n-a=981104, w=a-(k+1)=67471", n == 2**21 and n-a == m_dep and w_dep == a-(k+1))
C_dep = math.comb(n, m_dep); pw_dep = p_dep**w_dep
avg_floor = C_dep//pw_dep; target_floor = (Krem*C_dep)//pw_dep
check("avg_floor=57198030365", avg_floor == 57198030365, str(avg_floor))
check("target_floor=274836936291722953", target_floor == 274836936291722953, str(target_floor))
l2C = log2int(C_dep); l2pw = log2int(pw_dep)
check("log2 C = 2090873.279793", abs(l2C-2090873.279793) < 1e-4, f"{l2C:.6f}")
check("log2 p^w = 2090837.544547", abs(l2pw-2090837.544547) < 1e-4, f"{l2pw:.6f}")
check("avg = C/p^w = 2^35.735246", abs((l2C-l2pw)-35.735246) < 1e-4, f"2^{l2C-l2pw:.6f}")
# reference masked participation budget: nu*_ref,masked = (Krem/tau-1)^2; at tau=1 -> (Krem-1)^2
nu_ref = (Krem-1)**2
check("nu*_ref,masked (tau=1) = (Krem-1)^2 = 23088082660036 = 2^44.392214",
      nu_ref == 23088082660036 and abs(math.log2(nu_ref)-44.392214) < 1e-5, f"2^{math.log2(nu_ref):.6f}")
# deployment tau is Theta(1) and unknown (part of the open ledger); the mass factor does NOT
# make the bound vacuous at deployment: for any tau in [0.1,1], nu*_ref,masked stays 2^44..2^51,
# negligible vs the p^w-1 = 2^2090837.54 directions.  (toy vacuity is a small-scale artifact.)
for tau_t in [1.0, 0.41, 0.1]:
    lg = math.log2((Krem/tau_t-1)**2)
    check(f"nu*_ref,masked=(Krem/tau-1)^2 ~ 2^[44,52] at tau={tau_t} (Theta(1) mass => << 2^2090837 dirs)",
          44.0 <= lg <= 52.0 and lg < l2pw, f"2^{lg:.3f}")
# M31-list budget = B*_M31 / ceil(avg) (prop:q-exact-target)
M31 = Fraction(16777215, 1993678)
check("M31-list budget = 16777215/1993678 = 8.4152079724 (prop:q-exact-target)",
      abs(float(M31)-8.4152079724) < 1e-9, f"{float(M31):.10f}")

# ===================================================================== §2 decisive-row table
print("\n== §2 REDUCED equivalence + decisive row (17,16,8,3): four-mask table ==")
CFG = (17, 16, 8, 3); p, nn, mm, ww = CFG; pw = p**ww; C = masks(CFG)['C']
check("(17,16,8,3): C(16,8)=12870, p^w=4913", C == 12870 and pw == 4913)
# expected decisive-row values (from finished lane; witness-vs-lemma):
#             T_Q,   tau,    maxN, R_rawavg, tri_rA(tot), tri_rA(prim), L1/T,    primsh, G2-1,    K_Q,    PR,      nu*,     floorRHS
DEC = {
 'RAW':   (12870, 1.0000, 7, 2.672183, 10.5798, 10.4728,  9.5798, 0.9888, 0.13769,  8.4152,  666.52,  399.35, 26.006),
 'M_quot':(12800, 0.9946, 5, 1.908702, 11.8916, 11.7871, 10.9566, 0.9904, 0.13517,  8.4612,  888.11,  411.85, 25.767),
 'M_gen': ( 5286, 0.4107, 6, 2.290443,  6.0713,  5.9668, 13.7819, 0.9816, 0.07537, 20.4888, 2519.95, 5038.98, 19.242),
 'M_both':( 5256, 0.4084, 2, 0.763481,  6.1624,  6.0635, 14.0893, 0.9828, 0.07132, 20.6057, 2783.19, 5389.24, 18.718),
}
for tag in ['RAW', 'M_quot', 'M_gen', 'M_both']:
    r = res(CFG, tag); e = DEC[tag]
    KQ = float(M31)/r['tau']              # masked budget multiplier (raw budget held fixed)
    G2m1 = r['Gamma2']-1
    nu = (KQ-1)**2/G2m1
    ok = (r['T'] == e[0] and approx(r['tau'], e[1], ab=1e-3) and r['maxN'] == e[2]
          and approx(r['R_rawavg'], e[3], rel=1e-5) and approx(r['tri_rawavg'], e[4], rel=1e-3)
          and approx(r['tri_prim_rawavg'], e[5], rel=1e-3) and approx(r['L1_over_T'], e[6], rel=1e-3)
          and approx(r['primshare'], e[7], ab=1e-3) and approx(G2m1, e[8], rel=2e-3)
          and approx(KQ, e[9], rel=1e-3) and approx(r['PR'], e[10], rel=2e-3)
          and approx(nu, e[11], rel=2e-3) and approx(r['floorRHS'], e[12], rel=1e-3))
    check(f"decisive {tag}: T/tau/maxN/R/tri_tot/tri_prim/L1T/primsh/G2/K_Q/PR/nu*/floor match",
          ok, f"T={r['T']} tau={r['tau']:.4f} PR={r['PR']:.2f} nu*={nu:.2f} K_Q={KQ:.4f}")
    # REDUCED: (STAR)_masked [L1/T<=K_Q-1]  <=>  PR<=nu*  (algebraic equivalence, exact)
    star = r['L1_over_T'] <= (KQ-1); prb = r['PR'] <= nu
    check(f"  {tag}: (STAR)_masked <=> PR<=nu* agree", star == prb, f"both={star}")
# vacuity flag at toy scale (M_gen/M_both): nu*_masked > ndir
for tag in ['M_gen', 'M_both']:
    r = res(CFG, tag); KQ = float(M31)/r['tau']; nu = (KQ-1)**2/(r['Gamma2']-1)
    check(f"  {tag}: nu*_masked > ndir=4912 (PR-bound VACUOUS at toy scale)",
          nu > r['ndir'], f"nu*={nu:.1f} > {r['ndir']}")
# hypothesis of the squared biconditional: K_Q >= 1 (vacuity edge; always true in scope)
kqs = [float(M31)/res(CFG, tag)['tau'] for tag in ['RAW', 'M_quot', 'M_gen', 'M_both']]
check("K_Q >= 1 on every mask (biconditional hypothesis; K_Q in [8.4152, 20.6057])",
      all(kq >= 1 for kq in kqs) and approx(min(kqs), 8.4152, rel=1e-4)
      and approx(max(kqs), 20.6057, rel=1e-4), f"K_Q range [{min(kqs):.4f}, {max(kqs):.4f}]")

# ===================================================================== §3 #413 replay
print("\n== §3 #413 counterexample replay (witness-vs-lemma on the printed constants) ==")
rraw = res(CFG, 'RAW'); rgen = res(CFG, 'M_gen'); rquot = res(CFG, 'M_quot')
check("413 replay: RAW R = p^w*maxN/C = 4913*7/12870 = 2.672183 (exact)",
      Fraction(pw*7, C) == Fraction(34391, 12870) and approx(rraw['R_rawavg'], 2.672183, rel=1e-6),
      f"{float(Fraction(pw*7,C)):.6f}")
tri_prim_raw = 1 + rraw['primshare']*rraw['L1_over_T']   # = 1 + L1_prim/C (T=C for RAW)
check("413 replay: RAW primitive triangle 1+L1p/C = 10.472846 (#413's printed constant)",
      approx(tri_prim_raw, 10.472846, ab=5e-6), f"{tri_prim_raw:.6f}")
check("413 separation: R_true 2.672 < M31 budget 8.4152 < raw prim triangle 10.473 (L1 sufficient-not-necessary)",
      rraw['R_rawavg'] < 8.4152 < tri_prim_raw, f"{rraw['R_rawavg']:.4f} < 8.4152 < {tri_prim_raw:.4f}")
check("413 HEADLINE: M_gen support masking pulls triangle to 5.967/6.071 < 8.4152 (viable where raw overstrong)",
      rgen['tri_prim_rawavg'] < 8.4152 and rgen['tri_rawavg'] < 8.4152,
      f"prim={rgen['tri_prim_rawavg']:.4f} tot={rgen['tri_rawavg']:.4f}")
check("413 contrast: M_quot (branch-4 quotient cell alone) WORSENS to 11.89 > 8.4152",
      rquot['tri_rawavg'] > 8.4152 and approx(rquot['tri_rawavg'], 11.8916, rel=1e-3),
      f"tri_rawavg={rquot['tri_rawavg']:.4f}")
check("413 contrast: quotient cell is ~0.5% of supports (1-tau = 70/12870)",
      approx(1-rquot['tau'], 70/12870, rel=1e-3), f"1-tau={1-rquot['tau']:.4f}")

# ===================================================================== §4 equivalence flip
print("\n== §4 equivalence-flip scan (mask=M_gen): (STAR)_masked <=> PR<=(K-1)^2/(G2_Q-1) at all K ==")
G2m1 = rgen['Gamma2']-1; flips = []
for K in [1.5, 2, 3, 5, 8, 10, 13.7819, 14, 15, 20]:
    lhs = rgen['L1_over_T'] <= (K-1)
    rhs = rgen['PR'] <= ((K-1)**2/G2m1)
    flips.append(lhs == rhs)
check("(STAR)_masked <=> PR<=nu* agrees at EVERY scanned K (exact algebraic equivalence)",
      all(flips), f"{len(flips)}/{len(flips)} agree; flip between K=13.78 and K=15")

# ===================================================================== §5 not-a-projection + Parseval
print("\n== §5 support-side, NOT a character projection + Parseval survives per mask ==")
W = Wp(p); Eraw = dft(masks(CFG)['Nraw'], p, ww, W); Egen = dft(masks(CFG)['Ngen'], p, ww, W)
proj_like = 0; mixed = 0; born = 0
for t in range(1, pw):
    aa, bb = abs(Eraw[t]), abs(Egen[t])
    if bb < 1e-9 or abs(bb-aa) < 1e-6: proj_like += 1
    else: mixed += 1
    if aa < 1e-9 and bb > 1e-6: born += 1
check("M_gen NOT a projection: 4880 of 4912 directions frequency-MIXED (0<|E_Q|!=|E|)",
      mixed == 4880, f"mixed={mixed}, projection-consistent={proj_like}")
check("a projection can only kill, never create: 0 directions with |E|=0 but |E_Q|>0",
      born == 0, f"born={born}")
check("partition closes: mixed + projection-consistent = 4912", mixed+proj_like == pw-1)
worst_parse = max(res(CFG, tag)['parse'] for tag in ['RAW', 'M_quot', 'M_gen', 'M_both'])
check("Parseval ||E_Q||_2^2 = T_Q^2(Gamma2_Q-1) survives EVERY mask (relerr <= 3.8e-15)",
      worst_parse < 1e-9, f"worst relerr {worst_parse:.1e}")

# ===================================================================== §6 5-toy PR grid
print("\n== §6 5-toy PR grid: RAW vs M_gen (INERT on subgroup rows; primitive share survives) ==")
TOYS = [(17, 16, 8, 3), (17, 8, 4, 2), (41, 8, 4, 2), (97, 16, 8, 1), (97, 16, 8, 2)]
PRGRID = {  # (RAW PR, M_gen PR, M_gen tau)
 (17, 16, 8, 3): (666.52, 2519.95, 0.4107),
 (17,  8, 4, 2): (127.78,  127.78, 1.0000),
 (41,  8, 4, 2): (737.01,  737.01, 1.0000),
 (97, 16, 8, 1): ( 20.50,   53.51, 0.1198),
 (97, 16, 8, 2): (843.25, 3055.45, 0.5133),
}
for cfg in TOYS:
    rR = res(cfg, 'RAW'); rG = res(cfg, 'M_gen'); e = PRGRID[cfg]
    ok = approx(rR['PR'], e[0], rel=2e-3) and approx(rG['PR'], e[1], rel=2e-3) and approx(rG['tau'], e[2], ab=1e-3)
    check(f"grid {cfg}: PR_raw={e[0]} PR_Mgen={e[1]} (tau={e[2]})", ok,
          f"PR_raw={rR['PR']:.2f} PR_Mgen={rG['PR']:.2f} tau={rG['tau']:.4f}")
# M_gen INERT (tau=1) exactly on the proper-subgroup n=8 rows; active (tau<1) on full-group/large-field
inert = [cfg for cfg in TOYS if res(cfg, 'M_gen')['tau'] == 1.0]
active = [cfg for cfg in TOYS if res(cfg, 'M_gen')['tau'] < 1.0]
check("M_gen INERT (tau=1) exactly on the two proper-subgroup n=8 rows (no finite lift-collisions)",
      set(inert) == {(17, 8, 4, 2), (41, 8, 4, 2)}, f"inert={inert}")
check("M_gen ACTIVE (tau<1) on the full-group (17,16,8,3) + large-field (97,16,8,*) rows",
      set(active) == {(17, 16, 8, 3), (97, 16, 8, 1), (97, 16, 8, 2)}, f"active={active}")
# intrinsic (masked-avg/PR) units: masking RAISES PR 666->2520 and effsupp 0.14->0.51 at decisive row
check("intrinsic units caveat: masking RAISES PR 666->2520 and effsupp 0.14->0.51 (decisive row)",
      approx(rraw['PR'], 666.52, rel=2e-3) and approx(rgen['PR'], 2519.95, rel=2e-3)
      and approx(rraw['effsupp'], 0.1357, ab=2e-3) and approx(rgen['effsupp'], 0.5130, ab=2e-3),
      f"PR {rraw['PR']:.0f}->{rgen['PR']:.0f}  effsupp {rraw['effsupp']:.3f}->{rgen['effsupp']:.3f}")
# intrinsic masked-avg triangles gated to precision (not just >budget)
check("intrinsic masked-avg triangles: RAW 10.580 -> M_gen 14.782 (both > 8.4152 budget)",
      approx(rraw['tri_masked'], 10.580, rel=1e-3) and approx(rgen['tri_masked'], 14.782, rel=1e-3)
      and rraw['tri_masked'] > 8.4152 and rgen['tri_masked'] > 8.4152,
      f"{rraw['tri_masked']:.3f} -> {rgen['tri_masked']:.3f}")
# the three remaining grid primitive-share transitions (note Sec.5 table), gated
psh_rows = [((17, 8, 4, 2), 0.834, 0.834), ((41, 8, 4, 2), 0.928, 0.928), ((97, 16, 8, 1), 1.000, 1.000)]
psh_ok = True; psh_det = []
for cfg, sr, sg in psh_rows:
    a_, b_ = res(cfg, 'RAW')['primshare'], res(cfg, 'M_gen')['primshare']
    psh_ok = psh_ok and approx(a_, sr, ab=2e-3) and approx(b_, sg, ab=2e-3)
    psh_det.append(f"{cfg}: {a_:.3f}->{b_:.3f}")
check("remaining grid primitive-share transitions gated: 0.834->0.834, 0.928->0.928, 1.000->1.000",
      psh_ok, "; ".join(psh_det))
# 83-93% primitive Fourier share SURVIVES masking; 0.920->0.957 at (97,16,8,2)
r97R = res((97, 16, 8, 2), 'RAW'); r97G = res((97, 16, 8, 2), 'M_gen')
check("primitive Fourier share survives masking: 0.920 -> 0.957 at (97,16,8,2) (wall persists)",
      approx(r97R['primshare'], 0.920, ab=2e-3) and approx(r97G['primshare'], 0.957, ab=2e-3),
      f"{r97R['primshare']:.3f} -> {r97G['primshare']:.3f}")

# ===================================================================== §7 masked p^{w/2} floor
print("\n== §7 masked L2-route floor: exact form sqrt((p^w-1)(G2_Q-1)); sqrt(p^w-1)~=p^{w/2} factor INHERITED ==")
pw2 = p**(ww/2.0)
off = math.sqrt(pw/(pw-1))   # exact ratio between the approximate p^{w/2} form and the exact floor
for tag, exp_sqrt, exp_floor in [('RAW', 0.371, 26.006), ('M_quot', 0.368, 25.767),
                                 ('M_gen', 0.274, 19.242), ('M_both', 0.267, 18.718)]:
    r = res(CFG, tag)
    exact_id = abs(r['floorRHS'] - math.sqrt((pw-1)*(r['Gamma2']-1))) <= 1e-12*r['floorRHS']
    ratio = (pw2*r['sqrt_G2m1'])/r['floorRHS']
    ok = approx(r['sqrt_G2m1'], exp_sqrt, ab=2e-3) and approx(r['floorRHS'], exp_floor, rel=1e-3) \
         and exact_id and abs(ratio-off) <= 1e-12
    check(f"floor {tag}: floorRHS = sqrt((p^w-1)(G2_Q-1)) EXACT; p^(w/2)-form off by exactly sqrt(p^w/(p^w-1))",
          ok, f"floorRHS={r['floorRHS']:.3f}  p^(w/2)*sqrt={pw2*r['sqrt_G2m1']:.3f}  rel offset {off-1:.2e}")
check("masking rescales ONLY sqrt(G2_Q-1) (0.371->0.274); sqrt(p^w-1)~=p^(w/2) factor is mask-independent",
      approx(rraw['sqrt_G2m1'], 0.371, ab=2e-3) and approx(rgen['sqrt_G2m1'], 0.274, ab=2e-3)
      and approx(pw2, 17**1.5, rel=1e-9),
      f"sqrt(p^w-1)={math.sqrt(pw-1):.3f} ~= p^(w/2)={pw2:.3f}")

# ===================================================================== §8 falsifier
print("\n== §8 FALSIFIER: over-pruning to the single largest exact class => full-support delta ==")
perf = masks(CFG)['perfiber']; best = None
for z, classes in perf.items():
    for kk, cnt in classes.items():
        if best is None or cnt > best[0]: best = (cnt, z, kk)
cnt, z0, _ = best
Nsingle = [0]*pw; Nsingle[z0] = cnt
rs = analyze(Nsingle, p, ww, nn, C, W, 'single')
check("falsifier: single largest exact class (all mass on ONE fiber) => PR = p^w-1 = 4912 (full support)",
      approx(rs['PR'], pw-1, rel=1e-6) and approx(rs['effsupp'], 1.0, ab=1e-6),
      f"PR={rs['PR']:.2f} of {rs['ndir']}, effsupp={rs['effsupp']:.4f}")
check("falsifier: triangle(masked-avg) = 1+L1/T = p^w = 4913 (delta spectrum, route vacuous)",
      approx(rs['tri_masked'], float(pw), rel=1e-6), f"tri_masked={rs['tri_masked']:.2f} = p^w={pw}")
check("falsifier structural precondition (rem:mass-aware-logmoment): mask must NOT produce a sparse-heavy residual",
      rs['PR'] == rs['ndir'], "sparse-heavy single-fiber => PR>>nu* for any finite K: masked route dies")

# ===================================================================== §9 tamper
print("\n== §9 tamper self-tests (each must FAIL when corrupted) ==")
def tamper(name, cond_should_fail, note=""):
    ok = not cond_should_fail
    print(f"  [{'PASS' if ok else 'FAIL'}] tamper::{name} (corruption detected)" + (f"  ({note})" if note else ""))
    CHECKS.append((f"tamper::{name}", ok, ""))
# 1. the M_gen "win" is a RAW-AVG-units artifact: in masked-avg units the triangle is 14.78 > budget
tamper("mgen_win_is_rawavg_artifact", rgen['tri_masked'] <= 8.4152,
       "tri_masked(M_gen)=14.78 > 8.4152; only tri_rawavg passes")
# 2. the raw primitive-L1 triangle EXCEEDS the M31 budget (that is the whole #413 point)
tamper("raw_L1_within_budget", tri_prim_raw <= 8.4152, "10.4728 > 8.4152")
# 3. nu*_ref off-by-one
tamper("nu_ref_offbyone", ((Krem-1)**2) == 23088082660035)
# 4. M_gen is a character projection (claim no frequency mixing)
tamper("mgen_is_projection", mixed == 0, "4880 mixed directions => support-side, not projection")
# 5. falsifier gives a SPARSE spectrum (claim PR < ndir)
tamper("falsifier_sparse", rs['PR'] < rs['ndir'], "single heavy class => FULL support delta, PR=ndir")
# 6. branch-4 quotient masking IMPROVES over raw (it worsens: 11.89 > 10.58)
tamper("quot_improves", rquot['tri_rawavg'] <= rraw['tri_rawavg'],
       "M_quot 11.89 > RAW 10.58: quotient cell alone worsens")
# 7. the p^{w/2} closed form is claimed EXACT (it is approximate; exact form is sqrt((p^w-1)(G2-1)))
tamper("floor_pw2_form_exact", abs(pw2*rgen['sqrt_G2m1'] - rgen['floorRHS']) < 1e-9,
       "p^(w/2)-form differs by exactly sqrt(p^w/(p^w-1)) (rel 1.0e-4 at toy)")

# ===================================================================== summary
npass = sum(1 for _, c, _ in CHECKS if c); ntot = len(CHECKS)
print(f"\nRESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot} checks)")
import sys; sys.exit(0 if npass == ntot else 1)
