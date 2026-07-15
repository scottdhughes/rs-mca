#!/usr/bin/env python3
"""Exact ``m=2`` rank-two domain/quotient owner classifier.

The classifier deliberately separates five questions that cannot be merged:

1. Is the rank-two affine chart compatible?
2. Do its four unordered pairs determine one separable PGL2 involution?
3. Does that involution preserve the declared RS evaluation domain in uniform
   two-point orbits?
4. Is it the deck involution of a declared power or Chebyshev fold, and do the
   support, both received words, and explaining polynomial descend?
5. Is the resulting quotient cell actually recorded at its natural profile
   term by ``prop:stabilizer-payment``?

Only a chart passing every gate is labelled ``PAID_BY_THEOREM``.  In
particular, a domain-stable rational involution is not silently promoted to a
power/Chebyshev owner.  The finite GF(11), GF(13), and sequential GF(19)
enumerations are exact toy controls for the local ``m=2`` chart only.

Default usage recomputes and checks the frozen certificate.  Use
``--json --include-charts`` to emit the induced PGL2 involution and terminal
owner status for every compatible structural chart.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-rank2-owner-classifier/certificate.json"
)

P19_DOMAIN = (1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10)
P19_PETALS = (tuple(range(4, 8)), tuple(range(8, 12)), tuple(range(12, 16)))
P19_BACKGROUND = tuple(range(16, 18))


def inverse_mod(value: int, p: int) -> int:
    value %= p
    if value == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(value, -1, p)


def rank_mod(rows: list[list[int]], p: int) -> int:
    if not rows:
        return 0
    work = [[entry % p for entry in row] for row in rows]
    rank = 0
    width = len(work[0])
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inverse_mod(work[rank][column], p)
        work[rank] = [entry * scale % p for entry in work[rank]]
        for index in range(len(work)):
            if index == rank or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                (left - scale * right) % p
                for left, right in zip(work[index], work[rank], strict=True)
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def solve3(rows: list[list[int]], rhs: list[int], p: int) -> list[int]:
    work = [row[:] + [value % p] for row, value in zip(rows, rhs, strict=True)]
    for column in range(3):
        pivot = next(index for index in range(column, 3) if work[index][column] % p)
        work[column], work[pivot] = work[pivot], work[column]
        scale = inverse_mod(work[column][column], p)
        work[column] = [entry * scale % p for entry in work[column]]
        for index in range(3):
            if index == column:
                continue
            scale = work[index][column] % p
            work[index] = [
                (left - scale * right) % p
                for left, right in zip(work[index], work[column], strict=True)
            ]
    return [work[index][-1] for index in range(3)]


def residual_matrix(
    p: int,
    background: tuple[int, int],
    pairs: tuple[tuple[int, int], ...],
) -> list[list[int]]:
    points = [point for pair in pairs for point in pair]
    labels = [1, 1, 2, 2, 3, 3]
    rho1, rho2 = background

    def r_value(point: int) -> int:
        return (point - rho1) * (point - rho2) % p

    anchor = [
        [r_value(point) * pow(point, degree, p) % p for degree in range(3)]
        for point in points[:3]
    ]
    output = [[0] * 5 for _ in range(3)]
    for exponent in range(5):
        interpolation = solve3(
            anchor,
            [labels[index] * pow(points[index], exponent, p) % p for index in range(3)],
            p,
        )
        for row, point in enumerate(points[3:]):
            left = sum(
                interpolation[degree]
                * r_value(point)
                * pow(point, degree, p)
                for degree in range(3)
            )
            output[row][exponent] = (
                left - labels[row + 3] * pow(point, exponent, p)
            ) % p
    return output


def normalize_matrix(values: tuple[int, int, int, int], p: int) -> tuple[int, ...]:
    values = tuple(value % p for value in values)
    first = next((value for value in values if value), None)
    if first is None:
        raise ValueError("zero PGL2 matrix")
    scale = inverse_mod(first, p)
    return tuple(value * scale % p for value in values)


def induced_involution(
    p: int, pairs: tuple[tuple[int, int], ...]
) -> dict[str, object]:
    if len(pairs) < 2:
        return {"valid": False, "reason": "NEED_TWO_PAIRS"}
    (x0, y0), (x1, y1) = pairs[:2]
    s0, product0 = (x0 + y0) % p, x0 * y0 % p
    s1, product1 = (x1 + y1) % p, x1 * y1 % p
    a = (product0 - product1) % p
    b = (s0 * product1 - product0 * s1) % p
    c = (s0 - s1) % p
    d = (-a) % p
    determinant = (a * d - b * c) % p
    if determinant == 0:
        return {"valid": False, "reason": "SINGULAR_MATRIX"}
    matrix = normalize_matrix((a, b, c, d), p)

    def image(point: int) -> int | None:
        denominator = (matrix[2] * point + matrix[3]) % p
        if denominator == 0:
            return None
        return (matrix[0] * point + matrix[1]) * inverse_mod(denominator, p) % p

    pair_checks = []
    for pair in pairs:
        left, right = pair
        ok = image(left) == right and image(right) == left
        pair_checks.append({"pair": list(pair), "swapped": ok})
    square = (
        (matrix[0] * matrix[0] + matrix[1] * matrix[2]) % p,
        (matrix[0] * matrix[1] + matrix[1] * matrix[3]) % p,
        (matrix[2] * matrix[0] + matrix[3] * matrix[2]) % p,
        (matrix[2] * matrix[1] + matrix[3] * matrix[3]) % p,
    )
    square_scalar = square[1] == square[2] == 0 and square[0] == square[3] != 0
    valid = all(item["swapped"] for item in pair_checks) and square_scalar
    return {
        "valid": valid,
        "reason": "OK" if valid else "PAIR_OR_INVOLUTION_CHECK_FAILED",
        "matrix_abcd": list(matrix),
        "formula": "(a*x+b)/(c*x+d)",
        "determinant": determinant,
        "trace": (matrix[0] + matrix[3]) % p,
        "square_scalar": square_scalar,
        "pair_checks": pair_checks,
    }


def pgl_image(matrix: list[int], point: int, p: int) -> int | None:
    denominator = (matrix[2] * point + matrix[3]) % p
    if denominator == 0:
        return None
    return (matrix[0] * point + matrix[1]) * inverse_mod(denominator, p) % p


def two_orbits(matrix: list[int], domain: list[int], p: int) -> tuple[list[list[int]], list[int]]:
    domain_set = set(domain)
    poles = [point for point in domain if pgl_image(matrix, point, p) is None]
    if poles:
        return [], poles
    unseen = set(domain)
    orbits: list[list[int]] = []
    while unseen:
        point = min(unseen)
        mate = pgl_image(matrix, point, p)
        if mate not in domain_set:
            return [], []
        orbit = sorted({point, int(mate)})
        orbits.append(orbit)
        unseen.difference_update(orbit)
    return sorted(orbits), []


def is_multiplicative_coset(domain: list[int], p: int) -> bool:
    if not domain or any(point % p == 0 for point in domain):
        return False
    theta = domain[0] % p
    ratios = {point * inverse_mod(theta, p) % p for point in domain}
    if 1 not in ratios or len(ratios) != len(domain):
        return False
    return all((left * right) % p in ratios for left in ratios for right in ratios)


def polynomial_value(coefficients: list[int], point: int, p: int) -> int:
    return sum(
        coefficient * pow(point, degree, p)
        for degree, coefficient in enumerate(coefficients)
    ) % p


def power_quotient(coefficients: list[int], p: int) -> list[int] | None:
    if any(coefficients[index] % p for index in range(1, len(coefficients), 2)):
        return None
    return [coefficients[index] % p for index in range(0, len(coefficients), 2)]


def chebyshev_t2_quotient(coefficients: list[int], p: int) -> list[int] | None:
    even = power_quotient(coefficients, p)
    if even is None:
        return None
    inverse_two = inverse_mod(2, p)
    quotient = [0] * len(even)
    for power, coefficient in enumerate(even):
        scale = coefficient * pow(inverse_two, power, p) % p
        for index in range(power + 1):
            quotient[index] = (
                quotient[index] + scale * comb(power, index)
            ) % p
    return quotient


def terminal(status: str, reason: str, gates: dict[str, object], **extra: object) -> dict[str, object]:
    return {"status": status, "reason": reason, "gates": gates, **extra}


def classify_chart(chart: dict[str, object]) -> dict[str, object]:
    p = int(chart["p"])
    rank_c = int(chart["rankC"])
    rank_augmented = int(chart["rankAug"])
    gates: dict[str, object] = {
        "affine_compatible": rank_augmented == rank_c,
        "rank_two": rank_c == 2,
    }
    if rank_augmented > rank_c:
        return terminal(
            "INCOMPATIBLE_AFFINE_CHART",
            "rank([C|u])>rank(C)",
            gates,
            named_owner=None,
            induced_tau=None,
        )
    if rank_c != 2:
        return terminal(
            "NOT_RANK2_CHART",
            "owner classifier is scoped to compatible rank-two charts",
            gates,
            named_owner=None,
            induced_tau=None,
        )

    background = tuple(int(value) for value in chart["background"])
    support_pairs = tuple(tuple(int(value) for value in pair) for pair in chart["support_pairs"])
    tau = induced_involution(p, (background,) + support_pairs)
    gates["valid_pgl2_involution"] = tau["valid"]
    if not tau["valid"]:
        return terminal(
            "INVALID_PGL2_TEMPLATE",
            str(tau["reason"]),
            gates,
            named_owner=None,
            induced_tau=tau,
        )

    domain_raw = chart.get("domain")
    if domain_raw is None:
        gates["domain_supplied"] = False
        return terminal(
            "NO_RS_DOMAIN_SUPPLIED",
            "a structural pair template does not declare an RS evaluation domain",
            gates,
            named_owner=None,
            induced_tau=tau,
        )
    domain = [int(value) % p for value in domain_raw]
    gates["domain_supplied"] = True
    matrix = tau["matrix_abcd"]
    assert isinstance(matrix, list)
    images = [pgl_image(matrix, point, p) for point in domain]
    domain_invariant = None not in images and set(images) == set(domain)
    gates["tau_preserves_domain"] = domain_invariant
    gates["domain_poles"] = [
        point for point, image in zip(domain, images, strict=True) if image is None
    ]
    if not domain_invariant:
        return terminal(
            "UNPAID_NONINVARIANT",
            "the induced involution does not permute the full evaluation domain",
            gates,
            named_owner=None,
            induced_tau=tau,
        )

    orbits, poles = two_orbits(matrix, domain, p)
    uniform = not poles and len(orbits) * 2 == len(domain) and all(len(orbit) == 2 for orbit in orbits)
    gates["uniform_two_fibres"] = uniform
    gates["orbit_count"] = len(orbits)
    if not uniform:
        return terminal(
            "UNPAID_NONUNIFORM",
            "the declared domain has fixed points or nonuniform involution fibres",
            gates,
            named_owner=None,
            induced_tau=tau,
        )

    negative_matrix = list(normalize_matrix((-1, 0, 0, 1), p))
    tau_is_negation = matrix == negative_matrix
    fold = chart.get("declared_fold")
    if not tau_is_negation:
        gates["declared_power_or_chebyshev_fold"] = False
        return terminal(
            "UNPAID_RATIONAL_INVOLUTION_ONLY",
            "domain-stable PGL2 involution is not a declared power/Chebyshev deck map",
            gates,
            named_owner=None,
            induced_tau=tau,
        )
    if not isinstance(fold, dict):
        gates["declared_power_or_chebyshev_fold"] = False
        return terminal(
            "UNPAID_UNDECLARED_DOMAIN_SYMMETRY",
            "negation symmetry is present but no row fold is declared",
            gates,
            named_owner=None,
            induced_tau=tau,
        )
    fold_kind = fold.get("kind")
    scale_retained = 2 in fold.get("retained_scales", [])
    domain_kind = chart.get("domain_kind")
    chebyshev_geometry_certified = fold.get("geometry_certified") is True
    allowed = (
        fold_kind == "POWER_C2"
        and domain_kind == "multiplicative_coset"
        and is_multiplicative_coset(domain, p)
    ) or (
        fold_kind == "CHEBYSHEV_T2"
        and domain_kind == "chebyshev_twin_coset_x_domain"
        and chebyshev_geometry_certified
    )
    if fold_kind == "POWER_C2":
        fold_values = {point: point * point % p for point in domain}
    elif fold_kind == "CHEBYSHEV_T2":
        fold_values = {point: (2 * point * point - 1) % p for point in domain}
    else:
        fold_values = {}
    fold_fibres = sorted(
        sorted(point for point in domain if fold_values.get(point) == value)
        for value in sorted(set(fold_values.values()))
    )
    fold_matches_orbits = fold_fibres == orbits
    declared_fold_ok = allowed and scale_retained and fold_matches_orbits
    gates["declared_power_or_chebyshev_fold"] = declared_fold_ok
    gates["fold_kind"] = fold_kind
    gates["chebyshev_geometry_certified"] = chebyshev_geometry_certified
    gates["scale_two_retained"] = scale_retained
    gates["fold_fibres_match_tau_orbits"] = fold_matches_orbits
    if not declared_fold_ok:
        return terminal(
            "UNPAID_UNDECLARED_DOMAIN_SYMMETRY",
            "the row declaration does not certify this uniform scale-two fold",
            gates,
            named_owner=None,
            induced_tau=tau,
        )

    support = {int(value) % p for value in chart.get("witness_support", [])}
    support_descends = all((left in support) == (right in support) for left, right in orbits)
    gates["support_descends"] = support_descends
    if not support_descends:
        return terminal(
            "UNPAID_SUPPORT_NONDESCENT",
            "the selected witness support is not a union of complete fold fibres",
            gates,
            named_owner=None,
            induced_tau=tau,
        )

    received_words = chart.get("received_words", [])
    received_descends = isinstance(received_words, list) and len(received_words) == 2
    received_checks = []
    if received_descends:
        for word in received_words:
            values = word.get("values", []) if isinstance(word, dict) else []
            ok = len(values) == len(domain)
            value_map = {
                point: int(value) % p
                for point, value in zip(domain, values, strict=False)
            }
            ok = ok and all(value_map[left] == value_map[right] for left, right in orbits)
            received_checks.append({"name": word.get("name"), "descends": ok})
            received_descends = received_descends and ok
    gates["both_received_words_descend"] = received_descends
    gates["received_word_checks"] = received_checks
    if not received_descends:
        return terminal(
            "UNPAID_DATA_NONDESCENT",
            "both received words must be constant on every fold fibre",
            gates,
            named_owner=None,
            induced_tau=tau,
        )

    coefficients = [int(value) % p for value in chart.get("explaining_polynomial", [])]
    degree = max((index for index, value in enumerate(coefficients) if value), default=-1)
    degree_gate = degree < len(domain) and degree < int(chart.get("K", len(domain)))
    invariant_values = degree_gate and all(
        polynomial_value(coefficients, left, p) == polynomial_value(coefficients, right, p)
        for left, right in orbits
    )
    quotient_coefficients = (
        power_quotient(coefficients, p)
        if fold_kind == "POWER_C2"
        else chebyshev_t2_quotient(coefficients, p)
    )
    explainer_descends = invariant_values and quotient_coefficients is not None
    gates["explainer_degree_lt_K_le_n"] = degree_gate
    gates["explainer_descends"] = explainer_descends
    if not explainer_descends:
        return terminal(
            "UNPAID_EXPLAINER_NONDESCENT",
            "the explaining polynomial does not factor through the declared fold",
            gates,
            named_owner=None,
            induced_tau=tau,
        )

    budget = chart.get("profile_budget")
    budget_ok = (
        isinstance(budget, dict)
        and budget.get("owner") == "prop:stabilizer-payment"
        and budget.get("certified") is True
        and bool(budget.get("natural_descended_prefix_term"))
    )
    gates["quotient_profile_budget_certified"] = budget_ok
    if not budget_ok:
        return terminal(
            "UNPAID_QUOTIENT_BUDGET_MISSING",
            "descent alone is not payment without the natural quotient profile term",
            gates,
            named_owner=None,
            induced_tau=tau,
            quotient_polynomial=quotient_coefficients,
        )
    return terminal(
        "PAID_BY_THEOREM",
        "uniform declared fold and every witness datum descend to a budgeted quotient cell",
        gates,
        named_owner=["prop:quotient-descent", "prop:stabilizer-payment"],
        induced_tau=tau,
        quotient_polynomial=quotient_coefficients,
        quotient_support_size=len(support) // 2,
    )


def compatible_structural_charts(p: int) -> tuple[int, list[dict[str, object]], Counter[str]]:
    total = 0
    compatible: list[dict[str, object]] = []
    rank_partition: Counter[str] = Counter()
    available = list(range(2, p))
    for pair1 in itertools.combinations(available, 2):
        remaining1 = [point for point in available if point not in pair1]
        for pair2 in itertools.combinations(remaining1, 2):
            remaining2 = [point for point in remaining1 if point not in pair2]
            for pair3 in itertools.combinations(remaining2, 2):
                pairs = (pair1, pair2, pair3)
                residual = residual_matrix(p, (0, 1), pairs)
                rank_c = rank_mod([row[:4] for row in residual], p)
                rank_augmented = rank_mod(residual, p)
                total += 1
                rank_partition[f"rankC={rank_c},rankAug={rank_augmented}"] += 1
                if (rank_c, rank_augmented) != (2, 2):
                    continue
                chart = {
                    "p": p,
                    "rankC": rank_c,
                    "rankAug": rank_augmented,
                    "background": [0, 1],
                    "support_pairs": [list(pair) for pair in pairs],
                }
                result = classify_chart(chart)
                compatible.append({
                    "chart_id": f"GF({p}):" + ";".join(f"{x}-{y}" for x, y in pairs),
                    "background": [0, 1],
                    "support_pairs": [list(pair) for pair in pairs],
                    "rankC": rank_c,
                    "rankAug": rank_augmented,
                    **result,
                })
    return total, compatible, rank_partition


def p19_partition() -> dict[str, object]:
    background = tuple(P19_DOMAIN[index] for index in P19_BACKGROUND)
    partition: Counter[str] = Counter()
    compatible: list[dict[str, object]] = []
    for selections in itertools.product(*(itertools.combinations(petal, 2) for petal in P19_PETALS)):
        pairs = tuple(tuple(P19_DOMAIN[index] for index in pair) for pair in selections)
        residual = residual_matrix(19, background, pairs)
        rank_c = rank_mod([row[:4] for row in residual], 19)
        rank_augmented = rank_mod(residual, 19)
        partition[f"rankC={rank_c},rankAug={rank_augmented}"] += 1
        if (rank_c, rank_augmented) == (2, 2):
            compatible.append({"background": list(background), "support_pairs": [list(pair) for pair in pairs]})
    return {
        "p": 19,
        "domain": list(P19_DOMAIN),
        "chart_count": sum(partition.values()),
        "rank_partition": dict(sorted(partition.items())),
        "compatible_rank2_count": len(compatible),
        "compatible_rank2_charts": compatible,
    }


def paid_fixture() -> dict[str, object]:
    p = 13
    domain = list(range(1, p))
    return {
        "p": p,
        "rankC": 2,
        "rankAug": 2,
        "background": [1, 12],
        "support_pairs": [[2, 11], [3, 10], [4, 9]],
        "domain": domain,
        "domain_kind": "multiplicative_coset",
        "declared_fold": {"kind": "POWER_C2", "retained_scales": [2, 3, 4, 6]},
        "witness_support": [1, 12, 2, 11, 3, 10, 4, 9],
        "received_words": [
            {"name": "y0", "values": [point * point % p for point in domain]},
            {"name": "y1", "values": [pow(point, 4, p) for point in domain]},
        ],
        "explaining_polynomial": [1, 0, 2, 0, 1],
        "K": 5,
        "profile_budget": {
            "owner": "prop:stabilizer-payment",
            "certified": True,
            "natural_descended_prefix_term": "fixture scale-2 quotient profile term",
        },
    }


def rational_involution_fixture() -> dict[str, object]:
    domain = [2, 7, 3, 9, 4, 10, 5, 8, 6, 11]
    return {
        "p": 13,
        "rankC": 2,
        "rankAug": 2,
        "background": [2, 7],
        "support_pairs": [[3, 9], [4, 10], [5, 8]],
        "domain": domain,
        "domain_kind": "arbitrary_finite",
        "witness_support": domain,
    }


def mutation_controls() -> dict[str, str]:
    baseline = paid_fixture()
    controls: dict[str, str] = {}

    no_domain = copy.deepcopy(baseline)
    no_domain.pop("domain")
    controls["no_domain"] = classify_chart(no_domain)["status"]

    invalid = copy.deepcopy(baseline)
    invalid["support_pairs"][2][1] = 8
    controls["invalid_template"] = classify_chart(invalid)["status"]

    noninvariant = copy.deepcopy(baseline)
    noninvariant["domain"].remove(12)
    controls["domain_noninvariant"] = classify_chart(noninvariant)["status"]

    undeclared = copy.deepcopy(baseline)
    undeclared.pop("declared_fold")
    controls["fold_undeclared"] = classify_chart(undeclared)["status"]

    support = copy.deepcopy(baseline)
    support["witness_support"].remove(12)
    controls["support_nondescending"] = classify_chart(support)["status"]

    received = copy.deepcopy(baseline)
    received["received_words"][0]["values"][0] += 1
    controls["received_nondescending"] = classify_chart(received)["status"]

    explainer = copy.deepcopy(baseline)
    explainer["explaining_polynomial"][1] = 1
    controls["explainer_nondescending"] = classify_chart(explainer)["status"]

    budget = copy.deepcopy(baseline)
    budget["profile_budget"]["certified"] = False
    controls["budget_missing"] = classify_chart(budget)["status"]

    controls["rational_only"] = classify_chart(rational_involution_fixture())["status"]
    return controls


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_report(*, include_charts: bool) -> dict[str, object]:
    structural_fields = []
    total_compatible = 0
    for p in (11, 13):
        total, charts, rank_partition = compatible_structural_charts(p)
        statuses = Counter(str(chart["status"]) for chart in charts)
        entry: dict[str, object] = {
            "p": p,
            "total_charts": total,
            "rank_partition": dict(sorted(rank_partition.items())),
            "compatible_rank2_count": len(charts),
            "owner_status_counts": dict(sorted(statuses.items())),
            "compatible_chart_sha256": canonical_digest(charts),
        }
        if include_charts:
            entry["compatible_charts"] = charts
        structural_fields.append(entry)
        total_compatible += len(charts)

    paid = classify_chart(paid_fixture())
    mutations = mutation_controls()
    report: dict[str, object] = {
        "schema": "rs-mca-l1-b9-rank2-owner-classifier-v1",
        "status": "EXPERIMENTAL/EXACT_M2_DOMAIN_CLASSIFIER",
        "parameters": {"m": 2, "labels": [1, 2, 3], "fold_scale": 2},
        "theorem_interface": {
            "structural_descent": "prop:quotient-descent",
            "paid_owner": "prop:stabilizer-payment",
            "required_data": [
                "declared RS domain",
                "tau(D)=D with uniform two-point fibres",
                "declared retained power/Chebyshev scale two",
                "support descends",
                "both received words descend",
                "explaining polynomial descends",
                "natural quotient profile term certified",
            ],
        },
        "structural_fields": structural_fields,
        "sequential_p19": p19_partition(),
        "paid_positive_control": paid,
        "mutation_control_statuses": mutations,
        "summary": {
            "compatible_structural_charts_classified": total_compatible,
            "paid_structural_charts_without_declared_domain": 0,
            "p19_compatible_rank2_charts": 0,
            "partition_frozen": True,
        },
        "proof_status": {
            "proved_or_exact": [
                "all enumerated m=2 compatible structural charts emit a canonical PGL2 involution",
                "the classifier never pays a chart without domain, fold, witness-data, and budget gates",
                "the positive power-fold control reaches the named existing owner",
            ],
            "unproved": [
                "that any non-exact frontier rank-two template satisfies these gates",
                "the complete m=2 moving-support add-back against the full profile envelope",
                "any higher-m analogue",
            ],
        },
        "nonclaims": [
            "toy structural charts are not asymptotic evidence",
            "an arbitrary rational involution is not a paid quotient owner",
            "no m>2 statement is tested or asserted",
            "no global mixed-petal theorem is closed",
        ],
    }
    report["transcript_sha256"] = canonical_digest(report)
    return report


def tamper_selftest() -> int:
    expected = {
        "no_domain": "NO_RS_DOMAIN_SUPPLIED",
        "invalid_template": "INVALID_PGL2_TEMPLATE",
        "domain_noninvariant": "UNPAID_NONINVARIANT",
        "fold_undeclared": "UNPAID_UNDECLARED_DOMAIN_SYMMETRY",
        "support_nondescending": "UNPAID_SUPPORT_NONDESCENT",
        "received_nondescending": "UNPAID_DATA_NONDESCENT",
        "explainer_nondescending": "UNPAID_EXPLAINER_NONDESCENT",
        "budget_missing": "UNPAID_QUOTIENT_BUDGET_MISSING",
        "rational_only": "UNPAID_RATIONAL_INVOLUTION_ONLY",
    }
    actual = mutation_controls()
    paid = classify_chart(paid_fixture())["status"] == "PAID_BY_THEOREM"
    for name in sorted(expected):
        print(f"  {name:<25} {actual[name]}")
    if actual != expected or not paid:
        print("TAMPER-SELFTEST: FAIL")
        return 1
    print("TAMPER-SELFTEST: PASS (all owner gates discriminate)")
    return 0


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-charts", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))

    if args.tamper_selftest:
        return tamper_selftest()
    report = build_report(include_charts=args.include_charts)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != report:
        print("RESULT: FAIL (frozen owner-classifier certificate drift)", file=sys.stderr)
        return 1
    fields = report["structural_fields"]
    assert isinstance(fields, list)
    for field in fields:
        print(
            "[PASS] "
            f"GF({field['p']}): compatible_rank2={field['compatible_rank2_count']}, "
            f"statuses={field['owner_status_counts']}, "
            f"digest={field['compatible_chart_sha256'][:16]}..."
        )
    p19 = report["sequential_p19"]
    assert isinstance(p19, dict)
    print(
        "[PASS] GF(19) sequential charts: "
        f"partition={p19['rank_partition']}, compatible_rank2={p19['compatible_rank2_count']}"
    )
    print("RESULT: PASS (exact m=2 rank-two domain/owner partition reproduced)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
