#!/usr/bin/env python3
"""Independent Python/Singular/Macaulay2 replay for the 32221 CRT map.

The verifier rebuilds all 432 reduced ``3 x 3`` affine maps over GF(19)
without importing the Sage census.  It checks the complete rank histogram and
selects one representative of each stratum:

* full rank;
* coefficient-rank drop with affine inconsistency;
* compatible coefficient-rank drop.

For the unique compatible chart, all three engines verify the exact line

    F=(X+t)(X^2+16),    V=18(X+t),

and a nonzero rank-two minor.  The other representatives verify a nonzero
full determinant or augmented determinant.  Only the explicit nonzero
root/label localization is used; generic saturation is not used.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-32221/cas_certificate.json"
)
SAGE_CERTIFICATE_PATH = (
    ROOT / "experimental/data/certificates/l1-b9-frontier-32221/certificate.json"
)

P = 19
DOMAIN = (1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10)
CORE = tuple(range(4))
PETALS = (
    tuple(range(4, 8)),
    tuple(range(8, 12)),
    tuple(range(12, 16)),
)
BACKGROUND = (16, 17)
LABELS = (1, 2, 3)
EXPECTED_RANKS = {
    "rankM=2,rankAug=2": 1,
    "rankM=2,rankAug=3": 23,
    "rankM=3,rankAug=3": 408,
}


def trim(poly):
    values = [value % P for value in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_add(left, right):
    size = max(len(left), len(right))
    return trim(
        tuple(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        )
    )


def poly_neg(poly):
    return trim(tuple(-value for value in poly))


def poly_sub(left, right):
    return poly_add(left, poly_neg(right))


def poly_scalar(poly, scalar):
    return trim(tuple(scalar * value for value in poly))


def poly_mul(left, right):
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] = (output[i + j] + a * b) % P
    return trim(tuple(output))


def poly_divmod(numerator, denominator):
    numerator = list(trim(numerator))
    denominator = trim(denominator)
    if denominator == (0,):
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    inverse_lead = pow(denominator[-1], -1, P)
    while len(numerator) >= len(denominator) and any(numerator):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] * inverse_lead % P
        quotient[degree] = coefficient
        for index, value in enumerate(denominator):
            numerator[degree + index] = (
                numerator[degree + index] - coefficient * value
            ) % P
        while len(numerator) > 1 and numerator[-1] == 0:
            numerator.pop()
    return trim(tuple(quotient)), trim(tuple(numerator))


def poly_mod(poly, modulus):
    return poly_divmod(poly, modulus)[1]


def poly_inverse_mod(poly, modulus):
    old_r, r = trim(modulus), trim(poly)
    old_s, s = (0,), (1,)
    while r != (0,):
        quotient, remainder = poly_divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, poly_sub(old_s, poly_mul(quotient, s))
    if len(old_r) != 1 or old_r[0] == 0:
        raise ValueError("polynomial is not invertible modulo the modulus")
    return poly_mod(poly_scalar(old_s, pow(old_r[0], -1, P)), modulus)


def poly_gcd(left, right):
    left, right = trim(left), trim(right)
    while right != (0,):
        left, right = right, poly_mod(left, right)
    return poly_scalar(left, pow(left[-1], -1, P))


def locator(indices):
    output = (1,)
    for index in indices:
        output = poly_mul(output, ((-DOMAIN[index]) % P, 1))
    return output


def coefficient(poly, degree):
    return poly[degree] if degree < len(poly) else 0


def inverse_mod(value):
    return pow(value % P, -1, P)


def rref_mod(rows):
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
        work[rank] = [scale * entry % P for entry in work[rank]]
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


def rank_mod(rows):
    return len(rref_mod(rows)[1])


def transpose(rows):
    return tuple(
        tuple(row[column] for row in rows) for column in range(len(rows[0]))
    )


def det_mod(rows):
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


def support_assignments():
    for short_petal in range(3):
        occupancies = tuple(1 if index == short_petal else 2 for index in range(3))
        choices = [
            itertools.combinations(petal, occupancy)
            for petal, occupancy in zip(PETALS, occupancies, strict=True)
        ]
        for supports in itertools.product(*choices):
            yield tuple(tuple(support) for support in supports)


def canonical_assignment(supports):
    return [list(BACKGROUND), *[list(support) for support in supports]]


def reduced_payload(supports):
    R = locator(BACKGROUND)
    support_locators = [locator(support) for support in supports]
    B = (1,)
    for support_locator in support_locators:
        B = poly_mul(B, support_locator)
    if len(B) != 6:
        raise RuntimeError("CRT modulus must have degree five")
    G = (0,)
    for label, support_locator in zip(LABELS, support_locators, strict=True):
        target = poly_scalar(poly_inverse_mod(R, support_locator), label)
        complement, remainder = poly_divmod(B, support_locator)
        if remainder != (0,):
            raise RuntimeError("support locator does not divide B")
        projector = poly_mod(
            poly_mul(complement, poly_inverse_mod(complement, support_locator)),
            B,
        )
        G = poly_mod(poly_add(G, poly_mul(target, projector)), B)
    if poly_gcd(G, B) != (1,):
        raise RuntimeError("CRT multiplier is not a unit")
    columns = []
    for degree in range(4):
        remainder = poly_mod((0,) * degree + G, B)
        columns.append(tuple(coefficient(remainder, index) for index in (2, 3, 4)))
    M = tuple(
        tuple(columns[column][row] for column in range(3)) for row in range(3)
    )
    u = tuple(columns[3])
    augmented = tuple(row + (u[index],) for index, row in enumerate(M))

    all_indices = CORE + BACKGROUND + sum(supports, ())
    roots = tuple(DOMAIN[index] for index in all_indices)
    localization = 1
    for index, left in enumerate(roots):
        for right in roots[index + 1 :]:
            localization = localization * (left - right) % P
    for label in LABELS:
        localization = localization * label % P
    for index, left in enumerate(LABELS):
        for right in LABELS[index + 1 :]:
            localization = localization * (left - right) % P
    return {
        "supports": supports,
        "canonical_assignment": canonical_assignment(supports),
        "R": R,
        "support_locators": tuple(support_locators),
        "B": B,
        "G": G,
        "M": M,
        "u": u,
        "augmented": augmented,
        "rank_M": rank_mod(M),
        "rank_augmented": rank_mod(augmented),
        "localization_product": localization,
    }


def compatible_python_check(payload):
    points = []
    for t in range(P):
        f_lower = ((16 * t) % P, 16, t)
        residual = [
            (sum(payload["M"][row][column] * f_lower[column] for column in range(3))
             + payload["u"][row])
            % P
            for row in range(3)
        ]
        F = ((16 * t) % P, 16, t, 1)
        V = poly_mod(poly_mul(F, payload["G"]), payload["B"])
        gcd_FV = poly_gcd(F, V)
        if residual != [0, 0, 0]:
            raise RuntimeError("compatible affine line failed reduced equations")
        if V != ((18 * t) % P, 18) or gcd_FV != (t, 1):
            raise RuntimeError("compatible affine line factorization drift")
        points.append({"t": t, "F": F, "V": V, "gcd": gcd_FV})
    return {
        "solution_count": len(points),
        "formula": {
            "F": "(X+t)*(X^2+16)",
            "V": "18*(X+t)",
            "gcd": "X+t",
        },
        "all_points_verified": True,
        "points_sha256": hashlib.sha256(
            json.dumps(points, separators=(",", ":")).encode("ascii")
        ).hexdigest(),
    }


def representative_witness(payload, kind):
    if kind == "full_rank":
        unit = det_mod(payload["M"])
        if unit == 0:
            raise RuntimeError("full-rank determinant vanished")
        return {"kind": "det_M", "rows": [0, 1, 2], "columns": [0, 1, 2], "unit": unit}
    if kind == "affine_inconsistent":
        column_pivots = rref_mod(payload["augmented"])[1]
        row_pivots = rref_mod(transpose(payload["augmented"]))[1]
        if len(column_pivots) != 3 or len(row_pivots) != 3 or 3 not in column_pivots:
            raise RuntimeError("inconsistent witness does not use affine column")
        square = tuple(
            tuple(payload["augmented"][row][column] for column in column_pivots)
            for row in row_pivots
        )
        unit = det_mod(square)
        return {"kind": "augmented_minor", "rows": row_pivots, "columns": column_pivots, "unit": unit}
    column_pivots = rref_mod(payload["M"])[1]
    row_pivots = rref_mod(transpose(payload["M"]))[1]
    if len(column_pivots) != 2 or len(row_pivots) != 2:
        raise RuntimeError("compatible witness does not have rank two")
    square = tuple(
        tuple(payload["M"][row][column] for column in column_pivots)
        for row in row_pivots
    )
    unit = det_mod(square)
    return {"kind": "rank_two_minor", "rows": row_pivots, "columns": column_pivots, "unit": unit}


def flat_matrix(rows):
    return ",".join(str(entry) for row in rows for entry in row)


def witness_entries(payload, witness, suffix=""):
    source = payload["augmented"] if witness["kind"] == "augmented_minor" else payload["M"]
    return [
        f"{source[row][column]}{suffix}"
        for row in witness["rows"]
        for column in witness["columns"]
    ]


def singular_program(payload, witness, kind):
    size = len(witness["rows"])
    compatible = kind == "compatible_rankdrop"
    return "\n".join(
        [
            "ring r=19,(X,t),dp;",
            f"matrix M[3][3]={flat_matrix(payload['M'])};",
            f"matrix D[3][4]={flat_matrix(payload['augmented'])};",
            f"matrix W[{size}][{size}]={','.join(witness_entries(payload, witness))};",
            "matrix f[3][1]=16*t,16,t;",
            f"matrix u[3][1]={','.join(str(value) for value in payload['u'])};",
            "matrix J=M*f+u;",
            "poly F=X^3+t*X^2+16*X+16*t;",
            "poly V=18*X+18*t;",
            'print("RANKS="+string(rank(M))+","+string(rank(D)));',
            f'print("WITNESS="+string(det(W)=={witness["unit"]}));',
            (
                'print("INCIDENCE="+string(J[1,1]==0 and J[2,1]==0 and J[3,1]==0));'
                if compatible
                else 'print("INCIDENCE=1");'
            ),
            (
                'print("FACTOR="+string(F==(X+t)*(X^2+16) and V==18*(X+t)));'
                if compatible
                else 'print("FACTOR=1");'
            ),
            f'print("LOCAL="+string({payload["localization_product"]}!=0));',
            "quit;",
            "",
        ]
    )


def m2_matrix(rows):
    return "matrix{" + ",".join(
        "{" + ",".join(f"{entry}_S" for entry in row) + "}" for row in rows
    ) + "}"


def macaulay2_program(payload, witness, kind):
    size = len(witness["rows"])
    entries = witness_entries(payload, witness, "_S")
    witness_rows = [
        "{" + ",".join(entries[row * size : (row + 1) * size]) + "}"
        for row in range(size)
    ]
    compatible = kind == "compatible_rankdrop"
    return "\n".join(
        [
            "S=GF(19)[X,t];",
            f"M={m2_matrix(payload['M'])};",
            f"D={m2_matrix(payload['augmented'])};",
            f"W=matrix{{{','.join(witness_rows)}}};",
            "f=matrix{{16_S*t},{16_S},{t}};",
            "u=matrix{" + ",".join("{" + str(value) + "_S}" for value in payload["u"]) + "};",
            "J=M*f+u;",
            "F=X^3+t*X^2+16_S*X+16_S*t;",
            "V=18_S*X+18_S*t;",
            'print("RANKS=" | toString rank M | "," | toString rank D);',
            f'print("WITNESS=" | if det W == {witness["unit"]}_S then "1" else "0");',
            (
                'print("INCIDENCE=" | if J_(0,0) == 0_S and J_(1,0) == 0_S and J_(2,0) == 0_S then "1" else "0");'
                if compatible
                else 'print("INCIDENCE=1");'
            ),
            (
                'print("FACTOR=" | if F == (X+t)*(X^2+16_S) and V == 18_S*(X+t) then "1" else "0");'
                if compatible
                else 'print("FACTOR=1");'
            ),
            f'print("LOCAL=" | if {payload["localization_product"]}_S != 0_S then "1" else "0");',
            "exit 0",
            "",
        ]
    )


def parse_output(output, label):
    ranks = re.findall(r"RANKS=(\d+),(\d+)", output)
    checks = {
        key: re.findall(rf"{key}=(\d+)", output)
        for key in ("WITNESS", "INCIDENCE", "FACTOR", "LOCAL")
    }
    if not ranks or any(not values for values in checks.values()):
        raise RuntimeError(f"missing {label} output:\n{output[-3000:]}")
    return {
        "rank_M": int(ranks[-1][0]),
        "rank_augmented": int(ranks[-1][1]),
        "minor_verified": checks["WITNESS"][-1] == "1",
        "compatible_line_incidence_verified": checks["INCIDENCE"][-1] == "1",
        "compatible_line_factorization_verified": checks["FACTOR"][-1] == "1",
        "localization_nonzero": checks["LOCAL"][-1] == "1",
    }


def run_program(command, program, label):
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
    return parse_output(completed.stdout, label)


def python_result(payload, witness, kind):
    compatible = kind == "compatible_rankdrop"
    return {
        "rank_M": payload["rank_M"],
        "rank_augmented": payload["rank_augmented"],
        "minor_verified": witness["unit"] != 0,
        "compatible_line_incidence_verified": True,
        "compatible_line_factorization_verified": True,
        "localization_nonzero": payload["localization_product"] != 0,
        "compatible_line": compatible_python_check(payload) if compatible else None,
    }


def build_report():
    singular = shutil.which("Singular")
    macaulay2 = shutil.which("M2")
    if singular is None or macaulay2 is None:
        raise RuntimeError("Singular and Macaulay2 are both required")

    rank_histogram = Counter()
    representatives = {}
    payload_hash_rows = []
    for supports in support_assignments():
        payload = reduced_payload(supports)
        key = f"rankM={payload['rank_M']},rankAug={payload['rank_augmented']}"
        rank_histogram[key] += 1
        payload_hash_rows.append(
            {
                "canonical_assignment": payload["canonical_assignment"],
                "M": payload["M"],
                "u": payload["u"],
            }
        )
        kind = {
            (3, 3): "full_rank",
            (2, 3): "affine_inconsistent",
            (2, 2): "compatible_rankdrop",
        }[(payload["rank_M"], payload["rank_augmented"])]
        representatives.setdefault(kind, payload)
    if dict(sorted(rank_histogram.items())) != EXPECTED_RANKS:
        raise RuntimeError("independent Python rank histogram drift")
    if representatives["compatible_rankdrop"]["canonical_assignment"] != [
        [16, 17], [5], [8, 11], [14, 15]
    ]:
        raise RuntimeError("compatible chart drift")

    case_records = []
    for kind in ("full_rank", "affine_inconsistent", "compatible_rankdrop"):
        payload = representatives[kind]
        witness = representative_witness(payload, kind)
        python = python_result(payload, witness, kind)
        singular_result = run_program(
            [singular, "-q"], singular_program(payload, witness, kind), f"Singular {kind}"
        )
        macaulay2_result = run_program(
            [macaulay2, "--no-readline", "--silent"],
            macaulay2_program(payload, witness, kind),
            f"Macaulay2 {kind}",
        )
        case_records.append(
            {
                "kind": kind,
                "canonical_assignment": payload["canonical_assignment"],
                "M": [list(row) for row in payload["M"]],
                "u": list(payload["u"]),
                "representative_minor": witness,
                "localization_product": payload["localization_product"],
                "results": {
                    "python_modular_elimination": python,
                    "singular": singular_result,
                    "macaulay2": macaulay2_result,
                },
            }
        )

    sage_certificate = json.loads(SAGE_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if sage_certificate["schema"] != "rs-mca-l1-b9-frontier-32221-census-v1":
        raise RuntimeError("Sage certificate schema drift")
    return {
        "schema": "rs-mca-l1-b9-frontier-32221-reduced-crt-cas-v1",
        "status": "AUDIT/EXACT_REPRESENTATIVE_LOCALIZED_CAS_REPLAY",
        "statement": (
            "independently reproduce the full GF(19) reduced-rank census and "
            "verify representative full, inconsistent, and compatible strata"
        ),
        "rank_census": {
            "support_pattern_count": len(payload_hash_rows),
            "histogram": dict(sorted(rank_histogram.items())),
            "matrix_payload_sha256": hashlib.sha256(
                json.dumps(payload_hash_rows, sort_keys=True, separators=(",", ":")).encode("ascii")
            ).hexdigest(),
        },
        "cases": case_records,
        "linked_sage_certificate": {
            "path": str(SAGE_CERTIFICATE_PATH.relative_to(ROOT)),
            "sha256": hashlib.sha256(SAGE_CERTIFICATE_PATH.read_bytes()).hexdigest(),
        },
        "certificate": {
            "engines": {"Singular": singular, "Macaulay2": macaulay2},
            "localization": (
                "explicit nonzero product of core/background/support root "
                "differences and nonzero distinct-label factors"
            ),
            "generic_saturation_used": False,
        },
        "proof_status": {
            "exact": (
                "Python independently checks all 432 maps; Python, Singular, "
                "and Macaulay2 agree on representative ranks, minors, and the "
                "compatible common-factor line"
            ),
            "uniform": (
                "the separate degree-gap/UFD proof, not these representatives, "
                "must supply the uniform rank-drop implication"
            ),
        },
        "verdict": "GREEN_REPRESENTATIVE_CONTROL_ONLY",
    }


def validate_report(report):
    if report.get("schema") != "rs-mca-l1-b9-frontier-32221-reduced-crt-cas-v1":
        return False
    if report["rank_census"]["support_pattern_count"] != 432:
        return False
    if report["rank_census"]["histogram"] != EXPECTED_RANKS:
        return False
    if report["certificate"]["generic_saturation_used"]:
        return False
    expected_ranks = {
        "full_rank": (3, 3),
        "affine_inconsistent": (2, 3),
        "compatible_rankdrop": (2, 2),
    }
    for case in report["cases"]:
        if (case["kind"] == "compatible_rankdrop") != (
            case["canonical_assignment"] == [[16, 17], [5], [8, 11], [14, 15]]
        ):
            return False
        for result in case["results"].values():
            if (result["rank_M"], result["rank_augmented"]) != expected_ranks[case["kind"]]:
                return False
            if not all(
                result[key]
                for key in (
                    "minor_verified",
                    "compatible_line_incidence_verified",
                    "compatible_line_factorization_verified",
                    "localization_nonzero",
                )
            ):
                return False
        if case["kind"] == "compatible_rankdrop":
            line = case["results"]["python_modular_elimination"]["compatible_line"]
            if line["solution_count"] != 19 or not line["all_points_verified"]:
                return False
    return (
        report["linked_sage_certificate"]["sha256"]
        == hashlib.sha256(SAGE_CERTIFICATE_PATH.read_bytes()).hexdigest()
        and report.get("verdict") == "GREEN_REPRESENTATIVE_CONTROL_ONLY"
    )


def tamper_selftest(report):
    mutations = []
    for engine in ("python_modular_elimination", "singular", "macaulay2"):
        changed = copy.deepcopy(report)
        changed["cases"][2]["results"][engine]["rank_M"] += 1
        mutations.append((f"{engine}_rank", changed))
        changed = copy.deepcopy(report)
        changed["cases"][2]["results"][engine][
            "compatible_line_factorization_verified"
        ] = False
        mutations.append((f"{engine}_factor", changed))
    changed = copy.deepcopy(report)
    changed["certificate"]["generic_saturation_used"] = True
    mutations.append(("generic_saturation", changed))
    changed = copy.deepcopy(report)
    changed["linked_sage_certificate"]["sha256"] = "0" * 64
    mutations.append(("sage_link", changed))
    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<30}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (CAS validation)", file=sys.stderr)
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
    print("[PASS] Python census: 408 full, 23 inconsistent, 1 compatible")
    print("[PASS] Singular=Macaulay2: representative ranks/minors/factor line")
    print("RESULT: PASS (32221 independent reduced-CRT CAS replay)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
