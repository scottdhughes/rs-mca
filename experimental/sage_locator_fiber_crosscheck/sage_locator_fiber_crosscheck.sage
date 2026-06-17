#!/usr/bin/env sage -python
"""Optional Sage cross-checks for tiny locator-fiber experiments."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sage.all import GF, Integer, PolynomialRing


STATUS = "EXPERIMENTAL"
CLAIM = (
    "optional Sage finite-field locator-fiber cross-check only; "
    "no RS/list-decoding/MCA safety assertion; "
    "no theorem status upgrade"
)
INTERPOLATION_FLOOR_EXPLANATION = (
    "When agreement_size <= k, every support of distinct domain points admits "
    "a degree < k interpolant for arbitrary received values; such rows are "
    "sanity checks, not nontrivial locator-fiber evidence."
)
TEMPLATES = ("zero", "monomial", "random")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def current_repo_commit() -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=repo_root(),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def positive_divisors(value: int) -> list[int]:
    if value <= 0:
        raise ValueError("value must be positive")
    small: list[int] = []
    large: list[int] = []
    divisor = 1
    while divisor * divisor <= value:
        if value % divisor == 0:
            small.append(divisor)
            if divisor != value // divisor:
                large.append(value // divisor)
        divisor += 1
    return small + large[::-1]


def validate_inputs(
    *,
    p: int,
    n: int,
    k: int,
    agreement_size: int,
    template: str,
    max_witnesses: int,
) -> None:
    if p <= 2 or not Integer(p).is_prime():
        raise ValueError("p must be an odd prime")
    if n <= 0 or (p - 1) % n != 0:
        raise ValueError("n must be positive and divide p - 1")
    if not 0 < k <= n:
        raise ValueError("k must satisfy 0 < k <= n")
    if not 0 <= agreement_size <= n:
        raise ValueError("agreement_size must satisfy 0 <= agreement_size <= n")
    if template not in TEMPLATES:
        raise ValueError(f"template must be one of {', '.join(TEMPLATES)}")
    if max_witnesses < 0:
        raise ValueError("max_witnesses must be nonnegative")


def multiplicative_domain(p: int, n: int) -> list[Any]:
    field = GF(p)
    generator = field.multiplicative_generator()
    step = (p - 1) // n
    return [generator ** (step * index) for index in range(n)]


def received_values(
    domain: list[Any],
    *,
    p: int,
    k: int,
    template: str,
    seed: int,
) -> list[Any]:
    field = GF(p)
    if template == "zero":
        return [field(0) for _ in domain]
    if template == "monomial":
        return [x**k for x in domain]
    if template == "random":
        rng = random.Random(seed)
        return [field(rng.randrange(p)) for _ in domain]
    raise ValueError(f"template must be one of {', '.join(TEMPLATES)}")


def interpolate_polynomial(xs: list[Any], ys: list[Any], p: int) -> Any:
    field = GF(p)
    ring = PolynomialRing(field, "x")
    x = ring.gen()
    result = ring(0)
    for j, x_j in enumerate(xs):
        basis = ring(1)
        denominator = field(1)
        for m, x_m in enumerate(xs):
            if m == j:
                continue
            basis *= x - x_m
            denominator *= x_j - x_m
        result += ys[j] * denominator ** (-1) * basis
    return result


def support_quotient_orders(indices: tuple[int, ...], n: int) -> list[int]:
    support = set(indices)
    orders: list[int] = []
    for quotient_order in positive_divisors(n):
        if quotient_order in {1, n}:
            continue
        coset_size = n // quotient_order
        is_union = True
        for residue in range(quotient_order):
            count = sum(
                1
                for value in range(residue, n, quotient_order)
                if value in support
            )
            if count not in {0, coset_size}:
                is_union = False
                break
        if is_union:
            orders.append(quotient_order)
    return orders


def polynomial_coefficients_low_to_high(poly: Any) -> list[int]:
    degree = poly.degree()
    if degree < 0:
        return []
    return [int(poly[index]) for index in range(degree + 1)]


def witness_record(
    *,
    support_indices: tuple[int, ...],
    domain: list[Any],
    values: list[Any],
    poly: Any,
    quotient_orders: list[int],
) -> dict[str, Any]:
    degree = poly.degree()
    return {
        "support_indices": list(support_indices),
        "support_elements": [int(domain[index]) for index in support_indices],
        "support_values": [int(values[index]) for index in support_indices],
        "interpolated_coefficients_low_to_high": (
            polynomial_coefficients_low_to_high(poly)
        ),
        "polynomial_degree": None if degree < 0 else int(degree),
        "quotient_periodic": {
            "is_nontrivial": bool(quotient_orders),
            "quotient_orders": quotient_orders,
        },
    }


def analyze_case(
    *,
    p: int,
    n: int,
    k: int,
    agreement_size: int,
    template: str,
    seed: int,
    max_witnesses: int,
) -> dict[str, Any]:
    validate_inputs(
        p=p,
        n=n,
        k=k,
        agreement_size=agreement_size,
        template=template,
        max_witnesses=max_witnesses,
    )
    domain = multiplicative_domain(p, n)
    values = received_values(domain, p=p, k=k, template=template, seed=seed)
    candidate_supports = math.comb(n, agreement_size)
    quotient_orders = [order for order in positive_divisors(n) if 1 < order < n]
    periodic_counts = {str(order): 0 for order in quotient_orders}
    witnesses: list[dict[str, Any]] = []
    fiber_size = 0
    interpolation_floor = agreement_size <= k

    for support_indices in itertools.combinations(range(n), agreement_size):
        xs = [domain[index] for index in support_indices]
        ys = [values[index] for index in support_indices]
        poly = interpolate_polynomial(xs, ys, p)
        if poly.degree() >= k:
            continue

        fiber_size += 1
        support_orders = support_quotient_orders(support_indices, n)
        for order in support_orders:
            periodic_counts[str(order)] += 1
        if len(witnesses) < max_witnesses:
            witnesses.append(
                witness_record(
                    support_indices=support_indices,
                    domain=domain,
                    values=values,
                    poly=poly,
                    quotient_orders=support_orders,
                )
            )

    return {
        "schema_version": "sage-locator-fiber-crosscheck-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "inputs": {
            "p": p,
            "n": n,
            "k": k,
            "agreement_size": agreement_size,
            "template": template,
            "seed": seed,
            "max_witnesses": max_witnesses,
        },
        "domain": {
            "type": "F_p^*" if n == p - 1 else "multiplicative_subgroup",
            "order": n,
            "elements": [int(item) for item in domain],
        },
        "scan": {
            "candidate_supports": candidate_supports,
            "supports_tested": candidate_supports,
            "support_enumeration_complete": True,
            "fiber_size": fiber_size,
            "fiber_density": (
                fiber_size / candidate_supports if candidate_supports else None
            ),
            "interpolation_floor": interpolation_floor,
            "nontrivial_locator_constraint": not interpolation_floor,
            "interpolation_floor_explanation": INTERPOLATION_FLOOR_EXPLANATION,
            "validity_condition": "interpolation polynomial has degree < k",
        },
        "quotient_periodic_support_flags": {
            "checked": True,
            "nontrivial_quotient_orders": quotient_orders,
            "valid_support_counts_by_order": periodic_counts,
        },
        "witnesses": {
            "valid_supports": witnesses,
            "max_witnesses": max_witnesses,
        },
        "algorithm": {
            "name": "sage_prime_field_support_interpolation",
            "limitations": [
                "optional independent Sage cross-check",
                "finite prime-field experiment only",
                "coverage is evidence, not a theorem",
                "large support enumerations can be slow",
            ],
        },
        "source_comparison": {
            "python_pipeline_case_id": (
                f"locator_fiber_p{p}_n{n}_k{k}_a{agreement_size}_{template}"
            ),
            "python_reference_script": (
                "experimental/locator_fiber_sweep/"
                "run_locator_fiber_sweep.py"
            ),
        },
        "provenance": {
            "generator": (
                "experimental/sage_locator_fiber_crosscheck/"
                "sage_locator_fiber_crosscheck.sage"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
        },
    }


def selected_cases() -> list[dict[str, Any]]:
    return [
        {
            "p": 5,
            "n": 4,
            "k": 2,
            "agreement_size": 3,
            "template": "monomial",
            "seed": 0,
        },
        {
            "p": 5,
            "n": 4,
            "k": 2,
            "agreement_size": 3,
            "template": "zero",
            "seed": 0,
        },
        {
            "p": 17,
            "n": 16,
            "k": 8,
            "agreement_size": 9,
            "template": "monomial",
            "seed": 0,
        },
    ]


def aggregate_reports(reports: list[dict[str, Any]], preset: str) -> dict[str, Any]:
    return {
        "schema_version": "sage-locator-fiber-crosscheck-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "preset": preset,
        "reports": reports,
        "provenance": {
            "generator": (
                "experimental/sage_locator_fiber_crosscheck/"
                "sage_locator_fiber_crosscheck.sage"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
        },
    }


def write_json(report: dict[str, Any], path: Path | None) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def format_case_summary(report: dict[str, Any]) -> str:
    inputs = report["inputs"]
    scan = report["scan"]
    return "\n".join(
        [
            f"Sage locator-fiber cross-check ({report['status']})",
            (
                "inputs: "
                f"p={inputs['p']} n={inputs['n']} k={inputs['k']} "
                f"agreement_size={inputs['agreement_size']} "
                f"template={inputs['template']}"
            ),
            (
                "scan: "
                f"supports={scan['supports_tested']} "
                f"fiber_size={scan['fiber_size']} "
                f"density={scan['fiber_density']}"
            ),
            f"claim: {report['claim']}",
        ]
    )


def format_summary(report: dict[str, Any]) -> str:
    if "reports" not in report:
        return format_case_summary(report)
    lines = [
        f"Sage locator-fiber cross-check ({report['status']})",
        f"preset={report['preset']} cases={len(report['reports'])}",
        f"claim: {report['claim']}",
    ]
    for item in report["reports"]:
        inputs = item["inputs"]
        scan = item["scan"]
        lines.append(
            "case: "
            f"p={inputs['p']} n={inputs['n']} k={inputs['k']} "
            f"a={inputs['agreement_size']} template={inputs['template']} "
            f"fiber={scan['fiber_size']}/{scan['supports_tested']}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Optional Sage cross-check for tiny locator-fiber scans."
    )
    parser.add_argument("--p", type=int)
    parser.add_argument("--n", type=int)
    parser.add_argument("--k", type=int)
    parser.add_argument("--agreement-size", type=int)
    parser.add_argument("--template", choices=TEMPLATES)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--preset", choices=("selected",))
    parser.add_argument("--max-witnesses", type=int, default=5)
    parser.add_argument("--json-out", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        explicit_args = [args.p, args.n, args.k, args.agreement_size, args.template]
        if args.preset and any(value is not None for value in explicit_args):
            raise ValueError("use --preset or explicit case parameters, not both")
        if args.preset == "selected":
            reports = [
                analyze_case(
                    p=case["p"],
                    n=case["n"],
                    k=case["k"],
                    agreement_size=case["agreement_size"],
                    template=case["template"],
                    seed=case["seed"],
                    max_witnesses=args.max_witnesses,
                )
                for case in selected_cases()
            ]
            report = aggregate_reports(reports, args.preset)
        else:
            if any(value is None for value in explicit_args):
                raise ValueError(
                    "provide --p, --n, --k, --agreement-size, and --template"
                )
            report = analyze_case(
                p=args.p,
                n=args.n,
                k=args.k,
                agreement_size=args.agreement_size,
                template=args.template,
                seed=args.seed,
                max_witnesses=args.max_witnesses,
            )
    except ValueError as exc:
        parser.error(str(exc))

    write_json(report, args.json_out)
    print(format_summary(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
