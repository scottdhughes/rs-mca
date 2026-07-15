import Mathlib

/-!
# Power-weighted second-moment concentration floor

This module formalizes the proved concentration-floor lemma from
`experimental/notes/thresholds/cap25_v13_q_pw2_concentration_floor.md`.

For nonnegative target weights `X` supported on a finite set `s`, the
cleared Cauchy--Schwarz inequality is

```
(total mass)^2 <= |s| * (second moment).
```

Consequently, if the target universe has size at most `P`, then every
square-root second-moment certificate is at least
`total mass / sqrt P`.  Taking `P = p^w` gives the power-weighted floor
used by the source note, globally or on any individual stratum.

The deployed-row numerical margins are checked by the source verifier rather
than recomputed here.  The note's empirical typical-stratum assertion and its
open signed-`L¹` inverse route are not consequences of this module.
-/

namespace MomentToMax.PowerWeightedConcentrationFloor

open Finset BigOperators

/-- Total mass of a real-valued family on a finite target set. -/
def totalMass {ι : Type*} (s : Finset ι) (X : ι → ℝ) : ℝ :=
  ∑ i ∈ s, X i

/-- Unnormalized second moment of a real-valued family. -/
def secondMoment {ι : Type*} (s : Finset ι) (X : ι → ℝ) : ℝ :=
  ∑ i ∈ s, (X i) ^ 2

/-- Total mass for a family of exact natural-number target counts. -/
def natMass {ι : Type*} (s : Finset ι) (X : ι → ℕ) : ℕ :=
  ∑ i ∈ s, X i

/-- Exact natural-number second moment. -/
def natSecondMoment {ι : Type*} (s : Finset ι) (X : ι → ℕ) : ℕ :=
  ∑ i ∈ s, (X i) ^ 2

theorem secondMoment_nonneg {ι : Type*} (s : Finset ι) (X : ι → ℝ) :
    0 ≤ secondMoment s X := by
  apply Finset.sum_nonneg
  intro i hi
  positivity

theorem totalMass_nonneg {ι : Type*} (s : Finset ι) (X : ι → ℝ)
    (hX : ∀ i ∈ s, 0 ≤ X i) :
    0 ≤ totalMass s X := by
  exact Finset.sum_nonneg hX

/--
The exact cleared Cauchy--Schwarz floor, with the actual support cardinality.
No sign hypothesis is required in this squared form.
-/
theorem cauchySchwarz_floor {ι : Type*} (s : Finset ι) (X : ι → ℝ) :
    (totalMass s X) ^ 2 ≤ (s.card : ℝ) * secondMoment s X := by
  simpa [totalMass, secondMoment] using
    (sq_sum_le_card_mul_sum_sq (s := s) (f := X))

/--
Replace the actual target-set cardinality by any natural upper bound `P`.
-/
theorem cauchySchwarz_floor_of_card_le {ι : Type*} (s : Finset ι)
    (X : ι → ℝ) {P : ℕ} (hcard : s.card ≤ P) :
    (totalMass s X) ^ 2 ≤ (P : ℝ) * secondMoment s X := by
  calc
    (totalMass s X) ^ 2 ≤ (s.card : ℝ) * secondMoment s X :=
      cauchySchwarz_floor s X
    _ ≤ (P : ℝ) * secondMoment s X := by
      apply mul_le_mul_of_nonneg_right
      · exact_mod_cast hcard
      · exact secondMoment_nonneg s X

/--
Exact natural-number form for per-target counts.
-/
theorem nat_cauchySchwarz_floor_of_card_le {ι : Type*} (s : Finset ι)
    (X : ι → ℕ) {P : ℕ} (hcard : s.card ≤ P) :
    (natMass s X) ^ 2 ≤ P * natSecondMoment s X := by
  have hreal :=
    cauchySchwarz_floor_of_card_le s (fun i => (X i : ℝ)) hcard
  have hcast :
      ((natMass s X : ℕ) : ℝ) ^ 2 ≤
        (P : ℝ) * ((natSecondMoment s X : ℕ) : ℝ) := by
    simpa [natMass, totalMass, natSecondMoment, secondMoment] using hreal
  exact_mod_cast hcast

/--
Power-sized target-universe specialization of the exact count inequality.
-/
theorem nat_power_target_floor {ι : Type*} (s : Finset ι)
    (X : ι → ℕ) {p w : ℕ} (hcard : s.card ≤ p ^ w) :
    (natMass s X) ^ 2 ≤ p ^ w * natSecondMoment s X :=
  nat_cauchySchwarz_floor_of_card_le s X hcard

/--
The cleared floor implies a square-root upper envelope for total mass.
-/
theorem totalMass_le_sqrt_capacity_mul_secondMoment {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {P : ℕ}
    (hX : ∀ i ∈ s, 0 ≤ X i) (hcard : s.card ≤ P) :
    totalMass s X ≤ Real.sqrt ((P : ℝ) * secondMoment s X) := by
  apply (Real.le_sqrt (totalMass_nonneg s X hX)
    (mul_nonneg (by positivity) (secondMoment_nonneg s X))).2
  exact cauchySchwarz_floor_of_card_le s X hcard

/--
Normalized second-moment floor:
`mass / sqrt P <= sqrt(second moment)`.
-/
theorem normalizedMass_le_sqrtSecondMoment {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {P : ℕ}
    (hP : 0 < P) (hX : ∀ i ∈ s, 0 ≤ X i)
    (hcard : s.card ≤ P) :
    totalMass s X / Real.sqrt (P : ℝ) ≤
      Real.sqrt (secondMoment s X) := by
  have hP_real : (0 : ℝ) < P := by exact_mod_cast hP
  rw [div_le_iff₀ (Real.sqrt_pos.2 hP_real)]
  calc
    totalMass s X ≤ Real.sqrt ((P : ℝ) * secondMoment s X) :=
      totalMass_le_sqrt_capacity_mul_secondMoment s X hX hcard
    _ = Real.sqrt (P : ℝ) * Real.sqrt (secondMoment s X) :=
      Real.sqrt_mul hP_real.le _
    _ = Real.sqrt (secondMoment s X) * Real.sqrt (P : ℝ) := by
      ring

/--
The literal support/cardinality chain from the source proof. A caller may
take `s` to be the finite set of nonzero targets:
`mass / sqrt P <= mass / sqrt |s| <= sqrt(second moment)`.
-/
theorem support_capacity_floor_chain {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {P : ℕ}
    (hs : s.Nonempty) (hX : ∀ i ∈ s, 0 ≤ X i)
    (hcard : s.card ≤ P) :
    totalMass s X / Real.sqrt (P : ℝ) ≤
        totalMass s X / Real.sqrt (s.card : ℝ) ∧
      totalMass s X / Real.sqrt (s.card : ℝ) ≤
        Real.sqrt (secondMoment s X) := by
  have hcard_pos : 0 < s.card := Finset.card_pos.mpr hs
  have hcard_real : (0 : ℝ) < s.card := by exact_mod_cast hcard_pos
  have hcard_cast : (s.card : ℝ) ≤ P := by exact_mod_cast hcard
  have hsqrt :
      Real.sqrt (s.card : ℝ) ≤ Real.sqrt (P : ℝ) :=
    Real.sqrt_le_sqrt hcard_cast
  constructor
  · exact div_le_div_of_nonneg_left
      (totalMass_nonneg s X hX) (Real.sqrt_pos.2 hcard_real) hsqrt
  · exact normalizedMass_le_sqrtSecondMoment s X hcard_pos hX le_rfl

/--
If `R` is an `r=2` certificate, meaning
`secondMoment <= R^2`, then it cannot lie below the concentration floor.
-/
theorem normalizedMass_le_of_secondMoment_le_sq {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {P : ℕ} {R : ℝ}
    (hP : 0 < P) (hR : 0 ≤ R)
    (hX : ∀ i ∈ s, 0 ≤ X i) (hcard : s.card ≤ P)
    (hsecond : secondMoment s X ≤ R ^ 2) :
    totalMass s X / Real.sqrt (P : ℝ) ≤ R := by
  calc
    totalMass s X / Real.sqrt (P : ℝ) ≤
        Real.sqrt (secondMoment s X) :=
      normalizedMass_le_sqrtSecondMoment s X hP hX hcard
    _ ≤ R := (Real.sqrt_le_iff).2 ⟨hR, hsecond⟩

/--
Contrapositive certificate form: below-floor `R` cannot upper-bound the
second moment.
-/
theorem secondMoment_not_le_sq_of_below_floor {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {P : ℕ} {R : ℝ}
    (hP : 0 < P) (hR : 0 ≤ R)
    (hX : ∀ i ∈ s, 0 ≤ X i) (hcard : s.card ≤ P)
    (hbelow : R < totalMass s X / Real.sqrt (P : ℝ)) :
    ¬ secondMoment s X ≤ R ^ 2 := by
  intro hsecond
  exact (not_le_of_gt hbelow)
    (normalizedMass_le_of_secondMoment_le_sq s X hP hR hX hcard hsecond)

/--
Per-stratum form.  If a stratum's mass exceeds `T * sqrt P`, then its
square-root second moment exceeds `T`.
-/
theorem sqrtSecondMoment_gt_of_capacity_sqrt_mul_lt_mass {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {P : ℕ} {T : ℝ}
    (hP : 0 < P) (hX : ∀ i ∈ s, 0 ≤ X i)
    (hcard : s.card ≤ P)
    (hmass : T * Real.sqrt (P : ℝ) < totalMass s X) :
    T < Real.sqrt (secondMoment s X) := by
  have hP_real : (0 : ℝ) < P := by exact_mod_cast hP
  have hbelow :
      T < totalMass s X / Real.sqrt (P : ℝ) := by
    exact (lt_div_iff₀ (Real.sqrt_pos.2 hP_real)).2 hmass
  exact lt_of_lt_of_le hbelow
    (normalizedMass_le_sqrtSecondMoment s X hP hX hcard)

/--
The source note's power-weighted normalized floor, with `P = p^w`.
-/
theorem power_target_normalized_floor {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {p w : ℕ}
    (hp : 0 < p) (hX : ∀ i ∈ s, 0 ≤ X i)
    (hcard : s.card ≤ p ^ w) :
    totalMass s X / Real.sqrt ((p ^ w : ℕ) : ℝ) ≤
      Real.sqrt (secondMoment s X) := by
  exact normalizedMass_le_sqrtSecondMoment s X
    (pow_pos hp w) hX hcard

/--
Power-weighted per-stratum obstruction.
-/
theorem power_target_sqrtSecondMoment_gt {ι : Type*}
    (s : Finset ι) (X : ι → ℝ) {p w : ℕ} {T : ℝ}
    (hp : 0 < p) (hX : ∀ i ∈ s, 0 ≤ X i)
    (hcard : s.card ≤ p ^ w)
    (hmass : T * Real.sqrt ((p ^ w : ℕ) : ℝ) < totalMass s X) :
    T < Real.sqrt (secondMoment s X) := by
  exact sqrtSecondMoment_gt_of_capacity_sqrt_mul_lt_mass s X
    (pow_pos hp w) hX hcard hmass

#print axioms cauchySchwarz_floor
#print axioms nat_power_target_floor
#print axioms normalizedMass_le_sqrtSecondMoment
#print axioms support_capacity_floor_chain
#print axioms normalizedMass_le_of_secondMoment_le_sq
#print axioms sqrtSecondMoment_gt_of_capacity_sqrt_mul_lt_mass
#print axioms power_target_sqrtSecondMoment_gt

end MomentToMax.PowerWeightedConcentrationFloor
