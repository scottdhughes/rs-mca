# M1 a=327 pair-clear row17 dependence codesign

Status:

CANDIDATE / ROW17_DEPENDENCE_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL

This packet follows `811019a` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The seven-to-eight repair showed that adding row class `17` to the best
seven-zero rank-slack chamber is pair-clear but raises inactive rank from 4 to
5. This branch searches for profiles where the row geometry is already
co-designed so that row class `17` lies in the inactive span of:

```text
[6,7,8,14,18,19,20]
```

The target extended zero set is:

```text
[6,7,8,14,17,18,19,20]
```

The test is algebraic over `GF(17)`: no full projective chamber enumeration is
needed. For each candidate/profile, compute the rank/nullity of the base and
extended row sets, then search the extended nullspace for a pair-clear
direction.

## Search

The scanner covers:

```text
mutations generated = 240
candidate systems constructed = 720
structural pass candidates = 681
selected candidates = 233
basis profiles tested = 1398
target rows present profiles = 253
```

The row17 dependence screen reports:

```text
base rank-slack profiles = 12
base pair-clear profiles = 12
row17 dependent profiles = 175
extended rank-slack profiles = 0
extended pair-clear profiles = 14
extended rank-slack pair-clear profiles = 0
deep rank-slack repair profiles = 0
```

Failure counts:

```text
ROW17_DEPENDENCE_TARGET_ROWS_MISSING: 1145
ROW17_DEPENDENCE_BASE_NOT_RANKSLACK: 241
ROW17_DEPENDENCE_SUPPORT_ONLY: 12
```

## Best Profile

The best profile is:

```text
template = ninerow_w3_c3_d1
mutation = w3_c3_d1
assignment = fiber_round_robin
assignment seed = 119186
basis = basisaware_0_1_2_3_4_10
basis class indices = [0,1,2,3,4,10]
basis support sizes = [216,179,148,142,111,74]
coefficient matrix shape = [15,6]
```

Base seven-row chamber:

```text
zero classes = [6,7,8,14,18,19,20]
inactive rank = 4
inactive kernel nullity = 2
pair-clear direction = [1,9,6,6,1,6]
active classes = [5,9,11,12,13,15,16,17]
```

Extended row17 chamber:

```text
zero classes = [6,7,8,14,17,18,19,20]
inactive rank = 5
inactive kernel nullity = 1
pair-clear direction = [1,0,14,6,1,6]
active classes = [5,9,11,12,13,15,16]
```

## Interpretation

This is not the desired deep repair. The search found support-only variants:
row class `17` can be included while preserving pair-clear, but every such
profile raises inactive rank to 5. No tested profile kept:

```text
zero classes [6,7,8,14,17,18,19,20]
inactive rank <= 4
pair-clear direction nonempty
```

This sharpens the obstruction from "can we add row17?" to:

```text
can row17 be made dependent on the rank-4 inactive span while pair projections
stay nonzero?
```

The tested codesign front did not achieve that.

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
- global obstruction outside the tested row17 dependence codesign front

## Next Target

The next branch should stop treating row17 as a single row addition and instead
engineer the row span itself.

Natural next branch:

```text
m1-a327-pairclear-rowspan-dependence-mutation
```

Objective:

```text
force a linear dependence among row classes [6,7,8,14,17,18,19,20]
with rank <= 4,
while preserving a pair-clear kernel direction.
```

Use Python/GF(17) for row-space mutation and rank tests first. Use
Macaulay2/Singular only if a small module certificate appears. Sage should wait
until there is a genuine pair-clear coefficient kernel or exact-lift proxy.
