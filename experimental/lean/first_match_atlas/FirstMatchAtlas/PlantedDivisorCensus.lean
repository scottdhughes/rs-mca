/-!
# C3 planted-divisor census — Lean formalization

Companion to `experimental/notes/thresholds/c3_planted_divisor_census.md` and
its verifier `experimental/scripts/verify_c3_planted_divisor_census.py`.
The first packet shipped under the 2026-07-13 Shipping rule with a Lean
statement stub; the general integer census bound is now proved below.

Maps to hard input 1 (witness-exhaustive first-match atlas), cell **C3**
(planted-block, `asymptotic_rs_mca_frontiers.tex` L2399-2407) and the census
obligation of `def:algebraically-planted` (L7584-7595) /
`prop:planted-payment` (L4652-4657): "the allowed planted divisors of size
`ℓ` form a family of `e^{o(n)}` candidates."

`cosetCensusTotal N` is the Lean mirror of the note's BLOCK B/E closed form:
the total number of coset-type planted-divisor candidates of every size
`c ∣ N`, i.e. `∑_{c∣N} N/c`.  The substitution `e = N/c` makes this equal to
`sigmaOf N`, the ordinary sum-of-divisors function.  This module formalizes
that identity only at the concrete instances listed below, not for all `N`.

## What is PROVED here (`native_decide`, concrete finite instances)

Exact identities and spot values matching the Python verifier's BLOCK B/C/E/F
output for `N ∈ {12, 30, 360}`: the closed-form substitution
`cosetCensusTotal N = sigmaOf N`, the concrete `sigma` values, the
ramification-subsumption instance (inversion on `N=30` fixes exactly
`{0,15}`), and the negative-calibration gap (`cosetCensusTotal 12 = 28`
against the unrestricted `choose 12 6 = 924`).

## What is now PROVED for every `N`

`sigmaOf_le_mul_one_add_log2` proves, for every `N`, the integer bound
`sigmaOf N ≤ N * (1 + Nat.log2 N)`.  The proof is direct: complement every
divisor `d` to `N / d`, inject the resulting list into the denominators
`1,...,N`, and partition those denominators into dyadic blocks
`[2^j, 2^(j+1))`.  Every block contributes at most `N`, while
`Nat.lt_log2_self` shows that `1 + Nat.log2 N` blocks cover `1,...,N`.
This avoids an invalid floor-sensitive inference from the real inequality
`ln N ≤ log₂ N`: `Nat.log2` is a floored natural logarithm, so that real
comparison alone does not imply the displayed Nat bound.  The historical
declaration names `sigmaOf_subexponential` and
`sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED` are kept as proved
compatibility aliases.  We do not claim, and this file does not need, the
sharper classical Grönwall/Wigert bound `σ(N) = O(N log log N)`.

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

/-- Concrete regressions for the general `Nat.log2` theorem below. -/
theorem log2_bound_spot_12 : sigmaOf 12 ≤ 12 * (1 + Nat.log2 12) := by native_decide
theorem log2_bound_spot_30 : sigmaOf 30 ≤ 30 * (1 + Nat.log2 30) := by native_decide
theorem log2_bound_spot_360 : sigmaOf 360 ≤ 360 * (1 + Nat.log2 360) := by native_decide

/-! ## PROVED: integer subexponential census bound

`prop:planted-payment`'s hypothesis ("a family of `e^{o(n)}` candidates")
specialized to the coset-type generator family, as a concrete Nat bound.
The proof below is entirely core Lean and uses an exact dyadic partition,
not real analysis or a floating-point logarithm comparison. -/

private theorem foldl_add_eq_sum (l : List Nat) (acc : Nat) :
    l.foldl (· + ·) acc = acc + l.sum := by
  induction l generalizing acc with
  | nil => simp
  | cons x xs ih =>
      simp only [List.foldl_cons, List.sum_cons]
      rw [ih]
      omega

private theorem sum_eq_of_perm {xs ys : List Nat} (h : List.Perm xs ys) :
    xs.sum = ys.sum := by
  change xs.foldr Nat.add 0 = ys.foldr Nat.add 0
  exact h.foldr_eq' (fun _ _ _ _ _ => by
    simp [Nat.add_comm, Nat.add_left_comm, Nat.add_assoc]) 0

private theorem sum_map_le_of_nodup_subset (w : Nat → Nat) :
    ∀ (xs ys : List Nat), xs.Nodup → xs ⊆ ys →
      (xs.map w).sum ≤ (ys.map w).sum := by
  intro xs
  induction xs with
  | nil => simp
  | cons x xs ih =>
      intro ys hNodup hSubset
      have hxMem : x ∈ ys := hSubset (List.mem_cons_self x xs)
      have hxNotMem : x ∉ xs := (List.nodup_cons.mp hNodup).1
      have hTailNodup : xs.Nodup := (List.nodup_cons.mp hNodup).2
      have hTailSubset : xs ⊆ ys.erase x := by
        intro a ha
        have hne : a ≠ x := by
          intro hax
          subst a
          exact hxNotMem ha
        exact (List.mem_erase_of_ne hne).2
          (hSubset (List.mem_cons_of_mem x ha))
      have hTail := ih (ys.erase x) hTailNodup hTailSubset
      have hPerm : List.Perm (w x :: (ys.erase x).map w) (ys.map w) :=
        ((List.perm_cons_erase hxMem).map w).symm
      have hSum : w x + ((ys.erase x).map w).sum = (ys.map w).sum :=
        sum_eq_of_perm hPerm
      simp only [List.map_cons, List.sum_cons]
      omega

private theorem divisor_data {N d : Nat} (h : d ∈ divisorsOf N) :
    1 ≤ d ∧ d ≤ N ∧ d ∣ N := by
  simp only [divisorsOf, List.mem_filter, List.mem_map,
    List.mem_range, beq_iff_eq] at h
  obtain ⟨⟨k, hk, rfl⟩, hmod⟩ := h
  simp only [Nat.dvd_iff_mod_eq_zero]
  omega

private theorem divisorsOf_nodup (N : Nat) : (divisorsOf N).Nodup := by
  unfold divisorsOf
  have hmap : ((List.range N).map (· + 1)).Nodup := by
    change ((List.range N).map (· + 1)).Pairwise (fun a b => a ≠ b)
    rw [List.pairwise_map]
    exact (List.nodup_range N).imp fun hne hEq => hne (by omega)
  exact hmap.filter _

private theorem complement_data {N d : Nat} (h : d ∈ divisorsOf N) :
    let q := N / d
    1 ≤ q ∧ q ≤ N ∧ q ∣ N ∧ N / q = d := by
  have hd := divisor_data h
  have hdpos : 0 < d := hd.1
  have hqpos : 0 < N / d := by
    exact (Nat.le_div_iff_mul_le hdpos).2 (by simpa using hd.2.1)
  have hfactor : N / d * d = N := Nat.div_mul_cancel hd.2.2
  have hqdvd : N / d ∣ N := ⟨d, by omega⟩
  have hinv : N / (N / d) = d := by
    apply (Nat.div_eq_iff_eq_mul_left hqpos hqdvd).2
    simpa [Nat.mul_comm] using hfactor.symm
  exact ⟨hqpos, Nat.div_le_self _ _, hqdvd, hinv⟩

private theorem complement_mem_full_range {N d : Nat}
    (h : d ∈ divisorsOf N) :
    N / d ∈ (List.range N).map (· + 1) := by
  have hq := complement_data h
  apply List.mem_map.mpr
  exact ⟨N / d - 1, List.mem_range.mpr (by omega), by omega⟩

private theorem complement_injective_on_divisors {N a b : Nat}
    (ha : a ∈ divisorsOf N) (hb : b ∈ divisorsOf N)
    (h : N / a = N / b) : a = b := by
  have hia := (complement_data ha).2.2.2
  have hib := (complement_data hb).2.2.2
  rw [h] at hia
  omega

private theorem complement_list_nodup (N : Nat) :
    ((divisorsOf N).map (fun d => N / d)).Nodup := by
  change ((divisorsOf N).map (fun d => N / d)).Pairwise (fun a b => a ≠ b)
  rw [List.pairwise_map]
  exact (divisorsOf_nodup N).imp_of_mem fun ha hb hne hEq =>
    hne (complement_injective_on_divisors ha hb hEq)

private theorem sigma_le_harmonic_floor (N : Nat) :
    sigmaOf N ≤ (((List.range N).map (· + 1)).map (fun d => N / d)).sum := by
  have hSubset : (divisorsOf N).map (fun d => N / d) ⊆
      (List.range N).map (· + 1) := by
    intro q hq
    obtain ⟨d, hd, rfl⟩ := List.mem_map.mp hq
    exact complement_mem_full_range hd
  have hWeighted := sum_map_le_of_nodup_subset (fun q => N / q)
    ((divisorsOf N).map (fun d => N / d))
    ((List.range N).map (· + 1))
    (complement_list_nodup N) hSubset
  unfold sigmaOf
  rw [foldl_add_eq_sum]
  simp only [Nat.zero_add]
  have hPointwise :
      ((divisorsOf N).map (fun d => N / d)).map (fun q => N / q) =
        divisorsOf N := by
    rw [List.map_map]
    calc
      (divisorsOf N).map ((fun q => N / q) ∘ fun d => N / d) =
          (divisorsOf N).map (fun d => d) := by
            apply List.map_congr_left
            intro d hd
            exact (complement_data hd).2.2.2
      _ = divisorsOf N := List.map_id' _
  rw [hPointwise] at hWeighted
  exact hWeighted

private theorem sum_append_nat (xs ys : List Nat) :
    (xs ++ ys).sum = xs.sum + ys.sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, Nat.add_assoc]

private theorem sum_map_le_length_mul (w : Nat → Nat) (B : Nat) :
    ∀ (xs : List Nat), (∀ x ∈ xs, w x ≤ B) →
      (xs.map w).sum ≤ xs.length * B := by
  intro xs
  induction xs with
  | nil => simp
  | cons x xs ih =>
      intro h
      have hx : w x ≤ B := h x (List.mem_cons_self x xs)
      have hxs : ∀ y ∈ xs, w y ≤ B := by
        intro y hy
        exact h y (List.mem_cons_of_mem x hy)
      have ht := ih hxs
      simp only [List.map_cons, List.sum_cons, List.length_cons]
      calc
        w x + (xs.map w).sum ≤ B + xs.length * B :=
          Nat.add_le_add hx ht
        _ = (xs.length + 1) * B := by
          rw [Nat.add_mul, Nat.one_mul, Nat.add_comm]

private theorem div_antitone_denominator {N a b : Nat}
    (ha : 0 < a) (hab : a ≤ b) : N / b ≤ N / a := by
  apply (Nat.le_div_iff_mul_le ha).2
  exact Nat.le_trans (Nat.mul_le_mul_left (N / b) hab)
    (Nat.div_mul_le_self N b)

private def dyadicDenoms : Nat → List Nat
  | 0 => []
  | levels + 1 =>
      dyadicDenoms levels ++
        (List.range (2 ^ levels)).map (fun r => 2 ^ levels + r)

private theorem mem_dyadicDenoms_of_pos_lt {levels d : Nat}
    (hdpos : 0 < d) (hdlt : d < 2 ^ levels) :
    d ∈ dyadicDenoms levels := by
  induction levels with
  | zero =>
      simp only [Nat.pow_zero] at hdlt
      omega
  | succ levels ih =>
      simp only [dyadicDenoms, List.mem_append]
      by_cases hlow : d < 2 ^ levels
      · exact Or.inl (ih hlow)
      · apply Or.inr
        apply List.mem_map.mpr
        refine ⟨d - 2 ^ levels, List.mem_range.mpr ?_, ?_⟩
        · simp only [Nat.pow_succ] at hdlt
          omega
        · omega

private theorem dyadic_block_sum_le (N level : Nat) :
    ((((List.range (2 ^ level)).map (fun r => 2 ^ level + r)).map
      (fun d => N / d)).sum) ≤ N := by
  let block := (List.range (2 ^ level)).map (fun r => 2 ^ level + r)
  have hpoint : ∀ d ∈ block, N / d ≤ N / (2 ^ level) := by
    intro d hd
    have hlower : 2 ^ level ≤ d := by
      obtain ⟨r, _hr, rfl⟩ := List.mem_map.mp hd
      omega
    exact div_antitone_denominator (Nat.two_pow_pos level) hlower
  have hsum := sum_map_le_length_mul (fun d => N / d)
    (N / (2 ^ level)) block hpoint
  have hlength : block.length = 2 ^ level := by
    simp [block]
  rw [hlength] at hsum
  exact Nat.le_trans hsum (Nat.mul_div_le N (2 ^ level))

private theorem dyadic_sum_le (N : Nat) :
    ∀ levels : Nat,
      ((dyadicDenoms levels).map (fun d => N / d)).sum ≤ levels * N := by
  intro levels
  induction levels with
  | zero => simp [dyadicDenoms]
  | succ levels ih =>
      rw [dyadicDenoms, List.map_append, sum_append_nat]
      have hblock := dyadic_block_sum_le N levels
      calc
        ((dyadicDenoms levels).map (fun d => N / d)).sum +
            ((((List.range (2 ^ levels)).map
              (fun r => 2 ^ levels + r)).map (fun d => N / d)).sum) ≤
            levels * N + N := Nat.add_le_add ih hblock
        _ = (levels + 1) * N := by
          rw [Nat.add_mul, Nat.one_mul]

private theorem full_denoms_nodup (N : Nat) :
    ((List.range N).map (· + 1)).Nodup := by
  change ((List.range N).map (· + 1)).Pairwise (fun a b => a ≠ b)
  rw [List.pairwise_map]
  exact (List.nodup_range N).imp fun hne hEq => hne (by omega)

private theorem harmonic_floor_le_log2 (N : Nat) :
    (((List.range N).map (· + 1)).map (fun d => N / d)).sum ≤
      N * (1 + Nat.log2 N) := by
  let levels := Nat.log2 N + 1
  have hSubset : (List.range N).map (· + 1) ⊆ dyadicDenoms levels := by
    intro d hd
    obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hd
    have hrlt : r < N := List.mem_range.mp hr
    apply mem_dyadicDenoms_of_pos_lt
    · omega
    · exact Nat.lt_of_le_of_lt (by omega) Nat.lt_log2_self
  have hEmbed := sum_map_le_of_nodup_subset (fun d => N / d)
    ((List.range N).map (· + 1)) (dyadicDenoms levels)
    (full_denoms_nodup N) hSubset
  have hDyadic := dyadic_sum_le N levels
  calc
    (((List.range N).map (· + 1)).map (fun d => N / d)).sum ≤
        ((dyadicDenoms levels).map (fun d => N / d)).sum := hEmbed
    _ ≤ levels * N := hDyadic
    _ = N * (1 + Nat.log2 N) := by
      simp [levels, Nat.mul_comm, Nat.add_comm]

/-- Direct dyadic census bound.  In fact the proof also covers `N = 0`; the
printed `N ≥ 1` hypothesis is retained to match Claim 2's source wrapper. -/
theorem sigmaOf_le_mul_one_add_log2 :
    ∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N) := by
  intro N _hN
  exact Nat.le_trans (sigma_le_harmonic_floor N)
    (harmonic_floor_le_log2 N)

/-- Compatibility alias retaining the earlier asymptotic-facing name. -/
theorem sigmaOf_subexponential :
    ∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N) :=
  sigmaOf_le_mul_one_add_log2

/-- Compatibility alias for the historical statement-target declaration.
Despite its retained suffix, this declaration is now proved. -/
theorem sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED :
    ∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N) :=
  sigmaOf_le_mul_one_add_log2

end FirstMatchAtlas.PlantedDivisorCensus
