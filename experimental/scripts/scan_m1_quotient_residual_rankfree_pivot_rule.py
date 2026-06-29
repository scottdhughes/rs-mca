#!/usr/bin/env python3
"""Build the M1 quotient-residual rank-free pivot-rule audit JSON."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import zlib
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")
OUTPUT_DATA = Path("experimental/data/m1_quotient_residual_rankfree_pivot_rule.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
TARGET_BITS = 128
FIELD_DENOMINATOR = P**FIELD_DEGREE
PATTERN_CLASS = "quotient_residual_rref_pivot"

EXPECTED_RULES = [
    "compressed_variable_block_order",
    "fiber_coordinate_order",
    "incidence_greedy_matching_v1",
    "pair_boundary_pressure_asc",
    "pair_boundary_pressure_desc",
    "pair_label_coordinate_order",
    "quotient_full_fiber_first",
    "quotient_residual_balanced_order",
    "residual_partial_fiber_first",
    "row_type_pair_order",
    "rref_profile_type_pair_quota_mimic",
]

REQUIRED_NONCLAIMS = [
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
]

RANKFREE_RULE_RESULTS_ZLIB_B64 = """
eNrtnd9vHTeux9/7VxR57oNIUZS0b3vb7EWA/QGku/dlsTBEkdwe1LGzttNu9+L+75dj55ftkzpJ0/a4FtKgOTozGmnOlxSp+Yz0
988+//x/4+/nnz+a40R3Oi7saKePfvf5o3Eyvzk9Ozqz4/Fv0yM5fXGi4+yHI0iPvnh5xumz52d2fh7f6u6ZnZzvTk/Oj+SHo+93
FydRHrVc1R3HQnzI+MWrj3j9Y77+ka5/LNc/8uXHy0//97Ilahd29mx3Mk4ujk5OT/5jZ6dx0MXZC3t5wLNxcbb799H5N+O5xTd/
f1lXblhe1Qv9qs5/vDpldxLd/2acf7PdDZsIPrNgdR8lz+bCVAYxchXnIR3jXxVLma4slJVqmqOITTEQenSt1rNx8u2Rvzg+vt7K
kyjZXfwQhellyfPdd6cXR/P0+Px1S5o3pE4kqWRAalg5p1IUtXcabciAuC7UXCC7UJuJlD1phtJnIXt0rernY3cW9b84ubj+c32x
/UJMX7wpuPEbwRd0s6DcLNjzS7256psewajo0YE6WYVqwVRHaz4t7udsY5p6742ztvhSJ3VIs3TInTIP63K9R2en3x9d/PDc9vTq
Xy9OL3YWGtlu/ZHvxM62w+MQqP11u0PSO30xjo/ih3o+zi5248axeU+P4qs3HRJA4JS8E2jpKW67ozbp0RHi6lXVpptY1zRSSVM0
c82Jk5bC3F53aJPJdsGObxX4mdnR2YtjOxoXF/bs+WUXXwn6VVdfK+2NNfg4Prcvbn7/8hJvfumtR5smXinvxj18Sx2vDOatm/Ez
a/adCtJO2Bwyt9GNWmgDW025F+9xg232+KblqGimqkxh9mlqqK5DHDBee7R3/Z6fsvnbL7fV+Zbz/G6c7YbEDyrHp/PbkJ3a2c1T
jubxuPSoj756/NfHT//05M9Pvv7rky+PvvzLn/7ryZ9//9e/PH3y+z8ePf3bHx/fOvPFuZ2HgO1Yj+JCF988s4vd3COIczu2eRHt
uVLG+e4/9rb4ro65GBcvLpvx9ZM///ff/vj7p0fRlL88ffuiP3q9z27o5WMF2z5CsMhfXC/cPBjSjcKy78jNk70ZKq6GsEuPiDfK
aN+BW5V0o4xvnZwvT4YbZWXPcbfPpSvne6NsT6vLy8JDsdxaoYX3y3XmcJATUPOlBdPItbTKhJh7jSIaNnKKsXe6FDBP6E7J7rDc
jKlhH70iu1IMGiCDdLTwsz1NdwTxLCnG7WbNWFLrEqP3DI+RvI6+z3KvxoJ5GnYaEUfES8tg1whzgCPM7mTu1E6mHf0zQgb94SiC
4PnN7uSfR9/BUutS62Gp9fImv04yL0OjF2cR457PpdWl1XuhVbUl1iXWgxTr8RA7XjHrB4q184eLNeOefPJWId8uxBsTam/lcDcK
y9sTawdgFAlhoG6p2ZjWjbVKEweILKpXKtiSRmo1miTK3g3BGkeS1acVrGPWO4xieCtzSm9VKiv1ZhjG1NyzCtgcrc82hpKM0VBN
RDjPVEatvXS9Xv0ro9g3E+jRp4tlEj9uEoDpIxw43JD/NnMCac9sTIY91nPrdL59+tVsDOQ9JnXryMs66575mBun532nX83I9D0z
MjeaeTUlA2WPPd84srzs0KHYs8zNmN1SM6fqxXSzaoKU3frI5lxqdsCwLsbshS8nanLPVoflfJc9SwydFoOjWJ9pZm9JcFZuCgzh
KLrKpNQQmHioSKU2bGae7tWqKf6oPb+evJdxPCL31TXSLbNeZn1Pzfq1NV9/DrdG6pVp/cRMS0dPSMZpa7x5dpe4AjUpOp1nWEWz
4qk2MKHCFHHkoJokGeTisvfBwOsnz5d3e4077zPuFPhwlTLtGXdupVj0gcnYoQj/E9EQ7xJ+kloTljFqkXDuNXXQ5hlFXa1M8tHC
KmZJiGgCrdYyS56QDCmpp73CPzM/en526rvQ6RsL2IKyETJ8tvuRabGnTx//IcT3pzCC+yP7a6DQmT0bu5PtuYr968W4eAVBbbfg
NlKDpdxgaq6X0K2ScquEb5TgrXrwVj14qx68VU++dVa+dVa+dRbdOoZuHfPqqXO5Rs6cn744m3bk49nueIOeHl18f3p0bN/Z8dGt
eP7R9XO+tRsnbHf7+925Henuu935TnYbSPW7390Nsb2s8PmY39rFe9T5+rzXWvry8dO/PvnDk8dfHV1q+avHT5/8z+OvHn32sqMf
itfBQ8TrcrKKrYggbdRUb64jXFI4Ouy9SoVwVkkxIlOYMgYbdq5l+Jw6m1dfeN1h43UtvT9eh3fhddUm+DApVcy9gBGD8ADos5J1
Slsm0hh70SoR4EmKPCaxc8SKWb0uvG7hdSsu/3HBfsSTj/eOyvdOBr3PA5L8zqcme6aCbh24p8qriIf2zATRnpmgvGciiPbMA9Ge
aSA6FFsuVGaMpMQ+M3LUKWgR8IenHwMB6+b0ewwXEJlwm56FZhj/4FobS9K7bNlmkZFRRWcSb62GLxhAjTBDCp+QGg938Fqyay+p
IdfIu7c/4dYZFnC35n8WcLfUutS6gLul1aXVBdwtsS7gbon1A4C7/N7A3d588kdyx0MxCif0ZDhoYI3/EiunSjP3niJxc5RRe/IR
l1OFWbBPzXkOysWbAtAdRtGjJW2bMeRSwqoqEItKTQJkhOYVlGoTbNFF5TkGR4pXaHsNepjsz+EWcPfRZA5+hAPnfWQO7ZuL2Tfx
gnshnLQPwun7IJx91nOLt6HbTbqaermF6/DtI2nfkbSP9nlJ4eSDGdCIKYwEw5QypJ5yYlPDJo2r5Z4JJmOXNihNmMTJRpOuzfoA
tXmX7TKjZ0eWMqflWZoPz5w6tdazQo3OmZFvfVPZFjTonIGrxwWzJ/AF1y0TXib8mzPhBdKtDOrnyaAiSFTCqgmqZJodJZGI8thC
xu29esodKiVOOLixuk0wDkFjnjONsUC6TwTSpQXS/aIgnddJozRL0htyNi5WRXXLstRcJGrSGZoPYyqEkYRZGawDsACbT18g3QLp
fgMgHfzaIN08ffbs9CR0+u9XGNGrWOfjV6qDayQdXAPp4BpHB9cwOrhG0cEnh+j4RxC6svFP01mU1Dl8aPZwoQlSneEtt2XrtsXr
oAmHE7U4tOWuAj5rl5QcPx1CR5Z6SwjTewz2hXs319RQWsoNwCbXcLLDSbKNHNFsi/hZ5px5io2ZPwChwxs+AG54ALhh/3DD+uFO
ek66m0mNu9QapTJztY51hLPnVmZNtZBXqeJQ4qOCZO0NNDqdutlrXvon0XPvzc6Vu9A5z52lJhcurbGXGMEMMbKV0IVq5BoiBZJG
7hF/IUasPBVSjMMeXYrB6wY6xz83OPcxbwe8b/zxiWT67lnaGPYhWYsAJlMm3RDFCIYLRuQ7lEbv6JhTY4BWZ+8aIQmmhFhbHhEr
3xF/fMrm3zdqjg8xBC8fsSLdnXQcXndrb0+n7JtNORTtw1TGiHQj4LYYhzQNHDrQI/1MoEPn5M4YyWeMT2JT1WGGT/ItcQTXu6ZI
JnF4Wq9hPzOaOCNl9ZRN24hRzkSRxvbKlrYqcZ1KnlokA5AbzZaolHtImR2k5Jd7/kXd870AzJZQl1DvAVu2ZLpkeh+wsqXTpdP7
QJQdpE7T0uk71wGY0jOyqg2YKXpQnb20NnujgTRLkUiY6ugbWRYdS6lvj+861FnbLOl+Ql4HqVJcKn2nN4VRe1MtUk1SHanLKFqb
YwuZlu59zFSBnVPKQFKwkfYpoWaAAuNe40xLrEus9wLcWWP//RIqVNuWaCPuiOotWijNzagOAqhgXdlVNQuxJPI+86hJu0kViF7V
+8bsHKQ+6ac/Lsh7Xpz/kBfsD+ZxwSd6yPouvRcZarjt16azyazQotbSMedcUq8T3L1GqMuDmqRBGCGxYg8PTlHW8X6hOrxAnQcM
6rwPDnOAqA48JFRnlg20FQxvWmJwb1KLZPbwNEYejmdWEg3v1ypMRMndWiot/i/c1TIvVOcBoDppbs+vOcLAHh0xQYARgV8yMqXE
wuqaJ0tjjWCQSvyUqUpXMKKW6RdHdVZiuFCd33DsDZ8s9sa9+zzSIcXjmqL+wpXF09DG3ZuGe8HWUchLadtuGxChdMbt7Y8iyB1y
ZXKibR75rrfum6bsbjhzGVT7Nr08YnDb3l/yHgmoOeRUKLLSbdTDqg2j8ZMSdKC68J01l7fwnSXUJdSF7yyZLpkufGfpdOE76xHe
Q9JpSV3ZhvYJFQYrDLXei84E0fjaI1NKGjlaGqNMS6P0aIlSMkePS+rCd5Y3/flV2lNmihaOFH+ihZYHV600Q7ZCUlrpajqV2ohe
FIl+1aSh021Nf3Jb+M4S670W68J3FmK+8J31tu/Cd34CvlN5luFjdNCkvq2ggybY2eMq4YObAdus3uMaY2JmE4JOLUPBUcPUFr6z
8J3fAL7zq6+08/zFybx4cRaCtd0/v7l42cCHtcpOK7m5FuncYaIkrJKzNoy4EI00l3BvbQo5Z0rhVHv41F6Lz1mZaNBCdw4V3Snv
v0PdXehOU44fB5Wyp5miG5R6ptZrl5myCERPdNsPaRK4D6vCIJDAkHKTURa6s9CdFXfv12r+MK3+5Bh7H6azbzWeQ7GHOG5IG8qa
YsxJMEquqjCmD/LwlJECAkKt3T2sIoW72daFgzTCRW2rCN9hD9L64M5ZZ4mWzjiFx6wDAFOMcBZWVlLK2TvVTopNevNweDyrhW9f
K++sebyF7iyhLqEudGfJdMl0oTtLpwvdWTq9TNMORqc5AfSyLRqaXBu0CX3IKAXKtkHGiPRpNEAqtecBbZukSpNhm9wZU5KPu95+
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
96MQZw==
"""


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def exact_rows() -> list[dict[str, Any]]:
    raw = base64.b64decode("".join(RANKFREE_RULE_RESULTS_ZLIB_B64.split()))
    return json.loads(zlib.decompress(raw).decode())


def source_profiles(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["source_key"]: row
        for row in source["matrix_profiles"]
        if row["classification"] == PATTERN_CLASS
    }


def aggregate_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        value = str(item[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def add_counts(dst: dict[str, int], src: dict[str, int]) -> None:
    for key, value in src.items():
        dst[key] = dst.get(key, 0) + int(value)


def aggregate_pairs(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        add_counts(out, row["pivot_pair_counts"])
    return dict(sorted(out.items()))


def aggregate_rule_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_rule = {
        rule: {"tested": 0, "success": 0, "failed": 0}
        for rule in EXPECTED_RULES
    }
    by_class: dict[str, dict[str, int]] = {}
    total = 0
    success = 0
    deterministic_success = 0
    rref_mimic_success = 0
    matrices_with_success = set()
    large_matrix_success = 0
    best_failed = [-1, 1]
    best_failed_detail = None
    for row in rows:
        ncols = row["matrix_shape"][1]
        for attempt in row["rankfree_rule_attempts"]:
            total += 1
            rule = attempt["rule"]
            rule_class = attempt["rule_class"]
            assert rule in by_rule
            by_rule[rule]["tested"] += 1
            by_class.setdefault(rule_class, {"tested": 0, "success": 0, "failed": 0})
            by_class[rule_class]["tested"] += 1
            if attempt["minor_nonzero"]:
                success += 1
                matrices_with_success.add(row["candidate_id"])
                by_rule[rule]["success"] += 1
                by_class[rule_class]["success"] += 1
                if rule_class == "DETERMINISTIC_COMBINATORIAL_RULE":
                    deterministic_success += 1
                elif rule_class == "RREF_MIMIC_RULE":
                    rref_mimic_success += 1
                if ncols > 64:
                    large_matrix_success += 1
            else:
                by_rule[rule]["failed"] += 1
                by_class[rule_class]["failed"] += 1
                if attempt["minor_rank"] * best_failed[1] > best_failed[0] * ncols:
                    best_failed = [attempt["minor_rank"], ncols]
                    best_failed_detail = {
                        "candidate_id": row["candidate_id"],
                        "rule": rule,
                        "minor_rank": attempt["minor_rank"],
                        "selected_minor_size": ncols,
                    }
    if deterministic_success:
        status = "PARTIAL_DETERMINISTIC_RULE_SUCCESS"
    elif rref_mimic_success:
        status = "RREF_MIMIC_PARTIAL_SUCCESS"
    else:
        status = "RREF_DERIVED_PATTERN_ONLY"
    return {
        "rules_tested": len(EXPECTED_RULES),
        "rule_names": EXPECTED_RULES,
        "rank_free_attempts": total,
        "rank_free_successes": success,
        "deterministic_rule_successes": deterministic_success,
        "rref_mimic_rule_successes": rref_mimic_success,
        "matrices_with_rank_free_success": sorted(matrices_with_success),
        "large_matrix_rank_free_successes": large_matrix_success,
        "rank_free_failures": total - success,
        "success_by_rule": dict(sorted(by_rule.items())),
        "success_by_rule_class": dict(sorted(by_class.items())),
        "best_failed_minor_rank_ratio": best_failed,
        "best_failed_minor": best_failed_detail,
        "status": status,
    }


def matrix_record(row: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    assert row["source_key"] == profile["source_key"]
    assert row["matrix_shape"] == profile["matrix_shape"]
    assert row["rank"] == profile["rank"]
    assert row["nullity"] == profile["nullity"] == 0
    assert row["pivot_pair_counts"] == profile["pivot_pattern"]["pair_pivot_counts"]
    matrix_cols = row["matrix_shape"][1]
    success_rules = [
        attempt["rule"]
        for attempt in row["rankfree_rule_attempts"]
        if attempt["minor_nonzero"]
    ]
    if success_rules:
        if any(
            attempt["minor_nonzero"]
            and attempt["rule_class"] == "DETERMINISTIC_COMBINATORIAL_RULE"
            for attempt in row["rankfree_rule_attempts"]
        ):
            best_status = "DETERMINISTIC_COMBINATORIAL_RULE"
        else:
            best_status = "RREF_MIMIC_RULE"
    else:
        best_status = "RREF_DERIVED_ONLY"
    return {
        "candidate_id": row["candidate_id"],
        "source_key": row["source_key"],
        "source_packet": row["source_packet"],
        "source_family": row["source_family"],
        "pattern_class": PATTERN_CLASS,
        "matrix_shape": row["matrix_shape"],
        "rank": row["rank"],
        "nullity": row["nullity"],
        "rref_certificate_status": "CERTIFIED",
        "rref_certificate": {
            "certificate_type": "RREF_PIVOT_MINOR",
            "minor_size": matrix_cols,
            "minor_rank_full": row["minor_rank_full"],
            "determinant_nonzero": row["determinant_nonzero"],
            "pivot_rows_hash": row["pivot_rows_hash"],
            "pivot_cols_hash": row["pivot_cols_hash"],
            "pivot_pairs_hash": row["pivot_pairs_hash"],
            "minor_hash": row["minor_hash"],
            "row_type_counts": row["pivot_row_type_counts"],
            "pair_pivot_counts": row["pivot_pair_counts"],
            "status": "CERTIFIED_FULL_RANK",
        },
        "rankfree_rules": row["rankfree_rule_attempts"],
        "rankfree_rule_successes": success_rules,
        "best_rule_status": best_status,
        "compressed_dimensions_by_witness": row["compressed_dimensions_by_witness"],
        "remaining_equations_by_pair": row["remaining_equations_by_pair"],
        "route_cut_status": "ROUTE_CUT_CERTIFIED_CANDIDATE",
    }


def build_result(source: dict[str, Any]) -> dict[str, Any]:
    assert threshold_floor() == 6
    profiles = source_profiles(source)
    rows = exact_rows()
    rows.sort(key=lambda item: item["source_key"])
    assert len(rows) == len(profiles) == 8
    matrices = [matrix_record(row, profiles[row["source_key"]]) for row in rows]
    rule_summary = aggregate_rule_summary(rows)
    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "denominator": "17^32",
        "field_denominator": str(FIELD_DENOMINATOR),
        "agreement": TARGET_AGREEMENT,
        "agreement_target": TARGET_AGREEMENT,
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "pattern_class": PATTERN_CLASS,
        "construction_mode": "quotient_residual_rankfree_pivot_rule",
        "source_profile": {
            "path": str(SOURCE_DATA),
            "record_hash": source["record_hash"],
            "source_matrices": source["profile_summary"]["source_matrices"],
            "quotient_residual_profiles": len(matrices),
            "status": source["global_status"]["status"],
        },
        "matrix_count": len(matrices),
        "source_family_counts": aggregate_by(matrices, "source_family"),
        "source_packet_counts": aggregate_by(matrices, "source_packet"),
        "aggregate_pair_pivot_counts": aggregate_pairs(rows),
        "rule_summary": rule_summary,
        "rref_derived_certificates_replayed": len(matrices),
        "rank_free_successes": rule_summary["rank_free_successes"],
        "matrices": matrices,
        "theorem_assessment": {
            "target_statement": (
                "For the quotient_residual_rref_pivot class, a metadata-only "
                "row schedule selects a full column-rank minor over GF(17^32)."
            ),
            "rankfree_rules_tested": EXPECTED_RULES,
            "rankfree_rule_attempts": rule_summary["rank_free_attempts"],
            "rankfree_rule_successes": rule_summary["rank_free_successes"],
            "deterministic_rule_successes": rule_summary[
                "deterministic_rule_successes"
            ],
            "rref_mimic_rule_successes": rule_summary["rref_mimic_rule_successes"],
            "deterministic_schedule_proved": False,
            "reason_not_proved": (
                "Only the RREF-profile mimic rule succeeds, and only on two "
                "small 6-column quotient-residual matrices. No deterministic "
                "metadata rule succeeds, and the 192-column anchor-relaxed "
                "matrices remain RREF-derived."
            ),
            "status": rule_summary["status"],
        },
        "interpretation": {
            "a327_certificate_found": False,
            "candidate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "quotient_residual_candidates_certified_full_rank": True,
            "rankfree_rule_found": rule_summary["rank_free_successes"] > 0,
            "deterministic_rankfree_rule_found": rule_summary[
                "deterministic_rule_successes"
            ]
            > 0,
            "rref_mimic_partial_success": rule_summary[
                "rref_mimic_rule_successes"
            ]
            > 0,
            "deterministic_pivot_schedule_theorem_proved": False,
            "status": "AUDIT",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_quotient_residual_rankfree_pivot_rule.sage",
            "checks_GF_17_32": True,
            "reconstructs_8_quotient_residual_matrices": True,
            "replays_rref_derived_pivot_certificates": True,
            "tests_rankfree_rule_minors": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": REQUIRED_NONCLAIMS,
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": rule_summary["status"],
        },
        "status": "M1_QUOTIENT_RESIDUAL_RANKFREE_PIVOT_RULE_AUDIT",
    }
    result["record_hash"] = hash_payload(
        {
            "source_profile": result["source_profile"],
            "rule_summary": result["rule_summary"],
            "matrices": result["matrices"],
            "theorem_assessment": result["theorem_assessment"],
            "interpretation": result["interpretation"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE_DATA, type=Path)
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_result(load_json(args.source))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output, result)
        print(f"WROTE {args.output}")
        print(f"quotient-residual matrices: {result['matrix_count']}")
        print(f"rank-free attempts: {result['rule_summary']['rank_free_attempts']}")
        print(f"rank-free successes: {result['rank_free_successes']}")
        print(
            "deterministic successes: "
            f"{result['rule_summary']['deterministic_rule_successes']}"
        )
        print(
            "RREF-mimic successes: "
            f"{result['rule_summary']['rref_mimic_rule_successes']}"
        )
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
