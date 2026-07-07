#!/usr/bin/env python3
"""DECISIVE toy test: does the odd-evaluation GRS code have a RANDOM-LIKE Lee/cosine ledger?

Round-(n) stake: the random-code Cramer heuristic says N(rho) ~ p^r e^{-m I_cos(rho)} EXCEEDS the SP budget
e^{(m/2)ln(1/rho)} for rho in (0.303, 0.642) at deployed params => SP FALSE if the code is random-like.
This script EXACTLY ENUMERATES the code at toy scale: all c in F_p^{w_odd}, pi(c) = sum_{x in mu_n} e_p(f_c(x)),
ledger fraction F_code(rho) = #{c: |pi(c)| >= rho n}/p^{w_odd}; compares to the random model
F_rand(rho) = P(|avg_m of iid uniform-phase cos| >= rho) (Monte Carlo), m = n/2 (pairing +-x).
MATCH => the code is Lee-random-like => the SP-false warning is EMPIRICALLY SUPPORTED.
CODE << RANDOM => algebraic thinning exists => SP hope survives.
"""
from __future__ import annotations
import math
import numpy as np
import sympy


def ledger(n, p, w_odd, rhos):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    pts = np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)
    exps = [j for j in range(1, 4 * w_odd) if j % 2 == 1][:w_odd]
    POW = np.stack([np.array([pow(int(x), j, p) for x in pts], dtype=np.int64) for j in exps])
    tot = p ** w_odd
    counts = np.zeros(len(rhos), dtype=np.int64)
    chunk = 200000
    idx0 = 0
    tp = 2 * math.pi / p
    while idx0 < tot:
        idx = np.arange(idx0, min(idx0 + chunk, tot), dtype=np.int64)
        C = np.empty((len(idx), w_odd), dtype=np.int64)
        t = idx.copy()
        for k in range(w_odd):
            C[:, k] = t % p; t //= p
        ph = (C @ POW) % p
        pin = np.abs(np.exp(1j * tp * ph).sum(axis=1)) / n
        nz = ~(C == 0).all(axis=1)
        for i, r_ in enumerate(rhos):
            counts[i] += int((pin[nz] >= r_).sum())
        idx0 += chunk
    return counts, tot - 1


def random_model(m, rhos, samples=4_000_000, seed=3):
    rng = np.random.default_rng(seed)
    out = np.zeros(len(rhos))
    B = 500000
    done = 0
    while done < samples:
        b = min(B, samples - done)
        th = rng.uniform(0, 2 * math.pi, size=(b, m))
        avg = np.abs(np.cos(th).sum(axis=1)) / m
        for i, r_ in enumerate(rhos):
            out[i] += (avg >= r_).sum()
        done += b
    return out / samples


def main():
    rhos = [0.3, 0.4, 0.5, 0.6, 0.7]
    print("# CODE vs RANDOM Lee ledger (exact code enumeration vs MC random model). fractions log10.")
    for n, p, w_odd in [(16, 97, 2), (32, 97, 3), (16, 257, 2)]:
        if (p - 1) % n:
            continue
        cnt, tot = ledger(n, p, w_odd, rhos)
        fr = random_model(n // 2, rhos)
        print(f"\n  n={n} p={p} w_odd={w_odd}  (|code|={tot:,}, m={n//2})")
        print(f"    rho      F_code        F_random      ratio code/random")
        for i, r_ in enumerate(rhos):
            fc = cnt[i] / tot
            fr_ = fr[i]
            ratio = fc / fr_ if fr_ > 0 else float('nan')
            print(f"    {r_:.1f}   {fc:11.3e}   {fr_:11.3e}      {ratio:8.3f}")
    print("\n# ratio ~ 1 across rho => code is Lee-random-like => random-code Cramer heuristic applies at deployed")
    print("#   scale => SP is HEURISTICALLY FALSE in (0.303, 0.642). ratio << 1 => algebraic thinning, SP hope.")


if __name__ == "__main__":
    raise SystemExit(main())
