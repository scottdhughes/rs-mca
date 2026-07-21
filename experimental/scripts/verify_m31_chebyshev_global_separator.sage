#!/usr/bin/env sage
"""Independent Sage replay for the M31 Chebyshev global-separator packet."""

from array import array


p = 2^31 - 1
n = 2^21
k = 2^20
agreement = 1116023
sigma = agreement - k
radius = n - agreement
fold = 2^10

EXPECTED_Q = (462183554, 751088031, 26070540)
EXPECTED_DET = 398200308
EXPECTED_PREFIX_HASH = 1877696184


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def cmul(left, right):
    return (
        (left[0] * right[0] - left[1] * right[1]) % p,
        (left[0] * right[1] + left[1] * right[0]) % p,
    )


def cpow(value, exponent):
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = cmul(out, value)
        value = cmul(value, value)
        exponent >>= 1
    return out


def cheb_value(degree, value):
    if degree == 0:
        return 1
    if degree == 1:
        return value % p
    old, new = 1, value % p
    for _ in range(2, degree + 1):
        old, new = new, (2 * value * new - old) % p
    return new


def packed_quartic(degree):
    """Recompute the unnormalized order-(degree-2) transvectant modulo p."""
    # Sage's preparser makes integers in source expressions Sage Integers.
    # Keep the array dimensions and
    # indices native Python integers so this replay also exercises the packed
    # O(n)-memory implementation used by the Python verifier.
    n_int = int(degree)
    half = n_int // 2
    order = n_int - 2
    fac = array("I", [1])
    for value in range(1, n_int + 1):
        fac.append(int(fac[-1] * value % p))
    ifac = array("I", [0]) * int(n_int + 1)
    ifac[n_int] = int(inverse_mod(fac[n_int], p))
    for value in range(n_int, 0, -1):
        ifac[value - 1] = int(ifac[value] * value % p)

    coeff = array("I", [0]) * int(half + 1)
    two_power = int(power_mod(2, n_int - 1, p))
    quarter = inverse_mod(4, p)
    for j in range(half + 1):
        xdeg = n_int - 2 * j
        value = n_int * two_power % p
        value = value * fac[n_int - j - 1] % p
        value = value * ifac[j] % p
        value = value * ifac[xdeg] % p
        coeff[j] = int((-value if j % 2 else value) % p)
        two_power = int(two_power * quarter % p)

    def output(index_sum, allowed_heights):
        total = 0
        for j in range(half + 1):
            other = index_sum - j
            if other < 0 or other > half:
                continue
            for height in allowed_heights:
                i = 2 * j - height
                x1, z1 = 2 - height, height
                x2 = n_int - 2 * index_sum + height
                z2 = 2 - x2
                if i < 0 or i > order or min(x1, z1, x2, z2) < 0:
                    continue
                ax, az = n_int - 2 * j, 2 * j
                bx, bz = n_int - 2 * other, 2 * other
                value = coeff[j] * coeff[other] % p
                value = value * fac[order] % p
                value = value * ifac[i] * ifac[order - i] % p
                value = value * fac[ax] * ifac[x1] % p
                value = value * fac[az] * ifac[z1] % p
                value = value * fac[bx] * ifac[x2] % p
                value = value * fac[bz] * ifac[z2] % p
                if i % 2:
                    value = -value
                total = (total + value) % p
        return Integer(total)

    return (
        output(half - 1, (0,)),
        output(half, (0, 1, 2)),
        output(half + 1, (2,)),
    )


def quotient_replay():
    generator = (1717986917, 1288490189)
    check((generator[0]^2 + generator[1]^2) % p == 1, "norm one")
    check(cpow(generator, 2^30) == (p - 1, 0), "full torus order")
    qgen = cpow(generator, 2^18)
    check(cpow(qgen, 8192) == (1, 0), "quotient upper order")
    check(cpow(qgen, 4096) == (p - 1, 0), "quotient exact order")

    step = cmul(qgen, qgen)
    current = qgen
    roots = []
    for _ in range(2048):
        roots.append(Integer(current[0]))
        current = cmul(current, step)
    check(len(set(roots)) == 2048, "quotient distinct")
    check(all(cheb_value(2048, value) == 0 for value in roots), "quotient T2048")
    prefix_hash = Integer(
        sum((index + 1) * value for index, value in enumerate(roots[:198])) % p
    )
    check(prefix_hash == EXPECTED_PREFIX_HASH, "quotient ordered-prefix hash")

    Fp = GF(p)
    R.<Y> = PolynomialRing(Fp)
    chunks = [roots[33 * index : 33 * (index + 1)] for index in range(6)]
    factors = [prod(Y - Fp(root) for root in chunk) for chunk in chunks]
    a0, a1, b0, b1, c0, c1 = factors
    locators = (
        a0 * b0 * c0,
        a1 * b0 * c1,
        a0 * b1 * c1,
        a1 * b1 * c0,
    )
    check(all(poly.degree() == 99 for poly in locators), "lower locator degrees")
    M = matrix(Fp, 132, 132)
    for block, polynomial in enumerate(locators):
        for shift in range(33):
            for degree, coefficient in enumerate(polynomial.list()):
                M[degree + shift, 33 * block + shift] = coefficient
    determinant = Integer(M.det())
    check(determinant == EXPECTED_DET, "quotient determinant")
    check(M.rank() == 132, "quotient full rank")
    return determinant


check((p, n, k, sigma, radius) == (2147483647, 2097152, 1048576, 67447, 981129), "deployed constants")
Q = packed_quartic(n)
check(Q == EXPECTED_Q, "deployed quartic coefficients")
A, B, C = Q
check((B^2 - 4 * A * C) % p == 1653303809, "quartic root discriminant")
check((B^2 + 12 * A * C) % p == 299132536, "quartic I")
check((72 * A * B * C - 2 * B^3) % p == 1054263609, "quartic J")
check(power_mod(C * inverse_mod(A, p) % p, (p - 1) // 2, p) == p - 1, "nonsquare reciprocal")

determinant = quotient_replay()
check(33 * fold == 33792 < sigma, "lifted Forney gate")
check(3 * 33792 == 101376, "lifted index sum")
check(radius - 101376 == 879753, "common core")
check(n - 198 * 1024 - 2 * 879753 == 134894, "embedding count")
check(15 * sigma < k < 16 * sigma, "rank-16 boundary")
check(p - 2 * radius == 2145521389, "pair survivor margin")

# Native small-symbolic transvectants guard every packed coefficient, sign,
# binomial, and index convention used by the O(n) evaluator.
S.<X,Z> = PolynomialRing(QQ, 2)
for toy_n in (4, 6, 8, 10, 16):
    one = S(1)
    tx = X
    old, current = one, tx
    for _ in range(2, toy_n + 1):
        old, current = current, 2 * X * current - Z^2 * old
    Ftoy = current if toy_n > 1 else tx
    order = toy_n - 2
    transvectant = sum(
        (-1)^i * binomial(order, i)
        * Ftoy.derivative(X, order - i).derivative(Z, i)
        * Ftoy.derivative(X, i).derivative(Z, order - i)
        for i in range(order + 1)
    )
    allowed = {X^4, X^2 * Z^2, Z^4}
    check(transvectant.total_degree() == 4, "toy transvectant degree")
    check(set(transvectant.monomials()).issubset(allowed), "toy transvectant support")
    symbolic_coefficients = tuple(
        Integer(transvectant.monomial_coefficient(monomial)) % p
        for monomial in (X^4, X^2 * Z^2, Z^4)
    )
    check(symbolic_coefficients == packed_quartic(toy_n), "toy packed coefficients")

print("Sage M31 Chebyshev global separator: PASS")
print("quartic covariant:", Q)
print("quotient determinant:", determinant)
print("lifted Forney profile: (33792, 33792, 33792)")
print("pairwise survivor / rank-16 boundary: PASS")
print("M31 list row: OPEN; ledger movement: 0")
