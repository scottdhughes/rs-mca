# M1 a=327 collision-preserving nondegenerate lift

Status: `PARTIAL / EXPERIMENTAL / SEARCH_AUDIT`

This packet follows `9c2f278`, which split the exact-lift failure into two
clear regimes:

- high-capacity exact schedules reached capacity upper bound `448` and exact
  max-min `288`, but the codewords were degenerate;
- balanced exact schedules produced seven distinct codewords, but capacity
  collapsed, with best nondegenerate capacity upper bound `94`.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

This checkpoint does not generate new proxy target systems. It starts from the
stable robust proxy systems and tests exact linear pins intended to preserve
the proxy-support collision structure while forcing nonzero support in all six
difference-polynomial blocks.

## Method

For the top robust proxy systems, the exact Sage audit reconstructs the target
rows over `GF(17^32)` and tests coefficient-pin families:

- `coefficient_proxy_plus_5x1`;
- `coefficient_proxy_plus_5x2`;
- `coefficient_proxy_plus_5x4`;
- `coefficient_proxy_plus_6x1`.

Each family keeps the proxy-support free columns that produced high collision
capacity and adds small fixed nonzero values in the other witness blocks. The
audit tests prefix proxy pivots and mixed block pivots, then directly evaluates
every exact vector and runs the received-word max-min solver whenever the
capacity bound permits it.

## Result

The first exact audit tested `36` pinned exact vectors across the top three
robust proxy systems.

- `18` vectors were nondegenerate, with all six difference-polynomial blocks
  nonzero.
- `0` nondegenerate vectors retained capacity upper bound at least `327`.
- The best pinned nondegenerate capacity upper bound was `91`.
- Mixed block-pivot schedules were inconsistent for the tested row/pin
  combinations.

Current status:

`EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This is a useful negative result: the tested minimal coefficient pins do break
the exact degeneracy, but they also destroy the proxy-support collision
geometry. It is not a global obstruction and does not exhaust evaluation pins,
pairwise separation pins, or the full exact nullspace.

## Status labels

`CANDIDATE` means an exact `GF(17^32)` vector reaches min agreement at least
`327` and still needs a full proof-record audit before any public row update.

`EXACT_EXTRACTION_NO_A327` means the bounded pinned exact-lift strategies found
no exact `a=327` sample.

`PARTIAL` means the full exact nullspace and other pin families remain open.

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
