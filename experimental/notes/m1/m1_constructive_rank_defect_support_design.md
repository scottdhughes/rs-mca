# M1 constructive rank-defect support-design search

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records a local constructive support-pattern search for an `a=327`
interleaved-list certificate for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` support-design audit, not an MCA `N_bad` row, and it does
not claim protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, a global support-pattern rank-nullity classification, or a global
upper bound at `a=327`.

## Why This Layer Was Added

The prior surrogate-rank feedback search showed that multiplicity-changing
mutations selected by actual reduced rank over `GF(12289)` still exact-audited
as full rank over `GF(17^32)`. This checkpoint changes the search objective
again: instead of hoping pair-boundary pressure or multiplicity spread creates
rank defect, it generates support designs with explicit repeated-template
features.

For a support design, each coordinate has a membership set

```text
E_h = {i : h in S_i} subset {0,...,6}.
```

The reduced rank gate anchors `P_0=0` and tests the induced pairwise-overlap
constraints on the six difference polynomials. Positive nullity would be a
candidate algebraic gate toward seven distinct degree-`<256` codewords and one
received word. Full rank route-cuts only the tested support design.

## Search Layer

The scanner generated eighty deterministic constructive support designs across
four families:

```text
quotient_template
overlap_cycle
anchored_zero
quotient_integer
```

Every generated design is constrained to preserve

```text
|S_i| = 327 for all i,
max_{i<j} |S_i cap S_j| <= 255.
```

Each candidate records an `equation_template_histogram`, quotient-fiber
profiles, a quotient integer profile, and a structural rank-defect score. The
scanner then computes the reduced rank over the surrogate field `GF(12289)`,
where `512 | 12288`, and retains eight candidates for exact Sage audit over
`GF(17^32)`.

The surrogate field is only a screening field. The board-relevant denominator
remains `|F| = 17^32`.

## Exact Results

The eight retained candidates are:

```text
anchored_zero_cyclic_45_balanced_r12_seed_202609189:
  compressed variables 134, surrogate rank 134, exact rank 134, nullity 0

overlap_cycle_cyclic_3456_balanced_r12_seed_202608929:
  compressed variables 136, surrogate rank 136, exact rank 136, nullity 0

anchored_zero_cyclic_45_balanced_r0_seed_202609033:
  compressed variables 138, surrogate rank 138, exact rank 138, nullity 0

anchored_zero_cyclic_45_balanced_r16_seed_202609241:
  compressed variables 150, surrogate rank 150, exact rank 150, nullity 0

anchored_zero_cyclic_45_balanced_r14_seed_202609215:
  compressed variables 152, surrogate rank 152, exact rank 152, nullity 0

anchored_zero_cyclic_45_balanced_r8_seed_202609137:
  compressed variables 152, surrogate rank 152, exact rank 152, nullity 0

overlap_cycle_cyclic_3456_balanced_r6_seed_202608851:
  compressed variables 158, surrogate rank 158, exact rank 158, nullity 0

overlap_cycle_cyclic_3456_balanced_r2_seed_202608799:
  compressed variables 159, surrogate rank 159, exact rank 159, nullity 0
```

The retained exact-audited set contains five `anchored_zero` candidates and
three `overlap_cycle` candidates. No retained row had positive surrogate
nullity, and all retained rows have exact nullity `0` over `GF(17^32)`.

## Status Ledger

ROUTE_CUT_TESTED_CANDIDATES:

- eighty constructive repeated-template support designs generated;
- all candidates preserve `|S_i|=327` and pair intersections at most `255`;
- eight candidates retained after `GF(12289)` reduced-rank feedback;
- all eight exact-audited over `GF(17^32)`;
- all eight exact reduced rank gates are full rank with nullity `0`;
- no tested candidate improves PR #133.

PARTIAL / OPEN:

- larger constructive search;
- direct symbolic rank-defect construction;
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

This layer confirms that the first repeated-template constructive candidates
still full-rank exactly over `GF(17^32)`. The next useful move is not a board
update; it is either a larger constructive search with stronger template
forcing or a direct symbolic rank-defect construction that designs repeated
overlap equations rather than selecting them by proxy score.
