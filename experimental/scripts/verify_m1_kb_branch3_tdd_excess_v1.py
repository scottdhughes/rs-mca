#!/usr/bin/env python3
"""Verify the KoalaBear branch-3 TDD excess and defect-span route cut.

The load-bearing results are exact and field-general:

* a TDD supported on a union of size R+1+e factors as M_U Q with deg Q<=e;
* the silent shell has size at most e and the shortened space has dimension
  e+1;
* for a complete selected-witness family, selected-error affine rank is one
  plus the rank of the fixed-anchor residual codewords;
* a residual-codeword basis plus two anchor supports recovers the complete
  selected support union.

For the deployed KoalaBear row, selected affine rank at most three has a
budget-fitting global set-pair cap.  The script also checks an exact e=1
finite-field fixture and rejects invalid local-triple, repeated-cap, and raw
union payments.  No branch-3 charge is banked.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-tdd-excess-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_TDD_EXCESS_DEFECT_SPAN_ROUTE_CUT"
STATUS = (
    "PROVED_EXACT_TDD_SHORTENING_DEFECT_SPAN_BRIDGE_"
    "RANK3_GLOBAL_TERMINAL_FAIL_CLOSED_NO_LEDGER_MOVEMENT"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-tdd-excess-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_tdd_excess_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_tdd_excess_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-tdd-excess-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.sage"
)
PREDECESSOR_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_deep_ccl_tdd_v1.md"
)
PREDECESSOR_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-deep-ccl-tdd-v1/"
    "m1_kb_branch3_deep_ccl_tdd_v1.json"
)
PREDECESSOR_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py"
)
CARRIER_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.md"
)
CARRIER_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-low-excess-carrier-cut-v1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.json"
)
SELECTED_RANK_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "a6_actual_witness_core_rank_preflight.md"
)
SELECTED_RANK_VERIFIER_REL = Path(
    "experimental/scripts/"
    "verify_a6_actual_witness_core_rank_preflight.py"
)
ALL_LINERAY_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "all_lineray_affine_core_set_pair.md"
)
ALL_LINERAY_CERT_REL = Path(
    "experimental/data/certificates/"
    "all-lineray-affine-core/all_lineray_affine_core.json"
)
ALL_LINERAY_VERIFIER_REL = Path(
    "experimental/scripts/verify_all_lineray_affine_core.py"
)
FIRST_MATCH_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "kb_mca_1116048_first_match_ledger_v1.md"
)
THRESHOLDS_REL = Path("experimental/rs_mca_thresholds.tex")

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
T = A - K
MINIMUM_DISTANCE = R + 1
R_STAR = R // 3
HEAVY_FLOOR = R_STAR + 1
MAX_GLOBAL_CARRIER_EXCESS = 10
MIN_GLOBAL_UNPAID_EXCESS = 11

DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID
K_REM = 4_807_520

AFFINE_RANK3_CAP = math.comb(J + 3, 3)
AFFINE_RANK4_MIN_POSTDEEP_CAP = math.comb(HEAVY_FLOOR + 4, 4)
AFFINE_RANK4_CAP = math.comb(J + 4, 4)
UNION_KEYS_C_LE_2 = sum(math.comb(N, c) for c in range(3))
UNION_KEYS_C_LE_3 = sum(math.comb(N, c) for c in range(4))
FIRST_UNION_TAIL_E = K - 3
PROJECTIVE_MIN_E_GE_1 = Q_LINE + 1
CENTRAL_E0_UNION_LOG2_LOWER_BOUND = R - 1

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "row",
    "predecessor_state",
    "tdd_object",
    "excess_factorization",
    "overlap_control",
    "defect_span_bridge",
    "owner_registry",
    "classifier_contract",
    "exact_controls",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not prove the KoalaBear row safe.",
    "This packet does not close branch 3.",
    "This packet does not bank a TDD, affine-core, or union charge.",
    "This packet does not infer a global carrier from one local TDD triple.",
    "This packet does not infer complete-selector affine rank from three anchors.",
    "This packet does not sum rank-three caps over an unproved subfamily cover.",
    "This packet does not identify triple excess e with carrier excess e+1.",
    "This packet does not treat raw support-union enumeration as an injection.",
    "This packet does not force a primitive residual into a named owner.",
    "This packet does not determine U_2, U_Q, or U_A.",
    "This packet does not begin the degree-three parameter class.",
    "This packet does not authorize Lean or Paper-D theorem promotion.",
]

EDGE_CASES = [
    "The TDD must be nonzero; the zero-defect common-code-line family was routed earlier.",
    "The three slopes are finite and pairwise distinct.",
    "The triple excess e=|U|-(R+1) lies in [0,k-1].",
    "The carrier excess of the same union is kappa=e+1.",
    "M_U is the locator of D minus U, not the locator of U.",
    "The silent-shell bound uses that M_U is nonzero at every point of U.",
    "Every silent-shell point has membership in at least two error supports.",
    "A pair-specific common root is not a complete-family common-GCD owner.",
    "Affine rank is computed on one complete actual-witness selector.",
    "The rank-three cap is global once, not a per-triple or per-chart cap.",
    "Null ledger entries are not zero.",
]

REMAINING_RISKS = [
    "The first unpaid affine layer s=4 has no proved global owner.",
    "High selected-union excess and defect-span rank at least three remain compatible.",
    "No canonical slope injection or bounded multiplicity theorem for TDD unions is proved.",
    "The frozen tangent/common-line/residue branch is not globally closed.",
    "Branches 4 and 5, U_2, U_Q, and U_A remain open.",
    "The complete KoalaBear row inequality remains undecided.",
]


class VerificationError(RuntimeError):
    """A source, arithmetic, schema, or semantic check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def require_int(value: Any, label: str) -> None:
    require(type(value) is int, f"{label} is not an exact JSON integer")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON: {path}")
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
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing source binding: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        binding("packet-note", NOTE_REL, "human-readable proof and route cut"),
        binding(
            "certificate-readme",
            README_REL,
            "replay commands and scope summary",
        ),
        binding(
            "python-verifier",
            PYTHON_REL,
            "exact arithmetic, finite controls, schema, and mutations",
        ),
        binding(
            "sage-replay",
            SAGE_REL,
            "independent GF(17) shortening and TDD replay",
        ),
        binding(
            "predecessor-note",
            PREDECESSOR_NOTE_REL,
            "deep-owner, carrier-first, and TDD predecessor theorem",
        ),
        binding(
            "predecessor-certificate",
            PREDECESSOR_CERT_REL,
            "machine-readable predecessor ledger",
        ),
        binding(
            "predecessor-verifier",
            PREDECESSOR_VERIFIER_REL,
            "predecessor semantic and mutation replay",
        ),
        binding(
            "global-carrier-note",
            CARRIER_NOTE_REL,
            "one-global-carrier owner and excess-ten cutoff",
        ),
        binding(
            "global-carrier-certificate",
            CARRIER_CERT_REL,
            "machine-readable carrier contract",
        ),
        binding(
            "selected-rank-theorem",
            SELECTED_RANK_NOTE_REL,
            "complete selected-witness affine-core set-pair bound",
        ),
        binding(
            "selected-rank-verifier",
            SELECTED_RANK_VERIFIER_REL,
            "selected-witness theorem replay",
        ),
        binding(
            "all-lineray-theorem",
            ALL_LINERAY_NOTE_REL,
            "stronger complete-pair affine-core cross-check",
        ),
        binding(
            "all-lineray-certificate",
            ALL_LINERAY_CERT_REL,
            "machine-readable complete-pair theorem status",
        ),
        binding(
            "all-lineray-verifier",
            ALL_LINERAY_VERIFIER_REL,
            "complete-pair theorem finite replay",
        ),
        binding(
            "first-match-ledger",
            FIRST_MATCH_NOTE_REL,
            "frozen KoalaBear owner ordering and numerator scope",
        ),
        binding(
            "exact-thresholds",
            THRESHOLDS_REL,
            "RS distance and syndrome-line interfaces",
        ),
    ]


def matrix_rank_mod(rows: list[list[int]], modulus: int) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    work = [[value % modulus for value in row] for row in rows]
    active = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(active, len(work))
                if work[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        work[active], work[pivot] = work[pivot], work[active]
        inverse = pow(work[active][column], -1, modulus)
        work[active] = [
            value * inverse % modulus for value in work[active]
        ]
        for row in range(len(work)):
            if row == active:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[active])
                ]
        active += 1
        if active == len(work):
            break
    return active


def vector_add(*vectors: list[int], modulus: int) -> list[int]:
    require(vectors, "empty vector sum")
    width = len(vectors[0])
    require(
        all(len(vector) == width for vector in vectors),
        "vector width mismatch",
    )
    return [
        sum(vector[index] for vector in vectors) % modulus
        for index in range(width)
    ]


def vector_scale(scalar: int, vector: list[int], modulus: int) -> list[int]:
    return [scalar * value % modulus for value in vector]


def vector_subtract(
    first: list[int], second: list[int], modulus: int
) -> list[int]:
    return vector_add(
        first,
        vector_scale(-1, second, modulus),
        modulus=modulus,
    )


def vector_support(vector: list[int]) -> list[int]:
    return [index for index, value in enumerate(vector) if value != 0]


def locator_evaluations(
    domain: list[int], complement_indices: list[int], modulus: int
) -> list[int]:
    result = []
    roots = [domain[index] for index in complement_indices]
    for point in domain:
        value = 1
        for root in roots:
            value = value * (point - root) % modulus
        result.append(value)
    return result


def finite_field_control() -> dict[str, Any]:
    modulus = 17
    domain = list(range(8))
    n = 8
    k = 4
    redundancy = n - k
    minimum_distance = redundancy + 1

    shortened = []
    for excess in range(3):
        union_size = redundancy + 1 + excess
        complement = list(range(union_size, n))
        locator = locator_evaluations(domain, complement, modulus)
        basis = [
            [
                locator[index] * pow(domain[index], power, modulus) % modulus
                for index in range(n)
            ]
            for power in range(excess + 1)
        ]
        rank = matrix_rank_mod(basis, modulus)
        require(rank == excess + 1, "finite shortened dimension drift")
        require(
            all(
                all(vector[index] == 0 for index in complement)
                for vector in basis
            ),
            "finite shortened vector leaks outside its union",
        )
        shortened.append(
            {
                "excess": excess,
                "union_size": union_size,
                "locator_degree": k - 1 - excess,
                "shortened_dimension": rank,
            }
        )

    E0 = {0, 1}
    E1 = {2, 3}
    Ea = {4, 5}
    union = E0 | E1 | Ea
    a_slope = 2
    delta = locator_evaluations(
        domain,
        [index for index in range(n) if index not in union],
        modulus,
    )
    zero = [0] * n
    c0 = zero
    c1 = zero
    ca = vector_scale(-1, delta, modulus)
    f = [0] * n
    g = [0] * n
    inverse_one_minus_a = pow(1 - a_slope, -1, modulus)
    inverse_a = pow(a_slope, -1, modulus)
    for index in E0:
        f[index] = -delta[index] * inverse_one_minus_a % modulus
        g[index] = delta[index] * inverse_one_minus_a % modulus
    for index in E1:
        g[index] = -delta[index] * inverse_a % modulus

    e0 = vector_subtract(f, c0, modulus)
    e1 = vector_subtract(vector_add(f, g, modulus=modulus), c1, modulus)
    ea = vector_subtract(
        vector_add(
            f,
            vector_scale(a_slope, g, modulus),
            modulus=modulus,
        ),
        ca,
        modulus,
    )
    tdd = vector_add(
        vector_scale(1 - a_slope, c0, modulus),
        vector_scale(a_slope, c1, modulus),
        vector_scale(-1, ca, modulus),
        modulus=modulus,
    )

    require(set(vector_support(e0)) == E0, "finite E0 support drift")
    require(set(vector_support(e1)) == E1, "finite E1 support drift")
    require(set(vector_support(ea)) == Ea, "finite Ea support drift")
    require(tdd == delta, "finite TDD identity drift")
    require(set(vector_support(tdd)) == union, "finite silent shell drift")

    affine_rank = matrix_rank_mod(
        [
            vector_subtract(e1, e0, modulus),
            vector_subtract(ea, e0, modulus),
        ],
        modulus,
    )
    residual_rank = matrix_rank_mod([ca], modulus)
    require(affine_rank == residual_rank + 1, "finite rank bridge drift")

    return {
        "field": modulus,
        "code": {
            "n": n,
            "k": k,
            "R": redundancy,
            "minimum_distance": minimum_distance,
        },
        "shortened_spaces": shortened,
        "e1_fixture": {
            "slopes": [0, 1, a_slope],
            "support_weights": [
                len(vector_support(e0)),
                len(vector_support(e1)),
                len(vector_support(ea)),
            ],
            "supports_pairwise_disjoint": True,
            "triple_excess": len(union) - (redundancy + 1),
            "carrier_excess": len(union) - redundancy,
            "silent_shell_size": len(union - set(vector_support(tdd))),
            "selected_affine_rank": affine_rank,
            "residual_codeword_rank": residual_rank,
            "rank_bridge": affine_rank == residual_rank + 1,
            "post_deep_uniqueness_inequality": (
                len(E0) + redundancy // 3 < minimum_distance
            ),
        },
    }


def classify_selector(
    *,
    named_paid_owner: str | None,
    actual_complete_selector: bool,
    selector_attains_intrinsic_minimum: bool,
    retained_family_size_gt_15: bool,
    witness_contract: bool,
    minimum_global_carrier_excess: int | None,
    affine_rank: int | None,
    claims_undeclared_canonical_union_owner: bool,
) -> dict[str, Any]:
    if named_paid_owner is not None:
        return {
            "terminal": "PAID_NAMED_PREDECESSOR_OWNER",
            "owner": named_paid_owner,
            "cap": None,
            "ledger_charge_banked_by_this_packet": False,
        }
    if (
        actual_complete_selector
        and witness_contract
        and minimum_global_carrier_excess is not None
        and 0
        <= minimum_global_carrier_excess
        <= MAX_GLOBAL_CARRIER_EXCESS
    ):
        return {
            "terminal": "PAID_GLOBAL_CARRIER_EXCESS_LE_10",
            "owner": "INTEGRATED_GLOBAL_CARRIER",
            "cap": "PREDECESSOR_CARRIER_CAP",
            "ledger_charge_banked_by_this_packet": False,
        }
    if (
        actual_complete_selector
        and witness_contract
        and affine_rank is not None
        and 0 <= affine_rank <= 3
    ):
        cap = math.comb(J + affine_rank, affine_rank)
        return {
            "terminal": "PAID_SELECTED_AFFINE_CORE_RANK_LE_3",
            "owner": "ACTUAL_SELECTED_WITNESS_CORE_RANK",
            "cap": str(cap),
            "ledger_charge_banked_by_this_packet": False,
        }
    if claims_undeclared_canonical_union_owner:
        return {
            "terminal": "REJECTED_UNDECLARED_FUTURE_OWNER",
            "owner": None,
            "cap": None,
            "ledger_charge_banked_by_this_packet": False,
        }
    if (
        actual_complete_selector
        and witness_contract
        and selector_attains_intrinsic_minimum
        and retained_family_size_gt_15
        and minimum_global_carrier_excess is not None
        and minimum_global_carrier_excess
        >= MIN_GLOBAL_UNPAID_EXCESS
        and affine_rank is not None
        and affine_rank >= 4
    ):
        return {
            "terminal": "UNPAID_PRIMITIVE_INTRINSIC_RANK3_TDD_SPREAD",
            "owner": None,
            "cap": None,
            "ledger_charge_banked_by_this_packet": False,
        }
    return {
        "terminal": "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED",
        "owner": None,
        "cap": None,
        "ledger_charge_banked_by_this_packet": False,
    }


def expected_row() -> dict[str, Any]:
    return {
        "row_id": "koalabear-mca-A1116048",
        "p": P,
        "ambient_extension_degree": EXTENSION_DEGREE,
        "q_line": str(Q_LINE),
        "n": N,
        "k": K,
        "agreement_A": A,
        "redundancy_R": R,
        "error_cap_j": J,
        "full_row_rank_threshold_t": T,
        "minimum_distance": MINIMUM_DISTANCE,
        "deep_error_cutoff_r_star": R_STAR,
        "surviving_error_weight_floor_L": HEAVY_FLOOR,
        "three_times_L": 3 * HEAVY_FLOOR,
        "B_star": str(B_STAR),
        "U_paid": str(U_PAID),
        "B_remaining": str(B_REMAINING),
    }


def expected_predecessor_state() -> dict[str, Any]:
    return {
        "source_terminal": "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
        "deep_owner_extension_banked": True,
        "deep_owner_increment": "282054",
        "global_carrier_checked_first": True,
        "predecessor_tdd_uses_one_fixed_selector": True,
        "predecessor_high_union_does_not_transfer_between_selectors": True,
        "current_packet_reapplies_carrier_existentially": True,
        "predecessor_tdd_theorem_uniform_over_complete_selectors": True,
        "rank_minimizing_selector_gets_fresh_tdd_when_family_gt_15": True,
        "global_carrier_paid_through_excess": MAX_GLOBAL_CARRIER_EXCESS,
        "small_family_cap": 15,
        "tdd_requires_nonzero_defect": True,
        "tdd_triple_union_lower_bound": MINIMUM_DISTANCE,
        "branch3_closed_before": False,
        "branch3_closed_after": False,
    }


def expected_tdd_object() -> dict[str, Any]:
    return {
        "slopes": "alpha,beta,gamma finite pairwise distinct",
        "selected_codewords": "c_alpha,c_beta,c_gamma in RS_F(D,k)",
        "selected_errors": "e_eta=f+eta*g-c_eta",
        "selected_supports": "E_eta=supp(e_eta)",
        "defect_formula": (
            "Delta=(beta-gamma)c_alpha+(gamma-alpha)c_beta+"
            "(alpha-beta)c_gamma"
        ),
        "error_formula": (
            "Delta=-((beta-gamma)e_alpha+(gamma-alpha)e_beta+"
            "(alpha-beta)e_gamma)"
        ),
        "support_union": "U=E_alpha UNION E_beta UNION E_gamma",
        "support_containment": "supp(Delta) SUBSET U",
        "nonzero_required": True,
        "minimum_union_size": MINIMUM_DISTANCE,
        "triple_excess": "e=|U|-(R+1)",
        "triple_excess_minimum": 0,
        "triple_excess_maximum": K - 1,
        "carrier_excess": "kappa(U)=|U|-R=e+1",
        "local_e_le_9_implies_global_carrier_payment": False,
    }


def expected_excess_factorization() -> dict[str, Any]:
    records = []
    for excess in (0, 1, 2, 9, 10, K - 3, K - 2, K - 1):
        records.append(
            {
                "e": excess,
                "union_size": R + 1 + excess,
                "complement_size": K - 1 - excess,
                "locator_degree": K - 1 - excess,
                "Q_degree_cap": excess,
                "shortened_dimension": excess + 1,
                "carrier_excess": excess + 1,
            }
        )
    return {
        "complement_locator": "M_U=PRODUCT_(x in D_MINUS_U)(X-x)",
        "locator_degree": "deg(M_U)=k-1-e",
        "factorization": "Delta=M_U*Q",
        "Q_degree_bound": "deg(Q)<=e",
        "shortened_space_dimension": "e+1",
        "silent_shell": "U_MINUS_supp(Delta)=U INTERSECT Z(Q)",
        "silent_shell_bound": "|U_MINUS_supp(Delta)|<=e",
        "e_zero_projective_multiplicity": 1,
        "projective_multiplicity": "(q^(e+1)-1)/(q-1)",
        "projective_multiplicity_is_payment": False,
        "compressed_records": records,
    }


def expected_overlap_control() -> dict[str, Any]:
    return {
        "pair_intersection_sum": "P=SUM_(eta<theta)|E_eta INTERSECT E_theta|",
        "triple_intersection": "T=|E_alpha INTERSECT E_beta INTERSECT E_gamma|",
        "identity": "P-T=a_alpha+a_beta+a_gamma-|U|",
        "maximum_pair_lower_bound": (
            "ceil(max(0,a_alpha+a_beta+a_gamma-R-1-e)/3)"
        ),
        "silent_shell_membership_floor": 2,
        "deployed_heavy_floor": HEAVY_FLOOR,
        "deployed_three_heavy_floor": 3 * HEAVY_FLOOR,
        "deployed_R_plus_two": R + 2,
        "e_zero_forced_P_minus_T": 1,
        "e_ge_one_forced_P_minus_T": 0,
        "complete_family_common_gcd_forced": False,
    }


def expected_defect_span_bridge() -> dict[str, Any]:
    caps = [
        {
            "affine_rank_s": rank,
            "cap": str(math.comb(J + rank, rank)),
            "budget_fits": math.comb(J + rank, rank) <= B_REMAINING,
        }
        for rank in range(5)
    ]
    return {
        "selector_scope": (
            "ONE_MINIMUM_AFFINE_RANK_COMPLETE_ACTUAL_WITNESS_SELECTOR"
        ),
        "numerator_scope": "DISTINCT_FINITE_BAD_SLOPES",
        "one_witness_per_retained_slope_is_complete_for_numerator": True,
        "all_codewords_at_each_slope_required": False,
        "selector_set": (
            "Sel(Gamma)=ALL_COMPLETE_VALID_ACTUAL_WITNESS_SELECTORS"
        ),
        "intrinsic_rank": "s_star=MIN_(sigma in Sel(Gamma)) s(sigma)",
        "intrinsic_global_carrier_excess": (
            "kappa_star=MIN_(sigma in Sel(Gamma)) "
            "MAX(0,|UNION E_gamma^sigma|-R)"
        ),
        "selector_set_finite_nonempty_deployed": True,
        "intrinsic_minimum_attained_deployed": True,
        "carrier_owner_existential_over_complete_selectors": True,
        "kappa_star_ge_11_implies_every_selector_high_union": True,
        "carrier_and_rank_minimizers_may_differ": True,
        "chosen_selector_attains_intrinsic_minimum": True,
        "tdd_regenerated_on_chosen_rank_minimizer": True,
        "tdd_regeneration_family_size_floor": 16,
        "syndrome_direction_y1_nonzero_from_transversality": True,
        "anchors": "alpha,beta distinct retained slopes",
        "code_line": (
            "p+alpha*q=c_alpha AND p+beta*q=c_beta"
        ),
        "received_residuals": "a=f-p,b=g-q",
        "code_residuals": "r_gamma=c_gamma-(p+gamma*q)",
        "error_decomposition": "e_gamma=a+gamma*b-r_gamma",
        "tdd_residual_identity": (
            "Delta_(alpha,beta,gamma)=(alpha-beta)r_gamma"
        ),
        "selected_error_difference_space": (
            "D_sel=span{e_gamma-e_alpha}"
        ),
        "residual_codeword_space": "R_sel=span{r_gamma}",
        "direct_sum": "D_sel=<b> DIRECT_SUM R_sel",
        "rank_identity": "s_star=1+dim(R_sel)_FOR_MINIMIZING_SELECTOR",
        "rank_computed_on_local_triple_only": False,
        "arbitrary_nonminimizing_selector_certifies_exact_intrinsic_rank": False,
        "any_complete_selector_rank_le_3_certifies_payment": True,
        "basis_carrier_support_count": "s_star+1",
        "basis_carrier_equals_complete_selected_union": True,
        "basis_carrier_is_canonical": False,
        "rank_caps": caps,
        "largest_budget_fitting_affine_rank": 3,
        "rank3_cap": str(AFFINE_RANK3_CAP),
        "rank4_min_postdeep_cap": str(AFFINE_RANK4_MIN_POSTDEEP_CAP),
        "rank4_cap": str(AFFINE_RANK4_CAP),
        "rank3_fits": AFFINE_RANK3_CAP <= B_REMAINING,
        "rank4_min_postdeep_fits": (
            AFFINE_RANK4_MIN_POSTDEEP_CAP <= B_REMAINING
        ),
        "rank4_fits": AFFINE_RANK4_CAP <= B_REMAINING,
        "first_unpaid_intrinsic_affine_rank_stratum": 4,
        "first_unpaid_defect_span_rank": 3,
        "first_unpaid_basis_carrier_slopes": 5,
    }


def expected_owner_registry() -> dict[str, Any]:
    return {
        "first_match_order": [
            "NAMED_ALREADY_PAID_QUOTIENT_PERIODIC_JOHNSON_COMMON_SUPPORT",
            "ONE_GLOBAL_CARRIER_EXCESS_LE_10",
            "COMPLETE_SELECTOR_AFFINE_RANK_LE_3",
            "FUTURE_DEDUPLICATED_TDD_ROOT_UNION_WITH_PROVED_MULTIPLICITY",
            "UNPAID_PRIMITIVE_INTRINSIC_RANK3_TDD_SPREAD",
        ],
        "global_carrier_requires_complete_union": True,
        "global_carrier_owner_uses_minimum_over_complete_selectors": True,
        "carrier_complement_makes_every_complete_selector_high_union": True,
        "rank_terminal_requires_complete_selector": True,
        "rank_terminal_charge_once_globally": True,
        "future_union_owner_proved": False,
        "forbidden_inferences": [
            "LOCAL_TRIPLE_e_LE_9_IMPLIES_GLOBAL_CARRIER",
            "LOCAL_TRIPLE_RANK_IMPLIES_COMPLETE_SELECTOR_RANK",
            "REPEATED_RANK3_CAP_WITHOUT_BOUNDED_COVER",
            "TRIPLE_EXCESS_EQUALS_CARRIER_EXCESS",
            "ONE_KEY_PER_UNION_WITHOUT_INJECTION",
            "FORCED_OWNER_FOR_COMPATIBLE_PRIMITIVE_COMPONENT",
        ],
    }


def expected_classifier_contract() -> dict[str, Any]:
    base = {
        "named_paid_owner": None,
        "actual_complete_selector": True,
        "retained_family_size_gt_15": True,
        "witness_contract": True,
        "minimum_global_carrier_excess": None,
        "affine_rank": None,
        "selector_attains_intrinsic_minimum": True,
        "claims_undeclared_canonical_union_owner": False,
    }
    return {
        "required_global_inputs": [
            "ONE_COMPLETE_ACTUAL_WITNESS_SELECTOR",
            "ACTUAL_NONZERO_ERROR_SUPPORTS",
            "DECLARED_NONCONTAINMENT_AND_TRANSVERSALITY",
            "GLOBAL_CARRIER_COMPLETENESS_IF_USED",
            "MINIMUM_GLOBAL_CARRIER_EXCESS_OVER_ALL_COMPLETE_SELECTORS",
            "COMPLETE_SELECTOR_AFFINE_RANK_IF_USED",
            "CERTIFICATE_THAT_THE_RANK_SELECTOR_ATTAINS_s_star",
            "CERTIFICATE_THAT_THE_RETAINED_FAMILY_HAS_MORE_THAN_15_SLOPES",
        ],
        "controls": {
            "named_owner": classify_selector(
                **{**base, "named_paid_owner": "INVARIANT_QUOTIENT_DESCENT"}
            ),
            "global_carrier_10": classify_selector(
                **{**base, "minimum_global_carrier_excess": 10}
            ),
            "global_carrier_11": classify_selector(
                **{**base, "minimum_global_carrier_excess": 11}
            ),
            "complete_rank_3": classify_selector(
                **{**base, "affine_rank": 3}
            ),
            "complete_rank_4": classify_selector(
                **{**base, "affine_rank": 4}
            ),
            "certified_primitive_rank_4": classify_selector(
                **{
                    **base,
                    "minimum_global_carrier_excess": 11,
                    "affine_rank": 4,
                }
            ),
            "local_triple_rank_2_only": classify_selector(
                **{
                    **base,
                    "actual_complete_selector": False,
                    "affine_rank": 2,
                }
            ),
            "nonminimizing_complete_rank_3": classify_selector(
                **{
                    **base,
                    "selector_attains_intrinsic_minimum": False,
                    "affine_rank": 3,
                }
            ),
            "nonminimizing_complete_rank_4": classify_selector(
                **{
                    **base,
                    "selector_attains_intrinsic_minimum": False,
                    "affine_rank": 4,
                }
            ),
            "small_family_rank_4": classify_selector(
                **{
                    **base,
                    "retained_family_size_gt_15": False,
                    "minimum_global_carrier_excess": 11,
                    "affine_rank": 4,
                }
            ),
            "missing_witness_contract": classify_selector(
                **{**base, "witness_contract": False, "affine_rank": 3}
            ),
            "undeclared_future_union": classify_selector(
                **{
                    **base,
                    "claims_undeclared_canonical_union_owner": True,
                }
            ),
            "primitive_default": classify_selector(**base),
        },
        "deployed_complete_selector_certificate_present": False,
        "deployed_retained_family_size_gt_15_from_predecessor": True,
        "deployed_intrinsic_affine_rank_known": False,
        "deployed_terminal": (
            "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        ),
        "classifier_banks_charge": False,
    }


def expected_exact_controls() -> dict[str, Any]:
    return {
        "big_integer_boundaries": {
            "rank3_cap": str(AFFINE_RANK3_CAP),
            "rank3_cap_fits": AFFINE_RANK3_CAP < B_REMAINING,
            "rank3_remaining": str(B_REMAINING - AFFINE_RANK3_CAP),
            "rank4_min_postdeep_cap": str(
                AFFINE_RANK4_MIN_POSTDEEP_CAP
            ),
            "rank4_min_postdeep_cap_fits": (
                AFFINE_RANK4_MIN_POSTDEEP_CAP <= B_REMAINING
            ),
            "rank4_min_postdeep_shortfall": str(
                AFFINE_RANK4_MIN_POSTDEEP_CAP - B_REMAINING
            ),
            "rank4_cap": str(AFFINE_RANK4_CAP),
            "rank4_cap_fits": AFFINE_RANK4_CAP <= B_REMAINING,
            "rank4_shortfall": str(AFFINE_RANK4_CAP - B_REMAINING),
            "union_keys_complement_size_at_most_2": str(UNION_KEYS_C_LE_2),
            "union_c_le_2_fits": UNION_KEYS_C_LE_2 <= B_REMAINING,
            "union_keys_complement_size_at_most_3": str(UNION_KEYS_C_LE_3),
            "union_c_le_3_fits": UNION_KEYS_C_LE_3 <= B_REMAINING,
            "hypothetical_union_tail_starts_at_e": FIRST_UNION_TAIL_E,
            "projective_minimum_for_e_ge_1": str(PROJECTIVE_MIN_E_GE_1),
            "projective_minimum_fits": PROJECTIVE_MIN_E_GE_1 <= B_REMAINING,
            "central_e0_union_log2_lower_bound": (
                CENTRAL_E0_UNION_LOG2_LOWER_BOUND
            ),
            "central_e0_union_lower_bound_reason": (
                "C(2R,R+1)=C(2R,R)*R/(R+1)>2^(R-1)"
            ),
            "central_e0_union_lower_bound_exceeds_budget": (
                (1 << CENTRAL_E0_UNION_LOG2_LOWER_BOUND) > B_REMAINING
            ),
            "raw_union_or_projective_enumeration_pays": False,
        },
        "deployed_e1_fixture_arithmetic": {
            "R_plus_2": R + 2,
            "three_times_L": 3 * HEAVY_FLOOR,
            "identity_R_plus_2_equals_3L": R + 2 == 3 * HEAVY_FLOOR,
            "triple_excess": 1,
            "carrier_excess": 2,
            "support_weights": [HEAVY_FLOOR] * 3,
            "pairwise_disjoint_supports": True,
            "pair_locator_gcd_degree": 0,
            "displayed_weight_plus_r_star": HEAVY_FLOOR + R_STAR,
            "minimum_distance": MINIMUM_DISTANCE,
            "alternate_deep_witness_excluded": (
                HEAVY_FLOOR + R_STAR < MINIMUM_DISTANCE
            ),
            "full_row_rank_weight_gate": HEAVY_FLOOR >= T,
            "common_zero_locus_size": HEAVY_FLOOR + K - 2,
            "common_zero_locus_has_k_points": (
                HEAVY_FLOOR + K - 2 >= K
            ),
            "each_error_zero_mask_size": N - HEAVY_FLOOR,
            "each_error_zero_mask_contains_A_points": (
                N - HEAVY_FLOOR >= A
            ),
            "noncontained_exact_A_witness_argument": (
                "K_COMMON_ZEROS_PLUS_OPPOSITE_BLOCK_FOR_SLOPES_0_1_"
                "AND_M_U_LINEAR_QUOTIENT_CONTRADICTION_FOR_SLOPE_a"
            ),
            "fixture_is_branch3_counterexample": False,
            "fixture_paid_by_global_carrier": True,
            "fixture_paid_by_small_family_predecessor": True,
            "fixture_purpose": (
                "REJECT_LOW_e_FORCES_DISPLAYED_TDD_SUPPORT_"
                "COMMON_GCD_OR_CYCLIC_SHIFT_SYMMETRY"
            ),
            "other_heavy_witnesses_for_same_slopes_classified": False,
        },
        "python_GF17_control": finite_field_control(),
        "sage_replay_expected_schema": (
            "rs-mca-m1-kb-branch3-tdd-excess-v1-sage-control"
        ),
        "sage_replay_is_deployed_enumeration": False,
    }


def expected_ledger() -> dict[str, Any]:
    return {
        "U_paid_before": str(U_PAID),
        "B_remaining_before": str(B_REMAINING),
        "conditional_rank3_cap": str(AFFINE_RANK3_CAP),
        "conditional_rank3_remaining": str(
            B_REMAINING - AFFINE_RANK3_CAP
        ),
        "conditional_terminal_proved": True,
        "conditional_terminal_exhaustive_for_deployed_residual": False,
        "packet_banked_charge": "0",
        "tdd_charge": None,
        "affine_core_charge": None,
        "union_charge": None,
        "U_paid_after": str(U_PAID),
        "B_remaining_after": str(B_REMAINING),
        "K_rem": K_REM,
        "ledger_consequence": False,
        "branch3_closed": False,
        "U_2": None,
        "U_Q": None,
        "U_A": None,
        "lhs": None,
        "row_complete": False,
        "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        "next_attack": (
            "FIRST_INTRINSIC_AFFINE_RANK4_"
            "FIVE_SLOPE_THREE_RESIDUAL_TDD_SPREAD"
        ),
    }


def expected_audit_sections() -> dict[str, Any]:
    return {
        "parameter_dependence": (
            "SHORTENING_OVERLAP_AND_DEFECT_SPAN_FIELD_GENERAL_"
            "RANK_CUTOFF_AND_BUDGET_KOALABEAR_SPECIFIC"
        ),
        "layer_cake_dyadic_summability": "NOT_APPLICABLE",
        "moment_markov_chebyshev": "NOT_APPLICABLE",
        "numerical_evidence": (
            "EXACT_BIG_INTEGER_AND_GF17_CONTROLS_ONLY_"
            "NO_DEPLOYED_FIELD_ENUMERATION_NO_ASYMPTOTIC_EXTRAPOLATION"
        ),
        "edge_cases": EDGE_CASES,
        "remaining_risks": REMAINING_RISKS,
        "verdict": (
            "GREEN_LOCAL_LEMMAS_RED_LOW_EXCESS_CLOSURE_"
            "YELLOW_BRANCH3_AND_ROW"
        ),
    }


def validate_sources() -> None:
    predecessor = load_json(ROOT / PREDECESSOR_CERT_REL)
    require(
        predecessor["row"]["n"] == N
        and predecessor["row"]["k"] == K
        and predecessor["row"]["A"] == A
        and predecessor["row"]["R"] == R
        and predecessor["row"]["j"] == J
        and predecessor["row"]["t"] == T
        and predecessor["row"]["minimum_distance"] == MINIMUM_DISTANCE,
        "predecessor row drift",
    )
    require(
        int(predecessor["ledger"]["U_paid_after"]) == U_PAID
        and int(predecessor["ledger"]["B_remaining_after"]) == B_REMAINING
        and predecessor["ledger"]["K_rem"] == K_REM
        and predecessor["ledger"]["tdd_charge"] is None
        and predecessor["ledger"]["branch3_closed"] is False
        and predecessor["ledger"]["next_attack"]
        == "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
        "predecessor ledger drift",
    )

    carrier = load_json(ROOT / CARRIER_CERT_REL)
    require(
        carrier["budget_table"]["largest_budget_fitting_excess"] == 10
        and carrier["carrier_dichotomy"]["single_global_carrier_required"]
        is True
        and carrier["ledger"]["branch3_closed"] is False,
        "global-carrier interface drift",
    )

    all_lineray = load_json(ROOT / ALL_LINERAY_CERT_REL)
    require(
        all_lineray["status"] == "PROVED"
        and all_lineray["theorem"] == "all-LineRay affine-core set-pair"
        and all_lineray["formula"]
        == "sum 1/binom(s+wt(e),s) <= 1",
        "all-LineRay theorem status drift",
    )

    source_anchors = {
        PREDECESSOR_NOTE_REL: (
            "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
            "nonzero triple-distance defect",
            "valid for every such selection.",
        ),
        CARRIER_NOTE_REL: (
            "one global carrier",
            "kappa_*(Z) <= 10",
        ),
        SELECTED_RANK_NOTE_REL: (
            "Actual selected-witness core rank",
            "|Z|<=B_pair:=binom(s+w_Z,s)",
            "before defining any rank",
        ),
        ALL_LINERAY_NOTE_REL: (
            "All-LineRay affine-core set-pair theorem",
            "sum_((gamma,e) in P) 1/binom(s+wt(e),s) <= 1",
        ),
        FIRST_MATCH_NOTE_REL: (
            "KoalaBear",
            "first-match",
        ),
        THRESHOLDS_REL: (
            r"\label{prop:syndrome-line-normal-form}",
            r"\label{lem:independent-union-rays}",
        ),
    }
    for relative, anchors in source_anchors.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for anchor in anchors:
            require(anchor in text, f"source anchor missing: {relative}: {anchor}")

    require(R - J == T, "R-j=t arithmetic drift")
    require(MINIMUM_DISTANCE == R + 1, "minimum distance drift")
    require(HEAVY_FLOOR == R_STAR + 1, "heavy floor drift")
    require(3 * HEAVY_FLOOR == R + 2, "R+2=3L identity drift")
    require(
        AFFINE_RANK3_CAP
        == 157_397_034_144_292_985
        < B_REMAINING,
        "rank-three budget boundary drift",
    )
    require(
        AFFINE_RANK4_CAP
        == 38_605_872_343_809_750_481_845
        > B_REMAINING,
        "rank-four budget boundary drift",
    )
    require(
        AFFINE_RANK4_MIN_POSTDEEP_CAP
        == 621_897_958_437_476_295_030
        > B_REMAINING,
        "minimum post-deep rank-four boundary drift",
    )
    require(
        UNION_KEYS_C_LE_2 == 2_199_024_304_129
        and UNION_KEYS_C_LE_2 < B_REMAINING,
        "c<=2 union boundary drift",
    )
    require(
        UNION_KEYS_C_LE_3 == 1_537_228_672_810_876_929
        and UNION_KEYS_C_LE_3 > B_REMAINING,
        "c<=3 union boundary drift",
    )
    require(
        PROJECTIVE_MIN_E_GE_1 > B_REMAINING,
        "projective defect minimum unexpectedly fits",
    )


def build_certificate() -> dict[str, Any]:
    validate_sources()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "row": expected_row(),
        "predecessor_state": expected_predecessor_state(),
        "tdd_object": expected_tdd_object(),
        "excess_factorization": expected_excess_factorization(),
        "overlap_control": expected_overlap_control(),
        "defect_span_bridge": expected_defect_span_bridge(),
        "owner_registry": expected_owner_registry(),
        "classifier_contract": expected_classifier_contract(),
        "exact_controls": expected_exact_controls(),
        "charges": [],
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def require_exact_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    require(set(value) == expected, f"{label} keys drift")


def validate_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list, "source_bindings is not a list")
    require(
        canonical_bytes(bindings)
        == canonical_bytes(expected_source_bindings()),
        "source binding path/hash/role drift",
    )
    seen: set[str] = set()
    for source in bindings:
        require(type(source) is dict, "source binding is not an object")
        require_exact_keys(
            source,
            {"binding_id", "path", "sha256", "role"},
            "source binding",
        )
        require(
            all(
                type(source[key]) is str
                for key in ("binding_id", "path", "sha256", "role")
            ),
            "source binding type drift",
        )
        source_id = source["binding_id"]
        require(source_id not in seen, "duplicate source binding id")
        seen.add(source_id)
        path = Path(source["path"])
        require(
            not path.is_absolute() and ".." not in path.parts,
            "unsafe source path",
        )
        require(
            source["sha256"] == file_hash(path),
            f"source hash drift: {path}",
        )


def validate_certificate(
    artifact: dict[str, Any], *, exact_rebuild: bool = False
) -> None:
    require_exact_keys(artifact, TOP_KEYS, "top-level")
    require(artifact["schema"] == SCHEMA, "schema drift")
    require(artifact["artifact_kind"] == ARTIFACT_KIND, "artifact kind drift")
    require(artifact["status"] == STATUS, "status drift")
    require(
        artifact["payload_sha256"] == payload_hash(artifact),
        "payload hash drift",
    )
    validate_source_bindings(artifact["source_bindings"])

    expected_sections = {
        "row": expected_row(),
        "predecessor_state": expected_predecessor_state(),
        "tdd_object": expected_tdd_object(),
        "excess_factorization": expected_excess_factorization(),
        "overlap_control": expected_overlap_control(),
        "defect_span_bridge": expected_defect_span_bridge(),
        "owner_registry": expected_owner_registry(),
        "classifier_contract": expected_classifier_contract(),
        "exact_controls": expected_exact_controls(),
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
    }
    for label, expected in expected_sections.items():
        require(type(artifact[label]) is dict, f"{label} is not an object")
        require(
            canonical_bytes(artifact[label]) == canonical_bytes(expected),
            f"{label} payload or JSON type drift",
        )
    require(artifact["charges"] == [], "unexpected banked charge record")
    require(artifact["nonclaims"] == NONCLAIMS, "nonclaim list drift")

    row = artifact["row"]
    for key in (
        "p",
        "ambient_extension_degree",
        "n",
        "k",
        "agreement_A",
        "redundancy_R",
        "error_cap_j",
        "full_row_rank_threshold_t",
        "minimum_distance",
        "deep_error_cutoff_r_star",
        "surviving_error_weight_floor_L",
        "three_times_L",
    ):
        require_int(row[key], f"row.{key}")

    factorization = artifact["excess_factorization"]
    require(
        factorization["shortened_space_dimension"] == "e+1"
        and factorization["silent_shell_bound"]
        == "|U_MINUS_supp(Delta)|<=e"
        and factorization["projective_multiplicity_is_payment"] is False,
        "factorization boundary drift",
    )

    bridge = artifact["defect_span_bridge"]
    require(
        bridge["numerator_scope"] == "DISTINCT_FINITE_BAD_SLOPES"
        and bridge["one_witness_per_retained_slope_is_complete_for_numerator"]
        is True
        and bridge["all_codewords_at_each_slope_required"] is False
        and bridge["selector_set_finite_nonempty_deployed"] is True
        and bridge["intrinsic_minimum_attained_deployed"] is True
        and bridge["carrier_owner_existential_over_complete_selectors"]
        is True
        and bridge["kappa_star_ge_11_implies_every_selector_high_union"]
        is True
        and bridge["carrier_and_rank_minimizers_may_differ"] is True
        and bridge["chosen_selector_attains_intrinsic_minimum"] is True
        and bridge["tdd_regenerated_on_chosen_rank_minimizer"] is True
        and bridge["tdd_regeneration_family_size_floor"] == 16
        and bridge["syndrome_direction_y1_nonzero_from_transversality"]
        is True
        and bridge["rank_identity"]
        == "s_star=1+dim(R_sel)_FOR_MINIMIZING_SELECTOR"
        and bridge["rank_computed_on_local_triple_only"] is False
        and bridge[
            "arbitrary_nonminimizing_selector_certifies_exact_intrinsic_rank"
        ]
        is False
        and bridge["any_complete_selector_rank_le_3_certifies_payment"]
        is True
        and bridge["basis_carrier_equals_complete_selected_union"] is True
        and bridge["basis_carrier_is_canonical"] is False
        and bridge["largest_budget_fitting_affine_rank"] == 3
        and bridge["rank3_fits"] is True
        and bridge["rank4_min_postdeep_fits"] is False
        and bridge["rank4_fits"] is False
        and bridge["first_unpaid_basis_carrier_slopes"] == 5,
        "defect-span bridge drift",
    )

    classifier = artifact["classifier_contract"]
    controls = classifier["controls"]
    require(
        controls["named_owner"]["terminal"]
        == "PAID_NAMED_PREDECESSOR_OWNER"
        and controls["global_carrier_10"]["terminal"]
        == "PAID_GLOBAL_CARRIER_EXCESS_LE_10"
        and controls["global_carrier_11"]["terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and controls["complete_rank_3"]["terminal"]
        == "PAID_SELECTED_AFFINE_CORE_RANK_LE_3"
        and controls["complete_rank_4"]["terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and controls["certified_primitive_rank_4"]["terminal"]
        == "UNPAID_PRIMITIVE_INTRINSIC_RANK3_TDD_SPREAD"
        and controls["local_triple_rank_2_only"]["terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and controls["nonminimizing_complete_rank_3"]["terminal"]
        == "PAID_SELECTED_AFFINE_CORE_RANK_LE_3"
        and controls["nonminimizing_complete_rank_4"]["terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and controls["small_family_rank_4"]["terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and controls["missing_witness_contract"]["terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and controls["undeclared_future_union"]["terminal"]
        == "REJECTED_UNDECLARED_FUTURE_OWNER"
        and classifier["deployed_complete_selector_certificate_present"]
        is False
        and classifier["deployed_retained_family_size_gt_15_from_predecessor"]
        is True
        and classifier["deployed_intrinsic_affine_rank_known"] is False
        and classifier["deployed_terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and classifier["classifier_banks_charge"] is False,
        "classifier fail-closed boundary drift",
    )

    exact = artifact["exact_controls"]["big_integer_boundaries"]
    require(
        exact["rank3_cap_fits"] is True
        and exact["rank4_min_postdeep_cap_fits"] is False
        and exact["rank4_cap_fits"] is False
        and exact["union_c_le_2_fits"] is True
        and exact["union_c_le_3_fits"] is False
        and exact["projective_minimum_fits"] is False
        and exact["central_e0_union_lower_bound_exceeds_budget"] is True
        and exact["raw_union_or_projective_enumeration_pays"] is False,
        "exact boundary classification drift",
    )

    ledger = artifact["ledger"]
    require_int(ledger["K_rem"], "ledger.K_rem")
    require(
        ledger["conditional_terminal_proved"] is True
        and ledger["conditional_terminal_exhaustive_for_deployed_residual"]
        is False
        and ledger["packet_banked_charge"] == "0"
        and ledger["tdd_charge"] is None
        and ledger["affine_core_charge"] is None
        and ledger["union_charge"] is None
        and int(ledger["U_paid_after"]) == U_PAID
        and int(ledger["B_remaining_after"]) == B_REMAINING
        and ledger["ledger_consequence"] is False
        and ledger["branch3_closed"] is False
        and ledger["U_2"] is None
        and ledger["U_Q"] is None
        and ledger["U_A"] is None
        and ledger["lhs"] is None
        and ledger["row_complete"] is False,
        "no-bank ledger boundary drift",
    )

    if exact_rebuild:
        require(
            canonical_bytes(artifact) == canonical_bytes(build_certificate()),
            "certificate differs from exact rebuild",
        )


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    current = value
    for token in path[:-1]:
        current = current[token]
    current[path[-1]] = replacement


def run_tamper_selftest(artifact: dict[str, Any]) -> int:
    rejected = 0

    def mutate(name: str, path: tuple[Any, ...], replacement: Any) -> None:
        nonlocal rejected
        candidate = copy.deepcopy(artifact)
        set_path(candidate, path, replacement)
        candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except VerificationError:
            rejected += 1
            return
        raise VerificationError(f"tamper accepted: {name}")

    mutations = [
        ("schema", ("schema",), SCHEMA + "-drift"),
        ("kind", ("artifact_kind",), "ROW_CLOSURE"),
        ("status", ("status",), "PROVED_ROW_SAFE"),
        ("row-n", ("row", "n"), N - 1),
        ("row-k", ("row", "k"), K - 1),
        ("row-A", ("row", "agreement_A"), A - 1),
        ("row-R", ("row", "redundancy_R"), R - 1),
        ("row-j", ("row", "error_cap_j"), J - 1),
        ("row-t", ("row", "full_row_rank_threshold_t"), T - 1),
        ("row-distance", ("row", "minimum_distance"), MINIMUM_DISTANCE - 1),
        ("row-heavy", ("row", "surviving_error_weight_floor_L"), R_STAR),
        ("row-budget", ("row", "B_remaining"), str(B_REMAINING - 1)),
        (
            "predecessor-closed",
            ("predecessor_state", "branch3_closed_after"),
            True,
        ),
        (
            "tdd-not-uniform-over-selectors",
            (
                "predecessor_state",
                "predecessor_tdd_theorem_uniform_over_complete_selectors",
            ),
            False,
        ),
        (
            "zero-tdd",
            ("tdd_object", "nonzero_required"),
            False,
        ),
        (
            "off-by-one-carrier",
            ("tdd_object", "carrier_excess"),
            "kappa(U)=e",
        ),
        (
            "local-global-carrier",
            ("tdd_object", "local_e_le_9_implies_global_carrier_payment"),
            True,
        ),
        (
            "shortened-dimension",
            ("excess_factorization", "shortened_space_dimension"),
            "e",
        ),
        (
            "silent-bound",
            ("excess_factorization", "silent_shell_bound"),
            "|silent|<=e+1",
        ),
        (
            "projective-payment",
            ("excess_factorization", "projective_multiplicity_is_payment"),
            True,
        ),
        (
            "common-gcd-forced",
            ("overlap_control", "complete_family_common_gcd_forced"),
            True,
        ),
        (
            "local-rank",
            ("defect_span_bridge", "rank_computed_on_local_triple_only"),
            True,
        ),
        (
            "carrier-not-existential",
            (
                "defect_span_bridge",
                "carrier_owner_existential_over_complete_selectors",
            ),
            False,
        ),
        (
            "kappa-complement-not-uniform",
            (
                "defect_span_bridge",
                "kappa_star_ge_11_implies_every_selector_high_union",
            ),
            False,
        ),
        (
            "rank-selector-not-minimizing",
            (
                "defect_span_bridge",
                "chosen_selector_attains_intrinsic_minimum",
            ),
            False,
        ),
        (
            "tdd-not-regenerated",
            (
                "defect_span_bridge",
                "tdd_regenerated_on_chosen_rank_minimizer",
            ),
            False,
        ),
        (
            "syndrome-direction-not-certified",
            (
                "defect_span_bridge",
                "syndrome_direction_y1_nonzero_from_transversality",
            ),
            False,
        ),
        (
            "all-codewords-required",
            (
                "defect_span_bridge",
                "all_codewords_at_each_slope_required",
            ),
            True,
        ),
        (
            "nonmin-low-rank-does-not-pay",
            (
                "defect_span_bridge",
                "any_complete_selector_rank_le_3_certifies_payment",
            ),
            False,
        ),
        (
            "rank-identity",
            ("defect_span_bridge", "rank_identity"),
            "s=dim(R_sel)",
        ),
        (
            "basis-carrier",
            (
                "defect_span_bridge",
                "basis_carrier_equals_complete_selected_union",
            ),
            False,
        ),
        (
            "basis-carrier-canonical",
            ("defect_span_bridge", "basis_carrier_is_canonical"),
            True,
        ),
        (
            "rank3-cap",
            ("defect_span_bridge", "rank3_cap"),
            str(AFFINE_RANK3_CAP - 1),
        ),
        (
            "rank4-fits",
            ("defect_span_bridge", "rank4_fits"),
            True,
        ),
        (
            "rank4-min-heavy-fits",
            ("defect_span_bridge", "rank4_min_postdeep_fits"),
            True,
        ),
        (
            "paid-rank4",
            (
                "classifier_contract",
                "controls",
                "complete_rank_4",
                "terminal",
            ),
            "PAID_SELECTED_AFFINE_CORE_RANK_LE_4",
        ),
        (
            "paid-local-triple",
            (
                "classifier_contract",
                "controls",
                "local_triple_rank_2_only",
                "terminal",
            ),
            "PAID_SELECTED_AFFINE_CORE_RANK_LE_3",
        ),
        (
            "reject-nonminimizing-low-rank-selector",
            (
                "classifier_contract",
                "controls",
                "nonminimizing_complete_rank_3",
                "terminal",
            ),
            "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED",
        ),
        (
            "primitive-without-kappa-star",
            (
                "classifier_contract",
                "controls",
                "complete_rank_4",
                "terminal",
            ),
            "UNPAID_PRIMITIVE_INTRINSIC_RANK3_TDD_SPREAD",
        ),
        (
            "future-owner",
            ("owner_registry", "future_union_owner_proved"),
            True,
        ),
        (
            "delete-forbidden",
            ("owner_registry", "forbidden_inferences", 0),
            "LOCAL_TRIPLE_e_LE_9_IMPLIES_GLOBAL_CARRIER_ALLOWED",
        ),
        (
            "union-c3-fits",
            (
                "exact_controls",
                "big_integer_boundaries",
                "union_c_le_3_fits",
            ),
            True,
        ),
        (
            "exact-rank4-min-heavy-fits",
            (
                "exact_controls",
                "big_integer_boundaries",
                "rank4_min_postdeep_cap_fits",
            ),
            True,
        ),
        (
            "projective-fits",
            (
                "exact_controls",
                "big_integer_boundaries",
                "projective_minimum_fits",
            ),
            True,
        ),
        (
            "central-union-fits",
            (
                "exact_controls",
                "big_integer_boundaries",
                "central_e0_union_lower_bound_exceeds_budget",
            ),
            False,
        ),
        (
            "fixture-counterexample",
            (
                "exact_controls",
                "deployed_e1_fixture_arithmetic",
                "fixture_is_branch3_counterexample",
            ),
            True,
        ),
        (
            "fixture-not-carrier-paid",
            (
                "exact_controls",
                "deployed_e1_fixture_arithmetic",
                "fixture_paid_by_global_carrier",
            ),
            False,
        ),
        (
            "fixture-claims-all-heavy-witnesses-classified",
            (
                "exact_controls",
                "deployed_e1_fixture_arithmetic",
                "other_heavy_witnesses_for_same_slopes_classified",
            ),
            True,
        ),
        (
            "bank-charge",
            ("ledger", "packet_banked_charge"),
            str(AFFINE_RANK3_CAP),
        ),
        (
            "tdd-zero",
            ("ledger", "tdd_charge"),
            "0",
        ),
        (
            "move-U-paid",
            ("ledger", "U_paid_after"),
            str(U_PAID + AFFINE_RANK3_CAP),
        ),
        (
            "move-budget",
            ("ledger", "B_remaining_after"),
            str(B_REMAINING - AFFINE_RANK3_CAP),
        ),
        (
            "ledger-consequence",
            ("ledger", "ledger_consequence"),
            True,
        ),
        (
            "branch3-closed",
            ("ledger", "branch3_closed"),
            True,
        ),
        ("UQ-zero", ("ledger", "U_Q"), 0),
        ("UA-zero", ("ledger", "U_A"), 0),
        ("row-complete", ("ledger", "row_complete"), True),
        (
            "source-hash",
            ("source_bindings", 0, "sha256"),
            "0" * 64,
        ),
        (
            "source-path",
            ("source_bindings", 0, "path"),
            "../unsafe",
        ),
        (
            "duplicate-binding",
            ("source_bindings", 1, "binding_id"),
            artifact["source_bindings"][0]["binding_id"],
        ),
        (
            "nonclaim",
            ("nonclaims", 0),
            "This packet proves the KoalaBear row safe.",
        ),
    ]
    for name, path, replacement in mutations:
        mutate(name, path, replacement)

    candidate = copy.deepcopy(artifact)
    candidate["unexpected_top_level"] = True
    candidate["payload_sha256"] = payload_hash(candidate)
    try:
        validate_certificate(candidate)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: unknown top-level key")

    candidate = copy.deepcopy(artifact)
    candidate["ledger"]["unexpected_nested"] = True
    candidate["payload_sha256"] = payload_hash(candidate)
    try:
        validate_certificate(candidate)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: unknown nested key")

    bad_payload = copy.deepcopy(artifact)
    bad_payload["payload_sha256"] = "0" * 64
    try:
        validate_certificate(bad_payload)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: payload hash")

    try:
        parse_json('{"a":1,"a":2}', "duplicate-key-control")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: duplicate JSON key")

    try:
        parse_json('{"a":NaN}', "nonstandard-constant-control")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: NaN")

    return rejected


def write_certificate(artifact: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    artifact = build_certificate()

    if args.write:
        validate_certificate(artifact, exact_rebuild=True)
        write_certificate(artifact)
        print(f"WROTE {CERT_PATH.relative_to(ROOT)}")
        return 0

    if args.check:
        loaded = load_json(CERT_PATH)
        validate_certificate(loaded, exact_rebuild=True)
        print("PASS m1-kb-branch3-tdd-excess-v1")
        print(
            "rank boundary: C(j+3,3)=%d <= %d < C(L+4,4)=%d"
            % (
                AFFINE_RANK3_CAP,
                B_REMAINING,
                AFFINE_RANK4_MIN_POSTDEEP_CAP,
            )
        )
        print(
            "rank-4 maximal-weight diagnostic: C(j+4,4)=%d"
            % AFFINE_RANK4_CAP
        )
        print(
            "ledger: no charge banked; U_paid=%d; B_remaining=%d"
            % (U_PAID, B_REMAINING)
        )
        print(
            "next: affine-rank 4, defect-span rank 3, five-support carrier"
        )
        return 0

    rejected = run_tamper_selftest(artifact)
    print(f"PASS tamper-selftest: {rejected}/{rejected} mutations rejected")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
