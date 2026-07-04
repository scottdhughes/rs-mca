# M1 a=327 pair-clear row-span dependence mutation

Status:

EXACT_EXTRACTION_NO_A327 / ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL / PARTIAL / EXPERIMENTAL

This packet follows `8613e96` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The row17 dependence codesign branch found support-only profiles: adding row
class `17` could preserve pair-clear, but inactive rank rose to 5. This branch
changes the basis search itself. It uses target-aware bases that keep:

```text
[6,7,8,14,17,18,19,20]
```

out of the basis whenever possible, so the full eight-row span can be tested
directly.

The target is:

```text
rank([6,7,8,14,17,18,19,20]) <= 4
and pair-clear kernel nonempty
```

## Search

The scanner covers:

```text
mutations generated = 640
candidate systems constructed = 1920
structural pass candidates = 1758
selected candidates = 357
basis profiles tested = 2856
target rows present profiles = 2024
```

Result:

```text
base rank-slack profiles = 120
base pair-clear profiles = 8
extended rank-slack profiles = 112
extended pair-clear profiles = 16
extended rank-slack pair-clear profiles = 0
deep rank-slack repair profiles = 0
```

Failure counts:

```text
ROWSPAN_BASE_NOT_RANKSLACK: 1896
ROWSPAN_RANK_DEPENDENT_PAIRCLEAR_FAIL: 112
ROWSPAN_SUPPORT_ONLY: 16
ROWSPAN_TARGET_ROWS_MISSING: 832
```

## Best Rank-Dependent Profile

The best rank-dependent profile is:

```text
template = ninerow_P14_shear_c1_d1
mutation = P14_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 152526
basis = targetaware_0_1_2_3_4_11
basis class indices = [0,1,2,3,4,11]
basis support sizes = [142,142,142,142,105,74]
coefficient matrix shape = [20,6]
```

It achieves the row-span target:

```text
base rank = 4
base nullity = 2
extended rank = 4
extended nullity = 2
```

But the best direction in the extended nullspace is not pair-clear:

```text
direction = [0,1,1,2,0,1]
forced pair count = 3
forced pairs = [P56,P57,P67]
```

So this branch succeeds at row-span dependence but fails at pair projection
clearance.

## Interpretation

This is a sharper obstruction than the previous row17 branches. The row-span
part is no longer the main blocker: 112 tested profiles have the full extended
eight-row set at rank at most 4. The new blocker is that the rank-dependent
kernel forces pair projections, especially the tail pairs involving witnesses
5, 6, and 7.

In short:

```text
row-span dependence achieved
pair-clear kernel not achieved
```

The next move should target the three forced tail pairs directly, not rerun a
generic row-span search.

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
- global obstruction outside the tested row-span dependence mutation front

## Next Target

Natural next branch:

```text
m1-a327-pairclear-tailpair-projection-repair
```

Objective:

```text
keep rank([6,7,8,14,17,18,19,20]) <= 4
and repair the forced tail pairs P56, P57, P67
```

Use Python/GF(17) first. Macaulay2 or Singular is useful only if the tail-pair
projection repair becomes a small module certificate. Sage should wait until
there is a genuine pair-clear coefficient kernel or exact-lift proxy.
