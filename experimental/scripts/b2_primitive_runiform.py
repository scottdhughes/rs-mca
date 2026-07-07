#!/usr/bin/env python3
"""PRIMITIVE r-uniformity across gamma = log_p |mu_n|: does it survive at small gamma (Mersenne 0.34)?

Tests the CORRECTED lemma (odd-frequency / primitive part, = the `extras` object after coset-union
peel): max over c supported on ODD frequencies j (coprime to n=2^k, where x^j permutes mu_n) of
|pi(c)| = |sum_{a in mu_n} e_p(sum_{j odd} c_j a^j)|, as the number of odd frequencies r grows.
If max|pi|/sqrt(n) stays bounded uniformly in r ACROSS gamma, the primitive lemma is robust (not a
large-gamma artifact). Also reports the exact single-odd-monomial worst case.
"""
from __future__ import annotations
import argparse, math
import numpy as np
import sympy


def find_prime(n, gamma, tries=200000):
    """least prime p == 1 mod n with log_n(p) ~ 1/gamma (=> log_p(n) ~ gamma)."""
    target = n ** (1.0 / gamma)
    k0 = max(1, int(round((target - 1) / n)))
    for dk in range(tries):
        for k in ((k0 + dk), (k0 - dk)):
            if k < 1:
                continue
            p = k * n + 1
            if sympy.isprime(p):
                return p
    raise RuntimeError("no prime found")


def mu_n(p, n):
    g = int(sympy.primitive_root(p))
    z = pow(g, (p - 1) // n, p)
    return np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)


def primitive_probe(p, n, rmax, samples, seed=7):
    pts = mu_n(p, n)
    tp = 2 * math.pi / p
    oddj = [j for j in range(1, rmax * 3) if j % 2 == 1][:rmax]   # first rmax odd frequencies
    POW = np.empty((len(oddj), n), dtype=np.int64)
    for i, j in enumerate(oddj):
        POW[i] = np.array([pow(int(a), j, p) for a in pts], dtype=np.int64)
    tp_ = tp
    # single odd-monomial worst case (exact over the odd j sampled)
    smax = max(abs(np.exp(1j * tp_ * POW[i]).sum()) for i in range(len(oddj)))
    rng = np.random.default_rng(seed)
    rows = []
    for r in [x for x in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024] if x <= len(oddj)]:
        C = rng.integers(0, p, size=(samples, r), dtype=np.int64)
        C[(C == 0).all(axis=1)] = 1
        ph = (C @ POW[:r]) % p
        pin = np.abs(np.exp(1j * tp_ * ph).sum(axis=1))
        rows.append((r, pin.max() / math.sqrt(n)))
    return smax / math.sqrt(n), rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="0.34:1024,0.5:2048,0.68:4096,0.85:4096",
                    help="comma list of gamma:n")
    ap.add_argument("--rmax", type=int, default=512)
    ap.add_argument("--samples", type=int, default=300)
    a = ap.parse_args(argv)
    print(f"# PRIMITIVE (odd-freq) r-uniformity across gamma. samples={a.samples}")
    print(f"# max|pi|/sqrt(n): single-monomial (exact worst) then sampled over odd-support c as #freq grows")
    for cfg in a.configs.split(","):
        gt, n = cfg.split(":"); gt = float(gt); n = int(n)
        p = find_prime(n, gt)
        gamma = math.log(n) / math.log(p)
        smax, rows = primitive_probe(p, n, a.rmax, a.samples)
        tag = "> sqrt p" if gamma > 0.5 else "< sqrt p"
        print(f"\n  gamma~{gt} -> p={p}, n={n}, actual gamma={gamma:.3f} ({tag}); sqrt(n)={math.sqrt(n):.1f}")
        print(f"    single odd-monomial worst |pi|/sqrt(n) = {smax:.2f}")
        s = "    #odd-freq: " + "  ".join(f"r={r}:{v:.2f}" for r, v in rows)
        print(s)
    print("\n# bounded ~O(1)*sqrt(n) uniformly in r AND across gamma => primitive lemma robust.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
