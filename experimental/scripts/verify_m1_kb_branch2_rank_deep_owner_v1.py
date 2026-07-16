#!/usr/bin/env python3
"""Verify the KoalaBear branch-2 rank/deep owner packet.

For an actual MCA-bad slope at agreement A, the ambient field-native Hankel
rank is the minimum of the row depth t and the actual nonzero error weight.
Rank drop therefore lifts the same witness to the deep agreement n-t+1, where
Paper D bounds the distinct bad-slope set by t.  The charge is global once.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import math
import sys
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-branch2-rank-deep-owner-v1"
ARTIFACT_KIND = "M1_KB_BRANCH2_RANK_DEEP_OWNER"
STATUS = (
    "PROVED_FIELD_NATIVE_RANK_DROP_POLICY_DEEP_MCA_OWNER_"
    "BRANCH2_CLOSED_LEGACY_BRIDGE_RETIRED_PARTIAL_LEDGER"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch2-rank-deep-owner-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch2_rank_deep_owner_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md"
)
VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.sage"
)
PAPER_D_REL = Path("tex/cs25_cap_v12.tex")
THRESHOLDS_REL = Path("experimental/rs_mca_thresholds.tex")
PIVOT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch2_hankel_pivot_adapter_v1.md"
)
PIVOT_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch2-hankel-pivot-adapter-v1/"
    "m1_kb_branch2_hankel_pivot_adapter_v1.json"
)
PIVOT_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.py"
)
FIRST_MATCH_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
)
FIRST_MATCH_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/"
    "kb_mca_1116048_first_match_ledger_v1.json"
)
BASE_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "kb_mca_1116048_base_slope_universe_v2.md"
)
BASE_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2/"
    "kb_mca_1116048_base_slope_universe_v2.json"
)
BASE_VERIFIER_REL = Path(
    "experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py"
)
POST_C5_CERT_REL = Path(
    "experimental/data/certificates/m1-fp2-post-c5-mask-incidence-v1/"
    "m1_fp2_post_c5_mask_incidence_v1.json"
)

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
T = A - K
R0 = T - 1
A_DEEP = N - R0
LOCATOR_COORDS = J + 1
DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID_BEFORE = 2_602_153_473
RANK_DROP_CHARGE = T
U_PAID_AFTER = U_PAID_BEFORE + RANK_DROP_CHARGE
B_REMAINING_AFTER = B_STAR - U_PAID_AFTER
K_REM = 4_807_520

V2_ORDER = [
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
    "rank_drop_policy",
    "exact_support_rank_bridge",
    "deep_witness_lift",
    "deep_mca_owner",
    "branch2_first_match",
    "legacy_bridge_retirement",
    "small_field_control",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

EDGE_CASES = [
    "Rank is ambient F-rank of the t by (j+1) Hankel matrix.",
    "The rank threshold is t, not j+1 and not a scalar-stack threshold.",
    "The owner is intersected with the actual MCA-bad set; raw rank drop is not paid.",
    "The literal first-match rank cell subtracts branch 1 and is a subset of the safe rank-drop envelope.",
    "The actual error support omits zero-amplitude padding in the chosen co-support.",
    "The empty actual error support has rank zero but is paid only when noncontainment holds.",
    "The full agreement set enlarges the original witness support, so noncontainment persists upward.",
    "The derived deep agreement is n-t+1, not n-t.",
    "The charge counts distinct finite slopes globally once, not supports, charts, or pivots.",
    "Null is not zero.",
]

REMAINING_RISKS = [
    "Branch 3 tangent/common-line/residue-line still lacks a complete row-specific projector.",
    "The field-full quadratic support union and branches 4 through 5 remain open.",
    "U_2, U_Q, and U_A remain null.",
    "The complete KoalaBear upper ledger and row inequality remain undecided.",
]

NONCLAIMS = [
    "This packet does not prove the KoalaBear row safe.",
    "This packet does not count the raw algebraic rank-drop locus.",
    "This packet does not use or validate scalar-stack rank as ambient rank.",
    "This packet does not prove the legacy cyclotomic and field-native pivots equivalent.",
    "This packet does not close branch 1 or branches 3 through 5.",
    "This packet does not determine U_2, U_Q, or U_A.",
    "This packet does not begin the degree-three parameter class.",
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
        binding("packet-note", NOTE_REL, "human-readable proof and audit"),
        binding(
            "python-verifier",
            VERIFIER_REL,
            "deterministic certificate and mutation replay",
        ),
        binding(
            "sage-control",
            SAGE_REL,
            "independent rank, padding, incidence, and sharpness replay",
        ),
        binding(
            "paper-d-v12",
            PAPER_D_REL,
            "weighted Hankel convention and deep-MCA theorem",
        ),
        binding(
            "exact-thresholds",
            THRESHOLDS_REL,
            "exact-support reduction and tangent-floor sharpness",
        ),
        binding(
            "pivot-note",
            PIVOT_NOTE_REL,
            "field-native finite-pivot predecessor",
        ),
        binding(
            "pivot-certificate",
            PIVOT_CERT_REL,
            "machine-readable pivot-empty predecessor and row dimensions",
        ),
        binding(
            "pivot-verifier",
            PIVOT_VERIFIER_REL,
            "predecessor semantic and mutation replay",
        ),
        binding(
            "first-match-note",
            FIRST_MATCH_NOTE_REL,
            "frozen branch order and legacy cyclotomic dependency",
        ),
        binding(
            "first-match-certificate",
            FIRST_MATCH_CERT_REL,
            "machine-readable predecessor branch order",
        ),
        binding(
            "base-v2-note",
            BASE_NOTE_REL,
            "deployed base-slope replacement and retirement rationale",
        ),
        binding(
            "base-v2-certificate",
            BASE_CERT_REL,
            "current paid baseline, branch order, and null open terms",
        ),
        binding(
            "base-v2-verifier",
            BASE_VERIFIER_REL,
            "current baseline arithmetic replay",
        ),
        binding(
            "post-c5-certificate",
            POST_C5_CERT_REL,
            "open branch-3 through branch-5 source status",
        ),
    ]


def mod_inverse(value: int, prime: int) -> int:
    value %= prime
    require(value != 0, "attempted inversion of zero")
    return pow(value, -1, prime)


def dual_weights(domain: list[int], prime: int) -> list[int]:
    weights: list[int] = []
    for index, point in enumerate(domain):
        denominator = 1
        for other_index, other in enumerate(domain):
            if index != other_index:
                denominator = denominator * (point - other) % prime
        weights.append(mod_inverse(denominator, prime))
    return weights


def syndrome(
    word: list[int],
    domain: list[int],
    weights: list[int],
    redundancy: int,
    prime: int,
) -> list[int]:
    return [
        sum(
            weights[index]
            * pow(domain[index], moment, prime)
            * word[index]
            for index in range(len(domain))
        )
        % prime
        for moment in range(redundancy)
    ]


def hankel_matrix(
    syndrome_vector: list[int], depth: int, co_support_size: int
) -> list[list[int]]:
    require(
        len(syndrome_vector) >= depth + co_support_size,
        "syndrome window too short",
    )
    return [
        [
            syndrome_vector[row + column]
            for column in range(co_support_size + 1)
        ]
        for row in range(depth)
    ]


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "ragged matrix")
    work = [[value % prime for value in row] for row in matrix]
    rank = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = mod_inverse(work[rank][column], prime)
        work[rank] = [value * inverse % prime for value in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (work[row][entry] - factor * work[rank][entry])
                    % prime
                    for entry in range(width)
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def matrix_multiply_mod(
    left: list[list[int]], right: list[list[int]], prime: int
) -> list[list[int]]:
    require(left and right, "empty matrix product")
    inner = len(left[0])
    require(all(len(row) == inner for row in left), "ragged left matrix")
    require(len(right) == inner, "matrix product dimension mismatch")
    width = len(right[0])
    require(all(len(row) == width for row in right), "ragged right matrix")
    return [
        [
            sum(left[row][middle] * right[middle][column] for middle in range(inner))
            % prime
            for column in range(width)
        ]
        for row in range(len(left))
    ]


def explained_by_constant(
    word: list[int], support: tuple[int, ...], prime: int
) -> bool:
    values = {word[index] % prime for index in support}
    return len(values) <= 1


def bad_supports_constant_code(
    f: list[int],
    g: list[int],
    slope: int,
    agreement: int,
    prime: int,
) -> list[tuple[int, ...]]:
    word = [
        (f[index] + slope * g[index]) % prime
        for index in range(len(f))
    ]
    records: list[tuple[int, ...]] = []
    for support in combinations(range(len(f)), agreement):
        if not explained_by_constant(word, support, prime):
            continue
        jointly_contained = explained_by_constant(
            f, support, prime
        ) and explained_by_constant(g, support, prime)
        if not jointly_contained:
            records.append(support)
    return records


def vandermonde_factorization(
    domain: list[int],
    weights: list[int],
    error: list[int],
    depth: int,
    co_support_size: int,
    prime: int,
) -> list[list[int]]:
    actual_support = [
        index for index, value in enumerate(error) if value % prime
    ]
    left = [
        [
            pow(domain[index], row, prime)
            * weights[index]
            * error[index]
            % prime
            for index in actual_support
        ]
        for row in range(depth)
    ]
    right = [
        [
            pow(domain[index], column, prime)
            for column in range(co_support_size + 1)
        ]
        for index in actual_support
    ]
    return matrix_multiply_mod(left, right, prime)


@functools.cache
def build_small_field_control() -> dict[str, Any]:
    prime = 7
    domain = list(range(7))
    n = len(domain)
    dimension = 1
    agreement = 4
    redundancy = n - dimension
    co_support_size = n - agreement
    depth = agreement - dimension
    r0 = depth - 1
    deep_agreement = n - r0
    require(
        (n, dimension, agreement, co_support_size, depth, r0, deep_agreement)
        == (7, 1, 4, 3, 3, 2, 5),
        "small control dimensions drift",
    )

    tangent_coordinates = [0, 1, 2]
    sharp_slopes = [0, 1, 2]
    f = [0] * n
    g = [0] * n
    for index, slope in zip(tangent_coordinates, sharp_slopes):
        f[index] = (-slope) % prime
        g[index] = 1

    weights = dual_weights(domain, prime)
    u = syndrome(f, domain, weights, redundancy, prime)
    v = syndrome(g, domain, weights, redundancy, prime)

    ranks: dict[str, int] = {}
    error_weights: dict[str, int] = {}
    original_bad: list[int] = []
    deep_bad: list[int] = []
    branch2_slopes: list[int] = []
    original_witness_counts: dict[str, int] = {}
    deep_witness_counts: dict[str, int] = {}

    for slope in range(prime):
        combined_syndrome = [
            (u[index] + slope * v[index]) % prime
            for index in range(redundancy)
        ]
        matrix = hankel_matrix(
            combined_syndrome, depth, co_support_size
        )
        rank = matrix_rank_mod(matrix, prime)
        ranks[str(slope)] = rank

        word = [
            (f[index] + slope * g[index]) % prime
            for index in range(n)
        ]
        error_weights[str(slope)] = sum(value != 0 for value in word)
        original_supports = bad_supports_constant_code(
            f, g, slope, agreement, prime
        )
        deep_supports = bad_supports_constant_code(
            f, g, slope, deep_agreement, prime
        )
        original_witness_counts[str(slope)] = len(original_supports)
        deep_witness_counts[str(slope)] = len(deep_supports)
        if original_supports:
            original_bad.append(slope)
        if deep_supports:
            deep_bad.append(slope)
        if original_supports and rank < depth:
            branch2_slopes.append(slope)

    require(original_bad == sharp_slopes, "sharp original bad slopes drift")
    require(deep_bad == sharp_slopes, "sharp deep bad slopes drift")
    require(branch2_slopes == sharp_slopes, "sharp branch-2 slopes drift")
    require(
        all(ranks[str(slope)] == r0 for slope in sharp_slopes),
        "sharp branch-2 rank drift",
    )
    require(
        all(error_weights[str(slope)] == r0 for slope in sharp_slopes),
        "sharp branch-2 error weight drift",
    )

    designed_slope = 0
    designed_word = [
        (f[index] + designed_slope * g[index]) % prime
        for index in range(n)
    ]
    designed_actual_error = [
        index for index, value in enumerate(designed_word) if value
    ]
    designed_exact_support = (0, 3, 4, 5)
    designed_co_support = tuple(
        index for index in range(n) if index not in designed_exact_support
    )
    padded_zero_points = sorted(
        set(designed_co_support) - set(designed_actual_error)
    )
    require(
        designed_actual_error == [1, 2]
        and designed_co_support == (1, 2, 6)
        and padded_zero_points == [6],
        "designed padding control drift",
    )
    require(
        designed_exact_support
        in bad_supports_constant_code(
            f, g, designed_slope, agreement, prime
        ),
        "designed exact witness missing",
    )
    designed_syndrome = [
        (u[index] + designed_slope * v[index]) % prime
        for index in range(redundancy)
    ]
    designed_matrix = hankel_matrix(
        designed_syndrome, depth, co_support_size
    )
    designed_factorization = vandermonde_factorization(
        domain,
        weights,
        designed_word,
        depth,
        co_support_size,
        prime,
    )
    require(
        designed_matrix == designed_factorization,
        "small-field Vandermonde factorization failed",
    )
    require(
        matrix_rank_mod(designed_matrix, prime)
        == len(designed_actual_error)
        == r0,
        "small-field rank equals actual support failed",
    )

    contained_f = [0] * n
    contained_g = [0] * n
    contained_rank_drop_slopes: list[int] = []
    contained_bad_slopes: list[int] = []
    for slope in range(prime):
        contained_syndrome = syndrome(
            [
                (
                    contained_f[index]
                    + slope * contained_g[index]
                )
                % prime
                for index in range(n)
            ],
            domain,
            weights,
            redundancy,
            prime,
        )
        if matrix_rank_mod(
            hankel_matrix(
                contained_syndrome, depth, co_support_size
            ),
            prime,
        ) < depth:
            contained_rank_drop_slopes.append(slope)
        if bad_supports_constant_code(
            contained_f,
            contained_g,
            slope,
            agreement,
            prime,
        ):
            contained_bad_slopes.append(slope)

    require(
        contained_rank_drop_slopes == list(range(prime)),
        "raw contained rank-drop control drift",
    )
    require(
        contained_bad_slopes == [],
        "contained pair acquired an MCA-bad slope",
    )

    return {
        "status": "EXACT_TOY_SHARPNESS_AND_INCIDENCE_CONTROL",
        "p": prime,
        "n": n,
        "k": dimension,
        "agreement_A": agreement,
        "redundancy_R": redundancy,
        "co_support_size_j": co_support_size,
        "hankel_depth_t": depth,
        "r0": r0,
        "deep_agreement": deep_agreement,
        "domain": domain,
        "dual_weights": weights,
        "f": f,
        "g": g,
        "tangent_coordinates": tangent_coordinates,
        "sharp_slopes": sharp_slopes,
        "original_bad_slopes": original_bad,
        "deep_bad_slopes": deep_bad,
        "branch2_slopes": branch2_slopes,
        "branch2_count": len(branch2_slopes),
        "ranks_by_slope": ranks,
        "zero_codeword_error_weights_by_slope": error_weights,
        "original_witness_counts_by_slope": original_witness_counts,
        "deep_witness_counts_by_slope": deep_witness_counts,
        "designed_slope": designed_slope,
        "designed_exact_support": list(designed_exact_support),
        "designed_co_support": list(designed_co_support),
        "designed_actual_error_support": designed_actual_error,
        "designed_padded_zero_points": padded_zero_points,
        "designed_matrix": designed_matrix,
        "designed_factorization": designed_factorization,
        "factorization_exact": True,
        "rank_equals_min_t_actual_error_weight": True,
        "full_agreement_lift_checked": True,
        "sharp_charge_realized": True,
        "contained_raw_rank_drop_slopes": contained_rank_drop_slopes,
        "contained_bad_slopes": contained_bad_slopes,
        "raw_rank_drop_requires_actual_bad_incidence": True,
        "original_supports_per_slope": math.comb(n, agreement),
        "deep_supports_per_slope": math.comb(n, deep_agreement),
        "all_slopes_scanned": prime,
        "evidence_scope": "EXACT_TOY_CONTROL_NOT_DEPLOYED_PROOF",
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
        "co_support_size_j": J,
        "hankel_depth_t": T,
        "r0": R0,
        "deep_agreement": A_DEEP,
        "locator_coordinate_count": LOCATOR_COORDS,
        "ambient_hankel_shape": [T, LOCATOR_COORDS],
        "three_r0": 3 * R0,
        "deep_gate_rhs_n_minus_k": R,
        "B_star": str(B_STAR),
        "challenge_scope": "distinct finite slopes in F_(p^6)",
    }


def expected_rank_drop_policy() -> dict[str, Any]:
    return {
        "branch_number": 2,
        "predecessor_label": "rank_drop_or_pivot_failure",
        "safe_bounding_envelope": (
            "Z_2_env(f,g)=Bad_A(f,g)_INTERSECT_"
            "{gamma:rank_F(M_A(gamma))<t}"
        ),
        "literal_first_match_residual": (
            "Z_2_fm(f,g)=(Bad_A(f,g)_MINUS_Z_1(f,g))_INTERSECT_"
            "Z_2_env(f,g)"
        ),
        "literal_first_match_residual_subset_of_envelope": True,
        "requires_actual_bad_incidence": True,
        "raw_algebraic_rank_drop_paid": False,
        "matrix": (
            "M_A(gamma)=H_(t,j)(Syn_F(f+gamma*g))="
            "H_(t,j)(Syn_F(f))+gamma*H_(t,j)(Syn_F(g))"
        ),
        "matrix_shape": [T, LOCATOR_COORDS],
        "rank_field": "AMBIENT_F",
        "rank_threshold": T,
        "rank_predicate": "rank_F(M_A(gamma))<t",
        "failure_of_full_row_rank": True,
        "overdetermined_rank_less_than_j_plus_1_used": False,
        "scalar_stack_rank_used": False,
        "support_selector_used": False,
        "slope_set_is_support_independent": True,
        "infinity_included": False,
    }


def expected_exact_support_rank_bridge() -> dict[str, Any]:
    return {
        "exact_support_reduction_used": True,
        "exact_witness_support_size": A,
        "chosen_co_support_size": J,
        "actual_error_definition": "e_gamma=f+gamma*g-c",
        "actual_error_support": "E_gamma=supp(e_gamma)",
        "actual_error_support_subset_of_chosen_co_support": True,
        "actual_error_weight_upper_bound_before_rank": J,
        "zero_amplitude_padding_excluded": True,
        "nonzero_weight_formula": "w_x=lambda_x*e_gamma(x)",
        "factorization": (
            "M_A(gamma)=V_t(E_gamma)^T*diag(w_x)*V_(j+1)(E_gamma)"
        ),
        "right_vandermonde_surjective": True,
        "diagonal_invertible": True,
        "rank_identity": "rank_F(M_A(gamma))=min(t,|E_gamma|)",
        "rank_drop_equivalence": "rank_F(M_A(gamma))<t_IFF_|E_gamma|<=t-1",
        "rank_drop_error_weight_cap": R0,
        "empty_actual_error_support_allowed": True,
        "source_status": "PROVED_HERE_FROM_WEIGHTED_MOMENTS",
    }


def expected_deep_witness_lift() -> dict[str, Any]:
    return {
        "r0": R0,
        "deep_agreement_formula": "A_deep=n-r0=n-t+1",
        "deep_agreement": A_DEEP,
        "full_agreement_support": "S_star=D_MINUS_E_gamma",
        "full_agreement_size_lower_bound": A_DEEP,
        "original_support_subset_of_full_agreement_support": True,
        "same_codeword_explains_on_full_agreement_support": True,
        "noncontainment_persists_upward": True,
        "rank_drop_slope_is_deep_mca_bad": True,
        "separate_tangent_bridge_required": False,
        "off_by_one_guard": "n-t+1_NOT_n-t",
    }


def expected_deep_mca_owner() -> dict[str, Any]:
    return {
        "owner_id": "DEEP_MCA_RANK_DROP",
        "source_theorem": "tex/cs25_cap_v12.tex#thm:deep-mca",
        "theorem_object": "distinct finite MCA-bad slopes of one received pair",
        "deep_radius_error_count": R0,
        "gate_lhs_three_r0": 3 * R0,
        "gate_rhs_n_minus_k": R,
        "gate_holds": True,
        "upper_bound_formula": "r0+1=t",
        "upper_bound": T,
        "scope": "FIRST_MATCH_GLOBAL_ONCE",
        "per_support_charge": False,
        "per_pivot_charge": False,
        "uniform_in_received_pair": True,
        "charge_sharp": True,
        "sharpness_source": (
            "experimental/rs_mca_thresholds.tex#"
            "prop:universal-tangent-floor at agreement n-(t-1)"
        ),
        "sharpness_slopes": T,
    }


def expected_branch2_first_match() -> dict[str, Any]:
    return {
        "v2_order": V2_ORDER,
        "branch_index_one_based": 2,
        "branch_label": "rank_drop_or_pivot_failure",
        "rank_drop_owner": "DEEP_MCA_RANK_DROP",
        "rank_drop_charge": str(T),
        "pivot_failure_owner": "EMPTY_ACTUAL_BAD_SLOPE_SET",
        "pivot_failure_charge": "0",
        "pivot_failure_empty_imported_from_predecessor": True,
        "full_row_rank_pivot_success_survives_to_branch": 3,
        "later_branches_restricted_to_branch2_complement": True,
        "rank_drop_envelope_bound_used": True,
        "literal_rank_drop_cell_subset_of_envelope": True,
        "branch2_local_policy_complete": True,
        "branch1_projector_complete": False,
        "global_mask_replay_complete": False,
        "branches_3_to_5_complete": False,
    }


def expected_legacy_bridge_retirement() -> dict[str, Any]:
    return {
        "status": "RETIRED_NOT_REQUIRED_FOR_DEPLOYED_BRANCH2",
        "scope": "DEPLOYED_BRANCH2_ONLY",
        "legacy_symbol": "red_p(B_0(S))",
        "field_native_symbol": "B_Han(T)[h]",
        "identification_proved": False,
        "equivalence_claimed": False,
        "global_invalidity_claimed": False,
        "cyclotomic_lift_required_for_current_branch2_charge": False,
        "base_v2_requires_affine_row_adapter": False,
        "old_generated_collision_owner_optional_refinement": True,
        "old_t_p_charge_added": False,
    }


def expected_charges() -> list[dict[str, str]]:
    return [
        {
            "charge_id": "kb-branch2-deep-rank-drop",
            "owner_id": "DEEP_MCA_RANK_DROP",
            "amount": str(T),
            "scope": "FIRST_MATCH_GLOBAL_ONCE",
            "source_binding_id": "pivot-certificate",
            "source_pointer": "/row/hankel_depth_t",
            "amount_source_role": "ROW_HANKEL_DEPTH_T",
            "owner_derivation_binding_ids": [
                "packet-note",
                "paper-d-v12",
                "exact-thresholds",
            ],
        }
    ]


def expected_ledger() -> dict[str, Any]:
    return {
        "U_paid_before": str(U_PAID_BEFORE),
        "rank_drop_charge": str(T),
        "pivot_failure_charge": "0",
        "branch2_charge": str(T),
        "U_paid_after": str(U_PAID_AFTER),
        "B_remaining_after": str(B_REMAINING_AFTER),
        "K_rem": K_REM,
        "rank_subgate_closed": True,
        "pivot_subgate_closed": True,
        "branch2_closed": True,
        "legacy_bridge_required": False,
        "ledger_consequence": True,
        "U_2": None,
        "U_Q": None,
        "U_A": None,
        "lhs": None,
        "row_complete": False,
        "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        "next_attack": "BRANCH3_TANGENT_COMMON_LINE_RESIDUE_PROJECTOR",
    }


def expected_audit_sections() -> dict[str, Any]:
    return {
        "parameter_dependence": (
            "RANK_BRIDGE_FIELD_UNIFORM_DEEP_GATE_PARAMETER_DEPENDENT_"
            "PRINTED_LEDGER_KOALABEAR_SPECIFIC"
        ),
        "layer_cake_dyadic_summability": "NOT_APPLICABLE",
        "moment_markov_chebyshev": "NOT_APPLICABLE",
        "numerical_evidence": (
            "EXACT_TOY_CONTROL_ONLY_DEPLOYED_RESULT_IS_SYMBOLIC"
        ),
        "edge_cases": EDGE_CASES,
        "remaining_risks": REMAINING_RISKS,
    }


@functools.cache
def exact_multiplier(budget: int) -> int:
    return (budget * P**R0) // math.comb(N, J)


def resolve_pointer(value: Any, pointer: str) -> Any:
    current = value
    for token in pointer.lstrip("/").split("/"):
        current = current[token.replace("~1", "/").replace("~0", "~")]
    return current


def validate_sources() -> None:
    paper_d = (ROOT / PAPER_D_REL).read_text(encoding="utf-8")
    for anchor in (
        r"\label{lem:support-locator-syndrome-recurrence}",
        r"\label{thm:deep-mca}",
        r"3r\ \le\ w-1",
        r"\emca(C,\delta)\ \le\ \frac{r+1}q",
    ):
        require(anchor in paper_d, f"Paper D anchor missing: {anchor}")

    thresholds = (ROOT / THRESHOLDS_REL).read_text(encoding="utf-8")
    for anchor in (
        r"\label{lem:exact-agreement-reduction}",
        r"\label{prop:universal-tangent-floor}",
        r"B_{C,\Gamma}^{\rm MCA}(a)",
        r"\min\{\abs\Gamma,n-a+1\}",
    ):
        require(anchor in thresholds, f"exact-threshold anchor missing: {anchor}")

    pivot = load_json(ROOT / PIVOT_CERT_REL)
    require(
        pivot["row"]["hankel_depth_t"] == T
        and pivot["row"]["co_support_size_j"] == J,
        "pivot predecessor row dimensions drift",
    )
    refinement = pivot["branch2_refinement"]
    require(
        refinement["pivot_failure_empty_after_branch1"] is True
        and refinement["pivot_failure_actual_witness_count"] == 0,
        "pivot predecessor no longer closes pivot failure",
    )
    require(
        refinement["rank_policy_complete"] is False
        and refinement["rank_drop_owner"] is None,
        "pivot predecessor rank policy unexpectedly changed",
    )

    first_match = load_json(ROOT / FIRST_MATCH_CERT_REL)
    require(
        [record["branch"] for record in first_match["first_match_branches"]]
        == [
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
        ],
        "v1 first-match branch order drift",
    )

    base = load_json(ROOT / BASE_CERT_REL)
    require(
        base["first_match"]["v2_order"] == V2_ORDER,
        "base-v2 first-match order drift",
    )
    require(
        int(base["arithmetic"]["new_U_paid"]) == U_PAID_BEFORE
        and int(base["arithmetic"]["B_rem"]) == B_STAR - U_PAID_BEFORE
        and base["arithmetic"]["K_rem"] == K_REM,
        "base-v2 paid baseline drift",
    )
    require(
        base["theorem"]["requires_affine_row_adapter"] is False
        and base["first_match"][
            "old_generated_collision_owner_retained_as_optional_refinement"
        ]
        is True
        and base["arithmetic"]["old_charge_is_replaced_not_added"] is True,
        "base-v2 legacy-retirement rationale drift",
    )
    require(
        base["arithmetic"]["U_Q"] is None
        and base["arithmetic"]["U_A"] is None,
        "base-v2 null open terms drift",
    )

    post_c5 = load_json(ROOT / POST_C5_CERT_REL)
    records = post_c5["mask_inventory"]["records"]
    require(
        records[2]["order"] == 3
        and records[2]["branch"] == "tangent_common_line_residue"
        and records[2]["actual_slope_projector_complete"] is False,
        "post-C5 branch-3 open status drift",
    )

    require(
        3 * R0 <= R,
        "deployed deep-MCA gate failed",
    )
    require(
        A_DEEP == N - T + 1,
        "deep agreement off-by-one",
    )
    require(
        exact_multiplier(B_REMAINING_AFTER) == K_REM,
        "exact K_rem drift",
    )


def build_certificate() -> dict[str, Any]:
    validate_sources()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "row": expected_row(),
        "rank_drop_policy": expected_rank_drop_policy(),
        "exact_support_rank_bridge": expected_exact_support_rank_bridge(),
        "deep_witness_lift": expected_deep_witness_lift(),
        "deep_mca_owner": expected_deep_mca_owner(),
        "branch2_first_match": expected_branch2_first_match(),
        "legacy_bridge_retirement": expected_legacy_bridge_retirement(),
        "small_field_control": build_small_field_control(),
        "charges": expected_charges(),
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


def validate_source_bindings(bindings: Any) -> dict[str, Any]:
    require(type(bindings) is list, "source_bindings is not a list")
    require(
        canonical_bytes(bindings)
        == canonical_bytes(expected_source_bindings()),
        "source binding path/hash/role drift",
    )
    ids: set[str] = set()
    loaded: dict[str, Any] = {}
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
        require(source_id not in ids, "duplicate source binding id")
        ids.add(source_id)
        path = Path(source["path"])
        require(
            not path.is_absolute() and ".." not in path.parts,
            "unsafe source path",
        )
        require(
            source["sha256"] == file_hash(path),
            f"source hash drift: {path}",
        )
        if path.suffix == ".json":
            loaded[source_id] = load_json(ROOT / path)
    return loaded


def validate_certificate(
    cert: dict[str, Any], *, exact_rebuild: bool = False
) -> None:
    require_exact_keys(cert, TOP_KEYS, "top-level")
    require(cert["schema"] == SCHEMA, "schema drift")
    require(cert["artifact_kind"] == ARTIFACT_KIND, "artifact kind drift")
    require(cert["status"] == STATUS, "status drift")
    require(
        cert["payload_sha256"] == payload_hash(cert),
        "payload hash drift",
    )

    loaded = validate_source_bindings(cert["source_bindings"])
    expected_sections = {
        "row": expected_row(),
        "rank_drop_policy": expected_rank_drop_policy(),
        "exact_support_rank_bridge": expected_exact_support_rank_bridge(),
        "deep_witness_lift": expected_deep_witness_lift(),
        "deep_mca_owner": expected_deep_mca_owner(),
        "branch2_first_match": expected_branch2_first_match(),
        "legacy_bridge_retirement": expected_legacy_bridge_retirement(),
        "small_field_control": build_small_field_control(),
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
    }
    for label, expected in expected_sections.items():
        require(type(cert[label]) is dict, f"{label} is not an object")
        require(
            canonical_bytes(cert[label]) == canonical_bytes(expected),
            f"{label} payload or JSON type drift",
        )

    row = cert["row"]
    for key in (
        "p",
        "ambient_extension_degree",
        "n",
        "k",
        "agreement_A",
        "redundancy_R",
        "co_support_size_j",
        "hankel_depth_t",
        "r0",
        "deep_agreement",
        "locator_coordinate_count",
        "three_r0",
        "deep_gate_rhs_n_minus_k",
    ):
        require_int(row[key], f"row.{key}")
    require(row["three_r0"] <= row["deep_gate_rhs_n_minus_k"], "deep gate false")

    policy = cert["rank_drop_policy"]
    require_int(policy["branch_number"], "rank_drop_policy.branch_number")
    require_int(policy["rank_threshold"], "rank_drop_policy.rank_threshold")
    require(
        policy["requires_actual_bad_incidence"] is True
        and policy["raw_algebraic_rank_drop_paid"] is False
        and policy["literal_first_match_residual_subset_of_envelope"] is True,
        "incidence scope drift",
    )
    require(
        policy["rank_field"] == "AMBIENT_F"
        and policy["rank_threshold"] == T
        and policy["failure_of_full_row_rank"] is True
        and policy["overdetermined_rank_less_than_j_plus_1_used"] is False
        and policy["scalar_stack_rank_used"] is False,
        "rank policy drift",
    )

    bridge = cert["exact_support_rank_bridge"]
    for key in (
        "exact_witness_support_size",
        "chosen_co_support_size",
        "actual_error_weight_upper_bound_before_rank",
        "rank_drop_error_weight_cap",
    ):
        require_int(bridge[key], f"exact_support_rank_bridge.{key}")
    require(
        bridge["rank_drop_error_weight_cap"] == R0
        and bridge["zero_amplitude_padding_excluded"] is True
        and bridge["rank_identity"]
        == "rank_F(M_A(gamma))=min(t,|E_gamma|)",
        "rank-to-weight bridge drift",
    )

    lift = cert["deep_witness_lift"]
    require_int(lift["r0"], "deep_witness_lift.r0")
    require_int(
        lift["deep_agreement"], "deep_witness_lift.deep_agreement"
    )
    require_int(
        lift["full_agreement_size_lower_bound"],
        "deep_witness_lift.full_agreement_size_lower_bound",
    )
    require(
        lift["original_support_subset_of_full_agreement_support"] is True
        and lift["noncontainment_persists_upward"] is True
        and lift["rank_drop_slope_is_deep_mca_bad"] is True
        and lift["separate_tangent_bridge_required"] is False,
        "deep witness lift drift",
    )

    owner = cert["deep_mca_owner"]
    for key in (
        "deep_radius_error_count",
        "gate_lhs_three_r0",
        "gate_rhs_n_minus_k",
        "upper_bound",
        "sharpness_slopes",
    ):
        require_int(owner[key], f"deep_mca_owner.{key}")
    require(
        owner["gate_holds"] is True
        and owner["upper_bound"] == T
        and owner["scope"] == "FIRST_MATCH_GLOBAL_ONCE"
        and owner["per_support_charge"] is False
        and owner["per_pivot_charge"] is False
        and owner["charge_sharp"] is True,
        "deep owner charge drift",
    )

    branch2 = cert["branch2_first_match"]
    require_int(
        branch2["branch_index_one_based"],
        "branch2_first_match.branch_index_one_based",
    )
    require_int(
        branch2["full_row_rank_pivot_success_survives_to_branch"],
        "branch2_first_match.full_row_rank_pivot_success_survives_to_branch",
    )
    require(
        branch2["branch2_local_policy_complete"] is True
        and branch2["pivot_failure_charge"] == "0"
        and branch2["later_branches_restricted_to_branch2_complement"] is True
        and branch2["rank_drop_envelope_bound_used"] is True
        and branch2["literal_rank_drop_cell_subset_of_envelope"] is True
        and branch2["branch1_projector_complete"] is False
        and branch2["global_mask_replay_complete"] is False
        and branch2["branches_3_to_5_complete"] is False,
        "branch-2 first-match scope drift",
    )

    retirement = cert["legacy_bridge_retirement"]
    require(
        retirement["status"]
        == "RETIRED_NOT_REQUIRED_FOR_DEPLOYED_BRANCH2"
        and retirement["identification_proved"] is False
        and retirement["equivalence_claimed"] is False
        and retirement["global_invalidity_claimed"] is False
        and retirement[
            "cyclotomic_lift_required_for_current_branch2_charge"
        ]
        is False
        and retirement["old_generated_collision_owner_optional_refinement"]
        is True
        and retirement["old_t_p_charge_added"] is False,
        "legacy bridge retirement drift",
    )

    control = cert["small_field_control"]
    for key in (
        "p",
        "n",
        "k",
        "agreement_A",
        "redundancy_R",
        "co_support_size_j",
        "hankel_depth_t",
        "r0",
        "deep_agreement",
        "branch2_count",
        "designed_slope",
        "original_supports_per_slope",
        "deep_supports_per_slope",
        "all_slopes_scanned",
    ):
        require_int(control[key], f"small_field_control.{key}")
    require(
        control["branch2_count"] == control["hankel_depth_t"] == 3
        and control["factorization_exact"] is True
        and control["rank_equals_min_t_actual_error_weight"] is True
        and control["full_agreement_lift_checked"] is True
        and control["sharp_charge_realized"] is True
        and control["raw_rank_drop_requires_actual_bad_incidence"] is True,
        "small-field load-bearing control drift",
    )

    charges = cert["charges"]
    require(type(charges) is list, "charges is not a list")
    require(
        canonical_bytes(charges) == canonical_bytes(expected_charges()),
        "charge spec or JSON type drift",
    )
    require(len(charges) == 1, "unexpected charge count")
    charge = charges[0]
    require_exact_keys(
        charge,
        {
            "charge_id",
            "owner_id",
            "amount",
            "scope",
            "source_binding_id",
            "source_pointer",
            "amount_source_role",
            "owner_derivation_binding_ids",
        },
        "charge",
    )
    source_value = resolve_pointer(
        loaded[charge["source_binding_id"]], charge["source_pointer"]
    )
    require(
        type(source_value) is int
        and int(charge["amount"]) == source_value == T,
        "charge amount/source pointer drift",
    )
    binding_ids = {
        source["binding_id"] for source in cert["source_bindings"]
    }
    require(
        charge["amount_source_role"] == "ROW_HANKEL_DEPTH_T"
        and type(charge["owner_derivation_binding_ids"]) is list
        and set(charge["owner_derivation_binding_ids"])
        == {"packet-note", "paper-d-v12", "exact-thresholds"}
        and set(charge["owner_derivation_binding_ids"]) <= binding_ids,
        "charge provenance drift",
    )

    ledger = cert["ledger"]
    require_int(ledger["K_rem"], "ledger.K_rem")
    require(
        int(ledger["U_paid_before"]) + int(ledger["branch2_charge"])
        == int(ledger["U_paid_after"]),
        "paid charge sum drift",
    )
    require(
        int(ledger["B_remaining_after"])
        == B_STAR - int(ledger["U_paid_after"]),
        "remaining budget drift",
    )
    require(
        ledger["K_rem"] == exact_multiplier(B_REMAINING_AFTER),
        "exact K_rem replay drift",
    )
    require(
        ledger["rank_subgate_closed"] is True
        and ledger["pivot_subgate_closed"] is True
        and ledger["branch2_closed"] is True
        and ledger["legacy_bridge_required"] is False
        and ledger["ledger_consequence"] is True
        and ledger["U_2"] is None
        and ledger["U_Q"] is None
        and ledger["U_A"] is None
        and ledger["lhs"] is None
        and ledger["row_complete"] is False
        and ledger["inequality_status"] == "UNDECIDED_OPEN_COMPONENTS",
        "ledger closure/open-term drift",
    )

    audit = cert["audit_sections"]
    require(audit["edge_cases"] == EDGE_CASES, "edge cases drift")
    require(
        audit["remaining_risks"] == REMAINING_RISKS,
        "remaining risks drift",
    )
    require(cert["nonclaims"] == NONCLAIMS, "nonclaims drift")

    validate_sources()
    if exact_rebuild:
        require(
            canonical_bytes(cert) == canonical_bytes(build_certificate()),
            "deterministic certificate rebuild drift",
        )


def rehash(cert: dict[str, Any]) -> None:
    cert["payload_sha256"] = payload_hash(cert)


def set_path(
    value: dict[str, Any], path: tuple[Any, ...], replacement: Any
) -> None:
    target: Any = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def expect_reject(
    name: str,
    candidate: dict[str, Any],
    cases: list[tuple[str, bool]],
) -> None:
    try:
        validate_certificate(candidate)
    except (VerificationError, KeyError, TypeError, ValueError):
        cases.append((name, True))
        return
    cases.append((name, False))


def run_tamper_selftest(cert: dict[str, Any]) -> int:
    cases: list[tuple[str, bool]] = []

    def mutate(
        name: str,
        path: tuple[Any, ...],
        replacement: Any,
        *,
        hash_it: bool = True,
    ) -> None:
        candidate = copy.deepcopy(cert)
        set_path(candidate, path, replacement)
        if hash_it:
            rehash(candidate)
        expect_reject(name, candidate, cases)

    mutate("row-t-off-by-one", ("row", "hankel_depth_t"), T - 1)
    mutate("row-r0-off-by-one", ("row", "r0"), R0 + 1)
    mutate("deep-agreement-n-minus-t", ("row", "deep_agreement"), N - T)
    mutate("three-r0-drift", ("row", "three_r0"), 3 * R0 + 1)
    mutate(
        "matrix-shape-drift",
        ("row", "ambient_hankel_shape"),
        [T, LOCATOR_COORDS - 1],
    )
    mutate(
        "raw-rank-drop-paid",
        ("rank_drop_policy", "raw_algebraic_rank_drop_paid"),
        True,
    )
    mutate(
        "actual-incidence-erased",
        ("rank_drop_policy", "requires_actual_bad_incidence"),
        False,
    )
    mutate(
        "first-match-envelope-subset-erased",
        (
            "rank_drop_policy",
            "literal_first_match_residual_subset_of_envelope",
        ),
        False,
    )
    mutate(
        "rank-field-scalarized",
        ("rank_drop_policy", "rank_field"),
        "SCALAR_STACK_K",
    )
    mutate(
        "rank-threshold-j-plus-one",
        ("rank_drop_policy", "rank_threshold"),
        LOCATOR_COORDS,
    )
    mutate(
        "rank-predicate-j-plus-one",
        ("rank_drop_policy", "rank_predicate"),
        "rank_F(M_A(gamma))<j+1",
    )
    mutate(
        "scalar-stack-used",
        ("rank_drop_policy", "scalar_stack_rank_used"),
        True,
    )
    mutate(
        "support-selector-introduced",
        ("rank_drop_policy", "support_selector_used"),
        True,
    )
    mutate(
        "infinity-added",
        ("rank_drop_policy", "infinity_included"),
        True,
    )
    mutate(
        "charge-owner-derivation-erased",
        ("charges", 0, "owner_derivation_binding_ids"),
        ["pivot-certificate"],
    )
    mutate(
        "exact-support-size-drift",
        ("exact_support_rank_bridge", "exact_witness_support_size"),
        A + 1,
    )
    mutate(
        "actual-support-equals-padded",
        (
            "exact_support_rank_bridge",
            "actual_error_support",
        ),
        "E_gamma=D_MINUS_S",
    )
    mutate(
        "padding-included",
        (
            "exact_support_rank_bridge",
            "zero_amplitude_padding_excluded",
        ),
        False,
    )
    mutate(
        "zero-weights-allowed",
        ("exact_support_rank_bridge", "nonzero_weight_formula"),
        "w_x=lambda_x*e_gamma(x)_MAY_BE_ZERO",
    )
    mutate(
        "rank-forced-t",
        ("exact_support_rank_bridge", "rank_identity"),
        "rank_F(M_A(gamma))=t",
    )
    mutate(
        "rank-cap-t-not-t-minus-one",
        (
            "exact_support_rank_bridge",
            "rank_drop_error_weight_cap",
        ),
        T,
    )
    mutate(
        "full-support-not-enlarged",
        (
            "deep_witness_lift",
            "original_support_subset_of_full_agreement_support",
        ),
        False,
    )
    mutate(
        "noncontainment-not-preserved",
        ("deep_witness_lift", "noncontainment_persists_upward"),
        False,
    )
    mutate(
        "deep-mca-lift-erased",
        ("deep_witness_lift", "rank_drop_slope_is_deep_mca_bad"),
        False,
    )
    mutate(
        "unneeded-tangent-bridge",
        ("deep_witness_lift", "separate_tangent_bridge_required"),
        True,
    )
    mutate(
        "deep-off-by-one-text",
        ("deep_witness_lift", "off_by_one_guard"),
        "n-t",
    )
    mutate(
        "deep-gate-false",
        ("deep_mca_owner", "gate_holds"),
        False,
    )
    mutate(
        "deep-upper-t-minus-one",
        ("deep_mca_owner", "upper_bound"),
        T - 1,
    )
    mutate(
        "deep-charge-per-support",
        ("deep_mca_owner", "per_support_charge"),
        True,
    )
    mutate(
        "deep-charge-per-pivot",
        ("deep_mca_owner", "per_pivot_charge"),
        True,
    )
    mutate(
        "sharpness-erased",
        ("deep_mca_owner", "charge_sharp"),
        False,
    )
    mutate(
        "sharpness-t-minus-one",
        ("deep_mca_owner", "sharpness_slopes"),
        T - 1,
    )
    mutate(
        "owner-order-drift",
        ("branch2_first_match", "v2_order"),
        [V2_ORDER[1], V2_ORDER[0], *V2_ORDER[2:]],
    )
    mutate(
        "wrong-branch-index",
        ("branch2_first_match", "branch_index_one_based"),
        3,
    )
    mutate(
        "pivot-failure-reopened",
        (
            "branch2_first_match",
            "pivot_failure_empty_imported_from_predecessor",
        ),
        False,
    )
    mutate(
        "pivot-charge-one",
        ("branch2_first_match", "pivot_failure_charge"),
        "1",
    )
    mutate(
        "full-rank-paid-in-branch2",
        (
            "branch2_first_match",
            "full_row_rank_pivot_success_survives_to_branch",
        ),
        2,
    )
    mutate(
        "later-complement-erased",
        (
            "branch2_first_match",
            "later_branches_restricted_to_branch2_complement",
        ),
        False,
    )
    mutate(
        "branch1-falsely-complete",
        ("branch2_first_match", "branch1_projector_complete"),
        True,
    )
    mutate(
        "global-mask-falsely-complete",
        ("branch2_first_match", "global_mask_replay_complete"),
        True,
    )
    mutate(
        "later-branches-falsely-complete",
        ("branch2_first_match", "branches_3_to_5_complete"),
        True,
    )
    mutate(
        "legacy-identification-invented",
        ("legacy_bridge_retirement", "identification_proved"),
        True,
    )
    mutate(
        "legacy-equivalence-invented",
        ("legacy_bridge_retirement", "equivalence_claimed"),
        True,
    )
    mutate(
        "legacy-retirement-globalized",
        ("legacy_bridge_retirement", "scope"),
        "GLOBAL_ALL_LEDGERS",
    )
    mutate(
        "optional-refinement-invalidated",
        (
            "legacy_bridge_retirement",
            "old_generated_collision_owner_optional_refinement",
        ),
        False,
    )
    mutate(
        "old-tp-added",
        ("legacy_bridge_retirement", "old_t_p_charge_added"),
        True,
    )
    mutate(
        "control-branch2-count-drift",
        ("small_field_control", "branch2_count"),
        2,
    )
    mutate(
        "control-padding-erased",
        ("small_field_control", "designed_padded_zero_points"),
        [],
    )
    mutate(
        "control-factorization-false",
        ("small_field_control", "factorization_exact"),
        False,
    )
    mutate(
        "control-contained-bad",
        ("small_field_control", "contained_bad_slopes"),
        [0],
    )
    mutate(
        "control-incidence-scope-erased",
        (
            "small_field_control",
            "raw_rank_drop_requires_actual_bad_incidence",
        ),
        False,
    )
    mutate(
        "charge-t-minus-one",
        ("charges", 0, "amount"),
        str(T - 1),
    )
    mutate(
        "charge-per-chart",
        ("charges", 0, "scope"),
        "PER_CHART",
    )
    mutate(
        "charge-source-pointer-alias",
        ("charges", 0, "source_pointer"),
        "/row/co_support_size_j",
    )
    mutate(
        "ledger-add-old-tp",
        ("ledger", "U_paid_after"),
        str(U_PAID_AFTER + T * P),
    )
    mutate(
        "ledger-B-rem-drift",
        ("ledger", "B_remaining_after"),
        str(B_REMAINING_AFTER - 1),
    )
    mutate("ledger-K-rem-drift", ("ledger", "K_rem"), K_REM - 1)
    mutate(
        "rank-subgate-reopened",
        ("ledger", "rank_subgate_closed"),
        False,
    )
    mutate(
        "branch2-reopened",
        ("ledger", "branch2_closed"),
        False,
    )
    mutate(
        "legacy-required-again",
        ("ledger", "legacy_bridge_required"),
        True,
    )
    mutate("U2-null-to-zero", ("ledger", "U_2"), 0)
    mutate("UQ-null-to-zero", ("ledger", "U_Q"), 0)
    mutate("UA-null-to-zero", ("ledger", "U_A"), 0)
    mutate("row-falsely-complete", ("ledger", "row_complete"), True)
    mutate(
        "inequality-falsely-decided",
        ("ledger", "inequality_status"),
        "PROVED_PASS",
    )
    mutate(
        "source-hash-drift",
        ("source_bindings", 0, "sha256"),
        "0" * 64,
    )
    mutate(
        "source-role-drift",
        ("source_bindings", 0, "role"),
        "unrelated role",
    )
    mutate(
        "edge-cases-erased",
        ("audit_sections", "edge_cases"),
        ["none"],
    )
    mutate(
        "remaining-risks-erased",
        ("audit_sections", "remaining_risks"),
        ["none"],
    )
    mutate("nonclaims-erased", ("nonclaims",), ["none"])

    unknown_nested = copy.deepcopy(cert)
    unknown_nested["rank_drop_policy"]["unknown"] = True
    rehash(unknown_nested)
    expect_reject("unknown-nested-key", unknown_nested, cases)

    unknown_top = copy.deepcopy(cert)
    unknown_top["unknown"] = True
    rehash(unknown_top)
    expect_reject("unknown-top-key", unknown_top, cases)

    bad_payload = copy.deepcopy(cert)
    bad_payload["payload_sha256"] = "0" * 64
    expect_reject("payload-hash", bad_payload, cases)

    bad_bool = copy.deepcopy(cert)
    bad_bool["ledger"]["branch2_closed"] = 1
    rehash(bad_bool)
    expect_reject("integer-as-bool", bad_bool, cases)

    for name, raw in (
        ("duplicate-json-key", '{"schema":"a","schema":"b"}'),
        ("nan-json-token", '{"value":NaN}'),
    ):
        try:
            parse_json(raw, name)
        except (VerificationError, ValueError):
            cases.append((name, True))
        else:
            cases.append((name, False))

    failed = [name for name, passed in cases if not passed]
    require(not failed, f"mutations not rejected: {failed}")
    return len(cases)


def write_artifact() -> None:
    artifact = build_certificate()
    validate_certificate(artifact)
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {CERT_PATH.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.write:
        write_artifact()
        return 0

    cert = load_json(CERT_PATH)
    validate_certificate(cert, exact_rebuild=True)
    if args.tamper_selftest:
        count = run_tamper_selftest(cert)
        print(
            "M1_KB_BRANCH2_RANK_DEEP_OWNER_V1_TAMPER_PASS "
            f"rejected={count}/{count}"
        )
    else:
        print("M1_KB_BRANCH2_RANK_DEEP_OWNER_V1_VERIFY_PASS")
        print(
            "rank policy: actual bad slopes with ambient rank < "
            f"{T} lift to agreement {A_DEEP}"
        )
        print(
            "owner: DEEP_MCA_RANK_DROP; global distinct-slope charge "
            f"{RANK_DROP_CHARGE} (sharp)"
        )
        print(
            "ledger: U_paid=%d; B_remaining=%d; K_rem=%d"
            % (U_PAID_AFTER, B_REMAINING_AFTER, K_REM)
        )
        print(
            "open: branch 3 onward and U_2/U_Q/U_A; row undecided"
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
