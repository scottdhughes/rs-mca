# M1 a=327 protected-exchange exact audit

Status: `EXACT_AUDIT_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `c9f2e4c`, where protected local exchange produced the
cleanest proxy candidate in the `a=327` lane so far.

## Proxy baseline

Best protected-exchange proxy candidate:

```text
candidate id:                 7d2bb937c72e__PX48__one_for_two
proxy max-min:                335
proxy agreement vector:       [335,335,335,335,335,335,336]
capacity upper bound:         461
pair B values:                [671,671,671,671,671]
added six-class dominance:    0
protected stage-1 rows:       preserved
```

This cleared the proxy witness-7 pair Hall obstruction, but it was not a
certificate over the actual field.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This packet is an exact `GF(17^32)` audit of the two protected-exchange proxy
candidates. It does not claim a new public row.

## Exact audit method

The Sage audit reconstructs each protected-exchange target system and tests
exact row schedules over `GF(17^32)`:

```text
protected_rows_only
protected_plus_exchange_rows
selected_prefix_128
selected_prefix_256
```

For each full-row-rank exact schedule, it uses exact pivot columns and
proxy-guided free-column assignments:

```text
proxy_mod17_support
proxy_sparse_64
blockwise_constants
```

It also evaluates the direct proxy-vector mod-17 map. Every constructed exact
vector is evaluated directly on `H`, then the exact value-class rescheduler is
run when the capacity bound is high enough.

## Result

Exact audit summary:

```text
proxy candidates tested:      2
row schedules tested:         8
free schedules tested:        24
exact vectors constructed:    26
nondegenerate vectors:        0
best exact max-min:           287
best exact agreement vector:  [287,287,287,287,287,287,288]
best capacity upper bound:    447
best pair B values:           [575,575,575,575,575]
best failure mode:            DEGENERATE_CODEWORDS
```

All tested exact row schedules had full row rank:

```text
7d2bb937c72e__PX48__one_for_two:
  protected_rows_only:          16/16
  protected_plus_exchange_rows: 64/64
  selected_prefix_128:          128/128
  selected_prefix_256:          256/256

7d2bb937c72e__PX32__one_for_two:
  protected_rows_only:          16/16
  protected_plus_exchange_rows: 52/52
  selected_prefix_128:          128/128
  selected_prefix_256:          256/256
```

## Interpretation

This is a bounded exact-audit negative, not a route cut for all exact lifts.

The proxy protected-exchange geometry remains the strongest constructive
signal, but the tested exact free-column schedules all land in degenerate
codeword tuples. The best exact vector keeps reasonably high raw capacity but
does not preserve the proxy pair-7 repair:

```text
proxy pair B:  [671,671,671,671,671]
exact pair B:  [575,575,575,575,575]
```

The next exact attack should preserve nondegeneracy explicitly while keeping
the protected-exchange row schedule, rather than running more proxy searches.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`CANDIDATE` means a proxy or partial exact candidate remains pending exact
verification.

`EXACT_AUDIT_NO_A327` means the bounded exact schedules in this packet found
no exact `a>=327` witness.

`PARTIAL` means full exact nullspace extraction, nondegenerate exact schedules,
and broader protected-exchange exact lifting remain open.

## Failure labels

- `DEGENERATE_CODEWORDS`: fewer than seven distinct exact codewords.
- `PAIR7_REPAIR_LOST`: exact vector loses the pair-7 Hall repair.
- `COLLAPSE_RETURNS`: exact vector reintroduces six-class dominance.
- `CAPACITY_LOSS`: exact capacity upper bound drops below `327`.
- `LOW_RESCHEDULE`: capacity and pair repair survive, but exact max-min is
  below `327`.
- `EXACT_CANDIDATE_A327`: exact max-min reaches at least `327`.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No public-row update.
