#!/usr/bin/env sage
"""Independent Sage replay for the M1 F_(p^2) route-cut toy control."""

from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/m1-fp2-residual-route-cut-v1/"
    / "m1_fp2_residual_route_cut_v1.json"
)

B = GF(7)
R.<X> = PolynomialRing(B)
K.<a> = GF(7^2, modulus=X^2 + 1)
D = [K(value) for value in range(1, 7)]
f = [-a, K(0), K(0), K(0), K(0), K(1)]
g = [K(1), K(0), K(0), K(0), K(0), K(0)]


def explained(word, support):
    rows = [[D[index]^degree for degree in range(3)] for index in support[:3]]
    coefficients = matrix(K, rows).solve_right(vector(K, [word[index] for index in support[:3]]))
    return all(
        sum(coefficients[degree] * D[index]^degree for degree in range(3)) == word[index]
        for index in support
    )


records = []
supports = list(combinations(range(6), 5))
for gamma in K:
    word = [f[index] + gamma * g[index] for index in range(6)]
    for support in supports:
        if explained(word, support) and not (explained(f, support) and explained(g, support)):
            records.append((gamma, support))

assert records == [(a, (0, 1, 2, 3, 4))]
assert a^7 == -a
assert a^7 != a
assert not explained(f, records[0][1])
assert not explained(g, records[0][1])

artifact = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
toy = artifact["toy_control"]
assert toy["exact_census"]["slopes_enumerated"] == 49
assert toy["exact_census"]["bad_records"] == [
    {
        "slope_encoded": [0, 1],
        "support_indices": [0, 1, 2, 3, 4],
        "support_domain_points": [1, 2, 3, 4, 5],
    }
]
assert toy["exact_census"]["a_frobenius_encoded"] == [0, 6]
assert toy["support_checks"]["deployed_first_match_survival_proved"] is False

print("M1_FP2_RESIDUAL_ROUTE_CUT_V1_SAGE_PASS")
print("F_49 bad slopes: [a]; Frobenius(a)=-a is not bad")
