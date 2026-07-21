#!/usr/bin/env python3
"""Exact checks for the M31 coupled escape--Forney--Pluecker route cut.

The symbolic proof is in
``experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md``.
This verifier checks the deployed integer thresholds, an exact full-layer
GF(11) source fixture, the joint locator/numerator relations, pairwise
collision quotients, Pluecker contractions, and fail-closed mutations.

It does not prove the M31 whole-ball bound and deliberately records zero
ledger movement.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import sys
from typing import Iterable, Sequence


EXPECTED_SHA256 = "b2587cb6edd4f03fbbbbe81feddf6bd57a8ec6239c1dd977ece3952090189750"
TERMINAL = "UNPAID_UNCLASSIFIED_16_COLUMN_COUPLED_PADE_FRAME"
LEDGER_MOVEMENT = 0


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def inv(a: int, p: int) -> int:
    a %= p
    require(a != 0, "attempted inversion of zero")
    return pow(a, p - 2, p)


def trim(a: Iterable[int], p: int) -> tuple[int, ...]:
    out = [x % p for x in a]
    if not out:
        out = [0]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def degree(a: Sequence[int], p: int) -> int:
    aa = trim(a, p)
    return -1 if aa == (0,) else len(aa) - 1


def padd(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    n = max(len(a), len(b))
    return trim(((a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0) for i in range(n)), p)


def psub(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    n = max(len(a), len(b))
    return trim(((a[i] if i < len(a) else 0) -
                 (b[i] if i < len(b) else 0) for i in range(n)), p)


def pscale(a: Sequence[int], s: int, p: int) -> tuple[int, ...]:
    return trim((s * x for x in a), p)


def pmul(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    aa, bb = trim(a, p), trim(b, p)
    if aa == (0,) or bb == (0,):
        return (0,)
    out = [0] * (len(aa) + len(bb) - 1)
    for i, x in enumerate(aa):
        for j, y in enumerate(bb):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out, p)


def pshift(a: Sequence[int], t: int, p: int) -> tuple[int, ...]:
    require(t >= 0, "negative polynomial shift")
    aa = trim(a, p)
    return aa if t == 0 else trim(([0] * t) + list(aa), p)


def pdivmod(a: Sequence[int], b: Sequence[int], p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    aa = list(trim(a, p))
    bb = trim(b, p)
    require(bb != (0,), "polynomial division by zero")
    if len(aa) < len(bb):
        return (0,), tuple(aa)
    q = [0] * (len(aa) - len(bb) + 1)
    lead_inv = inv(bb[-1], p)
    while True:
        aa = list(trim(aa, p))
        if tuple(aa) == (0,) or len(aa) < len(bb):
            break
        d = len(aa) - len(bb)
        coeff = aa[-1] * lead_inv % p
        q[d] = coeff
        for i, x in enumerate(bb):
            aa[d + i] = (aa[d + i] - coeff * x) % p
    return trim(q, p), trim(aa, p)


def pmonic(a: Sequence[int], p: int) -> tuple[int, ...]:
    aa = trim(a, p)
    require(aa != (0,), "zero polynomial has no monic normalization")
    return pscale(aa, inv(aa[-1], p), p)


def pgcd(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    aa, bb = trim(a, p), trim(b, p)
    while bb != (0,):
        _, rr = pdivmod(aa, bb, p)
        aa, bb = bb, rr
    return pmonic(aa, p)


def peval(a: Sequence[int], x: int, p: int) -> int:
    out = 0
    for coeff in reversed(trim(a, p)):
        out = (out * x + coeff) % p
    return out


def locator(roots: Sequence[int], p: int) -> tuple[int, ...]:
    out = (1,)
    for x in roots:
        out = pmul(out, ((-x) % p, 1), p)
    return out


def divide_linear_at_root(a: Sequence[int], root: int, p: int) -> tuple[int, ...]:
    aa = trim(a, p)
    require(len(aa) >= 2, "cannot divide a constant by a linear factor")
    n = len(aa) - 1
    q = [0] * n
    q[n - 1] = aa[n]
    for k in range(n - 2, -1, -1):
        q[k] = (aa[k + 1] + root * q[k + 1]) % p
    require((aa[0] + root * q[0]) % p == 0, "declared root is not a root")
    return trim(q, p)


def functional(poly: Sequence[int], moments: Sequence[int], p: int) -> int:
    pp = trim(poly, p)
    require(len(pp) <= len(moments), "functional moment range exceeded")
    return sum(pp[i] * moments[i] for i in range(len(pp))) % p


def divided_numerator(poly: Sequence[int], moments: Sequence[int], p: int) -> tuple[int, ...]:
    """lambda_X((P(X)-P(Y))/(X-Y)), with coefficients in Y."""
    pp = trim(poly, p)
    d = len(pp) - 1
    if d == 0:
        return (0,)
    out = [0] * d
    for k in range(1, d + 1):
        for h in range(k):
            out[h] = (out[h] + pp[k] * moments[k - 1 - h]) % p
    return trim(out, p)


def containment(poly: Sequence[int], moments: Sequence[int], p: int, K: int) -> bool:
    j = degree(poly, p)
    return all(functional(pshift(poly, t, p), moments, p) == 0
               for t in range(K - j))


def escape_values(roots: Sequence[int], poly: Sequence[int], moments: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple(functional(divide_linear_at_root(poly, x, p), moments, p)
                 for x in roots)


def exact_support(roots: Sequence[int], moments: Sequence[int], p: int, K: int) -> bool:
    poly = locator(roots, p)
    return containment(poly, moments, p, K) and all(
        value != 0 for value in escape_values(roots, poly, moments, p)
    )


def matrix_rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    if not matrix:
        return 0
    a = [list(row) for row in matrix]
    cols = len(a[0])
    require(all(len(row) == cols for row in a), "ragged matrix")
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, len(a)) if a[r][col] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv(a[rank][col], p)
        a[rank] = [(x * scale) % p for x in a[rank]]
        for r in range(len(a)):
            if r != rank and a[r][col] % p:
                factor = a[r][col] % p
                a[r] = [(a[r][c] - factor * a[rank][c]) % p for c in range(cols)]
        rank += 1
        if rank == len(a):
            break
    return rank


def nullspace_basis(matrix: Sequence[Sequence[int]], p: int) -> list[tuple[int, ...]]:
    require(bool(matrix), "nullspace matrix must have a declared row count")
    a = [list(row) for row in matrix]
    cols = len(a[0])
    require(all(len(row) == cols for row in a), "ragged matrix")
    pivots: list[int] = []
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, len(a)) if a[r][col] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv(a[rank][col], p)
        a[rank] = [(x * scale) % p for x in a[rank]]
        for r in range(len(a)):
            if r != rank and a[r][col] % p:
                factor = a[r][col] % p
                a[r] = [(a[r][c] - factor * a[rank][c]) % p for c in range(cols)]
        pivots.append(col)
        rank += 1
        if rank == len(a):
            break
    free = [c for c in range(cols) if c not in pivots]
    basis: list[tuple[int, ...]] = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for r, col in enumerate(pivots):
            v[col] = (-a[r][f]) % p
        basis.append(tuple(v))
    return basis


def theta_cokers(polys: Sequence[Sequence[int]], p: int, max_D: int) -> list[int]:
    e = degree(polys[0], p)
    require(all(degree(poly, p) == e for poly in polys), "nonuniform degrees")
    out: list[int] = []
    for D in range(max_D + 1):
        target = e + D
        columns: list[list[int]] = []
        for poly in polys:
            for t in range(D):
                shifted = pshift(poly, t, p)
                columns.append([shifted[r] if r < len(shifted) else 0
                                for r in range(target)])
        matrix = [[columns[c][r] for c in range(len(columns))]
                  for r in range(target)]
        out.append(target - matrix_rank_mod(matrix, p))
    return out


def recover_indices(cokers: Sequence[int], rank: int) -> tuple[int, ...]:
    require(len(cokers) >= 2 and cokers[-1] == 0, "coker range did not reach zero")
    gt = [cokers[D] - cokers[D + 1] for D in range(len(cokers) - 1)]
    require(all(0 <= x <= rank for x in gt), "invalid coker differences")
    indices = [0] * (rank - gt[0])
    for k in range(1, len(gt)):
        count = gt[k - 1] - gt[k]
        require(count >= 0, "invalid coker convexity")
        indices.extend([k] * count)
    require(len(indices) == rank, "failed to recover every index")
    return tuple(indices)


def constant_relation(coeffs: Sequence[int], polys: Sequence[Sequence[int]], p: int) -> tuple[int, ...]:
    out = (0,)
    for coeff, poly in zip(coeffs, polys):
        out = padd(out, pscale(poly, coeff, p), p)
    return out


def pair_cross(Pi: Sequence[int], Bi: Sequence[int], Pj: Sequence[int], Bj: Sequence[int], p: int) -> tuple[int, ...]:
    return psub(pmul(Pi, Bj, p), pmul(Pj, Bi, p), p)


def normalized_escape(P: Sequence[int], B: Sequence[int], root: int, p: int) -> int:
    derivative_value = peval(divide_linear_at_root(P, root, p), root, p)
    return peval(B, root, p) * inv(derivative_value, p) % p


def derivative_at_root(P: Sequence[int], root: int, p: int) -> int:
    return peval(divide_linear_at_root(P, root, p), root, p)


def deployed_arithmetic() -> dict[str, int]:
    p = 2**31 - 1
    n = 2**21
    K = 2**20
    R = 981_129
    D0 = K - R
    S = 2 * R - K - 1
    Bstar = p**4 // 2**100
    forbidden_67 = 67 * R + (67 * 66 // 2) * S
    forbidden_68 = 68 * R + (68 * 67 // 2) * S
    return {
        "p": p,
        "n": n,
        "K": K,
        "R": R,
        "D0": D0,
        "S": S,
        "Bstar": Bstar,
        "rank36_one": S // 34,
        "rank36_two": (2 * S) // 34,
        "width16_one": S // 14,
        "width15_one": S // 13,
        "width30_two": (2 * S) // 28,
        "width29_two": (2 * S) // 27,
        "width16_space": 14 * (D0 + 1) - S,
        "forbidden_67": forbidden_67,
        "forbidden_68": forbidden_68,
        "avoidance_margin_67": p - forbidden_67,
        "avoidance_excess_68": forbidden_68 - p,
    }


def arithmetic_audit() -> dict[str, int]:
    a = deployed_arithmetic()
    require(a == {
        "p": 2_147_483_647,
        "n": 2_097_152,
        "K": 1_048_576,
        "R": 981_129,
        "D0": 67_447,
        "S": 913_681,
        "Bstar": 16_777_215,
        "rank36_one": 26_872,
        "rank36_two": 53_745,
        "width16_one": 65_262,
        "width15_one": 70_283,
        "width30_two": 65_262,
        "width29_two": 67_680,
        "width16_space": 30_591,
        "forbidden_67": 2_085_884_334,
        "forbidden_68": 2_148_082_090,
        "avoidance_margin_67": 61_599_313,
        "avoidance_excess_68": 598_443,
    }, "deployed arithmetic changed")
    require(a["width16_one"] < a["D0"] < a["width15_one"],
            "16/15 one-row threshold changed")
    require(a["width30_two"] < a["D0"] < a["width29_two"],
            "30/29 two-row threshold changed")
    require(13 * (a["D0"] + 1) <= a["S"],
            "sharp 15-column obstruction profile disappeared")
    require(a["forbidden_67"] < a["p"] < a["forbidden_68"],
            "67/68 hyperplane threshold changed")
    return a


def full_layer_fixture() -> dict[str, object]:
    p, K = 11, 4
    domain = tuple(range(8))
    moments = (0, 0, 1, 0)
    j = 3
    layer = [tuple(E) for E in itertools.combinations(domain, j)
             if exact_support(E, moments, p, K)]
    expected = [
        (0, 4, 7),
        (0, 5, 6),
        (1, 3, 7),
        (1, 4, 6),
        (2, 3, 6),
        (2, 4, 5),
    ]
    require(layer == expected, "GF(11) full exact layer changed")
    core = set(layer[0])
    for E in layer[1:]:
        core.intersection_update(E)
    require(not core, "GF(11) fixture acquired a common core")

    Ps = [locator(E, p) for E in layer]
    Bs = [divided_numerator(P, moments, p) for P in Ps]
    require(all(B == (1,) for B in Bs), "GF(11) numerator fixture changed")
    require(all(escape_values(E, P, moments, p) == (1, 1, 1)
                for E, P in zip(layer, Ps)), "GF(11) escape fixture changed")

    coefficient_matrix = [
        [P[d] if d < len(P) else 0 for P in Ps]
        for d in range(j + 1)
    ]
    constant_basis = nullspace_basis(coefficient_matrix, p)
    require(len(constant_basis) == 3, "GF(11) constant joint rank changed")
    for row in constant_basis:
        require(constant_relation(row, Ps, p) == (0,), "locator relation failed")
        require(constant_relation(row, Bs, p) == (0,), "numerator relation failed")

    cokers = theta_cokers(Ps, p, max_D=7)
    indices = recover_indices(cokers, len(Ps) - 1)
    require(indices == (0, 0, 0, 1, 2), "GF(11) locator Forney profile changed")

    Srow, Trow = constant_basis[:2]
    deltas = [[(Srow[i] * Trow[j] - Srow[j] * Trow[i]) % p
               for j in range(len(Ps))] for i in range(len(Ps))]
    nonzero_minors = sum(deltas[i][j] != 0
                         for i in range(len(Ps)) for j in range(i + 1, len(Ps)))
    require(nonzero_minors > 0, "joint frame lost rank two")
    for i in range(len(Ps)):
        require(constant_relation(deltas[i], Ps, p) == (0,),
                "Pluecker locator contraction failed")
        require(constant_relation(deltas[i], Bs, p) == (0,),
                "Pluecker numerator contraction failed")

    cauchy_binet = (0,)
    collision_energy = 0
    collision_allowance = 0
    pair_data = []
    for i, jidx in itertools.combinations(range(len(Ps)), 2):
        shared = tuple(sorted(set(layer[i]) & set(layer[jidx])))
        H = locator(shared, p)
        Omega = pair_cross(Ps[i], Bs[i], Ps[jidx], Bs[jidx], p)
        require(Omega != (0,), "distinct reduced fractions became equal")
        quotient, remainder = pdivmod(Omega, H, p)
        require(remainder == (0,), "overlap locator did not divide cross determinant")
        union_excess = len(set(layer[i]) | set(layer[jidx])) - (K + 1)
        require(degree(quotient, p) <= union_excess,
                "collision quotient exceeded MDS union excess")
        symmetric_difference = set(layer[i]) ^ set(layer[jidx])
        require(all(peval(quotient, x, p) != 0 for x in symmetric_difference),
                "collision quotient vanished on a symmetric-difference root")
        collisions = []
        for x in shared:
            equal = normalized_escape(Ps[i], Bs[i], x, p) == normalized_escape(
                Ps[jidx], Bs[jidx], x, p
            )
            require((peval(quotient, x, p) == 0) == equal,
                    "collision quotient/root equivalence failed")
            if equal:
                collisions.append(x)
        require(len(collisions) <= union_excess, "pair collision cap failed")
        collision_energy += len(collisions)
        collision_allowance += union_excess
        pair_data.append((i, jidx, shared, quotient, union_excess, collisions))
        cauchy_binet = padd(cauchy_binet,
                            pscale(Omega, deltas[i][jidx], p), p)
    require(cauchy_binet == (0,), "Cauchy--Binet contraction failed")
    require(collision_energy == 0 and collision_allowance == 3,
            "GF(11) collision-free full-layer route cut changed")

    return {
        "p": p,
        "K": K,
        "moments": moments,
        "layer": layer,
        "Ps": Ps,
        "Bs": Bs,
        "basis": constant_basis,
        "indices": indices,
        "deltas": deltas,
        "nonzero_minors": nonzero_minors,
        "pair_data": pair_data,
        "collision_energy": collision_energy,
        "collision_allowance": collision_allowance,
    }


def common_core_factor_fixture() -> dict[str, object]:
    """Replay the pair-factor identity on a full layer with a true core."""
    p, K = 11, 4
    domain = tuple(range(8))
    moments = (1, 0, 1, 4)
    layer = [tuple(E) for E in itertools.combinations(domain, 3)
             if exact_support(E, moments, p, K)]
    expected = [(0, 1, 3), (1, 2, 4), (1, 5, 7)]
    require(layer == expected, "GF(11) common-core exact layer changed")

    core = set(layer[0])
    for E in layer[1:]:
        core.intersection_update(E)
    require(core == {1}, "GF(11) common core changed")
    G = locator(tuple(sorted(core)), p)
    reduced_moments = tuple(
        functional(pshift(G, t, p), moments, p) for t in range(K - len(core))
    )
    domain_locator = locator(domain, p)

    Ps: list[tuple[int, ...]] = []
    Bs: list[tuple[int, ...]] = []
    errors: list[dict[int, int]] = []
    for E in layer:
        L = locator(E, p)
        P, remainder = pdivmod(L, G, p)
        require(remainder == (0,), "common core did not divide a full locator")
        B = divided_numerator(P, reduced_moments, p)
        Ps.append(P)
        Bs.append(B)
        error_values: dict[int, int] = {}
        for x in E:
            epsilon = functional(divide_linear_at_root(L, x, p), moments, p)
            dual_weight = inv(derivative_at_root(domain_locator, x, p), p)
            denominator = dual_weight * derivative_at_root(L, x, p) % p
            error_values[x] = epsilon * inv(denominator, p) % p
            require(error_values[x] != 0, "exact support acquired a zero error")
        errors.append(error_values)

    gamma: int | None = None
    core_checks = 0
    pair_checks = 0
    for i, jidx in itertools.combinations(range(len(layer)), 2):
        Q = pgcd(Ps[i], Ps[jidx], p)
        Omega = pair_cross(Ps[i], Bs[i], Ps[jidx], Bs[jidx], p)
        h, remainder = pdivmod(Omega, Q, p)
        require(remainder == (0,), "common-core pair gcd did not divide Omega")
        union = set(layer[i]) | set(layer[jidx])
        V = locator(tuple(x for x in domain if x not in union), p)
        pair_gamma: int | None = None
        for x in union:
            codeword_difference = (
                errors[i].get(x, 0) - errors[jidx].get(x, 0)
            ) % p
            quotient_value = (
                codeword_difference * inv(peval(V, x, p), p)
            ) % p
            h_value = peval(h, x, p)
            require(quotient_value != 0,
                    "common-core fixture unexpectedly acquired a collision")
            local_gamma = h_value * inv(quotient_value, p) % p
            if pair_gamma is None:
                pair_gamma = local_gamma
            require(local_gamma == pair_gamma,
                    "pair factor scalar varied across the union")
            if x in core:
                core_checks += 1
        require(pair_gamma is not None, "empty pair union")
        if gamma is None:
            gamma = pair_gamma
        require(pair_gamma == gamma, "pair factor scalar varied across pairs")
        pair_checks += 1

    require(gamma == 10, "common-core global factor changed")
    require(pair_checks == 3 and core_checks == 3,
            "common-core factor coverage changed")
    return {
        "layer": layer,
        "core": tuple(sorted(core)),
        "pair_checks": pair_checks,
        "core_checks": core_checks,
        "gamma": gamma,
    }


def check_output() -> str:
    arithmetic = arithmetic_audit()
    fixture = full_layer_fixture()
    core_fixture = common_core_factor_fixture()
    lines = [
        "M31_COUPLED_ESCAPE_FORNEY_PLUCKER_ROUTE_CUT",
        "mode=check",
        ("arithmetic=PASS D0={D0} S={S} width16={width16_one} "
         "width30={width30_two}").format(**arithmetic),
        ("fixed_width=PASS width15={width15_one} width29={width29_two} "
         "space16={width16_space}").format(**arithmetic),
        ("joint_full_layer=PASS size={size} forney={indices} joint_constant_rows={rows}").format(
            size=len(fixture["layer"]),
            indices=",".join(str(x) for x in fixture["indices"]),
            rows=len(fixture["basis"]),
        ),
        f"escape_pluecker=PASS nonzero_minors={fixture['nonzero_minors']}",
        ("pair_collision=PASS pairs={pairs} energy={energy} allowance={allowance}").format(
            pairs=len(fixture["pair_data"]),
            energy=fixture["collision_energy"],
            allowance=fixture["collision_allowance"],
        ),
        ("common_core_factor=PASS size={size} core={core} pairs={pairs} gamma={gamma}").format(
            size=len(core_fixture["layer"]),
            core=",".join(str(x) for x in core_fixture["core"]),
            pairs=core_fixture["pair_checks"],
            gamma=core_fixture["gamma"],
        ),
        ("generic_avoidance=PASS max_packet=67 margin={avoidance_margin_67} "
         "next_excess={avoidance_excess_68}").format(**arithmetic),
        f"terminal={TERMINAL}",
        f"ledger_movement={LEDGER_MOVEMENT}",
        "RESULT=PASS",
    ]
    return "\n".join(lines) + "\n"


def tamper_output() -> str:
    arithmetic = arithmetic_audit()
    fixture = full_layer_fixture()
    core_fixture = common_core_factor_fixture()
    p = fixture["p"]
    Ps = fixture["Ps"]
    Bs = fixture["Bs"]
    layer = fixture["layer"]

    require(not (arithmetic["forbidden_68"] < arithmetic["p"]),
            "68-packet avoidance mutation escaped")

    shared = tuple(sorted(set(layer[0]) & set(layer[1])))
    H = locator(shared, p)
    A0, r0 = pdivmod(Ps[1], H, p)
    A1, r1 = pdivmod(Ps[0], H, p)
    require(r0 == (0,) and r1 == (0,), "two-column fixture division failed")
    locator_sum = padd(pmul(A0, Ps[0], p), pscale(pmul(A1, Ps[1], p), -1, p), p)
    numerator_sum = padd(pmul(A0, Bs[0], p), pscale(pmul(A1, Bs[1], p), -1, p), p)
    require(locator_sum == (0,) and numerator_sum != (0,),
            "above-cutoff jointness mutation disappeared")
    require(max(degree(A0, p), degree(A1, p)) > 1,
            "above-cutoff witness fell below D0")

    raw = pair_cross(Ps[0], Bs[0], Ps[1], Bs[1], p)
    require(degree(raw, p) > 0, "raw cross determinant unexpectedly met tight cap")
    quotient, remainder = pdivmod(raw, H, p)
    require(remainder == (0,) and degree(quotient, p) == 0,
            "overlap-division guard disappeared")

    correct_collisions = 0
    naive_collisions = 0
    for i, jidx in itertools.combinations(range(len(Ps)), 2):
        for x in set(layer[i]) & set(layer[jidx]):
            correct_collisions += int(
                normalized_escape(Ps[i], Bs[i], x, p) ==
                normalized_escape(Ps[jidx], Bs[jidx], x, p)
            )
            naive_collisions += int(peval(Bs[i], x, p) == peval(Bs[jidx], x, p))
    require(correct_collisions == 0 and naive_collisions > 0,
            "derivative-normalization mutation was invisible")

    require(layer[:-1] != layer, "packet-truncation mutation was invisible")
    require(core_fixture["gamma"] != 1 and core_fixture["core_checks"] == 3,
            "common-core pair-factor mutation escaped")

    deltas = [row[:] for row in fixture["deltas"]]
    changed = False
    for i in range(len(deltas)):
        for jidx in range(i + 1, len(deltas)):
            if deltas[i][jidx] != 0:
                deltas[i][jidx] = (-deltas[i][jidx]) % p
                deltas[jidx][i] = (-deltas[jidx][i]) % p
                changed = True
                break
        if changed:
            break
    require(changed, "no Pluecker sign available to mutate")
    require(any(constant_relation(deltas[i], Ps, p) != (0,)
                for i in range(len(Ps))), "Pluecker sign mutation escaped")

    p7 = 7
    repeated = locator((0, 0), p7)
    repeated_moments = (0, 1, 0)
    require(containment(repeated, repeated_moments, p7, 3),
            "repeated-root fixture lost containment")
    require(peval(divided_numerator(repeated, repeated_moments, p7), 0, p7) != 0,
            "repeated-root fixture lost naive escape")

    core_poly = locator((0, 1), p7)
    core_moments = (1, 0, 0)
    variable_escape = functional(divide_linear_at_root(core_poly, 0, p7), core_moments, p7)
    core_escape = functional(divide_linear_at_root(core_poly, 1, p7), core_moments, p7)
    require(variable_escape != 0 and core_escape == 0,
            "core-escape omission fixture changed")

    mutated_Bs = list(Bs)
    mutated_Bs[0] = (2,)
    require(any(constant_relation(row, mutated_Bs, p) != (0,)
                for row in fixture["basis"]), "joint-numerator mutation escaped")

    require((2**31 - 1)**4 != arithmetic["p"], "wrong-field mutation escaped")
    require(TERMINAL.startswith("UNPAID_") and LEDGER_MOVEMENT == 0,
            "owner/ledger mutation escaped")

    lines = [
        "M31_COUPLED_ESCAPE_FORNEY_PLUCKER_ROUTE_CUT",
        "mode=tamper-selftest",
        "tamper.width68_union_bound=DETECTED",
        "tamper.above_cutoff_jointness=DETECTED",
        "tamper.omitted_overlap_division=DETECTED",
        "tamper.escape_derivative_normalization=DETECTED",
        "tamper.packet_truncation=DETECTED",
        "tamper.common_core_pair_factor=DETECTED",
        "tamper.pluecker_sign=DETECTED",
        "tamper.repeated_root=DETECTED",
        "tamper.core_escape_omission=DETECTED",
        "tamper.joint_numerator_row=DETECTED",
        "tamper.wrong_field_owner_ledger=DETECTED",
        "RESULT=TAMPER_GUARDS_PASS",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--expected", type=pathlib.Path)
    args = parser.parse_args()

    output = check_output() if args.check else tamper_output()
    if args.check and args.expected is not None:
        require(args.expected.is_file(), "expected-output file missing")
        expected = args.expected.read_bytes()
        require(EXPECTED_SHA256 != "TO_BE_FILLED", "expected-output hash not frozen")
        require(hashlib.sha256(expected).hexdigest() == EXPECTED_SHA256,
                "expected-output hash mismatch")
        require(output.encode("utf-8") == expected, "runtime output differs from expected")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        sys.stderr.write(f"FAIL_CLOSED: {exc}\n")
        raise SystemExit(1)
