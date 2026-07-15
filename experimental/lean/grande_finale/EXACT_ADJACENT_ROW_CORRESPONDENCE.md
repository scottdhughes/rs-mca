# Exact Adjacent-Row Hyperplane Correspondence

Status: **PROVED** for the finite hyperplane-avoidance and syndrome compiler
listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially the
lower-bound construction in `thm:exact-first-adjacent-row` (AD1).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Choose a direction outside all `M` hyperplanes when `M < |F|` | `GrandeFinale.ExactAdjacentRow.exists_separating_line` |
| Choose an intercept avoiding one collision hyperplane for each unordered pair when `choose M 2 < |F|` | `GrandeFinale.ExactAdjacentRow.exists_separating_line` |
| Use the literal gate `max M (choose M 2) < |F|` | `GrandeFinale.ExactAdjacentRow.exists_separating_line_of_max_lt` |
| Obtain `M` pairwise-distinct finite transverse slopes | `GrandeFinale.ExactAdjacentRow.exists_separating_line_of_max_lt` |
| Compile the transverse intersections into the exact syndrome-secant numerator | `GrandeFinale.ExactAdjacentRow.separatingHyperplanes_le_syndromeSecantNumerator` |
| Transfer the lower bound to the existing support-wise MCA numerator under syndrome surjectivity | `GrandeFinale.ExactAdjacentRow.separatingHyperplanes_le_B_MCA` |
| Combine the construction with a supplied exact support upper bound | `GrandeFinale.ExactAdjacentRow.B_MCA_eq_of_separatingHyperplanes` |

The unordered collision family is implemented as the two-element subsets of
the hyperplane index type, so its cardinality is definitionally connected to
`Nat.choose M 2`; the proof does not replace the paper's gate by an ordered-pair
or quadratic overestimate.

## Scope boundaries

This module does not yet construct the `(R-1)`-column syndrome hyperplanes from
an injective Reed–Solomon evaluation domain, prove the weighted Vandermonde
parity map has kernel equal to the evaluation code, or prove the exact support
upper bound. Consequently it proves the arrangement and generic MCA compiler
inside AD1, not the final Reed–Solomon equality or either AD2 threshold
implication.

## Verification

```text
lake build GrandeFinale.ExactAdjacentRow
```

The module prints the axioms of its four exported results. No `sorry`, `admit`,
`native_decide`, or added axiom occurs.
