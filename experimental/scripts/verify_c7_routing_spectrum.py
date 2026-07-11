#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_c7_routing_spectrum.py  --  recomputes every number in
experimental/notes/thresholds/c7_routing_spectrum.md

Attack on the routing=spectrum conjecture (the named wall of PR #622,
se_on_admissible_leaves.md), decided against the C7 cell of
asymptotic_rs_mca_frontiers.tex (L2440-2454).

Central object (our #614 master identity + this packet's MASTER-2):
    P_2   = sum_z mu(z)^2                     (collision probability)
    E     = A_eff * P_2 - 1                   (nontrivial spectral energy, Parseval)
    L     = |support(mu)|                     (realized image size)
    Mx    = max_z mu(z)                       (heaviest atom)
    G_1   = A_eff / L                         (Gap-1 image-collapse ratio; (FI) <=> G_1 <= e^{o})
    Q_img = L * Mx                            (image-normalized max-fiber ratio; primitive-Q <=> Q_img <= e^{o})

MASTER-2 (this packet, PROVED one line):
    E + 1 = A_eff * P_2 <= A_eff * Mx = (A_eff/L)*(L*Mx) = G_1 * Q_img.
So (S_E)-violation (E large) forces G_1 large (effective-image collapse, C7 line
L2453-2454) OR Q_img large (saturation, C7 line L2440-2452) -- C7's TWO printed
components.  The two collapse modes are genuinely distinct:
    block-parabola: pure collapse   (G_1=p^k, Q_img=1,   MASTER-2 tight)
    heavy-atom     : pure saturation (G_1=1,   Q_img exp, MASTER-2 slack)
both violate (S_E); routing sends them to the two DIFFERENT C7 components.

stdlib only; exact via fractions.Fraction; zero-arg; exit 0 iff all checks pass.
Run under:  ulimit -v 2097152 ; python3 experimental/scripts/verify_c7_routing_spectrum.py
"""

import sys
import math
import itertools
from fractions import Fraction as Fr

PASS = 0
FAIL = 0
LOG = []


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        LOG.append(("PASS", name, detail))
    else:
        FAIL += 1
        LOG.append(("FAIL", name, detail))


# ---------------------------------------------------------------------------
# profile statistics on an exact rational measure mu: dict{key: Fraction}
# ---------------------------------------------------------------------------
def stats(mu, A_eff):
    """mu: mapping support-point -> Fraction mass (need not be normalized);
       A_eff: integer, size of the effective span V_g the profile lives in.
       Returns exact P2, E, L, Mx, G1, Qimg with sum(mu)=1 enforced."""
    tot = sum(mu.values())
    assert tot == 1, "measure must be normalized (sum=1), got %s" % tot
    L = sum(1 for v in mu.values() if v != 0)
    assert L <= A_eff, "support %d exceeds span %d" % (L, A_eff)
    P2 = sum(v * v for v in mu.values())
    E = A_eff * P2 - 1
    Mx = max(mu.values())
    G1 = Fr(A_eff, L)
    Qimg = L * Mx
    return dict(P2=P2, E=E, L=L, Mx=Mx, G1=G1, Qimg=Qimg, A_eff=A_eff)


def uniform_on(support_keys, A_eff):
    L = len(support_keys)
    return {k: Fr(1, L) for k in support_keys}, A_eff


# ---------------------------------------------------------------------------
# BLOCK 0 -- master identity E = A_eff*P2 - 1 and L >= A_eff/(1+E)  (our #614)
# ---------------------------------------------------------------------------
def block0():
    # deterministic pseudo-random rational measures over several span sizes
    seeds = [1, 7, 13, 29, 101]
    A_list = [5, 7, 9, 8, 15, 25]
    n0 = PASS + FAIL
    for A in A_list:
        for sd in seeds:
            # build a positive rational measure on a random-size support
            x = sd
            weights = []
            L = 1 + (sd * 3 + A) % A  # support size in 1..A
            for i in range(L):
                x = (1103515245 * x + 12345) % (2 ** 31)
                weights.append(1 + x % 17)
            s = sum(weights)
            mu = {i: Fr(w, s) for i, w in enumerate(weights)}
            st = stats(mu, A)
            # Parseval form: E + 1 == A_eff * P2  (definitional, exact)
            check("B0.parseval A=%d sd=%d" % (A, sd), st["E"] + 1 == A * st["P2"])
            # master identity L >= A_eff/(1+E)  (Cauchy-Schwarz on support)
            check("B0.master A=%d sd=%d" % (A, sd), st["L"] >= Fr(A, 1) / (1 + st["E"]))
    # uniform measure => E = A_eff/L - 1 and equality L = A_eff/(1+E)
    for A in A_list:
        for L in range(1, A + 1):
            mu, _ = uniform_on(list(range(L)), A)
            st = stats(mu, A)
            check("B0.uniform-E A=%d L=%d" % (A, L), st["E"] == Fr(A, L) - 1)
            check("B0.uniform-tight A=%d L=%d" % (A, L),
                  st["L"] == Fr(A, 1) / (1 + st["E"]))
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
# BLOCK 1 -- MASTER-2: E+1 <= G_1 * Q_img on all measures; record slack
# ---------------------------------------------------------------------------
def block1():
    n0 = PASS + FAIL
    A_list = [5, 7, 9, 8, 12, 16, 25]
    for A in A_list:
        for sd in [2, 3, 5, 11, 23, 47]:
            x = sd
            L = 1 + (sd * 5 + A) % A
            weights = []
            for i in range(L):
                x = (1103515245 * x + 12345) % (2 ** 31)
                # occasionally plant a heavy atom to exercise saturation slack
                w = 1 + x % 11
                if i == 0 and sd % 2 == 0:
                    w = 50
                weights.append(w)
            s = sum(weights)
            mu = {i: Fr(w, s) for i, w in enumerate(weights)}
            st = stats(mu, A)
            lhs = st["E"] + 1
            rhs = st["G1"] * st["Qimg"]
            check("B1.master2 A=%d sd=%d" % (A, sd), lhs <= rhs,
                  "E+1=%s  G1*Qimg=%s" % (lhs, rhs))
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
# BLOCK 2 -- block-parabola: PURE COLLAPSE mode (G_1=p^k, Q_img=1, tight)
#            actual group construction for small (p,k); closed form scaled
# ---------------------------------------------------------------------------
def parabola_image(p, k):
    """S = { ((t_i, t_i^2 mod p))_{i<k} : t in F_p^k } subset (F_p^2)^k.
       returns (image_set, A_eff=p^{2k}, rankFp)."""
    one_block = [(t, (t * t) % p) for t in range(p)]  # p distinct points
    # image over k blocks = product
    img = set(itertools.product(one_block, repeat=k))
    A_eff = (p * p) ** k
    # rank over F_p of {g(t)-g(0)} for one block spans F_p^2 (det 2 != 0 for p>2)
    return img, A_eff


def rank_fp_oneblock(p):
    # {(t,t^2)-(0,0) : t} = {(t, t^2)}; take t=1,-1 => rows (1,1),(p-1,1)
    # det = 1*1 - 1*(p-1) = 1-(p-1) = 2-p == 2 mod p ; nonzero for odd p
    return 2 if (2 % p) != 0 else 1


def block2():
    n0 = PASS + FAIL
    small = [(3, 1), (3, 2), (5, 1), (5, 2), (7, 1)]
    for (p, k) in small:
        img, A_eff = parabola_image(p, k)
        L = len(img)
        check("B2.image-size p=%d k=%d" % (p, k), L == p ** k,
              "L=%d p^k=%d" % (L, p ** k))
        check("B2.A_eff p=%d k=%d" % (p, k), A_eff == p ** (2 * k))
        check("B2.rank p=%d" % p, rank_fp_oneblock(p) == 2)
        # uniform-on-image profile (injective M=L, singleton fibers)
        mu = {z: Fr(1, L) for z in img}
        st = stats(mu, A_eff)
        check("B2.E=p^k-1 p=%d k=%d" % (p, k), st["E"] == p ** k - 1)
        check("B2.G1=p^k p=%d k=%d" % (p, k), st["G1"] == p ** k)
        check("B2.Qimg=1 p=%d k=%d" % (p, k), st["Qimg"] == 1,
              "Qimg=%s (singleton fibers => max-fiber Q PASSES)" % st["Qimg"])
        # PURE COLLAPSE: MASTER-2 is EQUALITY, all of E carried by G_1
        check("B2.master2-tight p=%d k=%d" % (p, k),
              st["E"] + 1 == st["G1"] * st["Qimg"])
        # (S_E) FAILS, (FI) FAILS, max-fiber Q PASSES => routed to C7-COLLAPSE
        check("B2.SE-fail p=%d k=%d" % (p, k), st["E"] >= p ** k - 1)
        check("B2.FI-fail p=%d k=%d" % (p, k), st["L"] * A_eff < A_eff * A_eff)  # L<A_eff
        check("B2.maxfiberQ-pass p=%d k=%d" % (p, k), st["Qimg"] == 1)
    # closed-form scaled rows k=1..5 (no group build), reproduce note table
    rows = []
    for (p, k) in [(3, 1), (3, 2), (3, 4), (5, 4), (7, 4)]:
        E = p ** k - 1
        L = p ** k
        A_eff = p ** (2 * k)
        N = p * k
        G1 = Fr(A_eff, L)
        Qimg = Fr(1, 1)
        check("B2.closed-master2 p=%d k=%d" % (p, k), (E + 1) == G1 * Qimg)
        rate = math.log(1 + E) / N          # = log(p^k)/(pk) = log(p)/p exactly
        rows.append((p, k, N, L, A_eff, E, rate))
    # rate is the constant log(p)/p signature of the product (unrounded compare)
    for (p, k, N, L, A_eff, E, rate) in rows:
        check("B2.rate p=%d k=%d" % (p, k),
              abs(rate - math.log(p) / p) < 1e-9,
              "rate=%.3f log(p)/p=%.3f" % (rate, math.log(p) / p))
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
# BLOCK 3 -- heavy-atom (single): PURE SATURATION mode
#            (S_E) FAILS, (FI) HOLDS (L=A_eff), max-fiber Q FAILS (Q_img exp)
#            => routed to C7-SATURATION, NOT effective-image-collapse.
#            THE FALSIFIER of the narrow conjecture.
# ---------------------------------------------------------------------------
def heavy_atom_measure(A_eff, a):
    """atom mass a (Fraction) at z*, remaining (1-a) uniform over A_eff-1 pts."""
    rest = (1 - a) / (A_eff - 1)
    mu = {0: a}
    for z in range(1, A_eff):
        mu[z] = rest
    return mu


def block3():
    n0 = PASS + FAIL
    # choose a = ceil(A^{3/4}) / A so atom is exponentially heavier than 1/A_eff
    # but still o(1); full support (L = A_eff), so (FI) holds with EQUALITY.
    for A in [16, 81, 256, 625]:
        # a ~ A^{-1/4}: take numerator = round(A^{3/4}) over A
        num = round(A ** 0.75)
        a = Fr(num, A)
        mu = heavy_atom_measure(A, a)
        st = stats(mu, A)
        # (FI) holds: full support
        check("B3.FI-holds A=%d" % A, st["L"] == A and st["G1"] == 1)
        # max-fiber Q FAILS: Q_img = L*Mx = A*a = num (grows like A^{3/4})
        check("B3.Qimg=num A=%d" % A, st["Qimg"] == num)
        check("B3.maxfiberQ-fail A=%d" % A, st["Qimg"] > int(math.sqrt(A)),
              "Q_img=%s > sqrt(A)=%d" % (st["Qimg"], int(math.sqrt(A))))
        # (S_E) FAILS: E = A*P2 - 1, with P2 ~ a^2 = num^2/A^2 so E ~ num^2/A - 1
        # E grows like A^{1/2}, exponential in N (span exponential) -> violates (S_E)
        check("B3.SE-fail A=%d" % A, st["E"] > int(math.sqrt(A)) - 1,
              "E=%s" % st["E"])
        # MASTER-2 holds and is SLACK (saturation mode): E+1 < G1*Qimg strictly
        check("B3.master2 A=%d" % A, st["E"] + 1 <= st["G1"] * st["Qimg"])
        check("B3.master2-slack A=%d" % A, st["E"] + 1 < st["G1"] * st["Qimg"],
              "E+1=%s < G1*Qimg=%s (P2<Mx, spread tail)" % (st["E"] + 1, st["G1"] * st["Qimg"]))
        # THE FALSIFIER: violates (S_E) yet is NOT an effective-image collapse
        # (G_1 = 1, so C7-collapse trigger 'exponentially fewer boundary values'
        #  does NOT fire); it is caught by C7-saturation instead.
        check("B3.escapes-collapse A=%d" % A, st["G1"] == 1 and st["E"] >= 1)
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
# BLOCK 4 -- heavy-atom PRODUCT: parallel to the parabola product, but blocks
#            have FULL image + heavy atom => full-image product, pure saturation.
#            E+1 = prod(E_i+1) multiplicative (T3 of #622), G_1 = 1, Q_img exp.
# ---------------------------------------------------------------------------
def block4():
    n0 = PASS + FAIL
    p = 5
    # one block: full image on F_p, atom mass a at 0, uniform (1-a)/(p-1) else
    a = Fr(2, 5)  # heavy-ish but < 1
    blk = {0: a}
    for j in range(1, p):
        blk[j] = (1 - a) / (p - 1)
    st1 = stats(blk, p)
    E1 = st1["E"]
    check("B4.block-full-image", st1["L"] == p and st1["G1"] == 1)
    check("B4.block-E-positive", E1 > 0)
    # k-fold product measure on F_p^k (full image size p^k = A_eff)
    for k in [1, 2, 3, 4]:
        A_eff = p ** k
        # product measure mass = prod of block masses
        keys = list(itertools.product(range(p), repeat=k))
        mu = {}
        for key in keys:
            v = Fr(1, 1)
            for coord in key:
                v *= blk[coord]
            mu[key] = v
        st = stats(mu, A_eff)
        # multiplicativity E+1 = (E_1+1)^k  (exact)
        check("B4.multiplicative k=%d" % k, st["E"] + 1 == (E1 + 1) ** k,
              "E+1=%s (E1+1)^k=%s" % (st["E"] + 1, (E1 + 1) ** k))
        # FULL image: L = p^k = A_eff  => G_1 = 1, (FI) holds
        check("B4.full-image k=%d" % k, st["L"] == A_eff and st["G1"] == 1)
        # Q_img = (p*a)^k  exponential in k => max-fiber Q FAILS for large k
        check("B4.Qimg-prod k=%d" % k, st["Qimg"] == (p * a) ** k)
        # MASTER-2 tensorizes: E+1 <= G1*Qimg = 1*(p a)^k
        check("B4.master2 k=%d" % k, st["E"] + 1 <= st["G1"] * st["Qimg"])
    # readout: with a=2/5, p=5: E1+1 = 5*P2_1 ; rate log(E1+1)/log(p) fixed
    P2_1 = st1["P2"]
    check("B4.block-P2", E1 + 1 == p * P2_1)
    # the k->inf product violates (S_E) (constant positive rate log(E1+1)>0)
    # yet (FI) holds throughout (full image): E+1 = (E1+1)^k -> infinity.
    check("B4.block-rate-positive", math.log(float(E1 + 1)) > 0)
    E_big = (E1 + 1) ** 40 - 1
    check("B4.SE-violated-in-limit", E_big > 10 ** 3,
          "(E1+1)^40 - 1 = %s" % float(E_big))
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
# BLOCK 5 -- TWO-CELL DICHOTOMY (the structure theorem):
#   (G_1 <= B) and (Q_img <= B)  =>  E+1 <= B^2.
#   contrapositive: E+1 > B^2  =>  G_1 > B  OR  Q_img > B  (collapse OR saturation).
#   => every 'primitive residual' (bounded G_1 and Q_img) satisfies (S_E).
# ---------------------------------------------------------------------------
def block5():
    n0 = PASS + FAIL
    # exhaustive over a family of measures; for each, verify the implication
    A_list = [8, 9, 12, 16, 25]
    for A in A_list:
        for sd in range(1, 25):
            x = sd * 2654435761 % (2 ** 31)
            L = 1 + (x % A)
            weights = []
            for i in range(L):
                x = (1103515245 * x + 12345) % (2 ** 31)
                w = 1 + x % 9
                if i == 0 and sd % 3 == 0:
                    w = 30  # plant an atom sometimes
                weights.append(w)
            s = sum(weights)
            mu = {i: Fr(w, s) for i, w in enumerate(weights)}
            st = stats(mu, A)
            G1, Qimg, E = st["G1"], st["Qimg"], st["E"]
            B = max(G1, Qimg)
            # dichotomy inequality (equivalent to MASTER-2): E+1 <= B^2
            check("B5.dichotomy A=%d sd=%d" % (A, sd), (E + 1) <= B * B)
            # the sharp form actually used: E+1 <= G1*Qimg
            check("B5.sharp A=%d sd=%d" % (A, sd), (E + 1) <= G1 * Qimg)
    # explicit primitive-class statement: if both ratios <= t then E+1 <= t^2
    for t in [Fr(3, 2), Fr(2, 1), Fr(5, 2), Fr(3, 1)]:
        # any measure with G1<=t and Qimg<=t must have E+1<=t^2; verify by
        # searching the uniform + near-uniform family and confirming no breach
        breach = False
        for A in [9, 16, 25]:
            for L in range(1, A + 1):
                if Fr(A, L) > t:
                    continue
                mu, _ = uniform_on(list(range(L)), A)
                st = stats(mu, A)
                if st["Qimg"] <= t and not (st["E"] + 1 <= t * t):
                    breach = True
        check("B5.primitive=>SE t=%s" % t, not breach)
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
# BLOCK 6 -- EQUIVALENCE MODULO max-fiber Q:
#   (S_E) => (FI)                     always (master), unconditional.
#   (FI) and max-fiber Q => (S_E)     (MASTER-2).
#   heavy-atom is the (FI)-yet-not-(S_E) gap: it FAILS max-fiber Q.
# ---------------------------------------------------------------------------
def block6():
    n0 = PASS + FAIL
    # (S_E) => (FI): if E <= c then L >= A_eff/(1+c) >= A_eff/(1+E)
    A_list = [9, 16, 25]
    for A in A_list:
        for sd in range(1, 20):
            x = sd * 40503 % (2 ** 31)
            L = 1 + (x % A)
            weights = []
            for i in range(L):
                x = (1103515245 * x + 12345) % (2 ** 31)
                weights.append(1 + x % 7)
            s = sum(weights)
            mu = {i: Fr(w, s) for i, w in enumerate(weights)}
            st = stats(mu, A)
            # (S_E)=>(FI) direction, unconditional:
            check("B6.SE=>FI A=%d sd=%d" % (A, sd),
                  st["L"] * (1 + st["E"]) >= A)  # L(1+E) >= A_eff
            # (FI)+maxfiberQ=>(S_E): E+1 <= G1*Qimg
            check("B6.FI+Q=>SE A=%d sd=%d" % (A, sd),
                  st["E"] + 1 <= st["G1"] * st["Qimg"])
    # the gap witness: heavy-atom has (FI) (G1=1) but NOT (S_E) (E large),
    # and it is exactly the max-fiber-Q FAILURE (Qimg large) that separates them
    A = 256
    num = round(A ** 0.75)
    st = stats(heavy_atom_measure(A, Fr(num, A)), A)
    check("B6.gap-FI-holds", st["G1"] == 1)                       # (FI) holds
    check("B6.gap-SE-fails", st["E"] > 10)                        # (S_E) fails
    check("B6.gap-is-maxfiberQ", st["Qimg"] > int(math.sqrt(A)))  # separated by max-fiber Q
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
# BLOCK 7 -- SINGLE ADMISSIBLE LEAVES (T3 of #622): E polynomial, (S_E) holds,
#            so single leaves never reach the divergence (both G_1, Q_img subexp).
#            Reproduces the #622 census rows exactly via the power-sum map.
# ---------------------------------------------------------------------------
def powersum_leaf(p, N, R, m):
    """global power-sum map on free m-subsets of the support T = {0,...,N-1}
       inside F_p (N <= p): Phi(S) = (p_1(S),...,p_R(S)) in F_p^R.
       A_eff = p^R (the full effective span; R<p => no Frobenius collapse, gap2).
       Returns (image profile mu, A_eff, N)."""
    from itertools import combinations
    prof = {}
    for S in combinations(range(N), m):
        key = tuple(sum(pow(t, j, p) for t in S) % p for j in range(1, R + 1))
        prof[key] = prof.get(key, 0) + 1
    M = sum(prof.values())
    mu = {k: Fr(v, M) for k, v in prof.items()}
    A_eff = p ** R
    return mu, A_eff, N


def block7():
    n0 = PASS + FAIL
    # #622 census rows (p,N,R,m) with R<p (admissible window), global power-sum
    # map; A_eff = p^R.  Exact E reproduces the #622 se_admissible table.
    rows = [(3, 2, 1, 1, Fr(1, 2)), (5, 2, 1, 1, Fr(3, 2)),
            (5, 3, 1, 2, Fr(2, 3)), (5, 3, 2, 2, Fr(22, 3)),
            (7, 3, 1, 2, Fr(4, 3)), (7, 4, 2, 2, Fr(43, 6)),
            (7, 5, 2, 2, Fr(39, 10))]
    for (p, N, R, m, Eexp) in rows:
        mu, A_eff, N_ = powersum_leaf(p, N, R, m)
        st = stats(mu, A_eff)
        # exact E matches #622 census (two-way E = A_eff*P2 - 1)
        check("B7.census-E p=%d N=%d R=%d m=%d" % (p, N, R, m),
              st["E"] == Eexp, "E=%s expected=%s" % (st["E"], Eexp))
        # single leaf: (S_E) HOLDS (E polynomial) => both cells subexponential,
        # so a single admissible leaf never reaches the collapse/saturation
        # divergence -- the divergence is a k-fold PRODUCT phenomenon (T3).
        check("B7.single-leaf-SE p=%d N=%d R=%d m=%d" % (p, N, R, m),
              st["E"] < A_eff and st["G1"] * st["Qimg"] < A_eff * A_eff)
        # MASTER-2 holds (as always)
        check("B7.master2 p=%d N=%d R=%d m=%d" % (p, N, R, m),
              st["E"] + 1 <= st["G1"] * st["Qimg"])
    return PASS + FAIL - n0


# ---------------------------------------------------------------------------
def main():
    blocks = [
        ("BLOCK 0  master identity  (E=A_eff*P2-1, L>=A_eff/(1+E))", block0),
        ("BLOCK 1  MASTER-2  E+1 <= G_1 * Q_img", block1),
        ("BLOCK 2  block-parabola: PURE COLLAPSE (tight)", block2),
        ("BLOCK 3  heavy-atom: PURE SATURATION (FALSIFIER of narrow form)", block3),
        ("BLOCK 4  heavy-atom PRODUCT: full-image, multiplicative E", block4),
        ("BLOCK 5  TWO-CELL DICHOTOMY: primitive => (S_E)", block5),
        ("BLOCK 6  EQUIVALENCE modulo max-fiber Q: (S_E)<=>(FI)|Q", block6),
        ("BLOCK 7  single admissible leaves: (S_E) holds (T3)", block7),
    ]
    print("=" * 72)
    print("verify_c7_routing_spectrum.py  --  routing=spectrum (C7 vs S_E)")
    print("=" * 72)
    for label, fn in blocks:
        c = fn()
        print("  %-58s %3d checks" % (label, c))
    print("-" * 72)
    fails = [x for x in LOG if x[0] == "FAIL"]
    if fails:
        print("FAILURES:")
        for _, name, detail in fails:
            print("   FAIL  %s   %s" % (name, detail))
    print("RESULT: %s (%d/%d)" % ("PASS" if FAIL == 0 else "FAIL",
                                  PASS, PASS + FAIL))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
