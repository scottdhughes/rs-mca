# Separating-Pole Existence Correspondence

Status: **PROVED** for the exact same-field unordered-pair bound in equation
(4.6) and its complete prefix-fiber bad-slope cardinality corollary.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`thm:exact-list-line-bijection`, equation (4.6), and
`cor:exact-prefix-ray-realization`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Chosen two elements of an unordered polynomial pair | `GrandeFinale.SeparatingPole.pairLeft`, `GrandeFinale.SeparatingPole.pairRight` |
| Nonzero difference polynomial for a pair | `GrandeFinale.SeparatingPole.pairDifference`, `GrandeFinale.SeparatingPole.pairDifference_ne_zero` |
| Product over all unordered list pairs | `GrandeFinale.SeparatingPole.separatingPolynomial` |
| Degree bound `k * choose L 2` | `GrandeFinale.SeparatingPole.separatingPolynomial_natDegree_le` |
| Off-domain separating-pole existence | `GrandeFinale.SeparatingPole.exists_separating_pole` |
| Specialization to the complete prefix list | `GrandeFinale.SeparatingPole.exists_prefixFiber_separating_pole` |
| Existence of an exact prefix-fiber ray realization | `GrandeFinale.SeparatingPole.exists_prefixFiber_badSlopeSet_card_eq` |

## Statement comparison

For a finite list `L` of polynomials of natural degree at most `k`, Lean forms
`L.powersetCard 2`.  Each member is an unordered two-element sublist, and its
chosen difference polynomial is nonzero.  Their product has natural degree at
most

`L.card.choose 2 * k`.

The bad pole set is the union of the evaluation domain `D` and the roots of
that product.  Its cardinality is at most

`D.card + k * L.card.choose 2`.

Thus the literal strict budget from equation (4.6) yields a pole outside `D`
that is not a root of any pair difference.  Evaluation at that pole is
injective on `L`.  No ordered-pair factor of two is introduced.

The prefix specialization takes `k = K - 1` and obtains the degree bound from
the already-proved complete prefix-list interface.  Composing with
`ExactPrefixRay.badSlopeSet_card_eq_coefficientFiber` gives a pole whose MCA
bad-slope set has cardinality exactly equal to the coefficient fiber.

## Scope boundaries

The generic theorem and prefix specialization use one finite field: the
evaluation domain and every polynomial in the complete list already live in
the pole field.  The source also applies the bound after embedding a base-field
received word and list into a larger finite extension.  Coefficient mapping,
completeness of the mapped list against ambient-field explanations, and the
Vandermonde descent back to the base field are supplied by
`ScalarExtensionListLine.lean`.

## Verification

```text
lake env lean GrandeFinale/SeparatingPole.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
