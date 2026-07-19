import Std

/-!
# Route-D marked-puncture contact recursion v1

This standalone module records the theorem interfaces isolated by the Route-D
research packet.  It proves the exact carried-Q recursion, first-match
partition, and hereditary cardinality bridge from their explicit structural
hypotheses.  The finite F_7/F_11 arithmetic and obstruction pins below them are
also kernel checked.

Exact source provenance (Git object identities):

* repository commit: `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`;
* predecessor `rowsharp_q_prefix_atom_reductions_v1.md` blob:
  `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
* governing `agents.md` blob:
  `2fea2bce6a348105f0016fcf739b5247bf408d93`;
* predecessor `experimental/agents-log.md` blob:
  `45b04597efb40741b807e48b290a0544f2fe6baf`.

Verifier:
`experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py`.
-/

namespace RouteDMarkedPunctureContactRecursionV1

/-! ## Exact provenance pins -/

def sourceCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def rowsharpPredecessorBlob : String := "591c91a6aac6b48db0c16abc586b74d7a51e44e2"
def agentsBlob : String := "2fea2bce6a348105f0016fcf739b5247bf408d93"
def agentsLogPredecessorBlob : String := "45b04597efb40741b807e48b290a0544f2fe6baf"

theorem exact_source_sha_pins :
    sourceCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    rowsharpPredecessorBlob = "591c91a6aac6b48db0c16abc586b74d7a51e44e2" ∧
    agentsBlob = "2fea2bce6a348105f0016fcf739b5247bf408d93" ∧
    agentsLogPredecessorBlob = "45b04597efb40741b807e48b290a0544f2fe6baf" := by
  native_decide

/-! ## Generic marked-puncture interfaces

`Q (insert b P)`, not `Q P`, is the carried predicate.  The common root mark
`b` remains an argument of both child admissibility and insertion.  Thus these
interfaces do not silently quotient by a root-blind scalar action.
-/

universe u v w

section GenericInterfaces

variable {Root : Type u} {Parent : Type v} {Child : Type w}

/-- A stdlib-only equivalence record (Lean 4.14 core has no `Equiv`). -/
structure ExactEquiv (α : Type v) (β : Type w) where
  toFun : α → β
  invFun : β → α
  leftInv : ∀ x, invFun (toFun x) = x
  rightInv : ∀ y, toFun (invFun y) = y

def LeastContactParent
    (parentGood : Parent → Prop) (Q : Parent → Prop)
    (leastContact : Root → Parent → Prop) (b : Root) (S : Parent) : Prop :=
  parentGood S ∧ Q S ∧ leastContact b S

def CarriedQChild
    (childGood : Root → Child → Prop) (Q : Parent → Prop)
    (insert : Root → Child → Parent) (b : Root) (P : Child) : Prop :=
  childGood b P ∧ Q (insert b P)

/-- Exact least-contact erase/insert equivalence.  `forwardStructural` contains
the signed locator deconvolution, punctured domain, weight drop, and exclusion
of earlier boundary roots.  `backwardStructural` is its marked insertion
converse.  The inverse laws require the mark to be preserved explicitly.

The global algebraic structural hypotheses remain explicit inputs: this theorem
only packages them into the carried-key equivalence.
-/
theorem carriedQ_leastContact_erase_insert_equiv
    (parentGood : Parent → Prop) (childGood : Root → Child → Prop)
    (Q : Parent → Prop) (leastContact : Root → Parent → Prop)
    (erase : Root → Parent → Child) (insert : Root → Child → Parent)
    (b : Root)
    (forwardStructural : ∀ S, parentGood S → leastContact b S →
      childGood b (erase b S))
    (backwardStructural : ∀ P, childGood b P →
      parentGood (insert b P) ∧ leastContact b (insert b P))
    (eraseInsert : ∀ P, childGood b P → erase b (insert b P) = P)
    (insertErase : ∀ S, parentGood S → leastContact b S →
      insert b (erase b S) = S) :
    Nonempty (ExactEquiv
      {S : Parent // LeastContactParent parentGood Q leastContact b S}
      {P : Child // CarriedQChild childGood Q insert b P}) := by
  let toChild :
      {S : Parent // LeastContactParent parentGood Q leastContact b S} →
        {P : Child // CarriedQChild childGood Q insert b P} :=
    fun S => ⟨erase b S.1, by
      rcases S.2 with ⟨hParent, hQ, hLeast⟩
      refine ⟨forwardStructural S.1 hParent hLeast, ?_⟩
      simpa only [insertErase S.1 hParent hLeast] using hQ⟩
  let toParent :
      {P : Child // CarriedQChild childGood Q insert b P} →
        {S : Parent // LeastContactParent parentGood Q leastContact b S} :=
    fun P => ⟨insert b P.1, by
      rcases P.2 with ⟨hChild, hQ⟩
      rcases backwardStructural P.1 hChild with ⟨hParent, hLeast⟩
      exact ⟨hParent, hQ, hLeast⟩⟩
  refine ⟨{
    toFun := toChild
    invFun := toParent
    leftInv := ?_
    rightInv := ?_
  }⟩
  · intro S
    apply Subtype.ext
    change insert b (erase b S.1) = S.1
    exact insertErase S.1 S.2.1 S.2.2.2
  · intro P
    apply Subtype.ext
    change erase b (insert b P.1) = P.1
    exact eraseInsert P.1 P.2.1

def HasBoundaryContact
    (allowed : Root → Prop) (touches : Root → Parent → Prop) (S : Parent) : Prop :=
  ∃ b, allowed b ∧ touches b S

def IsLeastContact
    (allowed : Root → Prop) (precedes : Root → Root → Prop)
    (touches : Root → Parent → Prop) (b : Root) (S : Parent) : Prop :=
  allowed b ∧ touches b S ∧
    ∀ a, allowed a → precedes a b → ¬ touches a S

def HasUniqueLeastContact
    (allowed : Root → Prop) (precedes : Root → Root → Prop)
    (touches : Root → Parent → Prop) (S : Parent) : Prop :=
  ∃ b, IsLeastContact allowed precedes touches b S ∧
    ∀ c, IsLeastContact allowed precedes touches c S → c = b

/-- The named first-match deletions partition every boundary-contact parent:
existence supplies a least marked root and uniqueness makes distinct cells
disjoint.  This statement deliberately keeps the common-core mark `b`.

The global ordered boundary and support family remain explicit inputs and must
still be instantiated by the Route-D owner.
-/
theorem least_contact_partition
    (parentGood : Parent → Prop) (allowed : Root → Prop)
    (precedes : Root → Root → Prop) (touches : Root → Parent → Prop)
    (firstExists : ∀ S, parentGood S → HasBoundaryContact allowed touches S →
      ∃ b, IsLeastContact allowed precedes touches b S)
    (firstUnique : ∀ S b c,
      IsLeastContact allowed precedes touches b S →
      IsLeastContact allowed precedes touches c S → b = c) :
    ∀ S, parentGood S →
      (HasBoundaryContact allowed touches S ↔
        HasUniqueLeastContact allowed precedes touches S) := by
  intro S hParent
  constructor
  · intro hContact
    obtain ⟨b, hb⟩ := firstExists S hParent hContact
    refine ⟨b, hb, ?_⟩
    intro c hc
    exact firstUnique S c b hc hb
  · rintro ⟨b, hb, _⟩
    exact ⟨b, hb.1, hb.2.1⟩

/-- Summed hereditary cardinality transfer.  `cellCard = carriedCard` is the
cardinality shadow of `carriedQ_leastContact_erase_insert_equiv`.
`carriedHasQ`, `deletionHereditary`, and `coarseAccepts` explicitly construct
the inclusion from the carried child family into the coarse hereditary family;
`inclusionCardBound` consumes that inclusion.  Invariance or child freeness is
not assumed.

Producing the concrete local bound for every nonvanishing pivot, or routing a
vanishing pivot to the existing rank-drop owner, remains a global obligation.
-/
theorem hereditary_cardinality_bound
    (roots : List Root) (cellCard carriedCard coarseChildCard : Root → Nat)
    (Q : Parent → Prop) (Qchild : Child → Prop)
    (insert : Root → Child → Parent)
    (carriedMember childStructural coarseMember : Root → Child → Prop)
    (carriedHasQ : ∀ b P, carriedMember b P → Q (insert b P))
    (carriedHasStructure : ∀ b P, carriedMember b P → childStructural b P)
    (deletionHereditary : ∀ b P, Q (insert b P) → Qchild P)
    (coarseAccepts : ∀ b P, childStructural b P → Qchild P → coarseMember b P)
    (exactCarriedCard : ∀ b, cellCard b = carriedCard b)
    (inclusionCardBound : ∀ b,
      (∀ P, carriedMember b P → coarseMember b P) →
      carriedCard b ≤ coarseChildCard b) :
    (roots.map cellCard).sum ≤ (roots.map coarseChildCard).sum := by
  have pointwise (b : Root) : cellCard b ≤ coarseChildCard b := by
    rw [exactCarriedCard b]
    apply inclusionCardBound b
    intro P hCarried
    apply coarseAccepts b P
    · exact carriedHasStructure b P hCarried
    · exact deletionHereditary b P (carriedHasQ b P hCarried)
  induction roots with
  | nil => simp
  | cons b roots ih =>
      simpa using Nat.add_le_add (pointwise b) ih

end GenericInterfaces

/-! ## Kernel-checked locator and fixture pins -/

def sumMod (p : Nat) (xs : List Nat) : Nat :=
  xs.foldl (fun acc x => (acc + x) % p) 0

/-- First coefficient of `prod_{x in S} (1 - x X)` over `F_p`. -/
def locatorA1 (p : Nat) (support : List Nat) : Nat :=
  (p - sumMod p support) % p

def pairProductSumMod (p : Nat) : List Nat → Nat
  | [] => 0
  | x :: xs =>
      ((xs.foldl (fun acc y => (acc + x * y) % p) 0) +
        pairProductSumMod p xs) % p

def tripleProductSumMod (p : Nat) : List Nat → Nat
  | [] => 0
  | x :: xs =>
      (tripleProductSumMod p xs + x * pairProductSumMod p xs) % p

def locatorPrefix2 (p : Nat) (support : List Nat) : List Nat :=
  [locatorA1 p support, pairProductSumMod p support]

def locatorPrefix3 (p : Nat) (support : List Nat) : List Nat :=
  [locatorA1 p support, pairProductSumMod p support,
    (p - tripleProductSumMod p support) % p]

def deconvolveAux (p root previous : Nat) : List Nat → List Nat
  | [] => []
  | a :: rest =>
      let child := (a + root * previous) % p
      child :: deconvolveAux p root child rest

/-- Signed folding recurrence `child_d = parent_d + b * child_(d-1)`. -/
def deconvolve (p root : Nat) (coeffs : List Nat) : List Nat :=
  deconvolveAux p root 1 coeffs

def firstContact (boundary support : List Nat) : Option Nat :=
  boundary.find? (fun b => support.contains b)

def f7Parents : List (List Nat) := [[1, 2, 3], [2, 5, 6], [3, 4, 6]]

theorem f7_parent_fibre_locator_pin :
    f7Parents.map (locatorA1 7) = [1, 1, 1] := by
  native_decide

theorem f7_least_contact_pin :
    f7Parents.map (firstContact [1, 2, 3]) = [some 1, some 2, some 3] := by
  native_decide

theorem f7_signed_deconvolution_pin :
    [1, 2, 3].map (fun b => deconvolve 7 b [1]) = [[2], [3], [4]] := by
  native_decide

theorem f11_parent_and_signed_children_pin :
    locatorPrefix2 11 [1, 2, 3] = [5, 0] ∧
    deconvolve 11 1 [5, 0] = [6, 6] ∧
    deconvolve 11 2 [5, 0] = [7, 3] := by
  native_decide

def rawContactCell (b : Nat) (supports : List (List Nat)) : List (List Nat) :=
  supports.filter (fun support => support.contains b)

def leastContactCell (boundary : List Nat) (b : Nat)
    (supports : List (List Nat)) : List (List Nat) :=
  supports.filter (fun support => firstContact boundary support == some b)

/-- The raw F_11 cells overlap, while the named first-match deletion assigns the
single support only to root 1. -/
theorem f11_raw_overlap_and_first_match_pin :
    (rawContactCell 1 [[1, 2, 3]]).length = 1 ∧
    (rawContactCell 2 [[1, 2, 3]]).length = 1 ∧
    (leastContactCell [1, 2] 1 [[1, 2, 3]]).length = 1 ∧
    (leastContactCell [1, 2] 2 [[1, 2, 3]]).length = 0 := by
  native_decide

def sortTriple : List Nat → List Nat
  | [x, y, z] =>
      let lo := min x (min y z)
      let hi := max x (max y z)
      [lo, x + y + z - lo - hi, hi]
  | xs => xs

def scaleTripleMod (p a : Nat) (support : List Nat) : List Nat :=
  sortTriple (support.map (fun x => (a * x) % p))

def supportOrbitTriple (p : Nat) (scalars support : List Nat) : List (List Nat) :=
  (scalars.map (fun a => scaleTripleMod p a support)).eraseDups

def supportStabilizerTriple (p : Nat) (scalars support : List Nat) : List Nat :=
  scalars.filter (fun a => scaleTripleMod p a support == support)

def scaleTargetAux (p a degree : Nat) : List Nat → List Nat
  | [] => []
  | c :: rest => ((a ^ degree * c) % p) :: scaleTargetAux p a (degree + 1) rest

def targetStabilizer (p : Nat) (scalars target : List Nat) : List Nat :=
  scalars.filter (fun a => scaleTargetAux p a 1 target == target)

def avoidsFive (support : List Nat) : Bool := !(support.contains 5)

def f11RootBlindPadOrbit : List (List Nat) :=
  supportOrbitTriple 11 [1, 10] [2, 3, 6]

/-- Genuine root-blind Q guard: both pads avoid the full marked-root orbit
`{1,10}`, the full parent target is primitive, but the hereditary predicate
`5 notin S` distinguishes the two valid pads. -/
theorem f11_root_blind_q_noninvariance_pin :
    locatorPrefix2 11 [1, 2, 3, 6] = [10, 3] ∧
    targetStabilizer 11 [1,2,3,4,5,6,7,8,9,10] [10, 3] = [1] ∧
    locatorPrefix2 11 [2, 3, 6] = [0, 3] ∧
    targetStabilizer 11 [1,2,3,4,5,6,7,8,9,10] [0, 3] = [1, 10] ∧
    f11RootBlindPadOrbit = [[2, 3, 6], [5, 8, 9]] ∧
    f11RootBlindPadOrbit.all
      (fun pad => !(pad.any (fun x => [1, 10].contains x))) = true ∧
    avoidsFive [1, 2, 3, 6] = true ∧
    f11RootBlindPadOrbit.map avoidsFive = [true, false] := by
  native_decide

def f7RootBlindPadOrbit : List (List Nat) :=
  supportOrbitTriple 7 [1, 2, 4] [1, 2, 4]

/-- Genuine nonfree root-blind guard: the pad avoids the entire marked-root
orbit `{3,5,6}` and is fixed by all of `H={1,2,4}`, although the full parent
target is primitive.  Hence the root-blind pad orbit has size one, not three. -/
theorem f7_root_blind_nonfree_orbit_pin :
    locatorPrefix3 7 [1, 2, 3, 4] = [4, 0, 6] ∧
    targetStabilizer 7 [1,2,3,4,5,6] [4, 0, 6] = [1] ∧
    locatorPrefix3 7 [1, 2, 4] = [0, 0, 6] ∧
    targetStabilizer 7 [1,2,3,4,5,6] [0, 0, 6] = [1, 2, 4] ∧
    supportStabilizerTriple 7 [1, 2, 4] [1, 2, 4] = [1, 2, 4] ∧
    f7RootBlindPadOrbit = [[1, 2, 4]] ∧
    f7RootBlindPadOrbit.length = 1 ∧
    [1, 2, 4].length = 3 ∧
    [1, 2, 4].all (fun x => !([3, 5, 6].contains x)) = true := by
  native_decide

theorem exhaustive_control_counts_pin :
    2 ^ f7Parents.length = 8 ∧ 3 ^ f7Parents.length = 27 ∧ 27 - 2 ^ 3 = 19 := by
  native_decide

#print axioms carriedQ_leastContact_erase_insert_equiv
#print axioms least_contact_partition
#print axioms hereditary_cardinality_bound

end RouteDMarkedPunctureContactRecursionV1
