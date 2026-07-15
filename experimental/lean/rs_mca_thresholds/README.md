# Exact RS-MCA threshold formalization

This Lean 4 package formalizes the exact support-reduction layer from
`sec:witnesses` of `experimental/rs_mca_thresholds.tex`.

It imports the shared CA/MCA definitions from the Grande Finale package and
proves the challenge-restricted exact sparsification identity for arbitrary
finite linear codes. It also proves both identities in the half-distance
sparse theorem (HD1), including the literal Reed--Solomon distance
specialization `2r ≤ n - k`. Finally, it formalizes the quadratic
mean-overlap incidence argument (MO1--MO6), the literal real-root staircase
(MO7), and proves the exact MO4 numerator for injective Reed--Solomon
evaluation codes under
`n * (k + r) ≤ (n - r)^2` and `k + 1 ≤ n - r`. The package now also certifies the exact closed-ball endpoint conversion,
target-aware quadratic and half-distance window compilers (including the
zero-budget branch), and the asymptotic first-safe certificate formula
`a = k + 1 + gn + o(n)` with radius `1 - ρ - g + o(1)`.

Build with the pinned toolchain:

    lake build
