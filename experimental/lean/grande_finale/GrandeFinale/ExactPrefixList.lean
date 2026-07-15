import GrandeFinale.CollisionAwarePole
import GrandeFinale.SP

/-!
# Exact locator-prefix list correspondence

This module formalizes the exact finite support/list correspondence and the
no-extra-agreement clause in `prop:exact-prefix-list` of
`experimental/asymptotic_rs_mca_frontiers.tex`.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.ExactPrefixList

variable {F : Type*} [Field F]

/-- Evaluation points where `U` and `P` agree. -/
def agreementSet (D : Finset F) (U P : F[X]) : Finset F :=
  D.filter fun x ↦ U.eval x = P.eval x

/-- A depth-`m-K` locator-prefix fiber, represented by its equivalent exact
leading-coefficient cancellation condition. -/
def prefixSupportSet
    (D : Finset F) (U : F[X]) (K m : Nat) : Set (Finset F) :=
  {S | S ⊆ D ∧ S.card = m ∧
    (U - SP.locator S).degree < (K : WithBot Nat)}

/-- A degree-less-than-`K` polynomial in the radius-`m` list of `U`. -/
def listPolynomialSet
    (D : Finset F) (U : F[X]) (K m : Nat) : Set F[X] :=
  {P | P.degree < (K : WithBot Nat) ∧
    m ≤ (agreementSet D U P).card}

/-- A lower-degree polynomial cannot agree with a monic degree-`m`
polynomial at more than `m` evaluation points. -/
theorem agreementSet_card_le
    (D : Finset F) (U : F[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKm : K ≤ m)
    {P : F[X]} (hP : P.degree < (K : WithBot Nat)) :
    (agreementSet D U P).card ≤ m := by
  have hUdegree : U.degree = (m : WithBot Nat) := by
    rw [Polynomial.degree_eq_natDegree hU.ne_zero, hU.natDegree_eq]
  have hP_lt_U : P.degree < U.degree := by
    rw [hUdegree]
    exact hP.trans_le (WithBot.coe_le_coe.mpr hKm)
  have hUP : U ≠ P := by
    intro h
    subst P
    exact (lt_irrefl U.degree) hP_lt_U
  have hdegree : (U - P).degree = U.degree :=
    Polynomial.degree_sub_eq_left_of_degree_lt hP_lt_U
  have hnatDegree : (U - P).natDegree ≤ m := by
    rw [Polynomial.natDegree_eq_of_degree_eq hdegree, hU.natDegree_eq]
  exact CollisionAwarePole.poly_agree_card_le hUP hnatDegree D

/-- Every support in the prefix fiber produces a listed polynomial. -/
theorem prefixSupport_to_listPolynomial
    (D : Finset F) (U : F[X]) (K m : Nat)
    {S : Finset F} (hS : S ∈ prefixSupportSet D U K m) :
    U - SP.locator S ∈ listPolynomialSet D U K m := by
  rcases hS with ⟨hSD, hScard, hdegree⟩
  refine ⟨hdegree, ?_⟩
  rw [← hScard]
  apply Finset.card_le_card
  intro x hx
  rw [agreementSet, Finset.mem_filter]
  refine ⟨hSD hx, ?_⟩
  have hlocatorEval : (SP.locator S).eval x = 0 := by
    rw [SP.locator, Polynomial.eval_prod]
    exact Finset.prod_eq_zero hx (by simp)
  simp [eval_sub, hlocatorEval]

/-- A listed polynomial determines its full agreement support and its locator
exactly. -/
theorem listPolynomial_locator
    (D : Finset F) (U : F[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m)
    {P : F[X]} (hP : P ∈ listPolynomialSet D U K m) :
    let S := agreementSet D U P
    S.card = m ∧ U - P = SP.locator S := by
  rcases hP with ⟨hPdegree, hPlist⟩
  let S := agreementSet D U P
  have hSle : S.card ≤ m :=
    agreementSet_card_le D U hU hKm hPdegree
  have hScard : S.card = m := Nat.le_antisymm hSle hPlist
  have hmpos : 0 < m := hKpos.trans_le hKm
  have hPnat : P.natDegree < m := by
    by_cases hPzero : P = 0
    · simpa [hPzero] using hmpos
    · exact (Polynomial.natDegree_lt_iff_degree_lt hPzero).2
        (hPdegree.trans_le (WithBot.coe_le_coe.mpr hKm))
  have hdiff : (U - P).IsMonicOfDegree m := hU.sub hPnat
  have hzero : ∀ x ∈ S, (U - P).eval x = 0 := by
    intro x hx
    have hagree := (Finset.mem_filter.mp hx).2
    simp [eval_sub, hagree]
  have hroots : (U - P).roots = S.val := by
    apply Polynomial.roots_eq_of_degree_eq_card hzero
    simp [Polynomial.degree_eq_natDegree hdiff.ne_zero,
      hdiff.natDegree_eq, hScard]
  have hrootCard :
      Multiset.card (U - P).roots = (U - P).natDegree := by
    simp [hroots, hScard, hdiff.natDegree_eq]
  have hproduct :=
    Polynomial.prod_multiset_X_sub_C_of_monic_of_roots_card_eq
      hdiff.monic hrootCard
  have hlocator : U - P = SP.locator S := by
    rw [hroots] at hproduct
    simpa [SP.locator] using hproduct.symm
  exact ⟨hScard, hlocator⟩

/-- Exact prefix-list correspondence: listed polynomials are uniquely
`U - locator(S)` for supports in the prefix fiber. -/
theorem listPolynomial_iff_existsUnique_prefixSupport
    (D : Finset F) (U : F[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m)
    (P : F[X]) :
    P ∈ listPolynomialSet D U K m ↔
      ∃! S : Finset F,
        S ∈ prefixSupportSet D U K m ∧ P = U - SP.locator S := by
  constructor
  · intro hP
    let S := agreementSet D U P
    obtain ⟨hScard, hlocator⟩ :=
      listPolynomial_locator D U hU hKpos hKm hP
    have hSD : S ⊆ D := Finset.filter_subset _ _
    have hlocatorS : U - P = SP.locator S := by
      simpa [S] using hlocator
    have hPformS : P = U - SP.locator S := by
      rw [← hlocatorS, sub_sub_cancel]
    have hdegree : (U - SP.locator S).degree < (K : WithBot Nat) := by
      rw [← hPformS]
      exact hP.1
    refine ⟨S, ⟨⟨hSD, hScard, hdegree⟩, hPformS⟩, ?_⟩
    intro T hT
    rcases hT with ⟨⟨hTD, hTcard, _hTdegree⟩, hPform⟩
    have hTS : T ⊆ agreementSet D U P := by
      intro x hx
      rw [agreementSet, Finset.mem_filter]
      refine ⟨hTD hx, ?_⟩
      rw [hPform, eval_sub]
      have hlocatorEval : (SP.locator T).eval x = 0 := by
        rw [SP.locator, Polynomial.eval_prod]
        exact Finset.prod_eq_zero hx (by simp)
      simp [hlocatorEval]
    simpa [S] using Finset.eq_of_subset_of_card_le hTS (by
      rw [hScard, hTcard])
  · rintro ⟨S, ⟨hS, rfl⟩, _hunique⟩
    exact prefixSupport_to_listPolynomial D U K m hS

/-- Every listed polynomial has exactly `m` agreements, hence none has more. -/
theorem listPolynomial_agreementSet_card_eq
    (D : Finset F) (U : F[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m)
    {P : F[X]} (hP : P ∈ listPolynomialSet D U K m) :
    (agreementSet D U P).card = m :=
  (listPolynomial_locator D U hU hKpos hKm hP).1

#print axioms agreementSet_card_le
#print axioms prefixSupport_to_listPolynomial
#print axioms listPolynomial_locator
#print axioms listPolynomial_iff_existsUnique_prefixSupport
#print axioms listPolynomial_agreementSet_card_eq

end GrandeFinale.ExactPrefixList
