import Mathlib

open Nat

set_option maxHeartbeats 8000000

/-
Reduce a `choose` inequality to a `descFactorial` inequality (cancel `j!`).
-/
lemma choose_le_of_descFactorial {n j c b : ℕ}
    (h : n.descFactorial j ≤ c * b.descFactorial j) :
    n.choose j ≤ c * b.choose j := by
  rw [ Nat.descFactorial_eq_factorial_mul_choose, Nat.descFactorial_eq_factorial_mul_choose ] at h;
  nlinarith [ Nat.factorial_pos j ]

/-
The `j = 1` arithmetic case (already in `descFactorial` form).
-/
lemma case1 (n R3 : ℕ) (hn : 512 ≤ n) (h : n ≤ 6 * R3 + 4) :
    n.descFactorial 1 ≤ (R3 + 2) * (R3 + 1).descFactorial 1 := by
  norm_num [ Nat.descFactorial ] ; nlinarith [ show R3 ≥ 84 by contrapose! h; interval_cases R3 <;> linarith ] ;

/-
The `j = 2` arithmetic case.
-/
lemma case2 (n R3 : ℕ) (hn : 512 ≤ n) (h : n ≤ 6 * R3 + 4) :
    n.descFactorial 2 ≤ (R3 + 2) * (R3 + 1).descFactorial 2 := by
  simp [Nat.descFactorial];
  zify;
  rw [ Nat.cast_sub ] <;> push_cast <;> nlinarith [ Nat.pow_le_pow_left ( show R3 ≥ 85 by omega ) 2 ]

/-
The `j = 3` arithmetic case.
-/
lemma case3 (n R3 : ℕ) (hn : 512 ≤ n) (h : 3 * n ≤ 12 * R3 + 8) :
    n.descFactorial 3 ≤ (R3 + 2) * (R3 + 1).descFactorial 3 := by
  zify [ Nat.descFactorial_succ ];
  rcases R3 with ( _ | _ | R3 ) <;> norm_num at *;
  · grind;
  · grind;
  · rw [ Nat.cast_sub, Nat.cast_sub ] <;> push_cast <;> try linarith;
    nlinarith [ sq_nonneg ( ( n : ℤ ) - 512 ), sq_nonneg ( ( R3 : ℤ ) - 128 ), mul_le_mul_of_nonneg_left ( show ( n : ℤ ) ≤ 4 * ( R3 + 1 + 1 ) + 2 by linarith ) ( show ( 0 : ℤ ) ≤ R3 + 1 + 1 by linarith ) ]

/-
`2 * 2^(e-i) ≤ 2^e` when `1 ≤ i ≤ e`.
-/
lemma two_k_le (e i : ℕ) (hie : i ≤ e) (hi : 1 ≤ i) : 2 * 2 ^ (e - i) ≤ 2 ^ e := by
  rw [ ← pow_succ' ] ; exact pow_le_pow_right₀ ( by decide ) ( by omega ) ;

/-
For even `i` with `i ≤ e`, `3 ∣ 2^e - 2^(e-i)`.
-/
lemma dvd_three_of_even (e i : ℕ) (hie : i ≤ e) (hev : Even i) :
    3 ∣ (2 ^ e - 2 ^ (e - i)) := by
  -- Since $i$ is even, $2^i - 1$ is divisible by $3$.
  have h_div_3 : 3 ∣ (2 ^ i - 1) := by
    obtain ⟨ k, rfl ⟩ := even_iff_two_dvd.mp hev; simpa only [ one_pow, pow_mul ] using Nat.sub_dvd_pow_sub_pow _ 1 k;
  convert h_div_3.mul_left ( 2 ^ ( e - i ) ) using 1 ; rw [ mul_tsub, mul_one, ← pow_add, Nat.sub_add_cancel hie ]

/-
For odd `i` with `i ≤ e`, `3 ∤ 2^e - 2^(e-i)`.
-/
lemma not_dvd_three_of_odd (e i : ℕ) (hie : i ≤ e) (hod : Odd i) :
    ¬ (3 ∣ (2 ^ e - 2 ^ (e - i))) := by
  -- Since `i` is odd, `e` and `e - i` have opposite parity, so one of `(-1)^e,(-1)^(e-i)` is `1` and the other `-1`, giving difference `±2 ≠ 0` in `ZMod 3`.
  have h_parity : (-1 : ZMod 3) ^ e - (-1 : ZMod 3) ^ (e - i) ≠ 0 := by
    by_cases he : Even e <;> by_cases hi : Even ( e - i ) <;> simp_all +decide [ parity_simps ];
    · exact absurd hi ( by simpa using hod );
    · cases le_iff_exists_add'.mp hie ; simp_all +decide [ parity_simps ];
      by_cases hw : Even ‹_› <;> simp_all +decide;
      exact absurd he ( by simpa using hod );
    · grind;
  convert h_parity using 1;
  rw [ ← ZMod.natCast_eq_zero_iff ] ;
  rw [ Nat.cast_sub ( pow_le_pow_right₀ ( by decide ) ( Nat.sub_le _ _ ) ) ] ; norm_num [ ← ZMod.intCast_eq_intCast_iff ] ;
  erw [ show ( 2 : ZMod 3 ) = -1 by decide ]

/-
For `2 ≤ i ≤ e`, `3 * 2^e ≤ 4 * (2^e - 2^(e-i))`.
-/
lemma three_n_le_four_m (e i : ℕ) (hie : i ≤ e) (hi2 : 2 ≤ i) :
    3 * 2 ^ e ≤ 4 * (2 ^ e - 2 ^ (e - i)) := by
  rw [ show 2 ^ e = 2 ^ ( e - i ) * 2 ^ i by rw [ ← pow_add, Nat.sub_add_cancel hie ] ];
  nlinarith [ Nat.sub_add_cancel ( show 2 ^ ( e - i ) ≤ 2 ^ ( e - i ) * 2 ^ i from Nat.le_mul_of_pos_right _ ( pow_pos ( by decide ) _ ) ), pow_pos ( by decide : 0 < 2 ) ( e - i ), pow_le_pow_right₀ ( by decide : 1 ≤ 2 ) hi2 ]

/-- Dyadic packing inequality. For a dyadic rate `2^(-i)`, block length `n = 2^e`
with `n ≥ 512` and `i ≤ e`, message length `k = 2^(e-i)`, redundancy `m = n - k`,
`R3 = ⌊m/3⌋`, and small exponent `j = 3 - (m mod 3)`, the binomial ratio
`C(n,j)/C(R3+1,j)` is at most `R3 + 2`, stated multiplicatively. -/
theorem dyadic_packing_bound
    (i e n k m R3 j : ℕ)
    (hi : 1 ≤ i) (he : 9 ≤ e) (hie : i ≤ e)
    (hn : n = 2 ^ e) (hk : k = 2 ^ (e - i))
    (hm : m = n - k) (hR3 : R3 = m / 3) (hj : j = 3 - m % 3) :
    Nat.choose n j ≤ (R3 + 2) * Nat.choose (R3 + 1) j := by
  -- basic facts
  have hn512 : 512 ≤ n := by
    rw [hn]; calc (512 : ℕ) = 2 ^ 9 := by norm_num
      _ ≤ 2 ^ e := Nat.pow_le_pow_right (by norm_num) he
  have hmv : m = 2 ^ e - 2 ^ (e - i) := by rw [hm, hn, hk]
  have hk2n : 2 * 2 ^ (e - i) ≤ 2 ^ e := two_k_le e i hie hi
  -- from k ≤ n and m = n - k
  have hkle : 2 ^ (e - i) ≤ 2 ^ e := Nat.pow_le_pow_right (by norm_num) (Nat.sub_le e i)
  have h2m : n ≤ 2 * m := by
    rw [hmv, hn]; omega
  have hR3lo : 3 * R3 ≤ m := by rw [hR3]; omega
  have hR3hi : m ≤ 3 * R3 + 2 := by rw [hR3]; omega
  obtain ⟨hj1, hju⟩ : 1 ≤ j ∧ j ≤ 3 := by
    have : m % 3 < 3 := Nat.mod_lt _ (by norm_num)
    omega
  -- case split on parity of i
  rcases Nat.even_or_odd i with hev | hod
  · -- i even: j = 3
    have hdvd : 3 ∣ m := by rw [hmv]; exact dvd_three_of_even e i hie hev
    have hi2 : 2 ≤ i := by obtain ⟨t, ht⟩ := hev; omega
    have hjval : j = 3 := by omega
    have h4m : 3 * n ≤ 4 * m := by
      rw [hmv, hn]; exact three_n_le_four_m e i hie hi2
    have hbound : 3 * n ≤ 12 * R3 + 8 := by omega
    rw [hjval]
    exact choose_le_of_descFactorial (case3 n R3 hn512 hbound)
  · -- i odd: j ≤ 2
    have hnd : ¬ 3 ∣ m := by rw [hmv]; exact not_dvd_three_of_odd e i hie hod
    have hjle : j ≤ 2 := by omega
    have hbound : n ≤ 6 * R3 + 4 := by omega
    interval_cases j
    · exact choose_le_of_descFactorial (case1 n R3 hn512 hbound)
    · exact choose_le_of_descFactorial (case2 n R3 hn512 hbound)
#print axioms dyadic_packing_bound
