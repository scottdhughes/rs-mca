# Controls

## Positive controls

1. **Canonical exact-dimensional parent.** Fix a basis and coordinate order.
   From the nontransverse witness choose the first proper rich flat, then the
   first intermediate parent of dimension `rank(U)+1`. This preserves the
   common-zero set.
2. **Merged parent packets.** If several row-space packets map to one parent,
   all their differences lie in that parent. Because the parent vanishes on
   every source witness set, it vanishes on their union and still has at least
   `42,453` common actual zeros.
3. **Disjoint load.** The row-space packets from the predecessor partition are
   disjoint in slopes. Canonical assignment and merging preserve disjointness.
4. **Exact packet caps.** Dimension-two and dimension-three parents use the
   ordinary affine projection cap followed by the proved sub-square
   interleaving collapse and the fixed-pair slope multiplier `n-A`.
5. **Convex set-system bound.** For fixed total incidence, the sum of
   `binom(degree,k)` is minimized when coordinate degrees differ by at most
   one. The verifier exhausts small set systems independently.
6. **Weighted pin.** Parent weights are their assigned distinct-slope loads.
   Double counting `(slope, coordinate-set)` incidences gives the pinned-load
   bounds without assuming uniform packet sizes.

## Hostile controls

1. The complete nontransverse witness space may have dimension larger than
   `rank(U)+1`; it is not charged as though it had the smaller dimension until
   the canonical intermediate parent is selected.
2. Different row spaces may map to the same parent. Counting source row spaces
   as distinct parents would be false; equal parents are merged first.
3. Rich parents can have identical common-zero subsets. The convexity argument
   allows repeated subsets and becomes stronger, not weaker, in that case.
4. The anchor-good universe can have size below `m`. Padding it by empty
   coordinates to size `m` only weakens the intersection bounds.
5. A common coordinate does not by itself pay its packet union. The theorem
   uses the exact dimension-four pair-list cap to force span dimension at
   least five and makes no stronger payment claim.
6. Pair, triple, and fourfold common-zero conclusions concern parent spaces,
   not arbitrary original supports or active-v4 owners.
7. No parent or locator is cancelled independently in the row ledger.

## Finite controls

The primary verifier enumerates small uniform set systems and checks the
balanced-degree lower bound for pair, triple, and fourfold intersection
moments. The independent audit recomputes every deployed integer from separate
product formulas and checks all adjacent strict inequalities.