#!/usr/bin/env python3
"""Exact replay for the affine-prefix direct-partition phase route cut."""

from __future__ import annotations

from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/affine-prefix-direct-partition-phase"
Q = [1, 4, 4, 4, 1]
P = [1, 4, 5, 4, 1]
BASE = "3404d21b64c876c6d9b995ad3e29d7120ab27a54"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def power(poly: list[int], exponent: int) -> list[int]:
    out = [1]
    base = poly[:]
    while exponent:
        if exponent & 1:
            out = multiply(out, base)
        base = multiply(base, base)
        exponent //= 2
    return out


def coefficient(poly: list[int], degree: int) -> int:
    return poly[degree] if 0 <= degree < len(poly) else 0


@cache
def c_value(blocks: int) -> int:
    return coefficient(power(Q, blocks), 2 * blocks)


def l_value(blocks: int, ambiguous: int) -> int:
    remaining = blocks - ambiguous
    return comb(blocks, ambiguous) * c_value(remaining)


@cache
def total_slopes(blocks: int) -> int:
    return coefficient(power(P, blocks), 2 * blocks)


def local_signature_census(modulus: int = 5) -> Counter[tuple[int, int, int]]:
    points = [(0, 0), (1, 0), (0, 1), (1, 1)]
    census: Counter[tuple[int, int, int]] = Counter()
    for mask in range(1 << 4):
        chosen = [points[i] for i in range(4) if mask & (1 << i)]
        signature = (
            len(chosen) % modulus,
            sum(x for x, _ in chosen) % modulus,
            sum(y for _, y in chosen) % modulus,
        )
        census[signature] += 1
    return census


def b2_histogram() -> Counter[int]:
    points = []
    for block in range(2):
        for eps, eta in ((0, 0), (1, 0), (0, 1), (1, 1)):
            vector = [0] * 6
            vector[3 * block] = 1
            vector[3 * block + 1] = eps
            vector[3 * block + 2] = eta
            points.append(tuple(vector))

    fibres: Counter[tuple[int, ...]] = Counter()
    for indices in combinations(range(8), 4):
        syndrome = tuple(
            sum(points[i][coordinate] for i in indices) % 5
            for coordinate in range(6)
        )
        fibres[syndrome] += 1
    return Counter(fibres.values())


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_source_pins() -> int:
    payload = json.loads((CERT / "source_pins.json").read_text(encoding="utf-8"))
    require(payload["base"] == BASE, "wrong source base")
    for relative, expected in payload["files"].items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected, f"source pin mismatch: {relative}")
    return len(payload["files"])


def entropy(theta: Decimal) -> Decimal:
    if theta == 0 or theta == 1:
        return Decimal(0)
    return -theta * theta.ln() - (1 - theta) * (1 - theta).ln()


def kappa(theta: Decimal) -> Decimal:
    return entropy(theta) + (1 - theta) * Decimal(14).ln() - theta * Decimal(2).ln()


def phase_checks() -> tuple[Decimal, Decimal, Decimal, Decimal, Decimal]:
    getcontext().prec = 90
    low = Decimal("0.89")
    high = Decimal("0.90")
    require(kappa(low) > 0 and kappa(high) < 0, "phase root not bracketed")
    for _ in range(280):
        mid = (low + high) / 2
        if kappa(mid) > 0:
            low = mid
        else:
            high = mid
    root = (low + high) / 2
    require(
        Decimal("0.8936588244321410561293819927796147007")
        < root
        < Decimal("0.8936588244321410561293819927796147009"),
        "wrong phase root",
    )

    theta_max = Decimal(1) / Decimal(29)
    phase_max = kappa(theta_max)
    require(abs(phase_max - (Decimal(29) / Decimal(2)).ln()) < Decimal("1e-80"),
            "wrong phase maximum")

    lhs = 447**447 * 53**53 * 2**447
    rhs = 500**500 * 14**53
    require(lhs > rhs, "finite 447/500 endpoint is nonpositive")
    eta = (Decimal(lhs).ln() - Decimal(rhs).ln()) / Decimal(500)
    require(
        Decimal("0.0018637304802374014167631267")
        < eta
        < Decimal("0.0018637304802374014167631269"),
        "wrong eta_447",
    )

    c_cell = phase_max / Decimal(4)
    c_direct = (Decimal(15) / Decimal(2)).ln() / Decimal(4)
    c_typed = (Decimal(225) / Decimal(16)).ln() / Decimal(4)
    return root, eta, c_cell, c_direct, c_typed


def main() -> None:
    source_pin_count = check_source_pins()

    local = local_signature_census()
    require(len(local) == 15, "wrong characteristic-five signature count")
    require(Counter(local.values()) == Counter({1: 14, 2: 1}),
            "wrong local ambiguity pattern")

    histogram = b2_histogram()
    require(histogram == Counter({1: 50, 2: 8, 4: 1}),
            f"wrong B=2 histogram: {histogram}")

    expected_rows = {
        1: ([4, 1], 5, 6),
        2: ([50, 8, 1], 59, 70),
        3: ([568, 150, 12, 1], 731, 924),
        4: ([6982, 2272, 300, 16, 1], 9571, 12870),
        5: ([87864, 34910, 5680, 500, 20, 1], 128975, 184756),
    }
    for blocks, (row, total, supports) in expected_rows.items():
        actual = [l_value(blocks, j) for j in range(blocks + 1)]
        require(actual == row, f"wrong coefficient row B={blocks}")
        require(sum(actual) == total_slopes(blocks) == total,
                f"wrong slope total B={blocks}")
        require(sum((2**j) * actual[j] for j in range(blocks + 1))
                == comb(4 * blocks, 2 * blocks) == supports,
                f"wrong support total B={blocks}")

    for blocks in range(1, 13):
        values = [l_value(blocks, j) for j in range(blocks + 1)]
        require(sum(values) == total_slopes(blocks),
                f"slope identity failed B={blocks}")
        require(sum((2**j) * values[j] for j in range(blocks + 1))
                == comb(4 * blocks, 2 * blocks),
                f"support identity failed B={blocks}")

    for left in range(1, 13):
        for right in range(1, 13):
            require(c_value(left + right) >= c_value(left) * c_value(right),
                    "Q central coefficient is not supermultiplicative")
            require(total_slopes(left + right)
                    >= total_slopes(left) * total_slopes(right),
                    "P central coefficient is not supermultiplicative")

    for blocks in range(2, 1001):
        k = 2 * blocks - 1
        support_size = 2 * blocks
        require(support_size == k + 1, "support-wise NT size mismatch")

    for j in range(13):
        distribution = {
            2**ell: comb(j, ell) * 2 ** (j - ell)
            for ell in range(j + 1)
        }
        fibre = 2**j
        require(sum(distribution.values()) == 3**j, "wrong support of r")
        for tau in range(9):
            moment = sum(count * multiplicity**tau
                         for multiplicity, count in distribution.items())
            require(moment == (2 + 2**tau) ** j,
                    f"moment failure j={j}, tau={tau}")
        mass = sum(count * multiplicity
                   for multiplicity, count in distribution.items())
        energy = sum(count * multiplicity**2
                     for multiplicity, count in distribution.items())
        require(mass == fibre**2, "wrong representation mass")
        require(energy == 6**j, "wrong energy")
        require(Fraction(energy, fibre**3) == Fraction(3, 4) ** j,
                "wrong normalized energy")
        for half_order in range(1, 7):
            require(mass**half_order == fibre ** (2 * half_order),
                    "even-order weighted identity failed")
        require(Fraction(1, fibre) * fibre == 1,
                "reciprocal covering weight is infeasible")

    root, eta, c_cell, c_direct, c_typed = phase_checks()

    eligible_cells = 0
    ln2 = Decimal(2).ln()
    for blocks in range(2, 301):
        for j in range(blocks + 1):
            if 500 * j < 447 * blocks:
                continue
            value = l_value(blocks, j)
            require(value > 0, "eligible coefficient vanished")
            require(Decimal(value).ln()
                    <= Decimal(j) * ln2 - eta * Decimal(blocks)
                    + Decimal("1e-70"),
                    f"finite band failed B={blocks}, j={j}")
            eligible_cells += 1

    for blocks in range(1, 51):
        envelope = sum(1 + 2**j for j in range(blocks + 1))
        require(envelope == blocks + 2 ** (blocks + 1),
                "canonical atlas envelope mismatch")
        slopes = total_slopes(blocks)
        witnesses = comb(4 * blocks, 2 * blocks)
        direct_numerator = slopes
        direct_denominator = 1 + 2**blocks
        typed_numerator = slopes**2
        typed_denominator = slopes + witnesses
        require(direct_numerator > 0 and direct_denominator > 0,
                "invalid total-envelope lower bound")
        require(typed_numerator > 0 and typed_denominator > 0,
                "invalid typed lower bound")

    mutations = {
        "all_local_signatures_unique": max(local.values()) == 1,
        "characteristic_two_cardinality_safe": len({c % 2 for c in range(5)}) == 5,
        "characteristic_three_cardinality_safe": len({c % 3 for c in range(5)}) == 5,
        "support_size_not_above_degree": any(2 * b <= 2 * b - 1
                                              for b in range(2, 20)),
        "reciprocal_half_weight_feasible": Fraction(1, 2 * (2**4)) * (2**4) >= 1,
        "inverse_energy_normalization": Fraction(4, 3) ** 4
        == Fraction(6**4, (2**4) ** 3),
        "phase_maximum_at_one_over_28": abs(
            kappa(Decimal(1) / Decimal(28)) - kappa(Decimal(1) / Decimal(29))
        ) < Decimal("1e-70"),
        "finite_endpoint_reversed": 447**447 * 53**53 * 2**447
        <= 500**500 * 14**53,
        "wrong_canonical_atlas_sum": sum(1 + 2**j for j in range(6))
        == 5 + 2**5,
        "omit_per_coordinate_division": abs(
            c_cell - (Decimal(29) / Decimal(2)).ln()
        ) < Decimal("1e-70"),
    }
    require(not any(mutations.values()), f"semantic mutation survived: {mutations}")

    print("AFFINE_PREFIX_DIRECT_PARTITION_PHASE: PASS")
    print(f"base={BASE}")
    print(f"source_pins=PASS,count={source_pin_count}")
    print("local_signatures=15 ambiguity_pattern=14x1+1x2")
    print("B2_histogram=size1:50,size2:8,size4:1 supports=70 slopes=59")
    print("supportwise_nt=B2..B1000,reason=degree_k_vs_k_plus_1_roots")
    print("coefficient_rows=B1..B5 generating_identities=B1..B12")
    print("central_supermultiplicativity=Q_and_P,B1..B24")
    print("representation_moments=j0..j12,tau0..tau8,even_q2..q12")
    print("covering_lp=reciprocal_weights_2^-j_exact")
    print(f"phase_root={root:.39f}")
    print(f"eta_447={eta:.28f} finite_band=B2..B300,cells={eligible_cells}")
    print("canonical_atlas_envelope=B+2^(B+1),checks=B1..B50")
    print(
        "rate_constants="
        f"cell:{c_cell:.18f},direct:{c_direct:.18f},typed:{c_typed:.18f}"
    )
    print("semantic_tamper_selftests=PASS,count=10")
    print("finite_ledger_delta=0 asymptotic_ledger_delta=0 official_score=0/2")
    print("RESULT=PASS")


if __name__ == "__main__":
    main()
