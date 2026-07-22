#!/usr/bin/env sage
"""Independent Sage replay for the M31 fixed-template quotient route cut."""

import hashlib
import itertools
import json
import math


checks = 0


def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


p = 2^31 - 1
n = 2^21
K = 2^20
A = 1116023
RADIUS = n - A
w = A - K
c = 2048
N = n // c
Bstar = p^4 // 2^100

check(p == 2147483647, "prime")
check(is_prime(p), "Mersenne primality")
check((n, K, A, RADIUS, w, c, N, Bstar) ==
      (2097152, 1048576, 1116023, 981129, 67447, 2048, 1024, 16777215),
      "deployed constants")
check(divmod(A, c) == (544, 1911), "agreement quotient remainder")
check(divmod(RADIUS, c) == (479, 137), "error quotient remainder")
check(divmod(w, c) == (32, 1911), "prefix quotient remainder")


# Complete independent profile/cap census.
thresholds = [1, 15, 36, 65, Bstar]
counts = dict((value, 0) for value in thresholds)
rows = []
digest = hashlib.sha256()
for u in range(480):
    vmax = 136 if u == 0 else 544
    for v in range(vmax + 1):
        h = u + v + 1
        r = 1911 + c * v
        f = 544 - v
        M = 1023 - u - v
        check(r + c * f == A, "profile agreement")
        check(0 <= f <= M, "profile feasibility")
        if v >= 512:
            check(r >= K, "MDS uniqueness boundary")
            branch = "MDS_FIXED_TEMPLATE_UNIQUENESS"
            kappa = 0
            high_degree = -1
            low_degree = -1
            cap = 1
        else:
            check(r < K, "interleaved boundary")
            kappa = 512 - v
            high_degree = 511 - v
            low_degree = 510 - v
            check(K - r == c * high_degree + 137,
                  "137/1911 component split")
            cap = math.comb(M, kappa) // math.comb(f, kappa)
            branch = "INTERLEAVED_QUOTIENT_PACKING"
        row = (u, v, h, r, f, M, branch, kappa,
               high_degree, low_degree, cap)
        rows.append(row)
        digest.update((",".join(str(x) for x in row) + "\n").encode("ascii"))
        for threshold in thresholds:
            counts[threshold] += Integer(cap <= threshold)

check(len(rows) == 261192, "profile count")
check(counts == {1: 16422, 15: 17763, 36: 18105,
                 65: 18388, Bstar: 25767}, "cap census")
check(sum(Integer(row[1] >= 512) for row in rows) == 15807,
      "v>=512 census")
check(sum(Integer(row[-1] > Bstar) for row in rows) == 235425,
      "above-budget census")
paid = [row for row in rows if row[-1] <= Bstar]
unpaid = [row for row in rows if row[-1] > Bstar]
max_paid = max(row[-1] for row in paid)
min_unpaid = min(row[-1] for row in unpaid)
check(max_paid == 16769604, "maximum paid cap")
check([[row[0], row[1]] for row in paid if row[-1] == max_paid] ==
      [[128, 505], [472, 161]], "maximum paid profiles")
check(min_unpaid == 16808455, "minimum unpaid cap")
check([[row[0], row[1]] for row in unpaid if row[-1] == min_unpaid] ==
      [[224, 504], [471, 257]], "minimum unpaid profiles")
face_cap = next(row[-1] for row in rows if row[0] == 0 and row[1] == 0)
check(len(str(face_cap)) == 255, "face cap digits")


# Free F[phi]-module decomposition and the 136/137 cutoff boundary.
Fsmall = GF(257)
RX = PolynomialRing(Fsmall, names=('X',))
X = RX.gen()
RT = PolynomialRing(Fsmall, names=('T',))
T = RT.gen()
c0 = 5
rho = 2
L = 3
phi = X^5 + 7*X^2 + 11*X + 3


def decompose_in_phi(q):
    components = [RT.zero() for _ in range(c0)]
    remainder = RX(q)
    while remainder != 0:
        degree = remainder.degree()
        residue = degree % c0
        quotient_degree = (degree - residue) // c0
        coefficient = remainder.leading_coefficient()
        components[residue] += coefficient * T^quotient_degree
        remainder -= coefficient * X^residue * phi^quotient_degree
    return components


q_fixture = sum((Fsmall(a + 1) * X^a * phi^L if a < rho
                 else Fsmall(a + 1) * X^a * phi^(L - 1))
                for a in range(c0))
components = decompose_in_phi(q_fixture)
reconstructed = sum(X^a * RX(component(phi))
                    for a, component in enumerate(components))
check(reconstructed == q_fixture, "free-module reconstruction")
check(all(components[a].degree() <= L for a in range(rho)),
      "high component degree")
check(all(components[a].degree() <= L - 1 for a in range(rho, c0)),
      "low component degree")

roots = [Fsmall(1), Fsmall(2), Fsmall(3)]
difference_component = prod(T - root for root in roots)
check(difference_component.degree() == L, "intersection root polynomial")
check(sum(Integer(difference_component(value) == 0) for value in Fsmall) == L,
      "degree-L root bound fixture")


# Reciprocal cofactor bridge, including the exact w+s+1 valuation.
Fjet = GF(1009)
RP = PolynomialRing(Fjet, names=('x',))
x = RP.gen()
PS = PowerSeriesRing(Fjet, names=('z',), default_prec=32)
z = PS.gen()
A0 = 12
K0 = 8
w0 = A0 - K0
s0 = 5
gamma = Fjet(17)
locator = prod(x - Fjet(value) for value in range(1, A0 + 1))
hbar = x^s0 + 3*x^2 + 9
codeword = 5*x^(K0 - 1) + 2*x + 1
center = gamma * locator * hbar + codeword


def reciprocal_series(polynomial, degree):
    return PS(sum(polynomial[i] * z^(degree - i)
                  for i in range(polynomial.degree() + 1)))


Lrev = reciprocal_series(locator, A0)
Hrev = reciprocal_series(hbar, s0)
Yrev = reciprocal_series(center, A0 + s0)
Crev_ambient = PS(sum(codeword[i] * z^(A0 + s0 - i)
                      for i in range(codeword.degree() + 1)))
defect = Lrev * Hrev - gamma^(-1) * Yrev
check(defect == -gamma^(-1) * Crev_ambient, "reciprocal identity")
check(defect.valuation() == w0 + s0 + 1, "exact codeword valuation")
check((defect + O(z^(w0 + s0 + 1))) == 0,
      "reciprocal congruence")
target = gamma^(-1) * Yrev
recovered_h = target / Lrev
recovered_l = target / Hrev
check((recovered_h - Hrev + O(z^(w0 + 1))) == 0,
      "cofactor jet division")
check((recovered_l - Lrev + O(z^(w0 + 1))) == 0,
      "locator jet division")


# Exact 15-target quotient-level construction over GF(p).
Fp = GF(p)
RQ = PolynomialRing(Fp, names=('t',))
t = RQ.gen()
J = list(range(1, 512))
remaining = list(range(512, 1024))
blocks = []
sums = []
for index in range(15):
    anchor = remaining[:32]
    selected = None
    for point in remaining[32:]:
        candidate_sum = (sum(anchor) + point) % p
        if candidate_sum not in sums:
            selected = point
            break
    check(selected is not None, "15-target block choice")
    block = anchor + [selected]
    blocks.append(block)
    sums.append(sum(block) % p)
    block_set = set(block)
    remaining = [point for point in remaining if point not in block_set]
check(len(remaining) == 17, "15-target unused labels")
check(len(set(sums)) == 15, "15-target sums distinct")
block_digest_raw = json.dumps(
    {"blocks": [[int(point) for point in block] for block in blocks],
     "sums": [int(value) for value in sums],
     "unused": [int(point) for point in remaining]},
    sort_keys=True, separators=(",", ":"), ensure_ascii=True,
).encode("ascii") + b"\n"
block_digest = hashlib.sha256(block_digest_raw).hexdigest()

points = [0] + list(range(512, 1024))
values = dict((point, Fp(0)) for point in points)
for i, block in enumerate(blocks):
    for point in block:
        values[point] = Fp(i + 1)
interpolation_data = [(Fp(point), values[point]) for point in points]
G = RQ.lagrange_polynomial(interpolation_data)
check(G.degree() <= 512, "interpolation degree")
check(all(G(Fp(point)) == values[point] for point in points),
      "interpolation values")
VJ = prod(t - Fp(point) for point in J)
Wpoly = VJ * G
check(VJ.degree() == 511 and Wpoly.degree() <= 1023,
      "VJ and W degrees")
targets = []
for i, block in enumerate(blocks):
    scalar = Fp(i + 1)
    qi = scalar * VJ
    difference = Wpoly - qi
    E = J + block
    VE = prod(t - Fp(point) for point in E)
    quotient, remainder_poly = difference.quo_rem(VE)
    check(remainder_poly == 0, "exact quotient factorization")
    check(quotient.degree() <= 479, "quotient cofactor degree")
    zero_set = [point for point in range(1024)
                if difference(Fp(point)) == 0]
    check(zero_set == sorted(E), "exact quotient support")
    targets.append((-sum(Fp(point) for point in E)))
check(len(set(targets)) == 15, "15 distinct quotient targets")
check(1911 + c * 511 == K - 137, "15-target codeword degree")
check(1911 + c * 1023 == n - 137, "15-target center degree")
check(c * 479 == RADIUS - 137, "15-target cofactor degree")


# Varying-template gluing on a complete cubic-fiber RS toy model.
Ftoy = GF(97)
Rt = PolynomialRing(Ftoy, names=('y',))
y = Rt.gen()
D = [value for value in Ftoy if value != 0]
image = sorted(set(value^3 for value in D), key=lambda value: Integer(value))
fibers = dict((label, [value for value in D if value^3 == label])
              for label in image)
check(len(image) == 32, "toy quotient image")
check(all(len(fiber) == 3 for fiber in fibers.values()),
      "toy complete cubic fibers")
beta1, beta2 = image[0], image[1]
rest = image[2:]
Jtoy = rest[:2]
A1 = rest[2:5]
A2 = rest[5:8]
P1 = [fibers[beta1][0]]
P2 = [fibers[beta2][0]]
S1 = set(P1 + sum((fibers[label] for label in Jtoy + A1), []))
S2 = set(P2 + sum((fibers[label] for label in Jtoy + A2), []))
Itoy = S1.intersection(S2)
Ktoy = 7
check(len(S1) == len(S2) == 16, "toy support sizes")
check(len(Itoy) == 6 < Ktoy, "toy intersection gate")
g = prod(y - point for point in Itoy)
check(g.degree() == 6 < Ktoy, "toy gluing codeword")
received = {}
for point in D:
    if point in S1:
        received[point] = Ftoy(0)
    elif point in S2:
        received[point] = g(point)
    else:
        forbidden = {Ftoy(0), g(point)}
        received[point] = next(value for value in Ftoy if value not in forbidden)
agree_zero = {point for point in D if received[point] == 0}
agree_g = {point for point in D if received[point] == g(point)}
check(agree_zero == S1, "toy first exact agreement")
check(agree_g == S2, "toy second exact agreement")
check(P1 != P2, "toy different partial templates")


print("M31 c=2048 fixed-template interleaved quotient Sage replay")
print("profiles=%d cap<=B*=%d cap>B*=%d" %
      (len(rows), counts[Bstar], len(unpaid)))
print("profile00_cap_digits=%d block_digest=%s" %
      (len(str(face_cap)), block_digest))
print("fixed_template_targets=15 varying_template_intersection=135168")
print("checks=%d" % checks)
print("PASS")
