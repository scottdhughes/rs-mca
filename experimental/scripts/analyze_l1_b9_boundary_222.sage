#!/usr/bin/env sage
"""Exact algebra and finite censuses for the L1 B9-boundary ``(2,2,2)`` chart.

At ``m=2`` the profile is

    ell=d=4,  r=2,  t=3,  a_1=a_2=a_3=2.

Write ``F=L_D`` (monic quartic), let ``R`` be the quadratic
background locator, and let ``B_i`` be the three quadratic selected-support
locators.  The load-bearing fixed-support system is

    R V - B_i A_i = c_i F,                 i=1,2,3,

with ``deg(V),deg(A_i)<=2``.  It has 15 coefficient equations and 12
unknowns.  The 10-by-9 pairwise-difference system is recorded only as a
diagnostic because it omits the condition ``R | W``.

This script certifies four bounded claims:

* the fixed ``m=2`` profile lies exactly on B9 and has ``G2=GR=4``;
* the full homogeneous 15-by-12 system has rank 12 on the pairwise-coprime
  locator chart;
* after three-point interpolation, compatibility is three affine equations
  in the four lower coefficients of ``F``; a compatible coefficient-rank
  drop forces a degree-two complete-fibre quotient and recovers exactly two
  allegedly missed core points, so it cannot realize the exact ``d=4``
  profile;
* exhaustive structural censuses over GF(11) and GF(13), plus the exact
  ``(p,n,k,s)=(19,18,5,8)`` sequential RS fixture, agree with those claims.

The resulting ``m=2`` moving-support upper charge is certified: the rank-three
affine fibre contributes at most one factor of ``q`` per choice of background
and selected petal pairs.  The certificate does not prove domain-compatible
quotient descent, an asymptotic list bound, or the global mixed-petal theorem.
"""

from __future__ import annotations

import argparse
import builtins
import hashlib
import itertools
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

from sage.all import GF, QQ, PolynomialRing, matrix, vector
from sage.rings.integer import Integer as SageInteger


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experimental/scripts"))

from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    img_list,
    stabilizer_order,
    subgroup,
    sunflower_word_from_blocks,
)


CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-boundary-222/certificate.json"
)

EXPECTED_CENSUS = {
    11: {
        "total": 7560,
        "rank_histogram": {"1": 2, "2": 82, "3": 7476},
        "affine_rank_histogram": {
            "rankC=1,rankAug=2": 2,
            "rankC=2,rankAug=2": 18,
            "rankC=2,rankAug=3": 64,
            "rankC=3,rankAug=3": 7476,
        },
        "rank_involution_histogram": {
            "rankC=1,rankAug=2,backgroundInvolutionPairs=4": 2,
            "rankC=2,rankAug=2,backgroundInvolutionPairs=4": 18,
            "rankC=2,rankAug=3,backgroundInvolutionPairs=2": 12,
            "rankC=2,rankAug=3,backgroundInvolutionPairs=3": 52,
            "rankC=3,rankAug=3,backgroundInvolutionPairs=2": 5004,
            "rankC=3,rankAug=3,backgroundInvolutionPairs=3": 2324,
            "rankC=3,rankAug=3,backgroundInvolutionPairs=4": 148,
        },
    },
    13: {
        "total": 41580,
        "rank_histogram": {"1": 5, "2": 383, "3": 41192},
        "affine_rank_histogram": {
            "rankC=1,rankAug=2": 5,
            "rankC=2,rankAug=2": 49,
            "rankC=2,rankAug=3": 334,
            "rankC=3,rankAug=3": 41192,
        },
        "rank_involution_histogram": {
            "rankC=1,rankAug=2,backgroundInvolutionPairs=4": 5,
            "rankC=2,rankAug=2,backgroundInvolutionPairs=4": 49,
            "rankC=2,rankAug=3,backgroundInvolutionPairs=2": 172,
            "rankC=2,rankAug=3,backgroundInvolutionPairs=3": 162,
            "rankC=3,rankAug=3,backgroundInvolutionPairs=2": 29888,
            "rankC=3,rankAug=3,backgroundInvolutionPairs=3": 10818,
            "rankC=3,rankAug=3,backgroundInvolutionPairs=4": 486,
        },
    },
}

EXPECTED_RANK2_RECOVERY = {
    "split_compatible_locators": 24,
    "route_histogram": {"PROFILE_MIGRATION_CORE_RECOVERY": 24},
    "migrated_defect_histogram": {"2": 24},
    "exact_d4_survivors": 0,
}


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, SageInteger):
        return int(value)
    return value


def sha256_json(value):
    payload = json.dumps(json_ready(value), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def polynomial_fingerprint(poly):
    terms = []
    for exponent, coefficient in poly.dict().items():
        terms.append([list(map(int, exponent)), str(coefficient)])
    terms.sort()
    return {
        "total_degree": int(poly.total_degree()) if poly else -1,
        "term_count": len(terms),
        "sha256": sha256_json(terms),
    }


def exact_quotient(numerator, denominator, label):
    quotient, remainder = numerator.quo_rem(denominator)
    if remainder != 0:
        raise RuntimeError(f"non-exact structural division: {label}")
    return quotient


def profile_report():
    m = 2
    ell = d = 2 * m
    r = m
    t = 3
    a_i = [m, m, m]
    G2 = GR = ell
    lam = r + sum(a_i) - (ell + d)
    first_width = (ell + d - r + a_i[0] - 1) // a_i[0]
    second_width = 1 + (
        ell + d - r - a_i[0] + a_i[1] - 1
    ) // a_i[1]
    b9_left = 2 * max(0, d - ell + GR) + (t - 1) * G2
    b9_right = 2 * (t - 1) * ell
    K, M, b = 4, 3, 2
    n = K + 2 * m * M + b
    s = K + 2 * m
    auxiliary_a = 3 * m
    auxiliary_N = 2 * m * M
    return {
        "m2": {
            "ell": ell,
            "d": d,
            "r": r,
            "t": t,
            "a_i": a_i,
            "lambda": lam,
            "G2": G2,
            "GR": GR,
            "B8_widths": [first_width, second_width],
            "B9_left": b9_left,
            "B9_right": b9_right,
            "minimal_layout": {
                "K": K,
                "M": M,
                "b": b,
                "p": 19,
                "n": n,
                "k": K + 1,
                "s": s,
                "nK_minus_s2": n * K - s**2,
                "auxiliary_a": auxiliary_a,
                "auxiliary_N": auxiliary_N,
                "auxiliary_margin": auxiliary_a**2 - auxiliary_N * d,
            },
        },
    }


def coefficient_system_report():
    names = [
        "r1",
        "r0",
        "b11",
        "b10",
        "b21",
        "b20",
        "b31",
        "b30",
    ]
    S = PolynomialRing(QQ, names=names, order="degrevlex")
    g = S.gens_dict()
    PX = PolynomialRing(S, "X")
    X = PX.gen()
    R = X**2 + g["r1"] * X + g["r0"]
    B = [
        X**2 + g["b11"] * X + g["b10"],
        X**2 + g["b21"] * X + g["b20"],
        X**2 + g["b31"] * X + g["b30"],
    ]
    zero = PX.zero()

    full_rows = []
    for block, locator in enumerate(B):
        columns = [R * X**j for j in range(3)] + [zero] * 9
        offset = 3 + 3 * block
        for j in range(3):
            columns[offset + j] = -locator * X**j
        for degree in range(5):
            full_rows.append([column[degree] for column in columns])
    full_A = matrix(S, full_rows)

    pair_rows = []
    for block in (1, 2):
        columns = [zero] * 9
        for j in range(3):
            columns[j] = B[0] * X**j
            columns[3 * block + j] = -B[block] * X**j
        for degree in range(5):
            pair_rows.append([column[degree] for column in columns])
    pair_A = matrix(S, pair_rows)
    K = S.fraction_field()
    full_rank = matrix(K, full_A).rank()
    pair_rank = matrix(K, pair_A).rank()
    if full_rank != 12 or pair_rank != 9:
        raise RuntimeError("generic coefficient rank drift")

    return {
        "full_system": {
            "equations": 15,
            "unknowns": 12,
            "generic_rank": int(full_rank),
            "uniform_rank_proof": (
                "a homogeneous solution gives one polynomial H=RV=B_iA_i "
                "of degree at most 4; pairwise coprimality makes the degree-8 "
                "product R*B1*B2*B3 divide H, hence H=0"
            ),
            "structural_open_chart": (
                "R,B1,B2,B3 pairwise coprime; all locators split with distinct roots; "
                "the three petal labels are nonzero and distinct"
            ),
        },
        "pairwise_diagnostic": {
            "equations": 10,
            "unknowns": 9,
            "generic_rank": int(pair_rank),
            "uniform_rank_proof": (
                "B1*A1=B2*A2=B3*A3 has degree at most 4 but is divisible "
                "by the degree-6 product B1*B2*B3"
            ),
            "nonclaim": "this system omits R|W and is not load-bearing",
        },
    }


def symbolic_compatibility_report():
    names = [
        "rho1",
        "rho2",
        "x11",
        "x12",
        "x21",
        "x22",
        "x31",
        "x32",
        "f0",
        "f1",
        "f2",
        "f3",
    ]
    S = PolynomialRing(QQ, names=names, order="degrevlex")
    g = S.gens_dict()
    rho1, rho2 = g["rho1"], g["rho2"]
    points = [g[name] for name in ("x11", "x12", "x21", "x22", "x31", "x32")]
    f = [g[name] for name in ("f0", "f1", "f2", "f3")]
    labels = [1, 1, 2, 2, 3, 3]

    def R_at(z):
        return (z - rho1) * (z - rho2)

    def F_at(z):
        return z**4 + f[3] * z**3 + f[2] * z**2 + f[1] * z + f[0]

    rows = [
        [R_at(z), z * R_at(z), z**2 * R_at(z), labels[index] * F_at(z)]
        for index, z in enumerate(points)
    ]
    anchor_indices = [0, 1, 2]
    raw = []
    for row_index in (3, 4, 5):
        raw.append(matrix(S, [rows[i] for i in anchor_indices + [row_index]]).det())

    x11, x12, x21, x22, x31, x32 = points
    structural = [
        (x11 - x12) * (x21 - x22),
        x11 - x12,
        x11 - x12,
    ]
    residuals = [
        exact_quotient(poly, factor, f"anchor residual {index}")
        for index, (poly, factor) in enumerate(zip(raw, structural, strict=True))
    ]
    for residual in residuals:
        for left in f:
            for right in f:
                if residual.derivative(left).derivative(right) != 0:
                    raise RuntimeError("compatibility residual is not affine-linear in F")

    C = matrix(S, [[residual.derivative(coefficient) for coefficient in f] for residual in residuals])
    rank_minors = []
    common = (
        (x31 - x32)
        * (x11 - rho1) ** 2
        * (x12 - rho1) ** 2
        * (x11 - rho2) ** 2
        * (x12 - rho2) ** 2
        * (x21 - x11) ** 2
        * (x21 - x12) ** 2
        * (x21 - rho1) ** 2
        * (x21 - rho2) ** 2
    )
    for deleted in range(4):
        columns = [column for column in range(4) if column != deleted]
        minor = C.matrix_from_columns(columns).det()
        quotient = exact_quotient(minor, common, f"rank minor delete f{deleted}")
        if quotient == 0:
            raise RuntimeError("rank-drop residual vanished")
        rank_minors.append(
            {
                "deleted_coefficient": f"f{deleted}",
                "raw": polynomial_fingerprint(minor),
                "localized_residual": polynomial_fingerprint(quotient),
            }
        )

    anchor_det = matrix(
        S, [[rows[index][column] for column in range(3)] for index in anchor_indices]
    ).det()
    expected_anchor_det = (
        R_at(x11)
        * R_at(x12)
        * R_at(x21)
        * (x12 - x11)
        * (x21 - x11)
        * (x21 - x12)
    )
    if anchor_det != expected_anchor_det:
        raise RuntimeError("anchor Vandermonde identity drift")

    return {
        "evaluation_matrix": {
            "shape": [6, 4],
            "columns": ["R(z)", "zR(z)", "z^2R(z)", "c(z)F(z)"],
            "compatibility": "rank at most 3, equivalently all 4x4 minors vanish",
            "anchor_rows": ["x11", "x12", "x21"],
            "anchor_minor_identity": (
                "R(x11)R(x12)R(x21)(x12-x11)(x21-x11)(x21-x12)"
            ),
        },
        "anchor_residuals": [polynomial_fingerprint(poly) for poly in residuals],
        "coefficient_rank_matrix": {
            "shape": [3, 4],
            "generic_rank": 3,
            "localized_rank_drop_generators": rank_minors,
            "localization_statement": (
                "after inverting the displayed common structural factor, "
                "rank(C)<=2 is generated by the four localized residuals"
            ),
            "structural_factor": polynomial_fingerprint(common),
        },
        "low_rank_dichotomy": {
            "status": "RIGOROUS_LOCAL_LEMMA",
            "statement": (
                "on the disjoint split chart with pairwise-distinct nonzero petal labels, if "
                "rank(C)<=2 and a monic quartic "
                "F is compatible, then there are a nonzero constant a and a "
                "quadratic divisor B of F such that R*a-c_i*B vanishes on both "
                "roots of every support locator B_i; hence all four pairs are "
                "complete fibres of the degree-two map R*a/B"
            ),
            "proof_steps": [
                "rank(C)<=2 gives two independent kernel pairs (Q_j,G_j) with deg(Q_j)<=2 and deg(G_j)<=3",
                "Q1*G2-Q2*G1 has degree at most 5 and six support roots, so it is zero",
                "write every kernel pair as h*(A,B) with gcd(A,B)=1; the only possible base-point case has deg(A)=0, deg(B)<=1",
                "for the bad support set T and h_max=min(2-deg(A),3-deg(B)), dimension at least two gives 2<=h_max+1-|T|",
                "a compatible monic quartic makes V*B-A*F vanish at at least five roots in that base-point case, forcing an impossible degree comparison",
                "otherwise R*A=c_i*B at all six roots and V*B=A*F identically",
                "B divides F and deg(V)<=2 forces deg(A)=0 and deg(B)=2",
            ],
            "consequences": [
                "rank(C)=1 is affine-inconsistent for monic quartics",
                "every compatible rank(C)=2 stratum has a degree-two complete-fibre quotient template",
                "for an exact sunflower witness, compatible rank(C)=2 recovers exactly two roots of F inside the missed core and therefore exits the d=4 profile",
                "rank(C)=3 leaves an affine one-dimensional monic-F fibre",
            ],
            "exactness_boundary": (
                "write F=B*H and V=A*H as above.  Since W=R*V=A*R*H, "
                "gcd(F,W)=H has degree two on the disjoint split chart.  The "
                "sunflower word is zero on the core and P=L_(C\\D)*W, so the "
                "two roots of H are agreements, not missed-core points.  The "
                "canonical exact profile has F_new=B, W_new=A*R and d_new=2."
            ),
            "owner_boundary": (
                "quotient ownership is secondary on this exact m=2 component: "
                "the compatible rank-two chart has already migrated out of d=4.  "
                "For a non-exact or generalized chart, an arbitrary rational "
                "involution still is not a paid power/Chebyshev owner without the "
                "declared-domain and data-descent hypotheses"
            ),
            "characteristic_note": (
                "the complete-fibre conclusion is characteristic-free; when the "
                "degree-two rational map is separable, its nontrivial deck transformation "
                "is the corresponding PGL2 involution"
            ),
        },
    }


def inverse_mod(value, p):
    value %= p
    if value == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(value, p - 2, p)


def rank_mod(rows, p):
    work = [[entry % p for entry in row] for row in rows]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inverse_mod(work[rank][column], p)
        work[rank] = [(scale * entry) % p for entry in work[rank]]
        for index in range(len(work)):
            if index == rank or work[index][column] == 0:
                continue
            scale = work[index][column]
            work[index] = [
                (left - scale * right) % p
                for left, right in zip(work[index], work[rank], strict=True)
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def solve_square_mod(rows, rhs, p):
    if len(rows) != len(rows[0]) or len(rhs) != len(rows):
        raise ValueError("expected a square linear system")
    augmented = [
        [entry % p for entry in row] + [value % p]
        for row, value in zip(rows, rhs, strict=True)
    ]
    size = len(rows)
    for column in range(size):
        pivot = next(
            (index for index in range(column, size) if augmented[index][column]),
            None,
        )
        if pivot is None:
            raise RuntimeError("singular interpolation anchor")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = inverse_mod(augmented[column][column], p)
        augmented[column] = [
            (scale * entry) % p for entry in augmented[column]
        ]
        for index in range(size):
            if index == column or augmented[index][column] == 0:
                continue
            scale = augmented[index][column]
            augmented[index] = [
                (left - scale * right) % p
                for left, right in zip(
                    augmented[index], augmented[column], strict=True
                )
            ]
    return [augmented[index][-1] for index in range(size)]


def residual_matrix_mod(p, pairs):
    points = [point for pair in pairs for point in pair]
    labels = [1, 1, 2, 2, 3, 3]

    def R_at(point):
        return point * (point - 1) % p

    anchor = [
        [R_at(point) * pow(point, degree, p) % p for degree in range(3)]
        for point in points[:3]
    ]
    residual = [[0] * 5 for _ in range(3)]
    for exponent in range(5):
        rhs = [
            labels[index] * pow(points[index], exponent, p) % p
            for index in range(3)
        ]
        interpolation = solve_square_mod(anchor, rhs, p)
        for row, point in enumerate(points[3:]):
            left = sum(
                interpolation[degree]
                * R_at(point)
                * pow(point, degree, p)
                for degree in range(3)
            )
            right = labels[row + 3] * pow(point, exponent, p)
            residual[row][exponent] = (left - right) % p
    return residual


def involution_gamma(pair, p):
    u, v = pair
    return (1 - u - v) * inverse_mod(u * v, p) % p


def multiply_poly_mod(left, right, p):
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] = (output[i + j] + a * b) % p
    return output


def split_quartic_hits(p, pairs, residual):
    used = {0, 1}
    used.update(point for pair in pairs for point in pair)
    remaining = [point for point in range(p) if point not in used]
    hits = []
    for roots in itertools.combinations(remaining, 4):
        coefficients = [1]
        for root in roots:
            coefficients = multiply_poly_mod(coefficients, [-root % p, 1], p)
        if all(
            sum(row[degree] * coefficients[degree] for degree in range(5)) % p
            == 0
            for row in residual
        ):
            hits.append({"roots": list(roots), "coefficients": coefficients})
    return hits


def rank2_core_recovery_witness(p, pairs, hit):
    """Reconstruct W and certify exact-core migration for one split hit."""
    field = GF(p)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    labels = (1, 2, 3)
    F = sum(
        (field(coefficient) * X**degree for degree, coefficient in enumerate(hit["coefficients"])),
        PX.zero(),
    )
    R = X * (X - 1)
    support_locators = [
        (X - field(pair[0])) * (X - field(pair[1])) for pair in pairs
    ]
    rows = []
    rhs = []
    for block, (label, support_locator) in enumerate(
        zip(labels, support_locators, strict=True)
    ):
        columns = [R * X**j for j in range(3)] + [PX.zero()] * 9
        offset = 3 + 3 * block
        for j in range(3):
            columns[offset + j] = -support_locator * X**j
        target = field(label) * F
        for degree in range(5):
            rows.append([column[degree] for column in columns])
            rhs.append(target[degree])
    coefficient = matrix(field, rows)
    augmented = coefficient.augment(vector(field, rhs).column())
    if coefficient.rank() != 12 or augmented.rank() != 12:
        raise RuntimeError("split rank-two locator failed the full-system gate")
    solution = coefficient.solve_right(vector(field, rhs))
    V = sum((solution[j] * X**j for j in range(3)), PX.zero())
    W = R * V
    common = F.gcd(W).monic()
    if common.degree() != 2:
        raise RuntimeError("rank-two split witness did not recover two core roots")
    F_new = exact_quotient(F, common, "rank-two core recovery F")
    W_new = exact_quotient(W, common, "rank-two core recovery W")
    recovered = sorted(
        root for root in hit["roots"] if common(field(root)) == 0
    )
    missed_after = sorted(
        root for root in hit["roots"] if common(field(root)) != 0
    )
    if len(recovered) != 2 or len(missed_after) != 2:
        raise RuntimeError("rank-two core-recovery root partition drift")
    if any(W(field(root)) != 0 for root in recovered):
        raise RuntimeError("recovered root is not a W-zero")
    if any(W(field(root)) == 0 for root in missed_after):
        raise RuntimeError("migrated missed-core root was accidentally recovered")
    for label, pair in zip(labels, pairs, strict=True):
        reduced_difference = W_new - field(label) * F_new
        if any(reduced_difference(field(root)) != 0 for root in pair):
            raise RuntimeError("cancelled rank-two incidence identity failed")
    return {
        "original_F_roots": list(hit["roots"]),
        "recovered_core_roots": recovered,
        "migrated_missed_core_roots": missed_after,
        "gcd_F_W_coefficients": [int(common[index]) for index in range(3)],
        "F_new_coefficients": [int(F_new[index]) for index in range(3)],
        "W_new_coefficients": [int(W_new[index]) for index in range(3)],
        "original_defect": 4,
        "migrated_exact_defect": 2,
        "route": "PROFILE_MIGRATION_CORE_RECOVERY",
    }


def structural_census(p, *, omit_last=False):
    remaining = list(range(2, p))
    rank_histogram = Counter()
    affine_histogram = Counter()
    involution_histogram = Counter()
    representatives = {}
    split_locator_examples = {}
    split_histogram = Counter()
    split_hits_total = 0
    rank2_recovery_transcript = []
    total = 0
    configurations = []
    for pair1 in itertools.combinations(remaining, 2):
        remainder1 = [point for point in remaining if point not in pair1]
        for pair2 in itertools.combinations(remainder1, 2):
            remainder2 = [point for point in remainder1 if point not in pair2]
            for pair3 in itertools.combinations(remainder2, 2):
                configurations.append((pair1, pair2, pair3))
    if omit_last:
        configurations.pop()

    for pairs in configurations:
        total += 1
        residual = residual_matrix_mod(p, pairs)
        coefficient_rank = rank_mod([row[:4] for row in residual], p)
        augmented_rank = rank_mod(residual, p)
        gammas = [involution_gamma(pair, p) for pair in pairs]
        background_involution_pairs = 1 + max(Counter(gammas).values())
        rank_histogram[str(coefficient_rank)] += 1
        affine_key = f"rankC={coefficient_rank},rankAug={augmented_rank}"
        affine_histogram[affine_key] += 1
        involution_key = (
            f"{affine_key},backgroundInvolutionPairs={background_involution_pairs}"
        )
        involution_histogram[involution_key] += 1
        representatives.setdefault(
            affine_key,
            {
                "pairs": [list(pair) for pair in pairs],
                "residual_matrix_columns_f0_f1_f2_f3_x4": residual,
                "involution_gammas": gammas,
                "max_pairs_swapped_by_an_involution_that_swaps_background": (
                    background_involution_pairs
                ),
            },
        )
        if p == 13:
            hits = split_quartic_hits(p, pairs, residual)
            split_histogram[
                f"rankC={coefficient_rank},rankAug={augmented_rank},hits={len(hits)}"
            ] += 1
            split_hits_total += len(hits)
            if coefficient_rank == 2 and augmented_rank == 2:
                for hit in hits:
                    rank2_recovery_transcript.append(
                        {
                            "pairs": [list(pair) for pair in pairs],
                            "recovery": rank2_core_recovery_witness(p, pairs, hit),
                        }
                    )
            if hits and affine_key not in split_locator_examples:
                split_locator_examples[affine_key] = {
                    "pairs": [list(pair) for pair in pairs],
                    "involution_gammas": gammas,
                    "residual_matrix_columns_f0_f1_f2_f3_x4": residual,
                    "hits": hits,
                }

    report = {
        "p": p,
        "normalization": {
            "background_pair": [0, 1],
            "labels": [1, 2, 3],
            "support_pairs_labeled_and_internally_unordered": True,
        },
        "total": total,
        "rank_histogram": dict(sorted(rank_histogram.items())),
        "affine_rank_histogram": dict(sorted(affine_histogram.items())),
        "rank_involution_histogram": dict(sorted(involution_histogram.items())),
        "representatives": dict(sorted(representatives.items())),
        "configuration_transcript_sha256": sha256_json(
            [
                {
                    "pairs": pairs,
                    "residual": residual_matrix_mod(p, pairs),
                }
                for pairs in configurations
            ]
        ),
    }
    if p == 13:
        report["split_quartic_locator_histogram"] = dict(sorted(split_histogram.items()))
        report["split_quartic_locator_hits"] = split_hits_total
        report["split_quartic_locator_examples"] = dict(
            sorted(split_locator_examples.items())
        )
        report["rank2_exact_profile_migration"] = {
            "split_compatible_locators": len(rank2_recovery_transcript),
            "route_histogram": dict(
                sorted(
                    Counter(
                        row["recovery"]["route"]
                        for row in rank2_recovery_transcript
                    ).items()
                )
            ),
            "migrated_defect_histogram": dict(
                sorted(
                    Counter(
                        str(row["recovery"]["migrated_exact_defect"])
                        for row in rank2_recovery_transcript
                    ).items()
                )
            ),
            "transcript_sha256": sha256_json(rank2_recovery_transcript),
            "representative": (
                rank2_recovery_transcript[0]
                if rank2_recovery_transcript
                else None
            ),
            "exact_d4_survivors": 0,
        }
    return report


def locator(PX, X, field, domain, indices):
    output = PX.one()
    for index in indices:
        output *= X - field(domain[index])
    return output


def p19_fixture_report():
    p, n, k, s = 19, 18, 5, 8
    field = GF(p)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    domain = subgroup(p, n)
    core = tuple(range(4))
    petals = (tuple(range(4, 8)), tuple(range(8, 12)), tuple(range(12, 16)))
    background = tuple(range(16, 18))
    scalars = (1, 2, 3)
    word = sunflower_word_from_blocks(
        p,
        n,
        k,
        s,
        list(core),
        [list(petal) for petal in petals],
        "sunflower-sequential-m3",
    )
    if word is None:
        raise RuntimeError("failed to construct p=19 sequential sunflower")
    values = word["values"]
    F = locator(PX, X, field, domain, core)
    R = locator(PX, X, field, domain, background)

    coefficient_histogram = Counter()
    consistent = 0
    matrix_transcript = []
    for supports in itertools.product(
        *(itertools.combinations(petal, 2) for petal in petals)
    ):
        B = [locator(PX, X, field, domain, support) for support in supports]
        rows = []
        rhs = []
        for block, (scalar, support_locator) in enumerate(
            zip(scalars, B, strict=True)
        ):
            columns = [R * X**j for j in range(3)] + [PX.zero()] * 9
            offset = 3 + 3 * block
            for j in range(3):
                columns[offset + j] = -support_locator * X**j
            target = scalar * F
            for degree in range(5):
                rows.append([column[degree] for column in columns])
                rhs.append(target[degree])
        A = matrix(field, rows)
        H = A.augment(vector(field, rhs).column())
        rank_A = A.rank()
        rank_H = H.rank()
        coefficient_histogram[f"rankA={rank_A},rankAug={rank_H}"] += 1
        if rank_A == rank_H:
            consistent += 1
        matrix_transcript.append(
            {
                "supports": [list(support) for support in supports],
                "rank_A": int(rank_A),
                "rank_augmented": int(rank_H),
            }
        )
    if len(matrix_transcript) != 216 or consistent != 0:
        raise RuntimeError("p=19 fixed-support census drift")

    decoded = img_list(values, domain, k, s, p, "support")
    L_core = locator(PX, X, field, domain, core)
    planted = {
        tuple(int((scalar * L_core)(field(point))) for point in domain)
        for scalar in scalars
    }
    decoded_words = set(decoded)
    if not planted.issubset(decoded_words):
        raise RuntimeError("p=19 planted words missing from exact decoder")
    extras = decoded_words - planted
    targets = []
    for codeword, mask in decoded.items():
        agreement = {index for index in range(n) if mask & (1 << index)}
        d = len(set(core) - agreement)
        r = len(set(background) & agreement)
        hits = sorted(
            [len(set(petal) & agreement) for petal in petals if set(petal) & agreement],
            reverse=True,
        )
        if d == 4 and r == 2 and hits == [2, 2, 2]:
            targets.append(
                {
                    "codeword": list(map(int, codeword)),
                    "agreement_mask": int(mask),
                    "stabilizer_order": stabilizer_order(mask, n),
                }
            )
    if len(decoded) != 4 or len(extras) != 1 or targets:
        raise RuntimeError("p=19 exact decoder control drift")

    return {
        "row": {"p": p, "n": n, "k": k, "s": s, "sigma": 3, "ell": 4},
        "layout": {
            "domain": list(map(int, domain)),
            "core": list(core),
            "petals": [list(petal) for petal in petals],
            "background": list(background),
            "labels": list(scalars),
        },
        "fixed_support_census": {
            "systems": len(matrix_transcript),
            "rank_histogram": dict(sorted(coefficient_histogram.items())),
            "consistent_systems": consistent,
            "transcript_sha256": sha256_json(matrix_transcript),
        },
        "exact_list_decoder": {
            "list_size": len(decoded),
            "planted_words": len(planted),
            "extras": len(extras),
            "target_profile_count": len(targets),
            "decoded_sha256": sha256_json(
                sorted(
                    [
                        {"codeword": list(map(int, codeword)), "mask": int(mask)}
                        for codeword, mask in decoded.items()
                    ],
                    key=lambda row: (row["mask"], row["codeword"]),
                )
            ),
        },
    }


def moving_support_ledger_report():
    """Certified upper ledger charge after the low-rank exactness gate at m=2."""

    def finite_row(q, K, M, b):
        if K < 4 or M < 3 or b not in (2, 3):
            raise ValueError("m=2 B9 row requires K>=4, M>=3, and 2<=b<4")
        n = K + 4 * M + b
        selected_support_charts = comb(b, 2) * comb(M, 3) * comb(4, 2) ** 3
        old_cofactor_charge = selected_support_charts * q**3
        rank3_charge = selected_support_charts * q
        return {
            "q": q,
            "n": n,
            "K": K,
            "k": K + 1,
            "M": M,
            "b": b,
            "s": K + 4,
            "selected_support_charts": selected_support_charts,
            "rank_at_most_1_exact_d4_charge": 0,
            "rank2_exact_d4_charge": 0,
            "rank3_ambient_monic_F_charge": rank3_charge,
            "total_exact_d4_upper_bound": rank3_charge,
            "previous_fixed-pattern_cofactor_upper_bound": old_cofactor_charge,
            "improvement_factor": q**2,
        }

    rows = [
        finite_row(19, 4, 3, 2),
        finite_row(23, 4, 4, 2),
        finite_row(47, 4, 10, 2),
    ]
    return {
        "status": "RIGOROUS_M2_CHART_BOUND",
        "chart": {
            "m": 2,
            "ell": 4,
            "d": 4,
            "r": 2,
            "t": 3,
            "a_i": [2, 2, 2],
            "feasibility": ["K>=4", "M>=3", "2<=b<4"],
        },
        "support_chart_formula": "binom(b,2)*binom(M,3)*binom(4,2)^3",
        "rank_partition": {
            "affine_incompatible": "rank([C|u])>rank(C); charge zero and stop before migration",
            "rank_at_most_1": "incompatible, or removed by the same rank-drop core-recovery lemma if compatible",
            "compatible_rank2": "PROFILE_MIGRATION_CORE_RECOVERY from d=4 to d=2",
            "rank3": "exactly q ambient monic quartics per selected-support chart",
        },
        "exact_d4_upper_bound_formula": (
            "binom(b,2)*binom(M,3)*216*q"
        ),
        "old_cofactor_upper_bound_formula": (
            "binom(b,2)*binom(M,3)*216*q^3"
        ),
        "no_extra_core_choice_reason": (
            "the affine monic-F fibre already ranges over all quartics; valid "
            "split missed-core locators form a subset of those q ambient points"
        ),
        "fixed_m2_polynomial_consequence": (
            "because b<4 and M<=n/4, the exact target is O(n^3*q); "
            "if q<=n^A this is O(n^(A+3))"
        ),
        "finite_rows": rows,
        "nonclaim": (
            "this fixed m=2 calculation does not close the complete "
            "mixed-petal profile envelope"
        ),
    }


def validate_census(report):
    expected = EXPECTED_CENSUS[report["p"]]
    for key in ("total", "rank_histogram", "affine_rank_histogram", "rank_involution_histogram"):
        if report[key] != expected[key]:
            raise RuntimeError(
                f"GF({report['p']}) {key} drift: "
                f"actual={report[key]!r}, expected={expected[key]!r}"
            )
    if report["p"] == 13:
        recovery = report["rank2_exact_profile_migration"]
        for key, expected_value in EXPECTED_RANK2_RECOVERY.items():
            if recovery[key] != expected_value:
                raise RuntimeError(
                    f"GF(13) rank-two recovery {key} drift: "
                    f"actual={recovery[key]!r}, expected={expected_value!r}"
                )


def build_report():
    census11 = structural_census(11)
    census13 = structural_census(13)
    validate_census(census11)
    validate_census(census13)
    return json_ready(
        {
            "schema": "rs-mca-l1-b9-boundary-222-v2",
            "status": "EXPERIMENTAL/LOCAL_LEMMA",
            "profile": profile_report(),
            "coefficient_systems": coefficient_system_report(),
            "symbolic_compatibility": symbolic_compatibility_report(),
            "structural_censuses": [census11, census13],
            "exact_rs_control": p19_fixture_report(),
            "moving_support_ledger": moving_support_ledger_report(),
            "proof_status": {
                "rigorous": [
                    "B8 and B9 arithmetic for the fixed m=2 profile",
                    "uniform coefficient rank on the pairwise-coprime m=2 chart",
                    "evaluation-matrix compatibility reduction",
                    "compatible low-rank implies degree-two complete-fibre quotient",
                    "compatible rank-two split witnesses recover exactly two missed-core points and cannot realize exact d=4",
                    "the exact m=2 moving-support target has certified upper charge 216*binom(b,2)*binom(M,3)*q",
                ],
                "exact_finite_evidence": [
                    "GF(11) and GF(13) structural rank distributions",
                    "p=19 sequential sunflower has no compatible (2,2,2) support fibre",
                ],
                "unproved": [
                    "domain-compatible quotient ownership for non-exact rational fibre templates",
                    "comparison of the complete m=2 moving-support add-back with the profile envelope",
                    "any higher-m fixed-syndrome Pade dichotomy",
                ],
            },
            "nonclaims": [
                "does not infer a theorem from the empty minimal p=19 fixture",
                "does not claim a generic Groebner saturation was completed",
                "does not use the pairwise-only 10x9 system as the full compatibility test",
                "does not promote exact tiny-field evidence into an asymptotic bound",
                "does not use arbitrary rational quotient ownership to remove the exact rank-two chart",
                "does not prove that arbitrary non-exact rational fibre templates are paid by the existing quotient ledger",
                "does not close B11 or the full mixed-petal bucket",
            ],
            "verdict": "YELLOW - promising but unresolved; do not authorize global proof.",
        }
    )


def tamper_selftest():
    for p in (11, 13):
        tampered = structural_census(p, omit_last=True)
        try:
            validate_census(tampered)
        except RuntimeError:
            continue
        raise RuntimeError(f"GF({p}) omitted-configuration mutation was not detected")
    pairs = ((2, 6), (8, 9), (4, 12))
    hit = {
        "roots": [3, 5, 7, 10],
        "coefficients": [10, 4, 0, 1, 1],
    }
    rank2_core_recovery_witness(13, pairs, hit)
    tampered_hit = {
        "roots": hit["roots"],
        "coefficients": hit["coefficients"][:],
    }
    tampered_hit["coefficients"][0] = (
        tampered_hit["coefficients"][0] + 1
    ) % 13
    try:
        rank2_core_recovery_witness(13, pairs, tampered_hit)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("mutated rank-two locator passed the recovery gate")
    print("[PASS] omitted-configuration mutations rejected for GF(11) and GF(13)")
    print("[PASS] mutated rank-two locator rejected by the exactness gate")
    print("RESULT: PASS (B9-boundary census and exactness tamper self-test)")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.tamper_selftest:
        tamper_selftest()
        return 0
    actual = build_report()
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(actual, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != actual:
        print("RESULT: FAIL (frozen B9-boundary certificate drift)", file=sys.stderr)
        return 1
    print(
        "[PASS] full rank=12; GF(11)=7560, GF(13)=41580; "
        "rank2 exact d=4 survivors=0; m=2 charge=216*C(b,2)*C(M,3)*q; "
        "p=19 fixed-support systems=216, consistent=0"
    )
    print("RESULT: PASS (B9-boundary local algebra and exact censuses)")
    return 0


if __name__ == "__main__":
    raise SystemExit(builtins.int(main(sys.argv[1:])))
