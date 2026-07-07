import Mathlib

/-!
# Reciprocal-gap rigidity

Over a field `K`, for a `Finset K` of nonzero elements `B` with `B.card = b`,
the elementary symmetric functions of the reciprocals `B⁻¹ = B.image (·⁻¹)` are
governed by the **reciprocal esymm identity**
`e_j(B⁻¹) · e_b(B) = e_{b-j}(B)` (for `j ≤ b`; `Finset.esymm` below).

From this we deduce **reciprocal-gap rigidity**: if the low elementary symmetric
functions `e_1, …, e_t` of *both* `B` and `B⁻¹` vanish, and `t+1 ≤ b ≤ 2t+1`,
then *all* intermediate elementary symmetric functions `e_1, …, e_{b-1}` of `B`
vanish, i.e. `∏_{x∈B}(X - x)` is the binomial `X^b + (-1)^b e_b`.

As a further consequence (`binom_split_dvd`), if every element of a size-`b`
finset is both an `n`-th root of unity and an `b`-th root of a common value `c`,
then `b ∣ n`.

## Main results

* `ReciprocalGap.esymm_image_inv_mul` — the reciprocal esymm identity (Target 1).
* `ReciprocalGap.reciprocal_gap` — reciprocal-gap rigidity (Target 2).
* `ReciprocalGap.binom_split_dvd` — the divisibility corollary (Target 3).
-/

open Finset

namespace Finset

/-- The `n`-th elementary symmetric function of a `Finset`, defined via the
elementary symmetric function of its underlying multiset. -/
noncomputable def esymm {R : Type*} [CommSemiring R] (s : Finset R) (n : ℕ) : R :=
  s.val.esymm n

end Finset

namespace ReciprocalGap

attribute [local instance] Classical.propDecidable

variable {K : Type*} [Field K]

/-! ### The elementary symmetric function as a sum over subsets -/

/-- `Finset.esymm B n` is the sum of the products over all `n`-element subsets. -/
theorem esymm_eq_sum_powersetCard (B : Finset K) (n : ℕ) :
    B.esymm n = ∑ t ∈ B.powersetCard n, ∏ x ∈ t, x := by
  have h := Finset.esymm_map_val (id : K → K) B n
  rw [Multiset.map_id] at h
  simpa [Finset.esymm] using h

/-- The elementary symmetric function of the reciprocal set, expressed as a sum
over subsets of `B` of products of reciprocals. -/
theorem esymm_image_inv_eq (B : Finset K) (j : ℕ) :
    (B.image (·⁻¹)).esymm j = ∑ t ∈ B.powersetCard j, ∏ x ∈ t, x⁻¹ := by
  have hinj : Function.Injective ((·⁻¹) : K → K) :=
    Function.Involutive.injective (fun a => inv_inv a)
  have h := Finset.esymm_map_val ((·⁻¹) : K → K) B j
  rw [← Finset.image_val_of_injOn hinj.injOn] at h
  simpa [Finset.esymm] using h

/-- The top elementary symmetric function is the full product. -/
theorem esymm_card_eq_prod (B : Finset K) {b : ℕ} (hb : B.card = b) :
    B.esymm b = ∏ x ∈ B, x := by
  rw [esymm_eq_sum_powersetCard, ← hb, Finset.powersetCard_self, Finset.sum_singleton]

/-! ### Target 1 — the reciprocal esymm identity -/

/-- **Reciprocal esymm identity.** For a finset `B` of nonzero elements with
`B.card = b` and `j ≤ b`,
`e_j(B⁻¹) · e_b(B) = e_{b-j}(B)`,
where `B⁻¹ = B.image (·⁻¹)`.  (Division-free form of `e_j(B⁻¹) = e_{b-j}(B)/e_b(B)`.) -/
theorem esymm_image_inv_mul (B : Finset K) (h0 : (0 : K) ∉ B) {b j : ℕ}
    (hb : B.card = b) (hjb : j ≤ b) :
    (B.image (·⁻¹)).esymm j * B.esymm b = B.esymm (b - j) := by
  classical
  rw [esymm_image_inv_eq, esymm_card_eq_prod B hb, esymm_eq_sum_powersetCard,
    Finset.sum_mul]
  refine Finset.sum_bij' (fun t _ => B \ t) (fun u _ => B \ u) ?_ ?_ ?_ ?_ ?_
  · -- `B \ t` has size `b - j`
    intro t ht
    rw [Finset.mem_powersetCard] at ht ⊢
    exact ⟨Finset.sdiff_subset, by rw [Finset.card_sdiff_of_subset ht.1, hb, ht.2]⟩
  · -- `B \ u` has size `j`
    intro u hu
    rw [Finset.mem_powersetCard] at hu ⊢
    refine ⟨Finset.sdiff_subset, ?_⟩
    rw [Finset.card_sdiff_of_subset hu.1, hb, hu.2]; omega
  · -- left inverse
    intro t ht
    rw [Finset.mem_powersetCard] at ht
    exact Finset.sdiff_sdiff_eq_self ht.1
  · -- right inverse
    intro u hu
    rw [Finset.mem_powersetCard] at hu
    exact Finset.sdiff_sdiff_eq_self hu.1
  · -- the summand identity `(∏ x∈t, x⁻¹) * ∏ x∈B, x = ∏ x∈B\t, x`
    intro t ht
    have htB : t ⊆ B := (Finset.mem_powersetCard.mp ht).1
    have ha : (∏ x ∈ t, x) ≠ 0 := by
      rw [Finset.prod_ne_zero_iff]
      intro x hx hx0
      exact h0 (hx0 ▸ htB hx)
    have hsplit : (∏ x ∈ B \ t, x) * (∏ x ∈ t, x) = ∏ x ∈ B, x :=
      Finset.prod_sdiff htB
    rw [Finset.prod_inv_distrib, ← hsplit,
      mul_comm (∏ x ∈ B \ t, x) (∏ x ∈ t, x), inv_mul_cancel_left₀ ha]

/-! ### Target 2 — reciprocal-gap rigidity -/

/-- **Reciprocal-gap rigidity.** Let `K` be a field and `B : Finset K` a set of
nonzero elements with `B.card = b`, where `t + 1 ≤ b ≤ 2t + 1`.  If the low
elementary symmetric functions `e_1, …, e_t` of both `B` and its reciprocal set
`B⁻¹ = B.image (·⁻¹)` all vanish, then *every* intermediate elementary symmetric
function `e_1, …, e_{b-1}` of `B` vanishes.  Equivalently, `∏_{x∈B}(X - x)` is a
binomial `X^b + (-1)^b e_b`. -/
theorem reciprocal_gap (B : Finset K) (h0 : (0 : K) ∉ B)
    {b t : ℕ} (hb : B.card = b) (hbt : t + 1 ≤ b) (hb2t : b ≤ 2 * t + 1)
    (hB : ∀ j, 1 ≤ j → j ≤ t → B.esymm j = 0)
    (hBi : ∀ j, 1 ≤ j → j ≤ t → (B.image (·⁻¹)).esymm j = 0) :
    ∀ j, 1 ≤ j → j ≤ b - 1 → B.esymm j = 0 := by
  -- Reciprocal identity turns vanishing of `e_k(B⁻¹)` into vanishing of `e_{b-k}(B)`.
  have hrec : ∀ k, 1 ≤ k → k ≤ t → B.esymm (b - k) = 0 := by
    intro k hk1 hkt
    have hkb : k ≤ b := by omega
    have key := esymm_image_inv_mul B h0 hb hkb
    rw [hBi k hk1 hkt, zero_mul] at key
    exact key.symm
  intro j hj1 hjb
  by_cases hjt : j ≤ t
  · exact hB j hj1 hjt
  · have h1 : 1 ≤ b - j := by omega
    have h2 : b - j ≤ t := by omega
    have hval := hrec (b - j) h1 h2
    rwa [show b - (b - j) = j from by omega] at hval

/-! ### Target 3 — binomial splitting in `μ_n` forces `b ∣ n` -/

/-- **Binomial splitting divisibility.**  Let `B : Finset K` have `B.card = b ≥ 1`.
If every element of `B` is an `n`-th root of unity (`n ≥ 1`) *and* every element
is a `b`-th root of a common value `c` (`x ^ b = c`), then `b ∣ n`.

Interpretation: if `∏_{x∈B}(X - x)` is a binomial `X^b - c` whose roots all lie in
the group `μ_n` of `n`-th roots of unity, then `b ∣ n`.  Proof: translating by a
fixed root sends `B` injectively into `μ_{gcd(b,n)}`, which has at most `gcd(b,n)`
elements, forcing `b ≤ gcd(b,n) ≤ b`, i.e. `gcd(b,n) = b`. -/
theorem binom_split_dvd (B : Finset K) {b n : ℕ} (hb1 : 1 ≤ b) (hbcard : B.card = b)
    (hn1 : 1 ≤ n) (c : K)
    (hnpow : ∀ x ∈ B, x ^ n = 1) (hbpow : ∀ x ∈ B, x ^ b = c) :
    b ∣ n := by
  classical
  -- Every element of `B` is nonzero (else `0 = 0^n = 1`).
  have hne : ∀ x ∈ B, x ≠ 0 := by
    intro x hx hx0
    have hxn := hnpow x hx
    rw [hx0, zero_pow (show n ≠ 0 by omega)] at hxn
    exact zero_ne_one hxn
  -- Pick a base point `y ∈ B`; then `c = y ^ b ≠ 0`.
  obtain ⟨y, hy⟩ : B.Nonempty := by rw [← Finset.card_pos, hbcard]; omega
  have hyne : y ≠ 0 := hne y hy
  have hcne : c ≠ 0 := by rw [← hbpow y hy]; exact pow_ne_zero b hyne
  -- The shift `x ↦ x * y⁻¹` is injective on `B`.
  have hφinj : Set.InjOn (fun x => x * y⁻¹) (↑B : Set K) := by
    intro a _ b' _ hab
    exact mul_right_cancel₀ (inv_ne_zero hyne) hab
  set S := B.image (fun x => x * y⁻¹) with hS
  have hScard : S.card = b := by
    rw [hS, Finset.card_image_of_injOn hφinj, hbcard]
  -- Each shifted element is a `gcd b n`-th root of unity.
  have hgpos : 0 < Nat.gcd b n := Nat.gcd_pos_of_pos_left n hb1
  have hSsub : S ⊆ (Polynomial.nthRoots (Nat.gcd b n) (1 : K)).toFinset := by
    intro z hz
    rw [hS, Finset.mem_image] at hz
    obtain ⟨x, hx, rfl⟩ := hz
    rw [Multiset.mem_toFinset, Polynomial.mem_nthRoots hgpos]
    refine pow_gcd_eq_one.mpr ⟨?_, ?_⟩
    · rw [mul_pow, inv_pow, hbpow x hx, hbpow y hy, mul_inv_cancel₀ hcne]
    · rw [mul_pow, inv_pow, hnpow x hx, hnpow y hy, inv_one, mul_one]
  -- Counting: `b = |S| ≤ #μ_{gcd} ≤ gcd b n ≤ b`, hence `gcd b n = b`.
  have hScale : S.card ≤ Nat.gcd b n :=
    calc S.card
        ≤ (Polynomial.nthRoots (Nat.gcd b n) (1 : K)).toFinset.card :=
          Finset.card_le_card hSsub
      _ ≤ Multiset.card (Polynomial.nthRoots (Nat.gcd b n) (1 : K)) :=
          Multiset.toFinset_card_le _
      _ ≤ Nat.gcd b n := Polynomial.card_nthRoots (Nat.gcd b n) (1 : K)
  have h1 : b ≤ Nat.gcd b n := hScard ▸ hScale
  have h2 : Nat.gcd b n ≤ b := Nat.le_of_dvd hb1 (Nat.gcd_dvd_left b n)
  have hgeq : Nat.gcd b n = b := le_antisymm h2 h1
  have hdvd : Nat.gcd b n ∣ n := Nat.gcd_dvd_right b n
  rwa [hgeq] at hdvd

end ReciprocalGap
