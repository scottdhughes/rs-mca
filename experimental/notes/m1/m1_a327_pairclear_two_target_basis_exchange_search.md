# M1 a=327 pair-clear two-target basis exchange search

Status:

EXACT_EXTRACTION_NO_A327 / TWOTARGETBASIS_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL

This packet follows `b84b4ca` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The one-target basis exchange increased the rank-slack front but still returned
to the P456 obstruction. This branch tests the next bounded basis-model change:

```text
exactly two target zero classes may enter the coefficient basis
both target zero conditions are imposed as unit coordinate rows
```

The extended target remains:

```text
zero classes = [6,7,8,14,17,18,19,20]
rank guard = <=4
```

## Search

The scanner covers all available mutation specs and three assignment seed
offsets:

```text
mutations generated = 646
seed offsets = 3
candidate systems constructed = 5814
structural pass candidates = 5328
selected candidates = 685
basis profiles tested = 13700
target rows present profiles = 10020
extended rank-slack profiles = 640
```

The two-target model further increases the rank-slack front:

```text
one-target rank-slack profiles = 512
two-target rank-slack profiles = 640
```

but it still does not produce a pair-clear or cycle-pressure-reduced profile:

```text
exact pair-clear profiles = 0
cycle pressure reduced profiles = 0
```

Cycle forced-count histogram:

```text
3: 560
5: 20
6: 60
```

Front return counts:

```text
tail front = 580
P456 front = 80
mixed front = 20
```

Most common forced-pair patterns:

```text
P56,P57,P67: 360
P24,P56,P57,P67: 180
P45,P46,P47,P56,P57,P67: 40
P14,P15,P16,P45,P46,P56: 20
P14,P16,P17,P46,P47,P67: 20
P45,P46,P56: 20
```

## Best Profile

The best profile is:

```text
template = ninerow_P17_shear_c1_d1
mutation = P17_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 164466
basis = twotargetbasis_6_7_0_1_2_4_6_7
basis class indices = [0,1,2,4,6,7]
target basis classes = [6,7]
augmented basis zero classes = [6,7]
basis support sizes = [142,142,142,142,74,74]
coefficient matrix shape = [20,6]
```

It preserves the row-span target:

```text
base rank = 4
base nullity = 2
extended rank = 4
extended nullity = 2
```

Its best exchange kernel direction is:

```text
direction = [0,0,1,2,0,0]
forced pairs = [P45,P46,P56]
cycle pairs cleared = [P14,P16,P17,P47,P57,P67]
```

So the best two-target basis exchange also returns to the P456 front.

## Interpretation

The two-target basis exchange is a genuine basis-model expansion. It raises the
rank-slack count from 512 to 640, but it does not reduce the pair-clear cycle
pressure. The same obstruction pattern remains:

```text
best forced pairs = [P45,P46,P56]
```

The tested two-target exchange front does not break the tail/P456/mixed cycle.

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
- global obstruction outside the tested two-target basis exchange front

## Next Target

Do not continue by only widening target-basis exchange.

The next constructive branch should leave this rank-slack basis-exchange basin
and return to the higher-level template/hypergraph line with pair-clear cycle
feedback as a hard guard, or explicitly add support-class augmentation before
basis selection.
