#!/usr/bin/env sage
"""Exact Sage certificate for the M31 order-32 rotation route cut.

Let ``Lambda`` be the monic reduction of the standard Chebyshev polynomial
``T_32`` over ``GF(2^31-1)``.  For a monic degree-17 quotient locator

    P(Y) = Y^17 + sum_(j=0)^16 a_j Y^j,

The literal multiplicative-style rotation replaces ``P`` by
``Y^31 P mod Lambda``.  The symmetry-native Chebyshev rotation instead uses
``T_31(Y) P mod Lambda``.  Equality of the coefficients in degrees 16
through 31 for two such locators places their coefficient difference in the
right kernel of the corresponding 16-by-17 high map.

This replay treats the two rotations separately.  It derives rank 16 and a
one-dimensional kernel for each map.  For the intrinsic rotation, the kernel
is exactly the second-kind Chebyshev polynomial ``U_16`` and the integral
resultant is

    Res_Z(U_16,T_32) = 2^496.

Both kernel polynomials are therefore coprime to ``Lambda``.  Any two
17-subsets of a 31-point punctured quotient meet, so distinct subset locators
cannot differ by a nonzero multiple of either kernel polynomial.  Both
rotated high-prefix maps are injective on every punctured 17-subset family.
These are route cuts for the two proposed rotations, not a global M31 list
bound.

Usage:

    sage experimental/scripts/verify_m31_chebyshev_order32_rotation_injectivity_v1.sage --check
    sage experimental/scripts/verify_m31_chebyshev_order32_rotation_injectivity_v1.sage --tamper-selftest
"""

from __future__ import annotations

import argparse
import copy
import hashlib


P = 2^31 - 1
CHEBYSHEV_DEGREE = 32
ROTATION_EXPONENT = 31
SUBSET_SIZE = 17
HIGH_DEGREE_START = 16
HIGH_DEGREE_STOP = 32

EXPECTED_LOCATOR_COEFFICIENT_SHA256 = (
    "fd40f73e652c8c196303cda4ef5ee77786d01ae95b3e5a70962e7950220b52f0"
)
EXPECTED_ROOT_SHA256 = (
    "253eeda40a8f663d2e3db3ac8cbbe6a2d5c8bff2c5422f5e120a58ee8c661757"
)
EXPECTED_KERNEL_COEFFICIENTS = (
    1,
    0,
    922883926,
    0,
    1787128909,
    0,
    237254192,
    0,
    577962578,
    0,
    30724201,
    0,
    53081916,
    0,
    1776865326,
    0,
    821554693,
)
EXPECTED_INTRINSIC_KERNEL_COEFFICIENTS = (
    1,
    0,
    2147483503,
    0,
    3360,
    0,
    2147454079,
    0,
    126720,
    0,
    2147190783,
    0,
    372736,
    0,
    2147237887,
    0,
    65536,
)


def require(condition, label):
    """Raise an explicit certificate failure instead of using ``assert``."""
    if not condition:
        raise RuntimeError(label)


def chebyshev_polynomial(degree, variable):
    """Return standard ``T_degree`` via ``T_d=2 X T_(d-1)-T_(d-2)``."""
    ring = variable.parent()
    require(degree >= 0, "Chebyshev degree is nonnegative")
    if degree == 0:
        return ring.one()
    if degree == 1:
        return variable
    previous = ring.one()
    current = variable
    for _ in range(2, degree + 1):
        previous, current = current, 2 * variable * current - previous
    return current


def chebyshev_second_kind_polynomial(degree, variable):
    """Return standard ``U_degree`` via ``U_0=1``, ``U_1=2X``."""
    ring = variable.parent()
    require(degree >= 0, "second-kind Chebyshev degree is nonnegative")
    if degree == 0:
        return ring.one()
    if degree == 1:
        return 2 * variable
    previous = ring.one()
    current = 2 * variable
    for _ in range(2, degree + 1):
        previous, current = current, 2 * variable * current - previous
    return current


def integer_tuple_sha256(values):
    payload = ",".join(str(int(value)) for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def derive_report():
    """Derive every algebraic object from the recurrence and return its pins."""
    require(P == 2147483647 and is_prime(P), "deployed Mersenne prime")

    # First retain the characteristic-zero leading coefficient.  Its
    # reduction is 1 because 2^31 == 1 modulo 2^31-1, so T_32 itself is the
    # deployed monic locator even though its integral leading coefficient is
    # 2^31.
    ZZ_polynomials = PolynomialRing(ZZ, "Z")
    Z = ZZ_polynomials.gen()
    integral_T32 = chebyshev_polynomial(CHEBYSHEV_DEGREE, Z)
    integral_T31 = chebyshev_polynomial(ROTATION_EXPONENT, Z)
    integral_second_kind = tuple(
        chebyshev_second_kind_polynomial(degree, Z)
        for degree in range(SUBSET_SIZE)
    )
    integral_U16 = integral_second_kind[SUBSET_SIZE - 1]
    require(
        integral_T32.leading_coefficient() == 2^31,
        "integral T_32 leading coefficient",
    )
    require(integral_T31.degree() == 31, "integral T_31 degree")
    require(integral_U16.degree() == 16, "integral U_16 degree")
    require(integral_U16[0] == 1, "integral U_16 constant normalization")
    require(
        integral_U16.leading_coefficient() == 2^16,
        "integral U_16 leading coefficient",
    )

    # The exact integer identity is stronger than a finite-field sample:
    #
    #   T_31 U_j = T_(31-j) + T_32 U_(j-1),
    #
    # with the final summand zero at j=0.  Reduction modulo T_32 gives the
    # intrinsic rotation identity used below.
    for degree in range(SUBSET_SIZE):
        difference = (
            integral_T31 * integral_second_kind[degree]
            - chebyshev_polynomial(ROTATION_EXPONENT - degree, Z)
        )
        quotient, remainder = difference.quo_rem(integral_T32)
        expected_quotient = (
            ZZ_polynomials.zero()
            if degree == 0
            else integral_second_kind[degree - 1]
        )
        require(remainder == 0, "integral T31*U_j congruence remainder")
        require(
            quotient == expected_quotient,
            "integral T31*U_j congruence quotient",
        )

    intrinsic_integer_resultant = integral_U16.resultant(integral_T32)
    require(
        intrinsic_integer_resultant == 2^496,
        "exact resultant Res_Z(U_16,T_32)=2^496",
    )

    field = GF(P)
    polynomials = PolynomialRing(field, "Y")
    Y = polynomials.gen()
    T32 = chebyshev_polynomial(CHEBYSHEV_DEGREE, Y)
    T31 = chebyshev_polynomial(ROTATION_EXPONENT, Y)
    second_kind = tuple(
        chebyshev_second_kind_polynomial(degree, Y)
        for degree in range(SUBSET_SIZE)
    )
    U16 = second_kind[SUBSET_SIZE - 1]
    require(T32 == polynomials(integral_T32), "integral recurrence reduction")
    require(T31 == polynomials(integral_T31), "integral T_31 reduction")
    require(U16 == polynomials(integral_U16), "integral U_16 reduction")
    require(int(T32.leading_coefficient()) == 1, "T_32 leading coefficient mod p")
    locator = T32 / T32.leading_coefficient()
    require(locator.degree() == CHEBYSHEV_DEGREE, "quotient locator degree")
    require(locator.is_monic(), "quotient locator monic")
    require(locator == T32, "T_32 is already monic over the deployed field")
    require(
        gcd(locator, locator.derivative()) == 1,
        "quotient locator is squarefree",
    )

    locator_coefficients = tuple(
        int(locator[degree]) for degree in range(CHEBYSHEV_DEGREE + 1)
    )
    locator_coefficient_sha256 = integer_tuple_sha256(locator_coefficients)
    require(
        locator_coefficient_sha256 == EXPECTED_LOCATOR_COEFFICIENT_SHA256,
        "quotient locator coefficient hash",
    )

    roots_with_multiplicity = locator.roots()
    require(
        len(roots_with_multiplicity) == CHEBYSHEV_DEGREE,
        "T_32 splits completely over GF(p)",
    )
    require(
        all(multiplicity == 1 for _, multiplicity in roots_with_multiplicity),
        "all quotient roots are simple",
    )
    roots = tuple(
        sorted((root for root, _ in roots_with_multiplicity), key=lambda root: int(root))
    )
    require(len(set(roots)) == CHEBYSHEV_DEGREE, "quotient roots are distinct")
    require(all(root != 0 for root in roots), "quotient roots are nonzero")
    require(set(roots) == {-root for root in roots}, "quotient roots are antipodal")
    require(all(locator(root) == 0 for root in roots), "quotient root evaluation")
    root_sha256 = integer_tuple_sha256(roots)
    require(root_sha256 == EXPECTED_ROOT_SHA256, "ordered quotient-root hash")

    # Column j is the degree-16,...,31 part of Y^(31+j) modulo Lambda.
    # It is therefore the contribution of a_j to the rotated high prefix.
    rotated_monomials = tuple(
        (Y^(ROTATION_EXPONENT + degree)).mod(locator)
        for degree in range(SUBSET_SIZE)
    )
    high_matrix = matrix(
        field,
        HIGH_DEGREE_STOP - HIGH_DEGREE_START,
        SUBSET_SIZE,
        lambda row, column: rotated_monomials[column][HIGH_DEGREE_START + row],
    )
    require(high_matrix.nrows() == 16, "high map row count")
    require(high_matrix.ncols() == 17, "high map column count")
    require(high_matrix.rank() == 16, "high map exact rank")

    kernel = high_matrix.right_kernel()
    require(kernel.dimension() == 1, "high map kernel dimension")
    kernel_basis = kernel.basis()
    require(len(kernel_basis) == 1, "high map single kernel basis vector")
    require(kernel_basis[0][0] != 0, "kernel constant coefficient is nonzero")
    normalized_kernel_vector = kernel_basis[0] / kernel_basis[0][0]
    require(
        high_matrix * normalized_kernel_vector == vector(field, [0] * 16),
        "normalized vector lies in high-map kernel",
    )
    kernel_coefficients = tuple(int(value) for value in normalized_kernel_vector)
    require(
        kernel_coefficients == EXPECTED_KERNEL_COEFFICIENTS,
        "normalized K0 coefficients",
    )
    K0 = sum(
        normalized_kernel_vector[degree] * Y^degree
        for degree in range(SUBSET_SIZE)
    )
    require(K0.degree() == SUBSET_SIZE - 1, "K0 exact degree")
    require(K0[0] == 1, "K0 normalization")

    rotated_kernel_remainder = (Y^ROTATION_EXPONENT * K0).mod(locator)
    require(
        rotated_kernel_remainder.degree() <= HIGH_DEGREE_START - 1,
        "rotated K0 has no degree-16-through-31 terms",
    )
    require(
        all(
            rotated_kernel_remainder[degree] == 0
            for degree in range(HIGH_DEGREE_START, HIGH_DEGREE_STOP)
        ),
        "rotated K0 high coefficients vanish",
    )
    kernel_locator_gcd = gcd(K0, locator)
    require(kernel_locator_gcd == 1, "K0 is coprime to quotient locator")
    require(all(K0(root) != 0 for root in roots), "K0 misses every quotient root")

    # Evaluation of a remainder at a root of Lambda agrees with evaluation of
    # the unreduced polynomial.  This check binds the matrix computation to
    # the intended rotation on all 32 quotient labels.
    require(
        all(
            rotated_monomials[degree](root)
            == root^(ROTATION_EXPONENT + degree)
            for root in roots
            for degree in range(SUBSET_SIZE)
        ),
        "rotation/remainder evaluation identity on quotient roots",
    )

    # ------------------------------------------------------------------
    # Intrinsic Chebyshev rotation: T_31(Y) P(Y) modulo T_32(Y).
    # ------------------------------------------------------------------

    intrinsic_rotated_monomials = tuple(
        (T31 * Y^degree).mod(locator) for degree in range(SUBSET_SIZE)
    )
    intrinsic_high_matrix = matrix(
        field,
        HIGH_DEGREE_STOP - HIGH_DEGREE_START,
        SUBSET_SIZE,
        lambda row, column: intrinsic_rotated_monomials[column][
            HIGH_DEGREE_START + row
        ],
    )
    require(intrinsic_high_matrix.nrows() == 16, "intrinsic high map row count")
    require(intrinsic_high_matrix.ncols() == 17, "intrinsic high map column count")
    require(intrinsic_high_matrix.rank() == 16, "intrinsic high map exact rank")

    # The U_j form a basis of polynomials of degree at most 16.  In that
    # basis the intrinsic high map sends U_j to the high part of T_(31-j).
    # The first sixteen images have distinct degrees 31,...,16 and the last
    # image T_15 has no high part.  This gives a structural replay of rank 16
    # and identifies the kernel, independently of the raw monomial RREF.
    second_kind_basis_matrix = matrix(
        field,
        SUBSET_SIZE,
        SUBSET_SIZE,
        lambda row, column: second_kind[column][row],
    )
    require(second_kind_basis_matrix.rank() == 17, "U_0,...,U_16 basis rank")
    intrinsic_identity_images = tuple(
        chebyshev_polynomial(ROTATION_EXPONENT - degree, Y)
        for degree in range(SUBSET_SIZE)
    )
    require(
        all(
            (T31 * second_kind[degree]).mod(locator)
            == intrinsic_identity_images[degree]
            for degree in range(SUBSET_SIZE)
        ),
        "T_31 U_j equals T_(31-j) modulo T_32 for 0<=j<=16",
    )
    intrinsic_identity_high_matrix = matrix(
        field,
        HIGH_DEGREE_STOP - HIGH_DEGREE_START,
        SUBSET_SIZE,
        lambda row, column: intrinsic_identity_images[column][
            HIGH_DEGREE_START + row
        ],
    )
    require(
        intrinsic_high_matrix * second_kind_basis_matrix
        == intrinsic_identity_high_matrix,
        "intrinsic high map in second-kind basis",
    )
    require(
        intrinsic_identity_high_matrix[:, :16].rank() == 16,
        "T_31,...,T_16 high parts are independent",
    )
    require(
        intrinsic_identity_high_matrix.column(16) == vector(field, [0] * 16),
        "T_15 has zero intrinsic high part",
    )

    intrinsic_kernel = intrinsic_high_matrix.right_kernel()
    require(intrinsic_kernel.dimension() == 1, "intrinsic kernel dimension")
    intrinsic_kernel_basis = intrinsic_kernel.basis()
    require(len(intrinsic_kernel_basis) == 1, "intrinsic single kernel vector")
    require(
        intrinsic_kernel_basis[0][0] != 0,
        "intrinsic kernel constant coefficient is nonzero",
    )
    intrinsic_kernel_vector = (
        intrinsic_kernel_basis[0] / intrinsic_kernel_basis[0][0]
    )
    require(
        intrinsic_high_matrix * intrinsic_kernel_vector
        == vector(field, [0] * 16),
        "normalized intrinsic vector lies in kernel",
    )
    intrinsic_kernel_coefficients = tuple(
        int(value) for value in intrinsic_kernel_vector
    )
    require(
        intrinsic_kernel_coefficients == EXPECTED_INTRINSIC_KERNEL_COEFFICIENTS,
        "normalized intrinsic kernel coefficients",
    )
    require(
        intrinsic_kernel_coefficients
        == tuple(int(U16[degree]) for degree in range(SUBSET_SIZE)),
        "intrinsic kernel is exactly U_16",
    )

    intrinsic_rotated_kernel_remainder = (T31 * U16).mod(locator)
    T15 = chebyshev_polynomial(15, Y)
    require(
        intrinsic_rotated_kernel_remainder == T15,
        "T_31 U_16 equals T_15 modulo T_32",
    )
    require(
        intrinsic_rotated_kernel_remainder.degree() == 15,
        "intrinsic rotated U_16 remainder degree",
    )
    intrinsic_kernel_locator_gcd = gcd(U16, locator)
    require(
        intrinsic_kernel_locator_gcd == 1,
        "U_16 is coprime to quotient locator",
    )
    require(
        field(intrinsic_integer_resultant) != 0,
        "integer resultant stays nonzero modulo deployed prime",
    )
    require(all(U16(root) != 0 for root in roots), "U_16 misses every quotient root")
    intrinsic_multiplier_locator_gcd = gcd(T31, locator)
    require(
        intrinsic_multiplier_locator_gcd == 1,
        "T_31 is a unit modulo quotient locator",
    )
    require(
        all(T31(root) != 0 for root in roots),
        "T_31 is nonzero on every quotient root",
    )
    require(
        all(
            intrinsic_rotated_monomials[degree](root)
            == T31(root) * root^degree
            for root in roots
            for degree in range(SUBSET_SIZE)
        ),
        "intrinsic rotation/remainder evaluation identity",
    )

    quotient_size = len(roots)
    punctured_size = quotient_size - 1
    minimum_intersection = 2 * SUBSET_SIZE - punctured_size
    require(punctured_size == 31, "punctured quotient size")
    require(minimum_intersection == 3 > 0, "17-subsets necessarily intersect")
    require(
        SUBSET_SIZE - 1 == high_matrix.nrows(),
        "difference of monic degree-17 locators is in high-map domain",
    )

    # Logical closure encoded by the checked inputs above:
    #
    # * equal rotated high parts imply P_A-P_B is in ker(high_matrix);
    # * rank 16 makes that difference t*K0;
    # * distinct 17-subsets have t != 0 and share at least one root alpha;
    # * then K0(alpha)=0, contradicting gcd(K0,Lambda)=1.
    rotation_injective_on_punctured_subsets = (
        high_matrix.rank() == 16
        and kernel.dimension() == 1
        and kernel_locator_gcd == 1
        and minimum_intersection > 0
    )
    require(
        rotation_injective_on_punctured_subsets,
        "rotation injectivity contradiction inputs",
    )
    intrinsic_rotation_injective_on_punctured_subsets = (
        intrinsic_high_matrix.rank() == 16
        and intrinsic_kernel.dimension() == 1
        and intrinsic_kernel_locator_gcd == 1
        and minimum_intersection > 0
    )
    require(
        intrinsic_rotation_injective_on_punctured_subsets,
        "intrinsic rotation injectivity contradiction inputs",
    )

    return {
        "p": int(P),
        "integral_T32_leading_coefficient": int(integral_T32.leading_coefficient()),
        "deployed_T32_leading_coefficient": int(T32.leading_coefficient()),
        "locator_degree": int(locator.degree()),
        "locator_monic": bool(locator.is_monic()),
        "locator_squarefree": bool(gcd(locator, locator.derivative()) == 1),
        "locator_coefficient_sha256": locator_coefficient_sha256,
        "quotient_root_count": quotient_size,
        "quotient_roots_distinct": len(set(roots)) == quotient_size,
        "quotient_roots_nonzero": all(root != 0 for root in roots),
        "quotient_roots_antipodal": set(roots) == {-root for root in roots},
        "quotient_root_sha256": root_sha256,
        "literal_rotation_multiplier": "Y^31",
        "high_matrix_dimensions": (high_matrix.nrows(), high_matrix.ncols()),
        "high_matrix_rank": int(high_matrix.rank()),
        "high_matrix_kernel_dimension": int(kernel.dimension()),
        "K0_coefficients": kernel_coefficients,
        "rotated_K0_remainder_degree": int(rotated_kernel_remainder.degree()),
        "K0_locator_gcd_degree": int(kernel_locator_gcd.degree()),
        "K0_nonzero_on_quotient": all(K0(root) != 0 for root in roots),
        "intrinsic_rotation_multiplier": "T_31(Y)",
        "intrinsic_integer_resultant": int(intrinsic_integer_resultant),
        "intrinsic_integer_resultant_exponent": 496,
        "intrinsic_chebyshev_identity_count": SUBSET_SIZE,
        "intrinsic_second_kind_basis_rank": int(second_kind_basis_matrix.rank()),
        "intrinsic_high_matrix_dimensions": (
            intrinsic_high_matrix.nrows(),
            intrinsic_high_matrix.ncols(),
        ),
        "intrinsic_high_matrix_rank": int(intrinsic_high_matrix.rank()),
        "intrinsic_high_matrix_kernel_dimension": int(
            intrinsic_kernel.dimension()
        ),
        "intrinsic_kernel_coefficients": intrinsic_kernel_coefficients,
        "intrinsic_kernel_is_U16": intrinsic_kernel_coefficients
        == tuple(int(U16[degree]) for degree in range(SUBSET_SIZE)),
        "intrinsic_rotated_U16_remainder_degree": int(
            intrinsic_rotated_kernel_remainder.degree()
        ),
        "intrinsic_U16_locator_gcd_degree": int(
            intrinsic_kernel_locator_gcd.degree()
        ),
        "intrinsic_U16_nonzero_on_quotient": all(
            U16(root) != 0 for root in roots
        ),
        "intrinsic_T31_locator_gcd_degree": int(
            intrinsic_multiplier_locator_gcd.degree()
        ),
        "punctured_quotient_size": punctured_size,
        "subset_size": SUBSET_SIZE,
        "minimum_pair_intersection": minimum_intersection,
        "rotation_injective_on_punctured_17_subsets": (
            rotation_injective_on_punctured_subsets
        ),
        "intrinsic_rotation_injective_on_punctured_17_subsets": (
            intrinsic_rotation_injective_on_punctured_subsets
        ),
        "scope": "ROTATION_ROUTE_CUT_ONLY_ROW_OPEN",
    }


def validate_report(report):
    """Validate the semantic pins used by the packet and tamper self-test."""
    require(report["p"] == 2147483647, "report prime")
    require(
        report["integral_T32_leading_coefficient"] == 2147483648,
        "report integral T_32 leading coefficient",
    )
    require(
        report["deployed_T32_leading_coefficient"] == 1,
        "report deployed T_32 leading coefficient",
    )
    require(report["locator_degree"] == 32, "report locator degree")
    require(report["locator_monic"] is True, "report locator monicity")
    require(report["locator_squarefree"] is True, "report squarefreeness")
    require(
        report["locator_coefficient_sha256"]
        == EXPECTED_LOCATOR_COEFFICIENT_SHA256,
        "report locator hash",
    )
    require(report["quotient_root_count"] == 32, "report root count")
    require(report["quotient_roots_distinct"] is True, "report distinct roots")
    require(report["quotient_roots_nonzero"] is True, "report nonzero roots")
    require(report["quotient_roots_antipodal"] is True, "report antipodal roots")
    require(
        report["quotient_root_sha256"] == EXPECTED_ROOT_SHA256,
        "report root hash",
    )
    require(report["literal_rotation_multiplier"] == "Y^31", "report literal map")
    require(report["high_matrix_dimensions"] == (16, 17), "report matrix dimensions")
    require(report["high_matrix_rank"] == 16, "report matrix rank")
    require(
        report["high_matrix_kernel_dimension"] == 1,
        "report kernel dimension",
    )
    require(
        report["K0_coefficients"] == EXPECTED_KERNEL_COEFFICIENTS,
        "report K0 coefficients",
    )
    require(
        report["rotated_K0_remainder_degree"] == 15,
        "report rotated K0 remainder degree",
    )
    require(report["K0_locator_gcd_degree"] == 0, "report K0/locator gcd")
    require(
        report["K0_nonzero_on_quotient"] is True,
        "report K0 quotient-root exclusion",
    )
    require(
        report["intrinsic_rotation_multiplier"] == "T_31(Y)",
        "report intrinsic map",
    )
    require(
        report["intrinsic_integer_resultant"] == 2^496,
        "report exact intrinsic resultant",
    )
    require(
        report["intrinsic_integer_resultant_exponent"] == 496,
        "report intrinsic resultant exponent",
    )
    require(
        report["intrinsic_chebyshev_identity_count"] == 17,
        "report intrinsic identity count",
    )
    require(
        report["intrinsic_second_kind_basis_rank"] == 17,
        "report second-kind basis rank",
    )
    require(
        report["intrinsic_high_matrix_dimensions"] == (16, 17),
        "report intrinsic matrix dimensions",
    )
    require(
        report["intrinsic_high_matrix_rank"] == 16,
        "report intrinsic matrix rank",
    )
    require(
        report["intrinsic_high_matrix_kernel_dimension"] == 1,
        "report intrinsic kernel dimension",
    )
    require(
        report["intrinsic_kernel_coefficients"]
        == EXPECTED_INTRINSIC_KERNEL_COEFFICIENTS,
        "report intrinsic kernel coefficients",
    )
    require(
        report["intrinsic_kernel_is_U16"] is True,
        "report intrinsic kernel identification",
    )
    require(
        report["intrinsic_rotated_U16_remainder_degree"] == 15,
        "report intrinsic rotated U16 degree",
    )
    require(
        report["intrinsic_U16_locator_gcd_degree"] == 0,
        "report intrinsic U16/locator gcd",
    )
    require(
        report["intrinsic_U16_nonzero_on_quotient"] is True,
        "report intrinsic U16 root exclusion",
    )
    require(
        report["intrinsic_T31_locator_gcd_degree"] == 0,
        "report intrinsic multiplier/locator gcd",
    )
    require(report["punctured_quotient_size"] == 31, "report punctured size")
    require(report["subset_size"] == 17, "report subset size")
    require(
        report["minimum_pair_intersection"]
        == 2 * report["subset_size"] - report["punctured_quotient_size"]
        == 3,
        "report intersection floor",
    )
    require(
        report["rotation_injective_on_punctured_17_subsets"] is True,
        "report injectivity conclusion",
    )
    require(
        report["intrinsic_rotation_injective_on_punctured_17_subsets"] is True,
        "report intrinsic injectivity conclusion",
    )
    require(report["scope"] == "ROTATION_ROUTE_CUT_ONLY_ROW_OPEN", "report scope")


def run_check():
    report = derive_report()
    validate_report(report)
    print("M31 Chebyshev order-32 rotation injectivity Sage replay: PASS")
    print("locator: degree=32 monic=True roots=32 simple_nonzero=True")
    print("literal Y^31 high map: dimensions=(16,17) rank=16 kernel_dimension=1")
    print("literal K0 coefficients:", report["K0_coefficients"])
    print("literal rotated K0: remainder_degree=15 gcd(K0,Lambda)=1")
    print("intrinsic T_31 high map: dimensions=(16,17) rank=16 kernel_dimension=1")
    print("intrinsic kernel U16 coefficients:", report["intrinsic_kernel_coefficients"])
    print("intrinsic identities: T31*U_j=T_(31-j) mod T32 for j=0,...,16")
    print("intrinsic resultant: Res_Z(U16,T32)=2^496; gcd_Fp(U16,T32)=1")
    print("intersection: two 17-subsets of 31 points meet in at least 3 points")
    print("conclusion: both rotated high-prefix maps are injective; M31 list row OPEN")


def run_tamper_selftest():
    report = derive_report()
    validate_report(report)
    mutations = (
        ("prime", "p", P - 2),
        ("integral leading coefficient", "integral_T32_leading_coefficient", 2^31 - 1),
        ("deployed leading coefficient", "deployed_T32_leading_coefficient", 2),
        ("locator degree", "locator_degree", 31),
        ("locator monic", "locator_monic", False),
        ("locator squarefree", "locator_squarefree", False),
        ("locator hash", "locator_coefficient_sha256", "0" * 64),
        ("root count", "quotient_root_count", 31),
        ("root distinctness", "quotient_roots_distinct", False),
        ("root nonzero", "quotient_roots_nonzero", False),
        ("root antipodality", "quotient_roots_antipodal", False),
        ("root hash", "quotient_root_sha256", "f" * 64),
        ("literal map", "literal_rotation_multiplier", "T_31(Y)"),
        ("matrix dimensions", "high_matrix_dimensions", (15, 17)),
        ("matrix rank", "high_matrix_rank", 15),
        ("kernel dimension", "high_matrix_kernel_dimension", 2),
        ("K0 coefficients", "K0_coefficients", (2,) + EXPECTED_KERNEL_COEFFICIENTS[1:]),
        ("rotated remainder degree", "rotated_K0_remainder_degree", 16),
        ("K0 gcd", "K0_locator_gcd_degree", 1),
        ("K0 root exclusion", "K0_nonzero_on_quotient", False),
        ("intrinsic map", "intrinsic_rotation_multiplier", "Y^31"),
        ("intrinsic resultant", "intrinsic_integer_resultant", 2^495),
        ("intrinsic resultant exponent", "intrinsic_integer_resultant_exponent", 495),
        ("intrinsic identity count", "intrinsic_chebyshev_identity_count", 16),
        ("second-kind basis rank", "intrinsic_second_kind_basis_rank", 16),
        ("intrinsic matrix dimensions", "intrinsic_high_matrix_dimensions", (15, 17)),
        ("intrinsic matrix rank", "intrinsic_high_matrix_rank", 15),
        ("intrinsic kernel dimension", "intrinsic_high_matrix_kernel_dimension", 2),
        (
            "intrinsic kernel coefficients",
            "intrinsic_kernel_coefficients",
            (2,) + EXPECTED_INTRINSIC_KERNEL_COEFFICIENTS[1:],
        ),
        ("intrinsic kernel identity", "intrinsic_kernel_is_U16", False),
        ("intrinsic remainder degree", "intrinsic_rotated_U16_remainder_degree", 16),
        ("intrinsic U16 gcd", "intrinsic_U16_locator_gcd_degree", 1),
        ("intrinsic U16 root exclusion", "intrinsic_U16_nonzero_on_quotient", False),
        ("intrinsic multiplier gcd", "intrinsic_T31_locator_gcd_degree", 1),
        ("punctured size", "punctured_quotient_size", 32),
        ("subset size", "subset_size", 16),
        ("intersection floor", "minimum_pair_intersection", 2),
        ("injectivity", "rotation_injective_on_punctured_17_subsets", False),
        (
            "intrinsic injectivity",
            "intrinsic_rotation_injective_on_punctured_17_subsets",
            False,
        ),
        ("scope", "scope", "ROW_CLOSED"),
    )
    rejected = 0
    for label, key, bad_value in mutations:
        tampered = copy.deepcopy(report)
        tampered[key] = bad_value
        try:
            validate_report(tampered)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError("tamper escaped validation: %s" % label)
    require(rejected == len(mutations), "all semantic mutations rejected")
    print(
        "M31 Chebyshev order-32 rotation injectivity tamper-selftest: PASS "
        "(%s/%s rejected)" % (rejected, len(mutations))
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--tamper-selftest", action="store_true")
    arguments = parser.parse_args()
    if arguments.check:
        run_check()
    else:
        run_tamper_selftest()


if __name__ == "__main__":
    main()
