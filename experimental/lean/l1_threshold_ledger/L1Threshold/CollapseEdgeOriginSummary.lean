namespace L1Threshold

/-!
# W3 collapse-edge compact origin-audit summary

This file Lean-checks the compact origin-audit metadata shipped with the
collapse-edge packet. It intentionally does not replay the omitted per-edge
`GF(137)` affine arithmetic. Instead, it checks that the compact summary has
the expected six-case/two-family shape, zero mismatches, and the repeated
coset-level rule-count pattern audited by the Python edge-origin script.
-/

namespace CollapseEdgeOriginSummary

inductive Family where
  | v7
  | v11
deriving Repr, DecidableEq, BEq

structure RuleCounts where
  always : Nat
  atShift : Nat
  never : Nat
deriving Repr, DecidableEq, BEq

structure CosetSummary where
  cosetW : Nat
  isHead : Bool
  pointCount : Nat
  edgeRuleCount : Nat
  stored : RuleCounts
  expected : RuleCounts
  slopeZeroInterceptZero : Nat
  slopeNonzero : Nat
  slopeZeroInterceptNonzero : Nat
  mismatchCount : Nat
deriving Repr, DecidableEq, BEq

structure CaseSummary where
  family : Family
  quotientA : Nat
  quotientB : Nat
  shift : Nat
  ell : Nat
  p : Nat
  edgeRulesAudited : Nat
  cosetsAudited : Nat
  mismatchCount : Nat
  storedTotal : RuleCounts
  cosets : List CosetSummary
deriving Repr, DecidableEq, BEq

def totalRules (c : RuleCounts) : Nat :=
  c.always + c.atShift + c.never

def countsOK (c : RuleCounts) : Bool :=
  totalRules c == 136

def cosetOK (c : CosetSummary) : Bool :=
  c.pointCount == 17
    && c.edgeRuleCount == 136
    && c.mismatchCount == 0
    && c.stored == c.expected
    && c.stored.always == c.slopeZeroInterceptZero
    && c.stored.atShift == c.slopeNonzero
    && c.stored.never == c.slopeZeroInterceptNonzero
    && countsOK c.stored

def caseOK (c : CaseSummary) : Bool :=
  c.ell == 17
    && c.p == 137
    && c.edgeRulesAudited == 1088
    && c.cosetsAudited == 8
    && c.mismatchCount == 0
    && c.storedTotal == { always := 70, atShift := 976, never := 42 }
    && c.cosets.length == 8
    && c.cosets.all cosetOK

def mkCoset (w : Nat) (isHead : Bool) (counts : RuleCounts) : CosetSummary :=
  {
    cosetW := w
    isHead := isHead
    pointCount := 17
    edgeRuleCount := 136
    stored := counts
    expected := counts
    slopeZeroInterceptZero := counts.always
    slopeNonzero := counts.atShift
    slopeZeroInterceptNonzero := counts.never
    mismatchCount := 0
  }

def headCounts : RuleCounts := { always := 66, atShift := 45, never := 25 }
def alt1Counts : RuleCounts := { always := 1, atShift := 133, never := 2 }
def altGenericCounts : RuleCounts := { always := 0, atShift := 133, never := 3 }
def survivorCounts : RuleCounts := { always := 3, atShift := 133, never := 0 }
def totalCounts : RuleCounts := { always := 70, atShift := 976, never := 42 }

def standardCosets : List CosetSummary :=
  [
    mkCoset 10 true headCounts,
    mkCoset 1 false alt1Counts,
    mkCoset 127 false altGenericCounts,
    mkCoset 100 false altGenericCounts,
    mkCoset 96 false altGenericCounts,
    mkCoset 136 false altGenericCounts,
    mkCoset 37 false survivorCounts,
    mkCoset 41 false altGenericCounts
  ]

def mkCase (family : Family) (a b shift : Nat) : CaseSummary :=
  {
    family := family
    quotientA := a
    quotientB := b
    shift := shift
    ell := 17
    p := 137
    edgeRulesAudited := 1088
    cosetsAudited := 8
    mismatchCount := 0
    storedTotal := totalCounts
    cosets := standardCosets
  }

def case0 : CaseSummary := mkCase Family.v7 83 96 67
def case1 : CaseSummary := mkCase Family.v7 83 96 103
def case2 : CaseSummary := mkCase Family.v7 83 96 111
def case3 : CaseSummary := mkCase Family.v11 105 38 17
def case4 : CaseSummary := mkCase Family.v11 105 38 20
def case5 : CaseSummary := mkCase Family.v11 105 38 121

def allCases : List CaseSummary := [case0, case1, case2, case3, case4, case5]

def allCasesOK : Bool := allCases.all caseOK

def edgeRulesAudited : Nat := allCases.foldl (fun acc c => acc + c.edgeRulesAudited) 0
def mismatchCount : Nat := allCases.foldl (fun acc c => acc + c.mismatchCount) 0

theorem originSummaryAllCasesOK : allCasesOK = true := by
  decide

theorem originSummaryCaseCount : allCases.length = 6 := by
  decide

theorem originSummaryEdgeRulesAudited : edgeRulesAudited = 6528 := by
  decide

theorem originSummaryNoMismatches : mismatchCount = 0 := by
  decide

theorem originSummaryTwoFamilies :
    allCases.map (fun c => (c.family, c.quotientA, c.quotientB, c.shift)) =
      [(Family.v7, 83, 96, 67), (Family.v7, 83, 96, 103), (Family.v7, 83, 96, 111),
       (Family.v11, 105, 38, 17), (Family.v11, 105, 38, 20), (Family.v11, 105, 38, 121)] := by
  decide

theorem originSummaryRepeatedCosetPattern :
    allCases.map CaseSummary.cosets =
      [standardCosets, standardCosets, standardCosets,
       standardCosets, standardCosets, standardCosets] := by
  decide

#print axioms originSummaryAllCasesOK
#print axioms originSummaryEdgeRulesAudited
#print axioms originSummaryTwoFamilies

end CollapseEdgeOriginSummary
end L1Threshold
