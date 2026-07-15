# Reed--Solomon Exact-Support Upper-Bound Correspondence

Status: **PROVED** for the full-field support-atlas upper bound listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`lem:exact-agreement-reduction` and `prop:exact-support-upper`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Interpolate arbitrary values on exactly `k` evaluation points | `GrandeFinale.RSExactSupportUpper.exists_rsEval_explanation_on_card_eq` |
| Two degree-`< k` words agreeing on at least `k` points are equal | `GrandeFinale.RSExactSupportUpper.rsEval_eq_of_agree_on_card_ge` |
| An unexplained word on `S` remains unexplained on some exact `a`-subset | `GrandeFinale.RSExactSupportUpper.exists_exact_support_preserving_not_explained` |
| Every threshold-`a` MCA witness has an exact `a`-element support | `GrandeFinale.RSExactSupportUpper.mcaBad_has_exact_support` |
| Threshold bad slopes are the union of exact-support cells | `GrandeFinale.RSExactSupportUpper.mcaBadSlopes_eq_exactSupportFamily` |
| The full-field MCA numerator is at most `choose |D| a` | `GrandeFinale.RSExactSupportUpper.B_MCA_rsEval_le_choose` |

The reduction interpolates one received word on a `k`-subset of a witness
support. Because that word is not explained on the whole support, it disagrees
with the interpolant at another point. The resulting `k+1` points can be
extended to an exact `a`-element sub-support while preserving both the line
explanation and the failure of pair explanation.

## Scope boundaries

The module proves the literal full-field bound
`B_MCA (rsEval ev k) a <= choose |D| a` when `a >= k+1`. It does not include
the challenge-set minimum, compose this upper bound with the support-hyperplane
lower construction, or derive the final AD1 equality and AD2 implications.

## Verification

```text
lake env lean GrandeFinale/RSExactSupportUpper.lean
```

The module prints the axioms of its principal results. No proof placeholder or
added axiom occurs.
