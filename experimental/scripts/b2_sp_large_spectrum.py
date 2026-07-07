#!/usr/bin/env python3
"""SP large-spectrum probe: is the large spectrum of pi_odd(c) THIN (SP plausible)?

pi_odd(c) = sum_{a in mu_n} e_p(sum_{j in Jodd} c_j a^j),  Jodd = first w_odd odd exponents.
By T5 the 2s-th spectral moment is p^{w_odd} J_s <= p^{w_odd}(2s-1)!! n^s, but T14 shows the
moment method overshoots the SP target Sum_{c!=0}|pi_odd|^s <= n^{O(1)} n^s by n^{~19000} at
deployed scale -- so SP (if true) needs the LARGE SPECTRUM {c: |pi_odd(c)| ~ n} to be genuinely
THIN, thinner than moments force. This probe measures, by EXACT enumeration of c in F_p^{w_odd}:
  - max_{c!=0} |pi_odd(c)| / n           (how close to the c=0 spike n does any c!=0 get)
  - Lcount(theta) = #{c!=0 : |pi_odd(c)| >= theta*n}  for theta=0.5,0.7,0.9
and tracks how Lcount scales with p at FIXED (n, w_odd). If Lcount stays ~poly(n) as p grows,
SP is supported; if it grows like p^{const}, SP is in trouble. Also reports the ratio
(true Sum_{c!=0}|pi_odd|^s) / (SP target n^3 * n^s) for small s.
"""
from __future__ import annotations
import argparse, math
import numpy as np
import sympy


def mu_n(p, n):
    g = int(sympy.primitive_root(p))
    z = pow(g, (p - 1) // n, p)
    return np.array([pow(z, k, p) for k in range(n)], dtype=np.int64)


def odd_exps(n, w_odd):
    """first w_odd odd exponents coprime to n (=all odds when n=2^k)."""
    out, j = [], 1
    while len(out) < w_odd:
        if j % 2 == 1 and math.gcd(j, n) == 1:
            out.append(j)
        j += 1
    return out


def probe(p, n, w_odd, s_list, chunk=200000):
    pts = mu_n(p, n)
    J = odd_exps(n, w_odd)
    A = np.empty((w_odd, n), dtype=np.int64)     # A[t] = a^{J[t]} over a in mu_n
    for t, j in enumerate(J):
        A[t] = np.array([pow(int(a), j, p) for a in pts], dtype=np.int64)
    tp = 2 * math.pi / p
    # enumerate all c in F_p^{w_odd} (odometer), chunked
    total = p ** w_odd
    maxabs = 0.0
    Lcnt = {0.5: 0, 0.7: 0, 0.9: 0}
    Ssum = {s: 0.0 for s in s_list}     # Sum_{c!=0} |pi|^s
    # iterate c as base-p integers 0..total-1  (w_odd small)
    idx0 = 0
    while idx0 < total:
        idx = np.arange(idx0, min(idx0 + chunk, total), dtype=np.int64)
        # decode base-p digits -> C shape (len,w_odd)
        C = np.empty((len(idx), w_odd), dtype=np.int64)
        tmp = idx.copy()
        for t in range(w_odd):
            C[:, t] = tmp % p
            tmp //= p
        ph = (C @ A) % p                          # (len, n)
        pin = np.abs(np.exp(1j * tp * ph).sum(axis=1))   # (len,)
        nz = ~(C == 0).all(axis=1)                # c != 0 mask
        pinz = pin[nz]
        if pinz.size:
            maxabs = max(maxabs, float(pinz.max()))
            for th in Lcnt:
                Lcnt[th] += int((pinz >= th * n).sum())
            for s in s_list:
                Ssum[s] += float((pinz ** s).sum())
        idx0 += chunk
    return J, maxabs, Lcnt, Ssum, total


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--w_odd", type=int, default=2)
    ap.add_argument("--primes", default="", help="comma list of primes p (n|p-1); default auto-sweep")
    ap.add_argument("--nprimes", type=int, default=6)
    ap.add_argument("--s_list", default="2,4,8")
    a = ap.parse_args(argv)
    n, w_odd = a.n, a.w_odd
    s_list = [int(x) for x in a.s_list.split(",")]
    if a.primes:
        primes = [int(x) for x in a.primes.split(",")]
    else:
        primes, k = [], 1
        while len(primes) < a.nprimes:
            q = k * n + 1
            if sympy.isprime(q):
                primes.append(q)
            k += 1
    print(f"# SP large-spectrum probe: n={n}, w_odd={w_odd}, |mu_n|=n, exact enum of c in F_p^{w_odd}")
    print(f"# columns: p  gamma=log_p(n)  max|pi_odd|/n  L(.5) L(.7) L(.9)  [#c!=0]  "
          f"then per-s ratio true_Sum/(n^3 n^s)")
    for p in primes:
        J, maxabs, Lcnt, Ssum, total = probe(p, n, w_odd, s_list)
        gamma = math.log(n) / math.log(p)
        ratios = []
        for s in s_list:
            target = (n ** 3) * (n ** s)
            ratios.append(f"s={s}:{Ssum[s]/target:.2e}")
        print(f"  p={p:<7} g={gamma:.3f}  max/n={maxabs/n:.3f}  "
              f"L={Lcnt[0.5]:>4} {Lcnt[0.7]:>4} {Lcnt[0.9]:>4}  [{total-1}]  " + "  ".join(ratios))
    print(f"# exps J={J}")
    print("# SP plausible IFF L(theta) stays ~poly(n) (NOT growing ~p) AND true_Sum/(n^3 n^s) <= 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
