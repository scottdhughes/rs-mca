# M1 a=327 pair-clear tail-pair projection repair

Status:

EXACT_EXTRACTION_NO_A327 / TAILPAIR_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL

This packet follows `8184509` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The row-span dependence mutation branch achieved the rank target:

```text
rank([6,7,8,14,17,18,19,20]) <= 4
```

but its best nullspace direction forced the tail pairs:

```text
P56, P57, P67
```

This branch reranks the same target-aware row-span search by pair-projection
failure pattern, prioritizing rank-slack kernels with fewer forced pairs and
fewer forced tail pairs.

## Search

The scanner covers:

```text
mutations generated = 640
candidate systems constructed = 1920
structural pass candidates = 1758
selected candidates = 357
basis profiles tested = 2856
target rows present profiles = 2024
extended rank-slack profiles = 112
tail candidates = 112
```

No rank-slack candidate is pair-clear:

```text
extended pair-clear profiles = 16
deep rank-slack repair profiles = 0
```

Forced-pair histograms among rank-slack candidates:

```text
forced pair count:
  3: 72
  4: 24
  6: 16

tail forced count:
  1: 24
  3: 88
```

The most common forced-pair patterns are:

```text
P56,P57,P67: 48
P24,P56,P57,P67: 24
P45,P46,P56: 24
P45,P46,P47,P56,P57,P67: 16
```

## Best Tail-Pair Repair

The best profile is:

```text
template = ninerow_P17_shear_c1_d1
mutation = P17_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 154466
basis = targetaware_0_1_2_3_4_13
basis class indices = [0,1,2,3,4,13]
basis support sizes = [142,142,142,142,142,68]
coefficient matrix shape = [18,6]
```

It keeps the row-span target:

```text
base rank = 4
base nullity = 2
extended rank = 4
extended nullity = 2
```

Its best nullspace direction is:

```text
direction = [0,0,1,1,2,0]
forced pair count = 3
forced pairs = [P45,P46,P56]
tail pairs cleared = [P57,P67]
```

So the repair moves the obstruction: it clears `P57` and `P67`, but still
forces `P56` and introduces `P45/P46`.

## Interpretation

This is progress inside the rank-dependent row-span basin, but not an
`a=327` candidate. The tail-pair obstruction is now localized:

```text
old best forced pairs = [P56,P57,P67]
new best forced pairs = [P45,P46,P56]
```

The next repair should not search broadly for row-span dependence. It should
co-design pair projections for witnesses 4, 5, and 6 while keeping the
extended eight-row set rank at most 4.

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
- global obstruction outside the tested tail-pair projection repair front

## Next Target

Natural next branch:

```text
m1-a327-pairclear-p45-p46-p56-codesign
```

Objective:

```text
keep rank([6,7,8,14,17,18,19,20]) <= 4
repair forced projections P45, P46, P56
preserve P57 and P67 clearance
```

Use Python/GF(17) first. Macaulay2 or Singular is useful only if the pair
projection repair becomes a small module certificate. Sage should wait until
there is a genuine pair-clear coefficient kernel or exact-lift proxy.
