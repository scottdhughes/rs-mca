#!/usr/bin/env python3
"""Independent representative CAS replay for the ``(3,1,3,(2,2,2))`` frontier.

The full GF(19) census lives in ``analyze_l1_b9_frontier_31222.sage``.
This verifier deliberately does not import that analyzer.  It rebuilds two
compatible and two affine-inconsistent moving-monic-cubic systems from their
frozen support data, then asks Python modular elimination, Singular, and
Macaulay2 to agree on the ranks and representative minors.

For compatible rank drops it checks a nonzero 11 x 11 minor of ``C``.  For
inconsistent rank drops it checks a full 12 x 12 minor of ``[C|t*b]`` and the
factorization ``unit*t``.  This is a representative exact control, not a
generic saturation or a uniform theorem.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


P = 19
DOMAIN = (1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10)
CORE = (0, 1, 2, 3)
LABELS = (1, 2, 3)
PATTERNS = (
    {
        "name": "compatible-background-16",
        "background_support": (16,),
        "supports": ((4, 6), (8, 11), (13, 14)),
        "kind": "compatible",
        "expected_line": {"base": [0, 4, 4], "direction": [1, 1, 5]},
    },
    {
        "name": "compatible-background-17",
        "background_support": (17,),
        "supports": ((4, 7), (9, 10), (12, 15)),
        "kind": "compatible",
        "expected_line": {"base": [0, 17, 0], "direction": [1, 0, 9]},
    },
    {
        "name": "inconsistent-background-16",
        "background_support": (16,),
        "supports": ((4, 5), (8, 9), (13, 14)),
        "kind": "inconsistent",
    },
    {
        "name": "inconsistent-background-17",
        "background_support": (17,),
        "supports": ((4, 5), (8, 10), (12, 14)),
        "kind": "inconsistent",
    },
)
ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222/cas_certificate.json"
)


def poly_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] = (output[i + j] + a * b) % P
    return tuple(output)


def locator(indices: tuple[int, ...]) -> tuple[int, ...]:
    output = (1,)
    for index in indices:
        output = poly_mul(output, ((-DOMAIN[index]) % P, 1))
    return output


def shifted(poly: tuple[int, ...], degree: int) -> list[int]:
    output = [0] * 4
    for index, coefficient in enumerate(poly):
        if index + degree < 4:
            output[index + degree] = coefficient % P
    return output


def matrices(pattern: dict[str, object]) -> dict[str, tuple[tuple[int, ...], ...]]:
    R = locator(pattern["background_support"])
    support_locators = [locator(support) for support in pattern["supports"]]
    F = locator(CORE[:3])
    fixed_rows = []
    fixed_rhs = []
    moving_rows = []
    monic_rhs = []
    for block, (label, support_locator) in enumerate(
        zip(LABELS, support_locators, strict=True)
    ):
        columns = [shifted(R, degree) for degree in range(3)]
        for other_block in range(3):
            for degree in range(2):
                if other_block == block:
                    columns.append(
                        [(-entry) % P for entry in shifted(support_locator, degree)]
                    )
                else:
                    columns.append([0] * 4)
        if len(columns) != 9:
            raise RuntimeError("fixed coefficient-column count drift")
        for degree in range(4):
            fixed_row = tuple(column[degree] for column in columns)
            fixed_rows.append(fixed_row)
            fixed_rhs.append(label * F[degree] % P)
            moving_rows.append(
                fixed_row
                + tuple(
                    (-label) % P if degree == lower_degree else 0
                    for lower_degree in range(3)
                )
            )
            monic_rhs.append(label if degree == 3 else 0)
    return {
        "fixed": tuple(fixed_rows),
        "fixed_augmented": tuple(
            row + (rhs,) for row, rhs in zip(fixed_rows, fixed_rhs, strict=True)
        ),
        "moving": tuple(moving_rows),
        "moving_augmented": tuple(
            row + (rhs,) for row, rhs in zip(moving_rows, monic_rhs, strict=True)
        ),
    }


def inverse_mod(value: int) -> int:
    return pow(value % P, P - 2, P)


def rref_mod(rows: tuple[tuple[int, ...], ...]) -> tuple[list[list[int]], list[int]]:
    work = [[entry % P for entry in row] for row in rows]
    pivots = []
    rank = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inverse_mod(work[rank][column])
        work[rank] = [(scale * entry) % P for entry in work[rank]]
        for index in range(len(work)):
            if index == rank or work[index][column] == 0:
                continue
            scale = work[index][column]
            work[index] = [
                (left - scale * right) % P
                for left, right in zip(work[index], work[rank], strict=True)
            ]
        pivots.append(column)
        rank += 1
        if rank == len(work):
            break
    return work, pivots


def rank_mod(rows: tuple[tuple[int, ...], ...]) -> int:
    return len(rref_mod(rows)[1])


def pivot_columns_mod(rows: tuple[tuple[int, ...], ...]) -> list[int]:
    return rref_mod(rows)[1]


def transpose(rows: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row[column] for row in rows) for column in range(len(rows[0])))


def det_mod(rows: tuple[tuple[int, ...], ...]) -> int:
    work = [[entry % P for entry in row] for row in rows]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            (index for index in range(column, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % P
        inverse = inverse_mod(pivot_value)
        for index in range(column + 1, len(work)):
            scale = work[index][column] * inverse % P
            for inner in range(column, len(work)):
                work[index][inner] = (
                    work[index][inner] - scale * work[column][inner]
                ) % P
    return determinant % P


def normalize_direction(values: list[int]) -> list[int]:
    first = next(value % P for value in values if value % P)
    inverse = inverse_mod(first)
    return [value * inverse % P for value in values]


def affine_lower_line(payload: dict[str, tuple]) -> dict[str, list[int]] | None:
    augmented = payload["moving_augmented"]
    reduced, pivots = rref_mod(augmented)
    variable_count = len(augmented[0]) - 1
    if variable_count in pivots:
        return None
    pivot_variables = [column for column in pivots if column < variable_count]
    free = [column for column in range(variable_count) if column not in pivot_variables]
    if len(free) != 1:
        raise RuntimeError(f"expected one affine parameter, found {free}")
    free_column = free[0]
    particular = [0] * variable_count
    direction = [0] * variable_count
    direction[free_column] = 1
    pivot_row = {column: row for row, column in enumerate(pivots)}
    for column in pivot_variables:
        row = pivot_row[column]
        particular[column] = reduced[row][variable_count]
        direction[column] = -reduced[row][free_column] % P
    points = sorted(
        {
            tuple((particular[index] + scale * direction[index]) % P for index in range(9, 12))
            for scale in range(P)
        }
    )
    if len(points) != P:
        raise RuntimeError("lower cubic coefficients do not form an affine line")
    base = points[0]
    other = next(point for point in points[1:] if point != base)
    lower_direction = normalize_direction(
        [(right - left) % P for left, right in zip(base, other, strict=True)]
    )
    return {"base": list(base), "direction": lower_direction}


def representative_minor(payload: dict[str, tuple], kind: str) -> dict[str, object]:
    if kind == "compatible":
        rows = pivot_columns_mod(transpose(payload["moving"]))
        columns = pivot_columns_mod(payload["moving"])
        if len(rows) != 11 or len(columns) != 11:
            raise RuntimeError("compatible rank-drop minor has wrong size")
        square = tuple(
            tuple(payload["moving"][row][column] for column in columns)
            for row in rows
        )
        coefficient = det_mod(square)
        if coefficient == 0:
            raise RuntimeError("compatible witness minor vanished")
        return {
            "kind": "nonzero_11x11_C_minor",
            "rows_zero_based": rows,
            "columns_zero_based": columns,
            "unit_coefficient_mod_19": coefficient,
            "factorization": str(coefficient),
        }
    pivots = pivot_columns_mod(payload["moving_augmented"])
    if len(pivots) != 12 or 12 not in pivots:
        raise RuntimeError("inconsistent witness must use the monic RHS column")
    square = tuple(
        tuple(row[column] for column in pivots)
        for row in payload["moving_augmented"]
    )
    coefficient = det_mod(square)
    if coefficient == 0:
        raise RuntimeError("inconsistent augmented witness minor vanished")
    return {
        "kind": "nonzero_12x12_augmented_minor",
        "rows_zero_based": list(range(12)),
        "columns_zero_based": pivots,
        "unit_coefficient_mod_19": coefficient,
        "factorization": f"{coefficient}*t",
    }


def flat(rows: tuple[tuple[int, ...], ...]) -> str:
    return ",".join(str(entry) for row in rows for entry in row)


def witness_entries(payload: dict[str, tuple], witness: dict[str, object]) -> list[str]:
    source = payload["moving"] if witness["kind"].startswith("nonzero_11") else payload["moving_augmented"]
    entries = []
    for row in witness["rows_zero_based"]:
        for column in witness["columns_zero_based"]:
            entry = str(source[row][column])
            if witness["kind"].startswith("nonzero_12") and column == 12:
                entry = f"({entry})*t"
            entries.append(entry)
    return entries


def singular_program(payloads, witnesses) -> str:
    lines = ["ring r=19,(t),dp;"]
    for index, (payload, witness) in enumerate(zip(payloads, witnesses, strict=True)):
        size = len(witness["rows_zero_based"])
        expected = witness["factorization"]
        lines.extend(
            [
                f"matrix A{index}[12][9]={flat(payload['fixed'])};",
                f"matrix H{index}[12][10]={flat(payload['fixed_augmented'])};",
                f"matrix C{index}[12][12]={flat(payload['moving'])};",
                f"matrix D{index}[12][13]={flat(payload['moving_augmented'])};",
                f"matrix W{index}[{size}][{size}]={','.join(witness_entries(payload, witness))};",
                f'print("CASE{index}_FIXED="+string(rank(A{index}))+","+string(rank(H{index})));',
                f'print("CASE{index}_MOVING="+string(rank(C{index}))+","+string(rank(D{index})));',
                f'print("CASE{index}_WITNESS="+string(det(W{index})=={expected}));',
            ]
        )
    lines.extend(["quit;", ""])
    return "\n".join(lines)


def m2_matrix(rows: tuple[tuple[int, ...], ...], ring: str) -> str:
    encoded = [
        "{" + ",".join(f"{entry}_{ring}" for entry in row) + "}" for row in rows
    ]
    return "matrix{" + ",".join(encoded) + "}"


def m2_witness_matrix(payload, witness) -> str:
    source = payload["moving"] if witness["kind"].startswith("nonzero_11") else payload["moving_augmented"]
    encoded = []
    for row in witness["rows_zero_based"]:
        entries = []
        for column in witness["columns_zero_based"]:
            entry = f"{source[row][column]}_S"
            if witness["kind"].startswith("nonzero_12") and column == 12:
                entry = f"({entry})*t"
            entries.append(entry)
        encoded.append("{" + ",".join(entries) + "}")
    return "matrix{" + ",".join(encoded) + "}"


def macaulay2_program(payloads, witnesses) -> str:
    lines = ["R=GF(19);"]
    for index, payload in enumerate(payloads):
        lines.extend(
            [
                f"A={m2_matrix(payload['fixed'], 'R')};",
                f"H={m2_matrix(payload['fixed_augmented'], 'R')};",
                f"C={m2_matrix(payload['moving'], 'R')};",
                f"D={m2_matrix(payload['moving_augmented'], 'R')};",
                f'print("CASE{index}_FIXED=" | toString rank A | "," | toString rank H);',
                f'print("CASE{index}_MOVING=" | toString rank C | "," | toString rank D);',
            ]
        )
    lines.append("S=GF(19)[t];")
    for index, (payload, witness) in enumerate(zip(payloads, witnesses, strict=True)):
        expected = witness["factorization"].replace("*t", "_S*t")
        if "*t" not in witness["factorization"]:
            expected += "_S"
        lines.extend(
            [
                f"W={m2_witness_matrix(payload, witness)};",
                f'print("CASE{index}_WITNESS=" | if det W == {expected} then "1" else "0");',
            ]
        )
    lines.extend(["exit 0", ""])
    return "\n".join(lines)


def parse_output(output: str, count: int, witnesses) -> list[dict[str, object]]:
    results = []
    for index in range(count):
        fixed = re.findall(rf"CASE{index}_FIXED=(\d+),(\d+)", output)
        moving = re.findall(rf"CASE{index}_MOVING=(\d+),(\d+)", output)
        verified = re.findall(rf"CASE{index}_WITNESS=(\d+)", output)
        if not fixed or not moving or not verified:
            raise RuntimeError(f"missing CASE{index} data in CAS output:\n{output[-2000:]}")
        results.append(
            {
                "fixed": {"rank": int(fixed[-1][0]), "augmented_rank": int(fixed[-1][1])},
                "moving": {"rank": int(moving[-1][0]), "augmented_rank": int(moving[-1][1])},
                "representative_minor": {**witnesses[index], "identity_verified": verified[-1] == "1"},
            }
        )
    return results


def run_program(command, program, label, count, witnesses):
    try:
        completed = subprocess.run(
            command,
            input=program,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=60,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"{label} exceeded 60 seconds") from error
    if completed.returncode != 0:
        raise RuntimeError(f"{label} failed:\n{completed.stdout[-4000:]}")
    return parse_output(completed.stdout, count, witnesses)


def run_macaulay2_program(executable, program, count, witnesses):
    """Run a large M2 payload from a script file instead of a stdin pipe.

    Macaulay2 does not consume this verifier's matrix payload promptly from a
    pipe on every supported runtime, which can block ``communicate`` before
    its timeout becomes effective.  ``--script`` reads the same program from
    disk and implies the noninteractive flags needed by the replay.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".m2", encoding="utf-8"
    ) as script:
        script.write(program)
        script.flush()
        return run_program(
            [executable, "--script", script.name],
            None,
            "Macaulay2",
            count,
            witnesses,
        )


def expected_moving(kind: str) -> dict[str, int]:
    return {"rank": 11, "augmented_rank": 11 if kind == "compatible" else 12}


def build_report() -> dict[str, object]:
    singular = shutil.which("Singular")
    macaulay2 = shutil.which("M2")
    if singular is None or macaulay2 is None:
        raise RuntimeError("Singular and Macaulay2 are both required")
    payloads = [matrices(pattern) for pattern in PATTERNS]
    witnesses = [
        representative_minor(payload, pattern["kind"])
        for payload, pattern in zip(payloads, PATTERNS, strict=True)
    ]
    python_results = []
    for payload, witness in zip(payloads, witnesses, strict=True):
        python_results.append(
            {
                "fixed": {"rank": rank_mod(payload["fixed"]), "augmented_rank": rank_mod(payload["fixed_augmented"])},
                "moving": {"rank": rank_mod(payload["moving"]), "augmented_rank": rank_mod(payload["moving_augmented"])},
                "representative_minor": {**witness, "identity_verified": True},
            }
        )
    singular_results = run_program(
        [singular, "-q"], singular_program(payloads, witnesses), "Singular", len(payloads), witnesses
    )
    macaulay2_results = run_macaulay2_program(
        macaulay2,
        macaulay2_program(payloads, witnesses),
        len(payloads),
        witnesses,
    )
    affine_lines = []
    for pattern, payload in zip(PATTERNS, payloads, strict=True):
        line = affine_lower_line(payload)
        affine_lines.append({"name": pattern["name"], "line": line})
    encoded = json.dumps(payloads, sort_keys=True, separators=(",", ":"))
    return {
        "schema": "rs-mca-l1-b9-frontier-31222-cas-v1",
        "status": "AUDIT/EXACT_REPRESENTATIVE_CAS_REPLAY",
        "statement": "independently verify the two compatible and two affine-inconsistent GF(19) moving-cubic rank drops without generic saturation",
        "input": {
            "field": "GF(19)",
            "fixed_matrix_shape": [12, 9],
            "moving_matrix_shape": [12, 12],
            "patterns": [
                {
                    "name": pattern["name"],
                    "kind": pattern["kind"],
                    "background_support": list(pattern["background_support"]),
                    "petal_supports": [list(support) for support in pattern["supports"]],
                }
                for pattern in PATTERNS
            ],
        },
        "results": {
            "python_modular_elimination": python_results,
            "singular": singular_results,
            "macaulay2": macaulay2_results,
            "python_affine_lower_coefficient_lines": affine_lines,
        },
        "certificate": {
            "matrix_payload_sha256": hashlib.sha256(encoded.encode("ascii")).hexdigest(),
            "engines": {"Singular": singular, "Macaulay2": macaulay2},
        },
        "proof_status": {
            "exact": "three independent exact engines agree on the representative ranks and minors",
            "uniform": "unproved; the two compatible rank-drop lines remain UNPAID_RANKDROP_TEMPLATE",
        },
        "verdict": "YELLOW_REPRESENTATIVE_CONTROL_ONLY",
    }


def validate_report(report: dict[str, object]) -> bool:
    if report.get("schema") != "rs-mca-l1-b9-frontier-31222-cas-v1":
        return False
    engine_results = report["results"]
    for engine in ("python_modular_elimination", "singular", "macaulay2"):
        for pattern, result in zip(PATTERNS, engine_results[engine], strict=True):
            if result["fixed"] != {"rank": 9, "augmented_rank": 10}:
                return False
            if result["moving"] != expected_moving(pattern["kind"]):
                return False
            if not result["representative_minor"]["identity_verified"]:
                return False
    lines = engine_results["python_affine_lower_coefficient_lines"]
    for pattern, record in zip(PATTERNS, lines, strict=True):
        expected = pattern.get("expected_line")
        if record["line"] != expected:
            return False
    return report.get("verdict") == "YELLOW_REPRESENTATIVE_CONTROL_ONLY"


def tamper_selftest(report: dict[str, object]) -> int:
    mutations = []
    for engine in ("python_modular_elimination", "singular", "macaulay2"):
        changed = copy.deepcopy(report)
        changed["results"][engine][0]["moving"]["rank"] += 1
        mutations.append((f"{engine}_rank", changed))
        changed = copy.deepcopy(report)
        changed["results"][engine][0]["representative_minor"]["identity_verified"] = False
        mutations.append((f"{engine}_minor", changed))
    changed = copy.deepcopy(report)
    changed["results"]["python_affine_lower_coefficient_lines"][0]["line"]["direction"][0] += 1
    mutations.append(("affine_line", changed))
    failed = False
    for name, changed in mutations:
        caught = not validate_report(changed)
        print(f"  tamper {name:<34}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (representative CAS replay drift)", file=sys.stderr)
        return 1
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != report:
        print("RESULT: FAIL (frozen CAS certificate drift)", file=sys.stderr)
        return 1
    print("l1 B9 frontier (3,1,3,(2,2,2)) representative CAS replay")
    print("  patterns: two compatible and two affine-inconsistent rank drops")
    print("  engines: Python modular elimination, Singular, Macaulay2")
    print(f"  matrix payload: {report['certificate']['matrix_payload_sha256']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
