# Independent mathematics and custody audit

## Verdict

**GREEN for the stated payment and route cut.**

## Adversarial findings incorporated

1. **Six supports were not sharp.** Comparing arbitrary basis triples costs
   six omission sets. Comparing adjacent bases costs four, and the basis
   graph is connected. The proof now uses the latter.
2. **Minimum-floor rank-one capacity is not uniform.** A larger actual common
   core can lower the effective dimension and increase rank-one capacity.
   The payment uses the proved global maximum `4,070,947`.
3. **The adjacent cell is not declared paid.** At `K=778,969`, the strict
   minimum-distance inequality fails. The packet proves a dichotomy: the
   synchronized ray is paid, or a cubic near-MDS basis-edge word exists.
4. **The conditional lower interval is separated from the unconditional
   theorem.** From `K=774,075` through `778,969`, only the synchronized-ray
   branch is paid. A survivor must emit the named near-MDS word.
5. **Chronology is preserved.** The only summation is the disjoint partition
   of original frozen slopes into supports meeting and avoiding the actual
   common core.

## Mathematics checks

- vector divided-difference support containment uses only the frozen exact
  supports;
- a nonbasis triple lands in `W` and vanishes by the `3r<R+1` MDS bound;
- adjacent normalized bases land in `W` and synchronize by `4r<R+1`;
- basis-graph connectivity is reproved by basis exchange;
- passage from synchronized second differences to one affine correction ray
  is valid in the quotient by the common normalized direction;
- the universal-core-aware ray theorem retains all possible ray-universal
  coordinates;
- the four-endpoint optimization follows from exact convexity on both pieces;
- the cubic terminal degree is `(k-1)-z <= 3` with all quantities computed in
  the shortened row.

## Numerical checks

Primary and independent implementations agree on:

```text
first paid K                   778,970
first ray cap                1,067,271
maximum proper-drop cap      5,138,218
minimum payment slack           32,694
paid ambient cells              269,607
conditional cells                  4,895
conditional minimum slack              5
preceding conditional wall       over by 1
adjacent residual degree max            3
```

## Literature scope

Matroid basis-graph connectedness is classical, but no external theorem is
load-bearing: the packet contains the one-paragraph basis-exchange proof.
The Reed--Solomon/MCA claims are derived solely from pinned predecessor
interfaces and exact arithmetic.

## Build and custody checks

- all Python packet scripts compile with `py_compile`;
- the source-integration fragment compiles in a standalone theorem wrapper;
- the sealed manifest verifies SHA-256, Git blob SHA-1, and byte length for every bound file.

## Nonclaims

The audit rejects any statement that affine error rank twelve, the active-v4
ledger, or KoalaBear is closed by this packet.
