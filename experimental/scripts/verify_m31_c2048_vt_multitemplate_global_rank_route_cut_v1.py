#!/usr/bin/env python3
"""Verify the M31 c=2048 VT multitemplate global-rank route cut.

The packet proves a global locator-module/template-line stratification and an
exact pairwise escape criterion.  It deliberately certifies zero payment:
both the heavy fixed-template line and dispersed multitemplate line branches
remain unpaid.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable


SCHEMA_ID = "rs-mca-c2048-vt-multitemplate-global-rank-route-cut-v1"
ARCHITECTURE_ID = "M31_C2048_VT_MULTITEMPLATE_GLOBAL_RANK_ROUTE_CUT_V1"
STATUS = "PROVED_GLOBAL_STRATIFICATION_BOTH_BRANCHES_UNPAID"
DIAGNOSTIC = "UNPAID_VT_MULTITEMPLATE_GUARDED_LINE_INCIDENCE"
BOUNDARY_SUBTERMINAL = "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER"
GLOBAL_TERMINAL = "UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER"

P = 2**31 - 1
Q = P**4
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
R = N - AGREEMENT
W = K - R
C = 2_048
B_STAR = Q // 2**100
U_PAID = 3_730
MAX_LAMBDA = 17

PARENT_PR = 1045
PARENT_HEAD = "17883a3087b6c84ba72654cb847eeed1614e4b4b"
PARENT_PAYLOAD = "d0aa51bd3811ad5e93269f7174afc249fc2865715cb484e41cd233bcab775960"
MODULE_PARENT_PR = 1044
MODULE_PARENT_HEAD = "5b097b607ae60f7d46c730654eb04fa8a63c8595"
MODULE_PARENT_PAYLOAD = "c164f24810e0ed5015b3e538607e8867c7f634d5797de645c455447a08aaa303"
TEMPLATE_PARENT_PR = 1043
TEMPLATE_PARENT_HEAD = "0d93d366072a0ad3f66c73f9b5a6329a232b4293"
TEMPLATE_PARENT_PAYLOAD = "99febb07f517aac958e55eeba466e268a4ada793ef7960a189374603ea4a3ec9"
MULTIPREFIX_PAYLOAD = "dacb9136f5818a5f86d9ca8987fbe4d361a57a70ebb490eac50dfc3822e062e4"
FIXED_REMAINDER_PAYLOAD = "056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7"

ROOT = Path(__file__).resolve().parents[2]
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_c2048_vt_multitemplate_global_rank_route_cut.md"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_c2048_vt_multitemplate_global_rank_route_cut_v1.sage"
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_c2048_vt_multitemplate_global_rank_route_cut_v1.schema.json"
CERT_DIR = ROOT / "experimental/data/certificates/m31-c2048-vt-multitemplate-global-rank-route-cut-v1"
README_PATH = CERT_DIR / "README.md"
MANIFEST_PATH = CERT_DIR / "manifest.json"

SOURCE_SPECS = (
    ("packet_schema", SCHEMA_PATH, None,
     "Strict schema for the multitemplate global-rank route cut."),
    ("packet_verifier", VERIFIER_PATH, None,
     "Exact deployed arithmetic, load extremizers, source closure, and mutations."),
    ("packet_sage", SAGE_PATH, None,
     "Independent rank-one factorization and pairwise escape replay."),
    ("packet_note", NOTE_PATH, None,
     "Global locator module, template-line theorem, escape criterion, and route cut."),
    ("packet_readme", README_PATH, None,
     "Replay commands, dependency, and zero-payment scope."),
    ("parent_1045_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/manifest.json",
     "payload_sha256", "Exact guarded VT parent PR #1045."),
    ("parent_1045_note",
     ROOT / "experimental/notes/thresholds/m31_c2048_guarded_support_flat_separator.md",
     None, "Exact VT forward/converse and shifted-locator parent."),
    ("module_parent_1044_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json",
     "payload_sha256", "Exact fixed-template module-rank parent PR #1044."),
    ("module_parent_1044_note",
     ROOT / "experimental/notes/thresholds/m31_c2048_fixed_template_module_rank_route_cut.md",
     None, "Conditional thresholds and unpaid module-rank-drop theorem."),
    ("template_parent_1043_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json",
     "payload_sha256", "Exact fixed-template cap parent PR #1043."),
    ("template_parent_1043_note",
     ROOT / "experimental/notes/thresholds/m31_c2048_fixed_template_interleaved_quotient_route_cut.md",
     None, "Positional template blocks, cap formula, and two-template source."),
    ("multiprefix_source_manifest",
     ROOT / "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json",
     "payload_sha256", "Sealed fixed-multipartial H=1 source packet."),
    ("multiprefix_source_note",
     ROOT / "experimental/notes/thresholds/m31_c2048_multiprefix_30carrier_activation_route_cut.md",
     None, "Fixed-multipartial source formula and exact source floors."),
    ("fixed_remainder_source_manifest",
     ROOT / "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json",
     "payload_sha256", "Sealed fixed-remainder rank-one source packet."),
    ("fixed_remainder_source",
     ROOT / "experimental/notes/thresholds/m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut.md",
     None, "Realized 6796405-member rank-one locator-line source and scope guard."),
    ("active_ledger", ROOT / "experimental/grande_finale.tex", None,
     "Active nonnegative LIST chronology and unchanged atoms."),
    ("foundation", ROOT / "tex/cs25_cap_v13_2.tex", None,
     "Deployed field, domain, code, and exact-support conventions."),
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
        rendered = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (rendered + "\n").encode("ascii")


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, *, canonical: bool) -> Any:
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


def strict_json_path(path: Path, *, canonical: bool) -> Any:
    require(path.is_file(), f"JSON exists: {path}")
    return strict_json_bytes(path.read_bytes(), canonical=canonical)


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"bound source exists: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unsigned)).hexdigest()


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_sha256(result)
    return result


def internal_hash(path: Path, key: str | None) -> str | None:
    if key is None:
        return None
    value = strict_json_path(path, canonical=False)
    require(type(value) is dict, f"internal object: {path}")
    result = value.get(key)
    require(type(result) is str and len(result) == 64,
            f"internal hash: {path}")
    return result


def source_bindings() -> list[dict[str, Any]]:
    bindings = []
    for role, path, key, scope in SOURCE_SPECS:
        relative = path.relative_to(ROOT).as_posix()
        require(PurePosixPath(relative).as_posix() == relative,
                f"canonical source path: {path}")
        internal = internal_hash(path, key)
        if role == "parent_1045_manifest":
            require(internal == PARENT_PAYLOAD, "exact #1045 payload")
        if role == "module_parent_1044_manifest":
            require(internal == MODULE_PARENT_PAYLOAD, "exact #1044 payload")
        if role == "template_parent_1043_manifest":
            require(internal == TEMPLATE_PARENT_PAYLOAD, "exact #1043 payload")
        if role == "multiprefix_source_manifest":
            require(internal == MULTIPREFIX_PAYLOAD, "exact multiprefix payload")
        if role == "fixed_remainder_source_manifest":
            require(internal == FIXED_REMAINDER_PAYLOAD,
                    "exact fixed-remainder payload")
        bindings.append({
            "binding_id": f"M31_C2048_VT_MULTITEMPLATE::{role}",
            "internal_payload_sha256": internal,
            "path": relative,
            "role": role,
            "scope": scope,
            "sha256": sha256_path(path),
        })
    require(len({item["binding_id"] for item in bindings}) == len(bindings),
            "unique source binding ids")
    return bindings


def ceil_div(a: int, b: int) -> int:
    require(type(a) is int and type(b) is int and a >= 0 and b > 0,
            "ceil_div domain")
    return (a + b - 1) // b


def live_gates() -> list[dict[str, Any]]:
    values = (
        ("conditional_face_carrier_target", 9_216_781),
        ("post_U_paid_complete_boundary_target", B_STAR - U_PAID),
        ("full_forbidden_packet", B_STAR),
    )
    result = []
    for gate_id, u in values:
        m = u + 1
        result.append({
            "U": u,
            "gate_id": gate_id,
            "packet_size": m,
            "minimum_template_lines_no_heavy": ceil_div(m, MAX_LAMBDA),
            "target_field_converse_gate": Q > m * R,
            "guard_count": m * R,
        })
    return result


def deployed_arithmetic() -> dict[str, Any]:
    locator_high_rows = R % C + 1
    locator_low_rows = C - locator_high_rows
    difference_high_rows = R % C
    difference_low_rows = C - difference_high_rows
    difference_dimension = (
        difference_high_rows * (R // C + 1)
        + difference_low_rows * (R // C)
    )
    cap_00 = math.comb(1023, 512) // math.comb(544, 512)
    template_count_00 = 1024 * math.comb(2048, 137)
    return {
        "B_star": B_STAR,
        "K": K,
        "U_paid": U_PAID,
        "agreement": AGREEMENT,
        "fold_degree": C,
        "n": N,
        "p": P,
        "radius": R,
        "target_field_size": str(Q),
        "w": W,
        "radius_division": {"quotient": R // C, "remainder": R % C},
        "locator_degree_slice": {
            "degree_479_rows": locator_high_rows,
            "degree_478_rows": locator_low_rows,
            "ambient_free_module_rank_over_FT": C,
            "is_FT_submodule": False,
        },
        "difference_degree_slice": {
            "F_dimension": difference_dimension,
            "degree_479_rows": difference_high_rows,
            "degree_478_rows": difference_low_rows,
            "equals_radius": difference_dimension == R,
            "is_FT_submodule": False,
        },
        "profile_00": {
            "Lambda_SD": 17,
            "fixed_template_cap": str(cap_00),
            "fixed_template_cap_digits": len(str(cap_00)),
            "positional_template_lower": str(template_count_00),
            "positional_template_lower_digits": len(str(template_count_00)),
            "cap_exceeds_full_forbidden_packet": cap_00 >= B_STAR + 1,
            "templates_exceed_full_forbidden_packet": template_count_00 >= B_STAR + 1,
        },
    }


def source_coset_separation() -> dict[str, Any]:
    top_profiles = ((0, 0), (0, 1), (1, 0), (0, 2), (1, 1))
    rows = []
    for u, v in top_profiles:
        h = u + v + 1
        f = 544 - v
        available = 1024 - h
        candidates = math.comb(available, f)
        floor_32 = ceil_div(candidates, P**32)
        floor_33 = ceil_div(candidates, P**33)
        rows.append({
            "candidate_count": str(candidates),
            "floor_depth_32": floor_32,
            "floor_depth_33": floor_33,
            "partial_agreement_degree_in_T": v,
            "u": u,
            "v": v,
        })
    floors = [row["floor_depth_32"] for row in rows]
    return {
        "compatibility": "lambda*A_P(z)*J_eta(z)=lambda_prime*A_P_prime(z)*J_eta_prime(z) mod z^33 componentwise",
        "coset_modulus": "F[X]_<K",
        "depth": 32,
        "profile_domain": "v,v_prime<=511 (equivalently f,f_prime>=33)",
        "injectivity_gate": "v+v_prime<=32",
        "normalization": {
            "A_P": "z^v*Lambda_P(z^-1), where L_P=sum_(a<2048) X^a Lambda_(P,a)(phi)",
            "J_eta": "1+eta_1*z+...+eta_32*z^32",
            "P_role": "partial agreement template, not the partial error factor of the locator-line theorem",
            "U_P_eta": "L_P*(phi^f+eta_1*phi^(f-1)+...+eta_32*phi^(f-32))",
        },
        "conclusion_under_gate": "P=P_prime, eta=eta_prime, lambda=lambda_prime",
        "wedge_degree_upper": 32,
        "top_five": rows,
        "top_five_floors": floors,
        "top_five_sum": sum(floors),
        "top_five_excess_over_B_star": sum(floors) - B_STAR,
        "top_five_are_distinct_cosets": True,
        "top_five_can_be_summed_around_one_received_word": False,
        "top_three_sum": sum(floors[:3]),
        "top_three_margin_below_B_star": B_STAR - sum(floors[:3]),
        "root_free_fixed_cofactor": {
            "degree_at_most_136_preserves_depth_32_separation": True,
            "depth_32_codeword_degree_upper": K - 137,
            "degree_136_product_upper": K - 1,
            "uniform_degree_certificate_at_degree_137_requires_depth_at_least": 33,
            "top_five_depth_33_floors": [row["floor_depth_33"] for row in rows],
            "depth_33_floor_is_upper_bound": False,
        },
        "open_cofactor_strata": [
            "cofactors with roots on the evaluation domain",
            "support-dependent cofactors H_E",
            "arbitrary-word attained cofactors outside the canonical H=1 source stratum",
        ],
    }


def build_manifest() -> dict[str, Any]:
    manifest = {
        "architecture_id": ARCHITECTURE_ID,
        "chronology": {
            "active_partition_unchanged": True,
            "boundary_subterminal": BOUNDARY_SUBTERMINAL,
            "boundary_subterminal_unchanged": True,
            "diagnostic": DIAGNOSTIC,
            "diagnostic_is_first_match_owner": False,
            "global_terminal": GLOBAL_TERMINAL,
            "global_terminal_unchanged": True,
            "ledger_movement": 0,
            "owner_paid": False,
        },
        "deployed_arithmetic": deployed_arithmetic(),
        "external_dependencies": {
            "fixed_remainder_payload_sha256": FIXED_REMAINDER_PAYLOAD,
            "module_parent_head": MODULE_PARENT_HEAD,
            "module_parent_payload_sha256": MODULE_PARENT_PAYLOAD,
            "module_parent_pr": MODULE_PARENT_PR,
            "multiprefix_payload_sha256": MULTIPREFIX_PAYLOAD,
            "parent_head": PARENT_HEAD,
            "parent_payload_sha256": PARENT_PAYLOAD,
            "parent_pr": PARENT_PR,
            "template_parent_head": TEMPLATE_PARENT_HEAD,
            "template_parent_payload_sha256": TEMPLATE_PARENT_PAYLOAD,
            "template_parent_pr": TEMPLATE_PARENT_PR,
        },
        "global_locator_theorem": {
            "ambient_free_module": "F[T]^2048",
            "ambient_free_module_rank": C,
            "difference_degree_slice": "F[T]_(<=479)^137 direct_sum F[T]_(<=478)^1911",
            "difference_degree_slice_F_dimension": R,
            "degree_slices_are_FT_submodules": False,
            "locator_degree_slice": "F[T]_(<=479)^138 direct_sum F[T]_(<=478)^1910",
            "monic_fold_required": True,
            "primitive_line_equivalence": "one primitive F(T) locator line iff one positional partial-template block",
            "rank_is_locator_linear_rank_not_parent_quotient_difference_rank": True,
        },
        "pairwise_escape": {
            "automatic_absorption_if_d_at_most_w": True,
            "canonical_inverse_residue": "q=B(x)^(-1)*A_x, the unique degree<d residue with B*q=A_x mod A",
            "canonical_inverse_residue_degree": "d-1",
            "criterion": "W_(E\\{x}) subset W_E+W_F iff deg(q)<w iff d<=w",
            "criterion_scope": "x in E\\F; if x is in E intersection F, the pair never absorbs that escape",
            "deployed_close_pair_cutoff": W,
            "failed_VT_pairwise_distance_lower": W + 1,
            "flat_intersection_dimension": "max(w-d,0)",
            "same_received_word_distinct_boundary_flats_intersect_trivially": True,
            "pairwise_cut_is_already_RS_distance_for_actual_lists": True,
            "VT2_for_actual_boundary_lists_is_genuinely_higher_order": True,
        },
        "source_coset_separation": source_coset_separation(),
        "scope": {
            "deployed_row_closed": False,
            "impact": "MAXIMAL_CURRENT_HYPOTHESIS_ROUTE_CUT",
            "object": "LIST",
            "row": "Mersenne-31 list at 2^-100",
            "stable_paper_modified": False,
            "unit": "DISTINCT_BOUNDARY_SUPPORTS_AND_PRIMITIVE_TEMPLATE_LINES",
            "workboard_item": "M1",
        },
        "source_bindings": source_bindings(),
        "status": STATUS,
        "template_dichotomy": {
            "heavy_branch": "some line load >= Lambda_SD(u,v)+1 gives UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP",
            "live_gates": live_gates(),
            "max_conditional_threshold": MAX_LAMBDA,
            "no_heavy_branch": "number of primitive template lines >= ceil(packet_size/17)",
            "target_field_converse_required": "q>packet_size*R",
        },
        "current_hypothesis_route_cut": {
            "concentrated_load_shape_allowed_by_block_inequalities": True,
            "concentrated_load_shape_reason": "profile (0,0) cap exceeds every live packet and its rank-drop branch is unpaid",
            "dispersed_load_shape_allowed_by_block_inequalities": True,
            "dispersed_load_shape_establishes_pairwise_or_VT_incidence": False,
            "dispersed_load_shape_is_received_word_claim": False,
            "dispersed_load_shape_reason": "one member on each of packet_size distinct (0,0) template lines satisfies all block caps and thresholds",
            "fixed_remainder_realized_floor": 6_796_405,
            "missing_theorem": "row-uniform guarded incidence for the multitemplate primitive-line arrangement",
        },
        "nonclaims": {
            "U_Q_paid": False,
            "U_ext_paid": False,
            "U_list_int_paid": False,
            "U_new_paid": False,
            "VT_U_proved": False,
            "complete_boundary_paid": False,
            "general_rank_one_line_assigned_to_C1": False,
            "high_interior_paid": False,
            "load_countermodel_is_actual_received_word": False,
            "load_countermodel_satisfies_pairwise_or_VT_incidence": False,
            "module_rank_drop_classified": False,
            "official_endpoint_or_score_changed": False,
            "small_field_fixture_is_deployed_proof": False,
        },
        "schema": SCHEMA_ID,
    }
    return seal(manifest)


def build_schema(manifest: dict[str, Any]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    required = []
    for key, value in manifest.items():
        required.append(key)
        if key == "payload_sha256":
            properties[key] = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
        elif key == "source_bindings":
            properties[key] = {
                "type": "array", "minItems": len(SOURCE_SPECS),
                "maxItems": len(SOURCE_SPECS), "uniqueItems": True,
                "items": {"$ref": "#/$defs/sourceBinding"},
            }
        else:
            properties[key] = {"const": value}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "M31 c=2048 VT multitemplate global-rank route-cut certificate",
        "type": "object",
        "additionalProperties": False,
        "$defs": {
            "sourceBinding": {
                "type": "object", "additionalProperties": False,
                "properties": {
                    "binding_id": {"type": "string", "minLength": 1},
                    "internal_payload_sha256": {
                        "type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"
                    },
                    "path": {"type": "string", "minLength": 1},
                    "role": {"type": "string", "minLength": 1},
                    "scope": {"type": "string", "minLength": 1},
                    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                },
                "required": ["binding_id", "internal_payload_sha256", "path",
                             "role", "scope", "sha256"],
            }
        },
        "properties": properties,
        "required": required,
    }


def semantic_checks(manifest: dict[str, Any]) -> None:
    require(manifest["architecture_id"] == ARCHITECTURE_ID, "architecture")
    require(manifest["status"] == STATUS, "status")
    require(manifest["payload_sha256"] == payload_sha256(manifest), "payload seal")
    arithmetic = manifest["deployed_arithmetic"]
    require(R == 479 * C + 137, "radius division")
    require(W == 67_447, "w")
    require(arithmetic["locator_degree_slice"]["degree_479_rows"] == 138,
            "locator high rows")
    require(arithmetic["locator_degree_slice"]["degree_478_rows"] == 1910,
            "locator low rows")
    require(arithmetic["difference_degree_slice"]["degree_479_rows"] == 137,
            "difference high rows")
    require(arithmetic["difference_degree_slice"]["degree_478_rows"] == 1911,
            "difference low rows")
    require(arithmetic["difference_degree_slice"]["F_dimension"] == R,
            "difference dimension")
    require(arithmetic["locator_degree_slice"]["is_FT_submodule"] is False,
            "locator slice not submodule")
    require(arithmetic["difference_degree_slice"]["is_FT_submodule"] is False,
            "difference slice not submodule")
    gates = manifest["template_dichotomy"]["live_gates"]
    expected_lines = [542_164, 986_676, 986_896]
    require([g["minimum_template_lines_no_heavy"] for g in gates] == expected_lines,
            "live template-line counts")
    for gate in gates:
        require(gate["packet_size"] == gate["U"] + 1, "packet size")
        require(gate["guard_count"] == gate["packet_size"] * R, "guard count")
        require(gate["target_field_converse_gate"] is True, "target-field gate")
        require(gate["minimum_template_lines_no_heavy"]
                == ceil_div(gate["packet_size"], MAX_LAMBDA), "line ceiling")
    require(arithmetic["profile_00"]["fixed_template_cap_digits"] == 255,
            "profile 00 cap digits")
    require(arithmetic["profile_00"]["positional_template_lower_digits"] == 220,
            "profile 00 template digits")
    require(arithmetic["profile_00"]["cap_exceeds_full_forbidden_packet"] is True,
            "concentrated extremizer")
    require(arithmetic["profile_00"]["templates_exceed_full_forbidden_packet"] is True,
            "dispersed extremizer")
    require(manifest["chronology"]["ledger_movement"] == 0, "zero movement")
    require(manifest["chronology"]["owner_paid"] is False, "unpaid")
    require(manifest["nonclaims"]["VT_U_proved"] is False, "VT open")
    require(manifest["nonclaims"]["load_countermodel_is_actual_received_word"] is False,
            "load model scope")
    require(manifest["nonclaims"]["load_countermodel_satisfies_pairwise_or_VT_incidence"] is False,
            "load incidence scope")
    require(manifest["pairwise_escape"]["failed_VT_pairwise_distance_lower"] == W + 1,
            "pairwise cutoff")
    require(manifest["pairwise_escape"]["canonical_inverse_residue_degree"] == "d-1",
            "inverse-residue degree")
    require(manifest["pairwise_escape"]["same_received_word_distinct_boundary_flats_intersect_trivially"] is True,
            "same-word pairwise-flat specialization")
    cosets = manifest["source_coset_separation"]
    require(cosets["top_five_floors"]
            == [6_796_405, 3_614_120, 3_182_286, 1_920_222, 1_693_898],
            "top five floors")
    require(cosets["top_five_sum"] == B_STAR + 429_716,
            "top five formal excess")
    require(cosets["top_three_sum"] == B_STAR - 3_184_404,
            "top three margin")
    require(cosets["top_five_are_distinct_cosets"] is True,
            "top five separation")
    require(cosets["top_five_can_be_summed_around_one_received_word"] is False,
            "no source-floor summation")
    require(max(row["v"] for row in cosets["top_five"]) == 2,
            "top-five v range")
    require(all(a["v"] + b["v"] <= 32 for a in cosets["top_five"]
                for b in cosets["top_five"]), "pairwise wedge gate")
    root_free = cosets["root_free_fixed_cofactor"]
    require(root_free["depth_32_codeword_degree_upper"] == K - 137,
            "depth-32 headroom")
    require(root_free["degree_136_product_upper"] == K - 1,
            "root-free degree 136 headroom")
    require(root_free["uniform_degree_certificate_at_degree_137_requires_depth_at_least"] == 33,
            "root-free degree 137 gate")
    require(root_free["top_five_depth_33_floors"] == [1, 1, 1, 1, 1],
            "depth-33 source collapse")
    require(root_free["depth_33_floor_is_upper_bound"] is False,
            "depth-33 floor scope")
    require(len(manifest["source_bindings"]) == len(SOURCE_SPECS), "source count")


def expected_artifacts() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = build_manifest()
    return manifest, build_schema(manifest)


def write_artifacts() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    # The schema constrains source bindings generically and is therefore
    # independent of its own eventual byte hash.  A canonical placeholder
    # permits a clean bootstrap before source_bindings() hashes the file.
    if not SCHEMA_PATH.is_file():
        SCHEMA_PATH.write_bytes(canonical_json({}))
    manifest, schema = expected_artifacts()
    SCHEMA_PATH.write_bytes(canonical_json(schema))
    # Rebuild the manifest after the schema assumes its final bytes.
    manifest, schema = expected_artifacts()
    SCHEMA_PATH.write_bytes(canonical_json(schema))
    final_manifest, final_schema = expected_artifacts()
    require(final_schema == schema, "schema fixed point")
    manifest = final_manifest
    MANIFEST_PATH.write_bytes(canonical_json(manifest))
    print(f"WROTE {SCHEMA_PATH.relative_to(ROOT)}")
    print(f"WROTE {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"PAYLOAD {manifest['payload_sha256']}")


def check_artifacts() -> None:
    expected_manifest, expected_schema = expected_artifacts()
    actual_schema = strict_json_path(SCHEMA_PATH, canonical=True)
    require(actual_schema == expected_schema, "schema exact bytes/content")
    # Recompute after binding the checked schema bytes.
    expected_manifest, expected_schema = expected_artifacts()
    actual_manifest = strict_json_path(MANIFEST_PATH, canonical=True)
    require(actual_manifest == expected_manifest, "manifest exact bytes/content")
    semantic_checks(actual_manifest)
    print(f"PASS checks={CHECKS} payload={actual_manifest['payload_sha256']}")


def expect_failure(label: str, fn: Callable[[], None]) -> None:
    try:
        fn()
    except (VerificationError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return
    raise VerificationError(f"mutation survived: {label}")


def tamper_selftest() -> None:
    manifest = build_manifest()
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("architecture", lambda x: x.__setitem__("architecture_id", "WRONG")),
        ("status", lambda x: x.__setitem__("status", "PAID")),
        ("locator rows", lambda x: x["deployed_arithmetic"]["locator_degree_slice"].__setitem__("degree_479_rows", 137)),
        ("difference rows", lambda x: x["deployed_arithmetic"]["difference_degree_slice"].__setitem__("degree_478_rows", 1910)),
        ("difference dimension", lambda x: x["deployed_arithmetic"]["difference_degree_slice"].__setitem__("F_dimension", R - 1)),
        ("locator submodule", lambda x: x["deployed_arithmetic"]["locator_degree_slice"].__setitem__("is_FT_submodule", True)),
        ("line count 1", lambda x: x["template_dichotomy"]["live_gates"][0].__setitem__("minimum_template_lines_no_heavy", 542_163)),
        ("line count 2", lambda x: x["template_dichotomy"]["live_gates"][1].__setitem__("minimum_template_lines_no_heavy", 986_675)),
        ("line count 3", lambda x: x["template_dichotomy"]["live_gates"][2].__setitem__("minimum_template_lines_no_heavy", 986_895)),
        ("guard", lambda x: x["template_dichotomy"]["live_gates"][2].__setitem__("guard_count", 0)),
        ("field gate", lambda x: x["template_dichotomy"]["live_gates"][0].__setitem__("target_field_converse_gate", False)),
        ("rank-line equivalence", lambda x: x["global_locator_theorem"].__setitem__("primitive_line_equivalence", "false")),
        ("rank collision", lambda x: x["global_locator_theorem"].__setitem__("rank_is_locator_linear_rank_not_parent_quotient_difference_rank", False)),
        ("escape cutoff", lambda x: x["pairwise_escape"].__setitem__("failed_VT_pairwise_distance_lower", W)),
        ("escape criterion", lambda x: x["pairwise_escape"].__setitem__("criterion", "wrong")),
        ("inverse degree", lambda x: x["pairwise_escape"].__setitem__("canonical_inverse_residue_degree", "d")),
        ("same-word intersection", lambda x: x["pairwise_escape"].__setitem__("same_received_word_distinct_boundary_flats_intersect_trivially", False)),
        ("coset floor", lambda x: x["source_coset_separation"]["top_five_floors"].__setitem__(0, 6_796_404)),
        ("coset sum", lambda x: x["source_coset_separation"].__setitem__("top_five_sum", B_STAR)),
        ("coset summation", lambda x: x["source_coset_separation"].__setitem__("top_five_can_be_summed_around_one_received_word", True)),
        ("wedge v", lambda x: x["source_coset_separation"]["top_five"][0].__setitem__("v", 33)),
        ("root-free headroom", lambda x: x["source_coset_separation"]["root_free_fixed_cofactor"].__setitem__("degree_136_product_upper", K)),
        ("depth 33 floor", lambda x: x["source_coset_separation"]["root_free_fixed_cofactor"]["top_five_depth_33_floors"].__setitem__(0, 2)),
        ("depth 33 upper", lambda x: x["source_coset_separation"]["root_free_fixed_cofactor"].__setitem__("depth_33_floor_is_upper_bound", True)),
        ("paid", lambda x: x["chronology"].__setitem__("owner_paid", True)),
        ("movement", lambda x: x["chronology"].__setitem__("ledger_movement", 1)),
        ("VT claimed", lambda x: x["nonclaims"].__setitem__("VT_U_proved", True)),
        ("countermodel claimed actual", lambda x: x["nonclaims"].__setitem__("load_countermodel_is_actual_received_word", True)),
        ("countermodel claimed incidence", lambda x: x["nonclaims"].__setitem__("load_countermodel_satisfies_pairwise_or_VT_incidence", True)),
        ("source deletion", lambda x: x["source_bindings"].pop()),
        ("source hash", lambda x: x["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("parent payload", lambda x: x["external_dependencies"].__setitem__("parent_payload_sha256", "0" * 64)),
        ("profile cap", lambda x: x["deployed_arithmetic"]["profile_00"].__setitem__("cap_exceeds_full_forbidden_packet", False)),
        ("profile templates", lambda x: x["deployed_arithmetic"]["profile_00"].__setitem__("templates_exceed_full_forbidden_packet", False)),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        candidate = seal(candidate)
        def verify_mutation(c: dict[str, Any] = candidate) -> None:
            semantic_checks(c)
            require(c == manifest, "exact expected manifest")
        expect_failure(label, verify_mutation)

    expect_failure("duplicate JSON key", lambda: strict_json_bytes(
        b'{"x":1,"x":2}\n', canonical=False))
    expect_failure("float", lambda: strict_json_bytes(b'{"x":1.0}\n', canonical=False))
    expect_failure("non-ASCII", lambda: strict_json_bytes(b'{"x":"\xc3\xa9"}\n', canonical=False))
    expect_failure("noncanonical", lambda: strict_json_bytes(b'{ "x": 1 }\n', canonical=True))
    print(f"PASS tamper={len(mutations)+4} checks={CHECKS}")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_artifacts()
        elif args.check:
            check_artifacts()
        else:
            tamper_selftest()
    except VerificationError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
