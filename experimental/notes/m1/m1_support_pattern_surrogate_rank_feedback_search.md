# M1 support-pattern surrogate-rank feedback search

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records a local support-pattern search for an `a=327`
interleaved-list certificate for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` audit, not an MCA `N_bad` row, and it does not claim
protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, a global support-pattern classification, or a global upper bound
at `a=327`.

## Why This Layer Was Added

The previous multiplicity-mutation checkpoint closed the immediate risk that
the search only tested cyclic or histogram-stable support patterns. It still
selected retained rows by pair-boundary and multiplicity-spread pressure.
Those are useful combinatorial pressures, but they do not directly measure the
reduced interpolation rank.

This checkpoint adds a first feedback loop using actual reduced rank over the
surrogate field `GF(12289)`, where `512 | 12288`. The surrogate field is not a
proof field for the board row. It is a screening field used to choose retained
candidates before exact Sage audit over `GF(17^32)`.

## Search Layer

The scanner generated forty-eight deterministic support-pattern mutations from
the previous cyclic seeds. Each mutation uses degree-preserving pair
replacement on the membership hypergraph

```text
E_h = {i : h in S_i} subset {0,...,6}.
```

All generated candidates are constrained to preserve

```text
|S_i| = 327 for all i,
max_{i<j} |S_i cap S_j| <= 255.
```

The scanner first applies a multiplicity / pair-boundary prefilter, then
computes the actual reduced rank over `GF(12289)` for the top twelve
prefiltered candidates. It retains six candidates by the surrogate-rank
feedback score, preferring positive surrogate nullity if it appears and
otherwise keeping the lowest-rank / lowest-compressed-variable candidates.

The retained candidates are then exact-audited over `GF(17^32)` by Sage.

## Exact Results

The six retained candidates are:

```text
multiplicity_spread_cyclic_45_balanced_r2_seed_202607755:
  histogram {1:61, 2:69, 3:44, 4:70, 5:67, 6:64, 7:137}
  pair max 255, pairs at 255: 1
  compressed variables 59, surrogate rank 59, exact rank 59, nullity 0

multiplicity_spread_cyclic_3456_balanced_r0_seed_202608129:
  histogram {1:52, 2:80, 3:48, 4:58, 5:70, 6:77, 7:127}
  pair max 249, pairs at 255: 0
  compressed variables 67, surrogate rank 67, exact rank 67, nullity 0

multiplicity_spread_cyclic_45_balanced_r0_seed_202607721:
  histogram {1:57, 2:72, 3:42, 4:68, 5:72, 6:77, 7:124}
  pair max 254, pairs at 255: 0
  compressed variables 69, surrogate rank 69, exact rank 69, nullity 0

multiplicity_spread_cyclic_45_balanced_r1_seed_202607738:
  histogram {1:56, 2:69, 3:51, 4:72, 5:56, 6:82, 7:126}
  pair max 254, pairs at 255: 0
  compressed variables 77, surrogate rank 77, exact rank 77, nullity 0

multiplicity_spread_cyclic_3456_balanced_r2_seed_202608163:
  histogram {1:46, 2:82, 3:51, 4:58, 5:74, 6:83, 7:118}
  pair max 254, pairs at 255: 0
  compressed variables 87, surrogate rank 87, exact rank 87, nullity 0

multiplicity_spread_cyclic_3456_balanced_r1_seed_202608146:
  histogram {1:59, 2:69, 3:44, 4:61, 5:79, 6:79, 7:121}
  pair max 255, pairs at 255: 1
  compressed variables 101, surrogate rank 101, exact rank 101, nullity 0
```

Thus the surrogate-rank feedback did not find a proxy-positive nullity
candidate, and all exact-audited retained rows remain full rank over
`GF(17^32)`.

## Status Ledger

ROUTE_CUT_TESTED_CANDIDATES:

- forty-eight deterministic multiplicity-changing mutations generated;
- twelve candidates evaluated by actual reduced rank over `GF(12289)`;
- six rank-feedback candidates retained;
- all six exact-audited over `GF(17^32)`;
- all six have reduced nullity `0`;
- no tested candidate improves PR #133.

PARTIAL / OPEN:

- larger stochastic beams;
- constructive rank-defect objectives;
- positive-nullity extraction;
- global support-pattern rank-nullity classification;
- a global `Lambda_mu(C,327) <= 6` theorem.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`;
- global support-pattern rank-nullity classification;
- global `Lambda_mu(C,327) <= 6`.

## Next Step

This branch is a better search diagnostic than pure pair-boundary scoring: it
actually asks whether the surrogate reduced matrix drops rank before spending
exact `GF(17^32)` work. The retained candidates still full-rank, including
low-compressed-variable rows. The next useful step is either a substantially
larger stochastic beam using this same surrogate-rank feedback loop or a
constructive rank-defect search that designs repeated overlap equations
directly rather than hoping boundary pressure creates them.
