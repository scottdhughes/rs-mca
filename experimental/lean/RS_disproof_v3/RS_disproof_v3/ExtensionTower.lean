import Mathlib

/-!
# The 2-adic tower criterion (Paper A, `lem:ext-tower-criterion`)

This file formalizes the number-theoretic heart of the extension-field tower section of

  P. Chojecki, *Capacity-Edge Obstructions to Reed-Solomon Mutual Correlated Agreement
  over Smooth Multiplicative Domains* (`RS_disproof_v3.tex`).

For a prime `p ≡ 1 (mod 4)`, `β = v₂(p-1)`, and a divisor `m ∣ p-1` with `v₂(m) = β`,
the criterion states that for every power of two `d = 2^a`,

  `ord_{m·d}(p) = d`,

i.e. the multiplicative order of `p` modulo `m·d` is exactly `d`.  This is what supplies
the smooth extension towers `𝔽_{p^d}` of degree `d` used in `thm:ext-smooth-towers`.

The proof is via lifting-the-exponent (`padicValNat.pow_two_sub_one`): for `p ≡ 1 (mod 4)`,
`v₂(p^e - 1) = v₂(p-1) + v₂(e)`, so `m·2^a ∣ p^e - 1 ⇔ 2^a ∣ e`, whence the order is `2^a`.
-/

open scoped BigOperators

namespace ExtTower

/-
**Lifting the exponent for `p ≡ 1 (mod 4)`.**
`v₂(p^e - 1) = v₂(p-1) + v₂(e)` for `e ≥ 1`.
-/
lemma val_two_pow_sub_one {p : ℕ} (hp1 : 1 < p) (hpodd : ¬ 2 ∣ p) (hp4 : 4 ∣ p - 1)
    {e : ℕ} (he : 1 ≤ e) :
    padicValNat 2 (p ^ e - 1) = padicValNat 2 (p - 1) + padicValNat 2 e := by
  rcases Nat.even_or_odd' e with ⟨ k, rfl | rfl ⟩;
  · have h_lte : padicValNat 2 (p ^ (2 * k) - 1) + 1 = padicValNat 2 (p + 1) + padicValNat 2 (p - 1) + padicValNat 2 (2 * k) := by
      grind +suggestions;
    -- Since $p \equiv 1 \pmod{4}$, we have $p + 1 \equiv 2 \pmod{4}$, so $v_2(p + 1) = 1$.
    have h_v2_p1 : padicValNat 2 (p + 1) = 1 := by
      obtain ⟨ m, hm ⟩ := hp4; rw [ show p + 1 = 2 * ( 2 * m + 1 ) by omega ] ; rw [ padicValNat.mul ] <;> norm_num;
    linarith;
  · -- By the properties of the 2-adic valuation, we can split the valuation of the product into the sum of the valuations.
    have h_split : padicValNat 2 (p ^ (2 * k + 1) - 1) = padicValNat 2 (p - 1) + padicValNat 2 (∑ i ∈ Finset.range (2 * k + 1), p ^ i) := by
      rw [ ← padicValNat.mul ];
      · zify;
        cases p <;> norm_num [ ← geom_sum_mul, mul_comm ] at *;
      · omega;
      · exact ne_of_gt <| Finset.sum_pos ( fun _ _ => pow_pos ( zero_lt_one.trans hp1 ) _ ) ( by norm_num );
    simp_all +decide [ ← even_iff_two_dvd, parity_simps ];
    rw [ padicValNat.eq_zero_of_not_dvd, padicValNat.eq_zero_of_not_dvd ] <;> norm_num [ Nat.dvd_iff_mod_eq_zero, Nat.add_mod, Nat.mul_mod, Nat.pow_mod, Finset.sum_nat_mod, Nat.odd_iff.mp hpodd ]

/-
Divisibility characterization: for `p ≡ 1 (mod 4)` prime, `m ∣ p-1` with `v₂(m) = v₂(p-1)`,
`m · 2^a ∣ p^e - 1 ⇔ 2^a ∣ e`.
-/
lemma dvd_iff {p m a e : ℕ} (hp : Nat.Prime p) (hp4 : 4 ∣ p - 1) (hm : m ∣ p - 1)
    (hm0 : 0 < m) (hval : padicValNat 2 m = padicValNat 2 (p - 1)) :
    m * 2 ^ a ∣ p ^ e - 1 ↔ 2 ^ a ∣ e := by
  constructor;
  · by_cases he : e = 0;
    · aesop;
    · -- Note p^e - 1 ≠ 0 since p > 1 and e ≥ 1. By val_two_pow_sub_one, padicValNat 2 (p^e-1) = β + padicValNat 2 e.
      have h_val : padicValNat 2 (p ^ e - 1) = padicValNat 2 (p - 1) + padicValNat 2 e := by
        apply val_two_pow_sub_one hp.one_lt (by
        rw [ hp.dvd_iff_eq ] <;> aesop) hp4 (Nat.pos_of_ne_zero he);
      intro h_div
      have h_div_pow : padicValNat 2 (m * 2 ^ a) ≤ padicValNat 2 (p ^ e - 1) := by
        convert Nat.factorization_le_iff_dvd ( by positivity ) ( Nat.sub_ne_zero_of_lt ( one_lt_pow₀ hp.one_lt he ) ) |>.2 h_div 2 using 1;
      rw [ padicValNat.mul ] at h_div_pow <;> simp_all +decide;
      · exact Nat.dvd_trans ( pow_dvd_pow _ h_div_pow ) ( Nat.ordProj_dvd _ _ );
      · finiteness;
  · intro he_div
    have h_div : 2 ^ (padicValNat 2 (p - 1) + a) ∣ p ^ e - 1 := by
      rcases e.eq_zero_or_pos with rfl | he_pos <;> simp_all +decide [ Nat.pow_add ];
      have h_div : padicValNat 2 (p ^ e - 1) ≥ padicValNat 2 (p - 1) + a := by
        have h_div : padicValNat 2 (p ^ e - 1) = padicValNat 2 (p - 1) + padicValNat 2 e := by
          apply val_two_pow_sub_one hp.one_lt (by
          rw [ hp.dvd_iff_eq ] <;> aesop) hp4 he_pos;
        obtain ⟨ k, hk ⟩ := he_div; simp_all +decide [ padicValNat.mul, ne_of_gt ] ;
      rw [ ← pow_add ] ; exact Nat.dvd_trans ( pow_dvd_pow _ h_div ) ( Nat.ordProj_dvd _ _ ) ;
    -- Since $m = 2^{\text{padicValNat } 2 (p - 1)} \cdot t$ where $t$ is odd, we can write $m \cdot 2^a = 2^{\text{padicValNat } 2 (p - 1) + a} \cdot t$.
    obtain ⟨t, ht⟩ : ∃ t, m = 2 ^ padicValNat 2 (p - 1) * t ∧ Odd t := by
      refine' ⟨ m / 2 ^ padicValNat 2 ( p - 1 ), Eq.symm ( Nat.mul_div_cancel' <| hval ▸ Nat.ordProj_dvd _ _ ), _ ⟩;
      rw [ ← hval, Nat.odd_iff ];
      exact Nat.mod_two_ne_zero.mp fun contra => absurd ( Nat.dvd_of_mod_eq_zero contra ) ( Nat.not_dvd_ordCompl ( by norm_num ) ( by aesop ) );
    convert Nat.lcm_dvd h_div ( show t ∣ p ^ e - 1 from ?_ ) using 1;
    · rw [ ht.1, Nat.Coprime.lcm_eq_mul ] <;> ring_nf ; simp_all +decide [ Nat.coprime_mul_iff_left ] ;
      exact ⟨ Nat.Coprime.pow_left _ ( Nat.prime_two.coprime_iff_not_dvd.mpr <| by simpa [ ← even_iff_two_dvd ] using ht.2 ), Nat.Coprime.pow_left _ ( Nat.prime_two.coprime_iff_not_dvd.mpr <| by simpa [ ← even_iff_two_dvd ] using ht.2 ) ⟩;
    · exact dvd_trans ( ht.1.symm ▸ dvd_mul_left _ _ ) hm |> dvd_trans <| by simpa [ ← Int.natCast_dvd_natCast, hp.pos ] using sub_one_dvd_pow_sub_one _ _;

/-
Bridge: `(p : ZMod n)^e = 1 ↔ n ∣ p^e - 1` (for `1 < p`).
-/
lemma pow_eq_one_iff {p n e : ℕ} (hp1 : 1 < p) :
    (p : ZMod n) ^ e = 1 ↔ n ∣ p ^ e - 1 := by
  rcases p with ( _ | _ | p ) <;> simp_all +decide [ ← ZMod.natCast_eq_zero_iff ];
  rw [ sub_eq_zero ]

/-
**2-adic tower criterion** (`lem:ext-tower-criterion`).
For a prime `p ≡ 1 (mod 4)`, a divisor `m ∣ p-1` with `v₂(m) = v₂(p-1)`, and any `a`,
the multiplicative order of `p` modulo `m · 2^a` equals `2^a`.
-/
theorem tower_criterion {p m a : ℕ} (hp : Nat.Prime p) (hp4 : 4 ∣ p - 1) (hm : m ∣ p - 1)
    (hm0 : 0 < m) (hval : padicValNat 2 m = padicValNat 2 (p - 1)) :
    orderOf (p : ZMod (m * 2 ^ a)) = 2 ^ a := by
  apply Nat.dvd_antisymm;
  · rw [ orderOf_dvd_iff_pow_eq_one ];
    convert pow_eq_one_iff ?_ |>.2 ?_ using 1;
    · exact hp.one_lt;
    · exact dvd_iff hp hp4 hm hm0 hval |>.2 ( dvd_refl _ );
  · -- By definition of order, we know that $p^{orderOf(p)} \equiv 1 \pmod{m \cdot 2^a}$.
    have h_order : (p : ℕ) ^ orderOf (p : ZMod (m * 2 ^ a)) ≡ 1 [MOD m * 2 ^ a] := by
      simp +decide [ ← ZMod.natCast_eq_natCast_iff, pow_orderOf_eq_one ];
    convert dvd_iff hp hp4 hm hm0 hval |>.1 ( Nat.dvd_of_mod_eq_zero _ ) using 1;
    exact Nat.mod_eq_zero_of_dvd <| by simpa [ ← Int.natCast_dvd_natCast, Nat.cast_sub <| Nat.one_le_pow _ _ hp.pos ] using h_order.symm.dvd;

end ExtTower