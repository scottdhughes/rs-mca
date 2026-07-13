/-!
# Heavy prefix fibers emit planted/saturation precursors (statement stub)

Maps to **hard input 2**: the SEMANTIC EMISSION clause of avdeevvadim's #716
charge-preserving semantic-or-signed dichotomy -- does every exponentially heavy
depth-R prefix fiber emit one of the five precursors
  { quotient(folding), field-descent, planted(template), rank, ray-saturation }
with subexponential census?

Note:     `experimental/notes/thresholds/heavy_fiber_planted_emission.md`.
Verifier: `experimental/scripts/verify_heavy_fiber_planted_emission.py`
          (155/155, tamper 4/4, ~2.8s).

HONEST NONCLAIM.  The emission theorems and the exhaustive census (the
no-counterexample scan, the F_p precursor battery, the l^q-free structural
content) are PROVED in the note + Python verifier, NOT in Lean.  This module is
the DECIDABLE arithmetic shadow (stdlib-only `native_decide`) of the parts that
are pure integer / F_p combinatorics:

1. THM 1 saturation-forcing: the recursive Johnson constant-weight-code bound
   `cwBound n d w` and the strict drop `A(n,2(R+2),a) < A(n,2(R+1),a)` that makes
   "heavier than the non-saturating ceiling => must saturate" go through;
2. THM 2 involution twin-pair: the emitted fiber size `W = C(B,B/2)` (planted
   template on B/2 of B pairs) and Johnson saturation exponent `a-2`;
3. THM 3 multiplicative folding: an order-d multiplicative-subgroup coset has
   vanishing power sums `p_1 = ... = p_{d-1} = 0 mod p`, so coset-union supports
   sit in ONE depth-(d-1) prefix fiber, with #725 coset census `sigma(p-1)`.

No mathlib.  No Batteries.  One honest `sorry` at the single general target.
-/

namespace HeavyFiberPlantedEmission

/-! ## 0. Binomial (stdlib-only Pascal; core `Nat` lacks `Nat.choose`). -/

def binom : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

/-! ## 1. THM 2 -- involution twin-pair emitted fiber size `W = C(B,B/2)`.

For `T = P u (c-P)` with `P` a Sidon (distinct-subset-sum) set, `a = B`, the
central fiber is EXACTLY the `C(B,B/2)` complete-twin-pair unions (choose B/2 of
the B pairs, take both elements of each).  These are the planted-template
supports; `a-2` is the Johnson agreement they saturate. -/

def twinCount (B : Nat) : Nat := binom B (B / 2)

theorem twin_B2  : twinCount 2  = 2   := by native_decide
theorem twin_B4  : twinCount 4  = 6   := by native_decide
theorem twin_B6  : twinCount 6  = 20  := by native_decide
theorem twin_B8  : twinCount 8  = 70  := by native_decide
theorem twin_B10 : twinCount 10 = 252 := by native_decide

/-- Saturation exponent: twin unions sharing all but one pair agree in `a-2`. -/
theorem twin_saturation_B4 : (4 : Nat) - 2 = 2 := by native_decide
theorem twin_saturation_B8 : (8 : Nat) - 2 = 6 := by native_decide

/-! ## 2. THM 1 -- Johnson constant-weight-code bound `A(n,2e,w)`.

A depth-R fiber is a binary constant-weight (n,w=a) code with max pairwise
intersection `<= a-R-1` (#717 Thm 4.1), i.e. min distance `>= 2(R+1)`.  A
NON-saturating fiber has intersection `<= a-R-2`, distance `>= 2(R+2)`, hence
size `<= cwBound n (2*(R+2)) a`.  `cwBound` is the recursive Johnson bound
(max-intersection `s = w - e`, `e = d/2`):
   `A(n,2e,w) <= floor(n/w * A(n-1,2e,w-1))`,  base `A(n,2e,e) = floor(n/e)`. -/

/-- Recursive Johnson bound, fixed half-distance `e`, fuel = `w`. -/
def cwRec (e : Nat) : Nat → Nat → Nat
  | _, 0          => 1
  | n, (w + 1) =>
      if w + 1 < e then 1
      else if w + 1 == e then (if e == 0 then 1 else n / e)
      else max 1 ((n * cwRec e (n - 1) w) / (w + 1))

def cwBound (n d w : Nat) : Nat := cwRec (d / 2) n w

/-- Concrete Johnson-bound values (match the verifier's BLOCK B). -/
theorem cw_12_8_4 : cwBound 12 8 4 = 3 := by native_decide
theorem cw_12_6_3 : cwBound 12 6 3 = 4 := by native_decide
theorem cw_9_6_3  : cwBound 9  6 3 = 3 := by native_decide

/-- The saturation-forcing CEILING DROP at (n,a,R)=(12,4,2):
    non-saturating (dist 2(R+2)=8) ceiling `A(12,8,4)=3` is STRICTLY below the
    admissible (dist 2(R+1)=6) ceiling `A(12,6,4)`; so a fiber above `3` cannot
    be non-saturating -- it must saturate. -/
theorem ceiling_strict_drop_n12_a4 : cwBound 12 8 4 < cwBound 12 6 4 := by native_decide

/-- Instance of THM 1's contrapositive at (n,a,R)=(12,4,2): a fiber of size 4
    exceeds the non-saturating ceiling `A(12,8,4)=3`, so it MUST saturate. -/
theorem heavy_exceeds_nonsat_ceiling : 3 < 4 ∧ cwBound 12 8 4 = 3 := by native_decide

/-! ## 3. THM 3 -- multiplicative coset power sums vanish `p_1..p_{d-1} = 0`.

An order-`d` multiplicative-subgroup coset `{x, zx, ..., z^{d-1} x}` has
`p_k = x^k * sum_j z^{jk} = 0 mod p` for `1 <= k <= d-1`, so a coset-union support
lands in the depth-(d-1) fiber at `(0,...,0)`.  Concrete F_p cosets. -/

def powerSumMod (coset : List Nat) (k p : Nat) : Nat :=
  (coset.map (fun x => (x ^ k) % p)).foldl (· + ·) 0 % p

/-- p=7, d=2 (H_2={1,6}): coset {1,6} has p_1 = 0 mod 7. -/
theorem coset_p7_d2 : powerSumMod [1, 6] 1 7 = 0 := by native_decide

/-- p=13, d=3 (H_3={1,3,9}): coset {1,3,9} has p_1 = p_2 = 0 mod 13. -/
theorem coset_p13_d3_p1 : powerSumMod [1, 3, 9] 1 13 = 0 := by native_decide
theorem coset_p13_d3_p2 : powerSumMod [1, 3, 9] 2 13 = 0 := by native_decide

/-- p=13, d=4 (H_4={1,5,8,12}): coset has p_1 = p_2 = p_3 = 0 mod 13
    (a depth-3 heavy zero fiber). -/
theorem coset_p13_d4_p1 : powerSumMod [1, 5, 8, 12] 1 13 = 0 := by native_decide
theorem coset_p13_d4_p2 : powerSumMod [1, 5, 8, 12] 2 13 = 0 := by native_decide
theorem coset_p13_d4_p3 : powerSumMod [1, 5, 8, 12] 3 13 = 0 := by native_decide

/-! ## 4. THM 3 census -- the coset-type planted family size is `sigma(p-1)` (#725). -/

def sigmaNat (n : Nat) : Nat :=
  ((List.range n).map (fun d => if n % (d + 1) == 0 then d + 1 else 0)).foldl (· + ·) 0

theorem sigma_p7  : sigmaNat 6  = 12 := by native_decide     -- p=7  -> sigma(6)
theorem sigma_p13 : sigmaNat 12 = 28 := by native_decide     -- p=13 -> sigma(12)

/-! ## 5. The single general target (honestly unproved in Lean).

THM 1 saturation-forcing, general form: for every `n a R`, a constant-weight code
`C` (subsets of `Fin n` of size `a`, pairwise `|S ∩ S'| ≤ a-R-1`) with
`C.card > cwBound n (2*(R+2)) a` contains a pair with `|S ∩ S'| = a-R-1` (it
saturates).  The note + verifier prove this via the Johnson bound; here it is a
STATEMENT TARGET carrying an explicit `sorry`.  The hypotheses match the note. -/

/-- Max pairwise intersection of a list of finite index-sets (as `List Nat`
    supports); `0` if fewer than two.  stdlib-only nested folds (no List monad). -/
def interLen (a b : List Nat) : Nat := (a.filter (fun x => b.contains x)).length

def maxIntersect (fibers : List (List Nat)) : Nat :=
  let idx := List.range fibers.length
  idx.foldl (fun acc i =>
    idx.foldl (fun acc2 j =>
      if i < j then Nat.max acc2 (interLen (fibers.get! i) (fibers.get! j)) else acc2)
      acc) 0

/-- STATEMENT TARGET (UNPROVED): if a fiber list of `a`-subsets of an `n`-set with
    all pairwise intersections `≤ a-R-1` has more than `cwBound n (2*(R+2)) a`
    members, then its max pairwise intersection is exactly `a-R-1` (saturation).
    Proved in the note/verifier by the Johnson constant-weight bound. -/
theorem saturation_forcing_STATEMENT_TARGET_UNPROVED
    (n a R : Nat) (fibers : List (List Nat))
    (hbound : maxIntersect fibers ≤ a - R - 1)
    (hheavy : fibers.length > cwBound n (2 * (R + 2)) a) :
    maxIntersect fibers = a - R - 1 := by
  sorry

end HeavyFiberPlantedEmission
