#!/usr/bin/env sage
"""Independent Sage replay for the M31 rho=9 architecture wall."""

from itertools import combinations


p = 2^31 - 1
N = 2^21
m = 981129
w = 67447
d0 = N - w
L = 2^24
t = 276415
R = m * (N - m)
a = 9
q = ceil(L / a)
v = a + q
r = v - 1

rho = QQ(N * t) / (2 * N * t - R)
rho_proved = QQ(N * 276416) / (2 * N * 276416 - R)
z2 = QQ(a * q) / v
h2 = QQ(2 * N * t - R) / (N * t)

assert q == 1864136
assert a * q - L == 8
assert v == 1864145
assert r == 1864144
assert d0 - r == 165561
assert 2 * N * t - R == 64406010193
assert rho == QQ(579684270080) / 64406010193
assert z2 == QQ(16777224) / 1864145
assert z2 < 9 < rho
assert rho - z2 == QQ(61473694037368) / 120062141871229985
assert rho_proved == QQ(579686367232) / 64410204497
assert z2 - rho_proved == QQ(4985688279688) / 120069960662060065
assert rho_proved < z2 < 9 < rho
assert h2 * rho == 1
assert h2 * z2 < 1
assert t * h2 == 2 * t - QQ(R) / N
assert v < p and v % p != 0

# A small, fully materialized analog checks the root/dual-vector identities
# independently of the large arithmetic formulas.
aa, bb = 3, 5
vv = aa + bb
V = VectorSpace(QQ, vv)
roots = []
for i in range(aa):
    for j in range(bb):
        e = vector(QQ, [0] * vv)
        e[i] = 1
        e[aa + j] = -1
        roots.append(e)
z = vector(QQ, [QQ(bb) / vv] * aa + [QQ(-aa) / vv] * bb)
assert sum(z) == 0
assert all(alpha * alpha == 2 for alpha in roots)
assert all(alpha * z == 1 for alpha in roots)
assert set(roots[i] * roots[j] for i, j in combinations(range(len(roots)), 2)) == {0, 1}
G = matrix(QQ, [[x * y for y in roots] for x in roots])
assert G.rank() == vv - 1
Gp = G.change_ring(GF(101))
assert Gp.rank() == vv - 1

# Binary rectangle application to the complete K_{9,q-1} subrectangle.
b = q - 1
required_N = 2 * t + b - 1
assert 9 * b == L - 1
assert required_N == 2416964
assert required_N - N == 319812
assert required_N > N

# Exact integer jump: part size eight cannot carry L roots under rank d0,
# while part size nine can.
assert 8 * (d0 + 1 - 8) == 16237584 < L
assert 9 * q == L + 8

print("M31 rho=9 independent Sage replay: PASS")
print("abstract ADE witness feasible; canonical binary rectangle impossible")
print("row closure: false; ledger movement: 0")
