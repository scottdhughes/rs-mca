# M1 a=327 residual-degeneracy separation

Status: `PARTIAL / EXPERIMENTAL / SEARCH_AUDIT`

This packet follows `8255f1c`. The previous safe-separation audit showed that
off-skeleton pins could either preserve capacity while remaining degenerate, or
split witnesses while destroying capacity. This packet first identifies the
exact residual witness identifications in the high-capacity degenerate
skeletons, then targets those equivalence classes directly.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

For each tested robust proxy system, the Sage audit reconstructs the
high-capacity degenerate vector and records a degeneracy ledger:

- value-vector equivalence classes among the seven witnesses;
- zero blocks;
- fully equal witness pairs on `H`;
- largest-class histogram and capacity upper bound.

Then it tests targeted split families:

- split the largest degenerate pair at a quotient-safe coordinate;
- split the same pair at another coordinate in the same residual class;
- split one pair from each degenerate class;
- split several witnesses inside the largest class using evaluation-profile
  pins.

Each exact solution is evaluated directly over `GF(17^32)` and rescheduled if
its capacity permits it.

## Result

The exact audit tested `12` targeted residual-degeneracy split pin sets across
the top three robust proxy systems.

The degeneracy ledger was identical across the three tested systems:

```text
witness equivalence classes on H:
  [1,3,4,5,6,7]
  [2]
```

So the high-capacity skeleton is not an arbitrary collapse. It is a specific
six-witness identification class plus one separated witness.

The targeted quotient-aware split attempts produced:

- `12` exact vectors;
- `0` nondegenerate vectors;
- `0` capacity-preserving nondegenerate vectors;
- best capacity upper bound `374`, still degenerate;
- best exact max-min `192`.

Current status:

`EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This does not prove a global obstruction. It says the tested targeted splits do
not break the residual six-witness identification class while preserving the
dominant collision skeleton.

## Status labels

`CANDIDATE` means an exact `GF(17^32)` vector reaches min agreement at least
`327` and still needs a full proof-record audit before any public row update.

`EXACT_EXTRACTION_NO_A327` means the bounded residual-degeneracy split families
found no exact `a=327` sample.

`PARTIAL` means broader quotient-aware split families and the full exact
nullspace remain open.

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
