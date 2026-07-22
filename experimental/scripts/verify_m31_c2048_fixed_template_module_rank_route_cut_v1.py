#!/usr/bin/env python3
"""Verify the M31 c=2048 fixed-template module-rank route cut.

The verifier exhausts the proved occupancy atlas, computes the exact
relaxed-Singleton threshold for every profile, seals the theorem interface,
and rejects semantic mutations.  It certifies a route dichotomy only: no
ledger atom is moved and module-rank-drop components remain unpaid.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Callable


SCHEMA_ID = "rs-mca-c2048-fixed-template-module-rank-route-cut-v1"
ARCHITECTURE_ID = "M31_C2048_FIXED_TEMPLATE_MODULE_RANK_ROUTE_CUT_V1"
STATUS = "PROVED_FIXED_TEMPLATE_MODULE_RANK_DICHOTOMY_GLOBAL_OWNERS_OPEN"
PARENT_TERMINAL = "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER"
NEW_TERMINAL = "UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP"

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
B_STAR = P**4 // 2**100
U_PAID = 3_730
BOUNDARY_TARGET = 9_216_781
C = 2_048
FIBERS = N // C
AGREEMENT_QUOTIENT = AGREEMENT // C
AGREEMENT_REMAINDER = AGREEMENT % C
ERROR_QUOTIENT = RADIUS // C
ERROR_REMAINDER = RADIUS % C
PROFILE_COUNT = 261_192

PARENT_PR = 1043
PARENT_HEAD = "0d93d366072a0ad3f66c73f9b5a6329a232b4293"
PARENT_PAYLOAD = "99febb07f517aac958e55eeba466e268a4ada793ef7960a189374603ea4a3ec9"
FIXED_PREFIX_SOURCE_PAYLOAD = "056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7"
MULTIPREFIX_SOURCE_PAYLOAD = "dacb9136f5818a5f86d9ca8987fbe4d361a57a70ebb490eac50dfc3822e062e4"

EXPECTED_HISTOGRAM = {
    1: 32_703, 2: 16_896, 3: 16_657, 4: 16_486, 5: 16_349,
    6: 16_227, 7: 16_092, 8: 15_957, 9: 15_833, 10: 15_705,
    11: 15_574, 12: 15_447, 13: 15_314, 14: 15_184,
    15: 13_886, 16: 6_170, 17: 712,
}
EXPECTED_EQUALITY = [
    [31, 365, 14], [91, 400, 12], [223, 239, 8], [285, 266, 6],
]

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_c2048_fixed_template_module_rank_route_cut_v1.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_c2048_fixed_template_module_rank_route_cut_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_c2048_fixed_template_module_rank_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/README.md"
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the fixed-template module-rank packet."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Exact all-profile threshold census and semantic mutation replay."),
    ("packet_sage", SAGE_PATH, None,
     "Independent determinant-valuation and rank-drop replay."),
    ("packet_note", NOTE_PATH, None,
     "Symbolic local dichotomy, conditional arithmetic, and nonclaims."),
    ("packet_readme", README_PATH, None,
     "Replay and dependency contract."),
    ("parent_1043_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json",
     "payload_sha256", "Sealed exact predecessor PR #1043."),
    ("occupancy_atlas_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json",
     "payload_sha256", "Exhaustive c=2048 occupancy profile authority."),
    ("fixed_prefix_source_manifest",
     ROOT / "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json",
     "payload_sha256", "Exact rank-one fixed-prefix source and C1 first-match authority."),
    ("multiprefix_source_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json",
     "payload_sha256", "All-profile fixed-template source-floor authority."),
    ("exact_quotient_remainder_source",
     ROOT / "experimental/rs_mca_thresholds.tex", None,
     "Free F[phi]-module decomposition and complete-support factorization."),
    ("source_adapter",
     ROOT / "experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md",
     None, "Target-field LIST chronology and exact arbitrary-word adapter."),
    ("active_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active nonnegative LIST chronology and row-sharp target."),
    ("chen_zhang_citation", ROOT / "open-proximity.tex", None,
     "Repository bibliographic pointer to Chen-Zhang STOC 2025; the separately pinned arXiv v3 PDF is the primary source."),
)


class VerificationError(RuntimeError):
    """Fail-closed certificate error."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (text + "\n").encode("ascii")


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON is forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN and infinity are forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, *, canonical: bool = False) -> Any:
    require(len(raw) <= 32 * 1024 * 1024, "JSON size bound")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    value = json.loads(
        text, object_pairs_hook=unique_object, parse_int=int,
        parse_float=reject_float, parse_constant=reject_constant,
    )
    if canonical:
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def strict_json_path(path: Path, *, canonical: bool = False) -> Any:
    require(path.is_file(), f"JSON path exists: {path}")
    return strict_json_bytes(path.read_bytes(), canonical=canonical)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"bound source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_sha256(result)
    return result


def internal_payload(path: Path, key: str | None) -> str | None:
    if key is None:
        return None
    value = strict_json_path(path, canonical=True)
    require(type(value) is dict, f"internal payload object: {path}")
    internal = value.get(key)
    require(type(internal) is str and len(internal) == 64,
            f"internal payload hash: {path}")
    return internal


def expected_source_bindings() -> list[dict[str, Any]]:
    result = []
    for role, path, internal_key, scope in SOURCE_SPECS:
        relative = path.relative_to(ROOT)
        require(PurePosixPath(relative.as_posix()).as_posix() == relative.as_posix(),
                f"canonical source path: {path}")
        internal = internal_payload(path, internal_key)
        if role == "parent_1043_manifest":
            require(internal == PARENT_PAYLOAD, "exact #1043 payload")
        if role == "fixed_prefix_source_manifest":
            require(internal == FIXED_PREFIX_SOURCE_PAYLOAD,
                    "exact fixed-prefix source payload")
        if role == "multiprefix_source_manifest":
            require(internal == MULTIPREFIX_SOURCE_PAYLOAD,
                    "exact multiprefix source payload")
        result.append({
            "binding_id": f"M31_C2048_MODULE_RANK::{role}",
            "path": relative.as_posix(),
            "role": role,
            "scope": scope,
            "sha256": sha256_path(path),
            "internal_payload_sha256": internal,
        })
    return result


def feasible_profiles() -> list[tuple[int, int]]:
    profiles: list[tuple[int, int]] = []
    for u in range(480):
        vmax = 136 if u == 0 else 544
        for v in range(vmax + 1):
            h = u + v + 1
            error_partial = ERROR_REMAINDER + C * u
            agreement_partial = AGREEMENT_REMAINDER + C * v
            require(error_partial + agreement_partial == C * h,
                    "profile color sum")
            require(h <= error_partial <= h * (C - 1),
                    "error partial feasibility")
            require(h <= agreement_partial <= h * (C - 1),
                    "agreement partial feasibility")
            profiles.append((u, v))
    require(len(profiles) == PROFILE_COUNT, "profile count")
    require(len(set(profiles)) == PROFILE_COUNT, "profile uniqueness")
    return profiles


def threshold_row(u: int, v: int) -> tuple[int, ...]:
    h = u + v + 1
    r = AGREEMENT_REMAINDER + C * v
    f = AGREEMENT_QUOTIENT - v
    available = FIBERS - h
    require(r + C * f == AGREEMENT, "agreement decomposition")
    require(available == 1023 - u - v, "available labels")
    require(0 <= f <= available, "support feasibility")
    if v >= 512:
        require(r >= K, "fixed-template uniqueness gate")
        degree = -1
        dimension = K - r
        threshold = 1
        slack = 0
        equality = 0
    else:
        degree = 511 - v
        dimension = K - r
        require(dimension == C * degree + 137, "free-module dimension")
        require(available - degree == 512 - u >= 33,
                "quotient evaluation injectivity")
        threshold = 0
        slack = 0
        equality = 0
        for candidate in range(1, C + 1):
            left = (candidate + 1) * f * (C + 1 - candidate)
            right = available * (C + 1 - candidate) + candidate * dimension
            if left >= right:
                threshold = candidate
                slack = left - right
                equality = int(left == right)
                break
        require(1 <= threshold <= C, "threshold exists")
        require(degree >= 0 and dimension > 0, "positive message space")
        require(dimension - 1 - degree * (C + 1 - threshold)
                == 136 + degree * (threshold - 1),
                "strong-design comparison identity")
        require(136 + degree * (threshold - 1) >= 0,
                "strong-design comparison")
    return (u, v, h, r, f, available, degree, dimension,
            threshold, slack, equality)


def profile_census() -> dict[str, Any]:
    digest = hashlib.sha256()
    histogram: Counter[int] = Counter()
    equality_profiles: list[list[int]] = []
    total = 0
    source_violations: list[tuple[int, int, int, int]] = []
    rows = []
    for u, v in feasible_profiles():
        row = threshold_row(u, v)
        rows.append(row)
        digest.update((",".join(str(value) for value in row) + "\n").encode("ascii"))
        threshold = row[8]
        histogram[threshold] += 1
        total += threshold
        if row[10]:
            equality_profiles.append([u, v, threshold])
        f = row[4]
        available = row[5]
        prefix_depth = min(32, f)
        source_floor = (math.comb(available, f) + P**prefix_depth - 1) // P**prefix_depth
        if source_floor > threshold:
            source_violations.append((u, v, threshold, source_floor))

    require(dict(sorted(histogram.items())) == EXPECTED_HISTOGRAM,
            "threshold histogram")
    require(total == 1_988_814, "threshold sum")
    require(max(histogram) == 17, "maximum threshold")
    require(equality_profiles == EXPECTED_EQUALITY, "equality profiles")
    require(sum(histogram.values()) == PROFILE_COUNT, "histogram total")
    require(BOUNDARY_TARGET - total == 7_227_967,
            "conditional boundary-target margin")
    require(U_PAID + total == 1_992_544, "conditional low-plus-profile total")
    require(B_STAR - U_PAID - total == 14_784_671,
            "conditional full-budget margin")
    require(len(source_violations) == 193, "source violation count")
    require(Counter(row[2] for row in source_violations) == Counter({17: 176, 16: 17}),
            "source violation threshold histogram")
    require(max(source_violations, key=lambda row: row[3])
            == (0, 0, 17, 6_796_405), "largest rank-one source")
    require(next(row for row in source_violations if row[:2] == (1, 1))
            == (1, 1, 17, 1_693_898), "profile (1,1) rank-one source")
    return {
        "profile_count": len(rows),
        "rows_sha256": digest.hexdigest(),
        "threshold_histogram": {str(key): histogram[key]
                                for key in sorted(histogram)},
        "threshold_maximum": max(histogram),
        "threshold_sum": total,
        "equality_inclusive_profiles": equality_profiles,
        "equality_inclusive_profile_count": len(equality_profiles),
        "boundary_target_margin_if_globally_paid": BOUNDARY_TARGET - total,
        "U_paid_plus_threshold_sum": U_PAID + total,
        "B_star_margin_if_globally_paid": B_STAR - U_PAID - total,
        "proved_fixed_prefix_source_exceeds_threshold_profiles": len(source_violations),
        "source_violation_threshold_histogram": {"16": 17, "17": 176},
        "largest_rank_one_source": {
            "profile": [0, 0], "conditional_threshold": 17,
            "proved_source_floor": 6_796_405,
        },
        "largest_bideep_rank_one_source": {
            "profile": [1, 1], "conditional_threshold": 17,
            "proved_source_floor": 1_693_898,
        },
    }


def core_payload() -> dict[str, Any]:
    census = profile_census()
    require(P == 2_147_483_647, "Mersenne prime")
    require(N == 2_097_152 and K == 1_048_576, "deployed dimensions")
    require(B_STAR == 16_777_215, "LIST budget")
    require((AGREEMENT_QUOTIENT, AGREEMENT_REMAINDER) == (544, 1911),
            "agreement quotient remainder")
    require((ERROR_QUOTIENT, ERROR_REMAINDER) == (479, 137),
            "error quotient remainder")
    return {
        "schema": SCHEMA_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "deployed_parameters": {
            "p": P, "target_field_size": str(P**4), "n": N, "K": K,
            "agreement": AGREEMENT, "radius": RADIUS, "B_star": B_STAR,
            "U_paid": U_PAID, "boundary_target": BOUNDARY_TARGET,
            "fold_degree": C, "quotient_labels": FIBERS,
            "agreement_quotient": AGREEMENT_QUOTIENT,
            "agreement_remainder": AGREEMENT_REMAINDER,
        },
        "fixed_template_module": {
            "profile_coordinates": {
                "partial_label_count": "h=u+v+1",
                "partial_agreement_size": "r=1911+2048*v",
                "full_agreement_labels": "f=544-v",
                "available_quotient_labels": "M=1023-u-v",
            },
            "v_at_most_511_high_component_count": 137,
            "v_at_most_511_high_component_degree": "D=511-v",
            "v_at_most_511_low_component_count": 1911,
            "v_at_most_511_low_component_degree": "D-1=510-v",
            "message_dimension": "d=2048*D+137=1046665-2048*v",
            "evaluation_injectivity_margin": "M-D=512-u>=33",
            "v_at_least_512_fixed_template_cap": 1,
        },
        "determinant_valuation_lemma": {
            "module_regular_condition": "rank_F(T)(A_W)=ell",
            "selected_minor_nonzero": True,
            "minor_degree_upper": "ell*D",
            "point_nullity_upper": "ord_(T-b)(Delta)",
            "summed_intersection_upper": "sum_b dim_F(W intersect H_b)<=ell*D",
            "determinantal_divisor_degree_upper": "ell*(D-1)+min(ell,137)",
            "chen_design_comparison": "ell*D<=ell*(d-1)/(2049-ell)",
            "comparison_remainder": "136+D*(ell-1)>=0",
            "field_generic": True,
        },
        "localized_dichotomy": {
            "threshold_name": "Lambda_SD(u,v)",
            "threshold_definition": "least L in [1,2048] with (L+1)*f*(2049-L)>=M*(2049-L)+L*d",
            "threshold_equality_is_included": True,
            "oversized_family_size": "at least Lambda_SD(u,v)+1",
            "minimal_bad_subfamily_size": "2<=m<=Lambda_SD(u,v)+1",
            "difference_span_dimension": "1<=ell<=m-1",
            "conclusion": "rank_F(T)(A_W)<ell",
            "rank_drop_is_payment": False,
            "rank_drop_implies_named_quotient_owner": False,
            "known_fixed_prefix_sources_have_module_rank_at_most": 1,
        },
        "profile_census": census,
        "imported_combinatorics": {
            "source": "Chen-Zhang arXiv:2408.15925 v3 Appendix B",
            "primary_pdf_sha256": "1d4a4859229351d1c345653e5d7eb63682f855c0b080b947d40fe1ecaf88c56a",
            "primary_pdf_pages": 31,
            "primary_pdf_version_line": "arXiv:2408.15925v3 [cs.IT] 14 Apr 2025",
            "used_results": ["Theorem B.3", "Lemma B.4", "Theorem 2.15 hyperedge-loss bound"],
            "folded_wronskian_used": False,
            "multiplicative_generator_used": False,
            "FRS_orbit_transfer_claimed": False,
        },
        "chronology": {
            "parent_terminal": PARENT_TERMINAL,
            "nested_diagnostic_subterminal": NEW_TERMINAL,
            "global_terminal_unchanged": True,
            "active_partition_unchanged": True,
            "full_module_rank_stratum_reduced": True,
            "module_rank_drop_owner_paid": False,
            "varying_template_aggregation_paid": False,
            "conditional_threshold_sum_is_ledger_charge": False,
            "owner_paid": False,
        },
        "external_dependencies": {
            "parent_pr": PARENT_PR,
            "parent_head": PARENT_HEAD,
            "parent_payload_sha256": PARENT_PAYLOAD,
        },
        "scope": {
            "object": "LIST", "row": "Mersenne-31 list at 2^-100",
            "workboard_item": "M1",
            "unit": "DISTINCT_EXACT_BOUNDARY_CODEWORDS_PER_FIXED_TEMPLATE",
            "impact": "FULL_MODULE_RANK_ROUTE_CUT_AND_CONDITIONAL_PROFILE_THRESHOLDS",
            "ledger_movement": 0, "deployed_row_closed": False,
            "stable_paper_modified": False, "lean_used": False,
        },
        "nonclaims": {
            "global_profile_cap_proved": False,
            "complete_exact_boundary_paid": False,
            "boundary_target_paid": False,
            "module_rank_drop_classified": False,
            "varying_templates_aggregated": False,
            "high_interior_paid": False,
            "U_Q_paid": False, "U_list_int_paid": False,
            "U_ext_paid": False, "U_new_paid": False,
            "Chen_Zhang_FRS_theorem_transferred_directly": False,
            "official_endpoint_or_score_changed": False,
        },
    }


def build_manifest() -> dict[str, Any]:
    payload = core_payload()
    payload["source_bindings"] = expected_source_bindings()
    return seal(payload)


def source_binding_schema() -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": ["binding_id", "internal_payload_sha256", "path",
                     "role", "scope", "sha256"],
        "properties": {
            "binding_id": {"type": "string", "minLength": 1},
            "internal_payload_sha256": {
                "type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
            "path": {"type": "string", "minLength": 1},
            "role": {"type": "string", "minLength": 1},
            "scope": {"type": "string", "minLength": 1},
            "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
    }


def build_schema() -> dict[str, Any]:
    core = core_payload()
    keys = sorted([*core, "payload_sha256", "source_bindings"])
    properties: dict[str, Any] = {
        key: {"const": value} for key, value in core.items()
    }
    properties["payload_sha256"] = {
        "type": "string", "pattern": "^[0-9a-f]{64}$"}
    properties["source_bindings"] = {
        "type": "array", "minItems": len(SOURCE_SPECS),
        "maxItems": len(SOURCE_SPECS), "uniqueItems": True,
        "items": {"$ref": "#/$defs/sourceBinding"},
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "M31 fixed-template module-rank route-cut certificate",
        "type": "object", "additionalProperties": False,
        "required": keys, "properties": properties,
        "$defs": {"sourceBinding": source_binding_schema()},
    }


def validate_schema(schema: Any, payload: dict[str, Any]) -> None:
    require(type(schema) is dict, "schema object")
    require(schema == build_schema(), "schema exact replay")
    require(set(schema["required"]) == set(payload), "schema root keys")
    require(set(schema["properties"]) == set(payload), "schema properties")


def verify_payload(candidate: dict[str, Any], *, expected: dict[str, Any]) -> None:
    require(type(candidate) is dict, "manifest object")
    require(type(candidate.get("payload_sha256")) is str, "payload hash type")
    require(candidate.get("payload_sha256") == payload_sha256(candidate),
            "payload hash")
    bindings = candidate.get("source_bindings")
    require(type(bindings) is list and len(bindings) == len(SOURCE_SPECS),
            "source binding count")
    ids = [item.get("binding_id") for item in bindings if type(item) is dict]
    require(len(ids) == len(bindings) and len(set(ids)) == len(ids),
            "source binding IDs unique")
    require(candidate == expected, "manifest exact replay")


def write_artifacts() -> None:
    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_PATH.write_bytes(canonical_json(build_schema()))
    MANIFEST_PATH.write_bytes(canonical_json(build_manifest()))


def set_path(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def mutate(payload: dict[str, Any]) -> None:
        target: Any = payload
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    return mutate


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("threshold sum", set_path(("profile_census", "threshold_sum"), 1_988_815)),
        ("maximum threshold", set_path(("profile_census", "threshold_maximum"), 18)),
        ("equality convention", set_path(("localized_dichotomy", "threshold_equality_is_included"), False)),
        ("equality profile", set_path(("profile_census", "equality_inclusive_profiles", 0, 0), 30)),
        ("histogram", set_path(("profile_census", "threshold_histogram", "17"), 713)),
        ("source violation count", set_path(("profile_census", "proved_fixed_prefix_source_exceeds_threshold_profiles"), 192)),
        ("rank-one source floor", set_path(("profile_census", "largest_rank_one_source", "proved_source_floor"), 6_796_404)),
        ("bideep source floor", set_path(("profile_census", "largest_bideep_rank_one_source", "proved_source_floor"), 1_693_897)),
        ("boundary margin", set_path(("profile_census", "boundary_target_margin_if_globally_paid"), 7_227_966)),
        ("budget margin", set_path(("profile_census", "B_star_margin_if_globally_paid"), 14_784_670)),
        ("minor degree", set_path(("determinant_valuation_lemma", "minor_degree_upper"), "(ell-1)*D")),
        ("determinantal divisor", set_path(("determinant_valuation_lemma", "determinantal_divisor_degree_upper"), "ell*D")),
        ("rank hypothesis", set_path(("determinant_valuation_lemma", "module_regular_condition"), "rank_F(T)(A_W)>=ell-1")),
        ("field genericity", set_path(("determinant_valuation_lemma", "field_generic"), False)),
        ("rank-drop conclusion", set_path(("localized_dichotomy", "conclusion"), "rank_F(T)(A_W)<=ell")),
        ("rank drop payment", set_path(("localized_dichotomy", "rank_drop_is_payment"), True)),
        ("FRS import", set_path(("imported_combinatorics", "folded_wronskian_used"), True)),
        ("primary PDF hash", set_path(("imported_combinatorics", "primary_pdf_sha256"), "0" * 64)),
        ("generator import", set_path(("imported_combinatorics", "multiplicative_generator_used"), True)),
        ("global cap", set_path(("nonclaims", "global_profile_cap_proved"), True)),
        ("ledger movement", set_path(("scope", "ledger_movement"), 1)),
        ("row closure", set_path(("scope", "deployed_row_closed"), True)),
        ("parent head", set_path(("external_dependencies", "parent_head"), "0" * 40)),
        ("parent payload", set_path(("external_dependencies", "parent_payload_sha256"), "0" * 64)),
        ("nested subterminal", set_path(("chronology", "nested_diagnostic_subterminal"), "PAID")),
        ("global terminal", set_path(("chronology", "global_terminal_unchanged"), False)),
        ("owner paid", set_path(("chronology", "owner_paid"), True)),
        ("varying templates", set_path(("chronology", "varying_template_aggregation_paid"), True)),
    ]


def check() -> None:
    expected = build_manifest()
    manifest = strict_json_path(MANIFEST_PATH, canonical=True)
    schema = strict_json_path(SCHEMA_PATH, canonical=True)
    verify_payload(manifest, expected=expected)
    validate_schema(schema, manifest)
    print(
        "PASS: M31 c=2048 fixed-template module-rank route cut; "
        f"profiles={PROFILE_COUNT}, threshold_sum={expected['profile_census']['threshold_sum']}, "
        f"max={expected['profile_census']['threshold_maximum']}, checks={CHECKS}"
    )


def tamper_selftest() -> None:
    expected = build_manifest()
    rejected = 0
    for label, mutate in mutation_cases():
        forged = copy.deepcopy(expected)
        mutate(forged)
        forged = seal(forged)
        try:
            verify_payload(forged, expected=expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"semantic mutation accepted: {label}")
    malformed = [
        b'{"a":1,"a":2}\n', b'{"x":1.0}\n', b'{"x":NaN}\n',
        b'{"x":"\xc3\xa9"}\n', b'{"x":1}',
    ]
    for raw in malformed:
        try:
            strict_json_bytes(raw, canonical=True)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("malformed JSON mutation accepted")
    total = len(mutation_cases()) + len(malformed)
    require(rejected == total, "all mutations rejected")
    print(f"PASS: rejected {rejected}/{total} mutations; checks={CHECKS}")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.write:
        write_artifacts()
        check()
    elif args.tamper_selftest:
        tamper_selftest()
    else:
        check()


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
