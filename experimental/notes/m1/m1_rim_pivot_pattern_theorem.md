# M1 RIM pivot-pattern theorem audit

Status: AUDIT / CANDIDATE_THEOREM / COMPUTATIONAL_CERTIFICATE / PARTIAL /
EXPERIMENTAL

This note mines the 34 Sage-replayed pivot certificates for exact full-rank
`a=327` reduced-intersection matrices in the M1 interleaved-list workstream for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` pivot-profile audit, not an MCA `N_bad` row, and it does
not claim protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, an `a=327` certificate, or a global upper bound at `a=327`.

## Input

The input is the full pivot replay packet:

```text
experimental/data/m1_rim_support_pattern_pivot_replay.json
```

That packet already certified:

```text
34 / 34 prior exact full-rank a=327 RIM matrices
```

by Sage-replayed RREF pivot-minor certificates over `GF(17^32)`.

## Profile Mining Result

The 34 certificates split into three structural pivot families:

```text
support_overlap_rref_pivot:
  covered rows: 20
  source family: support_pattern
  compressed-variable range: 19..159
  pivot rows: support_overlap_row only

generic_pairwise_rref_pivot:
  covered rows: 6
  source family: balanced_clique
  compressed-variable range: 179..217
  pivot rows: balanced_or_generic_pairwise_row only

quotient_residual_rref_pivot:
  covered rows: 8
  source family: two_level_quotient_residual
  compressed-variable range: 6..192
  pivot rows: quotient_full_fiber_row plus residual_or_partial_fiber_row
```

The global certificate pattern is common to all 34:

```text
rref_pivot_minor_certificate:
  covered rows: 34
  statement: each tested matrix has an explicit Sage-replayed RREF
             pivot-minor certificate over GF(17^32).
```

That global statement is a computational certificate, not a structural theorem.
No single structural pivot schedule currently covers all three families.

## Aggregate Pivot Profile

Across all 34 certified matrices:

```text
balanced_or_generic_pairwise_row: 1226
quotient_full_fiber_row:          383
residual_or_partial_fiber_row:     37
support_overlap_row:             1901
```

The support-pattern families are the cleanest theorem target: all 20 use
support-overlap rows for every pivot. This suggests a deterministic
support-overlap pivot schedule, but the current packet only records the
observed RREF schedules. It does not prove that such a schedule works for an
entire support-pattern class.

## Candidate Theorem Targets

Candidate theorem A:

```text
For the tested support-pattern RIM rows, the RREF pivot schedule uses
support-overlap rows to cover every compressed variable.
```

Candidate theorem B:

```text
For the tested balanced-clique pairwise rows, generic pairwise rows provide
one RREF pivot for every compressed variable.
```

Candidate theorem C:

```text
For the tested two-level quotient-residual rows, quotient-fiber and residual
rows jointly provide one RREF pivot for every compressed variable.
```

These are candidate pattern statements over tested rows. None is promoted to a
class theorem in this checkpoint.

## Status Ledger

AUDIT / COMPUTATIONAL_CERTIFICATE:

- 34 certified pivot-minor packets loaded from the replay artifact;
- 34 pivot profiles derived and hash-checked against the replay artifact;
- three structural candidate pivot patterns identified;
- one global certificate pattern covers all 34 tested matrices;
- no positive nullity appears in the profiled rows;
- no `a=327` interleaved-list certificate appears.

CANDIDATE_THEOREM / PARTIAL:

- support-overlap schedule is the strongest next theorem target;
- no deterministic block-triangular or row-ordering proof is established;
- no common structural pivot theorem covers all 34 rows;
- global `Lambda_mu(C,327) <= 6` remains open.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- deterministic pivot-pattern theorem;
- global RIM full-rank theorem;
- global `Lambda_mu(C,327) <= 6`;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next Step

The next useful move is a deterministic support-overlap pivot-schedule proof for
the 20 support-pattern rows. The proof target should take the observed
support-overlap RREF pivot profiles and replace them with a reproducible
row-ordering or block-pivot rule that implies full column rank for the stated
support-pattern class.
