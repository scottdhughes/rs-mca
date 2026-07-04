# M1 a=327 pair-clear diverse rank-slack kernel repair

Status:

CANDIDATE / RANKSLACK_KERNEL_EIGHT_ROW_STABLE / PARTIAL / EXPERIMENTAL

This packet follows `3228415` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The five-row module audit identified an adjacent rank-slack chamber:

```text
base zero row classes = [7,8,10,12,16,17,18]
rank = 4
kernel nullity = 2
kernel projective basis =
  [[0,0,1,1,0,0], [1,16,3,0,14,11]]
```

This branch enumerates the full projective line in that 2D kernel:

```text
directions tested = 18
```

and checks active-row support and all 21 pair projections.

## Result

The kernel enumeration gives:

```text
pair-clear directions = 10
support-reduced directions = 1
nine-or-better directions = 0
coefficient-kernel directions = 0
```

The best pair-clear direction is:

```text
kernel coefficients = [1,2]
direction = [11,6,0,1,1,2]
projective direction = [1,16,0,14,14,11]
forced pair count = 0
zero row count = 8
zero row classes = [7,8,10,12,15,16,17,18]
active row count = 5
active row classes = [5,9,11,13,14]
```

This is exactly the support-reduced chamber audited in `3228415`.

The kernel also contains directions with more zero rows, but they break
pair-clear. For example, the basis direction:

```text
[0,0,1,1,0,0]
```

has 10 zero rows but 11 forced pairs. That explains why the raw kernel slack
does not immediately produce a stronger pair-clear chamber.

## Interpretation

The rank-slack 2D kernel is now exhausted:

- it can reproduce the eight-zero-row, five-active-row pair-clear chamber;
- it does not contain a pair-clear direction with nine or more zero rows;
- it does not contain a full coefficient kernel.

So the immediate rank-slack repair route is locally closed. The next
constructive move should not keep searching this same 2D kernel. It should look
for a different support-reduced chamber with either:

```text
rank-slack nullity >= 3
```

or:

```text
eight zero rows and inactive rank <=4
```

so there is still room to kill additional active rows while preserving
pair-clear projections.

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
- global obstruction outside the audited rank-slack kernel front

## Next Target

Move to:

```text
m1-a327-pairclear-deeper-rankslack-front
```

The scanner should prioritize profiles with:

```text
zero row count >= 8
inactive rank <= 4
```

or:

```text
kernel nullity >= 3
```

before running full projective scans. Use Python for the chamber search. Use
Macaulay2/Singular only for small module certificates. Sage should still wait
until a genuine pair-clear coefficient kernel or exact-lift proxy appears.
