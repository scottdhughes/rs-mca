#!/usr/bin/env sage
"""CRT verifier for the fixed-syndrome ``(3,2,1)`` rank dichotomy.

Let ``R`` have degree two and let the pairwise-coprime selected-support
locators ``B_i`` have degrees ``(3,2,1)``.  For distinct nonzero labels
``c_i``, define the CRT multiplier ``G`` modulo ``B=prod(B_i)`` by

    G = c_i R^(-1) mod B_i.

Then ``R*V-c_i*F`` is divisible by ``B_i`` for all ``i`` exactly when

    V = F*G mod B,       deg(V) <= 2.

Thus the three compatibility equations are the coefficients of degrees
``3,4,5`` of ``F*G mod B``.  The displayed proof certificate verifies the
triangular inverse step used in the local lemma and runs exact structural
finite-field controls.  It is not a global mixed-petal theorem.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

from sage.all import GF, PolynomialRing, QQ, matrix


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-boundary-321/dichotomy_certificate.json"
)
REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/l1_b9_boundary_321_independent_review.md"
)


def sha256_json(value):
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=int
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def locator(PX, X, roots):
    output = PX.one()
    for root in roots:
        output *= X - root
    return output


def crt_multiplier(PX, X, R, support_locators, labels):
    B = PX.one()
    for support_locator in support_locators:
        B *= support_locator
    G = PX.zero()
    for support_locator, label in zip(
        support_locators, labels, strict=True
    ):
        target = (label * R.inverse_mod(support_locator)) % support_locator
        complement = B // support_locator
        idempotent = (
            complement * complement.inverse_mod(support_locator)
        ) % B
        G = (G + target * idempotent) % B
    if G.gcd(B) != 1:
        raise RuntimeError("CRT multiplier must be a unit modulo B")
    return B, G


def compatibility_record(
    PX, X, R, support_locators, labels, *, include_coefficients=False
):
    B, G = crt_multiplier(PX, X, R, support_locators, labels)
    columns = []
    for degree in range(5):
        remainder = (X**degree * G) % B
        columns.append([remainder[index] for index in range(3, 6)])
    full = matrix(PX.base_ring(), 3, 5, lambda row, column: columns[column][row])
    lower = full.matrix_from_columns(range(4))
    lower_rank = int(lower.rank())
    full_rank = int(full.rank())
    J = G.inverse_mod(B) % B
    compatible_rank_drop = lower_rank < 3 and full_rank == lower_rank
    record = {
        "lower_rank": lower_rank,
        "full_rank": full_rank,
        "affine_monic_compatible": full_rank == lower_rank,
        "compatible_rank_drop": compatible_rank_drop,
        "inverse_degree": int(J.degree()),
    }
    if include_coefficients:
        record.update(
            {
                "B_coefficients_low_to_high": [
                    int(coefficient) for coefficient in B
                ],
                "G_coefficients_low_to_high": [
                    int(coefficient) for coefficient in G
                ],
                "J_coefficients_low_to_high": [
                    int(coefficient) for coefficient in J
                ],
            }
        )
    return record


def symbolic_inverse_triangle():
    coefficients = PolynomialRing(
        QQ,
        names=("b0", "b1", "b2", "b3", "b4", "b5", "j0", "j1", "j2", "j3", "j4", "j5"),
    )
    (
        b0,
        b1,
        b2,
        b3,
        b4,
        b5,
        j0,
        j1,
        j2,
        j3,
        j4,
        j5,
    ) = coefficients.gens()
    PX = PolynomialRing(coefficients, "X")
    X = PX.gen()
    B = X**6 + b5 * X**5 + b4 * X**4 + b3 * X**3 + b2 * X**2 + b1 * X + b0
    J = j0 + j1 * X + j2 * X**2 + j3 * X**3 + j4 * X**4 + j5 * X**5
    top = [((X**degree * J) % B)[5] for degree in range(3)]
    expected = [
        j5,
        j4 - b5 * j5,
        j3 - b5 * j4 + (b5**2 - b4) * j5,
    ]
    passed = all(left == right for left, right in zip(top, expected, strict=True))
    return {
        "coefficient_X5_of_J_xJ_x2J_mod_B": [str(value) for value in top],
        "triangular_expected": [str(value) for value in expected],
        "passed": passed,
        "consequence": "if J*P_2 is contained in P_4, then j5=j4=j3=0 and deg(J)<=2",
    }


def normalized_structural_census(p):
    field = GF(p)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    R = locator(PX, X, (field(0), field(1)))
    labels = (field(1), field(2), field(3))
    available = tuple(field(value) for value in range(2, p))
    histogram = Counter()
    rank_drop_inverse_degrees = Counter()
    compatible_rank_drops = []
    transcript_digest = hashlib.sha256()
    chart_count = 0
    for cubic_roots in itertools.combinations(available, 3):
        after_cubic = tuple(point for point in available if point not in cubic_roots)
        for quadratic_roots in itertools.combinations(after_cubic, 2):
            after_quadratic = tuple(
                point for point in after_cubic if point not in quadratic_roots
            )
            for linear_root in after_quadratic:
                roots = (cubic_roots, quadratic_roots, (linear_root,))
                support_locators = [locator(PX, X, block) for block in roots]
                record = compatibility_record(
                    PX, X, R, support_locators, labels
                )
                key = (
                    f"lowerRank={record['lower_rank']},"
                    f"fullRank={record['full_rank']}"
                )
                histogram[key] += 1
                if record["lower_rank"] < 3:
                    rank_drop_inverse_degrees[str(record["inverse_degree"])] += 1
                if record["compatible_rank_drop"]:
                    detailed = compatibility_record(
                        PX,
                        X,
                        R,
                        support_locators,
                        labels,
                        include_coefficients=True,
                    )
                    compatible_rank_drops.append(
                        {
                            "roots": [
                                [int(point) for point in block] for block in roots
                            ],
                            "record": detailed,
                        }
                    )
                transcript_row = {
                    "roots": [
                        [int(point) for point in block] for block in roots
                    ],
                    "lower_rank": record["lower_rank"],
                    "full_rank": record["full_rank"],
                    "inverse_degree": record["inverse_degree"],
                }
                transcript_digest.update(
                    json.dumps(
                        transcript_row,
                        sort_keys=True,
                        separators=(",", ":"),
                        default=int,
                    ).encode("ascii")
                )
                transcript_digest.update(b"\n")
                chart_count += 1
    expected_count = (
        len(tuple(itertools.combinations(available, 3)))
        * len(tuple(itertools.combinations(range(p - 5), 2)))
        * (p - 7)
    )
    if chart_count != expected_count:
        raise RuntimeError(
            f"normalized structural census drift: {chart_count} != {expected_count}"
        )
    return {
        "field": p,
        "normalization": "R=X(X-1), labels=(1,2,3), degrees=(3,2,1)",
        "chart_count": chart_count,
        "rank_histogram": dict(sorted(histogram.items())),
        "rank_drop_inverse_degree_histogram": dict(
            sorted(rank_drop_inverse_degrees.items())
        ),
        "compatible_rank_drop_count": len(compatible_rank_drops),
        "compatible_rank_drops": compatible_rank_drops,
        "transcript_sha256": transcript_digest.hexdigest(),
    }


def sequential_p19_census():
    p = 19
    field = GF(p)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    domain = tuple(field(value) for value in (1, 2, 4, 8, 16, 13, 7, 14, 9, 18, 17, 15, 11, 3, 6, 12, 5, 10))
    petals = (tuple(range(4, 8)), tuple(range(8, 12)), tuple(range(12, 16)))
    background = tuple(range(16, 18))
    labels = (field(1), field(2), field(3))
    R = locator(PX, X, tuple(domain[index] for index in background))
    histogram = Counter()
    inverse_degree_histogram = Counter()
    rank_drop_patterns = []
    transcript_digest = hashlib.sha256()
    chart_count = 0
    for sizes in itertools.permutations((3, 2, 1)):
        choices = [
            tuple(itertools.combinations(petal, size))
            for petal, size in zip(petals, sizes, strict=True)
        ]
        for supports in itertools.product(*choices):
            support_locators = [
                locator(
                    PX,
                    X,
                    tuple(domain[index] for index in support),
                )
                for support in supports
            ]
            record = compatibility_record(PX, X, R, support_locators, labels)
            key = (
                f"lowerRank={record['lower_rank']},"
                f"fullRank={record['full_rank']}"
            )
            histogram[key] += 1
            inverse_degree_histogram[str(record["inverse_degree"])] += 1
            if record["lower_rank"] < 3:
                detailed = compatibility_record(
                    PX,
                    X,
                    R,
                    support_locators,
                    labels,
                    include_coefficients=True,
                )
                rank_drop_patterns.append(
                    {
                        "sizes_by_labelled_petal": list(sizes),
                        "supports": [list(support) for support in supports],
                        "record": detailed,
                    }
                )
            transcript_row = {
                "sizes": list(sizes),
                "supports": [list(support) for support in supports],
                "lower_rank": record["lower_rank"],
                "full_rank": record["full_rank"],
                "inverse_degree": record["inverse_degree"],
            }
            transcript_digest.update(
                json.dumps(
                    transcript_row,
                    sort_keys=True,
                    separators=(",", ":"),
                    default=int,
                ).encode("ascii")
            )
            transcript_digest.update(b"\n")
            chart_count += 1
    if chart_count != 576:
        raise RuntimeError("sequential GF(19) support-pattern count drift")
    return {
        "field": p,
        "layout": "sequential (19,18,5,8), all six size assignments",
        "chart_count": chart_count,
        "rank_histogram": dict(sorted(histogram.items())),
        "inverse_degree_histogram": dict(sorted(inverse_degree_histogram.items())),
        "rank_drop_patterns": rank_drop_patterns,
        "compatible_rank_drop_count": sum(
            int(pattern["record"]["compatible_rank_drop"])
            for pattern in rank_drop_patterns
        ),
        "transcript_sha256": transcript_digest.hexdigest(),
    }


def build_report():
    if not REVIEW_PATH.exists():
        raise RuntimeError(f"missing independent review: {REVIEW_PATH}")
    review_text = REVIEW_PATH.read_text(encoding="utf-8")
    review_pass = (
        "**GREEN.**" in review_text
        and "fresh-context Codex proof audit" in review_text
        and "573q=10,887" in review_text
    )
    symbolic = symbolic_inverse_triangle()
    normalized = [normalized_structural_census(p) for p in (11, 13)]
    sequential = sequential_p19_census()
    exact_controls_pass = (
        symbolic["passed"]
        and all(row["compatible_rank_drop_count"] == 0 for row in normalized)
        and sequential["compatible_rank_drop_count"] == 0
        and sequential["rank_histogram"]
        == {"lowerRank=2,fullRank=3": 2, "lowerRank=3,fullRank=3": 574}
    )
    return {
        "schema": "rs-mca-l1-b9-boundary-321-dichotomy-v2",
        "status": "PROVED_LOCAL_CRT_LEMMA_INDEPENDENTLY_REVIEWED",
        "statement": (
            "for disjoint degree-(2;3,2,1) locators and distinct nonzero "
            "labels, every moving-monic-F rank drop is affine-inconsistent; "
            "full-rank charts contain at most q monic quartics"
        ),
        "parameters": {
            "deg_R": 2,
            "support_locator_degrees": [3, 2, 1],
            "deg_F": 4,
            "deg_V_max": 2,
            "label_hypothesis": "pairwise distinct and nonzero",
            "locator_hypothesis": "R,B1,B2,B3 pairwise coprime and monic",
        },
        "compatibility_equations": {
            "B": "B1*B2*B3, degree 6",
            "G": "G == c_i*R^(-1) mod B_i",
            "equations": "coefficients X^3,X^4,X^5 of (F*G mod B) vanish",
            "lower_coefficient_map_shape": [3, 4],
            "monic_column": "the X^4 column of the full 3x5 map",
            "original_rank_relation": (
                "rank(C_15x16)=rank(A_15x12)+rank(reduced_3x4)="
                "12+rank(reduced_3x4)"
            ),
        },
        "independent_review": {
            "path": str(REVIEW_PATH.relative_to(ROOT)),
            "sha256": hashlib.sha256(REVIEW_PATH.read_bytes()).hexdigest(),
            "verdict": "GREEN" if review_pass else "REVIEW_RECORD_INVALID",
        },
        "proof_certificate": {
            "steps": [
                "CRT converts the three divisibility equations to V=F*G mod B with deg(V)<=2",
                "rank below three plus monic compatibility makes the full 3x5 map have rank at most two",
                "with J=G^(-1) mod B, this forces J*P_2 to be contained in P_4",
                "the symbolic triangular coefficients force deg(J)<=2",
                "a monic quartic in J*P_2 forces deg(J)=2",
                "the cubic B_j then forces J=c_j^(-1)R as polynomials",
                "any other positive-degree B_i and c_i!=c_j contradict gcd(R,B_i)=1",
            ],
            "symbolic_inverse_triangle": symbolic,
        },
        "exact_controls": {
            "normalized_structural": normalized,
            "sequential_GF19": sequential,
            "all_pass": exact_controls_pass,
        },
        "ledger_consequence": {
            "full_rank_charge_per_support_pattern": "q",
            "rank_drop_charge": 0,
            "periodic_patterns_removed_in_frozen_GF19_layout": 3,
            "conservative_primitive_charge": "573*q",
            "at_q_19": 573 * 19,
            "standalone_profile_charge_including_periodic_bucket": 3 + 573 * 19,
        },
        "theorem_problem_id": "L1 B9 fixed-syndrome (3,2,1) moving-quartic rank dichotomy",
        "proof_status": {
            "proved_locally": [
                "the CRT equivalence and inverse-degree contradiction under the printed hypotheses",
                "the q bound on every full-rank support chart",
                "zero monic contribution from every rank-drop chart under the printed hypotheses",
            ],
            "independently_reviewed": [
                "the CRT kernel argument and all locator/label hypotheses",
                "the exact count of three separately-paid periodic support patterns",
                "the post-periodic primitive residual charge 573*q",
            ],
            "still_required": ["classification of the next remaining profile"],
        },
        "nonclaims": [
            "repeated or zero labels are not covered",
            "overlapping support or background locators are not covered",
            "no m>2 profile is covered",
            "no statement about PR #763 is made",
            "the global mixed-petal theorem is not closed",
        ],
        "verdict": (
            "GREEN_LOCAL_LEMMA_INDEPENDENTLY_REVIEWED"
            if exact_controls_pass and review_pass
            else "RED_CERTIFICATE_FAILURE"
        ),
    }


def validate_report(report):
    controls = report["exact_controls"]
    normalized = controls["normalized_structural"]
    sequential = controls["sequential_GF19"]
    return (
        report["schema"] == "rs-mca-l1-b9-boundary-321-dichotomy-v2"
        and report["proof_certificate"]["symbolic_inverse_triangle"]["passed"]
        and report["independent_review"]["verdict"] == "GREEN"
        and controls["all_pass"]
        and [row["chart_count"] for row in normalized] == [5040, 27720]
        and all(row["compatible_rank_drop_count"] == 0 for row in normalized)
        and sequential["chart_count"] == 576
        and sequential["rank_histogram"]
        == {"lowerRank=2,fullRank=3": 2, "lowerRank=3,fullRank=3": 574}
        and sequential["compatible_rank_drop_count"] == 0
        and report["ledger_consequence"]["at_q_19"] == 10887
        and report["ledger_consequence"][
            "standalone_profile_charge_including_periodic_bucket"
        ] == 10890
    )


def tamper_selftest(report):
    mutations = []
    changed = copy.deepcopy(report)
    changed["independent_review"]["verdict"] = "YELLOW"
    mutations.append(("independent_review", changed))
    changed = copy.deepcopy(report)
    changed["proof_certificate"]["symbolic_inverse_triangle"]["passed"] = False
    mutations.append(("symbolic_triangle", changed))
    changed = copy.deepcopy(report)
    changed["exact_controls"]["normalized_structural"][0][
        "compatible_rank_drop_count"
    ] = 1
    mutations.append(("compatible_rank_drop", changed))
    changed = copy.deepcopy(report)
    changed["exact_controls"]["sequential_GF19"]["rank_histogram"][
        "lowerRank=2,fullRank=3"
    ] += 1
    mutations.append(("GF19_rank_histogram", changed))
    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["at_q_19"] += 1
    mutations.append(("ledger_charge", changed))
    failed = False
    for name, changed in mutations:
        caught = not validate_report(changed)
        print(f"  tamper {name:<26}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))
    if args.tamper_selftest and CERTIFICATE_PATH.exists():
        frozen = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
        if not validate_report(frozen):
            print("RESULT: FAIL (frozen certificate invalid)", file=sys.stderr)
            return 1
        return tamper_selftest(frozen)
    report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (dichotomy certificate validation)", file=sys.stderr)
        return 1
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True, default=int) + "\n",
            encoding="utf-8",
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, default=int))
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != report:
        print("RESULT: FAIL (frozen dichotomy certificate drift)", file=sys.stderr)
        return 1
    controls = report["exact_controls"]
    print("l1 B9 boundary (3,2,1) CRT rank dichotomy")
    print(f"  statement: {report['statement']}")
    print(f"  equations: {report['compatibility_equations']['equations']}")
    for row in controls["normalized_structural"]:
        print(
            f"  GF({row['field']}): charts={row['chart_count']}, "
            f"ranks={row['rank_histogram']}, "
            f"compatible_rank_drops={row['compatible_rank_drop_count']}"
        )
    sequential = controls["sequential_GF19"]
    print(
        f"  GF(19): charts={sequential['chart_count']}, "
        f"ranks={sequential['rank_histogram']}, "
        f"compatible_rank_drops={sequential['compatible_rank_drop_count']}"
    )
    print(
        "  ledger: conservative primitive charge="
        f"{report['ledger_consequence']['at_q_19']}"
    )
    print(f"  theorem/problem: {report['theorem_problem_id']}")
    print(f"  proof status: {report['status']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(int(main(sys.argv[1:])))
