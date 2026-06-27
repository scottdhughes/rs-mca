# M1 a=507 Plus-One Slope Hunt

Date: 2026-06-26

Status: ROUTE_CUT / AUDIT / BRIDGE_NEEDED

## Objective

The current finite MCA row is

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

Under the finite-slope support-wise MCA convention, the current high-agreement
gate is

```text
LD_sw(C,506) = 7,
LD_sw(C,507) = 6,
q_line = 17^32,
floor(q_line / 2^128) = 6.
```

Thus `a=507` is exactly one retained bad slope short of clearing the board gate

```text
2^128 N_bad > q_line.
```

This packet asks whether a controlled extension of the current retained-event
families supplies one additional valid bad slope at agreement `a=507` while
preserving the same denominator `q_line=17^32`.

## Result

No same-predicate plus-one slope is found.

More strongly, the integrated tangent-star theorem already gives the exact
finite-slope support-wise upper bound in this range:

```text
LD_sw(C,a) = 513-a    for every a >= 427.
```

Therefore

```text
LD_sw(C,507) = 6
```

inside the finite-slope support-wise predicate.  Therefore any candidate from
the families below can only be counted in this packet if it lands in the exact
same finite-slope support-wise `LD_sw` predicate, with the same denominator
`q_line=17^32` and no change of event semantics.  Under that same-predicate
interpretation, the integrated bound `LD_sw(C,507)=6` excludes every seventh
retained slope.

This packet does not independently classify or exhaust quotient-core,
two-ended, CA/projective, curve, or interleaved objects outside the `LD_sw`
predicate.

There is one adjacent plus-one-looking object:

```text
line numerator 6 + interleaved-list numerator 1 = 7.
```

This comes from the integrated adjacent-ledger theorem.  It is not a seventh
finite support-wise bad slope.  It is recorded as `BRIDGE_NEEDED`, not as a
`PROOF_RECORD` slope and not as part of `N_bad`.

## Search Families

The scan covers these families:

1. current finite-slope support-wise tangent-star template;
2. tangent-floor refinements;
3. projective-slope and no-loss CA high-agreement ledgers;
4. quotient-core refinements that still assert the same support-wise predicate;
5. two-ended locator variants that still assert the same support-wise predicate;
6. slope symmetries, including Frobenius or dilation relabelings;
7. adjacent line-plus-interleaved-list ledger term.

The family labels are same-predicate exclusion labels, not independent
exhaustive searches over all objects in those mechanisms.  Families 1-6 are
blocked only insofar as a candidate is asserted to be a same-denominator
finite-slope support-wise `LD_sw` event.  Family 7 has total numerator `7` in a
conditional coding ledger, but it is not a support-wise slope count.

## Current Board Row Replay

For `n=512`, `k=256`, the exact tangent-star range starts at

```text
ceil((2n+k)/3) = 427.
```

The exact counts are:

| agreement `a` | `LD_sw(C,a)` | status |
|---:|---:|---|
| 506 | 7 | clears `2^-128` |
| 507 | 6 | safe endpoint |
| 508 | 5 | safe |
| 509 | 4 | safe |
| 510 | 3 | safe |

## Plus-One Accounting

At `a=507`:

```text
N_bad_old = 6
extra_valid_same_predicate_slopes = 0
N_bad_new = 6
threshold_floor = 6
clears_gate = false.
```

The adjacent coding ledger has:

```text
line_numerator = 6
interleaved_list_numerator = 1
conditional_total = 7
```

but its proof status is `BRIDGE_NEEDED` for the finite-slope support-wise board
row.

## Status Ledger

PROOF_RECORD:

- existing six finite-slope support-wise tangent-star bad slopes at `a=507`;
- exact replay of `a=506,...,510` using the tangent-star theorem;
- exact denominator and integer threshold.

ROUTE_CUT:

- no additional same-predicate finite-slope support-wise slope exists at
  `a=507`: any such slope, from any proposed mechanism, is counted by `LD_sw`
  and is excluded by the exact upper bound `LD_sw(C,507)=6`.

BRIDGE_NEEDED:

- the adjacent line-plus-interleaved-list ledger has total numerator `7`, but it
  is not a seventh support-wise bad slope and cannot be counted in `N_bad`
  without a separate board-predicate bridge.

NOT CLAIMED:

- ordinary list decoding;
- protocol soundness failure;
- efficient attack;
- exact `delta*_C`;
- a new finite-slope support-wise board frontier at `a=507`;
- permission to combine different denominators or event semantics.

OPEN:

- a genuinely new predicate bridge that lets the adjacent `+1` term be consumed
  by the board as a retained event with explicit denominator semantics;
- a non-finite-slope or protocol-facing certificate with its own denominator
  and retained-event ledger.
