#!/usr/bin/env python3
"""Exact finite-row ledger for the B7--B11 mixed-petal residual coordinates.

This script is deliberately a finite diagnostic.  It enumerates every
admissible *size profile* for a bounded maximal-sunflower row, counts the exact
number of support patterns represented by that profile, and applies the proved
fixed-pattern cofactor injection.  It does not assert that every support
pattern is realizable, and it does not promote a finite profile escape into an
asymptotic counterexample.

Default usage recomputes and checks the frozen certificate::

    python3 experimental/scripts/verify_l1_mixed_petal_frontier_ledger.py

Other modes::

    ... --tamper-selftest
    ... --case q,n,k,sigma,E,V2,VR --json --include-profiles
    ... --write-certificate

All arithmetic is Python integer arithmetic.  No floating-point logarithms are
used in the certificate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import comb, factorial, isqrt
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-mixed-petal-frontier-ledger/certificate.json"
)


@dataclass(frozen=True)
class CaseSpec:
    q: int
    n: int
    k: int
    sigma: int
    E: int
    V2: int
    VR: int


@dataclass(frozen=True)
class Layout:
    q: int
    n: int
    k: int
    sigma: int
    ell: int
    s: int
    core_size: int
    M: int
    b: int
    maximal: bool


DEFAULT_CASES = (
    CaseSpec(q=97, n=16, k=8, sigma=2, E=0, V2=0, VR=0),
    CaseSpec(q=17, n=16, k=8, sigma=1, E=0, V2=1, VR=1),
    CaseSpec(q=17, n=16, k=6, sigma=1, E=0, V2=0, VR=0),
)


def comb0(n: int, k: int) -> int:
    if n < 0 or k < 0 or k > n:
        return 0
    return comb(n, k)


def ceil_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("ceil_div requires a positive denominator")
    return -(-numerator // denominator)


def is_prime_power(value: int) -> bool:
    """Exact trial-division check for the finite rows used by this ledger."""
    if value < 2:
        return False
    candidate = 2
    while candidate * candidate <= value and value % candidate:
        candidate += 1 if candidate == 2 else 2
    if candidate * candidate > value:
        return True
    remainder = value
    while remainder % candidate == 0:
        remainder //= candidate
    return remainder == 1


def layout_for(spec: CaseSpec) -> Layout:
    if spec.q < 2:
        raise ValueError("q must be at least 2")
    if not is_prime_power(spec.q):
        raise ValueError("q must be a prime power")
    if not 0 < spec.k < spec.k + spec.sigma <= spec.n:
        raise ValueError("require 0 < k < k+sigma <= n")
    if (spec.q - 1) % spec.n:
        raise ValueError("the evaluation subgroup requires n to divide q-1")
    if min(spec.E, spec.V2, spec.VR) < 0:
        raise ValueError("E, V2, and VR must be nonnegative fixed integers")
    ell = spec.sigma + 1
    core_size = spec.k - 1
    outside_core = spec.n - core_size
    M, b = divmod(outside_core, ell)
    if M < 1:
        raise ValueError("the row has no complete sunflower petal")
    return Layout(
        q=spec.q,
        n=spec.n,
        k=spec.k,
        sigma=spec.sigma,
        ell=ell,
        s=spec.k + spec.sigma,
        core_size=core_size,
        M=M,
        b=b,
        maximal=0 <= b < ell,
    )


def lambda_j(layout: Layout) -> int:
    """Smallest lambda >= 0 with (s+lambda)^2 > n(k-1)."""
    return max(0, isqrt(layout.n * (layout.k - 1)) + 1 - layout.s)


def multiset_permutation_count(values: tuple[int, ...]) -> int:
    counts = Counter(values)
    out = factorial(len(values))
    for multiplicity in counts.values():
        out //= factorial(multiplicity)
    return out


def smallest_integer_power_cover(base: int, value: int) -> int | None:
    """Return the least B >= 0 with value <= base^B, or None for bad base."""
    if base < 2:
        return None
    if value <= 1:
        return 0
    exponent = 0
    power = 1
    while power < value:
        power *= base
        exponent += 1
    return exponent


def classify_profile(
    *,
    all_full: bool,
    agreement_slack: int,
    lambda_threshold: int,
    excess: int,
    G2: int,
    GR: int,
    spec: CaseSpec,
) -> str:
    if all_full:
        return "FULL_PETAL_SEPARATE"
    if agreement_slack >= lambda_threshold:
        return "PAID_JOHNSON"
    if excess > spec.E:
        return "ESCAPES_BY_COFACTOR_EXCESS"
    if G2 <= spec.V2:
        return "PAID_G2"
    if GR <= spec.VR:
        return "PAID_GR"
    return "ESCAPES_BOUNDED_EXCESS_BOX"


def profile_rows(
    spec: CaseSpec,
    *,
    max_profiles: int,
) -> list[dict[str, object]]:
    """Enumerate exact aggregate size profiles for one bounded row.

    A profile stores the nonincreasing positive petal-hit multiset.  Its
    support-pattern multiplicity includes assignments of that multiset to the
    chosen labelled petals, the point subsets inside those petals, and the
    background subset.  Lemma 17/B3 then bounds all codewords for each fixed
    support pattern without an extra choice of the missed core D.
    """

    layout = layout_for(spec)
    lj = lambda_j(layout)
    rows: list[dict[str, object]] = []

    for d in range(layout.core_size + 1):
        max_hit = min(layout.ell, d)
        if max_hit == 0:
            continue
        for r in range(layout.b + 1):
            background_choices = comb(layout.b, r)
            for t in range(2, layout.M + 1):
                petal_choices = comb(layout.M, t)
                for hits_ascending in itertools.combinations_with_replacement(
                    range(1, max_hit + 1), t
                ):
                    hits = tuple(reversed(hits_ascending))
                    h = sum(hits)
                    agreement_slack = r + h - (layout.ell + d)
                    if agreement_slack < 0:
                        continue

                    deficits = tuple(layout.ell - hit for hit in hits)
                    G2 = deficits[0] + deficits[1]
                    GR = (layout.ell - r) + deficits[0]
                    excess = d - layout.ell
                    a_star = hits[0]
                    all_full = all(hit == layout.ell for hit in hits)

                    width_floor_a1 = ceil_div(layout.ell + d - r, hits[0])
                    remaining = max(0, layout.ell + d - r - hits[0])
                    width_floor_a2 = 1 + ceil_div(remaining, hits[1])
                    width_gate_slack = (
                        2 * (t - 1) * layout.ell
                        - (2 * max(0, excess + GR) + (t - 1) * G2)
                    )
                    if width_gate_slack < 0:
                        raise RuntimeError(
                            "B9 width gate violated by an admissible profile: "
                            f"d={d},r={r},hits={hits},slack={width_gate_slack}"
                        )
                    if t < width_floor_a1 or t < width_floor_a2:
                        raise RuntimeError(
                            "B8 width floor violated by an admissible profile: "
                            f"d={d},r={r},hits={hits},"
                            f"floors=({width_floor_a1},{width_floor_a2})"
                        )

                    assignment_count = multiset_permutation_count(hits)
                    point_subset_count = 1
                    for hit in hits:
                        point_subset_count *= comb(layout.ell, hit)
                    support_pattern_count = (
                        background_choices
                        * petal_choices
                        * assignment_count
                        * point_subset_count
                    )

                    lemma17_exponent = d - a_star + 1
                    if lemma17_exponent < 0:
                        raise RuntimeError("Lemma 2 should force a_star <= d")
                    background_anchor_exponent = max(
                        0, d - max(r, a_star) + 1
                    )
                    if layout.b == 0:
                        selected_exponent = lemma17_exponent
                        selected_source = "LEMMA_17"
                    else:
                        selected_exponent = background_anchor_exponent
                        selected_source = "LEMMA_B3"

                    route = classify_profile(
                        all_full=all_full,
                        agreement_slack=agreement_slack,
                        lambda_threshold=lj,
                        excess=excess,
                        G2=G2,
                        GR=GR,
                        spec=spec,
                    )
                    row = {
                        "d": d,
                        "r": r,
                        "t": t,
                        "a_i": list(hits),
                        "a_star": a_star,
                        "u": sum(deficits),
                        "d_minus_ell": excess,
                        "G2": G2,
                        "GR": GR,
                        "lambda": agreement_slack,
                        "lambda_J": lj,
                        "lambda_minus_lambda_J": agreement_slack - lj,
                        "all_full": all_full,
                        "mixed_partial_target": not all_full,
                        "width_floor_a1": width_floor_a1,
                        "width_floor_a2": width_floor_a2,
                        "width_gate_slack": width_gate_slack,
                        "support_pattern_count": support_pattern_count,
                        "lemma17_exponent": lemma17_exponent,
                        "background_anchor_exponent": background_anchor_exponent,
                        "selected_injection_source": selected_source,
                        "selected_injection_exponent": selected_exponent,
                        "selected_injection_bound": (
                            support_pattern_count * layout.q**selected_exponent
                        ),
                        "b11_box_route": route,
                    }
                    rows.append(row)
                    if len(rows) > max_profiles:
                        raise RuntimeError(
                            f"profile limit {max_profiles} exceeded; "
                            "use a smaller finite row or raise --max-profiles"
                        )

    rows.sort(
        key=lambda row: (
            int(row["d"]),
            int(row["r"]),
            int(row["t"]),
            tuple(-int(hit) for hit in row["a_i"]),
        )
    )
    return rows


def theorem_box_bounds(spec: CaseSpec, layout: Layout) -> dict[str, object]:
    lj = lambda_j(layout)
    threshold = layout.s + lj
    johnson_denominator = threshold * threshold - layout.n * (layout.k - 1)
    if johnson_denominator <= 0:
        raise RuntimeError("lambda_J failed to enter the strict Johnson region")
    johnson_numerator = layout.n * (layout.n - layout.k + 1)
    johnson_fraction = Fraction(johnson_numerator, johnson_denominator)
    johnson_unique = 2 * threshold > layout.n + layout.k - 1
    johnson_floor = 1 if johnson_unique else johnson_fraction.numerator // johnson_fraction.denominator

    b5_support_sum = sum(comb0(2 * layout.ell, v) for v in range(spec.V2 + 1))
    b5 = (
        comb(layout.M, 2)
        * b5_support_sum
        * layout.q ** (2 * spec.E + spec.V2 + 2)
    )

    b6_support_sum = 0
    for w in range(spec.VR + 1):
        for v in range(spec.VR - w + 1):
            b6_support_sum += comb0(layout.b, layout.ell - w) * comb0(
                layout.ell, v
            )
    b6 = (
        layout.M
        * b6_support_sum
        * layout.q ** (2 * spec.E + spec.VR + 2)
    )

    return {
        "lambda_J": lj,
        "johnson": {
            "threshold": threshold,
            "unique_decoding_at_threshold": johnson_unique,
            "raw_numerator": johnson_numerator,
            "raw_denominator": johnson_denominator,
            "reduced_numerator": johnson_fraction.numerator,
            "reduced_denominator": johnson_fraction.denominator,
            "integer_floor_bound": johnson_floor,
        },
        "B5_two_anchor_bound": b5,
        "B6_background_petal_bound": b6,
        "B11_union_bound": johnson_floor + b5 + b6,
    }


def case_report(
    spec: CaseSpec,
    *,
    max_profiles: int,
    include_profiles: bool,
) -> dict[str, object]:
    layout = layout_for(spec)
    rows = profile_rows(spec, max_profiles=max_profiles)
    digest_payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(digest_payload.encode("utf-8")).hexdigest()

    class_profile_counts: Counter[str] = Counter()
    class_support_patterns: Counter[str] = Counter()
    class_injection_bounds: Counter[str] = Counter()
    for row in rows:
        route = str(row["b11_box_route"])
        class_profile_counts[route] += 1
        class_support_patterns[route] += int(row["support_pattern_count"])
        class_injection_bounds[route] += int(row["selected_injection_bound"])

    unresolved_routes = (
        "ESCAPES_BY_COFACTOR_EXCESS",
        "ESCAPES_BOUNDED_EXCESS_BOX",
    )
    unresolved_bound = sum(class_injection_bounds[route] for route in unresolved_routes)
    selected_total = sum(class_injection_bounds.values())
    unresolved_rows = [
        row for row in rows if row["b11_box_route"] in unresolved_routes
    ]
    unresolved_rows.sort(
        key=lambda row: int(row["selected_injection_bound"]), reverse=True
    )

    report: dict[str, object] = {
        "case": asdict(spec),
        "layout": asdict(layout),
        "hypothesis_visibility": {
            "finite_row_only": True,
            "q_poly_family_hyp_provided": False,
            "l1_lower_cutoff_family_hyp_provided": False,
            "fixed_thresholds_across_family": False,
            "exact_codeword_dedup": False,
            "exact_agreement_sets_enumerated": False,
            "profile_bounds_are_upper_bounds_not_realizability_counts": True,
            "lemma17_applicable": layout.b == 0,
            "lemmaB3_applicable": layout.maximal,
            "B11_applicable_as_finite_coordinate_partition": layout.maximal,
        },
        "theorem_box_bounds": theorem_box_bounds(spec, layout),
        "summary": {
            "profile_count": len(rows),
            "profile_sha256": digest,
            "all_width_gate_slacks_nonnegative": True,
            "class_profile_counts": dict(sorted(class_profile_counts.items())),
            "class_support_pattern_counts": dict(
                sorted(class_support_patterns.items())
            ),
            "class_injection_bound_totals": dict(
                sorted(class_injection_bounds.items())
            ),
            "selected_injection_bound_total": selected_total,
            "unresolved_injection_bound_total": unresolved_bound,
            "finite_n_power_cover_selected_total": smallest_integer_power_cover(
                layout.n, selected_total
            ),
            "finite_n_power_cover_unresolved_total": smallest_integer_power_cover(
                layout.n, unresolved_bound
            ),
            "diagnostic_conclusion": (
                "FINITE_PROFILE_BOX_HAS_NO_UNRESOLVED_UPPER_BOUND_MASS"
                if unresolved_bound == 0
                else "FINITE_PROFILE_LEDGER_REQUIRES_NEW_STRUCTURE"
            ),
        },
        "largest_unresolved_profiles": unresolved_rows[:8],
    }
    if include_profiles:
        report["profiles"] = rows
    return report


def build_certificate(*, max_profiles: int = 200_000) -> dict[str, object]:
    return {
        "schema": "rs-mca-l1-mixed-petal-frontier-ledger-v1",
        "status": "EXPERIMENTAL/AUDIT",
        "date": "2026-07-14",
        "statement": (
            "exact finite-row support-pattern and cofactor-injection ledger "
            "for the B7--B11 mixed/partial-petal coordinates"
        ),
        "sources": {
            "program": "experimental/notes/l1/l1_full_list_quotient_proof_program.md",
            "audit": "experimental/notes/l1/l1_imgfib_crosswalk_audit.md",
            "lemmas": ["17", "B3", "B5", "B6", "B7", "B8", "B9", "B10", "B11"],
        },
        "nonclaims": [
            "does not prove realizability of any enumerated support profile",
            "does not turn finite escapes into asymptotic sequences",
            "does not prove mixed-petal amplification or a blanket ImgFib bound",
            "does not merge generated, line, challenge, base, or extension fields",
        ],
        "cases": [
            case_report(
                spec,
                max_profiles=max_profiles,
                include_profiles=False,
            )
            for spec in DEFAULT_CASES
        ],
    }


def compare_certificate(expected: dict[str, object], actual: dict[str, object]) -> bool:
    return expected == actual


def tamper_selftest(actual: dict[str, object]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, object]], None]]] = [
        ("schema", lambda value: value.__setitem__("schema", "tampered")),
        (
            "profile_count",
            lambda value: value["cases"][0]["summary"].__setitem__(
                "profile_count", value["cases"][0]["summary"]["profile_count"] + 1
            ),
        ),
        (
            "profile_sha256",
            lambda value: value["cases"][0]["summary"].__setitem__(
                "profile_sha256", "0" * 64
            ),
        ),
        (
            "unresolved_bound",
            lambda value: value["cases"][0]["summary"].__setitem__(
                "unresolved_injection_bound_total",
                value["cases"][0]["summary"]["unresolved_injection_bound_total"]
                + 1,
            ),
        ),
        (
            "lambda_J",
            lambda value: value["cases"][1]["theorem_box_bounds"].__setitem__(
                "lambda_J", value["cases"][1]["theorem_box_bounds"]["lambda_J"] + 1
            ),
        ),
        (
            "width_gate",
            lambda value: value["cases"][1]["summary"].__setitem__(
                "all_width_gate_slacks_nonnegative", False
            ),
        ),
    ]
    failed = False
    for name, mutate in mutations:
        changed = copy.deepcopy(actual)
        mutate(changed)
        caught = not compare_certificate(changed, actual)
        print(f"  tamper {name:<20}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught
    if failed:
        print("TAMPER-SELFTEST: FAIL")
        return 1
    print("TAMPER-SELFTEST: PASS (every corruption caught)")
    return 0


def parse_case(raw: str) -> CaseSpec:
    try:
        values = [int(part.strip()) for part in raw.split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("case entries must be integers") from exc
    if len(values) != 7:
        raise argparse.ArgumentTypeError(
            "--case must have form q,n,k,sigma,E,V2,VR"
        )
    return CaseSpec(*values)


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=parse_case)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-profiles", action="store_true")
    parser.add_argument("--max-profiles", type=int, default=200_000)
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))

    if args.max_profiles <= 0:
        parser.error("--max-profiles must be positive")
    if args.case is not None:
        try:
            report = case_report(
                args.case,
                max_profiles=args.max_profiles,
                include_profiles=args.include_profiles,
            )
        except ValueError as exc:
            parser.error(str(exc))
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    actual = build_certificate(max_profiles=args.max_profiles)
    if args.write_certificate:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(actual, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0

    if not CERTIFICATE_PATH.exists():
        print(f"missing frozen certificate: {CERTIFICATE_PATH}", file=sys.stderr)
        return 2
    expected = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    if not compare_certificate(expected, actual):
        print("RESULT: FAIL (frozen certificate drift)", file=sys.stderr)
        return 1

    for case in actual["cases"]:
        spec = case["case"]
        summary = case["summary"]
        print(
            "[PASS] "
            f"q={spec['q']},n={spec['n']},k={spec['k']},sigma={spec['sigma']}: "
            f"profiles={summary['profile_count']}, "
            f"unresolved_bound={summary['unresolved_injection_bound_total']}, "
            f"digest={summary['profile_sha256'][:16]}..."
        )
    print("RESULT: PASS (frozen exact profile ledger reproduced)")
    if args.tamper_selftest:
        return tamper_selftest(actual)
    if args.json:
        print(json.dumps(actual, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
