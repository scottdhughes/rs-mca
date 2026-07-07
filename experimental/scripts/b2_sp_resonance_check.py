#!/usr/bin/env python3
"""VERIFY the subagent's resonant-monomial counterexample to round (d)'s S2off <= O(np).

Claim to check (reviewer != generator; this overturns a banked claim):
  (A) For c = e_{j0} (f_c = x^{j0}, j0 odd in J), S2off(c) = (d-1) n p (1+o(1)), d = gcd(j0, p-1).
      => S2off is NOT O(np) with absolute constant; worst-case K ~ d_max = largest odd divisor of
         m'=(p-1)/n that is <= w. (Dense coordinate-ascent MISSES these sparse optima.)
  (B) BUT the object that matters, |pi(c)| = |sum_{a in mu_n} e_p(f_c(a))|, is resonance-STABLE:
      for c=e_{j0}, a->a^{j0} permutes mu_n (j0 odd, gcd(j0,2^k)=1), so pi = subgroup Gauss period,
      |pi| <= ~sqrt(p) << n^0.9. So T15's sufficient condition max|pi|<=n^0.905 STILL holds; only the
      S2off PROXY is inflated (Cauchy-Schwarz loses sqrt(m') at resonances).
Also: deployed sanity -- m' = (p-1)/n and its odd part for the KoalaBear prime.
"""
from __future__ import annotations
import math
import numpy as np
import sympy


def mu_n(p, n):
    g = int(sympy.primitive_root(p))
    z = pow(g, (p - 1) // n, p)
    return np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)


def T_a_abs2_sum_offdiag(j0, mu, p):
    """S2off for f_c = x^{j0}: sum_{a in mu_n, a!=1} |sum_{y in F_p^*} e_p((a y)^{j0} - y^{j0})|^2."""
    Y = np.arange(1, p, dtype=np.int64)
    yj = np.power(Y, j0, dtype=object).astype(object) % p          # y^{j0}
    yj = np.array([int(v) for v in yj], dtype=np.int64)
    tp = 2 * math.pi / p
    eneg = np.exp(-1j * tp * yj)                                    # e_p(-y^{j0})
    s2 = 0.0
    for a in mu:
        a = int(a)
        ayj = (pow(a, j0, p) * yj) % p                             # (a y)^{j0} = a^{j0} y^{j0}
        Ta = (np.exp(1j * tp * ayj) * eneg).sum()
        if a != 1:
            s2 += abs(Ta) ** 2
    return s2


def pi_monomial(j0, mu, p):
    tp = 2 * math.pi / p
    aj = np.array([pow(int(a), j0, p) for a in mu], dtype=np.int64)
    return abs(np.exp(1j * tp * aj).sum())


def main():
    print("## (A)+(B) resonant monomial check: S2off/(np) = d-1 ?  and  |pi|/sqrt(p) = O(1) ?")
    print("#  n    p      m'      j0   d=gcd(j0,p-1)   S2off/(np)   (d-1)   |pi|/sqrt(p)   |pi|/n^0.9")
    configs = [
        (512, 7681), (512, 10753), (256, 7681), (128, 13441), (256, 7937),
    ]
    for n, p in configs:
        if (p - 1) % n != 0 or not sympy.isprime(p):
            print(f"  skip n={n} p={p}")
            continue
        mu = mu_n(p, n)
        mprime = (p - 1) // n
        w_odd = 8 if n <= 512 else 16
        J = [j for j in range(1, 3 * max(w_odd, 20)) if j % 2 == 1 and math.gcd(j, n) == 1][:max(w_odd, 16)]
        # pick the odd j in J maximizing gcd(j, p-1) (the resonance)
        j0 = max(J, key=lambda j: math.gcd(j, p - 1))
        d = math.gcd(j0, p - 1)
        s2 = T_a_abs2_sum_offdiag(j0, mu, p)
        pim = pi_monomial(j0, mu, p)
        print(f"  {n:<4} {p:<6} {mprime:<6}  {j0:<4} {d:<13}  {s2/(n*p):>9.3f}   {d-1:<5}  "
              f"{pim/math.sqrt(p):>10.3f}    {pim/(n**0.9):>8.3f}")
    # deployed sanity
    P = 2**31 - 2**24 + 1
    n = 2**21
    print(f"\n## deployed KoalaBear: p=2^31-2^24+1={P}, p-1 factors={sympy.factorint(P-1)}")
    mprime = (P - 1) // n
    oddpart = mprime
    while oddpart % 2 == 0:
        oddpart //= 2
    print(f"   n=2^21, m'=(p-1)/n={mprime}={sympy.factorint(mprime)}, ODD part of m' = {oddpart}")
    print(f"   => d_max = {oddpart} (127 <= w=67471, 127|p-1) => S2off worst-case ~ {oddpart-1} np, K NOT O(1)")
    # propagate sharp S2off through Cauchy-Schwarz: M <= sqrt(p + n sqrt(K p)), K=d_max
    K = oddpart
    M = math.sqrt(P + n * math.sqrt(K * P))
    print(f"   sharp-S2off => M=|pi| <= sqrt(p + n sqrt({K} p)) = 2^{math.log2(M):.2f} = n^{math.log(M)/math.log(n):.3f}")
    print(f"   T15 threshold n^0.905 = 2^{0.905*21:.2f};  route gives n^{math.log(M)/math.log(n):.3f} => "
          f"{'CLOSES' if math.log(M)/math.log(n) <= 0.905 else 'FAILS (lossy) -- need direct |pi| bound'}")


if __name__ == "__main__":
    main()
