import cs25_cap_v12.DeepMCA
import cs25_cap_v12.Johnson

set_option maxHeartbeats 8000000

/-!
# Threshold certificate interface: small-field degeneracy and scanner soundness

This file formalizes the parts of the *threshold formulation and certificate
interface* / *certificate scanner* sections of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*,

that are self-contained given the previously formalized error definitions and the
deep-regime theorem:

* `RSCap.emca_ge_inv_q` — **small-field degeneracy** (`prop:small-field`): every
  proper linear code has `ε_mca(C,δ) ≥ 1/q` for every `δ ∈ [0,1]`.
* `RSCap.dStar_eq_zero_of_small_field` — the degeneracy consequence
  `δ*_C(ε*) = 0` whenever `ε* < 1/q`.
* `RSCap.scanner_deep_safe` — the **scanner soundness** *Deep-safe* verdict
  (`thm:scanner-sound`, V3): if `3⌊δn⌋ ≤ w-1` and `⌊δn⌋+1 ≤ ε*·q` then
  `ε_mca(C,δ) ≤ ε*`; the corresponding sound CA verdict is `scanner_deep_safe_ca`.
-/

namespace RSCap

open Classical

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-
**Small-field degeneracy (`prop:small-field`).**  For any proper linear code
`C ⊊ Fⁿ` and any radius `δ ≥ 0`, `ε_mca(C, δ) ≥ 1/q`.  Witness: the pair
`(0, f₂)` with `f₂ ∉ C` has the MCA-bad slope `γ = 0` on the full support `D`.
-/
theorem emca_ge_inv_q (C : Submodule F (ι → F)) (hC : ∃ v : ι → F, v ∉ C)
    (δ : ℝ) (hδ0 : 0 ≤ δ) :
    (1 : ℝ) / (Fintype.card F) ≤ emcaErr (C : Set (ι → F)) δ := by
  -- Extract f2 with f2 ∉ C from hC. Consider the pair (f1, f2) := ((0 : ι → F), f2).
  obtain ⟨f2, hf2⟩ : ∃ f2 : ι → F, f2 ∉ C := hC
  set f1 : ι → F := (0 : ι → F);
  -- Claim: γ = 0 is MCA-bad, i.e. `mcaBad (C:Set) δ (0:ι→F) f2 0` holds.
  have h_mcaBad : mcaBad (C : Set (ι → F)) δ f1 f2 0 := by
    refine' ⟨ Finset.univ, _, _, _ ⟩ <;> norm_num;
    · exact mul_le_of_le_one_left ( Nat.cast_nonneg _ ) ( sub_le_self _ hδ0 );
    · exact ⟨ 0, C.zero_mem, fun _ => rfl ⟩;
    · contrapose! hf2;
      obtain ⟨ x, hx, y, hy, h ⟩ := hf2; convert hy; ext i; specialize h i; aesop;
  refine' le_trans _ ( Finset.le_sup' _ ( show ( f1, f2 ) ∈ Finset.univ from Finset.mem_univ _ ) );
  refine' div_le_div_of_nonneg_right _ ( Nat.cast_nonneg _ );
  exact_mod_cast Finset.card_pos.mpr ⟨ 0, Finset.mem_filter.mpr ⟨ Finset.mem_univ _, h_mcaBad ⟩ ⟩

/-
**Degeneracy of the challenge threshold.**  If `ε* < 1/q` then
`δ*_C(ε*) = 0`: no sub-capacity radius is `ε*`-admissible, since every radius has
`ε_mca ≥ 1/q > ε*`.
-/
theorem dStar_eq_zero_of_small_field (C : Submodule F (ι → F))
    (hC : ∃ v : ι → F, v ∉ C) (ρ εstar : ℝ)
    (hεq : εstar < (1 : ℝ) / (Fintype.card F)) :
    dStar (C : Set (ι → F)) ρ εstar = 0 := by
  unfold dStar;
  convert Real.sSup_empty;
  ext δ;
  by_cases hδ : 0 ≤ δ <;> by_cases hδ' : δ ≤ 1 <;> simp +decide;
  · exact fun _ _ => hεq.trans_le ( emca_ge_inv_q C hC δ hδ );
  · intro hδ_pos hδ_lt_1_minus_ρ
    have h_emca_ge_inv_q : 1 / (Fintype.card F : ℝ) ≤ emcaErr (C : Set (ι → F)) 1 := by
      apply emca_ge_inv_q C hC 1 (by norm_num);
    exact hεq.trans_le ( h_emca_ge_inv_q.trans ( emca_mono _ ( by linarith ) ) );
  · exact fun h => False.elim <| hδ h.le;
  · linarith

/-- **Scanner soundness — Deep-safe MCA verdict (`thm:scanner-sound`, V3).**
If `3⌊δn⌋ ≤ w-1` and the deep numerator `⌊δn⌋+1` fits under the budget,
`⌊δn⌋+1 ≤ ε*·q`, then `ε_mca(C,δ) ≤ ε*`. -/
theorem scanner_deep_safe (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ) (hδ : 0 ≤ δ)
    (h3r : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1)
    {εstar : ℝ} (hq : 0 < (Fintype.card F : ℝ))
    (hnum : (⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) + 1 ≤ εstar * (Fintype.card F)) :
    emcaErr (C : Set (ι → F)) δ ≤ εstar := by
  refine le_trans (emcaErr_le_deep C hw δ hδ h3r) ?_
  rw [div_le_iff₀ hq]; linarith

/-- **Scanner soundness — Deep-safe CA verdict.**  Same hypotheses give
`ε_ca(C,δ) ≤ ε*`. -/
theorem scanner_deep_safe_ca (C : Submodule F (ι → F)) {w : ℕ}
    (hw : ∀ z ∈ C, z ≠ (0 : ι → F) → w ≤ numDiff z (0 : ι → F))
    (δ : ℝ) (hδ : 0 ≤ δ)
    (h3r : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ w - 1)
    {εstar : ℝ} (hq : 0 < (Fintype.card F : ℝ))
    (hnum : (⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) + 1 ≤ εstar * (Fintype.card F)) :
    ecaErr (C : Set (ι → F)) δ δ ≤ εstar := by
  refine le_trans (ecaErr_le_deep C hw δ hδ h3r) ?_
  rw [div_le_iff₀ hq]; linarith

end RSCap