import Mathlib

/-!
# Power-sum rigidity

A finite multiset of size `d` over a field `K` is determined by its power sums
`p_1, …, p_d`, provided `1, …, d` are all invertible in `K` (i.e. `K` has
characteristic `0` or characteristic `> d`).

The main result is `PowersumRigidity.powersum_rigidity`.

## Proof outline

1. Represent each size-`d` multiset as the image of a tuple `v : Fin d → K`
   (`exists_tuple`).
2. Newton's identities (Mathlib's `MvPolynomial.mul_esymm_eq_sum`), evaluated at
   the tuple, give a triangular recurrence expressing the elementary symmetric
   functions in terms of the power sums (`newton_image`). Since `1, …, d` are
   invertible, equal power sums force equal elementary symmetric functions
   (`esymm_eq_of_psum_eq`).
3. By Vieta's formulas (`Multiset.prod_X_sub_X_eq_sum_esymm`) equal elementary
   symmetric functions force the monic polynomials `∏ (X - a)` to be equal, whose
   roots recover the multiset (`Multiset.roots_multiset_prod_X_sub_C`).
-/

open Finset Polynomial

namespace PowersumRigidity

variable {K : Type*} [Field K]

omit [Field K] in
/-- Every size-`d` multiset over `K` is the image of some tuple `v : Fin d → K`
under the universal map. -/
lemma exists_tuple {d : ℕ} (s : Multiset K) (hs : s.card = d) :
    ∃ v : Fin d → K, s = Finset.univ.val.map v := by
  have hlen : s.toList.length = d := by rw [Multiset.length_toList, hs]
  refine ⟨fun i => s.toList[(i : ℕ)]'(by rw [hlen]; exact i.2), ?_⟩
  have hl : List.ofFn (fun i : Fin d => s.toList[(i : ℕ)]'(by rw [hlen]; exact i.2))
      = s.toList := by
    apply List.ext_getElem
    · rw [List.length_ofFn, hlen]
    · intro n h1 h2
      rw [List.getElem_ofFn]
  rw [Fin.univ_val_map, hl, Multiset.coe_toList]

/-- `aeval` of a power-sum symmetric polynomial is the multiset power sum. -/
lemma aeval_psum {d : ℕ} (v : Fin d → K) (n : ℕ) :
    MvPolynomial.aeval v (MvPolynomial.psum (Fin d) K n)
      = ((Finset.univ.val.map v).map (· ^ n)).sum := by
  show MvPolynomial.aeval v (∑ i : Fin d, MvPolynomial.X i ^ n) = _
  rw [map_sum]
  simp only [map_pow, MvPolynomial.aeval_X]
  rw [Multiset.map_map]
  rfl

/-- Newton's identity, evaluated at a tuple `v`, as a recurrence for the multiset
elementary symmetric functions of the values of `v` in terms of lower ones and the
power sums. -/
lemma newton_image {d : ℕ} (v : Fin d → K) (k : ℕ) :
    (k : K) * (Finset.univ.val.map v).esymm k =
      (-1) ^ (k + 1) *
        ∑ a ∈ Finset.antidiagonal k with a.1 < k,
          (-1) ^ a.1 * (Finset.univ.val.map v).esymm a.1 *
            ((Finset.univ.val.map v).map (· ^ a.2)).sum := by
  have h := congrArg (MvPolynomial.aeval v) (MvPolynomial.mul_esymm_eq_sum (Fin d) K k)
  simpa only [map_mul, map_natCast, map_sum, map_pow, map_neg, map_one,
    MvPolynomial.aeval_esymm_eq_multiset_esymm, aeval_psum] using h

/-- If two tuples have equal power sums `p_1, …, p_d` and `1, …, d` are invertible,
then all their elementary symmetric functions up to degree `d` coincide. -/
lemma esymm_eq_of_psum_eq {d : ℕ} (v w : Fin d → K)
    (hchar : ∀ k, 1 ≤ k → k ≤ d → (k : K) ≠ 0)
    (hpe : ∀ j, 1 ≤ j → j ≤ d →
      ((Finset.univ.val.map v).map (· ^ j)).sum
        = ((Finset.univ.val.map w).map (· ^ j)).sum) :
    ∀ k, k ≤ d → (Finset.univ.val.map v).esymm k = (Finset.univ.val.map w).esymm k := by
  intro k
  induction k using Nat.strong_induction_on with
  | _ k ih =>
    intro hkd
    rcases Nat.eq_zero_or_pos k with hk0 | hk1
    · subst hk0
      simp [Multiset.esymm, Multiset.powersetCard_zero_left]
    · have hkne : (k : K) ≠ 0 := hchar k hk1 hkd
      have hv := newton_image v k
      have hw := newton_image w k
      have hsum : ∑ a ∈ Finset.antidiagonal k with a.1 < k,
            (-1 : K) ^ a.1 * (Finset.univ.val.map v).esymm a.1 *
              ((Finset.univ.val.map v).map (· ^ a.2)).sum =
          ∑ a ∈ Finset.antidiagonal k with a.1 < k,
            (-1 : K) ^ a.1 * (Finset.univ.val.map w).esymm a.1 *
              ((Finset.univ.val.map w).map (· ^ a.2)).sum := by
        refine Finset.sum_congr rfl (fun a ha => ?_)
        rw [Finset.mem_filter, Finset.mem_antidiagonal] at ha
        obtain ⟨hsum_eq, halt⟩ := ha
        have hesymm_a : (Finset.univ.val.map v).esymm a.1
            = (Finset.univ.val.map w).esymm a.1 :=
          ih a.1 halt (le_trans (le_of_lt halt) hkd)
        have ha2pos : 1 ≤ a.2 := by omega
        have ha2le : a.2 ≤ d := by omega
        rw [hesymm_a, hpe a.2 ha2pos ha2le]
      have key : (k : K) * (Finset.univ.val.map v).esymm k
          = (k : K) * (Finset.univ.val.map w).esymm k := by
        rw [hv, hw, hsum]
      exact mul_left_cancel₀ hkne key

/-- **Power-sum rigidity.** Over a field `K`, a size-`d` multiset is determined by
its power sums `p_1, …, p_d`, provided `1, …, d` are invertible in `K`
(characteristic `0` or `> d`). -/
theorem powersum_rigidity {d : ℕ} (A B : Multiset K)
    (hA : A.card = d) (hB : B.card = d)
    (hchar : ∀ k, 1 ≤ k → k ≤ d → (k : K) ≠ 0)
    (hp : ∀ j, 1 ≤ j → j ≤ d → (A.map (· ^ j)).sum = (B.map (· ^ j)).sum) :
    A = B := by
  obtain ⟨v, rfl⟩ := exists_tuple A hA
  obtain ⟨w, rfl⟩ := exists_tuple B hB
  have he : ∀ k, k ≤ d →
      (Finset.univ.val.map v).esymm k = (Finset.univ.val.map w).esymm k :=
    esymm_eq_of_psum_eq v w hchar hp
  have key : ((Finset.univ.val.map v).map (fun t => X - C t)).prod
      = ((Finset.univ.val.map w).map (fun t => X - C t)).prod := by
    rw [Multiset.prod_X_sub_X_eq_sum_esymm, Multiset.prod_X_sub_X_eq_sum_esymm, hA, hB]
    refine Finset.sum_congr rfl (fun j hj => ?_)
    rw [he j (Nat.lt_succ_iff.mp (Finset.mem_range.mp hj))]
  calc Finset.univ.val.map v
      = ((Finset.univ.val.map v).map (fun t => X - C t)).prod.roots :=
        (Polynomial.roots_multiset_prod_X_sub_C _).symm
    _ = ((Finset.univ.val.map w).map (fun t => X - C t)).prod.roots := by rw [key]
    _ = Finset.univ.val.map w := Polynomial.roots_multiset_prod_X_sub_C _

end PowersumRigidity
