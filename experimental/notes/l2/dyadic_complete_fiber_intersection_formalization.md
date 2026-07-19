# Complete-fiber intersection Lean formalization

## Status

PROVED

The source theorem is equation (1) in
`experimental/notes/l2/dyadic_complete_fiber_slicing_route_cut.md`.  The
source-facing Lean declaration is
`DyadicCompleteFiberSlicing.completeFiberIntersection` in the standalone
package `experimental/lean/dyadic_complete_fiber_slicing/`.

## Exact wrapper

The theorem quantifies over an arbitrary field `F`, a finite multiplicative
subgroup `H <= F^x` with `Fintype.card H = n`, a total order on `H`, natural
numbers satisfying `1 <= K <= m <= n`, a divisor `c | n`, an arbitrary
received word `U : H -> F`, and two distinct polynomials `P,Q`.  The hypotheses
`inReceivedList H K m U P` and `inReceivedList H K m U Q` say respectively
that each polynomial has natural degree below `K` and at least `m` agreement
points with `U`.  The conclusion is exactly

```text
|(completeFiberSet H c (canonicalSupport H m U P)) intersect
  (completeFiberSet H c (canonicalSupport H m U Q))| <= (K - 1) / c.
```

The file installs `Classical.decEq F` locally because the displayed finite-set
intersection must elaborate before any proof body is entered.  Printing the
theorem confirms that no `DecidableEq F` binder is exported; this is
noncomputable elaboration glue, not a strengthened source hypothesis.

## Proof map

1. `powerFiber_card` regards `x -> x^c` as `powMonoidHom c` on `H`.
   Mathlib's cyclicity instance for finite subgroups of units and
   `IsCyclic.card_powMonoidHom_ker` give kernel cardinality
   `gcd(|H|,c)=c`; `MonoidHom.card_fiber_eq_of_mem_range` transfers that
   cardinality to every nonempty fiber.
2. `Finset.sum_card_fiberwise_eq_card_filter` counts all subgroup elements
   above the common complete-fiber values.  Since every such fiber has `c`
   points, their total number is `c` times the common-value count.
3. Completeness puts each counted point in both canonical supports.
   `canonicalSupport_subset_agreementSet` therefore gives
   `P(x)=U(x)=Q(x)`.
4. Injecting `H` into `F` puts all counted points among the roots of the
   nonzero polynomial `P-Q`.  The root bound and the two degree hypotheses
   give at most `K-1` points.
5. The divisor hypothesis together with `n >= 1` proves `c > 0`, so
   `Nat.le_div_iff_mul_le` yields the source ceiling `(K-1)/c`.

The proof uses `hP.1` and `hQ.1` for degree.  The agreement-cardinality and
range hypotheses remain in the exported wrapper exactly as printed in the
source; canonical-support containment is sufficient for the intersection
argument.

## Axioms and replay

With Lean 4.28.0 and Mathlib commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`:

```text
lake build
Build completed successfully (8027 jobs).

#print axioms DyadicCompleteFiberSlicing.completeFiberIntersection
[propext, Classical.choice, Quot.sound]
```

There is no `sorry`, `admit`, `sorryAx`, custom `axiom`, or custom `opaque`
declaration in the Lean file.  The fail-closed verifier
`experimental/scripts/verify_dyadic_complete_fiber_intersection_formalization.py`
pins the source, proof, package, and this audit note and exercises a mutation
self-test.  The existing deployed-arithmetic verifier remains separate.

## Boundary

This Lean result certifies source equation (1) only.  It does not formalize
the subset-packing consequence (2), the independent Johnson-ball consequence
(3), the deployed dyadic arithmetic, the `1792` residual profiles, the
unproved uniform residual cap, the weighted-GRS or syndrome transport, Grand
List, Grand MCA, an extension-field list theorem, or an exact-threshold
conclusion.  The challenge-field denominator in the deployed ledger is not
used anywhere in this theorem.
