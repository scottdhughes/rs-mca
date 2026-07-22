#!/usr/bin/env python3
"""Exact controls for the M31 all-weight anchor-exchange Padé bijection.

This is a stdlib-only verifier.  It checks the corrected two-row key-equation
module for every degree-<K codeword in a complete GF(7) fixture, and checks
the source-bound nonanchor-codeword <-> (G,b) exchange-pair bijection by an
independent enumeration of both sides.

The finite fixture is evidence for (and a falsifier of implementations of)
the algebraic identities.  It is not an M31 list bound, a v4 owner, or a
payment of any global residual.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import Counter
from typing import Iterable, Iterator, Sequence


Poly = tuple[int, ...]  # coefficients in increasing degree order
ZERO: Poly = ()
ONE: Poly = (1,)


class CheckFailure(RuntimeError):
    """Raised when an exact verifier gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def trim(values: Iterable[int], p: int) -> Poly:
    out = [value % p for value in values]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def degree(poly: Poly) -> int:
    return len(poly) - 1


def coeff(poly: Poly, index: int) -> int:
    return poly[index] if 0 <= index < len(poly) else 0


def padd(left: Poly, right: Poly, p: int) -> Poly:
    return trim(
        (coeff(left, i) + coeff(right, i) for i in range(max(len(left), len(right)))),
        p,
    )


def pneg(poly: Poly, p: int) -> Poly:
    return trim((-value for value in poly), p)


def psub(left: Poly, right: Poly, p: int) -> Poly:
    return padd(left, pneg(right, p), p)


def pscale(poly: Poly, scalar: int, p: int) -> Poly:
    return trim((scalar * value for value in poly), p)


def pmul(left: Poly, right: Poly, p: int) -> Poly:
    if not left or not right:
        return ZERO
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out, p)


def pinv(value: int, p: int) -> int:
    value %= p
    require(value != 0, "attempted inversion of zero")
    return pow(value, p - 2, p)


def pdivmod(numerator: Poly, denominator: Poly, p: int) -> tuple[Poly, Poly]:
    require(bool(denominator), "polynomial division by zero")
    remainder = list(numerator)
    quotient = [0] * max(0, len(numerator) - len(denominator) + 1)
    inverse_lead = pinv(denominator[-1], p)
    while remainder and len(remainder) >= len(denominator):
        shift = len(remainder) - len(denominator)
        scale = remainder[-1] * inverse_lead % p
        quotient[shift] = scale
        for i, value in enumerate(denominator):
            remainder[shift + i] = (remainder[shift + i] - scale * value) % p
        while remainder and remainder[-1] == 0:
            remainder.pop()
    return trim(quotient, p), trim(remainder, p)


def pexact(numerator: Poly, denominator: Poly, p: int, label: str) -> Poly:
    quotient, remainder = pdivmod(numerator, denominator, p)
    require(not remainder, f"nonexact division: {label}")
    return quotient


def pmonic(poly: Poly, p: int) -> Poly:
    require(bool(poly), "zero polynomial has no monic normalization")
    return pscale(poly, pinv(poly[-1], p), p)


def pgcd(left: Poly, right: Poly, p: int) -> Poly:
    while right:
        _, remainder = pdivmod(left, right, p)
        left, right = right, remainder
    return pmonic(left, p) if left else ZERO


def pmod(poly: Poly, modulus: Poly, p: int) -> Poly:
    return pdivmod(poly, modulus, p)[1]


def peval(poly: Poly, x: int, p: int) -> int:
    total = 0
    for value in reversed(poly):
        total = (total * x + value) % p
    return total


def locator(points: Iterable[int], p: int) -> Poly:
    out = ONE
    for point in sorted(points):
        out = pmul(out, ((-point) % p, 1), p)
    return out


def interpolate(points: Sequence[int], values: Sequence[int], p: int) -> Poly:
    require(len(points) == len(values), "interpolation length mismatch")
    require(len(set(points)) == len(points), "interpolation points are not distinct")
    total = ZERO
    for i, point in enumerate(points):
        basis = ONE
        denominator = 1
        for j, other in enumerate(points):
            if i == j:
                continue
            basis = pmul(basis, ((-other) % p, 1), p)
            denominator = denominator * (point - other) % p
        total = padd(total, pscale(basis, values[i] * pinv(denominator, p), p), p)
    require(
        all(peval(total, point, p) == value % p for point, value in zip(points, values)),
        "interpolation replay failed",
    )
    return total


def all_polynomials(p: int, degree_bound: int) -> Iterator[Poly]:
    for values in itertools.product(range(p), repeat=degree_bound):
        yield trim(values, p)


def roots_in(poly: Poly, domain: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple(point for point in domain if peval(poly, point, p) == 0)


def poly_key(poly: Poly) -> tuple[int, ...]:
    return poly


def pair_key(g_poly: Poly, b_poly: Poly) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return poly_key(g_poly), poly_key(b_poly)


def enumerate_monic_split_divisors(
    points: Sequence[int], minimum_degree: int, p: int
) -> Iterator[Poly]:
    for size in range(minimum_degree, len(points) + 1):
        for subset in itertools.combinations(points, size):
            yield locator(subset, p)


def module_decompose(
    w_poly: Poly,
    n_poly: Poly,
    a0: Poly,
    l0: Poly,
    v_poly: Poly,
    u_poly: Poly,
    t_poly: Poly,
    p: int,
) -> tuple[Poly, Poly]:
    """Return alpha,beta for (W,N)=alpha(L0,0)+beta(V,A0)."""

    require(not pmod(psub(n_poly, pmul(w_poly, u_poly, p), p), t_poly, p), "module key equation")
    beta = pexact(n_poly, a0, p, "N/A0")
    alpha = pexact(psub(w_poly, pmul(beta, v_poly, p), p), l0, p, "(W-beta*V)/L0")
    require(padd(pmul(alpha, l0, p), pmul(beta, v_poly, p), p) == w_poly, "basis W replay")
    require(pmul(beta, a0, p) == n_poly, "basis N replay")
    return alpha, beta


def exact_error_support(
    u_poly: Poly, codeword: Poly, domain: Sequence[int], p: int
) -> tuple[int, ...]:
    return tuple(point for point in domain if peval(u_poly, point, p) != peval(codeword, point, p))


def force_selected_sublist_to_boundary(
    received: Sequence[int],
    selected: Sequence[Sequence[int]],
    radius: int,
    alphabet_size: int,
) -> tuple[tuple[int, ...], dict[str, int]]:
    """Preserve a selected sublist while forcing a minimum-agreement anchor.

    This is the finite-alphabet Corollary 3.3 construction.  The input rows
    are evaluation vectors, not polynomials; no Reed--Solomon structure is
    used by the lemma.
    """

    n = len(received)
    require(0 <= radius < n, "boundary forcing radius range")
    require(bool(selected), "boundary forcing selected sublist")
    require(len(selected) < alphabet_size, "fresh-symbol strict field slack")
    require(all(len(row) == n for row in selected), "boundary forcing row length")
    require(len({tuple(row) for row in selected}) == len(selected), "selected rows distinct")

    agreement = n - radius
    agreement_counts = [
        sum(left == right for left, right in zip(received, row, strict=True))
        for row in selected
    ]
    require(min(agreement_counts) >= agreement, "selected row outside input ball")
    anchor_index = min(range(len(selected)), key=agreement_counts.__getitem__)
    anchor = selected[anchor_index]
    t = agreement_counts[anchor_index] - agreement
    matching_coordinates = [
        index for index, (left, right) in enumerate(zip(received, anchor, strict=True))
        if left == right
    ]
    require(len(matching_coordinates) >= t, "anchor matching-coordinate supply")

    changed = list(received)
    for coordinate in matching_coordinates[:t]:
        used = {row[coordinate] for row in selected}
        fresh = next((value for value in range(alphabet_size) if value not in used), None)
        require(fresh is not None, "fresh symbol exists")
        changed[coordinate] = fresh

    final_agreements = [
        sum(left == right for left, right in zip(changed, row, strict=True))
        for row in selected
    ]
    require(min(final_agreements) >= agreement, "selected row lost from output ball")
    require(final_agreements[anchor_index] == agreement, "anchor not forced to boundary")
    require(
        all(after <= before for before, after in zip(agreement_counts, final_agreements, strict=True)),
        "fresh-symbol edit created an agreement",
    )
    return tuple(changed), {
        "anchor_index": anchor_index,
        "changed_coordinates": t,
        "initial_anchor_agreement": agreement_counts[anchor_index],
        "final_anchor_agreement": final_agreements[anchor_index],
        "retained_rows": len(selected),
    }


def run_boundary_forcing_fixture() -> dict[str, object]:
    """A nontrivial two-word interior ball forced onto its boundary."""

    p = 7
    n = 6
    radius = 3
    zero = (0,) * n
    # Evaluation of X(X-1), a degree-two RS codeword with roots 0 and 1.
    other_poly = (0, p - 1, 1)
    other = tuple(peval(other_poly, x, p) for x in range(n))
    received = list(zero)
    received[2] = other[2]
    received[3] = other[3]
    initial_distances = [
        sum(left != right for left, right in zip(received, row, strict=True))
        for row in (zero, other)
    ]
    require(initial_distances == [2, 2], "boundary fixture starts strictly interior")
    forced, audit = force_selected_sublist_to_boundary(
        received, (zero, other), radius, p
    )
    final_distances = [
        sum(left != right for left, right in zip(forced, row, strict=True))
        for row in (zero, other)
    ]
    require(max(final_distances) == radius, "boundary fixture exact radius")
    require(all(distance <= radius for distance in final_distances), "boundary fixture retention")
    return {
        "field": "GF(7)",
        "n": n,
        "R": radius,
        "selected_rows": 2,
        "strict_field_slack": 2 < p,
        "initial_distances": initial_distances,
        "final_distances": final_distances,
        "audit": audit,
    }


def audit_exchange_pair(
    *,
    g_poly: Poly,
    b_poly: Poly,
    a0: Poly,
    l0: Poly,
    v_poly: Poly,
    u_poly: Poly,
    t_poly: Poly,
    domain: Sequence[int],
    e0: Sequence[int],
    k: int,
    radius: int,
    w0: int,
    p: int,
) -> dict[str, object]:
    """Audit one pair already known to satisfy its admission predicates."""

    g = degree(g_poly)
    n = len(domain)
    j0 = len(e0)
    agreement = n - radius
    w = agreement - k
    t = radius - j0
    m = g - t
    require(w0 == (n - j0) - k == w + t, "slack identity w0=w+t")
    require(g_poly[-1] == 1, "G is not monic")
    require(not pmod(a0, g_poly, p), "G does not divide A0")
    require(g >= w0 + 1, "G degree below the nonanchor floor")
    require(m >= w + 1, "slack-normal degree floor m>=w+1")
    require(bool(b_poly), "zero b duplicates the anchor")
    require(degree(b_poly) < g - w0, "b degree gate")
    require(degree(b_poly) < m - w, "slack-normal b degree gate")
    require(pgcd(b_poly, g_poly, p) == ONE, "gcd(b,G) exact-support gate")

    h_poly = pgcd(l0, psub(g_poly, pmul(b_poly, v_poly, p), p), p)
    h = degree(h_poly)
    require(h >= j0 + g - radius, "H degree/radius gate")
    require(h >= m, "slack-normal gcd gate h>=m")

    a0_over_g = pexact(a0, g_poly, p, "A0/G")
    codeword = pmul(a0_over_g, b_poly, p)
    require(bool(codeword), "nonanchor pair reconstructed zero")
    require(degree(codeword) < k, "reconstructed codeword degree")

    l0_over_h = pexact(l0, h_poly, p, "L0/H")
    w_poly = pmul(g_poly, l0_over_h, p)
    n_poly = pmul(pmul(a0, b_poly, p), l0_over_h, p)
    require(n_poly == pmul(w_poly, codeword, p), "N=W*c orientation")

    errors = exact_error_support(u_poly, codeword, domain, p)
    expected_locator = locator(errors, p)
    require(w_poly == expected_locator, "exchange pair failed exact error-locator recovery")
    expected_weight = j0 + g - h
    require(len(errors) == expected_weight, "exchange weight identity")
    require(len(errors) == radius + m - h, "slack-normal weight identity j=R+m-h")
    require(len(errors) <= radius, "exchange pair reconstructs outside the list ball")
    require(errors != tuple(sorted(e0)), "nonanchor pair duplicates anchor support")

    alpha_expected = pexact(
        psub(g_poly, pmul(b_poly, v_poly, p), p), h_poly, p, "(G-bV)/H"
    )
    beta_expected = pmul(b_poly, l0_over_h, p)
    alpha, beta = module_decompose(
        w_poly, n_poly, a0, l0, v_poly, u_poly, t_poly, p
    )
    require(alpha == alpha_expected, "exchange alpha orientation")
    require(beta == beta_expected, "exchange beta orientation")

    repaired_anchor_points = tuple(point for point in e0 if point not in errors)
    require(locator(repaired_anchor_points, p) == h_poly, "H repaired-anchor roots")

    return {
        "codeword": codeword,
        "errors": errors,
        "H": h_poly,
        "h": h,
        "t": t,
        "w": w,
        "m": m,
        "W": w_poly,
        "N": n_poly,
        "alpha": alpha,
        "beta": beta,
    }


def run_toy_fixture() -> tuple[dict[str, object], dict[str, object]]:
    p = 7
    domain = tuple(range(6))
    n = len(domain)
    k = 3
    agreement = 4
    radius = n - agreement
    codewords = tuple(all_polynomials(p, k))
    require(len(codewords) == p**k == 343, "toy codeword census")

    configuration_count = 0
    code_check_count = 0
    listed_codeword_count = 0
    nonanchor_incidence_count = 0
    pair_candidate_count = 0
    admitted_pair_count = 0
    boundary_v_one_count = 0
    generic_v_count = 0
    naive_v_one_identity_count = 0
    generic_naive_identity_failures = 0
    wrong_exchange_coefficient_failures = 0
    wrong_received_orientation_failures = 0
    wrong_basis_sign_failures = 0
    wrong_swapped_basis_failures = 0
    weight_histogram: Counter[int] = Counter()
    listed_weight_histogram: Counter[int] = Counter()
    nonanchor_weight_histogram: Counter[int] = Counter()
    first_generic_witness: dict[str, object] | None = None
    first_weak_h_witness: dict[str, object] | None = None
    first_nonmonic_duplicate: dict[str, object] | None = None
    first_gcd_omission_witness: dict[str, object] | None = None
    first_zero_b_anchor_duplicate: dict[str, object] | None = None
    first_degree_gate_witness: dict[str, object] | None = None

    t_poly = locator(domain, p)
    require(degree(t_poly) == n, "toy domain locator degree")

    for e0_tuple in itertools.combinations(domain, radius):
        e0 = tuple(sorted(e0_tuple))
        s0 = tuple(point for point in domain if point not in e0)
        j0 = len(e0)
        s0_size = len(s0)
        w0 = s0_size - k
        a0 = locator(s0, p)
        l0 = locator(e0, p)
        require(pmul(a0, l0, p) == t_poly, "T=A0*L0")

        for v_values in itertools.product(range(1, p), repeat=j0):
            configuration_count += 1
            v_poly = interpolate(e0, v_values, p)
            h0_values = tuple(pinv(value, p) for value in v_values)
            h0 = interpolate(e0, h0_values, p)
            require(degree(v_poly) < j0 and degree(h0) < j0, "V/H0 degree")
            require(pmod(pmul(v_poly, h0, p), l0, p) == ONE, "V*H0=1 mod L0")

            u_poly = pmul(a0, h0, p)
            require(degree(u_poly) < n, "received interpolant degree")
            require(roots_in(u_poly, domain, p) == s0, "received zero set")
            require(
                all(peval(u_poly, point, p) != 0 for point in e0),
                "received anchor values must be units",
            )

            # The two displayed rows really lie in M_U, and have determinant T.
            require(not pmod(pneg(pmul(l0, u_poly, p), p), t_poly, p), "first basis row")
            require(
                not pmod(psub(a0, pmul(v_poly, u_poly, p), p), t_poly, p),
                "corrected second basis row",
            )
            require(pmul(l0, a0, p) == t_poly, "basis determinant")

            if first_zero_b_anchor_duplicate is None:
                g_mut = locator(s0[: w0 + 1], p)
                zero_reconstruction = pmul(
                    pexact(a0, g_mut, p, "zero-b A0/G"), ZERO, p
                )
                require(not zero_reconstruction, "b=0 did not duplicate the anchor")
                first_zero_b_anchor_duplicate = {
                    "G": list(g_mut),
                    "b": [],
                    "reconstructed_codeword": [],
                    "reason": "b=0 reconstructs the translated anchor for every G",
                }

            if first_degree_gate_witness is None:
                g_mut = locator(s0[: w0 + 1], p)
                forbidden_degree = degree(g_mut) - w0
                for candidate in all_polynomials(p, forbidden_degree + 1):
                    if degree(candidate) != forbidden_degree:
                        continue
                    if pgcd(candidate, g_mut, p) != ONE:
                        continue
                    c_mut = pmul(pexact(a0, g_mut, p, "degree-gate A0/G"), candidate, p)
                    if degree(c_mut) >= k:
                        first_degree_gate_witness = {
                            "G": list(g_mut),
                            "b": list(candidate),
                            "deg_b": degree(candidate),
                            "required_strict_upper_bound": forbidden_degree,
                            "reconstructed_degree": degree(c_mut),
                            "K": k,
                        }
                        break
                require(first_degree_gate_witness is not None, "degree-gate witness search")

            # Hostile module controls.  Modding out only by L0 accepts junk.
            weak_w, weak_n = ZERO, l0
            require(
                not pmod(psub(weak_n, pmul(weak_w, u_poly, p), p), l0, p),
                "wrong-modulus witness did not enter weakened module",
            )
            require(
                bool(pmod(psub(weak_n, pmul(weak_w, u_poly, p), p), t_poly, p)),
                "wrong-modulus witness accidentally entered exact module",
            )
            wrong_signed_row = (v_poly, pneg(a0, p))
            if pmod(
                psub(wrong_signed_row[1], pmul(wrong_signed_row[0], u_poly, p), p),
                t_poly,
                p,
            ):
                wrong_basis_sign_failures += 1
            swapped_row = (a0, v_poly)
            if pmod(
                psub(swapped_row[1], pmul(swapped_row[0], u_poly, p), p),
                t_poly,
                p,
            ):
                wrong_swapped_basis_failures += 1

            # The tempting uncorrected orientation U=A0*V is generally false.
            u_wrong = pmul(a0, v_poly, p)
            if pmod(psub(a0, pmul(v_poly, u_wrong, p), p), t_poly, p):
                wrong_received_orientation_failures += 1

            direct_pairs: dict[tuple[tuple[int, ...], tuple[int, ...]], Poly] = {}
            direct_nonanchors: dict[Poly, tuple[tuple[int, ...], tuple[int, ...]]] = {}
            anchor_seen = False

            # Exhaust every codeword, not only the radius-R list.
            for codeword in codewords:
                code_check_count += 1
                errors = exact_error_support(u_poly, codeword, domain, p)
                weight_histogram[len(errors)] += 1
                w_poly = locator(errors, p)
                n_poly = pmul(w_poly, codeword, p)
                module_decompose(w_poly, n_poly, a0, l0, v_poly, u_poly, t_poly, p)

                if len(errors) > radius:
                    continue
                listed_codeword_count += 1
                listed_weight_histogram[len(errors)] += 1
                if not codeword:
                    require(errors == e0, "zero codeword is not the translated anchor")
                    require(not anchor_seen, "anchor duplicate")
                    anchor_seen = True
                    continue

                common_zero = pgcd(a0, codeword, p)
                g_poly = pexact(a0, common_zero, p, "A0/gcd(A0,c)")
                a0_over_g = pexact(a0, g_poly, p, "A0/G direct")
                b_poly = pexact(codeword, a0_over_g, p, "c/(A0/G)")
                key = pair_key(g_poly, b_poly)
                require(key not in direct_pairs, "two codewords produced one exchange pair")
                direct_pairs[key] = codeword
                require(codeword not in direct_nonanchors, "duplicate direct nonanchor")
                direct_nonanchors[codeword] = key

                audited = audit_exchange_pair(
                    g_poly=g_poly,
                    b_poly=b_poly,
                    a0=a0,
                    l0=l0,
                    v_poly=v_poly,
                    u_poly=u_poly,
                    t_poly=t_poly,
                    domain=domain,
                    e0=e0,
                    k=k,
                    radius=radius,
                    w0=w0,
                    p=p,
                )
                require(audited["codeword"] == codeword, "direct pair reconstruction")

            require(anchor_seen, "translated anchor absent from list")

            enumerated_pairs: dict[tuple[tuple[int, ...], tuple[int, ...]], Poly] = {}
            for g_poly in enumerate_monic_split_divisors(s0, w0 + 1, p):
                g = degree(g_poly)
                for b_poly in all_polynomials(p, g - w0):
                    if not b_poly:
                        continue
                    pair_candidate_count += 1
                    if pgcd(b_poly, g_poly, p) != ONE:
                        # Preserve one exact-support mutation witness when its
                        # remaining algebraic gates happen to pass.
                        if first_gcd_omission_witness is None:
                            c_bad = pmul(pexact(a0, g_poly, p, "gcd mutation A0/G"), b_poly, p)
                            actual_new_error_count = len(
                                tuple(point for point in s0 if peval(c_bad, point, p) != 0)
                            )
                            require(actual_new_error_count < g, "gcd omission witness did not collapse support")
                            first_gcd_omission_witness = {
                                "E0": list(e0),
                                "V_values": list(v_values),
                                "G": list(g_poly),
                                "b": list(b_poly),
                                "actual_new_error_count": actual_new_error_count,
                                "claimed_g": g,
                            }
                        continue
                    h_poly = pgcd(l0, psub(g_poly, pmul(b_poly, v_poly, p), p), p)
                    h = degree(h_poly)
                    if h < j0 + g - radius:
                        if first_weak_h_witness is None:
                            c_weak = pmul(pexact(a0, g_poly, p, "weak-H A0/G"), b_poly, p)
                            weak_errors = exact_error_support(u_poly, c_weak, domain, p)
                            first_weak_h_witness = {
                                "E0": list(e0),
                                "V_values": list(v_values),
                                "g": g,
                                "h": h,
                                "weight": len(weak_errors),
                                "radius": radius,
                            }
                            require(len(weak_errors) > radius, "weak H witness not outside ball")
                        continue

                    admitted_pair_count += 1
                    key = pair_key(g_poly, b_poly)
                    require(key not in enumerated_pairs, "duplicate enumerated pair")
                    audited = audit_exchange_pair(
                        g_poly=g_poly,
                        b_poly=b_poly,
                        a0=a0,
                        l0=l0,
                        v_poly=v_poly,
                        u_poly=u_poly,
                        t_poly=t_poly,
                        domain=domain,
                        e0=e0,
                        k=k,
                        radius=radius,
                        w0=w0,
                        p=p,
                    )
                    reconstructed = audited["codeword"]
                    require(isinstance(reconstructed, tuple), "internal codeword type")
                    enumerated_pairs[key] = reconstructed

                    # alpha=G,beta=b is a module element, but it is not the
                    # exact error-locator/evaluator pair.  This is the subtle
                    # orientation mutation the checker is designed to catch.
                    wrong_w = padd(pmul(g_poly, l0, p), pmul(b_poly, v_poly, p), p)
                    wrong_n = pmul(b_poly, a0, p)
                    require(
                        not pmod(psub(wrong_n, pmul(wrong_w, u_poly, p), p), t_poly, p),
                        "wrong coefficients should still form some module element",
                    )
                    if wrong_w != audited["W"] or wrong_n != audited["N"]:
                        wrong_exchange_coefficient_failures += 1

                    # Scaling a monic G yields a duplicate representation if
                    # monicity is omitted.
                    if first_nonmonic_duplicate is None:
                        scale = 2
                        scaled_g = pscale(g_poly, scale, p)
                        scaled_b = pscale(b_poly, scale, p)
                        scaled_c = pmul(
                            pexact(a0, scaled_g, p, "A0/scaled G"), scaled_b, p
                        )
                        # Scaling G and b by the same unit leaves
                        # (A0/G)b unchanged.  Monicity removes this duplicate.
                        require(scaled_c == reconstructed, "nonmonic duplicate control")
                        first_nonmonic_duplicate = {
                            "G_lead": scaled_g[-1],
                            "monic_required": 1,
                        }

                    nonanchor_weight_histogram[len(audited["errors"])] += 1

                    if v_poly == ONE:
                        boundary_v_one_count += 1
                        require(audited["h"] == g, "V=1 boundary h=g")
                        require(audited["H"] == psub(g_poly, b_poly, p), "V=1 H=G-b")
                        require(b_poly == psub(g_poly, audited["H"], p), "V=1 b=G-H")
                        naive_v_one_identity_count += 1
                    else:
                        generic_v_count += 1
                        naive_b = psub(g_poly, audited["H"], p)
                        if naive_b != b_poly:
                            generic_naive_identity_failures += 1
                            if first_generic_witness is None:
                                first_generic_witness = {
                                    "E0": list(e0),
                                    "V_values": list(v_values),
                                    "V": list(v_poly),
                                    "G": list(g_poly),
                                    "b": list(b_poly),
                                    "H": list(audited["H"]),
                                    "G_minus_H": list(naive_b),
                                }

            require(direct_pairs == enumerated_pairs, "direct/enumerated pair atlas mismatch")
            require(
                set(direct_nonanchors) == set(enumerated_pairs.values()),
                "nonanchor codeword image mismatch",
            )
            nonanchor_incidence_count += len(enumerated_pairs)

    expected_configurations = math.comb(n, radius) * (p - 1) ** radius
    expected_code_checks = expected_configurations * p**k
    require(configuration_count == expected_configurations == 540, "configuration count")
    require(code_check_count == expected_code_checks == 185_220, "exhaustive code check count")
    require(nonanchor_incidence_count == 540, "nonanchor incidence count")
    require(admitted_pair_count == nonanchor_incidence_count, "admitted pair count")
    require(listed_codeword_count == 2 * configuration_count, "toy list size is not exactly two")
    require(boundary_v_one_count > 0, "no V=1 boundary controls")
    require(
        boundary_v_one_count + generic_v_count == nonanchor_incidence_count,
        "V=1/generic incidence partition",
    )
    require(
        naive_v_one_identity_count == boundary_v_one_count,
        "V=1 companion identity count",
    )
    require(generic_naive_identity_failures > 0, "generic V did not refute b=G-H")
    require(wrong_exchange_coefficient_failures == admitted_pair_count, "orientation mutation coverage")
    require(wrong_basis_sign_failures == configuration_count, "basis-sign mutation coverage")
    require(wrong_swapped_basis_failures > 0, "swapped-basis mutation coverage")
    require(wrong_received_orientation_failures > 0, "uncorrected-received mutation coverage")
    require(first_generic_witness is not None, "missing generic V route-cut witness")
    require(first_weak_h_witness is not None, "missing weakened-H hostile witness")
    require(first_nonmonic_duplicate is not None, "missing monicity hostile witness")
    require(first_gcd_omission_witness is not None, "missing gcd hostile witness")
    require(first_zero_b_anchor_duplicate is not None, "missing b=0 hostile witness")
    require(first_degree_gate_witness is not None, "missing degree hostile witness")

    summary: dict[str, object] = {
        "field": "GF(7)",
        "domain": list(domain),
        "n": n,
        "K": k,
        "agreement": agreement,
        "R": radius,
        "E0_supports": math.comb(n, radius),
        "unit_V_tables_per_E0": (p - 1) ** radius,
        "configurations": configuration_count,
        "codewords_per_configuration": p**k,
        "exhaustive_code_checks": code_check_count,
        "listed_codewords": listed_codeword_count,
        "nonanchor_incidences": nonanchor_incidence_count,
        "exchange_pair_candidates": pair_candidate_count,
        "admitted_exchange_pairs": admitted_pair_count,
        "slack_normal_identity_checks": admitted_pair_count,
        "slack_normal_form": "t=R-j0; w0=w+t; m=g-t; m>=w+1; deg(b)<m-w; h>=m; j=R+m-h",
        "all_codeword_weight_histogram": dict(sorted(weight_histogram.items())),
        "listed_weight_histogram": dict(sorted(listed_weight_histogram.items())),
        "nonanchor_weight_histogram": dict(sorted(nonanchor_weight_histogram.items())),
        "V_equals_one_boundary_controls": boundary_v_one_count,
        "generic_V_controls": generic_v_count,
        "generic_b_eq_G_minus_H_failures": generic_naive_identity_failures,
        "wrong_exchange_orientation_rejections": wrong_exchange_coefficient_failures,
        "wrong_basis_sign_rejections": wrong_basis_sign_failures,
        "wrong_swapped_basis_rejections": wrong_swapped_basis_failures,
        "wrong_received_orientation_rejections": wrong_received_orientation_failures,
    }
    hostile: dict[str, object] = {
        "generic_V_route_cut_witness": first_generic_witness,
        "weakened_H_gate_witness": first_weak_h_witness,
        "nonmonic_representation_witness": first_nonmonic_duplicate,
        "gcd_omission_witness": first_gcd_omission_witness,
        "zero_b_anchor_duplicate_witness": first_zero_b_anchor_duplicate,
        "degree_gate_witness": first_degree_gate_witness,
        "wrong_modulus_control": "(W,N)=(0,L0) lies in the mod-L0 relaxation but not M_U mod T",
        "wrong_exchange_orientation": (
            "alpha=G,beta=b produces a module element, not the exact pair; "
            "the exact coefficients are alpha=(G-bV)/H,beta=b(L0/H)"
        ),
    }
    return summary, hostile


def run_m31_arithmetic() -> dict[str, object]:
    p = 2**31 - 1
    n = 2**21
    k = 2**20
    agreement = 1_116_023
    radius = n - agreement
    j0 = radius
    s0 = n - j0
    w0 = s0 - k
    w = agreement - k
    t = radius - j0
    b_star = p**4 // 2**100
    forbidden = b_star + 1

    require(p == 2_147_483_647, "M31 prime arithmetic")
    require(radius == 981_129, "M31 radius")
    require(s0 == agreement, "M31 anchor agreement size")
    require(w0 == 67_447, "M31 w0")
    require(t == 0 and w0 == w + t, "M31 slack identity w0=w+t")
    require(b_star == 16_777_215 and forbidden == 16_777_216, "M31 list threshold")
    require(forbidden < p**4, "M31 fresh-symbol strict field slack")

    g_min = w0 + 1
    g_max = radius
    min_b_dimension = g_min - w0
    max_b_dimension = g_max - w0
    max_codeword_degree = (s0 - g_min) + (min_b_dimension - 1)
    require(max_codeword_degree == k - 1, "M31 reconstructed degree endpoint")
    require(g_min - t == w + 1, "M31 slack-normal m floor")

    # In the exact boundary-to-boundary companion, j=j0=R forces h=g.
    # For V=1, deg b<g and monicity then force H=G-b and b=G-H.
    # For arbitrary V (deg V<j0), bV may have degree far above g, so this
    # divisor-pair simplification is unavailable without a new theorem.
    max_deg_bv_minus_g = (g_max - w0 - 1) + (j0 - 1) - g_max
    require(max_deg_bv_minus_g == radius - w0 - 2 == 913_680, "generic V degree excess")

    return {
        "p": p,
        "n": n,
        "K": k,
        "agreement": agreement,
        "R": radius,
        "anchor_j0": j0,
        "anchor_s0": s0,
        "w0": w0,
        "w": w,
        "t": t,
        "B_star": b_star,
        "forbidden_list_size": forbidden,
        "fresh_symbol_margin": p**4 - forbidden,
        "boundary_anchor_reduction": (
            "a forbidden sublist of B_star+1 codewords can be retained while "
            "forcing one selected codeword to exact radius R"
        ),
        "remaining_census_quantifier": "BOUNDARY_ANCHORS_t=0_WITH_ARBITRARY_UNIT_V",
        "exchange_g_range": [g_min, g_max],
        "exchange_m_range": [g_min - t, g_max - t],
        "b_coefficient_dimension_range": [min_b_dimension, max_b_dimension],
        "max_reconstructed_codeword_degree": max_codeword_degree,
        "generic_V_possible_degree_excess_over_g": max_deg_bv_minus_g,
        "boundary_companion": "j=j0=R implies h=g",
        "V_equals_one_only": "H=G-b and b=G-H",
        "generic_unit_V_route_cut": (
            "the stated degree hypotheses leave deg(bV) above g, so h=g does not imply "
            "G-bV=H or b=G-H; "
            "the full corrected-module pair (G,b,V,H) must be retained"
        ),
        "ledger_movement": 0,
    }


def build_result() -> dict[str, object]:
    toy, hostile = run_toy_fixture()
    boundary = run_boundary_forcing_fixture()
    m31 = run_m31_arithmetic()
    return {
        "architecture": "M31_ALL_WEIGHT_ANCHOR_EXCHANGE_PADE_BIJECTION_V1",
        "status": "EXACT_FINITE_CONTROL_AND_M31_GENERIC_UNIT_V_DEGREE_ROUTE_CUT",
        "toy_exhaustive_control": toy,
        "boundary_forcing_control": boundary,
        "m31_exact_arithmetic": m31,
        "hostile_controls": hostile,
        "nonclaims": [
            "The GF(7) exhaustive fixture is not an asymptotic proof.",
            "This checker does not bound the number of admissible (G,b) pairs at M31.",
            "This checker does not assign U_Q, U_list-int, U_ext, or U_new.",
            "This checker does not pay the cross-weight v4 residual or close the M31 row.",
            "The V=1 divisor-pair identity is not asserted for a generic unit V.",
        ],
    }


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run all exact checks (default)")
    parser.add_argument("--json-summary", action="store_true", help="print the deterministic summary as JSON")
    parser.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="run all checks and print the hostile-control summary",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        result = build_result()
        if args.json_summary:
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        elif args.tamper_selftest:
            print("M31 all-weight anchor-exchange Pade bijection hostile controls: PASS")
            print(json.dumps(result["hostile_controls"], sort_keys=True, separators=(",", ":")))
        else:
            toy = result["toy_exhaustive_control"]
            m31 = result["m31_exact_arithmetic"]
            print("M31 all-weight anchor-exchange Pade bijection: PASS")
            print(
                "toy: "
                f"{toy['E0_supports']} E0 supports * "
                f"{toy['unit_V_tables_per_E0']} unit V tables * "
                f"{toy['codewords_per_configuration']} codewords = "
                f"{toy['exhaustive_code_checks']} exact code checks"
            )
            print(
                f"bijection: {toy['nonanchor_incidences']} nonanchor incidences; "
                f"{toy['admitted_exchange_pairs']} independently admitted pairs"
            )
            print(
                "M31 route cut: the generic-unit-V degree budget leaves deg(bV)-g up to "
                f"{m31['generic_V_possible_degree_excess_over_g']}; "
                "the V=1 identity b=G-H cannot be generalized"
            )
            print(
                "boundary forcing: B_star+1<q reduces the closing census to t=0 "
                "with arbitrary unit V"
            )
            print("ledger movement: 0; global M31 LIST row remains open")
        return 0
    except (CheckFailure, AssertionError, ValueError) as exc:
        print(f"M31 all-weight anchor-exchange Pade bijection: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
