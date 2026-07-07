#!/usr/bin/env python3
"""VERIFY the frozen-fiber counterexample to the peak-coherence estimate, at full deployed scale.

Model round: f_lambda(x) = lambda * x (x^D - 1)(x^D - alpha), D = 2^15, alpha = z20^D (order 32),
exponents {1, D+1=32769, 2D+1=65537} all odd <= w -- ADMISSIBLE 3-term c. Claims to verify:
 (1) On H = G_19 (level j=20 butterfly, N' = 2^19): f(y) = lambda*y*(q-1)(q-alpha) with q = y^D in mu_16;
     BOTH f(y) and f(z20*y) vanish EXACTLY on the fiber q=1 (size D = 2^15) -- common frozen fiber.
 (2) There exists lambda with |A_0|, |B_0| >= D - sqrt(450 D) > N'^0.76 = 22233, SAME frequency s*=0,
     and coherence Re(A_0 conj(B_0)) > 0.53 max(|A_0|,|B_0|)^2  -- REFUTING the proposed estimate.
 (3) Level-20 full spectrum: max_t|phihat_{G_20}| ~ 2D = 2^16 = |G_20|^{0.80} -- under |G_20|^{0.81} barely.
 (4) TOP level G_21: f vanishes on TWO fibers (q=1 and q=alpha, q now in mu_64) -- frozen mass 2^16 ~ deg f;
     max_t|phihat_{G_21}| ~ n^{0.762} < goal n^{0.81} (the GOAL still survives; degree budget caps it).
"""
from __future__ import annotations
import math
import numpy as np
import sympy

P = 2**31 - 2**24 + 1
K = 21
N = 1 << K
W = 67471
D = 1 << 15


def main():
    g0 = int(sympy.primitive_root(P))
    z21 = pow(g0, (P - 1) // N, P)                     # generator of G_21
    powtab = np.empty(N, dtype=np.int64)
    cur = 1
    for m in range(N):
        powtab[m] = cur; cur = (cur * z21) % P
    alpha = powtab[2 * D]                              # z20^D = z21^{2D}, order 32
    assert pow(int(alpha), 32, P) == 1 and pow(int(alpha), 16, P) != 1, "alpha must have order exactly 32"
    print(f"# f = lambda*x(x^D-1)(x^D-alpha), D=2^15, alpha=z21^{2*D} (order 32). exps {{1,{D+1},{2*D+1}}} all odd <= w={W}: "
          f"{all(e % 2 == 1 and e <= W for e in [1, D+1, 2*D+1])}")

    m = np.arange(N, dtype=np.int64)
    def fvals(lam):
        c1 = (lam * alpha) % P; cD1 = (-lam * (1 + alpha)) % P; c2D1 = lam % P
        return (c1 * powtab[m % N] + cD1 * powtab[((D + 1) * m) % N] + c2D1 * powtab[((2 * D + 1) * m) % N]) % P

    # (1) frozen-fiber counts on H=G_19 (indices m=0 mod 4) and coset z20*H (m=2 mod 4)
    lam0 = 1
    fv = fvals(lam0)
    H_idx = np.arange(0, N, 4); C_idx = np.arange(2, N, 4)          # G_19 and z20*G_19 inside G_21's indexing
    zH = int((fv[H_idx] == 0).sum()); zC = int((fv[C_idx] == 0).sum())
    print(f"(1) zeros of f on H=G_19: {zH} (claim {D});  zeros on coset z20*H: {zC} (claim {D})")

    # (2) lambda search: A_0, B_0 and coherence at s*=0
    Np = 1 << 19
    thr076 = Np ** 0.76
    rng = np.random.default_rng(5)
    best = None
    for lam in [int(x) for x in rng.integers(1, P, size=48)]:
        fv = fvals(lam)
        A0 = np.exp(2j * math.pi * fv[H_idx] / P).sum()
        B0 = np.exp(2j * math.pi * fv[C_idx] / P).sum()
        coh = (A0 * B0.conjugate()).real / max(abs(A0), abs(B0)) ** 2
        ok = abs(A0) > thr076 and abs(B0) > thr076
        score = coh if ok else -1
        if best is None or score > best[0]:
            best = (score, lam, A0, B0, coh, ok)
    _, lam, A0, B0, coh, ok = best
    print(f"(2) best lambda: |A_0|={abs(A0):.0f}, |B_0|={abs(B0):.0f}  (both > N'^0.76={thr076:.0f}? {ok})")
    print(f"    coherence Re(A0 conj B0)/max^2 = {coh:.3f}  (> 0.53? {coh > 0.53})  => estimate REFUTED? {ok and coh > 0.53}")

    # (3) level-20 full spectrum
    fv = fvals(lam)
    G20_idx = np.arange(0, N, 2)
    phi20 = np.exp(2j * math.pi * fv[G20_idx] / P)
    mx20 = float(np.abs(np.fft.fft(phi20)).max())
    print(f"(3) max|phihat_G20| = {mx20:.0f} = |G20|^{math.log(mx20)/math.log(1<<20):.4f}  "
          f"(|G20|^0.81 = {(1<<20)**0.81:.0f}; under? {mx20 < (1<<20)**0.81})")

    # (4) top level G_21: frozen mass (two fibers) + spectrum vs goal
    zTop = int((fv == 0).sum())
    phi21 = np.exp(2j * math.pi * fv / P)
    mx21 = float(np.abs(np.fft.fft(phi21)).max())
    goal = N ** 0.81
    print(f"(4) zeros of f on G_21: {zTop} (claim 2^16={1<<16});  max|phihat_G21| = {mx21:.0f} = n^{math.log(mx21)/math.log(N):.4f}")
    print(f"    goal n^0.81 = {goal:.0f}; GOAL SURVIVES this family? {mx21 < goal}  (margin {goal/mx21:.2f}x)")


if __name__ == "__main__":
    raise SystemExit(main())
