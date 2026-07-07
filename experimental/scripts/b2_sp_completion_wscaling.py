#!/usr/bin/env python3
"""DECISIVE: does max_psi |S(psi,c)| / sqrt(p) grow with w?  + verify the model's subgroup autocorrelation.

Part A (M1 test).  S(psi,c) = sum_{x in F_p^*} psi(x) e_p(f_c(x)),  psi in H^perp (order | m'=(p-1)/n).
  If max_psi |S| / sqrt(p) stays O(1) as w grows => M1 (odd-support degenerates the sheaf; completed sums ~sqrt p)
     => |pi_odd| <= (1/m') sum_psi |S| <= C sqrt p PROVES the sup bound directly (completion WORKS, model
        obstruction 6 too pessimistic).
  If it grows ~ sqrt(w) or ~ w => completion hits the degree wall (model obstruction 6 stands).
  Track max|S|/sqrt(p) against 1, sqrt(w), w as w increases at the deployed ratio w/n ~ 0.03.

Part B (model route 7, subgroup-internal autocorrelation -- RESONANCE-STABLE).
  T_a^G(c) = sum_{y in G} e_p(f_c(ay) - f_c(y)),  a in G   [sum over the SUBGROUP G, not F_p^*].
  Identity: |pi_odd(c)|^2 = sum_{a in G} T_a^G(c).  Cauchy: |pi_odd|^4 <= n * sum_{a in G} |T_a^G|^2.
  Target: sum_{a in G} |T_a^G(c)|^2 <= n^{2.62} (== |pi|<=n^0.905).  Verify identity + resonance-stability
  (dense c AND resonant monomial x^{j0}); report sum|T_a^G|^2 / (n p) and / n^2.62.
"""
from __future__ import annotations
import math
import numpy as np
import sympy


def index_table(p, g):
    ind = np.zeros(p, dtype=np.int64)
    cur = 1
    for e in range(p - 1):
        ind[cur] = e
        cur = (cur * g) % p
    return ind


def odd_exps(n, w_odd):
    return [j for j in range(1, 3 * w_odd + 4) if j % 2 == 1 and math.gcd(j, n) == 1][:w_odd]


def fc_on(Xmod, c, exps, p):
    acc = np.zeros(len(Xmod), dtype=np.int64)
    for cj, j in zip(c, exps):
        if cj:
            acc = (acc + cj * np.power(Xmod % p, j, dtype=object)) % p
    return np.array([int(v) for v in acc], dtype=np.int64)


def partA(n, p, w_odd, rng):
    g = int(sympy.primitive_root(p)); ind = index_table(p, g)
    exps = odd_exps(n, w_odd); w = 2 * w_odd
    X = np.arange(1, p, dtype=np.int64); indX = ind[X]
    mprime = (p - 1) // n; tpm = 2 * math.pi / (p - 1); tp = 2 * math.pi / p
    sp = math.sqrt(p)
    maxrats = []
    for r in range(3):
        c = rng.integers(1, p, size=w_odd, dtype=np.int64)
        ef = np.exp(1j * tp * fc_on(X, c, exps, p))
        mx = 0.0
        for jj in range(mprime):
            psi = np.exp(1j * tpm * ((n * jj) * indX % (p - 1)))
            mx = max(mx, abs((psi * ef).sum()))
        maxrats.append(mx / sp)
    mr = max(maxrats)
    print(f"  n={n:<5} p={p:<7} w={w:<4} w_odd={w_odd:<3} m'={mprime:<4} | max_psi|S|/sqrtp = {mr:5.2f}  "
          f"vs  sqrt(w)={math.sqrt(w):.2f}  w={w}   -> {'O(1)~M1' if mr < 2*math.sqrt(w) and mr < 6 else 'GROWS'}")
    return w, mr


def partB(n, p, w_odd, rng):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    G = np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)
    exps = odd_exps(n, w_odd); tp = 2 * math.pi / p; sp = math.sqrt(p)
    def autocorr(c):
        fG = fc_on(G, c, exps, p)                       # f_c on G
        eG = np.exp(1j * tp * fG)
        pi = eG.sum()
        # T_a^G = sum_{y in G} e_p(f_c(ay)-f_c(y)); a ranges over G
        s2 = 0.0; sumT = 0.0 + 0j
        for a in G:
            aG = (int(a) * G) % p
            faG = fc_on(aG, c, exps, p)
            Ta = (np.exp(1j * tp * faG) * np.conj(eG)).sum()
            sumT += Ta; s2 += abs(Ta) ** 2
        return abs(pi), sumT.real, s2
    thr = n ** 2.62
    for lbl, c in [("dense", rng.integers(1, p, size=w_odd, dtype=np.int64)),
                   ("monomial", None)]:
        if c is None:
            j0 = max(exps, key=lambda j: math.gcd(j, p - 1))
            c = np.zeros(w_odd, dtype=np.int64); c[exps.index(j0)] = 1; lbl = f"monomial x^{j0}"
        pim, sumT, s2 = autocorr(c)
        id_ok = abs(pim ** 2 - sumT) < 1e-6 * max(1, pim ** 2)
        print(f"    [{lbl:<14}] |pi|^2={pim**2:12.1f} =Sum_a T_a? {id_ok}  | Sum|T_a^G|^2/(np)={s2/(n*p):5.2f}  "
              f"/n^2.62={s2/thr:6.3f}  RMS/sqrtp={math.sqrt(s2/n)/sp:.2f}  (|pi|/sqrtp={pim/sp:.2f})")


def main():
    print("# PART A: w-scaling of max_psi|S(psi,c)|/sqrt(p) -- does completion beat the degree wall?")
    rng = np.random.default_rng(4)
    pts = []
    for n, p, w_odd in [(1024, 12289, 8), (1024, 40961, 16), (2048, 12289, 16),
                        (2048, 65537, 33), (4096, 65537, 33), (4096, 274177, 64)]:
        if (p - 1) % n or not sympy.isprime(p):
            continue
        pts.append(partA(n, p, w_odd, rng))
    print("  => if max|S|/sqrtp roughly CONSTANT as w rises 16->128, M1 holds and completion PROVES |pi|<=C sqrt p.")
    print("\n# PART B: model route 7 -- subgroup-internal autocorrelation Sum_{a in G}|T_a^G|^2 (resonance-stable)")
    for n, p, w_odd in [(512, 7681, 8), (1024, 12289, 16), (2048, 65537, 33)]:
        if (p - 1) % n or not sympy.isprime(p):
            continue
        print(f"  n={n} p={p} (n^2.62={n**2.62:.3e}, np={n*p:.3e}):")
        partB(n, p, w_odd, rng)
    print("# identity |pi|^2=Sum_a T_a^G must hold; Sum|T_a^G|^2/(np)~O(1) incl. monomial => resonance-stable route.")


if __name__ == "__main__":
    main()
