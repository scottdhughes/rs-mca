# M1 a=327 pair-clear P46/P67 tradeoff repair

Status:

EXACT_EXTRACTION_NO_A327 / P46P67_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL

This packet follows `c900d81` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The P45/P46/P56 codesign front reduced the target failure but introduced a
new tradeoff:

```text
previous best forced pairs = [P14,P16,P17,P46,P47,P67]
target pair still forced = P46
preserve pair still forced = P67
target pairs already clear = [P45,P56]
```

This branch directly targets:

```text
repair pairs = [P46,P67]
preserve clear pairs = [P45,P56]
spillover avoid pairs = [P14,P16,P17,P47]
```

It keeps the same extended row-span target:

```text
rank([6,7,8,14,17,18,19,20]) <= 4
```

and searches the rank-slack kernel with the objective:

```text
repair P46/P67 first
preserve P45/P56 second
avoid P14/P16/P17/P47 spillover third
minimize total forced pair projections fourth
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
basis profiles tested = 6850
target rows present profiles = 5010
extended rank-slack profiles = 320
```

No candidate repairs both `P46` and `P67` while preserving `P45/P56`:

```text
exact pair-clear profiles = 0
tradeoff repaired profiles = 0
clean tradeoff repaired profiles = 0
near repair profiles = 0
```

Repair forced-count histogram:

```text
1: 290
2: 30
```

Preserve forced-count histogram:

```text
0: 10
1: 270
2: 40
```

Spillover forced-count histogram:

```text
0: 280
1: 20
2: 10
4: 10
```

Most common forced-pair patterns:

```text
P56,P57,P67: 180
P24,P56,P57,P67: 90
P45,P46,P47,P56,P57,P67: 20
P14,P15,P16,P45,P46,P56: 10
P14,P16,P17,P46,P47,P67: 10
P45,P46,P56: 10
```

## Best Profile

The best profile is:

```text
template = ninerow_P14_shear_c1_d1
mutation = P14_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 162526
basis = targetaware_0_1_2_3_4_13
basis class indices = [0,1,2,3,4,13]
basis support sizes = [142,142,142,142,105,68]
coefficient matrix shape = [20,6]
```

It preserves the row-span target:

```text
base rank = 4
base nullity = 2
extended rank = 4
extended nullity = 2
```

Its best tradeoff kernel direction is:

```text
direction = [0,1,1,2,0,0]
repair pairs cleared = [P46]
repair pair still forced = P67
preserve pairs cleared = [P45]
preserve pair still forced = P56
spillover pairs cleared = [P14,P16,P17,P47]
forced pairs = [P56,P57,P67]
```

## Interpretation

The P46/P67 tradeoff search removes the new witness-1/4 spillover from the
P456 best profile, but it returns to the older tail obstruction:

```text
current best forced pairs = [P56,P57,P67]
```

So the obstruction cycles between two small fronts:

```text
tail front: P56/P57/P67
mixed front: P46/P67 with P45/P56 preservation pressure
```

The tested rank-slack row-span kernel family does not co-design both fronts in
one direction.

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
- global obstruction outside the tested P46/P67 tradeoff front

## Next Target

Natural next branch:

```text
m1-a327-pairclear-cyclic-tail-mixed-obstruction
```

Objective:

```text
formalize the observed two-front cycle:
  [P56,P57,P67] <-> [P14,P16,P17,P46,P47,P67]
inside the tested rank-slack row-span family
```

If continuing constructively instead, the next search should not simply rerank
the same nullity-2 kernels. It should add a new degree of freedom that can
break the tail/mixed tradeoff without losing the extended rank-slack target.
