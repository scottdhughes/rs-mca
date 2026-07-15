# Scalar-Extension List--Line Correspondence

Status: **PROVED** for base-to-extension coefficient descent, ambient-list
completeness, and the full finite equation-(4.6) exact list--line interface in
`thm:exact-list-line-bijection`.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`thm:exact-list-line-bijection`, equation (4.6), and
`cor:exact-prefix-ray-realization`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Base and extension evaluation maps | `GrandeFinale.ScalarExtensionListLine.baseEval`, `GrandeFinale.ScalarExtensionListLine.extensionEval` |
| Scalar extension of the received word and polynomial list | `GrandeFinale.ScalarExtensionListLine.extensionWord`, `GrandeFinale.ScalarExtensionListLine.mappedPolynomialList` |
| Mapped list preserves cardinality and agreement supports | `GrandeFinale.ScalarExtensionListLine.mappedPolynomialList_card`, `GrandeFinale.ScalarExtensionListLine.extensionAgreementSet_map_eq_base` |
| Vandermonde/interpolation coefficient descent | `GrandeFinale.ScalarExtensionListLine.exists_basePolynomial_of_many_agreements` |
| Mapped list is complete against ambient explanations | `GrandeFinale.ScalarExtensionListLine.mappedPolynomialList_complete` |
| Mapped-list evaluation image equals all MCA-bad slopes | `GrandeFinale.ScalarExtensionListLine.mappedPolynomialList_image_eval_eq_badSlopeSet` |
| Full extension-pole separation, image, and cardinality theorem | `GrandeFinale.ScalarExtensionListLine.exists_extensionPole_exact_listLine` |
| Direct extension-field prefix-fiber cardinality realization | `GrandeFinale.ScalarExtensionListLine.exists_extensionPrefix_badSlopeSet_card_eq_coefficientFiber` |

## Statement comparison

Let `B` and `F` be fields with `Algebra B F`, let `D` be a finite subset of
`B`, and let the received word take values in `B`.  If an ambient polynomial
`P : F[X]` of natural degree at most `k` agrees on at least `m` positions, with
`k + 1 <= m`, Lean selects `k + 1` of those positions.  Lagrange interpolation
over `B` produces a base polynomial `Q` of degree at most `k`.  Both `P` and
`Q.map (algebraMap B F)` have degree less than `k + 1` and agree on the selected
nodes, so polynomial uniqueness gives

`P = Q.map (algebraMap B F)`.

Algebra-map injectivity then proves equality of the complete agreement
supports.  Thus the coefficientwise image of any complete base list is
complete against every ambient-field explanation, not only against mapped
ones.

For finite `F`, the exact unordered-pair theorem from `SeparatingPole` selects
an off-domain pole under

`D.card + k * L.card.choose 2 < Fintype.card F`.

The exported theorem records pole admissibility, injectivity on the mapped
list, exact equality of its evaluation image with the MCA-bad slope set, and
bad-slope cardinality equal to the original base-list cardinality.  The direct
prefix specialization rewrites this cardinality as the coefficient-fiber
cardinality.

## Scope boundaries

The complete base list, its degree bound, both directions of its completeness
specification, and `k + 1 <= m` are explicit hypotheses of the generic
theorem.  `ExactPrefixList`, `PrefixPigeonhole`, and `ExactPrefixRay` supply
these inputs for the explicit locator-prefix list in the final specialization.

No finite-dimensionality assumption on `F` over `B` is needed.  Finiteness is
used only for selecting the pole.  This module itself does not include the
later proper-challenge translate-intersection transfer; that downstream
composition is supplied by `PrefixChallengeFloor.lean`.  An extension-field
`ExistsUnique` packaging of arbitrary prefix witnesses remains separate.

## Verification

```text
lake env lean GrandeFinale/ScalarExtensionListLine.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
