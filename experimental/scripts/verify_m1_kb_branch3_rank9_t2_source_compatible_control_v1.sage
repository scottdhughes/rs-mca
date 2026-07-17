#!/usr/bin/env sage
"""Exact t=2 source-compatible cyclic rich-pencil controls.

This verifier checks two toy rows.

* n=35, k=13 over GF(29^2): an exact 21+8 affine-rank-nine
  source-compatible family, together with the complete 839-slope post-deep
  nonzero-locator frontier.  Every selector in that ansatz is structurally
  inside carrier excess ten.
* n=36, k=14 over GF(17^2): the smallest row in this ansatz capable of
  carrier excess eleven.  It also has an exact 21+8 rank-nine family, but a
  compact exhaustive fixed-root inventory supplies a complete 287-slope
  post-deep selector of carrier excess five.

In each row the two remaining slopes have zero-polynomial witnesses of actual
weight two.  Direct restricted-generator checks prove noncontainment, and the
extended deep owner removes them at threshold floor(R/3)=7.  Thus the full
finite frontier has q slopes, partitioned as 2 deep plus q-2 post-deep.

The subset inventories use exact meet-in-the-middle half tables.  They never
materialize C(32,12) supports.  This is a toy control and makes no deployed
or ledger claim.
"""

import hashlib
import json
import operator
from itertools import combinations

import numpy as np


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_hash(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=int
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def field_coordinates(value):
    coefficients = list(value)
    require(len(coefficients) <= 2, "quadratic coordinate overflow")
    coefficients += [0] * (2 - len(coefficients))
    return [ZZ(coefficient) for coefficient in coefficients]


N35_OUTLIERS = (
    (3, 4, 8, 9, 11, 12, 14, 16, 19, 20, 28, 30),
    (7, 14, 16, 19, 20, 23, 24, 27, 29, 30, 31, 32),
    (4, 7, 9, 11, 12, 15, 21, 23, 29, 30, 32, 33),
    (4, 6, 7, 16, 19, 22, 24, 28, 29, 30, 31, 34),
    (4, 5, 7, 11, 12, 13, 17, 18, 20, 28, 30, 31),
    (4, 5, 7, 11, 12, 22, 23, 27, 28, 30, 33, 34),
    (3, 7, 10, 13, 18, 19, 22, 24, 30, 31, 33, 34),
    (4, 5, 6, 7, 10, 11, 17, 18, 25, 26, 27, 33),
)

N36_OUTLIERS = (
    (4, 6, 7, 10, 12, 13, 14, 17, 18, 19, 21, 22, 34),
    (6, 7, 11, 13, 15, 18, 21, 22, 24, 26, 27, 30, 34),
    (7, 8, 12, 13, 15, 17, 18, 19, 21, 23, 30, 32, 35),
    (6, 7, 8, 9, 10, 13, 15, 16, 18, 19, 20, 22, 31),
    (3, 6, 18, 21, 23, 24, 25, 26, 27, 30, 32, 33, 35),
    (5, 8, 9, 13, 19, 21, 22, 24, 25, 26, 29, 31, 32),
    (5, 6, 10, 12, 13, 18, 23, 25, 26, 31, 32, 33, 34),
    (3, 6, 11, 15, 17, 19, 20, 22, 23, 29, 31, 33, 35),
)


def build_row(
    *,
    p,
    modulus_coefficients,
    n,
    k,
    core,
    outliers,
    expected_omega,
    expected_alpha,
    expected_beta,
    expected_excess,
):
    base = GF(p)
    base_polynomial = PolynomialRing(base, "z")
    z = base_polynomial.gen()
    modulus = sum(
        base(coefficient) * z**degree
        for degree, coefficient in enumerate(modulus_coefficients)
    )
    require(modulus.is_irreducible(), "quadratic modulus is reducible")
    field = GF(p**2, name="u", modulus=modulus)
    u = field.gen()
    require(u.multiplicative_order() == p**2 - 1,
            "declared quadratic generator is not primitive")

    omega = u**((p**2 - 1) // n)
    require(omega.multiplicative_order() == n,
            "cyclic-domain generator order drift")
    require(field_coordinates(omega) == expected_omega,
            "cyclic-domain generator coordinates drift")
    domain = [omega**index for index in range(n)]
    require(len(set(domain)) == n and all(domain),
            "cyclic domain collision or zero")

    R = ZZ(n - k)
    j = ZZ(20)
    A = ZZ(n - j)
    t = ZZ(R - j)
    require(t == 2 and A == k + 2, "t=2 row arithmetic drift")
    sparse_indices = (0, 1, 2)
    B = tuple(range(3, n))
    require(len(B) == n - 3, "nonsource domain size drift")
    require(len(core) == k - 2 and set(core).issubset(B),
            "fixed-GCD core drift")
    moving_indices = tuple(index for index in B if index not in core)
    require(len(moving_indices) == 21, "rich moving-root count drift")

    polynomial_ring = PolynomialRing(field, "X")
    X = polynomial_ring.gen()
    a, b, c = domain[:3]

    def root_polynomial(indices):
        return prod(X - domain[index] for index in indices)

    def normalized_locator(indices):
        locator = root_polynomial(indices)
        require(locator(a) != 0, "locator gained sparse root a")
        return locator / locator(a)

    core_polynomial = root_polynomial(core)
    Q_0 = core_polynomial / core_polynomial(a)
    Q_1 = Q_0 * (X - a)
    require(Q_0(a) == 1 and Q_1(a) == 0,
            "source-pencil normalization drift")
    require(Q_1(b) != 0, "source-pencil b direction vanished")
    beta = Q_1(c) / Q_1(b)
    alpha = Q_0(c) - beta * Q_0(b)
    require(field_coordinates(alpha) == expected_alpha,
            "canonical source alpha drift")
    require(field_coordinates(beta) == expected_beta,
            "canonical source beta drift")

    source_0 = vector(field, [1, 0, alpha] + [0] * (n - 3))
    source_1 = vector(field, [0, 1, beta] + [0] * (n - 3))
    require(set(source_0.support()).union(source_1.support())
            == set(sparse_indices), "three-coordinate source support drift")

    rich_root_sets = tuple(
        tuple(sorted(core + (moving,))) for moving in moving_indices
    )
    root_sets = rich_root_sets + tuple(outliers)
    require(len(root_sets) == len(set(root_sets)) == 29,
            "declared 21+8 root inventory drift")
    require(all(len(root_set) == k - 1
                and set(root_set).issubset(B) for root_set in root_sets),
            "declared root set left the locator interface")

    # A nonzero degree-at-most-(k-1) word can agree at at most k-1 points
    # of B.  Reaching A=k+2 therefore forces all three sparse agreements.
    agreement_profiles = [
        (roots_in_B, sparse_agreements)
        for roots_in_B in range(k)
        for sparse_agreements in range(4)
        if roots_in_B + sparse_agreements >= A
    ]
    require(agreement_profiles == [(k - 1, 3)],
            "nonzero witness classification arithmetic drift")

    # D is the root set of X^n-1, hence lambda_x=x/n.
    lambdas = [point / field(n) for point in domain]
    for index, point in enumerate(domain):
        direct = 1 / prod(point - other for other in domain if other != point)
        require(direct == lambdas[index], "dual-weight formula drift")
    H = matrix(
        field,
        R,
        n,
        lambda row, column: lambdas[column] * domain[column]**row,
    )
    require(H.rank() == R, "RS parity-check rank drift")
    generator = matrix(
        field,
        k,
        n,
        lambda degree, column: domain[column]**degree,
    )
    require(generator.rank() == k, "RS generator rank drift")
    y_0 = H * source_0
    y_1 = H * source_1
    require(matrix(field, [y_0, y_1]).rank() == 2,
            "source syndrome line degenerated")
    frobenius_stack = matrix(
        field,
        [
            y_0,
            y_1,
            vector(field, [entry**p for entry in y_0]),
            vector(field, [entry**p for entry in y_1]),
        ],
    )
    require(frobenius_stack.rank() == 4,
            "source syndrome plane gained a quadratic descent")

    deep_threshold = ZZ(R // 3)
    require(deep_threshold == 7 and 3 * deep_threshold <= R,
            "toy deep threshold drift")
    special_slopes = (field(0), -alpha / beta)
    require(special_slopes[0] != special_slopes[1]
            and beta != 0, "special slopes collided")

    def restricted_generator_ranks(target, support):
        restricted = generator.matrix_from_columns(list(support))
        target_row = matrix(
            field, 1, len(support),
            [target[index] for index in support],
        )
        return (restricted.rank(), restricted.stack(target_row).rank())

    deep_exceptions = []
    for label, slope, anchor, expected_actual_support in (
        ("ETA_ZERO", special_slopes[0], 1, [0, 2]),
        ("ETA_NEG_ALPHA_OVER_BETA", special_slopes[1], 2, [0, 1]),
    ):
        received = source_0 + slope * source_1
        exact_support = tuple([anchor] + list(B[:int(A - 1)]))
        full_agreement = tuple(
            index for index, value in enumerate(received) if value == 0
        )
        actual_support = tuple(
            index for index, value in enumerate(received) if value != 0
        )
        require(len(exact_support) == A
                and set(exact_support).issubset(full_agreement),
                "special zero witness lost exact-A agreement")
        require(full_agreement == tuple([anchor] + list(B)),
                "special zero-witness full agreement set drift")
        require(list(actual_support) == expected_actual_support
                and received.hamming_weight() == 2,
                "special zero-witness actual support drift")
        require(source_1[anchor] != 0,
                "special epsilon1 contradiction value vanished")
        nt_ranks = restricted_generator_ranks(source_1, exact_support)
        require(nt_ranks == (k, k + 1),
                "special witness became source-contained")
        syndrome = H * received
        hankel = matrix(
            field,
            t,
            j + 1,
            lambda row, column: syndrome[row + column],
        )
        require(hankel.rank() == 2,
                "special weight-two Hankel rank drift")
        require(received.hamming_weight() <= deep_threshold,
                "special witness escaped extended deep owner")
        deep_exceptions.append({
            "label": label,
            "slope_coordinates": field_coordinates(slope),
            "witness_codeword": "ZERO_POLYNOMIAL",
            "exact_A_witness_support": list(exact_support),
            "full_agreement_set": list(full_agreement),
            "actual_error_support": list(actual_support),
            "actual_error_weight": ZZ(received.hamming_weight()),
            "restricted_generator_rank": ZZ(nt_ranks[0]),
            "augmented_epsilon1_rank": ZZ(nt_ranks[1]),
            "hankel_rank": ZZ(hankel.rank()),
            "deep_threshold": deep_threshold,
            "owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
        })

    # These are the exact deep exceptions.  For every other slope the zero
    # word agrees precisely on B, where both source vectors vanish, and is
    # therefore contained.  Every nonzero RS word has weight at least R+1;
    # since every received point has weight at most three, its error has
    # weight at least R+1-3=20>floor(R/3).
    for slope in field:
        if slope in special_slopes:
            continue
        received = source_0 + slope * source_1
        require(set(received.support()) == set(sparse_indices),
                "nonspecial zero-word agreement set drift")
        require(all(source_0[index] == 0 and source_1[index] == 0
                    for index in B),
                "zero word lost source containment on B")
    nonzero_codeword_error_lower_bound = ZZ(R + 1 - 3)
    require(R + 1 == n - k + 1
            and nonzero_codeword_error_lower_bound == 20
            and nonzero_codeword_error_lower_bound > deep_threshold,
            "MDS deep-exception separation drift")

    polynomials = []
    slopes = []
    errors = []
    supports = []
    hankel_ranks = []
    transverse_ranks = []
    noncontainment_ranks = []
    for root_set in root_sets:
        polynomial = normalized_locator(root_set)
        slope = polynomial(b)
        require(slope != 0, "locator gained zero b-value")
        require(polynomial(c) == alpha + beta * slope,
                "three-coordinate source compatibility failed")
        codeword = vector(field, [polynomial(point) for point in domain])
        error = source_0 + slope * source_1 - codeword
        support = tuple(
            index for index, value in enumerate(error) if value != 0
        )
        require(polynomial.degree() == k - 1,
                "selected locator degree drift")
        require(H * codeword == 0, "selected word left RS(D,k)")
        require(H * error == y_0 + slope * y_1,
                "selected syndrome incidence drift")
        require(set(support) == set(B) - set(root_set)
                and len(support) == error.hamming_weight() == j,
                "selected actual support drift")

        witness_support = tuple(sparse_indices) + tuple(root_set)
        nt_ranks = restricted_generator_ranks(source_0, witness_support)
        noncontainment_ranks.append(nt_ranks)
        require(nt_ranks == (k, k + 1),
                "selected nonzero locator became source-contained")

        restricted = H.matrix_from_columns(list(support))
        transverse = (
            restricted.rank(),
            restricted.augment(y_0.column()).rank(),
            restricted.augment(y_1.column()).rank(),
        )
        transverse_ranks.append(transverse)
        syndrome = H * error
        hankel = matrix(
            field,
            t,
            j + 1,
            lambda row, column: syndrome[row + column],
        )
        hankel_ranks.append(hankel.rank())
        polynomials.append(polynomial)
        slopes.append(slope)
        errors.append(error)
        supports.append(support)

    require(len(set(slopes)) == 29, "declared slopes collided")
    require(set(hankel_ranks) == {2}, "selected Hankel rank drift")
    require(set(transverse_ranks) == {(20, 21, 21)},
            "selected transversality drift")
    require(set(noncontainment_ranks) == {(k, k + 1)},
            "selected nonzero-locator noncontainment rank drift")
    affine_rank = matrix(
        field, [error - errors[0] for error in errors[1:]]
    ).rank()
    raw_rank = matrix(field, errors).rank()
    require((affine_rank, raw_rank) == (9, 10),
            "selected rank-nine tuple drift")
    carrier = set().union(*(set(support) for support in supports))
    carrier_excess = ZZ(len(carrier) - R)
    require(carrier == set(B) and carrier_excess == expected_excess,
            "selected carrier/excess drift")

    rich_gcd = polynomials[0]
    for polynomial in polynomials[1:21]:
        rich_gcd = gcd(rich_gcd, polynomial)
    require(rich_gcd.degree() == k - 2
            and core_polynomial.divides(rich_gcd),
            "rich fixed-GCD degree drift")
    rich_errors = errors[:21]
    rich_carrier = set().union(
        *(set(index for index, value in enumerate(error) if value != 0)
          for error in rich_errors)
    )
    require(rich_carrier == set(moving_indices)
            and len(rich_carrier) == 21,
            "rich moving support drift")

    return {
        "p": ZZ(p),
        "field": field,
        "u": u,
        "modulus": modulus,
        "modulus_coefficients": list(modulus_coefficients),
        "omega": omega,
        "domain": domain,
        "row": {
            "n": ZZ(n),
            "k": ZZ(k),
            "R": R,
            "j": j,
            "A": A,
            "t": t,
        },
        "B": B,
        "core": tuple(core),
        "moving_indices": moving_indices,
        "outliers": tuple(outliers),
        "Q_0": Q_0,
        "Q_1": Q_1,
        "alpha": alpha,
        "beta": beta,
        "source_0": source_0,
        "source_1": source_1,
        "H": H,
        "y_0": y_0,
        "y_1": y_1,
        "generator": generator,
        "deep_threshold": deep_threshold,
        "deep_exceptions": deep_exceptions,
        "nonzero_codeword_error_lower_bound": (
            nonzero_codeword_error_lower_bound
        ),
        "selected": {
            "slope_count": ZZ(len(slopes)),
            "affine_rank": ZZ(affine_rank),
            "raw_rank": ZZ(raw_rank),
            "carrier_size": ZZ(len(carrier)),
            "carrier_excess": carrier_excess,
            "hankel_rank": ZZ(2),
            "transverse_tuple": [20, 21, 21],
            "source_syndrome_frobenius_rank": ZZ(frobenius_stack.rank()),
            "noncontainment_target": "EPSILON_0",
            "restricted_generator_rank": ZZ(k),
            "augmented_target_rank": ZZ(k + 1),
            "uniform_nonzero_locator_noncontainment": True,
            "rich_line_size": ZZ(21),
            "rich_gcd_degree": ZZ(rich_gcd.degree()),
            "rich_moving_support_size": ZZ(len(rich_carrier)),
            "rich_x": ZZ(len(rich_carrier) - j),
        },
    }


def compact_post_deep_nonzero_locator_inventory(
    row,
    *,
    manual_u2_constant,
    manual_u2_linear,
    fixed_root,
    expected_compatible,
    expected_slope_count,
    expected_count_range,
    expected_missing,
    expected_intersection,
    expected_hash,
):
    """Count exact compatible supports from two 2^16 half tables.

    Elements a+b*u are encoded as a+p*b.  The manual product is the exact
    quotient-ring identity u^2=c0+c1*u for the bound Sage modulus.  Chunked
    NumPy arrays evaluate the affine incidence; no C(32,12) support list is
    materialized.
    """

    p = int(row["p"])
    q = p * p
    field = row["field"]

    def encode(value):
        coordinates = field_coordinates(value)
        return int(coordinates[0] + p * coordinates[1])

    def multiply(left, right):
        a = left % p
        b = left // p
        c = right % p
        d = right // p
        constant = (a * c + manual_u2_constant * b * d) % p
        linear = (a * d + b * c + manual_u2_linear * b * d) % p
        return constant + p * linear

    def add(left, right):
        return ((left % p + right % p) % p
                + p * ((left // p + right // p) % p))

    def negate(value):
        return ((-(value % p)) % p
                + p * ((-(value // p)) % p))

    def subtract(left, right):
        return add(left, negate(right))

    def power(value, exponent):
        result = 1
        while exponent:
            if exponent & 1:
                result = multiply(result, value)
            value = multiply(value, value)
            exponent >>= 1
        return result

    def inverse(value):
        require(value != 0, "manual inversion of zero")
        return power(value, q - 2)

    def divide(left, right):
        return multiply(left, inverse(right))

    def vector_multiply(left, right):
        left = np.asarray(left, dtype=np.int64)
        right = np.asarray(right, dtype=np.int64)
        a = left % p
        b = left // p
        c = right % p
        d = right // p
        return (
            (a * c + manual_u2_constant * b * d) % p
            + p * ((a * d + b * c + manual_u2_linear * b * d) % p)
        )

    def vector_add(left, right):
        left = np.asarray(left, dtype=np.int64)
        right = np.asarray(right, dtype=np.int64)
        return (
            (left % p + right % p) % p
            + p * ((left // p + right // p) % p)
        )

    require(multiply(p, p)
            == manual_u2_constant + p * manual_u2_linear,
            "manual quadratic relation drift")
    require(encode(row["u"] * row["u"]) == multiply(p, p),
            "manual/Sage quadratic multiplication mismatch")

    domain = row["domain"]
    a, b, c = domain[:3]
    B = list(row["B"])
    ratio_b = {
        index: divide(encode(b - domain[index]), encode(a - domain[index]))
        for index in B
    }
    ratio_c = {
        index: divide(encode(c - domain[index]), encode(a - domain[index]))
        for index in B
    }
    for index in B:
        require(ratio_b[index]
                == encode((b - domain[index]) / (a - domain[index])),
                "manual/Sage b-ratio mismatch")
        require(ratio_c[index]
                == encode((c - domain[index]) / (a - domain[index])),
                "manual/Sage c-ratio mismatch")

    alpha = encode(row["alpha"])
    beta = encode(row["beta"])
    factor_b = 1
    factor_c = 1
    if fixed_root is None:
        items = B
        selected_root_size = int(row["row"]["k"] - 1)
    else:
        require(fixed_root in B, "fixed inventory root left B")
        factor_b = ratio_b[fixed_root]
        factor_c = ratio_c[fixed_root]
        items = [index for index in B if index != fixed_root]
        selected_root_size = int(row["row"]["k"] - 2)
    require(len(items) == 32 and selected_root_size == 12,
            "compact inventory half-table dimensions drift")
    left_items = items[:16]
    right_items = items[16:]

    def half_table(half_items):
        size = 1 << 16
        product_b = np.ones(size, dtype=np.int16)
        product_c = np.ones(size, dtype=np.int16)
        cardinality = np.zeros(size, dtype=np.uint8)
        for mask in range(1, size):
            bit = mask & -mask
            offset = bit.bit_length() - 1
            # Sage's preparser interprets ``^`` as exponentiation, so use the
            # Python operator explicitly for the subset-mask deletion.
            previous = operator.xor(mask, bit)
            index = half_items[offset]
            product_b[mask] = multiply(
                int(product_b[previous]), ratio_b[index]
            )
            product_c[mask] = multiply(
                int(product_c[previous]), ratio_c[index]
            )
            cardinality[mask] = cardinality[previous] + 1
        return product_b, product_c, cardinality

    left_b, left_c, left_size = half_table(left_items)
    right_b, right_c, right_size = half_table(right_items)
    slope_counts = np.zeros(q, dtype=np.int64)
    lex_support = {}
    compatible_count = 0

    for left_cardinality in range(selected_root_size + 1):
        right_cardinality = selected_root_size - left_cardinality
        left_masks = np.flatnonzero(left_size == left_cardinality)
        right_masks = np.flatnonzero(right_size == right_cardinality)
        if not len(left_masks) or not len(right_masks):
            continue
        right_products_b = right_b[right_masks].astype(np.int64)
        right_products_c = right_c[right_masks].astype(np.int64)
        for start in range(0, len(left_masks), 128):
            mask_block = left_masks[start:start + 128]
            product_b = vector_multiply(
                left_b[mask_block].astype(np.int64)[:, None],
                right_products_b[None, :],
            )
            product_c = vector_multiply(
                left_c[mask_block].astype(np.int64)[:, None],
                right_products_c[None, :],
            )
            product_b = vector_multiply(factor_b, product_b)
            product_c = vector_multiply(factor_c, product_c)
            compatible = product_c == vector_add(
                alpha, vector_multiply(beta, product_b)
            )
            rows, columns = np.nonzero(compatible)
            compatible_count += len(rows)
            if not len(rows):
                continue
            slopes = product_b[rows, columns]
            slope_counts += np.bincount(slopes, minlength=q)
            for row_offset, column_offset, slope in zip(
                rows, columns, slopes
            ):
                left_mask = int(mask_block[row_offset])
                right_mask = int(right_masks[column_offset])
                support = [] if fixed_root is None else [fixed_root]
                support.extend(
                    left_items[position]
                    for position in range(16)
                    if left_mask >> position & 1
                )
                support.extend(
                    right_items[position]
                    for position in range(16)
                    if right_mask >> position & 1
                )
                support_tuple = tuple(sorted(support))
                slope = int(slope)
                if (slope not in lex_support
                        or support_tuple < lex_support[slope]):
                    lex_support[slope] = support_tuple

    nonzero_slopes = np.flatnonzero(slope_counts)
    require(compatible_count == int(slope_counts.sum()),
            "compatible support count/slope histogram mismatch")
    require(compatible_count == expected_compatible,
            "compatible support total drift")
    require(len(nonzero_slopes) == expected_slope_count,
            "compatible post-deep slope frontier drift")
    require(0 not in nonzero_slopes,
            "zero slope entered post-deep nonzero-locator frontier")
    count_range = (
        int(slope_counts[nonzero_slopes].min()),
        int(slope_counts[nonzero_slopes].max()),
    )
    require(count_range == expected_count_range,
            "per-slope compatible witness range drift")

    missing_nonzero = [
        value for value in range(1, q) if slope_counts[value] == 0
    ]
    require([[value % p, value // p] for value in missing_nonzero]
            == expected_missing, "excluded source-zero slope drift")
    excluded = divide(negate(alpha), beta)
    require(missing_nonzero == [excluded],
            "missing slope is not -alpha/beta")
    require(add(alpha, multiply(beta, excluded)) == 0,
            "excluded slope did not zero the c source value")
    require(len(nonzero_slopes) == q - 2,
            "post-deep inventory did not attain every admissible slope")

    records = [
        {
            "slope": [int(value % p), int(value // p)],
            "count": int(slope_counts[value]),
            "S": list(lex_support[int(value)]),
        }
        for value in nonzero_slopes
    ]
    inventory_hash = canonical_hash(records)
    require(inventory_hash == expected_hash,
            "compact inventory hash drift")
    k = int(row["row"]["k"])
    require(all(len(record["S"]) == k - 1
                and set(record["S"]).issubset(set(B))
                for record in records),
            "post-deep representative left nonzero-locator interface")
    common_roots = set(records[0]["S"])
    for record in records[1:]:
        common_roots.intersection_update(record["S"])
    require(sorted(common_roots) == expected_intersection,
            "lex-selector common-root intersection drift")
    carrier = set(B) - common_roots
    carrier_excess = ZZ(len(carrier) - row["row"]["R"])

    return {
        "half_table_size_each": ZZ(1 << 16),
        "root_sets_represented": ZZ(binomial(32, 12)),
        "fixed_root": fixed_root,
        "compatible_support_count": ZZ(compatible_count),
        "slope_count": ZZ(len(nonzero_slopes)),
        "witness_count_min": ZZ(count_range[0]),
        "witness_count_max": ZZ(count_range[1]),
        "omitted_deep_slopes": [[0, 0]] + expected_missing,
        "inventory_sha256": inventory_hash,
        "lex_selector_common_roots": sorted(common_roots),
        "lex_selector_carrier_size": ZZ(len(carrier)),
        "lex_selector_carrier_excess": carrier_excess,
        "uniform_nonzero_locator_noncontainment": {
            "target_source": "EPSILON_0",
            "forced_zero_set": "S_UNION_{b}",
            "forced_zero_count": ZZ(k),
            "degree_strict_upper_bound": ZZ(k),
            "contradictory_value_index": ZZ(0),
            "applies_to_every_compatible_support": True,
            "applies_to_every_lex_representative": True,
        },
    }


row35 = build_row(
    p=29,
    modulus_coefficients=(2, 24, 1),
    n=35,
    k=13,
    core=tuple(range(3, 14)),
    outliers=N35_OUTLIERS,
    expected_omega=[26, 16],
    expected_alpha=[28, 28],
    expected_beta=[2, 23],
    expected_excess=10,
)

post_deep_inventory35 = compact_post_deep_nonzero_locator_inventory(
    row35,
    manual_u2_constant=27,
    manual_u2_linear=5,
    fixed_root=None,
    expected_compatible=268_998,
    expected_slope_count=839,
    expected_count_range=(259, 390),
    expected_missing=[[12, 15]],
    expected_intersection=[3, 4, 5],
    expected_hash=(
        "24150857548e5bc9ee199e1d088bdcfb458191579db247a65ed311e5dfbc590e"
    ),
)

row36 = build_row(
    p=17,
    modulus_coefficients=(3, 16, 1),
    n=36,
    k=14,
    core=tuple(range(3, 15)),
    outliers=N36_OUTLIERS,
    expected_omega=[12, 16],
    expected_alpha=[13, 7],
    expected_beta=[5, 14],
    expected_excess=11,
)

post_deep_inventory36 = compact_post_deep_nonzero_locator_inventory(
    row36,
    manual_u2_constant=14,
    manual_u2_linear=1,
    fixed_root=3,
    expected_compatible=780_907,
    expected_slope_count=287,
    expected_count_range=(2_571, 2_833),
    expected_missing=[[1, 15]],
    expected_intersection=[3, 4, 5, 6, 7, 8],
    expected_hash=(
        "ceeef4c9024450f0c935a0ae0aaf6b4dab693a7605f404f65f1655eac8ae0452"
    ),
)


def carrier_cap(R, j, kappa):
    if kappa == 0:
        return ZZ(j + 1)
    numerator = binomial(R + kappa, kappa + 1)
    denominator = binomial(R + kappa - j - 1, kappa)
    require(denominator > 0, "low-carrier denominator vanished")
    return ZZ(numerator // denominator)


# Structural n=35 post-deep nonzero-locator cut: all such errors avoid the
# three source coordinates, so every selector in this ansatz lies in B and
# has excess at most 32-22=10.
require(len(row35["B"]) - row35["row"]["R"] == 10,
        "n=35 structural carrier cutoff drift")
require(post_deep_inventory35["lex_selector_carrier_excess"] == 7,
        "n=35 lex complete-selector excess drift")
cap35 = carrier_cap(22, 20, 7)
require(cap35 >= post_deep_inventory35["slope_count"],
        "n=35 low-carrier cap does not cover exact post-deep frontier")

# Minimal high-carrier-capable row inside the post-deep nonzero-locator,
# three-source/one-moving-root ansatz: 21 moving roots force R>=22; max excess
# is k-3, so excess>=11 forces k>=14 and n>=36.
require(row35["row"]["R"] == 22, "minimal R witness drift")
require(row35["row"]["k"] - 3 == 10,
        "n=35 maximum excess formula drift")
require(row36["row"]["k"] - 3 == 11
        and row36["row"]["n"] == 36,
        "minimal high-carrier row drift")

# The n=36 fixed-root inventory already attains every post-deep slope, so it
# is a complete selector for the post-deep nonzero-locator frontier.  Its
# lexicographic representatives have six common roots and excess five.
require(post_deep_inventory36["lex_selector_carrier_excess"] == 5,
        "n=36 complete-selector excess drift")
cap36 = carrier_cap(22, 20, 5)
require(cap36 >= post_deep_inventory36["slope_count"],
        "n=36 low-carrier cap does not cover exact post-deep frontier")


def public_row(row, inventory, cap, structural_maximum_excess):
    q = ZZ(row["field"].cardinality())
    require(inventory["slope_count"] + 2 == q,
            "full/deep/post-deep slope partition drift")
    return {
        "field": {
            "characteristic": row["p"],
            "degree": ZZ(2),
            "cardinality": row["field"].cardinality(),
            "modulus_coefficients_ascending": row["modulus_coefficients"],
            "primitive_generator_order": row["u"].multiplicative_order(),
            "omega_coordinates": field_coordinates(row["omega"]),
            "omega_order": row["omega"].multiplicative_order(),
        },
        "row": row["row"],
        "source": {
            "sparse_indices": [0, 1, 2],
            "core": list(row["core"]),
            "moving_indices": list(row["moving_indices"]),
            "canonical_alpha_coordinates": field_coordinates(row["alpha"]),
            "canonical_beta_coordinates": field_coordinates(row["beta"]),
            "compatibility_equation": "q_S(c)=alpha+beta*q_S(b)",
            "nonzero_witness_profile": [
                int(row["row"]["k"] - 1), 3
            ],
            "uniform_nonzero_locator_noncontainment": {
                "target_source": "EPSILON_0",
                "forced_zero_set": "S_UNION_{b}",
                "forced_zero_count": ZZ(row["row"]["k"]),
                "degree_strict_upper_bound": ZZ(row["row"]["k"]),
                "contradictory_value_index": ZZ(0),
                "selected_direct_rank_check": True,
                "proof_covers_all_inventory_representatives": True,
            },
        },
        "rank9_local_control": {
            "complete_selector": False,
            "root_set_count": ZZ(29),
            "outliers": [list(item) for item in row["outliers"]],
            **row["selected"],
        },
        "full_finite_frontier": {
            "finite_slope_count": q,
            "deep_exception_count": ZZ(2),
            "post_deep_nonzero_locator_slope_count": inventory["slope_count"],
            "partition_exact": True,
        },
        "deep_exceptions": {
            "owner_id": "DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION",
            "deep_threshold": row["deep_threshold"],
            "exception_count": ZZ(2),
            "exceptions": row["deep_exceptions"],
            "zero_word_contained_for_every_nonspecial_slope": True,
            "nonzero_codeword_minimum_weight": ZZ(row["row"]["R"] + 1),
            "received_word_maximum_weight": ZZ(3),
            "nonzero_codeword_error_lower_bound": row[
                "nonzero_codeword_error_lower_bound"
            ],
            "exceptions_are_exact": True,
        },
        "post_deep_nonzero_locator_inventory": inventory,
        "post_deep_low_carrier_exit": {
            "ansatz_structural_maximum_excess": ZZ(structural_maximum_excess),
            "lex_selector_excess": inventory[
                "lex_selector_carrier_excess"
            ],
            "lex_selector_cap": cap,
            "exact_post_deep_slope_count": inventory["slope_count"],
            "owner_applies_at_or_before_low_carrier": True,
            "no_rank9_residual_from_local_subfamily": True,
        },
    }


payload = {
    "schema": "rs-mca-m1-kb-branch3-rank9-t2-source-compatible-control-v1-sage",
    "status": "PASS",
    "classification": "EXACT_T2_CYCLIC_SOURCE_COMPATIBLE_DEEP_PLUS_LOW_CARRIER_CONTROLS",
    "n35": public_row(row35, post_deep_inventory35, cap35, 10),
    "n36": public_row(row36, post_deep_inventory36, cap36, 11),
    "minimality": {
        "scope": "POST_DEEP_NONZERO_LOCATOR_THREE_SOURCE_ONE_MOVING_ROOT_ANSATZ",
        "rich_moving_root_target": ZZ(21),
        "three_sparse_source_coordinates": ZZ(3),
        "t": ZZ(2),
        "minimum_R": ZZ(22),
        "maximum_carrier_excess_formula": "k-3",
        "minimum_k_for_excess_11": ZZ(14),
        "minimum_n_for_excess_11": ZZ(36),
    },
    "scope_guards": {
        "toy_scale_only": True,
        "deployed_field_instantiated": False,
        "deployed_complete_selector_inventory": False,
        "koalabear_rank9_closed": False,
        "ledger_movement": ZZ(0),
        "U_Q_determined": False,
        "U_A_determined": False,
        "lean_authorized": False,
    },
}
payload["payload_sha256"] = canonical_hash(payload)
print(json.dumps(payload, sort_keys=True, default=int))
