import GrandeFinale.RSParityKernel
import GrandeFinale.SyndromeLine

/-!
# Exact agreement reduction for Reed--Solomon MCA

This module formalizes the exact-agreement reduction behind the literal
support-atlas upper bound. An MCA witness on a support of size at least `a`
can be replaced, when `a >= k+1`, by a witness on an exact `a`-element
support.
-/

open Polynomial
open scoped Classical

noncomputable section

namespace GrandeFinale.RSExactSupportUpper

open GrandeFinale.CollisionAwarePole
open GrandeFinale.RSParityKernel
open GrandeFinale.SyndromeLine

variable {D F : Type*} [Field F] [Fintype D] [DecidableEq D]

omit [Fintype D] in
/-- Arbitrary values on `k` distinct evaluation points are explained by a
degree-`< k` Reed--Solomon word. -/
theorem exists_rsEval_explanation_on_card_eq
    (ev : D → F) (hev : Function.Injective ev)
    (k : Nat) (K : Finset D) (hK : K.card = k) (u : D → F) :
    GrandeFinale.Explained (rsEval ev k : Set (D → F)) u K := by
  let P : F[X] := Lagrange.interpolate K ev u
  have hPdeg : P.degree < (k : WithBot Nat) := by
    have hdeg := Lagrange.degree_interpolate_lt
      (s := K) (v := ev) (r := u) hev.injOn
    simpa [P, hK] using hdeg
  refine ⟨fun d ↦ P.eval (ev d), ?_, ?_⟩
  · exact (mem_rsEval).mpr ⟨P, hPdeg, fun _ ↦ rfl⟩
  · intro d hd
    exact Lagrange.eval_interpolate_at_node
      (s := K) (v := ev) (r := u) hev.injOn hd

omit [Fintype D] [DecidableEq D] in
/-- Two Reed--Solomon words agreeing on at least `k` evaluation points are
equal. -/
theorem rsEval_eq_of_agree_on_card_ge
    (ev : D → F) (hev : Function.Injective ev)
    (k : Nat) (K : Finset D) (hK : k ≤ K.card)
    {c c' : D → F} (hc : c ∈ rsEval ev k) (hc' : c' ∈ rsEval ev k)
    (hagree : ∀ d ∈ K, c d = c' d) :
    c = c' := by
  obtain ⟨P, hP, hcP⟩ := (mem_rsEval).mp hc
  obtain ⟨Q, hQ, hcQ⟩ := (mem_rsEval).mp hc'
  have hPQ : P = Q := by
    apply Polynomial.eq_of_degrees_lt_of_eval_index_eq
      (s := K) hev.injOn
    · exact hP.trans_le (WithBot.coe_le_coe.mpr hK)
    · exact hQ.trans_le (WithBot.coe_le_coe.mpr hK)
    · intro d hd
      calc
        P.eval (ev d) = c d := (hcP d).symm
        _ = c' d := hagree d hd
        _ = Q.eval (ev d) := hcQ d
  funext d
  rw [hcP d, hcQ d, hPQ]

omit [Fintype D] in
/-- If one received word is unexplained on `S`, then it remains unexplained on
some exact `a`-element sub-support whenever `k+1 <= a <= |S|`. -/
theorem exists_exact_support_preserving_not_explained
    (ev : D → F) (hev : Function.Injective ev)
    (k a : Nat) (hka : k + 1 ≤ a)
    (S : Finset D) (hSa : a ≤ S.card) (u : D → F)
    (hu : ¬ GrandeFinale.Explained (rsEval ev k : Set (D → F)) u S) :
    ∃ T : Finset D, T ⊆ S ∧ T.card = a ∧
      ¬ GrandeFinale.Explained (rsEval ev k : Set (D → F)) u T := by
  obtain ⟨K, hKS, hKcard⟩ :=
    Finset.exists_subset_card_eq (s := S) (n := k) (by omega)
  obtain ⟨c, hc, hcK⟩ :=
    exists_rsEval_explanation_on_card_eq ev hev k K hKcard u
  obtain ⟨x, hxS, hcx⟩ : ∃ x, x ∈ S ∧ c x ≠ u x := by
    by_contra h
    apply hu
    refine ⟨c, hc, ?_⟩
    intro x hxS
    by_contra hcx
    apply h
    exact ⟨x, hxS, hcx⟩
  have hxK : x ∉ K := by
    intro hxK
    exact hcx (hcK x hxK)
  have hKxS : insert x K ⊆ S := by
    intro y hy
    rw [Finset.mem_insert] at hy
    rcases hy with rfl | hy
    · exact hxS
    · exact hKS hy
  have hKxcard : (insert x K).card = k + 1 := by
    rw [Finset.card_insert_of_notMem hxK, hKcard]
  have huKx :
      ¬ GrandeFinale.Explained (rsEval ev k : Set (D → F)) u (insert x K) := by
    rintro ⟨c', hc', hc'Kx⟩
    have hcc' : c = c' := rsEval_eq_of_agree_on_card_ge
      ev hev k K (by omega) hc hc' (fun d hd ↦ by
        calc
          c d = u d := hcK d hd
          _ = c' d := (hc'Kx d (Finset.mem_insert_of_mem hd)).symm)
    apply hcx
    calc
      c x = c' x := congrFun hcc' x
      _ = u x := hc'Kx x (Finset.mem_insert_self x K)
  obtain ⟨T, hKxT, hTS, hTcard⟩ :=
    Finset.exists_subsuperset_card_eq hKxS (by omega) hSa
  refine ⟨T, hTS, hTcard, ?_⟩
  rintro ⟨c', hc', hc'T⟩
  apply huKx
  exact ⟨c', hc', fun d hd ↦ hc'T d (hKxT hd)⟩

omit [Fintype D] in
/-- Every threshold-`a` MCA witness for an injective Reed--Solomon code has an
exact `a`-element witness support when `a >= k+1`. -/
theorem mcaBad_has_exact_support
    (ev : D → F) (hev : Function.Injective ev)
    (k a : Nat) (hka : k + 1 ≤ a)
    (u0 u1 : D → F) (gamma : F)
    (hbad : GrandeFinale.MCABad (rsEval ev k : Set (D → F))
      u0 u1 a gamma) :
    ∃ T : Finset D, T.card = a ∧
      GrandeFinale.Explained (rsEval ev k : Set (D → F))
        (fun d ↦ u0 d + gamma * u1 d) T ∧
      ¬ GrandeFinale.ExplainedPair (rsEval ev k : Set (D → F)) u0 u1 T := by
  obtain ⟨S, hSa, hline, hpair⟩ := hbad
  rw [explainedPair_iff_explained_and] at hpair
  by_cases h0 : GrandeFinale.Explained (rsEval ev k : Set (D → F)) u0 S
  · have h1 : ¬ GrandeFinale.Explained (rsEval ev k : Set (D → F)) u1 S :=
      fun h1 ↦ hpair ⟨h0, h1⟩
    obtain ⟨T, hTS, hTcard, h1T⟩ :=
      exists_exact_support_preserving_not_explained
        ev hev k a hka S hSa u1 h1
    refine ⟨T, hTcard, ?_, ?_⟩
    · obtain ⟨c, hc, hcS⟩ := hline
      exact ⟨c, hc, fun d hd ↦ hcS d (hTS hd)⟩
    · rw [explainedPair_iff_explained_and]
      exact fun hp ↦ h1T hp.2
  · obtain ⟨T, hTS, hTcard, h0T⟩ :=
      exists_exact_support_preserving_not_explained
        ev hev k a hka S hSa u0 h0
    refine ⟨T, hTcard, ?_, ?_⟩
    · obtain ⟨c, hc, hcS⟩ := hline
      exact ⟨c, hc, fun d hd ↦ hcS d (hTS hd)⟩
    · rw [explainedPair_iff_explained_and]
      exact fun hp ↦ h0T hp.1

/-- The family of exact `a`-element supports. -/
def supportsExactly (a : Nat) : Finset (Finset D) :=
  (Finset.univ : Finset D).powersetCard a

section FiniteField

variable [Fintype F] [DecidableEq F]

omit [DecidableEq F] in
/-- For an injective Reed--Solomon code, threshold-`a` bad slopes are exactly
the union of the fixed-support cells indexed by exact `a`-element supports. -/
theorem mcaBadSlopes_eq_exactSupportFamily
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a : Nat) (hka : k + 1 ≤ a) (u0 u1 : D → F) :
    Finset.univ.filter (fun gamma : F ↦
      GrandeFinale.MCABad (rsEval ev k : Set (D → F)) u0 u1 a gamma) =
      badSlopeSetOnSupportFamily (parityCheck ev R)
        (supportsExactly a) u0 u1 := by
  have hker := ker_parityCheck_eq_rsEval ev hev k R hsize
  ext gamma
  simp only [Finset.mem_filter, Finset.mem_univ, true_and,
    badSlopeSetOnSupportFamily]
  constructor
  · intro hbad
    obtain ⟨T, hTcard, hline, hpair⟩ :=
      mcaBad_has_exact_support ev hev k a hka u0 u1 gamma hbad
    refine ⟨T, ?_, ?_⟩
    · simp [supportsExactly, hTcard]
    · unfold BadOnSupport
      rw [hker]
      exact ⟨hline, hpair⟩
  · rintro ⟨T, hT, hbadT⟩
    have hTcard : T.card = a := (Finset.mem_powersetCard.mp hT).2
    unfold BadOnSupport at hbadT
    rw [hker] at hbadT
    exact ⟨T, by omega, hbadT.1, hbadT.2⟩

/-- A fixed received line has at most `choose |D| a` MCA-bad slopes at
agreement `a >= k+1`. -/
theorem mcaBadSlopes_card_le_choose
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a : Nat) (hka : k + 1 ≤ a) (u0 u1 : D → F) :
    (Finset.univ.filter (fun gamma : F ↦
      GrandeFinale.MCABad (rsEval ev k : Set (D → F))
        u0 u1 a gamma)).card ≤ Nat.choose (Fintype.card D) a := by
  rw [mcaBadSlopes_eq_exactSupportFamily ev hev k R hsize a hka u0 u1]
  calc
    (badSlopeSetOnSupportFamily (parityCheck ev R)
        (supportsExactly a) u0 u1).card ≤ (supportsExactly a).card :=
      badSlopeSetOnSupportFamily_card_le _ _ _ _
    _ = Nat.choose (Fintype.card D) a := by
      simp [supportsExactly, Finset.card_powersetCard]

/-- Exact support-atlas upper bound for the full-field Reed--Solomon MCA
numerator. -/
theorem B_MCA_rsEval_le_choose
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a : Nat) (hka : k + 1 ≤ a) :
    GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) a ≤
      Nat.choose (Fintype.card D) a := by
  unfold GrandeFinale.B_MCA
  apply Finset.sup_le
  intro p _hp
  exact mcaBadSlopes_card_le_choose
    ev hev k R hsize a hka p.1 p.2

end FiniteField

#print axioms mcaBad_has_exact_support
#print axioms B_MCA_rsEval_le_choose

end GrandeFinale.RSExactSupportUpper
