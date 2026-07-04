# M1 a=327 pair-clear support augmentation search

Status:

EXACT_EXTRACTION_NO_A327 / SUPPORTAUG_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL

This packet follows `7076965` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The target-basis exchange fronts expanded the rank-slack family but did not
break the cyclic pair-clear obstruction. This branch changes the zero target
itself before basis selection:

```text
add one non-target support class to the extended zero target
then construct bases excluding the augmented zero set
```

The base extended target remains:

```text
zero classes = [6,7,8,14,17,18,19,20]
```

and the augmented target is:

```text
[6,7,8,14,17,18,19,20] + one support class
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
basis profiles tested = 10852
target rows present profiles = 7948
extended rank-slack profiles = 152
```

Support augmentation narrows the rank-slack front:

```text
two-target basis rank-slack profiles = 640
support-augmented rank-slack profiles = 152
```

but it still does not produce a pair-clear or cycle-pressure-reduced profile:

```text
exact pair-clear profiles = 0
cycle pressure reduced profiles = 0
```

Augmentation class counts among rank-slack profiles:

```text
0: 128
1: 16
2: 8
```

Cycle forced-count histogram:

```text
3: 116
5: 8
6: 28
```

Front return counts:

```text
tail front = 124
P456 front = 32
mixed front = 12
```

Most common forced-pair patterns:

```text
P56,P57,P67: 72
P24,P56,P57,P67: 36
P45,P46,P47,P56,P57,P67: 16
P14,P16,P17,P46,P47,P67: 12
P14,P15,P16,P45,P46,P56: 8
P45,P46,P56: 8
```

## Best Profile

The best profile is:

```text
template = ninerow_P17_shear_c1_d1
mutation = P17_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 164466
basis = supportaug_0_1_2_3_4_5_13
basis class indices = [1,2,3,4,5,13]
support augmentation class = 0
augmented zero classes = [0,6,7,8,14,17,18,19,20]
basis support sizes = [142,142,142,142,105,68]
coefficient matrix shape = [18,6]
```

It preserves rank slack:

```text
extended rank = 4
extended nullity = 2
```

Its best augmented-target kernel direction is:

```text
direction = [0,1,1,2,0,0]
forced pairs = [P45,P46,P56]
cycle pairs cleared = [P14,P16,P17,P47,P57,P67]
```

So the best support-augmentation profile still returns to the P456 front.

## Interpretation

Adding one support class before basis selection is a real target change, not a
nullspace rerank. It cuts the rank-slack front down to 152 profiles but does
not reduce the pair-clear cycle pressure. The best profile remains:

```text
best forced pairs = [P45,P46,P56]
```

This strengthens the local diagnosis: the rank-slack basis-exchange/support-
augmentation basin is not breaking the cyclic tail/P456/mixed obstruction.

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
- global obstruction outside the tested support-augmentation front

## Next Target

Leave this local rank-slack basin.

The next constructive move should return to a higher-level template/hypergraph
search where the cyclic pair-clear obstruction is a hard guard during
candidate generation, not a post-hoc nullspace repair target.
