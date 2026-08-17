## Summary

Stacked on exact parent `8911e26e78c8d91173c413f079a13f88a04701fe`.

This PR replaces the retracted three-slope packet. A proper rank-two drop can
leave additional universal coordinates in its rank-one subfamily; cancelling
those coordinates lowers the effective residual dimension and changes the
valid rank-one capacity. This packet retains that variable and converts the
capacity inequality into an exact common-locator floor.

For a proper drop at ambient dimension `K`, let `k` be the effective rank-one
dimension after cancelling its entire common pair core. Exact capacity
inversion gives

\[
\deg L_{\rm common}=K-k\ge K-\kappa(K).
\]

The floor is nondecreasing and includes:

```text
ambient K   incident load   max effective k   common-locator floor
262,711       1,301,847          262,710                    1
262,731       1,301,906          262,697                   34
264,388       1,306,789          260,256                4,132
300,000       1,408,829          209,241               90,759
500,000       1,894,705          107,312              392,688
1,048,576     2,751,700           40,231            1,008,345
```

At the full row, cap `2,751,709` is available at effective dimension `40,231`,
while the next dimension has cap `2,751,689`, below the forced load.

## Scope

- result: proved source-bound common-locator floor for every proper rank-two
  drop;
- affine error rank 12: not paid;
- affine error rank 13: not paid;
- active-v4 ledger movement: `0`;
- KoalaBear closure: not claimed.

The next theorem is a chronology-safe forest compiler for these forced common
cores. Local locator charges may not be summed independently.

## Verification

- `262,709` uniform-cap dimensions checked exactly;
- `785,867` active weighted-line endpoint profiles checked exactly;
- `785,866` ambient locator-floor cells checked exactly;
- locator floor has zero decreases;
- independent selected-cell audit: PASS;
- finite endpoint controls: `1,334`;
- hostile mutations: `8/8` rejected;
- no external theorem is load-bearing.

Canonical payload: `edef5ffa88a495a0a659a62a3ce891372b59458350ef4eab5b35f75ed5f37baa`.
