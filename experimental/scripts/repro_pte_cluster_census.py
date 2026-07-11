#!/usr/bin/env python3
"""Heavy reproducibility census for the PTE-cluster packing frontier note.

Stdlib-only. This is the SLOW script that *finds* the champions; the fast
verifier (verify_pte_cluster_packing.py) only re-checks the reported blocks.
Run under `ulimit -v 2097152`.

Stages (pass as argv[1], default 'all'):
  exh    diameter-bounded exhaustive optimum rho(b), b=6..14      (~30 s)
  sym    symmetric wide-diameter best rho(b) + champion, b=6..16  (~2-4 min,
         diameter/time-capped; prints the b=14 champion 0.156659)
  iap    interval-minus-AP family scan, b=6..18                   (~2 min)
  phi    max-fstar / phi(b) measurement, b=6..16                  (folded into sym)

Memory wall (documented, NO silent cap): the signature DP stores L1 distinct
(w,s,q) keys; for sparse near-interval blocks L1 ~ 2^b, so exact (fstar,L1)
computation is capped near b<=20 in 2 GB. Every truncation is printed. The
frontier does NOT converge in this range (see note R2/R5): both phi(b) and the
best rho creep upward with b and diameter.
"""
from __future__ import annotations
import itertools, math, sys, time
from collections import defaultdict
from math import gcd, log

LOG2 = math.log(2)
DPCAP = 1_600_000  # max distinct signatures held (memory wall, printed if hit)


def sig_dp(V, cap=DPCAP):
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
        if len(dp) > cap:
            return None
    return dp


def stat(V):
    dp = sig_dp(V)
    if dp is None:
        return None
    b = len(V); f = max(dp.values()); L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2


def canon(V):
    m = min(V); W = tuple(sorted(x - m for x in V)); g = 0
    for x in W:
        g = gcd(g, x)
    if g > 1:
        W = tuple(x // g for x in W)
    R = tuple(sorted(W[-1] - x for x in W))
    return min(W, R)


def sym_dels(n, d):
    c = n - 1
    pairs = [(i, c - i) for i in range(n // 2)]
    center = [c // 2] if n % 2 else []
    if d % 2 == 0:
        for ch in itertools.combinations(pairs, d // 2):
            D = set()
            for p in ch:
                D.update(p)
            yield D
    elif center:
        for ch in itertools.combinations(pairs, (d - 1) // 2):
            D = set(center)
            for p in ch:
                D.update(p)
            yield D


def stage_exh():
    print("=== EXHAUSTIVE diameter-bounded optimum rho(b) (affine-canonical) ===")
    cfg = {6: 5, 7: 5, 8: 5, 9: 4, 10: 4, 11: 4, 12: 4, 13: 3, 14: 3}
    for b in range(6, 15):
        sl = cfg[b]; seen = set(); best = None
        for rest in itertools.combinations(range(1, b + sl), b - 1):
            cv = canon((0,) + rest)
            if cv in seen:
                continue
            seen.add(cv)
            r = stat(cv)
            if r and r[0] >= 2 and (best is None or r[2] > best[0]):
                best = (r[2], cv, r[0], r[1])
        r, cv, f, L = best
        print(f"b={b:2d} diam<={b+sl-1} classes={len(seen):5d}  OPT rho={r:.6f} fstar={f} L1={L} V={cv}")


def stage_sym(bmax=16, tbudget=240):
    print("=== SYMMETRIC wide-diameter best rho(b) + champion + phi(b) ===")
    t0 = time.time(); champ = None
    for b in range(6, bmax + 1):
        bestr = None; bestf = None; diamcap = b + (10 if b <= 14 else 8)
        for d in range(0, diamcap - b + 1):
            n = b + d
            for D in sym_dels(n, d):
                V = tuple(x for x in range(n) if x not in D)
                if len(V) != b:
                    continue
                r = stat(V)
                if r is None:
                    continue
                f, L, rho = r
                if f >= 2 and (bestr is None or rho > bestr[0]):
                    bestr = (rho, tuple(sorted(D)), n, f, L)
                if f >= 2 and (bestf is None or f > bestf[0]):
                    bestf = (f, rho)
            if time.time() - t0 > tbudget:
                print(f"  [time budget hit at b={b}, d={d}; result is a lower bound]")
                break
        if bestr:
            rho, D, n, f, L = bestr
            phi = log(bestf[0]) / b
            print(f"b={b:2d}: BESTrho={rho:.6f} (fstar={f} L1={L} diam={n-1} del={D}) "
                  f"| MAXfstar={bestf[0]} phi={phi:.4f}")
            if champ is None or rho > champ[0]:
                champ = (rho, b, D, n, f, L)
        if time.time() - t0 > tbudget:
            break
    if champ:
        rho, b, D, n, f, L = champ
        V = tuple(x for x in range(n) if x not in D)
        print(f"\nCHAMPION rho={rho:.6f} at b={b} V={V} (fstar={f}, L1={L})")


def stage_iap(bmax=18):
    print("=== interval-minus-AP family best rho(b) ===")
    best = {}
    for n in range(6, bmax + 6):
        for g in range(3, n):
            for a in range(0, g + 3):
                D = set(range(a, n, g))
                V = tuple(x for x in range(n) if x not in D)
                b = len(V)
                if b < 6 or b > bmax:
                    continue
                r = stat(V)
                if r is None or r[0] < 2:
                    continue
                if b not in best or r[2] > best[b][0]:
                    best[b] = (r[2], n, a, g, r[0], r[1])
    for b in sorted(best):
        rho, n, a, g, f, L = best[b]
        dels = list(range(a, n, g))
        print(f"b={b:2d}: rho={rho:.6f} {{0..{n-1}}}\\{dels} (a={a},g={g}) fstar={f} L1={L}")


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    t0 = time.time()
    if stage in ("exh", "all"):
        stage_exh()
    if stage in ("sym", "phi", "all"):
        stage_sym()
    if stage in ("iap", "all"):
        stage_iap()
    print(f"\n[repro runtime {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
