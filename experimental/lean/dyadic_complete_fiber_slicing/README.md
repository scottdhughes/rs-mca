# Dyadic complete-fiber slicing formalization map

Build the standalone package with its pinned Lean 4.28 / Mathlib environment:

```bash
lake build
```

## Source correspondence

Source note:
`experimental/notes/l2/dyadic_complete_fiber_slicing_route_cut.md`.

| Source statement | Lean declaration | Status |
|---|---|---|
| Equation (1), complete-fiber intersection | `DyadicCompleteFiberSlicing.completeFiberIntersection` | PROVED |

The public theorem has the source wrapper: an arbitrary field; a finite
multiplicative subgroup `H` of cardinality `n`; `1 <= K <= m <= n`; a total
order on `H`; an arbitrary received word `U`; distinct degree-`< K`
polynomials with at least `m` agreements; and `c | n`.  Its conclusion is
exactly

```text
|E_c(P) intersect E_c(Q)| <= floor((K - 1) / c).
```

The file's local classical `DecidableEq F` is an elaboration instance, not a
public theorem parameter.  The proof uses Mathlib's cyclicity instance for
finite subgroups of a field's unit group, the power-map kernel cardinality,
fiberwise finite-set counting, and the polynomial root bound.

The clean package build succeeds in `8027` jobs.  The declaration reports
exactly the standard Mathlib axioms
`[propext, Classical.choice, Quot.sound]`; it has no `sorryAx` or custom axiom.

The source note's deployed integers are replayed separately with:

```bash
python3 experimental/data/certificates/dyadic-complete-fiber-slicing/verify_role07_dyadic_full_fiber_cut.py
```

That script and its canonical output retain SHA-256 digests `ae75af706c6f...`
and `7d884ffb903d...`, respectively.  The arithmetic replay does not verify the
field-theoretic proof; the Lean theorem does not verify the deployed ledger.

## Boundary

This package certifies equation (1) only.  It does not formalize the packing
consequences (2) or (3), the deployed integer ledger, the residual
`1792`-profile cap, the GRS/syndrome transport, Grand List, Grand MCA, or an
exact-threshold conclusion.  Those claims retain their statuses in the source
note.
