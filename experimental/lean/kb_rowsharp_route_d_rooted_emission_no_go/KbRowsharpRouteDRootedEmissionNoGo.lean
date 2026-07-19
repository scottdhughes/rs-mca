/-!
# KoalaBear Route-D rooted-emission no-go toys

This is a small, standalone Lean 4.14 companion for the exact finite toys in
the Route-D rooted-emission no-go packet.  It kernel-checks only:

* the 49 eight-point supports in the primitive `F_17` locator-prefix fiber
  with signed high coefficients `(-e₁,e₂) = (1,9)`;
* minor certificates showing that the full `3 x 9` owner Hankel matrices for
  `E₂ = (1,3)` and `E₃ = (1,3,5)` have ranks two and three over `F_17`;
  the displayed `3 x 4` matrices are their leading windows;
* the `E = (16)` punctured-padding fixture: locator deconvolution from the
  primitive target `(1,9)` to `(0,9)`, algebraic stabilizer `{1,16}` versus
  punctured-domain stabilizer `{1}`, the exact 24-element reconstructed fiber,
  and the rank-one full owner matrix;
* the repaired deep-gate arithmetic `3(t-1)=6 <= n-k=11` and the strict
  arithmetic obstructions `19 > 17` and `24 > 17`.

The final rooted-emission statement is proved only as a conditional finite-
cardinality wrapper.  It is scoped to one fixed line and an exact residual
after the eight named first-match deletions, and assumes the required injective
emission into `Fin t × Fin p`.  It does not construct that emission or claim a
global Route-D support certificate.
-/

namespace KbRowsharpRouteDRootedEmissionNoGo

/-! ## Repaired toy parameters -/

def toyN : Nat := 16
def toyK : Nat := 5
def toyA : Nat := 8
def toyJ : Nat := 8
def toyT : Nat := 3

/-- The fixed line is exactly the monomial direction `g = X^5`. -/
def fixedGExponent : Nat := 5

theorem repaired_parameter_pins :
    toyN = 16 ∧ toyK = 5 ∧ toyA = 8 ∧ toyJ = 8 ∧ toyT = 3 ∧
    fixedGExponent = 5 := by
  native_decide

theorem repaired_deep_gate_arithmetic :
    3 * (toyT - 1) = 6 ∧ toyN - toyK = 11 ∧
    3 * (toyT - 1) ≤ toyN - toyK := by
  native_decide

/-- The numeric input to the degree-five root bound: eight agreements exceed
the degree of `gamma*X^5-h` for `deg h < 5` and `gamma != 0`.  The polynomial
root-bound theorem itself is outside this decidable companion. -/
theorem repaired_root_count_arithmetic : toyK = 5 ∧ toyA = 8 ∧ toyK < toyA := by
  native_decide

/-! ## Primitive `F_17` locator-prefix fiber -/

/-- All `k`-element sublists, retaining the order of the input list. -/
def choose : Nat → List Nat → List (List Nat)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | k + 1, x :: xs =>
      (choose k xs).map (fun ys => x :: ys) ++ choose (k + 1) xs

/-- The nonzero elements of `F_17`, represented canonically by `1,...,16`. -/
def f17Nonzero : List Nat := (List.range 16).map (fun x => x + 1)

/-- The elementary symmetric sum `e₂`. -/
def elementaryTwo : List Nat → Nat
  | [] => 0
  | x :: xs => x * xs.sum + elementaryTwo xs

/-- Signed locator high coefficients `(-e₁,e₂)` reduced modulo 17. -/
def locatorPrefix17 (support : List Nat) : Nat × Nat :=
  ((17 - support.sum % 17) % 17, elementaryTwo support % 17)

def fullTarget17 : Nat × Nat := (1, 9)

/-- The exact primitive locator-prefix fiber used by the no-go toy. -/
def primitiveTargetFiber17 : List (List Nat) :=
  (choose 8 f17Nonzero).filter (fun support => locatorPrefix17 support = fullTarget17)

theorem primitive_target_fiber_has_49_supports :
    primitiveTargetFiber17.length = 49 := by
  native_decide

/-! ## Theorem 3: punctured padding and loss of an acting stabilizer -/

def punctureError17 : List Nat := [16]

def puncturedDomain17 : List Nat :=
  f17Nonzero.filter (fun point => point != 16)

/-- Deconvolve the first two signed locator coefficients through a fixed
locator prefix.  The large positive offset makes the natural-number
representatives safe before reduction modulo 17. -/
def deconvolvePrefix17
    (target fixedPrefix : Nat × Nat) : Nat × Nat :=
  let paddingFirst := (target.1 + 17 - fixedPrefix.1) % 17
  let paddingSecond :=
    (target.2 + 17 * 17 - fixedPrefix.2 - fixedPrefix.1 * paddingFirst) % 17
  (paddingFirst, paddingSecond)

def paddingTarget17 : Nat × Nat :=
  deconvolvePrefix17 fullTarget17 (locatorPrefix17 punctureError17)

/-- Algebraic scaling stabilizer of a signed depth-two target. -/
def prefixTargetStabilizer17 (target : Nat × Nat) : List Nat :=
  f17Nonzero.filter fun scalar =>
    target.1 * scalar % 17 = target.1 ∧
    target.2 * scalar ^ 2 % 17 = target.2

/-- Exact preservation of one finite source set under multiplication. -/
def scalarPreservesSet17 (scalar : Nat) (points : List Nat) : Bool :=
  (points.all fun point => points.contains (scalar * point % 17)) &&
  (points.all fun target =>
    points.any fun point => scalar * point % 17 == target)

def puncturedDomainStabilizer17 : List Nat :=
  f17Nonzero.filter fun scalar => scalarPreservesSet17 scalar puncturedDomain17

/-- Seven-point padding choices on the fixed punctured domain. -/
def paddingFiber17 : List (List Nat) :=
  (choose 7 puncturedDomain17).filter fun padding =>
    locatorPrefix17 padding = paddingTarget17

/-- Reinsert the fixed error point.  Every padding list is increasing inside
`1,...,15`, so appending 16 gives the canonical increasing full support. -/
def reconstructedPaddingFiber17 : List (List Nat) :=
  paddingFiber17.map fun padding => padding ++ punctureError17

def fullTargetFiberContainingPuncture17 : List (List Nat) :=
  primitiveTargetFiber17.filter fun support => support.contains 16

theorem puncture_locator_deconvolution_certificate :
    locatorPrefix17 punctureError17 = (1, 0) ∧
    paddingTarget17 = (0, 9) := by
  native_decide

theorem full_and_padding_stabilizer_certificates :
    prefixTargetStabilizer17 fullTarget17 = [1] ∧
    prefixTargetStabilizer17 paddingTarget17 = [1, 16] ∧
    puncturedDomainStabilizer17 = [1] := by
  native_decide

theorem padding_fiber_reconstruction_certificate :
    paddingFiber17.length = 24 ∧
    reconstructedPaddingFiber17 = fullTargetFiberContainingPuncture17 ∧
    reconstructedPaddingFiber17.all
      (fun support => locatorPrefix17 support == fullTarget17) = true := by
  native_decide

theorem twenty_four_exceeds_seventeen : 24 > 17 := by
  native_decide

/-! ## Exact rank certificates over `F_17` -/

/-- Integer determinant of a `3 x 3` matrix, used before reduction mod 17. -/
def det3 (a b c d e f g h i : Int) : Int :=
  a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

/-- The leading `3 x 4` window for `E₂ = (1,3)`. -/
def e2Entry : Nat → Nat → Int
  | 0, 0 => 13 | 0, 1 => 7 | 0, 2 => 6  | 0, 3 => 3
  | 1, 0 => 7  | 1, 1 => 6 | 1, 2 => 3  | 1, 3 => 11
  | 2, 0 => 6  | 2, 1 => 3 | 2, 2 => 11 | 2, 3 => 1
  | _, _ => 0

/-- The leading `3 x 4` window for `E₃ = (1,3,5)`. -/
def e3Entry : Nat → Nat → Int
  | 0, 0 => 8  | 0, 1 => 16 | 0, 2 => 0  | 0, 3 => 7
  | 1, 0 => 16 | 1, 1 => 0  | 1, 2 => 7  | 1, 3 => 14
  | 2, 0 => 0  | 2, 1 => 7  | 2, 2 => 14 | 2, 3 => 16
  | _, _ => 0

/-- The maximal minor on the three named columns. -/
def maximalMinor (matrix : Nat → Nat → Int) (c₀ c₁ c₂ : Nat) : Int :=
  det3
    (matrix 0 c₀) (matrix 0 c₁) (matrix 0 c₂)
    (matrix 1 c₀) (matrix 1 c₁) (matrix 1 c₂)
    (matrix 2 c₀) (matrix 2 c₁) (matrix 2 c₂)

/-- A `2 x 2` minor on the first two rows and named columns. -/
def firstTwoRowMinor (matrix : Nat → Nat → Int) (c₀ c₁ : Nat) : Int :=
  matrix 0 c₀ * matrix 1 c₁ - matrix 0 c₁ * matrix 1 c₀

/-- A `2 x 2` minor on arbitrary named rows and columns. -/
def minorTwo
    (matrix : Nat → Nat → Int) (r₀ r₁ c₀ c₁ : Nat) : Int :=
  matrix r₀ c₀ * matrix r₁ c₁ - matrix r₀ c₁ * matrix r₁ c₀

/-- A raw power-sum used inside the exact dual-weighted owner entry. -/
def moment17 (errors : List Nat) (degree : Nat) : Nat :=
  ((errors.map (fun x => x ^ degree)).sum) % 17

/-- The full three-row, nine-column owner Hankel matrix.  On `F_17^*` the
exact dual weight is `lambda_x = -x`, hence entry `(a,b)` is
`-sum_{x in E} x^(a+b+1)`. -/
def ownerHankelEntry (errors : List Nat) (row column : Nat) : Int :=
  ((17 - moment17 errors (row + column + 1)) % 17 : Nat)

def e2Errors : List Nat := [1, 3]
def e3Errors : List Nat := [1, 3, 5]

def ownerHankelRow (errors : List Nat) (row : Nat) : List Int :=
  (List.range 9).map (ownerHankelEntry errors row)

theorem exact_full_owner_hankel_rows :
    ownerHankelRow e2Errors 0 = [13, 7, 6, 3, 11, 1, 5, 0, 2] ∧
    ownerHankelRow e2Errors 1 = [7, 6, 3, 11, 1, 5, 0, 2, 8] ∧
    ownerHankelRow e2Errors 2 = [6, 3, 11, 1, 5, 0, 2, 8, 9] ∧
    ownerHankelRow e3Errors 0 = [8, 16, 0, 7, 14, 16, 12, 1, 7] ∧
    ownerHankelRow e3Errors 1 = [16, 0, 7, 14, 16, 12, 1, 7, 16] ∧
    ownerHankelRow e3Errors 2 = [0, 7, 14, 16, 12, 1, 7, 16, 15] := by
  native_decide

/-- Checks that an explicit matrix is the leading `3 x 4` window. -/
def isLeadingWindow
    (explicit : Nat → Nat → Int) (errors : List Nat) : Bool :=
  (List.range 3).all fun row =>
    (List.range 4).all fun column =>
      explicit row column == ownerHankelEntry errors row column

/-- Checks every maximal minor of a three-row, nine-column matrix. -/
def allFullOwnerMaximalMinorsZero
    (matrix : Nat → Nat → Int) : Bool :=
  (choose 3 (List.range 9)).all fun columns =>
    match columns with
    | [c₀, c₁, c₂] => maximalMinor matrix c₀ c₁ c₂ % 17 == 0
    | _ => false

/-- Checks every `2 x 2` minor of a three-row, nine-column matrix. -/
def allFullOwnerTwoMinorsZero
    (matrix : Nat → Nat → Int) : Bool :=
  (choose 2 (List.range 3)).all fun rows =>
    (choose 2 (List.range 9)).all fun columns =>
      match rows, columns with
      | [r₀, r₁], [c₀, c₁] =>
          minorTwo matrix r₀ r₁ c₀ c₁ % 17 == 0
      | _, _ => false

theorem displayed_matrices_are_leading_owner_windows :
    isLeadingWindow e2Entry e2Errors = true ∧
    isLeadingWindow e3Entry e3Errors = true := by
  native_decide

/-- All maximal minors vanish, while one `2 x 2` minor does not: rank `E₂=2`. -/
theorem e2_rank_two_minor_certificate :
    maximalMinor e2Entry 0 1 2 % 17 = 0 ∧
    maximalMinor e2Entry 0 1 3 % 17 = 0 ∧
    maximalMinor e2Entry 0 2 3 % 17 = 0 ∧
    maximalMinor e2Entry 1 2 3 % 17 = 0 ∧
    firstTwoRowMinor e2Entry 0 1 % 17 ≠ 0 := by
  native_decide

/-- A nonzero maximal minor: rank `E₃=3` (the maximum for three rows). -/
theorem e3_rank_three_minor_certificate :
    maximalMinor e3Entry 0 1 2 % 17 = 2 := by
  native_decide

/-- Every maximal minor of the full `3 x 9` matrix vanishes, while a
`2 x 2` minor does not: the full `E₂` owner Hankel rank is exactly two. -/
theorem e2_full_owner_rank_two_certificate :
    allFullOwnerMaximalMinorsZero (ownerHankelEntry e2Errors) = true ∧
    firstTwoRowMinor (ownerHankelEntry e2Errors) 0 1 % 17 ≠ 0 := by
  native_decide

/-- The leading nonzero maximal minor gives full `E₃` owner Hankel rank three. -/
theorem e3_full_owner_rank_three_certificate :
    maximalMinor (ownerHankelEntry e3Errors) 0 1 2 % 17 = 2 := by
  native_decide

/-- A nonzero entry and vanishing of all `2 x 2` minors certify that the full
`3 x 9` owner matrix for `E=(16)` has rank exactly one. -/
theorem puncture_full_owner_rank_one_certificate :
    ownerHankelEntry punctureError17 0 0 % 17 = 1 ∧
    allFullOwnerTwoMinorsZero (ownerHankelEntry punctureError17) = true := by
  native_decide

/-- Aggregate kernel-checked fixture for Theorem 3. -/
theorem punctured_padding_obstruction_fixture :
    locatorPrefix17 punctureError17 = (1, 0) ∧
    paddingTarget17 = (0, 9) ∧
    prefixTargetStabilizer17 fullTarget17 = [1] ∧
    prefixTargetStabilizer17 paddingTarget17 = [1, 16] ∧
    puncturedDomainStabilizer17 = [1] ∧
    paddingFiber17.length = 24 ∧
    reconstructedPaddingFiber17 = fullTargetFiberContainingPuncture17 ∧
    reconstructedPaddingFiber17.all
      (fun support => locatorPrefix17 support == fullTarget17) = true ∧
    24 > 17 ∧
    ownerHankelEntry punctureError17 0 0 % 17 = 1 ∧
    allFullOwnerTwoMinorsZero (ownerHankelEntry punctureError17) = true := by
  native_decide

/-! ## The exact pigeonhole obstruction -/

theorem nineteen_exceeds_seventeen : 19 > 17 := by
  native_decide

/-! ## Scoped conditional cardinality wrapper -/

/-- A marked Route-D support.  `commonCore` is the mark that emission must
preserve; it is not projected away by this interface. -/
structure MarkedSupport where
  support : List Nat
  commonCore : List Nat
deriving DecidableEq

/-- The eight named deletion predicates, in their exact first-match order. -/
structure NamedFirstMatchDeletions where
  generatedField : MarkedSupport → Bool
  quotientPlanted : MarkedSupport → Bool
  sparsePadeHankel : MarkedSupport → Bool
  m1WindowShadow : MarkedSupport → Bool
  rankDropPivot : MarkedSupport → Bool
  bcChart : MarkedSupport → Bool
  spShiftPair : MarkedSupport → Bool
  extensionSlope : MarkedSupport → Bool

/-- Survives all eight named deletions.  Keeping the fields separate makes
the scope auditable and prevents an unnamed aggregate predicate. -/
def survivesNamedFirstMatch
    (deletions : NamedFirstMatchDeletions) (x : MarkedSupport) : Bool :=
  !(deletions.generatedField x) &&
  !(deletions.quotientPlanted x) &&
  !(deletions.sparsePadeHankel x) &&
  !(deletions.m1WindowShadow x) &&
  !(deletions.rankDropPivot x) &&
  !(deletions.bcChart x) &&
  !(deletions.spShiftPair x) &&
  !(deletions.extensionSlope x)

/-- `residual` is exactly the marked part of `ambient` on one fixed line
and at one locator target `z`, after the eight named deletions. -/
def IsExactFixedLineResidual
    (deletions : NamedFirstMatchDeletions)
    (lineOf : MarkedSupport → Nat)
    (targetOf : MarkedSupport → Nat × Nat)
    (fixedLine : Nat) (z : Nat × Nat)
    (ambient residual : List MarkedSupport) : Prop :=
  residual.Nodup ∧
  ∀ x, x ∈ residual ↔
    x ∈ ambient ∧ lineOf x = fixedLine ∧ targetOf x = z ∧
      survivesNamedFirstMatch deletions x = true

/-- A map on a residual list is injective on the marked supports it contains. -/
def InjectiveOnResidual
    {α β : Type} [BEq α]
    (residual : List α) (emit : α → β) : Prop :=
  ∀ ⦃x⦄, x ∈ residual → ∀ ⦃y⦄, y ∈ residual → emit x = emit y → x = y

/--
**Conditional rooted-emission cardinality wrapper, scoped to `g = X^5`.**

`Fin t` is only an indexing envelope for the at-most-`t` rank-drop slopes in
`Z_rankdrop(f_z,g_z)`, and `Fin p` models `F_p`.  Mark preservation is decoded
from the full pair, not from its slope coordinate.  The proof consumes only
duplicate-freeness from `hExact` and the supplied `hInjective`; the exact
residual characterization and mark-preservation hypothesis are retained for
integrated-stub interface continuity and boundary visibility.  This is
bookkeeping only, not a construction of rooted incidence.  The conclusion is
only the local cardinality bound `|V_z| ≤ t*p`; it does not assert the deployed
global support certificate.
-/
theorem rootedEmission_fixedLine_cardinality_of_injective
    (p t : Nat) (z : Nat × Nat)
    (deletions : NamedFirstMatchDeletions)
    (lineOf : MarkedSupport → Nat)
    (targetOf : MarkedSupport → Nat × Nat)
    (ambient residual : List MarkedSupport)
    (hExact : IsExactFixedLineResidual deletions lineOf targetOf
      fixedGExponent z ambient residual)
    (emit : MarkedSupport → Fin t × Fin p)
    (markDecoder : Fin t × Fin p → List Nat)
    (hMarkPreserving : ∀ x ∈ residual, markDecoder (emit x) = x.commonCore)
    (hInjective : InjectiveOnResidual residual emit) :
    residual.length ≤ t * p := by
  let code : MarkedSupport → Nat := fun x =>
    p * (emit x).1.val + (emit x).2.val
  have code_lt (x : MarkedSupport) : code x < t * p := by
    have hstep :
        p * (emit x).1.val + (emit x).2.val <
          p * (emit x).1.val + p :=
      Nat.add_lt_add_left (emit x).2.isLt _
    have hfirst : (emit x).1.val + 1 ≤ t :=
      Nat.succ_le_of_lt (emit x).1.isLt
    dsimp [code]
    calc
      p * (emit x).1.val + (emit x).2.val <
          p * (emit x).1.val + p := hstep
      _ = p * ((emit x).1.val + 1) := by
        rw [Nat.mul_add, Nat.mul_one]
      _ ≤ p * t := Nat.mul_le_mul_left p hfirst
      _ = t * p := Nat.mul_comm p t
  have code_eq_emit_eq {x y : MarkedSupport}
      (h : code x = code y) : emit x = emit y := by
    have hp : 0 < p :=
      Nat.lt_of_le_of_lt (Nat.zero_le _) (emit x).2.isLt
    have hsnd : (emit x).2.val = (emit y).2.val := by
      have hm := congrArg (fun n => n % p) h
      dsimp [code] at hm
      rw [Nat.mul_add_mod, Nat.mod_eq_of_lt (emit x).2.isLt,
        Nat.mul_add_mod, Nat.mod_eq_of_lt (emit y).2.isLt] at hm
      exact hm
    have hfst : (emit x).1.val = (emit y).1.val := by
      have hmul : p * (emit x).1.val = p * (emit y).1.val := by
        dsimp [code] at h
        rw [hsnd] at h
        exact Nat.add_right_cancel h
      exact Nat.mul_left_cancel hp hmul
    exact Prod.ext (Fin.eq_of_val_eq hfst) (Fin.eq_of_val_eq hsnd)
  have codesNodup : (residual.map code).Nodup := by
    rw [List.Nodup, List.pairwise_map]
    exact hExact.1.imp_of_mem fun hx hy hxy hcode =>
      hxy (hInjective hx hy (code_eq_emit_eq hcode))
  have nodup_length_le_of_subset :
      ∀ (xs ys : List Nat), xs.Nodup → xs ⊆ ys → xs.length ≤ ys.length := by
    intro xs
    induction xs with
    | nil => simp
    | cons x xs ih =>
        intro ys hNodup hSubset
        have hx : x ∈ ys := hSubset (List.mem_cons_self x xs)
        have hTail : xs ⊆ ys.eraseP (fun a => a == x) := by
          intro a ha
          rw [List.mem_eraseP_of_neg]
          · exact hSubset (List.mem_cons_of_mem x ha)
          · intro hax
            have : a = x := eq_of_beq hax
            subst a
            exact (List.nodup_cons.mp hNodup).1 ha
        have hle := ih (ys.eraseP (fun a => a == x))
          (List.nodup_cons.mp hNodup).2 hTail
        cases ys with
        | nil => simp at hx
        | cons y ys =>
            have hpx : (fun a : Nat => a == x) x = true :=
              beq_self_eq_true x
            rw [List.length_eraseP_of_mem
              (p := fun a : Nat => a == x) hx hpx] at hle
            simp only [List.length_cons, Nat.add_one_sub_one] at hle ⊢
            exact Nat.succ_le_succ hle
  have codesSubset : residual.map code ⊆ List.range (t * p) := by
    intro n hn
    obtain ⟨x, _, rfl⟩ := List.mem_map.mp hn
    exact List.mem_range.mpr (code_lt x)
  have hle := nodup_length_le_of_subset
    (residual.map code) (List.range (t * p)) codesNodup codesSubset
  simpa using hle

/-- Compatibility alias for the original statement-target name.  Despite the
historical `_unproved` suffix, this declaration is a proved forwarding theorem.
New consumers should use `rootedEmission_fixedLine_cardinality_of_injective`. -/
theorem rootedEmission_fixedLine_target_unproved
    (p t : Nat) (z : Nat × Nat)
    (deletions : NamedFirstMatchDeletions)
    (lineOf : MarkedSupport → Nat)
    (targetOf : MarkedSupport → Nat × Nat)
    (ambient residual : List MarkedSupport)
    (hExact : IsExactFixedLineResidual deletions lineOf targetOf
      fixedGExponent z ambient residual)
    (emit : MarkedSupport → Fin t × Fin p)
    (markDecoder : Fin t × Fin p → List Nat)
    (hMarkPreserving : ∀ x ∈ residual, markDecoder (emit x) = x.commonCore)
    (hInjective : InjectiveOnResidual residual emit) :
    residual.length ≤ t * p := by
  exact rootedEmission_fixedLine_cardinality_of_injective
    p t z deletions lineOf targetOf ambient residual hExact emit markDecoder
      hMarkPreserving hInjective

#print axioms rootedEmission_fixedLine_cardinality_of_injective
#print axioms rootedEmission_fixedLine_target_unproved

end KbRowsharpRouteDRootedEmissionNoGo
