#!/usr/bin/env sage
"""Exact Sage census for the genuine mixed-petal ``(2,1,1)`` fixture.

The word is the sequential sunflower at ``(p,n,k,s)=(17,16,6,7)``.  Its
core has five coordinates, its five petals have two coordinates each, and
one background coordinate remains.  For every two-point core defect ``D``
the script enumerates the exact 120 labelled outside-core support templates

    5 * binom(4,2) * 2^2 = 120,

so the full finite census contains 1,200 fixed-support systems.  For each
template it solves both

    W - c_i L_D = L_{S_i} A_i

and the two independent pairwise-difference equations.  The coefficient
systems are respectively 9-by-8 and 6-by-5 over GF(17).  Exact agreement
support and the repository's independent support-subset decoder are checked
after reconstruction.

This is an exact tiny-case falsification fixture.  It does not promote a
finite full-rank census into the required uniform Padé-rank dichotomy.
"""

from __future__ import annotations

import argparse
import builtins
import hashlib
import itertools
import json
import sys
from pathlib import Path

from sage.rings.integer import Integer as SageInteger


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experimental/scripts"))

from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    img_list,
    mask_from_indices,
    stabilizer_order,
    subgroup,
    sunflower_word_from_blocks,
)


CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-mixed-petal-template-211/certificate.json"
)


def locator(R, X, field, domain, indices):
    out = R.one()
    for index in indices:
        out *= X - field(domain[index])
    return out


def canonical_poly(poly):
    if poly == 0:
        return []
    return [int(poly[index]) for index in range(poly.degree() + 1)]


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, SageInteger):
        return int(value)
    return value


def incidence_system(R, X, field, F, touched):
    """Return the full and W-eliminated affine systems.

    ``touched`` consists of ``(scalar, support_locator)`` pairs.  Its support
    degrees must be a labelled permutation of ``(2,1,1)``.
    """
    zero = R.zero()
    one = R.one()
    cofactor_degrees = tuple(2 - B.degree() for _, B in touched)
    if sorted(cofactor_degrees) != [0, 1, 1]:
        raise ValueError("expected cofactor degrees (0,1,1)")

    offsets = []
    next_column = 3
    pair_offsets = []
    next_pair_column = 0
    for degree in cofactor_degrees:
        offsets.append(next_column)
        pair_offsets.append(next_pair_column)
        next_column += degree + 1
        next_pair_column += degree + 1
    if next_column != 8 or next_pair_column != 5:
        raise RuntimeError("(2,1,1) should have eight/full and five/pair unknowns")

    rows = []
    rhs = []
    for (scalar, B), degree, offset in zip(
        touched, cofactor_degrees, offsets, strict=True
    ):
        columns = [one, X, X**2] + [zero] * 5
        for shift in range(degree + 1):
            columns[offset + shift] = -(X**shift) * B
        for coefficient_degree in range(3):
            rows.append(
                [column[coefficient_degree] for column in columns]
            )
            rhs.append((scalar * F)[coefficient_degree])

    base_scalar, base_B = touched[0]
    base_degree = cofactor_degrees[0]
    base_offset = pair_offsets[0]
    pair_rows = []
    pair_rhs = []
    for index in range(1, len(touched)):
        scalar, B = touched[index]
        degree = cofactor_degrees[index]
        offset = pair_offsets[index]
        columns = [zero] * 5
        for shift in range(base_degree + 1):
            columns[base_offset + shift] = (X**shift) * base_B
        for shift in range(degree + 1):
            columns[offset + shift] = -(X**shift) * B
        target = (scalar - base_scalar) * F
        for coefficient_degree in range(3):
            pair_rows.append(
                [column[coefficient_degree] for column in columns]
            )
            pair_rhs.append(target[coefficient_degree])

    matrix_A = matrix(field, rows)
    vector_b = vector(field, rhs)
    matrix_pair = matrix(field, pair_rows)
    vector_pair = vector(field, pair_rhs)
    return matrix_A, vector_b, matrix_pair, vector_pair, cofactor_degrees, offsets


def solve_incidence(R, X, field, F, touched):
    A, b, pair_A, pair_b, cofactor_degrees, offsets = incidence_system(
        R, X, field, F, touched
    )
    H = A.augment(b.column())
    pair_H = pair_A.augment(pair_b.column())
    rank = A.rank()
    augmented_rank = H.rank()
    pair_rank = pair_A.rank()
    pair_augmented_rank = pair_H.rank()
    if rank != pair_rank + 3 or augmented_rank != pair_augmented_rank + 3:
        raise RuntimeError("full and pairwise-difference ranks disagree")
    if rank != augmented_rank:
        status = "INCONSISTENT"
        solution = None
    elif rank != A.ncols():
        status = "POSITIVE_DIMENSIONAL"
        solution = None
    else:
        status = "UNIQUE"
        vector_solution = A.solve_right(b)
        W = sum(vector_solution[j] * X**j for j in range(3))
        cofactors = []
        for degree, offset in zip(cofactor_degrees, offsets, strict=True):
            cofactors.append(
                sum(
                    vector_solution[offset + shift] * X**shift
                    for shift in range(degree + 1)
                )
            )
        for (scalar, B), cofactor in zip(touched, cofactors, strict=True):
            if W - scalar * F != B * cofactor:
                raise RuntimeError("incidence reconstruction failed")
        solution = (W, tuple(cofactors))
    return {
        "rank": rank,
        "augmented_rank": augmented_rank,
        "pair_rank": pair_rank,
        "pair_augmented_rank": pair_augmented_rank,
        "status": status,
        "solution": solution,
    }


def has_exact_support(W, F, field, domain, D, background, petals, supports, scalars):
    if any(W(field(domain[index])) == 0 for index in D):
        return False
    if any(W(field(domain[index])) == 0 for index in background):
        return False
    for scalar, petal, support in zip(scalars, petals, supports, strict=True):
        difference = W - scalar * F
        support_set = set(support)
        for index in petal:
            if (difference(field(domain[index])) == 0) != (index in support_set):
                return False
    return True


def support_templates(petals):
    """Yield all 120 labelled outside-core ``(2,1,1)`` templates."""
    for full_index in range(len(petals)):
        remaining = [index for index in range(len(petals)) if index != full_index]
        for singleton_indices in itertools.combinations(remaining, 2):
            for singleton_points in itertools.product(
                *(petals[index] for index in singleton_indices)
            ):
                supports = [tuple() for _ in petals]
                supports[full_index] = tuple(petals[full_index])
                for index, point in zip(
                    singleton_indices, singleton_points, strict=True
                ):
                    supports[index] = (point,)
                yield tuple(supports)


def compatibility_line(field, R, X, domain, supports, scalars):
    """Return the normalized affine compatibility line for one template."""
    full_indices = [index for index, support in enumerate(supports) if len(support) == 2]
    singleton_indices = [
        index for index, support in enumerate(supports) if len(support) == 1
    ]
    if len(full_indices) != 1 or len(singleton_indices) != 2:
        raise ValueError("expected one full and two singleton supports")
    full_index = full_indices[0]
    first_index, second_index = singleton_indices
    B_full = locator(R, X, field, domain, supports[full_index])
    gamma = field(domain[supports[first_index][0]])
    delta = field(domain[supports[second_index][0]])
    delta_first = field(scalars[first_index] - scalars[full_index])
    delta_second = field(scalars[second_index] - scalars[full_index])
    B_gamma = B_full(gamma)
    B_delta = B_full(delta)
    if B_gamma == 0 or B_delta == 0:
        raise RuntimeError("disjoint petal supports produced a zero rank minor")
    coefficients = (
        delta_first * B_delta - delta_second * B_gamma,
        delta_first * gamma * B_delta - delta_second * delta * B_gamma,
        delta_first * gamma**2 * B_delta - delta_second * delta**2 * B_gamma,
    )
    if not any(coefficients):
        raise RuntimeError("compatibility equation vanished identically")
    pivot = next(value for value in coefficients if value != 0)
    normalized = tuple(int(value / pivot) for value in coefficients)
    return {
        "normalized_coefficients_f0_f1_constant": normalized,
        "full_index": full_index,
        "singleton_indices": (first_index, second_index),
        "B_full": B_full,
        "gamma": gamma,
        "delta": delta,
        "delta_first": delta_first,
        "delta_second": delta_second,
        "B_gamma": B_gamma,
        "B_delta": B_delta,
    }


def symbolic_rank_certificate():
    """Prove a nonzero maximal minor over the universal integer ring."""
    S = PolynomialRing(ZZ, names=("u", "v", "x", "y"))
    u, v, x, y = S.gens()
    T = PolynomialRing(S, "Z")
    Z = T.gen()
    zero = T.zero()
    one = T.one()
    locators = ((Z - u) * (Z - v), Z - x, Z - y)
    cofactor_degrees = (0, 1, 1)
    offsets = (3, 4, 6)
    rows = []
    for B, degree, offset in zip(
        locators, cofactor_degrees, offsets, strict=True
    ):
        columns = [one, Z, Z**2] + [zero] * 5
        for shift in range(degree + 1):
            columns[offset + shift] = -(Z**shift) * B
        for coefficient_degree in range(3):
            rows.append(
                [column[coefficient_degree] for column in columns]
            )
    full_matrix = matrix(S, rows)
    full_rows = [0, 1, 2, 4, 5, 6, 7, 8]
    full_minor = full_matrix.matrix_from_rows(full_rows).det()

    pair_rows = []
    pair_offsets = (0, 1, 3)
    for index in (1, 2):
        columns = [zero] * 5
        for shift in range(cofactor_degrees[0] + 1):
            columns[pair_offsets[0] + shift] = (
                Z**shift
            ) * locators[0]
        for shift in range(cofactor_degrees[index] + 1):
            columns[pair_offsets[index] + shift] = -(
                Z**shift
            ) * locators[index]
        for coefficient_degree in range(3):
            pair_rows.append(
                [column[coefficient_degree] for column in columns]
            )
    pair_matrix = matrix(S, pair_rows)
    pair_selected_rows = [1, 2, 3, 4, 5]
    pair_minor = pair_matrix.matrix_from_rows(pair_selected_rows).det()
    expected = (y - u) * (y - v)
    if full_minor != expected or pair_minor != expected:
        raise RuntimeError("universal maximal-minor identity drift")

    U = PolynomialRing(
        ZZ, names=("u", "v", "x", "y", "Delta_x", "Delta_y", "f0", "f1")
    )
    u0, v0, x0, y0, Delta_x, Delta_y, f0, f1 = U.gens()
    augmented_pair = matrix(
        U,
        [
            [u0 * v0, x0, 0, 0, 0, Delta_x * f0],
            [-(u0 + v0), -1, x0, 0, 0, Delta_x * f1],
            [1, 0, -1, 0, 0, Delta_x],
            [u0 * v0, 0, 0, y0, 0, Delta_y * f0],
            [-(u0 + v0), 0, 0, -1, y0, Delta_y * f1],
            [1, 0, 0, 0, -1, Delta_y],
        ],
    )
    B_x = (x0 - u0) * (x0 - v0)
    B_y = (y0 - u0) * (y0 - v0)
    F_x = x0**2 + f1 * x0 + f0
    F_y = y0**2 + f1 * y0 + f0
    augmented_expected = Delta_y * F_y * B_x - Delta_x * F_x * B_y
    if augmented_pair.det() != augmented_expected:
        raise RuntimeError("universal augmented-determinant identity drift")
    return {
        "coefficient_ring": "ZZ[u,v,x,y]",
        "canonical_block_order": ["full_support_uv", "singleton_x", "singleton_y"],
        "full_minor_rows_zero_based": full_rows,
        "pair_minor_rows_zero_based": pair_selected_rows,
        "full_minor": str(full_minor),
        "pair_minor": str(pair_minor),
        "locator_evaluation": "B_full(y)=(y-u)(y-v)",
        "nonvanishing_condition": "y is distinct from u and v",
        "rank_deficient_components_on_disjoint_chart": 0,
        "augmented_coefficient_ring": (
            "ZZ[u,v,x,y,Delta_x,Delta_y,f0,f1]"
        ),
        "augmented_determinant": (
            "Delta_y F(y) B_full(x) - Delta_x F(x) B_full(y)"
        ),
        "compatibility_zero_equation_verified": True,
    }


def build_report():
    p, n, k, s = 17, 16, 6, 7
    field = GF(p)
    R = PolynomialRing(field, "X")
    X = R.gen()
    domain = subgroup(p, n)
    core = tuple(range(5))
    petals = tuple(tuple(range(5 + 2 * j, 7 + 2 * j)) for j in range(5))
    background = (15,)
    scalars = (1, 2, 3, 4, 5)

    word = sunflower_word_from_blocks(
        p,
        n,
        k,
        s,
        list(core),
        [list(petal) for petal in petals],
        "sunflower-sequential-m5",
    )
    if word is None:
        raise RuntimeError("failed to construct the sequential sunflower")
    values = word["values"]
    L_C = locator(R, X, field, domain, core)
    expected_values = [0] * n
    for scalar, petal in zip(scalars, petals, strict=True):
        for index in petal:
            expected_values[index] = int(scalar * L_C(field(domain[index])))
    if values != expected_values:
        raise RuntimeError("sunflower constructor disagrees with its equations")

    templates = list(support_templates(petals))
    if len(templates) != 120 or len(set(templates)) != 120:
        raise RuntimeError("outside-core support-template count drift")

    symbolic_rank = symbolic_rank_certificate()
    line_multiplicities = {}
    template_lines = {}
    template_exact_counts = {}
    for supports in templates:
        template_key = tuple(tuple(support) for support in supports)
        line = compatibility_line(
            field, R, X, domain, supports, scalars
        )["normalized_coefficients_f0_f1_constant"]
        template_lines[template_key] = line
        line_multiplicities[line] = line_multiplicities.get(line, 0) + 1
        template_exact_counts[template_key] = 0

    raw_systems = 0
    full_rank_histogram = {}
    pair_rank_histogram = {}
    status_histogram = {}
    exact_by_D = {}
    rank_deficient = []
    consistent_not_exact = []
    consistent_not_exact_count = 0
    nonexact_reason_histogram = {}
    compatibility_true_count = 0
    canonical = []
    rank_transcript = []

    for D in itertools.combinations(core, 2):
        F = locator(R, X, field, domain, D)
        core_quotient, remainder = L_C.quo_rem(F)
        if remainder != 0:
            raise RuntimeError("core defect locator does not divide the core locator")
        exact_by_D[str(list(D))] = 0
        for supports in templates:
            raw_systems += 1
            touched = []
            for scalar, support in zip(scalars, supports, strict=True):
                if support:
                    touched.append(
                        (scalar, locator(R, X, field, domain, support))
                    )
            if len(touched) != 3:
                raise RuntimeError("profile should touch exactly three petals")
            compatibility = compatibility_line(
                field, R, X, domain, supports, scalars
            )
            line = compatibility["normalized_coefficients_f0_f1_constant"]
            line_holds = (
                field(line[0]) * F[0]
                + field(line[1]) * F[1]
                + field(line[2])
                == 0
            )
            direct_compatibility = (
                compatibility["delta_first"]
                * F(compatibility["gamma"])
                * compatibility["B_delta"]
                == compatibility["delta_second"]
                * F(compatibility["delta"])
                * compatibility["B_gamma"]
            )
            if line_holds != direct_compatibility:
                raise RuntimeError("normalized and evaluation compatibility disagree")
            compatibility_true_count += int(line_holds)
            solved = solve_incidence(R, X, field, F, tuple(touched))
            full_key = (
                f"rank={solved['rank']},augmented_rank={solved['augmented_rank']}"
            )
            pair_key = (
                f"rank={solved['pair_rank']},"
                f"augmented_rank={solved['pair_augmented_rank']}"
            )
            full_rank_histogram[full_key] = full_rank_histogram.get(full_key, 0) + 1
            pair_rank_histogram[pair_key] = pair_rank_histogram.get(pair_key, 0) + 1
            status = solved["status"]
            if line_holds != (status != "INCONSISTENT"):
                raise RuntimeError("compatibility determinant and affine rank disagree")
            status_histogram[status] = status_histogram.get(status, 0) + 1
            rank_row = {
                "D": list(D),
                "supports": [list(support) for support in supports],
                "rank": solved["rank"],
                "augmented_rank": solved["augmented_rank"],
                "pair_rank": solved["pair_rank"],
                "pair_augmented_rank": solved["pair_augmented_rank"],
                "status": status,
            }
            rank_transcript.append(rank_row)
            if status == "POSITIVE_DIMENSIONAL":
                rank_deficient.append(rank_row)
                continue
            if status == "INCONSISTENT":
                continue
            if status != "UNIQUE" or solved["solution"] is None:
                raise RuntimeError(f"unhandled incidence status {status}")

            W, cofactors = solved["solution"]
            P = core_quotient * W
            if P.degree() >= k:
                raise RuntimeError("reconstructed polynomial exceeds the RS degree bound")
            exact_support = has_exact_support(
                W,
                F,
                field,
                domain,
                D,
                background,
                petals,
                supports,
                scalars,
            )
            codeword = tuple(int(P(field(value))) for value in domain)
            agreement = [
                index
                for index, (left, right) in enumerate(
                    zip(codeword, values, strict=True)
                )
                if left == right
            ]
            expected = sorted(
                (set(core) - set(D)).union(
                    *(set(support) for support in supports)
                )
            )
            if not set(expected).issubset(agreement):
                raise RuntimeError("a prescribed agreement disappeared")
            if exact_support != (agreement == expected):
                raise RuntimeError("exact-support predicates disagree")
            if not exact_support:
                consistent_not_exact_count += 1
                extras = sorted(set(agreement) - set(expected))
                reasons = []
                if set(extras) & set(background):
                    reasons.append("BACKGROUND_EXTRA")
                if set(extras) & set(D):
                    reasons.append("CORE_DEFECT_EXTRA")
                touched_indices = {
                    index for index, support in enumerate(supports) if support
                }
                touched_points = set().union(
                    *(set(petals[index]) for index in touched_indices)
                )
                untouched_points = set().union(
                    *(
                        set(petals[index])
                        for index in range(len(petals))
                        if index not in touched_indices
                    )
                )
                if set(extras) & touched_points:
                    reasons.append("TOUCHED_PETAL_EXTRA")
                if set(extras) & untouched_points:
                    reasons.append("UNTOUCHED_PETAL_EXTRA")
                if not reasons:
                    raise RuntimeError("unclassified extra agreement")
                reason_key = "+".join(reasons)
                nonexact_reason_histogram[reason_key] = (
                    nonexact_reason_histogram.get(reason_key, 0) + 1
                )
                if len(consistent_not_exact) < 12:
                    consistent_not_exact.append(
                        {
                            "D": list(D),
                            "supports": [list(support) for support in supports],
                            "W": canonical_poly(W),
                            "extra_agreement_indices": extras,
                            "reason": reason_key,
                        }
                    )
                continue
            mask = mask_from_indices(agreement)
            exact_by_D[str(list(D))] += 1
            template_key = tuple(tuple(support) for support in supports)
            template_exact_counts[template_key] += 1
            canonical.append(
                {
                    "D": list(D),
                    "supports": [list(support) for support in supports],
                    "F": canonical_poly(F),
                    "W": canonical_poly(W),
                    "cofactors": [canonical_poly(cofactor) for cofactor in cofactors],
                    "P": canonical_poly(P),
                    "agreement_mask": mask,
                    "stabilizer_order": stabilizer_order(mask, n),
                }
            )

    if raw_systems != 1200:
        raise RuntimeError(f"fixed-support system count drift: {raw_systems}")

    canonical.sort(key=lambda row: (row["D"], row["supports"], row["P"]))
    rank_transcript.sort(key=lambda row: (row["D"], row["supports"]))
    canonical_hash = hashlib.sha256(
        json.dumps(
            json_ready(canonical), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    rank_hash = hashlib.sha256(
        json.dumps(
            json_ready(rank_transcript), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()

    decoded = img_list(values, domain, k, s, p, "support")
    decoded_target = []
    core_set = set(core)
    petal_sets = [set(petal) for petal in petals]
    background_set = set(background)
    for codeword, mask in decoded.items():
        agreement = {index for index in range(n) if mask & (1 << index)}
        d = len(core_set - agreement)
        r = len(agreement & background_set)
        hits = sorted(
            [len(agreement & petal) for petal in petal_sets if agreement & petal],
            reverse=True,
        )
        if d == 2 and r == 0 and hits == [2, 1, 1]:
            decoded_target.append(
                {
                    "codeword": [int(value) for value in codeword],
                    "agreement_mask": mask,
                    "stabilizer_order": stabilizer_order(mask, n),
                }
            )
    decoded_target.sort(key=lambda row: (row["agreement_mask"], row["codeword"]))
    decoded_hash = hashlib.sha256(
        json.dumps(
            json_ready(decoded_target), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    enumerated_masks = sorted(row["agreement_mask"] for row in canonical)
    decoded_masks = sorted(row["agreement_mask"] for row in decoded_target)
    if len(enumerated_masks) != len(set(enumerated_masks)):
        raise RuntimeError("distinct fixed-support fibres produced a duplicate mask")
    if enumerated_masks != decoded_masks:
        raise RuntimeError("incidence census and exact list decoder disagree")

    primitive_count = sum(row["stabilizer_order"] == 1 for row in canonical)
    if primitive_count != len(canonical):
        raise RuntimeError("target fixture unexpectedly contains a periodic mask")

    realized_template_histogram = {}
    for count in template_exact_counts.values():
        realized_template_histogram[str(count)] = (
            realized_template_histogram.get(str(count), 0) + 1
        )
    compatibility_line_multiplicity_histogram = {}
    for multiplicity in line_multiplicities.values():
        key = str(multiplicity)
        compatibility_line_multiplicity_histogram[key] = (
            compatibility_line_multiplicity_histogram.get(key, 0) + 1
        )

    return json_ready(
        {
            "schema": "rs-mca-l1-mixed-petal-template-211-v1",
            "status": "EXPERIMENTAL/PIPELINE_CHECK",
            "row": {
                "p": p,
                "n": n,
                "k": k,
                "s": s,
                "sigma": 1,
                "ell": 2,
            },
            "layout": {
                "domain": domain,
                "core": list(core),
                "petals": [list(petal) for petal in petals],
                "background": list(background),
                "scalars": list(scalars),
            },
            "profile": {
                "d": 2,
                "r": 0,
                "t": 3,
                "a_i": [2, 1, 1],
                "d_minus_ell": 0,
                "G2": 1,
                "GR": 2,
                "lambda": 0,
                "lambda_J": 2,
                "lambda_minus_lambda_J": -2,
            },
            "systems": {
                "outside_core_support_templates_per_D": len(templates),
                "core_defect_choices": 10,
                "fixed_support_systems": raw_systems,
                "full_incidence_shape": [9, 8],
                "pairwise_difference_shape": [6, 5],
                "full_rank_histogram": dict(sorted(full_rank_histogram.items())),
                "pair_rank_histogram": dict(sorted(pair_rank_histogram.items())),
                "status_histogram": dict(sorted(status_histogram.items())),
                "consistent_incidence_tuples": status_histogram.get("UNIQUE", 0),
                "consistent_not_exact_count": consistent_not_exact_count,
                "consistent_not_exact_reason_histogram": dict(
                    sorted(nonexact_reason_histogram.items())
                ),
                "rank_deficient_fixed_support_systems": len(rank_deficient),
                "rank_transcript_sha256": rank_hash,
            },
            "symbolic_rank_certificate": symbolic_rank,
            "compatibility": {
                "equation": (
                    "(c_j-c_f)F(gamma)B_full(delta)="
                    "(c_k-c_f)F(delta)B_full(gamma)"
                ),
                "affine_line_coordinates": ["f0", "f1", "constant"],
                "distinct_normalized_lines": len(line_multiplicities),
                "line_multiplicity_histogram": dict(
                    sorted(compatibility_line_multiplicity_histogram.items())
                ),
                "compatible_fixed_support_systems": compatibility_true_count,
                "matches_affine_rank_status": True,
            },
            "census": {
                "exact_support_solutions": len(canonical),
                "primitive_exact_support_solutions": primitive_count,
                "exact_support_solutions_by_D": exact_by_D,
                "direct_solution_sha256": canonical_hash,
                "decoder_target_count": len(decoded_target),
                "decoder_target_sha256": decoded_hash,
                "agreement_masks_match_decoder": True,
                "outside_template_exact_count_histogram": dict(
                    sorted(realized_template_histogram.items())
                ),
                "maximum_exact_solutions_per_outside_template": max(
                    template_exact_counts.values()
                ),
                "consistent_not_exact_examples": consistent_not_exact,
            },
            "owner_routing": {
                "cut_parameters_for_unpaid_fixture": {"E": 0, "V2": 0, "VR": 0},
                "global_B10_johnson_paid_solutions": 0,
                "auxiliary_johnson_margin": -4,
                "cyclic_support_stabilizer_paid_solutions": 0,
                "paid_G2_at_V2_0": 0,
                "paid_G2_at_V2_at_least_1": len(canonical),
                "paid_GR_at_VR_0": 0,
                "unpaid_at_V2_0_after_known_owners": len(canonical),
                "unpaid_at_V2_at_least_1_after_known_owners": 0,
                "rank_deficient_components_on_disjoint_211_chart": 0,
                "full_rank_injective_fixed_support_fibres": raw_systems,
                "conclusion_at_V2_0": "UNPAID_FULL_RANK_INJECTIVE_TINY_FIXTURE",
                "conclusion_at_V2_at_least_1": "PAID_B11_G2",
            },
            "solution_records": canonical,
            "rank_deficient_records": rank_deficient,
            "nonclaims": [
                "fixed p=17,n=16,k=6,s=7 word, layout, and (2,1,1) profile only",
                "the uniform rank proof applies only to the disjoint (2,1,1) support chart",
                "does not uniformly count the moving-support compatibility hypersurface",
                "cyclic stabilizer one does not exclude every possible quotient descent",
                "does not close B11 or prove the fixed-syndrome Pade rank dichotomy",
            ],
        }
    )


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args(argv)
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
        print("RESULT: FAIL (frozen template certificate drift)", file=sys.stderr)
        return 1
    systems = actual["systems"]
    census = actual["census"]
    print(
        "[PASS] templates={templates}, systems={systems}, full={full}, pair={pair}, "
        "exact={exact}, decoder={decoder}".format(
            templates=systems["outside_core_support_templates_per_D"],
            systems=systems["fixed_support_systems"],
            full=systems["full_rank_histogram"],
            pair=systems["pair_rank_histogram"],
            exact=census["exact_support_solutions"],
            decoder=census["decoder_target_count"],
        )
    )
    print("RESULT: PASS (Sage pairwise-rank census matches exact list decoder)")
    return 0


if __name__ == "__main__":
    raise SystemExit(builtins.int(main(sys.argv[1:])))
