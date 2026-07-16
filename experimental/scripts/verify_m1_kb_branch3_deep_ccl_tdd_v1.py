#!/usr/bin/env python3
"""Verify the KoalaBear branch-3 deep-owner extension and CCL/TDD cut.

The packet has two load-bearing claims.

* Actual noncontained witnesses of weight at most floor((n-k)/3) lift to the
  exact deep-MCA numerator.  This extends the already-paid branch-2 owner and
  banks only the incremental composite charge.
* After that deletion, the integrated excess-ten carrier owner is applied
  first.  A genuinely high selected union is either small or exhibits a
  nonzero triple-distance defect.

The script checks theorem-source interfaces, exact deployed arithmetic,
strict JSON/hash integrity, two exact finite-field controls, and mutation
rejection.  It does not enumerate the deployed field or pay the TDD residual.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-deep-ccl-tdd-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_DEEP_OWNER_EXTENSION_CCL_TDD_ROUTE_CUT"
STATUS = (
    "PROVED_DEEP_OWNER_EXTENSION_EXACT_SHARED_ENVELOPE_ACCOUNTING_DELTA_"
    "PROVED_CCL_TDD_DICHOTOMY_BRANCH3_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-deep-ccl-tdd-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_deep_ccl_tdd_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_deep_ccl_tdd_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-deep-ccl-tdd-v1/README.md"
)
VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py"
)
BRANCH2_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md"
)
BRANCH2_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch2-rank-deep-owner-v1/"
    "m1_kb_branch2_rank_deep_owner_v1.json"
)
BRANCH2_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py"
)
CARRIER_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_low_excess_carrier_cut_v1.md"
)
CARRIER_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-low-excess-carrier-cut-v1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.json"
)
CARRIER_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py"
)
PAPER_D_REL = Path("tex/cs25_cap_v12.tex")
THRESHOLDS_REL = Path("experimental/rs_mca_thresholds.tex")
CCL_TDD_SOURCE_REL = Path(
    "experimental/notes/thresholds/"
    "cap25_v13_seven_slope_ccl_tdd_split.md"
)
FIRST_MATCH_CERT_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-1116048-first-match-ledger-v1/"
    "kb_mca_1116048_first_match_ledger_v1.json"
)
POST_C5_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-fp2-post-c5-mask-incidence-v1/"
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
RANK_DROP_ERROR_CAP = T - 1
R_STAR = R // 3
A_STAR = N - R_STAR
DEEP_COMPOSITE_CAP = R_STAR + 1
BRANCH2_CHARGE = T
DEEP_INCREMENT = DEEP_COMPOSITE_CAP - BRANCH2_CHARGE
M0 = (R + T - 1) // T
SMALL_CAP = M0 - 1
M16_CARRIER_CAP = (M0 * J) // (M0 - 1)
M15_CARRIER_CAP = (SMALL_CAP * J) // (SMALL_CAP - 1)
MIN_DISTANCE = R + 1
CCL_CAP = J + 1
MAX_PAID_EXCESS = 10
B10 = math.comb(R + MAX_PAID_EXCESS, MAX_PAID_EXCESS + 1) // math.comb(
    R + MAX_PAID_EXCESS - J - 1,
    MAX_PAID_EXCESS,
)
B11 = math.comb(R + MAX_PAID_EXCESS + 1, MAX_PAID_EXCESS + 2) // math.comb(
    R + MAX_PAID_EXCESS + 1 - J - 1,
    MAX_PAID_EXCESS + 1,
)

DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID_BEFORE = 2_602_220_945
B_REMAINING_BEFORE = B_STAR - U_PAID_BEFORE
U_PAID_AFTER = U_PAID_BEFORE + DEEP_INCREMENT
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
    "branch_scope",
    "deep_owner_extension",
    "heavy_residual",
    "ccl_tdd_dichotomy",
    "toy_controls",
    "classifier_contract",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

EDGE_CASES = [
    "Actual error supports are tied to declared noncontained witnesses and exclude zero-amplitude padding.",
    "The extended deep owner uses existence of one valid witness of weight at most r_star.",
    "After deleting that intrinsic owner, every valid selected witness has weight at least r_star+1.",
    "The deep increment is a composite branch-2-plus-branch-3 allowance, not a stand-alone branch-3 cap.",
    "All slopes are finite and distinct; the point at infinity is excluded.",
    "The integrated excess-ten carrier owner is checked before the small-family and TDD terminals.",
    "A TDD is defined by a nonzero defect; the large triple union follows from RS minimum distance.",
    "The common-code-line argument routes an all-zero-defect family back to the selected-union carrier owner.",
    "No separate carrier or small-family charge is banked.",
    "Null ledger entries are not zero.",
]

REMAINING_RISKS = [
    "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT has no proved global owner.",
    "The frozen tangent/common-line/residue branch still lacks a complete paid projector.",
    "Branches 4 and 5, the field-full quadratic support union, U_2, U_Q, and U_A remain open.",
    "The complete KoalaBear row inequality remains undecided.",
]

NONCLAIMS = [
    "This packet does not prove the KoalaBear row safe.",
    "This packet does not close branch 3.",
    "This packet does not pay UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT.",
    "This packet does not claim that branch 3 alone has cap 282054.",
    "This packet does not add a separate common-code-line ledger charge.",
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


def file_sha256(path: Path) -> str:
    require(path.is_file(), f"missing source file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def source_binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_sha256(ROOT / relative),
        "role": role,
    }


def exact_multiplier(budget: int) -> int:
    return (budget * P**RANK_DROP_ERROR_CAP) // math.comb(N, J)


def weight(vector: list[int], modulus: int) -> int:
    return sum((entry % modulus) != 0 for entry in vector)


def vadd(left: list[int], right: list[int], modulus: int) -> list[int]:
    require(len(left) == len(right), "vector length mismatch")
    return [(a + b) % modulus for a, b in zip(left, right)]


def vsub(left: list[int], right: list[int], modulus: int) -> list[int]:
    require(len(left) == len(right), "vector length mismatch")
    return [(a - b) % modulus for a, b in zip(left, right)]


def vscale(scalar: int, vector: list[int], modulus: int) -> list[int]:
    return [(scalar * entry) % modulus for entry in vector]


def solve_square_mod(
    matrix: list[list[int]], rhs: list[int], modulus: int
) -> list[int]:
    n = len(matrix)
    require(n == len(rhs), "square solver RHS mismatch")
    require(all(len(row) == n for row in matrix), "matrix is not square")
    aug = [
        [entry % modulus for entry in row] + [rhs[i] % modulus]
        for i, row in enumerate(matrix)
    ]
    for col in range(n):
        pivot = next(
            (row for row in range(col, n) if aug[row][col] % modulus),
            None,
        )
        require(pivot is not None, "singular modular system")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        inv = pow(aug[col][col], -1, modulus)
        aug[col] = [(inv * entry) % modulus for entry in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col] % modulus
            if factor:
                aug[row] = [
                    (a - factor * b) % modulus
                    for a, b in zip(aug[row], aug[col])
                ]
    return [aug[row][-1] % modulus for row in range(n)]


def polynomial_eval(coeffs: list[int], x: int, modulus: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x + coeff) % modulus
    return value


def is_rs_codeword(
    vector: list[int],
    domain: list[int],
    dimension: int,
    modulus: int,
) -> bool:
    require(len(vector) == len(domain), "codeword/domain length mismatch")
    require(1 <= dimension <= len(domain), "invalid RS dimension")
    vandermonde = [
        [pow(domain[row], col, modulus) for col in range(dimension)]
        for row in range(dimension)
    ]
    coeffs = solve_square_mod(
        vandermonde,
        [entry % modulus for entry in vector[:dimension]],
        modulus,
    )
    return all(
        polynomial_eval(coeffs, x, modulus) == entry % modulus
        for x, entry in zip(domain, vector)
    )


def restriction_extends_to_rs_codeword(
    vector: list[int],
    agreement_indices: list[int],
    domain: list[int],
    dimension: int,
    modulus: int,
) -> bool:
    require(len(vector) == len(domain), "restriction/domain length mismatch")
    if len(agreement_indices) <= dimension:
        return True
    anchors = agreement_indices[:dimension]
    vandermonde = [
        [pow(domain[index], col, modulus) for col in range(dimension)]
        for index in anchors
    ]
    coeffs = solve_square_mod(
        vandermonde,
        [vector[index] % modulus for index in anchors],
        modulus,
    )
    return all(
        polynomial_eval(coeffs, domain[index], modulus)
        == vector[index] % modulus
        for index in agreement_indices
    )


def defect(
    slopes: list[int],
    codewords: list[list[int]],
    triple: tuple[int, int, int],
    modulus: int,
) -> list[int]:
    i, j, k = triple
    first = vscale(slopes[j] - slopes[k], codewords[i], modulus)
    second = vscale(slopes[k] - slopes[i], codewords[j], modulus)
    third = vscale(slopes[i] - slopes[j], codewords[k], modulus)
    return vadd(vadd(first, second, modulus), third, modulus)


def classify_selected_family(
    *,
    modulus: int,
    domain: list[int],
    dimension: int,
    j_bound: int,
    max_paid_excess: int,
    actual_noncontained_witnesses: bool,
    transversality_certified: bool,
    slopes: list[int],
    f_word: list[int],
    g_word: list[int],
    codewords: list[list[int]],
) -> dict[str, Any]:
    n = len(domain)
    redundancy = n - dimension
    require(0 <= j_bound < redundancy, "toy classifier requires j<R")
    require(max_paid_excess >= 0, "negative paid-excess cutoff")
    require(
        actual_noncontained_witnesses is True,
        "declared actual noncontained witness contract missing",
    )
    require(
        transversality_certified is True,
        "syndrome transversality contract missing",
    )
    require(len(slopes) == len(codewords), "slope/codeword count mismatch")
    require(len(set(slope % modulus for slope in slopes)) == len(slopes),
            "duplicate finite slope")
    require(len(f_word) == n and len(g_word) == n, "received word length")
    require(all(len(word) == n for word in codewords), "codeword length")
    require(
        all(is_rs_codeword(word, domain, dimension, modulus)
            for word in codewords),
        "selected decoder output is not an RS codeword",
    )

    errors: list[list[int]] = []
    supports: list[set[int]] = []
    for slope, codeword in zip(slopes, codewords):
        received = vadd(f_word, vscale(slope, g_word, modulus), modulus)
        error = vsub(received, codeword, modulus)
        require(weight(error, modulus) <= j_bound, "selected error overweight")
        errors.append(error)
        supports.append(
            {index for index, entry in enumerate(error) if entry % modulus}
        )

    for support in supports:
        agreement_indices = [
            index for index in range(n) if index not in support
        ]
        f_extends = restriction_extends_to_rs_codeword(
            f_word,
            agreement_indices,
            domain,
            dimension,
            modulus,
        )
        g_extends = restriction_extends_to_rs_codeword(
            g_word,
            agreement_indices,
            domain,
            dimension,
            modulus,
        )
        require(
            not (f_extends and g_extends),
            "selected full-agreement witness is contained/nontransverse",
        )

    global_union = set().union(*supports) if supports else set()
    global_excess = max(0, len(global_union) - redundancy)
    if global_excess <= max_paid_excess:
        if global_excess == 0:
            owner = "INDEPENDENT_UNION_RAYS"
            cap = j_bound + 1
        else:
            owner = "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT"
            cap = math.comb(
                redundancy + global_excess,
                global_excess + 1,
            ) // math.comb(
                redundancy + global_excess - j_bound - 1,
                global_excess,
            )
        return {
            "terminal": "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
            "family_size": len(slopes),
            "selected_union_size": len(global_union),
            "selected_union_excess": global_excess,
            "owner": owner,
            "owner_cap": cap,
        }

    m0 = (redundancy + (redundancy - j_bound) - 1) // (
        redundancy - j_bound
    )
    if len(slopes) <= m0 - 1:
        return {
            "terminal": "CERTIFIED_HIGH_UNION_SMALL_FAMILY",
            "family_size": len(slopes),
            "small_cap": m0 - 1,
            "selected_union_size": len(global_union),
            "selected_union_excess": global_excess,
        }

    for triple in itertools.combinations(range(len(slopes)), 3):
        delta = defect(slopes, codewords, triple, modulus)
        if any(entry % modulus for entry in delta):
            require(
                is_rs_codeword(delta, domain, dimension, modulus),
                "nonzero defect left the code",
            )
            union = supports[triple[0]] | supports[triple[1]] | supports[triple[2]]
            delta_support = {
                index
                for index, entry in enumerate(delta)
                if entry % modulus
            }
            require(
                delta_support <= union,
                "defect support escaped the triple error union",
            )
            require(
                len(union) >= redundancy + 1,
                "nonzero RS defect violated minimum distance",
            )
            return {
                "terminal": "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
                "family_size": len(slopes),
                "triple": list(triple),
                "defect_weight": weight(delta, modulus),
                "triple_union_size": len(union),
                "selected_union_size": len(global_union),
                "selected_union_excess": global_excess,
            }

    slope0, slope1 = slopes[0] % modulus, slopes[1] % modulus
    inv = pow((slope1 - slope0) % modulus, -1, modulus)
    q_word = vscale(
        inv,
        vsub(codewords[1], codewords[0], modulus),
        modulus,
    )
    p_word = vsub(
        codewords[0],
        vscale(slope0, q_word, modulus),
        modulus,
    )
    require(
        is_rs_codeword(p_word, domain, dimension, modulus)
        and is_rs_codeword(q_word, domain, dimension, modulus),
        "derived affine code-line left the code",
    )
    for slope, codeword in zip(slopes, codewords):
        expected = vadd(p_word, vscale(slope, q_word, modulus), modulus)
        require(expected == [entry % modulus for entry in codeword],
                "zero defects failed affine code-line reconstruction")

    a_word = vsub(f_word, p_word, modulus)
    b_word = vsub(g_word, q_word, modulus)
    carrier = {
        index
        for index, pair in enumerate(zip(a_word, b_word))
        if pair[0] % modulus or pair[1] % modulus
    }
    m = len(slopes)
    cancellation_bound = (m * j_bound) // (m - 1)
    require(len(carrier) <= cancellation_bound,
            "common-line carrier exceeds cancellation bound")
    require(cancellation_bound <= redundancy,
            "common-line threshold did not force an independent carrier")
    require(all(support <= carrier for support in supports),
            "selected error escaped common carrier")
    require(carrier == global_union,
            "common-line carrier differs from selected support union")
    require(
        max(0, len(carrier) - redundancy) <= max_paid_excess,
        "high-union all-zero-defect family escaped the carrier owner",
    )
    raise VerificationError(
        "low-excess family reached the post-carrier high-union classifier"
    )


def toy_controls() -> dict[str, Any]:
    modulus = 17
    domain = list(range(8))
    dimension = 4
    j_bound = 3
    redundancy = len(domain) - dimension
    slopes = [0, 1, 2, 3]
    zero = [0] * len(domain)

    a_word = [0, -1, -2, -3, 0, 0, 0, 0]
    b_word = [1, 1, 1, 1, 0, 0, 0, 0]
    ccl = classify_selected_family(
        modulus=modulus,
        domain=domain,
        dimension=dimension,
        j_bound=j_bound,
        max_paid_excess=0,
        actual_noncontained_witnesses=True,
        transversality_certified=True,
        slopes=slopes,
        f_word=[entry % modulus for entry in a_word],
        g_word=b_word,
        codewords=[zero[:] for _ in slopes],
    )
    require(ccl["terminal"] == "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
            "CCL toy control missed low-excess terminal")
    require(ccl["selected_union_size"] == redundancy,
            "CCL toy union should hit the independent boundary")
    require(ccl["selected_union_excess"] == 0,
            "CCL toy excess drift")
    require(ccl["owner_cap"] == j_bound + 1,
            "CCL toy independent-union cap drift")
    ccl_errors = [
        vadd(
            [entry % modulus for entry in a_word],
            vscale(slope, b_word, modulus),
            modulus,
        )
        for slope in slopes
    ]
    ccl_union = {
        index
        for error in ccl_errors
        for index, entry in enumerate(error)
        if entry % modulus
    }
    ccl_all_defects_zero = all(
        not any(
            entry % modulus
            for entry in defect(slopes, [zero[:] for _ in slopes], triple,
                                modulus)
        )
        for triple in itertools.combinations(range(len(slopes)), 3)
    )
    require(ccl_all_defects_zero, "CCL toy defect identity drift")
    require(len(ccl_union) == redundancy, "CCL toy union identity drift")

    minimum_word = [
        (x * (x - 1) * (x - 2)) % modulus
        for x in domain
    ]
    support = [index for index, value in enumerate(minimum_word) if value]
    require(len(support) == redundancy + 1, "toy minimum word weight drift")
    f_word = [0, 0, 0, 2, 10, 3, 2, 4]
    g_word = [0, 0, 0, 0, 14, 1, 4, 0]
    decoder_scalars = [6, 6, 10, 12]
    codewords = [
        vscale(scalar, minimum_word, modulus)
        for scalar in decoder_scalars
    ]
    tdd = classify_selected_family(
        modulus=modulus,
        domain=domain,
        dimension=dimension,
        j_bound=j_bound,
        max_paid_excess=0,
        actual_noncontained_witnesses=True,
        transversality_certified=True,
        slopes=slopes,
        f_word=f_word,
        g_word=g_word,
        codewords=codewords,
    )
    require(tdd["terminal"] == "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
            "TDD toy control missed terminal")
    require(tdd["defect_weight"] == redundancy + 1,
            "TDD toy defect should have minimum weight")
    require(tdd["triple_union_size"] == redundancy + 1,
            "TDD toy triple union should be sharp")

    positive_excess_owner = classify_selected_family(
        modulus=modulus,
        domain=domain,
        dimension=dimension,
        j_bound=j_bound,
        max_paid_excess=1,
        actual_noncontained_witnesses=True,
        transversality_certified=True,
        slopes=slopes,
        f_word=f_word,
        g_word=g_word,
        codewords=codewords,
    )
    require(
        positive_excess_owner["terminal"]
        == "CERTIFIED_LOW_EXCESS_COMMON_CARRIER"
        and positive_excess_owner["selected_union_excess"] == 1
        and positive_excess_owner["owner"]
        == "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT"
        and positive_excess_owner["owner_cap"] == 10,
        "positive-excess transverse-secant toy control drift",
    )

    small = classify_selected_family(
        modulus=modulus,
        domain=domain,
        dimension=dimension,
        j_bound=j_bound,
        max_paid_excess=0,
        actual_noncontained_witnesses=True,
        transversality_certified=True,
        slopes=slopes[:3],
        f_word=f_word,
        g_word=g_word,
        codewords=codewords[:3],
    )
    require(small["terminal"] == "CERTIFIED_HIGH_UNION_SMALL_FAMILY",
            "small-family control missed first-match terminal")

    duplicate_rejected = False
    try:
        classify_selected_family(
            modulus=modulus,
            domain=domain,
            dimension=dimension,
            j_bound=j_bound,
            max_paid_excess=0,
            actual_noncontained_witnesses=True,
            transversality_certified=True,
            slopes=[0, 1, 1, 3],
            f_word=[entry % modulus for entry in a_word],
            g_word=b_word,
            codewords=[zero[:] for _ in slopes],
        )
    except VerificationError:
        duplicate_rejected = True
    require(duplicate_rejected, "duplicate-slope toy mutation accepted")

    non_codeword_rejected = False
    bad_codewords = [zero[:] for _ in slopes]
    bad_codewords[0][-1] = 1
    try:
        classify_selected_family(
            modulus=modulus,
            domain=domain,
            dimension=dimension,
            j_bound=j_bound,
            max_paid_excess=0,
            actual_noncontained_witnesses=True,
            transversality_certified=True,
            slopes=slopes,
            f_word=[entry % modulus for entry in a_word],
            g_word=b_word,
            codewords=bad_codewords,
        )
    except VerificationError:
        non_codeword_rejected = True
    require(non_codeword_rejected, "non-codeword toy mutation accepted")

    overweight_rejected = False
    overweight_f = [1, 1, 1, 1, 0, 0, 0, 0]
    try:
        classify_selected_family(
            modulus=modulus,
            domain=domain,
            dimension=dimension,
            j_bound=j_bound,
            max_paid_excess=0,
            actual_noncontained_witnesses=True,
            transversality_certified=True,
            slopes=slopes,
            f_word=overweight_f,
            g_word=zero,
            codewords=[zero[:] for _ in slopes],
        )
    except VerificationError:
        overweight_rejected = True
    require(overweight_rejected, "overweight-error toy mutation accepted")

    noncontained_contract_rejected = False
    try:
        classify_selected_family(
            modulus=modulus,
            domain=domain,
            dimension=dimension,
            j_bound=j_bound,
            max_paid_excess=0,
            actual_noncontained_witnesses=False,
            transversality_certified=True,
            slopes=slopes,
            f_word=[entry % modulus for entry in a_word],
            g_word=b_word,
            codewords=[zero[:] for _ in slopes],
        )
    except VerificationError:
        noncontained_contract_rejected = True
    require(
        noncontained_contract_rejected,
        "missing noncontained-witness contract accepted",
    )

    transversality_contract_rejected = False
    try:
        classify_selected_family(
            modulus=modulus,
            domain=domain,
            dimension=dimension,
            j_bound=j_bound,
            max_paid_excess=0,
            actual_noncontained_witnesses=True,
            transversality_certified=False,
            slopes=slopes,
            f_word=[entry % modulus for entry in a_word],
            g_word=b_word,
            codewords=[zero[:] for _ in slopes],
        )
    except VerificationError:
        transversality_contract_rejected = True
    require(
        transversality_contract_rejected,
        "missing transversality contract accepted",
    )

    return {
        "field": "F_17",
        "domain_size": len(domain),
        "dimension": dimension,
        "redundancy": redundancy,
        "j_bound": j_bound,
        "threshold_m0": 4,
        "ccl_control": ccl,
        "ccl_identity_control": {
            "all_triple_defects_zero": ccl_all_defects_zero,
            "selected_union_size": len(ccl_union),
            "cancellation_bound": (
                len(slopes) * j_bound // (len(slopes) - 1)
            ),
        },
        "tdd_control": tdd,
        "positive_excess_owner_control": positive_excess_owner,
        "small_first_match_control": small,
        "duplicate_slope_mutation_rejected": duplicate_rejected,
        "non_codeword_mutation_rejected": non_codeword_rejected,
        "overweight_error_mutation_rejected": overweight_rejected,
        "missing_noncontained_witness_contract_rejected": (
            noncontained_contract_rejected
        ),
        "missing_transversality_contract_rejected": (
            transversality_contract_rejected
        ),
        "scope": "EXACT_FINITE_FIELD_CONTROL_NOT_DEPLOYED_PROOF",
    }


def expected_sources() -> list[dict[str, str]]:
    return [
        source_binding("packet-note", NOTE_REL, "statement and proof"),
        source_binding("packet-readme", README_REL, "replay contract"),
        source_binding("packet-verifier", VERIFIER_REL, "certificate verifier"),
        source_binding("branch2-note", BRANCH2_NOTE_REL,
                       "actual-support rank bridge and prior owner"),
        source_binding("branch2-certificate", BRANCH2_CERT_REL,
                       "prior charge and branch interface"),
        source_binding("branch2-verifier", BRANCH2_VERIFIER_REL,
                       "predecessor replay"),
        source_binding("carrier-note", CARRIER_NOTE_REL,
                       "actual-witness transversality and kappa-zero owner"),
        source_binding("carrier-certificate", CARRIER_CERT_REL,
                       "predecessor branch-3 scope"),
        source_binding("carrier-verifier", CARRIER_VERIFIER_REL,
                       "predecessor replay"),
        source_binding("paper-d-v12", PAPER_D_REL, "deep-MCA theorem"),
        source_binding("exact-thresholds", THRESHOLDS_REL,
                       "exact deep numerator and independent-union theorem"),
        source_binding("ccl-tdd-predecessor", CCL_TDD_SOURCE_REL,
                       "generic affine defect algebra"),
        source_binding("first-match-certificate", FIRST_MATCH_CERT_REL,
                       "frozen branch order"),
        source_binding("post-c5-certificate", POST_C5_CERT_REL,
                       "open branch-3 source status"),
    ]


def expected_artifact() -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_sources(),
        "row": {
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "q_line": str(Q_LINE),
            "n": N,
            "k": K,
            "R": R,
            "A": A,
            "j": J,
            "t": T,
            "minimum_distance": MIN_DISTANCE,
            "B_star": str(B_STAR),
        },
        "branch_scope": {
            "v2_order": V2_ORDER,
            "branch_index_one_based": 3,
            "frozen_branch_label": "tangent_common_line_residue",
            "predecessor_branch2_closed": True,
            "literal_branch3_subset_of_full_row_rank_envelope": True,
            "monotone_under_earlier_first_match_deletion": True,
            "branch1_projector_complete": False,
            "global_mask_replay_complete": False,
            "branch3_closed": False,
        },
        "deep_owner_extension": {
            "owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
            "source_theorem": "tex/cs25_cap_v12.tex#thm:deep-mca",
            "exact_numerator_source": (
                "experimental/rs_mca_thresholds.tex#"
                "cor:exact-deep-numerator"
            ),
            "r_star_formula": "floor((n-k)/3)",
            "r_star": R_STAR,
            "deep_agreement": A_STAR,
            "gate_lhs_three_r_star": 3 * R_STAR,
            "gate_rhs_n_minus_k": R,
            "gate_holds": 3 * R_STAR <= R,
            "membership": (
                "exists declared exact-A noncontained witness with "
                "|E_gamma|<=r_star"
            ),
            "full_agreement_support": "D_MINUS_E_gamma",
            "original_support_subset_of_full_agreement_support": True,
            "noncontainment_persists_upward": True,
            "upper_bound_formula": "r_star+1",
            "composite_upper_bound": DEEP_COMPOSITE_CAP,
            "prior_branch2_error_cap": RANK_DROP_ERROR_CAP,
            "prior_branch2_charge": BRANCH2_CHARGE,
            "prior_branch2_subset_of_extended_owner": True,
            "increment_formula": (
                "composite_upper_bound-prior_branch2_charge"
            ),
            "incremental_charge": DEEP_INCREMENT,
            "increment_is_standalone_branch3_cap": False,
            "scope": "COMPOSITE_FIRST_MATCH_GLOBAL_ONCE",
            "ambient_deep_cap_sharp": True,
            "literal_composite_cap_sharp_proved": False,
            "ambient_sharpness_source": (
                "experimental/rs_mca_thresholds.tex#"
                "prop:universal-tangent-floor at agreement n-r_star"
            ),
        },
        "heavy_residual": {
            "intrinsic_deletion": (
                "remove every slope admitting any declared witness "
                "with |E_gamma|<=r_star"
            ),
            "selected_witness_quantifier": "arbitrary valid witness per survivor",
            "actual_error_weight_lower_bound": R_STAR + 1,
            "actual_error_weight_upper_bound": J,
            "padded_co_support_used": False,
            "finite_distinct_slopes": True,
        },
        "ccl_tdd_dichotomy": {
            "defect_formula": (
                "Delta_ijk=(gamma_j-gamma_k)c_i+"
                "(gamma_k-gamma_i)c_j+(gamma_i-gamma_j)c_k"
            ),
            "defect_in_code": True,
            "defect_support_subset_of_triple_error_union": True,
            "nonzero_defect_minimum_weight": MIN_DISTANCE,
            "selected_union_owner_checked_first": True,
            "maximum_paid_selected_union_excess": MAX_PAID_EXCESS,
            "maximum_paid_selected_union_cap": str(B10),
            "first_unpaid_selected_union_excess": MAX_PAID_EXCESS + 1,
            "first_unpaid_selected_union_cap": str(B11),
            "maximum_paid_cap_fits_post_delta_budget": (
                B10 <= B_REMAINING_AFTER
            ),
            "first_unpaid_cap_exceeds_post_delta_budget": (
                B11 > B_REMAINING_AFTER
            ),
            "high_union_minimum_size": R + MAX_PAID_EXCESS + 1,
            "tdd_terminal": "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
            "tdd_paid": False,
            "all_defects_zero_implies_affine_code_line": True,
            "residual_formula": "e_i=(f-p)+gamma_i(g-q)",
            "one_coordinate_cancels_for_at_most_one_finite_slope": True,
            "carrier_bound_formula": "floor(m*j/(m-1))",
            "threshold_formula": "ceil(R/(R-j))=ceil(R/t)",
            "threshold_m0": M0,
            "small_family_cap": SMALL_CAP,
            "carrier_bound_at_m0": M16_CARRIER_CAP,
            "carrier_bound_at_m0_minus_1": M15_CARRIER_CAP,
            "m0_forces_carrier_at_most_R": M16_CARRIER_CAP <= R,
            "m0_minus_1_does_not_force_carrier_at_most_R": (
                M15_CARRIER_CAP > R
            ),
            "common_carrier_excess": 0,
            "common_line_owner": "INDEPENDENT_UNION_RAYS",
            "common_line_cap": CCL_CAP,
            "common_line_routes_back_to_selected_union_owner": True,
            "common_line_charge_banked": False,
            "first_match_terminals": [
                "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
                "CERTIFIED_HIGH_UNION_SMALL_FAMILY_15",
                "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
            ],
        },
        "toy_controls": toy_controls(),
        "classifier_contract": {
            "deployed_family_enumerated": False,
            "symbolic_dichotomy_proved": True,
            "requires_actual_decoder_codewords": True,
            "requires_declared_actual_noncontained_witnesses": True,
            "requires_certified_syndrome_transversality": True,
            "missing_witness_or_transversality_fails_closed": True,
            "selected_union_carrier_terminal_checked_first": True,
            "small_terminal_checked_before_tdd": True,
            "duplicate_slopes_rejected": True,
            "non_codewords_rejected": True,
            "overweight_errors_rejected": True,
            "tdd_requires_nonzero_defect": True,
            "failure_to_pay_tdd": (
                "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT"
            ),
        },
        "charges": [
            {
                "charge_id": "kb-branch3-deep-owner-extension",
                "owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
                "amount": str(DEEP_INCREMENT),
                "scope": "COMPOSITE_FIRST_MATCH_GLOBAL_ONCE_INCREMENT",
                "prior_allocated_amount": str(BRANCH2_CHARGE),
                "resulting_composite_cap": str(DEEP_COMPOSITE_CAP),
                "standalone_branch3_cap": False,
                "owner_derivation_binding_ids": [
                    "packet-note",
                    "branch2-note",
                    "paper-d-v12",
                    "exact-thresholds",
                ],
            }
        ],
        "ledger": {
            "U_paid_before": str(U_PAID_BEFORE),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "deep_owner_increment": str(DEEP_INCREMENT),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "K_rem": K_REM,
            "ledger_consequence": True,
            "carrier_alternative_charge": None,
            "small_family_alternative_charge": None,
            "tdd_charge": None,
            "branch3_closed": False,
            "U_2": None,
            "U_Q": None,
            "U_A": None,
            "lhs": None,
            "row_complete": False,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
            "next_attack": "UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT",
        },
        "audit_sections": {
            "parameter_dependence": (
                "UNIFORM_RS_WITNESS_LIFT_AND_CCL_TDD_"
                "PRINTED_ARITHMETIC_KOALABEAR_SPECIFIC"
            ),
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "numerical_evidence": (
                "EXACT_INTEGER_AND_FINITE_FIELD_CONTROLS_"
                "NOT_USED_AS_DEPLOYED_PROOF"
            ),
            "edge_cases": EDGE_CASES,
            "remaining_risks": REMAINING_RISKS,
        },
        "nonclaims": NONCLAIMS,
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_source_interfaces() -> None:
    paper_d = (ROOT / PAPER_D_REL).read_text(encoding="utf-8")
    for anchor in (
        r"\label{thm:deep-mca}",
        r"3r\ \le\ w-1",
        r"\emca(C,\delta)\ \le\ \frac{r+1}q",
        r"For $C=\RS[\F,D,k]$",
    ):
        require(anchor in paper_d, f"Paper D anchor missing: {anchor}")

    thresholds = (ROOT / THRESHOLDS_REL).read_text(encoding="utf-8")
    for anchor in (
        r"\label{lem:independent-union-rays}",
        r"\label{prop:universal-tangent-floor}",
        r"\label{cor:exact-deep-numerator}",
        r"3(n-a)\le n-k",
    ):
        require(anchor in thresholds, f"threshold anchor missing: {anchor}")

    ccl_source = (ROOT / CCL_TDD_SOURCE_REL).read_text(encoding="utf-8")
    for anchor in (
        "Delta_ijk",
        "supp(Delta_ijk) subset E_i union E_j union E_k",
        "all seven decoded words lie on one affine RS",
        "coordinate of `W` can cancel for at most one",
    ):
        require(anchor in ccl_source, f"CCL/TDD source anchor missing: {anchor}")

    branch2 = load_json(ROOT / BRANCH2_CERT_REL)
    require(
        branch2["deep_mca_owner"]["upper_bound"] == BRANCH2_CHARGE,
        "branch-2 prior charge drift",
    )
    require(
        branch2["exact_support_rank_bridge"]["rank_drop_error_weight_cap"]
        == RANK_DROP_ERROR_CAP,
        "branch-2 error cap drift",
    )
    require(
        branch2["ledger"]["U_paid_after"] == str(U_PAID_BEFORE),
        "branch-2 ledger baseline drift",
    )
    require(branch2["ledger"]["branch2_closed"] is True,
            "branch-2 closure drift")

    carrier = load_json(ROOT / CARRIER_CERT_REL)
    require(
        carrier["branch3_scope"]["frozen_branch_label"]
        == "tangent_common_line_residue",
        "carrier branch label drift",
    )
    require(
        carrier["carrier_dichotomy"]["kappa_zero_owner"]
        == "INDEPENDENT_UNION_RAYS"
        and carrier["carrier_dichotomy"]["kappa_zero_cap_formula"] == "j+1"
        and carrier["budget_table"]["records"][0]["cap"] == str(CCL_CAP),
        "carrier kappa-zero cap drift",
    )
    require(
        carrier["budget_table"]["largest_budget_fitting_excess"]
        == MAX_PAID_EXCESS
        and carrier["budget_table"]["B_10"] == str(B10),
        "carrier excess-ten cutoff drift",
    )
    require(
        carrier["budget_table"]["first_budget_failing_excess"]
        == MAX_PAID_EXCESS + 1
        and carrier["budget_table"]["B_11"] == str(B11),
        "carrier excess-eleven cutoff drift",
    )
    require(
        carrier["ledger"]["U_paid_after"] == str(U_PAID_BEFORE),
        "carrier ledger baseline drift",
    )
    require(carrier["ledger"]["branch3_closed"] is False,
            "carrier branch-3 status drift")

    first_match = load_json(ROOT / FIRST_MATCH_CERT_REL)
    branch3 = first_match["first_match_branches"][2]
    require(
        branch3["order"] == 3
        and branch3["branch"] == "tangent_common_line_residue",
        "first-match branch-3 interface drift",
    )

    post_c5 = load_json(ROOT / POST_C5_CERT_REL)
    post_branch3 = post_c5["mask_inventory"]["records"][2]
    require(
        post_branch3["order"] == 3
        and post_branch3["branch"] == "tangent_common_line_residue"
        and post_branch3["actual_slope_projector_complete"] is False,
        "post-C5 branch-3 open status drift",
    )


def validate_arithmetic() -> None:
    require(R == N - K, "R arithmetic drift")
    require(J == N - A, "j arithmetic drift")
    require(T == A - K == R - J, "t arithmetic drift")
    require(R_STAR == 349_525, "r_star drift")
    require(3 * R_STAR == 1_048_575 <= R, "deep gate drift")
    require(A_STAR == 1_747_627, "deep agreement drift")
    require(DEEP_COMPOSITE_CAP == 349_526, "deep cap drift")
    require(BRANCH2_CHARGE == 67_472, "branch-2 charge drift")
    require(DEEP_INCREMENT == 282_054, "increment drift")
    require(M0 == 16, "CCL threshold drift")
    require(SMALL_CAP == 15, "small-family cap drift")
    require(M16_CARRIER_CAP == 1_046_510 < R,
            "m=16 carrier boundary drift")
    require(M15_CARRIER_CAP == 1_051_182 > R,
            "m=15 carrier boundary drift")
    require(MIN_DISTANCE == 1_048_577, "minimum distance drift")
    require(CCL_CAP == 981_105, "CCL cap drift")
    require(B10 == 78_289_526_705_722_101, "B10 drift")
    require(B11 == 1_115_145_741_750_273_207, "B11 drift")
    require(B_STAR == 274_980_728_111_395_087, "B_star drift")
    require(B_REMAINING_BEFORE == 274_980_725_509_174_142,
            "prior budget drift")
    require(U_PAID_AFTER == 2_602_502_999, "new U_paid drift")
    require(B_REMAINING_AFTER == 274_980_725_508_892_088,
            "new budget drift")
    require(B10 <= B_REMAINING_AFTER < B11,
            "post-delta excess 10/11 budget cutoff drift")
    require(exact_multiplier(B_REMAINING_AFTER) == K_REM,
            "exact K_rem drift")


def validate_artifact(artifact: dict[str, Any]) -> None:
    require(set(artifact) == TOP_KEYS, "top-level key drift")
    require(artifact["payload_sha256"] == payload_hash(artifact),
            "payload hash mismatch")
    expected = expected_artifact()
    require(
        canonical_bytes(artifact) == canonical_bytes(expected),
        "certificate content differs from exact expected artifact",
    )


def write_certificate() -> None:
    validate_source_interfaces()
    validate_arithmetic()
    artifact = expected_artifact()
    validate_artifact(artifact)
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(artifact, indent=2, sort_keys=False, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {CERT_PATH.relative_to(ROOT)}")


def check_certificate() -> dict[str, Any]:
    validate_source_interfaces()
    validate_arithmetic()
    controls = toy_controls()
    require(
        controls == expected_artifact()["toy_controls"],
        "toy controls are not deterministic",
    )
    artifact = load_json(CERT_PATH)
    validate_artifact(artifact)
    print("PASS m1-kb-branch3-deep-ccl-tdd-v1")
    print(
        "  deep composite cap / prior / increment: "
        f"{DEEP_COMPOSITE_CAP} / {BRANCH2_CHARGE} / {DEEP_INCREMENT}"
    )
    print(
        "  CCL threshold m0 / carrier bounds m0,m0-1: "
        f"{M0} / {M16_CARRIER_CAP} / {M15_CARRIER_CAP}"
    )
    print(
        "  ledger U_paid / B_remaining / K_rem: "
        f"{U_PAID_AFTER} / {B_REMAINING_AFTER} / {K_REM}"
    )
    print("  terminal residual: UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT")
    return artifact


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    current: Any = value
    for token in path[:-1]:
        current = current[token]
    current[path[-1]] = replacement


def tamper_selftest() -> None:
    artifact = check_certificate()
    mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("schema", ("schema",), SCHEMA + "-tampered"),
        ("status", ("status",), "GREEN_ROW_COMPLETE"),
        ("row-r", ("row", "R"), R - 1),
        ("row-j", ("row", "j"), J + 1),
        ("row-t", ("row", "t"), T - 1),
        ("distance", ("row", "minimum_distance"), MIN_DISTANCE - 1),
        ("branch-index", ("branch_scope", "branch_index_one_based"), 2),
        ("branch-closed", ("branch_scope", "branch3_closed"), True),
        (
            "deep-r-star",
            ("deep_owner_extension", "r_star"),
            R_STAR + 1,
        ),
        (
            "deep-gate",
            ("deep_owner_extension", "gate_holds"),
            False,
        ),
        (
            "deep-cap",
            ("deep_owner_extension", "composite_upper_bound"),
            DEEP_COMPOSITE_CAP - 1,
        ),
        (
            "prior-subset",
            ("deep_owner_extension", "prior_branch2_subset_of_extended_owner"),
            False,
        ),
        (
            "increment",
            ("deep_owner_extension", "incremental_charge"),
            DEEP_INCREMENT + 1,
        ),
        (
            "standalone-cap",
            ("deep_owner_extension", "increment_is_standalone_branch3_cap"),
            True,
        ),
        (
            "literal-sharpness",
            ("deep_owner_extension", "literal_composite_cap_sharp_proved"),
            True,
        ),
        (
            "heavy-lower",
            ("heavy_residual", "actual_error_weight_lower_bound"),
            R_STAR,
        ),
        (
            "padded-support",
            ("heavy_residual", "padded_co_support_used"),
            True,
        ),
        (
            "defect-in-code",
            ("ccl_tdd_dichotomy", "defect_in_code"),
            False,
        ),
        (
            "tdd-paid",
            ("ccl_tdd_dichotomy", "tdd_paid"),
            True,
        ),
        (
            "carrier-first",
            ("ccl_tdd_dichotomy", "selected_union_owner_checked_first"),
            False,
        ),
        (
            "carrier-cutoff",
            ("ccl_tdd_dichotomy", "maximum_paid_selected_union_excess"),
            MAX_PAID_EXCESS + 1,
        ),
        (
            "carrier-b11",
            ("ccl_tdd_dichotomy", "first_unpaid_selected_union_cap"),
            str(B11 - 1),
        ),
        (
            "carrier-post-budget",
            (
                "ccl_tdd_dichotomy",
                "maximum_paid_cap_fits_post_delta_budget",
            ),
            False,
        ),
        (
            "threshold",
            ("ccl_tdd_dichotomy", "threshold_m0"),
            15,
        ),
        (
            "small-cap",
            ("ccl_tdd_dichotomy", "small_family_cap"),
            16,
        ),
        (
            "m16-bound",
            ("ccl_tdd_dichotomy", "carrier_bound_at_m0"),
            R + 1,
        ),
        (
            "m15-bound",
            ("ccl_tdd_dichotomy", "carrier_bound_at_m0_minus_1"),
            R,
        ),
        (
            "ccl-excess",
            ("ccl_tdd_dichotomy", "common_carrier_excess"),
            1,
        ),
        (
            "ccl-charge",
            ("ccl_tdd_dichotomy", "common_line_charge_banked"),
            True,
        ),
        (
            "toy-terminal",
            ("toy_controls", "tdd_control", "terminal"),
            "PAID_TDD",
        ),
        (
            "toy-union",
            ("toy_controls", "tdd_control", "triple_union_size"),
            4,
        ),
        (
            "toy-positive-owner",
            ("toy_controls", "positive_excess_owner_control", "owner_cap"),
            9,
        ),
        (
            "classifier-enumerated",
            ("classifier_contract", "deployed_family_enumerated"),
            True,
        ),
        (
            "classifier-noncontained-contract",
            (
                "classifier_contract",
                "requires_declared_actual_noncontained_witnesses",
            ),
            False,
        ),
        (
            "classifier-transversality-contract",
            (
                "classifier_contract",
                "requires_certified_syndrome_transversality",
            ),
            False,
        ),
        (
            "classifier-small-order",
            ("classifier_contract", "small_terminal_checked_before_tdd"),
            False,
        ),
        (
            "charge-amount",
            ("charges", 0, "amount"),
            str(DEEP_INCREMENT + 1),
        ),
        (
            "charge-standalone",
            ("charges", 0, "standalone_branch3_cap"),
            True,
        ),
        (
            "ledger-u-paid",
            ("ledger", "U_paid_after"),
            str(U_PAID_AFTER + 1),
        ),
        (
            "ledger-budget",
            ("ledger", "B_remaining_after"),
            str(B_REMAINING_AFTER - 1),
        ),
        ("ledger-k-rem", ("ledger", "K_rem"), K_REM - 1),
        (
            "ledger-carrier-charge",
            ("ledger", "carrier_alternative_charge"),
            str(B10),
        ),
        (
            "ledger-small-charge",
            ("ledger", "small_family_alternative_charge"),
            str(SMALL_CAP),
        ),
        ("ledger-tdd-charge", ("ledger", "tdd_charge"), "1"),
        ("ledger-row-complete", ("ledger", "row_complete"), True),
        (
            "next-attack",
            ("ledger", "next_attack"),
            "DEGREE_THREE",
        ),
        (
            "audit-layer-cake",
            ("audit_sections", "layer_cake_dyadic_summability"),
            "APPLICABLE",
        ),
        (
            "nonclaim-row-safe",
            ("nonclaims", 0),
            "This packet proves the KoalaBear row safe.",
        ),
    ]

    rejected = 0
    for label, path, replacement in mutations:
        mutated = copy.deepcopy(artifact)
        set_path(mutated, path, replacement)
        mutated["payload_sha256"] = payload_hash(mutated)
        try:
            validate_artifact(mutated)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {label}")

    bad_hash = copy.deepcopy(artifact)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        validate_artifact(bad_hash)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("bad payload hash accepted")

    for label, text in (
        ("duplicate-key", '{"a":1,"a":2}'),
        ("nan-constant", '{"a":NaN}'),
    ):
        try:
            parse_json(text, label)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"invalid JSON accepted: {label}")

    expected_rejections = len(mutations) + 3
    require(rejected == expected_rejections, "tamper rejection count drift")
    print(f"TAMPER PASS {rejected}/{expected_rejections} rejected")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.write:
            write_certificate()
        elif args.tamper_selftest:
            tamper_selftest()
        else:
            check_certificate()
    except (VerificationError, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
