#!/usr/bin/env python3
"""b2 / conj:Q primitive-core scaling: does #{primitive w-null blocks} <= n^3 as n grows?

Attack engine that BREAKS the 2^(n/2) MITM ceiling, so we reach deployed-shape large
power-of-2 n (deployed n = 2^21). Two exact ingredients:

  total_wnull(q,n,m,w) = #{ m-subsets M of mu_n : p_1(M)=...=p_w(M)=0 in F_q } ,
      computed by an EXACT dynamic program over the power-sum vector mod q
      (state = (#chosen, (p_1..p_w) mod q)); O(n * m * q^w) time, poly in n.

  extras (holmbuar's primitive core N_0, = "non-coset-union w-null", the b2/u2c object).
      For POWER-OF-TWO n, a w-null M with nontrivial stabilizer is mu_2-symmetric
      (odd moments auto-vanish, even moments descend), so by descent identity (D)
      of cap25_v13_qfin_rung_audit.md:
          structured(n,m,w) = total_wnull(n/2, m/2, floor(w/2))   (m even; else 0)
          extras(n,m,w)     = total_wnull(n,m,w) - structured(n,m,w).

Conjecture (deployed): extras <= n^3 at deployed depth. This measures the CROSSOVER
DEPTH w*(n) = min w with extras <= n^3, and its growth in n. Slow w*(n) growth =
supporting evidence; band depth itself (w~67471) stays unreachable.

Cross-checked at n=32 against the independent MITM in b2_dense_extras.py.
"""
from __future__ import annotations
import argparse, math
from collections import defaultdict


def _prime_factors(n):
    fs, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d); n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs


def primroot(q):
    facs = _prime_factors(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // p, q) != 1 for p in facs):
            return g
    raise ValueError(f"no primitive root mod {q}")


def mu_n(q, n):
    assert (q - 1) % n == 0, f"n={n} must divide q-1={q-1}"
    zeta = pow(primroot(q), (q - 1) // n, q)
    return [pow(zeta, k, q) for k in range(n)]


def total_wnull_np(q, n, m, w, pts):
    """Exact DP with numpy: state key = sum_h p_h * q^(h-1) in [0, q^w).
    Adding a point = a fixed index permutation (bijection); counts high->low.
    int64 (fits for n<=64); asserts no overflow."""
    import numpy as np
    size = q ** w
    radix = np.array([q ** h for h in range(w)], dtype=np.int64)
    idx = np.arange(size, dtype=np.int64)
    comps = np.stack([(idx // radix[h]) % q for h in range(w)])   # (w, size)
    dp = [np.zeros(size, dtype=np.int64) for _ in range(m + 1)]
    dp[0][0] = 1
    for x in pts:
        c = np.array([pow(int(x), h, q) for h in range(1, w + 1)], dtype=np.int64)
        perm = ((comps + c[:, None]) % q * radix[:, None]).sum(axis=0)   # bijection on [0,size)
        for count in range(m - 1, -1, -1):
            src = dp[count]
            if src.any():
                dp[count + 1][perm] += src
    assert dp[m].max() < (1 << 62), "int64 overflow risk; use object dtype for larger n"
    return int(dp[m][0])


def total_wnull(q, n, m, w, pts=None, backend="auto"):
    """Exact count of m-subsets of mu_n with p_1..p_w = 0 mod q.
    backend: 'np' (numpy dense DP, fast), 'py' (dict DP), 'auto' (np if importable)."""
    if m < 0 or m > n:
        return 0
    if pts is None:
        pts = mu_n(q, n)
    if backend in ("np", "auto"):
        try:
            return total_wnull_np(q, n, m, w, pts)
        except ImportError:
            if backend == "np":
                raise
    # precompute each point's (x, x^2, ..., x^w) mod q
    contrib = []
    for x in pts:
        v, xr = [], x
        for _ in range(w):
            v.append(xr); xr = xr * x % q
        contrib.append(tuple(v))
    zero = tuple([0] * w)
    dp = [defaultdict(int) for _ in range(m + 1)]
    dp[0][zero] = 1
    for ci in contrib:
        # iterate counts high->low so each point is used at most once
        for cnt in range(min(len(dp) - 2, m - 1), -1, -1):
            cur = dp[cnt]
            if not cur:
                continue
            nxt = dp[cnt + 1]
            for key, val in cur.items():
                nk = tuple((key[h] + ci[h]) % q for h in range(w))
                nxt[nk] += val
    return dp[m].get(zero, 0)


def extras_primitive(q, n, m, w, pts=None):
    """holmbuar primitive core via descent (power-of-two n)."""
    assert (n & (n - 1)) == 0, "descent identity here is for power-of-two n (deployed shape)"
    tot = total_wnull(q, n, m, w, pts)
    struct = total_wnull(q, n // 2, m // 2, w // 2) if (m % 2 == 0) else 0
    return tot, struct, tot - struct


def crossover_depth(q, n, rho_num, rho_den, wmax):
    """w*(n) = min w in [1,wmax] with extras <= n^3; report the profile."""
    pts = mu_n(q, n)
    K = rho_num * n // rho_den
    n3 = n ** 3
    profile, wstar = [], None
    for w in range(1, wmax + 1):
        if q <= w:
            break                       # Newton needs q > w
        m = K + w
        if m > n:
            break
        tot, struct, ex = extras_primitive(q, n, m, w, pts)
        log2_fiber = ((math.lgamma(n + 1) - math.lgamma(m + 1) - math.lgamma(n - m + 1)) / math.log(2)
                      - w * math.log2(q))
        profile.append({"w": w, "m": m, "total": tot, "struct": struct, "extras": ex,
                        "n^3": n3, "le_n3": ex <= n3, "log2_fiber": round(log2_fiber, 2)})
        if ex <= n3 and wstar is None:
            wstar = w
    return wstar, n3, profile


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--rho", default="1/2")
    ap.add_argument("--ns", default="16,32,64,128", help="comma list of power-of-2 n (n|q-1)")
    ap.add_argument("--wmax", type=int, default=6)
    ap.add_argument("--xcheck", action="store_true", help="cross-check n=32 vs MITM")
    args = ap.parse_args(argv)
    rn, rd = (int(x) for x in args.rho.split("/"))

    if args.xcheck:
        import importlib.util, pathlib
        p = pathlib.Path(__file__).with_name("b2_dense_extras.py")
        spec = importlib.util.spec_from_file_location("b2d", p)
        b2d = importlib.util.module_from_spec(spec); spec.loader.exec_module(b2d)
        q = args.q if (args.q - 1) % 32 == 0 else 97
        pts = mu_n(q, 32)
        for w in (1, 2, 3):
            m = 32 // 2 + w
            tot_dp = total_wnull(q, 32, m, w, pts)
            tot_mitm = b2d.count_wnull_mitm(b2d.mu_n(q, 32), q, 32, w, m)
            _, _, ex_dp = extras_primitive(q, 32, m, w, pts)
            ex_mitm = tot_mitm - b2d.count_wnull_structured(b2d.mu_n(q, 32), q, 32, w, m)
            ok = (tot_dp == tot_mitm) and (ex_dp == ex_mitm)
            print(f"[{'OK ' if ok else 'FAIL'}] xcheck q={q} n=32 w={w} m={m}: "
                  f"DP total={tot_dp} (MITM {tot_mitm}); descent extras={ex_dp} (MITM {ex_mitm})")
        print()

    ns = [int(x) for x in args.ns.split(",")]
    print(f"# q={args.q} rho={args.rho} : crossover depth w*(n) where primitive extras <= n^3")
    for n in ns:
        if (args.q - 1) % n:
            print(f"  n={n}: SKIP (n does not divide q-1={args.q-1})"); continue
        if n & (n - 1):
            print(f"  n={n}: SKIP (not a power of two)"); continue
        wstar, n3, prof = crossover_depth(args.q, n, rn, rd, args.wmax)
        tag = f"w*={wstar}" if wstar else f"w*>{args.wmax} (extras>n^3 through wmax)"
        print(f"  n={n:4} (n^3={n3}): {tag}")
        for r in prof:
            flag = "<=n^3" if r["le_n3"] else " >n^3"
            print(f"       w={r['w']} m={r['m']}: extras={r['extras']:>12}  [{flag}]  "
                  f"total={r['total']} struct={r['struct']} log2fiber={r['log2_fiber']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
