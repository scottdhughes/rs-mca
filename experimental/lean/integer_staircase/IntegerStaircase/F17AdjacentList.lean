import Std

/-!
# Exact F₁₇ adjacent list-staircase certificate

This module formalizes the finite certificate in
`experimental/notes/frontier-adjacent/toy_complete_adjacent_list_staircase_v1.md`.

For the Reed--Solomon toy row on `F₁₇ˣ` with `n = 16`, `k = 8`, it
kernel-checks all `choose 16 10 = 8008` ten-subsets.  They are bucketed by the
two leading non-monic coefficients of their vanishing polynomials.  The exact
largest fibre has size `32`, attained at the null prefix.  The module also
reconstructs all 32 degree-`< 8` codewords for the received word `X^10`,
checks exact agreement 10, and checks pairwise distinctness.

The safe side records the exact Johnson specialization
`L * (11^2 - 16*7) <= 16*(11-7)`: its denominator is 9, numerator is 64,
and hence its integral cap is 7.  The final theorem keeps the two semantic
bridges explicit: the prefix fibre is a lower bound for the true list numerator,
and the Johnson theorem bounds that numerator at agreement 11.  Those are the
standard prefix-witness and all-words Johnson results; this stdlib-only package
checks their complete F₁₇ instance and the adjacent endpoint arithmetic.

No `sorry`.  No Mathlib.
-/

namespace IntegerStaircase.F17AdjacentList

/-! ## Finite field arithmetic and subset enumeration -/

def p : Nat := 17

def add17 (x y : Nat) : Nat := (x + y) % p

def neg17 (x : Nat) : Nat := (p - x % p) % p

def sub17 (x y : Nat) : Nat := add17 x (neg17 y)

def mul17 (x y : Nat) : Nat := (x * y) % p

def domain : List Nat := (List.range 16).map (fun x => x + 1)

def combinations {α : Type} : Nat → List α → List (List α)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | k + 1, x :: xs =>
      (combinations k xs).map (fun ys => x :: ys) ++ combinations (k + 1) xs
termination_by _ xs => xs.length

def tenSubsets : List (List Nat) := combinations 10 domain

def secondElementary : List Nat → Nat
  | [] => 0
  | x :: xs => x * xs.sum + secondElementary xs

/-- The coefficients of `X^9` and `X^8` in `∏_{x∈S}(X-x)`, modulo 17. -/
def prefix₂ (S : List Nat) : Nat × Nat :=
  (neg17 S.sum, secondElementary S % p)

def allPrefix₂Keys : List (Nat × Nat) :=
  (List.range p).flatMap fun x => (List.range p).map fun y => (x, y)

def prefix₂Fibre (z : Nat × Nat) : List (List Nat) :=
  tenSubsets.filter fun S => prefix₂ S == z

def prefix₂FibreSize (z : Nat × Nat) : Nat := (prefix₂Fibre z).length

def maxPrefix₂FibreSize : Nat :=
  (allPrefix₂Keys.map prefix₂FibreSize).foldl Nat.max 0

def nonemptyPrefix₂KeyCount : Nat :=
  (allPrefix₂Keys.filter fun z => prefix₂FibreSize z > 0).length

def nullPrefix₂ : Nat × Nat := (0, 0)

def nullPrefix₂Fibre : List (List Nat) := prefix₂Fibre nullPrefix₂

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem tenSubsets_count : tenSubsets.length = 8008 := by native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem all_prefixes_are_realized : nonemptyPrefix₂KeyCount = 289 := by native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem exact_max_prefix₂_fibre : maxPrefix₂FibreSize = 32 := by native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem null_prefix₂_is_maximal :
    prefix₂FibreSize nullPrefix₂ = maxPrefix₂FibreSize := by native_decide

/-! ## Average floor and companion depth-three fibre -/

def averagePrefix₂Ceiling : Nat :=
  (tenSubsets.length + p * p - 1) / (p * p)

def nullPrefix₂Excess : Nat :=
  prefix₂FibreSize nullPrefix₂ - averagePrefix₂Ceiling

def thirdElementary : List Nat → Nat
  | [] => 0
  | x :: xs => x * secondElementary xs + thirdElementary xs

/-- The three leading non-monic coefficients for an eleven-subset. -/
def prefix₃ (S : List Nat) : Nat × Nat × Nat :=
  (neg17 S.sum, secondElementary S % p, neg17 (thirdElementary S))

def elevenSubsets : List (List Nat) := combinations 11 domain

def allPrefix₃Keys : List (Nat × Nat × Nat) :=
  (List.range p).flatMap fun x =>
    (List.range p).flatMap fun y => (List.range p).map fun z => (x, y, z)

def prefix₃FibreSize (z : Nat × Nat × Nat) : Nat :=
  (elevenSubsets.filter fun S => prefix₃ S == z).length

def prefix₃Index (z : Nat × Nat × Nat) : Nat :=
  z.1 * p * p + z.2.1 * p + z.2.2

def prefix₃Counts : Array Nat :=
  elevenSubsets.foldl (fun counts S =>
    let i := prefix₃Index (prefix₃ S)
    counts.set! i (counts.get! i + 1)) (mkArray (p * p * p) 0)

def maxPrefix₃FibreSize : Nat :=
  prefix₃Counts.foldl Nat.max 0

theorem average_prefix₂_ceiling_value : averagePrefix₂Ceiling = 28 := by
  native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem null_prefix₂_excess_value : nullPrefix₂Excess = 4 := by native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem elevenSubsets_count : elevenSubsets.length = 4368 := by native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem exact_max_prefix₃_fibre : maxPrefix₃FibreSize = 3 := by native_decide

/-! ## Vanishing polynomials and witness reconstruction -/

/-- Multiply a low-to-high coefficient list by `X - x` over F₁₇. -/
def mulXSub (x : Nat) (coeffs : List Nat) : List Nat :=
  let scaled := coeffs.map (fun c => mul17 c (neg17 x)) ++ [0]
  let shifted := 0 :: coeffs
  List.zipWith add17 scaled shifted

def vanishingPolynomial (S : List Nat) : List Nat :=
  S.foldl (fun coeffs x => mulXSub x coeffs) [1]

def coeffAt (coeffs : List Nat) (i : Nat) : Nat := coeffs.getD i 0

def polynomialPrefix₂ (S : List Nat) : Nat × Nat :=
  let coeffs := vanishingPolynomial S
  (coeffAt coeffs (S.length - 1), coeffAt coeffs (S.length - 2))

def polynomialPrefix₃ (S : List Nat) : Nat × Nat × Nat :=
  let coeffs := vanishingPolynomial S
  (coeffAt coeffs (S.length - 1), coeffAt coeffs (S.length - 2),
    coeffAt coeffs (S.length - 3))

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem prefix₃_matches_vanishing_coefficients :
    elevenSubsets.all (fun S => prefix₃ S == polynomialPrefix₃ S) = true := by
  native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem prefix₂_matches_vanishing_coefficients :
    tenSubsets.all (fun S => prefix₂ S == polynomialPrefix₂ S) = true := by
  native_decide

def receivedPolynomial : List Nat := List.replicate 10 0 ++ [1]

def reconstructedCodeword (S : List Nat) : List Nat :=
  List.zipWith sub17 receivedPolynomial (vanishingPolynomial S)

def evalPolynomial (coeffs : List Nat) (x : Nat) : Nat :=
  coeffs.reverse.foldl (fun acc c => add17 (mul17 acc x) c) 0

def agreementCount (coeffs : List Nat) : Nat :=
  (domain.filter fun x =>
    evalPolynomial coeffs x == evalPolynomial receivedPolynomial x).length

def hasDegreeLtEight (coeffs : List Nat) : Bool :=
  (coeffs.drop 8).all (fun c => c == 0)

def reconstructedCodewords : List (List Nat) :=
  nullPrefix₂Fibre.map reconstructedCodeword

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem reconstructed_codewords_count : reconstructedCodewords.length = 32 := by
  native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem reconstructed_codewords_have_degree_lt_eight :
    reconstructedCodewords.all hasDegreeLtEight = true := by
  native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem reconstructed_codewords_have_exact_agreement_ten :
    reconstructedCodewords.all (fun c => agreementCount c == 10) = true := by
  native_decide

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem reconstructed_codewords_pairwise_distinct :
    reconstructedCodewords.Nodup := by
  native_decide

/-! ## Budget, Johnson cell, and adjacent compilation -/

def natPow : Nat → Nat → Nat
  | _, 0 => 1
  | b, e + 1 => b * natPow b e

def blockLength : Nat := 16

def dimension : Nat := 8

def unsafeAgreement : Nat := 10

def safeAgreement : Nat := 11

def listDenominator : Nat := natPow p dimension

def targetPower : Nat := 29

def budget : Nat := listDenominator / natPow 2 targetPower

def johnsonIntersection : Nat := dimension - 1

def johnsonDenominator : Nat :=
  safeAgreement * safeAgreement - blockLength * johnsonIntersection

def johnsonNumerator : Nat :=
  blockLength * (safeAgreement - johnsonIntersection)

def johnsonCap : Nat := johnsonNumerator / johnsonDenominator

def johnsonDenominatorAt (a : Nat) : Nat :=
  a * a - blockLength * johnsonIntersection

def johnsonNumeratorAt (a : Nat) : Nat :=
  blockLength * (a - johnsonIntersection)

def johnsonCapAt (a : Nat) : Nat :=
  johnsonNumeratorAt a / johnsonDenominatorAt a

def johnsonRadiusSatisfied (a : Nat) : Bool :=
  blockLength * johnsonIntersection < a * a

def uniqueDecodingActive (a : Nat) : Bool :=
  blockLength + johnsonIntersection < 2 * a

def bestPackingCapAt (a : Nat) : Nat :=
  match uniqueDecodingActive a with
  | true => 1
  | false => johnsonCapAt a

theorem packing_cell_values :
    johnsonRadiusSatisfied unsafeAgreement = false
      ∧ johnsonRadiusSatisfied safeAgreement = true
      ∧ johnsonCapAt safeAgreement = 7
      ∧ uniqueDecodingActive safeAgreement = false
      ∧ johnsonCapAt 12 = 2
      ∧ uniqueDecodingActive 12 = true
      ∧ bestPackingCapAt 12 = 1 := by
  native_decide

/-- The companion adjacent pair has `L(11)=3` and safe cap `U(12)=1`. -/
theorem companion_adjacent_window :
    maxPrefix₃FibreSize = 3
      ∧ bestPackingCapAt 12 = 1
      ∧ (bestPackingCapAt 12 ≤ 1 ∧ 1 < maxPrefix₃FibreSize)
      ∧ (bestPackingCapAt 12 ≤ 2 ∧ 2 < maxPrefix₃FibreSize) := by
  native_decide

theorem listDenominator_value : listDenominator = 6975757441 := by native_decide

theorem budget_value : budget = 12 := by native_decide

theorem agreements_are_adjacent : safeAgreement = unsafeAgreement + 1 := by
  native_decide

theorem johnson_denominator_value : johnsonDenominator = 9 := by native_decide

theorem johnson_numerator_value : johnsonNumerator = 64 := by native_decide

theorem johnson_cap_value : johnsonCap = 7 := by native_decide

/-- The concrete Johnson inequality forces the integral cap `L <= 7`. -/
theorem le_seven_of_johnson_cell {L : Nat}
    (h : L * johnsonDenominator ≤ johnsonNumerator) : L ≤ johnsonCap := by
  have hden : johnsonDenominator = 9 := johnson_denominator_value
  have hnum : johnsonNumerator = 64 := johnson_numerator_value
  have hcap : johnsonCap = 7 := johnson_cap_value
  rw [hden, hnum] at h
  rw [hcap]
  omega

theorem numeric_adjacent_crossing :
    budget < maxPrefix₂FibreSize ∧ johnsonCap ≤ budget := by
  native_decide

/-- Complete numerical packet: `32 > 12 >= 7`. -/
theorem exact_F17_bound_window :
    maxPrefix₂FibreSize = 32 ∧ budget = 12 ∧ johnsonCap = 7
      ∧ budget < maxPrefix₂FibreSize ∧ johnsonCap ≤ budget := by
  native_decide

/--
Compile the finite packet into the actual list-numerator crossing.

The two hypotheses are precisely the semantic links supplied by the
prefix-witness construction and the all-received-words Johnson theorem.
-/
theorem F17_adjacent_list_crossing
    (listNumerator : Nat → Nat)
    (hprefixWitness : maxPrefix₂FibreSize ≤ listNumerator unsafeAgreement)
    (hJohnsonCell :
      listNumerator safeAgreement * johnsonDenominator ≤ johnsonNumerator) :
    budget < listNumerator unsafeAgreement
      ∧ listNumerator safeAgreement ≤ budget := by
  have hjohnson := le_seven_of_johnson_cell hJohnsonCell
  exact ⟨Nat.lt_of_lt_of_le numeric_adjacent_crossing.1 hprefixWitness,
    Nat.le_trans hjohnson numeric_adjacent_crossing.2⟩

def Safe (listNumerator : Nat → Nat) (a : Nat) : Prop :=
  listNumerator a ≤ budget

/--
If the true list numerator is antitone, the adjacent crossing makes agreement
11 the first safe integer: every agreement at most 10 is unsafe.
-/
theorem F17_first_safe_agreement
    (listNumerator : Nat → Nat)
    (hantitone : ∀ a b, a ≤ b → listNumerator b ≤ listNumerator a)
    (hprefixWitness : maxPrefix₂FibreSize ≤ listNumerator unsafeAgreement)
    (hJohnsonCell :
      listNumerator safeAgreement * johnsonDenominator ≤ johnsonNumerator) :
    Safe listNumerator safeAgreement
      ∧ ∀ b, b ≤ unsafeAgreement → ¬ Safe listNumerator b := by
  have hcross :=
    F17_adjacent_list_crossing listNumerator hprefixWitness hJohnsonCell
  constructor
  · exact hcross.2
  · intro b hb hsafe
    have hmono : listNumerator unsafeAgreement ≤ listNumerator b :=
      hantitone b unsafeAgreement hb
    have hbad : budget < listNumerator b :=
      Nat.lt_of_lt_of_le hcross.1 hmono
    exact (Nat.not_le_of_lt hbad) hsafe

def largestSafeClosedRadius : Nat := blockLength - safeAgreement

def firstUnsafeClosedRadius : Nat := blockLength - unsafeAgreement

def endpointNumerator : Nat := firstUnsafeClosedRadius

def endpointDenominator : Nat := blockLength

theorem closed_ball_endpoint :
    largestSafeClosedRadius = 5
      ∧ firstUnsafeClosedRadius = 6
      ∧ endpointNumerator * 8 = 3 * endpointDenominator := by
  native_decide

/--
The complete source-facing F₁₇ packet: the true list numerator crosses the
integer budget on the adjacent agreements 10/11, agreement 11 is first safe
under antitonicity, and the closed-ball endpoint is 5/16 with unattained upper
edge 6/16 = 3/8.
-/
theorem F17_complete_adjacent_list_certificate_of_bridges
    (listNumerator : Nat → Nat)
    (hantitone : ∀ a b, a ≤ b → listNumerator b ≤ listNumerator a)
    (hprefixWitness : maxPrefix₂FibreSize ≤ listNumerator unsafeAgreement)
    (hJohnsonCell :
      listNumerator safeAgreement * johnsonDenominator ≤ johnsonNumerator) :
    (budget < listNumerator unsafeAgreement
      ∧ listNumerator safeAgreement ≤ budget)
      ∧ (Safe listNumerator safeAgreement
        ∧ ∀ b, b ≤ unsafeAgreement → ¬ Safe listNumerator b)
      ∧ (largestSafeClosedRadius = 5
        ∧ firstUnsafeClosedRadius = 6
        ∧ endpointNumerator * 8 = 3 * endpointDenominator) := by
  exact ⟨F17_adjacent_list_crossing listNumerator hprefixWitness hJohnsonCell,
    F17_first_safe_agreement listNumerator hantitone hprefixWitness hJohnsonCell,
    closed_ball_endpoint⟩

#print axioms exact_max_prefix₂_fibre
#print axioms exact_max_prefix₃_fibre
#print axioms companion_adjacent_window
#print axioms prefix₂_matches_vanishing_coefficients
#print axioms reconstructed_codewords_pairwise_distinct
#print axioms le_seven_of_johnson_cell
#print axioms exact_F17_bound_window
#print axioms F17_adjacent_list_crossing
#print axioms F17_first_safe_agreement
#print axioms closed_ball_endpoint
#print axioms F17_complete_adjacent_list_certificate_of_bridges

end IntegerStaircase.F17AdjacentList
