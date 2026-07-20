#!/usr/bin/env python3
"""Verify the active-source matroid reindex and its exact route cuts.

The companion note contains the proofs.  This checker freezes the exact
KoalaBear arithmetic, enumerates sharp representable-matroid controls, binds
the predecessor source-load packet, and binds the exact GF(67^2) rank-nine
outside-carrier countercontrol.  It makes no deployed payment claim.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_projective_source_load_v1 as base
import verify_m1_rank9_rank1_regular_source_load_control_v1 as rank_one_control


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-rank9-active-source-matroid-reindex-v1"
STATUS = (
    "PROVED_ACTIVE_SOURCE_SPLIT_AND_SHARP_MATROID_REINDEX_"
    "DEPLOYED_PAYMENT_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates"
    / "m1-kb-rank9-active-source-matroid-reindex-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_active_source_matroid_reindex_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_active_source_matroid_reindex_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-active-source-matroid-reindex-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py"
)
PROJECTIVE_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-rank9-projective-source-load-v1/"
    "m1_kb_rank9_projective_source_load_v1.json"
)
PROJECTIVE_PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py"
)
DEPLOYED_HELPER_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py"
)
CYCLIC_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-cyclic-rich-pencil-control-v1/"
    "m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.json"
)
CYCLIC_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.md"
)
CYCLIC_SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.sage"
)
CYCLIC_PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py"
)
RANK_ONE_PYTHON_REL = Path(
    "experimental/scripts/verify_m1_rank9_rank1_regular_source_load_control_v1.py"
)
RANK_ONE_SAGE_REL = Path(
    "experimental/scripts/verify_m1_rank9_rank1_regular_source_load_control_v1.sage"
)
ROW_DESCRIPTOR_REL = Path(
    "experimental/scripts/verify_koalabear_frontier_adjacent.py"
)

PROJECTIVE_PAYLOAD = (
    "4f3d3cf162c516c58b5b979cc7a3ba36be3a9e9ed622239b14408f0022ed2267"
)
CYCLIC_PAYLOAD = (
    "8a7bb260aab1dfaaab146d587dca0d063e2c6123eaa6ae5fcb01a0e927d61009"
)

N = base.N
K = base.K
A = base.A
R = base.R
J = base.J
T = base.T
E_MAX = base.E_MAX
MIN_PLANT = T - (J // 20) + 1
MAX_UNIVERSAL_FOR_ALL_ACTIVE = MIN_PLANT - 1
FULL_OUTSIDE_BETA_CAP = math.comb(K - 2, 8)
FULL_OUTSIDE_BREAK_J = 20 + E_MAX // FULL_OUTSIDE_BETA_CAP + 1
FULL_OUTSIDE_BREAK_EXCESS = (
    FULL_OUTSIDE_BETA_CAP * (FULL_OUTSIDE_BREAK_J - 20) - E_MAX
)

ContractError = base.ContractError
require = base.require
payload_hash = base.payload_hash
source_binding = base.source_binding
matrix_rank_mod = base.matrix_rank_mod


def exact_int(value: Any, label: str) -> int:
    require(type(value) is int, f"{label} is not an exact integer")
    return value


def enumerate_matroid_bases(
    rows: list[list[int]], rank: int, prime: int
) -> list[tuple[int, ...]]:
    require(all(len(row) == rank for row in rows), "matroid row width")
    require(matrix_rank_mod(rows, prime) == rank, "matroid lost full rank")
    return [
        basis
        for basis in itertools.combinations(range(len(rows)), rank)
        if matrix_rank_mod([rows[index] for index in basis], prime) == rank
    ]


def matroid_counts(
    rows: list[list[int]], active_indices: set[int], rank: int, prime: int
) -> dict[str, int | str]:
    require(active_indices, "active set must be nonempty")
    require(all(any(rows[index]) for index in active_indices), "active loop")
    bases = enumerate_matroid_bases(rows, rank, prime)
    beta_0 = sum(not (set(basis) & active_indices) for basis in bases)
    beta_1 = sum(
        len(set(basis) & active_indices) == 1 for basis in bases
    )
    beta_hit = len(bases) - beta_0
    z = len(rows)
    r = len(active_indices)
    rhs_factor = max(0, z - r - (rank - 1))
    require(r * beta_0 <= rhs_factor * beta_1, "exchange inequality failed")
    coefficient = max(Fraction(1), Fraction(z - (rank - 1), r))
    require(
        Fraction(len(bases)) <= coefficient * beta_hit,
        "basis-hit corollary failed",
    )
    return {
        "rank": rank,
        "ground_size_z": z,
        "active_size_r": r,
        "beta": len(bases),
        "beta_0": beta_0,
        "beta_1": beta_1,
        "beta_hit": beta_hit,
        "exchange_lhs": r * beta_0,
        "exchange_rhs": rhs_factor * beta_1,
        "C_numerator": coefficient.numerator,
        "C_denominator": coefficient.denominator,
    }


def sharp_parallel_control(z: int, r: int) -> dict[str, int | str | bool]:
    rank = 8
    require(z >= rank and 1 <= r <= z - 7, "invalid sharp control")
    prime = 101
    rows: list[list[int]] = []
    for coordinate in range(7):
        row = [0] * rank
        row[coordinate] = 1
        rows.append(row)
    parallel = [0] * rank
    parallel[7] = 1
    rows.extend([parallel.copy() for _ in range(z - 7)])
    active = set(range(z - r, z))
    result = matroid_counts(rows, active, rank, prime)
    require(result["beta_0"] == z - r - 7, "sharp beta_0 drift")
    require(result["beta_1"] == r, "sharp beta_1 drift")
    require(result["beta_hit"] == r, "sharp beta_hit drift")
    require(
        result["exchange_lhs"] == result["exchange_rhs"],
        "sharp exchange lost equality",
    )
    require(
        Fraction(exact_int(result["beta"], "beta"), 1)
        == Fraction(
            exact_int(result["C_numerator"], "C numerator"),
            exact_int(result["C_denominator"], "C denominator"),
        )
        * exact_int(result["beta_hit"], "beta_hit"),
        "sharp corollary lost equality",
    )
    result["representable_over"] = "GF(101)"
    result["seven_coloops_one_parallel_class"] = True
    result["sharp_for_printed_hypotheses"] = True
    return result


def generic_exchange_control() -> dict[str, Any]:
    """Check every nonempty active set on one nontrivial rank-eight matroid."""

    prime = 101
    rank = 8
    rows = []
    for coordinate in range(rank):
        row = [0] * rank
        row[coordinate] = 1
        rows.append(row)
    rows.extend(
        [
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0],
        ]
    )
    bases = enumerate_matroid_bases(rows, rank, prime)
    checked = 0
    minimum_slack: int | None = None
    for mask in range(1, 1 << len(rows)):
        active = {index for index in range(len(rows)) if mask & (1 << index)}
        beta_0 = sum(not (set(basis) & active) for basis in bases)
        beta_1 = sum(len(set(basis) & active) == 1 for basis in bases)
        lhs = len(active) * beta_0
        rhs = max(0, len(rows) - len(active) - 7) * beta_1
        require(lhs <= rhs, "generic exchange control failed")
        slack = rhs - lhs
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        checked += 1
    require(checked == 2 ** len(rows) - 1, "active-set enumeration drift")
    return {
        "field": "GF(101)",
        "rank": rank,
        "ground_size": len(rows),
        "basis_count": len(bases),
        "nonempty_active_sets_checked": checked,
        "minimum_exchange_slack": minimum_slack,
        "all_active_rows_are_nonloops": True,
    }


def load_predecessor(relative: Path, expected_payload: str) -> dict[str, Any]:
    document = base.base.load_json(ROOT / relative)
    require(
        document.get("payload_sha256") == payload_hash(document),
        f"bad predecessor payload: {relative}",
    )
    require(
        document.get("payload_sha256") == expected_payload,
        f"unpinned predecessor payload: {relative}",
    )
    return document


def validate_projective_predecessor(document: dict[str, Any]) -> None:
    require(
        document.get("schema") == "rs-mca-m1-kb-rank9-projective-source-load-v1",
        "projective predecessor schema",
    )
    theorem = document.get("theorem_contract")
    incidence = document.get("same_selector_incidence")
    ledger = document.get("ledger")
    require(type(theorem) is dict, "projective theorem block")
    require(type(incidence) is dict, "projective incidence block")
    require(type(ledger) is dict, "projective ledger block")
    require(
        theorem.get("exact_identity")
        == "E_20^nz=sum_L w_L=sum_(h in Sigma) Lambda_h",
        "projective identity drift",
    )
    require(
        theorem.get("plant_size")
        == "s_L=A-x_L-deg(G_L)>=t-x_L+1>=18418",
        "projective plant drift",
    )
    require(
        incidence.get("source_h_outside_V_is_universal_rank_zero_edge_case")
        is True,
        "universal source edge drift",
    )
    require(
        theorem.get("current_deployed_terminal")
        == "UNBOUND_POST_TANGENT_SOURCE_LOAD",
        "projective terminal drift",
    )
    require(ledger.get("E_max") == str(E_MAX), "projective E_max drift")
    require(ledger.get("ledger_movement") == 0, "projective ledger moved")
    require(ledger.get("U_Q") is None and ledger.get("U_A") is None, "open terms drift")


def validate_cyclic_countercontrol(document: dict[str, Any]) -> dict[str, Any]:
    require(
        document.get("schema")
        == "rs-mca-m1-kb-branch3-rank9-cyclic-rich-pencil-control-v1",
        "cyclic predecessor schema",
    )
    fixture = document.get("exact_fixture")
    rank9 = document.get("incomplete_rank9_control")
    atlas = document.get("canonical_atlas_control")
    scope = document.get("scope_guards")
    closure = document.get("complete_selector_closure")
    require(type(fixture) is dict, "cyclic fixture block")
    require(type(rank9) is dict, "cyclic rank-nine block")
    require(type(atlas) is dict, "cyclic atlas block")
    require(type(scope) is dict, "cyclic scope block")
    require(type(closure) is dict, "cyclic closure block")
    row = fixture.get("row")
    require(
        row == {"A": 14, "R": 21, "j": 20, "k": 13, "n": 34, "t": 1},
        "cyclic row drift",
    )
    require(
        fixture.get("source_pair") == "epsilon_0=e_0, epsilon_1=e_1",
        "cyclic source pair drift",
    )
    require(rank9.get("carrier_size") == 32, "cyclic carrier size drift")
    require(rank9.get("affine_difference_rank") == 9, "cyclic affine rank drift")
    require(rank9.get("raw_witness_rank") == 10, "cyclic raw rank drift")
    require(rank9.get("kernel_core_rank") == 8, "cyclic kernel rank drift")
    require(rank9.get("regular_hankel_chart_count") == 29, "cyclic regular count drift")
    require(rank9.get("same_support_noncontainment_count") == 29, "cyclic noncontainment drift")
    require(rank9.get("witness_inventory_exhaustive") is False, "cyclic incompleteness drift")
    require(atlas.get("J_L") == 21, "cyclic J drift")
    require(atlas.get("Z_L_size_in_carrier") == 11, "cyclic z drift")
    require(atlas.get("beta_L") == 165, "cyclic beta drift")
    require(atlas.get("sparse_plant_size") == 2, "cyclic plant drift")
    require(atlas.get("atlas_excess") == 165, "cyclic excess drift")
    require(scope.get("deployed") is False, "cyclic scope became deployed")
    require(scope.get("incomplete_rank9_selector_declared_only") is True, "cyclic scope drift")
    require(closure.get("toy_family_closed") is True, "cyclic toy closure drift")
    require(
        closure.get("owner") == "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
        "cyclic earlier owner drift",
    )

    sigma = {0, 1}
    carrier = set(range(2, 34))
    rich_zero = set(exact_int(value, "rich core") for value in fixture["rich_core"])
    universal = sigma - carrier
    active = sigma & rich_zero
    require(len(universal) == 2 and not active, "cyclic source split drift")
    require(len(universal) + len(active) == atlas["sparse_plant_size"], "cyclic plant split")
    outside_excess = atlas["beta_L"] * (atlas["J_L"] - 20)
    require(outside_excess == 165, "cyclic outside excess drift")
    return {
        "field": "GF(67^2)",
        "row": row,
        "source_indices_Sigma": sorted(sigma),
        "carrier_indices_V": sorted(carrier),
        "universal_source_size_q": len(universal),
        "active_source_size_r_L": len(active),
        "J_L": atlas["J_L"],
        "z_L": atlas["Z_L_size_in_carrier"],
        "beta_L": atlas["beta_L"],
        "plant_size_s_L": atlas["sparse_plant_size"],
        "E_out": outside_excess,
        "affine_rank": rank9["affine_difference_rank"],
        "raw_rank": rank9["raw_witness_rank"],
        "kernel_rank": rank9["kernel_core_rank"],
        "regular_chart_count": rank9["regular_hankel_chart_count"],
        "noncontainment_count": rank9["same_support_noncontainment_count"],
        "selector_complete_for_full_received_pair": False,
        "separate_complete_selector_owner": closure["owner"],
        "classification": "EXACT_LOCAL_RS_COUNTERCONTROL_NOT_DEPLOYED_COUNTEREXAMPLE",
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("packet-note", NOTE_REL, "proof and sharp route cut"),
        source_binding("packet-readme", README_REL, "replay and scope guardrails"),
        source_binding("packet-python", SCRIPT_REL, "exact arithmetic, matroid controls, and mutations"),
        source_binding("projective-predecessor", PROJECTIVE_CERT_REL, "post-tangent source-load identity"),
        source_binding("projective-predecessor-python", PROJECTIVE_PYTHON_REL, "imported arithmetic and strict contract implementation"),
        source_binding("deployed-source-helper-python", DEPLOYED_HELPER_REL, "transitive finite-field and contract helpers"),
        source_binding("cyclic-countercontrol", CYCLIC_CERT_REL, "exact GF(67^2) local rank-nine control"),
        source_binding("cyclic-countercontrol-note", CYCLIC_NOTE_REL, "countercontrol statement and completeness warning"),
        source_binding("cyclic-countercontrol-python", CYCLIC_PYTHON_REL, "exact cyclic certificate verifier"),
        source_binding("cyclic-countercontrol-sage", CYCLIC_SAGE_REL, "independent exact finite-field replay"),
        source_binding("rank-one-countercontrol-python", RANK_ONE_PYTHON_REL, "independent exact GF(1009) replay"),
        source_binding("rank-one-countercontrol-sage", RANK_ONE_SAGE_REL, "independent Sage GF(1009) replay"),
        source_binding("koalabear-row-descriptor", ROW_DESCRIPTOR_REL, "deployed multiplicative-subgroup domain excludes zero"),
    ]


def expected_certificate() -> dict[str, Any]:
    projective = load_predecessor(PROJECTIVE_CERT_REL, PROJECTIVE_PAYLOAD)
    cyclic = load_predecessor(CYCLIC_CERT_REL, CYCLIC_PAYLOAD)
    validate_projective_predecessor(projective)
    cyclic_control = validate_cyclic_countercontrol(cyclic)
    sharp_controls = [
        sharp_parallel_control(15, 3),
        sharp_parallel_control(10, 3),
        sharp_parallel_control(19, 7),
    ]
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "deployed_row": {
            "n": N,
            "k": K,
            "A": A,
            "R": R,
            "j": J,
            "t": T,
            "rich_x_max": J // 20,
            "minimum_plant": MIN_PLANT,
            "E_max": str(E_MAX),
        },
        "source_carrier_split": {
            "universal_source": "U=Sigma\\V",
            "universal_size": "q=|U|",
            "active_line_source": "I_L=Sigma INTERSECT Z_L",
            "active_size": "r_L=|I_L|",
            "exact_plant_split": "S_L=U DISJOINT_UNION I_L",
            "exact_size_split": "s_L=q+r_L",
            "active_floor": "r_L>=max(0,t-x_L+1-q)",
            "uniform_all_lines_active_if_q_at_most": MAX_UNIVERSAL_FOR_ALL_ACTIVE,
            "active_source_row_is_K0_matroid_nonloop": True,
            "nonloop_uses_complete_selector_carrier_identity": True,
        },
        "matroid_reindex": {
            "rank": 8,
            "beta_0": "number of K0 bases in Z_L avoiding I_L",
            "beta_1": "number of K0 bases in Z_L meeting I_L exactly once",
            "beta_hit": "number of K0 bases in Z_L meeting I_L",
            "exchange_inequality": "r_L*beta_0<=(z_L-r_L-7)_+*beta_1",
            "basis_hit_bound": "beta_L<=C_L*beta_hit",
            "C_L": "max(1,(z_L-7)/r_L)",
            "coefficient_sharp_under_printed_matroid_hypotheses": True,
            "sharp_controls": sharp_controls,
            "generic_control": generic_exchange_control(),
        },
        "load_interface": {
            "E_out": "sum_(L:r_L=0) beta_L*(J_L-20)",
            "active_reallocation": "Lambda_h^act=sum_(L:r_L>0,h in I_L) beta_L*(J_L-20)/r_L",
            "exact_split": "E_20^nz=E_out+sum_(h in Sigma INTERSECT V) Lambda_h^act",
            "exchange_upper_bound": "E_20^nz<=E_out+sum_(L:r_L>0) C_L*beta_L_hit*(J_L-20)",
            "E_out_paid_here": False,
            "active_source_hit_basis_tail_paid_here": False,
        },
        "full_outside_source_subcell": {
            "hypothesis": "Sigma INTERSECT V is empty",
            "rank_one_excluded_by_source_syndrome_rank_two": True,
            "rank_two_source_floor": "|Sigma|>=t-x_L+2",
            "carrier_excess_identity": "z_L=t+nu-x_L",
            "z_cap": K - 2,
            "beta_cap": str(FULL_OUTSIDE_BETA_CAP),
            "first_single_line_break_J": FULL_OUTSIDE_BREAK_J,
            "break_excess_over_E_max": str(FULL_OUTSIDE_BREAK_EXCESS),
            "moving_root_template": {
                "x_L": 1,
                "Sigma_size": T + 1,
                "outside_gcd_root_set_C_size": K - 2,
                "domain": "multiplicative subgroup D of F_p^x",
                "domain_excludes_zero": True,
                "W_size": J + 1,
                "P": "L_C*X",
                "Q": "-L_C",
                "selected_slope_count": FULL_OUTSIDE_BREAK_J,
                "each_error_support_size": J,
                "each_exact_agreement_size": A,
                "source_syndrome_rank": 2,
                "support_wise_noncontainment": True,
                "one_line_Z_L_size": 0,
                "one_line_beta_L": 0,
                "positive_determinant_mass_constructed": False,
            },
            "actual_eight_outlier_rank9_binding_constructed": False,
            "regular_first_match_binding_constructed": False,
            "terminal": "UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR",
        },
        "exact_universal_countercontrol": cyclic_control,
        "exact_active_rank_one_countercontrol": rank_one_control.build_control(),
        "route_cut": {
            "local_regular_source_plant_hypotheses_force_r_positive": False,
            "abstract_nonloop_matroid_exchange_pays_E_out": False,
            "abstract_nonloop_matroid_exchange_pays_active_tail": False,
            "one_incomplete_selector_refutes_deployed_existential_route": False,
            "rank_one_tangent_regular_source_equations_force_zero_load": False,
            "current_terminals": [
                "UNPAID_UNIVERSAL_SOURCE_CELL",
                "UNBOUND_ACTIVE_SOURCE_HIT_BASIS_TAIL",
                "UNPAID_ACTIVE_RANK1_SELECTOR_COMPLETENESS",
                "UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR",
            ],
            "encompassing_terminal": "UNBOUND_POST_TANGENT_SOURCE_LOAD",
        },
        "ledger": {
            "U_paid": str(base.U_PAID),
            "B_remaining": str(base.B_REMAINING),
            "E_max": str(E_MAX),
            "ledger_movement": 0,
            "U_Q": None,
            "U_A": None,
            "row_status": "YELLOW_OPEN_SOURCE_CARRIER_AND_SOURCE_HIT_BASIS_TAILS",
        },
        "scope_guards": {
            "deployed_compatible_selector_produced": False,
            "deployed_rank9_paid": False,
            "koalabear_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "predecessors": {
            "projective_source_load": "payload-sha256:" + PROJECTIVE_PAYLOAD,
            "cyclic_rank9_control": "payload-sha256:" + CYCLIC_PAYLOAD,
        },
        "source_bindings": expected_source_bindings(),
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def strict_match(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type mismatch at {path}")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"key mismatch at {path}")
        for key in expected:
            strict_match(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_match(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"value mismatch at {path}")


def validate_certificate(document: dict[str, Any]) -> None:
    require(document.get("payload_sha256") == payload_hash(document), "payload hash mismatch")
    strict_match(document, expected_certificate())


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def certificate_mutations() -> list[Mutation]:
    return [
        ("status", lambda d: d.__setitem__("status", "PROVED_DEPLOYED_PAYMENT")),
        ("plant-split", lambda d: d["source_carrier_split"].__setitem__("exact_size_split", "s_L=r_L")),
        ("universal-threshold", lambda d: d["source_carrier_split"].__setitem__("uniform_all_lines_active_if_q_at_most", 18_418)),
        ("nonloop", lambda d: d["source_carrier_split"].__setitem__("active_source_row_is_K0_matroid_nonloop", False)),
        ("exchange", lambda d: d["matroid_reindex"].__setitem__("exchange_inequality", "beta_0<=beta_1")),
        ("coefficient", lambda d: d["matroid_reindex"].__setitem__("C_L", "1")),
        ("sharpness", lambda d: d["matroid_reindex"].__setitem__("coefficient_sharp_under_printed_matroid_hypotheses", False)),
        ("sharp-beta0", lambda d: d["matroid_reindex"]["sharp_controls"][0].__setitem__("beta_0", 0)),
        ("generic-count", lambda d: d["matroid_reindex"]["generic_control"].__setitem__("nonempty_active_sets_checked", 0)),
        ("exact-load", lambda d: d["load_interface"].__setitem__("exact_split", "E_20^nz=0")),
        ("pay-Eout", lambda d: d["load_interface"].__setitem__("E_out_paid_here", True)),
        ("pay-active", lambda d: d["load_interface"].__setitem__("active_source_hit_basis_tail_paid_here", True)),
        ("rank1", lambda d: d["full_outside_source_subcell"].__setitem__("rank_one_excluded_by_source_syndrome_rank_two", False)),
        ("z-cap", lambda d: d["full_outside_source_subcell"].__setitem__("z_cap", K - 1)),
        ("break-J", lambda d: d["full_outside_source_subcell"].__setitem__("first_single_line_break_J", 165)),
        ("moving-domain-zero", lambda d: d["full_outside_source_subcell"]["moving_root_template"].__setitem__("domain_excludes_zero", False)),
        ("moving-false-beta", lambda d: d["full_outside_source_subcell"]["moving_root_template"].__setitem__("one_line_beta_L", 1)),
        ("rank9-binding", lambda d: d["full_outside_source_subcell"].__setitem__("actual_eight_outlier_rank9_binding_constructed", True)),
        ("cyclic-q", lambda d: d["exact_universal_countercontrol"].__setitem__("universal_source_size_q", 0)),
        ("cyclic-r", lambda d: d["exact_universal_countercontrol"].__setitem__("active_source_size_r_L", 1)),
        ("cyclic-E", lambda d: d["exact_universal_countercontrol"].__setitem__("E_out", 0)),
        ("cyclic-complete", lambda d: d["exact_universal_countercontrol"].__setitem__("selector_complete_for_full_received_pair", True)),
        ("rank1-load", lambda d: d["exact_active_rank_one_countercontrol"].__setitem__("line_weight", 0)),
        ("rank1-beta", lambda d: d["exact_active_rank_one_countercontrol"].__setitem__("beta_L", 0)),
        ("rank1-complete", lambda d: d["exact_active_rank_one_countercontrol"].__setitem__("global_bad_slope_selector_complete", True)),
        ("terminal", lambda d: d["route_cut"].__setitem__("encompassing_terminal", "PAID")),
        ("false-deployed-refutation", lambda d: d["route_cut"].__setitem__("one_incomplete_selector_refutes_deployed_existential_route", True)),
        ("false-rank1-payment", lambda d: d["route_cut"].__setitem__("rank_one_tangent_regular_source_equations_force_zero_load", True)),
        ("ledger", lambda d: d["ledger"].__setitem__("ledger_movement", 1)),
        ("UQ", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("rank10", lambda d: d["scope_guards"].__setitem__("rank_at_least_ten_authorized", True)),
        ("predecessor", lambda d: d["predecessors"].__setitem__("projective_source_load", "payload-sha256:00")),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "00")),
        ("payload", lambda d: d.__setitem__("payload_sha256", "00")),
    ]


def run_tamper_selftest() -> int:
    expected = expected_certificate()
    rejected = 0
    for name, mutate in certificate_mutations():
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        if name != "payload":
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except ContractError:
            rejected += 1
        else:
            raise ContractError(f"certificate mutation survived: {name}")
    require(rejected == len(certificate_mutations()), "mutation count mismatch")
    print(f"M1 active-source matroid reindex mutations: {rejected}/{rejected} PASS")
    return 0


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(expected_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return run_tamper_selftest()
    if args.print_certificate:
        print(json.dumps(expected_certificate(), indent=2, sort_keys=True))
        return 0
    if args.write:
        write_certificate()
        print(CERT_PATH)
        return 0
    document = base.base.load_json(CERT_PATH)
    validate_certificate(document)
    print("M1 KoalaBear active-source matroid reindex: PASS")
    print("  S_L=(Sigma\\V) disjoint_union (Sigma intersect Z_L)")
    print("  sharp exchange: r*beta_0 <= (z-r-7)_+*beta_1")
    print(f"  full-outside rank-two cap first fails at J={FULL_OUTSIDE_BREAK_J}")
    print("  terminals: UNPAID_UNIVERSAL_SOURCE_CELL; UNBOUND_ACTIVE_SOURCE_HIT_BASIS_TAIL")
    print("             UNPAID_ACTIVE_RANK1_SELECTOR_COMPLETENESS")
    print("             UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR")
    print("  deployed payment remains YELLOW; ledger movement 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
