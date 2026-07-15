#!/usr/bin/env sage
"""Verify the total-degree-six reduced-CRT lemma for ``(3,1,3,(3,2,1))``.

For a retained background locator ``R`` of degree one, pairwise-coprime
positive locators ``B_i`` of degrees ``(3,2,1)``, and distinct nonzero labels
``c_i``, the divided equations are

    R*V - c_i*F = B_i*A_i,

where ``F`` is monic cubic, ``deg(V)<=2``, and
``deg(A_i)<=3-deg(B_i)``.  The fixed-``F`` coefficient matrix is ``12 x 9``
of rank nine.  Moving the three lower coefficients of ``F`` gives a
``12 x 12`` system.  If ``B=B_1*B_2*B_3`` and

    G = c_i*R^(-1) mod B_i,

then compatibility is exactly the vanishing of coefficients ``X^3,X^4,X^5``
in ``F*G mod B``.  This is a reduced affine ``3 x 3`` system.  Full rank gives
at most one monic cubic.  A compatible rank drop gives two independent kernel
pairs ``(F_j,V_j)``; because ``B`` divides ``F_0*V_1-F_1*V_0`` while the latter
has degree at most five, it vanishes.  If a monic pair ``(F_0,V_0)`` were
coprime, Euclid's lemma would give ``F_0|F_1`` for a second independent pair;
the cubic degree bound would make the pairs dependent.  Hence
``gcd(F,V)`` has positive degree for every monic cubic in the affine fibre.

Under the explicit split-core, zero core/background data, and disjointness
hypotheses, a root of ``gcd(F,V)`` is an additional core agreement.  Thus a
compatible rank drop migrates the exact ``d=3`` profile to ``d<=2``.  The algebra depends on
``sum(deg(B_i))=6``, not on the individual degree distribution; this packet
specializes the fixed-system bookkeeping to ``(3,2,1)`` and quotient degrees
``(0,1,2)``.

The symbolic identities and the frozen 1,152-key GF(19) census are exact.  The
packet is local.  Its bank state is recomputed from the two declared review
artifacts; the algebra and census do not by themselves authorize a ledger
change.
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

from sage.all import GF, PolynomialRing, QQ, matrix, vector


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31321-total-degree-crt/certificate.json"
)
PRIOR_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/certificate.json"
)
PRIOR_VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_lemma.sage"
)
PRIOR_LEMMA_PATH = (
    ROOT / "experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_lemma.md"
)
PRIOR_INDEPENDENT_REVIEW_PATH = (
    ROOT / "experimental/notes/l1/l1_b9_frontier_31222_independent_review.md"
)
PRIOR_YELLOW_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_cross_model_review.md"
)
PRIOR_GREEN_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_cross_model_review_v2.md"
)
CURRENT_YELLOW_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_frontier_31321_total_degree_crt_independent_review_yellow.md"
)
CURRENT_CROSS_MODEL_ATTEMPT1_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_frontier_31321_total_degree_crt_cross_model_attempt1.md"
)
CURRENT_INDEPENDENT_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_frontier_31321_total_degree_crt_final_package_independent_review.md"
)
CURRENT_CROSS_MODEL_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_frontier_31321_total_degree_crt_final_package_cross_model_review.md"
)

P = 19
N = 18
CORE = tuple(range(4))
PETALS = (
    tuple(range(4, 8)),
    tuple(range(8, 12)),
    tuple(range(12, 16)),
)
BACKGROUND = tuple(range(16, 18))
LABELS = (1, 2, 3)
TARGET_OCCUPANCIES = (3, 2, 1)


def sha256_json(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=int)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locator(PX, X, roots):
    output = PX.one()
    for root in roots:
        output *= X - root
    return output


def polynomial_from_coefficients(PX, coefficients):
    X = PX.gen()
    field = PX.base_ring()
    return sum(
        (field(value) * X**degree for degree, value in enumerate(coefficients)),
        PX.zero(),
    )


def coefficients_low_to_high(poly, degree):
    return [int(poly[index]) for index in range(degree + 1)]


def support_assignments():
    """Enumerate the 2*6*4*6*4=1,152 canonical labelled keys."""
    occupancies = tuple(dict.fromkeys(itertools.permutations(TARGET_OCCUPANCIES)))
    for background_support in itertools.combinations(BACKGROUND, 1):
        for occupancy in occupancies:
            choices = [
                tuple(itertools.combinations(petal, count))
                for petal, count in zip(PETALS, occupancy, strict=True)
            ]
            for supports in itertools.product(*choices):
                yield tuple(background_support), tuple(supports)


def canonical_assignment(background_support, supports):
    return [list(background_support), *[list(support) for support in supports]]


def canonical_ledger_key(background_support, supports):
    """Canonical key shared with the existing-owner ledger, order-free."""
    return {
        "background_support": list(background_support),
        "petal_size_assignment": [len(support) for support in supports],
        "petal_supports": [list(support) for support in supports],
    }


def canonical_set_sha256(rows):
    ordered = sorted(
        rows,
        key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")),
    )
    return sha256_json(ordered)


def pattern_id(background_support, supports):
    occupancy = "".join(str(len(support)) for support in supports)
    return (
        f"occ{occupancy}-b{background_support[0]}-"
        + "-".join("s" + ".".join(map(str, support)) for support in supports)
    )


def fixed_coefficient_matrix(PX, X, field, R, support_locators):
    """Return the 12 x 9 fixed-F matrix and quotient-degree bounds."""
    quotient_degrees = [3 - int(poly.degree()) for poly in support_locators]
    if sorted(quotient_degrees) != [0, 1, 2]:
        raise RuntimeError(f"quotient-degree drift: {quotient_degrees}")

    v_columns = [R * X**degree for degree in range(3)]
    offsets = []
    column_count = len(v_columns)
    for degree_bound in quotient_degrees:
        offsets.append(column_count)
        column_count += degree_bound + 1
    if column_count != 9:
        raise RuntimeError(f"expected nine fixed columns, found {column_count}")

    rows = []
    for block, (support_locator, degree_bound) in enumerate(
        zip(support_locators, quotient_degrees, strict=True)
    ):
        active = [PX.zero()] * column_count
        for degree in range(3):
            active[degree] = v_columns[degree]
        for degree in range(degree_bound + 1):
            active[offsets[block] + degree] = -support_locator * X**degree
        for coefficient_degree in range(4):
            rows.append([poly[coefficient_degree] for poly in active])
    return matrix(field, rows), quotient_degrees


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


def crt_multiplier(PX, R, support_locators, field):
    B = PX.one()
    for support_locator in support_locators:
        B *= support_locator
    G = PX.zero()
    for label, support_locator in zip(LABELS, support_locators, strict=True):
        complement = B // support_locator
        projector = complement * complement.inverse_mod(support_locator)
        residue = field(label) * R.inverse_mod(support_locator)
        G += residue * projector
    G = G.mod(B)
    if int(B.degree()) != 6:
        raise RuntimeError(f"expected degree-six CRT modulus, found {B.degree()}")
    if G.gcd(B) != 1:
        raise RuntimeError("CRT multiplier is not a unit modulo B")
    return B, G


def reduced_affine_map(PX, X, field, B, G):
    compatibility_degrees = (3, 4, 5)
    columns = []
    for lower_degree in range(3):
        remainder = (X**lower_degree * G).mod(B)
        columns.append(
            [remainder[degree] for degree in compatibility_degrees]
        )
    M = matrix(field, 3, 3, lambda row, column: columns[column][row])
    monic_remainder = (X**3 * G).mod(B)
    u = vector(
        field, [monic_remainder[degree] for degree in compatibility_degrees]
    )
    return M, u


def affine_solutions(M, rhs, field, max_solutions=10_000):
    rank_M = int(M.rank())
    augmented_rank = int(M.augment(rhs.column()).rank())
    if rank_M != augmented_rank:
        return rank_M, augmented_rank, []
    kernel = M.right_kernel().basis()
    count = int(field.order()) ** len(kernel)
    if count > max_solutions:
        raise RuntimeError(f"affine solution fibre too large: {count}")
    particular = M.solve_right(rhs)
    solutions = []
    for coefficients in itertools.product(
        range(int(field.order())), repeat=len(kernel)
    ):
        solution = vector(field, particular)
        for coefficient, direction in zip(coefficients, kernel, strict=True):
            solution += field(coefficient) * direction
        solutions.append(solution)
    return rank_M, augmented_rank, solutions


def replay_solution(
    PX,
    X,
    field,
    R,
    support_locators,
    quotient_degrees,
    B,
    G,
    F,
):
    """Construct and verify the unique fixed variables attached to ``F``."""
    V = (F * G).mod(B)
    if V and int(V.degree()) > 2:
        raise RuntimeError("compatible remainder exceeds degree two")
    fixed_coordinates = [V[degree] for degree in range(3)]
    quotient_polynomials = []
    for label, support_locator, degree_bound in zip(
        LABELS, support_locators, quotient_degrees, strict=True
    ):
        numerator = R * V - field(label) * F
        if numerator.mod(support_locator) != 0:
            raise RuntimeError("CRT solution is not divisible by a support locator")
        quotient = numerator // support_locator
        if quotient and int(quotient.degree()) > degree_bound:
            raise RuntimeError("quotient-degree bound failed")
        quotient_polynomials.append(quotient)
        fixed_coordinates.extend(
            quotient[degree] for degree in range(degree_bound + 1)
        )
    if len(fixed_coordinates) != 9:
        raise RuntimeError("fixed-coordinate count drift")
    return V, quotient_polynomials, fixed_coordinates


def symbolic_total_degree_map():
    coefficient_ring = PolynomialRing(
        QQ,
        names=(
            "b0", "b1", "b2", "b3", "b4", "b5",
            "g0", "g1", "g2", "g3", "g4", "g5",
            "f0", "f1", "f2",
        ),
    )
    (
        b0, b1, b2, b3, b4, b5,
        g0, g1, g2, g3, g4, g5,
        f0, f1, f2,
    ) = coefficient_ring.gens()
    PX = PolynomialRing(coefficient_ring, "X")
    X = PX.gen()
    B = X**6 + b5*X**5 + b4*X**4 + b3*X**3 + b2*X**2 + b1*X + b0
    G = g5*X**5 + g4*X**4 + g3*X**3 + g2*X**2 + g1*X + g0
    F = X**3 + f2*X**2 + f1*X + f0
    M, u = reduced_affine_map(PX, X, coefficient_ring, B, G)
    remainder = (F * G).mod(B)
    direct = vector(coefficient_ring, [remainder[index] for index in (3, 4, 5)])
    affine = M * vector(coefficient_ring, [f0, f1, f2]) + u

    pair_ring = PolynomialRing(
        QQ,
        names=(
            "a0", "a1", "a2", "a3", "d0", "d1", "d2", "d3",
            "v0", "v1", "v2", "w0", "w1", "w2",
        ),
    )
    (
        a0, a1, a2, a3, d0, d1, d2, d3,
        v0, v1, v2, w0, w1, w2,
    ) = pair_ring.gens()
    PY = PolynomialRing(pair_ring, "Y")
    Y = PY.gen()
    F0 = a3*Y**3 + a2*Y**2 + a1*Y + a0
    F1 = d3*Y**3 + d2*Y**2 + d1*Y + d0
    V0 = v2*Y**2 + v1*Y + v0
    V1 = w2*Y**2 + w1*Y + w0
    cross = F0*V1 - F1*V0

    return {
        "B": str(B),
        "G": str(G),
        "F": str(F),
        "compatibility_degrees": [3, 4, 5],
        "M_rows": [[str(value) for value in row] for row in M.rows()],
        "u": [str(value) for value in u],
        "affine_map_shape": [3, 3],
        "affine_identity_verified": bool(direct == affine),
        "det_M": str(M.det()),
        "det_M_sha256": hashlib.sha256(str(M.det()).encode("utf-8")).hexdigest(),
        "cross_polynomial_degree_bound": int(cross.degree()),
        "cross_polynomial_sha256": hashlib.sha256(
            str(cross).encode("utf-8")
        ).hexdigest(),
        "degree_gap": "deg(F0*V1-F1*V0)<=5<deg(B)=6",
        "distribution_independence": (
            "the reduced map and cross-degree argument use deg(B)=6, not the "
            "individual positive degrees of B1,B2,B3"
        ),
    }


def validate_bridge_control(control):
    """Fail closed on the split-core/zero-data/disjointness bridge."""
    try:
        field = GF(int(control["field"]))
        PX = PolynomialRing(field, "X")
        X = PX.gen()
        core = tuple(field(value) for value in control["core_roots"])
        background = tuple(field(value) for value in control["background_roots"])
        h = field(control["restored_core_root"])
        recorded_D = tuple(field(value) for value in control["missed_core_roots"])
        received = tuple(field(value) for value in control["received_core_values"])
        received_background = tuple(
            field(value) for value in control["received_background_values"]
        )
        if len(core) != 4 or len(set(core)) != 4:
            return False
        if len(background) != 1 or set(core).intersection(background):
            return False
        if h not in core:
            return False
        D = tuple(value for value in core if value != h)
        if recorded_D != D or len(D) != 3:
            return False
        if len(received) != 4 or any(value != 0 for value in received):
            return False
        if (
            len(received_background) != len(background)
            or any(value != 0 for value in received_background)
        ):
            return False

        F = polynomial_from_coefficients(PX, control["F_coefficients_low_to_high"])
        V = polynomial_from_coefficients(PX, control["V_coefficients_low_to_high"])
        expected_F = locator(PX, X, D)
        if F != expected_F or F.degree() != 3 or not F.is_squarefree():
            return False
        roots = F.roots()
        if (
            len(roots) != 3
            or {root for root, multiplicity in roots} != set(D)
            or any(multiplicity != 1 for root, multiplicity in roots)
        ):
            return False
        if not V or V.degree() > 2:
            return False

        core_locator = locator(PX, X, core)
        H = core_locator // F
        if H != X - h:
            return False
        R = locator(PX, X, background)
        if R.gcd(core_locator) != 1:
            return False
        gcd_FV = F.gcd(V)
        alpha = field(control["common_root_alpha"])
        if gcd_FV.degree() < 1 or gcd_FV(alpha) != 0:
            return False
        if alpha not in D or alpha == h:
            return False

        W = R * H * V
        agreements = tuple(
            value
            for value, received_value in zip(core, received, strict=True)
            if W(value) == received_value
        )
        missed = tuple(
            value
            for value, received_value in zip(core, received, strict=True)
            if W(value) != received_value
        )
        expected_agreements = tuple(
            value for value in core if value == h or (value in D and V(value) == 0)
        )
        expected_missed = tuple(value for value in D if V(value) != 0)
        return bool(
            agreements == expected_agreements
            and missed == expected_missed
            and len(missed) <= 2
            and [int(value) for value in agreements]
            == control["actual_core_agreement_roots"]
            and [int(value) for value in missed]
            == control["actual_missed_core_roots"]
            and control["pointwise_bridge_verified"]
            and control["exact_d3_excluded"]
        )
    except (KeyError, TypeError, ValueError, ArithmeticError):
        return False


def bridge_positive_control():
    field = GF(11)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    core = tuple(field(value) for value in (1, 2, 3, 4))
    background = (field(0),)
    h = field(4)
    D = tuple(value for value in core if value != h)
    F = locator(PX, X, D)
    V = X - field(1)
    R = locator(PX, X, background)
    H = locator(PX, X, core) // F
    W = R * H * V
    agreements = tuple(value for value in core if W(value) == 0)
    missed = tuple(value for value in core if W(value) != 0)
    control = {
        "field": 11,
        "core_roots": [int(value) for value in core],
        "background_roots": [int(value) for value in background],
        "restored_core_root": int(h),
        "missed_core_roots": [int(value) for value in D],
        "F_coefficients_low_to_high": coefficients_low_to_high(F, 3),
        "V_coefficients_low_to_high": coefficients_low_to_high(V, 2),
        "common_root_alpha": 1,
        "received_core_values": [0, 0, 0, 0],
        "received_background_values": [0],
        "actual_core_agreement_roots": [int(value) for value in agreements],
        "actual_missed_core_roots": [int(value) for value in missed],
        "pointwise_bridge_verified": True,
        "exact_d3_excluded": True,
    }
    if not validate_bridge_control(control):
        raise RuntimeError("bridge positive control failed")
    return control


def frozen_gf19_census():
    field = GF(P)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    domain = tuple(field(2) ** exponent for exponent in range(N))
    if len(set(domain)) != N:
        raise RuntimeError("frozen domain is not the full multiplicative subgroup")
    core_locator = locator(PX, X, tuple(domain[index] for index in CORE))
    actual_locators = []
    for restored_core in CORE:
        F = core_locator // (X - domain[restored_core])
        actual_locators.append((restored_core, F))

    fixed_rank_histogram = Counter()
    fixed_actual_augmented_histogram = Counter()
    moving_rank_histogram = Counter()
    reduced_rank_histogram = Counter()
    solution_count_histogram = Counter()
    support_degree_order_histogram = Counter()
    compatible_rankdrop_patterns = []
    rankdrop_solution_total = 0
    rankdrop_gcd_degree_histogram = Counter()
    rankdrop_zero_gcd = []
    full_rank_pattern_count = 0
    full_rank_solution_count = 0
    actual_split_core_incidence_count = 0
    actual_rankdrop_incidence_count = 0
    actual_rankdrop_bridge_failure_count = 0
    canonical_keys = []
    transcript = []

    for background_support, supports in support_assignments():
        canonical_keys.append(canonical_ledger_key(background_support, supports))
        R = locator(PX, X, tuple(domain[index] for index in background_support))
        support_locators = [
            locator(PX, X, tuple(domain[index] for index in support))
            for support in supports
        ]
        support_degrees = tuple(int(poly.degree()) for poly in support_locators)
        support_degree_order_histogram["".join(map(str, support_degrees))] += 1

        A, quotient_degrees = fixed_coefficient_matrix(
            PX, X, field, R, support_locators
        )
        rank_A = int(A.rank())
        fixed_rank_histogram[str(rank_A)] += 1
        if rank_A != 9:
            raise RuntimeError("fixed-F rank-nine theorem failed")

        actual_rows = []
        for restored_core, F in actual_locators:
            augmented_rank = int(A.augment(fixed_rhs(field, F).column()).rank())
            fixed_actual_augmented_histogram[
                f"rankA={rank_A},rankAug={augmented_rank}"
            ] += 1
            actual_rows.append(
                {
                    "restored_core": restored_core,
                    "rank_augmented": augmented_rank,
                }
            )

        C, moving_rhs = moving_monic_system(A, field)
        rank_C = int(C.rank())
        rank_C_augmented = int(C.augment(moving_rhs.column()).rank())
        moving_rank_histogram[
            f"rankC={rank_C},rankAug={rank_C_augmented}"
        ] += 1

        B, G = crt_multiplier(PX, R, support_locators, field)
        M, u = reduced_affine_map(PX, X, field, B, G)
        rank_M, rank_M_augmented, lower_coefficients = affine_solutions(
            M, -u, field
        )
        reduced_rank_histogram[
            f"rankM={rank_M},rankAug={rank_M_augmented}"
        ] += 1
        if rank_C != 9 + rank_M:
            raise RuntimeError("moving/reduced rank relation failed")
        if rank_C_augmented != 9 + rank_M_augmented:
            raise RuntimeError("augmented moving/reduced rank relation failed")
        solution_count_histogram[str(len(lower_coefficients))] += 1

        solution_rows = []
        gcd_degrees = Counter()
        for coefficients in lower_coefficients:
            F = X**3 + sum(
                coefficients[degree] * X**degree for degree in range(3)
            )
            V, quotients, fixed_coordinates = replay_solution(
                PX,
                X,
                field,
                R,
                support_locators,
                quotient_degrees,
                B,
                G,
                F,
            )
            moving_coordinates = vector(
                field,
                [*fixed_coordinates, *[coefficients[index] for index in range(3)]],
            )
            if C * moving_coordinates != moving_rhs:
                raise RuntimeError("12x12 solution replay failed")
            if rank_C < 12 and rank_C_augmented == rank_C:
                gcd_FV = F.gcd(V).monic()
                gcd_degree = int(gcd_FV.degree())
                gcd_degrees[str(gcd_degree)] += 1
                rankdrop_gcd_degree_histogram[str(gcd_degree)] += 1
                rankdrop_solution_total += 1
                row = {
                    "F_coefficients_low_to_high": coefficients_low_to_high(F, 3),
                    "V_coefficients_low_to_high": coefficients_low_to_high(V, 2),
                    "gcd_coefficients_low_to_high": coefficients_low_to_high(
                        gcd_FV, gcd_degree
                    ),
                    "gcd_degree": gcd_degree,
                    "quotient_coefficients_low_to_high": [
                        coefficients_low_to_high(quotient, degree_bound)
                        for quotient, degree_bound in zip(
                            quotients, quotient_degrees, strict=True
                        )
                    ],
                }
                solution_rows.append(row)
                if gcd_degree < 1:
                    rankdrop_zero_gcd.append(
                        {
                            "pattern_id": pattern_id(background_support, supports),
                            **row,
                        }
                    )

        if rank_C == 12:
            full_rank_pattern_count += 1
            if len(lower_coefficients) != 1:
                raise RuntimeError("full-rank pattern did not have one monic solution")
            full_rank_solution_count += len(lower_coefficients)
        elif rank_C_augmented == rank_C:
            compatible_rankdrop_patterns.append(
                {
                    "pattern_id": pattern_id(background_support, supports),
                    "canonical_assignment": canonical_assignment(
                        background_support, supports
                    ),
                    "support_degrees_in_label_order": list(support_degrees),
                    "quotient_degrees_in_label_order": quotient_degrees,
                    "rank_C": rank_C,
                    "rank_C_augmented": rank_C_augmented,
                    "rank_M": rank_M,
                    "rank_M_augmented": rank_M_augmented,
                    "monic_solution_count": len(lower_coefficients),
                    "gcd_degree_histogram": dict(sorted(gcd_degrees.items())),
                    "solutions_sha256": sha256_json(solution_rows),
                    "solution_examples": solution_rows[:4],
                    "B_coefficients_low_to_high": coefficients_low_to_high(B, 6),
                    "G_coefficients_low_to_high": coefficients_low_to_high(G, 5),
                    "M": [[int(value) for value in row] for row in M.rows()],
                    "u": [int(value) for value in u],
                }
            )

        for restored_core, F in actual_locators:
            coefficient_vector = vector(field, [F[index] for index in range(3)])
            if M * coefficient_vector + u != 0:
                continue
            actual_split_core_incidence_count += 1
            V, _quotients, _fixed = replay_solution(
                PX,
                X,
                field,
                R,
                support_locators,
                quotient_degrees,
                B,
                G,
                F,
            )
            if rank_C < 12:
                actual_rankdrop_incidence_count += 1
                H = core_locator // F
                W = R * H * V
                D = tuple(index for index in CORE if index != restored_core)
                missed = tuple(index for index in D if W(domain[index]) != 0)
                bridge_ok = bool(
                    F.gcd(V).degree() >= 1
                    and H == X - domain[restored_core]
                    and R.gcd(core_locator) == 1
                    and len(missed) <= 2
                )
                actual_rankdrop_bridge_failure_count += int(not bridge_ok)

        transcript.append(
            {
                "pattern_id": pattern_id(background_support, supports),
                "canonical_assignment": canonical_assignment(
                    background_support, supports
                ),
                "support_degrees_in_label_order": list(support_degrees),
                "quotient_degrees_in_label_order": quotient_degrees,
                "rank_A": rank_A,
                "actual_locator_rows": actual_rows,
                "rank_C": rank_C,
                "rank_C_augmented": rank_C_augmented,
                "rank_M": rank_M,
                "rank_M_augmented": rank_M_augmented,
                "monic_solution_count": len(lower_coefficients),
                "rankdrop_gcd_degree_histogram": dict(sorted(gcd_degrees.items())),
            }
        )

    if len(transcript) != 1_152:
        raise RuntimeError(f"support-pattern count drift: {len(transcript)}")
    if len({sha256_json(row) for row in canonical_keys}) != 1_152:
        raise RuntimeError("canonical support-key collision")
    return {
        "field": 19,
        "domain": [int(value) for value in domain],
        "support_pattern_formula": (
            "binom(2,1)*3!*binom(4,3)*binom(4,2)*binom(4,1)=1152"
        ),
        "support_pattern_count": len(transcript),
        "canonical_assignment_count": len(canonical_keys),
        "canonical_assignment_order_sha256": sha256_json(canonical_keys),
        "canonical_assignment_set_sha256": canonical_set_sha256(canonical_keys),
        "support_degree_order_histogram": dict(
            sorted(support_degree_order_histogram.items())
        ),
        "fixed_matrix_rank_histogram": dict(sorted(fixed_rank_histogram.items())),
        "fixed_actual_augmented_rank_histogram": dict(
            sorted(fixed_actual_augmented_histogram.items())
        ),
        "moving_rank_histogram": dict(sorted(moving_rank_histogram.items())),
        "reduced_rank_histogram": dict(sorted(reduced_rank_histogram.items())),
        "monic_solution_count_histogram": dict(
            sorted(solution_count_histogram.items(), key=lambda item: int(item[0]))
        ),
        "full_rank_pattern_count": full_rank_pattern_count,
        "full_rank_monic_solution_count": full_rank_solution_count,
        "compatible_rankdrop_pattern_count": len(compatible_rankdrop_patterns),
        "compatible_rankdrop_monic_solution_count": rankdrop_solution_total,
        "compatible_rankdrop_gcd_degree_histogram": dict(
            sorted(rankdrop_gcd_degree_histogram.items())
        ),
        "compatible_rankdrop_zero_gcd_count": len(rankdrop_zero_gcd),
        "compatible_rankdrop_zero_gcd_examples": rankdrop_zero_gcd,
        "compatible_rankdrop_patterns": compatible_rankdrop_patterns,
        "rankdrop_implication_GF19_status": (
            "VACUOUS_ALL_44_RANK_DROPS_ARE_AFFINE_INCONSISTENT"
        ),
        "actual_split_core_incidence_count": actual_split_core_incidence_count,
        "actual_rankdrop_incidence_count": actual_rankdrop_incidence_count,
        "actual_rankdrop_bridge_failure_count": actual_rankdrop_bridge_failure_count,
        "transcript_sha256": sha256_json(transcript),
    }


def linked_inputs():
    rows = {
        "prior_31222_certificate": PRIOR_CERTIFICATE_PATH,
        "prior_31222_sage_verifier": PRIOR_VERIFIER_PATH,
        "prior_31222_lemma": PRIOR_LEMMA_PATH,
        "prior_31222_independent_review": PRIOR_INDEPENDENT_REVIEW_PATH,
        "prior_31222_cross_model_yellow": PRIOR_YELLOW_REVIEW_PATH,
        "prior_31222_cross_model_green": PRIOR_GREEN_REVIEW_PATH,
        "current_31321_independent_yellow": CURRENT_YELLOW_REVIEW_PATH,
        "current_31321_cross_model_attempt1": CURRENT_CROSS_MODEL_ATTEMPT1_PATH,
    }
    missing = [str(path) for path in rows.values() if not path.exists()]
    if missing:
        raise RuntimeError(f"missing linked inputs: {missing}")
    return {
        name: {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path),
        }
        for name, path in rows.items()
    }


def prior_nonvacuous_total_degree_control():
    """Expose, without reinterpreting, the reviewed 31222 degree-six control."""
    prior = json.loads(PRIOR_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    frozen = prior["exact_controls"]["frozen_GF19"]
    return {
        "schema": prior["schema"],
        "status": prior["status"],
        "support_locator_degrees": prior["parameters"][
            "support_locator_degrees"
        ],
        "deg_B": prior["parameters"]["deg_B"],
        "deg_R": prior["parameters"]["deg_R"],
        "deg_F": prior["parameters"]["deg_F"],
        "deg_V_max": prior["parameters"]["deg_V_max"],
        "compatible_rankdrop_pattern_count": frozen[
            "compatible_rankdrop_pattern_count"
        ],
        "compatible_rankdrop_monic_cubic_count": frozen[
            "rankdrop_monic_cubic_count"
        ],
        "compatible_rankdrop_zero_gcd_count": frozen[
            "rankdrop_zero_gcd_count"
        ],
        "reviewed_verdict": prior["verdict"],
        "role": (
            "NONVACUOUS_TOTAL_DEGREE_SIX_CONTROL_ONLY; no theorem is imported "
            "from this prior row"
        ),
    }


def fresh_review_gate():
    """Require two independent GREEN/YES review artifacts before banking."""
    paths = {
        "independent_review": CURRENT_INDEPENDENT_REVIEW_PATH,
        "cross_model_review": CURRENT_CROSS_MODEL_REVIEW_PATH,
    }
    reviews = {}
    for name, path in paths.items():
        exists = path.exists()
        content = path.read_text(encoding="utf-8") if exists else ""
        verdict_green = any(
            line.strip() == "Verdict: GREEN" for line in content.splitlines()
        )
        ledger_authorization_yes = any(
            line.strip() == "Ledger authorization: YES"
            for line in content.splitlines()
        )
        row = {
            "path": str(path.relative_to(ROOT)),
            "exists": exists,
            "verdict_green": verdict_green,
            "ledger_authorization_yes": ledger_authorization_yes,
        }
        if exists:
            row["sha256"] = sha256_file(path)
        reviews[name] = row
    satisfied = all(
        row["exists"]
        and row["verdict_green"]
        and row["ledger_authorization_yes"]
        for row in reviews.values()
    )
    present_count = sum(bool(row["exists"]) for row in reviews.values())
    status = (
        "SATISFIED_TWO_HASH_LINKED_GREEN_REVIEWS"
        if satisfied
        else (
            "PRESENT_BUT_NOT_GREEN"
            if present_count == len(reviews)
            else "PENDING_REQUIRED_REVIEW_FILES"
        )
    )
    return {
        "required_review_count": 2,
        "reviews": reviews,
        "satisfied": satisfied,
        "status": status,
    }


def expected_statement():
    return (
        "for deg(R)=1 and pairwise-coprime positive B_i of degrees "
        "(3,2,1), the fixed-F 12x9 system has rank nine; the moving "
        "12x12 system reduces to the 3x3 affine high-coefficient map for "
        "F*G mod B; full rank gives at most one monic cubic, while every "
        "compatible rank drop forces gcd(F,V) to have positive degree "
        "and, under the explicit split-core/zero-data/disjointness bridge, "
        "migrates exact d=3 to d<=2"
    )


def expected_parameters():
    return {
        "profile": {"ell": 4, "d": 3, "r": 1, "t": 3, "a_i": [3, 2, 1]},
        "deg_R": 1,
        "support_locator_degrees_sorted": [3, 2, 1],
        "support_locator_hypotheses": (
            "B1,B2,B3 are monic, positive-degree, pairwise coprime, and "
            "each is coprime to R"
        ),
        "quotient_degrees_for_sorted_supports": [0, 1, 2],
        "deg_B": 6,
        "deg_F": 3,
        "deg_V_max": 2,
        "labels": [1, 2, 3],
        "label_hypothesis": "pairwise distinct and nonzero",
        "core_size": 4,
        "profile_bridge_hypotheses": [
            "the core, background, and labelled selected petal supports are pairwise disjoint",
            "the received word is zero on the core and retained background point",
            "the received word on labelled petal i is c_i*L_C",
            "the exact profile has one restored core agreement and one retained background agreement",
        ],
        "bridge_hypotheses": [
            "C consists of four distinct field points",
            "h is in C and D=C\\{h}",
            "F=L_D is monic, split, and squarefree",
            "gcd(R,L_C)=1",
            "the received word is zero on C and at the root of R",
            "H=L_C/F=X-h and W=R*H*V",
        ],
    }


def expected_frozen_system(symbolic):
    return {
        "equations": "R*V-c_i*F=B_i*A_i",
        "fixed_F_matrix_shape": [12, 9],
        "universal_fixed_rank": 9,
        "moving_monic_F_matrix_shape": [12, 12],
        "left_kernel_dimension": 3,
        "reduced_affine_map_shape": [3, 3],
        "compatibility_degrees": [3, 4, 5],
        "rank_relation": "rank(C_12x12)=9+rank(M_3x3)",
        "augmented_rank_relation": "rank([C|b])=9+rank([M|-u])",
        "symbolic_total_degree_map": symbolic,
    }


def expected_proof_certificate():
    return {
        "steps": [
            "a homogeneous fixed-F solution has B_i dividing R*V for every i",
            "coprimality with R gives B=B1*B2*B3 dividing V",
            "deg(B)=6>deg(V)<=2 forces V=0 and then every A_i=0, so the 12x9 map has rank nine",
            "CRT gives V=F*G mod B and compatibility is K(F)=M*(f0,f1,f2)^t+u=0 in degrees 3,4,5",
            "the moving and reduced ranks differ by the fixed rank nine",
            "rank(M)=3 gives at most one monic cubic for a canonical support key",
            "a compatible rank drop supplies two independent degree-at-most-three kernel pairs",
            "B divides F0*V1-F1*V0, whose degree is at most five, so the cross-polynomial vanishes",
            "if gcd(F0,V0)=1 then Euclid's lemma gives F0|F1; since F0 is cubic and deg(F1)<=3, the two pairs are dependent, a contradiction",
            "for split F=L_(C\\{h}), a common root alpha lies in C\\{h}",
            "W(alpha)=R(alpha)*(alpha-h)*V(alpha)=0 equals the zero received core datum",
            "the missed core is exactly D\\Z(V), hence has size at most two",
        ],
        "fixed_rank_nine": True,
        "full_rank_bound_per_key": 1,
        "compatible_rankdrop_gcd_positive": True,
        "exact_d3_migration_under_bridge": True,
        "distribution_independent_core": (
            "the common-factor proof uses only deg(B)=6 and deg(F)+deg(V)<=5"
        ),
        "specialized_degree_partition": [3, 2, 1],
        "specialized_quotient_degrees": [0, 1, 2],
    }


def expected_bridge_certificate():
    bridge = bridge_positive_control()
    return {
        "positive_control": bridge,
        "validator_accepts_positive_control": validate_bridge_control(bridge),
        "exact_missed_core_formula": "D\\Z(V)",
    }


def expected_numerical_evidence_limit():
    return (
        "the frozen GF19 census is exact but its 44 reduced rank drops are "
        "all affine-inconsistent; the compatible-rankdrop implication is "
        "proved algebraically and is not observed nonvacuously in this row"
    )


def expected_nonclaims(banked):
    return [
        (
            "the certificate banks only the reviewed 21,888 to 1,152 local replacement"
            if banked
            else "the certificate does not bank the 21,888 to 1,152 replacement"
        ),
        "the prior 31222 reviews are imported as algebraic provenance, not as review of this specialization",
        "no m>2 statement is made",
        "no PR #763 application is made",
        "no Lean formalization is claimed",
        "no global mixed-petal theorem is proved",
    ]


def build_report():
    symbolic = symbolic_total_degree_map()
    census = frozen_gf19_census()
    review_gate = fresh_review_gate()
    banked = bool(review_gate["satisfied"])
    return {
        "schema": "rs-mca-l1-b9-frontier-31321-total-degree-crt-v1",
        "status": (
            "PROVED_LOCAL_ALGEBRA_EXACT_GF19_CONTROL_FRESH_REVIEWS_GREEN"
            if banked
            else "PROVED_LOCAL_ALGEBRA_EXACT_GF19_CONTROL_PENDING_FRESH_REVIEW"
        ),
        "statement": expected_statement(),
        "parameters": expected_parameters(),
        "frozen_system": expected_frozen_system(symbolic),
        "proof_certificate": expected_proof_certificate(),
        "pointwise_bridge_certificate": expected_bridge_certificate(),
        "exact_GF19": census,
        "prior_nonvacuous_total_degree_control": (
            prior_nonvacuous_total_degree_control()
        ),
        "numerical_evidence_limit": expected_numerical_evidence_limit(),
        "linked_inputs": linked_inputs(),
        "fresh_review_gate": review_gate,
        "ledger_consequence": {
            "candidate_support_pattern_count": 1_152,
            "candidate_prior_charge": 21_888,
            "candidate_replacement_charge_after_fresh_green_review": 1_152,
            "banked": banked,
            "authorization": (
                "YES_TWO_HASH_LINKED_GREEN_REVIEWS"
                if banked
                else "NO_PENDING_TWO_HASH_LINKED_GREEN_REVIEWS"
            ),
        },
        "nonclaims": expected_nonclaims(banked),
        "verdict": (
            "GREEN_LOCAL_31321_LEMMA_LEDGER_AUTHORIZED"
            if banked
            else "YELLOW_LOCAL_PACKET_PENDING_FRESH_INDEPENDENT_REVIEW"
        ),
    }


def validate_report(report):
    try:
        census = report["exact_GF19"]
        review_gate = fresh_review_gate()
        banked = bool(review_gate["satisfied"])
        expected_status = (
            "PROVED_LOCAL_ALGEBRA_EXACT_GF19_CONTROL_FRESH_REVIEWS_GREEN"
            if banked
            else "PROVED_LOCAL_ALGEBRA_EXACT_GF19_CONTROL_PENDING_FRESH_REVIEW"
        )
        expected_ledger = {
            "candidate_support_pattern_count": 1_152,
            "candidate_prior_charge": 21_888,
            "candidate_replacement_charge_after_fresh_green_review": 1_152,
            "banked": banked,
            "authorization": (
                "YES_TWO_HASH_LINKED_GREEN_REVIEWS"
                if banked
                else "NO_PENDING_TWO_HASH_LINKED_GREEN_REVIEWS"
            ),
        }
        expected_verdict = (
            "GREEN_LOCAL_31321_LEMMA_LEDGER_AUTHORIZED"
            if banked
            else "YELLOW_LOCAL_PACKET_PENDING_FRESH_INDEPENDENT_REVIEW"
        )
        prior_control = report["prior_nonvacuous_total_degree_control"]
        return bool(
            report["schema"]
            == "rs-mca-l1-b9-frontier-31321-total-degree-crt-v1"
            and report["status"] == expected_status
            and report["statement"] == expected_statement()
            and report["parameters"] == expected_parameters()
            and report["frozen_system"]
            == expected_frozen_system(symbolic_total_degree_map())
            and report["proof_certificate"] == expected_proof_certificate()
            and report["pointwise_bridge_certificate"]
            == expected_bridge_certificate()
            and census["field"] == 19
            and census["domain"]
            == [1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10]
            and census["support_pattern_count"] == 1_152
            and census["canonical_assignment_count"] == 1_152
            and census["canonical_assignment_order_sha256"]
            == "314b4052c07e3e19fd803e04487f80f823470d77a1240db21b6f9f5fefada4be"
            and census["canonical_assignment_set_sha256"]
            == "2f76b435d74bf50a6a904da9fb1df58a09bdd02c07fd7f973e27fe142933c565"
            and census["support_pattern_formula"]
            == "binom(2,1)*3!*binom(4,3)*binom(4,2)*binom(4,1)=1152"
            and census["support_degree_order_histogram"]
            == {
                "123": 192,
                "132": 192,
                "213": 192,
                "231": 192,
                "312": 192,
                "321": 192,
            }
            and census["fixed_matrix_rank_histogram"] == {"9": 1_152}
            and census["fixed_actual_augmented_rank_histogram"]
            == {"rankA=9,rankAug=9": 1, "rankA=9,rankAug=10": 4_607}
            and census["moving_rank_histogram"]
            == {"rankC=11,rankAug=12": 44, "rankC=12,rankAug=12": 1_108}
            and census["reduced_rank_histogram"]
            == {"rankM=2,rankAug=3": 44, "rankM=3,rankAug=3": 1_108}
            and census["monic_solution_count_histogram"] == {"0": 44, "1": 1_108}
            and census["full_rank_pattern_count"] == 1_108
            and census["full_rank_monic_solution_count"] == 1_108
            and census["compatible_rankdrop_pattern_count"] == 0
            and census["compatible_rankdrop_monic_solution_count"] == 0
            and census["compatible_rankdrop_gcd_degree_histogram"] == {}
            and census["compatible_rankdrop_patterns"] == []
            and census["compatible_rankdrop_zero_gcd_count"] == 0
            and not census["compatible_rankdrop_zero_gcd_examples"]
            and census["rankdrop_implication_GF19_status"]
            == "VACUOUS_ALL_44_RANK_DROPS_ARE_AFFINE_INCONSISTENT"
            and census["actual_split_core_incidence_count"] == 1
            and census["actual_rankdrop_incidence_count"] == 0
            and census["actual_rankdrop_bridge_failure_count"] == 0
            and census["transcript_sha256"]
            == "2256ea69620c10d5c15012df4ebce046babaaa3e314b948221eeb3107ad80972"
            and prior_control == prior_nonvacuous_total_degree_control()
            and prior_control["schema"]
            == "rs-mca-l1-b9-frontier-31222-reduced-crt-lemma-v3"
            and prior_control["support_locator_degrees"] == [2, 2, 2]
            and prior_control["deg_B"] == 6
            and prior_control["deg_R"] == 1
            and prior_control["deg_F"] == 3
            and prior_control["deg_V_max"] == 2
            and prior_control["compatible_rankdrop_pattern_count"] == 2
            and prior_control["compatible_rankdrop_monic_cubic_count"] == 38
            and prior_control["compatible_rankdrop_zero_gcd_count"] == 0
            and prior_control["reviewed_verdict"]
            == "GREEN_LOCAL_LEMMA_LEDGER_AUTHORIZED"
            and report["numerical_evidence_limit"]
            == expected_numerical_evidence_limit()
            and report["linked_inputs"] == linked_inputs()
            and report["fresh_review_gate"] == review_gate
            and report["ledger_consequence"] == expected_ledger
            and report["nonclaims"] == expected_nonclaims(banked)
            and report["verdict"] == expected_verdict
        )
    except (KeyError, TypeError, ValueError, ArithmeticError):
        return False


def tamper_selftest(report):
    mutations = []

    changed = copy.deepcopy(report)
    changed["parameters"]["support_locator_degrees_sorted"] = [2, 2, 2]
    mutations.append(("degree_partition", changed))
    changed = copy.deepcopy(report)
    changed["parameters"]["quotient_degrees_for_sorted_supports"] = [1, 1, 1]
    mutations.append(("quotient_degrees", changed))
    changed = copy.deepcopy(report)
    changed["parameters"]["labels"] = [0, 2, 3]
    mutations.append(("zero_label", changed))
    changed = copy.deepcopy(report)
    changed["parameters"]["core_size"] = 5
    mutations.append(("core_size", changed))
    changed = copy.deepcopy(report)
    changed["parameters"]["support_locator_hypotheses"] = "coprimality deleted"
    mutations.append(("support_locator_hypotheses", changed))
    changed = copy.deepcopy(report)
    changed["parameters"]["profile_bridge_hypotheses"] = []
    mutations.append(("profile_bridge_hypotheses", changed))
    changed = copy.deepcopy(report)
    changed["parameters"]["bridge_hypotheses"] = []
    mutations.append(("bridge_hypotheses", changed))
    changed = copy.deepcopy(report)
    changed["frozen_system"]["fixed_F_matrix_shape"] = [12, 8]
    mutations.append(("fixed_matrix_shape", changed))
    changed = copy.deepcopy(report)
    changed["frozen_system"]["moving_monic_F_matrix_shape"] = [12, 11]
    mutations.append(("moving_matrix_shape", changed))
    changed = copy.deepcopy(report)
    changed["frozen_system"]["compatibility_degrees"] = [2, 3, 4]
    mutations.append(("compatibility_degrees", changed))
    changed = copy.deepcopy(report)
    changed["frozen_system"]["rank_relation"] = "rank(C_12x12)=0"
    mutations.append(("rank_relation", changed))
    changed = copy.deepcopy(report)
    changed["frozen_system"]["symbolic_total_degree_map"]["M_rows"] = [
        ["0", "0", "0"],
        ["0", "0", "0"],
        ["0", "0", "0"],
    ]
    mutations.append(("symbolic_reduced_matrix", changed))
    changed = copy.deepcopy(report)
    changed["proof_certificate"]["full_rank_bound_per_key"] = 19
    mutations.append(("full_rank_bound", changed))
    changed = copy.deepcopy(report)
    changed["exact_GF19"]["compatible_rankdrop_zero_gcd_count"] = 1
    mutations.append(("rankdrop_zero_gcd", changed))
    changed = copy.deepcopy(report)
    changed["exact_GF19"]["actual_rankdrop_bridge_failure_count"] = 1
    mutations.append(("finite_bridge", changed))
    changed = copy.deepcopy(report)
    changed["exact_GF19"]["moving_rank_histogram"]["rankC=12,rankAug=12"] -= 1
    mutations.append(("moving_rank_histogram", changed))
    changed = copy.deepcopy(report)
    changed["exact_GF19"]["transcript_sha256"] = "0" * 64
    mutations.append(("transcript_hash", changed))
    changed = copy.deepcopy(report)
    changed["exact_GF19"]["canonical_assignment_set_sha256"] = "0" * 64
    mutations.append(("canonical_assignment_set", changed))
    changed = copy.deepcopy(report)
    changed["exact_GF19"]["canonical_assignment_order_sha256"] = "0" * 64
    mutations.append(("canonical_assignment_order", changed))
    changed = copy.deepcopy(report)
    changed["exact_GF19"]["canonical_assignment_count"] = 1_151
    mutations.append(("duplicate_support_key", changed))
    changed = copy.deepcopy(report)
    changed["prior_nonvacuous_total_degree_control"][
        "compatible_rankdrop_monic_cubic_count"
    ] = 37
    mutations.append(("prior_nonvacuous_control", changed))

    bridge_path = ["pointwise_bridge_certificate", "positive_control"]
    changed = copy.deepcopy(report)
    control = changed[bridge_path[0]][bridge_path[1]]
    control["background_roots"] = [control["core_roots"][0]]
    mutations.append(("core_background_overlap", changed))
    changed = copy.deepcopy(report)
    control = changed[bridge_path[0]][bridge_path[1]]
    control["common_root_alpha"] = control["restored_core_root"]
    mutations.append(("alpha_equals_h", changed))
    changed = copy.deepcopy(report)
    control = changed[bridge_path[0]][bridge_path[1]]
    control["received_core_values"][0] = 1
    mutations.append(("nonzero_core_data", changed))
    changed = copy.deepcopy(report)
    control = changed[bridge_path[0]][bridge_path[1]]
    control["received_background_values"][0] = 1
    mutations.append(("nonzero_background_data", changed))
    changed = copy.deepcopy(report)
    control = changed[bridge_path[0]][bridge_path[1]]
    field = GF(int(control["field"]))
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    roots = [field(value) for value in control["missed_core_roots"]]
    repeated = (X - roots[0])**2 * (X - roots[1])
    control["F_coefficients_low_to_high"] = coefficients_low_to_high(repeated, 3)
    mutations.append(("repeated_core_locator", changed))
    changed = copy.deepcopy(report)
    control = changed[bridge_path[0]][bridge_path[1]]
    field = GF(int(control["field"]))
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    nonsplit = X**3 + X + field(4)
    if not nonsplit.is_irreducible():
        raise RuntimeError("nonsplit mutation control drift")
    control["F_coefficients_low_to_high"] = coefficients_low_to_high(nonsplit, 3)
    mutations.append(("nonsplit_core_locator", changed))

    for link_name in (
        "prior_31222_certificate",
        "prior_31222_sage_verifier",
        "prior_31222_lemma",
        "prior_31222_independent_review",
        "prior_31222_cross_model_yellow",
        "prior_31222_cross_model_green",
        "current_31321_independent_yellow",
        "current_31321_cross_model_attempt1",
    ):
        changed = copy.deepcopy(report)
        changed["linked_inputs"][link_name]["sha256"] = "0" * 64
        mutations.append((link_name, changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["banked"] = not bool(
        changed["ledger_consequence"]["banked"]
    )
    mutations.append(("ledger_bank_flag", changed))

    changed = copy.deepcopy(report)
    changed["fresh_review_gate"]["satisfied"] = not bool(
        changed["fresh_review_gate"]["satisfied"]
    )
    mutations.append(("review_gate_status", changed))

    for review_name, review in report["fresh_review_gate"]["reviews"].items():
        if not review["exists"]:
            continue
        changed = copy.deepcopy(report)
        changed["fresh_review_gate"]["reviews"][review_name]["sha256"] = "0" * 64
        mutations.append((f"fresh_{review_name}_hash", changed))

    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<34}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))

    if args.tamper_selftest and CERTIFICATE_PATH.exists():
        report = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    else:
        report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (total-degree-six CRT validation)", file=sys.stderr)
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
        print("RESULT: FAIL (frozen total-degree CRT certificate drift)", file=sys.stderr)
        return 1

    census = report["exact_GF19"]
    print("L1 B9 frontier (3,1,3,(3,2,1)) total-degree-six reduced-CRT lemma")
    print(f"  fixed-F matrix: {report['frozen_system']['fixed_F_matrix_shape']}, rank 9")
    print(f"  moving matrix: {report['frozen_system']['moving_monic_F_matrix_shape']}")
    print(f"  support patterns: {census['support_pattern_count']}")
    print(f"  moving ranks: {census['moving_rank_histogram']}")
    print(f"  reduced ranks: {census['reduced_rank_histogram']}")
    print(
        "  compatible rank drops: "
        f"{census['compatible_rankdrop_pattern_count']}; "
        f"zero-gcd={census['compatible_rankdrop_zero_gcd_count']}"
    )
    print(
        "  actual rank-drop split-core incidences: "
        f"{census['actual_rankdrop_incidence_count']}; "
        f"bridge failures={census['actual_rankdrop_bridge_failure_count']}"
    )
    print(f"  transcript: {census['transcript_sha256']}")
    print(f"  ledger banked: {report['ledger_consequence']['banked']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(int(main(sys.argv[1:])))
