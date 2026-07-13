/-!
# The positive-rooted split decomposition (statement stub)

Maps to **hard input 2**: the DECOMPOSITION step of avdeevvadim's #716
charge-preserving semantic-or-signed dichotomy (Sec 6), completed with the
heavy/light + layer-cake split of #729 on the admissible heavy fibers of #717.

Note:     `experimental/notes/thresholds/charge_preserving_split_decomposition.md`.
Verifier: `experimental/scripts/verify_charge_preserving_split_decomposition.py`
          (57/57, tamper 1/1).

The central analytic result of the note is **Theorem A**: for a positive-rooted
packet with global `P_A`-norming dual `g` (`||g||_{q'}=1`) and pointwise weights
`omega_s = Re conj((P_A g)(s)) > 0`, the natural charge `c_i = sum_{S in U_i} omega(S)`
of ANY piece satisfies the fourth #716 charge condition `||P_A b_{U_i}||_q >= c_i`
FOR FREE, with the common band `B_i = A`, because `g` is a feasible test function
in the duality representation of the `q`-norm:
    `c_i = Re<P_A b_{U_i}, g> <= ||P_A b_{U_i}||_q ||g||_{q'} = ||P_A b_{U_i}||_q`.
Together with (C1)-(C3) this makes the split a four-condition charge-preserving
decomposition; the pruned layers pay #716's signed clause (#729 Thm I) and the
heavy point masses are semantic candidates (#717 Thm 5.1).

HONEST NONCLAIM. Theorem A and all norm inequalities live over `R` with DFT band
projections and Holder/duality; they are PROVED in the note + Python verifier
(exact `Fraction` over `F_2^k`, exact-Parseval over `Z_C`), NOT in Lean. This
module is the DECIDABLE arithmetic shadow, stdlib-only `native_decide`, of the
parts that are integer/combinatorial:

1. the CARDINALITY OBSTRUCTION (the genuine residual, NOT the fourth condition):
   the split has `#heavy + Wmax_light` pieces; on a heavy fiber + flat tail of
   `K` fibers of size `D` this is `min(K,D)+1`, so the family `(K,D)=(2^m,2^m)`
   forces `minPieces = 2^m + 1 = L = e^{Omega(N)}` -- defeating #716's
   "at most e^{o(N)} packets".  Contrasted with the CONCENTRATED superincreasing
   family, whose split stays at `1 + (a-2)` pieces;
2. the superincreasing exact scalars `W = C(B,B/2)` (planted twin-pair template),
   `L = (3^B+1)/2`, Johnson saturation exponent `a-2`;
3. the layer-cake integer identity `sum_{j>=1} #{s : b s >= j} = sum_s b s`
   (an unpruned mask splits into `Wmax` pruned layers; #729's identity, reused).

No `sorry`. No mathlib. No Batteries.
-/

namespace ChargePreservingSplitDecomposition

/-! ## 0. Binomial (stdlib-only Pascal; core `Nat` lacks `Nat.choose`). -/

def binom : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

/-- Heavy-fiber size `W = C(B, B/2)` = the number of `B/2`-subsets of the `B`
    twin pairs = the planted-template count of the superincreasing heavy fiber. -/
theorem template_count_B4 : binom 4 2 = 6  := by native_decide
theorem template_count_B6 : binom 6 3 = 20 := by native_decide
theorem template_count_B8 : binom 8 4 = 70 := by native_decide

/-! ## 1. Superincreasing exact scalars (#717 Sec 7 / #728). -/

/-- Image size `L = (3^B + 1)/2` (exact `Nat` division). -/
theorem superL_B4 : (3 ^ 4 + 1) / 2 = 41   := by native_decide
theorem superL_B6 : (3 ^ 6 + 1) / 2 = 365  := by native_decide
theorem superL_B8 : (3 ^ 8 + 1) / 2 = 3281 := by native_decide

/-- Johnson saturation exponent: the heavy fiber saturates `|S ∩ S'| = a - 2`
    (`a = B`). -/
def johnsonSat (B : Nat) : Nat := B - 2
theorem johnson_B4 : johnsonSat 4 = 2 := by native_decide
theorem johnson_B6 : johnsonSat 6 = 4 := by native_decide
theorem johnson_B8 : johnsonSat 8 = 6 := by native_decide

/-! ## 2. Piece count of the heavy(point-mass)/light(layer-cake) split.

`l` is the multiset of positive-fiber sizes.  At threshold `th` the split makes
`#{v >= th}` heavy point masses and `max{v : v < th}` pruned layers.  `minPieces`
minimizes over the candidate thresholds (every fiber size, and `max+1`). -/

def maxSize (l : List Nat) : Nat := l.foldl Nat.max 0

def countGE (l : List Nat) (th : Nat) : Nat :=
  (l.filter (fun v => decide (th ≤ v))).length

def maxLT (l : List Nat) (th : Nat) : Nat :=
  (l.filter (fun v => decide (v < th))).foldl Nat.max 0

def pieceCountAt (l : List Nat) (th : Nat) : Nat := countGE l th + maxLT l th

/-- Minimum piece count over all candidate thresholds. -/
def minPieces (l : List Nat) : Nat :=
  ((maxSize l + 1) :: l).foldl (fun acc th => Nat.min acc (pieceCountAt l th))
    (l.length + maxSize l + 1)

/-! ### 2.1 CARDINALITY OBSTRUCTION (COUNTEREXAMPLE to an e^{o(N)}-piece split).

Heavy fiber `2^{2m}` plus a flat tail of `2^m` fibers of size `2^m`.  Then
`L = 2^m + 1`, `M = 2^{2m+1}`, and `minPieces = 2^m + 1 = L`: no threshold makes
both the heavy-point-mass count and the layer count subexponential. -/

theorem obstruction_m4 : minPieces (256  :: List.replicate 16  16)  = 17  := by native_decide
theorem obstruction_m5 : minPieces (1024 :: List.replicate 32  32)  = 33  := by native_decide
theorem obstruction_m6 : minPieces (4096 :: List.replicate 64  64)  = 65  := by native_decide

/-- `minPieces = 1 + 2^m` = the image size `L` of the witness (spread ⇒ e^{Ω(N)}). -/
theorem obstruction_eq_L_m4 : minPieces (256  :: List.replicate 16 16) = 1 + 2 ^ 4 := by native_decide
theorem obstruction_eq_L_m6 : minPieces (4096 :: List.replicate 64 64) = 1 + 2 ^ 6 := by native_decide

/-- Growth: the piece count is at least `2^m` (exponential when `M = e^{Θ(N)}`). -/
theorem obstruction_grows_m6 : 2 ^ 6 ≤ minPieces (4096 :: List.replicate 64 64) := by native_decide

/-! ### 2.2 CONCENTRATED contrast: the superincreasing split stays small.

Heavy fiber `W` (extracted as ONE semantic piece) over a tail whose maximum is
`a-2`-scale; the split has `1 + (a-2)` pieces regardless of how many tail fibers
there are.  Faithful compact skeletons of the verifier's `B4 -> 3`, `B6 -> 7`. -/

theorem concentrated_B4 : minPieces (6  :: List.replicate 12 2) = 3 := by native_decide
theorem concentrated_B6 : minPieces (20 :: List.replicate 12 6) = 7 := by native_decide

/-! ## 3. Layer-cake integer identity (#729, reused).

`sum_{j = 1}^{Wmax} #{s : b s >= j} = sum_s b s`: an unpruned integer mask of
max multiplicity `Wmax` splits into `Wmax` pruned (0/1) layers with total mass
preserved. -/

def layerSize (b : List Nat) (j : Nat) : Nat :=
  (b.filter (fun v => decide (j ≤ v))).length

def layerCakeSum (b : List Nat) : Nat :=
  ((List.range (maxSize b)).map (fun j => layerSize b (j + 1))).foldl (· + ·) 0

def total (b : List Nat) : Nat := b.foldl (· + ·) 0

theorem layercake_B4skel : layerCakeSum [6, 2, 2, 2, 1] = total [6, 2, 2, 2, 1] := by native_decide
theorem layercake_B6skel : layerCakeSum [20, 6, 6, 3, 2, 1] = total [20, 6, 6, 3, 2, 1] := by native_decide

end ChargePreservingSplitDecomposition
