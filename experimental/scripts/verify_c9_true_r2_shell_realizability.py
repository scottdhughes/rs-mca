#!/usr/bin/env python3
"""Verify the C9 convention repair and exact prefix-to-MCA realizations.

This packet has three deliberately separate conclusions:

* the integrated 152-support packet is an effective R=1 construction under
  the active exact-power-sum convention;
* its stored finite row has a stronger, full-slice R=1 prefix fiber with an
  exact base-field pole-line realization;
* a refined four-point block construction has complete true-R=2 Hamming-shell
  fibers and an exact locator-line realization with distinct slopes.

The final construction is over a separated arbitrary evaluation domain.  It
does not assert survival of the smooth/circle C1--C8 first-match routing.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Sequence


STATUS = "FIXED / AUDIT / OPEN GAP"
OLD_SCRIPT = Path("experimental/scripts/verify_sidon_direct_payment.py")
TRUE_R2_NOTE = Path("experimental/notes/audits/c9_r2_near_sidon_razor.md")
FRONTIERS = Path("experimental/asymptotic_rs_mca_frontiers.tex")
EXPECTED_OLD_SCRIPT_SHA256 = "2b4bb3e8c305cd64240194f25d24c8937b6f967149da81c04820c69a39dd17f0"
EXPECTED_TRUE_R2_NOTE_SHA256 = "2002746028b21cce2b65f2e498634c2e636ba96dd6d9d656a0d784a08e5bf33c"
EXPECTED_FRONTIERS_SHA256 = "0e3aa7b1ba79b1065439ae484f4cb989d80cabe18afb68ec63a6b21d1f3370fd"

OLD_K = 5
OLD_N = 20
OLD_M = 10
OLD_Q = 501
OLD_P = 505_020_040_141
SIGMA = math.log(4.0 / 3.0) / 8.0
TAU = 0.05


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime_64(n: int) -> bool:
    if n < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % prime == 0:
            return n == prime
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime_64(n: int) -> int:
    candidate = max(2, n + 1)
    if candidate > 2 and candidate % 2 == 0:
        candidate += 1
    while candidate < 2**64:
        if is_prime_64(candidate):
            return candidate
        candidate += 1 if candidate == 2 else 2
    raise ValueError("no 64-bit prime found")


def masks_of_weight(n: int, weight: int) -> Iterable[int]:
    for positions in itertools.combinations(range(n), weight):
        mask = 0
        for position in positions:
            mask |= 1 << position
        yield mask


def selected(mask: int, values: Sequence[int]) -> list[int]:
    return [value for index, value in enumerate(values) if (mask >> index) & 1]


def power_sum(mask: int, values: Sequence[int], exponent: int) -> int:
    return sum(value**exponent for value in selected(mask, values))


def elementary_123(items: Sequence[int]) -> tuple[int, int, int]:
    e1 = sum(items)
    e2 = sum(items[i] * items[j] for i in range(len(items)) for j in range(i + 1, len(items)))
    e3 = sum(
        items[i] * items[j] * items[k]
        for i in range(len(items))
        for j in range(i + 1, len(items))
        for k in range(j + 1, len(items))
    )
    return e1, e2, e3


def additive_energy(masks: Sequence[int], n: int) -> int:
    full = (1 << n) - 1
    differences: Counter[tuple[int, int]] = Counter()
    for left in masks:
        for right in masks:
            differences[(left & (~right & full), right & (~left & full))] += 1
    return sum(count * count for count in differences.values())


def poly_mul(left: Sequence[int], right: Sequence[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def poly_pow(poly: Sequence[int], exponent: int) -> list[int]:
    result = [1]
    for _ in range(exponent):
        result = poly_mul(result, poly)
    return result


def rational_matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    matrix = [[Fraction(value, 1) for value in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    column = 0
    while rank < len(matrix) and column < len(matrix[0]):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            column += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        column += 1
    return rank


def locator(items: Sequence[int]) -> list[int]:
    """Ascending coefficients of prod(X-t)."""
    result = [1]
    for item in items:
        result = poly_mul(result, [-item, 1])
    return result


def convention_audit(root: Path) -> dict[str, Any]:
    script = (root / OLD_SCRIPT).read_text(encoding="utf-8")
    true_r2_note = (root / TRUE_R2_NOTE).read_text(encoding="utf-8")
    tex = (root / FRONTIERS).read_text(encoding="utf-8")
    old_script_sha256 = sha256(root / OLD_SCRIPT)
    true_r2_note_sha256 = sha256(root / TRUE_R2_NOTE)
    frontiers_sha256 = sha256(root / FRONTIERS)
    checks = {
        "old_script_sha256_pin": old_script_sha256 == EXPECTED_OLD_SCRIPT_SHA256,
        "existing_true_R2_note_sha256_pin": true_r2_note_sha256 == EXPECTED_TRUE_R2_NOTE_SHA256,
        "frontiers_sha256_pin": frontiers_sha256 == EXPECTED_FRONTIERS_SHA256,
        "old_declares_R_2": bool(re.search(r"^R\s*=\s*2\s*$", script, re.MULTILINE)),
        "old_map_is_weight_and_p1": "return mask.bit_count(), support_sum(mask, points) % prime" in script,
        "old_checks_fixed_weight": '"all_fixed_weight"' in script,
        "frontiers_exact_map_p1_through_pR": r"\Phi(x)=\sum_{t\in T}x_t(t,t^2,\ldots,t^R)" in tex,
        "frontiers_R_independent_prefix_equations": "The number \\(R\\) is the number of independent prefix" in tex,
        "frontiers_full_slice_normalization": "The normalization is taken from the full profile slice" in tex,
        "frontiers_exact_ray_realization": r"\label{cor:exact-prefix-ray-realization}" in tex,
        "frontiers_primitive_residual": r"\label{def:primitive-first-match-residual}" in tex,
        "frontiers_balanced_core_catalogue": "Balanced-core and split-pencil cells" in tex,
        "existing_true_R2_replacement": "Exact two-moment counterexample to the unrestricted R=2 razor" in true_r2_note,
    }
    require(all(checks.values()), f"convention pin failed: {checks}")
    return {
        "checks": checks,
        "old_script_sha256": old_script_sha256,
        "existing_true_R2_note_sha256": true_r2_note_sha256,
        "frontiers_sha256": frontiers_sha256,
        "verdict": "old packet has effective R=1, not active-convention R=2",
    }


def old_points() -> list[int]:
    return [OLD_Q**block + offset for block in range(OLD_K) for offset in range(4)]


def old_heavy_mask(bits: Sequence[int]) -> int:
    mask = 0
    for block, bit in enumerate(bits):
        for offset in ((0, 3) if bit == 0 else (1, 2)):
            mask |= 1 << (4 * block + offset)
    return mask


def balanced_words(k: int) -> Iterable[tuple[int, ...]]:
    require(k > 0 and k % 5 == 0, "balanced word length must be a positive multiple of five")
    multiset = []
    for digit in range(5):
        multiset.extend([digit] * (k // 5))
    yield from set(itertools.permutations(multiset))


def old_prefix_mask(word: Sequence[int]) -> int:
    mask = 0
    for block, count in enumerate(word):
        for offset in range(count):
            mask |= 1 << (4 * block + offset)
    return mask


def old_sample_true_r2() -> dict[str, Any]:
    points = old_points()
    heavy = [old_heavy_mask(bits) for bits in itertools.product((0, 1), repeat=OLD_K)]
    fillers = [old_prefix_mask(word) for word in balanced_words(OLD_K)]
    omega = heavy + fillers
    require(len(omega) == len(set(omega)) == 152, "old sampled residual mass mismatch")
    fibers: dict[tuple[int, int], list[int]] = defaultdict(list)
    for mask in omega:
        fibers[
            (
                power_sum(mask, points, 1) % OLD_P,
                power_sum(mask, points, 2) % OLD_P,
            )
        ].append(mask)
    histogram = Counter(map(len, fibers.values()))
    require(histogram == Counter({1: 122, 5: 2, 10: 2}), "old sampled true-R2 histogram mismatch")
    M = len(omega)
    L = len(fibers)
    bar = Fraction(M, L)
    q = 3
    cutoff = math.exp(-SIGMA * OLD_N)
    total = Fraction(0, 1)
    low_rows = []
    for members in fibers.values():
        energy = additive_energy(members, OLD_N)
        delta = Fraction(energy, len(members) ** 3)
        if float(delta) <= cutoff:
            total += (Fraction(len(members), 1) / bar) ** q
            low_rows.append((len(members), energy, delta))
    gsid = total / L
    rate = math.log(float(gsid)) / (OLD_N * q)
    require(gsid == Fraction(4_465_125, 438_976), "old sampled true-R2 Gsid mismatch")
    require(rate < TAU, "old sampled true-R2 row unexpectedly crosses tau")
    return {
        "M": M,
        "L": L,
        "barN": [bar.numerator, bar.denominator],
        "fiber_histogram": {str(size): count for size, count in sorted(histogram.items())},
        "low_energy_rows": [
            {"size": size, "energy": energy, "delta": [delta.numerator, delta.denominator]}
            for size, energy, delta in sorted(low_rows)
        ],
        "q": q,
        "Gsid": [gsid.numerator, gsid.denominator],
        "normalized_log": rate,
        "tau": TAU,
        "finite_gate_fails": False,
    }


def old_full_r1() -> dict[str, Any]:
    points = old_points()
    require(len(set(points)) == OLD_N, "old points are not distinct")
    require(is_prime_64(OLD_P), "stored modulus is not prime")
    require(OLD_P > sum(points), "stored modulus does not give p1 no-wrap")
    fibers: dict[int, list[int]] = defaultdict(list)
    products: dict[int, int] = {}
    for mask in masks_of_weight(OLD_N, OLD_M):
        items = selected(mask, points)
        p1 = sum(items) % OLD_P
        fibers[p1].append(mask)
        products[mask] = math.prod(items) % OLD_P

    heavy = [old_heavy_mask(bits) for bits in itertools.product((0, 1), repeat=OLD_K)]
    target_values = {power_sum(mask, points, 1) % OLD_P for mask in heavy}
    require(len(target_values) == 1, "heavy supports do not share p1")
    target = next(iter(target_values))
    fiber = fibers[target]
    expected_local = [0, 1, 1, 2, 1, 1]  # pair-offset sums 0..5
    local_poly = [0] * 6
    for pair in itertools.combinations(range(4), 2):
        local_poly[sum(pair)] += 1
    require(local_poly == expected_local, "local pair-sum polynomial mismatch")
    expected_fiber = poly_pow(local_poly, OLD_K)[3 * OLD_K]
    require(expected_fiber == len(fiber) == 1052, "full p1 fiber size mismatch")

    composition_ok = True
    for mask in fiber:
        block_counts = []
        offset_total = 0
        for block in range(OLD_K):
            offsets = [offset for offset in range(4) if (mask >> (4 * block + offset)) & 1]
            block_counts.append(len(offsets))
            offset_total += sum(offsets)
        composition_ok &= block_counts == [2] * OLD_K and offset_total == 3 * OLD_K
    require(composition_ok, "target p1 fiber does not have the certified block composition")

    slopes = [(-products[mask]) % OLD_P for mask in fiber]
    require(len(set(slopes)) == len(fiber), "alpha=0 pole does not separate the full p1 fiber")
    energy = additive_energy(fiber, OLD_N)
    delta = Fraction(energy, len(fiber) ** 3)
    cutoff = math.exp(-SIGMA * OLD_N)
    require(float(delta) <= cutoff, "full R1 fiber is not below the fixed energy cutoff")
    M = math.comb(OLD_N, OLD_M)
    L = len(fibers)
    bar = Fraction(M, L)
    stored_heavy_size = 32
    stored_heavy_energy = 7776
    stored_heavy_delta = Fraction(stored_heavy_energy, stored_heavy_size**3)
    require(float(stored_heavy_delta) <= cutoff, "stored heavy fiber misses cutoff")
    stored_q = 3
    stored_current_gsid = (
        (Fraction(stored_heavy_size, 1) / bar) ** stored_q / L
    )
    stored_current_rate = math.log(float(stored_current_gsid)) / (OLD_N * stored_q)
    require(
        stored_current_gsid == Fraction(10_280_632_832, 98_540_708_249_269),
        "stored residual full-slice-normalization moment mismatch",
    )
    require(stored_current_rate < 0.0, "stored residual still has positive full-slice-normalized rate")
    q = 4
    contribution = (Fraction(len(fiber), 1) / bar) ** q / L
    rate = math.log(float(contribution)) / (OLD_N * q)
    require(rate > TAU, "full-slice R1 lower moment does not cross tau")

    # U=X^10-e1 X^9, r0=U/X, r1=-1/X.  For gamma=-Q_S(0),
    # H_S=(U-Q_S-gamma)/X has degree <=7 and exact agreement S.
    e1 = target
    pole_checks = []
    for mask in fiber:
        items = selected(mask, points)
        q_poly = locator(items)
        gamma = (-q_poly[0]) % OLD_P
        u_poly = [0] * 11
        u_poly[9] = -e1
        u_poly[10] = 1
        numerator = [u_poly[i] - q_poly[i] for i in range(11)]
        numerator[0] -= gamma if gamma <= OLD_P // 2 else gamma - OLD_P
        # Divisibility is checked modulo p because gamma is a field element.
        divisible = numerator[0] % OLD_P == 0
        quotient_degree = max((i - 1 for i in range(1, 11) if numerator[i] % OLD_P), default=-1)
        exact_roots = all(
            (math.prod((x - t) % OLD_P for t in items) % OLD_P == 0) == (x in items)
            for x in points
        )
        pole_checks.append(divisible and quotient_degree <= 7 and exact_roots)
    require(all(pole_checks), "pole-line algebra failed")

    return {
        "parameters": {"N": OLD_N, "m": OLD_M, "R_effective": 1, "p": OLD_P},
        "full_slice": {"M": M, "L": L, "barN": [bar.numerator, bar.denominator]},
        "target": target,
        "fiber_size": len(fiber),
        "energy": energy,
        "delta": [delta.numerator, delta.denominator],
        "cutoff": cutoff,
        "pole_alpha": 0,
        "distinct_bad_slopes": len(set(slopes)),
        "code_dimension": 8,
        "q": q,
        "one_fiber_Gsid_lower": [contribution.numerator, contribution.denominator],
        "normalized_log_lower": rate,
        "tau": TAU,
        "stored_152_residual_under_current_full_slice_normalization": {
            "heavy_fiber_size": stored_heavy_size,
            "heavy_over_barN": float(Fraction(stored_heavy_size, 1) / bar),
            "q": stored_q,
            "Gsid": [stored_current_gsid.numerator, stored_current_gsid.denominator],
            "normalized_log": stored_current_rate,
            "finite_gate_fails": False,
        },
        "passes": True,
    }


def old_residual_current_full_slice_asymptotic() -> dict[str, Any]:
    rows = []
    for k in (5, 10, 20, 40, 80, 160):
        q = max(2, math.ceil(math.log(4 * k)))
        log_max_ratio_upper = (
            math.log(4 * k + 1)
            + math.log(6 * k + 1)
            + k * math.log(5.0 / 8.0)
        )
        log_residual_mass_ratio_upper = (
            math.log(2.0)
            + math.log(4 * k + 1)
            + k * math.log(5.0 / 16.0)
        )
        log_moment_upper = (
            log_residual_mass_ratio_upper + (q - 1) * log_max_ratio_upper
        )
        rows.append(
            {
                "k": k,
                "q": q,
                "log_max_fiber_over_barN_upper": log_max_ratio_upper,
                "log_ordinary_moment_upper": log_moment_upper,
                "normalized_log_moment_upper": log_moment_upper / (4 * k * q),
            }
        )
    require(rows[-1]["log_max_fiber_over_barN_upper"] < 0.0, "old residual Q bound does not decay")
    require(rows[-1]["normalized_log_moment_upper"] < 0.0, "old residual moment bound does not decay")
    return {
        "bounds": {
            "M_full_lower": "16^k/(4k+1)",
            "L_full_upper": "(6k+1)5^k",
            "residual_mass_upper": "2*5^k",
            "residual_max_fiber": "2^k",
            "max_fiber_over_barN_upper": "(4k+1)(6k+1)(5/8)^k",
        },
        "rows": rows,
        "verdict": (
            "stored residual satisfies the current-frontiers full-slice image-normalized "
            "max-fiber and ordinary-moment bounds asymptotically; primitive-leaf "
            "applicability is not asserted"
        ),
    }


def first_odd_exponent_above(bound: int, base: int = 16) -> int:
    exponent = 1
    while base**exponent <= bound:
        exponent += 2
    return exponent


def refined_points(k: int) -> tuple[int, int, list[int]]:
    base = 16
    d0 = first_odd_exponent_above(14 * k, base)
    centers = [base ** (d0 + 2 * block) for block in range(k)]
    points = [center + offset for center in centers for offset in range(4)]
    return base, d0, points


def shell_masks(k: int, h: int) -> list[int]:
    masks = []
    for inner_blocks in itertools.combinations(range(k), h):
        inner = set(inner_blocks)
        mask = 0
        for block in range(k):
            for offset in ((1, 2) if block in inner else (0, 3)):
                mask |= 1 << (4 * block + offset)
        masks.append(mask)
    return masks


def full_image_formula(k: int) -> tuple[int, int]:
    F = [1, 4, 5, 4, 1]
    fk = poly_pow(F, k)
    fkm1 = poly_pow(F, k - 1)
    L = fk[2 * k] + k * fkm1[2 * k - 2]
    return math.comb(4 * k, 2 * k), L


def shell_energy_formula(k: int, h: int) -> int:
    return sum(
        math.comb(k, d)
        * math.comb(k - d, d)
        * math.comb(k - 2 * d, h - d) ** 2
        for d in range(min(h, k - h) + 1)
    )


def refined_exhaustive_row(k: int) -> dict[str, Any]:
    base, d0, points = refined_points(k)
    n = 4 * k
    m = 2 * k
    signatures: dict[tuple[int, int], list[int]] = defaultdict(list)
    for mask in masks_of_weight(n, m):
        items = selected(mask, points)
        signatures[(sum(items), sum(item * item for item in items))].append(mask)
    M, L_formula = full_image_formula(k)
    require(len(signatures) == L_formula, f"true-R2 image formula failed at k={k}")
    require(sum(map(len, signatures.values())) == M, f"true-R2 mass failed at k={k}")

    shell_rows = []
    for h in range(k + 1):
        shell = shell_masks(k, h)
        labels = {
            (power_sum(mask, points, 1), power_sum(mask, points, 2)) for mask in shell
        }
        require(len(labels) == 1, f"shell is not a true-R2 fiber at k={k}, h={h}")
        label = next(iter(labels))
        require(set(signatures[label]) == set(shell), f"shell is not a complete fiber at k={k}, h={h}")
        e_values = [elementary_123(selected(mask, points))[2] for mask in shell]
        require(len(set(e_values)) == len(shell), f"e3 does not separate shell at k={k}, h={h}")
        energy = additive_energy(shell, n)
        require(energy == shell_energy_formula(k, h), f"energy formula failed at k={k}, h={h}")
        shell_rows.append({"h": h, "size": len(shell), "energy": energy, "distinct_e3": len(set(e_values))})

    central_shell = shell_masks(k, k // 2)
    central_locators = [locator(selected(mask, points)) for mask in central_shell]
    affine_rows = [
        [coefficient - base_coefficient for coefficient, base_coefficient in zip(poly, central_locators[0])]
        for poly in central_locators[1:]
    ]
    affine_rank = rational_matrix_rank(affine_rows)
    if k >= 3:
        require(affine_rank > 1, f"central true-R2 shell has rational affine rank one at k={k}")

    return {
        "k": k,
        "N": n,
        "m": m,
        "base": base,
        "d0": d0,
        "M": M,
        "L": len(signatures),
        "central_locator_affine_rank_over_Q": affine_rank,
        "shells": shell_rows,
    }


def refined_base_field_lift() -> dict[str, Any]:
    k = 2
    _, _, points = refined_points(k)
    bound = sum(item**3 for item in points)
    require(bound < 2**64 - 1000, "sample no-wrap bound is not 64-bit")
    prime = next_prime_64(bound)
    require(prime > bound and is_prime_64(prime), "sample prime certificate failed")
    shell = shell_masks(k, 1)
    a = 2 * k
    dimension = a - 3
    e_rows = [elementary_123(selected(mask, points)) for mask in shell]
    require(len({row[:2] for row in e_rows}) == 1, "sample lift lacks common e1,e2")
    require(len({row[2] % prime for row in e_rows}) == len(shell), "sample lift slopes collide")
    e1, e2 = e_rows[0][:2]
    algebra = []
    for mask, (_, _, e3) in zip(shell, e_rows):
        q_poly = locator(selected(mask, points))
        u_gamma = [0] * (a + 1)
        u_gamma[a] = 1
        u_gamma[a - 1] = -e1
        u_gamma[a - 2] = e2
        u_gamma[a - 3] = -e3
        difference = [u_gamma[i] - q_poly[i] for i in range(a + 1)]
        degree = max((i for i, coefficient in enumerate(difference) if coefficient), default=-1)
        exact_roots = all(
            (math.prod((x - t) % prime for t in selected(mask, points)) % prime == 0)
            == (x in selected(mask, points))
            for x in points
        )
        algebra.append(degree <= a - 4 and exact_roots)
    require(all(algebra), "sample exact locator-line lift failed")
    return {
        "k": k,
        "prime": prime,
        "no_wrap_cube_sum": bound,
        "agreement": a,
        "code_dimension": dimension,
        "distinct_bad_slopes": len(shell),
        "retained_support_occupancy": 1,
        "passes": True,
    }


def asymptotic_rows() -> dict[str, Any]:
    samples = []
    for k in (12, 24, 48, 96, 192, 384):
        h = k // 2
        M, L = full_image_formula(k)
        bar = Fraction(M, L)
        f = math.comb(k, h)
        energy = shell_energy_formula(k, h)
        delta = Fraction(energy, f**3)
        q = max(2, math.ceil(math.log(4 * k)))
        log_lower = q * (math.log(f) - (math.log(M) - math.log(L))) - math.log(L)
        rate = log_lower / (4 * k * q)
        samples.append(
            {
                "k": k,
                "q": q,
                "log_barN_over_k": (math.log(M) - math.log(L)) / k,
                "log_delta_over_k": (math.log(energy) - 3 * math.log(f)) / k,
                "normalized_log_Gsid_lower": rate,
                "below_sigma_cut": math.log(energy) - 3 * math.log(f) <= -SIGMA * 4 * k,
            }
        )
    require(all(row["below_sigma_cut"] for row in samples), "central shell misses cutoff")
    require(samples[-1]["normalized_log_Gsid_lower"] > TAU, "logarithmic-q sample misses tau")
    limit = math.log(15.0 / 8.0) / 4.0
    require(limit > TAU, "asymptotic rate does not cross tau")
    return {
        "samples": samples,
        "limits": {
            "log_M_over_k": math.log(16.0),
            "log_L_over_k": math.log(15.0),
            "log_barN_over_k": math.log(16.0 / 15.0),
            "log_f_over_k": math.log(2.0),
            "log_energy_over_k": math.log(6.0),
            "log_delta_over_k": math.log(3.0 / 4.0),
            "normalized_log_Gsid_lower": limit,
        },
        "moment_accessibility": "q_k=ceil(log(4k)) gives log L_k/q_k=o(N_k)",
    }


def build_report(root: Path) -> dict[str, Any]:
    report = {
        "schema": "c9-true-r2-shell-realizability-v1",
        "status": STATUS,
        "convention": convention_audit(root),
        "old_sample_true_R2": old_sample_true_r2(),
        "full_R1_finite": old_full_r1(),
        "old_residual_current_full_slice_asymptotic": old_residual_current_full_slice_asymptotic(),
        "true_R2_exhaustive": [refined_exhaustive_row(k) for k in range(2, 6)],
        "true_R2_base_field_lift": refined_base_field_lift(),
        "true_R2_asymptotic": asymptotic_rows(),
        "scope": {
            "proved": [
                "current-frontiers R counts nonconstant p1 through pR coordinates",
                "corrected full-slice finite R1 fiber and exact MCA line",
                "complete true-R2 shell fibers and exact arbitrary-domain MCA line",
            ],
            "open": [
                "survival after the smooth/circle C1-C8 first-match atlas",
                (
                    "whether the raw product family yields a post-factor "
                    "higher-dimensional balanced-core chart, and any resulting payment"
                ),
                "any deployed-row or target-threshold consequence",
            ],
        },
    }
    validate_report(report)
    payload = json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False)
    report["payload_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return report


def validate_report(report: dict[str, Any]) -> None:
    """Fail closed on every load-bearing certificate field."""
    require(report.get("schema") == "c9-true-r2-shell-realizability-v1", "schema mismatch")
    require(report.get("status") == STATUS, "status mismatch")

    convention = report["convention"]
    require(all(convention["checks"].values()), "a convention/source check is false")
    require(
        convention["old_script_sha256"] == EXPECTED_OLD_SCRIPT_SHA256,
        "old script digest mismatch",
    )
    require(
        convention["existing_true_R2_note_sha256"] == EXPECTED_TRUE_R2_NOTE_SHA256,
        "existing true-R2 note digest mismatch",
    )
    require(
        convention["frontiers_sha256"] == EXPECTED_FRONTIERS_SHA256,
        "frontiers digest mismatch",
    )
    require(
        convention["verdict"] == "old packet has effective R=1, not active-convention R=2",
        "convention verdict mismatch",
    )

    old_sample = report["old_sample_true_R2"]
    require(
        (old_sample["M"], old_sample["L"], old_sample["q"]) == (152, 126, 3),
        "old sample scales mismatch",
    )
    require(old_sample["Gsid"] == [4_465_125, 438_976], "old sample moment mismatch")
    require(
        old_sample["normalized_log"] < TAU and old_sample["finite_gate_fails"] is False,
        "old sample gate mismatch",
    )

    finite = report["full_R1_finite"]
    require(
        finite["parameters"] == {"N": 20, "m": 10, "R_effective": 1, "p": OLD_P},
        "finite parameters mismatch",
    )
    require(
        finite["full_slice"]
        == {"M": 184_756, "L": 4_481, "barN": [184_756, 4_481]},
        "finite full-slice scale mismatch",
    )
    require(
        (finite["fiber_size"], finite["energy"]) == (1_052, 19_726_716),
        "finite fiber certificate mismatch",
    )
    require(finite["delta"] == [4_931_679, 291_063_152], "finite energy ratio mismatch")
    require(
        (finite["distinct_bad_slopes"], finite["code_dimension"]) == (1_052, 8),
        "finite line certificate mismatch",
    )
    require(
        finite["one_fiber_Gsid_lower"]
        == [430_474_891_952_689_285_601, 4_551_496_773_325_485_841],
        "finite moment fraction mismatch",
    )
    require(
        finite["normalized_log_lower"] > TAU and finite["passes"] is True,
        "finite moment gate mismatch",
    )
    residual = finite["stored_152_residual_under_current_full_slice_normalization"]
    require(
        (residual["heavy_fiber_size"], residual["q"]) == (32, 3),
        "stored residual parameters mismatch",
    )
    require(
        residual["Gsid"] == [10_280_632_832, 98_540_708_249_269],
        "stored residual moment mismatch",
    )
    require(
        residual["normalized_log"] < 0.0 and residual["finite_gate_fails"] is False,
        "stored residual gate mismatch",
    )

    old_asymptotic = report["old_residual_current_full_slice_asymptotic"]
    require(len(old_asymptotic["rows"]) == 6, "old asymptotic row count mismatch")
    require(old_asymptotic["rows"][-1]["k"] == 160, "old asymptotic terminal row mismatch")
    require(
        old_asymptotic["rows"][-1]["log_max_fiber_over_barN_upper"] < 0.0,
        "old max-fiber bound mismatch",
    )
    require(
        old_asymptotic["rows"][-1]["normalized_log_moment_upper"] < 0.0,
        "old moment bound mismatch",
    )
    require(
        "primitive-leaf applicability is not asserted" in old_asymptotic["verdict"],
        "old asymptotic scope mismatch",
    )

    exhaustive = report["true_R2_exhaustive"]
    require([row["k"] for row in exhaustive] == [2, 3, 4, 5], "exhaustive k range mismatch")
    expected_ranks = {2: 1, 3: 2, 4: 5, 5: 8}
    for row in exhaustive:
        k = row["k"]
        expected_M, expected_L = full_image_formula(k)
        require(
            (row["N"], row["m"], row["M"], row["L"])
            == (4 * k, 2 * k, expected_M, expected_L),
            f"exhaustive scales mismatch at k={k}",
        )
        require(
            row["central_locator_affine_rank_over_Q"] == expected_ranks[k],
            f"rational rank mismatch at k={k}",
        )
        require(len(row["shells"]) == k + 1, f"shell count mismatch at k={k}")
        for shell in row["shells"]:
            h = shell["h"]
            size = math.comb(k, h)
            require(
                shell["size"] == shell["distinct_e3"] == size,
                f"shell size/separation mismatch at k={k}, h={h}",
            )
            require(
                shell["energy"] == shell_energy_formula(k, h),
                f"shell energy mismatch at k={k}, h={h}",
            )

    lift = report["true_R2_base_field_lift"]
    require(
        lift["k"] == 2 and lift["agreement"] == 4 and lift["code_dimension"] == 1,
        "field-lift parameters mismatch",
    )
    require(
        lift["prime"] == next_prime_64(lift["no_wrap_cube_sum"]),
        "field-lift prime mismatch",
    )
    require(
        lift["prime"] > lift["no_wrap_cube_sum"] and is_prime_64(lift["prime"]),
        "field-lift no-wrap mismatch",
    )
    require(
        lift["distinct_bad_slopes"] == 2 and lift["retained_support_occupancy"] == 1,
        "field-lift slope certificate mismatch",
    )
    require(lift["passes"] is True, "field-lift algebra mismatch")

    asymptotic = report["true_R2_asymptotic"]
    expected_limit = math.log(15.0 / 8.0) / 4.0
    require(
        math.isclose(
            asymptotic["limits"]["normalized_log_Gsid_lower"],
            expected_limit,
            rel_tol=0.0,
            abs_tol=1e-15,
        ),
        "asymptotic limit mismatch",
    )
    require(expected_limit > TAU, "asymptotic limit misses tau")
    require(len(asymptotic["samples"]) == 6, "asymptotic sample count mismatch")
    require(
        all(row["below_sigma_cut"] is True for row in asymptotic["samples"]),
        "asymptotic cutoff mismatch",
    )
    require(
        asymptotic["samples"][-1]["k"] == 384
        and asymptotic["samples"][-1]["normalized_log_Gsid_lower"] > TAU,
        "asymptotic terminal gate mismatch",
    )

    scope = report["scope"]
    require(any("C1-C8" in item for item in scope["open"]), "C1-C8 scope warning missing")
    require(
        any("deployed-row" in item for item in scope["open"]),
        "deployed-row nonclaim missing",
    )


def tamper_selftest(root: Path) -> None:
    report = build_report(root)
    mutations = [
        (
            "source digest",
            lambda item: item["convention"].__setitem__("frontiers_sha256", "0" * 64),
        ),
        ("old sample image", lambda item: item["old_sample_true_R2"].__setitem__("L", 127)),
        ("finite fiber", lambda item: item["full_R1_finite"].__setitem__("fiber_size", 1_053)),
        (
            "stored residual moment",
            lambda item: item["full_R1_finite"][
                "stored_152_residual_under_current_full_slice_normalization"
            ].__setitem__("Gsid", [1, 1]),
        ),
        (
            "true-R2 image",
            lambda item: item["true_R2_exhaustive"][-1].__setitem__(
                "L", item["true_R2_exhaustive"][-1]["L"] + 1
            ),
        ),
        (
            "rational rank",
            lambda item: item["true_R2_exhaustive"][-1].__setitem__(
                "central_locator_affine_rank_over_Q", 1
            ),
        ),
        (
            "field occupancy",
            lambda item: item["true_R2_base_field_lift"].__setitem__(
                "retained_support_occupancy", 2
            ),
        ),
        (
            "asymptotic limit",
            lambda item: item["true_R2_asymptotic"]["limits"].__setitem__(
                "normalized_log_Gsid_lower", 0.0
            ),
        ),
        ("scope", lambda item: item["scope"].__setitem__("open", ["nothing remains"])),
    ]
    rejected = []
    for name, mutate in mutations:
        mutant = copy.deepcopy(report)
        mutate(mutant)
        try:
            validate_report(mutant)
        except (KeyError, TypeError, ValueError):
            rejected.append(name)
        else:
            raise ValueError(f"tamper mutation was accepted: {name}")
    print(f"TAMPER SELF-TEST: PASS ({len(rejected)}/{len(mutations)})")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    root = repo_root()
    if args.tamper_selftest:
        tamper_selftest(root)
        return 0
    report = build_report(root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        finite = report["full_R1_finite"]
        asymptotic = report["true_R2_asymptotic"]
        print("RESULT: PASS")
        print(f"status: {report['status']}")
        print(
            "finite full-R1: "
            f"M={finite['full_slice']['M']} L={finite['full_slice']['L']} "
            f"fiber={finite['fiber_size']} slopes={finite['distinct_bad_slopes']} "
            f"rate={finite['normalized_log_lower']:.12f}"
        )
        print(
            "true-R2 limit: "
            f"log(15/8)/4={asymptotic['limits']['normalized_log_Gsid_lower']:.12f}"
        )
        print(f"payload_sha256: {report['payload_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
