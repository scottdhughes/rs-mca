#!/usr/bin/env sage
"""Independent Sage replay of the full-field rank-two/K-slope control."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/m1-fp2-post-c5-mask-incidence-v1/"
    / "m1_fp2_post_c5_mask_incidence_v1.json"
)

B = GF(7)
F.<a> = GF(7^6)
p = 7

z = F.multiplicative_generator()
assert z.minpoly().degree() == 6
gamma = z^((F.order() - 1) // (p^2 - 1))
assert gamma^(p^2) == gamma
assert gamma^p != gamma

D = [B(0), B(1), B(2), B(3)]
weights = []
for i, x in enumerate(D):
    denominator = B(1)
    for j, y in enumerate(D):
        if i != j:
            denominator *= x - y
    weights.append(F(denominator^(-1)))

H = matrix(
    F,
    3,
    4,
    lambda row, col: weights[col] * F(D[col])^row,
)
assert H.rank() == 3
assert H * vector(F, [1, 1, 1, 1]) == vector(F, [0, 0, 0])

columns = [H.column(index) for index in range(4)]
assert matrix(F, [list(columns[index]) for index in range(3)]).rank() == 3

alpha = z
u = columns[0] + alpha * columns[1]
y1 = columns[2]
y0 = u - gamma * y1
Y = matrix(F, [list(y0), list(y1)]).transpose()
assert Y.rank() == 2

V_E = matrix(F, [list(columns[0]), list(columns[1])]).row_space()
assert u in V_E
assert y1 not in V_E
assert y0 not in V_E
assert y0 + gamma * y1 == u

for e in [1, 2, 3]:
    frobenius_Y = Y.apply_map(lambda value: value^(p^e))
    assert Y.augment(frobenius_Y).rank() > Y.rank()

r0 = H.solve_right(y0)
r1 = H.solve_right(y1)
assert H * r0 == y0
assert H * r1 == y1

H_E = H.matrix_from_columns([0, 1])
error_values = H_E.solve_right(u)
error = vector(F, [error_values[0], error_values[1], 0, 0])
explained_word = r0 + gamma * r1 - error
assert H * explained_word == 0
assert explained_word[2] == explained_word[3]

artifact = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
control = artifact["full_field_control"]
assert control["global_syndrome_rank"] == 2
assert control["gamma_in_parameter_field"] is True
assert control["gamma_in_base_field"] is False
assert control["projective_field_full"] is True
assert control["fixed_support_equation_holds"] is True
assert control["support_noncontained"] is True
assert control["received_pair_realizable"] is True
assert control["survives_deployed_kb_branches_1_to_5_proved"] is False

print("M1_FP2_POST_C5_MASK_INCIDENCE_V1_SAGE_PASS")
print("full projective field, syndrome rank 2, and one K\\B support root coexist")
