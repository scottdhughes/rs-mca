# Controls

## Positive controls

1. **Frozen records.**  Each selected slope retains one exact size-`m`
   explanation support and one minimizing pair before any incidence count.
2. **Complete pair cores.**  The lower bound `|H_gamma|>=m-theta_gamma` uses
   only the frozen support and minimizer.
3. **Global-core test.**  Full incident pair-difference span implies that the
   entire direction code vanishes at the coordinate; this is what promotes a
   local incidence to a whole-family shortening coordinate.
4. **Proper-span gauge.**  Subtracting one incident codeword pair places every
   incident explanation in the proper pair-difference span before division.
5. **Complete agreement domains.**  Shortening is performed on the complete
   scalar agreement domain.  Any shortened simultaneous pair explanation
   lifts to the original domain, preserving noncontainment.  RS interpolation
   uniqueness then supplies an exact target-size noncontained sub-support.
6. **Refreezing.**  After every shortening or rank drop, minimizing pairs may
   be chosen afresh.  No stale minimizer is transported as an optimizer.
7. **Endpoint clones.**  Identical coordinate lines are merged with integer
   multiplicity; all counts remain in original coordinate units.

## Hostile controls

1. An arbitrary exact support may not be modified by swapping in a core
   coordinate; a `GF(5)` regression in the predecessor adapter shows that this
   can create pair containment.
2. The incidence lower bound is not an upper bound on a proper-span family.
   It only selects the next nested subfamily.
3. Loads at different ranks are nested and may not be added.
4. The rich-flat caps from #1173 are not summed over emitted spaces.
5. A full incident span is useful only because all its generators vanish at
   the same actual coordinate.
6. The rank-one endpoint counts distinct affine slope points, not witnesses or
   support choices.
7. The theorem moves no active-v4 ledger atom and does not claim full
   KoalaBear closure.

## Finite controls

The primary verifier checks all `9,437,139` deployed rank/dimension cells
(the exact per-rank counts are frozen in `result.json`), 138 small
low-dominant support compositions, 1,500 weighted high-resource cells, the
271 endpoint deficiency vectors, and eight hostile certificate mutations.
A separately written audit reconstructs the recurrence and endpoint bound
without importing the primary verifier.
