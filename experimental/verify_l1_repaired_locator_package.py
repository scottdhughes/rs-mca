#!/usr/bin/env python3
"""Verify finite identities from the L1 repaired locator theorem package.

Status: EXPERIMENTAL / AUDIT.

This script checks tiny prime-field instances of the exact identities in
experimental/l1_repaired_locator_theorem_package.md:

* image fibers match the cumulative repaired list object;
* raw support fibers are binomial moments of exact agreement shells;
* binomial inversion recovers the exact agreement shell counts;
* adding a degree-<k polynomial preserves all shell and raw moment counts;
* primitive exact shells match syndrome weight shells in exhaustive tiny cases.

It does not assert a positive worst-case RS list-size theorem, MCA theorem,
line-decoding theorem, or protocol-safety consequence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
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
    polynomial_degree,
    trim_poly,
)


STATUS = "EXPERIMENTAL / AUDIT"
CLAIM = (
    "finite verifier for repaired locator identities only; "
    "no positive list-size theorem, MCA theorem, or protocol-safety claim"
)
SYNDROME_ENUM_LIMIT = 10000


@dataclass(frozen=True)
class Case:
    name: str
    p: int
    n: int
    k: int
    s: int
    template: str
    seed: int = 0
    exhaustive: bool = False
    syndrome: bool = False


DEFAULT_CASES = (
    "p5-zero",
    "p5-monomial",
    "p5-random",
    "p17-zero",
    "p17-monomial",
    "p17-random",
)


CASE_PRESETS = {
    "p5-zero": Case("p5-zero", 5, 4, 2, 3, "zero", exhaustive=True, syndrome=True),
    "p5-monomial": Case(
        "p5-monomial", 5, 4, 2, 3, "monomial", exhaustive=True, syndrome=True
    ),
    "p5-random": Case(
        "p5-random", 5, 4, 2, 3, "random", seed=1, exhaustive=True, syndrome=True
    ),
    "p17-zero": Case("p17-zero", 17, 16, 8, 9, "zero"),
    "p17-monomial": Case("p17-monomial", 17, 16, 8, 9, "monomial"),
    "p17-random": Case("p17-random", 17, 16, 8, 9, "random", seed=0),
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
    if case.template not in {"zero", "monomial", "random"}:
        raise ValueError("template must be zero, monomial, or random")


def received_values(case: Case, domain: list[int]) -> list[int]:
    if case.template == "zero":
        return [0 for _ in domain]
    if case.template == "monomial":
        return [pow(x, case.k, case.p) for x in domain]
    rng = random.Random(case.seed)
    return [rng.randrange(case.p) for _ in domain]


def all_low_degree_polynomials(p: int, k: int) -> list[tuple[int, ...]]:
    return [trim_poly(coeffs) for coeffs in itertools.product(range(p), repeat=k)]


def support_images(
    *,
    p: int,
    n: int,
    k: int,
    domain: list[int],
    values: list[int],
) -> tuple[dict[int, int], dict[int, set[tuple[int, ...]]], dict[str, int]]:
    raw_moments: dict[int, int] = {}
    image_by_t: dict[int, set[tuple[int, ...]]] = {}
    supports_checked: dict[str, int] = {}
    for t in range(k + 1, n + 1):
        images: set[tuple[int, ...]] = set()
        raw_count = 0
        checked = 0
        for support in itertools.combinations(range(n), t):
            checked += 1
            xs = [domain[index] for index in support]
            ys = [values[index] for index in support]
            poly = interpolate_polynomial(xs, ys, p)
            if polynomial_degree(poly) < k:
                raw_count += 1
                images.add(poly)
        raw_moments[t] = raw_count
        image_by_t[t] = images
        supports_checked[str(t)] = checked
    return raw_moments, image_by_t, supports_checked


def agreement_size(poly: Iterable[int], domain: list[int], values: list[int], p: int) -> int:
    return sum(1 for x, y in zip(domain, values, strict=True) if eval_poly(poly, x, p) == y)


def agreement_shells(
    polynomials: Iterable[tuple[int, ...]],
    *,
    p: int,
    n: int,
    domain: list[int],
    values: list[int],
) -> dict[int, int]:
    shells = {a: 0 for a in range(n + 1)}
    for poly in polynomials:
        shells[agreement_size(poly, domain, values, p)] += 1
    return shells


def moment_from_shells(shells: dict[int, int], t: int, n: int) -> int:
    return sum(math.comb(a, t) * shells.get(a, 0) for a in range(t, n + 1))


def invert_shell(raw_moments: dict[int, int], a: int, n: int) -> int:
    return sum(
        ((-1) ** (t - a)) * math.comb(t, a) * raw_moments.get(t, 0)
        for t in range(a, n + 1)
    )


def cumulative_from_moments(raw_moments: dict[int, int], s: int, n: int) -> int:
    return sum(
        ((-1) ** (t - s)) * math.comb(t - 1, s - 1) * raw_moments.get(t, 0)
        for t in range(s, n + 1)
    )


def matrix_rref(matrix: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    column_count = len(rows[0]) if rows else 0
    for column in range(column_count):
        pivot = next((r for r in range(pivot_row, len(rows)) if rows[r][column] % p), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column] % p, -1, p)
        rows[pivot_row] = [(value * inverse) % p for value in rows[pivot_row]]
        for r, row in enumerate(rows):
            if r == pivot_row:
                continue
            factor = row[column] % p
            if factor:
                rows[r] = [
                    (entry - factor * pivot_entry) % p
                    for entry, pivot_entry in zip(row, rows[pivot_row], strict=True)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivot_columns


def parity_check_matrix(domain: list[int], k: int, p: int) -> list[list[int]]:
    generator = [[pow(x, degree, p) for x in domain] for degree in range(k)]
    rref, pivots = matrix_rref(generator, p)
    pivot_set = set(pivots)
    free_columns = [column for column in range(len(domain)) if column not in pivot_set]
    rows: list[list[int]] = []
    for free in free_columns:
        vector = [0] * len(domain)
        vector[free] = 1
        for row_index, pivot_column in enumerate(pivots):
            vector[pivot_column] = (-rref[row_index][free]) % p
        rows.append(vector)
    return rows


def syndrome(matrix: list[list[int]], vector: list[int], p: int) -> tuple[int, ...]:
    return tuple(sum(row[i] * vector[i] for i in range(len(vector))) % p for row in matrix)


def syndrome_weight_shells(
    *,
    p: int,
    n: int,
    k: int,
    domain: list[int],
    values: list[int],
) -> dict[int, int]:
    if p**n > SYNDROME_ENUM_LIMIT:
        raise ValueError("syndrome enumeration limit exceeded")
    checks = parity_check_matrix(domain, k, p)
    target = syndrome(checks, values, p)
    shells = {weight: 0 for weight in range(n + 1)}
    for error in itertools.product(range(p), repeat=n):
        error_values = list(error)
        if syndrome(checks, error_values, p) == target:
            shells[sum(1 for value in error_values if value != 0)] += 1
    return shells


def exhaustive_shells(
    *,
    p: int,
    n: int,
    k: int,
    domain: list[int],
    values: list[int],
) -> dict[int, int]:
    if p**k > SYNDROME_ENUM_LIMIT:
        raise ValueError("low-degree polynomial enumeration limit exceeded")
    return agreement_shells(
        all_low_degree_polynomials(p, k),
        p=p,
        n=n,
        domain=domain,
        values=values,
    )


def verify_values(
    *,
    name: str,
    p: int,
    n: int,
    k: int,
    s: int,
    domain: list[int],
    values: list[int],
    exhaustive: bool,
    syndrome_check: bool,
) -> dict[str, Any]:
    raw_moments, image_by_t, supports_checked = support_images(
        p=p, n=n, k=k, domain=domain, values=values
    )
    image_polys = image_by_t[k + 1]
    shells = agreement_shells(image_polys, p=p, n=n, domain=domain, values=values)
    direct_list_size = sum(shells.get(a, 0) for a in range(s, n + 1))
    moment_checks = {
        str(t): {
            "raw_moment": raw_moments[t],
            "from_shells": moment_from_shells(shells, t, n),
            "passed": raw_moments[t] == moment_from_shells(shells, t, n),
        }
        for t in range(k + 1, n + 1)
    }
    inversion_checks = {
        str(a): {
            "direct_shell": shells.get(a, 0),
            "from_raw_moments": invert_shell(raw_moments, a, n),
            "passed": shells.get(a, 0) == invert_shell(raw_moments, a, n),
        }
        for a in range(k + 1, n + 1)
    }
    image_at_s = image_by_t[s]
    list_at_s = {
        poly
        for poly in image_polys
        if agreement_size(poly, domain, values, p) >= s
    }
    exhaustive_result: dict[str, Any] | None = None
    if exhaustive:
        all_shells = exhaustive_shells(p=p, n=n, k=k, domain=domain, values=values)
        exhaustive_result = {
            "shells": {str(key): value for key, value in all_shells.items() if value},
            "matches_support_shells_above_k": all(
                all_shells.get(a, 0) == shells.get(a, 0) for a in range(k + 1, n + 1)
            ),
        }
    syndrome_result: dict[str, Any] | None = None
    if syndrome_check:
        weight_shells = syndrome_weight_shells(
            p=p, n=n, k=k, domain=domain, values=values
        )
        shell_comparison = {
            str(a): {
                "primitive_shell_count": shells.get(a, 0),
                "syndrome_weight_shell_count": weight_shells.get(n - a, 0),
                "passed": shells.get(a, 0) == weight_shells.get(n - a, 0),
            }
            for a in range(k + 1, n + 1)
        }
        syndrome_result = {
            "weight_shells": {
                str(key): value for key, value in weight_shells.items() if value
            },
            "primitive_shell_comparison": shell_comparison,
            "all_shells_match": all(row["passed"] for row in shell_comparison.values()),
        }
    cumulative_from_raw = cumulative_from_moments(raw_moments, s, n)
    checks = {
        "image_equals_cumulative_list": image_at_s == list_at_s,
        "moment_identity": all(row["passed"] for row in moment_checks.values()),
        "binomial_inversion": all(row["passed"] for row in inversion_checks.values()),
        "cumulative_identity": cumulative_from_raw == direct_list_size,
        "zero_word_overcount": (
            raw_moments[s] == math.comb(n, s) and direct_list_size == 1
        )
        if all(value == 0 for value in values)
        else None,
        "exhaustive_shells": None
        if exhaustive_result is None
        else exhaustive_result["matches_support_shells_above_k"],
        "primitive_syndrome_shells": None
        if syndrome_result is None
        else syndrome_result["all_shells_match"],
    }
    all_required_checks = [
        value for value in checks.values() if isinstance(value, bool)
    ]
    return {
        "name": name,
        "parameters": {"p": p, "n": n, "k": k, "s": s},
        "supports_checked": supports_checked,
        "raw_moments": {str(key): value for key, value in raw_moments.items()},
        "exact_agreement_shells": {
            str(key): value for key, value in shells.items() if value
        },
        "image_fiber_size_at_s": len(image_at_s),
        "direct_list_size_at_s": direct_list_size,
        "cumulative_from_raw_moments_at_s": cumulative_from_raw,
        "moment_checks": moment_checks,
        "inversion_checks": inversion_checks,
        "exhaustive_result": exhaustive_result,
        "syndrome_result": syndrome_result,
        "checks": checks,
        "all_passed": all(all_required_checks),
    }


def translate_values(
    values: list[int], domain: list[int], polynomial: tuple[int, ...], p: int
) -> list[int]:
    return [
        (value + eval_poly(polynomial, x, p)) % p
        for value, x in zip(values, domain, strict=True)
    ]


def verify_case(case: Case) -> dict[str, Any]:
    validate_case(case)
    domain = multiplicative_domain(case.p, case.n)
    values = received_values(case, domain)
    base = verify_values(
        name=case.name,
        p=case.p,
        n=case.n,
        k=case.k,
        s=case.s,
        domain=domain,
        values=values,
        exhaustive=case.exhaustive,
        syndrome_check=case.syndrome,
    )
    translator = (1, 1) if case.k > 1 else (1,)
    translated = verify_values(
        name=f"{case.name}-translated",
        p=case.p,
        n=case.n,
        k=case.k,
        s=case.s,
        domain=domain,
        values=translate_values(values, domain, translator, case.p),
        exhaustive=False,
        syndrome_check=False,
    )
    coset_checks = {
        "raw_moments_invariant": base["raw_moments"] == translated["raw_moments"],
        "exact_shells_invariant": (
            base["exact_agreement_shells"] == translated["exact_agreement_shells"]
        ),
        "list_size_invariant": (
            base["direct_list_size_at_s"] == translated["direct_list_size_at_s"]
        ),
    }
    return {
        "case": {
            "name": case.name,
            "p": case.p,
            "n": case.n,
            "k": case.k,
            "s": case.s,
            "template": case.template,
            "seed": case.seed,
            "exhaustive": case.exhaustive,
            "syndrome": case.syndrome,
        },
        "domain": domain,
        "base": base,
        "coset_translation": {
            "translator_low_to_high": list(translator),
            "checks": coset_checks,
            "all_passed": all(coset_checks.values()),
        },
        "all_passed": base["all_passed"] and all(coset_checks.values()),
    }


def build_report(cases: list[Case]) -> dict[str, Any]:
    results = [verify_case(case) for case in cases]
    return {
        "schema_version": "l1-repaired-locator-package-verifier-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "provenance": {
            "generator": "experimental/verify_l1_repaired_locator_package.py",
            "created_at_utc": utc_now(),
            "repo_commit": current_repo_commit(),
        },
        "summary": {
            "cases": len(results),
            "all_passed": all(result["all_passed"] for result in results),
            "syndrome_cases": sum(1 for case in cases if case.syndrome),
            "exhaustive_cases": sum(1 for case in cases if case.exhaustive),
        },
        "results": results,
    }


def parse_cases(values: list[str] | None) -> list[Case]:
    requested = values or list(DEFAULT_CASES)
    return [CASE_PRESETS[value] for value in requested]


def print_text_report(report: dict[str, Any]) -> None:
    print("L1 repaired locator theorem package verifier")
    print(f"Status: {report['status']}")
    print(f"Cases: {report['summary']['cases']}")
    print(f"All passed: {report['summary']['all_passed']}")
    for result in report["results"]:
        case = result["case"]
        base = result["base"]
        print(
            "case={name} p={p} n={n} k={k} s={s} template={template}: "
            "list={list_size} raw_s={raw_s} cumulative={cumulative} "
            "passed={passed}".format(
                **case,
                list_size=base["direct_list_size_at_s"],
                raw_s=base["raw_moments"][str(case["s"])],
                cumulative=base["cumulative_from_raw_moments_at_s"],
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
