#!/usr/bin/env python3
"""Build and verify the fail-closed M1 A4 SPI-atlas manifests.

The deployed KoalaBear artifact records the proved base-generated-field
image-cell cap, but it deliberately does *not* identify the source affine-row
indices with SPI charts.  Until that adapter is proved, the candidate family
has zero represented charts and an unpaid terminal.

The GF(19) artifact is an exhaustive, non-banking machinery control for the
48 support patterns in the L1 profile (ell,d,r,t,a_i)=(4,4,2,2,(3,3)).
It tests canonical keys, first-match routing, duplicate rejection, and exact
charge arithmetic; it proves no deployed M1 claim.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_REL = Path("experimental/data/schemas/m1_a4_spi_atlas_manifest_v1.schema.json")
SCHEMA_PATH = ROOT / SCHEMA_REL
VERIFIER_REL = Path("experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py")
OWNER_HELPERS_REL = Path("experimental/scripts/scan_l1_full_list_quotient_conjecture.py")
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/m1-a4-spi-atlas-manifest-v1"
)
GF19_PATH = CERT_DIR / "gf19_442233_machinery_control.json"
KB_PATH = CERT_DIR / "kb_mca_a1116048_base_generated_family.json"

KB_NOTE = Path(
    "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
)
KB_PACKET = Path(
    "experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/"
    "kb_mca_1116048_first_match_ledger_v1.json"
)
KB_VERIFIER = Path(
    "experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py"
)
GF19_NOTE = Path(
    "experimental/notes/l1/l1_mixed_petal_residual_frontier_ledger.md"
)
GF19_SCANNER = Path(
    "experimental/scripts/verify_l1_mixed_petal_frontier_ledger.py"
)
GF19_PROFILE_VERIFIER = Path(
    "experimental/scripts/verify_l1_b9_m2_full_rank_ledger.py"
)
ELIMINANT_CONTROL_SOURCE = Path(
    "experimental/data/certificates/m1-a4-spi-atlas-manifest-v1/"
    "eliminant_identity_control.json"
)

SCRIPT_DIR = ROOT / "experimental/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    b11_frontier_record,
    classify_b11_box,
    johnson_slack_needed,
    rotate_mask,
    stabilizer_order,
)

SCHEMA_ID = "rs-mca-m1-a4-spi-atlas-manifest-v1"
L1_OWNER_ORDER = [
    "PERIODIC_SUPPORT",
    "INVARIANT_QUOTIENT_DESCENT",
    "AUXILIARY_JOHNSON",
    "GLOBAL_JOHNSON",
    "B11_G2",
    "B11_GR",
    "UNPAID_PRIMITIVE",
]
M1_OWNER_ORDER = [
    "contained_or_noncontained_failure",
    "rank_drop_or_pivot_failure",
    "tangent_common_line_residue",
    "quotient_periodic_or_divisor_stabilized",
    "planted_prefix_structured",
    "extension_valued_slope",
    "base_generated_field_collision",
    "sparse_sigma_or_sparse_support",
    "m1_half_turn_or_coefficient_shadow",
    "primitive_qfin_residual",
]

P_KB = 2_130_706_433
E_KB = 6
Q_KB = P_KB**E_KB
N_KB = 2_097_152
K_KB = 1_048_576
A_KB = 1_116_048
J_KB = N_KB - A_KB
T_KB = A_KB - K_KB
W_KB = T_KB - 1
KERNEL_KB = J_KB + 1 - T_KB
DENOMINATOR = 1 << 128
B_STAR_KB = Q_KB // DENOMINATOR
GENERATED_CHARGE = T_KB * P_KB
QUOTIENT_TERMINAL_CHARGE = 471_447_040
U_PAID_KB = GENERATED_CHARGE + QUOTIENT_TERMINAL_CHARGE

EXPECTED_GF_ASSIGNMENT_HASH = (
    "03d00b8d225d5af19ed74f105895d31aa738abb50dc3111e65f4bb90be387644"
)
EXPECTED_GF_MASK_HASH = (
    "49bf3c30e5139c61638b8917e298ddc7d0f36418ccce13d202968adace871fd2"
)


class VerificationError(RuntimeError):
    """A certificate or semantic invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(path: Path) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def source_binding(binding_id: str, path: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": path.as_posix(),
        "sha256": file_hash(path),
        "role": role,
    }


def nullable_profile(profile_id: str) -> dict[str, Any]:
    return {
        "profile_id": profile_id,
        "ell": None,
        "d": None,
        "r": None,
        "t": None,
        "a_i": [],
        "G2": None,
        "GR": None,
    }


def field_record(p: int, extension_degree: int, domain: str) -> dict[str, Any]:
    q = p**extension_degree
    return {
        "characteristic_p": p,
        "extension_degree": extension_degree,
        "q_base": str(p),
        "q_line": str(q),
        "sampling_denominator": str(DENOMINATOR),
        "target_bits": 128,
        "B_star_q": str(q // DENOMINATOR),
        "B_star_q_minus_1": str((q - 1) // DENOMINATOR),
        "budget_floors_coincide": q // DENOMINATOR == (q - 1) // DENOMINATOR,
        "domain": domain,
    }


def terminal_unpaid() -> dict[str, Any]:
    return {
        "kind": "UNPAID_PRIMITIVE",
        "owner_id": None,
        "charge_id": None,
        "numeric_charge": None,
        "eliminant": None,
    }


def mask(support: list[int]) -> int:
    result = 0
    for point in support:
        result |= 1 << point
    return result


def cyclic_quotient_scales(mask_value: int, n: int) -> list[int]:
    return [
        scale
        for scale in range(2, n + 1)
        if n % scale == 0 and rotate_mask(mask_value, n // scale, n) == mask_value
    ]


def gf19_assignments() -> list[tuple[list[list[int]], list[int], list[int]]]:
    petals = [list(range(4, 8)), list(range(8, 12)), list(range(12, 16))]
    background = [16, 17]
    result: list[tuple[list[list[int]], list[int], list[int]]] = []
    for touched in itertools.combinations(range(3), 2):
        for left in itertools.combinations(petals[touched[0]], 3):
            for right in itertools.combinations(petals[touched[1]], 3):
                selected_petals: list[list[int]] = [[], [], []]
                selected_petals[touched[0]] = list(left)
                selected_petals[touched[1]] = list(right)
                selected = sorted(background + list(left) + list(right))
                assignment = [background, *selected_petals]
                result.append((assignment, list(touched), selected))
    return result


def gf19_gate_derivation(selected_mask: int) -> tuple[list[dict[str, Any]], int, list[int]]:
    stabilizer = stabilizer_order(selected_mask, 18)
    quotient_scales = cyclic_quotient_scales(selected_mask, 18)
    lambda_j = johnson_slack_needed(18, 5, 8)
    b11 = b11_frontier_record(
        ell=4,
        petal_count=3,
        d=4,
        r=2,
        a_i=[3, 3],
        agreement_slack=0,
        lambda_j=lambda_j,
        maximal=True,
    )
    box = classify_b11_box(b11, E=0, V2=0, VR=0)
    auxiliary = b11["auxiliary_johnson"]
    evidence = {
        "PERIODIC_SUPPORT": f"cyclic exponent-shift stabilizer order is {stabilizer}",
        "INVARIANT_QUOTIENT_DESCENT": f"complete cyclic fibre scales are {quotient_scales}; no all-data descent certificate",
        "AUXILIARY_JOHNSON": (
            "required=%d domain=%d degree=%d margin=%d"
            % (
                auxiliary["required_agreement"],
                auxiliary["petal_domain_size"],
                auxiliary["effective_degree_bound"],
                auxiliary["margin"],
            )
        ),
        "GLOBAL_JOHNSON": f"lambda={b11['lambda']} is below lambda_J={lambda_j}",
        "B11_G2": f"classification={box} at (d-ell,G2,GR)=({b11['d_minus_ell']},{b11['G2']},{b11['GR']})",
        "B11_GR": f"classification={box} at (d-ell,G2,GR)=({b11['d_minus_ell']},{b11['G2']},{b11['GR']})",
        "UNPAID_PRIMITIVE": "no earlier frozen owner is eligible",
    }
    eligible = {
        "PERIODIC_SUPPORT": stabilizer > 1,
        "INVARIANT_QUOTIENT_DESCENT": False,
        "AUXILIARY_JOHNSON": bool(auxiliary["paid"]),
        "GLOBAL_JOHNSON": int(b11["lambda"]) >= lambda_j,
        "B11_G2": box == "PAID_G2",
        "B11_GR": box == "PAID_GR",
        "UNPAID_PRIMITIVE": True,
    }
    gates = [
        {
            "owner_id": owner_id,
            "eligible": eligible[owner_id],
            "evidence": evidence[owner_id],
        }
        for owner_id in L1_OWNER_ORDER
    ]
    return gates, stabilizer, quotient_scales


def gf19_gates(selected_mask: int) -> list[dict[str, Any]]:
    gates, _, _ = gf19_gate_derivation(selected_mask)
    return [
        dict(gate)
        for gate in gates
    ]


def build_gf19_manifest() -> dict[str, Any]:
    assignments = gf19_assignments()
    assignment_digest = canonical_hash([entry[0] for entry in assignments])
    masks = [mask(entry[2]) for entry in assignments]
    mask_digest = canonical_hash(masks)
    require(assignment_digest == EXPECTED_GF_ASSIGNMENT_HASH, "GF19 assignment digest drift")
    require(mask_digest == EXPECTED_GF_MASK_HASH, "GF19 mask digest drift")

    charts: list[dict[str, Any]] = []
    for index, (assignment, touched, selected) in enumerate(assignments):
        selected_mask = mask(selected)
        gates, selected_stabilizer, quotient_scales = gf19_gate_derivation(selected_mask)
        charts.append(
            {
                "chart_id": f"gf19-442233-{index:03d}",
                "canonical_key": {
                    "A": 8,
                    "quantifier_scope": "GF19_L1_CONTROL_442233",
                    "locator_chart_id": f"petals-{touched[0]}-{touched[1]}",
                    "patch": "full-agreement-cofactor-support",
                    "rank_s": None,
                    "pivot_rows": [],
                    "pivot_cols": [],
                    "pivot_kind": "CONTROL_NOT_COMPUTED",
                    "h": index,
                },
                "support_pattern": {
                    "active_petal_labels": touched,
                    "petal_supports": assignment[1:],
                    "background_support": assignment[0],
                    "selected_support": selected,
                    "selected_support_mask": selected_mask,
                    "stabilizer_order": selected_stabilizer,
                    "complete_fibre_scales": quotient_scales,
                },
                "gates": gates,
                "localization": {
                    "split_support": True,
                    "distinct_labels": True,
                    "noncontainment": True,
                    "finite_pivot": False,
                    "earlier_pivots_zero": False,
                },
                "terminal": terminal_unpaid(),
            }
        )

    artifact: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "artifact_kind": "CONTROL_FIXTURE",
        "status": "AUDIT",
        "quantifier_scope": {
            "scope_id": "GF19_L1_CONTROL_442233",
            "received_lines": "one frozen sequential GF(19) toy layout",
            "slopes": "not enumerated; support-owner machinery only",
            "supports": "all 48 canonical labelled support patterns",
            "uniformity": "EXACT_FINITE_CONTROL_ONLY",
            "excluded_scopes": [
                "deployed M1 rows",
                "slope eliminants",
                "asymptotic conclusions",
            ],
        },
        "row": {
            "row_id": "gf19-l1-442233-control",
            "field": field_record(19, 1, "frozen sequential evaluation domain 0..17"),
            "n": 18,
            "k": 5,
            "agreement_A": 8,
            "error_count_j": 10,
            "syndrome_depth_t": 3,
            "prefix_depth_w": 2,
            "kernel_dimension_lower_bound": 8,
            "deficiency_one": False,
            "profile": {
                "profile_id": "L1_ELL4_D4_R2_T2_A33",
                "ell": 4,
                "d": 4,
                "r": 2,
                "t": 2,
                "a_i": [3, 3],
                "G2": 2,
                "GR": 3,
            },
        },
        "owner_policy": {
            "policy_id": "L1_FROZEN_FIRST_MATCH_V1",
            "order": L1_OWNER_ORDER,
            "fallback_unpaid_owner_id": "UNPAID_PRIMITIVE",
            "terminal_order_frozen": True,
            "unpaid_semantics": "unpaid under this owner stack, not algebraically primitive",
        },
        "coverage": {
            "scope_complete": True,
            "row_complete": False,
            "unit_kind": "EXPLICIT_CHART",
            "expected_units": 48,
            "represented_units": 48,
            "missing_units": 0,
            "paid_count": 0,
            "eliminant_count": 0,
            "unpaid_count": 48,
            "canonical_assignment_sha256": assignment_digest,
            "mask_list_sha256": mask_digest,
            "coverage_status": "CONTROL_SCOPE_ENUMERATED",
            "uncovered_scopes": [
                "slope equations and eliminants",
                "deployed-row chart adapter",
            ],
        },
        "source_bindings": [
            source_binding("atlas-schema", SCHEMA_REL, "closed manifest contract"),
            source_binding("atlas-verifier", VERIFIER_REL, "semantic and mutation verifier"),
            source_binding("l1-owner-helpers", OWNER_HELPERS_REL, "cyclic stabilizer and Johnson/B11 helpers"),
            source_binding("eliminant-control-equations", ELIMINANT_CONTROL_SOURCE, "synthetic ideal-identity positive control"),
            source_binding("gf19-ledger-note", GF19_NOTE, "aggregate profile definitions"),
            source_binding("gf19-ledger-scanner", GF19_SCANNER, "exact profile enumerator"),
            source_binding(
                "gf19-profile-verifier",
                GF19_PROFILE_VERIFIER,
                "frozen GF(19) case and profile coordinates",
            ),
        ],
        "charts": charts,
        "compressed_chart_families": [],
        "ledger": {
            "ledger_consequence": False,
            "charges": [],
            "U_paid": "0",
            "U_Q": None,
            "U_A": "17328",
            "lhs": None,
            "B_star": "0",
            "inequality_status": "CONTROL_ONLY_NO_LEDGER_CONSEQUENCE",
            "eliminant_aggregation_mode": "NONE_CONTROL",
            "eliminant_charge": "0",
            "charge_ids_unique": True,
        },
        "nonclaims": [
            "The 48-pattern control is not a deployed M1 atlas.",
            "UNPAID_PRIMITIVE means unpaid under the frozen owner order only.",
            "The control has no ledger consequence and does not bank 17,328.",
            "No slope eliminant or fixed-syndrome rank theorem is asserted.",
        ],
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def build_kb_manifest() -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "artifact_kind": "DEPLOYED_PARTIAL_MANIFEST",
        "status": "PARTIAL",
        "quantifier_scope": {
            "scope_id": "KB_MCA_A1116048_BASE_FINITE_SLOPE_CANDIDATES",
            "received_lines": "all received lines only after the source packet's prior buckets",
            "slopes": "finite base-valued slopes in F_p only",
            "supports": "not enumerated by the source affine-row packet",
            "uniformity": "CANDIDATE_CAPACITY_NAMESPACE_WITH_UNPROVEN_SPI_ADAPTER",
            "excluded_scopes": [
                "extension-valued slopes in F_(p^6) minus F_p",
                "raw support multiplicity",
                "all SPI charts not mapped to affine rows",
            ],
        },
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "field": field_record(P_KB, E_KB, "KoalaBear multiplicative subgroup of F_(p^6)^*"),
            "n": N_KB,
            "k": K_KB,
            "agreement_A": A_KB,
            "error_count_j": J_KB,
            "syndrome_depth_t": T_KB,
            "prefix_depth_w": W_KB,
            "kernel_dimension_lower_bound": KERNEL_KB,
            "deficiency_one": False,
            "profile": nullable_profile("M1_A4_FULL_ROW_UNRESOLVED"),
        },
        "owner_policy": {
            "policy_id": "KB_MCA_1116048_FIRST_MATCH_LEDGER_V1",
            "order": M1_OWNER_ORDER,
            "fallback_unpaid_owner_id": "primitive_qfin_residual",
            "terminal_order_frozen": True,
            "unpaid_semantics": "unmapped capacity indices remain unpaid until the SPI-to-affine-row adapter is proved",
        },
        "coverage": {
            "scope_complete": False,
            "row_complete": False,
            "unit_kind": "CAPACITY_INDEX_NOT_CHART",
            "expected_units": T_KB,
            "represented_units": 0,
            "missing_units": T_KB,
            "paid_count": 0,
            "eliminant_count": 0,
            "unpaid_count": 0,
            "canonical_assignment_sha256": None,
            "mask_list_sha256": None,
            "coverage_status": "BOUNDED_FAMILY_ONLY",
            "uncovered_scopes": [
                "SPI chart to affine-row index adapter",
                "extension-valued slopes",
                "primitive q-finite residual",
                "U_Q and U_A",
            ],
        },
        "source_bindings": [
            source_binding("atlas-schema", SCHEMA_REL, "closed manifest contract"),
            source_binding("atlas-verifier", VERIFIER_REL, "semantic and mutation verifier"),
            source_binding("kb-first-match-note", KB_NOTE, "proved ledger statement"),
            source_binding("kb-first-match-packet", KB_PACKET, "machine-readable owner charge"),
            source_binding("kb-first-match-verifier", KB_VERIFIER, "exact and tamper replay"),
        ],
        "charts": [],
        "compressed_chart_families": [
            {
                "family_id": "kb-a1116048-affine-row-capacity-namespace",
                "canonical_key_prefix": {
                    "A": A_KB,
                    "quantifier_scope": "KB_MCA_A1116048_BASE_FINITE_SLOPE_CANDIDATES",
                    "locator_chart_id": "UNMAPPED_SPI_CHART",
                    "patch": "candidate-base-finite-slope",
                    "rank_s": None,
                    "pivot_rows": [],
                    "pivot_cols": [],
                    "pivot_kind": "SOURCE_AFFINE_ROW_INDEX_NOT_SPI_PIVOT",
                },
                "h_start": 0,
                "h_end": W_KB,
                "index_count": T_KB,
                "index_semantics": "capacity labels only; h is not yet proved equal to the source affine-row index i",
                "candidate_owner_id": "base_generated_field_collision",
                "chart_adapter_status": "UNPROVEN",
                "per_index_image_cap": str(P_KB),
                "family_image_cap": str(GENERATED_CHARGE),
                "source_claim_pointer": "/generated_field_collision_charge",
                "earlier_pivots_zero_by_definition": True,
                "finite_pivot_nonzero": True,
                "noncontainment_localized": True,
                "split_support_localized": False,
                "gate_scope": {
                    "base_valued": True,
                    "finite_affine": True,
                    "prior_buckets_removed": True,
                    "extension_valued_excluded": True,
                },
                "terminal": terminal_unpaid(),
                "source_binding_ids": [
                    "kb-first-match-note",
                    "kb-first-match-packet",
                    "kb-first-match-verifier",
                ],
            }
        ],
        "ledger": {
            "ledger_consequence": False,
            "charges": [
                {
                    "charge_id": "kb-base-generated-image-cell-cover",
                    "owner_id": "base_generated_field_collision",
                    "amount": str(GENERATED_CHARGE),
                    "scope": "IMPORTED_GLOBAL_ONCE",
                    "source_binding_id": "kb-first-match-packet",
                    "source_claim_pointer": "/deployed_arithmetic/B_gen_t_times_p",
                },
                {
                    "charge_id": "kb-terminal-quotient-raw",
                    "owner_id": "quotient_periodic_or_divisor_stabilized",
                    "amount": str(QUOTIENT_TERMINAL_CHARGE),
                    "scope": "IMPORTED_GLOBAL_ONCE",
                    "source_binding_id": "kb-first-match-packet",
                    "source_claim_pointer": "/deployed_arithmetic/terminal_quotient_raw_paid_cost",
                },
            ],
            "U_paid": str(U_PAID_KB),
            "U_Q": None,
            "U_A": None,
            "lhs": None,
            "B_star": str(B_STAR_KB),
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
            "eliminant_aggregation_mode": "NOT_COMPUTED",
            "eliminant_charge": None,
            "charge_ids_unique": True,
        },
        "nonclaims": [
            "The h namespace is not an enumeration of deployed SPI charts.",
            "The tp cap is an image-cell cover, not a support multiplicity bound.",
            "Extension-valued slopes remain unpaid.",
            "U_Q, U_A, and the target inequality remain undecided.",
            "This artifact does not improve the KoalaBear frontier.",
        ],
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def _is_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise VerificationError(f"unsupported schema type {expected!r}")


def validate_schema_value(
    value: Any,
    node: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> None:
    if "$ref" in node:
        ref = node["$ref"]
        require(ref.startswith("#/$defs/"), f"{path}: unsupported ref {ref}")
        target = root_schema["$defs"][ref.rsplit("/", 1)[1]]
        validate_schema_value(value, target, root_schema, path)
        return
    if "anyOf" in node:
        errors = []
        for option in node["anyOf"]:
            try:
                validate_schema_value(value, option, root_schema, path)
                return
            except VerificationError as exc:
                errors.append(str(exc))
        raise VerificationError(f"{path}: no anyOf branch matched")
    if "const" in node:
        require(value == node["const"], f"{path}: const mismatch")
    if "enum" in node:
        require(value in node["enum"], f"{path}: enum mismatch")
    expected_type = node.get("type")
    if expected_type is not None:
        require(_is_type(value, expected_type), f"{path}: expected {expected_type}")
    if isinstance(value, dict):
        required = node.get("required", [])
        missing = sorted(set(required) - set(value))
        require(not missing, f"{path}: missing keys {missing}")
        properties = node.get("properties", {})
        if node.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            require(not unknown, f"{path}: unknown keys {unknown}")
        for key, child in value.items():
            if key in properties:
                validate_schema_value(child, properties[key], root_schema, f"{path}.{key}")
    if isinstance(value, list):
        if "minItems" in node:
            require(len(value) >= node["minItems"], f"{path}: too few items")
        if node.get("uniqueItems"):
            encoded = [canonical_bytes(item) for item in value]
            require(len(encoded) == len(set(encoded)), f"{path}: duplicate items")
        if "items" in node:
            for index, child in enumerate(value):
                validate_schema_value(child, node["items"], root_schema, f"{path}[{index}]")
    if isinstance(value, str):
        if "minLength" in node:
            require(len(value) >= node["minLength"], f"{path}: string too short")
        if "pattern" in node:
            require(re.fullmatch(node["pattern"], value) is not None, f"{path}: pattern mismatch")
    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in node:
        require(value >= node["minimum"], f"{path}: below minimum")


def assert_closed_object_schemas(node: Any, path: str = "$schema") -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            require(
                node.get("additionalProperties") is False,
                f"{path}: object schema is not fail-closed",
            )
        for key, value in node.items():
            assert_closed_object_schemas(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_closed_object_schemas(value, f"{path}[{index}]")


def validate_row_arithmetic(artifact: dict[str, Any]) -> None:
    row = artifact["row"]
    field = row["field"]
    p = field["characteristic_p"]
    extension = field["extension_degree"]
    q = p**extension
    denominator = 1 << field["target_bits"]
    require(int(field["q_base"]) == p, "q_base must equal the characteristic field size")
    require(int(field["q_line"]) == q, "q_line extension arithmetic drift")
    require(int(field["sampling_denominator"]) == denominator, "sampling denominator drift")
    b_q = q // denominator
    b_q_minus_1 = (q - 1) // denominator
    require(int(field["B_star_q"]) == b_q, "B_star_q drift")
    require(int(field["B_star_q_minus_1"]) == b_q_minus_1, "B_star_q_minus_1 drift")
    require(field["budget_floors_coincide"] == (b_q == b_q_minus_1), "budget-floor flag drift")
    require(row["error_count_j"] == row["n"] - row["agreement_A"], "j=n-A drift")
    require(row["syndrome_depth_t"] == row["agreement_A"] - row["k"], "t=A-k drift")
    require(row["prefix_depth_w"] == row["syndrome_depth_t"] - 1, "w=t-1 drift")
    kernel = row["error_count_j"] + 1 - row["syndrome_depth_t"]
    require(row["kernel_dimension_lower_bound"] == kernel, "kernel lower-bound drift")
    require(row["deficiency_one"] == (kernel == 1), "deficiency-one flag drift")
    require(int(artifact["ledger"]["B_star"]) == b_q, "ledger B_star drift")


def validate_source_bindings(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    bindings = artifact["source_bindings"]
    ids = [binding["binding_id"] for binding in bindings]
    require(len(ids) == len(set(ids)), "duplicate source binding id")
    by_id = {binding["binding_id"]: binding for binding in bindings}
    for binding in bindings:
        path = Path(binding["path"])
        require(not path.is_absolute(), "source path must be repository-relative")
        require(".." not in path.parts, "source path traversal rejected")
        require(
            (ROOT / path).resolve().is_relative_to(ROOT.resolve()),
            "source binding escapes repository root",
        )
        require((ROOT / path).is_file(), f"missing source binding {path}")
        require(binding["sha256"] == file_hash(path), f"source hash drift: {path}")
    return by_id


def first_eligible(gates: list[dict[str, Any]]) -> str | None:
    for gate in gates:
        if gate["eligible"]:
            return gate["owner_id"]
    return None


def resolve_json_pointer(binding: dict[str, Any], pointer: str) -> Any:
    path = ROOT / binding["path"]
    require(path.suffix == ".json", "claim pointer requires a JSON source binding")
    value: Any = load_json(path)
    require(pointer.startswith("/"), "JSON pointer must start with slash")
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            require(part in value, f"JSON pointer component missing: {part}")
            value = value[part]
        elif isinstance(value, list):
            require(part.isdigit() and int(part) < len(value), "JSON pointer list index invalid")
            value = value[int(part)]
        else:
            raise VerificationError("JSON pointer traverses a scalar")
    return value


def normalize_poly(coefficients: list[int], p: int) -> list[int]:
    result = [coefficient % p for coefficient in coefficients]
    while result and result[-1] == 0:
        result.pop()
    return result


def multiply_poly(left: list[int], right: list[int], p: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] = (result[i + j] + left_value * right_value) % p
    return normalize_poly(result, p)


def add_poly(left: list[int], right: list[int], p: int) -> list[int]:
    result = [0] * max(len(left), len(right))
    for index in range(len(result)):
        result[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % p
    return normalize_poly(result, p)


def validate_eliminant(
    eliminant: dict[str, Any],
    p: int,
    chart: dict[str, Any],
    binding_by_id: dict[str, dict[str, Any]],
) -> int:
    coeffs = eliminant["coefficients_low_to_high"]
    nonzero_indices = [index for index, coefficient in enumerate(coeffs) if coefficient % p]
    require(eliminant["nonzero"], "eliminant must be certified nonzero")
    require(nonzero_indices, "zero eliminant rejected")
    require(eliminant["degree"] == max(nonzero_indices), "eliminant degree drift")
    require(
        eliminant["root_space_id"] == f"{chart['chart_id']}::{eliminant['variable']}",
        "root space must be chart-specific in v1",
    )

    ideal = eliminant["ideal_combination"]
    binding_id = ideal["equation_source_binding_id"]
    require(binding_id in binding_by_id, "ideal combination source binding missing")
    source_generators = resolve_json_pointer(
        binding_by_id[binding_id], ideal["equation_source_pointer"]
    )
    source_variable = resolve_json_pointer(
        binding_by_id[binding_id], ideal["equation_variable_pointer"]
    )
    source_chart_key_sha256_allowlist = resolve_json_pointer(
        binding_by_id[binding_id], ideal["equation_chart_key_sha256_allowlist_pointer"]
    )
    require(source_variable == eliminant["variable"], "ideal variable drifts from pinned equation source")
    require(
        isinstance(source_chart_key_sha256_allowlist, list)
        and len(source_chart_key_sha256_allowlist) == len(set(source_chart_key_sha256_allowlist))
        and canonical_hash(chart["canonical_key"]) in source_chart_key_sha256_allowlist,
        "ideal equation source is not bound to the canonical chart key",
    )
    require(
        source_generators == ideal["generators_low_to_high"],
        "ideal generators drift from pinned equation source",
    )
    generators = ideal["generators_low_to_high"]
    multipliers = ideal["multipliers_low_to_high"]
    require(len(generators) == len(multipliers), "ideal generator/multiplier count drift")
    combination: list[int] = []
    for generator, multiplier in zip(generators, multipliers, strict=True):
        combination = add_poly(combination, multiply_poly(generator, multiplier, p), p)
    require(
        combination == normalize_poly(coeffs, p),
        "printed ideal combination does not equal the eliminant",
    )

    roots = eliminant["root_set"]
    require(roots == sorted(set(roots)), "root set must be sorted and exact")
    require(eliminant["root_count"] == len(roots), "root count drift")
    for root in roots:
        require(0 <= root < p, "root outside base field")
        value = sum(coefficient * pow(root, index, p) for index, coefficient in enumerate(coeffs)) % p
        require(value == 0, "listed eliminant root is not a root")
    if eliminant["certificate_mode"] == "EXACT_BASE_FIELD_ENUMERATION":
        require(p <= 10_000, "large-field exact enumeration requires a future factor/gcd certificate")
        exact = [
            root
            for root in range(p)
            if sum(coefficient * pow(root, index, p) for index, coefficient in enumerate(coeffs)) % p == 0
        ]
        require(roots == exact, "root set is not the exact base-field root set")
        return len(roots)
    require(roots == [] and eliminant["root_count"] == 0, "degree-bound mode must not claim enumerated roots")
    return eliminant["degree"]


def validate_terminals_and_coverage(
    artifact: dict[str, Any],
    binding_by_id: dict[str, dict[str, Any]],
) -> None:
    policy_order = artifact["owner_policy"]["order"]
    fallback_owner = artifact["owner_policy"]["fallback_unpaid_owner_id"]
    require(artifact["owner_policy"]["terminal_order_frozen"], "owner order is not frozen")
    require(len(policy_order) == len(set(policy_order)), "duplicate owner in policy")
    require(fallback_owner == policy_order[-1], "unpaid fallback is not the final frozen owner")
    charts = artifact["charts"]
    chart_ids = [chart["chart_id"] for chart in charts]
    require(len(chart_ids) == len(set(chart_ids)), "duplicate chart id")
    canonical_keys = [canonical_bytes(chart["canonical_key"]) for chart in charts]
    require(len(canonical_keys) == len(set(canonical_keys)), "duplicate canonical chart assignment")

    counts = {"NAMED_PAID_OWNER": 0, "CERTIFIED_SLOPE_ELIMINANT": 0, "UNPAID_PRIMITIVE": 0}
    eliminant_charge = 0
    charge_by_id = {
        charge["charge_id"]: charge for charge in artifact["ledger"]["charges"]
    }
    p = artifact["row"]["field"]["characteristic_p"]
    for chart in charts:
        gates = chart["gates"]
        require([gate["owner_id"] for gate in gates] == policy_order, f"{chart['chart_id']}: owner order drift")
        winner = first_eligible(gates)
        terminal = chart["terminal"]
        counts[terminal["kind"]] += 1
        if terminal["kind"] == "UNPAID_PRIMITIVE":
            require(winner == fallback_owner, f"{chart['chart_id']}: unpaid is not first match")
            require(
                terminal["owner_id"] is None
                and terminal["charge_id"] is None
                and terminal["numeric_charge"] is None
                and terminal["eliminant"] is None,
                f"{chart['chart_id']}: unpaid terminal carries a payment",
            )
        elif terminal["kind"] == "NAMED_PAID_OWNER":
            require(terminal["owner_id"] == winner, f"{chart['chart_id']}: paid owner is not first match")
            require(terminal["owner_id"] in policy_order, "unregistered paid owner")
            require(terminal["owner_id"] != fallback_owner, "unpaid fallback cannot be a paid owner")
            require(terminal["charge_id"] in charge_by_id, "paid owner has no registered global charge")
            require(
                charge_by_id[terminal["charge_id"]]["owner_id"] == terminal["owner_id"],
                "paid terminal references another owner's charge",
            )
            require(terminal["numeric_charge"] is None, "global owner cost must not be multiplied per chart")
            require(terminal["eliminant"] is None, "paid-owner terminal also carries eliminant")
            require(all(chart["localization"].values()), "paid owner lacks a localization gate")
        else:
            require(terminal["owner_id"] is None and terminal["charge_id"] is None, "eliminant terminal carries owner")
            require(terminal["eliminant"] is not None, "eliminant terminal missing eliminant")
            require(winner == fallback_owner, "eliminant bypasses an earlier eligible owner")
            require(all(chart["localization"].values()), "eliminant lacks a localization gate")
            safe_charge = validate_eliminant(
                terminal["eliminant"], p, chart, binding_by_id
            )
            require(
                terminal["numeric_charge"] == safe_charge,
                "eliminant terminal charge does not match its safe certificate mode",
            )
            eliminant_charge += safe_charge

    families = artifact["compressed_chart_families"]
    family_ids = [family["family_id"] for family in families]
    require(len(family_ids) == len(set(family_ids)), "duplicate compressed family id")
    for family in families:
        require(family["h_end"] >= family["h_start"], "compressed family has reversed range")
        require(
            family["index_count"] == family["h_end"] - family["h_start"] + 1,
            "compressed family index count drift",
        )
        require(set(family["source_binding_ids"]) <= set(binding_by_id), "family source binding missing")
        require(family["chart_adapter_status"] == "UNPROVEN", "v1 compressed families are capacity-only")
        require(family["terminal"] == terminal_unpaid(), "capacity family must fail closed to unpaid")

    coverage = artifact["coverage"]
    represented = len(charts)
    require(coverage["represented_units"] == represented, "represented unit count drift")
    require(
        coverage["expected_units"] == coverage["represented_units"] + coverage["missing_units"],
        "coverage arithmetic drift",
    )
    if coverage["unit_kind"] == "EXPLICIT_CHART":
        require(not families, "explicit-chart coverage cannot count compressed capacity slots")
    else:
        require(not charts, "capacity-index coverage cannot contain explicit charts")
        require(coverage["represented_units"] == 0, "capacity indices cannot be represented as charts")
        require(
            coverage["expected_units"] == sum(family["index_count"] for family in families),
            "capacity coverage does not equal its namespace sizes",
        )
        require(
            coverage["missing_units"] == coverage["expected_units"],
            "capacity namespaces must remain entirely unrepresented in v1",
        )
    require(coverage["paid_count"] == counts["NAMED_PAID_OWNER"], "paid terminal count drift")
    require(coverage["eliminant_count"] == counts["CERTIFIED_SLOPE_ELIMINANT"], "eliminant count drift")
    require(coverage["unpaid_count"] == counts["UNPAID_PRIMITIVE"], "unpaid terminal count drift")
    if coverage["scope_complete"]:
        require(coverage["missing_units"] == 0, "scope complete with missing units")
    if coverage["row_complete"]:
        require(
            artifact["artifact_kind"] == "DEPLOYED_COMPLETE_MANIFEST"
            and artifact["status"] == "COMPLETE",
            "row completeness requires a complete deployed manifest",
        )
        require(coverage["scope_complete"], "row complete without scope completeness")
        require(coverage["coverage_status"] == "ROW_COMPLETE", "row complete with bounded status")
        require(
            artifact["quantifier_scope"]["uniformity"] == "PROVED_ROW_UNIFORM",
            "bounded quantifier scope cannot be marked row complete",
        )
        require(not artifact["quantifier_scope"]["excluded_scopes"], "row complete with excluded scopes")
        require(not coverage["uncovered_scopes"], "row complete with uncovered chart scopes")
        require(coverage["unit_kind"] == "EXPLICIT_CHART", "row complete requires explicit charts")
        require(coverage["unpaid_count"] == 0, "row complete contains unpaid charts")

    ledger = artifact["ledger"]
    if counts["CERTIFIED_SLOPE_ELIMINANT"]:
        require(
            ledger["eliminant_aggregation_mode"] == "DISJOINT_CHART_SUM",
            "eliminants require the v1 disjoint-chart aggregation",
        )
        require(
            ledger["eliminant_charge"] is not None
            and int(ledger["eliminant_charge"]) == eliminant_charge,
            "eliminant ledger charge drift",
        )
    elif ledger["eliminant_aggregation_mode"] == "NONE_CONTROL":
        require(ledger["eliminant_charge"] == "0", "empty control eliminant charge drift")
    else:
        require(ledger["eliminant_charge"] is None, "open eliminant ledger prints a charge")


def validate_ledger(artifact: dict[str, Any], binding_by_id: dict[str, dict[str, Any]]) -> None:
    ledger = artifact["ledger"]
    charges = ledger["charges"]
    registered_charges = {
        "gf19-l1-442233-control": [],
        "koalabear-mca-A1116048": [
            {
                "charge_id": "kb-base-generated-image-cell-cover",
                "owner_id": "base_generated_field_collision",
                "amount": str(GENERATED_CHARGE),
                "scope": "IMPORTED_GLOBAL_ONCE",
                "source_binding_id": "kb-first-match-packet",
                "source_claim_pointer": "/deployed_arithmetic/B_gen_t_times_p",
            },
            {
                "charge_id": "kb-terminal-quotient-raw",
                "owner_id": "quotient_periodic_or_divisor_stabilized",
                "amount": str(QUOTIENT_TERMINAL_CHARGE),
                "scope": "IMPORTED_GLOBAL_ONCE",
                "source_binding_id": "kb-first-match-packet",
                "source_claim_pointer": "/deployed_arithmetic/terminal_quotient_raw_paid_cost",
            },
        ],
    }
    row_id = artifact["row"]["row_id"]
    require(row_id in registered_charges, "row has no registered global-charge set")
    require(
        charges == registered_charges[row_id],
        "global charges drift from the row-specific exact registry",
    )
    ids = [charge["charge_id"] for charge in charges]
    require(len(ids) == len(set(ids)), "duplicate ledger charge id")
    semantic_keys = [
        (
            charge["owner_id"],
            charge["scope"],
            charge["source_binding_id"],
            charge["source_claim_pointer"],
        )
        for charge in charges
    ]
    require(len(semantic_keys) == len(set(semantic_keys)), "duplicate semantic global charge")
    source_claim_keys = [
        (charge["source_binding_id"], charge["source_claim_pointer"])
        for charge in charges
    ]
    require(len(source_claim_keys) == len(set(source_claim_keys)), "source claim charged more than once")
    charge_owners = [charge["owner_id"] for charge in charges]
    require(
        len(charge_owners) == len(set(charge_owners)),
        "v1 permits at most one global charge per owner",
    )
    require(ledger["charge_ids_unique"], "charge uniqueness flag is false")
    owners = set(artifact["owner_policy"]["order"])
    for charge in charges:
        require(charge["owner_id"] in owners, "charge owner is outside frozen policy")
        require(charge["source_binding_id"] in binding_by_id, "charge source binding missing")
        source_value = resolve_json_pointer(
            binding_by_id[charge["source_binding_id"]],
            charge["source_claim_pointer"],
        )
        require(type(source_value) is int and source_value >= 0, "charge source claim is not a nonnegative integer")
        require(int(charge["amount"]) == source_value, "charge amount drifts from source claim")
    if charges:
        require(ledger["U_paid"] is not None, "nonempty charge ledger has null U_paid")
    if ledger["U_paid"] is not None:
        require(int(ledger["U_paid"]) == sum(int(charge["amount"]) for charge in charges), "U_paid charge sum drift")

    status = ledger["inequality_status"]
    terms = [ledger["U_paid"], ledger["U_Q"], ledger["U_A"]]
    for name in ("U_paid", "U_Q", "U_A", "lhs", "B_star", "eliminant_charge"):
        value = ledger[name]
        if value is not None:
            require(int(value) >= 0, f"{name} must be nonnegative")
    if ledger["U_A"] is not None and ledger["eliminant_charge"] is not None:
        require(
            int(ledger["U_A"]) >= int(ledger["eliminant_charge"]),
            "U_A undercounts certified eliminants",
        )
    if status in {"PROVED_PASS", "PROVED_FAIL"}:
        require(
            artifact["artifact_kind"] == "DEPLOYED_COMPLETE_MANIFEST"
            and artifact["status"] == "COMPLETE",
            "proved inequality requires a complete deployed manifest",
        )
        require(artifact["coverage"]["row_complete"], "proved inequality requires row completeness")
        require(ledger["ledger_consequence"], "proved inequality without ledger consequence")
        require(all(term is not None for term in terms), "proved inequality has null terms")
        total = sum(int(term) for term in terms if term is not None)
        require(ledger["lhs"] is not None and int(ledger["lhs"]) == total, "lhs sum drift")
        if status == "PROVED_PASS":
            require(total <= int(ledger["B_star"]), "false PROVED_PASS")
        else:
            require(total > int(ledger["B_star"]), "false PROVED_FAIL")
    else:
        require(not ledger["ledger_consequence"], "open/control ledger claims consequence")
        require(ledger["lhs"] is None, "open/control ledger must not print a final lhs")
    if status == "CONTROL_ONLY_NO_LEDGER_CONSEQUENCE":
        require(artifact["artifact_kind"] == "CONTROL_FIXTURE", "control status on deployed manifest")
    if status == "UNDECIDED_OPEN_COMPONENTS":
        require(any(term is None for term in terms), "undecided ledger has every term")


def validate_gf19_specific(artifact: dict[str, Any]) -> None:
    require(
        (artifact["artifact_kind"], artifact["status"])
        in {
            ("CONTROL_FIXTURE", "AUDIT"),
            ("DEPLOYED_COMPLETE_MANIFEST", "COMPLETE"),
        },
        "GF19 artifact/status pairing drift",
    )
    require(artifact["owner_policy"]["order"] == L1_OWNER_ORDER, "GF19 owner policy drift")
    row = artifact["row"]
    require(
        (
            row["field"]["characteristic_p"],
            row["field"]["extension_degree"],
            row["n"],
            row["k"],
            row["agreement_A"],
            row["error_count_j"],
            row["syndrome_depth_t"],
        )
        == (19, 1, 18, 5, 8, 10, 3),
        "GF19 row constants drift",
    )
    profile = artifact["row"]["profile"]
    require(
        (profile["ell"], profile["d"], profile["r"], profile["t"], profile["a_i"], profile["G2"], profile["GR"])
        == (4, 4, 2, 2, [3, 3], 2, 3),
        "GF19 profile drift",
    )
    assignments = gf19_assignments()
    expected_assignments = [entry[0] for entry in assignments]
    expected_masks = [mask(entry[2]) for entry in assignments]
    require(len(expected_assignments) == 48, "GF19 enumeration size drift")
    require(canonical_hash(expected_assignments) == EXPECTED_GF_ASSIGNMENT_HASH, "GF19 assignment hash drift")
    require(canonical_hash(expected_masks) == EXPECTED_GF_MASK_HASH, "GF19 mask hash drift")
    actual_assignments = [
        [
            chart["support_pattern"]["background_support"],
            *chart["support_pattern"]["petal_supports"],
        ]
        for chart in artifact["charts"]
    ]
    actual_masks = [chart["support_pattern"]["selected_support_mask"] for chart in artifact["charts"]]
    require(actual_assignments == expected_assignments, "GF19 canonical assignment list drift")
    require(actual_masks == expected_masks, "GF19 mask list drift")
    require(len(set(actual_masks)) == 48, "GF19 duplicate support mask")
    for chart in artifact["charts"]:
        selected_mask = chart["support_pattern"]["selected_support_mask"]
        gates, expected_stabilizer, expected_scales = gf19_gate_derivation(selected_mask)
        require(
            expected_stabilizer == 1,
            f"{chart['chart_id']}: nontrivial cyclic exponent-shift stabilizer",
        )
        require(
            chart["support_pattern"]["stabilizer_order"] == expected_stabilizer,
            "stored cyclic stabilizer drift",
        )
        require(
            chart["support_pattern"]["complete_fibre_scales"] == expected_scales,
            "stored cyclic quotient scales drift",
        )
        require(chart["gates"] == gates, f"{chart['chart_id']}: derived gate record drift")
    occupancies = [tuple(len(petal) for petal in assignment[1:]) for assignment in actual_assignments]
    require(
        {occupancy: occupancies.count(occupancy) for occupancy in set(occupancies)}
        == {(3, 3, 0): 16, (3, 0, 3): 16, (0, 3, 3): 16},
        "GF19 occupancy histogram drift",
    )
    require(artifact["coverage"]["canonical_assignment_sha256"] == EXPECTED_GF_ASSIGNMENT_HASH, "stored assignment digest drift")
    require(artifact["coverage"]["mask_list_sha256"] == EXPECTED_GF_MASK_HASH, "stored mask digest drift")
    require(int(artifact["ledger"]["U_A"]) == 48 * 19**2 == 17_328, "GF19 control charge drift")


def validate_kb_source_packet() -> None:
    packet = load_json(ROOT / KB_PACKET)
    branches = packet["first_match_branches"]
    require([branch["branch"] for branch in branches] == M1_OWNER_ORDER, "source first-match order drift")
    generated = branches[6]
    require(generated["order"] == 7, "source generated-owner order drift")
    require(generated["status"] == "PROVED_IMAGE_CELL_COVER", "source generated-owner status drift")
    require(generated["row_count_bound_R"] == T_KB, "source row-count bound drift")
    require(generated["base_field_slope_values"] == P_KB, "source base-slope count drift")
    require(generated["cost"] == GENERATED_CHARGE, "source generated charge drift")
    require(generated["not_a_raw_support_bound"] is True, "source support warning drift")


def validate_kb_specific(artifact: dict[str, Any]) -> None:
    require(artifact["artifact_kind"] == "DEPLOYED_PARTIAL_MANIFEST", "KB kind drift")
    require(artifact["owner_policy"]["order"] == M1_OWNER_ORDER, "KB owner policy drift")
    row = artifact["row"]
    require(
        (
            row["field"]["characteristic_p"],
            row["field"]["extension_degree"],
            row["n"],
            row["k"],
            row["agreement_A"],
            row["error_count_j"],
            row["syndrome_depth_t"],
            row["prefix_depth_w"],
            row["kernel_dimension_lower_bound"],
            row["deficiency_one"],
        )
        == (P_KB, E_KB, N_KB, K_KB, A_KB, J_KB, T_KB, W_KB, KERNEL_KB, False),
        "KB row constants drift",
    )
    require(KERNEL_KB == 913_633, "KB kernel arithmetic drift")
    require(B_STAR_KB == 274_980_728_111_395_087, "KB B_star drift")
    require(GENERATED_CHARGE == 143_763_024_447_376, "KB generated charge drift")
    require(U_PAID_KB == 143_763_495_894_416, "KB U_paid drift")
    families = artifact["compressed_chart_families"]
    require(len(families) == 1, "KB must contain one bounded candidate family")
    family = families[0]
    require(family["h_start"] == 0 and family["h_end"] == W_KB, "KB h range drift")
    require(family["index_count"] == T_KB, "KB capacity count drift")
    require(family["chart_adapter_status"] == "UNPROVEN", "KB adapter overclaim")
    require(family["candidate_owner_id"] == "base_generated_field_collision", "KB candidate owner drift")
    require(int(family["per_index_image_cap"]) == P_KB, "KB per-index cap drift")
    require(int(family["family_image_cap"]) == GENERATED_CHARGE, "KB family cap drift")
    require(family["finite_pivot_nonzero"], "KB source finite-pivot hypothesis drift")
    require(family["noncontainment_localized"], "KB source noncontainment hypothesis drift")
    require(family["earlier_pivots_zero_by_definition"], "KB first-nonzero-row definition drift")
    require(all(family["gate_scope"].values()), "KB source gate-scope drift")
    require(family["terminal"] == terminal_unpaid(), "KB family must remain unpaid")
    require(artifact["coverage"]["unit_kind"] == "CAPACITY_INDEX_NOT_CHART", "KB coverage unit overclaim")
    require(artifact["coverage"]["represented_units"] == 0, "KB cannot represent charts before adapter")
    require(artifact["coverage"]["missing_units"] == T_KB, "KB missing-capacity count drift")
    require(artifact["ledger"]["U_Q"] is None and artifact["ledger"]["U_A"] is None, "KB open terms overclaimed")
    validate_kb_source_packet()


def validate_manifest(artifact: dict[str, Any], schema: dict[str, Any]) -> None:
    assert_closed_object_schemas(schema)
    validate_schema_value(artifact, schema, schema)
    require(artifact["schema"] == SCHEMA_ID, "schema id drift")
    require(
        (artifact["artifact_kind"], artifact["status"])
        in {
            ("CONTROL_FIXTURE", "AUDIT"),
            ("DEPLOYED_PARTIAL_MANIFEST", "PARTIAL"),
            ("DEPLOYED_COMPLETE_MANIFEST", "COMPLETE"),
        },
        "artifact kind/status pairing drift",
    )
    require(artifact["payload_sha256"] == payload_hash(artifact), "payload hash drift")
    validate_row_arithmetic(artifact)
    binding_by_id = validate_source_bindings(artifact)
    validate_terminals_and_coverage(artifact, binding_by_id)
    validate_ledger(artifact, binding_by_id)
    if artifact["row"]["row_id"] == "gf19-l1-442233-control":
        validate_gf19_specific(artifact)
    elif artifact["row"]["row_id"] == "koalabear-mca-A1116048":
        validate_kb_specific(artifact)
    else:
        raise VerificationError("unregistered row_id")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant rejected: {value}")


def parse_json_text(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_json_constant,
    )
    require(isinstance(value, dict), f"top-level JSON value must be an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    return parse_json_text(path.read_text(encoding="utf-8"), str(path))


def check_stored(schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    expected = [(GF19_PATH, build_gf19_manifest()), (KB_PATH, build_kb_manifest())]
    loaded = []
    for path, fresh in expected:
        require(path.is_file(), f"missing stored certificate {path.relative_to(ROOT)}")
        stored = load_json(path)
        validate_manifest(stored, schema)
        require(stored == fresh, f"stored certificate drift: {path.relative_to(ROOT)}")
        loaded.append(stored)
    return loaded[0], loaded[1]


def render_json(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=False) + "\n"


def write_artifacts() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    GF19_PATH.write_text(render_json(build_gf19_manifest()), encoding="utf-8")
    KB_PATH.write_text(render_json(build_kb_manifest()), encoding="utf-8")


def rehash(artifact: dict[str, Any]) -> None:
    artifact["payload_sha256"] = payload_hash(artifact)


def set_nested(artifact: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = artifact
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def synthetic_eliminant_control(
    base: dict[str, Any],
    *,
    mode: str = "EXACT_BASE_FIELD_ENUMERATION",
) -> dict[str, Any]:
    candidate = copy.deepcopy(base)
    chart = candidate["charts"][0]
    for key in chart["localization"]:
        chart["localization"][key] = True
    chart["terminal"] = {
        "kind": "CERTIFIED_SLOPE_ELIMINANT",
        "owner_id": None,
        "charge_id": None,
        "numeric_charge": 1,
        "eliminant": {
            "variable": "lambda",
            "root_space_id": f"{chart['chart_id']}::lambda",
            "certificate_mode": mode,
            "coefficients_low_to_high": [-1, 1],
            "degree": 1,
            "nonzero": True,
            "ideal_combination": {
                "equation_source_binding_id": "eliminant-control-equations",
                "equation_source_pointer": "/systems/x_minus_1/generators_low_to_high",
                "equation_variable_pointer": "/systems/x_minus_1/variable",
                "equation_chart_key_sha256_allowlist_pointer": "/chart_key_sha256_allowlist",
                "generators_low_to_high": [[-1, 1]],
                "multipliers_low_to_high": [[1]],
            },
            "root_set": [1] if mode == "EXACT_BASE_FIELD_ENUMERATION" else [],
            "root_count": 1 if mode == "EXACT_BASE_FIELD_ENUMERATION" else 0,
        },
    }
    candidate["coverage"]["eliminant_count"] = 1
    candidate["coverage"]["unpaid_count"] = 47
    candidate["ledger"]["eliminant_aggregation_mode"] = "DISJOINT_CHART_SUM"
    candidate["ledger"]["eliminant_charge"] = "1"
    rehash(candidate)
    return candidate


def synthetic_complete_control(base: dict[str, Any]) -> dict[str, Any]:
    candidate = synthetic_eliminant_control(base)
    template = copy.deepcopy(candidate["charts"][0]["terminal"])
    for chart in candidate["charts"]:
        for key in chart["localization"]:
            chart["localization"][key] = True
        chart["terminal"] = copy.deepcopy(template)
        chart["terminal"]["eliminant"]["root_space_id"] = (
            f"{chart['chart_id']}::lambda"
        )
    candidate["artifact_kind"] = "DEPLOYED_COMPLETE_MANIFEST"
    candidate["status"] = "COMPLETE"
    candidate["quantifier_scope"]["uniformity"] = "PROVED_ROW_UNIFORM"
    candidate["quantifier_scope"]["excluded_scopes"] = []
    candidate["coverage"]["row_complete"] = True
    candidate["coverage"]["coverage_status"] = "ROW_COMPLETE"
    candidate["coverage"]["uncovered_scopes"] = []
    candidate["coverage"]["eliminant_count"] = 48
    candidate["coverage"]["unpaid_count"] = 0
    candidate["ledger"]["ledger_consequence"] = True
    candidate["ledger"]["U_Q"] = "0"
    candidate["ledger"]["lhs"] = "17328"
    candidate["ledger"]["inequality_status"] = "PROVED_FAIL"
    candidate["ledger"]["eliminant_charge"] = "48"
    rehash(candidate)
    return candidate


def synthetic_m1_explicit_terminal_control(
    kb: dict[str, Any],
    gf: dict[str, Any],
    *,
    paid: bool,
) -> dict[str, Any]:
    """Build an in-memory M1 chart to exercise the M1 fallback vocabulary."""
    candidate = copy.deepcopy(kb)
    chart = copy.deepcopy(gf["charts"][0])
    chart["chart_id"] = "m1-explicit-terminal-control"
    chart["canonical_key"].update(
        {
            "A": A_KB,
            "quantifier_scope": "SYNTHETIC_M1_TERMINAL_CONTROL_ONLY",
            "locator_chart_id": "synthetic-m1-locator",
            "patch": "synthetic-terminal-semantics",
            "h": 0,
        }
    )
    chart["gates"] = [
        {
            "owner_id": owner_id,
            "eligible": owner_id
            in (
                {"base_generated_field_collision", "primitive_qfin_residual"}
                if paid
                else {"primitive_qfin_residual"}
            ),
            "evidence": "synthetic M1 terminal-semantics control",
        }
        for owner_id in M1_OWNER_ORDER
    ]
    if paid:
        for key in chart["localization"]:
            chart["localization"][key] = True
        chart["terminal"] = {
            "kind": "NAMED_PAID_OWNER",
            "owner_id": "base_generated_field_collision",
            "charge_id": "kb-base-generated-image-cell-cover",
            "numeric_charge": None,
            "eliminant": None,
        }
    else:
        chart["terminal"] = terminal_unpaid()
    candidate["charts"] = [chart]
    candidate["compressed_chart_families"] = []
    candidate["coverage"].update(
        {
            "scope_complete": False,
            "unit_kind": "EXPLICIT_CHART",
            "expected_units": 1,
            "represented_units": 1,
            "missing_units": 0,
            "paid_count": int(paid),
            "eliminant_count": 0,
            "unpaid_count": int(not paid),
            "coverage_status": "BOUNDED_FAMILY_ONLY",
        }
    )
    return candidate


def mutation_cases(gf: dict[str, Any], kb: dict[str, Any]) -> list[tuple[str, dict[str, Any], bool]]:
    cases: list[tuple[str, dict[str, Any], bool]] = []

    def changed(label: str, base: dict[str, Any], path: tuple[Any, ...], value: Any, *, hash_it: bool = True) -> None:
        candidate = copy.deepcopy(base)
        set_nested(candidate, path, value)
        if hash_it:
            rehash(candidate)
        cases.append((label, candidate, hash_it))

    changed("wrong-extension-field", kb, ("row", "field", "extension_degree"), 5)
    changed("wrong-denominator", kb, ("row", "field", "sampling_denominator"), str(DENOMINATOR + 1))
    changed("wrong-j", kb, ("row", "error_count_j"), J_KB + 1)
    changed("wrong-t", kb, ("row", "syndrome_depth_t"), T_KB + 1)
    changed("wrong-w", kb, ("row", "prefix_depth_w"), W_KB + 1)
    changed("false-deficiency-one", kb, ("row", "deficiency_one"), True)
    changed("missing-finite-pivot", kb, ("compressed_chart_families", 0, "finite_pivot_nonzero"), False)

    duplicate = copy.deepcopy(gf)
    duplicate["charts"][1]["canonical_key"] = copy.deepcopy(duplicate["charts"][0]["canonical_key"])
    rehash(duplicate)
    cases.append(("duplicate-chart", duplicate, True))

    order_swap = copy.deepcopy(gf)
    order_swap["owner_policy"]["order"][0:2] = reversed(order_swap["owner_policy"]["order"][0:2])
    rehash(order_swap)
    cases.append(("owner-order-swap", order_swap, True))

    later_owner = copy.deepcopy(gf)
    later_owner["charts"][0]["gates"][0]["eligible"] = True
    rehash(later_owner)
    cases.append(("later-owner-before-earlier", later_owner, True))

    def synthetic_paid(base: dict[str, Any]) -> dict[str, Any]:
        candidate = copy.deepcopy(base)
        candidate["ledger"]["charges"] = [
            {
                "charge_id": "synthetic-global",
                "owner_id": "PERIODIC_SUPPORT",
                "amount": "1",
                "scope": "GLOBAL_ONCE",
                "source_binding_id": "eliminant-control-equations",
                "source_claim_pointer": "/charges/synthetic_global",
            }
        ]
        candidate["ledger"]["U_paid"] = "1"
        candidate["charts"][0]["gates"][0]["eligible"] = True
        candidate["charts"][0]["terminal"] = {
            "kind": "NAMED_PAID_OWNER",
            "owner_id": "PERIODIC_SUPPORT",
            "charge_id": "synthetic-global",
            "numeric_charge": None,
            "eliminant": None,
        }
        candidate["coverage"]["paid_count"] = 1
        candidate["coverage"]["unpaid_count"] = 47
        return candidate

    paid_without_localization = synthetic_paid(gf)
    rehash(paid_without_localization)
    cases.append(("paid-owner-missing-localization", paid_without_localization, True))

    paid_per_chart = synthetic_paid(gf)
    for key in paid_per_chart["charts"][0]["localization"]:
        paid_per_chart["charts"][0]["localization"][key] = True
    paid_per_chart["charts"][0]["terminal"]["numeric_charge"] = 1
    rehash(paid_per_chart)
    cases.append(("global-charge-multiplied-per-chart", paid_per_chart, True))

    eliminant_bypasses_owner = synthetic_eliminant_control(gf)
    eliminant_bypasses_owner["charts"][0]["gates"][0]["eligible"] = True
    rehash(eliminant_bypasses_owner)
    cases.append(("eliminant-bypasses-first-owner", eliminant_bypasses_owner, True))

    eliminant_missing_localization = synthetic_eliminant_control(gf)
    eliminant_missing_localization["charts"][0]["localization"]["finite_pivot"] = False
    rehash(eliminant_missing_localization)
    cases.append(("eliminant-missing-localization", eliminant_missing_localization, True))

    zero_eliminant = synthetic_eliminant_control(gf)
    zero_eliminant["charts"][0]["terminal"]["eliminant"]["coefficients_low_to_high"] = [0]
    zero_eliminant["charts"][0]["terminal"]["eliminant"]["degree"] = 0
    rehash(zero_eliminant)
    cases.append(("zero-eliminant", zero_eliminant, True))

    wrong_degree = synthetic_eliminant_control(gf)
    wrong_degree["charts"][0]["terminal"]["eliminant"]["degree"] = 2
    rehash(wrong_degree)
    cases.append(("wrong-eliminant-degree", wrong_degree, True))

    bad_ideal_source = synthetic_eliminant_control(gf)
    bad_ideal_source["charts"][0]["terminal"]["eliminant"]["ideal_combination"]["generators_low_to_high"] = [[1, 1]]
    rehash(bad_ideal_source)
    cases.append(("ideal-generator-source-drift", bad_ideal_source, True))

    bad_ideal_identity = synthetic_eliminant_control(gf)
    bad_ideal_identity["charts"][0]["terminal"]["eliminant"]["ideal_combination"]["multipliers_low_to_high"] = [[2]]
    rehash(bad_ideal_identity)
    cases.append(("invalid-ideal-combination", bad_ideal_identity, True))

    wrong_root_space = synthetic_eliminant_control(gf)
    wrong_root_space["charts"][0]["terminal"]["eliminant"]["root_space_id"] = "shared::lambda"
    rehash(wrong_root_space)
    cases.append(("cross-chart-root-space", wrong_root_space, True))

    wrong_ideal_variable = synthetic_eliminant_control(gf)
    wrong_ideal_variable["charts"][0]["terminal"]["eliminant"]["variable"] = "mu"
    wrong_ideal_variable["charts"][0]["terminal"]["eliminant"]["root_space_id"] = (
        f"{wrong_ideal_variable['charts'][0]['chart_id']}::mu"
    )
    rehash(wrong_ideal_variable)
    cases.append(("ideal-variable-source-drift", wrong_ideal_variable, True))

    wrong_ideal_chart = synthetic_eliminant_control(gf)
    wrong_ideal_chart["charts"][0]["canonical_key"]["h"] = 999
    rehash(wrong_ideal_chart)
    cases.append(("ideal-chart-key-source-drift", wrong_ideal_chart, True))

    undercounted_chart_sum = synthetic_eliminant_control(gf)
    undercounted_chart_sum["charts"][1]["terminal"] = copy.deepcopy(
        undercounted_chart_sum["charts"][0]["terminal"]
    )
    for key in undercounted_chart_sum["charts"][1]["localization"]:
        undercounted_chart_sum["charts"][1]["localization"][key] = True
    undercounted_chart_sum["charts"][1]["terminal"]["eliminant"]["root_space_id"] = (
        f"{undercounted_chart_sum['charts'][1]['chart_id']}::lambda"
    )
    undercounted_chart_sum["coverage"]["eliminant_count"] = 2
    undercounted_chart_sum["coverage"]["unpaid_count"] = 46
    rehash(undercounted_chart_sum)
    cases.append(("undercounted-disjoint-chart-sum", undercounted_chart_sum, True))

    duplicate_charge = copy.deepcopy(kb)
    duplicate_charge["ledger"]["charges"].append(copy.deepcopy(duplicate_charge["ledger"]["charges"][0]))
    duplicate_charge["ledger"]["U_paid"] = str(U_PAID_KB + GENERATED_CHARGE)
    rehash(duplicate_charge)
    cases.append(("duplicate-charge", duplicate_charge, True))

    semantic_duplicate = copy.deepcopy(kb)
    second_charge = copy.deepcopy(semantic_duplicate["ledger"]["charges"][0])
    second_charge["charge_id"] = "same-global-charge-new-id"
    semantic_duplicate["ledger"]["charges"].append(second_charge)
    semantic_duplicate["ledger"]["U_paid"] = str(U_PAID_KB + GENERATED_CHARGE)
    rehash(semantic_duplicate)
    cases.append(("distinct-id-semantic-double-charge", semantic_duplicate, True))

    alias_duplicate = copy.deepcopy(kb)
    alias_charge = copy.deepcopy(alias_duplicate["ledger"]["charges"][0])
    alias_charge["charge_id"] = "same-owner-alias-pointer"
    alias_charge["source_claim_pointer"] = "/first_match_branches/6/cost"
    alias_duplicate["ledger"]["charges"].append(alias_charge)
    alias_duplicate["ledger"]["U_paid"] = str(U_PAID_KB + GENERATED_CHARGE)
    rehash(alias_duplicate)
    cases.append(("same-owner-alias-pointer-double-charge", alias_duplicate, True))

    cross_owner_alias = copy.deepcopy(kb)
    cross_owner_charge = copy.deepcopy(cross_owner_alias["ledger"]["charges"][0])
    cross_owner_charge["charge_id"] = "cross-owner-alias-pointer"
    cross_owner_charge["owner_id"] = "sparse_sigma_or_sparse_support"
    cross_owner_charge["source_claim_pointer"] = "/first_match_branches/6/cost"
    cross_owner_alias["ledger"]["charges"].append(cross_owner_charge)
    cross_owner_alias["ledger"]["U_paid"] = str(U_PAID_KB + GENERATED_CHARGE)
    rehash(cross_owner_alias)
    cases.append(("cross-owner-alias-pointer-double-charge", cross_owner_alias, True))

    changed(
        "wrong-fallback-owner",
        kb,
        ("owner_policy", "fallback_unpaid_owner_id"),
        "m1_half_turn_or_coefficient_shadow",
    )

    amount_drift = copy.deepcopy(kb)
    amount_drift["ledger"]["charges"][0]["amount"] = str(GENERATED_CHARGE + 1)
    amount_drift["ledger"]["U_paid"] = str(U_PAID_KB + 1)
    rehash(amount_drift)
    cases.append(("charge-source-amount-drift", amount_drift, True))

    adapter_overclaim = copy.deepcopy(kb)
    adapter_overclaim["compressed_chart_families"][0]["chart_adapter_status"] = "PROVED"
    rehash(adapter_overclaim)
    cases.append(("compressed-adapter-overclaim", adapter_overclaim, True))

    changed("unpaid-with-numeric-charge", gf, ("charts", 0, "terminal", "numeric_charge"), 361)
    bounded_complete = copy.deepcopy(gf)
    bounded_complete["artifact_kind"] = "DEPLOYED_COMPLETE_MANIFEST"
    bounded_complete["status"] = "COMPLETE"
    bounded_complete["coverage"]["row_complete"] = True
    bounded_complete["coverage"]["coverage_status"] = "ROW_COMPLETE"
    rehash(bounded_complete)
    cases.append(("row-complete-on-bounded-scope", bounded_complete, True))

    false_pass = synthetic_complete_control(gf)
    false_pass["ledger"]["inequality_status"] = "PROVED_PASS"
    rehash(false_pass)
    cases.append(("false-proved-pass", false_pass, True))

    null_terms = synthetic_complete_control(gf)
    null_terms["ledger"]["U_Q"] = None
    null_terms["ledger"]["lhs"] = None
    rehash(null_terms)
    cases.append(("proved-result-with-null-terms", null_terms, True))

    complete_with_uncovered_scope = synthetic_complete_control(gf)
    complete_with_uncovered_scope["coverage"]["uncovered_scopes"] = ["unpaid extension slopes"]
    rehash(complete_with_uncovered_scope)
    cases.append(("complete-with-uncovered-scope", complete_with_uncovered_scope, True))

    negative_pass = synthetic_complete_control(gf)
    negative_pass["ledger"]["U_Q"] = "-17328"
    negative_pass["ledger"]["lhs"] = "0"
    negative_pass["ledger"]["inequality_status"] = "PROVED_PASS"
    rehash(negative_pass)
    cases.append(("negative-ledger-term", negative_pass, True))

    wrong_cyclic_action = copy.deepcopy(gf)
    wrong_cyclic_action["charts"][0]["support_pattern"]["complete_fibre_scales"] = [2]
    rehash(wrong_cyclic_action)
    cases.append(("wrong-cyclic-quotient-action", wrong_cyclic_action, True))

    hardcoded_gate = copy.deepcopy(gf)
    hardcoded_gate["charts"][0]["gates"][2]["evidence"] = "hardcoded margin"
    rehash(hardcoded_gate)
    cases.append(("owner-gate-derivation-drift", hardcoded_gate, True))

    changed(
        "source-hash-drift",
        kb,
        ("source_bindings", 0, "sha256"),
        "0" * 64,
    )
    changed(
        "source-path-traversal",
        kb,
        ("source_bindings", 0, "path"),
        "../outside.md",
    )
    unknown_key = copy.deepcopy(gf)
    unknown_key["charts"][0]["terminal"]["unexpected"] = True
    rehash(unknown_key)
    cases.append(("unknown-nested-key", unknown_key, True))

    bool_integer = copy.deepcopy(gf)
    bool_integer["row"]["n"] = True
    rehash(bool_integer)
    cases.append(("boolean-integer-alias", bool_integer, True))
    changed("payload-hash-drift", gf, ("status",), "PARTIAL", hash_it=False)
    return cases


def tamper_selftest(schema: dict[str, Any]) -> int:
    gf = build_gf19_manifest()
    kb = build_kb_manifest()
    validate_manifest(gf, schema)
    validate_manifest(kb, schema)
    positive_exact = synthetic_eliminant_control(gf, mode="EXACT_BASE_FIELD_ENUMERATION")
    positive_degree = synthetic_eliminant_control(gf, mode="SAFE_DEGREE_BOUND")
    positive_complete = synthetic_complete_control(gf)
    validate_manifest(positive_exact, schema)
    validate_manifest(positive_degree, schema)
    validate_manifest(positive_complete, schema)
    m1_unpaid = synthetic_m1_explicit_terminal_control(kb, gf, paid=False)
    m1_paid = synthetic_m1_explicit_terminal_control(kb, gf, paid=True)
    for candidate in (m1_unpaid, m1_paid):
        validate_schema_value(candidate, schema, schema)
        binding_by_id = validate_source_bindings(candidate)
        validate_terminals_and_coverage(candidate, binding_by_id)
        validate_ledger(candidate, binding_by_id)
    cases = mutation_cases(gf, kb)
    rejected = 0
    for label, candidate, _ in cases:
        try:
            validate_manifest(candidate, schema)
        except (VerificationError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"mutation was not rejected: {label}")
    require(rejected == len(cases), f"expected {len(cases)} mutation rejections, got {rejected}")
    targeted_m1_mutations = []
    missing_paid_localization = copy.deepcopy(m1_paid)
    missing_paid_localization["charts"][0]["localization"]["finite_pivot"] = False
    targeted_m1_mutations.append(("M1 paid owner missing localization", missing_paid_localization))
    multiplied_paid_charge = copy.deepcopy(m1_paid)
    multiplied_paid_charge["charts"][0]["terminal"]["numeric_charge"] = 1
    targeted_m1_mutations.append(("M1 global charge multiplied per chart", multiplied_paid_charge))
    bypassed_first_owner = copy.deepcopy(m1_paid)
    bypassed_first_owner["charts"][0]["gates"][0]["eligible"] = True
    targeted_m1_mutations.append(("M1 paid owner bypasses first match", bypassed_first_owner))
    wrong_charge_owner = copy.deepcopy(m1_paid)
    wrong_charge_owner["charts"][0]["terminal"]["charge_id"] = "kb-terminal-quotient-raw"
    targeted_m1_mutations.append(("M1 paid-owner/charge-owner mismatch", wrong_charge_owner))
    paid_fallback = copy.deepcopy(m1_unpaid)
    paid_fallback["charts"][0]["terminal"] = {
        "kind": "NAMED_PAID_OWNER",
        "owner_id": "primitive_qfin_residual",
        "charge_id": "kb-base-generated-image-cell-cover",
        "numeric_charge": None,
        "eliminant": None,
    }
    for key in paid_fallback["charts"][0]["localization"]:
        paid_fallback["charts"][0]["localization"][key] = True
    targeted_m1_mutations.append(("M1 paid fallback", paid_fallback))
    for label, candidate in targeted_m1_mutations:
        try:
            binding_by_id = validate_source_bindings(candidate)
            validate_terminals_and_coverage(candidate, binding_by_id)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"targeted mutation was not rejected: {label}")
    parser_tampers = [
        ('{"schema":"x","schema":"y"}', "duplicate-key"),
        ('{"value":NaN}', "nonstandard-constant"),
    ]
    for text, label in parser_tampers:
        try:
            parse_json_text(text, label)
        except VerificationError:
            pass
        else:
            raise VerificationError(f"parser mutation was not rejected: {label}")
    binding_by_id = validate_source_bindings(gf)
    large_field_chart = copy.deepcopy(positive_exact["charts"][0])
    large_field_eliminant = copy.deepcopy(large_field_chart["terminal"]["eliminant"])
    large_field_eliminant["coefficients_low_to_high"] = [-1, 0, 1]
    large_field_eliminant["degree"] = 2
    large_field_eliminant["ideal_combination"]["equation_source_pointer"] = (
        "/systems/x2_minus_1/generators_low_to_high"
    )
    large_field_eliminant["ideal_combination"]["equation_variable_pointer"] = (
        "/systems/x2_minus_1/variable"
    )
    large_field_eliminant["ideal_combination"]["generators_low_to_high"] = [[-1, 0, 1]]
    try:
        validate_eliminant(large_field_eliminant, 10_007, large_field_chart, binding_by_id)
    except VerificationError:
        pass
    else:
        raise VerificationError("large-field incomplete root enumeration was not rejected")
    large_degree = copy.deepcopy(large_field_eliminant)
    large_degree["certificate_mode"] = "SAFE_DEGREE_BOUND"
    large_degree["root_set"] = []
    large_degree["root_count"] = 0
    require(
        validate_eliminant(large_degree, 10_007, large_field_chart, binding_by_id) == 2,
        "large-field degree-bound positive control drift",
    )
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite both deterministic JSON artifacts")
    parser.add_argument("--check", action="store_true", help="verify stored artifacts and exact regeneration")
    parser.add_argument("--tamper-selftest", action="store_true", help="run semantic and parser mutation controls")
    args = parser.parse_args()

    schema = load_json(SCHEMA_PATH)
    assert_closed_object_schemas(schema)
    if args.write:
        write_artifacts()
    if args.check:
        gf, kb = check_stored(schema)
        print("CHECK: PASS (2/2 manifests; exact regeneration and source hashes)")
        print(f"GF19: charts={len(gf['charts'])} unpaid={gf['coverage']['unpaid_count']} charge={gf['ledger']['U_A']}")
        print(
            "KB: adapter=%s represented=%d/%d U_paid=%s B_star=%s inequality=%s"
            % (
                kb["compressed_chart_families"][0]["chart_adapter_status"],
                kb["coverage"]["represented_units"],
                kb["coverage"]["expected_units"],
                kb["ledger"]["U_paid"],
                kb["ledger"]["B_star"],
                kb["ledger"]["inequality_status"],
            )
        )
    if args.tamper_selftest:
        rejected = tamper_selftest(schema)
        print(
            f"TAMPER SELFTEST: PASS ({rejected} semantic + 2 parser + "
            "1 large-field omitted-root mutation rejected; exact, degree, complete-manifest, and M1 explicit-terminal positive controls passed)"
        )
    if not (args.write or args.check or args.tamper_selftest):
        gf = build_gf19_manifest()
        kb = build_kb_manifest()
        validate_manifest(gf, schema)
        validate_manifest(kb, schema)
        print("generated manifests validate; use --write, --check, or --tamper-selftest")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
