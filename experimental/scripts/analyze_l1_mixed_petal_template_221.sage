#!/usr/bin/env sage
"""Exact Sage census for one compressed mixed-petal (2,2,1) template.

The row is the sequential sunflower at (p,n,k,s)=(17,16,8,10).  This is a
pipeline and falsification fixture only: its B11 coordinates are bounded and
it cannot certify asymptotic mixed-petal amplification.

The script directly enumerates all three labelled assignments of the sorted
profile ``(2,2,1)``, hence

    3 * binom(7,2) * binom(3,2)^2 * binom(3,1) = 1701

support tuples, solves the 9-by-7 incidence system over GF(17), checks exact
agreement support, and independently compares with the repository's exact
support-subset list decoder.
"""

from __future__ import annotations

import argparse
import builtins
import hashlib
import itertools
import json
import sys
from pathlib import Path

from sage.rings.integer import Integer as SageInteger


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experimental/scripts"))

from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    img_list,
    mask_from_indices,
    stabilizer_order,
    subgroup,
    sunflower_word_from_blocks,
)


CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-mixed-petal-template-221/certificate.json"
)


def locator(R, X, field, domain, indices):
    out = R.one()
    for index in indices:
        out *= X - field(domain[index])
    return out


def coefficients(poly, length):
    return [poly[index] for index in range(length)]


def canonical_poly(poly):
    if poly == 0:
        return []
    return [int(poly[index]) for index in range(poly.degree() + 1)]


def json_ready(value):
    """Recursively convert Sage integer scalars to JSON-native integers."""
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, SageInteger):
        return int(value)
    return value


def solve_incidence(R, X, field, F, B1, B2, B3):
    zero = R.zero()
    one = R.one()
    locators = (B1, B2, B3)
    cofactor_degrees = tuple(2 - B.degree() for B in locators)
    if any(degree < 0 for degree in cofactor_degrees):
        raise ValueError("support locator degree exceeds the core defect")
    offsets = []
    next_column = 3
    for degree in cofactor_degrees:
        offsets.append(next_column)
        next_column += degree + 1
    if next_column != 7:
        raise ValueError("the (2,2,1) profile should have seven unknowns")
    blocks = []
    for scalar, B, degree, offset in zip(
        (1, 2, 3), locators, cofactor_degrees, offsets, strict=True
    ):
        columns = [one, X, X**2] + [zero] * 4
        for shift in range(degree + 1):
            columns[offset + shift] = -(X**shift) * B
        blocks.append((columns, scalar * F))
    rows = []
    rhs = []
    for columns, target in blocks:
        for degree in range(3):
            rows.append([column[degree] for column in columns])
            rhs.append(target[degree])
    matrix_A = matrix(field, rows)
    vector_b = vector(field, rhs)
    augmented = matrix_A.augment(vector_b.column())
    rank = matrix_A.rank()
    augmented_rank = augmented.rank()
    if rank != augmented_rank:
        return rank, augmented_rank, "INCONSISTENT", None
    if rank != matrix_A.ncols():
        return rank, augmented_rank, "POSITIVE_DIMENSIONAL", None
    solution = matrix_A.solve_right(vector_b)
    w0, w1, w2 = solution[:3]
    W = w0 + w1 * X + w2 * X**2
    cofactors = []
    for degree, offset in zip(cofactor_degrees, offsets, strict=True):
        cofactors.append(
            sum(solution[offset + shift] * X**shift for shift in range(degree + 1))
        )
    for scalar, B, A in zip((1, 2, 3), locators, cofactors, strict=True):
        assert W - scalar * F == B * A
    return rank, augmented_rank, "UNIQUE", (W, tuple(cofactors))


def has_exact_support(W, F, field, domain, D, petals, supports, scalars):
    if not all(W(field(domain[index])) != 0 for index in D):
        return False
    for scalar, petal, support in zip(scalars, petals, supports, strict=True):
        difference = W - scalar * F
        for index in petal:
            if (difference(field(domain[index])) == 0) != (index in support):
                return False
    return True


def solver_controls(R, X, field):
    """Exercise unique, positive-dimensional, and non-exact branches."""
    control_domain = [1, 2, 5, 7, 8, 9, 10, 16, 4, 11, 14, 6, 12, 0, 13, 15]
    D = (0, 1)
    F = locator(R, X, field, control_domain, D)
    petals = ((7, 8, 9), (10, 11, 12), (13, 14, 15))
    supports = ((7, 8), (10, 11), (13,))
    B1 = locator(R, X, field, control_domain, supports[0])
    B2 = locator(R, X, field, control_domain, supports[1])
    B3 = locator(R, X, field, control_domain, supports[2])
    rank, augmented_rank, status, solution = solve_incidence(
        R, X, field, F, B1, B2, B3
    )
    if status != "UNIQUE" or solution is None:
        raise RuntimeError("positive-control incidence system is not unique")
    W, _ = solution
    if W != field(6):
        raise RuntimeError("positive-control reconstruction drift")
    if not has_exact_support(
        W, F, field, control_domain, D, petals, supports, (1, 2, 3)
    ):
        raise RuntimeError("positive control failed exact-support check")

    nonexact_domain = list(control_domain)
    nonexact_domain[14] = 3
    if has_exact_support(
        W, F, field, nonexact_domain, D, petals, supports, (1, 2, 3)
    ):
        raise RuntimeError("hidden extra agreement was not rejected")

    zero = R.zero()
    quadratic = X**2
    linear = X
    rank0, augmented_rank0, status0, solution0 = solve_incidence(
        R, X, field, zero, quadratic, quadratic, linear
    )
    if status0 != "POSITIVE_DIMENSIONAL" or solution0 is not None:
        raise RuntimeError("positive-dimensional solver branch was not exposed")
    return {
        "unique_exact_support_control": True,
        "consistent_nonexact_control_rejected": True,
        "positive_dimensional_control_exposed": True,
        "positive_control_rank": rank,
        "positive_control_augmented_rank": augmented_rank,
        "positive_dimensional_control_rank": rank0,
        "positive_dimensional_control_augmented_rank": augmented_rank0,
    }


def build_report():
    p, n, k, s = 17, 16, 8, 10
    field = GF(p)
    R = PolynomialRing(field, "X")
    X = R.gen()
    domain = subgroup(p, n)
    core = tuple(range(7))
    petals = (
        tuple(range(7, 10)),
        tuple(range(10, 13)),
        tuple(range(13, 16)),
    )
    scalars = (1, 2, 3)
    word = sunflower_word_from_blocks(
        p,
        n,
        k,
        s,
        list(core),
        [list(petal) for petal in petals],
        "sunflower-sequential-m3",
    )
    if word is None:
        raise RuntimeError("failed to build the sequential sunflower")
    values = word["values"]
    L_C = locator(R, X, field, domain, core)
    expected_values = [0] * n
    for scalar, petal in zip(scalars, petals, strict=True):
        for index in petal:
            expected_values[index] = int(scalar * L_C(field(domain[index])))
    if values != expected_values:
        raise RuntimeError("imported sunflower constructor does not match its equations")
    controls = solver_controls(R, X, field)

    raw_support_tuples = 0
    coefficient_rank_histogram = {}
    status_histogram = {}
    consistent_count = 0
    positive_dimensional_count = 0
    exact_support_count = 0
    primitive_exact_count = 0
    canonical = []
    rank_transcript = []
    consistent_not_exact = []
    size_assignments = sorted(set(itertools.permutations((2, 2, 1))))

    for D in itertools.combinations(core, 2):
        F = locator(R, X, field, domain, D)
        core_quotient, core_remainder = L_C.quo_rem(F)
        assert core_remainder == 0
        for sizes in size_assignments:
            support_iterators = [
                itertools.combinations(petal, size)
                for petal, size in zip(petals, sizes, strict=True)
            ]
            for supports in itertools.product(*support_iterators):
                raw_support_tuples += 1
                B1, B2, B3 = [
                    locator(R, X, field, domain, support) for support in supports
                ]
                rank, augmented_rank, status, solution = solve_incidence(
                    R, X, field, F, B1, B2, B3
                )
                key = f"rank={rank},augmented_rank={augmented_rank}"
                coefficient_rank_histogram[key] = (
                    coefficient_rank_histogram.get(key, 0) + 1
                )
                status_histogram[status] = status_histogram.get(status, 0) + 1
                rank_transcript.append(
                    {
                        "D": list(D),
                        "supports": [list(support) for support in supports],
                        "rank": rank,
                        "augmented_rank": augmented_rank,
                        "status": status,
                    }
                )
                if status == "POSITIVE_DIMENSIONAL":
                    positive_dimensional_count += 1
                    continue
                if status == "INCONSISTENT":
                    continue
                if status != "UNIQUE" or solution is None:
                    raise RuntimeError(f"unhandled incidence status: {status}")
                consistent_count += 1
                W, cofactors = solution
                P = core_quotient * W
                if P.degree() >= k:
                    raise RuntimeError("reconstructed polynomial exceeds degree bound")

                chosen = tuple(set(support) for support in supports)
                exact_support = has_exact_support(
                    W, F, field, domain, D, petals, chosen, scalars
                )
                if not exact_support:
                    if len(consistent_not_exact) < 12:
                        consistent_not_exact.append(
                            {
                                "D": list(D),
                                "supports": [list(support) for support in supports],
                                "W": canonical_poly(W),
                            }
                        )
                    continue

                exact_support_count += 1
                codeword = tuple(int(P(field(value))) for value in domain)
                agreement = [
                    index
                    for index, (left, right) in enumerate(
                        zip(codeword, values, strict=True)
                    )
                    if left == right
                ]
                expected = sorted(
                    (set(core) - set(D)).union(*(set(support) for support in supports))
                )
                if agreement != expected:
                    raise RuntimeError("exact-support reconstruction drift")
                mask = mask_from_indices(agreement)
                stabilizer = stabilizer_order(mask, n)
                if stabilizer == 1:
                    primitive_exact_count += 1
                canonical.append(
                    {
                        "D": list(D),
                        "supports": [list(support) for support in supports],
                        "a_i_labelled": list(sizes),
                        "F": canonical_poly(F),
                        "B": [canonical_poly(B1), canonical_poly(B2), canonical_poly(B3)],
                        "W": canonical_poly(W),
                        "cofactors": [canonical_poly(A) for A in cofactors],
                        "P": canonical_poly(P),
                        "agreement_mask": mask,
                        "stabilizer_order": stabilizer,
                    }
                )

    if raw_support_tuples != 1701:
        raise RuntimeError(f"raw support count drift: {raw_support_tuples}")
    if positive_dimensional_count:
        raise RuntimeError(
            "target census contains positive-dimensional fibres; "
            "explicit affine-kernel enumeration is required"
        )
    canonical.sort(
        key=lambda row: (row["D"], row["supports"], row["P"])
    )
    canonical_payload = json.dumps(
        json_ready(canonical), sort_keys=True, separators=(",", ":")
    )
    canonical_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
    rank_transcript.sort(key=lambda row: (row["D"], row["supports"]))
    rank_transcript_hash = hashlib.sha256(
        json.dumps(
            json_ready(rank_transcript), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()

    decoded = img_list(values, domain, k, s, p, "support")
    decoded_target = []
    core_set = set(core)
    petal_sets = [set(petal) for petal in petals]
    for codeword, mask in decoded.items():
        agreement = {index for index in range(n) if mask & (1 << index)}
        d = len(core_set - agreement)
        hits = sorted(
            [len(agreement & petal) for petal in petal_sets if agreement & petal],
            reverse=True,
        )
        if d == 2 and hits == [2, 2, 1]:
            decoded_target.append(
                {
                    "codeword": [int(value) for value in codeword],
                    "agreement_mask": mask,
                    "stabilizer_order": stabilizer_order(mask, n),
                }
            )
    decoded_target.sort(key=lambda row: (row["agreement_mask"], row["codeword"]))
    decoded_hash = hashlib.sha256(
        json.dumps(
            json_ready(decoded_target), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()

    enumerated_masks = sorted(row["agreement_mask"] for row in canonical)
    decoded_masks = sorted(row["agreement_mask"] for row in decoded_target)
    if len(set(enumerated_masks)) != len(enumerated_masks):
        raise RuntimeError("distinct support fibres reconstructed a duplicate codeword")
    if enumerated_masks != decoded_masks:
        raise RuntimeError(
            "direct incidence enumeration and exact list decoder disagree on masks"
        )

    sigma = s - k
    d = 2
    r = 0
    auxiliary_agreement = sigma + d + 1 - r
    auxiliary_domain_size = len(petals) * (sigma + 1)
    auxiliary_margin = (
        auxiliary_agreement**2 - auxiliary_domain_size * d
    )
    if auxiliary_margin <= 0:
        raise RuntimeError("target fixture unexpectedly left auxiliary Johnson")
    auxiliary_numerator = auxiliary_domain_size * (auxiliary_agreement - d)
    auxiliary_integer_bound = auxiliary_numerator // auxiliary_margin

    return json_ready({
        "schema": "rs-mca-l1-mixed-petal-template-221-v2",
        "status": "EXPERIMENTAL/PIPELINE_CHECK",
        "row": {"p": p, "n": n, "k": k, "s": s, "sigma": 2, "ell": 3},
        "layout": {
            "domain": domain,
            "core": list(core),
            "petals": [list(petal) for petal in petals],
            "scalars": list(scalars),
        },
        "profile": {
            "d": 2,
            "r": 0,
            "t": 3,
            "a_i": [2, 2, 1],
            "d_minus_ell": -1,
            "G2": 2,
            "GR": 4,
            "lambda": 0,
            "lambda_J": 1,
            "lambda_minus_lambda_J": -1,
        },
        "census": {
            "raw_support_tuples": raw_support_tuples,
            "coefficient_rank_histogram": dict(sorted(coefficient_rank_histogram.items())),
            "incidence_status_histogram": dict(sorted(status_histogram.items())),
            "rank_deficient_consistent_tuples": positive_dimensional_count,
            "consistent_incidence_tuples": consistent_count,
            "exact_support_solutions": exact_support_count,
            "primitive_exact_support_solutions": primitive_exact_count,
            "direct_solution_sha256": canonical_hash,
            "rank_transcript_sha256": rank_transcript_hash,
            "decoder_target_count": len(decoded_target),
            "decoder_target_sha256": decoded_hash,
            "agreement_masks_match_decoder": True,
            "sunflower_word_equations_reconstructed_independently": True,
        },
        "owner_routing": {
            "rank_deficient_components": positive_dimensional_count,
            "full_rank_unique_solutions": exact_support_count,
            "global_B10_johnson_paid_solutions": 0,
            "auxiliary_johnson": {
                "required_agreement": auxiliary_agreement,
                "petal_domain_size": auxiliary_domain_size,
                "degree_bound": d,
                "margin": auxiliary_margin,
                "sharp_numerator": auxiliary_numerator,
                "integer_floor_bound_per_fixed_D_R0": auxiliary_integer_bound,
                "paid_solutions": exact_support_count,
            },
            "cyclic_support_stabilizer_paid_solutions": (
                exact_support_count - primitive_exact_count
            ),
            "paid_G2_at_V2_0": 0,
            "paid_GR_at_VR_0": 0,
            "B11_bounded_excess_box_solutions": exact_support_count,
            "unpaid_after_known_owners": 0,
            "conclusion": "PAID_FIXED_D_R0_AUXILIARY_JOHNSON",
        },
        "solution_records": canonical,
        "solver_controls": controls,
        "consistent_not_exact_examples": consistent_not_exact,
        "nonclaims": [
            "fixed p=17,n=16,k=8,s=10 word, layout, and (2,2,1) profile only",
            "does not prove a B11 asymptotic frontier bound",
            "does not exclude rank-deficient components for other layouts or profiles",
            "does not prove quotient descent, periodicity, or Johnson coverage",
            "cyclic stabilizer one does not exclude every possible quotient descent",
            "does not furnish an unpaid frontier after the auxiliary Johnson owner",
        ],
    })


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args(argv)
    actual = build_report()
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(actual, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if expected != actual:
        print("RESULT: FAIL (frozen template certificate drift)", file=sys.stderr)
        return 1
    census = actual["census"]
    print(
        "[PASS] raw={raw}, rank={rank}, consistent={consistent}, exact={exact}, "
        "decoder={decoder}".format(
            raw=census["raw_support_tuples"],
            rank=census["coefficient_rank_histogram"],
            consistent=census["consistent_incidence_tuples"],
            exact=census["exact_support_solutions"],
            decoder=census["decoder_target_count"],
        )
    )
    print("RESULT: PASS (Sage incidence census matches exact list decoder)")
    return 0


if __name__ == "__main__":
    raise SystemExit(builtins.int(main(sys.argv[1:])))
