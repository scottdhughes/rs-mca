# M1 a=327 collapse-quotient line search

Status: `TESTED_QUOTIENT_LINES_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `8dbcb6b`, which showed that the high-performing soft
target systems have large quotient spaces but that the best sampled behavior is
still collapse-only.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

For each high-performing soft target core, the scanner extracts collapse
anchors `c` from the collapse subspace and quotient directions `q` from the
target nullspace quotient. It then evaluates affine lines

```text
c + lambda q
```

over `GF(12289)` for a fixed set of 32 nonzero lambda values. Candidate line
specs are also replayed over the other four proxy primes when the same
free-column direction exists.

This is a proxy search only. A public proof record still requires exact
`GF(17^32)` reconstruction and Sage verification.

## Result

The bounded first pass tested:

- 2 high-performing soft target cores;
- 6 collapse anchors;
- 32 ranked quotient directions;
- 3,072 lambda values over `GF(12289)`;
- top-line capacity/collapse replay over four additional proxy primes.

No proxy line candidate reached the `a=327` threshold. The best line result was:

```text
best capacity upper bound = 403
best proxy max-min = 259
best six-class dominance = 2
best failure mode = LINE_LOW_RESCHEDULE
```

This is a useful tradeoff signal. Unlike the earlier quotient samples, affine
lines from collapse anchors can preserve substantial capacity while reducing
the `[1,3,4,5,6,7]` dominance from `359` to `2`. But the received-word
rescheduler loses too much balance, landing at max-min `259`.

Failure-mode counts for the primary line sweep were:

```text
LINE_REDUCED_CAPACITY_UNSCHEDULED 3072
LINE_LOW_RESCHEDULE                 96
```

Here `LINE_REDUCED_CAPACITY_UNSCHEDULED` is the cheap pre-rescheduler screen:
the line has capacity at least `327` and lower six-class dominance, so the best
lambda for each anchor/direction is then rescheduled exactly. Those exact
reschedules all failed below `327`.

No exact `GF(17^32)` audit was triggered.

## Status labels

`CANDIDATE` means a proxy line candidate reaches `a>=327` with six-class
dominance below the collapse anchor and needs exact `GF(17^32)` extraction.

`TESTED_QUOTIENT_LINES_NO_A327` means the bounded affine line sweep found no
collapse-reduced proxy `a>=327` candidate.

`PARTIAL` means broader quotient directions, lambda sweeps, two-dimensional
planes, and exact-field extraction remain open.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
