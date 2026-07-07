import L1Threshold.CollapseEdgeCertificate
import L1Threshold.CollapseEdgeOriginSummary

namespace L1Threshold

/-!
# W3 collapse-edge compact packet gate

This module is the small reviewer-facing aggregate for the compact
collapse-edge PR packet. It combines:

* the finite graph checker in `CollapseEdgeCertificate`; and
* the compact origin-audit metadata/count checker in
  `CollapseEdgeOriginSummary`.

It still does not replay the omitted per-edge `GF(137)` affine arithmetic.
-/

namespace CollapseEdgeCompactPacket

set_option maxRecDepth 1000000
set_option maxHeartbeats 2000000

theorem compactPacketOK :
    CollapseEdgeCertificate.checkAllCases = true
      ∧ CollapseEdgeOriginSummary.allCasesOK = true
      ∧ CollapseEdgeOriginSummary.edgeRulesAudited = 6528
      ∧ CollapseEdgeOriginSummary.mismatchCount = 0
      ∧ CollapseEdgeCertificate.allCases.map CollapseEdgeCertificate.alternateContribution =
          [1, 1, 1, 1, 1, 1] := by
  decide

theorem compactPacketNoGraphOrSummaryMismatches :
    CollapseEdgeCertificate.checkAllCases = true
      ∧ CollapseEdgeOriginSummary.allCasesOK = true := by
  decide

#print axioms compactPacketOK
#print axioms compactPacketNoGraphOrSummaryMismatches

end CollapseEdgeCompactPacket
end L1Threshold
