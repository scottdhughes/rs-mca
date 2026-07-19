/-!
# Rank-nine fixed-basis exact compiler

This standalone Lean 4.14 module formalizes the exact finite compiler in
Sections 1, 3, and 4 of
`experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at source commit `3404d21` (Scott Hughes).

The source binomial coefficients are represented by the standard descending-
factorial quotient. The sharp union threshold is quantified over the carrier
size. Basis multiplicities are represented by their finite list; `total` and
`excess20` exactly encode the sums in Eqs. (1.6) and (4.4). The two compiler
theorems retain the pointwise-cap/cardinality or aggregate-excess/cardinality
hypotheses and prove the source's exact integer conclusions.

No proof placeholder, custom postulate, Mathlib import, field model, selector
construction, five-pencil realization, or ledger payment is used.
-/

namespace Rank9FixedBasisExactCompiler

/-- Standard natural factorial. -/
def factorial : Nat → Nat
  | 0 => 1
  | k + 1 => (k + 1) * factorial k

/-- Standard descending factorial `m * (m-1) * ... * (m-k+1)`. -/
def descFactorial (m : Nat) : Nat → Nat
  | 0 => 1
  | k + 1 => (m - k) * descFactorial m k

/-- The source binomial coefficient, by the standard identity
`C(m,k) = m.descFactorial(k) / k!`. -/
def binom (m k : Nat) : Nat := descFactorial m k / factorial k

abbrev n : Nat := 2097152
abbrev j : Nat := 981104
abbrev lowBase : Nat := 67480
abbrev target : Nat := 17907572507584
abbrev m20 : Nat := (21 * j) / 20 + 1
abbrev c0 : Nat := binom lowBase 8
abbrev eMax : Nat := (target + 1) * c0 - 20 * binom n 8 - 1

/-- Sum of the finite list of basis multiplicities. -/
def total : List Nat → Nat
  | [] => 0
  | m :: ms => m + total ms

/-- Source Eq. (4.4): aggregate excess above the pointwise cap 20. -/
def excess20 : List Nat → Nat
  | [] => 0
  | m :: ms => (m - 20) + excess20 ms

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (1.4): the exact order-eight lower incidence. -/
theorem c0_value :
    c0 = 10658592438443717273371372062592575 := by
  decide

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (3.1): for every carrier size, the printed strict inequality
excluding 21 slopes is equivalent to the exact sharp integer threshold. -/
theorem large_union_threshold_iff (MB : Nat) :
    21 * (MB - j) > MB ↔ m20 ≤ MB := by
  change 21 * (MB - 981104) > MB ↔ 1030160 ≤ MB
  omega

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (3.2): the named low-union interval is exactly the displayed
closed integer interval. -/
theorem low_union_interval_iff (MB : Nat) :
    (j < MB ∧ MB < m20) ↔ (981105 ≤ MB ∧ MB ≤ 1030159) := by
  change (981104 < MB ∧ MB < 1030160) ↔
    (981105 ≤ MB ∧ MB ≤ 1030159)
  omega

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (4.1): the exact cap-20 quotient. -/
theorem cap20_tail_value :
    (20 * binom n 8) / c0 = 17411776716968 := by
  decide

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (4.2): the exact margin below the target. -/
theorem cap20_margin_value :
    target - (20 * binom n 8) / c0 = 495795790616 := by
  decide

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (4.3): the cap-21 quotient and its exact excess over the
target. -/
theorem cap21_tail_and_excess :
    (21 * binom n 8) / c0 = 18282365552816 ∧
    (21 * binom n 8) / c0 - target = 374793045232 := by
  decide

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (4.5): the exact largest sufficient aggregate excess
allowance. -/
theorem aggregate_excess_max_value :
    eMax = 5284485264881189380664190436821715347228277374 := by
  decide

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (4.5) and its following sharpness sentence: `eMax` is the
last aggregate excess whose quotient is the target; adding one raises the
quotient by exactly one. -/
theorem aggregate_excess_sharp :
    (20 * binom n 8 + eMax) / c0 = target ∧
    (20 * binom n 8 + (eMax + 1)) / c0 = target + 1 := by
  decide

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eq. (4.1): pointwise cap 20 gives the exact upper sum. -/
theorem total_le_twenty_mul_length
    (counts : List Nat)
    (hCap : ∀ m ∈ counts, m ≤ 20) :
    total counts ≤ 20 * counts.length := by
  induction counts with
  | nil => decide
  | cons m ms ih =>
      have hm : m ≤ 20 := hCap m (by simp)
      have hms : ∀ x ∈ ms, x ≤ 20 := by
        intro x hx
        exact hCap x (by simp [hx])
      have htail := ih hms
      simp only [total, List.length_cons]
      omega

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eqs. (4.4)--(4.5): every finite multiplicity list satisfies
the exact baseline-plus-excess upper sum. -/
theorem total_le_baseline_add_excess (counts : List Nat) :
    total counts ≤ 20 * counts.length + excess20 counts := by
  induction counts with
  | nil => decide
  | cons m ms ih =>
      simp only [total, excess20, List.length_cons]
      omega

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eqs. (1.6) and (4.1): if the finite basis-multiplicity family has
at most `C(n,8)` entries and every multiplicity is at most 20, the printed
double count gives the exact sharp cap-20 conclusion. -/
theorem uniform_cap20_compiler
    (H : Nat)
    (counts : List Nat)
    (hLower : H * c0 ≤ total counts)
    (hCard : counts.length ≤ binom n 8)
    (hCap : ∀ m ∈ counts, m ≤ 20) :
    H ≤ 17411776716968 := by
  have hPointwise := total_le_twenty_mul_length counts hCap
  have hCardScaled : 20 * counts.length ≤ 20 * binom n 8 :=
    Nat.mul_le_mul_left 20 hCard
  have hUpper : total counts ≤ 20 * binom n 8 :=
    Nat.le_trans hPointwise hCardScaled
  have hLower' :
      H * 10658592438443717273371372062592575 ≤ total counts := by
    simpa [c0] using hLower
  have hUpper' :
      total counts ≤
        185585031655346888507331569717051216521723904000 := by
    calc
      total counts ≤ 20 * binom n 8 := hUpper
      _ = 185585031655346888507331569717051216521723904000 := by
        decide
  omega

/-- Source: `experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21`, Eqs. (1.6), (4.4), and (4.5): the exact aggregate excess
hypothesis and basis-family cardinality force the target bound. -/
theorem aggregate_excess_compiler
    (H : Nat)
    (counts : List Nat)
    (hLower : H * c0 ≤ total counts)
    (hCard : counts.length ≤ binom n 8)
    (hExcess : excess20 counts ≤ eMax) :
    H ≤ target := by
  have hBaseline := total_le_baseline_add_excess counts
  have hCardScaled : 20 * counts.length ≤ 20 * binom n 8 :=
    Nat.mul_le_mul_left 20 hCard
  have hUpper : total counts ≤ 20 * binom n 8 + eMax := by
    exact Nat.le_trans hBaseline (Nat.add_le_add hCardScaled hExcess)
  have hLower' :
      H * 10658592438443717273371372062592575 ≤ total counts := by
    simpa [c0] using hLower
  have hUpper' :
      total counts ≤
        190869516920228077887995760153872931868952181374 := by
    calc
      total counts ≤ 20 * binom n 8 + eMax := hUpper
      _ = 190869516920228077887995760153872931868952181374 := by
        decide
  change H ≤ 17907572507584
  omega

#print axioms c0_value
#print axioms large_union_threshold_iff
#print axioms low_union_interval_iff
#print axioms cap20_tail_value
#print axioms cap20_margin_value
#print axioms cap21_tail_and_excess
#print axioms aggregate_excess_max_value
#print axioms aggregate_excess_sharp
#print axioms total_le_twenty_mul_length
#print axioms total_le_baseline_add_excess
#print axioms uniform_cap20_compiler
#print axioms aggregate_excess_compiler

end Rank9FixedBasisExactCompiler
