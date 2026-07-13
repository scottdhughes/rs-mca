/-!
# The Sidon-paired depth-1 fiber profile is an exponential staircase (statement stub)

Maps to **hard input 2**: the CONCENTRATION clause -- the last unproved clause of
avdeevvadim's #716 charge-preserving semantic-or-signed dichotomy (Sec 6) on the
Sidon-paired depth-1 class -- flagged by #732 Theorem B as its residual
"staircase-concentration / max-fiber" hypothesis.  This packet DECIDES it,
negatively.

Note:     `experimental/notes/thresholds/staircase_concentration_sidon_paired.md`.
Verifier: `experimental/scripts/verify_staircase_concentration_sidon_paired.py`
          (88/88, tamper 3/3).

Class (#735 Thm 2 / #732 / #728 / #717 Sec 7):
  `P` distinct-subset-sum, `|P|=B`, `c > 2 sum P`, `T = P u (c-P)`, `|T|=2B`,
  `a = B`, `Phi(S) = sum_{t in S} t` over `Z`.  A support meets each twin pair
  `{A_i, c-A_i}` as empty / low-only / high-only / both; `s = #unpaired pairs`.

Central analytic results of the note (PROVED in the note + Python verifier, over
`Z` with dissociativity + binomial asymptotics; NOT in Lean):
  Thm 1  (B[+-2] base): `|Phi^{-1}(sigma)| = C(B-s, (B-s)/2)`, with `C(B,s) 2^s`
         syndromes at unpaired-count `s` (`s == B mod 2`); recovers
         `L = (3^B+1)/2`, `M = C(2B,B)`, central `W = C(B, B/2)`.
  Thm 2  (any distinct-subset-sum `P`): `>= C(B,s)` distinct syndromes each with
         fiber `>= C(B-s,(B-s)/2)`.
  Thm 3  (COUNTEREXAMPLE): for small `eta > 0`,
         `#{sigma : fiber >= e^{eta N} M/L} = e^{Theta(N)}`, and
         `min_{T_h}(#{fiber>=T_h} + max{fiber<T_h}) = e^{Theta(N)}`, `N = 2B`.
         Profile NOT staircase-concentrated -> #732 Thm B.2 fails on this class.

This module is the DECIDABLE arithmetic shadow (stdlib-only `native_decide`, no
mathlib, no `sorry`) of the parts that are integer/combinatorial:
  1. the exact fiber staircase `C(B-s,(B-s)/2)` and its central term `C(B,B/2)`;
  2. the level-count `C(B,s) 2^s` summing (weighted by the fiber) to
     `M = C(2B,B)` and (unweighted) to `L = (3^B+1)/2`;
  3. the NON-CONCENTRATION witness: at `B=60` there are more than `60^12`
     syndromes (unpaired-count `s=20`) EACH with fiber more than `60^6` -- i.e.
     super-polynomially many super-polynomially-heavy fibers, so no threshold
     separates "few heavy" from "small light" (Thm 3, defeats #732 Thm B.2's
     "at most e^{o(N)} packets").
-/

namespace StaircaseConcentrationSidonPaired

/-! ## 0. Fast exact binomial (multiplicative; stdlib `Nat`, exact division). -/

/-- `binom n k = C(n,k)` via the running product `prod_{i<k} (n-i)/(i+1)`; each
    partial quotient is exact (`= C(n, i+1)`), so `native_decide` handles large
    `n` without the exponential blow-up of naive Pascal recursion. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- The exact fiber size at unpaired-count `s` (B[+-2] base): `C(B-s,(B-s)/2)`. -/
def fiber (B s : Nat) : Nat := binom (B - s) ((B - s) / 2)

/-- The number of syndromes at unpaired-count `s`: `C(B,s) 2^s`. -/
def levelCount (B s : Nat) : Nat := binom B s * 2 ^ s

/-- Valid unpaired counts: `s` with `s == B (mod 2)`, `0 <= s <= B`. -/
def validS (B : Nat) : List Nat :=
  (List.range (B + 1)).filter (fun s => s % 2 == B % 2)

/-! ## 1. The exact staircase and central fiber (#717 Sec 7 / #735 Thm 2). -/

/-- The `B = 8` fiber staircase `C(8-s,(8-s)/2)` for `s = 0,2,4,6,8`. -/
theorem staircase_B8 :
    (validS 8).map (fun s => fiber 8 s) = [70, 20, 6, 2, 1] := by native_decide

/-- Central fiber `= C(B, B/2)` (= #735 Thm 2's twin-pair-union count). -/
theorem central_B8  : fiber 8  0 = binom 8  4  := by native_decide
theorem central_B10 : fiber 10 0 = binom 10 5  := by native_decide
theorem central_B12 : fiber 12 0 = binom 12 6  := by native_decide

/-- Level counts `C(8,s) 2^s` for `s = 0,2,4,6,8`. -/
theorem levelCounts_B8 :
    (validS 8).map (fun s => levelCount 8 s) = [1, 112, 1120, 1792, 256] := by
  native_decide

/-! ## 2. The two closed-form totals `L = (3^B+1)/2` and `M = C(2B,B)`. -/

/-- Image size: `sum_s C(B,s) 2^s = (3^B + 1)/2` (`B = 8`). -/
theorem imageSize_B8 :
    ((validS 8).map (fun s => levelCount 8 s)).foldl (· + ·) 0 = (3 ^ 8 + 1) / 2 := by
  native_decide

/-- Slice size: `sum_s [C(B,s) 2^s] * C(B-s,(B-s)/2) = C(2B,B)` (`B = 8`). -/
theorem sliceSize_B8 :
    ((validS 8).map (fun s => levelCount 8 s * fiber 8 s)).foldl (· + ·) 0
      = binom 16 8 := by native_decide

/-- Same two identities at `B = 6` (an independent check). -/
theorem imageSize_B6 :
    ((validS 6).map (fun s => levelCount 6 s)).foldl (· + ·) 0 = (3 ^ 6 + 1) / 2 := by
  native_decide
theorem sliceSize_B6 :
    ((validS 6).map (fun s => levelCount 6 s * fiber 6 s)).foldl (· + ·) 0
      = binom 12 6 := by native_decide

/-! ## 3. NON-CONCENTRATION witness (Thm 3): super-polynomially many
    super-polynomially-heavy fibers -- so the profile is NOT staircase-
    concentrated and #732 Theorem B.2's hypothesis is FALSE on this class. -/

/-- At `B = 60`, unpaired-count `s = 20`: MORE than `60^12` syndromes. -/
theorem manyHeavySyndromes_B60 : levelCount 60 20 > 60 ^ 12 := by native_decide

/-- ... EACH with fiber MORE than `60^6` (well above the mean `M/L`). -/
theorem heavyFiber_B60 : fiber 60 20 > 60 ^ 6 := by native_decide

/-- Packaged: a level with both a super-polynomial COUNT and super-polynomial
    fiber SIZE simultaneously.  No single threshold can call these few-and-heavy
    or many-and-light, which is exactly the failure of #732 Thm B.2. -/
theorem notStaircaseConcentrated_B60 :
    levelCount 60 20 > 60 ^ 12 ∧ fiber 60 20 > 60 ^ 6 :=
  ⟨manyHeavySyndromes_B60, heavyFiber_B60⟩

end StaircaseConcentrationSidonPaired
