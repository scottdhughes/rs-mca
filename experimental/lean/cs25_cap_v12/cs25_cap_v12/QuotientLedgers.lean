import cs25_cap_v12.BlueprintCommon

/-!
# Blueprint: quotient support and image ledgers (`sec:quotient-support-upper`, `sec:quotient-distinct-parameter`)

Skeletons (proofs `sorry`) for the safe-side *upper-bound* ledgers of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

These bound the number of support-wise MCA-bad (or no-loss CA-bad) parameters whose
*witness support* belongs to a declared quotient-remainder support family, via the
"one support pays for at most one line / at most `d` curve parameters" principle.

Formalized here:

* `explainedOn`, `jointlyExplainedOn`, `tupleJointlyExplainedOn` — the support-wise
  explanation predicates.
* `lem_one_support_one_line` — `lem:one-support-one-line`: on a fixed support of size
  `≥ a ≥ k`, at most one finite slope is support-wise noncontained.
* `prop_support_family_line_ledger` — the aggregate line ledger
  `#{family-witnessed bad slopes} ≤ |𝒮|` (`prop:divisor-union-support-ledger`, line
  part; `prop:distinct-parameter-line-ledger`).
* `lem_one_support_d_curve` — `lem:one-support-d-curve`: one support pays for at most
  `d` degree-`d` power-curve parameters.
* `prop_support_family_curve_ledger` — the aggregate curve ledger `≤ d·|𝒮|`
  (`thm:exact-quotient-image-lcm-ledger`, degree bound part).
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- The word `w` is *explained on* the support `S` by the code `RS[F, D, k]`: some
codeword agrees with `w` on all of `S`. -/
def explainedOn (dom : ι → F) (k : ℕ) (w : ι → F) (S : Finset ι) : Prop :=
  ∃ p ∈ RSpoly dom k, ∀ x ∈ S, w x = p x

/-- The pair `(f, g)` is *jointly explained on* `S`: some pair of codewords agrees with
`f` and `g` respectively on all of `S`. -/
def jointlyExplainedOn (dom : ι → F) (k : ℕ) (f g : ι → F) (S : Finset ι) : Prop :=
  ∃ pf ∈ RSpoly dom k, ∃ pg ∈ RSpoly dom k, (∀ x ∈ S, f x = pf x) ∧ (∀ x ∈ S, g x = pg x)

/-- A `(d+1)`-tuple `f` is *jointly explained on* `S` by the interleaved code
`C^{≡(d+1)}`: each row is explained by a codeword on `S`. -/
def tupleJointlyExplainedOn (dom : ι → F) (k : ℕ) {d : ℕ} (f : Fin (d + 1) → ι → F)
    (S : Finset ι) : Prop :=
  ∀ i, ∃ p ∈ RSpoly dom k, ∀ x ∈ S, f i x = p x

/-
**`lem:one-support-one-line` — one support pays for at most one line parameter.**

For `C = RS[F, D, k]`, `a ≥ k`, and a fixed support `S` with `|S| ≥ a`, at most one
finite slope `z ∈ F` can be support-wise noncontained on `S` (i.e. `f + z·g` explained
on `S` while `(f, g)` is not jointly explained on `S`).
-/
theorem lem_one_support_one_line (dom : ι → F) {k a : ℕ} (S : Finset ι)
    (hak : k ≤ a) (hSa : a ≤ S.card) (f g : ι → F) :
    (Finset.univ.filter (fun z : F =>
        explainedOn dom k (fun x => f x + z * g x) S ∧
          ¬ jointlyExplainedOn dom k f g S)).card ≤ 1 := by
  by_contra! h_contra;
  obtain ⟨z₁, z₂, hz₁, hz₂, hne⟩ : ∃ z₁ z₂ : F, z₁ ≠ z₂ ∧ explainedOn dom k (fun x => f x + z₁ * g x) S ∧ explainedOn dom k (fun x => f x + z₂ * g x) S ∧ ¬jointlyExplainedOn dom k f g S := by
    obtain ⟨ z₁, hz₁, z₂, hz₂, hne ⟩ := Finset.one_lt_card.mp h_contra; use z₁, z₂; aesop;
  obtain ⟨p₁, hp₁⟩ := hz₂
  obtain ⟨p₂, hp₂⟩ := hne.left;
  obtain ⟨Q₁, hQ₁⟩ := hp₁.left
  obtain ⟨Q₂, hQ₂⟩ := hp₂.left;
  refine' hne.2 ⟨ fun i => eval ( dom i ) ( Q₁ - Polynomial.C ( z₁ * ( z₁ - z₂ ) ⁻¹ ) * ( Q₁ - Q₂ ) ), _, fun i => eval ( dom i ) ( Polynomial.C ( ( z₁ - z₂ ) ⁻¹ ) * ( Q₁ - Q₂ ) ), _, _ ⟩ <;> simp_all +decide;
  · refine' ⟨ Q₁ - Polynomial.C ( z₁ * ( z₁ - z₂ ) ⁻¹ ) * ( Q₁ - Q₂ ), _, _ ⟩ <;> simp_all +decide;
    refine' lt_of_le_of_lt ( Polynomial.degree_sub_le _ _ ) _ ; simp_all +decide [ Polynomial.degree_mul ];
    exact lt_of_le_of_lt ( add_le_add_three ( Polynomial.degree_C_le ) ( Polynomial.degree_C_le ) ( Polynomial.degree_sub_le _ _ ) ) ( by aesop );
  · refine' ⟨ Polynomial.C ( z₁ - z₂ ) ⁻¹ * ( Q₁ - Q₂ ), _, _ ⟩ <;> simp_all +decide;
    exact lt_of_le_of_lt ( add_le_add ( Polynomial.degree_C_le ) ( Polynomial.degree_sub_le _ _ ) ) ( by aesop );
  · grind

/-
**`prop:divisor-union-support-ledger` / `prop:distinct-parameter-line-ledger`
(line part).**

For any support family `𝒮` all of whose members have size `≥ a ≥ k`, the number of
finite support-wise MCA-bad slopes witnessed by `𝒮` is at most `|𝒮|`.
-/
theorem prop_support_family_line_ledger (dom : ι → F) {k a : ℕ} (𝒮 : Finset (Finset ι))
    (hak : k ≤ a) (hfam : ∀ S ∈ 𝒮, a ≤ S.card) (f g : ι → F) :
    (Finset.univ.filter (fun z : F => ∃ S ∈ 𝒮,
        explainedOn dom k (fun x => f x + z * g x) S ∧
          ¬ jointlyExplainedOn dom k f g S)).card ≤ 𝒮.card := by
  refine' le_trans ( Finset.card_le_card _ ) _;
  exact Finset.biUnion 𝒮 fun S => Finset.filter ( fun z => explainedOn dom k ( fun x => f x + z * g x ) S ∧ ¬jointlyExplainedOn dom k f g S ) Finset.univ;
  · grind;
  · refine' le_trans ( Finset.card_biUnion_le ) _;
    exact le_trans ( Finset.sum_le_sum fun S hS => show Finset.card _ ≤ 1 from by simpa using lem_one_support_one_line dom S hak ( hfam S hS ) f g ) ( by simp +decide )

/-
**`lem:one-support-d-curve` — one support pays for at most `d` curve parameters.**

For a degree-`d` power curve `W_γ = f₀ + γ f₁ + ⋯ + γ^d f_d` and a fixed support `S`
with `|S| ≥ a ≥ k`, at most `d` parameters `γ` can be support-wise curve-noncontained
on `S`.
-/
theorem lem_one_support_d_curve (dom : ι → F) {k a d : ℕ} (S : Finset ι)
    (hak : k ≤ a) (hSa : a ≤ S.card) (f : Fin (d + 1) → ι → F) :
    (Finset.univ.filter (fun γ : F =>
        explainedOn dom k (fun x => ∑ i : Fin (d + 1), γ ^ (i : ℕ) * f i x) S ∧
          ¬ tupleJointlyExplainedOn dom k f S)).card ≤ d := by
  by_contra h_contra;
  -- Since $\neg tupleJointlyExplainedOn dom k f S$ holds, there exists some $i$ such that $f i$ is not explained on $S$.
  obtain ⟨i, hi⟩ : ∃ i : Fin (d + 1), ¬∃ p ∈ RSpoly dom k, ∀ x ∈ S, f i x = p x := by
    simp_all +decide [ tupleJointlyExplainedOn ];
    obtain ⟨ γ, hγ ⟩ := Finset.card_pos.mp ( pos_of_gt h_contra ) ; aesop;
  obtain ⟨γs, hγs⟩ : ∃ γs : Fin (d + 1) → F, Function.Injective γs ∧ ∀ j : Fin (d + 1), explainedOn dom k (fun x => ∑ i : Fin (d + 1), γs j ^ (i : ℕ) * f i x) S ∧ ¬ tupleJointlyExplainedOn dom k f S := by
    obtain ⟨γs, hγs⟩ : ∃ γs : Finset F, γs.card = d + 1 ∧ ∀ γ ∈ γs, explainedOn dom k (fun x => ∑ i : Fin (d + 1), γ ^ (i : ℕ) * f i x) S ∧ ¬ tupleJointlyExplainedOn dom k f S := by
      exact Exists.elim ( Finset.exists_subset_card_eq ( by linarith : d + 1 ≤ Finset.card ( Finset.filter ( fun γ => explainedOn dom k ( fun x => ∑ i : Fin ( d + 1 ), γ ^ ( i : ℕ ) * f i x ) S ∧ ¬ tupleJointlyExplainedOn dom k f S ) Finset.univ ) ) ) fun γs hγs => ⟨ γs, hγs.2, fun γ hγ => Finset.mem_filter.mp ( hγs.1 hγ ) |>.2 ⟩;
    have := Finset.equivFinOfCardEq hγs.1;
    exact ⟨ fun j => this.symm j, fun j j' h => by simpa [ Fin.ext_iff ] using h, fun j => hγs.2 _ <| this.symm j |>.2 ⟩;
  -- For each $j$, explainedness gives a codeword $p j ∈ RSpoly dom k$ with $∀ x ∈ S, (∑ i, (γs j)^(i:ℕ) * f i x) = p j x$.
  obtain ⟨p, hp⟩ : ∃ p : Fin (d + 1) → (ι → F), (∀ j : Fin (d + 1), p j ∈ RSpoly dom k) ∧ (∀ j : Fin (d + 1), ∀ x ∈ S, (∑ i : Fin (d + 1), γs j ^ (i : ℕ) * f i x) = p j x) := by
    choose p hp using fun j => hγs.2 j |>.1;
    exact ⟨ p, fun j => hp j |>.1, fun j x hx => hp j |>.2 x hx ⟩;
  -- The $(d+1)×(d+1)$ Vandermonde matrix $V j i = (γs j)^(i:ℕ)$ is invertible because the $γs j$ are pairwise distinct.
  obtain ⟨W, hW⟩ : ∃ W : Matrix (Fin (d + 1)) (Fin (d + 1)) F, W * Matrix.of (fun j i : Fin (d + 1) => γs j ^ (i : ℕ)) = 1 := by
    have h_vandermonde_inv : Matrix.det (Matrix.of (fun j i : Fin (d + 1) => γs j ^ (i : ℕ))) ≠ 0 := by
      erw [ Matrix.det_vandermonde ];
      exact Finset.prod_ne_zero_iff.mpr fun i hi => Finset.prod_ne_zero_iff.mpr fun j hj => sub_ne_zero_of_ne <| hγs.1.ne <| by aesop;
    exact ⟨ _, Matrix.nonsing_inv_mul _ <| show IsUnit _ from isUnit_iff_ne_zero.mpr h_vandermonde_inv ⟩;
  -- For each fixed $i$, on $S$: $f i x = ∑ j, W i j * (p j x)$ (invert the linear system $∑ i V j i · f i x = p j x$).
  have h_inv : ∀ x ∈ S, f i x = ∑ j : Fin (d + 1), W i j * p j x := by
    intro x hx
    have h_inv : ∑ j : Fin (d + 1), W i j * (∑ k : Fin (d + 1), γs j ^ (k : ℕ) * f k x) = f i x := by
      have h_inv : ∑ j : Fin (d + 1), W i j * (∑ k : Fin (d + 1), γs j ^ (k : ℕ) * f k x) = ∑ k : Fin (d + 1), (∑ j : Fin (d + 1), W i j * γs j ^ (k : ℕ)) * f k x := by
        simp +decide only [Finset.mul_sum _ _ _, Finset.sum_mul, mul_assoc];
        exact Finset.sum_comm;
      replace hW := congr_fun ( congr_fun hW i ) ; simp_all +decide [ Matrix.mul_apply ] ;
      simp +decide [ Matrix.one_apply ];
    exact h_inv.symm.trans ( Finset.sum_congr rfl fun j hj => by rw [ hp.2 j x hx ] );
  refine' hi ⟨ fun x => ∑ j, W i j * p j x, _, _ ⟩;
  · choose Q hQ using hp.1;
    refine' ⟨ ∑ j, W i j • Q j, _, _ ⟩ <;> simp_all +decide [ Polynomial.degree_lt_iff_coeff_zero ];
    simp +decide [ Polynomial.eval_finset_sum ];
  · exact h_inv

/-
**`thm:exact-quotient-image-lcm-ledger` (degree-bound part).**

For a degree-`d` power curve and a support family `𝒮` (members of size `≥ a ≥ k`), the
number of support-wise curve-MCA-bad parameters witnessed by `𝒮` is at most `d·|𝒮|`.
-/
theorem prop_support_family_curve_ledger (dom : ι → F) {k a d : ℕ}
    (𝒮 : Finset (Finset ι)) (hak : k ≤ a) (hfam : ∀ S ∈ 𝒮, a ≤ S.card)
    (f : Fin (d + 1) → ι → F) :
    (Finset.univ.filter (fun γ : F => ∃ S ∈ 𝒮,
        explainedOn dom k (fun x => ∑ i : Fin (d + 1), γ ^ (i : ℕ) * f i x) S ∧
          ¬ tupleJointlyExplainedOn dom k f S)).card ≤ d * 𝒮.card := by
  refine' le_trans ( Finset.card_le_card _ ) _;
  exact Finset.biUnion 𝒮 fun S => Finset.filter ( fun γ => explainedOn dom k ( fun x => ∑ i : Fin ( d + 1 ), γ ^ ( i : ℕ ) * f i x ) S ∧ ¬ tupleJointlyExplainedOn dom k f S ) Finset.univ;
  · grind;
  · refine' le_trans ( Finset.card_biUnion_le ) _;
    refine' le_trans ( Finset.sum_le_sum fun S hS => show Finset.card _ ≤ d from _ ) _;
    · convert lem_one_support_d_curve dom S hak ( hfam S hS ) f using 1;
    · simp +decide [ mul_comm ]

end RSCap