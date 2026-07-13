import AsymptoticRsMcaFrontiers.Deep

/-!
# Universal tangent floor and the exact Reed--Solomon deep numerator

The tangent construction is written directly in word coordinates. A finite
set X of coordinates is labelled by distinct challenge slopes. At coordinate
x in X, the received pair has value (-gamma_x, 1); it is zero off X. At slope
gamma_x the line therefore agrees with the zero codeword away from X minus x.
Minimum distance prevents the second received word from being explained on
that same support.

Combining this lower construction with the challenge-restricted deep upper
bound proves the exact numerator in the deep regime.
-/

open scoped Classical

noncomputable section

namespace AsymptoticRsMcaFrontiers.Tangent

open AsymptoticRsMcaFrontiers.Deep

variable {D F : Type*} [Fintype D] [DecidableEq D]
  [Field F] [Fintype F] [DecidableEq F]

/-- The second received word of the tangent construction. -/
def tangentOne (X : Finset D) : D → F := fun x ↦ if x ∈ X then 1 else 0

/-- The first received word of the tangent construction. -/
def tangentZero (X : Finset D) (slope : D → F) : D → F :=
  fun x ↦ if x ∈ X then -slope x else 0

/-- Remove all labelled coordinates other than x. -/
def tangentSupport (X : Finset D) (x : D) : Finset D :=
  Finset.univ \ (X.erase x)

omit [Fintype F] [DecidableEq F] in
/-- Every labelled coordinate produces a support-wise MCA-bad slope. The only
code input is a minimum-distance lower bound strictly larger than the size of
the labelled coordinate set. -/
theorem tangent_bad_of_mem (C : Submodule F (D → F)) {d a : Nat}
    (hmin : ∀ z ∈ C, z ≠ (0 : D → F) → d ≤ RSCap.numDiff z 0)
    (X : Finset D) (slope : D → F)
    (ha : a ≤ Fintype.card D) (hsize : X.card ≤ Fintype.card D - a + 1) (hdist : X.card < d)
    {x : D} (hx : x ∈ X) :
    GrandeFinale.MCABad (C : Set (D → F))
      (tangentZero X slope) (tangentOne X) a (slope x) := by
  classical
  let S := tangentSupport X x
  have hxS : x ∈ S := by
    simp [S, tangentSupport, hx]
  have hScard : a ≤ S.card := by
    have hcard : S.card = Fintype.card D - (X.card - 1) := by
      dsimp [S, tangentSupport]
      rw [Finset.card_sdiff]
      simp [Finset.card_erase_of_mem hx]
    rw [hcard]
    have hXn : X.card ≤ Fintype.card D := Finset.card_le_univ X
    omega
  have hline : GrandeFinale.Explained (C : Set (D → F))
      (fun y ↦ tangentZero X slope y + slope x * tangentOne X y) S := by
    refine ⟨0, C.zero_mem, ?_⟩
    intro y hy
    have hyErase : y ∉ X.erase x := (Finset.mem_sdiff.mp hy).2
    by_cases hyX : y ∈ X
    · have hyx : y = x := by
        simpa [Finset.mem_erase, hyX] using hyErase
      subst y
      simp [tangentZero, tangentOne, hx]
    · simp [tangentZero, tangentOne, hyX]
  have hpair : ¬ GrandeFinale.ExplainedPair (C : Set (D → F))
      (tangentZero X slope) (tangentOne X) S := by
    rintro ⟨c0, hc0, c1, hc1, _h0, h1⟩
    have hc1x : c1 x = 1 := by simpa [tangentOne, hx] using h1 x hxS
    have hc1ne : c1 ≠ (0 : D → F) := by
      intro hz
      have h01 : (0 : F) = 1 := by simpa [hz] using hc1x
      exact zero_ne_one h01
    have hweight : RSCap.numDiff c1 0 ≤ X.card := by
      unfold RSCap.numDiff
      apply Finset.card_le_card
      intro y hy
      have hc1y : c1 y ≠ 0 := (Finset.mem_filter.mp hy).2
      by_contra hyX
      have hyS : y ∈ S := by
        simp [S, tangentSupport, hyX]
      have : c1 y = 0 := by simpa [tangentOne, hyX] using h1 y hyS
      exact hc1y this
    have := hmin c1 hc1 hc1ne
    omega
  exact ⟨S, hScard, hline, hpair⟩

/-- A labelled coordinate chart injects its labels into the
challenge-restricted bad-slope set. -/
theorem tangent_chart_lower (C : Submodule F (D → F)) (Γ : Finset F)
    {d a : Nat}
    (hmin : ∀ z ∈ C, z ≠ (0 : D → F) → d ≤ RSCap.numDiff z 0)
    (X : Finset D) (slope : D → F)
    (hΓ : ∀ x ∈ X, slope x ∈ Γ) (hinj : Set.InjOn slope X)
    (ha : a ≤ Fintype.card D) (hsize : X.card ≤ Fintype.card D - a + 1) (hdist : X.card < d) :
    X.card ≤ B_MCA_challenge (C : Set (D → F)) Γ a := by
  let f0 := tangentZero X slope
  let f1 := tangentOne (F := F) X
  have hsubset : X.image slope ⊆
      challengeBadSlopes (C : Set (D → F)) Γ f0 f1 a := by
    intro γ hγ
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hγ
    exact Finset.mem_filter.mpr ⟨hΓ x hx,
      tangent_bad_of_mem C hmin X slope ha hsize hdist hx⟩
  calc
    X.card = (X.image slope).card := (Finset.card_image_of_injOn hinj).symm
    _ ≤ (challengeBadSlopes (C : Set (D → F)) Γ f0 f1 a).card :=
      Finset.card_le_card hsubset
    _ ≤ B_MCA_challenge (C : Set (D → F)) Γ a :=
      Finset.le_sup
        (f := fun p : (D → F) × (D → F) ↦
          (challengeBadSlopes (C : Set (D → F)) Γ p.1 p.2 a).card)
        (Finset.mem_univ (f0, f1))

/-- Universal tangent floor for any linear code whose minimum distance is
strictly larger than n-a+1. -/
theorem tangent_floor (C : Submodule F (D → F)) (Γ : Finset F)
    {d a : Nat}
    (hmin : ∀ z ∈ C, z ≠ (0 : D → F) → d ≤ RSCap.numDiff z 0)
    (ha1 : 1 ≤ a) (ha : a ≤ Fintype.card D)
    (hdist : Fintype.card D - a + 1 < d) :
    min Γ.card (Fintype.card D - a + 1) ≤
      B_MCA_challenge (C : Set (D → F)) Γ a := by
  let t := min Γ.card (Fintype.card D - a + 1)
  have htD : t ≤ Fintype.card D := by
    dsimp [t]
    have := min_le_right Γ.card (Fintype.card D - a + 1)
    omega
  obtain ⟨X, _hXuniv, hXcard⟩ :=
    Finset.exists_subset_card_eq (s := (Finset.univ : Finset D)) htD
  have htΓ : t ≤ Γ.card := by exact min_le_left _ _
  obtain ⟨G, hGΓ, hGcard⟩ := Finset.exists_subset_card_eq (s := Γ) htΓ
  let e : X ≃ G := Finset.equivOfCardEq (hXcard.trans hGcard.symm)
  let slope : D → F :=
    Function.extend Subtype.val (fun z : X ↦ (e z : F)) 0
  have hslope (x : D) (hx : x ∈ X) : slope x = (e ⟨x, hx⟩ : F) := by
    simpa only [slope] using
      (Subtype.val_injective.extend_apply (fun z : X ↦ (e z : F))
        (0 : D → F) ⟨x, hx⟩)
  have hslopeΓ : ∀ x ∈ X, slope x ∈ Γ := by
    intro x hx
    rw [hslope x hx]
    exact hGΓ (e ⟨x, hx⟩).property
  have hinj : Set.InjOn slope X := by
    intro x hx y hy hxy
    have heq : (e ⟨x, hx⟩ : F) = (e ⟨y, hy⟩ : F) :=
      (hslope x hx).symm.trans (hxy.trans (hslope y hy))
    have hsub : e ⟨x, hx⟩ = e ⟨y, hy⟩ := Subtype.ext heq
    exact congrArg Subtype.val (e.injective hsub)
  have hsize : X.card ≤ Fintype.card D - a + 1 := by
    rw [hXcard]
    exact min_le_right _ _
  have hXd : X.card < d := hsize.trans_lt hdist
  have hchart :=
    tangent_chart_lower C Γ hmin X slope hslopeΓ hinj ha hsize hXd
  rw [hXcard] at hchart
  simpa only [t] using hchart

/-- Exact challenge-restricted deep numerator for Reed--Solomon codes. -/
theorem rs_B_MCA_challenge_eq_deep (dom : D → F)
    (hdom : Function.Injective dom) {k a : Nat} (Γ : Finset F)
    (hk : 1 ≤ k) (hka : k + 1 ≤ a) (ha : a ≤ Fintype.card D)
    (hdeep : 3 * (Fintype.card D - a) ≤ Fintype.card D - k) :
    B_MCA_challenge (RSCap.RSpoly dom k) Γ a =
      min Γ.card (Fintype.card D - a + 1) := by
  have hn : 0 < Fintype.card D := by omega
  have hkn : k ≤ Fintype.card D := by omega
  have hdist : Fintype.card D - a + 1 < Fintype.card D + 1 - k := by omega
  apply Nat.le_antisymm
  · exact rs_B_MCA_challenge_le_deep dom hdom Γ hkn hn ha hdeep
  · exact tangent_floor (RSCap.RSpolySubmodule dom k) Γ
      (RSCap.rs_min_weight dom hdom k) (by omega) ha hdist

#print axioms tangent_bad_of_mem
#print axioms tangent_chart_lower
#print axioms tangent_floor
#print axioms rs_B_MCA_challenge_eq_deep

end AsymptoticRsMcaFrontiers.Tangent
