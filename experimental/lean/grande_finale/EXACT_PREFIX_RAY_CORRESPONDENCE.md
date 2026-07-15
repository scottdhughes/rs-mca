# Exact Prefix-Ray Correspondence

Status: **PROVED** for the same-field, fixed-pole support-to-slope image,
separating-pole cardinality, and exact agreement-support clauses of
`cor:exact-prefix-ray-realization`.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`cor:exact-prefix-ray-realization`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Evaluation-domain inclusion and restricted received word | `GrandeFinale.ExactPrefixRay.domainEval`, `GrandeFinale.ExactPrefixRay.polynomialWord` |
| Agreement-set transport between the subtype domain and `D` | `GrandeFinale.ExactPrefixRay.image_polynomialAgreementSet_eq`, `GrandeFinale.ExactPrefixRay.polynomialAgreementSet_card_eq` |
| Degree and completeness interface for the finite prefix list | `GrandeFinale.ExactPrefixRay.listedPolynomial_natDegree_le_pred`, `GrandeFinale.ExactPrefixRay.listedPolynomial_agreements`, `GrandeFinale.ExactPrefixRay.mem_listedPolynomials_of_degree_agreements` |
| A prefix support is the full polynomial agreement support | `GrandeFinale.ExactPrefixRay.prefixPolynomial_agreementSet_eq_support` |
| The corresponding line point retains exactly that support | `GrandeFinale.ExactPrefixRay.lineAgreementSet_image_eq_support` |
| Direct support-to-slope image equals the full MCA-bad slope set | `GrandeFinale.ExactPrefixRay.coefficientFiber_slope_image_eq_badSlopeSet` |
| A separating pole gives exact bad-slope/fiber cardinality | `GrandeFinale.ExactPrefixRay.badSlopeSet_card_eq_coefficientFiber` |

## Statement comparison

Lean uses `K` for the locator-cancellation cutoff, so the source code
parameter `k` is `K - 1` and the coefficient-prefix depth is `m - K`.  The
received polynomial is the explicit monic
`PrefixPigeonhole.prefixPolynomial K m z`, and a support `S` maps directly to
the slope

`(prefixPolynomial K m z - locator S).eval alpha`.

The image of this map is proved equal to the complete finite MCA-bad slope set
of the pole line.  This image equality does not require separation.  When
evaluation at `alpha` is injective on the complete polynomial list, locator
injectivity makes the support-to-slope map injective as well, so the bad-slope
cardinality is exactly the coefficient-fiber cardinality.

For each support in the fiber, Lean also proves that the polynomial agreement
set is exactly `S`, then transports the quotient explaining polynomial's line
agreement set back from the subtype evaluation domain to the same `S`.

## Scope boundaries

This is the same-field specialization: the evaluation domain, prefix
polynomial, complete list, pole, and MCA slopes all lie in one finite field.
It assumes a pole outside `D`; the cardinality theorem additionally assumes
that the pole separates the complete list.  `SeparatingPole.lean` proves
existence under the exact same-field equation-(4.6) budget.  The
base-to-extension coefficient descent and ambient-list completeness needed
when the list is constructed over a proper subfield are supplied by
`ScalarExtensionListLine.lean`.

The module exports the exact support-to-slope image and the exact agreement
support of the displayed quotient explanation.  The additional uniqueness
layer for arbitrary explanations, including the occupancy-one statement, is
supplied by `ExactPrefixRayUniqueness.lean`.

## Verification

```text
lake env lean GrandeFinale/ExactPrefixRay.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
