#!/usr/bin/env python3
"""x4b: four-deployed-row budget audit for the MomentTradeStaircase column. Printed exact constants.

CAP (PROVED, unconditional; rigidity core Lean-anchored):
  L1: any t-null block has |B| >= t+1 (locator X^b otherwise; 0 not in mu_n).
  L2: disjoint families have k <= floor(n/(t+1)).
  L3 (Erdos-Littlewood-Offord 1945): per (prefix, degree), staircase members from one family+tail are
      sub-unions of EQUAL total size => <= C(k, floor(k/2)) for ANY size profile.
Row constants from grande_finale.tex finite tables + certificates: n = 2^21 for all four rows;
  KB (p = 2^31-2^24+1): B* = floor(p^6/2^128); M31 (p' = 2^31-1): B* = floor(p'^4/2^100) = 16777215.
  t: KB-MCA 67471, KB-list 67470, M31-MCA 67447 (w_safe printed), M31-list 67446 (derived from a+).
"""
import math

def log2C(n, b):
    return (math.lgamma(n+1) - math.lgamma(b+1) - math.lgamma(n-b+1)) / math.log(2)

N = 2**21
ROWS = [
    ("KB-MCA",   2**31-2**24+1, 67471, 6, 128, "a+=1116048"),
    ("KB-list",  2**31-2**24+1, 67470, 6, 128, "a+=1116047"),
    ("M31-MCA",  2**31-1,       67447, 4, 100, "a+=1116024, w_safe printed"),
    ("M31-list", 2**31-1,       67446, 4, 100, "a+=1116023, w derived"),
]

def main():
    log2n = math.log2(N)
    print(f"# x4b four-row audit: n = 2^21; criterion t >= n/(2 log2 n) - 1 = {N/(2*log2n)-1:,.0f}")
    for name, p, t, e, shift, note in ROWS:
        k = N // (t + 1)
        Bstar_bits = e * math.log2(p) - shift
        elo_bits = log2C(k, k // 2)
        # window
        tl2p = t * math.log2(p)
        lo, hi = 1, N // 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if log2C(N, mid) < tl2p: lo = mid
            else: hi = mid
        bmin = hi; kwin = N // bmin
        # M31-style residue: smallest k with C(k, k/2) > B*
        kneed = k
        for kk in range(2, k + 1):
            if log2C(kk, kk // 2) > Bstar_bits:
                kneed = kk
                break
        else:
            kneed = None
        print(f"\n## {name} (p={p}, t={t}) [{note}]")
        print(f"   UNCONDITIONAL: k <= {k} (<= 2 log2 n = 42: option (a) HOLDS, log-bounded)")
        print(f"   per-(prefix,degree) mass <= C({k},{k//2}) = 2^{elo_bits:.2f}  [Erdos-LO]  vs n^2 = 2^42: "
              f"{'FITS' if elo_bits <= 42 else 'over'}  vs B* = 2^{Bstar_bits:.2f}: "
              f"{'FITS unconditionally' if elo_bits <= Bstar_bits else f'GAP {elo_bits - Bstar_bits:.2f} bits'}")
        if kneed:
            print(f"   RESIDUE (unconditional closure vs B*): exclude k >= {kneed} disjoint blocks all of size "
                  f"in [{t+1:,}, {N//kneed:,}]  (C({kneed},{kneed//2}) = 2^{log2C(kneed,kneed//2):.2f} > B*)")
        print(f"   WINDOW (first-moment): blocks confined to b >= {bmin:,} => k <= {kwin}; conditional mass <= {2**kwin}")

if __name__ == "__main__":
    raise SystemExit(main())
