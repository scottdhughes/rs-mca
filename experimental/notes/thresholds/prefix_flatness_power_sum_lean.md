# Lean-verified prefix-flatness power-sum bound (2026-07-10)

Status: `PROVED` (Lean, zero-`sorry`). Module: `experimental/lean/powersum_rigidity/PowersumRigidity/PrefixFlatness.lean`
(builds `leanprover/lean4:v4.31.0`; `#print axioms` = `[propext, Classical.choice, Quot.sound]` on all results;
full package green). Machine-checks the load-bearing inequality of the Fourier-flat / prefix-flat payment.

## What it proves

`thm:prefix-flatness-power-sum` (`rs_mca_entropy_frontiers.tex`) and `thm:fourier-flat-q` (`grande_finale.tex`)
turn a Weil/character-sum bound on the power sums `p_j(a) = Σ_t a_t^j` (`a_t = ψ(α·g(t))`) into a bound on the
prefix-fiber count `e_m(a) = R̂(α)`. The Li–Wan generating-function core is:

    **if  ‖p_j(a)‖ ≤ Λ  for all 1 ≤ j ≤ m,   then  ‖e_m(a)‖ ≤ C(Λ+m-1, m) = [u^m](1-u)^{-Λ}.**

`PrefixFlatness.esymm_norm_le` is exactly this, over `K = ℝ` or `ℂ` (`RCLike`), for `e_m = Multiset.esymm`.
The bound `B Λ m := (∏_{i<m}(Λ+i))/m! = C(Λ+m-1, m)` is the coefficient of the majorizing series `(1-u)^{-Λ}`.

## Proof (machine-checked)

Strong induction on `m` via Newton's identity `m·e_m = (-1)^{m+1} Σ_{i<m} (-1)^i e_i p_{m-i}`
(`PowersumRigidity.newton_image`, already in the package). Taking norms and using `‖p_j‖ ≤ Λ` gives
`m·‖e_m‖ ≤ Λ·Σ_{i<m} ‖e_i‖`, majorized by the rising-factorial recursion `m·B_m = Λ·Σ_{i<m} B_i`
(`PrefixFlatness.B_rec`), which `B Λ m` satisfies. No `sorry`, no `native_decide`.

## Placement

This is the "easy direction" of Fourier-flatness (bounded power sums ⟹ bounded fiber): the payment mechanism,
now with a machine-checked kernel. It does NOT establish the power-sum bound `‖p_j‖ ≤ Λ` itself (that is Weil,
valid only for `w = o(√p)` — the deployed rows sit far past it), and it does NOT discharge the dense-regime
input `prob:entropy-inverse-q` (the `√p`/BGK inverse theorem carried as the `(PF)/(MA)` hypotheses). It hardens
the conditional-payment step of a submission-track manuscript, in the same Lean package as the reciprocal-gap
(`mersenne_reciprocal_gap`) and Frobenius-closure (`FrobeniusClosure`) results.

Main results: `PrefixFlatness.esymm_norm_le`, `PrefixFlatness.B_rec`, `PrefixFlatness.B`.
