#!/usr/bin/env python3
"""Attack (1): the resonance-stable subgroup 4th moment  Sum_{a in G} |T_a^G(c)|^2 <= n^{2.62}.

phi(z^k) = e_p(f_c(z^k)),  z = generator of G=mu_n, so phi is a length-n sequence on Z/n.
Autocorrelation T_a^G = sum_y phi(ay) conj(phi(y))  => Wiener-Khinchin: three EXACT equal forms
  (F1) Sum_{a in G}|T_a^G|^2 = (1/n) Sum_{t} |phihat_t|^4          (phihat = DFT of phi over Z/n)
  (F2) = Sum_{x1 x2 = x3 x4 in G} e_p(f(x1)+f(x2)-f(x3)-f(x4))     (multiplicative energy weighted)
  (F3) = Sum_{u in G} |R_u|^2,  R_u = sum_{x in G} e_p(f(x)+f(u/x)) = (phi *conv phi)(u)
This script (a) VERIFIES F1==direct==F2(small n)==F3 exactly; (b) measures the target ratio
Sum|T_a^G|^2 / n^{2.62}; (c) tests the SUB-ROUTE 'max_u|R_u| <= n^{0.81} => target' by measuring
max_u|R_u| and its n-exponent as n grows (dense + resonant-monomial + coordinate-ascent-adversarial c);
(d) reports the G-spectrum |phihat| profile (flat vs peaky) and the diagonal/off-diagonal split of F2.
"""
from __future__ import annotations
import math
import numpy as np
import sympy


def Gseq(p, n):
    g = int(sympy.primitive_root(p)); z = pow(g, (p - 1) // n, p)
    return np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)   # G[k] = z^k


def odd_exps(n, w_odd):
    return [j for j in range(1, 3 * w_odd + 4) if j % 2 == 1 and math.gcd(j, n) == 1][:w_odd]


def phi_seq(Gk, c, exps, p):
    acc = np.zeros(len(Gk), dtype=np.int64)
    for cj, j in zip(c, exps):
        if cj:
            acc = (acc + cj * np.power(Gk % p, j, dtype=object)) % p
    fk = np.array([int(v) for v in acc], dtype=np.int64)
    return np.exp(2j * math.pi * fk / p)               # phi(z^k)


def direct_4moment(Gk, c, exps, p):
    """Sum_{a in G}|T_a^G|^2 directly, T_a^G = sum_{y in G} e_p(f(ay)-f(y))."""
    tp = 2 * math.pi / p
    fG = np.zeros(len(Gk), dtype=np.int64)
    acc = np.zeros(len(Gk), dtype=np.int64)
    for cj, j in zip(c, exps):
        if cj:
            acc = (acc + cj * np.power(Gk % p, j, dtype=object)) % p
    fG = np.array([int(v) for v in acc], dtype=np.int64)
    eG = np.exp(1j * tp * fG)
    s2 = 0.0
    for a in Gk:
        aG = (int(a) * Gk) % p
        acc2 = np.zeros(len(Gk), dtype=np.int64)
        for cj, j in zip(c, exps):
            if cj:
                acc2 = (acc2 + cj * np.power(aG % p, j, dtype=object)) % p
        faG = np.array([int(v) for v in acc2], dtype=np.int64)
        Ta = (np.exp(1j * tp * faG) * np.conj(eG)).sum()
        s2 += abs(Ta) ** 2
    return s2


def mult_energy_direct(Gk, c, exps, p):
    """F2 brute (O(n^3)) -- small n only. Uses index map for xy/z."""
    n = len(Gk); tp = 2 * math.pi / p
    idx = {int(Gk[k]): k for k in range(n)}
    acc = np.zeros(n, dtype=np.int64)
    for cj, j in zip(c, exps):
        if cj:
            acc = (acc + cj * np.power(Gk % p, j, dtype=object)) % p
    fk = np.array([int(v) for v in acc], dtype=np.int64)   # f(z^k)
    e = np.exp(1j * tp * fk)
    tot = 0.0 + 0j
    Ginv = [pow(int(Gk[k]), p - 2, p) for k in range(n)]
    for i in range(n):
        for j2 in range(n):
            xy = (int(Gk[i]) * int(Gk[j2])) % p
            for k in range(n):
                x4 = (xy * Ginv[k]) % p
                l = idx[x4]
                tot += e[i] * e[j2] * np.conj(e[k]) * np.conj(e[l])
    return tot


def probe(n, p, w_odd, rng, do_brute=False):
    Gk = Gseq(p, n); exps = odd_exps(n, w_odd)
    def stats(c, label):
        phi = phi_seq(Gk, c, exps, p)
        phihat = np.fft.fft(phi)                          # DFT over Z/n
        F1 = (np.abs(phihat) ** 4).sum() / n
        R = np.fft.ifft(phihat * phihat)                  # self-convolution R_u = (phi*phi)(u) [numpy ifft has 1/n]
        F3 = (np.abs(R) ** 2).sum() * n                   # Parseval: Sum_u|R_u|^2 = n * mean|R|^2... = F1
        maxR = np.abs(R).max()
        diag = 2 * n * n - n                              # diagonal {x3,x4}={x1,x2}, all phase 1
        offdiag = F1 - diag
        thr = n ** 2.62
        line = (f"    [{label:<16}] Sum|T^G|^2={F1:11.1f} /n^2.62={F1/thr:6.3f} | diag=2n^2-n={diag} "
                f"offdiag={offdiag:+.1f} (/n^2.62={offdiag/thr:+.4f}) | max_u|R_u|={maxR:7.1f}=n^{math.log(maxR)/math.log(n):.3f}"
                f" (route<=n^0.81) F3==F1?{abs(F3-F1)<1e-4*max(1,F1)}")
        checks = ""
        if do_brute:
            direct = direct_4moment(Gk, c, exps, p)
            checks += f" F1==direct?{abs(F1-direct)<1e-5*max(1,F1)}"
            if n <= 130:
                F2 = mult_energy_direct(Gk, c, exps, p)
                checks += f" ==F2?{abs(F1-F2.real)<1e-4*max(1,F1) and abs(F2.imag)<1e-4*max(1,abs(F2))}"
        print(line + ("  [CHECK:" + checks + "]" if checks else ""))
        return maxR
    # dense, resonant monomial, and adversarial (coord ascent on |pi| then eval 4-moment)
    stats(rng.integers(1, p, size=w_odd, dtype=np.int64), "dense")
    j0 = max(exps, key=lambda j: math.gcd(j, p - 1))
    cm = np.zeros(w_odd, dtype=np.int64); cm[exps.index(j0)] = 1
    stats(cm, f"monomial x^{j0}")
    # coordinate ascent maximizing Sum|T^G|^2 itself (the real adversary for THIS object)
    best_c = rng.integers(1, p, size=w_odd, dtype=np.int64);
    def obj(c):
        ph = phi_seq(Gk, c, exps, p); pht = np.fft.fft(ph); return (np.abs(pht)**4).sum()/n
    cur = obj(best_c)
    for _ in range(2):
        for t in range(w_odd):
            cand = rng.integers(0, p, size=64, dtype=np.int64); bv, bo = best_c[t], cur
            for v in cand:
                best_c[t] = v; o = obj(best_c)
                if o > bo: bo, bv = o, v
            best_c[t] = bv; cur = bo
    stats(best_c, "adversarial(4mom)")


def main():
    rng = np.random.default_rng(7)
    print("# Attack (1): subgroup 4th moment Sum_{a in G}|T_a^G|^2 <= n^2.62 (=8.17 np). Three FFT forms.")
    print("# identity checks on small n; then target ratio + max_u|R_u| exponent (sub-route needs <= n^0.81).")
    for n, p, w_odd, brute in [(128, 13441, 8, True), (512, 7681, 8, False),
                               (1024, 12289, 16, False), (2048, 65537, 33, False), (4096, 274177, 64, False)]:
        if (p - 1) % n or not sympy.isprime(p):
            continue
        print(f"\n### n={n} p={p} gamma={math.log(n)/math.log(p):.3f} (n^2.62={n**2.62:.2e})")
        probe(n, p, w_odd, rng, do_brute=brute)
    print("\n# If max_u|R_u| exponent stays <= 0.81 as n grows => the sup-of-R route proves the target.")
    print("# (max|R_u|<=n^0.81 => Sum_u|R_u|^2 <= n*(n^0.81)^2 = n^2.62.)")


if __name__ == "__main__":
    main()
