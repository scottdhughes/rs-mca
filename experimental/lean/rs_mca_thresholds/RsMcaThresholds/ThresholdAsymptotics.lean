import RsMcaThresholds.EndpointCompiler
import Mathlib.Analysis.Asymptotics.Lemmas
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# Asymptotic threshold compiler

This file formalizes the certificate-crossing argument in
thm:intro-delta-formula from experimental/rs_mca_thresholds.tex.
-/

open scoped Classical Topology
open Filter Asymptotics

noncomputable section

namespace RsMcaThresholds
namespace ThresholdAsymptotics

set_option autoImplicit false

/-- A safe predicate has first safe agreement a₀ when a₀ is safe and
no safe agreement is smaller. -/
def IsFirstSafe (safe : ℕ → Prop) (a₀ : ℕ) : Prop :=
  safe a₀ ∧ ∀ ⦃a : ℕ⦄, safe a → a₀ ≤ a

/-- Finite crossing squeeze behind the first assertion of
thm:intro-delta-formula. Integer rounding costs less than one agreement
coordinate. -/
theorem firstSafeAgreement_crossing_bounds
    (safe : ℕ → Prop) (a₀ k n : ℕ) (g η : ℝ)
    (hfirst : IsFirstSafe safe a₀) (hmono : Monotone safe)
    (hn : 0 < n) (hg : 0 ≤ g) (hη : 0 < η)
    (hsafe : ∀ a : ℕ,
      ((k + 1 : ℕ) : ℝ) + (g + η) * n ≤ a → safe a)
    (hunsafe : ∀ a : ℕ,
      (a : ℝ) ≤ ((k + 1 : ℕ) : ℝ) + (g - η) * n → ¬ safe a) :
    ((k + 1 : ℕ) : ℝ) + (g - η) * n < a₀ ∧
      (a₀ : ℝ) < ((k + 1 : ℕ) : ℝ) + (g + η) * n + 1 := by
  let lower : ℝ := ((k + 1 : ℕ) : ℝ) + (g - η) * n
  let upper : ℝ := ((k + 1 : ℕ) : ℝ) + (g + η) * n
  have hlower : lower < (a₀ : ℝ) := by
    by_cases hlower0 : 0 ≤ lower
    · have hfloorUnsafe : ¬ safe ⌊lower⌋₊ :=
        hunsafe ⌊lower⌋₊ (by simpa [lower] using Nat.floor_le hlower0)
      have hfloorLt : ⌊lower⌋₊ < a₀ := by
        by_contra hnot
        have ha₀floor : a₀ ≤ ⌊lower⌋₊ := Nat.le_of_not_gt hnot
        exact hfloorUnsafe (hmono ha₀floor hfirst.1)
      have hsucc : ((⌊lower⌋₊ + 1 : ℕ) : ℝ) ≤ a₀ := by
        exact_mod_cast Nat.succ_le_of_lt hfloorLt
      exact (Nat.lt_floor_add_one lower).trans_le (by simpa using hsucc)
    · exact (lt_of_not_ge hlower0).trans_le (Nat.cast_nonneg a₀)
  have hupper0 : 0 ≤ upper := by
    dsimp [upper]
    positivity
  have hceilSafe : safe ⌈upper⌉₊ :=
    hsafe ⌈upper⌉₊ (by simpa [upper] using Nat.le_ceil upper)
  have ha₀ceil : a₀ ≤ ⌈upper⌉₊ := hfirst.2 hceilSafe
  have hupper : (a₀ : ℝ) < upper + 1 :=
    (Nat.cast_le.mpr ha₀ceil).trans_lt (Nat.ceil_lt_add_one hupper0)
  exact ⟨by simpa [lower] using hlower, by simpa [upper] using hupper⟩

/-- Matching safe and unsafe certificate crossings force the first safe
agreement to equal k + 1 + g n + o(n). This is the analytic core of
thm:intro-delta-formula. -/
theorem firstSafeAgreement_isLittleO
    (n k a₀ : ℕ → ℕ) (g : ℕ → ℝ)
    (safe : ℕ → ℕ → Prop)
    (hn : ∀ i, 0 < n i) (hntop : Tendsto n atTop atTop)
    (hg : ∀ i, 0 ≤ g i)
    (hfirst : ∀ i, IsFirstSafe (safe i) (a₀ i))
    (hmono : ∀ i, Monotone (safe i))
    (hsafeCross : ∀ η : ℝ, 0 < η → ∀ᶠ i in atTop, ∀ b : ℕ,
      ((k i + 1 : ℕ) : ℝ) + (g i + η) * n i ≤ b → safe i b)
    (hunsafeCross : ∀ η : ℝ, 0 < η → ∀ᶠ i in atTop, ∀ b : ℕ,
      (b : ℝ) ≤ ((k i + 1 : ℕ) : ℝ) + (g i - η) * n i →
        ¬ safe i b) :
    (fun i => (a₀ i : ℝ) - ((k i + 1 : ℕ) : ℝ) -
        g i * (n i : ℝ)) =o[atTop]
      (fun i => (n i : ℝ)) := by
  have hnRealTop : Tendsto (fun i => (n i : ℝ)) atTop atTop :=
    tendsto_natCast_atTop_atTop.comp hntop
  have hratio : Tendsto
      (fun i => ((a₀ i : ℝ) - ((k i + 1 : ℕ) : ℝ) -
        g i * (n i : ℝ)) / (n i : ℝ))
      atTop (𝓝 0) := by
    refine Metric.tendsto_atTop.2 ?_
    intro ε hε
    rw [← eventually_atTop]
    have hsafeEventually := hsafeCross (ε / 4) (by positivity)
    have hunsafeEventually := hunsafeCross (ε / 4) (by positivity)
    have hlarge : ∀ᶠ i in atTop, (2 : ℝ) / ε < (n i : ℝ) :=
      hnRealTop.eventually (eventually_gt_atTop ((2 : ℝ) / ε))
    filter_upwards [hsafeEventually, hunsafeEventually, hlarge] with
      i hsafeI hunsafeI hlargeI
    have hbounds := firstSafeAgreement_crossing_bounds
      (safe i) (a₀ i) (k i) (n i) (g i) (ε / 4)
      (hfirst i) (hmono i) (hn i) (hg i) (by positivity)
      hsafeI hunsafeI
    have hnR : (0 : ℝ) < n i := by exact_mod_cast hn i
    have htwo : (2 : ℝ) < (n i : ℝ) * ε :=
      (div_lt_iff₀ hε).mp hlargeI
    rw [Real.dist_eq, sub_zero, abs_lt]
    constructor
    · rw [lt_div_iff₀ hnR]
      nlinarith [hbounds.1]
    · rw [div_lt_iff₀ hnR]
      nlinarith [hbounds.2]
  refine (isLittleO_iff_tendsto
    (fun i hzero => ?_)).2 hratio
  exact False.elim
    ((Nat.cast_ne_zero.mpr (Nat.ne_of_gt (hn i))) hzero)

/-- The o(n) agreement formula and convergence of k/n imply the
normalized radius formula δ = 1 - ρ - g + o(1). -/
theorem certificateRadius_tendsto
    (n k a₀ : ℕ → ℕ) (g : ℕ → ℝ) (ρ : ℝ)
    (hn : ∀ i, 0 < n i) (hntop : Tendsto n atTop atTop)
    (hthreshold :
      (fun i => (a₀ i : ℝ) - ((k i + 1 : ℕ) : ℝ) -
          g i * (n i : ℝ)) =o[atTop]
        (fun i => (n i : ℝ)))
    (hkRate : Tendsto
      (fun i => (k i : ℝ) / (n i : ℝ)) atTop (𝓝 ρ)) :
    Tendsto
      (fun i => (1 - (a₀ i : ℝ) / (n i : ℝ)) -
        (1 - ρ - g i)) atTop (𝓝 0) := by
  have hconst : Tendsto (fun _ : ℕ => ρ) atTop (𝓝 ρ) :=
    tendsto_const_nhds
  have hrateError : Tendsto
      (fun i => ρ - (k i : ℝ) / (n i : ℝ)) atTop (𝓝 0) := by
    simpa using hconst.sub hkRate
  have hone : Tendsto (fun i => (1 : ℝ) / (n i : ℝ))
      atTop (𝓝 0) :=
    (tendsto_const_div_atTop_nhds_zero_nat (1 : ℝ)).comp hntop
  have herror := hthreshold.tendsto_div_nhds_zero
  have hcombined : Tendsto
      (fun i => (ρ - (k i : ℝ) / (n i : ℝ)) -
        (1 : ℝ) / (n i : ℝ) -
        ((a₀ i : ℝ) - ((k i + 1 : ℕ) : ℝ) -
          g i * (n i : ℝ)) / (n i : ℝ))
      atTop (𝓝 0) := by
    simpa using (hrateError.sub hone).sub herror
  refine hcombined.congr' (Eventually.of_forall fun i => ?_)
  have hn0 : (n i : ℝ) ≠ 0 :=
    Nat.cast_ne_zero.mpr (Nat.ne_of_gt (hn i))
  field_simp [hn0]
  push_cast
  ring

#print axioms firstSafeAgreement_crossing_bounds
#print axioms firstSafeAgreement_isLittleO
#print axioms certificateRadius_tendsto

end ThresholdAsymptotics
end RsMcaThresholds
