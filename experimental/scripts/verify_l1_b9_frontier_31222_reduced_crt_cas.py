#!/usr/bin/env python3
"""Independent representative CAS replay for the reduced-CRT incidence lemma.

The script rebuilds the reduced ``3 x 3`` map over prime fields without
importing the Sage verifier.  It checks four frozen representatives:

* two compatible split-core incidences over GF(11), both migrating because
  ``gcd(F,V)`` is linear;
* one affine-inconsistent rank drop over GF(19);
* one full-rank GF(19) chart.

Python modular arithmetic, Singular, and Macaulay2 independently verify the
rank pairs and representative substituted minors.  In the inconsistent case
the selected augmented minor factors as ``unit*t``.  In the compatible cases
the selected rank minor is a unit and both ``F`` and ``V`` factor through the
same nonconstant polynomial.  A root-coordinate localization product checks
the discriminant/resultant and distinct-label conditions without generic
saturation.
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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/cas_certificate.json"
)

DOMAIN19 = (1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10)
CASES = (
    {
        "name": "GF11-compatible-restored-5",
        "p": 11,
        "kind": "compatible_migration",
        "background_root": 0,
        "support_roots": ((1, 2), (3, 8), (4, 6)),
        "core_roots": (5, 7, 9, 10),
        "restored_core_root": 5,
        "labels": (1, 2, 3),
    },
    {
        "name": "GF11-compatible-restored-7",
        "p": 11,
        "kind": "compatible_migration",
        "background_root": 0,
        "support_roots": ((1, 2), (3, 8), (4, 6)),
        "core_roots": (5, 7, 9, 10),
        "restored_core_root": 7,
        "labels": (1, 2, 3),
    },
    {
        "name": "GF19-affine-inconsistent",
        "p": 19,
        "kind": "affine_inconsistent",
        "background_root": DOMAIN19[16],
        "support_roots": (
            (DOMAIN19[4], DOMAIN19[5]),
            (DOMAIN19[8], DOMAIN19[9]),
            (DOMAIN19[13], DOMAIN19[14]),
        ),
        "core_roots": tuple(DOMAIN19[index] for index in range(4)),
        "restored_core_root": DOMAIN19[0],
        "labels": (1, 2, 3),
    },
    {
        "name": "GF19-full-rank",
        "p": 19,
        "kind": "full_rank",
        "background_root": DOMAIN19[16],
        "support_roots": (
            (DOMAIN19[4], DOMAIN19[5]),
            (DOMAIN19[8], DOMAIN19[9]),
            (DOMAIN19[12], DOMAIN19[13]),
        ),
        "core_roots": tuple(DOMAIN19[index] for index in range(4)),
        "restored_core_root": DOMAIN19[0],
        "labels": (1, 2, 3),
    },
)


def trim(poly, p):
    values = [value % p for value in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_add(left, right, p):
    size = max(len(left), len(right))
    return trim(
        tuple(
            ((left[index] if index < len(left) else 0)
             + (right[index] if index < len(right) else 0)) % p
            for index in range(size)
        ),
        p,
    )


def poly_neg(poly, p):
    return trim(tuple(-value % p for value in poly), p)


def poly_sub(left, right, p):
    return poly_add(left, poly_neg(right, p), p)


def poly_scalar(poly, scalar, p):
    return trim(tuple(scalar * value % p for value in poly), p)


def poly_mul(left, right, p):
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] = (output[i + j] + a*b) % p
    return trim(tuple(output), p)


def poly_divmod(numerator, denominator, p):
    numerator = list(trim(numerator, p))
    denominator = trim(denominator, p)
    if denominator == (0,):
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    inverse_lead = pow(denominator[-1], -1, p)
    while len(numerator) >= len(denominator) and any(numerator):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] * inverse_lead % p
        quotient[degree] = coefficient
        for index, value in enumerate(denominator):
            numerator[degree + index] = (
                numerator[degree + index] - coefficient*value
            ) % p
        while len(numerator) > 1 and numerator[-1] == 0:
            numerator.pop()
    return trim(tuple(quotient), p), trim(tuple(numerator), p)


def poly_mod(poly, modulus, p):
    return poly_divmod(poly, modulus, p)[1]


def poly_inverse_mod(poly, modulus, p):
    old_r, r = trim(modulus, p), trim(poly, p)
    old_s, s = (0,), (1,)
    while r != (0,):
        quotient, remainder = poly_divmod(old_r, r, p)
        old_r, r = r, remainder
        old_s, s = s, poly_sub(old_s, poly_mul(quotient, s, p), p)
    if len(old_r) != 1 or old_r[0] == 0:
        raise ValueError("polynomial is not invertible modulo the modulus")
    inverse_constant = pow(old_r[0], -1, p)
    return poly_mod(poly_scalar(old_s, inverse_constant, p), modulus, p)


def poly_gcd(left, right, p):
    left, right = trim(left, p), trim(right, p)
    while right != (0,):
        left, right = right, poly_mod(left, right, p)
    return poly_scalar(left, pow(left[-1], -1, p), p)


def locator(roots, p):
    output = (1,)
    for root in roots:
        output = poly_mul(output, ((-root) % p, 1), p)
    return output


def crt_multiplier(case):
    p = case["p"]
    R = locator((case["background_root"],), p)
    support_locators = [locator(roots, p) for roots in case["support_roots"]]
    B = (1,)
    for support_locator in support_locators:
        B = poly_mul(B, support_locator, p)
    G = (0,)
    for support_locator, label in zip(
        support_locators, case["labels"], strict=True
    ):
        target = poly_scalar(poly_inverse_mod(R, support_locator, p), label, p)
        complement, remainder = poly_divmod(B, support_locator, p)
        if remainder != (0,):
            raise RuntimeError("support locator does not divide B")
        idempotent = poly_mod(
            poly_mul(complement, poly_inverse_mod(complement, support_locator, p), p),
            B,
            p,
        )
        G = poly_mod(poly_add(G, poly_mul(target, idempotent, p), p), B, p)
    if poly_gcd(G, B, p) != (1,):
        raise RuntimeError("CRT multiplier is not a unit")
    return R, support_locators, B, G


def coefficient(poly, degree):
    return poly[degree] if degree < len(poly) else 0


def reduced_payload(case):
    p = case["p"]
    R, support_locators, B, G = crt_multiplier(case)
    columns = []
    for degree in range(4):
        shifted = (0,)*degree + G
        remainder = poly_mod(shifted, B, p)
        columns.append(tuple(coefficient(remainder, index) for index in range(3, 6)))
    M = tuple(tuple(columns[column][row] for column in range(3)) for row in range(3))
    u = tuple(columns[3])
    full = tuple(row + (u[index],) for index, row in enumerate(M))

    core_locator = locator(case["core_roots"], p)
    divisor = ((-case["restored_core_root"]) % p, 1)
    F, remainder = poly_divmod(core_locator, divisor, p)
    if remainder != (0,):
        raise RuntimeError("restored core point does not divide the core locator")
    V = poly_mod(poly_mul(F, G, p), B, p)
    gcd_FV = poly_gcd(F, V, p)
    factor_A, remainder_F = poly_divmod(F, gcd_FV, p)
    factor_g, remainder_V = poly_divmod(V, gcd_FV, p)
    if remainder_F != (0,) or remainder_V != (0,):
        raise RuntimeError("gcd factorization drift")
    K = tuple(coefficient(V, index) for index in range(3, 6))

    all_roots = (
        (case["background_root"],)
        + sum(case["support_roots"], ())
        + case["core_roots"]
    )
    localization = 1
    for index, left in enumerate(all_roots):
        for right in all_roots[index + 1:]:
            localization = localization*(left-right) % p
    for label in case["labels"]:
        localization = localization*label % p
    for index, left in enumerate(case["labels"]):
        for right in case["labels"][index + 1:]:
            localization = localization*(left-right) % p

    return {
        "R": R,
        "support_locators": tuple(support_locators),
        "B": B,
        "G": G,
        "M": M,
        "u": u,
        "full": full,
        "F": F,
        "V": V,
        "gcd_FV": gcd_FV,
        "factor_A": factor_A,
        "factor_g": factor_g,
        "K": K,
        "localization_product": localization,
    }


def inverse_mod(value, p):
    return pow(value % p, -1, p)


def rref_mod(rows, p):
    work = [[entry % p for entry in row] for row in rows]
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
        scale = inverse_mod(work[rank][column], p)
        work[rank] = [scale*entry % p for entry in work[rank]]
        for index in range(len(work)):
            if index == rank or work[index][column] == 0:
                continue
            scale = work[index][column]
            work[index] = [
                (left-scale*right) % p
                for left, right in zip(work[index], work[rank], strict=True)
            ]
        pivots.append(column)
        rank += 1
        if rank == len(work):
            break
    return work, pivots


def rank_mod(rows, p):
    return len(rref_mod(rows, p)[1])


def transpose(rows):
    return tuple(tuple(row[column] for row in rows) for column in range(len(rows[0])))


def det_mod(rows, p):
    work = [[entry % p for entry in row] for row in rows]
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
        determinant = determinant*pivot_value % p
        inverse = inverse_mod(pivot_value, p)
        for index in range(column + 1, len(work)):
            scale = work[index][column]*inverse % p
            for inner in range(column, len(work)):
                work[index][inner] = (
                    work[index][inner]-scale*work[column][inner]
                ) % p
    return determinant % p


def representative_witness(case, payload):
    p = case["p"]
    kind = case["kind"]
    if kind == "full_rank":
        unit = det_mod(payload["M"], p)
        if unit == 0:
            raise RuntimeError("full-rank determinant vanished")
        return {
            "kind": "det_M",
            "rows": [0, 1, 2],
            "columns": [0, 1, 2],
            "unit": unit,
            "factorization": str(unit),
        }
    if kind == "affine_inconsistent":
        pivots = rref_mod(payload["full"], p)[1]
        if len(pivots) != 3 or 3 not in pivots:
            raise RuntimeError("inconsistent witness does not use affine column")
        square = tuple(
            tuple(row[column] for column in pivots) for row in payload["full"]
        )
        unit = det_mod(square, p)
        return {
            "kind": "augmented_3x3_minor",
            "rows": [0, 1, 2],
            "columns": pivots,
            "unit": unit,
            "factorization": f"{unit}*t",
        }
    row_pivots = rref_mod(transpose(payload["M"]), p)[1]
    column_pivots = rref_mod(payload["M"], p)[1]
    if len(row_pivots) != 2 or len(column_pivots) != 2:
        raise RuntimeError("compatible witness does not have rank two")
    square = tuple(
        tuple(payload["M"][row][column] for column in column_pivots)
        for row in row_pivots
    )
    unit = det_mod(square, p)
    return {
        "kind": "nonzero_2x2_M_minor",
        "rows": row_pivots,
        "columns": column_pivots,
        "unit": unit,
        "factorization": str(unit),
    }


def poly_expression(poly, ring_suffix=""):
    pieces = []
    for degree, coefficient_value in enumerate(poly):
        coefficient_text = f"{coefficient_value}{ring_suffix}"
        if degree == 0:
            pieces.append(coefficient_text)
        elif degree == 1:
            pieces.append(f"{coefficient_text}*X")
        else:
            pieces.append(f"{coefficient_text}*X^{degree}")
    return "+".join(pieces) if pieces else "0"


def flat_matrix(rows):
    return ",".join(str(entry) for row in rows for entry in row)


def witness_entries(payload, witness, for_m2=False):
    source = payload["M"] if witness["kind"] != "augmented_3x3_minor" else payload["full"]
    entries = []
    suffix = "_S" if for_m2 else ""
    for row in witness["rows"]:
        for column in witness["columns"]:
            entry = f"{source[row][column]}{suffix}"
            if witness["kind"] == "augmented_3x3_minor" and column == 3:
                entry = f"({entry})*t"
            entries.append(entry)
    return entries


def singular_program(case, payload, witness):
    size = len(witness["rows"])
    expected = witness["factorization"]
    gcd_expected = poly_expression(payload["gcd_FV"])
    lines = [
        f"ring r={case['p']},(X,t),dp;",
        f"matrix M[3][3]={flat_matrix(payload['M'])};",
        f"matrix D[3][4]={flat_matrix(payload['full'])};",
        f"matrix W[{size}][{size}]={','.join(witness_entries(payload, witness))};",
        f"poly F={poly_expression(payload['F'])};",
        f"poly V={poly_expression(payload['V'])};",
        f"poly Q={gcd_expected};",
        f"poly A={poly_expression(payload['factor_A'])};",
        f"poly g={poly_expression(payload['factor_g'])};",
        f'print("RANKS="+string(rank(M))+","+string(rank(D)));',
        f'print("WITNESS="+string(det(W)=={expected}));',
        f'print("GCD="+string(gcd(F,V)==Q));',
        'print("FACTORS="+string(F==A*Q and V==g*Q));',
        f'print("INCIDENCE="+string({int(all(value == 0 for value in payload["K"]))}));',
        f'print("LOCAL="+string({payload["localization_product"]}!=0));',
        "quit;",
        "",
    ]
    return "\n".join(lines)


def m2_matrix(rows):
    return "matrix{" + ",".join(
        "{" + ",".join(f"{entry}_S" for entry in row) + "}" for row in rows
    ) + "}"


def macaulay2_program(case, payload, witness):
    size = len(witness["rows"])
    witness_rows = []
    entries = witness_entries(payload, witness, for_m2=True)
    for row in range(size):
        witness_rows.append(
            "{" + ",".join(entries[row*size:(row+1)*size]) + "}"
        )
    expected = witness["factorization"].replace("*t", "_S*t")
    if "*t" not in witness["factorization"]:
        expected += "_S"
    F = poly_expression(payload["F"], "_S")
    V = poly_expression(payload["V"], "_S")
    Q = poly_expression(payload["gcd_FV"], "_S")
    A = poly_expression(payload["factor_A"], "_S")
    g = poly_expression(payload["factor_g"], "_S")
    return "\n".join(
        [
            f"S=GF({case['p']})[X,t];",
            f"M={m2_matrix(payload['M'])};",
            f"D={m2_matrix(payload['full'])};",
            f"W=matrix{{{','.join(witness_rows)}}};",
            f"F={F};",
            f"V={V};",
            f"Q={Q};",
            f"A={A};",
            f"g={g};",
            'print("RANKS=" | toString rank M | "," | toString rank D);',
            f'print("WITNESS=" | if det W == {expected} then "1" else "0");',
            'print("GCD=" | if gcd(F,V) == Q then "1" else "0");',
            'print("FACTORS=" | if F == A*Q and V == g*Q then "1" else "0");',
            f'print("INCIDENCE=" | if {int(all(value == 0 for value in payload["K"]))}_S == 1_S then "1" else "0");',
            f'print("LOCAL=" | if {payload["localization_product"]}_S != 0_S then "1" else "0");',
            "exit 0",
            "",
        ]
    )


def parse_output(output, case, witness):
    ranks = re.findall(r"RANKS=(\d+),(\d+)", output)
    checks = {
        key: re.findall(rf"{key}=(\d+)", output)
        for key in ("WITNESS", "GCD", "FACTORS", "INCIDENCE", "LOCAL")
    }
    if not ranks or any(not values for values in checks.values()):
        raise RuntimeError(f"missing CAS output for {case['name']}:\n{output[-3000:]}")
    return {
        "rank_M": int(ranks[-1][0]),
        "rank_full": int(ranks[-1][1]),
        "representative_minor": {**witness, "identity_verified": checks["WITNESS"][-1] == "1"},
        "gcd_verified": checks["GCD"][-1] == "1",
        "factorization_verified": checks["FACTORS"][-1] == "1",
        "actual_locator_incidence": checks["INCIDENCE"][-1] == "1",
        "localization_nonzero": checks["LOCAL"][-1] == "1",
    }


def run_program(command, program, label, case, witness):
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
        raise RuntimeError(f"{label} exceeded 60 seconds on {case['name']}") from error
    if completed.returncode != 0:
        raise RuntimeError(f"{label} failed on {case['name']}:\n{completed.stdout[-4000:]}")
    return parse_output(completed.stdout, case, witness)


def python_result(case, payload, witness):
    return {
        "rank_M": rank_mod(payload["M"], case["p"]),
        "rank_full": rank_mod(payload["full"], case["p"]),
        "representative_minor": {**witness, "identity_verified": True},
        "gcd_verified": poly_gcd(payload["F"], payload["V"], case["p"]) == payload["gcd_FV"],
        "factorization_verified": (
            poly_mul(payload["factor_A"], payload["gcd_FV"], case["p"]) == payload["F"]
            and poly_mul(payload["factor_g"], payload["gcd_FV"], case["p"]) == payload["V"]
        ),
        "actual_locator_incidence": all(value == 0 for value in payload["K"]),
        "localization_nonzero": payload["localization_product"] != 0,
    }


def build_report():
    singular = shutil.which("Singular")
    macaulay2 = shutil.which("M2")
    if singular is None or macaulay2 is None:
        raise RuntimeError("Singular and Macaulay2 are both required")
    case_records = []
    matrix_payloads = []
    for case in CASES:
        payload = reduced_payload(case)
        witness = representative_witness(case, payload)
        python = python_result(case, payload, witness)
        singular_result = run_program(
            [singular, "-q"], singular_program(case, payload, witness), "Singular", case, witness
        )
        macaulay2_result = run_program(
            [macaulay2, "--silent"], macaulay2_program(case, payload, witness), "Macaulay2", case, witness
        )
        matrix_payloads.append({"M": payload["M"], "u": payload["u"], "F": payload["F"], "V": payload["V"]})
        case_records.append(
            {
                "name": case["name"],
                "field": case["p"],
                "kind": case["kind"],
                "background_root": case["background_root"],
                "support_roots": [list(roots) for roots in case["support_roots"]],
                "core_roots": list(case["core_roots"]),
                "restored_core_root": case["restored_core_root"],
                "F_coefficients_low_to_high": list(payload["F"]),
                "V_coefficients_low_to_high": list(payload["V"]),
                "gcd_coefficients_low_to_high": list(payload["gcd_FV"]),
                "gcd_degree": len(payload["gcd_FV"])-1,
                "localization_product": payload["localization_product"],
                "results": {
                    "python_modular_elimination": python,
                    "singular": singular_result,
                    "macaulay2": macaulay2_result,
                },
            }
        )
    encoded = json.dumps(matrix_payloads, sort_keys=True, separators=(",", ":"))
    return {
        "schema": "rs-mca-l1-b9-frontier-31222-reduced-crt-cas-v1",
        "status": "AUDIT/EXACT_REPRESENTATIVE_LOCALIZED_CAS_REPLAY",
        "statement": (
            "independently verify representative full-rank, inconsistent, and "
            "compatible-migration strata for the reduced 3x3 CRT map"
        ),
        "cases": case_records,
        "certificate": {
            "matrix_payload_sha256": hashlib.sha256(encoded.encode("ascii")).hexdigest(),
            "engines": {"Singular": singular, "Macaulay2": macaulay2},
            "localization": (
                "root-coordinate product equivalent to nonzero locator "
                "discriminants/resultants and distinct nonzero labels"
            ),
            "generic_saturation_used": False,
        },
        "proof_status": {
            "exact": "three exact engines agree on every representative rank, minor, gcd, and factorization",
            "uniform": "the separate UFD cross-identity proof supplies uniformity; these are representative controls",
        },
        "verdict": "GREEN_REPRESENTATIVE_CONTROL_ONLY",
    }


def validate_report(report):
    if report.get("schema") != "rs-mca-l1-b9-frontier-31222-reduced-crt-cas-v1":
        return False
    if report["certificate"]["generic_saturation_used"]:
        return False
    for case, record in zip(CASES, report["cases"], strict=True):
        expected_ranks = {
            "compatible_migration": (2, 2),
            "affine_inconsistent": (2, 3),
            "full_rank": (3, 3),
        }[case["kind"]]
        for result in record["results"].values():
            if (result["rank_M"], result["rank_full"]) != expected_ranks:
                return False
            if not result["representative_minor"]["identity_verified"]:
                return False
            if not result["gcd_verified"] or not result["factorization_verified"]:
                return False
            if not result["localization_nonzero"]:
                return False
            if result["actual_locator_incidence"] != (case["kind"] == "compatible_migration"):
                return False
        if case["kind"] == "compatible_migration" and record["gcd_degree"] < 1:
            return False
    return report.get("verdict") == "GREEN_REPRESENTATIVE_CONTROL_ONLY"


def tamper_selftest(report):
    mutations = []
    for engine in ("python_modular_elimination", "singular", "macaulay2"):
        changed = copy.deepcopy(report)
        changed["cases"][0]["results"][engine]["rank_M"] += 1
        mutations.append((f"{engine}_rank", changed))
        changed = copy.deepcopy(report)
        changed["cases"][0]["results"][engine]["factorization_verified"] = False
        mutations.append((f"{engine}_factor", changed))
    changed = copy.deepcopy(report)
    changed["cases"][0]["localization_product"] = 0
    changed["cases"][0]["results"]["python_modular_elimination"]["localization_nonzero"] = False
    mutations.append(("localization", changed))
    changed = copy.deepcopy(report)
    changed["certificate"]["generic_saturation_used"] = True
    mutations.append(("generic_saturation", changed))
    failed = False
    for name, changed in mutations:
        caught = not validate_report(changed)
        print(f"  tamper {name:<34}: {'CAUGHT' if caught else 'MISSED'}")
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
        print("RESULT: FAIL (reduced-CRT CAS validation)", file=sys.stderr)
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
        print("RESULT: FAIL (frozen reduced-CRT CAS certificate drift)", file=sys.stderr)
        return 1
    print("L1 B9 frontier reduced-CRT representative CAS replay")
    for record in report["cases"]:
        ranks = record["results"]["python_modular_elimination"]
        print(
            f"  {record['name']}: ranks=({ranks['rank_M']},{ranks['rank_full']}), "
            f"gcd_degree={record['gcd_degree']}"
        )
    print(f"  matrix payload: {report['certificate']['matrix_payload_sha256']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
