import GrandeFinale.ExactPrefixRayUniqueness

/-!
# Finite separating-pole existence

This module formalizes the exact unordered-pair root-avoidance bound in
equation (4.6) of `experimental/asymptotic_rs_mca_frontiers.tex`. A finite
field larger than the evaluation domain plus `k * choose L 2` contains a pole
outside the domain at which every polynomial in a degree-`k` list has a
distinct value.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.SeparatingPole

variable {F : Type*} [Field F]

/-- A chosen first element of a two-element finset. The value is irrelevant
outside the cardinality-two case. -/
def pairLeft (A : Finset F[X]) : F[X] :=
  if hA : A.card = 2 then
    Classical.choose (Finset.card_eq_two.mp hA)
  else 0

/-- A chosen second element of a two-element finset. -/
def pairRight (A : Finset F[X]) : F[X] :=
  if hA : A.card = 2 then
    Classical.choose (Classical.choose_spec (Finset.card_eq_two.mp hA))
  else 0

theorem pairLeft_ne_pairRight
    (A : Finset F[X]) (hA : A.card = 2) :
    pairLeft A ≠ pairRight A := by
  rw [pairLeft, pairRight, dif_pos hA, dif_pos hA]
  exact (Classical.choose_spec
    (Classical.choose_spec (Finset.card_eq_two.mp hA))).1

theorem pair_eq_pairLeft_pairRight
    (A : Finset F[X]) (hA : A.card = 2) :
    A = {pairLeft A, pairRight A} := by
  rw [pairLeft, pairRight, dif_pos hA, dif_pos hA]
  exact (Classical.choose_spec
    (Classical.choose_spec (Finset.card_eq_two.mp hA))).2

theorem pairLeft_mem (A : Finset F[X]) (hA : A.card = 2) :
    pairLeft A ∈ A := by
  have hmem : pairLeft A ∈
      ({pairLeft A, pairRight A} : Finset F[X]) := by simp
  rw [← pair_eq_pairLeft_pairRight A hA] at hmem
  exact hmem

theorem pairRight_mem (A : Finset F[X]) (hA : A.card = 2) :
    pairRight A ∈ A := by
  have hmem : pairRight A ∈
      ({pairLeft A, pairRight A} : Finset F[X]) := by simp
  rw [← pair_eq_pairLeft_pairRight A hA] at hmem
  exact hmem

/-- The nonzero polynomial attached to an unordered pair. -/
def pairDifference (A : Finset F[X]) : F[X] :=
  pairLeft A - pairRight A

theorem pairDifference_ne_zero
    (A : Finset F[X]) (hA : A.card = 2) :
    pairDifference A ≠ 0 :=
  sub_ne_zero.mpr (pairLeft_ne_pairRight A hA)

/-- Product of one difference polynomial for each unordered pair in `L`. -/
def separatingPolynomial (L : Finset F[X]) : F[X] :=
  ∏ A ∈ L.powersetCard 2, pairDifference A

theorem separatingPolynomial_ne_zero (L : Finset F[X]) :
    separatingPolynomial L ≠ 0 := by
  rw [separatingPolynomial, Finset.prod_ne_zero_iff]
  intro A hA
  exact pairDifference_ne_zero A (Finset.mem_powersetCard.mp hA).2

theorem separatingPolynomial_natDegree_le
    (L : Finset F[X]) (k : Nat)
    (hdegree : ∀ P ∈ L, P.natDegree ≤ k) :
    (separatingPolynomial L).natDegree ≤ L.card.choose 2 * k := by
  calc
    (separatingPolynomial L).natDegree ≤
        ∑ A ∈ L.powersetCard 2, (pairDifference A).natDegree := by
      exact natDegree_prod_le _ _
    _ ≤ ∑ _A ∈ L.powersetCard 2, k := by
      apply Finset.sum_le_sum
      intro A hA
      have hpair := Finset.mem_powersetCard.mp hA
      exact (natDegree_sub_le _ _).trans (max_le
        (hdegree (pairLeft A) (hpair.1 (pairLeft_mem A hpair.2)))
        (hdegree (pairRight A) (hpair.1 (pairRight_mem A hpair.2))))
    _ = L.card.choose 2 * k := by
      simp [Finset.card_powersetCard]

/-- Exact equation-(4.6) root-avoidance bound: there is an off-domain pole
separating every polynomial in the list. -/
theorem exists_separating_pole
    [Fintype F] [DecidableEq F]
    (D : Finset F) (k : Nat) (L : Finset F[X])
    (hdegree : ∀ P ∈ L, P.natDegree ≤ k)
    (hbudget : D.card + k * L.card.choose 2 < Fintype.card F) :
    ∃ alpha : F, alpha ∉ D ∧
      Set.InjOn (fun P : F[X] ↦ P.eval alpha) (L : Set F[X]) := by
  let R := separatingPolynomial L
  have hRne : R ≠ 0 := separatingPolynomial_ne_zero L
  have hRdegree : R.natDegree ≤ k * L.card.choose 2 := by
    have h := separatingPolynomial_natDegree_le L k hdegree
    simpa [R, Nat.mul_comm] using h
  let bad : Finset F := D ∪ R.roots.toFinset
  have hbadcard : bad.card < Fintype.card F := by
    calc
      bad.card ≤ D.card + R.roots.toFinset.card := Finset.card_union_le _ _
      _ ≤ D.card + R.natDegree := Nat.add_le_add_left
        ((Multiset.toFinset_card_le _).trans (Polynomial.card_roots' R)) _
      _ ≤ D.card + k * L.card.choose 2 := Nat.add_le_add_left hRdegree _
      _ < Fintype.card F := hbudget
  have hexists : ∃ alpha : F, alpha ∉ bad := by
    by_contra hnone
    push_neg at hnone
    have hcard := Finset.card_le_card
      (fun alpha _ ↦ hnone alpha : (Finset.univ : Finset F) ⊆ bad)
    rw [Finset.card_univ] at hcard
    omega
  obtain ⟨alpha, halpha⟩ := hexists
  have halphaParts : alpha ∉ D ∧ alpha ∉ R.roots.toFinset := by
    simpa [bad] using halpha
  refine ⟨alpha, halphaParts.1, ?_⟩
  intro P hP Q hQ hEval
  by_contra hPQ
  let A : Finset F[X] := {P, Q}
  have hAcard : A.card = 2 := by simp [A, hPQ]
  have hAsub : A ⊆ L := by
    intro T hT
    simp only [A, Finset.mem_insert, Finset.mem_singleton] at hT
    rcases hT with rfl | rfl
    · exact hP
    · exact hQ
  have hAmem : A ∈ L.powersetCard 2 :=
    Finset.mem_powersetCard.mpr ⟨hAsub, hAcard⟩
  have hleft : pairLeft A = P ∨ pairLeft A = Q := by
    have := pairLeft_mem A hAcard
    simpa [A] using this
  have hright : pairRight A = P ∨ pairRight A = Q := by
    have := pairRight_mem A hAcard
    simpa [A] using this
  have hleftEval : (pairLeft A).eval alpha = P.eval alpha := by
    rcases hleft with hleft | hleft
    · rw [hleft]
    · rw [hleft]
      exact hEval.symm
  have hrightEval : (pairRight A).eval alpha = P.eval alpha := by
    rcases hright with hright | hright
    · rw [hright]
    · rw [hright]
      exact hEval.symm
  have hpairRoot : (pairDifference A).eval alpha = 0 := by
    simp [pairDifference, eval_sub, hleftEval, hrightEval]
  have hdvd : pairDifference A ∣ R := by
    dsimp [R, separatingPolynomial]
    exact Finset.dvd_prod_of_mem (fun A ↦ pairDifference A) hAmem
  have hRroot : R.eval alpha = 0 := by
    obtain ⟨T, hT⟩ := hdvd
    rw [hT, eval_mul, hpairRoot, zero_mul]
  exact halphaParts.2
    (Multiset.mem_toFinset.mpr ((Polynomial.mem_roots hRne).mpr hRroot))

/-- The exact complete prefix list admits a separating off-domain pole under
the literal equation-(4.6) budget with code parameter `K - 1`. -/
theorem exists_prefixFiber_separating_pole
    [Fintype F] [DecidableEq F]
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F)
    (hbudget : D.card + (K - 1) *
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m).card.choose 2 <
        Fintype.card F) :
    ∃ alpha : F, alpha ∉ D ∧
      Set.InjOn (fun P : F[X] ↦ P.eval alpha)
        (PrefixPigeonhole.listedPolynomials D
          (PrefixPigeonhole.prefixPolynomial K m z) K m : Set F[X]) := by
  apply exists_separating_pole D (K - 1)
    (PrefixPigeonhole.listedPolynomials D
      (PrefixPigeonhole.prefixPolynomial K m z) K m)
  · intro P hP
    exact ExactPrefixRay.listedPolynomial_natDegree_le_pred D
      (PrefixPigeonhole.prefixPolynomial K m z)
      (PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z)
      hKpos hKm hP
  · exact hbudget

/-- Under the exact pole-existence budget, some pole realizes precisely as
many MCA-bad slopes as there are supports in the coefficient fiber. -/
theorem exists_prefixFiber_badSlopeSet_card_eq
    [Fintype F] [DecidableEq F]
    (D : Finset F) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → F)
    (hbudget : D.card + (K - 1) *
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m).card.choose 2 <
        Fintype.card F) :
    ∃ alpha : F, alpha ∉ D ∧
      (ExactListLine.badSlopeSet
        (ExactPrefixRay.domainEval D)
        (ExactPrefixRay.polynomialWord D
          (PrefixPigeonhole.prefixPolynomial K m z))
        alpha (K - 1) m).card =
          (PrefixPigeonhole.coefficientFiber D K m z).card := by
  obtain ⟨alpha, halpha, hseparates⟩ :=
    exists_prefixFiber_separating_pole D hKpos hKm z hbudget
  exact ⟨alpha, halpha,
    ExactPrefixRay.badSlopeSet_card_eq_coefficientFiber
      D hKpos hKm z alpha halpha hseparates⟩

#print axioms separatingPolynomial_natDegree_le
#print axioms exists_separating_pole
#print axioms exists_prefixFiber_separating_pole
#print axioms exists_prefixFiber_badSlopeSet_card_eq

end GrandeFinale.SeparatingPole
