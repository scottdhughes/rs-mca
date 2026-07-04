# M1 a=327 pair-clear deeper rank-slack front

Status:

CANDIDATE / DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY / PARTIAL / EXPERIMENTAL

This packet follows `ced3433` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous rank-slack kernel repair showed that the immediate 2D kernel
adjacent to the `w2_c0_d1` five-row chamber is exhausted:

```text
directions tested = 18
pair-clear directions = 10
support-reduced directions = 1
nine-or-better directions = 0
coefficient-kernel directions = 0
```

This branch searches a broader front for a stronger chamber with:

```text
zero row count >= 8
inactive rank <= 4
```

That is the useful target because it would combine eight killed rows with
additional inactive nullity, leaving room to remove more active rows while
preserving all 21 pair projections.

## Search

The scanner covers:

```text
mutations generated = 160
candidate systems constructed = 480
structural pass candidates = 459
diverse candidates selected = 36
sampled profiles = 108
sample directions per profile = 75000
sample pair-clear directions = 1821587
full profiles scanned = 4
full directions tested = 6034392
full pair-clear directions = 1441440
```

The sampled screen found many support-reduced fronts but no deeper rank-slack
front:

```text
sample deep rank-slack profiles = 0
sample failure counts =
  DCHAMBER_SAMPLE_SUPPORT_REDUCED: 54
  DCHAMBER_SAMPLE_LOWER_SUPPORT: 19
  DCHAMBER_SAMPLE_NINE_ROW: 19
  DCHAMBER_SAMPLE_RANK_SLACK: 16
```

All four full projective scans confirmed support-reduced chambers:

```text
full direct support-reduced profiles = 4
full rank-slack profiles = 4
full support-reduced extension profiles = 4
full deep rank-slack profiles = 0
```

## Best Full Profile

The best full profile is:

```text
template = ninerow_w3_c3_d1
mutation = w3_c3_d1
assignment = fiber_round_robin
assignment seed = 117186
basis = basisaware_0_1_2_3_5_10
basis class indices = [0,1,2,3,5,10]
basis support sizes = [216,179,148,142,111,74]
coefficient matrix shape = [15,6]
```

Its best direct support-reduced chamber has:

```text
direction = [1,0,14,6,11,6]
zero row count = 8
zero row classes = [6,7,8,14,17,18,19,20]
inactive rank = 5
inactive kernel nullity = 1
active row count = 7
active row classes = [4,9,11,12,13,15,16]
```

Its best rank-slack chamber has:

```text
direction = [1,4,1,6,11,6]
zero row count = 7
zero row classes = [6,7,8,14,18,19,20]
inactive rank = 4
inactive kernel nullity = 2
active row count = 8
active row classes = [4,9,11,12,13,15,16,17]
```

## Interpretation

The deeper front did not find the desired combination:

```text
zero row count >= 8
inactive rank <= 4
```

The result is still useful. It confirms that support-reduced chambers are not
isolated to the earlier `w2_c0_d1` packet, but in this tested broader front the
eight-zero chambers still have inactive rank 5, while inactive-rank-4 chambers
drop to seven zero rows.

So the current obstruction is not pair-clear support alone. It is the coupling
between:

```text
eight zero rows
rank-slack nullity
pair-clear projections
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
- global obstruction outside the tested deeper rank-slack front

## Next Target

Do not immediately rerun the same broad chamber search. The next useful branch
should audit one of the support-reduced-only chambers, or search specifically
for a local move that converts the best seven-zero rank-slack chamber into an
eight-zero chamber without raising inactive rank.

The natural branch is:

```text
m1-a327-pairclear-rankslack-seven-to-eight-repair
```

Start from the best `w3_c3_d1` full profile and focus on the adjacent pair:

```text
seven-zero rank-slack chamber:
  zero classes = [6,7,8,14,18,19,20]
  inactive rank = 4
  nullity = 2

eight-zero support-reduced chamber:
  zero classes = [6,7,8,14,17,18,19,20]
  inactive rank = 5
  nullity = 1
```

The question is whether row class `17` can be added to the zero set while
keeping pair-clear and inactive rank at most 4.
