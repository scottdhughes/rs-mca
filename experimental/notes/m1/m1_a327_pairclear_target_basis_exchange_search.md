# M1 a=327 pair-clear target-basis exchange search

Status:

EXACT_EXTRACTION_NO_A327 / TARGETBASIS_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL

This packet follows `fa084a3` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The cyclic tail/mixed audit showed that pure nullity-2 kernel reranking cycles
between:

```text
[P56,P57,P67]
[P45,P46,P56]
[P14,P16,P17,P46,P47,P67]
```

This branch changes the basis model instead of only changing the objective.
It allows exactly one target zero class into the coefficient basis and imposes
that target zero condition as a unit coordinate row.

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
basis profiles tested = 10960
target rows present profiles = 8016
extended rank-slack profiles = 512
```

The target-basis model increases the rank-slack front:

```text
previous rank-slack profiles = 320
target-basis rank-slack profiles = 512
```

but it does not produce a pair-clear direction:

```text
exact pair-clear profiles = 0
cycle pressure reduced profiles = 0
```

Cycle forced-count histogram:

```text
3: 448
5: 16
6: 48
```

Front return counts:

```text
tail front = 464
P456 front = 64
mixed front = 16
```

Most common forced-pair patterns:

```text
P56,P57,P67: 288
P24,P56,P57,P67: 144
P45,P46,P47,P56,P57,P67: 32
P14,P15,P16,P45,P46,P56: 16
P14,P16,P17,P46,P47,P67: 16
P45,P46,P56: 16
```

## Best Profile

The best profile is:

```text
template = ninerow_P17_shear_c1_d1
mutation = P17_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 164466
basis = targetbasis_6_0_1_2_4_5_6
basis class indices = [0,1,2,4,5,6]
target basis class = 6
augmented basis zero classes = [6]
basis support sizes = [142,142,142,142,105,74]
coefficient matrix shape = [19,6]
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

So the best target-basis exchange returns to the P456 front.

## Interpretation

Putting one target class into the basis is a real model change and does create
more rank-slack profiles. However, the pair-clear obstruction remains in the
same local cycle:

```text
target-basis exchange best = [P45,P46,P56]
```

The tested exchange front does not break the tail/mixed conservation pattern.

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
- global obstruction outside the tested target-basis exchange front

## Next Target

Do not continue by only widening the one-target basis exchange.

The next constructive move should add a different degree of freedom, such as:

```text
two-target basis exchange with a bounded front, or
support-class augmentation before basis selection, or
return to the higher-level template/hypergraph line with the cyclic pair-clear
feedback as a guard
```

If the next branch is proof-oriented, convert the cyclic front plus the
target-basis exchange into a small GF(17) matroid/module obstruction packet.
