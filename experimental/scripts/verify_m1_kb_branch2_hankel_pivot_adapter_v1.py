#!/usr/bin/env python3
"""Verify the KoalaBear M1 branch-2 Hankel pivot adapter.

This packet makes only the field-native finite-pivot subgate executable.  It
does not define the rank owner, identify the Hankel pivot with the older
cyclotomic O-valued row packet, or assign a ledger charge.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-branch2-hankel-pivot-adapter-v1"
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch2-hankel-pivot-adapter-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch2_hankel_pivot_adapter_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch2_hankel_pivot_adapter_v1.md"
)
VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.sage"
)
PAPER_D_REL = Path("tex/cs25_cap_v12.tex")
KB_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
)
KB_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/"
    "kb_mca_1116048_first_match_ledger_v1.json"
)
POST_C5_NOTE_REL = Path(
    "experimental/notes/m1/m1_fp2_post_c5_mask_incidence_v1.md"
)
POST_C5_CERT_REL = Path(
    "experimental/data/certificates/m1-fp2-post-c5-mask-incidence-v1/"
    "m1_fp2_post_c5_mask_incidence_v1.json"
)
POST_C5_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py"
)
PREDECESSOR_NOTE_REL = Path(
    "experimental/notes/m1/m1_fp2_residual_route_cut_v1.md"
)
PREDECESSOR_CERT_REL = Path(
    "experimental/data/certificates/m1-fp2-residual-route-cut-v1/"
    "m1_fp2_residual_route_cut_v1.json"
)
COORDINATE_TRANSFER_REL = Path(
    "experimental/notes/f1/f1_extension_coordinate_transfer.md"
)
EXTRACTOR_REL = Path(
    "experimental/scripts/extract_regular_hankel_minors.py"
)
BASE_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2/"
    "kb_mca_1116048_base_slope_universe_v2.json"
)

P = 2_130_706_433
N = 2_097_152
K_DIM = 1_048_576
A = 1_116_048
R = N - K_DIM
J = N - A
T = A - K_DIM
LOCATOR_COORDS = J + 1
KERNEL_LOWER = LOCATOR_COORDS - T
MATRIX_ENTRY_COUNT = T * LOCATOR_COORDS
SCALARIZED_ROWS = 3 * T
SCALARIZED_KERNEL_LOWER = LOCATOR_COORDS - SCALARIZED_ROWS
B_STAR = P**6 // (1 << 128)
U_PAID = 2_602_153_473
B_REMAINING = B_STAR - U_PAID
STATUS = (
    "PROVED_PAPER_D_IMPLICIT_FINITE_PIVOT_ADAPTER_"
    "PIVOT_FAILURE_EMPTY_RANK_POLICY_AND_LEGACY_BRIDGE_OPEN_"
    "NO_LEDGER_EFFECT"
)

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "row",
    "paper_d_adapter",
    "branch2_refinement",
    "scalarization_replay",
    "prime_field_control",
    "two_root_control",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}


class VerificationError(RuntimeError):
    """A parser, source-binding, arithmetic, or semantic check failed."""


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


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON: {path}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=lambda token: (_ for _ in ()).throw(
            VerificationError(f"non-finite JSON token: {token}")
        ),
    )
    require(type(value) is dict, f"top-level JSON is not an object: {path}")
    return value


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


def file_hash(relative_path: Path) -> str:
    path = ROOT / relative_path
    require(path.is_file(), f"missing source binding: {relative_path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(
    binding_id: str, relative_path: Path, role: str
) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative_path.as_posix(),
        "sha256": file_hash(relative_path),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("packet-note", NOTE_REL, "human-readable proof audit"),
        source_binding(
            "python-verifier",
            VERIFIER_REL,
            "deterministic builder and mutation verifier",
        ),
        source_binding(
            "sage-control",
            SAGE_REL,
            "two-root exact control and scalarization rank guardrails",
        ),
        source_binding(
            "paper-d-v12",
            PAPER_D_REL,
            "authoritative syndrome locator and exact support-image theorem",
        ),
        source_binding(
            "kb-first-match-note",
            KB_NOTE_REL,
            "frozen branch order and legacy cyclotomic row packet",
        ),
        source_binding(
            "kb-first-match-certificate",
            KB_CERT_REL,
            "machine-readable branch-2 open status",
        ),
        source_binding(
            "post-c5-note",
            POST_C5_NOTE_REL,
            "predecessor mask inventory and quadratic residual",
        ),
        source_binding(
            "post-c5-certificate",
            POST_C5_CERT_REL,
            "machine-readable predecessor route cut",
        ),
        source_binding(
            "post-c5-verifier",
            POST_C5_VERIFIER_REL,
            "predecessor semantic replay",
        ),
        source_binding(
            "quadratic-route-cut-note",
            PREDECESSOR_NOTE_REL,
            "exact F over K restriction and fixed-support incidence",
        ),
        source_binding(
            "quadratic-route-cut-certificate",
            PREDECESSOR_CERT_REL,
            "machine-readable scalarization contract",
        ),
        source_binding(
            "coordinate-transfer",
            COORDINATE_TRANSFER_REL,
            "support-wise restriction of scalars",
        ),
        source_binding(
            "hankel-extractor",
            EXTRACTOR_REL,
            "existing locator and Hankel recurrence helpers",
        ),
        source_binding(
            "base-ledger",
            BASE_CERT_REL,
            "current paid baseline and null open terms",
        ),
    ]


def mod_inverse(value: int, prime: int) -> int:
    value %= prime
    require(value != 0, "attempted inversion of zero")
    return pow(value, -1, prime)


def polynomial_multiply(
    left: list[int], right: list[int], prime: int
) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            out[i + j] = (
                out[i + j] + left_value * right_value
            ) % prime
    return out


def locator_coefficients(
    roots: list[int] | tuple[int, ...], prime: int
) -> list[int]:
    """Return coefficients low-to-high for prod(X-root)."""
    coefficients = [1]
    for root in roots:
        coefficients = polynomial_multiply(
            coefficients, [(-root) % prime, 1], prime
        )
    return coefficients


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
    require(len(word) == len(domain) == len(weights), "syndrome length mismatch")
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


def hankel_times_locator(
    syndrome_vector: list[int],
    depth: int,
    locator: list[int],
    prime: int,
) -> list[int]:
    j = len(locator) - 1
    require(
        len(syndrome_vector) >= depth + j,
        "syndrome window too short",
    )
    return [
        sum(
            syndrome_vector[row + column] * locator[column]
            for column in range(j + 1)
        )
        % prime
        for row in range(depth)
    ]


def solve_square_mod(
    matrix: list[list[int]], vector: list[int], prime: int
) -> list[int]:
    n = len(matrix)
    require(n > 0 and len(vector) == n, "bad square solve dimensions")
    require(all(len(row) == n for row in matrix), "matrix not square")
    work = [
        [value % prime for value in row] + [vector[index] % prime]
        for index, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(
            (
                row
                for row in range(column, n)
                if work[row][column] % prime
            ),
            None,
        )
        require(pivot is not None, "singular interpolation matrix")
        work[column], work[pivot] = work[pivot], work[column]
        inverse = mod_inverse(work[column][column], prime)
        work[column] = [
            value * inverse % prime for value in work[column]
        ]
        for row in range(n):
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (work[row][entry] - factor * work[column][entry])
                    % prime
                    for entry in range(n + 1)
                ]
    return [work[row][-1] for row in range(n)]


def evaluate_polynomial(
    coefficients: list[int], point: int, prime: int
) -> int:
    total = 0
    power = 1
    for coefficient in coefficients:
        total = (total + coefficient * power) % prime
        power = power * point % prime
    return total


def explained_on(
    word: list[int],
    support: tuple[int, ...],
    domain: list[int],
    dimension: int,
    prime: int,
) -> bool:
    require(len(support) >= dimension, "support smaller than dimension")
    interpolation_indices = support[:dimension]
    matrix = [
        [
            pow(domain[index], degree, prime)
            for degree in range(dimension)
        ]
        for index in interpolation_indices
    ]
    coefficients = solve_square_mod(
        matrix,
        [word[index] for index in interpolation_indices],
        prime,
    )
    return all(
        evaluate_polynomial(coefficients, domain[index], prime)
        == word[index] % prime
        for index in support
    )


def first_nonzero(values: list[int]) -> int | None:
    return next((index for index, value in enumerate(values) if value), None)


def build_prime_field_control() -> dict[str, Any]:
    prime = 17
    domain = list(range(6))
    n = len(domain)
    dimension = 2
    agreement = 4
    redundancy = n - dimension
    co_support_size = n - agreement
    depth = agreement - dimension
    designed_support = (0, 1, 2, 3)
    designed_co_support = (4, 5)
    designed_slope = 3

    g = [point * point % prime for point in domain]
    f = [(-designed_slope * value) % prime for value in g]

    weights = dual_weights(domain, prime)
    u = syndrome(f, domain, weights, redundancy, prime)
    v = syndrome(g, domain, weights, redundancy, prime)
    records: list[dict[str, Any]] = []
    recurrence_checks = 0
    direct_checks = 0
    contained_incidence_checks = 0

    for agreement_support in combinations(range(n), agreement):
        support_set = set(agreement_support)
        co_support = tuple(
            index for index in range(n) if index not in support_set
        )
        locator = locator_coefficients(
            [domain[index] for index in co_support], prime
        )
        a_vector = hankel_times_locator(u, depth, locator, prime)
        b_vector = hankel_times_locator(v, depth, locator, prime)
        pivot = first_nonzero(b_vector)

        for slope in range(prime):
            word = [
                (f[index] + slope * g[index]) % prime
                for index in range(n)
            ]
            direct_explained = explained_on(
                word, agreement_support, domain, dimension, prime
            )
            jointly_explained = explained_on(
                f, agreement_support, domain, dimension, prime
            ) and explained_on(
                g, agreement_support, domain, dimension, prime
            )
            direct_bad = direct_explained and not jointly_explained
            incidence = all(
                (a_value + slope * b_value) % prime == 0
                for a_value, b_value in zip(a_vector, b_vector)
            )
            recurrence_bad = incidence and pivot is not None
            require(
                direct_bad == recurrence_bad,
                "direct interpolation and Hankel adapter disagree",
            )
            direct_checks += 1
            recurrence_checks += 1

            if incidence and pivot is None:
                require(
                    all(value == 0 for value in a_vector),
                    "B=0 incidence did not force A=0",
                )
                require(
                    jointly_explained,
                    "B=0 incidence was not jointly contained",
                )
                contained_incidence_checks += 1

            if recurrence_bad:
                require(pivot is not None, "missing pivot on bad incidence")
                require(
                    all(value == 0 for value in b_vector[:pivot]),
                    "pivot is not the first nonzero coordinate",
                )
                require(b_vector[pivot] != 0, "pivot coordinate vanished")
                recovered = (
                    -a_vector[pivot]
                    * mod_inverse(b_vector[pivot], prime)
                ) % prime
                require(recovered == slope, "pivot slope recovery failed")
                require(
                    all(
                        (
                            a_vector[row] * b_vector[pivot]
                            - a_vector[pivot] * b_vector[row]
                        )
                        % prime
                        == 0
                        for row in range(depth)
                    ),
                    "cross equations failed",
                )
                records.append(
                    {
                        "slope": slope,
                        "agreement_support_indices": list(agreement_support),
                        "co_support_indices": list(co_support),
                        "co_support_domain_points": [
                            domain[index] for index in co_support
                        ],
                        "locator_coefficients_low_to_high": locator,
                        "A_Han": a_vector,
                        "B_Han": b_vector,
                        "least_pivot_h": pivot,
                    }
                )

    require(
        any(
            record["slope"] == designed_slope
            and record["agreement_support_indices"]
            == list(designed_support)
            and record["co_support_indices"] == list(designed_co_support)
            and record["locator_coefficients_low_to_high"] == [3, 8, 1]
            and record["A_Han"] == [0, 14]
            and record["B_Han"] == [0, 1]
            and record["least_pivot_h"] == 1
            for record in records
        ),
        "designed non-first-pivot bad incidence missing",
    )
    require(records, "prime-field control has no bad incidences")
    require(
        weights == [16, 5, 7, 10, 12, 1],
        "full-domain dual-weight convention drift",
    )
    require(
        sorted({record["slope"] for record in records})
        == [designed_slope],
        "prime control acquired an unintended bad slope",
    )

    contained_support = designed_support
    contained_co_support = designed_co_support
    contained_f = [(1 + 2 * point) % prime for point in domain]
    contained_g = [(4 + 3 * point) % prime for point in domain]
    contained_f[4] = (contained_f[4] + 5) % prime
    contained_f[5] = (contained_f[5] + 7) % prime
    contained_g[4] = (contained_g[4] + 6) % prime
    contained_g[5] = (contained_g[5] + 8) % prime
    contained_locator = locator_coefficients(
        [domain[index] for index in contained_co_support], prime
    )
    contained_a = hankel_times_locator(
        syndrome(contained_f, domain, weights, redundancy, prime),
        depth,
        contained_locator,
        prime,
    )
    contained_b = hankel_times_locator(
        syndrome(contained_g, domain, weights, redundancy, prime),
        depth,
        contained_locator,
        prime,
    )
    require(
        contained_a == [0, 0] and contained_b == [0, 0],
        "positive B=0 contained-incidence recurrence failed",
    )
    require(
        explained_on(
            contained_f,
            contained_support,
            domain,
            dimension,
            prime,
        )
        and explained_on(
            contained_g,
            contained_support,
            domain,
            dimension,
            prime,
        ),
        "positive B=0 control is not jointly contained",
    )
    contained_test_slope = 11
    require(
        explained_on(
            [
                (
                    contained_f[index]
                    + contained_test_slope * contained_g[index]
                )
                % prime
                for index in range(n)
            ],
            contained_support,
            domain,
            dimension,
            prime,
        ),
        "positive B=0 control lost affine incidence",
    )

    return {
        "status": "EXACT_FINITE_CONTROL_NOT_DEPLOYED_EVIDENCE",
        "p": prime,
        "n": n,
        "k": dimension,
        "agreement_A": agreement,
        "j": co_support_size,
        "t": depth,
        "domain": domain,
        "dual_weights": weights,
        "f": f,
        "g": g,
        "designed_bad_slope": designed_slope,
        "designed_agreement_support_indices": list(designed_support),
        "designed_co_support_indices": list(designed_co_support),
        "designed_locator_coefficients_low_to_high": [3, 8, 1],
        "designed_A_Han": [0, 14],
        "designed_B_Han": [0, 1],
        "designed_least_pivot_h": 1,
        "supports_enumerated": len(list(combinations(range(n), agreement))),
        "slopes_per_support": prime,
        "direct_checks": direct_checks,
        "recurrence_checks": recurrence_checks,
        "contained_incidence_checks": contained_incidence_checks,
        "bad_record_count": len(records),
        "distinct_bad_slopes": sorted(
            {record["slope"] for record in records}
        ),
        "records_sha256": canonical_hash(records),
        "all_bad_records_have_least_pivot": all(
            record["least_pivot_h"] is not None for record in records
        ),
        "non_first_pivot_exercised": any(
            record["least_pivot_h"] == 1 for record in records
        ),
        "B_zero_positive_control": {
            "agreement_support_indices": list(contained_support),
            "co_support_indices": list(contained_co_support),
            "locator_coefficients_low_to_high": contained_locator,
            "A_Han": contained_a,
            "B_Han": contained_b,
            "test_slope": contained_test_slope,
            "joint_containment_directly_checked": True,
            "affine_incidence_directly_checked": True,
        },
        "direct_interpolation_equals_hankel_adapter": True,
        "B_zero_incidence_implies_joint_containment": True,
    }


EDGE_CASES = [
    "S denotes the agreement support and T=D minus S denotes the co-support.",
    "Locator coefficients are ordered low-to-high and include the monic top coefficient.",
    "The syndrome uses the exact dual weights lambda_x.",
    "The ambient F-valued Hankel rows are canonical; scalarized K rows are only an equivalence replay.",
    "Under finite incidence, B_T=0 forces A_T=0 and therefore joint containment.",
    "The least nonzero B_T coordinate is a deterministic pivot but not a rank owner.",
    "The underdetermined Hankel matrix has a large kernel; kernel nonemptiness is not payment.",
    "Null is not zero.",
]

REMAINING_RISKS = [
    "The KoalaBear rank_drop policy and its paid owner remain unspecified.",
    "No theorem identifies the field-native Hankel pivot with the legacy O-valued cyclotomic B_0 row.",
    "Branches 3 through 5 still lack complete executable row-specific projectors.",
    "Field-full rank-two roots may vary across supports.",
    "The exact two-root control is not proved to survive the unresolved rank policy or branches 3 through 5.",
    "U_2, U_Q, and U_A remain open.",
]

NONCLAIMS = [
    "This packet does not complete KoalaBear branch 2.",
    "This packet does not define or pay a rank-drop owner.",
    "This packet does not identify B_Han with the legacy cyclotomic B_0.",
    "This packet does not bound the union of roots over supports.",
    "This packet does not claim the two-root control survives branches 2 through 5.",
    "This packet does not change the ledger or set U_2, U_Q, or U_A.",
    "This packet does not begin the degree-three parameter class.",
]


def build_certificate() -> dict[str, Any]:
    prime_control = build_prime_field_control()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": "M1_KB_BRANCH2_HANKEL_PIVOT_ADAPTER",
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "ambient_extension_degree": 6,
            "quadratic_parameter_extension_degree": 2,
            "n": N,
            "k": K_DIM,
            "agreement_A": A,
            "redundancy_r": R,
            "co_support_size_j": J,
            "hankel_depth_t": T,
            "locator_coordinate_count": LOCATOR_COORDS,
            "ambient_hankel_shape": [T, LOCATOR_COORDS],
            "ambient_hankel_entry_count": MATRIX_ENTRY_COUNT,
            "ambient_kernel_dimension_lower_bound": KERNEL_LOWER,
            "scalarized_row_count": SCALARIZED_ROWS,
            "scalarized_kernel_dimension_lower_bound": (
                SCALARIZED_KERNEL_LOWER
            ),
            "B_star": str(B_STAR),
            "U_paid": str(U_PAID),
            "B_remaining": str(B_REMAINING),
        },
        "paper_d_adapter": {
            "agreement_support_symbol": "S",
            "agreement_support_cardinality": A,
            "co_support_definition": "T=D_MINUS_S",
            "co_support_cardinality": J,
            "locator": "L_T(X)=prod_{x_in_T}(X-x)=sum_{b=0}^j ell_b X^b",
            "locator_coefficient_order": "LOW_TO_HIGH_WITH_MONIC_TOP",
            "locator_top_coefficient": 1,
            "dual_weight_formula": (
                "lambda_x=(prod_{y_in_D,y!=x}(x-y))^(-1)"
            ),
            "syndrome_formula": (
                "Syn(Y)_m=sum_{x_in_D} lambda_x*x^m*Y(x)"
            ),
            "syndrome_moment_range": "0<=m<r",
            "U_definition": "H_(t,j)(Syn_F(f))",
            "V_definition": "H_(t,j)(Syn_F(g))",
            "matrix_entry_formula": "H(w)[h,b]=w[h+b]",
            "matrix_materialization_required": False,
            "evaluation_mode": "IMPLICIT_TRUNCATED_CONVOLUTION",
            "A_Han_definition": "A_Han(T)=U*ell_T",
            "B_Han_definition": "B_Han(T)=V*ell_T",
            "quotient_map": "Phi_T^F(w)=H_(t,j)(w)*ell_T",
            "quotient_map_kernel": "W_T(F)",
            "quotient_map_isomorphism": "F^r/W_T(F)_TO_F^t",
            "finite_noncontained_equivalence": (
                "f+gamma*g_EXPLAINED_ON_S_AND_NOT_JOINTLY_CONTAINED"
                "_IFF_A_Han+gamma*B_Han=0_AND_B_Han!=0"
            ),
            "source_status": "IMPORTED_PROVED_PAPER_D_V12",
        },
        "branch2_refinement": {
            "predecessor_machine_status": "UNBOUND_SOURCE_SYMBOL",
            "corrected_pivot_status": "FIELD_NATIVE_HANKEL_PIVOT_DEFINED",
            "pivot_adapter_complete": True,
            "scope": (
                "ACTUAL_FINITE_SUPPORT_WISE_NONCONTAINED_INCIDENCE_"
                "AFTER_CONTAINED_AND_INCONSISTENT_CASES"
            ),
            "branch1_projector_complete": False,
            "rank_policy_status": "UNSPECIFIED",
            "legacy_O_lift_red_p_bridge_status": "UNPROVEN",
            "least_pivot_rule": "h_star=MIN_h_WITH_B_Han(T)[h]!=0",
            "earlier_pivot_equations": "B_Han(T)[h]=0_FOR_h<h_star",
            "pivot_inequation": "B_Han(T)[h_star]!=0",
            "cross_equations": (
                "A_Han(T)[m]*B_Han(T)[h_star]"
                "-A_Han(T)[h_star]*B_Han(T)[m]=0_FOR_ALL_m"
            ),
            "slope_formula": (
                "gamma=-A_Han(T)[h_star]/B_Han(T)[h_star]"
            ),
            "pivot_labels": T,
            "pivot_labels_are_hankel_rows_not_supports": True,
            "pivot_failure_empty_after_branch1": True,
            "pivot_failure_actual_witness_count": 0,
            "reason_pivot_failure_empty": (
                "FINITE_NONCONTAINED_INCIDENCE_REQUIRES_B_Han_NOT_ZERO"
            ),
            "rank_policy_complete": False,
            "deployed_rank_drop_predicate_complete": False,
            "rank_drop_owner": None,
            "rank_drop_charge": None,
            "legacy_red_p_bridge": False,
            "legacy_paper_d_symbol": "B_Han(T)[h]",
            "legacy_kb_symbol": "red_p(B_0(S))",
            "legacy_identification_proved": False,
            "cyclotomic_lift_map": None,
            "branch2_complete": False,
            "paid_owner": None,
            "charge": None,
        },
        "scalarization_replay": {
            "tower": "F_p_SUBSET_F_(p^2)_SUBSET_F_(p^6)",
            "F_over_K_basis_size": 3,
            "domain_and_dual_weights_lie_in": "F_p_SUBSET_K",
            "ambient_recurrence_decomposes_coordinatewise": True,
            "ambient_zero_iff_all_three_K_coordinate_blocks_zero": True,
            "ambient_B_nonzero_iff_some_K_coordinate_is_nonzero": True,
            "scalarized_equation_count": SCALARIZED_ROWS,
            "scalarized_pivot_labels_identical_to_ambient_labels": False,
            "reason_labels_differ": (
                "AMBIENT_LABEL_h_HAS_THREE_K_COORDINATES_AFTER_BASIS_EXPANSION"
            ),
            "ambient_adapter_is_canonical_branch2_label_set": True,
            "canonical_label_set": "AMBIENT_HANKEL_ROWS_h=0_TO_t-1",
            "scalar_replay_scan_order": "ROW_h_FIRST_THEN_BASIS_COMPONENT_i",
            "flattened_scalar_least_coordinate_is_canonical": False,
            "scalarization_defines_branch2_labels": False,
            "equivalence_scope": "COMMON_K_VALUED_LOCATOR_SLICE_ONLY",
            "full_restriction_of_scalars_column_count": 3 * LOCATOR_COORDS,
            "simple_scalar_stack_column_count": LOCATOR_COORDS,
            "scalar_stack_rank_equivalent_to_ambient_matrix": False,
            "rank_falsifier": (
                "M_F=[1,beta]_HAS_F_RANK_1_WHILE_ITS_K_COEFFICIENT_"
                "STACK_HAS_K_RANK_2_FOR_beta_IN_F_MINUS_K"
            ),
            "scalarization_is_equivalence_replay_only": True,
        },
        "prime_field_control": prime_control,
        "two_root_control": {
            "status": "EXACT_SMALL_TOWER_ROUTE_CUT_CONTROL",
            "base_field": "F_7",
            "parameter_field": "F_(7^2)",
            "ambient_field": "F_(7^6)",
            "domain": [0, 1, 2, 3, 4, 5],
            "n": 6,
            "k": 2,
            "agreement_A": 4,
            "j": 2,
            "t": 2,
            "supports_enumerated": 15,
            "co_supports": [[0, 1], [2, 4]],
            "co_supports_disjoint": True,
            "agreement_supports": [[2, 3, 4, 5], [0, 1, 3, 5]],
            "gamma_1": "eta",
            "gamma_2": "eta+1",
            "gamma_values_distinct": True,
            "both_gammas_in_parameter_field": True,
            "both_gammas_outside_base_field": True,
            "global_syndrome_rank": 2,
            "projective_syndrome_field_full": True,
            "both_support_equations_hold": True,
            "both_supports_noncontained": True,
            "both_least_pivot_equations_hold": True,
            "least_pivots": [0, 1],
            "distinct_support_roots_proved": True,
            "exact_support_root_count": 2,
            "frobenius_augmented_ranks": {"1": 3, "2": 3, "3": 3},
            "survives_rank_policy_proved": False,
            "survives_branches_3_to_5_proved": False,
            "route_cut": (
                "BRANCH1_PLUS_FIELD_NATIVE_PIVOT_PLUS_POST_C5_FULL_FIELD"
                "_RANK2_DOES_NOT_IMPLY_GLOBAL_ONE_ROOT"
            ),
            "evidence_scope": "EXACT_TOY_CONTROL_NOT_DEPLOYED_ASYMPTOTIC_BOUND",
        },
        "ledger": {
            "pivot_subgate_closed": True,
            "pivot_failure_actual_witness_count": 0,
            "rank_subgate_closed": False,
            "branch2_closed": False,
            "legacy_red_p_bridge_closed": False,
            "field_full_rank_two_support_union_closed": False,
            "pivot_adapter_charge": None,
            "branch2_charge": None,
            "rank_drop_charge": None,
            "U_2": None,
            "U_Q": None,
            "U_A": None,
            "ledger_consequence": False,
            "row_complete": False,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
            "next_attack": (
                "FREEZE_THE_RANK_DROP_THRESHOLD_OWNER_AND_ITS_RELATION"
                "_TO_THE_FIELD_NATIVE_HANKEL_PENCIL"
            ),
        },
        "audit_sections": {
            "parameter_dependence": (
                "FORMULA_UNIFORM_OVER_FINITE_RS_DOMAINS_"
                "DIMENSIONS_AND_LEDGER_KOALABEAR_SPECIFIC"
            ),
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "numerical_evidence": (
                "EXACT_FINITE_CONTROLS_ONLY_NO_ASYMPTOTIC_INFERENCE"
            ),
            "edge_cases": EDGE_CASES,
            "remaining_risks": REMAINING_RISKS,
        },
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_sources() -> None:
    paper_d = (ROOT / PAPER_D_REL).read_text(encoding="utf-8")
    for anchor in (
        r"\label{lem:support-locator-syndrome-recurrence}",
        r"\label{lem:exact-line-image-map}",
        r"A_T:=H_{t,j}(u)\boldsymbol\ell_T",
        r"B_T:=H_{t,j}(v)\boldsymbol\ell_T",
        r"A_T+zB_T=0",
        r"B_T\ne0",
    ):
        require(anchor in paper_d, f"Paper D adapter anchor missing: {anchor}")

    kb_note = (ROOT / KB_NOTE_REL).read_text(encoding="utf-8")
    for anchor in (
        "rank-drop or pivot failure",
        "red_p(B_0(S)) != 0",
        "L_i(S,Z) = A_i(S) + Z B_i(S)",
    ):
        require(anchor in kb_note, f"KB legacy anchor missing: {anchor}")

    post_c5 = load_json(ROOT / POST_C5_CERT_REL)
    branch2 = post_c5["mask_inventory"]["records"][1]
    require(branch2["order"] == 2, "predecessor branch-2 order drift")
    require(
        branch2["machine_status"] == "UNBOUND_SOURCE_SYMBOL",
        "predecessor branch-2 source status drift",
    )
    require(
        branch2["actual_slope_projector_complete"] is False,
        "predecessor branch 2 unexpectedly complete",
    )

    predecessor_note = (ROOT / PREDECESSOR_NOTE_REL).read_text(
        encoding="utf-8"
    )
    for anchor in (
        "Lemma 1: exact quadratic-parameter scalarization",
        "3(A-k) = 202,416",
        "fixed support contributes at most one slope",
    ):
        require(
            anchor in predecessor_note,
            f"quadratic predecessor anchor missing: {anchor}",
        )

    predecessor = load_json(ROOT / PREDECESSOR_CERT_REL)
    transfer = predecessor["coordinate_transfer"]
    require(
        transfer["basis_length"] == 3
        and transfer["support_and_noncontainment_preserved"] is True
        and transfer["reduced_syndrome_equations"] == SCALARIZED_ROWS,
        "quadratic scalarization contract drift",
    )

    coordinate_transfer = (ROOT / COORDINATE_TRANSFER_REL).read_text(
        encoding="utf-8"
    )
    for anchor in (
        "exact support-wise MCA transfer",
        "Phi(C_F) = C_B^e.",
        "containment and noncontainment are",
    ):
        require(
            anchor in coordinate_transfer,
            f"coordinate-transfer source anchor missing: {anchor}",
        )

    base = load_json(ROOT / BASE_CERT_REL)
    require(
        int(base["arithmetic"]["new_U_paid"]) == U_PAID,
        "current paid baseline drift",
    )


def validate_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list, "source_bindings is not a list")
    for index, entry in enumerate(bindings):
        require(type(entry) is dict, f"source binding {index} is not an object")
        require(
            set(entry) == {"binding_id", "path", "sha256", "role"},
            f"source binding {index} keys drift",
        )
    require(
        bindings == expected_source_bindings(),
        "source binding path/hash/role drift",
    )
    ids = [entry["binding_id"] for entry in bindings]
    require(len(ids) == len(set(ids)), "duplicate source binding id")


def validate(artifact: dict[str, Any], *, exact_rebuild: bool = True) -> None:
    require(set(artifact) == TOP_KEYS, "top-level keys drift")
    require(artifact["schema"] == SCHEMA, "schema drift")
    require(
        artifact["artifact_kind"]
        == "M1_KB_BRANCH2_HANKEL_PIVOT_ADAPTER",
        "artifact kind drift",
    )
    require(
        artifact["status"] == STATUS,
        "status drift",
    )
    expected_structure = build_certificate()
    for section in (
        "row",
        "paper_d_adapter",
        "branch2_refinement",
        "scalarization_replay",
        "prime_field_control",
        "two_root_control",
        "ledger",
        "audit_sections",
    ):
        require(type(artifact[section]) is dict, f"{section} is not an object")
        require(
            set(artifact[section]) == set(expected_structure[section]),
            f"{section} keys drift",
        )
    validate_source_bindings(artifact["source_bindings"])
    validate_sources()

    row = artifact["row"]
    for key in (
        "p",
        "ambient_extension_degree",
        "quadratic_parameter_extension_degree",
        "n",
        "k",
        "agreement_A",
        "redundancy_r",
        "co_support_size_j",
        "hankel_depth_t",
        "locator_coordinate_count",
        "ambient_hankel_entry_count",
        "ambient_kernel_dimension_lower_bound",
        "scalarized_row_count",
        "scalarized_kernel_dimension_lower_bound",
    ):
        require_int(row[key], f"row.{key}")
    require(
        (
            row["p"],
            row["ambient_extension_degree"],
            row["quadratic_parameter_extension_degree"],
            row["n"],
            row["k"],
            row["agreement_A"],
            row["redundancy_r"],
            row["co_support_size_j"],
            row["hankel_depth_t"],
            row["locator_coordinate_count"],
        )
        == (P, 6, 2, N, K_DIM, A, R, J, T, LOCATOR_COORDS),
        "row constants drift",
    )
    require(
        row["ambient_hankel_shape"] == [T, LOCATOR_COORDS],
        "ambient Hankel shape drift",
    )
    require(
        row["ambient_hankel_entry_count"] == MATRIX_ENTRY_COUNT,
        "ambient matrix entry count drift",
    )
    require(
        row["ambient_kernel_dimension_lower_bound"] == KERNEL_LOWER,
        "ambient kernel lower bound drift",
    )
    require(
        row["scalarized_row_count"] == SCALARIZED_ROWS
        and row["scalarized_kernel_dimension_lower_bound"]
        == SCALARIZED_KERNEL_LOWER,
        "scalarized dimension drift",
    )
    require(int(row["B_star"]) == B_STAR, "B_star drift")
    require(
        int(row["U_paid"]) == U_PAID
        and int(row["B_remaining"]) == B_REMAINING,
        "ledger baseline drift",
    )

    adapter = artifact["paper_d_adapter"]
    require(
        adapter["agreement_support_symbol"] == "S"
        and adapter["agreement_support_cardinality"] == A
        and adapter["co_support_definition"] == "T=D_MINUS_S"
        and adapter["co_support_cardinality"] == J,
        "support/complement convention drift",
    )
    require_int(
        adapter["locator_top_coefficient"],
        "paper_d_adapter.locator_top_coefficient",
    )
    require(
        adapter["locator"]
        == "L_T(X)=prod_{x_in_T}(X-x)=sum_{b=0}^j ell_b X^b"
        and adapter["locator_coefficient_order"]
        == "LOW_TO_HIGH_WITH_MONIC_TOP"
        and adapter["locator_top_coefficient"] == 1,
        "locator coefficient order drift",
    )
    require(
        adapter["dual_weight_formula"]
        == "lambda_x=(prod_{y_in_D,y!=x}(x-y))^(-1)"
        and adapter["syndrome_formula"]
        == "Syn(Y)_m=sum_{x_in_D} lambda_x*x^m*Y(x)"
        and adapter["syndrome_moment_range"] == "0<=m<r",
        "weighted syndrome contract drift",
    )
    require(
        adapter["U_definition"] == "H_(t,j)(Syn_F(f))"
        and adapter["V_definition"] == "H_(t,j)(Syn_F(g))"
        and adapter["matrix_entry_formula"] == "H(w)[h,b]=w[h+b]"
        and adapter["A_Han_definition"] == "A_Han(T)=U*ell_T"
        and adapter["B_Han_definition"] == "B_Han(T)=V*ell_T",
        "implicit Hankel formula drift",
    )
    require(
        adapter["matrix_materialization_required"] is False,
        "huge Hankel matrix falsely materialized",
    )
    require(
        adapter["evaluation_mode"]
        == "IMPLICIT_TRUNCATED_CONVOLUTION",
        "implicit evaluation mode drift",
    )
    require(
        adapter["quotient_map"] == "Phi_T^F(w)=H_(t,j)(w)*ell_T"
        and adapter["quotient_map_kernel"] == "W_T(F)"
        and adapter["quotient_map_isomorphism"] == "F^r/W_T(F)_TO_F^t",
        "canonical quotient-map contract drift",
    )
    require(
        adapter["finite_noncontained_equivalence"].endswith(
            "IFF_A_Han+gamma*B_Han=0_AND_B_Han!=0"
        ),
        "finite support-image equivalence drift",
    )
    require(
        adapter["source_status"] == "IMPORTED_PROVED_PAPER_D_V12",
        "Paper D provenance drift",
    )

    branch2 = artifact["branch2_refinement"]
    require_int(
        branch2["pivot_labels"],
        "branch2_refinement.pivot_labels",
    )
    require_int(
        branch2["pivot_failure_actual_witness_count"],
        "branch2_refinement.pivot_failure_actual_witness_count",
    )
    require(
        branch2["predecessor_machine_status"] == "UNBOUND_SOURCE_SYMBOL",
        "predecessor status drift",
    )
    require(
        branch2["corrected_pivot_status"]
        == "FIELD_NATIVE_HANKEL_PIVOT_DEFINED"
        and branch2["pivot_adapter_complete"] is True,
        "pivot status drift",
    )
    require(
        branch2["scope"]
        == (
            "ACTUAL_FINITE_SUPPORT_WISE_NONCONTAINED_INCIDENCE_"
            "AFTER_CONTAINED_AND_INCONSISTENT_CASES"
        )
        and branch2["branch1_projector_complete"] is False,
        "relative pivot scope drift",
    )
    require(
        branch2["least_pivot_rule"]
        == "h_star=MIN_h_WITH_B_Han(T)[h]!=0",
        "least pivot rule drift",
    )
    require(
        branch2["earlier_pivot_equations"]
        == "B_Han(T)[h]=0_FOR_h<h_star"
        and branch2["pivot_inequation"]
        == "B_Han(T)[h_star]!=0",
        "pivot chart equations drift",
    )
    require(
        branch2["cross_equations"]
        == (
            "A_Han(T)[m]*B_Han(T)[h_star]"
            "-A_Han(T)[h_star]*B_Han(T)[m]=0_FOR_ALL_m"
        )
        and branch2["slope_formula"]
        == "gamma=-A_Han(T)[h_star]/B_Han(T)[h_star]",
        "pivot cross-equation or root formula drift",
    )
    require(branch2["pivot_labels"] == T, "ambient pivot label count drift")
    require(
        branch2["pivot_labels_are_hankel_rows_not_supports"] is True,
        "pivot labels misidentified",
    )
    require(
        branch2["pivot_failure_empty_after_branch1"] is True,
        "pivot failure reopened",
    )
    require(
        branch2["pivot_failure_actual_witness_count"] == 0,
        "pivot failure actual-witness count drift",
    )
    require(
        branch2["reason_pivot_failure_empty"]
        == "FINITE_NONCONTAINED_INCIDENCE_REQUIRES_B_Han_NOT_ZERO",
        "pivot failure reason drift",
    )
    require(
        branch2["rank_policy_complete"] is False
        and branch2["deployed_rank_drop_predicate_complete"] is False
        and branch2["rank_drop_owner"] is None
        and branch2["rank_drop_charge"] is None,
        "rank policy invented",
    )
    require(
        branch2["legacy_red_p_bridge"] is False
        and branch2["legacy_paper_d_symbol"] == "B_Han(T)[h]"
        and branch2["legacy_kb_symbol"] == "red_p(B_0(S))"
        and branch2["legacy_identification_proved"] is False
        and branch2["cyclotomic_lift_map"] is None,
        "legacy bridge invented",
    )
    require(branch2["branch2_complete"] is False, "branch 2 falsely complete")
    require(
        branch2["paid_owner"] is None and branch2["charge"] is None,
        "pivot adapter falsely charged",
    )

    scalar = artifact["scalarization_replay"]
    require_int(
        scalar["scalarized_equation_count"],
        "scalarization_replay.scalarized_equation_count",
    )
    require_int(
        scalar["full_restriction_of_scalars_column_count"],
        "scalarization_replay.full_restriction_of_scalars_column_count",
    )
    require_int(
        scalar["simple_scalar_stack_column_count"],
        "scalarization_replay.simple_scalar_stack_column_count",
    )
    require(
        scalar["tower"] == "F_p_SUBSET_F_(p^2)_SUBSET_F_(p^6)"
        and scalar["F_over_K_basis_size"] == 3
        and scalar["domain_and_dual_weights_lie_in"] == "F_p_SUBSET_K",
        "F/K basis size drift",
    )
    require(
        scalar["ambient_recurrence_decomposes_coordinatewise"] is True
        and scalar["ambient_zero_iff_all_three_K_coordinate_blocks_zero"]
        is True
        and scalar["ambient_B_nonzero_iff_some_K_coordinate_is_nonzero"]
        is True,
        "scalarization equivalence drift",
    )
    require(
        scalar["scalarized_pivot_labels_identical_to_ambient_labels"]
        is False,
        "ambient and scalarized label sets falsely identified",
    )
    require(
        scalar["ambient_adapter_is_canonical_branch2_label_set"] is True
        and scalar["canonical_label_set"]
        == "AMBIENT_HANKEL_ROWS_h=0_TO_t-1"
        and scalar["scalar_replay_scan_order"]
        == "ROW_h_FIRST_THEN_BASIS_COMPONENT_i"
        and scalar["flattened_scalar_least_coordinate_is_canonical"] is False
        and scalar["scalarization_defines_branch2_labels"] is False
        and scalar["equivalence_scope"]
        == "COMMON_K_VALUED_LOCATOR_SLICE_ONLY"
        and scalar["full_restriction_of_scalars_column_count"]
        == 3 * LOCATOR_COORDS
        and scalar["simple_scalar_stack_column_count"] == LOCATOR_COORDS
        and scalar["scalar_stack_rank_equivalent_to_ambient_matrix"] is False
        and scalar["scalarization_is_equivalence_replay_only"] is True,
        "canonical adapter direction drift",
    )
    require(
        "F_RANK_1" in scalar["rank_falsifier"]
        and "K_RANK_2" in scalar["rank_falsifier"],
        "rank falsifier drift",
    )

    prime = artifact["prime_field_control"]
    for key in (
        "p",
        "n",
        "k",
        "agreement_A",
        "j",
        "t",
        "designed_bad_slope",
        "designed_least_pivot_h",
        "supports_enumerated",
        "slopes_per_support",
        "direct_checks",
        "recurrence_checks",
        "contained_incidence_checks",
        "bad_record_count",
    ):
        require_int(prime[key], f"prime_field_control.{key}")
    expected_prime = build_prime_field_control()
    require(prime == expected_prime, "prime-field control drift")
    require(
        prime["direct_interpolation_equals_hankel_adapter"] is True,
        "prime control lost exact adapter equivalence",
    )
    require(
        prime["B_zero_incidence_implies_joint_containment"] is True,
        "prime control lost B=0 containment check",
    )
    require(
        prime["all_bad_records_have_least_pivot"] is True,
        "prime control has an unpivoted bad incidence",
    )
    require(
        prime["dual_weights"] == [16, 5, 7, 10, 12, 1]
        and prime["designed_co_support_indices"] == [4, 5]
        and prime["designed_locator_coefficients_low_to_high"] == [3, 8, 1]
        and prime["designed_A_Han"] == [0, 14]
        and prime["designed_B_Han"] == [0, 1]
        and prime["designed_least_pivot_h"] == 1
        and prime["non_first_pivot_exercised"] is True,
        "prime convention/non-first-pivot control drift",
    )
    require(
        prime["B_zero_positive_control"]
        == {
            "agreement_support_indices": [0, 1, 2, 3],
            "co_support_indices": [4, 5],
            "locator_coefficients_low_to_high": [3, 8, 1],
            "A_Han": [0, 0],
            "B_Han": [0, 0],
            "test_slope": 11,
            "joint_containment_directly_checked": True,
            "affine_incidence_directly_checked": True,
        },
        "positive B=0 contained-incidence control drift",
    )

    control = artifact["two_root_control"]
    for key in (
        "n",
        "k",
        "agreement_A",
        "j",
        "t",
        "supports_enumerated",
        "global_syndrome_rank",
        "exact_support_root_count",
    ):
        require_int(control[key], f"two_root_control.{key}")
    require(
        control["status"] == "EXACT_SMALL_TOWER_ROUTE_CUT_CONTROL",
        "two-root control status drift",
    )
    require(
        control["base_field"] == "F_7"
        and control["parameter_field"] == "F_(7^2)"
        and control["ambient_field"] == "F_(7^6)"
        and control["gamma_1"] == "eta"
        and control["gamma_2"] == "eta+1",
        "two-root field/gamma label drift",
    )
    require(
        control["domain"] == [0, 1, 2, 3, 4, 5]
        and (control["n"], control["k"], control["agreement_A"])
        == (6, 2, 4)
        and (control["j"], control["t"]) == (2, 2)
        and control["supports_enumerated"] == 15
        and control["co_supports"] == [[0, 1], [2, 4]]
        and control["co_supports_disjoint"] is True
        and control["agreement_supports"]
        == [[2, 3, 4, 5], [0, 1, 3, 5]],
        "two-root support convention drift",
    )
    for key in (
        "gamma_values_distinct",
        "both_gammas_in_parameter_field",
        "both_gammas_outside_base_field",
        "projective_syndrome_field_full",
        "both_support_equations_hold",
        "both_supports_noncontained",
        "both_least_pivot_equations_hold",
        "distinct_support_roots_proved",
    ):
        require(control[key] is True, f"two-root control lost {key}")
    require(control["global_syndrome_rank"] == 2, "two-root rank drift")
    require(
        control["least_pivots"] == [0, 1]
        and control["exact_support_root_count"] == 2
        and control["frobenius_augmented_ranks"]
        == {"1": 3, "2": 3, "3": 3},
        "two-root pivot/root/field control drift",
    )
    require(
        control["survives_rank_policy_proved"] is False
        and control["survives_branches_3_to_5_proved"] is False,
        "toy control promoted to deployed first-match survivor",
    )
    require(
        control["route_cut"]
        == (
            "BRANCH1_PLUS_FIELD_NATIVE_PIVOT_PLUS_POST_C5_FULL_FIELD"
            "_RANK2_DOES_NOT_IMPLY_GLOBAL_ONE_ROOT"
        ),
        "two-root route cut drift",
    )

    ledger = artifact["ledger"]
    require_int(
        ledger["pivot_failure_actual_witness_count"],
        "ledger.pivot_failure_actual_witness_count",
    )
    require(ledger["pivot_subgate_closed"] is True, "pivot subgate not closed")
    require(
        ledger["pivot_failure_actual_witness_count"] == 0,
        "ledger pivot-failure count drift",
    )
    require(
        ledger["rank_subgate_closed"] is False
        and ledger["branch2_closed"] is False
        and ledger["legacy_red_p_bridge_closed"] is False,
        "open branch-2 dependency falsely closed",
    )
    require(
        ledger["field_full_rank_two_support_union_closed"] is False,
        "rank-two union falsely closed",
    )
    require(
        ledger["pivot_adapter_charge"] is None
        and ledger["branch2_charge"] is None
        and ledger["rank_drop_charge"] is None,
        "open branch-2 component charged",
    )
    require(
        ledger["U_2"] is None
        and ledger["U_Q"] is None
        and ledger["U_A"] is None,
        "null open ledger term changed",
    )
    require(
        ledger["ledger_consequence"] is False
        and ledger["row_complete"] is False,
        "row closure overclaim",
    )
    require(
        ledger["inequality_status"] == "UNDECIDED_OPEN_COMPONENTS"
        and ledger["next_attack"]
        == (
            "FREEZE_THE_RANK_DROP_THRESHOLD_OWNER_AND_ITS_RELATION"
            "_TO_THE_FIELD_NATIVE_HANKEL_PENCIL"
        ),
        "ledger open-status/next-attack drift",
    )

    audit = artifact["audit_sections"]
    require(
        audit["layer_cake_dyadic_summability"] == "NOT_APPLICABLE",
        "layer-cake status drift",
    )
    require(
        audit["moment_markov_chebyshev"] == "NOT_APPLICABLE",
        "moment status drift",
    )
    require(audit["edge_cases"] == EDGE_CASES, "edge cases drift")
    require(
        audit["remaining_risks"] == REMAINING_RISKS,
        "remaining risks drift",
    )
    require(artifact["nonclaims"] == NONCLAIMS, "nonclaims drift")
    require(
        artifact["payload_sha256"] == payload_hash(artifact),
        "payload hash drift",
    )

    if exact_rebuild:
        require(
            canonical_bytes(artifact) == canonical_bytes(build_certificate()),
            "deterministic certificate rebuild drift",
        )


def expect_reject(
    name: str, artifact: dict[str, Any], cases: list[tuple[str, bool]]
) -> None:
    try:
        validate(artifact, exact_rebuild=False)
    except (VerificationError, KeyError, TypeError, ValueError):
        cases.append((name, True))
        return
    cases.append((name, False))


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    target: Any = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def run_tamper_selftest(artifact: dict[str, Any]) -> int:
    cases: list[tuple[str, bool]] = []

    def mutate(name: str, path: tuple[Any, ...], replacement: Any) -> None:
        candidate = copy.deepcopy(artifact)
        set_path(candidate, path, replacement)
        candidate["payload_sha256"] = payload_hash(candidate)
        expect_reject(name, candidate, cases)

    mutate("row-j-drift", ("row", "co_support_size_j"), J - 1)
    mutate("row-t-drift", ("row", "hankel_depth_t"), T + 1)
    mutate(
        "matrix-shape-drift",
        ("row", "ambient_hankel_shape"),
        [T, LOCATOR_COORDS - 1],
    )
    mutate(
        "matrix-materialized",
        ("paper_d_adapter", "matrix_materialization_required"),
        True,
    )
    mutate(
        "support-complement-reversed",
        ("paper_d_adapter", "co_support_definition"),
        "S=D_MINUS_T",
    )
    mutate(
        "locator-order-reversed",
        ("paper_d_adapter", "locator_coefficient_order"),
        "HIGH_TO_LOW",
    )
    mutate(
        "locator-nonmonic-bool",
        ("paper_d_adapter", "locator_top_coefficient"),
        True,
    )
    mutate(
        "dual-weights-omitted",
        ("paper_d_adapter", "dual_weight_formula"),
        "lambda_x=1",
    )
    mutate(
        "syndrome-moment-off-by-one",
        ("paper_d_adapter", "syndrome_moment_range"),
        "0<=m<=r",
    )
    mutate(
        "hankel-U-V-swapped",
        ("paper_d_adapter", "U_definition"),
        "H_(t,j)(Syn_F(g))",
    )
    mutate(
        "support-image-weakened",
        ("paper_d_adapter", "finite_noncontained_equivalence"),
        "A_Han+gamma*B_Han=0",
    )
    mutate(
        "paper-d-provenance-erased",
        ("paper_d_adapter", "source_status"),
        "NEW_THEOREM",
    )
    mutate(
        "pivot-status-reopened",
        ("branch2_refinement", "corrected_pivot_status"),
        "UNBOUND_SOURCE_SYMBOL",
    )
    mutate(
        "pivot-adapter-reopened",
        ("branch2_refinement", "pivot_adapter_complete"),
        False,
    )
    mutate(
        "branch1-projector-invented",
        ("branch2_refinement", "branch1_projector_complete"),
        True,
    )
    mutate(
        "nonleast-pivot",
        ("branch2_refinement", "least_pivot_rule"),
        "CHOOSE_ANY_NONZERO",
    )
    mutate(
        "pivot-labels-tripled",
        ("branch2_refinement", "pivot_labels"),
        SCALARIZED_ROWS,
    )
    mutate(
        "pivot-called-support",
        (
            "branch2_refinement",
            "pivot_labels_are_hankel_rows_not_supports",
        ),
        False,
    )
    mutate(
        "pivot-failure-reopened",
        ("branch2_refinement", "pivot_failure_empty_after_branch1"),
        False,
    )
    mutate(
        "cross-equations-omitted",
        ("branch2_refinement", "cross_equations"),
        "OMITTED",
    )
    mutate(
        "slope-sign-flipped",
        ("branch2_refinement", "slope_formula"),
        "gamma=A/B",
    )
    mutate(
        "rank-policy-invented",
        ("branch2_refinement", "rank_policy_complete"),
        True,
    )
    mutate(
        "rank-predicate-invented",
        (
            "branch2_refinement",
            "deployed_rank_drop_predicate_complete",
        ),
        True,
    )
    mutate(
        "rank-owner-invented",
        ("branch2_refinement", "rank_drop_owner"),
        "PERIODIC_OWNER",
    )
    mutate(
        "rank-charge-zero",
        ("branch2_refinement", "rank_drop_charge"),
        0,
    )
    mutate(
        "legacy-bridge-invented",
        ("branch2_refinement", "legacy_red_p_bridge"),
        True,
    )
    mutate(
        "legacy-identification-invented",
        ("branch2_refinement", "legacy_identification_proved"),
        True,
    )
    mutate(
        "cyclotomic-map-invented",
        ("branch2_refinement", "cyclotomic_lift_map"),
        "UNPROVED_MAP",
    )
    mutate(
        "branch2-falsely-complete",
        ("branch2_refinement", "branch2_complete"),
        True,
    )
    mutate(
        "pivot-owner-invented",
        ("branch2_refinement", "paid_owner"),
        "rank_drop_or_pivot_failure",
    )
    mutate(
        "pivot-charge-zero",
        ("branch2_refinement", "charge"),
        0,
    )
    mutate(
        "scalarization-basis-drift",
        ("scalarization_replay", "F_over_K_basis_size"),
        2,
    )
    mutate(
        "scalarization-tower-drift",
        ("scalarization_replay", "tower"),
        "F_p_SUBSET_F_(p^3)_SUBSET_F_(p^6)",
    )
    mutate(
        "scalar-labels-identified",
        (
            "scalarization_replay",
            "scalarized_pivot_labels_identical_to_ambient_labels",
        ),
        True,
    )
    mutate(
        "scalarization-made-canonical",
        (
            "scalarization_replay",
            "ambient_adapter_is_canonical_branch2_label_set",
        ),
        False,
    )
    mutate(
        "scalar-component-major-scan",
        ("scalarization_replay", "scalar_replay_scan_order"),
        "BASIS_COMPONENT_i_FIRST_THEN_ROW_h",
    )
    mutate(
        "scalar-flat-coordinate-made-canonical",
        (
            "scalarization_replay",
            "flattened_scalar_least_coordinate_is_canonical",
        ),
        True,
    )
    mutate(
        "scalar-rank-equivalence-invented",
        (
            "scalarization_replay",
            "scalar_stack_rank_equivalent_to_ambient_matrix",
        ),
        True,
    )
    mutate(
        "prime-record-count-drift",
        ("prime_field_control", "bad_record_count"),
        artifact["prime_field_control"]["bad_record_count"] + 1,
    )
    mutate(
        "prime-adapter-equivalence-false",
        (
            "prime_field_control",
            "direct_interpolation_equals_hankel_adapter",
        ),
        False,
    )
    mutate(
        "prime-bzero-containment-false",
        (
            "prime_field_control",
            "B_zero_incidence_implies_joint_containment",
        ),
        False,
    )
    mutate(
        "prime-dual-weight-drift",
        ("prime_field_control", "dual_weights"),
        [1, 1, 1, 1, 1, 1],
    )
    mutate(
        "prime-non-first-pivot-erased",
        ("prime_field_control", "non_first_pivot_exercised"),
        False,
    )
    mutate(
        "prime-bzero-positive-control-erased",
        (
            "prime_field_control",
            "B_zero_positive_control",
            "joint_containment_directly_checked",
        ),
        False,
    )
    mutate(
        "two-roots-collapsed",
        ("two_root_control", "gamma_values_distinct"),
        False,
    )
    mutate(
        "two-root-gamma-label-base",
        ("two_root_control", "gamma_1"),
        "1",
    )
    mutate(
        "two-root-base-valued",
        ("two_root_control", "both_gammas_outside_base_field"),
        False,
    )
    mutate(
        "two-root-parameter-membership-erased",
        ("two_root_control", "both_gammas_in_parameter_field"),
        False,
    )
    mutate(
        "two-root-field-not-full",
        ("two_root_control", "projective_syndrome_field_full"),
        False,
    )
    mutate(
        "two-root-rank-one",
        ("two_root_control", "global_syndrome_rank"),
        1,
    )
    mutate(
        "two-root-support-failure",
        ("two_root_control", "both_support_equations_hold"),
        False,
    )
    mutate(
        "two-root-pivots-collapsed",
        ("two_root_control", "least_pivots"),
        [0, 0],
    )
    mutate(
        "two-root-count-one",
        ("two_root_control", "exact_support_root_count"),
        1,
    )
    mutate(
        "two-root-promoted-to-rank-survivor",
        ("two_root_control", "survives_rank_policy_proved"),
        True,
    )
    mutate(
        "two-root-promoted-post5",
        ("two_root_control", "survives_branches_3_to_5_proved"),
        True,
    )
    mutate(
        "rank-subgate-falsely-closed",
        ("ledger", "rank_subgate_closed"),
        True,
    )
    mutate(
        "rank2-union-falsely-closed",
        ("ledger", "field_full_rank_two_support_union_closed"),
        True,
    )
    mutate(
        "pivot-ledger-charge-zero",
        ("ledger", "pivot_adapter_charge"),
        0,
    )
    mutate(
        "branch2-ledger-charge-zero",
        ("ledger", "branch2_charge"),
        0,
    )
    mutate(
        "rank-ledger-charge-zero",
        ("ledger", "rank_drop_charge"),
        0,
    )
    mutate("U2-null-to-zero", ("ledger", "U_2"), 0)
    mutate("UQ-null-to-zero", ("ledger", "U_Q"), 0)
    mutate("UA-null-to-zero", ("ledger", "U_A"), 0)
    mutate("row-falsely-complete", ("ledger", "row_complete"), True)
    mutate(
        "inequality-falsely-decided",
        ("ledger", "inequality_status"),
        "PROVED",
    )
    mutate(
        "source-hash-drift",
        ("source_bindings", 0, "sha256"),
        "0" * 64,
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

    nested_unknown = copy.deepcopy(artifact)
    nested_unknown["ledger"]["unknown_field"] = True
    nested_unknown["payload_sha256"] = payload_hash(nested_unknown)
    expect_reject("unknown-nested-key", nested_unknown, cases)

    unknown = copy.deepcopy(artifact)
    unknown["unknown_field"] = True
    unknown["payload_sha256"] = payload_hash(unknown)
    expect_reject("unknown-top-key", unknown, cases)

    bad_payload = copy.deepcopy(artifact)
    bad_payload["payload_sha256"] = "0" * 64
    expect_reject("payload-hash", bad_payload, cases)

    bad_bool = copy.deepcopy(artifact)
    bad_bool["ledger"]["pivot_subgate_closed"] = 1
    bad_bool["payload_sha256"] = payload_hash(bad_bool)
    expect_reject("integer-as-bool", bad_bool, cases)

    for name, raw in (
        ("duplicate-json-key", '{"schema":"a","schema":"b"}'),
        ("nan-json-token", '{"value":NaN}'),
    ):
        try:
            json.loads(
                raw,
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=lambda token: (_ for _ in ()).throw(
                    VerificationError(f"non-finite JSON token: {token}")
                ),
            )
        except (VerificationError, ValueError):
            cases.append((name, True))
        else:
            cases.append((name, False))

    rejected = sum(1 for _, passed in cases if passed)
    failed = [name for name, passed in cases if not passed]
    require(not failed, f"mutations not rejected: {failed}")
    return rejected


def emit() -> None:
    artifact = build_certificate()
    validate(artifact)
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
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
        print(
            "M1_KB_BRANCH2_HANKEL_PIVOT_ADAPTER_V1_TAMPER_PASS "
            f"rejected={rejected}/{rejected}"
        )
    else:
        print("M1_KB_BRANCH2_HANKEL_PIVOT_ADAPTER_V1_VERIFY_PASS")
        print(
            "pivot subgate: field-native Hankel adapter executable; "
            "finite pivot failure empty on actual noncontained incidences"
        )
        print(
            "route cut: exact small-tower field-full rank-2 pair has "
            "two distinct quadratic support roots"
        )
        print(
            "open: rank policy and legacy red_p bridge; "
            "branch 2 incomplete; U_2/U_Q/U_A null"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
