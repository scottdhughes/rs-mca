#!/usr/bin/env sage
"""Independent Sage replay for the fixed-line sextic MCA counterexample."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/frontier-extension-fixed-line-audit-v1/"
      "frontier_extension_fixed_line_audit_v1.json"
)

p = 7
R = PolynomialRing(GF(p), names=("x",))
x = R.gen()
modulus = x^6 + 2
assert modulus.is_irreducible()
F = GF(p^6, names=("a",), modulus=modulus)
a = F.gen()

D = [1, 2, 3, 4, 5, 6]
k = 3
A = 5
f = [-a, F(0), F(0), F(0), F(0), F(1)]
g = [F(1), F(0), F(0), F(0), F(0), F(0)]


def interpolation_weights(source_indices, target_index):
    target = GF(p)(D[target_index])
    weights = []
    for source_index in source_indices:
        source = GF(p)(D[source_index])
        numerator = GF(p)(1)
        denominator = GF(p)(1)
        for other_index in source_indices:
            if other_index == source_index:
                continue
            other = GF(p)(D[other_index])
            numerator *= target - other
            denominator *= source - other
        weights.append(numerator / denominator)
    return weights


def support_is_rs_codeword(values, support):
    sources = list(support[:k])
    for target_index in support[k:]:
        predicted = sum(
            F(weight) * values[source_index]
            for source_index, weight in zip(
                sources, interpolation_weights(sources, target_index)
            )
        )
        if predicted != values[target_index]:
            return False
    return True


def agreeing_supports(values, agreement):
    return [
        list(support)
        for support in Subsets(range(len(D)), agreement)
        if support_is_rs_codeword(values, list(support))
    ]


def max_rs_agreement(values):
    for agreement in range(len(D), k - 1, -1):
        supports = agreeing_supports(values, agreement)
        if supports:
            return agreement, supports
    raise AssertionError("no RS interpolation support")


bad = []
bad_records = []
for z in F:
    values = [f[i] + z * g[i] for i in range(len(D))]
    supports = agreeing_supports(values, A)
    if supports:
        agreement, maximal_supports = max_rs_agreement(values)
        bad.append(z)
        bad_records.append((z, agreement, supports, maximal_supports, values))

assert bad == [a]
assert a.minpoly().degree() == 6
assert a^p not in bad
assert len(bad) % 6 != 0
assert bad_records[0][1] == A < len(D)
assert bad_records[0][2] == [[0, 1, 2, 3, 4]]
assert bad_records[0][3] == [[0, 1, 2, 3, 4]]
assert not support_is_rs_codeword(f, bad_records[0][2][0])
assert not support_is_rs_codeword(g, bad_records[0][2][0])
assert all(value != 0 for value in D)
assert set(D) == set(GF(p)) - {GF(p)(0)}
assert not any(
    all(value in GF(p) for value in [scalar * entry for entry in f + g])
    for scalar in GF(p)
    if scalar != 0
)

packet = json.loads(CERT.read_text(encoding="utf-8"))
counterexample = packet["fixed_line_counterexample"]
assert counterexample["field"]["modulus_coefficients_low_to_high"] == [2, 0, 0, 0, 0, 0, 1]
assert counterexample["code"]["slack_t"] == A - k == 2
assert counterexample["code"]["domain_in_base_field"] == D
assert counterexample["received_line"]["pair_descends_to_base_after_common_nonzero_scaling"] is False
assert counterexample["exact_census"]["bad_slope_set_encoded"] == [7]
assert counterexample["exact_census"]["full_degree_bad_slope_count"] == 1
assert counterexample["exact_census"]["full_degree_count_divisible_by_six"] is False
assert counterexample["exact_census"]["bad_set_frobenius_stable"] is False
assert counterexample["local_support_checks_for_the_unique_bad_slope"]["support_indices"] == [0, 1, 2, 3, 4]
assert counterexample["local_support_checks_for_the_unique_bad_slope"]["support_domain_points"] == [1, 2, 3, 4, 5]

budget = packet["koalabear_budget_audit"]
p_kb = budget["row"]["p"]
B_rem = int(budget["baseline"]["B_rem"])
assert B_rem // p_kb == 129056129
assert p_kb^2 > B_rem
assert budget["K_rem_qfin"]["is_direct_extension_degree_ceiling"] is False

print("SAGE CHECK: PASS")
print("bad slopes = [a]")
print("a^7 is bad =", a^7 in bad)
print("full-degree bad count = 1 (not divisible by 6)")
print("t =", A - k)
print("conditional e_Y=1 Delta cap =", B_rem // p_kb)
