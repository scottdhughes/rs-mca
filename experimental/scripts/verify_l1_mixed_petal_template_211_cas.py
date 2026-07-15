#!/usr/bin/env python3
"""Independent Singular/Macaulay2 audit for the ``(2,1,1)`` fixture.

The verifier imports neither the scanner nor the Sage census.  It rebuilds
all 1,200 full 9-by-8 and eliminated 6-by-5 affine systems over GF(17), sends
them to Singular and Macaulay2, and checks the frozen rank census.  It also
asks both systems to verify the universal maximal-minor identity

    det = (y-u)(y-v) = B_full(y),

which proves that the coefficient-rank-deficient locus is empty after
localizing to the disjoint-support chart.
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
CORE = tuple(range(5))
PETALS = tuple(tuple(range(5 + 2 * j, 7 + 2 * j)) for j in range(5))
SCALARS = (1, 2, 3, 4, 5)
EXPECTED = {
    "total": 1200,
    "full_rank8_augmented9": 1124,
    "full_rank_deficient": 0,
    "full_consistent": 76,
    "pair_rank5_augmented6": 1124,
    "pair_rank_deficient": 0,
    "pair_consistent": 76,
    "symbolic_minor_verified": 1,
    "symbolic_augmented_verified": 1,
}


@dataclass(frozen=True)
class Fibre:
    full: tuple[tuple[int, ...], ...]
    full_augmented: tuple[tuple[int, ...], ...]
    pair: tuple[tuple[int, ...], ...]
    pair_augmented: tuple[tuple[int, ...], ...]


def poly_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            out[i + j] = (out[i + j] + left_value * right_value) % P
    return tuple(out)


def locator(indices: tuple[int, ...]) -> tuple[int, ...]:
    out = (1,)
    for index in indices:
        out = poly_mul(out, ((-DOMAIN[index]) % P, 1))
    return out


def coefficient(poly: tuple[int, ...], degree: int) -> int:
    return poly[degree] if degree < len(poly) else 0


def support_templates() -> list[tuple[tuple[int, ...], ...]]:
    out = []
    for full_index in range(len(PETALS)):
        remaining = [index for index in range(len(PETALS)) if index != full_index]
        for singleton_indices in itertools.combinations(remaining, 2):
            for singleton_points in itertools.product(
                *(PETALS[index] for index in singleton_indices)
            ):
                supports = [tuple() for _ in PETALS]
                supports[full_index] = PETALS[full_index]
                for index, point in zip(
                    singleton_indices, singleton_points, strict=True
                ):
                    supports[index] = (point,)
                out.append(tuple(supports))
    if len(out) != 120 or len(set(out)) != 120:
        raise RuntimeError("outside-core template count drift")
    return out


def incidence_fibre(
    D: tuple[int, ...], supports: tuple[tuple[int, ...], ...]
) -> Fibre:
    F = locator(D)
    touched = [
        (scalar, locator(support), len(support))
        for scalar, support in zip(SCALARS, supports, strict=True)
        if support
    ]
    if len(touched) != 3 or sorted(size for _, _, size in touched) != [1, 1, 2]:
        raise RuntimeError("expected the labelled profile (2,1,1)")
    cofactor_degrees = [2 - size for _, _, size in touched]
    full_offsets = []
    pair_offsets = []
    next_full = 3
    next_pair = 0
    for degree in cofactor_degrees:
        full_offsets.append(next_full)
        pair_offsets.append(next_pair)
        next_full += degree + 1
        next_pair += degree + 1
    if next_full != 8 or next_pair != 5:
        raise RuntimeError("unknown-count drift")

    full_rows: list[tuple[int, ...]] = []
    full_rhs: list[int] = []
    for (scalar, B, _), degree, offset in zip(
        touched, cofactor_degrees, full_offsets, strict=True
    ):
        for row_degree in range(3):
            row = [int(row_degree == 0), int(row_degree == 1), int(row_degree == 2)] + [0] * 5
            for shift in range(degree + 1):
                source_degree = row_degree - shift
                if source_degree >= 0:
                    row[offset + shift] = (-coefficient(B, source_degree)) % P
            full_rows.append(tuple(row))
            full_rhs.append((scalar * coefficient(F, row_degree)) % P)

    pair_rows: list[tuple[int, ...]] = []
    pair_rhs: list[int] = []
    base_scalar, base_B, _ = touched[0]
    base_degree = cofactor_degrees[0]
    for index in (1, 2):
        scalar, B, _ = touched[index]
        degree = cofactor_degrees[index]
        for row_degree in range(3):
            row = [0] * 5
            for shift in range(base_degree + 1):
                source_degree = row_degree - shift
                if source_degree >= 0:
                    row[pair_offsets[0] + shift] = coefficient(
                        base_B, source_degree
                    )
            for shift in range(degree + 1):
                source_degree = row_degree - shift
                if source_degree >= 0:
                    row[pair_offsets[index] + shift] = (
                        -coefficient(B, source_degree)
                    ) % P
            pair_rows.append(tuple(value % P for value in row))
            pair_rhs.append(
                ((scalar - base_scalar) * coefficient(F, row_degree)) % P
            )

    full = tuple(full_rows)
    pair = tuple(pair_rows)
    return Fibre(
        full=full,
        full_augmented=tuple(
            row + (rhs,) for row, rhs in zip(full, full_rhs, strict=True)
        ),
        pair=pair,
        pair_augmented=tuple(
            row + (rhs,) for row, rhs in zip(pair, pair_rhs, strict=True)
        ),
    )


def fibres(*, omit_last: bool = False) -> list[Fibre]:
    out = [
        incidence_fibre(D, supports)
        for D in itertools.combinations(CORE, 2)
        for supports in support_templates()
    ]
    if omit_last:
        out.pop()
    return out


def matrix_payload_hash(items: list[Fibre]) -> str:
    payload = [
        {
            "A": fibre.full,
            "H": fibre.full_augmented,
            "P": fibre.pair,
            "Q": fibre.pair_augmented,
        }
        for fibre in items
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
        "int fullaug=0;",
        "int fullrankdef=0;",
        "int fullconsistent=0;",
        "int pairaug=0;",
        "int pairrankdef=0;",
        "int pairconsistent=0;",
    ]
    for index, fibre in enumerate(items):
        lines.extend(
            [
                f"matrix A{index}[9][8]={flat(fibre.full)};",
                f"matrix H{index}[9][9]={flat(fibre.full_augmented)};",
                f"matrix P{index}[6][5]={flat(fibre.pair)};",
                f"matrix Q{index}[6][6]={flat(fibre.pair_augmented)};",
                "total=total+1;",
                f"if(rank(A{index})<8){{fullrankdef=fullrankdef+1;}}",
                f"if(rank(A{index})==rank(H{index})){{fullconsistent=fullconsistent+1;}}",
                f"if(rank(A{index})==8 && rank(H{index})==9){{fullaug=fullaug+1;}}",
                f"if(rank(P{index})<5){{pairrankdef=pairrankdef+1;}}",
                f"if(rank(P{index})==rank(Q{index})){{pairconsistent=pairconsistent+1;}}",
                f"if(rank(P{index})==5 && rank(Q{index})==6){{pairaug=pairaug+1;}}",
            ]
        )
    lines.extend(
        [
            "ring s=0,(u,v,x,y,dj,dk,f0,f1),dp;",
            "matrix S[5][5]=-(u+v),-1,x,0,0,1,0,-1,0,0,u*v,0,0,y,0,-(u+v),0,0,-1,y,1,0,0,0,-1;",
            "int symbolic=(det(S)-(y-u)*(y-v)==0);",
            "matrix Z[6][6]=u*v,x,0,0,0,dj*f0,-(u+v),-1,x,0,0,dj*f1,1,0,-1,0,0,dj,u*v,0,0,y,0,dk*f0,-(u+v),0,0,-1,y,dk*f1,1,0,0,0,-1,dk;",
            "poly symbolicaug=dk*(y^2+f1*y+f0)*(x-u)*(x-v)-dj*(x^2+f1*x+f0)*(y-u)*(y-v);",
            "int augmented=(det(Z)-symbolicaug==0);",
            'print("TOTAL="+string(total));',
            'print("FULL_RANK8_AUGMENTED9="+string(fullaug));',
            'print("FULL_RANK_DEFICIENT="+string(fullrankdef));',
            'print("FULL_CONSISTENT="+string(fullconsistent));',
            'print("PAIR_RANK5_AUGMENTED6="+string(pairaug));',
            'print("PAIR_RANK_DEFICIENT="+string(pairrankdef));',
            'print("PAIR_CONSISTENT="+string(pairconsistent));',
            'print("SYMBOLIC_MINOR_VERIFIED="+string(symbolic));',
            'print("SYMBOLIC_AUGMENTED_VERIFIED="+string(augmented));',
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
        "fullaug=0;",
        "fullrankdef=0;",
        "fullconsistent=0;",
        "pairaug=0;",
        "pairrankdef=0;",
        "pairconsistent=0;",
    ]
    for fibre in items:
        lines.extend(
            [
                f"A={m2_matrix(fibre.full)};",
                f"H={m2_matrix(fibre.full_augmented)};",
                f"P={m2_matrix(fibre.pair)};",
                f"Q={m2_matrix(fibre.pair_augmented)};",
                "total=total+1;",
                "if rank A < 8 then fullrankdef=fullrankdef+1;",
                "if rank A == rank H then fullconsistent=fullconsistent+1;",
                "if rank A == 8 and rank H == 9 then fullaug=fullaug+1;",
                "if rank P < 5 then pairrankdef=pairrankdef+1;",
                "if rank P == rank Q then pairconsistent=pairconsistent+1;",
                "if rank P == 5 and rank Q == 6 then pairaug=pairaug+1;",
            ]
        )
    lines.extend(
        [
            "S=ZZ[u,v,x,y,dj,dk,f0,f1];",
            "T=matrix{{-(u+v),-1,x,0,0},{1,0,-1,0,0},{u*v,0,0,y,0},{-(u+v),0,0,-1,y},{1,0,0,0,-1}};",
            "symbolic=if det T == (y-u)*(y-v) then 1 else 0;",
            "Z=matrix{{u*v,x,0,0,0,dj*f0},{-(u+v),-1,x,0,0,dj*f1},{1,0,-1,0,0,dj},{u*v,0,0,y,0,dk*f0},{-(u+v),0,0,-1,y,dk*f1},{1,0,0,0,-1,dk}};",
            "symbolicaug=dk*(y^2+f1*y+f0)*(x-u)*(x-v)-dj*(x^2+f1*x+f0)*(y-u)*(y-v);",
            "augmented=if det Z == symbolicaug then 1 else 0;",
            'print("TOTAL=" | toString total);',
            'print("FULL_RANK8_AUGMENTED9=" | toString fullaug);',
            'print("FULL_RANK_DEFICIENT=" | toString fullrankdef);',
            'print("FULL_CONSISTENT=" | toString fullconsistent);',
            'print("PAIR_RANK5_AUGMENTED6=" | toString pairaug);',
            'print("PAIR_RANK_DEFICIENT=" | toString pairrankdef);',
            'print("PAIR_CONSISTENT=" | toString pairconsistent);',
            'print("SYMBOLIC_MINOR_VERIFIED=" | toString symbolic);',
            'print("SYMBOLIC_AUGMENTED_VERIFIED=" | toString augmented);',
            "exit 0",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_counts(output: str) -> dict[str, int]:
    mapping = {
        "TOTAL": "total",
        "FULL_RANK8_AUGMENTED9": "full_rank8_augmented9",
        "FULL_RANK_DEFICIENT": "full_rank_deficient",
        "FULL_CONSISTENT": "full_consistent",
        "PAIR_RANK5_AUGMENTED6": "pair_rank5_augmented6",
        "PAIR_RANK_DEFICIENT": "pair_rank_deficient",
        "PAIR_CONSISTENT": "pair_consistent",
        "SYMBOLIC_MINOR_VERIFIED": "symbolic_minor_verified",
        "SYMBOLIC_AUGMENTED_VERIFIED": "symbolic_augmented_verified",
    }
    found = {}
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
        raise RuntimeError(
            f"{label} failed with exit {completed.returncode}:\n{completed.stdout[-4000:]}"
        )
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
    missing = [
        name
        for name, path in (("Singular", singular), ("M2", macaulay2))
        if path is None
    ]
    if missing:
        raise RuntimeError("missing required CAS: " + ", ".join(missing))
    singular_counts = run_program([singular, "-q"], singular_program(items), "Singular")
    macaulay2_counts = run_macaulay2_program(
        macaulay2,
        macaulay2_program(items),
        "Macaulay2",
    )
    return {
        "schema": "rs-mca-l1-mixed-petal-template-211-cas-v1",
        "status": "EXPERIMENTAL/PIPELINE_CHECK",
        "matrix_payload_sha256": matrix_payload_hash(items),
        "singular": singular_counts,
        "macaulay2": macaulay2_counts,
        "cross_cas_equal": singular_counts == macaulay2_counts,
        "matches_expected": singular_counts == EXPECTED and macaulay2_counts == EXPECTED,
        "interpretation": (
            "all 1200 coefficient systems have full column rank; 76 are uniquely "
            "consistent and 1124 are inconsistent; the universal minor is B_full(y)"
        ),
        "nonclaims": [
            "does not count the moving-support compatibility hypersurface uniformly",
            "does not prove the full mixed-petal theorem",
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
            print("RESULT: FAIL (omitted-fibre mutation went undetected)")
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
        "[PASS] Singular=Macaulay2: 1200 full-rank systems, "
        "76 unique, 1124 inconsistent, universal minor/augmented identities verified"
    )
    print("RESULT: PASS (independent full/pair rank and symbolic-minor census)")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
