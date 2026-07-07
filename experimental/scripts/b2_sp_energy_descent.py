#!/usr/bin/env python3
"""Reframe (i): the L^4 / multiplicative-ENERGY descent. Is E(G_j)/E(G_{j-1}) bounded & stable?

E(G_j) := sum_{a in G_j}|T_a^{G_j}|^2 = (1/2^j) sum_t |phihat_{G_j}(t)|^4 = the mult-energy (OffDiag+diagonal).
Positive, additive; the index-2 split (x_i in G_{j-1} vs coset zeta G_{j-1}, parity-balanced) recurses it.
The per-level ENERGY ratio  kappa_j := E(G_j)/E(G_{j-1})  governs an inductive proof of E(G_k) <= K (2^k)^theta_E,
theta_E = 2*0.81 (since E ~ (2^j)^{2 theta} for max|phihat|~(2^j)^theta). PROOF viable iff kappa_j <= 2^{2*0.81}=
2^1.62=3.07 (geometric-mean sense) -- i.e. energy grows <= 3.07x/level; the trivial doubling gives ~4.
Also decompose E(G_j) into the all-even 'diagonal-subgroup' part (= E(G_{j-1})) and the coset cross part,
to expose the recursion.  Reports kappa_j, theta_E-exponent log_{2^j}(E), and E/(2^j p) (OffDiag-normalized).
"""
from __future__ import annotations
import math
import numpy as np
import sympy

P = 2**31 - 2**24 + 1
assert (P - 1) % (2**24) == 0 and sympy.isprime(P)


def phi_top(J, exps, c):
    N = 1 << J
    g = int(sympy.primitive_root(P)); zJ = pow(g, (P - 1) // N, P)
    powtab = np.empty(N, dtype=np.int64); cur = 1
    for m in range(N):
        powtab[m] = cur; cur = (cur * zJ) % P
    ar = np.arange(N, dtype=np.int64); fval = np.zeros(N, dtype=np.int64)
    for ci, j in zip(c, exps):
        if ci:
            fval = (fval + ci * powtab[(ar * j) % N]) % P
    return np.exp(2j * math.pi * fval / P)


def energy(phij):
    hat = np.fft.fft(phij)
    return (np.abs(hat) ** 4).sum() / len(phij)          # E(G_j) = (1/N) sum|phihat|^4


def run(label, c, J=18, Jmin=10):
    phiJ = phi_top(J, exps, c)
    prevE = None
    print(f"\n  [{label}]  j: (Nj)   E(G_j)      E/(2^j p)   theta_E=log_Nj(E)/1   kappa=E_j/E_{{j-1}}  (vs 2^1.62=3.07)")
    kappas = []
    for j in range(Jmin, J + 1):
        step = 1 << (J - j)
        phij = phiJ[::step]
        Nj = len(phij)
        E = energy(phij)
        thetaE = math.log(E) / math.log(Nj) if E > 1 else 0.0
        kappa = (E / prevE) if prevE is not None else float('nan')
        if not math.isnan(kappa):
            kappas.append(kappa)
        kk = f"{kappa:.3f}" if not math.isnan(kappa) else "  -  "
        print(f"      j={j:<3}(2^{j})  {E:11.1f}  {E/(Nj*P):8.4f}   {thetaE:.3f}(=2x{thetaE/2:.3f})    {kk}")
        prevE = E
    if kappas:
        print(f"      => kappa range [{min(kappas):.3f}, {max(kappas):.3f}], geo-mean {math.exp(np.mean(np.log(kappas))):.3f}"
              f"  (proof-viable if geo-mean <= 3.07; trivial doubling ~4)")


def main():
    global exps
    exps = [j for j in range(1, 512) if j % 2 == 1][:128]
    rng = np.random.default_rng(2)
    print("# L^4 energy descent E(G_j)=(1/2^j)sum|phihat|^4 (=mult-energy OffDiag+diag). deployed prime, 128 odd exps.")
    print("# kappa_j=E(G_j)/E(G_{j-1}); PROOF of E(G_k)<=K(2^k)^1.62 viable iff kappa geo-mean <= 2^1.62=3.07.")
    run("dense", rng.integers(1, P, size=len(exps), dtype=np.int64))
    cm = np.zeros(len(exps), dtype=np.int64); cm[0] = 1
    run("monomial x^1", cm)
    # adversarial for ENERGY (maximize E(G_J))
    def objE(cc):
        return energy(phi_top(18, exps, cc))
    best = rng.integers(1, P, size=len(exps), dtype=np.int64); cur = objE(best)
    for t in range(0, len(exps), 2):                        # every other coord (speed)
        cand = rng.integers(0, P, size=12, dtype=np.int64); bv, bo = best[t], cur
        for v in cand:
            best[t] = v; o = objE(best)
            if o > bo: bo, bv = o, v
        best[t] = bv; cur = bo
    run("adversarial(E)", best)
    print("\n# If kappa geo-mean <= ~3.07 for all c, the index-2 ENERGY recursion gives an inductive proof up the")
    print("#   tower; combine with a small-subgroup (BGK) base at ~sqrt p. theta_E ~ 2x0.60 => margin under 2x0.81.")


if __name__ == "__main__":
    raise SystemExit(main())
