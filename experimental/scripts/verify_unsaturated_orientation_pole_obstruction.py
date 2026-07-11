#!/usr/bin/env python3
"""Replay the pre-atlas unsaturated-orientation pole route cut.

This verifier is zero-argument and stdlib-only.  It checks two independent
parts of experimental/notes/thresholds/
unsaturated_orientation_pole_obstruction.md:

1. exact uniform-fiber occupancy identities and support add-back; and
2. small finite instances of the complete locator-prefix/pole-line bijection,
   including a proper scalar extension F_25/F_5, the depth-zero F_10009
   orientation examples, and the positive-depth F_109 example.

The pole checks include the locator degree bound, separating-pole injection,
line identity, exact full agreement, support-wise nontriviality, and the
converse prefix criterion.  They certify the pre-atlas algebra only; they do
not classify any witness through C1--C8.
"""

from collections import Counter, defaultdict
from itertools import combinations
from math import comb


CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def ceil_div(numerator, denominator):
    require(denominator > 0, "ceil_div requires a positive denominator")
    return (numerator + denominator - 1) // denominator


def is_prime(value):
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


class PrimeField:
    def __init__(self, prime):
        require(is_prime(prime), f"{prime} is not prime")
        self.p = prime
        self.order = prime
        self.zero = 0
        self.one = 1

    def embed(self, value):
        return value % self.p

    def add(self, left, right):
        return (left + right) % self.p

    def sub(self, left, right):
        return (left - right) % self.p

    def neg(self, value):
        return (-value) % self.p

    def mul(self, left, right):
        return (left * right) % self.p

    def inv(self, value):
        require(value % self.p != 0, "division by zero in prime field")
        return pow(value, self.p - 2, self.p)

    def div(self, numerator, denominator):
        return self.mul(numerator, self.inv(denominator))

    def format(self, value):
        return str(value)


class QuadraticField:
    """F_(p^2)=F_p[u]/(u^2-nonsquare), represented by pairs (a,b)."""

    def __init__(self, prime, nonsquare):
        require(is_prime(prime), f"{prime} is not prime")
        require(
            pow(nonsquare, (prime - 1) // 2, prime) == prime - 1,
            f"{nonsquare} is not a nonsquare modulo {prime}",
        )
        self.p = prime
        self.nonsquare = nonsquare % prime
        self.order = prime * prime
        self.zero = (0, 0)
        self.one = (1, 0)

    def embed(self, value):
        return (value % self.p, 0)

    def add(self, left, right):
        return ((left[0] + right[0]) % self.p, (left[1] + right[1]) % self.p)

    def sub(self, left, right):
        return ((left[0] - right[0]) % self.p, (left[1] - right[1]) % self.p)

    def neg(self, value):
        return ((-value[0]) % self.p, (-value[1]) % self.p)

    def mul(self, left, right):
        a, b = left
        c, d = right
        return (
            (a * c + self.nonsquare * b * d) % self.p,
            (a * d + b * c) % self.p,
        )

    def inv(self, value):
        a, b = value
        denominator = (a * a - self.nonsquare * b * b) % self.p
        require(denominator != 0, "division by zero in quadratic field")
        inverse_denominator = pow(denominator, self.p - 2, self.p)
        return (
            (a * inverse_denominator) % self.p,
            (-b * inverse_denominator) % self.p,
        )

    def div(self, numerator, denominator):
        return self.mul(numerator, self.inv(denominator))

    def format(self, value):
        return f"({value[0]}+{value[1]}u)"


def poly_trim(polynomial, field):
    polynomial = list(polynomial)
    while len(polynomial) > 1 and polynomial[-1] == field.zero:
        polynomial.pop()
    return polynomial


def poly_degree(polynomial, field):
    polynomial = poly_trim(polynomial, field)
    return -1 if polynomial == [field.zero] else len(polynomial) - 1


def poly_add(left, right, field):
    size = max(len(left), len(right))
    out = [field.zero] * size
    for index in range(size):
        lvalue = left[index] if index < len(left) else field.zero
        rvalue = right[index] if index < len(right) else field.zero
        out[index] = field.add(lvalue, rvalue)
    return poly_trim(out, field)


def poly_sub(left, right, field):
    size = max(len(left), len(right))
    out = [field.zero] * size
    for index in range(size):
        lvalue = left[index] if index < len(left) else field.zero
        rvalue = right[index] if index < len(right) else field.zero
        out[index] = field.sub(lvalue, rvalue)
    return poly_trim(out, field)


def poly_mul(left, right, field):
    out = [field.zero] * (len(left) + len(right) - 1)
    for left_power, left_coefficient in enumerate(left):
        for right_power, right_coefficient in enumerate(right):
            product = field.mul(left_coefficient, right_coefficient)
            out[left_power + right_power] = field.add(
                out[left_power + right_power], product
            )
    return poly_trim(out, field)


def poly_scale(polynomial, scalar, field):
    return poly_trim([field.mul(scalar, value) for value in polynomial], field)


def poly_eval(polynomial, point, field):
    value = field.zero
    for coefficient in reversed(polynomial):
        value = field.add(field.mul(value, point), coefficient)
    return value


def divide_by_x_minus_alpha(numerator, alpha, field):
    numerator = poly_trim(numerator, field)
    require(
        poly_eval(numerator, alpha, field) == field.zero,
        "linear division called on a nonvanishing numerator",
    )
    degree = poly_degree(numerator, field)
    if degree <= 0:
        return [field.zero]

    quotient = [field.zero] * degree
    quotient[degree - 1] = numerator[degree]
    for power in range(degree - 1, 0, -1):
        quotient[power - 1] = field.add(
            numerator[power], field.mul(alpha, quotient[power])
        )
    remainder = field.add(numerator[0], field.mul(alpha, quotient[0]))
    require(remainder == field.zero, "synthetic division left a remainder")
    return poly_trim(quotient, field)


def interpolate(points, values, field):
    require(len(points) == len(values), "interpolation data length mismatch")
    require(len(set(points)) == len(points), "interpolation points are not distinct")
    result = [field.zero]
    for index, point in enumerate(points):
        basis = [field.one]
        denominator = field.one
        for other_index, other_point in enumerate(points):
            if other_index == index:
                continue
            basis = poly_mul(basis, [field.neg(other_point), field.one], field)
            denominator = field.mul(denominator, field.sub(point, other_point))
        scale = field.div(values[index], denominator)
        result = poly_add(result, poly_scale(basis, scale, field), field)
    return poly_trim(result, field)


def locator(support, field):
    polynomial = [field.one]
    for point in support:
        polynomial = poly_mul(polynomial, [field.neg(point), field.one], field)
    return polynomial


def locator_prefix(locator_polynomial, size, width):
    return tuple(locator_polynomial[size - index] for index in range(1, width + 1))


def prefix_polynomial(size, prefix, field):
    polynomial = [field.zero] * (size + 1)
    polynomial[size] = field.one
    for index, coefficient in enumerate(prefix, 1):
        polynomial[size - index] = coefficient
    return polynomial


def integer_poly_mul(left, right):
    out = [0] * (len(left) + len(right) - 1)
    for left_power, left_coefficient in enumerate(left):
        for right_power, right_coefficient in enumerate(right):
            out[left_power + right_power] += left_coefficient * right_coefficient
    return out


def partial_orientation_coefficient(c, partial_fibers, rho):
    one_fiber = [0] * (c + 1)
    for selected in range(1, c):
        one_fiber[selected] = comb(c, selected)
    polynomial = [1]
    for _ in range(partial_fibers):
        polynomial = integer_poly_mul(polynomial, one_fiber)
    return polynomial[rho] if 0 <= rho < len(polynomial) else 0


def occupancy_formula(b, c, fiber_count, profile):
    exceptional, full, partial, rho = profile
    if not (0 <= exceptional <= b):
        return 0
    if not (0 <= full <= fiber_count and 0 <= partial <= fiber_count - full):
        return 0
    coefficient = partial_orientation_coefficient(c, partial, rho)
    return (
        comb(b, exceptional)
        * comb(fiber_count, partial)
        * comb(fiber_count - partial, full)
        * coefficient
    )


def occupancy_profile(selected, exceptional_points, fibers):
    selected = set(selected)
    exceptional = len(selected.intersection(exceptional_points))
    full = 0
    partial = 0
    rho = 0
    for fiber in fibers:
        count = len(selected.intersection(fiber))
        if count == len(fiber):
            full += 1
        elif count > 0:
            partial += 1
            rho += count
    return exceptional, full, partial, rho


def abstract_uniform_system(b, c, fiber_count):
    exceptional = tuple(range(b))
    fibers = []
    cursor = b
    for _ in range(fiber_count):
        fibers.append(tuple(range(cursor, cursor + c)))
        cursor += c
    return tuple(range(cursor)), exceptional, tuple(fibers)


def validate_occupancy_system(b, c, fiber_count):
    domain, exceptional, fibers = abstract_uniform_system(b, c, fiber_count)
    counts = Counter()
    for size in range(len(domain) + 1):
        for selected in combinations(domain, size):
            counts[occupancy_profile(selected, exceptional, fibers)] += 1

    nonempty_slices = 0
    for exceptional_count in range(b + 1):
        for full in range(fiber_count + 1):
            for partial in range(fiber_count + 1):
                for rho in range(c * fiber_count + 1):
                    profile = (exceptional_count, full, partial, rho)
                    expected = occupancy_formula(b, c, fiber_count, profile)
                    actual = counts[profile]
                    require(
                        actual == expected,
                        f"occupancy mismatch for {(b, c, fiber_count, profile)}: "
                        f"{actual}!={expected}",
                    )
                    if actual:
                        nonempty_slices += 1

    for size in range(len(domain) + 1):
        add_back = sum(
            count
            for profile, count in counts.items()
            if profile[0] + c * profile[1] + profile[3] == size
        )
        require(
            add_back == comb(len(domain), size),
            f"occupancy add-back failed at size {size}",
        )
    require(sum(counts.values()) == 2 ** len(domain), "total occupancy add-back failed")
    return nonempty_slices


def power_fibers(domain, exponent, prime):
    grouped = defaultdict(list)
    for point in domain:
        grouped[pow(point, exponent, prime)].append(point)
    fibers = tuple(tuple(sorted(points)) for _, points in sorted(grouped.items()))
    require(bool(fibers), "power map has no fibers")
    require(
        all(len(fiber) == exponent for fiber in fibers),
        "power map does not have the requested uniform fiber size",
    )
    require(sum(len(fiber) for fiber in fibers) == len(domain), "power fibers miss points")
    return fibers


def verify_complete_pole_bijection(base, scalar, domain, size, width, prefix, alpha):
    require(2 <= size <= len(domain), "invalid support size")
    require(0 <= width <= size - 2, "invalid prefix depth")
    require(len(prefix) == width, "prefix length mismatch")
    k = size - width - 1

    supports = tuple(combinations(domain, size))
    locators = {
        support: locator(tuple(base.embed(point) for point in support), base)
        for support in supports
    }
    prefixes = {
        support: locator_prefix(polynomial, size, width)
        for support, polynomial in locators.items()
    }
    complete_fiber = tuple(support for support in supports if prefixes[support] == prefix)
    require(bool(complete_fiber), "selected prefix fiber is empty")
    require(
        alpha not in {scalar.embed(point) for point in domain},
        "pole lies in the evaluation domain",
    )

    values = []
    for support in complete_fiber:
        locator_scalar = [scalar.embed(value) for value in locators[support]]
        values.append(poly_eval(locator_scalar, alpha, scalar))
    require(len(values) == len(set(values)), "pole does not separate locator values")

    prefix_base = tuple(base.embed(value) for value in prefix)
    u_base = prefix_polynomial(size, prefix_base, base)
    u_scalar = [scalar.embed(value) for value in u_base]

    # This is the finite converse: U_z-Q_T has degree <=k exactly for supports
    # in the complete prefix fiber.  Since size>k, such a polynomial is the
    # unique possible exact-support explanation before pole division.
    for support in supports:
        candidate = poly_sub(u_base, locators[support], base)
        require(
            (poly_degree(candidate, base) <= k) == (prefixes[support] == prefix),
            "converse prefix criterion failed",
        )

    slopes = {}
    for support in complete_fiber:
        locator_scalar = [scalar.embed(value) for value in locators[support]]
        p_scalar = poly_sub(u_scalar, locator_scalar, scalar)
        require(poly_degree(p_scalar, scalar) <= k, "list polynomial degree exceeds k")

        gamma = poly_eval(p_scalar, alpha, scalar)
        numerator = list(p_scalar)
        numerator[0] = scalar.sub(numerator[0], gamma)
        h_polynomial = divide_by_x_minus_alpha(numerator, alpha, scalar)
        require(poly_degree(h_polynomial, scalar) < k, "pole quotient degree exceeds k-1")
        require(
            gamma
            == scalar.sub(
                poly_eval(u_scalar, alpha, scalar),
                poly_eval(locator_scalar, alpha, scalar),
            ),
            "slope is not U_z(alpha)-Q_S(alpha)",
        )

        agreement = []
        for point in domain:
            scalar_point = scalar.embed(point)
            inverse_denominator = scalar.inv(scalar.sub(scalar_point, alpha))
            r_zero = scalar.mul(poly_eval(u_scalar, scalar_point, scalar), inverse_denominator)
            r_one = scalar.neg(inverse_denominator)
            residual = scalar.sub(
                scalar.add(r_zero, scalar.mul(gamma, r_one)),
                poly_eval(h_polynomial, scalar_point, scalar),
            )
            expected_residual = scalar.mul(
                poly_eval(locator_scalar, scalar_point, scalar), inverse_denominator
            )
            require(residual == expected_residual, "pole-line identity failed")
            if residual == scalar.zero:
                agreement.append(point)
        require(tuple(agreement) == support, "full agreement set is not exactly the support")

        interpolation_points = [scalar.embed(point) for point in support[:k]]
        interpolation_values = [
            scalar.neg(scalar.inv(scalar.sub(point, alpha)))
            for point in interpolation_points
        ]
        attempted_r_one = interpolate(interpolation_points, interpolation_values, scalar)
        require(poly_degree(attempted_r_one, scalar) < k, "interpolant degree is too large")
        require(
            any(
                poly_eval(attempted_r_one, scalar.embed(point), scalar)
                != scalar.neg(scalar.inv(scalar.sub(scalar.embed(point), alpha)))
                for point in support
            ),
            "r_1 was unexpectedly explained on a noncommon support",
        )
        slopes[support] = gamma

    require(len(slopes) == len(complete_fiber), "support-to-witness map lost a support")
    require(len(set(slopes.values())) == len(complete_fiber), "support-to-slope map collided")
    return complete_fiber, slopes


def validate_profile_instance(
    name,
    base,
    scalar,
    domain,
    exponent,
    size,
    width,
    profile,
    alpha,
    prefix=None,
    expected_complete=None,
    expected_profile_fiber=None,
    expected_total_profile=None,
    expected_slopes=None,
):
    fibers = power_fibers(domain, exponent, base.p)
    all_supports = tuple(combinations(domain, size))
    support_profiles = {
        support: occupancy_profile(support, (), fibers) for support in all_supports
    }
    total_profile = sum(1 for value in support_profiles.values() if value == profile)
    formula = occupancy_formula(0, exponent, len(fibers), profile)
    require(total_profile == formula, f"{name}: finite occupancy formula mismatch")
    if expected_total_profile is not None:
        require(total_profile == expected_total_profile, f"{name}: unexpected profile total")

    base_locators = {
        support: locator(tuple(base.embed(point) for point in support), base)
        for support in all_supports
    }
    grouped_profile = defaultdict(list)
    for support in all_supports:
        if support_profiles[support] == profile:
            key = locator_prefix(base_locators[support], size, width)
            grouped_profile[key].append(support)
    require(bool(grouped_profile), f"{name}: profile has no prefix values")
    if prefix is None:
        prefix = min(
            grouped_profile,
            key=lambda key: (-len(grouped_profile[key]), key),
        )
    prefix = tuple(base.embed(value) for value in prefix)

    lower = ceil_div(total_profile, base.order ** width)
    profile_fiber = tuple(grouped_profile[prefix])
    require(
        len(profile_fiber) >= lower,
        f"{name}: profile-prefix fiber misses the pigeonhole lower bound",
    )
    if expected_profile_fiber is not None:
        require(
            len(profile_fiber) == expected_profile_fiber,
            f"{name}: unexpected profile-prefix count",
        )

    complete_fiber, slopes = verify_complete_pole_bijection(
        base, scalar, domain, size, width, prefix, alpha
    )
    if expected_complete is not None:
        require(len(complete_fiber) == expected_complete, f"{name}: complete prefix size changed")

    cell_slopes = {slopes[support] for support in profile_fiber}
    require(
        len(cell_slopes) == len(profile_fiber),
        f"{name}: diagonal profile cell lost actual slopes",
    )
    if width == 0:
        require(
            len(cell_slopes) == total_profile,
            f"{name}: depth-zero cell does not equal H_phi(lambda)",
        )
    if expected_slopes is not None:
        require(cell_slopes == expected_slopes, f"{name}: slope set changed")

    return {
        "name": name,
        "complete": len(complete_fiber),
        "profile_total": total_profile,
        "profile_fiber": len(profile_fiber),
        "lower": lower,
        "slopes": len(cell_slopes),
    }


def main():
    occupancy_rows = []
    for parameters in ((0, 2, 4), (1, 3, 3), (2, 4, 2)):
        slices = validate_occupancy_system(*parameters)
        occupancy_rows.append((parameters, slices))

    instances = []

    # A proper scalar extension.  Here u^2=2 over F_5.  With a=2 and w=0,
    # every locator difference has degree at most one, so alpha=u (outside the
    # base field) separates all six locators automatically.
    base_five = PrimeField(5)
    scalar_twenty_five = QuadraticField(5, 2)
    proper_extension_pole = (0, 1)
    require(
        proper_extension_pole
        not in {scalar_twenty_five.embed(value) for value in range(base_five.order)},
        "F_25 pole unexpectedly lies in the embedded base field",
    )
    instances.append(
        validate_profile_instance(
            "F_25/F_5 depth zero",
            base_five,
            scalar_twenty_five,
            (1, 2, 3, 4),
            exponent=2,
            size=2,
            width=0,
            profile=(0, 0, 2, 2),
            alpha=proper_extension_pole,
            prefix=(),
            expected_complete=6,
            expected_profile_fiber=4,
            expected_total_profile=4,
        )
    )

    base_10009 = PrimeField(10009)
    domain_10009 = (1, 792, 6706, 6382, 10008, 9217, 3303, 3627)
    for size, expected in ((2, 24), (3, 32), (4, 16)):
        instances.append(
            validate_profile_instance(
                f"F_10009 depth zero a={size}",
                base_10009,
                base_10009,
                domain_10009,
                exponent=2,
                size=size,
                width=0,
                profile=(0, 0, size, size),
                alpha=2,
                prefix=(),
                expected_complete=comb(8, size),
                expected_profile_fiber=expected,
                expected_total_profile=expected,
            )
        )

    base_109 = PrimeField(109)
    domain_109 = (1, 101, 64, 33, 63, 41, 108, 8, 45, 76, 46, 68)
    instances.append(
        validate_profile_instance(
            "F_109 positive depth",
            base_109,
            base_109,
            domain_109,
            exponent=2,
            size=3,
            width=1,
            profile=(0, 0, 3, 3),
            alpha=0,
            prefix=(0,),
            expected_complete=4,
            expected_profile_fiber=4,
            expected_total_profile=160,
            expected_slopes={1, 33, 76, 108},
        )
    )

    print("object: unsaturated orientation separating-pole pre-atlas route cut")
    for parameters, slices in occupancy_rows:
        print(
            "occupancy identity (b,c,N)=%s: %d nonempty slices PASS"
            % (parameters, slices)
        )
    for row in instances:
        print(
            "%s: complete=%d profile=%d selected=%d lower=%d slopes=%d PASS"
            % (
                row["name"],
                row["complete"],
                row["profile_total"],
                row["profile_fiber"],
                row["lower"],
                row["slopes"],
            )
        )
    print(f"RESULT: PASS ({CHECKS} checks)")


if __name__ == "__main__":
    main()
