import Mathlib

/-!
# Exact deployed unsafe certificates for Reed–Solomon MCA

This file formalizes the *unconditional* arithmetic content of the paper
"The Reed–Solomon MCA Frontier for the Proximity Prize", specifically the
exact integer certificates of the theorem *exact identity-scale unsafe
certificates* (`sec:deployed-unsafe`) and the equivalent comparisons listed
in the appendices *exact arithmetic certificate format* (`app:cert`) and the
*minimal verification script* (`app:script`).

The underlying combinatorics (the identity-prefix floor
`|List(RS[F,D,K], 1-m/n, U)| ≥ ⌈binom(n,m)/|B|^w⌉` and the simple-pole
conversion) reduce each deployed claim to a handful of exact integer
comparisons on very large numbers.  Those comparisons are what is verified
here, by kernel-checked computation.

Common parameters: the deployed rows use evaluation domain size
`n = 2^21` and dimension `k = 2^20`.

For each row we record three kinds of statement, matching the script
`check_mca` / `check_list`:

* `*_pass`   : the unsafe comparison at the deployed agreement `m` holds;
* `*_next`   : the *same* comparison fails one step later (at `m+1`, `w+1`),
               i.e. `m` is exactly the edge;
* `*_pole`   : (MCA rows only) the simple-pole slope-budget inequality
               `binom(L₀,2)·k < q - n`, with `L₀ = ⌊q/2^bits⌋ + 1`.
-/

namespace RSMCACertificates

/-- Evaluation domain size of the deployed rows, `n = 2^21`. -/
def n : ℕ := 2 ^ 21

/-- Dimension of the deployed rows, `k = 2^20`. -/
def k : ℕ := 2 ^ 20

/-- KoalaBear base-field characteristic prime `p = 2^31 - 2^24 + 1`. -/
def pKB : ℕ := 2 ^ 31 - 2 ^ 24 + 1

/-- Mersenne-31 prime `p' = 2^31 - 1`. -/
def pM31 : ℕ := 2 ^ 31 - 1

/-! ## (a) KoalaBear MCA row (`m = 1116047`, `w = 67470`, extension `6`, target `2^-128`) -/

/-- KoalaBear MCA, pass at `m = 1116047`:
`binom(2^21, 1116047) > p^67470 · ⌊p^6 / 2^128⌋`. -/
theorem koalabear_mca_pass :
    Nat.choose n 1116047 > pKB ^ 67470 * (pKB ^ 6 / 2 ^ 128) := by
  native_decide

/-- KoalaBear MCA, failure one step later at `m = 1116048`, `w = 67471`:
`binom(2^21, 1116048) ≤ p^67471 · ⌊p^6 / 2^128⌋`. -/
theorem koalabear_mca_next :
    ¬ (Nat.choose n 1116048 > pKB ^ 67471 * (pKB ^ 6 / 2 ^ 128)) := by
  native_decide

/-- KoalaBear MCA, simple-pole slope-budget inequality
`binom(L₀,2)·k < q - n` with `L₀ = ⌊p^6 / 2^128⌋ + 1`. -/
theorem koalabear_mca_pole :
    ((pKB ^ 6 / 2 ^ 128) + 1) * (pKB ^ 6 / 2 ^ 128) / 2 * k < pKB ^ 6 - n := by
  native_decide

/-! ## (b) KoalaBear list row (`m = 1116046`, `w = 67470`, extension `6`, target `2^-128`) -/

/-- KoalaBear list, pass at `m = 1116046`:
`binom(2^21, 1116046) · 2^128 > p^67470 · p^6`. -/
theorem koalabear_list_pass :
    Nat.choose n 1116046 * 2 ^ 128 > pKB ^ 67470 * pKB ^ 6 := by
  native_decide

/-- KoalaBear list, failure one step later at `m = 1116047`, `w = 67471`:
`binom(2^21, 1116047) · 2^128 ≤ p^67471 · p^6`. -/
theorem koalabear_list_next :
    ¬ (Nat.choose n 1116047 * 2 ^ 128 > pKB ^ 67471 * pKB ^ 6) := by
  native_decide

/-! ## (c) Mersenne-31 MCA row (`m = 1116023`, `w = 67446`, extension `4`, target `2^-100`) -/

/-- Mersenne-31 MCA, pass at `m = 1116023`:
`binom(2^21, 1116023) > p'^67446 · ⌊p'^4 / 2^100⌋`. -/
theorem mersenne31_mca_pass :
    Nat.choose n 1116023 > pM31 ^ 67446 * (pM31 ^ 4 / 2 ^ 100) := by
  native_decide

/-- Mersenne-31 MCA, failure one step later at `m = 1116024`, `w = 67447`:
`binom(2^21, 1116024) ≤ p'^67447 · ⌊p'^4 / 2^100⌋`. -/
theorem mersenne31_mca_next :
    ¬ (Nat.choose n 1116024 > pM31 ^ 67447 * (pM31 ^ 4 / 2 ^ 100)) := by
  native_decide

/-- Mersenne-31 MCA, simple-pole slope-budget inequality
`binom(L₀,2)·k < q - n` with `L₀ = ⌊p'^4 / 2^100⌋ + 1`. -/
theorem mersenne31_mca_pole :
    ((pM31 ^ 4 / 2 ^ 100) + 1) * (pM31 ^ 4 / 2 ^ 100) / 2 * k < pM31 ^ 4 - n := by
  native_decide

/-! ## (d) Mersenne-31 list row (`m = 1116022`, `w = 67446`, extension `4`, target `2^-100`) -/

/-- Mersenne-31 list, pass at `m = 1116022`:
`binom(2^21, 1116022) · 2^100 > p'^67446 · p'^4`. -/
theorem mersenne31_list_pass :
    Nat.choose n 1116022 * 2 ^ 100 > pM31 ^ 67446 * pM31 ^ 4 := by
  native_decide

/-- Mersenne-31 list, failure one step later at `m = 1116023`, `w = 67447`:
`binom(2^21, 1116023) · 2^100 ≤ p'^67447 · p'^4`. -/
theorem mersenne31_list_next :
    ¬ (Nat.choose n 1116023 * 2 ^ 100 > pM31 ^ 67447 * pM31 ^ 4) := by
  native_decide

end RSMCACertificates
