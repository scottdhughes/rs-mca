# Dense-shell FOLD weighted-curvature certificate

This standalone stdlib-only Lean 4.14 package kernel-checks the exact
linear-arithmetic compiler behind
`experimental/notes/thresholds/dense_shell_fold_curvature_certificate.md`:

- the weighted summation-by-parts identity for 17 drops;
- exact equivalence of the cleared `57/50` fold and its curvature certificate;
- the sharper `17/15` implication under nonpositive weighted curvature;
- the third-difference sign convention; and
- the `256`, `289`, and weight-sum constants.

It does not prove monotonicity or the curvature sign for the realized
dense-shell cascade.  The full Section 8.4 FOLD input remains open.

Run:

```bash
lake build
```
