import RsMcaThresholds.ExactSparsification

/-!
# Exact sparse mutual layer below half the minimum distance

This file formalizes `thm:exact-half-distance-sparse` (HD1) from
`experimental/rs_mca_thresholds.tex`.
-/

open scoped BigOperators Classical

noncomputable section

namespace RsMcaThresholds
namespace HalfDistanceSparse

set_option autoImplicit false

open ExactSparsification

universe u v

variable {F : Type u} {D : Type v}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]

local notation "Word" => D → F

/-- Every nonzero codeword has Hamming weight at least `d`. This is the exact
minimum-distance interface used by HD1. -/
def MinimumDistanceAtLeast (C : Submodule F Word) (d : ℕ) : Prop :=
  ∀ c ∈ C, c ≠ 0 → d ≤ (wordSupport c).card

omit [Fintype F] [DecidableEq D] in
theorem mem_wordSupport_iff {f : Word} {x : D} :
    x ∈ wordSupport f ↔ f x ≠ 0 := by
  simp [wordSupport]

omit [Fintype F] in
theorem mem_pairSupport_iff {f₀ f₁ : Word} {x : D} :
    x ∈ pairSupport f₀ f₁ ↔ f₀ x ≠ 0 ∨ f₁ x ≠ 0 := by
  simp [pairSupport, wordSupport]

omit [Fintype F] in
/-- Under the half-distance hypothesis, a codeword explaining a sparse line
point on a large support must be zero. -/
theorem explaining_codeword_eq_zero
    (C : Submodule F Word) (d r : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hhalf : 2 * r ≤ d - 1)
    (hr : r ≤ Fintype.card D)
    (e₀ e₁ c : Word) (γ : F) (S : Finset D)
    (hsparse : SparseAt e₀ e₁ (Fintype.card D - r))
    (hS : Fintype.card D - r ≤ S.card)
    (hc : c ∈ C)
    (hline : ∀ x ∈ S, c x = e₀ x + γ * e₁ x) :
    c = 0 := by
  have hE : (pairSupport e₀ e₁).card ≤ r := by
    unfold SparseAt at hsparse
    simpa [Nat.sub_sub_self hr] using hsparse
  have hcomp : (Finset.univ \ S).card ≤ r := by
    rw [Finset.card_sdiff]
    simp only [Finset.inter_univ, Finset.card_univ]
    have hScard : S.card ≤ Fintype.card D := by
      simpa using Finset.card_le_univ S
    omega
  have hcsub :
      wordSupport c ⊆ pairSupport e₀ e₁ ∪ (Finset.univ \ S) := by
    intro x hx
    by_cases hxE : x ∈ pairSupport e₀ e₁
    · exact Finset.mem_union_left _ hxE
    · apply Finset.mem_union_right
      rw [Finset.mem_sdiff]
      refine ⟨Finset.mem_univ x, ?_⟩
      intro hxS
      have he₀ : e₀ x = 0 := by
        by_contra hne
        exact hxE ((mem_pairSupport_iff).2 (Or.inl hne))
      have he₁ : e₁ x = 0 := by
        by_contra hne
        exact hxE ((mem_pairSupport_iff).2 (Or.inr hne))
      have hcne : c x ≠ 0 := (mem_wordSupport_iff).1 hx
      apply hcne
      rw [hline x hxS, he₀, he₁]
      simp
  have hcweight : (wordSupport c).card ≤ 2 * r := by
    calc
      (wordSupport c).card
          ≤ (pairSupport e₀ e₁ ∪ (Finset.univ \ S)).card :=
        Finset.card_le_card hcsub
      _ ≤ (pairSupport e₀ e₁).card + (Finset.univ \ S).card :=
        Finset.card_union_le _ _
      _ ≤ r + r := Nat.add_le_add hE hcomp
      _ = 2 * r := by omega
  by_contra hcne
  have hdle := hdist c hc hcne
  have hcpos : 0 < (wordSupport c).card := by
    apply Finset.card_pos.mpr
    rw [Finset.nonempty_iff_ne_empty]
    intro hempty
    apply hcne
    funext x
    by_contra hcx
    have hxmem : x ∈ wordSupport c := (mem_wordSupport_iff).2 hcx
    rw [hempty] at hxmem
    simp at hxmem
  omega

omit [Fintype F] in
/-- Every sparse MCA-bad slope below half the distance is determined by a
nonzero coordinate of the sparse pair. -/
theorem mcaBad_mem_coordinateSlope_image
    (C : Submodule F Word) (d r : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hhalf : 2 * r ≤ d - 1)
    (hr : r ≤ Fintype.card D)
    (e₀ e₁ : Word)
    (hsparse : SparseAt e₀ e₁ (Fintype.card D - r))
    (γ : F)
    (hbad : GrandeFinale.MCABad (C : Set Word) e₀ e₁
      (Fintype.card D - r) γ) :
    γ ∈ (pairSupport e₀ e₁).image (fun x => -e₀ x / e₁ x) := by
  rcases hbad with ⟨S, hS, ⟨c, hc, hline⟩, hpair⟩
  have hc0 : c = 0 :=
    explaining_codeword_eq_zero C d r hdist hhalf hr e₀ e₁ c γ S
      hsparse hS hc hline
  have hex : ∃ x ∈ S, e₀ x ≠ 0 ∨ e₁ x ≠ 0 := by
    by_contra h
    push_neg at h
    apply hpair
    refine ⟨0, C.zero_mem, 0, C.zero_mem, ?_, ?_⟩
    · intro x hx
      simpa using (h x hx).1.symm
    · intro x hx
      simpa using (h x hx).2.symm
  rcases hex with ⟨x, hxS, hxne⟩
  have hxE : x ∈ pairSupport e₀ e₁ :=
    (mem_pairSupport_iff).2 hxne
  have heq : e₀ x + γ * e₁ x = 0 := by
    simpa [hc0] using (hline x hxS).symm
  have he₁ : e₁ x ≠ 0 := by
    intro he₁
    have he₀ : e₀ x = 0 := by simpa [he₁] using heq
    exact hxne.elim (fun h => h he₀) (fun h => h he₁)
  have hγ : γ = -e₀ x / e₁ x := by
    apply (eq_div_iff he₁).2
    linear_combination heq
  exact Finset.mem_image.mpr ⟨x, hxE, hγ.symm⟩

omit [Fintype F] in
/-- The upper half of HD1: a sparse pair has at most one bad slope per
coordinate in its support union. -/
theorem restrictedMCA_card_le_min
    (Γ : Finset F) (C : Submodule F Word) (d r : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hhalf : 2 * r ≤ d - 1)
    (hr : r ≤ Fintype.card D)
    (e₀ e₁ : Word)
    (hsparse : SparseAt e₀ e₁ (Fintype.card D - r)) :
    (restrictedMCABadSlopes Γ C e₀ e₁
      (Fintype.card D - r)).card ≤ min Γ.card r := by
  have hsupport : (pairSupport e₀ e₁).card ≤ r := by
    unfold SparseAt at hsparse
    simpa [Nat.sub_sub_self hr] using hsparse
  have hsub :
      restrictedMCABadSlopes Γ C e₀ e₁ (Fintype.card D - r) ⊆
        (pairSupport e₀ e₁).image (fun x => -e₀ x / e₁ x) := by
    intro γ hγ
    exact mcaBad_mem_coordinateSlope_image C d r hdist hhalf hr e₀ e₁
      hsparse γ (Finset.mem_filter.mp hγ).2
  apply (Nat.le_min).2
  constructor
  · exact Finset.card_le_card (Finset.filter_subset _ _)
  · exact le_trans (Finset.card_le_card hsub)
      (le_trans Finset.card_image_le hsupport)

/-- The sparse mutual numerator is at most the HD1 value. -/
theorem sparseMutualChallenge_le_min
    (Γ : Finset F) (C : Submodule F Word) (d r : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hhalf : 2 * r ≤ d - 1)
    (hr : r ≤ Fintype.card D) :
    sparseMutualChallenge Γ C (Fintype.card D - r) ≤ min Γ.card r := by
  unfold sparseMutualChallenge
  refine Finset.sup_le ?_
  intro p hp
  by_cases hsparse : SparseAt p.1 p.2 (Fintype.card D - r)
  · simp only [hsparse, if_true]
    exact restrictedMCA_card_le_min Γ C d r hdist hhalf hr p.1 p.2 hsparse
  · simp [hsparse]

/-- Indicator word equal to one on `E` and zero off `E`. -/
def plantedOne (E : Finset D) : Word :=
  fun x => if x ∈ E then 1 else 0

/-- Word that stores the negative challenge slope assigned to each point of
`E` by an equivalence `E ≃ G`. -/
def plantedSlope (E : Finset D) (G : Finset F) (φ : E ≃ G) : Word :=
  fun x => if hx : x ∈ E then -(φ ⟨x, hx⟩ : F) else 0

omit [Fintype F] in
theorem pairSupport_planted_subset
    (E : Finset D) (G : Finset F) (φ : E ≃ G) :
    pairSupport (plantedSlope E G φ) (plantedOne E) ⊆ E := by
  intro x hx
  rw [mem_pairSupport_iff] at hx
  by_contra hxE
  have h₀ : plantedSlope E G φ x = 0 := by simp [plantedSlope, hxE]
  have h₁ : plantedOne (F := F) E x = (0 : F) := by simp [plantedOne, hxE]
  exact hx.elim (fun h => h h₀) (fun h => h h₁)

omit [Fintype F] in
/-- Every selected challenge slope is MCA-bad for the planted sparse pair. -/
theorem plantedSlope_mcaBad
    (C : Submodule F Word) (d r t : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hhalf : 2 * r ≤ d - 1)
    (hr : r ≤ Fintype.card D)
    (E : Finset D) (G : Finset F)
    (hEcard : E.card = t) (ht : t ≤ r)
    (φ : E ≃ G) (γ : F) (hγG : γ ∈ G) :
    GrandeFinale.MCABad (C : Set Word)
      (plantedSlope E G φ) (plantedOne E)
      (Fintype.card D - r) γ := by
  let xE : E := φ.symm ⟨γ, hγG⟩
  let x : D := xE
  have hxE : x ∈ E := xE.property
  have hφ : φ xE = ⟨γ, hγG⟩ := φ.apply_symm_apply ⟨γ, hγG⟩
  let S : Finset D := Finset.univ \ (E.erase x)
  have hxS : x ∈ S := by
    simp [S]
  have htpos : 0 < t := by
    have hGpos : 0 < G.card := Finset.card_pos.mpr ⟨γ, hγG⟩
    have hcard : G.card = t := by
      simpa [hEcard] using (Fintype.card_congr φ).symm
    omega
  have hScard : Fintype.card D - r ≤ S.card := by
    have herase : (E.erase x).card = t - 1 := by
      rw [Finset.card_erase_of_mem hxE, hEcard]
    have hSformula :
        S.card = Fintype.card D - (t - 1) := by
      simp [S, Finset.card_sdiff, herase]
    omega
  refine ⟨S, hScard, ?_, ?_⟩
  · refine ⟨0, C.zero_mem, ?_⟩
    intro y hyS
    have hyerase : y ∉ E.erase x := (Finset.mem_sdiff.mp hyS).2
    by_cases hyE : y ∈ E
    · have hyx : y = x := by
        by_contra hyx
        exact hyerase (Finset.mem_erase.mpr ⟨hyx, hyE⟩)
      subst y
      change (0 : F) =
        plantedSlope E G φ x + γ * plantedOne E x
      simp [plantedSlope, plantedOne, hxE, x, xE, hφ]
    · change (0 : F) =
        plantedSlope E G φ y + γ * plantedOne E y
      simp [plantedSlope, plantedOne, hyE]
  · intro hpair
    rcases hpair with ⟨c₀, hc₀, c₁, hc₁, h₀, h₁⟩
    have hc₁ne : c₁ ≠ 0 := by
      intro hc₁zero
      have hxagree := h₁ x hxS
      change c₁ x = plantedOne E x at hxagree
      simp [hc₁zero, plantedOne, hxE] at hxagree
    have hc₁sub : wordSupport c₁ ⊆ E := by
      intro y hy
      by_contra hyE
      have hyS : y ∈ S := by
        rw [Finset.mem_sdiff]
        refine ⟨Finset.mem_univ _, ?_⟩
        intro hyerase
        exact hyE (Finset.mem_of_mem_erase hyerase)
      have hyagree := h₁ y hyS
      have hc₁zero : c₁ y = 0 := by
        simpa [plantedOne, hyE] using hyagree
      exact (mem_wordSupport_iff.mp hy) hc₁zero
    have hweight : (wordSupport c₁).card ≤ r :=
      le_trans (Finset.card_le_card hc₁sub) (hEcard.le.trans ht)
    have hdle := hdist c₁ hc₁ hc₁ne
    omega

/-- The planted construction gives the matching HD1 lower bound. -/
theorem min_le_sparseMutualChallenge
    (Γ : Finset F) (C : Submodule F Word) (d r : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hhalf : 2 * r ≤ d - 1)
    (hr : r ≤ Fintype.card D) :
    min Γ.card r ≤
      sparseMutualChallenge Γ C (Fintype.card D - r) := by
  let t := min Γ.card r
  have htΓ : t ≤ Γ.card := min_le_left _ _
  have htr : t ≤ r := min_le_right _ _
  have htD : t ≤ (Finset.univ : Finset D).card := by
    simpa using htr.trans hr
  obtain ⟨G, hGΓ, hGcard⟩ :=
    Finset.exists_subset_card_eq (s := Γ) htΓ
  obtain ⟨E, -, hEcard⟩ :=
    Finset.exists_subset_card_eq (s := (Finset.univ : Finset D)) htD
  let φ : E ≃ G :=
    Fintype.equivOfCardEq (by simp [Fintype.card_coe, hEcard, hGcard])
  by_cases ht0 : t = 0
  · simp [t, ht0]
  have hsparse :
      SparseAt (plantedSlope E G φ) (plantedOne E)
        (Fintype.card D - r) := by
    unfold SparseAt
    rw [Nat.sub_sub_self hr]
    exact le_trans
      (Finset.card_le_card (pairSupport_planted_subset E G φ))
      (hEcard.le.trans htr)
  have hGbad :
      G ⊆ restrictedMCABadSlopes Γ C
        (plantedSlope E G φ) (plantedOne E)
        (Fintype.card D - r) := by
    intro γ hγ
    simp only [restrictedMCABadSlopes, Finset.mem_filter]
    exact ⟨hGΓ hγ,
      plantedSlope_mcaBad C d r t hdist hhalf hr E G hEcard htr φ γ hγ⟩
  have hcard :
      t ≤ (restrictedMCABadSlopes Γ C
        (plantedSlope E G φ) (plantedOne E)
        (Fintype.card D - r)).card := by
    rw [← hGcard]
    exact Finset.card_le_card hGbad
  have hp :
      ((plantedSlope E G φ, plantedOne E) : Word × Word) ∈
        (Finset.univ : Finset (Word × Word)) := Finset.mem_univ _
  have hsup := Finset.le_sup
    (s := (Finset.univ : Finset (Word × Word)))
    (f := fun p : Word × Word =>
      if SparseAt p.1 p.2 (Fintype.card D - r)
      then (restrictedMCABadSlopes Γ C p.1 p.2
        (Fintype.card D - r)).card
      else 0) hp
  exact hcard.trans (by
    simpa [sparseMutualChallenge, hsparse] using hsup)

/-- Exact sparse mutual numerator below half the minimum distance (first
identity in HD1). -/
theorem exact_half_distance_sparse
    (Γ : Finset F) (_hΓ : Γ.Nonempty)
    (C : Submodule F Word) (d r : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hr : r ≤ Fintype.card D)
    (hhalf : 2 * r ≤ d - 1) :
    sparseMutualChallenge Γ C (Fintype.card D - r) = min Γ.card r := by
  apply le_antisymm
  · exact sparseMutualChallenge_le_min Γ C d r hdist hhalf hr
  · exact min_le_sparseMutualChallenge Γ C d r hdist hhalf hr

/-- If a code has the Reed--Solomon distance lower bound `n - k + 1`,
the HD1 hypothesis has the literal paper form `2r ≤ n - k`. -/
theorem exact_half_distance_sparse_rsDistance
    (Γ : Finset F) (hΓ : Γ.Nonempty)
    (C : Submodule F Word) (k r : ℕ)
    (hdist : MinimumDistanceAtLeast C (Fintype.card D - k + 1))
    (hr : r ≤ Fintype.card D)
    (hhalf : 2 * r ≤ Fintype.card D - k) :
    sparseMutualChallenge Γ C (Fintype.card D - r) = min Γ.card r := by
  apply exact_half_distance_sparse Γ hΓ C
    (Fintype.card D - k + 1) r hdist hr
  omega

/-- Exact MCA numerator below half the minimum distance (second identity in
HD1). -/
theorem exact_half_distance_mca
    (Γ : Finset F) (hΓ : Γ.Nonempty)
    (C : Submodule F Word) (d r : ℕ)
    (hdist : MinimumDistanceAtLeast C d)
    (hr : r ≤ Fintype.card D)
    (hhalf : 2 * r ≤ d - 1) :
    B_MCA_challenge Γ C (Fintype.card D - r) =
      max (B_CA_challenge Γ C (Fintype.card D - r))
        (min Γ.card r) := by
  rw [exact_sparsification_challenge,
    exact_half_distance_sparse Γ hΓ C d r hdist hr hhalf]

/-- Reed--Solomon-distance specialization of the second HD1 identity. -/
theorem exact_half_distance_mca_rsDistance
    (Γ : Finset F) (hΓ : Γ.Nonempty)
    (C : Submodule F Word) (k r : ℕ)
    (hdist : MinimumDistanceAtLeast C (Fintype.card D - k + 1))
    (hr : r ≤ Fintype.card D)
    (hhalf : 2 * r ≤ Fintype.card D - k) :
    B_MCA_challenge Γ C (Fintype.card D - r) =
      max (B_CA_challenge Γ C (Fintype.card D - r))
        (min Γ.card r) := by
  rw [exact_sparsification_challenge,
    exact_half_distance_sparse_rsDistance Γ hΓ C k r hdist hr hhalf]

#print axioms exact_half_distance_sparse
#print axioms exact_half_distance_mca

end HalfDistanceSparse
end RsMcaThresholds
