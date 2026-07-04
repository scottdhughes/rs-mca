# M1 a=327 pair-clear direction support chamber search

Status:

CANDIDATE / CHAMBER_NINE_ROW_STABLE / PARTIAL / EXPERIMENTAL

This packet follows `a9acb86` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous audit showed that the pinned five-row inactive chamber

```text
inactive row classes = [13,16,17,18,19]
direction = [0,5,0,0,0,1]
projective direction = [0,1,0,0,0,7]
inactive rank = 5
inactive kernel nullity = 1
```

is closed under one-row extension: adding any one of the nine active rows gives
rank 6.

This branch does not try to kill another active row inside that same chamber.
Instead, it exhaustively scans all projective directions in `GF(17)^6` for the
same base `14 x 6` coefficient matrix and asks whether there is a different
pair-clear support chamber with either:

```text
at least 6 zero rows
```

or

```text
at least 5 zero rows and inactive rank <= 4
```

The second condition is the useful chamber-slack target: a five-zero-row chamber
with rank at most 4 would have inactive kernel dimension at least 2, leaving
room to impose another active-row zero while preserving a nonzero direction.

## Result

The full projective scan over `GF(17)^6` tested:

```text
projective directions tested = 1508598
pair-clear directions = 360360
distinct pair-clear support chambers = 51
```

Among these pair-clear chambers:

```text
pair-clear nine-row-or-better chambers = 1
direct support-reduced chambers = 0
rank-slack chambers = 0
```

The unique nine-row-or-better chamber is the already banked pinned chamber:

```text
zero row classes = [13,16,17,18,19]
zero row count = 5
inactive rank = 5
inactive kernel nullity = 1
exemplar projective direction = [0,1,0,0,0,7]
active row classes = [0,2,3,5,6,11,12,14,15]
```

The extension probe tested lower-zero-row chambers by adding one active row and
searching the resulting kernel for a pair-clear vector:

```text
extension chambers tested = 50
extension tests = 571
extension pair-clear successes = 134
support-reduced extensions = 0
```

So the full base projective direction front does not produce:

- a direct `<=8` active-row pair-clear direction;
- a five-zero-row rank-slack chamber;
- a one-row extension that gives support reduction.

## Interpretation

This is a local front result for the current base `14 x 6` pair-clear module.
It sharpens the previous module syzygy audit:

- `a9acb86` proved the pinned inactive chamber is internally closed;
- this packet shows the full projective direction front for the same base
  matrix has no better pair-clear support chamber.

The result does not rule out:

- a different basis profile;
- a different template mutation;
- a different selected-class assignment;
- a higher-level pair-clear construction;
- an exact `a=327` witness outside this base direction-support front.

## Non-claims

This packet does not claim:

- an `a=327` certificate
- Sage `GF(17^32)` exact lift
- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- global obstruction outside the base direction-support chamber front

## Next Target

Move upstream rather than scanning this base matrix again:

```text
m1-a327-pairclear-template-chamber-mutation-search
```

The next constructive pass should vary the template/basis/assignment enough to
change the `14 x 6` coefficient arrangement, then rerun this chamber score on
each structural-pass candidate. The score to optimize is:

```text
pair-clear direction with >=6 zero rows
```

or:

```text
pair-clear chamber with >=5 zero rows and inactive rank <=4
```

Use Python first for broad GF(17) chamber scoring. Use Macaulay2/Singular only
for small pinned module certificates. Sage should still wait until a pair-clear
direction-kernel proxy target exists.
