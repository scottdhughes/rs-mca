import Mathlib

/-!
# The mass-aware few-shell moment inequality

This module formalizes the exact inequality in section 4 of
`cap25_v13_m31_chebyshev_entropy_inverse_shells.md`.
-/

open scoped BigOperators

namespace M31FewShell

/-- A probability mass with pointwise bound `B` has its `(n+1)`-moment bounded by `B^n`. -/
theorem massMoment_le_of_max
    {ι : Type*} [Fintype ι] (ν : ι → ℝ)
    (B P : ℝ) (n : ℕ)
    (hν0 : ∀ z, 0 ≤ ν z)
    (hνB : ∀ z, ν z ≤ B)
    (hνsum : ∑ z, ν z = 1)
    (hP : 0 ≤ P) :
    P ^ n * ∑ z, ν z ^ (n + 1) ≤ (B * P) ^ n := by
  calc
    P ^ n * ∑ z, ν z ^ (n + 1)
        ≤ P ^ n * ∑ z, B ^ n * ν z := by
          exact mul_le_mul_of_nonneg_left
            (Finset.sum_le_sum fun z _ => by
              rw [pow_succ]
              exact mul_le_mul_of_nonneg_right
                (pow_le_pow_left₀ (hν0 z) (hνB z) n) (hν0 z))
            (pow_nonneg hP n)
    _ = (B * P) ^ n := by
      rw [← Finset.mul_sum, hνsum, mul_one, mul_pow]
      exact mul_comm _ _

/--
Mass-aware form of the source inequality:
`p^(w*(ℓ-1)) * ∑ ν(z)^ℓ ≤ (A*p^w/M)^(ℓ-1)`.
-/
theorem fewShell_mass_bound
    {ι : Type*} [Fintype ι] (ν : ι → ℝ)
    (A M p : ℝ) (w ℓ : ℕ)
    (hν0 : ∀ z, 0 ≤ ν z)
    (hνsum : ∑ z, ν z = 1)
    (hνmax : ∀ z, ν z ≤ A / M)
    (_hM : 0 < M) (_hA : 0 ≤ A)
    (hp : 0 ≤ p) (hℓ : 1 ≤ ℓ) :
    p ^ (w * (ℓ - 1)) * ∑ z, ν z ^ ℓ ≤
      (A * p ^ w / M) ^ (ℓ - 1) := by
  simpa only [Nat.sub_add_cancel hℓ, pow_mul, div_mul_eq_mul_div] using
    massMoment_le_of_max ν (A / M) (p ^ w) (ℓ - 1)
      hν0 hνmax hνsum (pow_nonneg hp w)

#print axioms massMoment_le_of_max
#print axioms fewShell_mass_bound

end M31FewShell
