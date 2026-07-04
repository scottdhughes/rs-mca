# M1 a=327 pair-clear slot row syzygy

Status:

CANDIDATE / PCSYZ_DIRECTION_REDUCE_ROWS / PARTIAL / EXPERIMENTAL

This packet follows `8ae0631` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous row-reduction checkpoint preserved pair-clear slots and reduced
the best unit-slot support:

```text
forced pair count = 0
slot nonzero rows = 11
coefficient rank/nullity = 6/0
```

This branch stops treating the proxy direction as only a coordinate slot. For
each retained pair-clear slot profile, it tests anchored projective directions:

```text
v = e_slot + a e_j
```

over `GF(17)`, and scores the active row support of `M v` while keeping all 21
pair projections nonzero. This is still a proxy/syzygy search. No Sage
`GF(17^32)` exact lift is attempted.

## Result

The bounded direction pass used:

```text
mutations generated = 48
candidate systems constructed = 144
structural-pass candidates = 138
structural-pass candidates analyzed = 24
structural-pass candidates skipped = 114
top classes = 14
random bases = 0
direction max extra coordinates = 1
basis profiles tested = 25854
slot profiles tested = 155124
pair-clear slot profiles = 126
pair-clear slot-kernel profiles = 0
direction profiles tested = 48
direction vectors tested = 3888
pair-clear direction profiles = 48
pair-clear direction-kernel profiles = 0
row-reduced direction profiles = 48
```

The best direction is:

```text
template = pcsyzygy_base_w1_c3_d1
mutation = base_w1_c3_d1
assignment = fiber_round_robin
basis = basisaware_1_4_7_8_9_10
anchor slot = 5
direction vector = [0,5,0,0,0,1]
direction weight = 2
forced pair count = 0
forced pairs = none
direction nonzero rows = 9
direction nonzero row classes = [0,2,3,5,6,11,12,14,15]
```

Relative to `8ae0631`:

```text
unit slot rows = 11
projective direction rows = 9
slot rows improved 11 -> 9
pair projections remain clear
direction kernels remain 0
```

The pair-projection scalars for the best direction are all nonzero:

```text
P12=9, P13=1, P14=10, P15=2, P16=11, P17=3
P23=9, P24=1, P25=10, P26=2, P27=11
P34=9, P35=1, P36=10, P37=2
P45=9, P46=1, P47=10
P56=9, P57=1, P67=9
```

## Interpretation

This is real local progress. The pair-clear obstruction remains solved, and
the active row support is no longer tied to a coordinate unit slot. Allowing a
two-term projective direction cuts the support from 11 rows to 9 rows.

The result is still not a proxy-positive kernel target:

```text
direction nonzero rows = 9
pair-clear direction-kernel profiles = 0
```

The active blocker is now a nine-row pair-clear direction system.

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
- failure outside this bounded pair-clear direction front

## Next Target

Move to:

```text
m1-a327-pairclear-direction-nine-row-repair
```

Target the nine active row classes directly:

```text
[0,2,3,5,6,11,12,14,15]
```

The next Python pass should preserve:

```text
direction vector = [0,5,0,0,0,1]
forced_pair_count = 0
```

while reducing:

```text
direction_nonzero_rows <= 8
```

or creating an actual direction kernel. If these nine rows stabilize under
local mutation, then Macaulay2 or Singular is appropriate for a small
module/syzygy check on this pinned row system. Sage should still wait until a
pair-clear direction-kernel proxy target exists.
