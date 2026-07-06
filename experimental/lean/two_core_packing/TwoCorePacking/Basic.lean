import Mathlib

/-!
# Universal packing lemma (two-core closure)

This file formalizes and proves the "universal packing lemma" that upgrades the
two-core closure coding-theory result to `PROVED` for all four admissible
Reed–Solomon rates `ρ = k/n ∈ {1/2, 1/4, 1/8, 1/16}` at every power-of-two block
length `n = 2^e` with `e ≥ 9`.

For `e ≥ 9` and `den ∈ {2, 4, 8, 16}` set
  `n = 2^e`, `k = n / den`, `m = n - k`, `R3 = ⌊m/3⌋`, `j = 3 - (m % 3)`.
The main theorem `universal_packing` states
  `Nat.choose n j ≤ (R3 + 2) * Nat.choose (R3 + 1) j`,
the Case-A packing bound of the a426 two-core dichotomy.

Source note: `experimental/notes/certificate_scanner/two_core_closure_general.md`,
section "Universal packing lemma".

The proof is fully constructive (no `sorry`, no extra axioms beyond Lean/Mathlib
defaults). The exponent `e` is symbolic throughout; the four rates are handled by
a case split on `den`, and the value of `j ∈ {1,2,3}` is determined per rate from
`m % 3` (with `j = 3` exactly for `den ∈ {4,16}` and `j ∈ {1,2}` for `den ∈ {2,8}`,
the latter using that `3 ∤ 2^t`).
-/

open Nat

namespace TwoCorePacking

/-- Split a power of two: `2^e = 2^t * 2^(e-t)` when `t ≤ e`. -/
theorem two_pow_split (e t : ℕ) (h : t ≤ e) : 2 ^ e = 2 ^ t * 2 ^ (e - t) := by
  rw [← pow_add]; congr 1; omega

/-- Multiplying by `j !` converts a descending-factorial inequality of the shape
`n.descFactorial j ≤ c * a.descFactorial j` into the binomial inequality
`n.choose j ≤ c * a.choose j`. -/
theorem choose_le_of_descFactorial_le {n a c j : ℕ}
    (h : n.descFactorial j ≤ c * a.descFactorial j) :
    n.choose j ≤ c * a.choose j := by
  have key : j ! * n.choose j ≤ j ! * (c * a.choose j) := by
    calc j ! * n.choose j = n.descFactorial j :=
          (Nat.descFactorial_eq_factorial_mul_choose n j).symm
      _ ≤ c * a.descFactorial j := h
      _ = c * (j ! * a.choose j) := by rw [Nat.descFactorial_eq_factorial_mul_choose a j]
      _ = j ! * (c * a.choose j) := by ring
  exact Nat.le_of_mul_le_mul_left key (Nat.factorial_pos j)

/-- Core polynomial packing inequality for `j = 1`. -/
theorem desc1 (n R3 : ℕ) (hub : n ≤ 6 * R3 + 4) (hlb : 85 ≤ R3) :
    n.descFactorial 1 ≤ (R3 + 2) * (R3 + 1).descFactorial 1 := by
  rw [Nat.descFactorial_one, Nat.descFactorial_one]
  nlinarith [hlb, hub, Nat.mul_le_mul hlb (le_refl R3)]

/-- Core polynomial packing inequality for `j = 2`. -/
theorem desc2 (n R3 : ℕ) (hub : n ≤ 6 * R3 + 4) (hlb : 85 ≤ R3) :
    n.descFactorial 2 ≤ (R3 + 2) * (R3 + 1).descFactorial 2 := by
  have hR : (R3 + 1).descFactorial 2 = R3 * (R3 + 1) := by
    rw [show (2 : ℕ) = 1 + 1 from rfl, Nat.descFactorial_succ, Nat.descFactorial_one]
    simp
  rw [hR]
  refine le_trans (Nat.descFactorial_le_pow n 2) ?_
  refine le_trans (Nat.pow_le_pow_left hub 2) ?_
  have key : 85 * (R3 * R3) ≤ R3 * (R3 * R3) := Nat.mul_le_mul hlb (le_refl (R3 * R3))
  nlinarith [hlb, key]

/-- Core polynomial packing inequality for `j = 3`. -/
theorem desc3 (n R3 : ℕ) (hub : n ≤ 4 * R3) (hlb : 128 ≤ R3) :
    n.descFactorial 3 ≤ (R3 + 2) * (R3 + 1).descFactorial 3 := by
  have hR : (R3 + 1).descFactorial 3 = (R3 - 1) * (R3 * (R3 + 1)) := by
    rw [show (3 : ℕ) = 2 + 1 from rfl, Nat.descFactorial_succ,
        show (2 : ℕ) = 1 + 1 from rfl, Nat.descFactorial_succ, Nat.descFactorial_one]
    simp [Nat.mul_comm, Nat.mul_assoc]
  rw [hR]
  refine le_trans (Nat.descFactorial_le_pow n 3) ?_
  refine le_trans (Nat.pow_le_pow_left hub 3) ?_
  obtain ⟨b, rfl⟩ : ∃ b, R3 = b + 1 := ⟨R3 - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  have hb : 127 ≤ b := by omega
  nlinarith [hb, Nat.mul_le_mul hb (le_refl (b * b)),
    Nat.mul_le_mul hb (le_refl (b * b * b)), sq_nonneg b]

/-- **Universal packing lemma.**

For a natural exponent `e ≥ 9` and a rate denominator `den ∈ {2, 4, 8, 16}`, with
`n = 2^e`, `k = n / den`, `m = n - k`, `R3 = ⌊m/3⌋` and `j = 3 - (m % 3)`, one has
`Nat.choose n j ≤ (R3 + 2) * Nat.choose (R3 + 1) j`. -/
theorem universal_packing
    (e den n k m R3 j : ℕ)
    (he : 9 ≤ e)
    (hden : den = 2 ∨ den = 4 ∨ den = 8 ∨ den = 16)
    (hn : n = 2 ^ e)
    (hk : k = n / den)
    (hm : m = n - k)
    (hR3 : R3 = m / 3)
    (hj : j = 3 - m % 3) :
    Nat.choose n j ≤ (R3 + 2) * Nat.choose (R3 + 1) j := by
  rcases hden with h | h | h | h
  · -- den = 2, j ∈ {1, 2}
    rw [h] at hk
    obtain ⟨p, hp, hpge, hp3⟩ : ∃ p, n = 2 * p ∧ 256 ≤ p ∧ ¬ (3 ∣ p) := by
      refine ⟨2 ^ (e - 1), ?_, ?_, ?_⟩
      · rw [hn, two_pow_split e 1 (by omega)]; norm_num
      · calc (256 : ℕ) = 2 ^ 8 := by norm_num
          _ ≤ 2 ^ (e - 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
      · intro hd; exact absurd (Nat.Prime.dvd_of_dvd_pow (by norm_num) hd) (by decide)
    have hm_eq : m = p := by omega
    have hmod : m % 3 ≠ 0 := fun h0 => hp3 (hm_eq ▸ Nat.dvd_of_mod_eq_zero h0)
    rcases (show m % 3 = 1 ∨ m % 3 = 2 by omega) with h1 | h1
    · -- j = 2
      have hj2 : j = 2 := by omega
      have hub : n ≤ 6 * R3 + 4 := by omega
      have hlb : 85 ≤ R3 := by omega
      subst hj2
      exact choose_le_of_descFactorial_le (desc2 n R3 hub hlb)
    · -- j = 1
      have hj1 : j = 1 := by omega
      have hub : n ≤ 6 * R3 + 4 := by omega
      have hlb : 85 ≤ R3 := by omega
      subst hj1
      exact choose_le_of_descFactorial_le (desc1 n R3 hub hlb)
  · -- den = 4, j = 3
    rw [h] at hk
    obtain ⟨p, hp, hpge⟩ : ∃ p, n = 4 * p ∧ 128 ≤ p := by
      refine ⟨2 ^ (e - 2), ?_, ?_⟩
      · rw [hn, two_pow_split e 2 (by omega)]; norm_num
      · calc (128 : ℕ) = 2 ^ 7 := by norm_num
          _ ≤ 2 ^ (e - 2) := Nat.pow_le_pow_right (by norm_num) (by omega)
    have hj3 : j = 3 := by omega
    have hub : n ≤ 4 * R3 := by omega
    have hlb : 128 ≤ R3 := by omega
    subst hj3
    exact choose_le_of_descFactorial_le (desc3 n R3 hub hlb)
  · -- den = 8, j ∈ {1, 2}
    rw [h] at hk
    obtain ⟨p, hp, hpge, hp3⟩ : ∃ p, n = 8 * p ∧ 64 ≤ p ∧ ¬ (3 ∣ p) := by
      refine ⟨2 ^ (e - 3), ?_, ?_, ?_⟩
      · rw [hn, two_pow_split e 3 (by omega)]; norm_num
      · calc (64 : ℕ) = 2 ^ 6 := by norm_num
          _ ≤ 2 ^ (e - 3) := Nat.pow_le_pow_right (by norm_num) (by omega)
      · intro hd; exact absurd (Nat.Prime.dvd_of_dvd_pow (by norm_num) hd) (by decide)
    have hm_eq : m = 7 * p := by omega
    have hmod : m % 3 ≠ 0 := by
      intro h0
      have hd3 : (3 : ℕ) ∣ 7 * p := hm_eq ▸ Nat.dvd_of_mod_eq_zero h0
      rcases (Nat.Prime.dvd_mul (by norm_num : Nat.Prime 3)).1 hd3 with h7 | hpp
      · exact absurd h7 (by decide)
      · exact hp3 hpp
    rcases (show m % 3 = 1 ∨ m % 3 = 2 by omega) with h1 | h1
    · -- j = 2
      have hj2 : j = 2 := by omega
      have hub : n ≤ 6 * R3 + 4 := by omega
      have hlb : 85 ≤ R3 := by omega
      subst hj2
      exact choose_le_of_descFactorial_le (desc2 n R3 hub hlb)
    · -- j = 1
      have hj1 : j = 1 := by omega
      have hub : n ≤ 6 * R3 + 4 := by omega
      have hlb : 85 ≤ R3 := by omega
      subst hj1
      exact choose_le_of_descFactorial_le (desc1 n R3 hub hlb)
  · -- den = 16, j = 3
    rw [h] at hk
    obtain ⟨p, hp, hpge⟩ : ∃ p, n = 16 * p ∧ 32 ≤ p := by
      refine ⟨2 ^ (e - 4), ?_, ?_⟩
      · rw [hn, two_pow_split e 4 (by omega)]; norm_num
      · calc (32 : ℕ) = 2 ^ 5 := by norm_num
          _ ≤ 2 ^ (e - 4) := Nat.pow_le_pow_right (by norm_num) (by omega)
    have hj3 : j = 3 := by omega
    have hub : n ≤ 4 * R3 := by omega
    have hlb : 128 ≤ R3 := by omega
    subst hj3
    exact choose_le_of_descFactorial_le (desc3 n R3 hub hlb)

/-! ## Non-vacuity guards

Concrete instantiations at `e = 9` (`n = 512`) for each of the four admissible
rates, confirming the hypotheses are simultaneously satisfiable (the statement is
not vacuous) and reproducing the `(R3, j)` values of the note's numeric table:
`den=2 → (85,2)`, `den=4 → (128,3)`, `den=8 → (149,2)`, `den=16 → (160,3)`. -/

example : Nat.choose 512 2 ≤ (85 + 2) * Nat.choose (85 + 1) 2 :=
  universal_packing 9 2 512 256 256 85 2 (by norm_num) (Or.inl rfl)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)

example : Nat.choose 512 3 ≤ (128 + 2) * Nat.choose (128 + 1) 3 :=
  universal_packing 9 4 512 128 384 128 3 (by norm_num) (Or.inr (Or.inl rfl))
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)

example : Nat.choose 512 2 ≤ (149 + 2) * Nat.choose (149 + 1) 2 :=
  universal_packing 9 8 512 64 448 149 2 (by norm_num) (Or.inr (Or.inr (Or.inl rfl)))
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)

example : Nat.choose 512 3 ≤ (160 + 2) * Nat.choose (160 + 1) 3 :=
  universal_packing 9 16 512 32 480 160 3 (by norm_num) (Or.inr (Or.inr (Or.inr rfl)))
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)

end TwoCorePacking

-- Confirm no unexpected axioms (in particular, no `sorryAx`).
#print axioms TwoCorePacking.universal_packing
