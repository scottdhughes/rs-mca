# M1 support-pattern multiplicity-mutation search

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records a broader local support-pattern search for an `a=327`
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
`delta*_C`, or a global upper bound at `a=327`.

## Why This Layer Was Needed

The previous surrogate-nullity search retained support-pattern mutations that
hit the pair-intersection boundary, but the mutation move still preserved the
seed multiplicity histograms. The remaining risk was that the search had not
actually explored support hypergraphs with substantially different coordinate
membership sizes.

This checkpoint changes that. It uses degree-preserving pair replacements:
two coordinates are replaced by two new membership patterns with the same
total witness incidences. This keeps every support size fixed at `327`, but it
can move mass between low- and high-multiplicity coordinates.

The retained candidates contain many coordinates of sizes `1,2,6,7`, so they
are not cyclic re-embeddings and not histogram-preserving two-switch variants.

## Search Layer

The scanner generated twenty deterministic support-pattern mutations from the
previous cyclic seeds, using objectives for:

- multiplicity spread;
- pair-boundary pressure;
- anchor compression;
- quotient-fiber repetition;
- mixed pair-boundary / multiplicity-spread pressure.

It retained six candidates by a multiplicity/pair-boundary/rank-proxy score.
The retained candidates all satisfy:

```text
|S_i| = 327 for all i,
max_{i<j} |S_i cap S_j| = 255.
```

The surrogate field `GF(12289)` is only a screening tool. The exact
`GF(17^32)` rank gate is the source of the route-cut status.

## Exact Results

The six exact-audited retained candidates are:

```text
multiplicity_spread_cyclic_3456_balanced_seed_202607204:
  histogram {1:62, 2:97, 3:28, 4:58, 5:49, 6:54, 7:164}
  pairs at 255: 6
  compressed variables 30, rank 30, nullity 0

multiplicity_spread_cyclic_45_balanced_seed_202607014:
  histogram {1:66, 2:88, 3:33, 4:56, 5:48, 6:63, 7:158}
  pairs at 255: 8
  compressed variables 23, rank 23, nullity 0

multiplicity_spread_cyclic_45_interval_high_overlap_seed_202606919:
  histogram {1:57, 2:84, 3:48, 4:44, 5:67, 6:75, 7:137}
  pairs at 255: 6
  compressed variables 69, rank 69, nullity 0

multiplicity_spread_cyclic_3456_near_boundary_seed_202607109:
  histogram {1:47, 2:83, 3:52, 4:74, 5:50, 6:68, 7:138}
  pairs at 255: 7
  compressed variables 89, rank 89, nullity 0

mixed_boundary_spread_cyclic_3456_balanced_seed_202607280:
  histogram {1:68, 2:93, 3:24, 4:53, 5:53, 6:61, 7:160}
  pairs at 255: 9
  compressed variables 19, rank 19, nullity 0

mixed_boundary_spread_cyclic_45_balanced_seed_202607090:
  histogram {1:69, 2:89, 3:29, 4:47, 5:55, 6:69, 7:154}
  pairs at 255: 9
  compressed variables 32, rank 32, nullity 0
```

Thus none of the retained multiplicity-changing candidates has non-diagonal
interpolation nullity. None can produce an `a=327` interleaved-list
certificate.

## Status Ledger

ROUTE_CUT_TESTED_CANDIDATES:

- twenty deterministic multiplicity-changing mutations generated;
- six retained by surrogate score;
- all six exact-audited over `GF(17^32)`;
- all six have reduced nullity `0`;
- no tested candidate improves PR #133.

PARTIAL / OPEN:

- larger multiplicity-mutation beams;
- support-pattern moves not built from two-coordinate replacements;
- positive-nullity extraction;
- a global `Lambda_mu(C,327) <= 6` theorem.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next Step

This closes the specific risk that the previous nullity search was preserving
nice cyclic or histogram-stable support patterns. The broader search still
full-ranks, even for boundary-heavy candidates with very small compressed
dimension. A next attempt should either use a much larger stochastic beam or
switch to a constructive rank-defect objective rather than continuing to score
only by boundary pressure and multiplicity spread.
