# Exact Prefix-List Correspondence

Status: **PROVED** for the exact support/list correspondence and the
no-extra-agreement clause.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`prop:exact-prefix-list` and equation (4.1).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Agreement support of `U` and a lower-degree polynomial `P` | `GrandeFinale.ExactPrefixList.agreementSet` |
| Prefix fiber represented by exact leading-coefficient cancellation | `GrandeFinale.ExactPrefixList.prefixSupportSet` |
| Degree-less-than-`K` polynomial list at agreement `m` | `GrandeFinale.ExactPrefixList.listPolynomialSet` |
| A lower-degree polynomial has at most `m` agreements with monic degree `m` | `GrandeFinale.ExactPrefixList.agreementSet_card_le` |
| Every prefix support produces the listed polynomial `U - locator(S)` | `GrandeFinale.ExactPrefixList.prefixSupport_to_listPolynomial` |
| A listed polynomial has exactly `m` agreements and recovers their locator | `GrandeFinale.ExactPrefixList.listPolynomial_locator` |
| Exact unique support/list correspondence | `GrandeFinale.ExactPrefixList.listPolynomial_iff_existsUnique_prefixSupport` |
| No listed polynomial has an additional agreement | `GrandeFinale.ExactPrefixList.listPolynomial_agreementSet_card_eq` |

## Statement comparison

The source fixes `w = m - K` and a monic polynomial `U_z` whose first `w`
coefficients below the leading term equal the prefix `z`. The Lean module
represents membership in that prefix fiber by the exact cancellation condition

`degree (U - locator S) < K`.

For two monic degree-`m` polynomials, this is the algebraic condition used in
the source proof: their leading terms and first `m - K` lower coefficients
cancel. The module keeps `U` arbitrary subject to `IsMonicOfDegree U m`, so
the result includes the displayed `U_z` specialization.

Codewords are represented by their unique degree-less-than-`K` polynomial
representatives. The forward theorem constructs `U - locator(S)`. Conversely,
the agreement support of every listed polynomial has cardinality exactly `m`,
and `U - P` is proved equal to its monic locator. Equal-cardinality support
inclusion then gives uniqueness.

## Scope boundaries

The module proves the bijection and exact-agreement parts of
`prop:exact-prefix-list`. It does not yet define the coefficient-vector map
or prove the pigeonhole list-size lower bound inside this module; those are
formalized separately in `PrefixPigeonhole.lean`. It does not perform the
later simple-pole conversion or prove the separating-pole list--line
bijection itself; the same-field fixed-pole composition is formalized in
`ExactListLine.lean` and `ExactPrefixRay.lean`.

## Verification

```text
lake env lean GrandeFinale/ExactPrefixList.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
