# Exact Prefix-Ray Witness Uniqueness Correspondence

Status: **PROVED** for the same-field, separating-pole witness-incidence and
occupancy-one clause of `cor:exact-prefix-ray-realization`.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`cor:exact-prefix-ray-realization`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| A field support viewed in the subtype evaluation domain | `GrandeFinale.ExactPrefixRayUniqueness.supportOnDomain` |
| Exact transport and cardinality of that support | `GrandeFinale.ExactPrefixRayUniqueness.image_supportOnDomain_eq`, `GrandeFinale.ExactPrefixRayUniqueness.supportOnDomain_card_eq` |
| Prefix support gives a member of the complete list | `GrandeFinale.ExactPrefixRayUniqueness.listedPolynomial_mem_of_mem_coefficientFiber` |
| Arbitrary explanation reconstructs the canonical quotient and support | `GrandeFinale.ExactPrefixRayUniqueness.explanation_eq_and_support_image_eq` |
| Exact line-witness predicate | `GrandeFinale.ExactPrefixRayUniqueness.IsExactLineWitness` |
| Occupancy one for the selected prefix slope | `GrandeFinale.ExactPrefixRayUniqueness.existsUnique_exactLineWitness` |

## Statement comparison

Fix a prefix support `S` and its slope

`gamma = (prefixPolynomial K m z - locator S).eval alpha`.

Lean considers an arbitrary polynomial `G` of degree less than `K - 1` that
explains this line point on any subtype support `T` with at least `m` points.
It reconstructs

`P' = (X - C alpha) * G + C gamma`.

The line equations show that `P'` agrees with the received polynomial on `T`,
so completeness puts `P'` in the exact prefix list.  Evaluation gives
`P'.eval alpha = gamma`; separation of the list therefore forces `P'` to be
the polynomial attached to `S`.  Exact agreement support then gives
`T.image Subtype.val = S`, and cancellation of `X - C alpha` identifies `G`
with the canonical quotient explaining polynomial.

`existsUnique_exactLineWitness` packages this as uniqueness of the pair
`(support, explaining polynomial)`.  Its predicate initially permits supports
of cardinality at least `m`; the theorem proves that the unique support is the
canonical one and hence has cardinality exactly `m`.

## Scope boundaries

This theorem uses the same finite field for the evaluation domain, prefix
polynomial, pole, and slopes.  It assumes the pole lies outside the domain and
separates the complete polynomial list.  It does not prove a separating pole
exists itself; `SeparatingPole.lean` supplies the exact same-field
equation-(4.6) existence theorem.  It does not perform coefficient descent
from an extension field to a proper base field.

Together with `ExactPrefixRay.coefficientFiber_slope_image_eq_badSlopeSet` and
`ExactPrefixRay.badSlopeSet_card_eq_coefficientFiber`, this closes the
same-field support, slope, and exact-witness clauses of the source corollary.

## Verification

```text
lake env lean GrandeFinale/ExactPrefixRayUniqueness.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
