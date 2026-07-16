#!/usr/bin/env python3
"""Verify the exhaustive M1 quadratic-parameter residual route cut.

The packet proves an exact restriction-of-scalars/scalarization statement for
the degree-two slope stratum and records why the currently available uniform
gates do not pay it.  It deliberately leaves U_2, U_Q, and U_A null.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-fp2-residual-route-cut-v1"
CERT_DIR = ROOT / "experimental/data/certificates/m1-fp2-residual-route-cut-v1"
CERT_PATH = CERT_DIR / "m1_fp2_residual_route_cut_v1.json"
NOTE_REL = Path("experimental/notes/m1/m1_fp2_residual_route_cut_v1.md")
VERIFIER_REL = Path("experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py")
SAGE_REL = Path("experimental/scripts/verify_m1_fp2_residual_route_cut_v1.sage")
FIRST_MATCH_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
)
BASE_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_base_slope_universe_v2.md"
)
BASE_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2/"
    "kb_mca_1116048_base_slope_universe_v2.json"
)
UNIFORM_CUT_REL = Path(
    "experimental/notes/m1/m1_extension_uniform_atlas_route_cut_v2.md"
)
UNIFORM_CERT_REL = Path(
    "experimental/data/certificates/m1-extension-uniform-atlas-route-cut-v2/"
    "m1_extension_uniform_atlas_route_cut_v2.json"
)
FIXED_LINE_REL = Path(
    "experimental/notes/frontier-adjacent/frontier_extension_fixed_line_audit_v1.md"
)
FIXED_LINE_CERT_REL = Path(
    "experimental/data/certificates/frontier-extension-fixed-line-audit-v1/"
    "frontier_extension_fixed_line_audit_v1.json"
)
COORDINATE_REL = Path("experimental/notes/f1/f1_extension_coordinate_transfer.md")
PROJECTIVE_REL = Path(
    "experimental/notes/thresholds/projective_syndrome_c5_first_match.md"
)
COMPLETE_ABSORPTION_REL = Path(
    "experimental/notes/thresholds/fixed_deficiency_complete_absorption.md"
)
PAPER_D_REL = Path("tex/cs25_cap_v12.tex")
THRESHOLDS_REL = Path("experimental/rs_mca_thresholds.tex")

P = 2_130_706_433
E = 6
P2 = P**2
Q = P**E
N = 2_097_152
K_DIM = 1_048_576
A = 1_116_048
J = N - A
T_SYNDROME = A - K_DIM
W = T_SYNDROME - 1
DEFICIENCY = N + K_DIM - 2 * A
B_STAR = Q // (1 << 128)
U_PAID = 2_602_153_473
B_REM = B_STAR - U_PAID
R2_UNIVERSE = P2 - P
R2_ORBITS = R2_UNIVERSE // 2

FIRST_MATCH_ORDER = [
    "contained_or_noncontained_failure",
    "rank_drop_or_pivot_failure",
    "tangent_common_line_residue",
    "quotient_periodic_or_divisor_stabilized",
    "planted_prefix_structured",
    "extension_valued_slope",
    "residual_base_slope_universe",
    "sparse_sigma_or_sparse_support",
    "m1_half_turn_or_coefficient_shadow",
    "primitive_qfin_residual",
]

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "row",
    "first_match_scope",
    "field_tower",
    "coordinate_transfer",
    "route_tests",
    "toy_control",
    "classification",
    "leaves",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}


class VerificationError(RuntimeError):
    """Raised for every fail-closed parser or semantic violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def require_int(value: Any, label: str) -> None:
    require(type(value) is int, f"{label} is not an exact JSON integer")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON value is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path.relative_to(ROOT)}")
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return canonical_hash(payload)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(binding_id: str, rel_path: Path, role: str) -> dict[str, str]:
    path = ROOT / rel_path
    require(path.is_file(), f"missing source binding: {rel_path}")
    return {
        "binding_id": binding_id,
        "path": rel_path.as_posix(),
        "sha256": file_hash(path),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("route-cut-note", NOTE_REL, "human-readable theorem and audit"),
        source_binding("python-verifier", VERIFIER_REL, "exact builder and mutation verifier"),
        source_binding("sage-replay", SAGE_REL, "independent F_49 replay"),
        source_binding("first-match-ledger", FIRST_MATCH_REL, "frozen owner order and open branch 6"),
        source_binding("base-slope-note", BASE_NOTE_REL, "current paid baseline and open complement"),
        source_binding("base-slope-certificate", BASE_CERT_REL, "machine-readable current ledger"),
        source_binding("uniform-atlas-route-cut", UNIFORM_CUT_REL, "row-uniform quantifier and d_eff wall"),
        source_binding("uniform-atlas-certificate", UNIFORM_CERT_REL, "machine-readable predecessor cut"),
        source_binding("fixed-line-correction", FIXED_LINE_REL, "Frobenius and dimension-degree correction"),
        source_binding("fixed-line-certificate", FIXED_LINE_CERT_REL, "machine-readable correction packet"),
        source_binding("coordinate-transfer", COORDINATE_REL, "exact support-wise restriction of scalars"),
        source_binding("projective-field-descent", PROJECTIVE_REL, "pair-field versus parameter-field guard"),
        source_binding("complete-absorption", COMPLETE_ABSORPTION_REL, "uniform fixed-deficiency envelope"),
        source_binding("paper-d", PAPER_D_REL, "restriction-of-scalars and dimension-degree theorems"),
        source_binding("thresholds", THRESHOLDS_REL, "MCA and Johnson/deep gate statements"),
    ]


# F_49 = F_7[u]/(u^2+1), encoded as (constant, u coefficient).
Elt = tuple[int, int]
P_TOY = 7
ZERO: Elt = (0, 0)
ONE: Elt = (1, 0)
U: Elt = (0, 1)


def fadd(left: Elt, right: Elt) -> Elt:
    return ((left[0] + right[0]) % P_TOY, (left[1] + right[1]) % P_TOY)


def fneg(value: Elt) -> Elt:
    return ((-value[0]) % P_TOY, (-value[1]) % P_TOY)


def fsub(left: Elt, right: Elt) -> Elt:
    return fadd(left, fneg(right))


def fmul(left: Elt, right: Elt) -> Elt:
    # u^2=-1.
    return (
        (left[0] * right[0] - left[1] * right[1]) % P_TOY,
        (left[0] * right[1] + left[1] * right[0]) % P_TOY,
    )


def fpow(value: Elt, exponent: int) -> Elt:
    require(exponent >= 0, "negative toy-field exponent")
    out = ONE
    base = value
    power = exponent
    while power:
        if power & 1:
            out = fmul(out, base)
        base = fmul(base, base)
        power >>= 1
    return out


def finv(value: Elt) -> Elt:
    require(value != ZERO, "toy-field division by zero")
    inverse = fpow(value, P_TOY**2 - 2)
    require(fmul(value, inverse) == ONE, "toy-field inverse failure")
    return inverse


def fdiv(left: Elt, right: Elt) -> Elt:
    return fmul(left, finv(right))


def lagrange_coefficients(points: list[Elt], values: list[Elt]) -> list[Elt]:
    require(len(points) == len(values) == 3, "toy interpolation needs three points")
    coefficients = [ZERO, ZERO, ZERO]
    for i in range(3):
        # Product_{j!=i} (X-x_j) = X^2-(x_j+x_k)X+x_j*x_k.
        others = [j for j in range(3) if j != i]
        xj, xk = points[others[0]], points[others[1]]
        numerator = [fmul(xj, xk), fneg(fadd(xj, xk)), ONE]
        denominator = fmul(fsub(points[i], xj), fsub(points[i], xk))
        scale = fdiv(values[i], denominator)
        for degree in range(3):
            coefficients[degree] = fadd(
                coefficients[degree], fmul(scale, numerator[degree])
            )
    return coefficients


def eval_poly(coefficients: list[Elt], point: Elt) -> Elt:
    out = ZERO
    for coefficient in reversed(coefficients):
        out = fadd(fmul(out, point), coefficient)
    return out


def explained(word: list[Elt], support: tuple[int, ...]) -> bool:
    points = [((index + 1) % P_TOY, 0) for index in support[:3]]
    values = [word[index] for index in support[:3]]
    polynomial = lagrange_coefficients(points, values)
    return all(
        eval_poly(polynomial, ((index + 1) % P_TOY, 0)) == word[index]
        for index in support
    )


def encode(value: Elt) -> list[int]:
    return [value[0], value[1]]


def derive_toy_control() -> dict[str, Any]:
    require(all((x * x + 1) % P_TOY != 0 for x in range(P_TOY)), "X^2+1 reducible")
    domain = list(range(1, 7))
    f_word = [fneg(U), ZERO, ZERO, ZERO, ZERO, ONE]
    g_word = [ONE, ZERO, ZERO, ZERO, ZERO, ZERO]
    supports = list(itertools.combinations(range(6), 5))
    records: list[dict[str, Any]] = []
    for c0 in range(P_TOY):
        for c1 in range(P_TOY):
            slope = (c0, c1)
            word = [fadd(f_word[index], fmul(slope, g_word[index])) for index in range(6)]
            for support in supports:
                if explained(word, support) and not (
                    explained(f_word, support) and explained(g_word, support)
                ):
                    records.append(
                        {
                            "slope_encoded": encode(slope),
                            "support_indices": list(support),
                            "support_domain_points": [domain[index] for index in support],
                        }
                    )
    require(
        records
        == [
            {
                "slope_encoded": [0, 1],
                "support_indices": [0, 1, 2, 3, 4],
                "support_domain_points": [1, 2, 3, 4, 5],
            }
        ],
        "F_49 bad-slope census drift",
    )
    conjugate = fpow(U, P_TOY)
    support = tuple(records[0]["support_indices"])
    return {
        "purpose": "FIXED_LINE_FROBENIUS_CLOSURE_FALSIFIER_ONLY",
        "field": {
            "base_order": P_TOY,
            "extension_degree": 2,
            "order": P_TOY**2,
            "modulus_coefficients_low_to_high": [1, 0, 1],
            "modulus_irreducible": True,
            "basis": ["1", "a"],
        },
        "code": {
            "domain": domain,
            "n": 6,
            "k": 3,
            "agreement_A": 5,
        },
        "received_line": {
            "f_values_encoded": [encode(value) for value in f_word],
            "g_values_encoded": [encode(value) for value in g_word],
            "formula": "f=(-a,0,0,0,0,1), g=(1,0,0,0,0,0)",
        },
        "exact_census": {
            "slopes_enumerated": P_TOY**2,
            "supports_per_slope": len(supports),
            "bad_records": records,
            "bad_slope_count": len(records),
            "a_frobenius_encoded": encode(conjugate),
            "a_frobenius_equals_minus_a": conjugate == fneg(U),
            "bad_set_frobenius_stable": False,
        },
        "support_checks": {
            "f_restriction_is_codeword": explained(f_word, support),
            "g_restriction_is_codeword": explained(g_word, support),
            "simultaneously_explained": explained(f_word, support)
            and explained(g_word, support),
            "deployed_first_match_survival_proved": False,
        },
        "verdict": "BAD_SET_EQUALS_SINGLETON_A_NOT_FIXED_BY_FROBENIUS",
    }


def leaf(index: int) -> dict[str, Any]:
    return {
        "leaf_id": f"R2_FIRST_NONCONTAINED_COORDINATE_{index}",
        "first_noncontained_coordinate": index,
        "witness_assignment_rule": "WITHIN_EACH_WITNESS_LEAST_NONCONTAINED_K_COORDINATE",
        "slope_leaf_disjointness_proved": False,
        "equation_family": {
            "quantifiers": "FOR_ALL_F_G_FOR_ALL_SURVIVING_A_SUPPORTS_EXISTS_P0_P1_P2",
            "slope_equations": ["gamma^(p^2)-gamma=0", "gamma^p-gamma!=0"],
            "product_explanation": "f_j+gamma*g_j=P_j_on_S_for_j=0,1,2_deg(P_j)<k",
            "earlier_coordinate_containment": f"coordinates_0_through_{index - 1}_contained_on_S"
            if index > 0
            else "VACUOUS",
            "selected_coordinate_noncontainment": f"(f_{index},g_{index})_not_simultaneously_explained_on_S",
            "original_first_match_mask_interface": "ABSTRACT_Z_LT_6_SET_DIFFERENCE_FROM_BOUND_FIRST_MATCH_POLICY",
            "first_match_mask_predicates_machine_encoded": False,
            "fixed_support_quotient_equation": "ybar_0+gamma*ybar_1=0_with_pair_not_both_zero",
            "fixed_support_root_cap": 1,
            "source_binding_ids": ["coordinate-transfer", "thresholds", "first-match-ledger"],
        },
        "terminal": {
            "kind": "UNPAID_TOWER_DEGREE_2",
            "reason": "EXACT_ARITY3_DIAGONAL_RETYPE_NO_EXISTING_BAND_OWNER",
            "owner_id": None,
            "charge_id": None,
            "numeric_charge": None,
            "missing_lemma": "ROW_UNIFORM_DEDUPLICATED_SUPPORT_TO_SLOPE_UNION_BOUND",
            "scalarization_and_incidence_equations_bound": True,
            "first_match_mask_equations_bound": False,
        },
    }


EDGE_CASES = [
    "Slope field, pair projective-syndrome field, and eliminant coefficient field are distinct.",
    "The first five branch masks are carried literally and are not declared paid by this packet.",
    "The least-coordinate witness assignment is disjoint, but projected scalar bad-slope sets may overlap.",
    "Class exhaustivity is relative to the declared post-5 residual predicate; this packet does not replay branch-1-through-5 mask equations.",
    "Root deduplication is within one received line; across lines the operation is a supremum or maximum.",
    "The F_49 singleton has not been proved to survive the deployed earlier first-match branches.",
    "The two-column fixed-support system does not imply d_eff<=1 after unioning supports.",
    "Finite infinity is excluded and null is not zero.",
]

REMAINING_RISKS = [
    "The branch-1-through-5 mask adapter is set-theoretic rather than machine-encoded in this packet.",
    "No source-derived deployed eliminant or support-to-slope union bound exists for this class.",
    "Coordinate projection does not automatically preserve an earlier paid-owner label.",
    "A future small exact-root union or structural owner could close R2 without contradicting this route cut.",
    "U_Q and the rest of U_A remain open, so even an R2 payment would not close the row.",
]

NONCLAIMS = [
    "The packet does not prove that every received pair or witness descends to F_(p^2).",
    "The packet does not pay a three-interleaved or scalar F_(p^2) MCA owner.",
    "The packet does not prove d_eff<=1 or a budget-fitting exact-root union.",
    "The F_49 control is not a deployed KoalaBear witness or first-match survivor.",
    "The raw universe and hypothetical orbit counts are route cuts, not lower bounds on the actual residual.",
    "The packet does not assign U_2, U_Q, or U_A, change the ledger, or improve the public frontier.",
]


def build_certificate() -> dict[str, Any]:
    leaves = [leaf(index) for index in range(3)]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": "M1_FP2_RESIDUAL_ROUTE_CUT",
        "status": "PROVED_SCALARIZATION_MASK_RELATIVE_CLASS_EXHAUSTIVE_UNPAID_ROW_OPEN",
        "source_bindings": expected_source_bindings(),
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "ambient_extension_degree": E,
            "q": str(Q),
            "n": N,
            "k": K_DIM,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T_SYNDROME,
            "prefix_depth_w": W,
            "deficiency_d": DEFICIENCY,
            "B_star": str(B_STAR),
            "U_paid": str(U_PAID),
            "B_remaining": str(B_REM),
            "U_Q": None,
            "U_A": None,
        },
        "first_match_scope": {
            "policy_id": "KB_MCA_1116048_FIRST_MATCH_LEDGER_V2_BASE_SLOPE_REPLACEMENT",
            "order": FIRST_MATCH_ORDER,
            "active_branch_number": 6,
            "active_branch": "extension_valued_slope",
            "earlier_branch_count": 5,
            "earlier_assignments_removed_by_actual_slope_projection": True,
            "earlier_branches_all_paid_claimed": False,
            "post5_residual_definition": "Z_a(f,g)_MINUS_UNION_OF_ACTUAL_BRANCH_1_THROUGH_5_SLOPE_PROJECTIONS",
            "mask_predicates_machine_encoded": False,
            "mask_adapter_status": "NOT_SUPPLIED_IN_THIS_PACKET",
            "received_pairs": "ALL_ADMISSIBLE_F_(p^6)_VALUED_PAIRS",
            "supports": "ALL_SURVIVING_SUPPORT_WITNESSES_OF_SIZE_AT_LEAST_A_REDUCED_TO_EXACT_A",
            "slopes": "ALL_FINITE_GAMMA_IN_F_(p^2)_MINUS_F_p",
            "within_line_aggregation": "DISJOINT_FIRST_MATCH_THEN_EXACT_ROOT_UNION_DEDUPLICATION",
            "across_line_aggregation": "SUPREMUM_OR_MAXIMUM",
            "sampled_atlas": False,
        },
        "field_tower": {
            "base_field": "F_p",
            "parameter_field": "F_(p^2)",
            "ambient_value_field": "F_(p^6)",
            "degrees": {"parameter_over_base": 2, "ambient_over_parameter": 3, "ambient_over_base": 6},
            "parameter_field_order": str(P2),
            "proper_degree_two_stratum_size": str(R2_UNIVERSE),
            "membership_equation": "gamma^(p^2)-gamma=0",
            "nonbase_inequation": "gamma^p-gamma!=0",
            "minimal_extension_degree_partition": [2, 3, 6],
            "unique_degree_two_intermediate_field": True,
            "parameter_field_only": True,
            "received_pair_descent_inferred": False,
            "projective_syndrome_descent_inferred": False,
        },
        "coordinate_transfer": {
            "basis_field": "F_(p^2)",
            "basis_length": 3,
            "interleaving_arity": 3,
            "multiplication_matrix_for_gamma_in_parameter_field": "gamma*I_3",
            "line_formula": "Psi_K(f+gamma*g)=(f_i+gamma*g_i)_(i=0,1,2)",
            "code_formula": "Psi_K(RS_F(D,k))=RS_K(D,k)^3",
            "support_and_noncontainment_preserved": True,
            "canonical_witness_leaf_rule": "WITHIN_EACH_WITNESS_LEAST_NONCONTAINED_K_COORDINATE",
            "slope_leaf_disjointness_proved": False,
            "slope_leaf_aggregation": "EXACT_WITHIN_LINE_UNION_DEDUPLICATION_REQUIRED",
            "leaf_indices": [0, 1, 2],
            "raw_equation_rows": 3 * A,
            "raw_equation_columns": 3 * K_DIM + 1,
            "reduced_syndrome_equations": 3 * (A - K_DIM),
            "reduced_affine_parameter_columns": 2,
            "fixed_support_root_cap": 1,
            "fixed_support_cap_extends_to_support_union": False,
            "is_positive_MCA_bound": False,
        },
        "route_tests": {
            "deep_gate": {
                "lhs_3j": 3 * J,
                "rhs_n_minus_k": N - K_DIM,
                "holds": 3 * J <= N - K_DIM,
            },
            "half_distance_gate": {
                "lhs_2j": 2 * J,
                "rhs_n_minus_k": N - K_DIM,
                "holds": 2 * J <= N - K_DIM,
            },
            "johnson_gate": {
                "A_squared": str(A**2),
                "k_minus_1_times_n": str((K_DIM - 1) * N),
                "holds": A**2 > (K_DIM - 1) * N,
            },
            "complete_absorption": {
                "original_deficiency": DEFICIENCY,
                "required_effective_deficiency_for_bare_binomial": 1,
                "effective_deficiency_collapse_proved": False,
            },
            "raw_parameter_universe": {
                "size": str(R2_UNIVERSE),
                "B_remaining": str(B_REM),
                "excess": str(R2_UNIVERSE - B_REM),
                "fits": R2_UNIVERSE <= B_REM,
                "coarse_exact_root_polynomial": "(Z^(p^2)-Z)/(Z^p-Z)",
                "coarse_exact_root_degree": str(R2_UNIVERSE),
                "coarse_exact_root_union_fits": R2_UNIVERSE <= B_REM,
            },
            "hypothetical_frobenius_orbit_relaxation": {
                "valid_for_arbitrary_fixed_lines": False,
                "orbit_count": str(R2_ORBITS),
                "orbit_count_excess_over_B_remaining": str(R2_ORBITS - B_REM),
                "even_one_unit_per_orbit_fits": R2_ORBITS <= B_REM,
                "actual_root_degree_if_orbit_union": str(R2_UNIVERSE),
            },
            "dimension_degree": {
                "p_squared": str(P2),
                "positive_degree_e_Y_ge_2_fits": P2 <= B_REM,
                "provisional_max_Delta_if_e_Y_1": B_REM // P,
                "allocation_assumption": "U_Q=U_A_other=0_PROVISIONAL_ONLY",
            },
            "decision": "NO_EXISTING_ROUTE_PAYS_R2",
        },
        "toy_control": derive_toy_control(),
        "classification": {
            "class_id": "KB_MCA_A1116048_BRANCH6_MINIMAL_SLOPE_FIELD_DEGREE_2",
            "declared_post5_residual_class_complete": True,
            "deployed_mask_replay_complete": False,
            "coverage_scope": "RELATIVE_TO_ABSTRACT_POST5_RESIDUAL_PREDICATE",
            "class_closed": False,
            "leaf_count": len(leaves),
            "leaf_ids_sha256": canonical_hash([entry["leaf_id"] for entry in leaves]),
            "all_leaves_have_exact_scalarization_equation_family": True,
            "all_leaves_have_machine_encoded_first_match_masks": False,
            "all_leaves_have_exactly_one_terminal": True,
            "all_terminals": "UNPAID_TOWER_DEGREE_2",
            "terminal_reason": "EXACT_ARITY3_DIAGONAL_RETYPE_NO_EXISTING_BAND_OWNER",
        },
        "leaves": leaves,
        "ledger": {
            "U_2": None,
            "U_Q": None,
            "U_A": None,
            "class_charge": None,
            "class_charge_bankable": False,
            "row_complete": False,
            "ledger_consequence": False,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
            "next_attack": "ROW_UNIFORM_DEDUPLICATED_TWO_COLUMN_SUPPORT_TO_SLOPE_UNION",
        },
        "audit_sections": {
            "parameter_dependence": "STRUCTURAL_TRANSFER_UNIFORM_BUDGET_TESTS_ROW_SPECIFIC",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "numerical_evidence": "EXACT_INTEGER_ARITHMETIC_AND_EXHAUSTIVE_TOY_CONTROL_ONLY",
            "edge_cases": EDGE_CASES,
            "remaining_risks": REMAINING_RISKS,
        },
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list, "source_bindings is not a list")
    expected = expected_source_bindings()
    require(bindings == expected, "source binding path/hash/role drift")
    ids = [entry["binding_id"] for entry in bindings]
    require(len(ids) == len(set(ids)), "duplicate source binding id")


def validate(artifact: dict[str, Any], *, exact_rebuild: bool = True) -> None:
    require(set(artifact) == TOP_KEYS, "top-level keys drift")
    require(artifact["schema"] == SCHEMA, "schema drift")
    require(artifact["artifact_kind"] == "M1_FP2_RESIDUAL_ROUTE_CUT", "artifact kind drift")
    require(
        artifact["status"]
        == "PROVED_SCALARIZATION_MASK_RELATIVE_CLASS_EXHAUSTIVE_UNPAID_ROW_OPEN",
        "status drift",
    )
    validate_source_bindings(artifact["source_bindings"])

    row = artifact["row"]
    for key in (
        "p",
        "ambient_extension_degree",
        "n",
        "k",
        "agreement_A",
        "error_count_j",
        "syndrome_depth_t",
        "prefix_depth_w",
        "deficiency_d",
    ):
        require_int(row[key], f"row.{key}")
    require(row["p"] == P and row["ambient_extension_degree"] == E, "field row drift")
    require(row["n"] == N and row["k"] == K_DIM and row["agreement_A"] == A, "row drift")
    require(row["error_count_j"] == J and row["syndrome_depth_t"] == T_SYNDROME, "row derived drift")
    require(row["deficiency_d"] == DEFICIENCY, "deficiency drift")
    require(int(row["q"]) == Q and int(row["B_star"]) == B_STAR, "budget field drift")
    require(int(row["U_paid"]) == U_PAID and int(row["B_remaining"]) == B_REM, "paid ledger drift")
    require(row["U_Q"] is None and row["U_A"] is None, "open row terms changed from null")

    scope = artifact["first_match_scope"]
    require(
        scope["policy_id"]
        == "KB_MCA_1116048_FIRST_MATCH_LEDGER_V2_BASE_SLOPE_REPLACEMENT",
        "first-match policy id drift",
    )
    require(scope["order"] == FIRST_MATCH_ORDER, "first-match order drift")
    base_certificate = load_json(ROOT / BASE_CERT_REL)
    require(
        base_certificate["first_match"]["v2_order"] == FIRST_MATCH_ORDER,
        "first-match order does not match the bound base-v2 certificate",
    )
    require(scope["active_branch_number"] == 6, "active branch drift")
    require(scope["earlier_branch_count"] == 5, "earlier branch count drift")
    require(scope["earlier_assignments_removed_by_actual_slope_projection"] is True, "prior mask drift")
    require(scope["earlier_branches_all_paid_claimed"] is False, "prior owners falsely declared paid")
    require(scope["mask_predicates_machine_encoded"] is False, "first-match masks falsely encoded")
    require(scope["mask_adapter_status"] == "NOT_SUPPLIED_IN_THIS_PACKET", "mask adapter overclaim")
    require(scope["received_pairs"] == "ALL_ADMISSIBLE_F_(p^6)_VALUED_PAIRS", "all-pair scope drift")
    require(scope["across_line_aggregation"] == "SUPREMUM_OR_MAXIMUM", "cross-line aggregation drift")
    require(scope["sampled_atlas"] is False, "sampled atlas promoted")

    tower = artifact["field_tower"]
    require(tower["degrees"] == {"parameter_over_base": 2, "ambient_over_parameter": 3, "ambient_over_base": 6}, "tower degree drift")
    require(int(tower["parameter_field_order"]) == P2, "parameter field order drift")
    require(int(tower["proper_degree_two_stratum_size"]) == R2_UNIVERSE, "R2 cardinality drift")
    require(tower["membership_equation"] == "gamma^(p^2)-gamma=0", "membership equation drift")
    require(tower["nonbase_inequation"] == "gamma^p-gamma!=0", "base exclusion drift")
    require(tower["received_pair_descent_inferred"] is False, "pair descent overclaim")

    transfer = artifact["coordinate_transfer"]
    require(transfer["basis_length"] == transfer["interleaving_arity"] == 3, "arity drift")
    require(transfer["multiplication_matrix_for_gamma_in_parameter_field"] == "gamma*I_3", "diagonal action drift")
    require(transfer["support_and_noncontainment_preserved"] is True, "support transfer drift")
    require(transfer["leaf_indices"] == [0, 1, 2], "coordinate leaf drift")
    require(transfer["slope_leaf_disjointness_proved"] is False, "witness leaves promoted to disjoint slope leaves")
    require(
        transfer["slope_leaf_aggregation"]
        == "EXACT_WITHIN_LINE_UNION_DEDUPLICATION_REQUIRED",
        "slope-leaf aggregation drift",
    )
    require(transfer["raw_equation_rows"] == 3 * A, "raw equation rows drift")
    require(transfer["raw_equation_columns"] == 3 * K_DIM + 1, "raw equation columns drift")
    require(transfer["reduced_syndrome_equations"] == 3 * T_SYNDROME, "syndrome equation count drift")
    require(transfer["fixed_support_root_cap"] == 1, "fixed support cap drift")
    require(transfer["fixed_support_cap_extends_to_support_union"] is False, "fixed-support cap promoted")
    require(transfer["is_positive_MCA_bound"] is False, "retyping promoted to payment")

    routes = artifact["route_tests"]
    require(routes["deep_gate"]["holds"] is False and routes["deep_gate"]["lhs_3j"] == 3 * J, "deep gate drift")
    require(routes["half_distance_gate"]["holds"] is False and routes["half_distance_gate"]["lhs_2j"] == 2 * J, "half-distance gate drift")
    require(routes["johnson_gate"]["holds"] is False, "Johnson gate promoted")
    require(int(routes["johnson_gate"]["A_squared"]) == A**2, "Johnson lhs drift")
    require(int(routes["johnson_gate"]["k_minus_1_times_n"]) == (K_DIM - 1) * N, "Johnson rhs drift")
    require(routes["complete_absorption"]["original_deficiency"] == DEFICIENCY, "complete deficiency drift")
    require(routes["complete_absorption"]["required_effective_deficiency_for_bare_binomial"] == 1, "d_eff wall drift")
    require(routes["complete_absorption"]["effective_deficiency_collapse_proved"] is False, "d_eff collapse invented")
    raw = routes["raw_parameter_universe"]
    require(int(raw["size"]) == R2_UNIVERSE, "raw universe drift")
    require(int(raw["excess"]) == R2_UNIVERSE - B_REM, "raw excess drift")
    require(raw["fits"] is False and raw["coarse_exact_root_union_fits"] is False, "raw universe falsely fits")
    orbit = routes["hypothetical_frobenius_orbit_relaxation"]
    require(orbit["valid_for_arbitrary_fixed_lines"] is False, "fixed-line Frobenius closure invented")
    require(int(orbit["orbit_count"]) == R2_ORBITS, "orbit count drift")
    require(orbit["even_one_unit_per_orbit_fits"] is False, "orbit relaxation falsely fits")
    dimension = routes["dimension_degree"]
    require(dimension["positive_degree_e_Y_ge_2_fits"] is False, "e_Y>=2 falsely fits")
    require(dimension["provisional_max_Delta_if_e_Y_1"] == B_REM // P, "e_Y=1 cap drift")
    require(routes["decision"] == "NO_EXISTING_ROUTE_PAYS_R2", "route decision drift")

    require(artifact["toy_control"] == derive_toy_control(), "toy control drift")
    classification = artifact["classification"]
    require(classification["declared_post5_residual_class_complete"] is True, "declared R2 class not exhaustive")
    require(classification["deployed_mask_replay_complete"] is False, "deployed mask replay overclaim")
    require(
        classification["coverage_scope"] == "RELATIVE_TO_ABSTRACT_POST5_RESIDUAL_PREDICATE",
        "relative coverage scope drift",
    )
    require(classification["class_closed"] is False, "unpaid class falsely closed")
    require(classification["leaf_count"] == 3, "leaf count drift")
    leaves = artifact["leaves"]
    require(type(leaves) is list and len(leaves) == 3, "leaf list drift")
    require(leaves == [leaf(index) for index in range(3)], "leaf equation/terminal drift")
    require(
        classification["leaf_ids_sha256"]
        == canonical_hash([entry["leaf_id"] for entry in leaves]),
        "leaf assignment digest drift",
    )

    ledger = artifact["ledger"]
    require(ledger["U_2"] is None and ledger["U_Q"] is None and ledger["U_A"] is None, "null ledger term changed")
    require(ledger["class_charge"] is None and ledger["class_charge_bankable"] is False, "unpaid class charged")
    require(ledger["row_complete"] is False and ledger["ledger_consequence"] is False, "row closure overclaim")
    audit = artifact["audit_sections"]
    require(audit["layer_cake_dyadic_summability"] == "NOT_APPLICABLE", "layer-cake drift")
    require(audit["moment_markov_chebyshev"] == "NOT_APPLICABLE", "moment drift")
    require(audit["edge_cases"] == EDGE_CASES, "edge-case caveats drift")
    require(audit["remaining_risks"] == REMAINING_RISKS, "remaining-risk caveats drift")
    require(artifact["nonclaims"] == NONCLAIMS, "nonclaims drift")
    require(artifact["payload_sha256"] == payload_hash(artifact), "payload hash drift")

    if exact_rebuild:
        require(canonical_bytes(artifact) == canonical_bytes(build_certificate()), "deterministic certificate rebuild drift")


def expect_reject(name: str, artifact: dict[str, Any]) -> None:
    try:
        validate(artifact)
    except (VerificationError, KeyError, TypeError, ValueError):
        return
    raise VerificationError(f"tamper accepted: {name}")


def run_tamper_selftest(artifact: dict[str, Any]) -> int:
    cases: list[tuple[str, dict[str, Any]]] = []

    def mutate(name: str, path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(artifact)
        target: Any = candidate
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        candidate["payload_sha256"] = payload_hash(candidate)
        cases.append((name, candidate))

    mutate("ambient-degree-to-two", ("field_tower", "degrees", "ambient_over_base"), 2)
    mutate("parameter-degree-to-three", ("field_tower", "degrees", "parameter_over_base"), 3)
    mutate("arity-three-to-two", ("coordinate_transfer", "interleaving_arity"), 2)
    mutate("pair-falsely-descends", ("field_tower", "received_pair_descent_inferred"), True)
    mutate("omit-nonbase-equation", ("field_tower", "nonbase_inequation"), "OMITTED")
    mutate("raw-p2-not-p2-minus-p", ("field_tower", "proper_degree_two_stratum_size"), str(P2))
    mutate("branch-six-to-seven", ("first_match_scope", "active_branch_number"), 7)
    mutate("owner-order-swap", ("first_match_scope", "order"), FIRST_MATCH_ORDER[::-1])
    mutate("prior-masks-not-literal", ("first_match_scope", "earlier_assignments_removed_by_actual_slope_projection"), False)
    mutate("prior-branches-called-paid", ("first_match_scope", "earlier_branches_all_paid_claimed"), True)
    mutate("sampled-lines", ("first_match_scope", "received_pairs"), "ONE_SAMPLED_PAIR")
    mutate("average-across-lines", ("first_match_scope", "across_line_aggregation"), "AVERAGE")
    mutate("sampled-atlas-promoted", ("first_match_scope", "sampled_atlas"), True)
    mutate("fixed-support-cap-unioned", ("coordinate_transfer", "fixed_support_cap_extends_to_support_union"), True)
    mutate("retyping-called-payment", ("coordinate_transfer", "is_positive_MCA_bound"), True)
    mutate("deep-gate-overclaim", ("route_tests", "deep_gate", "holds"), True)
    mutate("half-gate-overclaim", ("route_tests", "half_distance_gate", "holds"), True)
    mutate("johnson-overclaim", ("route_tests", "johnson_gate", "holds"), True)
    mutate("d-eff-two", ("route_tests", "complete_absorption", "required_effective_deficiency_for_bare_binomial"), 2)
    mutate("d-eff-collapse-invented", ("route_tests", "complete_absorption", "effective_deficiency_collapse_proved"), True)
    mutate("raw-universe-fits", ("route_tests", "raw_parameter_universe", "fits"), True)
    mutate("orbit-closure-invented", ("route_tests", "hypothetical_frobenius_orbit_relaxation", "valid_for_arbitrary_fixed_lines"), True)
    mutate("orbit-count-banked", ("route_tests", "hypothetical_frobenius_orbit_relaxation", "even_one_unit_per_orbit_fits"), True)
    mutate("dimension-two-fits", ("route_tests", "dimension_degree", "positive_degree_e_Y_ge_2_fits"), True)
    mutate("class-incomplete", ("classification", "declared_post5_residual_class_complete"), False)
    mutate("mask-replay-overclaim", ("classification", "deployed_mask_replay_complete"), True)
    mutate("class-falsely-closed", ("classification", "class_closed"), True)
    mutate("omit-leaf", ("leaves",), artifact["leaves"][:2])
    duplicate_leaves = copy.deepcopy(artifact["leaves"])
    duplicate_leaves[2] = copy.deepcopy(duplicate_leaves[1])
    mutate("duplicate-leaf", ("leaves",), duplicate_leaves)
    mutate("generic-unpaid-terminal", ("leaves", 0, "terminal", "kind"), "UNPAID_PRIMITIVE")
    mutate("unpaid-zero-charge", ("leaves", 0, "terminal", "numeric_charge"), 0)
    mutate("unpaid-missing-incidence-equations", ("leaves", 0, "terminal", "scalarization_and_incidence_equations_bound"), False)
    mutate("unpaid-mask-equations-invented", ("leaves", 0, "terminal", "first_match_mask_equations_bound"), True)
    mutate("U2-null-to-zero", ("ledger", "U_2"), "0")
    mutate("UQ-null-to-zero", ("ledger", "U_Q"), "0")
    mutate("UA-null-to-zero", ("ledger", "U_A"), "0")
    mutate("bank-unpaid-class", ("ledger", "class_charge_bankable"), True)
    mutate("row-complete-overclaim", ("ledger", "row_complete"), True)
    mutate("toy-promoted-to-deployed", ("toy_control", "purpose"), "DEPLOYED_PAYMENT")
    mutate("toy-orbit-stable", ("toy_control", "exact_census", "bad_set_frobenius_stable"), True)
    mutate("source-hash-drift", ("source_bindings", 0, "sha256"), "0" * 64)
    mutate("erase-edge-cases", ("audit_sections", "edge_cases"), ["none"])
    mutate("erase-risks", ("audit_sections", "remaining_risks"), ["none"])
    mutate("erase-nonclaims", ("nonclaims",), ["none"])

    unknown = copy.deepcopy(artifact)
    unknown["unknown_field"] = True
    unknown["payload_sha256"] = payload_hash(unknown)
    cases.append(("unknown-key", unknown))

    bad_payload = copy.deepcopy(artifact)
    bad_payload["payload_sha256"] = "0" * 64
    cases.append(("payload-hash", bad_payload))

    bool_as_int = copy.deepcopy(artifact)
    bool_as_int["row"]["agreement_A"] = True
    bool_as_int["payload_sha256"] = payload_hash(bool_as_int)
    cases.append(("bool-as-integer", bool_as_int))

    for name, candidate in cases:
        expect_reject(name, candidate)

    parser_cases = 0
    for text, name in [
        ('{"schema":1,"schema":1}', "duplicate-key"),
        ('{"x":NaN}', "nonstandard-constant"),
    ]:
        try:
            parse_json(text, name)
        except VerificationError:
            parser_cases += 1
        else:
            raise VerificationError(f"tamper accepted: {name}")
    return len(cases) + parser_cases


def emit() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    artifact = build_certificate()
    CERT_PATH.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {CERT_PATH.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.emit:
        emit()
        return 0

    artifact = load_json(CERT_PATH)
    validate(artifact)
    if args.tamper_selftest:
        rejected = run_tamper_selftest(artifact)
        print(f"M1_FP2_RESIDUAL_ROUTE_CUT_V1_TAMPER_PASS rejected={rejected}/{rejected}")
    else:
        print("M1_FP2_RESIDUAL_ROUTE_CUT_V1_VERIFY_PASS")
        print(
            "R2 universe=%d B_remaining=%d; diagonal arity=3 leaves=3"
            % (R2_UNIVERSE, B_REM)
        )
        print(
            "gates: deep=%s half=%s johnson=%s; d=%d; U_2/U_Q/U_A remain null"
            % (
                3 * J <= N - K_DIM,
                2 * J <= N - K_DIM,
                A**2 > (K_DIM - 1) * N,
                DEFICIENCY,
            )
        )
        print(
            "terminal: UNPAID_TOWER_DEGREE_2 "
            "(declared post-5 class exhaustive; mask replay and row open)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
