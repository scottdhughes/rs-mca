#!/usr/bin/env sage
"""Independent Sage replay for the M31 canonical-Popov/rank-46 compiler.

The deployed layer is exact integer arithmetic.  The finite-field layer checks
the canonical selector, padding/error factorization, interpolation lattice,
shifted weak-Popov degrees, and Pluecker/gcd divisibility on small controls.
It does not enumerate the deployed M31 code.
"""

from itertools import combinations, product


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


# ---------------------------------------------------------------- deployed
p = 2^31 - 1
n = 2^21
K = 2^20
a = 1116023
w = a - K
radius = n - a
budget = p^4 // 2^100
forbidden = budget + 1
J0 = 614160
s = n - J0
lam = K - 1
low_cap = 3730
high_layers = radius - J0
tail = forbidden - low_cap - 45 * high_layers

check((p, n, K, a, w, radius) ==
      (2147483647, 2097152, 1048576, 1116023, 67447, 981129),
      "deployed constants")
check((budget, forbidden) == (16777215, 16777216), "deployed budget")


def balanced_lower(M, set_size):
    q, r = divmod(M * set_size, n)
    return n * q * (q - 1) // 2 + r * q, q, r


lo3730, q3730, r3730 = balanced_lower(3730, s)
up3730 = binomial(3730, 2) * lam
lo3731, q3731, r3731 = balanced_lower(3731, s)
up3731 = binomial(3731, 2) * lam
check((q3730, r3730, up3730 - lo3730) == (2637, 1370336, 202311),
      "3730 packing row")
check((q3731, r3731, lo3731 - up3731) == (2638, 756176, 19019),
      "3731 packing exclusion")
check((high_layers, tail) == (366969, 259881), "rank-46 tail")
check(low_cap + 45 * high_layers == 16517335, "occupancy base")
check(budget - (low_cap + 45 * high_layers) == 259880, "occupancy safety")

Smax = 2 * radius - K - 1
qS, rS = divmod(Smax, 44)


def ordered_prefix(k):
    return k * qS + max(0, rS - (44 - k))


check((Smax, qS, rS) == (913681, 20765, 21), "Forney division")
check(tuple(ordered_prefix(k) for k in range(1, 5)) ==
      (20765, 41530, 62295, 83060), "ordered Forney bounds")
check(ordered_prefix(3) < K - radius < ordered_prefix(4), "rank-three endpoint")
check(45 - (Smax // (K - radius) + 1) == 31, "low Forney rows")


# ------------------------------------------------ integer convexity control
toy_n, toy_M, toy_s = 6, 4, 3
toy_total = toy_M * toy_s
values = []
for incidences in product(range(toy_M + 1), repeat=toy_n):
    if sum(incidences) == toy_total:
        values.append(sum(binomial(value, 2) for value in incidences))
qtoy, rtoy = divmod(toy_total, toy_n)
balanced_toy = toy_n * binomial(qtoy, 2) + rtoy * qtoy
check(min(values) == balanced_toy == 6, "integer convexity exhaustive toy")


# -------------------------------------------- finite-field canonical Popov
F = GF(11)
R.<X> = PolynomialRing(F)
D = [F(i) for i in range(8)]
toy_K = 4
toy_a = 5
toy_w = toy_a - toy_K
toy_radius = len(D) - toy_a
Lambda = prod(X - x for x in D)

# A deterministic received word with one padded listed codeword.
base = R.zero()
received = [base(x) for x in D]
received[1] += F(3)
received[6] += F(5)
Uhat = R.lagrange_polynomial(list(zip(D, received)))


def wdeg_pivot(row):
    Wp, Np = row
    degW = Wp.degree() if Wp else -10^9
    degN = Np.degree() - (toy_K - 1) if Np else -10^9
    return max(degW, degN), (1 if degN >= degW else 0)


def popov_reduce():
    rows = [[R.one(), Uhat], [R.zero(), Lambda]]
    for _ in range(1000):
        wd0, pv0 = wdeg_pivot(rows[0])
        wd1, pv1 = wdeg_pivot(rows[1])
        if pv0 != pv1:
            break
        i, j = (0, 1) if wd0 <= wd1 else (1, 0)
        wi = wdeg_pivot(rows[i])[0]
        wj = wdeg_pivot(rows[j])[0]
        pivot = pv0
        delta = wj - wi
        coeff = rows[j][pivot].leading_coefficient() / rows[i][pivot].leading_coefficient()
        rows[j] = [rows[j][col] - coeff * X^delta * rows[i][col] for col in range(2)]
    else:
        raise RuntimeError("Popov reduction did not terminate")
    rows.sort(key=lambda row: wdeg_pivot(row)[0])
    return rows


g1, g2 = popov_reduce()
d1, d2 = wdeg_pivot(g1)[0], wdeg_pivot(g2)[0]
det = g1[0] * g2[1] - g1[1] * g2[0]
check(det % Lambda == 0 and (det // Lambda).degree() == 0, "Popov determinant")
check(gcd(g1[0], g2[0]).degree() == 0, "Popov first-coordinate gcd")
check(d1 + d2 == len(D) - toy_K + 1, "Popov degree sum")
check(wdeg_pivot(g1)[1] != wdeg_pivot(g2)[1], "weak Popov pivots")

listed = []
for coeffs in product(F, repeat=toy_K):
    c = sum((coeffs[i] * X^i for i in range(toy_K)), R.zero())
    agreements = tuple(i for i, x in enumerate(D) if c(x) == received[i])
    if len(agreements) >= toy_a:
        listed.append((c, agreements))

check(len(listed) >= 1, "toy list nonempty")
selected_seen = set()
padded = 0
for c, agreements in listed:
    selected = tuple(agreements[:toy_a])
    check(selected not in selected_seen, "canonical selector injective")
    selected_seen.add(selected)
    roots = tuple(i for i in range(len(D)) if i not in selected)
    errors = tuple(i for i in range(len(D)) if i not in agreements)
    padding = tuple(i for i in agreements if i not in selected)
    padded += bool(padding)
    check(set(roots) == set(errors).union(padding), "error-padding roots")
    check(set(errors).isdisjoint(padding), "error-padding disjoint")

    W = prod(X - D[i] for i in roots)
    Npoly = W * c
    check(W.is_monic() and W.degree() == toy_radius, "boundary locator degree")
    check(Lambda % W == 0 and Npoly % W == 0, "split and divisible")
    check(all(W(D[i]) * received[i] == Npoly(D[i]) for i in range(len(D))),
          "lattice membership")

    pivot = selected[-1]
    prefix_errors = tuple(i for i in errors if i < pivot)
    Qh = prod(X - D[i] for i in range(pivot + 1, len(D)))
    Pprefix = prod(X - D[i] for i in prefix_errors)
    check(W == Qh * Pprefix, "complete suffix factorization")
    check(Pprefix.degree() == (pivot + 1) - toy_a, "prefix error degree")
    check(W(D[pivot]) != 0 and c(D[pivot]) == received[pivot], "pivot agreement")

    # Division by the suffix gives the exact prefix interpolation pair.
    Mprefix = Pprefix * c
    check(all(Pprefix(D[i]) * received[i] == Mprefix(D[i])
              for i in range(pivot + 1)), "prefix lattice after suffix division")

    # Unique Popov coordinates, obtained from the determinant identity.
    Anum = W * g2[1] - Npoly * g2[0]
    Bnum = Npoly * g1[0] - W * g1[1]
    check(Anum % det == 0 and Bnum % det == 0, "Popov coordinate divisibility")
    Acoef, Bcoef = Anum // det, Bnum // det
    check(Acoef * g1[0] + Bcoef * g2[0] == W, "Popov W coordinates")
    check(Acoef * g1[1] + Bcoef * g2[1] == Npoly, "Popov N coordinates")
    check(Acoef.degree() <= toy_radius - d1 if Acoef else True, "A degree cap")
    check(Bcoef.degree() <= toy_radius - d2 if Bcoef else True, "B degree cap")

check(padded > 0, "toy exercises an interior padded locator")


# ---------------------------------------- Pluecker/gcd divisibility control
patterns = (
    (0, 1, 2),
    (0, 3, 4),
    (1, 3, 5),
    (2, 4, 5),
    (0, 5, 6),
    (1, 4, 6),
)
locators = [prod(X - F(root) for root in roots) for roots in patterns]
check(gcd(locators).degree() == 0, "primitive locator row")

# Standard five-row syzygy basis P_i e_0-P_0 e_i; retain first three rows.
Hrows = []
for i in range(1, len(locators)):
    row = [R.zero()] * len(locators)
    row[0] = locators[i]
    row[i] = -locators[0]
    Hrows.append(row)
H3 = Matrix(R, Hrows[:3])
check(H3.rank() == 3, "rank-three syzygy control")
for I in combinations(range(len(locators)), 3):
    minor = H3.matrix_from_columns(I).det()
    complement = [locators[k] for k in range(len(locators)) if k not in I]
    G = gcd(complement)
    check(minor == 0 or minor % G == 0, "Pluecker/gcd divisibility")

# Independent column-matroid fixtures for the two exhaustive terminals.
noncoloop = Matrix(F, [[1, 0, 1, 0, 0, 1],
                      [0, 1, 1, 0, 0, 1],
                      [0, 0, 0, 1, 1, 1]])
check(noncoloop.rank() == 3 and noncoloop.matrix_from_columns(range(5)).rank() == 3,
      "noncoloop deletion retains rank three")
coloop = Matrix(F, [[1, 0, 1, 0, 1, 0],
                   [0, 1, 1, 1, 0, 0],
                   [0, 0, 0, 0, 0, 1]])
check(coloop.rank() == 3 and coloop.matrix_from_columns(range(5)).rank() == 2,
      "coloop deletion collapses to rank two")


print("Sage M31 canonical-Popov rank-46 compiler: PASS")
print("deployed packing: cap 3730; first excluded 3731 by margin 19019")
print("forced marked rank-46 keys:", tail)
print("toy list size:", len(listed), "padded rows:", padded,
      "Popov profile:", (d1, d2))
print("rank-three minor cap: 62295 < 67447; aggregate bound does not certify rank four")
print("terminals: UNPAID_PADDING_BRIDGE / UNPAID_COMMON_CORE_ADD_BACK / UNPAID_RANK2_COLOOP")
print("M31 row: OPEN; ledger movement: 0")
