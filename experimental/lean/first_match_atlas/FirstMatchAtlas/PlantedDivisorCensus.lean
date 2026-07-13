/-!
# C3 planted-divisor census — Lean statement target

Companion to `experimental/notes/thresholds/c3_planted_divisor_census.md` and
its verifier `experimental/scripts/verify_c3_planted_divisor_census.py`.
First packet shipped under the 2026-07-13 Shipping rule: theorem-shaped
claims also carry a Lean statement stub.

Maps to hard input 1 (witness-exhaustive first-match atlas), cell **C3**
(planted-block, `asymptotic_rs_mca_frontiers.tex` L2399-2407) and the census
obligation of `def:algebraically-planted` (L7584-7595) /
`prop:planted-payment` (L4652-4657): "the allowed planted divisors of size
`ℓ` form a family of `e^{o(n)}` candidates."

`cosetCensusTotal N` is the Lean mirror of the note's BLOCK B/E closed form:
the total number of coset-type planted-divisor candidates of every size
`c ∣ N`, i.e. `∑_{c∣N} N/c`.  The substitution `e = N/c` makes this equal to
`sigmaOf N`, the ordinary sum-of-divisors function.

## What is PROVED here (`native_decide`, concrete finite instances)

Exact identities and spot values matching the Python verifier's BLOCK B/C/E/F
output for `N ∈ {12, 30, 360}`: the closed-form substitution
`cosetCensusTotal N = sigmaOf N`, the concrete `sigma` values, the
ramification-subsumption instance (inversion on `N=30` fixes exactly
`{0,15}`), and the negative-calibration gap (`cosetCensusTotal 12 = 28`
against the unrestricted `choose 12 6 = 924`).

## What is a STATEMENT TARGET ONLY (`sorry`, honestly unproved)

`sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED` states, for every `N`,
the elementary harmonic-type bound `sigmaOf N ≤ N * (1 + Nat.log2 N)`.  This
is the Nat-friendly WEAKER form of the note's real-valued elementary bound:
`σ(N) ≤ N(1+ln N)` implies it (since `ln N ≤ log2 N` for `N ≥ 1`), and the
weaker form already suffices as the formalization target for the census's
subexponential claim.  The note's PROVED status for the `ln` bound rests on
the elementary calculus argument given in the note text (`divisors(N) ⊆ {1,...,N}` ⟹ `σ(N) ≤ N·H_N ≤ N(1+ln N)`) plus the
verifier's numerical confirmation on `N = 1..50000`, **not** on this Lean
statement — proving the general `∀ N` case here is left to the proving
queue.  We do not claim, and this file does not need, the sharper classical
Grönwall/Wigert bound `σ(N) = O(N log log N)`.

No mathlib import: core Lean 4 only (`Nat.log2` is a core function),
matching the package's existing convention (`FirstMatchAtlas.lean`).
No new lakefile entry needed: this module is reached by `import` from the
package root `FirstMatchAtlas.lean`.
-/

namespace FirstMatchAtlas.PlantedDivisorCensus

/-- Divisors of `N`, by direct trial scan (mirrors the Python verifier's
`divisors_trial`, restricted to the decidable finite instances checked
below). -/
def divisorsOf (N : Nat) : List Nat :=
  ((List.range N).map (· + 1)).filter (fun d => N % d == 0)

/-- `sigma(N) = ∑_{d∣N} d`. -/
def sigmaOf (N : Nat) : Nat :=
  (divisorsOf N).foldl (· + ·) 0

/-- The coset-census total `∑_{c∣N} N/c`: for every divisor `c` of `N`, the
number of cosets of the order-`c` subgroup of `Z/N` is `N/c` (BLOCK B of the
Python verifier); summing over every achievable planted-block size `c`
gives this total, which the `e = N/c` substitution identifies with
`sigmaOf N`. -/
def cosetCensusTotal (N : Nat) : Nat :=
  ((divisorsOf N).map (fun c => N / c)).foldl (· + ·) 0

/-- Elementary (unmemoized) binomial coefficient, core Lean only. -/
def choose : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => choose n k + choose n (k + 1)

/-- Fixed points of the multiplier automorphism `k ↦ m*k mod N` on `Z/N`,
by direct brute-force scan (mirrors the Python verifier's
`fixed_points_bruteforce`, BLOCK C). -/
def fixedPoints (N m : Nat) : List Nat :=
  (List.range N).filter (fun k => (m * k) % N == k)

/-! ## PROVED: exact census identities and spot values -/

theorem divisorsOf_12_value : divisorsOf 12 = [1, 2, 3, 4, 6, 12] := by native_decide
theorem sigmaOf_12_value : sigmaOf 12 = 28 := by native_decide
theorem sigmaOf_30_value : sigmaOf 30 = 72 := by native_decide
theorem sigmaOf_360_value : sigmaOf 360 = 1170 := by native_decide

theorem cosetCensusTotal_eq_sigma_12 :
    cosetCensusTotal 12 = sigmaOf 12 := by native_decide
theorem cosetCensusTotal_eq_sigma_30 :
    cosetCensusTotal 30 = sigmaOf 30 := by native_decide
theorem cosetCensusTotal_eq_sigma_360 :
    cosetCensusTotal 360 = sigmaOf 360 := by native_decide

/-- Ramification subsumption spot instance: inversion (`m = N-1 = 29`) on
`N = 30` fixes exactly `{0, 15}` — the identity coset of the order-2
subgroup, already counted by `cosetCensusTotal`.  Matches
`lem:circle-edge-cases-repaired`'s "at most two ramification points" and the
note's Claim 3. -/
theorem inversion_fixed_30 : fixedPoints 30 29 = [0, 15] := by native_decide

/-- Negative-calibration spot instance (note's BLOCK F, Claim 5): the
coset-type census total at `N = 12` is dwarfed by the unrestricted binomial
count at the same scale. -/
theorem gap_at_12 : cosetCensusTotal 12 < choose 12 6 := by native_decide
theorem gap_at_12_value : choose 12 6 = 924 := by native_decide

/-- The `Nat.log2` bound holds at every spot instance checked so far
(consistent with, but not a proof of, the general target below). -/
theorem log2_bound_spot_12 : sigmaOf 12 ≤ 12 * (1 + Nat.log2 12) := by native_decide
theorem log2_bound_spot_30 : sigmaOf 30 ≤ 30 * (1 + Nat.log2 30) := by native_decide
theorem log2_bound_spot_360 : sigmaOf 360 ≤ 360 * (1 + Nat.log2 360) := by native_decide

/-! ## STATEMENT TARGET — UNPROVED

`prop:planted-payment`'s hypothesis ("a family of `e^{o(n)}` candidates")
specialized to the coset-type generator family, as a concrete Nat bound.
Honestly marked unproved: proving this for all `N` needs a harmonic-number
lemma not developed in this core-Lean-only package. -/
theorem sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED :
    ∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N) := by
  sorry

end FirstMatchAtlas.PlantedDivisorCensus
