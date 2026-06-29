# M1 a=327 Incumbent-Guided Target Mutation

Status:

`CANDIDATE / PARTIAL / EXPERIMENTAL`

Track:

`INTERLEAVED_LIST`

Row:

`RS[F_17^32,H,256]`

Agreement target:

`a = 327`

## Summary

This packet mutates the best target systems from the balanced target/codeword
solver around the observed rescheduling deficit.

Parent checkpoint:

`43a8a66 add M1 a327 balanced target codeword solver`

Parent best proxy result:

- raw capacity upper bound: `457`
- proxy rescheduled max-min: `319`
- agreement vector: `[319, 320, 319, 319, 319, 319, 319]`

This branch uses that incumbent failure pattern as a feedback signal.  It
mutates selected target rows using deficit repair, anti-six-of-seven,
variance-minimizing, fiber-rebalancing, and hybrid objectives.

## Result

The controlled first pass tested:

- base incumbents: `5`
- mutation rounds per incumbent: `10`
- mutated target systems: `50`
- row budgets: `512, 640`
- nullspace samples per system over `GF(12289)`: `32`
- total proxy codeword tuple samples: `1600`

Best proxy result:

- raw capacity upper bound: `459`
- proxy rescheduled max-min: `329`
- agreement vector: `[329, 330, 329, 329, 329, 329, 329]`
- proxy candidate systems: `13`
- proxy candidate samples: `52`

This is the first local constructive-search packet in this lane that crosses
the `a=327` threshold in the proxy field.

## Exact Lift Audit

The Sage audit performs a bounded exact lift check on the top proxy-trigger
systems:

- exact field: `GF(17^32)`
- audited systems: `3`
- lifted proxy samples per system: `4`
- exact lifted `a>=327` samples: `0`

The best exact lift has:

- capacity upper bound: `439`
- rescheduled max-min: `257`
- status: `EXACT_LIFT_DEGENERATE_CODEWORDS`

The lift audit reduces the proxy coefficients modulo `17` and evaluates the
resulting degree-`<256` codewords over `GF(17^32)`.  That is an exact
finite-field check for those lifted tuples, but it is not a full exact
nullspace extraction for the target systems.

The attempted direct exact `GF(17^32)` row reduction for the first 640-row
target system was too slow for this packet, so full exact nullspace extraction
is left open.

## Interpretation

The incumbent-guided mutation objective worked at the proxy-search level:

`319 -> 329`.

This is strong evidence that the prior bottleneck diagnosis was correct:
capacity was available, but the target system needed to be mutated using the
actual post-rescheduling deficit.

However, the proxy hit is not a board-facing proof record.  The simple exact
coefficient lift does not preserve the proxy certificate, and no exact
`GF(17^32)` witness has been extracted.

## Proof Status

Valid:

- The proxy search found target/codeword tuples over `GF(12289)` whose exact
  proxy received-word rescheduling reaches `a=329`.
- The top lifted tuples over `GF(17^32)` do not verify an `a=327`
  interleaved-list certificate.

Not claimed:

- no `a=327` interleaved-list proof record;
- no global `Lambda_mu(C,327) <= 6`;
- no MCA `N_bad`;
- no protocol soundness failure;
- no ordinary list-decoding theorem beyond the stated interleaved-list
  predicate;
- no exact `Lambda_mu`;
- no exact `delta*_C`;
- no improvement over PR `#133`;
- no full exact `GF(17^32)` nullspace extraction for the proxy target systems.

## Next Step

The immediate next attack should not be another broad target generator.  It
should implement exact extraction for the proxy-positive target systems:

1. reconstruct the top mutated target systems over `GF(17^32)`;
2. avoid full dense 640-by-1536 RREF when possible;
3. try block/quotient row elimination, modular lifting, or targeted free-column
   schedules;
4. sample exact nullspace vectors;
5. run the exact received-word rescheduler;
6. promote only if Sage verifies seven distinct degree-`<256` codewords and one
   received word with agreement at least `327` for every witness.
