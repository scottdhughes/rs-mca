import GrandeFinale.PrefixPigeonhole

/-!
# Exact separating-pole list--line interface

This module formalizes the finite-field core of
`thm:exact-list-line-bijection` in
`experimental/asymptotic_rs_mca_frontiers.tex`: at a pole that separates a
complete polynomial list, evaluation identifies that list exactly with the
MCA-bad slopes of the simple-pole received line. It also proves equality of
the original and line agreement supports.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.ExactListLine

variable {F D : Type*} [Field F]

/-- Agreement positions of a polynomial with a received word. -/
def polynomialAgreementSet [Fintype D] [DecidableEq D]
    (ev : D → F) (U : D → F) (P : F[X]) : Finset D :=
  Finset.univ.filter fun x ↦ U x = P.eval (ev x)

theorem mem_polynomialAgreementSet
    [Fintype D] [DecidableEq D]
    (ev : D → F) (U : D → F) (P : F[X]) (x : D) :
    x ∈ polynomialAgreementSet ev U P ↔ U x = P.eval (ev x) := by
  simp [polynomialAgreementSet]

/-- The quotient `(P(X) - P(alpha))/(X - alpha)` used to explain the
corresponding point of the pole line. -/
def explainingPolynomial (alpha : F) (P : F[X]) : F[X] :=
  Classical.choose (X_sub_C_dvd_sub_C_eval (a := alpha) (p := P))

theorem explainingPolynomial_spec (alpha : F) (P : F[X]) :
    P - C (P.eval alpha) =
      (X - C alpha) * explainingPolynomial alpha P :=
  Classical.choose_spec (X_sub_C_dvd_sub_C_eval (a := alpha) (p := P))

/-- The quotient polynomial lies in the dimension-`k` RS code whenever
`P` has degree at most `k`. -/
theorem explainingPolynomial_degree_lt
    (alpha : F) (P : F[X]) {k : Nat} (hPdeg : P.natDegree ≤ k) :
    (explainingPolynomial alpha P).degree < (k : WithBot Nat) := by
  let Q := explainingPolynomial alpha P
  have hfactor : P - C (P.eval alpha) = (X - C alpha) * Q :=
    explainingPolynomial_spec alpha P
  by_cases hQzero : Q = 0
  · change Q.degree < (k : WithBot Nat)
    simp [hQzero]
  · rw [← natDegree_lt_iff_degree_lt hQzero]
    have hnum : (P - C (P.eval alpha)).natDegree ≤ k :=
      (natDegree_sub_le _ _).trans (by simp [hPdeg])
    have heq :
        (X - C alpha).natDegree + Q.natDegree =
          (P - C (P.eval alpha)).natDegree := by
      rw [hfactor, natDegree_mul (X_sub_C_ne_zero alpha) hQzero]
    rw [natDegree_X_sub_C] at heq
    omega

/-- Pointwise equality with the quotient explanation is equivalent to the
original polynomial agreement. -/
theorem explainingPolynomial_agrees_iff
    (ev : D → F) (U : D → F) (alpha : F)
    (halpha : ∀ x, ev x ≠ alpha) (P : F[X]) (x : D) :
    (explainingPolynomial alpha P).eval (ev x) =
        CollisionAwarePole.fpole ev U alpha x +
          P.eval alpha * CollisionAwarePole.gpole ev alpha x ↔
      U x = P.eval (ev x) := by
  let Q := explainingPolynomial alpha P
  have hfactorEval :
      P.eval (ev x) - P.eval alpha =
        (ev x - alpha) * Q.eval (ev x) := by
    have h := congrArg (Polynomial.eval (ev x))
      (explainingPolynomial_spec alpha P)
    simpa [Q, eval_sub, eval_mul, eval_C, eval_X] using h
  have hne : ev x - alpha ≠ 0 := sub_ne_zero.mpr (halpha x)
  have hQ :
      Q.eval (ev x) =
        (P.eval (ev x) - P.eval alpha) * (ev x - alpha)⁻¹ := by
    apply mul_right_cancel₀ hne
    calc
      Q.eval (ev x) * (ev x - alpha) =
          (ev x - alpha) * Q.eval (ev x) := mul_comm _ _
      _ = P.eval (ev x) - P.eval alpha := hfactorEval.symm
      _ = ((P.eval (ev x) - P.eval alpha) * (ev x - alpha)⁻¹) *
          (ev x - alpha) := by field_simp
  have hline :
      CollisionAwarePole.fpole ev U alpha x +
          P.eval alpha * CollisionAwarePole.gpole ev alpha x =
        (U x - P.eval alpha) * (ev x - alpha)⁻¹ := by
    simp [CollisionAwarePole.fpole, CollisionAwarePole.gpole]
    ring
  change Q.eval (ev x) = _ ↔ _
  rw [hQ, hline]
  constructor
  · intro h
    have hcancel := mul_right_cancel₀ (inv_ne_zero hne) h
    exact (sub_left_injective hcancel).symm
  · intro h
    apply congrArg (fun y ↦ (y - P.eval alpha) * (ev x - alpha)⁻¹)
    exact h.symm

/-- The agreement set of a listed polynomial is preserved exactly on its
corresponding point of the pole line. -/
theorem lineAgreementSet_eq_polynomialAgreementSet
    [Fintype D] [DecidableEq D]
    (ev : D → F) (U : D → F) (alpha : F)
    (halpha : ∀ x, ev x ≠ alpha) (P : F[X]) :
    (Finset.univ.filter fun x ↦
      (explainingPolynomial alpha P).eval (ev x) =
        CollisionAwarePole.fpole ev U alpha x +
          P.eval alpha * CollisionAwarePole.gpole ev alpha x) =
      polynomialAgreementSet ev U P := by
  ext x
  simp only [Finset.mem_filter, Finset.mem_univ, true_and,
    polynomialAgreementSet]
  exact explainingPolynomial_agrees_iff ev U alpha halpha P x

/-- MCA-bad slopes of the simple-pole line. -/
def badSlopeSet [Fintype F] [DecidableEq F]
    (ev : D → F) (U : D → F) (alpha : F) (k m : Nat) : Finset F :=
  Finset.univ.filter fun gamma ↦
    GrandeFinale.MCABad
      (CollisionAwarePole.rsEval ev k : Set (D → F))
      (CollisionAwarePole.fpole ev U alpha)
      (CollisionAwarePole.gpole ev alpha) m gamma

/-- A complete finite polynomial list maps onto exactly the MCA-bad slope set
at any admissible pole. -/
theorem image_eval_eq_badSlopeSet
    [Fintype D] [DecidableEq D] [Fintype F] [DecidableEq F]
    (ev : D → F) (hev : Function.Injective ev)
    (U : D → F) (alpha : F) (halpha : ∀ x, ev x ≠ alpha)
    (k m : Nat) (hkm : k + 1 ≤ m) (L : Finset F[X])
    (hdeg : ∀ P ∈ L, P.natDegree ≤ k)
    (hlist : ∀ P ∈ L, m ≤ (polynomialAgreementSet ev U P).card)
    (hcomplete : ∀ P : F[X], P.natDegree ≤ k →
      m ≤ (polynomialAgreementSet ev U P).card → P ∈ L) :
    L.image (fun P ↦ P.eval alpha) =
      badSlopeSet ev U alpha k m := by
  ext gamma
  constructor
  · intro hgamma
    obtain ⟨P, hP, rfl⟩ := Finset.mem_image.mp hgamma
    apply Finset.mem_filter.mpr
    refine ⟨Finset.mem_univ _, ?_⟩
    apply CollisionAwarePole.eval_slope_mcaBad ev hev k m hkm U P
      (hdeg P hP) alpha halpha (polynomialAgreementSet ev U P)
      (hlist P hP)
    intro x hx
    exact (mem_polynomialAgreementSet ev U P x).mp hx
  · intro hgamma
    have hbad := (Finset.mem_filter.mp hgamma).2
    obtain ⟨S, hmS, ⟨c, hc, hcS⟩, _hnotPair⟩ := hbad
    obtain ⟨G, hGdegree, hGval⟩ := CollisionAwarePole.mem_rsEval.mp hc
    let P : F[X] := (X - C alpha) * G + C gamma
    have hPdeg : P.natDegree ≤ k := by
      have hprod : ((X - C alpha) * G).natDegree ≤ k := by
        by_cases hGzero : G = 0
        · simp [hGzero]
        · have hGnat : G.natDegree < k :=
            (natDegree_lt_iff_degree_lt hGzero).mpr hGdegree
          rw [natDegree_mul (X_sub_C_ne_zero alpha) hGzero,
            natDegree_X_sub_C]
          omega
      exact (natDegree_add_le _ _).trans (by simp [hprod])
    have hSsub : S ⊆ polynomialAgreementSet ev U P := by
      intro x hx
      apply (mem_polynomialAgreementSet ev U P x).mpr
      have hline :
          G.eval (ev x) =
            CollisionAwarePole.fpole ev U alpha x +
              gamma * CollisionAwarePole.gpole ev alpha x :=
        (hGval x).symm.trans (hcS x hx)
      have hne : ev x - alpha ≠ 0 := sub_ne_zero.mpr (halpha x)
      dsimp [P]
      simp only [eval_add, eval_mul, eval_sub, eval_X, eval_C]
      dsimp [CollisionAwarePole.fpole, CollisionAwarePole.gpole] at hline
      field_simp [hne] at hline
      calc
        U x = (U x + -gamma) + gamma := by ring
        _ = G.eval (ev x) * (ev x - alpha) + gamma := by rw [← hline]
        _ = (ev x - alpha) * G.eval (ev x) + gamma := by ring
    have hPagree : m ≤ (polynomialAgreementSet ev U P).card :=
      hmS.trans (Finset.card_le_card hSsub)
    have hPL : P ∈ L := hcomplete P hPdeg hPagree
    apply Finset.mem_image.mpr
    refine ⟨P, hPL, ?_⟩
    simp [P]

/-- At a separating pole, evaluation is a bijection in cardinal form: the
complete polynomial list and the MCA-bad slope set have equal size. -/
theorem badSlopeSet_card_eq
    [Fintype D] [DecidableEq D] [Fintype F] [DecidableEq F]
    (ev : D → F) (hev : Function.Injective ev)
    (U : D → F) (alpha : F) (halpha : ∀ x, ev x ≠ alpha)
    (k m : Nat) (hkm : k + 1 ≤ m) (L : Finset F[X])
    (hdeg : ∀ P ∈ L, P.natDegree ≤ k)
    (hlist : ∀ P ∈ L, m ≤ (polynomialAgreementSet ev U P).card)
    (hcomplete : ∀ P : F[X], P.natDegree ≤ k →
      m ≤ (polynomialAgreementSet ev U P).card → P ∈ L)
    (hseparates : Set.InjOn (fun P : F[X] ↦ P.eval alpha) L) :
    (badSlopeSet ev U alpha k m).card = L.card := by
  rw [← image_eval_eq_badSlopeSet ev hev U alpha halpha k m hkm L
    hdeg hlist hcomplete]
  exact Finset.card_image_of_injOn hseparates

#print axioms explainingPolynomial_degree_lt
#print axioms explainingPolynomial_agrees_iff
#print axioms lineAgreementSet_eq_polynomialAgreementSet
#print axioms image_eval_eq_badSlopeSet
#print axioms badSlopeSet_card_eq

end GrandeFinale.ExactListLine
