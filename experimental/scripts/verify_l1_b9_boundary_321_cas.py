#!/usr/bin/env python3
"""Independent CAS replay for the two GF(19) boundary-321 rank drops.

This verifier rebuilds only the two moving-monic-quartic systems isolated by
``analyze_l1_b9_boundary_321.sage``.  It does not import that analyzer.  Python
modular elimination, Singular, and Macaulay2 must all report

    rank(C)=14,  rank([C|b_monic])=15,

while the corresponding fixed-core systems report ``(12,13)``.  For each
exceptional chart it also selects a nonzero augmented ``15 x 15`` minor after
scaling the monic column by ``t`` and verifies the representative factorization
``determinant = unit*t``.  This is not a generic saturation or theorem.
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
BACKGROUND = (16, 17)
LABELS = (1, 2, 3)
EXCEPTIONAL = (
    {
        "sizes": (3, 1, 2),
        "supports": ((4, 5, 6), (8,), (13, 15)),
    },
    {
        "sizes": (1, 3, 2),
        "supports": ((4,), (8, 9, 10), (12, 13)),
    },
)
EXPECTED_FIXED = {"rank": 12, "augmented_rank": 13}
EXPECTED_MOVING = {"rank": 14, "augmented_rank": 15}
ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-boundary-321/cas_certificate.json"
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
    output = [0] * 5
    for index, coefficient in enumerate(poly):
        if index + degree < 5:
            output[index + degree] = coefficient % P
    return output


def matrices(pattern: dict[str, tuple]) -> dict[str, tuple[tuple[int, ...], ...]]:
    sizes = pattern["sizes"]
    supports = pattern["supports"]
    F = locator(CORE)
    R = locator(BACKGROUND)
    support_locators = [locator(tuple(support)) for support in supports]
    block_columns: list[list[list[int]]] = []
    for block, (support_locator, size) in enumerate(
        zip(support_locators, sizes, strict=True)
    ):
        columns = [shifted(R, degree) for degree in range(3)]
        for other_block, other_size in enumerate(sizes):
            for degree in range(5 - other_size):
                if other_block == block:
                    columns.append(
                        [(-entry) % P for entry in shifted(support_locator, degree)]
                    )
                else:
                    columns.append([0] * 5)
        if len(columns) != 12:
            raise RuntimeError("coefficient-column count drift")
        block_columns.append(columns)

    fixed_rows = []
    fixed_rhs = []
    moving_rows = []
    monic_rhs = []
    for block, label in enumerate(LABELS):
        for degree in range(5):
            fixed_row = tuple(column[degree] for column in block_columns[block])
            fixed_rows.append(fixed_row)
            fixed_rhs.append(label * F[degree] % P)
            moving_rows.append(
                fixed_row
                + tuple(
                    (-label) % P if degree == lower_degree else 0
                    for lower_degree in range(4)
                )
            )
            monic_rhs.append(label if degree == 4 else 0)
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


def rank_mod(rows: tuple[tuple[int, ...], ...]) -> int:
    work = [[entry % P for entry in row] for row in rows]
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
        rank += 1
    return rank


def pivot_columns_mod(rows: tuple[tuple[int, ...], ...]) -> list[int]:
    work = [[entry % P for entry in row] for row in rows]
    pivots: list[int] = []
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
    return pivots


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


def augmented_minor_witness(payload: dict[str, tuple]) -> dict[str, object]:
    pivots = pivot_columns_mod(payload["moving_augmented"])
    if len(pivots) != 15 or 16 not in pivots:
        raise RuntimeError("expected a full augmented minor using the monic column")
    square = tuple(
        tuple(row[column] for column in pivots)
        for row in payload["moving_augmented"]
    )
    coefficient = det_mod(square)
    if coefficient == 0:
        raise RuntimeError("selected augmented witness minor vanished")
    return {
        "pivot_columns_zero_based": pivots,
        "unit_coefficient_mod_19": coefficient,
        "factorization": f"{coefficient}*t",
    }


def flat(rows: tuple[tuple[int, ...], ...]) -> str:
    return ",".join(str(entry) for row in rows for entry in row)


def singular_minor_matrix(
    payload: dict[str, tuple], witness: dict[str, object]
) -> str:
    columns = witness["pivot_columns_zero_based"]
    entries = []
    for row in payload["moving_augmented"]:
        for column in columns:
            entry = str(row[column])
            entries.append(f"({entry})*t" if column == 16 else entry)
    return ",".join(entries)


def singular_program(
    payloads: list[dict[str, tuple]], witnesses: list[dict[str, object]]
) -> str:
    lines = ["ring r=19,(t),dp;"]
    for index, (payload, witness) in enumerate(
        zip(payloads, witnesses, strict=True)
    ):
        lines.extend(
            [
                f"matrix A{index}[15][12]={flat(payload['fixed'])};",
                f"matrix H{index}[15][13]={flat(payload['fixed_augmented'])};",
                f"matrix C{index}[15][16]={flat(payload['moving'])};",
                f"matrix D{index}[15][17]={flat(payload['moving_augmented'])};",
                f"matrix W{index}[15][15]={singular_minor_matrix(payload, witness)};",
                f'print("CASE{index}_FIXED="+string(rank(A{index}))+","+string(rank(H{index})));',
                f'print("CASE{index}_MOVING="+string(rank(C{index}))+","+string(rank(D{index})));',
                f'print("CASE{index}_WITNESS="+string(det(W{index})=={witness["unit_coefficient_mod_19"]}*t));',
            ]
        )
    lines.extend(["quit;", ""])
    return "\n".join(lines)


def m2_matrix(rows: tuple[tuple[int, ...], ...]) -> str:
    encoded = [
        "{" + ",".join(f"{entry}_R" for entry in row) + "}" for row in rows
    ]
    return "matrix{" + ",".join(encoded) + "}"


def m2_minor_matrix(
    payload: dict[str, tuple], witness: dict[str, object]
) -> str:
    columns = witness["pivot_columns_zero_based"]
    encoded = []
    for row in payload["moving_augmented"]:
        entries = []
        for column in columns:
            entry = f"{row[column]}_S"
            entries.append(f"({entry})*t" if column == 16 else entry)
        encoded.append("{" + ",".join(entries) + "}")
    return "matrix{" + ",".join(encoded) + "}"


def macaulay2_program(
    payloads: list[dict[str, tuple]], witnesses: list[dict[str, object]]
) -> str:
    lines = ["R=GF(19);"]
    for index, payload in enumerate(payloads):
        lines.extend(
            [
                f"A={m2_matrix(payload['fixed'])};",
                f"H={m2_matrix(payload['fixed_augmented'])};",
                f"C={m2_matrix(payload['moving'])};",
                f"D={m2_matrix(payload['moving_augmented'])};",
                f'print("CASE{index}_FIXED=" | toString rank A | "," | toString rank H);',
                f'print("CASE{index}_MOVING=" | toString rank C | "," | toString rank D);',
            ]
        )
    lines.append("S=GF(19)[t];")
    for index, (payload, witness) in enumerate(
        zip(payloads, witnesses, strict=True)
    ):
        lines.extend(
            [
                f"W={m2_minor_matrix(payload, witness)};",
                f'print("CASE{index}_WITNESS=" | if det W == {witness["unit_coefficient_mod_19"]}_S*t then "1" else "0");',
            ]
        )
    lines.extend(["exit 0", ""])
    return "\n".join(lines)


def parse_output(
    output: str,
    case_count: int,
    witnesses: list[dict[str, object]],
) -> list[dict[str, object]]:
    results = []
    for index in range(case_count):
        fixed = re.findall(rf"CASE{index}_FIXED=(\d+),(\d+)", output)
        moving = re.findall(rf"CASE{index}_MOVING=(\d+),(\d+)", output)
        witness = re.findall(rf"CASE{index}_WITNESS=(\d+)", output)
        if not fixed or not moving or not witness:
            raise RuntimeError(f"missing CASE{index} ranks in CAS output")
        results.append(
            {
                "fixed": {
                    "rank": int(fixed[-1][0]),
                    "augmented_rank": int(fixed[-1][1]),
                },
                "moving": {
                    "rank": int(moving[-1][0]),
                    "augmented_rank": int(moving[-1][1]),
                },
                "augmented_minor_factorization": {
                    **witnesses[index],
                    "identity_verified": witness[-1] == "1",
                },
            }
        )
    return results


def run_program(
    command: list[str],
    program: str | None,
    label: str,
    count: int,
    witnesses: list[dict[str, object]],
):
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
        raise RuntimeError(
            f"{label} failed with exit {completed.returncode}:\n{completed.stdout[-4000:]}"
        )
    return parse_output(completed.stdout, count, witnesses)


def run_macaulay2_program(
    executable: str,
    program: str,
    count: int,
    witnesses: list[dict[str, object]],
):
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


def build_report():
    singular = shutil.which("Singular")
    macaulay2 = shutil.which("M2")
    if singular is None or macaulay2 is None:
        raise RuntimeError("Singular and Macaulay2 are both required")
    payloads = [matrices(pattern) for pattern in EXCEPTIONAL]
    witnesses = [augmented_minor_witness(payload) for payload in payloads]
    python_results = [
        {
            "fixed": {
                "rank": rank_mod(payload["fixed"]),
                "augmented_rank": rank_mod(payload["fixed_augmented"]),
            },
            "moving": {
                "rank": rank_mod(payload["moving"]),
                "augmented_rank": rank_mod(payload["moving_augmented"]),
            },
            "augmented_minor_factorization": {
                **witness,
                "identity_verified": True,
            },
        }
        for payload, witness in zip(payloads, witnesses, strict=True)
    ]
    singular_results = run_program(
        [singular, "-q"],
        singular_program(payloads, witnesses),
        "Singular",
        len(payloads),
        witnesses,
    )
    macaulay2_results = run_macaulay2_program(
        macaulay2,
        macaulay2_program(payloads, witnesses),
        len(payloads),
        witnesses,
    )
    encoded_payload = json.dumps(payloads, sort_keys=True, separators=(",", ":"))
    return {
        "schema": "rs-mca-l1-b9-boundary-321-cas-v2",
        "status": "AUDIT/EXACT_REPRESENTATIVE_CAS_REPLAY",
        "statement": "independently verify the two GF(19) moving-F rank drops are affine-inconsistent and their representative augmented minors factor as unit*t",
        "input": {
            "field": "GF(19)",
            "patterns": [
                {
                    "sizes_by_labelled_petal": list(pattern["sizes"]),
                    "supports": [list(support) for support in pattern["supports"]],
                }
                for pattern in EXCEPTIONAL
            ],
            "fixed_matrix_shape": [15, 12],
            "moving_matrix_shape": [15, 16],
        },
        "expected": {"fixed": EXPECTED_FIXED, "moving": EXPECTED_MOVING},
        "results": {
            "python_modular_elimination": python_results,
            "singular": singular_results,
            "macaulay2": macaulay2_results,
        },
        "certificate": {
            "matrix_payload_sha256": hashlib.sha256(
                encoded_payload.encode("ascii")
            ).hexdigest(),
            "engines": {
                "Singular": singular,
                "Macaulay2": macaulay2,
            },
        },
        "theorem_problem_id": "L1 B9 residual frontier; local moving-F rank-drop audit",
        "proof_status": {
            "exact": "three independent exact engines agree on both representative rank pairs and unit*t augmented-minor factorizations",
            "uniform": "the separate CRT inverse lemma supplies the uniform rank-drop implication without generic saturation",
        },
        "verdict": "GREEN_REPRESENTATIVE_CONTROL - the reviewed CRT lemma, not this specialization, supplies uniformity.",
    }


def validate_report(report: dict[str, object]) -> bool:
    expected_case = {"fixed": EXPECTED_FIXED, "moving": EXPECTED_MOVING}
    return (
        report.get("schema") == "rs-mca-l1-b9-boundary-321-cas-v2"
        and report.get("expected") == expected_case
        and all(
            result["fixed"] == EXPECTED_FIXED
            and result["moving"] == EXPECTED_MOVING
            and result["augmented_minor_factorization"]["identity_verified"]
            and result["augmented_minor_factorization"]["factorization"].endswith("*t")
            for engine_results in report["results"].values()
            for result in engine_results
        )
    )


def tamper_selftest(report: dict[str, object]) -> int:
    mutations = []
    for engine in ("python_modular_elimination", "singular", "macaulay2"):
        changed = copy.deepcopy(report)
        changed["results"][engine][0]["moving"]["rank"] += 1
        mutations.append((engine, changed))
        changed = copy.deepcopy(report)
        changed["results"][engine][0]["augmented_minor_factorization"][
            "identity_verified"
        ] = False
        mutations.append((f"{engine}_minor", changed))
    failed = False
    for name, changed in mutations:
        caught = not validate_report(changed)
        print(f"  tamper {name:<28}: {'CAUGHT' if caught else 'MISSED'}")
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
        print("RESULT: FAIL (CAS ranks disagree)", file=sys.stderr)
        return 1
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
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
    print("l1 B9 boundary (3,2,1) representative CAS replay")
    print("  inputs: two GF(19) moving-F rank-drop patterns")
    print("  object: fixed 15x12 and moving 15x16 coefficient systems")
    for engine, results in report["results"].items():
        print(f"  {engine}: {results}")
    print(f"  certificate: {report['certificate']['matrix_payload_sha256']}")
    print(f"  theorem/problem: {report['theorem_problem_id']}")
    print(f"  proof status: {report['status']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
