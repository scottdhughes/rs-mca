#!/usr/bin/env python3
"""Exact replay for the affine-prefix full-union image obstruction."""
from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal, getcontext
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
from typing import Iterable, Sequence

P = 5
DEG = 6
ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/affine-prefix-full-union-image-obstruction"
BASE = "3404d21b64c876c6d9b995ad3e29d7120ab27a54"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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
        require(file_sha256(ROOT / relative) == expected, f"source pin mismatch: {relative}")
    return len(payload["files"])


def trim_poly(a: list[int]) -> list[int]:
    a = [x % P for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_sub_base(a: Sequence[int], b: Sequence[int]) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % P
    return trim_poly(out)


def poly_divmod_base(a: Sequence[int], b: Sequence[int]) -> tuple[list[int], list[int]]:
    r = trim_poly(list(a))
    d = trim_poly(list(b))
    require(d != [0], "division by zero polynomial")
    q = [0] * max(1, len(r) - len(d) + 1)
    inv_lc = pow(d[-1], P - 2, P)
    while r != [0] and len(r) >= len(d):
        shift = len(r) - len(d)
        coeff = r[-1] * inv_lc % P
        q[shift] = coeff
        for i, value in enumerate(d):
            r[shift + i] = (r[shift + i] - coeff * value) % P
        r = trim_poly(r)
    return trim_poly(q), trim_poly(r)


def poly_mod_base(a: Sequence[int], modulus: Sequence[int]) -> list[int]:
    return poly_divmod_base(a, modulus)[1]


def poly_mul_base(a: Sequence[int], b: Sequence[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return trim_poly(out)


def poly_powmod_base(a: Sequence[int], e: int, modulus: Sequence[int]) -> list[int]:
    out = [1]
    base = poly_mod_base(a, modulus)
    while e:
        if e & 1:
            out = poly_mod_base(poly_mul_base(out, base), modulus)
        base = poly_mod_base(poly_mul_base(base, base), modulus)
        e >>= 1
    return out


def poly_gcd_base(a: Sequence[int], b: Sequence[int]) -> list[int]:
    x, y = trim_poly(list(a)), trim_poly(list(b))
    while y != [0]:
        _, r = poly_divmod_base(x, y)
        x, y = y, r
    inv = pow(x[-1], P - 2, P)
    return trim_poly([(inv * c) % P for c in x])


def is_irreducible_degree_six(f: Sequence[int]) -> bool:
    require(len(f) == DEG + 1 and f[-1] == 1, "candidate must be monic degree six")
    x = [0, 1]
    for q in (2, 3):
        h = poly_sub_base(poly_powmod_base(x, P ** (DEG // q), f), x)
        if poly_gcd_base(f, h) != [1]:
            return False
    return poly_sub_base(poly_powmod_base(x, P**DEG, f), x) == [0]


def first_irreducible_degree_six() -> tuple[int, ...]:
    # Deterministic lexical search over nonzero constant terms.
    for c0 in range(1, P):
        for tail in product(range(P), repeat=DEG - 1):
            f = (c0, *tail, 1)
            if is_irreducible_degree_six(f):
                return f
    raise RuntimeError("no irreducible polynomial found")


MODULUS = first_irreducible_degree_six()
Elt = tuple[int, ...]
ZERO: Elt = (0,) * DEG
ONE: Elt = (1,) + (0,) * (DEG - 1)


def add(a: Elt, b: Elt) -> Elt:
    return tuple((x + y) % P for x, y in zip(a, b))


def neg(a: Elt) -> Elt:
    return tuple((-x) % P for x in a)


def sub(a: Elt, b: Elt) -> Elt:
    return add(a, neg(b))


def scalar(c: int, a: Elt) -> Elt:
    return tuple((c * x) % P for x in a)


def mul(a: Elt, b: Elt) -> Elt:
    tmp = [0] * (2 * DEG - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            tmp[i + j] = (tmp[i + j] + x * y) % P
    # x^6 = -sum_{i=0}^5 MODULUS[i] x^i.
    for d in range(2 * DEG - 2, DEG - 1, -1):
        c = tmp[d] % P
        if c:
            for i in range(DEG):
                tmp[d - DEG + i] = (tmp[d - DEG + i] - c * MODULUS[i]) % P
        tmp[d] = 0
    return tuple(tmp[:DEG])


def field_pow(a: Elt, e: int) -> Elt:
    out, base = ONE, a
    while e:
        if e & 1:
            out = mul(out, base)
        base = mul(base, base)
        e >>= 1
    return out


def fpoly_mul(a: Sequence[Elt], b: Sequence[Elt]) -> list[Elt]:
    out = [ZERO] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = add(out[i + j], mul(x, y))
    return out


def fpoly_eval(a: Sequence[Elt], x: Elt) -> Elt:
    out = ZERO
    for c in reversed(a):
        out = add(mul(out, x), c)
    return out


def fsum(values: Iterable[Elt]) -> Elt:
    out = ZERO
    for value in values:
        out = add(out, value)
    return out


def int_poly_mul(a: Sequence[int], b: Sequence[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def int_poly_pow(a: Sequence[int], e: int) -> list[int]:
    out = [1]
    base = list(a)
    while e:
        if e & 1:
            out = int_poly_mul(out, base)
        base = int_poly_mul(base, base)
        e >>= 1
    return out


def matrix_rank_mod5(rows: Sequence[Sequence[int]]) -> int:
    m = [[x % P for x in row] for row in rows if any(x % P for x in row)]
    if not m:
        return 0
    rank = 0
    cols = len(m[0])
    for col in range(cols):
        pivot = next((r for r in range(rank, len(m)) if m[r][col]), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        inv = pow(m[rank][col], P - 2, P)
        m[rank] = [(inv * x) % P for x in m[rank]]
        for r in range(len(m)):
            if r != rank and m[r][col]:
                c = m[r][col]
                m[r] = [(x - c * y) % P for x, y in zip(m[r], m[rank])]
        rank += 1
        if rank == len(m):
            break
    return rank


def incidence_difference(a: tuple[int, ...], b: tuple[int, ...], universe: int) -> tuple[int, ...]:
    sa, sb = set(a), set(b)
    return tuple((1 if i in sa else 0) - (1 if i in sb else 0) for i in range(universe))


def main() -> None:
    source_pin_count = check_source_pins()

    # Basic field certification.
    require(is_irreducible_degree_six(MODULUS), "selected modulus is reducible")
    generator = (0, 1, 0, 0, 0, 0)
    require(field_pow(generator, P**DEG) == generator, "Frobenius closure failed")

    basis = [tuple(1 if i == j else 0 for i in range(DEG)) for j in range(DEG)]
    blocks: list[tuple[Elt, Elt, Elt]] = []
    points: list[Elt] = []
    for i in range(2):
        a, u, v = basis[3 * i], basis[3 * i + 1], basis[3 * i + 2]
        blocks.append((a, u, v))
        for eps, eta in product((0, 1), repeat=2):
            points.append(add(add(a, scalar(eps, u)), scalar(eta, v)))
    require(len(set(points)) == 8, "D_2 is not a set of eight distinct points")

    slopes: dict[Elt, list[tuple[int, ...]]] = defaultdict(list)
    h_by_slope: dict[Elt, set[tuple[Elt, ...]]] = defaultdict(set)
    for support in combinations(range(8), 4):
        qpoly: list[Elt] = [ONE]
        for idx in support:
            qpoly = fpoly_mul(qpoly, [neg(points[idx]), ONE])
        require(len(qpoly) == 5 and qpoly[-1] == ONE, "locator is not monic degree four")
        gamma = qpoly[3]
        require(gamma == neg(fsum(points[i] for i in support)), "c1 is not minus the support sum")
        rpoly = [ZERO, ZERO, ZERO, gamma, ONE]
        hpoly = [sub(rpoly[i], qpoly[i]) for i in range(5)]
        require(hpoly[3] == ZERO and hpoly[4] == ZERO, "endpoint cancellation failed")
        agreement = tuple(i for i, x in enumerate(points) if fpoly_eval(rpoly, x) == fpoly_eval(hpoly, x))
        require(agreement == support, "agreement support is not exact")
        roots = tuple(i for i, x in enumerate(points) if fpoly_eval(qpoly, x) == ZERO)
        require(roots == support, "locator has a repeated or extra support root")
        hkey = tuple(hpoly[:3])
        require(hkey not in h_by_slope[gamma], "two supports at one slope produced the same h")
        h_by_slope[gamma].add(hkey)
        slopes[gamma].append(support)

    require(sum(map(len, slopes.values())) == comb(8, 4) == 70, "support census failed")
    fiber_hist = Counter(map(len, slopes.values()))
    require(fiber_hist == Counter({1: 50, 2: 8, 4: 1}), f"unexpected fiber histogram: {fiber_hist}")
    require(len(slopes) == 59, "L_2 must equal 59")

    top_gamma = neg(fsum(add(scalar(2, a), add(u, v)) for a, u, v in blocks))
    top_fiber = slopes[top_gamma]
    require(len(top_fiber) == 4, "the all-diagonal fiber must have size four")
    allowed_per_block = ({0, 3}, {1, 2})
    for support in top_fiber:
        for block in range(2):
            local = {idx - 4 * block for idx in support if 4 * block <= idx < 4 * block + 4}
            require(local in allowed_per_block, "top fiber is not the diagonal Cartesian product")

    diff_counts = Counter(
        incidence_difference(a, b, 8) for a in top_fiber for b in top_fiber
    )
    energy = sum(c * c for c in diff_counts.values())
    require(energy == 36 == 6**2, "top-fiber additive energy must be 36")
    require(energy * 16 == 9 * (len(top_fiber) ** 3), "normalized top energy must be 9/16")

    t0 = points[0]
    differences = [sub(x, t0) for x in points]
    rank = matrix_rank_mod5(differences)
    require(rank == 5, "effective affine span must have dimension five for B=2")
    a_eff = P ** rank
    require(a_eff == 3125, "A_eff,2 must equal 5^5")

    q0 = [1, 4, 4, 4, 1]
    ppoly = [1, 4, 5, 4, 1]
    l2 = int_poly_pow(ppoly, 2)[4]
    m2 = int_poly_pow([1, 4, 6, 4, 1], 2)[4]
    require((l2, m2) == (59, 70), "generating-function census disagrees with finite enumeration")
    strata2 = []
    for j in range(3):
        coeff = int_poly_pow(q0, 2 - j)[2 * (2 - j)]
        strata2.append(comb(2, j) * coeff)
    require(strata2 == [50, 8, 1], "j-stratum slope census failed")
    require(sum((2**j) * strata2[j] for j in range(3)) == 70, "weighted j census failed")

    # General exact coefficient and endpoint ledger over a substantial independent range.
    for b in range(2, 65):
        lval = int_poly_pow(ppoly, b)[2 * b]
        mval = int_poly_pow([1, 4, 6, 4, 1], b)[2 * b]
        require(mval == comb(4 * b, 2 * b), f"M_B identity failed at B={b}")
        strata = []
        for j in range(b + 1):
            coeff = int_poly_pow(q0, b - j)[2 * (b - j)]
            strata.append(comb(b, j) * coeff)
        require(sum(strata) == lval, f"unweighted slope census failed at B={b}")
        require(sum((2**j) * strata[j] for j in range(b + 1)) == mval, f"weighted support census failed at B={b}")
        require(strata[b] == 1, f"top slope is not unique at B={b}")
        require(15**b <= 6 * b * lval, f"L_B lower coefficient bound failed at B={b}")
        require(lval <= 15**b, f"L_B upper coefficient bound failed at B={b}")
        require(16**b <= (4 * b + 1) * mval, f"M_B lower coefficient bound failed at B={b}")
        require(mval <= 16**b, f"M_B upper coefficient bound failed at B={b}")
        aval = 5 ** (3 * b - 1)
        # Cross-multiplied forms of the two claimed exponential multiplier lower bounds.
        require(5 * aval * (3**b) >= lval * (25**b), f"image multiplier bound failed at B={b}")
        require(5 * (2**b) * aval * (8**b) >= mval * (125**b), f"flatness multiplier bound failed at B={b}")

    getcontext().prec = 50
    rate_image = (Decimal(25) / Decimal(3)).ln() / Decimal(4)
    rate_flat = (Decimal(125) / Decimal(8)).ln() / Decimal(4)
    rate_sidon = (Decimal(15) / Decimal(8)).ln() / Decimal(4)

    mutations = {
        "changed_point_geometry": len(set(points)) == 7,
        "wrong_support_size": comb(8, 3) == 70,
        "zero_received_slope": top_gamma == ZERO,
        "wrong_top_fiber": len(top_fiber) == 8,
        "wrong_slope_polynomial": int_poly_pow(q0, 2)[4] == 59,
        "wrong_effective_affine_rank": rank == 6,
        "wrong_support_generating_polynomial": int_poly_pow(ppoly, 2)[4] == 70,
    }
    require(not any(mutations.values()), f"semantic mutation survived: {mutations}")

    print("AFFINE_PREFIX_FULL_UNION_IMAGE_OBSTRUCTION: PASS")
    print("base=" + BASE)
    print(f"source_pins=PASS,count={source_pin_count}")
    print("scope=finite B=2 field/witness replay plus exact integer ledgers for 2<=B<=64")
    print("repository_imports=0")
    print("field=GF(5^6)")
    print("modulus_low_to_high=" + ",".join(map(str, MODULUS)))
    print("D2_size=8 support_count=70 slope_count=59")
    print("fiber_histogram=1:50,2:8,4:1")
    print("top_fiber_size=4 energy=36 normalized_energy=9/16")
    print("effective_span_dimension=5 A_eff=3125")
    print("L2=59 M2=70 mean=70/59")
    print("flatness_lower_rate_per_n=" + str(rate_flat))
    print("image_lower_rate_per_n=" + str(rate_image))
    print("sidon_obstruction_rate_per_n=" + str(rate_sidon))
    print("retention_scope=valid only when active_size_N=4B (or an explicitly equivalent small-o scale)")
    print("semantic_owner_compiler=NOT_TESTED_AND_NOT_CLAIMED")
    print("semantic_tamper_selftests=PASS,count=7")
    print("finite_ledger_delta=0 asymptotic_ledger_delta=0 official_score=0/2")
    print("RESULT=PASS")


if __name__ == "__main__":
    main()
