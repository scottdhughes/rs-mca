#!/usr/bin/env sage
"""Exact GF(19) fixed-syndrome census for the ``(3,2,3,(2,2,1))`` row.

For the retained background locator ``R`` of degree two, missed-core locator
``F`` of degree three, and labelled selected-petal locators of degrees
``(2,2,1)`` in some order, the divided equations are

    R*V - c_i*F = B_i*A_i,

with ``deg(V)<=1`` and ``deg(A_i)<=3-deg(B_i)``.  Thus the fixed-``F``
matrix is ``12 x 9``.  Adjoining the three lower coefficients of a monic cubic
gives a square ``12 x 12`` moving-``F`` system.

Writing ``B=B_1*B_2*B_3`` and

    G = c_i*R^(-1) mod B_i,

the three left-kernel compatibility equations are precisely the coefficients
of degrees 2, 3, and 4 in ``F*G mod B``.  The script derives this reduced
``3 x 3`` affine map symbolically, checks the rank relation on all 432 frozen
GF(19) support patterns, enumerates every compatible affine fibre, tests all
four actual missed-core locators, and independently replays the full decoder.

This is an exact finite control and a frozen symbolic statement.  The uniform
rank-drop implication is written separately and still requires a fresh proof
review before it can change the ledger.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

from sage.all import GF, QQ, PolynomialRing, matrix, vector


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "experimental/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    img_list,
    subgroup,
    sunflower_word_from_blocks,
)


CERTIFICATE_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-frontier-32221/certificate.json"
)
OWNER_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-32221-owner-partition/certificate.json"
)

P = 19
N = 18
K = 5
SIGMA = 3
CORE = tuple(range(4))
PETALS = (
    tuple(range(4, 8)),
    tuple(range(8, 12)),
    tuple(range(12, 16)),
)
BACKGROUND = tuple(range(16, 18))
LABELS = (1, 2, 3)


def sha256_json(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=int
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def locator(PX, X, field, domain, indices):
    output = PX.one()
    for index in indices:
        output *= X - field(domain[index])
    return output


def agreement_mask(poly, values, domain, field):
    mask = 0
    for index, point in enumerate(domain):
        if int(poly(field(point))) == int(values[index]):
            mask |= 1 << index
    return mask


def agreement_profile(mask):
    agreement = {index for index in range(N) if mask & (1 << index)}
    return {
        "d": len(set(CORE) - agreement),
        "r": len(set(BACKGROUND) & agreement),
        "a_i": sorted(
            [
                len(set(petal) & agreement)
                for petal in PETALS
                if set(petal) & agreement
            ],
            reverse=True,
        ),
        "agreement_size": len(agreement),
    }


def canonical_assignment(background_support, supports):
    return [list(background_support), *[list(support) for support in supports]]


def pattern_id(background_support, supports):
    occupancies = tuple(len(support) for support in supports)
    short_petal = occupancies.index(1)
    return (
        f"short{short_petal}-b16.17-"
        + "-".join("s" + ".".join(map(str, support)) for support in supports)
    )


def support_assignments():
    for short_petal in range(len(PETALS)):
        occupancies = tuple(
            1 if index == short_petal else 2 for index in range(len(PETALS))
        )
        support_choices = [
            tuple(itertools.combinations(petal, occupancy))
            for petal, occupancy in zip(PETALS, occupancies, strict=True)
        ]
        for supports in itertools.product(*support_choices):
            yield BACKGROUND, tuple(supports)


def coefficient_matrix(PX, X, field, R, support_locators):
    """Return the 12 x 9 fixed-F coefficient matrix."""
    v_columns = [R * X**degree for degree in range(2)]
    a_degrees = [3 - locator_poly.degree() for locator_poly in support_locators]
    offsets = []
    column_count = len(v_columns)
    for degree_bound in a_degrees:
        offsets.append(column_count)
        column_count += degree_bound + 1
    if column_count != 9:
        raise RuntimeError(f"expected nine fixed columns, found {column_count}")

    rows = []
    for block, (support_locator, degree_bound) in enumerate(
        zip(support_locators, a_degrees, strict=True)
    ):
        active = [PX.zero()] * column_count
        for degree in range(2):
            active[degree] = v_columns[degree]
        for degree in range(degree_bound + 1):
            active[offsets[block] + degree] = -support_locator * X**degree
        for coefficient_degree in range(4):
            rows.append([poly[coefficient_degree] for poly in active])
    return matrix(field, rows), a_degrees


def fixed_rhs(field, F):
    return vector(
        field,
        [field(label) * F[degree] for label in LABELS for degree in range(4)],
    )


def moving_monic_system(A, field):
    rows = []
    rhs = []
    for block, label in enumerate(LABELS):
        for degree in range(4):
            row = list(A.row(4 * block + degree))
            row.extend(
                -field(label) if degree == lower_degree else field.zero()
                for lower_degree in range(3)
            )
            rows.append(row)
            rhs.append(field(label) if degree == 3 else field.zero())
    return matrix(field, rows), vector(field, rhs)


def crt_unit(PX, support_locators, R, field):
    B = PX.one()
    for support_locator in support_locators:
        B *= support_locator
    G = PX.zero()
    for label, support_locator in zip(LABELS, support_locators, strict=True):
        complement = B // support_locator
        projector = complement * complement.inverse_mod(support_locator)
        residue = field(label) * R.inverse_mod(support_locator)
        G += residue * projector
    return B, G.mod(B)


def reduced_affine_map(PX, X, field, B, G):
    degrees = (2, 3, 4)
    columns = []
    for lower_degree in range(3):
        remainder = (X**lower_degree * G).mod(B)
        columns.append([remainder[degree] for degree in degrees])
    M = matrix(field, 3, 3, lambda row, column: columns[column][row])
    monic_remainder = (X**3 * G).mod(B)
    u = vector(field, [monic_remainder[degree] for degree in degrees])
    return M, u


def affine_solutions(C, rhs, field, max_solutions=1000):
    rank_C = int(C.rank())
    rank_augmented = int(C.augment(rhs.column()).rank())
    if rank_C != rank_augmented:
        return rank_C, rank_augmented, []
    kernel_basis = C.right_kernel().basis()
    count = int(field.order()) ** len(kernel_basis)
    if count > max_solutions:
        raise RuntimeError(f"affine fibre too large: {count}")
    particular = C.solve_right(rhs)
    solutions = []
    for coefficients in itertools.product(
        range(int(field.order())), repeat=len(kernel_basis)
    ):
        solution = vector(field, particular)
        for coefficient, direction in zip(coefficients, kernel_basis, strict=True):
            solution += field(coefficient) * direction
        solutions.append(solution)
    return rank_C, rank_augmented, solutions


def symbolic_reduced_map():
    names = [f"b{i}" for i in range(5)]
    names += [f"g{i}" for i in range(5)]
    names += [f"f{i}" for i in range(3)]
    coefficients = PolynomialRing(QQ, names=names)
    generators = dict(zip(names, coefficients.gens(), strict=True))
    PX = PolynomialRing(coefficients, "Z")
    Z = PX.gen()
    b = [generators[f"b{i}"] for i in range(5)]
    g = [generators[f"g{i}"] for i in range(5)]
    f = [generators[f"f{i}"] for i in range(3)]
    B = Z**5 + sum(b[index] * Z**index for index in range(5))
    G = sum(g[index] * Z**index for index in range(5))
    F = Z**3 + sum(f[index] * Z**index for index in range(3))
    remainder = (F * G).mod(B)
    M = []
    u = []
    identity_verified = True
    substitutions = {variable: 0 for variable in f}
    for degree in (2, 3, 4):
        coefficient = remainder[degree]
        row = [coefficient.coefficient(variable) for variable in f]
        constant = coefficient.subs(substitutions)
        identity_verified &= coefficient == sum(
            row[index] * f[index] for index in range(3)
        ) + constant
        M.append([str(entry) for entry in row])
        u.append(str(constant))
    return {
        "B": "Z^5+b4*Z^4+b3*Z^3+b2*Z^2+b1*Z+b0",
        "G": "g4*Z^4+g3*Z^3+g2*Z^2+g1*Z+g0",
        "F": "Z^3+f2*Z^2+f1*Z+f0",
        "compatibility_degrees": [2, 3, 4],
        "M_rows_for_f0_f1_f2": M,
        "u": u,
        "affine_identity_verified": bool(identity_verified),
    }


def rankdrop_line_record(PX, X, solutions):
    points = []
    for solution in solutions:
        V = sum(solution[degree] * X**degree for degree in range(2))
        F = X**3 + sum(solution[9 + degree] * X**degree for degree in range(3))
        gcd_FV = F.gcd(V).monic()
        points.append(
            {
                "t": int(F[2]),
                "V_coefficients_low_to_high": [int(V[degree]) for degree in range(2)],
                "F_coefficients_low_to_high": [int(F[degree]) for degree in range(4)],
                "gcd_coefficients_low_to_high": [
                    int(gcd_FV[degree]) for degree in range(gcd_FV.degree() + 1)
                ],
                "gcd_degree": int(gcd_FV.degree()),
            }
        )
    points.sort(key=lambda row: row["t"])
    expected_t = list(range(P))
    parameterization_verified = (
        [row["t"] for row in points] == expected_t
        and all(
            row["V_coefficients_low_to_high"] == [(18 * row["t"]) % P, 18]
            and row["F_coefficients_low_to_high"]
            == [(16 * row["t"]) % P, 16, row["t"], 1]
            and row["gcd_coefficients_low_to_high"] == [row["t"], 1]
            for row in points
        )
    )
    quadratic = X**2 + 16
    return {
        "ambient_solution_count": len(points),
        "parameter": "t=f2 in GF(19)",
        "formula": {
            "V": "18*(X+t)",
            "F": "(X+t)*(X^2+16)",
            "gcd": "X+t",
        },
        "parameterization_verified": parameterization_verified,
        "quadratic_factor_irreducible_over_GF19": bool(quadratic.is_irreducible()),
        "points_sha256": sha256_json(points),
        "points": points,
    }


def build_report():
    field = GF(P)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    domain = subgroup(P, N)
    word = sunflower_word_from_blocks(
        P,
        N,
        K,
        K + SIGMA,
        list(CORE),
        [list(petal) for petal in PETALS],
        "sunflower-sequential-m3",
    )
    if word is None:
        raise RuntimeError("failed to construct the sequential sunflower")
    values = word["values"]
    core_locator = locator(PX, X, field, domain, CORE)
    actual_locators = {}
    for restored_core in CORE:
        missed_core = tuple(index for index in CORE if index != restored_core)
        F = locator(PX, X, field, domain, missed_core)
        H = core_locator // F
        actual_locators[tuple(int(F[degree]) for degree in range(4))] = (
            restored_core,
            missed_core,
            H,
        )

    fixed_rank_histogram = Counter()
    actual_locator_rank_histogram = Counter()
    moving_rank_histogram = Counter()
    reduced_rank_histogram = Counter()
    support_status_histogram = Counter()
    ambient_solution_total = 0
    valid_locator_solution_total = 0
    exact_target_occurrences = 0
    exact_target_words = {}
    compatible_rankdrop_templates = []
    transcript = []

    for background_support, supports in support_assignments():
        R = locator(PX, X, field, domain, background_support)
        support_locators = [
            locator(PX, X, field, domain, support) for support in supports
        ]
        A, a_degrees = coefficient_matrix(PX, X, field, R, support_locators)
        rank_A = int(A.rank())
        fixed_rank_histogram[str(rank_A)] += 1
        fixed_rows = []
        for F_key, (restored_core, missed_core, _H) in actual_locators.items():
            F = sum(field(F_key[degree]) * X**degree for degree in range(4))
            rhs_F = fixed_rhs(field, F)
            rank_augmented = int(A.augment(rhs_F.column()).rank())
            actual_locator_rank_histogram[
                f"rankA={rank_A},rankAug={rank_augmented}"
            ] += 1
            fixed_rows.append(
                {
                    "restored_core": restored_core,
                    "missed_core": list(missed_core),
                    "rank_augmented": rank_augmented,
                }
            )

        C, moving_rhs = moving_monic_system(A, field)
        rank_C, rank_C_augmented, solutions = affine_solutions(
            C, moving_rhs, field
        )
        moving_rank_histogram[
            f"rankC={rank_C},rankAug={rank_C_augmented}"
        ] += 1

        B, G = crt_unit(PX, support_locators, R, field)
        M, u = reduced_affine_map(PX, X, field, B, G)
        rank_M = int(M.rank())
        reduced_augmented = M.augment((-u).column())
        rank_M_augmented = int(reduced_augmented.rank())
        reduced_rank_histogram[
            f"rankM={rank_M},rankAug={rank_M_augmented}"
        ] += 1
        if rank_C != rank_A + rank_M:
            raise RuntimeError("moving/reduced rank relation failed")
        if rank_C_augmented != rank_A + rank_M_augmented:
            raise RuntimeError("augmented moving/reduced rank relation failed")

        ambient_solution_total += len(solutions)
        valid_in_pattern = 0
        exact_in_pattern = []
        for solution in solutions:
            V = sum(solution[degree] * X**degree for degree in range(2))
            F = X**3 + sum(
                solution[9 + degree] * X**degree for degree in range(3)
            )
            for block, (label, support_locator, degree_bound) in enumerate(
                zip(LABELS, support_locators, a_degrees, strict=True)
            ):
                offset = 2 + sum(a_degrees[index] + 1 for index in range(block))
                A_i = sum(
                    solution[offset + degree] * X**degree
                    for degree in range(degree_bound + 1)
                )
                if R * V - field(label) * F != support_locator * A_i:
                    raise RuntimeError("fixed-syndrome solution failed identity replay")
            if any((F * G).mod(B)[degree] != 0 for degree in (2, 3, 4)):
                raise RuntimeError("CRT compatibility replay failed")
            F_key = tuple(int(F[degree]) for degree in range(4))
            if F_key not in actual_locators:
                continue
            valid_in_pattern += 1
            valid_locator_solution_total += 1
            restored_core, missed_core, H = actual_locators[F_key]
            W = R * H * V
            mask = agreement_mask(W, values, domain, field)
            row = agreement_profile(mask)
            if row["d"] == 3 and row["r"] == 2 and row["a_i"] == [2, 2, 1]:
                exact_target_occurrences += 1
                evaluations = tuple(int(W(field(point))) for point in domain)
                record = {
                    "pattern_id": pattern_id(background_support, supports),
                    "background_support": list(background_support),
                    "petal_supports": [list(support) for support in supports],
                    "restored_core": restored_core,
                    "missed_core": list(missed_core),
                    "agreement_mask": int(mask),
                    "agreement_set": [
                        index for index in range(N) if mask & (1 << index)
                    ],
                    "V_coefficients_low_to_high": [
                        int(V[degree]) for degree in range(2)
                    ],
                    "F_coefficients_low_to_high": [
                        int(F[degree]) for degree in range(4)
                    ],
                }
                exact_in_pattern.append(record)
                exact_target_words.setdefault(evaluations, record)

        if rank_C < 12 and rank_C_augmented == rank_C:
            rankdrop_line = rankdrop_line_record(PX, X, solutions)
            compatible_rankdrop_templates.append(
                {
                    "pattern_id": pattern_id(background_support, supports),
                    "canonical_assignment": canonical_assignment(
                        background_support, supports
                    ),
                    "labelled_occupancies": [len(support) for support in supports],
                    "rank_A": rank_A,
                    "rank_C": rank_C,
                    "rank_C_augmented": rank_C_augmented,
                    "rank_M": rank_M,
                    "rank_M_augmented": rank_M_augmented,
                    "B_coefficients_low_to_high": [
                        int(B[degree]) for degree in range(6)
                    ],
                    "G_coefficients_low_to_high": [
                        int(G[degree]) for degree in range(5)
                    ],
                    "M": [[int(entry) for entry in row] for row in M.rows()],
                    "u": [int(entry) for entry in u],
                    "owner": "UNPAID_COMPATIBLE_RANKDROP_BEFORE_UNIFORM_LEMMA",
                    "affine_line": rankdrop_line,
                }
            )

        if not solutions:
            support_status = "ZERO_AFFINE_INCOMPATIBLE"
        elif exact_in_pattern:
            support_status = "REALIZES_EXACT_TARGET"
        else:
            support_status = "AMBIENT_ONLY_NO_EXACT_TARGET"
        support_status_histogram[support_status] += 1
        transcript.append(
            {
                "pattern_id": pattern_id(background_support, supports),
                "canonical_assignment": canonical_assignment(
                    background_support, supports
                ),
                "labelled_occupancies": [len(support) for support in supports],
                "rank_A": rank_A,
                "actual_locator_rows": fixed_rows,
                "rank_C": rank_C,
                "rank_C_augmented": rank_C_augmented,
                "rank_M": rank_M,
                "rank_M_augmented": rank_M_augmented,
                "ambient_solution_count": len(solutions),
                "valid_core_locator_solution_count": valid_in_pattern,
                "exact_target_solution_count": len(exact_in_pattern),
                "support_status": support_status,
            }
        )

    if len(transcript) != 432:
        raise RuntimeError(f"support-pattern count drift: {len(transcript)}")

    decoded = img_list(values, domain, K, K + SIGMA, P, "support")
    planted = {
        tuple(
            int((field(label) * core_locator)(field(point))) for point in domain
        )
        for label in LABELS
    }
    decoded_words = set(decoded)
    if not planted.issubset(decoded_words):
        raise RuntimeError("planted words missing from exact decoder")
    decoder_targets = []
    for codeword, mask in decoded.items():
        row = agreement_profile(mask)
        if row["d"] == 3 and row["r"] == 2 and row["a_i"] == [2, 2, 1]:
            decoder_targets.append(
                {
                    "codeword": list(map(int, codeword)),
                    "agreement_mask": int(mask),
                    "agreement_set": [
                        index for index in range(N) if mask & (1 << index)
                    ],
                }
            )
    if set(exact_target_words) != {
        tuple(int(value) for value in row["codeword"]) for row in decoder_targets
    }:
        raise RuntimeError("rank census and independent decoder target sets disagree")

    owner_link = json.loads(OWNER_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if owner_link["schema"] != "rs-mca-l1-b9-frontier-32221-owner-partition-v1":
        raise RuntimeError("owner certificate schema drift")
    owner_assignments = [row["canonical_assignment"] for row in owner_link["patterns"]]
    transcript_assignments = [row["canonical_assignment"] for row in transcript]
    if owner_assignments != transcript_assignments:
        raise RuntimeError("owner/census canonical assignment order drift")

    return {
        "schema": "rs-mca-l1-b9-frontier-32221-census-v1",
        "status": "EXPERIMENTAL/EXACT_FINITE_GF19_FIXED_SYNDROME_CENSUS",
        "statement": (
            "classify the fixed and moving cubic systems for all 432 support "
            "patterns in (ell,d,r,t,a_i)=(4,3,2,3,(2,2,1))"
        ),
        "input": {
            "p": P,
            "n": N,
            "k": K,
            "sigma": SIGMA,
            "ell": 4,
            "core": list(CORE),
            "petals": [list(petal) for petal in PETALS],
            "background": list(BACKGROUND),
            "labels": list(LABELS),
            "domain": list(map(int, domain)),
        },
        "frozen_system": {
            "equations": "R*V-c_i*F=B_i*A_i",
            "degrees": {
                "R": 2,
                "V_max": 1,
                "F_monic": 3,
                "B_i_sorted": [2, 2, 1],
                "A_i_max_for_B_i_sorted": [1, 1, 2],
            },
            "fixed_F_matrix_shape": [12, 9],
            "moving_monic_F_matrix_shape": [12, 12],
            "universal_fixed_rank": 9,
            "left_kernel_dimension": 3,
            "crt_modulus_degree": 5,
            "crt_compatibility_equations": (
                "coefficients X^2,X^3,X^4 of (F*G mod B) vanish, where "
                "B=B1*B2*B3 and G=c_i*R^(-1) mod B_i"
            ),
            "reduced_affine_map_shape": [3, 3],
            "rank_relation": "rank(C_12x12)=9+rank(M_3x3)",
            "augmented_rank_relation": (
                "rank([C|b])=9+rank([M|-u])"
            ),
            "symbolic_reduced_map": symbolic_reduced_map(),
        },
        "owner_certificate": {
            "path": str(OWNER_CERTIFICATE_PATH.relative_to(ROOT)),
            "sha256": hashlib.sha256(OWNER_CERTIFICATE_PATH.read_bytes()).hexdigest(),
        },
        "result": {
            "support_pattern_count": len(transcript),
            "fixed_matrix_rank_histogram": dict(sorted(fixed_rank_histogram.items())),
            "actual_locator_rank_histogram": dict(
                sorted(actual_locator_rank_histogram.items())
            ),
            "moving_rank_histogram": dict(sorted(moving_rank_histogram.items())),
            "reduced_rank_histogram": dict(sorted(reduced_rank_histogram.items())),
            "support_status_histogram": dict(
                sorted(support_status_histogram.items())
            ),
            "compatible_support_pattern_count": sum(
                row["ambient_solution_count"] > 0 for row in transcript
            ),
            "ambient_monic_cubic_solution_total": ambient_solution_total,
            "valid_core_locator_solution_occurrences": valid_locator_solution_total,
            "exact_target_solution_occurrences": exact_target_occurrences,
            "exact_target_codeword_count": len(exact_target_words),
            "independent_decoder_list_size": len(decoded),
            "independent_decoder_extra_count": len(decoded_words - planted),
            "independent_decoder_target_count": len(decoder_targets),
            "compatible_rankdrop_pattern_count": len(
                compatible_rankdrop_templates
            ),
            "transcript_sha256": sha256_json(transcript),
        },
        "compatible_rankdrop_templates": compatible_rankdrop_templates,
        "exact_target_words": list(exact_target_words.values()),
        "independent_decoder_targets": decoder_targets,
        "proof_status": {
            "exact_finite": [
                "all 432 canonical support patterns are checked",
                "all coefficient, moving, reduced, and augmented ranks are exact over GF(19)",
                "all compatible affine fibres are enumerated and identity-replayed",
                "all four actual missed-core locators are tested in every pattern",
                "the independent full decoder agrees on the exact target set",
                "the unique compatible ambient rank-drop line has a nonconstant gcd in all 19 points",
            ],
            "uniform_argument_to_review": [
                "the fixed-F 12x9 matrix has rank nine by coprime-locator divisibility",
                "a compatible moving rank drop gives a nonzero homogeneous direction",
                "the degree-five CRT modulus divides a cross-polynomial of degree at most four",
                "the resulting common factor migrates every actual split locator to d<=2",
            ],
        },
        "nonclaims": [
            "the exact finite census alone is not a uniform theorem",
            "ambient monic cubics need not be split missed-core locators",
            "no ledger payment is made before fresh independent review",
            "no m>2, PR #763, Lean, commit, or GitHub action is made",
        ],
        "verdict": (
            "YELLOW - the symbolic system and finite controls are frozen; "
            "the uniform rank-drop lemma still requires fresh review."
        ),
    }


def validate_report(report):
    result = report["result"]
    templates = report["compatible_rankdrop_templates"]
    symbolic = report["frozen_system"]["symbolic_reduced_map"]
    return (
        report["schema"] == "rs-mca-l1-b9-frontier-32221-census-v1"
        and report["frozen_system"]["fixed_F_matrix_shape"] == [12, 9]
        and report["frozen_system"]["moving_monic_F_matrix_shape"] == [12, 12]
        and report["frozen_system"]["reduced_affine_map_shape"] == [3, 3]
        and symbolic["compatibility_degrees"] == [2, 3, 4]
        and symbolic["affine_identity_verified"]
        and int(result["support_pattern_count"]) == 432
        and result["fixed_matrix_rank_histogram"] == {"9": 432}
        and result["actual_locator_rank_histogram"] == {
            "rankA=9,rankAug=10": 1_728
        }
        and result["moving_rank_histogram"]
        == {
            "rankC=11,rankAug=11": 1,
            "rankC=11,rankAug=12": 23,
            "rankC=12,rankAug=12": 408,
        }
        and result["reduced_rank_histogram"]
        == {
            "rankM=2,rankAug=2": 1,
            "rankM=2,rankAug=3": 23,
            "rankM=3,rankAug=3": 408,
        }
        and int(result["compatible_rankdrop_pattern_count"]) == 1
        and len(templates) == 1
        and templates[0]["canonical_assignment"]
        == [[16, 17], [5], [8, 11], [14, 15]]
        and templates[0]["affine_line"]["ambient_solution_count"] == 19
        and templates[0]["affine_line"]["parameterization_verified"]
        and templates[0]["affine_line"]["quadratic_factor_irreducible_over_GF19"]
        and int(result["ambient_monic_cubic_solution_total"]) == 427
        and int(result["valid_core_locator_solution_occurrences"]) == 0
        and int(result["exact_target_solution_occurrences"]) == 0
        and int(result["exact_target_codeword_count"]) == 0
        and int(result["independent_decoder_list_size"]) == 4
        and int(result["independent_decoder_target_count"]) == 0
        and not report["exact_target_words"]
        and not report["independent_decoder_targets"]
        and report["owner_certificate"]["sha256"]
        == hashlib.sha256(OWNER_CERTIFICATE_PATH.read_bytes()).hexdigest()
    )


def tamper_selftest(report):
    mutations = []
    changed = copy.deepcopy(report)
    changed["frozen_system"]["fixed_F_matrix_shape"] = [12, 8]
    mutations.append(("fixed_matrix_shape", changed))
    changed = copy.deepcopy(report)
    changed["frozen_system"]["symbolic_reduced_map"]["compatibility_degrees"] = [3, 4]
    mutations.append(("compatibility_degrees", changed))
    changed = copy.deepcopy(report)
    changed["result"]["moving_rank_histogram"]["rankC=12,rankAug=12"] -= 1
    mutations.append(("moving_rank_histogram", changed))
    changed = copy.deepcopy(report)
    changed["compatible_rankdrop_templates"][0]["affine_line"][
        "parameterization_verified"
    ] = False
    mutations.append(("rankdrop_factor", changed))
    changed = copy.deepcopy(report)
    changed["owner_certificate"]["sha256"] = "0" * 64
    mutations.append(("owner_link", changed))
    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<24}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))
    report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (internal fixed-syndrome validation)", file=sys.stderr)
        return 1
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True, default=int) + "\n",
            encoding="utf-8",
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, default=int))
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != report:
        print("RESULT: FAIL (frozen fixed-syndrome certificate drift)", file=sys.stderr)
        return 1
    result = report["result"]
    print("L1 B9 frontier (3,2,3,(2,2,1)) exact GF(19) fixed-syndrome census")
    print(f"  fixed-F matrix: {report['frozen_system']['fixed_F_matrix_shape']}")
    print(
        "  moving monic-F matrix: "
        f"{report['frozen_system']['moving_monic_F_matrix_shape']}"
    )
    print(
        "  CRT compatibility: "
        f"{report['frozen_system']['crt_compatibility_equations']}"
    )
    print(f"  support patterns: {result['support_pattern_count']}")
    print(f"  moving ranks: {result['moving_rank_histogram']}")
    print(f"  reduced ranks: {result['reduced_rank_histogram']}")
    print(
        "  exact targets: "
        f"rank={result['exact_target_codeword_count']}, "
        f"decoder={result['independent_decoder_target_count']}"
    )
    print(f"  transcript: {result['transcript_sha256']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(int(main(sys.argv[1:])))
