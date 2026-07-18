#!/usr/bin/env python3
"""Independent prime-field replay of the exact rank-one rank-nine control."""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "experimental/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import verify_m1_kb_rank9_deployed_source_incidence_contract_v1 as base


P = 1009
N = 50
K = 10
R = 40
J = 36
A = 14
T = 4
DOMAIN = list(range(N))

EPSILON_0_VALUES = [
    0, 0, 0, 0, 230, 809, 909, 167, 329, 6, 949, 40, 120, 718,
    959, 773, 221, 213, 6, 437, 170, 847, 272, 394, 658, 167,
    934, 522, 326, 158, 253, 38, 917, 887, 190,
]
EPSILON_1_VALUES = [
    649, 436, 380, 511, 674, 815, 980, 44, 602, 931, 1001, 738,
    362, 196, 873, 443, 182, 446, 468, 33, 377, 706, 164, 792,
    122, 45, 955, 939, 598, 119, 294, 438, 84, 708, 782,
]
RICH_SLOPES = list(range(1, 22)) + [47, 75, 547, 623, 657, 806, 819, 864, 934, 989]
OUTLIER_SLOPES = list(range(101, 109))
OUTLIER_CORES = [
    [1, 2, 3, 4, 5, 6, 7, 9, 11],
    [0, 1, 3, 4, 5, 6, 8, 9, 10],
    [0, 2, 3, 4, 7, 9, 10, 11, 12],
    [0, 2, 3, 4, 5, 6, 7, 10, 11],
    [0, 1, 3, 4, 6, 7, 8, 10, 12],
    [1, 2, 4, 7, 8, 9, 10, 11, 12],
    [1, 2, 3, 5, 8, 9, 10, 11, 12],
    [0, 2, 3, 4, 5, 8, 9, 11, 12],
]
OUTLIER_SOURCE_ZEROS = [
    [26, 30, 34, 39, 41],
    [16, 20, 21, 32, 38],
    [13, 15, 36, 40, 42],
    [14, 22, 37, 41, 42],
    [17, 27, 28, 31, 37],
    [23, 24, 29, 33, 35],
    [19, 34, 35, 36, 40],
    [18, 25, 38, 39, 43],
]
EXPECTED_MINORS = [
    227, 590, 650, 178, 261, 275, 912, 144, 286, 933, 978, 630, 405,
    117, 896, 143, 611, 315, 604, 107, 787, 696, 826, 896, 959, 969,
    9, 207, 492, 655, 330, 91, 90, 189, 589, 789, 595, 120, 793,
]

ContractError = base.ContractError
require = base.require
rank_mod = base.matrix_rank_mod
inverse_mod = base.inverse_mod


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % P
    return result


def root_polynomial(roots: list[int]) -> list[int]:
    result = [1]
    for root in roots:
        result = poly_mul(result, [(-root) % P, 1])
    return result


def poly_scale(polynomial: list[int], scalar: int) -> list[int]:
    return [(scalar * coefficient) % P for coefficient in polynomial]


def poly_add(left: list[int], right: list[int]) -> list[int]:
    width = max(len(left), len(right))
    return [
        ((left[index] if index < len(left) else 0)
         + (right[index] if index < len(right) else 0)) % P
        for index in range(width)
    ]


def poly_eval(polynomial: list[int], point: int) -> int:
    value = 0
    for coefficient in reversed(polynomial):
        value = (value * point + coefficient) % P
    return value


def evaluations(polynomial: list[int]) -> list[int]:
    return [poly_eval(polynomial, point) for point in DOMAIN]


def determinant_mod(matrix: list[list[int]]) -> int:
    require(matrix and len(matrix) == len(matrix[0]), "determinant matrix not square")
    work = [[entry % P for entry in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % P
        inverse = inverse_mod(pivot_value, P)
        work[column] = [entry * inverse % P for entry in work[column]]
        for row in range(column + 1, len(work)):
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[column])
                ]
    return determinant % P


def mat_vec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(left * right for left, right in zip(row, vector)) % P for row in matrix]


def restricted_membership(values: list[int], support: list[int]) -> bool:
    matrix = [[pow(DOMAIN[index], degree, P) for degree in range(K)] for index in support]
    augmented = [row + [values[index]] for row, index in zip(matrix, support)]
    return rank_mod(matrix, P) == rank_mod(augmented, P)


def build_control() -> dict[str, Any]:
    h_polynomial = root_polynomial(list(range(9)))
    require(h_polynomial == [0, 969, 397, 71, 319, 251, 509, 546, 973, 1], "H coefficients")
    h_values = evaluations(h_polynomial)
    epsilon_0 = [0] * 9 + EPSILON_0_VALUES + [0] * 6
    epsilon_1 = [0] * 9 + EPSILON_1_VALUES + [0] * 6
    sigma = {index for index, pair in enumerate(zip(epsilon_0, epsilon_1)) if pair != (0, 0)}
    require(sigma == set(range(9, 44)), "source support")

    lambdas = []
    for point in DOMAIN:
        denominator = 1
        for other in DOMAIN:
            if other != point:
                denominator = denominator * (point - other) % P
        lambdas.append(inverse_mod(denominator, P))
    parity = [
        [lambdas[column] * pow(DOMAIN[column], row, P) % P for column in range(N)]
        for row in range(R)
    ]
    generator = [[pow(point, degree, P) for point in DOMAIN] for degree in range(K)]
    require(rank_mod(parity, P) == R and rank_mod(generator, P) == K, "RS ranks")
    y_0 = mat_vec(parity, epsilon_0)
    y_1 = mat_vec(parity, epsilon_1)
    require(rank_mod([y_0, y_1], P) == 2, "source syndrome rank")

    records: list[dict[str, Any]] = []
    for slope in RICH_SLOPES:
        polynomial = poly_scale(h_polynomial, slope)
        codeword = evaluations(polynomial)
        error = [
            (left + slope * right - code) % P
            for left, right, code in zip(epsilon_0, epsilon_1, codeword)
        ]
        records.append({"slope": slope, "polynomial": polynomial, "error": error, "kind": "RICH"})

    q_polynomials = []
    for slope, core, source_zeros in zip(OUTLIER_SLOPES, OUTLIER_CORES, OUTLIER_SOURCE_ZEROS):
        q_polynomial = root_polynomial(core)
        polynomial = poly_add(poly_scale(h_polynomial, slope), q_polynomial)
        codeword = evaluations(polynomial)
        error = [
            (left + slope * right - code) % P
            for left, right, code in zip(epsilon_0, epsilon_1, codeword)
        ]
        zero = {index for index, value in enumerate(error) if value == 0}
        require(zero == set(core).union(source_zeros), "outlier zero set")
        q_polynomials.append(q_polynomial)
        records.append({"slope": slope, "polynomial": polynomial, "error": error, "kind": "OUTLIER"})

    moments = []
    for source in [epsilon_0, epsilon_1]:
        moments.append([
            sum(
                lambdas[index] * source[index] * pow(DOMAIN[index], degree, P)
                for index in range(N)
            ) % P
            for degree in range(R)
        ])
    M_0 = [[moments[0][row + column] for column in range(J + 1)] for row in range(T)]
    M_1 = [[moments[1][row + column] for column in range(J + 1)] for row in range(T)]

    errors = []
    supports = []
    minors = []
    for record in records:
        slope = record["slope"]
        error = record["error"]
        support = [index for index, value in enumerate(error) if value]
        zero = [index for index in range(N) if index not in support]
        require(len(support) == J and len(zero) == A, "weight/agreement")
        contained_0 = restricted_membership(epsilon_0, zero)
        contained_1 = restricted_membership(epsilon_1, zero)
        require(not contained_0 and not contained_1, "individual source containment")
        locator = root_polynomial(support)
        require(len(locator) == J + 1, "locator degree")
        matrix_slope = [
            [(M_0[row][column] + slope * M_1[row][column]) % P for column in range(J + 1)]
            for row in range(T)
        ]
        require(mat_vec(matrix_slope, locator) == [0] * T, "Hankel equation")
        require(mat_vec(M_1, locator) != [0] * T, "H2 locator")
        minor = determinant_mod([row[:T] for row in matrix_slope])
        require(minor, "regular minor")
        minors.append(minor)
        errors.append(error)
        supports.append(support)
    require(minors == EXPECTED_MINORS, "regular minor list")
    require(set().union(*(set(support) for support in supports)) == set(range(N)), "carrier")

    raw_rank = rank_mod(errors, P)
    affine_rows = [[(left - right) % P for left, right in zip(error, errors[0])] for error in errors[1:]]
    affine_rank = rank_mod(affine_rows, P)
    q_words = [evaluations(polynomial) for polynomial in q_polynomials]
    k0_rank = rank_mod(q_words, P)
    require((affine_rank, raw_rank, k0_rank) == (9, 10, 8), "rank tuple")
    require(rank_mod(affine_rows + q_words, P) == affine_rank, "K0 containment")
    intersection_rank = affine_rank + K - rank_mod(affine_rows + generator, P)
    require(intersection_rank == 8, "intersection rank")

    rich_common_zero = set(range(N))
    for record in records:
        if record["kind"] == "RICH":
            rich_common_zero &= {
                index for index, value in enumerate(record["error"]) if value == 0
            }
    require(rich_common_zero == set(range(13)), "rich common-zero set")
    Z = rich_common_zero
    plant = sorted(Z & sigma)
    require(plant == [9, 10, 11, 12], "plant")
    g_rows = [[poly_eval(polynomial, index) for polynomial in q_polynomials] for index in sorted(Z)]
    beta = sum(
        rank_mod([g_rows[index] for index in basis], P) == 8
        for basis in itertools.combinations(range(len(g_rows)), 8)
    )
    require(beta == 1197, "beta")
    e20 = beta * (len(RICH_SLOPES) - 20)
    require(e20 == 13_167, "E20")
    require(all(epsilon_1[index] and (-epsilon_0[index] * inverse_mod(epsilon_1[index], P)) % P == 0 for index in plant), "plant label")

    tangent = {
        (-epsilon_0[index] * inverse_mod(epsilon_1[index], P)) % P
        for index in sigma
        if epsilon_1[index]
    }
    selected = set(RICH_SLOPES + OUTLIER_SLOPES)
    require(0 in tangent and not tangent & selected, "tangent deletion")
    component = set()
    for index in set(range(N)) - Z:
        denominator = (epsilon_1[index] - h_values[index]) % P
        if denominator:
            component.add((-epsilon_0[index] * inverse_mod(denominator, P)) % P)
    require(component == {0} | set(RICH_SLOPES), "scalar component completeness")

    return {
        "field": "GF(1009)",
        "row": {"n": N, "k": K, "R": R, "j": J, "A": A, "t": T},
        "source_support_size": len(sigma),
        "selected_record_count": len(records),
        "rich_slope_count_J_L": len(RICH_SLOPES),
        "outlier_count": len(OUTLIER_SLOPES),
        "all_deficits_zero": True,
        "carrier_size": N,
        "affine_rank": affine_rank,
        "raw_rank": raw_rank,
        "K0_rank": k0_rank,
        "affine_direction_intersection_RS_rank": intersection_rank,
        "rich_common_zero_size_z_L": len(Z),
        "outside_source_common_roots": list(range(9)),
        "plant": plant,
        "plant_size": len(plant),
        "plant_floor_t_minus_x_plus_1": T,
        "beta_L": beta,
        "line_weight": e20,
        "rank_one_pair": "P=0,Q=prod_(r=0)^8(X-r)",
        "zero_codeword_slope": 0,
        "zero_codeword_slope_in_tangent_image": True,
        "selected_slopes_disjoint_from_tangent_image": True,
        "tangent_image_size": len(tangent),
        "scalar_H_component_complete_after_tangent_deletion": True,
        "regular_chart_count": len(minors),
        "regular_minor_columns": [0, 1, 2, 3],
        "all_regular_minors_nonzero": True,
        "all_H2_locator_nonzero": True,
        "all_support_wise_noncontained": True,
        "both_individual_sources_noncodeword_on_every_support": True,
        "projective_source_fiber": "FINITE:0",
        "fiber_load": {"numerator": e20, "denominator": 1},
        "per_plant_point_load": {
            "numerator": Fraction(e20, len(plant)).numerator,
            "denominator": Fraction(e20, len(plant)).denominator,
        },
        "global_bad_slope_selector_complete": False,
        "deployed": False,
        "classification": "EXACT_RECORD_LEVEL_RANK1_REGULAR_RANK9_ROUTE_CUT",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    result = build_control()
    print("M1 rank-one regular rank-nine source-load control: PASS")
    print(
        f"  records={result['selected_record_count']} beta={result['beta_L']} "
        f"E20={result['line_weight']} plant={result['plant']}"
    )
    print("  local implication refuted; global selector completeness remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
