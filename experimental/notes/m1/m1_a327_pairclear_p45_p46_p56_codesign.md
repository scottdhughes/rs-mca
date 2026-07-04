# M1 a=327 pair-clear P45/P46/P56 codesign

Status:

EXACT_EXTRACTION_NO_A327 / P456_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL

This packet follows `e48c576` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The tail-pair projection repair moved the best rank-dependent kernel from:

```text
old forced pairs = [P56,P57,P67]
```

to:

```text
new forced pairs = [P45,P46,P56]
```

This branch directly targets those projections while preserving clearance of:

```text
P57, P67
```

It keeps the same extended row-span target:

```text
rank([6,7,8,14,17,18,19,20]) <= 4
```

and searches the rank-slack kernel with a target-specific objective:

```text
clear P45/P46/P56 first
preserve P57/P67 second
minimize total forced pair projections third
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

No candidate clears all target projections:

```text
exact pair-clear profiles = 0
target repaired profiles = 0
near repair profiles = 0
```

target forced-count histogram:

```text
1: 280
3: 40
```

Preserve forced-count histogram:

```text
0: 20
1: 10
2: 290
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
template = ninerow_W57_c13_pm1
mutation = W57_c13_pm1
assignment = fiber_round_robin
assignment seed = 193081
basis = targetaware_0_1_2_3_4_10
basis class indices = [0,1,2,3,4,10]
basis support sizes = [216,111,105,105,74,74]
coefficient matrix shape = [20,6]
```

It preserves the row-span target:

```text
base rank = 4
base nullity = 2
extended rank = 4
extended nullity = 2
```

Its best target-specific kernel direction is:

```text
direction = [0,0,0,1,0,2]
target pairs cleared = [P45,P56]
target pair still forced = P46
preserve pairs cleared = [P57]
preserve pair still forced = P67
forced pairs = [P14,P16,P17,P46,P47,P67]
```

## Interpretation

The P456 codesign search does not clear the target triple. It does show that
the obstruction can be moved:

```text
previous best forced pairs = [P45,P46,P56]
current best forced pairs includes only one target pair: P46
```

But this improvement costs `P67` and introduces extra forced pairs involving
witnesses 1 and 4:

```text
P14, P16, P17, P47
```

So the next useful target is not broad row-span search. It is a smaller
projection tradeoff:

```text
repair P46 and restore P67
while keeping P45 and P56 clear
```

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
- global obstruction outside the tested P45/P46/P56 codesign front

## Next Target

Natural next branch:

```text
m1-a327-pairclear-p46-p67-tradeoff-repair
```

Objective:

```text
keep rank([6,7,8,14,17,18,19,20]) <= 4
keep P45 and P56 clear
repair P46
restore P67
avoid introducing new forced P14/P16/P17/P47 projections
```

Use Python/GF(17) first. Macaulay2 or Singular is useful only if the projection
repair becomes a small module certificate. Sage should wait until there is a
genuine pair-clear coefficient kernel or exact-lift proxy.
