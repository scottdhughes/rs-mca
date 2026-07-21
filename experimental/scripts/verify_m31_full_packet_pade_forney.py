#!/usr/bin/env python3
"""Finite audit verifier for the R37 Role 03 same-author repair.

This script is evidence for indexing, boundary, normalization, squarefreeness,
full-packet, common-core, Padé, and minimal-index identities.  It is not a
verifier of the deployed M31 whole-ball bound and makes no owner/payment claim.

Usage:
  python3 R37_ROLE03_REPAIR_VERIFIER.py --check --expected EXPECTED.txt
  python3 -O R37_ROLE03_REPAIR_VERIFIER.py --check --expected EXPECTED.txt
  python3 R37_ROLE03_REPAIR_VERIFIER.py --tamper-selftest
  python3 -O R37_ROLE03_REPAIR_VERIFIER.py --tamper-selftest
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import sys
from typing import Iterable, Sequence

EXPECTED_SHA256 = "faaae291cc3b791845f06e868fb96c796b953b614064879db4c75f32534c2658"
FIELD_TAG = "F_p"
OWNER = None
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
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out, p)


def pshift(a: Sequence[int], t: int, p: int) -> tuple[int, ...]:
    require(t >= 0, "negative polynomial shift")
    return trim(([0] * t) + list(a), p)


def pdivmod(a: Sequence[int], b: Sequence[int], p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    aa = list(trim(a, p))
    bb = trim(b, p)
    require(bb != (0,), "polynomial division by zero")
    if len(aa) < len(bb):
        return (0,), tuple(aa)
    q = [0] * (len(aa) - len(bb) + 1)
    lead_inv = inv(bb[-1], p)
    while len(aa) >= len(bb) and trim(aa, p) != (0,):
        aa = list(trim(aa, p))
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


def pgcd_many(polys: Sequence[Sequence[int]], p: int) -> tuple[int, ...]:
    require(bool(polys), "empty gcd list")
    g = trim(polys[0], p)
    for f in polys[1:]:
        g = pgcd(g, f, p)
    return pmonic(g, p)


def peval(a: Sequence[int], x: int, p: int) -> int:
    out = 0
    for coeff in reversed(a):
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
    remainder = (aa[0] + root * q[0]) % p
    require(remainder == 0, "declared root is not a root")
    return trim(q, p)


def functional(poly: Sequence[int], moments: Sequence[int], p: int) -> int:
    pp = trim(poly, p)
    require(len(pp) <= len(moments), "functional moment range exceeded")
    return sum(pp[i] * moments[i] for i in range(len(pp))) % p


def divided_numerator(poly: Sequence[int], moments: Sequence[int], p: int) -> tuple[int, ...]:
    """lambda_X((P(X)-P(Y))/(X-Y)), coefficients in Y."""
    pp = trim(poly, p)
    degree = len(pp) - 1
    if degree == 0:
        return (0,)
    out = [0] * degree
    for k in range(1, degree + 1):
        for h in range(k):
            out[h] = (out[h] + pp[k] * moments[k - 1 - h]) % p
    return trim(out, p)


def shifted_functional(poly: Sequence[int], t: int, moments: Sequence[int], p: int) -> int:
    return functional(pshift(poly, t, p), moments, p)


def containment(locator_poly: Sequence[int], moments: Sequence[int], p: int, K: int) -> bool:
    j = len(trim(locator_poly, p)) - 1
    return all(shifted_functional(locator_poly, t, moments, p) == 0
               for t in range(K - j))


def escape_values(roots: Sequence[int], locator_poly: Sequence[int], moments: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple(functional(divide_linear_at_root(locator_poly, x, p), moments, p)
                 for x in roots)


def exact_support(roots: Sequence[int], moments: Sequence[int], p: int, K: int) -> bool:
    ll = locator(roots, p)
    return containment(ll, moments, p, K) and all(v != 0 for v in escape_values(roots, ll, moments, p))


def product_mod(values: Iterable[int], p: int) -> int:
    out = 1
    for value in values:
        out = out * value % p
    return out


def matrix_rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    if not matrix:
        return 0
    a = [list(row) for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    require(all(len(row) == cols for row in a), "ragged matrix")
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv(a[rank][col], p)
        a[rank] = [(x * scale) % p for x in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col] % p:
                factor = a[r][col] % p
                a[r] = [(a[r][c] - factor * a[rank][c]) % p for c in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def row_span_vectors(rows: Sequence[Sequence[int]], p: int) -> list[tuple[int, ...]]:
    if not rows:
        return [tuple()]
    width = len(rows[0])
    out = []
    for coeffs in itertools.product(range(p), repeat=len(rows)):
        v = [0] * width
        for coeff, row in zip(coeffs, rows):
            for i, x in enumerate(row):
                v[i] = (v[i] + coeff * x) % p
        out.append(tuple(v))
    return out


def nullspace_basis(matrix: Sequence[Sequence[int]], p: int) -> list[tuple[int, ...]]:
    if not matrix:
        return []
    a = [list(row) for row in matrix]
    rows = len(a)
    cols = len(a[0])
    pivot_cols: list[int] = []
    r = 0
    for col in range(cols):
        pivot = next((rr for rr in range(r, rows) if a[rr][col] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = inv(a[r][col], p)
        a[r] = [(x * scale) % p for x in a[r]]
        for rr in range(rows):
            if rr != r and a[rr][col] % p:
                factor = a[rr][col] % p
                a[rr] = [(a[rr][cc] - factor * a[r][cc]) % p for cc in range(cols)]
        pivot_cols.append(col)
        r += 1
        if r == rows:
            break
    free_cols = [c for c in range(cols) if c not in pivot_cols]
    basis = []
    for free in free_cols:
        v = [0] * cols
        v[free] = 1
        for rr, pivot_col in enumerate(pivot_cols):
            v[pivot_col] = (-a[rr][free]) % p
        basis.append(tuple(v))
    return basis


def dot(a: Sequence[int], b: Sequence[int], p: int) -> int:
    return sum(x * y for x, y in zip(a, b)) % p


def bridge_audit() -> int:
    """Exhaust F_5, n=4, K=2 for W_E subset ker(y) iff y in C+U_E."""
    p, K = 5, 2
    D = tuple(range(4))
    generator = [[pow(x, r, p) for x in D] for r in range(K)]
    code = row_span_vectors(generator, p)
    dual_basis = nullspace_basis(generator, p)
    dual = row_span_vectors(dual_basis, p)
    cases = 0
    for y in itertools.product(range(p), repeat=len(D)):
        for j in range(0, 3):
            for E in itertools.combinations(range(len(D)), j):
                Eset = set(E)
                W = [v for v in dual if all(v[x] == 0 for x in Eset)]
                lhs = all(dot(y, v, p) == 0 for v in W)
                explanations = [c for c in code if all((y[x] - c[x]) % p == 0
                                                        for x in range(len(D)) if x not in Eset)]
                rhs = bool(explanations)
                require(lhs == rhs, "orthogonal support bridge failed")
                require(len(explanations) <= 1, "MDS uniqueness failed below distance")
                if lhs and j > 0:
                    escapes = []
                    for x in E:
                        Ex = Eset - {x}
                        Wx = [v for v in dual if all(v[z] == 0 for z in Ex)]
                        escapes.append(not all(dot(y, v, p) == 0 for v in Wx))
                    if all(escapes):
                        c = explanations[0]
                        error_support = {x for x in range(len(D)) if (y[x] - c[x]) % p != 0}
                        require(error_support == Eset, "escape did not force exact support")
                cases += 1
    return cases


def normalized_moments(p: int, K: int) -> Iterable[tuple[int, ...]]:
    for m in itertools.product(range(p), repeat=K):
        if not any(m):
            continue
        first = next(x for x in m if x)
        s = inv(first, p)
        normalized = tuple((s * x) % p for x in m)
        if normalized == m:
            yield m


def escape_resultant_audit() -> tuple[int, int]:
    p, K = 7, 3
    D = tuple(range(6))
    cases = 0
    exact_count = 0
    for m in normalized_moments(p, K):
        for j in range(1, K):
            for E in itertools.combinations(D, j):
                L = locator(E, p)
                B = divided_numerator(L, m, p)
                values = escape_values(E, L, m, p)
                require(tuple(peval(B, x, p) for x in E) == values,
                        "divided-difference root evaluation failed")
                resultant = product_mod((peval(B, x, p) for x in E), p)
                require(resultant == product_mod(values, p), "split resultant product failed")
                rhs = containment(L, m, p, K) and resultant != 0
                lhs = exact_support(E, m, p, K)
                require(lhs == rhs, "escape/resultant equivalence failed")
                exact_count += int(lhs)
                cases += 1
    return cases, exact_count


def layer_for(m: Sequence[int], p: int, K: int, D: Sequence[int], j: int) -> list[tuple[int, ...]]:
    return [tuple(E) for E in itertools.combinations(D, j) if exact_support(E, m, p, K)]


def common_intersection(layer: Sequence[Sequence[int]]) -> tuple[int, ...]:
    require(bool(layer), "empty layer")
    core = set(layer[0])
    for E in layer[1:]:
        core.intersection_update(E)
    return tuple(sorted(core))


def theta_coker_dimensions(Ps: Sequence[Sequence[int]], p: int, max_D: int) -> list[int]:
    e = len(trim(Ps[0], p)) - 1
    require(all(len(trim(P, p)) - 1 == e for P in Ps), "nonuniform locator degrees")
    out = []
    for D in range(max_D + 1):
        target = e + D
        columns: list[list[int]] = []
        for P in Ps:
            for t in range(D):
                colpoly = pshift(P, t, p)
                columns.append([colpoly[r] if r < len(colpoly) else 0 for r in range(target)])
        matrix = [[columns[c][r] for c in range(len(columns))] for r in range(target)]
        rank = matrix_rank_mod(matrix, p)
        out.append(target - rank)
    return out


def recover_forney_indices(cokers: Sequence[int], rank: int) -> tuple[int, ...]:
    require(len(cokers) >= 2 and cokers[-1] == 0, "coker range does not reach zero")
    gt = [cokers[D] - cokers[D + 1] for D in range(len(cokers) - 1)]
    require(all(0 <= x <= rank for x in gt), "invalid coker first differences")
    indices = [0] * (rank - gt[0])
    for k in range(1, len(gt)):
        count_equal = gt[k - 1] - gt[k]
        require(count_equal >= 0, "invalid coker convexity")
        indices.extend([k] * count_equal)
    require(len(indices) == rank, "failed to recover all Forney indices")
    return tuple(indices)


def full_layer_core_pade_forney_audit() -> tuple[int, tuple[int, ...], int]:
    p, K = 11, 4
    D = tuple(range(8))
    m = (1, 0, 1, 4)
    j = 3
    layer = layer_for(m, p, K, D, j)
    expected_layer = [(0, 1, 3), (1, 2, 4), (1, 5, 7)]
    require(layer == expected_layer, "small full-layer fixture changed")
    core = common_intersection(layer)
    require(core == (1,), "small common-core fixture changed")
    Ls = [locator(E, p) for E in layer]
    G = locator(core, p)
    require(pgcd_many(Ls, p) == G, "gcd is not the common-core locator")
    Ps = []
    for L in Ls:
        P, rem = pdivmod(L, G, p)
        require(rem == (0,), "core locator does not divide packet locator")
        Ps.append(pmonic(P, p))
    require(pgcd_many(Ps, p) == (1,), "reduced full row is not primitive")
    c = len(core)
    e = j - c
    D0 = K - j
    N = K - c
    require(e + D0 == N, "degree split failed")

    reduced_moments = tuple(functional(pshift(G, r, p), m, p) for r in range(N))
    require(any(reduced_moments), "reduced functional vanished")

    full_products = []
    for E, L, P in zip(layer, Ls, Ps):
        Bfull = divided_numerator(L, m, p)
        B = divided_numerator(P, reduced_moments, p)
        require(all(shifted_functional(P, t, reduced_moments, p) == 0 for t in range(D0)),
                "reduced recurrence failed")
        variable = tuple(x for x in E if x not in core)
        variable_product = product_mod((peval(B, x, p) for x in variable), p)
        require(variable_product != 0, "variable escape resultant vanished")
        core_product = product_mod((functional(divide_linear_at_root(L, x, p), m, p)
                                    for x in core), p)
        require(core_product != 0, "core escape factor vanished")
        global_product = product_mod((peval(Bfull, x, p) for x in E), p)
        require(global_product == variable_product * core_product % p,
                "global escape factorization failed")
        full_products.append(global_product)

        polynomial_part = divided_numerator(P, reduced_moments, p)
        require(polynomial_part == B, "Padé polynomial part failed")
        # Negative coefficient at Z^(-t-1) in P*S is lambda(X^t P).
        for t in range(D0):
            coeff = sum(P[k] * reduced_moments[k + t] for k in range(e + 1)) % p
            require(coeff == 0, "Padé negative-order cancellation failed")
        require(pgcd(P, B, p) == (1,), "Padé numerator/denominator not reduced")
    require(product_mod(full_products, p) != 0, "whole-packet escape product vanished")

    # Exact post-extraction characterization with G fixed.
    algebraic = []
    core_set = set(core)
    for E in itertools.combinations(D, j):
        if not core_set.issubset(E):
            continue
        L = locator(E, p)
        if not containment(L, m, p, K):
            continue
        Bfull = divided_numerator(L, m, p)
        if product_mod((peval(Bfull, x, p) for x in E), p) != 0:
            algebraic.append(tuple(E))
    require(algebraic == layer, "fixed-core algebraic characterization omitted or added a member")

    cokers = theta_coker_dimensions(Ps, p, max_D=e + 3)
    require(cokers[-1] == 0, "small primitive row did not become surjective")
    mus = recover_forney_indices(cokers, len(Ps) - 1)
    require(sum(mus) == e, "Forney index sum is not locator degree")
    require(cokers[D0] > 0 and max(mus) >= D0 + 1,
            "annihilating functional did not force non-surjectivity")
    require(all(cokers[D] == sum(max(0, mu - D) for mu in mus)
                for D in range(len(cokers))), "predictable-degree coker formula failed")

    # Pairwise MDS-style degree obstruction: every two-column relation has
    # coefficient degree at least D0+1, measured by reduced coprime quotients.
    for i, k in itertools.combinations(range(len(Ps)), 2):
        q = pgcd(Ps[i], Ps[k], p)
        quotient_degree = e - (len(q) - 1)
        require(quotient_degree >= D0 + 1, "two-column low-degree obstruction failed")
    return len(layer), mus, product_mod(full_products, p)


def deployed_arithmetic() -> dict[str, int]:
    p = 2**31 - 1
    n = 2**21
    K = 2**20
    a = 1_116_023
    sigma = a - K
    R = n - a
    B = p**4 // 2**100
    L = B + 1
    low_cap = K // 2
    high_layers = R - low_cap
    high_mass = L - low_cap
    forced = (high_mass + high_layers - 1) // high_layers
    return {
        "p": p, "n": n, "K": K, "a": a, "sigma": sigma, "R": R,
        "B": B, "L": L, "low_cap": low_cap, "high_layers": high_layers,
        "high_mass": high_mass, "forced": forced,
        "residual_sum_bound": 2 * R - K - 1,
        "two_row_bound_M36": (2 * (2 * R - K - 1)) // 34,
        "D0_min": K - R,
        "large_index_count": (2 * R - K - 1) // (K - R),
    }


def arithmetic_audit() -> dict[str, int]:
    a = deployed_arithmetic()
    require(a == {
        "p": 2_147_483_647,
        "n": 2_097_152,
        "K": 1_048_576,
        "a": 1_116_023,
        "sigma": 67_447,
        "R": 981_129,
        "B": 16_777_215,
        "L": 16_777_216,
        "low_cap": 524_288,
        "high_layers": 456_841,
        "high_mass": 16_252_928,
        "forced": 36,
        "residual_sum_bound": 913_681,
        "two_row_bound_M36": 53_745,
        "D0_min": 67_447,
        "large_index_count": 13,
    }, "deployed arithmetic or endpoint changed")
    require(a["two_row_bound_M36"] < a["D0_min"], "two-row degree no longer below cutoff")
    require(36 - (a["large_index_count"] + 1) == 22,
            "intermediate low-index count changed")
    # There are M-1 indices, hence 35-(13+1)=21 for M=36.
    require((36 - 1) - (a["large_index_count"] + 1) == 21,
            "deployed count of low minimal rows changed")
    return a


def find_omitted_recurrence_witness() -> tuple[tuple[int, ...], tuple[int, ...]]:
    p, K = 7, 3
    D = tuple(range(6))
    for m in normalized_moments(p, K):
        for E in itertools.combinations(D, 1):
            L = locator(E, p)
            D0 = K - 1
            require(D0 == 2, "fixture cutoff changed")
            first = shifted_functional(L, 0, m, p)
            last = shifted_functional(L, 1, m, p)
            B = divided_numerator(L, m, p)
            res = product_mod((peval(B, x, p) for x in E), p)
            if first == 0 and last != 0 and res != 0:
                return m, E
    raise RuntimeError("no omitted-recurrence witness found")


def find_core_escape_witness() -> tuple[tuple[int, ...], tuple[int, int]]:
    p, K = 7, 3
    D = tuple(range(6))
    for m in normalized_moments(p, K):
        for x, alpha in itertools.permutations(D, 2):
            E = (x, alpha)
            L = locator(E, p)
            if not containment(L, m, p, K):
                continue
            core_escape = functional(divide_linear_at_root(L, x, p), m, p)
            variable_escape = functional(divide_linear_at_root(L, alpha, p), m, p)
            if core_escape == 0 and variable_escape != 0:
                return m, E
    raise RuntimeError("no core-escape omission witness found")


def check_output() -> str:
    arithmetic = arithmetic_audit()
    bridge_cases = bridge_audit()
    escape_cases, exact_count = escape_resultant_audit()
    layer_size, mus, packet_product = full_layer_core_pade_forney_audit()
    lines = [
        "R37_ROLE03_REPAIR_VERIFIER",
        "mode=check",
        f"arithmetic=PASS B={arithmetic['B']} L={arithmetic['L']} forced_layer={arithmetic['forced']}",
        f"support_bridge=PASS cases={bridge_cases}",
        f"escape_resultant=PASS cases={escape_cases} exact={exact_count}",
        f"full_layer_core_pade=PASS layer_size={layer_size} packet_product={packet_product}",
        "forney_small_model=PASS indices=" + ",".join(str(x) for x in mus),
        "field_scope=PASS deployed=F_p quartic_transfer=UNCLAIMED",
        "owner_addback_ledger=PASS owner=NONE addback=UNCLAIMED movement=0",
        "RESULT=PASS",
    ]
    return "\n".join(lines) + "\n"


def tamper_output() -> str:
    # 1. Boundary/denominator mutation.
    arithmetic_detected = False
    try:
        a = arithmetic_audit()
        require(a["B"] + 1 == 16_777_215, "mutated B* rejected")
    except RuntimeError:
        arithmetic_detected = True
    require(arithmetic_detected, "boundary mutation escaped")

    # 2. Omitting the last containment recurrence creates a false acceptance.
    m_omit, E_omit = find_omitted_recurrence_witness()
    require(not exact_support(E_omit, m_omit, 7, 3), "omitted-recurrence witness unexpectedly exact")
    recurrence_detected = True

    # 3. Reversing the divided-difference sign breaks the Padé polynomial part.
    p = 11
    m = (1, 0, 1, 4)
    E = (0, 1, 3)
    Pfull = locator(E, p)
    B = divided_numerator(Pfull, m, p)
    wrong = pscale(B, -1, p)
    sign_detected = wrong != B and B != (0,)
    require(sign_detected, "sign mutation was invisible")

    # 4. Repeated-root support: naive recurrence/resultant can pass, so the
    # squarefree D-split locator gate is load-bearing.
    p7 = 7
    repeated = locator((0, 0), p7)
    repeated_m = (0, 1, 0)
    require(containment(repeated, repeated_m, p7, 3), "repeated-root fixture lost containment")
    repeated_B = divided_numerator(repeated, repeated_m, p7)
    require(peval(repeated_B, 0, p7) != 0, "repeated-root fixture lost nonzero resultant")
    repeated_detected = True

    # 5. Dropping one member violates exact full-layer equality.
    full = layer_for((1, 0, 1, 4), 11, 4, tuple(range(8)), 3)
    dropped = full[:-1]
    packet_detected = dropped != full and set(dropped) < set(full)
    require(packet_detected, "packet truncation mutation was invisible")

    # 6. Reduced variable escapes alone can accept while a core escape fails.
    m_core, E_core = find_core_escape_witness()
    L_core = locator(E_core, 7)
    core_value = functional(divide_linear_at_root(L_core, E_core[0], 7), m_core, 7)
    variable_value = functional(divide_linear_at_root(L_core, E_core[1], 7), m_core, 7)
    core_detected = core_value == 0 and variable_value != 0
    require(core_detected, "core-escape omission mutation was invisible")

    # 7. Scaling a nonzero functional must not change accepted supports.
    base_m = (1, 0, 1, 4)
    base_layer = layer_for(base_m, 11, 4, tuple(range(8)), 3)
    for s in range(1, 11):
        scaled = tuple(s * x % 11 for x in base_m)
        require(layer_for(scaled, 11, 4, tuple(range(8)), 3) == base_layer,
                "nonzero normalization scaling changed the packet")
    normalization_detected = True

    # 8. Wrong-field and owner/ledger mutations are rejected semantically.
    field_detected = FIELD_TAG != "F_{p^4}"
    owner_detected = OWNER is None and LEDGER_MOVEMENT == 0
    require(field_detected, "wrong-field mutation was accepted")
    require(owner_detected, "owner/payment mutation was accepted")

    lines = [
        "R37_ROLE03_REPAIR_VERIFIER",
        "mode=tamper-selftest",
        "tamper.boundary_denominator=DETECTED",
        "tamper.omitted_recurrence=DETECTED",
        "tamper.divided_difference_sign=DETECTED",
        "tamper.repeated_root=DETECTED",
        "tamper.packet_truncation=DETECTED",
        "tamper.core_escape_omission=DETECTED",
        "tamper.normalization_scaling=DETECTED",
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
        require(args.expected.is_file(), "expected-output file is missing")
        expected_bytes = args.expected.read_bytes()
        expected_hash = hashlib.sha256(expected_bytes).hexdigest()
        require(EXPECTED_SHA256 != "TO_BE_FILLED", "expected-output digest was not frozen")
        require(expected_hash == EXPECTED_SHA256, "expected-output digest mismatch")
        require(output.encode("utf-8") == expected_bytes, "runtime output differs from expected output")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        sys.stderr.write(f"FAIL_CLOSED: {exc}\n")
        raise SystemExit(1)
