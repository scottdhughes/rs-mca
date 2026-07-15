import GrandeFinale.ScalarExtensionListLine

/-!
# Prefix-fiber floors for proper challenge sets

This module composes the scalar-extension exact list--line interface with the
finite translate-intersection compiler.  A prescribed coefficient fiber gives
an exact full-field MCA floor, and every proper challenge set retains the
literal ceiling fraction of that floor.  Choosing a largest coefficient fiber
then supplies the explicit nested-ceiling prefix bound.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.PrefixChallengeFloor

variable {B F : Type*} [Field B] [Field F] [Algebra B F]

/-- The bad slopes on any explicit simple-pole line are bounded by the full
MCA numerator of the corresponding Reed--Solomon evaluation code. -/
theorem badSlopeSet_card_le_B_MCA
    {D : Type*} [Fintype D]
    [Fintype F] [DecidableEq F]
    (ev : D → F) (U : D → F) (alpha : F) (k m : Nat) :
    (ExactListLine.badSlopeSet ev U alpha k m).card ≤
      GrandeFinale.B_MCA
        (CollisionAwarePole.rsEval ev k : Set (D → F)) m := by
  change
    (Finset.univ.filter fun gamma : F ↦
      GrandeFinale.MCABad
        (CollisionAwarePole.rsEval ev k : Set (D → F))
        (CollisionAwarePole.fpole ev U alpha)
        (CollisionAwarePole.gpole ev alpha) m gamma).card ≤
    Finset.univ.sup (fun p : (D → F) × (D → F) ↦
      (Finset.univ.filter fun gamma : F ↦
        GrandeFinale.MCABad
          (CollisionAwarePole.rsEval ev k : Set (D → F))
          p.1 p.2 m gamma).card)
  exact Finset.le_sup
    (f := fun p : (D → F) × (D → F) ↦
      (Finset.univ.filter fun gamma : F ↦
        GrandeFinale.MCABad
          (CollisionAwarePole.rsEval ev k : Set (D → F))
          p.1 p.2 m gamma).card)
    (Finset.mem_univ
      (CollisionAwarePole.fpole ev U alpha,
        CollisionAwarePole.gpole ev alpha))

set_option maxHeartbeats 800000 in
/-- A prescribed coefficient fiber gives its exact ceiling-density floor for
every finite extension-field challenge set. -/
theorem extensionPrefix_challenge_floor
    [Fintype F] [DecidableEq F]
    (D : Finset B) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (z : Fin (m - K) → B)
    (hbudget : D.card + (K - 1) *
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m).card.choose 2 <
        Fintype.card F)
    (Gamma : Finset F) :
    (Gamma.card *
        (PrefixPigeonhole.coefficientFiber D K m z).card) ⌈/⌉
        Fintype.card F ≤
      ChallengeIntersection.B_MCA_challenge
        (CollisionAwarePole.rsEval
          (ScalarExtensionListLine.extensionEval (F := F) D) (K - 1) :
            Set (↑D → F))
        m Gamma := by
  letI : DecidableEq ↑D := Classical.decEq ↑D
  obtain ⟨alpha, _halpha, hcard⟩ :=
    ScalarExtensionListLine.exists_extensionPrefix_badSlopeSet_card_eq_coefficientFiber
        (F := F) D hKpos hKm z hbudget
  have hfull :
      (PrefixPigeonhole.coefficientFiber D K m z).card ≤
        GrandeFinale.B_MCA
          (CollisionAwarePole.rsEval
            (ScalarExtensionListLine.extensionEval (F := F) D) (K - 1) :
              Set (↑D → F))
          m := by
    rw [← hcard]
    exact badSlopeSet_card_le_B_MCA
      (ScalarExtensionListLine.extensionEval (F := F) D)
      (ScalarExtensionListLine.extensionWord (F := F)
        (fun x : ↑D ↦
          (PrefixPigeonhole.prefixPolynomial K m z).eval x.1))
      alpha (K - 1) m
  exact ChallengeIntersection.challenge_floor_of_full_floor
    (C := CollisionAwarePole.rsEval
      (ScalarExtensionListLine.extensionEval (F := F) D) (K - 1))
    (a := m)
    (M := (PrefixPigeonhole.coefficientFiber D K m z).card)
    (Gamma := Gamma) hfull

/-- Choosing a largest coefficient fiber gives the literal nested-ceiling
proper-challenge floor under a uniform equation-(4.6) field-size budget. -/
theorem heavy_extensionPrefix_challenge_floor
    [Fintype B] [Fintype F] [DecidableEq F]
    (D : Finset B) {K m : Nat} (hKpos : 0 < K) (hKm : K ≤ m)
    (hbudget :
      D.card + (K - 1) * (D.card.choose m).choose 2 < Fintype.card F)
    (Gamma : Finset F) :
    (Gamma.card *
        (D.card.choose m ⌈/⌉ (Fintype.card B) ^ (m - K))) ⌈/⌉
        Fintype.card F ≤
      ChallengeIntersection.B_MCA_challenge
        (CollisionAwarePole.rsEval
          (ScalarExtensionListLine.extensionEval (F := F) D) (K - 1) :
            Set (↑D → F))
        m Gamma := by
  obtain ⟨z, hz⟩ :=
    PrefixPigeonhole.exists_large_coefficientFiber D K m
  have hFiberLe :
      (PrefixPigeonhole.coefficientFiber D K m z).card ≤
        D.card.choose m := by
    calc
      (PrefixPigeonhole.coefficientFiber D K m z).card ≤
          (D.powersetCard m).card :=
        Finset.card_le_card (Finset.filter_subset _ _)
      _ = D.card.choose m := by simp [Finset.card_powersetCard]
  have hListLe :
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m).card ≤
        D.card.choose m := by
    rw [ScalarExtensionListLine.prefixListedPolynomials_card_eq_coefficientFiber
      D hKm z]
    exact hFiberLe
  have hchoose :
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m).card.choose 2 ≤
        (D.card.choose m).choose 2 :=
    Nat.choose_le_choose 2 hListLe
  have hzbudget : D.card + (K - 1) *
      (PrefixPigeonhole.listedPolynomials D
        (PrefixPigeonhole.prefixPolynomial K m z) K m).card.choose 2 <
        Fintype.card F := by
    exact (Nat.add_le_add_left
      (Nat.mul_le_mul_left (K - 1) hchoose) D.card).trans_lt hbudget
  have hzchallenge := extensionPrefix_challenge_floor
    (F := F) D hKpos hKm z hzbudget Gamma
  have hcardF : 0 < Fintype.card F := Fintype.card_pos
  exact ((gc_mul_ceilDiv hcardF).monotone_l
    (Nat.mul_le_mul_left Gamma.card hz)).trans hzchallenge

#print axioms badSlopeSet_card_le_B_MCA
#print axioms extensionPrefix_challenge_floor
#print axioms heavy_extensionPrefix_challenge_floor

end GrandeFinale.PrefixChallengeFloor
