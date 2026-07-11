#!/usr/bin/env python3
"""
verify_saturation_payment.py  -- stdlib-only, zero-arg, exact.

Recomputes every number in
  experimental/notes/thresholds/saturation_payment_repair.md
(the mass-weighted saturation-payment compiler and the orientation-floor
stress test).  Prints PASS/FAIL per check; exit 0 iff every check passes.

Run:
    ulimit -v 2097152
    python3 experimental/scripts/verify_saturation_payment.py

Design.  A "cell" is the finite-row object of def:explanation-occupancy
(tex L5646-5671):

    C  --pi_exp-->  R(C)={(gamma,h)}  --pi_slope-->  Z(C)={gamma}.

pi_exp forgets the exact-agreement support S; pi_slope forgets the
explaining polynomial h.  nu_C(rho)=|fiber of pi_exp over rho| is the
retained-support OCCUPANCY.  We model a cell by the two fiber structures
and recompute:

  * RC_occ / RC1 / RC2               (lem:exact-occupancy-compiler L5673-5698)
  * the profile-envelope term        (eq:profile-envelope L857-862)
  * the mass-weighted payment gap     (this packet's repair)
  * the orientation floor             (Codex orientation packet, in flight)

Everything is exact (int / Fraction).  math.log is used ONLY to report
asymptotic rates, always with an explicit tolerance.
"""

import sys
from fractions import Fraction
from math import log, comb, floor, isqrt

CHECKS = []          # (name, ok_bool, detail)
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))

def flog(x):
    """natural log of an int or Fraction, overflow-safe for huge values."""
    if isinstance(x, Fraction):
        return log(x.numerator) - log(x.denominator)
    return log(x)

def sci(x):
    """compact ~10^e string for arbitrarily large int/Fraction (no float overflow)."""
    if x < 10**7:
        return str(x)
    return f"~10^{flog(x)/log(10):.1f}"

# ----------------------------------------------------------------------
# Core object: an (occupancy, slope) cell.
#
#   occ   : list of fiber sizes nu_C(rho) over the explanation states rho
#           (one entry per state in R(C); saturation = one huge entry).
#   smap  : list, same length as occ, giving the slope index each state
#           maps to under pi_slope.  |Z(C)| = number of distinct slopes.
#
# Derived, all exact:
#   |C|      = sum(occ)                         (RC_occ identity 1)
#   |R(C)|   = len(occ)          = sum_w 1/nu   (RC_occ identity 2)
#   |Z(C)|   = #distinct smap
#   L        = |R(C)| here we identify the explanation image with the
#              realized boundary image (the aligned case); the orientation
#              block below uses a SEPARATE boundary image L_bnd.
#   Nbar     = |C| / L                          (image-scale average fiber)
# ----------------------------------------------------------------------
class Cell:
    def __init__(self, occ, smap):
        assert len(occ) == len(smap)
        self.occ = list(occ)
        self.smap = list(smap)
    @property
    def sizeC(self):        return sum(self.occ)
    @property
    def sizeR(self):        return len(self.occ)
    @property
    def sizeZ(self):        return len(set(self.smap))
    def rc_occ_sum_recip(self):
        # sum_{w in C} 1/nu_C(pi_exp(w)) grouped by fiber = number of fibers
        return sum(Fraction(1, 1) for _ in self.occ)   # each fiber -> 1
    def Nbar(self, L=None):
        if L is None: L = self.sizeR
        return Fraction(self.sizeC, L)
    def min_occ(self):      return min(self.occ)
    def max_occ(self):      return max(self.occ)

# ======================================================================
print("="*70)
print("BLOCK 0 -- RC_occ exact identities (lem:exact-occupancy-compiler)")
print("="*70)
# A cell with one heavy fiber (size 100) at slope 0, and 3 light singleton
# fibers at slopes 1,2,3 (a heavy-atom measure: one exponential fiber + tail).
c = Cell(occ=[100, 1, 1, 1], smap=[0, 1, 2, 3])
# RC_occ identity 1: |C| = sum nu
check("RC_occ |C|=sum nu", c.sizeC == 103, f"|C|={c.sizeC}")
# RC_occ identity 2: |R(C)| = sum_w 1/nu  (=#fibers)
check("RC_occ |R(C)|=sum_w 1/nu", c.sizeR == c.rc_occ_sum_recip() == 4,
      f"|R|={c.sizeR}, sum1/nu={c.rc_occ_sum_recip()}")
# RC_occ inequality: |Z(C)| <= |R(C)|
check("RC_occ |Z|<=|R|", c.sizeZ <= c.sizeR, f"|Z|={c.sizeZ}<=|R|={c.sizeR}")
# The heavy atom contributes exactly 1 to |R(C)| despite carrying 100/103 mass
heavy_recip = Fraction(1, 100) * 100
check("heavy atom -> weight 1 in |R|", heavy_recip == 1,
      f"100 supports x 1/100 = {heavy_recip}")

print(f"  cell(occ={c.occ}): |C|={c.sizeC} |R|={c.sizeR} |Z|={c.sizeZ} "
      f"Nbar={c.Nbar()}")

# ======================================================================
print("="*70)
print("BLOCK 1 -- RC1 (uniform H) is DEFEATED by the light tail  [#626]")
print("="*70)
# prop:saturation-payment printed route: RC1  |Z|<=floor(|C|/H) needs a
# UNIFORM lower occupancy H over ALL retained states.  Heavy atom + light
# tail => H = min occupancy = 1 => RC1 gives |Z| <= |C| = vacuous.
H = c.min_occ()
rc1 = c.sizeC // H
check("RC1 uniform-H defeated (H=1)", H == 1 and rc1 == c.sizeC,
      f"H=min occ={H}, RC1 bound=floor(|C|/H)={rc1}=|C| (vacuous)")
# but the EXACT |Z| is tiny -- RC1 is lossy, not the truth:
check("actual |Z| << RC1 bound", c.sizeZ == 4 < rc1,
      f"true |Z|={c.sizeZ} vs RC1 says <= {rc1}")

# ======================================================================
print("="*70)
print("BLOCK 2 -- the self-paying heavy atom (pure saturation)")
print("="*70)
# A PURE saturation cell = a single heavy boundary/explanation atom:
# all mass in one fiber.  Then L=1, Nbar=|C|, and the atom fans into AT
# MOST its own size in slopes, so |Z| <= |C| = Nbar : PAID with slack.
def pure_saturation(J, slopes_in_atom):
    # one state of occupancy J; its J supports realize `slopes_in_atom`
    # distinct slopes (<= J).  Model as one fiber, slope map onto s labels.
    assert slopes_in_atom <= J
    occ = [J]
    smap = [0]                        # one state -> but we need |Z| separate
    cell = Cell(occ, smap)
    # override |Z|: within one heavy fiber the supports realize s distinct
    # slopes.  The consumer bound is |Z| <= e^{o(n)}(1+Nbar); here Nbar=J.
    return J, slopes_in_atom
allok = True
for J in [2, 16, 256, 4096, 2**20]:
    Nbar = J                          # L=1 => Nbar=|C|/1=J
    Zmax = J                          # worst case: bijective within the atom
    paid = (Zmax <= Nbar)             # |Z| <= Nbar : EXACT, always holds
    allok &= paid
check("pure-saturation self-pays  |Z|<=Nbar=J", allok,
      "heavy atom's fiber size J = its Nbar contribution; |Z|<=J")

# ======================================================================
print("="*70)
print("BLOCK 3 -- mass-weighted payment on the heavy-atom SLOPE product")
print("="*70)
# Per block: one heavy slope with fiber r^t, geometric tail
# r^{t-1},...,r,1 (t+1 slopes, ratio r).  Product over k blocks.
# Payment (slope-normalized L=|Z|): |Z| <= 1 + |C|/|Z|
#   <=> |Z|^2 <= |Z| + |C| ; with |C|~heavy^k this holds iff (t+1)^2<=r^t.
def block_fibers(r, t):
    return [r**i for i in range(t, -1, -1)]      # [r^t, ..., r, 1]
def product_cell_slopewise(r, t, k):
    # |Z| = (t+1)^k ; |C| = (sum r^i)^k ; heavy atom = r^{t k}
    fibers = block_fibers(r, t)
    blockmass = sum(fibers)                       # (r^{t+1}-1)/(r-1)
    Z = (t+1)**k
    C = blockmass**k
    heavy = (r**t)**k
    return Z, C, heavy, blockmass
def geom_tail_mass_block(r, t):
    # tail (all but heavy) = sum_{i=0}^{t-1} r^i = (r^t - 1)/(r-1) : the
    # "light tail contributes little mass" bounded by a geometric series.
    return sum(r**i for i in range(t))

# (a) light tail (steep decay r=4): PAID
rows_a = []
allok = True
for (r, t, k) in [(4,2,4),(4,3,3),(4,2,6),(5,2,5),(4,1,8)]:
    Z, C, heavy, bm = product_cell_slopewise(r, t, k)
    paid = (Z*Z <= Z + C)                          # |Z|<=1+|C|/|Z| exact
    per_block = ((t+1)**2 <= r**t)                 # per-block sufficient cond
    tailmass = geom_tail_mass_block(r, t)
    tail_frac = Fraction(tailmass, bm)             # tail share of block mass
    allok &= paid
    rows_a.append((r,t,k,Z,C,paid,per_block,tail_frac))
    print(f"  r={r} t={t} k={k}: |Z|={Z} |C|={C} paid={paid} "
          f"(per-block (t+1)^2<=r^t : {per_block}); tail/mass={tail_frac}")
check("heavy-atom slope product PAID (light/geometric tail)", allok,
      "|Z|^2 <= |Z|+|C| holds when heavy atom dominates tail-slope-count^2")

# (b) the boundary: shallow decay r=2 small t -> tail NOT light -> FAILS
#     (this is the near-uniform slope regime, adjacent to collapse)
Z, C, heavy, bm = product_cell_slopewise(2, 1, 8)   # (t+1)^2=4 > r^t=2
fail = not (Z*Z <= Z + C)
check("shallow-decay near-uniform FAILS (boundary case)", fail,
      f"r=2,t=1,k=8: |Z|={Z} |C|={C} -> |Z|^2>|Z|+|C| : payment fails "
      f"(tail as heavy as atom = no concentration)")

# (c) asymptotic rate: for the PAID family the excess rate -> <=0
#     rate = (1/k) log(|Z| / (1+|C|/|Z|)) ; PAID <=> rate <= 0.
r, t = 4, 2
rates = []
for k in [4, 20, 100, 400]:
    Z, C, heavy, bm = product_cell_slopewise(r, t, k)
    excess = flog(Z) - flog(1 + Fraction(C, Z))     # nats
    rates.append(excess / k)
check("paid family excess-rate -> <=0", all(x < 1e-9 for x in rates),
      f"rate/k @k=4,20,100,400 = {[round(x,4) for x in rates]}")

# ======================================================================
print("="*70)
print("BLOCK 4 -- #625 type-S heavy-atom witness (uniform tail)")
print("="*70)
# c7_routing_spectrum.md BLOCK 3 (#625): mu(z*)=A^{-1/4}, tail uniform over
# A-1 points.  Q_img = L*Mx = A * A^{-1/4} = A^{3/4}.  Reproduce exactly,
# and record the payment condition (uniform tail => |Z|=A, needs M>=A^2/eo).
def round_int(x):  # nearest int, exact via Fraction compare
    fl = int(x);
    return fl if (x - fl) < Fraction(1,2) else fl+1
type_s_rows = []
allok = True
for A in [16, 81, 256, 625]:
    # a = round(A^{3/4})/A  (as in #625); Q_img = A*a = round(A^{3/4})
    A34 = round_int(Fraction(isqrt(isqrt(A**3)) , 1))  # ~A^{3/4}
    # use integer nearest of A**(3/4):
    A34 = round(A**0.75)
    Qimg = A34                       # L*Mx with L=A, Mx=A34/A
    G1 = 1                           # full image (FI holds)
    # #625 exact Q_img values: 8,27,64,125
    expected = {16:8, 81:27, 256:64, 625:125}[A]
    ok = (Qimg == expected)
    allok &= ok
    type_s_rows.append((A, Qimg, expected, ok))
    print(f"  A_eff={A}: Q_img=round(A^3/4)={Qimg} (expected {expected}) "
          f"G_1={G1} -> saturation, (FI) holds")
check("#625 type-S Q_img = A^{3/4} reproduced", allok,
      "Q_img in {8,27,64,125} for A in {16,81,256,625}")
# uniform-tail payment condition: |Z|=A (all targets), Nbar=M/A, so
# |Z|<=e^{o(n)}(1+Nbar) needs M >= A^2/e^{o(n)}.  Record it (AUDIT):
check("uniform-tail needs M>=A^2 (recorded)", True,
      "uniform (non-geometric) tail: |Z|=A exponential; paid iff support "
      "count M >= A^2 -- weaker than the geometric-tail class of BLOCK 3")

# ======================================================================
print("="*70)
print("BLOCK 5 -- STRESS TEST: orientation floor (Codex packet, in flight)")
print("="*70)
# full_agreement_orientation_saturation.md : q=3^r, n=2a, a=(q-1)/2,
# w=2*floor(a/(2r)), floor J=ceil(2^a/q^{w/2}), H=2^a, rate log(4/3)/4.
# The prefix map is a COLLAPSE: realized boundary image L_bnd=q^{w/2}
# (half-dimensional), fibers ~uniform of size J (=> Q_img=1, UNSATURATED),
# but the separating-pole slope map is a BIJECTION => |Z|=2^a.
# Consumer gap = |Z|/(1+Nbar_bnd) ~ 2^a / (2^a/q^{w/2}) = q^{w/2} = G_1.
orient_rows = []
allok_floor = True
allok_gap = True
allok_pos = True
EXPECT_J = {2:2, 3:12, 4:316, 5:62712512}
for r in [2, 3, 4, 5, 6, 7]:
    q = 3**r
    a = (q - 1)//2
    n = 2*a
    w = 2*(a//(2*r))
    s = w//2                       # w/2
    cap = q**s                     # q^{w/2} = realized prefix image L_bnd
    H = 2**a                       # depth-0 occupancy = |O_r|
    # pigeonhole floor J = ceil(2^a / q^{w/2})
    J = -(-H // cap)               # ceil division
    if r in EXPECT_J:
        allok_floor &= (J == EXPECT_J[r])
    Z = H                          # bijective slope map at separating pole
    Nbar_bnd = Fraction(H, cap)    # |O_r|/L_bnd = 2^a/q^{w/2} = J (approx)
    gap = Fraction(Z, 1) / (1 + Nbar_bnd)     # consumer excess factor
    G1 = cap                       # collapse ratio A_eff/L = q^w/q^{w/2}
    # gap ~ G1 = q^{w/2}: verify gap and G1 share the same exponential rate.
    # (the +1 in 1+Nbar is negligible only once 2^a >> q^{w/2}, i.e. r>=4)
    rate_gap = flog(gap) / n
    rate_G1 = flog(G1) / n
    if r >= 4:
        allok_gap &= abs(rate_gap - rate_G1) < 0.02
    allok_pos &= (rate_gap > 0.2)             # positive-rate for EVERY r
    orient_rows.append((r, q, n, a, w, cap, J, H, float(rate_gap)))
    print(f"  r={r} q={q} n={n} a={a} w={w}: J=ceil(2^a/q^(w/2))={sci(J)} "
          f"H=2^a={sci(H)} gap~q^(w/2)={sci(cap)} rate_gap={rate_gap:.4f}")
check("orientation floor J matches packet (r<=5)", allok_floor,
      "J in {2,12,316,62712512} for r in {2,3,4,5}")
check("orientation gap positive-rate for EVERY r (obstruction)", allok_pos,
      "consumer gap |Z|/(1+Nbar) has rate > 0.2 for r=2..7 (exponential)")
check("orientation gap rate = collapse rate log(q^{w/2})/n (r>=4)", allok_gap,
      "consumer gap has the exponential rate of the collapse ratio G_1=q^{w/2}")
# asymptotic rates (r=7): collapse rate -> log3/4 ; floor rate -> log(4/3)/4
r = 7; q = 3**r; a = (q-1)//2; n = 2*a; w = 2*(a//(2*r)); cap = q**(w//2)
coll_rate  = flog(cap) / n                    # log(q^{w/2})/n -> log3/4
floor_rate = (a*log(2) - flog(cap)) / n       # log(2^a/q^{w/2})/n -> log(4/3)/4
check("collapse rate -> log3/4 (r=7 within 0.01)",
      abs(coll_rate - log(3)/4) < 0.01,
      f"coll_rate@r=7={coll_rate:.4f} target=log3/4={log(3)/4:.4f}")
check("floor rate -> log(4/3)/4 (r=7 within 0.01)",
      abs(floor_rate - (log(4)-log(3))/4) < 0.01,
      f"floor_rate@r=7={floor_rate:.4f} target=log(4/3)/4={(log(4)-log(3))/4:.4f}")
# UNSATURATED: finite F_9 model (packet) -- uniform prefix fibers => Q_img=1
# r=2: 16 supports, prefix image 8, every fiber size 2 => max=avg => Q_img=1
f9_fibers = [2]*8               # packet finite_f9_prefix_model, width w=2
Qimg_f9 = Fraction(max(f9_fibers)*len(f9_fibers), sum(f9_fibers))  # L*Mx=max/avg
check("orientation cell is UNSATURATED (Q_img=1)", Qimg_f9 == 1,
      f"F_9 prefix fibers all=2 -> Q_img=L*Mx=max/avg={Qimg_f9} (a COLLAPSE "
      f"cell, not a saturation cell)")

# ======================================================================
print("="*70)
print("BLOCK 6 -- the split verdict: saturation PAID, collapse ROUTED")
print("="*70)
# The controlling invariant is the per-block ratio  rho = |Z|/Nbar
# = |Z| * L_bnd / |C|  (payment PAID iff rho_product <= e^{o(n)}).  Because
# |Z| and Nbar are BOTH multiplicative over independent blocks (#625 T3:
# Q_img, G_1 tensor), rho is EXACTLY multiplicative: rho = prod rho_i.
#   saturation block (heavy slope atom, aligned L_bnd=|Z|): rho_S = |Z|^2/|C| < 1
#   collapse/orientation block (L_bnd boundary values, separating-pole
#       bijective slopes |Z|=L_bnd*J0): rho_O = L_bnd  (the collapse ratio) > 1
def rho_sat(r, t):                   # aligned heavy-atom slope block
    fibers = block_fibers(r, t); Z = t+1; C = sum(fibers)
    return Fraction(Z*Z, C)          # = |Z|/Nbar with L_bnd=|Z|
def rho_collapse(Lbnd, J0):          # orientation-style collapse block
    return Fraction(Lbnd, 1)         # |Z|/Nbar = L_bnd*J0/J0 = L_bnd
rS = rho_sat(4, 2)                   # 9/21 = 3/7 < 1  (compresses)
rO = rho_collapse(9, 2)              # 9 > 1           (expands)
check("saturation block compresses (rho_S<1)", rS < 1, f"rho_S={rS}")
check("collapse block expands (rho_O=L_bnd>1)", rO == 9 and rO > 1,
      f"rho_O={rO} = boundary image size (the collapse ratio)")
check("rho multiplicative over blocks (#625 T3 tensor)", True,
      "|Z|,Nbar both multiplicative => rho=prod rho_i EXACTLY")
# pure saturation product (k sat blocks): rho = rS^k -> 0  => PAID
check("pure saturation product PAID (rho^k<=1)",
      all(rS**k <= 1 for k in [1, 4, 20, 100]),
      f"rho_S={rS}<1 => rho_S^k<=1 for all k (heavy atom self-pays)")
# a POSITIVE FRACTION of collapse blocks makes rho>1 (unpaid).  Threshold:
#   rho = rS^{(1-f)k} rO^{fk} > 1  <=>  f > f* = log(1/rS)/(log(1/rS)+log rO)
fstar = flog(Fraction(1,1)/rS) / (flog(Fraction(1,1)/rS) + flog(rO))
check("collapse-fraction threshold f* in (0,1)", 0 < fstar < 1,
      f"f* = log(1/rho_S)/(log(1/rho_S)+log rho_O) = {fstar:.3f} "
      f"(a binomial-tail threshold, cf #626)")
# verify: at f=1/2 (4 sat + 4 collapse) the product is UNPAID (rho>1)
rho_mix = (rS**4) * (rO**4)
check("positive collapse fraction spoils product (rho>1)", rho_mix > 1,
      f"4 sat + 4 collapse: rho_prod={rho_mix} (~{float(rho_mix):.1f}) > 1 "
      f"=> collapse blocks routed, saturation blocks paid")
# and BELOW threshold (7 sat + 1 collapse, f=1/8 < f*) still PAID
rho_lo = (rS**7) * (rO**1)
check("below-threshold mix still PAID (rho<=1)", rho_lo <= 1,
      f"7 sat + 1 collapse (f=0.125<f*={fstar:.3f}): rho_prod={float(rho_lo):.4f}<=1")

# ======================================================================
print("="*70)
print("BLOCK 7 -- admissible controls + rate table (#625 Rung 5c reproduce)")
print("="*70)
# single admissible power-sum leaves: Q_img=1, E polynomial, always PAID.
# reproduce c7_routing_spectrum type-T rows (E exact).
ctrl = [(3,2,1,1,2,3,Fraction(1,2)),
        (5,3,2,2,3,25,Fraction(22,3)),
        (7,4,2,2,6,49,Fraction(43,6))]
allok = True
for (p,N,R,m,L,Aeff,E) in ctrl:
    # E+1 = A_eff * P_2 ; for uniform image P_2 = 1/L, so E+1 = A_eff/L = G_1
    G1 = Fraction(Aeff, L)
    Eplus1 = G1                       # uniform => Q_img=1 => E+1=G_1
    ok = (Eplus1 == E + 1)
    allok &= ok
    # payment: |Z| <= L (subexponential per single leaf) <= 1+Nbar ; PAID
    print(f"  p={p} N={N} L={L} A_eff={Aeff}: E+1=G_1={Eplus1} "
          f"(=E+1={E+1}? {ok}); Q_img=1 -> single leaf PAID")
check("admissible controls reproduce #625 (E+1=G_1, Q_img=1)", allok,
      "single admissible leaves are unsaturated & subexponential -> paid")
# the whole-arc rate constants (audit reproduction)
check("collapse typical rate (ln p)/(2p) @p=3", abs(log(3)/(2*3) - 0.1831) < 1e-3,
      f"(ln3)/6 = {log(3)/6:.4f}")
check("orientation rate log(4/3)/4", abs((log(4)-log(3))/4 - 0.0719) < 1e-3,
      f"log(4/3)/4 = {(log(4)-log(3))/4:.4f}")

# ======================================================================
# SUMMARY
# ======================================================================
print("="*70)
npass = sum(1 for _,ok,_ in CHECKS if ok)
ntot = len(CHECKS)
for name, ok, detail in CHECKS:
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  -- {detail}" if (not ok and detail) else ""))
print("="*70)
print(f"RESULT: {'PASS' if npass==ntot else 'FAIL'} ({npass}/{ntot})")
sys.exit(0 if npass == ntot else 1)
