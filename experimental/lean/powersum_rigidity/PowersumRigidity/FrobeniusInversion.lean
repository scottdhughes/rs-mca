import Mathlib
import PowersumRigidity.Basic
import PowersumRigidity.ReciprocalGap

/-!
# Frobenius power-sum inversion (L5) and the Mersenne reciprocal-gap theorem

Over a field `K` of characteristic `p` (prime), for a finset `B ⊆ μ_{p+1}` (every
element satisfies `x ^ (p+1) = 1`), the Frobenius endomorphism `x ↦ x ^ p`
coincides with inversion `x ↦ x⁻¹` on `B` (because `x · x^p = x^{p+1} = 1`).
Consequently the `p`-th power of the `j`-th power sum of `B` equals the `j`-th
power sum of the *reciprocals* `B⁻¹`:

`(∑_{x∈B} x^j)^p = ∑_{x∈B} (x⁻¹)^j`.

This is **Lemma L5** (`psum_inv_eq_psum_pow`).  It converts vanishing of the
power sums of `B` into vanishing of the power sums of `B⁻¹` for free.

Combining L5 with Newton's identities (a triangular solve, extracted from
`PowersumRigidity.Basic`) which bridge power-sum vanishing and elementary
symmetric-function vanishing, and with `ReciprocalGap.reciprocal_gap`, we obtain
the full **Mersenne reciprocal-gap theorem** (`mersenne_reciprocal_gap`): if the
low elementary symmetric functions `e_1,…,e_t` of `B ⊆ μ_{p+1}` vanish, and
`t+1 ≤ b ≤ 2t+1` with `1,…,t` invertible, then *every* intermediate
`e_1,…,e_{b-1}` of `B` vanishes.

## Main results

* `FrobeniusInversion.psum_inv_eq_psum_pow` — **L5**, the Frobenius power-sum
  inversion identity.
* `FrobeniusInversion.psum_zero_of_inv` / `psum_image_inv_zero` — its corollaries
  (power-sum vanishing transfers to `B⁻¹`, in element and image form).
* `FrobeniusInversion.esymm_zero_of_psum_zero` /
  `FrobeniusInversion.psum_zero_of_esymm_zero` — the two Newton bridges between
  power-sum vanishing and esymm vanishing on `[1,t]`.
* `FrobeniusInversion.mersenne_reciprocal_gap` — the capstone.
-/

open Finset

namespace FrobeniusInversion

attribute [local instance] Classical.propDecidable

variable {K : Type*} [Field K] {p : ℕ} [Fact (Nat.Prime p)] [CharP K p] {B : Finset K}

/-! ### Target 1 — the Frobenius power-sum inversion identity (L5) -/

/-- The reciprocal-vs-inverse power sums are related by inversion on `B`, seen as
a sum over the image finset `B⁻¹ = B.image (·⁻¹)`.  Inversion is an involution,
hence injective, so this is a bare reindexing (no cancellation needed). -/
theorem sum_pow_image_inv (j : ℕ) :
    (∑ y ∈ B.image (·⁻¹), y ^ j) = ∑ x ∈ B, (x⁻¹) ^ j := by
  have hinj : Function.Injective ((·⁻¹) : K → K) :=
    Function.Involutive.injective (fun a => inv_inv a)
  rw [Finset.sum_image hinj.injOn]

/-- **Frobenius power-sum inversion identity (Lemma L5).**  Over a field `K` of
prime characteristic `p`, if every element of `B` is a `(p+1)`-th root of unity
(`x ^ (p+1) = 1`, i.e. `B ⊆ μ_{p+1}`), then for every `j`,
`(∑_{x∈B} x^j)^p = ∑_{x∈B} (x⁻¹)^j`.

The proof: the Frobenius `x ↦ x^p` distributes over the sum (`sum_pow_char`),
and on `B` one has `x⁻¹ = x^p` (since `x · x^p = x^{p+1} = 1`), whence
`(x⁻¹)^j = (x^p)^j = (x^j)^p`. -/
theorem psum_inv_eq_psum_pow (hB1 : ∀ x ∈ B, x ^ (p + 1) = 1) (j : ℕ) :
    (∑ x ∈ B, x ^ j) ^ p = ∑ x ∈ B, (x⁻¹) ^ j := by
  rw [sum_pow_char]
  refine Finset.sum_congr rfl (fun x hx => ?_)
  have hxinv : x⁻¹ = x ^ p := by
    apply inv_eq_of_mul_eq_one_right
    rw [← pow_succ' x p]
    exact hB1 x hx
  rw [hxinv]
  exact pow_right_comm x j p

/-- Corollary of L5 (element form): if the `j`-th power sum of `B` vanishes, so
does the `j`-th power sum of the reciprocals. -/
theorem psum_zero_of_inv (hB1 : ∀ x ∈ B, x ^ (p + 1) = 1) {j : ℕ}
    (h : (∑ x ∈ B, x ^ j) = 0) : (∑ x ∈ B, (x⁻¹) ^ j) = 0 := by
  have hp0 : p ≠ 0 := (Fact.out : Nat.Prime p).pos.ne'
  rw [← psum_inv_eq_psum_pow hB1 j, h, zero_pow hp0]

/-- Corollary of L5 (image form): if the `j`-th power sum of `B` vanishes, so does
the `j`-th power sum over the reciprocal finset `B⁻¹ = B.image (·⁻¹)`. -/
theorem psum_image_inv_zero (hB1 : ∀ x ∈ B, x ^ (p + 1) = 1) {j : ℕ}
    (h : (∑ x ∈ B, x ^ j) = 0) : (∑ y ∈ B.image (·⁻¹), y ^ j) = 0 := by
  rw [sum_pow_image_inv]
  exact psum_zero_of_inv hB1 h

/-! ### Target 2 — the Newton bridges (power-sum ⟺ esymm vanishing on `[1,t]`)

These are extracted/adapted from the triangular Newton solve in
`PowersumRigidity.Basic` (`newton_image`, `exists_tuple`). -/

/-- **Newton bridge, psum ⟹ esymm.**  If the power sums `p_1,…,p_t` of a multiset
`s` all vanish and `1,…,t` are invertible, then the elementary symmetric functions
`e_1,…,e_t` of `s` all vanish. -/
lemma esymm_zero_of_psum_zero {b t : ℕ} (s : Multiset K)
    (hs : Multiset.card s = b)
    (hchar : ∀ k, 1 ≤ k → k ≤ t → (k : K) ≠ 0)
    (hp : ∀ j, 1 ≤ j → j ≤ t → (s.map (· ^ j)).sum = 0) :
    ∀ k, 1 ≤ k → k ≤ t → s.esymm k = 0 := by
  obtain ⟨v, rfl⟩ := PowersumRigidity.exists_tuple s hs
  intro k
  induction k using Nat.strong_induction_on with
  | _ k ih =>
    intro hk1 hkt
    have hkne : (k : K) ≠ 0 := hchar k hk1 hkt
    have hnewton := PowersumRigidity.newton_image v k
    have hk0 : (k : K) * (Finset.univ.val.map v).esymm k = 0 := by
      rw [hnewton, Finset.sum_eq_zero ?_, mul_zero]
      intro a ha
      rw [Finset.mem_filter, Finset.mem_antidiagonal] at ha
      obtain ⟨hae, halt⟩ := ha
      rcases Nat.eq_zero_or_pos a.1 with h0 | hpos
      · have ha2 : a.2 = k := by omega
        rw [ha2, hp k hk1 hkt, mul_zero]
      · rw [ih a.1 halt hpos (by omega), mul_zero, zero_mul]
    exact (mul_eq_zero.mp hk0).resolve_left hkne

/-- **Newton bridge, esymm ⟹ psum.**  If the elementary symmetric functions
`e_1,…,e_t` of a multiset `s` all vanish, then the power sums `p_1,…,p_t` of `s`
all vanish.  (No invertibility hypothesis needed: only `(-1)^{k+1} ≠ 0`.) -/
lemma psum_zero_of_esymm_zero {b t : ℕ} (s : Multiset K)
    (hs : Multiset.card s = b)
    (hesymm : ∀ k, 1 ≤ k → k ≤ t → s.esymm k = 0) :
    ∀ k, 1 ≤ k → k ≤ t → (s.map (· ^ k)).sum = 0 := by
  obtain ⟨v, rfl⟩ := PowersumRigidity.exists_tuple s hs
  intro k hk1 hkt
  have hnewton := PowersumRigidity.newton_image v k
  rw [hesymm k hk1 hkt, mul_zero] at hnewton
  have hmem : ((0, k) : ℕ × ℕ) ∈
      (Finset.antidiagonal k).filter (fun a => a.1 < k) := by
    rw [Finset.mem_filter, Finset.mem_antidiagonal]
    exact ⟨Nat.zero_add k, hk1⟩
  have hSUM : (∑ a ∈ Finset.antidiagonal k with a.1 < k,
        (-1) ^ a.1 * (Finset.univ.val.map v).esymm a.1 *
          ((Finset.univ.val.map v).map (· ^ a.2)).sum) =
      ((Finset.univ.val.map v).map (· ^ k)).sum := by
    rw [Finset.sum_eq_single_of_mem ((0, k) : ℕ × ℕ) hmem]
    · simp [Multiset.esymm, Multiset.powersetCard_zero_left]
    · intro a ha hane
      obtain ⟨a1, a2⟩ := a
      rw [Finset.mem_filter, Finset.mem_antidiagonal] at ha
      obtain ⟨hae, halt⟩ := ha
      have ha1 : 1 ≤ a1 := by
        by_contra hcon
        apply hane
        have e1 : a1 = 0 := by omega
        have e2 : a2 = k := by omega
        rw [e1, e2]
      rw [hesymm a1 ha1 (by omega), mul_zero, zero_mul]
  rw [hSUM] at hnewton
  have hne : ((-1 : K)) ^ (k + 1) ≠ 0 := pow_ne_zero _ (neg_ne_zero.mpr one_ne_zero)
  exact (mul_eq_zero.mp hnewton.symm).resolve_left hne

/-! ### Target 3 — the Mersenne reciprocal-gap capstone -/

/-- **Mersenne reciprocal-gap theorem.**  Let `K` be a field of prime
characteristic `p` and `B : Finset K` with `B ⊆ μ_{p+1}` (every `x ∈ B` satisfies
`x ^ (p+1) = 1`), `B.card = b`, and `t+1 ≤ b ≤ 2t+1`.  If `1,…,t` are invertible
in `K` and the low elementary symmetric functions `e_1,…,e_t` of `B` all vanish,
then *every* intermediate `e_1,…,e_{b-1}` of `B` vanishes.

The proof chains: Newton (esymm ⟹ psum) turns `hBnull` into vanishing of the
power sums of `B`; L5 (`psum_image_inv_zero`) transfers this to the reciprocals
`B⁻¹`; Newton (psum ⟹ esymm) turns that into vanishing of the esymm of `B⁻¹`; and
then `ReciprocalGap.reciprocal_gap` applies. -/
theorem mersenne_reciprocal_gap (B : Finset K) {b t : ℕ}
    (hB1 : ∀ x ∈ B, x ^ (p + 1) = 1) (hb : B.card = b) (hbt : t + 1 ≤ b)
    (hb2t : b ≤ 2 * t + 1)
    (hchar : ∀ k, 1 ≤ k → k ≤ t → (k : K) ≠ 0)
    (hBnull : ∀ j, 1 ≤ j → j ≤ t → B.esymm j = 0) :
    ∀ j, 1 ≤ j → j ≤ b - 1 → B.esymm j = 0 := by
  have hinj : Function.Injective ((·⁻¹) : K → K) :=
    Function.Involutive.injective (fun a => inv_inv a)
  -- `0 ∉ B`, since `0 ^ (p+1) = 0 ≠ 1`.
  have h0 : (0 : K) ∉ B := by
    intro h
    have h1 := hB1 0 h
    rw [zero_pow (Nat.succ_ne_zero p)] at h1
    exact one_ne_zero h1.symm
  -- esymm(B) = 0 on [1,t]  ⟹  psum(B) = 0 on [1,t].
  have hpsumB : ∀ j, 1 ≤ j → j ≤ t → (∑ x ∈ B, x ^ j) = 0 :=
    psum_zero_of_esymm_zero B.val hb hBnull
  -- psum(B) = 0  ⟹  psum(B⁻¹) = 0  (Lemma L5).
  have hpsumBi : ∀ j, 1 ≤ j → j ≤ t → (∑ y ∈ B.image (·⁻¹), y ^ j) = 0 := by
    intro j hj1 hjt
    exact psum_image_inv_zero hB1 (hpsumB j hj1 hjt)
  -- psum(B⁻¹) = 0 on [1,t]  ⟹  esymm(B⁻¹) = 0 on [1,t].
  have hcardBi : (B.image (·⁻¹)).card = b := by
    rw [Finset.card_image_of_injOn hinj.injOn]; exact hb
  have hesymmBi : ∀ j, 1 ≤ j → j ≤ t → (B.image (·⁻¹)).esymm j = 0 :=
    esymm_zero_of_psum_zero (B.image (·⁻¹)).val hcardBi hchar hpsumBi
  exact ReciprocalGap.reciprocal_gap B h0 hb hbt hb2t hBnull hesymmBi

end FrobeniusInversion
