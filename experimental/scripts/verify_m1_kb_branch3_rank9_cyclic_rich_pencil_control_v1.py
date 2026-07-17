#!/usr/bin/env python3
"""Strict certificate checker for the cyclic rich-pencil toy closure.

Sage independently recomputes the finite-field construction.  This
standard-library checker binds that replay, its exact fixture, the imported
low-excess owner, scope guards, source hashes, and mutation tests.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-rank9-cyclic-rich-pencil-control-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_RANK9_CYCLIC_RICH_PENCIL_TOY_CLOSURE"
STATUS = "PROVED_EXACT_CYCLIC_TOY_LOW_EXCESS_COMPLETE_SELECTOR_CLOSURE"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-rank9-cyclic-rich-pencil-control-v1"
)
CERT_PATH = (
    CERT_DIR / "m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.json"
)

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-cyclic-rich-pencil-control-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.sage"
)
ATLAS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)
ATLAS_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-rich-pencil-atlas-v1/"
    "m1_kb_branch3_rank9_rich_pencil_atlas_v1.json"
)
OWNER_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_low_excess_carrier_cut_v1.md"
)
OWNER_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-low-excess-carrier-cut-v1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.json"
)
CONTRACT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_5_mask_contract_v1.md"
)

SAGE_PAYLOAD_SHA256 = (
    "57d75ce456986e63726109eeabe2c9c373e97c2d63fc824e12f8e55e6691dcaf"
)
FRONTIER_DISTRIBUTION_SHA256 = (
    "b6026aec9c60ea9dff901ecc44e4a92cbd29541e9c96a39426987a8b7c12c894"
)
DECLARED_SLOPES_SHA256 = (
    "6a7919285bf8cb8aa1a9521736d1f06bdbbab5101f3ee906c24ef722f561efa3"
)
FULL_SLOPES_SHA256 = (
    "03068944744fb7f5e6bdb18b5c88a4bc0eb84de89dbbcd051b29b67dfd8a8d7b"
)
LEX_PAIRS_SHA256 = (
    "a7ca35c31e7fa33063a392e984071b7946b604563907bcdacc8da2a98b0ebc2b"
)
PERIODIC_Q0_FRONTIER_COUNTS_SHA256 = (
    "1428b891e9e3bfe0e44ee45ed8f438778763fe46bd4b67853f45a26ae8f5c082"
)

RICH_CORE = [4, 5, 13, 15, 16, 19, 21, 22, 27, 28, 30]
OUTLIERS = [
    [3, 4, 5, 6, 7, 13, 17, 23, 24, 25, 30, 31],
    [5, 6, 7, 8, 13, 15, 16, 18, 21, 23, 24, 32],
    [3, 5, 7, 10, 13, 14, 15, 17, 20, 21, 24, 30],
    [2, 5, 7, 9, 10, 20, 22, 23, 24, 28, 30, 33],
    [2, 5, 15, 16, 18, 19, 20, 23, 24, 30, 31, 33],
    [5, 7, 8, 9, 11, 13, 15, 19, 20, 25, 31, 33],
    [7, 12, 14, 15, 17, 19, 20, 25, 26, 31, 32, 33],
    [3, 4, 8, 15, 17, 22, 24, 25, 26, 28, 29, 30],
]
FULL_SELECTOR_CORE = [5, 7, 8, 9, 11, 15, 18, 20, 24, 33]
RELATIVE_EXPONENTS = [
    0,
    54,
    3,
    24,
    63,
    1,
    64,
    46,
    48,
    27,
    5,
    36,
    44,
    7,
    49,
    23,
    17,
    57,
    33,
    62,
    4,
    35,
    13,
    58,
    60,
    42,
    39,
    43,
    16,
    37,
    52,
    40,
]

U_PAID = 2_602_502_999
B_REMAINING = 274_980_725_508_892_088

NONCLAIMS = [
    "This packet does not instantiate the KoalaBear field or cyclic domain.",
    "This packet does not provide a deployed complete-selector inventory.",
    "This packet does not prove global branch-1 survival for the sparse pair.",
    "This packet does not promote the incomplete 29-slope selector to a full selector.",
    "This packet does not move the KoalaBear ledger.",
    "This packet does not close deployed rank nine or the rich-pencil aggregate.",
    "This packet does not determine U_Q or U_A.",
    "This packet does not authorize Lean or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """A schema, source, arithmetic, or semantic check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def reject_float(value: str) -> None:
    raise VerificationError(f"floating-point JSON number: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path}")
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing bound source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(
    binding_id: str, relative: Path, role: str
) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def predecessor_payload(relative: Path) -> str:
    data = load_json(ROOT / relative)
    require(
        data.get("payload_sha256") == payload_hash(data),
        f"bad predecessor payload: {relative}",
    )
    return str(data["payload_sha256"])


def expected_certificate() -> dict[str, Any]:
    source_bindings = [
        source_binding("packet-note", NOTE_REL, "exact statement and scope"),
        source_binding("packet-readme", README_REL, "replay instructions"),
        source_binding("packet-python", PYTHON_REL, "strict certificate checker"),
        source_binding("packet-sage", SAGE_REL, "exact finite-field replay"),
        source_binding("atlas-note", ATLAS_NOTE_REL, "canonical rich-pencil identity"),
        source_binding("owner-note", OWNER_NOTE_REL, "low-excess complete-selector owner"),
        source_binding("selector-contract", CONTRACT_NOTE_REL, "complete-selector quantifiers"),
    ]
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": source_bindings,
        "predecessor_bindings": {
            "rich_pencil_atlas_payload": predecessor_payload(ATLAS_CERT_REL),
            "low_excess_owner_payload": predecessor_payload(OWNER_CERT_REL),
        },
        "exact_fixture": {
            "field": {
                "characteristic": 67,
                "degree": 2,
                "cardinality": 4_489,
                "modulus_coefficients_ascending": [2, 63, 1],
                "primitive_generator_coordinates": [0, 1],
                "omega_exponent": 132,
                "omega_coordinates": [41, 55],
                "omega_order": 34,
            },
            "row": {"n": 34, "k": 13, "R": 21, "j": 20, "A": 14, "t": 1},
            "domain": "D_i=omega^i for 0<=i<34",
            "source_pair": "epsilon_0=e_0, epsilon_1=e_1",
            "root_witness": [
                "P_S=product_(i in S)(X-D_i)",
                "q_S=P_S/P_S(D_0)",
                "eta_S=q_S(D_1)",
                "e_S=epsilon_0+eta_S*epsilon_1-ev_D(q_S)",
            ],
            "rich_core": RICH_CORE,
            "outliers": OUTLIERS,
            "full_selector_core": FULL_SELECTOR_CORE,
            "relative_ratio_generator": 63,
            "relative_exponents_for_indices_2_through_33": RELATIVE_EXPONENTS,
        },
        "sage_replay": {
            "schema": SCHEMA + "-sage",
            "payload_sha256": SAGE_PAYLOAD_SHA256,
            "classification": "EXACT_CYCLIC_COMPLETE_SELECTOR_LOW_EXCESS_CLOSURE",
            "all_finite_field_claims_recomputed": True,
        },
        "incomplete_rank9_control": {
            "declared_slope_count": 29,
            "rich_support_count": 21,
            "outlier_count": 8,
            "selected_slopes_sha256": DECLARED_SLOPES_SHA256,
            "complete_on_declared_Gamma": True,
            "declared_Gamma_exhausts_full_bad_set": False,
            "witness_inventory_exhaustive": False,
            "all_selected_slopes_quadratic": True,
            "all_deficits_zero": True,
            "affine_difference_rank": 9,
            "raw_witness_rank": 10,
            "kernel_core_rank": 8,
            "carrier_size": 32,
            "carrier_excess": 11,
            "ten_supports_recover_carrier": True,
            "regular_hankel_chart_count": 29,
            "same_support_noncontainment_count": 29,
            "support_rank": 20,
            "support_plus_direction_rank": 21,
            "q0_c2_count": 0,
            "q0_c17_count": 0,
            "periodic_support_count": 0,
            "syndrome_rank": 2,
            "frobenius_stack_rank": 3,
            "projective_syndrome_field_full": True,
        },
        "canonical_atlas_control": {
            "rich_line_count": 1,
            "pair_only_line_count": 196,
            "J_L": 21,
            "M_L": 21,
            "x_L": 1,
            "delta_histogram": {"0": 21},
            "Z_L_size_in_carrier": 11,
            "beta_L": 165,
            "gcd_degree": 11,
            "sparse_plant_size": 2,
            "candidate_mask_basis_incidences": 14_355,
            "valid_mask_basis_incidences": 14_198,
            "distinct_valid_bases": 10_898,
            "maximum_basis_multiplicity": 21,
            "direct_excess": 165,
            "atlas_excess": 165,
        },
        "complete_noncontained_frontier": {
            "agreement_pattern": [12, 2],
            "twelve_subset_count": 225_792_840,
            "noncontained_bad_slope_count": 66,
            "all_frontier_slopes_quadratic": True,
            "declared_slope_count": 29,
            "unselected_slope_count": 37,
            "selected_witness_count_min": 3_420_854,
            "selected_witness_count_max": 3_421_402,
            "frontier_distribution_sha256": FRONTIER_DISTRIBUTION_SHA256,
            "minimum_full_selector_affine_rank_computed": True,
            "minimum_full_selector_affine_rank": 2,
            "periodic_q0_c2_support_count": 3_003,
            "periodic_q0_c2_projected_slope_count": 66,
            "periodic_q0_c2_witness_count_min": 41,
            "periodic_q0_c2_witness_count_max": 51,
            "periodic_q0_c2_frontier_counts_sha256": PERIODIC_Q0_FRONTIER_COUNTS_SHA256,
            "q0_c17_existential_slope_count": 0,
            "q0_c17_empty_reason": "EACH_17_FIBRE_CONTAINS_0_OR_1_OUTSIDE_B",
        },
        "complete_selector_closure": {
            "selector_rule": "LEX_FIRST_PAIR_PER_RELATIVE_RESIDUE",
            "pair_sum_residues_covered": 66,
            "full_selector_constructed": True,
            "selected_slope_count": 66,
            "full_slopes_sha256": FULL_SLOPES_SHA256,
            "lex_pairs_sha256": LEX_PAIRS_SHA256,
            "affine_difference_rank": 2,
            "polynomial_affine_rank": 2,
            "polynomial_to_error_difference_map_rank": 12,
            "raw_witness_rank": 3,
            "common_gcd_degree": 10,
            "carrier_size": 22,
            "carrier_excess": 1,
            "kappa_star": 1,
            "kappa_star_proved_exact": True,
            "q0_c2_count": 0,
            "q0_c17_count": 0,
            "periodic_support_count": 0,
            "minimum_affine_rank": 2,
            "minimum_affine_rank_proved_exact": True,
            "owner": "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
            "owner_cutoff": 10,
            "owner_eligible": True,
            "owner_cap_B_1": 231,
            "owner_cap_fits_66_slopes": True,
            "toy_family_closed": True,
        },
        "minimality": {
            "ansatz": "TWO_SPARSE_ONE_MOVING_ROOT_HIGH_CARRIER_RANK9",
            "minimum_R": 21,
            "minimum_k": 13,
            "minimum_n": 34,
            "minimum_outliers": 8,
            "minimum_quadratic_or_sextic_prime": 67,
            "global_minimality_claimed": False,
        },
        "owner_semantics": {
            "owner_is_existential_over_complete_selectors": True,
            "complete_selector_carrier_excess_at_most_ten": True,
            "incomplete_rank9_selector_can_define_residual": False,
            "first_match_terminal": "AT_OR_BEFORE_BRANCH3_LOW_EXCESS_COMMON_CARRIER",
        },
        "scope_guards": {
            "exact_toy_control": True,
            "incomplete_rank9_selector_declared_only": True,
            "separate_full_selector_exhausts_toy_bad_set": True,
            "global_branch1_survival_proved": False,
            "koalabear_field_instantiated": False,
            "koalabear_domain_instantiated": False,
            "deployed": False,
            "deployed_complete_selector_inventory": False,
            "deployed_aggregate_gate_proved": False,
            "deployed_rank9_closed": False,
        },
        "ledger": {
            "U_paid_before": str(U_PAID),
            "U_paid_after": str(U_PAID),
            "B_remaining_before": str(B_REMAINING),
            "B_remaining_after": str(B_REMAINING),
            "movement": "0",
        },
        "audit": {
            "toy_verdict": "GREEN_EXACT_COMPLETE_SELECTOR_LOW_EXCESS_CLOSURE",
            "deployed_verdict": "YELLOW_NO_DEPLOYED_IMPLICATION",
            "parameter_dependence": "EXACT_GF67_2_ORDER34_TOY_ONLY",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
        },
        "nonclaims": NONCLAIMS,
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def strict_match(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type mismatch at {path}")
    if type(expected) is dict:
        require(actual.keys() == expected.keys(), f"key mismatch at {path}")
        for key in expected:
            strict_match(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_match(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"value mismatch at {path}")


def validate_certificate(data: dict[str, Any]) -> None:
    expected = expected_certificate()
    strict_match(data, expected)
    require(data["payload_sha256"] == payload_hash(data), "payload hash mismatch")
    require(len(RICH_CORE) == 11, "rich core size drift")
    require(len(OUTLIERS) == 8, "outlier count drift")
    require(all(len(item) == 12 for item in OUTLIERS), "outlier size drift")
    require(len(FULL_SELECTOR_CORE) == 10, "full selector core size drift")
    require(len(RELATIVE_EXPONENTS) == 32, "relative exponent count drift")
    require(len(set(RELATIVE_EXPONENTS)) == 32, "relative exponents collided")
    require(
        data["canonical_atlas_control"]["direct_excess"]
        == data["canonical_atlas_control"]["atlas_excess"]
        == data["canonical_atlas_control"]["beta_L"],
        "atlas identity drift",
    )
    require(
        data["complete_selector_closure"]["selected_slope_count"]
        == data["complete_noncontained_frontier"]["noncontained_bad_slope_count"],
        "full selector no longer exhausts frontier",
    )
    require(
        data["complete_selector_closure"]["carrier_excess"]
        <= data["complete_selector_closure"]["owner_cutoff"],
        "complete selector lost low-excess eligibility",
    )
    require(
        data["complete_noncontained_frontier"]["noncontained_bad_slope_count"]
        <= data["complete_selector_closure"]["owner_cap_B_1"]
        == 231,
        "toy slope count no longer fits B_1",
    )
    require(
        data["complete_selector_closure"]["affine_difference_rank"]
        == data["complete_selector_closure"]["polynomial_affine_rank"]
        == data["complete_selector_closure"]["minimum_affine_rank"]
        == data["complete_noncontained_frontier"]["minimum_full_selector_affine_rank"],
        "complete-selector minimum affine rank drift",
    )
    require(
        data["complete_selector_closure"]["polynomial_to_error_difference_map_rank"]
        == 12,
        "polynomial-to-error injection drift",
    )
    require(
        data["complete_selector_closure"]["carrier_excess"]
        == data["complete_selector_closure"]["kappa_star"]
        == 1,
        "complete-selector minimum carrier excess drift",
    )
    require(
        data["complete_selector_closure"]["q0_c2_count"] == 0
        and data["complete_noncontained_frontier"]["periodic_q0_c2_projected_slope_count"]
        == 66,
        "chosen-selector and existential Q0 projections were conflated",
    )
    require(
        not data["incomplete_rank9_control"]["declared_Gamma_exhausts_full_bad_set"],
        "incomplete rank-nine selector promoted to exhaustive",
    )
    require(data["ledger"]["movement"] == "0", "toy packet moved ledger")


def rehash(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


Mutation = tuple[str, Callable[[dict[str, Any]], None], bool]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-bad"), True),
        ("status", lambda d: d.__setitem__("status", "PROVED_DEPLOYED"), True),
        ("field-p", lambda d: d["exact_fixture"]["field"].__setitem__("characteristic", 71), True),
        ("omega-order", lambda d: d["exact_fixture"]["field"].__setitem__("omega_order", 33), True),
        ("row-j", lambda d: d["exact_fixture"]["row"].__setitem__("j", 19), True),
        ("rich-core", lambda d: d["exact_fixture"]["rich_core"].__setitem__(0, 3), True),
        ("outlier", lambda d: d["exact_fixture"]["outliers"][0].pop(), True),
        ("full-core", lambda d: d["exact_fixture"]["full_selector_core"].pop(), True),
        ("relative-exp", lambda d: d["exact_fixture"]["relative_exponents_for_indices_2_through_33"].__setitem__(0, 1), True),
        ("sage-payload", lambda d: d["sage_replay"].__setitem__("payload_sha256", "0" * 64), True),
        ("sage-class", lambda d: d["sage_replay"].__setitem__("classification", "DEPLOYED"), True),
        ("declared-count", lambda d: d["incomplete_rank9_control"].__setitem__("declared_slope_count", 30), True),
        ("declared-exhaustive", lambda d: d["incomplete_rank9_control"].__setitem__("declared_Gamma_exhausts_full_bad_set", True), True),
        ("declared-rank", lambda d: d["incomplete_rank9_control"].__setitem__("affine_difference_rank", 8), True),
        ("declared-carrier", lambda d: d["incomplete_rank9_control"].__setitem__("carrier_excess", 10), True),
        ("declared-q0", lambda d: d["incomplete_rank9_control"].__setitem__("q0_c2_count", 1), True),
        ("frobenius", lambda d: d["incomplete_rank9_control"].__setitem__("frobenius_stack_rank", 2), True),
        ("beta", lambda d: d["canonical_atlas_control"].__setitem__("beta_L", 164), True),
        ("direct", lambda d: d["canonical_atlas_control"].__setitem__("direct_excess", 164), True),
        ("atlas", lambda d: d["canonical_atlas_control"].__setitem__("atlas_excess", 166), True),
        ("frontier", lambda d: d["complete_noncontained_frontier"].__setitem__("noncontained_bad_slope_count", 65), True),
        ("frontier-hash", lambda d: d["complete_noncontained_frontier"].__setitem__("frontier_distribution_sha256", "0" * 64), True),
        ("minimum-rank", lambda d: d["complete_noncontained_frontier"].__setitem__("minimum_full_selector_affine_rank", 1), True),
        ("periodic-inventory", lambda d: d["complete_noncontained_frontier"].__setitem__("periodic_q0_c2_support_count", 3_002), True),
        ("periodic-projection", lambda d: d["complete_noncontained_frontier"].__setitem__("periodic_q0_c2_projected_slope_count", 65), True),
        ("periodic-hash", lambda d: d["complete_noncontained_frontier"].__setitem__("periodic_q0_c2_frontier_counts_sha256", "0" * 64), True),
        ("c17-reason", lambda d: d["complete_noncontained_frontier"].__setitem__("q0_c17_empty_reason", "LEX_ONLY"), True),
        ("full-selector", lambda d: d["complete_selector_closure"].__setitem__("full_selector_constructed", False), True),
        ("full-count", lambda d: d["complete_selector_closure"].__setitem__("selected_slope_count", 65), True),
        ("full-rank", lambda d: d["complete_selector_closure"].__setitem__("affine_difference_rank", 9), True),
        ("polynomial-rank", lambda d: d["complete_selector_closure"].__setitem__("polynomial_affine_rank", 1), True),
        ("difference-map", lambda d: d["complete_selector_closure"].__setitem__("polynomial_to_error_difference_map_rank", 11), True),
        ("full-carrier", lambda d: d["complete_selector_closure"].__setitem__("carrier_size", 32), True),
        ("full-excess", lambda d: d["complete_selector_closure"].__setitem__("carrier_excess", 11), True),
        ("kappa-star", lambda d: d["complete_selector_closure"].__setitem__("kappa_star", 0), True),
        ("minimum-affine", lambda d: d["complete_selector_closure"].__setitem__("minimum_affine_rank", 1), True),
        ("full-gcd", lambda d: d["complete_selector_closure"].__setitem__("common_gcd_degree", 9), True),
        ("full-periodic", lambda d: d["complete_selector_closure"].__setitem__("periodic_support_count", 1), True),
        ("owner", lambda d: d["complete_selector_closure"].__setitem__("owner", "UNPAID"), True),
        ("owner-cutoff", lambda d: d["complete_selector_closure"].__setitem__("owner_cutoff", 0), True),
        ("owner-eligible", lambda d: d["complete_selector_closure"].__setitem__("owner_eligible", False), True),
        ("owner-cap", lambda d: d["complete_selector_closure"].__setitem__("owner_cap_B_1", 65), True),
        ("owner-cap-fit", lambda d: d["complete_selector_closure"].__setitem__("owner_cap_fits_66_slopes", False), True),
        ("toy-closed", lambda d: d["complete_selector_closure"].__setitem__("toy_family_closed", False), True),
        ("global-min", lambda d: d["minimality"].__setitem__("global_minimality_claimed", True), True),
        ("owner-semantic", lambda d: d["owner_semantics"].__setitem__("incomplete_rank9_selector_can_define_residual", True), True),
        ("deployed", lambda d: d["scope_guards"].__setitem__("deployed", True), True),
        ("deployed-inventory", lambda d: d["scope_guards"].__setitem__("deployed_complete_selector_inventory", True), True),
        ("branch1", lambda d: d["scope_guards"].__setitem__("global_branch1_survival_proved", True), True),
        ("ledger", lambda d: d["ledger"].__setitem__("movement", "1"), True),
        ("verdict", lambda d: d["audit"].__setitem__("deployed_verdict", "GREEN"), True),
        ("nonclaim", lambda d: d["nonclaims"].pop(), True),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64), True),
        ("predecessor", lambda d: d["predecessor_bindings"].__setitem__("low_excess_owner_payload", "0" * 64), True),
        ("type-confusion", lambda d: d["complete_selector_closure"].__setitem__("owner_cutoff", True), True),
        ("payload", lambda d: d.__setitem__("payload_sha256", "0" * 64), False),
    ]


def run_tamper_selftest() -> int:
    base = expected_certificate()
    passed = 0
    for name, mutate, should_rehash in mutation_cases():
        candidate = copy.deepcopy(base)
        mutate(candidate)
        if should_rehash:
            rehash(candidate)
        try:
            validate_certificate(candidate)
        except (VerificationError, KeyError, TypeError, ValueError):
            passed += 1
        else:
            raise VerificationError(f"mutation escaped validation: {name}")

    parser_cases = {
        "duplicate": '{"schema":"a","schema":"b"}',
        "nan": '{"x":NaN}',
        "infinity": '{"x":Infinity}',
        "float": '{"x":1.0}',
        "overflow-float": '{"x":1e9999}',
    }
    for name, text in parser_cases.items():
        try:
            parse_json(text, name)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"parser mutation escaped: {name}")

    print(f"tamper_selftest=PASS ({passed}/{passed})")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--tamper-selftest", action="store_true")
    action.add_argument("--print-template", action="store_true")
    args = parser.parse_args()

    if args.print_template:
        print(json.dumps(expected_certificate(), indent=2, sort_keys=True))
        return
    if args.tamper_selftest:
        run_tamper_selftest()
        return

    data = load_json(CERT_PATH)
    validate_certificate(data)
    print(f"schema={SCHEMA}")
    print("field=GF(67^2), cyclic_domain_order=34")
    print("declared_rank9_selector=29/66 slopes, atlas_excess=165")
    print("complete_selector=66/66 slopes, affine_rank=2, carrier_excess=1")
    print("owner=CERTIFIED_LOW_EXCESS_COMMON_CARRIER")
    print("classification=EXACT_CYCLIC_TOY_CLOSURE_NO_LEDGER_MOVEMENT")
    print("check=PASS")


if __name__ == "__main__":
    main()
