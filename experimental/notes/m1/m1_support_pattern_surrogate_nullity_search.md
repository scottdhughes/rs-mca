# M1 support-pattern surrogate-nullity search

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
`delta*_C`, or a global upper bound at `a=327`.

## Search Objective

The support/interpolation search works with seven support sets

```text
S_0, ..., S_6 subset H
```

with

```text
|S_i| = 327,
max_{i<j} |S_i cap S_j| <= 255.
```

At each coordinate `h`, the membership hypergraph records

```text
E_h = {i : h in S_i} subset {0,...,6}.
```

The objective is positive nullity for the reduced pairwise-overlap
interpolation matrix over `GF(17^32)`. A positive nullity would still need
extraction and distinctness checks before becoming a lower-bound certificate.

## Mutation Layer

The previous cyclic support-pattern packet showed that simple cyclic
hypergraphs remain full rank. This checkpoint stops preserving the cyclic
form and applies deterministic balanced two-switch mutations directly to the
membership hypergraph.

The scanner generated twelve mutated designs from the earlier cyclic seeds
using three proxy objectives:

- pair-boundary pressure;
- anchor-compression pressure;
- quotient-fiber repetition pressure.

It retained the six best candidates by a row-pattern / pair-boundary proxy and
then Sage-audited those retained candidates over both:

```text
GF(12289)       surrogate, 512 | 12288,
GF(17^32)      exact board field.
```

The surrogate rank is only a screening tool. The exact `GF(17^32)` rank is
the source of the route-cut status.

## Exact Results

All retained candidates satisfy:

```text
|S_i| = 327 for all i,
max pair intersection = 255.
```

The retained candidates push several pair intersections to the allowed
boundary. Exact Sage ranks are:

```text
pair_boundary_cyclic_3456_near_boundary_seed_202606399:
  compressed variables 360, rank 360, nullity 0

pair_boundary_cyclic_45_interval_high_overlap_seed_202606297:
  compressed variables 365, rank 365, nullity 0

fiber_repetition_cyclic_45_interval_high_overlap_seed_202606331:
  compressed variables 381, rank 381, nullity 0

anchor_compression_cyclic_3456_near_boundary_seed_202606416:
  compressed variables 355, rank 355, nullity 0

anchor_compression_cyclic_45_interval_high_overlap_seed_202606314:
  compressed variables 374, rank 374, nullity 0

fiber_repetition_cyclic_3456_near_boundary_seed_202606433:
  compressed variables 366, rank 366, nullity 0
```

Thus none of the six surrogate-scored mutations has a non-diagonal
interpolation solution. None can produce an `a=327` interleaved-list
certificate.

## Status Ledger

ROUTE_CUT_TESTED_CANDIDATES:

- twelve deterministic membership-hypergraph mutations generated;
- six retained by surrogate proxy score;
- all six exact-audited over `GF(17^32)`;
- all six have reduced nullity `0`;
- no tested candidate improves PR #133.

PARTIAL / OPEN:

- larger mutation beams;
- mutation moves that change multiplicity histograms rather than preserving
  seed pattern sizes;
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

The tested direct two-switch layer still full-ranks. The next useful search
should either widen the beam substantially or use mutation moves that change
the membership multiplicity histogram itself, while keeping `|S_i|=327` and
pair intersections at most `255`. Any proxy-positive candidate still needs the
same exact Sage rank gate and, if nullity appears, extraction of seven
distinct codewords and one received word.
