#!/usr/bin/env python3
"""Verify the compact W3 collapse-edge PR packet.

This verifier intentionally checks only the compact summary shipped in this PR.
The full raw edge-rule certificate and the arithmetic-origin generator remain
outside this compact packet; the Lean file is the self-contained finite graph
certificate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_ORIGIN = (
    "experimental/data/certificates/l1-residual-excess-classifier/"
    "w3_collapse_edge_origin_audit_combo012_sizes10_2_3.json"
)
DEFAULT_LEAN = "experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeCertificate.lean"
DEFAULT_ORIGIN_LEAN = "experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeOriginSummary.lean"
DEFAULT_STRUCTURAL_LEAN = "experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeStructuralLemma.lean"
DEFAULT_PACKET_LEAN = "experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeCompactPacket.lean"

EXPECTED_SOURCE_SHA256 = "1aab9da15bf074232122898bd9958fe2f2240eacdbc138af5638851be99a889d"
EXPECTED_CASES = {
    ("LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v7", "affine_83_96", 67),
    ("LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v7", "affine_83_96", 103),
    ("LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v7", "affine_83_96", 111),
    ("LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v11", "affine_105_38", 17),
    ("LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v11", "affine_105_38", 20),
    ("LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v11", "affine_105_38", 121),
}


def check_origin(path: Path, issues: list[str]) -> dict:
    data = json.loads(path.read_text())
    if data.get("status") != "L1_W3_COLLAPSE_EDGE_ORIGIN_CERTIFIED":
        issues.append("unexpected origin status %r" % data.get("status"))
    if data.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        issues.append("unexpected raw source sha256")
    if int(data.get("case_count", -1)) != 6:
        issues.append("origin case_count is not 6")
    if int(data.get("edge_rules_audited", -1)) != 6528:
        issues.append("edge_rules_audited is not 6528")
    if int(data.get("mismatch_count", -1)) != 0:
        issues.append("origin mismatch_count is nonzero")
    if data.get("mismatches"):
        issues.append("origin mismatches list is nonempty")
    seen_cases = {
        (case.get("target_family_id"), case.get("quotient_member"), int(case.get("shift", -1)))
        for case in data.get("case_summaries", [])
    }
    if seen_cases != EXPECTED_CASES:
        issues.append("case identity set mismatch")
    for case in data.get("case_summaries", []):
        label = "%s/%s/%s" % (case.get("target_family_id"), case.get("quotient_member"), case.get("shift"))
        if int(case.get("edge_rules_audited", -1)) != 1088:
            issues.append("%s: edge_rules_audited is not 1088" % label)
        if int(case.get("cosets_audited", -1)) != 8:
            issues.append("%s: cosets_audited is not 8" % label)
        if int(case.get("mismatch_count", -1)) != 0:
            issues.append("%s: mismatch_count is nonzero" % label)
        if case.get("stored_rule_counts_total") != {"always": 70, "at_shift": 976, "never": 42}:
            issues.append("%s: unexpected total edge-rule counts" % label)
        for coset in case.get("cosets", []):
            if int(coset.get("edge_rule_count", -1)) != 136:
                issues.append("%s/coset%s: edge_rule_count is not 136" % (label, coset.get("coset_w")))
            if int(coset.get("mismatch_count", -1)) != 0:
                issues.append("%s/coset%s: mismatch_count is nonzero" % (label, coset.get("coset_w")))
            if coset.get("stored_rule_counts") != coset.get("expected_rule_counts"):
                issues.append("%s/coset%s: stored/expected counts differ" % (label, coset.get("coset_w")))
    return data


def check_lean(path: Path, issues: list[str]) -> None:
    text = path.read_text()
    required = [
        "def checkCase",
        "def alternateContribution",
        "def collapseEdgeSurvivor",
        "theorem collapseEdgeAllCasesOk",
        "theorem collapseEdgeAllCaseContributionsLeOne",
        "theorem collapseEdgeShiftsAreTwoTriples",
        "theorem collapseEdgeAllActualSurvivorsSame",
        "theorem collapseEdgeAllAlternateContributionsExact",
        "no reconstruction of the underlying `GF(137)` arithmetic",
    ]
    for needle in required:
        if needle not in text:
            issues.append("Lean file missing %r" % needle)


def check_origin_lean(path: Path, issues: list[str]) -> None:
    text = path.read_text()
    required = [
        "theorem originSummaryAllCasesOK",
        "theorem originSummaryCaseCount",
        "theorem originSummaryEdgeRulesAudited",
        "theorem originSummaryNoMismatches",
        "theorem originSummaryTwoFamilies",
        "theorem originSummaryRepeatedCosetPattern",
    ]
    for needle in required:
        if needle not in text:
            issues.append("origin-summary Lean file missing %r" % needle)


def check_structural_lean(path: Path, issues: list[str]) -> None:
    text = path.read_text()
    required = [
        "def dangerousAntecedent",
        "def dangerousImpliesAlternateCollapse",
        "def uniqueCoset37SurvivorConclusion",
        "theorem allDangerousAntecedentsOK",
        "theorem dangerousPatternForcesAlternateCollapse",
        "theorem dangerousPatternForcesUniqueCoset37Survivor",
        "theorem dangerousPatternStructuralPacketOK",
        "finite graph certificate only",
    ]
    for needle in required:
        if needle not in text:
            issues.append("structural-lemma Lean file missing %r" % needle)


def check_packet_lean(path: Path, issues: list[str]) -> None:
    text = path.read_text()
    required = [
        "theorem compactPacketOK",
        "theorem compactPacketNoGraphOrSummaryMismatches",
        "theorem compactPacketStructuralLemmaOK",
        "CollapseEdgeCertificate.checkAllCases = true",
        "CollapseEdgeOriginSummary.edgeRulesAudited = 6528",
        "CollapseEdgeStructuralLemma.allStructuralCasesOK = true",
    ]
    for needle in required:
        if needle not in text:
            issues.append("compact-packet Lean file missing %r" % needle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", default=DEFAULT_ORIGIN)
    parser.add_argument("--lean", default=DEFAULT_LEAN)
    parser.add_argument("--origin-lean", default=DEFAULT_ORIGIN_LEAN)
    parser.add_argument("--structural-lean", default=DEFAULT_STRUCTURAL_LEAN)
    parser.add_argument("--packet-lean", default=DEFAULT_PACKET_LEAN)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    issues: list[str] = []
    origin = check_origin(Path(args.origin), issues)
    check_lean(Path(args.lean), issues)
    check_origin_lean(Path(args.origin_lean), issues)
    check_structural_lean(Path(args.structural_lean), issues)
    check_packet_lean(Path(args.packet_lean), issues)
    result = {
        "ok": not issues,
        "issues": issues,
        "status": origin.get("status"),
        "case_count": origin.get("case_count"),
        "edge_rules_audited": origin.get("edge_rules_audited"),
        "source_sha256": origin.get("source_sha256"),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("OK" if not issues else "FAIL")
        for issue in issues:
            print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
