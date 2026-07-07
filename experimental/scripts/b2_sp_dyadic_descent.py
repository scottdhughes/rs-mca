#!/usr/bin/env python3
"""Attack the CRUX via dyadic descent: is max_t|phihat_{G_j}| provable by induction up the 2-power tower?

G_j = mu_{2^j} subset F_p (nested: G_{j-1} = <z_j^2> subset G_j). phi_j[m] = e_p(f_c(z_j^m)), and
phihat_{G_j}(chi_t) = DFT(phi_j)_t.  The tower is EXACTLY the FFT decimation-in-time butterfly:
phi_{G_{j-1}} = even subsamples of phi_{G_j}, and phihat_{G_j}(t) = A_t + w^t B_t where A = DFT of even
samples (= over G_{j-1}), B = DFT of odd samples (= over the coset zeta G_{j-1}).  So an INDUCTIVE proof
of  max_t |phihat_{G_j}| <= (2^j)^theta  needs the per-level ratio
    rho_j := max_t|phihat_{G_j}| / max_t|phihat_{G_{j-1}}|
to satisfy  rho_j <= 2^theta = 2^0.81 = 1.75  (bound stays ON SCALE, descent PROVES the sup bound);
rho_j ~ 2 would only give a mild constant 2^{(k-j0)(1-theta)} accumulation.  This script measures rho_j
across the tower for dense / adversarial / monomial c, plus the A/B cancellation |phihat|/(|A|+|B|).
DECISIVE: if rho_j <= ~1.75 uniformly, the dyadic-descent inverse theorem is a viable PROOF route.
"""
from __future__ import annotations
import math
import numpy as np
import sympy

P = 2**31 - 2**24 + 1          # deployed KoalaBear prime; v_2(p-1)=24 so mu_{2^j} exists for j<=24
assert (P - 1) % (2**24) == 0 and sympy.isprime(P)


def phi_top(J, exps, c):
    """phi_J[m] = e_p(f_c(z_J^m)), m=0..2^J-1, via power-table indexing (z_J = element of order 2^J)."""
    N = 1 << J
    g = int(sympy.primitive_root(P)); zJ = pow(g, (P - 1) // N, P)
    powtab = np.empty(N, dtype=np.int64)                 # powtab[m] = zJ^m
    cur = 1
    for m in range(N):
        powtab[m] = cur; cur = (cur * zJ) % P
    m_arange = np.arange(N, dtype=np.int64)
    fval = np.zeros(N, dtype=np.int64)
    for ci, j in zip(c, exps):
        if ci:
            idx = (m_arange * j) % N                       # (z_J^m)^j = z_J^{mj mod 2^J}
            fval = (fval + ci * powtab[idx]) % P
    return np.exp(2j * math.pi * fval / P)                 # phi_J[m]


def descent(J, Jmin, exps, c):
    phiJ = phi_top(J, exps, c)
    rows = []
    prev_max = None
    for j in range(J, Jmin - 1, -1):
        step = 1 << (J - j)
        phij = phiJ[::step]                                # samples over G_j = <z_J^{2^{J-j}}>
        Nj = len(phij)
        hat = np.fft.fft(phij)
        mabs = np.abs(hat)
        mx = float(mabs.max())
        # A/B split (butterfly): even/odd subsamples of phi_j -> G_{j-1}
        cancel = None
        if Nj >= 2:
            A = np.fft.fft(phij[0::2]); B = np.fft.fft(phij[1::2])
            # phihat_j(t) = A_{t mod Nj/2} + w^t B_{t mod Nj/2}; measure |phihat|/(|A|+|B|) at argmax
            tstar = int(mabs.argmax()); h = Nj // 2
            num = abs(hat[tstar]); den = abs(A[tstar % h]) + abs(B[tstar % h])
            cancel = num / den if den > 0 else float('nan')
        rho = (prev_max / mx) if (prev_max is not None) else float('nan')  # ratio to the NEXT-HIGHER level
        rows.append((j, Nj, mx, mx / math.sqrt(Nj), math.log(mx) / math.log(Nj) if mx > 1 else 0.0, rho, cancel))
        prev_max = mx
    return rows


def main():
    J, Jmin = 18, 9
    exps = [j for j in range(1, 512) if j % 2 == 1][:128]   # 128 odd exps in [1,255] (no wrap for j>=8)
    rng = np.random.default_rng(2)
    print(f"# Dyadic descent up the 2-power tower G_j=mu_{{2^j}} subset F_p (p=2^31-2^24+1). exps: 128 odd in [1,255].")
    print(f"# rho_j = max|phihat_{{G_j}}| / max|phihat_{{G_{{j-1}}}}| (UP the tower). PROOF viable iff rho <= 2^0.81=1.75.")
    print(f"# cancel = |phihat|/(|A|+|B|) at argmax (butterfly A,B over G_{{j-1}}); <1 => cancellation helps descent.")
    def show(label, c):
        rows = descent(J, Jmin, exps, c)
        print(f"\n  [{label}]  j: (Nj)  max|phihat|  /sqrtNj  exp=log_Nj  rho(up)  cancel")
        # print low->high so rho reads as the up-step ratio into level j
        for (j, Nj, mx, r, e, rho, canc) in reversed(rows):
            rr = f"{rho:.3f}" if not math.isnan(rho) else "  -  "
            cc = f"{canc:.3f}" if (canc is not None and not math.isnan(canc)) else " - "
            print(f"      j={j:<3}(2^{j})  {mx:9.1f}  {r:6.2f}   {e:.3f}    {rr}    {cc}")
        rhos = [rho for (_,_,_,_,_,rho,_) in rows if not math.isnan(rho)]
        if rhos:
            print(f"      => rho(up) range [{min(rhos):.3f}, {max(rhos):.3f}], mean {np.mean(rhos):.3f}  "
                  f"(2^0.81={2**0.81:.3f}; PROOF-viable if <=1.75, mild-accumulation if ~2)")
    c = rng.integers(1, P, size=len(exps), dtype=np.int64)
    show("dense", c)
    cm = np.zeros(len(exps), dtype=np.int64); cm[0] = 1                  # monomial x^1
    show("monomial x^1", cm)
    # adversarial: maximize max|phihat_{G_J}| by coordinate ascent (a few restarts)
    def obj(cc):
        return float(np.abs(np.fft.fft(phi_top(J, exps, cc))).max())
    best = rng.integers(1, P, size=len(exps), dtype=np.int64); cur = obj(best)
    for t in range(len(exps)):
        cand = rng.integers(0, P, size=24, dtype=np.int64); bv, bo = best[t], cur
        for v in cand:
            best[t] = v; o = obj(best)
            if o > bo: bo, bv = o, v
        best[t] = bv; cur = bo
    show("adversarial", best)
    print("\n# VERDICT: if rho(up) <= ~1.75 across the tower for ALL c (incl adversarial), the dyadic-descent")
    print("#   inverse theorem is a viable PROOF route for max|phihat|<=n^0.81 => the whole barrier.")


if __name__ == "__main__":
    raise SystemExit(main())
