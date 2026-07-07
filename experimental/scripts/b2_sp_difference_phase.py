#!/usr/bin/env python3
"""Attack (1): is the difference phase g(y)=f_c(zeta y)-f_c(y) SIMPLER than f_c, or self-similar?

Per-level butterfly at level J: domain G_{J-1}=mu_{2^{J-1}}=<z>, z=zeta^2, zeta=z_J (order 2^J).
  A[m] = e_p(f_c(zeta^{2m})),  B[m] = e_p(f_c(zeta^{2m+1})),  m=0..2^{J-1}-1.
  Ahat=DFT(A) (=phihat over G_{J-1}), Bhat=DFT(B) (coset half-spectrum), and the DIFFERENCE phase
  g-seq[m]=B[m]*conj(A[m])=e_p(g(z^m)), ghat=DFT(g-seq).  phihat_{G_J} = butterfly(Ahat,Bhat).
Decisive comparisons (dense + adversarial c), exponents = log_{2^{J-1}}(max):
  - exp(max|Ahat|)  [f_c sup]   vs   exp(max|ghat|)  [difference-phase sup]:
      exp(g) < exp(f_c) => g SIMPLER => descent bottoms out (a real gain).
      exp(g) ~ exp(f_c) => SELF-SIMILAR => descent is a pure induction over the phase class (no simplification).
  - PEAK-COINCIDENCE: at s*=argmax|Ahat|, |Bhat[s*]|/max|Bhat|  (small => peaks separated, ratio<2 explained),
    and the realized per-level sup ratio rho = max|phihat_{G_J}| / max|Ahat|.
  - does the (zeta^i-1) weighting bias g's coefficient sizes? report ||c'||-profile summary, c'_i=c_i(zeta^i-1).
"""
from __future__ import annotations
import math
import numpy as np
import sympy

P = 2**31 - 2**24 + 1
assert (P - 1) % (2**24) == 0 and sympy.isprime(P)


def setup(J, exps):
    N = 1 << J
    g0 = int(sympy.primitive_root(P)); zeta = pow(g0, (P - 1) // N, P)   # order 2^J
    powtab = np.empty(N, dtype=np.int64); cur = 1
    for m in range(N):
        powtab[m] = cur; cur = (cur * zeta) % P
    return zeta, powtab, N


def phases(c, exps, powtab, N):
    """A[m]=e_p(f_c(zeta^{2m})), B[m]=e_p(f_c(zeta^{2m+1})), m=0..N/2-1."""
    half = N // 2
    mA = np.arange(0, N, 2, dtype=np.int64)      # even exponents 2m
    mB = np.arange(1, N, 2, dtype=np.int64)      # odd exponents  2m+1
    fA = np.zeros(half, dtype=np.int64); fB = np.zeros(half, dtype=np.int64)
    for ci, i in zip(c, exps):
        if ci:
            fA = (fA + ci * powtab[(mA * i) % N]) % P
            fB = (fB + ci * powtab[(mB * i) % N]) % P
    return np.exp(2j * math.pi * fA / P), np.exp(2j * math.pi * fB / P)


def analyze(label, c, exps, zeta, powtab, N):
    A, B = phases(c, exps, powtab, N)
    half = len(A)
    Ah, Bh = np.fft.fft(A), np.fft.fft(B)
    gseq = B * np.conj(A)                          # e_p(g(z^m))
    gh = np.fft.fft(gseq)
    def ex(v):
        m = float(np.abs(v).max()); return m, (math.log(m) / math.log(half) if m > 1 else 0.0)
    mA_, eA = ex(Ah); mB_, eB = ex(Bh); mg_, eg = ex(gh)
    # butterfly: phihat_{G_J}(t) for t in Z/N; residue s, two values Ah[s] +/- omega^s Bh[s]
    s = np.arange(half); omega = np.exp(2j * math.pi * s / N)
    plus = np.abs(Ah + omega * Bh); minus = np.abs(Ah - omega * Bh)
    mfull = float(max(plus.max(), minus.max()))
    rho = mfull / mA_
    sstar = int(np.abs(Ah).argmax()); coincide = abs(Bh[sstar]) / mB_
    print(f"  [{label:<14}] exp|Ah|(f_c)={eA:.3f}  exp|ghat|(g)={eg:.3f}  {'g SIMPLER' if eg<eA-0.02 else 'SELF-SIMILAR'}"
          f"  | peak-coincide |Bh[argmaxA]|/max|Bh|={coincide:.3f}  rho={rho:.3f}")
    return eA, eg


def main():
    J = 18
    exps = [j for j in range(1, 4096) if j % 2 == 1][:256]
    zeta, powtab, N = setup(J, exps)
    rng = np.random.default_rng(3)
    print(f"# Difference phase g=f_c(zeta y)-f_c(y). Domain G_17=mu_2^17. exps=256 odd. Is g simpler than f_c?")
    # (zeta^i - 1) weighting profile
    cprime_abs = np.array([abs((pow(int(zeta), i, P) - 1) % P) for i in exps])
    print(f"# (zeta^i-1) magnitudes across exps: they are ~uniform in [0,p) (median {np.median(cprime_abs):.3e}, "
          f"p/2={P//2:.3e}) => no support reduction, generic reweighting.")
    dense = rng.integers(1, P, size=len(exps), dtype=np.int64)
    analyze("dense", dense, exps, zeta, powtab, N)
    cm = np.zeros(len(exps), dtype=np.int64); cm[0] = 1
    analyze("monomial x^1", cm, exps, zeta, powtab, N)
    # adversarial: maximize max|Ahat| (the f_c sup)
    def obj(cc):
        A, _ = phases(cc, exps, powtab, N); return float(np.abs(np.fft.fft(A)).max())
    best = rng.integers(1, P, size=len(exps), dtype=np.int64); cur = obj(best)
    for t in range(0, len(exps), 3):
        cand = rng.integers(0, P, size=10, dtype=np.int64); bv, bo = best[t], cur
        for v in cand:
            best[t] = v; o = obj(best)
            if o > bo: bo, bv = o, v
        best[t] = bv; cur = bo
    analyze("adversarial", best, exps, zeta, powtab, N)
    print("\n# VERDICT: if exp(g) ~ exp(f_c) (self-similar), the descent is a pure induction over the odd-phase")
    print("#   class -- proving the per-level lemma needs a SPECTRAL-NONCONCENTRATION statement for g, extracted")
    print("#   from the inductive hypothesis (the naive convolution/sup bound is too weak). Not a free reduction.")


if __name__ == "__main__":
    raise SystemExit(main())
