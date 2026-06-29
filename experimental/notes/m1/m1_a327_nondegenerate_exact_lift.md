# M1 a=327 nondegenerate exact lift

Status: `PARTIAL / EXPERIMENTAL / SEARCH_AUDIT`

This packet follows the robust proxy constrained-extraction checkpoint
`f9a43ea`. That checkpoint found 13 proxy-positive target systems whose
pivot/free-column structure is stable across five proxy primes, but the first
bounded `GF(17^32)` 64-row lift collapsed to degenerate codewords with exact
rescheduled max-min `256`.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

This packet does not generate new proxy target systems. It tests whether the
stable proxy free space from `f9a43ea` can be lifted exactly while avoiding the
degenerate subspace seen in the first exact partial solve.

## Method

The Sage audit reconstructs the top robust proxy system over `GF(17^32)` and
tests bounded constrained solves:

- row subsets: proxy-pivot, fiber-diverse, deficit, full-target sample, and a
  128-row proxy-pivot subset when reached by the vector cap;
- free schedules: proxy-support columns, balanced common-free columns by
  witness block, and seeded common-free columns;
- exact value patterns: all ones, blockwise constants, generator powers, and
  seeded base-field values.

For every exact vector constructed, the audit directly evaluates the seven
codewords on `H`, computes value classes, runs the exact received-word
max-min assignment when the capacity bound permits it, and records whether the
failure is due to degeneracy, low capacity, or low rescheduling.

## Result

The bounded exact audit tested `32` exact vectors from the top stable proxy
system.

- `4` proxy-support schedules remained high-capacity but degenerate. The best
  exact rescheduled max-min among them was `288`, with capacity upper bound
  `448`, but the codewords were not distinct.
- `12` balanced or seeded free-column schedules produced seven distinct
  codewords, but their value-class capacity collapsed. The best nondegenerate
  capacity upper bound was `94`.
- `16` fiber-diverse partial solves had singular scheduled pivot minors under
  the tested pivot-column schedule.

No exact `GF(17^32)` sample reached agreement `327`.

Current status:

`EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This is a bounded exact-lift failure for the named schedules only. It does not
exhaust the full exact nullspace of the robust proxy systems.

## Status labels

`CANDIDATE` means an exact `GF(17^32)` sample reaches min agreement at least
`327` and requires a full proof-record audit before any board update.

`EXACT_EXTRACTION_NO_A327` means the named bounded exact-lift strategies found
no exact `a=327` sample.

`PARTIAL` means the full exact nullspace of the robust proxy systems is not
exhausted.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No improvement over PR #133 unless a later Sage proof record verifies an
  exact `a>=327` witness.
