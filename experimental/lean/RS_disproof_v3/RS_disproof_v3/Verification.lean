import RS_disproof_v3.Main

/-!
# Verification record: fully-checked Fermat instances (Appendix V1–V3)

This file discharges, by exact computation (`native_decide`), the concrete
verification records of the appendix of

  P. Chojecki, *Capacity-Edge Obstructions to Reed-Solomon Mutual Correlated Agreement
  over Smooth Multiplicative Domains* (`RS_disproof_v3.tex`),

for the small Fermat primes `p = 17` and `p = 257`, and turns them into fully formal,
concrete instances of Theorem 2.1(b) (error `≥ 1 - 1/p` one symbol below capacity).

The domains are the power-of-two multiplicative subgroups `Q = ⟨2⟩ ≤ 𝔽_p^×`:

* `Q17 ≤ 𝔽_17^×` of order `8` (the unique order-`8` subgroup, `{x : x^8 = 1}`);
* `Q257 ≤ 𝔽_257^×` of order `16` (the unique order-`16` subgroup, `{x : x^16 = 1}`).

For each we verify the restricted-sumset coverage `|r^∧Q| = p - 1` (V1), then feed it into
the quotient-locator lower bound `RSLocator.epsMca_ge_restrictedSumset_full` to obtain a
concrete MCA obstruction with error exactly `1 - 1/p`.

Everything here is checked by the kernel-verified reflection tactic `native_decide`
(so `Lean.ofReduceBool` appears among the axioms), with no `sorry` and no added `axiom`.
-/

open scoped BigOperators

instance : Fact (Nat.Prime 17) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 257) := ⟨by norm_num⟩

/-- The order-`8` multiplicative subgroup `⟨2⟩ ≤ 𝔽_17^×`. -/
def Q17 : Finset (ZMod 17) := {1, 2, 4, 8, 9, 13, 15, 16}

/-- The order-`16` multiplicative subgroup `⟨2⟩ ≤ 𝔽_257^×`. -/
def Q257 : Finset (ZMod 257) :=
  {1, 2, 4, 8, 16, 32, 64, 128, 256, 255, 253, 249, 241, 225, 193, 129}

/-! ### Subgroup identification -/

/-- `Q17` is exactly the unique subgroup of order `8` of `𝔽_17^×` (the eighth roots of `1`). -/
theorem Q17_eq_subgroup : Q17 = Finset.univ.filter (fun x : ZMod 17 => x ^ 8 = 1) := by
  native_decide

/-- `Q257` is exactly the unique subgroup of order `16` of `𝔽_257^×`. -/
theorem Q257_eq_subgroup : Q257 = Finset.univ.filter (fun x : ZMod 257 => x ^ 16 = 1) := by
  native_decide

theorem Q17_card : Q17.card = 8 := by native_decide
theorem Q257_card : Q257.card = 16 := by native_decide

/-! ### V1: Restricted-sumset coverage `|r^∧Q| = p - 1` -/

/-- V1 (`p = 17`, `r = M/2 + 1 = 3`, the case of Theorem 2.1(b) not covered by the
Fermat digit lemma): `|3^∧⟨2⟩| = 16 = p - 1`. -/
theorem coverage_p17_r3 : (RSLocator.restrictedSumset Q17 3).card = 16 := by native_decide

/-- V1 (`p = 17`, `r = M + 1 = 5`): `|5^∧⟨2⟩| = 16 = p - 1`. -/
theorem coverage_p17_r5 : (RSLocator.restrictedSumset Q17 5).card = 16 := by native_decide

/-- V1 (`p = 257`, `r = M/2 + 1 = 9`): `|9^∧⟨2⟩| = 256 = p - 1`. -/
theorem coverage_p257_r9 : (RSLocator.restrictedSumset Q257 9).card = 256 := by native_decide

/-! ### Concrete instances of Theorem 2.1(b): error `≥ 1 - 1/p` -/

/-- **Theorem 2.1(b) for `p = 17`.**  Over `𝔽_17` with domain `D = ⟨2⟩` (order `8`),
rate `ρ = 1/2` (`k = 4`), and radius `δ = 3/8 = 1 - ρ - 1/8` (one symbol below capacity),
the support-wise line-MCA error is at least `16/17 = 1 - 1/p`. -/
theorem thm_main_b_p17 :
    (16 : ℝ) / 17 ≤ RSLocator.epsMca Q17 4 (3 / 8 : ℝ) := by
  have hq : Q17.card = 8 := Q17_card
  have h := RSLocator.epsMca_ge_restrictedSumset_full Q17 5 4 (by norm_num)
    (by rw [hq]; norm_num) (by norm_num) (3 / 8 : ℝ) (by rw [hq]; push_cast; norm_num)
  rw [coverage_p17_r5] at h
  have hcard : (Fintype.card (ZMod 17) : ℝ) = 17 := by rw [ZMod.card]; norm_num
  rw [hcard] at h
  push_cast at h
  linarith [h]

/-- **Theorem 2.1(b) for `p = 257`.**  Over `𝔽_257` with domain `D = ⟨2⟩` (order `16`),
rate `ρ = 1/2` (`k = 8`), and radius `δ = 7/16 = 1 - ρ - 1/16` (one symbol below
capacity), the support-wise line-MCA error is at least `256/257 = 1 - 1/p`. -/
theorem thm_main_b_p257 :
    (256 : ℝ) / 257 ≤ RSLocator.epsMca Q257 8 (7 / 16 : ℝ) := by
  have hq : Q257.card = 16 := Q257_card
  have h := RSLocator.epsMca_ge_restrictedSumset_full Q257 9 8 (by norm_num)
    (by rw [hq]; norm_num) (by norm_num) (7 / 16 : ℝ) (by rw [hq]; push_cast; norm_num)
  rw [coverage_p257_r9] at h
  have hcard : (Fintype.card (ZMod 257) : ℝ) = 257 := by rw [ZMod.card]; norm_num
  rw [hcard] at h
  push_cast at h
  linarith [h]

/-! ### Deployed-field DSH ladder side-conditions (Theorem 2.1(a) numeric interval arithmetic)

Theorem 2.1(a) applies to a prime `p`, a divisor `N ∣ n` of the domain order, and a rate
`ρ` precisely when the Dias da Silva–Hamidoune coverage side-condition

  `(ρN + 1)((1-ρ)N - 1) + 1 ≥ p`

holds; DSH (the external combinatorial input) then upgrades this to full coverage
`(ρN+1)^∧Q = 𝔽_p`, giving MCA error one at radius `1 - ρ - 1/N` and above.  We certify these
arithmetic side-conditions exactly for the deployed FFT primes BabyBear `15·2²⁷+1`, KoalaBear
`2³¹-2²⁴+1`, and `3·2³⁰+1`.  With `r = ρN` and `s = (1-ρ)N = N - r`: -/

/-- The Dias da Silva–Hamidoune ladder side-condition `(r+1)(s-1)+1 ≥ p` with `r = ρN`,
`s = N - r`.  This is the exact numeric hypothesis of Theorem 2.1(a) / Lemma DSH. -/
def dshLadder (p N r : ℕ) : Prop := p ≤ (r + 1) * ((N - r) - 1) + 1

/-- `N = 2^18` qualifies at all four prize rates `ρ ∈ {1/2,1/4,1/8,1/16}` (i.e. `r ∈
{2¹⁷,2¹⁶,2¹⁵,2¹⁴}`) for BabyBear `p = 15·2²⁷+1`. -/
theorem dsh_babybear_N18 :
    dshLadder (15 * 2 ^ 27 + 1) (2 ^ 18) (2 ^ 17) ∧
    dshLadder (15 * 2 ^ 27 + 1) (2 ^ 18) (2 ^ 16) ∧
    dshLadder (15 * 2 ^ 27 + 1) (2 ^ 18) (2 ^ 15) ∧
    dshLadder (15 * 2 ^ 27 + 1) (2 ^ 18) (2 ^ 14) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> (unfold dshLadder; norm_num)

/-- `N = 2^18` qualifies at all four prize rates for KoalaBear `p = 2³¹-2²⁴+1`. -/
theorem dsh_koalabear_N18 :
    dshLadder (2 ^ 31 - 2 ^ 24 + 1) (2 ^ 18) (2 ^ 17) ∧
    dshLadder (2 ^ 31 - 2 ^ 24 + 1) (2 ^ 18) (2 ^ 16) ∧
    dshLadder (2 ^ 31 - 2 ^ 24 + 1) (2 ^ 18) (2 ^ 15) ∧
    dshLadder (2 ^ 31 - 2 ^ 24 + 1) (2 ^ 18) (2 ^ 14) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> (unfold dshLadder; norm_num)

/-- `N = 2^18` qualifies at all four prize rates for `p = 3·2³⁰+1`. -/
theorem dsh_three_N18 :
    dshLadder (3 * 2 ^ 30 + 1) (2 ^ 18) (2 ^ 17) ∧
    dshLadder (3 * 2 ^ 30 + 1) (2 ^ 18) (2 ^ 16) ∧
    dshLadder (3 * 2 ^ 30 + 1) (2 ^ 18) (2 ^ 15) ∧
    dshLadder (3 * 2 ^ 30 + 1) (2 ^ 18) (2 ^ 14) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> (unfold dshLadder; norm_num)

/-- The sharper divisor `N = 2^17` already qualifies at rates `1/2` and `1/4`
(`r ∈ {2¹⁶, 2¹⁵}`) for all three deployed primes, giving the tighter `2⁻¹⁷` radius gap. -/
theorem dsh_N17_rates_half_quarter :
    dshLadder (15 * 2 ^ 27 + 1) (2 ^ 17) (2 ^ 16) ∧
    dshLadder (15 * 2 ^ 27 + 1) (2 ^ 17) (2 ^ 15) ∧
    dshLadder (2 ^ 31 - 2 ^ 24 + 1) (2 ^ 17) (2 ^ 16) ∧
    dshLadder (2 ^ 31 - 2 ^ 24 + 1) (2 ^ 17) (2 ^ 15) ∧
    dshLadder (3 * 2 ^ 30 + 1) (2 ^ 17) (2 ^ 16) ∧
    dshLadder (3 * 2 ^ 30 + 1) (2 ^ 17) (2 ^ 15) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> (unfold dshLadder; norm_num)

/-! ### V3: Pigeonhole list sizes over `𝔽_17`

For `p = 17`, domain `D = 𝔽_17^×` (`n = 16`), `k = 8`, `ℓ = 9`: the number of `9`-subsets of
`𝔽_17^×` with each prescribed sum is `672` or `673` (mean `₁₆C₉/17 = 672.9`).  Hence every
received word `x⁹ + z·x⁸` has at least `672` degree-`<8` codewords agreeing with it on the
`9`-point witness sets, i.e. within relative distance `1 - 9/16` — the pigeonhole bound of
Theorem 2.1(d) is essentially exact here. -/

/-- `𝔽_17^×`, the order-`16` multiplicative group. -/
def D17star : Finset (ZMod 17) := Finset.univ.erase 0

/-- V3 (lower bound): every prescribed sum is achieved by at least `672` of the `9`-subsets
of `𝔽_17^×`. -/
theorem pigeonhole_p17_lb : ∀ z : ZMod 17,
    672 ≤ ((D17star.powersetCard 9).filter (fun A => ∑ b ∈ A, b = -z)).card := by
  native_decide

/-- V3 (upper bound): every prescribed sum is achieved by at most `673` of the `9`-subsets. -/
theorem pigeonhole_p17_ub : ∀ z : ZMod 17,
    ((D17star.powersetCard 9).filter (fun A => ∑ b ∈ A, b = -z)).card ≤ 673 := by
  native_decide
