#!/usr/bin/env python3
"""Verify tiny L1 determinantal support criterion identities.

Status: EXPERIMENTAL / AUDIT.

This verifier checks the finite identities in
experimental/l1_determinantal_support_criterion.md:

* generalized Vandermonde minors vanish iff locator recurrences hold;
* Cramer minors vanish iff recovered scaled amplitudes vanish;
* the resulting quasi-affine support system matches the guarded Hankel-divisor
  shell from experimental/l1_syndrome_catalecticant_shells.py.

This is finite audit evidence only. It does not assert a positive worst-case
RS list theorem, MCA theorem, line-decoding theorem, or protocol-safety
consequence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.verify_l1_syndrome_catalecticant_shells import (
    CASE_PRESETS,
    DEFAULT_CASES,
    STATUS,
    Case,
    Atom,
    guarded_hankel_divisor_atoms,
    monic_locator_coeffs,
    multiplicative_domain,
    parity_weights,
    received_values,
    recovered_scaled_amplitudes,
    recurrence_passes,
    syndrome_moments,
    validate_case,
)


CLAIM = (
    "finite verifier for the determinantal support criterion only; "
    "no positive list-size theorem, MCA theorem, or protocol-safety claim"
)


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


def det_mod(matrix: list[list[int]], p: int) -> int:
    if not matrix:
        return 1
    rows = [row[:] for row in matrix]
    size = len(rows)
    det = 1
    sign = 1
    for column in range(size):
        pivot = next((r for r in range(column, size) if rows[r][column] % p), None)
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            sign = -sign
        pivot_value = rows[column][column] % p
        det = (det * pivot_value) % p
        inverse = pow(pivot_value, -1, p)
        for r in range(column + 1, size):
            factor = (rows[r][column] * inverse) % p
            if factor:
                rows[r] = [
                    (entry - factor * pivot_entry) % p
                    for entry, pivot_entry in zip(rows[r], rows[column], strict=True)
                ]
    return (det * sign) % p


def vandermonde_denominator(roots: list[int], offset: int, p: int) -> int:
    matrix = [
        [pow(root, offset + row, p) for root in roots]
        for row in range(len(roots))
    ]
    return det_mod(matrix, p)


def support_minor(
    roots: list[int], syndrome: tuple[int, ...], offset: int, p: int
) -> int:
    j = len(roots)
    if j == 0:
        return syndrome[offset] % p
    matrix = [
        [pow(root, offset + row, p) for root in roots] + [syndrome[offset + row]]
        for row in range(j + 1)
    ]
    return det_mod(matrix, p)


def cramer_minor(
    roots: list[int], syndrome: tuple[int, ...], column: int, p: int
) -> int:
    j = len(roots)
    matrix = [[pow(root, row, p) for root in roots] for row in range(j)]
    for row in range(j):
        matrix[row][column] = syndrome[row]
    return det_mod(matrix, p)


def determinant_recurrence_passes(
    roots: list[int], syndrome: tuple[int, ...], D: int, p: int
) -> bool:
    j = len(roots)
    return all(support_minor(roots, syndrome, offset, p) == 0 for offset in range(D - j))


def cramer_guard_passes(roots: list[int], syndrome: tuple[int, ...], p: int) -> bool:
    if not roots:
        return True
    return all(
        cramer_minor(roots, syndrome, column, p) != 0
        for column in range(len(roots))
    )


def determinantal_support_atoms(
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
        if not determinant_recurrence_passes(roots, syndrome, D, p):
            continue
        if not cramer_guard_passes(roots, syndrome, p):
            continue
        scaled = recovered_scaled_amplitudes(roots, syndrome, p)
        atoms.add((tuple(error_support), tuple(value % p for value in scaled)))
    return atoms


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
        denominator_checks = []
        recurrence_checks = []
        cramer_checks = []
        for error_support in itertools.combinations(range(case.n), j):
            roots = [domain[index] for index in error_support]
            locator = monic_locator_coeffs(roots, case.p)
            denominator_checks.extend(
                vandermonde_denominator(roots, offset, case.p) != 0
                for offset in range(D - j)
            )
            determinant_ok = determinant_recurrence_passes(
                roots, target_syndrome, D, case.p
            )
            recurrence_ok = recurrence_passes(locator, target_syndrome, D, case.p)
            recurrence_checks.append(determinant_ok == recurrence_ok)
            if recurrence_ok:
                scaled = recovered_scaled_amplitudes(roots, target_syndrome, case.p)
                cramer_checks.append(
                    cramer_guard_passes(roots, target_syndrome, case.p)
                    == all(value % case.p != 0 for value in scaled)
                )

        determinantal_atoms = determinantal_support_atoms(
            p=case.p,
            n=case.n,
            j=j,
            D=D,
            domain=domain,
            syndrome=target_syndrome,
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
            "vandermonde_denominators_nonzero": all(denominator_checks),
            "determinants_match_recurrences": all(recurrence_checks),
            "cramer_minors_match_amplitude_guard": all(cramer_checks),
            "determinantal_support_count": len(determinantal_atoms),
            "guarded_hankel_divisor_count": len(hankel_atoms),
            "determinantal_equals_hankel": determinantal_atoms == hankel_atoms,
            "atoms": [
                {"support": list(support), "scaled_amplitudes": list(scaled)}
                for support, scaled in sorted(determinantal_atoms)
            ],
        }

    checks = {
        "all_vandermonde_denominators_nonzero": all(
            row["vandermonde_denominators_nonzero"] for row in shell_results.values()
        ),
        "all_determinants_match_recurrences": all(
            row["determinants_match_recurrences"] for row in shell_results.values()
        ),
        "all_cramer_minors_match_guards": all(
            row["cramer_minors_match_amplitude_guard"] for row in shell_results.values()
        ),
        "all_determinantal_shells_match_hankel": all(
            row["determinantal_equals_hankel"] for row in shell_results.values()
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
        },
        "domain": domain,
        "syndrome": list(target_syndrome),
        "shells": shell_results,
        "checks": checks,
        "all_passed": all(checks.values()),
    }


def build_report(cases: list[Case]) -> dict[str, Any]:
    results = [verify_case(case) for case in cases]
    return {
        "schema_version": "l1-determinantal-support-criterion-verifier-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "provenance": {
            "generator": "experimental/verify_l1_determinantal_support_criterion.py",
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
    print("L1 determinantal support criterion verifier")
    print(f"Status: {report['status']}")
    print(f"Cases: {report['summary']['cases']}")
    print(f"All passed: {report['summary']['all_passed']}")
    for result in report["results"]:
        case = result["case"]
        shell_bits = ", ".join(
            "a={a}: det={determinantal_support_count} hankel={guarded_hankel_divisor_count} passed={determinantal_equals_hankel}".format(
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
