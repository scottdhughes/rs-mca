# Exact deep MCA frontier

Status: **PROVED** in Lean 4.28.

This package formalizes the finite exact-deep claims stated in
`experimental/asymptotic_rs_mca_frontiers.tex`. It connects the paper's
exact agreement numerator to the existing real-radius deep-MCA proof, adds a
challenge-restricted numerator, and proves its exact value for Reed--Solomon
codes by a coordinate tangent construction.

## Claim correspondence

| Paper claim | Lean theorem | Relation |
| --- | --- | --- |
| Deep-regime upper bound (`thm:deep-regime-upper`) | `Deep.B_MCA_le_deep` | Exact finite-cardinality form |
| Challenge-restricted deep upper bound used in `cor:exact-deep-numerator` | `Deep.B_MCA_challenge_le_deep`, `Deep.rs_B_MCA_challenge_le_deep` | Includes both the challenge-cardinality and `n-a+1` ceilings |
| Universal tangent floor (`prop:universal-tangent-floor`) | `Tangent.tangent_floor` | Proved for any linear code with the stated minimum-distance inequality |
| Exact deep numerator (`cor:exact-deep-numerator`) | `Tangent.rs_B_MCA_challenge_eq_deep` | Exact equality for an injective RS evaluation domain |

`Deep.mcaBad_iff_radius` proves that support-wise badness at agreement
`a` is literally the existing radius predicate at `(n-a)/n`. The upper
bound then extracts the unnormalized cardinality statement from
`RSCap`'s deep-regime theorem.

For the lower bound, choose
`t = min Γ.card (n-a+1)` coordinates and label them by distinct challenge
slopes. The received pair is zero away from those coordinates and has values
`(-γ, 1)` on a coordinate labelled by `γ`. At that slope, the affine
combination agrees with the zero codeword after deleting the other labelled
coordinates. Any codeword explaining the second received word would be
nonzero with weight at most `t`, contradicting the minimum-distance
hypothesis.

The Lean result also permits an empty challenge set; both sides are then zero.
The paper states the nonempty case. Its hypotheses `1 ≤ k`,
`k + 1 ≤ a ≤ n`, and `3(n-a) ≤ n-k` are represented explicitly in the
final theorem.

## Verification

From this directory:

```sh
lake build
```

The modules end with `#print axioms` checks for the principal bridge,
upper-bound, tangent-floor, and equality theorems. Their reports contain only
the standard `propext`, `Classical.choice`, and `Quot.sound` axioms.

## Scope

This package proves the finite exact numerator in the deep regime. The paper's
later asymptotic threshold composition and adjacent-row results are outside
this package.

The development imports the exact definitions in `GrandeFinale` and the
deep-MCA and Reed--Solomon minimum-distance theorems in `cs25_cap_v12`.
