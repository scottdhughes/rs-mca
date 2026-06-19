#!/usr/bin/env python3
"""Verify tiny L1 quotient-defect closure identities.

Status: EXPERIMENTAL / AUDIT.

This verifier checks finite instances of the identities in
experimental/l1_quotient_defect_closure.md:

* primitive Hankel full-row rank when j >= tau;
* one-defect quotient lifts produce trivial-stabilizer supports;
* boundary-locator filtering removes the defect and preserves reserve;
* low-defect support factorization as boundary times quotient locator.

This is finite audit evidence only. It does not assert a positive worst-case
RS list theorem, MCA theorem, line-decoding theorem, or protocol-safety
consequence.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.verify_l1_periodic_support_multisequence_reduction import (  # noqa: E501
    deterministic_amplitudes,
    is_invariant,
    locator_in_T_power,
    moments_from_orbit_fourier,
    orbit_fourier,
    quotient_locator,
    stabilizer_size,
    subgroup_elements,
    support_moments,
)
from experimental.verify_l1_syndrome_catalecticant_shells import (
    monic_locator_coeffs,
    multiplicative_domain,
)


STATUS = "EXPERIMENTAL / AUDIT"
CLAIM = (
    "finite verifier for quotient-defect closure identities only; no positive "
    "list-size theorem, MCA theorem, or protocol-safety claim"
)


@dataclass(frozen=True)
class DefectCase:
    name: str
    p: int
    n: int
    k: int
    d: int
    core_support: tuple[int, ...]
    boundary_support: tuple[int, ...]


CASE_PRESETS = {
    "p17-n16-d2-one-defect": DefectCase(
        name="p17-n16-d2-one-defect",
        p=17,
        n=16,
        k=8,
        d=2,
        core_support=(1, 9, 3, 11),
        boundary_support=(0,),
    ),
    "p17-n16-d4-two-defect": DefectCase(
        name="p17-n16-d4-two-defect",
        p=17,
        n=16,
        k=8,
        d=4,
        core_support=(2, 6, 10, 14),
        boundary_support=(0, 1),
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


def poly_mul(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    product = [0] * (len(left) + len(right) - 1)
    for i, a_value in enumerate(left):
        for j, b_value in enumerate(right):
            product[i + j] = (product[i + j] + a_value * b_value) % p
    return tuple(product)


def poly_eval(coeffs: tuple[int, ...], value: int, p: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % p
        power = (power * value) % p
    return total


def matrix_rank_mod(matrix: list[list[int]], p: int) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % p, -1, p)
        rows[rank] = [(value * inv) % p for value in rows[rank]]
        for row in range(row_count):
            if row != rank and rows[row][col] % p:
                factor = rows[row][col] % p
                rows[row] = [
                    (rows[row][idx] - factor * rows[rank][idx]) % p
                    for idx in range(col_count)
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def hankel_rank(syndrome: tuple[int, ...], j: int, D: int, p: int) -> int:
    tau = D - j
    matrix = [
        [syndrome[row + col] % p for col in range(j + 1)]
        for row in range(tau)
    ]
    return matrix_rank_mod(matrix, p)


def support_from_indices(domain: list[int], indices: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(domain[index] for index in indices)


def full_coset_core(
    domain: list[int], support_values: set[int], d: int, p: int
) -> set[int]:
    subgroup = subgroup_elements(domain, d, p)
    core: set[int] = set()
    seen: set[frozenset[int]] = set()
    for value in domain:
        coset = frozenset((kappa * value) % p for kappa in subgroup)
        if coset in seen:
            continue
        seen.add(coset)
        if coset.issubset(support_values):
            core.update(coset)
    return core


def boundary_filter(
    syndrome: tuple[int, ...], boundary_locator: tuple[int, ...], p: int
) -> tuple[int, ...]:
    beta = len(boundary_locator) - 1
    return tuple(
        sum(boundary_locator[u] * syndrome[r + u] for u in range(beta + 1)) % p
        for r in range(len(syndrome) - beta)
    )


def one_defect_lift_check(case: DefectCase, domain: list[int]) -> dict[str, Any]:
    support = set(
        support_from_indices(domain, case.core_support + case.boundary_support)
    )
    support_indices = tuple(domain.index(value) for value in sorted(support))
    stabilizer = stabilizer_size(domain, support_indices, case.p)
    boundary_singleton = len(case.boundary_support) == 1
    return {
        "support_size": len(support),
        "stabilizer_size": stabilizer,
        "trivial_stabilizer": stabilizer == 1,
        "boundary_singleton": boundary_singleton,
    }


def verify_case(case: DefectCase) -> dict[str, Any]:
    domain = multiplicative_domain(case.p, case.n)
    D = case.n - case.k
    support_values_set = set(
        support_from_indices(domain, case.core_support + case.boundary_support)
    )
    core_values = set(support_from_indices(domain, case.core_support))
    boundary_values = set(support_from_indices(domain, case.boundary_support))
    support_indices = tuple(domain.index(value) for value in sorted(support_values_set))
    core_indices = tuple(domain.index(value) for value in sorted(core_values))

    amplitudes = deterministic_amplitudes(domain, support_indices, case.p)
    syndrome = support_moments(amplitudes, D, case.p)
    j = len(support_indices)
    tau = D - j
    rank = hankel_rank(syndrome, j, D, case.p)

    core = full_coset_core(domain, support_values_set, case.d, case.p)
    boundary = support_values_set - core
    boundary_locator = monic_locator_coeffs(sorted(boundary), case.p)
    core_locator = monic_locator_coeffs(sorted(core), case.p)
    support_locator = monic_locator_coeffs(sorted(support_values_set), case.p)
    product_locator = poly_mul(boundary_locator, core_locator, case.p)

    filtered = boundary_filter(syndrome, boundary_locator, case.p)
    transformed_core_amplitudes = {
        root: (amplitudes[root] * poly_eval(boundary_locator, root, case.p)) % case.p
        for root in core
    }
    expected_filtered = support_moments(
        transformed_core_amplitudes, D - len(boundary), case.p
    )

    fourier = orbit_fourier(transformed_core_amplitudes, case.d, case.p)
    quotient = quotient_locator(core_locator, case.d)
    reconstructed_filtered = moments_from_orbit_fourier(
        fourier, D - len(boundary), case.d, case.p
    )

    checks = {
        "hankel_full_row_rank": (j >= tau and rank == tau) or j < tau,
        "core_is_periodic": is_invariant(domain, core_indices, case.d, case.p),
        "core_locator_in_T_power": locator_in_T_power(core_locator, case.d),
        "support_factorization": support_locator == product_locator,
        "boundary_matches_defect": boundary == boundary_values,
        "filter_removes_boundary": filtered == expected_filtered,
        "filtered_reserve_preserved": (D - len(boundary)) - len(core) == D - j,
        "filtered_fourier_decomposition": filtered == reconstructed_filtered,
        "transformed_amplitudes_nonzero": all(
            value % case.p != 0 for value in transformed_core_amplitudes.values()
        ),
    }
    if len(case.boundary_support) == 1:
        one_defect = one_defect_lift_check(case, domain)
        checks["one_defect_trivial_stabilizer"] = one_defect["trivial_stabilizer"]
        checks["one_defect_has_single_boundary"] = one_defect["boundary_singleton"]

    return {
        "case": {
            "name": case.name,
            "p": case.p,
            "n": case.n,
            "k": case.k,
            "D": D,
            "d": case.d,
            "j": j,
            "tau": tau,
            "core_size": len(core),
            "boundary_size": len(boundary),
        },
        "support": sorted(support_values_set),
        "core": sorted(core),
        "boundary": sorted(boundary),
        "rank": rank,
        "quotient_locator": list(quotient),
        "checks": checks,
        "all_passed": all(checks.values()),
    }


def build_report(cases: list[DefectCase]) -> dict[str, Any]:
    results = [verify_case(case) for case in cases]
    return {
        "schema_version": "l1-quotient-defect-closure-verifier-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "provenance": {
            "generator": "experimental/verify_l1_quotient_defect_closure.py",
            "created_at_utc": utc_now(),
            "repo_commit": current_repo_commit(),
        },
        "summary": {
            "cases": len(results),
            "all_passed": all(result["all_passed"] for result in results),
        },
        "results": results,
    }


def parse_cases(values: list[str] | None) -> list[DefectCase]:
    requested = values or list(DEFAULT_CASES)
    return [CASE_PRESETS[value] for value in requested]


def print_text_report(report: dict[str, Any]) -> None:
    print("L1 quotient defect closure verifier")
    print(f"Status: {report['status']}")
    print(f"Cases: {report['summary']['cases']}")
    print(f"All passed: {report['summary']['all_passed']}")
    for result in report["results"]:
        case = result["case"]
        print(
            "case={name} p={p} n={n} k={k} j={j} d={d}: "
            "boundary={boundary_size} rank={rank} all={passed}".format(
                **case,
                rank=result["rank"],
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
