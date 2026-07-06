import cap25_cap_v13_raw_compact.Floor

/-!
# The simple-pole conversion and mutual correlated agreement (MCA)

This file formalizes the *flexible-budget simple-pole conversion* of the paper
(Corollary "flexible-budget conversion", built on Theorem "deep-point list-to-CA
conversion") and the definition of mutual correlated agreement `emca`.

Given a received word `U` and a family `P` of `≥ L` distinct polynomials of degree `≤ k`
each agreeing with `U` on at least `m` positions (a large decoding list for
`RS[F, D, k+1]`), and a slope budget `binom(L,2)·k < |𝔽| - n`, the conversion produces a
pair `(f₁, f₂)` with at least `L` distinct MCA-bad slopes for `RS[F, D, k]`.  Hence
`emca(RS[F,D,k], 1 - m/n) ≥ L / |𝔽|`.

Combined with the identity-prefix floor (`RSMCA.identity_floor`), this yields the deployed
**MCA-row** unsafe certificates structurally.
-/

open Polynomial Finset RSMCA
open scoped Classical

namespace RSMCA

variable {B F : Type*} [Field B] [Field F] [Algebra B F]
  [Fintype B] [Fintype F] [DecidableEq F] [DecidableEq B]

/-- The word `f_α = U / (x - α)`. -/
noncomputable def fpole (D : Finset B) (U : D → F) (α : F) : D → F :=
  fun x => U x / (algebraMap B F (x : B) - α)

/-- The word `g_α = -1 / (x - α)`. -/
noncomputable def gpole (D : Finset B) (α : F) : D → F :=
  fun x => -(algebraMap B F (x : B) - α)⁻¹

/-- `(f₁, f₂)` is column-explained on `S` by a pair of `RS[F,D,K]` codewords. -/
def colExplained (D : Finset B) (K : ℕ) (S : Finset D) (f1 f2 : D → F) : Prop :=
  ∃ c1 ∈ (RS D K : Set (D → F)), ∃ c2 ∈ (RS D K : Set (D → F)),
    ∀ x ∈ S, f1 x = c1 x ∧ f2 x = c2 x

/-- `γ` is an MCA-bad slope for `(f₁, f₂)` at agreement threshold `m` for `RS[F,D,K]`:
there is a support `S` of size `≥ m` on which `f₁ + γ f₂` is a codeword, yet the pair
`(f₁, f₂)` cannot be simultaneously explained by a codeword pair on `S`. -/
def MCAbadSlope (D : Finset B) (K m : ℕ) (f1 f2 : D → F) (γ : F) : Prop :=
  ∃ S : Finset D, m ≤ S.card ∧
    (∃ c ∈ (RS D K : Set (D → F)), ∀ x ∈ S, f1 x + γ * f2 x = c x) ∧
    ¬ colExplained D K S f1 f2

/-- The set of MCA-bad slopes of a pair. -/
noncomputable def badSet (D : Finset B) (K m : ℕ) (f1 f2 : D → F) : Finset F :=
  Finset.univ.filter (fun γ => MCAbadSlope D K m f1 f2 γ)

/-- `emca(RS[F,D,K], 1 - m/n)`: the maximum over pairs of the fraction of MCA-bad slopes. -/
noncomputable def emca (D : Finset B) (K m : ℕ) : ℝ :=
  ⨆ p : (D → F) × (D → F), ((badSet D K m p.1 p.2).card : ℝ) / Fintype.card F

/-- `emca` dominates the bad-slope fraction of every pair. -/
lemma le_emca (D : Finset B) (K m : ℕ) (f1 f2 : D → F) :
    ((badSet D K m f1 f2).card : ℝ) / Fintype.card F ≤ emca (F := F) D K m := by
  unfold emca
  exact le_ciSup (f := fun p : (D → F) × (D → F) =>
      ((badSet D K m p.1 p.2).card : ℝ) / Fintype.card F)
    (Set.Finite.bddAbove (Set.finite_range _)) (f1, f2)

/-- **Column bound at a pole.** For a pole `α` off the evaluation domain, any `RS[F,D,k]`
codeword agrees with `g_α = -1/(x-α)` on at most `k` positions of `D`. -/
lemma gpole_col_bound (D : Finset B) (k : ℕ) (α : F)
    (hα : α ∉ D.image (fun x => algebraMap B F (x : B)))
    (c2 : D → F) (hc2 : c2 ∈ (RS D k : Set (D → F))) :
    (Finset.univ.filter (fun x : D => gpole D α x = c2 x)).card ≤ k := by
  obtain ⟨h, hdeg, hval⟩ := hc2
  set g : F[X] := (X - C α) * h + 1 with hg
  have hgne : g ≠ 0 := by
    intro h0
    have : g.eval α = 0 := by rw [h0]; simp
    rw [hg] at this; simp at this
  have hgdeg : g.natDegree ≤ k := by
    rw [hg]
    by_cases hh : h = 0
    · simp [hh]
    · have hhnat : h.natDegree < k := (natDegree_lt_iff_degree_lt hh).mpr hdeg
      calc ((X - C α) * h + 1).natDegree
          ≤ max ((X - C α) * h).natDegree (1 : F[X]).natDegree := natDegree_add_le _ _
        _ ≤ k := by
            rw [natDegree_mul (X_sub_C_ne_zero α) hh, natDegree_X_sub_C]
            simp; omega
  have hmap : ∀ x ∈ (Finset.univ.filter (fun x : D => gpole D α x = c2 x)),
      algebraMap B F (x : B) ∈ g.roots.toFinset := by
    intro x hx
    rw [mem_filter] at hx
    have hne : algebraMap B F (x : B) - α ≠ 0 := by
      intro hzero
      exact hα (mem_image.mpr ⟨x, x.2, by linear_combination hzero⟩)
    have hgp : gpole D α x = h.eval (algebraMap B F (x : B)) := by rw [hx.2, hval]
    rw [Multiset.mem_toFinset, mem_roots hgne, hg]
    simp only [IsRoot.def, eval_add, eval_mul, eval_sub, eval_X, eval_C, eval_one]
    have hh2 : -(algebraMap B F (x : B) - α)⁻¹ = h.eval (algebraMap B F (x : B)) := hgp
    field_simp at hh2 ⊢
    linear_combination -hh2
  calc (Finset.univ.filter (fun x : D => gpole D α x = c2 x)).card
      ≤ g.roots.toFinset.card := by
        refine Finset.card_le_card_of_injOn (fun x => algebraMap B F (x : B)) hmap ?_
        intro a _ b _ hab
        exact Subtype.ext ((algebraMap B F).injective hab)
    _ ≤ Multiset.card g.roots := Multiset.toFinset_card_le _
    _ ≤ g.natDegree := card_roots' g
    _ ≤ k := hgdeg

set_option maxHeartbeats 1000000 in
/-- **Good pole existence.** If `n + |P|(|P|-1)·k < |𝔽|`, there is a pole `α` off the
evaluation domain at which the polynomials of `P` (each of degree `≤ k`) take distinct
values. -/
lemma exists_pole (D : Finset B) (k : ℕ) (P : Finset F[X])
    (hdeg : ∀ p ∈ P, p.natDegree ≤ k)
    (hbudget : D.card + P.card * (P.card - 1) * k < Fintype.card F) :
    ∃ α : F, α ∉ D.image (fun x => algebraMap B F (x : B)) ∧
      Set.InjOn (fun p : F[X] => p.eval α) (P : Set F[X]) := by
  set R : F[X] := ∏ pq ∈ P.offDiag, (pq.1 - pq.2) with hR
  have hRne : R ≠ 0 := by
    rw [hR, Finset.prod_ne_zero_iff]
    intro pq hpq; rw [Finset.mem_offDiag] at hpq; exact sub_ne_zero.mpr hpq.2.2
  have hoff : P.offDiag.card = P.card * (P.card - 1) := by
    rw [Finset.offDiag_card, Nat.mul_sub_one]
  have hRdeg : R.natDegree ≤ P.card * (P.card - 1) * k := by
    calc R.natDegree ≤ ∑ pq ∈ P.offDiag, (pq.1 - pq.2).natDegree := natDegree_prod_le _ _
      _ ≤ ∑ _pq ∈ P.offDiag, k := by
          apply Finset.sum_le_sum
          intro pq hpq; rw [Finset.mem_offDiag] at hpq
          exact le_trans (natDegree_sub_le _ _) (max_le (hdeg _ hpq.1) (hdeg _ hpq.2.1))
      _ = P.card * (P.card - 1) * k := by rw [Finset.sum_const, smul_eq_mul, hoff]
  set bad : Finset F := D.image (fun x => algebraMap B F (x : B)) ∪ R.roots.toFinset with hbad
  have hbadcard : bad.card < Fintype.card F := by
    calc bad.card ≤ (D.image (fun x => algebraMap B F (x : B))).card + R.roots.toFinset.card :=
          Finset.card_union_le _ _
      _ ≤ D.card + R.natDegree := Nat.add_le_add (Finset.card_image_le)
          (le_trans (Multiset.toFinset_card_le _) (card_roots' R))
      _ ≤ D.card + P.card * (P.card - 1) * k := by omega
      _ < Fintype.card F := hbudget
  have hexists : ∃ α : F, α ∉ bad := by
    by_contra hcon
    push_neg at hcon
    have hcard := Finset.card_le_card (fun α _ => hcon α : (Finset.univ : Finset F) ⊆ bad)
    rw [Finset.card_univ] at hcard; omega
  obtain ⟨α, hα⟩ := hexists
  rw [hbad, Finset.mem_union] at hα
  push_neg at hα
  refine ⟨α, hα.1, ?_⟩
  intro p hp q hq hpq
  have hp' : p ∈ P := Finset.mem_coe.mp hp
  have hq' : q ∈ P := Finset.mem_coe.mp hq
  by_contra hne
  have hmem : (p, q) ∈ P.offDiag := Finset.mem_offDiag.mpr ⟨hp', hq', hne⟩
  have hdvd : (p - q) ∣ R := by rw [hR]; exact Finset.dvd_prod_of_mem _ hmem
  have hroot : (p - q).eval α = 0 := by rw [eval_sub]; exact sub_eq_zero.mpr hpq
  have hR0 : R.eval α = 0 := by obtain ⟨S, hS⟩ := hdvd; rw [hS, eval_mul, hroot, zero_mul]
  exact hα.2 (Multiset.mem_toFinset.mpr ((mem_roots hRne).mpr hR0))

/-- **A single converted slope is MCA-bad.** For `p ∈ P` and a pole `α` off `D`, the slope
`γ = p(α)` is MCA-bad for `(f_α, g_α)`. -/
lemma slope_mca_bad (D : Finset B) (k m : ℕ) (hk : k < m) (U : D → F) (α : F)
    (hα : α ∉ D.image (fun x => algebraMap B F (x : B)))
    (p : F[X]) (hpdeg : p.natDegree ≤ k)
    (hpagree : m ≤ (Finset.univ.filter
      (fun x : D => U x = p.eval (algebraMap B F (x : B)))).card) :
    MCAbadSlope D k m (fpole D U α) (gpole D α) (p.eval α) := by
  set S : Finset D := Finset.univ.filter
    (fun x : D => U x = p.eval (algebraMap B F (x : B))) with hS
  obtain ⟨q, hq⟩ := X_sub_C_dvd_sub_C_eval (a := α) (p := p)
  have hqdeg : q.degree < (k : WithBot ℕ) := by
    by_cases hq0 : q = 0
    · rw [hq0, degree_zero]; exact WithBot.bot_lt_coe k
    · rw [← natDegree_lt_iff_degree_lt hq0]
      have hnum : (p - C (p.eval α)).natDegree ≤ k :=
        le_trans (natDegree_sub_le _ _) (by simp [hpdeg])
      have heq : (X - C α).natDegree + q.natDegree = (p - C (p.eval α)).natDegree := by
        rw [hq, natDegree_mul (X_sub_C_ne_zero α) hq0]
      rw [natDegree_X_sub_C] at heq
      omega
  refine ⟨S, ?_, ?_, ?_⟩
  · rwa [hS]
  · refine ⟨fun x => q.eval (algebraMap B F (x : B)), ⟨q, hqdeg, fun x => rfl⟩, ?_⟩
    intro x hx
    rw [hS, mem_filter] at hx
    have hne : algebraMap B F (x : B) - α ≠ 0 := by
      intro hzero; exact hα (mem_image.mpr ⟨x, x.2, by linear_combination hzero⟩)
    have hqe : p.eval (algebraMap B F (x : B)) - p.eval α
        = (algebraMap B F (x : B) - α) * q.eval (algebraMap B F (x : B)) := by
      have := congrArg (eval (algebraMap B F (x : B))) hq
      simpa [eval_sub, eval_mul, eval_C, eval_X] using this
    rw [fpole, gpole, hx.2]
    field_simp
    linear_combination hqe
  · rintro ⟨c1, _, c2, hc2, hcol⟩
    have hSsub : S ⊆ Finset.univ.filter (fun x : D => gpole D α x = c2 x) := by
      intro x hx
      rw [mem_filter]
      exact ⟨mem_univ _, (hcol x hx).2⟩
    have hcard := Finset.card_le_card hSsub
    have hb := gpole_col_bound D k α hα c2 hc2
    have hmk : m ≤ k := le_trans hpagree (le_trans (by rw [hS] at hcard ⊢; exact hcard) hb)
    omega

/-- **Flexible-budget simple-pole conversion.** A decoding list of `L = |P|` polynomials of
degree `≤ k` for the received word `U`, each agreeing on `≥ m` positions, with slope budget
`n + L(L-1)k < |𝔽|`, forces `emca(RS[F,D,k], 1 - m/n) ≥ L / |𝔽|`. -/
theorem flexible_pole_conversion (D : Finset B) (k m : ℕ) (hk : k < m) (U : D → F)
    (P : Finset F[X])
    (hdeg : ∀ p ∈ P, p.natDegree ≤ k)
    (hagree : ∀ p ∈ P, m ≤ (Finset.univ.filter
      (fun x : D => U x = p.eval (algebraMap B F (x : B)))).card)
    (hbudget : D.card + P.card * (P.card - 1) * k < Fintype.card F) :
    (P.card : ℝ) / Fintype.card F ≤ emca (F := F) D k m := by
  obtain ⟨α, hα, hinj⟩ := exists_pole D k P hdeg hbudget
  have hmaps : ∀ p ∈ P, p.eval α ∈ badSet D k m (fpole D U α) (gpole D α) := by
    intro p hp
    rw [badSet, Finset.mem_filter]
    exact ⟨Finset.mem_univ _, slope_mca_bad D k m hk U α hα p (hdeg p hp) (hagree p hp)⟩
  have hcard : P.card ≤ (badSet D k m (fpole D U α) (gpole D α)).card :=
    Finset.card_le_card_of_injOn (fun p => p.eval α) hmaps hinj
  calc (P.card : ℝ) / Fintype.card F
      ≤ ((badSet D k m (fpole D U α) (gpole D α)).card : ℝ) / Fintype.card F := by
        gcongr
    _ ≤ emca (F := F) D k m := le_emca (F := F) D k m _ _

/-- **Bridge from the identity-prefix floor.** For `K = k+1`, the fiber construction of
`RSMCA.identity_floor` yields a received word `U` and a family `P` of polynomials of degree
`≤ k`, each agreeing with `U` on `≥ m` positions, with `|P| ≥ ⌊binom(n,m)/|𝔹|^{m-(k+1)}⌋`. -/
lemma exists_poly_list (D : Finset B) (k m : ℕ) (hkm : k + 1 ≤ m) (hmn : m ≤ D.card) :
    ∃ (U : D → F) (P : Finset F[X]),
      (D.card).choose m / (Fintype.card B) ^ (m - (k + 1)) ≤ P.card ∧
      (∀ p ∈ P, p.natDegree ≤ k) ∧
      (∀ p ∈ P, m ≤ (Finset.univ.filter
        (fun x : D => U x = p.eval (algebraMap B F (x : B)))).card) := by
  obtain ⟨z, hz⟩ := exists_heavy_fiber (B := B) D (k + 1) m
  refine ⟨recv (F := F) D (k + 1) m z,
    (fiber D (k + 1) m z).image (fun M => (cpoly (k + 1) m z M).map (algebraMap B F)),
    ?_, ?_, ?_⟩
  · have hinj : Set.InjOn (fun M => (cpoly (k + 1) m z M).map (algebraMap B F))
        (fiber D (k + 1) m z : Set (Finset B)) := by
      intro M hM M' hM' heq
      have hcode : code (F := F) D (k + 1) m z M = code (F := F) D (k + 1) m z M' := by
        funext x
        have := congrArg (fun (P : F[X]) => P.eval (algebraMap B F (x : B))) heq
        simpa [code, eval_map, eval₂_at_apply] using this
      exact code_injOn D hmn z hM hM' hcode
    rw [Finset.card_image_of_injOn hinj]; exact hz
  · intro p hp
    rw [Finset.mem_image] at hp
    obtain ⟨M, hM, rfl⟩ := hp
    rw [natDegree_map_eq_of_injective (algebraMap B F).injective]
    have hd := cpoly_degree hkm D z hM
    by_cases h0 : cpoly (k + 1) m z M = 0
    · simp [h0]
    · rw [← Nat.lt_succ_iff]; exact (natDegree_lt_iff_degree_lt h0).mpr hd
  · intro p hp
    rw [Finset.mem_image] at hp
    obtain ⟨M, hM, rfl⟩ := hp
    have hag := code_agrees (F := F) D z hM
    have hfilter : (Finset.univ.filter (fun x : D =>
        recv (F := F) D (k + 1) m z x =
          ((cpoly (k + 1) m z M).map (algebraMap B F)).eval (algebraMap B F (x : B))))
        = Finset.univ.filter (fun x : D =>
          code (F := F) D (k + 1) m z M x = recv (F := F) D (k + 1) m z x) := by
      apply Finset.filter_congr
      intro x _
      have key : ((cpoly (k + 1) m z M).map (algebraMap B F)).eval (algebraMap B F (x : B))
          = code (F := F) D (k + 1) m z M x := by simp [code, eval_map, eval₂_at_apply]
      rw [key]; exact eq_comm
    rw [hfilter]; exact hag

/-- **MCA lower bound from the floor.** If the identity-prefix floor for `K = k+1` is at
least `L₀`, and the slope budget `n + L₀(L₀-1)k < |𝔽|` holds, then
`emca(RS[F,D,k], 1 - m/n) ≥ L₀ / |𝔽|`. -/
theorem emca_ge_of_floor (D : Finset B) (k m : ℕ) (hk1 : k + 1 ≤ m) (hmn : m ≤ D.card)
    (L0 : ℕ)
    (hfloor : L0 ≤ (D.card).choose m / (Fintype.card B) ^ (m - (k + 1)))
    (hbudget : D.card + L0 * (L0 - 1) * k < Fintype.card F) :
    (L0 : ℝ) / Fintype.card F ≤ emca (F := F) D k m := by
  obtain ⟨U, P, hcard, hdeg, hagree⟩ := exists_poly_list (F := F) D k m hk1 hmn
  have hL0P : L0 ≤ P.card := le_trans hfloor hcard
  obtain ⟨P', hP'sub, hP'card⟩ := Finset.exists_subset_card_eq hL0P
  have hbud' : D.card + P'.card * (P'.card - 1) * k < Fintype.card F := by
    rw [hP'card]; exact hbudget
  have hconv := flexible_pole_conversion D k m (by omega) U P'
    (fun p hp => hdeg p (hP'sub hp)) (fun p hp => hagree p (hP'sub hp)) hbud'
  rwa [hP'card] at hconv

/-- Arithmetic helper: `n < L₀·2^t` (with `0 < n`) gives `2^{-t} < L₀/n` over `ℝ`. -/
lemma ratio_lt {q L0 t : ℕ} (hq : 0 < q) (h : q < L0 * 2 ^ t) :
    (1 : ℝ) / 2 ^ t < (L0 : ℝ) / q := by
  have hqr : (0 : ℝ) < q := by exact_mod_cast hq
  have h2 : (0 : ℝ) < 2 ^ t := by positivity
  rw [div_lt_div_iff₀ h2 hqr]
  have : (q : ℝ) < (L0 : ℝ) * 2 ^ t := by exact_mod_cast h
  linarith

end RSMCA
