import GrandeFinale
import cs25_cap_v12.RSSandwich

/-!
# Exact integer deep-regime MCA upper bound

This module connects the exact agreement-grid numerator to a finite-field
deep-regime cardinality bound.

The bridge is literal: at agreement `a`, radius `(n-a)/n`, the two support-wise
MCA predicates coincide.  The resulting theorem bounds the maximum number of
bad slopes in an arbitrary finite challenge set, rather than only the
full-field normalized probability.
-/

open scoped Classical

noncomputable section

namespace AsymptoticRsMcaFrontiers.Deep

variable {D F : Type*} [Fintype D] [DecidableEq D]
  [Field F] [Fintype F] [DecidableEq F]

/-- The closed-grid radius attached to agreement `a`. -/
def agreementRadius (a : Nat) : Real :=
  ((Fintype.card D - a : Nat) : Real) / Fintype.card D

/-- At the exact grid radius `(n-a)/n`, the real support-size test is exactly
the integer agreement test `a ≤ |S|`. -/
theorem radius_support_iff {a : Nat} (ha : a ≤ Fintype.card D)
    (hn : 0 < Fintype.card D) (S : Finset D) :
    (1 - agreementRadius (D := D) a) * Fintype.card D ≤ (S.card : Real) ↔
      a ≤ S.card := by
  have hnR : (0 : Real) < Fintype.card D := by exact_mod_cast hn
  rw [agreementRadius, Nat.cast_sub ha]
  constructor
  · intro h
    have h' : (a : Real) ≤ S.card := by
      field_simp [ne_of_gt hnR] at h
      nlinarith
    exact_mod_cast h'
  · intro h
    have h' : (a : Real) ≤ S.card := by exact_mod_cast h
    field_simp [ne_of_gt hnR]
    nlinarith

/-- The exact-agreement and real-radius definitions of support-wise MCA badness
coincide at a closed integer grid point. -/
theorem mcaBad_iff_radius {C : Set (D → F)} {f0 f1 : D → F}
    {a : Nat} (ha : a ≤ Fintype.card D) (hn : 0 < Fintype.card D) (γ : F) :
    GrandeFinale.MCABad C f0 f1 a γ ↔
      RSCap.mcaBad C (agreementRadius (D := D) a) f0 f1 γ := by
  constructor
  · rintro ⟨S, hSa, ⟨c, hc, hline⟩, hpair⟩
    refine ⟨S, (radius_support_iff ha hn S).2 hSa, ?_, ?_⟩
    · exact ⟨c, hc, fun x hx ↦ (hline x hx).symm⟩
    · rintro ⟨c0, hc0, c1, hc1, hsim⟩
      apply hpair
      exact ⟨c0, hc0, c1, hc1,
        fun x hx ↦ (hsim x hx).1.symm,
        fun x hx ↦ (hsim x hx).2.symm⟩
  · rintro ⟨S, hSa, ⟨c, hc, hline⟩, hpair⟩
    refine ⟨S, (radius_support_iff ha hn S).1 hSa, ?_, ?_⟩
    · exact ⟨c, hc, fun x hx ↦ (hline x hx).symm⟩
    · rintro ⟨c0, hc0, c1, hc1, h0, h1⟩
      apply hpair
      exact ⟨c0, hc0, c1, hc1,
        fun x hx ↦ ⟨(h0 x hx).symm, (h1 x hx).symm⟩⟩

/-- Exact bad slopes for one received pair after restriction to the actual
challenge set. -/
def challengeBadSlopes (C : Set (D → F)) (Γ : Finset F)
    (f0 f1 : D → F) (a : Nat) : Finset F :=
  Γ.filter fun γ ↦ GrandeFinale.MCABad C f0 f1 a γ

/-- Exact challenge-restricted MCA numerator: maximize the deduplicated slope
count over all received pairs. -/
def B_MCA_challenge (C : Set (D → F)) (Γ : Finset F) (a : Nat) : Nat :=
  Finset.univ.sup fun p : (D → F) × (D → F) ↦
    (challengeBadSlopes C Γ p.1 p.2 a).card

/-- Restricting the challenge set cannot increase the full-field numerator. -/
theorem B_MCA_challenge_le_B_MCA (C : Set (D → F)) (Γ : Finset F)
    (a : Nat) :
    B_MCA_challenge C Γ a ≤ GrandeFinale.B_MCA C a := by
  refine Finset.sup_le fun p hp ↦ ?_
  refine (Finset.card_le_card ?_).trans (Finset.le_sup (f := fun p : (D → F) × (D → F) ↦ (Finset.univ.filter (fun γ : F ↦ GrandeFinale.MCABad C p.1 p.2 a γ)).card) hp)
  intro γ hγ
  simp only [challengeBadSlopes, Finset.mem_filter] at hγ ⊢
  exact ⟨Finset.mem_univ γ, hγ.2⟩

/-- A challenge-restricted numerator is at most the challenge cardinality. -/
theorem B_MCA_challenge_le_card (C : Set (D → F)) (Γ : Finset F)
    (a : Nat) : B_MCA_challenge C Γ a ≤ Γ.card := by
  refine Finset.sup_le fun p _hp ↦ ?_
  simpa [challengeBadSlopes] using Finset.card_filter_le Γ
    (fun γ : F ↦ GrandeFinale.MCABad C p.1 p.2 a γ)

/-- Exact cardinal form of the abstract deep-regime proof for one received
pair.  Unlike the normalized theorem, this conclusion can be intersected with
an arbitrary challenge set without changing denominators. -/
theorem mcaBad_card_le_deep (C : Submodule F (D → F)) {d : Nat}
    (hmin : ∀ z ∈ C, z ≠ (0 : D → F) → d ≤ RSCap.numDiff z 0)
    (δ : Real) (hδ : 0 ≤ δ)
    (hdeep : 3 * ⌊δ * (Fintype.card D : Real)⌋₊ ≤ d - 1)
    (f0 f1 : D → F) :
    (Finset.univ.filter fun γ : F ↦
      RSCap.mcaBad (C : Set (D → F)) δ f0 f1 γ).card ≤
        ⌊δ * (Fintype.card D : Real)⌋₊ + 1 := by
  by_cases hclose : RSCap.intClose (C : Set (D → F)) δ f0 f1
  · obtain ⟨c0, hc0, c1, hc1, hclose⟩ := hclose
    have hhalf : 2 * ⌊δ * (Fintype.card D : Real)⌋₊ ≤ d - 1 := by omega
    exact (RSCap.mcaBad_close_tangent C hmin δ hhalf
      f0 f1 c0 hc0 c1 hc1 hclose).trans (Nat.le_succ _)
  · rcases RSCap.close_slope_dichotomy C hmin δ hδ hdeep f0 f1 with h | h
    · exact (hclose h).elim
    · refine (Finset.card_le_card ?_).trans h
      intro γ hγ
      have hmca := (Finset.mem_filter.mp hγ).2
      exact Finset.mem_filter.mpr
        ⟨Finset.mem_univ γ, RSCap.mcaBad_imp_caClose _ _ _ _ _ hmca⟩

/-- The exact full-field MCA numerator satisfies the deep-regime bound. -/
theorem B_MCA_le_deep (C : Submodule F (D → F)) {d a : Nat}
    (hmin : ∀ z ∈ C, z ≠ (0 : D → F) → d ≤ RSCap.numDiff z 0)
    (hn : 0 < Fintype.card D) (ha : a ≤ Fintype.card D)
    (hdeep : 3 * (Fintype.card D - a) ≤ d - 1) :
    GrandeFinale.B_MCA (C : Set (D → F)) a ≤ Fintype.card D - a + 1 := by
  let δ := agreementRadius (D := D) a
  have hnR : (0 : Real) < Fintype.card D := by exact_mod_cast hn
  have hδ : 0 ≤ δ := by
    exact div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)
  have hradius : δ * (Fintype.card D : Real) = (Fintype.card D - a : Nat) := by
    dsimp [δ, agreementRadius]
    field_simp [ne_of_gt hnR]
  have hfloor : ⌊δ * (Fintype.card D : Real)⌋₊ = Fintype.card D - a := by
    rw [hradius]
    simp
  refine Finset.sup_le fun p _hp ↦ ?_
  have heq :
      (Finset.univ.filter fun γ : F ↦
        GrandeFinale.MCABad (C : Set (D → F)) p.1 p.2 a γ) =
      (Finset.univ.filter fun γ : F ↦
        RSCap.mcaBad (C : Set (D → F)) δ p.1 p.2 γ) := by
    ext γ
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    exact mcaBad_iff_radius ha hn γ
  rw [heq]
  simpa [hfloor] using
    mcaBad_card_le_deep C hmin δ hδ (by simpa [hfloor] using hdeep) p.1 p.2

/-- Deep upper bound with both the challenge-cardinality ceiling and the exact
`r+1` incidence ceiling visible. -/
theorem B_MCA_challenge_le_deep (C : Submodule F (D → F))
    (Γ : Finset F) {d a : Nat}
    (hmin : ∀ z ∈ C, z ≠ (0 : D → F) → d ≤ RSCap.numDiff z 0)
    (hn : 0 < Fintype.card D) (ha : a ≤ Fintype.card D)
    (hdeep : 3 * (Fintype.card D - a) ≤ d - 1) :
    B_MCA_challenge (C : Set (D → F)) Γ a ≤
      min Γ.card (Fintype.card D - a + 1) := by
  exact Nat.le_min.mpr ⟨B_MCA_challenge_le_card _ _ _,
    (B_MCA_challenge_le_B_MCA _ _ _).trans
      (B_MCA_le_deep C hmin hn ha hdeep)⟩

/-- Reed--Solomon specialization of the exact challenge-restricted deep upper
bound. -/
theorem rs_B_MCA_challenge_le_deep (dom : D → F)
    (hdom : Function.Injective dom) {k a : Nat} (Γ : Finset F)
    (hk : k ≤ Fintype.card D) (hn : 0 < Fintype.card D)
    (ha : a ≤ Fintype.card D)
    (hdeep : 3 * (Fintype.card D - a) ≤ Fintype.card D - k) :
    B_MCA_challenge (RSCap.RSpoly dom k) Γ a ≤
      min Γ.card (Fintype.card D - a + 1) := by
  apply B_MCA_challenge_le_deep (RSCap.RSpolySubmodule dom k) Γ
    (RSCap.rs_min_weight dom hdom k) hn ha
  omega

#print axioms radius_support_iff
#print axioms mcaBad_iff_radius
#print axioms mcaBad_card_le_deep
#print axioms B_MCA_le_deep
#print axioms B_MCA_challenge_le_deep
#print axioms rs_B_MCA_challenge_le_deep

end AsymptoticRsMcaFrontiers.Deep
