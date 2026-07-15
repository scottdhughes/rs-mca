import RsMcaThresholds.QuadraticStaircase

/-!
# Endpoint and target-aware compiler

This file formalizes the finite core of `lem:appendix-endpoint` and the
sampling-denominator conversion used by the target compilers in
`experimental/rs_mca_thresholds.tex`.
-/

open scoped Classical

noncomputable section

namespace RsMcaThresholds
namespace EndpointCompiler

set_option autoImplicit false

open ExactSparsification

universe u v

variable {F : Type u} {D : Type v}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]

local notation "Word" => D → F

/-- Closed-ball agreement at real radius `δ`: exactly `floor(δ n)` errors are
permitted. -/
noncomputable def radiusAgreement (n : ℕ) (δ : ℝ) : ℕ :=
  n - ⌊δ * n⌋₊

/-- The integer numerator budget attached to normalized target `ε` and
challenge set `Γ`. -/
noncomputable def targetBudget (ε : ℝ) (Γ : Finset F) : ℕ :=
  ⌊ε * Γ.card⌋₊

/-- Challenge-normalized MCA error at a real closed-ball radius. -/
noncomputable def normalizedMCAAtRadius (Γ : Finset F)
    (C : Submodule F Word) (δ : ℝ) : ℝ :=
  (B_MCA_challenge Γ C (radiusAgreement (Fintype.card D) δ) : ℝ) /
    Γ.card

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- MCA badness is antitone in the agreement threshold. -/
theorem mcaBad_of_le_agreement (C : Submodule F Word)
    (f₀ f₁ : Word) (γ : F) {a b : ℕ} (hab : a ≤ b) :
    GrandeFinale.MCABad (C : Set Word) f₀ f₁ b γ →
      GrandeFinale.MCABad (C : Set Word) f₀ f₁ a γ := by
  rintro ⟨S, hSb, hline, hpair⟩
  exact ⟨S, hab.trans hSb, hline, hpair⟩

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- The restricted bad-slope set shrinks as required agreement increases. -/
theorem restrictedMCABadSlopes_subset_of_le (Γ : Finset F)
    (C : Submodule F Word) (f₀ f₁ : Word) {a b : ℕ} (hab : a ≤ b) :
    restrictedMCABadSlopes Γ C f₀ f₁ b ⊆
      restrictedMCABadSlopes Γ C f₀ f₁ a := by
  intro γ hγ
  simp only [restrictedMCABadSlopes, Finset.mem_filter] at hγ ⊢
  exact ⟨hγ.1, mcaBad_of_le_agreement C f₀ f₁ γ hab hγ.2⟩

omit [DecidableEq F] in
/-- `lem:appendix-endpoint`, monotonicity part: the exact challenge numerator
is nonincreasing in agreement. -/
theorem B_MCA_challenge_antitone (Γ : Finset F)
    (C : Submodule F Word) {a b : ℕ} (hab : a ≤ b) :
    B_MCA_challenge Γ C b ≤ B_MCA_challenge Γ C a := by
  refine Finset.sup_le ?_
  intro p hp
  exact (Finset.card_le_card
      (restrictedMCABadSlopes_subset_of_le Γ C p.1 p.2 hab)).trans
    (Finset.le_sup
      (f := fun q : Word × Word =>
        (restrictedMCABadSlopes Γ C q.1 q.2 a).card) hp)

omit [DecidableEq F] in
/-- Normalized error is at most `ε` exactly when the integer numerator is at
most `floor(ε |Γ|)`. The challenge denominator is explicit. -/
theorem normalizedMCAAtRadius_le_iff_budget
    (Γ : Finset F) (hΓ : Γ.Nonempty) (C : Submodule F Word)
    (ε δ : ℝ) (hε : 0 ≤ ε) :
    normalizedMCAAtRadius Γ C δ ≤ ε ↔
      B_MCA_challenge Γ C (radiusAgreement (Fintype.card D) δ) ≤
        targetBudget ε Γ := by
  have hΓposNat : 0 < Γ.card := Finset.card_pos.mpr hΓ
  have hΓpos : (0 : ℝ) < Γ.card := by exact_mod_cast hΓposNat
  have hprod : 0 ≤ ε * (Γ.card : ℝ) :=
    mul_nonneg hε (by positivity)
  unfold normalizedMCAAtRadius targetBudget
  rw [div_le_iff₀ hΓpos]
  exact (Nat.le_floor_iff hprod).symm

omit [DecidableEq F] in
/-- Integer first-safe conversion. If `a₀` is safe and `a₀-1` is unsafe,
then error radius `r` is safe exactly when `r ≤ n-a₀`. -/
theorem safe_errorRadius_iff (Γ : Finset F) (C : Submodule F Word)
    (budget n a₀ r : ℕ)
    (ha₀pos : 1 ≤ a₀) (ha₀n : a₀ ≤ n) (hrn : r ≤ n)
    (hsafe : B_MCA_challenge Γ C a₀ ≤ budget)
    (hunsafe : budget < B_MCA_challenge Γ C (a₀ - 1)) :
    B_MCA_challenge Γ C (n - r) ≤ budget ↔ r ≤ n - a₀ := by
  constructor
  · intro hrSafe
    by_contra hrBound
    have hagree : n - r ≤ a₀ - 1 := by omega
    have hmono :
        B_MCA_challenge Γ C (a₀ - 1) ≤
          B_MCA_challenge Γ C (n - r) :=
      B_MCA_challenge_antitone Γ C hagree
    omega
  · intro hrBound
    have hagree : a₀ ≤ n - r := by omega
    exact (B_MCA_challenge_antitone Γ C hagree).trans hsafe

/-- Natural-floor form of the closed endpoint conversion. -/
theorem floor_mul_le_iff_lt_endpoint (n a₀ : ℕ) (δ : ℝ)
    (hn : 0 < n) (hδ : 0 ≤ δ) :
    ⌊δ * n⌋₊ ≤ n - a₀ ↔
      δ < ((n - a₀ + 1 : ℕ) : ℝ) / n := by
  have hnReal : (0 : ℝ) < n := by exact_mod_cast hn
  have hmul : 0 ≤ δ * (n : ℝ) := mul_nonneg hδ hnReal.le
  rw [← Nat.lt_add_one_iff, Nat.floor_lt hmul, lt_div_iff₀ hnReal]

/-- Full real-radius endpoint conversion from `lem:appendix-endpoint`.
The hypotheses `0 ≤ δ ≤ 1` make the closed-ball radius lie in the length-`n`
grid. -/
theorem safe_realRadius_iff (Γ : Finset F) (C : Submodule F Word)
    (budget n a₀ : ℕ) (δ : ℝ)
    (hn : 0 < n) (ha₀pos : 1 ≤ a₀) (ha₀n : a₀ ≤ n)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hsafe : B_MCA_challenge Γ C a₀ ≤ budget)
    (hunsafe : budget < B_MCA_challenge Γ C (a₀ - 1)) :
    B_MCA_challenge Γ C (radiusAgreement n δ) ≤ budget ↔
      δ < ((n - a₀ + 1 : ℕ) : ℝ) / n := by
  have hnReal : (0 : ℝ) ≤ n := by positivity
  have hmulLe : δ * (n : ℝ) ≤ n := by
    have := mul_le_mul_of_nonneg_right hδ1 hnReal
    simpa using this
  have hrn : ⌊δ * n⌋₊ ≤ n := Nat.floor_le_of_le hmulLe
  unfold radiusAgreement
  rw [safe_errorRadius_iff Γ C budget n a₀ ⌊δ * n⌋₊
    ha₀pos ha₀n hrn hsafe hunsafe]
  exact floor_mul_le_iff_lt_endpoint n a₀ δ hn hδ0

omit [DecidableEq F] in
/-- Exact numerator data through radius `B-1`, together with a tangent
lower bound at radius `B`, identify the first safe agreement. -/
theorem staircase_first_safe (Γ : Finset F) (C : Submodule F Word)
    (n B : ℕ) (hBpos : 1 ≤ B) (hBΓ : B < Γ.card) (hBn : B ≤ n)
    (hstair : ∀ r : ℕ, r ≤ B - 1 →
      B_MCA_challenge Γ C (n - r) = min Γ.card (r + 1))
    (htangent : B + 1 ≤ B_MCA_challenge Γ C (n - B)) :
    B_MCA_challenge Γ C (n - B + 1) ≤ B ∧
      B < B_MCA_challenge Γ C ((n - B + 1) - 1) := by
  have hsafeEq : B_MCA_challenge Γ C (n - B + 1) = B := by
    rw [show n - B + 1 = n - (B - 1) by omega,
      hstair (B - 1) le_rfl]
    rw [show B - 1 + 1 = B by omega, min_eq_right (by omega)]
  constructor
  · omega
  · have hagree : (n - B + 1) - 1 = n - B := by omega
    rw [hagree]
    omega

/-- Generic target compiler behind both `cor:prize-window-compiler` and
`cor:half-distance-window-compiler`. -/
theorem staircase_safe_realRadius_iff (Γ : Finset F)
    (C : Submodule F Word) (n B : ℕ) (δ : ℝ)
    (hn : 0 < n) (hBpos : 1 ≤ B) (hBΓ : B < Γ.card) (hBn : B ≤ n)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hstair : ∀ r : ℕ, r ≤ B - 1 →
      B_MCA_challenge Γ C (n - r) = min Γ.card (r + 1))
    (htangent : B + 1 ≤ B_MCA_challenge Γ C (n - B)) :
    B_MCA_challenge Γ C (radiusAgreement n δ) ≤ B ↔
      δ < (B : ℝ) / n := by
  have hfirst := staircase_first_safe Γ C n B hBpos hBΓ hBn
    hstair htangent
  have ha₀pos : 1 ≤ n - B + 1 := by omega
  have ha₀n : n - B + 1 ≤ n := by omega
  have hendpoint := safe_realRadius_iff Γ C B n (n - B + 1) δ
    hn ha₀pos ha₀n hδ0 hδ1 hfirst.1 hfirst.2
  have hendpointNat : n - (n - B + 1) + 1 = B := by omega
  simpa [hendpointNat] using hendpoint

/-- Target-aware normalized form with the sampling denominator and integer
budget visible. -/
theorem normalized_target_window_of_exact_staircase
    (Γ : Finset F) (hΓ : Γ.Nonempty) (C : Submodule F Word)
    (ε : ℝ) (B : ℕ) (δ : ℝ)
    (hε : 0 ≤ ε) (hbudget : targetBudget ε Γ = B)
    (hn : 0 < Fintype.card D) (hBpos : 1 ≤ B)
    (hBΓ : B < Γ.card) (hBn : B ≤ Fintype.card D)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hstair : ∀ r : ℕ, r ≤ B - 1 →
      B_MCA_challenge Γ C (Fintype.card D - r) =
        min Γ.card (r + 1))
    (htangent : B + 1 ≤
      B_MCA_challenge Γ C (Fintype.card D - B)) :
    normalizedMCAAtRadius Γ C δ ≤ ε ↔
      δ < (B : ℝ) / Fintype.card D := by
  rw [normalizedMCAAtRadius_le_iff_budget Γ hΓ C ε δ hε, hbudget]
  exact staircase_safe_realRadius_iff Γ C (Fintype.card D) B δ
    hn hBpos hBΓ hBn hδ0 hδ1 hstair htangent

/-- `cor:half-distance-window-compiler`: any certified exact staircase
through radius `R` compiles to the complete target window whenever the
integer budget satisfies `B ≤ R + 1`. -/
theorem half_distance_target_window
    (Γ : Finset F) (hΓ : Γ.Nonempty) (C : Submodule F Word)
    (ε : ℝ) (B R : ℕ) (δ : ℝ)
    (hε : 0 ≤ ε) (hbudget : targetBudget ε Γ = B)
    (hn : 0 < Fintype.card D) (hBpos : 1 ≤ B)
    (hBΓ : B < Γ.card) (hBn : B ≤ Fintype.card D)
    (hBR : B ≤ R + 1) (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hstair : ∀ r : ℕ, r ≤ R →
      B_MCA_challenge Γ C (Fintype.card D - r) =
        min Γ.card (r + 1))
    (htangent : B + 1 ≤
      B_MCA_challenge Γ C (Fintype.card D - B)) :
    normalizedMCAAtRadius Γ C δ ≤ ε ↔
      δ < (B : ℝ) / Fintype.card D := by
  apply normalized_target_window_of_exact_staircase
    Γ hΓ C ε B δ hε hbudget hn hBpos hBΓ hBn hδ0 hδ1
  · intro r hr
    exact hstair r (by omega)
  · exact htangent

omit [DecidableEq F] in
/-- A zero integer target budget is already violated at radius zero whenever
the tangent numerator is nonzero. This is the degenerate branch of the
target compiler. -/
theorem zero_budget_radius_zero_unsafe
    (Γ : Finset F) (hΓ : Γ.Nonempty) (C : Submodule F Word)
    (ε : ℝ) (hε : 0 ≤ ε) (hbudget : targetBudget ε Γ = 0)
    (htangent : 1 ≤ B_MCA_challenge Γ C (Fintype.card D)) :
    ε < normalizedMCAAtRadius Γ C 0 := by
  apply lt_of_not_ge
  intro hsafe
  have hnum := (normalizedMCAAtRadius_le_iff_budget
    Γ hΓ C ε 0 hε).mp hsafe
  rw [hbudget] at hnum
  simp only [radiusAgreement, zero_mul, Nat.floor_zero, Nat.sub_zero] at hnum
  omega

/-- `cor:prize-window-compiler` specialized to the exact quadratic
Reed--Solomon staircase. The integer target budget is the first unsafe
radius, so the safe closed-ball radii form the open interval `[0, B / n)`. -/
theorem rs_quadratic_target_window
    (Γ : Finset F) (hΓ : Γ.Nonempty)
    (dom : D → F) (hdom : Function.Injective dom) (k : ℕ)
    (ε : ℝ) (B : ℕ) (δ : ℝ)
    (hε : 0 ≤ ε) (hbudget : targetBudget ε Γ = B)
    (hk : k < Fintype.card D) (hBpos : 1 ≤ B)
    (hBΓ : B < Γ.card)
    (hBroot : B - 1 ≤
      ⌊QuadraticStaircase.quadraticRoot (Fintype.card D) k⌋₊)
    (hBdist : B ≤ Fintype.card D - k - 1)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) :
    normalizedMCAAtRadius Γ (RSCap.RSpolySubmodule dom k) δ ≤ ε ↔
      δ < (B : ℝ) / Fintype.card D := by
  have hn : 0 < Fintype.card D := by omega
  have hBn : B ≤ Fintype.card D := by omega
  have hstair : ∀ r : ℕ, r ≤ B - 1 →
      B_MCA_challenge Γ (RSCap.RSpolySubmodule dom k)
          (Fintype.card D - r) = min Γ.card (r + 1) := by
    intro r hr
    exact QuadraticStaircase.rs_quadratic_staircase_exact
      Γ hΓ dom hdom k r hk (hr.trans hBroot)
  have hka : k + 1 ≤ Fintype.card D - B := by omega
  have htangentRaw := QuadraticMeanOverlap.rs_hasTangentLower
    Γ dom hdom k B hBn hka
  have htangent : B + 1 ≤
      B_MCA_challenge Γ (RSCap.RSpolySubmodule dom k)
        (Fintype.card D - B) := by
    simpa [QuadraticMeanOverlap.HasTangentLower,
      min_eq_right (Nat.succ_le_iff.mpr hBΓ)] using htangentRaw
  exact normalized_target_window_of_exact_staircase
    Γ hΓ (RSCap.RSpolySubmodule dom k) ε B δ hε hbudget hn
      hBpos hBΓ hBn hδ0 hδ1 hstair htangent

/-- For an injective Reed--Solomon evaluation code, the universal tangent
construction supplies the nonzero numerator needed by the zero-budget
branch. -/
theorem rs_zero_budget_radius_zero_unsafe
    (Γ : Finset F) (hΓ : Γ.Nonempty)
    (dom : D → F) (hdom : Function.Injective dom) (k : ℕ)
    (ε : ℝ) (hε : 0 ≤ ε) (hbudget : targetBudget ε Γ = 0)
    (hk : k < Fintype.card D) :
    ε < normalizedMCAAtRadius Γ (RSCap.RSpolySubmodule dom k) 0 := by
  have htangentRaw := QuadraticMeanOverlap.rs_hasTangentLower
    Γ dom hdom k 0 (Nat.zero_le _) (by omega)
  have htangent : 1 ≤
      B_MCA_challenge Γ (RSCap.RSpolySubmodule dom k)
        (Fintype.card D) := by
    simpa [QuadraticMeanOverlap.HasTangentLower,
      min_eq_right (Finset.one_le_card.mpr hΓ)] using htangentRaw
  exact zero_budget_radius_zero_unsafe Γ hΓ
    (RSCap.RSpolySubmodule dom k) ε hε hbudget htangent

#print axioms B_MCA_challenge_antitone
#print axioms normalizedMCAAtRadius_le_iff_budget
#print axioms safe_errorRadius_iff
#print axioms safe_realRadius_iff
#print axioms staircase_first_safe
#print axioms normalized_target_window_of_exact_staircase
#print axioms half_distance_target_window
#print axioms rs_quadratic_target_window
#print axioms rs_zero_budget_radius_zero_unsafe

end EndpointCompiler
end RsMcaThresholds
