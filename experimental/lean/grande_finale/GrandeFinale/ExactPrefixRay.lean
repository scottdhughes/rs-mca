import GrandeFinale.ExactListLine

/-!
# Exact locator-prefix ray realization

This module specializes the same-field list--line bijection to the complete
locator-prefix fibers of `cor:exact-prefix-ray-realization` in
`experimental/asymptotic_rs_mca_frontiers.tex`. It identifies the direct
support-to-slope image with the full MCA-bad slope set and proves that each
support remains the exact agreement support on its corresponding line point.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.ExactPrefixRay

variable {F : Type*} [Field F]

/-- Inclusion of a finite evaluation domain into its field. -/
abbrev domainEval (D : Finset F) : ↥D → F := fun x ↦ x.1

/-- Restriction of a polynomial received word to the evaluation domain. -/
abbrev polynomialWord (D : Finset F) (U : F[X]) : ↥D → F :=
  fun x ↦ U.eval x.1

omit [Field F] in
theorem domainEval_ne_of_not_mem
    (D : Finset F) {alpha : F} (halpha : alpha ∉ D) :
    ∀ x : ↥D, domainEval D x ≠ alpha := by
  intro x hx
  apply halpha
  simpa [domainEval, hx] using x.property

/-- The subtype agreement support maps exactly to the polynomial agreement
support on `D`. -/
theorem image_polynomialAgreementSet_eq
    (D : Finset F) (U P : F[X]) :
    (ExactListLine.polynomialAgreementSet
      (domainEval D) (polynomialWord D U) P).image
        (fun x : ↥D ↦ x.1) =
      ExactPrefixList.agreementSet D U P := by
  ext x
  simp [ExactListLine.polynomialAgreementSet,
    ExactPrefixList.agreementSet, domainEval, polynomialWord, and_comm]

theorem polynomialAgreementSet_card_eq
    (D : Finset F) (U P : F[X]) :
    (ExactListLine.polynomialAgreementSet
      (domainEval D) (polynomialWord D U) P).card =
      (ExactPrefixList.agreementSet D U P).card := by
  let A := ExactListLine.polynomialAgreementSet
    (domainEval D) (polynomialWord D U) P
  calc
    A.card = (A.image (fun x : ↥D ↦ x.1)).card :=
      (Finset.card_image_of_injective A Subtype.val_injective).symm
    _ = (ExactPrefixList.agreementSet D U P).card := by
      rw [image_polynomialAgreementSet_eq D U P]

theorem listedPolynomial_natDegree_le_pred
    (D : Finset F) (U : F[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m)
    {P : F[X]} (hP : P ∈ PrefixPigeonhole.listedPolynomials D U K m) :
    P.natDegree ≤ K - 1 := by
  have hdegree : P.degree < (K : WithBot Nat) :=
    ((PrefixPigeonhole.mem_listedPolynomials_iff
      D U hU hKpos hKm P).mp hP).1
  by_cases hPzero : P = 0
  · simp [hPzero]
  · have hnat : P.natDegree < K :=
      (natDegree_lt_iff_degree_lt hPzero).mpr hdegree
    omega

theorem listedPolynomial_agreements
    (D : Finset F) (U : F[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m)
    {P : F[X]} (hP : P ∈ PrefixPigeonhole.listedPolynomials D U K m) :
    m ≤ (ExactListLine.polynomialAgreementSet
      (domainEval D) (polynomialWord D U) P).card := by
  rw [polynomialAgreementSet_card_eq D U P]
  exact ((PrefixPigeonhole.mem_listedPolynomials_iff
    D U hU hKpos hKm P).mp hP).2

theorem mem_listedPolynomials_of_degree_agreements
    (D : Finset F) (U : F[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m)
    (P : F[X]) (hdegree : P.natDegree ≤ K - 1)
    (hagree : m ≤ (ExactListLine.polynomialAgreementSet
      (domainEval D) (polynomialWord D U) P).card) :
    P ∈ PrefixPigeonhole.listedPolynomials D U K m := by
  apply (PrefixPigeonhole.mem_listedPolynomials_iff
    D U hU hKpos hKm P).mpr
  constructor
  · by_cases hPzero : P = 0
    · simp [hPzero]
    · apply (natDegree_lt_iff_degree_lt hPzero).mp
      omega
  · rw [← polynomialAgreementSet_card_eq D U P]
    exact hagree

/-- A support in the coefficient fiber is the full agreement support of its
listed polynomial, not merely a subset of it. -/
theorem prefixPolynomial_agreementSet_eq_support
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F) {S : Finset F}
    (hS : S ∈ PrefixPigeonhole.coefficientFiber D K m z) :
    ExactPrefixList.agreementSet D
        (PrefixPigeonhole.prefixPolynomial K m z)
        (PrefixPigeonhole.prefixPolynomial K m z - SP.locator S) = S := by
  let U := PrefixPigeonhole.prefixPolynomial K m z
  have hU : U.IsMonicOfDegree m :=
    PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z
  have hSprefixFinset :
      S ∈ PrefixPigeonhole.prefixSupportFinset D U K m :=
    (PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
      D hKm z S).mp hS
  have hSprefix : S ∈ ExactPrefixList.prefixSupportSet D U K m :=
    (PrefixPigeonhole.mem_prefixSupportFinset_iff D U K m S).mp
      hSprefixFinset
  have hP := ExactPrefixList.prefixSupport_to_listPolynomial
    D U K m hSprefix
  have hlocator :=
    (ExactPrefixList.listPolynomial_locator D U hU hKpos hKm hP).2
  apply SP.locator_injective
  calc
    SP.locator (ExactPrefixList.agreementSet D U (U - SP.locator S)) =
        U - (U - SP.locator S) := hlocator.symm
    _ = SP.locator S := sub_sub_cancel _ _

/-- On the pole line, the point produced by a prefix support retains exactly
that support as its agreement set. -/
theorem lineAgreementSet_image_eq_support
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F) {S : Finset F}
    (hS : S ∈ PrefixPigeonhole.coefficientFiber D K m z)
    (alpha : F) (halpha : alpha ∉ D) :
    ((Finset.univ.filter fun x : ↥D ↦
      (ExactListLine.explainingPolynomial alpha
        (PrefixPigeonhole.prefixPolynomial K m z - SP.locator S)).eval x.1 =
          CollisionAwarePole.fpole
              (domainEval D)
              (polynomialWord D
                (PrefixPigeonhole.prefixPolynomial K m z)) alpha x +
            (PrefixPigeonhole.prefixPolynomial K m z - SP.locator S).eval alpha *
              CollisionAwarePole.gpole (domainEval D) alpha x)).image
        (fun x : ↥D ↦ x.1) = S := by
  rw [ExactListLine.lineAgreementSet_eq_polynomialAgreementSet
    (domainEval D)
    (polynomialWord D (PrefixPigeonhole.prefixPolynomial K m z)) alpha
    (domainEval_ne_of_not_mem D halpha)
    (PrefixPigeonhole.prefixPolynomial K m z - SP.locator S)]
  rw [image_polynomialAgreementSet_eq]
  exact prefixPolynomial_agreementSet_eq_support D hKpos hKm z hS

/-- The direct prefix-support-to-slope map has image exactly the full MCA-bad
slope set of the same-field pole line. -/
theorem coefficientFiber_slope_image_eq_badSlopeSet
    [Fintype F] [DecidableEq F]
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F) (alpha : F) (halpha : alpha ∉ D) :
    (PrefixPigeonhole.coefficientFiber D K m z).image
        (fun S ↦ (PrefixPigeonhole.prefixPolynomial K m z -
          SP.locator S).eval alpha) =
      ExactListLine.badSlopeSet
        (domainEval D)
        (polynomialWord D (PrefixPigeonhole.prefixPolynomial K m z))
        alpha (K - 1) m := by
  let U := PrefixPigeonhole.prefixPolynomial K m z
  let L := PrefixPigeonhole.listedPolynomials D U K m
  have hU : U.IsMonicOfDegree m :=
    PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z
  have himage := ExactListLine.image_eval_eq_badSlopeSet
    (domainEval D) Subtype.val_injective (polynomialWord D U)
    alpha (domainEval_ne_of_not_mem D halpha) (K - 1) m
    (by omega) L
    (fun P hP ↦ listedPolynomial_natDegree_le_pred
      D U hU hKpos hKm hP)
    (fun P hP ↦ listedPolynomial_agreements
      D U hU hKpos hKm hP)
    (fun P hdegree hagree ↦ mem_listedPolynomials_of_degree_agreements
      D U hU hKpos hKm P hdegree hagree)
  have hfiber :
      PrefixPigeonhole.coefficientFiber D K m z =
        PrefixPigeonhole.prefixSupportFinset D U K m := by
    ext S
    exact PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
      D hKm z S
  rw [hfiber]
  simpa only [L, U, PrefixPigeonhole.listedPolynomials,
    Finset.image_image, Function.comp_apply] using himage

/-- At a pole separating the listed polynomials, the number of MCA-bad slopes
is exactly the prefix-fiber size. -/
theorem badSlopeSet_card_eq_coefficientFiber
    [Fintype F] [DecidableEq F]
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F) (alpha : F) (halpha : alpha ∉ D)
    (hseparates : Set.InjOn (fun P : F[X] ↦ P.eval alpha)
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m : Set F[X])) :
    (ExactListLine.badSlopeSet
      (domainEval D)
      (polynomialWord D (PrefixPigeonhole.prefixPolynomial K m z))
      alpha (K - 1) m).card =
        (PrefixPigeonhole.coefficientFiber D K m z).card := by
  rw [← coefficientFiber_slope_image_eq_badSlopeSet
    D hKpos hKm z alpha halpha]
  apply Finset.card_image_of_injOn
  intro S hS T hT hST
  apply SP.locator_injective
  apply sub_right_injective
  apply hseparates
  · apply (PrefixPigeonhole.mem_listedPolynomials_iff D
      (PrefixPigeonhole.prefixPolynomial K m z)
      (PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z)
      hKpos hKm _).mpr
    apply ExactPrefixList.prefixSupport_to_listPolynomial
    apply (PrefixPigeonhole.mem_prefixSupportFinset_iff D
      (PrefixPigeonhole.prefixPolynomial K m z) K m S).mp
    exact (PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
      D hKm z S).mp hS
  · apply (PrefixPigeonhole.mem_listedPolynomials_iff D
      (PrefixPigeonhole.prefixPolynomial K m z)
      (PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z)
      hKpos hKm _).mpr
    apply ExactPrefixList.prefixSupport_to_listPolynomial
    apply (PrefixPigeonhole.mem_prefixSupportFinset_iff D
      (PrefixPigeonhole.prefixPolynomial K m z) K m T).mp
    exact (PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
      D hKm z T).mp hT
  · exact hST

#print axioms prefixPolynomial_agreementSet_eq_support
#print axioms lineAgreementSet_image_eq_support
#print axioms coefficientFiber_slope_image_eq_badSlopeSet
#print axioms badSlopeSet_card_eq_coefficientFiber

end GrandeFinale.ExactPrefixRay
