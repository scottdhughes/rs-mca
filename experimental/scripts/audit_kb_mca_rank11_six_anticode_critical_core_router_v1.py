#!/usr/bin/env python3
"""Independent exact audit for the six-anticode / critical-core router.

This implementation deliberately does not import the primary verifier.  It
uses a falling-binomial recurrence for the fixed-endpoint envelope and a
product-ratio implementation for the common-core averaging calculation.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb
from pathlib import Path
import hashlib
import json

P = 2130706433
EXT = 6
N = 2097152
K = 1048576
M = 1116048
W = 67472
NEAR = 134944
BUDGET = 274980728111395087
RESOURCE = 106618568137036225644
RANK = 10
RAY = 8147918


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def required_low(tau: int) -> int:
    return BUDGET - NEAR - RESOURCE // (tau + 1) + 1


def binomial_profile(limit: int) -> list[int]:
    """Return C(K-q+10,10), q=0..limit, by exact recurrence."""
    profile = [comb(K + RANK, RANK)]
    current = profile[0]
    for q in range(limit):
        numerator = K - q
        denominator = K - q + RANK
        current = current * numerator // denominator
        profile.append(current)
    return profile


def low_interval_max(
    g_values: list[int], count: int, required_total: int, peak: int, endpoint: int
) -> tuple[int, tuple[int, ...]] | None:
    required_total = max(0, required_total)
    if count == 0:
        return (0, ()) if required_total == 0 else None
    if required_total > count * endpoint:
        return None
    if required_total <= count * peak:
        return count * g_values[peak], (peak,) * count
    lower, extra = divmod(required_total, count)
    values = (lower,) * (count - extra) + (lower + 1,) * extra
    return sum(g_values[q] for q in values), values


def audit_six_anticodes() -> dict[str, int]:
    tau = 1798
    agreement = M - tau
    denominator = comb(W - tau + RANK, RANK)
    q_limit = N - agreement
    profile = binomial_profile(q_limit)
    maximum = -1
    maxima: list[int] = []
    for q, coefficient in enumerate(profile):
        value = q * (coefficient // denominator) + 1
        if value > maximum:
            maximum = value
            maxima = [q]
        elif value == maximum:
            maxima.append(q)
    assert maxima == [95326]
    q_peak = maxima[0]

    high = RESOURCE // (tau + 1)
    required = required_low(tau)
    five_total = NEAR + high + 5 * maximum
    six_total = NEAR + high + 6 * maximum
    assert five_total == 256951591393251779
    assert BUDGET - five_total == 18029136718143308
    assert six_total == 296488817049636544
    assert six_total - BUDGET == 21508088938241457
    assert 5 * maximum + RAY < required

    threshold = required - 5 * maximum
    outer = max(
        q for q in range(q_peak, q_limit + 1)
        if q * (profile[q] // denominator) + 1 >= threshold
    )
    assert outer == 247518
    assert outer * (profile[outer] // denominator) + 1 == 18029257843230307
    assert (outer + 1) * (profile[outer + 1] // denominator) + 1 == 18029105617115083
    common_endpoint = N - outer
    triple = 3 * common_endpoint - 2 * N
    assert common_endpoint == 1849634
    assert triple == 1354598 > K

    for q in range(q_limit + 1):
        profile[q] *= q
    g_values = profile
    peak = max(range(q_limit + 1), key=g_values.__getitem__)
    assert peak == 95326
    concavity_endpoint = 190651
    high_min = concavity_endpoint + 1
    for q in range(1, concavity_endpoint + 1):
        assert g_values[q + 1] - 2 * g_values[q] + g_values[q - 1] <= 0
    for q in range(high_min, q_limit):
        assert g_values[q + 1] - 2 * g_values[q] + g_values[q - 1] >= 0
        assert g_values[q + 1] < g_values[q]

    support_first_excluded = 167814
    support_load = 5 * support_first_excluded
    cases: list[Fraction] = []
    configurations: list[tuple[int, int | None, tuple[int, ...]]] = []

    for high_count in range(7):
        low_count = 6 - high_count
        best: int | None = None
        best_config: tuple[int, int | None, tuple[int, ...]] | None = None
        if high_count == 0:
            low = low_interval_max(
                g_values, low_count, support_load, peak, concavity_endpoint
            )
            assert low is not None
            best, lows = low
            best_config = (0, None, lows)
        else:
            for upper_count in range(high_count):
                lower_count = high_count - upper_count - 1
                base_load = upper_count * q_limit + lower_count * high_min
                base_value = (
                    upper_count * g_values[q_limit]
                    + lower_count * g_values[high_min]
                )
                for residual in range(high_min, q_limit + 1):
                    low = low_interval_max(
                        g_values,
                        low_count,
                        support_load - base_load - residual,
                        peak,
                        concavity_endpoint,
                    )
                    if low is None:
                        continue
                    low_value, lows = low
                    candidate = base_value + g_values[residual] + low_value
                    if best is None or candidate > best:
                        best = candidate
                        best_config = (upper_count, residual, lows)
        assert best is not None and best_config is not None
        bound = Fraction(best, denominator) + 6
        assert bound < required
        cases.append(bound)
        configurations.append(best_config)

    worst = max(range(7), key=cases.__getitem__)
    assert worst == 0
    assert configurations[0] == (0, None, (139845,) * 6)
    critical_gap = Fraction(required) - cases[0]
    assert critical_gap == Fraction(
        5039866042250644297697303907940552741600048679872,
        7575576854420300947226509036769468677,
    )

    return {
        "tau": tau,
        "five_slack": BUDGET - five_total,
        "six_overage": six_total - BUDGET,
        "outer_q": outer,
        "common_endpoint": common_endpoint,
        "triple_intersection": triple,
        "maximum_pair_error_support": support_first_excluded - 1,
        "worst_support_case": worst,
    }


def core_average(required: int, agreement: int, size: int) -> Fraction:
    value = Fraction(required)
    for offset in range(size):
        value *= Fraction(agreement - offset, N - offset)
    return value


def pair_cap_two(tau: int) -> int:
    return comb(K + 2, 2) // comb(W - tau + 2, 2)


def audit_critical_core() -> dict[str, int]:
    best_types: tuple[int, int, dict[str, int]] | None = None
    best_gap: tuple[int, int, dict[str, int]] | None = None
    best_33: tuple[int, int, int, int, dict[str, int]] | None = None
    forcing = 0

    for tau in range(1, W):
        agreement = M - tau
        required = required_low(tau)
        owner = N - agreement
        q2 = pair_cap_two(tau)

        average32 = core_average(required, agreement, 32)
        slopes32 = ceil_fraction(average32)
        types32 = (slopes32 + owner - 1) // owner
        gap32 = types32 - q2
        record32 = {
            "tau": tau,
            "agreement": agreement,
            "slopes": slopes32,
            "types": types32,
            "q2": q2,
            "gap": gap32,
        }
        candidate_types = (types32, -tau, record32)
        candidate_gap = (gap32, -tau, record32)
        if best_types is None or candidate_types[:2] > best_types[:2]:
            best_types = candidate_types
        if best_gap is None or candidate_gap[:2] > best_gap[:2]:
            best_gap = candidate_gap
        if gap32 > 0:
            forcing += 1

        average33 = core_average(required, agreement, 33)
        slopes33 = ceil_fraction(average33)
        types33 = (slopes33 + owner - 1) // owner
        gap33 = types33 - q2
        record33 = {
            "tau": tau,
            "agreement": agreement,
            "slopes": slopes33,
            "types": types33,
            "q2": q2,
            "gap": gap33,
        }
        candidate33 = (gap33, types33, slopes33, -tau, record33)
        if best_33 is None or candidate33[:4] > best_33[:4]:
            best_33 = candidate33

    assert best_types is not None and best_gap is not None and best_33 is not None
    chosen = best_types[2]
    assert chosen == {
        "tau": 3304,
        "agreement": 1112744,
        "slopes": 378013809,
        "types": 385,
        "q2": 267,
        "gap": 118,
    }
    assert pair_cap_two(3304) ** 2 < P**EXT
    assert forcing == 9675
    assert best_gap[2]["tau"] == 2673
    assert best_gap[2]["gap"] == 119
    wall = best_33[4]
    assert wall == {
        "tau": 2815,
        "agreement": 1113233,
        "slopes": 198803088,
        "types": 203,
        "q2": 262,
        "gap": -59,
    }

    return {
        "tau": chosen["tau"],
        "slopes": chosen["slopes"],
        "types": chosen["types"],
        "pair_cap": chosen["q2"],
        "dimension_floor": 3,
        "forcing_cutoffs": forcing,
        "core33_gap": wall["gap"],
    }


def verify_manifest() -> str:
    path = Path(
        "experimental/data/certificates/"
        "kb-mca-rank11-six-anticode-critical-core-router-v1/manifest.json"
    )
    manifest = json.loads(path.read_text())
    for record in manifest["files"]:
        data = Path(record["path"]).read_bytes()
        assert len(data) == record["bytes"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
    payload = {key: value for key, value in manifest.items()
               if key != "canonical_payload_sha256"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    assert digest == manifest["canonical_payload_sha256"]
    return digest


def main() -> None:
    six = audit_six_anticodes()
    core = audit_critical_core()
    payload = verify_manifest()
    print(
        "KB_MCA_RANK11_SIX_ANTICODE_CORE_AUDIT_PASS "
        f"five_slack={six['five_slack']} "
        f"support_max={six['maximum_pair_error_support']} "
        f"core32_slopes={core['slopes']} "
        f"core32_types={core['types']} "
        f"payload={payload}"
    )


if __name__ == "__main__":
    main()
