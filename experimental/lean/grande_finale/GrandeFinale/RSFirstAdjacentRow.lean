import GrandeFinale.ExactAdjacentRow
import GrandeFinale.RSExactSupportUpper
import GrandeFinale.RSSupportHyperplanes

/-!
# Exact first adjacent Reed--Solomon row

This module composes the weighted Vandermonde parity kernel, the distinct
`(R-1)`-support syndrome hyperplanes, the literal finite-field separating-line
construction, and the exact support-atlas upper bound. The result is the
full-field numerator equality (AD1) in
`thm:exact-first-adjacent-row`.
-/

open scoped Classical

noncomputable section

namespace GrandeFinale.RSFirstAdjacentRow

open GrandeFinale.ExactAdjacentRow
open GrandeFinale.CollisionAwarePole
open GrandeFinale.RSExactSupportUpper
open GrandeFinale.RSParityKernel
open GrandeFinale.RSSupportHyperplanes
open GrandeFinale.SyndromeLine

variable {D F : Type*} [Field F] [Fintype D] [DecidableEq D]

/-- Exact `a`-element supports, indexed by the finite powerset of the
evaluation domain. -/
abbrev exactSupportIndex (a : Nat) : Type _ :=
  ↥((Finset.univ : Finset D).powersetCard a)

omit [DecidableEq D] in
/-- The exact-support index has literal binomial cardinality. -/
@[simp] theorem card_exactSupportIndex (a : Nat) :
    Fintype.card (exactSupportIndex (D := D) a) =
      Nat.choose (Fintype.card D) a := by
  simp [exactSupportIndex]

/-- The exact `(R-1)` support hyperplanes, reindexed by the finite powerset
whose cardinality is definitionally exposed to the AD1 compiler. -/
theorem exists_exactSupportHyperplanes
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (hR : 0 < R) :
    ∃ ell : exactSupportIndex (D := D) (R - 1) →
        (Fin R → F) →ₗ[F] F,
      (∀ E, ell E ≠ 0) ∧
      Function.Injective (fun E ↦ LinearMap.ker (ell E)) ∧
      (∀ E, syndromeSpan (parityCheck ev R) (E.1 : Set D) =
        LinearMap.ker (ell E)) := by
  obtain ⟨ell₀, hell₀, hker₀, hspan₀⟩ :=
    exists_distinct_supportHyperplanes ev hev R hR
  let toCardSubtype :
      exactSupportIndex (D := D) (R - 1) →
        {E : Finset D // E.card = R - 1} :=
    fun E ↦ ⟨E.1, (Finset.mem_powersetCard.mp E.2).2⟩
  refine ⟨fun E ↦ ell₀ (toCardSubtype E), ?_, ?_, ?_⟩
  · intro E
    exact hell₀ (toCardSubtype E)
  · intro E E' hker
    have hindex : toCardSubtype E = toCardSubtype E' := hker₀ hker
    apply Subtype.ext
    simpa [toCardSubtype] using congrArg Subtype.val hindex
  · intro E
    exact hspan₀ (toCardSubtype E)

section FiniteField

variable [Fintype F] [DecidableEq F]

/-- AD1 in redundancy coordinates: at agreement `k+1`, the full-field MCA
numerator is exactly the number of `(R-1)`-element supports. -/
theorem B_MCA_rsEval_eq_choose_redundancy_pred
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hR : 0 < R)
    (hsize : k + R = Fintype.card D)
    (hgate :
      max (Nat.choose (Fintype.card D) (R - 1))
          ((Nat.choose (Fintype.card D) (R - 1)).choose 2) <
        Fintype.card F) :
    GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) (k + 1) =
      Nat.choose (Fintype.card D) (R - 1) := by
  let ι := exactSupportIndex (D := D) (R - 1)
  letI : LinearOrder ι := WellOrderingRel.isWellOrder.linearOrder
  obtain ⟨ell, hell, hker, hspan⟩ :=
    exists_exactSupportHyperplanes ev hev R hR
  have hRle : R ≤ Fintype.card D := by omega
  have ha : k + 1 ≤ Fintype.card D := by omega
  have herrors :
      ∀ E : ι, E.1.card ≤ Fintype.card D - (k + 1) := by
    intro E
    have hEcard : E.1.card = R - 1 :=
      (Finset.mem_powersetCard.mp E.2).2
    omega
  have hιcard :
      Fintype.card ι = Nat.choose (Fintype.card D) (R - 1) := by
    simp [ι]
  have hcard : Fintype.card ι < Fintype.card F := by
    rw [hιcard]
    exact (Nat.le_max_left _ _).trans_lt hgate
  have hpairs : (Fintype.card ι).choose 2 < Fintype.card F := by
    rw [hιcard]
    exact (Nat.le_max_right _ _).trans_lt hgate
  have hparityKer := ker_parityCheck_eq_rsEval ev hev k R hsize
  have hchoose :
      Nat.choose (Fintype.card D) (k + 1) =
        Nat.choose (Fintype.card D) (R - 1) := by
    apply Nat.choose_symm_of_eq_add
    omega
  have hupper :
      GrandeFinale.B_MCA
          ((parityCheck ev R).ker : Set (D → F)) (k + 1) ≤
        Fintype.card ι := by
    rw [hparityKer, hιcard]
    simpa [hchoose] using
      B_MCA_rsEval_le_choose ev hev k R hsize (k + 1) (by omega)
  have heq := B_MCA_eq_of_separatingHyperplanes
    (ι := ι) (H := parityCheck ev R)
    (parityCheck_surjective ev hev R hRle)
    (k + 1) ha (fun E : ι ↦ E.1) herrors
    ell hell hker hspan hcard hpairs hupper
  rw [hparityKer, hιcard] at heq
  exact heq

/-- AD1 in the paper's agreement coordinates:
`B_MCA (RS(D,k)) (k+1) = choose |D| (k+1)`. -/
theorem B_MCA_rsEval_eq_choose_succ
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hR : 0 < R)
    (hsize : k + R = Fintype.card D)
    (hgate :
      max (Nat.choose (Fintype.card D) (R - 1))
          ((Nat.choose (Fintype.card D) (R - 1)).choose 2) <
        Fintype.card F) :
    GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) (k + 1) =
      Nat.choose (Fintype.card D) (k + 1) := by
  rw [B_MCA_rsEval_eq_choose_redundancy_pred
    ev hev k R hR hsize hgate]
  apply Nat.choose_symm_of_eq_add
  omega

end FiniteField

#print axioms exists_exactSupportHyperplanes
#print axioms B_MCA_rsEval_eq_choose_redundancy_pred
#print axioms B_MCA_rsEval_eq_choose_succ

end GrandeFinale.RSFirstAdjacentRow
