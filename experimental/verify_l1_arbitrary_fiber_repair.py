#!/usr/bin/env python3
"""Verify the L1 arbitrary-fiber repair identity in tiny prime fields.

Status: EXPERIMENTAL / AUDIT.

This verifier checks the exact finite identity

    |Fib_U(s)| = sum_P binom(|A_P(U)|, s),

where P ranges over the low-degree polynomials appearing as U mod L_S for
s-subsets S in the raw support fiber.  It is finite evidence and an audit
sanity check for experimental/l1_arbitrary_fiber_repair.md; it does not assert
Reed-Solomon list-decoding, MCA, or protocol safety.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


STATUS = "EXPERIMENTAL / AUDIT"
CLAIM = (
    "finite verifier for the raw-support fiber multiplicity identity only; "
    "no RS/list-decoding/MCA safety assertion; no theorem status upgrade"
)
TEMPLATES = ("zero", "monomial", "random")
DEFAULT_CASES = (
    "p5-zero",
    "p5-monomial",
    "p17-zero",
    "p17-monomial",
    "p17-random",
)


@dataclass(frozen=True)
class RepairCase:
    name: str
    p: int
    n: int
    k: int
    s: int
    template: str
    seed: int | None = None


CASE_PRESETS = {
    "p5-zero": RepairCase("p5-zero", p=5, n=4, k=2, s=3, template="zero"),
    "p5-monomial": RepairCase(
        "p5-monomial", p=5, n=4, k=2, s=3, template="monomial"
    ),
    "p17-zero": RepairCase("p17-zero", p=17, n=16, k=8, s=9, template="zero"),
    "p17-monomial": RepairCase(
        "p17-monomial", p=17, n=16, k=8, s=9, template="monomial"
    ),
    "p17-random": RepairCase(
        "p17-random", p=17, n=16, k=8, s=9, template="random", seed=0
    ),
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


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value in {2, 3}:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def primitive_root_prime(p: int) -> int:
    if not is_prime(p):
        raise ValueError("p must be prime")
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def multiplicative_domain(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p - 1")
    generator = primitive_root_prime(p)
    step = (p - 1) // n
    return [pow(generator, step * index, p) for index in range(n)]


def received_values(case: RepairCase, domain: list[int]) -> list[int]:
    if case.template == "zero":
        return [0 for _ in domain]
    if case.template == "monomial":
        return [pow(x, case.k, case.p) for x in domain]
    if case.template == "random":
        rng = random.Random(case.seed if case.seed is not None else 0)
        return [rng.randrange(case.p) for _ in domain]
    raise ValueError(f"template must be one of {', '.join(TEMPLATES)}")


def trim_poly(coeffs: Iterable[int]) -> tuple[int, ...]:
    out = list(coeffs)
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def polynomial_degree(coeffs: Iterable[int]) -> int:
    return len(trim_poly(coeffs)) - 1


def add_poly(left: Iterable[int], right: Iterable[int], p: int) -> tuple[int, ...]:
    left_values = tuple(left)
    right_values = tuple(right)
    size = max(len(left_values), len(right_values))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left_values[index] if index < len(left_values) else 0)
            + (right_values[index] if index < len(right_values) else 0)
        ) % p
    return trim_poly(out)


def scale_poly(coeffs: Iterable[int], scalar: int, p: int) -> tuple[int, ...]:
    return trim_poly((scalar * coeff) % p for coeff in coeffs)


def multiply_by_linear(coeffs: Iterable[int], root: int, p: int) -> tuple[int, ...]:
    values = tuple(coeffs)
    out = [0] * (len(values) + 1)
    for index, coeff in enumerate(values):
        out[index] = (out[index] - root * coeff) % p
        out[index + 1] = (out[index + 1] + coeff) % p
    return trim_poly(out)


def interpolate_polynomial(xs: list[int], ys: list[int], p: int) -> tuple[int, ...]:
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    if len(set(xs)) != len(xs):
        raise ValueError("interpolation points must be distinct")
    if not xs:
        return ()

    result: tuple[int, ...] = ()
    for j, x_j in enumerate(xs):
        basis: tuple[int, ...] = (1,)
        denominator = 1
        for m, x_m in enumerate(xs):
            if m == j:
                continue
            basis = multiply_by_linear(basis, x_m, p)
            denominator = (denominator * (x_j - x_m)) % p
        scale = (ys[j] * pow(denominator, -1, p)) % p
        result = add_poly(result, scale_poly(basis, scale, p), p)
    return trim_poly(result)


def eval_poly(coeffs: Iterable[int], x: int, p: int) -> int:
    value = 0
    for coeff in reversed(tuple(coeffs)):
        value = (value * x + coeff) % p
    return value


def validate_case(case: RepairCase) -> None:
    if case.template not in TEMPLATES:
        raise ValueError(f"unknown template: {case.template}")
    if not is_prime(case.p):
        raise ValueError("p must be prime")
    if case.n <= 0 or (case.p - 1) % case.n != 0:
        raise ValueError("n must be positive and divide p - 1")
    if not 0 < case.k < case.s <= case.n:
        raise ValueError("case must satisfy 0 < k < s <= n")


def histogram(values: Iterable[int]) -> dict[str, int]:
    out: dict[str, int] = {}
    for value in values:
        key = str(value)
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda item: int(item[0])))


def verify_case(case: RepairCase, *, include_rows: bool = False) -> dict[str, Any]:
    validate_case(case)
    domain = multiplicative_domain(case.p, case.n)
    values = received_values(case, domain)
    raw_supports_by_poly: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    supports_checked = 0

    for support in itertools.combinations(range(case.n), case.s):
        supports_checked += 1
        xs = [domain[index] for index in support]
        ys = [values[index] for index in support]
        poly = interpolate_polynomial(xs, ys, case.p)
        if polynomial_degree(poly) < case.k:
            raw_supports_by_poly.setdefault(poly, []).append(support)

    raw_fiber_size = sum(len(supports) for supports in raw_supports_by_poly.values())
    image_fiber_size = len(raw_supports_by_poly)
    maximal_supports: set[tuple[int, ...]] = set()
    canonical_selectors: set[tuple[int, ...]] = set()
    exact_full_agreement_polys = 0
    multiplicity_rows: list[dict[str, Any]] = []
    multiplicity_identity_holds = True

    for poly, supports in sorted(raw_supports_by_poly.items()):
        agreement = tuple(
            index
            for index, x in enumerate(domain)
            if eval_poly(poly, x, case.p) == values[index]
        )
        agreement_size = len(agreement)
        if agreement_size < case.s:
            multiplicity_identity_holds = False
        expected = math.comb(agreement_size, case.s)
        observed = len(supports)
        if expected != observed:
            multiplicity_identity_holds = False
        maximal_supports.add(agreement)
        canonical_selectors.add(tuple(agreement[: case.s]))
        if agreement_size == case.s:
            exact_full_agreement_polys += 1
        multiplicity_rows.append(
            {
                "polynomial_low_to_high": list(poly),
                "agreement_size": agreement_size,
                "raw_support_multiplicity": observed,
                "expected_multiplicity": expected,
                "identity_holds": observed == expected,
            }
        )

    repaired_counts_match = (
        image_fiber_size == len(maximal_supports) == len(canonical_selectors)
    )
    expected_total = sum(row["expected_multiplicity"] for row in multiplicity_rows)

    result: dict[str, Any] = {
        "case": {
            "name": case.name,
            "p": case.p,
            "n": case.n,
            "k": case.k,
            "s": case.s,
            "template": case.template,
            "seed": case.seed,
        },
        "domain": {
            "type": "F_p^* subgroup",
            "order": case.n,
            "elements": domain,
        },
        "received_word": {
            "template": case.template,
            "seed": case.seed,
            "values": values,
        },
        "counts": {
            "supports_checked": supports_checked,
            "raw_support_fiber_size": raw_fiber_size,
            "image_fiber_size": image_fiber_size,
            "maximal_support_fiber_size": len(maximal_supports),
            "canonical_selector_fiber_size": len(canonical_selectors),
            "exact_full_agreement_fiber_size": exact_full_agreement_polys,
            "multiplicity_sum": expected_total,
        },
        "checks": {
            "multiplicity_identity_holds": multiplicity_identity_holds,
            "raw_equals_multiplicity_sum": raw_fiber_size == expected_total,
            "repaired_counts_match": repaired_counts_match,
            "zero_overcount_detected": (
                case.template == "zero"
                and image_fiber_size == 1
                and raw_fiber_size == math.comb(case.n, case.s)
            ),
        },
        "multiplicity_histograms": {
            "agreement_size": histogram(
                row["agreement_size"] for row in multiplicity_rows
            ),
            "raw_support_multiplicity": histogram(
                row["raw_support_multiplicity"] for row in multiplicity_rows
            ),
        },
        "status": STATUS,
        "claim": CLAIM,
    }
    if include_rows:
        result["multiplicity_rows"] = multiplicity_rows
    return result


def parse_case(values: list[str] | None) -> list[RepairCase]:
    requested = values or list(DEFAULT_CASES)
    cases: list[RepairCase] = []
    for value in requested:
        try:
            cases.append(CASE_PRESETS[value])
        except KeyError as exc:
            choices = ", ".join(sorted(CASE_PRESETS))
            raise SystemExit(f"unknown case {value!r}; choices: {choices}") from exc
    return cases


def build_report(cases: list[RepairCase], *, include_rows: bool = False) -> dict[str, Any]:
    results = [verify_case(case, include_rows=include_rows) for case in cases]
    all_passed = all(
        result["checks"]["multiplicity_identity_holds"]
        and result["checks"]["raw_equals_multiplicity_sum"]
        and result["checks"]["repaired_counts_match"]
        for result in results
    )
    return {
        "schema_version": "l1-arbitrary-fiber-repair-verifier-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "provenance": {
            "generator": "experimental/verify_l1_arbitrary_fiber_repair.py",
            "created_at_utc": utc_now(),
            "repo_commit": current_repo_commit(),
        },
        "summary": {
            "cases": len(results),
            "all_passed": all_passed,
            "include_rows": include_rows,
            "zero_overcount_cases": sum(
                1 for result in results if result["checks"]["zero_overcount_detected"]
            ),
        },
        "results": results,
    }


def print_text_report(report: dict[str, Any]) -> None:
    print("L1 arbitrary-fiber repair verifier")
    print(f"Status: {report['status']}")
    print(f"Cases: {report['summary']['cases']}")
    print(f"All passed: {report['summary']['all_passed']}")
    print(f"Zero overcount cases: {report['summary']['zero_overcount_cases']}")
    for result in report["results"]:
        case = result["case"]
        counts = result["counts"]
        checks = result["checks"]
        print(
            "case={name} p={p} n={n} k={k} s={s} template={template}: "
            "raw={raw_support_fiber_size}, image={image_fiber_size}, "
            "max={maximal_support_fiber_size}, canonical={canonical_selector_fiber_size}, "
            "exact_full={exact_full_agreement_fiber_size}, passed={passed}".format(
                **case,
                **counts,
                passed=(
                    checks["multiplicity_identity_holds"]
                    and checks["raw_equals_multiplicity_sum"]
                    and checks["repaired_counts_match"]
                ),
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
    parser.add_argument(
        "--include-rows",
        action="store_true",
        help="include every per-polynomial multiplicity row in JSON output",
    )
    args = parser.parse_args(argv)

    report = build_report(parse_case(args.case), include_rows=args.include_rows)
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
