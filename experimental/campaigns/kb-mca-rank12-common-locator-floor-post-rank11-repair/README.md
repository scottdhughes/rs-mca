# Rank-twelve common-locator floor

## Exact parent and corrected scope

This packet is stacked on the uniform rank-one repair at exact parent
`8911e26e78c8d91173c413f079a13f88a04701fe`.

It replaces the retracted dimension-matched three-slope packet. The omitted
variable there was the number of additional universal coordinates in the
rank-one subfamily produced by a proper rank-two drop. Those coordinates
lower the effective residual dimension and can increase the valid rank-one
capacity. This packet retains that variable exactly.

The result is a structural route cut, not an affine-error-rank-12 payment. It
moves no active-v4 ledger atom and does not claim KoalaBear closure.

## Rank-two incident load

The source-bound descent supplies a rank-two explanation family of

```text
L_2 = 5,170,912
```

slopes. At ambient dimension `K`, a proper complete-core drop at a coordinate
`x` produces at least

\[
I_2(K)=\left\lceil
\frac{L_2(67{,}472+K)-C_2(K)}{1{,}048{,}576+K}
\right\rceil
\]

rank-at-most-one slopes after shortening `x`.

Let `u` be the number of further coordinates universal for this rank-one
subfamily. Complete-agreement locator cancellation is source-bound, so after
removing them the effective residual dimension is

\[
k=K-1-u.
\]

The proper-drop subfamily therefore has a common pair-core locator of degree

\[
c=u+1=K-k.
\]

## Exact rank-one capacity function

For `1<=k<262,710`, the packet independently reconstructs the parent uniform
weighted-line cap `U(k)`. It checks all `262,709` dimensions and recovers

```text
U(1)       = 4,070,947
U(262,709) = 1,301,883.
```

For `k>=262,710`, cancel all universal coordinates first and apply the
heavy/light stability theorem. Put

\[
V=1{,}048{,}576-2\cdot67{,}472-k+2.
\]

The exact cap is bounded by

\[
S(k)=\max\{2V+2,981{,}136\}.
\]

The verifier checks all `785,867` active endpoint cells. The unique high
extremal profile has two heavy line classes, each of effective outside
deficiency one; every other high profile contributes at most `981,105`
points, and the light-only cap is at most `31`.

Define

\[
A(k)=\begin{cases}
U(k),&k<262{,}710,\\
S(k),&k\ge262{,}710.
\end{cases}
\]

The exact transition is

```text
A(262,709) = 1,301,883
A(262,710) = 1,301,850.
```

The function is nonincreasing.

## Locator-floor theorem

For each ambient dimension `K`, define

\[
\kappa(K)=\max\{k\le K-1:A(k)\ge I_2(K)\}.
\]

Any proper rank-two drop at `K` must satisfy

\[
\boxed{\deg L_{\rm common}\ge K-\kappa(K)}.
\]

Indeed, after cancelling the common locator the rank-one subfamily has
effective dimension `k=K-c` and at most `A(k)` slopes. Since it contains at
least `I_2(K)` slopes, `k<=kappa(K)`.

The verifier checks all `785,866` ambient dimensions. The locator floor is
nondecreasing. Selected exact cells are:

```text
ambient K   incident load   max effective k   common-locator floor
262,711       1,301,847          262,710                    1
262,712       1,301,850          262,710                    2
262,713       1,301,853          262,709                    4
262,731       1,301,906          262,697                   34
264,388       1,306,789          260,256                4,132
300,000       1,408,829          209,241               90,759
500,000       1,894,705          107,312              392,688
1,048,576     2,751,700           40,231            1,008,345
```

At the full KoalaBear dimension, the next effective dimension already has cap
`2,751,689`, below the forced `2,751,700`; the maximal legal effective
dimension is exactly `40,231`, whose cap is `2,751,709`.

Additional exact milestones:

```text
locator >= 32        by ambient K =   262,731  (actual floor 34)
locator >= 4,131     by ambient K =   264,388  (actual floor 4,132)
locator >= 100,000   by ambient K =   303,866  (actual floor 100,002)
locator >= 500,000   by ambient K =   587,137
locator >= 1,000,000 by ambient K = 1,040,688
```

## What this proves and does not prove

It proves that an early proper rank-two drop cannot remain an unstructured
rank-one family: it must carry a quantitatively large, source-bound common
pair core. The required locator grows from one coordinate at the first cell
to more than one million coordinates at the full row.

It does not pay affine error rank twelve. The common-core subfamilies may
overlap in slope units, so they cannot be summed independently or inserted
into an active owner without a chronology theorem.

## Strongest next theorem

Build a chronology-safe forest compiler for these forced locator subfamilies.
The most promising split is:

1. locators of degree at least `4,132`, where the existing order-32 and
   common-core staircase interfaces become available; and
2. the narrow initial window `262,711<=K<264,388`, where the exact locator
   floor is below that threshold and a finite near-extremal rank-two
   classification is required.

The compiler must assign each original slope once, preserve the actual
minimizing-pair provenance, and either cancel one common locator or emit the
smallest overlap collision. A sum of local shortening charges is not valid.

## Verification

```bash
python3 experimental/scripts/verify_kb_mca_rank12_common_locator_floor_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_common_locator_floor_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank12_common_locator_floor_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_common_locator_floor_manifest_v1.py
```

The primary verifier checks `262,709` uniform-cap dimensions, `785,867`
active endpoint profiles, and `785,866` ambient locator-floor cells. The
independent audit directly reconstructs eight selected cells and exhausts
`1,334` finite endpoint controls. No external theorem is load-bearing.
