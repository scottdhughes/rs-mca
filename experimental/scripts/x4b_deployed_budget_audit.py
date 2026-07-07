#!/usr/bin/env python3
"""x4b step 2: deployed-row budget audit for the MomentTradeStaircase column. Printed exact constants.

THE UNCONDITIONAL CAP (rigidity + pigeonhole; rigidity is Lean-anchored via powersum_rigidity):
  any t-null block B (e_1..e_t = 0) has |B| >= t+1  [locator would be X^b otherwise; 0 not in mu_n]
  => any DISJOINT family of blocks in a domain of size n has k <= floor(n/(t+1))
  => per-prefix MomentTradeStaircase multiplicity <= 2^k  (each member = tail + a sub-union of the family;
     sub-unions of equal total size only, so 2^k is conservative).
CRITERION: the x4 primitive budget is n^2, so the moment column is UNCONDITIONALLY affordable when
  2^{floor(n/(t+1))} <= n^2   <=>   floor(n/(t+1)) <= 2 log2 n   <=>   t >~ n/(2 log2 n) - 1.
CONDITIONAL sharpening (first-moment window): E[#blocks size b] = C(n,b)/p^t < 1 outside b in
  [n/2 - d, n/2 + d]; solve for d. Blocks confined to the window => k <= floor(n/(n/2 - d)) (usually 2)
  => mass <= 4. Also print the b = t+1 deficit (the Q-gap cliff; cross-check vs prop:proper-q-gap 1.66e6).
Rows: KB-MCA deployed; the toy witness row (193, 64, 3) for contrast; criterion check for both.
"""
from __future__ import annotations
import math


def log2C(n, b):
    return (math.lgamma(n + 1) - math.lgamma(b + 1) - math.lgamma(n - b + 1)) / math.log(2)


def audit(name, p, n, t):
    print(f"\n### row {name}: p={p}, n={n}, t={t}")
    k_uncond = n // (t + 1)
    log2n = math.log2(n)
    crit_t = n / (2 * log2n) - 1
    ok = k_uncond <= 2 * log2n
    print(f"  UNCONDITIONAL: |B| >= t+1 = {t+1}  =>  k <= floor(n/(t+1)) = {k_uncond}")
    print(f"    per-prefix moment-column mass <= 2^{k_uncond};  n^2 budget = 2^{2*log2n:.1f}")
    print(f"    criterion t >= n/(2 log2 n) - 1 = {crit_t:,.0f}:  t = {t:,} -> {'PASS: moment column <= n^2 UNCONDITIONALLY' if ok else 'FAIL: 2^k exceeds n^2 (column open at this row)'}")
    # first-moment window
    tlog2p = t * math.log2(p)
    maxb = log2C(n, n // 2)
    if maxb < tlog2p:
        print(f"    first-moment: even b=n/2 has log2 C(n,b) = {maxb:,.0f} < t log2 p = {tlog2p:,.0f} -> NO blocks expected at any size (mean<1 everywhere)")
        return
    lo, hi = 1, n // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if log2C(n, mid) < tlog2p:
            lo = mid
        else:
            hi = mid
    bmin = hi
    d = n // 2 - bmin
    k_window = n // bmin if bmin > 0 else 0
    cliff = tlog2p - log2C(n, t + 1)
    print(f"    first-moment window: mean >= 1 iff b in [{bmin:,}, {n - bmin:,}]  (d = n/2 - bmin = {d:,})")
    print(f"    => window-conditional k <= floor(n/bmin) = {k_window}; mass <= 2^{k_window} = {2**k_window}")
    print(f"    b = t+1 deficit (the Q-gap cliff): t log2 p - log2 C(n,t+1) = {cliff:,.0f} bits"
          f"  (prop:proper-q-gap ~ 1.66e6 at KB: {'MATCHES' if abs(cliff - 1.66e6) < 5e4 else 'differs'})")


def main():
    print("# x4b MomentTradeStaircase budget audit -- exact printed constants")
    audit("KB-MCA (deployed)", 2**31 - 2**24 + 1, 2**21, 67471)
    audit("toy witness row", 193, 64, 3)
    audit("toy (97, 32, 2)", 97, 32, 2)
    print("\n# PASS rows: the moment column is closed UNCONDITIONALLY (<= n^2) by rigidity+pigeonhole alone.")
    print("# FAIL rows (small t/n ratio, incl. the witness toy): the column is genuinely live there --")
    print("#   consistent with the verified primitive witness at (193,64,3) and the C(R,R/2) toy blowup.")


if __name__ == "__main__":
    raise SystemExit(main())
