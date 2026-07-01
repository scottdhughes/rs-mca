# M1 a=327 high-buffer pairclass before split

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `0f2655a`, where one- and two-row compensated
split-and-replace moves preserved the pair gains and reduced collapse but never
restored capacity:

```text
pre-split pair B values  = [1024,577,576,1024,1024]
pre-split capacity       = 384
post-split pair B values = [1024,593,592,1024,1024]
post-split capacity      = 315
capacity loss            = 69
```

The live question was whether the pair-class system can be strengthened before
the split, so that the known capacity loss still leaves capacity at least
`327`.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Method

The audit starts from the scalable pair-class extension-96 base system and
adds pre-split buffer rows from five families:

```text
pair57_buffer
all_capacity_buffer
pair27_37_plus_capacity
quotient_fiber_buffer
mixed_buffer
```

The buffer budgets are:

```text
32, 64, 96, 128
```

For each buffer system, the audit solves an exact pivot-row subset over
`GF(17^32)`, evaluates the resulting vector directly on `H`, then applies the
known split:

```text
split_6_keep1457 at coordinate 1
```

The pivot-row subset schedule is a search schedule, not a certificate that the
full overdetermined target system is solved. The candidate vectors are still
evaluated exactly as seven codeword tuples over `GF(17^32)`.

## Result

The 20-case bounded audit produced:

```text
systems tested:                         20
timeouts:                               9
pre-split exact vectors:                11
post-split exact vectors:               11
pre-split capacity-buffer vectors:       0
post-split capacity-preserving vectors:  0
```

Best retained row:

```text
pre-split capacity       = 393
post-split capacity      = 322
post-split pair B values = [1024,608,608,1024,1024]
post-split collapse      = [[1,4,5,7],[6],[3],[2]]
failure mode             = BUFFER_NOT_CREATED
```

Failure count:

```text
BUFFER_NOT_CREATED: 11
HIGH_BUFFER_TIMEOUT: 9
```

The best completed case is:

```text
buffer rows   = 64
buffer family = pair27_37_plus_capacity
pre capacity  = 393
post capacity = 322
B27/B37       = 608/608
```

## Interpretation

This branch moved the pre-split pair values and the post-split capacity in the
right direction:

```text
B27/B37 after split: 593/592 -> 608/608
post-split capacity: 315 -> 322
```

But it did not create the intended upstream reserve:

```text
pre-split capacity target = 420
best pre-split capacity   = 393
```

It also did not clear the final capacity threshold:

```text
post-split target capacity = 327
best post-split capacity   = 322
```

So this exact pass does not produce an `a>=327` witness. It does show that
pair-class-plus-buffer rows can improve the local basin, but the available
buffer in this schedule remains too small by about five post-split capacity
units and about twenty-seven pre-split buffer units.

The timeout count keeps the result partial. Larger buffer systems and different
upstream target systems remain open, but this named bounded pass found no exact
certificate.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means this named high-buffer pairclass pass found no
exact `a>=327` witness.

`PARTIAL` means broader upstream target redesign, larger buffer schedules, and
different exact solve schedules remain open.

## Failure labels

- `BUFFER_NOT_CREATED`: pre-split capacity stays below the `420` reserve
  target.
- `BUFFER_CREATES_COLLAPSE`: capacity reserve appears only with unacceptable
  collapse.
- `BUFFER_KILLS_PAIR27_37`: capacity reserve destroys the `{2,7}` / `{3,7}`
  pair-class gains.
- `SPLIT_CONSUMES_BUFFER`: reserve exists, but the split still drops capacity
  below `327`.
- `SPLIT_PAIR57_LOSS`: split destroys the `{5,7}` guard.
- `SPLIT_LOW_RESCHEDULE`: capacity and pair guards survive, but exact max-min
  remains below `327`.
- `HIGH_BUFFER_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

This bounded high-buffer pass almost reaches post-split capacity:

```text
best post-split capacity = 322
target                  = 327
```

The next useful branch should either test a more aggressive upstream
capacity-reserve construction or write a local-basin conservation note
summarizing the observed tradeoff:

```text
pair-class growth and collapse reduction are possible,
but the tested extension-96 buffer schedule cannot create enough reserve before
the split.
```
