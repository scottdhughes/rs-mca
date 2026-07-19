import Std
import Std.Tactic

/-!
# Route-D owner-typed forest-to-cell compiler v1

This standalone theorem layer records the finite cardinality composition used
by the Route-D compiler. It does not construct the deployed deletion executor,
actual-incidence compiler, forest theorem, or support-level cell injections.
-/

namespace RouteDOwnerTypedForestCellCompilerV1

def baseCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def prefixCommit : String := "e83962ae5ad7bacb391b691ffd37f0abef977b83"
def prefixNoteBlob : String := "591c91a6aac6b48db0c16abc586b74d7a51e44e2"
def allMinorsCommit : String := "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"
def allMinorsNoteBlob : String := "f24ce928df7e7170c1b4f3228d5fe9b184be50b4"
def squareFoldCommit : String := "f64e03a1215653eeafe3186df55269273d9f7653"
def squareFoldNoteBlob : String := "301144d04458027131779907f7f74aa5a6682bf4"
def complementaryChargeCommit : String := "19c061ee094388e3261e8151e6c799826801ae12"
def complementaryChargeNoteBlob : String := "c1bceae338a55c3f94381bf8f71d8b1584f05e95"

theorem exact_source_pins :
    baseCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    prefixCommit = "e83962ae5ad7bacb391b691ffd37f0abef977b83" ∧
    prefixNoteBlob = "591c91a6aac6b48db0c16abc586b74d7a51e44e2" ∧
    allMinorsCommit = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0" ∧
    allMinorsNoteBlob = "f24ce928df7e7170c1b4f3228d5fe9b184be50b4" ∧
    squareFoldCommit = "f64e03a1215653eeafe3186df55269273d9f7653" ∧
    squareFoldNoteBlob = "301144d04458027131779907f7f74aa5a6682bf4" ∧
    complementaryChargeCommit =
      "19c061ee094388e3261e8151e6c799826801ae12" ∧
    complementaryChargeNoteBlob =
      "c1bceae338a55c3f94381bf8f71d8b1584f05e95" := by
  native_decide

structure OwnerRouteGuard where
  actualIncidence : Prop
  allMaximalMinorsVanish : Prop
  routedExactlyOnce : Prop
  fixedTargetPreserved : Prop
  literalCorePreserved : Prop
  carriedKeysPreserved : Prop

def ValidOwnerRoute (guard : OwnerRouteGuard) : Prop :=
  guard.actualIncidence ∧
  guard.allMaximalMinorsVanish ∧
  guard.routedExactlyOnce ∧
  guard.fixedTargetPreserved ∧
  guard.literalCorePreserved ∧
  guard.carriedKeysPreserved

/-- The owner interface exposes every load-bearing clause. This theorem does
not infer actual incidence or all-minors vanishing from a projected label. -/
theorem valid_owner_route_preserves_target_core_and_keys
    (guard : OwnerRouteGuard)
    (valid : ValidOwnerRoute guard) :
    guard.routedExactlyOnce ∧
      guard.fixedTargetPreserved ∧ guard.literalCorePreserved ∧
      guard.carriedKeysPreserved := by
  exact ⟨valid.2.2.1, valid.2.2.2.1, valid.2.2.2.2.1, valid.2.2.2.2.2⟩

/-- One root per forest component identifies every edge with its unique
nonroot child. The graph construction supplies this equality. -/
theorem rooted_forest_edge_nonroot_count
    (primitiveEdges nonrootVertices : Nat)
    (edgeChildBijection : primitiveEdges = nonrootVertices) :
    primitiveEdges = nonrootVertices := by
  exact edgeChildBijection

/-- Cardinality form of the complementary-cell charge theorem. -/
theorem complementary_cell_addback
    (generated primitive markedCells complementCells cellCapacity : Nat)
    (generatedInjective : generated ≤ markedCells)
    (primitiveInjective : primitive ≤ complementCells)
    (cellPartition : markedCells + complementCells = cellCapacity) :
    generated + primitive ≤ cellCapacity := by
  omega

/-- The complete owner-typed forest compiler. The owner gate records the exact
all-minors route, while the arithmetic conclusion uses the full-rank
primitive forest and the two support-level complementary injections. -/
theorem owner_typed_forest_to_complementary_cell_compiler
    (guard : OwnerRouteGuard)
    (generated primitive nonrootVertices markedCells complementCells t p : Nat)
    (validOwner : ValidOwnerRoute guard)
    (edgeChildBijection : primitive = nonrootVertices)
    (generatedInjective : generated ≤ markedCells)
    (nonrootInjective : nonrootVertices ≤ complementCells)
    (cellPartition : markedCells + complementCells = t * p) :
    ValidOwnerRoute guard ∧ generated + primitive ≤ t * p := by
  constructor
  · exact validOwner
  · omega

theorem deployed_capacity_pin :
    67472 * 2130706433 = 143763024447376 := by
  native_decide

/-- The positive finite fixture saturates Fin 2 × F_3: two generated
supports plus four primitive forest edges use all six cells. -/
theorem positive_saturating_fixture_pin :
    4 = 5 - 1 ∧ 2 + 4 = 2 * 3 := by
  native_decide

/-- Exact raw F23 warning: forest orientation does not construct the missing
cell injection. This is pre-first-match and is not a deployed counterexample. -/
theorem raw_f23_forest_cell_capacity_no_go :
    55 > 2 * 23 ∧ 55 - 2 * 23 = 9 := by
  native_decide

end RouteDOwnerTypedForestCellCompilerV1
