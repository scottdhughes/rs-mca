# M1 a=327 compensated repaired-skeleton split v2

Status: `PROOF_RECORD | CANDIDATE | EXACT_EXTRACTION_NO_A327 | PARTIAL`

This packet reruns the compensated repaired-skeleton split search after the
Sage-native cache checkpoint `c181b13`. The previous compensated branch
`1a75dfe` timed out before constructing exact vectors because it rebuilt the
`GF(17^32)` repaired skeleton in the hot path. This v2 branch loads the
prepared skeleton cache and appends split/replacement rows in cached
pivot/free coordinates.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is not an MCA row, not a protocol claim, and not a public-board update.

## Cache

The exact cache artifact is:

```text
experimental/data/cache/m1_a327_repaired_skeleton_budget32_prepared_state.sobj
```

with SHA-256:

```text
f77410189226820cf8e8a2830f3a48523a92e485347702754c854fa8955addb4
```

The cache stores the budget-32 repaired skeleton matrix, right-hand side,
pivots, free columns, pivot matrix, pivot inverse, base vector, fixed specs,
and exact field/subgroup data. The v2 audit must not call
`repaired_context()` in the split-grid hot path.

## Baseline

The repaired skeleton is:

```text
capacity              = 333
B({1,7})..B({5,7})    = [1024,657,656,1024,1024]
collapse pattern      = [[1,4,5,7],[6],[3],[2]]
six-class dominance   = 0
```

The direct failed split damages the skeleton as:

```text
capacity              = 315
B({1,7})..B({5,7})    = [1024,593,592,512,1024]
```

Damage profile:

```text
capacity loss = 18
B({2,7}) loss = 64
B({3,7}) loss = 64
B({4,7}) loss = 512
B({5,7}) loss = 0
```

So `B({4,7})` is a first-class repair target.

## Search Grid

The v2 audit tests:

```text
split families: split_4_from_157, split_14_vs_57, split_1_from_457
replacement bundle sizes: 8, 16, 32
selectors: capacity_first, B27_B37_first, B47_first, balanced_repair,
           quotient_fiber_local
```

Total planned systems: `45`.

The current JSON is a partial ledger, not the full grid:

```text
systems tested             = 1 / 45
exact vectors constructed  = 1
best capacity              = 180
best pair values           = [577,657,656,515,577]
best collapse pattern      = [[1,5],[7],[6],[4],[3],[2]]
best failure               = COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED
```

The full grid remains mathematically live. The v2 audit now writes progress
after every case so future runs do not lose completed vectors if a slow
residual solve has to be interrupted.

Replacement classes include:

```text
{2,7}, {3,7}, {4,7},
{2,3,7}, {2,4,7}, {3,4,7},
{4,5,7}, {1,4,7},
{1,4}, {1,4,5}, {1,4,5,7}
```

## Guards

A locally promising vector must satisfy:

```text
capacity >= 327
B({2,7}) >= 654
B({3,7}) >= 654
B({4,7}) >= 654
B({5,7}) >= 654
D2 split preserved
six-class dominance = 0
```

An exact candidate additionally requires seven distinct degree-`<256`
codewords and exact max-min agreement at least `327` on `H`.

## Non-claims

- No `a=327` interleaved-list certificate unless Sage verifies the exact
  witness.
- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No public-row update.
