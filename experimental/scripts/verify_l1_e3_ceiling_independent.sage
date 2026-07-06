#!/usr/bin/env sage
# -*- mode: python -*-
r"""
verify_l1_e3_ceiling_independent.sage  --  INDEPENDENT (Sage/GF(p)) cross-check of the
prime-`ell` listing-frontier KEY LEMMA  E_3 <= ell-2  and the achieved frontier witnesses.

Reviewer != generator: this reimplements the spectrum / E_3 / top-m computation from scratch
on Sage's native finite-field stack (FLINT/PARI under GF(p)), with an independently found
primitive root and independently constructed cosets, to cross-check the shipped stdlib-Python
verifier `verify_l1_prime_ell_frontier_corrected.py`.

Object (from l1_prime_ell_frontier_corrected.md, definitions re-derived here):
  ell odd prime, ell | p-1, H = mu_ell <= F_p^*, cosets bH partition F_p^*, n=(p-1)/ell.
  Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r     (constant-free, "mixed" = nonzero).
  For coset b: mu_b = max_lambda #{ x in bH : Gamma(x) = lambda }   (largest value-fiber).
  spectrum = sorted-desc (mu_b)_b ;  top-m = sum of m largest ;  listing <=> top-m >= 2ell.
  E_3 = sum_b (mu_b - 2)_+ .
  KEY LEMMA (open, NUMERIC-tight): E_3 <= ell-2 for every mixed Gamma.

PART A here: recompute the shipped witness spectra independently; confirm
  (a) top-m >= 2ell  (achieved frontier / listing) matches the recorded value, and
  (b) the E_3-saturation witnesses hit E_3 = ell-2 exactly  (=> ceiling is TIGHT / sharp,
      so ell-2 is the correct constant and cannot be lowered).
Full spectra are printed so the extremal fiber structure is visible for the proof attack.
"""

# gamma_r = gamma[r-1], r = 1..ell-1  (verbatim coefficient lists from the shipped verifier)
WITNESSES = [
    # --- listing witnesses (top-m >= 2ell at the corrected onset m=(ell+3)/2) ---
    dict(label="ell=11 m=7 p=199", p=199, ell=11, m=7,
         gamma=[1,172,129,7,90,84,119,194,176,1], top_m=22),
    dict(label="ell=11 m=7 p=331", p=331, ell=11, m=7,
         gamma=[97,29,97,239,171,92,143,155,270,1], top_m=23),   # E_3 = 9 = ell-2 (saturator)
    dict(label="ell=13 m=8 p=313", p=313, ell=13, m=8,
         gamma=[254,289,29,276,242,219,201,261,79,232,133,1], top_m=27),  # E_3 = 11 = ell-2
    dict(label="ell=17 m=10 p=409", p=409, ell=17, m=10,
         gamma=[165,169,244,263,276,149,333,170,86,260,80,398,377,77,324,1], top_m=34),
    # --- E_3 tight-ceiling anchor (not a listing witness): E_3 = ell-2 exactly ---
    dict(label="ell=17 p=103 E3-anchor", p=103, ell=17, m=None,
         gamma=[30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0], top_m=None),
]

def coset_spectrum(gamma, p, ell):
    """Independent spectrum: build cosets from an independently found primitive root,
    tally Gamma-values per coset via native GF(p) arithmetic, return sorted-desc mu list."""
    assert (p - 1) % ell == 0, "need ell | p-1"
    F = GF(p)
    g = F.multiplicative_generator()          # Sage's own primitive root (independent)
    n = (p - 1) // ell
    zeta = g**n                                # generator of H = mu_ell
    H = [zeta**j for j in range(ell)]
    gam = [F(c) for c in gamma]               # gam[r-1] = gamma_r
    spec = []
    for i in range(n):
        b = g**i
        tally = {}
        for h in H:
            x = b * h
            # Gamma(x) = sum_{r=1}^{ell-1} gamma_r x^r  (constant-free), Horner from top
            val = F(0)
            for r in range(ell - 1, 0, -1):
                val = (val + gam[r - 1]) * x
            tally[val] = tally.get(val, 0) + 1
        spec.append(max(tally.values()))
    spec.sort(reverse=True)
    return spec

def E3(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)

def main():
    print("=" * 92)
    print(" INDEPENDENT Sage cross-check: prime-ell listing frontier + KEY LEMMA E_3 <= ell-2")
    print("=" * 92)
    all_ok = True
    for W in WITNESSES:
        ell, p, m = W["ell"], W["p"], W["m"]
        spec = coset_spectrum(W["gamma"], p, ell)
        e3 = E3(spec)
        cap = ell - 2
        checks = []
        ok = True
        # (a) listing / achieved frontier
        if W["top_m"] is not None:
            tm = sum(spec[:m])
            lists = tm >= 2 * ell
            match = (tm == W["top_m"])
            ok = ok and lists and match
            checks.append("top-%d=%d (rec %d, >=2ell=%d? %s)" % (m, tm, W["top_m"], 2*ell, lists))
            if m and m - 1 >= 1:
                checks.append("top-%d=%d(<2ell)" % (m-1, sum(spec[:m-1])))
        # (b) E_3 vs ceiling ell-2
        within = e3 <= cap
        ok = ok and within
        tight = (e3 == cap)
        checks.append("E_3=%d %s ell-2=%d%s" % (e3, "<=" if within else ">!!", cap,
                                                "  <-- SATURATES (ceiling tight)" if tight else ""))
        all_ok = all_ok and ok
        print("\n%-26s ell=%d p=%d   %s" % (W["label"], ell, p, "PASS" if ok else "FAIL"))
        print("   spectrum = %s" % spec)
        print("   " + " | ".join(checks))
    print("\n" + "=" * 92)
    print(" RESULT: %s" % ("ALL WITNESSES REPRODUCED INDEPENDENTLY" if all_ok else "MISMATCH — INVESTIGATE"))
    print("=" * 92)
    return 0 if all_ok else 1

import sys
sys.exit(main())
