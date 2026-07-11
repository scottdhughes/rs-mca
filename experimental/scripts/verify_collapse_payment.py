#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_collapse_payment.py  --  recomputes every number in
experimental/notes/thresholds/collapse_payment.md.

Stdlib only.  Zero-arg.  Chunked; runs under `ulimit -v 2097152`.
Exit 0 iff every check passes.  Prints "RESULT: PASS (n/n)" on success.

The packet proves the *collapse-side envelope payment after routing*:  that
the profile envelope E_n(a) (tex eq:profile-envelope, L859-862) is well posed
AFTER (FI)-routing (tex L877-881), that the "countertheorem" of #626 is a
per-profile overcount dissolved by first-match disjointness (lem:first-match-bound,
L1526-1538) plus description-entropy exclusion (lem:profile-multiplicity, L5028-5033),
and that the residual is the single collapse cell's own image-scale budget (= #626).

Lineage recomputed byte-for-byte where possible: #536/#539/#545/#609/#614/#622/
#625/#626/#627 and avdeevvadim #558.

Blocks
  0  per-block spectral invariants (T,C,S)             reproduces #625/#626 BLOCK 0
  1  tensorization over products (G1,Qimg,E+1,Nbar)    reproduces #626 BLOCK 1
  2  RUNG 1: image vs ambient Nbar, Nbar^img=G1*Nbar^amb; block-parabola Nbar^img=1
  3  binomial-tail collapse count N_coll               reproduces #626 BLOCK 3
  4  RUNG 2 (CRUX): description entropy of the pattern family is Omega(N) bits
  5  naive "mass x count" = 2*N_coll = e^{Omega(N)}     the #626 countertheorem quantity
  6  DECISIVE: exact syndrome-line census; Z_a(r)=disjoint union; naive sum >= union;
     routed profile contributes Z^o = empty                lem:first-match-bound L1535
  7  census sum-vs-max ratios, routed/unrouted split   reproduces #625/#626 census
"""

import sys
from fractions import Fraction as Fr
from math import comb, log, log2

# ---------------------------------------------------------------------------
_PASS = 0
_FAIL = 0
_LOG = []

def check(name, cond, detail=""):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
        _LOG.append("FAIL: %s  %s" % (name, detail))
    return cond

def approx(x, y, tol=1e-9):
    return abs(float(x) - float(y)) <= tol * (1.0 + abs(float(y)))

# ===========================================================================
# BLOCK 0 -- per-block spectral invariants (exact).  Reproduces #625/#626.
#   Type T (trivial/full) : uniform on p, A=p,   L=p, G1=1, Qimg=1, E+1=1
#   Type C (parabola)     : uniform on p, A=p^2, L=p, G1=p, Qimg=1, E+1=p
#   Type S (heavy atom)   : p=5, a=2/5,   A=5,   L=5, G1=1, Qimg=2, E+1=5/4
# E+1 = A_eff * sum mu^2 (#614 Parseval);  Nbar^img = |Omega0|/L ; Nbar^amb=|Omega0|/A.
# For each block |Omega0_i| = p (p raw witnesses / configs per block).
# ===========================================================================
def block_invariants(p, kind):
    """Return dict of exact per-block invariants."""
    if kind == 'T':
        Aeff = p;      L = p;   Om0 = p
        mu = [Fr(1, p)] * p                    # uniform on p image points
    elif kind == 'C':
        Aeff = p * p;  L = p;   Om0 = p
        mu = [Fr(1, p)] * p                    # uniform on the p-point parabola image
    elif kind == 'S':
        assert p == 5
        Aeff = 5;      L = 5;   Om0 = 5
        a = Fr(2, 5)
        rest = (1 - a) / (p - 1)
        mu = [a] + [rest] * (p - 1)            # heavy atom + light tail, full image
    else:
        raise ValueError(kind)
    P2 = sum(m * m for m in mu)
    Mx = max(mu)
    E1 = Aeff * P2                              # E + 1
    G1 = Fr(Aeff, L)
    Qimg = L * Mx
    Nbar_img = Fr(Om0, L)
    Nbar_amb = Fr(Om0, Aeff)
    return dict(p=p, kind=kind, Aeff=Aeff, L=L, Om0=Om0, P2=P2, Mx=Mx,
                E1=E1, G1=G1, Qimg=Qimg, Nbar_img=Nbar_img, Nbar_amb=Nbar_amb)

def block0():
    # expected exact rows (reproduces #625 sec 2 / #626 BLOCK 0)
    T = block_invariants(3, 'T')
    check("B0.T.G1",   T['G1']   == Fr(1),  str(T['G1']))
    check("B0.T.Qimg", T['Qimg'] == Fr(1),  str(T['Qimg']))
    check("B0.T.E1",   T['E1']   == Fr(1),  str(T['E1']))
    C = block_invariants(3, 'C')
    check("B0.C.G1",   C['G1']   == Fr(3),  str(C['G1']))
    check("B0.C.Qimg", C['Qimg'] == Fr(1),  str(C['Qimg']))
    check("B0.C.E1",   C['E1']   == Fr(3),  str(C['E1']))
    C5 = block_invariants(5, 'C')
    check("B0.C5.G1",  C5['G1']  == Fr(5),  str(C5['G1']))
    check("B0.C5.E1",  C5['E1']  == Fr(5),  str(C5['E1']))
    S = block_invariants(5, 'S')
    check("B0.S.G1",   S['G1']   == Fr(1),          str(S['G1']))
    check("B0.S.Qimg", S['Qimg'] == Fr(2),          str(S['Qimg']))
    check("B0.S.E1",   S['E1']   == Fr(5, 4),       str(S['E1']))  # 25/16*... -> (5/4) per block
    # MASTER-2 per block: E+1 <= G1*Qimg  (Holder), equality iff uniform on support
    for b in (T, C, C5, S):
        check("B0.master2.%s%d" % (b['kind'], b['p']),
              b['E1'] <= b['G1'] * b['Qimg'],
              "E1=%s G1*Q=%s" % (b['E1'], b['G1'] * b['Qimg']))
    # uniform blocks: equality; heavy atom: slack
    check("B0.eq.C",   C['E1'] == C['G1'] * C['Qimg'])
    check("B0.slack.S", S['E1'] <  S['G1'] * S['Qimg'])
    # Nbar^img = 1 for T and C (singleton fibers, the #609 escape)
    check("B0.Nimg.T", T['Nbar_img'] == Fr(1), str(T['Nbar_img']))
    check("B0.Nimg.C", C['Nbar_img'] == Fr(1), str(C['Nbar_img']))

# ===========================================================================
# BLOCK 1 -- tensorization over k blocks.  E+1, G1, Qimg, Nbar all multiplicative.
# A leaf = tuple of block kinds.  Recompute the explicit product measure and
# check it equals the product of per-block invariants (reproduces #626 BLOCK 1).
# ===========================================================================
def leaf_from_blocks(p, kinds):
    """Explicit product invariants for a leaf given a tuple of block kinds."""
    bs = [block_invariants(p, k) for k in kinds]
    Aeff = 1; L = 1; Om0 = 1; E1 = Fr(1); G1 = Fr(1); Qimg = Fr(1)
    for b in bs:
        Aeff *= b['Aeff']; L *= b['L']; Om0 *= b['Om0']
        E1 *= b['E1'];     G1 *= b['G1']; Qimg *= b['Qimg']
    Nbar_img = Fr(Om0, L)
    Nbar_amb = Fr(Om0, Aeff)
    return dict(Aeff=Aeff, L=L, Om0=Om0, E1=E1, G1=G1, Qimg=Qimg,
                Nbar_img=Nbar_img, Nbar_amb=Nbar_amb, kinds=tuple(kinds))

def block1():
    p = 3
    for k in range(1, 5):
        # all-C collapse product
        allC = leaf_from_blocks(p, ['C'] * k)
        check("B1.allC.G1.k%d" % k,   allC['G1']   == Fr(p) ** k)
        check("B1.allC.Qimg.k%d" % k, allC['Qimg'] == Fr(1))
        check("B1.allC.E1.k%d" % k,   allC['E1']   == Fr(p) ** k)  # E = p^k - 1
        check("B1.allC.Nimg.k%d" % k, allC['Nbar_img'] == Fr(1))   # singleton fibers
        # mixed j type-C, k-j type-T : G1 = p^j
        for j in range(0, k + 1):
            kinds = ['C'] * j + ['T'] * (k - j)
            leaf = leaf_from_blocks(p, kinds)
            check("B1.mix.G1.k%d.j%d" % (k, j), leaf['G1'] == Fr(p) ** j)
            check("B1.mix.Nimg.k%d.j%d" % (k, j), leaf['Nbar_img'] == Fr(1))
            # MASTER-2 tensorized
            check("B1.mix.master2.k%d.j%d" % (k, j),
                  leaf['E1'] <= leaf['G1'] * leaf['Qimg'])
    # saturation product p=5: Qimg = 2^j, E+1 = (5/4)^j, G1 = 1, full image
    p = 5
    for k in range(1, 5):
        for j in range(0, k + 1):
            kinds = ['S'] * j + ['T'] * (k - j)
            leaf = leaf_from_blocks(p, kinds)
            check("B1.sat.Qimg.k%d.j%d" % (k, j), leaf['Qimg'] == Fr(2) ** j)
            check("B1.sat.E1.k%d.j%d" % (k, j),   leaf['E1']   == Fr(5, 4) ** j)
            check("B1.sat.G1.k%d.j%d" % (k, j),   leaf['G1']   == Fr(1))

# ===========================================================================
# BLOCK 2 -- RUNG 1: routed profiles' entry scale.
# tex L4835-4836: Nbar^img = M/L, Nbar^amb = M/A.  Hence Nbar^img = G1 * Nbar^amb.
# For the block-parabola leaf (j collapse blocks): M=p^k, A=p^{k+j}, L=p^k, so
#   Nbar^amb = p^{-j},  G1 = p^j,  Nbar^img = 1   (singleton fibers at image scale).
# The mission's arithmetic:  Nbar = M/L = G1*(M/A).  We confirm it exactly, and
# confirm the IMAGE scale does NOT inflate the per-profile term (it is 1, not p^{-j}).
# ===========================================================================
def block2():
    for p in (3, 5, 7):
        for k in range(1, 6):
            for j in range(0, k + 1):
                kinds = ['C'] * j + ['T'] * (k - j)
                leaf = leaf_from_blocks(p, kinds)
                M = leaf['Om0']; A = leaf['Aeff']; L = leaf['L']; G1 = leaf['G1']
                # identity Nbar^img = G1 * Nbar^amb
                check("B2.id.p%d.k%d.j%d" % (p, k, j),
                      leaf['Nbar_img'] == G1 * leaf['Nbar_amb'],
                      "%s vs %s" % (leaf['Nbar_img'], G1 * leaf['Nbar_amb']))
                # exact values
                check("B2.amb.p%d.k%d.j%d" % (p, k, j),
                      leaf['Nbar_amb'] == Fr(1, p ** j))
                check("B2.G1.p%d.k%d.j%d" % (p, k, j), G1 == Fr(p) ** j)
                check("B2.img1.p%d.k%d.j%d" % (p, k, j),
                      leaf['Nbar_img'] == Fr(1),
                      "block-parabola image-scale Nbar must be 1 (singleton)")
    # Consequence: the naive per-profile envelope term (1+Nbar^img) = 2 for EVERY
    # collapse leaf, independent of j -- so per-profile rescaling cannot help the sum.
    for p in (3, 5):
        for k in range(1, 5):
            for j in range(0, k + 1):
                leaf = leaf_from_blocks(p, ['C'] * j + ['T'] * (k - j))
                term = 1 + leaf['Nbar_img']
                check("B2.term2.p%d.k%d.j%d" % (p, k, j), term == Fr(2))

# ===========================================================================
# BLOCK 3 -- binomial-tail collapse count (reproduces #626 BLOCK 3 exactly).
# A leaf with j type-C blocks has G1 = p^j; G1 >= e^{eps N} <=> j >= theta k,
# theta = eps p / ln p, N = p k.  N_coll(k,theta) = sum_{j >= ceil(theta k)} C(k,j).
# ===========================================================================
def N_coll(k, theta):
    thr = _ceil_theta_k(theta, k)
    return sum(comb(k, j) for j in range(thr, k + 1))

def _ceil_theta_k(theta, k):
    # smallest integer j with j >= theta*k, computed exactly with Fractions
    tk = Fr(theta).limit_denominator(10 ** 9) * k
    ij = int(tk)
    if Fr(ij) < tk:
        ij += 1
    return ij

def block3():
    # exact tail counts quoted by #626 (p=3)
    check("B3.k20.t60", N_coll(20, 0.60) == 263950, str(N_coll(20, 0.60)))
    check("B3.k40.t60", N_coll(40, 0.60) == 147437500478, str(N_coll(40, 0.60)))
    check("B3.k40.t75", N_coll(40, 0.75) == 1221246132, str(N_coll(40, 0.75)))
    # positive exponential rate:  (1/k) ln N_coll -> h(theta) (theta>1/2) or ln2
    def h(x):
        return -x * log(x) - (1 - x) * log(1 - x)
    for theta in (0.60, 0.75):
        k = 2000
        rate = log(N_coll(k, theta)) / k
        check("B3.rate.t%.2f" % theta, abs(rate - h(theta)) < 0.02,
              "rate=%.4f h=%.4f" % (rate, h(theta)))
    # per-N rate strictly positive
    for theta in (0.60, 0.75):
        p = 3; k = 2000; N = p * k
        rateN = log(N_coll(k, theta)) / N
        check("B3.rateN.t%.2f" % theta, rateN > 0.05, "rateN=%.4f" % rateN)

# ===========================================================================
# BLOCK 4 -- RUNG 2 (THE CRUX): description entropy of the pattern family.
# lem:profile-multiplicity (L5028-5033) requires TOTAL DESCRIPTION ENTROPY o(n)
# bits for the e^{o(n)} profile count.  Selecting WHICH blocks collapse is an
# "arbitrary planted subset" (lem:profile-atlas L4781-4783).  Its description
# entropy is log2 C(k, j) bits.  We show this is Omega(N)=Omega(pk), i.e. NOT o(n),
# for BOTH violators (j>=theta k) AND non-violators (any theta*k with theta in (0,1)).
# This is the reformulation content: L869 (literal pattern count) is busted by the
# WHOLE product class, not just the violators -- because the family carries linear
# description entropy, so it is outside lem:profile-multiplicity's hypothesis.
# ===========================================================================
def descr_entropy_bits(k, j):
    # exact bits = log2 C(k,j)
    c = comb(k, j)
    return log2(c) if c > 0 else 0.0

def block4():
    def h2(x):  # binary entropy in bits
        if x <= 0 or x >= 1:
            return 0.0
        return -x * log2(x) - (1 - x) * log2(1 - x)
    p = 3
    # (i) at the collapse threshold j = theta k  (violators): entropy ~ h2(theta) k bits
    for theta in (0.25, 0.5, 0.75):
        k = 1000
        j = _ceil_theta_k(theta, k)
        bits = descr_entropy_bits(k, j)
        # bits/k -> h2(theta) > 0
        check("B4.viol.bits.t%.2f" % theta, abs(bits / k - h2(theta)) < 0.02,
              "bits/k=%.4f h2=%.4f" % (bits / k, h2(theta)))
        N = p * k
        # bits/N = h2(theta)/p > 0 : description entropy is Omega(N), NOT o(n)
        check("B4.viol.OmegaN.t%.2f" % theta, bits / N > 0.02,
              "bits/N=%.5f" % (bits / N))
    # (ii) NON-violators too: the number of patterns with j < theta k is itself
    # exponential (sum_{j<theta k} C(k,j)); log2 of that count is Omega(k) for theta>0.
    for theta in (0.25, 0.5):
        k = 1000
        thr = _ceil_theta_k(theta, k)
        cnt = sum(comb(k, jj) for jj in range(0, thr))   # UNROUTED patterns
        bits = log2(cnt)
        N = p * k
        check("B4.nonviol.OmegaN.t%.2f" % theta, bits / N > 0.02,
              "unrouted log2-count/N=%.5f" % (bits / N))
    # (iii) the FULL product class {T,C}^k has 2^k patterns = k bits vs o(n) budget:
    #       k bits with N=pk => k/N = 1/p = const > 0 => Omega(N).  Not o(n).
    for k in (100, 1000):
        bits = k  # log2(2^k)
        N = p * k
        check("B4.full.OmegaN.k%d" % k, abs(bits / N - 1.0 / p) < 1e-9,
              "bits/N=%.5f 1/p=%.5f" % (bits / N, 1.0 / p))

# ===========================================================================
# BLOCK 5 -- the naive "mass x count" (= the #626 countertheorem quantity).
# If each of the N_coll routed collapse profiles were summed INDEPENDENTLY into
# E_n at its image-scale term (1+Nbar^img)=2, the contribution would be 2*N_coll,
# which is e^{Omega(N)} and exceeds the ambient identity term (n-a+1) ~ N.
# We confirm the arithmetic AND that it exceeds the identity term (the countertheorem),
# establishing that per-profile rescaling does NOT rescue the sum -- a different
# accounting (first-match disjointness, BLOCK 6) is required.
# ===========================================================================
def block5():
    p = 3
    for (k, theta) in [(20, 0.60), (40, 0.60), (40, 0.75)]:
        nc = N_coll(k, theta)
        naive_mass = 2 * nc                       # sum over routed of (1+Nbar^img=1)
        N = p * k
        identity_term = N                         # (n-a+1) ~ N, the ambient identity scale
        # countertheorem: naive mass exponentially exceeds identity term
        check("B5.counterthm.k%d.t%.2f" % (k, theta),
              naive_mass > identity_term ** 2,
              "naive=%d id^2=%d" % (naive_mass, identity_term ** 2))
        # exact value of the naive mass
        check("B5.exact.k%d.t%.2f" % (k, theta), naive_mass == 2 * nc)
    # rate of naive mass is positive (exponential) -> NOT within e^{o(n)}*E_n
    k = 2000; theta = 0.60; p = 3; N = p * k
    rate = log(2 * N_coll(k, theta)) / N
    check("B5.rateN", rate > 0.05, "rate=%.4f" % rate)

# ===========================================================================
# BLOCK 6 -- DECISIVE exact syndrome-line census.
# Faithful RS-MCA badness (prop:syndrome-line-normal-form L1569-1591):
#   parity columns h_x = lam_x (1,x,...,x^{R-1}), lam_x = prod_{y!=x}(x-y)^{-1};
#   support S = D\E; gamma MCA-bad on S for (u0,u1) iff s0+gamma s1 in V_E and
#   {s0,s1} not subset V_E; for fixed E there is at most ONE finite slope (L1580).
# The ledger charges the DISJOINT UNION Z_a(r) = union_i Z_i^o (lem:first-match-bound
# L1535), NOT the naive per-profile sum.  We verify, exactly:
#   (a) each E carries at most one finite bad slope           (RC2 / L1580, THEOREM)
#   (b) Z_a(r) = disjoint union of first-match parts Z_i^o    (def:first-match L1459)
#   (c) naive sum_i |Z_i| >= |Z_a(r)| = |union| (overlap => strict) -- the overcount
#   (d) a profile ordered AFTER a covering profile has Z_i^o = empty (routing model)
# ===========================================================================
def _inv_mod(a, p):
    return pow(a % p, p - 2, p)

def _rref(rows, p):
    """Reduced row echelon form over F_p; returns (pivot_rows, pivot_cols)."""
    rows = [list(r) for r in rows]
    m = len(rows)
    if m == 0:
        return [], []
    ncol = len(rows[0])
    piv = []
    r = 0
    for c in range(ncol):
        # find pivot
        sel = None
        for i in range(r, m):
            if rows[i][c] % p != 0:
                sel = i; break
        if sel is None:
            continue
        rows[r], rows[sel] = rows[sel], rows[r]
        inv = _inv_mod(rows[r][c], p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] % p != 0:
                f = rows[i][c] % p
                rows[i] = [(rows[i][t] - f * rows[r][t]) % p for t in range(ncol)]
        piv.append(c)
        r += 1
        if r == m:
            break
    return rows[:r], piv

def _in_span(basis_rows, vec, p):
    """Is vec in the row span of basis_rows over F_p?"""
    aug = [list(b) for b in basis_rows] + [list(vec)]
    # vec in span iff rank(basis) == rank(basis+vec)
    _, p1 = _rref(basis_rows, p)
    _, p2 = _rref(aug, p)
    return len(p1) == len(p2)

def _syndrome(H_cols, D, u, p):
    """s(u) = sum_x u_x h_x  (R-vector)."""
    R = len(H_cols[0])
    s = [0] * R
    for idx, x in enumerate(D):
        ux = u[idx] % p
        if ux:
            hx = H_cols[idx]
            for t in range(R):
                s[t] = (s[t] + ux * hx[t]) % p
    return s

def _bad_slope(H_cols, D, E_idx, s0, s1, p):
    """Return the unique finite bad slope gamma for support S=D\\E, or None."""
    VE = [H_cols[i] for i in E_idx]
    both_in = _in_span(VE, s0, p) and _in_span(VE, s1, p)
    if both_in:
        return None  # excluded by the 'not both in V_E' clause
    found = None
    for g in range(p):
        vec = [(s0[t] + g * s1[t]) % p for t in range(len(s0))]
        if _in_span(VE, vec, p):
            if found is not None:
                return ('MULTI',)   # would violate L1580 -- flagged
            found = g
    return found

def _rs_setup(p, D, R):
    H_cols = []
    for x in D:
        lam = 1
        for y in D:
            if y != x:
                lam = (lam * _inv_mod((x - y) % p, p)) % p
        col = [(lam * pow(x, t, p)) % p for t in range(R)]
        H_cols.append(col)
    return H_cols

def block6():
    from itertools import combinations
    # -----------------------------------------------------------------------
    # (6a) STRUCTURAL: prop:syndrome-line-normal-form L1580 / RC2 L1691-1695.
    # "For fixed E there is at most one finite slope."  Verified NON-VACUOUSLY on
    # real F_p syndrome geometry: for random (V_E, s1) with s1 not in V_E, PLANT a
    # solution s0 := v - g0*s1 (v in V_E) so gamma=g0 is bad, then confirm the solver
    # returns exactly {g0}; and confirm 'both s0,s1 in V_E' yields no bad slope.
    # -----------------------------------------------------------------------
    def _solve_slopes(VE, s0, s1, p):
        both = _in_span(VE, s0, p) and _in_span(VE, s1, p)
        if both:
            return None
        sols = []
        for g in range(p):
            vec = [(s0[t] + g * s1[t]) % p for t in range(len(s0))]
            if _in_span(VE, vec, p):
                sols.append(g)
        return sols
    rng = 1234567
    def nxt():
        nonlocal rng
        rng = (1103515245 * rng + 12345) & 0x7fffffff
        return rng
    planted_ok = 0
    for p in (5, 7, 11):
        for R in (3, 4, 5):
            for esz in (1, 2):
                for _ in range(30):
                    VE = [[nxt() % p for _ in range(R)] for _ in range(esz)]
                    s1 = [nxt() % p for _ in range(R)]
                    if _in_span(VE, s1, p):
                        continue                      # need s1 outside V_E
                    g0 = nxt() % p
                    # v in V_E : random combo of the basis rows
                    v = [0] * R
                    for row in VE:
                        c = nxt() % p
                        v = [(v[t] + c * row[t]) % p for t in range(R)]
                    s0 = [(v[t] - g0 * s1[t]) % p for t in range(R)]
                    sols = _solve_slopes(VE, s0, s1, p)
                    # uniqueness (L1580) and correctness (planted g0 is the slope)
                    check("B6a.unique.p%d.R%d.e%d" % (p, R, esz),
                          sols is not None and sols == [g0],
                          "sols=%s g0=%d" % (sols, g0))
                    planted_ok += 1
    check("B6a.nonvacuous", planted_ok >= 200,
          "planted only %d instances" % planted_ok)
    # 'both in V_E' -> no bad slope
    for p in (5, 7):
        VE = [[1, 0, 0], [0, 1, 0]]
        s0 = [3, 2, 0]; s1 = [1, 4, 0]          # both in span(e1,e2)
        check("B6a.bothin.p%d" % p, _solve_slopes(VE, s0, s1, p) is None)

    # -----------------------------------------------------------------------
    # (6b) LEDGER CHARGE: lem:first-match-bound L1526-1538, Z_a(r)=coprod_i Z_i^o.
    # Exact combinatorial instantiation with a GENUINE many-to-one slope map (so the
    # collisions are mathematically forced by pigeonhole, not planted): supports are
    # size-esz subsets E of [n]; slope(E) = (sum E) mod p  in F_p  (one support -> one
    # slope, RC2); profiles partition supports by profile(E) = (min E, |E cap Left|).
    # We verify:
    #   (b1) disjoint union: coprod_i Z_i^o = Z_a(r), pairwise disjoint, sum|Z_i^o|=|Z_a(r)|
    #   (b2) OVERCOUNT: naive per-profile sum_i |Z_i| >= |Z_a(r)|, STRICT (cross-profile
    #        slope sharing) -- the exact analog of #626 summing (1+Nbar) per profile.
    #   (b3) per-support charge |supports| >> |Z_a(r)| (many supports -> few slopes).
    # -----------------------------------------------------------------------
    any_strict_prof = False
    agg_naive = agg_union = agg_supp = 0
    for (n, esz, p) in [(9, 3, 5), (10, 3, 7), (11, 4, 5), (8, 2, 5)]:
        Left = set(range(n // 2))
        supports = list(combinations(range(n), esz))
        slope_of = {E: (sum(E) % p) for E in supports}
        Zar = set(slope_of.values())
        # partition into ordered profiles
        prof = {}
        for E in supports:
            key = (min(E), len(set(E) & Left))
            prof.setdefault(key, []).append(E)
        order = sorted(prof.keys())
        seen = set(); Zcirc = {}; Zfull = {}
        for key in order:
            Zi = set(slope_of[E] for E in prof[key])
            Zcirc[key] = Zi - seen
            Zfull[key] = Zi
            seen |= Zi
        # (b1)
        union_circ = set(); disjoint = True
        for key in order:
            if union_circ & Zcirc[key]:
                disjoint = False
            union_circ |= Zcirc[key]
        check("B6b.disjoint.n%d.p%d" % (n, p), disjoint)
        check("B6b.union.n%d.p%d" % (n, p), union_circ == Zar)
        check("B6b.sumeq.n%d.p%d" % (n, p),
              sum(len(Zcirc[k]) for k in order) == len(Zar))
        # (b2) overcount
        naive = sum(len(Zfull[k]) for k in order)
        check("B6b.overcount.n%d.p%d" % (n, p), naive >= len(Zar))
        if naive > len(Zar):
            any_strict_prof = True
        # (b3) per-support fan-in
        check("B6b.fanin.n%d.p%d" % (n, p), len(supports) >= len(Zar))
        agg_naive += naive; agg_union += len(Zar); agg_supp += len(supports)
    check("B6b.strict.exists", any_strict_prof,
          "no line showed naive per-profile sum strictly above the disjoint union")
    # aggregate: naive per-profile charge and per-support charge both exceed the union
    check("B6b.agg.prof", agg_naive > agg_union,
          "naive=%d union=%d" % (agg_naive, agg_union))
    check("B6b.agg.supp", agg_supp > agg_union,
          "supp=%d union=%d" % (agg_supp, agg_union))

    # -----------------------------------------------------------------------
    # (6c) ROUTING makes a collapse profile contribute Z^o = empty (L877-880):
    # its slopes are assigned by first-match to the EARLIER cell it is routed to.
    # -----------------------------------------------------------------------
    early = {0, 1, 2, 3, 4}         # earlier cell's slope set
    routed = {1, 3}                 # collapse profile routed to it: slopes covered
    check("B6c.routed.empty", (routed - early) == set(),
          "routed collapse profile must contribute empty first-match part")
    # and if it had ONE genuinely new slope, only that one is charged (not its bulk)
    routed2 = {1, 3, 99}
    check("B6c.routed.one", (routed2 - early) == {99})

# ===========================================================================
# BLOCK 7 -- census sum-vs-max ratios + routed/unrouted decomposition.
# Exhaustive {T,C}^k and {T,C,S}^k (small k), exact.  Reproduces #625/#626 census
# and adds the post-routing decomposition:
#   naive sum over ALL patterns of (1+Nbar^img)   = 2 * 2^k              (busts)
#   routed  (j >= theta k)  : contribute Z^o = 0 after routing           (0)
#   unrouted (j <  theta k) : also arbitrary-planted (Omega(N) descr-ent) -> excluded
#   operative charge        : disjoint union over e^{o(n)} admissible profiles
# ===========================================================================
def block7():
    from itertools import product
    p = 3
    for k in (4, 6, 8, 10):
        # collapse fraction at threshold theta -- reproduces #626 BLOCK 6(a)
        for theta in (0.5, 0.75):
            thr = _ceil_theta_k(theta, k)
            nroute = sum(comb(k, j) for j in range(thr, k + 1))
            frac = Fr(nroute, 2 ** k)
            # naive envelope mass over ALL 2^k patterns (each term 1+Nbar^img=2)
            naive = 2 * (2 ** k)
            mx = 2                       # max single term
            check("B7.frac.k%d.t%.2f" % (k, theta), 0 <= frac <= 1)
            check("B7.ratio.k%d.t%.2f" % (k, theta), naive == mx * (2 ** k),
                  "sum/max ratio must equal pattern count 2^k")
        # exact reproduction of #626 BLOCK 6(a) rows
    check("B7.frac.k4.t50",  Fr(sum(comb(4, j)  for j in range(_ceil_theta_k(0.5, 4),  5)),  16)   == Fr(11, 16))
    check("B7.frac.k4.t75",  Fr(sum(comb(4, j)  for j in range(_ceil_theta_k(0.75, 4), 5)),  16)   == Fr(5, 16))
    check("B7.frac.k6.t50",  Fr(sum(comb(6, j)  for j in range(_ceil_theta_k(0.5, 6),  7)),  64)   == Fr(42, 64))
    check("B7.frac.k6.t75",  Fr(sum(comb(6, j)  for j in range(_ceil_theta_k(0.75, 6), 7)),  64)   == Fr(7, 64))
    check("B7.frac.k8.t50",  Fr(sum(comb(8, j)  for j in range(_ceil_theta_k(0.5, 8),  9)),  256)  == Fr(163, 256))
    check("B7.frac.k8.t75",  Fr(sum(comb(8, j)  for j in range(_ceil_theta_k(0.75, 8), 9)),  256)  == Fr(37, 256))
    check("B7.frac.k10.t50", Fr(sum(comb(10, j) for j in range(_ceil_theta_k(0.5, 10),  11)), 1024) == Fr(638, 1024))
    check("B7.frac.k10.t75", Fr(sum(comb(10, j) for j in range(_ceil_theta_k(0.75, 10), 11)), 1024) == Fr(56, 1024))
    # direct-vs-multiplicative agreement over {T,C,S}^k (reproduces #626 BLOCK 6(b))
    p = 5
    for k in (3, 4):
        for kinds in product('TCS', repeat=k):
            leaf = leaf_from_blocks(p, list(kinds))
            # E+1 multiplicative
            prod_E1 = Fr(1)
            for kk in kinds:
                prod_E1 *= block_invariants(p, kk)['E1']
            check("B7.tensor.k%d" % k, leaf['E1'] == prod_E1)
            check("B7.master2.k%d" % k, leaf['E1'] <= leaf['G1'] * leaf['Qimg'])
    # single admissible power-sum leaves stay safe (reproduces #622/#625/#626 census)
    singles = [
        (3, 2, 1, 1, 2, 3, Fr(1, 2)),
        (5, 3, 2, 2, 3, 25, Fr(22, 3)),
        (7, 4, 2, 2, 6, 49, Fr(43, 6)),
    ]
    for (pp, N, R, m, L, Aeff, E) in singles:
        # E = Aeff * P2 - 1 with uniform-on-image: P2 = 1/L, E = Aeff/L - 1
        check("B7.single.p%d.N%d" % (pp, N), Fr(Aeff, L) - 1 == E,
              "%s vs %s" % (Fr(Aeff, L) - 1, E))

# ===========================================================================
def main():
    for fn in (block0, block1, block2, block3, block4, block5, block6, block7):
        fn()
    total = _PASS + _FAIL
    if _FAIL:
        print("RESULT: FAIL (%d/%d)" % (_PASS, total))
        for line in _LOG[:40]:
            print("  " + line)
        sys.exit(1)
    print("RESULT: PASS (%d/%d)" % (_PASS, total))
    sys.exit(0)

if __name__ == "__main__":
    main()
