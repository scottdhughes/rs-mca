#!/usr/bin/env python3
"""Verify the deployed full-slice odd single-monomial Fourier budget.

This checker is stdlib-only and uses always-active explicit checks.  It
recomputes the large binomial integers, the four strict budget comparisons,
the supporting two-block Plotkin arithmetic, and the quadratic-method route
cut.  It does not verify C9, first-match Fourier survival, weighted circles,
even or multimonomial modes, a global max-fiber bound, or score movement.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from math import comb, factorial, gcd, isqrt
from pathlib import Path
import sys
from typing import Any, Callable


class VerificationError(RuntimeError):
    """Raised when an always-active certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


BASE_COMMIT = "fe93bb59dff3d022f66a097208e17c27e1e0deb4"
CERTIFICATE_ID = "deployed-c9-odd-monomial-fourier-budget-v1"
CERTIFICATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "certificates"
    / "deployed-c9-odd-monomial-fourier-budget"
    / "deployed_c9_odd_monomial_fourier_budget.json"
)

PINNED_PARAMETERS = {
    "p": 2_130_706_433,
    "q": 131_072,
    "w": 67_471,
    "negative_blocks": 8,
    "positive_blocks": 8,
    "t_minus": 60_000,
    "t_plus": 51_566,
}

PINNED_PROVENANCE = {
    "round": "RS_MCA_HOMERUN_9PRO_20260713_R14",
    "role": "08_C9_WEIGHTED_CIRCLE_SIGNED_PAYMENT",
    "worker_return": "ROLE_08_20260713T120834Z_final_response.md",
    "model_effort": "native gpt-5.6-sol ultra hostile integration worker",
    "hostile_audit_scope": (
        "finite full-slice odd single-monomial Fourier budget and "
        "quadratic-method route cut only"
    ),
}

PINNED_CLAIM_SCOPE = {
    "object": "complete fixed-composition 16-block full-slice absolute Fourier ledger",
    "paid_stratum": "odd single-monomial modes",
    "route_cut": (
        "absolute Gauss-period plus uniform cycle-index majorant is "
        "nonpaying at the quadratic mode"
    ),
    "novelty": "exact q=2^17 fixed-composition 16-block instantiation only",
    "supporting_known_machinery": [
        "experimental/notes/thresholds/signed_local_minority_fixed_composition.md",
        "experimental/asymptotic_rs_mca_frontiers.tex#thm:prefix-flatness-power-sum",
        "experimental/notes/roadmaps/b2_conjq_partial_results.md#round-f",
    ],
}

PINNED_PUBLICATION_GATE = {
    "rule": (
        "narrow, source-valid, nonduplicative, theorem-facing, replayable, "
        "and explicit about the remaining wall"
    ),
    "overlap_checked_through_pr": 739,
    "newer_pr_seen": True,
    "decision": "PRZ_CANDIDATE_NARROW_SCOPE_ONLY",
    "refuse_if": [
        "framed as C9 or hard-input-2 payment",
        "framed as a first-match or arbitrary weighted-circle theorem",
        "framed as payment of even or multimonomial modes",
        (
            "framed as a global max-fiber, Q-to-RC, image-scale add-back, "
            "or score improvement"
        ),
    ],
}

PINNED_NONCLAIMS = [
    "no C9 or hard-input-2 payment",
    "no first-match Fourier factorization or survival",
    "no arbitrary weighted circle",
    "no even-mode or multimonomial payment",
    "no global max-fiber bound",
    "no Q-to-RC implication",
    "no image-scale add-back",
    "no official score movement",
    "odd axes are paid only in the complete full-slice absolute Fourier ledger",
]


def load_certificate() -> dict[str, Any]:
    try:
        parsed = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise VerificationError(f"cannot load certificate: {error}") from error
    require(isinstance(parsed, dict), "certificate root must be an object")
    return parsed


def factor_integer(value: int) -> dict[str, int]:
    require(value >= 1, "factorization input must be positive")
    factors: dict[str, int] = {}
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent:
            factors[str(divisor)] = exponent
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors[str(remaining)] = factors.get(str(remaining), 0) + 1
    return factors


def is_prime_trial(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    limit = isqrt(value)
    while divisor <= limit:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def power_of_two_exponent(value: int) -> int:
    require(value > 0, "power-of-two input must be positive")
    require(value & (value - 1) == 0, "value is not a power of two")
    return value.bit_length() - 1


def unsigned_be_sha256(value: int) -> str:
    require(value >= 0, "fingerprint input must be nonnegative")
    length = max(1, (value.bit_length() + 7) // 8)
    return sha256(value.to_bytes(length, "big")).hexdigest()


def fingerprint(value: int) -> dict[str, int | str]:
    return {
        "bit_length": value.bit_length(),
        "sha256_unsigned_be": unsigned_be_sha256(value),
    }


def max_strict_binary_exponent(numerator: int, denominator: int) -> int:
    require(0 < numerator < denominator, "strict exponent requires 0<num<den")
    return ((denominator - 1) // numerator).bit_length() - 1


def verify_max_strict_binary_exponent(
    numerator: int, denominator: int, exponent: int, label: str
) -> None:
    require(exponent >= 0, f"{label}: exponent must be nonnegative")
    require(
        numerator * (1 << exponent) < denominator,
        f"{label}: advertised strict comparison failed",
    )
    require(
        numerator * (1 << (exponent + 1)) >= denominator,
        f"{label}: exponent is not maximal",
    )


def binary_ratio_floor(numerator: int, denominator: int) -> int:
    require(numerator >= denominator > 0, "ratio floor requires num>=den>0")
    exponent = max(0, numerator.bit_length() - denominator.bit_length())
    while denominator * (1 << exponent) > numerator:
        exponent -= 1
    while denominator * (1 << (exponent + 1)) <= numerator:
        exponent += 1
    return exponent


def verify_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    expected_top_keys = {
        "schema_version",
        "certificate_id",
        "status",
        "base_commit",
        "provenance",
        "claim_scope",
        "parameters",
        "expected",
        "publication_gate",
        "nonclaims",
    }
    require(set(certificate) == expected_top_keys, "certificate top-level keys")
    require(certificate["schema_version"] == 1, "schema version")
    require(certificate["certificate_id"] == CERTIFICATE_ID, "certificate id")
    require(
        certificate["status"] == "PROVED_EXACT_FINITE_FULL_SLICE_AUDIT",
        "certificate status",
    )
    require(certificate["base_commit"] == BASE_COMMIT, "base commit")
    require(certificate["provenance"] == PINNED_PROVENANCE, "provenance")
    require(certificate["claim_scope"] == PINNED_CLAIM_SCOPE, "claim scope")
    require(certificate["parameters"] == PINNED_PARAMETERS, "deployed parameters")
    require(
        certificate["publication_gate"] == PINNED_PUBLICATION_GATE,
        "publication gate",
    )
    require(certificate["nonclaims"] == PINNED_NONCLAIMS, "nonclaims")

    p = PINNED_PARAMETERS["p"]
    q = PINNED_PARAMETERS["q"]
    w = PINNED_PARAMETERS["w"]
    negative_blocks = PINNED_PARAMETERS["negative_blocks"]
    positive_blocks = PINNED_PARAMETERS["positive_blocks"]
    t_minus = PINNED_PARAMETERS["t_minus"]
    t_plus = PINNED_PARAMETERS["t_plus"]
    total_blocks = negative_blocks + positive_blocks

    require(total_blocks == 16, "fixed-composition block count")
    require(is_prime_trial(p), "p is not prime")
    require(p > w, "supporting Newton/Plotkin input requires p>w")
    p_minus_1_factorization = factor_integer(p - 1)
    require(p_minus_1_factorization == {"2": 24, "127": 1}, "p-1 factorization")
    require(is_prime_trial(127), "cofactor 127 is not prime")

    q_exponent = power_of_two_exponent(q)
    require((p - 1) % q == 0, "q does not divide p-1")
    period_index = (p - 1) // q
    require(q > w, "complete-coset power-sum range requires q>w")
    require(max(t_minus, t_plus) < p, "cycle multipliers must be nonzero mod p")
    require(0 < t_minus < q and 0 < t_plus < q, "slice sizes")

    odd_degrees = tuple(range(1, w + 1, 2))
    require(
        all(gcd(degree, q) == 1 for degree in odd_degrees),
        "an odd power does not permute H",
    )
    odd_degree_count = len(odd_degrees)
    odd_mode_count = odd_degree_count * (p - 1)

    lambda_value = isqrt(p)
    if lambda_value * lambda_value < p:
        lambda_value += 1
    lambda_lower_margin = p - (lambda_value - 1) ** 2
    lambda_upper_margin = lambda_value**2 - p
    require(lambda_lower_margin > 0, "lambda lower square gate")
    require(lambda_upper_margin > 0, "lambda upper square gate")

    gauss_period_square_margin = (
        (period_index * lambda_value - 1) ** 2
        - (period_index - 1) ** 2 * p
    )
    require(period_index * lambda_value - 1 > 0, "Gauss-period sign gate")
    require(gauss_period_square_margin > 0, "Gauss-period integer bound")

    dense_occupancy = q - t_minus
    positive_complement = q - t_plus
    n = total_blocks * q
    support_size = negative_blocks * dense_occupancy + positive_blocks * t_plus
    minority_total = negative_blocks * t_minus + positive_blocks * t_plus
    delta = w + 1
    delta_q = delta * q
    pair_variance = t_minus * (q - t_minus) + t_plus * (q - t_plus)
    pair_gap = delta_q - pair_variance
    require(pair_gap > 0, "pair Plotkin gap")
    pair_cap = delta_q // pair_gap
    require(pair_cap * pair_gap <= delta_q, "pair-cap lower floor comparison")
    require(delta_q < (pair_cap + 1) * pair_gap, "pair-cap upper floor comparison")

    zero_minus = comb(q, t_minus)
    zero_plus = comb(q, t_plus)
    full_slice = zero_minus**negative_blocks * zero_plus**positive_blocks
    ambient_target = p**w

    cycle_minus = comb(lambda_value + t_minus - 1, t_minus)
    cycle_plus = comb(lambda_value + t_plus - 1, t_plus)
    odd_per_mode = cycle_minus**negative_blocks * cycle_plus**positive_blocks
    odd_budget = odd_mode_count * odd_per_mode

    d2_exponent = max_strict_binary_exponent(odd_budget, ambient_target)
    d3_exponent = max_strict_binary_exponent(odd_budget, full_slice)
    d4_exponent = max_strict_binary_exponent(full_slice, ambient_target)
    labeled_budget = factorial(total_blocks) * (full_slice + odd_budget)
    d5_exponent = max_strict_binary_exponent(labeled_budget, ambient_target)
    verify_max_strict_binary_exponent(odd_budget, ambient_target, d2_exponent, "D2")
    verify_max_strict_binary_exponent(odd_budget, full_slice, d3_exponent, "D3")
    verify_max_strict_binary_exponent(full_slice, ambient_target, d4_exponent, "D4")
    verify_max_strict_binary_exponent(labeled_budget, ambient_target, d5_exponent, "D5")

    quadratic_lambda = 2 * lambda_value
    require(gcd(2, q) == 2, "quadratic power-map kernel on H")
    require(
        (quadratic_lambda - 1) ** 2 < 4 * p < quadratic_lambda**2,
        "quadratic period square gate",
    )
    quadratic_minus = comb(quadratic_lambda + t_minus - 1, t_minus)
    quadratic_plus = comb(quadratic_lambda + t_plus - 1, t_plus)
    require(quadratic_minus > zero_minus, "quadratic minus majorant is nonpaying")
    require(quadratic_plus > zero_plus, "quadratic plus majorant is nonpaying")
    quadratic_minus_floor = binary_ratio_floor(quadratic_minus, zero_minus)
    quadratic_plus_floor = binary_ratio_floor(quadratic_plus, zero_plus)
    require(
        zero_minus * (1 << quadratic_minus_floor) <= quadratic_minus
        < zero_minus * (1 << (quadratic_minus_floor + 1)),
        "quadratic minus ratio floor",
    )
    require(
        zero_plus * (1 << quadratic_plus_floor) <= quadratic_plus
        < zero_plus * (1 << (quadratic_plus_floor + 1)),
        "quadratic plus ratio floor",
    )

    derived_expected = {
        "p_minus_1_factorization": p_minus_1_factorization,
        "q_power_of_two_exponent": q_exponent,
        "coset_index": period_index,
        "n": n,
        "support_size": support_size,
        "minority_total": minority_total,
        "dense_occupancy": dense_occupancy,
        "positive_complement": positive_complement,
        "delta": delta,
        "delta_q": delta_q,
        "pair_variance": pair_variance,
        "pair_gap": pair_gap,
        "pair_cap": pair_cap,
        "odd_degree_count": odd_degree_count,
        "odd_mode_count": odd_mode_count,
        "period_index": period_index,
        "lambda": lambda_value,
        "lambda_lower_margin": lambda_lower_margin,
        "lambda_upper_margin": lambda_upper_margin,
        "gauss_period_square_margin": gauss_period_square_margin,
        "quadratic_lambda": quadratic_lambda,
        "d2_max_strict_exponent": d2_exponent,
        "d3_max_strict_exponent": d3_exponent,
        "d4_max_strict_exponent": d4_exponent,
        "d5_max_strict_exponent": d5_exponent,
        "quadratic_minus_excess_floor_bits": quadratic_minus_floor,
        "quadratic_plus_excess_floor_bits": quadratic_plus_floor,
        "large_integer_fingerprints": {
            "zero_minus": fingerprint(zero_minus),
            "zero_plus": fingerprint(zero_plus),
            "full_slice": fingerprint(full_slice),
            "ambient_target": fingerprint(ambient_target),
            "cycle_minus": fingerprint(cycle_minus),
            "cycle_plus": fingerprint(cycle_plus),
            "odd_per_mode": fingerprint(odd_per_mode),
            "odd_budget": fingerprint(odd_budget),
            "quadratic_minus_majorant": fingerprint(quadratic_minus),
            "quadratic_plus_majorant": fingerprint(quadratic_plus),
        },
    }
    require(certificate["expected"] == derived_expected, "derived arithmetic")

    return {
        "expected": derived_expected,
        "total_blocks": total_blocks,
    }


def print_report(certificate: dict[str, Any], result: dict[str, Any]) -> None:
    expected = result["expected"]
    fingerprints = expected["large_integer_fingerprints"]
    parameters = certificate["parameters"]
    print(f"CERTIFICATE: {certificate['certificate_id']}")
    print(f"BASE_COMMIT: {certificate['base_commit']}")
    print(
        "SCOPE: complete fixed-composition 16-block full slice; "
        "odd single-monomial absolute Fourier ledger only"
    )
    print(
        "PRIME_GATE: "
        f"p={parameters['p']} prime; p-1=2^24*127; "
        f"q=2^{expected['q_power_of_two_exponent']} divides p-1; "
        f"index={expected['period_index']}"
    )
    print(
        "PROFILE: "
        f"n={expected['n']} support={expected['support_size']} "
        f"minority_total={expected['minority_total']} "
        f"blocks={parameters['negative_blocks']}+{parameters['positive_blocks']} "
        f"t_minus={parameters['t_minus']} t_plus={parameters['t_plus']}"
    )
    print(
        "PAIR_CAP_SUPPORT: "
        f"delta*q={expected['delta_q']} B_pair={expected['pair_variance']} "
        f"gap={expected['pair_gap']} cap={expected['pair_cap']}"
    )
    print(
        "ODD_INPUTS: "
        f"odd_degrees={expected['odd_degree_count']} "
        f"modes={expected['odd_mode_count']} lambda={expected['lambda']} "
        f"cycle_bits={fingerprints['cycle_minus']['bit_length']},"
        f"{fingerprints['cycle_plus']['bit_length']}"
    )
    print(
        "D2: odd_budget/p^w < 2^-"
        f"{expected['d2_max_strict_exponent']} (maximal strict exponent) PASS"
    )
    print(
        "D3: odd_budget/M < 2^-"
        f"{expected['d3_max_strict_exponent']} (maximal strict exponent) PASS"
    )
    print(
        "D4: M/p^w < 2^-"
        f"{expected['d4_max_strict_exponent']} (maximal strict exponent) PASS"
    )
    print(
        "D5: 16!*(M+odd_budget)/p^w < 2^-"
        f"{expected['d5_max_strict_exponent']} (maximal strict exponent) PASS"
    )
    print(
        "QUADRATIC_METHOD_FLOOR: "
        f"lambda2={expected['quadratic_lambda']} majorant/zero floor bits="
        f"{expected['quadratic_minus_excess_floor_bits']},"
        f"{expected['quadratic_plus_excess_floor_bits']} PASS"
    )
    print(
        "OVERLAP_GATE: checked through PR #"
        f"{certificate['publication_gate']['overlap_checked_through_pr']}; "
        f"decision={certificate['publication_gate']['decision']}"
    )
    print(f"NOVELTY: {certificate['claim_scope']['novelty']}")
    print("NONCLAIMS: " + "; ".join(certificate["nonclaims"]))
    print("RESULT: PASS")


def mutate_path(
    certificate: dict[str, Any], path: tuple[str | int, ...], mutation: Callable[[Any], Any]
) -> None:
    require(path, "mutation path must be nonempty")
    cursor: Any = certificate
    for key in path[:-1]:
        cursor = cursor[key]
    final_key = path[-1]
    cursor[final_key] = mutation(cursor[final_key])


def run_tamper_selftest(certificate: dict[str, Any]) -> None:
    verify_certificate(certificate)
    mutations: tuple[tuple[str, tuple[str | int, ...], Callable[[Any], Any]], ...] = (
        ("schema", ("schema_version",), lambda value: value + 1),
        ("base", ("base_commit",), lambda value: "0" + value[1:]),
        ("status", ("status",), lambda value: value + "_TAMPERED"),
        ("prime", ("parameters", "p"), lambda value: value + 2),
        ("q", ("parameters", "q"), lambda value: value + 1),
        ("width", ("parameters", "w"), lambda value: value - 1),
        ("minus_slice", ("parameters", "t_minus"), lambda value: value + 1),
        ("plus_slice", ("parameters", "t_plus"), lambda value: value - 1),
        ("blocks", ("parameters", "negative_blocks"), lambda value: value - 1),
        ("pair_cap", ("expected", "pair_cap"), lambda value: value + 1),
        (
            "odd_count",
            ("expected", "odd_mode_count"),
            lambda value: value + 1,
        ),
        (
            "D2",
            ("expected", "d2_max_strict_exponent"),
            lambda value: value + 1,
        ),
        (
            "D5",
            ("expected", "d5_max_strict_exponent"),
            lambda value: value - 1,
        ),
        (
            "fingerprint",
            (
                "expected",
                "large_integer_fingerprints",
                "odd_budget",
                "sha256_unsigned_be",
            ),
            lambda value: ("0" if value[0] != "0" else "1") + value[1:],
        ),
        (
            "overlap",
            ("publication_gate", "overlap_checked_through_pr"),
            lambda value: value - 1,
        ),
        (
            "novelty",
            ("claim_scope", "novelty"),
            lambda value: value + " and more",
        ),
        (
            "nonclaim",
            ("nonclaims", 0),
            lambda value: "C9 paid",
        ),
    )
    rejected = 0
    for label, path, mutation in mutations:
        corrupted = deepcopy(certificate)
        mutate_path(corrupted, path, mutation)
        caught = False
        try:
            verify_certificate(corrupted)
        except VerificationError:
            caught = True
        require(caught, f"tamper mutation survived: {label}")
        rejected += 1
    require(rejected == len(mutations), "tamper rejection count")
    print(f"TAMPER_SELFTEST: rejected={rejected}/{len(mutations)}")
    print("RESULT: PASS tamper-selftest")


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true", help="run the full check")
    modes.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="confirm that every in-memory mutation is rejected",
    )
    args = parser.parse_args()

    try:
        certificate = load_certificate()
        if args.check:
            result = verify_certificate(certificate)
            print_report(certificate, result)
        else:
            run_tamper_selftest(certificate)
    except VerificationError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
