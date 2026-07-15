#!/usr/bin/env sage
"""Exact GF(19) census for the residual ``(3,1,3,(2,2,2))`` profile.

For a retained background locator ``R`` of degree one, a missed-core locator
``F`` of degree three, and three selected-support locators ``B_i`` of degree
two, the divided fixed-syndrome equations are

    R*V - c_i*F = B_i*A_i,

with ``deg(V)<=2`` and ``deg(A_i)<=1``.  The fixed-``F`` matrix is ``12 x 9``.
Adjoining the three lower coefficients of a monic cubic gives a square
``12 x 12`` moving-``F`` system.

The script enumerates all 432 labelled support patterns in the frozen
sequential GF(19) sunflower, solves the exact moving system, restricts ambient
monic cubics to the four actual missed-core locators, and rechecks every valid
candidate on the full evaluation domain.  This is a finite falsification and
rank-stratum packet, not a uniform theorem or a ledger payment.
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

from sage.all import GF, PolynomialRing, matrix, vector


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "experimental/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    img_list,
    stabilizer_order,
    subgroup,
    sunflower_word_from_blocks,
)


CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222/certificate.json"
)
OWNER_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31222-owner-partition/certificate.json"
)


def sha256_json(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=int
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def locator(PX, X, field, domain, indices):
    output = PX.one()
    for index in indices:
        output *= X - field(domain[index])
    return output


def agreement_mask(poly, values, domain, field):
    mask = 0
    for index, point in enumerate(domain):
        if int(poly(field(point))) == int(values[index]):
            mask |= 1 << index
    return mask


def profile(mask, core, petals, background):
    agreement = {index for index in range(18) if mask & (1 << index)}
    return {
        "d": len(set(core) - agreement),
        "r": len(set(background) & agreement),
        "a_i": sorted(
            [len(set(petal) & agreement) for petal in petals if set(petal) & agreement],
            reverse=True,
        ),
        "agreement_size": len(agreement),
    }


def coefficient_matrix(PX, X, field, R, support_locators):
    columns = [R * X**degree for degree in range(3)]
    offsets = []
    for support_locator in support_locators:
        offsets.append(len(columns))
        columns.extend(-support_locator * X**degree for degree in range(2))
    if len(columns) != 9:
        raise RuntimeError(f"expected 9 fixed columns, found {len(columns)}")

    rows = []
    for block in range(3):
        active = [PX.zero()] * len(columns)
        for degree in range(3):
            active[degree] = columns[degree]
        offset = offsets[block]
        for degree in range(2):
            active[offset + degree] = columns[offset + degree]
        for coefficient_degree in range(4):
            rows.append([poly[coefficient_degree] for poly in active])
    return matrix(field, rows)


def fixed_rhs(field, F, labels):
    return vector(
        field,
        [
            field(label) * F[degree]
            for label in labels
            for degree in range(4)
        ],
    )


def moving_monic_system(A, labels, field):
    rows = []
    rhs = []
    for block, label in enumerate(labels):
        for degree in range(4):
            row = list(A.row(4 * block + degree))
            row.extend(
                -field(label) if degree == lower_degree else field.zero()
                for lower_degree in range(3)
            )
            rows.append(row)
            rhs.append(field(label) if degree == 3 else field.zero())
    return matrix(field, rows), vector(field, rhs)


def affine_solutions(C, rhs, field, max_solutions=100_000):
    rank_C = C.rank()
    rank_augmented = C.augment(rhs.column()).rank()
    if rank_C != rank_augmented:
        return rank_C, rank_augmented, []
    basis = C.right_kernel().basis()
    solution_count = int(field.order()) ** len(basis)
    if solution_count > max_solutions:
        raise RuntimeError(f"affine fibre too large: {solution_count}")
    particular = C.solve_right(rhs)
    solutions = []
    for coefficients in itertools.product(
        range(int(field.order())), repeat=len(basis)
    ):
        solution = vector(field, particular)
        for coefficient, basis_vector in zip(
            coefficients, basis, strict=True
        ):
            solution += field(coefficient) * basis_vector
        solutions.append(solution)
    return rank_C, rank_augmented, solutions


def normalize_direction(values, p):
    first = next((value % p for value in values if value % p), None)
    if first is None:
        raise ValueError("zero affine-line direction")
    inverse = pow(int(first), -1, p)
    return [int(value * inverse % p) for value in values]


def cubic_affine_line_record(solutions, valid_F, p):
    points = sorted(
        {
            tuple(int(solution[9 + degree]) for degree in range(3))
            for solution in solutions
        }
    )
    if len(points) != p:
        raise RuntimeError(f"expected {p} cubic coefficient points, found {len(points)}")
    base = points[0]
    other = next(point for point in points[1:] if point != base)
    direction = normalize_direction(
        [(right - left) % p for left, right in zip(base, other, strict=True)],
        p,
    )
    valid_lower = {
        tuple(coefficients[degree] for degree in range(3))
        for coefficients in valid_F
    }
    intersections = sorted(set(points) & valid_lower)
    return {
        "base_lower_coefficients": list(base),
        "normalized_direction": direction,
        "ambient_monic_cubic_count": len(points),
        "coefficient_points_sha256": sha256_json(points),
        "actual_missed_core_intersections": [list(point) for point in intersections],
    }


def build_report():
    p, n, k, sigma = 19, 18, 5, 3
    field = GF(p)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    domain = subgroup(p, n)
    core = tuple(range(4))
    petals = (
        tuple(range(4, 8)),
        tuple(range(8, 12)),
        tuple(range(12, 16)),
    )
    background = tuple(range(16, 18))
    labels = (1, 2, 3)
    word = sunflower_word_from_blocks(
        p,
        n,
        k,
        k + sigma,
        list(core),
        [list(petal) for petal in petals],
        "sunflower-sequential-m3",
    )
    if word is None:
        raise RuntimeError("failed to construct the sequential sunflower")
    values = word["values"]
    core_locator = locator(PX, X, field, domain, core)
    missed_core_data = []
    for missed in itertools.combinations(core, 3):
        F = locator(PX, X, field, domain, missed)
        H = core_locator // F
        missed_core_data.append((tuple(missed), F, H))
    valid_F = {tuple(int(coefficient) for coefficient in F): (missed, H)
               for missed, F, H in missed_core_data}

    fixed_rank_histogram = Counter()
    moving_rank_histogram = Counter()
    fixed_matrix_rank_histogram = Counter()
    support_status_histogram = Counter()
    rankdrop_status_histogram = Counter()
    ambient_solution_total = 0
    compatible_support_patterns = 0
    valid_core_locator_solutions = 0
    exact_target_solution_occurrences = 0
    exact_target_words = {}
    exceptional_patterns = []
    compatible_rankdrop_templates = []
    transcript = []

    for background_support in itertools.combinations(background, 1):
        R = locator(PX, X, field, domain, background_support)
        support_choices = [
            tuple(itertools.combinations(petal, 2)) for petal in petals
        ]
        for supports in itertools.product(*support_choices):
            support_locators = [
                locator(PX, X, field, domain, support) for support in supports
            ]
            A = coefficient_matrix(PX, X, field, R, support_locators)
            rank_A = int(A.rank())
            fixed_matrix_rank_histogram[str(rank_A)] += 1
            fixed_rows = []
            for missed, F, _H in missed_core_data:
                rhs_F = fixed_rhs(field, F, labels)
                rank_aug_F = int(A.augment(rhs_F.column()).rank())
                fixed_rank_histogram[
                    f"rankA={rank_A},rankAug={rank_aug_F}"
                ] += 1
                fixed_rows.append(
                    {"missed_core": list(missed), "rank_augmented": rank_aug_F}
                )

            C, monic_rhs = moving_monic_system(A, labels, field)
            rank_C, rank_C_augmented, solutions = affine_solutions(
                C, monic_rhs, field
            )
            moving_rank_histogram[
                f"rankC={rank_C},rankAug={rank_C_augmented}"
            ] += 1
            if rank_C == 12:
                rankdrop_status = "FULL_RANK"
            elif rank_C_augmented > rank_C:
                rankdrop_status = "AFFINE_INCONSISTENT_RANKDROP"
            else:
                rankdrop_status = "UNPAID_RANKDROP_TEMPLATE"
            rankdrop_status_histogram[rankdrop_status] += 1
            ambient_solution_total += len(solutions)
            compatible_support_patterns += bool(solutions)
            exact_in_pattern = []
            valid_in_pattern = 0
            for solution in solutions:
                V = sum(solution[degree] * X**degree for degree in range(3))
                F = X**3 + sum(
                    solution[9 + degree] * X**degree for degree in range(3)
                )
                F_key = tuple(int(coefficient) for coefficient in F)
                if F_key not in valid_F:
                    continue
                valid_in_pattern += 1
                valid_core_locator_solutions += 1
                missed, H = valid_F[F_key]
                W = R * H * V
                mask = agreement_mask(W, values, domain, field)
                row = profile(mask, core, petals, background)
                if row["d"] == 3 and row["r"] == 1 and row["a_i"] == [2, 2, 2]:
                    exact_target_solution_occurrences += 1
                    evaluations = tuple(int(W(field(point))) for point in domain)
                    record = {
                        "background_support": list(background_support),
                        "petal_supports": [list(support) for support in supports],
                        "missed_core": list(missed),
                        "agreement_mask": int(mask),
                        "agreement_set": [
                            index for index in range(n) if mask & (1 << index)
                        ],
                        "agreement_stabilizer_order": stabilizer_order(mask, n),
                        "V_coefficients_low_to_high": [
                            int(V[degree]) for degree in range(3)
                        ],
                        "F_coefficients_low_to_high": [
                            int(F[degree]) for degree in range(4)
                        ],
                    }
                    exact_in_pattern.append(record)
                    exact_target_words.setdefault(evaluations, record)

            if not solutions:
                support_status = "ZERO_AFFINE_INCOMPATIBLE"
            elif exact_in_pattern:
                support_status = "REALIZES_EXACT_TARGET"
            else:
                support_status = "ZERO_NO_EXACT_TARGET_IN_AMBIENT_FIBRE"
            support_status_histogram[support_status] += 1
            if rank_C < 12 or rank_C != rank_C_augmented or exact_in_pattern:
                affine_line = (
                    cubic_affine_line_record(solutions, valid_F, p)
                    if rankdrop_status == "UNPAID_RANKDROP_TEMPLATE"
                    else None
                )
                if affine_line is not None:
                    compatible_rankdrop_templates.append(
                        {
                            "background_support": list(background_support),
                            "petal_supports": [list(support) for support in supports],
                            "rank_C": int(rank_C),
                            "rank_C_augmented": int(rank_C_augmented),
                            "affine_monic_cubic_line": affine_line,
                            "owner": "UNPAID_RANKDROP_TEMPLATE",
                        }
                    )
                exceptional_patterns.append(
                    {
                        "background_support": list(background_support),
                        "petal_supports": [list(support) for support in supports],
                        "rank_A": rank_A,
                        "rank_C": int(rank_C),
                        "rank_C_augmented": int(rank_C_augmented),
                        "ambient_solution_count": len(solutions),
                        "valid_core_locator_solution_count": valid_in_pattern,
                        "exact_target_solutions": exact_in_pattern,
                        "support_status": support_status,
                        "rankdrop_status": rankdrop_status,
                        "affine_monic_cubic_line": affine_line,
                    }
                )
            transcript.append(
                {
                    "background_support": list(background_support),
                    "petal_supports": [list(support) for support in supports],
                    "rank_A": rank_A,
                    "fixed_F_rows": fixed_rows,
                    "rank_C": int(rank_C),
                    "rank_C_augmented": int(rank_C_augmented),
                    "ambient_solution_count": len(solutions),
                    "valid_core_locator_solution_count": valid_in_pattern,
                    "exact_target_solution_count": len(exact_in_pattern),
                    "support_status": support_status,
                    "rankdrop_status": rankdrop_status,
                }
            )

    if len(transcript) != 432:
        raise RuntimeError(f"support-pattern count drift: {len(transcript)}")

    decoded = img_list(values, domain, k, k + sigma, p, "support")
    planted = {
        tuple(
            int((field(label) * core_locator)(field(point))) for point in domain
        )
        for label in labels
    }
    decoded_words = set(decoded)
    if not planted.issubset(decoded_words):
        raise RuntimeError("planted words missing from exact decoder")
    decoded_targets = []
    for codeword, mask in decoded.items():
        row = profile(mask, core, petals, background)
        if row["d"] == 3 and row["r"] == 1 and row["a_i"] == [2, 2, 2]:
            decoded_targets.append(
                {
                    "codeword": list(map(int, codeword)),
                    "agreement_mask": int(mask),
                    "agreement_set": [
                        index for index in range(n) if mask & (1 << index)
                    ],
                    "stabilizer_order": stabilizer_order(mask, n),
                }
            )
    if set(exact_target_words) != {
        tuple(int(value) for value in row["codeword"]) for row in decoded_targets
    }:
        raise RuntimeError("rank census and independent decoder target sets disagree")

    owner_link = json.loads(OWNER_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if owner_link["schema"] != "rs-mca-l1-b9-frontier-31222-owner-partition-v3":
        raise RuntimeError("owner certificate schema drift")
    return {
        "schema": "rs-mca-l1-b9-frontier-31222-census-v1",
        "status": "EXPERIMENTAL/EXACT_FINITE_GF19_CENSUS",
        "statement": (
            "classify the exact fixed and moving cubic systems for all 432 "
            "support patterns in (ell,d,r,t,a_i)=(4,3,1,3,(2,2,2))"
        ),
        "input": {
            "p": p,
            "n": n,
            "k": k,
            "sigma": sigma,
            "ell": 4,
            "core": list(core),
            "petals": [list(petal) for petal in petals],
            "background": list(background),
            "labels": list(labels),
            "domain": list(map(int, domain)),
        },
        "frozen_system": {
            "equations": "R*V-c_i*F=B_i*A_i",
            "degrees": {
                "R": 1,
                "V_max": 2,
                "F_monic": 3,
                "B_i": [2, 2, 2],
                "A_i_max": [1, 1, 1],
            },
            "fixed_F_matrix_shape": [12, 9],
            "moving_monic_F_matrix_shape": [12, 12],
            "universal_fixed_rank": 9,
            "left_kernel_dimension": 3,
            "crt_compatibility_equations": (
                "coefficients X^3,X^4,X^5 of (F*G mod B) vanish, "
                "where B=B1*B2*B3 and G=c_i*R^(-1) mod B_i"
            ),
            "reduced_lower_map_shape": [3, 3],
            "monic_affine_column": "the X^3 column of the full 3x4 map",
            "rank_relation": "rank(C_12x12)=9+rank(reduced_3x3)",
        },
        "owner_certificate": {
            "path": str(OWNER_CERTIFICATE_PATH.relative_to(ROOT)),
            "sha256": hashlib.sha256(OWNER_CERTIFICATE_PATH.read_bytes()).hexdigest(),
        },
        "result": {
            "support_pattern_count": len(transcript),
            "fixed_matrix_rank_histogram": dict(sorted(fixed_matrix_rank_histogram.items())),
            "fixed_F_rank_histogram": dict(sorted(fixed_rank_histogram.items())),
            "moving_rank_histogram": dict(sorted(moving_rank_histogram.items())),
            "rankdrop_status_histogram": dict(sorted(rankdrop_status_histogram.items())),
            "support_status_histogram": dict(sorted(support_status_histogram.items())),
            "compatible_support_patterns": compatible_support_patterns,
            "ambient_monic_cubic_solution_total": ambient_solution_total,
            "valid_core_locator_solution_occurrences": valid_core_locator_solutions,
            "exact_target_solution_occurrences": exact_target_solution_occurrences,
            "exact_target_codeword_count": len(exact_target_words),
            "exact_target_periodicity_histogram": dict(
                sorted(
                    Counter(
                        str(record["agreement_stabilizer_order"])
                        for record in exact_target_words.values()
                    ).items()
                )
            ),
            "independent_decoder_list_size": len(decoded),
            "independent_decoder_extra_count": len(decoded_words - planted),
            "independent_decoder_target_count": len(decoded_targets),
            "transcript_sha256": sha256_json(transcript),
        },
        "exceptional_patterns": exceptional_patterns,
        "compatible_rankdrop_templates": compatible_rankdrop_templates,
        "exact_target_words": list(exact_target_words.values()),
        "independent_decoder_targets": decoded_targets,
        "proof_status": {
            "exact_finite": [
                "all 432 support patterns and four actual missed-core locators are checked",
                "all ranks and affine fibres are exact over GF(19)",
                "every valid locator solution is rechecked on the full domain",
                "the support-subset decoder independently checks the realized target set",
            ],
            "unproved": [
                "a uniform bound for arbitrary received sunflowers",
                "a symbolic rank-drop dichotomy",
                "classification or payment of the two compatible ambient cubic-line templates",
                "any ledger improvement from this finite census alone",
            ],
        },
        "nonclaims": [
            "an exact finite census is not a uniform theorem",
            "ambient monic cubics need not be split missed-core locators",
            "no m>2 or PR #763 statement is made",
        ],
        "verdict": "YELLOW - exact finite rank census only; symbolic classification remains required.",
    }


def validate_report(report):
    result = report["result"]
    fixed_total = sum(int(value) for value in result["fixed_F_rank_histogram"].values())
    moving_total = sum(int(value) for value in result["moving_rank_histogram"].values())
    status_total = sum(int(value) for value in result["support_status_histogram"].values())
    rankdrop_total = sum(int(value) for value in result["rankdrop_status_histogram"].values())
    target_words = report["exact_target_words"]
    decoder_targets = report["independent_decoder_targets"]
    return (
        report["schema"] == "rs-mca-l1-b9-frontier-31222-census-v1"
        and report["frozen_system"]["fixed_F_matrix_shape"] == [12, 9]
        and report["frozen_system"]["moving_monic_F_matrix_shape"] == [12, 12]
        and int(result["support_pattern_count"]) == 432
        and fixed_total == 4 * 432
        and moving_total == 432
        and status_total == 432
        and rankdrop_total == 432
        and int(result["rankdrop_status_histogram"].get("UNPAID_RANKDROP_TEMPLATE", 0)) == 2
        and len(report["compatible_rankdrop_templates"]) == 2
        and all(
            row["owner"] == "UNPAID_RANKDROP_TEMPLATE"
            for row in report["compatible_rankdrop_templates"]
        )
        and all(
            not row["affine_monic_cubic_line"]["actual_missed_core_intersections"]
            for row in report["compatible_rankdrop_templates"]
        )
        and int(result["exact_target_codeword_count"]) == len(target_words)
        and int(result["independent_decoder_target_count"]) == len(decoder_targets)
        and {
            int(row["agreement_mask"]) for row in target_words
        } == {
            int(row["agreement_mask"]) for row in decoder_targets
        }
        and report["owner_certificate"]["sha256"]
        == hashlib.sha256(OWNER_CERTIFICATE_PATH.read_bytes()).hexdigest()
    )


def tamper_selftest(report):
    mutations = []
    changed = copy.deepcopy(report)
    changed["frozen_system"]["moving_monic_F_matrix_shape"] = [12, 13]
    mutations.append(("matrix_shape", changed))
    changed = copy.deepcopy(report)
    first_key = next(iter(changed["result"]["moving_rank_histogram"]))
    changed["result"]["moving_rank_histogram"][first_key] += 1
    mutations.append(("moving_rank_histogram", changed))
    changed = copy.deepcopy(report)
    changed["result"]["exact_target_codeword_count"] += 1
    mutations.append(("target_count", changed))
    changed = copy.deepcopy(report)
    changed["compatible_rankdrop_templates"][0]["owner"] = "PAID_B11_G2"
    mutations.append(("rankdrop_owner", changed))
    changed = copy.deepcopy(report)
    changed["owner_certificate"]["sha256"] = "0" * 64
    mutations.append(("owner_link", changed))
    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<24}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))
    report = build_report()
    if not validate_report(report):
        print("RESULT: FAIL (internal census validation)", file=sys.stderr)
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
        print("RESULT: FAIL (frozen census certificate drift)", file=sys.stderr)
        return 1
    result = report["result"]
    print("L1 B9 frontier (3,1,3,(2,2,2)) exact GF(19) census")
    print(f"  fixed system: {report['frozen_system']['fixed_F_matrix_shape']}")
    print(f"  moving system: {report['frozen_system']['moving_monic_F_matrix_shape']}")
    print(f"  support patterns: {result['support_pattern_count']}")
    print(f"  moving ranks: {result['moving_rank_histogram']}")
    print(f"  support statuses: {result['support_status_histogram']}")
    print(
        "  exact targets: "
        f"rank={result['exact_target_codeword_count']}, "
        f"decoder={result['independent_decoder_target_count']}"
    )
    print(f"  transcript: {result['transcript_sha256']}")
    print(f"  proof status: {report['status']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(int(main(sys.argv[1:])))
