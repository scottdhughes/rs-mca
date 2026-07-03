import cs25_cap_v12.SafeSide

set_option maxHeartbeats 8000000

/-!
# The deep regime: unconditional mutual correlated agreement

This file formalizes the paper's

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*,

**deep-regime mutual correlated agreement, unconditional** (`thm:deep-mca`).

For an `F`-linear code `C ⊆ Fⁿ` of minimum Hamming weight `w`, writing
`r := ⌊δ·n⌋`, if `3r ≤ w-1` (one third of the distance) then

  `ε_ca(C, δ) ≤ (r+1)/q`   and   `ε_mca(C, δ) ≤ (r+1)/q`.

The heart is the **close-slope dichotomy**: each pair `(f₁,f₂)` is either
*tangent* (column-close to `C^{≡2}`, so no CA-bad and `≤ r` MCA-bad slopes) or
*generic* (at most `r+1` slopes `γ` with `f₁+γf₂` close to `C`).  The generic
alternative comes from a rider double count on the recovered line.
-/

namespace RSCap

open Classical

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-
The set of *close slopes* of a pair: those `γ` for which `f₁+γf₂` is
`δ`-close to `C`.
-/
omit [Fintype F] in
theorem mcaBad_imp_caClose (C : Set (ι → F)) (δ : ℝ) (f1 f2 : ι → F) (γ : F)
    (h : mcaBad C δ f1 f2 γ) : caClose C δ (fun i => f1 i + γ * f2 i) := by
  obtain ⟨ S, hS, hc, hne ⟩ := h;
  obtain ⟨ c, hc, hc' ⟩ := hc;
  refine' ⟨ c, hc, _ ⟩;
  unfold relDist;
  rw [ div_le_iff₀ ];
  · have h_numDiff : numDiff (fun i => f1 i + γ * f2 i) c ≤ (Fintype.card ι : ℕ) - S.card := by
      exact Finset.card_le_card ( show Finset.filter ( fun i => f1 i + γ * f2 i ≠ c i ) Finset.univ ⊆ Finset.univ \ S from fun i hi => Finset.mem_sdiff.mpr ⟨ Finset.mem_univ _, fun hi' => Finset.mem_filter.mp hi |>.2 <| hc' i hi' ⟩ ) |> le_trans <| by simp +decide [ Finset.card_sdiff ] ;
    exact le_trans ( Nat.cast_le.mpr h_numDiff ) ( by rw [ Nat.cast_sub ( show S.card ≤ Fintype.card ι from le_trans ( Finset.card_le_univ _ ) ( by simp +decide ) ) ] ; nlinarith );
  · exact Nat.cast_pos.mpr ( Fintype.card_pos_iff.mpr ⟨ Classical.choose ( show ∃ i, i ∈ S from Finset.nonempty_of_ne_empty ( by aesop_cat ) ) ⟩ )

/-
**The close-slope dichotomy (core of `thm:deep-mca`).**  Let `C` be a
submodule of minimum weight `w`, `r := ⌊δ·n⌋`, and `3r ≤ w-1`.  Then every pair
`(f₁,f₂)` is either column-`δ`-close to the interleaved code (tangent), or has at
most `r+1` close slopes.
-/
theorem close_slope_dichotomy (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ) (hδ : 0 ≤ δ)
    (h3r : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1)
    (f1 f2 : ι → F) :
    intClose (C : Set (ι → F)) δ f1 f2 ∨
      (Finset.univ.filter
        (fun γ => caClose (C : Set (ι → F)) δ (fun i => f1 i + γ * f2 i))).card
        ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊ + 1 := by
  by_contra h_contra;
  -- Let Scl := Finset.univ.filter (fun γ => caClose (C:Set) δ (fun i => f1 i + γ*f2 i)).
  set Scl := Finset.univ.filter (fun γ : F => caClose (C : Set (ι → F)) δ (fun i => f1 i + γ * f2 i)) with hScl_def
  have hScl_card : Scl.card ≥ 2 := by
    grind;
  -- For each γ ∈ Scl, `caClose` gives a codeword p_γ ∈ C with relDist (f1+γf2) p_γ ≤ δ, so its error set has card ≤ r (numDiff (f1+γf2) p_γ ≤ δn, integer ≤ ⌊δn⌋ = r). Use choice to fix p_γ and let E_γ = univ.filter (fun i => f1 i + γ*f2 i ≠ p_γ i), |E_γ| ≤ r.
  obtain ⟨p, hp⟩ : ∃ p : F → ι → F, (∀ γ ∈ Scl, p γ ∈ C ∧ numDiff (fun i => f1 i + γ * f2 i) (p γ) ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊) := by
    have hp : ∀ γ ∈ Scl, ∃ p_γ ∈ C, numDiff (fun i => f1 i + γ * f2 i) p_γ ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
      intro γ hγ
      obtain ⟨p_γ, hp_γ⟩ : ∃ p_γ ∈ C, relDist (fun i => f1 i + γ * f2 i) p_γ ≤ δ := by
        aesop;
      refine' ⟨ p_γ, hp_γ.1, Nat.le_floor _ ⟩;
      convert mul_le_mul_of_nonneg_right hp_γ.2 ( Nat.cast_nonneg ( Fintype.card ι ) ) using 1;
      unfold relDist; by_cases h : Fintype.card ι = 0 <;> simp +decide [ h ] ;
      simp +decide [ numDiff ];
      exact fun x => False.elim <| h.not_gt <| Fintype.card_pos_iff.mpr ⟨ x ⟩;
    choose! p hp using hp; exact ⟨ p, fun γ hγ => hp γ hγ ⟩ ;
  -- Take p1 := p_{γ1}, p2 := p_{γ2}, E1, E2. Define (in the field, γ1 ≠ γ2 so γ1-γ2 ≠ 0):
  obtain ⟨γ1, γ2, hγ1, hγ2, hγ1γ2⟩ : ∃ γ1 γ2 : F, γ1 ∈ Scl ∧ γ2 ∈ Scl ∧ γ1 ≠ γ2 := by
    exact Finset.one_lt_card_iff.1 hScl_card;
  set c2 := (γ1 - γ2)⁻¹ • (p γ1 - p γ2) with hc2_def
  set c1 := p γ1 - γ1 • c2 with hc1_def
  set e1 := f1 - c1 with he1_def
  set e2 := f2 - c2 with he2_def
  set T := (Finset.univ.filter (fun i => e1 i ≠ 0 ∨ e2 i ≠ 0)) with hT_def
  have hT_card : T.card ≤ 2 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
    have hT_card : T.card ≤ (Finset.univ.filter (fun i => f1 i + γ1 * f2 i ≠ p γ1 i)).card + (Finset.univ.filter (fun i => f1 i + γ2 * f2 i ≠ p γ2 i)).card := by
      refine' le_trans ( Finset.card_le_card _ ) ( Finset.card_union_le _ _ );
      intro i hi; simp_all +decide [ sub_eq_iff_eq_add ] ;
      grind;
    exact hT_card.trans ( by rw [ two_mul ] ; exact add_le_add ( hp γ1 hγ1 |>.2 ) ( hp γ2 hγ2 |>.2 ) );
  -- For every γ ∈ Scl, the vector (fun i => e1 i + γ * e2 i) has numDiff to 0 at most r.
  have h_numDiff : ∀ γ ∈ Scl, numDiff (fun i => e1 i + γ * e2 i) 0 ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
    intro γ hγ
    have hz : (fun i => p γ i - (c1 i + γ * c2 i)) ∈ C := by
      convert C.sub_mem ( hp γ hγ |>.1 ) ( C.add_mem ( C.sub_mem ( hp γ1 hγ1 |>.1 ) ( C.smul_mem γ1 ( C.smul_mem ( ( γ1 - γ2 ) ⁻¹ ) ( C.sub_mem ( hp γ1 hγ1 |>.1 ) ( hp γ2 hγ2 |>.1 ) ) ) ) ) ( C.smul_mem γ ( C.smul_mem ( ( γ1 - γ2 ) ⁻¹ ) ( C.sub_mem ( hp γ1 hγ1 |>.1 ) ( hp γ2 hγ2 |>.1 ) ) ) ) ) using 1
    have hz_zero : (fun i => p γ i - (c1 i + γ * c2 i)) = 0 := by
      have hz_zero : numDiff (fun i => p γ i - (c1 i + γ * c2 i)) 0 ≤ 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
        have hz_zero : numDiff (fun i => p γ i - (c1 i + γ * c2 i)) 0 ≤ T.card + numDiff (fun i => f1 i + γ * f2 i) (p γ) := by
          refine' le_trans _ ( Finset.card_union_le _ _ );
          refine' Finset.card_le_card _;
          intro i hi; by_cases hi' : e1 i = 0 <;> by_cases hi'' : e2 i = 0 <;> simp_all +decide [ sub_eq_iff_eq_add ] ;
          exact Ne.symm hi;
        linarith [ hp γ hγ ];
      exact Classical.not_not.1 fun h => not_lt_of_ge ( hw _ hz h ) ( lt_of_le_of_lt hz_zero ( lt_of_le_of_lt h3r ( Nat.pred_lt ( ne_bot_of_gt ( show 0 < w from Nat.pos_of_ne_zero ( by
                                                                                                                                                  rintro rfl; simp_all +decide [ numDiff ] ;
                                                                                                                                                  simp_all +decide [ Nat.floor_eq_zero.mpr h3r ];
                                                                                                                                                  exact h rfl ) ) ) ) ) )
    have hz_eq : ∀ i, e1 i + γ * e2 i = (f1 i + γ * f2 i) - p γ i := by
      intro i; replace hz_zero := congr_fun hz_zero i; simp_all +decide [ sub_eq_iff_eq_add ] ; ring;
    have hz_card : numDiff (fun i => e1 i + γ * e2 i) 0 ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
      convert hp γ hγ |>.2 using 1;
      simp +decide [ numDiff, hz_eq ];
      simp +decide only [sub_eq_zero]
    exact hz_card;
  -- Now the dichotomy on |T|:
  by_cases hT_card_le_r : T.card ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊;
  · -- Since |T| ≤ r, we have relDist2 f1 f2 c1 c2 ≤ δ.
    have h_relDist2_le_δ : relDist2 f1 f2 c1 c2 ≤ δ := by
      have h_relDist2_le_δ : (T.card : ℝ) ≤ δ * (Fintype.card ι : ℝ) := by
        exact le_trans ( Nat.cast_le.mpr hT_card_le_r ) ( Nat.floor_le ( mul_nonneg hδ ( Nat.cast_nonneg _ ) ) );
      convert div_le_of_le_mul₀ _ _ h_relDist2_le_δ using 1 <;> norm_num;
      · unfold relDist2; simp +decide [ Finset.filter_or ] ;
        simp +decide [ T, e1, e2, sub_eq_zero ];
        simp +decide [ Finset.filter_or ];
      · exact hδ;
    refine' h_contra ( Or.inl ⟨ c1, _, c2, _, h_relDist2_le_δ ⟩ );
    · exact C.sub_mem ( hp γ1 hγ1 |>.1 ) ( C.smul_mem _ ( C.smul_mem _ ( C.sub_mem ( hp γ1 hγ1 |>.1 ) ( hp γ2 hγ2 |>.1 ) ) ) );
    · exact C.smul_mem _ ( C.sub_mem ( hp γ1 hγ1 |>.1 ) ( hp γ2 hγ2 |>.1 ) );
  · have h_double_count : ∑ j ∈ T, (Finset.filter (fun γ => e1 j + γ * e2 j = 0) Scl).card ≤ T.card := by
      have h_double_count : ∀ j ∈ T, (Finset.filter (fun γ => e1 j + γ * e2 j = 0) Scl).card ≤ 1 := by
        intro j hj
        by_cases he2j : e2 j = 0;
        · simp_all +decide [ Finset.ext_iff ];
        · exact Finset.card_le_one.mpr fun x hx y hy => mul_left_cancel₀ he2j <| by linear_combination ( Finset.mem_filter.mp hx |>.2 ) - ( Finset.mem_filter.mp hy |>.2 ) ;
      exact le_trans ( Finset.sum_le_sum h_double_count ) ( by simp +decide );
    have h_double_count : ∀ γ ∈ Scl, (Finset.filter (fun j => e1 j + γ * e2 j = 0) T).card ≥ T.card - ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
      intro γ hγ
      have h_numDiff_gamma : numDiff (fun i => e1 i + γ * e2 i) 0 ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊ := h_numDiff γ hγ
      have h_numDiff_gamma_T : (Finset.filter (fun j => e1 j + γ * e2 j ≠ 0) T).card ≤ ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
        refine' le_trans _ h_numDiff_gamma;
        exact Finset.card_mono fun x hx => by aesop;
      rw [ Finset.filter_not, Finset.card_sdiff ] at h_numDiff_gamma_T ; norm_num at *;
      rw [ add_comm ] ; exact h_numDiff_gamma_T.trans ( by rw [ Finset.inter_eq_left.mpr ( Finset.filter_subset _ _ ) ] ) ;
    have h_double_count : ∑ γ ∈ Scl, (Finset.filter (fun j => e1 j + γ * e2 j = 0) T).card ≤ T.card := by
      convert ‹∑ j ∈ T, Finset.card ( Finset.filter ( fun γ => e1 j + γ * e2 j = 0 ) Scl ) ≤ T.card› using 1;
      exact Finset.sum_card_bipartiteAbove_eq_sum_card_bipartiteBelow fun a b => e1 b + a * e2 b = 0;
    have h_double_count : ∑ γ ∈ Scl, (T.card - ⌊δ * (Fintype.card ι : ℝ)⌋₊) ≤ T.card := by
      exact le_trans ( Finset.sum_le_sum ‹_› ) h_double_count;
    simp +zetaDelta at *;
    nlinarith [ Nat.sub_add_cancel hT_card_le_r.le ]

/-
**`thm:deep-mca`, correlated-agreement bound.**  `ε_ca(C, δ) ≤ (r+1)/q`.
-/
theorem ecaErr_le_deep (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ) (hδ : 0 ≤ δ)
    (h3r : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1) :
    ecaErr (C : Set (ι → F)) δ δ
      ≤ ((⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) + 1) / (Fintype.card F) := by
  refine' Finset.sup'_le _ _ _;
  intro p hp
  by_cases h_intClose : intClose (C : Set (ι → F)) δ p.1 p.2;
  · unfold prob; simp_all +decide [ caBad ] ;
    positivity;
  · have := close_slope_dichotomy C hw δ hδ h3r p.1 p.2;
    simp_all +decide [ prob, caBad ];
    gcongr ; norm_cast

/-
**`thm:deep-mca`, mutual bound.**  `ε_mca(C, δ) ≤ (r+1)/q`.
-/
theorem emcaErr_le_deep (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ) (hδ : 0 ≤ δ)
    (h3r : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1) :
    emcaErr (C : Set (ι → F)) δ
      ≤ ((⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) + 1) / (Fintype.card F) := by
  convert emca_le_of_eca_le C hw δ _ _ using 1;
  rotate_left;
  grind;
  exact ( ⌊δ * ( Fintype.card ι : ℝ ) ⌋₊ + 1 ) / ( Fintype.card F : ℝ );
  · convert ecaErr_le_deep C hw δ hδ h3r using 1;
  · rw [ max_eq_left ( by gcongr ; linarith ) ]

end RSCap