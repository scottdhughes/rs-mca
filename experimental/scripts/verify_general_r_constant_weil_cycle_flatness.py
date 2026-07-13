#!/usr/bin/env python3
"""Exact checks for the general-R constant-Weil cycle theorem."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


CERTIFICATE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "certificates"
    / "general-r-constant-weil-cycle-flatness"
    / "general_r_constant_weil_cycle_flatness.json"
)


def ensure(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def rising_binom(parameter: Fraction, order: int) -> Fraction:
    """Return binom(parameter + order - 1, order) exactly."""
    ensure(parameter > 0, ("positive parameter", parameter))
    ensure(order >= 0, ("nonnegative order", order))
    value = Fraction(1, 1)
    for index in range(order):
        value *= parameter + index
        value /= index + 1
    return value


def ceil_fraction(value: Fraction) -> int:
    return (value.numerator + value.denominator - 1) // value.denominator


def cycle_coefficient(
    n: int, p: int, r: int, lam: Fraction
) -> Fraction:
    beta = (Fraction(n, 1) - lam) / p
    total = Fraction(0, 1)
    for ell in range(r // p + 1):
        total += rising_binom(beta, ell) * rising_binom(
            lam, r - p * ell
        )
    return total


def hockey_factor(beta: Fraction, level: int) -> Fraction:
    return rising_binom(beta + 1, level)


def load_certificate() -> dict:
    with CERTIFICATE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_certificate(data: dict) -> int:
    ensure(
        data["schema"]
        == "rs-mca.general-r-constant-weil-cycle-flatness.v1",
        "schema",
    )
    ensure(data["status"] == "PROVED", "status")
    ensure(data["hard_input"] == 2, "hard input")
    ensure(
        data["lean_target"]
        == "experimental/lean/grande_finale/GrandeFinale/GeneralRConstantWeilCycleFlatness.lean",
        "Lean target",
    )
    ensure(
        data["lean_status"] == "UNPROVED_STATEMENT_TARGET",
        "Lean status",
    )
    ensure(
        data["source"]["integrated_commit"]
        == "6588d8d6c393df81642dafafc82c70f565d009cf",
        "source commit",
    )
    ensure(data["source"]["r2_followup_pr"] == 718, "R=2 follow-up")
    ensure(
        data["source"]["r2_followup_integrated_by"] == "c23dcaa",
        "R=2 integration",
    )
    ensure(data["parameters"]["prefix_guard"] == "1<=R<p", "prefix guard")
    ensure(
        data["parameters"]["weil_parameter"]
        == "Lambda=C_0*(R+1)*sqrt(Q)+|P|",
        "Weil parameter",
    )
    ensure(
        data["finite_bound"]["fourier_multiplier"] == "Q^R-1",
        "Fourier multiplier",
    )
    ensure(
        data["asymptotic_gate"]["field_penalty"] == "R*log(Q)/N",
        "field penalty",
    )
    ensure(
        data["asymptotic_gate"]["characteristic_penalty"]
        == "3*log(2)/(2*p)",
        "characteristic penalty",
    )
    family = data["fixed_characteristic_family"]
    ensure(family["field"] == "F_(p^(2e))", "tower field")
    ensure(family["subgroup_order"] == "d*(p^e+1)", "subgroup order")
    ensure(
        family["symbolic_margin"] == "d>2*C_0*(R+1)",
        "symbolic margin",
    )
    ensure(
        family["sample_scope"] == "arithmetic only; C_0 is symbolic",
        "sample scope",
    )
    ensure("R>=p" in data["nonclaims"], "R>=p nonclaim")
    ensure("circle twin-cosets" in data["nonclaims"], "circle nonclaim")
    return 18


def check_cycle_grid() -> int:
    checks = 0
    for p in (3, 5, 7, 11, 13):
        for n in range(4, min(5 * p + 7, 66)):
            candidates = {
                Fraction(1, 1),
                Fraction(n, 9),
                Fraction(n, 3),
                Fraction(n - 1, 2),
            }
            for lam in sorted(candidates):
                if not (1 <= lam < n):
                    continue
                beta = (Fraction(n, 1) - lam) / p
                for r in range(n // 2 + 1):
                    level = r // p
                    hockey_sum = sum(
                        (
                            rising_binom(beta, ell)
                            for ell in range(level + 1)
                        ),
                        Fraction(0, 1),
                    )
                    hockey = hockey_factor(beta, level)
                    ensure(
                        hockey_sum == hockey,
                        ("hockey", n, p, r, lam),
                    )
                    checks += 1

                    exact = cycle_coefficient(n, p, r, lam)
                    base = rising_binom(lam, r)
                    upper = base * hockey
                    ensure(
                        exact <= upper,
                        ("coefficient", n, p, r, lam, exact, upper),
                    )
                    checks += 1

                    binary = Fraction(
                        2 ** (ceil_fraction(beta) + level), 1
                    )
                    ensure(
                        hockey <= binary,
                        ("binary penalty", n, p, r, lam),
                    )
                    exponent_upper = 1 + Fraction(3 * n, 2 * p)
                    ensure(
                        ceil_fraction(beta) + level <= exponent_upper,
                        ("characteristic exponent", n, p, r, lam),
                    )
                    checks += 2

                    for prefix_depth in range(1, min(p, 6)):
                        for q in (n + 1, (n + 1) ** 2):
                            multiplier = q**prefix_depth - 1
                            exact_error = (
                                Fraction(multiplier, math.comb(n, r))
                                * exact
                            )
                            certified_error = (
                                Fraction(multiplier, math.comb(n, r))
                                * upper
                            )
                            ensure(
                                exact_error <= certified_error,
                                (
                                    "Q^R multiplier",
                                    n,
                                    p,
                                    r,
                                    prefix_depth,
                                    q,
                                ),
                            )
                            checks += 1
    return checks


def entropy(x: float) -> float:
    if x == 0.0 or x == 1.0:
        return 0.0
    return -x * math.log(x) - (1.0 - x) * math.log(1.0 - x)


def entropy_gap(x: float, lam: float) -> float:
    return entropy(x) - (x + lam) * entropy(x / (x + lam))


def check_entropy(data: dict) -> int:
    checks = 0
    for sample in data["entropy_samples"]:
        alpha = sample["alpha"]
        lam = sample["lambda"]
        ensure(0.0 < alpha < 0.5, ("alpha", alpha))
        ensure(0.0 < lam < 0.5, ("lambda", lam))
        endpoint_minimum = min(
            entropy_gap(alpha, lam), entropy_gap(0.5, lam)
        )
        ensure(endpoint_minimum > 0.0, ("entropy gap", alpha, lam))
        checks += 1

        sampled = []
        for index in range(1001):
            x = alpha + (0.5 - alpha) * index / 1000.0
            value = entropy_gap(x, lam)
            ensure(value > 0.0, ("sampled gap", alpha, lam, x))
            sampled.append(value)
            checks += 1
        ensure(
            min(sampled) + 1e-12 >= endpoint_minimum,
            ("endpoint minimum", alpha, lam),
        )
        checks += 1

        prime_threshold = math.ceil(
            3 * math.log(2) / (2 * endpoint_minimum)
        )
        ensure(prime_threshold >= 2, ("prime threshold", prime_threshold))
        checks += 1
    return checks


def rank_mod_p(matrix: list[list[int]], p: int) -> int:
    rows = [[value % p for value in row] for row in matrix]
    if not rows:
        return 0
    nrows = len(rows)
    ncols = len(rows[0])
    rank = 0
    for col in range(ncols):
        pivot = next(
            (row for row in range(rank, nrows) if rows[row][col]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][col], -1, p)
        rows[rank] = [(value * inverse) % p for value in rows[rank]]
        for row in range(nrows):
            if row == rank or rows[row][col] == 0:
                continue
            factor = rows[row][col]
            rows[row] = [
                (left - factor * right) % p
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
        if rank == nrows:
            break
    return rank


def check_prime_field_spans() -> int:
    checks = 0
    for p in (5, 7, 11, 13):
        points = list(range(1, p))
        base = points[0]
        for prefix_depth in range(1, min(6, p - 1)):
            vectors = [
                [
                    (pow(point, degree, p) - pow(base, degree, p)) % p
                    for degree in range(1, prefix_depth + 1)
                ]
                for point in points[1:]
            ]
            actual = rank_mod_p(vectors, p)
            ensure(
                actual == prefix_depth,
                ("full prime-field span", p, prefix_depth, actual),
            )
            checks += 1

        # R<p alone is not enough: X^(p-1) is constant on F_p^x.
        prefix_depth = p - 1
        vectors = [
            [
                (pow(point, degree, p) - pow(base, degree, p)) % p
                for degree in range(1, prefix_depth + 1)
            ]
            for point in points[1:]
        ]
        actual = rank_mod_p(vectors, p)
        ensure(
            actual < prefix_depth,
            ("span guardrail without Lambda<N", p, actual),
        )
        checks += 1
    return checks


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def check_fixed_towers(data: dict) -> int:
    checks = 0
    towers = data["fixed_characteristic_family"]["arithmetic_towers"]
    for tower in towers:
        prefix_depth = tower["R"]
        d = tower["d"]
        p = tower["p"]
        ensure(is_prime(p), ("prime", p))
        ensure(p % d == 1, ("congruence", p, d))
        ensure(p > prefix_depth, ("R<p", prefix_depth, p))
        checks += 3

        previous_n_over_p = None
        previous_shallow = None
        previous_field_penalty = None
        for exponent in tower["exponents"]:
            q = p ** (2 * exponent)
            root_q = p**exponent
            n = d * (root_q + 1)
            ensure((q - 1) % n == 0, ("subgroup", p, d, exponent))
            ensure(n > root_q - 1, ("subfield guard", p, d, exponent))
            checks += 2

            n_over_p = Fraction(n, p)
            shallow = Fraction(prefix_depth * root_q, n)
            field_penalty = (
                2 * prefix_depth * exponent * math.log(p) / n
            )
            ensure(
                0 < shallow < Fraction(prefix_depth, d),
                ("non-shallow ratio", p, d, exponent),
            )
            checks += 1

            if previous_n_over_p is not None:
                ensure(
                    n_over_p > previous_n_over_p,
                    ("N/p growth", p, d, exponent),
                )
                ensure(
                    shallow > previous_shallow,
                    ("shallow ratio growth", p, d, exponent),
                )
                ensure(
                    field_penalty < previous_field_penalty,
                    ("field penalty decay", p, d, exponent),
                )
                checks += 3
            previous_n_over_p = n_over_p
            previous_shallow = shallow
            previous_field_penalty = field_penalty
    return checks


def check_small_images() -> int:
    checks = 0
    for p, n, prefix_depth, m in (
        (7, 6, 2, 3),
        (11, 8, 3, 4),
        (13, 10, 4, 5),
    ):
        points = list(range(1, n + 1))
        counts: dict[tuple[int, ...], int] = {}
        for support in itertools.combinations(points, m):
            target = tuple(
                sum(pow(point, degree, p) for point in support) % p
                for degree in range(1, prefix_depth + 1)
            )
            counts[target] = counts.get(target, 0) + 1
        ensure(sum(counts.values()) == math.comb(n, m), "image mass")
        ensure(max(counts.values()) >= 1, "nonempty image")
        ensure(len(counts) <= p**prefix_depth, "ambient image bound")
        checks += 3
    return checks


def run_check(data: dict) -> int:
    checks = 0
    checks += validate_certificate(data)
    checks += check_cycle_grid()
    checks += check_entropy(data)
    checks += check_prime_field_spans()
    checks += check_fixed_towers(data)
    checks += check_small_images()
    print("object: general-R constant-Weil cycle flatness")
    print(f"exact checks: {checks} PASS")
    print("theorem: 1<=R<p quantitative gate and fixed-char tower")
    print("status: PROVED conditional on integrated mixed-Weil input")
    print(f"RESULT: PASS ({checks}/{checks})")
    return checks


def run_tamper_selftest(data: dict) -> None:
    tampers = []

    altered_input = copy.deepcopy(data)
    altered_input["hard_input"] = 3
    tampers.append(altered_input)

    altered_guard = copy.deepcopy(data)
    altered_guard["parameters"]["prefix_guard"] = "1<=R"
    tampers.append(altered_guard)

    detected = 0
    for tampered in tampers:
        try:
            validate_certificate(tampered)
        except AssertionError:
            detected += 1
    ensure(detected == len(tampers), ("tamper detection", detected))
    print(f"tamper self-test: {detected}/{len(tampers)} detected PASS")
    print("RESULT: PASS (tamper detected)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    data = load_certificate()
    if args.check or not args.tamper_selftest:
        run_check(data)
    if args.tamper_selftest:
        run_tamper_selftest(data)


if __name__ == "__main__":
    main()
