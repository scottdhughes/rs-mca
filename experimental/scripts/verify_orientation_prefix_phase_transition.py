#!/usr/bin/env python3
"""Certify the proved special coarse orientation-prefix phase bracket.

For q=3^r, N=q-1=2a, and 0<=u<=a-2, equal locator prefixes force
the ternary orientation-difference word to vanish at every odd Fourier
frequency whose Frobenius orbit meets [1,u]. If E_(r,u) is the number of
odd frequencies whose orbit avoids that interval, each orientation-prefix
fiber is at most 2^E_(r,u) by an information-set projection.

This stdlib-only verifier exhausts F_9 and F_27, checks exact Frobenius
avoidance counts on safe rows, audits the conditional Janson inequalities,
and checks the high-depth Plotkin consequence. It does not claim an exact
image size, endpoint injectivity, or an unconditional Janson estimate.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
import resource
import sys
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_FLOOR, localcontext
from pathlib import Path
from typing import Any, Callable, Iterable


STATUS = "PROVED_SPECIAL_COARSE_PHASE_BRACKET"
SCHEMA = "orientation_prefix_phase_transition.v1"
BASE_SHA = "5091826cd6a91becda5e54393b209b9ccc7ffc89"
ADDRESS_SPACE_CAP_BYTES = 1024**3
ARTIFACT = Path(
    "experimental/data/certificates/orientation-prefix-phase-transition/"
    "orientation_prefix_phase_transition.json"
)
PHASE_NOTE = Path(
    "experimental/notes/thresholds/orientation_prefix_phase_transition.md"
)
FRONTIERS_TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
FINITE_FIELDS = {
    2: (1, 0, 1),       # X^2+1
    3: (1, 2, 0, 1),    # X^3-X+1
}
EXACT_JANSON_R = tuple(range(2, 11))
SUPERCRITICAL_SAMPLES = ((16, 4), (25, 5), (36, 6), (49, 7))

FIXED_C_VALUES = (1, 2, 4, 8)
FIXED_C_SAMPLE_R = (12, 16, 32, 64)
TEX_LABEL_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "def:profile-payment": (
        "uniformly in the received line",
        "given first-match atlas",
    ),
    "prop:exact-prefix-list": (
        "1\\le K\\le m\\le n",
        "w=m-K",
        "No such codeword agrees on more than",
    ),
    "def:paid-cell": (
        "actual first-match projection",
        "scaled realized cell",
    ),
    "def:structured-folding": (
        "complete-fiber folding map",
        "multiplicative coset",
    ),
}

SOURCE_REQUIREMENTS: dict[Path, tuple[str, ...]] = {
    PHASE_NOTE: (
        "E_{r,u}",
        "Janson",
        "Plotkin",
        "2^{|E_{r,u}|}",
        "\\frac q2",
        "first nonzero digit",
        "\\tag{CW}",
    ),
    Path(
        "experimental/notes/thresholds/"
        "full_agreement_orientation_saturation.md"
    ): (
        "C_S(T)C_S(-T)=1-T^(2a)",
        "ceil(2^a/q^ceil(u/2))",
        "No statement in this packet is",
    ),
    Path("experimental/notes/l1/l1_aperiodic_prefix_collision.md"): (
        "constant-weight code",
        "minimum Hamming distance",
        "Plotkin-type bound",
    ),
}


class CheckFailure(AssertionError):
    """Raised when an exact replay invariant fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


def repo_root() -> Path:
    override = os.environ.get("OPPT_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def impose_address_space_cap() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = ADDRESS_SPACE_CAP_BYTES
    if hard != resource.RLIM_INFINITY:
        cap = min(cap, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    require(
        soft != resource.RLIM_INFINITY and soft <= ADDRESS_SPACE_CAP_BYTES,
        "RLIMIT_AS exceeds one GiB",
    )
    return int(soft)


def without_hash(obj: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(obj)
    out.pop("payload_sha256", None)
    return out


def payload_hash(obj: dict[str, Any]) -> str:
    raw = json.dumps(
        without_hash(obj), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def prime_factors(value: int) -> tuple[int, ...]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return tuple(factors)


class GF3Extension:
    """Tiny table-backed F_3[X]/(modulus), sufficient for q=9,27."""

    def __init__(self, modulus: tuple[int, ...]):
        require(modulus[-1] % 3 == 1, "finite-field modulus monic")
        self.modulus = tuple(value % 3 for value in modulus)
        self.degree = len(modulus) - 1
        self.q = 3**self.degree
        self._digits = tuple(self._decode(value) for value in range(self.q))
        self.add_table = tuple(
            tuple(self._add_raw(x, y) for y in range(self.q))
            for x in range(self.q)
        )
        self.mul_table = tuple(
            tuple(self._mul_raw(x, y) for y in range(self.q))
            for x in range(self.q)
        )

    def _decode(self, value: int) -> tuple[int, ...]:
        digits = []
        for _ in range(self.degree):
            digits.append(value % 3)
            value //= 3
        return tuple(digits)

    @staticmethod
    def _encode(digits: Iterable[int]) -> int:
        out = 0
        place = 1
        for digit in digits:
            out += (digit % 3) * place
            place *= 3
        return out

    def _add_raw(self, left: int, right: int) -> int:
        return self._encode(
            (a + b) % 3
            for a, b in zip(self._digits[left], self._digits[right])
        )

    def _mul_raw(self, left: int, right: int) -> int:
        raw = [0] * (2 * self.degree - 1)
        for i, a in enumerate(self._digits[left]):
            for j, b in enumerate(self._digits[right]):
                raw[i + j] += a * b
        for degree in range(len(raw) - 1, self.degree - 1, -1):
            coefficient = raw[degree] % 3
            if coefficient:
                for offset in range(self.degree):
                    raw[degree - self.degree + offset] -= (
                        coefficient * self.modulus[offset]
                    )
        return self._encode(raw[: self.degree])

    def add(self, left: int, right: int) -> int:
        return self.add_table[left][right]

    def neg(self, value: int) -> int:
        return self._encode((-digit) % 3 for digit in self._digits[value])

    def mul(self, left: int, right: int) -> int:
        return self.mul_table[left][right]

    def pow(self, value: int, exponent: int) -> int:
        out = 1
        base = value
        while exponent:
            if exponent & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            exponent >>= 1
        return out

    def primitive_element(self) -> int:
        order = self.q - 1
        factors = prime_factors(order)
        for candidate in range(2, self.q):
            if all(
                self.pow(candidate, order // factor) != 1
                for factor in factors
            ):
                return candidate
        raise CheckFailure("primitive finite-field element not found")

    def digits(self, value: int) -> tuple[int, ...]:
        return self._digits[value]


def locator_polynomial(
    field: GF3Extension, roots: tuple[int, ...]
) -> list[int]:
    coefficients = [1]
    for root in roots:
        nxt = [0] * (len(coefficients) + 1)
        for degree, coefficient in enumerate(coefficients):
            nxt[degree] = field.add(
                nxt[degree], field.neg(field.mul(root, coefficient))
            )
            nxt[degree + 1] = field.add(
                nxt[degree + 1], coefficient
            )
        coefficients = nxt
    return coefficients


def matrix_rank_mod3(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    rows = [row[:] for row in matrix]
    width = len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                index
                for index in range(pivot_row, len(rows))
                if rows[index][column] % 3
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = 1 if rows[pivot_row][column] % 3 == 1 else 2
        rows[pivot_row] = [
            inverse * value % 3 for value in rows[pivot_row]
        ]
        for index in range(len(rows)):
            if index == pivot_row:
                continue
            multiple = rows[index][column] % 3
            if multiple:
                rows[index] = [
                    (left - multiple * right) % 3
                    for left, right in zip(rows[index], rows[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row

def nullspace_basis_mod3(
    matrix: list[list[int]], width: int
) -> list[list[int]]:
    require(
        all(len(row) == width for row in matrix),
        "nullspace matrix width",
    )
    original = [[value % 3 for value in row] for row in matrix]
    rows = [row[:] for row in original if any(row)]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                index
                for index in range(pivot_row, len(rows))
                if rows[index][column] % 3
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = 1 if rows[pivot_row][column] == 1 else 2
        rows[pivot_row] = [
            inverse * value % 3 for value in rows[pivot_row]
        ]
        for index in range(len(rows)):
            if index == pivot_row:
                continue
            multiple = rows[index][column] % 3
            if multiple:
                rows[index] = [
                    (left - multiple * right) % 3
                    for left, right in zip(rows[index], rows[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    free_columns = [
        column for column in range(width)
        if column not in pivot_columns
    ]
    basis = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for index, pivot in enumerate(pivot_columns):
            vector[pivot] = (-rows[index][free]) % 3
        basis.append(vector)
    require(
        len(basis) == width - len(pivot_columns),
        "nullspace dimension",
    )
    require(
        all(
            sum(left * right for left, right in zip(row, vector)) % 3 == 0
            for row in original
            for vector in basis
        ),
        "nullspace basis vectors satisfy constraints",
    )
    return basis


def information_set_positions(
    basis: list[list[int]], width: int
) -> tuple[int, ...]:
    if not basis:
        return ()
    require(
        all(len(vector) == width for vector in basis),
        "information-set basis width",
    )
    dimension = len(basis)
    selected: list[int] = []
    current_rank = 0
    for column in range(width):
        candidate = selected + [column]
        projected = [
            [vector[position] for position in candidate]
            for vector in basis
        ]
        next_rank = matrix_rank_mod3(projected)
        if next_rank > current_rank:
            selected.append(column)
            current_rank = next_rank
        if current_rank == dimension:
            break
    require(
        current_rank == dimension and len(selected) == dimension,
        "information-set projection injective on direction space",
    )
    return tuple(selected)



def odd_frobenius_orbits(r: int) -> list[tuple[int, ...]]:
    q = 3**r
    modulus = q - 1
    unseen = set(range(1, modulus, 2))
    orbits = []
    while unseen:
        start = min(unseen)
        orbit = []
        current = start
        while current not in orbit:
            require(current % 2 == 1, "Frobenius preserves odd frequencies")
            orbit.append(current)
            current = 3 * current % modulus
        require(current == start, "Frobenius orbit closes at its start")
        orbit_tuple = tuple(orbit)
        require(all(value in unseen for value in orbit_tuple), "orbit partition")
        unseen.difference_update(orbit_tuple)
        orbits.append(orbit_tuple)
    require(sum(map(len, orbits)) == (q - 1) // 2, "odd orbit mass")
    require(
        all(r % len(orbit) == 0 for orbit in orbits),
        "orbit sizes divide r",
    )
    return orbits


def avoidance_from_orbits(
    r: int, u: int, orbits: list[tuple[int, ...]]
) -> dict[str, Any]:
    q = 3**r
    a = (q - 1) // 2
    require(0 <= u <= a - 2, "legal orientation-prefix depth")
    avoiding = [orbit for orbit in orbits if min(orbit) > u]
    hit = [orbit for orbit in orbits if min(orbit) <= u]
    e_value = sum(map(len, avoiding))
    direct = sum(
        all(
            (pow(3, step, q - 1) * frequency) % (q - 1) > u
            for step in range(r)
        )
        for frequency in range(1, q - 1, 2)
    )
    checks = {
        "direct_avoidance_matches_orbit_sum": direct == e_value,
        "hit_and_avoid_partition_odd_frequencies": (
            sum(map(len, hit)) + e_value == a
        ),
        "all_avoiding_orbits_miss_window": all(
            all(value > u for value in orbit) for orbit in avoiding
        ),
        "all_hit_orbits_meet_window": all(
            any(value <= u for value in orbit) for orbit in hit
        ),
    }
    require(all(checks.values()), "exact Frobenius avoidance count")
    return {
        "r": r,
        "q": q,
        "N": q - 1,
        "a": a,
        "u": u,
        "total_orbit_count": len(orbits),
        "orbit_size_histogram": {
            str(size): count
            for size, count in sorted(Counter(map(len, orbits)).items())
        },
        "hit_orbit_count": len(hit),
        "avoiding_orbit_count": len(avoiding),
        "hit_frequency_count": a - e_value,
        "E_r_u": e_value,
        "kernel_dimension_upper_bound_over_F3": e_value,
        "ambient_F3_kernel_cardinality_upper_bound": 3**e_value,
        "sign_information_set_fiber_bound": 2**e_value,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def ternary_digits(value: int, width: int) -> tuple[int, ...]:
    digits = []
    for _ in range(width):
        digits.append(value % 3)
        value //= 3
    require(value == 0, "ternary word fits declared width")
    return tuple(digits)


def has_cyclic_zero_run(value: int, width: int, run: int) -> bool:
    require(1 <= run <= width, "legal cyclic zero-run length")
    digits = ternary_digits(value, width)
    return any(
        all(digits[(start + offset) % width] == 0 for offset in range(run))
        for start in range(width)
    )


def ternary_value(digits: tuple[int, ...]) -> int:
    value = 0
    place = 1
    for digit in digits:
        require(0 <= digit <= 2, "ternary digit")
        value += digit * place
        place *= 3
    return value


def swap_first_nonzero_ternary_digit(value: int, width: int) -> int:
    digits = list(ternary_digits(value, width))
    first = next(
        (index for index, digit in enumerate(digits) if digit),
        None,
    )
    require(first is not None, "parity involution excludes all-zero word")
    digits[first] = 3 - digits[first]
    return ternary_value(tuple(digits))


def least_odd_greater_than(u: int) -> int:
    return u + 1 if u % 2 == 0 else u + 2


def plotkin_bound(a: int, u: int) -> int | None:
    distance = least_odd_greater_than(u)
    if 2 * distance <= a:
        return None
    return (2 * distance) // (2 * distance - a)


def hamming_histogram(
    groups: dict[tuple[int, ...], list[int]], a: int, u: int
) -> Counter[int]:
    if u == 0:
        return Counter(
            {
                distance: 2 ** (a - 1) * math.comb(a, distance)
                for distance in range(1, a + 1)
            }
        )
    histogram: Counter[int] = Counter()
    for masks in groups.values():
        for left_index, left in enumerate(masks):
            for right in masks[left_index + 1 :]:
                histogram[(left ^ right).bit_count()] += 1
    return histogram


def finite_orientation_census(r: int) -> dict[str, Any]:
    field = GF3Extension(FINITE_FIELDS[r])
    q = field.q
    n = q - 1
    a = n // 2
    generator = field.primitive_element()
    require(field.pow(generator, n) == 1, "generator order divides N")
    require(
        all(
            field.pow(generator, n // factor) != 1
            for factor in prime_factors(n)
        ),
        "generator has exact order N",
    )
    minus_one = field.neg(1)
    require(field.pow(generator, a) == minus_one, "generator antipode")
    representatives = tuple(
        field.pow(generator, index) for index in range(a)
    )
    odd_frequencies = tuple(range(1, a - 1, 2))
    weights = {
        frequency: tuple(
            field.pow(generator, index * frequency)
            for index in range(a)
        )
        for frequency in odd_frequencies
    }

    records = []
    for mask in range(2**a):
        roots = tuple(
            representatives[index]
            if not (mask >> index) & 1
            else field.neg(representatives[index])
            for index in range(a)
        )
        locator = locator_polynomial(field, roots)
        require(
            len(locator) == a + 1 and locator[-1] == 1,
            "monic orientation locator",
        )
        prefix = tuple(
            locator[a - index] for index in range(1, a - 1)
        )
        fourier = []
        for frequency in odd_frequencies:
            total = 0
            for index, weight in enumerate(weights[frequency]):
                term = (
                    weight
                    if not (mask >> index) & 1
                    else field.neg(weight)
                )
                total = field.add(total, term)
            fourier.append(total)
        records.append((mask, prefix, tuple(fourier)))

    orbits = odd_frobenius_orbits(r)
    rows = []
    for u in range(a - 1):
        active_frequencies = tuple(
            value for value in odd_frequencies if value <= u
        )
        active_positions = tuple(
            odd_frequencies.index(value) for value in active_frequencies
        )
        groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
        prefix_to_fourier: dict[
            tuple[int, ...], tuple[int, ...]
        ] = {}
        refinement_consistent = True
        fourier_signatures = set()
        for mask, prefix, fourier in records:
            prefix_key = prefix[:u]
            signature = tuple(
                fourier[index] for index in active_positions
            )
            groups[prefix_key].append(mask)
            fourier_signatures.add(signature)
            previous = prefix_to_fourier.setdefault(
                prefix_key, signature
            )
            refinement_consistent &= previous == signature

        avoidance = avoidance_from_orbits(r, u, orbits)
        rank_matrix = []
        for frequency in active_frequencies:
            for coordinate in range(r):
                rank_matrix.append(
                    [
                        field.digits(weight)[coordinate]
                        for weight in weights[frequency]
                    ]
                )
        fourier_rank = matrix_rank_mod3(rank_matrix)
        kernel_basis = nullspace_basis_mod3(rank_matrix, a)
        information_positions = information_set_positions(
            kernel_basis, a
        )
        projected_basis = [
            [
                vector[position]
                for position in information_positions
            ]
            for vector in kernel_basis
        ]
        information_rank = matrix_rank_mod3(projected_basis)
        information_injective_on_fibers = all(
            len(
                {
                    tuple(
                        (mask >> position) & 1
                        for position in information_positions
                    )
                    for mask in masks
                }
            )
            == len(masks)
            for masks in groups.values()
        )
        fiber_sizes = Counter(map(len, groups.values()))
        maximum_fiber = max(map(len, groups.values()))
        distances = hamming_histogram(groups, a, u)
        pair_count = sum(distances.values())
        minimum_distance = min(distances) if distances else None
        distance_floor = least_odd_greater_than(u)
        p_bound = plotkin_bound(a, u)
        checks = {
            "all_orientations_censused": (
                sum(map(len, groups.values())) == 2**a
            ),
            "equal_prefix_implies_equal_active_fourier": (
                refinement_consistent
            ),
            "fourier_rank_matches_orbit_count": (
                fourier_rank == a - avoidance["E_r_u"]
            ),
            "nullspace_dimension_matches_E": (
                len(kernel_basis) == avoidance["E_r_u"]
            ),
            "information_set_has_full_direction_rank": (
                information_rank == len(kernel_basis)
                and len(information_positions) == len(kernel_basis)
            ),
            "all_prefix_fibers_injective_on_information_set": (
                information_injective_on_fibers
            ),
            "fiber_below_2_to_E_bound": (
                maximum_fiber
                <= avoidance["sign_information_set_fiber_bound"]
            ),
            "locator_factor_Hamming_floor": (
                minimum_distance is None
                or minimum_distance >= distance_floor
            ),
            "pair_histogram_mass": pair_count
            == sum(
                size * (size - 1) // 2 * count
                for size, count in fiber_sizes.items()
            ),
            "plotkin_gate_when_active": (
                p_bound is None or maximum_fiber <= p_bound
            ),
        }
        require(all(checks.values()), f"full F_{q} depth-{u} census")
        rows.append(
            {
                "u": u,
                "orientation_count": 2**a,
                "exact_prefix_image_size": len(groups),
                "exact_fourier_signature_image_size": (
                    len(fourier_signatures)
                ),
                "prefix_refines_fourier_partition": (
                    refinement_consistent
                ),
                "fiber_size_histogram": {
                    str(size): count
                    for size, count in sorted(fiber_sizes.items())
                },
                "maximum_prefix_fiber": maximum_fiber,
                "E_r_u": avoidance["E_r_u"],
                "fourier_constraint_rank_over_F3": fourier_rank,
                "E_dimension_upper_bound": avoidance["E_r_u"],
                "actual_F3_kernel_dimension": len(kernel_basis),
                "actual_F3_kernel_cardinality": 3 ** len(kernel_basis),
                "sign_information_set_fiber_bound": avoidance[
                    "sign_information_set_fiber_bound"
                ],
                "information_set_positions": list(
                    information_positions
                ),
                "information_set_dimension": len(kernel_basis),
                "within_fiber_pair_count": pair_count,
                "within_fiber_hamming_histogram": {
                    str(distance): count
                    for distance, count in sorted(distances.items())
                },
                "minimum_nonsingleton_hamming_distance": (
                    minimum_distance
                ),
                "proved_hamming_floor_d_u": distance_floor,
                "plotkin_bound_when_d_u_gt_a_over_2": p_bound,
                "checks": checks,
                "all_pass": all(checks.values()),
            }
        )

    checks = {
        "field_order": q == 3**r,
        "full_orientation_count": len(records) == 2**a,
        "all_legal_depths_censused": len(rows) == a - 1,
        "all_depth_rows_pass": all(row["all_pass"] for row in rows),
        "endpoint_present_without_exact_claim": (
            rows[-1]["u"] == a - 2
        ),
    }
    require(all(checks.values()), f"full F_{q} orientation census")
    return {
        "role": (
            "complete finite census only; exact finite image statistics "
            "are not promoted to a general exact-image theorem"
        ),
        "field_model": (
            "F_3[t]/"
            f"({list(field.modulus)}) in ascending coefficients"
        ),
        "r": r,
        "q": q,
        "N": n,
        "a": a,
        "primitive_element_encoding": generator,
        "orientation_count": 2**a,
        "depth_rows": rows,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def ceil_log3_ratio(q: int, denominator: int) -> tuple[int, int]:
    require(denominator > 0, "positive logarithm denominator")
    power = 1
    exponent = 0
    while power * denominator < q:
        power *= 3
        exponent += 1
    return exponent, power


def decimal_exp_product(
    q: int,
    numerator: int,
    denominator: int,
    precision: int,
    prefactor_denominator: int = 1,
) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        exponent = -Decimal(numerator) / Decimal(denominator)
        return +(
            Decimal(q)
            * exponent.exp()
            / Decimal(prefactor_denominator)
        )


def stable_exp_floor(
    q: int,
    numerator: int,
    denominator: int,
    prefactor_denominator: int = 1,
) -> tuple[int, str]:
    low = decimal_exp_product(
        q, numerator, denominator, 90, prefactor_denominator
    )
    high = decimal_exp_product(
        q, numerator, denominator, 140, prefactor_denominator
    )
    low_floor = int(low.to_integral_value(rounding=ROUND_FLOOR))
    high_floor = int(high.to_integral_value(rounding=ROUND_FLOOR))
    require(
        low_floor == high_floor,
        "Decimal exponential floor stable across precision",
    )
    return high_floor, format(high, ".36E")


def janson_row(
    r: int, u: int, exact_e: int | None
) -> dict[str, Any]:
    q = 3**r
    a = (q - 1) // 2
    require(0 <= u <= a - 2, "Janson row legal depth")
    ell, power = ceil_log3_ratio(q, u + 1)
    conditions = {
        "L_at_least_one": ell >= 1,
        "two_L_at_most_r": 2 * ell <= r,
        "ceil_log_upper": q <= power * (u + 1),
        "ceil_log_lower_strict": (
            ell >= 1 and (power // 3) * (u + 1) < q
        ),
    }
    require(all(conditions.values()), "Janson theorem conditions")
    raw_first_floor, raw_first_decimal = stable_exp_floor(
        q, r, 2 * power
    )
    raw_second_floor, raw_second_decimal = stable_exp_floor(
        q, r * (u + 1), 6 * q
    )
    first_floor, first_decimal = stable_exp_floor(
        q, r, 2 * power, 2
    )
    second_floor, second_decimal = stable_exp_floor(
        q, r * (u + 1), 6 * q, 2
    )
    rational_order = (u + 1) * power < 3 * q
    numeric_checks = {
        "rational_exponent_order": rational_order,
        "raw_first_upper_not_above_raw_second": (
            raw_first_floor <= raw_second_floor
        ),
        "halved_first_upper_not_above_halved_second": (
            first_floor <= second_floor
        ),
        "exact_E_below_parity_halved_first_upper_when_counted": (
            exact_e is None or exact_e <= first_floor
        ),
    }
    require(
        all(numeric_checks.values()),
        "Janson numeric/rational gates",
    )
    return {
        "r": r,
        "q": q,
        "a": a,
        "u": u,
        "L": ell,
        "three_to_L": power,
        "conditions": conditions,
        "exact_E_r_u": exact_e,
        "raw_zero_run_first_bound": {
            "formula": "q*exp(-r/(2*3^L))",
            "decimal_36_digits": raw_first_decimal,
            "floor": raw_first_floor,
        },
        "raw_zero_run_second_bound": {
            "formula": "q*exp(-r*(u+1)/(6q))",
            "decimal_36_digits": raw_second_decimal,
            "floor": raw_second_floor,
        },
        "first_bound": {
            "formula": "(q/2)*exp(-r/(2*3^L))",
            "decimal_36_digits": first_decimal,
            "floor": first_floor,
        },
        "second_bound": {
            "formula": "(q/2)*exp(-r*(u+1)/(6q))",
            "decimal_36_digits": second_decimal,
            "floor": second_floor,
        },
        "numeric_and_rational_checks": numeric_checks,
        "all_pass": (
            all(conditions.values()) and all(numeric_checks.values())
        ),
    }


def exact_janson_samples() -> dict[str, Any]:
    rows = []
    for r in EXACT_JANSON_R:
        q = 3**r
        a = (q - 1) // 2
        candidate_depths = {
            min(a - 2, max(1, ceil_div(2 * a, r))),
            min(a - 2, max(1, a // 2)),
        }
        orbits = odd_frobenius_orbits(r)
        for u in sorted(candidate_depths):
            ell, _ = ceil_log3_ratio(q, u + 1)
            if 2 * ell > r:
                continue
            avoidance = avoidance_from_orbits(r, u, orbits)
            row = janson_row(r, u, avoidance["E_r_u"])
            avoiding_frequencies = [
                frequency
                for orbit in orbits
                if min(orbit) > u
                for frequency in orbit
            ]
            zero_run_avoiders = [
                word
                for word in range(q)
                if not has_cyclic_zero_run(word, r, ell)
            ]
            avoider_set = set(zero_run_avoiders)
            partners = {
                word: swap_first_nonzero_ternary_digit(word, r)
                for word in zero_run_avoiders
            }
            odd_avoiders = {
                word for word in zero_run_avoiders if word % 2 == 1
            }
            even_avoiders = avoider_set - odd_avoiders
            odd_avoiding_frequencies = set(avoiding_frequencies)
            zero_run_avoidance_count = len(zero_run_avoiders)
            zero_run_checks = {
                "window_implies_power_scale": (
                    3 ** (r - ell) <= u + 1
                ),
                "all_zero_word_excluded": 0 not in avoider_set,
                "parity_map_preserves_avoider_set": (
                    set(partners.values()) == avoider_set
                ),
                "parity_map_is_involution": all(
                    partners[partners[word]] == word
                    for word in zero_run_avoiders
                ),
                "parity_map_flips_integer_parity": all(
                    (word - partner) % 2 == 1
                    for word, partner in partners.items()
                ),
                "parity_classes_exactly_halved": (
                    len(odd_avoiders)
                    == len(even_avoiders)
                    == zero_run_avoidance_count // 2
                    and zero_run_avoidance_count % 2 == 0
                ),
                "E_frequencies_are_odd": all(
                    frequency % 2 == 1
                    for frequency in odd_avoiding_frequencies
                ),
                "E_subset_of_odd_zero_run_avoiders": (
                    odd_avoiding_frequencies <= odd_avoiders
                ),
                "exact_E_not_above_odd_avoider_count": (
                    avoidance["E_r_u"] <= len(odd_avoiders)
                ),
                "exact_raw_avoider_count_below_Janson_upper": (
                    zero_run_avoidance_count
                    <= row["raw_zero_run_first_bound"]["floor"]
                ),
                "exact_odd_avoider_count_below_halved_Janson_upper": (
                    len(odd_avoiders) <= row["first_bound"]["floor"]
                ),
            }
            require(
                all(zero_run_checks.values()),
                "cyclic ternary zero-run/Janson sample",
            )
            row["cyclic_ternary_zero_run_ledger"] = {
                "run_length_L": ell,
                "exact_word_count_3_to_r": q,
                "exact_zero_run_avoidance_count": (
                    zero_run_avoidance_count
                ),
                "parity_involution": (
                    "swap the first nonzero ternary digit 1<->2"
                ),
                "exact_odd_avoidance_count": len(odd_avoiders),
                "exact_even_avoidance_count": len(even_avoiders),
                "E_subset_size": avoidance["E_r_u"],
                "checks": zero_run_checks,
                "all_pass": all(zero_run_checks.values()),
            }
            row["all_pass"] = (
                row["all_pass"] and all(zero_run_checks.values())
            )
            row["exact_avoidance_orbit_ledger"] = {
                key: avoidance[key]
                for key in (
                    "total_orbit_count",
                    "orbit_size_histogram",
                    "hit_orbit_count",
                    "avoiding_orbit_count",
                    "hit_frequency_count",
                    "E_r_u",
                )
            }
            rows.append(row)
    checks = {
        "all_rows_meet_Janson_conditions": all(
            row["all_pass"] for row in rows
        ),
        "every_sample_has_exact_avoidance_count": all(
            row["exact_E_r_u"] is not None for row in rows
        ),
        "cyclic_zero_run_implication_and_exact_counts": all(
            row["cyclic_ternary_zero_run_ledger"]["all_pass"]
            for row in rows
        ),
        "parity_halving_involution": all(
            row["cyclic_ternary_zero_run_ledger"]["checks"][
                "parity_classes_exactly_halved"
            ]
            and row["cyclic_ternary_zero_run_ledger"]["checks"][
                "parity_map_is_involution"
            ]
            for row in rows
        ),
        "multiple_safe_depths_sampled": (
            len(rows) >= len(EXACT_JANSON_R)
        ),
    }
    require(all(checks.values()), "exact Janson sample packet")
    return {
        "role": (
            "finite exact avoidance checks of the proved conditional "
            "bound; not an empirical replacement for the Janson proof"
        ),
        "rows": rows,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def supercritical_payload() -> dict[str, Any]:
    rows = []
    for r, target_t in SUPERCRITICAL_SAMPLES:
        q = 3**r
        a = (q - 1) // 2
        u = min(a - 2, ceil_div(target_t * a, r))
        row = janson_row(r, u, None)
        with localcontext() as context:
            context.prec = 80
            loose_ratio = (
                Decimal(q)
                * (
                    -Decimal(r * (u + 1))
                    / Decimal(6 * q)
                ).exp()
                / Decimal(2 * a)
            )
            log_fiber_ratio = loose_ratio * Decimal(2).ln()
        row.update(
            {
                "target_t": target_t,
                "actual_scale_ratio_r_times_u_over_a": (
                    f"{r * u}/{a}"
                ),
                "Janson_E_over_a_upper_decimal": format(
                    loose_ratio, ".30E"
                ),
                "log_fiber_over_a_upper_decimal": format(
                    log_fiber_ratio, ".30E"
                ),
                "interpretation": (
                    "illustrative theorem-bound row only; this finite "
                    "row is not asserted to have E=o(a)"
                ),
            }
        )
        rows.append(row)
    checks = {
        "target_scales_increase": [
            row["target_t"] for row in rows
        ]
        == sorted(row["target_t"] for row in rows),
        "all_rows_meet_conditional_gate": all(
            row["all_pass"] for row in rows
        ),
        "finite_rows_not_called_asymptotic_conclusions": all(
            "not asserted" in row["interpretation"] for row in rows
        ),
    }
    require(
        all(checks.values()),
        "supercritical theorem-bound samples",
    )
    return {
        "symbolic_implication": {
            "hypotheses": (
                "0<=u_r<=a_r-2 and r*u_r/a_r -> infinity"
            ),
            "eventual_Janson_condition": (
                "q/(u+1)=O(r/t_r), so L=O(log r) and "
                "2L<=r eventually"
            ),
            "avoidance_conclusion": (
                "E_(r,u)/a <= (q/(2a)) "
                "exp(-r(u+1)/(6q)) = o(1)"
            ),
            "fiber_conclusion": (
                "max_z |O_r intersect Phi_u^(-1)(z)| "
                "<= 2^E = exp(o(a))"
            ),
            "scope": (
                "upper bound only; neither an exact image size nor "
                "an exact endpoint multiplicity"
            ),
        },
        "sample_rows": rows,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def fixed_c_bracket_payload() -> dict[str, Any]:
    rows = []
    limit_rows = []
    for c in FIXED_C_VALUES:
        with localcontext() as context:
            context.prec = 100
            log_two = Decimal(2).ln()
            log_three = Decimal(3).ln()
            lower_limit = max(
                Decimal(0),
                log_two - Decimal(c) * log_three / Decimal(2),
            )
            upper_limit = (
                (-Decimal(c) / Decimal(12)).exp() * log_two
            )
        limit_rows.append(
            {
                "c": c,
                "lower_rate_limit": format(lower_limit, ".36E"),
                "upper_rate_limit": format(upper_limit, ".36E"),
                "limits_ordered": lower_limit <= upper_limit,
            }
        )
        for r in FIXED_C_SAMPLE_R:
            q = 3**r
            a = (q - 1) // 2
            u = c * a // r
            require(0 <= u <= a - 2, "fixed-c sample legal depth")
            janson = janson_row(r, u, None)
            with localcontext() as context:
                context.prec = 100
                log_two = Decimal(2).ln()
                log_three = Decimal(3).ln()
                finite_lower = max(
                    Decimal(0),
                    log_two
                    - (
                        Decimal(ceil_div(u, 2))
                        * Decimal(r)
                        * log_three
                        / Decimal(a)
                    ),
                )
                finite_upper = (
                    Decimal(q)
                    / Decimal(2 * a)
                    * (
                        -Decimal(r * (u + 1))
                        / Decimal(6 * q)
                    ).exp()
                    * log_two
                )
                scale = Decimal(r * u) / Decimal(a)
            row_checks = {
                "critical_depth_is_floor_c_a_over_r": (
                    u == c * a // r
                ),
                "legal_depth": 0 <= u <= a - 2,
                "Janson_conditions": janson["all_pass"],
                "finite_rate_bounds_ordered": (
                    finite_lower <= finite_upper
                ),
                "parity_halved_second_bound_present": (
                    janson["second_bound"]["formula"].startswith("(q/2)")
                ),
            }
            require(
                all(row_checks.values()),
                "fixed-c critical-window sample",
            )
            rows.append(
                {
                    "c": c,
                    "r": r,
                    "q": q,
                    "a": a,
                    "u_floor_c_a_over_r": u,
                    "c_times_a_mod_r": c * a % r,
                    "u_is_odd": u % 2 == 1,
                    "ceil_u_over_2": ceil_div(u, 2),
                    "actual_r_u_over_a_decimal": format(
                        scale, ".30E"
                    ),
                    "L": janson["L"],
                    "Janson_conditions": janson["conditions"],
                    "finite_normalized_lower_rate": format(
                        finite_lower, ".36E"
                    ),
                    "finite_normalized_upper_rate": format(
                        finite_upper, ".36E"
                    ),
                    "parity_halved_E_second_bound_floor": (
                        janson["second_bound"]["floor"]
                    ),
                    "checks": row_checks,
                    "all_pass": all(row_checks.values()),
                }
            )
    checks = {
        "all_fixed_c_rows_pass": all(row["all_pass"] for row in rows),
        "all_limit_brackets_ordered": all(
            row["limits_ordered"] for row in limit_rows
        ),
        "full_c_by_r_grid": len(rows)
        == len(FIXED_C_VALUES) * len(FIXED_C_SAMPLE_R),
        "positive_fixed_c_values": all(c > 0 for c in FIXED_C_VALUES),
        "floor_depth_rounding_exercised": any(
            row["c_times_a_mod_r"] != 0 for row in rows
        ),
        "ceil_half_rounding_exercised": any(
            row["u_is_odd"] for row in rows
        ),
        "both_roundings_with_positive_lower_rate_exercised": any(
            row["c_times_a_mod_r"] != 0
            and row["u_is_odd"]
            and Decimal(row["finite_normalized_lower_rate"]) > 0
            for row in rows
        ),
    }
    require(all(checks.values()), "fixed-c rate bracket packet")
    return {
        "statement": {
            "depth": "u_r=floor(c*a/r), fixed c>0",
            "maximum_fiber": (
                "M_r(u)=max_z |O_r intersect Phi_u^(-1)(z)|"
            ),
            "lower_rate": "max(0,log(2)-c*log(3)/2)",
            "upper_rate": "exp(-c/12)*log(2)",
            "bracket": (
                "lower_rate <= liminf log(M_r)/a <= "
                "limsup log(M_r)/a <= upper_rate"
            ),
            "lower_input": (
                "PR #634: M_r>=ceil(2^a/q^ceil(u_r/2))"
            ),
            "upper_input": (
                "2^|E| information-set bound plus the parity-halved "
                "(q/2) Janson estimate"
            ),
        },
        "limit_rows": limit_rows,
        "sample_rows": rows,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def high_depth_plotkin_payload(
    finite_censuses: list[dict[str, Any]],
) -> dict[str, Any]:
    rows = []
    for r in range(2, 9):
        q = 3**r
        a = (q - 1) // 2
        for label, u in (
            ("half-depth", min(a - 2, a // 2)),
            ("endpoint-depth", a - 2),
        ):
            distance = least_odd_greater_than(u)
            bound = plotkin_bound(a, u)
            require(
                2 * distance > a and bound is not None,
                "active Plotkin row",
            )
            rows.append(
                {
                    "label": label,
                    "r": r,
                    "q": q,
                    "a": a,
                    "u": u,
                    "d_u_least_odd_greater_than_u": distance,
                    "condition_2d_u_gt_a": 2 * distance > a,
                    "fiber_bound_floor_2d_over_2d_minus_a": (
                        bound
                    ),
                }
            )
    finite_rows = [
        row
        for census in finite_censuses
        for row in census["depth_rows"]
        if row["plotkin_bound_when_d_u_gt_a_over_2"] is not None
    ]
    endpoint_rows = [
        row for row in rows if row["label"] == "endpoint-depth"
    ]
    for row in endpoint_rows:
        row["endpoint_refined_upper_bound"] = 2
        row["endpoint_refinement_applicable"] = (
            row["a"] >= 4
            and row["d_u_least_odd_greater_than_u"] >= row["a"] - 1
            and row["a"] - 1 >= 3
        )
    checks = {
        "all_rows_have_active_Plotkin_denominator": all(
            row["condition_2d_u_gt_a"] for row in rows
        ),
        "finite_censuses_respect_Plotkin": all(
            row["maximum_prefix_fiber"]
            <= row["plotkin_bound_when_d_u_gt_a_over_2"]
            for row in finite_rows
        ),
        "raw_Plotkin_endpoint_bound_at_most_two_for_r_at_least_three": all(
            row["fiber_bound_floor_2d_over_2d_minus_a"] <= 2
            for row in endpoint_rows
            if row["r"] >= 3
        ),
        "F9_raw_Plotkin_exception_is_three": next(
            row for row in endpoint_rows if row["r"] == 2
        )["fiber_bound_floor_2d_over_2d_minus_a"] == 3,
        "separate_endpoint_refinement_is_two_for_all_rows": all(
            row["endpoint_refined_upper_bound"] == 2
            and row["endpoint_refinement_applicable"]
            for row in endpoint_rows
        ),
        "finite_endpoint_censuses_below_refined_bound": all(
            census["depth_rows"][-1]["maximum_prefix_fiber"] <= 2
            for census in finite_censuses
        ),
    }
    require(all(checks.values()), "high-depth Plotkin packet")
    return {
        "theorem": (
            "equal depth-u prefixes have binary Hamming distance "
            "at least d_u, the least odd integer greater than u; "
            "if d_u>a/2, Plotkin gives "
            "M<=floor(2d_u/(2d_u-a))"
        ),
        "endpoint_corollary": (
            "at u=a-2, translating one binary word to zero makes "
            "every other word have at most one zero; two such words "
            "would have distance at most 2<a-1, so every endpoint "
            "fiber has size at most 2, not necessarily exactly 2"
        ),
        "rows": rows,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def pin_tex_labels(root: Path) -> dict[str, Any]:
    text = (root / FRONTIERS_TEX).read_text(encoding="utf-8")
    lines = text.splitlines()
    pins: dict[str, Any] = {}
    for label, requirements in TEX_LABEL_REQUIREMENTS.items():
        pattern = re.compile(
            r"\\label(?:\[[^\]]*\])?\{"
            + re.escape(label)
            + r"\}"
        )
        matches = [
            index
            for index, line in enumerate(lines)
            if pattern.search(line)
        ]
        found_once = len(matches) == 1
        statement = ""
        environment = None
        line_number = None
        if found_once:
            index = matches[0]
            line_number = index + 1
            begin_pattern = re.compile(
                r"\\begin\{"
                r"(definition|theorem|corollary|proposition|lemma)"
                r"\}"
            )
            start = index
            while (
                start >= 0
                and not begin_pattern.search(lines[start])
            ):
                start -= 1
            if start >= 0:
                match = begin_pattern.search(lines[start])
                require(
                    match is not None,
                    f"environment parse for {label}",
                )
                environment = match.group(1)
                end = start
                marker = f"\\end{{{environment}}}"
                while end < len(lines) and marker not in lines[end]:
                    end += 1
                if end < len(lines):
                    statement = "\n".join(lines[start : end + 1])
        token_checks = {
            token: token in statement for token in requirements
        }
        pins[label] = {
            "found_once": found_once,
            "line": line_number,
            "environment": environment,
            "statement_sha256": (
                text_hash(statement) if statement else None
            ),
            "hypothesis_tokens": token_checks,
            "all_hypothesis_tokens_found": (
                bool(statement) and all(token_checks.values())
            ),
        }
    phase_marker_absent = (
        "orientation_prefix_phase_transition" not in text
    )
    return {
        "path": str(FRONTIERS_TEX),
        "file_sha256": text_hash(text),
        "labels": pins,
        "all_labels_found_and_audited": all(
            pin["found_once"]
            and pin["all_hypothesis_tokens_found"]
            for pin in pins.values()
        ),
        "phase_packet_marker_absent": phase_marker_absent,
        "no_phase_packet_promoted": phase_marker_absent,
    }


def pin_sources(root: Path) -> dict[str, Any]:
    pins = {}
    for relative, requirements in SOURCE_REQUIREMENTS.items():
        path = root / relative
        require(path.is_file(), f"required source exists: {relative}")
        text = path.read_text(encoding="utf-8")
        token_checks = {
            token: token in text for token in requirements
        }
        pins[str(relative)] = {
            "sha256": text_hash(text),
            "required_phrases": token_checks,
            "all_required_phrases_found": all(
                token_checks.values()
            ),
        }
    return {
        "files": pins,
        "all_sources_pinned": all(
            pin["all_required_phrases_found"]
            for pin in pins.values()
        ),
    }


def theorem_payload() -> dict[str, Any]:
    return {
        "parameters": "q=3^r, N=q-1=2a, 0<=u<=a-2",
        "avoidance_set": (
            "E_(r,u)={odd m in [1,N-1]: "
            "[3^j m]_N>u for every 0<=j<r}"
        ),
        "fourier_implication": (
            "equal locator prefixes imply that the ternary "
            "orientation-difference word has zero Fourier transform "
            "on every odd Frobenius orbit meeting [1,u]"
        ),
        "ambient_linear_container": (
            "the necessary Fourier constraints have an F3-linear "
            "direction space of dimension d<=|E_(r,u)|"
        ),
        "sign_information_set_fiber_bound": (
            "an injective d-coordinate information set maps the sign "
            "cube into {+1,-1}^d, so every fiber has size at most "
            "2^d<=2^|E_(r,u)|"
        ),
        "hamming_bound": (
            "distinct equal-prefix orientations have Hamming "
            "distance at least the least odd d_u>u"
        ),
        "Janson_bound": {
            "L": "ceil(log_3(q/(u+1)))",
            "conditions": "1<=L and 2L<=r",
            "parity_halving": (
                "first-nonzero-digit 1<->2 pairs labelled zero-run "
                "avoiders and leaves exactly half at odd frequencies"
            ),
            "first": (
                "|E_(r,u)|<=(q/2) exp(-r/(2*3^L))"
            ),
            "second": (
                "(q/2) exp(-r/(2*3^L))"
                "<=(q/2) exp(-r(u+1)/(6q))"
            ),
        },
        "fixed_c_rate_bracket": (
            "for u_r=floor(c*a/r), fixed c>0: "
            "max(0,log(2)-c*log(3)/2) <= liminf log(M_r)/a "
            "<= limsup log(M_r)/a <= exp(-c/12)*log(2)"
        ),
        "supercritical_corollary": (
            "if r*u_r/a_r tends to infinity, the conditional "
            "bound is eventually available and every "
            "orientation-prefix fiber is exp(o(a_r))"
        ),
        "supercritical_image_entropy": (
            "log|Phi_u(O_r)|=a*log(2)-o(a); this is asymptotic "
            "entropy, not an exact image formula"
        ),
    }


def scope_payload() -> dict[str, Any]:
    return {
        "base_commit": BASE_SHA,
        "pr_lineage_pins": [
            {
                "pr": 631,
                "role": (
                    "profilewise pigeonhole and z-dependent "
                    "fixed-prefix separating-pole transport"
                ),
            },
            {
                "pr": 634,
                "role": (
                    "antipodal general-depth lower floors and "
                    "critical-scale positive-exponent specialization"
                ),
            },
            {
                "pr": 636,
                "role": (
                    "qualitative C7 geography only; exact flatness, "
                    "Q_img=1, and G1 stress equalities are not consumed"
                ),
            },
        ],
        "scope": (
            "coarse phase bracket for the canonical antipodal O_r "
            "family over q=3^r; uniformity is only over z inside O_r, "
            "with no all-support, cross-prefix-line, exact C7-stress, "
            "augmented-atlas, or post-router conclusion"
        ),
        "promotion_gate": (
            "experimental packet only; hypotheses must be audited "
            "before any TeX promotion"
        ),
    }


def nonclaims_payload() -> list[str]:
    return [
        "No exact formula for the realized orientation-prefix image is claimed.",
        "The information-set bound 2^E is an upper bound, not an exact orientation-fiber count.",
        "No endpoint injectivity or exact endpoint multiplicity is claimed.",
        "The endpoint Plotkin statement is only an upper bound.",
        "The Janson estimate is used only under its printed 2L<=r condition.",
        "No uniform bound is claimed for complete all-support prefix fibers or any family beyond O_r.",
        "No Q_img=1 or exact G1=q^(u/2) stress equality is claimed.",
        "No single received line or pole is claimed to work across distinct prefixes z.",
        "No subexponential prefix-value or prefix-profile census is claimed.",
        "Finite supercritical rows illustrate theorem bounds; no finite number is called o(a).",
        "No fixed finite c is claimed to give subexponential fibers; that requires r*u/a->infinity.",
        "No arbitrary augmented-atlas, primitive-residual, or global hard-input conclusion is claimed.",
        "No statement is promoted into the frontiers TeX by this packet.",
    ]


def verification_payload() -> dict[str, Any]:
    stem = (
        "python3 experimental/scripts/"
        "verify_orientation_prefix_phase_transition.py"
    )
    return {
        "stdlib_only": True,
        "address_space_cap_bytes": ADDRESS_SPACE_CAP_BYTES,
        "data_dir_override_environment": "OPPT_DATA_DIR",
        "zero_argument_mode": "--check",
        "finite_full_censuses": ["F_9", "F_27"],
        "exact_Janson_sample_r": list(EXACT_JANSON_R),
        "semantic_tamper_mutations": 17,
        "artifact_path": str(ARTIFACT),
        "regeneration": stem + " --write",
        "check": stem + " --check",
        "tamper_selftest": stem + " --tamper-selftest",
    }


def top_level_checks(
    finite_censuses: list[dict[str, Any]],
    exact_janson: dict[str, Any],
    supercritical: dict[str, Any],
    fixed_c: dict[str, Any],
    plotkin: dict[str, Any],
    tex_pins: dict[str, Any],
    source_pins: dict[str, Any],
    scope: dict[str, Any],
    nonclaims: list[str],
) -> dict[str, bool]:
    return {
        "exact_GF9_full_census": finite_censuses[0]["all_pass"],
        "exact_GF27_full_census": finite_censuses[1]["all_pass"],
        "sign_cube_information_set_fiber_bound": all(
            row["checks"]["fiber_below_2_to_E_bound"]
            and row["checks"][
                "all_prefix_fibers_injective_on_information_set"
            ]
            for census in finite_censuses
            for row in census["depth_rows"]
        ),
        "equal_prefix_Fourier_implication": all(
            row["checks"][
                "equal_prefix_implies_equal_active_fourier"
            ]
            for census in finite_censuses
            for row in census["depth_rows"]
        ),
        "locator_factor_Hamming_floor": all(
            row["checks"]["locator_factor_Hamming_floor"]
            for census in finite_censuses
            for row in census["depth_rows"]
        ),
        "exact_avoidance_and_Janson_samples": (
            exact_janson["all_pass"]
        ),
        "parity_halved_Janson_gate": (
            exact_janson["checks"]["parity_halving_involution"]
        ),
        "conditional_supercritical_rows": (
            supercritical["all_pass"]
        ),
        "fixed_c_critical_window_rate_bracket": fixed_c["all_pass"],
        "high_depth_Plotkin": plotkin["all_pass"],
        "frontiers_hypotheses_pinned": (
            tex_pins["all_labels_found_and_audited"]
        ),
        "source_hypotheses_pinned": (
            source_pins["all_sources_pinned"]
        ),
        "no_TeX_promotion": tex_pins["no_phase_packet_promoted"],
        "no_exact_image_or_endpoint_claim": (
            any("No exact formula" in claim for claim in nonclaims)
            and any(
                "No endpoint injectivity" in claim
                for claim in nonclaims
            )
        ),
        "cyclic_zero_run_implication_and_exact_counts": (
            exact_janson["checks"][
                "cyclic_zero_run_implication_and_exact_counts"
            ]
        ),
        "PR_scope_631_634_636": [
            pin["pr"] for pin in scope["pr_lineage_pins"]
        ] == [631, 634, 636],
        "scope_boundary_nonclaims_live": all(
            any(token in claim for claim in nonclaims)
            for token in (
                "No uniform bound",
                "No Q_img=1",
                "No single received line",
                "No subexponential prefix-value",
                "No fixed finite c",
            )
        ),
    }


def build_payload() -> dict[str, Any]:
    root = repo_root()
    finite_censuses = [
        finite_orientation_census(r) for r in (2, 3)
    ]
    exact_janson = exact_janson_samples()
    supercritical = supercritical_payload()
    fixed_c = fixed_c_bracket_payload()
    plotkin = high_depth_plotkin_payload(finite_censuses)
    tex_pins = pin_tex_labels(root)
    source_pins = pin_sources(root)
    scope = scope_payload()
    nonclaims = nonclaims_payload()
    checks = top_level_checks(
        finite_censuses,
        exact_janson,
        supercritical,
        fixed_c,
        plotkin,
        tex_pins,
        source_pins,
        scope,
        nonclaims,
    )
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "object": (
            "orientation-prefix Fourier-avoidance phase transition"
        ),
        "status": STATUS,
        "verdict": (
            "PROVED_SPECIAL_COARSE_PHASE_BRACKET: equal-prefix Fourier "
            "constraints plus an information set give 2^|E|; parity "
            "halves the printed Janson bound to q/2, yielding the fixed-c "
            "CW bracket and the supercritical restricted-family upper side"
        ),
        "base_sha": BASE_SHA,
        "generated_by": (
            "experimental/scripts/"
            "verify_orientation_prefix_phase_transition.py"
        ),
        "theorem": theorem_payload(),
        "scope_and_pr_pins": scope,
        "frontiers_label_pins": tex_pins,
        "integrated_source_pins": source_pins,
        "finite_full_orientation_censuses": finite_censuses,
        "exact_avoidance_Janson_samples": exact_janson,
        "supercritical_theorem_bound_samples": supercritical,
        "fixed_c_critical_window_bracket": fixed_c,
        "high_depth_Plotkin": plotkin,
        "nonclaims": nonclaims,
        "verification": verification_payload(),
        "checks": checks,
        "all_pass": all(checks.values()),
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate_against(
    candidate: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    errors = []
    if candidate.get("payload_sha256") != payload_hash(candidate):
        errors.append(
            "payload_sha256 does not authenticate candidate payload"
        )
    if without_hash(candidate) != without_hash(expected):
        errors.append(
            "candidate payload differs from exact recomputation"
        )
    if not candidate.get("all_pass"):
        errors.append("all_pass is false")
    checks = candidate.get("checks")
    if (
        not isinstance(checks, dict)
        or not checks
        or not all(checks.values())
    ):
        errors.append("one or more top-level checks fail")
    return errors


def write_artifact(root: Path, effective_cap: int) -> int:
    payload = build_payload()
    if not payload["all_pass"]:
        print("RESULT: FAIL internal checks", file=sys.stderr)
        return 1
    path = root / ARTIFACT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {path}")
    print(f"payload_sha256: {payload['payload_sha256']}")
    print(f"RLIMIT_AS: {effective_cap} bytes")
    print(f"verdict: {payload['verdict']}")
    print("RESULT: PASS")
    return 0


def check_artifact(root: Path, effective_cap: int) -> int:
    path = root / ARTIFACT
    if not path.is_file():
        print(
            f"RESULT: FAIL missing artifact {path}",
            file=sys.stderr,
        )
        return 1
    candidate = json.loads(path.read_text(encoding="utf-8"))
    expected = build_payload()
    errors = validate_against(candidate, expected)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print("RESULT: FAIL", file=sys.stderr)
        return 1
    finite = candidate["finite_full_orientation_censuses"]
    print("orientation-prefix phase-transition artifact check passed")
    print(f"payload_sha256: {candidate['payload_sha256']}")
    print(
        "finite censuses: "
        + ", ".join(
            f"F_{row['q']}={row['orientation_count']} "
            f"orientations/{len(row['depth_rows'])} depths"
            for row in finite
        )
    )
    print(
        "exact Janson rows: "
        f"{len(candidate['exact_avoidance_Janson_samples']['rows'])}"
    )
    print(f"RLIMIT_AS: {effective_cap} bytes")
    print("RESULT: PASS")
    return 0


def tamper_selftest(effective_cap: int) -> int:
    expected = build_payload()

    def finite_prefix_image(x: dict[str, Any]) -> None:
        x["finite_full_orientation_censuses"][0][
            "depth_rows"
        ][1]["exact_prefix_image_size"] += 1

    def finite_fourier_rank(x: dict[str, Any]) -> None:
        x["finite_full_orientation_censuses"][1][
            "depth_rows"
        ][3]["fourier_constraint_rank_over_F3"] -= 1

    def finite_hamming(x: dict[str, Any]) -> None:
        x["finite_full_orientation_censuses"][1][
            "depth_rows"
        ][1]["proved_hamming_floor_d_u"] += 2

    def kernel_bound(x: dict[str, Any]) -> None:
        x["finite_full_orientation_censuses"][0][
            "depth_rows"
        ][0]["sign_information_set_fiber_bound"] -= 1

    def avoidance_count(x: dict[str, Any]) -> None:
        x["exact_avoidance_Janson_samples"]["rows"][0][
            "exact_E_r_u"
        ] += 1

    def janson_L(x: dict[str, Any]) -> None:
        x["exact_avoidance_Janson_samples"]["rows"][1][
            "L"
        ] += 1

    def janson_floor(x: dict[str, Any]) -> None:
        x["exact_avoidance_Janson_samples"]["rows"][2][
            "first_bound"
        ]["floor"] -= 1

    def parity_count(x: dict[str, Any]) -> None:
        x["exact_avoidance_Janson_samples"]["rows"][0][
            "cyclic_ternary_zero_run_ledger"
        ]["exact_odd_avoidance_count"] += 1

    def fixed_c_rate(x: dict[str, Any]) -> None:
        x["fixed_c_critical_window_bracket"]["limit_rows"][0][
            "upper_rate_limit"
        ] = "0"

    def fixed_c_rounding(x: dict[str, Any]) -> None:
        row = next(
            item
            for item in x["fixed_c_critical_window_bracket"]["sample_rows"]
            if item["c"] == 1 and item["r"] == 12
        )
        row["ceil_u_over_2"] -= 1

    def supercritical_depth(x: dict[str, Any]) -> None:
        x["supercritical_theorem_bound_samples"][
            "sample_rows"
        ][0]["u"] -= 1

    def plotkin_distance(x: dict[str, Any]) -> None:
        x["high_depth_Plotkin"]["rows"][0][
            "d_u_least_odd_greater_than_u"
        ] += 2

    def plotkin_scope(x: dict[str, Any]) -> None:
        x["high_depth_Plotkin"]["endpoint_corollary"] = (
            "endpoint fibers are exactly two"
        )

    def tex_pin(x: dict[str, Any]) -> None:
        x["frontiers_label_pins"]["labels"]["def:paid-cell"][
            "found_once"
        ] = False

    def source_pin(x: dict[str, Any]) -> None:
        first = next(
            iter(x["integrated_source_pins"]["files"].values())
        )
        first["sha256"] = "f" * 64

    def pr_scope(x: dict[str, Any]) -> None:
        x["scope_and_pr_pins"]["pr_lineage_pins"][0]["pr"] = 621

    def nonclaim(x: dict[str, Any]) -> None:
        x["nonclaims"].pop()

    mutations: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = [
        ("finite prefix image", finite_prefix_image),
        ("finite Fourier rank", finite_fourier_rank),
        ("finite Hamming floor", finite_hamming),
        ("kernel bound", kernel_bound),
        ("avoidance count", avoidance_count),
        ("Janson L", janson_L),
        ("Janson floor", janson_floor),
        ("parity-halved avoider count", parity_count),
        ("fixed-c upper rate", fixed_c_rate),
        ("fixed-c rounded lower exponent", fixed_c_rounding),
        ("supercritical depth", supercritical_depth),
        ("Plotkin distance", plotkin_distance),
        ("Plotkin endpoint scope", plotkin_scope),
        ("TeX hypothesis pin", tex_pin),
        ("source pin", source_pin),
        ("PR scope pin", pr_scope),
        ("nonclaim", nonclaim),
    ]
    accepted = []
    for name, mutate in mutations:
        bad = copy.deepcopy(expected)
        mutate(bad)
        bad["payload_sha256"] = payload_hash(bad)
        if not validate_against(bad, expected):
            accepted.append(name)
    if accepted:
        print(
            f"RESULT: FAIL undetected mutations: {accepted}",
            file=sys.stderr,
        )
        return 1
    print(
        f"tamper self-test rejected {len(mutations)} "
        "semantic mutations"
    )
    print(f"RLIMIT_AS: {effective_cap} bytes")
    print("RESULT: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--write", action="store_true", help="write exact JSON"
    )
    modes.add_argument(
        "--check", action="store_true", help="recompute/check JSON"
    )
    modes.add_argument(
        "--tamper-selftest",
        action="store_true",
        help=(
            "reject semantic mutations even after adversarial rehashing"
        ),
    )
    args = parser.parse_args(argv)
    effective_cap = impose_address_space_cap()
    root = repo_root()
    if args.write:
        return write_artifact(root, effective_cap)
    if args.tamper_selftest:
        return tamper_selftest(effective_cap)
    return check_artifact(root, effective_cap)


if __name__ == "__main__":
    raise SystemExit(main())
