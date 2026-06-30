# M1 a=327 witness-7 pair protected local exchange

Status: `CANDIDATE / SAGE_PENDING / PARTIAL / EXPERIMENTAL`

This packet follows `ad2ed83`. The stage-2 rebuild/refill scan regressed from
the stage-1 witness-7 pair repair incumbent, so this branch preserves the
stage-1 pair repair rows and mutates only the unprotected complement.

## Baseline

Stage-1 witness-7 pair repair from `8669680`:

```text
proxy max-min:              315
capacity upper bound:       455
pair B values:              [631,631,631,631,631]
pair deficit to 654:        [23,23,23,23,23]
added six-class dominance:  0
```

Stage-2 rebuild/refill from `ad2ed83`:

```text
proxy max-min:              314
pair B values:              [628,628,628,628,628]
pair deficit to 654:        [26,26,26,26,26]
```

The live target was to preserve the rows responsible for the `631` pair floor
and add the remaining `23` pair credits without reintroducing the six-witness
collapse class.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is a proxy-field search over `GF(12289)`. It is not a `GF(17^32)` proof
record.

## Method

The scanner reconstructs the best stage-1 target system and marks its
`pair7_repair` rows as protected. It removes only unprotected skeleton rows,
adds local witness-7 repair rows, and refills from non-removed skeleton rows
when needed.

Exchange budgets:

```text
8, 16, 24, 32, 48
```

Exchange moves:

```text
one_for_one
two_for_one
one_for_two
fiber_local
balanced_five_pair
residual_patch
```

The scan records:

- whether protected rows are preserved;
- proxy max-min;
- capacity upper bound;
- `B({1,7}),...,B({5,7})`;
- old three-subset guard values;
- total and added six-class dominance.

## Result

First bounded protected exchange run:

```text
base systems:       1
target systems:     30
proxy samples:      480
proxy candidates:   2
```

Best retained sample:

```text
exchange move:                 one_for_two
exchange budget:               48
proxy max-min:                 335
agreement vector:              [335,335,335,335,335,335,336]
capacity upper bound:          461
pair B values:                 [671,671,671,671,671]
pair Hall bound:               335
remaining pair deficit:        [-17,-17,-17,-17,-17]
added six-class dominance:     0
failure mode:                  PROTECTED_EXCHANGE_PROXY_CANDIDATE
```

The best target system preserves all protected stage-1 repair rows:

```text
protected row count:      16
removed unprotected rows: 48
new repair rows:          48
refill rows:              0
target row count:         640
```

## Interpretation

This is a proxy candidate, not a proof record.

The protected exchange did what the stage-2 rebuild did not: it preserved the
stage-1 pair repair and then cleared the pair Hall bottleneck without adding
six-class dominance.

Compared with the stage-1 incumbent:

```text
proxy max-min:        315 -> 335
pair B:               631 -> 671
remaining deficit:     23 -> -17
capacity:             455 -> 461
added collapse:         0 -> 0
```

The next step is exact extraction over `GF(17^32)` for the protected-exchange
proxy candidates. The proxy vector is not a certificate over the actual row
field and does not update any public row.

## Status labels

`CANDIDATE` means the proxy protected exchange reaches `a>=327` and needs
exact `GF(17^32)` extraction.

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`PARTIAL` means exact lifting and broader protected-exchange neighborhoods
remain open.

## Failure labels

- `PROTECTED_EXCHANGE_NOT_REPAIRED`: some `B({i,7})` remains below `654`.
- `PROTECTED_EXCHANGE_REGRESSES_PAIR7`: the exchange loses part of the
  protected pair repair.
- `PROTECTED_EXCHANGE_COLLAPSE_RETURNS`: pair repair improves only by adding
  six-class dominance.
- `PROTECTED_EXCHANGE_CAPACITY_LOSS`: pair repair improves but capacity drops
  below `327`.
- `PROTECTED_EXCHANGE_LOW_RESCHEDULE`: pair Hall clears but proxy max-min
  remains below `327`.
- `PROTECTED_EXCHANGE_PROXY_CANDIDATE`: proxy max-min reaches at least `327`
  with low/no added collapse.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
