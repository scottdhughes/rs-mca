import Mathlib

/-!
# Degree-two interval moment-map max fibres

This module formalizes the proved R2 core of
`experimental/notes/thresholds/moment_map_max_fiber.md`.

For the interval block `{0, ..., b-1}`, every Boolean subset has signature
`(|S|, sum S, sum x^2)`.  The signatures lie in the exact finite box printed
in the note.  A finite-fibre double count proves that the largest fibre pays
only a polynomial loss:

`2^b <= B(b) * fstar(b) <= b^6 * fstar(b)` for `b >= 2`.

The later local-CLT claim with exponent `9/2` is measured in the source note
and is deliberately not promoted here.
-/

namespace MomentToMax.MomentMapMaxFiber

open Finset BigOperators Filter

abbrev Signature := Nat × Nat × Nat

def intervalSubsets (b : Nat) : Finset (Finset Nat) :=
  (Finset.range b).powerset

def signature (S : Finset Nat) : Signature :=
  (S.card, (∑ x ∈ S, x, ∑ x ∈ S, x * x))

def linearCap (b : Nat) : Nat :=
  ∑ x ∈ Finset.range b, x

def squareCap (b : Nat) : Nat :=
  ∑ x ∈ Finset.range b, x * x

def signatureBox (b : Nat) : Finset Signature :=
  (Finset.range (b + 1)).product
    ((Finset.range (linearCap b + 1)).product
      (Finset.range (squareCap b + 1)))

def boxCard (b : Nat) : Nat :=
  (b + 1) * (linearCap b + 1) * (squareCap b + 1)

def intervalFiber (b : Nat) (z : Signature) : Finset (Finset Nat) :=
  (intervalSubsets b).filter fun S => signature S = z

def intervalMaxFiber (b : Nat) : Nat :=
  (signatureBox b).sup fun z => (intervalFiber b z).card

theorem intervalSubsets_card (b : Nat) :
    (intervalSubsets b).card = 2 ^ b := by
  simp [intervalSubsets]

theorem signatureBox_card (b : Nat) :
    (signatureBox b).card = boxCard b := by
  simp [signatureBox, boxCard, Nat.mul_assoc]

theorem signature_mem_box {b : Nat} {S : Finset Nat}
    (hS : S ∈ intervalSubsets b) :
    signature S ∈ signatureBox b := by
  have hsub : S ⊆ Finset.range b := by
    simpa [intervalSubsets] using hS
  have hcard : S.card ≤ b := by
    simpa using Finset.card_le_card hsub
  have hlin : (∑ x ∈ S, x) ≤ linearCap b := by
    exact Finset.sum_le_sum_of_subset_of_nonneg hsub
      (fun _ _ _ => Nat.zero_le _)
  have hsq : (∑ x ∈ S, x * x) ≤ squareCap b := by
    exact Finset.sum_le_sum_of_subset_of_nonneg hsub
      (fun _ _ _ => Nat.zero_le _)
  simpa [signatureBox, signature] using
    And.intro (Nat.lt_succ_of_le hcard)
      (And.intro (Nat.lt_succ_of_le hlin) (Nat.lt_succ_of_le hsq))

theorem intervalFiber_card_le_max {b : Nat} {z : Signature}
    (hz : z ∈ signatureBox b) :
    (intervalFiber b z).card ≤ intervalMaxFiber b :=
  by
    simpa [intervalMaxFiber] using
      (Finset.le_sup (f := fun z => (intervalFiber b z).card) hz)

theorem intervalMaxFiber_le_subsets (b : Nat) :
    intervalMaxFiber b ≤ (intervalSubsets b).card := by
  apply Finset.sup_le
  intro z _
  exact Finset.card_le_card (Finset.filter_subset _ _)

theorem intervalMaxFiber_le_two_pow (b : Nat) :
    intervalMaxFiber b ≤ 2 ^ b := by
  simpa [intervalSubsets] using intervalMaxFiber_le_subsets b

/-- Exact finite pigeonhole inequality using the source note's signature box. -/
theorem two_pow_le_box_mul_max (b : Nat) :
    2 ^ b ≤ boxCard b * intervalMaxFiber b := by
  have hsum :=
    Finset.sum_card_fiberwise_eq_card_filter
      (intervalSubsets b) (signatureBox b) signature
  have hall :
      (intervalSubsets b).filter (fun S => signature S ∈ signatureBox b) =
        intervalSubsets b := by
    apply Finset.filter_eq_self.mpr
    intro S hS
    exact signature_mem_box hS
  rw [hall] at hsum
  calc
    2 ^ b = (intervalSubsets b).card := (intervalSubsets_card b).symm
    _ = ∑ z ∈ signatureBox b, (intervalFiber b z).card := by
      simpa [intervalFiber] using hsum.symm
    _ ≤ ∑ _z ∈ signatureBox b, intervalMaxFiber b := by
      exact Finset.sum_le_sum fun z hz =>
        intervalFiber_card_le_max hz
    _ = (signatureBox b).card * intervalMaxFiber b := by simp
    _ = boxCard b * intervalMaxFiber b := by rw [signatureBox_card]

theorem linearCap_succ (b : Nat) :
    linearCap (b + 1) = linearCap b + b := by
  simp [linearCap, Finset.sum_range_succ]

theorem squareCap_succ (b : Nat) :
    squareCap (b + 1) = squareCap b + b * b := by
  simp [squareCap, Finset.sum_range_succ]

theorem twice_linearCap_succ_le_sq {b : Nat} (hb : 2 ≤ b) :
    2 * (linearCap b + 1) ≤ b ^ 2 := by
  induction b, hb using Nat.le_induction with
  | base => norm_num [linearCap]
  | succ b hb ih =>
      rw [linearCap_succ]
      nlinarith

theorem thrice_squareCap_succ_le_cube {b : Nat} (hb : 2 ≤ b) :
    3 * (squareCap b + 1) ≤ b ^ 3 := by
  induction b, hb using Nat.le_induction with
  | base => norm_num [squareCap]
  | succ b hb ih =>
      rw [squareCap_succ]
      nlinarith

/-- The exact signature box has at most `b^6` cells for `b >= 2`. -/
theorem boxCard_le_pow_six {b : Nat} (hb : 2 ≤ b) :
    boxCard b ≤ b ^ 6 := by
  have hlin := twice_linearCap_succ_le_sq hb
  have hsq := thrice_squareCap_succ_le_cube hb
  have hprod :
      6 * ((linearCap b + 1) * (squareCap b + 1)) ≤ b ^ 5 := by
    calc
      6 * ((linearCap b + 1) * (squareCap b + 1)) =
          (2 * (linearCap b + 1)) * (3 * (squareCap b + 1)) := by ring
      _ ≤ (b ^ 2) * (b ^ 3) := Nat.mul_le_mul hlin hsq
      _ = b ^ 5 := by ring
  have hbplus : b + 1 ≤ 6 * b := by omega
  apply Nat.le_of_mul_le_mul_left ?_ (by norm_num : 0 < 6)
  calc
    6 * boxCard b =
        (b + 1) * (6 * ((linearCap b + 1) * (squareCap b + 1))) := by
          simp [boxCard]
          ring
    _ ≤ (6 * b) * (b ^ 5) := Nat.mul_le_mul hbplus hprod
    _ = 6 * (b ^ 6) := by ring

/--
The interval max fibre has binary exponential size up to the source note's
polynomial loss.
-/
theorem two_pow_le_pow_six_mul_intervalMaxFiber {b : Nat} (hb : 2 ≤ b) :
    2 ^ b ≤ b ^ 6 * intervalMaxFiber b := by
  calc
    2 ^ b ≤ boxCard b * intervalMaxFiber b := two_pow_le_box_mul_max b
    _ ≤ b ^ 6 * intervalMaxFiber b :=
      Nat.mul_le_mul_right _ (boxCard_le_pow_six hb)

/-! ## Logarithmic rate -/

noncomputable def intervalFiberRate (b : Nat) : Real :=
  Real.log (intervalMaxFiber b) / b

noncomputable def lowerRate (b : Nat) : Real :=
  Real.log 2 - 6 * (Real.log b / b)

theorem intervalMaxFiber_pos (b : Nat) :
    0 < intervalMaxFiber b := by
  have h := two_pow_le_box_mul_max b
  have hp : 0 < 2 ^ b := pow_pos (by norm_num : 0 < (2 : Nat)) b
  by_contra hnot
  have hz : intervalMaxFiber b = 0 := Nat.eq_zero_of_not_pos hnot
  rw [hz, Nat.mul_zero] at h
  exact (Nat.not_le_of_lt hp h)

theorem log_intervalMaxFiber_le (b : Nat) :
    Real.log (intervalMaxFiber b) ≤ b * Real.log 2 := by
  have hcast :
      ((intervalMaxFiber b : Nat) : Real) ≤ ((2 ^ b : Nat) : Real) := by
    exact_mod_cast intervalMaxFiber_le_two_pow b
  have hlog :=
    Real.log_le_log (by exact_mod_cast intervalMaxFiber_pos b) hcast
  simpa [Nat.cast_pow, Real.log_pow] using hlog

theorem log_intervalMaxFiber_lower_cleared {b : Nat} (hb : 2 ≤ b) :
    (b : Real) * Real.log 2 ≤
      6 * Real.log b + Real.log (intervalMaxFiber b) := by
  have hnat := two_pow_le_pow_six_mul_intervalMaxFiber hb
  have hcast :
      ((2 ^ b : Nat) : Real) ≤
        (((b ^ 6) * intervalMaxFiber b : Nat) : Real) := by
    exact_mod_cast hnat
  have hlog := Real.log_le_log (by positivity) hcast
  have hb0 : (b : Real) ≠ 0 := by positivity
  have hmax0 : ((intervalMaxFiber b : Nat) : Real) ≠ 0 := by
    exact_mod_cast (intervalMaxFiber_pos b).ne'
  simpa [Nat.cast_pow, Nat.cast_mul, Real.log_pow,
    Real.log_mul (pow_ne_zero 6 hb0) hmax0, mul_add, add_comm, add_left_comm,
    add_assoc] using hlog

theorem intervalFiberRate_le_log_two {b : Nat} (hb : 0 < b) :
    intervalFiberRate b ≤ Real.log 2 := by
  rw [intervalFiberRate, div_le_iff₀ (by positivity : (0 : Real) < b)]
  simpa [mul_comm] using log_intervalMaxFiber_le b

theorem lowerRate_le_intervalFiberRate {b : Nat} (hb : 2 ≤ b) :
    lowerRate b ≤ intervalFiberRate b := by
  have hbR : (0 : Real) < b := by positivity
  have hclear := log_intervalMaxFiber_lower_cleared hb
  rw [lowerRate, intervalFiberRate, le_div_iff₀ hbR]
  field_simp
  nlinarith

theorem log_natCast_div_natCast_tendsto_zero :
    Tendsto (fun b : Nat => Real.log b / b) atTop (nhds 0) := by
  have hlo :=
    Real.isLittleO_log_id_atTop.comp_tendsto
      (tendsto_natCast_atTop_atTop (R := Real))
  simpa only [Function.comp_apply, id_eq] using hlo.tendsto_div_nhds_zero

theorem lowerRate_tendsto_log_two :
    Tendsto lowerRate atTop (nhds (Real.log 2)) := by
  have h :=
    (log_natCast_div_natCast_tendsto_zero.const_mul (6 : Real)).const_sub
      (Real.log 2)
  simpa [lowerRate] using h

/--
The interval-block largest-fibre rate tends to `log 2`.  This is the analytic
form of the source note's lower witness; the universal ceiling is the trivial
fact that a fibre contains at most all `2^b` subsets.
-/
theorem intervalFiberRate_tendsto_log_two :
    Tendsto intervalFiberRate atTop (nhds (Real.log 2)) := by
  apply Filter.Tendsto.squeeze' lowerRate_tendsto_log_two tendsto_const_nhds
  · filter_upwards [eventually_ge_atTop 2] with b hb
    exact lowerRate_le_intervalFiberRate hb
  · filter_upwards [eventually_ge_atTop 2] with b hb
    exact intervalFiberRate_le_log_two (by omega)

/--
Any global rate that contains every interval-block rate and has the universal
Boolean-cube ceiling must equal `log 2`.  This is the two-line source
compiler, independent of how the ambient class of integer blocks is packaged.
-/
theorem rateSupremum_eq_log_two_of_interval_minorant
    (globalRate : Real)
    (hupper : globalRate ≤ Real.log 2)
    (hinterval : ∀ b, intervalFiberRate b ≤ globalRate) :
    globalRate = Real.log 2 := by
  apply le_antisymm hupper
  apply le_of_tendsto intervalFiberRate_tendsto_log_two
  exact Filter.Eventually.of_forall hinterval

/-! ## Literal supremum over finite blocks -/

def blockSubsets (V : Finset Nat) : Finset (Finset Nat) :=
  V.powerset

def blockFiber (V : Finset Nat) (z : Signature) : Finset (Finset Nat) :=
  (blockSubsets V).filter fun S => signature S = z

def blockSignatureImage (V : Finset Nat) : Finset Signature :=
  (blockSubsets V).image signature

def blockMaxFiber (V : Finset Nat) : Nat :=
  (blockSignatureImage V).sup fun z => (blockFiber V z).card

noncomputable def blockFiberRate (V : Finset Nat) : Real :=
  Real.log (blockMaxFiber V) / V.card

theorem blockMaxFiber_le_subsets (V : Finset Nat) :
    blockMaxFiber V ≤ (blockSubsets V).card := by
  apply Finset.sup_le
  intro z _
  exact Finset.card_le_card (Finset.filter_subset _ _)

theorem blockMaxFiber_le_two_pow (V : Finset Nat) :
    blockMaxFiber V ≤ 2 ^ V.card := by
  simpa [blockSubsets] using blockMaxFiber_le_subsets V

theorem blockMaxFiber_pos (V : Finset Nat) :
    0 < blockMaxFiber V := by
  have hempty : (∅ : Finset Nat) ∈ blockSubsets V := by
    simp [blockSubsets]
  have hz : signature ∅ ∈ blockSignatureImage V :=
    Finset.mem_image.mpr ⟨∅, hempty, rfl⟩
  have hle :
      (blockFiber V (signature ∅)).card ≤ blockMaxFiber V := by
    simpa [blockMaxFiber] using
      (Finset.le_sup (f := fun z => (blockFiber V z).card) hz)
  have hpos : 0 < (blockFiber V (signature ∅)).card := by
    rw [Finset.card_pos]
    exact ⟨∅, Finset.mem_filter.mpr ⟨hempty, rfl⟩⟩
  omega

/-- On the interval block, the generic block maximum is the exact box maximum. -/
theorem blockMaxFiber_range_eq_intervalMaxFiber (b : Nat) :
    blockMaxFiber (Finset.range b) = intervalMaxFiber b := by
  apply Nat.le_antisymm
  · apply Finset.sup_le
    intro z hz
    obtain ⟨S, hS, rfl⟩ := Finset.mem_image.mp hz
    have hbox : signature S ∈ signatureBox b := by
      apply signature_mem_box
      simpa [blockSubsets, intervalSubsets] using hS
    simpa [blockFiber, blockSubsets, intervalFiber, intervalSubsets] using
      intervalFiber_card_le_max hbox
  · apply Finset.sup_le
    intro z hz
    by_cases hzero : intervalFiber b z = ∅
    · simp [hzero]
    · obtain ⟨S, hS⟩ := Finset.nonempty_iff_ne_empty.mpr hzero
      have hSpow : S ∈ blockSubsets (Finset.range b) := by
        simpa [blockSubsets, intervalSubsets] using (Finset.mem_filter.mp hS).1
      have hsig : signature S = z := (Finset.mem_filter.mp hS).2
      have hzimg : z ∈ blockSignatureImage (Finset.range b) :=
        Finset.mem_image.mpr ⟨S, hSpow, hsig⟩
      have hle :=
        Finset.le_sup (f := fun z =>
          (blockFiber (Finset.range b) z).card) hzimg
      simpa [blockMaxFiber, blockFiber, blockSubsets,
        intervalFiber, intervalSubsets] using hle

theorem blockFiberRate_range (b : Nat) :
    blockFiberRate (Finset.range b) = intervalFiberRate b := by
  simp [blockFiberRate, intervalFiberRate,
    blockMaxFiber_range_eq_intervalMaxFiber]

theorem blockFiberRate_le_log_two {V : Finset Nat} (hV : V.Nonempty) :
    blockFiberRate V ≤ Real.log 2 := by
  have hcast :
      ((blockMaxFiber V : Nat) : Real) ≤ ((2 ^ V.card : Nat) : Real) := by
    exact_mod_cast blockMaxFiber_le_two_pow V
  have hlog :=
    Real.log_le_log (by exact_mod_cast blockMaxFiber_pos V) hcast
  have hlog' :
      Real.log (blockMaxFiber V) ≤ V.card * Real.log 2 := by
    simpa [Nat.cast_pow, Real.log_pow] using hlog
  rw [blockFiberRate, div_le_iff₀ (by
    exact_mod_cast (Finset.card_pos.mpr hV))]
  simpa [mul_comm] using hlog'

def blockFiberRates : Set Real :=
  {r | ∃ V : Finset Nat, V.Nonempty ∧ r = blockFiberRate V}

noncomputable def phiStar : Real :=
  sSup blockFiberRates

theorem blockFiberRates_nonempty : blockFiberRates.Nonempty := by
  refine ⟨blockFiberRate {0}, ?_⟩
  exact ⟨{0}, by simp, rfl⟩

theorem blockFiberRates_bddAbove : BddAbove blockFiberRates := by
  refine ⟨Real.log 2, ?_⟩
  rintro r ⟨V, hV, rfl⟩
  exact blockFiberRate_le_log_two hV

/--
The degree-two moment-map max-fibre exponential rate is exactly `log 2`.
The interval blocks supply the lower limit; no block can exceed the full
Boolean-cube size.
-/
theorem phiStar_eq_log_two :
    phiStar = Real.log 2 := by
  apply le_antisymm
  · apply csSup_le blockFiberRates_nonempty
    intro r hr
    obtain ⟨V, hV, rfl⟩ := hr
    exact blockFiberRate_le_log_two hV
  · apply le_of_tendsto intervalFiberRate_tendsto_log_two
    filter_upwards [eventually_ge_atTop 1] with b hb
    apply le_csSup blockFiberRates_bddAbove
    refine ⟨Finset.range b, ⟨0, Finset.mem_range.mpr hb⟩, ?_⟩
    exact (blockFiberRate_range b).symm

#print axioms two_pow_le_box_mul_max
#print axioms boxCard_le_pow_six
#print axioms two_pow_le_pow_six_mul_intervalMaxFiber
#print axioms intervalFiberRate_tendsto_log_two
#print axioms phiStar_eq_log_two
#print axioms rateSupremum_eq_log_two_of_interval_minorant

end MomentToMax.MomentMapMaxFiber
