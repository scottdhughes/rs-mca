#!/usr/bin/env python3
"""Independent Singular/Macaulay2 rank census for the (2,2,1) fixture.

This verifier does not import the scanner or the Sage census.  It rebuilds
the fixed-support incidence matrices over GF(17) from the frozen evaluation
domain, sends all 1,701 labelled-profile matrices to each CAS, and checks that
every coefficient matrix has full column rank.  Seven augmented systems have
the same rank and the other 1,694 gain one rank:

    rank(A) = 7,  rank([A|b]) in {7,8}.

Thus seven fixed-support fibres have a unique solution, 1,694 are empty, and
the rank-deficient fixed-support locus is empty.  This is a toy compatibility
calculation, not an asymptotic B11 theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass


P = 17
DOMAIN = (1, 3, 9, 10, 13, 5, 15, 11, 16, 14, 8, 7, 4, 12, 2, 6)
CORE = tuple(range(7))
PETALS = (
    tuple(range(7, 10)),
    tuple(range(10, 13)),
    tuple(range(13, 16)),
)
EXPECTED = {
    "total": 1701,
    "rank7_augmented8": 1694,
    "coefficient_rank_deficient": 0,
    "consistent": 7,
    "other": 7,
}


@dataclass(frozen=True)
class Fibre:
    coefficient: tuple[tuple[int, ...], ...]
    augmented: tuple[tuple[int, ...], ...]


def poly_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % P
    return tuple(out)


def locator(indices: tuple[int, ...]) -> tuple[int, ...]:
    out = (1,)
    for index in indices:
        out = poly_mul(out, ((-DOMAIN[index]) % P, 1))
    return out


def neg_coeff(poly: tuple[int, ...], degree: int) -> int:
    return (-poly[degree]) % P if degree < len(poly) else 0


def incidence_fibre(
    D: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> Fibre:
    F = locator(D)
    locators = [locator(support) for support in supports]
    cofactor_degrees = [2 - len(support) for support in supports]
    offsets = []
    next_column = 3
    for degree in cofactor_degrees:
        offsets.append(next_column)
        next_column += degree + 1
    if next_column != 7:
        raise RuntimeError("profile should have exactly seven incidence unknowns")
    rows: list[tuple[int, ...]] = []
    rhs: list[int] = []
    for scalar, B, cofactor_degree, offset in zip(
        (1, 2, 3), locators, cofactor_degrees, offsets, strict=True
    ):
        for degree in range(3):
            row = [int(degree == 0), int(degree == 1), int(degree == 2)] + [0] * 4
            for shift in range(cofactor_degree + 1):
                source_degree = degree - shift
                row[offset + shift] = (
                    neg_coeff(B, source_degree) if source_degree >= 0 else 0
                )
            rows.append(tuple(row))
            rhs.append((scalar * F[degree]) % P)
    coefficient = tuple(rows)
    augmented = tuple(row + (entry,) for row, entry in zip(rows, rhs, strict=True))
    return Fibre(coefficient=coefficient, augmented=augmented)


def fibres(*, omit_last: bool = False) -> list[Fibre]:
    out = []
    for D in itertools.combinations(CORE, 2):
        for sizes in sorted(set(itertools.permutations((2, 2, 1)))):
            support_iterators = [
                itertools.combinations(petal, size)
                for petal, size in zip(PETALS, sizes, strict=True)
            ]
            for supports in itertools.product(*support_iterators):
                out.append(incidence_fibre(D, supports))
    if omit_last:
        out.pop()
    return out


def matrix_payload_hash(items: list[Fibre]) -> str:
    payload = [
        {"A": fibre.coefficient, "H": fibre.augmented} for fibre in items
    ]
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def flat(matrix: tuple[tuple[int, ...], ...]) -> str:
    return ",".join(str(entry) for row in matrix for entry in row)


def singular_program(items: list[Fibre]) -> str:
    lines = [
        "ring r=17,(x),dp;",
        "int total=0;",
        "int rank7aug8=0;",
        "int rankdef=0;",
        "int consistent=0;",
        "int other=0;",
    ]
    for index, fibre in enumerate(items):
        lines.extend(
            [
                f"matrix A{index}[9][7]={flat(fibre.coefficient)};",
                f"matrix H{index}[9][8]={flat(fibre.augmented)};",
                "total=total+1;",
                f"if(rank(A{index})<7){{rankdef=rankdef+1;}}",
                f"if(rank(A{index})==rank(H{index})){{consistent=consistent+1;}}",
                (
                    f"if(rank(A{index})==7 && rank(H{index})==8)"
                    "{rank7aug8=rank7aug8+1;}else{other=other+1;}"
                ),
            ]
        )
    lines.extend(
        [
            'print("TOTAL="+string(total));',
            'print("RANK7_AUGMENTED8="+string(rank7aug8));',
            'print("COEFFICIENT_RANK_DEFICIENT="+string(rankdef));',
            'print("CONSISTENT="+string(consistent));',
            'print("OTHER="+string(other));',
            "quit;",
        ]
    )
    return "\n".join(lines) + "\n"


def m2_matrix(matrix: tuple[tuple[int, ...], ...]) -> str:
    rows = ["{" + ",".join(f"{entry}_R" for entry in row) + "}" for row in matrix]
    return "matrix{" + ",".join(rows) + "}"


def macaulay2_program(items: list[Fibre]) -> str:
    lines = [
        "R=GF(17);",
        "total=0;",
        "rank7aug8=0;",
        "rankdef=0;",
        "consistent=0;",
        "other=0;",
    ]
    for fibre in items:
        lines.extend(
            [
                f"A={m2_matrix(fibre.coefficient)};",
                f"H={m2_matrix(fibre.augmented)};",
                "total=total+1;",
                "if rank A < 7 then rankdef=rankdef+1;",
                "if rank A == rank H then consistent=consistent+1;",
                (
                    "if rank A == 7 and rank H == 8 "
                    "then rank7aug8=rank7aug8+1 else other=other+1;"
                ),
            ]
        )
    lines.extend(
        [
            'print("TOTAL=" | toString total);',
            'print("RANK7_AUGMENTED8=" | toString rank7aug8);',
            'print("COEFFICIENT_RANK_DEFICIENT=" | toString rankdef);',
            'print("CONSISTENT=" | toString consistent);',
            'print("OTHER=" | toString other);',
            "exit 0",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_counts(output: str) -> dict[str, int]:
    mapping = {
        "TOTAL": "total",
        "RANK7_AUGMENTED8": "rank7_augmented8",
        "COEFFICIENT_RANK_DEFICIENT": "coefficient_rank_deficient",
        "CONSISTENT": "consistent",
        "OTHER": "other",
    }
    found: dict[str, int] = {}
    for external, internal in mapping.items():
        matches = re.findall(rf"{external}=(\d+)", output)
        if not matches:
            raise RuntimeError(f"missing {external} in CAS output")
        found[internal] = int(matches[-1])
    return found


def run_program(
    command: list[str], program: str | None, label: str
) -> dict[str, int]:
    completed = subprocess.run(
        command,
        input=program,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        tail = completed.stdout[-4000:]
        raise RuntimeError(f"{label} failed with exit {completed.returncode}:\n{tail}")
    return parse_counts(completed.stdout)


def run_macaulay2_program(
    executable: str, program: str, label: str
) -> dict[str, int]:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".m2", encoding="utf-8"
    ) as script:
        script.write(program)
        script.flush()
        return run_program(
            [executable, "--script", script.name], None, label
        )


def verify(*, omit_last: bool = False) -> dict[str, object]:
    items = fibres(omit_last=omit_last)
    singular = shutil.which("Singular")
    macaulay2 = shutil.which("M2")
    if singular is None or macaulay2 is None:
        missing = [name for name, path in (("Singular", singular), ("M2", macaulay2)) if path is None]
        raise RuntimeError("missing required CAS: " + ", ".join(missing))
    singular_counts = run_program([singular, "-q"], singular_program(items), "Singular")
    macaulay2_counts = run_macaulay2_program(
        macaulay2,
        macaulay2_program(items),
        "Macaulay2",
    )
    return {
        "schema": "rs-mca-l1-mixed-petal-template-221-cas-v2",
        "status": "EXPERIMENTAL/PIPELINE_CHECK",
        "matrix_payload_sha256": matrix_payload_hash(items),
        "singular": singular_counts,
        "macaulay2": macaulay2_counts,
        "cross_cas_equal": singular_counts == macaulay2_counts,
        "matches_expected": singular_counts == EXPECTED and macaulay2_counts == EXPECTED,
        "interpretation": (
            "all fixed-support coefficient matrices have full column rank; "
            "seven systems have unique solutions, 1694 are inconsistent, "
            "and the rank-deficient fixed-support locus is empty"
        ),
        "nonclaims": [
            "does not compute a symbolic asymptotic determinantal stratification",
            "does not prove quotient descent, periodicity, or Johnson coverage",
            "does not close B11",
        ],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.tamper_selftest:
        tampered = verify(omit_last=True)
        if tampered["matches_expected"]:
            print("RESULT: FAIL (omitted-fibre tamper went undetected)")
            return 1
        print("[PASS] omitted-fibre mutation rejected by both frozen counts")
        print("RESULT: PASS (CAS rank-census tamper self-test)")
        return 0
    report = verify()
    if not report["cross_cas_equal"] or not report["matches_expected"]:
        print(json.dumps(report, indent=2, sort_keys=True))
        print("RESULT: FAIL (CAS rank-census drift)")
        return 1
    print(
        "[PASS] Singular=Macaulay2: total=1701, rank(A)=7 throughout, "
        "7 unique and 1694 inconsistent fibres"
    )
    print("RESULT: PASS (independent fixed-support rank census)")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
