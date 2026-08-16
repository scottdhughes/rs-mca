#!/usr/bin/env python3
"""Independent audit for the KoalaBear source-bound shortening adapter."""

from itertools import product

N, K, M = 2_097_152, 1_048_576, 1_116_048
LOADS = [
    2_843_853_816_476_423, 93_708_171_878_891, 3_087_708_134_499,
    101_738_094_101, 3_352_119_806, 110_444_488, 3_638_792,
    119_884, 3_950, 131,
]
DIMS = [8, 7, 6, 5, 3, 2, 2, 2, 2, 2]

rows = []
for k in range(1, 11):
    triple = (N-k, K-k, M-k)
    assert triple[0]-triple[1] == 1_048_576
    assert triple[2]-triple[1] == 67_472
    assert triple[0]-triple[2] == 981_104
    rows.append((k, *triple, LOADS[k-1], DIMS[k-1]))

# Independent GF(5) replacement barrier.
p = 5
r1 = [0, 0, 1, 0]
def matches(points):
    return any(all((a+b*x) % p == r1[x] for x in points)
               for a,b in product(range(p), repeat=2))
assert not matches([0,1,2])
assert matches([0,1,3])
assert not matches([0,1,2,3])

# Independent shortening lift check at T={3}: K'=1 codewords are constants.
shortened = [(r1[x] * pow((x-3) % p, -1, p)) % p for x in [0,1,2]]
assert len(set(shortened)) > 1

# Count all quadratics over GF(5) with f(0)=2, f(1)=4.
constrained = []
for a,b,c in product(range(p), repeat=3):
    if a == 2 and (a+b+c) % p == 4:
        constrained.append((a,b,c))
assert len(constrained) == 5
# They are exactly 2+2X+q X(X-1).
expected = sorted((2, (2-q) % p, q) for q in range(p))
assert sorted(constrained) == expected

print("KB_MCA_RANK11_SOURCE_SHORTENING_AUDIT_PASS")
print(f"rows={len(rows)}")
print(f"load1={rows[0][-2]}")
print(f"last_row={rows[-1]}")
print(f"shortened_values={shortened}")
