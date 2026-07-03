import cs25_cap_v12.DeepMCA
import cs25_cap_v12.MainCap

set_option maxHeartbeats 8000000

/-!
# The Reed–Solomon code as a submodule, its minimum distance, and the RS sandwich

To instantiate the abstract results (`thm:deep-mca`, `thm:main`) at the *actual*
Reed–Solomon code, this file packages `RSCap.RSpoly` (the degree-`< k` evaluation
code, from `TheoremA.lean`) as an `F`-submodule and proves its **minimum distance**
`n - k + 1` (the Singleton bound, attained): every nonzero codeword has Hamming
weight at least `n - k + 1`, because a nonzero polynomial of degree `< k` has at
most `k-1` roots among the `n` distinct evaluation points.

Consequences:

* `RSCap.rs_emcaErr_le_deep` / `RSCap.rs_ecaErr_le_deep` — the **deep-regime
  theorem for RS** (`thm:deep-mca`, RS form): `3⌊δn⌋ ≤ n-k` gives
  `ε_mca, ε_ca ≤ (⌊δn⌋+1)/q`.
* `RSCap.rs_two_sided_sandwich` — the **two-sided sandwich** for a single RS row:
  the safe deep bound at `δ_safe` together with the universal cap at `δ_unsafe`.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-
`0` is a Reed–Solomon codeword (the zero polynomial).
-/
omit [Fintype ι] [Fintype F] in
theorem RSpoly_zero_mem (dom : ι → F) (k : ℕ) : (0 : ι → F) ∈ RSpoly dom k := by
  refine' ⟨ 0, _, _ ⟩ <;> norm_num

/-
Reed–Solomon codewords are closed under addition.
-/
omit [Fintype ι] [Fintype F] in
theorem RSpoly_add_mem (dom : ι → F) (k : ℕ) {a b : ι → F}
    (ha : a ∈ RSpoly dom k) (hb : b ∈ RSpoly dom k) : a + b ∈ RSpoly dom k := by
  obtain ⟨ Qa, hQa_deg, hQa_eval ⟩ := ha
  obtain ⟨ Qb, hQb_deg, hQb_eval ⟩ := hb;
  exact ⟨ Qa + Qb, by exact lt_of_le_of_lt ( Polynomial.degree_add_le _ _ ) ( max_lt hQa_deg hQb_deg ), fun i => by simp +decide [ hQa_eval i, hQb_eval i ] ⟩

/-
Reed–Solomon codewords are closed under scalar multiplication.
-/
omit [Fintype ι] [Fintype F] in
theorem RSpoly_smul_mem (dom : ι → F) (k : ℕ) (r : F) {c : ι → F}
    (hc : c ∈ RSpoly dom k) : r • c ∈ RSpoly dom k := by
  obtain ⟨ Q, hQ₁, hQ₂ ⟩ := hc; use Polynomial.C r * Q; simp_all +decide ;
  exact lt_of_le_of_lt ( add_le_of_nonpos_left ( Polynomial.degree_C_le ) ) hQ₁

/-- The Reed–Solomon code `RS[F, D, k]` as an `F`-submodule of `Fⁿ`. -/
def RSpolySubmodule (dom : ι → F) (k : ℕ) : Submodule F (ι → F) where
  carrier := RSpoly dom k
  add_mem' ha hb := RSpoly_add_mem dom k ha hb
  zero_mem' := RSpoly_zero_mem dom k
  smul_mem' r _ hc := RSpoly_smul_mem dom k r hc

omit [Fintype ι] [Fintype F] in
@[simp] theorem RSpolySubmodule_coe (dom : ι → F) (k : ℕ) :
    ((RSpolySubmodule dom k : Submodule F (ι → F)) : Set (ι → F)) = RSpoly dom k := rfl

/-
**Minimum distance of the Reed–Solomon code (Singleton).**  On an injective
evaluation domain, every nonzero codeword of `RS[F,D,k]` has Hamming weight at
least `n - k + 1`.
-/
omit [Fintype F] in
theorem rs_min_weight (dom : ι → F) (hdom : Function.Injective dom) (k : ℕ) :
    ∀ z ∈ RSpolySubmodule dom k, z ≠ (0 : ι → F) →
      Fintype.card ι + 1 - k ≤ numDiff z (0 : ι → F) := by
  -- By definition of the Reed–Solomon code, every nonzero codeword has Hamming weight at least $n - k + 1$.
  intros z hz hz_nonzero
  obtain ⟨Q, hQdeg, hQeval⟩ := hz;
  -- Since $Q$ is a polynomial of degree less than $k$, it can have at most $k-1$ roots.
  have hQ_roots : (Finset.univ.filter (fun i => Q.eval (dom i) = 0)).card ≤ k - 1 := by
    by_cases hQ_zero : Q = 0;
    · exact False.elim ( hz_nonzero ( funext fun i => by simp +decide [ hQ_zero, hQeval ] ) );
    · have hQ_roots : (Finset.image dom (Finset.univ.filter (fun i => Q.eval (dom i) = 0))).card ≤ Q.roots.toFinset.card := by
        exact Finset.card_le_card fun x hx => by aesop;
      rw [ Finset.card_image_of_injective _ hdom ] at hQ_roots;
      exact le_trans hQ_roots ( le_trans ( Multiset.toFinset_card_le _ ) ( Nat.le_sub_one_of_lt ( lt_of_le_of_lt ( Polynomial.card_roots' _ ) ( Polynomial.natDegree_lt_iff_degree_lt ( by aesop ) |>.2 hQdeg ) ) ) );
  have hQ_roots : (Finset.univ.filter (fun i => z i ≠ 0)).card = Fintype.card ι - (Finset.univ.filter (fun i => z i = 0)).card := by
    rw [ Finset.filter_not, Finset.card_sdiff ] ; aesop;
  rcases k with ( _ | k ) <;> simp_all +decide [ numDiff ];
  · exact hz_nonzero ( funext hQeval );
  · omega

/-- **Deep-regime theorem for RS, mutual form (`thm:deep-mca`).**  If
`3⌊δn⌋ + k ≤ n` (i.e. `3⌊δn⌋ ≤ n-k`, one third of the distance), then
`ε_mca(RS[F,D,k], δ) ≤ (⌊δn⌋+1)/q`. -/
theorem rs_emcaErr_le_deep (dom : ι → F) (hdom : Function.Injective dom) (k : ℕ)
    (δ : ℝ) (hδ : 0 ≤ δ)
    (h3r : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ + k ≤ Fintype.card ι) :
    emcaErr (RSpoly dom k) δ
      ≤ ((⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) + 1) / (Fintype.card F) := by
  have hw := rs_min_weight dom hdom k
  have h3r' : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ (Fintype.card ι + 1 - k) - 1 := by
    omega
  have := emcaErr_le_deep (RSpolySubmodule dom k) hw δ hδ h3r'
  simpa using this

/-- **Deep-regime theorem for RS, correlated form (`thm:deep-mca`).** -/
theorem rs_ecaErr_le_deep (dom : ι → F) (hdom : Function.Injective dom) (k : ℕ)
    (δ : ℝ) (hδ : 0 ≤ δ)
    (h3r : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ + k ≤ Fintype.card ι) :
    ecaErr (RSpoly dom k) δ δ
      ≤ ((⌊δ * (Fintype.card ι : ℝ)⌋₊ : ℝ) + 1) / (Fintype.card F) := by
  have hw := rs_min_weight dom hdom k
  have h3r' : 3 * ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ (Fintype.card ι + 1 - k) - 1 := by
    omega
  have := ecaErr_le_deep (RSpolySubmodule dom k) hw δ hδ h3r'
  simpa using this

/-- **Two-sided sandwich for a single Reed–Solomon row.**  For one RS code
`C = RS[F,D,k]`, the safe deep bound at `δ_safe` (unconditional, one third of the
distance) coexists with the universal cap at `δ_unsafe` (from the fiber list,
capacity edge): `ε_mca(C, δ_safe) ≤ (⌊δ_safe·n⌋+1)/q` while
`(1/2k)(1 - n/q) < ε_mca(C, δ_unsafe)`. -/
theorem rs_two_sided_sandwich (dom : ι → F) (hdom : Function.Injective dom)
    {k : ℕ} (hk : 1 ≤ k)
    (δsafe : ℝ) (hδsafe : 0 ≤ δsafe)
    (h3r : 3 * ⌊δsafe * (Fintype.card ι : ℝ)⌋₊ + k ≤ Fintype.card ι)
    (δunsafe : ℝ)
    (hak : (k : ℝ) < (1 - δunsafe) * Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    {N ℓ Bc : ℕ} (hBc : 0 < Bc)
    (hyp : (Bc : ℝ) * ((Fintype.card F : ℝ) / k + 1) ≤ (Nat.choose N ℓ : ℝ))
    (hfiber : ∃ (U : ι → F) (L : ℕ) (P : Fin L → Polynomial F),
        1 ≤ L ∧ (∀ i, (P i).degree ≤ (k : WithBot ℕ)) ∧
        (∀ i j, i ≠ j → P i ≠ P j) ∧
        (∀ i, ((Finset.univ.filter (fun x => (P i).eval (dom x) ≠ U x)).card : ℝ)
          ≤ δunsafe * Fintype.card ι) ∧
        (Nat.choose N ℓ : ℝ) / (Bc : ℝ) ≤ (L : ℝ)) :
    emcaErr (RSpoly dom k) δsafe
        ≤ ((⌊δsafe * (Fintype.card ι : ℝ)⌋₊ : ℝ) + 1) / (Fintype.card F)
      ∧ (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
          < emcaErr (RSpoly dom k) δunsafe := by
  refine ⟨rs_emcaErr_le_deep dom hdom k δsafe hδsafe h3r, ?_⟩
  exact universal_cap_emca_of_fiber_list dom hdom (by omega) δunsafe hak hq hBc hyp hfiber

end RSCap