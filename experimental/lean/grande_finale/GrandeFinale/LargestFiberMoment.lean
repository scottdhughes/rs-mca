import GrandeFinale.QEntropyInverse

/-!
# Largest fibers and normalized moments

This module formalizes the exact finite inequalities in
`lem:largest-fiber-log-detail` and `lem:q-to-sp-detail` of
`experimental/asymptotic_rs_mca_frontiers.tex`.

The source states the claims for nonnegative integer fiber sizes. The Lean
statements prove the stronger real-valued form for arbitrary finite
nonnegative fibers.
-/

open scoped BigOperators

noncomputable section

namespace GrandeFinale.LargestFiberMoment

/-- The average fiber size over the full finite target set. -/
def fiberMean {ι : Type*} (S : Finset ι) (N : ι → ℝ) : ℝ :=
  (∑ s ∈ S, N s) / S.card

/-- The image-normalized `q`-moment of the fiber sizes. -/
def normalizedMoment {ι : Type*}
    (S : Finset ι) (N : ι → ℝ) (q : Nat) : ℝ :=
  (∑ s ∈ S, (N s / fiberMean S N) ^ q) / S.card

/-- The normalized ratio at a selected largest fiber. -/
def largestFiberRatio {ι : Type*}
    (S : Finset ι) (N : ι → ℝ) (smax : ι) : ℝ :=
  N smax / fiberMean S N

/-- Positive total mass on a nonempty target set gives positive mean. -/
theorem fiberMean_pos {ι : Type*} {S : Finset ι} {N : ι → ℝ}
    (hS : S.Nonempty) (htotal : 0 < ∑ s ∈ S, N s) :
    0 < fiberMean S N := by
  unfold fiberMean
  exact div_pos htotal (by exact_mod_cast hS.card_pos)

/-- Normalizing by the exact mean makes the total normalized mass equal to
the number of targets. -/
theorem sum_div_fiberMean_eq_card {ι : Type*}
    {S : Finset ι} {N : ι → ℝ}
    (hS : S.Nonempty) (htotal : 0 < ∑ s ∈ S, N s) :
    ∑ s ∈ S, N s / fiberMean S N = S.card := by
  rw [← Finset.sum_div]
  unfold fiberMean
  field_simp [htotal.ne', Nat.ne_of_gt hS.card_pos]

/-- The selected largest fiber contributes the lower normalized-moment bound
`R^q / L`. -/
theorem largestFiberRatio_pow_div_card_le_normalizedMoment
    {ι : Type*} {S : Finset ι} {N : ι → ℝ}
    (hN : ∀ s ∈ S, 0 ≤ N s)
    {smax : ι} (hsmax : smax ∈ S)
    (htotal : 0 < ∑ s ∈ S, N s) (q : Nat) :
    largestFiberRatio S N smax ^ q / S.card ≤
      normalizedMoment S N q := by
  have hS : S.Nonempty := ⟨smax, hsmax⟩
  have hmean : 0 < fiberMean S N := fiberMean_pos hS htotal
  unfold largestFiberRatio normalizedMoment
  apply div_le_div_of_nonneg_right
  · exact Finset.single_le_sum
      (fun s hs ↦ pow_nonneg (div_nonneg (hN s hs) hmean.le) q) hsmax
  · exact_mod_cast (Nat.zero_le S.card)

/-- The normalized `q`-moment is at most `R^(q-1)` when `R` is the
largest normalized fiber ratio. -/
theorem normalizedMoment_le_largestFiberRatio_pow_pred
    {ι : Type*} {S : Finset ι} {N : ι → ℝ}
    (hN : ∀ s ∈ S, 0 ≤ N s)
    {smax : ι} (hsmax : smax ∈ S)
    (hmax : ∀ s ∈ S, N s ≤ N smax)
    (htotal : 0 < ∑ s ∈ S, N s)
    (q : Nat) (hq : 1 ≤ q) :
    normalizedMoment S N q ≤
      largestFiberRatio S N smax ^ (q - 1) := by
  have hS : S.Nonempty := ⟨smax, hsmax⟩
  have hmean : 0 < fiberMean S N := fiberMean_pos hS htotal
  have hmass :
      ∑ s ∈ S, N s / fiberMean S N ≤ (S.card : ℝ) := by
    exact (sum_div_fiberMean_eq_card hS htotal).le
  have hmoment := QEntropyInverse.collision_moment_le_of_max
    S (fun s ↦ N s / fiberMean S N)
    (fun s hs ↦ div_nonneg (hN s hs) hmean.le)
    (S.card : ℝ) (by exact_mod_cast hS.card_pos)
    hmass (largestFiberRatio S N smax)
    (div_nonneg (hN smax hsmax) hmean.le)
    (fun s hs ↦ div_le_div_of_nonneg_right (hmax s hs) hmean.le)
    q hq
  simpa [normalizedMoment, largestFiberRatio,
    QFourierTao.collisionMoment, div_eq_inv_mul] using hmoment

/-- The two exact normalized moment inequalities from
`lem:largest-fiber-log-detail`. -/
theorem largestFiber_normalizedMoment_bounds
    {ι : Type*} {S : Finset ι} {N : ι → ℝ}
    (hN : ∀ s ∈ S, 0 ≤ N s)
    {smax : ι} (hsmax : smax ∈ S)
    (hmax : ∀ s ∈ S, N s ≤ N smax)
    (htotal : 0 < ∑ s ∈ S, N s)
    (q : Nat) (hq : 2 ≤ q) :
    largestFiberRatio S N smax ^ q / S.card ≤
        normalizedMoment S N q ∧
      normalizedMoment S N q ≤
        largestFiberRatio S N smax ^ (q - 1) := by
  exact ⟨largestFiberRatio_pow_div_card_le_normalizedMoment
      hN hsmax htotal q,
    normalizedMoment_le_largestFiberRatio_pow_pred
      hN hsmax hmax htotal q (by omega)⟩

/-- Finite logarithmic form of the lower moment bound:
`q log R - log L <= log(moment)`. -/
theorem q_mul_log_largestFiberRatio_sub_log_card_le_log_normalizedMoment
    {ι : Type*} {S : Finset ι} {N : ι → ℝ}
    (hN : ∀ s ∈ S, 0 ≤ N s)
    {smax : ι} (hsmax : smax ∈ S)
    (hmaxpos : 0 < N smax)
    (htotal : 0 < ∑ s ∈ S, N s) (q : Nat) :
    (q : ℝ) * Real.log (largestFiberRatio S N smax) -
        Real.log S.card ≤
      Real.log (normalizedMoment S N q) := by
  have hS : S.Nonempty := ⟨smax, hsmax⟩
  have hmean : 0 < fiberMean S N := fiberMean_pos hS htotal
  have hratio : 0 < largestFiberRatio S N smax :=
    div_pos hmaxpos hmean
  have hcard : 0 < (S.card : ℝ) := by exact_mod_cast hS.card_pos
  have hlower := largestFiberRatio_pow_div_card_le_normalizedMoment
    hN hsmax htotal q
  have hleft :
      0 < largestFiberRatio S N smax ^ q / (S.card : ℝ) :=
    div_pos (pow_pos hratio q) hcard
  have hlog := Real.log_le_log hleft hlower
  rw [Real.log_div (pow_ne_zero q hratio.ne') hcard.ne',
    Real.log_pow] at hlog
  exact hlog

/-- Cleared Q-to-SP second-moment inequality:
`sum N^2 <= kappa * mean * sum N`. -/
theorem sum_sq_le_kappa_mul_mean_mul_sum
    {ι : Type*} {S : Finset ι} {N : ι → ℝ}
    (hN : ∀ s ∈ S, 0 ≤ N s)
    (κ : ℝ)
    (hmax : ∀ s ∈ S, N s ≤ κ * fiberMean S N) :
    ∑ s ∈ S, N s ^ 2 ≤
      κ * fiberMean S N * ∑ s ∈ S, N s := by
  calc
    ∑ s ∈ S, N s ^ 2 ≤
        ∑ s ∈ S, (κ * fiberMean S N) * N s := by
      apply Finset.sum_le_sum
      intro s hs
      simpa [pow_two] using
        mul_le_mul_of_nonneg_right (hmax s hs) (hN s hs)
    _ = κ * fiberMean S N * ∑ s ∈ S, N s := by
      rw [Finset.mul_sum]

/-- Exact normalized Q-to-SP statement:
`M⁻¹ sum N^2 <= kappa * mean`. -/
theorem secondMoment_div_total_le_kappa_mul_mean
    {ι : Type*} {S : Finset ι} {N : ι → ℝ}
    (hN : ∀ s ∈ S, 0 ≤ N s)
    (htotal : 0 < ∑ s ∈ S, N s)
    (κ : ℝ)
    (hmax : ∀ s ∈ S, N s ≤ κ * fiberMean S N) :
    (∑ s ∈ S, N s ^ 2) / (∑ s ∈ S, N s) ≤
      κ * fiberMean S N := by
  rw [div_le_iff₀ htotal]
  exact sum_sq_le_kappa_mul_mean_mul_sum hN κ hmax

#print axioms largestFiber_normalizedMoment_bounds
#print axioms q_mul_log_largestFiberRatio_sub_log_card_le_log_normalizedMoment
#print axioms secondMoment_div_total_le_kappa_mul_mean

end GrandeFinale.LargestFiberMoment
