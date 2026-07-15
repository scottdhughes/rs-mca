import GrandeFinale.SeparatingPole

/-!
# Scalar-extension exact list--line interface

This module formalizes the base-to-extension descent step in
`thm:exact-list-line-bijection` from
`experimental/asymptotic_rs_mca_frontiers.tex`. A degree-bounded polynomial
over the extension that agrees sufficiently often with a base-valued received
word is obtained by mapping a base-field polynomial. Consequently a complete
base-field list remains complete against ambient-field explanations.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.ScalarExtensionListLine

variable {B F : Type*} [Field B] [Field F] [Algebra B F]

/-- Inclusion of the finite base-field evaluation domain. -/
abbrev baseEval (D : Finset B) : ↥D → B := fun x ↦ x.1

/-- Evaluation-domain inclusion followed by the scalar embedding. -/
abbrev extensionEval (D : Finset B) : ↥D → F :=
  fun x ↦ algebraMap B F x.1

/-- Scalar extension of a base-valued received word. -/
abbrev extensionWord {D : Finset B} (U : ↥D → B) : ↥D → F :=
  fun x ↦ algebraMap B F (U x)

/-- Coefficientwise scalar extension of a finite polynomial list. -/
def mappedPolynomialList (L : Finset B[X]) : Finset F[X] :=
  L.image fun P ↦ P.map (algebraMap B F)

theorem mappedPolynomialList_card (L : Finset B[X]) :
    (mappedPolynomialList (F := F) L).card = L.card := by
  apply Finset.card_image_of_injective
  exact Polynomial.map_injective (algebraMap B F) (algebraMap B F).injective

theorem extensionEval_injective (D : Finset B) :
    Function.Injective (extensionEval (F := F) D) := by
  intro x y hxy
  apply Subtype.ext
  exact (algebraMap B F).injective hxy

/-- Agreement supports are unchanged when both the word and polynomial are
mapped to the extension. -/
theorem extensionAgreementSet_map_eq_base
    (D : Finset B) (U : ↥D → B) (Q : B[X]) :
    ExactListLine.polynomialAgreementSet
        (extensionEval (F := F) D) (extensionWord (F := F) U)
        (Q.map (algebraMap B F)) =
      ExactListLine.polynomialAgreementSet (baseEval D) U Q := by
  ext x
  rw [ExactListLine.mem_polynomialAgreementSet,
    ExactListLine.mem_polynomialAgreementSet, Polynomial.eval_map_apply]
  change algebraMap B F (U x) = algebraMap B F (Q.eval x.1) ↔
    U x = Q.eval x.1
  exact (algebraMap B F).injective.eq_iff

/-- Vandermonde/interpolation descent: an ambient polynomial of degree at
most `k` agreeing with a base-valued word on at least `m ≥ k+1` positions is
the coefficientwise map of a base polynomial of degree at most `k`. -/
theorem exists_basePolynomial_of_many_agreements
    (D : Finset B) (U : ↥D → B) (k m : Nat) (hkm : k + 1 ≤ m)
    (P : F[X]) (hPdegree : P.natDegree ≤ k)
    (hPagree : m ≤ (ExactListLine.polynomialAgreementSet
      (extensionEval (F := F) D) (extensionWord (F := F) U) P).card) :
    ∃ Q : B[X], Q.natDegree ≤ k ∧
      P = Q.map (algebraMap B F) ∧
      ExactListLine.polynomialAgreementSet
          (extensionEval (F := F) D) (extensionWord (F := F) U) P =
        ExactListLine.polynomialAgreementSet (baseEval D) U Q := by
  let A := ExactListLine.polynomialAgreementSet
    (extensionEval (F := F) D) (extensionWord (F := F) U) P
  have hkA : k + 1 ≤ A.card := hkm.trans hPagree
  obtain ⟨T, hTA, hTcard⟩ := Finset.exists_subset_card_eq hkA
  let Q : B[X] := Lagrange.interpolate T (fun x : ↥D ↦ x.1) U
  have hnodesB : Set.InjOn (fun x : ↥D ↦ x.1) T := by
    intro x _ y _ hxy
    exact Subtype.ext hxy
  have hnodesF : Set.InjOn (fun x : ↥D ↦ algebraMap B F x.1) T := by
    intro x hx y hy hxy
    exact hnodesB hx hy ((algebraMap B F).injective hxy)
  have hQdegree : Q.degree < ((k + 1 : Nat) : WithBot Nat) := by
    have h := Lagrange.degree_interpolate_lt U hnodesB
    rw [hTcard] at h
    exact h
  have hQnatDegree : Q.natDegree ≤ k := by
    by_cases hQzero : Q = 0
    · simp [hQzero]
    · have hnat : Q.natDegree < k + 1 :=
        (natDegree_lt_iff_degree_lt hQzero).mpr hQdegree
      omega
  have hPdegreeLt : P.degree < ((k + 1 : Nat) : WithBot Nat) := by
    by_cases hPzero : P = 0
    · simp [hPzero]
    · apply (natDegree_lt_iff_degree_lt hPzero).mp
      omega
  have hQmapDegree :
      (Q.map (algebraMap B F)).degree <
        ((k + 1 : Nat) : WithBot Nat) := by
    rw [Polynomial.degree_map]
    exact hQdegree
  have hPmap : P = Q.map (algebraMap B F) := by
    apply Polynomial.eq_of_degrees_lt_of_eval_index_eq T hnodesF
      (by simpa [hTcard] using hPdegreeLt)
      (by simpa [hTcard] using hQmapDegree)
    intro x hx
    have hxA : x ∈ A := hTA hx
    have hagree := (ExactListLine.mem_polynomialAgreementSet
      (extensionEval (F := F) D) (extensionWord (F := F) U) P x).mp hxA
    rw [Polynomial.eval_map_apply,
      Lagrange.eval_interpolate_at_node U hnodesB hx]
    exact hagree.symm
  refine ⟨Q, hQnatDegree, hPmap, ?_⟩
  rw [hPmap]
  exact extensionAgreementSet_map_eq_base (F := F) D U Q

theorem mappedPolynomialList_degree
    (L : Finset B[X]) (k : Nat)
    (hdegree : ∀ Q ∈ L, Q.natDegree ≤ k)
    {P : F[X]} (hP : P ∈ mappedPolynomialList (F := F) L) :
    P.natDegree ≤ k := by
  obtain ⟨Q, hQ, rfl⟩ := Finset.mem_image.mp hP
  rw [Polynomial.natDegree_map]
  exact hdegree Q hQ

theorem mappedPolynomialList_agreements
    (D : Finset B) (U : ↥D → B) (L : Finset B[X]) (m : Nat)
    (hlist : ∀ Q ∈ L, m ≤ (ExactListLine.polynomialAgreementSet
      (baseEval D) U Q).card)
    {P : F[X]} (hP : P ∈ mappedPolynomialList (F := F) L) :
    m ≤ (ExactListLine.polynomialAgreementSet
      (extensionEval (F := F) D) (extensionWord (F := F) U) P).card := by
  obtain ⟨Q, hQ, rfl⟩ := Finset.mem_image.mp hP
  rw [extensionAgreementSet_map_eq_base]
  exact hlist Q hQ

/-- Completeness descends every ambient explanation to the base field, so the
coefficientwise image of a complete base list is complete over the extension. -/
theorem mappedPolynomialList_complete
    (D : Finset B) (U : ↥D → B) (k m : Nat) (hkm : k + 1 ≤ m)
    (L : Finset B[X])
    (hcomplete : ∀ Q : B[X], Q.natDegree ≤ k →
      m ≤ (ExactListLine.polynomialAgreementSet (baseEval D) U Q).card →
        Q ∈ L)
    (P : F[X]) (hPdegree : P.natDegree ≤ k)
    (hPagree : m ≤ (ExactListLine.polynomialAgreementSet
      (extensionEval (F := F) D) (extensionWord (F := F) U) P).card) :
    P ∈ mappedPolynomialList (F := F) L := by
  obtain ⟨Q, hQdegree, hPmap, hsets⟩ :=
    exists_basePolynomial_of_many_agreements
      D U k m hkm P hPdegree hPagree
  apply Finset.mem_image.mpr
  refine ⟨Q, hcomplete Q hQdegree ?_, hPmap.symm⟩
  rw [← hsets]
  exact hPagree

/-- The mapped complete list has image exactly the ambient MCA-bad slope set
at every admissible extension-field pole. -/
theorem mappedPolynomialList_image_eval_eq_badSlopeSet
    [Fintype F] [DecidableEq F]
    (D : Finset B) (U : ↥D → B) (k m : Nat) (hkm : k + 1 ≤ m)
    (L : Finset B[X])
    (hdegree : ∀ Q ∈ L, Q.natDegree ≤ k)
    (hlist : ∀ Q ∈ L, m ≤ (ExactListLine.polynomialAgreementSet
      (baseEval D) U Q).card)
    (hcomplete : ∀ Q : B[X], Q.natDegree ≤ k →
      m ≤ (ExactListLine.polynomialAgreementSet (baseEval D) U Q).card →
        Q ∈ L)
    (alpha : F) (halpha : ∀ x : ↥D, extensionEval (F := F) D x ≠ alpha) :
    (mappedPolynomialList (F := F) L).image (fun P ↦ P.eval alpha) =
      ExactListLine.badSlopeSet
        (extensionEval (F := F) D) (extensionWord (F := F) U)
        alpha k m := by
  apply ExactListLine.image_eval_eq_badSlopeSet
    (extensionEval (F := F) D) (extensionEval_injective (F := F) D)
    (extensionWord (F := F) U) alpha halpha k m hkm
    (mappedPolynomialList (F := F) L)
  · intro P hP
    exact mappedPolynomialList_degree (F := F) L k hdegree hP
  · intro P hP
    exact mappedPolynomialList_agreements (F := F) D U L m hlist hP
  · intro P hPdegree hPagree
    exact mappedPolynomialList_complete
      D U k m hkm L hcomplete P hPdegree hPagree

/-- Under the literal equation-(4.6) budget measured using the base list size,
some extension-field pole separates the mapped list, whose evaluation image
is exactly the ambient MCA-bad slope set with the original base-list size. -/
theorem exists_extensionPole_exact_listLine
    [Fintype F] [DecidableEq F]
    (D : Finset B) (U : ↥D → B) (k m : Nat) (hkm : k + 1 ≤ m)
    (L : Finset B[X])
    (hdegree : ∀ Q ∈ L, Q.natDegree ≤ k)
    (hlist : ∀ Q ∈ L, m ≤ (ExactListLine.polynomialAgreementSet
      (baseEval D) U Q).card)
    (hcomplete : ∀ Q : B[X], Q.natDegree ≤ k →
      m ≤ (ExactListLine.polynomialAgreementSet (baseEval D) U Q).card →
        Q ∈ L)
    (hbudget : D.card + k * L.card.choose 2 < Fintype.card F) :
    ∃ alpha : F,
      (∀ x : ↥D, extensionEval (F := F) D x ≠ alpha) ∧
      Set.InjOn (fun P : F[X] ↦ P.eval alpha)
        (mappedPolynomialList (F := F) L : Set F[X]) ∧
      (mappedPolynomialList (F := F) L).image (fun P ↦ P.eval alpha) =
        ExactListLine.badSlopeSet
          (extensionEval (F := F) D) (extensionWord (F := F) U)
          alpha k m ∧
      (ExactListLine.badSlopeSet
        (extensionEval (F := F) D) (extensionWord (F := F) U)
        alpha k m).card = L.card := by
  let LF := mappedPolynomialList (F := F) L
  have hLFcard : LF.card = L.card := mappedPolynomialList_card (F := F) L
  have hdomainCard :
      (D.image (algebraMap B F)).card = D.card :=
    Finset.card_image_of_injective D (algebraMap B F).injective
  obtain ⟨alpha, halpha, hseparates⟩ :=
    SeparatingPole.exists_separating_pole
      (D.image (algebraMap B F)) k LF
      (fun P hP ↦ mappedPolynomialList_degree (F := F) L k hdegree hP)
      (by simpa [hdomainCard, hLFcard] using hbudget)
  have halphaEval : ∀ x : ↥D, extensionEval (F := F) D x ≠ alpha := by
    intro x hx
    apply halpha
    exact Finset.mem_image.mpr ⟨x.1, x.property, hx⟩
  refine ⟨alpha, halphaEval, hseparates, ?_, ?_⟩
  · exact mappedPolynomialList_image_eval_eq_badSlopeSet
      D U k m hkm L hdegree hlist hcomplete alpha halphaEval
  · calc
    (ExactListLine.badSlopeSet
      (extensionEval (F := F) D) (extensionWord (F := F) U)
      alpha k m).card = LF.card := by
        apply ExactListLine.badSlopeSet_card_eq
          (extensionEval (F := F) D) (extensionEval_injective (F := F) D)
          (extensionWord (F := F) U) alpha halphaEval k m hkm LF
          (fun P hP ↦ mappedPolynomialList_degree (F := F) L k hdegree hP)
          (fun P hP ↦ mappedPolynomialList_agreements
            (F := F) D U L m hlist hP)
          (fun P hPdegree hPagree ↦ mappedPolynomialList_complete
            D U k m hkm L hcomplete P hPdegree hPagree)
          hseparates
    _ = L.card := hLFcard

/-- Cardinality form of the scalar-extension exact list--line theorem. -/
theorem exists_extensionPole_badSlopeSet_card_eq_baseList
    [Fintype F] [DecidableEq F]
    (D : Finset B) (U : ↥D → B) (k m : Nat) (hkm : k + 1 ≤ m)
    (L : Finset B[X])
    (hdegree : ∀ Q ∈ L, Q.natDegree ≤ k)
    (hlist : ∀ Q ∈ L, m ≤ (ExactListLine.polynomialAgreementSet
      (baseEval D) U Q).card)
    (hcomplete : ∀ Q : B[X], Q.natDegree ≤ k →
      m ≤ (ExactListLine.polynomialAgreementSet (baseEval D) U Q).card →
        Q ∈ L)
    (hbudget : D.card + k * L.card.choose 2 < Fintype.card F) :
    ∃ alpha : F,
      (∀ x : ↥D, extensionEval (F := F) D x ≠ alpha) ∧
      (ExactListLine.badSlopeSet
        (extensionEval (F := F) D) (extensionWord (F := F) U)
        alpha k m).card = L.card := by
  obtain ⟨alpha, halpha, _hseparates, _himage, hcard⟩ :=
    exists_extensionPole_exact_listLine
      D U k m hkm L hdegree hlist hcomplete hbudget
  exact ⟨alpha, halpha, hcard⟩

theorem prefixListedPolynomials_card_eq_coefficientFiber
    (D : Finset B) {K m : Nat} (hKm : K ≤ m)
    (z : Fin (m - K) → B) :
    (PrefixPigeonhole.listedPolynomials D
      (PrefixPigeonhole.prefixPolynomial K m z) K m).card =
        (PrefixPigeonhole.coefficientFiber D K m z).card := by
  have hfiber :
      PrefixPigeonhole.coefficientFiber D K m z =
        PrefixPigeonhole.prefixSupportFinset D
          (PrefixPigeonhole.prefixPolynomial K m z) K m := by
    ext S
    exact PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset
      D hKm z S
  rw [hfiber, PrefixPigeonhole.listedPolynomials]
  apply Finset.card_image_of_injOn
  intro S _ T _ hST
  apply SP.locator_injective
  exact sub_right_injective hST

/-- Direct scalar-extension prefix-ray cardinality theorem: under equation
(4.6), an extension-field pole has exactly one bad slope per prefix support. -/
theorem exists_extensionPrefix_badSlopeSet_card_eq_coefficientFiber
    [Fintype F] [DecidableEq F]
    (D : Finset B) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → B)
    (hbudget : D.card + (K - 1) *
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m).card.choose 2 <
        Fintype.card F) :
    ∃ alpha : F,
      (∀ x : ↥D, extensionEval (F := F) D x ≠ alpha) ∧
      (ExactListLine.badSlopeSet
        (extensionEval (F := F) D)
        (extensionWord (F := F)
          (fun x : ↥D ↦
            (PrefixPigeonhole.prefixPolynomial K m z).eval x.1))
        alpha (K - 1) m).card =
          (PrefixPigeonhole.coefficientFiber D K m z).card := by
  let U := PrefixPigeonhole.prefixPolynomial K m z
  let L := PrefixPigeonhole.listedPolynomials D U K m
  have hU : U.IsMonicOfDegree m :=
    PrefixPigeonhole.prefixPolynomial_isMonicOfDegree K m hKm z
  obtain ⟨alpha, halpha, hcard⟩ :=
    exists_extensionPole_badSlopeSet_card_eq_baseList
      D (fun x : ↥D ↦ U.eval x.1) (K - 1) m (by omega) L
      (fun P hP ↦ ExactPrefixRay.listedPolynomial_natDegree_le_pred
        D U hU hKpos hKm hP)
      (fun P hP ↦ ExactPrefixRay.listedPolynomial_agreements
        D U hU hKpos hKm hP)
      (fun P hPdegree hPagree ↦
        ExactPrefixRay.mem_listedPolynomials_of_degree_agreements
          D U hU hKpos hKm P hPdegree hPagree)
      hbudget
  refine ⟨alpha, halpha, hcard.trans ?_⟩
  exact prefixListedPolynomials_card_eq_coefficientFiber D hKm z

#print axioms exists_basePolynomial_of_many_agreements
#print axioms mappedPolynomialList_complete
#print axioms mappedPolynomialList_image_eval_eq_badSlopeSet
#print axioms exists_extensionPole_exact_listLine
#print axioms exists_extensionPole_badSlopeSet_card_eq_baseList
#print axioms exists_extensionPrefix_badSlopeSet_card_eq_coefficientFiber

end GrandeFinale.ScalarExtensionListLine
