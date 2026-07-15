#!/usr/bin/env python3
"""Independent CAS verifier for the L1 B9-boundary ``(2,2,2)`` slice.

This script does not import the Sage analyzer or the full-list scanner.  It
rebuilds all 216 fixed-support systems in the frozen
``(p,n,k,s)=(19,18,5,8)`` sequential layout, sends the identical matrix
payload to Singular and Macaulay2, and checks

    rank(A)=12,  rank([A|b])=13

for every system.  It also independently repeats the GF(11)/GF(13)
compatibility-rank census with integer modular arithmetic and verifies one
explicit GF(13) degree-two quotient witness.  For its three compatible split
quartics it also independently checks that ``gcd(F,W)`` has degree two, so
the explaining polynomial recovers two allegedly missed core points and the
exact profile migrates from ``d=4`` to ``d=2``.

These are exact finite and local-algebra checks.  They do not prove a
moving-support count or the global mixed-petal theorem.
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
from collections import Counter
from dataclasses import dataclass
from math import comb


P = 19
DOMAIN = (1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10)
CORE = tuple(range(4))
PETALS = (tuple(range(4, 8)), tuple(range(8, 12)), tuple(range(12, 16)))
BACKGROUND = tuple(range(16, 18))
LABELS = (1, 2, 3)
EXPECTED_CAS = {
    "total": 216,
    "rank12_augmented13": 216,
    "coefficient_rank_deficient": 0,
    "consistent": 0,
    "other": 0,
}
EXPECTED_STRUCTURAL = {
    11: {
        "total": 7560,
        "rank": {"1": 2, "2": 82, "3": 7476},
        "affine": {
            "rankC=1,rankAug=2": 2,
            "rankC=2,rankAug=2": 18,
            "rankC=2,rankAug=3": 64,
            "rankC=3,rankAug=3": 7476,
        },
        "common_involution": {"1": 2, "2": 18, "3": 148},
    },
    13: {
        "total": 41580,
        "rank": {"1": 5, "2": 383, "3": 41192},
        "affine": {
            "rankC=1,rankAug=2": 5,
            "rankC=2,rankAug=2": 49,
            "rankC=2,rankAug=3": 334,
            "rankC=3,rankAug=3": 41192,
        },
        "common_involution": {"1": 5, "2": 49, "3": 486},
    },
}
EXPECTED_PAYLOAD_SHA256 = "75b334c9eeb2a25bf7c6d9d1f517ae7120cd20c097c8002e518a00e29781f2b8"
EXPECTED_MOVING_SUPPORT = {
    "formula": "binom(b,2)*binom(M,3)*216*q",
    "rank2_exact_d4_charge": 0,
    "rows": [
        {
            "q": 19,
            "n": 18,
            "selected_support_charts": 216,
            "exact_d4_upper_bound": 4104,
            "old_cofactor_upper_bound": 1481544,
        },
        {
            "q": 23,
            "n": 22,
            "selected_support_charts": 864,
            "exact_d4_upper_bound": 19872,
            "old_cofactor_upper_bound": 10512288,
        },
        {
            "q": 47,
            "n": 46,
            "selected_support_charts": 25920,
            "exact_d4_upper_bound": 1218240,
            "old_cofactor_upper_bound": 2691092160,
        },
    ],
}
@dataclass(frozen=True)
class Fibre:
    coefficient: tuple[tuple[int, ...], ...]
    augmented: tuple[tuple[int, ...], ...]


def poly_mul(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] = (output[i + j] + a * b) % p
    return tuple(output)


def locator(values: tuple[int, ...], p: int) -> tuple[int, ...]:
    output = (1,)
    for value in values:
        output = poly_mul(output, ((-value) % p, 1), p)
    return output


def shifted(poly: tuple[int, ...], shift: int, length: int, p: int) -> list[int]:
    output = [0] * length
    for degree, coefficient in enumerate(poly):
        if degree + shift < length:
            output[degree + shift] = coefficient % p
    return output


def full_fibre(supports: tuple[tuple[int, ...], ...]) -> Fibre:
    F = locator(tuple(DOMAIN[index] for index in CORE), P)
    R = locator(tuple(DOMAIN[index] for index in BACKGROUND), P)
    support_locators = [
        locator(tuple(DOMAIN[index] for index in support), P) for support in supports
    ]
    rows: list[tuple[int, ...]] = []
    rhs: list[int] = []
    for block, (scalar, support_locator) in enumerate(
        zip(LABELS, support_locators, strict=True)
    ):
        columns = [shifted(R, shift, 5, P) for shift in range(3)] + [[0] * 5 for _ in range(9)]
        offset = 3 + 3 * block
        for shift in range(3):
            columns[offset + shift] = [(-entry) % P for entry in shifted(support_locator, shift, 5, P)]
        for degree in range(5):
            rows.append(tuple(column[degree] for column in columns))
            rhs.append(scalar * F[degree] % P)
    coefficient = tuple(rows)
    augmented = tuple(row + (entry,) for row, entry in zip(rows, rhs, strict=True))
    return Fibre(coefficient=coefficient, augmented=augmented)


def fibres(*, omit_last: bool = False) -> list[Fibre]:
    output = [
        full_fibre(supports)
        for supports in itertools.product(
            *(itertools.combinations(petal, 2) for petal in PETALS)
        )
    ]
    if omit_last:
        output.pop()
    return output


def matrix_payload_hash(items: list[Fibre]) -> str:
    payload = [
        {"A": fibre.coefficient, "H": fibre.augmented} for fibre in items
    ]
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def flat(rows: tuple[tuple[int, ...], ...]) -> str:
    return ",".join(str(entry) for row in rows for entry in row)


def singular_program(items: list[Fibre]) -> str:
    lines = [
        "ring r=19,(x),dp;",
        "int total=0;",
        "int rank12aug13=0;",
        "int rankdef=0;",
        "int consistent=0;",
        "int other=0;",
    ]
    for index, fibre in enumerate(items):
        lines.extend(
            [
                f"matrix A{index}[15][12]={flat(fibre.coefficient)};",
                f"matrix H{index}[15][13]={flat(fibre.augmented)};",
                "total=total+1;",
                f"if(rank(A{index})<12){{rankdef=rankdef+1;}}",
                f"if(rank(A{index})==rank(H{index})){{consistent=consistent+1;}}",
                (
                    f"if(rank(A{index})==12 && rank(H{index})==13)"
                    "{rank12aug13=rank12aug13+1;}else{other=other+1;}"
                ),
            ]
        )
    lines.extend(
        [
            'print("TOTAL="+string(total));',
            'print("RANK12_AUGMENTED13="+string(rank12aug13));',
            'print("COEFFICIENT_RANK_DEFICIENT="+string(rankdef));',
            'print("CONSISTENT="+string(consistent));',
            'print("OTHER="+string(other));',
            "quit;",
        ]
    )
    return "\n".join(lines) + "\n"


def m2_matrix(rows: tuple[tuple[int, ...], ...]) -> str:
    encoded_rows = [
        "{" + ",".join(f"{entry}_R" for entry in row) + "}" for row in rows
    ]
    return "matrix{" + ",".join(encoded_rows) + "}"


def macaulay2_program(items: list[Fibre]) -> str:
    lines = [
        "R=GF(19);",
        "total=0;",
        "rank12aug13=0;",
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
                "if rank A < 12 then rankdef=rankdef+1;",
                "if rank A == rank H then consistent=consistent+1;",
                (
                    "if rank A == 12 and rank H == 13 "
                    "then rank12aug13=rank12aug13+1 else other=other+1;"
                ),
            ]
        )
    lines.extend(
        [
            'print("TOTAL=" | toString total);',
            'print("RANK12_AUGMENTED13=" | toString rank12aug13);',
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
        "RANK12_AUGMENTED13": "rank12_augmented13",
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
        raise RuntimeError(f"{label} exceeded the 60-second verifier timeout") from error
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


def inverse_mod(value: int, p: int) -> int:
    value %= p
    if not value:
        raise ZeroDivisionError
    return pow(value, p - 2, p)


def rank_mod(rows: list[list[int]], p: int) -> int:
    work = [[entry % p for entry in row] for row in rows]
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
        work[rank] = [(scale * entry) % p for entry in work[rank]]
        for index in range(len(work)):
            if index == rank or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                (left - scale * right) % p
                for left, right in zip(work[index], work[rank], strict=True)
            ]
        rank += 1
    return rank


def solve3(rows: list[list[int]], rhs: list[int], p: int) -> list[int]:
    work = [row[:] + [value % p] for row, value in zip(rows, rhs, strict=True)]
    for column in range(3):
        pivot = next(index for index in range(column, 3) if work[index][column] % p)
        work[column], work[pivot] = work[pivot], work[column]
        scale = inverse_mod(work[column][column], p)
        work[column] = [(scale * entry) % p for entry in work[column]]
        for index in range(3):
            if index == column:
                continue
            scale = work[index][column] % p
            work[index] = [
                (left - scale * right) % p
                for left, right in zip(work[index], work[column], strict=True)
            ]
    return [work[index][-1] for index in range(3)]


def residual_matrix(p: int, pairs: tuple[tuple[int, int], ...]) -> list[list[int]]:
    points = [point for pair in pairs for point in pair]
    labels = [1, 1, 2, 2, 3, 3]
    r_value = lambda point: point * (point - 1) % p
    anchor = [
        [r_value(point) * pow(point, degree, p) % p for degree in range(3)]
        for point in points[:3]
    ]
    output = [[0] * 5 for _ in range(3)]
    for exponent in range(5):
        interpolation = solve3(
            anchor,
            [labels[index] * pow(points[index], exponent, p) % p for index in range(3)],
            p,
        )
        for row, point in enumerate(points[3:]):
            left = sum(
                interpolation[degree]
                * r_value(point)
                * pow(point, degree, p)
                for degree in range(3)
            )
            output[row][exponent] = (
                left - labels[row + 3] * pow(point, exponent, p)
            ) % p
    return output


def structural_census(p: int) -> dict[str, object]:
    rank_counts: Counter[int] = Counter()
    affine_counts: Counter[tuple[int, int]] = Counter()
    common_counts: Counter[int] = Counter()
    total = 0
    available = list(range(2, p))
    for pair1 in itertools.combinations(available, 2):
        remaining1 = [point for point in available if point not in pair1]
        for pair2 in itertools.combinations(remaining1, 2):
            remaining2 = [point for point in remaining1 if point not in pair2]
            for pair3 in itertools.combinations(remaining2, 2):
                pairs = (pair1, pair2, pair3)
                residual = residual_matrix(p, pairs)
                coefficient_rank = rank_mod([row[:4] for row in residual], p)
                augmented_rank = rank_mod(residual, p)
                gammas = [
                    (1 - u - v) * inverse_mod(u * v, p) % p for u, v in pairs
                ]
                total += 1
                rank_counts[coefficient_rank] += 1
                affine_counts[(coefficient_rank, augmented_rank)] += 1
                if len(set(gammas)) == 1:
                    common_counts[coefficient_rank] += 1
    return {
        "total": total,
        "rank": {str(key): value for key, value in sorted(rank_counts.items())},
        "affine": {
            f"rankC={key[0]},rankAug={key[1]}": value
            for key, value in sorted(affine_counts.items())
        },
        "common_involution": {
            str(key): value for key, value in sorted(common_counts.items())
        },
    }


def poly_eval(poly: tuple[int, ...], value: int, p: int) -> int:
    return sum(coefficient * pow(value, degree, p) for degree, coefficient in enumerate(poly)) % p


def quotient_witness(
    *, tamper_scalar: bool = False, tamper_recovery: bool = False
) -> dict[str, object]:
    p = 13
    pairs = ((2, 6), (8, 9), (4, 12))
    denominator_roots = (3, 7)
    R = locator((0, 1), p)
    B = locator(denominator_roots, p)
    scalar_a = 8 if tamper_scalar else 9
    gamma = (1 - pairs[0][0] - pairs[0][1]) * inverse_mod(
        pairs[0][0] * pairs[0][1], p
    ) % p
    residual = residual_matrix(p, pairs)
    coefficient_rank = rank_mod([row[:4] for row in residual], p)
    augmented_rank = rank_mod(residual, p)
    if (coefficient_rank, augmented_rank) != (2, 2):
        raise RuntimeError("quotient witness is not a compatible rank-two chart")
    identities = []
    for label, pair in zip((1, 2, 3), pairs, strict=True):
        difference = tuple(
            (scalar_a * R[index] - label * B[index]) % p for index in range(3)
        )
        values = [poly_eval(difference, point, p) for point in pair]
        if values != [0, 0]:
            raise RuntimeError("quotient fibre identity failed")
        identities.append({"label": label, "pair": pair, "difference": difference})
    all_pairs = ((0, 1),) + pairs + (denominator_roots,)
    gammas = [
        (1 - u - v) * inverse_mod(u * v, p) % p
        for u, v in all_pairs[1:]
    ]
    if any(value != gamma for value in gammas):
        raise RuntimeError("quotient witness involution gamma drift")
    split_root_sets = ((3, 5, 7, 10), (3, 5, 7, 11), (3, 7, 10, 11))
    migrations = []
    for roots in split_root_sets:
        F = locator(roots, p)
        if any(poly_eval(F, point, p) for point in roots):
            raise RuntimeError("split quartic construction failed")
        quotient, remainder = divmod_poly(F, B, p)
        if remainder != (0,):
            raise RuntimeError("common quadratic does not divide compatible quartic")
        V = tuple(scalar_a * entry % p for entry in quotient)
        W = poly_mul(R, V, p)
        for label, pair in zip((1, 2, 3), pairs, strict=True):
            numerator = poly_sub(W, tuple(label * entry % p for entry in F), p)
            support_locator = locator(pair, p)
            _, support_remainder = divmod_poly(numerator, support_locator, p)
            if support_remainder != (0,):
                raise RuntimeError("full quotient incidence identity failed")
        exactness_W = list(W)
        if tamper_recovery and roots == split_root_sets[0]:
            exactness_W[0] = (exactness_W[0] + 1) % p
        common = gcd_poly(F, tuple(exactness_W), p)
        if len(common) - 1 != 2:
            raise RuntimeError("rank-two witness failed the degree-two core-recovery gate")
        F_new, F_remainder = divmod_poly(F, common, p)
        W_new, W_remainder = divmod_poly(tuple(exactness_W), common, p)
        if F_remainder != (0,) or W_remainder != (0,):
            raise RuntimeError("core-recovery gcd division failed")
        recovered = sorted(root for root in roots if poly_eval(common, root, p) == 0)
        missed_after = sorted(root for root in roots if poly_eval(common, root, p) != 0)
        if len(recovered) != 2 or missed_after != [3, 7]:
            raise RuntimeError("rank-two exact defect did not migrate from four to two")
        migrations.append(
            {
                "original_F_roots": list(roots),
                "gcd_F_W": list(common),
                "recovered_core_roots": recovered,
                "migrated_missed_core_roots": missed_after,
                "F_new": list(F_new),
                "W_new": list(W_new),
                "route": "PROFILE_MIGRATION_CORE_RECOVERY",
            }
        )
    return {
        "verified": True,
        "p": p,
        "background": [0, 1],
        "support_pairs": [list(pair) for pair in pairs],
        "labels": [1, 2, 3],
        "quadratic_divisor_roots": list(denominator_roots),
        "scalar_a": scalar_a,
        "involution_gamma": gamma,
        "compatibility_coefficient_rank": coefficient_rank,
        "compatibility_augmented_rank": augmented_rank,
        "residual_matrix_columns_f0_f1_f2_f3_x4": residual,
        "split_compatible_quartic_roots": [list(roots) for roots in split_root_sets],
        "exact_profile_migrations": migrations,
        "exact_d4_survivors": 0,
        "fibre_identities": identities,
    }


def poly_sub(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    length = max(len(left), len(right))
    output = [0] * length
    for index in range(length):
        output[index] = (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        ) % p
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return tuple(output)


def divmod_poly(
    numerator: tuple[int, ...], denominator: tuple[int, ...], p: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    remainder = list(numerator)
    while len(remainder) > 1 and remainder[-1] == 0:
        remainder.pop()
    quotient = [0] * max(1, len(remainder) - len(denominator) + 1)
    inverse_lead = inverse_mod(denominator[-1], p)
    while len(remainder) >= len(denominator) and any(remainder):
        shift = len(remainder) - len(denominator)
        coefficient = remainder[-1] * inverse_lead % p
        quotient[shift] = coefficient
        for index, value in enumerate(denominator):
            remainder[index + shift] = (
                remainder[index + shift] - coefficient * value
            ) % p
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    while len(quotient) > 1 and quotient[-1] == 0:
        quotient.pop()
    return tuple(quotient), tuple(remainder or [0])


def gcd_poly(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    a = left
    b = right
    while b != (0,):
        _, remainder = divmod_poly(a, b, p)
        a, b = b, remainder
    inverse_lead = inverse_mod(a[-1], p)
    return tuple(coefficient * inverse_lead % p for coefficient in a)


def moving_support_ledger() -> dict[str, object]:
    rows = []
    for q, K, M, b in ((19, 4, 3, 2), (23, 4, 4, 2), (47, 4, 10, 2)):
        charts = comb(b, 2) * comb(M, 3) * comb(4, 2) ** 3
        rows.append(
            {
                "q": q,
                "n": K + 4 * M + b,
                "selected_support_charts": charts,
                "exact_d4_upper_bound": charts * q,
                "old_cofactor_upper_bound": charts * q**3,
            }
        )
    return {
        "formula": "binom(b,2)*binom(M,3)*216*q",
        "rank2_exact_d4_charge": 0,
        "rows": rows,
    }


def verify(*, omit_last: bool = False) -> dict[str, object]:
    items = fibres(omit_last=omit_last)
    singular = shutil.which("Singular")
    macaulay2 = shutil.which("M2")
    if singular is None or macaulay2 is None:
        missing = [
            name
            for name, path in (("Singular", singular), ("M2", macaulay2))
            if path is None
        ]
        raise RuntimeError("missing required CAS: " + ", ".join(missing))
    singular_counts = run_program(
        [singular, "-q"], singular_program(items), "Singular"
    )
    macaulay2_counts = run_macaulay2_program(
        macaulay2,
        macaulay2_program(items),
        "Macaulay2",
    )
    structural = {p: structural_census(p) for p in (11, 13)}
    payload_hash = matrix_payload_hash(items)
    moving = moving_support_ledger()
    return {
        "schema": "rs-mca-l1-b9-boundary-222-cas-v2",
        "status": "EXPERIMENTAL/LOCAL_LEMMA_CHECK",
        "matrix_payload_sha256": payload_hash,
        "singular": singular_counts,
        "macaulay2": macaulay2_counts,
        "cross_cas_equal": singular_counts == macaulay2_counts,
        "matches_expected_cas": (
            singular_counts == EXPECTED_CAS and macaulay2_counts == EXPECTED_CAS
        ),
        "matches_frozen_payload": payload_hash == EXPECTED_PAYLOAD_SHA256,
        "structural_censuses": structural,
        "matches_expected_structural": all(
            structural[p] == EXPECTED_STRUCTURAL[p] for p in (11, 13)
        ),
        "quotient_witness": quotient_witness(),
        "moving_support_ledger": moving,
        "matches_expected_moving_support": moving == EXPECTED_MOVING_SUPPORT,
        "nonclaims": [
            "does not compute the generic Groebner saturation",
            "does not prove a moving-support incidence bound",
            "does not promote the empty p=19 fixture to an asymptotic theorem",
            "does not use rational quotient ownership for the exact rank-two removal",
            "does not show that non-exact rational quotient witnesses are paid by an existing quotient owner",
            "does not close B11 or the global mixed-petal bucket",
        ],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.tamper_selftest:
        tampered = verify(omit_last=True)
        quotient_mutation_caught = False
        recovery_mutation_caught = False
        moving_mutation_caught = False
        try:
            quotient_witness(tamper_scalar=True)
        except RuntimeError:
            quotient_mutation_caught = True
        try:
            quotient_witness(tamper_recovery=True)
        except RuntimeError:
            recovery_mutation_caught = True
        tampered_moving = moving_support_ledger()
        tampered_moving["rows"][0]["exact_d4_upper_bound"] += 1
        moving_mutation_caught = tampered_moving != EXPECTED_MOVING_SUPPORT
        if (
            tampered["matches_expected_cas"]
            or tampered["matches_frozen_payload"]
            or not quotient_mutation_caught
            or not recovery_mutation_caught
            or not moving_mutation_caught
        ):
            print("RESULT: FAIL (omitted-fibre mutation went undetected)")
            return 1
        print(
            "[PASS] omitted p=19 fibre and mutations of quotient, core recovery, and moving ledger rejected"
        )
        print("RESULT: PASS (B9-boundary CAS tamper self-test)")
        return 0
    report = verify()
    passed = all(
        [
            report["cross_cas_equal"],
            report["matches_expected_cas"],
            report["matches_frozen_payload"],
            report["matches_expected_structural"],
            report["quotient_witness"]["verified"],
            report["quotient_witness"]["exact_d4_survivors"] == 0,
            len(report["quotient_witness"]["exact_profile_migrations"]) == 3,
            report["matches_expected_moving_support"],
        ]
    )
    if args.json or not passed:
        print(json.dumps(report, indent=2, sort_keys=True))
    if not passed:
        print("RESULT: FAIL (B9-boundary independent CAS drift)")
        return 1
    print(
        "[PASS] Singular=Macaulay2: 216 systems, rank(A)=12, "
        "rank([A|b])=13; GF(11)/GF(13) censuses reproduced; "
        "rank2 split witnesses migrate d=4 to d=2"
    )
    print("RESULT: PASS (independent B9-boundary CAS and quotient check)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
