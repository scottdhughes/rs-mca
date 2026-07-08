import L1Threshold.CollapseEdgeCertificate
import L1Threshold.CollapseEdgeOriginSummary
import L1Threshold.CollapseEdgeStructuralLemma
import L1Threshold.CollapseEdgeGraphMechanism
import L1Threshold.CollapseEdgeOriginDot
import L1Threshold.CollapseEdgeOriginArithmetic

namespace L1Threshold

/-!
# W3 collapse-edge compact packet gate

This module is the small reviewer-facing aggregate for the compact
collapse-edge PR packet. It combines:

* the finite graph checker in `CollapseEdgeCertificate`; and
* the compact origin-audit metadata/count checker in
  `CollapseEdgeOriginSummary`; and
* the proof-facing dangerous-pattern wrapper in
  `CollapseEdgeStructuralLemma`; and
* the matching/triangle graph-mechanism checker in
  `CollapseEdgeGraphMechanism`; and
* the compact origin dot-product checker in `CollapseEdgeOriginDot`; and
* the compact modular edge-origin arithmetic checker in
  `CollapseEdgeOriginArithmetic`.

It still does not reconstruct the W3 geometry symbolically.
-/

namespace CollapseEdgeCompactPacket

theorem compactPacketOK :
    CollapseEdgeCertificate.checkAllCases = true
      ∧ CollapseEdgeOriginSummary.allCasesOK = true
      ∧ CollapseEdgeStructuralLemma.allStructuralCasesOK = true
      ∧ CollapseEdgeGraphMechanism.allGraphMechanismsOK = true
      ∧ CollapseEdgeGraphMechanism.allEdgeRuleMechanismsOK = true
      ∧ CollapseEdgeOriginDot.allRowsOK = true
      ∧ CollapseEdgeOriginArithmetic.allRowsOK = true
      ∧ CollapseEdgeOriginSummary.edgeRulesAudited = 6528
      ∧ CollapseEdgeOriginDot.edgeRows.length = 6528
      ∧ CollapseEdgeOriginArithmetic.edgeRows.length = 6528
      ∧ CollapseEdgeOriginSummary.mismatchCount = 0
      ∧ CollapseEdgeCertificate.allCases.map CollapseEdgeCertificate.alternateContribution =
          [1, 1, 1, 1, 1, 1] := by
  exact
    And.intro CollapseEdgeCertificate.collapseEdgeAllCasesOk
      (And.intro CollapseEdgeOriginSummary.originSummaryAllCasesOK
        (And.intro CollapseEdgeStructuralLemma.dangerousPatternStructuralPacketOK
          (And.intro CollapseEdgeGraphMechanism.allGraphMechanismsCertified
            (And.intro CollapseEdgeGraphMechanism.allEdgeRuleMechanismsCertified
              (And.intro CollapseEdgeOriginDot.edgeOriginDotAllRowsOK
                (And.intro CollapseEdgeOriginArithmetic.edgeOriginArithmeticAllRowsOK
                  (And.intro CollapseEdgeOriginSummary.originSummaryEdgeRulesAudited
                    (And.intro CollapseEdgeOriginDot.edgeOriginDotRowCount
                      (And.intro CollapseEdgeOriginArithmetic.edgeOriginArithmeticRowCount
                        (And.intro CollapseEdgeOriginSummary.originSummaryNoMismatches
                          CollapseEdgeCertificate.collapseEdgeAllAlternateContributionsExact))))))))))

theorem compactPacketNoGraphOrSummaryMismatches :
    CollapseEdgeCertificate.checkAllCases = true
      ∧ CollapseEdgeOriginSummary.allCasesOK = true
      ∧ CollapseEdgeStructuralLemma.allStructuralCasesOK = true
      ∧ CollapseEdgeGraphMechanism.allGraphMechanismsOK = true
      ∧ CollapseEdgeGraphMechanism.allEdgeRuleMechanismsOK = true
      ∧ CollapseEdgeOriginDot.allRowsOK = true
      ∧ CollapseEdgeOriginArithmetic.allRowsOK = true := by
  exact
    And.intro CollapseEdgeCertificate.collapseEdgeAllCasesOk
      (And.intro CollapseEdgeOriginSummary.originSummaryAllCasesOK
        (And.intro CollapseEdgeStructuralLemma.dangerousPatternStructuralPacketOK
          (And.intro CollapseEdgeGraphMechanism.allGraphMechanismsCertified
            (And.intro CollapseEdgeGraphMechanism.allEdgeRuleMechanismsCertified
              (And.intro CollapseEdgeOriginDot.edgeOriginDotAllRowsOK
                CollapseEdgeOriginArithmetic.edgeOriginArithmeticAllRowsOK)))))

theorem compactPacketStructuralLemmaOK :
    CollapseEdgeStructuralLemma.allDangerousCasesCollapse = true
      ∧ CollapseEdgeStructuralLemma.allDangerousCasesHaveUniqueSurvivor = true
      ∧ CollapseEdgeStructuralLemma.allStructuralCasesOK = true := by
  decide

theorem compactPacketGraphMechanismOK :
    CollapseEdgeGraphMechanism.allGraphMechanismsOK = true
      ∧ CollapseEdgeGraphMechanism.allEdgeRuleMechanismsOK = true := by
  exact
    And.intro CollapseEdgeGraphMechanism.allGraphMechanismsCertified
      CollapseEdgeGraphMechanism.allEdgeRuleMechanismsCertified

#print axioms compactPacketOK
#print axioms compactPacketNoGraphOrSummaryMismatches
#print axioms compactPacketStructuralLemmaOK
#print axioms compactPacketGraphMechanismOK

end CollapseEdgeCompactPacket
end L1Threshold
