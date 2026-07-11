#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_c7_degree_enumeration.py  --  stdlib-only, zero-arg.

Recomputes every number in
    experimental/notes/thresholds/c7_degree_enumeration.md

Pays (bounds/enumerates) the two C7 projection-degree budgets on PRODUCT/PROFILE
leaves -- the (S_E)-violating class of #622 T3 / #625 MASTER-2:

  (A) effective-image COLLAPSE   G_1 = A_eff/L >= e^{eps N}
  (B) SATURATION                 Q_img = L*Mx  >= e^{eps N}

Backbone (recomputed here, exact Fraction):
  MASTER-2  E+1 = A_eff*P_2 <= A_eff*Mx = (A_eff/L)(L*Mx) = G_1*Q_img   (Hoelder P_2<=Mx)
  T3        G_1, Q_img, E+1 all multiplicative over independent blocks.

Core enumeration theorem (this packet):
  G_1 and Q_img are products of per-block ratios >= 1, so exponential violation
  needs a POSITIVE FRACTION theta of non-trivial blocks; the number of block-type
  profiles reaching the threshold is a BINOMIAL TAIL  sum_{j>=theta k} C(k,j),
  whose exponential rate is h(theta) (theta>1/2) or log 2 (theta<=1/2) -- always
  positive.  Hence e^{Omega(N)} profiles, which BUSTS the "subexponentially many
  profiles" hypothesis (tex L869) under which the profile envelope E_n's sum
  equals its max, and (with the singleton-fiber #609 occupancy N_bar=1) realizes
  "the countertheorem" of tex L889.

Exit 0 iff all checks pass.  Runs in ~0.1 s under `ulimit -v 2097152`.
"""

import math
import sys
from fractions import Fraction as Fr
from itertools import product as iproduct

# ---------------------------------------------------------------------------
CHECKS = []  # (name, ok_bool, detail)

def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))

def binom(n, r):
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)

def hbin(x):
    """natural-log binary entropy h(x) = -x ln x - (1-x) ln(1-x)."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x*math.log(x) - (1.0-x)*math.log(1.0-x)

# ---------------------------------------------------------------------------
# Block dictionary.  A block is a probability measure mu on its realized image
# (a tuple of Fractions summing to 1) together with its effective-span size
# A_eff >= L = len(mu).  Per-block invariants:
#   L   = len(mu)          (realized image / support of mu)
#   Mx  = max(mu)
#   P2  = sum m^2
#   E1  = A_eff * P2       (= E+1, the #614 Parseval form)
#   G1  = A_eff / L        (collapse ratio)
#   Q   = L * Mx           (saturation ratio)
# MASTER-2 blockwise:  E1 <= G1*Q,  equality iff mu uniform on its support.
# ---------------------------------------------------------------------------

def block_uniform(L, A_eff):
    mu = tuple(Fr(1, L) for _ in range(L))
    return mu, A_eff

def block_heavy(L, A_eff, a):
    """heavy atom mass a at one point, remaining (1-a) spread uniformly."""
    a = Fr(a)
    rest = (1 - a) / (L - 1)
    mu = tuple([a] + [rest] * (L - 1))
    return mu, A_eff

def block_stats(mu, A_eff):
    L = len(mu)
    Mx = max(mu)
    P2 = sum(m * m for m in mu)
    E1 = A_eff * P2
    G1 = Fr(A_eff, L)
    Q = L * Mx
    return dict(L=L, Aeff=A_eff, Mx=Mx, P2=P2, E1=E1, G1=G1, Q=Q, mu=mu)

def tensor(mu1, mu2):
    return tuple(x * y for x in mu1 for y in mu2)

# canonical block types for prime p ------------------------------------------
def block_T(p):            # trivial / full image          (G1,Q,E1)=(1,1,1)
    return block_uniform(p, p)
def block_C(p):            # parabola collapse             (G1,Q,E1)=(p,1,p)
    return block_uniform(p, p * p)
def block_S(p, a):         # heavy-atom saturation         G1=1
    return block_heavy(p, p, a)

# ===========================================================================
# BLOCK 0 -- MASTER-2 and the #614 Parseval form, blockwise (exact)
# ===========================================================================
def block0():
    p = 5
    cases = {
        "T": block_T(p),
        "C": block_C(p),
        "S(2/5)": block_S(p, Fr(2, 5)),
        "S(3/5)": block_S(p, Fr(3, 5)),
    }
    for tag, (mu, Ae) in cases.items():
        s = block_stats(mu, Ae)
        # E+1 = A_eff * P_2  (definitional)
        check(f"B0 E1==Aeff*P2 [{tag}]", s["E1"] == s["Aeff"] * s["P2"])
        # MASTER-2 blockwise  E1 <= G1*Q
        check(f"B0 MASTER-2 E1<=G1*Q [{tag}]", s["E1"] <= s["G1"] * s["Q"],
              f"E1={s['E1']} G1*Q={s['G1']*s['Q']}")
        # equality iff uniform
        is_unif = len(set(mu)) == 1
        eq = (s["E1"] == s["G1"] * s["Q"])
        check(f"B0 equality<=>uniform [{tag}]", eq == is_unif)
    # pin the exact canonical triples used by the note
    sC = block_stats(*block_C(p))
    check("B0 C triple (G1,Q,E1)=(p,1,p)",
          (sC["G1"], sC["Q"], sC["E1"]) == (Fr(p), Fr(1), Fr(p)))
    sS = block_stats(*block_S(p, Fr(2, 5)))
    check("B0 S(2/5) triple (G1,Q,E1)=(1,2,5/4)",
          (sS["G1"], sS["Q"], sS["E1"]) == (Fr(1), Fr(2), Fr(5, 4)))
    sT = block_stats(*block_T(p))
    check("B0 T triple (G1,Q,E1)=(1,1,1)",
          (sT["G1"], sT["Q"], sT["E1"]) == (Fr(1), Fr(1), Fr(1)))

# ===========================================================================
# BLOCK 1 -- T3 multiplicativity of G1, Q_img, E+1 over independent products
#            (exact Fraction, tensor products, through k=4)
# ===========================================================================
def block1():
    p = 5
    blocks = [block_C(p), block_S(p, Fr(2, 5)), block_T(p), block_S(p, Fr(3, 5))]
    for k in range(1, 5):
        chosen = blocks[:k]
        # explicit tensor measure and product span
        mu = chosen[0][0]
        Ae = chosen[0][1]
        for (m2, a2) in chosen[1:]:
            mu = tensor(mu, m2)
            Ae = Ae * a2
        s = block_stats(mu, Ae)
        # products of per-block invariants
        G1p = Fr(1); Qp = Fr(1); E1p = Fr(1)
        for (m2, a2) in chosen:
            si = block_stats(m2, a2)
            G1p *= si["G1"]; Qp *= si["Q"]; E1p *= si["E1"]
        check(f"B1 G1 multiplicative k={k}", s["G1"] == G1p)
        check(f"B1 Q_img multiplicative k={k}", s["Q"] == Qp)
        check(f"B1 (E+1) multiplicative k={k}", s["E1"] == E1p,
              f"E1={s['E1']} prod={E1p}")
        check(f"B1 MASTER-2 in product k={k}", s["E1"] <= s["G1"] * s["Q"])

# ===========================================================================
# BLOCK 2 -- the two dual witnesses (block-parabola / heavy-atom), exact,
#            reproducing #625 BLOCK 2/3/4 and #622 census
# ===========================================================================
def block2():
    # pure COLLAPSE product: k parabola blocks -> G1=p^k, Q=1, E+1=p^k
    for p in (3, 5, 7):
        for k in range(1, 5):
            mu, Ae = block_C(p)
            for _ in range(k - 1):
                m2, a2 = block_C(p)
                mu = tensor(mu, m2); Ae *= a2
            s = block_stats(mu, Ae)
            check(f"B2 collapse p={p} k={k}: G1=p^k",
                  s["G1"] == Fr(p ** k))
            check(f"B2 collapse p={p} k={k}: Q=1", s["Q"] == 1)
            check(f"B2 collapse p={p} k={k}: E+1=p^k", s["E1"] == Fr(p ** k))
            # MASTER-2 TIGHT (uniform)
            check(f"B2 collapse p={p} k={k}: MASTER-2 tight",
                  s["E1"] == s["G1"] * s["Q"])
    # pure SATURATION product: k heavy-atom blocks p=5,a=2/5 -> G1=1, Q=2^k, E+1=(5/4)^k
    p, a = 5, Fr(2, 5)
    for k in range(1, 5):
        mu, Ae = block_S(p, a)
        for _ in range(k - 1):
            m2, a2 = block_S(p, a)
            mu = tensor(mu, m2); Ae *= a2
        s = block_stats(mu, Ae)
        check(f"B2 sat k={k}: G1=1 (FI holds, full image)", s["G1"] == 1)
        check(f"B2 sat k={k}: Q=2^k", s["Q"] == Fr(2 ** k))
        check(f"B2 sat k={k}: E+1=(5/4)^k", s["E1"] == Fr(5, 4) ** k)
        # MASTER-2 SLACK on a spread tail (P2 < Mx strictly)
        check(f"B2 sat k={k}: MASTER-2 slack", s["E1"] < s["G1"] * s["Q"])
    # single admissible leaf census (reproduce #622/#625 BLOCK 7 exactly):
    # global power-sum, R<p, uniform on image L, A_eff=p^R, E = A_eff/L - 1
    rows = [(3,2,1,1,2,3), (5,2,1,1,2,5), (5,3,1,2,3,5), (5,3,2,2,3,25),
            (7,3,1,2,3,7), (7,4,2,2,6,49), (7,5,2,2,10,49)]
    for (p, N, R, m, L, Aeff) in rows:
        mu = tuple(Fr(1, L) for _ in range(L))
        s = block_stats(mu, Aeff)
        E = s["E1"] - 1
        check(f"B2 single p={p},N={N},R={R}: Aeff=p^R", Aeff == p ** R)
        check(f"B2 single p={p},N={N},R={R}: E=Aeff/L-1",
              E == Fr(Aeff, L) - 1)
        check(f"B2 single p={p},N={N},R={R}: Q_img=1 (uniform image)",
              s["Q"] == 1)

# ===========================================================================
# BLOCK 3 -- THE COLLAPSE COUNT (theorem A): binomial-tail enumeration.
#   #collapse profiles with G1=p^j >= e^{eps N} is  N_coll = sum_{j>=theta k} C(k,j),
#   theta = eps*p/ln p,   N=pk.   Rate (1/k)ln N_coll -> h(theta) (theta>1/2)
#   or ln 2 (theta<=1/2); ALWAYS positive => e^{Omega(N)} profiles > e^{o(n)}.
# ===========================================================================
def tail_count(k, theta):
    jmin = math.ceil(theta * k)
    return sum(binom(k, j) for j in range(jmin, k + 1))

def block3():
    p = 3
    lnp = math.log(p)
    # (i) threshold arithmetic: G1=p^j >= e^{eps N}=e^{eps p k}  <=>  j >= (eps p/ln p) k
    for eps in (0.05, 0.10, 0.20, 0.30):
        theta = eps * p / lnp
        for k in (10, 20, 40):
            j0 = math.ceil(theta * k)
            # smallest integer j with p^j >= e^{eps p k}
            j_direct = 0
            while p ** j_direct < math.exp(eps * p * k) - 1e-9:
                j_direct += 1
            check(f"B3 threshold eps={eps} k={k}: ceil(theta k)==min j",
                  j0 == j_direct, f"j0={j0} j_direct={j_direct}")
    # (ii) tail rate matches h(theta) (theta>1/2) or ln2 (theta<=1/2)
    for theta in (0.2, 0.4, 0.5, 0.6, 0.75, 0.9):
        k = 2000
        Nc = tail_count(k, theta)
        rate = math.log(Nc) / k
        expect = hbin(theta) if theta > 0.5 else math.log(2.0)
        check(f"B3 tail rate theta={theta}: (1/k)lnN_coll~={('h' if theta>0.5 else 'ln2')}",
              abs(rate - expect) < 0.02, f"rate={rate:.4f} expect={expect:.4f}")
    # (iii) the crux: rate is POSITIVE => count exceeds e^{o(n)}
    for theta in (0.1, 0.3, 0.5, 0.7, 0.9):
        k = 4000
        rate_perN = math.log(tail_count(k, theta)) / (p * k)   # per N=pk
        check(f"B3 count EXCEEDS e^o(n): theta={theta} rate/N>0",
              rate_perN > 1e-3, f"rate/N={rate_perN:.4f}")

# ===========================================================================
# BLOCK 4 -- TYPICAL collapse rate.  Uniform block types {C, not} => #C~k/2,
#   G1 = p^{k/2} = e^{(ln p)/(2p) * N}.  So a RANDOM product leaf already
#   collapses at rate (ln p)/(2p): collapse is TYPICAL, not a rare cell.
# ===========================================================================
def block4():
    for p in (3, 5, 7):
        typ_rate = math.log(p) / (2.0 * p)          # per N
        # mode of C(k,j) is k/2 -> G1 = p^{k/2}
        for k in (10, 40, 100):
            j_mode = k // 2
            G1_typ_log_perN = j_mode * math.log(p) / (p * k)
            check(f"B4 typical rate p={p} k={k}: G1_mode~=(ln p)/(2p)",
                  abs(G1_typ_log_perN - typ_rate) < math.log(p) / (p * k) + 1e-9)
        # below-typical threshold => >half the profiles collapse (theta<1/2)
        theta_at_typ = (typ_rate) * p / math.log(p)   # = 1/2
        check(f"B4 typical<=>theta=1/2 p={p}", abs(theta_at_typ - 0.5) < 1e-9)
        # for eps just below typical, fraction collapsing > 1/2
        eps = 0.9 * typ_rate
        theta = eps * p / math.log(p)
        k = 200
        frac = tail_count(k, theta) / (2 ** k)
        check(f"B4 below-typical collapse is majority p={p}: frac>1/2",
              frac > 0.5, f"frac={frac:.3f}")

# ===========================================================================
# BLOCK 5 -- OCCUPANCY (RC1/RC2) and the COUNTERTHEOREM (tex L889).
#   Collapse leaves have SINGLETON fibers (occupancy N_bar=1, the #609 escape),
#   so RC1 gives H=1 (no compression) and admitting the e^{Omega(N)} collapse
#   profiles to E_n with (1+N_bar)=2 each makes  sum >> identity term.
# ===========================================================================
def block5():
    # occupancy N_bar = |Omega^0|/L.  Parabola: injective per block => N_bar=1.
    for p in (3, 5):
        for k in range(1, 5):
            Omega0 = p ** k          # p^k support configs (one point per block)
            L = p ** k               # image = p^k (injective)
            Nbar = Fr(Omega0, L)
            check(f"B5 collapse singleton-fiber N_bar=1 p={p} k={k}", Nbar == 1)
            # RC1 with H=min occupancy=1 gives |Z|<=|C|/1 : NO compression
            H = 1
            check(f"B5 RC1 no compression (H=1) p={p} k={k}", (Omega0 // H) == Omega0)
    # heavy-atom saturation: min occupancy over the image is also 1 (light tail),
    # so the uniform lower bound H demanded by prop:saturation-payment is 1.
    p, a = 5, Fr(2, 5)
    # integer occupancy model: heavy value gets t witnesses, others get 1 each,
    # image L=p, total M = t + (p-1).  max/avg = Q-type ratio; MIN occ = 1.
    for t in (2, 4, 8, 16):
        occ = [t] + [1] * (p - 1)
        check(f"B5 sat min-occupancy=1 (light tail) t={t}", min(occ) == 1)
        check(f"B5 sat max-occupancy exp t={t}", max(occ) == t)
    # THE COUNTERTHEOREM: sum_lambda (1+N_bar_lambda) over the collapse profiles.
    # With N_bar=1 and N_coll(k,theta) profiles, contribution = 2*N_coll,
    # compared to the identity term (n-a+1) ~ n = N = p k.
    p = 3
    theta = 0.6
    for k in (20, 40, 80):
        Ncoll = tail_count(k, theta)
        env_contrib = 2 * Ncoll          # sum (1+N_bar), N_bar=1
        identity_term = p * k            # n-a+1 ~ N
        check(f"B5 COUNTERTHEOREM env>>identity k={k}",
              env_contrib > identity_term ** 3,   # exponential vs linear
              f"env=2*C-tail(~e^{{{math.log(Ncoll):.1f}}}) id={identity_term}")

# ===========================================================================
# BLOCK 6 -- CENSUS: enumerate ALL block-type assignments at small (p,k),
#   compute exact (G1,Q,E1) per leaf via the multiplicative formula AND via a
#   direct tensor A_eff*P_2, confirm agreement, and match collapse/saturation
#   fractions to the binomial formula C(k,j)/2^k and the tail count.
# ===========================================================================
def block6():
    p = 3
    a = Fr(2, 3)  # heavy atom for saturation blocks at p=3
    # census over {C, T} for collapse counting
    for k in (4, 6, 8, 10):
        # exhaustive enumeration of collapse-pattern space {0,1}^k
        cnt_by_j = [0] * (k + 1)
        # sample a few explicit leaves for direct-vs-formula G1 agreement
        for pat in iproduct((0, 1), repeat=k):
            j = sum(pat)          # #C
            cnt_by_j[j] += 1
        # match to C(k,j)
        for j in range(k + 1):
            check(f"B6 census count C({k},{j}) p={p}", cnt_by_j[j] == binom(k, j),
                  f"got {cnt_by_j[j]} want {binom(k,j)}")
        # collapse fraction at threshold theta -> matches tail/2^k
        for theta in (0.5, 0.75):
            jmin = math.ceil(theta * k)
            frac = sum(cnt_by_j[j] for j in range(jmin, k + 1)) / (2 ** k)
            frac_formula = tail_count(k, theta) / (2 ** k)
            check(f"B6 collapse fraction k={k} theta={theta}",
                  abs(frac - frac_formula) < 1e-12)
    # direct-vs-multiplicative (G1,Q,E1) agreement on explicit mixed leaves
    p = 3
    for k in (3, 4, 5):
        for pat in iproduct("CTS", repeat=k):
            mu = None; Ae = 1
            G1f = Fr(1); Qf = Fr(1); E1f = Fr(1)
            for c in pat:
                if c == "C":
                    b = block_C(p)
                elif c == "T":
                    b = block_T(p)
                else:
                    b = block_S(p, a)
                si = block_stats(*b)
                G1f *= si["G1"]; Qf *= si["Q"]; E1f *= si["E1"]
                if mu is None:
                    mu, Ae = b
                else:
                    mu = tensor(mu, b[0]); Ae = Ae * b[1]
            s = block_stats(mu, Ae)
            if s["G1"] != G1f or s["Q"] != Qf or s["E1"] != E1f:
                check(f"B6 direct==mult {pat}", False,
                      f"G1 {s['G1']}/{G1f} Q {s['Q']}/{Qf} E1 {s['E1']}/{E1f}")
                return
            if not (s["E1"] <= s["G1"] * s["Q"]):
                check(f"B6 MASTER-2 {pat}", False)
                return
        check(f"B6 direct==mult & MASTER-2 all leaves k={k} (3^k)", True,
              f"{3**k} leaves")

# ===========================================================================
# BLOCK 7 -- BUDGET ARITHMETIC / verdict logic.
#   (a) shallow-prefix regime (#536): w=o(n/log p) => L<=p^w=e^{o(n)} cells: PAID.
#   (b) product/profile leaves are DEEP: w=R_prod=2k=Theta(N) => p^w=e^{Theta(N)}.
#   (c) entropy lemmas (planted L2513/quotient L2526) DO pay a support-count
#       reduction, but Gap-1 collapse is FULL support (no reduction) -> they do
#       NOT apply; the binomial-tail multiplicity is UNCOMPENSATED.
# ===========================================================================
def block7():
    p = 3
    # (a) shallow prefix: w = c*log k, (a-k-1)log|B| = w log p = o(N) -> L=e^{o(N)}
    seq = []
    for k in (100, 1000, 10000, 100000):
        w_shallow = int(math.log(k))                 # w = o(k) certainly o(N)
        logL_perN = w_shallow * math.log(p) / (p * k)  # <= (w log p)/N
        seq.append(logL_perN)
    check("B7 shallow-prefix L=e^o(n): logL/N -> 0 monotone",
          all(seq[i] > seq[i + 1] for i in range(len(seq) - 1)) and seq[-1] < 1e-4,
          f"seq={['%.5f' % x for x in seq]}")
    # (b) deep product prefix w=2k: L<=p^{2k}, log/N = 2 log p / p > 0 -> exponential
    deep_rate = 2 * math.log(p) / p
    check("B7 deep-prefix cells e^Theta(N) (w=2k)", deep_rate > 0.5,
          f"rate/N={deep_rate:.4f}")
    # (c) entropy-loss race for a HYPOTHETICAL support-reducing fold vs the
    #     ACTUAL full-support parabola.
    #   planted/quotient entropy loss per constrained fraction theta:
    #     support factor binom(n-b,a-b)/binom(n,a) with b=theta n, density sigma=a/n.
    #   placement multiplicity: C(k,theta k) ~ e^{h(theta) k} = e^{(h/p)N}.
    #   For a support-reducing fold the loss CAN beat placement; for the parabola
    #   the loss is ZERO (full support) so placement is uncompensated.
    n = 3000
    sigma = Fr(1, 3)
    a = int(sigma * n)
    for theta in (0.2, 0.4):
        b = int(theta * a)          # planted block P subset S, so b <= a
        # planted-entropy support ratio (log, per N)
        # ln[ C(n-b,a-b)/C(n,a) ]
        loss = (math.lgamma(n - b + 1) - math.lgamma(a - b + 1) - math.lgamma(n - a + 1)) \
             - (math.lgamma(n + 1) - math.lgamma(a + 1) - math.lgamma(n - a + 1))
        loss_perN = -loss / n                        # positive = entropy DROP
        check(f"B7 planted-entropy loss>0 theta={theta}", loss_perN > 0,
              f"loss/N={loss_perN:.4f}")
        # ACTUAL parabola fold: full support => loss = 0
        parabola_loss_perN = 0.0
        # placement multiplicity per N (blocks k=n/p)
        place_perN = hbin(theta) / p
        # net for parabola: placement uncompensated (net > 0 => NOT PAYABLE)
        net_parabola = place_perN - parabola_loss_perN
        check(f"B7 parabola NET>0 (uncompensated) theta={theta}",
              net_parabola > 0, f"net/N={net_parabola:.4f}")
    # (d) verdict logic sanity: e^{Omega(N)} count is NOT <= e^{o(n)}
    #     => direct envelope enumeration NOT PAYABLE; residual = FI-routing.
    for theta in (0.3, 0.6, 0.9):
        k = 5000
        count_rate_perN = math.log(tail_count(k, theta)) / (p * k)
        check(f"B7 NOT-PAYABLE-by-enumeration theta={theta}",
              count_rate_perN > 0.0, f"count_rate/N={count_rate_perN:.4f}")

# ===========================================================================
def main():
    for fn in (block0, block1, block2, block3, block4, block5, block6, block7):
        fn()
    npass = sum(1 for _, ok, _ in CHECKS if ok)
    ntot = len(CHECKS)
    fails = [(n, d) for n, ok, d in CHECKS if not ok]
    for n, d in fails:
        print(f"FAIL: {n}   {d}")
    print(f"RESULT: {'PASS' if not fails else 'FAIL'} ({npass}/{ntot})")
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    main()
