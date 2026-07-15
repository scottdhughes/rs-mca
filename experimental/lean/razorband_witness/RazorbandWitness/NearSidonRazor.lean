import Mathlib

namespace RazorbandWitness.NearSidonRazor

open Finset BigOperators

/-!
# Exact two-moment Prouhet product and repaired finite razor

This module formalizes the exact finite core of
`experimental/notes/audits/c9_r2_near_sidon_razor.md`.

It verifies the unique local degree-two Prouhet collision, constructs the
block-choice moment fiber, computes its size and factorized additive energy,
and proves the two finite inequalities behind the repaired razor. It does not
claim that the separated-block domain is a smooth multiplicative/circle domain
or that the product fiber survives a primitive first-match deletion.
-/

/-! ## The six-point local Prouhet collision -/

abbrev LocalCoord := Fin 6

/-- The ordered local value set `{0,1,2,4,5,6}`. -/
def localValue : LocalCoord → ℕ := ![0, 1, 2, 4, 5, 6]

/-- The two colliding three-subsets, represented by their local indices. -/
def localA : Finset LocalCoord := {0, 3, 4}
def localB : Finset LocalCoord := {1, 2, 5}

/-- Cardinality, first moment, and second moment of a local subset. -/
def localSignature (S : Finset LocalCoord) : ℕ × ℕ × ℕ :=
  (S.card, ∑ i ∈ S, localValue i, ∑ i ∈ S, (localValue i) ^ 2)

theorem localA_signature : localSignature localA = (3, 9, 41) := by
  native_decide

theorem localB_signature : localSignature localB = (3, 9, 41) := by
  native_decide

/-- Exhaustion of all 64 local subsets: the displayed unordered pair is the
only nontrivial collision of cardinality and the first two moments. -/
theorem localSignature_eq_classification :
    ∀ S T : Finset LocalCoord, localSignature S = localSignature T →
      S = T ∨ (S = localA ∧ T = localB) ∨ (S = localB ∧ T = localA) := by
  native_decide

/-- Number of distinct local signatures among subsets of a fixed weight. -/
def localSignatureCount (w : ℕ) : ℕ :=
  (((Finset.univ : Finset (Finset LocalCoord)).filter
      (fun S => S.card = w)).image localSignature).card

/-- The exact coefficient vector of `P(x) = (1+x)^6 - x^3`. -/
theorem localSignatureCount_table :
    (List.range 7).map localSignatureCount = [1, 6, 15, 19, 15, 6, 1] := by
  native_decide

/-! ## Separated block-choice fiber -/

/-- One Boolean choice between the two local trades in every block. -/
abbrev ProuhetChoice (k : ℕ) := Fin k → Bool

/-- Local subset selected by a Boolean block choice. -/
def chosenLocal (b : Bool) : Finset LocalCoord :=
  if b then localA else localB

/-- First moment after translating the local values by `C=20`. -/
def shiftedFirst (b : Bool) : ℕ :=
  (chosenLocal b).sum (fun i => 20 + localValue i)

/-- Second moment after translating the local values by `C=20`. -/
def shiftedSecond (b : Bool) : ℕ :=
  (chosenLocal b).sum (fun i => (20 + localValue i) ^ 2)

theorem shiftedFirst_eq (b : Bool) : shiftedFirst b = 69 := by
  cases b <;> decide

theorem shiftedSecond_eq (b : Bool) : shiftedSecond b = 1601 := by
  cases b <;> decide

/-- Integer first moment of the separated `Q=1000` block product. -/
def firstMoment {k : ℕ} (choice : ProuhetChoice k) : ℕ :=
  ∑ i : Fin k, shiftedFirst (choice i) * 1000 ^ (i : ℕ)

/-- Integer second moment of the separated `Q=1000` block product. -/
def secondMoment {k : ℕ} (choice : ProuhetChoice k) : ℕ :=
  ∑ i : Fin k, shiftedSecond (choice i) * 1000 ^ (2 * (i : ℕ))

theorem firstMoment_eq_constant {k : ℕ} (choice : ProuhetChoice k) :
    firstMoment choice = ∑ i : Fin k, 69 * 1000 ^ (i : ℕ) := by
  apply Finset.sum_congr rfl
  intro i hi
  rw [shiftedFirst_eq]

theorem secondMoment_eq_constant {k : ℕ} (choice : ProuhetChoice k) :
    secondMoment choice = ∑ i : Fin k, 1601 * 1000 ^ (2 * (i : ℕ)) := by
  apply Finset.sum_congr rfl
  intro i hi
  rw [shiftedSecond_eq]

/-- Every pair of block choices has the same two global moments. -/
theorem twoMomentFiber {k : ℕ} (choice other : ProuhetChoice k) :
    firstMoment choice = firstMoment other ∧
      secondMoment choice = secondMoment other := by
  constructor
  · rw [firstMoment_eq_constant, firstMoment_eq_constant]
  · rw [secondMoment_eq_constant, secondMoment_eq_constant]

/-- The displayed block-product fiber has exactly `2^k` choices. -/
theorem prouhetChoice_card (k : ℕ) :
    Fintype.card (ProuhetChoice k) = 2 ^ k := by
  simp [ProuhetChoice]

/-! ## Exact factorized additive energy -/

/-- A local ordered additive-energy quadruple. -/
structure LocalQuad where
  a : Bool
  b : Bool
  c : Bool
  d : Bool
  deriving DecidableEq, Fintype

/-- Boolean incidence coordinate as a natural number. -/
def bitNat (b : Bool) : ℕ := if b then 1 else 0

/-- The six local solutions of `a+d=b+c`. -/
def LocalEnergyWitness :=
  {q : LocalQuad // bitNat q.a + bitNat q.d = bitNat q.b + bitNat q.c}

deriving instance Fintype for LocalEnergyWitness

theorem localEnergyWitness_card : Fintype.card LocalEnergyWitness = 6 := by
  decide

/-- Difference equality factorizes independently across the `k` blocks. -/
abbrev ProductEnergyWitness (k : ℕ) := Fin k → LocalEnergyWitness

/-- Exact ordered additive-energy count of the product fiber. -/
def productEnergyCount (k : ℕ) : ℕ :=
  Fintype.card (ProductEnergyWitness k)

theorem productEnergyCount_eq (k : ℕ) : productEnergyCount k = 6 ^ k := by
  simp [productEnergyCount, ProductEnergyWitness, localEnergyWitness_card]

/-- Exact cardinality of the product fiber. -/
def productFiberCard (k : ℕ) : ℕ := Fintype.card (ProuhetChoice k)

theorem productFiberCard_eq (k : ℕ) : productFiberCard k = 2 ^ k :=
  prouhetChoice_card k

/-- Normalized energy `Δ=E/f^3` of the product fiber. -/
def productNormalizedEnergy (k : ℕ) : ℚ :=
  (productEnergyCount k : ℚ) / (productFiberCard k : ℚ) ^ 3

theorem productNormalizedEnergy_eq (k : ℕ) :
    productNormalizedEnergy k = (3 / 4 : ℚ) ^ k := by
  rw [productNormalizedEnergy, productEnergyCount_eq, productFiberCard_eq]
  push_cast
  have hpow : (((2 : ℚ) ^ k) ^ 3) = (8 : ℚ) ^ k := by
    calc
      ((2 : ℚ) ^ k) ^ 3 = (2 : ℚ) ^ (k * 3) := by rw [pow_mul]
      _ = (2 : ℚ) ^ (3 * k) := by rw [Nat.mul_comm]
      _ = ((2 : ℚ) ^ 3) ^ k := by rw [pow_mul]
      _ = (8 : ℚ) ^ k := by norm_num
  rw [hpow, ← div_pow]
  norm_num

/-- The exact three-block central image coefficient from inclusion-exclusion. -/
theorem centralImageCoefficient_threeBlocks :
    Nat.choose 18 9 - 3 * Nat.choose 12 6 + 3 * Nat.choose 6 3 - 1 = 45907 := by
  decide

/-- Finite exponential excess base from the `k=3r` normalization lower bound. -/
def normalizedExcessBase : ℚ := 45907 / 32768

theorem normalizedExcessBase_gt_one : (1 : ℚ) < normalizedExcessBase := by
  norm_num [normalizedExcessBase]

/-- The exact product energy tends to zero in the printed absolute sense. -/
theorem productNormalizedEnergy_tendsto_zero :
    Filter.Tendsto productNormalizedEnergy Filter.atTop (nhds 0) := by
  have h : Filter.Tendsto (fun n : ℕ => (3 / 4 : ℚ) ^ n)
      Filter.atTop (nhds 0) :=
    tendsto_pow_atTop_nhds_zero_of_norm_lt_one (by
      rw [← Rat.norm_cast_real]
      norm_num [Real.norm_eq_abs])
  exact h.congr' (Filter.Eventually.of_forall fun n =>
    (productNormalizedEnergy_eq n).symm)

/-- A fixed `c=1/2<1` power lower gate does not imply TeX-high energy. In
squared form, the product satisfies `Δ² ≥ 1/f` for every block count. -/
theorem productEnergy_passes_fixedHalfPowerGate (k : ℕ) :
    (1 / 2 : ℚ) ^ k ≤ (productNormalizedEnergy k) ^ 2 := by
  rw [productNormalizedEnergy_eq]
  calc
    (1 / 2 : ℚ) ^ k ≤ (9 / 16 : ℚ) ^ k :=
      pow_le_pow_left₀ (by norm_num) (by norm_num) k
    _ = (((3 / 4 : ℚ) ^ 2) ^ k) := by norm_num
    _ = ((3 / 4 : ℚ) ^ k) ^ 2 := by
      simp only [← pow_mul]
      rw [Nat.mul_comm]

/-- Exact rational identity behind the three-block normalized excess. -/
theorem normalizedExcess_identity (r : ℕ) :
    normalizedExcessBase ^ r * (64 : ℚ) ^ (3 * r) =
      (2 : ℚ) ^ (3 * r) * (45907 : ℚ) ^ r := by
  norm_num [normalizedExcessBase, pow_mul, ← mul_pow]

/-- If the three-block image lower bound and ambient-mass upper bound hold,
the image-normalized fiber ratio is at least
`(45907/32768)^r > 1`. This is the exact finite compiler used by the
counterexample subsequence. -/
theorem normalizedExcess_lower_of_threeBlock_bounds
    (r : ℕ) (imageMass fullMass : ℚ) (hfullPos : 0 < fullMass)
    (himage : (45907 : ℚ) ^ r ≤ imageMass)
    (hfull : fullMass ≤ (64 : ℚ) ^ (3 * r)) :
    normalizedExcessBase ^ r ≤
      (2 : ℚ) ^ (3 * r) * imageMass / fullMass := by
  apply (le_div_iff₀ hfullPos).2
  have hbaseNonneg : (0 : ℚ) ≤ normalizedExcessBase ^ r :=
    pow_nonneg (le_trans (by norm_num) normalizedExcessBase_gt_one.le) r
  calc
    normalizedExcessBase ^ r * fullMass
        ≤ normalizedExcessBase ^ r * (64 : ℚ) ^ (3 * r) :=
          mul_le_mul_of_nonneg_left hfull hbaseNonneg
    _ = (2 : ℚ) ^ (3 * r) * (45907 : ℚ) ^ r :=
      normalizedExcess_identity r
    _ ≤ (2 : ℚ) ^ (3 * r) * imageMass :=
      mul_le_mul_of_nonneg_left himage (by positivity)

/-! ## Repaired finite razor implications -/

/-- Full-slice normalized fiber ratio `f / (M/L) = fL/M`. -/
def normalizedFiberRatio (fiberMass fullMass imageSize : ℕ) : ℚ :=
  (fiberMass : ℚ) * imageSize / fullMass

/-- Small realized image pays every residual fiber without an energy input. -/
theorem normalizedFiberRatio_le_imageSize
    {fiberMass fullMass imageSize : ℕ}
    (hfiber : fiberMass ≤ fullMass) (hfull : 0 < fullMass) :
    normalizedFiberRatio fiberMass fullMass imageSize ≤ imageSize := by
  unfold normalizedFiberRatio
  apply (div_le_iff₀ (by exact_mod_cast hfull)).2
  exact_mod_cast (show fiberMass * imageSize ≤ imageSize * fullMass by
    simpa [Nat.mul_comm] using Nat.mul_le_mul_right imageSize hfiber)

/-- Normalized additive energy for an arbitrary finite Boolean fiber. -/
def normalizedEnergyOf (energy fiberMass : ℕ) : ℚ :=
  (energy : ℚ) / (fiberMass : ℚ) ^ 3

/-- The Boolean-cube energy consequence used by the repaired razor:
`E^3 ≤ f^8` forces `Δ^3 ≤ 1/f`. Thus positive-rate large fibers are in the
exponentially low-energy branch rather than the proposed fixed-power
high-energy branch. -/
theorem normalizedEnergy_cube_le_inv_card
    {energy fiberMass : ℕ} (hfiber : 0 < fiberMass)
    (henergy : energy ^ 3 ≤ fiberMass ^ 8) :
    (normalizedEnergyOf energy fiberMass) ^ 3 ≤ (1 : ℚ) / fiberMass := by
  unfold normalizedEnergyOf
  rw [div_pow]
  have hfq : (0 : ℚ) < fiberMass := by exact_mod_cast hfiber
  apply (div_le_div_iff₀ (pow_pos (pow_pos hfq 3) 3) hfq).2
  have henergyQ : (energy : ℚ) ^ 3 ≤ (fiberMass : ℚ) ^ 8 := by
    exact_mod_cast henergy
  calc
    (energy : ℚ) ^ 3 * fiberMass
        ≤ (fiberMass : ℚ) ^ 8 * fiberMass :=
          mul_le_mul_of_nonneg_right henergyQ (le_of_lt hfq)
    _ = 1 * ((fiberMass : ℚ) ^ 3) ^ 3 := by ring

#print axioms localSignature_eq_classification
#print axioms localSignatureCount_table
#print axioms twoMomentFiber
#print axioms prouhetChoice_card
#print axioms productEnergyCount_eq
#print axioms productNormalizedEnergy_eq
#print axioms centralImageCoefficient_threeBlocks
#print axioms normalizedExcessBase_gt_one
#print axioms productNormalizedEnergy_tendsto_zero
#print axioms productEnergy_passes_fixedHalfPowerGate
#print axioms normalizedExcess_identity
#print axioms normalizedExcess_lower_of_threeBlock_bounds
#print axioms normalizedFiberRatio_le_imageSize
#print axioms normalizedEnergy_cube_le_inv_card

end RazorbandWitness.NearSidonRazor
