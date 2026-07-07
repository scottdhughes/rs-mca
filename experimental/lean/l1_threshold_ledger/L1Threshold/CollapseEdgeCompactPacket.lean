import L1Threshold.CollapseEdgeCertificate
import L1Threshold.CollapseEdgeOriginSummary
import L1Threshold.CollapseEdgeOriginArithmetic

namespace L1Threshold

/-!
# W3 collapse-edge compact packet gate

This module is the small reviewer-facing aggregate for the compact
collapse-edge PR packet. It combines:

* the finite graph checker in `CollapseEdgeCertificate`; and
* the compact origin-audit metadata/count checker in
  `CollapseEdgeOriginSummary`; and
* the compact modular edge-origin arithmetic checker in
  `CollapseEdgeOriginArithmetic`.

It still does not reconstruct the W3 geometry symbolically.
-/

namespace CollapseEdgeCompactPacket

theorem compactPacketOK :
    CollapseEdgeCertificate.checkAllCases = true
      ∧ CollapseEdgeOriginSummary.allCasesOK = true
      ∧ CollapseEdgeOriginArithmetic.allRowsOK = true
      ∧ CollapseEdgeOriginSummary.edgeRulesAudited = 6528
      ∧ CollapseEdgeOriginArithmetic.edgeRows.length = 6528
      ∧ CollapseEdgeOriginSummary.mismatchCount = 0
      ∧ CollapseEdgeCertificate.allCases.map CollapseEdgeCertificate.alternateContribution =
          [1, 1, 1, 1, 1, 1] := by
  exact
    And.intro CollapseEdgeCertificate.collapseEdgeAllCasesOk
      (And.intro CollapseEdgeOriginSummary.originSummaryAllCasesOK
        (And.intro CollapseEdgeOriginArithmetic.edgeOriginArithmeticAllRowsOK
          (And.intro CollapseEdgeOriginSummary.originSummaryEdgeRulesAudited
            (And.intro CollapseEdgeOriginArithmetic.edgeOriginArithmeticRowCount
              (And.intro CollapseEdgeOriginSummary.originSummaryNoMismatches
                CollapseEdgeCertificate.collapseEdgeAllAlternateContributionsExact)))))

theorem compactPacketNoGraphOrSummaryMismatches :
    CollapseEdgeCertificate.checkAllCases = true
      ∧ CollapseEdgeOriginSummary.allCasesOK = true
      ∧ CollapseEdgeOriginArithmetic.allRowsOK = true := by
  exact
    And.intro CollapseEdgeCertificate.collapseEdgeAllCasesOk
      (And.intro CollapseEdgeOriginSummary.originSummaryAllCasesOK
        CollapseEdgeOriginArithmetic.edgeOriginArithmeticAllRowsOK)

#print axioms compactPacketOK
#print axioms compactPacketNoGraphOrSummaryMismatches

end CollapseEdgeCompactPacket
end L1Threshold
