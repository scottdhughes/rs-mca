#!/usr/bin/env python3
"""Run tiny EXPERIMENTAL locator-fiber sweeps over prime fields."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import random
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


STATUS = "EXPERIMENTAL"
CLAIM = (
    "tiny exhaustive prime-field locator-fiber sweep only; "
    "no RS/list-decoding/MCA safety assertion; "
    "no theorem status upgrade"
)
INTERPOLATION_FLOOR_EXPLANATION = (
    "When agreement_size <= k, every support of distinct domain points admits "
    "a degree < k interpolant for arbitrary received values; such rows are "
    "sanity checks, not nontrivial locator-fiber evidence."
)
TEMPLATES = ("zero", "monomial", "random")
DEFAULT_P_VALUES = (5, 17)
DEFAULT_TEMPLATES = ("zero", "monomial", "random")
DEFAULT_SEEDS = (0, 1)
DEFAULT_MAX_SUPPORTS = 200_000
CSV_COLUMNS = (
    "p",
    "n",
    "k",
    "agreement_size",
    "template",
    "seed",
    "supports_checked",
    "fiber_size",
    "fiber_density",
    "interpolation_floor",
    "nontrivial_locator_constraint",
    "nontrivial_quotient_orders",
    "quotient_periodic_valid_support_counts",
    "status",
    "json_file",
)


@dataclass(frozen=True)
class SweepCase:
    p: int
    n: int
    k: int
    agreement_size: int
    template: str
    seed: int | None


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


def parse_parameter(values: Iterable[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"parameter must be key=value: {value!r}")
        key, item = value.split("=", 1)
        if not key:
            raise ValueError("parameter key must be nonempty")
        out[key] = item
    return out


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


def multiplicative_domain(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p - 1")
    generator = primitive_root_prime(p)
    step = (p - 1) // n
    return [pow(generator, step * i, p) for i in range(n)]


def received_values(
    domain: list[int],
    *,
    p: int,
    k: int,
    template: str,
    seed: int,
) -> list[int]:
    if template == "zero":
        return [0 for _ in domain]
    if template == "monomial":
        return [pow(x, k, p) for x in domain]
    if template == "random":
        rng = random.Random(seed)
        return [rng.randrange(p) for _ in domain]
    raise ValueError(f"template must be one of {', '.join(TEMPLATES)}")


def trim_poly(coeffs: list[int]) -> list[int]:
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs


def polynomial_degree(coeffs: list[int]) -> int:
    return len(trim_poly(coeffs[:])) - 1


def add_poly(left: list[int], right: list[int], p: int) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % p
    return trim_poly(out)


def scale_poly(coeffs: list[int], scalar: int, p: int) -> list[int]:
    return trim_poly([(scalar * coeff) % p for coeff in coeffs])


def multiply_by_linear(coeffs: list[int], root: int, p: int) -> list[int]:
    out = [0] * (len(coeffs) + 1)
    for index, coeff in enumerate(coeffs):
        out[index] = (out[index] - root * coeff) % p
        out[index + 1] = (out[index + 1] + coeff) % p
    return trim_poly(out)


def interpolate_polynomial(xs: list[int], ys: list[int], p: int) -> list[int]:
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    if len(set(xs)) != len(xs):
        raise ValueError("interpolation points must be distinct")
    if not xs:
        return []

    result: list[int] = []
    for j, x_j in enumerate(xs):
        basis = [1]
        denominator = 1
        for m, x_m in enumerate(xs):
            if m == j:
                continue
            basis = multiply_by_linear(basis, x_m, p)
            denominator = (denominator * (x_j - x_m)) % p
        scale = (ys[j] * pow(denominator, -1, p)) % p
        result = add_poly(result, scale_poly(basis, scale, p), p)
    return trim_poly(result)


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


def validate_case(case: SweepCase) -> None:
    if case.p <= 2 or not is_prime(case.p):
        raise ValueError("p must be an odd prime")
    if case.n <= 0 or (case.p - 1) % case.n != 0:
        raise ValueError("n must be positive and divide p - 1")
    if not 0 < case.k <= case.n:
        raise ValueError("k must satisfy 0 < k <= n")
    if not 0 <= case.agreement_size <= case.n:
        raise ValueError("agreement_size must satisfy 0 <= agreement_size <= n")
    if case.template not in TEMPLATES:
        raise ValueError(f"template must be one of {', '.join(TEMPLATES)}")


def witness_record(
    *,
    support_indices: tuple[int, ...],
    domain: list[int],
    values: list[int],
    coeffs: list[int],
    quotient_orders: list[int],
) -> dict[str, Any]:
    degree = polynomial_degree(coeffs)
    return {
        "support_indices": list(support_indices),
        "support_elements": [domain[index] for index in support_indices],
        "support_values": [values[index] for index in support_indices],
        "interpolated_coefficients_low_to_high": coeffs,
        "polynomial_degree": None if degree < 0 else degree,
        "quotient_periodic": {
            "is_nontrivial": bool(quotient_orders),
            "quotient_orders": quotient_orders,
        },
    }


def analyze_case(
    case: SweepCase,
    *,
    max_witnesses: int,
    max_supports: int,
    parameters: dict[str, str],
) -> dict[str, Any]:
    validate_case(case)
    if max_witnesses < 0:
        raise ValueError("max_witnesses must be nonnegative")
    if max_supports <= 0:
        raise ValueError("max_supports must be positive")

    candidate_supports = math.comb(case.n, case.agreement_size)
    if candidate_supports > max_supports:
        raise ValueError(
            "candidate support count exceeds max_supports; "
            "increase --max-supports only for intentional tiny experiments"
        )

    domain = multiplicative_domain(case.p, case.n)
    values = received_values(
        domain,
        p=case.p,
        k=case.k,
        template=case.template,
        seed=0 if case.seed is None else case.seed,
    )
    quotient_orders = [
        order for order in positive_divisors(case.n) if 1 < order < case.n
    ]
    periodic_counts = {str(order): 0 for order in quotient_orders}
    witnesses: list[dict[str, Any]] = []
    fiber_size = 0
    interpolation_floor = case.agreement_size <= case.k

    for support_indices in itertools.combinations(
        range(case.n),
        case.agreement_size,
    ):
        xs = [domain[index] for index in support_indices]
        ys = [values[index] for index in support_indices]
        coeffs = interpolate_polynomial(xs, ys, case.p)
        if polynomial_degree(coeffs) >= case.k:
            continue

        fiber_size += 1
        support_orders = support_quotient_orders(support_indices, case.n)
        for order in support_orders:
            periodic_counts[str(order)] += 1
        if len(witnesses) < max_witnesses:
            witnesses.append(
                witness_record(
                    support_indices=support_indices,
                    domain=domain,
                    values=values,
                    coeffs=coeffs,
                    quotient_orders=support_orders,
                )
            )

    return {
        "schema_version": "locator-fiber-sweep-case-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "inputs": {
            "p": case.p,
            "n": case.n,
            "k": case.k,
            "agreement_size": case.agreement_size,
            "template": case.template,
            "seed": case.seed,
            "max_witnesses": max_witnesses,
            "max_supports": max_supports,
        },
        "domain": {
            "type": "F_p^*" if case.n == case.p - 1 else "multiplicative_subgroup",
            "order": case.n,
            "elements": domain,
        },
        "received_word": {
            "template": case.template,
            "values": values,
            "monomial_degree": case.k if case.template == "monomial" else None,
            "seed": case.seed if case.template == "random" else None,
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
            "definition": (
                "support is a union of kernel cosets for H -> quotient of "
                "the listed order"
            ),
            "nontrivial_quotient_orders": quotient_orders,
            "valid_support_counts_by_order": periodic_counts,
        },
        "witnesses": {
            "valid_supports": witnesses,
            "max_witnesses": max_witnesses,
        },
        "algorithm": {
            "name": "exhaustive_prime_field_support_interpolation",
            "limitations": [
                "tiny exhaustive prime-field scan only",
                "candidate supports grow binomially",
                "coverage is experimental evidence, not a theorem",
                "extension fields are not included in this script",
            ],
        },
        "provenance": {
            "generator": (
                "experimental/locator_fiber_sweep/"
                "run_locator_fiber_sweep.py"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
            "parameters": parameters,
        },
    }


def default_k_values(p: int) -> tuple[int, ...]:
    if p == 5:
        return (2,)
    if p == 17:
        return (4, 8)
    n = p - 1
    return tuple(sorted({max(1, n // 4), max(1, n // 2)}))


def default_agreement_sizes(n: int, k: int) -> tuple[int, ...]:
    return tuple(sorted({k, min(n, k + 1), min(n, k + 2)}))


def dedupe_sorted(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(set(values)))


def build_cases(
    *,
    p_values: Iterable[int],
    templates: Iterable[str],
    seeds: Iterable[int],
    k_values: Iterable[int] | None = None,
    agreement_sizes: Iterable[int] | None = None,
) -> list[SweepCase]:
    cases: list[SweepCase] = []
    selected_templates = tuple(templates)
    selected_seeds = tuple(seeds)
    for template in selected_templates:
        if template not in TEMPLATES:
            raise ValueError(f"template must be one of {', '.join(TEMPLATES)}")

    for p in p_values:
        if p <= 2 or not is_prime(p):
            raise ValueError("p values must be odd primes")
        n = p - 1
        selected_k_values = (
            dedupe_sorted(k_values)
            if k_values is not None
            else default_k_values(p)
        )
        for k in selected_k_values:
            selected_agreements = (
                dedupe_sorted(agreement_sizes)
                if agreement_sizes is not None
                else default_agreement_sizes(n, k)
            )
            for agreement_size in selected_agreements:
                for template in selected_templates:
                    template_seeds = selected_seeds if template == "random" else (None,)
                    for seed in template_seeds:
                        case = SweepCase(
                            p=p,
                            n=n,
                            k=k,
                            agreement_size=agreement_size,
                            template=template,
                            seed=seed,
                        )
                        validate_case(case)
                        cases.append(case)
    return cases


def normalized_template(template: str, seed: int | None) -> str:
    if template == "random":
        return f"random_seed{seed}"
    return template


def output_name(case: SweepCase) -> str:
    return (
        f"locator_fiber_p{case.p}_n{case.n}_k{case.k}_"
        f"a{case.agreement_size}_{normalized_template(case.template, case.seed)}"
        ".json"
    )


def csv_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    if isinstance(value, dict):
        return ";".join(f"{key}:{value[key]}" for key in sorted(value, key=int))
    return str(value)


def write_json(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def row_from_report(
    case: SweepCase,
    report: dict[str, Any],
    json_file: str,
) -> dict[str, Any]:
    scan = report["scan"]
    quotient = report["quotient_periodic_support_flags"]
    return {
        "p": case.p,
        "n": case.n,
        "k": case.k,
        "agreement_size": case.agreement_size,
        "template": case.template,
        "seed": case.seed,
        "supports_checked": scan["supports_tested"],
        "fiber_size": scan["fiber_size"],
        "fiber_density": scan["fiber_density"],
        "interpolation_floor": scan["interpolation_floor"],
        "nontrivial_locator_constraint": scan["nontrivial_locator_constraint"],
        "nontrivial_quotient_orders": quotient["nontrivial_quotient_orders"],
        "quotient_periodic_valid_support_counts": quotient[
            "valid_support_counts_by_order"
        ],
        "status": report["status"],
        "json_file": json_file,
    }


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row[column]) for column in CSV_COLUMNS})


def build_markdown(summary: dict[str, Any]) -> str:
    rows = summary["rows"]
    lines = [
        "# Locator-Fiber Sweep",
        "",
        "Tiny exhaustive experimental output only.",
        "No RS/list-decoding/MCA safety assertion.",
        "No theorem status upgrade.",
        "",
        "Rows with agreement_size <= k are interpolation-floor sanity rows.",
        "Nontrivial locator-fiber constraints begin at agreement_size > k.",
        "",
        "## Outputs",
        "",
        "- CSV: locator_fiber_sweep.csv",
        f"- Per-run JSON files: {len(rows)}",
        "",
        "## Summary",
        "",
        (
            "| p | n | k | agreement | template | seed | supports | "
            "fiber size | density | nontrivial | JSON |"
        ),
        "|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['p']} | {row['n']} | {row['k']} | "
            f"{row['agreement_size']} | {row['template']} | "
            f"{csv_value(row['seed'])} | {row['supports_checked']} | "
            f"{row['fiber_size']} | {csv_value(row['fiber_density'])} | "
            f"{row['nontrivial_locator_constraint']} | {row['json_file']} |"
        )

    lines.extend(
        [
            "",
            "## Provenance",
            "",
            f"- Status: {summary['status']}",
            f"- Claim discipline: {summary['claim']}",
            f"- Repo commit: {summary['provenance']['repo_commit']}",
            f"- Created at UTC: {summary['provenance']['created_at_utc']}",
            "- Optional CAS tools are not required by this sweep runner.",
            "",
        ]
    )
    return "\n".join(lines)


def run_case(
    case: SweepCase,
    out_dir: Path,
    *,
    max_witnesses: int,
    max_supports: int,
    parameters: dict[str, str],
) -> dict[str, Any]:
    report = analyze_case(
        case,
        max_witnesses=max_witnesses,
        max_supports=max_supports,
        parameters=parameters,
    )
    json_file = output_name(case)
    write_json(report, out_dir / json_file)
    return row_from_report(case, report, json_file)


def run_sweep(
    out_dir: Path,
    *,
    p_values: Iterable[int] = DEFAULT_P_VALUES,
    templates: Iterable[str] = DEFAULT_TEMPLATES,
    seeds: Iterable[int] = DEFAULT_SEEDS,
    k_values: Iterable[int] | None = None,
    agreement_sizes: Iterable[int] | None = None,
    max_witnesses: int = 5,
    max_supports: int = DEFAULT_MAX_SUPPORTS,
    parameters: dict[str, str] | None = None,
) -> dict[str, Any]:
    if max_witnesses < 0:
        raise ValueError("max_witnesses must be nonnegative")
    if max_supports <= 0:
        raise ValueError("max_supports must be positive")

    parameters = parameters or {}
    out_dir.mkdir(parents=True, exist_ok=True)
    cases = build_cases(
        p_values=p_values,
        templates=templates,
        seeds=seeds,
        k_values=k_values,
        agreement_sizes=agreement_sizes,
    )
    rows = [
        run_case(
            case,
            out_dir,
            max_witnesses=max_witnesses,
            max_supports=max_supports,
            parameters=parameters,
        )
        for case in cases
    ]
    rows.sort(
        key=lambda row: (
            row["p"],
            row["k"],
            row["agreement_size"],
            row["template"],
            csv_value(row["seed"]),
        )
    )

    summary = {
        "schema_version": "locator-fiber-sweep-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "output_directory": str(out_dir),
        "rows": rows,
        "provenance": {
            "generator": (
                "experimental/locator_fiber_sweep/"
                "run_locator_fiber_sweep.py"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
            "parameters": parameters,
        },
    }
    write_csv(rows, out_dir / "locator_fiber_sweep.csv")
    (out_dir / "locator_fiber_sweep.md").write_text(build_markdown(summary))
    return summary


def parse_int_values(
    values: list[int] | None,
    defaults: tuple[int, ...],
) -> tuple[int, ...]:
    if not values:
        return defaults
    return tuple(values)


def format_summary(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Locator-fiber sweep ({summary['status']})",
            f"output_directory={summary['output_directory']}",
            f"runs={len(summary['rows'])}",
            "csv=locator_fiber_sweep.csv",
            "markdown=locator_fiber_sweep.md",
            f"claim: {summary['claim']}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run bounded EXPERIMENTAL locator-fiber sweeps."
    )
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--p", type=int, action="append")
    parser.add_argument("--k", type=int, action="append")
    parser.add_argument("--agreement-size", type=int, action="append")
    parser.add_argument("--template", choices=TEMPLATES, action="append")
    parser.add_argument("--seed", type=int, action="append")
    parser.add_argument("--max-witnesses", type=int, default=5)
    parser.add_argument("--max-supports", type=int, default=DEFAULT_MAX_SUPPORTS)
    parser.add_argument(
        "--parameter",
        action="append",
        default=[],
        help="Additional provenance parameter as key=value. May be repeated.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_sweep(
            args.out_dir,
            p_values=parse_int_values(args.p, DEFAULT_P_VALUES),
            templates=tuple(args.template) if args.template else DEFAULT_TEMPLATES,
            seeds=parse_int_values(args.seed, DEFAULT_SEEDS),
            k_values=tuple(args.k) if args.k else None,
            agreement_sizes=(
                tuple(args.agreement_size) if args.agreement_size else None
            ),
            max_witnesses=args.max_witnesses,
            max_supports=args.max_supports,
            parameters=parse_parameter(args.parameter),
        )
    except ValueError as exc:
        parser.error(str(exc))

    print(format_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
