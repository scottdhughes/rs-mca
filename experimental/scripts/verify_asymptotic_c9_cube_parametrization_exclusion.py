#!/usr/bin/env python3
"""Exact small checks for the endpoint full-cube exclusion packet."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations, product


class VerificationError(RuntimeError):
    """A check failed with enough context to reproduce it."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise VerificationError(f"no primitive root found modulo {prime}")


def endpoint_parameters(depth: int, endpoint: str) -> tuple[int, int]:
    if endpoint == "zero":
        return 0, depth
    if endpoint == "one":
        return 1, depth + 1
    if endpoint == "one-minus-r":
        return 1 - depth, depth
    if endpoint == "minus-r":
        return -depth, depth + 1
    raise VerificationError(f"unknown endpoint label: {endpoint}")


def endpoint_exponents(depth: int, shift: int, n: int) -> list[int]:
    exponents = {0}
    exponents.update((shift + offset) % n for offset in range(depth))
    return sorted(exponents)


def endpoint_matrix(
    n: int, prime: int, depth: int, shift: int
) -> list[list[int]]:
    require((prime - 1) % n == 0, f"N={n} does not divide p-1={prime - 1}")
    zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
    require(
        pow(zeta, n, prime) == 1
        and all(pow(zeta, k, prime) != 1 for k in range(1, n)),
        f"constructed zeta does not have exact order {n} modulo {prime}",
    )
    return [
        [pow(zeta, exponent * column, prime) for column in range(n)]
        for exponent in endpoint_exponents(depth, shift, n)
    ]


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [value * inverse % prime for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    size = len(matrix)
    require(
        all(len(row) == size for row in matrix),
        "determinant requested for a non-square matrix",
    )
    work = [[value % prime for value in row] for row in matrix]
    determinant = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % prime
            for entry in range(column, size):
                work[row][entry] = (
                    work[row][entry] - factor * work[column][entry]
                ) % prime
    return determinant % prime


def endpoint_fibers(
    n: int, prime: int, weight: int, depth: int, shift: int
) -> dict[tuple[int, ...], list[int]]:
    matrix = endpoint_matrix(n, prime, depth, shift)
    fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for support in combinations(range(n), weight):
        mask = sum(1 << index for index in support)
        syndrome = tuple(
            sum(row[index] for index in support) % prime for row in matrix
        )
        fibers[syndrome].append(mask)
    return fibers


def verify_endpoint_rows() -> tuple[int, int, int, int]:
    row_cases = 0
    minor_checks = 0
    support_subset_checks = 0
    pair_checks = 0
    endpoints = ("zero", "one", "one-minus-r", "minus-r")

    for n, prime in ((4, 5), (8, 17)):
        for depth in range(1, n // 2 + 1):
            for endpoint in endpoints:
                shift, distance_side = endpoint_parameters(depth, endpoint)
                matrix = endpoint_matrix(n, prime, depth, shift)
                require(
                    len(matrix) == distance_side,
                    f"wrong augmented row count for {(n, prime, depth, endpoint)}",
                )

                for columns in combinations(range(n), distance_side):
                    minor = [[row[column] for column in columns] for row in matrix]
                    require(
                        determinant_mod(minor, prime) != 0,
                        f"zero full-spark minor for row={(n, prime, depth, endpoint)}, "
                        f"columns={columns}",
                    )
                    minor_checks += 1

                for support_size in range(1, distance_side + 1):
                    for columns in combinations(range(n), support_size):
                        restricted = [
                            [row[column] for column in columns] for row in matrix
                        ]
                        require(
                            rank_mod(restricted, prime) == support_size,
                            "kernel vector can have forbidden support: "
                            f"row={(n, prime, depth, endpoint)}, columns={columns}",
                        )
                        support_subset_checks += 1

                for weight in range(1, n):
                    fibers = endpoint_fibers(
                        n, prime, weight, depth, shift
                    )
                    for syndrome, family in fibers.items():
                        for left, right in combinations(family, 2):
                            distance = (left ^ right).bit_count()
                            require(
                                distance >= 2 * distance_side,
                                "endpoint distance failure: "
                                f"row={(n, prime, depth, endpoint)}, weight={weight}, "
                                f"syndrome={syndrome}, masks={(left, right)}, "
                                f"distance={distance}, required={2 * distance_side}",
                            )
                            pair_checks += 1
                row_cases += 1

    require(pair_checks > 0, "small endpoint rows produced no colliding pairs")
    return row_cases, minor_checks, support_subset_checks, pair_checks


def f2_rank(vectors: list[int], dimension: int) -> int:
    basis = [0] * dimension
    rank = 0
    for original in vectors:
        value = original
        while value:
            pivot = value.bit_length() - 1
            if basis[pivot]:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                rank += 1
                break
    return rank


def anf_degree(values: list[int], dimension: int) -> int:
    coefficients = values[:]
    for bit in range(dimension):
        for mask in range(1 << dimension):
            if mask & (1 << bit):
                coefficients[mask] ^= coefficients[mask ^ (1 << bit)]
    return max(
        (mask.bit_count() for mask, value in enumerate(coefficients) if value),
        default=0,
    )


def walsh_vectors(
    outputs: tuple[int, ...], n: int, prime: int, dimension: int
) -> dict[int, tuple[int, ...]]:
    vectors: dict[int, tuple[int, ...]] = {}
    for mode in range(1, 1 << dimension):
        coefficients = []
        for coordinate in range(n):
            total = sum(
                (1 if (mode & point).bit_count() % 2 == 0 else -1)
                * ((outputs[point] >> coordinate) & 1)
                for point in range(1 << dimension)
            )
            coefficients.append(total % prime)
        vectors[mode] = tuple(coefficients)
    return vectors


def matrix_times_vector(
    matrix: list[list[int]], vector: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    return tuple(
        sum(left * right for left, right in zip(row, vector)) % prime
        for row in matrix
    )


def verify_one_cube_map(
    outputs: tuple[int, ...],
    n: int,
    prime: int,
    depth: int,
    shift: int,
    distance_side: int,
    dimension: int,
) -> tuple[bool, bool, int]:
    domain_size = 1 << dimension
    counts = Counter(outputs)

    directed_hamming = 0
    incidence = 0
    for coordinate in range(n):
        for bit in range(dimension):
            changes = sum(
                ((outputs[point] ^ outputs[point ^ (1 << bit)]) >> coordinate)
                & 1
                for point in range(domain_size)
            )
            directed_hamming += changes
            if changes:
                incidence += 1

    # Check 2D H(X) <= directed_hamming/domain exactly.  Since
    # H(X)=d-domain^(-1) sum_y n_y log_2(n_y), exponentiation gives the
    # integer comparison below.
    left_exponent = (
        2 * distance_side * domain_size * dimension - directed_hamming
    )
    right_integer = 1
    for count in counts.values():
        right_integer *= count ** (2 * distance_side * count)
    require(
        left_exponent <= 0 or (1 << left_exponent) <= right_integer,
        "entropy/influence lower bound failed: "
        f"d={dimension}, image={len(counts)}, "
        f"left_exponent={left_exponent}, right_integer={right_integer}",
    )
    require(
        directed_hamming <= incidence * domain_size,
        "influence/incidence upper bound failed: "
        f"d={dimension}, directed_hamming={directed_hamming}, "
        f"incidence={incidence}",
    )

    injective = len(counts) == domain_size
    if injective:
        require(
            2 * distance_side * dimension <= incidence,
            f"injective incidence bound failed for d={dimension}",
        )

    nonlinear = any(
        anf_degree(
            [((outputs[point] >> coordinate) & 1) for point in range(domain_size)],
            dimension,
        )
        >= 2
        for coordinate in range(n)
    )

    matrix = endpoint_matrix(n, prime, depth, shift)
    coefficients = walsh_vectors(outputs, n, prime, dimension)
    active_by_coordinate: list[list[int]] = [[] for _ in range(n)]
    active_modes: list[int] = []
    mode_checks = 0
    for mode, vector in coefficients.items():
        if not any(vector):
            continue
        require(
            matrix_times_vector(matrix, vector, prime) == (0,) * len(matrix),
            f"Walsh coefficient is outside endpoint kernel: mode={mode}, d={dimension}",
        )
        support_size = sum(value != 0 for value in vector)
        require(
            support_size >= distance_side + 1,
            "Walsh coefficient violates full-spark support: "
            f"mode={mode}, support={support_size}, required={distance_side + 1}",
        )
        active_modes.append(mode)
        for coordinate, value in enumerate(vector):
            if value:
                active_by_coordinate[coordinate].append(mode)
        mode_checks += 1

    global_rank = f2_rank(active_modes, dimension)
    local_ranks = [f2_rank(modes, dimension) for modes in active_by_coordinate]
    require(
        len(counts) <= 1 << global_rank,
        "Walsh quotient image bound failed: "
        f"image={len(counts)}, global_rank={global_rank}, d={dimension}",
    )

    selected_basis: list[int] = []
    for mode in active_modes:
        if f2_rank(selected_basis + [mode], dimension) > len(selected_basis):
            selected_basis.append(mode)
    require(
        len(selected_basis) == global_rank,
        f"failed to select active-mode basis in dimension {dimension}",
    )
    selected_support_sum = sum(
        sum(coefficients[mode][coordinate] != 0 for coordinate in range(n))
        for mode in selected_basis
    )
    require(
        (distance_side + 1) * global_rank <= selected_support_sum,
        f"basis support lower count failed in dimension {dimension}",
    )
    require(
        selected_support_sum <= sum(local_ranks),
        "local Walsh-rank double count failed: "
        f"selected_support={selected_support_sum}, local_rank_sum={sum(local_ranks)}",
    )
    require(
        len(counts) ** (distance_side + 1) <= 1 << sum(local_ranks),
        "Walsh image-rank inequality failed: "
        f"image={len(counts)}, local_rank_sum={sum(local_ranks)}",
    )
    return nonlinear, injective, mode_checks


def verify_cube_maps() -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
    int,
    int,
    int,
    int,
]:
    n, prime, weight, depth, shift = 8, 17, 4, 2, 0
    distance_side = 2
    fibers = endpoint_fibers(n, prime, weight, depth, shift)
    syndrome, family = max(
        fibers.items(), key=lambda item: (len(item[1]), item[1], item[0])
    )
    require(
        len(family) >= 4,
        f"expected a nontrivial endpoint fiber of size at least four, got {len(family)}",
    )

    maps_checked = 0
    nonlinear_maps = 0
    injective_maps = 0
    mode_checks = 0
    alphabets = {
        2: tuple(family[:4]),
        3: tuple(family[:3]),
    }
    for dimension, alphabet in alphabets.items():
        alphabet_size = len(alphabet)
        for labels in product(range(alphabet_size), repeat=1 << dimension):
            outputs = tuple(alphabet[label] for label in labels)
            nonlinear, injective, checked_modes = verify_one_cube_map(
                outputs,
                n,
                prime,
                depth,
                shift,
                distance_side,
                dimension,
            )
            maps_checked += 1
            nonlinear_maps += int(nonlinear)
            injective_maps += int(injective)
            mode_checks += checked_modes

    require(nonlinear_maps > 0, "enumeration found no nonlinear cube maps")
    require(injective_maps > 0, "enumeration found no injective cube maps")
    return (
        syndrome,
        tuple(family),
        alphabets[2],
        alphabets[3],
        maps_checked,
        nonlinear_maps,
        injective_maps,
        mode_checks,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact checks")
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")

    rows, minors, supports, pairs = verify_endpoint_rows()
    (
        syndrome,
        family,
        alphabet_d2,
        alphabet_d3,
        maps,
        nonlinear,
        injective,
        modes,
    ) = verify_cube_maps()
    total = rows + minors + supports + pairs + maps + modes
    print(f"endpoint_row_cases={rows}")
    print(f"full_spark_minor_checks={minors}")
    print(f"kernel_support_subset_checks={supports}")
    print(f"within_fiber_pair_checks={pairs}")
    print(f"cube_source_syndrome={syndrome}")
    print(f"cube_source_fiber={[hex(mask) for mask in family]}")
    print(f"cube_d2_alphabet={[hex(mask) for mask in alphabet_d2]}")
    print(f"cube_d3_alphabet={[hex(mask) for mask in alphabet_d3]}")
    print(f"cube_maps_checked={maps}")
    print(f"nonlinear_cube_maps_checked={nonlinear}")
    print(f"injective_cube_maps_checked={injective}")
    print(f"walsh_kernel_mode_checks={modes}")
    print(f"RESULT: PASS (work_items={total})")


if __name__ == "__main__":
    main()
