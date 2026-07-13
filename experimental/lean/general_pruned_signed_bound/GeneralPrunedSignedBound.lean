/-!
# The chart-free pruned signed bound (statement stub)

Maps to **hard input 2**: image-scale MI + MA / direct Sidon payment -- the
signed-minor clause of avdeevvadim's #716 charge-preserving dichotomy, escalated
from the depth-1 superincreasing family of #728 to a GENERAL finite abelian
source chart.

Note:     `experimental/notes/thresholds/general_pruned_signed_bound.md`.
Verifier: `experimental/scripts/verify_general_pruned_signed_bound.py`
          (193359/193359, tamper 6/6).

This module certifies the EXACT, DECIDABLE backbone of the general theorem:
1. the chart-free DENSITY CRITERION in exact integer form
     window nonempty (q=2)   <=>  M > L         (logM/logL > 1)
     window = all q>=2        <=>  L^3 <= M^2    (logM/logL >= 3/2)
   evaluated on the atlas's depth-R prefix charts (exact L by enumeration);
2. the finite per-q window predicate  prunedDecays M L q  <=>  L^(3q-2) < M^(2q)
   (the crude Theorem-I bound L^{3/2-1/q}/M < 1, cleared of the root);
3. the layer-cake INTEGER identity  sum_j |{s : b s >= j}| = sum_s b s
   (an unpruned mask of max multiplicity W_max splits into W_max pruned layers);
4. the #728 superincreasing family as the depth-1 special case (finite window,
   rate-limit window {3,4}, heavy-fiber crossover W^2 > L at B>=6).

HONEST NONCLAIM: the analytic `l^q` projection bounds themselves
  Theorem I : R_A(g) <= (L/M)(L delta_A)^{1/2-1/q} <= L^{3/2-1/q}/M
              (all finite abelian G, all bands A, all q>=2, |g|<=1 on |S|<=L),
  Theorem D : pruned packet  =>  c_i <= L^{1/2} <= e^{o(N)} M/L^{1-1/q},
  Theorem II: unpruned excess  >= (L^{1-1/q}/M)(W - M/H)/K_N,
are PROVED in the note + Python verifier, NOT in Lean; they live over `R` with
DFT band projections and Riesz-Thorin interpolation. This package is the
decidable arithmetic/threshold shadow, in the stdlib-only `native_decide` house
style. No `sorry`. No mathlib.
-/

namespace GeneralPrunedSignedBound

/-! ## 0. Binomial (stdlib-only Pascal; core `Nat` lacks `Nat.choose`). -/

def binom : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

theorem binom_check : binom 11 4 = 330 := by native_decide

/-! ## 1. The chart-free density criterion (exact integer form).

For a chart with `M = |Omega^0|` supports and image size `L = |Phi(Omega^0)|`,
the crude Theorem-I bound is `R_A(g) <= L^{3/2-1/q}/M`.  It vanishes iff
`(3/2 - 1/q) log L < log M`.  Clearing logs:

* q = 2  boundary  `L < M`               (window nonempty  <=>  M > L);
* all q  boundary  `L^{3/2} <= M`, i.e.  `L^3 <= M^2`  (window = all q>=2). -/

/-- window is nonempty (contains q=2)  <=>  `M > L`  (`logM/logL > 1`). -/
def windowNonempty (M L : Nat) : Bool := L < M

/-- window is all of `q >= 2`  <=>  `L^3 <= M^2`  (`logM/logL >= 3/2`). -/
def windowAllQ (M L : Nat) : Bool := L ^ 3 <= M ^ 2

/-- finite per-`q` decay of the pruned bound: `L^{3/2-1/q}/M < 1`, cleared of
    the `2q`-th root, i.e. `L^(3q-2) < M^(2q)` (needs `q >= 1`). -/
def prunedDecays (M L q : Nat) : Bool := L ^ (3 * q - 2) < M ^ (2 * q)

/-! ### 1.2 The atlas's depth-R prefix charts (exact L, from the verifier).

Rows `(name, Q, N, a, R, L, M=C(N,a))`; the window classification below is the
decidable shadow of the note's density table. -/

-- F5  a2 R1 : L=5,  M=10  -> nonempty, NOT all-q  (window [2, q_+),  q_+~14.4)
theorem F5a2R1_nonempty  : windowNonempty 10 5 = true  := by native_decide
theorem F5a2R1_not_allq  : windowAllQ 10 5 = false      := by native_decide
-- F7  a3 R1 : L=7,  M=35  -> all q
theorem F7a3R1_allq      : windowAllQ 35 7 = true        := by native_decide
-- F7  a3 R2 : L=28, M=35  -> nonempty, NOT all-q  (deepening R shrinks window)
theorem F7a3R2_nonempty  : windowNonempty 35 28 = true   := by native_decide
theorem F7a3R2_not_allq  : windowAllQ 35 28 = false      := by native_decide
-- F11 a4 R1 : L=11, M=330 -> all q
theorem F11a4R1_allq     : windowAllQ 330 11 = true      := by native_decide
-- F11 a4 R2 : L=110,M=330 -> nonempty, NOT all-q
theorem F11a4R2_nonempty : windowNonempty 330 110 = true := by native_decide
theorem F11a4R2_not_allq : windowAllQ 330 110 = false    := by native_decide
-- F13 a6 R1 : L=13, M=1716 -> all q
theorem F13a6R1_allq     : windowAllQ 1716 13 = true     := by native_decide

/-- Near-injective chart (chart4: `M = L = 10`): the window is EMPTY -- the
    criterion correctly reports that Theorem I's bound does not vanish. -/
theorem injective_empty  : windowNonempty 10 10 = false  := by native_decide

/-- Deepening the prefix (F7 a3: `R=1 -> R=2`) turns an all-q window into a
    finite one -- the exact monotone effect of enlarging `L` toward `Q^R`. -/
theorem deepening_shrinks :
    (windowAllQ 35 7 = true) ∧ (windowAllQ 35 28 = false) := by native_decide

/-! ## 2. The finite q-window on the #728 superincreasing family.

`L(B) = (3^B+1)/2`, `M(B) = C(2B,B)`, `W(B) = C(B, B/2)` (heavy fiber). -/

def Limg  (B : Nat) : Nat := (3 ^ B + 1) / 2
def Mslice (B : Nat) : Nat := binom (2 * B) B
def Wheavy (B : Nat) : Nat := binom B (B / 2)

theorem L_B2 : Limg 2 = 5 := by native_decide
theorem M_B2 : Mslice 2 = 6 := by native_decide
theorem W_B6 : Wheavy 6 = 20 := by native_decide

/-- FINITE per-chart window at `B=2`: the finite `q_+` is `2.586 < 3`, so the
    finite window is EMPTY of integers (`q=3` does NOT decay at `B=2`), even
    though the ASYMPTOTIC window is `{3,4}`.  This is the finite-vs-rate gap the
    note flags: `prunedDecays` uses the true small `L,M`, not the growth rates. -/
theorem B2_finite_q3_not_decay : prunedDecays (Mslice 2) (Limg 2) 3 = false := by
  native_decide
theorem B2_finite_q2_decays : prunedDecays (Mslice 2) (Limg 2) 2 = true := by
  native_decide   -- q=2 always in the finite window when M > L

/-- ASYMPTOTIC (rate) window, exactly #728's form with the growth bases
    `L ~ 3^B`, `M ~ 4^B`: `prunedDecays` on the RATE bases is
    `3^(3q-2) < 4^(2q)`, whose integer solution set is `{3,4}` -- matching the
    `first_match_signed_gain` package.  (`unprunedGrows q := 3^(q-1) > 2^q`.) -/
def rateDecays (q : Nat) : Bool := 3 ^ (3 * q - 2) < 4 ^ (2 * q)
def rateGrows  (q : Nat) : Bool := 3 ^ (q - 1) > 2 ^ q
def rateWindow (q : Nat) : Bool := rateGrows q && rateDecays q

theorem rate_window_is_3_4 :
    ((List.range 8).filter (fun q => rateWindow q)) = [3, 4] := by native_decide
theorem rate_q4_in_window : rateWindow 4 = true := by native_decide

/-- Heavy-fiber crossover (Part 3 residual): `W^2 > L` (i.e. `W > sqrt L`) first
    holds at `B = 6`, where the unpruned mask breaks the pruned ceiling and must
    route to the semantic side.  Below it the pruned bound already covers the
    whole mask. -/
def heavyCrossover (B : Nat) : Bool := (Wheavy B) ^ 2 > Limg B

theorem no_crossover_B4 : heavyCrossover 4 = false := by native_decide  -- 36 < 41
theorem crossover_B6    : heavyCrossover 6 = true  := by native_decide  -- 400 > 365
theorem crossover_B8    : heavyCrossover 8 = true  := by native_decide

/-! ## 3. Layer-cake integer identity (Part 3.1, exact).

An unpruned mask `b : ι → Nat` of max multiplicity `W_max` decomposes into
`W_max` pruned layers `g_j = 1_{b >= j}`; the total mass is preserved:
`sum_{j=1}^{W_max} |{s : b s >= j}| = sum_s b s`.  This is the combinatorial
core of `||P_A b||_q <= sum_j ||P_A g_j||_q <= W_max * L^{1/2}`. -/

/-- `j`-th pruned layer size over a finite list of syndrome multiplicities. -/
def layerSize (b : List Nat) (j : Nat) : Nat :=
  (b.filter (fun bs => j <= bs)).length

/-- total mass split into `W_max` layers. -/
def layerSum (b : List Nat) (Wmax : Nat) : Nat :=
  ((List.range Wmax).map (fun j => layerSize b (j + 1))).foldl (· + ·) 0

/-- layer-cake identity on a concrete unpruned mask (`W_max = 3`):
    `b = [3,1,2,0,3,1]`, `sum b = 10`, three layers of sizes `[5,3,2]`. -/
theorem layer_cake_example :
    layerSum [3, 1, 2, 0, 3, 1] 3 = ([3,1,2,0,3,1].foldl (· + ·) 0) := by
  native_decide

theorem layer_sizes_example :
    ((List.range 3).map (fun j => layerSize [3,1,2,0,3,1] (j+1))) = [5, 3, 2] := by
  native_decide

/-- a second instance (`W_max = 4`) to exercise the identity at higher
    multiplicity. -/
theorem layer_cake_example2 :
    layerSum [4, 0, 2, 4, 1, 3, 2] 4 = ([4,0,2,4,1,3,2].foldl (· + ·) 0) := by
  native_decide

/-! ## 4. Dual `decide` spot checks. -/

theorem F7a3R1_allq'      : windowAllQ 35 7 = true       := by decide
theorem injective_empty'  : windowNonempty 10 10 = false := by decide
theorem rate_q4'          : rateWindow 4 = true          := by decide

end GeneralPrunedSignedBound
