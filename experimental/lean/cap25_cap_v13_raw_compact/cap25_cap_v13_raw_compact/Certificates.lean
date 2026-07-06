import cap25_cap_v13_raw_compact.Conversion

/-!
# Deployed unsafe certificates, derived structurally from the identity-prefix floor

This file derives the deployed **list-row** unsafe certificates of the paper
(Theorem "exact identity-scale unsafe certificates", rows (b) and (d)) as structural
consequences of `RSMCA.identity_floor`, rather than as standalone arithmetic facts.

For a list row with dimension `K = k`, the identity-prefix floor gives an explicit
`𝔹`-valued received word whose decoding list for `RS[F, D, k]` at agreement threshold
`m` has size at least `⌊binom(n,m) / |𝔹|^{m-k}⌋`.  The deployed exact inequality says this
floor exceeds the *safe* list budget `⌊|𝔽| / 2^t⌋` (targets `t = 128` for KoalaBear,
`t = 100` for Mersenne-31).  Hence the actual list is unsafe.

The field hypotheses `Fintype.card B = p`, `Fintype.card F = q` describe a Reed–Solomon
row whose evaluation domain lies in the base field `𝔹 = 𝔽_p` while codewords are sampled
over the extension `𝔽 = 𝔽_q`; such fields exist since the KoalaBear prime
`2^31 - 2^24 + 1` and the Mersenne-31 prime `2^31 - 1` are prime.
-/

open RSMCA

namespace RSMCACertificates

variable {B F : Type*} [Field B] [Field F] [Algebra B F]
  [Fintype B] [Fintype F] [DecidableEq F] [DecidableEq B]

/-- **Structural list-unsafe criterion.** If the identity-prefix floor
`⌊binom(n,m) / |𝔹|^{m-K}⌋` already exceeds the safe list budget `⌊|𝔽| / 2^t⌋`, then there
is a `𝔹`-valued received word whose `RS[F, D, K]`-list at agreement threshold `m` exceeds
the safe budget. -/
theorem list_unsafe_of_floor (D : Finset B) (K m t : ℕ) (hKm : K ≤ m) (hmn : m ≤ D.card)
    (hcert : Fintype.card F / 2 ^ t
        < (D.card).choose m / (Fintype.card B) ^ (m - K)) :
    ∃ Ub : D → B,
      Fintype.card F / 2 ^ t
        < (listSet D K m (fun x => algebraMap B F (Ub x))).ncard := by
  obtain ⟨Ub, hUb⟩ := identity_floor (F := F) D K m hKm hmn
  exact ⟨Ub, lt_of_lt_of_le hcert hUb⟩

/-- KoalaBear list row (`n = 2^21`, `k = 2^20`, `m = 1116046`, target `t = 128`,
extension degree `6`, so `q = p^6` with `p = 2^31 - 2^24 + 1`).

The `RS[F, D, k]` decoding list at agreement `1116046` exceeds the safe budget `⌊q/2^128⌋`. -/
theorem koalabear_list_unsafe
    (hB : Fintype.card B = 2 ^ 31 - 2 ^ 24 + 1)
    (hF : Fintype.card F = (2 ^ 31 - 2 ^ 24 + 1) ^ 6)
    (D : Finset B) (hD : D.card = 2 ^ 21) :
    ∃ Ub : D → B,
      Fintype.card F / 2 ^ 128
        < (listSet D (2 ^ 20) 1116046 (fun x => algebraMap B F (Ub x))).ncard := by
  apply list_unsafe_of_floor D (2 ^ 20) 1116046 128 (by norm_num) (by rw [hD]; norm_num)
  rw [hB, hF, hD]
  native_decide

/-- Mersenne-31 list row (`n = 2^21`, `k = 2^20`, `m = 1116022`, target `t = 100`,
extension degree `4`, so `q = p'^4` with `p' = 2^31 - 1`).

The `RS[F, D, k]` decoding list at agreement `1116022` exceeds the safe budget `⌊q/2^100⌋`. -/
theorem mersenne31_list_unsafe
    (hB : Fintype.card B = 2 ^ 31 - 1)
    (hF : Fintype.card F = (2 ^ 31 - 1) ^ 4)
    (D : Finset B) (hD : D.card = 2 ^ 21) :
    ∃ Ub : D → B,
      Fintype.card F / 2 ^ 100
        < (listSet D (2 ^ 20) 1116022 (fun x => algebraMap B F (Ub x))).ncard := by
  apply list_unsafe_of_floor D (2 ^ 20) 1116022 100 (by norm_num) (by rw [hD]; norm_num)
  rw [hB, hF, hD]
  native_decide

/-! ## MCA-row certificates (via the flexible-budget simple-pole conversion) -/

/-- KoalaBear MCA slope-list floor value `L₀ = ⌊q / 2^128⌋ + 1` with `q = p^6`. -/
def koalabearL0 : ℕ := (2 ^ 31 - 2 ^ 24 + 1) ^ 6 / 2 ^ 128 + 1

/-- Mersenne-31 MCA slope-list floor value `L₀ = ⌊q / 2^100⌋ + 1` with `q = (p')^4`. -/
def mersenne31L0 : ℕ := (2 ^ 31 - 1) ^ 4 / 2 ^ 100 + 1

/-- KoalaBear MCA row (`n = 2^21`, `k = 2^20`, `m = 1116047`, `K = k+1`, target `t = 128`,
extension degree `6`, `q = p^6` with `p = 2^31 - 2^24 + 1`).

Using the identity-prefix floor for `K = k+1` and the flexible-budget simple-pole
conversion, `emca(RS[F,D,k], 1 - m/n)` exceeds the target `2^{-128}`. -/
theorem koalabear_mca_unsafe
    (hB : Fintype.card B = 2 ^ 31 - 2 ^ 24 + 1)
    (hF : Fintype.card F = (2 ^ 31 - 2 ^ 24 + 1) ^ 6)
    (D : Finset B) (hD : D.card = 2 ^ 21) :
    (1 : ℝ) / 2 ^ 128 < emca (F := F) D (2 ^ 20) 1116047 := by
  have hmain : (koalabearL0 : ℝ) / Fintype.card F ≤ emca (F := F) D (2 ^ 20) 1116047 := by
    refine emca_ge_of_floor D (2 ^ 20) 1116047 (by norm_num) (by rw [hD]; norm_num)
      koalabearL0 ?_ ?_
    · rw [hB, hD]; native_decide
    · rw [hF, hD]; native_decide
  have hcardF : Fintype.card F < koalabearL0 * 2 ^ 128 := by rw [hF]; native_decide
  calc (1 : ℝ) / 2 ^ 128 < (koalabearL0 : ℝ) / Fintype.card F :=
        ratio_lt Fintype.card_pos hcardF
    _ ≤ emca (F := F) D (2 ^ 20) 1116047 := hmain

/-- Mersenne-31 MCA row (`n = 2^21`, `k = 2^20`, `m = 1116023`, `K = k+1`, target `t = 100`,
extension degree `4`, `q = (p')^4` with `p' = 2^31 - 1`).

Using the identity-prefix floor for `K = k+1` and the flexible-budget simple-pole
conversion, `emca(RS[F,D,k], 1 - m/n)` exceeds the target `2^{-100}`. -/
theorem mersenne31_mca_unsafe
    (hB : Fintype.card B = 2 ^ 31 - 1)
    (hF : Fintype.card F = (2 ^ 31 - 1) ^ 4)
    (D : Finset B) (hD : D.card = 2 ^ 21) :
    (1 : ℝ) / 2 ^ 100 < emca (F := F) D (2 ^ 20) 1116023 := by
  have hmain : (mersenne31L0 : ℝ) / Fintype.card F ≤ emca (F := F) D (2 ^ 20) 1116023 := by
    refine emca_ge_of_floor D (2 ^ 20) 1116023 (by norm_num) (by rw [hD]; norm_num)
      mersenne31L0 ?_ ?_
    · rw [hB, hD]; native_decide
    · rw [hF, hD]; native_decide
  have hcardF : Fintype.card F < mersenne31L0 * 2 ^ 100 := by rw [hF]; native_decide
  calc (1 : ℝ) / 2 ^ 100 < (mersenne31L0 : ℝ) / Fintype.card F :=
        ratio_lt Fintype.card_pos hcardF
    _ ≤ emca (F := F) D (2 ^ 20) 1116023 := hmain

end RSMCACertificates
