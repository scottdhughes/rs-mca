import cs25_cap_v12.Main

/-!
# Safe-side pincer: mutual from correlated agreement up to half the distance

This file formalizes the *safe-side* half of the two-sided sandwich of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*,

namely the theorem **mutual from correlated agreement, up to half the distance**
(`thm:mca-from-ca`) and its immediate corollary **the band conjecture loses its
support-mismatch layer below half the distance** (`cor:band-reduction`).

The result is stated for an arbitrary `F`-linear code `C ⊆ Fⁿ` (a `Submodule`)
of minimum Hamming weight `w`.  Writing `r := ⌊δ·n⌋`, if `2r ≤ w-1` (the
unique-decoding radius of the interleaved code `C^{≡2}` in column weight) then

  `ε_mca(C, δ) ≤ max (ε_ca(C, δ), r/q)`.

The core dichotomy: for each pair `(f₁,f₂)`, either the pair is `δ`-far in column
distance — then every MCA-bad slope is CA-bad — or the pair is `δ`-close — then
every MCA-bad slope is one of at most `r` explicit tangent ratios `-e₁ⱼ/e₂ⱼ`.
-/

namespace RSCap

open Classical

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-
**Case (b): far pairs.**  If a pair `(f₁,f₂)` is *not* `δ`-close to the
interleaved code, then every MCA-bad slope at radius `δ` is CA-bad at radii
`(δ,δ)`.  (A large support `S` explaining `f₁+γf₂` gives a codeword within
relative distance `≤ δ`.)
-/
omit [Fintype F] in
theorem mcaBad_far_imp_caBad (C : Set (ι → F)) (δ : ℝ) (f1 f2 : ι → F) (γ : F)
    (hfar : ¬ intClose C δ f1 f2) (hmca : mcaBad C δ f1 f2 γ) :
    caBad C δ δ f1 f2 γ := by
  obtain ⟨ S, hS₁, hS₂, hS₃ ⟩ := hmca;
  refine' ⟨ _, hfar ⟩;
  refine' ⟨ hS₂.choose, hS₂.choose_spec.1, _ ⟩;
  have h_numDiff : numDiff (fun i => f1 i + γ * f2 i) hS₂.choose ≤ Fintype.card ι - S.card := by
    refine' le_trans ( Finset.card_le_card _ ) _;
    exact Finset.univ \ S;
    · exact fun x hx => Finset.mem_sdiff.mpr ⟨ Finset.mem_univ _, fun hx' => Finset.mem_filter.mp hx |>.2 <| hS₂.choose_spec.2 x hx' ⟩;
    · rw [ Finset.card_sdiff ] ; simp +decide;
  by_cases h_card : Fintype.card ι = 0;
  · simp_all +decide [ Fintype.card_eq_zero_iff ];
    exact False.elim ( hS₃ _ hS₂.choose_spec.1 _ hS₂.choose_spec.1 );
  · rw [ relDist, div_le_iff₀ ];
    · exact le_trans ( Nat.cast_le.mpr h_numDiff ) ( by rw [ Nat.cast_sub ( show S.card ≤ Fintype.card ι from le_trans ( Finset.card_le_univ _ ) ( by simp +decide ) ) ] ; nlinarith );
    · positivity

/-
**Case (a): close pairs.**  Let `C` be a submodule of minimum weight `w`
with `2r ≤ w-1` (`r := ⌊δ·n⌋`).  If a pair `(f₁,f₂)` is `δ`-close to the
interleaved code, witnessed by codewords `p₁,p₂` with column-error set `E`
(`|E| ≤ r`), then every MCA-bad slope is a tangent ratio `-e₁ⱼ/e₂ⱼ` for some
`j ∈ E` with `e₂ⱼ ≠ 0`, where `eᵢ = fᵢ - pᵢ`.  In particular the set of MCA-bad
slopes has at most `r` elements.
-/
theorem mcaBad_close_tangent (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ)
    (h2r : 2 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1)
    (f1 f2 : ι → F) (p1 : ι → F) (hp1 : p1 ∈ C) (p2 : ι → F) (hp2 : p2 ∈ C)
    (hclose : relDist2 f1 f2 p1 p2 ≤ δ) :
    (Finset.univ.filter (fun γ => mcaBad (C : Set (ι → F)) δ f1 f2 γ)).card
      ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
  refine' le_trans ( Finset.card_le_card _ ) _;
  exact Finset.image ( fun j : ι => if f2 j = p2 j then 0 else - ( f1 j - p1 j ) / ( f2 j - p2 j ) ) ( Finset.univ.filter ( fun j => f2 j ≠ p2 j ) );
  · intro γ hγ
    obtain ⟨S, hS₁, hS₂, hS₃⟩ := (Finset.mem_filter.mp hγ).right
    obtain ⟨c, hc₁, hc₂⟩ := hS₂
    have h_eq : c = p1 + γ • p2 := by
      have h_eq : numDiff (c - (p1 + γ • p2)) 0 ≤ 2 * ⌊δ * (Fintype.card ι)⌋₊ := by
        have h_eq : numDiff (c - (p1 + γ • p2)) 0 ≤ (Fintype.card ι - S.card) + (Finset.univ.filter (fun j => f1 j ≠ p1 j ∨ f2 j ≠ p2 j)).card := by
          have h_eq : Finset.univ.filter (fun j => c j - (p1 j + γ * p2 j) ≠ 0) ⊆ Finset.univ \ S ∪ Finset.univ.filter (fun j => f1 j ≠ p1 j ∨ f2 j ≠ p2 j) := by
            grind;
          exact le_trans ( Finset.card_le_card h_eq ) ( Finset.card_union_le _ _ ) |> le_trans <| by simp +decide [ Finset.card_sdiff ] ;
        have h_eq : (Finset.univ.filter (fun j => f1 j ≠ p1 j ∨ f2 j ≠ p2 j)).card ≤ ⌊δ * (Fintype.card ι)⌋₊ := by
          unfold relDist2 at hclose;
          exact Nat.le_floor ( by rwa [ div_le_iff₀ ( Nat.cast_pos.mpr <| Fintype.card_pos_iff.mpr ⟨ Classical.choose <| Finset.card_pos.mp <| show 0 < Finset.card S from Nat.pos_of_ne_zero <| by aesop_cat ⟩ ) ] at hclose );
        have h_eq : (Fintype.card ι - S.card) ≤ ⌊δ * (Fintype.card ι)⌋₊ := by
          exact Nat.le_floor <| by rw [ Nat.cast_sub <| show S.card ≤ Fintype.card ι from le_trans ( Finset.card_le_univ _ ) <| by simp +decide ] ; linarith;
        linarith;
      contrapose! h_eq;
      exact lt_of_lt_of_le ( Nat.lt_of_le_of_lt h2r ( Nat.pred_lt ( ne_bot_of_gt ( Nat.pos_of_ne_zero ( by
        intro h; simp_all +decide [ numDiff ] ;
        obtain ⟨ i, hi, hi' ⟩ := hS₃ p1 hp1 p2 hp2 ; specialize hc₂ i hi ; specialize hS₃ ( p1 + γ • p2 ) ( C.add_mem hp1 ( C.smul_mem γ hp2 ) ) ( p1 + γ • p2 ) ( C.add_mem hp1 ( C.smul_mem γ hp2 ) ) ; simp_all +decide [ funext_iff ] ;
        have h_contra : (Finset.univ.filter (fun i => f1 i ≠ p1 i ∨ f2 i ≠ p2 i)).card ≤ ⌊δ * (Fintype.card ι)⌋₊ := by
          have h_contra : (Finset.univ.filter (fun i => f1 i ≠ p1 i ∨ f2 i ≠ p2 i)).card / (Fintype.card ι : ℝ) ≤ δ := by
            convert hclose using 1;
          exact Nat.le_floor <| by rwa [ div_le_iff₀ <| Nat.cast_pos.mpr <| Fintype.card_pos_iff.mpr ⟨ i ⟩ ] at h_contra;
        simp_all +decide [ Nat.floor_eq_zero.mpr h2r ] ) ) ) ) ) ( hw _ ( by
        exact C.sub_mem hc₁ ( C.add_mem hp1 ( C.smul_mem γ hp2 ) ) ) ( sub_ne_zero_of_ne h_eq ) );
    simp_all +decide;
    grind;
  · refine' le_trans ( Finset.card_image_le ) _;
    contrapose! hclose;
    refine' lt_of_lt_of_le _ ( div_le_div_of_nonneg_right ( Nat.cast_le.mpr <| Finset.card_mono <| show Finset.filter ( fun j => f2 j ≠ p2 j ) Finset.univ ⊆ Finset.filter ( fun j => f1 j ≠ p1 j ∨ f2 j ≠ p2 j ) Finset.univ from fun x hx => by aesop ) <| Nat.cast_nonneg _ );
    rw [ lt_div_iff₀ ] <;> norm_cast;
    · exact Nat.lt_of_floor_lt hclose;
    · exact Fintype.card_pos_iff.mpr ( by contrapose! hclose; aesop )

/-
**Theorem `thm:mca-from-ca`.**  For an `F`-linear code `C` of minimum
Hamming weight `w`, with `r := ⌊δ·n⌋` and `2r ≤ w-1`,

  `ε_mca(C, δ) ≤ max (ε_ca(C, δ), r/q)`.
-/
theorem emca_le_max_eca_tangent (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ)
    (h2r : 2 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1) :
    emcaErr (C : Set (ι → F)) δ
      ≤ max (ecaErr (C : Set (ι → F)) δ δ)
          ((⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) / (Fintype.card F)) := by
  -- By definition of `emcaErr`, it suffices to show that for any pair `(f1, f2)`, the probability of `mcaBad` is bounded by `max (ecaErr C δ δ) (r/q)`.
  suffices h : ∀ (f1 f2 : ι → F), prob (fun γ : F => mcaBad (C : Set (ι → F)) δ f1 f2 γ) ≤
    max (ecaErr (C : Set (ι → F)) δ δ) ((⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) / (Fintype.card F : ℝ)) by
      exact Finset.sup'_le _ _ fun p hp => h p.1 p.2;
  intro f1 f2
  by_cases hclose : intClose (C : Set (ι → F)) δ f1 f2;
  · obtain ⟨ p1, hp1, p2, hp2, hclose ⟩ := hclose;
    refine' le_trans _ ( le_max_right _ _ );
    exact div_le_div_of_nonneg_right ( mod_cast mcaBad_close_tangent C hw δ h2r f1 f2 p1 hp1 p2 hp2 hclose ) ( Nat.cast_nonneg _ );
  · refine' le_trans _ ( le_max_left _ _ );
    refine' le_trans _ ( Finset.le_sup' _ ( Finset.mem_univ ( f1, f2 ) ) );
    exact prob_mono fun γ hγ => mcaBad_far_imp_caBad _ _ _ _ _ hclose hγ

/-- **Corollary `cor:band-reduction`.**  Any correlated-agreement bound
`ε_ca(C,δ) ≤ ε` upgrades to `ε_mca(C,δ) ≤ max (ε, r/q)` below half the distance. -/
theorem emca_le_of_eca_le (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ)
    (h2r : 2 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1)
    {ε : ℝ} (hε : ecaErr (C : Set (ι → F)) δ δ ≤ ε) :
    emcaErr (C : Set (ι → F)) δ
      ≤ max ε ((⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) / (Fintype.card F)) := by
  refine le_trans (emca_le_max_eca_tangent C hw δ h2r) ?_
  exact max_le_max hε le_rfl

end RSCap