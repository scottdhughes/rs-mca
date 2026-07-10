import Mathlib

/-!
# Vandermonde rank kills the inverse output (`prop:vandermonde-kills-low-rank`)

The endpoint of the entropy-scale inverse-theorem skeleton (`prob:entropy-inverse-q`,
`grande_finale.tex`): the "rank defect" alternative `(b)` is impossible on the moment curve. This module
machine-checks its core — the scaled Vandermonde columns of `t ≤ R` distinct points are linearly independent.

    v_i = ρ_i · (1, y_i, y_i², …, y_i^{R-1}) ∈ K^R,   t ≤ R,  y_i distinct,  ρ_i ≠ 0
    ⟹  {v_1, …, v_t}  linearly independent.

Consequently `t` such columns span a `t`-dimensional subspace, so a positive-density subset (`t = Θ(n)`) of
primitive moment-curve columns cannot lie in any affine subspace of dimension `o(n)` — which is the alternative
that `prob:entropy-inverse-q` must produce for a contradiction. So this is the machine-checked terminal step:
once the entropy/PFR machinery yields a rank defect, `VandermondeRank.columns_linearIndependent` refutes it.

## Main result

* `VandermondeRank.columns_linearIndependent` — the scaled Vandermonde columns are linearly independent.
* `VandermondeRank.no_low_dim` — the finite-dimensional consequence: their span has dimension `t`.
-/

open Matrix

namespace VandermondeRank

variable {K : Type*} [Field K]

/-- **Vandermonde rank kills the inverse output (core).**  For `t ≤ R`, distinct points `y : Fin t → K`, and
nonzero weights `ρ`, the scaled Vandermonde columns `i ↦ (j ↦ ρ i · y i ^ j) : Fin R → K` are linearly
independent over `K`. -/
theorem columns_linearIndependent {t R : ℕ} (htR : t ≤ R)
    (y : Fin t → K) (hy : Function.Injective y) (ρ : Fin t → K) (hρ : ∀ i, ρ i ≠ 0) :
    LinearIndependent K (fun i : Fin t => (fun j : Fin R => ρ i * y i ^ (j : ℕ))) := by
  rw [Fintype.linearIndependent_iff]
  intro c hc
  -- reduce to the leading `t × t` Vandermonde system on `d_i = c_i ρ_i`
  set d : Fin t → K := fun i => c i * ρ i with hd
  have hMv : (Matrix.vandermonde y)ᵀ *ᵥ d = 0 := by
    funext j
    have hj := congrFun hc (Fin.castLE htR j)
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hj
    simp only [Matrix.mulVec, dotProduct, Matrix.transpose_apply, Matrix.vandermonde_apply,
      Pi.zero_apply]
    rw [← hj]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    rw [hd, Fin.val_castLE]; ring
  -- the Vandermonde matrix is nonsingular (distinct points)
  have hdet : (Matrix.vandermonde y)ᵀ.det ≠ 0 := by
    rw [Matrix.det_transpose]; exact Matrix.det_vandermonde_ne_zero_iff.mpr hy
  have hd0 : d = 0 := Matrix.eq_zero_of_mulVec_eq_zero hdet hMv
  intro i
  have hi : c i * ρ i = 0 := by have := congrFun hd0 i; rwa [hd, Pi.zero_apply] at this
  exact (mul_eq_zero.mp hi).resolve_right (hρ i)

/-- The span of the `t` scaled Vandermonde columns has full dimension `t`: no `o(n)`-dimensional subspace can
contain a positive-density (`t = Θ(n)`) set of moment-curve columns.  (The refutation of alternative `(b)`.) -/
theorem no_low_dim {t R : ℕ} (htR : t ≤ R)
    (y : Fin t → K) (hy : Function.Injective y) (ρ : Fin t → K) (hρ : ∀ i, ρ i ≠ 0) :
    Module.finrank K (Submodule.span K
      (Set.range (fun i : Fin t => (fun j : Fin R => ρ i * y i ^ (j : ℕ))))) = t := by
  have hli := columns_linearIndependent htR y hy ρ hρ
  rw [finrank_span_eq_card hli, Fintype.card_fin]

end VandermondeRank
