import GrandeFinale.PrefixRigidityPacking
import GrandeFinale.ScalarExtensionListLine

/-!
# Identity-prefix collision-aware MCA floor

This module exports the direct finite composition in
`cor:identity-prefix-floor` of
`experimental/asymptotic_rs_mca_frontiers.tex`.  It selects a prefix list of
exactly the pigeonhole-ceiling size and applies the collision-aware simple-pole
conversion, yielding equations (4.2)--(4.3) without a monotonicity assumption
on the displayed rational expression.  It also records the immediate exact
proper-challenge ceiling transfer.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.IdentityPrefixCollisionFloor

variable {F : Type*} [Field F]

/-- The literal identity-prefix list floor `L_m` from equation (4.3). -/
def identityPrefixListFloor [Fintype F]
    (D : Finset F) (k m : Nat) : Nat :=
  D.card.choose m ⌈/⌉ (Fintype.card F) ^ (m - k - 1)

/-- The collision-aware distinct-slope floor `M(L)` from equation (4.2). -/
def collisionAwareFloor (q n k L : Nat) : Nat :=
  L * (q - n) ⌈/⌉ ((q - n) + k * (L - 1))

private theorem B_MCA_decidableEq_irrel
    [Fintype F] [DecidableEq F] {D : Type*} [Fintype D]
    (d₁ d₂ : DecidableEq D) (C : Set (D → F)) (a : Nat) :
    @GrandeFinale.B_MCA F D _ _ _ d₁ C a =
      @GrandeFinale.B_MCA F D _ _ _ d₂ C a := by
  have h : d₁ = d₂ := Subsingleton.elim _ _
  subst d₂
  rfl

set_option maxHeartbeats 800000 in
/-- Exact identity-prefix MCA floor (4.3).  An exact `L_m`-element sublist is
selected from the heavy prefix fiber before invoking the collision-aware pole
theorem. -/
theorem identityPrefix_collisionAware_floor
    [Fintype F] [DecidableEq F]
    (D : Finset F) {k m : Nat} (hkm : k + 1 ≤ m)
    (hmD : m ≤ D.card) (hqn : D.card < Fintype.card F) :
    collisionAwareFloor (Fintype.card F) D.card k
        (identityPrefixListFloor D k m) ≤
      GrandeFinale.B_MCA
        (CollisionAwarePole.rsEval (ExactPrefixRay.domainEval D) k :
          Set (↑D → F))
        m := by
  let Lm := identityPrefixListFloor D k m
  obtain ⟨z, hz0⟩ :=
    PrefixPigeonhole.exists_large_coefficientFiber D (k + 1) m
  have hdepth : m - k - 1 = m - (k + 1) := by omega
  have hz :
      Lm ≤ (PrefixPigeonhole.coefficientFiber D (k + 1) m z).card := by
    simpa [Lm, identityPrefixListFloor, hdepth] using hz0
  let U := PrefixPigeonhole.prefixPolynomial (k + 1) m z
  let P := PrefixPigeonhole.listedPolynomials D U (k + 1) m
  have hU : U.IsMonicOfDegree m := by
    exact PrefixPigeonhole.prefixPolynomial_isMonicOfDegree
      (k + 1) m hkm z
  have hPcard :
      P.card =
        (PrefixPigeonhole.coefficientFiber D (k + 1) m z).card := by
    simpa [P, U] using
      (ScalarExtensionListLine.prefixListedPolynomials_card_eq_coefficientFiber
        D hkm z)
  rw [← hPcard] at hz
  obtain ⟨L, hLP, hLcard⟩ := Finset.exists_subset_card_eq hz
  have hden : 0 < (Fintype.card F) ^ (m - k - 1) := by positivity
  have hcover :
      D.card.choose m ≤
        (Fintype.card F) ^ (m - k - 1) * Lm := by
    apply (ceilDiv_le_iff_le_mul hden).mp
    simp [Lm, identityPrefixListFloor]
  have hLmpos : 0 < Lm := by
    have hnum : 0 < D.card.choose m := Nat.choose_pos hmD
    by_contra hnot
    have hzero : Lm = 0 := Nat.eq_zero_of_not_pos hnot
    rw [hzero, Nat.mul_zero] at hcover
    omega
  have hL : L.Nonempty := by
    rw [← Finset.card_pos, hLcard]
    exact hLmpos
  have hdegree : ∀ Q ∈ L, Q.natDegree ≤ k := by
    intro Q hQ
    have hQP :
        Q ∈ PrefixPigeonhole.listedPolynomials D U (k + 1) m := by
      simpa [P] using hLP hQ
    simpa using ExactPrefixRay.listedPolynomial_natDegree_le_pred
      D U hU (by omega) hkm hQP
  have hagree : ∀ Q ∈ L, ∃ S : Finset ↑D,
      m ≤ S.card ∧ ∀ x ∈ S,
        ExactPrefixRay.polynomialWord D U x =
          Q.eval (ExactPrefixRay.domainEval D x) := by
    intro Q hQ
    have hQP :
        Q ∈ PrefixPigeonhole.listedPolynomials D U (k + 1) m := by
      simpa [P] using hLP hQ
    let S := ExactListLine.polynomialAgreementSet
      (ExactPrefixRay.domainEval D) (ExactPrefixRay.polynomialWord D U) Q
    refine ⟨S, ?_, ?_⟩
    · simpa [S] using ExactPrefixRay.listedPolynomial_agreements
        D U hU (by omega) hkm hQP
    · intro x hx
      apply (ExactListLine.mem_polynomialAgreementSet
        (ExactPrefixRay.domainEval D) (ExactPrefixRay.polynomialWord D U)
        Q x).mp
      simpa [S] using hx
  have hdomain : Fintype.card ↑D < Fintype.card F := by
    simpa using hqn
  have hbound := CollisionAwarePole.collisionAwarePole_le_B_MCA
    (F := F) (D := ↑D)
    (ExactPrefixRay.domainEval D) Subtype.val_injective
    k m hkm (ExactPrefixRay.polynomialWord D U)
    L hL hdegree hagree hdomain
  rw [hLcard] at hbound
  simpa [collisionAwareFloor, Lm] using hbound

set_option maxHeartbeats 800000 in
/-- The identity-prefix collision-aware floor after restriction to any finite
challenge set. -/
theorem identityPrefix_collisionAware_challenge_floor
    [Fintype F] [DecidableEq F]
    (D : Finset F) {k m : Nat} (hkm : k + 1 ≤ m)
    (hmD : m ≤ D.card) (hqn : D.card < Fintype.card F)
    (Gamma : Finset F) :
    (Gamma.card *
        collisionAwareFloor (Fintype.card F) D.card k
          (identityPrefixListFloor D k m)) ⌈/⌉
        Fintype.card F ≤
      ChallengeIntersection.B_MCA_challenge
        (CollisionAwarePole.rsEval (ExactPrefixRay.domainEval D) k :
          Set (↑D → F))
        m Gamma := by
  let concrete : DecidableEq ↑D := inferInstance
  letI : DecidableEq ↑D := concrete
  have hfull0 := identityPrefix_collisionAware_floor D hkm hmD hqn
  letI : DecidableEq ↑D := Classical.decEq ↑D
  have hfull :
      collisionAwareFloor (Fintype.card F) D.card k
          (identityPrefixListFloor D k m) ≤
        GrandeFinale.B_MCA
          (CollisionAwarePole.rsEval (ExactPrefixRay.domainEval D) k :
            Set (↑D → F))
          m := by
    exact hfull0.trans_eq (B_MCA_decidableEq_irrel
      concrete (inferInstance : DecidableEq ↑D)
      (CollisionAwarePole.rsEval (ExactPrefixRay.domainEval D) k :
        Set (↑D → F)) m)
  exact ChallengeIntersection.challenge_floor_of_full_floor
    (C := CollisionAwarePole.rsEval (ExactPrefixRay.domainEval D) k)
    (a := m)
    (M := collisionAwareFloor (Fintype.card F) D.card k
      (identityPrefixListFloor D k m))
    (Gamma := Gamma) hfull

#print axioms identityPrefix_collisionAware_floor
#print axioms identityPrefix_collisionAware_challenge_floor

end GrandeFinale.IdentityPrefixCollisionFloor
