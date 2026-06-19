#!/usr/bin/env python3
"""Verify tiny L1 periodic-support multisequence reductions.

Status: EXPERIMENTAL / AUDIT.

This verifier checks the finite identities in
experimental/l1_periodic_support_multisequence_reduction.md:

* support invariance iff the locator lies in T^d;
* locator coefficient sparsity for periodic supports;
* original recurrences iff all decimated recurrences;
* orbit Fourier decomposition and inverse-DFT amplitude recovery;
* primitive guard equivalence under inverse DFT;
* exact-stabilizer counts agree with Mobius inversion.

This is finite audit evidence only. It does not assert a positive worst-case
RS list theorem, MCA theorem, line-decoding theorem, or protocol-safety
consequence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.verify_l1_syndrome_catalecticant_shells import (
    monic_locator_coeffs,
    multiplicative_domain,
    parity_weights,
    received_values,
    recurrence_passes,
    recovered_scaled_amplitudes,
    syndrome_moments,
    Case as BaseCase,
)


STATUS = "EXPERIMENTAL / AUDIT"
CLAIM = (
    "finite verifier for periodic-support multisequence reductions only; "
    "no positive list-size theorem, MCA theorem, or protocol-safety claim"
)


@dataclass(frozen=True)
class PeriodicCase:
    name: str
    p: int
    n: int
    k: int
    j: int
    d: int
    template: str
    seed: int = 0


CASE_PRESETS = {
    "p17-n8-j2-d2-random": PeriodicCase(
        "p17-n8-j2-d2-random", p=17, n=8, k=4, j=2, d=2, template="random", seed=3
    ),
    "p17-n16-j4-d2-random": PeriodicCase(
        "p17-n16-j4-d2-random", p=17, n=16, k=8, j=4, d=2, template="random", seed=4
    ),
    "p17-n16-j4-d4-random": PeriodicCase(
        "p17-n16-j4-d4-random", p=17, n=16, k=8, j=4, d=4, template="random", seed=5
    ),
}
DEFAULT_CASES = tuple(CASE_PRESETS)


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


def validate_case(case: PeriodicCase) -> None:
    if case.p < 2 or any(case.p % divisor == 0 for divisor in range(2, int(case.p**0.5) + 1)):
        raise ValueError("p must be prime")
    if case.n <= 0 or (case.p - 1) % case.n != 0:
        raise ValueError("n must be positive and divide p - 1")
    if not 0 < case.k < case.n:
        raise ValueError("case must satisfy 0 < k < n")
    if case.template not in {"zero", "monomial", "random"}:
        raise ValueError("template must be zero, monomial, or random")
    if case.n % case.d != 0:
        raise ValueError("d must divide n")
    if case.j % case.d != 0:
        raise ValueError("d must divide j")
    if case.j > case.n - case.k:
        raise ValueError("j must be at most D=n-k")


def divisors(value: int) -> list[int]:
    return [candidate for candidate in range(1, value + 1) if value % candidate == 0]


def mobius(value: int) -> int:
    remaining = value
    prime_count = 0
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            prime_count += 1
            if remaining % divisor == 0:
                return 0
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        prime_count += 1
    return -1 if prime_count % 2 else 1


def subgroup_elements(domain: list[int], d: int, p: int) -> list[int]:
    return sorted(value for value in domain if pow(value, d, p) == 1)


def support_values(domain: list[int], support: tuple[int, ...]) -> set[int]:
    return {domain[index] for index in support}


def is_invariant(
    domain: list[int], support: tuple[int, ...], d: int, p: int
) -> bool:
    values = support_values(domain, support)
    subgroup = subgroup_elements(domain, d, p)
    return all((kappa * value) % p in values for value in values for kappa in subgroup)


def stabilizer_size(domain: list[int], support: tuple[int, ...], p: int) -> int:
    values = support_values(domain, support)
    stabilizer = [
        multiplier
        for multiplier in domain
        if {(multiplier * value) % p for value in values} == values
    ]
    return len(stabilizer)


def locator_in_T_power(locator: tuple[int, ...], d: int) -> bool:
    degree = len(locator) - 1
    if degree % d != 0:
        return False
    return all(coefficient == 0 for exponent, coefficient in enumerate(locator) if exponent % d)


def quotient_locator(locator: tuple[int, ...], d: int) -> tuple[int, ...]:
    degree = len(locator) - 1
    if degree % d != 0:
        raise ValueError("degree must be divisible by d")
    return tuple(locator[d * index] for index in range(degree // d + 1))


def decimated_recurrence_passes(
    quotient: tuple[int, ...], syndrome: tuple[int, ...], D: int, d: int, p: int
) -> bool:
    j_prime = len(quotient) - 1
    j = d * j_prime
    for c in range(d):
        t = 0
        while c + d * t < D - j:
            value = sum(
                quotient[h] * syndrome[c + d * (t + h)]
                for h in range(j_prime + 1)
            )
            if value % p:
                return False
            t += 1
    return True


def deterministic_amplitudes(domain: list[int], support: tuple[int, ...], p: int) -> dict[int, int]:
    amplitudes: dict[int, int] = {}
    for rank, index in enumerate(support):
        amplitudes[domain[index]] = (rank + 1) % p or 1
    return amplitudes


def support_moments(amplitudes: dict[int, int], D: int, p: int) -> tuple[int, ...]:
    return tuple(
        sum(value * pow(root, moment, p) for root, value in amplitudes.items()) % p
        for moment in range(D)
    )


def orbit_fourier(
    amplitudes: dict[int, int], d: int, p: int
) -> dict[int, list[int]]:
    quotient: dict[int, list[int]] = {}
    for root in amplitudes:
        quotient.setdefault(pow(root, d, p), [])
    result: dict[int, list[int]] = {}
    for y_value in quotient:
        orbit_roots = [root for root in amplitudes if pow(root, d, p) == y_value]
        result[y_value] = [
            sum(amplitudes[root] * pow(root, c, p) for root in orbit_roots) % p
            for c in range(d)
        ]
    return result


def moments_from_orbit_fourier(
    fourier: dict[int, list[int]], D: int, d: int, p: int
) -> tuple[int, ...]:
    moments = []
    for moment in range(D):
        c = moment % d
        t = moment // d
        moments.append(
            sum(values[c] * pow(y_value, t, p) for y_value, values in fourier.items()) % p
        )
    return tuple(moments)


def inverse_dft_amplitude(
    root: int, fourier_values: list[int], d: int, p: int
) -> int:
    inv_d = pow(d % p, -1, p)
    return (
        inv_d
        * sum(fourier_values[c] * pow(root, (-c) % (p - 1), p) for c in range(d))
    ) % p


def primitive_guard_from_inverse_dft(
    amplitudes: dict[int, int], fourier: dict[int, list[int]], d: int, p: int
) -> bool:
    return all(
        inverse_dft_amplitude(root, fourier[pow(root, d, p)], d, p) != 0
        for root in amplitudes
    )


def primitive_support_passes(
    domain: list[int],
    support: tuple[int, ...],
    syndrome: tuple[int, ...],
    D: int,
    p: int,
) -> bool:
    roots = [domain[index] for index in support]
    locator = monic_locator_coeffs(roots, p)
    if not recurrence_passes(locator, syndrome, D, p):
        return False
    scaled = recovered_scaled_amplitudes(roots, syndrome, p)
    return all(value % p != 0 for value in scaled)


def support_counts(
    domain: list[int], syndrome: tuple[int, ...], D: int, j: int, p: int
) -> tuple[dict[int, int], dict[int, int]]:
    gcd_value = math.gcd(len(domain), j)
    p_counts = {d: 0 for d in divisors(gcd_value)}
    q_counts = {d: 0 for d in divisors(gcd_value)}
    for support in itertools.combinations(range(len(domain)), j):
        if not primitive_support_passes(domain, support, syndrome, D, p):
            continue
        exact = stabilizer_size(domain, support, p)
        if exact in q_counts:
            q_counts[exact] += 1
        for d in p_counts:
            if exact % d == 0:
                p_counts[d] += 1
    return p_counts, q_counts


def verify_case(case: PeriodicCase) -> dict[str, Any]:
    validate_case(case)
    domain = multiplicative_domain(case.p, case.n)
    weights = parity_weights(domain, case.p)
    base = BaseCase(
        name=case.name,
        p=case.p,
        n=case.n,
        k=case.k,
        s=case.n - case.j,
        template=case.template,
        seed=case.seed,
    )
    values = received_values(base, domain)
    D = case.n - case.k
    syndrome = syndrome_moments(values, domain, weights, D, case.p)

    support_rows: list[dict[str, Any]] = []
    periodic_supports: list[tuple[int, ...]] = []
    for support in itertools.combinations(range(case.n), case.j):
        roots = [domain[index] for index in support]
        locator = monic_locator_coeffs(roots, case.p)
        invariant = is_invariant(domain, support, case.d, case.p)
        in_t_power = locator_in_T_power(locator, case.d)
        sparse = all(
            coefficient == 0
            for exponent, coefficient in enumerate(locator)
            if exponent % case.d
        )
        row: dict[str, Any] = {
            "support": list(support),
            "invariant": invariant,
            "locator_in_T_power": in_t_power,
            "coefficient_sparsity": sparse,
            "invariance_matches_locator": invariant == in_t_power == sparse,
        }
        if invariant:
            periodic_supports.append(support)
            quotient = quotient_locator(locator, case.d)
            original_ok = recurrence_passes(locator, syndrome, D, case.p)
            decimated_ok = decimated_recurrence_passes(
                quotient, syndrome, D, case.d, case.p
            )
            amplitudes = deterministic_amplitudes(domain, support, case.p)
            moments = support_moments(amplitudes, D, case.p)
            fourier = orbit_fourier(amplitudes, case.d, case.p)
            moments_from_fourier = moments_from_orbit_fourier(
                fourier, D, case.d, case.p
            )
            inverse_values = {
                str(root): inverse_dft_amplitude(
                    root, fourier[pow(root, case.d, case.p)], case.d, case.p
                )
                for root in amplitudes
            }
            row.update(
                {
                    "original_recurrence": original_ok,
                    "decimated_recurrence": decimated_ok,
                    "original_matches_decimated": original_ok == decimated_ok,
                    "orbit_fourier_moments_match": moments == moments_from_fourier,
                    "inverse_dft_matches_amplitudes": all(
                        inverse_values[str(root)] == value
                        for root, value in amplitudes.items()
                    ),
                    "primitive_guard_matches_inverse_dft": (
                        all(value != 0 for value in amplitudes.values())
                        == primitive_guard_from_inverse_dft(
                            amplitudes, fourier, case.d, case.p
                        )
                    ),
                }
            )
        support_rows.append(row)

    # Build a nontrivial syndrome from the first periodic support when possible
    # so Mobius inversion is checked on a support-generated primitive shell.
    mobius_syndrome = syndrome
    if periodic_supports:
        amplitudes = deterministic_amplitudes(domain, periodic_supports[0], case.p)
        mobius_syndrome = support_moments(amplitudes, D, case.p)
    p_counts, q_counts = support_counts(domain, mobius_syndrome, D, case.j, case.p)
    mobius_counts = {
        d: sum(
            mobius(e // d) * p_counts[e]
            for e in p_counts
            if e % d == 0
        )
        for d in p_counts
    }

    checks = {
        "invariance_locator_sparsity_equivalence": all(
            row["invariance_matches_locator"] for row in support_rows
        ),
        "original_decimated_equivalence": all(
            row.get("original_matches_decimated", True) for row in support_rows
        ),
        "orbit_fourier_decomposition": all(
            row.get("orbit_fourier_moments_match", True) for row in support_rows
        ),
        "inverse_dft_recovery": all(
            row.get("inverse_dft_matches_amplitudes", True) for row in support_rows
        ),
        "primitive_guard_equivalence": all(
            row.get("primitive_guard_matches_inverse_dft", True) for row in support_rows
        ),
        "mobius_inversion": mobius_counts == q_counts,
    }

    return {
        "case": {
            "name": case.name,
            "p": case.p,
            "n": case.n,
            "k": case.k,
            "j": case.j,
            "d": case.d,
            "template": case.template,
            "seed": case.seed,
        },
        "domain": domain,
        "syndrome": list(syndrome),
        "periodic_support_count": len(periodic_supports),
        "support_rows": support_rows,
        "mobius": {
            "p_counts": {str(key): value for key, value in p_counts.items()},
            "q_counts_direct": {str(key): value for key, value in q_counts.items()},
            "q_counts_mobius": {str(key): value for key, value in mobius_counts.items()},
        },
        "checks": checks,
        "all_passed": all(checks.values()),
    }


def build_report(cases: list[PeriodicCase]) -> dict[str, Any]:
    results = [verify_case(case) for case in cases]
    return {
        "schema_version": "l1-periodic-support-multisequence-verifier-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "provenance": {
            "generator": "experimental/verify_l1_periodic_support_multisequence_reduction.py",
            "created_at_utc": utc_now(),
            "repo_commit": current_repo_commit(),
        },
        "summary": {
            "cases": len(results),
            "all_passed": all(result["all_passed"] for result in results),
        },
        "results": results,
    }


def parse_cases(values: list[str] | None) -> list[PeriodicCase]:
    requested = values or list(DEFAULT_CASES)
    return [CASE_PRESETS[value] for value in requested]


def print_text_report(report: dict[str, Any]) -> None:
    print("L1 periodic support multisequence verifier")
    print(f"Status: {report['status']}")
    print(f"Cases: {report['summary']['cases']}")
    print(f"All passed: {report['summary']['all_passed']}")
    for result in report["results"]:
        case = result["case"]
        print(
            "case={name} p={p} n={n} k={k} j={j} d={d}: periodic={periodic} all={passed}".format(
                **case,
                periodic=result["periodic_support_count"],
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
