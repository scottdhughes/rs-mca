# M1 a=327 reserve-pairclass co-design before split

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `c7eed3e`, where upstream buffering improved the local
post-split basin but did not clear the two active thresholds:

```text
best post-split capacity      = 322
best post-split pair B values = [1024,608,608,1024,1024]
post capacity deficit         = 5
B27/B37 deficits              = 46 / 46
```

The live question was whether pre-split rows can be selected by their
post-split value, rather than by raw pre-split capacity alone.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Method

The audit starts from the same scalable pair-class extension-96 base system as
the high-buffer packet and adds co-designed pre-split rows from five families:

```text
pair27_37_plus_capacity
pair27_37_plus_57_guard
quotient_fiber_buffer
mixed_buffer_pairclass
postsplit_survivor_rows
```

The requested extension sizes are:

```text
64, 96, 128, 160
```

For each candidate row, the audit records a heuristic delta ledger:

```text
pre/post capacity delta
pre/post B({2,7}) delta
pre/post B({3,7}) delta
pre/post B({5,7}) delta
quotient fiber
```

Each retained exact system is solved by a pivot-row subset schedule over
`GF(17^32)`, evaluated directly on `H`, then re-solved and re-evaluated after
the known split:

```text
split_6_keep1457 at coordinate 1
```

The pivot-row subset schedule is a search schedule, not a certificate that the
full overdetermined target system is solved. The produced vectors are still
evaluated exactly as candidate codeword tuples over `GF(17^32)`.

## Result

The bounded audit produced:

```text
systems tested:                         20
timeouts:                               14
pre-split exact vectors:                 6
post-split exact vectors:                6
post-split capacity-preserving vectors:  1
post-split pairclass-repaired vectors:   0
post-split pair57-preserving vectors:    6
collapse-reduced vectors:                6
```

Best retained row:

```text
row family         = quotient_fiber_buffer
row extension size = 96
pre-split capacity = 402
post-split capacity = 329
post-split pair B values = [1024,641,640,1024,1024]
post-split collapse = [[1,4,5,7],[6],[3],[2]]
capacity loss = 73
failure mode = RESERVE_NOT_CREATED
```

Failure count:

```text
RESERVE_NOT_CREATED: 6
CODESIGN_TIMEOUT:    14
```

## Interpretation

This is a genuine improvement over `c7eed3e`.

The previous high-buffer best was:

```text
post-split capacity      = 322
post-split B27/B37       = 608/608
```

The co-designed best is:

```text
post-split capacity      = 329
post-split B27/B37       = 641/640
```

So the co-design selector cleared the post-split capacity threshold while
preserving the reduced-collapse pattern and the `{5,7}` guard. The remaining
deficit is now concentrated in the pairclass Hall targets:

```text
target B27/B37 = 654/654
current best   = 641/640
remaining gap  = 13 / 14
```

The pre-split reserve target `430` was not reached:

```text
best pre-split capacity = 402
```

But the practical post-split capacity barrier did move:

```text
322 -> 329
```

That means the local basin is not exhausted. The new bottleneck is no longer
capacity alone; it is a small remaining B27/B37 pairclass deficit in a
post-split capacity-preserving, pair57-preserving, collapse-reduced exact
geometry.

The timeout count keeps the result partial. In particular, the larger
extension sizes mostly did not complete under the bounded per-case timeout.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means this named reserve/pairclass co-design pass
found no exact `a>=327` witness.

`PARTIAL` means larger row extensions, tighter pairclass-only refinements, and
alternate exact solve schedules remain open.

## Failure labels

- `RESERVE_NOT_CREATED`: pre-split capacity stays below the conservative
  reserve target `430`.
- `RESERVE_NOT_POSTSPLIT_SURVIVING`: pre-split reserve exists, but the split
  consumes it and post-split capacity falls below `327`.
- `PAIRCLASS_NOT_CREATED`: post-split B27/B37 remain below `654`.
- `PAIR57_GUARD_LOSS`: post-split `B({5,7})` falls below `654`.
- `COLLAPSE_RETURNS`: capacity or pair repair appears only by recreating
  collapse.
- `LOW_RESCHEDULE`: post capacity and pair guards clear, but exact max-min
  remains below `327`.
- `EXACT_CANDIDATE`: exact max-min reaches at least `327`.

## Non-claims

- No `a=327` interleaved-list certificate.
- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No public-row update.

## Next target

The next constructive move should be very narrow:

```text
start from the post-split capacity-preserving 96-row quotient-fiber buffer
geometry and add a small B27/B37-only repair layer worth about 13/14 pair
credits, while preserving capacity >=327 and B57 >=654.
```

This is more promising than a broad conservation note now, because the
co-design branch broke the post-split capacity wall and left a small,
quantified pairclass deficit.
