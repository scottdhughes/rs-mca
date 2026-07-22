#!/usr/bin/env python3
"""Verify the M31 exact all-weight anchor-exchange Padé packet.

The packet records a field-uniform, actual-codeword bijection relative to one
listed anchor.  It also records the sharp route cut that the one-anchor
rank-two module permits every unit residue ``V``, and the fresh-symbol theorem
reducing deployed row closure to boundary anchors.  It deliberately does
*not* claim the remaining M31 incidence bound, any v4 ledger payment, or row
closure.

All proof gates use explicit exceptions and therefore remain active under
``python -O``.  ``--print-template`` emits canonical one-line JSON and this
script never writes the pinned manifest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Sequence


SCHEMA_ID = "rs-mca-m31-all-weight-anchor-exchange-pade-bijection-v1"
THEOREM_ID = "M31_ALL_WEIGHT_ANCHOR_EXCHANGE_PADE_BIJECTION_V1"
ARCHITECTURE_ID = "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
ARTIFACT_KIND = "EXACT_ALL_WEIGHT_CODEWORD_BIJECTION_BOUNDARY_REDUCTION_AND_ROUTE_CUT"
STATUS = "PROVED_EXACT_ALL_WEIGHT_BIJECTION_BOUNDARY_FORCING_GENERIC_V_ROUTE_CUT_ROW_OPEN"

PARENT_COMPILER_ID = "M31_LIST_V4_GLOBAL_COMPLETION_COMPILER_V2"
PARENT_COMPILER_PAYLOAD = "d8acc7accdb9b6720b109af5ececc8569f0822f6550a35241234d99264acbc4e"
SOURCE_ADAPTER_PAYLOAD = "21b213e2b3dfc7f8f99049aea44542ce5ae06dd59b62c10555f9faf5aaa882ce"
CANONICAL_PADE_PAYLOAD = "b23186b09c7017fc80e836b70eea042077a30db22706763d33a98c053a44b0c3"
PARTITION_SHA256 = "816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc"

UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"
ATOM_ORDER = ("U_paid", "U_Q", "U_list_int", "U_ext", "U_new")

P = 2**31 - 1
Q = P**4
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
BUDGET = Q // 2**100
NONANCHOR_BUDGET = BUDGET - 1
U_PAID = 3_730

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_all_weight_anchor_exchange_pade_bijection_v1.schema.json"
DEFAULT_MANIFEST = ROOT / "experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json"

PARENT_COMPILER_PATH = ROOT / "experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json"
SOURCE_ADAPTER_PATH = ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json"
CANONICAL_PADE_PATH = ROOT / "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json"


class VerificationError(RuntimeError):
    """Raised when any exact packet gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (encoded + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity JSON forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_decode(raw: bytes, *, canonical: bool) -> dict[str, Any]:
    require(len(raw) <= 64 * 1024 * 1024, "JSON size cap")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise VerificationError("invalid JSON") from exc
    require(type(value) is dict, "top-level JSON object")
    if canonical:
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def strict_load(path: Path, *, canonical: bool = True) -> dict[str, Any]:
    require(path.exists() and path.is_file(), f"JSON source exists: {path}")
    return strict_decode(path.read_bytes(), canonical=canonical)


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def canonical_repo_path(value: str) -> Path:
    require(type(value) is str and value.isascii(), "source path ASCII string")
    pure = PurePosixPath(value)
    require(not pure.is_absolute(), "source path is relative")
    require(len(pure.parts) > 0, "source path nonempty")
    require("." not in pure.parts and ".." not in pure.parts, "source path canonical")
    resolved = ROOT.joinpath(*pure.parts)
    require(resolved.exists() and resolved.is_file(), f"source exists: {value}")
    require(not resolved.is_symlink(), f"source is not symlink: {value}")
    require(resolved.resolve().is_relative_to(ROOT.resolve()), f"source contained: {value}")
    return resolved


def strict_payload_pin(path: Path, expected: str, label: str) -> dict[str, Any]:
    data = strict_load(path)
    require(type(data.get("payload_sha256")) is str, f"{label}: payload field")
    require(data["payload_sha256"] == expected, f"{label}: payload pin")
    require(payload_sha256(data) == expected, f"{label}: payload seal")
    return data


def source_binding(
    binding_id: str,
    path_text: str,
    role: str,
    scope: str,
    *,
    internal_payload_sha256: str | None = None,
) -> dict[str, Any]:
    path = canonical_repo_path(path_text)
    if internal_payload_sha256 is not None:
        strict_payload_pin(path, internal_payload_sha256, binding_id)
    return {
        "binding_id": binding_id,
        "internal_payload_sha256": internal_payload_sha256,
        "path": path_text,
        "role": role,
        "scope": scope,
        "sha256": sha256_path(path),
    }


def validate_schema() -> None:
    schema = strict_load(SCHEMA_PATH, canonical=False)
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft")
    require(schema.get("$id") == SCHEMA_ID, "schema id")
    require(schema.get("type") == "object", "schema object")
    require(schema.get("additionalProperties") is False, "schema top closed")
    required = {
        "architecture_id",
        "artifact_kind",
        "bijection_contract",
        "boundary_specialization",
        "dependency_contract",
        "generic_v_route_cut",
        "ledger_state",
        "m31_specialization",
        "module_contract",
        "nonclaims",
        "payload_sha256",
        "row_contract",
        "schema",
        "source_bindings",
        "status",
        "theorem_id",
        "toy_replays",
    }
    require(set(schema.get("required", [])) == required, "schema required keys")
    require(set(schema.get("properties", {})) == required, "schema property keys")


def verify_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    parent = strict_payload_pin(PARENT_COMPILER_PATH, PARENT_COMPILER_PAYLOAD, "parent compiler")
    source = strict_payload_pin(SOURCE_ADAPTER_PATH, SOURCE_ADAPTER_PAYLOAD, "source adapter")
    pade = strict_payload_pin(CANONICAL_PADE_PATH, CANONICAL_PADE_PAYLOAD, "canonical Padé predecessor")

    require(parent.get("compiler_id") == PARENT_COMPILER_ID, "parent compiler id")
    require(parent.get("architecture_id") == ARCHITECTURE_ID, "parent architecture")
    require(parent.get("partition", {}).get("partition_sha256") == PARTITION_SHA256, "parent partition")
    require(parent.get("atom_state", {}).get("known_sum") == U_PAID, "parent U_paid")
    require(parent.get("atom_state", {}).get("null_atoms") == list(ATOM_ORDER[1:]), "parent null atoms")
    require(parent.get("atom_state", {}).get("row_closed") is False, "parent row open")

    require(source.get("architecture_id") == ARCHITECTURE_ID, "source architecture")
    require(source.get("partition", {}).get("partition_sha256") == PARTITION_SHA256, "source partition")
    require(source.get("partition", {}).get("unit") == UNIT, "source codeword unit")
    atoms = source.get("atoms")
    require(type(atoms) is list and [row.get("atom_id") for row in atoms] == list(ATOM_ORDER), "source atom order")
    require(atoms[0].get("value") == U_PAID and atoms[0].get("bankable") is True, "source low payment")
    require(all(row.get("value") is None and row.get("bankable") is False for row in atoms[1:]), "source open atoms")

    require(pade.get("status") == "PROVED_DEPLOYED_SYMBOLIC_BRIDGE_TOY_COALESCENCE_ROUTE_CUT_ROW_OPEN", "Padé predecessor status")
    require(pade.get("scope", {}).get("deployed_row_closed") is False, "Padé predecessor row open")
    return parent, source, pade


def arithmetic() -> None:
    require(P == 2_147_483_647, "M31 prime")
    require(Q == 21_267_647_892_944_572_736_998_860_269_687_930_881, "quartic field cardinality")
    require(N == 2_097_152 and K == 1_048_576, "deployed n K")
    require(AGREEMENT == 1_116_023, "deployed agreement")
    require(RADIUS == 981_129 and W == 67_447, "deployed R w")
    require(BUDGET == 16_777_215 and NONANCHOR_BUDGET == 16_777_214, "deployed budgets")
    require(BUDGET + 1 < Q, "fresh-symbol strict field slack")
    # The cancellation used by the all-weight normal form is exact for every
    # j0, not merely at the deployed boundary.
    for j0 in (0, 1, RADIUS // 2, RADIUS - 1, RADIUS):
        t = RADIUS - j0
        s0 = N - j0
        w0 = s0 - K
        require(w0 == W + t, "all-weight w0 cancellation")
        for m in (W + 1, W + 2, W + 17):
            g = m + t
            require(g - w0 == m - W, "all-weight b-degree cancellation")
            require(j0 + g - RADIUS == m, "all-weight gcd cancellation")
            for h in (m, m + 1):
                require(j0 + g - h == RADIUS + m - h, "all-weight exact-weight cancellation")


def source_bindings() -> list[dict[str, Any]]:
    return [
        source_binding(
            "M31_ANCHOR_EXCHANGE::packet_schema",
            "experimental/data/schemas/m31_all_weight_anchor_exchange_pade_bijection_v1.schema.json",
            "packet_schema",
            "Closed top-level schema for the exact bijection and route cut.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::packet_verifier",
            "experimental/scripts/verify_m31_all_weight_anchor_exchange_packet_v1.py",
            "packet_verifier",
            "Fail-closed source, payload, theorem-contract, and mutation verifier.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::primary_replay",
            "experimental/scripts/verify_m31_all_weight_anchor_exchange_pade_bijection_v1.py",
            "primary_replay",
            "Independent-standard-library exact prime-field exhaustion and proof-critical mutations.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::sage_replay",
            "experimental/scripts/verify_m31_all_weight_anchor_exchange_pade_bijection_v1.sage",
            "sage_replay",
            "Independent GF(7), boundary V=1, and characteristic-two GF(8) exhaustion.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::theorem_note",
            "experimental/notes/thresholds/m31_all_weight_anchor_exchange_pade_bijection_v1.md",
            "theorem_note",
            "Field-uniform proof, exact inverse map, edge cases, and M31 residual theorem.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::packet_readme",
            "experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/README.md",
            "packet_readme",
            "Replay commands and explicit zero-payment scope.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::parent_compiler_manifest",
            "experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json",
            "parent_compiler_manifest",
            "Sealed v4 global completion compiler and exact five-atom chronology.",
            internal_payload_sha256=PARENT_COMPILER_PAYLOAD,
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::parent_compiler_verifier",
            "experimental/scripts/verify_m31_list_v4_global_completion_compiler.py",
            "parent_compiler_verifier",
            "Exact parent arithmetic, source graph, and signed completion target.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::parent_compiler_note",
            "experimental/notes/thresholds/m31_list_v4_global_completion_compiler.md",
            "parent_compiler_note",
            "Current M31 LIST closure contract and boundary-only route cut.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::source_adapter_manifest",
            "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
            "source_adapter_manifest",
            "Sealed codeword-valued v4 source partition and banked low atom.",
            internal_payload_sha256=SOURCE_ADAPTER_PAYLOAD,
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::active_v4_ledger",
            "experimental/grande_finale.tex",
            "active_v4_ledger",
            "Active LIST owner chronology and null-atom semantics.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::cap_foundation",
            "tex/cs25_cap_v13_2.tex",
            "cap_foundation",
            "Deployed RS parameters, domain, and exact-support conventions.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::canonical_pade_manifest",
            "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json",
            "canonical_pade_manifest",
            "Sealed predecessor Pade route-cut packet; not a payment import.",
            internal_payload_sha256=CANONICAL_PADE_PAYLOAD,
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::canonical_pade_note",
            "experimental/notes/thresholds/m31_canonical_masked_pade_global_route_cut.md",
            "canonical_pade_note",
            "Prior fixed-weight masked Pade reduction and route cut.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::canonical_pade_verifier",
            "experimental/scripts/verify_m31_canonical_masked_pade_global_route_cut_v1.py",
            "canonical_pade_verifier",
            "Prior symbolic and exact small-field Pade replay.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::quotient_fiber_audit",
            "experimental/notes/audits/audit_quotient_cell_prefix_fiber_and_split_pencil_census.md",
            "quotient_fiber_audit",
            "Existing quotient-owner distinction and exact prefix-fibre context.",
        ),
        source_binding(
            "M31_ANCHOR_EXCHANGE::quotient_fiber_verifier",
            "experimental/scripts/verify_quotient_cell_prefix_fiber_floor.py",
            "quotient_fiber_verifier",
            "Existing exact quotient-cell prefix-fibre lower-floor replay.",
        ),
    ]


def build_template() -> dict[str, Any]:
    arithmetic()
    parent, source, pade = verify_dependencies()
    bindings = source_bindings()
    require(len(bindings) == 17, "direct source-binding count")
    require(len({row["binding_id"] for row in bindings}) == len(bindings), "unique binding ids")
    require(len({row["path"] for row in bindings}) == len(bindings), "unique binding paths")

    payload: dict[str, Any] = {
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "bijection_contract": {
            "anchor_case": {
                "anchor_is_translated_zero_codeword": True,
                "j0_zero_list_is_singleton": True,
                "j0_positive_required_for_inverse_residue_V": True,
                "zero_pair_before_exclusion": "(G,H,b)=(1,1,0)",
            },
            "complete_list_identity": "|L_R(y)|=1+#X(V)",
            "exact_inverse": {
                "codeword": "c=(A0/G)*b",
                "error_locator": "G*(L0/H)",
                "error_weight": "j=j0+g-h",
                "pair_recovery": "G=L_(E(c) intersect S0); b=c*G/A0",
            },
            "nonanchor_pair": {
                "G": {
                    "divides": "A0",
                    "minimum_degree": "g>=w0+1",
                    "monic": True,
                },
                "H": {
                    "definition": "H=monic_gcd(L0,G-b*V)",
                    "full_gcd_not_arbitrary_divisor": True,
                    "radius_gate": "h>=j0+g-R",
                },
                "b": {
                    "coprime_gate": "gcd(b,G)=1",
                    "degree_gate": "deg(b)<g-w0",
                    "nonzero": True,
                },
            },
            "slack_normal_form": {
                "definitions": "t=R-j0; m=g-t",
                "derived_relations": "w0=w+t; g=m+t",
                "exact_weight": "j=R+m-h",
                "gcd_degree_gate": "h=deg(gcd(L0,G-b*V))>=m",
                "minimum_m": "m>=w+1",
                "polynomial_degree_gate": "deg(b)<m-w",
                "scope": "DERIVED_CANCELLATION_NOT_A_NEW_BOUND",
            },
            "uniqueness_unit": UNIT,
        },
        "boundary_specialization": {
            "boundary_anchor_gate": "j0=R implies h>=g",
            "boundary_companion_iff": "j=R iff h=g",
            "fresh_symbol_reduction": {
                "counterexample_sublist_size": BUDGET + 1,
                "field_gate": "B_star+1<|F|",
                "field_gate_holds_at_M31": True,
                "proof_step": "choose a minimum-agreement selected codeword and replace t matching received symbols by symbols outside all selected coordinate values",
                "retains_selected_sublist": True,
                "row_equivalence": "M31_LIST_BOUND_IFF_BOUNDARY_ANCHOR_PAIR_CENSUS_BOUND",
                "target_anchor_slack": "t=0",
            },
            "interior_companion_iff": "j<R iff h>g",
            "V_equals_one": {
                "admitted_H": "H=G-b",
                "admitted_b": "b=G-H",
                "all_admitted_have_h_equal_g": True,
                "hypotheses": "j0=R and V=1",
                "not_valid_for_generic_V": True,
            },
        },
        "dependency_contract": {
            "canonical_pade_predecessor": {
                "import_mode": "CONTEXT_AND_REGRESSION_ONLY",
                "path": str(CANONICAL_PADE_PATH.relative_to(ROOT)),
                "payload_sha256": pade["payload_sha256"],
            },
            "parent_compiler": {
                "compiler_id": parent["compiler_id"],
                "path": str(PARENT_COMPILER_PATH.relative_to(ROOT)),
                "payload_sha256": parent["payload_sha256"],
                "pr": 1052,
            },
            "partition_sha256": PARTITION_SHA256,
            "stacked_dependency": True,
            "source_adapter": {
                "path": str(SOURCE_ADAPTER_PATH.relative_to(ROOT)),
                "payload_sha256": source["payload_sha256"],
            },
        },
        "generic_v_route_cut": {
            "construction": "for arbitrary unit table v on E0 interpolate V=v and H0=v^(-1), then U=A0*H0",
            "every_unit_residue_realizable": True,
            "implication": "ONE_EXACT_ANCHOR_PLUS_RANK_TWO_CANNOT_FORCE_PROPER_STRUCTURE_ON_V",
            "not_forced_from_one_anchor": [
                "LOW_DEGREE_V",
                "RATIONAL_V",
                "PERIODIC_V",
                "QUOTIENT_V",
            ],
            "route_cut_is_not_census_counterexample": True,
            "unit_group": "(F[X]/(L0))^*",
        },
        "ledger_state": {
            "atoms": [
                {
                    "atom_id": "U_paid",
                    "bankable": True,
                    "status": "BANKED_BY_PARENT_NOT_THIS_PACKET",
                    "value": U_PAID,
                },
                *[
                    {
                        "atom_id": atom,
                        "bankable": False,
                        "status": "OPEN_UNPAID",
                        "value": None,
                    }
                    for atom in ATOM_ORDER[1:]
                ],
            ],
            "closure_mode_if_missing_census_proved": "DIRECT_COMPLETE_LIST_BOUND_NOT_ATOM_SUM",
            "known_parent_sum": U_PAID,
            "movement_from_this_packet": 0,
            "null_atoms": list(ATOM_ORDER[1:]),
            "official_endpoint_or_score_movement": 0,
            "row_closed": False,
        },
        "m31_specialization": {
            "B_star": BUDGET,
            "K": K,
            "agreement": AGREEMENT,
            "base_prime": P,
            "code_field_cardinality": str(Q),
            "minimum_g": 67_448,
            "minimum_m": 67_448,
            "missing_uniform_pair_census_target": NONANCHOR_BUDGET,
            "missing_uniform_theorem": "#X(V)<=16777214 for every boundary-anchor M31 triple (A0,L0,V)",
            "n": N,
            "radius": RADIUS,
            "reduced_anchor_quantifier": "j0=R; t=0; V arbitrary unit modulo L0",
            "row_counterexample_size": BUDGET + 1,
            "shift_w": W,
            "status": "UNPROVED",
        },
        "module_contract": {
            "basis": [["L0", "0"], ["V", "A0"]],
            "basis_coordinates_for_exchange_row": {
                "alpha": "(G-b*V)/H",
                "beta": "b*L0/H",
                "exchange_pair_is_not_basis_coordinates": True,
            },
            "congruence": "N congruent W*U modulo A0*L0",
            "determinant": "A0*L0",
            "module": "M_U={(W,N):N congruent W*U modulo A0*L0}",
            "orientation": "ROWS_ORDERED_AS_(W,N)",
        },
        "nonclaims": {
            "census_bound_proved": False,
            "boundary_forcing_proves_census_bound": False,
            "complete_M31_list_bound_proved": False,
            "generic_V_has_low_degree": False,
            "generic_V_has_quotient_structure": False,
            "generic_V_is_periodic": False,
            "ledger_atom_paid_by_this_packet": False,
            "official_endpoint_or_score_changed": False,
            "row_closed": False,
            "stable_paper_modified": False,
            "toy_replay_is_deployed_proof": False,
            "V_equals_one_boundary_formula_applies_generically": False,
        },
        "payload_sha256": "",
        "row_contract": {
            "complete_list_budget": BUDGET,
            "nonanchor_pair_budget": NONANCHOR_BUDGET,
            "object": "LIST",
            "partition_sha256": PARTITION_SHA256,
            "quantifier": "BIJECTION_UNIFORM_OVER_EVERY_ACTUAL_ANCHOR; M31_CLOSURE_REDUCED_TO_BOUNDARY_ANCHORS_t=0_WITH_ARBITRARY_UNIT_V",
            "row": "Mersenne-31 list at 2^-100",
            "target_epsilon": "2^-100",
            "unit": UNIT,
            "workboard_item": "M1/L",
        },
        "schema": SCHEMA_ID,
        "source_bindings": bindings,
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "toy_replays": {
            "gf7_arbitrary_unit": {
                "configurations": 540,
                "direct_code_checks": 185_220,
                "nonanchor_incidences": 540,
                "scope": "EXACT_TOY_CONTROL",
            },
            "gf7_boundary_V_one": {
                "direct_code_checks": 12_005,
                "gh_histogram": [
                    {"count": 126, "g": 2, "h": 2},
                    {"count": 14, "g": 3, "h": 3},
                ],
                "shift_pair_incidences": 140,
                "supports": 35,
            },
            "gf8_characteristic_two": {
                "configurations": 735,
                "direct_code_checks": 376_320,
                "nonanchor_incidences": 630,
                "scope": "EXACT_TOY_CONTROL_NOT_DEPLOYED_PROOF",
            },
            "fresh_symbol_boundary_forcing": {
                "field": "GF(7)",
                "final_distances": [3, 3],
                "initial_distances": [2, 2],
                "radius": 3,
                "selected_codewords": 2,
            },
            "j0_zero_rejection_fixture": True,
            "replay_independence": "PRIMARY_PYTHON_AND_INDEPENDENT_SAGE_SHARE_NO_IMPLEMENTATION_CODE",
        },
    }
    return seal(payload)


def verify_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list and len(bindings) == 17, "source binding list")
    ids: set[str] = set()
    paths: set[str] = set()
    pins = 0
    for index, binding in enumerate(bindings):
        require(type(binding) is dict, f"binding {index}: object")
        require(set(binding) == {"binding_id", "internal_payload_sha256", "path", "role", "scope", "sha256"}, f"binding {index}: exact keys")
        require(type(binding["binding_id"]) is str and binding["binding_id"].isascii(), f"binding {index}: id")
        require(binding["binding_id"] not in ids, f"binding {index}: unique id")
        ids.add(binding["binding_id"])
        path = canonical_repo_path(binding["path"])
        require(binding["path"] not in paths, f"binding {index}: unique path")
        paths.add(binding["path"])
        require(type(binding["role"]) is str and binding["role"].isascii(), f"binding {index}: role")
        require(type(binding["scope"]) is str and binding["scope"].isascii(), f"binding {index}: scope")
        require(type(binding["sha256"]) is str and len(binding["sha256"]) == 64, f"binding {index}: hash shape")
        require(binding["sha256"] == sha256_path(path), f"binding {index}: fresh hash")
        internal = binding["internal_payload_sha256"]
        if internal is not None:
            pins += 1
            require(type(internal) is str and len(internal) == 64, f"binding {index}: pin shape")
            strict_payload_pin(path, internal, f"binding {index}")
    require(pins == 3, "three internal payload pins")


def validate(payload: dict[str, Any], expected: dict[str, Any] | None = None) -> None:
    arithmetic()
    require(payload.get("schema") == SCHEMA_ID, "payload schema")
    require(payload.get("theorem_id") == THEOREM_ID, "theorem id")
    require(payload.get("architecture_id") == ARCHITECTURE_ID, "architecture id")
    require(payload.get("artifact_kind") == ARTIFACT_KIND, "artifact kind")
    require(payload.get("status") == STATUS, "status")
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")

    module = payload["module_contract"]
    require(module["orientation"] == "ROWS_ORDERED_AS_(W,N)", "module row orientation")
    require(module["congruence"] == "N congruent W*U modulo A0*L0", "module congruence")
    require(module["basis"] == [["L0", "0"], ["V", "A0"]], "module basis")
    require(module["basis_coordinates_for_exchange_row"]["alpha"] == "(G-b*V)/H", "alpha coordinate")
    require(module["basis_coordinates_for_exchange_row"]["beta"] == "b*L0/H", "beta coordinate")
    require(module["basis_coordinates_for_exchange_row"]["exchange_pair_is_not_basis_coordinates"] is True, "coordinate distinction")

    pair = payload["bijection_contract"]["nonanchor_pair"]
    require(pair["G"] == {"divides": "A0", "minimum_degree": "g>=w0+1", "monic": True}, "G gates")
    require(pair["b"] == {"coprime_gate": "gcd(b,G)=1", "degree_gate": "deg(b)<g-w0", "nonzero": True}, "b gates")
    require(pair["H"]["definition"] == "H=monic_gcd(L0,G-b*V)", "full gcd definition")
    require(pair["H"]["full_gcd_not_arbitrary_divisor"] is True, "full gcd gate")
    require(pair["H"]["radius_gate"] == "h>=j0+g-R", "radius gate")
    inverse = payload["bijection_contract"]["exact_inverse"]
    require(inverse["codeword"] == "c=(A0/G)*b", "inverse codeword")
    require(inverse["error_locator"] == "G*(L0/H)", "exact locator")
    require(inverse["error_weight"] == "j=j0+g-h", "exact weight")
    require(payload["bijection_contract"]["complete_list_identity"] == "|L_R(y)|=1+#X(V)", "anchor add-back")
    require(payload["bijection_contract"]["anchor_case"]["j0_zero_list_is_singleton"] is True, "j0 zero singleton")

    slack = payload["bijection_contract"]["slack_normal_form"]
    require(slack["definitions"] == "t=R-j0; m=g-t", "slack definitions")
    require(slack["derived_relations"] == "w0=w+t; g=m+t", "slack relations")
    require(slack["minimum_m"] == "m>=w+1", "slack minimum m")
    require(slack["polynomial_degree_gate"] == "deg(b)<m-w", "slack b gate")
    require(slack["gcd_degree_gate"] == "h=deg(gcd(L0,G-b*V))>=m", "slack gcd gate")
    require(slack["exact_weight"] == "j=R+m-h", "slack weight")

    boundary = payload["boundary_specialization"]
    require(boundary["boundary_anchor_gate"] == "j0=R implies h>=g", "boundary gate")
    require(boundary["boundary_companion_iff"] == "j=R iff h=g", "boundary iff")
    require(boundary["interior_companion_iff"] == "j<R iff h>g", "interior iff")
    forcing = boundary["fresh_symbol_reduction"]
    require(forcing["counterexample_sublist_size"] == BUDGET + 1, "boundary forcing size")
    require(forcing["field_gate"] == "B_star+1<|F|", "boundary forcing field gate")
    require(forcing["field_gate_holds_at_M31"] is True, "boundary forcing M31 gate")
    require(forcing["retains_selected_sublist"] is True, "boundary forcing retention")
    require(forcing["target_anchor_slack"] == "t=0", "boundary forcing target")
    require(forcing["row_equivalence"] == "M31_LIST_BOUND_IFF_BOUNDARY_ANCHOR_PAIR_CENSUS_BOUND", "boundary forcing equivalence")
    require(boundary["V_equals_one"]["hypotheses"] == "j0=R and V=1", "V=1 hypotheses")
    require(boundary["V_equals_one"]["not_valid_for_generic_V"] is True, "V=1 scope guard")

    route = payload["generic_v_route_cut"]
    require(route["every_unit_residue_realizable"] is True, "generic V realization")
    require(route["route_cut_is_not_census_counterexample"] is True, "route-cut scope")
    require(route["implication"] == "ONE_EXACT_ANCHOR_PLUS_RANK_TWO_CANNOT_FORCE_PROPER_STRUCTURE_ON_V", "route-cut implication")

    m31 = payload["m31_specialization"]
    require(m31["base_prime"] == P and m31["n"] == N and m31["K"] == K, "M31 core parameters")
    require(m31["agreement"] == AGREEMENT and m31["radius"] == RADIUS and m31["shift_w"] == W, "M31 derived parameters")
    require(m31["code_field_cardinality"] == str(Q), "M31 field cardinality")
    require(m31["B_star"] == BUDGET, "M31 budget")
    require(m31["minimum_g"] == W + 1 and m31["minimum_m"] == W + 1, "M31 degree floor")
    require(m31["missing_uniform_pair_census_target"] == NONANCHOR_BUDGET, "M31 pair target")
    require(m31["row_counterexample_size"] == BUDGET + 1, "M31 counterexample size")
    require(m31["reduced_anchor_quantifier"] == "j0=R; t=0; V arbitrary unit modulo L0", "M31 boundary quantifier")
    require(m31["status"] == "UNPROVED", "M31 residual open")

    ledger = payload["ledger_state"]
    require(ledger["movement_from_this_packet"] == 0, "zero ledger movement")
    require(ledger["official_endpoint_or_score_movement"] == 0, "zero official movement")
    require(ledger["known_parent_sum"] == U_PAID, "parent low payment")
    require(ledger["null_atoms"] == list(ATOM_ORDER[1:]), "four null atoms")
    require(ledger["row_closed"] is False, "row open")
    require([row["atom_id"] for row in ledger["atoms"]] == list(ATOM_ORDER), "ledger atom order")
    require(all(row["value"] is None for row in ledger["atoms"][1:]), "ledger null values")
    require(all(value is False for value in payload["nonclaims"].values()), "all nonclaims false")

    dependency = payload["dependency_contract"]
    require(dependency["parent_compiler"]["payload_sha256"] == PARENT_COMPILER_PAYLOAD, "parent payload")
    require(dependency["source_adapter"]["payload_sha256"] == SOURCE_ADAPTER_PAYLOAD, "source payload")
    require(dependency["canonical_pade_predecessor"]["payload_sha256"] == CANONICAL_PADE_PAYLOAD, "Padé payload")
    require(dependency["partition_sha256"] == PARTITION_SHA256, "partition digest")
    verify_source_bindings(payload["source_bindings"])

    if expected is None:
        expected = build_template()
    deep_exact(payload, expected)


def mutate(path: Sequence[Any], value: Any) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def apply(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        cursor: Any = out
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        return seal(out)
    return apply


def tamper_selftest(expected: dict[str, Any]) -> int:
    def add_unknown(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["unknown"] = 1
        return seal(out)

    def stale_seal(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["m31_specialization"]["agreement"] -= 1
        return out

    def delete_binding(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["source_bindings"].pop()
        return seal(out)

    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("schema", mutate(("schema",), "rs-mca-m31-all-weight-anchor-exchange-pade-bijection-v0")),
        ("theorem id", mutate(("theorem_id",), "M31_ANCHOR_EXCHANGE_V0")),
        ("architecture", mutate(("architecture_id",), "GRANDE_FINALE_V3_EXACT_COMPLETION")),
        ("artifact kind", mutate(("artifact_kind",), "UPPER_BOUND")),
        ("status closure", mutate(("status",), "ROW_CLOSED")),
        ("unknown top key", add_unknown),
        ("stale payload seal", stale_seal),
        ("reversed congruence", mutate(("module_contract", "congruence"), "W congruent N*U modulo A0*L0")),
        ("reversed module", mutate(("module_contract", "module"), "M_U={(W,N):W congruent N*U modulo A0*L0}")),
        ("basis swap", mutate(("module_contract", "basis"), [["V", "A0"], ["L0", "0"]])),
        ("wrong first basis row", mutate(("module_contract", "basis", 0), ["A0", "0"])),
        ("wrong alpha", mutate(("module_contract", "basis_coordinates_for_exchange_row", "alpha"), "G")),
        ("wrong beta", mutate(("module_contract", "basis_coordinates_for_exchange_row", "beta"), "b")),
        ("identify pair with coordinates", mutate(("module_contract", "basis_coordinates_for_exchange_row", "exchange_pair_is_not_basis_coordinates"), False)),
        ("G nonmonic", mutate(("bijection_contract", "nonanchor_pair", "G", "monic"), False)),
        ("G wrong divisor", mutate(("bijection_contract", "nonanchor_pair", "G", "divides"), "L0")),
        ("G weak floor", mutate(("bijection_contract", "nonanchor_pair", "G", "minimum_degree"), "g>=w0")),
        ("allow zero b", mutate(("bijection_contract", "nonanchor_pair", "b", "nonzero"), False)),
        ("weak b degree", mutate(("bijection_contract", "nonanchor_pair", "b", "degree_gate"), "deg(b)<=g-w0")),
        ("omit b coprimality", mutate(("bijection_contract", "nonanchor_pair", "b", "coprime_gate"), "NONE")),
        ("arbitrary H divisor", mutate(("bijection_contract", "nonanchor_pair", "H", "full_gcd_not_arbitrary_divisor"), False)),
        ("wrong H definition", mutate(("bijection_contract", "nonanchor_pair", "H", "definition"), "H divides gcd(L0,G-b*V)")),
        ("weak radius gate", mutate(("bijection_contract", "nonanchor_pair", "H", "radius_gate"), "h>j0+g-R")),
        ("wrong codeword", mutate(("bijection_contract", "exact_inverse", "codeword"), "c=G*b")),
        ("wrong locator division", mutate(("bijection_contract", "exact_inverse", "error_locator"), "G*H")),
        ("wrong weight sign", mutate(("bijection_contract", "exact_inverse", "error_weight"), "j=j0+g+h")),
        ("drop anchor addback", mutate(("bijection_contract", "complete_list_identity"), "|L_R(y)|=#X(V)")),
        ("j0 zero nonsingleton", mutate(("bijection_contract", "anchor_case", "j0_zero_list_is_singleton"), False)),
        ("t wrong sign", mutate(("bijection_contract", "slack_normal_form", "definitions"), "t=j0-R; m=g-t")),
        ("m wrong definition", mutate(("bijection_contract", "slack_normal_form", "definitions"), "t=R-j0; m=g+t")),
        ("w0 cancellation wrong", mutate(("bijection_contract", "slack_normal_form", "derived_relations"), "w0=w-t; g=m+t")),
        ("m floor weak", mutate(("bijection_contract", "slack_normal_form", "minimum_m"), "m>=w")),
        ("slack b weak", mutate(("bijection_contract", "slack_normal_form", "polynomial_degree_gate"), "deg(b)<=m-w")),
        ("slack H wrong", mutate(("bijection_contract", "slack_normal_form", "gcd_degree_gate"), "h>=m-1")),
        ("slack j wrong", mutate(("bijection_contract", "slack_normal_form", "exact_weight"), "j=R-m+h")),
        ("slack promoted bound", mutate(("bijection_contract", "slack_normal_form", "scope"), "PROVED_UPPER_BOUND")),
        ("boundary weak gate", mutate(("boundary_specialization", "boundary_anchor_gate"), "j0=R implies h>=g-1")),
        ("boundary forcing off by one", mutate(("boundary_specialization", "fresh_symbol_reduction", "counterexample_sublist_size"), BUDGET)),
        ("boundary forcing weak field gate", mutate(("boundary_specialization", "fresh_symbol_reduction", "field_gate"), "B_star+1<=|F|")),
        ("boundary forcing no retention", mutate(("boundary_specialization", "fresh_symbol_reduction", "retains_selected_sublist"), False)),
        ("boundary forcing wrong slack", mutate(("boundary_specialization", "fresh_symbol_reduction", "target_anchor_slack"), "t>=0")),
        ("boundary forcing false equivalence", mutate(("boundary_specialization", "fresh_symbol_reduction", "row_equivalence"), "SUFFICIENT_ONLY")),
        ("boundary iff reversed", mutate(("boundary_specialization", "boundary_companion_iff"), "j=R iff h>g")),
        ("interior iff reversed", mutate(("boundary_specialization", "interior_companion_iff"), "j<R iff h=g")),
        ("V1 leaked generic", mutate(("boundary_specialization", "V_equals_one", "not_valid_for_generic_V"), False)),
        ("V1 missing hypothesis", mutate(("boundary_specialization", "V_equals_one", "hypotheses"), "j0=R")),
        ("V1 wrong H", mutate(("boundary_specialization", "V_equals_one", "admitted_H"), "H=G-b*V")),
        ("generic V not every unit", mutate(("generic_v_route_cut", "every_unit_residue_realizable"), False)),
        ("generic V forced low", mutate(("generic_v_route_cut", "not_forced_from_one_anchor"), ["RATIONAL_V"])),
        ("route cut claims counterexample", mutate(("generic_v_route_cut", "route_cut_is_not_census_counterexample"), False)),
        ("M31 p", mutate(("m31_specialization", "base_prime"), P - 1)),
        ("M31 agreement", mutate(("m31_specialization", "agreement"), AGREEMENT - 1)),
        ("M31 radius", mutate(("m31_specialization", "radius"), RADIUS - 1)),
        ("M31 w", mutate(("m31_specialization", "shift_w"), W - 1)),
        ("M31 minimum g", mutate(("m31_specialization", "minimum_g"), W)),
        ("M31 minimum m", mutate(("m31_specialization", "minimum_m"), W)),
        ("M31 census off by one", mutate(("m31_specialization", "missing_uniform_pair_census_target"), BUDGET)),
        ("M31 all-anchor quantifier", mutate(("m31_specialization", "reduced_anchor_quantifier"), "all actual anchors")),
        ("M31 counterexample off by one", mutate(("m31_specialization", "row_counterexample_size"), BUDGET)),
        ("M31 census claimed", mutate(("m31_specialization", "status"), "PROVED")),
        ("false list proof", mutate(("nonclaims", "complete_M31_list_bound_proved"), True)),
        ("false census proof", mutate(("nonclaims", "census_bound_proved"), True)),
        ("boundary forcing claimed census", mutate(("nonclaims", "boundary_forcing_proves_census_bound"), True)),
        ("false generic periodicity", mutate(("nonclaims", "generic_V_is_periodic"), True)),
        ("false payment", mutate(("nonclaims", "ledger_atom_paid_by_this_packet"), True)),
        ("false closure", mutate(("nonclaims", "row_closed"), True)),
        ("ledger movement", mutate(("ledger_state", "movement_from_this_packet"), 1)),
        ("official movement", mutate(("ledger_state", "official_endpoint_or_score_movement"), 1)),
        ("U Q zero", mutate(("ledger_state", "atoms", 1, "value"), 0)),
        ("row closed", mutate(("ledger_state", "row_closed"), True)),
        ("parent payload", mutate(("dependency_contract", "parent_compiler", "payload_sha256"), "0" * 64)),
        ("source payload", mutate(("dependency_contract", "source_adapter", "payload_sha256"), "0" * 64)),
        ("Padé payload", mutate(("dependency_contract", "canonical_pade_predecessor", "payload_sha256"), "0" * 64)),
        ("partition digest", mutate(("dependency_contract", "partition_sha256"), "0" * 64)),
        ("unstack dependency", mutate(("dependency_contract", "stacked_dependency"), False)),
        ("toy count", mutate(("toy_replays", "gf7_arbitrary_unit", "nonanchor_incidences"), 539)),
        ("characteristic two count", mutate(("toy_replays", "gf8_characteristic_two", "configurations"), 734)),
        ("boundary forcing toy", mutate(("toy_replays", "fresh_symbol_boundary_forcing", "final_distances"), [2, 3])),
        ("source hash", mutate(("source_bindings", 0, "sha256"), "0" * 64)),
        ("source traversal", mutate(("source_bindings", 0, "path"), "../schema.json")),
        ("source pin", mutate(("source_bindings", 6, "internal_payload_sha256"), "0" * 64)),
        ("delete source binding", delete_binding),
    ]

    rejected = 0
    for label, fn in mutations:
        candidate = fn(expected)
        try:
            validate(candidate, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")

    malformed = (
        b'{"a":1,"a":2}',
        b'{"a":1.5}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        '{"\u00e9":1}'.encode("utf-8"),
    )
    for raw in malformed:
        try:
            strict_decode(raw, canonical=False)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("malformed JSON accepted")
    require(rejected == len(mutations) + len(malformed), "all mutations rejected")
    return rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.check or args.tamper_selftest or args.print_template):
        args.check = True
    require(sum((args.check, args.tamper_selftest, args.print_template)) == 1, "select exactly one mode")
    validate_schema()
    expected = build_template()
    validate(expected, expected)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
        return
    if args.tamper_selftest:
        count = tamper_selftest(expected)
        print(f"M31 all-weight anchor-exchange packet mutations: {count}/{count} rejected PASS")
        return

    actual = strict_load(args.manifest)
    validate(actual, expected)
    print("M31 all-weight anchor-exchange Padé packet v1: PASS")
    print("module: N=W*U mod A0*L0; basis (L0,0),(V,A0) PASS")
    print("complete list: anchor + exact (G,b) divisor/gcd census PASS")
    print("all-weight slack form: m>=67448, deg(b)<m-67447, h>=m PASS")
    print("fresh-symbol forcing: B_star+1<q; closing census reduced to t=0 PASS")
    print("generic V: every unit residue realizable; rank-two structural shortcut CUT")
    print("M31 missing theorem: boundary #X(V)<=16777214 for arbitrary unit V; row OPEN; ledger movement 0")
    print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
