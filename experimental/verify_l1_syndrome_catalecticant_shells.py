#!/usr/bin/env python3
"""Verify tiny L1 syndrome-catalecticant shell identities.

Status: EXPERIMENTAL / AUDIT.

This verifier checks small prime-field instances of the exact identities in
experimental/l1_syndrome_catalecticant_shells.md:

* exact RS list shells;
* primitive maximal-agreement support shells;
* fixed-weight syndrome shells;
* guarded Hankel-divisor shells.

All four objects are compared as canonical atoms:

    (error_support_indices, scaled_error_amplitudes)

where the scaled amplitude at x is v_x e_x and v_x=1/Omega_H'(x).

This is finite audit evidence only. It does not assert a positive worst-case
RS list theorem, MCA theorem, line-decoding theorem, or protocol-safety
consequence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.verify_l1_arbitrary_fiber_repair import (
    eval_poly,
    interpolate_polynomial,
    is_prime,
    multiplicative_domain,
    multiply_by_linear,
    polynomial_degree,
    trim_poly,
)


STATUS = "EXPERIMENTAL / AUDIT"
CLAIM = (
    "finite verifier for syndrome-catalecticant shell identities only; "
    "no positive list-size theorem, MCA theorem, or protocol-safety claim"
)
TEMPLATES = ("zero", "monomial", "random")
DEFAULT_CASES = ("p5-zero", "p5-monomial", "p5-random", "p7-random")
MAX_ERROR_ENUMERATION = 200000

Atom = tuple[tuple[int, ...], tuple[int, ...]]


@dataclass(frozen=True)
class Case:
    name: str
    p: int
    n: int
    k: int
    s: int
    template: str
    seed: int = 0


CASE_PRESETS = {
    "p5-zero": Case("p5-zero", p=5, n=4, k=2, s=3, template="zero"),
    "p5-monomial": Case("p5-monomial", p=5, n=4, k=2, s=3, template="monomial"),
    "p5-random": Case("p5-random", p=5, n=4, k=2, s=3, template="random", seed=1),
    "p7-random": Case("p7-random", p=7, n=6, k=3, s=4, template="random", seed=2),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def current_repo_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def validate_case(case: Case) -> None:
    if not is_prime(case.p):
        raise ValueError("p must be prime")
    if case.n <= 0 or (case.p - 1) % case.n != 0:
        raise ValueError("n must be positive and divide p - 1")
    if not 0 < case.k < case.s <= case.n:
        raise ValueError("case must satisfy 0 < k < s <= n")
    if case.template not in TEMPLATES:
        raise ValueError(f"template must be one of {', '.join(TEMPLATES)}")
    if case.p**case.n > MAX_ERROR_ENUMERATION:
        raise ValueError("case exceeds error-vector enumeration limit")


def received_values(case: Case, domain: list[int]) -> list[int]:
    if case.template == "zero":
        return [0 for _ in domain]
    if case.template == "monomial":
        return [pow(x, case.k, case.p) for x in domain]
    rng = random.Random(case.seed)
    return [rng.randrange(case.p) for _ in domain]


def all_low_degree_polynomials(p: int, k: int) -> list[tuple[int, ...]]:
    return [trim_poly(coeffs) for coeffs in itertools.product(range(p), repeat=k)]


def parity_weights(domain: list[int], p: int) -> list[int]:
    weights: list[int] = []
    for i, x_value in enumerate(domain):
        derivative = 1
        for j, y_value in enumerate(domain):
            if i == j:
                continue
            derivative = (derivative * (x_value - y_value)) % p
        weights.append(pow(derivative, -1, p))
    return weights


def syndrome_moments(
    vector: list[int], domain: list[int], weights: list[int], D: int, p: int
) -> tuple[int, ...]:
    return tuple(
        sum(
            weights[index] * value * pow(domain[index], moment, p)
            for index, value in enumerate(vector)
        )
        % p
        for moment in range(D)
    )


def vector_from_poly(poly: Iterable[int], domain: list[int], p: int) -> list[int]:
    return [eval_poly(poly, x_value, p) for x_value in domain]


def error_vector(values: list[int], codeword: list[int], p: int) -> list[int]:
    return [(value - code) % p for value, code in zip(values, codeword, strict=True)]


def atom_from_error(error: list[int], weights: list[int], p: int) -> Atom:
    support = tuple(index for index, value in enumerate(error) if value % p)
    scaled = tuple((weights[index] * error[index]) % p for index in support)
    return support, scaled


def exact_rs_shell_atoms(
    *,
    p: int,
    k: int,
    j: int,
    domain: list[int],
    weights: list[int],
    values: list[int],
) -> set[Atom]:
    atoms: set[Atom] = set()
    for poly in all_low_degree_polynomials(p, k):
        codeword = vector_from_poly(poly, domain, p)
        error = error_vector(values, codeword, p)
        if sum(1 for value in error if value) == j:
            atoms.add(atom_from_error(error, weights, p))
    return atoms


def primitive_support_shell_atoms(
    *,
    p: int,
    n: int,
    k: int,
    a: int,
    domain: list[int],
    weights: list[int],
    values: list[int],
) -> set[Atom]:
    atoms: set[Atom] = set()
    for agreement_support in itertools.combinations(range(n), a):
        xs = [domain[index] for index in agreement_support]
        ys = [values[index] for index in agreement_support]
        poly = interpolate_polynomial(xs, ys, p)
        if polynomial_degree(poly) >= k:
            continue
        codeword = vector_from_poly(poly, domain, p)
        actual_support = tuple(
            index
            for index, (value, code) in enumerate(zip(values, codeword, strict=True))
            if value == code
        )
        if actual_support != agreement_support:
            continue
        atoms.add(atom_from_error(error_vector(values, codeword, p), weights, p))
    return atoms


def syndrome_weight_shell_atoms(
    *,
    p: int,
    n: int,
    j: int,
    D: int,
    domain: list[int],
    weights: list[int],
    target_syndrome: tuple[int, ...],
) -> set[Atom]:
    atoms: set[Atom] = set()
    for error in itertools.product(range(p), repeat=n):
        error_values = list(error)
        if sum(1 for value in error_values if value) != j:
            continue
        if syndrome_moments(error_values, domain, weights, D, p) == target_syndrome:
            atoms.add(atom_from_error(error_values, weights, p))
    return atoms


def monic_locator_coeffs(roots: list[int], p: int) -> tuple[int, ...]:
    coeffs: tuple[int, ...] = (1,)
    for root in roots:
        coeffs = multiply_by_linear(coeffs, root, p)
    return coeffs


def solve_square(matrix: list[list[int]], rhs: list[int], p: int) -> list[int]:
    size = len(rhs)
    rows = [row[:] + [rhs_value % p] for row, rhs_value in zip(matrix, rhs, strict=True)]
    pivot_row = 0
    for column in range(size):
        pivot = next((r for r in range(pivot_row, size) if rows[r][column] % p), None)
        if pivot is None:
            raise ValueError("singular matrix")
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column] % p, -1, p)
        rows[pivot_row] = [(value * inverse) % p for value in rows[pivot_row]]
        for r in range(size):
            if r == pivot_row:
                continue
            factor = rows[r][column] % p
            if factor:
                rows[r] = [
                    (entry - factor * pivot_entry) % p
                    for entry, pivot_entry in zip(rows[r], rows[pivot_row], strict=True)
                ]
        pivot_row += 1
    return [rows[row][-1] % p for row in range(size)]


def recovered_scaled_amplitudes(
    roots: list[int], syndrome: tuple[int, ...], p: int
) -> list[int]:
    j = len(roots)
    if j == 0:
        return []
    matrix = [[pow(root, moment, p) for root in roots] for moment in range(j)]
    rhs = [syndrome[moment] for moment in range(j)]
    return solve_square(matrix, rhs, p)


def recurrence_passes(
    locator: tuple[int, ...], syndrome: tuple[int, ...], D: int, p: int
) -> bool:
    j = len(locator) - 1
    return all(
        sum(locator[i] * syndrome[row + i] for i in range(j + 1)) % p == 0
        for row in range(D - j)
    )


def guarded_hankel_divisor_atoms(
    *,
    p: int,
    n: int,
    j: int,
    D: int,
    domain: list[int],
    syndrome: tuple[int, ...],
) -> set[Atom]:
    atoms: set[Atom] = set()
    for error_support in itertools.combinations(range(n), j):
        roots = [domain[index] for index in error_support]
        locator = monic_locator_coeffs(roots, p)
        if len(locator) != j + 1 or locator[-1] % p != 1:
            raise AssertionError("locator construction failed")
        if not recurrence_passes(locator, syndrome, D, p):
            continue
        scaled = recovered_scaled_amplitudes(roots, syndrome, p)
        if any(value % p == 0 for value in scaled):
            continue
        atoms.add((tuple(error_support), tuple(value % p for value in scaled)))
    return atoms


def subgroup_weight_formula_holds(domain: list[int], weights: list[int], p: int) -> bool:
    n = len(domain)
    inv_n = pow(n % p, -1, p)
    return all(weight == (x_value * inv_n) % p for x_value, weight in zip(domain, weights))


def verify_case(case: Case) -> dict[str, Any]:
    validate_case(case)
    domain = multiplicative_domain(case.p, case.n)
    weights = parity_weights(domain, case.p)
    values = received_values(case, domain)
    D = case.n - case.k
    target_syndrome = syndrome_moments(values, domain, weights, D, case.p)
    shell_results: dict[str, Any] = {}

    for a in range(case.s, case.n + 1):
        j = case.n - a
        exact_atoms = exact_rs_shell_atoms(
            p=case.p,
            k=case.k,
            j=j,
            domain=domain,
            weights=weights,
            values=values,
        )
        primitive_atoms = primitive_support_shell_atoms(
            p=case.p,
            n=case.n,
            k=case.k,
            a=a,
            domain=domain,
            weights=weights,
            values=values,
        )
        syndrome_atoms = syndrome_weight_shell_atoms(
            p=case.p,
            n=case.n,
            j=j,
            D=D,
            domain=domain,
            weights=weights,
            target_syndrome=target_syndrome,
        )
        hankel_atoms = guarded_hankel_divisor_atoms(
            p=case.p,
            n=case.n,
            j=j,
            D=D,
            domain=domain,
            syndrome=target_syndrome,
        )
        shell_results[str(a)] = {
            "a": a,
            "j": j,
            "tau": D - j,
            "exact_rs_shell_count": len(exact_atoms),
            "primitive_support_shell_count": len(primitive_atoms),
            "syndrome_weight_shell_count": len(syndrome_atoms),
            "guarded_hankel_divisor_shell_count": len(hankel_atoms),
            "all_sets_equal": (
                exact_atoms == primitive_atoms == syndrome_atoms == hankel_atoms
            ),
            "atoms": [
                {"support": list(support), "scaled_amplitudes": list(scaled)}
                for support, scaled in sorted(exact_atoms)
            ],
        }

    zero_syndrome = all(value == 0 for value in target_syndrome)
    zero_guard_check = None
    if zero_syndrome:
        zero_guard_check = all(
            shell_results[str(a)]["guarded_hankel_divisor_shell_count"] == 0
            for a in range(case.s, case.n)
        ) and shell_results[str(case.n)]["guarded_hankel_divisor_shell_count"] == 1

    checks = {
        "subgroup_weight_formula": subgroup_weight_formula_holds(
            domain, weights, case.p
        ),
        "all_shell_objects_match": all(
            row["all_sets_equal"] for row in shell_results.values()
        ),
        "zero_syndrome_guard": zero_guard_check,
    }
    required = [value for value in checks.values() if isinstance(value, bool)]
    return {
        "case": {
            "name": case.name,
            "p": case.p,
            "n": case.n,
            "k": case.k,
            "s": case.s,
            "template": case.template,
            "seed": case.seed,
        },
        "domain": domain,
        "weights": weights,
        "syndrome": list(target_syndrome),
        "shells": shell_results,
        "checks": checks,
        "all_passed": all(required),
    }


def build_report(cases: list[Case]) -> dict[str, Any]:
    results = [verify_case(case) for case in cases]
    return {
        "schema_version": "l1-syndrome-catalecticant-shells-verifier-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "provenance": {
            "generator": "experimental/verify_l1_syndrome_catalecticant_shells.py",
            "created_at_utc": utc_now(),
            "repo_commit": current_repo_commit(),
        },
        "summary": {
            "cases": len(results),
            "all_passed": all(result["all_passed"] for result in results),
        },
        "results": results,
    }


def parse_cases(values: list[str] | None) -> list[Case]:
    requested = values or list(DEFAULT_CASES)
    return [CASE_PRESETS[value] for value in requested]


def print_text_report(report: dict[str, Any]) -> None:
    print("L1 syndrome catalecticant shell verifier")
    print(f"Status: {report['status']}")
    print(f"Cases: {report['summary']['cases']}")
    print(f"All passed: {report['summary']['all_passed']}")
    for result in report["results"]:
        case = result["case"]
        shell_bits = ", ".join(
            "a={a}: exact={exact_rs_shell_count} hankel={guarded_hankel_divisor_shell_count} passed={all_sets_equal}".format(
                **row
            )
            for row in result["shells"].values()
        )
        print(
            "case={name} p={p} n={n} k={k} s={s} template={template}: {shells} all={passed}".format(
                **case,
                shells=shell_bits,
                passed=result["all_passed"],
            )
        )
    print(f"claim: {report['claim']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        choices=sorted(CASE_PRESETS),
        help="case preset to run; defaults to all verifier presets",
    )
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    report = build_report(parse_cases(args.case))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text_report(report)
    return 0 if report["summary"]["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
