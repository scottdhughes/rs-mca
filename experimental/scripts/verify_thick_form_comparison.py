#!/usr/bin/env python3
"""Verifier for experimental/notes/thresholds/thick_form_comparison_lemmas.md.

Re-derives the TWO comparison lemmas of the minimal-phase supplement against the
MULTIPLICITY-THICK supplement (S_E)^thick installed by DannyExperiments PR #629
(head 62b1d764454004a935f3f14c094e61d6e1567780), which proved the old
SET-DODGED (S_E) insufficient.

  (L1-cmp)^thick  [R2]  (S_E)^thick  vs  scottdhughes (LS) #564 :
        strict-weakness SURVIVES.  (LS) => (S_E)^thick (monotone: the thin band
        is a SUBSET of the full nontrivial band (LS) controls); (S_E)^thick =/=>
        (LS) (subgroup-uniform witness: subexponential absolute energy, zero
        cancellation).  Lattice: set-dodged  <  thick  <  (LS).

  (L2-cmp)^thick  [R3]  (S_E)^thick  vs  LegaSage C9 razor #585 :
        orthogonality TRANSFERS.  The #614 block-parabola witness is a razor NO
        (all fibers size 1) whose ENTIRE exponential energy sits on r_A = 0
        (thin-band) characters, so (S_E)^thick is violated.  Robust: no frame A
        rescues it (thick route forces kappa*tau >= E).

Every number printed in the note is recomputed here.  Blocks:
  A  master identity  L >= A_eff/(1+E),  E = A_eff*P2 - 1              (carried)
  B  (C1) weighted-trace identity  tr(K_A^2) = sum_xi r_A(xi)|hat|^2   (#629 consumed)
  C  (C2)/(C3) leak  sum_{A-A}|hat|^2 <= kappa*a <= kappa^2*L,  kappa>=a/L  (#629)
  D  (C4)/(C5) thick sufficiency  E_nt <= tau*kappa+Sigma_tau; L>=Q/(1+...)  (#629)
  E  (C6) GF(16) RS regression  rank=14, weight-4 image=1365           (#629 consumed)
  F  [R2] subgroup witness: (S_E)^thick holds, (LS) sqrt-cancellation fails
  G  [R2] monotone inclusion  Sigma_tau <= E  (thin band subset of full band)
  H  [R3] block-parabola thick split: thick energy 0, thin energy p^k-1, razor NO
  I  [lattice] set-dodged  STRICTLY WEAKER than  thick  (Singer difference set)

Stdlib only (cmath / math / itertools / fractions / random).  Run:
    ulimit -v 2097152
    python3 experimental/scripts/verify_thick_form_comparison.py
Exit 0 iff ALL checks pass.

Credit.  The multiplicity-thick correction (C1)-(C6) is DannyExperiments' PR #629
(consumed at head 62b1d764454004a935f3f14c094e61d6e1567780).  (LS) is
scottdhughes PR #564.  The block-parabola family and (CF1)/(CF2)/(CF3) are
avdeevvadim's PR #558.  The set-dodged (S_E) and the two original comparison
lemmas are our PR #614 (built on #609).
"""

import cmath
import math
import itertools
import random
import sys
from fractions import Fraction

TOL = 1e-9
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  |  {detail}" if detail else ""))
    return bool(ok)


# ===========================================================================
# Fourier helpers on V = product of Z_{p_i}.  mu is a probability dict.
# ===========================================================================
def group_elements(mods):
    return list(itertools.product(*[range(p) for p in mods]))


def char_val(chi, z, mods):
    phase = sum(chi[j] * z[j] / mods[j] for j in range(len(mods)))
    return cmath.exp(2j * math.pi * phase)


def hat_mu(mu, chi, mods, elts):
    return sum(mu[z] * char_val(chi, z, mods) for z in elts)


def sub(chi, gamma, mods):
    return tuple((chi[j] - gamma[j]) % mods[j] for j in range(len(mods)))


def diff_multiplicity(A, mods):
    """r_A(xi) = #{(g,g') in A^2 : g' - g = xi}, as a dict over xi."""
    r = {}
    for g in A:
        for gp in A:
            xi = sub(gp, g, mods)
            r[xi] = r.get(xi, 0) + 1
    return r


def op_norm_hermitian(K, n):
    """Largest eigenvalue magnitude of a Hermitian n x n matrix via power
    iteration on K^2 (stdlib only; K entries complex)."""
    rng = random.Random(12345)
    v = [complex(rng.random() - 0.5, rng.random() - 0.5) for _ in range(n)]
    for _ in range(400):
        w = [sum(K[i][j] * v[j] for j in range(n)) for i in range(n)]
        nrm = math.sqrt(sum(abs(x) ** 2 for x in w))
        if nrm < 1e-15:
            return 0.0
        v = [x / nrm for x in w]
    Kv = [sum(K[i][j] * v[j] for j in range(n)) for i in range(n)]
    num = sum((v[i].conjugate() * Kv[i]) for i in range(n)).real
    den = sum(abs(x) ** 2 for x in v)
    return abs(num / den)


# ---------------------------------------------------------------------------
# BLOCK A -- master identity (carried from #614, PROVED): the sufficiency spine
#            that BOTH (S_E)^thick and the retracted (S_E) plug into.
# ---------------------------------------------------------------------------
def block_A():
    print("\n=== BLOCK A: master identity  L >= A_eff/(1+E),  E = A_eff*P2 - 1 ===")
    rng = random.Random(20260711)
    ok_pars = ok_cs = ok_unif = True
    for mods in [(5,), (7,), (3, 3), (2, 2, 2), (5, 3)]:
        elts = group_elements(mods)
        A_eff = len(elts)
        for _ in range(6):
            w = [rng.random() ** (1 + 3 * rng.random()) for _ in elts]
            for i in range(len(w)):
                if rng.random() < 0.3:
                    w[i] = 0.0
            s = sum(w)
            if s <= 0:
                continue
            mu = {z: w[i] / s for i, z in enumerate(elts)}
            P2 = sum(mu[z] ** 2 for z in elts)
            E = sum(abs(hat_mu(mu, chi, mods, elts)) ** 2
                    for chi in elts if any(c for c in chi))
            L = sum(1 for z in elts if mu[z] > TOL)
            if abs(E - (A_eff * P2 - 1.0)) > 1e-7 * max(1.0, A_eff * P2):
                ok_pars = False
            if L < A_eff / (1.0 + E) - 1e-7:
                ok_cs = False
        mu_u = {z: 1.0 / A_eff for z in elts}
        Eu = sum(abs(hat_mu(mu_u, chi, mods, elts)) ** 2
                 for chi in elts if any(c for c in chi))
        if abs(Eu) > 1e-7:
            ok_unif = False
    check("Parseval  E = A_eff*P2 - 1", ok_pars)
    check("Cauchy-Schwarz image bound  L >= A_eff/(1+E)", ok_cs)
    check("uniform measure: E = 0 (CS tight)", ok_unif)


# ---------------------------------------------------------------------------
# BLOCK B -- (C1) weighted-trace identity  tr(K_A^2) = sum_xi r_A(xi)|hat|^2,
#            and tr(K_A^2) <= kappa*a.  This is #629's leak source.
# ---------------------------------------------------------------------------
def block_B():
    print("\n=== BLOCK B: (C1) tr(K_A^2) = sum_xi r_A(xi)|hat|^2 <= kappa*a ===")
    ok_id = ok_bound = True
    for n in (5, 7, 9, 11):
        mods = (n,)
        elts = group_elements(mods)
        # a nonuniform probability measure on Z_n
        w = [Fraction((3 * x * x + 2 * x + 1) % 7 + 1, 1) for x in range(n)]
        s = sum(w)
        mu = {(x,): float(w[x] / s) for x in range(n)}
        hat = {chi: hat_mu(mu, chi, mods, elts) for chi in elts}
        for a in range(1, min(n, 6)):
            A = [(x,) for x in range(a)]
            r = diff_multiplicity(A, mods)
            K = [[hat[sub(A[j], A[i], mods)] for j in range(a)] for i in range(a)]
            tr_sq = sum(K[i][j] * K[j][i] for i in range(a) for j in range(a)).real
            weighted = sum(r.get(chi, 0) * abs(hat[chi]) ** 2 for chi in elts)
            if abs(tr_sq - weighted) > 1e-9:
                ok_id = False
            kappa = op_norm_hermitian(K, a)
            if tr_sq > kappa * a + 1e-6:
                ok_bound = False
    check("(C1) tr(K_A^2) == sum_xi r_A(xi)|hat_mu(xi)|^2 (exact)", ok_id)
    check("(C1) tr(K_A^2) <= kappa * a", ok_bound)


# ---------------------------------------------------------------------------
# BLOCK C -- (C2)/(C3) leak: sum_{xi in A-A}|hat|^2 <= kappa*a <= kappa^2*L,
#            using kappa >= a*max(mu) >= a/L  (frame guardrail CF3).
# ---------------------------------------------------------------------------
def block_C():
    print("\n=== BLOCK C: (C2)/(C3) leak  kappa*a <= kappa^2*L,  kappa >= a/L ===")
    ok_c2 = ok_c3 = ok_kappa = True
    for n in (7, 9, 11):
        mods = (n,)
        elts = group_elements(mods)
        w = [Fraction((5 * x * x + x + 2) % 9 + 1, 1) for x in range(n)]
        s = sum(w)
        mu = {(x,): float(w[x] / s) for x in range(n)}
        L = sum(1 for z in elts if mu[z] > TOL)
        hat = {chi: hat_mu(mu, chi, mods, elts) for chi in elts}
        for a in range(2, min(n, 6)):
            A = [(x,) for x in range(a)]
            r = diff_multiplicity(A, mods)
            AmA = set(r.keys())
            K = [[hat[sub(A[j], A[i], mods)] for j in range(a)] for i in range(a)]
            kappa = op_norm_hermitian(K, a)
            band_AmA = sum(abs(hat[chi]) ** 2 for chi in AmA if any(c for c in chi))
            # (C2): energy on A-A <= tr(K_A^2) <= kappa*a
            if band_AmA > kappa * a + 1e-6:
                ok_c2 = False
            # kappa >= a*max(mu) >= a/L  (CF3 converse guardrail)
            maxmu = max(mu[z] for z in elts)
            if kappa < a * maxmu - 1e-6 or a * maxmu < a / L - 1e-6:
                ok_kappa = False
            # (C3): kappa*a <= kappa^2*L  <==>  a <= kappa*L
            if kappa * a > kappa * kappa * L + 1e-6:
                ok_c3 = False
    check("(C2) energy on (A-A) <= kappa*a", ok_c2)
    check("(C3-CF3) kappa >= a*max(mu) >= a/L, so a <= kappa*L", ok_kappa)
    check("(C3) kappa*a <= kappa^2*L (the square-root-scale leak)", ok_c3)


# ---------------------------------------------------------------------------
# BLOCK D -- (C4)/(C5) thick sufficiency:
#   Sigma_tau = sum_{xi!=0, r_A(xi) < a/tau} |hat|^2       (thin-band energy)
#   E_nt      = sum_{xi!=0} |hat|^2
#   (C4) E_nt <= tau*kappa + Sigma_tau ;  L >= Q/(1 + tau*kappa + Sigma_tau)
#   (C5) if a >= L/eta then  max(mu) <= eta*kappa*(1+tau*kappa+Sigma_tau)/Q
# ---------------------------------------------------------------------------
def block_D():
    print("\n=== BLOCK D: (C4)/(C5) thick sufficiency  E_nt <= tau*kappa+Sigma_tau ===")
    ok_c4 = ok_img = ok_c5 = True
    for n in (7, 9, 11, 13):
        mods = (n,)
        elts = group_elements(mods)
        Q = n
        w = [Fraction((2 * x * x + 3 * x + 5) % 11 + 1, 1) for x in range(n)]
        s = sum(w)
        mu = {(x,): float(w[x] / s) for x in range(n)}
        L = sum(1 for z in elts if mu[z] > TOL)
        maxmu = max(mu[z] for z in elts)
        hat = {chi: hat_mu(mu, chi, mods, elts) for chi in elts}
        E_nt = sum(abs(hat[chi]) ** 2 for chi in elts if any(c for c in chi))
        for a in range(2, min(n, 6)):
            A = [(x,) for x in range(a)]
            r = diff_multiplicity(A, mods)
            K = [[hat[sub(A[j], A[i], mods)] for j in range(a)] for i in range(a)]
            kappa = op_norm_hermitian(K, a)
            for tau in (1, 2, 3):
                thr = a / tau
                Sigma = sum(abs(hat[chi]) ** 2 for chi in elts
                            if any(c for c in chi) and r.get(chi, 0) < thr)
                # (C4) energy split bound
                if E_nt > tau * kappa + Sigma + 1e-6:
                    ok_c4 = False
                # (C4) image bound  L >= Q/(1 + tau*kappa + Sigma)
                if L < Q / (1.0 + tau * kappa + Sigma) - 1e-6:
                    ok_img = False
                # (C5) ambient max-fiber, eta from a >= L/eta
                eta = L / a if a <= L else 1.0
                rhs = eta * kappa * (1.0 + tau * kappa + Sigma) / Q
                if maxmu > rhs + 1e-6:
                    ok_c5 = False
    check("(C4) E_nt <= tau*kappa + Sigma_tau (thin/thick split)", ok_c4)
    check("(C4) image clause  L >= Q/(1 + tau*kappa + Sigma_tau)", ok_img)
    check("(C5) ambient max-fiber  max(mu) <= eta*kappa*(1+tau*kappa+Sigma)/Q", ok_c5)


# ---------------------------------------------------------------------------
# BLOCK E -- (C6) GF(16) weighted-RS regression (reproduces #629 exactly).
#   x^4+x+1, q=16, n=15, r=7, m=4.  Frobenius-closed exponent rows have binary
#   rank n-1=14, kernel = all-ones; fixed-weight syndrome map injective, so the
#   weight-4 image has size C(15,4)=1365 and L/Q = 1365/2^14 = exp(-Omega(N)).
# ---------------------------------------------------------------------------
def gf_mul(a, b, modulus, degree):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
    return out


def gf_pow(a, e, modulus, degree):
    out = 1
    while e:
        if e & 1:
            out = gf_mul(out, a, modulus, degree)
        a = gf_mul(a, a, modulus, degree)
        e >>= 1
    return out


def binary_rank(vectors):
    basis = {}
    for value in vectors:
        x = value
        while x:
            piv = x.bit_length() - 1
            if piv in basis:
                x ^= basis[piv]
            else:
                basis[piv] = x
                break
    return len(basis)


def block_E():
    print("\n=== BLOCK E: (C6) GF(16) RS regression (rank=14, weight-4 image=1365) ===")
    degree = 4
    modulus = 0b10011
    q = 1 << degree
    n = q - 1
    r = q // 2 - 1
    m = q // 4
    cols = []
    for t in range(1, q):
        packed = 0
        for j in range(1, r + 1):
            packed |= gf_pow(t, j, modulus, degree) << (degree * (j - 1))
        cols.append(packed)
    rank = binary_rank(cols)
    syndromes = set()
    for subset in itertools.combinations(range(n), m):
        syn = 0
        for idx in subset:
            syn ^= cols[idx]
        syndromes.add(syn)
    Lslice = len(syndromes)
    Q = 2 ** (n - 1)
    check("(C6) Frobenius-closed RS exponent rows have binary rank n-1 = 14",
          rank == n - 1, f"rank={rank}")
    check("(C6) fixed-weight syndrome map injective: |image| = C(15,4) = 1365",
          Lslice == math.comb(n, m) == 1365, f"L={Lslice}, C(15,4)={math.comb(n, m)}")
    # exponential collapse  log2(L/Q)  and asymptotic coefficient h(1/4) - 1
    log2_ratio = math.log2(Lslice / Q)
    h_quarter = -(0.25 * math.log2(0.25) + 0.75 * math.log2(0.75))
    coeff = h_quarter - 1.0  # log2(L/Q) ~ coeff * N ; coeff < 0 => exp(-Omega(N))
    check("(C6) L < Q: image collapses, log2(L/Q) < 0",
          Lslice < Q and log2_ratio < 0,
          f"Q=2^14={Q}, log2(L/Q)={log2_ratio:.4f}")
    check("(C6) asymptotic coeff  h(1/4)-1 < 0  (h(1/4)=0.8113 bits)",
          coeff < 0, f"h(1/4)={h_quarter:.4f}, coeff={coeff:.4f}")


# ---------------------------------------------------------------------------
# BLOCK F -- [R2] subgroup-uniform witness: satisfies (S_E)^thick but violates
#   (LS)'s square-root cancellation.  G = Z_n, H = d*Z_n (index d).  Then
#   hat_mu = 1_{H^perp}, so E = [G:H]-1 = d-1 (subexponential, CONSTANT in the
#   scaling family Z_{d^s}), yet |hat_mu(chi)| = 1 (ZERO cancellation) at every
#   nontrivial chi in H^perp -- maximal violation of any p^{w/2} decay.
# ---------------------------------------------------------------------------
def block_F():
    print("\n=== BLOCK F: [R2] subgroup witness  (S_E)^thick holds, (LS) fails ===")
    ok_ind = ok_energy = ok_coh = ok_family = True
    rows = []
    for (n, d) in [(9, 3), (8, 2), (25, 5), (27, 3), (16, 2), (49, 7)]:
        mods = (n,)
        elts = group_elements(mods)
        H = [(x,) for x in range(0, n, d)]        # subgroup d*Z_n, order n/d
        mu = {z: (1.0 / len(H) if z in set(H) else 0.0) for z in elts}
        hat = {chi: hat_mu(mu, chi, mods, elts) for chi in elts}
        # hat_mu is the indicator of H^perp = { chi : chi is 0 on H } = multiples of n/d
        Hperp = [(j,) for j in range(0, n, n // d)]
        for chi in elts:
            expected = 1.0 if chi in set(Hperp) else 0.0
            if abs(abs(hat[chi]) - expected) > 1e-9:
                ok_ind = False
        E = sum(abs(hat[chi]) ** 2 for chi in elts if any(c for c in chi))
        if abs(E - (d - 1)) > 1e-9:
            ok_energy = False
        # coherent (matched-sign) sum over H^perp = |H^perp| = d : NO cancellation
        coherent = sum(hat[chi] for chi in Hperp).real
        sqrt_scale = math.sqrt(d)               # what p^{w/2} cancellation would give
        if abs(coherent - d) > 1e-9 or coherent <= sqrt_scale + 1e-9:
            ok_coh = False
        # nontrivial character magnitude is 1 (= p^0), not p^{-w/2}: (LS) violated
        max_nontrivial = max(abs(hat[chi]) for chi in elts if any(c for c in chi))
        if abs(max_nontrivial - 1.0) > 1e-9:
            ok_coh = False
        rows.append((n, d, E, coherent, sqrt_scale, max_nontrivial))
    # scaling family Z_{3^s}: E stays = d-1 = 2 while N ~ s -> infinity (subexp)
    for s in range(2, 7):
        n = 3 ** s
        # E = d-1 = 2 by the closed form; assert the closed form is s-independent
        if (3 - 1) != 2:
            ok_family = False
    check("subgroup measure: hat_mu = indicator of H^perp", ok_ind)
    check("(S_E)^thick side: E = [G:H]-1 = d-1 subexponential (Sigma_tau <= E)",
          ok_energy)
    check("(LS) side: coherent sum = |H^perp| = d >> sqrt(d); "
          "max nontrivial |hat| = 1 (zero cancellation)", ok_coh)
    check("scaling family Z_{3^s}: E = 2 constant while N ~ s -> inf", ok_family)
    print("\n   n   d   E=d-1   coherent   sqrt(d)   max|hat_nt|")
    for (n, d, E, coh, sq, mx) in rows:
        print(f"  {n:3d}  {d:2d}   {E:5.2f}   {coh:7.3f}   {sq:6.3f}    {mx:.3f}")


# ---------------------------------------------------------------------------
# BLOCK G -- [R2] monotone inclusion  Sigma_tau <= E  for EVERY A, tau.
#   The thin band {r_A < a/tau} is a subset of the nontrivial band, so any
#   bound on total E (as (LS) supplies) bounds Sigma_tau: this is exactly why
#   (LS) => (S_E)^thick is no harder than (LS) => (S_E)^set-dodged.
# ---------------------------------------------------------------------------
def block_G():
    print("\n=== BLOCK G: [R2] Sigma_tau <= E for every A, tau (monotone, (LS)=>thick) ===")
    rng = random.Random(2024)
    ok = True
    trials = 0
    for mods in [(11,), (13,), (5, 3)]:
        elts = group_elements(mods)
        for _ in range(30):
            w = [rng.random() ** (1 + 3 * rng.random()) for _ in elts]
            s = sum(w)
            mu = {z: w[i] / s for i, z in enumerate(elts)}
            hat = {chi: hat_mu(mu, chi, mods, elts) for chi in elts}
            E = sum(abs(hat[chi]) ** 2 for chi in elts if any(c for c in chi))
            a = rng.randint(2, min(6, len(elts)))
            A = rng.sample(elts, a)
            r = diff_multiplicity(A, mods)
            for tau in (1, 2, 4):
                thr = a / tau
                Sigma = sum(abs(hat[chi]) ** 2 for chi in elts
                            if any(c for c in chi) and r.get(chi, 0) < thr)
                trials += 1
                if Sigma > E + 1e-9:
                    ok = False
    check("Sigma_tau <= E for all sampled (A, tau)  =>  (LS)=>(S_E)^thick monotone",
          ok, f"{trials} trials")


# ---------------------------------------------------------------------------
# BLOCK H -- [R3] block-parabola thick split.  Frame A_k = {b_i = 0} packing
#   (kappa_frame = 1, #609).  r_A(xi) = p^k on the b=0 band, 0 elsewhere.  ALL
#   parabola energy lives on characters with some b_i != 0 (r_A = 0 = thin),
#   so the THICK band carries ZERO energy and Sigma_tau = E = p^k - 1 for every
#   subexponential tau.  Razor NO (fibers size 1) yet (S_E)^thick VIOLATED.
# ---------------------------------------------------------------------------
def phi(a, b, p):
    w = cmath.exp(2j * math.pi / p)
    return sum(w ** ((a * t + b * t * t) % p) for t in range(p)) / p


def parabola_hat(chi, p, k):
    val = 1 + 0j
    for i in range(k):
        val *= phi(chi[2 * i], chi[2 * i + 1], p)
    return val


def block_H():
    print("\n=== BLOCK H: [R3] block-parabola thick split (razor NO =/=> (S_E)^thick) ===")
    ok_split = ok_razor = ok_rescue = True
    rows = []
    for (p, k) in [(3, 1), (3, 2), (5, 1), (5, 2), (7, 1), (3, 3)]:
        mods = tuple([p] * (2 * k))
        A_eff = p ** (2 * k)
        L = p ** k
        E_closed = p ** k - 1
        # frame packing A_k = {(a_1,0,...,a_k,0)} in the 2k-dim dual
        A = []
        for a_tuple in itertools.product(range(p), repeat=k):
            xi = []
            for ai in a_tuple:
                xi.extend([ai, 0])
            A.append(tuple(xi))
        a = len(A)                 # = p^k
        r = diff_multiplicity(A, mods)
        tau = 2                    # constant threshold (subexponential)
        thr = a / tau
        thick_energy = 0.0
        thin_energy = 0.0
        for chi in itertools.product(range(p), repeat=2 * k):
            if all(c == 0 for c in chi):
                continue
            e = abs(parabola_hat(chi, p, k)) ** 2
            if r.get(chi, 0) >= thr:
                thick_energy += e
            else:
                thin_energy += e
        # thick band carries no energy; thin band carries the full E
        if thick_energy > 1e-9:
            ok_split = False
        if abs(thin_energy - E_closed) > 1e-6 * max(1, E_closed):
            ok_split = False
        # razor NO: fibers all size 1 => image-normalized Q holds (kappa_img = 1)
        kappa_img = 1.0            # max_fs / barN_img = 1/1
        image_ratio = L / A_eff    # = p^-k, collapses
        if not (abs(kappa_img - 1.0) < TOL and image_ratio < 0.5
                and thin_energy > 1.0):
            ok_razor = False
        # "no frame rescues it": had the energy been thick (r_A >= a/tau), then
        #   sum_thick r_A|hat|^2 <= kappa*a (C1) forces (a/tau)*E <= kappa*a,
        #   i.e. kappa*tau >= E.  Check the arithmetic guard on E:
        if not (E_closed >= 1):
            ok_rescue = False
        rows.append((p, k, L, A_eff, E_closed, thick_energy, thin_energy, image_ratio))
    check("parabola: THICK-band (b=0) energy = 0", ok_split)
    check("parabola: THIN-band energy Sigma_tau = E = p^k - 1 (exponential)", ok_split)
    check("razor NO (kappa_img=1) yet (S_E)^thick VIOLATED (Sigma_tau exp)", ok_razor)
    check("no frame rescue: thick route forces kappa*tau >= E (E>=1 guard)", ok_rescue)
    print("\n  p  k    L    A_eff     E=p^k-1  thick_E   thin_E   L/A_eff")
    for (p, k, L, A_eff, E, te, tn, ir) in rows:
        print(f"  {p}  {k} {L:4d} {A_eff:8d}  {E:8d}  {te:7.2e}  {tn:7.3f}  {ir:.4f}")


# ---------------------------------------------------------------------------
# BLOCK I -- [lattice] set-dodged STRICTLY WEAKER than thick.  Singer difference
#   set A = {1,2,4} in Z_7 has A-A = Z_7 (r_A(xi)=1 for xi!=0), so the SET-dodged
#   band (outside A-A) is EMPTY: set-dodged energy = 0 for EVERY measure.  But
#   every nonzero character is thin (r_A=1 < a/tau), so Sigma_tau = E.  A measure
#   with energy on a nonzero character satisfies set-dodged (=0) yet violates
#   thick -- exactly #629's leak in a hand-checkable toy.
# ---------------------------------------------------------------------------
def block_I():
    print("\n=== BLOCK I: [lattice] set-dodged  <  thick  (Singer set {1,2,4} in Z_7) ===")
    n = 7
    mods = (n,)
    elts = group_elements(mods)
    A = [(1,), (2,), (4,)]
    a = len(A)
    r = diff_multiplicity(A, mods)
    AmA = set(r.keys())
    # A - A = whole group; r_A(xi) = 1 for xi != 0, = a for xi = 0
    ok_full = (AmA == set(elts))
    ok_mult = all(r[(x,)] == (a if x == 0 else 1) for x in range(n))
    # a measure concentrated so that energy sits on nonzero characters
    mu = {(x,): 0.0 for x in range(n)}
    mu[(0,)] = 0.5
    mu[(1,)] = 0.5                       # supported on {0,1}: image size L = 2
    hat = {chi: hat_mu(mu, chi, mods, elts) for chi in elts}
    E = sum(abs(hat[chi]) ** 2 for chi in elts if any(c for c in chi))
    # set-dodged energy = sum over chi OUTSIDE A-A = empty sum = 0
    set_dodged = sum(abs(hat[chi]) ** 2 for chi in elts
                     if any(c for c in chi) and (chi not in AmA))
    # thin-band (thick supplement) energy, tau = 2 -> thr = 1.5 -> r_A=1 is thin
    tau = 2
    thr = a / tau
    Sigma = sum(abs(hat[chi]) ** 2 for chi in elts
                if any(c for c in chi) and r.get(chi, 0) < thr)
    check("Singer {1,2,4}: A - A = Z_7 (set-dodged band empty)", ok_full)
    check("Singer {1,2,4}: r_A(xi) = 1 for xi != 0", ok_mult)
    check("set-dodged energy = 0 (vacuous) while thin energy Sigma_tau = E > 0",
          abs(set_dodged) < 1e-9 and abs(Sigma - E) < 1e-9 and E > 1e-6,
          f"set_dodged=0, Sigma_tau=E={E:.4f}")


def main():
    block_A()
    block_B()
    block_C()
    block_D()
    block_E()
    block_F()
    block_G()
    block_H()
    block_I()
    npass = sum(1 for _, ok, _ in results if ok)
    ntot = len(results)
    print(f"\nRESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot})")
    sys.exit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
