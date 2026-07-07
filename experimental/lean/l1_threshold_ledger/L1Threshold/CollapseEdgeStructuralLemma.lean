import L1Threshold.CollapseEdgeCertificate

namespace L1Threshold

/-!
# W3 collapse-edge structural lemma wrapper

This module repackages the finite graph certificate from
`CollapseEdgeCertificate` into the proof-facing implication used by the W3
block memo:

* for the six stored dangerous cases, the head antecedent is
  `(missing,stray)=(2,1)`;
* those dangerous cases have alternate contribution at most `1`;
* in fact the only large alternate component is the coset-37 triple
  `[17,36,130]`, so the alternate contribution is exactly `1`.

Scope:

* finite graph certificate only;
* no reconstruction of the underlying `GF(137)` arithmetic;
* no symbolic W3 lemma or global L1 theorem.
-/

namespace CollapseEdgeStructuralLemma

set_option maxRecDepth 1000000
set_option maxHeartbeats 2000000

open CollapseEdgeCertificate

def dangerousAntecedent (caseCert : CaseCert) : Bool :=
  (caseCert.headMissing == 2) && (caseCert.headStray == 1)

def alternateCollapseConclusion (caseCert : CaseCert) : Bool :=
  decide (alternateContribution caseCert <= 1)

def dangerousImpliesAlternateCollapse (caseCert : CaseCert) : Bool :=
  (! dangerousAntecedent caseCert) || alternateCollapseConclusion caseCert

def uniqueCoset37SurvivorConclusion (caseCert : CaseCert) : Bool :=
  (alternateLarge caseCert == [collapseEdgeSurvivor])
    && (alternateContribution caseCert == 1)

def structuralCaseConclusion (caseCert : CaseCert) : Bool :=
  dangerousAntecedent caseCert
    && alternateCollapseConclusion caseCert
    && uniqueCoset37SurvivorConclusion caseCert

def allDangerousAntecedents : Bool :=
  allCases.all dangerousAntecedent

def allDangerousCasesCollapse : Bool :=
  allCases.all dangerousImpliesAlternateCollapse

def allDangerousCasesHaveUniqueSurvivor : Bool :=
  allCases.all uniqueCoset37SurvivorConclusion

def allStructuralCasesOK : Bool :=
  allCases.all structuralCaseConclusion

theorem allDangerousAntecedentsOK :
    allDangerousAntecedents = true := by
  decide

theorem dangerousPatternForcesAlternateCollapse :
    allDangerousCasesCollapse = true := by
  decide

theorem dangerousPatternForcesUniqueCoset37Survivor :
    allDangerousCasesHaveUniqueSurvivor = true := by
  decide

theorem dangerousPatternStructuralPacketOK :
    allStructuralCasesOK = true := by
  decide

theorem structuralAlternateContributionsExact :
    allCases.map alternateContribution = [1, 1, 1, 1, 1, 1] := by
  decide

theorem structuralActualSurvivorsSame :
    allCases.map alternateLarge = collapseEdgeExpectedSurvivorPattern := by
  decide

#print axioms allDangerousAntecedentsOK
#print axioms dangerousPatternForcesAlternateCollapse
#print axioms dangerousPatternForcesUniqueCoset37Survivor
#print axioms dangerousPatternStructuralPacketOK

end CollapseEdgeStructuralLemma
end L1Threshold
