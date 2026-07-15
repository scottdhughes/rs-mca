import GrandeFinale.ExactPrefixRay

/-!
# Exact locator-prefix ray witness uniqueness

This module completes the same-field witness-incidence clause of
`cor:exact-prefix-ray-realization` in
`experimental/asymptotic_rs_mca_frontiers.tex`. At a separating pole, every
degree-bounded explanation of a slope coming from a prefix support reconstructs
the same listed polynomial, quotient explanation, and exact agreement support.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.ExactPrefixRayUniqueness

variable {F : Type*} [Field F]

/-- The positions of `S` viewed in the subtype evaluation domain `D`. -/
def supportOnDomain (D S : Finset F) : Finset ↥D :=
  Finset.univ.filter fun x ↦ x.1 ∈ S

omit [Field F] in
theorem mem_supportOnDomain (D S : Finset F) (x : ↥D) :
    x ∈ supportOnDomain D S ↔ x.1 ∈ S := by
  simp [supportOnDomain]

omit [Field F] in
theorem image_supportOnDomain_eq
    (D S : Finset F) (hSD : S ⊆ D) :
    (supportOnDomain D S).image (fun x : ↥D ↦ x.1) = S := by
  ext x
  constructor
  · intro hx
    obtain ⟨y, hy, rfl⟩ := Finset.mem_image.mp hx
    exact (Finset.mem_filter.mp hy).2
  · intro hx
    apply Finset.mem_image.mpr
    refine ⟨⟨x, hSD hx⟩, ?_, rfl⟩
    simp [supportOnDomain, hx]

omit [Field F] in
theorem supportOnDomain_card_eq
    (D S : Finset F) (hSD : S ⊆ D) :
    (supportOnDomain D S).card = S.card := by
  calc
    (supportOnDomain D S).card =
        ((supportOnDomain D S).image (fun x : ↥D ↦ x.1)).card :=
      (Finset.card_image_of_injective _ Subtype.val_injective).symm
    _ = S.card := by rw [image_supportOnDomain_eq D S hSD]

theorem mem_polynomialAgreementSet
    (D : Finset F) (U P : F[X]) (x : F) :
    x ∈ ExactPrefixList.agreementSet D U P ↔
      x ∈ D ∧ U.eval x = P.eval x := by
  simp [ExactPrefixList.agreementSet]

/-- A support in the coefficient fiber produces a member of the complete
finite polynomial list. -/
theorem listedPolynomial_mem_of_mem_coefficientFiber
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F) {S : Finset F}
    (hS : S ∈ PrefixPigeonhole.coefficientFiber D K m z) :
    PrefixPigeonhole.prefixPolynomial K m z - SP.locator S ∈
      PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m := by
  apply (PrefixPigeonhole.mem_listedPolynomials_iff D
    (PrefixPigeonhole.prefixPolynomial K m z)
    (PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z)
    hKpos hKm _).mpr
  apply ExactPrefixList.prefixSupport_to_listPolynomial
  apply (PrefixPigeonhole.mem_prefixSupportFinset_iff D
    (PrefixPigeonhole.prefixPolynomial K m z) K m S).mp
  exact (PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
    D hKm z S).mp hS

/-- Any sufficiently large degree-bounded explanation of the line point
coming from `S` is the displayed quotient explanation, and its support is
exactly `S`. -/
theorem explanation_eq_and_support_image_eq
    [Fintype F] [DecidableEq F]
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F) {S : Finset F}
    (hS : S ∈ PrefixPigeonhole.coefficientFiber D K m z)
    (alpha : F) (halpha : alpha ∉ D)
    (hseparates : Set.InjOn (fun P : F[X] ↦ P.eval alpha)
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m : Set F[X]))
    (T : Finset ↥D) (hmT : m ≤ T.card) (G : F[X])
    (hGdegree : G.degree < ((K - 1 : Nat) : WithBot Nat))
    (hGline : ∀ x ∈ T,
      G.eval x.1 =
        CollisionAwarePole.fpole
            (ExactPrefixRay.domainEval D)
            (ExactPrefixRay.polynomialWord D
              (PrefixPigeonhole.prefixPolynomial K m z)) alpha x +
          (PrefixPigeonhole.prefixPolynomial K m z - SP.locator S).eval alpha *
            CollisionAwarePole.gpole
              (ExactPrefixRay.domainEval D) alpha x) :
    G = ExactListLine.explainingPolynomial alpha
        (PrefixPigeonhole.prefixPolynomial K m z - SP.locator S) ∧
      T.image (fun x : ↥D ↦ x.1) = S := by
  let U := PrefixPigeonhole.prefixPolynomial K m z
  let P := U - SP.locator S
  let gamma := P.eval alpha
  let P' : F[X] := (X - C alpha) * G + C gamma
  have hU : U.IsMonicOfDegree m :=
    PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z
  have hPmem : P ∈ PrefixPigeonhole.listedPolynomials D U K m := by
    exact listedPolynomial_mem_of_mem_coefficientFiber
      D hKpos hKm z hS
  have hP'degree : P'.natDegree ≤ K - 1 := by
    have hprod : ((X - C alpha) * G).natDegree ≤ K - 1 := by
      by_cases hGzero : G = 0
      · simp [hGzero]
      · have hGnat : G.natDegree < K - 1 :=
          (natDegree_lt_iff_degree_lt hGzero).mpr hGdegree
        rw [natDegree_mul (X_sub_C_ne_zero alpha) hGzero,
          natDegree_X_sub_C]
        omega
    exact (natDegree_add_le _ _).trans (by simp [hprod])
  have hTsub : T ⊆ ExactListLine.polynomialAgreementSet
      (ExactPrefixRay.domainEval D) (ExactPrefixRay.polynomialWord D U) P' := by
    intro x hx
    apply (ExactListLine.mem_polynomialAgreementSet
      (ExactPrefixRay.domainEval D) (ExactPrefixRay.polynomialWord D U)
      P' x).mpr
    have hline :
        G.eval x.1 =
          CollisionAwarePole.fpole
              (ExactPrefixRay.domainEval D)
              (ExactPrefixRay.polynomialWord D U) alpha x +
            gamma * CollisionAwarePole.gpole
              (ExactPrefixRay.domainEval D) alpha x := by
      simpa [U, P, gamma] using hGline x hx
    have hne : x.1 - alpha ≠ 0 := by
      exact sub_ne_zero.mpr (ExactPrefixRay.domainEval_ne_of_not_mem
        D halpha x)
    dsimp [P']
    simp only [eval_add, eval_mul, eval_sub, eval_X, eval_C]
    dsimp [CollisionAwarePole.fpole, CollisionAwarePole.gpole] at hline
    field_simp [hne] at hline
    calc
      U.eval x.1 = (U.eval x.1 + -gamma) + gamma := by ring
      _ = G.eval x.1 * (x.1 - alpha) + gamma := by rw [← hline]
      _ = (x.1 - alpha) * G.eval x.1 + gamma := by ring
  have hP'mem : P' ∈ PrefixPigeonhole.listedPolynomials D U K m := by
    apply ExactPrefixRay.mem_listedPolynomials_of_degree_agreements
      D U hU hKpos hKm P' hP'degree
    exact hmT.trans (Finset.card_le_card hTsub)
  have hP'eq : P' = P := by
    apply hseparates hP'mem hPmem
    simp [P', gamma]
  have hsupport : ExactPrefixList.agreementSet D U P = S := by
    have h := ExactPrefixRay.prefixPolynomial_agreementSet_eq_support
      D hKpos hKm z hS
    change ExactPrefixList.agreementSet D U P = S at h
    exact h
  have hTimageSub : T.image (fun x : ↥D ↦ x.1) ⊆ S := by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hy
    rw [← hsupport]
    apply (mem_polynomialAgreementSet D U P x.1).mpr
    refine ⟨x.property, ?_⟩
    have hagree := (ExactListLine.mem_polynomialAgreementSet
      (ExactPrefixRay.domainEval D) (ExactPrefixRay.polynomialWord D U)
      P' x).mp (hTsub hx)
    rw [hP'eq] at hagree
    exact hagree
  have hScard : S.card = m := by
    have hSprefix : S ∈ ExactPrefixList.prefixSupportSet D U K m := by
      apply (PrefixPigeonhole.mem_prefixSupportFinset_iff D U K m S).mp
      exact (PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
        D hKm z S).mp hS
    exact hSprefix.2.1
  have hTimage : T.image (fun x : ↥D ↦ x.1) = S := by
    apply Finset.eq_of_subset_of_card_le hTimageSub
    rw [hScard, Finset.card_image_of_injective _ Subtype.val_injective]
    exact hmT
  refine ⟨?_, hTimage⟩
  apply mul_left_cancel₀ (X_sub_C_ne_zero alpha)
  rw [← ExactListLine.explainingPolynomial_spec alpha P]
  calc
    (X - C alpha) * G = P' - C gamma := by simp [P']
    _ = P - C (P.eval alpha) := by rw [hP'eq]

/-- Exact line witnesses consist of a sufficiently large support and a
degree-bounded polynomial explaining the selected line point there. -/
def IsExactLineWitness
    (D : Finset F) (U : F[X]) (alpha : F) (k m : Nat) (gamma : F)
    (w : Finset ↥D × F[X]) : Prop :=
  m ≤ w.1.card ∧ w.2.degree < (k : WithBot Nat) ∧
    ∀ x ∈ w.1,
      w.2.eval x.1 =
        CollisionAwarePole.fpole
            (ExactPrefixRay.domainEval D)
            (ExactPrefixRay.polynomialWord D U) alpha x +
          gamma * CollisionAwarePole.gpole
            (ExactPrefixRay.domainEval D) alpha x

/-- At a separating pole, each prefix support has exactly one exact line
witness: its full support and its quotient explaining polynomial. -/
theorem existsUnique_exactLineWitness
    [Fintype F] [DecidableEq F]
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F) {S : Finset F}
    (hS : S ∈ PrefixPigeonhole.coefficientFiber D K m z)
    (alpha : F) (halpha : alpha ∉ D)
    (hseparates : Set.InjOn (fun P : F[X] ↦ P.eval alpha)
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m : Set F[X])) :
    ∃! w : Finset ↥D × F[X],
      IsExactLineWitness D (PrefixPigeonhole.prefixPolynomial K m z)
        alpha (K - 1) m
        ((PrefixPigeonhole.prefixPolynomial K m z - SP.locator S).eval alpha)
        w := by
  let U := PrefixPigeonhole.prefixPolynomial K m z
  let P := U - SP.locator S
  let T₀ := supportOnDomain D S
  let G₀ := ExactListLine.explainingPolynomial alpha P
  have hSprefix : S ∈ ExactPrefixList.prefixSupportSet D U K m := by
    apply (PrefixPigeonhole.mem_prefixSupportFinset_iff D U K m S).mp
    exact (PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
      D hKm z S).mp hS
  have hSD : S ⊆ D := hSprefix.1
  have hScard : S.card = m := hSprefix.2.1
  have hPmem : P ∈ PrefixPigeonhole.listedPolynomials D U K m := by
    exact listedPolynomial_mem_of_mem_coefficientFiber
      D hKpos hKm z hS
  have hPdegree : P.natDegree ≤ K - 1 :=
    ExactPrefixRay.listedPolynomial_natDegree_le_pred D U
      (PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z)
      hKpos hKm hPmem
  have hsupport : ExactPrefixList.agreementSet D U P = S := by
    have h := ExactPrefixRay.prefixPolynomial_agreementSet_eq_support
      D hKpos hKm z hS
    change ExactPrefixList.agreementSet D U P = S at h
    exact h
  refine ⟨(T₀, G₀), ?_, ?_⟩
  · refine ⟨?_, ExactListLine.explainingPolynomial_degree_lt
      alpha P hPdegree, ?_⟩
    · rw [supportOnDomain_card_eq D S hSD, hScard]
    · intro x hx
      apply (ExactListLine.explainingPolynomial_agrees_iff
        (ExactPrefixRay.domainEval D) (ExactPrefixRay.polynomialWord D U)
        alpha (ExactPrefixRay.domainEval_ne_of_not_mem D halpha) P x).mpr
      have hxS : x.1 ∈ S := (mem_supportOnDomain D S x).mp hx
      have hxAgreement : x.1 ∈ ExactPrefixList.agreementSet D U P := by
        rw [hsupport]
        exact hxS
      exact (mem_polynomialAgreementSet D U P x.1).mp hxAgreement |>.2
  · rintro ⟨T, G⟩ hTG
    obtain ⟨hG, hTimage⟩ := explanation_eq_and_support_image_eq
      D hKpos hKm z hS alpha halpha hseparates T hTG.1 G hTG.2.1 hTG.2.2
    apply Prod.ext
    · apply Finset.ext
      intro x
      simp only [T₀, supportOnDomain, Finset.mem_filter,
        Finset.mem_univ, true_and]
      rw [← hTimage]
      simp
    · exact hG

#print axioms explanation_eq_and_support_image_eq
#print axioms existsUnique_exactLineWitness

end GrandeFinale.ExactPrefixRayUniqueness
