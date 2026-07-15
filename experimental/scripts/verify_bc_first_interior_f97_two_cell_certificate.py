#!/usr/bin/env python3
"""Verify the exact F_97 two-cell first-match certificate.

This is a standalone, stdlib-only finite verifier.  It reconstructs the
first-interior LineRay incidence of the pinned affine line, factors two
common-GCD cells, and enumerates each residual projective plane in two
independent ways:

* all |P^2(F_97)| projective coefficient points; and
* all monic split divisors of the appropriate residual domain polynomial.

The result is a special finite certificate, not an asymptotic or deployed-row
claim.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter


STATUS = "PROVED-SPECIAL / EXACT FINITE CERTIFICATE"
P = 97
N = 16
K = 5
M = 7
W = 2
D1_TARGET = 4
OMEGA = N - M

U = (11, 17, 84, 52, 77, 65, 2, 28, 39, 59, 35, 84, 46, 87, 83, 71)
V = (91, 2, 23, 68, 85, 91, 65, 60, 85, 27, 9, 7, 18, 79, 76, 11)

EXPECTED_SUPPORTS = (
    ("z0", 0, (3, 4, 5, 8, 9, 11, 14)),
    ("z1", 1, (0, 1, 2, 3, 6, 7, 12)),
    ("z2a", 2, (4, 6, 10, 11, 12, 13, 14)),
    ("z2b", 2, (1, 2, 3, 4, 6, 11, 15)),
)

EXPECTED_CELLS = (
    {
        "name": "A",
        "members": ("z0", "z1", "z2a"),
        "gcd_roots": (15,),
        "split_roots": {
            (0, 1, 2, 3, 5, 7, 8, 9),
            (0, 1, 2, 6, 7, 10, 12, 13),
            (4, 5, 8, 9, 10, 11, 13, 14),
        },
    },
    {
        "name": "B",
        "members": ("z0", "z1", "z2b"),
        "gcd_roots": (10, 13),
        "split_roots": {
            (0, 1, 2, 6, 7, 12, 15),
            (0, 5, 7, 8, 9, 12, 14),
            (4, 5, 8, 9, 11, 14, 15),
        },
    },
)

# Filled from the canonical payload below.  Keeping the digest pinned makes a
# fixture change visible even when every mathematical check is updated too.
EXPECTED_CERTIFICATE_SHA256 = (
    "d77eefe2dcbb6b2544c991d2a6fc9022f430ddb2b5b7ad7a3d3e83147d614130"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


# ------------------------------------------------------------------ F_p/poly
def inv(a: int) -> int:
    require(a % P != 0, "attempted to invert zero")
    return pow(a % P, P - 2, P)


def pnorm(poly):
    out = [x % P for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return out


def pdeg(poly) -> int:
    return len(pnorm(poly)) - 1


def padd(left, right):
    out = [0] * max(len(left), len(right))
    for i in range(len(out)):
        out[i] = ((left[i] if i < len(left) else 0)
                  + (right[i] if i < len(right) else 0)) % P
    return pnorm(out)


def pscale(poly, scalar):
    return pnorm([(scalar % P) * coefficient % P for coefficient in poly])


def pmul(left, right):
    if not left or not right:
        return []
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % P
    return pnorm(out)


def pdivmod(dividend, divisor):
    dividend = pnorm(dividend)
    divisor = pnorm(divisor)
    require(bool(divisor), "polynomial division by zero")
    quotient = [0] * max(0, len(dividend) - len(divisor) + 1)
    leading_inverse = inv(divisor[-1])
    while dividend and len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        scalar = dividend[-1] * leading_inverse % P
        quotient[shift] = scalar
        for j, coefficient in enumerate(divisor):
            dividend[shift + j] = (
                dividend[shift + j] - scalar * coefficient
            ) % P
        dividend = pnorm(dividend)
    return pnorm(quotient), dividend


def pgcd(left, right):
    left, right = pnorm(left), pnorm(right)
    while right:
        left, right = right, pdivmod(left, right)[1]
    return pscale(left, inv(left[-1])) if left else []


def pgcd_many(polys):
    polys = [list(poly) for poly in polys]
    require(bool(polys), "empty polynomial GCD")
    out = polys[0]
    for poly in polys[1:]:
        out = pgcd(out, poly)
    return out


def peval(poly, x: int) -> int:
    out = 0
    for coefficient in reversed(poly):
        out = (out * x + coefficient) % P
    return out


def pfrom_roots(roots):
    out = [1]
    for root in roots:
        out = pmul(out, [(-root) % P, 1])
    return out


def pad(poly, length: int):
    return tuple(poly[i] if i < len(poly) else 0 for i in range(length))


# -------------------------------------------------------------- domain mu_16
def primitive_root() -> int:
    for candidate in range(2, P):
        if pow(candidate, (P - 1) // 2, P) != 1 \
                and pow(candidate, (P - 1) // 3, P) != 1:
            return candidate
    raise AssertionError("no primitive root")


GENERATOR = primitive_root()
H = pow(GENERATOR, (P - 1) // N, P)
D = tuple(pow(H, exponent, P) for exponent in range(N))
LAMBDA = pfrom_roots(D)
require(len(set(D)) == N, "mu_16 domain points are not distinct")
require(LAMBDA == [P - 1] + [0] * (N - 1) + [1],
        "domain polynomial is not X^16-1")


# ----------------------------------------------------------- linear algebra
def matrix_rank(matrix) -> int:
    if not matrix:
        return 0
    work = [[entry % P for entry in row] for row in matrix]
    ncols = len(work[0])
    rank = 0
    for column in range(ncols):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scalar = inv(work[rank][column])
        work[rank] = [scalar * entry % P for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                scalar = work[row][column]
                work[row] = [
                    (entry - scalar * pivot_entry) % P
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def interpolate(indices, values):
    require(len(indices) == len(values), "interpolation length mismatch")
    out = []
    for i, index in enumerate(indices):
        numerator = [1]
        denominator = 1
        for j, other_index in enumerate(indices):
            if i == j:
                continue
            numerator = pmul(numerator, [(-D[other_index]) % P, 1])
            denominator = denominator * (D[index] - D[other_index]) % P
        out = padd(out, pscale(numerator, values[i] * inv(denominator)))
    require(all(peval(out, D[index]) == value
                for index, value in zip(indices, values)),
            "interpolation replay failed")
    return out


# ------------------------------------------------------- incidence recovery
def line_word(slope: int):
    return tuple((u + slope * v) % P for u, v in zip(U, V))


def minimal_shifted_degree(word) -> int:
    """Find min d with W*word=N, deg W<=d, deg N<=d+K-1."""
    for degree in range(N + 1):
        ncols = (degree + 1) + (degree + K)
        matrix = []
        for x, y in zip(D, word):
            matrix.append(
                [(y * pow(x, j, P)) % P for j in range(degree + 1)]
                + [(-pow(x, j, P)) % P for j in range(degree + K)]
            )
        if matrix_rank(matrix) < ncols:
            return degree
    raise AssertionError("no shifted interpolation kernel")


def restriction_polynomial(word, support):
    head = support[:K]
    polynomial = interpolate(head, tuple(word[index] for index in head))
    if all(peval(polynomial, D[index]) == word[index] for index in support):
        require(pdeg(polynomial) < K, "restriction polynomial degree overflow")
        return polynomial
    return None


def cyclic_aperiodic(indices) -> bool:
    support = set(indices)
    return all(
        {(index + shift) % N for index in support} != support
        for shift in range(1, N)
    )


def reconstruct_witnesses(first_interior_slopes):
    line_rays = []
    raw_support_count = 0
    for slope in first_interior_slopes:
        word = line_word(slope)
        by_codeword = {}
        for support in itertools.combinations(range(N), M):
            polynomial = restriction_polynomial(word, support)
            if polynomial is None:
                continue
            key = pad(polynomial, K)
            by_codeword.setdefault(key, []).append(tuple(support))
        for coefficients, supports in by_codeword.items():
            agreement = tuple(
                index for index, x in enumerate(D)
                if peval(coefficients, x) == word[index]
            )
            require(len(supports) == math.comb(len(agreement), M),
                    "LineRay support saturation failed")
            require(all(set(support).issubset(agreement) for support in supports),
                    "support is not contained in its agreement set")
            raw_support_count += len(supports)
            line_rays.append({
                "slope": slope,
                "support": agreement,
                "coefficients": coefficients,
                "representatives": tuple(sorted(supports)),
            })

    expected_by_key = {
        (slope, support): label
        for label, slope, support in EXPECTED_SUPPORTS
    }
    found_by_key = {
        (ray["slope"], ray["support"]): ray for ray in line_rays
    }
    require(set(found_by_key) == set(expected_by_key),
            "retained first-interior LineRay list changed")
    require(raw_support_count == 4 and len(line_rays) == 4,
            "expected four saturated support/LineRay witnesses")

    witnesses = {}
    for key, label in expected_by_key.items():
        ray = found_by_key[key]
        require(len(ray["support"]) == M, "agreement set is not exactly size 7")
        require(ray["representatives"] == (ray["support"],),
                "expected a unique support representative")
        require(cyclic_aperiodic(ray["support"]),
                "retained support is cyclic-periodic")
        error_roots = tuple(index for index in range(N)
                            if index not in set(ray["support"]))
        locator = pfrom_roots(D[index] for index in error_roots)
        require(pdeg(locator) == OMEGA and locator[-1] == 1,
                "error locator is not monic of degree 9")
        witnesses[label] = {
            **ray,
            "label": label,
            "error_roots": error_roots,
            "locator": locator,
        }
    return witnesses


def common_support_count() -> int:
    count = 0
    for support in itertools.combinations(range(N), M):
        if restriction_polynomial(U, support) is not None \
                and restriction_polynomial(V, support) is not None:
            count += 1
    return count


# ---------------------------------------------------------- cell enumeration
def projective_points():
    for second in range(P):
        for third in range(P):
            yield (1, second, third)
    for third in range(P):
        yield (0, 1, third)
    yield (0, 0, 1)


def root_indices(poly):
    return tuple(index for index, x in enumerate(D) if peval(poly, x) == 0)


def enumerate_cell(cell_spec, witnesses):
    member_locators = [witnesses[label]["locator"]
                       for label in cell_spec["members"]]
    common_gcd = pgcd_many(member_locators)
    gcd_roots = root_indices(common_gcd)
    require(gcd_roots == cell_spec["gcd_roots"],
            f"cell {cell_spec['name']} common GCD changed")
    require(pdeg(common_gcd) == len(gcd_roots),
            f"cell {cell_spec['name']} GCD degree/root mismatch")

    residual_degree = OMEGA - pdeg(common_gcd)
    residual_locators = []
    for locator in member_locators:
        quotient, remainder = pdivmod(locator, common_gcd)
        require(not remainder and pdeg(quotient) == residual_degree,
                f"cell {cell_spec['name']} GCD division failed")
        residual_locators.append(quotient)

    vectors = [list(pad(locator, residual_degree + 1))
               for locator in residual_locators]
    plane_rank = matrix_rank(vectors)
    require(plane_rank == 3,
            f"cell {cell_spec['name']} residual locators do not span a plane")

    active_indices = tuple(index for index in range(N)
                           if index not in set(gcd_roots))
    residual_domain = pfrom_roots(D[index] for index in active_indices)
    quotient, remainder = pdivmod(LAMBDA, common_gcd)
    require(not remainder and quotient == residual_domain,
            f"cell {cell_spec['name']} residual domain factorization failed")

    projective_hit_roots = []
    projective_count = 0
    for coefficients in projective_points():
        projective_count += 1
        combination = []
        for coefficient, locator in zip(coefficients, residual_locators):
            combination = padd(combination, pscale(locator, coefficient))
        if pdeg(combination) != residual_degree:
            continue
        combination = pscale(combination, inv(combination[-1]))
        _quotient, remainder = pdivmod(residual_domain, combination)
        if remainder:
            continue
        roots = root_indices(combination)
        require(len(roots) == residual_degree,
                f"cell {cell_spec['name']} projective split-root mismatch")
        projective_hit_roots.append(roots)

    expected_projective_count = P * P + P + 1
    require(projective_count == expected_projective_count,
            f"cell {cell_spec['name']} projective-plane size mismatch")
    require(len(projective_hit_roots) == len(set(projective_hit_roots)),
            f"cell {cell_spec['name']} duplicate projective split locators")

    divisor_hit_roots = []
    divisor_count = 0
    for roots in itertools.combinations(active_indices, residual_degree):
        divisor_count += 1
        locator = pfrom_roots(D[index] for index in roots)
        vector = list(pad(locator, residual_degree + 1))
        if matrix_rank(vectors + [vector]) == plane_rank:
            divisor_hit_roots.append(tuple(roots))

    expected_divisor_count = math.comb(len(active_indices), residual_degree)
    require(divisor_count == expected_divisor_count,
            f"cell {cell_spec['name']} divisor census size mismatch")
    require(set(projective_hit_roots) == set(divisor_hit_roots),
            f"cell {cell_spec['name']} dual enumerations disagree")
    require(set(projective_hit_roots) == cell_spec["split_roots"],
            f"cell {cell_spec['name']} exact split-locator intersection changed")

    cell_witnesses = tuple(
        label for label, witness in witnesses.items()
        if set(gcd_roots).issubset(witness["error_roots"])
    )
    slopes = tuple(sorted({witnesses[label]["slope"]
                           for label in cell_witnesses}))
    require(set(cell_witnesses) == set(cell_spec["members"]),
            f"cell {cell_spec['name']} witness membership changed")
    require(slopes == (0, 1, 2),
            f"cell {cell_spec['name']} slope projection changed")

    return {
        "name": cell_spec["name"],
        "gcd_roots": gcd_roots,
        "gcd_degree": pdeg(common_gcd),
        "residual_degree": residual_degree,
        "plane_rank": plane_rank,
        "projective_count": projective_count,
        "divisor_count": divisor_count,
        "split_roots": tuple(sorted(projective_hit_roots)),
        "witnesses": cell_witnesses,
        "slopes": slopes,
    }


def canonical_payload(d1_histogram, witnesses, cells, first_match_parts):
    return {
        "field": P,
        "domain": list(D),
        "parameters": {"n": N, "K": K, "m": M, "w": W,
                       "d1": D1_TARGET, "omega": OMEGA},
        "line": {"u": list(U), "v": list(V)},
        "d1_histogram": sorted(d1_histogram.items()),
        "witnesses": [
            {
                "label": label,
                "slope": witnesses[label]["slope"],
                "support": list(witnesses[label]["support"]),
                "error_roots": list(witnesses[label]["error_roots"]),
            }
            for label, _slope, _support in EXPECTED_SUPPORTS
        ],
        "cells": [
            {
                "name": cell["name"],
                "gcd_roots": list(cell["gcd_roots"]),
                "residual_degree": cell["residual_degree"],
                "plane_rank": cell["plane_rank"],
                "projective_count": cell["projective_count"],
                "divisor_count": cell["divisor_count"],
                "split_roots": [list(roots) for roots in cell["split_roots"]],
                "witnesses": list(cell["witnesses"]),
                "slopes": list(cell["slopes"]),
            }
            for cell in cells
        ],
        "first_match_parts": [list(part) for part in first_match_parts],
        "first_match_slope_budget": sum(len(part) for part in first_match_parts),
    }


def main() -> int:
    d1_histogram = Counter()
    slopes_by_degree = {}
    for slope in range(P):
        degree = minimal_shifted_degree(line_word(slope))
        d1_histogram[degree] += 1
        slopes_by_degree.setdefault(degree, []).append(slope)
    require(dict(sorted(d1_histogram.items())) == {4: 3, 6: 94},
            "shifted minimal-degree histogram changed")
    first_interior_slopes = tuple(slopes_by_degree[D1_TARGET])
    require(first_interior_slopes == (0, 1, 2),
            "first-interior slopes changed")

    common_supports = common_support_count()
    require(common_supports == 0, "a common support appeared")
    require(math.gcd(M, N) == 1, "fixture no longer forces aperiodicity")
    require(all(cyclic_aperiodic(support)
                for support in itertools.combinations(range(N), M)),
            "a cyclic-periodic 7-subset appeared")

    witnesses = reconstruct_witnesses(first_interior_slopes)
    cells = tuple(enumerate_cell(spec, witnesses) for spec in EXPECTED_CELLS)

    covered_witnesses = set().union(*(set(cell["witnesses"]) for cell in cells))
    require(covered_witnesses == set(witnesses),
            "two common-GCD cells do not cover all retained witnesses")
    first_match_parts = (
        cells[0]["slopes"],
        tuple(slope for slope in cells[1]["slopes"]
              if slope not in set(cells[0]["slopes"])),
    )
    require(first_match_parts == ((0, 1, 2), ()),
            "ordered first-match slope parts changed")
    first_match_budget = sum(len(part) for part in first_match_parts)
    require(first_match_budget == 3, "exact first-match slope budget changed")

    payload = canonical_payload(
        dict(sorted(d1_histogram.items())), witnesses, cells, first_match_parts
    )
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256 is not None:
        require(digest == EXPECTED_CERTIFICATE_SHA256,
                "canonical certificate digest changed")

    print("=== BC first-interior F97 two-cell certificate ===")
    print(f"status: {STATUS}")
    print(f"field/domain: F_{P}, D=mu_{N}, generator={H}")
    print(f"parameters: (K,m,w,d1,omega)=({K},{M},{W},{D1_TARGET},{OMEGA})")
    print(f"d1 histogram: {dict(sorted(d1_histogram.items()))}; "
          f"first-interior slopes={list(first_interior_slopes)}")
    print(f"common supports: {common_supports}; all 7-subsets cyclic-aperiodic: yes")
    print("retained witnesses:")
    for label, _slope, _support in EXPECTED_SUPPORTS:
        witness = witnesses[label]
        print(f"  {label}: z={witness['slope']} support={list(witness['support'])} "
              f"error_roots={list(witness['error_roots'])}")
    print("factored cells (dual exact enumeration):")
    for cell in cells:
        print(
            f"  {cell['name']}: gcd_roots={list(cell['gcd_roots'])} "
            f"residual_degree={cell['residual_degree']} rank={cell['plane_rank']} "
            f"P2_points={cell['projective_count']} "
            f"divisor_candidates={cell['divisor_count']} "
            f"split_count={len(cell['split_roots'])}"
        )
        print(f"    split_roots={[list(roots) for roots in cell['split_roots']]}")
    print(f"cover: A union B={sorted(covered_witnesses)}")
    print(f"ordered first-match slope parts="
          f"{[list(part) for part in first_match_parts]}; budget={first_match_budget}")
    print(f"certificate_sha256: {digest}")
    print("claim_boundary: exact retained first-interior subincidence only; "
          "not a full tangent atlas, extension cell, or deployed/asymptotic theorem")
    print("RESULT: PASS (EXACT FINITE TWO-CELL FIRST-MATCH CERTIFICATE)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
