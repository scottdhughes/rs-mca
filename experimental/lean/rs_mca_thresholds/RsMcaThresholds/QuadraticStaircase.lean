import RsMcaThresholds.QuadraticMeanOverlap

/-!
# Exact quadratic staircase

This file formalizes the literal real-square-root radius MO7 from
`cor:mean-overlap-exact` in `experimental/rs_mca_thresholds.tex`, together
with the integer cap needed by the radius hypotheses of MO4.
-/

open scoped Classical

noncomputable section

namespace RsMcaThresholds
namespace QuadraticStaircase

set_option autoImplicit false

open ExactSparsification
open QuadraticMeanOverlap

universe u v

variable {F : Type u} {D : Type v}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]

/-- The smaller real root in MO7. -/
noncomputable def quadraticRoot (n k : ℕ) : ℝ :=
  (3 * (n : ℝ) -
    Real.sqrt ((n : ℝ) * (5 * (n : ℝ) + 4 * (k : ℝ)))) / 2

/-- The exact integer MO7 radius, capped by the literal MO4 side condition
`r ≤ n-k-1`. The cap is redundant in the intended proper-code range but keeps
that side condition visible at the Lean boundary. -/
noncomputable def quadraticRadius (n k : ℕ) : ℕ :=
  min (n - k - 1) ⌊quadraticRoot n k⌋₊

/-- The MO7 radical is real and its displayed value is the smaller root of
`x^2 - 3nx + n(n-k)`. -/
theorem quadraticRoot_is_root (n k : ℕ) :
    (quadraticRoot n k) ^ 2 -
        3 * (n : ℝ) * quadraticRoot n k +
        (n : ℝ) * ((n : ℝ) - (k : ℝ)) = 0 := by
  have hdisc :
      0 ≤ (n : ℝ) * (5 * (n : ℝ) + 4 * (k : ℝ)) := by positivity
  have hsqrt := Real.sq_sqrt hdisc
  rw [quadraticRoot]
  nlinarith

/-- For `k ≤ n`, the smaller MO7 root is nonnegative, so its natural floor
has the ordinary floor specification. -/
theorem quadraticRoot_nonneg {n k : ℕ} (hk : k ≤ n) :
    0 ≤ quadraticRoot n k := by
  have hn : (0 : ℝ) ≤ n := by positivity
  have hkn : (k : ℝ) ≤ n := by exact_mod_cast hk
  have hnk : (n : ℝ) * k ≤ (n : ℝ) * n :=
    mul_le_mul_of_nonneg_left hkn hn
  have hsqrt :
      Real.sqrt ((n : ℝ) * (5 * (n : ℝ) + 4 * (k : ℝ))) ≤
        3 * (n : ℝ) := by
    apply Real.sqrt_le_iff.mpr
    constructor
    · positivity
    · nlinarith
  rw [quadraticRoot]
  nlinarith

/-- The smaller root lies on the decreasing side of the quadratic. -/
theorem two_mul_quadraticRoot_le (n k : ℕ) :
    2 * quadraticRoot n k ≤ 3 * (n : ℝ) := by
  have hsqrt :
      0 ≤ Real.sqrt ((n : ℝ) * (5 * (n : ℝ) + 4 * (k : ℝ))) :=
    Real.sqrt_nonneg _
  rw [quadraticRoot]
  nlinarith

/-- In the proper-code range, the smaller root lies strictly below the
redundancy `n-k`. -/
theorem quadraticRoot_lt_distance {n k : ℕ} (hk : k < n) :
    quadraticRoot n k < (n - k : ℕ) := by
  have hkReal : (k : ℝ) < n := by exact_mod_cast hk
  have hnReal : (0 : ℝ) < n := by
    exact_mod_cast (Nat.zero_lt_of_lt hk)
  have hkNonneg : (0 : ℝ) ≤ k := by positivity
  have hprod :
      0 < ((n : ℝ) - k) * ((n : ℝ) + k) :=
    mul_pos (sub_pos.mpr hkReal) (by nlinarith)
  have hsquare :
      ((n : ℝ) + 2 * (k : ℝ)) ^ 2 <
        (n : ℝ) * (5 * (n : ℝ) + 4 * (k : ℝ)) := by
    nlinarith
  have hsqrt :
      (n : ℝ) + 2 * (k : ℝ) <
        Real.sqrt ((n : ℝ) * (5 * (n : ℝ) + 4 * (k : ℝ))) := by
    by_contra h
    have hsqrtLe :
        Real.sqrt ((n : ℝ) * (5 * (n : ℝ) + 4 * (k : ℝ))) ≤
          (n : ℝ) + 2 * (k : ℝ) := le_of_not_gt h
    have hdiscLe := (Real.sqrt_le_iff.mp hsqrtLe).2
    nlinarith
  rw [quadraticRoot, Nat.cast_sub (Nat.le_of_lt hk)]
  nlinarith

/-- The visible MO4 cap is redundant: the capped natural radius is exactly the
raw natural floor printed in MO7. -/
theorem quadraticRadius_eq_floor {n k : ℕ} (hk : k < n) :
    quadraticRadius n k = ⌊quadraticRoot n k⌋₊ := by
  have hrootNonneg : 0 ≤ quadraticRoot n k :=
    quadraticRoot_nonneg (Nat.le_of_lt hk)
  have hfloorReal :
      (⌊quadraticRoot n k⌋₊ : ℝ) ≤ quadraticRoot n k :=
    Nat.floor_le hrootNonneg
  have hfloorLtReal :
      (⌊quadraticRoot n k⌋₊ : ℝ) < (n - k : ℕ) :=
    hfloorReal.trans_lt (quadraticRoot_lt_distance hk)
  have hfloorLt : ⌊quadraticRoot n k⌋₊ < n - k := by
    exact_mod_cast hfloorLtReal
  unfold quadraticRadius
  apply min_eq_right
  omega

/-- Every integer radius below the capped MO7 floor satisfies the literal MO3
quadratic inequality. -/
theorem quadratic_condition_of_le_radius {n k r : ℕ}
    (hk : k < n) (hr : r ≤ quadraticRadius n k) :
    n * (k + r) ≤ (n - r) ^ 2 := by
  have hrCap : r ≤ n - k - 1 :=
    hr.trans (min_le_left _ _)
  have hrFloor : r ≤ ⌊quadraticRoot n k⌋₊ :=
    hr.trans (min_le_right _ _)
  have hrn : r ≤ n := by omega
  have hkLe : k ≤ n := Nat.le_of_lt hk
  have hrootNonneg : 0 ≤ quadraticRoot n k :=
    quadraticRoot_nonneg hkLe
  have hfloor : (⌊quadraticRoot n k⌋₊ : ℝ) ≤ quadraticRoot n k :=
    Nat.floor_le hrootNonneg
  have hrReal : (r : ℝ) ≤ quadraticRoot n k := by
    have : (r : ℝ) ≤ (⌊quadraticRoot n k⌋₊ : ℝ) := by
      exact_mod_cast hrFloor
    exact this.trans hfloor
  have hdecreasing :
      (r : ℝ) + quadraticRoot n k - 3 * (n : ℝ) ≤ 0 := by
    have hrootSide := two_mul_quadraticRoot_le n k
    nlinarith
  have hproduct :
      0 ≤ ((r : ℝ) - quadraticRoot n k) *
        ((r : ℝ) + quadraticRoot n k - 3 * (n : ℝ)) :=
    mul_nonneg_of_nonpos_of_nonpos (sub_nonpos.mpr hrReal) hdecreasing
  have hrootEq := quadraticRoot_is_root n k
  have hpoly :
      0 ≤ (r : ℝ) ^ 2 - 3 * (n : ℝ) * (r : ℝ) +
        (n : ℝ) * ((n : ℝ) - (k : ℝ)) := by
    nlinarith
  have hquadReal :
      (n : ℝ) * ((k : ℝ) + (r : ℝ)) ≤
        ((n : ℝ) - (r : ℝ)) ^ 2 := by
    nlinarith
  have hcastQuad :
      (n : ℝ) * ((k : ℝ) + (r : ℝ)) ≤
        ((n - r : ℕ) : ℝ) ^ 2 := by
    rw [Nat.cast_sub hrn]
    exact hquadReal
  exact_mod_cast hcastQuad

/-- Raw-floor form of the MO3 implication, matching the displayed MO7 radius. -/
theorem quadratic_condition_of_le_floor {n k r : ℕ}
    (hk : k < n) (hr : r ≤ ⌊quadraticRoot n k⌋₊) :
    n * (k + r) ≤ (n - r) ^ 2 := by
  apply quadratic_condition_of_le_radius hk
  rwa [quadraticRadius_eq_floor hk]

/-- The cap in `quadraticRadius` exposes the exact-agreement side condition
needed by MO4. -/
theorem add_one_le_agreement_of_le_radius {n k r : ℕ}
    (hk : k < n) (hr : r ≤ quadraticRadius n k) :
    k + 1 ≤ n - r := by
  have hrCap : r ≤ n - k - 1 :=
    hr.trans (min_le_left _ _)
  omega

/-- Paper-facing MO7 staircase for injective Reed--Solomon evaluation codes. -/
theorem rs_quadratic_staircase_exact
    (Γ : Finset F) (_hΓ : Γ.Nonempty)
    (dom : D → F) (hdom : Function.Injective dom)
    (k r : ℕ) (hk : k < Fintype.card D)
    (hr : r ≤ ⌊quadraticRoot (Fintype.card D) k⌋₊) :
    B_MCA_challenge Γ (RSCap.RSpolySubmodule dom k)
        (Fintype.card D - r) = min Γ.card (r + 1) := by
  have hrRadius : r ≤ quadraticRadius (Fintype.card D) k := by
    rwa [quadraticRadius_eq_floor hk]
  apply rs_quadratic_mean_overlap_exact Γ dom hdom k r
  · have hrCap : r ≤ Fintype.card D - k - 1 :=
      hrRadius.trans (min_le_left _ _)
    omega
  · exact add_one_le_agreement_of_le_radius hk hrRadius
  · exact quadratic_condition_of_le_floor hk hr

#print axioms quadraticRoot_is_root
#print axioms quadratic_condition_of_le_radius
#print axioms rs_quadratic_staircase_exact

end QuadraticStaircase
end RsMcaThresholds
