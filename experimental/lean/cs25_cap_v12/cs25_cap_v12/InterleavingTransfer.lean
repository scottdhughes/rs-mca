import cs25_cap_v12.BlueprintCommon

/-!
# Blueprint: interleaving transfer and explicit witnesses (`lem:inter`, `sec:answers-explicit`)

Skeletons (proofs `sorry`) for two independent parts of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*:

* `lem_inter_eca`, `lem_inter_emca` — **interleaving transfer** (`lem:inter`): for a
  linear code `C`, the `s`-fold interleaved code `C^{≡s}` (here `RSCap.interleave C s`,
  a code over the index type `ι × Fin s`) has CA/MCA error at least that of `C`.  The
  argument is the column-agreement inequality `dist_s(hᐩ, C^{≡s}) ≥ dist(h, C)` with
  equality on diagonal codewords.

* `thm_explicit_head_floor_even` / `thm_explicit_head_floor_odd` —
  **explicit head-and-pairs floor** (`thm:explicit-head-floor`): when the quotient
  set `Q = φ(D)` is antipodally symmetric (`−Q = Q`, `0 ∉ Q`), the pigeonhole in the
  fiber lemma is removed: the pure power word `φ^m|_D` (`m` even) resp. the one-head
  word `(φ^m − t·φ^{m−1})|_D` (`m` odd) carries an *explicit* list of
  `C(N/2, m/2)` resp. `C(N/2 − 1, (m−1)/2)` codewords of `RS[F, D, K]`.

* `thm_explicit_pairs` — **explicit certifying pairs up to a pole**
  (`thm:explicit-pairs`): for at least half of the poles `α ∈ F ∖ D`, the explicit
  simple-pole pair `(u/(x−α), −1/(x−α))` has many distinct CA-bad slopes.  Stated here
  in an abstracted counting form.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-
**`lem:inter` (CA form).**  For a linear code `C` and interleaving arity `s ≥ 1`,
the correlated-agreement error of the interleaved code `C^{≡s}` is at least that of
`C`:  `ε_ca(C, δ) ≤ ε_ca(C^{≡s}, δ)`.
-/
theorem lem_inter_eca (C : Set (ι → F)) {s : ℕ} (hs : 1 ≤ s) (δ : ℝ) :
    ecaErr C δ δ ≤ ecaErr (interleave C s) δ δ := by
  refine' Finset.sup'_le _ _ _;
  intro p hp;
  refine' le_trans _ ( Finset.le_sup' _ _ );
  convert prob_mono _;
  rotate_left;
  exact ( fun x => p.1 x.1, fun x => p.2 x.1 );
  · simp +decide;
  · intro γ hγ;
    constructor;
    · obtain ⟨ c, hc₁, hc₂ ⟩ := hγ.1;
      refine' ⟨ fun i => c i.1, _, _ ⟩ <;> simp_all +decide [ interleave ];
      convert hc₂ using 1;
      unfold relDist;
      unfold numDiff; simp +decide [ Fintype.card_prod ] ;
      rw [ show ( Finset.univ.filter fun i : ι × Fin s => ¬p.1 i.1 + γ * p.2 i.1 = c i.1 ) = Finset.univ.filter ( fun i : ι => ¬p.1 i + γ * p.2 i = c i ) ×ˢ Finset.univ from ?_, Finset.card_product ] ; simp +decide [ div_eq_mul_inv, mul_assoc, mul_comm, mul_left_comm, ne_of_gt ( zero_lt_one.trans_le hs ) ];
      ext ⟨ i, j ⟩ ; simp +decide [ Finset.mem_product ] ;
    · rintro ⟨ c1, hc1, c2, hc2, h ⟩;
      -- By definition of `relDist2`, we know that
      have h_relDist2 : (Finset.univ.filter (fun i : ι × Fin s => p.1 i.1 ≠ c1 i ∨ p.2 i.1 ≠ c2 i)).card ≤ δ * (Fintype.card ι * s) := by
        unfold relDist2 at h;
        rw [ div_le_iff₀ ] at h <;> norm_cast at * ; aesop;
        cases isEmpty_or_nonempty ι <;> simp_all +decide;
        · exact hγ.2 ⟨ p.1, by
            convert hγ.1.choose_spec.1, p.2, by
            convert hγ.1.choose_spec.1, by
            unfold relDist2; aesop; ⟩;
        · exact ⟨ Fintype.card_pos, hs ⟩;
      -- By definition of `relDist2`, we know that there exists some `t : Fin s` such that
      obtain ⟨t, ht⟩ : ∃ t : Fin s, (Finset.univ.filter (fun i : ι => p.1 i ≠ c1 (i, t) ∨ p.2 i ≠ c2 (i, t))).card ≤ δ * (Fintype.card ι) := by
        have h_relDist2 : ∑ t : Fin s, (Finset.univ.filter (fun i : ι => p.1 i ≠ c1 (i, t) ∨ p.2 i ≠ c2 (i, t))).card ≤ δ * (Fintype.card ι * s) := by
          convert h_relDist2 using 1;
          simp +decide only [Finset.card_filter];
          rw [ Finset.sum_comm ];
          rw [ ← Finset.sum_product' ];
          rfl;
        contrapose! h_relDist2;
        simpa [ mul_assoc, mul_comm, mul_left_comm, Finset.mul_sum _ _ _ ] using Finset.sum_lt_sum_of_nonempty ⟨ ⟨ 0, hs ⟩, Finset.mem_univ _ ⟩ fun t ht => h_relDist2 t;
      refine' hγ.2 ⟨ fun i => c1 ( i, t ), _, fun i => c2 ( i, t ), _, _ ⟩;
      · exact hc1 t;
      · exact hc2 t;
      · refine' div_le_of_le_mul₀ _ _ _ <;> norm_cast;
        · exact Nat.zero_le _;
        · exact le_of_not_gt fun h => by nlinarith [ show ( Fintype.card ι : ℝ ) > 0 by exact Nat.cast_pos.mpr ( Fintype.card_pos_iff.mpr ⟨ Classical.choose ( Finset.card_pos.mp ( show 0 < Finset.card ( Finset.univ : Finset ι ) from Finset.card_pos.mpr ⟨ Classical.choose ( Finset.card_pos.mp ( show 0 < Finset.card ( Finset.univ : Finset ι ) from by
                                                                                                                                                                                                                                                                                                        exact absurd ‹δ < 0› ( not_lt_of_ge ( le_trans ( by exact div_nonneg ( Nat.cast_nonneg _ ) ( Nat.cast_nonneg _ ) ) ‹relDist2 ( fun x => p.1 x.1 ) ( fun x => p.2 x.1 ) c1 c2 ≤ δ› ) ) ) ), Finset.mem_univ _ ⟩ ) ) ⟩ ) ] ;

/-
**`lem:inter` (MCA form).**  Likewise `ε_mca(C, δ) ≤ ε_mca(C^{≡s}, δ)`.
-/
theorem lem_inter_emca (C : Set (ι → F)) {s : ℕ} (hs : 1 ≤ s) (δ : ℝ) :
    emcaErr C δ ≤ emcaErr (interleave C s) δ := by
  by_contra h_contra;
  obtain ⟨p, hp⟩ : ∃ p : (ι → F) × (ι → F), prob (fun γ => mcaBad C δ p.1 p.2 γ) > emcaErr (interleave C s) δ := by
    contrapose! h_contra;
    exact Finset.sup'_le _ _ fun p _ => h_contra p;
  refine' hp.not_ge ( le_trans _ ( Finset.le_sup' _ _ ) );
  convert prob_mono _;
  rotate_left;
  exact ⟨ fun x => p.1 x.1, fun x => p.2 x.1 ⟩;
  · grind +qlia;
  · rintro γ ⟨ S, hS₁, ⟨ c, hc₁, hc₂ ⟩, hc₃ ⟩;
    refine' ⟨ S ×ˢ Finset.univ, _, _, _ ⟩ <;> simp_all +decide [ Finset.card_product ];
    · nlinarith;
    · exact ⟨ fun p => c p.1, fun t => hc₁, fun a b ha => rfl ⟩;
    · intro x hx y hy;
      contrapose! hc₃;
      exact ⟨ fun i => x ( i, ⟨ 0, hs ⟩ ), hx ⟨ 0, hs ⟩, fun i => y ( i, ⟨ 0, hs ⟩ ), hy ⟨ 0, hs ⟩, fun i hi => hc₃ i hi ⟨ 0, hs ⟩ ⟩

/-- **`thm:explicit-head-floor`(i) — pure power word, `m` even.**

Let `dom` be `(φ, c)`-smooth over `B` with `N = n/c` even, and suppose the quotient
`Q = φ(D)` is antipodally symmetric with `0 ∉ Q`.  For even `m` with `2 ≤ m ≤ N − 2`
and `c·m ≤ K − 1 + 2c`, the explicit *pure power word* `u = φ^m|_D` carries a list of
at least `C(N/2, m/2)` distinct codewords of `RS[F, D, K]` at radius `1 − cm/n`, with
no pigeonhole and no subfield division. -/
theorem thm_explicit_head_floor_even (dom : ι → F) (hdom : Function.Injective dom)
    (φ : Polynomial F) {c N K m : ℕ}
    (hc : 0 < c) (hφdeg : φ.natDegree = c) (hcN : c * N = Fintype.card ι) (hNeven : Even N)
    (hnegQ : ∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i))
    (h0 : ∀ i, φ.eval (dom i) ≠ 0)
    (hm_even : Even m) (hm_lo : 2 ≤ m) (hm_hi : m ≤ N - 2)
    (hmK : c * m ≤ K - 1 + 2 * c) :
    HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
      (fun i => (φ.eval (dom i)) ^ m) (Nat.choose (N / 2) (m / 2)) := by
  sorry

/-- **`thm:explicit-head-floor`(ii) — one-head word, `m` odd.**

Under the same antipodal hypotheses, for odd `m` and every `t ∈ Q` the explicit
*one-head word* `u = (φ^m − t·φ^{m−1})|_D` carries a list of at least
`C(N/2 − 1, (m−1)/2)` distinct codewords of `RS[F, D, K]` at radius `1 − cm/n`. -/
theorem thm_explicit_head_floor_odd (dom : ι → F) (hdom : Function.Injective dom)
    (φ : Polynomial F) {c N K m : ℕ} (t : F)
    (hc : 0 < c) (hφdeg : φ.natDegree = c) (hcN : c * N = Fintype.card ι) (hNeven : Even N)
    (hnegQ : ∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i))
    (h0 : ∀ i, φ.eval (dom i) ≠ 0) (ht : ∃ i, φ.eval (dom i) = t)
    (hm_odd : Odd m) (hm_lo : 2 ≤ m) (hm_hi : m ≤ N - 2)
    (hmK : c * m ≤ K - 1 + 2 * c) :
    HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
      (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1))
      (Nat.choose (N / 2 - 1) ((m - 1) / 2)) := by
  sorry

/-- **`thm:explicit-pairs` — explicit certifying pairs, up to the choice of a pole.**

Given an explicit list of `L₀` distinct polynomials `P : Fin L₀ → F[X]` of degree
`≤ K` all agreeing with a pure power word `u` on at least `A` points of `D` (deep:
`A > K`), the explicit simple-pole pairs
`f_α(x) = u(x)/(x − α)`, `g_α(x) = −1/(x − α)` (`α ∈ Ω := F ∖ range dom`) satisfy:
for at least half of the `α ∈ Ω`, the set of distinct CA-bad slopes `{P_M(α)}` of the
pair `(f_α, g_α)` at radius `δ = 1 − A/n` has size at least `⌈(q − n)/(3K)⌉`.

Here `caBad (RSpoly dom (K+1)) δ δ f_α g_α (P i).eval α` is the paper's CA-badness of
the slope `P_M(α)`. -/
theorem thm_explicit_pairs (dom : ι → F) (hdom : Function.Injective dom)
    {K L₀ A : ℕ} (hdeep : K < A) (hAn : A ≤ Fintype.card ι)
    (u : Polynomial F) (P : Fin L₀ → Polynomial F)
    (hPdeg : ∀ i, (P i).degree ≤ (K : WithBot ℕ)) (hPinj : Function.Injective P)
    (hagree : ∀ i, A ≤ (Finset.univ.filter (fun x => (P i).eval (dom x) = u.eval (dom x))).card) :
    let Ω : Finset F := Finset.univ.filter (fun α => α ∉ Set.range dom)
    (Ω.filter (fun α =>
        ⌈(Fintype.card F - Fintype.card ι : ℝ) / (3 * K)⌉ ≤
          ((Finset.univ.image (fun i => (P i).eval α)).card : ℤ))).card
      * 2 ≥ Ω.card := by
  sorry

end RSCap