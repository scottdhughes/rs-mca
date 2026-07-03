import Mathlib
import RS_disproof_v3.Main

/-!
# Scalar-coset extension towers (Paper A, `sec:extension-towers`)

This file finishes the extension-field tower section of

  P. Chojecki, *Capacity-Edge Obstructions to Reed-Solomon Mutual Correlated Agreement
  over Smooth Multiplicative Domains* (`RS_disproof_v3.tex`),

whose number-theoretic heart (the `2`-adic tower criterion, `lem:ext-tower-criterion`) is
formalized in `RS_disproof_v3.ExtensionTower`.  Here we formalize the *combinatorial* core:
the scalar-coset construction (`lem:ext-coset-subgroup`) and the two MCA obstructions it
yields, the full-density theorem (`thm:ext-smooth-towers`) and the box-density proposition
(`prop:ext-density`).

## Setup

Let `E / K` be a finite field extension of degree `d` with `K`-basis `b = (1, ζ, …, ζ^{d-1})`
(here recorded abstractly as any `Module.Basis (Fin d) K E`).  Let `H ⊆ K` be the order-`m`
subgroup of `K^×` (so `0 ∉ H`).  The paper's smooth domain

  `D = ⊔_{i=0}^{d-1} ζ^i H ≤ E^×`

is realized as `scalarCosetDomain b H`, the disjoint union of the scalar cosets
`ζ^i H = { h · ζ^i : h ∈ H } = { h • (b i) : h ∈ H }`.

## External input

Exactly as the rest of the project (see `RS_disproof_v3.Main`), the Dias da Silva–Hamidoune
coverage theorem is **not** in Mathlib and is *imported* by the paper.  We therefore take the
`H`-level (prime-field) restricted-sumset conclusions as hypotheses — full coverage
`r^{∧}H = (r+1)^{∧}H = K` for `thm:ext-smooth-towers`, and density
`|r^{∧}H|, |(r+1)^{∧}H| ≥ θ|K|` for `prop:ext-density` — and prove the (genuinely new) lift
of these `H`-level facts to the `E`-level restricted sumset `(k+1)^{∧}D` via the basis
box argument, and thence to the MCA error through the locator lower bound of `Main`.
-/

open Polynomial
open scoped BigOperators Classical
open Module

namespace RSLocator

variable {K E : Type*} [Field K] [Fintype K] [DecidableEq K]
  [Field E] [Fintype E] [DecidableEq E] [Algebra K E]

/-- The scalar coset `ζ^i · H = { h • (b i) : h ∈ H }`. -/
noncomputable def scalarCoset {d : ℕ} (b : Basis (Fin d) K E) (H : Finset K) (i : Fin d) : Finset E :=
  H.image (fun h => h • b i)

/-- The scalar-coset domain `D = ⊔_{i} ζ^i H`. -/
noncomputable def scalarCosetDomain {d : ℕ} (b : Basis (Fin d) K E) (H : Finset K) : Finset E :=
  Finset.univ.biUnion (fun i => scalarCoset b H i)

/- The scalar map `t ↦ t • (b i)` is injective (as `b i ≠ 0`). -/
omit [Fintype K] [DecidableEq K] [Fintype E] [DecidableEq E] in
lemma smul_basis_injective {d : ℕ} (b : Basis (Fin d) K E) (i : Fin d) :
    Function.Injective (fun t : K => t • b i) :=
  smul_left_injective K (b.ne_zero i)

/-
Each scalar coset has exactly `|H|` elements.
-/
omit [Fintype K] [DecidableEq K] [Fintype E] in
lemma scalarCoset_card {d : ℕ} (b : Basis (Fin d) K E) (H : Finset K) (i : Fin d) :
    (scalarCoset b H i).card = H.card := by
  exact Finset.card_image_of_injective _ ( smul_basis_injective b i )

/-
Distinct scalar cosets are disjoint (uses `0 ∉ H` and basis independence).
-/
omit [Fintype K] [DecidableEq K] [Fintype E] in
lemma scalarCoset_disjoint {d : ℕ} (b : Basis (Fin d) K E) (H : Finset K)
    (h0 : (0 : K) ∉ H) {i j : Fin d} (hij : i ≠ j) :
    Disjoint (scalarCoset b H i) (scalarCoset b H j) := by
  simp +decide [ scalarCoset, Finset.disjoint_left ];
  intro a ha x hx h; have := b.linearIndependent; simp_all +decide [ linearIndependent_iff' ] ;
  specialize this { i, j } ( fun k => if k = i then -a else if k = j then x else 0 ) ; simp_all +decide [ Finset.sum_ite, Finset.filter_ne', Finset.filter_eq' ]

/-
The scalar-coset domain has `d · |H|` elements.
-/
omit [Fintype K] [DecidableEq K] [Fintype E] in
lemma scalarCosetDomain_card {d : ℕ} (b : Basis (Fin d) K E) (H : Finset K)
    (h0 : (0 : K) ∉ H) :
    (scalarCosetDomain b H).card = d * H.card := by
  rw [ scalarCosetDomain, Finset.card_biUnion ];
  · simp +decide [ scalarCoset_card ];
  · exact fun i _ j _ hij => scalarCoset_disjoint b H h0 hij

/-
**Box membership (core of the scalar-coset argument).**
Given per-coordinate subsets `T i ⊆ H`, the field element `∑_i (∑_{t ∈ T i} t) • (b i)` is a
sum of `∑_i |T i|` distinct elements of `D = scalarCosetDomain b H`, hence lies in the
restricted sumset `(∑_i |T i|)^{∧}D`.
-/
omit [Fintype K] [DecidableEq K] [Fintype E] in
lemma box_mem_restrictedSumset {d : ℕ} (b : Basis (Fin d) K E) (H : Finset K)
    (h0 : (0 : K) ∉ H) (T : Fin d → Finset K) (hTsub : ∀ i, T i ⊆ H) :
    (∑ i, (∑ t ∈ T i, t) • b i) ∈
      restrictedSumset (scalarCosetDomain b H) (∑ i, (T i).card) := by
  refine' Finset.mem_image.mpr ⟨ Finset.biUnion Finset.univ fun i => ( T i ).image ( fun t => t • b i ), _, _ ⟩;
  · refine' Finset.mem_powersetCard.mpr ⟨ _, _ ⟩;
    · exact Finset.biUnion_subset.mpr fun i _ => Finset.image_subset_iff.mpr fun t ht => Finset.mem_biUnion.mpr ⟨ i, Finset.mem_univ _, Finset.mem_image_of_mem _ ( hTsub i ht ) ⟩;
    · rw [ Finset.card_biUnion ];
      · exact Finset.sum_congr rfl fun i _ => Finset.card_image_of_injective _ ( smul_basis_injective b i );
      · intro i _ j _ hij; have := scalarCoset_disjoint b H h0 hij; simp_all +decide [ Finset.disjoint_left ] ;
        intro a ha x hx; contrapose! this; simp_all +decide [ scalarCoset ] ;
        exact ⟨ a, hTsub i ha, x, hTsub j hx, this ⟩;
  · rw [ Finset.sum_biUnion ];
    · simp +decide [ Finset.sum_smul ];
      exact Finset.sum_congr rfl fun i _ => Finset.sum_image <| by intro x hx y hy hxy; simpa [ b.ne_zero ] using smul_basis_injective b i hxy;
    · intro i _ j _ hij;
      exact Finset.disjoint_left.mpr fun x hx₁ hx₂ => by obtain ⟨ t₁, ht₁, rfl ⟩ := Finset.mem_image.mp hx₁; obtain ⟨ t₂, ht₂, h ⟩ := Finset.mem_image.mp hx₂; have := scalarCoset_disjoint b H h0 hij; exact Finset.disjoint_left.mp this ( Finset.mem_image_of_mem _ ( hTsub i ht₁ ) ) ( Finset.mem_image.mpr ⟨ t₂, hTsub j ht₂, h ⟩ ) ;

/-- The per-coordinate size vector: coordinate `0` carries `r + 1`, the others carry `r`. -/
def cosetSizes {d : ℕ} [NeZero d] (r : ℕ) (i : Fin d) : ℕ := if i = 0 then r + 1 else r

/-
The total size `∑_i cosetSizes r i = r·d + 1`.
-/
lemma sum_cosetSizes {d : ℕ} [NeZero d] (r : ℕ) : ∑ i, cosetSizes (d := d) r i = r * d + 1 := by
  unfold cosetSizes; simp +decide [ mul_comm, Finset.sum_ite, Finset.filter_eq', Finset.filter_ne' ] ;
  cases d <;> norm_num at * ; linarith!;

/-
**Scalar-coset coverage (`thm:ext-smooth-towers`, combinatorial step).**
If both `r^{∧}H` and `(r+1)^{∧}H` cover the whole scalar field `K`, then `(r·d+1)^{∧}D` covers
the whole extension field `E`.
-/
theorem scalarCoset_cover {d : ℕ} [NeZero d] (b : Basis (Fin d) K E) (H : Finset K)
    (h0 : (0 : K) ∉ H) (r : ℕ)
    (hr1 : restrictedSumset H (r + 1) = Finset.univ)
    (hr : restrictedSumset H r = Finset.univ) :
    restrictedSumset (scalarCosetDomain b H) (r * d + 1) = Finset.univ := by
  -- By definition of $T$, we have that $\sum_{i} (\sum_{t \in T_i} t) • b_i = y$.
  have h_sum : ∀ y : E, ∃ T : Fin d → Finset K, (∀ i, T i ⊆ H) ∧ (∀ i, (T i).card = cosetSizes r i) ∧ y = Finset.sum Finset.univ (fun i => (Finset.sum (T i) id) • b i) := by
    intro y
    obtain ⟨T, hT⟩ : ∃ T : Fin d → Finset K, (∀ i, T i ⊆ H) ∧ (∀ i, (T i).card = cosetSizes r i) ∧ ∀ i, (∑ t ∈ T i, t) = (b.repr y) i := by
      have hT : ∀ i : Fin d, ∀ x : K, x ∈ restrictedSumset H (cosetSizes r i) := by
        intro i x; by_cases hi : i = 0 <;> simp_all +decide [ cosetSizes ] ;
      simp_all +decide [ restrictedSumset ];
      exact ⟨ fun i => Classical.choose ( hT i ( b.repr y i ) ), fun i => Classical.choose_spec ( hT i ( b.repr y i ) ) |>.1.1, fun i => Classical.choose_spec ( hT i ( b.repr y i ) ) |>.1.2, fun i => Classical.choose_spec ( hT i ( b.repr y i ) ) |>.2 ⟩;
    refine' ⟨ T, hT.1, hT.2.1, _ ⟩;
    conv_lhs => rw [ ← b.sum_repr y ];
    exact Finset.sum_congr rfl fun i _ => by rw [ ← hT.2.2 i ] ; rfl;
  refine' Finset.eq_univ_of_forall _;
  intro y
  obtain ⟨T, hT_sub, hT_card, hy⟩ := h_sum y
  have hT_sum : (∑ i, (∑ t ∈ T i, t) • b i) ∈ restrictedSumset (scalarCosetDomain b H) (∑ i, (T i).card) := by
    apply box_mem_restrictedSumset b H h0 T hT_sub;
  simp_all +decide [ sum_cosetSizes ]

/-
**Box (`prop:ext-density`, combinatorial step).**
The `E`-restricted sumset `(r·d+1)^{∧}D` contains a `K`-basis box of size
`|(r+1)^{∧}H| · |r^{∧}H|^{d-1} = ∏_i |cosetSizes r i ^{∧} H|`, whose cardinality is exactly
this product because the basis coordinate map is injective.
-/
omit [Fintype K] [Fintype E] in
theorem card_box_le_restrictedSumset {d : ℕ} [NeZero d] (b : Basis (Fin d) K E) (H : Finset K)
    (h0 : (0 : K) ∉ H) (r : ℕ) :
    (∏ i, (restrictedSumset H (cosetSizes (d := d) r i)).card) ≤
      (restrictedSumset (scalarCosetDomain b H) (r * d + 1)).card := by
  -- To show B ⊆ restrictedSumset, B ⊆ Dom^{r·d + 1}.
  have hB_subset : ∀ c ∈ Fintype.piFinset (fun i => restrictedSumset H (cosetSizes r i)), (∑ i, c i • b i) ∈ restrictedSumset (scalarCosetDomain b H) (r * d + 1) := by
    intro c hc;
    obtain ⟨T, hT⟩ : ∃ T : Fin d → Finset K, (∀ i, T i ⊆ H) ∧ (∀ i, (T i).card = cosetSizes r i) ∧ (∀ i, ∑ t ∈ T i, t = c i) := by
      simp_all +decide [ Fintype.mem_piFinset ];
      exact ⟨ fun i => Classical.choose ( Finset.mem_image.mp ( hc i ) ), fun i => Classical.choose_spec ( Finset.mem_image.mp ( hc i ) ) |>.1 |> fun h => Finset.mem_powersetCard.mp h |>.1, fun i => Classical.choose_spec ( Finset.mem_image.mp ( hc i ) ) |>.1 |> fun h => Finset.mem_powersetCard.mp h |>.2, fun i => Classical.choose_spec ( Finset.mem_image.mp ( hc i ) ) |>.2 ⟩;
    convert box_mem_restrictedSumset b H h0 T hT.1 using 1;
    · rw [ Finset.sum_congr rfl fun i _ => hT.2.1 i, sum_cosetSizes ];
    · aesop;
  refine' le_trans _ ( Finset.card_le_card <| show ( Finset.image ( fun c : Fin d → K => ∑ i, c i • b i ) ( Fintype.piFinset fun i => restrictedSumset H ( cosetSizes r i ) ) ) ⊆ restrictedSumset ( scalarCosetDomain b H ) ( r * d + 1 ) from fun x hx => by aesop );
  rw [ Finset.card_image_of_injective ];
  · rw [ Fintype.card_piFinset ];
  · exact fun c d h => by simpa [ funext_iff ] using b.equivFun.symm.injective <| by simpa [ funext_iff ] using h;

/-
The extension degree equals the ambient field-size ratio: `|E| = |K|^d`.
-/
omit [DecidableEq K] [DecidableEq E] in
lemma card_ext {d : ℕ} (b : Basis (Fin d) K E) :
    Fintype.card E = Fintype.card K ^ d := by
  convert ( Module.card_fintype b );
  simp +decide

/-
**Smooth extension towers: full density (`thm:ext-smooth-towers`).**
Under full Dias da Silva–Hamidoune coverage of the scalar subgroup `H` (both at sizes `r` and
`r+1`), the MCA error of `RS[E, D, k]` with `k = r·d` equals `1` at every radius
`δ ≥ 1 - ρ - 1/n` (`n = |D| = d·|H|`).
-/
theorem thm_ext_smooth_towers {d : ℕ} [NeZero d] (b : Basis (Fin d) K E) (H : Finset K)
    (h0 : (0 : K) ∉ H) (r : ℕ) (hrH : r + 1 ≤ H.card)
    (hr1 : restrictedSumset H (r + 1) = Finset.univ)
    (hr : restrictedSumset H r = Finset.univ)
    (k : ℕ) (hk : k = r * d)
    (δ : ℝ) (hδ : (1 - δ) * ((scalarCosetDomain b H).card : ℝ) ≤ (k + 1 : ℝ)) :
    epsMca (scalarCosetDomain b H) k δ = 1 := by
  apply epsMca_eq_one_of_cover_full;
  rotate_right;
  exact r * d + 1;
  · exact Nat.succ_pos _;
  · rw [ scalarCosetDomain_card b H h0 ] ; nlinarith [ NeZero.pos d ];
  · exact hk;
  · exact scalarCoset_cover b H h0 r hr1 hr;
  · exact hδ

/-
**Box-density extension bound (`prop:ext-density`).**
Without full coverage, if `|r^{∧}H|, |(r+1)^{∧}H| ≥ θ·|K|` for some `0 ≤ θ`, then the MCA error
of `RS[E, D, k]` with `k = r·d` is at least `θ^d` at every radius `δ ≥ 1 - ρ - 1/n`.
-/
theorem prop_ext_density {d : ℕ} [NeZero d] (b : Basis (Fin d) K E) (H : Finset K)
    (h0 : (0 : K) ∉ H) (r : ℕ) (hrH : r + 1 ≤ H.card)
    (θ : ℝ) (hθ0 : 0 ≤ θ)
    (hr1 : θ * (Fintype.card K : ℝ) ≤ ((restrictedSumset H (r + 1)).card : ℝ))
    (hr : θ * (Fintype.card K : ℝ) ≤ ((restrictedSumset H r).card : ℝ))
    (k : ℕ) (hk : k = r * d)
    (δ : ℝ) (hδ : (1 - δ) * ((scalarCosetDomain b H).card : ℝ) ≤ (k + 1 : ℝ)) :
    θ ^ d ≤ epsMca (scalarCosetDomain b H) k δ := by
  have := @epsMca_ge_restrictedSumset_full E;
  refine' le_trans _ ( this _ _ _ _ _ _ δ hδ );
  any_goals exact r * d + 1;
  · refine' le_trans _ ( div_le_div_of_nonneg_right ( Nat.cast_le.mpr ( card_box_le_restrictedSumset b H h0 r ) ) ( Nat.cast_nonneg _ ) );
    rw [ le_div_iff₀ ( Nat.cast_pos.mpr <| Fintype.card_pos ) ];
    rw [ card_ext b ];
    push_cast [ ← mul_pow ];
    refine' le_trans _ ( Finset.prod_le_prod _ fun i _ => show ( restrictedSumset H ( cosetSizes r i ) |> Finset.card : ℝ ) ≥ θ * Fintype.card K from _ );
    · rw [ Finset.prod_const, Finset.card_fin ];
    · exact fun _ _ => mul_nonneg hθ0 ( Nat.cast_nonneg _ );
    · unfold cosetSizes; aesop;
  · exact Nat.succ_pos _;
  · rw [ scalarCosetDomain_card b H h0 ] ; nlinarith [ NeZero.pos d ];
  · exact hk

end RSLocator
