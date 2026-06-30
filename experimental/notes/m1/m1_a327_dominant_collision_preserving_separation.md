# M1 a=327 dominant-collision-preserving separation

Status: `PARTIAL / EXPERIMENTAL / SEARCH_AUDIT`

This packet follows `9bbffb8`. The previous exact lift showed that
coefficient pins break degeneracy, but only by destroying the collision
capacity. This audit therefore chooses separation pins at coordinates outside
the dominant all-seven collision set of the high-capacity degenerate skeleton.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

For each tested robust proxy system, the audit reconstructs the high-capacity
degenerate exact skeleton from the proxy-support schedule. Coordinates where
all seven codewords collide are protected. Candidate separation coordinates are
chosen from the remaining dominant size-six collision coordinates, with quotient
fiber diversity.

The exact systems keep:

- the proxy-pivot target rows;
- the proxy-support coefficient pins preserving the high-capacity skeleton;
- one of several off-skeleton separation pin families:
  - one pairwise separation pin;
  - two pairwise separation pins;
  - five evaluation pins on `D_3,\ldots,D_7`;
  - six evaluation pins on `D_2,\ldots,D_7`.

Every exact solution is evaluated directly over `GF(17^32)` and rescheduled
when its value-class capacity permits it.

## Result

The first exact audit tested `24` safe-separation pin sets across the top three
robust proxy systems.

- `9` exact vectors were constructed.
- `6` vectors were nondegenerate.
- `0` nondegenerate vectors preserved capacity at least `327`.
- The best high-capacity vector had capacity upper bound `374`, but remained
  degenerate and rescheduled only to max-min `192`.
- The best nondegenerate vectors had capacity upper bound `82`.

Current status:

`EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This is not a global obstruction. It says the tested off-skeleton pairwise and
evaluation separation pins still do not combine the two needed properties:
capacity preservation and witness distinctness.

## Status labels

`CANDIDATE` means an exact `GF(17^32)` vector reaches min agreement at least
`327` and still needs a full proof-record audit before any public row update.

`EXACT_EXTRACTION_NO_A327` means the bounded safe-separation families found no
exact `a=327` sample.

`PARTIAL` means broader safe pin families and the full exact nullspace remain
open.

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
