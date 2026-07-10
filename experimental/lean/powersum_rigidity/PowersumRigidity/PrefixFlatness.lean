import Mathlib
import PowersumRigidity.Basic

/-!
# The prefix-flatness power-sum bound (Li–Wan generating-function inequality)

This module machine-checks the load-bearing inequality behind the Fourier-flat / prefix-flat payment
(`thm:prefix-flatness-power-sum` in `rs_mca_entropy_frontiers.tex`, `thm:fourier-flat-q` in `grande_finale.tex`):
if every power sum of a family is bounded by `Λ`, the `m`-th elementary symmetric function is bounded by the
generalized binomial coefficient `C(Λ+m-1, m) = [u^m](1-u)^{-Λ}`.

    if  ‖p_j(a)‖ ≤ Λ  for all 1 ≤ j ≤ m,   then  ‖e_m(a)‖ ≤ B Λ m,
    B Λ m := (∏_{i<m}(Λ+i)) / m!   =   C(Λ+m-1, m).

This is exactly the step that converts a Weil/character-sum bound on the power sums `p_j(a)` (the deployed
`a_t = ψ(α·g(t))`) into a bound on the prefix-fiber count `e_m(a) = R̂(α)`. The proof is a strong induction on
`m` via Newton's identity (`PowersumRigidity.newton_image`), majorized by the rising-factorial recursion
`m·B_m = Λ·Σ_{i<m} B_i` (`B_rec`).

## Main results

* `PrefixFlatness.B` — the bound `C(Λ+m-1, m)`.
* `PrefixFlatness.B_rec` — the rising-factorial recursion `m·B_m = Λ·Σ_{i<m} B_i`.
* `PrefixFlatness.esymm_norm_le` — the prefix-flatness inequality `‖e_m‖ ≤ B Λ m`.
-/

open Finset

namespace PrefixFlatness

/-- The generalized binomial bound `B Λ m = (∏_{i<m}(Λ+i))/m! = C(Λ+m-1, m)`. -/
noncomputable def B (Λ : ℝ) (m : ℕ) : ℝ := (∏ i ∈ Finset.range m, (Λ + i)) / m.factorial

@[simp] lemma B_zero (Λ : ℝ) : B Λ 0 = 1 := by simp [B]

lemma B_nonneg {Λ : ℝ} (hΛ : 0 ≤ Λ) (m : ℕ) : 0 ≤ B Λ m := by
  apply div_nonneg
  · exact Finset.prod_nonneg fun i _ => by positivity
  · positivity

/-- `(m+1)·B_{m+1} = (Λ+m)·B_m`: the one-step rising-factorial recursion. -/
lemma succ_mul_B (Λ : ℝ) (m : ℕ) :
    ((m : ℝ) + 1) * B Λ (m + 1) = (Λ + m) * B Λ m := by
  have hm : (m.factorial : ℝ) ≠ 0 := by positivity
  have hm1 : ((m : ℝ) + 1) ≠ 0 := by positivity
  have hfac : ((m + 1).factorial : ℝ) = ((m : ℝ) + 1) * (m.factorial : ℝ) := by
    exact_mod_cast Nat.factorial_succ m
  rw [B, B, Finset.prod_range_succ, hfac]
  field_simp

/-- The rising-factorial recursion `m·B_m = Λ·Σ_{i<m} B_i`. -/
lemma B_rec (Λ : ℝ) (m : ℕ) :
    (m : ℝ) * B Λ m = Λ * ∑ i ∈ Finset.range m, B Λ i := by
  induction m with
  | zero => simp
  | succ m ih =>
    have h := succ_mul_B Λ m
    rw [Finset.sum_range_succ, mul_add, ← ih]
    push_cast
    rw [h]; ring

variable {K : Type*} [RCLike K]

/-- Reindex a filtered-antidiagonal sum over `{(i,j) : i+j=k, i<k}` to a range sum over `i < k`. -/
lemma sum_filter_antidiag {M : Type*} [AddCommMonoid M] (k : ℕ) (g : ℕ → ℕ → M) :
    ∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k), g a.1 a.2
      = ∑ i ∈ Finset.range k, g i (k - i) := by
  rw [Finset.sum_filter, Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk,
      Finset.sum_range_succ]
  simp only [lt_irrefl, if_false, add_zero]
  refine Finset.sum_congr rfl (fun i hi => ?_)
  rw [Finset.mem_range] at hi
  simp [hi]

/-- **Prefix-flatness power-sum bound.**  Over `K = ℝ` or `ℂ`, if every power sum
`p_j = (s.map (·^j)).sum` of a finite multiset `s` satisfies `‖p_j‖ ≤ Λ` for `1 ≤ j ≤ m`, then the `m`-th
elementary symmetric function is bounded by the generalized binomial coefficient:
`‖s.esymm m‖ ≤ B Λ m = C(Λ+m-1, m)`. -/
theorem esymm_norm_le (s : Multiset K) (Λ : ℝ) (hΛ : 0 ≤ Λ) (m : ℕ)
    (hp : ∀ j, 1 ≤ j → j ≤ m → ‖(s.map (· ^ j)).sum‖ ≤ Λ) :
    ‖s.esymm m‖ ≤ B Λ m := by
  obtain ⟨d, hd⟩ : ∃ d, s.card = d := ⟨_, rfl⟩
  obtain ⟨v, rfl⟩ := PowersumRigidity.exists_tuple s hd
  set t := Finset.univ.val.map v with ht
  suffices H : ∀ k, k ≤ m → ‖t.esymm k‖ ≤ B Λ k from H m le_rfl
  intro k
  induction k using Nat.strong_induction_on with
  | _ k ih =>
    intro hkm
    rcases Nat.eq_zero_or_pos k with hk0 | hk1
    · subst hk0
      have h0 : t.esymm 0 = 1 := by simp [Multiset.esymm, Multiset.powersetCard_zero_left]
      rw [h0]; simp
    · have hkK : ‖(k : K)‖ = (k : ℝ) := by simp
      have hkpos : (0 : ℝ) < k := by exact_mod_cast hk1
      have hnewton := PowersumRigidity.newton_image v k
      have hnorm : (k : ℝ) * ‖t.esymm k‖
          ≤ ∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k),
              ‖t.esymm a.1‖ * ‖(t.map (· ^ a.2)).sum‖ := by
        calc (k : ℝ) * ‖t.esymm k‖
            = ‖(k : K) * t.esymm k‖ := by rw [norm_mul, hkK]
          _ = ‖∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k),
                (-1 : K) ^ a.1 * t.esymm a.1 * (t.map (· ^ a.2)).sum‖ := by
              rw [hnewton, norm_mul, norm_pow, norm_neg, norm_one, one_pow, one_mul]
          _ ≤ ∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k),
                ‖(-1 : K) ^ a.1 * t.esymm a.1 * (t.map (· ^ a.2)).sum‖ := norm_sum_le _ _
          _ = ∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k),
                ‖t.esymm a.1‖ * ‖(t.map (· ^ a.2)).sum‖ := by
              refine Finset.sum_congr rfl (fun a _ => ?_)
              rw [norm_mul, norm_mul, norm_pow, norm_neg, norm_one, one_pow, one_mul]
      have hbound : ∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k),
              ‖t.esymm a.1‖ * ‖(t.map (· ^ a.2)).sum‖
          ≤ ∑ i ∈ Finset.range k, B Λ i * Λ := by
        rw [sum_filter_antidiag k (fun i j => ‖t.esymm i‖ * ‖(t.map (· ^ j)).sum‖)]
        refine Finset.sum_le_sum (fun i hi => ?_)
        rw [Finset.mem_range] at hi
        have him : i ≤ m := le_trans (le_of_lt hi) hkm
        have hjpos : 1 ≤ k - i := by omega
        have hjm : k - i ≤ m := le_trans (Nat.sub_le k i) hkm
        have hei : ‖t.esymm i‖ ≤ B Λ i := ih i hi him
        have hpj : ‖(t.map (· ^ (k - i))).sum‖ ≤ Λ := hp (k - i) hjpos hjm
        calc ‖t.esymm i‖ * ‖(t.map (· ^ (k - i))).sum‖
            ≤ B Λ i * ‖(t.map (· ^ (k - i))).sum‖ :=
              mul_le_mul_of_nonneg_right hei (norm_nonneg _)
          _ ≤ B Λ i * Λ := mul_le_mul_of_nonneg_left hpj (B_nonneg hΛ i)
      have hkBk : (k : ℝ) * B Λ k = ∑ i ∈ Finset.range k, B Λ i * Λ := by
        rw [B_rec, Finset.mul_sum]; exact Finset.sum_congr rfl (fun i _ => by ring)
      have hfin : (k : ℝ) * ‖t.esymm k‖ ≤ (k : ℝ) * B Λ k := by
        rw [hkBk]; exact le_trans hnorm hbound
      exact le_of_mul_le_mul_left hfin hkpos

end PrefixFlatness
