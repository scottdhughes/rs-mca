#!/usr/bin/env sage
"""Independent Sage replay for the M31 whole-ball Pluecker route cut."""

from itertools import permutations, product


def theta_matrix(polynomials, D):
    base = polynomials[0].base_ring()
    e = max(poly.degree() for poly in polynomials)
    out = matrix(base, e + D, len(polynomials) * D)
    for block, poly in enumerate(polynomials):
        for shift in range(D):
            for exponent, coefficient in enumerate(poly.list()):
                out[exponent + shift, block * D + shift] = coefficient
    return out


def parity_products_from_factors(factors):
    A0, A1, B0, B1, C0, C1 = factors
    return (A0 * B0 * C0, A1 * B0 * C1, A0 * B1 * C1, A1 * B1 * C0)


def infer_forney(polynomials):
    e = max(poly.degree() for poly in polynomials)
    nullities = {
        D: 4 * D - theta_matrix(polynomials, D).rank()
        for D in range(e + 2)
    }
    candidates = []
    for mu1 in range(e + 1):
        for mu2 in range(mu1, e + 1):
            mu3 = e - mu1 - mu2
            if mu3 < mu2:
                continue
            candidate = (mu1, mu2, mu3)
            if all(
                nullities[D] == sum(max(0, D - mu) for mu in candidate)
                for D in nullities
            ):
                candidates.append(candidate)
    if len(candidates) != 1:
        raise RuntimeError("Forney profile is not uniquely determined")
    return candidates[0]


def crt_residues(factors, H):
    A0, A1, B0, B1, C0, C1 = factors
    H00, H10, H01, H11 = H
    return (
        (H10 * B0 * C1 + H11 * B1 * C0) % A0,
        (H00 * B0 * C0 + H01 * B1 * C1) % A1,
        (H01 * A0 * C1 + H11 * A1 * C0) % B0,
        (H00 * A0 * C0 + H10 * A1 * C1) % B1,
        (H10 * A1 * B0 + H01 * A0 * B1) % C0,
        (H00 * A0 * B0 + H11 * A1 * B1) % C1,
    )


def normalized_pgl2(p):
    representatives = set()
    for entries in product(range(p), repeat=int(4)):
        a, b, c, d = entries
        if (a * d - b * c) % p == 0:
            continue
        first = next(value for value in entries if value)
        inv = inverse_mod(first, p)
        representatives.add(tuple((value * inv) % p for value in entries))
    return sorted(representatives)


def pgl2_stabilizer(support, p):
    target = set(support)
    representatives = normalized_pgl2(p)
    stabilizer = []
    for a, b, c, d in representatives:
        image = set()
        for point in support:
            denominator = (c * point + d) % p
            if denominator == 0:
                break
            image.add(((a * point + b) * inverse_mod(denominator, p)) % p)
        else:
            if image == target:
                stabilizer.append((a, b, c, d))
    return representatives, stabilizer


# Exact deployed arithmetic.
p = 2^31 - 1
n = 2^21
K = 2^20
agreement = 1116023
sigma = agreement - K
radius = n - agreement
budget = p^4 // 2^100
r = 33 * 1024
assert (p, n, K, agreement) == (2147483647, 2097152, 1048576, 1116023)
assert (sigma, radius, budget) == (67447, 981129, 16777215)
assert 2 * r - sigma == 137
assert (r, 2 * r, 3 * r) == (33792, 67584, 101376)
assert 33928 - r == 136
assert 2 * sigma - r == 101102
assert 3 * r + sigma - 137 == 168686
assert r - 136 == 33656


# Symbolic determinant factorization for r=1.
ParameterRing = PolynomialRing(QQ, names=("a0", "a1", "b0", "b1", "c0", "c1"))
a0, a1, b0, b1, c0, c1 = ParameterRing.gens()
FunctionField = FractionField(ParameterRing)
R.<x> = PolynomialRing(FunctionField)
factors = tuple(x - FunctionField(value) for value in (a0, a1, b0, b1, c0, c1))
polynomials = parity_products_from_factors(factors)
determinant = theta_matrix(polynomials, 1).determinant()
Phi = (
    a0*a1*b0 + a0*a1*b1 - a0*b0*b1 - a1*b0*b1
    - a0*a1*c0 + b0*b1*c0 - a0*a1*c1 + b0*b1*c1
    + a0*c0*c1 + a1*c0*c1 - b0*c0*c1 - b1*c0*c1
)
expected_determinant = (a1 - a0) * (b1 - b0) * (c0 - c1) * Phi
assert determinant == FunctionField(expected_determinant)


# Exhaustive GF(7) census and the exact Pluecker sign fixture.
F7 = GF(7)
R7.<y> = PolynomialRing(F7)
rank_counts = {3: 0, 4: 0}
phi_zero = 0
for values in permutations(range(7), int(6)):
    aa0, aa1, bb0, bb1, cc0, cc1 = map(F7, values)
    local_factors = tuple(y - value for value in (aa0, aa1, bb0, bb1, cc0, cc1))
    local_polynomials = parity_products_from_factors(local_factors)
    rank = theta_matrix(local_polynomials, 1).rank()
    if rank not in rank_counts:
        raise RuntimeError("unexpected GF(7) rank")
    rank_counts[rank] += 1
    local_phi = (
        aa0*aa1*bb0 + aa0*aa1*bb1 - aa0*bb0*bb1 - aa1*bb0*bb1
        - aa0*aa1*cc0 + bb0*bb1*cc0 - aa0*aa1*cc1 + bb0*bb1*cc1
        + aa0*cc0*cc1 + aa1*cc0*cc1 - bb0*cc0*cc1 - bb1*cc0*cc1
    )
    if local_phi == 0:
        phi_zero += 1
assert rank_counts == {3: 1344, 4: 3696}
assert phi_zero == 1344

toy_values = (0, 1, 2, 3, 4, 6)
toy_factors = tuple(y - F7(value) for value in toy_values)
toy_polynomials = parity_products_from_factors(toy_factors)
S = vector(R7, (1, 3, 6, 4))
T = vector(R7, (1, y, 3 + 3*y, 3*y))
assert sum(S[i] * toy_polynomials[i] for i in range(4)) == 0
assert sum(T[i] * toy_polynomials[i] for i in range(4)) == 0
assert infer_forney(toy_polynomials) == (0, 1, 2)
Delta = {(i, j): S[i] * T[j] - S[j] * T[i] for i in range(4) for j in range(i + 1, 4)}
A0, A1, B0, B1, C0, C1 = toy_factors
quotients = {
    "A0": Delta[1, 3] // A0,
    "A1": Delta[0, 2] // A1,
    "B0": Delta[2, 3] // B0,
    "B1": Delta[0, 1] // B1,
    "C0": Delta[1, 2] // C0,
    "C1": Delta[0, 3] // C1,
}
assert quotients == {"A0": 5, "A1": 3, "B0": 6, "B1": 1, "C0": 3, "C1": 3}
qA0, qA1 = quotients["A0"], quotients["A1"]
qB0, qB1 = quotients["B0"], quotients["B1"]
qC0, qC1 = quotients["C0"], quotients["C1"]
assert A0*qA1 + B0*qB1 + C0*qC1 == 0
assert -A1*qA0 + B0*qB1 - C1*qC0 == 0
assert A0*qA1 - B1*qB0 + C1*qC0 == 0
assert A1*qA0 + B1*qB0 + C0*qC1 == 0
assert B0*B1*qB0*qB1 - A0*A1*qA0*qA1 + C0*C1*qC0*qC1 == 0
assert all(residue == 0 for residue in crt_residues(toy_factors, S))

# Exhaust every constant row on the primitive GF(7) face: the global and
# six-CRT kernels agree exactly.
for coefficients in product(F7, repeat=int(4)):
    global_zero = sum(coefficients[i] * toy_polynomials[i] for i in range(4)) == 0
    crt_zero = all(residue == 0 for residue in crt_residues(toy_factors, coefficients))
    assert global_zero == crt_zero


# Exact PGL-asymmetric degree-two primitive control over GF(23).
F23 = GF(23)
R23.<z> = PolynomialRing(F23)
support23 = (1, 2, 4, 5, 7, 8, 10, 12, 13, 15, 19, 20)
chunks23 = ((1, 2), (10, 12), (4, 20), (8, 19), (5, 15), (7, 13))
factors23 = tuple(prod(z - F23(point) for point in chunk) for chunk in chunks23)
polynomials23 = parity_products_from_factors(factors23)
ranks23 = tuple(theta_matrix(polynomials23, D).rank() for D in range(1, 7))
assert ranks23 == (3, 6, 8, 10, 11, 12)
assert infer_forney(polynomials23) == (0, 2, 4)
constant23 = vector(R23, (1, 9, 18, 18))
assert sum(constant23[i] * polynomials23[i] for i in range(4)) == 0
assert all(residue == 0 for residue in crt_residues(factors23, constant23))

theta3 = theta_matrix(polynomials23, 3)
cokernel23 = vector(F23, (1, 5, 12, 0, 8, 8, 15, 10, 8))
assert theta3.nrows() == 9 and theta3.ncols() == 12 and theta3.rank() == 8
assert cokernel23 * theta3 == 0

pgl23, stabilizer23 = pgl2_stabilizer(support23, 23)
assert len(pgl23) == 12144
assert stabilizer23 == [(1, 0, 0, 1)]

print("M31 whole-ball Pluecker Sage replay PASS")
print("deployed arithmetic: 137 cells / tau=0..136 / h=137-tau PASS")
print("symbolic r=1 determinant factorization PASS")
print("GF(7) census: 3696 rank 4 + 1344 rank 3 PASS")
print("GF(7) Pluecker signs and six CRT congruences PASS")
print("GF(23) profile (0,2,4) with trivial PGL2 stabilizer PASS")
print("RESULT: UNIVERSAL_SOURCE_BRIDGE_REQUIRED; M31 rows remain OPEN")
