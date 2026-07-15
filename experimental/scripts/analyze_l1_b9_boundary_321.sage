#!/usr/bin/env sage
"""Exact GF(19) rank census for the B9 ``(3,2,1)`` boundary profile.

The frozen row is the sequential sunflower

    (p,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2).

For every labelled support pattern with hit multiset ``(3,2,1)``, retained
background equal to both background points, and missed core equal to the
four-point core, solve the exact coefficient system

    R V - c_i F = L_{S_i} A_i,

where ``deg(V)<=2`` and ``deg(A_i)<=4-|S_i|``.  The system has 15 coefficient
equations and 12 unknowns.  Compatible solutions are re-evaluated on the full
domain so extra agreements cannot masquerade as exact frontier witnesses.

This is an exact finite falsification packet, not an asymptotic theorem.
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
    / "experimental/data/certificates/l1-b9-boundary-321/certificate.json"
)


def sha256_json(value):
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=int
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


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


def coefficient_system(PX, X, field, F, R, support_locators, labels, sizes):
    columns = [R * X**degree for degree in range(3)]
    offsets = []
    for support_locator, size in zip(support_locators, sizes, strict=True):
        offsets.append(len(columns))
        columns.extend(
            -support_locator * X**degree for degree in range(5 - size)
        )
    if len(columns) != 12:
        raise RuntimeError(f"expected 12 columns, found {len(columns)}")

    rows = []
    rhs = []
    for block, label in enumerate(labels):
        active = [PX.zero()] * len(columns)
        for degree in range(3):
            active[degree] = columns[degree]
        offset = offsets[block]
        for degree in range(5 - sizes[block]):
            active[offset + degree] = columns[offset + degree]
        target = field(label) * F
        for degree in range(5):
            rows.append([poly[degree] for poly in active])
            rhs.append(target[degree])
    return matrix(field, rows), vector(field, rhs)


def compatible_solutions(A, rhs, field, max_solutions=100_000):
    rank_A = A.rank()
    augmented = A.augment(rhs.column())
    rank_augmented = augmented.rank()
    if rank_A != rank_augmented:
        return rank_A, rank_augmented, []
    kernel_basis = A.right_kernel().basis()
    solution_count = int(field.order()) ** len(kernel_basis)
    if solution_count > max_solutions:
        raise RuntimeError(
            f"compatible affine fibre too large to enumerate: {solution_count}"
        )
    particular = A.solve_right(rhs)
    solutions = []
    for coefficients in itertools.product(
        range(int(field.order())), repeat=len(kernel_basis)
    ):
        solution = vector(field, particular)
        for coefficient, basis_vector in zip(
            coefficients, kernel_basis, strict=True
        ):
            solution += field(coefficient) * basis_vector
        solutions.append(solution)
    return rank_A, rank_augmented, solutions


def moving_monic_F_system(A, labels, field):
    """Adjoin the four lower coefficients of monic quartic F.

    The fixed-F equations are ``A*z=c_i*F``.  Writing
    ``F=X^4+sum_{j=0}^3 f_j X^j`` gives a 15-by-16 affine system.
    """
    rows = []
    rhs = []
    for block, label in enumerate(labels):
        for degree in range(5):
            row = list(A.row(5 * block + degree))
            row.extend(
                -field(label) if degree == lower_degree else field.zero()
                for lower_degree in range(4)
            )
            rows.append(row)
            rhs.append(field(label) if degree == 4 else field.zero())
    C = matrix(field, rows)
    monic_rhs = vector(field, rhs)
    return C, monic_rhs


def build_report():
    p, n, k, sigma = 19, 18, 5, 3
    ell = sigma + 1
    field = GF(p)
    PX = PolynomialRing(field, "X")
    X = PX.gen()
    domain = subgroup(p, n)
    core = tuple(range(4))
    petals = (tuple(range(4, 8)), tuple(range(8, 12)), tuple(range(12, 16)))
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
    F = locator(PX, X, field, domain, core)
    R = locator(PX, X, field, domain, background)

    rank_histogram = Counter()
    moving_F_rank_histogram = Counter()
    stabilizer_histogram = Counter()
    compatible_patterns = 0
    compatible_affine_solutions = 0
    moving_F_ambient_solution_total = 0
    moving_F_exceptional_patterns = []
    exact_target_words = {}
    transcript = []

    for sizes in itertools.permutations((3, 2, 1)):
        support_choices = [
            tuple(itertools.combinations(petal, size))
            for petal, size in zip(petals, sizes, strict=True)
        ]
        for supports in itertools.product(*support_choices):
            support_locators = [
                locator(PX, X, field, domain, support) for support in supports
            ]
            A, rhs = coefficient_system(
                PX, X, field, F, R, support_locators, labels, sizes
            )
            rank_A, rank_augmented, solutions = compatible_solutions(A, rhs, field)
            rank_histogram[f"rankA={rank_A},rankAug={rank_augmented}"] += 1
            C, monic_rhs = moving_monic_F_system(A, labels, field)
            rank_C = C.rank()
            rank_C_augmented = C.augment(monic_rhs.column()).rank()
            moving_F_rank_histogram[
                f"rankC={rank_C},rankAug={rank_C_augmented}"
            ] += 1
            moving_solution_count = (
                p ** (16 - rank_C)
                if rank_C == rank_C_augmented
                else 0
            )
            moving_F_ambient_solution_total += moving_solution_count
            intended = list(background) + [point for support in supports for point in support]
            intended_mask = sum(1 << index for index in intended)
            support_stabilizer = stabilizer_order(intended_mask, n)
            stabilizer_histogram[str(support_stabilizer)] += 1
            if rank_C < 15 or rank_C != rank_C_augmented:
                moving_F_exceptional_patterns.append(
                    {
                        "sizes_by_labelled_petal": list(sizes),
                        "supports": [list(support) for support in supports],
                        "support_stabilizer_order": support_stabilizer,
                        "rank_C": int(rank_C),
                        "rank_C_augmented": int(rank_C_augmented),
                        "ambient_solution_count": int(moving_solution_count),
                    }
                )
            compatible_patterns += bool(solutions)
            compatible_affine_solutions += len(solutions)
            exact_in_pattern = 0
            for solution in solutions:
                V = sum(solution[degree] * X**degree for degree in range(3))
                W = R * V
                mask = agreement_mask(W, values, domain, field)
                exact_profile = profile(mask, core, petals, background)
                if (
                    exact_profile["d"] == 4
                    and exact_profile["r"] == 2
                    and exact_profile["a_i"] == [3, 2, 1]
                ):
                    evaluations = tuple(
                        int(W(field(point))) for point in domain
                    )
                    exact_target_words[evaluations] = {
                        "agreement_mask": int(mask),
                        "agreement_set": [
                            index for index in range(n) if mask & (1 << index)
                        ],
                        "stabilizer_order": stabilizer_order(mask, n),
                    }
                    exact_in_pattern += 1
            transcript.append(
                {
                    "sizes_by_labelled_petal": list(sizes),
                    "supports": [list(support) for support in supports],
                    "support_stabilizer_order": support_stabilizer,
                    "rank_A": int(rank_A),
                    "rank_augmented": int(rank_augmented),
                    "moving_F_rank": int(rank_C),
                    "moving_F_augmented_rank": int(rank_C_augmented),
                    "moving_F_ambient_solution_count": int(moving_solution_count),
                    "affine_solution_count": len(solutions),
                    "exact_target_solution_count": exact_in_pattern,
                }
            )

    if len(transcript) != 576:
        raise RuntimeError(f"support-pattern count drift: {len(transcript)}")

    decoded = img_list(values, domain, k, k + sigma, p, "support")
    planted = {
        tuple(
            int((field(label) * F)(field(point))) for point in domain
        )
        for label in labels
    }
    decoded_words = set(decoded)
    if not planted.issubset(decoded_words):
        raise RuntimeError("planted words missing from exact decoder")
    decoded_targets = []
    for codeword, mask in decoded.items():
        row = profile(mask, core, petals, background)
        if row["d"] == 4 and row["r"] == 2 and row["a_i"] == [3, 2, 1]:
            decoded_targets.append(
                {
                    "codeword": list(map(int, codeword)),
                    "agreement_mask": int(mask),
                    "stabilizer_order": stabilizer_order(mask, n),
                }
            )
    if len(decoded) != 4 or len(decoded_words - planted) != 1:
        raise RuntimeError("exact decoder control drift")
    if len(decoded_targets) != len(exact_target_words):
        raise RuntimeError("rank census and independent decoder disagree")

    primitive_patterns = int(stabilizer_histogram["1"])
    periodic_patterns = len(transcript) - primitive_patterns
    return {
        "schema": "rs-mca-l1-b9-boundary-321-v1",
        "status": "EXPERIMENTAL/EXACT_FINITE_GF19_RANK_CENSUS",
        "statement": (
            "classify all fixed supports for (d,r,t,a_i)=(4,2,3,(3,2,1)) "
            "in the sequential GF(19) sunflower"
        ),
        "input": {
            "p": p,
            "n": n,
            "k": k,
            "sigma": sigma,
            "ell": ell,
            "core": list(core),
            "petals": [list(petal) for petal in petals],
            "background": list(background),
            "labels": list(labels),
            "domain": list(map(int, domain)),
        },
        "object": {
            "equations": "R*V-c_i*F=L_{S_i}*A_i",
            "degree_bounds": {
                "V": 2,
                "A_i_for_support_sizes_3_2_1": [1, 2, 3],
            },
            "matrix_shape": [15, 12],
            "moving_monic_F_matrix_shape": [15, 16],
            "support_profile": [3, 2, 1],
            "support_pattern_formula": "3!*binom(4,3)*binom(4,2)*binom(4,1)=576",
        },
        "result": {
            "support_patterns": len(transcript),
            "support_stabilizer_histogram": dict(sorted(stabilizer_histogram.items())),
            "periodic_support_patterns": periodic_patterns,
            "primitive_support_patterns": primitive_patterns,
            "rank_histogram": dict(sorted(rank_histogram.items())),
            "moving_monic_F_rank_histogram": dict(
                sorted(moving_F_rank_histogram.items())
            ),
            "moving_monic_F_ambient_solution_total": int(
                moving_F_ambient_solution_total
            ),
            "moving_monic_F_exceptional_patterns": moving_F_exceptional_patterns,
            "compatible_support_patterns": compatible_patterns,
            "compatible_affine_solutions": compatible_affine_solutions,
            "exact_target_codewords_from_rank_census": len(exact_target_words),
            "exact_target_codewords_from_independent_decoder": len(decoded_targets),
            "decoded_list_size": len(decoded),
            "decoded_extra_count": len(decoded_words - planted),
            "transcript_sha256": sha256_json(transcript),
        },
        "exact_target_words": list(exact_target_words.values()),
        "proof_certificate": {
            "field_arithmetic": "Sage GF(19)",
            "support_enumeration": "exhaustive labelled patterns",
            "full_domain_recheck": True,
            "independent_exact_support_subset_decoder": True,
        },
        "theorem_problem_id": "L1 B9 residual frontier; local profile (4,2,3,(3,2,1))",
        "proof_status": {
            "exact": [
                "all 576 support patterns are enumerated",
                "all coefficient and augmented ranks are over GF(19)",
                "all moving-monic-F ranks and ambient fibre sizes are exact over GF(19)",
                "every compatible affine solution is rechecked on the full domain",
                "the exact decoder independently checks realized target codewords",
            ],
            "unproved": [
                "non-realization for other domains or fields",
                "an asymptotic rank dichotomy",
                "closure of the remaining mixed-petal ledger",
            ],
        },
        "nonclaims": [
            "an empty finite fixture is not an asymptotic theorem",
            "cyclic stabilizer one does not exclude every quotient descent",
            "no m>2 profile is analyzed",
        ],
        "verdict": "YELLOW - exact finite control only; do not authorize global proof.",
    }


def validate_report(report):
    result = report["result"]
    histogram_total = sum(int(value) for value in result["rank_histogram"].values())
    stabilizer_total = sum(
        int(value) for value in result["support_stabilizer_histogram"].values()
    )
    moving_rank_total = sum(
        int(value) for value in result["moving_monic_F_rank_histogram"].values()
    )
    return (
        report["schema"] == "rs-mca-l1-b9-boundary-321-v1"
        and int(result["support_patterns"]) == 576
        and histogram_total == 576
        and stabilizer_total == 576
        and moving_rank_total == 576
        and int(result["periodic_support_patterns"])
        + int(result["primitive_support_patterns"])
        == 576
        and int(result["exact_target_codewords_from_rank_census"])
        == int(result["exact_target_codewords_from_independent_decoder"])
    )


def tamper_selftest(report):
    mutations = []
    changed = copy.deepcopy(report)
    changed["result"]["support_patterns"] += 1
    mutations.append(("support_patterns", changed))
    changed = copy.deepcopy(report)
    changed["result"]["support_stabilizer_histogram"]["1"] += 1
    mutations.append(("stabilizer_histogram", changed))
    changed = copy.deepcopy(report)
    changed["result"]["exact_target_codewords_from_rank_census"] += 1
    mutations.append(("decoder_crosscheck", changed))
    changed = copy.deepcopy(report)
    first_key = next(iter(changed["result"]["moving_monic_F_rank_histogram"]))
    changed["result"]["moving_monic_F_rank_histogram"][first_key] += 1
    mutations.append(("moving_F_rank_histogram", changed))
    failed = False
    for name, changed in mutations:
        caught = not validate_report(changed)
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
        print("RESULT: FAIL (internal report validation)", file=sys.stderr)
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
        print("RESULT: FAIL (frozen boundary-321 certificate drift)", file=sys.stderr)
        return 1
    result = report["result"]
    print("l1 B9 boundary (3,2,1) exact GF(19) census")
    print(f"  input: p=19,n=18,k=5,sigma=3; matrix=15x12")
    print(f"  object: {report['object']['equations']}")
    print(f"  support patterns: {result['support_patterns']}")
    print(f"  support stabilizers: {result['support_stabilizer_histogram']}")
    print(f"  rank histogram: {result['rank_histogram']}")
    print(f"  moving-F ranks: {result['moving_monic_F_rank_histogram']}")
    print(
        "  moving-F ambient solutions: "
        f"{result['moving_monic_F_ambient_solution_total']}"
    )
    print(f"  compatible patterns: {result['compatible_support_patterns']}")
    print(
        "  exact target codewords: "
        f"rank={result['exact_target_codewords_from_rank_census']}, "
        f"decoder={result['exact_target_codewords_from_independent_decoder']}"
    )
    print(f"  certificate: {result['transcript_sha256']}")
    print(f"  theorem/problem: {report['theorem_problem_id']}")
    print(f"  proof status: {report['status']}")
    print(f"  verdict: {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(int(main(sys.argv[1:])))
