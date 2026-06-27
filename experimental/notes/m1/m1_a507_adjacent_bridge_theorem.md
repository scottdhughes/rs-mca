# M1 a=507 Adjacent Bridge Obstruction

Date: 2026-06-27

Status: PROVED_OBSTRUCTION / AUDIT / BRIDGE_REJECTED_FOR_CURRENT_ROW

## Purpose

This note resolves the current-board version of the `a=507` adjacent bridge
question.

The active finite row is

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board row uses the finite-slope support-wise MCA predicate

```text
LD_sw(C,a).
```

The exact high-agreement tangent-star theorem gives

```text
LD_sw(C,a) = 513-a    for a >= 427.
```

In particular,

```text
LD_sw(C,507) = 6.
```

The adjacent high-agreement coding ledger has the arithmetic

```text
line numerator             = 6,
interleaved-list numerator = 1,
conditional total          = 7.
```

The question is whether that adjacent `6+1=7` ledger can be consumed as the
same board-counted `N_bad=7` event, with denominator

```text
q_line = 17^32.
```

## Decision Theorem

There is no bridge map `B` that simultaneously satisfies all five current-row
board-consumption conditions:

1. Predicate preservation: `B` sends the adjacent interleaved-list `+1` to the
   same finite-slope support-wise `LD_sw` retained-event class used by the
   current board row.
2. Denominator preservation: `B` keeps the denominator `q_line=17^32`.
3. Disjointness: the image of the adjacent `+1` is disjoint from the six known
   `LD_sw(C,507)` retained slopes.
4. No double counting: the image contributes one new retained event after all
   fiber corrections.
5. Agreement preservation: the image is still an agreement-`507` event.

Equivalently, the adjacent `6+1=7` ledger is not board-consumable as a new
`N_bad=7` row for the current finite-slope support-wise MCA predicate.

## Proof

Assume for contradiction that such a bridge `B` exists.

By predicate preservation, the image of the adjacent `+1` is a finite-slope
support-wise `LD_sw` retained event at agreement `507`.

By disjointness and no double counting, it is not one of the six already counted
finite-slope support-wise events. Therefore the six known retained events plus
the image of the adjacent `+1` give at least seven distinct events in the same
`LD_sw(C,507)` predicate.

Thus

```text
LD_sw(C,507) >= 7.
```

This contradicts the exact tangent-star theorem

```text
LD_sw(C,507) = 6.
```

Therefore no bridge satisfying the five current-row board-consumption
conditions exists.

## What Still Remains True

The adjacent coding ledger remains valid as a separate ledger:

```text
line numerator             = 6,
interleaved-list numerator = 1,
conditional total          = 7.
```

Since

```text
floor(17^32 / 2^128) = 6,
```

that conditional total would clear the integer gate if a protocol or coding
reduction proved that both terms are charged to one compatible retained-event
sampler.

This theorem says only that the `+1` cannot be added to the current
finite-slope support-wise `LD_sw` numerator.

## Decision Table

```text
same-predicate finite-slope board row:
  N_bad(507) = 6
  clears_gate = false
  status = PROVED_SAFE_FOR_THIS_PREDICATE

adjacent line-plus-list coding ledger:
  conditional_total = 7
  clears_gate_if_consumable = true
  status = SEPARATE_LEDGER_NOT_CURRENT_BOARD_ROW

bridge into current board row:
  status = PROVED_OBSTRUCTION
  reason = exact LD_sw(C,507)=6 rules out a disjoint seventh same-predicate event
```

## Non-Claims

NOT CLAIMED:

- a new frontier row at `a=507`;
- protocol soundness failure;
- ordinary list-decoding failure;
- exact `delta*_C`;
- impossibility of separate interleaved-list, CA, projective, curve, or protocol
  ledgers with their own event semantics;
- impossibility of a different board track with a separately justified
  denominator.

## Status Ledger

PROVED:

- same-predicate current-row bridge is impossible;
- the obstruction is the exact upper bound `LD_sw(C,507)=6`;
- the current board-counted numerator remains `N_bad=6`;
- the adjacent `6+1=7` arithmetic is not countable in the current row.

SEPARATE LEDGER:

- the adjacent line-plus-interleaved-list coding ledger still has conditional
  total `7`;
- it remains usable only after a theorem states a compatible predicate,
  denominator, and sampler.

OPEN:

- whether a separate protocol-facing adjacent ledger can be used on another
  board track;
- whether a genuinely new event outside finite-slope `LD_sw` has a valid
  denominator and retained-event semantics;
- extension-valued or curve/projective variants with exact transfer theorems.
